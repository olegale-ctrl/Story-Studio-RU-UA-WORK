# SI-E01.2b.3-G02 — explicit owner approval of D1–D4

**Date:** 2026-11-10
**Status:** **OWNER APPROVED / NARROW CREATIVE ClaimItem CURRENTNESS POLICY ONLY**
**Owner decision:** “договорились утверждаю все 4” — in direct response to the four proposed G02-D1–D4 decisions, following the recommendation to approve each.
**Approved proposal:** `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_G02_OWNER_DECISION_PROPOSAL.md` on `docs/story-intelligence-si-e01-2b-3-g02-owner-clarification` at exact SHA `e191eec53b2938bc0188ba0b579c9738a1beeb8b`.
**Evidence:** `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_CONTRACT_GAPS.md` and `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_RESULT.md` at `f549bc4437a2af3e2f1f349ce266715bcc5589e2`; independent G02 blocker review on the approved proposal branch.
**Previously approved:** G01 D1–D5, `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_APPROVAL_2026_11_10.md`. G01 and earlier accepted SI/1/R1/R1a/R1b are not revoked.

## Decision: approve all four G02 parts as written

**G02-D1 — independent original direct CREATIVE ClaimItem roots.** Every exact `ClaimItem` directly listed in the original CREATIVE Run C's `payload.semantic_input_refs` remains a required-current substantive producer constraint in SI/1 V1, unless an **already approved explicit machine-readable exclusive-role binding** establishes otherwise. The existing V1 schema contains no such binding. Mere appearance of Qa in original `hook_claim_refs` or chapter `claim_refs` proves usage, **not exclusivity**. Changing K2/K3 hook Qa→Qc adds a current Qc payload dependency but does not remove direct C input Qa. Valid historical Qa absent from the observed active set => **STALE / INPUT_STALE**; missing or corrupt Qa in required audit closure => **INVALID**.

**G02-D2 — multi-role and independent constraints.** An exact ClaimItem may be required by the original CREATIVE direct input, current hook/chapter, current Angle, E1, ClaimCheck, Risk, or other still-applicable substantive role. Changing one role never cancels another. Retain exact original E1/ChannelContext and still-applicable C producer bindings per G01; do not promote audit-only `C.input_snapshot` or `C.context_snapshot` to current inputs. Current K3 hook/chapter refs also require exact observed active SIRefs. No inference from order, duplicate count, timestamps, opaque request hash, text, or an unapproved role map; no implicit latest or rebase.

**G02-D3 — owner-approved expected outcomes.** The complete eight-row case table in the approved G02 proposal is binding as test policy. In particular, the exact G02 reproducer has C direct `Qa,Qb`, K1 hook `Qa`, K3 hook `Qc`, chapter `Qb`, observed `Qb,Qc` but no active Qa: **STALE / INPUT_STALE**. Add exact Qa with all other required domain inputs active: **CURRENT**, if the graph is valid and no ERef boundary applies. Text-only K3 with unchanged substantive inputs can be CURRENT without K1/K2 active. Shared hook+chapter Qa or independent Check/Risk Qa absent active => STALE. Missing/hash-broken historical Qa => INVALID. Unrelated Selection head does not change Creative currentness. Relevant ERef without validated exact editorial snapshot remains INVALID. These are *expected policy results*, not results from an already implemented currentness API.

**G02-D4 — bounded implementation and future option.** Implement only a typed pure read-only rule on accepted SI/1 bytes; do not add fields, record types, error codes, codecs, request methods, dependencies, editorial adapters, providers, persistence, protected writes or UI authorization. This conservative policy can produce deliberate false-stale after harmless hook edits, preferring provenance over unsupported automatic constraint removal. Any future **Claim Input Role Map** or proof of exclusive hook-only roots is an **architecture backlog candidate, not approved implementation**; requires a separate owner-reviewed contract/wire/migration/license assessment. G02 does not authorize a new architecture RFC or edits to an existing one.

## Contract precedence and limits

This owner approval resolves **only G02's direct CREATIVE ClaimItem role ambiguity**. Approved G01 D1–D5 still governs HUMAN_EDIT historical base exclusion, typed payload projection, frozen original CREATIVE Run, E1/channel/Angle compatibility, Brief selection, and ERef boundary. All other SI/1, R1, R1a, R1b and SI-D01–D10 rules remain in force. In particular:
- Historical K1/K2, `H.previous`, REVISION edit-base, Run metadata and audit snapshots are **verified**, not automatically required-current domain identities.
- A valid historical-but-no-longer-active substantive dependency is **STALE**, while broken/missing/hash-conflicting required audit records are **INVALID**. `CURRENT` is not evidence truth, scoring/eligibility, approval, execution, identity, rights or production readiness.
- No claim of independent execution of the G02 reproducer or tests is made by this approval. Codex reported **103 SI/exit 0** and **945 full/raw Python exit 0/outer exit 0** at blocked G02 stage; zero currentness tests existed. The older shell-exit anomaly did not recur, but its cause remains unknown.

## Implementation gate and STOP

The historical G02 feature branch remains **BLOCKED_CONTRACT / NO CODE**; the *specific owner-choice blocker* is resolved by this approval. Implementation may begin **only** under the separately published, strict-allowlist `SI-E01.2b.3-RESUME-2` Codex task from its exact docs-branch SHA. If any new material ambiguity appears, STOP with new CONTRACT_GAPS; do not infer new policy from this approval. Publish a feature branch and STOP for independent review; do not start SI-E02 or any other stage.

**Retained STOP:** no PR/merge/release or `main` changes; no RFC/ERef adapter, actual execution, provider, fact-checking, reviewer rights, persistence, editorial/storage protected writes. `PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF; Windows S3.2b BLOCKED_HOST_NOT_PROVIDED.
