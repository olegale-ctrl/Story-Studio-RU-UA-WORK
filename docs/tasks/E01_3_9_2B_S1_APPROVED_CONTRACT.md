# E01.3.9.2b — Approved Storage & Command Protocol v1 (S1)

**Status: APPROVED BY PROJECT OWNER — normative protocol contract; not an implemented or qualified storage system.**
**Decision date:** 2026-11-06.
**Repository:** `olegale-ctrl/Story-Studio-RU-UA-WORK`.
**Approved source revision:** `docs/tasks/E01_3_9_2_S1_STORAGE_COMMAND_CONTRACT_PROPOSAL.md` at commit `83ac4ac3fa5104a9a43bc2fa5f98d735a694f49c` (S1a).
**Owner instruction:** «утверждаю S1 переходим к S2» (2026-11-06).

This file records the owner's approval of **S1 as amended by S1a**. The historical source file may retain its `PROPOSAL` heading; **this approval document supersedes that status for the S1 normative contract at the exact commit above only**. No later or earlier variant is automatically approved. S1 approval does not certify runtime behavior, OS security, power-loss durability or production readiness.

## 1. Normative scope approved

The following requirements in the exact approved S1 source revision are binding for subsequent S2 work:

1. Closed protocol v1 schemas and exact validation rules: ContentHead/CommittedHead, HistoryGuard and typed blobs, Request, FrozenCommand, Authorization, TransactionPlan, AnchorState, journal framing/records, initialization/registration and receipts; version/enum/field/length/counter rules (§2, §4–§7).
2. Canonical UTF-8 JSON and domain-separated SHA-256/HMAC-SHA-256, exact dependency ordering without cyclic COMMIT references, and literal synthetic golden vectors (§2–§3, §13). Test vectors are **normative expected outputs**, not evidence of an implemented secure key/provider.
3. Admission, idempotency, frozen request/authorization, exact gate×decision permissions, protected policy lookup, no implicit grant inheritance and session binding (§5, §10). The normative **policy/provider boundary** is approved; concrete Windows token, IPC, ACL, installer and policy deployment remain subject to implementation and separate tests.
4. W0–W9 transaction states, primary snapshot replacement commit point, explicit persistence barriers, genesis/ABORT/exact-head repair, proof-bound reconciliation, complete authenticated journal/anchor checks, replay and exact receipts (§8–§9).
5. Immutable verified approval order, retained negative decisions/REVOKE barriers, import/transfer/backup/restore restrictions and continuity fail-closed semantics (§4, §10–§11).
6. Closed error classes, deterministic failure precedence, invariants, negative cases, test expectations and traceability (§12, §15).
7. The operation tag `PUBLISH_REVISION` is **reserved and DISABLED**. It cannot be admitted, dereferenced, written or replayed as a valid v1 operation until a separately approved closed revision-proposal/builder contract and corresponding protocol revision. No generic arbitrary JSON snapshot write is permitted (§5.3).
8. **Partial terminal COMMIT reconstruction is OFF.** No automatic reconstruction of torn terminal COMMIT or guessed/truncated journal tail. Enabling it requires a separate owner decision and exhaustive negative/fault tests (§9.1).
9. No change to E00, approved A1–A14/O1–O10/D1–D12, existing schema-1/2 editorial bytes or attestation rules, or Story Intelligence's non-authoritative discovery/evaluation/creative outputs.

## 2. Matters deliberately NOT approved by this decision

The owner approved **S1**, not an independent numerical or hardware selection. S1 §14 explicitly labels these as proposals; they remain open:

- **Q1 numeric capacity/backup policy:** suggested 32 GiB retained per production, 80% warning, +64 MiB reserve and 2 GiB free-space floor, weekly/pre-maintenance backups and four validated bundles are **not yet owner-approved settings**. They may be modeled as explicit *test parameters*, never deployed defaults or silently asserted as accepted. Backup destination/access/privacy/retention remain owner decisions.
- **Specific qualified Windows/hardware profiles:** W11-N, W10-S and VM-F in S1 §14.2 are templates, not accepted exact build/UBR, controller, firmware, caching or power-loss qualifications. Windows 10 support depends on a maintained security configuration. Offline CPU-only Intel iGPU + local NTFS remains the approved target class (D12).
- **Revision publication:** no enabled PUBLISH_REVISION, proposal schema, builder, permissions or arbitrary snapshot publication.
- **Provider deployment:** exact production OS principal extraction, protected policy store/update synchronization, service identity, ACL, DPAPI key lifecycle, IPC and installer remain unimplemented and unqualified.
- **Legacy resolution, disaster-recovery key export, compaction, rotation and optional partial COMMIT reconstruction:** no permission to implement or enable by implication.
- **Production durability claims:** process-kill and physical power-loss guarantees must be demonstrated separately. GitHub repo size policy is not a quota for local protected storage.

## 3. Next milestone authorized: E01.3.9.3 / S2

Proceed with a **pure deterministic in-memory protocol model and tests**, implemented in isolated new Python modules. S2 may encode and validate S1 protocol structures, model authenticated journal/anchor states, transition/reconcile over an injected virtual store, reproduce vectors and perform deterministic fault injection. Use **synthetic fixtures and explicitly injected fake keys/authorization decisions** only; fake permissions are test inputs, not trusted production identity or real editorial approvals.

S2 must **not** implement or touch actual Windows service, DPAPI/ACL/IPC, privileged paths, real protected primary/journal/anchor, filesystem flush/replace, backup, key provisioning, network or media. It must not expose an executable production writer or claim security/durability. A test-only virtual persistence adapter may simulate barrier events and crashes; actual OS durability remains for a later stage. No changes to existing approved editorial models, contracts or their golden bytes.

S2 work may be split into independently reviewable substeps (e.g. protocol primitives/vectors, then state machine/fault tests) to avoid mixing unverified serialization and recovery logic. Each substep requires exact branch/SHA, scope, tests and independent review before continuation. The S1 normative text may not be silently modified during S2; any discovered ambiguity is documented and returned for owner decision.

## 4. GitHub provenance and scope control

- This decision is added as **one docs-only file** on a feature branch based exactly on S1a commit `83ac4ac3fa5104a9a43bc2fa5f98d735a694f49c`.
- Follow the repository storage policy in the separate policy commit `ceca15c20cedd5277ad0bdafc418eef149e7bc7b`. That policy branch has **not** been assumed merged into this lineage.
- Never commit real keys, personal information, service artifacts, journal/anchor backups, models or media. Do not merge, create PR, release or change `main` without separate owner permission.
- Changes to the approved S1 normative contract require an explicit documented revision and owner authorization; do not treat implementation convenience as approval.
