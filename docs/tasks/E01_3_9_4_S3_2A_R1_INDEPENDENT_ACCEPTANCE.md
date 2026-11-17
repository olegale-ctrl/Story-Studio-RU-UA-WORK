# E01.3.9.4 / S3.2a-R1 — Independent acceptance (PURE_ONLY)

**Date:** 2026-11-09. **Decision:** **ACCEPTED / PURE_ONLY**.
**Review scope:** published source and GitHub evidence, not Windows-native qualification.
**Repository:** `olegale-ctrl/Story-Studio-RU-UA-WORK`.

## Exact provenance

- Initial S3.2a implementation: `b27a084c99510406c407d5785328a31eb5f1df94`.
- Initial independent review and defect S32A-R01: `c61d82591ec37d1285672f599180aa0c7fa2125c`, `docs/tasks/E01_3_9_4_S3_2A_INDEPENDENT_REVIEW.md`.
- Corrective implementation R1: `13ed35db93e05641631ad3fa4a0d2ea3475c6719`.
- QA evidence: `4d979c5ee73ac64e8153aa061ab1369dca1623f2`, `docs/tasks/E01_3_9_4_S3_2A_R1_ACCEPTANCE_EVIDENCE.md`.
- Verified GitHub compare QA evidence vs R1: exactly one commit, one new Markdown report (253 lines), no source/test changes; QA branch HEAD matches reported SHA; no PR observed. No GitHub workflow run or commit status supplied as independent test proof.
- The current review is a separate docs-only acceptance, not an amendment to the approved S1/S2/S3.1a contracts.

## Independent source review of S32A-R01

Reviewed `editorial/windows_lab/dispatcher.py`, `fixtures.py` and negative tests at the QA evidence SHA.

- `Factory.candidate()` builds fixture bytes/transaction without constructing `VirtualStore` or calling `TransactionModel.execute`.
- `Dispatcher._dispatch()` checks fixture request byte identity, policy/grants, 32-admission limit, quarantine and pre-admission faults **before** calling `Factory.materialize()`.
- `materialize()` is the explicit boundary that may execute a synthetic S2 seed for an admitted cold request, with a stable-head comparison. Early W0 rejection without events does not retain an empty store.
- R1 tests prepare cold requests using an independent helper factory and instrument `TransactionModel.execute` to reject unexpected execution on denied requests. They cover policy, missing grants, pre-admission faults, byte mismatch, quarantine and capacity.
- Existing exact replay/LOOKUP and authorized cold paths remain covered in the test suite. No source-level recurrence of S32A-R01 was identified.

The QA report additionally documents an independent pre-R1 vs R1 cold differential: pre-R1 attempted one synthetic seed execution on denied cold B; R1 attempted zero. This is **Codex-reported diagnostic evidence**, not an independently rerun probe by this reviewer.

## Test evidence and limitation

The QA report records these completed **Linux / Python 3.12.14** runs:
- LAB protocol: **10 OK**.
- LAB dispatcher: **24 OK**.
- Existing storage suites: **169 OK**, including the D-01 regression.
- Full discovery: **842 OK**.
- Extra cold-denial / differential probes and log SHA-256 are documented in the QA report; private logs are not attached to GitHub.

These runs were **not independently executed** by this reviewer. Acceptance relies on independently inspected GitHub source/diff and the explicit Codex test evidence. It does not represent CI or Windows-native proof.

The previous Windows run reported **841 OK / 1 FAIL** in full discovery: `tests.test_sprint23_2.Sprint232Tests.test_env_override`. The QA report shows unchanged test and production blobs across R1 and a Linux `PureWindowsPath` diagnostic reproducing the same separator-sensitive assertion on both revisions. Classify as **BASELINE_PLATFORM_FAILURE**, not a new R1 storage regression. The real Windows rerun is **BLOCKED** and remains open for a separate cross-platform test task. Do not rewrite the earlier FAIL as PASS.

## Immutable boundaries and qualification

- S1/S2.1–S2.4, D-01, golden vectors, S3.1a, `LAB_ACL_1`, `LAB_LIMITS_1` remain unchanged.
- `PUBLISH_REVISION` **DISABLED**; partial COMMIT reconstruction **OFF**.
- Only portable Python RAM/fixture behavior is accepted. No real SID/SCM/ACL/SDDL/named pipes, token impersonation, Windows service, attempted-write observer, native protected writer, NTFS durability, DPAPI or power-loss evidence is claimed.
- `LAB_SERVICE_TESTED`, `PROCESS_QUALIFIED`, `POWER_LOSS_QUALIFIED`: **NOT EARNED**. Native LT01–LT15 and native RISK-01–RISK-04 remain pending/blocked.
- S3.2b implementation, installation and native test execution remain **NOT AUTHORIZED** until separately approved host, admin scope, pinned runtime/source and later exact HostProfile/artifact hashes per `E01_3_9_4_S3_2A_OWNER_DECISION.md`.
- External-ideas register remains in its own docs branch at `4ad198a095b155a57d6d0b162fc977260119962b`; candidates are not adoption approvals. No registry merge or implementation is implied.

**Disposition:** close S32A-R01 and S3.2a at **ACCEPTED / PURE_ONLY**. Next authorized activity may be **documentation-only S3.2b host readiness preflight**, not native coding or installation. Any native work requires a new explicit owner gate. No PR/merge/release/`main` changes.
