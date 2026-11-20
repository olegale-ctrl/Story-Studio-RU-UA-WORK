# DQ-01 PURE-RESUME — contract input ambiguity

**Current checkpoint status: BLOCKED_CONTRACT.** Native status remains
**NATIVE_BLOCKED_PRE_WRITE_GATE**. Date: 2026-11-20 (Europe/Kiev).

This section supersedes the earlier checkpoint report preserved below.
**Stage A is not complete and is not ready for acceptance.** The owner's
PURE-RESUME task explicitly requires BLOCKED_CONTRACT on a contract
contradiction; this checkpoint records the incompatible strict-input and
positive-oracle requirements rather than inventing an acceptance rule.

## Exact starting point and scope

- Branch: `feat/mvp-08b-4-dq-01-native-sqlite-lab` (continued, no reset).
- Resume base: `9729a426f50714b269d947232e07a010b61f0f84`.
- Verified resume base tree: `bdefe8aa69d79b410d5823978375a72357aadaec`.
- Working tree was clean before this task. No AGENTS.md was found by the
  workspace search.
- Unchanged authority: contract commit
  `c15ac152258586be1ed1b57f205830edfffc9ae1`, tree
  `19192e46ad0f3b3cc9d9bc9809d3896e1e13e639`.
- Exactly two existing authorized files changed: `tests/test_dq01_contracts.py`
  and this `RESULT.md`. `contracts.py` and all other code are unchanged.
- Full diff: `git diff --binary 9729a426f50714b269d947232e07a010b61f0f84 HEAD`.
  Final publication commit/tree and this report's self hashes are supplied in
  the publication reply; use `git rev-parse HEAD HEAD^{tree}` to verify.

## C-A01 — original ticket bytes absent from two positive case inputs

Pinned source: `docs/tasks/MVP_08B_4_DQ_00/NATIVE_EVIDENCE_CONTRACT_PROPOSAL.md`.

The following requirements must all be satisfied without contract changes:

1. Section 7, line 131: NOT_COMMITTED requires the exact retained ticket
   bundle, including canonical ticket and its full expected immutable closure.
2. Section 2, line 46: `AbsenceProof.ticket_sha256` is a Digest, whereas
   OperationTicket refs use the separately defined closed four-field Ref.
3. Catalogue rules, line 161: only the selected case's inputs/facts are
   available, and a missing ticket/Ack must not be borrowed from another entry.
4. F01-P03 (lines 986 onward) and F02-P07 (1325 onward) expect proven
   NOT_COMMITTED and namespace_barrier=false.

**Observed fixture facts, computed directly from the pinned Git object:**

| Case | Explicit ticket | Required ticket digest in AbsenceProof | Original ticket in inputs + typed/payload closure? | Expected outcome/barrier |
|---|---|---|---|---|
| F01-P01, control | TP | 07b38b65c665b6348837c7826110fa05e8bd08bf6b441508fc9648c0dae14831 | YES | NOT_COMMITTED / true |
| F01-P02, control | TA | 4c0e03133930623d16d0f40ca977e13ffc9d46be9599b82a5227a8aaad3af14a | YES | NOT_ATTEMPTED / true |
| F01-P03 | TRN0 | 07b38b65c665b6348837c7826110fa05e8bd08bf6b441508fc9648c0dae14831 (TP) | NO | NOT_COMMITTED / false |
| F02-P07 | TRN | 4c0e03133930623d16d0f40ca977e13ffc9d46be9599b82a5227a8aaad3af14a (TA) | NO | NOT_COMMITTED / false |

TRN0 hashes to
`4c5190b1c469b2c1ad69896a645bdd6af6196f1033f154256684cd00ae77b6a1`;
TRN hashes to
`1a9d07ade8de7cb512ccaa61ca7cb5700c786a82c7e6cf10eae74fd93539ce87`.
Neither supplies the original ticket bytes identified by its linked
AbsenceProof. Both are phase R tickets. ProofAck references the original
AbsenceProof; it does not add a typed reference to the missing TP/TA.

The two cases assert `ticket_retained=true`. That assertion is a conditional
fixture fact, not the missing canonical bytes or an explicit retained-bundle
input. The TP/TA literals exist elsewhere in the catalogue, so this is **not**
a missing repository artifact. The unresolved issue is case-local availability
and the authorized interpretation of that assertion.

An alternative interpretation is possible: treat `ticket_sha256` as a semantic
lookup edge into an explicitly retained bundle, with `ticket_retained=true`
asserting the bundle exists. The contract does not specify that bundle input
or its fixture availability rule, nor explicitly authorize lookup of those
bytes from the otherwise excluded catalogue. This checkpoint does **not**
claim that negative R is logically impossible. It records the ambiguity that
prevents simultaneously proving exact ticket bytes, respecting strict
case-local inputs, and accepting these two positive outcomes without choosing
an additional rule. A Digest lookup by itself must not manufacture custody.

No missing ticket was silently supplied, no historical proof was assumed to
be a separately trusted attestation, and no hash/schema was changed to make
these expectations pass. Full schema/proof implementation stopped at this
contract boundary, as instructed. This is a finding for independent review,
not a revision to G1–G6, OD4 or CP decisions.

## Reproduction and test meaning

The test module now embeds all 23 exact DOC.ORACLE records from the pinned
Markdown. The existing 58 canonical literals and all expected SHA/lengths are
unchanged. The earlier external document verifier was not used.

`_case_byte_closure` starts only from `case.inputs` and follows exact typed
refs, including decoded DataObject payload refs, through the hash-verified
catalogue resolver. It does not turn raw Digest strings or true facts into
extra edges. `_missing_absence_ticket_bytes` then compares each encountered
AbsenceProof.ticket_sha256 with the canonical OperationTickets actually
available in that closure. These helpers are diagnostics in the authorized
existing test file, not a new contract API.

The 23 `test_document_case_byte_inputs_only` tests check byte closures and
reproduce the missing-ticket inventory. The two positive-control and two
negative-close finding tests distinguish available original tickets from
phase R substitutes. Their successful assertions demonstrate the finding;
**they are not successful semantic executions of the 23 DOC.ORACLE cases**.
In particular, the code does not change the two official expected outcomes
into approved negative outcomes. No test uses an oracle's case ID or expected
answer to authorize a native proof.

## Actual PURE-RESUME test runs

| Suite | Python | PASS | FAIL | SKIP | Deselected | Exit | pytest time |
|---|---|---:|---:|---:|---:|---:|---:|
| Wire + contract-gap diagnostics | 3.10.22 | 179 | 0 | 0 | 0 | 0 | 1.49 s |
| Wire + contract-gap diagnostics | 3.13.18 | 179 | 0 | 0 | 0 | 0 | 1.18 s |
| Six existing PURE modules | 3.10.22 | 203 | 0 | 0 | 0 | 0 | 26.17 s |
| Six existing PURE modules | 3.13.18 | 203 | 0 | 0 | 0 | 0 | 22.00 s |
| Read-only SP subset | 3.10.22 | 65 + 110 subtests | 0 | 0 | 4 | 0 | 0.35 s |
| Read-only SP subset | 3.13.18 | 65 + 110 subtests | 0 | 0 | 4 | 0 | 0.37 s |

Python versions/builds and pytest 9.2.0 were measured again and match the
historical rows below. SQLite was not queried or connected for PURE-RESUME.
Each interpreter's three sequential suites ran under a 60 s outer timeout;
actual command totals: **28.180 s** (3.10), **23.691 s** (3.13), both exits 0.
No timeout, startup failure, skip or forbidden audit event occurred in these
resume runs. `AUDIT_BLOCKED_EVENTS []` on both interpreters.

The runner uses the same pre-pytest write/process/connect audit guard and
`PYTHONDONTWRITEBYTECODE=1`, `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, `-B`,
`-q -s -p no:cacheprovider -p no:tmpdir -p no:logging` as recorded below.
SP deliberately excludes `test_missing_wav`, `test_duplicate_json_rejected`,
`test_read_limit`, `test_symlink_rejected` because they create files. No full
SP PASS is claimed. No JUnit/native log/cache/temp/evidence file was generated.
Audit observation is not native syscall isolation or SQLite qualification.

## Completion matrix and resolution proposals

| Requested work | Current status |
|---|---|
| All 58 canonical byte entries / byte closures | PASS on both runtimes; 57 distinct preimages |
| All 23 case input byte closures and ticket-availability audit | Checked; two positive cases expose C-A01 |
| All 23 official semantic DOC.ORACLE outcomes | NOT_RUN / BLOCKED_CONTRACT; zero semantic acceptance claimed |
| 17 closed schemas, inline/binding/role/index validation | NOT_COMPLETED; contracts.py unchanged from resume base |
| Full CommitProof/AbsenceProof/Hold/Recovery/Ack semantics | NOT_COMPLETED / BLOCKED_CONTRACT |
| Adversarial schema/proof/generation/foreign-binding tests | Full requested set NOT_IMPLEMENTED; prior wire/ref negatives remain |
| Native root/runtime/SQLite/process/FI/security qualification | NOT_RUN / NATIVE_BLOCKED_PRE_WRITE_GATE |
| Windows / production | NOT_RUN / NOT_AUTHORIZED |

Possible resolution options, **PROPOSAL only**:

- Explicitly add the original TP to F01-P03 and TA to F02-P07 inputs, retaining
  their existing bytes/hashes and the strict case-local availability rule.
- Specify a retained-ticket-bundle input and its exact byte membership, plus
  whether ticket_sha256 is an authorized semantic lookup edge. Missing bundle
  entries or ticket_retained=false must remain fail-closed. A true flag alone
  must not become native qualification.
- If historical proofs are intended to enter already qualified, define that
  boundary and its required provenance explicitly; a public hash is not an
  attestation or replacement for missing custody evidence.

No option is selected automatically. Contract source files are outside this
resume allowlist and were not edited. Independent review should first decide
whether C-A01 follows the intended interpretation; if another interpretation
is already normative, identify the exact contract text and fixture inputs.

## Changed-file hashes and publication

`tests/test_dq01_contracts.py`:
Git blob SHA-1 `15c2b92f21a32a12738c62e9700ceb66bb1c1882`;
raw SHA-256 `6b39c237dce2231e419b0c0fc57cdd0a599300b9ef88d309e2158071292e8fd4`.
This report's final hashes are in the publication reply to avoid a self-hash
cycle. The historical file hashes below refer only to the prior checkpoint.

Only these two existing files are published. No root/DB/journal/native log,
SQLite connection, native child, fault injection, model/provider/media call,
CI/dependency/contract/main change, merge, release or production operation.
No native pre-write permission was requested again or inferred.

**STOP — BLOCKED_CONTRACT / NATIVE_BLOCKED_PRE_WRITE_GATE.** No Stage A-ready
claim and no automatic continuation after publication.

---

# Historical checkpoint 9729a426f50714b269d947232e07a010b61f0f84

The following content is preserved as the prior run record; it is not a claim
that its counts, file hashes, status or implementation scope describe resume.

# MVP-08B.4-DQ-01 — blocked pre-write gate / pure wire preparation

**Status: BLOCKED_PRE_WRITE_GATE.** Date: 2026-11-20 (Europe/Kiev).

This is a partial implementation checkpoint, not a completed SQLite lab,
native qualification, independent acceptance or authorization to continue.

## Authority and immutable inputs

- Owner task: MVP-08B.4-DQ-01; CP-01–CP-05 APPROVED_WITH_PRECONDITIONS.
- Subsequent owner answer: **ROOT NOT YET QUALIFIED**; the proposed
  `/home/<linux-user>/dq01-lab-isolated` is neither final nor authorized.
  Read-only preflight must be presented to the owner before confirmation.
  SQLite DB creation, native writes and fault injection remain forbidden.
- Implementation branch: `feat/mvp-08b-4-dq-01-native-sqlite-lab`.
- Exact implementation base: `162a5ff109358625c25ff92402064d214fa50bc0`.
- Verified base tree: `4c4bf6405e9dec6d707a1c6928b6068222469041`.
- Contract source: `c15ac152258586be1ed1b57f205830edfffc9ae1`.
- Verified contract tree: `19192e46ad0f3b3cc9d9bc9809d3896e1e13e639`.
- Contract branch was not merged or copied into the implementation tree.
- Native authority remains DQ.LAB version 2; physical SQLite schema/layout/
  user_version remains 1. Neither is revised by this wire-only checkpoint.

Publication commit/tree and this report's own hashes are supplied in the
publication reply: a tracked report cannot contain its own final Git identity.
Resolve them with `git rev-parse HEAD HEAD^{tree}` in the published branch.
Exact full diff: `git diff --binary 162a5ff109358625c25ff92402064d214fa50bc0 HEAD`.

## Read-only root preflight — no root selected or created

Measured process identity: uid=1000, gid=1000, user `agent`, passwd home
`/home/agent`, shell `/bin/bash`. The owner's template consequently maps to
**candidate only** `/home/agent/dq01-lab-isolated`.

| Existing component | Mode | uid:gid | st_dev | st_ino | lstat symlink / mount |
|---|---|---|---|---|---|
| `/` | 0755 | 65534:65534 | 27 | 262145 | false / true |
| `/home` | 0755 | 65534:65534 | 27 | 9223372036854776417 | false / false |
| `/home/agent` | 0700 | 1000:1000 | 27 | 9223372036854780767 | false / false |
| `/home/agent/dq01-lab-isolated` | MISSING | NOT_MEASURED | NOT_MEASURED | NOT_MEASURED | NOT_MEASURED |

Provenance: direct `id`, `getent passwd`, `uname -a`, `lstat`, `is_mount`
and read of `/proc/self/mountinfo` in the execution environment. The matching
mount entry for the candidate's existing ancestors reports mountpoint `/`,
filesystem **overlay**, options **ro,nosuid,nodev,relatime**. No write probe,
mkdir, chmod, root fallback or SQLite connection was performed. This is an
observation of existing ancestors, not a qualified root filesystem/identity.

The missing candidate has no physical identity, contents, ownership or
permissions to qualify. Its empty/exclusive/nonproduction status cannot be
established from a missing path. A canonical locator is not a physical root.
No claim is made that the read-only overlay can satisfy the selected local
storage profile. Root isolation, native C-level path enforcement, root/file
caps and custody remain **NOT_QUALIFIED**. No TOCTOU guarantee is inferred
from these read-only observations. The earlier Windows F-drive discussion
does not grant access to this Linux candidate or to any Windows host.

Required next owner action: review these measurements and supply/confirm a
concrete isolated Linux root that can actually be qualified. No substitute
under `/tmp`, workspace or another home was chosen. Confirmation of a locator
alone will not bypass the remaining runtime/security/profile checks.

## Runtime observations — not a measured qualification profile

OS: Linux 6.18.57, x86_64, glibc 2.41; kernel build string observed:
`#1 SMP Tue Oct 20 21:56:04 UTC 2026`.

| Interpreter | Python/build | pytest | sqlite3.sqlite_version attribute |
|---|---|---|---|
| `/workspace/work/venv310/bin/python` | 3.10.22; Oct 9 2026 15:21:30; Clang 22.1.3 | 9.2.0 | 3.53.1 |
| `/workspace/work/venv313/bin/python` | 3.13.18; Oct 26 2026 14:08:20; Clang 23.1.3 | 9.2.0 | 3.53.1 |

These are actual imported runtime attributes, not a SQLite query or database
measurement. SQLite source ID, compile options, PRAGMA support/readback,
database identity, schema cookie, profile canonical digest and root capacity
are **NOT_MEASURED / NOT_QUALIFIED**. No connection, including `:memory:`, was
opened. No matching profile or native PASS is asserted; no runtime was
installed, changed or silently substituted.

## Exactly what was prepared

Only side-effect-free wire foundations were implemented: strict canonical
UTF-8 JSON, lowercase SHA-256 typed references, full byte-reference closure,
iterative graph traversal, payload byte/hash/length checks and payload ref
edges. Duplicate keys, floats, nonfinite numbers, surrogates, noncanonical
bytes, foreign version/scope/kind references and unresolved/substituted bytes
are rejected. The package has no storage initialization on import.

**Stage A is incomplete.** These APIs expressly do not validate the 17 closed
record schemas, inline field schemas, binding, roles, indices, native checks,
custody, application outcomes or P/A/R proof predicates. `typed_ref` hashes a
header-bearing record; it does not certify a proof. `ByteClosure` is only
non-authoritative byte-graph statistics. No native caller exists.

Local codec implementation guards (64 JSON nesting levels, 100000 tree visits)
are not proposed changes to the approved evidence schemas or a qualified
resource policy. Graph bounds are separate: 2048 depth, 8192 nodes; record
bound 4 MiB, payload bound 1 MiB. Complete schema/resource qualification is
still required before using this preparation in the lab.

All 58 literal entries were extracted directly from the pinned native-contract
Markdown, retaining its expected lengths and SHA literals. The earlier local
build/check verifier was not imported or executed. Both byte identity and
reference closure were checked using this new implementation. HT/HC remain
identical bytes: 58 entries, 57 distinct canonical preimages. Catalogue
alternatives and deliberately bad semantic specimens were not interpreted as
one database history or accepted native evidence. This is a new local wire
check, **not independent acceptance** and not full vector conformance.

## Allowlist and exact changed-file registry

All ten authorized paths were absent in the exact base; the initial base
worktree was clean and the requested branch was unused. Only four paths below
are created. No placeholders for unimplemented storage APIs were introduced.
All new files use Git mode 100644.

| Authorized path | This checkpoint |
|---|---|
| `experimental_mvp/durable_storage_lab/__init__.py` | NEW; side-effect-free namespace |
| `experimental_mvp/durable_storage_lab/contracts.py` | NEW; wire-only foundations |
| `experimental_mvp/durable_storage_lab/store.py` | NOT_IMPLEMENTED / NOT_CREATED |
| `experimental_mvp/durable_storage_lab/root_guard.py` | NOT_IMPLEMENTED / NOT_CREATED; manual read-only preflight only |
| `experimental_mvp/durable_storage_lab/harness.py` | NOT_IMPLEMENTED / NOT_CREATED |
| `tests/test_dq01_contracts.py` | NEW; wire tests only |
| `tests/test_dq01_store.py` | NOT_IMPLEMENTED / NOT_CREATED |
| `tests/test_dq01_faults.py` | NOT_IMPLEMENTED / NOT_CREATED |
| `tests/test_dq01_security.py` | NOT_IMPLEMENTED / NOT_CREATED |
| `docs/tasks/MVP_08B_4_DQ_01/RESULT.md` | NEW; this blocked checkpoint report |

| New implementation/test file | Git blob SHA-1 | Raw SHA-256 |
|---|---|---|
| `experimental_mvp/durable_storage_lab/__init__.py` | c336e4208cb66d1890f3c43842fca824682f487e | a4c515045748cf5ba88a50f63215cc9fa26b7768993a0dc1c903c74b75ed8939 |
| `experimental_mvp/durable_storage_lab/contracts.py` | 7cd78144d61cf9673a375ca1e529e3a79fe7512e | 3c4a22090975cd2d3db325425cefb990300e814d85e97abc87fe89b3721a0777 |
| `tests/test_dq01_contracts.py` | 00233e9a2cd69335617841c37cdb3382f789aabf | b15e3dd73241708b1cee9721992e230fc4764d9d657983de6cf695bd0e55a3ec |

## Executed checks

| Suite | Python | PASS | FAIL | SKIP | Deselected / NOT_RUN | Exit | Actual suite time |
|---|---|---:|---:|---:|---|---:|---:|
| DQ wire preparation | 3.10.22 | 152 | 0 | 0 | 0 | 0 | 0.76 s |
| DQ wire preparation | 3.13.18 | 152 | 0 | 0 | 0 | 0 | 0.48 s |
| Six existing PURE modules | 3.10.22 | 203 | 0 | 0 | 0 | 0 | 20.92 s |
| Six existing PURE modules | 3.13.18 | 203 | 0 | 0 | 0 | 0 | 16.49 s |
| Read-only SP subset | 3.10.22 | 65 + 110 subtests | 0 | 0 | 4 | 0 | 0.31 s |
| Read-only SP subset | 3.13.18 | 65 + 110 subtests | 0 | 0 | 4 | 0 | 0.34 s |

Six PURE modules: contracts, controller, faults, simulator, observer, no_effects
under `tests/test_offline_generation_job_*.py`. SP modules:
`tests/test_topic_to_film.py`, `tests/test_topic_to_film_v1_1.py`.
Explicitly deselected on both runtimes: `test_missing_wav`,
`test_duplicate_json_rejected`, `test_read_limit`, `test_symlink_rejected`;
they create files and are **NOT_RUN**, not PASS or SKIP. Full SP suite was not
run under this gate.

Each interpreter ran the three suites sequentially under a 60 s outer
watchdog; measured command totals 22.122 s (3.10) and 17.430 s (3.13), exits 0.
No acceptance command timeout occurred; measured testing stayed below 300 s.
An earlier wire-only 3.10 run also passed 152 tests in 0.84 s, exit 0.

Two earlier runner startup attempts were **not successful test runs**:
default pytest FD capture attempted a temporary-file open (exit 1), then
pytest logging attempted its file handler open (exit 3). An audit hook denied
each before the open completed; no DQ tests executed in either attempt.
Capture and logging were disabled, not the effect guard. Final successful
commands reported `AUDIT_BLOCKED_EVENTS []` on both runtimes.

Launch environment: `PYTHONDONTWRITEBYTECODE=1`,
`PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`, Python `-B`; pytest arguments
`-q -s -p no:cacheprovider -p no:tmpdir -p no:logging`.
The effect guard installed before `pytest.main` rejects write-mode `open`
(mode `w/a/x/+` or flags WRONLY/RDWR/CREAT/TRUNC/APPEND), SQLite connects,
subprocess.Popen, socket connect/bind, mkdir/remove/rmdir/rename/chmod/link/
symlink/system/fork/posix_spawn/kill. It does not claim native syscall
isolation: Python audit observation is not qualification of SQLite C-level
path behavior. New wire code imports neither SQLite nor OS/process/network
APIs; no native adapter was exercised.

No JUnit, pytest cache, bytecode, benchmark log, lab directory or evidence
archive was intentionally created by these test runs. Raw stdout/exit results
are in execution-tool records; this tracked report records their measured
summaries. No external test-artifact root was selected before the gate.

## Required checks not performed

| Requirement | Status / reason |
|---|---|
| Full 17 closed DTO schemas, role/index/binding validators | NOT_IMPLEMENTED; wire primitives are insufficient |
| 23 DOC.ORACLE cases (F01-P01–P03/N01–N06; F02-P01–P07/N01–N07) | NOT_RUN; neither native provenance nor complete pure semantic validators exist |
| Qualified root/profile/PRAGMA readback | BLOCKED_PRE_WRITE_GATE |
| InitializeNew/OpenExisting/P/A/R/snapshot/inspect/acknowledge | NOT_IMPLEMENTED / NOT_RUN |
| FI-01–FI-22 and P/A/R subcases | NOT_RUN / BLOCKED_PRE_WRITE_GATE |
| CW-01 invocation; CW-02 ACK; CW-03 software kill | NOT_RUN; requested/observed checkpoint NONE; no worker spawned/killed |
| CW-04 internal VFS/fsync | NOT_RUN / BLOCKED_INSTRUMENTATION |
| CW-05 power-loss | NOT_RUN / OUT_OF_SCOPE |
| SQLite durable recovery, concurrency, CAS, busy/full/security limits | NOT_RUN |
| Windows 10/11 / NTFS | WINDOWS_NOT_RUN |
| Whole-application recovery, general restore, production/live providers | OUT_OF_SCOPE / NOT_RUN |

In particular, no NOT_COMMITTED, COMMITTED, qualified absence, ProofAck,
post-R release, native custody or native security PASS was produced. Known
PURE test outcomes remain PURE-only. No contract contradiction is asserted
from the missing environment; the blocker is the explicit pre-write gate.

## Source integrity and handoff

Pinned source Markdown SHA-256 at `c15ac152258586be1ed1b57f205830edfffc9ae1`,
all under `docs/tasks/MVP_08B_4_DQ_00/`:

| File | SHA-256 |
|---|---|
| DQ_01_IMPLEMENTATION_TASK.md | 7b1f8024d1ec31b637fee1835b21c0e1d57b7b73212c08ab07aea2d5aca0b0fd |
| DURABLE_STORAGE_CONTRACT_PROPOSAL.md | 41549df1f263e0ec2579427379275d6ac600c4d151372b3106fab83fe685e7d2 |
| NATIVE_EVIDENCE_CONTRACT_PROPOSAL.md | 7fbc5094243da27116822939d0809664a544cdc77c59e7f70c7b52b617f8b7e8 |
| FAULT_INJECTION_MATRIX.md | 042741459f8ecfce56d669655ec5cf2088f5c510b8a8ea859136b0bca9ac1619 |
| SQLITE_QUALIFICATION_PROFILE.md | 7205897894369ab2d6d3d56594abf6b5731155442284e848826303b9c04efb0a |
| TEST_ROOT_SECURITY_CONTRACT.md | b629bb16e5d6ce56690bc0cc4b0c5a8fce9e8b1c8789fa3d83f440eef70d3683 |
| OWNER_APPROVAL.md | fbc2223e62ea30d2345c08659e55be3b23374714637706b81e62310ec98d489b |

All changes are new files within the allowlist. Existing G1–G6, PURE core,
SP contracts, CI and dependencies are unchanged. No SQLite DB/journal,
models, media rendering, provider calls, payments, production permissions,
main update, merge or release. No root/evidence cleanup was performed.

**STOP: BLOCKED_PRE_WRITE_GATE.** Review this partial checkpoint and the exact
root observations. Do not treat the wire preparation as a completed Stage A,
completed DQ-01, durable JobStore, approved runtime or independent acceptance.
