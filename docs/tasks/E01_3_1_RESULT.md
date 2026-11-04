# E01.3.1 — canonical revision hashes

## Scope and baseline

Branch: `feat/editorial-e01-3-1-hashes`.
Base: `d020c638475f671b9c8fe8ce61e0e7da06399cda` (accepted E01.2.2).

The owner-approved schema-1 clarification is recorded in
`docs/tasks/E01_3_1_HASH_CONTRACT.md`; E00 itself was not silently changed.
Implementation is isolated in `editorial/integrity.py`, with focused tests in
`tests/test_editorial_hashes.py`. Codec, models, Sprint 26 and schema v3 are
unchanged. Only Python standard-library `json` and `hashlib` are used.

## API

```python
from editorial.integrity import (
    HashVerificationError,
    canonical_revision_bytes,
    compute_revision_content_hash,
    verify_revision_content_hash,
)

payload_bytes = canonical_revision_bytes(revision, companion=None)
digest = compute_revision_content_hash(revision, companion=None)
verify_revision_content_hash(revision, companion=None)  # None or exception
```

SourceRevision requires its exact SourceDetails, ClaimRevision its ClaimReview,
and RightsReview its RightsDetails. Missing, wrong-type, unexpected or
owner-mismatched companions raise structured `HashVerificationError`. No
snapshot lookup or graph traversal occurs.

`verify_revision_content_hash` compares the supplied lowercase hash with a fresh
SHA-256 and returns `None` on success. A mismatch raises
`HashVerificationError(ModelError)` carrying code `CONTENT_HASH_MISMATCH`, path
`$.ref.content_hash`, a clear message, and the affected RevisionRef. It never
rewrites the revision.

## Canonical payload

Every payload contains `editorial_schema_version=1`, `kind`, `id`, `revision`
and every semantic field listed in the approved hash contract. It omits its own
`content_hash` and companion `owner_ref`. Nested RevisionRefs remain complete,
including supplied content hashes. Null semantic fields remain explicit and
meaningful arrays keep their order.

The five and only five schema-1 audit exclusions are:

1. ProductionRevision.created_at;
2. SourceDetails.accessed_at;
3. ClaimReview.reviewed_at;
4. EvidenceLink.reviewed_at;
5. RightsReview.reviewed_at.

Published dates and rights expiry are included, including null. RightsReview
contains `subject_kind`, `subject_id`, `subject_revision` and `material_digest`,
but no full subject Ref. Thus Source/Asset may contain full `rights_ref` without
creating a reverse content-hash cycle.

For AssetRevision only, flat payload identity remains `kind="asset"`; the media
type is stored as `asset_kind="image|audio|video"`. E01.2 JSON continues using
its existing media field `kind`.

Canonical JSON uses `ensure_ascii=False`, `sort_keys=True`, compact separators,
`allow_nan=False`, and UTF-8. No Unicode normalization, trimming, case changes
or array sorting occurs.

## Synthetic schema-1 vectors

The full synthetic fixture locks all nine results in tests. Representative
examples:

| Revision | SHA-256 |
| --- | --- |
| production | `14da48a7be1878a11f09ed12d95b993dbb6048de5e5d613e3af2187d1154b675` |
| script | `f46dcb9e5ab40ef1e114200ae075e0f2f1df4a6fcaddc74021d5f1579813aa08` |
| asset | `4c39964a170275165439e6adf7277e67c7943ed8437442876fe340ef06ac8753` |
| rights_review | `6f046e4b9905fb312658955adc7217163b062120d778492521979400ee1ef393` |

These values are content hashes of synthetic semantic payloads, not media
sha256, rights material digests, dependency digests or snapshot checksums.

## Test matrix and actual result

| Area | Verified behavior |
| --- | --- |
| Coverage | Canonical payload and SHA-256 for all nine revision types |
| Determinism | Repeated bytes/hash and fixed golden vectors; JSON key insertion order has no effect |
| Semantics | Semantic field, nested ref hash, identity id/revision and rights subject changes alter hash |
| Audit exclusions | All five excluded timestamp categories leave the relevant revision hash unchanged |
| Included dates | published_at and expires_at are present as null and alter hash when changed |
| Self-reference | Changing only the revision's own supplied content_hash does not alter bytes/hash |
| Asset collision | identity kind remains asset; asset_kind preserves media type and affects hash |
| Rights cycle | subject binding has kind/id/revision/material_digest and no subject content_hash |
| Text | RU/UK, emoji, whitespace and combining characters stay exact; NFC-equivalent text hashes differently |
| Diagnostics | Correct hash succeeds; mismatch and companion errors have stable codes and paths |
| Isolation | Asset hashing performs no media read, file write, network access or process launch |
| Regression | All prior decoder, encoder and E01.1b editorial tests continue to pass |

Environment: Linux, Python 3.12.14, existing `.venv`; no installation or
external service.

```sh
.venv/bin/python -m unittest discover -s tests -p 'test_editorial_*.py' -q
```

Result: **127 tests passed**. This is 15 E01.3.1 tests plus the previous 112
editorial tests.

## Findings and remaining scope

Two ambiguities were resolved explicitly by the owner before implementation:
the closed audit timestamp list and the AssetRevision `kind` collision. There
are no remaining E01.3.1 architectural questions.

This task does not verify reference targets, source/asset rights binding,
cycles, conflicting revisions or production ownership. It does not implement a
dependency digest, snapshot checksum, approval authority, factual/right review,
media-byte hashing, persistence, CLI or workflow. Those boundaries remain for
separately authorized work; E01.3.2 has not started.
