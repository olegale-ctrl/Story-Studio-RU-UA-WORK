# SI-E01.2b.1 — independent static acceptance

**Date:** 2026-11-09
**Status:** **ACCEPTED / PURE_READ_ONLY_RESOLVER_AND_AUDIT_CLOSURE_ONLY**
**Feature commit:** `0c27547377255016ec2fc399090ce99b63d69485`
**Exact base:** `73c4e519033d27e7ca079570a563d340d1a2f61e`
**Review evidence:** independent GitHub inspection of complete implementation, graph tests, literal-vector tests, report, R1 §§1.1–1.3 and exact Codex task; **no independent execution of Python test suite**.

## 1. Independently checked publication

- Remote branch `feat/story-intelligence-si-e01-2b-1-pure-resolver-closure` points to exact feature commit.
- Base→feature: ahead=1, behind=0; exactly four new files / **803 additions, 0 deletions**, matching the approved allowlist: `story_intelligence/resolver_v1.py`, two `tests/test_story_intelligence_resolver*.py` files, and `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_1_RESULT.md`. Historical files untouched.
- `main` observed at `e1f4efb0fb5ff290bb198349213c004b4667ef0f`; no feature PR or commit statuses or PR-triggered workflow run found.
- Codex reports Linux x86_64 Python 3.12.14, targeted **85 OK**, full **927 OK**, seven independent graph vectors, `git diff --check`, exact remote SHA and clean worktree. Tests were **not independently rerun**; GitHub CI PASS is not asserted.

## 2. Independent technical review

Read complete `resolver_v1.py` and `test_story_intelligence_resolver_v1.py`, seven literal manifests/bytes/digests and the full result report. Implementation:
- Public `resolve_si_closure(records,roots)` and `resolve_si_record(records,expected_ref)` validate supplied complete records using accepted local SI/1 validators and derive actual byte hashes; no dynamic I/O, network, mutation, persistence, editorial/storage writes or implicit latest lookup.
- Strict indexing by `(type,id,revision)`; conflicting canonical bytes for same identity `REF_HASH_MISMATCH`, duplicate equal records rejected; byte identity of all reachable refs verified including root digest.
- Schema-driven extraction of H.previous, H.origin.run_ref, H.input_refs and typed nested payload SIRefs using accepted `_SCHEMAS`, not shape guesses; ignores free-form text and distinguishes ERefs.
- Iterative DFS with color state detects cycles and verifies missing/mismatched reachable refs; canonical sorted unique manifest returned as detached plain data, with old revisions included as audit ancestry rather than currentness.
- For every reachable RunRecord, recomputes `Closure(semantic_input_refs + context active_input_refs + selection_head_refs)` and compares exact list with `input_snapshot`. Structural record validation already enforces equality with H.input_refs. No subset-only acceptance.
- Graph fixture covers manual records, Evidence/Claim/Source, Discovery/creative/evaluation runs, selected creative K1/K2/K3 with frozen originating run and distinct revision runs, historical Source revisions, nested portfolio and private discussion packet. Seven hardcoded vectors check root, manifest, canonical bytes and SHA; tests additionally exercise a separately authored edge-based oracle. Negative tests include missing refs, hashes, cycles, Run self/output, snapshot under/over-set/order, no-latest, ERef-as-SIRef, text lookalikes, duplicates, immutability and long iterative graph.
- Preflight cycle-before-edge-hash priority is diagnostic only and does not approve hash-inconsistent reachable graphs: all edges must pass exact hash checks before a successful result.

No blocking discrepancy was identified within the **bounded read-only audit-graph resolver**. This is **static source and test review**, not an independent runtime proof or a security audit. This stage does not certify external ERef material, method actually creating output, semantic currentness, selection/eligibility/rights/identity, grants, privacy, persistence or renderer authority.

## 3. Follow-on gates

**SI-E01.2b.1 ACCEPTED / PURE_ONLY.** SI-E01.2a-RESUME+F1 stays accepted as typed local foundation. Previous original/R1/R1a/R1b contracts and SI-D01–SI-D10 remain in force.

Next separately bounded candidate: **SI-E01.2b.2 — pure read-only Run-stage/provenance and original Creative Run ancestry verification**, using the accepted resolver and immutable supplied records. Explicitly **exclude semantic currentness/selection-head readiness, operations, evaluator, request replay, export, privacy authorization, workspace/persistence and editorial authority**. These require later separately bounded gates. A new exact source SHA and independent review are mandatory.

Do not merge, PR, release, start SI-E02, enable `PUBLISH_REVISION` (still disabled) or partial COMMIT reconstruction (still OFF), or resume S3.2b (BLOCKED_HOST_NOT_PROVIDED). Windows native host qualification is not claimed.

**STOP — this acceptance document is not authorization to implement further stages without the next owner handoff.**
