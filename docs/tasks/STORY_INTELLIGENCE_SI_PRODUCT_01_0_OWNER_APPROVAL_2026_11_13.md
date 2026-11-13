# SI-PRODUCT-01.0 — Owner approval recording

Дата решения: **2026-11-13** (Europe/Kyiv).
**APPROVED / OWNER DECISION — ARCHITECTURE AND PD-01–PD-08.**
**DOCS ONLY. IMPLEMENTATION NOT AUTHORIZED.**

Основание — явное сообщение владельца «SI-PRODUCT-01.0 — Owner Approval Recording»
в текущей сессии: четыре документа утверждены как архитектурная основа, PD-01–PD-08
утверждены с обязательными условиями PD-01/PD-05 ниже. Запись не является решением,
принятым Codex вместо владельца, и не заявляет отдельную аутентификацию/подпись.

## 1. Exact approved source and ancestry

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Reference branch: `docs/story-intelligence-si-product-01-0-projection-contract`.
Exact reference commit: `5e0ddf45aacb2412dd15b9a4923acb40c6a6c7bd`.
Его exact parent / evaluator foundation base:
`35451f6441bd5428e132ae65f2080209b51fe009`.
Recording branch: `docs/story-intelligence-si-product-01-0-owner-approval`.
Новый recording commit строится поверх reference commit, не поверх main/archive branch.

Владелец утверждает exact contents четырёх документов на reference commit как
архитектурную основу в указанном scope. Blob identities — file identities, не новый
canonical protocol, не подписи и не runtime golden vectors:

| Approved source file | Exact blob at reference commit | Approved scope |
| --- | --- | --- |
| [CONTRACT_PROPOSAL](STORY_INTELLIGENCE_SI_PRODUCT_01_0_CONTRACT_PROPOSAL.md) | `9df03496e20b53a63f1d9341757486b959296ecc` | Private admission/Card, RU/UK catalog, status/score boundaries, exact preservation, privacy/limitations |
| [TEST_ORACLES](STORY_INTELLIGENCE_SI_PRODUCT_01_0_TEST_ORACLES.md) | `ad397a0659f9cd2e2c4ea78f1d5dad2616ac22a2` | P01–P42 and expansions, literal W01 RU/UK as future executable acceptance requirements; not evidence of execution |
| [OWNER_DECISIONS](STORY_INTELLIGENCE_SI_PRODUCT_01_0_OWNER_DECISIONS.md) | `8c254668206d42eea3195daf9cff213359aaa767` | Recommended choices PD-01–PD-08, with mandatory conditions below; alternatives not selected |
| [RESULT](STORY_INTELLIGENCE_SI_PRODUCT_01_0_RESULT.md) | `e244eba020576827dca6ce4a63d49f27cdac1fb7` | Architecture inventory/compatibility findings and accurately scoped historical verification record |

Historical PROPOSAL / NOT APPROVED wording на reference commit superseded только
этим approval и только в указанном scope. В recording revision актуализированы
статусы/approval links и добавлены обязательные условия; selectors, strings, card
fields, actions, score rules и evaluator semantics не меняются. Исторические test
counts не превращаются в результаты тестирования несуществующей Projection.
Файлы с `_PROPOSAL` в имени не переименовываются; это сохраняет existing links.

## 2. Approved decisions

| Decision | Status | Owner-selected rule |
| --- | --- | --- |
| PD-01 | **APPROVED** | Exact invocation association через безопасную повторную проверку pinned evaluator; mismatch → отказ без replacement; условия §3 обязательны |
| PD-02 | **APPROVED** | Private local Card с пятью sections; строгие OK/Rejected формы; отдельная presentation availability без новых SI/1 статусов |
| PD-03 | **APPROVED** | Explicit display_locale ru/uk, fixed dictionary, no fallback; evaluator locale/inputs не меняются |
| PD-04 | **APPROVED** | Exact integer score из/із1000 или UNKNOWN presentation; no thresholds/probabilities/ranking/production signal |
| PD-05 | **APPROVED** | Closed 30-family condition catalog, exact matching и отдельные validation explanations; условия §4 обязательны |
| PD-06 | **APPROVED** | Все diagnostic slots, blockers/gaps/actions и порядок сохраняются; no top-N/dedup by visible text |
| PD-07 | **APPROVED** | Generic per-type private aliases; no raw identifiers/paths/hashes/private text, no display grants/public sharing inferred |
| PD-08 | **APPROVED** | Все шесть fixed limitations; creative eligibility не scientific/rights/editorial/production/publication authority |

## 3. Mandatory PD-01 condition — evaluator verification

- **В V1 сохраняется безопасная повторная проверка evaluator.** Same-invocation
  verification не заменяется доверием к detached result, digest alone, cached flag,
  trusted-handoff shortcut или неполной проверкой структуры.
- При допустимых inputs вызывается тот же pinned pure evaluator с exact invocation
  arguments; supplied/recomputed outputs сравниваются по existing canonical values.
  Mismatch, exception или unsupported input не чинятся и не дают accepted Card.
  Existing admission failures до проверяемого вызова не становятся positive result.
- Предусмотреть и фактически измерить performance вне pure projection logic при её
  будущем implementation acceptance: environment/Python/CPU, fixture sizes, repeat
  counts, measured evaluator-only и full projection-with-verification durations.
  Никаких придуманных latency guarantees или изменяющих решение time thresholds.
- **Оптимизация не может ослаблять безопасность или проверяемость. Любое изменение
  механизма verification требует отдельного контракта и утверждения владельца.**
  Это относится и к альтернативе trusted same-invocation handoff: в V1 она не выбрана.
  Performance measurement сама по себе не является разрешением обхода проверки.
- Timing не попадает в Card и не влияет на result, ordering, privacy или eligibility.

## 4. Mandatory PD-05 condition — executable findings coverage

Будущее отдельное implementation task обязано обеспечить executable test coverage
**всех 30** семейств: RC01–RC09, C01–C05, K01–K06, V01, Q01–Q04, F01–F05.
Проверяются RU и UK, blocking cases, material findings и их сохранение при нескольких
одновременных conditions. 30 × 2 — минимальная family/locale matrix, не общее число
unittest methods и не замена variant-specific/negative tests.

Обязательны оба Risk path variants, Claim/evidence conditions, generic LEGAL плюс
specific Visual rights, full ordered T25/W01, INVALID/STALE distinction, missing/
unsupported projection inputs, privacy, nonmutation/detachment, score/UNKNOWN и все
шесть limitations. Mapping/catalog inspection не заменяет вызов настоящей Projection.

**Существующие evaluator tests не доказывают работоспособность ещё не реализованной
Projection.** 78 evaluator tests исторического preflight — evidence evaluator только.
Нужны новые исполняемые projection tests с genuine evaluator results, independently
literal expected RU/UK outputs и без mock accepted-success paths. В этом recording
этапе эти tests не создаются, не меняются и не запускаются как будто уже существуют.

## 5. Approval limits and unchanged boundaries

Утверждены архитектура и test requirements, **не implementation authorization**,
не runtime PASS, не production readiness. Для реализации требуется отдельное явное
задание владельца; подготовленный [implementation task draft](STORY_INTELLIGENCE_SI_PRODUCT_01_1_IMPLEMENTATION_TASK_DRAFT.md)
не запускается и не становится утверждённым executable scope через эту ссылку.

Не меняются SI/1, evaluator, EvaluationReport/RunRecord/Request, девять criteria/weights,
score completeness/currentness/provenance, EVAL-P01–P04, RC-P01–P06, Q1–Q3,
SI-E02.1/TI/SR, G01/G02/F1-D1, editorial/storage contracts. Нет новых authority,
scientific certainty, rights clearance, authenticated reviewer или verified assets.
RU/UK, CPU-only, licensing gates сохраняются; LLM/provider/network/UI/persistence/
discovery/production integration отсутствуют. No hooks/findings/assets/Brief invention.

EVAL-P05 **OPEN**; PUBLISH_REVISION **DISABLED**; partial COMMIT reconstruction **OFF**;
Windows S3.2b **BLOCKED_HOST_NOT_PROVIDED**.

## 6. Publication, evidence and STOP

Recording commit и review ZIP — local Codex workspace. Никакой push/PR/merge/tag/release
без отдельного разрешения. Предыдущее разрешение загрузить старый `review.zip` в
archive-only branch не разрешает публикацию этого нового recording/ZIP.

В [RESULT](STORY_INTELLIGENCE_SI_PRODUCT_01_0_RESULT.md) — документы/проверки записи;
full recording SHA/parent, diff и ZIP сообщаются после local commit. Собственный SHA
в содержимое того же commit не встраивается. WORKLOG дополнен по repository rules.
**READY_FOR_OWNER_REVIEW — запись утверждения. STOP. НЕ НАЧИНАТЬ РЕАЛИЗАЦИЮ.**
