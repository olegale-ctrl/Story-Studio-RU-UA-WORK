# SI-E01.2b.2-F1 — independent static acceptance and closure of SI-E01.2b.2

**Date:** 2026-11-10
**Decision:** **F1 ACCEPTED; SI-E01.2b.2 + F1 ACCEPTED / PURE_CROSS_RECORD_PROVENANCE_ONLY**
**Accepted fix:** `9785a84e95f99470e94a4c644606854428144df2`
**Fix base:** `9a2999bae72b1d6bd6784e7df305f59dea1bfd2e`
**Previous independent blocker:** `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_2_INDEPENDENT_REVIEW_F1.md` on `docs/story-intelligence-si-e01-2b-2-independent-review-f1` @ `8a055dae91d65cb00fa55abda24553b128fee413`.
**Evidence level:** Independent GitHub source/diff/tests/contract review; **no independent Python execution**.

## 1. Publication, exact scope, independent checks

- Fix remote HEAD equals exactly `9785a84e95f99470e94a4c644606854428144df2`; source feature remote HEAD equals exact fix base `9a2999bae72b1d6bd6784e7df305f59dea1bfd2e`.
- Compare base→fix: **ahead=1, behind=0; three allowlisted files, 218 additions, zero deletions**: `story_intelligence/provenance_v1.py` +2, `tests/test_story_intelligence_provenance_v1.py` +70, `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_2_F1_RESULT.md` new +146.
- `main` observed unchanged at `e1f4efb0fb5ff290bb198349213c004b4667ef0f`; no fix PR, commit statuses, or PR-triggered workflow runs observed.
- Production fix adds exactly two lines in `verify_si_provenance`: when reachable `EvaluationReport`, compare `p['rubric_ref']` with `run['payload']['rubric_ref']`; otherwise fail existing `PROVENANCE_MISMATCH` at exact `$.records[i].payload.rubric_ref`.
- The existing `generator(...)` has already checked actual EVALUATION stage/method/version, and the accepted resolver has already checked the exact SIRefs, hashes, reachability, DAG and Run snapshots. Guard neither rewrites refs nor adds coercion/latest fallback.
- Full independent inspection of three new F1 test methods: matching true Rubric case, distinct Rubric B case, same-id/new-revision Rubric B case. Negative cases rebuild legal content-addressed graph including original Run/Rubric, pass accepted `resolve_si_closure` before asserting the precise provenance-only mismatch/error path, and assert input immutability. New fixture uses real Rubric and REVISION Run for changed-revision case; no production hash/resolver mocks.
- Codex-reported red: 3 F1 methods, two expected failures before fix (old verifier accepted mismatch). Green: **3 F1, 18 provenance, 103 SI, 945 full unittest methods OK**, zero skipped/errors/failures. Environment Linux/Python 3.12.14; byte-identical previous 14 foundation, 18+3 record/value, 7 resolver, 9 provenance literal vectors; `git diff --check` and worktree clean Codex-reported. These were **not independently executed**; no GitHub CI PASS implied.
- This directly closes prior F1 violation of approved R1 §3.1: EvaluationReport.payload.rubric_ref must equal actual EVALUATION RunRecord.payload.rubric_ref. The reported/red-green cases and independent source check agree.

## 2. Scope and limitations retained

Accepted SI-E01.2b.2 verifies pure read-only **consistency of supplied typed records**: real generating Run stage/method/version, exact historical previous chain, original CREATIVE Run retention K1→K2→K3 and HUMAN_EDIT direct roots, plus exact EvaluationReport Rubric-to-Run binding. Prior accepted SI-E01.2b.1 resolver handles local hashes, graph and Run snapshots. No certificate of actual execution, identity, rights, semantic currentness, eligibility/scoring, evidence truth, ERef material, FieldGrant authorization, persistence/export, privacy or editorial approval.

RFC `docs/architecture/STORY_INTELLIGENCE_SI_RESOLVER_FOLLOW_UP_RFC.md` at docs branch `c6923614b932b0dbbb667cdd54dea1646d0a758b` remains **PROPOSAL/OWNER_REVIEW**, not an approved change to SI contracts or execution scope.

**SI-E01.2b.2 + F1 is ACCEPTED / PURE_CROSS_RECORD_PROVENANCE_ONLY.** This is an acceptance of a bounded static review, not a declaration that the whole Story Intelligence engine is finished.

## 3. Next gate

SI-E01.2b.3 (pure semantic dependency/currentness of exact SI records) is a distinct stage requiring its own precise task, allowed files, test requirements, owner handoff, and independent review. R1 §4.2 distinguishes semantic-input ancestry from full audit Closure and treats observed current context and ERef snapshot separately. No automatic approval of selections, eligibility, editorial rights or renderer.

**STOP.** No SI-E01.2b.3, SI-E02, production operation executors, RFC implementations, protected writes, PR, merge, release or `main` changes authorized by this review. `PUBLISH_REVISION` remains DISABLED, partial COMMIT reconstruction OFF and S3.2b BLOCKED_HOST_NOT_PROVIDED.
