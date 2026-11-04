# E01.3.6.1 — Canonical snapshot checksum

## Result

Implemented the canonical full-snapshot checksum on branch
`feat/editorial-e01-3-6-1-snapshot-checksum`, based on
`fac192088a62d5fe1f56b88df17407a979bdedb2`.

The public module API is:

- `canonical_snapshot_bytes(snapshot) -> bytes`;
- `compute_snapshot_checksum(snapshot) -> str`;
- `verify_snapshot_checksum(snapshot) -> None`;
- `SnapshotChecksumError` with `ModelError`/`Violation` diagnostics.

## Canonical form

`canonical_snapshot_bytes` obtains the normative complete wire representation
from the existing `encode_snapshot(snapshot)`. It parses those UTF-8 JSON bytes,
removes only the root `snapshot_checksum` member, and serializes the remaining
object with:

```python
json.dumps(
    payload,
    ensure_ascii=False,
    sort_keys=True,
    separators=(',', ':'),
    allow_nan=False,
).encode('utf-8')
```

Array order and Unicode code points are preserved. No normalization, revision
filtering, timestamp filtering, generation change, or implicit sorting of
arrays is performed. SHA-256 is returned as 64 lowercase hexadecimal digits.

`verify_snapshot_checksum` compares the computed digest with the stored value.
A mismatch raises `SnapshotChecksumError` with code
`SNAPSHOT_CHECKSUM_MISMATCH` and path `$.snapshot_checksum`.

## Golden vector

The tests contain literal expected canonical bytes for a valid empty schema-1
snapshot. Their literal expected SHA-256 is:

```text
bdf122857990d12c1a64f433c8e5165132ccf660cc92cf05eca226233312f214
```

Neither expected value is computed through the production checksum helper.

## Coverage

Targeted tests cover:

- literal golden canonical bytes and SHA-256;
- repeatability and JSON object-key order independence;
- changes to generation, approval decisions, events, and active refs;
- all represented audit timestamp categories;
- source, claim, and rights companion metadata;
- revision contents;
- exclusion of only the stored checksum field;
- successful and failed verification;
- exact RU/UK, emoji, and combining-character preservation;
- snapshot immutability and absence of file/network side effects.

Targeted command:

```text
.venv/bin/python -m unittest discover -s tests -p 'test_editorial_snapshot_checksum.py' -v
```

Result: 15 test methods passed in 0.219 seconds; 0 failures and 0 errors.

Complete regression command:

```text
.venv/bin/python -m unittest discover -s tests -p 'test_editorial_*.py' -q
```

Result: 217 tests passed in 5.724 seconds; 0 failures and 0 errors. This includes
all 202 tests present at the task baseline. `git diff --check` and bytecode
compilation of the new implementation and tests also passed.

## Changed files

- `editorial/snapshot_checksum.py`;
- `tests/test_editorial_snapshot_checksum.py`;
- `docs/tasks/E01_3_6_1_RESULT.md`.

The model, codec, revision hashing, graph, rights binding, package builders,
dependency digest, Sprint 26, and media pipeline were not changed.

## Security and scope boundary

Successful checksum verification establishes only equality between the full
canonical serialized state and its stored checksum. It does not verify revision
content hashes, the dependency graph, rights binding, approvals, policy,
readiness, or provenance. It is not a digital signature and cannot detect an
attacker who can modify both the snapshot data and the stored checksum.

No persistence, atomic save, generation increment, lock, recovery, approval
authority, rights policy, handoff manifest, CLI, GUI, FFmpeg, or TTS work was
introduced. E01.3.6.2 was not started.
