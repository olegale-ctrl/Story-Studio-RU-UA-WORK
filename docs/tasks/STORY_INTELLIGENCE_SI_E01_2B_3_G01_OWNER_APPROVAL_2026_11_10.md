# SI-E01.2b.3-G01 — explicit owner approval (D1–D5)

**Date:** 2026-11-10
**Status:** **OWNER APPROVED / NARROW SEMANTIC-CURRENTNESS CLARIFICATION ONLY**
**Owner decision received:** “D1 — Историческая база HUMAN_EDIT: УТВЕРЖДАЮ; D2 — Правила содержательных зависимостей: УТВЕРЖДАЮ; D3 — Creative и исходный CREATIVE Run: УТВЕРЖДАЮ; D4–D5 — Применение и тестовые сценарии: УТВЕРЖДАЮ.”
**Approved proposal:** `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_DECISION_PROPOSAL.md` on `docs/story-intelligence-si-e01-2b-3-g01-owner-clarification` @ `8a734ca0d43785dde6c303688ac0eaf60d7e2167`.
**Grounding:** `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_CONTRACT_GAPS.md` and `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_RESULT.md` @ blocked feature commit `1e62383ddc555c06ca2ab9be7ae462f99954c281`; independent blocker review `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_G01_INDEPENDENT_BLOCKER_REVIEW.md`.

## 1. Exact scope of approval

Owner **approves D1, D2, D3 and D4–D5 as written in the linked G01 proposal**. This document records that decision; it does not replace, rewrite or broadly reinterpret the original SI/1 spec, R1, R1a, R1b, SI-D01–SI-D10, previous accepted modules, or their existing SHA/golden vectors. Where G01 addresses the specific HUMAN_EDIT causal→semantic ambiguity, apply this approved narrow clarification. Otherwise prior owner-approved contracts retain their original precedence.

**D1 — HUMAN_EDIT edit-base is causal/audit, not required-current solely by its position.** The exact previous revision in `H.previous`, `H.input_refs[0]` and `REVISION Run.semantic_input_refs[0]` remains mandatory and cryptographically validated for audit/provenance. The older version is not required in the observed active set simply because it was the editing base. Missing/hash-conflicting historical ancestry is **INVALID**, not STALE.

**D2 — typed semantic projection, no auto-rebase.** Required-current dependencies derive from the queried revision's actual typed payload and still-applicable domain-specific producer bindings. A current payload role supersedes a historical binding of that same role; exact new refs must be checked. Inherited producer refs without an applicable override retain their exact SIRef. Do not silently drop conflicting substantive constraints, infer latest, or rewrite immutable Run roots. Unresolved role ambiguity must fail closed and be reported, not guessed.

**D3 — CreativeAlternative K1→K2→K3.** Original CREATIVE Run `C` remains frozen in `payload.run_ref`, distinct from the actual REVISION Run in `H.origin.run_ref`. Historical K1/K2 and C are fully verified for audit, not required-current identities merely by ancestry. Original C's still-applicable exact EvaluationReport and domain/context bindings must be considered in currentness; C's audit input_snapshot/context_snapshot is not the current view. Revised payload angle/claim refs control their corresponding roles. An Angle change incompatible with unchanged original E1/channel/claim constraints cannot become CURRENT by rebasing E1 or silently ignoring the conflict; valid historical but obsolete domain binding is **STALE**. Text-only Creative edits with unchanged substantive bindings can be CURRENT when all required exact refs are active and the ERef boundary is satisfied.

**D4 — scope and boundaries.** Apply D1–D2 to other R1a RevisableRecordSet types using their actual typed payload refs. Brief's actually used Creative Selection compares to explicit observed selection heads; unrelated heads do not stale E1/K. Packet freshness remains separate. Relevant ERef without supplied exact validated editorial snapshot is INVALID, not proof of CURRENT. No truth, approval, identity, rights, execution or authority claims.

**D5 — owner-approved expected cases.** The complete D5 case table in the proposal is approved as the expected-state policy, including: Source S3 CURRENT with S1/S2 inactive but intact; corrupted S2 INVALID; text-only K3 CURRENT with unchanged substantive exact refs; missing active original E1 STALE; incompatible changed Angle STALE (INVALID only on independently established structural/provenance contradiction); E1 unchanged by unrelated selection heads CURRENT; Brief used selection head changed STALE; relevant unvalidated ERef INVALID. Codex must instantiate genuine hash-consistent bundles and precise observed sets, not assert these labels from illustrative aliases.

## 2. What this approval does NOT authorize

D6 in the proposal is a **scope and STOP gate**, not an additional semantic rule. It remains in force. The owner has **not** approved an ERef adapter, RFC implementations, additional fields/record types/error codes, mutable cache, persistence, workspace/SQLite, request execution, semantic fact-checking, auto-latest, reviewer authority, protected writes, SI-E02, PR/merge/release, or changes to `main`.

The previous **SI-E01.2b.3 BLOCKED_CONTRACT** report is valid historical evidence. G01's *specific owner-decision blocker is resolved* by this approval, but **no SI-E01.2b.3 implementation has been accepted or executed**. New implementation is permitted only through a separately published, strict-allowlist `SI-E01.2b.3-RESUME` Codex task with exact branch/SHA, evidence and STOP for independent review. If a new material ambiguity appears, STOP with precise CONTRACT_GAPS rather than extrapolate this approval.

## 3. Unresolved test evidence

The blocked run reported **103 SI tests OK / exit 0**, **945 full unittest methods OK but shell exit 1**, and zero currentness tests / exit 5 because no implementation existed. This approval does **not** turn the full suite into a PASS or diagnose its exit discrepancy. The RESUME task must require a clean full-suite process exit 0 or a separately documented, reproducible explanation and independent owner disposition; no `|| true`, swallowed exit status or unapproved harness edits.

## 4. STOP retained

`PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF; Windows S3.2b BLOCKED_HOST_NOT_PROVIDED. No change to protected editorial/storage boundaries, RFC status, original SI/1 contracts, accepted SI modules or `main`. **STOP after docs publication; owner forwards bounded RESUME task to Codex separately.**
