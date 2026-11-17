import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from integrations.wav2lip_cpu import render_talking_portrait


class Wav2LipCpuTests(unittest.TestCase):
    def test_requires_explicit_external_assets(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            with self.assertRaises(FileNotFoundError):
                render_talking_portrait(face=root / "missing.png",
                    audio=root / "missing.wav", output=root / "out.mp4",
                    checkout=root / "wav2lip", checkpoint=root / "model.pth",
                    python_exe=root / "python.exe")

    def test_builds_cpu_command_without_executing_model(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            checkout = root / "wav2lip"
            checkout.mkdir()
            for name in ("portrait.png", "voice.wav", "model.pth", "python.exe"):
                (root / name).write_bytes(b"test")
            (checkout / "inference.py").write_text("# mock")
            output = root / "out.mp4"
            def fake_run(cmd, **kwargs):
                self.assertIn("--static", cmd)
                self.assertEqual(kwargs["env"]["CUDA_VISIBLE_DEVICES"], "")
                self.assertEqual(kwargs["cwd"], str(checkout.resolve()))
                output.write_bytes(b"video")
            with patch("integrations.wav2lip_cpu.subprocess.run", side_effect=fake_run):
                result = render_talking_portrait(face=root / "portrait.png",
                    audio=root / "voice.wav", output=output, checkout=checkout,
                    checkpoint=root / "model.pth", python_exe=root / "python.exe")
            self.assertEqual(result, output)

    def test_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            checkout = root / "wav2lip"
            checkout.mkdir()
            for name in ("portrait.png", "voice.wav", "model.pth", "python.exe"):
                (root / name).write_bytes(b"test")
            (checkout / "inference.py").write_text("# mock")
            output = root / "out.mp4"
            output.write_bytes(b"original")
            with self.assertRaises(FileExistsError):
                render_talking_portrait(face=root / "portrait.png",
                    audio=root / "voice.wav", output=output, checkout=checkout,
                    checkpoint=root / "model.pth", python_exe=root / "python.exe")
            self.assertEqual(output.read_bytes(), b"original")


if __name__ == "__main__":
    unittest.main()
