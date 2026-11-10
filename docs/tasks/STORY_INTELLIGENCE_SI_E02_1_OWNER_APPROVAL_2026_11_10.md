# SI-E02.1 — Owner approval P01–P05

**Дата:** 2026-11-10 (Europe/Kyiv).
**Статус: APPROVED / OWNER DECISION — P01–P05 ONLY.**
**Scope:** documentation and contract preparation only; production implementation NOT AUTHORIZED.

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Source branch: `docs/story-intelligence-si-e02-0-architecture-inventory`.
Exact source: `a577746f308828d75d2ea7262eaa94ab18a523c1`.
Publication branch: `docs/story-intelligence-si-e02-1-owner-approval`.
Owner handoff: **«OWNER APPROVED — P01–P05»**, с конкретными решениями ниже.

## Нормативное решение

Основание — [SI-E02.0 owner proposal](STORY_INTELLIGENCE_SI_E02_0_OWNER_DECISION_PROPOSAL.md),
[inventory](STORY_INTELLIGENCE_SI_E02_0_ARCHITECTURE_INVENTORY.md) и
[contract gap matrix](STORY_INTELLIGENCE_SI_E02_0_CONTRACT_GAP_MATRIX.md) на exact base.
Владелец выбрал P01/1, P02/2, P03/1, P04/1, P05/2. Это supersedes только ожидание
решения по этим пяти вопросам; старые документы остаются историческими и не редактируются.

### P01 — Topic Scoring / Ranking: option 1 APPROVED

Повторно использовать девять ранее утверждённых SI-D04 критериев и веса.
Сравнение criterion-by-criterion показывает evidence, confidence и явные UNKNOWN.
Existing aggregate допустим только по утверждённым completeness rules: UNKNOWN
не 0; никаких implicit weight changes, новых thresholds или скрытой renormalization.
Редактор-человек определяет приоритет. Automatic cross-candidate ranking, tie-breaking
и priority execution **не утверждены**. Наличие балла не объективизирует суждение
и не означает science/rights/production readiness.

### P02 — Durable Topic Intent: option 2 APPROVED, contract design only

Подготовить узкий **proposal** durable human intent относительно exact StoryIdea.
Рассмотреть research/defer/reject/prioritize как возможные действия; точные operation
names и semantics остаются **PROPOSAL до отдельного approval**. Сначала проверить
минимальное расширение existing Selection semantics; параллельный approval mechanism
без доказанной необходимости не вводить. Нет auto topic approval; reviewer labels
не authenticated identities. Persistence/lifecycle implementation заблокированы до
отдельного contract approval. Это разрешение проектировать, не изменять schema/code.

### P03 — Production Brief Consumer: option 1 APPROVED

Повторно использовать **existing SI ProductionBrief**. Первый consumer — private,
human-reviewable editorial card с exact provenance и прежними evidence/rights boundaries.
Новый ProductionBrief wire type не нужен. Automated SI→editorial handoff, assignment
queue и production execution остаются отдельной будущей работой.

### P04 — ERef Integration Order: option 1 APPROVED

Первый bounded implementation path **может** использовать local SI bundles без ERefs
после отдельного implementation handoff. Existing ERefs нельзя удалять/подменять
ради CURRENT. Exact G01/G02/F1-D1 обязательны. Read-only editorial snapshot adapter
требует отдельного утверждённого контракта. Нет implicit latest, rebasing или
UNKNOWN-as-validated. P04 не изменяет error/status behavior принятого currentness.

### P05 — Scientific Review Coverage: option 2 APPROVED, requirements design only

Подготовить science-specific review profile/checklist: terminology, chronology,
competing explanations, counter-evidence, qualifications, source traceability,
intended-use rights. Различать established evidence, interpretation, uncertainty и
unsupported claims. Scientific readiness не выводится из numerical score.
Essential unreviewed claims либо essential materials без прав/проверенного fallback
остаются blockers. Универсальные source-count thresholds, экспертные credentials
или automatic scientific approval не изобретать. Детальные checklist IDs, capture/
completion rules и будущий executable profile **не утверждены этим решением**.

## Приоритеты и что не утверждено

Сохраняются [SI-D01–SI-D10](STORY_INTELLIGENCE_V1_OWNER_APPROVAL_2026_11_09.md),
[original SI/1](STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md),
[R1](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md),
[R1a](STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md),
[R1b approval](STORY_INTELLIGENCE_V1_R1B_OWNER_APPROVAL_2026_11_09.md),
[G01](STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_APPROVAL_2026_11_10.md),
[G02](STORY_INTELLIGENCE_SI_E01_2B_3_G02_OWNER_APPROVAL_2026_11_10.md) и
[F1-D1](STORY_INTELLIGENCE_SI_E01_2B_3_F1_D1_OWNER_APPROVAL_2026_11_10.md).
A1–A14/O1–O10/storage contracts и editorial/render boundaries не пересматриваются.

[Topic Intent proposal](STORY_INTELLIGENCE_SI_E02_1_TOPIC_INTENT_CONTRACT_PROPOSAL.md)
и [Scientific Review proposal](STORY_INTELLIGENCE_SI_E02_1_SCIENTIFIC_REVIEW_PROFILE_PROPOSAL.md)
создаются по P02/P05, но **не получают APPROVED status через ссылку из этого документа**.
Их exact wire/version/action/capture/retention решения требуют отдельного owner review.
Current SI/1 validators продолжают разрешать только существующие Selection scopes,
choices и targets. Ни одного нового enum/method/record не вводится в этом этапе.

## Публикация и STOP

Создаются только четыре allowlisted SI-E02.1 Markdown, включая [RESULT](STORY_INTELLIGENCE_SI_E02_1_RESULT.md).
Existing files/code/schemas/tests/contracts/RFC/main неизменны.
**Unit tests: NOT RUN — DOCS ONLY.** Проверяются base, allowlist, links/status/diff;
final commit/remote SHA и clean worktree сообщаются после publication в handoff.

**STOP для independent review.** SI-E02.2/implementation не начинать; без UI,
evaluators, operations, adapters, persistence, production integrations, PR/merge/release.
`PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF; Windows S3.2b
BLOCKED_HOST_NOT_PROVIDED. RU/UA сохраняется с wire locales `ru/uk`; CPU-only и
обязательные лицензии/права до коммерческого использования остаются gates.
