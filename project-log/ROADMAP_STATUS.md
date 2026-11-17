# Актуальный срез дорожной карты — 2026-11-04

**Текущая рабочая версия — Sprint 26; проект на паузе.** Этот раздел приоритетнее устаревшей ниже таблицы, начинающейся со Sprint 04. Исторические заметки ниже сохранены для аудита, не следует трактовать их как актуальные ворота реализации.

| Направление | Статус | Следующая проверка |
|---|---|---|
| Windows базовая сборка | Sprint 26 MVP в `main`; Silero Voice Studio Sprint 25.1 проверен пользователем | Подтвердить полный Windows end-to-end MP4 Sprint 26 отдельным тестом |
| CPU Lip Sync | Только открытый экспериментальный PR #5, **не merged**, внешние веса/зависимости не поставляются | Лицензия, Windows CPU окружение, реальная скорость и качество после отдельного согласования |
| Поиск интернет-историй | В RU/UA ещё не реализован | Read-only анализ оригинала и оригинальный интерфейс StoryCandidate |
| Оценка и Writing-DNA RU/UA | Методология китайского исходника исследована, собственная независимая реализация ещё не готова | Evidence ledger, ranking rubric, original prompts, evaluation tests |
| Лицензии | CC BY-NC-SA pinned upstream; китайские материалы/внешние модели коммерчески не одобрены | Подробный provenance review, SBOM, право на модели и корпуса |
| Переход к Codex | `AGENTS.md`, handoff, аудит и инструкция в документационной ветке | Review/merge документационного PR, затем read-only задание Codex |
| Релиз и установка | Один основной Windows-проект, инкрементальные ZIP-накладки | Никаких новых папок и ложных ссылок на несуществующие архивы |

---

## Историческая дорожная карта (хронология)

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

- CI setup correction: a historical `tests/test_sprint20.py` imports `pytest`, so GitHub Actions installs pytest explicitly and runs the full pytest suite. Local project tests (`python -m pytest -q tests`): 119 passed, 15 subtests passed (Linux Python 3.13); remote CI result pending.

- GitHub Actions follow-up: full-repository pytest collection also found intentionally isolated upstream tests. Added `pytest.ini` and restrict CI test discovery to our `tests/` directory; upstream tests require their own separate dependency and legal audit.


## Sprint 26 — first-video MVP (2026-11-03)
- Implemented scene-plan -> offline WAV/Silero -> still images -> v3 timeline -> FFmpeg MP4 with burned subtitles.
- Includes RU and UK sample scene plans and CLI options for local pictures or existing WAVs.
- **Gate pending:** CI checks and actual Windows end-to-end MP4 playback; scene-level timing only.
- Next after Windows confirmation: improve storyboard/images and narration synchronization using legally cleared ideas and adapters from original upstream.
