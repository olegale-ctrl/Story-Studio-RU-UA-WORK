# E01.3.9.1b — Approved Atomic Storage Architecture Decision

**Status: APPROVED BY PROJECT OWNER — architecture only.**
**Decision date:** 2026-11-05.
**Repository:** `olegale-ctrl/Story-Studio-RU-UA-WORK`.
**Source proposal:** `docs/tasks/E01_3_9_1_ATOMIC_STORAGE_PROPOSAL.md`, E01.3.9.1a, commit `afb0e9ccd6edd995e6f5855ffe41627c190fa4e7`.
**Owner decision:** «утверждаю D1–D12 в указанной редакции и пошли дальше» (2026-11-05), referring to the reviewed D1–D12 and the review qualifications below.

This document is the **normative record of the owner's approval of D1–D12**. The proposal remains a historical design proposal: its original “awaiting decision” label is superseded **only for D1–D12** by this decision. Its unimplemented mechanisms, untested platform assumptions and future S1–S8 gates are not thereby declared tested, deployed or ready.

## Approved decisions

| ID | Approved architecture decision |
|---|---|
| **D1** | Protected writes use a dedicated local Windows service identity/service SID and a managed service-owned `ProgramData` project root. Standard-user UI/CLI needs no elevation for normal operations; without the service, only local drafts and safe read-only diagnostics are available. Same-user writable anchor/primary is not equivalent protected authority. |
| **D2** | Select architecture **A**: one authoritative canonical editorial JSON, a protected authenticated file journal, and an external protected head anchor. Adopt proposed W0–W9 protocol with **primary JSON replacement as snapshot commit point**. Separate journal/anchor writes are not falsely described as one atomic filesystem transaction. Switching to B/C requires a new owner decision and, where relevant, a revision of E00. |
| **D3** | Use domain-separated HMAC-SHA-256 for protected storage metadata, a service-only key protected by ACL and Windows DPAPI. Storage MAC does not replace optional schema-2 signatures, human authorization or verified provenance. Key loss blocks trust; no auto-key regeneration to restore it. |
| **D4** | Permit only proof-bound reconciliation from E01.3.9.1a §6.1: verified authenticated prefix extension, pre-intent ABORT where absence of intent is provable, or exact forward completion of B after authenticated intent. Never abort after intent, guess journal records, or recreate a missing anchor. **Reconstruction of a terminal partial COMMIT is a separate optional capability, not enabled in the first implementation until its exhaustive fault tests and explicit acceptance demonstrate safety; otherwise fail closed and require authorized manual recovery.** |
| **D5** | Adopt the §9.3 continuity/history guard. Imported or legacy decisions gain no fabricated order or authority. `CONTINUITY_LOST` cannot be cleared by an administrative acknowledgement, new epoch or checksum. Affected keys remain blocked until a separately approved legacy-resolution/proof contract applies. |
| **D6** | Cross-machine transfer creates an explicitly authorized new machine-bound local epoch/baseline. Foreign approval order/authority remains unverified; known history barriers and consumed request/session IDs cannot be silently erased. Local storage MAC keys are not exported. |
| **D7** | MVP retains complete journal, receipts, tombstones, verified order proofs and committed images. Storage quotas/warnings may block new protected writes, **never silently prune authenticated history**. Configure user-visible warnings and fail closed on insufficient space; choose numeric quotas, backup destination, access and retention parameters before implementation acceptance. No automatic compaction without a separately approved authenticated checkpoint design. |
| **D8** | Separate process-crash consistency from qualified power-loss durability. Require the §5.4/§13.4 acceptance gates and disclose that full privileged rollback of all protected state is outside baseline detection. Do not advertise power-loss durability on unqualified Windows/storage configurations. |
| **D9** | Administrative elevation is needed for installing/maintaining the protected service, ACL and key provisioning only. Initialization, recovery and editorial gate permissions are separately and explicitly granted; neither elevation nor installer status confers all-gate authorization. Reinstall must not reset protected history. |
| **D10** | Introduce a separate versioned storage-protocol v1 boundary with ContentHead/CommittedHead, anchor, framed journal, frozen commands/receipts, and continuity metadata. Closed wire schemas, canonical/MAC rules, deterministic golden vectors and state transitions require separate approval **before executable storage implementation**. Do not add storage fields to editorial schema 2 or alter its digests. |
| **D11** | Unbound review sessions become invalid on restart; reserved IDs are never reused, including after abort. Bound accepted intent replays the same exact transaction rather than creating a new review. Verified ordering never derives from wall clock, UUID or JSON array position. |
| **D12** | First supported target is offline Windows 10/11 on local NTFS and a standard Intel-integrated-graphics CPU-only PC; no required cloud, NVIDIA/CUDA or GPU acceleration. Windows builds and actual storage/controller/cache profiles require testing before corresponding production/durability claims. Network/sync/removable filesystems and Linux/macOS protected adapters are out of initial scope. |

## Binding qualifications and unresolved parameters

1. **D4 — narrow recovery:** deterministic reconstruction of a torn terminal `SNAPSHOT_COMMIT` remains **disabled by default**. S1 must specify it as an independently gated optional transition with exact proofs, negative tests and an explicit fallback to blocked/manual recovery. No automatic tail truncation or repair of partial PREPARE/INTENT.
2. **D7 — storage growth:** the policy is preservation of proofs and images, **not** infinite storage promises. Before production acceptance the owner must approve numeric quota thresholds, user warnings, disk-full behavior, backup placement/access and retention. S1 may propose defaults with trade-offs, but **must not treat suggested numbers as owner-approved**. Existing GitHub repository size limits are unrelated to local protected storage quotas.
3. **D8/D12 — qualified hardware:** define exact Windows builds/editions, NTFS/storage/controller/cache profiles, process-kill matrix and power-loss qualification plan. The initial CPU-only PC is a target class, not evidence that power-loss tests passed. A protected writer cannot be called production-qualified without the required test evidence.
4. The exact protocol wire schemas, recovery proofs, Windows ACL/IPC/service installer, full history/restore handling and authority evaluator remain **future implementation or approval work**. No inherited approval of an S2–S8 task.
5. Preserve E00, A1–A14, O1–O10, all existing schema-1/schema-2 contracts, and the Story Intelligence architecture decision. Discovery/Evaluation/Creative and Production Brief never acquire storage authority or bypass editorial/rights gates.

## Next authorized milestone

The owner authorized **continuing to S1 documentation/design-contract preparation**, not implementing the storage engine.

**S1 output:** a separate **proposal** for a closed v1 storage/command contract with field schemas, canonical serialization/MAC domain separation, deterministic examples/golden vectors, W0–W9 state transitions and journal/anchor reconciliation, exact idempotency/session/order/history invariants, bounded error codes, quota/profile open decisions, and traceability to D1–D12 and E00/A/O. This S1 deliverable remains **UNAPPROVED** until separately reviewed by the owner.

**Explicitly not authorized:** executable code, Windows service, journal/anchor writes, policy changes, PR, merge, release, or changes to `main`.

## Repository hygiene and provenance

Use the project's adopted `docs/GITHUB_REPOSITORY_STORAGE_POLICY.md` from separate commit `ceca15c20cedd5277ad0bdafc418eef149e7bc7b` as a cross-branch reference for subsequent Codex tasks. This decision does **not** claim that policy branch has been merged or that the file exists in this branch. Never commit local protected anchors, journals, keys, backups, media, models, secrets or real personal data to GitHub.

Changes to this decision require a separate owner-approved documented revision; no Codex task may silently reinterpret D1–D12.
