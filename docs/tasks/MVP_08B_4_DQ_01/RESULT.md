# MVP-08B.4-DQ-01 / STAGE-A-RESUME-2 — Result

**STAGE_A_PURE_READY_FOR_INDEPENDENT_REVIEW**

**Native status: NATIVE_BLOCKED_PRE_WRITE_GATE.** PURE_ONLY / NO_NATIVE_WRITES.
Date: 2026-11-20 (Europe/Kiev). This is the implementation author's result,
not independent acceptance or permission to begin the next stage.

## Exact provenance and publication identity

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Branch: `feat/mvp-08b-4-dq-01-native-sqlite-lab`.
Resume base commit: `6190dc50bd13bbb34e0adcc57ddc219a4c5cd44d`.
Verified base tree: `68554f3fc4f4ef560a0ce3502b58b820d5c12f5d`.
Contract authority: `4a6780bf519e03ddafa5ae9d7ed0f4309bff7c89`.
Verified authority tree: `e327219b1ba07de5479d167d3280ff29024f90a8`.

The owner reports independent reviewer C-A01 **ACCEPTED_DOCS_ONLY** in the
STAGE-A-RESUME-2 instruction. This is the source of the acceptance record;
no new independent acceptance is asserted here. Contract objects were read
at the exact revision. No contract branch merge/copy into implementation,
main update, CI/dependency/core modification or extra path was performed.
The resume started on the exact clean HEAD/tree; no AGENTS.md was found by
workspace search. Prior reports remain available in commits 9729a426… and
6190dc50…; their incomplete/blocking statuses are superseded only for Stage A.

The publication reply supplies final commit/tree and this report's own hashes
without a self-hash cycle. Verify with `git rev-parse HEAD HEAD^{tree}`.
Exact diff: `git diff --binary 6190dc50bd13bbb34e0adcc57ddc219a4c5cd44d HEAD`.

## Completed pure implementation

Only the three authorized existing files changed:

- `experimental_mvp/durable_storage_lab/contracts.py`;
- `tests/test_dq01_contracts.py`;
- `docs/tasks/MVP_08B_4_DQ_01/RESULT.md`.

The module supplies strict canonical JSON/typed refs/byte closure, all **17
closed DQ.LAB v2 record schemas**, their inline types and all **9 closed
synthetic payload schemas**. It rejects missing/extra keys, bool-as-int,
noncanonical UUID/digest/hex, unsupported states/versions/scope/kinds,
non-scalar Unicode, duplicate keys, float/nonfinite numbers, changed raw
payload hash/length, unsorted/duplicate sets and unresolved/substituted refs.
The exact Config literals, closed PhysicalIdentity/Custody/Checks structures
and separate evidence version 2 / SQLite schema version 1 are preserved.

`DocumentGraph` resolves only explicit case roots and their full typed closure,
including decoded payload edges. It enforces binding/role/ownership,
admission key identity, immutable object and member history, job/event/CAS
revision consistency, slot state and current indices, marker/root replay,
registry/P/A/R generations, complete projections and model outbox/read limits.
Iteration, caching and depth/node bounds do not create a general DAG engine.
Validated internal records are not exposed as mutable cached authority.

Pure semantic checks cover PrepareEvidence, CommitProof, AbsenceProof,
HoldEvidence, RecoveryEvidence and ProofAck. They check exact M/binding,
marker/member/projection presence or absence, retained original ticket bytes,
pre-R proof/snapshot, Ack G+1 and post-R control/root linkage. Historical
application root and current control root are separate. Absence does not
follow from staging or false boolean assertions. Recovery resolution alone
cannot release a barrier. R absence allows only the same exact retained
Ack/M step; it never authorizes reapplying A or recomputing Ack from a fresh
snapshot. Known documentary A COMMITTED survives lost/invalid R material,
including a missing retained R bundle when an independent original A proof
remains available for the same M/binding.

In-memory DTO histories exercise ADVANCE_MODEL, ENQUEUE_MODEL,
RESERVE_READ_MODEL and TERMINAL_MODEL after the literal ADMIT history,
including one token/job, three calls/checkpoint, retained history, terminal
release and refusal to reopen a terminal job. This is not a store, dispatcher,
executor, native recovery test or production JobStore implementation.

## Bytes, schema, documentary semantics and native qualification

These boundaries are explicit in the APIs:

1. `typed_ref` hashes canonical header-bearing bytes; it intentionally does
   not certify a schema or proof.
2. `validate_schema` checks closed structures and payload encoding.
3. `DocumentGraph.validate` checks conditional documentary semantics and
   returns no native proof or permit.
4. `evaluate_document_case(inputs, facts, resolve)` receives **no case ID,
   finding, expected answer or rule text**. It computes a `DocumentDecision`
   from explicit case-local material and conditional facts.
5. Every decision has `native_qualified=false`,
   `native_application_outcome=UNKNOWN`, `execution_authorized=false`.
   Those read-only properties are checked for all 23 oracle results.

DocumentDecision.application_outcome and next_action are conditional fixture
semantics only. No native COMMITTED/NOT_COMMITTED, custody qualification,
SQLite checks or permissions result from valid hashes, true fixture facts or
a successful pure validator. Checks/Custody assertions remain synthetic.
There is no native adapter, native caller or effect API in this increment.

C-A01 is applied exactly: F01-P03 explicitly supplies **V-TP** as
original_ticket, F02-P07 explicitly supplies **V-TA**. Raw ticket_sha256 never
fetches missing bytes. Negative missing-ticket cases remain UNKNOWN/HOLD;
removing/substituting original_ticket or setting a true flag without bytes
fails closed. Added tickets never establish live coordinator continuity or
custody. The global fixture dictionary is only a resolver for explicit typed
edges; literal-only tests use their own explicitly declared all-entry roots,
not an implicit DOC.ORACLE fallback.

All **58 canonical literals** (57 distinct preimages, HT/HC alias) match
pinned authority bytes/lengths/SHA-256 exactly and match the unchanged base
literal tuples. All **23 case objects** match the new authority exactly,
including expected outcomes, facts and explicit C-A01 original_ticket refs.
A separate AST/Git-object comparison verified these equalities, exit 0.

## Actual 23 semantic oracle results, separate from diagnostics

The dedicated pytest selection `-k test_semantic_oracle` executed exactly 23
cases on each interpreter. Each checks five outcome/generation/barrier fields,
allowed-action semantics and denied native authority. No diagnostic test is
counted as one of these 23 semantic PASS results.

| Case | Documentary A | G | Documentary R | Barrier / uncertainty | Python 3.10.22 / 3.13.18 |
|---|---|---:|---|---|---|
| F01-P01 | NOT_COMMITTED | 0 | NOT_STARTED | true / false | PASS / PASS |
| F01-P02 | NOT_ATTEMPTED | 1 | NOT_STARTED | true / false | PASS / PASS |
| F01-N01 | UNKNOWN | None | NOT_STARTED | true / true | PASS / PASS |
| F01-N02 | UNKNOWN | None | NOT_STARTED | true / true | PASS / PASS |
| F01-N03 | UNKNOWN | None | NOT_STARTED | true / true | PASS / PASS |
| F01-N04 | UNKNOWN | None | NOT_STARTED | true / true | PASS / PASS |
| F01-N05 | UNKNOWN | None | NOT_STARTED | true / true | PASS / PASS |
| F01-N06 | UNKNOWN | 1 | NOT_STARTED | true / true | PASS / PASS |
| F01-P03 | NOT_COMMITTED | 1 | COMMITTED | false / false | PASS / PASS |
| F02-P01 | NOT_ATTEMPTED | 1 | NOT_STARTED | true / false | PASS / PASS |
| F02-P02 | COMMITTED | 2 | NOT_STARTED | true / false | PASS / PASS |
| F02-P03 | UNKNOWN | None | NOT_STARTED | true / true | PASS / PASS |
| F02-P04 | COMMITTED | None | UNKNOWN | true / true | PASS / PASS |
| F02-P05 | COMMITTED | 3 | COMMITTED | false / false | PASS / PASS |
| F02-P06 | COMMITTED | 2 | NOT_COMMITTED | true / false | PASS / PASS |
| F02-P07 | NOT_COMMITTED | 2 | COMMITTED | false / false | PASS / PASS |
| F02-N01 | COMMITTED | 3 | UNKNOWN | true / true | PASS / PASS |
| F02-N02 | COMMITTED | 3 | UNKNOWN | true / true | PASS / PASS |
| F02-N03 | COMMITTED | 3 | UNKNOWN | true / true | PASS / PASS |
| F02-N04 | COMMITTED | 4 | UNKNOWN | true / true | PASS / PASS |
| F02-N05 | COMMITTED | 3 | UNKNOWN | true / true | PASS / PASS |
| F02-N06 | COMMITTED | 1 | UNKNOWN | true / true | PASS / PASS |
| F02-N07 | COMMITTED | 2 | UNKNOWN | true / true | PASS / PASS |

The two descriptive allowed_next labels QUALIFIED_REOPEN_INSPECT_ONLY and
QUALIFIED_INSPECT_A_ONLY express the same pure restriction here: inspection
of A, no application write. Their cases have identical inputs/facts. The test
oracle maps both to INSPECT_A; it does not echo case ID/rule text to fabricate
a distinction. All other allowed-next labels are checked against their
specific computed action (same-M apply, exact R, same-Ack retry, historical
read-only replay or next-new-M). Reopen itself is a future native procedure,
not exercised or authorized by these pure results. Original expected strings
are preserved in the fixtures; no contract values were edited.

## Final audited test matrix

Python 3.10.22 build: Oct 9 2026 15:21:30, Clang 22.1.3.
Python 3.13.18 build: Oct 26 2026 14:08:20, Clang 23.1.3.
pytest: **9.2.0** on both. Existing venv interpreters were used without installs.

| Final suite | Python | PASS | FAIL | SKIP | Deselected | Exit | pytest duration |
|---|---|---:|---:|---:|---:|---:|---:|
| 23 semantic oracle | 3.10.22 | 23 | 0 | 0 | 373 | 0 | 1.43 s |
| 23 semantic oracle | 3.13.18 | 23 | 0 | 0 | 373 | 0 | 1.11 s |
| Remaining DQ schema/graph/adversarial | 3.10.22 | 373 | 0 | 0 | 23 | 0 | 11.45 s |
| Remaining DQ schema/graph/adversarial | 3.13.18 | 373 | 0 | 0 | 23 | 0 | 8.11 s |
| Six unchanged PURE modules | 3.10.22 | 203 | 0 | 0 | 0 | 0 | 20.99 s |
| Six unchanged PURE modules | 3.13.18 | 203 | 0 | 0 | 0 | 0 | 17.63 s |
| Read-only SP subset | 3.10.22 | 65 + 110 subtests | 0 | 0 | 4 | 0 | 0.31 s |
| Read-only SP subset | 3.13.18 | 65 + 110 subtests | 0 | 0 | 4 | 0 | 0.26 s |

The complementary DQ selections cover all **396** tests per interpreter;
selection deselections are not unexecuted tests. In the 373, 23 byte-input
diagnostics remain diagnostics, distinct from the dedicated semantic tests.
SP excludes four genuinely unexecuted file-writing tests: test_missing_wav,
test_duplicate_json_rejected, test_read_limit, test_symlink_rejected.
Full SP PASS and Windows qualification are not claimed.

Both final commands were bounded by an external 60 s watchdog, each running
four suites sequentially. Command totals: **34.369 s** (3.10) and **27.256 s**
(3.13), exits 0, no timeout. Final acceptance testing remained below 300 s.
Each successful command reported **AUDIT_BLOCKED_EVENTS []**.

Environment: `PYTHONDONTWRITEBYTECODE=1`,
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, Python `-B`; pytest common arguments:
`-q -s -p no:cacheprovider -p no:tmpdir -p no:logging`.
The pre-pytest audit hook rejects write-mode opens, SQLite connections,
subprocess spawning, socket connects/binds, mkdir/remove/rename/chmod/link/
symlink/fork/posix_spawn/system/kill. Raw stdout includes every computed
SEMANTIC_ORACLE decision and suite exit/timing in execution-tool records.
No JUnit, cache, temp file or native log was generated. Python audit coverage
is not a claim of native syscall isolation or SQLite path qualification.

Development checks are not hidden: an earlier run returned exit 1 with
**2 failed / 312 passed** in 3.40 s; F01-N01/N02 improperly exposed generation
from a snapshot after custody/ticket loss. This was corrected to None without
weakening expected answers. A subsequent pre-final run passed 387 tests in
8.45 s, exit 0. Final audited runs above additionally cover the independent A
proof / missing R-bundle edge and other adversarial cases. No final failure,
skip or command timeout remains.

## File hashes and unchanged boundaries

| File | Git blob SHA-1 | Raw SHA-256 |
|---|---|---|
| experimental_mvp/durable_storage_lab/contracts.py | 801bc24d4331d4c1781ffddb32508d0b0ae051ee | ef3cae2e5c5fd2a5b562019d0c78fe17fe5b318a32e20da0db1c2f5fce5739f8 |
| tests/test_dq01_contracts.py | 333d5fb6a9d48eb6a7db1ad69c3d9d90f805cddb | e16e7c86ebdd1bb8ee834ad5ed47a68e9528c30d2367d5a6f7f37bcd2782aa42 |

The report's own final blob/SHA-256 is supplied in the publication reply.
Pinned authority NATIVE_EVIDENCE_CONTRACT_PROPOSAL.md SHA-256:
`a395951c100346a96eb6249f55c097db953e1dbf3d225bc0a360893379cd0a5c`.
It is read at commit 4a6780bf… and not changed or copied into this branch.
Only the three allowed existing paths differ from resume base; no new paths.
All G1–G6/PURE/SP implementations and contracts, OD4/CP decisions, dependencies
and CI remain unchanged. Main is read-only; no merge or release.

## Limitations and STOP

- Native pre-write gate remains unpassed. `/home/agent/dq01-lab-isolated`
  remains the unqualified absent candidate on read-only overlay per the owner
  instruction; this task did not create it, probe writes or select a fallback.
- SQLite connections, DB/journal/root creation, native measurements/PRAGMA,
  native evidence, native storage/recovery/security and FI-01–FI-22: NOT_RUN.
- Native process kill, fault injection, VFS/fsync and power-loss: NOT_RUN.
- Windows qualification, providers/executors, production and next Stage:
  NOT_RUN / NOT_AUTHORIZED in this task.
- Synthetic facts are not trusted measurements, signatures, rights clearances
  or qualified custody. This pure code does not close OS/storage TOCTOU risks.
- The result is ready for independent **Stage A pure review only**. No own
  report is substituted for independent acceptance or owner authorization.

**STOP after publication.** Do not begin Stage B/native work or any next
implementation stage without independent acceptance and its required grants.
