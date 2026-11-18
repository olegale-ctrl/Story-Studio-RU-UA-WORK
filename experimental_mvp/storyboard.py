"""Experimental local storyboard. No production authorization is represented here."""
from dataclasses import asdict, dataclass
from hashlib import sha256
import json
from pathlib import Path
import shutil
import uuid

MODES = ('AI_VIDEO', 'AI_IMAGE', 'IMAGE_PAN_ZOOM', 'LOCAL_VIDEO', 'STOCK_VIDEO',
         'MAP', 'INFOGRAPHIC', 'TEXT_ANIMATION', 'PLACEHOLDER')
STATUSES = ('PLANNED', 'READY', 'WAITING_FOR_QUOTA', 'WAITING_FOR_USER', 'GENERATING',
            'IMPORTED', 'FAILED', 'SKIPPED')
IMAGES = {'.png', '.jpg', '.jpeg', '.webp', '.bmp'}
VIDEOS = {'.mp4', '.mov', '.mkv', '.webm'}


@dataclass
class VideoAnchor:
    anchor_id: str
    scene_id: str
    start_ms: int
    duration_ms: int
    narration_excerpt: str = ''
    visual_description: str = ''
    image_prompt: str = ''
    video_prompt: str = ''
    negative_prompt: str = ''
    reference_image: str = ''
    preferred_provider: str = ''
    provider_model: str = ''
    generation_mode: str = 'PLACEHOLDER'
    generation_status: str = 'PLANNED'
    local_asset_path: str = ''
    license_status: str = 'UNKNOWN'
    fallback_mode: str = 'NONE'


def suggest(scene, total_ms, step_ms=7000):
    """Never replace existing anchors or assets implicitly."""
    if scene.get('anchors'):
        raise ValueError('Якоря уже существуют; редактируйте их явно, материалы сохранены.')
    if type(total_ms) is not int or total_ms <= 0 or type(step_ms) is not int or step_ms <= 0:
        raise ValueError('Длительность должна быть положительным целым числом мс.')
    return [asdict(VideoAnchor(uuid.uuid4().hex, scene['id'], start,
                              min(step_ms, total_ms-start), scene.get('text', ''),
                              scene.get('visual', ''), scene.get('prompt', ''),
                              scene.get('prompt', '')))
            for start in range(0, total_ms, step_ms)]


def validate(scene, total_ms):
    anchors = scene.get('anchors', [])
    if not anchors:
        return []  # Explicit legacy scene-image / color mode.
    errors, ids, end = [], set(), 0
    for a in sorted(anchors, key=lambda a: a.get('start_ms', -1)):
        key = a.get('anchor_id')
        if not isinstance(key, str) or not key or key in ids:
            errors.append('Отсутствующий / повторный anchor_id')
        ids.add(key)
        if a.get('scene_id') != scene['id']:
            errors.append(f'{key}: чужая сцена')
        start, length = a.get('start_ms'), a.get('duration_ms')
        if type(start) is not int or type(length) is not int or start < 0 or length <= 0:
            errors.append(f'{key}: неверное время'); continue
        if start != end:
            errors.append(f'{key}: пробел или перекрытие {end} → {start} мс')
        end = start + length
        if a.get('generation_mode') not in MODES or a.get('generation_status') not in STATUSES:
            errors.append(f'{key}: неизвестный режим / статус')
        path = a.get('local_asset_path')
        if path:
            p = Path(path).expanduser()
            if not p.is_file() or p.suffix.lower() not in IMAGES | VIDEOS:
                errors.append(f'{key}: файл отсутствует / неподдерживаемый путь')
            elif a.get('asset_sha256') and sha256(p.read_bytes()).hexdigest() != a['asset_sha256']:
                errors.append(f'{key}: материал изменился после импорта')
        elif a.get('generation_mode') == 'TEXT_ANIMATION' and (a.get('visual_description') or a.get('narration_excerpt')):
            pass
        elif a.get('fallback_mode') != 'PLACEHOLDER':
            errors.append(f'{key}: нет материала; явно разрешите PLACEHOLDER fallback')
    if end != total_ms:
        errors.append(f'Покрытие {end} мс ≠ озвучка {total_ms} мс; исправьте шкалу явно')
    return errors


def reorder(scene, anchor_id, offset):
    items = sorted(scene['anchors'], key=lambda a: a['start_ms'])
    index = next(i for i, a in enumerate(items) if a['anchor_id'] == anchor_id)
    target = index + offset
    if 0 <= target < len(items):
        items[index], items[target] = items[target], items[index]
    start = 0
    for a in items:
        a['start_ms'] = start
        start += a['duration_ms']
    scene['anchors'] = items


def split(scene, anchor_id, max_ms):
    """Explicit split retaining originals and source offsets; no generation requests."""
    from copy import deepcopy
    if type(max_ms) is not int or max_ms <= 0:
        raise ValueError('Неверная длительность части.')
    index = next(i for i, a in enumerate(scene['anchors']) if a['anchor_id'] == anchor_id)
    original = scene['anchors'][index]
    parts = []
    for offset in range(0, original['duration_ms'], max_ms):
        part = deepcopy(original)
        part.update(anchor_id=original['anchor_id'] if offset == 0 else uuid.uuid4().hex,
                    start_ms=original['start_ms']+offset, duration_ms=min(max_ms, original['duration_ms']-offset),
                    source_start_ms=original.get('source_start_ms', 0)+offset)
        parts.append(part)
    scene['anchors'][index:index+1] = parts
    return parts


def fingerprint(anchor):
    fields = ('image_prompt', 'video_prompt', 'negative_prompt', 'reference_image',
              'preferred_provider', 'provider_model', 'generation_mode', 'duration_ms')
    payload = {k: anchor.get(k, '') for k in fields}
    ref = payload['reference_image']
    if ref:
        payload['reference_sha256'] = sha256(Path(ref).read_bytes()).hexdigest()
    return sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def import_asset(anchor, source, workspace, *, provider='MANUAL', license_status='UNKNOWN'):
    source = Path(source).expanduser().resolve(strict=True)
    if source.suffix.lower() not in IMAGES | VIDEOS or not source.is_file():
        raise ValueError('Импортируйте изображение или MP4/MOV/MKV/WebM.')
    content = source.read_bytes()
    digest = sha256(content).hexdigest()
    folder = Path(workspace) / 'assets'
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / (digest + source.suffix.lower())
    if not target.exists():
        # Content addressed, never overwrite an existing user asset.
        with target.open('xb') as stream:
            stream.write(content)
    elif sha256(target.read_bytes()).hexdigest() != digest:
        raise ValueError('Повреждён локальный кэш материала.')
    anchor.update(local_asset_path=str(target.resolve()), asset_sha256=digest,
                  generation_status='IMPORTED', license_status=license_status,
                  provenance={'provider': provider, 'original_name': source.name,
                              'prompt_fingerprint': fingerprint(anchor), 'sha256': digest})
    return target


def video_spec(anchor, strict=True):
    """Probe actual input, do not trust project duration metadata."""
    import subprocess
    from experimental_mvp.pipeline import executable
    source=Path(anchor['local_asset_path']).expanduser().resolve(strict=True)
    probe=subprocess.run([executable('ffprobe'),'-v','error','-select_streams','v:0',
                          '-show_entries','stream=codec_type:format=duration','-of','json',str(source)],
                         capture_output=True,check=True,timeout=25)
    value=json.loads(probe.stdout)
    if not value.get('streams'):raise ValueError('Нет видеопотока.')
    measured=round(float(value['format']['duration'])*1000)
    start=anchor.get('source_start_ms',0);end=anchor.get('source_end_ms',measured)
    if type(start) is not int or type(end) is not int or not 0<=start<end<=measured+1:
        raise ValueError('Неверный исходный интервал видеоклипа.')
    policy=anchor.get('short_clip_policy','ERROR' if strict else 'HOLD_LAST_FRAME')
    if policy not in ('ERROR','HOLD_LAST_FRAME','LOOP'):raise ValueError('Неверное решение для короткого клипа.')
    if end-start<anchor['duration_ms'] and policy=='ERROR':
        raise ValueError(f"Клип {measured} мс, используемый интервал {end-start} мс короче якоря {anchor['duration_ms']} мс. Выберите trim / HOLD_LAST_FRAME / LOOP явно.")
    return dict(measured_ms=measured,start_ms=start,end_ms=end,available_ms=end-start,policy=policy)


def render(scene, index, length, folder, log, ffmpeg, command, profile=None, cancelled=lambda: False):
    """Normalize every anchor to the same profile. Short video holds its last frame."""
    errors = validate(scene, round(length * 1000))
    if errors:
        raise ValueError('\n'.join(errors))
    width, height, fps = output_profile(profile)
    strict = bool(profile and profile.get("timeline_version"))
    clips = []
    inputs = []
    for n, anchor in enumerate(sorted(scene['anchors'], key=lambda a: a['start_ms'])):
        if cancelled():
            from experimental_mvp.pipeline import BuildStopped
            raise BuildStopped('Сборка остановлена между якорями.')
        seconds = anchor['duration_ms'] / 1000
        absolute = (profile or {}).get('scene_start_ms',0)
        frames = round((absolute+anchor['start_ms']+anchor['duration_ms'])*fps/1000)-round((absolute+anchor['start_ms'])*fps/1000)
        if strict and frames<1:raise ValueError('Якорь короче одного выходного кадра.')
        spec = None
        source = anchor.get('local_asset_path')
        args = []
        if source:
            p = Path(source).resolve(strict=True)
            suffix = p.suffix.lower()
            local = folder / f'anchor{index:03}_{n:03}{suffix}'
            shutil.copyfile(p, local)
            if anchor.get('asset_sha256') and sha256(local.read_bytes()).hexdigest() != anchor['asset_sha256']:
                raise ValueError('Материал подменён перед исполнением.')
            args = ['-loop', '1', '-framerate', str(fps)] if suffix in IMAGES else []
            args += ['-i', local.name]
            if suffix in VIDEOS:
                spec = video_spec({**anchor,'local_asset_path':str(local)}, strict)
                if not strict and 'short_clip_policy' not in anchor:
                    with log.open('a',encoding='utf-8') as stream:stream.write('LEGACY: implicit hold-last-frame; choose an explicit policy in timeline v1.\n')
            inputs.append({'anchor_id': anchor['anchor_id'], 'sha256': sha256(local.read_bytes()).hexdigest(),
                           'copied_input': local.name, 'source_start_ms': anchor.get('source_start_ms', 0),
                           'source_interval': spec, 'fit_mode': anchor.get('fit_mode','FIT'),
                           'timeline_duration_ms': anchor['duration_ms'], 'output_frames': frames if strict else None,
                           'license_status': anchor.get('license_status', 'UNKNOWN')})
        else:
            args = ['-f', 'lavfi', '-i', f'color=c=0x17365a:s={width}x{height}:r={fps}']
        if anchor.get('fit_mode','FIT') == 'CROP':
            sizing=f'scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height}'
        else:
            sizing=f'scale={width}:{height}:force_original_aspect_ratio=decrease,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2'
        prefix = f"trim=start={spec['start_ms']/1000}:end={spec['end_ms']/1000},setpts=PTS-STARTPTS," if spec else ''
        filters = prefix+sizing+f',setsar=1,fps={fps},format=yuv420p'
        if spec and spec['policy']=='LOOP':
            count=max(1,round(spec['available_ms']*fps/1000))
            filters += f',loop=loop=-1:size={count}:start=0,settb=expr=1/{fps},setpts=N'
        # Padding is explicit in timeline projects. Legacy projects retain published behavior.
        if not spec or spec['policy']=='HOLD_LAST_FRAME' or not strict:
            filters += f',tpad=stop_mode=clone:stop_duration={seconds}'
        if not source and anchor['generation_mode'] == 'TEXT_ANIMATION':
            import os
            import textwrap
            fonts = [Path(anchor.get('text_font_path') or '__no_font__'),
                     Path(os.environ.get('WINDIR', 'C:/Windows'))/'Fonts'/'arial.ttf',
                     Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')]
            font = next((f for f in fonts if f.is_file()), None)
            if font is None:
                raise ValueError('Для TEXT_ANIMATION задайте text_font_path к локальному TTF.')
            shutil.copyfile(font, folder/'animation-font.ttf')
            text = anchor.get('visual_description') or anchor['narration_excerpt']
            text_name = f'animation{index:03}_{n:03}.txt'
            (folder/text_name).write_text('\n'.join(textwrap.wrap(text[:180], 34)), encoding='utf-8')
            filters += (f",drawtext=fontfile=animation-font.ttf:textfile={text_name}:expansion=none:"
                        "fontcolor=white:fontsize=20:x='max(16,40-t*4)':y=(h-text_h)/2")
        if source and Path(source).suffix.lower() in IMAGES and anchor['generation_mode'] == 'IMAGE_PAN_ZOOM':
            filters += f",zoompan=z='min(zoom+0.0005,1.08)':d=1:s={width}x{height}:fps={fps}"
        name = f'visual{index:03}_{n:03}.mp4'
        command([ffmpeg, '-nostdin', '-v', 'error', '-xerror', *args, '-an', '-vf', filters,
                 *(['-frames:v',str(frames)] if strict else ['-t',str(seconds)]),
                 *(['-r',str(fps)] if strict or (spec and spec['policy']=='LOOP') else []), '-c:v', 'libx264', '-preset', 'ultrafast', '-threads', '4', name], folder, log)
        clips.append(name)
    (folder / f'anchor-inputs{index:03}.json').write_text(json.dumps(inputs, ensure_ascii=False, indent=2), encoding='utf-8')
    listing = f'anchors{index:03}.txt'
    (folder / listing).write_text(''.join(f"file '{name}'\n" for name in clips), encoding='ascii')
    name = f'scene{index:03}.mp4'
    command([ffmpeg, '-nostdin', '-v', 'error', '-f', 'concat', '-safe', '1', '-i', listing,
             *(['-frames:v',str(sum(round((absolute+a['start_ms']+a['duration_ms'])*fps/1000)-round((absolute+a['start_ms'])*fps/1000) for a in scene['anchors']))] if strict else ['-t',str(length)]), '-c', 'copy', name], folder, log)
    return name


def output_profile(profile=None):
    p = profile or {}
    w, h, fps = p.get('width', 1920), p.get('height', 1080), p.get('fps', 30)
    if any(type(x) is not int for x in (w, h, fps)) or not (160 <= w <= 3840 and 90 <= h <= 2160 and 1 <= fps <= 60) or w % 2 or h % 2:
        raise ValueError('Неверный профиль вывода (чётные размеры, FPS 1–60).')
    return w, h, fps
