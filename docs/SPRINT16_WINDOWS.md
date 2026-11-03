# Sprint 16 — Edge TTS RU/UA narrated demo

Unpack Sprint16.zip into existing project root and overwrite files. **Do not remove other project files.**

Prerequisites: Python with `edge-tts` (`python -m pip install edge-tts`); existing `scripts/build_narrated_demo.py`, `scripts/inspect_voice_demo.py`, `core.cli` from Sprint 14/15; FFmpeg in `tools/ffmpeg/bin/ffmpeg.exe` or PATH; internet.

PowerShell:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_edge_demo.ps1 -ListVoices
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_edge_demo.ps1 -Locale uk -Gender female
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_edge_demo.ps1 -Locale uk -Gender male
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_edge_demo.ps1 -Locale ru -Gender female
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_edge_demo.ps1 -Locale ru -Gender male
```

Each run writes to `examples/narrated_<locale>/media/voice*.mp3`, converts to PCM WAV, builds timeline, validates it, and creates `narrated-<locale>-s16.mp4` with 1920x1080 burned subtitles. **Move or rename the previous output MP4 before rerunning the same locale**, to avoid overwriting. `-NoRender` generates project/audio only; `-ExportSrt` also creates a separate SRT (may cause double subtitles in players). Set `-Voice uk-UA-OstapNeural` to explicitly select a same-language voice.

`edge-tts` uses an online consumer endpoint that may change. Commercial output rights have not been confirmed by Microsoft: this is an experimental local workflow, not a cleared commercial publishing provider. Never ship FFmpeg or voice assets in release ZIPs without licensing review.

Test: `python -m unittest discover -s tests -v`. Windows end-to-end run is pending user confirmation.
