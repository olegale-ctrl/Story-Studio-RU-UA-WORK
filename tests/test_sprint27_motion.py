"""Sprint 27 tests: Ken Burns motion and vertical (9:16) rendering."""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
import wave
from pathlib import Path

from scripts.first_video import build, main


def tone(path: Path, duration_s: float = 1.0) -> None:
    frames = int(24000 * duration_s)
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(24000)
        f.writeframes(b"\x00\x00" * frames)


class Sprint27MotionTests(unittest.TestCase):
    def setUp(self):
        if not shutil.which("ffmpeg"):
            self.skipTest("FFmpeg not installed")

    def test_motion_render_end_to_end(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            audio = root / "audio"
            audio.mkdir()
            tone(audio / "voice1.wav", 1.0)
            tone(audio / "voice2.wav", 1.0)

            plan = root / "plan.json"
            plan.write_text(json.dumps({
                "locale": "ru",
                "title": "Motion Test",
                "scenes": [
                    {"text": "Первая сцена с наездом камеры"},
                    {"text": "Вторая сцена с панорамированием"},
                ]
            }, ensure_ascii=False), encoding="utf-8")

            out_dir = root / "out_motion"
            proj_path, video_path = build(
                plan, out_dir, audio_dir=audio,
                render=True, motion=True, width=320, height=180
            )

            self.assertIsNotNone(video_path)
            self.assertTrue(video_path.is_file())
            self.assertGreater(video_path.stat().st_size, 2000)

    def test_vertical_motion_render(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            audio = root / "audio"
            audio.mkdir()
            tone(audio / "voice1.wav", 1.0)

            plan = root / "plan.json"
            plan.write_text(json.dumps({
                "locale": "uk",
                "title": "Vertical Test",
                "scenes": [
                    {"text": "Вертикальне відео 9:16 для Shorts"},
                ]
            }, ensure_ascii=False), encoding="utf-8")

            out_dir = root / "out_vertical"
            # Vertical test at 180x320
            proj_path, video_path = build(
                plan, out_dir, audio_dir=audio,
                render=True, motion=True, width=180, height=320
            )

            self.assertIsNotNone(video_path)
            self.assertTrue(video_path.is_file())
            self.assertGreater(video_path.stat().st_size, 1000)

    def test_cli_flags(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            audio = root / "audio"
            audio.mkdir()
            tone(audio / "voice1.wav", 1.0)

            plan = root / "plan.json"
            plan.write_text(json.dumps({
                "locale": "ru",
                "scenes": [{"text": "CLI test"}]
            }, ensure_ascii=False), encoding="utf-8")

            out_dir = root / "cli_out"
            rc = main([
                "--plan", str(plan),
                "--output-dir", str(out_dir),
                "--audio-dir", str(audio),
                "--motion",
                "--vertical",
                "--width", "180",
                "--height", "320",
            ])
            self.assertEqual(rc, 0)
            self.assertTrue((out_dir / "first-video.mp4").is_file())


if __name__ == "__main__":
    unittest.main()
