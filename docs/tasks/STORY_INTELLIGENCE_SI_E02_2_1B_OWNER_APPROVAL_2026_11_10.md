# SI-E02.2.1b — EVAL findings contract: owner approval and freeze

Дата: 2026-11-10.
**APPROVED / OWNER DECISION — EVAL-P01–P04 AND 42 TEST REQUIREMENTS.**
**DOCS ONLY. IMPLEMENTATION NOT AUTHORIZED. EVAL-P05 OPEN / NOT APPROVED.**

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Source branch: `docs/story-intelligence-si-e02-2-1a-eval-findings-contract`.
Exact base: `78285d35e7a816dd9f98430613a518ee1dda90c1`.
Publication branch: `docs/story-intelligence-si-e02-2-1b-findings-approval`.
Основание — явное решение владельца в задании SI-E02.2.1b.

## 1. Exact approved revision and precedence

На указанном base зафиксированы и одобрены в приведённой ниже области:

| Источник | Exact Git blob (file identity, не golden vector) | Область approval |
| --- | --- | --- |
| [FINDINGS_CONTRACT_PROPOSAL](STORY_INTELLIGENCE_SI_E02_2_1A_FINDINGS_CONTRACT_PROPOSAL.md) | `74f5626c8e1ce2c0ba514fcd668496527a5fe7b6` | EVAL-P01–P04, связанные closed local types, digest bindings, confidence/portfolio rules, validation/mappings/order и неизменные boundaries |
| [TEST_ORACLES](STORY_INTELLIGENCE_SI_E02_2_1A_TEST_ORACLES.md) | `14edf438c42a373214d91ba02a24128c9a12e86c` | Все N01–N04 и T01–T38 как normative future test requirements, с исходными limitations |

Оригинальные документы не редактируются. Их исторические PROPOSAL/NOT APPROVED
формулировки superseded **только для указанного approval**, не для EVAL-P05 и не
для реализации. Настоящие явные уточнения имеют приоритет в своей узкой области;
остальное exact содержание сохраняется. [EVAL-D01–D03](STORY_INTELLIGENCE_SI_E02_2_1A_OWNER_APPROVAL_2026_11_10.md)
остаются утверждёнными. Никакой blanket approval всех будущих EVALUATE behaviors.

## 2. EVAL-P01 — Closed non-persisted findings structure: APPROVED

Утверждён exact HumanFindingsInput local value contract из §§1–3 источника:
EvaluationBinding с exact StoryIdea/Angle/Audience/Channel/Rubric refs, complete
ordered ratings SHA-256, frozen ContextSnapshot и exact ordered semantic input roots;
individual confidence findings и portfolio-entry duplicate findings с canonical
verification всех bindings. Полные Rating bytes включают value/confidence/basis/
explanation и exact refs. Portfolio binding включает exact index, entry digest и
candidate ref, а не совпадающий title/id.

Literal local `contract_tag` остаётся **`si-evaluate-findings/proposal-1`** из frozen
источника: слово proposal в значении не даёт права переименовать approved input.
Не добавлять новый wire version, transport/Request field или SI record. У local value
нет H/SIRef, persistence, authority, authenticated reviewer или fabricated Run output.
SHA связывает bytes, но не доказывает identity, чтение, scientific truth либо rights.

## 3. EVAL-P02 — Confidence consideration: APPROVED

- SUFFICIENT: неопределённость рассмотрена человеком только для limited eligibility.
- INSUFFICIENT и missing required confidence finding: research gap, EVIDENCE_NEEDED.
- Duplicate или conflicting finding keys: INVALID по утверждённому mapping, не last-wins.
- UNKNOWN rating value остаётся UNKNOWN; aggregate при нём UNKNOWN.
- Исходный confidence level не изменяется.
- Nonempty basis/reason/reviewer label не заменяет human finding.

Missing consideration само по себе **не инвалидирует** иначе structurally valid SI
graph. Отсутствующее обязательное поле local object, malformed finding или неверный
binding — отдельные validation failures, а не этот eligibility gap.

## 4. EVAL-P03 — Exhaustive local portfolio coverage: APPROVED

В первой bounded версии expected pairs охватывают **все entries KNOWN local
ChannelContext portfolio**. DISTINCT закрывает только duplicate-review gap exact pair;
DUPLICATE, UNRESOLVED и missing required pair finding дают REVIEW_DUPLICATE с
DUPLICATE_REVIEW_NEEDED. UNKNOWN portfolio даёт NEEDS_RESEARCH/EVIDENCE_NEEDED;
KNOWN empty portfolio не создаёт local pair-review gap.

Coverage локальна, не доказывает global novelty/market uniqueness. Никаких silent
shortlists, automatic topic rejection/merging/prioritization или Selection/Topic Intent.
Одинаковый candidate ref в нескольких entries не отменяет exact index/entry binding.

## 5. EVAL-P04 — Validation and diagnostics: APPROVED

Утверждены exact validation phases, binding checks, existing code mappings,
deterministic diagnostics ordering и сохранение всех applicable eligibility reasons
из §5 frozen источника. В частности:

- Missing human finding — eligibility gap; не malformed SI graph сам по себе.
- Invalid finding structure, wrong digest, wrong exact ref и conflicting finding — validation failure.
- INVALID важнее STALE; нет accepted current evaluation при любом из них.
- R1 §3.2 precedence остаётся: validation/currentness → BLOCKED → NEEDS_INPUT → NEEDS_RESEARCH → REVIEW_DUPLICATE → ELIGIBLE_FOR_CREATIVE.
- Положительные findings и high score не дают automatic approval/production permission.

Wrong shape/hash/missing SIRef нельзя переименовывать в обычную research uncertainty.
Нет новых reason codes, исправления refs, automatic rebasing или implicit latest.

## 6. EVAL-P05 — OPEN / NOT APPROVED

Не разрешены Request envelope changes, findings inclusion в request_payload_sha256,
новые request_id semantics, persistent replay mapping или operation version changes.
Ссылки на existing R1 request rules в proposal/T27 сохраняют условный будущий смысл,
не утверждают adapter или current Request shape. EVAL-P05 не prerequisite для bounded
pure evaluator без request_id/persistence. Outer integration требует отдельного approval.

## 7. Approval всех 42 oracle requirements

| Группа | Количество | Нормативная область |
| --- | ---: | --- |
| N01–N04 | 4 | Numeric boundaries, literal 510 example и UNKNOWN propagation |
| T01–T09 | 9 | Confidence, conflicts, frozen ratings/Rubric bindings |
| T10–T22 | 13 | Exact pair outcomes, exhaustive coverage, changed portfolio/candidates |
| T23–T28 | 6 | Blockers/precedence, determinism и request boundary |
| T29–T38 | 10 | Exact refs/provenance/currentness, Unicode, mutation и diagnostics boundaries |
| Всего | 42 | Future test requirements, не выполненные tests |

Утверждены также stated fixture/oracle discipline и limitations:

- **Unit tests: NOT RUN — DOCS ONLY.** Approval не evidence runtime PASS.
- T25 не задаёт complete literal oracle base eligibility classifier; missing-framing mappings и complete premises не изобретать.
- T27 касается future Request integration, не executable requirement текущего pure evaluator и не исключение из EVAL-P05 OPEN.
- G01/G02/F1-D1 suites/vectors не переписывать; T31–T33 сохраняют их boundaries, не требуют future Creative roots для EVALUATE.
- Никаких manufactured golden vectors или заявления readiness неописанного base classifier.

## 8. Compatibility and STOP

Original/R1/R1a/R1b, SI/1 schemas/records/field order, EvaluationReport/RunRecord,
девять SI-D04 weights, aggregate formula, R1 precedence, exact canonical hashes,
provenance и G01/G02/F1-D1 неизменны. RU/UA wire `ru/uk`, CPU-only fallback и
licensing constraints сохранены. No new record/wire field/operation/dependency.

[Implementation boundary](STORY_INTELLIGENCE_SI_E02_2_1B_IMPLEMENTATION_BOUNDARY.md)
отделяет закрытый findings contract от base-classifier details; см.
[RESULT](STORY_INTELLIGENCE_SI_E02_2_1B_RESULT.md).
`PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF;
Windows S3.2b BLOCKED_HOST_NOT_PROVIDED. Без PR/merge/release/main changes.
**STOP для independent review. SI-E02.2.1-RESUME не начинать.**
