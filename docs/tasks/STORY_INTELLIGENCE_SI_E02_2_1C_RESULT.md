# SI-E02.2.1c — Required-current clarification: result

Дата: 2026-11-10.
**COMPLETED — DOCS ONLY / IMPLEMENTATION NOT AUTHORIZED.**

## Git preflight и состав

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Source: `feat/story-intelligence-si-e02-2-1-resume-pure-evaluate`.
Exact base / parent: `ba7af2aaf3571fe801ee26b6027fd5b734b50094`.
Publication branch: `docs/story-intelligence-si-e02-2-1c-required-current-contract`.

До edits remote source HEAD и local HEAD совпали с base; worktree clean, unmerged
paths отсутствовали. RESUME RESULT/CONTRACT_GAPS прочитаны; checked approved findings,
original/R1/R1a/R1b и G01/G02/F1-D1 boundaries. Ветка создана строго от exact base.
Final full commit/remote SHA, parent и diff/stat сообщаются после публикации;
self-referential hash не встраивается в собственное содержимое commit.

Только четыре новых файла:

| Файл | Статус / результат |
| --- | --- |
| [OWNER_APPROVAL_2026_11_10](STORY_INTELLIGENCE_SI_E02_2_1C_OWNER_APPROVAL_2026_11_10.md) | Нормативно APPROVED / OWNER DECISION **только EVAL-F01–F03** |
| [REQUIRED_CURRENT_CONTRACT_PROPOSAL](STORY_INTELLIGENCE_SI_E02_2_1C_REQUIRED_CURRENT_CONTRACT_PROPOSAL.md) | PROPOSAL / NOT APPROVED: separate local premise, exact binding/coverage, requirements/period/evidence, diagnostics/privacy |
| [TEST_ORACLES](STORY_INTELLIGENCE_SI_E02_2_1C_TEST_ORACLES.md) | PROPOSAL / NOT APPROVED / NOT RUN: 34 cases, у каждого явный approval status expected outcome |
| Этот RESULT | Документационные проверки, remaining decisions и STOP |

## Approved principles и proposed details

EVAL-F01: explicit human determination REQUIRED/NOT_REQUIRED/UNDETERMINED, без
вывода из keywords/Text/dates/clock/LLM/assumptions.
EVAL-F02: UNDETERMINED либо missing REQUIRED specification/period → NEEDS_INPUT;
complete REQUIRED с недостаточно установленной freshness → NEEDS_RESEARCH;
NOT_REQUIRED не устанавливает freshness/reliability и не снимает ordinary research gap.
EVAL-F03: отдельная non-persisted exact-bound premise; missing determination — input
gap, malformed/contradictory binding — validation failure; no reviewer authority.

Proposal **не меняет HumanFindingsInput**. Reuse его EvaluationBinding как отдельное
значение; отдельные hashes связывают source assessment с context/ratings и required_data.
Охват semantic Source set исключает исключительно historical/audit ancestors.
Required data specs и review periods frozen, UTC интервалы заданы человеком; нет
TTL/default expiry или календарного обновления. Multiple sources рассматриваются
раздельно. Adequacy proposal требует coherent Evidence/ClaimCheck/Material/locator/
coverage support, а не только positive Text; машина не доказывает истину/реальное чтение.

Предложено переиспользовать EVIDENCE_NEEDED для input/research gaps с разными diagnostic
classes; **этот mapping и exact paths ещё не утверждены**. INVALID прежде STALE,
higher BLOCKED и lower reasons сохраняются. New error vocabulary не вводится.

## Original reproducer

Оригинальный EVAL-RESUME-G01 остаётся неизменным: 8 records/8-ref Closure/6 CURRENT
roots; UNKNOWN Source.freshness_requirement; нет claims/risks/ERefs/duplicate candidates,
ratings KNOWN5/HIGH и approved finding arrays пусты. Все четыре исходных input hash
переписаны в TEST_ORACLES без изменений и сверены с source report.

Для этого exact graph с отдельным UNDETERMINED owner-approved expected primary
outcome теперь **NEEDS_INPUT**, не NEEDS_RESEARCH/ELIGIBLE. Missing premise также
NEEDS_INPUT по F03. Это normative expected outcomes, не выполненный engine тест;
старые BLOCKED отчёты не переписаны, ранее «eligibility не вычислялся» остаётся верным.

## Remaining owner decisions / implementation impact

- RC-P01: exact local structure/tag/nullable argument и digest bindings — до premise validator/API consumption.
- RC-P02: Source coverage/requirements completeness, missing vs malformed и contradictory combination rules — до input-gap/coverage implementation.
- RC-P03: frozen UTC interval/review_period/coverage comparison — до temporal adequacy logic.
- RC-P04: minimum explicit evidence/check/material support и human-reviewed scope — до positive freshness establishment.
- RC-P05: existing-code/path mappings и combined diagnostics/order — до полного independent oracle этих branches.
- RC-P06: argument-only private lifetime и запрет implicit capture/export — граница pure use; persistence/export contracts не prerequisites pure computation.

Новое material противоречие approved contracts в этом docs этапе не выявлено.
Есть конкретные unapproved варианты adequacy/coverage/encoding для separate owner review,
а не право выбрать их автоматически. Full base classifier BC01/BC02/non-freshness
framing и старое T25 limitation этим узким proposal не объявляются закрытыми.
EVAL-P05 остаётся OPEN и не prerequisite bounded pure evaluator.

## Verification и STOP

**Unit tests: NOT RUN — DOCS ONLY.** Новый diagnostic script/evaluator/test code не
создавался и не запускался; прежний reproducer execution не выдан за новый PASS.
Проверены exact base/source, four-file A-only allowlist, 20 relative links/fences,
34 явно маркированных cases, EVAL-F scope vs RC proposal statuses, исходные hash
identities и unchanged approved HumanFindingsInput/source report blobs.
`git diff --check` и `git diff --cached --check` — exit 0. Фактические stats/parent/
remote SHA equality/clean worktree проверяются при publication и сообщаются в handoff.

Existing schemas/field order, EvaluationReport/RunRecord, EVAL-P01–P04, SI-D04 nine
weights/formula, R1 precedence, G01/G02/F1-D1, canonical hashes/provenance/refs,
contracts/source/tests/golden vectors/config/dependencies/RFC/WORKLOG неизменны.
RU/UA wire `ru/uk`, CPU-only и licensing constraints сохранены. Нет SI-D03/Topic
Intent/science automation/ERef adapter/production handoff/Windows writer, network/
LLM/GPU/provider или новой authority. `PUBLISH_REVISION` DISABLED; partial COMMIT
reconstruction OFF; Windows S3.2b BLOCKED_HOST_NOT_PROVIDED.
Без PR/merge/release/main changes. **STOP для independent review. Evaluator не возобновлён.**
