# Story Production RU/UA — план внедрения идей WanGP

**Дата:** 2026-11-06. **Статус:** концепция одобрена, implementation tasks пока не утверждены. Источник решений WP-01–WP-16: [STORY_PRODUCTION_WANGP_ADOPTION_DECISION_2026-11-06.md](../architecture/STORY_PRODUCTION_WANGP_ADOPTION_DECISION_2026-11-06.md).

## 1. Независимость от текущего storage-трека

S2.1–S2.4 — pure protocol/recovery model. S3.1 — Windows design-only PROPOSAL, Q1/Windows profiles и S3.2 не утверждены. Не менять E00, A1–A14, O1–O10, D1–D12, S1, golden vectors. Story Intelligence → Production Brief ещё не реализован; Shot Production должен использовать его версионированный handoff, а не подменять редакционные решения. Черновики/медиа отдельно от protected editorial storage.

## 2. Будущие отдельные задачи (не запускать автоматически)

| ID | Этап | Артефакт | Gate |
|---|---|---|---|
| SP-00 | Contracts, docs-only | Brief handoff, Shot/Take types/state, invalidation graph, review/lock, provider/job API, storage/rights boundaries | Owner approval |
| SP-01 | CPU storyboard slice | ≥3 сцены RU/UK, ручной план, takes, preview, FFmpeg export | Real Windows CPU smoke |
| SP-02 | Selective rebuild | hashes, stale graph, regenerate only affected assets | Mutation matrix |
| SP-03 | Preflight & provider registry | CPU adapters, dry-run, capability discovery, rights checks | Offline/no-GPU tests |
| SP-04 | Queue & recovery | idempotent request_id, receipts, cancel, unknown-after-restart | Lost ACK/crash matrix |
| SP-05 | Technical QA | FAULT/CHECK/EDITORIAL_REVIEW, timecoded evidence, fix/retest | Deterministic fixtures |
| SP-06 | Cast/Place/Voice Bible | Versioned references, impacted-shot report | Consent/voice/license gate |
| SP-07 | Timeline & Deliver | compare/restore, exact text, audio/SRT/burn-in, versioned manifest | Non-destructive exports |
| SP-08 | Media Flow & Workspaces | bounded chunks, overlap, resume, galleries, backup/restore | Interrupted batch |
| SP-09 | Windows Manager | pinned runtime, offline CPU install, rollback | Windows qualification |
| SP-10 | Optional API/MCP | localhost opt-in, scoped agents, workspace isolation, safe skills | Security approval |
| SP-11 | Optional WanGPProvider | feasibility + license/hardware/API verification | Separate integration approval |
| SP-12 | Commercial readiness | license/ToS/rights/attribution register, provenance evidence | Owner/legal approval |

SP-09–SP-11 не блокируют CPU-only MVP. Защищённый broker и реальные protected writes — только в отдельном S3.

## 3. SP-00: что обязательно определить до кода

Предлагаемые **имена, не утверждённая schema**: `ProductionBriefRef`, `Sequence`, `ShotSpec`, `TakeRef`, `CastRef`, `PlaceRef`, `VoiceRef`, `MediaAssetRef`, `RenderJob`, `ReviewFinding`, `TimelineRevision`, `DeliverableManifest`, `ProviderCapability`.

Для каждого: ID/version, ownership, immutable vs editable fields, refs, locale, provenance, rights, hashes, transitions, conflict/retry, retention, storage boundary. ShotSpec candidate fields: `shot_id`, `sequence_id`, `brief_revision`, `claim_refs`, `prompt_revision`, `reference_revisions`, `planned_duration_ms`, `actual_duration_ms`, `selected_take_id`, `lock/exclude`, `review_status`, `artifact_hash`, `provider/model/version`. Отдельно закрыть human approval vs editorial approval, source-of-truth for timings и recovery semantics.

## 4. Минимальные acceptance scenarios

1. **CPU-only RU/UK:** Windows 10/11 + Intel integrated graphics, без NVIDIA/WanGP/интернета; ≥3 сцены, WAV, SRT и playable MP4 через FFmpeg. Ручной режим без LLM.
2. **Selective rebuild:** изменение текста сцены 2 сохраняет hashes сцен 1/3, обновляет только зависимые narration/subtitles/timeline/export; изменение длительности корректирует offsets без потери дублей.
3. **Review/locks:** reject/redo/choose earlier take, lock/exclude; генератор не меняет locked shot без согласия, а «approve take» не создаёт editorial grant.
4. **QA:** fixtures с пустым WAV, black/frozen frame, неверным subtitle timestamp, audio clipping/silence; измеримые дефекты FAULT, неуверенный lip-sync CHECK/not measurable, всё с shot/time/evidence.
5. **Preflight:** missing input, unsupported model, offline, disk limit, invalid rights/region — отказ до inference/paid call с RU/UK диагностикой; planned dimensions/ETA не выдают за факт.
6. **Jobs:** повтор exact request_id+payload после lost ACK возвращает прежний job, altered payload — conflict, после crash возможен unknown_after_restart без автоматического resubmit.
7. **Chunk resume:** interruption сохраняет validated checkpoints; changed source hash/tool/settings не принимает старые chunks, originals и referenced assets не удаляются.
8. **Versions:** compare v1/v2, restore/duplicate без стирания истории; REVOKED editorial APPROVE не возрождается.
9. **Workspaces:** missing refs видимы, archive opt-in, shared asset не удаляется в другом workspace, backup/restore проверяет dependencies.
10. **Provider off:** без WanGP/GPU/cloud весь CPU путь работает; unsupported provider не вызывает silent fallback к платной модели.
11. **Security:** agent без scope не читает/отменяет чужие jobs и не пишет в protected store; credentials не попадают в Git/logs.
12. **Commercial:** per-model/voice/media license, region, output rights, ToS и атрибуция проверены; paid WanGP embedding только с письменным разрешением.
13. **Installer:** чистая Windows без winget, offline pinned CPU setup, rollback runtime без отката protected editorial history.

## 5. Stop conditions и следующая задача

Ни один успешный MP4, preview, SHA или LLM verdict не равен protected approval, legal rights или разрешению на публикацию. Любая неразрешённая лицензия, конфликт authority, невалидный output, неопределённый оплачиваемый job или нарушение storage boundary — STOP/explicit review.

Следующий предлагаемый шаг: **SP-00 Production Handoff & Shot Contract Proposal** — исключительно docs/fixtures в новой ветке после отдельного owner approval, затем независимая проверка и STOP. Не менять `main`, не создавать PR/merge/release без разрешения.
