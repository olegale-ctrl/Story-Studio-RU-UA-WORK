import json
import tempfile
import unittest
from pathlib import Path
from core.project_schema import Project
from core.mp4_render import render_mp4

class Sprint13Tests(unittest.TestCase):
    def setUp(self):
        self.project = Project.from_json(Path('examples/demo_project.json').read_text(encoding='utf-8'))

    def test_hd_burn_without_sidecar(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'hd.mp4'
            result = render_mp4(self.project, 'examples/demo_media', path, burn_subtitles=True, width=1280, height=720)
            self.assertEqual((result['width'], result['height']), (1280, 720))
            self.assertEqual(result['subtitles'], [])
            self.assertTrue(path.exists())
            self.assertFalse((Path(temp) / 'hd.sub01.srt').exists())

    def test_optional_sidecar(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'with_srt.mp4'
            result = render_mp4(self.project, 'examples/demo_media', path, burn_subtitles=True, width=640, height=360, export_srt_files=True)
            self.assertEqual(len(result['subtitles']), 1)
            self.assertTrue(Path(result['subtitles'][0]).exists())

    def test_odd_dimension_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            with self.assertRaisesRegex(ValueError, 'width must be an even integer'):
                render_mp4(self.project, 'examples/demo_media', Path(temp)/'bad.mp4', width=1279, height=720)
