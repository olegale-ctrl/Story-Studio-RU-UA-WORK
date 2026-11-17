# SI-E01.2b.3-RESUME — independent review of G02 STOP

**Date:** 2026-11-10
**Verdict:** **BLOCKED_CONTRACT CONFIRMED / NO IMPLEMENTATION ACCEPTED**
**Feature commit:** `f549bc4437a2af3e2f1f349ce266715bcc5589e2`
**Exact base:** `e735d729f6dad8ff874a92d52b37f4a95bb8fc20`
**Evidence level:** independent GitHub branch/diff/static contract/reproducer inspection; **no independent execution of reproducer or unittest**.

## 1. Publication and tests

Remote feature HEAD is the reported commit; base branch HEAD is the exact reported base. Base-to-feature comparison: ahead=1, behind=0, **2 new Markdown files only, 322 additions, 0 deletions**: `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_CONTRACT_GAPS.md` (+192) and `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_RESULT.md` (+130). No code, currentness tests, or vectors were created. At review `main=e1f4efb0fb5ff290bb198349213c004b4667ef0f`, unchanged; no feature PR found.

Codex reports a constructed ERef-free **19-record, 19-reachable, 11-observed-active-identity** bundle passing existing exact resolver/provenance; literal bundle/context hashes and a full reproducible snippet are in GAPS. This is a **reported** reproducer, not independently executed here. Codex reports existing SI **103 OK/exit 0**, full unittest **945 OK/raw Python exit 0/outer session exit 0**, currentness pattern **0 tests/exit 5** because none were written. The prior wrapper exit discrepancy did not recur; cause of historical exit 1 not established. The clean full baseline is evidence of **unchanged previously accepted code**, not SI-E01.2b.3 implementation acceptance. Git diff --check and clean worktree are Codex-reported; the two-file allowlist is independently verified via GitHub.

## 2. G02 is a genuine ambiguity in approved contracts

R1 §1.3/§2 defines `CREATIVE Run.semantic_input_refs` as an ordered list of exact operation inputs including claim/check/source roots, without an embedded role label for each input. R1a §4 preserves immutable C and current `CreativeAlternative.payload.hook_claim_refs`/chapter claim refs through HUMAN_EDIT. Owner-approved G01 D2/D3 allows *same-role* override by current payload while retaining still-applicable producer constraints; it does **not** define how to prove exclusivity of a direct ClaimItem root to a hook or chapter role.

The G02 graph is therefore insufficient to distinguish: Qa originally hook-only and replaceable by Qc, or Qa additionally a frozen independent production constraint. Both interpretations use the same valid exact bytes and recorded histories; changing only the current hook does not distinguish them. C's opaque `request_payload_sha256` cannot be decoded into a role map. Treating all claims as replaceable loses constraints; treating all old claims as current overrides G01 role replacement; arbitrarily declaring INVALID mischaracterizes a structurally sound graph. The approved G01 remains valid and unchanged.

## 3. Independent recommendation — PROPOSAL, NOT OWNER APPROVAL

Choose conservative retention for *ambiguous* flat `CREATIVE Run` direct ClaimItem roots, and allow replacement only where the record graph proves an unambiguous role assignment. Specifically, a ClaimItem appearing in K1.hook_claim_refs is **not by itself sufficient evidence** that it served *only* as hook input; chapter membership similarly does not prove exclusivity. Absent an approved exclusive provenance role, keep exact Qa required-current even when hook payload now uses Qc: the exact G02 observed set lacking Qa yields **STALE / INPUT_STALE**. This is a read-only conservative policy for currentness, not a ban on HUMAN_EDIT or a trusted rights/evidence check.

Shared claims: if a claim is used in more than one role, removal from one role does not remove surviving roles. Any claim independently referenced from current Angle, E1, ClaimCheck, Risk, or another substantive retained binding remains required-current regardless of hook edit. It is dangerous to infer independent constraints merely by membership in unrelated audit snapshots, so no audit→semantic promotion. A separate explicit role-map/creator option could enable more precise replacement in future, but **is not approved** or needed to implement the conservative policy as specified here.

**Product tradeoff:** old direct C-root Qa might stay required despite a benign hook edit, leading to more STALE assessments and explicit regeneration rather than silently losing constraints. This errs on editorial reproducibility, not automation convenience. G01's 'text-only Creative edit CURRENT' example remains true when substantive bindings are unchanged, because their original exact refs remain active. Nothing here makes K1/K2/REVISION Run metadata current domain identities.

## 4. STOP and next decision

Separate `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_G02_OWNER_DECISION_PROPOSAL.md` records a narrow decision and exact expected vectors. It requires **explicit owner approval**, not a broad approval inferred from G01. Until approved and translated to a new bounded Codex task, SI-E01.2b.3 remains **BLOCKED_CONTRACT**. Do not start SI-E02, new fields, RFC/ERef adapter, semantic fact checking, operation execution, persistence or protected writes, PR/merge/release. `PUBLISH_REVISION` DISABLED, partial COMMIT reconstruction OFF, S3.2b BLOCKED_HOST_NOT_PROVIDED.
