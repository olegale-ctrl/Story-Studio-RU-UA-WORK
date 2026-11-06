# E01.3.9.4 / S3.1 — Independent Review and S3.2 Lab Gate

**Date:** 2026-11-06. **Status:** S3.1 accepted as a completed design-only deliverable; Windows mechanisms remain **PROPOSAL**. **S3.2 implementation NOT AUTHORIZED**. This report does not approve O-WIN items or authorize deployment.

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`
S3.1 branch: `docs/editorial-e01-3-9-4-s3-1-windows-storage-spec`
Reviewed commit: `2cd694ece9fa3806bcfbdd1e92f34a9c773b7aef`
Exact base: `76c3478ed243317acc833eff5cfe2d767e886d11`

## 1. Independent GitHub scope verification

- Compare base/head: ahead 1, behind 0, exactly one commit.
- Exactly two added documents: `docs/tasks/E01_3_9_4_S3_1_WINDOWS_STORAGE_SPEC.md` (665 content lines, blob `7c779bc88d176e51804896d7b8ec77f6aadfbd32`) and `docs/tasks/E01_3_9_4_S3_1_RESULT.md` (123 content lines, blob `fdcf43f4ad410ac818e270cf3ce7b5a454fcd8ed`).
- No changes to code, E00/A/O/D/S1 contracts, S2 tests or golden vectors. `main` at review time: `e1f4efb0fb5ff290bb198349213c004b4667ef0f`. No PR found for S3.1 branch; no PR-triggered workflow runs found.
- Unit tests and actual Windows/service tests **were not run by the reviewer**; Codex reported documentation checks, not executable qualification.

## 2. Technical assessment

- All WS01–WS12 contain candidate mechanisms, normative references, failure behavior, verification, residual risks and approval markers. The 14 gates T01–T14 and decisions O-WIN-01–O-WIN-08 are explicitly listed.
- The notation `I` (approved invariant), `F` (documented API fact), `P` (proposed mechanism), `Q` (qualification) correctly prevents mistaking design from tested OS guarantees.
- S1 W0–W9 ordering and W5 namespace replacement / W8 finalization separation preserved. No fictitious multi-file atomic commit or Windows directory fsync.
- `MoveFileExW` candidate does not claim power-loss durability. `ReplaceFileW` unsupported WRITE_THROUGH semantics are not treated as a guaranteed fallback.
- Named pipes: SID from impersonated token rather than request data, explicit pipe DACL/server authentication, scoped command + 12 independent gate/decision grants, fail-stop on RevertToSelf failure. Concrete access masks/resource bounds still open.
- DPAPI current-user service profile proposed without silent LOCAL_MACHINE fallback, auto-key regeneration or invented key rotation.
- Retained lineage D-01 authenticated parent epoch gate maintained. Journal/anchor/negative decisions/receipts and safe failure when proofs are incomplete are preserved.
- Q1-A historical numbers and Q1-B owner-sized policy are **unapproved**; W11-N/W10-S/VM-F specific host profiles are **unapproved**. T01–T14 are test plans only, not observed evidence.
- S3.2 first scope: isolated service lifecycle + IPC/identity + bounded S1 parsing against mock store/provider, not real storage, backups, keys or migration.

**Review verdict:** S3.1 design deliverable accepted for document completeness and compatibility; this does not approve proposed native mechanisms, certify real Windows behavior, or allow S3.2 executable code.

## 3. Required owner decisions before lab coding

### L-01 — Lab service and identity

Proposed separate lab SCM service `StoryStudioBrokerLab`, separate pipe, install directory and synthetic root/fixtures. No production service endpoint, identity, keys, actual history, registration or approval. Non-SCM test harness is possible for preliminary tests, but must not count as SCM qualification.

**Decision required:** exact Windows lab VM/host, installer permissions, service account, service SID (RESTRICTED vs UNRESTRICTED), binary/search-path protection and uninstall lifecycle. No silent security downgrade.

### L-02 — IPC test contract and resource bounds

Proposed versioned **lab-only** named-pipe endpoint; strict bounded S1 parser (1 MiB); reject remote/anonymous clients and unknown fields; explicit DACL and per-message impersonation/revert; OS-backed client checks of server identity. Do not create a generic file-write/upload/review control channel.

**Decision required:** closed lab endpoint naming, SDDL/access masks, SQOS/token requirements, max workers, operation/request timeouts and cancellation semantics, server PID/service identity attestation, lab response wrapper and deterministic fail-closed behavior. These values must be reviewed before coding, not guessed.

### L-03 — Mock authority and storage boundaries

Proposed deterministic mock provider with all 12 distinct gate/decision pairs and synthetic SID fixtures; mock transaction store only. Tests must show rejection before W1/PREPARE and no protected I/O.

**Decision required:** exact test-only wrapper distinguishing lab output from production without extending S1 wire, injection boundary between original S1 parser/engine and mock policy, and handling unknown-after-restart with no invented receipt.

### L-04 — Windows test plan and evidence

Proposed Windows tests of SCM lifecycle, wrong SID/anonymous/remote denial, pipe squatting, RevertToSelf failure, access masks, malformed/oversize input, gate grants, service restart and cancel with synthetic fixtures. Record exact OS/build/NTFS, script/tool versions and redacted evidence.

**Decision required:** minimum host/VM profile, deterministic tests/thresholds and evidence storage. A lab skeleton can be labelled `LAB_SERVICE_TESTED` only; it is **not** qualified protected W0–W9 storage or power-loss durability.

## 4. Decisions that remain out of scope

- Q1 backup/capacity numbers, native primary replacement/flush recipe, real DPAPI provisioning, key disaster recovery, operational backup and restore, production protected path/NativeRootBinding are not approved.
- No code or schema modifications to E00/A/O/D/S1, S2.1–S2.4 or golden vectors. `PUBLISH_REVISION` remains DISABLED; partial COMMIT reconstruction OFF.
- Creative Story Intelligence / WanGP concepts cannot grant or bypass editorial privileges. No PR, merge, release or modification to main.

## 5. Proposed next step — S3.1a, documentation only

Codex should draft the complete **S3.1a Lab Execution Contract**, including alternatives for L-01–L-04, exact laboratory identity, SDDL/access masks, bounded IPC contract, test synthetic provider, explicit failure cases and acceptance matrix, with primary Windows references. Stop after commit, request owner approval. **Do not start S3.2** until the exact lab contract is approved separately.
