"""Local experimental production, separate from Story Studio release storage."""
import argparse
from datetime import datetime, timezone
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import uuid

from scripts.edge_voice_demo import synthesize
from experimental_mvp.captions import CueError, calculated, render_srt, validate

VOICES = {"ru": "ru-RU-SvetlanaNeural", "uk": "uk-UA-PolinaNeural"}
ROOT = Path(os.environ.get("STORY_MVP_HOME") or (Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "StoryStudioMVP")).resolve()
DEMOS = Path(__file__).with_name("demos")


def save(path, project):
    if "scenes" in project:
        identify(project)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                     delete=False) as stream:
        temp = Path(stream.name)
        try:
            json.dump(project, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        except BaseException:
            stream.close()
            temp.unlink(missing_ok=True)
            raise
    try:
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)


def load(path):
    project = json.loads(path.read_text(encoding="utf-8-sig"))
    if "scenes" in project:
        identify(project, seed=str(path.resolve()))
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


def command(args, folder, log, timeout=300):
    with log.open("a", encoding="utf-8") as stream:
        stream.write(f"\n{args[0]} {args[-1]}\n")
        stream.flush()
        result = subprocess.run(args, cwd=folder, stdout=stream, stderr=stream,
                                timeout=timeout, check=False)
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


def render_preview(project, index, workspace, audio):
    source, start, length, approximate = audio
    scene = project["scenes"][index]
    overrides = project.get("captions_by_scene", {})
    validate(overrides.get(scene["id"], calculated(scene["text"], length)), length, index + 1)
    captions = render_srt([scene], [(0, length)], overrides)
    folder = workspace.resolve() / ("preview-" + uuid.uuid4().hex[:12])
    folder.mkdir(parents=True)
    log = folder / "preview.log"
    (folder / "captions.srt").write_text(captions, encoding="utf-8")
    ffmpeg = executable("ffmpeg")
    clip = render_scene(scene, index + 1, length / 1000, folder, log, ffmpeg)
    command([ffmpeg, "-nostdin", "-v", "error", "-i", clip, "-ss", str(start / 1000),
             "-i", str(source), "-map", "0:v:0", "-map", "1:a:0",
             "-vf", "subtitles=captions.srt", "-t", str(length / 1000),
             "-c:v", "libx264", "-preset", "ultrafast", "-threads", "4",
             "-c:a", "aac", "-movflags", "+faststart", "preview.mp4"], folder, log)
    return folder / "preview.mp4", approximate


def render_scene(scene, index, length, folder, log, ffmpeg):
    colors = ["0x17365a", "0x275148", "0x603d44", "0x39466b"]
    image = scene.get("image")
    if image:
        source = Path(image).expanduser().resolve(strict=True)
        if source.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".bmp"}:
            raise ValueError("Используйте PNG, JPEG, WebP или BMP.")
        local = folder / f"image{index:03}{source.suffix.lower()}"
        shutil.copyfile(source, local)
        image_args = ["-loop", "1", "-framerate", "30", "-i", local.name]
    else:
        color = colors[(index - 1) % len(colors)]
        image_args = ["-f", "lavfi", "-i", f"color=c={color}:s=1920x1080:r=30"]
    fade = min(0.22, length / 3)
    filters = ("scale=1920:1080:force_original_aspect_ratio=decrease:"
               "force_divisible_by=2,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,"
               f"setsar=1,format=yuv420p,fade=t=in:d={fade},"
               f"fade=t=out:st={length-fade}:d={fade}")
    clip = f"scene{index:03}.mp4"
    command([ffmpeg, "-nostdin", "-v", "error", *image_args, "-an", "-vf", filters,
             "-t", str(length), "-c:v", "libx264", "-preset", "ultrafast",
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
                spans = list(intervals([s["text"] for s in scenes], length))
            except ValueError as exc:
                issues.append((None, "audio", str(exc), False))
    overrides = project.get("captions_by_scene", {})
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
        if key in overrides:
            try:
                validate(overrides[key], length if length is not None else float("inf"), index)
            except CueError as exc:
                issues.append((key, "captions", str(exc), False))
    return issues


def preview_signature(project):
    """Determine staleness without opening or transmitting media contents."""
    selection = {k: project.get(k) for k in ("locale", "voice", "audio", "scenes", "captions_by_scene")}
    sources = [project.get("audio")]
    for scene in project["scenes"]:
        sources.extend((scene.get("image"), None if project.get("audio") else scene.get("audio")))
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
    if project.get("approved") is not True:
        raise ValueError("Сначала подтвердите переход к производству.")
    identify(project)
    scenes = project["scenes"]
    texts = [scene["text"].strip() for scene in scenes]
    ffmpeg, ffprobe = executable("ffmpeg"), executable("ffprobe")
    workspace = workspace.resolve()
    workspace.mkdir(parents=True, exist_ok=True)
    prefix = "movie-preview-" if preview else "run-"
    folder = workspace / (prefix + uuid.uuid4().hex[:12])
    folder.mkdir()
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
        notify("Озвучка подготовлена")
        checkpoint()
        (folder / "captions.srt").write_text(render_srt(scenes, spans, project.get("captions_by_scene", {})),
                                             encoding="utf-8")
        save(folder / "timing.json", {"method": timing, "scenes_ms": spans})
        clips = []
        for index, (scene, (start, end)) in enumerate(zip(scenes, spans), 1):
            checkpoint()
            notify(f"Видео: сцена {index}/{len(scenes)}")
            clips.append(render_scene(scene, index, (end - start) / 1000, folder, log, ffmpeg))
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
        (folder / "pending.mp4").replace(folder / "final.mp4")
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
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--project", type=Path)
    parser.add_argument("--workspace", type=Path, default=ROOT / "runs")
    parser.add_argument("--audio", type=Path, help="Override the project audiobook with an MP3/WAV")
    parser.add_argument("--approve", action="store_true", help="Confirm this local experimental render")
    args = parser.parse_args()
    if args.check:
        for name in ("ffmpeg", "ffprobe"):
            subprocess.run([executable(name), "-version"], check=True, stdout=subprocess.DEVNULL)
            print(name, "OK")
        print("Edge TTS client:", bool(importlib.util.find_spec("edge_tts")), "(network untested)")
        from tkinter import Tcl
        print("Tcl:", Tcl().eval("info patchlevel"))
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
    main()
