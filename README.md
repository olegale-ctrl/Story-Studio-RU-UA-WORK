# Story Studio RU/UA

A Windows-first Russian/Ukrainian adaptation and substantial rework of [konlu/story-studio](https://github.com/konlu/story-studio). This is **not just a translation**: the goal is a reusable, local-first video-production pipeline with original RU/UA prompts, speech, subtitles, media assembly and verified export paths.

## Current status — Sprint 26 Windows validation (2026-11-16)

- RU/UA project code, CLI, neutral timeline, FFmpeg rendering and Windows scripts are tracked in this repository.
- Edge TTS (online, experimental) and local Silero (explicitly trusted external model) can be selected through the Voice Studio desktop UI.
- **The Sprint 26 first-video pipeline is verified on Windows**: local Silero narration in Russian and Ukrainian, user-supplied WAV files and images, burned subtitles with verified timing, and a valid 1280×720 H.264/AAC MP4. See `SPRINT26_WINDOWS_VALIDATION_REPORT.md`.
- **346 automated tests pass** (349 under pytest) on Windows with Python 3.10 and 3.13; CI runs the suite on Ubuntu and Windows 11. Not a production release.
- Windows 10/11 is the primary target; portable architecture for macOS/Linux is planned.

## Quick checks (existing Windows working folder)

```powershell
python -m unittest discover -s tests -v
.\.venv\Scripts\python.exe .\scripts\first_video.py `
  --plan .\examples\first_video_plan_uk.json `
  --silero-model C:\StoryStudioModels\v5_cis_base_nostress.pt `
  --voice ukr_igor `
  --output-dir .\output\first-video-uk
```

Under pytest, pass an ASCII `--basetemp` if your Windows profile name is not ASCII
(`pytest` derives its temporary directory from `%TEMP%`).

Use the incremental `Sprint_25_1.zip` to update an existing tested local installation. Keep `.venv`, user-installed FFmpeg, model weights, cached media and personal settings outside Git. See `INSTALL_S25_1.txt`.

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
