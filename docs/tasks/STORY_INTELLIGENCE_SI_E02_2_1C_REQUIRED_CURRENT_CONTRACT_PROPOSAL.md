# SI-E02.2.1c — Required-current local premise proposal

Дата: 2026-11-10. **PROPOSAL / NOT APPROVED / NOT IMPLEMENTED.**
Base: `ba7af2aaf3571fe801ee26b6027fd5b734b50094`.
Нормативны только [EVAL-F01–F03](STORY_INTELLIGENCE_SI_E02_2_1C_OWNER_APPROVAL_2026_11_10.md).
Все структуры и конкретные predicates/mappings ниже — рекомендации RC-P01–P06 для
отдельного review. Это local plain-value contract, не SI/1 wire schema/operation.

## 1. Separate premise и reused types — RC-P01

Отдельный argument future pure evaluator: RequiredCurrentPremise или explicit None
для missing premise. Omitted argument предлагается эквивалентным None; это local
API choice, не изменение Request. HumanFindingsInput не получает дополнительных
полей, tag или altered digest. Ни H/SIRef, ни record/output/replay map не создаются.

Reuse exact EvaluationBinding из [approved findings contract §2–3](STORY_INTELLIGENCE_SI_E02_2_1A_FINDINGS_CONTRACT_PROPOSAL.md)
с [approval](STORY_INTELLIGENCE_SI_E02_2_1B_OWNER_APPROVAL_2026_11_10.md): Idea/Angle/
Audience/Channel/Rubric, ordered semantic roots, ContextSnapshot, ratings digest.
Значение premise.binding должно совпасть по C с binding existing HumanFindingsInput
и explicit evaluation arguments. Оно не назначает observed context.

Text/Hash/SIRef/Known/UTC — existing SI types. UTC — exact valid UTC seconds;
Period — замкнутый интервал предоставленных UTC boundaries, from_utc≤to_utc.
Plain dict/list/int/string only; все перечисленные поля required, без coercion,
normalization, unknown fields. Existing canonical value limits сохраняются, новых
quotas нет. `C`/`D=SHA256(C)` — existing exact canonical primitives, без нового domain.

```text
RequiredCurrentPremise = {
 contract_tag: "si-required-current/proposal-1",
 binding: EvaluationBinding,
 determination: REQUIRED | NOT_REQUIRED | UNDETERMINED,
 required_data: Known<List<DataRequirement>>,
 source_freshness: List<SourceFreshness>
}
DataRequirement = {
 source_ref: SIRef<SourceItem>,
 specification: Known<Text>, period: Known<Period>
}
Period = {from_utc: UTC, to_utc: UTC}
SourceFreshness = {
 binding_sha256: Hash, requirements_sha256: Hash,
 source_ref: SIRef<SourceItem>,
 applicability: APPLICABLE | NOT_APPLICABLE | UNDETERMINED,
 review_period: Known<Period>,
 outcome: ESTABLISHED | INSUFFICIENT | UNKNOWN,
 evidence: List<FreshnessEvidence>, reason: Text
}
FreshnessEvidence = {
 evidence_ref: SIRef<EvidenceItem>, check_ref: SIRef<ClaimCheck>,
 material_ref: SIRef<SourceItem>, material_sha256: Hash,
 coverage: Period
}
```

Closed local enums ровно как в нотации. Human reason описывает рассмотрение, но не
становится машинным result code, authority, truth или proof только из-за непустоты.
Existing record fields/Run/Report hash protocol остаются неизменными.

## 2. Exact binding, source coverage и changes — RC-P01/02

Каждая SourceFreshness содержит:

- binding_sha256 = D(полного EvaluationBinding), включая ratings/context/roots;
- requirements_sha256 = D({determination,required_data}) с exact значениями этих полей.

Это предотвращает accidental reuse другого scope/requirements; не подпись человека.
Модель угроз такая же, как SI private supplied assertions: злоумышленник может
переписать весь свой workspace и hashes; локальная проверка не доказывает review.

S — unique exact SourceItem refs, являющиеся current substantive dependencies этой
оценки: explicit semantic roots и typed payload/applicable producer dependencies по
accepted G01/G02/F1-D1. Полный audit Closure не равен S. Sources исключительно в
H.previous/исторических Run snapshots не добавляются в S автоматически. При реализации
проекция должна следовать accepted semantic roles, не новому «latest» traversal;
accepted currentness APIs/модули изменять или ослаблять для получения S запрещено.

DataRequirement.source_ref — в S, максимум одна requirement на exact source; несколько
необходимых data aspects одного source перечисляются в его explicit specification.
Все реально объявленные обязательными sources входят в KNOWN required_data; caller
делает явное human assertion полноты этого набора, машина не угадывает скрытые цели.
List упорядочен canonical exact ref tuple (type,id,revision,sha256); duplicates, включая
identical, INVALID/TYPE. Не сортировать malformed authored list автоматически.

Одна SourceFreshness на каждый source из S, в том же canonical order. Missing item
не добавляет fake entry и не считается NOT_APPLICABLE: proposed ordinary research gap.
Extra source вне S → INVALID/PROVENANCE_MISMATCH; missing referenced record → REF_MISSING.
Evidence/check/material refs тоже exact graph/provenance verified, но их исторические
audit ancestors не расширяют S автоматически только из-за premise proof lookup.
Они не становятся новыми operation semantic roots скрытым образом; это explicit
supplied support refs, frozen bytes которых проверяются для local judgement. Для
заявленных support roots отдельно применяются accepted currentness/ERef checks
относительно того же observed context. Relevant ERef support-материала без snapshot
даёт INVALID/REF_MISSING; proof не служит обходом adapter boundary. Такой extra check
не добавляет audit-only ancestors в S и не меняет semantics existing API. Если Source
уже является содержательной зависимостью main evaluation roots, proof label не
позволяет исключить его из S.

Source revision/context/ratings/required_data/period change требует нового bound human
input. Никаких auto carry-forward/rehash/rebase. Genuine old internally consistent
binding с изменённым observed context → STALE/INPUT_STALE; mismatched digest в
предоставленных bytes → INVALID/REF_HASH_MISMATCH, а не угаданная «просто устарелость».
Wrong-source item в otherwise current binding — validation failure, не research.

## 3. Required determination/specification — RC-P02

Нормативные states F02/F03 не выбираются по user_goal или Source text. Предлагается:

| Determination | Well-formed required_data | Eligibility contribution |
| --- | --- | --- |
| UNDETERMINED | UNKNOWN(reason) | NEEDS_INPUT; SourceFreshness может дополнительно дать research reasons |
| NOT_REQUIRED | KNOWN [] | Нет required-current gap; ordinary freshness рассматривается отдельно |
| REQUIRED | UNKNOWN, KNOWN [] либо list с UNKNOWN specification/period | NEEDS_INPUT: specification/period не complete |
| REQUIRED | Непустой list, все specification и period KNOWN | Требование complete; недостаточная freshness → NEEDS_RESEARCH |

UNDETERMINED с KNOWN list и NOT_REQUIRED с непустым/UNKNOWN required_data предлагается
отклонять TYPE как contradicting local combination. Это **proposed shape consistency**,
не дополнительное owner-approved правило F01. Missing entire premise (None) — NEEDS_INPUT.
Присутствующий object без required field, например required_data, — MISSING_FIELD/INVALID;
UNKNOWN в присутствующем поле не malformed и не превращается в missing SIRef.

REQUIRED list может указывать subset S: current data обязательны для этих sources,
остальные проходят ordinary freshness assessment, не автоматически REQUIRED.
Если source target ещё не определён, required_data=UNKNOWN — honest incomplete spec;
нельзя создать fake/dangling SourceItem ref вместо определения data target.

Period задаётся человеком как frozen интервал, не «сегодня», TTL или generated now.
As-of можно выразить from_utc=to_utc; horizon — явным интервалом. Никаких default
max_age, calendar rollovers, online checks или чтения системного времени. Temporal
comparisons только между supplied UTC values; from>to → TYPE, не research.

## 4. Ordinary/required source freshness и evidence — RC-P03/04

SourceItem.freshness_requirement остаётся descriptive Known<Text>. UNKNOWN не означает
ни REQUIRED, ни NOT_REQUIRED, ни established freshness. Premise не меняет этот record.
Даже KNOWN «вечнозелёная» строка не устанавливает NOT_APPLICABLE: решение explicit.
Предлагаемая source-level таблица:

| Explicit source assessment | Contribution |
| --- | --- |
| Missing SourceFreshness или applicability UNDETERMINED | NEEDS_RESEARCH/EVIDENCE_NEEDED |
| NOT_APPLICABLE, outcome UNKNOWN, review_period UNKNOWN, evidence [] | Нет ordinary freshness gap; явное человеческое scope решение, не global reliability |
| APPLICABLE, outcome UNKNOWN/INSUFFICIENT | NEEDS_RESEARCH/EVIDENCE_NEEDED |
| APPLICABLE, ESTABLISHED без достаточной bound evidence/KNOWN review_period | NEEDS_RESEARCH/EVIDENCE_NEEDED; asserted word не proof |
| APPLICABLE, ESTABLISHED с adequate support по правилам ниже | Нет freshness gap этой exact source/scope |

Для source в REQUIRED list NOT_APPLICABLE противоречит explicit requirement → TYPE.
Другие сочетания NOT_APPLICABLE (например ESTABLISHED или nonempty evidence) → TYPE,
не попытка выбрать удобную ветку. APPLICABLE/UNDETERMINED допускают supplied evidence;
положительная adequacy используется только при APPLICABLE+ESTABLISHED.

Для complete required source review_period должен быть KNOWN и совпадать с его
required period; несовпадение **valid intervals** — insufficient freshness → research,
а malformed interval — validation failure. Для ordinary APPLICABLE source без
required_data также нужен explicit KNOWN review_period для positive establishment.

Предлагаемая minimum support rule для ESTABLISHED, без автоматического fact-checking:

1. Evidence list непуст. Все evidence_ref/check_ref/material_ref graph/hash/provenance
   validated; EvidenceItem.source_ref == material_ref, ClaimCheck.claim_ref ==
   EvidenceItem.claim_ref, Known ClaimCheck.evidence_refs включает exact evidence_ref.
   Несовместимые exact roles — PROVENANCE_MISMATCH, не auto correction.
2. EvidenceItem.locator KNOWN nonempty; relation=supports; ClaimCheck state=supported
   либо qualified с existing qualification/metadata invariants. Unreviewed/disputed/
   insufficient support не становится adequate из одного текста — research gap.
3. material_ref.payload.material_sha256 KNOWN и равен supplied material_sha256.
   Known mismatch → REF_HASH_MISMATCH; UNKNOWN material hash не подставлять supplied
   значением, establishment остаётся недостаточным (research). Record hash ≠ material hash.
4. Хотя бы один такой support имеет coverage, включающий весь review_period.
   Для первой версии не склеивать интервалы разных proofs неявно. Coverage — explicit
   human-reviewed temporal assertion, не inferred capture/publication date.
5. SourceFreshness.reason связывает рассмотрение exact subject source с данным
   scope/specification. Эта связь задаётся человеком в bound SourceFreshness, а не
   semantic parsing ClaimItem.statement/reason. Refs/period/hash checks доказывают
   coherence и наличие recorded support, **не** истинность, реальное чтение или
   что material действительно подтверждает freshness. Лживый coherent human input
   остаётся вне гарантии pure verifier; нельзя выдавать его за scientific certification.

Publication/capture dates допустимы как metadata рассмотренного источника, но сами по
себе не inference requiredness/adequacy. Source freshness не равна истинности claim,
лицензии, доступности raw bytes или editorial authority. Rights/blocking scientific
conditions сохраняют приоритет даже при adequate freshness support.

Это новые **proposed** adequacy/coverage constraints RC-P03/04. Они требуют review:
existing schemas задают evidence/check representation, но F01–F03 не утверждают эти
конкретные predicates. No automatic evidence creation, scientific profile workflow,
материальный fetch, disk read или новый evidence wire type.

## 5. Validation и deterministic diagnostics — RC-P05

Порядок дополняет existing approved findings verification без его изменения:

1. Existing SI/local shapes и typed ref syntax; для present premise — closed keys/
   tag/enums/Known/period shapes. Unknown key → UNKNOWN_FIELD, absent field → MISSING_FIELD;
   wrong enum/type/order/contradiction → TYPE, unsupported tag → VERSION_UNSUPPORTED.
2. Resolver/provenance для existing roots, observed refs и declared premise support
   refs; errors сохраняются. No valid-looking dict/hash shortcuts.
3. Binding/requirements digest checks, exact source coverage/order/unique keys,
   role coherence/evidence hash checks; malformed binding не используется для F02.
4. Все applicable accepted currentness checks плюс frozen vs observed context:
   любая INVALID важнее STALE. Historical-only ancestry не promoted.
5. Только для valid CURRENT inputs missing premise/UNDETERMINED/incomplete REQUIRED
   дают input-gap; source assessments дают research gaps; объединить с other base
   conditions и прежними findings, применить R1 priority, сохранить все reasons.

При None новая premise даёт только missing-determination diagnostic; не генерировать
фиктивные per-source assessments или diagnostics из несуществующего массива. Уже
установленные other base research conditions всё равно сохраняются. Present premise
с отсутствующим item для S даёт отдельный coverage research gap по §2/4.
None premise не отменяет graph/currentness validation остальных inputs. Нельзя
вернуть NEEDS_INPUT, скрыв broken ref, relevant ERef или higher-priority BLOCKED.
Duplicates одного source в premise → TYPE по второму item, identical и contradictory
одинаково; никаких last-wins. Phase order: shape → graph → binding/coherence →
currentness → eligibility; внутри local objects declared field order, arrays по индексу.
Сохранять existing validator order для SI errors. Не менять accepted modules.

Все следующие **конкретные code/path mappings — PROPOSAL**, не новый owner approval:

| Condition | Existing code / result | Proposed field_path |
| --- | --- | --- |
| Missing entire premise / UNDETERMINED | EVIDENCE_NEEDED / NEEDS_INPUT | $.required_current_premise / $.required_current_premise.determination |
| REQUIRED spec absent/empty/UNKNOWN | EVIDENCE_NEEDED / NEEDS_INPUT | $.required_current_premise.required_data |
| UNKNOWN specification/period in item i | EVIDENCE_NEEDED / NEEDS_INPUT | $.required_current_premise.required_data.value[i].specification или .period |
| Missing source assessment | EVIDENCE_NEEDED / NEEDS_RESEARCH | $.required_current_premise.source_freshness |
| Applicable UNKNOWN/insufficient proof | EVIDENCE_NEEDED / NEEDS_RESEARCH | $.required_current_premise.source_freshness[i].outcome |
| Wrong exact source role / conflicting binding | PROVENANCE_MISMATCH / INVALID | Фактический source_ref/binding path |
| Wrong digest/hash, missing ref, wrong type, cycle | Existing REF_HASH_MISMATCH / REF_MISSING / REF_TYPE_MISMATCH / DEPENDENCY_CYCLE / INVALID | Фактический failing field/accepted API path |
| Genuine outdated frozen context/source | INPUT_STALE / STALE | $.required_current_premise.binding.context_snapshot либо accepted currentness path |

Diagnostic input_ref — exact affected SourceItem ref, scope Idea ref либо null для
missing whole premise; message не authority. Для source coverage omission message
включает full exact ref, не label-only. Причины input и research могут иметь один code,
но отдельные diagnostics и precedence class: class определяется condition, не code.
Generated reason_codes — unique lexical ASCII union. Diagnostic ordering/dedup как
approved EVAL-P04: (precedence class,code,field_path,C(input_ref),message); classes
BLOCKED→NEEDS_INPUT→NEEDS_RESEARCH→REVIEW_DUPLICATE. Exact messages фиксируются future
literal fixtures, не генерируются evaluator как собственный oracle.

## 6. Privacy, non-persistence и owner decisions — RC-P06

Все premises/freshness reasons могут быть private. Не логировать/экспортировать,
не помещать в Run.caveats, EvaluationReport, ReviewPacket, rationale JSON или Request.
В local binding нет request_id/cache/replay/time/credential. Same explicit inputs
в любое календарное время дают тот же результат; новое решение требует нового
explicit input, не обновления source record/авто-reapproval.

| Decision NOT APPROVED | Что предложено | Реальный implementation gate |
| --- | --- | --- |
| RC-P01 Local shape/binding | Separate nullable premise, exact EvaluationBinding, source/requirements hashes | Local premise validator/API consumption |
| RC-P02 Specification/coverage | Global determination, per-source requirements, S excludes audit-only refs, missing vs malformed правила | Required-current input-gap и coverage branches |
| RC-P03 Period model | Frozen inclusive UTC intervals, explicit review_period, no clock/TTL | Temporal adequacy comparison, не realtime recency service |
| RC-P04 Evidence establishment | Exact Evidence/Check/Material/locator/coverage checks + explicit human judgement; no proof of truth | Positive source freshness establishment |
| RC-P05 Diagnostics/order | Existing codes/paths, INVALID before STALE, all input/research reasons | Independent complete outcomes для этих branches |
| RC-P06 Privacy/lifetime | Argument-only; no storage/export/request capture | Только граница pure use; durable/export остаются отдельно, не prerequisite pure path |

Новое material противоречие утверждённых контрактов при подготовке не установлено.
Полнота base classifier BC01/BC02 и non-freshness framing по-прежнему не доказана
этим узким предложением; прежнее T25 limitation не снимается. Это не разрешение
самостоятельно дополнять missing base policies или объявлять engine ready.

[Oracles](STORY_INTELLIGENCE_SI_E02_2_1C_TEST_ORACLES.md) — NOT APPROVED. Никаких новых
SI/1 schemas/fields/order/operations/error codes, canonical hashes/provenance changes.
EVAL-P01–P04/HumanFindingsInput unchanged, EVAL-P05 OPEN; G01/G02/F1-D1 сохраняются.
RU/UA `ru/uk`, CPU-only/licensing constraints сохранены; нет SI-D03/Topic Intent/
science automation/ERef adapter/production handoff/Windows writer/network/LLM/GPU/provider.
**Unit tests: NOT RUN — DOCS ONLY. STOP; без реализации/PR/merge/release/main changes.**
`PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF;
Windows S3.2b BLOCKED_HOST_NOT_PROVIDED.
