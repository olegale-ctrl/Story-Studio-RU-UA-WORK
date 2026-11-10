# SI-E01.2b.3-G02 — proposed owner decision on CREATIVE direct ClaimItem inputs

**Date:** 2026-11-10
**Status:** **PROPOSAL / OWNER REVIEW / NOT APPROVED**
**G02 source:** `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_CONTRACT_GAPS.md` and `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_RESULT.md` @ `f549bc4437a2af3e2f1f349ce266715bcc5589e2`.
**Independent review:** `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_G02_INDEPENDENT_BLOCKER_REVIEW.md`.
**Previously approved:** G01 D1–D5 @ `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_APPROVAL_2026_11_10.md`; not reopened. This proposal only closes role exclusivity ambiguity for direct CREATIVE Run ClaimItem roots and has no runtime authority.

## G02-D1 — conservative baseline for flat CREATIVE ClaimItem roots

For a CREATIVE Run C, **every exact direct ClaimItem in `C.payload.semantic_input_refs` remains an independently required-current originating ClaimItem unless an already-approved explicit machine-readable, exclusive role binding can establish otherwise**. Matching an exact ClaimItem to `K1.payload.hook_claim_refs` or `K1.payload.chapters[].claim_refs` demonstrates *use* in that output position, **not that the direct C input was exclusively limited to that position**. In the SI/1 V1 accepted wire schemas C has no exclusive-role annotation, so for existing records there is no inference from list position, duplicate count, text, timestamps, `request_payload_sha256`, or other hidden metadata. A current hook/chapter may contain additional or different refs while immutable C keeps its original input commitments.

Consequently: `K2/K3` human edits may change the hook/chapter ClaimItem refs as permitted by R1a and G01, but removing an originally direct C ClaimItem from the output does **not** erase its exact independent currentness constraint. If that original ClaimItem is missing/replaced in the observed active domain set, currentness is **STALE / INPUT_STALE**, even if the new hook claim is active. This is intentionally conservative, and is not a structural INVALID if the historical bundle is otherwise valid.

This policy **does not** prohibit HUMAN_EDIT, replace original C, treat old K1/K2 as active, promote `Run.input_snapshot` to semantic input, or change approved D1–D5. It narrows the meaning of "same-role override": output hook/chapter usage can be replaced, but exclusivity of an independent CREATIVE direct input cannot be inferred without explicit role evidence.

## G02-D2 — double-use, inherited constraints, and no fabricated roles

Retain exact independent substantive refs when they are established through **any** still-applicable binding (e.g. the original CREATIVE direct input, current Angle/claim/check/evidence/risk link, an original exact EvaluationReport or ChannelContext dependency). A claim used in both hook and chapter must remain required if any original independent producer constraint or current substantive role still requires it. Do not deduplicate away role meaning, grant a removed hook authority to cancel a retained Check/Risk/qualification, or mistake a mere audit-only occurrence for current relevance.

Distinguish **direct C.semantic_input_refs** from C's **audit-only Run.input_snapshot/Run.context_snapshot**, which are never promoted to required-current because they contain old refs. Preserve original C's exact E1/Channel/other still-applicable producer inputs as required by G01. Current output payload hook/chapter refs also become required-current by their own typed domain roles; the retained original direct C ClaimItem and new hook ClaimItem are both checked when they differ.

Do not allow silent latest, auto-rebase, invented role annotations, opaque commitment decoding, or trusted editorial/execution claims.

## G02-D3 — fixed expected cases to approve

| Scenario (all refs valid, exact original audit bundle) | Required-current claim constraints | Expected |
| --- | --- | --- |
| **Exact G02 synthetic graph:** C roots include `Qa,Qb`; K1 hook `Qa`, chapter `Qb`; K3 hook `Qc`, chapter `Qb`; observed active includes `Qb,Qc`, excludes `Qa`; Angle/Idea/E1/Channel unchanged, K1/K2 inactive | `Qa` (retained exact C direct root), `Qb` (C + chapter), `Qc` (current hook) | **STALE / INPUT_STALE** |
| Same graph; add exact `Qa` to observed active; all other required substantive refs active | `Qa,Qb,Qc` | **CURRENT** (dependency freshness only; not eligibility/rights/review readiness) |
| Text-only Creative K3 edit with unchanged K1 hook/chapter/Angle claim refs and all original direct C ClaimItems active | No obsolete K1/K2 revisions required; exact C substantive producer claims remain active | **CURRENT**, subject to all other domain/ERef checks |
| Qa used for both original hook and chapter; current hook changes to Qc but chapter retains Qa; Qa absent observed | Qa required by chapter and original C | **STALE / INPUT_STALE** |
| Qa also referenced by a still-current ClaimCheck/Risk/Evaluation basis; current hook changes to Qc; Qa absent observed | Qa retained independently | **STALE / INPUT_STALE** |
| Historical Qa record missing/incorrect hash in full audit closure, even if observed active has Qc | N/A, invalid bundle/ancestry | **INVALID** with existing resolver/provenance error |
| New Qc active but unrelated other Selection head changed | No new relevance from unrelated head | Same currentness as before head change |
| Relevant ERef with no supplied exact validated editorial snapshot | No trust from opaque hash | **INVALID**, unchanged G01 boundary |

The G02 reproducer's exact literal bundle/context digests and individual SIRefs remain in source GAPS. Expected currentness states here are **policy proposals**, not outputs of an implemented checker or independently executed tests. For any future code task, construct exact valid literal test oracle cases without fabricating role provenance. For `CURRENT` examples, check *all* required substantive refs and no ERef gap first.

## G02-D4 — implementation consequences and future evolution

If approved, implement a narrowly scoped typed rule for direct C ClaimItem roots as independently retained exact substantive dependencies. Current payload hook/chapter refs retain their own roles; both sets may be required. Other R1/R1a/G01 semantics remain intact. **No new SI field, record type, method, codec, provider, storage, ERef adapter, or test-harness change is approved here.**

The resulting conservative false-stale tradeoff is **deliberate**: a benign hook rewrite can require retaining original exact ClaimItem in active context or creating a new CreativeAlternative through the approved process with updated producer roots; it cannot silently remove immutable generator inputs. Any future ability to prove exclusive hook-only inputs, relax this constraint, or introduce a source-role map requires a **separate contract/wire change and explicit owner approval**. The checker must not use Python heuristics to infer exclusivity.

## Owner decision required

Owner must explicitly **approve or request amendment** for G02-D1 (conservative original direct inputs), G02-D2 (double-use/role semantics), G02-D3 (expected-state cases) and G02-D4 (bounded implementation/no new wire fields). Until then:

**SI-E01.2b.3 = BLOCKED_CONTRACT.** No SI-E01.2b.3-RESUME-2 task is authorized and no implementation may start. After approval, publish a separate owner-approval document and bounded Codex RESUME-2 task on a new docs-only branch, requiring exact base SHA and independent review. The previous G01 D1–D5 remains approved; no revisions to original contracts or accepted historical files.

**STOP:** No SI-E02, RFC changes, ERef adapter, truth/rights/approval semantics, persistence, protected editorial/storage writes, PR/merge/release, or `main` changes. `PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF; Windows S3.2b BLOCKED_HOST_NOT_PROVIDED.
