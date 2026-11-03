import tempfile
import unittest
from pathlib import Path
from core.mp4_render import render_mp4
from core.project_schema import Project, Track, MediaAsset, Clip

class Mp4Tests(unittest.TestCase):
    def project(self, duration=1000):
        return Project('demo', 'uk', (), fps=25, width=64, height=64,
                       tracks=(Track('v', 'video'),), media=(MediaAsset('i', 'image', 'img.ppm'),),
                       clips=(Clip('c', 'v', 'i', 0, duration),))

    def test_missing_media(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):
                render_mp4(self.project(), tmp, Path(tmp).parent / 'test-output.mp4')

    def test_frame_alignment(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                render_mp4(self.project(1010), tmp, Path(tmp).parent / 'test-output.mp4')

    def test_existing_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'out.mp4'; out.touch()
            with self.assertRaises(FileExistsError):
                render_mp4(self.project(), tmp, out)

    def test_real_ffmpeg(self):
        import shutil
        if not shutil.which('ffmpeg'):
            self.skipTest('ffmpeg not installed')
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / 'media'; root.mkdir()
            (root / 'img.ppm').write_bytes(b'P6\n64 64\n255\n' + bytes([80, 110, 180]) * (64*64))
            out = Path(tmp) / 'video.mp4'
            result = render_mp4(self.project(), root, out)
            self.assertTrue(out.stat().st_size > 1000)
            self.assertEqual(result['duration_ms'], 1000)
