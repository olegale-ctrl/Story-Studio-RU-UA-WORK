"""Validate a locally generated narrated demo without extra Python packages."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import wave


def inspect(root: Path, locale: str) -> dict:
    if locale not in ('ru', 'uk'):
        raise ValueError('locale must be ru or uk')
    project_path = root / 'narrated_project.json'
    project = json.loads(project_path.read_text(encoding='utf-8'))
    if project.get('content_locale') != locale or project.get('schema_version') != 3:
        raise ValueError('wrong locale or project schema')
    clips = project.get('clips', [])
    audio_clips = [c for c in clips if c.get('track_id') == 'a']
    video_clips = [c for c in clips if c.get('track_id') == 'v']
    captions = project.get('subtitles', [])
    if not (len(audio_clips) == len(video_clips) == len(captions) == 3):
        raise ValueError('expected 3 audio, video and subtitle segments')
    media = {m['id']: m for m in project['media']}
    total = 0
    for i in range(3):
        a, v, s = audio_clips[i], video_clips[i], captions[i]
        wav = root / 'media' / media[a['media_id']]['path']
        img = root / 'media' / media[v['media_id']]['path']
        if not img.is_file():
            raise FileNotFoundError(img)
        with wave.open(str(wav), 'rb') as f:
            if f.getnframes() <= 0 or f.getframerate() <= 0:
                raise ValueError('empty WAV')
            duration = (f.getnframes() * 1000 + f.getframerate() - 1) // f.getframerate()
        if abs(duration - a['duration_ms']) > 1:
            raise ValueError('WAV duration differs from audio clip')
        if a['start_ms'] != total or v['start_ms'] != total or s['start_ms'] != total:
            raise ValueError('scene and captions out of sync')
        if s['duration_ms'] != a['duration_ms'] or v['duration_ms'] < a['duration_ms']:
            raise ValueError('captions/audio exceed scene')
        total += v['duration_ms']
    return {'locale': locale, 'scenes': 3, 'duration_ms': total, 'wav_segments': 3, 'subtitles': 3}


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument('--locale', choices=['ru', 'uk'], required=True)
    p.add_argument('--project-dir', type=Path)
    a = p.parse_args()
    root = a.project_dir or Path('examples') / ('narrated_' + a.locale)
    try:
        print('OK:', json.dumps(inspect(root, a.locale), ensure_ascii=False))
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print('ERROR:', exc)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
