# SI-E02.2.1e — Independent full T25 conditional oracle

Дата: 2026-11-12 (Europe/Kyiv).
**CONDITIONAL — OWNER APPROVAL REQUIRED (Q1/Q2/Q3). NOT RUN.**
Base: `1c4724da06c087374ac5a7098554760d5752f9fd`.
[RC approval](STORY_INTELLIGENCE_SI_E02_2_1E_RC_OWNER_APPROVAL_2026_11_12.md) не
утверждает [base decision proposal](STORY_INTELLIGENCE_SI_E02_2_1E_BASE_CLASSIFIER_DECISION_PROPOSAL.md)
и этот T25 oracle. Ниже complete independently authored **parameterized fixture and
expected tuple list**, не fabricated golden SHA values и не результат future evaluator.

## 1. Scope and assumptions selected for this oracle

Используются recommended Q1-A/B/C, Q2-A/C alternative A и Q3-A/B/R.
Generic SCIENTIFIC blocking Risk имеет EVIDENCE_NEEDED/class BLOCKED согласно Q2-C
(**NOT APPROVED**). Required-current UNDETERMINED→NEEDS_INPUT — уже EVAL-F02;
UNKNOWN rating→NEEDS_RESEARCH и unresolved exact pair→REVIEW_DUPLICATE уже установлены.
Exact base messages/paths pinning и полномочия Q1/Q3 applicability ещё conditional.

Здесь нет missing mandatory SI fields, malformed premise, graph corruption, STALE,
claims review conflict, rights/capability subtype, private export или future Creative/
Selection/Brief. Источник один, declared ordinary freshness NOT_APPLICABLE. Единственный
NEEDS_RESEARCH trigger — UNKNOWN **rating value**, не hidden general research policy.
Это позволяет перечислить полный reason/diagnostic set, а не «как минимум четыре».

## 2. Complete synthetic graph template (11 records)

Symbols below mean actual exact SIRefs generated from independently authored bytes,
не strings/aliases, переданные accepted validators. Canonical hashes строятся позже
independent stdlib JSON/SHA256 до запуска engine; **новые golden vectors здесь не нужны**.
Никакой будущий evaluator не используется для получения ожидаемых values/refs/outcomes.

### Headers and identity rules

Record index n=0..10: id=`{n+1:08x}-2222-4222-8222-222222222222` в lowercase;
H.si_version=1, H.type=table type, revision=1, previous=null, created_at=2026-11-12T00:00:00Z,
editorial_refs=[]. No UUID/time calls: fixed fixture identities/descriptive times.
Manual records: creator_label="Fixture author", origin={mode:MANUAL_INPUT,run_ref:null,
imported_from:null}; H.input_refs=direct payload SIRefs в approved schema order.
StoryIdea records: creator_label="SI_ENGINE", RULE_DERIVED with respective Run,
imported_from=null, H.input_refs=[T,S]. Run records: SI_ENGINE/RUN_METADATA, no run_ref/
imported_from, H.input_refs=canonical Closure([T,S]). Every reference gets the exact
SHA256(C(H+payload)); no fake all-zero digest, no circular output linkage.

### Payload table (all required fields specified)

K(x)=KNOWN(value=x), U(x)=UNKNOWN(reason=x). A Text listed below is literal fixture data,
not a keyword for policy inference. All UTC strings end with Z; wire locale **ru**.

| index / symbol / type | Exact payload |
| --- | --- |
| 0 / T / Intake | input_kind=TOPIC; raw_input="Synthetic science topic"; locale=ru; supplied_source_refs=[]; user_goal=K("Synthetic editorial exercise") |
| 1 / S / SourceItem | source_kind=LOCAL; original_locator="synthetic:material"; title=K("Synthetic material"); author=K("Fixture"); publisher=K("Fixture"); published_at=captured_at=K("2026-11-01T00:00:00Z"); material_sha256=SHA256(raw bytes `synthetic fixture material`) wrapped K; editorial_ref=null; rights_note=K("Synthetic fixture; not a licence"); freshness_requirement=U("Review pending") |
| 2 / RD / RunRecord | DISCOVERY payload defined below, semantic_input_refs=[T,S] |
| 3 / I / StoryIdea | intake_ref=T; title="Synthetic science topic"; summary="Synthetic editorial premise"; viewer_question="What remains uncertain?"; source_refs=K([S]); candidate_binding=null; origin Run RD |
| 4 / RP / RunRecord | Separate DISCOVERY payload below, roots=[T,S], same closed discovery options |
| 5 / P / StoryIdea | intake_ref=T; title="Synthetic portfolio topic"; summary="Prior synthetic premise"; viewer_question="What was previously considered?"; source_refs=K([S]); candidate_binding=null; origin Run RP |
| 6 / AU / AudienceHypothesis | locale=ru; region=K("Fixture region"); knowledge_level=K("General"); motivation=K("Learning"); interests=K(["Science history"]); age_range=K("Adults"); basis_refs=[T]; assumptions=["Synthetic editorial hypothesis, not audience statistics"] |
| 7 / H / ChannelContext | channel_alias="Fixture channel"; purpose="Science history"; audience_ref=AU; constraints=[]; portfolio=K([entry0 defined below]); analytics=K("Synthetic hypothesis, not measured statistics"); capability_notes=K("CPU-only editorial planning; not measured execution") |
| 8 / A / Angle | idea_ref=I; audience_ref=AU; question="What remains uncertain?"; thesis="Synthetic editorial premise"; claim_refs=[]; distinction="Human comparison pending"; limitations=[] |
| 9 / G / Rubric | method_id="si-rubric"; method_version="1"; blocker_policy_version="1"; missing_policy=ALL_REQUIRED; nine criteria below |
| 10 / R / Risk | category=SCIENTIFIC; severity=HIGH; blocking=true; basis_refs=[A]; description="Synthetic explicit scientific risk"; mitigation="Review remains pending"; resolution=OPEN; resolution_basis_refs=[]; owner_role="Fixture editor" |

U(x) is UNKNOWN union notation; AU is the exact Audience ref. No symbol spelling
is passed as a SIRef.

Run payload for RD and RP: stage=DISCOVERY, method_id="si.discover-local",
method_version="1-r1", semantic_input_refs=[T,S], input_snapshot=Closure([T,S]),
context_snapshot={context_version:1,active_input_refs:[],selection_head_refs:[],
editorial_snapshot_sha256:U("No editorial snapshot")}, editorial_snapshot_sha256 equal
that Known value, rubric_ref=null, provider=null, started_at=finished_at=
2026-11-12T00:00:00Z, confidence={level:HIGH,basis:"Synthetic fixture"},
fresh_trends=U("No live trends"), caveats=["Synthetic fixture, not executed discovery"].
request_payload_sha256 independently equals D({portfolio_ref:null}) for both Runs,
using the existing closed DISCOVER_LOCAL options. These are synthetic descriptive
metadata, **not a real Request/idempotency or executed operation proof**. No new
Request field/version or DISCOVER call is claimed.
Run has no output backlinks. StoryIdea H origin rules above provide the exact linkage.

Portfolio entry0: story_ref=P, published_title="Synthetic portfolio topic",
published_locator=K("synthetic:portfolio"), published_at=K("2026-11-01T00:00:00Z"),
angle_notes="Comparison pending", basis_ref=T. Human comparison UNRESOLVED regardless
of normalized title similarity; there is exactly one required local pair.

Rubric criteria in approved order: audience_interest:15, channel_fit:10, angle_novelty:10,
evidence_quality:20, narrative_potential:15, visual_feasibility:10, resource_fit:10,
risk_manageability:5, portfolio_distinctness:5 (key:weight_percent). Each criterion description="Synthetic
criterion", min=0, max=5, direction=HIGH_IS_BETTER. Total weight100; no alteration to SI-D04.

## 3. Explicit evaluation inputs and local premises

semantic_input_refs=[I,A,AU,H,G,R]. observed_active_input_refs=unique canonical tuple-sorted
[T,S,I,P,AU,H,A,G,R]; selection_head_refs=[]. This is authored fixture order, no runtime
normalization. Every producer/previous dependency is supplied. Main C claim set empty;
applicable explicit Risk set={R}; main source S set={S}, including portfolio provenance.
No ERefs anywhere. No hidden scientific judgment inferred from A.thesis/R.description.

Ratings exactly nine in Rubric order. For k=0 (audience_interest):
value=U("Rating not supplied"). For k=1..8: value=K(5).
For every rating: basis_refs=[AU,A], explanation="Synthetic supplied rating",
confidence={level:HIGH,basis:"Synthetic judgement, not a probability"}.
No UNKNOWN confidence, so confidence_findings=[]; UNKNOWN value **remains UNKNOWN**.

Context C={context_version:1,active_input_refs:observed_active_input_refs,
selection_head_refs:[],editorial_snapshot_sha256:U("No editorial snapshot")}.
Bv={idea_ref:I,angle_ref:A,audience_ref:AU,channel_ref:H,rubric_ref:G,
semantic_input_refs:[I,A,AU,H,G,R],context_snapshot:C,ratings_sha256:D(ratings)}.
HumanFindingsInput={contract_tag:"si-evaluate-findings/proposal-1",binding:Bv,
confidence_findings:[],duplicate_findings:[{
 binding_sha256:D(Bv),portfolio_entry_index:0,portfolio_entry_sha256:D(entry0),
 candidate_ref:P,outcome:UNRESOLVED,reason:"Comparison pending"}]}.

Separate RequiredCurrentPremise={contract_tag:"si-required-current/proposal-1",binding:Bv,
determination:UNDETERMINED,required_data:U("Scope not specified"),source_freshness:[{
 binding_sha256:D(Bv),requirements_sha256:D({determination:UNDETERMINED,
 required_data:U("Scope not specified")}),source_ref:S,applicability:NOT_APPLICABLE,
 review_period:U("Not applicable"),outcome:UNKNOWN,evidence:[],reason:"Scope considered"}]}.
These exact local types are approved; no fields added to existing HumanFindingsInput.
No source freshness gap inferred merely from SourceItem.freshness_requirement UNKNOWN.

Preconditions before eligibility must actually pass future accepted validators,
resolver/provenance/currentness and local binding checks. No graph/currentness success
is being claimed from an executed fixture today. Headers/payloads are a full independently
authored construction specification; tests must instantiate exact refs, not aliases.

## 4. Complete independently specified expected result

**CONDITIONAL — OWNER APPROVAL REQUIRED for Q2-C alternative A, Q1 applicability and
Q3 field/profile policy.** No new output record or wire response schema is defined.
Conceptual pure result must carry:

- validation/currentness accepted CURRENT (future execution requirement, NOT RUN);
- primary eligibility **BLOCKED**, due explicit applicable R;
- aggregate_tenths=UNKNOWN(reason="At least one required rating is unknown.");
- reason_codes exactly **[DUPLICATE_REVIEW_NEEDED,EVIDENCE_NEEDED]**;
- exact **four** diagnostics below, in this order.

| order / condition class | code | field_path | input_ref | fixed message |
| --- | --- | --- | --- | --- |
| 1 / BLOCKED | EVIDENCE_NEEDED | $.records[10].payload.blocking | R | An explicit scientific risk remains blocking. |
| 2 / NEEDS_INPUT | EVIDENCE_NEEDED | $.required_current_premise.determination | I | Required-current determination is unresolved. |
| 3 / NEEDS_RESEARCH | EVIDENCE_NEEDED | $.ratings[0].value | G | A required rating is unknown. |
| 4 / REVIEW_DUPLICATE | DUPLICATE_REVIEW_NEEDED | $.human_findings.duplicate_findings[0].outcome | H | A portfolio comparison is unresolved. |

input_ref expands to the exact real SIRef from graph above, not its symbol spelling.
Ordering is class first, then code/path/C(ref)/message. A single EVIDENCE_NEEDED code
represents **three distinct conditions** in three classes; deduplicating reason_codes
must not collapse these diagnostics. No primary NEEDS_INPUT/REVIEW_DUPLICATE merely
because lexical code order differs; score does not override R.

Independent arithmetic: known eight ratings contribute 2×(100−15)×5=850. This is **not**
the aggregate. Aggregate UNKNOWN, not 850/0/renormalized1000. HIGH confidence is not a
value substitution or actual factual probability.

## 5. Normative versus conditional mapping

| Component | Already established | Still conditional |
| --- | --- | --- |
| Explicit open applicable blocker outranks all lower conditions | R1 priority | Which Risks applicable and generic SCIENTIFIC code/path/message: Q2-A/C |
| Required-current UNDETERMINED | EVAL-F02/approved RC D02 NEEDS_INPUT | Not permission to infer requiredness from Text |
| UNKNOWN required rating | SI-D04/R1: UNKNOWN aggregate and research | New literal rating diagnostic string/path pinned by Q3 proposal |
| UNRESOLVED exact portfolio pair | Approved EVAL-P03: duplicate-review gap | Literal nonmissing-pair message/path fixture under Q3 pinning |
| Context/main role sufficiency | Exact graph/provenance/currentness obligations | Q1 empty claim-set treatment and Q3 explicit essential-field/profile choices |

Owner may select another existing-code Q2 mapping; then this full expected set must
be revised **before implementation**, not auto-generated from engine. C14/C44 BX is
not used as finalized Q2 authority here: this oracle intentionally uses generic
scientific R to isolate the remaining category mapping choice. No new code introduced.

## 6. Bounded regression oracles (NOT RUN)

- If remove explicit Risk R from declared semantic/active scope in a new coherent
  fixture, primary NEEDS_INPUT; remaining three diagnostics survive. This is a new
  explicit hypothetical fixture, **not** permission to hide a real blocker.
- If replace UNDETERMINED by valid NOT_REQUIRED in a new matching premise, primary
  remains BLOCKED with input diagnostic removed; research/duplicate remain.
- If supply rating0 K(5) and recompute human bindings, aggregate1000, primary still
  BLOCKED; no automatic R mitigation or duplicate resolution.
- If pair0 changes to DISTINCT with exact matching human input, only duplicate
  diagnostic disappears; no risk/current-data clearance.
- Missing/corrupt R/ref/producer must be INVALID before any accepted eligibility;
  new observed context with intact old binding is STALE, not auto-rehash.
- Inputs exact bytes unchanged, repeated calls deterministic/detached; messages never
  echo private reason/IDs/hashes. Future product projection explains four conditions
  without exposing technical identifiers; UI not implemented.

No test executed, no golden vector generated, no real material/identity/rights or
scientific certification. **Unit tests: NOT RUN — DOCS ONLY.**
EVAL-P05 OPEN; PUBLISH_REVISION DISABLED; partial COMMIT reconstruction OFF;
Windows S3.2b BLOCKED_HOST_NOT_PROVIDED. STOP; no implementation/PR/merge/release/main changes.
