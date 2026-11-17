import tempfile
import unittest
from pathlib import Path

from experimental_mvp.pipeline import DEMOS, brief, build, intervals, load, save, subtitles


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
