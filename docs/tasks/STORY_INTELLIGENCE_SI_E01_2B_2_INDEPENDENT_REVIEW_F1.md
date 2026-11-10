# SI-E01.2b.2 — independent static review, F1 blocking contract discrepancy

**Date:** 2026-11-10
**Verdict:** **CHANGES_REQUIRED / F1 / NOT ACCEPTED YET**.
**Feature:** `feat/story-intelligence-si-e01-2b-2-pure-provenance` @ `9a2999bae72b1d6bd6784e7df305f59dea1bfd2e`.
**Exact base:** `112ebd76b2a08fc2ba44cfcd53a3a2c8979f832c`.
**Evidence:** independent GitHub static review; **no independent Python test execution**.

## Publication verification

Feature remote HEAD equals the supplied SHA. Base→feature: one commit ahead, zero behind; exactly four allowed newly added files, **583 additions, 0 deletions**: `story_intelligence/provenance_v1.py`, `tests/test_story_intelligence_provenance_v1.py`, `tests/test_story_intelligence_provenance_vectors_v1.py`, `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_2_RESULT.md`. Existing files and accepted literal vectors unchanged by this diff. `main` observed at `e1f4efb0fb5ff290bb198349213c004b4667ef0f`; no feature PR, commit statuses or PR-triggered workflow runs detected. Codex reports Linux/Python 3.12.14 **15 provenance, 100 SI and 942 full tests passing** (zero skipped; no independent rerun). `diff --check`, clean worktree and exact SHA are Codex-reported, not independently executed.

Reviewed complete `provenance_v1.py`, provenance graph tests, literal-vector test method and generator/report, approved R1 §3.1 and R1a §4, local `records_v1.py` checks and the prior accepted resolver. The module delegates exact hash/DAG/snapshot verification to the accepted resolver, enforces actual run stage/method/version and history chains, detects reused ancestral revision runs, checks exact HUMAN_EDIT direct roots and original CREATIVE Run retention K1→K2→K3. Genuine positive and negative hash-consistent graph tests are present.

## F1 — missing exact EvaluationReport Rubric binding (blocking)

**Binding contract:** `docs/tasks/STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md` §3.1 states **“Payload.run_ref = H.origin.run_ref; rubric/method refs совпадают с RunRecord.”** For an EvaluationReport with `payload.run_ref = H.origin.run_ref = E`, the actual EVALUATION RunRecord `E.payload.rubric_ref` must match the report's `payload.rubric_ref` exactly.

**Observed code gap:** `provenance_v1.py` `generator(...)` checks `(stage, method_id, method_version)` for EVALUATION, but nowhere compares `EvaluationReport.payload.rubric_ref` with that generating Run's `payload.rubric_ref`. Accepted `records_v1.py` only compares `EvaluationReport.payload.run_ref` to `H.origin.run_ref` and requires EVALUATION RunRecord.rubric_ref to be non-null; the resolver follows exact SIRef edges but does not certify equal rubric binding.

**Minimal conceptual counterexample:** valid exact Rubrics A and B (distinct actual refs); a valid EVALUATION Run with `rubric_ref=A`, stage `EVALUATION`, method `si.evaluate/1-r1`, self-consistent semantic inputs/input_snapshot; its immutable EvaluationReport with `run_ref=E`, `H.origin.run_ref=E`, **`rubric_ref=B`** and newly calculated correct record/root hash. Both rubric records and full audit ancestors are in the explicit bundle. The accepted resolver sees a consistent DAG; the new verifier would also accept, because it does not check A==B. This is a source-derived static counterexample, **not a separately executed reproducer**. The violated equality is unambiguous, cross-record, and already in the approved scope of provenance consistency.

**Required fix:** compare exact SIRefs on actual generating EVALUATION Run and report. On mismatch throw existing `SIValidationError('PROVENANCE_MISMATCH', '$.records[i].payload.rubric_ref', ...)`; no coercion, latest fallback, or new codes. Add at least one **true hash-consistent** negative graph where the **accepted resolver passes first**, then `verify_si_provenance` rejects the mismatch at the expected path. Ensure positive matching rubrics and inputs/outputs remain valid; regressions across all new and historical suites.

No widening into rubric weights/eligibility/evidence scoring, semantic currentness, Request execution, rights, ERef adapter, source grants or other R1 operation root inference. Other future-stage boundaries remain separately gated. Avoid replacing original source tests or literal vectors.

## Decision and STOP

**SI-E01.2b.2 is NOT ACCEPTED until F1 is fixed and independently reviewed.** SI-E01.2b.1 remains ACCEPTED / PURE_RESOLVER_ONLY; this finding does not revoke previous acceptances. Fix in a fresh, narrowly bounded F1 feature branch from exact `9a2999bae72b1d6bd6784e7df305f59dea1bfd2e`; do not alter the published feature branch, main, original contracts, resolver or existing literal vectors.

STOP: no SI-E01.2b.3, SI-E02, implementation of RFC, PR/merge/release, editorial/storage changes. `PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF; S3.2b BLOCKED_HOST_NOT_PROVIDED.
