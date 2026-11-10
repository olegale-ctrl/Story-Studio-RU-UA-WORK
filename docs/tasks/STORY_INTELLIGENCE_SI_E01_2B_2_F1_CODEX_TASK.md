# CODEX TASK — SI-E01.2b.2-F1: exact EvaluationReport rubric↔Run binding

**Date:** 2026-11-10
**Status:** **BOUNDED F1 FIX ONLY / NOT STARTED**
**Blocker:** `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_2_INDEPENDENT_REVIEW_F1.md` (`ff8faa6896673a5bd0ceea417e791c1f9f7856df`).
**Owner handoff:** execution authorization only for this narrow F1; no PR, merge, release, `main` change, wider provenance improvements or next stage.

## 1. Exact source and isolated fix branch

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
**Source branch:** `feat/story-intelligence-si-e01-2b-2-pure-provenance`.
**Exact source SHA:** `9a2999bae72b1d6bd6784e7df305f59dea1bfd2e`.
Verify source **remote HEAD equals exact SHA** before any change; mismatch → STOP. Do **not** use this docs branch, `main`, or the RFC branch as the code base.

Create **new** branch: `fix/story-intelligence-si-e01-2b-2-f1-rubric-run-binding` from the exact source SHA. Do not modify historical feature, main, accepted modules, or the review docs.

Read approved `docs/tasks/STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md` §3.1 (exact report/run rubric binding), R1 §1 and §2, R1a (for scope context), `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_2_CODEX_TASK.md`, original SI-E01.2b.2 result, this independent F1 review, and current `provenance_v1.py` and its tests.

## 2. Exactly one behavior change

For each reachable `EvaluationReport`, after accepted resolver proves exact Run and `generator(...)` proves EVALUATION stage, `si.evaluate`, `1-r1`, verify:

`EvaluationReport.payload.rubric_ref == actual_generative_RunRecord.payload.rubric_ref`

Compare entire typed SIRef exactly (type/id/revision/sha256). On mismatch fail closed with existing `PROVENANCE_MISMATCH` and precise output path `$.records[i].payload.rubric_ref`. The validator must **not** silently rewrite either ref, tolerate different Rubric versions, infer latest, request external data or add an error code. Keep existing run-stage, creative K1→K2→K3, ancestry, input snapshot, HUMAN_EDIT direct-root invariants unmodified.

This is cross-record consistency only; it does **not** certify rubric criteria/weights, eligibility, scoring, actual Run execution, editor identity, review rights, truth or authority.

## 3. Strict allowlist

Only:
1. **Edit** `story_intelligence/provenance_v1.py` (minimal guard).
2. **Edit** `tests/test_story_intelligence_provenance_v1.py` (focused positive and negative regression tests).
3. **Create** `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_2_F1_RESULT.md`.

**Do not edit** `tests/test_story_intelligence_provenance_vectors_v1.py`, any earlier literal vectors, resolver/codec/model/records, source R1/R1a/R1b contracts, acceptance docs, WORKLOG, CI/config/dependencies, editorial/storage, or other files. If correct implementation requires more, STOP and report reason without expanding allowlist.

## 4. Required tests and red/green evidence

Create a fully valid in-memory content-addressed graph containing **two distinct, real valid Rubric records A and B**, plus an EVALUATION Run that references A and an EvaluationReport that references B. Every required reference must point to actual correctly hashed bytes; rebuild changed full record refs as necessary. Before fix, assert independently that `resolve_si_closure(records, [report_ref])` **accepts**, and that the old provenance verifier incorrectly accepts this graph. Record this *red phase* (test failure against pre-fix module) accurately. After the fix, require exact error `PROVENANCE_MISMATCH` at `$.records[i].payload.rubric_ref`; do not let `REF_HASH_MISMATCH`, missing refs, stage mismatch or another preliminary check mask this defect.

Add matching positive report/run Rubric case and at least one different valid Rubric revision/hash adversarial case if feasible in the bounded scope. Ensure inputs remain unchanged and a successful manifest is detached. Do not monkeypatch production resolver or hash functions for success fixtures. Existing nine literal positive bundle/root/manifest vectors must remain unchanged.

Execute project's venv:
- focused new F1 regression methods (report exact names and red/green outcomes);
- `python -m unittest discover -s tests -p 'test_story_intelligence_provenance*.py' -v`;
- `python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v`;
- `python -m unittest discover -s tests -v`.

Baseline is Codex-reported **15 provenance / 100 SI / 942 full tests**; report actual observed counts/exits/no skips rather than assume. Rerun full suite after the final code and test changes. Verify existing 14 foundation, 18+3 records/value, seven resolver and nine provenance vectors are byte-identical. `git diff --check`, exact diff allowlist, branch/base/parent SHA, clean working tree, remote SHA equality; report OS/Python version and full suite duration.

## 5. Publication and STOP

Publish only the new fix branch with exact base, final commit, changed files, diffs, before/after reproducer and actual test evidence. If the approved R1 and this guard conflict, STOP and document with concrete example rather than change contracts or improvise. No PR/merge/release/main change. Leave RFC proposals separate and untouched.

**STOP after publication for independent F1 review.** Do not start SI-E01.2b.3, SI-E02, ERef, performance optimization, semantic gates, persistence, or operation execution. `PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF; S3.2b BLOCKED_HOST_NOT_PROVIDED.
