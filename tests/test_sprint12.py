import json
import tempfile
import unittest
from pathlib import Path
from core.project_schema import Project
from core.mp4_render import render_mp4

class Sprint12Tests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(Path('examples/demo_project.json').read_text(encoding='utf-8'))

    def test_audio_outside_video_rejected(self):
        for c in self.data['clips']:
            if c['track_id'] == 'a': c['start_ms'] = 2900
        project = Project.from_json(json.dumps(self.data))
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaisesRegex(ValueError, 'exceeds video duration'):
                render_mp4(project, 'examples/demo_media', Path(tmp)/'output.mp4')

    def test_two_audio_clips_and_burn(self):
        audio = next(c for c in self.data['clips'] if c['track_id']=='a')
        audio['duration_ms']=1000
        extra=dict(audio, id='sound2', start_ms=1500)
        self.data['clips'].append(extra)
        project=Project.from_json(json.dumps(self.data))
        with tempfile.TemporaryDirectory() as tmp:
            result=render_mp4(project,'examples/demo_media',Path(tmp)/'output.mp4',burn_subtitles=True)
            self.assertTrue(Path(result['video']).is_file())
            self.assertTrue(result['burned_subtitles'])
