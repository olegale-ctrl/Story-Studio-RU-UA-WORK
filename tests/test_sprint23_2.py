import os
import unittest
from pathlib import Path
from unittest.mock import patch
from scripts.voice_studio import silero_preview_command
from integrations.silero_local import SileroLocalProvider

class Sprint232Tests(unittest.TestCase):
    def test_windows_default_path(self):
        with patch('scripts.voice_studio.sys.platform', 'win32'), patch.dict(os.environ, {}, clear=True):
            cmd = silero_preview_command(Path('python'), 'uk', 'ukr_igor', 'Привіт', trusted=True)
        self.assertIn(r'C:\StoryStudioModels\v5_cis_base_nostress.pt', cmd)
    def test_env_override(self):
        with patch.dict(os.environ, {'STORY_SILERO_MODEL': '/custom/v5_cis_base_nostress.pt'}):
            cmd = silero_preview_command(Path('python'), 'ru', 'ru_dmitriy', 'Тест', trusted=True)
        self.assertIn('/custom/v5_cis_base_nostress.pt', cmd)
    def test_untrusted_blocked(self):
        with self.assertRaises(ValueError):
            silero_preview_command(Path('python'), 'uk', 'ukr_igor', 'Тест', trusted=False)
    def test_provider_has_no_temp_copy(self):
        self.assertFalse(hasattr(SileroLocalProvider, '_compatible_model_path'))

if __name__ == '__main__':
    unittest.main()
