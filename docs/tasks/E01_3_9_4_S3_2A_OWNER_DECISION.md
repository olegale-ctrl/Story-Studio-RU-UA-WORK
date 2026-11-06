# E01.3.9.4 — Owner decision: S3.2a / S3.2b split and artifact-hash sequencing

**Date:** 2026-11-06
**Status:** **APPROVED** — only the portable Python S3.2a scope described below. S3.2b native Windows implementation, installation, qualification and S3.3 remain **NOT AUTHORIZED**.

**Exact owner instruction:** "Утверждаю разделение S3.2a / S3.2b и предложенный порядок фиксации хешей. Подготовь задание Codex для S3.2a, только portable Python LAB Core, без Windows VM и защищённого writer."

## 1. Decision provenance and precedence

- Independent Phase 0 report at `88cb9e8823803c2f78c982af28f991ce012dc5cf`: `docs/tasks/E01_3_9_4_S3_2_PREFLIGHT.md`, `docs/tasks/E01_3_9_4_S3_2_RESULT.md`. Its `BLOCKED_PRE_IMPLEMENTATION` status correctly described the **then-effective** requirement.
- Proposed split at `a288d9a9ea3711931669595f9b3b6c33f52a7e18`: `docs/tasks/E01_3_9_4_S3_2_PHASE0_REVIEW_AND_SPLIT_PROPOSAL.md`. **The owner now approves the split and sequencing in that proposal.**
- Existing owner-approved L-01–L-04: `docs/tasks/E01_3_9_4_S3_2_OWNER_LAB_DECISIONS.md` (revision `0fa6b61aebc7689f787e2dd276607a2f0084b7ac`).
- Normative lab specification: `docs/tasks/E01_3_9_4_S3_1A_LAB_EXECUTION_CONTRACT.md` at `cf70b8c0a93841f2bff272b584a2106374e3016f`. Historical PROPOSAL heading is superseded for L-01–L-04 by the subsequent explicit owner decision; its exact technical constraints remain binding unless specifically amended.

**Limited amendment to S3.1a §7.1 and the previous S3.2 task Phase 0 gate:** a complete Windows HostProfile and Windows admin/install authorization are **not prerequisites to writing/testing isolated, pure, portable S3.2a Python code**. This is not a waiver for Windows native code, native runs or installation. S3.2a must not claim `LAB_SERVICE_TESTED`, `PROCESS_QUALIFIED` or `POWER_LOSS_QUALIFIED`.

## 2. Explicitly approved S3.2a work

New, portable Python 3.12 LAB/1 codec, synthetic `S32_FIXTURES_1` factory, pure bounded mock authorization and RAM-only dispatcher, plus pure unit tests. Linux execution is permitted. Reuse the **unchanged** S1 decoder and S2.1–S2.4 transaction model/virtual store. Never add production authority or treat a synthetic principal as authenticated Windows identity.

Strict new-file allowlist (no edits to existing files):
- `editorial/windows_lab/__init__.py`
- `editorial/windows_lab/protocol.py`
- `editorial/windows_lab/fixtures.py`
- `editorial/windows_lab/dispatcher.py`
- `tests/test_windows_lab_protocol_v1.py`
- `tests/test_windows_lab_dispatcher_v1.py`
- `docs/tasks/E01_3_9_4_S3_2A_RESULT.md`

No `service.py`, `client.py`, `win32_native.py`, `manifest.py`, PowerShell installers, SCM operations, named-pipe implementation, real SID/SDDL/ACL/token inspection, DPAPI, native attempted-write observer, production protected writer, actual journal/anchor/registration, key provisioning, network service, subprocess or GPU dependency. Test-only synthetic 32-byte S1 keys are allowed **only as RAM fixtures** and must never be treated as production keys. No modifications to S1/S2/golden or existing architecture decisions.

## 3. Approved hash/host sequencing

1. **Before S3.2a coding:** pin exact Git source SHA and S3.1a/S1/S2 contract revisions, the new-file allowlist and Python 3.12 runtime used for pure tests. No Windows VM is required for S3.2a.
2. **Before future native S3.2b work:** separately identify and approve a real isolated Windows 11 Pro x64 VM, OS edition/build/UBR, hypervisor/resources, permitted admin operations, source/runtime identity and evidence boundary. No implied authorization to change a normal developer workstation.
3. **After native adapter/test/observer artifacts are built but before any native run:** compute actual byte-exact SHA-256 values, pin source SHA and runtime, assemble full canonical S3.1a HostProfile, independently check hashes, and obtain separate owner approval for the exact profile and installation/test execution.
4. **Any relevant host/runtime/source/artifact change:** STOP, re-pin and reapprove before native execution. No placeholder/fabricated or circular self-hashes.

This sequencing is a procedural clarification only. It does not relax `LAB_ACL_1`, `LAB_LIMITS_1`, the RISK-01–RISK-04 checks or LT01–LT15 for future S3.2b.

## 4. Immutable boundaries and STOP

`PUBLISH_REVISION` stays DISABLED; partial COMMIT reconstruction OFF. All E00/A/O/D1–D12/S1/S2.1–S2.4/D-01/golden behavior remains unchanged. No Q1, protected Windows storage, production profiles, S3.2b, S3.3, PR, merge, release or `main` change is authorized.

The next action is the **separate S3.2a Codex task**. Publish a feature branch and result for independent review; STOP before S3.2b.
