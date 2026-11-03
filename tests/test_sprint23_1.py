import importlib.util
import pathlib
import tempfile
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('silero_local', ROOT / 'integrations' / 'silero_local.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class Sprint231Tests(unittest.TestCase):
    def test_non_windows_uses_original(self):
        source = pathlib.Path('some/модель.pt')
        with patch.object(module.os, 'name', 'posix'):
            with module.SileroLocalProvider._compatible_model_path(source) as path:
                self.assertEqual(path, source)

    def test_windows_ascii_uses_original(self):
        source = pathlib.Path('C:/models/model.pt')
        with patch.object(module.os, 'name', 'nt'):
            with module.SileroLocalProvider._compatible_model_path(source) as path:
                self.assertEqual(path, source)

    @unittest.skipUnless(__import__('os').name == 'nt', 'Windows-specific integration test')
    def test_windows_unicode_path_uses_ascii_copy_and_cleans_up(self):
        import hashlib
        import os
        with tempfile.TemporaryDirectory() as directory:
            source = pathlib.Path(directory) / 'Олег' / 'model.pt'
            source.parent.mkdir()
            source.write_bytes(b'test bytes')
            with patch.object(module, 'KNOWN_SHA256', hashlib.sha256(b'test bytes').hexdigest()):
                with module.SileroLocalProvider._compatible_model_path(source) as copied:
                    self.assertTrue(copied.exists())
                    self.assertEqual(copied.read_bytes(), b'test bytes')
                    self.assertTrue(str(copied).isascii())
                    temporary = copied
                self.assertFalse(temporary.exists())


if __name__ == '__main__':
    unittest.main()
