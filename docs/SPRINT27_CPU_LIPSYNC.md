# Sprint 27 — CPU lip sync (experimental)

Goal: animate a **fictional adult portrait** with the Ukrainian or Russian Silero WAV from Sprint 26, on Windows with integrated graphics only.

## Current scope

An opt-in, external Wav2Lip adapter is wired to Story Studio in `integrations/wav2lip_cpu.py` and `scripts/talking_portrait.py`. It launches the **separately installed** Wav2Lip inference script in CPU mode and checks the output. It does **not** install PyTorch, download weights, or bundle the upstream code. It does **not** yet automatically substitute the resulting talking clip into the Sprint 26 scene renderer.

**Licensing:** Public Wav2Lip releases have non-commercial/research restrictions; model weights and training data may have additional restrictions. This adapter is a technical experiment only. Do not publish commercial outputs without independent clearance. Keep Wav2Lip and weights outside this repository.

**Performance:** CPU lip sync can be very slow, especially on older Intel integrated-graphics systems. Start with a short 2–4-second WAV and a cropped front-facing portrait. An integrated GPU is not equivalent to CUDA; the adapter forces CPU by clearing CUDA visibility. Actual runtime and image quality must be tested on the user's Windows PC.

## Inputs

1. Save the **original, clean portrait** as `assets/portrait-man.png` (do not use a screenshot with embedded subtitles/player controls). The visual mock-up with video controls is not a suitable model input.
2. Use an existing `output/first-video-uk/media/voice1.wav` produced by Sprint 26, or generate a short WAV using the installed Silero voice.
3. Separately install a compatible, trusted Wav2Lip checkout, its Python dependencies and model checkpoint. Verify compatibility with your Python/PyTorch/CPU environment first.

## Run from Story Studio root (PowerShell)

```powershell
python .\scripts\talking_portrait.py `
  --portrait .\assets\portrait-man.png `
  --audio .\output\first-video-uk\media\voice1.wav `
  --wav2lip-dir "C:\PATH\TO\Wav2Lip" `
  --checkpoint "C:\PATH\TO\wav2lip_gan.pth" `
  --wav2lip-python "C:\PATH\TO\wav2lip-venv\Scripts\python.exe" `
  --output .\output\talking-man.mp4
```

Replace **all** `C:\PATH\TO` placeholders with actual installed paths. The output must not already exist. Optionally supply `--ffmpeg "C:\PATH\TO\ffmpeg.exe"` if FFmpeg is not on PATH.

## Verification

```powershell
python -m unittest tests.test_sprint27_cpu_lipsync -v
```

Check that the output plays, lips follow speech, and audio is preserved. **No actual CPU render is claimed until the user runs this test.**

## Next gate

If CPU performance is unusable, benchmark a lightweight alternative rather than silently switching to cloud APIs. Add scene substitution and subtitle overlay only after a successful 2–4-second local talking-portrait render.
