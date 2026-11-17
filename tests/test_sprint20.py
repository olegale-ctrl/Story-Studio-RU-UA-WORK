"""Sprint 20 voice catalog tests.

Rewritten to plain unittest so the suite runs with
`python -m unittest discover -s tests -v` without a pytest dependency.
pytest still collects unittest.TestCase classes unchanged.
"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from voice_studio import VOICE_CATALOG, preview_command, validate_settings


class Sprint20Tests(unittest.TestCase):
    def test_catalog(self):
        self.assertEqual(VOICE_CATALOG['ru']['male'], 'ru-RU-DmitryNeural')
        self.assertEqual(VOICE_CATALOG['uk']['female'], 'uk-UA-PolinaNeural')

    def test_command_has_preview_and_voice(self):
        cmd = preview_command(Path('python.exe'), 'ru', 'male', '+10%', '+5Hz', 'Тест', True)
        self.assertIn('--preview', cmd)
        self.assertIn('--strict-voice-settings', cmd)
        self.assertEqual(cmd[cmd.index('--voice') + 1], 'ru-RU-DmitryNeural')
        self.assertEqual(cmd[cmd.index('--preview-text') + 1], 'Тест')

    def test_invalid_settings(self):
        for rate, pitch in (('+101%', '+0Hz'), ('0%', '+0Hz'), ('+0%', '5Hz'), ('+0%', '+101Hz')):
            with self.subTest(rate=rate, pitch=pitch):
                with self.assertRaises(ValueError):
                    validate_settings('ru', 'male', rate, pitch, 'Тест')

    def test_empty_text(self):
        with self.assertRaises(ValueError):
            validate_settings('uk', 'female', '+0%', '+0Hz', '  ')


if __name__ == '__main__':
    unittest.main()
