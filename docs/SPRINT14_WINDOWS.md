# Sprint 14 — first narrated video (Windows)

Requires Windows PowerShell 5.1, Python and locally installed FFmpeg (Sprint 13). No voice recordings, voices, or external media are distributed.

## 1. Check available Windows TTS voices

```powershell
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
$s.GetInstalledVoices() | ForEach-Object { "$($_.VoiceInfo.Name) — $($_.VoiceInfo.Culture.Name)" }
$s.Dispose()
```

You need a **ru** or **uk** Windows SAPI voice matching the chosen language. If none is installed, the script **stops with a list** rather than mispronouncing Ukrainian with an English voice. Not every Windows language pack provides a SAPI voice.

## 2. Create spoken audio and a valid v3 project

From the project root:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\make_voice_demo.ps1 -Locale uk
```

For Russian use `-Locale ru`. To select a particular installed voice, add `-VoiceName 'EXACT NAME'`.

## 3. Render narrated video

```powershell
python -m core.cli check .\examples\narrated_uk\narrated_project.json
python -m core.cli render-mp4 .\examples\narrated_uk\narrated_project.json --media-root .\examples\narrated_uk\media --output .\narrated-uk-s14.mp4 --burn-subtitles --width 1920 --height 1080 --crf 22
```

The video has three original gradient scenes, three **spoken** audio clips and readable Ukrainian captions. No extra SRT is created when captions are burned, unless `--export-srt` is added. For Russian replace `uk` with `ru` throughout.

## Scope and limits

This is an offline **system TTS demonstration**, not an integrated AI voice platform. Quality and language availability depend on installed Windows voices. The frames are generated original backgrounds, not AI imagery. FFmpeg binaries are not redistributed. Audio and video rendering on the user's Windows require validation.
