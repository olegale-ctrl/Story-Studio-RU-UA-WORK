"""Sprint 28 tests: Background music (BGM) with audio ducking and dynamic subtitles."""
from __future__ import annotations

import json
import shutil
import tempfile
import unittest
import wave
from pathlib import Path

from core.mp4_render import render_mp4
from core.project_schema import Clip, MediaAsset, Project, Track
from core.subtitles import chunk_scene_subtitles, get_subtitle_style
from scripts.first_video import build, main


def tone(path: Path, duration_s: float = 1.0, freq_byte: int = 120) -> None:
    frames = int(48000 * duration_s)
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(48000)
        f.writeframes(bytes([freq_byte]) * (frames * 2))


class Sprint28BgmSubtitlesTests(unittest.TestCase):
    def setUp(self):
        if not shutil.which("ffmpeg"):
            self.skipTest("FFmpeg not installed")

    def test_chunk_scene_subtitles(self):
        text = "Озвучення, зображення та субтитри об'єднуються в одному проєкті."
        chunks = chunk_scene_subtitles(text, start_ms=1000, duration_ms=4800, max_words=3)
        self.assertGreaterEqual(len(chunks), 2)

        # First chunk starts at 1000
        self.assertEqual(chunks[0]["start_ms"], 1000)

        # Total duration must equal 4800ms
        total_dur = sum(c["duration_ms"] for c in chunks)
        self.assertEqual(total_dur, 4800)

        # Chunks must be contiguous
        for a, b in zip(chunks[:-1], chunks[1:]):
            self.assertEqual(a["start_ms"] + a["duration_ms"], b["start_ms"])

    def test_subtitle_style_responsive(self):
        style_h = get_subtitle_style(1280, 720)
        style_v = get_subtitle_style(720, 1280)

        self.assertIn("MarginV=", style_h)
        self.assertIn("MarginV=", style_v)
        # Vertical format must have larger bottom margin and outline for mobile UI
        self.assertGreater(int(style_v.split("MarginV=")[1].split(",")[0]),
                           int(style_h.split("MarginV=")[1].split(",")[0]))

    def test_render_with_bgm_and_ducking(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            media = root / "media"
            media.mkdir()
            (media / "img1.ppm").write_bytes(b"P6\n64 64\n255\n" + bytes([80, 110, 180]) * (64 * 64))
            tone(media / "voice1.wav", 1.0, 150)
            tone(media / "bgm.wav", 3.0, 50)

            proj = Project(
                "bgm_demo", "uk", (), fps=25, width=64, height=64,
                tracks=(Track("v", "video"), Track("a", "audio")),
                media=(MediaAsset("i1", "image", "img1.ppm"), MediaAsset("a1", "audio", "voice1.wav")),
                clips=(Clip("c_v", "v", "i1", 0, 1000), Clip("c_a", "a", "a1", 0, 1000)),
            )

            out_video = root / "ducked_output.mp4"
            res = render_mp4(
                proj, media, out_video,
                bgm_path=media / "bgm.wav", bgm_volume=0.20, ducking=True,
            )

            self.assertTrue(out_video.is_file())
            self.assertGreater(out_video.stat().st_size, 2000)
            self.assertEqual(res["bgm"], str((media / "bgm.wav").resolve()))
            self.assertTrue(res["ducking"])

    def test_build_pipeline_with_bgm_and_subtitles(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            audio = root / "audio"
            audio.mkdir()
            tone(audio / "voice1.wav", 2.0)
            tone(root / "music.wav", 5.0)

            plan = root / "plan.json"
            plan.write_text(json.dumps({
                "locale": "uk",
                "title": "BGM Demo",
                "scenes": [
                    {"text": "Тестовий текст з фоновою музикою та динамічними субтитрами."},
                ],
            }, ensure_ascii=False), encoding="utf-8")

            out_dir = root / "out_bgm"
            rc = main([
                "--plan", str(plan),
                "--output-dir", str(out_dir),
                "--audio-dir", str(audio),
                "--bgm", str(root / "music.wav"),
                "--bgm-volume", "0.25",
                "--sub-words", "3",
                "--width", "180",
                "--height", "320",
            ])
            self.assertEqual(rc, 0)
            video = out_dir / "first-video.mp4"
            self.assertTrue(video.is_file())
            self.assertGreater(video.stat().st_size, 2000)

            # Check that project.json has multiple dynamic subtitle chunks
            proj_data = json.loads((out_dir / "project.json").read_text(encoding="utf-8"))
            self.assertGreater(len(proj_data["subtitles"]), 1)


if __name__ == "__main__":
    unittest.main()
