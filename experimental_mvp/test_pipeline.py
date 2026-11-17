import tempfile
import unittest
from pathlib import Path
import shutil
from unittest.mock import patch
import wave

from experimental_mvp.pipeline import (DEMOS, brief, build, executable, intervals,
                                       load, save, subtitles)
from experimental_mvp.captions import CueError, render_srt


class PipelineTests(unittest.TestCase):
    def test_manual_cues_round_trip_and_follow_scene_after_reorder(self):
        with tempfile.TemporaryDirectory() as temp:
            file = Path(temp) / "project.json"
            project = {"scenes": [{"text": "Первый"}, {"text": "Другий"}]}
            save(file, project)
            scene = project["scenes"][0]
            overrides = {scene["id"]: [{"start_ms": 125, "end_ms": 826, "text": "Правка"}]}
            project["captions_by_scene"] = overrides
            save(file, project)
            reopened = load(file)
            self.assertEqual(reopened["captions_by_scene"], overrides)
            reopened["scenes"].reverse()
            srt = render_srt(reopened["scenes"], [(0, 1500), (1500, 2500)], overrides)
            self.assertIn("00:00:01,625 --> 00:00:02,326\nПравка", srt)
            self.assertLess(srt.index("Другий"), srt.index("Правка"))

    def test_shortened_audio_rejects_manual_interval_and_reset_recovers(self):
        scenes = [{"id": "one", "text": "Первый"}, {"id": "two", "text": "Другий"}]
        overrides = {"two": [{"start_ms": 150, "end_ms": 900, "text": "Правка"}]}
        with self.assertRaisesRegex(CueError, "Сцена 2, реплика 1.*500 мс"):
            render_srt(scenes, [(0, 1200), (1200, 1700)], overrides)
        overrides.clear()
        self.assertIn("00:00:01,200 --> 00:00:01,700\nДругий",
                      render_srt(scenes, [(0, 1200), (1200, 1700)], overrides))
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
