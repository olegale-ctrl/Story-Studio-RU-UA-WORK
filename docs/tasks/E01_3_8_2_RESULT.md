# E01.3.8.2 — Immutable Schema-2 Models and Local Invariants

## Result

E01.3.8.2 adds isolated immutable schema-2 models based on
`E01_3_8_1_APPROVED_CONTRACT.md`. Existing schema-1 models, constructors, codec,
integrity services, and CLI behavior are unchanged.

## Changes

### Public types and values in `editorial.schema2_model`

- `ApprovalAuthorityEvidence`: a frozen dataclass with all fourteen approved
  fields required by its constructor, including nullable signature and
  reconsideration fields.
- `Schema2Snapshot`: a frozen temporary in-memory aggregate containing an
  existing schema-1 `ContractSnapshot`, an immutable evidence tuple, and the
  explicit model version `editorial_schema_version=2`.
- `Schema2ModelError`: a `ModelError` subtype carrying the existing immutable
  `Violation` structure with schema-2-specific error codes and field paths.
- `required_declaration_codes(gate, decision)`: a pure lookup for the exact
  closed declaration sequence.
- Immutable declaration tuples for SCRIPT APPROVE, SCENES APPROVE, editorial
  HANDOFF APPROVE, and all non-APPROVE decisions.

`Schema2Snapshot.base_snapshot` is only a temporary container for shared domain
data. Its nested schema-1 envelope remains version 1 and is not represented as
a schema-2 wire envelope. The future schema-2 codec must produce the approved
flat JSON shape.

## Local invariants

`ApprovalAuthorityEvidence` validates:

- canonical lowercase UUIDs;
- exact Windows SID and POSIX UID/machine principal grammars;
- nonempty display name (maximum 256 code points) and policy version (maximum
  128 code points), with surrogate code points rejected and no normalization;
- an immutable nonempty declaration tuple of at most 16 known, unique codes;
- a valid exact UTC-seconds timestamp;
- lowercase SHA-256 shape;
- an all-null or all-present signature triple;
- exact `ed25519`, canonical unpadded base64url encoding of 64 bytes, and the
  approved signing-key identifier grammar;
- no direct self-reference in `reconsiders_record_id`.

`Schema2Snapshot` validates:

- exact aggregate and tuple member types and schema version 2;
- the 10,000-item evidence limit and evidence count not exceeding approvals;
- unique approval, review-session, and request IDs;
- linkage to an existing ApprovalRecord;
- exact declaration sequence for the linked ApprovalRecord gate and decision;
- evidence order matching ApprovalRecord order while allowing legacy records
  without evidence.

Legacy ApprovalRecords are retained without fabricated evidence. Model
construction makes no authority or authentication claim.

## Deliberately excluded

This task does not implement schema-2 JSON decoding/encoding, attestation digest
calculation or verification, snapshot checksum changes, reconsideration-history
integrity, graph/dependency/current-package validation, signature trust,
authority evaluation, policy lookup, schema migration, storage, clock access,
or file/network operations. Those responsibilities remain separate from local
value construction.

## Validation

Environment: Linux, Python standard library only. The implementation makes no
claim that native Windows execution was tested; Windows principal syntax was
covered with platform-independent unit tests.

Commands and results:

```text
python -m unittest discover -s tests -p "test_editorial*.py" -v
Ran 349 tests in 5.780s — OK

python -m compileall -q editorial tests
exit 0

git diff --check
exit 0
```

The 349 tests include 45 new schema-2 model tests covering the required success,
failure, immutability, legacy, ordering, size, import-side-effect, and I/O cases.

## Compatibility and limitations

- No existing source file or schema-1 constructor was modified.
- Existing schema-1 codec and all prior editorial tests continue to pass.
- Signature validation is syntactic only; no cryptographic or trust decision is
  made.
- Exact declaration matching is checked by the aggregate where the linked
  ApprovalRecord is available. Attestation digest integrity and reconsideration
  semantics require the later integrity layer.

## Next dependency

E01.3.8.3 may add the separately authorized strict schema-2 codec. This task
does not begin codec or migration work.

## Files

- `editorial/schema2_model.py`
- `tests/test_editorial_schema2_model.py`
- `docs/tasks/E01_3_8_2_RESULT.md`
