# Sprint 26 — first narrated video (Windows)

Goal: **produce a complete MP4 with spoken RU/UA narration, images and burned subtitles**, not merely a three-color technology demo.

The implementation uses our existing v3 timeline, FFmpeg renderer and isolated Silero provider. It does **not** execute the upstream Chinese modules or use their corpora. The pinned original remains a design/engineering reference, subject to CC BY-NC-SA licensing restrictions.

## One-command Windows validation with local Silero

From the existing project root in PowerShell (where `.venv` and local FFmpeg are already configured):

```powershell
.\.venv\Scripts\python.exe .\scripts\first_video.py `
  --plan .\examples\first_video_plan_uk.json `
  --silero-model C:\StoryStudioModels\v5_cis_base_nostress.pt `
  --voice ukr_igor `
  --output-dir .\output\first-video-uk
```

If your trusted Silero model is elsewhere, substitute its actual path. The `output\first-video-uk` folder must not exist before the run; use a new output name for a repeat. The script will print `VIDEO:` and `PROJECT:` paths. Output video is `output\first-video-uk\first-video.mp4`.

To preview the project without FFmpeg rendering, append `--no-render`. To create a Russian version, choose `first_video_plan_ru.json` and a compatible Russian Silero speaker (e.g. `ru_igor`). No cloud API, image generator, or paid service is called.

## Real pictures (optional)

The `scenes` entries in the plan can each specify `"image": "scene1.jpg"`. Put these images in one local directory and add `--images-dir C:\path\to\images`. Each image filename must be a simple PNG/JPG/PPM filename in that directory, not an absolute path. If omitted, an original gradient background is generated. Avoid copyrighted/unknown-rights imagery for redistribution.

## Existing audio (optional)

Instead of Silero, pass `--audio-dir C:\path\to\wavs` containing `voice1.wav`, `voice2.wav`, ... for the plan's scenes. This is useful for checking the pipeline independently of TTS and for reusing approved voices.

## Verification

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe -m core.cli check .\output\first-video-uk\project.json
```

Open the MP4 in VLC. Verify audible Ukrainian speech, correct order, subtitle text/timing, no subtitle shadows/filename overlays, and correct image aspect ratio. Send the last 15 PowerShell lines if an error occurs.

## Known limitations

- Scene-level subtitle timing only; not word-level forced alignment.
- No LLM scenario generation, image generation, editor-native export or CapCut integration yet.
- Silero local model is trusted PyTorch code and should be used only from a source the user trusts.
- Test suite can validate the offline timeline with synthetic WAVs, but real Silero/Windows and playback need user validation.
- Current upstream license rights remain unresolved for commercial reuse. This Sprint 26 code does not import additional upstream modules.
