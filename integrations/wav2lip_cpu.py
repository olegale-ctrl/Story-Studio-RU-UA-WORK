"""Opt-in CPU Wav2Lip adapter. External checkout and weights are NOT distributed.

Wav2Lip's public release is restricted to research/personal/non-commercial use.
Check its current terms and all model dependencies before any commercial use.
"""
from __future__ import annotations

import subprocess
from pathlib import Path


def render_talking_portrait(*, face: Path, audio: Path, output: Path,
                            checkout: Path, checkpoint: Path,
                            python_exe: Path, ffmpeg_exe: Path | None = None,
                            timeout_seconds: int = 7200) -> Path:
    face, audio, output = Path(face), Path(audio), Path(output)
    checkout, checkpoint = Path(checkout), Path(checkpoint)
    python_exe = Path(python_exe)
    for label, path in (("portrait", face), ("audio", audio),
                        ("checkpoint", checkpoint), ("Python", python_exe),
                        ("inference.py", checkout / "inference.py")):
        if not path.is_file():
            raise FileNotFoundError(f"{label} missing: {path}")
    if face.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
        raise ValueError("Portrait must be PNG or JPEG")
    if audio.suffix.lower() != ".wav":
        raise ValueError("Audio must be WAV")
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite: {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [str(python_exe.resolve()), str((checkout / "inference.py").resolve()),
               "--checkpoint_path", str(checkpoint.resolve()),
               "--face", str(face.resolve()), "--audio", str(audio.resolve()),
               "--outfile", str(output.resolve()), "--static", "True",
               "--fps", "25", "--pads", "0", "10", "0", "0"]
    # Wav2Lip uses ffmpeg through PATH. Add its directory only when supplied.
    import os
    env = os.environ.copy()
    env["CUDA_VISIBLE_DEVICES"] = ""
    if ffmpeg_exe is not None:
        ffmpeg_exe = Path(ffmpeg_exe)
        if not ffmpeg_exe.is_file():
            raise FileNotFoundError(f"FFmpeg missing: {ffmpeg_exe}")
        env["PATH"] = str(ffmpeg_exe.resolve().parent) + os.pathsep + env.get("PATH", "")
    subprocess.run(command, cwd=str(checkout.resolve()), env=env,
                   check=True, timeout=timeout_seconds)
    if not output.is_file() or output.stat().st_size == 0:
        raise RuntimeError("Lip-sync tool did not produce a nonempty MP4")
    return output
