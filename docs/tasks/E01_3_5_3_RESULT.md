# E01.3.5.3 — Current package and active refs coherence

## Result

Implemented the current-package layer on branch
`feat/editorial-e01-3-5-3-current-package`, based on
`ac98f3e2a7ef7d386bea229dd22c828793e236ab`.

The implementation adds two public module-level operations:

- `build_current_package(snapshot, gate) -> CurrentPackage`;
- `compute_current_dependency_digest(snapshot, gate, policy_version) -> str`.

`CurrentPackage` is immutable and records the parsed gate, the exact active root,
the validated `HistoricalPackage`, and successful coherence verification. It
does not represent approval, rights clearance, readiness, or a media manifest.
HANDOFF remains an editorial dependency package.

## Selection and coherence rules

The current builder resolves exact active references from the snapshot. It does
not select the greatest revision number and does not replace a missing active
selection with a historical revision.

- SCRIPT requires active production, candidate, and script references. The
  script must refer exactly to the selected production and candidate. Its root
  is the active script.
- SCENES and HANDOFF additionally require an active scene plan. The scene plan
  must refer exactly to the active script. Their root is the active scene plan.
- A null or separately selected incoherent scene plan has no effect on SCRIPT.

Every required active reference must resolve by `(kind, id, revision)` and its
supplied `content_hash` must equal the exact stored reference. Failures are
reported as `CurrentPackageError` with a stable code and exact JSON field path.
Covered failure classes include missing active selections, absent or wrong-kind
targets, hash mismatches, production/candidate/script coherence mismatches, an
invalid gate, and failures returned by the historical package validator.

After active-chain checks, `build_current_package` delegates full package and
revision integrity validation to `build_historical_package`. The current digest
operation then delegates canonical payload construction and SHA-256 computation
to `compute_dependency_digest`. No second digest implementation was introduced.

## Contract erratum

`E01_3_5_3_CONTRACT_ERRATA.md` records that the canonical dependency payload has
seven top-level keys. This corrects only the earlier prose count. The payload,
canonical bytes, golden vectors, and historical documents remain unchanged.

## Changed files

- `editorial/current_package.py` — current selection, coherence validation, and
  delegation APIs;
- `tests/test_editorial_current_package.py` — positive, negative, equivalence,
  immutability, and side-effect tests;
- `docs/tasks/E01_3_5_3_CONTRACT_ERRATA.md` — seven-key terminology correction;
- `docs/tasks/E01_3_5_3_RESULT.md` — this report.

Existing model, codec, graph, rights binding, historical package, dependency
digest, Sprint 26, and FFmpeg pipeline files were not changed.

## Verification

Targeted command:

```text
.venv/bin/python -m unittest discover -s tests -p 'test_editorial_current_package.py' -v
```

Result: 16 test methods passed, including parameterized/subtest coverage of more
than 18 required scenarios; 0 failures and 0 errors.

Complete regression command:

```text
.venv/bin/python -m unittest discover -s tests -p 'test_editorial_*.py' -q
```

Result: 202 tests passed in 5.529 seconds; 0 failures and 0 errors. This includes
all 186 tests that existed at the task baseline. `git diff --check` and Python
bytecode compilation of the new implementation and tests also passed.

## Scope boundary

This task does not add approval authority, rights policy decisions, production
readiness, a frozen handoff manifest, snapshot persistence, or any new checksum
or hashing algorithm. No follow-up E01 task was started.
