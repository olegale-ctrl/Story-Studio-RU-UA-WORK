import hashlib
import tempfile
import unittest
from pathlib import Path
from scripts.voice_studio import preview_file_signature, preview_output_path


class Sprint251Tests(unittest.TestCase):
    def test_silero_unicode_root_independent_of_console_text(self):
        root = Path('/tmp/Олег/Story-Studio-RU-UA')
        actual = preview_output_path('silero_local', 'uk', 'ukr_igor', root=root)
        self.assertEqual(actual, root / 'examples/voice_previews/silero-uk-ukr_igor.wav')

    def test_silero_invalid_voice_rejected(self):
        with self.assertRaises(ValueError):
            preview_output_path('silero_local', 'uk', 'ru_dmitriy')

    def test_edge_default_preview_matches_cli(self):
        root = Path('/tmp/Имя/Story')
        text = 'Тестовый голос'
        got = preview_output_path('edge', 'ru', 'female', text=text, root=root)
        digest = hashlib.sha256(text.encode('utf-8')).hexdigest()[:12]
        self.assertEqual(got, root / 'examples/narrated_ru/ru-ru-svetlananeural/media' / f'preview-{digest}.mp3')

    def test_edge_settings_folder(self):
        result = preview_output_path('edge', 'uk', 'male', '+5%', '-2Hz', 'Тест')
        digest = hashlib.sha256('+5%|-2Hz'.encode('utf-8')).hexdigest()[:12]
        self.assertIn('settings-' + digest, result.parts)

    def test_file_signature_for_missing_and_changed_file(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'silero.wav'
            self.assertIsNone(preview_file_signature(path))
            path.write_bytes(b'a' * 2048)
            sig = preview_file_signature(path)
            self.assertEqual(sig[0], 2048)
            path.write_bytes(b'b' * 4096)
            self.assertNotEqual(sig, preview_file_signature(path))


if __name__ == '__main__':
    unittest.main()
