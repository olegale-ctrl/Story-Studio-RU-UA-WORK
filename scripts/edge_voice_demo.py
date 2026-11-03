"""Generate a RU/UA narrated demo with Edge TTS, then optionally render MP4.

Network service: Edge Read Aloud via third-party edge-tts; not licensed for commercial distribution by this project.
"""
from __future__ import annotations
import argparse
import hashlib
import re
import shutil
import json
from pathlib import Path
import subprocess
import sys
import time

VOICES = {
    'uk': {'female': 'uk-UA-PolinaNeural', 'male': 'uk-UA-OstapNeural'},
    'ru': {'female': 'ru-RU-SvetlanaNeural', 'male': 'ru-RU-DmitryNeural'},
}

def resolve_voice(locale: str, voice: str | None, gender: str) -> str:
    if locale not in VOICES: raise ValueError('Only ru/uk supported')
    result = voice or VOICES[locale][gender]
    if not result.startswith(('uk-UA-' if locale == 'uk' else 'ru-RU-')):
        raise ValueError('Voice locale does not match content locale')
    return result

def run(cmd: list[str]) -> None:
    print('RUN:', ' '.join(cmd), flush=True)
    subprocess.run(cmd, check=True)

def ffmpeg_executable(root: Path) -> str:
    for candidate in (root/'tools/ffmpeg/bin/ffmpeg.exe',root/'tools/ffmpeg/bin/ffmpeg'):
        if candidate.is_file(): return str(candidate)
    return 'ffmpeg'

def valid_audio(path: Path, ffprobe: str = 'ffprobe') -> bool:
    """Check that an audio stream exists and the container is readable."""
    if not path.is_file() or path.stat().st_size < 1024:
        return False
    try:
        result = subprocess.run([ffprobe, '-v', 'error', '-select_streams', 'a:0',
            '-show_entries', 'stream=codec_name,duration', '-of', 'default=noprint_wrappers=1',
            str(path)], capture_output=True, text=True, check=False, timeout=30)
    except (OSError, subprocess.TimeoutExpired):
        return False
    return result.returncode == 0 and 'codec_name=' in result.stdout


def cache_key(voice: str, line: str, rate: str = '+0%', pitch: str = '+0Hz') -> str:
    payload = json.dumps({'provider': 'edge-tts', 'voice': voice, 'text': line,
                          'rate': rate, 'pitch': pitch}, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()


def safe_voice_name(voice: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_-]', '_', voice).lower()


def next_video_path(root: Path, locale: str, voice: str) -> Path:
    stem = f'narrated-{locale}-{safe_voice_name(voice)}-s17'
    first = root / f'{stem}.mp4'
    if not first.exists():
        return first
    for index in range(2, 10000):
        candidate = root / f'{stem}-{index:03d}.mp4'
        if not candidate.exists():
            return candidate
    raise RuntimeError('Too many output versions')


def synthesize(voice: str, line: str, mp3: Path, ffprobe: str = 'ffprobe',
               attempts: int = 3, rate: str = '+0%', pitch: str = '+0Hz',
               allow_fallback: bool = True) -> None:
    """Synthesize atomically, recording actual settings when fallback is used.

    A fallback never silently masquerades as requested settings in the cache.
    """
    mp3.parent.mkdir(parents=True, exist_ok=True)
    key = cache_key(voice, line, rate, pitch)
    stamp = mp3.with_suffix('.cache.json')
    try:
        record = json.loads(stamp.read_text(encoding='utf-8'))
    except (FileNotFoundError, ValueError, OSError):
        record = {}
    if record.get('key') == key and valid_audio(mp3, ffprobe):
        if record.get('fallback'):
            print('WARNING: CACHED fallback audio uses settings:',
                  record.get('actual_rate'), record.get('actual_pitch'), flush=True)
        print('CACHED:', mp3, flush=True)
        return

    # Preserve existing validated audio until replacement has passed validation.
    # Do not leave stale metadata pointing at newly synthesized audio.
    stamp.unlink(missing_ok=True)
    temp = mp3.with_name(mp3.stem + '.partial.mp3')
    settings = [(rate, pitch)]
    if allow_fallback and pitch != '+0Hz':
        settings.append((rate, '+0Hz'))
    if allow_fallback and rate != '+0%':
        settings.append(('+0%', '+0Hz'))
    for actual_rate, actual_pitch in settings:
        if (actual_rate, actual_pitch) != (rate, pitch):
            print(f'WARNING: TTS fallback to rate={actual_rate}, pitch={actual_pitch}; '
                  'requested voice settings could not be produced.', flush=True)
        for attempt in range(1, attempts + 1):
            temp.unlink(missing_ok=True)
            command = [sys.executable, '-m', 'edge_tts', '--voice', voice,
                       '--text', line, '--rate', actual_rate, '--pitch', actual_pitch,
                       '--write-media', str(temp)]
            print(f'TTS attempt {attempt}/{attempts}: {voice} '
                  f'rate={actual_rate} pitch={actual_pitch}', flush=True)
            try:
                result = subprocess.run(command, check=False, timeout=120)
                success = result.returncode == 0 and valid_audio(temp, ffprobe)
            except (OSError, subprocess.TimeoutExpired) as exc:
                print(f'WARNING: TTS command failed: {exc}', flush=True)
                success = False
            if success:
                # Metadata written only after the MP3 has been validated.
                temp.replace(mp3)
                metadata = {'key': key, 'voice': voice, 'requested_rate': rate,
                            'requested_pitch': pitch, 'actual_rate': actual_rate,
                            'actual_pitch': actual_pitch,
                            'fallback': (actual_rate, actual_pitch) != (rate, pitch)}
                temp_stamp = stamp.with_name(stamp.name + '.partial')
                temp_stamp.write_text(json.dumps(metadata, ensure_ascii=False), encoding='utf-8')
                temp_stamp.replace(stamp)
                return
            temp.unlink(missing_ok=True)
            if attempt < attempts:
                time.sleep(min(attempt * 2, 6))
    temp.unlink(missing_ok=True)
    raise RuntimeError(f'Edge TTS did not produce valid audio for {voice}; '
                       f'tried {len(settings)} settings profiles x {attempts} attempts.')


def build(locale: str, gender: str, voice: str | None, output: Path, render: bool, crf: int, export_srt: bool, rate: str = '+0%', pitch: str = '+0Hz', preview: bool = False, preview_text: str | None = None, allow_fallback: bool = True) -> None:
    root = Path(__file__).resolve().parents[1]
    selected = resolve_voice(locale, voice, gender)
    sys.path.insert(0,str(root/'scripts'))
    from build_narrated_demo import LINES, build as build_project
    # Separate project/media for each voice: no cross-voice reuse of WAV or MP3.
    output = output / safe_voice_name(selected)
    if rate != '+0%' or pitch != '+0Hz':
        output = output / ('settings-' + hashlib.sha256(f'{rate}|{pitch}'.encode()).hexdigest()[:12])
    media = output/'media'
    media.mkdir(parents=True,exist_ok=True)
    ffmpeg = ffmpeg_executable(root)
    ffprobe = str(Path(ffmpeg).with_name('ffprobe.exe')) if Path(ffmpeg).is_file() and Path(ffmpeg).suffix == '.exe' else 'ffprobe'
    if preview:
        sample = preview_text or ('Это пример выбранного голоса.' if locale == 'ru' else 'Це приклад вибраного голосу.')
        target = media / ('preview-' + hashlib.sha256(sample.encode('utf-8')).hexdigest()[:12] + '.mp3')
        synthesize(selected, sample, target, ffprobe, rate=rate, pitch=pitch, allow_fallback=allow_fallback)
        print('PREVIEW:', target.resolve())
        return
    for index, line in enumerate(LINES[locale],1):
        mp3 = media/f'voice{index}.mp3'
        wav = media/f'voice{index}.wav'
        synthesize(selected, line, mp3, ffprobe, rate=rate, pitch=pitch, allow_fallback=allow_fallback)
        run([ffmpeg,'-hide_banner','-loglevel','error','-y','-i',str(mp3),'-ar','24000','-ac','1','-c:a','pcm_s16le',str(wav)])
        if not wav.is_file() or wav.stat().st_size <= 44: raise RuntimeError(f'Empty WAV: {wav}')
    project = build_project(locale,output)
    run([sys.executable,str(root/'scripts/inspect_voice_demo.py'),'--locale',locale,'--project-dir',str(output)])
    run([sys.executable,'-m','core.cli','check',str(project)])
    if render:
        video = next_video_path(root, locale, selected) if rate == '+0%' and pitch == '+0Hz' else next_video_path(root, locale, selected + '-settings-' + hashlib.sha256(f'{rate}|{pitch}'.encode()).hexdigest()[:12])
        cmd=[sys.executable,'-m','core.cli','render-mp4',str(project),'--media-root',str(media),'--output',str(video),'--burn-subtitles','--width','1920','--height','1080','--crf',str(crf)]
        if export_srt: cmd.append('--export-srt')
        run(cmd)
        print('SUCCESS:',video)
    else:
        print('SUCCESS: project:',project)

def main():
    p=argparse.ArgumentParser(description='RU/UA Edge TTS narrated video')
    p.add_argument('--locale',choices=['ru','uk'],default='uk')
    p.add_argument('--gender',choices=['female','male'],default='female')
    p.add_argument('--voice')
    p.add_argument('--list-voices',action='store_true')
    p.add_argument('--output-dir',type=Path)
    p.add_argument('--no-render',action='store_true')
    p.add_argument('--export-srt',action='store_true')
    p.add_argument('--crf',type=int,default=22)
    p.add_argument('--rate',default='+0%',help='Edge TTS speech rate, e.g. +10%% or -15%%')
    p.add_argument('--pitch',default='+0Hz',help='Edge TTS pitch, e.g. +5Hz or -10Hz')
    p.add_argument('--preview',action='store_true',help='Generate short MP3 only, no video')
    p.add_argument('--preview-text',help='Optional preview text')
    p.add_argument('--strict-voice-settings',action='store_true',help='Fail rather than fallback to default settings')
    args=p.parse_args()
    if args.list_voices:
        for locale, sexes in VOICES.items():
            for sex, name in sexes.items(): print(f'{locale} {sex}: {name}')
        print('Full online catalog: python -m edge_tts --list-voices')
        return
    if not 0<=args.crf<=51: p.error('--crf must be between 0 and 51')
    if not re.fullmatch(r'[+-]\d{1,3}%',args.rate) or int(args.rate[:-1]) not in range(-100,101): p.error('Invalid --rate (allowed -100%..+100%)')
    if not re.fullmatch(r'[+-]\d{1,3}Hz',args.pitch) or int(args.pitch[:-2]) not in range(-100,101): p.error('Invalid --pitch (allowed -100Hz..+100Hz)')
    out=args.output_dir or Path('examples')/f'narrated_{args.locale}'
    build(args.locale,args.gender,args.voice,out,not args.no_render,args.crf,args.export_srt,args.rate,args.pitch,args.preview,args.preview_text,not args.strict_voice_settings)
if __name__=='__main__': main()
