# ROADMAP STATUS — updated 2026-11-17 (Sprint 28 Stage 2 Architecture)

| Этап | Статус | Критерий | Блокер |
|---|---|---|---|
| 0. Baseline | IN PROGRESS | Архив, inventory, Git, тесты | Git на машине пользователя не проверен; тесты и inventory есть |
| 1. Лицензии | **COMPLETED (Stage 1)** | Реестры, SBOM, решения | Реестры заполнены; SBOM добавлен в Sprint 28 (SBOM.cdx.json + drift-gate) |
| 2. Архитектура | **COMPLETED (Stage 2)** | Контракты и ADR | Typed VoiceProvider-контракт + ADR-0009 + SBOM реализованы; контракт image-провайдера отложен до реального этапа 5 |
| 3. RU/UA сценарии | IN PROGRESS | Оригинальные проверенные примеры | Только locale scaffolding, без библиотеки |
| 4. Провайдеры | IN PROGRESS | Тестируемые адаптеры | Silero local проверен на Windows; Edge TTS — только экспериментально, коммерческие права не подтверждены; **unified VoiceProvider-контракт добавлен в Sprint 28** (core/providers.py, ADR-0009) |
| 5. Визуальная система | NOT STARTED | Очищенные референсы | Права на медиа |
| 6. Экспорт | IN PROGRESS | Реальные проекты Kdenlive/DaVinci | Локальный MP4-маршрут проверен на Windows; нативный импорт редакторов не реализован |
| 7. Windows | IN PROGRESS | Чистая установка Win10/11 | CLI и 346 тестов проходят на Windows; чистая установка на Win10/11 не проверялась |
| 8. Community 1.0 | NOT STARTED | QA + compliance gate | Аудит |
| 9. Professional | NOT STARTED | Права, оплата, спрос | Проверка спроса |
| 10. Cloud | NOT STARTED | Экономика, безопасность, право | Будущее |

## 2026-11-17 — Sprint 28 Stage 2 Architecture COMPLETED
- **Typed provider contract** (`core/providers.py`): `VoiceProvider` Protocol,
  `ensure_voice_provider()`, `PreRecordedAudioProvider`, registry `SPECS` with
  license metadata per provider, `require_commercial_use()` gate.
- **`first_video.py` unified**: both narration routes (user WAV files, Silero)
  now go through the same contract; behavior unchanged (374 pytest + 19
  subtests, unittest 368 OK in `.venv`).
- **SBOM**: `scripts/generate_sbom.py` generates deterministic CycloneDX 1.5
  `LICENSES/SBOM.cdx.json` from the Stage 1 CSVs; `--check` byte-compares so CI
  fails on drift between registers and SBOM.
- **ADR-0009** (License and Compliance) written and recorded in DECISIONS.md.
- **Next**: Stage 3 (RU/UA сценарии) — original verified example library; keep
  Stage 4 provider adapters aligned with the new contract.

## 2026-11-16 — Sprint 27 License Audit (этап 1) COMPLETED
- **DEPENDENCY_LICENSES.csv**: 25 runtime Python packages catalogued (all permissive: MIT/BSD/Apache/PSF/HPND). No GPL in Python deps.
- **ASSET_REGISTER.csv**: Local project assets documented (`assets/sponsor/*.png` — user QR codes, USER CLEARANCE REQUIRED). Upstream media remains BLOCKED/REPLACE.
- **AI_MODELS_AND_SERVICES.csv**: Silero (CC BY-NC-SA 4.0, non-commercial, local), Edge TTS (COMMERCIAL BLOCKED), PyTorch (BSD-3, APPROVED).
- **THIRD_PARTY_NOTICES.md**: Formal notices written for all components.
- **Silero SHA256 verified in code** (integrations/silero_local.py); ASCII-path enforcement on Windows; `trusted=True` mandatory.
- **BLOCKED items documented**: Silero weights (need commercial license), edge-tts output (no commercial grant), upstream CC BY-NC-SA (needs provenance/replacement).
- **Next**: Stage 2 (Architecture) — typed provider interfaces, ADR-0009 (License and Compliance), SBOM generation.

## Sprint 08 note
- Timeline diagnostics and SHA-256 bundle integrity implemented; neither native editor export nor Windows validation completed.

Sprint 09: CLI check/preview/bundle/verify implemented; Windows runtime validation remains NOT TESTED.


Sprint 11: Windows user confirmed Sprint10 playback; local FFmpeg auto-detection and optional caption burn-in implemented, Windows burn-in not yet verified.

## Sprint 12
- Implemented: controlled subtitle styling; multiple audio timeline clips with trimming, offset and mixing.
- Windows smoke test pending; original upstream and editor interoperability still not validated.

## Sprint 14 status
- Implemented: original gradient demo frames, Windows SAPI voice-generation workflow, timed 3-scene narrated project, regression tests.
- Pending: Windows voice availability and spoken video verification; quality review and user choice of TTS providers.

## Sprint 15
- Narrated video orchestration and preflight implemented; Windows user validation pending.
- Real-world TTS provider integration and editor export still open.

## Sprint 16
- Experimental Edge TTS four-voice RU/UA demo pipeline added; Windows validation pending.
- Provider abstraction, GUI, local/offline models and commercial license gate remain open.

## Sprint 17
Реализованы изоляция голосов и версионирование MP4; Windows интеграционный тест ожидается.

## 2026-11-03 — Sprint 25.1
- **Source repository baseline:** imported current RU/UA Sprint 25 source (148 text files) to GitHub, plus full upstream as pinned Git submodule. Upstream engineering snapshot isolated.
- **Audio GUI:** Unicode-safe preview path discovery and synthesis timing implemented, tests green; Windows physical model test outstanding.
- **QA:** 106/106 unit tests successful in Linux Python 3.13 after generating portable temporary test media; no declaration of Windows CI success.
- **License gate:** current upstream CC BY-NC-SA 4.0 vs archived MIT; cannot approve commercial rights until per-component provenance is verified.


- **CI workflow:** Ubuntu Python 3.10/3.13 test matrix configured; no claim of successful GitHub Actions run until checked.

- CI setup correction: a historical `tests/test_sprint20.py` imports `pytest`, so GitHub Actions installs pytest explicitly and runs the full pytest suite. Local project tests (`python -m pytest -q tests`): 119 passed, 15 subtests passed (Linux Python 3.13); remote CI result pending.

- GitHub Actions follow-up: full-repository pytest collection also found intentionally isolated upstream tests. Added `pytest.ini` and restrict CI test discovery to our `tests/` directory; upstream tests require their own separate dependency and legal audit.


## Sprint 26 — first-video MVP (2026-11-03)
- Implemented scene-plan -> offline WAV/Silero -> still images -> v3 timeline -> FFmpeg MP4 with burned subtitles.
- Includes RU and UK sample scene plans and CLI options for local pictures or existing WAVs.
- **Gate pending:** CI checks and actual Windows end-to-end MP4 playback; scene-level timing only.
- Next after Windows confirmation: improve storyboard/images and narration synchronization using legally cleared ideas and adapters from original upstream.

## 2026-11-16 — Sprint 26 Windows validation PASSED
- Full first-video pipeline executed on Windows with local Silero for both
  locales, plus a user-media (`--audio-dir` + `--images-dir`) run. Output MP4s
  verified with `ffprobe` (h264 1280x720 @25 fps, AAC 48 kHz stereo),
  `volumedetect` (speech present) and frame sampling (subtitle timing exact).
- Test suite: 116 tests OK in `.venv` (Python 3.10.11) and system Python 3.15.
  Two pre-existing test defects fixed (pytest-only import, platform-dependent
  path assertion).
- Pipeline defect fixed: a failed run no longer leaves a partial output tree.
- **Still pending:** audible intelligibility check by the user, vertical
  1080x1920 run, word-level subtitle alignment, `pytest -q` local run.
- Roadmap stage 6 (export) moves from prototype to a verified Windows path for
  the local-MP4 route; native editor import (Kdenlive/DaVinci) remains open.

## 2026-11-16 — Test suite expansion (116 → 346 tests)
- Automated suite extended from 116 to **346 tests** (349 under pytest, plus 19
  subtests); all pass on Windows in `.venv` (Python 3.10.11) and in system
  Python 3.15.
- Coverage: `core/` modules now sit at 91–100 %; `first_video.py` 96 %,
  `voice_settings.py` 97 %, `hardware_profile.py` 98 %, `studio_runtime.py` 87 %.
- **Fix:** `Project.to_dict()` returned tuples while `from_dict()` requires
  lists, so `from_dict(to_dict())` failed. Now symmetric.
- **CI:** added a `windows-2022` job so Windows-specific path, encoding and
  subprocess behaviour is checked on every push.
- Stage 7 (Windows) blocker list is now: clean Win10/11 install not yet
  exercised, vertical 1080x1920 path not validated, GUI not covered by CI.
