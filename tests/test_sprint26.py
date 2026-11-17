"""Sprint 26 pipeline tests: stdlib, no Silero model or network required."""
import json
import sys
import tempfile
import types
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

    def test_failed_run_leaves_no_output_directory(self):
        """A runtime failure must not leave a half-written output tree behind.

        Otherwise a retry with the same --output-dir fails with
        "Output directory already exists" and the user has to clean up manually.
        """
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            audio = root / "audio"
            audio.mkdir()
            tone(audio / "voice1.wav")
            plan = root / "plan.json"
            plan.write_text(json.dumps({"locale": "uk", "scenes": [{"text": "Привіт"}]}),
                            encoding="utf-8")
            out = root / "out"

            class FailingProvider:
                # Must satisfy the ADR-0009 VoiceProvider contract now that
                # first_video validates every adapter before use.
                provider_id = "silero_local"

                def voices(self, locale):
                    return ()

                def synthesize(self, **kwargs):
                    raise RuntimeError("synthesis failed")

            original = sys.modules.get("integrations.silero_local")
            module = types.ModuleType("integrations.silero_local")

            def factory(model_path, *, trusted=False):
                return FailingProvider()

            module.SileroLocalProvider = factory
            sys.modules["integrations.silero_local"] = module
            try:
                with self.assertRaises(RuntimeError):
                    build(plan, out, silero_model=Path("fake.pt"), voice="ukr_igor",
                          render=False)
            finally:
                if original is not None:
                    sys.modules["integrations.silero_local"] = original
                else:
                    sys.modules.pop("integrations.silero_local", None)
            self.assertFalse(out.exists(), "failed run must not leave an output directory")
