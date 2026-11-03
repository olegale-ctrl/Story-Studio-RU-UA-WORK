"""Sprint 26 pipeline tests: stdlib, no Silero model or network required."""
import json
import tempfile
import unittest
import wave
from pathlib import Path

from core.project_schema import Project
from scripts.first_video import build, read_plan, safe_image, wav_ms


def tone(path):
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(24000)
        f.writeframes(b"\x00\x00" * 24000)


class Sprint26Tests(unittest.TestCase):
    def test_plan_validation(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "plan.json"
            p.write_text('{"locale":"uk","scenes":[{"text":"Привіт"}]}', encoding="utf-8")
            self.assertEqual(read_plan(p)["locale"], "uk")
            p.write_text('{"locale":"en","scenes":[{"text":"Hello"}]}', encoding="utf-8")
            with self.assertRaises(ValueError):
                read_plan(p)

    def test_image_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(ValueError):
                safe_image(Path(td), "../outside.jpg")

    def test_wav_duration(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "voice1.wav"
            tone(p)
            self.assertEqual(wav_ms(p), 1000)

    def test_build_project_without_model(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            audio = root / "audio"
            audio.mkdir()
            tone(audio / "voice1.wav")
            tone(audio / "voice2.wav")
            plan = root / "plan.json"
            plan.write_text(json.dumps({"locale":"uk","scenes":[
                {"text":"Перша сцена"},{"text":"Друга сцена"}]}, ensure_ascii=False), encoding="utf-8")
            project_path, video = build(plan, root / "out", audio_dir=audio, render=False)
            self.assertIsNone(video)
            project = Project.from_json(project_path.read_text(encoding="utf-8"))
            self.assertEqual(len(project.clips), 4)
            self.assertEqual(len(project.subtitles), 2)
            self.assertEqual(project.clips[0].duration_ms, 1400)
            self.assertEqual(project.clips[2].start_ms, 1400)
            self.assertTrue((root / "out/media/frame1.ppm").is_file())
            with self.assertRaises(FileExistsError):
                build(plan, root / "out", audio_dir=audio, render=False)

    def test_missing_audio_rejected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            audio = root / "audio"
            audio.mkdir()
            plan = root / "plan.json"
            plan.write_text('{"locale":"ru","scenes":[{"text":"Тест"}]}', encoding="utf-8")
            with self.assertRaises(FileNotFoundError):
                build(plan, root / "out", audio_dir=audio, render=False)
