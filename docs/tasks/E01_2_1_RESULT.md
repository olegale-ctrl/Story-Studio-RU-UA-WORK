# E01.2.1 — strict snapshot decoder

## Scope and baseline

Branch: `feat/editorial-e01-2-1-decoder`.
Base: `ae0bc4ecb4b2e19de0f232e593ad9d63413a6992` (E01.1b-2).
Only three files are added: `editorial/codec.py`,
`tests/test_editorial_codec.py`, and this report. Existing models, constructors,
package exports, CLI, renderer, Sprint 26 and timeline v3 are unchanged.

Contract sources: E00 final specification at commit
`e520648411b99264688ff66dc61ad0e974201ed3`, E01.1a model contract at
`a097c480bf1ffae2ee0e20a8c9b7900c00e185a0`, and the baseline
`docs/tasks/E01_1B_RESULT.md`. The accepted Q5 amendment is mandatory:
RightsReview wire records contain `subject_kind` (`source` or `asset`).

## API and mapping

```python
from editorial.codec import DecodeError, decode_snapshot

snapshot = decode_snapshot(raw_bytes)  # ContractSnapshot
```

The function accepts exactly `bytes`. It either returns the complete immutable
snapshot or raises `DecodeError`, a subclass of existing `ModelError`.
`error.violation` carries `code`, `field_path` and `message`; for example,
`MISSING_FIELD` at `$.rights_reviews[0].subject_kind`. No partial result escapes.
Codes distinguish syntax, encoding, shape, enum/reference kinds, limits and
model-local invariant failures. Existing local model checks are reused.

Nine revision collections map to existing concrete revision types in the
normative collection order. Source metadata maps to `SourceDetails`, claim
metadata to `ClaimReview`, rights metadata to `RightsDetails`; their owner refs
come directly from the corresponding wire record. Thus `subject_kind` and
`expires_at` survive without changing the old RightsReview constructor.
Events, approvals and nullable active selections are retained. Non-null active
refs become the production/candidate/script/scene_plan internal slots, in that
order. UUID reuse between different object kinds remains permitted.

No defaults are inserted for absent fields, including nullable fields. Strings
are preserved without trimming, case correction or Unicode normalization.
Dates remain canonical UTC-second strings. Array order is preserved; revision
collections must already be ordered by `(id, revision)` and unique.

`editorial/__init__.py` is deliberately unchanged: the previous lightweight
package import does not acquire a JSON import. Import the API from the codec
module explicitly. All implementation dependencies are Python standard library.

## Validation and test matrix

| Area | Checks and test coverage |
| --- | --- |
| Input and parser | bytes only; strict UTF-8; BOM rejection; Cyrillic, emoji, combining symbols and escaped Unicode; unpaired surrogate rejection; syntax/trailing input; duplicate keys including escaped names |
| Numbers | NaN, positive/negative Infinity and all floating-point tokens rejected; booleans rejected as integers |
| Envelope | schema version exactly integer 1; every required root key; no extra keys; arrays and active refs have exact shapes |
| Records | every field required, including nullable fields; unknown fields rejected in all collections and nested records; closed enums and vocabularies; canonical UUIDs and lowercase hashes |
| Dates and local invariants | actual calendar validity and UTC seconds; numeric bounds; nullable pairs; unique nested IDs; frozen tuples and model-local constraints |
| Rights and companions | mandatory subject_kind; only source/asset; complete source/claim/rights metadata; lossless companion mapping |
| References | kind matches each typed field/collection/active slot; unknown graph targets remain permitted |
| Ordering | reject unsorted or duplicate revisions; reject duplicate approval/event IDs; preserve events and approvals order |
| Limits | 32 MiB input; container depth 64; strings 100000 code points; arrays 10000; combined revisions 10000; segments/scenes 1000 (shared bounded-array parser, explicit segment test) |
| Sources and assets | lexical URL/local path checks; existing pure model path validator reused; no file existence checks or requests |
| Isolation | fresh-process audit hook blocks file access during decode and network/process operations; immutable result; unchanged source fixture; late invalid records produce exceptions |
| Checksum | lowercase 64-hex shape only; deliberately arbitrary well-formed checksum accepted |

Depth is checked before recursive JSON parsing; raw size is checked before UTF-8
decoding. Other limits are enforced during structural validation after parsing.
This is a bounded-input decoder, not a streaming parser.

## Actual verification

Environment: Linux, Python 3.12.14, existing `.venv`; no dependency installation.

```sh
.venv/bin/python -m unittest discover -s tests -p 'test_editorial_*.py' -q
```

Result: **99 tests passed**, 1.735 seconds. This comprises 35 decoder tests and
the existing 64 E01.1/E01.1b model tests. Tests use synthetic inline data and
require no external files, services, LLMs, paid APIs or credentials.
Windows execution and the unrelated renderer/TTS suite were not run.

## Compatibility, findings and remaining work

No blocking contract conflict was found. The existing E01.1b model and public
constructors are unchanged; all previous editorial tests pass. Q5 does not
require global UUID uniqueness. Rights expiry versus review time remains a
cross-object check deferred by the existing model boundary. The decoder only
checks each date's wire form; it does not consult a clock.

No graph resolution, dependency digest, hashing, checksum verification, factual
validation, approval authority, storage, CLI workflow, merge or release is
implemented. Validly shaped unresolved references are intentionally accepted.

E01.2.2 still needs the separately authorized encoder: exact reverse mapping of
all fields and companions, explicit nulls, enum/date representation and ordering,
plus round-trip tests and rejection of incomplete internal snapshots that cannot
produce the full wire contract. Canonical serialization/hashing and E01.3
integrity checks remain separate work. E01.2.2 has not been started.
