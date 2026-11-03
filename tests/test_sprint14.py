import json
from pathlib import Path
import tempfile
import unittest
import wave
from scripts.build_narrated_demo import build, duration_ms
from core.project_schema import Project

class Sprint14Tests(unittest.TestCase):
    def test_build_both_locales(self):
        for locale in ('ru','uk'):
            with self.subTest(locale=locale), tempfile.TemporaryDirectory() as d:
                root=Path(d)
                media=root/'media'; media.mkdir()
                for i in range(1,4):
                    with wave.open(str(media/f'voice{i}.wav'),'wb') as f:
                        f.setnchannels(1); f.setsampwidth(2); f.setframerate(16000); f.writeframes(b'\x00\x00'*16000)
                project_path=build(locale,root,32,18)
                project=Project.from_json(project_path.read_text(encoding='utf-8'))
                self.assertEqual(len(project.clips),6)
                self.assertEqual(len(project.subtitles),3)
                self.assertEqual(project.content_locale,locale)
                self.assertEqual(duration_ms(media/'voice1.wav'),1000)
                self.assertTrue((media/'frame1.ppm').is_file())
    def test_missing_voice_fails(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(FileNotFoundError): build('uk',Path(d),32,18)
if __name__=='__main__': unittest.main()
