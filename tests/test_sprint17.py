import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts' / 'edge_voice_demo.py'
spec = importlib.util.spec_from_file_location('edge_voice_demo', SCRIPT)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

class Sprint17Tests(unittest.TestCase):
    def test_cache_key_voice_and_text(self):
        a = mod.cache_key('ru-RU-SvetlanaNeural', 'Привет')
        self.assertNotEqual(a, mod.cache_key('ru-RU-DmitryNeural', 'Привет'))
        self.assertNotEqual(a, mod.cache_key('ru-RU-SvetlanaNeural', 'Другой текст'))
    def test_voice_validation(self):
        with self.assertRaises(ValueError):
            mod.resolve_voice('uk', 'ru-RU-DmitryNeural', 'male')
    def test_versioned_outputs(self):
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            p = mod.next_video_path(base, 'ru', 'ru-RU-DmitryNeural')
            p.touch()
            self.assertNotEqual(p, mod.next_video_path(base, 'ru', 'ru-RU-DmitryNeural'))
            self.assertNotEqual(p, mod.next_video_path(base, 'ru', 'ru-RU-SvetlanaNeural'))
    def test_cache_rejects_wrong_voice(self):
        with tempfile.TemporaryDirectory() as d:
            mp3 = Path(d)/'voice1.mp3'
            mp3.write_bytes(b'x'*2000)
            mp3.with_suffix('.cache.json').write_text('{"key":"wrong"}', encoding='utf-8')
            with patch.object(mod, 'valid_audio', side_effect=[True, True]), patch.object(mod.subprocess, 'run') as run:
                run.return_value.returncode = 0
                run.side_effect = lambda cmd, **kw: (mp3.with_name('voice1.partial.mp3').write_bytes(b'x'*2000), type('Result', (), {'returncode': 0})())[1]
                mod.synthesize('ru-RU-DmitryNeural','text',mp3,attempts=1)
                self.assertEqual(run.call_count, 1)
                self.assertIn('ru-RU-DmitryNeural', mp3.with_suffix('.cache.json').read_text(encoding='utf-8'))
    def test_matching_cache_skips_generation(self):
        with tempfile.TemporaryDirectory() as d:
            mp3=Path(d)/'voice1.mp3'; mp3.write_bytes(b'x'*2000)
            mp3.with_suffix('.cache.json').write_text('{"key":"'+mod.cache_key('voice','text')+'"}', encoding='utf-8')
            with patch.object(mod, 'valid_audio', return_value=True), patch.object(mod.subprocess, 'run') as run:
                mod.synthesize('voice','text',mp3)
                run.assert_not_called()

if __name__=='__main__': unittest.main()
