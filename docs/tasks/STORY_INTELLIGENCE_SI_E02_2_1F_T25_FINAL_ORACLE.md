# SI-E02.2.1f — Final T25 contract

Дата: 2026-11-12 (Europe/Kyiv).
**APPROVED TEST REQUIREMENT / NOT RUN. NOT IMPLEMENTED.**
Base: `e64cedd73a11e2e69893639b9889795899ebea4c`.
Authority: [Q owner approval](STORY_INTELLIGENCE_SI_E02_2_1F_OWNER_APPROVAL_2026_11_12.md).

## 1. Exact fixture frozen by reference

The independently authored [SI-E02.2.1e T25](STORY_INTELLIGENCE_SI_E02_2_1E_T25_TEST_ORACLE.md),
exact Git blob `1fab899bfe065d8fe7fe7f3bfc653c47fc03544c` at the base, is the fixture
and expected-result source. Its §§2–3 **incorporated unchanged**: all headers/IDs,
11 payloads, producer Runs, full observed/root/context/ratings/local premise values,
canonical construction and genuine graph requirements. §§4/6 expected results and
bounded regression requirements are normative under the newly approved Q1/Q2/Q3.
Historical conditional wording is superseded for this scope; source file not edited.

No fixture bytes are recomputed by evaluator, no all-zero/fake SIRef hash, no producer
output backlink, no real Request/idempotency claim. Current task does not create
executable graph/code/new golden digests. Future tests must independently construct
exact canonical bytes and actual SHA-256 refs before calling evaluator.

Symbols below are **actual SIRefs from that construction**, not alias strings:

| Symbol | Source fixture index / role |
| --- | --- |
| I | records[3], current StoryIdea |
| H | records[7], ChannelContext with exactly one portfolio entry |
| G | records[9], Rubric profile (si-rubric,1,1) |
| R | records[10], SCIENTIFIC/HIGH/blocking=true/OPEN Risk, basis=[Angle A] |

The graph remains ERef-free with no main claims, Check conflict, Creative/Selection/
Brief or hidden required-source evidence gap. All main roots and graph checks must
actually pass future accepted validators/resolver/provenance/currentness; **not
claimed executed today**. Producer metadata is synthetic, not actual DISCOVER execution.

## 2. Four independent simultaneous conditions

1. Explicit applicable SCIENTIFIC OPEN blocking Risk R. Q2-C **alternative A** now
   selects EVIDENCE_NEEDED with condition class BLOCKED; no subtype inference.
2. Separate required-current premise determination=UNDETERMINED. RC D02 contributes
   NEEDS_INPUT; source ordinary freshness explicitly NOT_APPLICABLE, no extra source gap.
3. Exactly rating0 audience_interest.value=UNKNOWN, all nine confidence levels HIGH.
   No confidence finding is required; UNKNOWN value remains UNKNOWN/NEEDS_RESEARCH.
4. Exactly portfolio pair0 is human UNRESOLVED with full exact binding/entry digest.
   No future Selection/Topic Intent; this contributes REVIEW_DUPLICATE.

Other eight ratings remain KNOWN5. Independent known weighted contribution850 is
**not** aggregate. Aggregate UNKNOWN, not 850/0/renormalized1000. No score-based Risk
clearance, inferred source freshness or authenticated reviewer claim.

## 3. Normative exact expected result and deterministic order

Conceptual pure decision (not new SI/1 record/response schema):

- graph/currentness preconditions: valid and CURRENT, subject to real future test;
- primary eligibility: **BLOCKED**;
- aggregate_tenths: `{state:UNKNOWN,reason:"At least one required rating is unknown."}`;
- reason_codes: **[DUPLICATE_REVIEW_NEEDED,EVIDENCE_NEEDED]**;
- exactly four diagnostics below, in this order.

| order / condition class | code | field_path | input_ref | fixed message |
| --- | --- | --- | --- | --- |
| 1 / BLOCKED | EVIDENCE_NEEDED | $.records[10].payload.blocking | R | An explicit scientific risk remains blocking. |
| 2 / NEEDS_INPUT | EVIDENCE_NEEDED | $.required_current_premise.determination | I | Required-current determination is unresolved. |
| 3 / NEEDS_RESEARCH | EVIDENCE_NEEDED | $.ratings[0].value | G | A required rating is unknown. |
| 4 / REVIEW_DUPLICATE | DUPLICATE_REVIEW_NEEDED | $.human_findings.duplicate_findings[0].outcome | H | A portfolio comparison is unresolved. |

Literal tuples/paths/refs/messages unchanged from source. Ref symbols expand to its
exact generated type/id/revision/sha256, not human labels. Sort class rank first,
then code/path/C(ref)/message as approved. reason_codes are unique lexical ASCII;
three EVIDENCE_NEEDED conditions **must not collapse into one diagnostic**.
The diagnostics express blocker/input/research/duplicate independently.
No reordering for score or repeated code, no future implementation-based oracle changes.

Source bounded regressions also preserve exact conditions: explicit coherent fixture
without R → primary NEEDS_INPUT; complete NOT_REQUIRED premise removes only input
diagnostic; rating0 KNOWN5 yields aggregate1000 but Risk still BLOCKED; pair DISTINCT
removes only duplicate diagnostic. These hypothetical fixtures do not permit hiding
an actually applicable blocker. Invalid refs fail before eligibility; genuine changed
context STALE; inputs never mutated and repeated same inputs deterministic/detached.

## 4. BX reservation now resolved under approved Q2

These are **C14/C44**, not T25 R index10. Use the independently declared rights
fixture from [C01–C48 source](STORY_INTELLIGENCE_SI_E02_2_1D_TEST_ORACLES.md):
VisualRef8 at records[8] REQUIRED/unresolved rights/no usable documented replacement;
RiskRef9 at records[9] LEGAL/blocking=true/OPEN, applicable basis includes that Visual.
Actual exact refs/extra support records must be constructed, no fabricated aliases.

Both BX and generic LEGAL Risk are now normative (not alternatives to each other):

| ordered BLOCKED class diagnostics | code | field_path | input_ref | fixed message |
| --- | --- | --- | --- | --- |
| first (generic Risk) | EVIDENCE_NEEDED | $.records[9].payload.blocking | RiskRef9 | An explicit legal risk remains blocking. |
| second (specific BX) | RIGHTS_BLOCKED | $.records[8].payload.rights_state | VisualRef8 | Essential material rights are unresolved. |

Then C14 appends RC D02:
`(EVIDENCE_NEEDED,$.required_current_premise.determination,I,
"Required-current determination is unresolved.",NEEDS_INPUT)`.
C44 instead appends RC D08 for its specified insufficient Source2 coverage:
`(EVIDENCE_NEEDED,$.required_current_premise.source_freshness[1].outcome,S2,
"Source freshness evidence is insufficient.",NEEDS_RESEARCH)`.

Under the original cases' complete other premises: each composed set has three
diagnostics, primary BLOCKED, reason_codes [EVIDENCE_NEEDED,RIGHTS_BLOCKED]; their
original RC rating/temporal expectations remain unchanged. Generic LEGAL Risk does
not use RIGHTS_BLOCKED; specific unresolved Visual does. This resolves exactly the
reserved BX/base scope without rewriting history or inferring actual material rights.

## 5. Qualification, independence and STOP

This is an **APPROVED TEST REQUIREMENT**, not executed/passed test, literal golden
hash vector, real material/rights/science qualification or actual producer execution.
Independent executable fixture construction remains normal future test work. No
changes merely to make implementation pass; actual contradiction requires precise
reproducer/review, not replacement contract.

[Q3 product qualification](STORY_INTELLIGENCE_SI_E02_2_1F_OWNER_APPROVAL_2026_11_12.md)
limits essential knowledge_level/motivation/capability_notes to bounded EVALUATE;
early Discovery may retain hypotheses without being fully evaluated/production-ready.
KNOWN notes not actual CPU/tool proof. Future product projection explains conditions
without raw SIRef/hash/codes, not implemented here. RC/C01–C48/G01/G02/F1-D1/EVAL-P01–P04
preserved; EVAL-P05 OPEN and T27 deferred.

**Unit tests: NOT RUN — DOCS ONLY.** PUBLISH_REVISION DISABLED; partial COMMIT
reconstruction OFF; Windows S3.2b BLOCKED_HOST_NOT_PROVIDED.
STOP FOR INDEPENDENT REVIEW. No code/tests/PR/merge/release/main changes.
