"""Installation checks with an explicit opt-in to online voice synthesis."""
from importlib import metadata
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import wave


def check(edge_locale=None):
    from experimental_mvp.pipeline import (VOICES, build, duration, executable,
                                           preview_audio, render_preview, synthesize)

    def attempt(label, action, remedy):
        try:
            result = action()
        except Exception as exc:
            print(f"{label}: FAIL · {exc}\n  {remedy}", file=sys.stderr)
            return False
        print(f"{label}: OK · {result}")
        return True

    def tk_window():
        from tkinter import Tk
        root = Tk()
        try:
            root.withdraw()
            root.update_idletasks()
            return root.tk.eval("info patchlevel")
        finally:
            root.destroy()

    def version(name):
        result = subprocess.run([executable(name), "-version"], check=True, capture_output=True,
                                text=True, encoding="utf-8", errors="replace", timeout=15)
        return result.stdout.splitlines()[0]

    def codecs():
        with TemporaryDirectory(prefix="story-studio-check-") as temp:
            root = Path(temp)
            local = root / "check.wav"
            with wave.open(str(local), "wb") as stream:
                stream.setparams((1, 2, 24000, 0, "NONE", "not compressed"))
                stream.writeframes(bytes(24000))
            project = {"locale": "ru", "approved": True, "audio": str(local),
                       "scenes": [{"text": "Проверка"}]}
            output = build(project, root, lambda _: None)
            probe = subprocess.run([executable("ffprobe"), "-v", "error", "-show_entries",
                                    "stream=codec_name:stream_tags=language",
                                    "-of", "json", str(output)],
                                   check=True, capture_output=True, timeout=15)
            streams = json.loads(probe.stdout)["streams"]
            if [s["codec_name"] for s in streams] != ["h264", "aac", "mov_text"]:
                raise RuntimeError("Потоки MP4 не совпали с ожидаемыми.")
            if streams[2].get("tags", {}).get("language") != "rus":
                raise RuntimeError("Отсутствует языковая метка субтитров.")
            render_preview(project, 0, root, preview_audio(project, 0, root))
        return "1920×1080 H.264/AAC, mov_text/rus и предпросмотр с libass"

    def edge():
        voice = VOICES[edge_locale]
        sample = {"ru": "Проверка голоса.", "uk": "Перевірка голосу."}[edge_locale]
        with TemporaryDirectory(prefix="story-studio-edge-") as temp:
            output = Path(temp) / "check.mp3"
            probe = executable("ffprobe")
            synthesize(voice, sample, output, ffprobe=probe, attempts=1, allow_fallback=False)
            return f"{voice}, {duration(output, probe)} мс"

    print(f"Python: {sys.version.split()[0]}")
    tk_ok = attempt("Tk", tk_window,
                    "Установите Windows Python с компонентом tcl/tk and IDLE и повторите проверку.")
    tools_ok = all([
        attempt(name, lambda: version(name),
                f"Распакуйте закреплённую сборку FFmpeg и задайте STORY_MVP_{name.upper()} "
                f"на полный путь к {name}.exe.")
        for name in ("ffmpeg", "ffprobe")
    ])
    codecs_ok = tools_ok and attempt("Локальная сборка", codecs,
                                     "Используйте проверенную сборку из инструкции RC-01 "
                                     "с libx264, AAC, mov_text и libass.")
    try:
        client = metadata.version("edge-tts")
    except metadata.PackageNotFoundError:
        client = None
    print("Edge TTS:", client or "клиент не установлен (для локального аудио допустимо)")
    edge_ok = True
    if edge_locale:
        edge_ok = attempt("Онлайн-синтез Edge", edge,
                          "Установите requirements-edge-win-amd64.txt, проверьте доступ к Edge "
                          "и повторите. Можно продолжить с локальным MP3/WAV.")
    else:
        print("Онлайн-синтез: не запрошен. Для проверки: --check-edge ru или --check-edge uk.")
    return 0 if tk_ok and codecs_ok and edge_ok else 1
