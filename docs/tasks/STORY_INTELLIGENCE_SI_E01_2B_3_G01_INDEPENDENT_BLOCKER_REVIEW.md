# SI-E01.2b.3 — independent review of G01 BLOCKED_CONTRACT

**Date:** 2026-11-10
**Decision:** **BLOCKED_CONTRACT CONFIRMED / NO IMPLEMENTATION ACCEPTED**.
**Blocker commit:** `1e62383ddc555c06ca2ab9be7ae462f99954c281`.
**Exact base:** `658212f9a8f5e91a5af9551093cbd85d7512c08a`.
**Scope:** independent static GitHub verification of Codex's STOP and the owner-facing contract question, not a redefinition of approved R1/R1a.

## Publication evidence

- Remote `feat/story-intelligence-si-e01-2b-3-pure-semantic-currentness` at exact announced commit; one commit ahead of exact source base, zero behind.
- Diff is two newly added files only: `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_CONTRACT_GAPS.md` (+140), `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_RESULT.md` (+96). No currentness code, tests or vectors.
- `main` remained `e1f4efb0fb5ff290bb198349213c004b4667ef0f` at review. No PR found.
- Codex-reported targeted SI suite: **103 OK, exit 0**. Currentness pattern: **0 tests, exit 5**, as expected from absence of newly written tests; not PASS. Full suite: **945 OK per unittest summary, but shell/session exit 1**. The latter is **not a full-suite PASS**; root cause not established. Do not label the runtime failure a known baseline failure, and do not waive it for implementation acceptance.
- `git diff --check` and clean worktree are Codex-reported; historical code unchanged by the independently checked GitHub diff. No independent Python suite execution.

## Contract review: why the STOP is valid

Approved R1 §1.2 says `active_input_refs` carry current domain refs, excluding previous/history-only and Run metadata, with only one exact revision per (type,id). R1 §1.3 declares `Run.semantic_input_refs` to be direct operation inputs. R1 §2 and R1a §2–4 require `REVISE_INPUT` Run semantic roots to start with the exact previous revision, then payload refs. R1 §4.2 says SemanticClosure follows substantive payload refs plus origin Run.semantic_input_refs, excluding generic H.previous, audit snapshots, and context metadata. Thus merely removing H.previous traversal leaves the exact same obsolete base in a REVISION Run's required semantic roots.

The genuine ERef-free SourceItem S1→S2→S3 example in GAPS (verified resolver/provenance) demonstrates the conflict: `observed_active_input_refs=[S3]` is valid, while recursively retaining R3's exact edit-base S2 and R2's edit-base S1 makes a freshly edited S3 incorrectly STALE. A second real K1→K2→K3 Creative case demonstrates the opposite failure: skipping all provenance/original-CREATIVE Run roots loses the originating EvaluationReport/Channel/context substantive dependencies, because Creative payload has no explicit evaluation_ref. Both are plausible consequences of ambiguous role-aware traversal; choosing either silently changes the approved currentness semantics.

The G01 report carefully distinguishes this unresolved role projection from ERef: approved R1 §1.2 already requires INVALID when a relevant exact editorial snapshot is not provided, so ERef absence is not an additional necessary blocker for the ERef-free reproducer. Correct pure implementation requires owner-approved **causal-operation vs semantic-currentness projection** and test vectors, without new metadata or an editor adapter unless separately approved.

## Owner recommendation (NOT YET APPROVED CONTRACT)

Propose a small amendment: distinguish (a) immutable causal/audit edit base, (b) substantive dependency references of the **queried current revision** and (c) original CREATIVE Run's frozen substantive inputs, with **explicit replacement/override by current payload role** and no auto-latest resolution. Old version identities must never be required in the observed active set purely from `previous` or from their REVISION Run's first semantic root. Current domain references remain exact and cannot be silently rebound; original CREATIVE Run stays auditable and contributes required evaluation/context dependencies only under an explicit approved rule that explains updates and conflicts. Do not treat approval of this recommendation as implicit in R1/R1a.

A separate `_G01_OWNER_DECISION.md` may be proposed for approval; until then, this review is evidence and recommendation, **not authorizing implementation**.

## Exit-code evidence issue

Before accepting future SI-E01.2b.3 code, require a full clean-suite execution whose **process exit is 0**, or a separate independently diagnosed, documented environment/execution defect and owner disposition. The existing report's `945 OK` alongside exit 1 is insufficient full-suite evidence. Do not change unrelated CI/test harness or scripts within the SI-E01.2b.3 allowlist. Any diagnostic work should be read-only and separately bounded.

## STOP / retained gates

**SI-E01.2b.3 remains BLOCKED_CONTRACT.** Previous SI-E01.2b.2/F1, SI-E01.2b.1 and local typed foundation acceptances remain valid in their limited scope. No SI-E02, performance/RFC implementation, ERef adapter, workspace, operation execution, PR/merge/release, main change, protected storage writes; `PUBLISH_REVISION` DISABLED, partial COMMIT reconstruction OFF, S3.2b BLOCKED_HOST_NOT_PROVIDED.
