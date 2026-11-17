# SI-E02.2.1d — Required-current final owner-review proposal

Дата: 2026-11-12 (Europe/Kyiv).
**PROPOSAL / OWNER REVIEW PREPARATION. RC-P01–P06 NOT APPROVED.**
**DOCS ONLY / IMPLEMENTATION NOT AUTHORIZED.**
Base: `1fa37fa03b0dfb0a6ed754ddf70e9665c5a91eb0`.

## 1. Approval boundary and delta

Нормативны [EVAL-F01–F03](STORY_INTELLIGENCE_SI_E02_2_1C_OWNER_APPROVAL_2026_11_10.md),
[EVAL-P01–P04](STORY_INTELLIGENCE_SI_E02_2_1B_OWNER_APPROVAL_2026_11_10.md), original/
R1/R1a/R1b и G01/G02/F1-D1. RC-P01–P06 здесь — exact decisions для review, не approval.
[SI-E02.2.1c proposal](STORY_INTELLIGENCE_SI_E02_2_1C_REQUIRED_CURRENT_CONTRACT_PROPOSAL.md)
и его 34 cases остаются historical NOT APPROVED, без edits.

Главное уточнение RC-P03: **снять equality required/review intervals**. Предлагается
explicit confirmed coverage, содержащая required interval включительно с обеих сторон.
Owner одобрил направление такого рассмотрения в задании 1d, но не весь temporal
contract/структуру RC. Публикация этого package не фиксирует окончательное решение.

Структуру 1c рекомендуется сохранить: отдельная nullable premise и exact reuse
EvaluationBinding. Не добавлять второй as_of, max_age, acknowledgement, reviewer,
per-proof request hash или ещё один record. Они дублируют frozen Period/binding либо
расширяют authority/lifecycle. `review_period` сохраняется для ordinary freshness;
для positive establishment это **заявленный и поддержанный confirmed interval**, а
не интервал, обязанный равняться required period. Hashes двух разных scopes не
сливать: binding hash защищает context/ratings, requirements hash — determination/data.

## 2. RC-P01 — Closed field-by-field local schema

Argument `required_current_premise`: None либо следующий plain dict; omitted argument
предлагается считать None. Это local API convention, не Request field. None означает
missing determination (NEEDS_INPUT по F03); object с missing key — malformed.
Все поля в таблице required. Plain dict/list/str/int, Known union exact, no bool-as-int,
coercion, Unicode/date normalization, unknown keys или silent sorting. SI canonical
value limits сохраняются; новых bundle limits нет. No H/SIRef у premise.

| Path / field | Exact type / closed values | Check / meaning |
| --- | --- | --- |
| contract_tag | literal `si-required-current/proposal-1` | Exact local tag, не SI/1 version |
| binding | approved EvaluationBinding | C-equality с existing HumanFindingsInput.binding и explicit call |
| binding.idea_ref | SIRef<StoryIdea> | Exact type/id/revision/hash |
| binding.angle_ref | SIRef<Angle> | Angle.idea/audience roles совместимы с binding |
| binding.audience_ref | SIRef<AudienceHypothesis> | Existing ru/uk, не inferred analytics |
| binding.channel_ref | SIRef<ChannelContext> | Channel.audience_ref == binding.audience_ref |
| binding.rubric_ref | SIRef<Rubric> | Approved 9 criteria/weights; no latest |
| binding.semantic_input_refs | List<SIRef> | Exact ordered supplied roots, не sorted Closure |
| binding.context_snapshot | exact existing ContextSnapshot | context_version=1, active_input_refs, selection_head_refs, editorial_snapshot_sha256 unchanged |
| binding.ratings_sha256 | Hash | D(whole ordered supplied ratings) |
| determination | REQUIRED / NOT_REQUIRED / UNDETERMINED | Explicit human editorial premise, не keyword inference |
| required_data | Known<List<DataRequirement>> | Known list asserts complete declared required-source set |
| required_data.value[i].source_ref | SIRef<SourceItem> | Source in main S; one entry/source, canonical order |
| required_data.value[i].specification | Known<Text> | UNKNOWN = incomplete required data, не missing field |
| required_data.value[i].period | Known<Period> | UNKNOWN = required period unspecified |
| Period.from_utc / to_utc | UTC / UTC | Valid UTC seconds, inclusive, from≤to |
| source_freshness | List<SourceFreshness> | One assessment/source in main S, missing item = research gap |
| source_freshness[i].binding_sha256 | Hash | D(binding) |
| source_freshness[i].requirements_sha256 | Hash | D({determination,required_data}) |
| source_freshness[i].source_ref | SIRef<SourceItem> | Exact subject, in S |
| source_freshness[i].applicability | APPLICABLE / NOT_APPLICABLE / UNDETERMINED | Explicit ordinary freshness applicability |
| source_freshness[i].review_period | Known<Period> | Declared confirmed window; needs recorded support for positive use |
| source_freshness[i].outcome | ESTABLISHED / INSUFFICIENT / UNKNOWN | Not a scientific approval |
| source_freshness[i].evidence | List<FreshnessEvidence> | Authored order retained, no implicit union/stitching |
| source_freshness[i].reason | Text | Private human explanation, not code/credential |
| evidence[j].evidence_ref | SIRef<EvidenceItem> | Exact recorded evidence |
| evidence[j].check_ref | SIRef<ClaimCheck> | Exact recorded human check of same claim |
| evidence[j].material_ref | SIRef<SourceItem> | Exact material source of EvidenceItem |
| evidence[j].material_sha256 | Hash | Compare with KNOWN material SourceItem digest |
| evidence[j].coverage | Period | Explicit human-reviewed interval supported by this evidence |

Text nonempty/exact Unicode, Hash=64 lowercase hex. Known<T> ровно KNOWN/value либо
UNKNOWN/reason; null вместо Known недопустим. UTC ровно YYYY-MM-DDTHH:MM:SSZ с
реальной календарной датой/временем (no leap-second 60), по accepted SI UTC rules.
From>to диагностируется TYPE на .to_utc; malformed boundary — на самом from_utc/to_utc.
D(x)=SHA256(C(x)) existing canonical bytes, без нового domain/separator. Никаких clock,
UUID generation, request_id, authority, persistence или изменений HumanFindingsInput.

### Independent schema examples (parameterized, not wire aliases)

B — independently authored valid EvaluationBinding, S1 — real exact SourceItem ref;
эти symbols раскрываются в genuine fixtures, не передаются validators как строки.

- Positive: {contract_tag:literal,binding:B,determination:UNDETERMINED,
  required_data:{state:UNKNOWN,reason:"Scope not specified"},source_freshness:[]}.
  Well-formed, primary NEEDS_INPUT, не INVALID (source coverage gaps отдельно).
- Positive: NOT_REQUIRED + required_data=KNOWN[]; S1 assessment NOT_APPLICABLE,
  review_period=UNKNOWN, outcome=UNKNOWN, evidence=[], correct digests. No freshness
  gap, только если S={S1} и остальные conditions clear.
- Negative: удалить required_data key → MISSING_FIELD; заменить его на null → TYPE.
- Negative: binding.ratings_sha256 не равен D(actual ratings) → REF_HASH_MISMATCH;
  другой genuine frozen context при matching internal digests → STALE/INPUT_STALE.
- Negative: два identical либо contradictory S1 assessments → TYPE второго item;
  source_ref genuine, но вне S → PROVENANCE_MISMATCH. Missing record → REF_MISSING.

## 3. RC-P02 — Source-set algorithm proposal

Source role projection **не заменяет** accepted [currentness](../../story_intelligence/currentness_v1.py)
и не даёт validity certificate. [Resolver](../../story_intelligence/resolver_v1.py) /
[provenance](../../story_intelligence/provenance_v1.py) сначала проверяют exact audit
Closure всех нужных refs. Missing/hash/type/cycle/provenance — INVALID, no partial S.
Предлагаемый worklist соответствует typed traversal принятого currentness, а не
«всем SourceItems из bundle» или списку latest. Неподдерживаемый future type/tag fail closed.

1. Seed ordered main worklist = explicit semantic_input_refs данного evaluation;
   unrelated observed/context roots только проверяются, не автоматически включаются
   в substantive S. Typed root roles будущего bounded API должны быть явно заданы;
   ReviewPacket не становится domain input. No future Creative/Selection prerequisite.
2. Вести visited exact tuple (type,id,revision,sha256), S и expected used heads отдельно.
   При посещении SourceItem добавить **сам ref** в S, включая explicit Source root.
3. Typed payload refs обходить по accepted schema, Known=UNKNOWN refs не порождает.
   Не обходить H.previous, H.input_refs и Run.input_snapshot/context_snapshot как
   semantic edges. Они остаются mandatory audit-verifiable.
4. Explicit substantive RunRecord прозрачен через semantic_input_refs; REVISION
   base-first ref исключается как edit-base согласно accepted logic. Metadata Run
   не становится active domain identity. Selection payload dependencies при фактическом
   использовании проверяются по accepted roles/observed heads, не по самой новой дате.
5. Для domain record проверить own typed/header ERefs и actual producer Run header
   ERefs **до** HUMAN_EDIT skip. Обычный HUMAN_EDIT: пройти current payload, не
   восстанавливать semantic refs прежнего base через R.semantic_input_refs.
6. Для non-HUMAN_EDIT producers идти по substantive semantic_input_refs, исключая
   causal previous. payload.run_ref EvaluationReport не обходить вторично как domain
   edge. CreativeAlternative: payload.run_ref — original C, actual REVISION header
   отдельно. Сохранить original C direct ClaimItem constraints и applicable E1/Channel
   bindings; skip only genesis Angle role, overridden current payload Angle, как в
   accepted implementation. Это не разрешение удалить другие C inputs. Incompatible
   current Angle/frozen E1 → STALE, не auto rebase.
7. Finish main S как unique canonical tuple-sorted set. Check accepted currentness
   всех applicable main domain roots; INVALID любой relevant ERef приоритетнее STALE.
   Не менять accepted APIs ради экспорта S: future local projection обязана совпасть
   с их semantics и regression fixtures.
8. Premise support evidence/check/material refs отдельно resolve/provenance/currentness
   относительно того же observed context. Их ERefs не обходятся. Proof-only material
   не добавляет автоматически freshness-review-of-proof recursion в main S. Если тот
   же source имеет main substantive path, он обязательно остаётся S. Аудит ancestors
   support refs никогда не promoted только из-за proof lookup.

DataRequirement и SourceFreshness ordered by canonical exact source tuple; duplicates
identity проверяются до ordering, second entry → TYPE, no last-wins/dedup. Conflicting
hashes одной identity — REF_HASH_MISMATCH раньше coverage decisions. Missing assessment
для S → research; extra assessment outside S → validation failure. Multiple sources
рассматриваются независимо: adequate S1 не снимает gap S2.

### Four independent source-graph examples

Symbols — independently authored genuine graph templates, not executed cases.

| Graph | Explicit current paths | Audit-only / other paths | Independently expected S / boundary |
| --- | --- | --- | --- |
| SG1 | Source S3 HUMAN_EDIT; Evidence E→material T1 | S3.previous=S2.previous=S1, old R snapshots | {S3,T1}; S1/S2 intact but inactive не требуют assessments |
| SG2 | Current Idea.source_refs=[B]; current Check→Evidence→A | Historical Idea1 referenced A | {A,B}; independent current evidence path сохраняет A, несмотря на Idea edit |
| SG3 | Current K3→Angle B; original C direct Check→Evidence→A и direct Qa | K1/K2, старые snapshots | {A,B} плюс остальные actual current Source paths; Qa остаётся G02 constraint; ERef actual R3/original C → INVALID |
| SG4 | Main Idea→A; freshness proof Check→Evidence→material M | M только explicit support, old M history | Main S={A}; M отдельно graph/currentness/ERef-checked; если main Risk.basis_refs→M, S={A,M} |

SG3 — accepted dependency boundary example, не требование Creative для EVALUATE.
SG2 не делает старый A CURRENT автоматически: exact active set должен удовлетворять
всем текущим paths; иначе STALE, а missing A в audit graph — INVALID.

## 4. RC-P02/03 — Determination, missing values and temporal inclusion

Предлагаемые combinations 1c сохраняются: UNDETERMINED→required_data UNKNOWN;
NOT_REQUIRED→KNOWN[]; REQUIRED допускает UNKNOWN/KNOWN[]/partial specification
как honest incomplete input. Противоречивые combinations (например NOT_REQUIRED
с requirements) → TYPE. Эти exact combination checks ещё требуют owner approval.
REQUIRED complete означает nonempty list с KNOWN specification/period для каждого
явно declared required source (subset S). Нет target → UNKNOWN spec, не fake ref.

None premise → only missing-determination diagnostic, no fabricated per-source
assessments. Present premise с missing S item → separate research condition.
Required incomplete spec/period → NEEDS_INPUT. Полный requirement при insufficient
recorded freshness → NEEDS_RESEARCH. NOT_REQUIRED не снимает applicable ordinary gaps.
UNKNOWN SourceItem.freshness_requirement не requiredness/applicability inference;
explicit human determination/assessment не редактирует descriptive SI record.

### Revised temporal predicate (NOT APPROVED RC detail)

R = required_data.value[k].period.value для REQUIRED source.
Q = source_freshness[i].review_period.value — explicit declared confirmed coverage.
E = отдельный evidence[j].coverage с coherent recorded review.

- Required positive: Q.from_utc≤R.from_utc **и** Q.to_utc≥R.to_utc (inclusive).
- Кроме того, **один** adequate E должен покрывать весь Q: E.from_utc≤Q.from_utc
  и E.to_utc≥Q.to_utc. Wider Q разрешён только с explicit reviewed support, не по датам.
- Ordinary APPLICABLE source без REQUIRED entry: Q explicit KNOWN; adequate E покрывает
  Q. Нет required R, но это не automatic exemption от ordinary freshness.
- Ни одного adequate single E → research. Несколько intervals нельзя stitch/union,
  даже если их сумма могла бы покрыть R/Q. Порядок evidence не выбирает победителя.
- UNKNOWN required R при REQUIRED → input gap; UNKNOWN Q при applicable source →
  research. Malformed boundary/from>to → TYPE; valid partial/disjoint Q→research.
- As-of = явный degenerate interval from=to. Нет generated now/default TTL/max_age,
  online recency или time-zone conversion. Same bytes в другой день → тот же result.

Literal independent examples: R=[2026-11-01T00:00:00Z,2026-11-04T00:00:00Z].
Q=[2026-10-31T00:00:00Z,2026-11-05T00:00:00Z] с таким же поддержанным E покрывает R.
Q до 2026-11-03T23:59:59Z не покрывает R; Q начиная 2026-11-05T00:00:00Z disjoint.
E1=01..02 и E2=02..04 не заменяют single E=01..04. Никаких publication-date defaults.

## 5. RC-P04 — Integrity, recorded review, truth

| Layer | Exact proposed checks | Что positive result НЕ доказывает |
| --- | --- | --- |
| Structural integrity | Existing shape/ref/hash/DAG/provenance/currentness; source.subject in S; digest equality | Чтение материала, честность caller, scientific validity |
| Recorded human consideration | Evidence.source_ref==material_ref; Check.claim_ref==Evidence.claim_ref; KNOWN Check.evidence_refs содержит exact evidence; locator KNOWN; relation supports; Check supported/qualified; known matching material digest; single reviewed coverage covers Q/R | Правдивость statement/coverage, полноту научного review, реальную доступность/лицензию material |
| Factual/scientific truth | Не вычисляется pure evaluator | Никаких certifications, automatic reviewer identity/authority или external verifier |

Existing [ClaimCheck validation](../../story_intelligence/records_v1.py) требует
metadata только у reviewed states, qualification ровно у qualified и known nonempty
evidence у supported/qualified. Локальный premise не создаёт эти records и не меняет
state. Human связывает claim/evidence с subject Source через explicit bound assessment;
ClaimItem.statement не парсится для поиска дат/смысловой релевантности.

Missing exact ref/wrong claim-source relationship/digest mismatch — INVALID. Valid
unreviewed/disputed/insufficient evidence, UNKNOWN locator/material digest или empty
support → research, не fabricated support. KNOWN material hash mismatch → INVALID;
UNKNOWN material hash не заполняется supplied hash. No side-effect file read/fetch.
Publication/capture timestamps — лишь данные, не самостоятельный requiredness или
adequacy proof. Rights и explicit blocking Risk сохраняются; supported freshness не
означает truth/rights/ELIGIBLE при других gaps. Враждебный coherent caller способен
сфабриковать весь local input; hashes не криптографическая подпись reviewer.

Такое coherence/coverage сравнение реализуемо на existing SI/1 records + local value,
без schema changes/authority/scientific service. Это readiness подсистемы только после
approval RC; полнота base classifier рассматривается отдельно в
[READINESS_AUDIT](STORY_INTELLIGENCE_SI_E02_2_1D_READINESS_AUDIT.md).

## 6. RC-P05 — Exact diagnostics proposal and SI-PRODUCT-01

Все mappings ниже PROPOSAL. Existing Diagnostic={code,field_path,input_ref,message};
D01–D16 — documentary labels, не новые codes/fields. P=`$.required_current_premise`,
I=binding.idea_ref, S=exact subject Source ref. i/k/j — actual authored array indices.
Сообщения fixed, не конкатенация reason/specification/title/UUID/hash/unknown key.

| ID / condition | Existing code | field_path | input_ref | Fixed message | Class |
| --- | --- | --- | --- | --- | --- |
| D01 missing premise | EVIDENCE_NEEDED | P | null | Required-current determination is missing. | NEEDS_INPUT |
| D02 UNDETERMINED | EVIDENCE_NEEDED | P.determination | I | Required-current determination is unresolved. | NEEDS_INPUT |
| D03 required_data UNKNOWN/empty | EVIDENCE_NEEDED | P.required_data | I | Required data specification is missing. | NEEDS_INPUT |
| D04 item specification UNKNOWN | EVIDENCE_NEEDED | P.required_data.value[k].specification | S | Required source data are unspecified. | NEEDS_INPUT |
| D05 required period UNKNOWN | EVIDENCE_NEEDED | P.required_data.value[k].period | S | Required period is unspecified. | NEEDS_INPUT |
| D06 source assessment omitted | EVIDENCE_NEEDED | P.source_freshness | S | Source freshness review is missing. | NEEDS_RESEARCH |
| D07 applicability UNDETERMINED | EVIDENCE_NEEDED | P.source_freshness[i].applicability | S | Source freshness applicability is unresolved. | NEEDS_RESEARCH |
| D08 applicable UNKNOWN/INSUFFICIENT or inadequate E/Q | EVIDENCE_NEEDED | P.source_freshness[i].outcome | S | Source freshness evidence is insufficient. | NEEDS_RESEARCH |
| D09 applicable review_period UNKNOWN | EVIDENCE_NEEDED | P.source_freshness[i].review_period | S | Source review period is unspecified. | NEEDS_RESEARCH |
| D10 genuine context mismatch | INPUT_STALE | P.binding.context_snapshot | I | Evaluation context has changed. | STALE |
| D11 hash mismatch | REF_HASH_MISMATCH | Actual declared digest/material_sha256 field | S if coherent subject exists, else I | Exact content binding does not match. | INVALID |
| D12 wrong subject/claim/material role | PROVENANCE_MISMATCH | Actual source_ref/evidence_ref/check_ref/material_ref field | S if coherent subject exists, else I | Exact source or review binding is inconsistent. | INVALID |
| D13 duplicate source assessment/requirement | TYPE | Second item's source_ref | Duplicate exact S | A source entry is repeated. | INVALID |
| D14 malformed local premise | TYPE / MISSING_FIELD / UNKNOWN_FIELD / VERSION_UNSUPPORTED | Known failing path; unexpected key uses parent container path | null | Required-current premise is malformed. | INVALID |
| D15 SI graph/ref/invalid currentness | Accepted underlying code | Declared premise ref field if unique failing SIRef is identified; otherwise accepted API path; code-only currentness uses corresponding explicit root argument path | Validated failing/query ref if available, else null | Supplied references cannot be validated. | INVALID |
| D16 valid stale dependencies | INPUT_STALE | Corresponding explicit root argument path | Queried exact root ref | Evaluation dependencies have changed. | STALE |

D11 exact paths: P.binding.ratings_sha256, P.source_freshness[i].binding_sha256,
P.source_freshness[i].requirements_sha256, P.source_freshness[i].evidence[j].material_sha256.
D12: out-of-S→source_freshness[i].source_ref; Check.claim mismatch→...evidence[j].check_ref;
Evidence.source mismatch→...evidence[j].material_ref. Graph error normalization is proposed locally: if the failing exact SIRef identity
is uniquely identified in source-specific premise refs, normalize to its first path
in this exact priority: required_data.value[k].source_ref, then source_freshness[i].source_ref
and its evidence[j] refs (evidence_ref/check_ref/material_ref), arrays in authored order.
Repeated mentions inside binding/context are excluded from this shortcut; they use
accepted paths if no source-specific match exists. Preserve the accepted code. Otherwise preserve accepted
API path. No accepted validator changes or partial successful graph check.
Currentness API returns codes, not hidden ERef paths: main root k uses
`$.semantic_input_refs[k]`; explicit proof root uses its declared evidence/check/material
ref path; a dependency-boundary-only call uses `$.root`. Do not invent an underlying
ERef error path the API did not supply. Wrong SIRef role/hash/missing
record first diagnosed by underlying accepted API, not remapped to convenient research.

Missing data list emits D03; nonempty partial list emits D04/D05 for each applicable
item, not a redundant D03. Missing assessment emits D06, no fabricated D08 for missing
object. D09 and D08 can coexist (unknown period plus insufficient evidence); one D08
per assessment even with multiple failed supports. NOT_APPLICABLE well-formed item
emits none; REQUIRED contradiction or bad period/enum → D14/TYPE at actual field.

Validation order: SI/local shapes → exact graph/provenance → binding/coverage/role
checks → all relevant currentness results → eligibility. Existing validators retain
paths/order; local fields declared order, arrays authored order, unknown local keys
sorted for first failing container diagnostic. First fatal error by phase/traversal,
no accepted result; in currentness phase INVALID any root wins over STALE. No lower
eligibility claims from malformed input. Valid current inputs collect **all** D01–D09
and all established base/findings reasons before choosing R1 highest state.

Unique reason_codes sorted ASCII. Generated diagnostics unique by (code,path,C(ref),message),
sorted (class rank,code,path,C(ref),message exact Unicode), class order
BLOCKED→NEEDS_INPUT→NEEDS_RESEARCH→REVIEW_DUPLICATE. Class is condition, not code:
EVIDENCE_NEEDED legitimately represents either input or research in this proposal.

**SI-PRODUCT-01:** future Editorial Decision Projection must map these condition/path
families and static templates to human explanations («Не задан необходимый период»,
«Нужна проверка свежести источника»), resolving source labels only under a separate
privacy-aware presentation contract. Editor must not need SIRef/hash/internal code.
Projection/UI НЕ реализуются и не утверждаются здесь. Technical Diagnostic is private
internal value, not product text. No new machine code vocabulary required.

## 7. RC-P06 — Privacy and review choices

No persistence, implicit logs/telemetry/export, Request/Run/Report/Packet embedding,
request_id/replay, actual review identity claim, clock/network/LLM/GPU/provider.
Premise free text/specifications/source labels не входят в diagnostic message.
input_ref и accepted API paths могут раскрывать private identifiers/unknown key names:
не выводить/логировать raw diagnostics/exceptions автоматически. Local unknown-key
message/container path не копирует secret key. Accepted API exceptions не меняются;
future projection must whitelist/map, не просто render str(error). Internal technical
values передаются только caller в том же private memory boundary.

| Owner choice still NOT APPROVED | Exact recommendation / change |
| --- | --- |
| RC-P01 | §2 closed local schema, exact EvaluationBinding reuse, None vs malformed; без новых fields/simplification beyond avoiding redundant clocks |
| RC-P02 | §3 worklist/S, proof-only check boundary, duplicates/order; §4 combinations and missing coverage |
| RC-P03 | §4 inclusive Q⊇R plus one E⊇Q; replaces 1c equality; no stitching/TTL |
| RC-P04 | §5 coherent recorded support, insufficient vs invalid distinctions, explicit truth limits |
| RC-P05 | §6 D01–D16 exact static messages/paths/refs, all reasons/order and privacy handling |
| RC-P06 | §7 argument-only lifecycle, no implicit sinks, separate future product projection |

[TEST_ORACLES](STORY_INTELLIGENCE_SI_E02_2_1D_TEST_ORACLES.md) gives every C01–C34
and temporal/privacy additions. Все новые RC details/oracles NOT APPROVED.
**Unit tests: NOT RUN — DOCS ONLY.** RU/UA wire `ru/uk`, CPU-only/licensing gates,
EVAL-P05 OPEN, PUBLISH_REVISION DISABLED, partial COMMIT reconstruction OFF,
Windows S3.2b BLOCKED_HOST_NOT_PROVIDED. STOP; без реализации/PR/merge/release/main changes.
