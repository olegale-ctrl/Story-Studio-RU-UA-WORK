# SI-E02.1a — Topic Intent & Scientific Review: owner approval

Дата: 2026-11-10.
**APPROVED / OWNER DECISION — TI-P01–TI-P06 / SR-P01–SR-P04 ONLY.**
Scope: документация. **IMPLEMENTATION NOT AUTHORIZED.**

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Source branch: `docs/story-intelligence-si-e02-1-owner-approval`.
Exact base: `3e9adca8cdd17da69a3e72225a8129a8122c4311`.
Publication branch: `docs/story-intelligence-si-e02-1a-contract-decisions`.
Основание — явное решение владельца в задании SI-E02.1a.

## Область действия

Сохраняются [P01–P05](STORY_INTELLIGENCE_SI_E02_1_OWNER_APPROVAL_2026_11_10.md)
с options 1/2/1/1/2. Ниже утверждаются только перечисленные принципы из
[Topic Intent proposal](STORY_INTELLIGENCE_SI_E02_1_TOPIC_INTENT_CONTRACT_PROPOSAL.md)
и [Scientific Review proposal](STORY_INTELLIGENCE_SI_E02_1_SCIENTIFIC_REVIEW_PROFILE_PROPOSAL.md).
Их прежний PROPOSAL status остаётся историческим; эта публикация закрывает ожидание
решения по десяти принципам, но не утверждает оба предложения целиком.
Рекомендации по admission, builder order, новым wire values и capture не становятся
нормативными через ссылку. Открытые детали перечислены в
[boundary matrix](STORY_INTELLIGENCE_SI_E02_1A_CONTRACT_BOUNDARY_MATRIX.md).

## Утверждённые решения Topic Intent

### TI-P01 — Versioned Selection extension

Утверждено направление минимального расширения existing Selection под отдельным
версионированным контрактом. Legacy SI/1 неизменен. Параллельный TopicIntent record
не вводить без независимо доказанной необходимости. Exact schema version,
reader dispatch и migration behavior остаются открытыми.

### TI-P02 — Human actions

Утверждён смысловой набор `RESEARCH`, `DEFER`, `REJECT`, `PRIORITIZE` под концептуальным
purpose `TOPIC_INTENT`. Это требования, **не допустимые сейчас SI/1 wire tokens**.
RESEARCH выражает намерение исследовать; DEFER — отложить рассмотрение; REJECT —
отказаться от разработки exact темы/context; PRIORITIZE — выделить её для внимания
человеком. Нет automatic approval, ranking, job execution или authority grant.
Точное включение в command/choice schema и поведение admission ещё не утверждены.

### TI-P03 — Exact scope

Утверждены exact StoryIdea revision + Audience + Channel context, explicit human
action и exact target binding. Target относится к той же точной StoryIdea, а не
просто к совпадающему id. Human intent не доказывает authenticated editorial authority.

### TI-P04 — Immutable history

Утверждена exact-scope append-only revision chain с явным predecessor и
compare-and-set semantics. Новая StoryIdea revision либо изменённый audience/channel
context требует нового exact scope. Старые решения автоматически не переносятся.
Точные admission/atomicity/error details остаются отдельным контрактом.

### TI-P05 — Idempotency

Повторно использовать утверждённые [R1 §6](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md)
byte-exact request-id semantics. Идентичные retries не создают новых revisions и
не откатывают current head. Изменённые canonical request bytes с тем же request_id
дают conflict. Новый command envelope или новый error vocabulary этим не утверждены.

### TI-P06 — Private persistence boundary

Утверждено требование private, durable, integrity-preserving storage. Exact location,
locking, atomicity, recovery, retention, deletion, backup и privacy guarantees требуют
отдельного SI-D03 lifecycle contract. Durable writer implementation не разрешена.
RAM-only проверки не доказывают durable или crash-safe запись.

## Утверждённые решения Scientific Review

### SR-P01 — Profile form

Использовать нормативный scientific review checklist поверх existing SI records.
Не создавать параллельный ScientificApproval record или authority mechanism.
Нормативно требование checklist, а не ещё не определённый executable profile/version.

### SR-P02 — Coverage

Обязательно рассмотреть все семь областей:

- SR-C01 — terminology and definitions;
- SR-C02 — chronology and dating;
- SR-C03 — competing explanations;
- SR-C04 — counter-evidence;
- SR-C05 — qualifications and uncertainty;
- SR-C06 — source traceability;
- SR-C07 — intended-use rights.

Обязательное рассмотрение не означает положительного результата, завершённого
исследования или научной истины. Exact machine-readable completion criteria
остаются открытыми. Эти labels не новые wire enums, permissions или ClaimCheck states.

### SR-P03 — Human responsibility

Обязательны explicit human review и escalation нерешённых существенных противоречий,
неподтверждённых essential claims и rights gaps. Scores, confidence и reviewer labels
не доказывают truth, competence или authority. Existing blockers сохраняют силу;
запрос дополнительного review сам по себе blocker не снимает. Точная процедура
эскалации, ответственность и проверяемые traceability boundaries ещё требуют контракта.

### SR-P04 — Capture strategy

Начать с private human-readable checklist. Machine-verifiable completion, durable
capture, field mapping и export требуют отдельных утверждённых контрактов.
Hidden JSON в rationale/reason запрещён. Наличие текста «проверено» не machine proof.

## Совместимость, границы и STOP

Сохраняются SI-D01–D10, original/R1/R1a/R1b и
[G01](STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_APPROVAL_2026_11_10.md),
[G02](STORY_INTELLIGENCE_SI_E01_2B_3_G02_OWNER_APPROVAL_2026_11_10.md),
[F1-D1](STORY_INTELLIGENCE_SI_E01_2B_3_F1_D1_OWNER_APPROVAL_2026_11_10.md).
Historical ancestry не становится required-current автоматически; original CREATIVE
constraints и actual producer ERefs не игнорируются. Relevant ERef без exact validated
snapshot остаётся INVALID / REF_MISSING. Нельзя удалять ERefs ради CURRENT.

P01 сохраняет девять SI-D04 criteria/weights и completeness rules, без auto ranking;
P03 — existing ProductionBrief для private human-reviewable card; P04 — возможность
будущего bounded ERef-free пути, без adapter или handoff. Новые TI/SR contracts не
становятся общим prerequisite для pure EVALUATE на existing valid ERef-free SI inputs.
Это разграничение зависимостей, не разрешение реализации EVALUATE сейчас.

E00/A1–A14/O1–O10/storage и approved architecture не изменяются.
`PUBLISH_REVISION` — DISABLED; partial COMMIT reconstruction — OFF;
Windows S3.2b — BLOCKED_HOST_NOT_PROVIDED. RU/UA с wire locales `ru/uk`, CPU-only
fallback и licensing requirements сохраняются; нет автоматического импорта корпусов.

**Unit tests: NOT RUN — DOCS ONLY.** См. [RESULT](STORY_INTELLIGENCE_SI_E02_1A_RESULT.md).
Без production code, schemas, adapters, tests, UI, persistence и новых dependencies.
Без PR/merge/release/main changes. **STOP для independent review; SI-E02.2 не начинать.**
