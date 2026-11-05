# E01.3.7.2 — Approval decision history and revocation projection

## Result

Implemented a deterministic, read-only projection of stored approval decisions
on branch `feat/editorial-e01-3-7-2-decision-history`, based exactly on
`c9341e9aa78b8bae0de83687abfcadbd010b31de`.

The projection reads only `ApprovalRecord` values contained in a fully validated
snapshot. It does not accept external history, create records, alter decisions,
or trust a caller-provided integrity flag.

## Public API

`editorial.approval_history` exports:

- `evaluate_approval_history(snapshot, gate, policy_version, target_ref, dependency_digest)`;
- `evaluate_current_approval_history(snapshot, gate, policy_version)`;
- frozen `ApprovalDecisionKey`;
- frozen `ApprovalHistoryResult`;
- `ApprovalHistoryState`;
- `ApprovalHistoryDiagnostic`;
- `ApprovalHistoryError` for invalid historical key inputs.

Historical evaluation calls `validate_snapshot_integrity(snapshot)` and uses the
exact supplied key without consulting active refs or selecting a latest
revision. Current evaluation calls `validate_current_snapshot_integrity`, then
uses the existing bulk approval-consistency API to admit only records matching
the exact current package.

## Exact decision key

The grouping key contains all four values:

1. exact gate;
2. literal `policy_version`;
3. full exact `RevisionRef`, including `content_hash`;
4. exact `dependency_digest`.

Records are not grouped by UUID alone or digest alone. Records for another gate,
policy, revision/hash, or digest remain independent history.

## Chronology and ambiguity

The projection takes the maximum normative UTC `ApprovalRecord.timestamp`.
Snapshot array order and record UUIDs do not break timestamp ties.

- One record at the latest timestamp is selected as `latest_record`; its state
  is `RECORDED_APPROVE`, `RECORDED_REJECT`, `RECORDED_REVISE`, or
  `RECORDED_REVOKE`.
- Different decisions at the same latest timestamp produce
  `AMBIGUOUS_HISTORY` with
  `CONFLICTING_DECISIONS_SAME_TIMESTAMP`.
- Equal decisions at the same latest timestamp are safely collapsed to their
  recorded state only when actor, reason, and review declarations are also
  identical. No record is selected, and
  `EQUIVALENT_DECISIONS_SAME_TIMESTAMP` documents the duplicate projection.
- Equal decisions with different actor/reason/declarations produce
  `AMBIGUOUS_HISTORY` with
  `NON_EQUIVALENT_RECORDS_SAME_TIMESTAMP`.
- No records for the exact key produce `NO_DECISION`.

All matching record IDs remain in snapshot order for diagnostics. Older APPROVE
does not override newer REVOKE/REJECT/REVISE. A newer recorded APPROVE after a
REVOKE becomes the last recorded state, but the projection does not claim that
new human review or authority was established.

## Verification

Targeted command:

```text
.venv/bin/python -m unittest discover -s tests -p 'test_editorial_approval_history.py' -q
```

Result: 31 tests passed in 1.246 seconds; 0 failures and 0 errors.

Required full regression:

```text
.venv/bin/python -m unittest discover -s tests -p 'test_editorial_*.py' -q
```

Result: 304 tests passed in 8.986 seconds; 0 failures and 0 errors. This includes
all 273 tests present at the task baseline.

Static checks:

```text
git diff --check
python -m compileall -q editorial tests
```

Both completed successfully with no output. Tests ran in the supplied Linux
cloud environment; no Windows compatibility claim is made from them.

## Covered scenarios

The tests cover no-decision state; every single decision; approve followed by
revoke/reject/revise; approve after revoke; repeated decisions; out-of-order
arrays; all timestamp tie cases; exact policy/target/digest/gate isolation;
historical evaluation after active switching; return to a revoked coherent
chain; current SCRIPT/SCENES/HANDOFF; checksum, graph, and current-chain
failures; Unicode metadata; deterministic calls; immutability; and absence of
file, network, and subprocess side effects.

## Changed files

- `editorial/approval_history.py`;
- `tests/test_editorial_approval_history.py`;
- `docs/tasks/E01_3_7_2_RESULT.md`.

Existing model, consistency, integrity, package, digest, storage, Sprint 26,
timeline v3, CLI, GUI, FFmpeg, and TTS files were not changed.

## Limitations and open contract decisions

`ApprovalRecord` cannot prove actor identity, authority, or that a newer APPROVE
after REVOKE followed a required new human review. The projection therefore
reports only recorded history. Reviewer identity verification, authority,
review-declaration policy, rights/expiry policy, material-fact coverage, gate
ordering, readiness, and commands that create decisions require separate
contracts and were not implemented.

No state authorizes render, export, production, or commercial use. No later
stage was started.
