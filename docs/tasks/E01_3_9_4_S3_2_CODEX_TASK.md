# Codex task — E01.3.9.4 / S3.2 Windows LAB Broker (strictly non-production)

**Status:** OWNER-APPROVED LAB CHOICES; IMPLEMENTATION CONDITIONAL ON PRE-EXECUTION GATES.
**Repository:** `olegale-ctrl/Story-Studio-RU-UA-WORK`
**Source branch:** `docs/editorial-e01-3-9-4-s3-2-approved-lab-task`
**Source base:** the exact GitHub commit containing this task, to be pinned in the Codex handoff; do not use `main` or an older branch.
**Target implementation branch:** `feat/editorial-e01-3-9-4-s3-2-windows-lab-broker`.

## A. Authoritative references and non-negotiable scope

Read these complete files **at exact reviewed revisions** before work:

1. `docs/tasks/E01_3_9_4_S3_2_OWNER_LAB_DECISIONS.md` — owner approval L-01–L-04, explicit remaining host gate.
2. `docs/tasks/E01_3_9_4_S3_1A_LAB_EXECUTION_CONTRACT.md` at `cf70b8c0a93841f2bff272b584a2106374e3016f` — normative **LAB/1** wire, SDDL, limits, fixture factory and LT01–LT15.
3. `docs/tasks/E01_3_9_4_S3_1A_INDEPENDENT_REVIEW.md` at `818551171d1e955cf1dca6ddaf8cc54994c7528c` — RISK-01–RISK-04.
4. `docs/tasks/E01_3_9_4_S3_1_WINDOWS_STORAGE_SPEC.md` and approved D1–D12/S1 contracts, S2.1–S2.4 sources and golden vectors.

The output is an **isolated test-only SCM service**, client, bounded LAB/1 transport, OS token/ACL validation, injected synthetic authority and RAM-only S2 transaction model. It must **never** touch real protected primary/journal/anchor/registration/DPAPI/backup/keys, production reviewers or media. `PUBLISH_REVISION` stays DISABLED; partial COMMIT reconstruction OFF. CPU-only, offline; no external services, mandatory GPU, third-party Python packages or subprocesses in broker runtime.

## B. PHASE 0 — mandatory non-invasive preflight; STOP if any gate missing

**Do not create/edit executable code or install anything before this gate.** Verify exact source SHA/branch and that `main` is untouched. Inspect existing APIs `editorial/storage_protocol_v1.py`, `editorial/storage_transaction_model_v1.py`; never edit them.

Prepare `docs/tasks/E01_3_9_4_S3_2_PREFLIGHT.md` with:

1. Proposed actual isolated Win11 Pro x64 VM **HostProfile**: edition, full build and UBR, hypervisor, 4 vCPU / 8 GiB RAM / 64 GiB local NTFS or greater, offline, no shared folders, service-account provisioning method, administrator/install authority, supported OS/license, Python private runtime source/version, evidence isolation. Do **not** infer these from the developer workstation or invent values.
2. Precise planned `LAB_ACL_1` SDDL expansion/Windows SID binding test strategy; identify whether service account, restricted SID and `SeChangeNotifyPrivilege`-only mode can be tested.
3. Explicit plan for `HostProfile.adapter_artifact_sha256` and `test_artifact_sha256`: those hashes **cannot exist before their code/artifacts are built**. The S3.1a requirement to approve a *complete* HostProfile before coding and running is circular. Flag it; request owner-approved sequencing clarification (pre-code host/runtime/source identity, post-build pinned artifact hashes before native run). Do not insert fake hashes or silently reinterpret the approved contract.
4. Native execution/SCM install must be separately authorized for this **specific** lab VM. No auto-provisioning of accounts or admin service installation on an unspecified machine.
5. Planned test-first evidence for RISK-01–RISK-04, with positive and negative outcomes and no privilege escalation.

**If exact HostProfile, its sequencing clarification, or permission to modify the specific VM is missing: commit only this preflight document plus `docs/tasks/E01_3_9_4_S3_2_RESULT.md` marked `BLOCKED_PRE_IMPLEMENTATION`; publish branch and STOP. Do not implement or claim tests.** The task below is the ready-to-run implementation plan *after* the missing owner gates are explicitly approved.

## C. PHASE 1 — only after Phase 0 approval: test-first, isolated implementation

Create **new files only** under the following exact allowlist. No edits to any existing file:

- `editorial/windows_lab/__init__.py`
- `editorial/windows_lab/protocol.py`
- `editorial/windows_lab/manifest.py`
- `editorial/windows_lab/fixtures.py`
- `editorial/windows_lab/dispatcher.py`
- `editorial/windows_lab/win32_native.py`
- `editorial/windows_lab/service.py`
- `editorial/windows_lab/client.py`
- `scripts/windows_lab/install_lab.ps1`
- `scripts/windows_lab/uninstall_lab.ps1`
- `scripts/windows_lab/run_lab_matrix.ps1`
- `tests/test_windows_lab_protocol_v1.py`
- `tests/test_windows_lab_dispatcher_v1.py`
- `tests/test_windows_lab_native_v1.py`
- `docs/tasks/E01_3_9_4_S3_2_PREFLIGHT.md`
- `docs/tasks/E01_3_9_4_S3_2_RESULT.md`

If another file is essential, **STOP and request scope amendment**, do not edit unrelated files. Never change approved S1/S2 contracts, golden vectors, CI, requirements, packaging, default `main`, or project policy. Use stdlib (`ctypes` for Win32) and pinned private Python runtime; do not assume `pywin32` or system Python/PATH.

### C1. Pure LAB/1 codec and byte tests

- Exact `SSLB` magic, uint32 big-endian payload length, canonical UTF-8 JSON, closed typed LabHello/Execute/Lookup/Ack/Result schemas, no duplicate keys/unknown fields/floats/NaN/BOM/surrogates; enforce outer depth ≤65 and nested existing S1 depth ≤64 **without weakening S1 decoder**.
- S1 request bytes ≤1,048,576; LAB EXECUTE JSON ≤1,052,672; HELLO/LOOKUP/ACK and responses ≤4096; validate before allocation/admission.
- Test three literal HELLO/HELLO_RESULT/ACK byte oracles from S3.1a §3.5 using independently hardcoded expected headers, lengths and SHA-256. Never update S1 golden vectors.
- Server OS message boundaries: exactly one frame/message; client byte-read exact frame and EOF; ACK is transport receipt only. Deny pipelining, trailing bytes, fragmented OS messages, malformed and overlimit input. All negative tests verify no model W1/PREPARE.

### C2. Identity and Win32 SCM/named pipe boundary

- Lab service `StoryStudioBrokerLab`, separate account `SSLabBrokerSvc`, `SERVICE_SID_TYPE_RESTRICTED`, `SeChangeNotifyPrivilege` only, no automatic `SeImpersonatePrivilege` or UNRESTRICTED fallback.
- Exact approved `LAB_ACL_1` pipe/service/process/token/file descriptors and specific access masks; pipe `\\.\pipe\StoryStudioBrokerLab.v1`. Use `FILE_FLAG_FIRST_PIPE_INSTANCE`, reject remote clients, never permit `FILE_CREATE_PIPE_INSTANCE` to clients; client access `0x00120083`, byte-read, `SECURITY_IDENTIFICATION` and dynamic tracking.
- Client independently checks pipe DACL/owner, SCM service/PID, process creation identity/ImagePath, TokenUser=SA, enabled SV and restricted SV **on every connection before sending HELLO or request**; no PID/name-only trust.
- Server authenticates the actual impersonated SID for **every OS message including ACK**, maps only pinned A/B SIDs to synthetic mock principals; no trust in caller JSON principal. Verify `RevertToSelf` + no residual token. On failure fail-stop entire service; do not log/execute under impersonated token.
- Bounded synchronous I/O (4 workers/1 dispatcher/queue 2), no unlimited thread/handle pool, 32 RAM admissions, specified 2s/5s/10s/1s timeouts. `CancelSynchronousIo` races require observed completion before reuse or process fail-stop.
- Use exact restricted service/runtime installation constraints and **only** pinned isolated VM after explicit install permission. Installer must fail on preexisting account/service/path/pipe collision; cleanup must match manifest identity and allowlisted paths, never delete by name alone.

### C3. Injected authorization and RAM-only execution

- Use original S1 parser/validation and unchanged `TransactionModel` + `VirtualStore`; adapt with injected fixture authority, never implement a parallel permissive engine.
- `S32_FIXTURES_1` closed factory, all 17 policy cases × allowed FaultCase, UUIDv5 incarnation-based fixture IDs, exact 12 gate×decision pairs and independent command grants. Client cannot supply arbitrary blob, path, policy, approval or fixture selector. No general upload or review-session API.
- Require `PROTECTED_SNAPSHOT_WRITE` + operation grant + exact GateDecisionGrant where applicable; B no editorial rights. Wrong principal, session, bytes, grant or old incarnation denied **before** W1/PREPARE. Validate original D-01 parent epoch protection remains intact.
- 32 admissions/incarnation, no eviction; same-ID same principal/exact bytes returns byte-identical cached LabResult, no second model call; changed bytes/session/principal conflicts; LOOKUP never uses client digest as authorization by itself.
- After service restart, old incarnation outcome `UNKNOWN_AFTER_RESTART` or whitelist denial, **not** success/ABORT or recovery. `MOCK_PENDING` only for explicit RAM fixture faults; no fabricated protected receipt. Return LAB_ONLY summary digest only; never raw S1 Receipt/MAC, key, journal or protected evidence.
- Runtime must have zero regular-file write attempts, no DPAPI, registry persistence, network, subprocess, production file handles, or production keys. Elevated installer/harness file operations are separately bounded and must not be attributed to service hot path.

### C4. Required Windows qualification tests — LT01–LT15

Implement the **entire** S3.1a §7.2 matrix; do not silently shrink it. At minimum:

- LT01–LT02: 3 install/start/stop/cleanup cycles, 10 normal restarts, 10 crash/restarts; collision/identity/cleanup negative cases.
- LT03–LT06: exact access masks, A/B/Denied/Admin, pipe squatting, wrong server identity, anonymous/remote/SQOS, impersonation/token-query/revert/residual failures. Distinguish native observations from injected fault paths.
- LT07–LT08: framing/depth/oversize/malformed, slow readers, 4+1 clients, full 1,052,672-byte EXECUTE under 4096-byte pipe buffers, timeouts and 10 cancellation races at each ARM/IO/COMPLETE point. Failure triggers STOP/review; **no automatic buffer/time/privilege increase**.
- LT09: **144** gate×decision cells = 12 exact allow, 132 deny.
- LT10: B denied, all 5 command-grant cases ×6 operations, missing-grant negatives, PUBLISH_REVISION always denied.
- LT11–LT13: replay, lost ACK, conflict, unknown after restart, 32 admitted IDs then 33rd denied without eviction, pre-admission denial with zero W1/events/IDs.
- LT14: independent attempted-write audit (including denied attempts) over entire service runtime; zero forbidden writes and zero audit gaps, no child processes. Missing observer coverage = BLOCKED.
- LT15: original S2.1–S2.4 and D-01 regression/golden tests pass unchanged; LAB wrapper independently rejected by S1 Receipt decoder.

Use `EvidenceIndex` schema from §7.3. Record exact Windows build/UBR, source SHA, runtime and artifact SHA, case/repetition, PASS/FAIL/BLOCKED, NATIVE/INJECTED/PURE and redacted trace digests. Real SIDs/passwords/private manifests/ETW traces/dumps **must not** be committed. If native Windows environment unavailable, mark Windows cases `BLOCKED`, not `PASS` or `LAB_SERVICE_TESTED`.

## D. Required commands / review evidence

Run, on a supported Python environment:

```powershell
python -m unittest tests.test_windows_lab_protocol_v1 -v
python -m unittest tests.test_windows_lab_dispatcher_v1 -v
python -m unittest tests.test_storage_protocol_v1 -v
python -m unittest tests.test_storage_transaction_model_v1 -v
python -m unittest tests.test_storage_recovery_adversarial_v1 -v
python -m unittest discover -s tests -v
git diff --check
git status --short
git rev-parse HEAD
```

Native Windows `tests.test_windows_lab_native_v1` plus `run_lab_matrix.ps1` only on **explicitly authorized and pinned isolated VM**; report each LT01–LT15 result. A non-Windows skip is not a qualification PASS. For each failure provide the earliest deterministic reproducer, observed native error code and a minimal bounded fix proposal; no stealth contract revision.

## E. Result and STOP

Write `docs/tasks/E01_3_9_4_S3_2_RESULT.md` with: base/head SHA, exact changed files, implementation summary, HostProfile/approval gate, test counts and commands, 15-row LT matrix, RISK-01–04 results, full error details, evidence hashes, forbidden-write audit coverage, and explicit qualification labels. A complete code branch may be reviewed as **UNQUALIFIED** if native tests are unavailable; never label it `LAB_SERVICE_TESTED` without all native cases PASS and independent review.

Publish the **feature branch only**, with clean working tree and exact remote SHA. No PR, merge, release, production service, production keys, Q1 decisions, protected NTFS writer or `main` changes. **STOP before S3.3.**
