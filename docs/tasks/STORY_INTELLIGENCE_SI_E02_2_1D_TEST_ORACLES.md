# SI-E02.2.1d — Final proposed independent oracles

Дата: 2026-11-12 (Europe/Kyiv).
**PROPOSAL / NOT APPROVED / NOT RUN. No golden vectors required or manufactured.**
Base: `1fa37fa03b0dfb0a6ed754ddf70e9665c5a91eb0`.
[Final proposal](STORY_INTELLIGENCE_SI_E02_2_1D_REQUIRED_CURRENT_FINAL_PROPOSAL.md)
определяет все schemas/predicates/diagnostics D01–D16. D labels — documentary aliases
для полного tuple (code,path,input_ref,fixed message,class), не новые wire codes.
Ни один row не утверждён как test artifact; F/Existing отмечают лишь normative
primary rule, RC — детали, требующие approval. Tests/evaluator не запускались.

## 1. Exact parameterized fixture notation

Независимый fixture builder будущего implementation должен дать genuine records и
content-addressed SIRefs, не mock hashes. Символы здесь — **parameters templates**,
не допустимые string SIRefs. Expected outputs authored здесь, не получены из engine.
C/D canonical primitives — independent stdlib JSON/SHA-256 при построении fixtures;
их буквальные expected digests позднее фиксируются до implementation, не из evaluator.

- B: complete valid/current input bundle, no unrelated gaps/blockers/duplicates;
  nine known ratings5/HIGH (aggregate1000); KNOWN empty portfolio, approved findings;
  one main Source S, roots ordered Idea I,Angle,Audience,Channel,Rubric,S. Source-level
  Unknown freshness_requirement допускается, source metadata не human premise.
- Binding Bv = exact EvaluationBinding этих inputs, expected=observed ContextSnapshot.
  Каждая changed fixture перестраивает все genuine downstream refs и manifests, Bv
  и correct premise digests, если case не указывает deliberate mismatch.
- R=[2026-11-01T00:00:00Z,2026-11-04T00:00:00Z], W=[2026-10-31T00:00:00Z,2026-11-05T00:00:00Z].
- U: exact local tag, binding=Bv, determination=UNDETERMINED, required_data=UNKNOWN
  reason="Scope not specified", source_freshness=[NA(S)].
- N: same tag/binding, NOT_REQUIRED, required_data=KNOWN[], source_freshness=[NA(S)].
- K: REQUIRED, required_data=KNOWN[{source_ref:S,specification:KNOWN("Synthetic data scope"),
  period:KNOWN(R)}], source_freshness=[OK(S,R,R)].
- NA(S): correct binding/requirements digests, source_ref=S, NOT_APPLICABLE,
  review_period=UNKNOWN reason="Not applicable", outcome=UNKNOWN, evidence=[],
  reason="Scope considered".
- OK(S,Q,E): correct digests, source_ref=S, APPLICABLE, review_period=KNOWN(Q),
  outcome=ESTABLISHED, evidence=[P(S,E)], reason="Scope considered".
- X(S): correct digests, S, APPLICABLE, review_period=KNOWN(R), outcome=UNKNOWN,
  evidence=[], reason="Review pending".
- P(S,E): real Evidence e / ClaimCheck c / material Source m, exact fields evidence_ref=e,
  check_ref=c,material_ref=m,material_sha256=m.payload.material_sha256.value,coverage=E.
  e.source_ref=m, c.claim_ref=e.claim_ref=Claim q, c.evidence_refs=KNOWN[e], relation=supports,
  locator=KNOWN("Section 1"), c.state=supported with valid metadata. Subject S human
  binding is explicit in OK; no parsing q.statement. All support roots current;
  e/c/m proof-only unless case explicitly places main semantic path to m.
- input_ref symbols I/S/T/c/m are exact refs resolved in that fixture; actual UUID/hash
  spellings stay internal. All unexplained Known union UNKNOWN reasons use literal
  "Review pending". Field order follows declared schema, authored arrays canonical.

For cases with base Risk/rights use an explicit extended B: material Visual at
records[8] REQUIRED, rights_state=UNKNOWN/fallback=UNKNOWN; Risk at records[9]
LEGAL/blocking=true/OPEN with basis_refs to that Visual. Caller explicitly supplies
this as an essential-rights blocker; context/root hashes rebuilt. Expected base
diagnostic BX=(RIGHTS_BLOCKED,$.records[8].payload.rights_state,VisualRef,
"Essential material rights are unresolved.",BLOCKED) is a **proposed BC02/BC05 mapping**,
not established by RC approval. See readiness audit; these rows cannot certify classifier.

## 2. Every original C01–C34 (exact delta from templates)

All diagnostics below expand D definitions in final proposal; explicit i=0/k=0/j=0
unless stated. Lists are complete for stated B premises. Codes are lexical unique
union, diagnostics sorted by prescribed class/code/path/ref/message. Empty list means
no additional condition; complete ELIGIBLE requires all B assumptions.

| ID | Exact premise delta / graph condition | Expected primary; reason_codes | Exact diagnostic selectors (paths/ref/messages expand D table) | Status / existing requirement |
| --- | --- | --- | --- | --- |
| C01 | U; B | NEEDS_INPUT; [EVIDENCE_NEEDED] | D02 P.determination / I | F02 primary; RC structure/code; N02/T25 |
| C02 | K required_data=UNKNOWN; separately KNOWN[], assessment=X(S) | NEEDS_INPUT; [EVIDENCE_NEEDED] | D03 P.required_data/I; D08 P.source_freshness[0].outcome/S | F02; RC missing representation; T25 |
| C03 | K required_data.value[0].period=UNKNOWN, assessment=OK(S,R,R) | NEEDS_INPUT; [EVIDENCE_NEEDED] | D05 P.required_data.value[0].period/S | F02; RC period/detail; T25 |
| C04 | K assessment=X(S) | NEEDS_RESEARCH; [EVIDENCE_NEEDED] | D08 P.source_freshness[0].outcome/S | F02 primary; RC adequacy; T24 |
| C05 | K unchanged with genuine support | ELIGIBLE_FOR_CREATIVE; [] | none | R1/F02 absence of gap; RC concrete adequacy; N02/T02 |
| C06 | N unchanged | ELIGIBLE_FOR_CREATIVE; [] | none | F02; RC applicability encoding; T22 |
| C07 | N assessment=X(S), Source freshness_requirement=UNKNOWN | NEEDS_RESEARCH; [EVIDENCE_NEEDED] | D08 P.source_freshness[0].outcome/S | F02; RC diagnostic; T24 |
| C08 | None premise; B | NEEDS_INPUT; [EVIDENCE_NEEDED] | D01 P/null | F03 primary; RC None/code; T25 |
| C09 | Remove required_data key from N | INVALID; [MISSING_FIELD] | D14 P.required_data/null | F03 failure; RC field; T34 |
| C10 | N assessment=NA(T), T genuine but not main S; context otherwise B | INVALID; [PROVENANCE_MISMATCH] | D12 P.source_freshness[0].source_ref/T | F03 binding principle; RC S; T18 |
| C11 | Genuine old K/S/Bv; observed context now selects S2 (new Source revision), historical graph intact | STALE; [INPUT_STALE] | D10 P.binding.context_snapshot/I | Existing R1/G01; RC wrapper; T17/T19 |
| C12 | K frozen context A; observed context B with additional valid active ref, all graph valid | STALE; [INPUT_STALE] | D10 P.binding.context_snapshot/I | Existing/EVAL-P04; T38 |
| C13 | S={S1,S2} ordered, REQUIRED list only S1; assessments [OK(S1,R,R),X(S2)] | NEEDS_RESEARCH; [EVIDENCE_NEEDED] | D08 P.source_freshness[1].outcome/S2 | F02; RC independent coverage; T14 |
| C14 | U + explicit essential-rights fixture above | BLOCKED; [EVIDENCE_NEEDED,RIGHTS_BLOCKED] | BX at $.records[8].payload.rights_state/Visual; D02 P.determination/I | R1/F02 primary; BX base mapping NOT APPROVED; T23/T25 |
| C15 | S1 REQUIRED period UNKNOWN, S2 ordinary; [OK(S1,R,R),X(S2)] | NEEDS_INPUT; [EVIDENCE_NEEDED] | D05 P.required_data.value[0].period/S1; D08 P.source_freshness[1].outcome/S2 | F02/R1 priority; RC mapping; T24/T25 |
| C16 | Exact original EVAL-RESUME-G01 unchanged + U with source_freshness=[] | NEEDS_INPUT; [EVIDENCE_NEEDED] | D02 P.determination/I; D06 P.source_freshness/S | F02 explicitly approved primary; RC coverage; T25 |
| C17 | Exact original graph/ratings/findings, premise=None | NEEDS_INPUT; [EVIDENCE_NEEDED] | D01 P/null; no fabricated source diagnostics | F03; RC encoding; T25 |
| C18 | SG1 graph minus independent E→T1 branch; current Idea I2 HUMAN_EDIT replaces old source role with S3, all current main paths only S3; N assessment NA(S3); S1/S2 and I1 intact inactive audit | ELIGIBLE_FOR_CREATIVE; [] under B | none for S1/S2; graph/currentness still checked | Existing G01; RC S; T31 |
| C19 | N, root I2 HUMAN_EDIT actual producer Run has unresolved H.editorial_refs; rest valid | INVALID; [REF_MISSING] | D15 $.semantic_input_refs[0]/I2; code-only API, no fabricated ERef path | Existing F1-D1; T32/T33 |
| C20 | Boundary-only K3 query with relevant original C ERef; no new EVALUATE dependency | INVALID; [REF_MISSING] | D15 $.root/K3 | Existing G01/G02/F1-D1; T32 |
| C21 | Boundary-only K3, valid original C direct Claim Qa absent active, no ERef | STALE; [INPUT_STALE] | D16 $.root/K3 | Existing G02; T32 |
| C22 | Two K calls at different calendar dates; mutate detached output if mutable (otherwise check immutable return), inputs unchanged | Same ELIGIBLE_FOR_CREATIVE; []; exact input bytes unchanged | none; output detached | Pure task rule; implementation NOT RUN; T26/T35 |
| C23 | N; source.freshness_requirement UNKNOWN, NA(S) explicit | ELIGIBLE_FOR_CREATIVE; []; record metadata still UNKNOWN | none | F01/F02 no inference; RC positive scope; T22 |
| C24 | K OK(S,R,R) but evidence=[] | NEEDS_RESEARCH; [EVIDENCE_NEEDED] | D08 P.source_freshness[0].outcome/S | RC-P04 specific rule NOT APPROVED; T24 |
| C25 | K proof material_sha256 differs from KNOWN m digest | INVALID; [REF_HASH_MISMATCH] | D11 P.source_freshness[0].evidence[0].material_sha256/S | F03 failure principle; RC check; T07 |
| C26 | K graph-valid check unreviewed, or relation=insufficient, or locator UNKNOWN (separate subcases), no other adequate support | NEEDS_RESEARCH; [EVIDENCE_NEEDED] | D08 P.source_freshness[0].outcome/S once | RC-P04 adequacy; T29/T30 graph positive |
| C27 | K Q=R, only E=[2026-11-01T00:00:00Z,2026-11-03T23:59:59Z] | NEEDS_RESEARCH; [EVIDENCE_NEEDED] | D08 P.source_freshness[0].outcome/S | RC-P03/04; T24 |
| C28 | K required period from=2026-11-04T00:00:01Z, to=2026-11-04T00:00:00Z | INVALID; [TYPE] | D14 P.required_data.value[0].period.to_utc/null | RC temporal shape; T34 |
| C29 | Change K required R.to to 2026-11-05T00:00:00Z; deliberately retain old requirements_sha256 | INVALID; [REF_HASH_MISMATCH] | D11 P.source_freshness[0].requirements_sha256/S | F03 binding principle; RC digest; T36 |
| C30 | K append duplicate S assessment, byte-identical or opposite valid outcome (two subcases) | INVALID; [TYPE] | D13 P.source_freshness[1].source_ref/S | F03 conflicting principle; RC uniqueness; T05/T06 |
| C31 | Three separate K mutations: review_period=null; root unknown key; bad contract_tag | INVALID; respectively [TYPE], [UNKNOWN_FIELD], [VERSION_UNSUPPORTED] | D14 respectively P.source_freshness[0].review_period, P (container), P.contract_tag; ref=null | F03; exact local shape/privacy RC; T34 |
| C32 | K missing material record m (all declared refs retain exact valid shape) | INVALID; [REF_MISSING] | D15 P.source_freshness[0].evidence[0].material_ref/m (unique failed ref normalized to declared field) | Existing graph rule; not adequacy; T29 |
| C33 | U required_data=KNOWN[K requirement]; separately N required_data=UNKNOWN | INVALID; [TYPE] | D14 P.required_data/null | **RC-P02 only**, F01–F03 do not establish this exact combination rejection; T34 |
| C34 | K support m has relevant ERef, another root stale | INVALID; [REF_MISSING] | D15 P.source_freshness[0].evidence[0].material_ref/m | Existing INVALID/ERef priority; RC proof-root boundary; T33 |

P above expands `$.required_current_premise`. Every fixed message and ref/class is
specified by D table; BX is separately declared conditional base tuple. C32 uses the explicit proposed D15 unique-failing-ref normalization, not a fabricated
records array index. Nested failures without an identified declared ref preserve
accepted API paths. No claim of executed content-addressed fixtures is made.

## 3. Added independent temporal/privacy/coverage cases

| ID | Exact premise/source condition | Expected primary; codes; diagnostic path/ref | Approval status / existing requirement |
| --- | --- | --- | --- |
| C35 | K Q=W, single coherent E=W | ELIGIBLE_FOR_CREATIVE; []; none | RC revised inclusion, owner-approved task direction only, not final RC approval |
| C36 | K Q=[2026-11-03T00:00:00Z,2026-11-05T00:00:00Z], E=Q | NEEDS_RESEARCH; [EVIDENCE_NEEDED]; D08 P.source_freshness[0].outcome/S | RC partial overlap |
| C37 | K Q=[2026-11-05T00:00:00Z,2026-11-06T00:00:00Z], E=Q | NEEDS_RESEARCH; [EVIDENCE_NEEDED]; D08 same path/S | RC disjoint |
| C38 | K Q=R, E1=01T00..02T00 and E2=02T00..04T00 (November 2026 UTC), both individually coherent | NEEDS_RESEARCH; [EVIDENCE_NEEDED]; D08 same path/S | RC no interval stitching |
| C39 | K Q=W but E=R only | NEEDS_RESEARCH; [EVIDENCE_NEEDED]; D08 same path/S; wider Q not supported | RC explicit wider support |
| C40 | K Q=R; first E insufficient, second E=W fully coherent | ELIGIBLE_FOR_CREATIVE; []; none; evidence order reversal same result | RC any single adequate support, no first-match accident |
| C41 | K required period from=to=2026-11-04T00:00:00Z; Q/E include that boundary | ELIGIBLE_FOR_CREATIVE; []; none | RC inclusive degenerate interval |
| C42 | K required period=UNKNOWN and APPLICABLE Q=UNKNOWN/outcome=UNKNOWN/evidence=[] | NEEDS_INPUT; [EVIDENCE_NEEDED]; D05 period/S, D09 review_period/S, D08 outcome/S | F02 priority; RC multiple distinct diagnostics |
| C43 | K period boundary=2026-02-30T00:00:00Z or offset +02:00 or second=60 (separate subcases) | INVALID/[TYPE]; D14 actual malformed from_utc or to_utc/null | RC valid UTC seconds, no normalization |
| C44 | S1 adequate wider Q=W/E=W; S2 partial Q like C36; explicit rights blocker fixture | BLOCKED; [EVIDENCE_NEEDED,RIGHTS_BLOCKED]; BX + D08 P.source_freshness[1].outcome/S2 | R1/F02 primary, RC and BX mapping conditional |
| C45 | U.source_freshness[0].reason replaced by private names/tokens (only free Text; bindings remain valid) | NEEDS_INPUT; [EVIDENCE_NEEDED]; D02 fixed message exactly, no private Text in message | RC privacy; SI-PRODUCT-01 future projection |
| C46 | N has unexpected key whose name is a private credential-like string | INVALID/[UNKNOWN_FIELD]; D14 P/null; fixed malformed message, no key copy | RC safe unknown-key container path |
| C47 | K source_freshness=[] | NEEDS_RESEARCH; [EVIDENCE_NEEDED]; D06 P.source_freshness/S; no fake D08 | RC missing assessment vs malformed |
| C48 | N declares Source S as NOT_APPLICABLE yet outcome=ESTABLISHED | INVALID/[TYPE]; D14 P.source_freshness[0].outcome/null | RC contradictory assessment |

C45 uses SourceFreshness.reason; U has NA(S). All
fields remain exact closed schema. Diagnostic input_ref remains private internal
technical value; safe message is not permission to export raw diagnostics.
All temporal additions use reviewed coverage, not publication/capture timestamp.

## 4. Limits and readiness

[C original identities](STORY_INTELLIGENCE_SI_E02_2_1C_TEST_ORACLES.md) and original
EVAL-RESUME-G01 hashes remain unchanged; C16's primary NEEDS_INPUT is already F02,
not a new executed result. No new engine golden vectors or tests are claimed.
C14/C15/C44 demonstrate composition with explicit base premises, not classifier
extraction from arbitrary legal/scientific Text. BX and full T25 remain subject to
[readiness decisions](STORY_INTELLIGENCE_SI_E02_2_1D_READINESS_AUDIT.md).
Accepted 42 findings requirements/G01/G02/F1-D1 suites do not change. T27 future
Request integration remains non-executable for pure path; EVAL-P05 OPEN.

**Unit tests: NOT RUN — DOCS ONLY.** No implicit approval of RC tests/structures,
scientific truth, identity/rights/native qualification. STOP; no implementation,
PR/merge/release/main changes. PUBLISH_REVISION DISABLED; partial COMMIT reconstruction
OFF; Windows S3.2b BLOCKED_HOST_NOT_PROVIDED.
