"""Conservative FFmpeg MP4 renderer: sequential still images + optional audio + SRT.

Supports static images, Ken Burns smooth camera motion (zoom, pan, cut-punch),
background music (BGM) with audio ducking, and modern subtitle styling.
"""
from __future__ import annotations
from pathlib import Path
import shutil
import os
import tempfile
import subprocess
from .project_schema import Project
from .media_paths import validate_media_path
from .subtitles import export_srt, get_subtitle_style
from .motion import resolve_shot_motion, camera_at


def find_ffmpeg() -> str:
    """Prefer a user-managed local binary; fall back to PATH."""
    local = Path(__file__).resolve().parent.parent / 'tools' / 'ffmpeg' / 'bin' / ('ffmpeg.exe' if os.name == 'nt' else 'ffmpeg')
    if local.is_file():
        return str(local)
    found = shutil.which('ffmpeg')
    if not found:
        raise ValueError('FFmpeg not found: place it at tools/ffmpeg/bin/ffmpeg.exe or add to PATH')
    return found


def render_motion_clip(
    image_path: Path,
    dest_path: Path,
    width: int,
    height: int,
    fps: int,
    frames: int,
    shot: dict,
    ffmpeg: str,
    crf: int = 22,
) -> None:
    """Render a single image shot with smooth Ken Burns motion into an MP4 clip."""
    try:
        from PIL import Image
    except ImportError as exc:
        raise ValueError('Rendering with motion requires pillow: pip install pillow') from exc

    im = Image.open(image_path).convert('RGB')
    duration_s = frames / fps

    cmd = [
        ffmpeg, '-hide_banner', '-loglevel', 'error', '-y',
        '-f', 'rawvideo', '-pixel_format', 'rgb24',
        '-video_size', f'{width}x{height}',
        '-framerate', str(fps),
        '-i', 'pipe:0',
        '-an',
        '-c:v', 'libx264', '-preset', 'veryfast', '-crf', str(crf),
        '-pix_fmt', 'yuv420p', '-vf', 'setsar=1',
        '-movflags', '+faststart',
        str(dest_path),
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    try:
        for k in range(frames):
            t_rel = (k / max(1, frames - 1)) * duration_s
            z, px, py = camera_at(shot, t_rel, duration_s)
            scale = min(im.width / width, im.height / height) / z
            x = (im.width - width * scale) * px
            y = (im.height - height * scale) * py
            frame_img = im.transform(
                (width, height),
                Image.Transform.AFFINE,
                (scale, 0, x, 0, scale, y),
                Image.Resampling.BILINEAR,
            )
            proc.stdin.write(frame_img.tobytes())
        proc.stdin.close()
        stderr = proc.stderr.read().decode('utf-8', errors='replace')
        proc.stderr.close()
        if proc.wait() != 0:
            raise RuntimeError(f'FFmpeg motion clip failed: {stderr}')
    except BaseException:
        proc.kill()
        proc.wait()
        raise


def render_mp4(
    project: Project,
    media_root: str | Path,
    output: str | Path,
    *,
    ffmpeg: str | None = None,
    burn_subtitles: bool = False,
    crf: int = 23,
    width: int | None = None,
    height: int | None = None,
    export_srt_files: bool | None = None,
    motion: bool = False,
    bgm_path: str | Path | None = None,
    bgm_volume: float = 0.25,
    ducking: bool = True,
) -> dict:
    project.validate()
    root = Path(media_root).resolve(strict=True)
    if not root.is_dir():
        raise ValueError('media root must be a directory')
    output = Path(output).resolve()
    if output.exists():
        raise FileExistsError('output already exists')
    if output.suffix.lower() != '.mp4':
        raise ValueError('output must end in .mp4')
    if root == output or root in output.parents:
        raise ValueError('output must be outside media root')
    ffmpeg = ffmpeg or find_ffmpeg()
    if not shutil.which(ffmpeg) and not Path(ffmpeg).is_file():
        raise ValueError('FFmpeg executable not found')
    if not isinstance(crf, int) or isinstance(crf, bool) or not 0 <= crf <= 51:
        raise ValueError('CRF must be an integer from 0 to 51')
    # Output dimensions override the small demo project's native 320x180 size.
    width = project.width if width is None else width
    height = project.height if height is None else height
    for value, label in ((width, 'width'), (height, 'height')):
        if isinstance(value, bool) or not isinstance(value, int) or not 2 <= value <= 8192 or value % 2:
            raise ValueError(f'{label} must be an even integer between 2 and 8192')
    # Do not place a same-name SRT next to burned MP4: many players auto-load it.
    if export_srt_files is None:
        export_srt_files = not burn_subtitles
    tracks = {t.id: t.kind for t in project.tracks}
    media = {m.id: m for m in project.media}
    video = sorted((c for c in project.clips if tracks[c.track_id] == 'video'), key=lambda c: (c.start_ms, c.id))
    audio = [c for c in project.clips if tracks[c.track_id] == 'audio']
    if not 1 <= len(video) <= 100:
        raise ValueError('requires 1..100 image clips')
    cursor = 0
    for clip in video:
        if media[clip.media_id].kind != 'image' or clip.source_in_ms != 0:
            raise ValueError('only still images with source_in_ms=0 supported')
        if clip.start_ms != cursor:
            raise ValueError('image clips must be contiguous starting at zero')
        cursor += clip.duration_ms
        if clip.duration_ms % (1000 / project.fps) != 0:
            raise ValueError('clip duration must align to full video frames')
    if len(audio) > 32:
        raise ValueError('maximum 32 audio clips supported')
    for clip in audio:
        if media[clip.media_id].kind != 'audio':
            raise ValueError('audio clip requires audio asset')
        if clip.start_ms + clip.duration_ms > cursor:
            raise ValueError('audio clip exceeds video duration')

    def source(rel):
        safe = validate_media_path(rel)
        path = (root / safe).resolve(strict=True)
        if root not in path.parents or not path.is_file():
            raise ValueError('media path escapes root or is not a file')
        return path

    sources = [source(media[c.media_id].path) for c in video]
    audio_paths = [source(media[c.media_id].path) for c in audio]

    bgm_file = None
    if bgm_path is not None:
        bgm_file = Path(bgm_path).resolve(strict=True)
        if not bgm_file.is_file():
            raise FileNotFoundError(f"BGM audio file not found: {bgm_file}")

    tempdir = None
    if motion or burn_subtitles:
        tempdir = tempfile.TemporaryDirectory(prefix='story-studio-render-')

    command = [ffmpeg, '-hide_banner', '-loglevel', 'error', '-nostdin', '-n']

    if motion:
        motion_clips = []
        for i, (clip, path) in enumerate(zip(video, sources)):
            frames = int(round(clip.duration_ms * project.fps / 1000))
            shot = {'id': clip.id, 'duration_s': clip.duration_ms / 1000}
            resolve_shot_motion(shot, index=i, total_shots=len(video), preset_mode=True)
            clip_dest = Path(tempdir.name) / f'motion_v{i}.mp4'
            render_motion_clip(path, clip_dest, width, height, project.fps, frames, shot, ffmpeg, crf)
            motion_clips.append(clip_dest)
            command += ['-i', str(clip_dest)]
        filters = ''.join(f'[{i}:v]setsar=1,format=yuv420p[v{i}];' for i in range(len(video)))
        filters += ''.join(f'[v{i}]' for i in range(len(video))) + f'concat=n={len(video)}:v=1:a=0[vout]'
    else:
        for clip, path in zip(video, sources):
            command += ['-loop', '1', '-framerate', str(project.fps), '-t', f'{clip.duration_ms / 1000:.3f}', '-i', str(path)]
        filters = ''.join(f'[{i}:v]scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p[v{i}];' for i in range(len(video)))
        filters += ''.join(f'[v{i}]' for i in range(len(video))) + f'concat=n={len(video)}:v=1:a=0[vout]'

    for path in audio_paths:
        command += ['-i', str(path)]

    if bgm_file is not None:
        command += ['-i', str(bgm_file)]

    has_audio_stream = bool(audio) or (bgm_file is not None)
    dur_s = cursor / 1000.0

    if audio:
        for i, clip in enumerate(audio):
            filters += (f';[{len(video)+i}:a:0]atrim=start={clip.source_in_ms/1000:.3f}:'
                        f'duration={clip.duration_ms/1000:.3f},asetpts=PTS-STARTPTS,'
                        f'aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,'
                        f'adelay={clip.start_ms}:all=1[a{i}]')
        if len(audio) > 1:
            filters += ';' + ''.join(f'[a{i}]' for i in range(len(audio))) + (
                f'amix=inputs={len(audio)}:duration=longest:normalize=0,atrim=duration={dur_s:.3f}[voice_mix]'
            )
        else:
            filters += ';[a0]anull[voice_mix]'

    if bgm_file is not None:
        bgm_idx = len(video) + len(audio)
        fade_out_st = max(0.0, dur_s - 1.5)
        fade_out_dur = min(1.5, dur_s)
        fade_in_dur = min(1.0, dur_s)
        filters += (
            f';[{bgm_idx}:a:0]aloop=loop=-1:size=2e+09,atrim=0:{dur_s:.3f},'
            f'asetpts=PTS-STARTPTS,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo,'
            f'afade=t=in:st=0:d={fade_in_dur:.3f},afade=t=out:st={fade_out_st:.3f}:d={fade_out_dur:.3f},'
            f'volume={bgm_volume:.3f}[bgm_raw]'
        )
        if audio and ducking:
            filters += (
                ';[voice_mix]asplit=2[voice_play][voice_sc]'
                ';[bgm_raw][voice_sc]sidechaincompress=threshold=0.08:ratio=4:attack=150:release=350[bgm_ducked]'
                ';[voice_play][bgm_ducked]amix=inputs=2:duration=longest:normalize=0[aout]'
            )
        elif audio:
            filters += ';[voice_mix][bgm_raw]amix=inputs=2:duration=longest:normalize=0[aout]'
        else:
            filters += ';[bgm_raw]anull[aout]'
    elif audio:
        filters += ';[voice_mix]anull[aout]'

    command += ['-filter_complex', filters, '-map', '[vout]']
    if has_audio_stream:
        command += ['-map', '[aout]', '-c:a', 'aac', '-b:a', '128k']
    else:
        command += ['-an']

    if burn_subtitles:
        if len([t for t in project.tracks if t.kind == 'subtitle']) != 1:
            raise ValueError('burn-in requires exactly one subtitle track')
        srt = Path(tempdir.name) / 'captions.srt'
        track = next(t for t in project.tracks if t.kind == 'subtitle')
        srt.write_text(export_srt(project, track_id=track.id), encoding='utf-8')
        style = get_subtitle_style(width, height)
        command[command.index('-filter_complex') + 1] = filters + ';[vout]subtitles=captions.srt:force_style=\'' + style + '\'[vburn]'
        command[command.index('-map') + 1] = '[vburn]'

    command += ['-c:v', 'libx264', '-crf', str(crf), '-pix_fmt', 'yuv420p', '-r', str(project.fps), '-movflags', '+faststart', '-t', f'{cursor/1000:.3f}', str(output)]
    subtitle_tracks = [t for t in project.tracks if t.kind == 'subtitle']
    subtitle_targets = ([output.with_name(f'{output.stem}.sub{i:02}.srt') for i in range(1, len(subtitle_tracks)+1)] if export_srt_files else [])
    if any(path.exists() for path in subtitle_targets):
        raise FileExistsError('subtitle output already exists')
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        subprocess.run(command, check=True, capture_output=True, text=True, timeout=300, cwd=tempdir.name if tempdir else None)
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
        output.unlink(missing_ok=True)
        raise ValueError(f'FFmpeg failed: {str(getattr(exc, "stderr", "timeout"))[-1200:]}') from exc
    finally:
        if tempdir:
            tempdir.cleanup()

    srt_paths = []
    for path, track in zip(subtitle_targets, subtitle_tracks):
        path.write_text(export_srt(project, track_id=track.id), encoding='utf-8-sig')
        srt_paths.append(str(path))

    return {
        'video': str(output),
        'subtitles': srt_paths,
        'duration_ms': cursor,
        'clips': len(video),
        'burned_subtitles': burn_subtitles,
        'crf': crf,
        'width': width,
        'height': height,
        'motion': motion,
        'bgm': str(bgm_file) if bgm_file else None,
        'ducking': ducking if bgm_file else False,
    }
