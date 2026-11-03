import unittest
from unittest.mock import patch
from pathlib import Path
from core.mp4_render import find_ffmpeg, render_mp4
from core.project_schema import Project

class Sprint11Tests(unittest.TestCase):
    def test_crf_range(self):
        import json
        project = Project.from_json(Path('examples/demo_project.json').read_text(encoding='utf-8'))
        with self.assertRaisesRegex(ValueError, 'CRF'):
            render_mp4(project, 'examples/demo_media', 'unused.mp4', ffmpeg='python', crf=52)
    def test_find_ffmpeg_path_or_error(self):
        try:
            value = find_ffmpeg()
            self.assertTrue(value)
        except ValueError as e:
            self.assertIn('FFmpeg', str(e))
