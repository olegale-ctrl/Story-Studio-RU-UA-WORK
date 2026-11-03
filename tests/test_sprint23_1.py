"""Regression gate for the current Sprint 23.2 ASCII-path Silero policy.

The old Sprint 23.1 Unicode temporary-copy tests were superseded in Sprint 23.2.
Do not silently restore a 90 MB model copy to a temporary location.
"""
import tempfile
import unittest
from pathlib import Path
from integrations.silero_local import SileroLocalProvider


class Sprint231CurrentPolicyTests(unittest.TestCase):
    def test_missing_trusted_model_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'v5_cis_base_nostress.pt'
            with self.assertRaises(FileNotFoundError):
                SileroLocalProvider(path, trusted=True)

    def test_unexpected_model_filename_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'wrong-model.pt'
            path.write_bytes(b'placeholder')
            with self.assertRaisesRegex(ValueError, 'Unexpected model filename'):
                SileroLocalProvider(path, trusted=True)

    def test_no_implicit_temporary_model_copy(self):
        self.assertFalse(hasattr(SileroLocalProvider, '_compatible_model_path'))


if __name__ == '__main__':
    unittest.main()
