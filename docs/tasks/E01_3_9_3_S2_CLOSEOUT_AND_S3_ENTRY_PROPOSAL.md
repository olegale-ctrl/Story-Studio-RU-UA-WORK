# E01.3.9.3 — S2 Closeout / S3 Entry Proposal

**Date:** 2026-11-06.
**Status:** S2 independently code-reviewed and accepted for *pure in-memory protocol modeling*; S3 is a **proposed design task**, not an approved implementation.
**Base SHA:** `21b1f06c1560ff65e6dc9c47ac9a972e5a3f2879` (S2.4).
**No PR/merge/release/main changes.**

## Verified lineage of S2

1. S2.1 wire/crypto: `c91c7b30ff64ce9f83702f3ecd4b2a2c92ca3335`. Pure canonical JSON, hashing/HMAC, frame validators, golden vectors. Report: 69 new tests and 20 SHA-256 / 10 HMAC literals.
2. S2.2 virtual W0–W9, proof-bound recovery: `301aed34b72b0a8bb714a41e540d7e1abdbf9e98`. Report: 79 model tests, full 787, 344 fault matrix scenarios.
3. S2.3 independent adversarial fixtures: `d816f1b94a71e04363371d9bc05b06f52a7fc0d6`. 13 tests / 1,659 parameterized scenarios. The originally red D-01 test showed retained parent epoch alias was incorrectly accepted.
4. S2.4 minimal D-01 correction: `21b1f06c1560ff65e6dc9c47ac9a972e5a3f2879`. The model now compares `LineageEntry.storage_epoch_id` to `_scan(parent).registration.storage_epoch_id` before inherited IDs/decisions/order or any W1/PREPARE writes. D-01 unchanged original test passes. Eight additional regression methods cover positive parent transfer, mismatched epoch, anchor/journal and negative history. Report: S2.3 13 OK, S2.2 87 OK, S2.1 69 OK, full discovery 808 OK.

**Independent review boundaries:** GitHub exact branch SHA/file scope and code diff inspected; existing D-01 reproducer checked unchanged. Reported .venv test execution was done by Codex, **not independently rerun** by the reviewer. No evidence of production OS-level security, crash/power-loss durability or service functioning is claimed.

## Scope and outstanding boundaries

- Normative S1 source: `docs/tasks/E01_3_9_2B_S1_APPROVED_CONTRACT.md` and approved S1a source, with prior E00/A1–A14/O1–O10/D1–D12 retained.
- `PUBLISH_REVISION` remains disabled; optional partial terminal COMMIT reconstruction remains OFF.
- Q1 numeric quotas, retention/backup cadence and Windows qualification profiles are **not owner-approved**. Treat their values as proposals, not production constants.
- There is no Windows service, IPC authentication, DPAPI/ACL/key provisioning, real filesystem atomicity, actual backups, real operational recovery or security qualification.
- Earlier Story Intelligence / natural narration research is a **separate editorial track**; neither merged nor required for S3. The D-01 remediation is completed in S2.4, not in that editorial branch.

## Suggested S3 staging

### S3.1 — Windows protected-storage qualification and executable implementation spec

**Design-only**, no runtime implementation. Identify production boundary/identity, key lifecycle, service-only writes, request/gate/decision grants, IPC/frozen authentication, local NTFS durability assumptions, filesystem atomic replacement and directory flush feasibility, lock recovery, journal/anchor recovery/reconciliation, retention/backup/free-space operational policy, service-less draft behavior, log privacy, migration cutover and rollback.

Specify platform qualification cases on real Windows 10/11 + NTFS with user-level and service-level accounts, security failure cases, power cut / process-kill / disk-full / permissions testing, offline/CPU-only behavior, and explicitly unqualified network shares/removable/cloud filesystems.

Treat numeric Q1 policy and W11-N/W10-S/VM-F profiles as *open owner decisions*. State alternatives, rationales and conservative defaults, but do not encode as approved values.

Deliver in an isolated documentation-only branch from the exact S2 closeout SHA; solicit owner review and **STOP**.

### S3.2 — Windows service skeleton, after S3.1 contract approval

Service boundary, IPC and authenticated identity skeleton; no protected write without matching scoped grants; tests against mock store; no real key exposure or assumption of approved quotas. Each implementation and test stage gets separate Codex task/review.

### S3.3 — Protected NTFS writer and recovery qualification

Only after separately approved Windows environment/backup/key decisions; use explicit Windows permissions and key store. Conduct offline process-kill / corruption / fault-injection tests in isolated nonproduction test directories with synthetic keys; never claim real power-loss durability solely from virtual tests.

## Safeguards for next task

1. Keep S2.1–S2.4 tests and golden vectors unchanged.
2. Never merge into main or create PR/release absent owner's explicit instruction.
3. No large assets, secrets, keys, production data or protected artifacts in Git.
4. Do not start S3 code before the owner has reviewed and approved S3.1, any unresolved Q1 decisions and platform assumptions.
