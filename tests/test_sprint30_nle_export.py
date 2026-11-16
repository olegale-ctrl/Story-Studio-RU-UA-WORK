"""Sprint 30 tests: NLE exchange exporters (FCPXML, CapCut Desktop draft, EDL)."""
from __future__ import annotations

import json
import tempfile
import unittest
import wave
import xml.etree.ElementTree as ET
from pathlib import Path

from core.nle_export import export_capcut_draft, export_edl, export_fcpxml
from core.project_schema import Clip, MediaAsset, Project, Subtitle, Track
from scripts.first_video import build


def tone(path: Path, duration_s: float = 1.0) -> None:
    frames = int(48000 * duration_s)
    with wave.open(str(path), "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(48000)
        f.writeframes(b"\x00\x00" * frames)


class Sprint30NleExportTests(unittest.TestCase):
    def make_project(self, root: Path) -> tuple[Project, Path]:
        media = root / "media"
        media.mkdir()
        (media / "f1.ppm").write_bytes(b"P6\n64 64\n255\n" + bytes([80, 110, 180]) * (64 * 64))
        (media / "f2.ppm").write_bytes(b"P6\n64 64\n255\n" + bytes([180, 110, 80]) * (64 * 64))
        tone(media / "v1.wav", 1.0)
        tone(media / "v2.wav", 1.5)
        tone(media / "bgm.wav", 5.0)

        proj = Project(
            title="NLE Test Timeline",
            content_locale="uk",
            scenes=(),
            fps=25.0,
            width=1080,
            height=1920,
            tracks=(
                Track("v", "video"),
                Track("a", "audio"),
                Track("s", "subtitle"),
            ),
            media=(
                MediaAsset("i1", "image", "f1.ppm"),
                MediaAsset("i2", "image", "f2.ppm"),
                MediaAsset("a1", "audio", "v1.wav"),
                MediaAsset("a2", "audio", "v2.wav"),
            ),
            clips=(
                Clip("cv1", "v", "i1", 0, 1000),
                Clip("cv2", "v", "i2", 1000, 1500),
                Clip("ca1", "a", "a1", 0, 1000),
                Clip("ca2", "a", "a2", 1000, 1500),
            ),
            subtitles=(
                Subtitle("s1", "s", 0, 1000, "Перша репліка", "uk"),
                Subtitle("s2", "s", 1000, 1500, "Друга репліка", "uk"),
            ),
        )
        return proj, media

    def test_export_fcpxml(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            proj, media = self.make_project(root)
            fcpxml_file = root / "timeline.fcpxml"

            res = export_fcpxml(proj, media, fcpxml_file, bgm_path=media / "bgm.wav")
            self.assertTrue(res.is_file())

            # Parse and validate XML structure
            tree = ET.parse(str(fcpxml_file))
            root_elem = tree.getroot()
            self.assertEqual(root_elem.tag, "fcpxml")
            self.assertEqual(root_elem.attrib.get("version"), "1.8")

            # Check resources
            resources = root_elem.find("resources")
            self.assertIsNotNone(resources)
            assets = resources.findall("asset")
            self.assertGreaterEqual(len(assets), 4)

            # Check spine clips
            spine = root_elem.find(".//spine")
            self.assertIsNotNone(spine)
            clips = spine.findall("asset-clip")
            self.assertGreaterEqual(len(clips), 2)

    def test_export_capcut_draft(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            proj, media = self.make_project(root)
            draft_dir = root / "capcut_draft"

            res = export_capcut_draft(
                proj, media, draft_dir,
                draft_name="My CapCut Story",
                bgm_path=media / "bgm.wav",
                bgm_volume=0.20,
            )
            self.assertTrue(res.is_dir())
            content_file = draft_dir / "draft_content.json"
            meta_file = draft_dir / "draft_meta_info.json"
            self.assertTrue(content_file.is_file())
            self.assertTrue(meta_file.is_file())

            # Validate draft content JSON schema
            content = json.loads(content_file.read_text(encoding="utf-8"))
            self.assertEqual(content["canvas_config"]["width"], 1080)
            self.assertEqual(content["canvas_config"]["height"], 1920)
            self.assertIn("materials", content)
            self.assertIn("tracks", content)

            track_types = [t["type"] for t in content["tracks"]]
            self.assertIn("video", track_types)
            self.assertIn("audio", track_types)
            self.assertIn("text", track_types)

            meta = json.loads(meta_file.read_text(encoding="utf-8"))
            self.assertEqual(meta["draft_name"], "My CapCut Story")

    def test_export_edl(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            proj, media = self.make_project(root)
            edl_file = root / "timeline.edl"

            res = export_edl(proj, media, edl_file)
            self.assertTrue(res.is_file())
            content = edl_file.read_text(encoding="utf-8")
            self.assertIn("TITLE:", content)
            self.assertIn("FCM: NON-DROP FRAME", content)
            self.assertIn("001  AX       V     C", content)
            self.assertIn("002  AX       V     C", content)

    def test_build_with_export_nle_flag(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            audio = root / "audio"
            audio.mkdir()
            tone(audio / "voice1.wav", 1.0)
            tone(root / "music.wav", 3.0)

            plan = root / "plan.json"
            plan.write_text(json.dumps({
                "locale": "uk",
                "title": "NLE Pipeline Test",
                "scenes": [{"text": "Тест для експорту в DaVinci та CapCut"}],
            }, ensure_ascii=False), encoding="utf-8")

            out_dir = root / "nle_out"
            build(
                plan, out_dir, audio_dir=audio,
                render=False,
                bgm_path=root / "music.wav",
                export_nle=True,
            )

            self.assertTrue((out_dir / "project.json").is_file())
            self.assertTrue((out_dir / "project.fcpxml").is_file())
            self.assertTrue((out_dir / "capcut_draft" / "draft_content.json").is_file())
            self.assertTrue((out_dir / "project.edl").is_file())


if __name__ == "__main__":
    unittest.main()
