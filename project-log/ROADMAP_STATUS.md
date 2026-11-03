# ROADMAP STATUS — updated Sprint 04 (2026-10-30)

| Этап | Статус | Критерий | Блокер |
|---|---|---|---|
| 0. Baseline | IN PROGRESS | Архив, inventory, Git, тесты | Git на машине пользователя не проверен; SBOM отсутствует |
| 1. Лицензии | IN PROGRESS | Реестры, SBOM, решения | Корпуса/медиа/транзитивные зависимости |
| 2. Архитектура | IN PROGRESS | Контракты и ADR | Timeline v2/SRT готовы частично; нет typed clip model/providers; есть media manifest prototype |
| 3. RU/UA сценарии | IN PROGRESS | Оригинальные проверенные примеры | Только locale scaffolding, без библиотеки |
| 4. Провайдеры | NOT STARTED | Тестируемые адаптеры | Условия API/весов |
| 5. Визуальная система | NOT STARTED | Очищенные референсы | Права на медиа |
| 6. Экспорт | IN PROGRESS | Реальные проекты Kdenlive/DaVinci | Есть SRT + media manifest prototype, нет редакторского импорта; есть экспериментальный MP4 FFmpeg на Linux |
| 7. Windows | NOT STARTED | Чистая установка Win10/11 | CLI и 53 теста пройдены пользователем на Windows; Sprint10 MP4 ещё не проверен |
| 8. Community 1.0 | NOT STARTED | QA + compliance gate | Аудит |
| 9. Professional | NOT STARTED | Права, оплата, спрос | Проверка спроса |
| 10. Cloud | NOT STARTED | Экономика, безопасность, право | Будущее |

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

- CI setup correction: a historical `tests/test_sprint20.py` imports `pytest`, so GitHub Actions installs pytest explicitly and runs the full pytest suite. Local result: 176 passed, 2 skipped, 22 subtests passed (Linux Python 3.13); remote CI result pending.
