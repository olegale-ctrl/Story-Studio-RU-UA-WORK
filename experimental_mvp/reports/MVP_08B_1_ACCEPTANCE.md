# MVP-08B.1 — Independent contract-review packet

**Final status: READY_FOR_INDEPENDENT_MVP_08B_1_CONTRACT_REVIEW.** Date2026-11-18. New architecture is PROPOSAL — NOT APPROVED FOR IMPLEMENTATION. Runtime/new-oracle execution NOT_RUN; Windows WINDOWS_NOT_RUN; provider API NOT_RUN; payments NONE.

Evidence labels: EXISTING = inspected base APIs/historical reports; APPROVED = owner acceptance/D01–D08; PROPOSED = new contracts/oracles; OPEN = OD01–OD08; NOT_IMPLEMENTED = all new Dispatcher/simulator/ingestion behavior.

## Exact authority and source baseline

Repository `olegale-ctrl/Story-Studio-RU-UA-WORK`; branch `docs/story-studio-experimental-mvp-08b-1-dispatcher-contract`. Base commit `1ff403e47d35adb34139278de1d056fbbc563e6d`, base tree `2fecb71e711861431a775f4aa3764d771f35ecb5`. Research reference `f4661c86103bbcedf304201202203f20f3bb2747`, exact eight documents read directly, no branch merge. External source inventory contains 22 exact Git source records:6 Python interfaces,8 base reports including unchanged owner decisions,8 research documents, each with blob SHA1/content SHA256 and snapshot. I01–I16 in architecture inventory identify source symbols/behavior/limitations.

APPROVED owner decision: MVP-08A OWNER_ACCEPTED_WITH_LIMITATIONS and this stage CONTRACT_PREPARATION_ONLY, recorded in a new owner-acceptance document. Original D01–D08 file remains byte-for-byte unchanged. Prior candidate acceptance/test reports remain historical; their 837 passed/2 skipped results are **not new tests in this stage**. Independent review text itself was not provided; only the owner task's acceptance assertion is recorded, without fabricated findings.

## Fifteen changed documents

1. [MVP_08A_OWNER_ACCEPTANCE.md](MVP_08A_OWNER_ACCEPTANCE.md) — new owner decision, accepted SHA/tree, limitations and STOP.
2. [MVP_08B_1_ARCHITECTURE.md](MVP_08B_1_ARCHITECTURE.md) — exact interface inventory, mutation/errors/atomicity, reuse/gaps, D/P1 traceability.
3. [MVP_08B_1_JOB_CONTRACT.md](MVP_08B_1_JOB_CONTRACT.md) — GenerationJob v1, immutable request/grant history, execution/result/related records.
4. [MVP_08B_1_STATE_MACHINE.md](MVP_08B_1_STATE_MACHINE.md) —22 states,38 explicit transition rules with W/preconditions/authority/effects/recovery/errors.
5. [MVP_08B_1_PROVIDER_ADAPTER.md](MVP_08B_1_PROVIDER_ADAPTER.md) — provider-neutral interface, separate capabilities/entitlements/prices/rights; no guessed Wan version.
6. [MVP_08B_1_OFFLINE_SIMULATOR.md](MVP_08B_1_OFFLINE_SIMULATOR.md) —18 deterministic scenario specifications, virtual clock, durable simulator ledger, no sockets/charges.
7. [MVP_08B_1_BUDGET_QUOTA.md](MVP_08B_1_BUDGET_QUOTA.md) —$0 guards, reservations, unknown billing, expiry and reapproval; no live free-credit inference.
8. [MVP_08B_1_RESULT_INGESTION.md](MVP_08B_1_RESULT_INGESTION.md) — proposed transport/SSRF limits, exact media/result identity, DFE-v1 and Library mismatches.
9. [MVP_08B_1_ASSET_HANDOFF.md](MVP_08B_1_ASSET_HANDOFF.md) —11 saga checkpoints, unknown import hold, exact asset/target and saved-JSON authority.
10. [MVP_08B_1_RECOVERY_MATRIX.md](MVP_08B_1_RECOVERY_MATRIX.md) —26 failure scenarios with charge/asset risk, confirmations and oracles, cancellation by phase.
11. [MVP_08B_1_SECURITY_RIGHTS.md](MVP_08B_1_SECURITY_RIGHTS.md) — rights/data/credential/retention boundaries and P1-02 lifecycle protocol.
12. [MVP_08B_1_TEST_ORACLES.md](MVP_08B_1_TEST_ORACLES.md) —78 meaningful executable-ready specifications, **all NOT_RUN**, not executable tests.
13. [MVP_08B_1_IMPLEMENTATION_PLAN.md](MVP_08B_1_IMPLEMENTATION_PLAN.md) — proposed .2/.3/.4/.5 stages, entry/exit/STOP, no current implementation authority.
14. [MVP_08B_1_OPEN_DECISIONS.md](MVP_08B_1_OPEN_DECISIONS.md) — OD01–OD08, recommendations NOT_APPROVED, concrete blocking scopes/defaults.
15. This acceptance index.

All changes are new Markdown under experimental_mvp/reports/. No executable code/tests,existing reports,main,CI,normativePG/G3.2.1,production storage or permissions changed. No simulator,media fixtures or downloads generated in this task. External JSON tables/scripts are documentation consistency evidence, not a Dispatcher/test runtime.

## Core findings and remaining gates

P1-01: existing nb_frames remains reported metadata, not actual decoded-count proof; new DFE-v1 requires separate complete evidence and explicit mismatch handling. P1-02: existing Tcl mitigations/Linux passes do not close native lifecycle risk; future ownership/isolation/stress and actual Windows qualification required. P1-03: Library links are historical; JSON is authoritative.11-step saga never invents cross-resource atomicity or completes from a GUI/link acknowledgement alone.

OD01 exact live profile; OD02 unique Library ingestion receipt; OD03 stable project identity/save coordination; OD04 decoded-frame/media policy; OD05 grant authority/expiry containment; OD06 Tk worker isolation; OD07 store/network/resource qualification; OD08 retention/deletion authority. These block specified **future** stages/actions, not preparation of this contract. No need to reopen D01–D08. Missing sources/base mismatch are not blockers here: exact sources are available. No implementation was used to conceal unresolved questions.

No automatic resubmit after unknown provider outcome/charge. No blind re-import after ambiguous Library commit. No re-generation for failed attachment/save. Same bytes do not merge rights/provenance. No stale overwrite,automatic model fallback,implicit approval renewal or live API activation from a$0 budget. COMPLETED is an exact saved-version receipt, not permanent authority to restore old scenes after later edits.

## Documentation verification and external evidence

Checks cover exact base/tree and parent, 15-file reports-only allowlist/new100644 modes,UTF8/relative links/table shape,all 22 states and 38 rules including terminal/uncertainty/continuation constraints,reachability as a **static graph only**,all 78 oracle IDs/required fields,26 recovery scenarios/coverage,18 simulator scripts,OD01–OD08 defaults,transition↔oracle references,D01–D08/P1 traceability,exact source blob hashes and unchanged D01–D08/executable files. `git diff --check` and candidate tree reconstruction from exact base are recorded externally. Passing documentation checks is not proof of runtime safety or execution of the proposed state machine.

Machine-readable results and exact check count: external `document-consistency-results.json`. External packet includes exact full-index diff,all15documents,Git blob/content SHA manifest,source-reference inventory and snapshots,open-decision register,state/oracle/recovery/simulator tables,transition traceability,validation/reproduction scripts and results,remote branch/main verification. Final commit/tree and archive SHA256 are in handoff and external ACCEPTANCE_PACKET.json/ARCHIVE.sha256; a document cannot embed its own containing commit hash without circularity.

Runtime/FFmpeg/GUI/new tests/Windows/provider calls are NOT_RUN in this documentation stage. Git and documentation parsing/hash checks were performed; no runtime pass claims inferred from old evidence. No new accounts,payments,credits,credentials,browser automation or production permissions.

## STOP

Hand off for independent ChatGPT audit and explicit owner decision. Do not implement Dispatcher or Wan adapter, start .2 automatically, change main/CI/PG/storage,merge,release or grant production permissions. All new recommendations remain PROPOSAL.
