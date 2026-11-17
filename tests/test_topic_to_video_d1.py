"""Exercise D1's real evaluator, Projection, and synthetic video path."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts import topic_to_video as cli
from tests.test_story_intelligence_decision_projection_v1 import stale_args


FIXTURE = Path(__file__).resolve().parents[1] / "examples" / "topic_d1_synthetic.json"


class SyntheticVerticalSlice(unittest.TestCase):
    @unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"),
                         "D1 positive render requires FFmpeg and ffprobe")
    def test_two_reproducible_videos_with_subtitles(self):
        topic = json.loads(FIXTURE.read_text(encoding="utf-8"))
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            results = []
            for name in ("first", "second"):
                output = root / name
                with patch.object(cli, "evaluate_si", wraps=cli.evaluate_si) as evaluate, \
                        patch.object(cli, "project_evaluation", wraps=cli.project_evaluation) as project:
                    cli.run(FIXTURE, output)
                evaluate.assert_called_once()
                self.assertEqual(project.call_count, 2)
                cards = json.loads((output / "private-cards.json").read_text(encoding="utf-8"))
                self.assertEqual(set(cards), {"ru", "uk"})
                for locale, card in cards.items():
                    self.assertEqual(card["display_locale"], locale)
                    self.assertEqual(card["availability"], "DISPLAYABLE")
                    wire = json.dumps(card, ensure_ascii=False)
                    self.assertNotIn(topic["permit"]["digest"], wire)
                    self.assertNotIn("Synthetic science topic", wire)
                    self.assertNotIn("sha256", wire)
                    self.assertNotIn("field_path", wire)
                    self.assertNotIn("input_ref", wire)
                    plan = json.loads((output / f"plan-{locale}.json").read_text(encoding="utf-8"))
                    self.assertEqual(plan, topic["plans"][locale])
                    project_json = json.loads((output / locale / "project.json").read_text(encoding="utf-8"))
                    self.assertEqual(project_json["content_locale"], locale)
                    subtitle, = project_json["subtitles"]
                    self.assertEqual((subtitle["text"], subtitle["start_ms"], subtitle["duration_ms"]),
                                     (plan["scenes"][0]["text"], 0, 1000))
                    self.assertTrue((output / locale / "first-video.mp4").is_file())
                results.append({path: (output / path).read_bytes() for path in [
                    "manifest.json", "evaluation.json", "private-cards.json",
                    "plan-ru.json", "plan-uk.json", "ru/project.json", "uk/project.json",
                ]})
            self.assertEqual(*results)

    def test_unbound_and_external_materials_fail_before_build(self):
        original = json.loads(FIXTURE.read_text(encoding="utf-8"))

        def reject(root, topic):
            source = root / "topic.json"
            cli.write_json(source, topic)
            output = root / "result"
            with patch.object(cli.first_video, "build") as build:
                with self.assertRaises((ValueError, TypeError)):
                    cli.run(source, output)
            build.assert_not_called()
            self.assertFalse(output.exists())

        def mutate_wav(path):
            data = cli.synthetic_wav()
            path.write_bytes(data[:-1] + b"x")

        def result_changed(**inputs):
            result = real_evaluate(**inputs)
            result["aggregate_tenths"]["value"] = 999
            return result

        def card_changed(*args):
            result = real_project(*args)
            result["sections"]["reasons"].append("Unbound text")
            return result

        real_evaluate = cli.evaluate_si
        real_project = cli.project_evaluation
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            cases = {
                "missing permit": lambda t: t.pop("permit"),
                "digest": lambda t: t["permit"].update(digest="0" * 64),
                "permit version": lambda t: t["permit"].update(version="unsupported"),
                "production": lambda t: t.update(purpose="PRODUCTION"),
                "other topic": lambda t: t.update(scenario="other"),
                "text": lambda t: t["plans"]["ru"]["scenes"][0].update(text="Изменённый текст"),
                "locale": lambda t: t["plans"]["ru"].update(locale="uk"),
                "incomplete": lambda t: t["evaluation_inputs"].pop("ratings"),
                "evaluation input": lambda t: t["evaluation_inputs"].update(ui_locale="ru"),
                "invalid": lambda t: t["evaluation_inputs"].update(records=[]),
                "stale": lambda t: t.update(evaluation_inputs=stale_args()),
                "WAV path": lambda t: t.update(audio_dir="../outside"),
                "TTS model": lambda t: t.update(silero_model="model.pt"),
                "external image": lambda t: t["plans"]["uk"]["scenes"][0].update(image="../outside.png"),
                "empty plan": lambda t: t["plans"]["uk"].update(scenes=[]),
            }
            for label, change in cases.items():
                with self.subTest(label=label):
                    topic = deepcopy(original)
                    change(topic)
                    reject(root, topic)
            for target, substitute in [
                ("write_wav", mutate_wav),
                ("evaluate_si", result_changed),
                ("project_evaluation", card_changed),
                ("project_evaluation", lambda *_: {"availability": "UNAVAILABLE"}),
            ]:
                with self.subTest(target=target, substitute=substitute.__name__):
                    with patch.object(cli, target, side_effect=substitute):
                        reject(root, original)
            self.assertEqual([p.name for p in root.iterdir()], ["topic.json"])

    def test_failure_after_first_build_publishes_nothing(self):
        with TemporaryDirectory() as temporary:
            output = Path(temporary) / "result"
            with patch.object(cli.first_video, "build", side_effect=[
                (Path("project.json"), Path("first-video.mp4")), RuntimeError("second render failed"),
            ]) as build, patch.object(cli, "inspect_video", return_value={}) as inspect:
                with self.assertRaisesRegex(RuntimeError, "second render failed"):
                    cli.run(FIXTURE, output)
            self.assertEqual(build.call_count, 2)
            inspect.assert_called_once()
            self.assertFalse(output.exists())
            self.assertEqual(list(Path(temporary).iterdir()), [])
