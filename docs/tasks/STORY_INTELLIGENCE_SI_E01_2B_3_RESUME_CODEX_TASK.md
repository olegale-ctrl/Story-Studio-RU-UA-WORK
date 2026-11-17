# CODEX TASK — SI-E01.2b.3-RESUME: pure semantic currentness after owner-approved G01

**Date:** 2026-11-10
**Status:** **READY FOR OWNER HANDOFF / NOT STARTED**
**Approval authority:** `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_APPROVAL_2026_11_10.md` committed at `c61801d6fe3bde1557429c17c009c77cfebd50b1`.
**Prior stop:** `feat/story-intelligence-si-e01-2b-3-pure-semantic-currentness` @ `1e62383ddc555c06ca2ab9be7ae462f99954c281`, **BLOCKED_CONTRACT / NO CODE**. Do not continue that feature branch.

## 1. Exact starting point, new feature and STOP

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
**Source branch:** `docs/story-intelligence-si-e01-2b-3-g01-approval-resume`.
**Exact source commit:** the final remote HEAD of this docs branch, **provided by the owner in the handoff after publication**. First compare the source remote HEAD with that literal SHA; mismatch => **STOP before editing**. Verify that the owner-approval document and this task are present at that exact SHA.
**New feature branch:** `feat/story-intelligence-si-e01-2b-3-resume-currentness` created only from the exact docs-branch source SHA. Do not use main, the blocked feature, an RFC, or another base as fallback.

Owner has approved G01 **D1, D2, D3 and D4–D5** exactly as written in `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_DECISION_PROPOSAL.md`. D6 remains a STOP/scope gate, not permission for extra work. Read the approval, G01 proposal, independent blocker review, blocked `CONTRACT_GAPS` and `RESULT`, original SI/1, owner-approved R1 §§1.2/1.3/2/3.1/4.1–4.3/5, R1a §§2–4, R1b and approvals, previous SI-E01.2a/2b.1/2b.2 acceptance notes, original SI-E01.2b.3 task, and the accepted `model_v1.py`, `codec_v1.py`, `records_v1.py`, `resolver_v1.py`, `provenance_v1.py`. Specific G01 clarification resolves only HUMAN_EDIT causal→semantic projection. Prior contract precedence otherwise unchanged.

## 2. Strict deliverable and public API

Create only a **pure, deterministic, read-only, in-memory** SI/1 currentness evaluator `story_intelligence/currentness_v1.py`, using accepted exact resolver/provenance. Suggested minimal API (do not add wire fields or new record types):

`check_si_currentness(records, root, observed_active_input_refs, observed_selection_head_refs) -> {'currentness':'CURRENT'|'STALE'|'INVALID','reason_codes':List[existing Code]}`.

Document the exact argument validation, deterministic status/error/path and result-copy behavior. `root` is one exact SIRef, observed sets are supplied plain lists of exact SIRefs; they are **observations, not proof of trusted harness authority**. Do not silently accept a hash or timestamp as proof of an observed current head. Validate exact refs and duplicates/conflicting (type,id) identities; do not infer latest, merge conflicting heads, or mutate input. Use only existing SIValidationError codes/reason_codes. For malformed API shape, use precise existing SIValidationError code/path; for structurally invalid supplied reachable graph or unresolved required exact refs, classify INVALID rather than STALE, with deterministic diagnostics. If contract/API error representation cannot be made consistent without new wire fields/codes, STOP with precise GAPS, not a guessed public contract.

Before any CURRENT result, verify full reachable audit DAG/hashes/snapshots and actual provenance with accepted `verify_si_provenance`. Supplied unrelated valid records are not implicit current heads. Missing/incorrect hashes, broken previous ancestry, cycles, conflicting identities and malformed observed context cannot be reported as ordinary STALE.

## 3. Owner-approved G01 semantic projection: mandatory

**Audit vs semantic:** `resolve_si_closure` and `verify_si_provenance` continue to check the complete historical graph. Semantic currentness must NOT require `H.previous`, `H.origin.run_ref`, `H.input_refs`, Run.input_snapshot, Run.context_snapshot, or historical Run metadata as current domain identities merely because they are audit edges. R1 §4.2 semantic dependency roots are substantive, not the entire audit Closure.

**D1 HUMAN_EDIT:** The first exact base_ref in a REVISION Run.semantic_input_refs is a mandatory *causal editing base*, fully verified but **not required-current solely by being the first root**. Do not recurse through obsolete previous revisions to require S1/S2 when checking S3, or K1/K2 when checking K3. No change to accepted `H.input_refs`, Run.semantic_input_refs, original CREATIVE run or frozen snapshots.

**D2 typed current-payload roles:** Traverse typed substantive refs in the queried current revision's payload, including nested Known/list refs. Exclude only approved provenance-only/audit roles; never use generic dict-shape guesses or remove a domain ref because it happens to be old. Current revision's explicitly bound role supersedes a historical producer binding for the *same role*, but not another role; retain still-applicable exact producer dependencies. All exact refs must resolve, and required-current refs must match the observed active set by full (type,id,revision,sha256). Different active revision or absent required ref => STALE, provided the graph is otherwise valid. Extra unrelated observed refs/selection heads and list order must not affect currentness. Do not infer currentness from the queried root's own H.previous chain.

**D3 Creative:** For K1, use substantive inputs of actual original CREATIVE Run C, including its exact EvaluationReport and required idea/angle/audience/channel/rubric/claim/check/source/risk context under R1 §4.2. For K2/K3, preserve C's exact provenance, do not require K1/K2 as current identities, and project typed current `angle_ref`, `hook_claim_refs` and nested chapter claim refs over the corresponding roles in C. Original E1/ChannelContext and other still-relevant producer constraints **remain exact**; do not rebase to a different E2/channel from observed. If a revised Angle is incompatible with original E1 or immutable evaluation/channel/claim bindings, the valid historical record is STALE, not CURRENT; use INVALID only for an actual structural/hash/provenance contradiction under existing contracts. For unchanged domain bindings, text-only K3 can be CURRENT despite historical K1/K2 being inactive. Never treat C.input_snapshot or C.context_snapshot as required-current sets.

**D4 other records/Selection/ERef:** Apply D1–D2 to all R1a RevisableRecordSet types as their typed payloads permit. EvaluationReport dependencies must include exact current substantive EVALUATION roots and Rubric (with already accepted report↔Run rubric binding); unrelated future Creative/Selection/Brief/Packet heads do not stale E1. A Brief's actually used `creative_selection_ref` must be compared against observed selection heads, not active input refs. Unrelated heads do not stale E1/K; Brief's own WITHDRAW affects review projection, not automatically its semantic currentness. Packet's whole-context freshness is a different stage, **not implemented here**. A relevant ERef without exact validated editorial snapshot context => INVALID under R1 §1.2; **no ERef adapter in scope**, no false CURRENT from an opaque digest, UNKNOWN, or user-supplied status.

**Boundary of D2/D3:** The approval authorizes *role-aware projection*, not an arbitrary new mapping from old C roots to new domain roles. If typed schema and approved R1/R1a/G01 do not determine how to inherit or override a particular substantive ref (e.g. multiple same-type claims, original evaluation versus revised angle), STOP and record the exact ambiguous fixture, competing results, and minimal owner choice. Do not silently broaden to semantics/authority or assert CURRENT by dropping a constraint.

## 4. Required true-graph tests and literal vectors

Use real SI/1 records, exact SHA-256, accepted resolver/provenance and explicit observed sets. Build at least **six independently literal** positive/negative graph+context vectors with stable expected state/reason codes and canonical graph/context digests, plus focused tests covering **all eight owner-approved D5 cases**:
1. S1→S2→S3 SourceItem HUMAN_EDIT with observed exact S3 and inactive S1/S2: CURRENT; changing/removing S2 bytes/ref: INVALID, not STALE.
2. K1→K2→K3 Creative text-only edits with original C, unchanged domain refs and required E1/channel/etc active but K1/K2 inactive: CURRENT (ERef-free fixture). Removing/replacing exact original E1 in observed context while its historical record still resolves: STALE.
3. K3 changes A1→A2 and introduces idea/claim incompatible with original E1/channel: STALE, never implicit rebase or false CURRENT.
4. E1 unchanged domain deps: CURRENT despite changed unrelated Creative/Selection/Brief/Packet heads; changed required Idea/Angle/Rubric/Source/Check exact refs: STALE, while malformed/missing exact ref in bundle: INVALID.
5. Brief B1 with actual used Creative Selection head S: CURRENT with matching exact S; changed used head S2: STALE; unrelated heads ignored; WITHDRAW Brief head not automatic Brief domain STALE.
6. Relevant ERef without validated editorial snapshot: INVALID, even when SI audit graph otherwise resolves.
7. Duplicate or conflicting observed (type,id) heads, wrong ref types, duplicate roots, malformed observed list, reordered active sets, no implicit latest, historical previous absent, non-mutating detached results.
8. Correctly preserve immutable C and REVISION Runs, canonical Run snapshots, earlier vectors and existing resolver/provenance outputs.

Independently establish expected outcomes (not by copying the function's output). Record literal exact refs/hashes and context digests in tests; do not merely regenerate expected values from the implementation under test. At least one graph must explicitly demonstrate **accepted resolver+provenance PASS, semantic STALE**, and one must demonstrate **accepted resolver+provenance PASS, semantic CURRENT despite inactive historical edit bases**. ERef-free genuine fixtures for CURRENT are mandatory. If an approved expected case is not representable without inventing a new field or editorial adapter, STOP with GAPS rather than counterfeit a positive test.

## 5. Strict allowlist: NEW files only

1. `story_intelligence/currentness_v1.py`
2. `tests/test_story_intelligence_currentness_v1.py`
3. `tests/test_story_intelligence_currentness_vectors_v1.py`
4. `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_RESULT.md`
5. `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_CONTRACT_GAPS.md` **optional only if BLOCKED_CONTRACT**.

Do not edit any existing file, including previous blocked `STORY_INTELLIGENCE_SI_E01_2B_3_RESULT.md`/`CONTRACT_GAPS.md`, accepted code/tests/vectors, original contracts, owner approvals, architecture RFC, WORKLOG, README, dependencies, CI/config, editorial/storage, main or previous feature branches. If a change outside allowlist becomes necessary, STOP and document why; do not create partial code under unresolved semantics. If BLOCKED_CONTRACT again, publish only RESUME_RESULT + RESUME_CONTRACT_GAPS, with no currentness code/tests.

## 6. Evidence, full-suite exit anomaly and publication

Run in the project venv and report actual commands, OS/Python version, counts, exit codes, skipped count, durations:
- `.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_currentness*.py' -v`
- `.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v`
- `.venv/bin/python -m unittest discover -s tests -v`

Prior **Codex-reported** baseline: 103 SI/exit 0; 945 full unittest summary OK but **shell/session exit 1**, unexplained; 0 currentness tests/exit 5 because STOP. **Do not call 945 OK + exit 1 a full-suite PASS.** In a read-only diagnostic, capture raw Python process return code separately from outer shell/session status, unfiltered stderr/stdout and command invocation, without pipelines, `|| true`, swallowed failures, environment mutation or new repository files. If the full suite exits 0, report the clean evidence; if unittest says OK but execution still returns 1, record the precise mismatch and status **REVIEW_BLOCKED_EVIDENCE**, not PASS or automatic waiver. Do not change unrelated tests/harness/CI to fix it. Any nonzero targeted test process is also a blocker.

Verify unchanged prior 14 foundation, 18+3 record/value, 7 resolver, 9 provenance literal vectors, and unchanged existing accepted files; `git diff --check`, strict A-only allowlist, exact base/parent/remote SHA, clean worktree and no PR/merge/release/main changes. Report test counts actually observed, not baseline assumptions. A Linux PASS does not qualify Windows native storage.

Publish only the new bounded feature branch and its report with exact commit SHA. **STOP for independent review**; no SI-E02, RFC, ERef adapter, persistence, operation execution, semantic truth/approval/rights checks, PR/merge/release or protected writes. `PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF; Windows S3.2b BLOCKED_HOST_NOT_PROVIDED.
