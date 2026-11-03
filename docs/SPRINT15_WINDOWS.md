# Sprint 15 — one-command narrated demo

Unpack Sprint15.zip into the existing project root, replacing files. Sprint14 must already be installed. No FFmpeg binaries or TTS voices are included.

**List available Windows SAPI voices** (Windows PowerShell 5.1):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_narrated_demo.ps1 -ListVoices
```

**Create narrated Ukrainian MP4** (requires an installed `uk` SAPI voice):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_narrated_demo.ps1 -Locale uk
```

For Russian use `-Locale ru`. Optional `-VoiceName 'exact installed voice name'`, `-ExportSrt`, `-Crf 20`.

The script checks voice locale, creates 3 WAV segments, generates JSON/PPM project, validates timing and schema, and renders `narrated-uk-s15.mp4` at 1920x1080 with burned captions. It refuses to overwrite existing output. If no matching SAPI voice exists, **it stops without pretending to create narration**. Next step is to select a separately licensed local TTS provider.

This is not an AI-generated video and not proof of voice quality on the user's PC. No Windows execution has been performed by the developer here.
