# SI-E02.2.1c — Required-current data: owner approval

Дата: 2026-11-10.
**APPROVED / OWNER DECISION — EVAL-F01–F03 ONLY.**
**DOCS ONLY. IMPLEMENTATION NOT AUTHORIZED.**

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Source: `feat/story-intelligence-si-e02-2-1-resume-pure-evaluate`.
Exact base: `ba7af2aaf3571fe801ee26b6027fd5b734b50094`.
Publication branch: `docs/story-intelligence-si-e02-2-1c-required-current-contract`.
Основание — явное owner-approved задание SI-E02.2.1c.

## EVAL-F01 — Explicit required-current determination

Необходимость current data не выводится из keywords в user_goal/title/description,
непустого SourceItem.freshness_requirement, publication/capture date, system clock,
LLM inference или implicit editorial assumptions.
Утверждены conceptual values **REQUIRED / NOT_REQUIRED / UNDETERMINED**.
Determination явно поставляет caller как human editorial decision.
Это не новое SI/1 поле или record и не inferred scientific judgment.

## EVAL-F02 — Eligibility distinction

Утверждено:

- UNDETERMINED → NEEDS_INPUT.
- REQUIRED при отсутствии спецификации необходимых данных или периода → NEEDS_INPUT.
- REQUIRED с полными requirements, но недостаточно установленной freshness → NEEDS_RESEARCH.
- NOT_REQUIRED не устанавливает автоматически source freshness или factual reliability.
- Applicable ordinary freshness uncertainty → NEEDS_RESEARCH.
- При NOT_REQUIRED и отсутствии applicable freshness uncertainty дополнительного required-current gap нет.

Сохраняются higher-priority BLOCKED и все applicable lower-priority diagnostics.
Отсутствие дополнительного gap не равно безусловному ELIGIBLE_FOR_CREATIVE:
остальные утверждённые conditions/precedence остаются обязательными.

Для **exact synthetic reproducer EVAL-RESUME-G01** из
[CONTRACT_GAPS §3](STORY_INTELLIGENCE_SI_E02_2_1_RESUME_CONTRACT_GAPS.md)
expected primary outcome при human determination UNDETERMINED и отсутствии
higher-priority blocker — **NEEDS_INPUT**. Не заменять его NEEDS_RESEARCH/ELIGIBLE.
Это expected policy, не результат выполнения evaluator и не исправление прошлого отчёта.

## EVAL-F03 — Separate exact-bound premise

Determination представляется **отдельной non-persisted caller-supplied premise**,
связанной с exact evaluation context и relevant SI records. Approved HumanFindingsInput
не изменяется; confidence/duplicate fields нельзя использовать для freshness decision.
Malformed/contradictory premise bindings → validation failure.
Missing required determination → NEEDS_INPUT, не автоматически INVALID.
Никакого authority/authenticated reviewer claim не появляется.

## Область approval и неизменные контракты

[Required-current contract proposal](STORY_INTELLIGENCE_SI_E02_2_1C_REQUIRED_CURRENT_CONTRACT_PROPOSAL.md)
и [test oracles](STORY_INTELLIGENCE_SI_E02_2_1C_TEST_ORACLES.md) остаются
**PROPOSAL / NOT APPROVED**. Поля, tag, evidence/coverage/period rules, конкретные
code/path mappings и oracle fixtures в них этим документом не утверждаются.
Нормативны только EVAL-F01–F03 выше; не вводить новые error codes или TTL defaults.

Сохраняются [EVAL-P01–P04](STORY_INTELLIGENCE_SI_E02_2_1B_OWNER_APPROVAL_2026_11_10.md),
точный [HumanFindingsInput](STORY_INTELLIGENCE_SI_E02_2_1A_FINDINGS_CONTRACT_PROPOSAL.md),
EVAL-P05 OPEN, original/R1/R1a/R1b, SI-D04 weights/formula/R1 precedence,
[G01](STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_APPROVAL_2026_11_10.md),
[G02](STORY_INTELLIGENCE_SI_E01_2B_3_G02_OWNER_APPROVAL_2026_11_10.md),
[F1-D1](STORY_INTELLIGENCE_SI_E01_2B_3_F1_D1_OWNER_APPROVAL_2026_11_10.md).
SI/1 schemas/field order, EvaluationReport/RunRecord, exact refs/hashes/provenance
не меняются. UNKNOWN descriptive metadata не исправляется premise задним числом.

[RESUME_RESULT](STORY_INTELLIGENCE_SI_E02_2_1_RESUME_RESULT.md) остаётся историческим
BLOCKED_CONTRACT. Текущий approval задаёт required-current принципы; exact local
contract ещё требует review/approval, реализация не возобновляется.
RU/UA wire `ru/uk`, CPU-only fallback и licensing constraints сохраняются.
Без SI-D03/Topic Intent/science automation/ERef adapter/production handoff/Windows
writer, network/LLM/GPU/provider интеграций.
**Unit tests: NOT RUN — DOCS ONLY.** См. [RESULT](STORY_INTELLIGENCE_SI_E02_2_1C_RESULT.md).
`PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF;
Windows S3.2b BLOCKED_HOST_NOT_PROVIDED. Без PR/merge/release/main changes.
**STOP для independent review. Evaluator implementation не возобновлять.**
