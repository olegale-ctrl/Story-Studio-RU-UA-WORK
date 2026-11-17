# E01.3.8.3a — Schema-2 Event Codec Without Semantic Substitution

## Reason for the change

The initial E01.3.8.3 codec temporarily represented a schema-2
`schema_migrated` event as `operation_failed` while delegating common envelope
work to the schema-1 codec. Although the final wire value was restored, that
temporary object had the wrong event meaning. E01.3.8.3a removes this semantic
substitution completely.

## Version-aware Event mapping

Schema-2 events now have a dedicated strict parser in
`editorial.versioned_codec`:

1. Every Event object is checked for the exact existing field set and common
   UUID, timestamp, refs, text, nullability, array, and scalar rules.
2. The closed schema-2 action vocabulary contains the seven existing actions
   plus `schema_migrated`.
3. `schema_migrated` constructs an immutable `Schema2Event` directly.
4. Every existing action constructs the unchanged schema-1 `Event` directly.
5. Unknown actions fail at the exact `$.events[index].action` path.
6. Event IDs remain unique and input order is retained.

The unchanged portion of a schema-2 envelope is still validated by the existing
schema-1 codec, with an empty temporary Event collection. The independently
parsed real schema-2 Event tuple is then attached to the immutable aggregate.
No event is renamed, copied under another meaning, or represented by a false
action.

Encoding follows the same separation. The existing codec serializes only the
unchanged common envelope with an empty Event collection. The version-aware
mapper writes the real Event objects and exact actions into that envelope before
canonical serialization and strict round-trip validation.

## Changed files

- `editorial/versioned_codec.py`
- `tests/test_editorial_schema2_codec.py`
- `docs/tasks/E01_3_8_3A_RESULT.md`

`editorial/codec.py`, schema-1 models, checksum, history, migration, authority,
and storage code were not changed.

## Regression coverage

The schema-2 codec suite now has 42 tests. Added coverage verifies:

- mixed existing and `schema_migrated` events preserve exact types/actions;
- multiple `schema_migrated` records round-trip at codec level without making a
  migration-policy claim;
- canonical bytes contain `schema_migrated` and no substituted
  `operation_failed`;
- unknown schema-2 actions fail with the exact action path;
- malformed migration Events fail at their exact malformed field;
- two consecutive canonical round-trips produce identical bytes.

Existing tests also continue to verify direct schema-2 `schema_migrated`
round-trip, schema-1 rejection of that action, canonical stability, strict
unknown-field rejection, and schema-1 direct/versioned codec equivalence.

## Validation

Environment: Linux, Python standard library only.

```text
python -m unittest discover -s tests -p "test_editorial*.py" -v
Ran 391 tests in 6.035s — OK

python -m compileall -q editorial tests
exit 0

git diff --check
exit 0
```

## Schema-1 compatibility

Schema 1 continues to use `decode_snapshot()` and `encode_snapshot()` directly.
Its Event action vocabulary is unchanged and still rejects `schema_migrated`.
The refactor adds no fallback for unknown actions and no schema-1 model or wire
field.

## Remaining limits

This is a codec-only correction. Multiple migration events are structurally
representable but their policy validity is not decided here. The codec still
does not migrate data, calculate or verify attestation digests, verify
signatures, evaluate identity/authority, verify schema-2 checksums, or access
files and networks. E01.3.8.4 was not started.
