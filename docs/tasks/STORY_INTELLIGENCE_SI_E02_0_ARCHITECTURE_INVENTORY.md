# SI-E02.0 — Architecture inventory

Дата: 2026-11-10 (Europe/Kyiv). **DOCS ONLY / IMPLEMENTATION NOT AUTHORIZED.**
Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Exact base: `9a631ebca2bccdd8e0157528b20080380ba8dcfe`.
Ветка: `docs/story-intelligence-si-e02-0-architecture-inventory`.

## Основание и правила статуса

На exact base найдены [итоговая приёмка SI-E01.2b.3](STORY_INTELLIGENCE_SI_E01_2B_3_FINAL_ACCEPTANCE_2026_11_10.md)
и [SI-E02 Planning Proposal](STORY_INTELLIGENCE_SI_E02_PLANNING_PROPOSAL_2026_11_10.md).
Первая принимает pure semantic currentness на `cd82fd654b270adcdf702eba915fd22c59aaeaff`
по independent static/code/contract review; runtime независимо **не перезапускался**.
Вторая — PROPOSAL, не утверждённый SI-E02 implementation contract. Owner handoff
разрешил только текущую документационную инвентаризацию SI-E02.0.

- IMPLEMENTED — существует конкретный код указанного ограниченного механизма;
  это не доказательство production qualification или наличия полного workflow.
- CONTRACT_APPROVED — есть нормативное owner decision, но указанный executor отсутствует.
- PROPOSAL — рекомендация/план, ещё не разрешение реализации.
- MISSING — в inspected first-party source нет требуемого механизма/типа/интерфейса.
- BLOCKED — применимый gate явно запрещает/останавливает путь до prerequisites.

Составные компоненты разделены на data/contract/runtime строки. Наличие schema
или тестового fixture не считается исполнением Discovery/Evaluation/assignment.
Проверены first-party `story_intelligence/`, `editorial/`, `core/`, `scripts/`, tests
и нормативные docs; upstream/reference материалы отделены от принятых компонентов.

## Архитектурная карта

| Компонент | Назначение | Текущий статус | Основание | Пробел |
| --- | --- | --- | --- | --- |
| Topic Discovery — offline contract | Локальная тема/источники → StoryIdea, possible duplicates | CONTRACT_APPROVED | [R1 §2](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md), DISCOVER_LOCAL/si.discover-local; [SI-D01–10 approval](STORY_INTELLIGENCE_V1_OWNER_APPROVAL_2026_11_09.md) | Нет executor, локального dedup/каталога или выполнения stage |
| Topic Discovery — поиск/runtime | Retrieval, построение карточек, discovery runs | MISSING | [SI source](../../story_intelligence/__init__.py), [provenance_v1._GENERATORS](../../story_intelligence/provenance_v1.py) только проверяет существующий DISCOVERY Run | Нет crawler/search/trends/API; URL_METADATA не делает fetch |
| Topic input — editorial data | Ручные кандидаты и source metadata | IMPLEMENTED | [editorial/model.py](../../editorial/model.py): CandidateRevision, SourceRevision, SourceDetails; [codec](../../editorial/codec.py) | discovery_method закрыт manual_topic/manual_url/manual_local; не machine Discovery |
| Topic Scoring — agreed policy | Девять heuristic criteria, weights, UNKNOWN и blockers | CONTRACT_APPROVED | [Original §5](STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md), [R1 §3](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md), SI-D04 approval | Нет исполняемого evaluator/ranker; не probability/viral model |
| Topic Scoring — data validation | Rubric/ratings/assessment representations | IMPLEMENTED | [records_v1._SCHEMAS/_local](../../story_intelligence/records_v1.py): Rubric/EvaluationReport; editorial GenreProfile, RubricCriterion, CriterionRating, CandidateRevision.assessment | Не вычисляет score, не подтверждает rating basis, truth или полноту cross-record критериев |
| Topic Scoring — evaluator/ranking | Вычисление eligibility/aggregate и сравнение тем | MISSING | SI source содержит validators/resolver/provenance/currentness, не EVALUATE executor | Нужны закрытые executable postconditions/oracles существующего method; ranking/ties/comparability не реализованы |
| Editorial Selection — coherent packages | Проверка выбранных editorial refs и зависимостей | IMPLEMENTED | [current_package.build_current_package](../../editorial/current_package.py), ActiveSelections в model.py | Coherence не решение редактора, не approval authority |
| Editorial Selection — SI data | Exact human intent для Creative/Brief | IMPLEMENTED | records_v1 Selection; [model_v1.validate_header](../../story_intelligence/model_v1.py); currentness сравнивает used head | Валидатор не создаёт Selection и не проверяет все условия его принятия/eligibility |
| Editorial Selection — SI command/projection | RECORD_SELECTION, SELECT/REQUEST_CHANGES/WITHDRAW, BriefReviewState | CONTRACT_APPROVED | R1 §§2/4; R1a closed operation sets | Нет executor, human review UI/CLI или вычислителя полного BriefReviewState |
| Topic decision / priority | Долговечное решение именно о StoryIdea и очередности тем | MISSING | Selection.target_ref в records_v1 допускает только CreativeAlternative/ProductionBrief; [R1 §4.1](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md) | Нельзя назвать topic approval/reject существующим SI Selection или редакционным SCRIPT APPROVE |
| Story Intelligence — SI/1 foundation | Typed records, canonical bytes/hash, exact Closure, provenance/currentness | IMPLEMENTED | [codec_v1](../../story_intelligence/codec_v1.py), [model_v1](../../story_intelligence/model_v1.py), records_v1, [resolver_v1](../../story_intelligence/resolver_v1.py), provenance_v1, [currentness_v1](../../story_intelligence/currentness_v1.py); final acceptance | Только pure read-only supplied-data consistency; не engine execution/truth/rights |
| Creative output schemas | Hooks, titles, chapters, retention hypothesis, visuals/risks | IMPLEMENTED | records_v1: CreativeAlternative, VisualRequirement, Risk; original C и actual revision Runs проверяет provenance | PROPOSE_CREATIVE/template generation и human editing operations не реализованы |
| Production Brief — существующий SI тип | Самостоятельное pre-script задание | IMPLEMENTED | records_v1: ProductionBrief, _PRODUCTION, _local; provenance BRIEF_ASSEMBLY; currentness | Реализованы структура/проверки supplied graph, не сборка/сохранение/передача |
| Production Brief — assembly operation | ASSEMBLE_BRIEF, exact inputs, optional used Creative Selection | CONTRACT_APPROVED | R1 §2; [R1a](STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md) | Нет builder/executor или интерфейса в production |
| Production Brief — editorial embedded value | Frozen brief внутри ScriptRevision | IMPLEMENTED | editorial.model.BriefValue, ScriptRevision | Не заменяет SI ProductionBrief: нет полного evaluation/run/production payload |
| Production Assignment | Assignee/queue/deadline/resource reservation/ack | MISSING | editorial.model.ProductionRevision — production context; ScriptRevision.production_ref/candidate_ref — связи, не job; SI schema не содержит assignment record/method | Нужен отдельный контракт только если владелец требует durable assignment; не обходить protected publication |
| Review/evidence/rights — data | Claims, источники, exact evidence, qualifications, intended use | IMPLEMENTED | SI ClaimItem/EvidenceItem/ClaimCheck; editorial ClaimRevision/EvidenceLink/ClaimReview/RightsReview/RightsDetails; [rights_binding](../../editorial/rights_binding.py) | Material match не license/expiry/rights permission; metadata review не автоматический fact check |
| Editorial approval consistency/history | Exact decision key, negative history, reconsideration/REVOKE | IMPLEMENTED | [approval_consistency.evaluate_approval_consistency](../../editorial/approval_consistency.py), [approval_history.evaluate_current_approval_history](../../editorial/approval_history.py), [approval_attestation](../../editorial/approval_attestation.py) | Pure consistency/history/attestation не deployed OS authentication/authority |
| Protected authority contract | Gate×decision grants, sessions, anchor, editorial HANDOFF | CONTRACT_APPROVED | [A1–A14](E01_3_7_3_APPROVED_CONTRACT.md), [O1–O10](E01_3_8_1_APPROVED_CONTRACT.md) | SI labels/Selection не grants; runtime service отсутствует |
| Storage protocol / virtual model | S1 wire/crypto, W0–W9/recovery на VirtualStore | IMPLEMENTED | [storage_protocol_v1](../../editorial/storage_protocol_v1.py); [storage_transaction_model_v1](../../editorial/storage_transaction_model_v1.py): TransactionModel, VirtualStore, FixtureAuthority | Ключи/identity/grants синтетические, filesystem writer не реализован |
| Native protected Windows storage | SCM/SID/ACL/DPAPI/NTFS real writer | BLOCKED | [S3.2b host readiness](E01_3_9_4_S3_2B_PHASE0_HOST_READINESS.md) | BLOCKED_HOST_NOT_PROVIDED; portable LAB/virtual store не production service |
| SI persistence/request lifecycle | Private workspace, durable revisions/idempotency/retention | CONTRACT_APPROVED | SI-D03 — утверждён только принцип private workspace; R1 §6 | Конкретные location/atomicity/concurrency/privacy/retry lifecycle требуют отдельного контракта; writer MISSING |
| ERef integration | Validated exact editorial snapshot для SI consumers | MISSING | Currentness API не принимает snapshot/adapter; final acceptance/F1-D1 | Relevant ERef → INVALID/REF_MISSING, не CURRENT от UNKNOWN/hash |
| ReviewPacket — schema | Recorded private DISCUSSION_ONLY capture + redaction data | IMPLEMENTED | records_v1 ReviewPacket/_packet; [R1b approval](STORY_INTELLIGENCE_V1_R1B_OWNER_APPROVAL_2026_11_09.md) | Export builder, actual privacy review/grant verification/lifecycle не реализованы |
| Existing production MVP | Local WAV/stills → timeline/MP4; project/bundle validation | IMPLEMENTED | [first_video.read_plan/build](../../scripts/first_video.py), [core/project_schema.py](../../core/project_schema.py), [mp4_render.py](../../core/mp4_render.py), [export_bundle.write_bundle](../../core/export_bundle.py) | Вход не SIRef/Brief; нет автоматически проверенного SI/editorial handoff; local code не квалифицирован этим audit |
| SI-E02 next contract/runtime | Следующий ограниченный stage | PROPOSAL | SI-E02 Planning Proposal | E02.1/E02.2 не начаты, implementation не разрешена |

## Действующие границы, а не пробелы для обхода

- [G01 approval](STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_APPROVAL_2026_11_10.md):
  historical edit-base проверяется, но не становится current identity сам по себе.
- [G02 approval](STORY_INTELLIGENCE_SI_E01_2B_3_G02_OWNER_APPROVAL_2026_11_10.md):
  direct original C ClaimItem constraints остаются exact, новый hook их не отменяет.
- [F1-D1 approval](STORY_INTELLIGENCE_SI_E01_2B_3_F1_D1_OWNER_APPROVAL_2026_11_10.md):
  actual current producer ERefs и original C ERefs relevant; historical-only Run не
  promoted лишь по audit presence. Это реализовано в принятом F1-FIX, не открытый gap.
- [D1–D12](E01_3_9_1B_APPROVED_ARCHITECTURE_DECISION.md) и
  [S1 approval](E01_3_9_2B_S1_APPROVED_CONTRACT.md) приняты позже concept review
  2026-11-05. Его историческое «storage proposal не утверждён» не отменяет поздние
  approvals. Однако S1 не реализация Windows service; S2/portable LAB — pure only.
- [Portable LAB acceptance](E01_3_9_4_S3_2A_R1_INDEPENDENT_ACCEPTANCE.md) не даёт
  native qualification или production grants; Windows-platform limitation сохранена.
- [Архитектура SI](../architecture/STORY_INTELLIGENCE_ARCHITECTURE_DECISION_2026-11-05.md)
  запрещает подменять recommendation правами/approval. Переписывание завершённых
  этапов не требуется: нужны отдельно ограниченные дополнения и implementation gates.
- E00/1 проверен в [нормативном historical Git object](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/e520648411b99264688ff66dc61ad0e974201ed3/docs/EDITORIAL_E00_FINAL_SPEC.md):
  новый editorial production default 9:16 720×1280, explicit 16:9 1280×720;
  старые first_video defaults не меняются. Файл проверен в указанном commit,
  не предполагается присутствующим в current tree и не копируется.
- RU/UA — пользовательское название локализации; wire locale **ru/uk**, не ua.
  [RU UI](../../locales/ru/ui.json), [UK UI](../../locales/uk/ui.json) существуют;
  [script prompts](../../locales/ru/prompts/script_system.txt) не Creative executor.
- [Upstream reference guide](../../upstream/konlu-story-studio/modules/history-writing/GUIDE.md)
  не принятый SI engine. Китайские корпуса/Writing-DNA/AI providers автоматически
  не заимствуются; [import gate](../../LICENSES/IMPORT_LICENSE_GATE.md) сохраняется.
- `PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF; Windows S3.2b
  BLOCKED_HOST_NOT_PROVIDED. Нет нового permission читать/write protected storage.

## Вывод и переход

Existing ScriptRevision связывает production_ref и candidate_ref: для простой
привязки контекста эта часть уже есть. Отдельная queue/assignee/lifecycle модель
нужна только при таком явном требовании, не для переименования existing link.

Основной пробел — **операционный слой и связанные границы передачи**, а не отсутствие
SI типов или pure integrity. [Contract matrix](STORY_INTELLIGENCE_SI_E02_0_CONTRACT_GAP_MATRIX.md)
разделяет implementation gaps и необходимые owner decisions;
[proposal](STORY_INTELLIGENCE_SI_E02_0_OWNER_DECISION_PROPOSAL.md) не переутверждает
уже принятые веса/Selection semantics/Brief schema. **NOT RUN — DOCS ONLY.**
