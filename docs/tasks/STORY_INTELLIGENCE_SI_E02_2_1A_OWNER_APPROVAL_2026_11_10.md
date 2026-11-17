# SI-E02.2.1a — EVAL-G01: owner approval

Дата: 2026-11-10.
**APPROVED / OWNER DECISION — EVAL-D01–D03 ONLY.**
**Scope: DOCS ONLY. IMPLEMENTATION NOT AUTHORIZED.**

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Source branch: `feat/story-intelligence-si-e02-2-1-pure-evaluate`.
Exact base: `24cbe823574489f7f7450af1a662203a164efbcf`.
Publication branch: `docs/story-intelligence-si-e02-2-1a-eval-findings-contract`.
Основание — явное owner-approved задание SI-E02.2.1a.

## EVAL-D01 — UNKNOWN confidence

Явный human finding определяет, достаточно ли рассмотрена неопределённость
**для ограниченной цели EVALUATE eligibility**. Finding обязан быть привязан к exact
evaluation inputs и relevant rating. Он не меняет исходный confidence level,
не превращает UNKNOWN rating в KNOWN и не удостоверяет scientific truth/evidence quality.
Finding нельзя выводить из непустого Text, ключевых слов или reviewer label.
При необходимости finding его отсутствие или противоречивость должны приводить к
fail-closed поведению. Точная форма и mapping такого отказа предлагаются отдельно,
а не утверждаются этим принципом.

## EVAL-D02 — Duplicate comparison

Human finding фиксирует результат сравнения конкретной duplicate candidate pair.
Концептуальные outcomes: **DISTINCT / DUPLICATE / UNRESOLVED**.
Он указывает exact current StoryIdea и Angle, exact portfolio candidate и relevant
context. Нельзя основывать решение только на normalized title equality либо
свободном Angle.distinction. Missing finding не равен DISTINCT.
Ни Selection/Topic Intent record, ни automatic topic prioritization не создаются.

## EVAL-D03 — Deterministic precedence

Findings проверяются **до использования** при определении eligibility.
Сохраняется [R1 §3.2](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md):

1. Invalid/stale inputs — нет accepted current evaluation.
2. Blocking risks — BLOCKED.
3. Missing required inputs — NEEDS_INPUT.
4. Research gaps — NEEDS_RESEARCH.
5. Unresolved duplicates — REVIEW_DUPLICATE.
6. Иначе — ELIGIBLE_FOR_CREATIVE.

Все relevant reasons остаются видимыми. Новые SI/1 reason codes без отдельного
owner approval запрещены. Положительный finding не отменяет blocking risk,
не заменяет claims/evidence/rights review и не разрешает производство.

## Что не утверждено этим решением

[Findings contract](STORY_INTELLIGENCE_SI_E02_2_1A_FINDINGS_CONTRACT_PROPOSAL.md) и
[test oracles](STORY_INTELLIGENCE_SI_E02_2_1A_TEST_ORACLES.md) имеют статус
**PROPOSAL / NOT APPROVED**, включая поля, local tag, hashing bindings, coverage,
error mapping, ordering и missing/conflicting behavior. Их публикация и ссылки
здесь не утверждают proposed structure и не разрешают implementation.

[Предыдущие RESULT](STORY_INTELLIGENCE_SI_E02_2_1_RESULT.md) и
[CONTRACT_GAPS](STORY_INTELLIGENCE_SI_E02_2_1_CONTRACT_GAPS.md) остаются историческими
BLOCKED_CONTRACT artifacts. Принципы EVAL-D01–D03 задают направление разрешения
EVAL-G01; до отдельного review полного input contract и resume handoff engine не возобновлять.

Original/R1/R1a/R1b, SI-D01–D10, [SI-E02.1a approval](STORY_INTELLIGENCE_SI_E02_1A_OWNER_APPROVAL_2026_11_10.md),
[G01](STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_APPROVAL_2026_11_10.md),
[G02](STORY_INTELLIGENCE_SI_E01_2B_3_G02_OWNER_APPROVAL_2026_11_10.md) и
[F1-D1](STORY_INTELLIGENCE_SI_E01_2B_3_F1_D1_OWNER_APPROVAL_2026_11_10.md) неизменны.
Ни новых SI/1 полей/типов/порядков, ни изменения hashes/девяти weights/formula нет.
RU/UA с wire locales `ru/uk`, CPU-only fallback и licensing requirements сохраняются.
SI-D03/Topic Intent/science automation/ERef adapter для ERef-free inputs/production
handoff/Windows writer/network/LLM/GPU/provider не prerequisites pure evaluator.

**Unit tests: NOT RUN — DOCS ONLY.** См. [RESULT](STORY_INTELLIGENCE_SI_E02_2_1A_RESULT.md).
`PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF;
Windows S3.2b BLOCKED_HOST_NOT_PROVIDED. Без PR/merge/release/main changes.
**STOP для independent review; SI-E02.2.1 implementation не возобновлять.**
