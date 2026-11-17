# E01.2.2 — deterministic JSON encoder

## Scope and baseline

Branch: `feat/editorial-e01-2-2-encoder`.
Base: `9923856b1c2e06d0b5da276b579e23b7c68ec36a` (accepted E01.2.1).

Changed files:

- `editorial/codec.py` — encoder and structured encode diagnostics;
- `tests/test_editorial_encoder.py` — focused round-trip and rejection tests;
- `docs/tasks/E01_2_2_RESULT.md` — this report.

The E01.1b model, package exports, decoder contract, Sprint 26, timeline v3,
CLI and renderer are unchanged. No dependency was added. E01.3 was not started.

## Public API

```python
from editorial.codec import EncodeError, decode_snapshot, encode_snapshot

raw: bytes = encode_snapshot(snapshot)
restored = decode_snapshot(raw)
assert restored == snapshot
```

`encode_snapshot(snapshot: ContractSnapshot) -> bytes` maps all nine concrete
revision collections to the E00 envelope. SourceRevision is joined with exactly
one SourceDetails, ClaimRevision with exactly one ClaimReview, and RightsReview
with exactly one RightsDetails. Rights records always contain the Q5
`subject_kind` and nullable `expires_at` fields. All other nullable fields are
also emitted explicitly.

The encoder maps enum instances to their normative string values and preserves
texts, supplied hashes, UUIDs, timestamps, array order and active-selection
slots. It retains `snapshot_checksum` exactly as supplied; it neither computes
nor verifies a checksum.

Serialization is fixed to UTF-8 without BOM, `ensure_ascii=False`,
`sort_keys=True`, `separators=(',', ':')`, and `allow_nan=False`. Semantically
significant arrays are not sorted. Revision collections must already use the
contract kind/id/revision order.

`EncodeError` extends the existing `ModelError` and carries the usual immutable
`Violation(code, field_path, message)`. The encoder first builds and validates a
complete in-memory envelope, then returns bytes. Invalid inputs never produce a
partial result.

## Validation performed before returning bytes

| Area | Encoder behavior |
| --- | --- |
| Aggregate type | Requires an exact `ContractSnapshot` |
| Revision payloads | Requires supported concrete types and normative collection/id/revision order; rejects duplicates |
| Companions | Requires exactly one per source/claim/rights revision, matching full owner ref and collection position; rejects missing, extra, duplicate or mismatched metadata |
| Wire values | Uses the strict E01.2.1 decoder to validate all required fields, reference kinds, closed vocabularies, dates, UUIDs, hashes, limits and nullability |
| Losslessness | Compares the decoded result with the original snapshot and rejects any non-reversible internal representation |
| Checksum | Validates wire shape through the decoder; preserves the supplied value and performs no computation |
| Side effects | Uses only in-memory conversion; no filesystem, network or process access |

This reuse of the strict decoder keeps encoder acceptance identical to the
approved wire contract. A decoder violation is re-exposed as `EncodeError` with
the same exact JSON field path and an encoder-stable `INVALID_VALUE` code.

## Round-trip examples covered

- Full snapshot with one value from each of the nine collections.
- RU/UK Cyrillic text, emoji and a combining character, including leading and
  trailing spaces inside a script segment.
- Source, claim and rights companion metadata, including explicit nulls and
  Q5 `subject_kind`.
- Multiple approvals, events, script segments and scenes, whose input order is
  preserved.
- `decode_snapshot(encode_snapshot(snapshot)) == snapshot`.
- `decode -> encode -> decode` from normative JSON.
- Arbitrary well-formed supplied checksum (`'0' * 64`) retained unchanged.
- Equivalent JSON with different object-key order encoded to identical bytes.

## Test matrix and actual result

| Test group | Coverage |
| --- | --- |
| Complete mapping | All revision types, refs, asset data, companions, approvals, events and active refs |
| Determinism | Repeated encoding, reordered source JSON keys, exact compact sorted-key JSON rules |
| Preservation | Unicode, whitespace, nulls, metadata, hashes, revision numbers and meaningful array order |
| Strict rejection | Missing/extra/mismatched companions, absent rights details/subject kind, weak legacy vocabulary values, unsupported payloads and invalid internal revision order |
| Isolation | Fresh-process audit hook rejects file, network and process activity during decode/encode round-trip |
| Regression | All E01.2.1 and E01.1/E01.1b editorial tests |

Environment: Linux, Python 3.12.14, existing `.venv`; no installations or
external services.

```sh
.venv/bin/python -m unittest discover -s tests -p 'test_editorial_*.py' -q
```

Result: **112 tests passed in 1.940 seconds**. This consists of 13 new encoder
tests plus the previous 99 editorial tests.

## Findings and compatibility

No E00/model contradiction and no decoder reversibility defect were found.
Consequently the approved decoder logic was not altered. Its module now also
exports the encoder symbols, while `editorial/__init__.py` remains unchanged to
preserve the established lightweight package import. Existing imports from
`editorial.codec` continue to work.

The current model deliberately permits construction of some legacy payloads
whose string fields are only nonempty. The encoder does not repair those values:
for example, an unsupported production `intended_use` or approval `gate` is
rejected at its normative wire path. Missing companion metadata is likewise not
inferred or fabricated.

## Remaining E01.3 work

E01.3 still owns reference-graph and cross-object integrity: resolving targets,
dependency relationships and any approved digest/checksum semantics. Canonical
content hashing, checksum calculation/verification, dependency digest,
approval authority, persistence, atomic save/locks/recovery and CLI workflow
remain unimplemented. No E01.3 code or tests were added in this task.
