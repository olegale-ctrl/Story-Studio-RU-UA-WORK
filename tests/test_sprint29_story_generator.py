"""Sprint 29 tests: Story generation, prompt enhancement, and end-to-end story-to-video."""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
import wave
from pathlib import Path

from core.prompt_builder import enhance_prompt, STYLES
from core.story_generator import (
    _extract_json,
    generate_offline_story,
    generate_story,
    StoryPlan,
)
from scripts.story_to_video import main, run_story_to_video


def tone(path: Path, duration_s: float = 1.0) -> None:
    frames = int(48000 * duration_s)
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(48000)
        f.writeframes(bytes([100]) * (frames * 2))


class Sprint29StoryTests(unittest.TestCase):
    def test_enhance_prompt(self):
        res = enhance_prompt("ancient stone fortress on a cliff", style="cinematic", aspect_ratio="16:9")
        self.assertIn("35mm photograph", res["prompt"])
        self.assertIn("fortress", res["prompt"])
        self.assertIn("--ar 16:9", res["prompt"])
        self.assertIn("deformed", res["negative_prompt"])

        res_hist = enhance_prompt("knights banquet hall", style="historical", aspect_ratio="9:16")
        self.assertIn("historical painting", res_hist["prompt"])
        self.assertIn("--ar 9:16", res_hist["prompt"])

    def test_extract_json(self):
        raw1 = '{"title": "Test", "scenes": []}'
        self.assertEqual(_extract_json(raw1)["title"], "Test")

        raw_block = 'Here is the plan:\n```json\n{"title": "Block", "scenes": []}\n```\nHope it helps!'
        self.assertEqual(_extract_json(raw_block)["title"], "Block")

    def test_generate_offline_story(self):
        plan_uk = generate_offline_story("Таємниці давнього Львова", locale="uk", style="historical")
        self.assertIsInstance(plan_uk, StoryPlan)
        self.assertEqual(plan_uk.locale, "uk")
        self.assertEqual(len(plan_uk.scenes), 3)
        self.assertTrue(all(len(s.text) > 10 for s in plan_uk.scenes))
        self.assertTrue(all(len(s.image_prompt) > 20 for s in plan_uk.scenes))

        plan_ru = generate_offline_story("Тайны Марианской впадины", locale="ru", style="dark_mystery")
        self.assertEqual(plan_ru.locale, "ru")
        self.assertEqual(len(plan_ru.scenes), 3)

    def test_story_to_video_pipeline(self):
        if not shutil.which("ffmpeg"):
            self.skipTest("FFmpeg not installed")

        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            audio = root / "audio"
            audio.mkdir()
            tone(audio / "voice1.wav", 1.0)
            tone(audio / "voice2.wav", 1.0)
            tone(audio / "voice3.wav", 1.0)
            tone(root / "bgm.wav", 4.0)

            out_dir = root / "story_output"
            story_file, video_file = run_story_to_video(
                topic="Козацькі таємниці",
                output_dir=out_dir,
                locale="uk",
                style="historical",
                audio_dir=audio,
                bgm_path=root / "bgm.wav",
                motion=True,
                vertical=True,
                width=180,
                height=320,
            )

            self.assertTrue(story_file.is_file())
            self.assertIsNotNone(video_file)
            self.assertTrue(video_file.is_file())
            self.assertGreater(video_file.stat().st_size, 2000)

            # Verify story_plan.json structure
            plan_data = json.loads(story_file.read_text(encoding="utf-8"))
            self.assertEqual(plan_data["locale"], "uk")
            self.assertEqual(len(plan_data["scenes"]), 3)
            self.assertIn("image_prompt", plan_data["scenes"][0])


if __name__ == "__main__":
    unittest.main()
