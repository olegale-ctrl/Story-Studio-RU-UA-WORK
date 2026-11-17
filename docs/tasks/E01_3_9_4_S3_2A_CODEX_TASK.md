# Codex task — E01.3.9.4 / S3.2a: portable Python LAB Core (NO Windows VM)

**Status:** owner-authorized **S3.2a only**; no S3.2b, protected writer or production deployment.

**Repository:** `olegale-ctrl/Story-Studio-RU-UA-WORK`
**Source branch:** `docs/editorial-e01-3-9-4-s3-2a-approved-task`
**Source SHA:** pin the exact published commit containing this task in the handoff; do not start from `main` or a floating ref.
**New feature branch:** `feat/editorial-e01-3-9-4-s3-2a-portable-lab-core`

## 0. Read and pin before coding

Read these complete sources at the exact revisions:

1. `docs/tasks/E01_3_9_4_S3_2A_OWNER_DECISION.md` — latest owner authorization; this is the narrow exception to the earlier no-code-without-VM gate.
2. `docs/tasks/E01_3_9_4_S3_2_PHASE0_REVIEW_AND_SPLIT_PROPOSAL.md` at `a288d9a9ea3711931669595f9b3b6c33f52a7e18`.
3. `docs/tasks/E01_3_9_4_S3_1A_LAB_EXECUTION_CONTRACT.md` at `cf70b8c0a93841f2bff272b584a2106374e3016f`: §§3.1–3.5, 5 (pure limits), 6.1–6.3, 7.2–7.3; L-01–L-04 previously owner-approved.
4. `docs/tasks/E01_3_9_4_S3_1A_INDEPENDENT_REVIEW.md` at `818551171d1e955cf1dca6ddaf8cc54994c7528c` — RISK-01–04; distinguish pure checks from native checks.
5. `docs/tasks/E01_3_9_4_S3_2_PREFLIGHT.md`, `docs/tasks/E01_3_9_4_S3_2_RESULT.md` at `88cb9e8823803c2f78c982af28f991ce012dc5cf` — historical blocked result, not the current S3.2a code gate.
6. Existing approved S1 and S2 sources/tests/golden: `editorial/storage_protocol_v1.py`, `editorial/storage_transaction_model_v1.py`, `editorial/storage_recovery_adversarial_v1.py` (if present), `tests/test_storage_protocol_v1.py`, `tests/test_storage_transaction_model_v1.py`, `tests/test_storage_recovery_adversarial_v1.py`, D-01 regressions and approved S1b/D1–D12. Reuse public existing APIs; **do not edit them**.

Record exact source/contract SHA and Python runtime version in the result. No real Windows HostProfile is required or to be invented in this stage.

## 1. Exact new-file allowlist — no other modifications

Create only:

```text
editorial/windows_lab/__init__.py
editorial/windows_lab/protocol.py
editorial/windows_lab/fixtures.py
editorial/windows_lab/dispatcher.py
tests/test_windows_lab_protocol_v1.py
tests/test_windows_lab_dispatcher_v1.py
docs/tasks/E01_3_9_4_S3_2A_RESULT.md
```

No modifications to any existing files, `main`, CI, dependencies, golden vectors or S1/S2 models. No `service.py`, `client.py`, `win32_native.py`, `manifest.py`, installers, PowerShell, executable packaging, native observer, network endpoints, OS impersonation, actual SID/SDDL, pipe handles, DPAPI or protected files. Use Python 3.12 stdlib only; no GPU or paid/cloud API. The LAB module must be importable and its tests runnable on Linux.

If a necessary change is outside the allowlist, or the normative contract conflicts with an existing S1/S2 invariant, **STOP** and report the exact reproducer; do not silently expand scope.

## 2. Protocol: pure LAB/1 codec and exact bytes

Implement only an in-memory `encode_lab`/`decode_lab`-style API (names may differ if documented), with explicit type/length checks:

- Frame = ASCII `SSLB` + 4-byte unsigned big-endian JSON length + exact canonical UTF-8 JSON; no trailer or extra frames.
- Strict closed `LabHello`, `LabExecute`, `LabLookup`, `LabAck`, `LabHelloResult`, `LabResult`, `MockSummary`, `LabError` shapes from S3.1a §§3.2–3.3. Required fields only, no unknown/missing fields or implicit type coercion. UUID, SHA-256 hex, enum values, scope and `lab_version` exact.
- Strict JSON: no duplicate keys, floats/NaN/Infinity, BOM, invalid UTF-8, surrogates, noncanonical key order/spacing or trailing bytes; outer depth ≤65, nested S1 Request separately validated by **unchanged** S1 decoder/validator and depth ≤64.
- Reject N=0 and N>1,052,672 **before** body allocation. For HELLO/LOOKUP/ACK/response enforce JSON ≤4096 bytes; EXECUTE JSON ≤1,052,672, canonical nested S1 Request ≤1,048,576 bytes. Use explicit byte-length accounting, not character count.
- Validate complete frame as a pure byte buffer; **do not** claim to enforce Win32 OS message boundaries, one-WriteFile behavior, pipe ACK/EOF, client authentication or native timeout. Those are S3.2b.
- ACK hash = SHA256(exact response JSON bytes), not header+body, S1 digest or MAC. It is transport acknowledgement only.
- Test the three literal byte oracles from S3.1a §3.5 as independently hardcoded expected JSON bytes, header bytes, length and SHA-256: HELLO 159 / `53534c420000009f` / `b6b3da12fd7423f404ccf700476499c4af9e3a9ba84a6716a02e0ce8b78cdccf`; HELLO_RESULT 357 / `53534c4200000165` / `812089bdaef8791dd8127ca21bd771e65c48d5c78a41577c125af38f7604f119`; ACK 195 / `53534c42000000c3` / `ad5152df65e4b22d874736635590a422c780024046598df3fa22deacd7b716d2`.
- LAB result wrapper must be rejected as an S1 Receipt by the existing S1 parser. Never modify original S1 golden vectors.

## 3. Synthetic fixture factory: S32_FIXTURES_1

Implement a **closed, deterministic, pure** fixture factory in `fixtures.py`, using existing S1/S2 test APIs and valid synthetic RAM-only data:

- Exactly 17 `PolicyCase` values: five CG cases (`CG_INIT`, `CG_MIGRATE`, `CG_RECOVERY`, `CG_WRITER_ONLY`, `CG_NONE`) and 12 GD cases (SCRIPT/SCENES/HANDOFF × approve/reject/revise/revoke).
- Recognize **all 17 probes under every policy case**: INIT_EMPTY, IMPORT, TRANSFER, MIGRATE, RECOVERY and 12 GD names. Unauthorized cross-policy probes must fail as `LAB_POLICY_DENIED` after whitelist recognition, **not** `LAB_FIXTURE_NOT_ALLOWED`.
- `FaultCase` exactly as S3.1a §6.1; do not expose fault selection through request JSON, environment, CLI, IPC or dynamic plugin name. A test/harness injects a fixed closed case before constructing the in-memory dispatcher.
- Synthetic principal A = `windows-sid:S-1-5-21-1000-1000-1000-1001`; B = `windows-sid:S-1-5-21-1000-1000-1000-1002`. These are **mock values**, not real Windows SID identity proof. No request field can self-assign principal.
- Exact `CommandGrant` + `GateDecisionGrant` matrix from S3.1a §6.2. Require `PROTECTED_SNAPSHOT_WRITE` AND operation grant AND matching gate/decision grant where applicable. B has no command or gate grants. `PUBLISH_REVISION` is disabled unconditionally.
- For generated UUID-valued request/session/approval/event/epoch IDs use UUIDv5 namespace = provided synthetic current incarnation, names exactly `S32_FIXTURES_1/<policy_case>/<actor A|B>/<probe>/<slot 0..63>/<role>` with `seed` for stable production/machine/epoch/policy roles. Validate finite role/probe/slot vocabulary; non-GD slots only 0, GD slots 0..63. No arbitrary caller-supplied fixture files/paths/blobs/approvals.
- Keep image ≤128 KiB, startup bundle ≤16 MiB, candidate blob bytes ≤256 KiB; construct bounded candidates on demand, not 64×17 histories. No real editorial records, user secrets, real approvals, production keys or filesystem writes.
- If needed to run unchanged S1 model, use only explicitly pinned, **test-only synthetic 32-byte keys in RAM**. Synthetic verification/human-review assertions are fixture inputs, never a real reviewer decision or native SID authority.

## 4. Pure dispatcher: authorization, replay and RAM state

Implement a small, injectable, deterministic **non-network** dispatcher in `dispatcher.py`. It receives an immutable **trusted synthetic caller context from the test harness** (not from LAB JSON). The future Windows adapter alone will provide authenticated A/B mapping; this stage does not authenticate Windows users.

- Validate lab run/incarnation and strict envelope/S1 shape before any model call. Wrong run: `LAB_RUN_MISMATCH`. Old incarnation: `UNKNOWN_AFTER_RESTART` (with unknown admission), without model execution. Rewrapping old request under a new incarnation: fixture whitelist denial, never fresh admission.
- Reuse unchanged `TransactionModel` and `VirtualStore` for accepted operations; do not invent a second permissive engine. Factory must produce a valid `TransactionInput`, `FixtureAuthority`, frozen command and synthetic seeded store for the selected case/probe.
- Existing request ID: first check authenticated synthetic principal/read scope and **full canonical S1 bytes** including session; same ID + principal + exact bytes returns **byte-identical** cached LabResult with no new S2 event/W1; different bytes/principal/session -> conflict/deny before model call. LOOKUP uses stored bytes and principal; digest alone never grants access.
- New request ID: recognize approved fixture candidate; evaluate current policy/grants and frozen review/package/session assertions; only then call unchanged model. Any pre-admission rejection produces zero model W1/PREPARE/events/IDs and does not consume the 32-admission quota.
- Exactly 32 RAM-admitted IDs per incarnation, no eviction; 33rd **new** valid ID returns `LAB_CAPACITY`, while known replay and lookup continue. Do not cache unbounded denied requests. One synthetic dispatcher/model writer; any queue/busy/time limit simulated with explicit deterministic hooks, **not** presented as a native 4-worker/4096-buffer/5-second Windows test.
- Mock outcome only `MOCK_FINALIZED`, `MOCK_ABORTED`, `MOCK_PENDING`, `DENIED`, `NOT_ADMITTED`, `UNKNOWN_AFTER_RESTART`. Terminal results require verified terminal RAM receipt/anchor; no fabricated success, ABORT or recovery. Explicit PREPARE/INTENT injected `SimulatedCrash` produces `MOCK_PENDING` and frozen RAM prefix, no S2 recovery call. Crash after RAM final + new incarnation yields unknown, not invented prior final.
- For terminal summary compute `SHA256(b"story-studio-s3-2-lab-result-v1" + b"\\x00" + exact_canonical_internal_receipt_bytes)`; do **not** export receipt, MAC, key ID, anchor, journal, head, raw approval evidence or production file paths. LabResult is a closed `lab_only:true` wrapper; `mock_admission` = NONE/RAM/UNKNOWN and errors use only closed LAB labels.
- No file/network/registry/subprocess/GPU operations in runtime; no S1/S2 edits. Keep all synthetic model state in RAM. No raw error string, traceback, secret or arbitrary exception message in LabError.
- Pure crash/response-loss tests may simulate unknown delivery and cache retention, but cannot claim Windows native cancellation, token restoration or real durability.

## 5. Test-first acceptance — actual executable tests, not only documentation

Create tests only in the two allowed new `tests/` files. At minimum cover:

1. Golden byte oracles 3/3; strict positive/negative framing and schemas; over-limit before allocation, depth, duplicate keys, unknown fields, unicode/NaN/floats/booleans-as-integers, malformed lengths, nested S1 rejection, LAB-vs-S1 receipt separation.
2. All **144** GD policy-case × gate/decision cells (12 allow, 132 `LAB_POLICY_DENIED`), using real fixture whitelist recognition for all probes. Explicitly assert no virtual W1/event/admission on the 132 denied cells.
3. Five CG policy cases × six S1 operation classes; B denied in every case; missing writer grant/operation grant, PUBLISH_REVISION always denied, unauthorized caller-supplied principal/policy/fault/fixture selector rejected.
4. UUIDv5 derivation and slot bounds, old incarnation/new incarnation behavior, full-byte/principal/session conflicts, wrong run, lookup digest-only attempts, byte-identical replay, lost ACK/response-loss simulations, no double model call.
5. 32 admissions and 33rd capacity denial, replay/lookup still available, no denial-cache growth or eviction.
6. Explicit fault cases: PREPARE/INTENT `MOCK_PENDING`, synthetic crash after final and restart `UNKNOWN_AFTER_RESTART`, pre-admission denial with zero events, injected dispatcher stalls reported as **pure simulation only**.
7. Existing storage regressions/golden unchanged, including D-01. Do not treat `unittest` success as native LT qualification.

Suggested commands (adjust only for actual existing test module names, report exact executed commands):

```bash
python -m unittest tests.test_windows_lab_protocol_v1 -v
python -m unittest tests.test_windows_lab_dispatcher_v1 -v
python -m unittest tests.test_storage_protocol_v1 tests.test_storage_transaction_model_v1 tests.test_storage_recovery_adversarial_v1 -v
python -m unittest discover -s tests -v
git diff --check
git status --short
git rev-parse HEAD
```

Use the project's `.venv` when present. No Windows-specific test is required or authorized for S3.2a. If the full suite cannot run, report exact missing dependency/error, not PASS.

## 6. Result, labels and STOP

Create `docs/tasks/E01_3_9_4_S3_2A_RESULT.md` with:
- Exact source SHA, final branch/commit SHA (report final SHA in handoff if self-reference would be circular), changed-file list and blob hashes, Python/OS/runtime, commands, test counts and exit status.
- Fixture policy/probe coverage, 144-cell results, grant and idempotency/capacity/fault cases, three independent byte oracles, unchanged S1/S2/D-01 tests.
- Pure-only evidence: `PURE_ONLY` / `S3_2A_PORTABLE_TESTED` only if actually tested; distinguish failed, skipped and blocked. **LT01–LT15 not declared fully PASS**. RISK-01/03 BLOCKED, RISK-02 native BLOCKED, RISK-04 pure subset only. `LAB_SERVICE_TESTED`, `PROCESS_QUALIFIED`, `POWER_LOSS_QUALIFIED` not earned.
- Explicit no-OS-authentication/no-ACL/no-native-IO/no-protected-writer statement, known limitations, any stop conditions and earliest reproducible failure.
- No real SIDs/passwords/keys/private Windows manifests/ETW logs or heavy binaries committed.

Commit and publish **only** `feat/editorial-e01-3-9-4-s3-2a-portable-lab-core`, clean working tree and exact remote SHA. No PR, merge, release or `main` change. **STOP for independent review; do not start S3.2b or S3.3.**
