# WORKLOG

## 2026-10-30 — Session 1: planning and initial archive inventory

### Выполнено
- Подготовлен мастер-промпт, roadmap и шаблоны журналов.
- Подтверждён исходный архив: 576 файлов (не считая каталогов), SHA256 `a4a9354270a3da072a155b0e5fbdb84f58bec1617b150ccfedc0f156177b24c6`.
- Прочитан корневой LICENSE: MIT, Copyright (c) 2026 konlu.
- Выполнен предварительный список вложенных файлов и медиа.

### Проверки
- ZIP открыт и прочитан; запуск программных тестов НЕ выполнялся в этой сессии.

### Ограничения
- Лицензии сторонних материалов НЕ подтверждены.
- Ни один кодовый файл оригинала не изменён.

### Следующий шаг
1. Распаковать копию и создать Git baseline.
2. Проанализировать manifests, install scripts и download URLs.
3. Заполнить реестры по каждому активу и зависимости.


## 2026-10-30 — Sprint 01 (текущая сессия)
- Сформирована единая рабочая копия из исходного ZIP и пакета планирования.
- Добавлены docs/PROJECT_STRUCTURE.md и docs/ORIGIN_AND_ATTRIBUTION.md.
- Сформированы audits/DEPENDENCY_REFERENCES.csv и audits/ASSET_TRIAGE.csv.
- Выполнены baseline unittest-команды, результат в audits/TEST_BASELINE.txt.
- Исходный программный код не изменён.
- Лицензии сторонних материалов не подтверждены, публичный релиз заблокирован.
- Следующий шаг: ручной аудит зависимостей и источников корпусов, затем архитектура провайдеров.

## 2026-10-30 — Sprint 02: архитектурное решение и статический аудит
- Прочитан NEXT_SESSION Sprint 01 и код `scripts/setup_dependencies.py`.
- Подготовлен ADR-0001 (PROPOSED), без изменения оригинального кода.
- Выделены явно объявленные версии/диапазоны pyJianYingDraft, Pillow, numpy, websockets, Coli; отмечены pymediainfo/libmediainfo, ffmpeg/ffprobe.
- Создан предварительный реестр проверки лицензий; все сторонние компоненты пока REVIEW REQUIRED.
- Интернет-проверка лицензий, SBOM, Windows-тесты и тесты редакторов в этой сессии НЕ выполнялись.
- Следующий шаг: проверка загрузок и первичных лицензий, затем модель монтажного проекта.

## 2026-10-30 — Sprint 03: master prompt v1.1 and initial core
- Replaced master prompt with v1.1 (fork/rework, REPLACE/BLOCKED Chinese content, local-first providers, separate locales, CapCut feasibility, transitive dependencies).
- Added ADR-0002, initial `core/project_schema.py`, 7 unit tests, original RU/UA prompt templates and UI strings.
- No original modules or scripts changed.
- No paid APIs, Windows tests, editor imports, license approvals or releases performed.
- Run: `python -m unittest discover -s tests -v` from project root.
- Remaining: dependency license verification, SBOM, real export adapters, robust schema expansion.

## 2026-10-30 — Sprint 04: editor-neutral timeline v2 + SRT
- Read `MASTER_PROMPT.md` v1.1 and `NEXT_SESSION.md` from Sprint 03; no Git checkout was available in the isolated update workspace (Git state on user's machine unknown).
- Changed: `core/project_schema.py` (v2 tracks/subtitles + strict validation + v1 in-memory migration); `tests/test_project_schema.py` (14 new cases).
- Added: `core/subtitles.py`, `tests/test_subtitles.py` (3 cases), `docs/ADR-0003-TIMELINE-V2.md`, `audits/SPRINT04_TEST_RESULTS.txt`, installer.
- Tests: 24/24 passed, Python 3.13 Linux. Command `PYTHONPATH=<Sprint04Root> python -m unittest discover -s <Sprint04Root>/tests -q`. No Windows, editor, full-repository or integration tests.
- License: new Python code uses only stdlib; no license approvals issued. Upstream binaries, Python/npm transitive deps, Chinese corpora and third-party media remain release-blocked pending evidence.
- No original scripts/modules changed. No network, API calls, publication or payments.
- Next: clip references, JSON Schema/fixtures, static dependency inventory with provenance; Windows smoke test by user when ready.

## 2026-10-30 — Sprint 05: unified log and media manifest prototype
- Merged user-provided Sprint 02, 03 and 04 append entries into the full WORKLOG.md, preserving the original entries and order. No manual append is required.
- Added `core/media_manifest.py` with portable relative-path validation and deterministic media manifest output; original v2 schema unchanged.
- Added 5 unit tests and ADR-0004. No third-party runtime dependencies introduced.
- Combined isolated test suite: see `audits/SPRINT05_TEST_RESULTS.txt` (Linux). No Windows or editor import test performed.
- No license approvals; original Chinese content and unverified downloaded models remain blocked from release.
- Next: typed clip model/schema migration, Windows smoke tests, direct/transitive dependency inventory.

## 2026-10-30 — Sprint 06: typed clips and schema v3
- Received user Sprint05 ZIP and reconstructed core using verified Sprint03–05 update packages.
- Added MediaAsset and Clip to project v3, track/media kind checks, unique IDs, source offsets, portable media paths.
- Added strict in-memory v1/v2 to v3 migration; original JSON files are not modified.
- Added draft JSON Schema (structural checks only; semantic cross-references require Python validation).
- Refactored portable path validator into core/media_paths.py.
- Tests: 37/37 isolated Python unit tests passed on Linux; no Windows/editor integration tests.
- No third-party dependencies introduced, no new license approvals.
- Deliverable contains complete replacement logs; no manual append.

## 2026-10-30 — Sprint 07: portable export bundle prototype
- Implemented `core/export_bundle.py`: deterministic v3 media/clip/SRT manifest, timeline duration, dry-run by default, optional preflighted file copy.
- Added 6 isolated tests and ADR-0006. Existing destination rejected, path containment enforced, missing source preflighted.
- Tests: 40 isolated unittest cases passed on Linux. No Windows, real video editor import or original upstream end-to-end validation.
- No new third-party packages. No new license approvals; Chinese corpora/media remain blocked.
- Full replacement project logs included; no manual append.

## 2026-10-30 — Sprint 08: integrity and timeline diagnostics
- Added `core/timeline_audit.py` for non-blocking overlap and unverified source-offset diagnostics.
- Added `core/bundle_integrity.py` and SHA-256 `integrity.json` generation in `core/export_bundle.py`.
- Added v1/v2/v3 migration fixtures and five tests.
- Tests: all isolated tests passed on Linux; see `audits/SPRINT08_TEST_RESULTS.txt`. No Windows/editor integration tests.
- No third-party dependencies or license approvals added. Chinese corpora/media remain release-blocked.

## 2026-10-30 — Sprint 09: Windows-friendly CLI
- Added `core/cli.py`: check, preview, bundle and verify with exit codes, Unicode and safe error handling.
- Added `tests/test_cli.py`, Windows PowerShell usage in `docs/CLI_WINDOWS.md`, ADR-0008.
- Ran isolated unittest suite on Linux; result in `audits/SPRINT09_TEST_RESULTS.txt`.
- No Windows or editor integration performed; no native editor format supported yet.
- No new third-party dependencies or license approvals. JSON Schema semantic parity remains open.

## 2026-10-30 — Sprint 10: первый MP4-прототип
- Получено от пользователя подтверждение Windows: `python -m core.cli check tests/fixtures/project_v3.json` → OK; `python -m unittest discover -s tests -v` → 53 tests, OK (0.248 s). Это пользовательская проверка Sprint09, а не запуск Sprint10 на Windows.
- Добавлены `core/mp4_render.py`, CLI `render-mp4`, тесты и самостоятельный demo (3 PPM, WAV, RU/UA JSON, SRT).
- Реально собран 3-секундный MP4 и SRT в Linux через установленный FFmpeg; тесты Sprint10 прошли (54/54). Не подтверждено на Windows до запуска пользователем.
- Поддержка ограничена последовательными image-клипами, 0–1 аудиоклипом, H.264/AAC и отдельными SRT; нет burn-in и native editor export.
- FFmpeg не включён в пакет. Лицензионные разрешения на распространение сторонних бинарников и моделей не выдавались.
- Следующий шаг: Windows render smoke test, улучшение обработки аудио и ошибок, schema parity, затем переходы и MP4 subtitle burn-in.


## 2026-10-30 — Sprint 11: Windows FFmpeg and optional burned captions
- User confirmed Sprint 10 on Windows: three colored frames changed and synthetic audio tone played; command returned OK with 3000 ms, three clips, separate SRT.
- Added local FFmpeg auto-discovery, optional subtitle burn-in (`--burn-subtitles`), H.264 CRF setting, and Windows instructions.
- No FFmpeg binary distributed. GPL-enabled build licensing remains a release gate.
- Test results and Windows burn-in validation: pending; see next session for exact state.

## 2026-10-30 — Sprint 12: subtitle styling and audio timeline
- Windows user verified Sprint11 burn-in: subtitles appear in MP4; player overlay filename disappears after pause. Screenshot revealed oversized shadow/double-edge effect, not motion.
- Set FFmpeg/libass subtitle force_style to white text, thin black outline, Shadow=0, centered bottom with margin.
- Added up to 32 timed audio clips with source offsets, trim, delay and mix; out-of-bounds audio rejected.
- FFmpeg remains user-installed only; no third-party binary redistributed.
- Linux test results in docs/SPRINT12_TEST_RESULTS.txt. Windows Sprint12 verification pending.

## 2026-10-30 — Sprint 14: narrated RU/UA video demo
- User confirmed Sprint13 Windows: 1920x1080 and clear burned captions, with no redundant SRT.
- Added Windows SAPI voice synthesis script with exact locale matching, generated original PPM scene backgrounds, WAV duration-aligned timeline and three separate spoken clips.
- This is a local TTS demonstration, not AI voice integration; Windows speech voice availability is a prerequisite. No Windows test yet.
- FFmpeg binary not included; licensing and voice rights remain subject to review.

## 2026-10-30 — Sprint 15: one-command narrated video workflow
- Added SAPI voice listing and locale preflight, integrated generation/inspection/schema check/1920x1080 render PowerShell runner.
- Added independent WAV/timeline consistency inspection and two unit tests.
- No new third-party libraries, voices or FFmpeg binaries distributed. Windows voice availability and output still need user validation.

## 2026-10-30 — Sprint 16: Edge TTS four-voice RU/UA prototype
- User confirmed Polina Ukrainian neural voice successfully produced and played via Edge TTS 7.3.1 on Windows. SAPI had only en-US Zira.
- Added optional online Edge TTS integration with two voices per language, MP3-to-WAV conversion via locally installed FFmpeg, reuse of existing narrated project generator and validator, one-command MP4 export.
- Added strict voice locale guard, no commercial use assertion, no bundled third-party binaries, five unit tests.
- Windows end-to-end narrated MP4 with Edge TTS is not yet user verified.


## Sprint 16 hotfix — 2026-11-02
- Edge TTS: retry up to three times, reject zero-byte/corrupt MP3 using ffprobe, delete bad files, reuse valid cached MP3.
- Confirmed user-side Polina 21456 bytes and Svetlana 20736 bytes; Dmitry failed with zero-byte file.
- End-to-end Windows rendering remains to be verified.

## 2026-11-02 — Sprint 17
- Исправлен дефект смешивания голосов в кэше: SHA-256 по провайдеру, голосу, тексту и параметрам.
- Проекты и аудиофайлы разделены по голосам, старые неразмеченные MP3 не переиспользуются.
- Выходные MP4 имеют уникальные имена и версии без перезаписи.
- Добавлены пять регрессионных тестов.
- Полный Windows/Edge TTS рендер требует проверки пользователем.

## 2026-11-03 — Sprint 25.1: GitHub baseline + Unicode-safe Voice Studio preview
- Imported 148 text source/test/docs files from the user-provided Sprint 25 snapshot into the private GitHub repository; no generated audio/video, model weights or `.venv`.
- Full upstream Story Studio revision `87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1` pinned as a Git submodule; 40 upstream engineering files preserved separately with their original CC BY-NC-SA license.
- Fixed Voice Studio: Python child process uses UTF-8 I/O; output files are located deterministically instead of trusting mojibake-prone `PREVIEW:` output. Added check for fresh Silero WAV and displayed synthesis timing/RTF.
- Tests generate their own small temporary demo images/audio; obsolete Sprint 23.1 tests replaced with current Sprint 23.2 model path/trust checks.
- Validated Python syntax; `python -m unittest discover -s tests -v`: 106 tests OK, 0 failures, Linux Python 3.13. Windows GUI and actual Silero model still await local confirmation.
- Modified: `scripts/voice_studio.py`, `tests/test_sprint25_1.py`, `tests/demo_media_support.py`, `tests/test_sprint11.py`, `tests/test_sprint12.py`, `tests/test_sprint13.py`, `tests/test_sprint23_1.py`, 5 project-log files, `SPRINT_25_1_REPORT.md`, `INSTALL_S25_1.txt`, root `README.md`, `.gitignore`, and `.github/workflows/tests.yml`.
- Blockers: licensing provenance (historical MIT snapshot vs current CC BY-NC-SA upstream), Windows end-to-end test, commercial provider rights.
- Next: run Windows QA, incorporate feedback, then continue Sprint 26 with original video's reusable adapters, while preserving source attribution and licensing gate.


- CI setup correction: a historical `tests/test_sprint20.py` imports `pytest`, so GitHub Actions installs pytest explicitly and runs the full pytest suite. Local project tests (`python -m pytest -q tests`): 119 passed, 15 subtests passed (Linux Python 3.13); remote CI result pending.

- GitHub Actions follow-up: full-repository pytest collection also found intentionally isolated upstream tests. Added `pytest.ini` and restrict CI test discovery to our `tests/` directory; upstream tests require their own separate dependency and legal audit.


## 2026-11-03 — Sprint 26 first-video implementation
- User confirmed Windows Sprint 25.1 Silero ukr_igor preview and playback; screenshot shows Preview ready, 11.2 s synthesis, 2.2 s WAV, RTF 5.17.
- Added `scripts/first_video.py`: a single command for offline local Silero or existing WAVs, per-scene local pictures or generated original gradients, editor-neutral v3 project, scene-level subtitles and FFmpeg MP4 burn-in.
- Added RU/UA sample plans, five regression tests and Windows validation instructions. No Chinese corpora or additional upstream code loaded.
- Validation: GitHub Actions CI pending at time of authoring; actual Windows MP4 not tested yet. User validation required before further video quality work.
- Files: `scripts/first_video.py`, `examples/first_video_plan_ru.json`, `examples/first_video_plan_uk.json`, `tests/test_sprint26.py`, `docs/SPRINT26_FIRST_VIDEO_WINDOWS.md`, four project logs.
- Next: verify CI; user runs real Silero end-to-end on Windows and checks exported video.


## 2026-11-04 — Codex onboarding and Chinese upstream audit handoff (documentation only)
- Пользователь согласовал переход подготовки документации к Codex и приоритет глубокого исследования Discovery / Editorial Ranking / Narrative DNA. **Код и локальные установленные версии на паузе**; это не Sprint 27.
- Подготовлены `AGENTS.md`, `project-log/CODEX_HANDOFF.md`, `docs/CODEX_ONBOARDING.md`, `docs/UPSTREAM_DEEP_AUDIT_2026-11-04.md`; обновлён `MASTER_PROMPT.md` до v1.2 и ссылки/статусы в журналах.
- Исходные данные аудита: pinned китайский commit `87c2bbf...`; локальный поиск в `history_tool.py`, 57 исторических записей, 296 новых биографических файлов, описательные Writing-DNA/hook rules; отдельно перечислены инженерные сильные стороны и не воспроизведённые риски. Источники и оговорки включены в отчёт.
- Лицензия: оригинал pinned CC BY-NC-SA 4.0; старый MIT-архив исторический, права на внешние корпуса и лицензии моделей/зависимостей не закрыты. Никаких APPROVED выдано.
- Тесты: **не запускались** для документационных изменений; GitHub link/content review после записи. Реальный Windows end-to-end, TTS платные API, Wav2Lip CPU inference и внешний Jianying export не запускались.
- GitHub: отдельная ветка `docs/codex-handoff-audit-20261104`; приёмка через PR, без merge в `main`. Не готовить новых ZIP-накладок, пока пользователь не попросит.
- Следующий шаг: пользователь проверяет документационный PR; после его принятия передать Codex read-only запрос из `docs/CODEX_ONBOARDING.md`. При новых находках обновлять audit с file/line и tests, но не менять runtime без отдельной задачи.
