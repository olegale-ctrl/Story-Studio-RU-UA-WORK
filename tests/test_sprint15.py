import tempfile
import unittest
from pathlib import Path
from scripts.build_narrated_demo import build
from scripts.inspect_voice_demo import inspect
import wave

class Sprint15Tests(unittest.TestCase):
    def test_inspection_generated_demo(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            media = root / 'media'
            media.mkdir()
            for i in range(1, 4):
                with wave.open(str(media / f'voice{i}.wav'), 'wb') as w:
                    w.setnchannels(1); w.setsampwidth(2); w.setframerate(16000)
                    w.writeframes(b'\x00\x00' * 16000)
            build('uk', root, width=16, height=8)
            result = inspect(root, 'uk')
            self.assertEqual(result['wav_segments'], 3)
            self.assertGreater(result['duration_ms'], 3000)
    def test_wrong_locale_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            media = root / 'media'; media.mkdir()
            for i in range(1, 4):
                with wave.open(str(media / f'voice{i}.wav'), 'wb') as w:
                    w.setnchannels(1); w.setsampwidth(2); w.setframerate(16000)
                    w.writeframes(b'\x00\x00' * 16000)
            build('ru', root, width=16, height=8)
            with self.assertRaises(ValueError): inspect(root, 'uk')

if __name__ == '__main__': unittest.main()
