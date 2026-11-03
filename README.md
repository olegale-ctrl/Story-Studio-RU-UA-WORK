# Story Studio RU/UA

A Windows-first Russian/Ukrainian adaptation and substantial rework of [konlu/story-studio](https://github.com/konlu/story-studio). This is **not just a translation**: the goal is a reusable, local-first video-production pipeline with original RU/UA prompts, speech, subtitles, media assembly and verified export paths.

## Current status — Sprint 26 (2026-11-03)

- RU/UA project code, CLI, neutral timeline, FFmpeg rendering and Windows scripts are tracked in this repository.
- Edge TTS (online, experimental) and local Silero (explicitly trusted external model) can be selected through the Voice Studio desktop UI.
- Sprint 25.1 fixes false `Preview failed` messages with Cyrillic Windows profile paths and displays synthesis timing, WAV duration and real-time factor.
- Sprint 25.1 Voice Studio + Silero preview and playback were confirmed on Windows by the user. Automated CI checks for Python 3.10 and 3.13 passed for the Sprint 26 pull request. Not a production release.
- **Sprint 26:** `scripts/first_video.py` assembles a RU/UA narrated video from a scene plan, trusted local Silero or existing WAV files, optional local images, scene-level subtitles and the existing FFmpeg renderer. Real end-to-end Windows MP4 playback still requires user verification.
- Windows 10/11 is the primary target; portable architecture for macOS/Linux is planned.

## Sprint 26: first video on Windows

See [`docs/SPRINT26_FIRST_VIDEO_WINDOWS.md`](docs/SPRINT26_FIRST_VIDEO_WINDOWS.md) for the full procedure. Example, from the project root (replace the model path with your actual local model path):

```powershell
python .\scripts\first_video.py `
  --plan .\examples\first_video_plan_uk.json `
  --silero-model "C:\StoryStudioModels\v5_cis_base_nostress.pt" `
  --voice ukr_igor `
  --output-dir .\output\first-video-uk
```

The output is `output/first-video-uk/first-video.mp4`. Use a new output directory for each run. This is an MVP with scene-level timing, not word-level alignment.

## Quick checks (existing Windows working folder)

```powershell
python -m unittest discover -s tests -v
powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_voice_studio.ps1
```

The Sprint 25.1 incremental ZIP remains the previous Voice Studio update, **not** the Sprint 26 package. For Sprint 26, download the current `main` source or update a Git checkout; do not overwrite local `.venv`, FFmpeg, model weights, cached media or personal settings.

## Preserving the original video-creation technology

The **complete original repository** is pinned as a Git submodule at `upstream/konlu-full`. It contains the original Chinese modules, corpora, references and scripts in a separate tree. To obtain it in a Git checkout:

```powershell
git submodule update --init --recursive
```

An additional 40-file byte-identical engineering reference is committed under `upstream/konlu-story-studio/`. These modules include rendering, motion, speech alignment, pacing, Jianying export and setup. We study and adapt proven mechanisms rather than rebuilding everything from zero. The original is *not* automatically imported into the RU/UA runtime.

## Project organization

- `core/` — media/timeline/render/bundle library and CLI
- `scripts/` — Windows scripts, TTS demos and Voice Studio
- `integrations/` — opt-in local providers (no bundled weights)
- `locales/` — RU and UK language packages
- `tests/` — automated tests and temporary test fixture generator
- `project-log/` — decisions, worklog, roadmap, next session
- `LICENSES/` — provenance, assets/dependency tracking and release gates
- `upstream/` — isolated original project and technical reference snapshot

## Licensing and commercial-use warning

**Do not treat this repository as cleared for commercial redistribution.** The current pinned original `konlu/story-studio` declares **CC BY-NC-SA 4.0**. Our older local archive contained an MIT-license copy, but that does **not** establish that the current original or all inherited modules, datasets, assets and services are MIT-licensed. Review `LICENSES/IMPORT_LICENSE_GATE.md` and `docs/UPSTREAM_TECHNOLOGY_IMPORT.md`. Commercial Professional/Cloud plans require rights clearance or independently implemented substitutes.

The code and voice models have separate licenses. FFmpeg binaries, Silero weights, API keys and generated media are not included in Git.

## Development approach

GitHub stores the source of truth and each tested change; compact Sprint ZIPs update the Windows working installation. See `MASTER_PROMPT.md` and `project-log/NEXT_SESSION.md` for project goals and current state.
