import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from core.cli import run

FIXTURE = Path(__file__).parent / 'fixtures' / 'project_v3.json'

class CliTests(unittest.TestCase):
    def invoke(self, args):
        with contextlib.redirect_stdout(io.StringIO()) as out, contextlib.redirect_stderr(io.StringIO()) as err:
            code = run(args)
        return code, out.getvalue(), err.getvalue()

    def test_check_valid(self):
        code, out, err = self.invoke(['check', str(FIXTURE)])
        self.assertEqual(code, 0, err)
        self.assertIn('schema v3', out)

    def test_preview_does_not_write(self):
        code, out, err = self.invoke(['preview', str(FIXTURE)])
        self.assertEqual(code, 0, err)
        self.assertIn('bundle_version', json.loads(out))

    def test_bad_project_is_nonzero(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.json'; p.write_text('{broken', encoding='utf-8')
            code, _, err = self.invoke(['check', str(p)])
            self.assertEqual(code, 2)
            self.assertIn('ERROR', err)

    def test_bundle_verify_and_corruption(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); src=root/'media'; src.mkdir()
            fixture=json.loads(FIXTURE.read_text(encoding='utf-8'))
            for asset in fixture['media']:
                p=src/asset['path']; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(b'fake media')
            for scene in fixture['scenes']:
                for field in ('image_path','audio_path'):
                    if scene[field]:
                        p=src/scene[field];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b'fake media')
            out=root/'out'
            code, _, err = self.invoke(['bundle',str(FIXTURE),'--media-root',str(src),'--output',str(out)])
            self.assertEqual(code,0,err)
            self.assertEqual(self.invoke(['verify',str(out)])[0],0)
            (out/'project.json').write_text('tampered',encoding='utf-8')
            self.assertEqual(self.invoke(['verify',str(out)])[0],2)

    def test_missing_bundle_returns_nonzero(self):
        self.assertEqual(self.invoke(['verify','missing-bundle-path'])[0],2)
