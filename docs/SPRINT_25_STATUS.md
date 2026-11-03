# Sprint 25 — verified state

- Windows 10/11 is the primary platform, with portability to macOS/Linux planned.
- CPU-only offline Silero works locally after placing the trusted model at `C:\StoryStudioModels\v5_cis_base_nostress.pt` (not committed).
- `scripts/voice_studio.py` exists in the latest user-provided snapshot.
- Silero preview produced a valid WAV: mono, 24000 Hz, approximately 2.16 seconds.
- The Voice Studio UI incorrectly showed `Preview failed` and omitted synthesis metrics. A likely cause is console encoding corruption in the `PREVIEW:` path when the Windows user directory contains Cyrillic characters; this still needs a tested fix.
- Existing local source tree is the authoritative Sprint 25 version until it is safely imported.
- Do not commit downloaded model weights, `.venv`, generated media, API tokens, or local hardware-specific paths as configuration defaults.
- Do not claim this bootstrap repository is a complete or tested release.
