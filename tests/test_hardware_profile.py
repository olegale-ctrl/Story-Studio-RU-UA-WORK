import unittest
from unittest.mock import patch
from core.hardware_profile import probe, recommend


class HardwareProfileTests(unittest.TestCase):
    def test_cpu_is_always_default(self):
        self.assertEqual(recommend({'ram_gib': 16})['default_device'], 'cpu')

    def test_gpu_name_does_not_imply_acceleration(self):
        with patch('core.hardware_profile._windows_info', return_value={
            'cpu': 'Intel CPU', 'ram_bytes': 8 * 1024**3,
            'gpu_names': ['Intel UHD Graphics'], 'logical_processors': 8
        }):
            profile = probe()
        self.assertFalse(profile['gpu_tts_acceleration_verified'])
        self.assertEqual(recommend(profile)['gpu_acceleration'], 'disabled_until_backend_verified')

    def test_low_ram_warning(self):
        self.assertTrue(recommend({'ram_gib': 2})['low_memory_warning'])
        self.assertFalse(recommend({'ram_gib': None})['low_memory_warning'])

    def test_probe_handles_missing_windows_data(self):
        with patch('core.hardware_profile._windows_info', return_value={}):
            self.assertTrue(probe()['cpu_available'])


if __name__ == '__main__':
    unittest.main()
