# E01.3.9.4 / S3.2 — Owner-approved LAB choices L-01–L-04

**Decision date:** 2026-11-06
**Decision status:** **APPROVED FOR LABORATORY S3.2 SCOPE ONLY**. Approval of design choices is **not** qualification of Windows behavior, installation permission on an unspecified machine, production deployment approval, or permission to write protected editorial data.

**Owner instruction:** "Утверждаю L-01–L-04 в рекомендованной редакции S3.1a, с обязательными проверками RISK-01–RISK-04. Подготовь задание Codex для S3.2 в строго лабораторном объёме."

**Exact approved source revision:** `cf70b8c0a93841f2bff272b584a2106374e3016f`
**Normative lab contract:** `docs/tasks/E01_3_9_4_S3_1A_LAB_EXECUTION_CONTRACT.md` at that SHA.
**Independent review:** `docs/tasks/E01_3_9_4_S3_1A_INDEPENDENT_REVIEW.md` at `818551171d1e955cf1dca6ddaf8cc54994c7528c`.

## Approved bounded choices

| ID | Owner-approved laboratory choice | Not thereby approved |
|---|---|---|
| **L-01** | Isolated `StoryStudioBrokerLab` own-process SCM service, dedicated local `SSLabBrokerSvc`, `NT SERVICE\StoryStudioBrokerLab` RESTRICTED service SID, `SeChangeNotifyPrivilege` only, named client A/B/Denied and `SSLabClients` lab group, pinned private runtime, no auto restart, explicit allowlisted cleanup | Real installation without separate machine/admin authorization, privilege broadening, production service identity |
| **L-02** | Exact `LAB_ACL_1` SDDL/masks; `\\.\pipe\StoryStudioBrokerLab.v1`; `SSLB`/LAB/1 closed schema; server message-read/client byte-read; one message/request/response/ACK; `LAB_LIMITS_1` (4 workers, 1 dispatcher, queue 2, 32 RAM admissions/incarnation, specified byte/time limits) | Widened DACL, GENERIC_WRITE, SeImpersonate, relaxed deadlines, unreviewed IPC variants |
| **L-03** | `S32_FIXTURES_1`, 17 closed policy cases and closed FaultCase set, authenticated real lab SID → synthetic A/B principal mapping, 12 independent gate/decision grants, 144-cell matrix, RAM-only model/replay, incarnation-scoped IDs, LAB_ONLY summary wrapper without raw S1 Receipt/MAC/key | Real review approval, production protected writer, persistence, real DPAPI, new S1 wire |
| **L-04** | **Initial target** isolated, maintained Windows 11 Pro x64 VM, CPU-only, 4 vCPU, 8 GiB RAM, 64 GiB local NTFS, no shared host folders or production data; LT01–LT15, redacted private EvidenceIndex; all-PASS qualification only for lab service behavior | Windows 10 qualification, real W0–W9 native durability, power-loss certification, Q1, production Windows deployment profile |

All parameter details, exact ACL/limits, alternative consequences and test matrix are incorporated **by exact SHA reference** to S3.1a; this document is not a partial replacement contract. If the actual Windows behavior contradicts a selected parameter, the required response is **STOP + evidence + separately reviewed contract revision**, not silent fallback or escalation.

## Mandatory independent-review gates

- **RISK-01:** Native restricted service SID, dedicated account, minimal privilege set, impersonation and token/query/access checks on the selected Windows host; fail closed, never grant `SeImpersonatePrivilege` or switch to UNRESTRICTED automatically.
- **RISK-02:** Native large single-message `WriteFile` (including max 1,052,672-byte EXECUTE), 4096-byte pipe buffers, bounded synchronous workers, 5-second deadlines, cancellation/slow-reader races. Failure requires STOP/revision, not automatic increased limits.
- **RISK-03:** Native process/token QUERY rights, identity proof, exact ACL/DACL; verify no unintended privilege exposure. No production broker rights inferred.
- **RISK-04:** Request bytes/principal/session/identity binding for EXECUTE/LOOKUP, exact replay and unknown-after-restart, no digest-only authorization, no fabricated terminal receipt.

## Outstanding pre-execution parameters and authorization

The owner has approved the **recommended lab profile**, **not supplied the exact test VM/host**. The S3.1a contract requires actual `HostProfile` including edition/build/UBR, hypervisor, runtime and artifact hashes, plus approval of that exact profile before **native S3.2 coding/run**. No such host-specific values are recorded here and **must not be invented**.

Before any SCM installation, account creation, service start or native host changes, obtain explicit approval for the **identified isolated test machine**, required administrator access and reversible installation procedure. The Codex task may be prepared now, but execution remains conditional on these host and install gates. If unavailable, perform only non-invasive inventory/design/preflight and report BLOCKED; do not silently run on the developer's ordinary Windows machine.

## Unchanged boundaries

- Existing S1, D1–D12, E00/A/O, S2.1–S2.4 and golden vectors immutable; `PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF.
- No protected NTFS writer, authoritative primary, journal, anchor, real registration, DPAPI key, backup/restore, actual migration or recovery, production endpoint, media, models, network sockets or subprocess from broker runtime.
- Q1 numeric policies, production W11-N/W10-S/VM-F profiles, and `PROCESS_QUALIFIED`/`POWER_LOSS_QUALIFIED` remain unapproved/unearned.
- No PR, merge, release or `main` change.

**Next:** separate scoped S3.2 Codex task. Review/STOP before any S3.3 or native protected storage.
