# E01.3.9.4 / S3.2a — Independent review of portable LAB Core

**Date:** 2026-11-06. **Review verdict:** `CHANGES_REQUIRED` before independent sign-off on S3.2a. Existing Codex qualification `PURE_ONLY / S3_2A_PORTABLE_TESTED` is accurately labeled but not yet independently accepted as conforming to every pre-admission invariant.

**Reviewed GitHub commit:** `b27a084c99510406c407d5785328a31eb5f1df94`. **Exact base:** `8967e858916bc7884e03c01aff33d5a2b7079612`.

## 1. Independent provenance and scope checks

- `compare_commits`: exactly one commit ahead, zero behind, exactly seven paths: `editorial/windows_lab/{__init__,protocol,fixtures,dispatcher}.py`; `tests/test_windows_lab_{protocol,dispatcher}_v1.py`; `docs/tasks/E01_3_9_4_S3_2A_RESULT.md`. Six Python files added, prior STOP result updated with history preserved.
- Remote feature-branch HEAD matched `b27a084c99510406c407d5785328a31eb5f1df94`; `main` observed at `e1f4efb0fb5ff290bb198349213c004b4667ef0f` (unchanged). No PR found for feature branch.
- Reviewed full current `protocol.py`, `dispatcher.py`, `fixtures.py`, both new test sources, source S1 `storage_protocol_v1.py` and S2 `storage_transaction_model_v1.py`; inspected Codex result. No native SCM/Windows service, network listener or protected writer added.
- Codex reports 10 protocol + 19 dispatcher unittest OK; 169 preexisting storage tests and 837 full discovery OK, 144 gate/decision cases 12 allow / 132 deny. These are **Codex-run reports**; independent reviewer **did not run the Python tests or inspect the private raw logs**, and GitHub had no status checks / workflow runs for this commit.
- Explicitly correct NUL separator `bytes([0])`, and tests cover three literal LAB byte oracles, internal validated S1 Receipt/MAC and non-exposure of raw receipt in the LAB response.
- S3.2b / S3.3 not authorized and `LAB_SERVICE_TESTED` / `PROCESS_QUALIFIED` / `POWER_LOSS_QUALIFIED` not earned.

## 2. BLOCKING REVIEW FINDING S32A-R01: cold unauthorized request causes synthetic seed execution before policy denial

**Normative basis:** S3.1a §6.3, mandatory dispatcher ordering and invariant: on pre-admission failure, **zero model W1/PREPARE/events/IDs**; startup seed operations must be distinguishable from authorized client admission. Prior owner-approved task §4 repeats this.

**Observed source order (static code review):**
- `editorial/windows_lab/dispatcher.py` `_dispatch` around lines 98–108 calls `self.factory.candidate(actor, probe, slot)` **before** `self.factory.allowed(actor, probe)`; it also calls the candidate builder before checking 32-admission capacity, quarantine or pre-admission fault branches.
- `editorial/windows_lab/fixtures.py` `Factory.candidate` around lines 500–513, on a cold non-genesis probe, creates `VirtualStore`, computes a GENESIS/IMPORT seed and invokes unchanged `TransactionModel.execute(seed)`, producing synthetic W1/journal/anchor operations, before saving `_stores[key]`.
- Thus a first-time **unauthorized B** or **cross-policy denied** LAB request can trigger model seed execution and populate `_stores` while it will then be rejected `LAB_POLICY_DENIED`. A capacity/quarantine/fault rejection can likewise cause new cold-case preparation before its rejection.
- The new test `test_all_probes_recognized_for_all_policies_and_b_denied` prepares the target via `d.execute_frame('B', probe)` **before** taking the baseline (`before=self.events(d)`). But `execute_frame` itself calls `factory.candidate`; consequently that test does not detect cold pre-authorization model work. The 144-cell test uses the same preparation pattern.
- This is a **source-level causal finding**, not a claim of independently executed failing unit test, nor any indication of real disk writes or OS privilege bypass. Existing success assertions and count `model_calls == 0` do not cover `TransactionModel.execute(seed)`, which is invoked directly inside the Factory and not counted by the dispatcher.
- The separation of synthetic startup fixture seeding from client operations must be explicit. **Lazy seeding on the unauthorized request path is not evidence of zero events at denial time.**

**Required correction, without dictating implementation architecture:** design a pure pre-admission path for identity/scope, request-id whitelist, live grant, quota, quarantine and deny/fault checks **before any stateful model seed**, or isolate/prebuild approved seeds outside request admission and prove the separation. Validate full request-template bytes before accepting an operation; avoid broadening the fixture whitelist or moving client-controlled bytes into authority. On a cold unauthorized or malformed but structurally valid request, ensure no new S2 model operation/events/ids, including temporary synthetic stores; no hidden fixture seeding from rejected request paths. If this cannot be achieved under fixed S3.1a constraints, STOP and report the precise contract/design issue rather than weakening the invariant.

## 3. Required independent negative regression tests

The tests must not accidentally mutate the **target** dispatcher before taking baseline:
1. Obtain a deterministic valid LAB EXECUTE frame from a **separate helper/factory instance** sharing pinned run/incarnation/policy; do not call `execute_frame` on the target. Construct a new cold target dispatcher with `_stores == {}`; invoke `dispatch(frame, Caller('B'))` for at least a GD probe. Assert `LAB_POLICY_DENIED`, `model_calls == 0`, `admissions == 0`, and no model seed execution or virtual events on target (instrument `TransactionModel.execute` in a way that also detects factory seed calls).
2. Same for actor A with cross-policy denied GD request (recognized fixture ID), CG_WRITER_ONLY / CG_NONE and missing grant.
3. Independently exercise fault-before-admission (`READ_STALL`, `DISPATCH_STALL`, `PRE_ADMISSION_DENY`) for cold non-genesis probes, so fault denial cannot seed S2.
4. Exercise the 33rd valid request **for a cold new probe** after quota 32 is reached, and a quarantined cold new probe. Ensure no additional seed events/model calls before `LAB_CAPACITY` or `LAB_BUSY`. Known exact replay/LOOKUP must still succeed without a new seed.
5. Test structurally valid but **full-byte-mismatched** request (approved fixture request ID with altered reason/session) on a cold non-genesis target: response denial/conflict, zero S2 model operations including seed. This is necessary to establish the mandatory pre-admission ordering across content and fixture matching.
6. Run existing exact-byte oracles, 144 GD cells, 30 CG cases, B denied, 32/33 capacity, loss/restart/receipt NUL checks, storage 169 and full discovery. Preserve normal authorized cold-case success.

**Test labels:** all of the above remain `PURE_ONLY`; not Windows LT03–LT06/08/14 native proof. Do not claim `LAB_SERVICE_TESTED`.

## 4. Non-blocking observations

- `Factory.candidate` currently generates/retains synthetic seeds on demand; cost and reproducible denial economics deserve explicit bounded measurements (candidate generation is expensive in the report). Keep deterministic runtime bounds and no unbounded materialization.
- `protocol.py` maintains a manually copied S1 error-name tuple; this carries version-drift risk. Do not refactor S1/S2 in this correction. Consider pinning a parity test if the approved S1 contract defines a public error vocabulary.
- Reported dispatcher suite (~829 s) and full discovery (~1002 s) are costly; future performance work should preserve semantics and evidence. Not a reason to relax 144 authorization checks or receipt validation.

## 5. Review disposition and next action

**Do not accept S3.2a as fully compliant or initiate S3.2b/S3.3 yet.** The published code and existing tests are valuable, and the Codex `PURE_ONLY` execution report stands, but fix S32A-R01 and demonstrate the new cold-denial invariants.

Next task: tightly scoped `S3.2a-R1` correction in a fresh feature branch **only within existing S3.2a seven-path allowlist**, including full result and reproducible negative tests. No changes to S1/S2, golden vectors, native Windows code, main, PR/merge/release. STOP after publish for another independent review.

This independent review is a **docs-only** report; it authorizes no new native or production capabilities.
