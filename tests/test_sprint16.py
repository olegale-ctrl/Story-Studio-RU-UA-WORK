import importlib.util
from pathlib import Path
import tempfile
import unittest

SRC=Path(__file__).resolve().parents[1]/'scripts'/'edge_voice_demo.py'
spec=importlib.util.spec_from_file_location('edge_voice_demo',SRC)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
class EdgeVoiceTest(unittest.TestCase):
    def test_catalog(self):
        self.assertEqual(len([v for voices in mod.VOICES.values() for v in voices.values()]),4)
    def test_locale_guard(self):
        with self.assertRaises(ValueError): mod.resolve_voice('uk','ru-RU-DmitryNeural','male')
    def test_default_male(self):
        self.assertEqual(mod.resolve_voice('uk',None,'male'),'uk-UA-OstapNeural')
    def test_default_russian(self):
        self.assertEqual(mod.resolve_voice('ru',None,'female'),'ru-RU-SvetlanaNeural')
    def test_ffmpeg_local(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(mod.ffmpeg_executable(Path(tmp)),'ffmpeg')
if __name__=='__main__':unittest.main()
