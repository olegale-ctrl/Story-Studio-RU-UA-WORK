# CODEX TASK — E01.3.9.4 / S3.2b Phase 0: Windows LAB host readiness

**Date:** 2026-11-09. **Status:** DOCUMENTATION-ONLY PREFLIGHT AUTHORIZED; **S3.2b NATIVE IMPLEMENTATION/INSTALL/RUN NOT AUTHORIZED**.
**Repository:** `olegale-ctrl/Story-Studio-RU-UA-WORK`.

## 1. Source and execution rule

Read this task from branch `docs/editorial-e01-3-9-4-s3-2a-accept-s3-2b-phase0`. Before any action, fetch and verify its exact remote HEAD SHA; record it as the base. Do not silently use `main` or an older S3.2a branch. If the branch advanced after the owner's handoff, STOP and report the new SHA for reconciliation.

Create only a new documentation branch:
`docs/editorial-e01-3-9-4-s3-2b-phase0-host-readiness`.

If it already exists, do not reset/force-push it; inspect and STOP if ownership/history is unclear.

## 2. Normative reading order

1. `docs/tasks/E01_3_9_4_S3_2A_R1_INDEPENDENT_ACCEPTANCE.md` — accepted `PURE_ONLY`.
2. `docs/tasks/E01_3_9_4_S3_2A_R1_ACCEPTANCE_EVIDENCE.md` and S32A-R01 review.
3. `docs/tasks/E01_3_9_4_S3_2A_OWNER_DECISION.md` — approved phase split and hash/host sequence.
4. `docs/tasks/E01_3_9_4_S3_2_OWNER_LAB_DECISIONS.md` — L-01–L-04, RISK-01–RISK-04.
5. `docs/tasks/E01_3_9_4_S3_1A_LAB_EXECUTION_CONTRACT.md` — LAB/1, HostProfile §7.1, LT01–LT15, native evidence boundaries.
6. `docs/tasks/E01_3_9_4_S3_2_PREFLIGHT.md` and `E01_3_9_4_S3_2_PHASE0_REVIEW_AND_SPLIT_PROPOSAL.md` — earlier STOP and sequencing.
7. `docs/tasks/E01_3_9_4_S3_1_WINDOWS_STORAGE_SPEC.md` — design vs actual qualification.
8. Separately read `docs/architecture/EXTERNAL_IDEAS_AND_ADOPTION_REGISTER.md` at branch `docs/external-ideas-adoption-register`, SHA `4ad198a095b155a57d6d0b162fc977260119962b`, without merge/cherry-pick. Note applicability; candidates are not approved integrations.

S1/S2/D-01/golden, `LAB_ACL_1`, `LAB_LIMITS_1` are immutable. `PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF.

## 3. Phase 0 goal

Prepare a factual **read-only host readiness report** for separately approving **one isolated maintained Windows 11 Pro x64 virtual machine** as the future native LAB host.

**Do not assume the current workstation, Codex Linux container, WSL session or ordinary Windows PC is the approved isolated VM.** If no VM is available, produce an honest blocked report and a minimal owner input checklist. Do not invent host values or use placeholders as if observed.

Gather only non-invasive, available facts, explicitly marking each as `OBSERVED`, `OWNER_DECLARED`, `TO_VERIFY`, `NOT_PROVIDED` or `BLOCKED`:

- VM alias (non-identifying), isolated guest access method and actual VM/host distinction.
- Windows edition, version, full build and UBR, x64 architecture, update/support/licensing status.
- Hypervisor type/version, allocated vCPU/RAM, virtual disk size, local NTFS volume, isolation from production.
- Offline/network restrictions, shared folders/clipboard/host mounts, snapshots/rollback and whether real user/production data, credentials, accounts or keys are absent.
- Candidate Python 3.12 runtime origin/version/bitness and private runtime pinning plan. Compute actual runtime hash only if the exact artifact is safely accessible; otherwise `TO_VERIFY`.
- Source commit/contract revisions and proposed private evidence location/retention, observer independence, redaction and cleanup.
- Separate owner/admin approval requirements for account creation, SCM install/start/stop/delete, pipe/ACL tests, fault injection, observer and VM rollback.

Target L-04: isolated Windows 11 Pro x64, **4 vCPU, 8 GiB RAM, 64 GiB virtual NTFS disk**, with no shared host folders or production data. These are approved target parameters, **not proof of the available machine**.

Do not publish actual account SIDs, passwords, tokens, personal machine names, serial numbers, product keys, private VM paths, real account identifiers, keys or private EvidenceIndex in GitHub. If a fact is sensitive, record only a redacted status and retain evidence privately.

## 4. Native sequencing: no shortcut

A. **Before native coding:** identify the exact isolated VM; establish owner approval of its use, permitted admin operations, source and runtime identity, and evidence boundary. No implicit approval from the L-01–L-04 design decision.

B. **After separately authorized native code is built, before any native run:** compute byte-exact SHA-256 for native adapter, test harness and independent observer; pin source/runtime; construct canonical S3.1a HostProfile; independently verify hashes and obtain owner approval of exact profile and installation/test scope.

C. Any relevant change to host, OS build/UBR, runtime, source, artifact or observer invalidates approval: STOP/re-pin/reapprove. No fabricated, empty, circular or pre-build artifact hashes.

Do **not** create full HostProfile with guessed artifact hashes during this Phase 0. An inventory/readiness record is not a HostProfile approval.

## 5. Risk and acceptance planning (documentation only)

Map native evidence still needed for:
- RISK-01: real restricted service SID, least privileges, impersonation/TokenUser/RevertToSelf and fail-stop.
- RISK-02: exact 1,052,672-byte single WriteFile, 4096-byte pipe buffers, 4 workers/1 dispatcher/queue 2, deadlines, slow readers and cancellation races.
- RISK-03: actual SCM/process/token/pipe rights, server authenticity and forbidden access checks.
- RISK-04: principal/request/session/full-bytes binding, replay/LOOKUP, restart unknown, 32 admissions/33rd refusal.
- LT01–LT15 including LT14 independent attempted-write observer, all denied attempts and redacted EvidenceIndex.

Describe the planned observer and evidence boundary, but do not implement or run them. Pure S3.2a tests do not qualify native behavior.

## 6. Strict allowlist and verification

**Only one new file may be created:**
`docs/tasks/E01_3_9_4_S3_2B_PHASE0_HOST_READINESS.md`.

It must contain:
1. Exact base/branch/source revision and docs consulted.
2. Observation method, environment actually accessible and trust level for each fact.
3. Host inventory/readiness matrix with explicit unknowns and blockers.
4. Owner decisions/permissions still required, with precise minimal questions.
5. Hash/HostProfile sequencing without fabricated values.
6. Native RISK-01–04 and LT01–15 readiness matrix (all unrun marked BLOCKED).
7. External-ideas applicability gate and Windows baseline failure noted as separate pending task.
8. Final outcome: `READY_FOR_OWNER_HOST_APPROVAL` only if actual VM facts are adequately verified, otherwise `BLOCKED_HOST_NOT_PROVIDED`, `BLOCKED_AUTHORIZATION` or another precisely justified `BLOCKED_...`.
9. Explicit STOP: no native implementation, install, service, SCM, accounts, ACL, observer or tests performed.

Do not modify code, tests, contracts, registry, `main`, CI, dependencies, S1/S2, golden or any other file. Do not run elevated commands, provision accounts, install services, change Windows settings, create shared folders or use production data. No PR/merge/release.

For documentation-only work run `git diff --check`, verify exactly one new file, exact base and clean worktree after push. No Python test run is required; do not claim test PASS without executing it.

## 7. Handoff and STOP

Publish the docs-only feature branch. Report exact base SHA, result SHA, remote HEAD, one-file diff, redacted host-readiness summary and any missing owner inputs. **STOP**. Do not start S3.2b native coding or S3.3. Owner approval is a separate future action.
