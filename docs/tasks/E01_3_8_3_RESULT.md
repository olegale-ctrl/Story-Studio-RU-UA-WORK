# E01.3.8.3 — Strict Versioned Editorial Codec

## Result

E01.3.8.3 adds strict version dispatch and a schema-2 JSON codec while retaining
the existing schema-1 codec and public behavior unchanged. The implementation
does not migrate data, calculate or verify digests/checksums, evaluate authority,
or perform storage or network operations.

## Public API and dispatch

`editorial.versioned_codec` exports:

- `decode_editorial_versioned(data: bytes) -> ContractSnapshot | Schema2Snapshot`
- `encode_editorial_versioned(snapshot: ContractSnapshot | Schema2Snapshot) -> bytes`

The decoder parses the strict root once to obtain the required integer
`editorial_schema_version`:

- version 1 delegates to the existing `decode_snapshot()` without changing its
  behavior;
- version 2 uses the new schema-2 path;
- absent, non-integer, boolean, floating, string, and unsupported versions are
  rejected with structured paths;
- no version is inferred and no migration occurs.

The versioned encoder delegates an exact `ContractSnapshot` to the existing
`encode_snapshot()`. A `Schema2Snapshot` is encoded as the approved flat root
envelope. The internal `base_snapshot` name never appears on wire.

## Schema-2 mapping

Schema 2 retains every schema-1 root field and requires the additional
`approval_authority_evidence` array, including when it is empty. Each evidence
object requires all fourteen approved fields. JSON declaration arrays become
immutable tuples; nullable values remain null; UUIDs, Unicode, timestamps,
array order, and the supplied `snapshot_checksum` are retained exactly.

Canonical output uses UTF-8 and:

```python
json.dumps(
    envelope,
    ensure_ascii=False,
    sort_keys=True,
    separators=(',', ':'),
    allow_nan=False,
)
```

Output is passed through the strict versioned decoder and must round-trip to the
same immutable model before bytes are returned.

## Event compatibility

`Schema2Event` represents only the new schema-2 action `schema_migrated`.
Existing actions continue to use the unchanged schema-1 `Event`. The schema-2
codec accepts and round-trips both. The schema-1 codec still rejects
`schema_migrated`; its event vocabulary was not weakened.

## Strict parsing and diagnostics

The versioned codec reuses the established parser limits and diagnostics:

- 32 MiB input and nesting depth 64;
- strict UTF-8 with no BOM;
- duplicate-key detection before object conversion;
- no floats, NaN, or Infinity;
- no surrogate code points or Unicode normalization;
- array and text limits;
- complete required-field and unknown-field checks;
- strict scalar types with no coercion;
- exact evidence formats, declaration order, linkage, uniqueness, and order.

Errors remain `DecodeError`/`EncodeError` with immutable `Violation` values and
JSON-style field paths. Evidence model failures preserve their distinct local
codes, including principal, declaration, signature, duplicate, and ordering
failures. Structurally valid evidence makes no authenticated-identity or
effective-authority claim.

## Files

- `editorial/versioned_codec.py` — version dispatch and schema-2 codec.
- `editorial/schema2_model.py` — schema-2-only migration Event type.
- `tests/test_editorial_schema2_codec.py` — 36 strict codec tests.
- `docs/tasks/E01_3_8_3_RESULT.md` — this report.

The existing `editorial/codec.py`, schema-1 models, constructors, checksum,
dependency, consistency, history, and CLI modules were not changed.

## Compatibility

- Existing schema-1 fixtures still use the original codec unchanged.
- Versioned schema-1 decode equals direct `decode_snapshot()`.
- Versioned schema-1 encode equals direct `encode_snapshot()`.
- Schema 2 cannot fall through to schema 1 or silently discard evidence.
- Legacy ApprovalRecords without evidence remain representable in schema 2.
- Existing `snapshot_checksum` values are preserved and are not recomputed.

## Validation

Environment: Linux, Python standard library only.

```text
python -m unittest discover -s tests -p "test_editorial*.py" -v
Ran 385 tests in 5.846s — OK

python -m compileall -q editorial tests
exit 0

git diff --check
exit 0
```

The 385-test total includes 36 new schema-2 codec tests and the 45 schema-2
model tests from E01.3.8.2.

## Known limits and E01.3.8.4

The codec checks only structure and local invariants. It intentionally does not
recompute `attestation_digest`, verify Ed25519 signatures or identity, evaluate
authority or policy, verify the schema-2 snapshot checksum, establish trusted
history, migrate schema 1, or access storage. E01.3.8.4 remains responsible for
the next separately approved integrity work.
