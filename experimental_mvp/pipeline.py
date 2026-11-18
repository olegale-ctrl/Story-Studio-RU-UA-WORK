"""Local experimental rendering, separate from Story Studio release storage."""
import argparse
from contextlib import contextmanager
from contextvars import ContextVar
import time
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import uuid

from experimental_mvp.captions import CueError, calculated, render_srt, validate

VOICES = {"ru": "ru-RU-SvetlanaNeural", "uk": "uk-UA-PolinaNeural"}
ROOT = Path(os.environ.get("STORY_MVP_HOME") or (Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "StoryStudioMVP")).resolve()
DEMOS = Path(__file__).with_name("demos")


def synthesize(*args, **kwargs):
    try:
        from scripts.edge_voice_demo import synthesize as online_synthesis
    except ModuleNotFoundError as exc:
        if exc.name not in {"scripts", "scripts.edge_voice_demo"}:
            raise
        raise RuntimeError(
            "Адаптер Edge отсутствует. Для онлайн-озвучки откройте полный checkout "
            "и установите requirements-edge-win-amd64.txt. Для локальной сборки "
            "импортируйте MP3/WAV сцены или общую дорожку проекта."
        ) from exc
    return online_synthesis(*args, **kwargs)


def save(path, project):
    if "scenes" in project:
        from copy import deepcopy
        project = deepcopy(project) if project.get("timeline") else project
        identify(project)
        if project.get("timeline"):
            from experimental_mvp.timeline import validate_project
            validate_project(project)
    # Serialize before touching disk; verify the exact bytes read back before replace.
    payload=json.dumps(project,ensure_ascii=False,indent=2,allow_nan=False)+"\n"
    path.parent.mkdir(parents=True,exist_ok=True)
    temp=None
    try:
        with tempfile.NamedTemporaryFile(mode="w",encoding="utf-8",newline="",dir=path.parent,delete=False) as stream:
            temp=Path(stream.name)
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        encoded=payload.encode("utf-8")
        if temp.read_bytes()!=encoded:raise ValueError("Временный JSON не совпал с записываемым проектом.")
        json.loads(temp.read_text(encoding="utf-8"))
        temp.replace(path)
    finally:
        if temp is not None:temp.unlink(missing_ok=True)


def load(path):
    project = json.loads(path.read_text(encoding="utf-8-sig"))
    if "scenes" in project:
        identify(project, seed=str(path.resolve()))
        def relative(record, field):
            value = record.get(field)
            if isinstance(value, str) and value.startswith("./"):
                record[field] = str((path.parent / value).resolve())
        relative(project, "audio")
        for scene in project["scenes"]:
            for field in ("audio", "image"):
                relative(scene, field)
            for anchor in scene.get("anchors", []):
                for field in ("local_asset_path", "reference_image"):
                    relative(anchor, field)
    return project


def identify(project, seed=None):
    used = set()
    for index, scene in enumerate(project["scenes"]):
        key = scene.get("id")
        if not isinstance(key, str) or not re.fullmatch(r"[0-9a-f]{32}", key) or key in used:
            key = uuid.uuid5(uuid.NAMESPACE_URL, f"{seed}#{index}").hex if seed else uuid.uuid4().hex
            if key in used:
                key = uuid.uuid4().hex
            scene["id"] = key
        used.add(key)


def file_digest(path):
    with path.open("rb") as stream:
        digest = sha256()
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
        return digest.hexdigest()


def audio_source(project, scene):
    if scene.get("audio"):
        path = Path(scene["audio"]).expanduser().resolve(strict=True)
        if path.suffix.lower() not in {".mp3", ".wav"}:
            raise ValueError("Импорт сцены поддерживает MP3 и WAV.")
        return path, ["import", file_digest(path)]
    locale = project["locale"]
    voice = scene.get("voice") or project.get("voice") or VOICES[locale]
    allowed = {VOICES[locale]}
    if locale == "ru":
        allowed.add("ru-RU-DmitryNeural")
    if voice not in allowed:
        raise ValueError("Голос не подходит языку проекта.")
    return voice, ["edge", voice, scene["text"].strip()]


def audio_key(project, scene, cache):
    source, signature = audio_source(project, scene)
    fingerprint = sha256(json.dumps(signature, ensure_ascii=False).encode()).hexdigest()
    return source, cache / scene["id"] / fingerprint


def scene_audio(project, scene, cache, ffmpeg, ffprobe, announce=print):
    folder = cache / scene["id"]
    folder.mkdir(parents=True, exist_ok=True)
    log = folder / "audio.log"
    def record(message):
        with log.open("a", encoding="utf-8") as stream:
            stream.write(f"{datetime.now(timezone.utc).isoformat()} {message}\n")

    entry = None
    try:
        source, entry = audio_key(project, scene, cache)
        entry.mkdir(parents=True, exist_ok=True)
        ready = entry / "audio.wav"
        if ready.exists():
            try:
                ms = duration(ready, ffprobe)
            except (ValueError, OSError, subprocess.SubprocessError, KeyError):
                pass
            else:
                record(f"reuse {entry.name} {ms} ms")
                announce(f"{scene['id']}: повторное использование")
                return ready, ms
        with tempfile.TemporaryDirectory(dir=entry) as staging:
            temp = Path(staging)
            if isinstance(source, Path):
                record(f"import {entry.name} {source.suffix.lower()}")
                incoming = temp / ("input" + source.suffix.lower())
                shutil.copyfile(source, incoming)
                if audio_key(project, scene, cache)[1] != entry or file_digest(incoming) != file_digest(source):
                    raise ValueError("Исходное аудио изменилось при копировании.")
            else:
                if not scene["text"].strip():
                    raise ValueError("Добавьте текст сцены.")
                announce(f"{scene['id']}: синтез {source}")
                record(f"edge {entry.name} {source}")
                incoming = temp / "speech.mp3"
                synthesize(source, scene["text"].strip(), incoming, ffprobe=ffprobe,
                           attempts=3, allow_fallback=False)
            command([ffmpeg, "-nostdin", "-v", "error", "-i", incoming.name,
                     "-map", "0:a:0", "-ac", "1", "-ar", "24000", "audio.wav"], temp, log)
            ms = duration(temp / "audio.wav", ffprobe)
            (temp / "audio.wav").replace(ready)
        (entry / "error.json").unlink(missing_ok=True)
        record(f"ready {entry.name} {ms} ms")
        return ready, ms
    except Exception as exc:
        if entry is not None and entry.is_dir():
            save(entry / "error.json", {"message": str(exc)})
        record(f"{type(exc).__name__}: {exc}")
        raise RuntimeError(f"Сцена {scene['id']}: {exc}\nЖурнал: {log}") from exc


def audio_status(project, scene, cache):
    if project.get("audio"):
        return "Общая дорожка"
    try:
        _, entry = audio_key(project, scene, cache)
        if (entry / "audio.wav").is_file():
            return "Готово"
        if (entry / "error.json").is_file():
            return "Сбой"
    except (OSError, ValueError, KeyError):
        return "Ошибка источника"
    return "Ожидает сборки"


def brief(topic, locale):
    if locale == "uk":
        return (f"Тема: {topic}\nОцінка: оберіть конкретне питання й часові межі.\n"
                "Аудиторія: допитливі глядачі без спеціальної підготовки.\n"
                f"Вступ 1: Що ми насправді знаємо про «{topic}»?\n"
                "Вступ 2: Почнімо з однієї знахідки. Що вона може розповісти?\n"
                "Вступ 3: Яке популярне пояснення варто перевірити?\n"
                "Структура: питання → докази й альтернативи → межі висновку.\n"
                "Твердження для перевірки: дати, місця, причинні зв’язки.\n"
                "Джерела: звіти розкопок, наукові огляди, музейні каталоги.\n"
                "Ризики: неповнота даних, суперечливі датування й узагальнення.\n"
                "Візуальні варіанти: карта, хронологія, схема знахідки.\n"
                "Чекає рішення редактора. Фактичні твердження не перевірено.")
    return (f"Тема: {topic}\nОценка: выберите конкретный вопрос и временные рамки.\n"
            "Аудитория: любознательные зрители без специальной подготовки.\n"
            f"Вступление 1: Что мы на самом деле знаем о теме «{topic}»?\n"
            "Вступление 2: Начнём с одной находки. О чём она может рассказать?\n"
            "Вступление 3: Какое популярное объяснение стоит проверить?\n"
            "Структура: вопрос → свидетельства и альтернативы → границы вывода.\n"
            "Утверждения для проверки: даты, места, причинные связи.\n"
            "Источники: отчёты раскопок, научные обзоры, музейные каталоги.\n"
            "Риски: неполнота данных, спорные датировки и обобщения.\n"
            "Визуальные варианты: карта, хронология, схема находки.\n"
            "Ожидается решение редактора. Фактические утверждения не проверены.")


def executable(name):
    configured = os.environ.get("STORY_MVP_" + name.upper())
    path = configured or shutil.which(name)
    if not path:
        raise RuntimeError(f"Не найден {name}. Укажите STORY_MVP_{name.upper()}.")
    return path


_preview_session=ContextVar('story_experimental_preview_session',default=None)


@contextmanager
def preview_session(cancelled):
    current=_preview_session.get()
    if current is not None:
        yield current
        return
    session={'cancelled':cancelled,'folders':[],'processes':[],'started':time.monotonic()}
    token=_preview_session.set(session)
    try:
        if cancelled():raise BuildStopped('Предпросмотр отменён до запуска.')
        yield session
        if cancelled():raise BuildStopped('Предпросмотр отменён.')
    except BaseException:
        for folder in reversed(session['folders']):
            shutil.rmtree(folder)
        raise
    finally:
        _preview_session.reset(token)


def register_preview_folder(folder):
    session=_preview_session.get()
    if session is not None:session['folders'].append(Path(folder))


def discard_preview_result(path,workspace):
    """Delete only the exact result returned by this worker, never arbitrary siblings."""
    path=Path(path);workspace=Path(workspace).resolve()
    folder=path.parent
    if path.name not in ('preview.mp4','final.mp4') or not re.fullmatch(r'(timeline-preview|movie-preview|preview)-[0-9a-f]{12}',folder.name):
        raise ValueError('Неизвестная папка preview: удаление запрещено.')
    if folder.resolve().parent!=workspace or folder.is_symlink():
        raise ValueError('Результат preview вне рабочей папки.')
    if folder.exists():shutil.rmtree(folder)


def command(args, folder, log, timeout=300):
    with log.open("a", encoding="utf-8") as stream:
        stream.write(f"\n{args[0]} {args[-1]}\n")
        stream.flush()
        session=_preview_session.get()
        if session is None:
            result=subprocess.run(args,cwd=folder,stdout=stream,stderr=stream,timeout=timeout,check=False)
        else:
            if session['cancelled']():raise BuildStopped('Предпросмотр отменён до запуска FFmpeg.')
            started=time.monotonic()
            process=subprocess.Popen(args,cwd=folder,stdout=stream,stderr=stream)
            record={'pid':process.pid,'returncode':None};session['processes'].append(record)
            try:
                while True:
                    try:
                        code=process.wait(timeout=.05)
                        break
                    except subprocess.TimeoutExpired:
                        if session['cancelled']():raise BuildStopped('Предпросмотр отменён во время команды.')
                        if time.monotonic()-started>=timeout:raise subprocess.TimeoutExpired(args,timeout)
                result=subprocess.CompletedProcess(args,code)
                if session['cancelled']():raise BuildStopped('Предпросмотр отменён после команды.')
            finally:
                if process.poll() is None:
                    process.terminate()
                    try:process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        process.kill();process.wait(timeout=2)
                record['returncode']=process.returncode
                stream.write(f"owned_pid={process.pid} exit={process.returncode} elapsed={time.monotonic()-started:.3f}s\n")
        stream.write(f"exit={result.returncode}\n")
    if result.returncode:
        raise RuntimeError(f"Этап завершился с кодом {result.returncode}. Журнал: {log}")


def duration(path, ffprobe):
    result = subprocess.run([ffprobe, "-v", "error", "-select_streams", "a:0",
                             "-show_entries", "stream=codec_type:format=duration",
                             "-of", "json", str(path)], capture_output=True, check=True, timeout=25)
    data = json.loads(result.stdout)
    if not data.get("streams") or float(data["format"]["duration"]) <= 0:
        raise ValueError("Файл должен содержать аудиодорожку положительной длительности.")
    return round(float(data["format"]["duration"]) * 1000)


def intervals(texts, total):
    weights = [max(1, len(text.split())) for text in texts]
    if total < 250 * len(weights):
        raise ValueError("Аудио слишком короткое для количества сцен.")
    free = total - 250 * len(weights)
    elapsed = 0
    cumulative = 0
    for index, weight in enumerate(weights, 1):
        cumulative += weight
        end = 250 * index + (free * cumulative // sum(weights))
        yield elapsed, end
        elapsed = end


def subtitles(texts, spans):
    return render_srt([{"text": text} for text in texts], spans, {})


def preview_audio(project, index, workspace):
    """Resolve the scene audio without invoking synthesis."""
    scene = project["scenes"][index]
    ffprobe = executable("ffprobe")
    if project.get("audio"):
        source = Path(project["audio"]).expanduser().resolve(strict=True)
        if source.suffix.lower() not in {".mp3", ".wav"}:
            raise ValueError("Импорт озвучки поддерживает MP3 и WAV.")
        texts = [item["text"].strip() for item in project["scenes"]]
        if project.get("timeline"):
            from experimental_mvp.timeline import measure_audio
            entry = measure_audio(project, workspace)["scenes"][index]
            start,end = entry["start_ms"],entry["end_ms"]
        else:
            start, end = list(intervals(texts, duration(source, ffprobe)))[index]
        return source, start, end - start, True
    source, entry = audio_key(project, scene, workspace / "scene-audio")
    ready = entry / "audio.wav"
    if ready.is_file():
        try:
            return ready, 0, duration(ready, ffprobe), False
        except (ValueError, OSError, subprocess.SubprocessError, KeyError):
            pass
    if isinstance(source, Path):
        return source, 0, duration(source, ffprobe), False
    raise ValueError(f"Сцена {index + 1}: подготовьте озвучку кнопкой «Подготовить / повторить сцену».")


def render_preview(project, index, workspace, audio, *, cancelled=lambda:False):
    with preview_session(cancelled):
        return _render_preview(project,index,workspace,audio,cancelled=cancelled)


def _render_preview(project, index, workspace, audio, *, cancelled=lambda:False):
    source, start, length, approximate = audio
    scene = project["scenes"][index]
    overrides = project.get("captions_by_scene", {})
    validate(overrides.get(scene["id"], calculated(scene["text"], length)), length, index + 1)
    captions = render_srt([scene], [(0, length)], overrides)
    folder = workspace.resolve() / ("preview-" + uuid.uuid4().hex[:12])
    folder.mkdir(parents=True)
    register_preview_folder(folder)
    log = folder / "preview.log"
    (folder / "captions.srt").write_text(captions, encoding="utf-8")
    ffmpeg = executable("ffmpeg")
    profile=project.get("output_profile")
    if project.get("timeline"):
        from experimental_mvp.storyboard import output_profile
        profile={**(profile or {}),"timeline_version":1,"scene_start_ms":0,
                 "frame_count":round(length*output_profile(profile)[2]/1000)}
    clip = render_scene(scene, index + 1, length / 1000, folder, log, ffmpeg, profile,cancelled)
    command([ffmpeg, "-nostdin", "-v", "error", "-i", clip, "-ss", str(start / 1000),
             "-i", str(source), "-map", "0:v:0", "-map", "1:a:0",
             "-vf", "subtitles=captions.srt", "-t", str(length / 1000),
             "-c:v", "libx264", "-preset", "ultrafast", "-threads", "4",
             "-c:a", "aac", "-movflags", "+faststart", "preview.mp4"], folder, log)
    return folder / "preview.mp4", approximate


def render_scene(scene, index, length, folder, log, ffmpeg, profile=None, cancelled=lambda: False):
    if scene.get("anchors"):
        from experimental_mvp.storyboard import render
        return render(scene, index, length, folder, log, ffmpeg, command, profile, cancelled)
    if profile:
        from experimental_mvp.storyboard import output_profile
        width, height, fps = output_profile(profile)
    else:
        width, height, fps = 1920, 1080, 30
    colors = ["0x17365a", "0x275148", "0x603d44", "0x39466b"]
    image = scene.get("image")
    if image:
        source = Path(image).expanduser().resolve(strict=True)
        if source.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".bmp"}:
            raise ValueError("Используйте PNG, JPEG, WebP или BMP.")
        local = folder / f"image{index:03}{source.suffix.lower()}"
        shutil.copyfile(source, local)
        image_args = ["-loop", "1", "-framerate", str(fps), "-i", local.name]
    else:
        color = colors[(index - 1) % len(colors)]
        image_args = ["-f", "lavfi", "-i", f"color=c={color}:s={width}x{height}:r={fps}"]
    fade = min(0.22, length / 3)
    filters = (f"scale={width}:{height}:force_original_aspect_ratio=decrease:"
               f"force_divisible_by=2,pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,"
               f"setsar=1,format=yuv420p,fade=t=in:d={fade},"
               f"fade=t=out:st={length-fade}:d={fade}")
    clip = f"scene{index:03}.mp4"
    command([ffmpeg, "-nostdin", "-v", "error", *image_args, "-an", "-vf", filters,
             *( ["-frames:v", str(profile["frame_count"])] if profile and "frame_count" in profile else ["-t", str(length)]), "-c:v", "libx264", "-preset", "ultrafast",
             "-threads", "4", clip], folder, log)
    return clip


def check_project(project, workspace):
    """Inspect effective local inputs without generating speech."""
    issues = []
    scenes = project["scenes"]
    if not scenes:
        return [(None, "scenes", "Добавьте хотя бы одну сцену.", False)]
    ffmpeg, ffprobe = executable("ffmpeg"), executable("ffprobe")

    def inspect(value, field, scene_id):
        try:
            path = Path(value).expanduser().resolve(strict=True)
            audio = field != "image"
            allowed = {".wav", ".mp3"} if audio else {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
            if not path.is_file() or path.suffix.lower() not in allowed:
                raise ValueError("Неподдерживаемый файл.")
            length = duration(path, ffprobe) if audio else None
            limit = ["-t", "1"] if audio else ["-frames:v", "1"]
            subprocess.run([ffmpeg, "-nostdin", "-v", "error", "-xerror", "-i", str(path),
                            "-map", "0:a:0" if audio else "0:v:0", *limit, "-f", "null", "-"],
                           capture_output=True, check=True, timeout=25)
            return length
        except (ValueError, OSError, KeyError, subprocess.SubprocessError) as exc:
            issues.append((scene_id, field, f"Файл отсутствует или не читается: {value} ({exc})", False))
            return None

    whole = project.get("audio")
    spans = None
    if whole:
        length = inspect(whole, "audio", None)
        if length is not None:
            try:
                if project.get("timeline"):
                    from experimental_mvp.timeline import timing_map
                    spans = [(s["start_ms"],s["end_ms"]) for s in timing_map(project,whole_ms=length)["scenes"]]
                else:
                    spans = list(intervals([s["text"] for s in scenes], length))
            except ValueError as exc:
                issues.append((None, "audio", str(exc), False))
    overrides = project.get("captions_by_scene", {})
    anchor_ids = [a.get("anchor_id") for s in scenes for a in s.get("anchors", [])]
    if len(anchor_ids) != len(set(anchor_ids)):
        issues.append((None, "anchors", "anchor_id должны быть уникальны во всём проекте.", False))
    for index, scene in enumerate(scenes, 1):
        key = scene["id"]
        if not scene["text"].strip():
            issues.append((key, "text", "Пустой текст сцены.", False))
        if scene.get("image"):
            inspect(scene["image"], "image", key)
        if whole:
            length = spans[index - 1][1] - spans[index - 1][0] if spans else None
        elif scene.get("audio"):
            length = inspect(scene["audio"], "scene_audio", key)
        else:
            length = None
            try:
                _, entry = audio_key(project, scene, workspace / "scene-audio")
            except (ValueError, OSError, KeyError) as exc:
                issues.append((key, "voice", str(exc), False))
            else:
                if (entry / "audio.wav").is_file():
                    try:
                        length = duration(entry / "audio.wav", ffprobe)
                    except (ValueError, OSError, KeyError, subprocess.SubprocessError):
                        pass
            if length is None:
                issues.append((key, "captions", "Длительность и таймкоды ожидают озвучку.", True))
        if scene.get("anchors"):
            from experimental_mvp.storyboard import validate as validate_anchors
            if project.get("timeline"):
                from experimental_mvp.storyboard import video_spec, VIDEOS
                for anchor in scene["anchors"]:
                    if anchor.get("local_asset_path") and Path(anchor["local_asset_path"]).suffix.lower() in VIDEOS:
                        try:
                            video_spec(anchor, True)
                        except (ValueError,OSError,KeyError,subprocess.SubprocessError) as exc:
                            issues.append((key,"anchors",str(exc),False))
            if length is not None:
                for message in validate_anchors(scene, length):
                    issues.append((key, "anchors", message, False))
            else:
                issues.append((key, "anchors", "Покрытие якорей ожидает длительность озвучки.", True))
        if key in overrides:
            try:
                validate(overrides[key], length if length is not None else float("inf"), index)
            except CueError as exc:
                issues.append((key, "captions", str(exc), False))
    return issues


def preview_signature(project):
    """Determine staleness without opening or transmitting media contents."""
    selection = {k: project.get(k) for k in ("locale", "voice", "audio", "scenes", "captions_by_scene", "output_profile", "timeline")}
    sources = [project.get("audio")]
    for scene in project["scenes"]:
        sources.extend((scene.get("image"), None if project.get("audio") else scene.get("audio")))
        sources.extend(a.get("local_asset_path") for a in scene.get("anchors", []))
    stamps = []
    for value in filter(None, sources):
        try:
            stat = Path(value).expanduser().stat()
            stamps.append((value, stat.st_size, stat.st_mtime_ns))
        except OSError:
            stamps.append((value, None))
    return sha256(json.dumps([selection, stamps], sort_keys=True).encode()).hexdigest()


def export_history(workspace):
    """Incomplete or failed exports are never candidates for playback."""
    history = []
    for folder in workspace.glob("run-*"):
        try:
            result = load(folder / "result.json")
            status = result["status"]
        except (OSError, ValueError, KeyError):
            status = "interrupted"
        if status == "running":
            status = "interrupted"
        video = folder / "final.mp4"
        history.append((folder, status if status != "complete" or video.is_file() else "interrupted"))
    return sorted(history, key=lambda item: item[0].stat().st_mtime_ns, reverse=True)


class BuildStopped(RuntimeError):
    pass


def build(project, workspace, notify=print, *, preview=False, cancelled=lambda: False):
    if preview:
        with preview_session(cancelled):
            return _build(project,workspace,notify,preview=preview,cancelled=cancelled)
    return _build(project,workspace,notify,preview=preview,cancelled=cancelled)


def _build(project, workspace, notify=print, *, preview=False, cancelled=lambda: False):
    from copy import deepcopy
    project = deepcopy(project)
    if project.get("approved") is not True:
        raise ValueError("Сначала подтвердите локальную экспериментальную сборку; production permissions не выдаются.")
    identify(project)
    scenes = project["scenes"]
    texts = [scene["text"].strip() for scene in scenes]
    ffmpeg, ffprobe = executable("ffmpeg"), executable("ffprobe")
    workspace = workspace.resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    prefix = "movie-preview-" if preview else "run-"
    folder = workspace / (prefix + uuid.uuid4().hex[:12])
    folder.mkdir()
    if preview:register_preview_folder(folder)
    log = folder / "build.log"
    log.write_text(datetime.now(timezone.utc).isoformat() + "\n", encoding="utf-8")
    save(folder / "result.json", {"status": "running"})
    save(folder / "project.json", project)

    def checkpoint():
        if cancelled():
            raise BuildStopped("Сборка остановлена. Подготовленные сегменты сохранены.")

    try:
        scene_numbers = {scene["id"]: index for index, scene in enumerate(scenes, 1)}
        errors = [
            f"{'Сцена ' + str(scene_numbers[key]) + ' / ' if key else ''}{field}: {message}"
            for key, field, message, pending in check_project(project, workspace) if not pending
        ]
        if errors:
            raise ValueError("\n".join(errors))
        checkpoint()
        notify("Озвучка")
        audio = project.get("audio")
        if audio:
            source = Path(audio).expanduser().resolve(strict=True)
            if source.suffix.lower() not in {".mp3", ".wav"}:
                raise ValueError("Импорт озвучки поддерживает MP3 и WAV.")
            imported = folder / ("import" + source.suffix.lower())
            shutil.copyfile(source, imported)
            if project.get("timeline"):
                from experimental_mvp.timeline import timing_map
                mapped = timing_map(project, whole_ms=duration(imported, ffprobe))
                spans = [(s["start_ms"], s["end_ms"]) for s in mapped["scenes"]]
            else:
                spans = list(intervals(texts, duration(imported, ffprobe)))
            audio_args = ["-i", imported.name]
            timing = "estimated_word_weighted_from_imported_audio"
        else:
            spans = []
            segments = []
            start = 0
            cache = workspace / "scene-audio"
            failures = []
            for index, scene in enumerate(scenes, 1):
                checkpoint()
                notify(f"Озвучка: сцена {index}/{len(scenes)}")
                try:
                    ready, ms = scene_audio(project, scene, cache, ffmpeg, ffprobe, notify)
                except RuntimeError as exc:
                    failures.append(f"#{index}: {exc}")
                    continue
                name = f"speech{index:03}.wav"
                shutil.copyfile(ready, folder / name)
                segments.append(name)
                spans.append((start, start + ms))
                start += ms
            if failures:
                raise RuntimeError("\n".join(failures))
            (folder / "speech.txt").write_text("".join(f"file '{name}'\n" for name in segments),
                                               encoding="ascii")
            audio_args = ["-f", "concat", "-safe", "1", "-i", "speech.txt"]
            timing = "measured_scene_boundaries_estimated_cue_boundaries"
        if project.get("timeline"):
            from experimental_mvp.timeline import timing_map
            if not audio:
                mapped = timing_map(project, scene_ms={s["id"]: end-start for s,(start,end) in zip(scenes,spans)})
                spans = [(s["start_ms"],s["end_ms"]) for s in mapped["scenes"]]
            save(folder / "audio-timing-map.json", mapped)
        notify("Озвучка подготовлена")
        checkpoint()
        (folder / "captions.srt").write_text(render_srt(scenes, spans, project.get("captions_by_scene", {})),
                                             encoding="utf-8")
        save(folder / "timing.json", {"method": timing, "scenes_ms": spans})
        clips = []
        for index, (scene, (start, end)) in enumerate(zip(scenes, spans), 1):
            checkpoint()
            notify(f"Видео: сцена {index}/{len(scenes)}")
            profile = project.get("output_profile")
            if project.get("timeline"):
                from experimental_mvp.storyboard import output_profile
                fps = output_profile(profile)[2]
                profile = {**(profile or {}), "timeline_version": 1, "scene_start_ms": start,
                           "frame_count": round(end*fps/1000)-round(start*fps/1000)}
            clips.append(render_scene(scene, index, (end-start)/1000, folder, log, ffmpeg, profile, cancelled))
        (folder / "scenes.txt").write_text("".join(f"file '{name}'\n" for name in clips),
                                          encoding="ascii")
        checkpoint()
        notify("Сборка MP4")
        command([ffmpeg, "-nostdin", "-v", "error", "-f", "concat", "-safe", "1",
                 "-i", "scenes.txt", *audio_args, "-i", "captions.srt",
                 "-map", "0:v:0", "-map", "1:a:0", "-map", "2:s:0",
                 "-c:v", "copy", "-c:a", "aac", "-c:s", "mov_text",
                 "-metadata:s:s:0", "language=" + {"ru": "rus", "uk": "ukr"}[project["locale"]],
                 "-disposition:s:0", "default", "-movflags", "+faststart", "pending.mp4"], folder, log)
        checkpoint()
        if project.get("timeline"):
            from experimental_mvp.storyboard import output_profile
            measured = subprocess.run([ffprobe, "-v", "error", "-show_entries",
                                       "format=duration:stream=codec_type,duration,nb_frames",
                                       "-of", "json", str(folder / "pending.mp4")], capture_output=True, check=True)
            values=json.loads(measured.stdout)
            actual=float(values["format"]["duration"])
            video_stream=next(s for s in values["streams"] if s["codec_type"]=="video")
            audio_stream=next(s for s in values["streams"] if s["codec_type"]=="audio")
            video_seconds=float(video_stream["duration"]);audio_seconds=float(audio_stream["duration"])
            expected=spans[-1][1]/1000;fps=output_profile(project.get("output_profile"))[2]
            tolerance=max(.1,2/fps);expected_frames=round(spans[-1][1]*fps/1000)
            frames=int(video_stream["nb_frames"])
            passed=(abs(actual-expected)<=tolerance and abs(video_seconds-expected)<=tolerance
                    and abs(video_seconds-audio_seconds)<=tolerance and frames==expected_frames)
            save(folder / "duration-check.json", {"expected_seconds":expected,"actual_seconds":actual,
                 "video_seconds":video_seconds,"audio_seconds":audio_seconds,
                 "video_audio_delta_seconds":abs(video_seconds-audio_seconds),
                 "expected_frames":expected_frames,"actual_frames":frames,
                 "tolerance_seconds":tolerance,"passed":passed})
            if not passed:raise ValueError("Длительность/кадры MP4 не совпали с озвучкой в допустимом допуске.")
        (folder / "pending.mp4").replace(folder / "final.mp4")
        output = folder / "final.mp4"
        save(folder / "execution-evidence.json", {
            "mode": "EXPERIMENTAL_LOCAL_ONLY", "production_permissions": False,
            "project_sha256": sha256((folder / "project.json").read_bytes()).hexdigest(),
            "output_sha256": sha256(output.read_bytes()).hexdigest(),
            "audio_inputs": [{"file": p.name, "sha256": file_digest(p)}
                             for p in sorted([*folder.glob("import.*"), *folder.glob("speech*.wav")])],
            "captions_sha256": file_digest(folder / "captions.srt"),
            "tool_versions": {name: subprocess.run([executable(name), "-version"],
                capture_output=True, text=True, check=True).stdout.splitlines()[0]
                for name in ("ffmpeg", "ffprobe")},
            "copied_visual_inputs": [json.loads(p.read_text(encoding="utf-8")) for p in sorted(folder.glob("anchor-inputs*.json"))],
            "anchors": [{"anchor_id": a["anchor_id"], "sha256": a.get("asset_sha256"),
                         "license_status": a.get("license_status", "UNKNOWN")}
                        for scene in scenes for a in scene.get("anchors", [])]})
        save(folder / "result.json", {"status": "complete", "timing": timing})
        return folder / "final.mp4"
    except (BuildStopped, KeyboardInterrupt):
        save(folder / "result.json", {"status": "interrupted"})
        raise
    except Exception as exc:
        save(folder / "result.json", {"status": "error", "message": str(exc)})
        raise RuntimeError(f"{exc}\nПапка сборки: {folder}") from exc


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Offline installation and codec check")
    parser.add_argument("--check-edge", choices=VOICES,
                        help="Also synthesize a short sample using the online service")
    parser.add_argument("--project", type=Path)
    parser.add_argument("--workspace", type=Path, default=ROOT / "runs")
    parser.add_argument("--audio", type=Path, help="Override the project audiobook with an MP3/WAV")
    parser.add_argument("--approve", action="store_true", help="Confirm this local experimental render")
    args = parser.parse_args()
    if args.check or args.check_edge:
        from experimental_mvp.diagnostics import check
        return check(args.check_edge)
    elif args.project:
        project = load(args.project)
        if args.audio:
            project["audio"] = str(args.audio.resolve())
        if args.approve:
            project["approved"] = True
        print(build(project, args.workspace))
    else:
        from experimental_mvp.ui import launch
        launch()


if __name__ == "__main__":
    raise SystemExit(main())
