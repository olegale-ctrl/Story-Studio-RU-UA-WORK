# MVP-08B.2a-FIX-01 — Final handoff

Status: **PROPOSAL / DOCS_ONLY — OWNER REVIEW REQUIRED**. Date: 2026-11-20.

Project status remains **BLOCKED_CONTRACT**. This document proposes resolution of accepted findings; it does not approve EC-01–EC-10, G1–G6, implementation, real APIs, spending, storage, CI, main, merge, release or production permissions.

Source precedence: owner instruction in this conversation accepting the limited audit and F01–F05; exact independent review `3744eb5584e72e338dc51fa3a6fe7aed4882651b`; original freeze `c5cd33023880fd6726b74f5631eb766cc0959892`; original B.1 `f0bce140451bf00a86f3939330e77ed63b2c98be`; B.2 `04ea194e4d57c8a0550d7412281da58d4ba252c5`; SP/1.1 `16d28ec0376c8c28f879c8aacb18d5378fea83a3`. Historical documents remain unchanged. New PURE records below are proposals, not replacements for approved external contracts.

## Result and review boundary

**Document package: READY_FOR_INDEPENDENT_REVIEW. Project: DOCS_ONLY / BLOCKED_CONTRACT.** Resolution proposals for F01–F05 are written; independent confirmation and owner G1–G6 decisions are still pending. No assertion that contract findings are independently closed, EC choices approved, implementation authorized or production qualified is made.

Branch: `docs/mvp-08b-2a-fix-01-contract-ambiguity-resolution`.
Exact base: `3744eb5584e72e338dc51fa3a6fe7aed4882651b`, tree `6d30b37dc07e88b2b5eec773de93a23be1879eef` (independent review, parent original freeze c5cd330).
The final commit/tree and file blob SHA/SHA-256 are recorded in the accompanying external manifest and final response. They cannot be self-embedded into a file that contributes to that same commit/tree without circularity.

## Exact change scope

Only six new Markdown documents in `docs/tasks/MVP_08B_2A_FIX_01/`:

| File | Purpose |
|---|---|
| CONTRACT_RECORDS_AND_PREIMAGES.md | F01: 25 closed hash kinds, transport boundary, 36 canonical value examples |
| ACTIVE_INTENT_AND_ADMISSION.md | F02: active slot, replay/conflict and terminal release semantics |
| COMMIT_RESTART_AND_FENCING.md | F03/F04: tri-state commit, stable identity, restart/ownership and reservations |
| ERROR_AND_ORACLE_MATRIX.md | F05: exact codes, precedence, counters and corrected source-oracle crosswalk |
| PURE_CORE_GATE_PROPOSAL.md | Pending G1–G6, F06/F07 boundary and proposed narrow future scope |
| FINAL_HANDOFF.md | Status, provenance, validation limits and STOP |

No existing Markdown, implementation, workflow, contract source or main is modified. No PR/CI/model/runtime/store execution is requested or performed. The supporting scripts outside the repository calculate document examples and verify Git/Markdown evidence; they are not a GenerationJob/JobStore implementation.

## Source evidence and independent-review instructions

Read the original independent review CONTRACT_FINDINGS.md, EC_DECISION_MATRIX.md, MVP_08B_3_IMPLEMENTATION_GATE.md and OWNER_HANDOFF.md at the exact base. Compare original B.1 JOB_CONTRACT/STATE_MACHINE/RECOVERY_MATRIX/TEST_ORACLES and original freeze before judging these proposals. B.2 and SP/1.1 remain exact historical sources; do not use this addendum as a replacement for their Asset Library/Route D contracts.

Check especially: all hashed shapes closed and acyclic; no authority from typed digest; active slot cannot be bypassed by changing request/batch; terminal replay does not reopen; unknown COMMIT never implies absence; unresolved identity survives only as explicit fake precondition; current fences authorize applying old immutable proofs; cancellation follows SM31; three calls includes initial; stale callers write nothing; prefix metadata is not MP4 evidence. New proposed PURE fake records must not be confused with approved real contracts.

External packet contains source commit/tree and blob/SHA-256 manifest, exact diff, changed-file manifest, 36 canonical vectors/hex and arithmetic comparison. An independent reviewer should recompute hashes and apply the patch to the exact base tree. Review arithmetic separately from schema, transition and security semantics.

## Verification actually performed

Document arithmetic: Python local encoding expression and independent Node typed-AST renderer agree for 36 byte/digest examples; exit code 0. Source encoding expression checked without importing the implementation. Git object/base/tree and docs-only diff checks are recorded externally. These are documentation/evidence checks; no runtime acceptance tests executed.

| Qualification | Actual result |
|---|---|
| Canonical example arithmetic | PASS for fixed document examples only |
| Future A01–A10 / R01–R16 / E01–E20 | NOT_RUN |
| Pure GenerationJob implementation | NOT_RUN; not authorized |
| SQLite/durable store/power loss/recovery | NOT_RUN |
| Windows native ownership/path/clock | WINDOWS_NOT_RUN |
| Asset ingestion/project save/real MP4 | NOT_RUN |
| Provider requests/paid services/production | STOP; not authorized |

## Open decisions and remaining blockers

All G1–G6 and EC01–EC10 remain OWNER_DECISION_PENDING. Review must determine whether F01–F05 proposals eliminate contradictions without weakening original boundaries. Proposed new PURE type namespace, exact messages/precedence, slot lifetime, fake commit/restart model, virtual limits, observe-only scope and new stage name are not owner-approved. Durable storage, native clock/reparse/TOCTOU defense, real rights/media and live provider qualification remain later separate gates. No automatic claim of exactly-once execution, durable Windows safety or commercial qualification is made.

**STOP.** Await independent ChatGPT review and separate owner decision. Do not start MVP-08B.3, create JobStore/Dispatcher implementation, change main/CI, merge, release, launch models, call real providers, spend funds or grant production permissions.
