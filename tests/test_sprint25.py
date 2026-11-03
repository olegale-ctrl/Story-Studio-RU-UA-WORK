import tempfile
import unittest
import wave
from pathlib import Path
from scripts.voice_studio import hardware_summary, audio_duration_seconds, synthesis_metrics

class Sprint25Tests(unittest.TestCase):
    def test_hardware_summary(self):
        value = hardware_summary({'cpu_name':'Intel test', 'ram_gib':7.9, 'gpu_names':['Intel Graphics']}, {'low_memory_warning':False})
        self.assertIn('Intel test', value)
        self.assertIn('CPU', value)
        self.assertIn('7.9 GiB', value)
    def test_low_memory_warning(self):
        value = hardware_summary({'cpu_name':'test', 'ram_gib':2, 'gpu_names':[]}, {'low_memory_warning':True})
        self.assertIn('LOW RAM', value)
    def test_wav_metrics(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'test.wav'
            with wave.open(str(path), 'wb') as audio:
                audio.setnchannels(1)
                audio.setsampwidth(2)
                audio.setframerate(8000)
                audio.writeframes(b'\x00\x00' * 16000)
            self.assertEqual(audio_duration_seconds(path), 2.0)
            self.assertIn('1.50x', synthesis_metrics(path, 3.0))
    def test_other_audio_no_duration_guess(self):
        self.assertIsNone(audio_duration_seconds(Path('test.mp3')))
        self.assertIn('unavailable', synthesis_metrics(Path('test.mp3'), 2.0))

if __name__ == '__main__':
    unittest.main()
