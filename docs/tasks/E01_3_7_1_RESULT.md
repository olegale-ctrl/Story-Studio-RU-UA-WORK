# E01.3.7.1 — ApprovalRecord dependency consistency and staleness

## Result

Implemented a pure stored-approval consistency evaluator on branch
`feat/editorial-e01-3-7-1-approval-consistency`, based exactly on
`ab9c1590b4c3bd7ff8e7c266d8efdaf9361ef47c`.

The evaluator accepts only an approval ID and reads the corresponding
`ApprovalRecord` from the supplied snapshot. It does not accept an external
record or an externally asserted integrity flag.

## Public API

`editorial.approval_consistency` exports:

- `evaluate_approval_consistency(snapshot, approval_id, gate, policy_version)`;
- `evaluate_all_approval_consistency(snapshot, gate, policy_version)`;
- frozen `ApprovalConsistencyResult`;
- `ApprovalConsistencyReason`;
- `ApprovalConsistencyError` for lookup/input failures.

Every operation first calls the existing
`validate_current_snapshot_integrity(snapshot, gate, policy_version)`. The
single-record operation then finds the ID inside `snapshot.base.approvals`. The
bulk operation evaluates every stored record in snapshot order after one full
current-integrity call and one current digest computation.

## Exact consistency semantics

A result is dependency-consistent only when all four comparisons succeed after
full current-snapshot integrity validation:

1. stored `approval.gate` equals the requested canonical gate;
2. stored `approval.policy_version` equals the supplied string literally;
3. the full stored `approval.object_ref`, including `content_hash`, equals the
   exact current package root;
4. stored `approval.dependency_digest` equals the computed current digest.

All mismatches are retained in this fixed order:

1. `GATE_MISMATCH`;
2. `POLICY_VERSION_MISMATCH`;
3. `TARGET_REF_MISMATCH`;
4. `DEPENDENCY_DIGEST_MISMATCH`.

Historical staleness is returned as data, not raised as snapshot corruption.
Checksum, graph, revision-hash, rights-binding, current-chain, package, and
digest failures continue to propagate through their existing structured
exceptions before a consistency result can be produced.

The result preserves the stored `ApprovalDecision` for `approve`, `reject`,
`revise`, and `revoke`. It deliberately has no `approved`, `ready`, authority,
rights grant, render, or export field. All decisions use the same dependency
comparison.

## Covered behavior

- exact SCRIPT, SCENES, and editorial HANDOFF matches;
- each individual mismatch and all mismatches together in fixed order;
- new current ScriptRevision and ScenePlanRevision;
- referenced Source, Claim, GenreProfile, RightsReview, and Asset revisions;
- unreferenced historical revisions outside package closure;
- SCRIPT independence from a downstream active scene plan;
- explicit return to a previous coherent exact chain;
- all four decisions without filtering or precedence;
- empty collections, unknown approval IDs, and snapshot-order bulk results;
- checksum, graph, unreferenced content-hash, and active-chain failures;
- literal Unicode policy versions without normalization;
- immutability and absence of file, network, and subprocess side effects.

## Verification

Targeted command:

```text
.venv/bin/python -m unittest discover -s tests -p 'test_editorial_approval_consistency.py' -q
```

Result: 29 tests passed in 1.786 seconds; 0 failures and 0 errors.

Required full regression:

```text
.venv/bin/python -m unittest discover -s tests -p 'test_editorial_*.py' -q
```

Result: 273 tests passed in 9.449 seconds; 0 failures and 0 errors. This includes
all 244 tests present at the task baseline.

Static checks:

```text
git diff --check
python -m compileall -q editorial tests
```

Both completed successfully with no output. Tests ran in the supplied Linux
cloud environment; no Windows compatibility claim is made from them.

## Changed files

- `editorial/approval_consistency.py`;
- `tests/test_editorial_approval_consistency.py`;
- `docs/tasks/E01_3_7_1_RESULT.md`.

Existing model, integrity, package, digest, current-package, persistence,
Sprint 26, timeline v3, render, CLI, and GUI files were not changed.

## Open questions and scope boundary

No contract ambiguity blocked this stage. Decision-history precedence, actor
authority, identity verification, revocation effect, idempotent commands,
review declarations, rights policy/expiry, material-fact coverage, gate order,
and readiness remain separate future work.

A dependency-consistent `APPROVE` is only a matching historical record. It does
not authorize production, render, export, or commercial use. No later stage was
started.
