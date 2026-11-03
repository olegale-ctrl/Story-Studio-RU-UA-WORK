"""Contract tests: no model file, torch, or network required."""
import unittest
from integrations.silero_local import SileroLocalProvider


class SileroLocalTests(unittest.TestCase):
    def test_ukrainian_voices(self):
        self.assertEqual(SileroLocalProvider.voices('uk'), ('ukr_igor', 'ukr_roman'))

    def test_russian_voices(self):
        self.assertIn('ru_dmitriy', SileroLocalProvider.voices('ru'))

    def test_unknown_locale(self):
        self.assertEqual(SileroLocalProvider.voices('en'), ())

    def test_trust_gate(self):
        with self.assertRaises(ValueError):
            SileroLocalProvider('missing.pt')


if __name__ == '__main__':
    unittest.main()
