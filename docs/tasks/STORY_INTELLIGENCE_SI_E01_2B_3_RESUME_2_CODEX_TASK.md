# CODEX TASK — SI-E01.2b.3-RESUME-2: pure semantic currentness under approved G01 + G02

**Date:** 2026-11-10
**Status:** **READY FOR EXPLICIT OWNER HANDOFF / NOT STARTED**
**Approval:** `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_G02_OWNER_APPROVAL_2026_11_10.md` @ `53625a79f357052dca53ad9c7bca0cce71ed95fc`.
**G02 source:** `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_G02_OWNER_DECISION_PROPOSAL.md` @ `e191eec53b2938bc0188ba0b579c9738a1beeb8b`.
**Earlier G01:** `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_APPROVAL_2026_11_10.md` @ `c61801d6fe3bde1557429c17c009c77cfebd50b1`.
**Historical G02 STOP (no code):** `feat/story-intelligence-si-e01-2b-3-resume-currentness` @ `f549bc4437a2af3e2f1f349ce266715bcc5589e2`.

## 1. Exact base, separate branch, mandatory preflight

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
**Source branch:** `docs/story-intelligence-si-e01-2b-3-g02-approval-resume-2`.
**Exact source SHA:** provided literally in the owner handoff after this document's publication. Verify source remote HEAD **equals** that SHA and both G02 approval and this task exist at that SHA before editing; mismatch → STOP. Do not branch from `main`, historical G01 docs, either blocked SI-E01.2b.3 branch or the separate architecture RFC.

**New feature branch:** `feat/story-intelligence-si-e01-2b-3-resume-2-currentness`, created only from the exact source SHA. No PR, merge, release, `main` change or protected writes.

Read in this order:
1. Owner-approved SI/1 original specification, R1 §§1.1–1.3/2/3.1/4.1–4.3/5/6, R1a §§2–4, R1b and owner approvals, SI-D01–SI-D10.
2. G01 owner approval and G01 D1–D5 proposal; G02 owner approval and G02 D1–D4 proposal; G02 independent blocker review and exact reproducer in `STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_CONTRACT_GAPS.md`.
3. Previous `STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_CODEX_TASK.md`, G01/G02 BLOCKED reports, SI-E01.2b.1 and SI-E01.2b.2/F1 independent acceptance.
4. Existing accepted `story_intelligence/{codec_v1.py,model_v1.py,records_v1.py,resolver_v1.py,provenance_v1.py}` and their tests/golden vectors.

**Precedence:** original → precise R1 → precise R1a → precise approved R1b; G01 and G02 owner approvals resolve **only their specific currentness ambiguities**. Do not reinterpret other contracts. The resolver-follow-up RFC and future Claim Input Role Map are NOT approved implementation authority.

## 2. Narrow deliverable and API

Create a **pure deterministic, read-only, CPU-only, in-memory** `story_intelligence/currentness_v1.py`, without network, disk, subprocess, external providers, GPU, mutable cache or new dependencies.

Suggested public API:
`check_si_currentness(records, root, observed_active_input_refs, observed_selection_head_refs) -> {'currentness':'CURRENT'|'STALE'|'INVALID','reason_codes':List[existing Code]}`.

Use accepted exact SIRef/resolver and provenance. Document argument validation, deterministic errors/path/status, no mutation and detached result. `root` is an exact SIRef; observed sets are explicit supplied exact refs, **not authenticated currentness authority**. Validate malformed lists, refs, duplicates and conflicting (type,id) active heads; no implicit latest, no automatic rebase or changing original records. Do not add wire fields, record types, status values or error codes. If an exact error-code mapping is still under-specified, STOP with precise GAPS rather than invent a public contract.

**Before CURRENT:** validate full reachable exact audit DAG/hashes, Run snapshots and generating provenance using the accepted resolver and `verify_si_provenance`. Missing/hash-corrupt/cyclic ancestry is INVALID, never merely STALE. A valid historical exact domain dependency absent or replaced in observed active input refs is STALE. No trusted fact, license, reviewer identity, run-execution proof or production permission follows from CURRENT.

## 3. Approved G01 behavior (unchanged)

- HUMAN_EDIT `H.previous`, REVISION Run first `semantic_input_refs` base, `H.input_refs`, generating Run metadata and snapshots are required **causal/audit** evidence, but their historical identities are not required-current merely because they are edit bases. S3 may be CURRENT with S1/S2 inactive; K3 may be CURRENT with K1/K2 inactive. Still verify all immutable ancestors.
- Required-current domain dependencies are typed current payload refs plus still-applicable exact original producer constraints; distinguish SemanticClosure from Audit Closure, including nested typed refs and `Known` wrappers. A changed explicit payload role replaces that payload role, but not an independent producer constraint. Do not infer roles from generic dict shape or list order.
- Creative K1/K2/K3 retains exact original CREATIVE Run C and substantive original E1/Channel/Idea/Audience/Angle/claim/check/source/risk constraints as applicable; C.input_snapshot and C.context_snapshot remain audit-only. Revised Angle incompatible with frozen E1/channel cannot become CURRENT through implicit rebase: STALE for valid obsolete substantive bindings, INVALID only for proven structural/provenance errors.
- E1's domain currentness does not depend on later Creative/Selection/Brief/Packet heads. Brief's **actually used** Creative Selection exact ref is compared with observed selection heads, not active domain refs. Unrelated heads do not stale records. Packet freshness/UI BriefReviewState not implemented. Relevant ERef without exact validated editorial snapshot => INVALID, not CURRENT; no ERef adapter in scope.

## 4. Newly approved G02 exact rule — MUST IMPLEMENT

For the original CREATIVE Run C, **each direct ClaimItem SIRef in `C.payload.semantic_input_refs` remains an independent required-current exact substantive dependency**, even when K2/K3's current `hook_claim_refs` or chapter claim refs have changed. Current hook/chapter ClaimItem refs **also** remain required-current; the union can include both original Qa and new Qc. A match between a C direct ClaimItem and K1's original hook/chapter is *not* proof of exclusive hook/chapter role. Do not infer exclusive role from order, counts, duplicate occurrence, text, timestamps, opaque `request_payload_sha256` or old Run snapshots. V1 contains no approved exclusive-role map.

- Exact G02 reproducer: C roots include Qa and Qb; K1 hook Qa/chapter Qb; K3 hook Qc/chapter Qb; observed active Qb/Qc but not Qa, all other required refs active, valid complete audit/provenance => **STALE / INPUT_STALE**, not CURRENT or INVALID.
- Same exact valid graph plus active Qa and all required refs => **CURRENT**, provided no ERef/current-context issue.
- Shared Qa hook+chapter, or still-required Check/Risk/E1/Angle Qa: changing hook never removes independent Qa constraints. Qa absent active => STALE.
- Qa missing/corrupt from audit graph => INVALID, not STALE; unrelated Selection head changes cannot alter K3 currentness.
- Text-only K3 with unchanged substantive bindings and all required exact original C inputs active can be CURRENT despite inactive K1/K2.
- Do not extend G02 to make **all** old audit snapshot refs current or to force historical K1/K2 active; G01 remains binding. No new role-map field, no heuristics and no silent latest.

## 5. Required true graph tests, literal vectors and STOP

Build real content-addressed, closed, schema-valid bundles and observed exact SIRef lists. Existing resolver/provenance must PASS on valid STALE cases. At least **six independent literal deterministic graph+context vectors** with exact expected state/reason codes and canonical digests; expected outputs must be independently authored, not generated by currentness implementation. Reuse the exact 19-record G02 reproducer from `STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_CONTRACT_GAPS.md` as one oracle and verify its published graph/context hashes. No mocks/monkeypatches for resolver/hash success.

Cover at minimum:
1. **All eight G01-D5 owner-approved expected scenarios**, including S1→S2→S3 CURRENT with inactive S1/S2; corrupted S2 INVALID; K1→K2→K3 text-only CURRENT; original E1 absent active STALE; incompatible Angle STALE; E1 unaffected by selection; Brief used selection changed STALE; relevant unvalidated ERef INVALID.
2. **All eight G02-D3 approved scenarios**, including Qa/Qb/Qc exact graph STALE; Qa restored CURRENT; double-role hook/chapter and Check/Risk; corrupted Qa INVALID; unrelated selection unchanged; ERef invalid.
3. E1 required Idea/Angle/Rubric/Source/ClaimCheck replacements => STALE, absent/corrupt historical refs => INVALID; no future-head contamination.
4. Observed list reordering/duplicates/conflicting exact heads, malformed refs, exact SHA/revision mismatch, no implicit latest, unchanged inputs and detached result.
5. Both (a) valid resolver/provenance PASS + semantic STALE, and (b) valid resolver/provenance PASS + semantic CURRENT despite inactive historical edit bases.
6. Verify previous 14 foundation, 18+3 records, 7 resolver and 9 provenance literal vectors unchanged byte-for-byte.

If any required approved scenario is not representable with existing schema and no ERef adapter, or an unresolved substantive role beyond G02 prevents a correct algorithm, **BLOCKED_CONTRACT and STOP**, publish only GAPS and RESULT. Do not implement a partial evaluator that invents owner policy.

## 6. Strict allowlist — NEW files only

Allowed:
1. `story_intelligence/currentness_v1.py`
2. `tests/test_story_intelligence_currentness_v1.py`
3. `tests/test_story_intelligence_currentness_vectors_v1.py`
4. `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_2_RESULT.md`
5. `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_2_CONTRACT_GAPS.md` **only if blocked**.

No edits to any existing files (including both previous GAPS/RESULT pairs), accepted code/tests/vectors, G01/G02 approval, original contracts, architecture RFC, WORKLOG, README, CI/config, dependency files, editorial/storage or other branches. On BLOCKED_CONTRACT create only the two RESUME_2 docs, **no code/tests**. Scope expansion requires STOP and a separate owner decision.

## 7. Test evidence, publication and final STOP

Use project venv, report exact OS/Python, commands, test counts, durations, skipped, raw Python and outer shell exit codes:
- `.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_currentness*.py' -v`
- `.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v`
- `.venv/bin/python -m unittest discover -s tests -v`

Latest **Codex-reported unchanged-code baseline** at G02: **103 SI / exit 0**, **945 full / raw Python exit 0 / outer exit 0**. Earlier unexplained wrapper exit 1 did not recur; do not pretend its cause was diagnosed. If any test reports OK but process/session exits nonzero, status is **REVIEW_BLOCKED_EVIDENCE**, not PASS; no swallowed exits, `|| true`, pipeline masking, harness edits or waiver. On blocked no-code path, 0 currentness tests/exit 5 is expected and must not be called PASS. A Linux PASS does not qualify Windows native storage.

Before publishing: verify exact source SHA, commit parent/base, A-only allowlist, `git diff --check`, golden vectors unchanged, clean worktree, final remote SHA equality, no PR/merge/release/main changes. Publish feature branch with exact commit, changed files, independent literal vectors, test evidence and report.

**STOP after publication for independent review.** Do not start SI-E02, RFC/Claim Role Map, ERef adapter, semantic truth/rights/approval, operation executors, persistence, protected writes, PR/merge/release or `main` changes. `PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF; Windows S3.2b BLOCKED_HOST_NOT_PROVIDED.
