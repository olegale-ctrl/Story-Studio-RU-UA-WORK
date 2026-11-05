# E01.3.6.2 — Integrated editorial snapshot integrity validation

## Result

Implemented a read-only integration layer on branch
`feat/editorial-e01-3-6-2-integrity-validation`, based exactly on
`2a3336a9a244ea9447ea014669e75fbbb7d99c77`.

The implementation composes the existing checksum, graph, revision hash,
rights binding, current package, and dependency digest operations. None of
their algorithms was copied or changed.

## Public API

`editorial.snapshot_integrity` exports:

- `validate_snapshot_integrity(snapshot) -> SnapshotIntegrityResult`;
- `validate_current_snapshot_integrity(snapshot, gate, policy_version) -> CurrentSnapshotIntegrityResult`;
- frozen `SnapshotIntegrityResult`;
- frozen `CurrentSnapshotIntegrityResult`;
- `SnapshotIntegrityError` for integration-boundary input errors.

`SnapshotIntegrityResult` contains only:

- `checksum_verified`;
- `revision_count`;
- `binding_count`;
- `material_bindings` as the existing structured `RightsBindingResult` tuple.

`CurrentSnapshotIntegrityResult` contains the full snapshot result, the existing
`CurrentPackage`, and the canonical current dependency digest. Neither result
contains approval, readiness, commercial-use, render, or export decisions.

## Deterministic validation order

For a valid `ContractSnapshot` input, failure priority is:

1. `verify_snapshot_checksum(snapshot)`;
2. `validate_reference_graph(snapshot)`;
3. `verify_revision_content_hash(revision, companion)` for every revision in
   contract collection order, including unreferenced history;
4. `validate_all_rights_bindings(snapshot, graph)` for every Source/Asset;
5. return the immutable full-snapshot result.

The current operation first performs all five full-snapshot steps, then calls
`build_current_package(snapshot, gate)`, then calls
`compute_current_dependency_digest(snapshot, gate, policy_version)`.
No caller-supplied prevalidated package or boolean bypass is accepted.

Existing exception types and violation codes propagate. Full-history revision
hash failures remain `HashVerificationError`; the integration layer reattaches
their exact wire collection path, such as
`$.sources[1].ref.content_hash`. A malformed companion owner cannot have a
canonical checksum because `encode_snapshot` rejects it first with the existing
`EncodeError`, `COMPANION_OWNER`, and exact wire path.

## Failure modes covered

- snapshot checksum mismatch, including generation/approval/event changes;
- missing, wrong-revision, wrong-hash, active, approval, and event graph refs;
- invalid content hashes in active and unreferenced historical revisions;
- companion metadata inconsistent with its supplied revision hash;
- malformed companion ownership rejected during canonical checksum encoding;
- Source and Asset material digest mismatches;
- missing current active selections and incoherent active chains;
- missing or incoherent scene plans for SCENES/HANDOFF.

`MaterialBindingState.UNCONFIRMED` remains a valid structural draft result. It is
not converted into permission or readiness. SCRIPT does not require an active
scene plan and its digest remains independent of a separately selected
downstream scene plan.

## Tests

Targeted command:

```text
.venv/bin/python -m unittest discover -s tests -p 'test_editorial_snapshot_integrity.py' -q
```

Result: 27 tests passed in 1.750 seconds; 0 failures and 0 errors.

Required full regression command:

```text
.venv/bin/python -m unittest discover -s tests -p 'test_editorial_*.py' -q
```

Result: 244 tests passed in 6.942 seconds; 0 failures and 0 errors. This includes
all 217 tests present at the task baseline.

Required static checks:

```text
git diff --check
python -m compileall -q editorial tests
```

Both commands completed successfully with no output. Tests ran in the supplied
Linux cloud environment; no Windows compatibility claim is made from them.

## Changed files

- `editorial/snapshot_integrity.py`;
- `tests/test_editorial_snapshot_integrity.py`;
- `docs/tasks/E01_3_6_2_RESULT.md`.

Existing E01 modules, timeline v3, Sprint 26, renderer, CLI, GUI, FFmpeg, and TTS
files were not changed.

## Security and scope boundary

Successful validation establishes structural and cryptographic consistency of
the stored data relative to its supplied checksum and hashes. It does not prove
reviewer identity, factual truth, source authenticity, copyright ownership,
approval validity, absence of revocation, rights-policy compliance, production
readiness, or permission for commercial distribution. It does not authorize
render or export.

No persistence, atomic save, generation increment, lock, backup/recovery,
approval authority, rights policy/expiry decision, handoff manifest, or
readiness mechanism was added. No later stage was started.
