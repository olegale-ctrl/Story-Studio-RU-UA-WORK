# CODEX TASK — SI-E01.2b.2: pure Run-stage and R1a revision provenance verification

**Date:** 2026-11-09
**Status:** **READY FOR OWNER HANDOFF — BOUNDED NEW UNIT; NOT STARTED**
**Gate:** `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_1_INDEPENDENT_ACCEPTANCE.md` (acceptance commit `ffbfaae0882e9635ce52631ecc4bd2d7e25e961a`).
**Governance:** no PR, merge, release, main update, editorial/storage writes. STOP for independent review.

## 1. Source SHA, new branch and exact STOP

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
**Source branch:** `docs/story-intelligence-si-e01-2b-1-independent-acceptance`.
**Exact source SHA:** supplied in owner handoff after this task is published; verify the **remote source HEAD equals that literal SHA** before creating the feature branch. Never substitute default/main, an old feature branch or an unverified local tip. Mismatch => STOP without code changes.

**New isolated feature branch:** `feat/story-intelligence-si-e01-2b-2-pure-provenance`.

No rewrites, amendments, rebases, force pushes or modifications of previous accepted branches. If Codex is unable to create/check this branch from the exact SHA, STOP with evidence.

## 2. Approved contracts and accepted code

Before implementation read:
- `docs/tasks/STORY_INTELLIGENCE_V1_OWNER_APPROVAL_2026_11_09.md` (SI-D01–SI-D10).
- `docs/tasks/STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md` (18 record payloads and origin).
- `docs/tasks/STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md` §§1.1–1.3, 2, 4.1–4.2, 5.1 (exact Run stages/methods, output provenance, audit DAG and roots).
- `docs/tasks/STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md` §§2–5 (record creation/revision and two distinct Creative RunRefs).
- `docs/tasks/STORY_INTELLIGENCE_V1_R1B_REVIEWPACKET_FIELD_PATH_CLARIFICATION.md` and its explicit owner approval (only for packet paths, no new provenance authority).
- `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_RESUME_F1_INDEPENDENT_ACCEPTANCE.md` and `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_1_INDEPENDENT_ACCEPTANCE.md`.
- Existing `story_intelligence/{codec_v1.py,model_v1.py,records_v1.py,resolver_v1.py}` and their tests, including the seven literal graph vectors.

Precedence original → precise R1 overrides → precise R1a overrides → precise approved R1b. If an exact binding requirement is unresolved, document competing interpretations and **STOP**, rather than inventing a new wire contract or loosening constraints.

## 3. Scope: read-only cross-record provenance verifier, no operations

Implement a new **pure, read-only** module `story_intelligence/provenance_v1.py` with public API:

`verify_si_provenance(records, roots) -> list[SIRef]`

Input is the same explicit finite plain in-memory records/roots supplied to accepted `resolve_si_closure`. First invoke/reuse that resolver for exact hashes, typed transitive audit Closure, cycles and Run snapshot completeness. No fetch, no workspace, no auto-latest, no mutation. Return a detached canonical manifest of the verified closure only after **all** applicable cross-record checks pass; never return partial success.

For **every reachable SI record**, verify the following local-to-bundle cross-record relations where applicable:
- A derived H.origin.run_ref must resolve to a **real exact RunRecord**, already verified by the resolver, and its actual `payload.stage` / `method_id` / `method_version` must match the approved record type/revision/Origin mechanism. Initial StoryIdea → DISCOVERY / `si.discover-local,1-r1`; initial CreativeAlternative → CREATIVE / `si.creative-templates,1-r1`; initial EvaluationReport → EVALUATION / `si.evaluate,1-r1`; initial ReviewPacket → PACKET_EXPORT / `si.review-packet,1-r1`; RULE_DERIVED assembled ProductionBrief → BRIEF_ASSEMBLY / `si.brief-assembly,1-r1`; a HUMAN_EDIT revision → REVISION / `si.human-revision,1-r1`. For other initially MANUAL_INPUT/USER_IMPORT types, no generating Run; use accepted strict header rules. Existing local checks for method/stage themselves do **not** prove the specific record originated from that Run, so do not label the result as trusted execution evidence.
- When revision >1, resolve each exact `H.previous`, require the same identity/type and immediate predecessor revision (already checked structurally), preserve ancestry all the way to revision1, ensure the generating run for a HUMAN_EDIT record is separate from prior original runs, and preserve the unchanged previous bytes. Do not silently synthesize an intermediate record or hop across versions.
- **CreativeAlternative R1a dual-run invariant**: initial K1 must bind `H.origin.run_ref == payload.run_ref`, and the referenced Run must truly have CREATIVE stage. For every K2/K3/etc HUMAN_EDIT, H.origin.run_ref must be an exact REVISION Run, while `payload.run_ref` remains the **same exact original CREATIVE Run** from genesis K1. Verify the whole resolved previous chain; reject null, alien CREATIVE runs, swapped REVISION run, wrong stage, missing ancestor, or borrowed original run after an attempted ancestry rewrite. Do not re-label edited content as new template output. Old Selection does not transfer to a new creative revision.
- No output-backlink assumptions: the generating Run deliberately has **no** `output_refs`. Verify all declared relationships that can be checked from accepted immutable records, without pretending the Run cryptographically attests that it actually generated the text or that a human label is authentic.
- R1 operation-root assertions **only where unambiguous** from exact approved contracts and already present fields: for a HUMAN_EDIT revision `H.input_refs[0]` must be exact H.previous, and the revision Run.semantic_input_refs must include the exact preceding record as its direct source; for initial derived outputs verify that the Run's declared roots are not a circular reference to its own output (the resolver already enforces DAG). Cross-record bindings required for specific operation roots should be checked if their exact expected order is unambiguously specified; never treat audit `Run.input_snapshot` as equivalent to direct operation roots.

**Explicitly NOT in this unit:** independent verification of user's privacy/rights/identity, ERef material, currentness, selection-head approval/readiness, eligibility/rubric, actual source field/index/text grants, evidence truth, semantic dependency matching against observed active context, request/response, operation execution, idempotency or storage. Cross-record provenance checks are *consistency of supplied records*, not evidence that their alleged operations happened or an authority certificate.

## 4. Error behavior and adversarial cases

Use existing R1 `SIValidationError` codes only: generally `PROVENANCE_MISMATCH` for wrong generating stage, original Creative Run substitution, or incorrect revision-Run binding; missing/hash/type/cycle errors continue from the resolver; meaningful exact `$.records[i].H.origin.run_ref`, `$.records[i].payload.run_ref`, `$.records[i].H.previous`, `...semantic_input_refs` paths where relevant. No error-code additions, coerced values, repair/autofill, ignored invalid records, or acceptance of partial graph.

Build **true content-addressed** positive graphs with independently computed complete-record SHA256 refs (no fake placeholder hashes as success) for:
- initial Discovery→StoryIdea, Evaluation→EvaluationReport, CREATIVE→K1, BRIEF_ASSEMBLY→ProductionBrief, PACKET_EXPORT→ReviewPacket;
- ordinary manual/import record and legal HUMAN_EDIT ancestry;
- K1→K2→K3 Creative history with one originating CREATIVE Run and distinct REVISION generating runs.

Negative tests must **recompute mutated record hashes and dependent refs carefully** so rejection identifies provenance violations rather than merely failing early on stale hashes. Test wrong Run stage with valid ref/hash; correct Run stage but wrong originating Run; mismatch of K2 original vs K1 originating Run; K3 carrying K2 Revision Run as original; modified K1 ancestry; missing previous; missing Run; wrong REVISION direct base input; malformed root/bundle; detached outputs and untouched input. If a scenario requires changing an already hashed ancestor, rebuild the entire downstream synthetic graph topologically; never bypass accepted hashes by monkeypatching the production resolver to fabricate a positive chain.

At least **six independent literal positive provenance-case fixtures** plus multiple adversarial negative cases. Include actual exact input/root/manifest bytes and hashes or an independently generated canonical regression oracle; avoid test vectors whose expected result is computed by the function under test. Existing 14 foundation, 18+3 record/value and seven resolver graph vectors must remain byte-for-byte unchanged.

## 5. Exact allowlist — only NEW files

1. `story_intelligence/provenance_v1.py`
2. `tests/test_story_intelligence_provenance_v1.py`
3. `tests/test_story_intelligence_provenance_vectors_v1.py`
4. `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_2_RESULT.md`
5. `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_2_CONTRACT_GAPS.md` — optional, only for a genuine blocker.

Do not edit existing code or tests, approved contracts, branches, reports, config, workflow, dependencies, WORKLOG, editorial/storage, or any unrelated file. If a change to accepted resolver/record logic is necessary, STOP with precise evidence; do not expand the allowlist. No new dependencies, internet, Context7, provider/model, ffmpeg, GPU or host tools needed for this stdlib-only task.

## 6. Evidence, tests and STOP

Execute with the project's Python interpreter and report OS/Python version, exact commands, exit codes and actual numbers:
- `python -m unittest discover -s tests -p 'test_story_intelligence_provenance*.py' -v`
- `python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v`
- `python -m unittest discover -s tests -v`

Codex-reported previous baseline is **85 targeted / 927 full**; do not claim independent verification or assume counts without running. Report vector independence and all new positive/negative cases, including exact stage/binding failures. Run `git diff --check`, validate allowed files, branch/base/parent/remote equality, clean worktree, no test skips/failure suppression and no change to earlier literal vectors.

If a new material contract gap blocks correct verification, **STOP before implementing guessed semantics** and publish only new `_CONTRACT_GAPS.md` and `_RESULT.md` with minimal contradictory examples, owner choices and an honest BLOCKED_CONTRACT status.

Publish only the fresh feature branch and hand back result/commit for **independent review**. **STOP.** Do not implement SI-E01.2b.3 (semantic currentness), SI-E02, operation executor, selection/eligibility engine, persistence/privacy/export, renderer or protected editorial integration. `PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF; S3.2b BLOCKED_HOST_NOT_PROVIDED.
