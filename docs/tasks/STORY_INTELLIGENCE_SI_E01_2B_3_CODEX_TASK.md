# CODEX TASK — SI-E01.2b.3: pure semantic dependency/currentness check, bounded contract-first

**Date:** 2026-11-10
**Status:** **READY FOR OWNER HANDOFF / NOT STARTED**
**Prerequisite:** `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_2_F1_INDEPENDENT_ACCEPTANCE.md` @ `705102014931847a3bf9800d3bf01e21ffb88dc4`.
**Execution gate:** owner must forward this task with the final exact docs-branch remote HEAD SHA; do not auto-start SI-E02.

## 1. Source and branch

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Source branch: `docs/story-intelligence-si-e01-2b-2-f1-independent-acceptance`.
Exact source SHA: **supplied in the owner handoff after this task's publication**. Before edits Codex MUST check that remote source HEAD is exactly that SHA. Mismatch => STOP.
New feature branch: `feat/story-intelligence-si-e01-2b-3-pure-semantic-currentness`, created from that exact source commit. Never use `main`, a previous feature, or the separate RFC branch as an implicit fallback.

## 2. Read binding authority before implementation

Read: owner-approved `STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md`, `STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md` especially §§1.1–1.3, 2, 3.1, 4.1–4.3, 5.1–5.3 and §6, `STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md`, approved R1b P01–P05 and corresponding owner approvals, SI-D01–SI-D10, accepted SI-E01.2a/F1, SI-E01.2b.1 and SI-E01.2b.2/F1 acceptance notes, and `story_intelligence/{codec_v1.py,model_v1.py,records_v1.py,resolver_v1.py,provenance_v1.py}`. Precedence original → precise R1 → precise R1a → approved R1b.

Separate RFC `docs/architecture/STORY_INTELLIGENCE_SI_RESOLVER_FOLLOW_UP_RFC.md` @ `c6923614b932b0dbbb667cdd54dea1646d0a758b` is PROPOSAL/OWNER_REVIEW only; no permission to implement ERef integration, Asset Registry, performance refactors, semantic fact-checking, storage or Draft UX.

## 3. Pure read-only scope

Produce `story_intelligence/currentness_v1.py`: a **pure, deterministic in-memory semantic-ref/currentness evaluator** on supplied exact SI/1 records and an explicit **observed current SI context**, not a new persisted record, UI projection, operation, or authority result.

Suggested minimal public API:
`check_si_currentness(records, root, observed_active_input_refs, observed_selection_head_refs) -> {currentness:'CURRENT'|'STALE'|'INVALID', reason_codes:List<existing Code>}`

Implement only this local Python API; do not add wire fields/types, modify codec/hashes, persist a projection or invent an unapproved request envelope. All supplied values must have validated plain-list and SIRef shape; the API must be documented with exact deterministic errors and fail-closed behavior. If an existing contract forbids a proposed API shape, STOP and document the discrepancy.

Separate **structural/hash graph INVALID** from **valid historical but no longer current STALE**. Resolve exact semantic dependency refs and selected roots from the supplied complete bundle with accepted resolver and provenance checker where applicable. Missing, mismatched or cyclic typed refs cannot become STALE merely because the current context changed; use INVALID with existing R1 codes, not synthetic fallback. Never auto-resolve latest, infer current head from timestamp/id, rebase old refs, or convert UNKNOWN into Known.

**SemanticClosure is distinct from Audit Closure.** R1 §4.2: follow substantive typed payload refs and the generating Run's `semantic_input_refs`; exclude `H.previous`, `Run.input_snapshot`, `Run.context_snapshot`, `H.origin.run_ref` as a generic edge, and unrelated heads/labels/timestamps. Treat `H.previous` as historical audit ancestry only; it does not by itself make a revised record stale because the older version is no longer active. Retain direct domain dependencies from current revision, including refs that are also explicitly recorded as content dependencies; a Creative revision's `payload.run_ref` is original provenance, not automatically current domain input merely because it is a typed field. Distinguish such provenance-only refs from meaningful domain fields using the approved typed schema and R1/R1a semantics, not arbitrary `dict` shape detection. Correctly handle historical generating Run `semantic_input_refs` without using its stored `input_snapshot` as current input.

**Comparison of current inputs:** For a derived domain record (e.g. EvaluationReport, CreativeAlternative, ProductionBrief), compare its exact semantic refs to caller-provided explicit observed active SIRef set. Compare an actually **used creative Selection** for a Brief to observed selection-head refs, not the active input set. Additional unrelated active records/heads must not make a record STALE. Replacing/removing a *required* dependency does make it STALE; exact ref identity is type/id/revision/sha256, not only id or content. Input ordering of active sets should not invent staleness; reject duplicate conflicting identities and conflicting declared heads rather than silently choosing a version. With a revised current source/idea, historical E1/K1/B1 may become STALE, but a changed selection head alone must not change E1 or K1 domain currentness. A Brief that consumes an old selected Creative may become STALE after head changes. WITHDRAW changes review projection, not automatically Brief's domain currentness.

**ERefs:** approved R1 requires separate exact validated editorial snapshot context when ERefs are relevant. This pure task has **no editorial adapter or ERef material**. Never claim CURRENT when a queried domain record requires an ERef freshness assertion without a validated supplied snapshot. If R1 leaves no valid deterministic way to represent/decide that state with this API, **STOP before implementing guessed semantics and publish CONTRACT_GAPS**. Do not treat `editorial_snapshot_sha256=UNKNOWN` as implicit permission or infer trust from shape/digest alone. Under-specification of active input coverage/identity or causal dependency extraction also requires STOP instead of weaker currentness labels.

**No UI/BriefReviewState projection** in this task: specifically no readiness states, `READY_FOR_BRIEF_REVIEW`, selection eligibility, reviewer rights or Packet capture; no source truth, qualitative evidence evaluation, semantic gate, run execution, identity or authorization. Do not equate `CURRENT` with eligibility/approval/production permission. No I/O/storage/network/providers/GPU/FFmpeg/editorial imports, or new dependencies.

## 4. Testable cases and acceptance

Build true content-addressed closed-bundle graphs with actual Run/provenance and exact refs. Test at least:
- EVALUATION E1 CURRENT with required inputs; remains CURRENT when unrelated creative/selection/Brief/Packet heads change; no requirement to include future selections.
- E1 STALE on exact Idea/source/claim/check/rubric dependency replacement/removal, without changed historical bytes; E1 INVALID on corrupt/missing/hash-conflicting semantic ref, not mislabeled STALE.
- Creative K1 and revised K2/K3: currentness follows active domain dependencies and latest explicit inputs, not solely old `H.previous` or old originating CREATIVE Run; changing creative Selection head alone must not stale the alternative.
- Brief B1: CURRENT only with its substantive domain dependencies and, when used, matching exact creative Selection head; change to used head -> STALE while E1 remains CURRENT. WITHDRAW of Brief head affects UI review state, not necessarily Brief's own domain currentness.
- Changed unrelated current head, reordered observed input lists, duplicate/conflicting heads, stale historical revisions, active set missing/containing different exact SHA or revision, and no implicit latest lookup.
- Snapshot/ERef-required ambiguous contexts => explicit INVALID/UNAVAILABLE or documented BLOCKED_CONTRACT according to approved R1, never falsely CURRENT.
- No mutation, detached results, deterministic reason_codes, stable errors, retained old golden vectors.

For expected states use an independent test oracle and at least six literal deterministic scenario vectors with exact expected currentness/reason codes and canonical digests of supplied graph/observed context (where coherent with the contracts). If a required positive 'CURRENT' state cannot be legitimately established under approved R1 due to unresolved ERef/observed-context authority, publish BLOCKED_CONTRACT rather than constructing misleading fixtures.

## 5. Strict allowlist: only NEW files

1. `story_intelligence/currentness_v1.py`
2. `tests/test_story_intelligence_currentness_v1.py`
3. `tests/test_story_intelligence_currentness_vectors_v1.py`
4. `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_RESULT.md`
5. `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_CONTRACT_GAPS.md` — optional if genuinely blocked.

No edits to accepted files, vectors, contracts, workflow/CI/config, WORKLOG, editorial/storage, docs RFC, `main` or any previous feature branch. If a required existing-file change becomes necessary STOP with exact evidence.

## 6. Test/evidence and STOP

Use the project's venv with exact commands:
`python -m unittest discover -s tests -p 'test_story_intelligence_currentness*.py' -v`
`python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v`
`python -m unittest discover -s tests -v`

Previous **Codex-reported** baseline is **103 SI / 945 full**; rerun and report actual counts, exit codes, runtime, zero skips, independent graph oracles and literal vectors. Verify prior SI golden vectors byte-for-byte unchanged, `git diff --check`, exact A-only allowlist, clean worktree, source HEAD/base/parent/remote SHA equality and no PR/merge/release/main changes. Linux tests do not assert Windows native qualification.

If the approved contracts do not specify sufficient semantics for a correct implementation, publish only GAPS + RESULT as **BLOCKED_CONTRACT** and STOP without partial/guessed code. After implementation publish only the bounded new feature branch and **STOP for independent review**. SI-E02 and RFC implementations remain separately gated. `PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF; S3.2b BLOCKED_HOST_NOT_PROVIDED.
