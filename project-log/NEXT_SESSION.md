# Next session — after Sprint 28 Stage 2 Architecture (2026-11-17)

**Stage 2 (Архитектура) COMPLETED.** Typed `VoiceProvider` contract + license
registry + commercial gate in `core/providers.py` (ADR-0009); `first_video.py`
routes both narration sources through the contract; deterministic CycloneDX
SBOM generated from the Stage 1 registers with a `--check` drift gate
(`python scripts/generate_sbom.py --check` must stay green). Tests: 374 pytest
+ 19 subtests OK, unittest 368 OK (`.venv`, Windows).

**Next exact step: begin Stage 3 — RU/UA сценарии (этап 3).** Complete:
- [ ] Define the example-library format for scene plans (original RU/UA texts only)
- [ ] Add 3–5 verified original scene plans with legal images (own/CC0) per locale
- [ ] Wire examples through the first-video pipeline; document each example's provenance in ASSET_REGISTER.csv
- [ ] Keep provider adapters aligned with ADR-0009 (adapter + SPECS row + register row + tests)
- [ ] Update ROADMAP_STATUS.md to mark Stage 3 progress

**Open items carried over:**
- Git repo status on the user machine (Stage 0 blocker) — confirm the local clone/remote sync
- Clean Win10/11 install validation (Stage 7), GUI not covered by CI
- Image-provider contract deferred until Stage 5 (Визуальная система)
- No voice provider is APPROVED for commercial use — commercial gate stays closed

---

# Next session — after Sprint 26 Windows validation (2026-11-16)

**Windows validation gate PASSED.** The Sprint 26 first-video pipeline was run end to end on Windows with local Silero for both locales, plus user-media (`--audio-dir` + `--images-dir`) runs. Full MP4s verified with `ffprobe` and `volumedetect`, test suite 116/116 OK in `.venv` (Python 3.10.11) and system Python 3.15. Two pre-existing test defects fixed.

**Next exact step:** begin **Stage 1 — License Audit** (этап 1). Complete:
- [ ] Populate DEPENDENCY_LICENSES.csv with all runtime Python packages (25 items verified)
- [ ] Complete ASSET_REGISTER.csv with all media assets (local QR codes reviewed, upstream media BLOCKED/REPLACE)
- [ ] Generate THIRD_PARTY_NOTICES.md with formal copyright notices per component
- [ ] Document all licensing decisions in LICENSE_REVIEW_LOG.md
- [ ] Verify Silero model SHA256 matches known good copy (already in code)
- [ ] Confirm edge-tts COMMERCIAL BLOCKED status documented
- [ ] Update ROADMAP_STATUS.md to mark Stage 1 (Лицензии) as COMPLETED
- [ ] Prepare for Stage 2 (Архитектура) — typed provider interfaces, ADR-0009 (License and Compliance)

**Still pending from Sprint 26:**
- Audible intelligibility check by user (not part of MVP)
- Word-level subtitle alignment (not in MVP scope)
- Vertical 1080x1920 validated (already done: 1080×1920 render produced and OK)
- `pytest -q` local run verification (already passed in CI with ASCII basetemp)

**Next session:** Continue license audit documentation, then move to architecture contracts and ADR-0009.

---

# Next session — Sprint 26 first-video pipeline (2026-11-03)

Windows Sprint 25.1 Silero Ukrainian preview verified by user: Preview ready, WAV 2.2 s, synthesis 11.2 s, RTF 5.17, playback reported working.

Current work: `scripts/first_video.py` builds an offline narrated MP4 from a RU/UA JSON scene plan with local Silero or existing WAVs, optional local images, generated gradient fallbacks, scene subtitles and existing FFmpeg renderer. See `docs/SPRINT26_FIRST_VIDEO_WINDOWS.md`.

**Next user validation gate:** On Windows run `scripts/first_video.py --plan examples/first_video_plan_uk.json --silero-model C:\StoryStudioModels\v5_cis_base_nostress.pt --voice ukr_igor --output-dir output/first-video-uk`, then inspect `output/first-video-uk/first-video.mp4` for spoken audio, subtitles, picture and timing. Output directory must not exist already.

No full Chinese original code was executed or included in the pipeline; upstream rights and provider terms remain gated. CI and local synthetic tests must be checked before claiming verified status.

# Next session — after Sprint 25.1 (2026-11-03)

Repository: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK

- Complete upstream Chinese original is pinned as a Git submodule at `upstream/konlu-full`; engineering files also preserved in `upstream/konlu-story-studio/`. Do not overwrite the RU/UA implementation from upstream.
- Our RU/UA Sprint 25 code baseline has been imported to GitHub. Sprint 25.1 fixes Voice Studio's Unicode console-path preview failure by determining the expected output path before synthesis; adds UTF-8 subprocess environment and synthesis metrics in the UI.
- Next on Windows: install `Sprint_25_1.zip` OVER the current local project, keeping `.venv`, models and other local assets; run `python -m unittest discover -s tests -v`; start Voice Studio via `scripts/run_voice_studio.ps1`; generate Ukrainian Silero preview and confirm `Preview ready`, audio playback and time metrics. Test Edge TTS too if internet access permits.
- Do not upload, distribute, or commercialize Chinese corpora/media and current upstream CC BY-NC-SA 4.0 source without legal review. Historical local MIT license provenance differs from current upstream license.
- Tests run on Linux Python 3.13: 106 passed, 0 failed. Windows GUI + actual Silero model were NOT tested in the CI/container environment. Save Windows test outcome in next worklog entry.


## Sprint 17 follow-up
Проверить мужской ru-RU-DmitryNeural после установки патча. Далее: каталог голосов, preview, надёжная синхронизация.