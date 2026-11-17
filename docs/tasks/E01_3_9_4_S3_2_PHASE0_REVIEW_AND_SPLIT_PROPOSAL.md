# E01.3.9.4 / S3.2 — Phase 0 independent review and safe development split

**Date:** 2026-11-06. **Status:** Phase 0 report accepted as an accurate STOP; proposed phase split **NOT YET OWNER-APPROVED**. No S3.2 executable work is authorized by this document.

**Repository:** `olegale-ctrl/Story-Studio-RU-UA-WORK`
**Reviewed commit:** `88cb9e8823803c2f78c982af28f991ce012dc5cf`
**Exact reviewed base:** `0fa6b61aebc7689f787e2dd276607a2f0084b7ac`
**Branch:** `feat/editorial-e01-3-9-4-s3-2-windows-lab-broker`

## 1. GitHub and evidence review

- GitHub compare: one commit ahead, none behind the exact base, **two added docs only**: `docs/tasks/E01_3_9_4_S3_2_PREFLIGHT.md` (131 content lines) and `docs/tasks/E01_3_9_4_S3_2_RESULT.md` (113 content lines). No executable code, tests or golden vectors changed.
- Branch remote SHA matched `88cb9e8823803c2f78c982af28f991ce012dc5cf`; `main` observed unchanged at `e1f4efb0fb5ff290bb198349213c004b4667ef0f`; no matching PR.
- Codex reported Python 3.12.14, 169 pure storage tests PASS and 808 full discovery PASS, plus 1659 existing parameterized scenarios printed by S2.3. Independent reviewer has **not rerun** the tests; private log SHA hashes are documented in the result but logs not inspected.
- No actual Win11 VM/SCM account, admin install authorization, HostProfile build/UBR, pinned Win Python runtime or Windows observer supplied. LT01–LT15, RISK-01–04 remain BLOCKED. `LAB_SERVICE_TESTED`, `PROCESS_QUALIFIED`, `POWER_LOSS_QUALIFIED`: not obtained.
- Report accurately followed the then-binding Phase 0 instruction; `BLOCKED_PRE_IMPLEMENTATION` is a requirements/input gate, **not a failed test or source-code defect**.

## 2. Observation: avoid unnecessary full-development lock

The prior S3.2 instruction required a named, authorized, isolated Windows VM **before writing any executable code**, although pure LAB/1 framing, bounded decoding, synthetic fixture factory, authorization and in-memory replay can be designed/tested on a Linux/Python environment without Windows identities or protected disk.

It is reasonable to split **development permission** from **native installation and qualification permission**. This changes the previous phase gate and therefore requires an explicit owner decision. It is not a reinterpretation of the already-approved S3.1a schema.

The S3.1a `HostProfile` includes artifact SHA-256 for adapter/test/observer. Those values are unknowable before a build. Suggested sequencing:
1. For portable-only development, approve the exact immutable upstream source/contract and the explicit pure file allowlist. No Windows VM or installation.
2. On future Windows VM, obtain specific admin permission, verified OS/build/UBR/hypervisor resources and pinned runtime source/version.
3. Build native adapter/test/observer; pin their byte-exact artifacts and hashes **before running any SCM/native test**, produce complete HostProfile, then require a separate owner approval of that exact profile/hash and authorized installation.
4. Any artifact/runtime/OS change invalidates the native approval; native tests only on re-pinned profile. Never invent hashes or claim unrun qualification.

The full canonical S3.1a HostProfile remains required before native testing, not before isolated portable code.

## 3. Proposed stages, not currently authorized

### S3.2a — portable RAM-only LAB/1 core, no Windows install

**Candidate source:** exact head `88cb9e8823803c2f78c982af28f991ce012dc5cf` (or subsequent expressly approved docs-only review branch), feature branch exclusively.

**Strict candidate new-file allowlist:**
- `editorial/windows_lab/__init__.py`
- `editorial/windows_lab/protocol.py`
- `editorial/windows_lab/fixtures.py`
- `editorial/windows_lab/dispatcher.py`
- `tests/test_windows_lab_protocol_v1.py`
- `tests/test_windows_lab_dispatcher_v1.py`
- `docs/tasks/E01_3_9_4_S3_2A_RESULT.md`

No edits to existing files. No `service.py`, `client.py`, `win32_native.py`, PowerShell installers or adapter-specific production roots. A portable standalone preflight schema for synthetic metadata only; **do not** use actual account SIDs, Windows account provisioning, real S1 protected data or real keys.

Design and acceptance targets:
- `SSLB` envelope and canonical LAB JSON, strict typed schemas, 3 literal byte examples, max-request/outer-envelope size/depth limits and complete rejection before admission.
- Shared unchanged S1 decoder and S2 TransactionModel/VirtualStore; deterministic `S32_FIXTURES_1` whitelist of synthetic fixtures and exact 12 gate×decision grants, no caller-controlled authority.
- Mock dispatcher: bounded queue and explicit state machine where possible in pure tests, incarnation/request ID binding, same ID/bytes/principal replay without duplicate W1, old incarnation unknown/denied, safe errors and non-production result wrapper.
- Enforce production separation: no raw S1 receipt/MAC/key/journal/anchor or protected writes, no credential/key provisioning/network/GPU/subprocess, no hidden fallback.
- Pure tests: framing, malformed/oversize/unknown fields, 144 gate cells (12 allow/132 deny), B no grants, PUBLISH_REVISION refused, 32 RAM admissions/33rd capacity, replay and conflict, lost ACK/restart simulation and negative fault cases.
- Test originally approved storage suites + full discovery; no alteration of existing S1/S2/golden or source code.
- Prefix every LAB pure result/test with qualification `PURE_ONLY`; actual LT01–LT15 are **not fully PASS**, even if pure portions tested. RISK-01–03 remain BLOCKED, RISK-02 native component blocked, RISK-04 only pure subset.
- If the S3.1a contract proves inconsistent in pure implementation, STOP/report exact issue and request separate versioned contract revision; do not silently enlarge access rights, alter S1 or add transport endpoints.

### S3.2b — native Windows lab adapter and qualification

**Requires separately identified/approved supported Windows 11 Pro x64 VM, admin installation permission, pinned full HostProfile and source/runtime/adapter/test/observer hashes before native run**. Code only after scope approval; no full service installation on developer workstation by default.

- Implement limited Win32 SCM/named pipes/server identity/impersonation/ACL/service lifetime and bounded cancellation according to the S3.1a L-01/L-02 choices. No production protected writes or real DPAPI/keys.
- Run LT01–LT15 with Windows native/pure evidence separated, including RISK-01–04, RISK-02 max 1,052,672 byte EXECUTE in one WriteFile against 4096 pipe buffers and timeout; fail if behavior differs.
- Independent attempted-write observer, capture results with redacted private EvidenceIndex; no sensitive logs in Git. No independent proof of complete coverage means BLOCKED.
- `LAB_SERVICE_TESTED` label only after all cases PASS and independent review. No `PROCESS_QUALIFIED` or `POWER_LOSS_QUALIFIED` from a lab test.

## 4. Approval requested

A. Approve the **phase split and sequencing clarification** as described above: pure S3.2a work can begin without a Windows VM; actual native SCM install/qualification still requires a separately approved VM and exact HostProfile built after adapter/test/observer artifacts exist.

B. Approve a separate, explicitly scoped **S3.2a portable-only Codex assignment** based on the above allowlist. S3.2b and S3.3 remain STOP until their own gates close.

This is **not** an approval of new L-01–L-04 values, Q1, production deployment, privilege escalation, protected storage or unrelated WanGP/LTX additions.

**STOP:** no runtime/code changes have been made for this split proposal. No PR, merge, release or `main` changes.
