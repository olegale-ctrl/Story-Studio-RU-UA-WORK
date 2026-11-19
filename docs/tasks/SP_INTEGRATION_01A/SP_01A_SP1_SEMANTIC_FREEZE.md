# SP/1 semantic freeze for review

**SP-INTEGRATION-01a · 2026-11-19 · DOCS_ONLY · FREEZE_FOR_REVIEW, NOT OWNER_APPROVED.**

This freeze pins observed semantics at candidate8f0b4de; it is **not approval of SP/1**. Version remains `SP/1-PROPOSAL`, policy `SP-REVIEW-ONLY/1`. No existing schema, function, G3 or MVP08B rule is modified. Owner must explicitly approve a bounded diagnostic interpretation or authorize a later reconciliation task. Final release verifier remains absent.

|Rule|Exact function / JSON fields|Existing test / fresh vector|Observed invariant|Approval status|
|---|---|---|---|---|
|SF01 transport boundary|prepare_intent, VERSION; all schemas schema_version|test_absent_dispatcher_never_direct_render; FV01–04/FV26|Diagnostic transport only; not JobStore payload, PG envelope, trusted identity, execution grant, rights proof or release grant|PROPOSAL; only review requested|
|SF02 independent axes|initial_readiness, assess_release; six named axis fields|test_render_intent_never_grants, test_boolean_axis_rejected; FV11–19|Exact string unknown/false/true; unknown≠true; no CLI boolean promotion|PROPOSAL, no authority granted|
|SF03 SI separation|initial_readiness, assess_release; si_eligible vs facts_reviewed|test_si_does_not_clear_facts; FV18|SI eligibility cannot set factual truth/review|PROPOSAL; preserves existing boundary|
|SF04 no diagnostic release|initial_readiness, assess_release, run_gates; release_allowed|test_even_all_assertions_are_not_authority; FV24/FV27|Returned false; readiness/report/gate schemas forbid true|PROPOSAL; independent verifier required for any future change|
|SF05 local intent digest|prepare_intent; intent_sha256|test_repeat_intent_deterministic_not_submitted,test_stale_sha_and_policy; FV01H–04H/FV10|Local deterministic comparison only, not job ID/acceptance/PG binding/execution-idempotency guarantee|PROPOSAL; no identity mapping approved|
|SF06 intermediate gates|run_gates; status,phase,technical_pass|test_intermediate_not_final_technical_pass,test_final_incomplete; FV23/FV27|INTERMEDIATE_CHECKS_PASS≠TECHNICALLY_PASS; actual technical_pass stays unknown; final blocked|PROPOSAL; qualified worker contracts absent|
|SF07 fallback|prepare_intent, assess_release; fallback_class/blockers|test_equivalent_needs_evidence,test_degraded_without_policy,test_placeholder_production; FV20–22/FV28–30|none/equivalent/degraded/placeholder only; equivalent never auto-qualified; degraded release denied; production placeholder blocked|PROPOSAL; no substitution authorization|
|SF08 asserted conditions vs authority|assess_release; necessary_conditions_satisfied, release_allowed|test_even_all_assertions_are_not_authority; FV24/G04|Necessary flag evaluates supplied assertions only; cannot authenticate evidence/actor/currentness or publish|PROPOSAL; not complete readiness validation|
|SF09 draft restrictions|prepare_intent, assess_release; mode|test_a_defaults_draft,test_a_production_blocked,test_draft_no_gates_bypass; FV05/FV25|A default draft; A production policy blocker; draft not execution authorization or gate bypass|PROPOSAL; no Class A production policy|
|SF10 flag intent only|prepare_intent, initial_readiness; requested_attestations|test_render_intent_never_grants; FV26|render/facts/rights switches request attestation but all axes remain unknown|PROPOSAL; attestation verifier missing|

Axis names: `script_ready`, `facts_reviewed`, `rights_cleared`, `authorized_for_render`, `technical_pass`, `authorized_for_release`. Owners/evidence/change rules remain the proposals in SP_INTEGRATION_01/READINESS_AND_RELEASE_POLICY.md; no actors or authority registry are appointed by this freeze. Render and release are separate scopes; changing SHA/policy requires future applicability verification, not just equality testing.

## Exact digest domain

Body fields in prepare_intent: schema_version,policy_version,route,mode,fallback_class,inputs,requested_attestations,proposed_job_types. Its digest excludes the output's intent_sha256,status,blockers,accepted_job_ids. Existing SI canonical primitive supplies strict bounded UTF8 JSON (no floats, sorted keys, compact separators, no Unicode normalization). Fresh vectors independently recompute hashes with hashlib and explicit encoding for these bounded fixtures. Equivalent input dict insertion orders do not create separate jobs; **no job exists here**. Raw artifact SHA, PG own-binding domain prefix, SI record identity and proposed MVP08B JCS-LOCAL-1 are separate domains. No reinterpretation/substitution is approved.

## Seven schemas inspected

|Schema|Required interpretation|Gap / semantic validation beyond shape|
|---|---|---|
|route.schema.json|Route/mode/local digest, always BLOCKED_DISPATCHER_CONTRACT|Cross-artifact equality not checked by schema|
|readiness.schema.json|Six tri-state axes; separate SI; release false; evidence/bindings declarations|Evidence validity/currentness/authority not proven; G02 typed-reference lexical risk|
|jobs.schema.json|NO_APPROVED_JOBSTORE_API; empty accepted IDs and observations|Not a local authoritative status mirror|
|artifact_manifest.schema.json|Diagnostic declared observations; storage publication blocked|No protected storage receipt or PG typed binding|
|job_intent.schema.json|Prepared declaration, seven proposed job labels; no accepted jobs|G01 cross-field/hash invariants; G02 LF; G03 semantic plan/path checks|
|technical_gate_report.schema.json|Partial checks; technical_pass unknown; release false|Image/clip/MP4 decoder/tool evidence and final publication missing|
|production_readiness_report.schema.json|Supplied-assertion diagnostic, release false|G04: necessary flag is not whole-readiness/schema verification|

All seven top-level schemas reject unknown properties and require their declared fields. This does not imply nested plan extra keys are rejected or semantic constraints are complete. No schema alone proves rights, currentness, trust or actual execution.

## Contract gap register — no in-place fixes

|ID|Exact observed mismatch / scope gap|Disposition|
|---|---|---|
|G01|job_intent schema accepts topic input with route D, empty stages and zero digest; prepare_intent produces coherent values but no general imported-intent semantic verifier exists|Strict interchange approval withheld; require future cross-field/stage-order/digest verification decision|
|G02|Schema pattern `^[0-9a-f]{64}$` accepts64 a characters plus final LF; runtime validate_materials uses fullmatch and raises ValueError. Similar `$`-anchored UUID/ref patterns require review, not assumed fixed|Exact hash syntax cannot be certified by schema alone; no wire/schema patch authorized here|
|G03|Schema admits scene text single space/image ../x.png; validate_plan rejects. This weaker structural layer was partly documented already|Require runtime semantic validator after shape checks; schema-only acceptance rejected|
|G04|assess_release can return necessary_conditions_satisfied=true for six asserted axes+policy/fallback/blockers without a complete readiness-schema object/evidence|Keep explicitly diagnostic; no authority or release implication, no claim full readiness validation|

These gaps do not create release_allowed=true or an execution path in the reviewed version. They do prevent declaring seven schemas equivalent to runtime validation or treating the local digest as trusted acceptance. P0 owner options are in the dossier; **no chosen option recorded**.
