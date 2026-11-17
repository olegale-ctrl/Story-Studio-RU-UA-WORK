# SI-E02.2.1a — Human findings: proposed test oracles

Дата: 2026-11-10. **PROPOSAL / NOT APPROVED / NOT RUN.**
Base: `24cbe823574489f7f7450af1a662203a164efbcf`.
[Owner approval](STORY_INTELLIGENCE_SI_E02_2_1A_OWNER_APPROVAL_2026_11_10.md) утверждает
только EVAL-D01–D03; таблицы ниже зависят от отдельного approval
[proposed local contract](STORY_INTELLIGENCE_SI_E02_2_1A_FINDINGS_CONTRACT_PROPOSAL.md),
в частности EVAL-P01–P04. Это требования к будущим тестам, не executable tests,
не утверждённые golden vectors и не фактические PASS.

## Fixture/oracle discipline

B — будущий genuine ERef-free content-addressed граф с exact Idea/Angle/Audience/
Channel/Rubric/Intake/producer Run и всеми relevant source/check/risk refs. Все domain
inputs valid/current, framing достаточно, no open blocker/research/duplicate gaps,
KNOWN complete local portfolio (пустой, если case не задаёт другое).
Никакого Creative/Selection/Brief для EVALUATE. Положительная достаточность supplied
human data — явно authored premise fixture, не вывод из одного CURRENT.

R — девять KNOWN ratings в approved order, each=5, с basis_refs/explanation и HIGH
confidence. При confidence UNKNOWN тест добавляет exact human finding только где
указано. При nonempty portfolio сравнение каждой entry требуется по EVAL-P03.
Expected scores/outcomes/reasons/paths автор тестов фиксирует **до** вызова engine.
Hash/ref fixtures строятся independently stdlib JSON/SHA-256, literal expected digests
фиксируются отдельно после approval структуры; не брать ожидания из evaluator.
Нельзя mock-подменять resolver/provenance или считать fake hash валидным.

Для valid/current cases resolver/provenance должны реально принять graph, а accepted
currentness — подтвердить CURRENT. Для provenance-negative cases resolver может пройти,
но provenance должен отказать. Schema/hash failures проверяются как таковые, а не
подменяются искусственным boolean. После изменения ancestor перестроить настоящие
hashes всех descendants и manifests, кроме намеренно повреждённого edge.

## Независимые numeric oracles

Approved weights в порядке Rubric: 15/10/10/20/15/10/10/5/5.

| ID | Values | Буквальное ожидаемое значение |
| --- | --- | --- |
| N01 | Девять 0 | KNOWN 0 |
| N02 | Девять 5 | KNOWN 1000 |
| N03 | 1/2/3/4/5/0/1/2/3 | KNOWN 510 |
| N04 | В R заменить один value на UNKNOWN | UNKNOWN, не 0/взвешенное среднее; NEEDS_RESEARCH/EVIDENCE_NEEDED |

Findings не меняют values/confidence/weights/aggregate. Для UNKNOWN aggregate exact
reason Text будущего результата также потребуется literal fixture при implementation
handoff; этот документ не вводит новое поле или canonical bytes EvaluationReport.

## Положительные, отрицательные и adversarial cases

Где сказано INVALID/STALE — никакого accepted current eligibility/result, даже если
arithmetic вычислим. Для valid inputs reason_codes — lexical unique union всех
applicable codes; rows с одним condition перечисляют полный ожидаемый список.

| ID | Изменение B/R или findings | Независимый expected oracle |
| --- | --- | --- |
| T01 | UNKNOWN confidence, непустой basis, finding отсутствует | NEEDS_RESEARCH; [EVIDENCE_NEEDED]; aggregate KNOWN 1000; basis не считается finding |
| T02 | Тот же rating + exact SUFFICIENT | ELIGIBLE_FOR_CREATIVE; []; aggregate 1000; исходный level остаётся UNKNOWN |
| T03 | Тот же rating + INSUFFICIENT | NEEDS_RESEARCH; [EVIDENCE_NEEDED]; score 1000 не снимает gap |
| T04 | UNKNOWN rating value + UNKNOWN confidence + SUFFICIENT | NEEDS_RESEARCH; [EVIDENCE_NEEDED]; aggregate UNKNOWN, исходный rating не меняется |
| T05 | Два findings одного criterion с разными outcomes, binding корректен | INVALID/TYPE по `$.human_findings.confidence_findings[1]`; не выбирать positive/last |
| T06 | Два byte-identical findings того же criterion | Такой же INVALID/TYPE, не silently deduplicate |
| T07 | Полный новый binding, но отдельный finding имеет digest старого rating/binding | INVALID/REF_HASH_MISMATCH по фактически первому неверному digest field; не STALE-as-research |
| T08 | Старые genuine Rubric/ratings/binding целы, observed context выбрал новую Rubric | STALE/INPUT_STALE; никакого reuse old positive finding как current |
| T09 | Новый Rubric ref с неверным hash или неверными weights/key set | INVALID/REF_HASH_MISMATCH или TYPE на соответствующей проверке; 100% сумма не разрешает изменённые SI-D04 weights |
| T10 | Title-match portfolio entry, сравнения нет | REVIEW_DUPLICATE; [DUPLICATE_REVIEW_NEEDED]; Angle.distinction не решает outcome |
| T11 | Exact pair T10 с DISTINCT | ELIGIBLE_FOR_CREATIVE; []; только эта pair закрыта |
| T12 | Exact pair T10 с DUPLICATE | REVIEW_DUPLICATE; [DUPLICATE_REVIEW_NEEDED]; нет merge/reject/priority/Selection |
| T13 | Exact pair T10 с UNRESOLVED | REVIEW_DUPLICATE; тот же code, без auto DISTINCT |
| T14 | Три entries: DISTINCT, DUPLICATE, UNRESOLVED | REVIEW_DUPLICATE; code один unique, две отдельные pair diagnostics с index 1 и 2 |
| T15 | Три entries: DISTINCT, DISTINCT, missing | REVIEW_DUPLICATE; diagnostic на duplicate_findings и entry index 2; отсутствие не DISTINCT |
| T16 | Нет title match, но KNOWN portfolio entry есть и finding отсутствует | По proposed exhaustive coverage — REVIEW_DUPLICATE; это EVAL-P03 choice, не уже approved dedup rule |
| T17 | Genuine старый Channel/binding, observed active refs сменили portfolio membership/order | STALE/INPUT_STALE; findings по старым indices не переносить |
| T18 | Новый binding/context, но старый portfolio entry digest либо чужой candidate_ref | INVALID/REF_HASH_MISMATCH либо PROVENANCE_MISMATCH по actual mismatch; нельзя присоединить review к другому материалу |
| T19 | Candidate revision поменялась: old exact candidate и frozen context сохранились, observed context новый | STALE/INPUT_STALE; no implicit latest; при dangling new ref — INVALID/REF_MISSING |
| T20 | Дважды один portfolio index, DISTINCT затем UNRESOLVED | INVALID/TYPE по второму item, независимо от reason/request wording |
| T21 | Findings для двух разных indices с одной exact candidate ref, обе entries явно DISTINCT | Valid; обе entries покрыты; не схлопывать по candidate id, ELIGIBLE при B premises |
| T22 | KNOWN empty portfolio vs UNKNOWN portfolio | Empty: нет pair gap; UNKNOWN: NEEDS_RESEARCH/EVIDENCE_NEEDED; UNKNOWN не known [] |
| T23 | Положительные findings + open CENTRAL factual scientific blocker | BLOCKED; [CENTRAL_CLAIM_UNSUPPORTED]; aggregate1000 не clearance |
| T24 | Research gap и UNRESOLVED pair одновременно | NEEDS_RESEARCH; [DUPLICATE_REVIEW_NEEDED,EVIDENCE_NEEDED]; обе diagnostics видимы |
| T25 | Blocking claim + missing framing + research + duplicate conditions | BLOCKED; все relevant existing reasons сохранены; нет подавления нижних классов/score override |
| T26 | Same call дважды; затем изменён только reason finding | Identical input → identical detached result; changed reason не reuse cached human input; pure API не имеет request_id/cache |
| T27 | Same outer request_id/different canonical bytes, если будущий approved adapter включает findings | По existing R1 — REQUEST_CONFLICT. **Outer adapter NOT APPROVED/NOT IMPLEMENTED**, никакого current request schema extension; pure call не выдаёт этот conflict |
| T28 | Добавить request_id в proposed local envelope | INVALID/UNKNOWN_FIELD; byte-exact request semantics не дают hidden replay mechanism |
| T29 | Missing exact basis_ref/candidate_ref target в bundle | INVALID/REF_MISSING до eligibility, не missing-human-finding research |
| T30 | Wrong ref type/hash; cycle; actual Run method/provenance mismatch | INVALID соответствующего existing code; использовать настоящие graphs, не один test flag |
| T31 | Legitimate HUMAN_EDIT history-only dependency/ERef в старом Run; current producer без ERef | Прежняя G01/F1-D1 expected CURRENT при достаточных current inputs; findings не повышают audit-only ref до required-current |
| T32 | Relevant original CREATIVE Run ERef/direct claim constraint или actual current REVISION Run ERef | Relevant unresolved ERef → INVALID/REF_MISSING; замена exact required G02 claim → accepted STALE/INPUT_STALE; findings не обходят эти разные проверки |
| T33 | Один root STALE, другой имеет relevant unresolved ERef | INVALID/REF_MISSING важнее STALE при любом порядке проверки roots |
| T34 | Keys/indices переставлены, неизвестный enum/tag, лишнее или missing field, bool вместо index | INVALID/TYPE, VERSION_UNSUPPORTED, UNKNOWN_FIELD либо MISSING_FIELD по §5; не canonicalize/reorder/coerce malformed input |
| T35 | ru и uk fixtures, composed/decomposed reason или explanation | Exact Unicode сохраняется; изменения bound rating/context bytes меняют digests; никаких ua aliases/normalization/автоперевода |
| T36 | Изменён только basis_refs/explanation/confidence.basis прежнего criterion | rating/list/binding digests больше не совпадают со старыми findings; INVALID/REF_HASH_MISMATCH, no transplanted positive review |
| T37 | Вызов с findings для known HIGH confidence | INVALID/TYPE; этот input не подменяет factual confidence |
| T38 | Смена unrelated existing Selection head в frozen vs observed ContextSnapshot | Explicit expected-context mismatch → STALE; не новая semantic dependency EVALUATE от будущего Selection |

## Diagnostics и ограничения ожиданий

Для T25 конкретные missing-framing code/message/path фиксируются из separately
specified base evaluator condition mapping, **не изобретены этим findings proposal**.
Он проверяет precedence и сохранение всех переданных base-condition reasons, но
не утверждает новый общий classifier research/framing/risk. Если реализация требует
неопределённого classifier, нужен отдельный gap; T25 нельзя выдать за готовый literal
vector всей EVALUATE операции. Та же оговорка относится к exact localized messages:
implementation handoff фиксирует ожидаемые strings до runtime, не получает их из функции.

T31–T33 расширяют входные cases, не переписывают accepted G01/G02/F1-D1 suites/vectors.
В evaluator, не принимающем Creative roots, T32 original C проверяется на boundary
через accepted APIs, а current producer case — непосредственно на допустимом input.
Не добавлять Creative в обязательные EVALUATE roots ради теста.

Mutation oracle для всех cases: originals records/refs/ratings/findings/context
сохраняют exact bytes; returned mutable values detached. Даже отказ не меняет input.
Determinism oracle: повтор, другой dictionary insertion order при тех же valid
canonical values, lexical reason-code union и stable generated diagnostic order.
Ошибки нескольких malformed SI полей сохраняют accepted validator order; нет
требования менять existing modules ради нового invalid-input diagnostics ordering.

Missing findings и conflicting findings принципиально различны: первые не разрешают
positive eligibility (research/duplicate-review по proposal), вторые не дают accepted
result вообще. Это proposed конкретизация fail-closed, требует EVAL-P02/P04 approval.

**Unit tests: NOT RUN — DOCS ONLY.** Новые tests/runtime/vector artifacts не созданы.
Ни один case не evidence научной истинности, identity/rights или Windows qualification.
`PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF;
Windows S3.2b BLOCKED_HOST_NOT_PROVIDED. **STOP; без реализации/PR/merge/release/main changes.**
