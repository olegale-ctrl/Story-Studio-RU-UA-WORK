# Sprint 18 — Edge TTS voice controls and preview

The PowerShell launcher uses only the project-local `.venv/Scripts/python.exe` (no Hermes/PATH fallback).

List the four built-in RU/UA voices:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_edge_demo.ps1 -ListVoices
```

Generate a short preview MP3 without rendering a video:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_edge_demo.ps1 -Locale ru -Gender male -Preview -Rate '+10%' -Pitch '+5Hz'
```

Render with custom speech parameters:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_edge_demo.ps1 -Locale uk -Gender female -Rate '-10%'
```

Cache identity includes provider, voice, exact text, rate and pitch. Non-default settings use isolated output folders and MP4 names. Preview files are distinct from narration scene files. Existing default Sprint 17 cache remains reusable. Edge TTS is an unofficial online service and may intermittently return NoAudioReceived. No commercial rights are asserted.
