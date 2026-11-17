# E01.3.9.4 / S3.1a — Independent Review of Windows Lab Execution Contract

**Date:** 2026-11-06. **Review status:** ACCEPTED AS DESIGN DELIVERABLE; **L-01–L-04 NOT YET OWNER-APPROVED; S3.2 NOT AUTHORIZED.** No service implementation, Windows qualification, production storage or key-management activity was performed during this review.

**Repository:** `olegale-ctrl/Story-Studio-RU-UA-WORK`

**Reviewed branch:** `docs/editorial-e01-3-9-4-s3-1a-lab-execution-contract`

**Reviewed exact SHA:** `cf70b8c0a93841f2bff272b584a2106374e3016f`

**Exact base:** `c3f65c5253c5e02be17fcf8676f280e6e83d9e63`

## 1. Scope verified through GitHub

Comparison: 1 commit ahead, 0 behind. Exactly two new files:

- `docs/tasks/E01_3_9_4_S3_1A_LAB_EXECUTION_CONTRACT.md` — 793 content lines; blob `dfa37ceb8fa38fde9b3bec50995a0e9eaea24a8a`.
- `docs/tasks/E01_3_9_4_S3_1A_RESULT.md` — 72 content lines; blob `d18984d3531dc821b1ec7de80acc39005b94ff34`.

No changes to E00/A/O/D/S1, S2.1–S2.4 tests/golden, prior S3.1, or implementation. The S3.1a branch HEAD matched the reviewed commit. `main` remained `e1f4efb0fb5ff290bb198349213c004b4667ef0f`; no matching PR found. Documentation files have no trailing whitespace; fenced blocks are balanced. Claimed repository-local `git diff --check` was reported by Codex, not independently executed by this reviewer.

## 2. Independent verification of byte examples

An independent Python computation over the exact literal JSON examples confirmed:

| Message | JSON bytes | Eight-byte SSLB header (hex) | SHA-256 JSON |
|---|---:|---|---|
| HELLO | 159 | `53534c420000009f` | `b6b3da12fd7423f404ccf700476499c4af9e3a9ba84a6716a02e0ce8b78cdccf` |
| HELLO_RESULT | 357 | `53534c4200000165` | `812089bdaef8791dd8127ca21bd771e65c48d5c78a41577c125af38f7604f119` |
| ACK | 195 | `53534c42000000c3` | `ad5152df65e4b22d874736635590a422c780024046598df3fa22deacd7b716d2` |

This is **only a pure byte computation**, not execution of native Windows pipe protocol or Windows cryptography. Python/Node comparison from Codex was not independently witnessed.

## 3. Security/architecture assessment

The proposal retains the original S1 command envelope inside a distinguishable **LAB/1 / SSLB** transport, not a new S1 protocol version. Its `LabResult` exposes no raw Receipt/MAC/key/protected history. Scoped SID-to-synthetic principal mapping is distinct from Windows installation/account authority. `PUBLISH_REVISION` stays disabled; partial COMMIT reconstruction stays off. Mock W0–W9 is RAM-only; unknown outcome after process restart is not falsely recovered.

The proposed client pipe mask `0x00120083` allows required read/write-data, READ_CONTROL, FILE_READ_ATTRIBUTES and SYNCHRONIZE while omitting bit `0x4` (FILE_APPEND_DATA / FILE_CREATE_PIPE_INSTANCE). The client deliberately remains in byte-read mode, while the server uses message-type/read-mode. Microsoft describes both the difference between read modes and the FILE_CREATE_PIPE_INSTANCE access hazard.

References:
- [Named Pipe Security and Access Rights](https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-security-and-access-rights).
- [Named Pipe Type, Read, and Wait Modes](https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-type-read-and-wait-modes).
- [CreateNamedPipeW documentation](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-createnamedpipew).
- [SERVICE_SID_INFO / restricted SID](https://learn.microsoft.com/en-us/openspecs/windows_protocols/ms-scmr/ea1a9acd-4bb2-473f-ae5b-55969c5960fc).

No blocking logical contradiction found by static review. **Design rationale alone cannot establish executable correctness of the selected Windows identity/security configuration.**

## 4. Mandatory first-run uncertainty gates

**RISK-01 — Identity/impersonation.** The combination `SERVICE_SID_TYPE_RESTRICTED`, separate dedicated `SSLabBrokerSvc`, only `SeChangeNotifyPrivilege`, and strict `SecurityIdentification` on every message must be tested with real Windows SIDs and tokens. It is not established merely by structurally correct SDDL. Verify installer can set the process/token descriptors and ordinary users can perform the specified identity checks. If observed permissions fail, STOP and revise the approved contract; no automatic elevation or privilege loosening.

**RISK-02 — Synchronous pipe capacity/deadlines.** The contract requires a single `WriteFile` per message, `EXECUTE` up to 1,052,672 JSON bytes, 4096-byte declared pipe buffers, four bounded synchronous workers, 5-second read/write/ACK windows, and cancellation. Windows documentation notes that a write may block when pipe quota is exhausted. LT07/LT08 must include at-limit messages, slow readers, timeouts and CancelSynchronousIo completion races, not only the short HELLO/ACK golden bytes. Any failure is a qualification failure; no hidden increase in buffer, rights, or timeout.

**RISK-03 — Token query exposure.** The proposed process/token DACL grants `SSLabClients` tightly scoped QUERY rights for authenticating the lab server. Confirm real Windows access-check behavior and that neither error handling nor installation broadens these rights. This is a lab-only trust decision, not authorization to apply it to the production broker.

**RISK-04 — Exact request identity.** `EXECUTE` binds full S1 request bytes, while `LOOKUP` carries a digest and ID only; ensure lookup uses stored canonical bytes and authenticated principal, and never treats a client-supplied digest alone as an authorization proof. Preserve the distinction between pre-admission denials and requests admitted to RAM before lost ACK.

## 5. Proposed owner decisions — not approvals

| Decision | Recommended bounded choice | Condition before S3.2 |
|---|---|---|
| L-01 | Isolated `StoryStudioBrokerLab`, dedicated local service account + restricted service SID; no production roots/keys, no auto restart | Approve exact account/identity/installation protocol; fail closed on missing privileges |
| L-02 | `LAB_ACL_1`, specific masks, message-type server + byte-read client, SSLB envelope and `LAB_LIMITS_1` | Approve exact SDDL/worker/timeouts and required RISK-01/02 native test-first gates |
| L-03 | `S32_FIXTURES_1`, synthetic A/B grant mapping, all 12 gate×decision pairs, RAM-only idempotency, non-production result wrapper | Approve scope, forbid raw S1 receipt or real protected writer |
| L-04 | Isolated maintained Windows 11 Pro x64 VM, CPU-only 4 vCPU / 8 GiB RAM / 64 GiB local NTFS; LT01–LT15 | Pin actual Windows build/UBR, VM/hypervisor, source/runtime hashes before claiming any lab qualification |

S3.2 should be issued as a **test-first, mock-only** service skeleton assignment only upon explicit owner approval of the exact L-01–L-04 revision and availability of the identified lab host. Windows 10 support remains a separate eventual qualification; Q1 quotas and W11-N/W10-S/VM-F production profiles are unapproved.

## 6. Decision and STOP

**Accepted:** S3.1a documentation completeness, exact branch/file scope, visible byte examples and conceptually safe separation between lab mock behavior and protected editorial authority.

**Not accepted as evidence:** actual Windows SDDL/AccessCheck, SCM account permissions, token impersonation, pipe max-size/timeout behavior, W0–W9 native durability, or any production security claim.

No code, PR, merge, release or changes to `main`. STOP pending owner decision L-01–L-04. S3.2 must not begin from this review automatically.
