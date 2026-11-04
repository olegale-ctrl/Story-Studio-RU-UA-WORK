# DECISIONS

## ADR-0001 — Windows-first, RU/UA, Community + Professional
Дата: 2026-10-30
Статус: принято пользователем
Решение: Windows 10/11 первая платформа, macOS/Linux позже; русский и украинский; Community open-source, Professional отдельно, Cloud после проверки спроса.
Последствия: изоляция платформенных и платных модулей.

## ADR-0002 — Нейтральная монтажная модель
Дата: 2026-10-30
Статус: проектное предложение, требует технического подтверждения
Решение: единая JSON timeline; Kdenlive/DaVinci приоритет; CapCut только после feasibility.

## ADR-0005 — Schema v3: typed media and clips
Дата: 2026-10-30
Статус: принято для прототипа
Решение: медиа как MediaAsset, клипы как Clip, обязательные связи с дорожками и типами, переносимые пути. Старые v1/v2 загружаются с миграцией в памяти.
Ограничения: реальный импорт в видеоредакторы и проверка длительности исходного файла ещё не реализованы.

## ADR-0006 — Portable bundle as intermediate format
Дата: 2026-10-30
Статус: prototype implemented
Решение: dry-run manifest by default; optional explicit media copy and SRT export; no claims of native editor support.

## ADR-0007 — Non-blocking overlaps and portable bundle checksums
Date: 2026-10-30. Decision: report same-track overlap as warning, attach SHA-256 integrity manifest to materialized bundles; media source duration remains unverified.

## Sprint 14
- Use installed Windows SAPI voice for the first offline narration smoke test, not a bundled third-party model. Require matching ru/uk voice; fail clearly otherwise.
- Generate project/media locally and preserve existing v3 schema and renderer.

## Sprint 15
- Refuse voice locale mismatch instead of generating incorrect-language speech.
- Keep Windows SAPI demo local and optional; no redistribution of TTS voices.

## Sprint 16
- Offer Polina/Ostap and Svetlana/Dmitry as initial RU/UA Edge voice choices. Never substitute across languages.
- Edge Read Aloud through edge-tts is a prototype provider, not an approved commercial publishing path.

## Sprint 17
Кэш TTS должен учитывать голос и текст; разные голоса не разделяют медиа. MP4 никогда не перезаписывается автоматически.

## ADR-2026-11-03 — Preserve original upstream as pinned Git submodule
- Decision: RU/UA code remains primary working tree. Complete Chinese original is pinned as an isolated Git submodule; 40 original technical files are also kept in an isolated reference directory.
- Rationale: preserve proven video production workflow and all original materials without overwriting RU/UA adaptations or bloating ZIP releases.
- Legal gate: CC BY-NC-SA 4.0 on current upstream; historical MIT copy is not adequate evidence to green-light commercialization.
- Sprint releases remain incremental ZIPs; each release's exact files are committed to GitHub.



## ADR-2026-11-04 — Codex onboarding: read-only audit before new development
Дата: 2026-11-04. Статус: согласовано направление аудита и подготовка документов; реализация новых функций **не санкционирована**.
Решение: один приватный GitHub-репозиторий, Sprint 26 в `main`, Sprint 25.1 локально как резерв. Новый `AGENTS.md` указывает Codex на короткий handoff и конкретные источники; первый Codex этап перепроверяет претензии к китайскому поиску историй, factual evidence и редакционной драматургии без изменений кода.
Причины: пользователь считает поиск и сценарную систему наиболее ценными; текущие инструменты локального corpus search не равны автономному интернет-агрегатору, а редакционные hooks не являются доказанным retention predictor.
Последствия: новые оригинальные RU/UA Discovery, Evidence и Narrative DNA требуют отдельной проектной приёмки; старый lip-sync PR #5 остаётся экспериментальным; никакой новый ZIP или новая рабочая папка на этом шаге не нужны.


## ADR-2026-11-04 — Intelligent AI provider discovery and free-tier manager
Дата: 2026-11-04. Статус: **продуктовое направление согласовано пользователем; реализация не санкционирована**.
Решение: Story Studio RU/UA должен поддерживать не только реестр существующих бесплатных и условно-бесплатных AI-сервисов, но и **поиск новых сервисов, независимую оценку пригодности, проверку официального происхождения, API/ручного доступа, бесплатных квот, лицензий и коммерческих прав, отслеживание изменений условий и обоснованный выбор провайдера** для изображений и коротких видео. В будущем архитектура расширяется на TTS/ASR.
Ограничения: без обхода лимитов, CAPTCHA и ToS, без массовой регистрации аккаунтов; без платных запросов и включения новых провайдеров без одобрения пользователя; web-only бесплатные квоты не приравниваются к API; при недоступности облака используется FFmpeg + изображения.
Последствия: отдельный исследовательский поток после текущего аудита Codex; Sprint 26 и экспериментальный PR #5 не менять. Спецификация: `docs/AI_PROVIDER_DISCOVERY_AND_ORCHESTRATION_SPEC.md`.
