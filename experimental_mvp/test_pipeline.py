import tempfile
import unittest
from pathlib import Path
import shutil
from unittest.mock import patch
import wave

from experimental_mvp.pipeline import (DEMOS, brief, build, executable, intervals,
                                       load, save, subtitles)


class PipelineTests(unittest.TestCase):
    def test_projects_round_trip_and_default_to_unapproved(self):
        for locale in ("ru", "uk"):
            with self.subTest(locale=locale), tempfile.TemporaryDirectory() as temp:
                project = load(DEMOS / f"{locale}.json")
                file = Path(temp) / "local" / "project.json"
                save(file, project)
                self.assertEqual(load(file), project)
                with self.assertRaisesRegex(ValueError, "подтвердите"):
                    build(project, Path(temp) / "runs")
                self.assertFalse((Path(temp) / "runs").exists())
                self.assertIn(project["topic"], brief(project["topic"], locale))

    def test_imported_audio_intervals_are_contiguous(self):
        spans = list(intervals(["коротко", "друга сцена довша"], 2011))
        self.assertEqual(spans[0][0], 0)
        self.assertEqual(spans[0][1], spans[1][0])
        self.assertGreater(spans[1][1] - spans[1][0], spans[0][1])
        self.assertEqual(spans[1][1], 2011)

    def test_srt_preserves_cyrillic_and_does_not_emit_user_markup(self):
        output = subtitles(["<b>Історія</b>"], [(0, 1500)])
        self.assertIn("00:00:00,000 --> 00:00:01,500", output)
        self.assertIn("Історія", output)
        self.assertNotIn("<b>", output)

    def test_resume_failure_edit_and_reorder(self):
        try:
            executable("ffmpeg")
            executable("ffprobe")
        except RuntimeError as exc:
            self.skipTest(str(exc))
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            audio = root / "fixture.wav"
            with wave.open(str(audio), "wb") as stream:
                stream.setparams((1, 2, 24000, 0, "NONE", "not compressed"))
                stream.writeframes(bytes(24000))
            calls = []

            def synthesis(voice, text, output, **_):
                calls.append(text)
                if text == "middle" and calls.count(text) == 1:
                    raise RuntimeError("Deterministic simulated TTS failure")
                shutil.copyfile(audio, output)

            project_file = root / "project.json"
            project = {"locale": "ru", "approved": True,
                       "scenes": [{"text": s} for s in ("first", "middle", "last")]}
            save(project_file, project)
            ids = [s["id"] for s in project["scenes"]]
            runs = root / "runs"
            with patch("experimental_mvp.pipeline.synthesize", side_effect=synthesis):
                with self.assertRaisesRegex(RuntimeError, "simulated TTS failure"):
                    build(project, runs)
                self.assertEqual(calls, ["first", "middle", "last"])
                self.assertIn("simulated TTS failure",
                              (runs / "scene-audio" / ids[1] / "audio.log").read_text())
                project = load(project_file)
                self.assertEqual([s["id"] for s in project["scenes"]], ids)
                build(project, runs)
                self.assertEqual(calls, ["first", "middle", "last", "middle"])
                project["scenes"][0]["text"] = "updated"
                project["scenes"].reverse()
                final = build(project, runs)
                self.assertEqual(calls, ["first", "middle", "last", "middle", "updated"])
                srt = (final.parent / "captions.srt").read_text(encoding="utf-8")
                self.assertLess(srt.index("last"), srt.index("middle"))
                self.assertLess(srt.index("middle"), srt.index("updated"))
                print(f"Deterministic synthesis calls: {calls}")
