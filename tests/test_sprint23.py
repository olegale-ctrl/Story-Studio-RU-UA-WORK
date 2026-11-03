import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import voice_studio


class Sprint23Tests(unittest.TestCase):
    def test_edge_still_supported(self):
        cmd = voice_studio.preview_command(Path('python'), 'ru', 'female', '+0%', '+0Hz', 'Hello')
        self.assertIn('edge_voice_demo.py', ' '.join(cmd))

    def test_silero_trust_required(self):
        with self.assertRaises(ValueError):
            voice_studio.silero_preview_command(Path('python'), 'uk', 'ukr_igor', 'Привіт')

    def test_silero_command(self):
        cmd = voice_studio.silero_preview_command(Path('python'), 'uk', 'ukr_igor', 'Привіт', trusted=True)
        self.assertIn('--trust-local-model', cmd)
        self.assertIn('silero_studio_preview.py', ' '.join(cmd))

    def test_wrong_locale_voice(self):
        with self.assertRaises(ValueError):
            voice_studio.silero_preview_command(Path('python'), 'ru', 'ukr_igor', 'test', trusted=True)


if __name__ == '__main__':
    unittest.main()
