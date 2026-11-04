# E01.3.3 — RightsReview subject/material binding

## Scope and baseline

Branch: `feat/editorial-e01-3-3-rights-binding`.
Base: `4784886ab05640962b1272ce01d9c7470539bec2` (accepted E01.3.2).

This task adds only the pure Source/Asset → RightsReview structural and material
binding check. Codec, model, E01.3.1 hashes, E01.3.2 graph, Sprint 26, timeline
v3 and renderer are unchanged.

The governing contracts resolve the preimplementation questions as follows:

- SourceDetails.material_digest=null is a valid unresolved state, not structural
  corruption and never confirmed rights;
- a present but unequal digest is an integrity error;
- multiple historical RightsReview records may describe the same subject;
  the subject's exact rights_ref selects the applicable record;
- structural validation covers every historical SourceRevision and
  AssetRevision, while active policy/readiness remains deferred.

## API and result states

```python
from editorial.rights_binding import (
    MaterialBindingState,
    RightsBindingError,
    RightsBindingResult,
    validate_rights_binding,
    validate_all_rights_bindings,
)

one = validate_rights_binding(snapshot, prevalidated_graph, source_or_asset)
all_history = validate_all_rights_bindings(snapshot, prevalidated_graph)
```

`RightsBindingResult` is frozen and contains:

- exact `subject_ref`;
- exact selected `rights_ref`;
- `structural_match=True`;
- `material_state=CONFIRMED|UNCONFIRMED`.

A result is returned only after kind, UUID and revision match. Structural
mismatches raise `RightsBindingError(ModelError)` with an immutable Violation.
The result deliberately has no `allowed`, `permitted`, readiness, intended-use
or expiry-policy field.

`CONFIRMED` means only that a stored digest is present and equal:

- SourceRevision: SourceDetails.material_digest equals
  RightsReview.material_digest;
- AssetRevision: AssetRevision.sha256 equals RightsReview.material_digest.

`UNCONFIRMED` applies only to SourceRevision with explicit null
SourceDetails.material_digest after a structurally correct subject match. Asset
sha256 is mandatory, so Asset has no corresponding missing-digest state.

## Exact checks

The function requires the subject object and exact RightsReview target to be
the same objects indexed by the supplied prevalidated E01.3.2 graph. It then
checks:

1. subject.rights_ref resolves exactly to RightsReview;
2. exactly one matching RightsDetails companion exists and owner_ref matches;
3. RightsDetails.subject_kind equals source or asset;
4. RightsReview.subject_id equals subject.ref.id;
5. RightsReview.subject_revision equals subject.ref.revision;
6. the appropriate material digest is confirmed or explicitly unresolved.

Bulk validation iterates every historical SourceRevision and AssetRevision in
the snapshot's canonical revision order. It neither selects active revisions
nor scans unrelated RightsReview records. Multiple reviews for one exact
subject remain legal; only the exact rights_ref is evaluated.

| Error code | Meaning/path |
| --- | --- |
| `GRAPH_SNAPSHOT_MISMATCH` | graph, subject or rights target belongs to another aggregate |
| `RIGHTS_TARGET` | rights_ref is not the exact graph RightsReview target |
| `COMPANION_BINDING` / `COMPANION_OWNER` | missing, ambiguous or mismatched typed metadata |
| `SUBJECT_KIND_MISMATCH` | RightsDetails.subject_kind differs from object kind |
| `SUBJECT_ID_MISMATCH` | subject UUID differs |
| `SUBJECT_REVISION_MISMATCH` | subject revision differs |
| `MATERIAL_DIGEST_MISMATCH` | known Source digest or Asset sha256 differs from review material_digest |

RightsReview.status is retained but not interpreted. Tests demonstrate that
approved, restricted, unknown and blocked all produce the same binding result
when structural/material data is identical. In particular, approved plus a
null Source material digest remains UNCONFIRMED.

## Graph and hash boundaries

The validator consumes an already validated ReferenceGraph. It does not add or
remove graph edges. RightsReview subject_kind/id/revision/material_digest remains
a non-edge binding, so no RightsReview → Source/Asset reverse dependency is
introduced and E01.3.1 canonical hashes remain unchanged.

The positive fixture contains separate exact RightsReview revisions for Source
and Asset and rebuilds all RevisionRef.content_hash values in dependency order
through E01.3.1 before E01.3.2 graph validation. Placeholder hashes are never
accepted as positive graph data.

## Tests and actual result

Tests cover:

- confirmed Source and Asset bindings;
- wrong subject_kind, subject_id and subject_revision;
- Source and Asset material mismatch;
- null Source material digest as UNCONFIRMED;
- all historical subject revisions;
- multiple RightsReview records for one exact subject;
- all RightsStatus values without authority inference;
- unchanged dependency graph and absence of reverse rights edges;
- no filesystem, network, process or mutation side effects;
- all previous 142 editorial tests.

Environment: Linux, Python 3.12.14, existing `.venv`; no dependency or external
service added.

```sh
.venv/bin/python -m unittest discover -s tests -p 'test_editorial_*.py' -q
```

Result: **153 tests passed in 3.022 seconds** — 11 new rights-binding tests and
all 142 previous editorial tests.

## Files, deferred scope and open questions

Added files:

- `editorial/rights_binding.py`;
- `tests/test_editorial_rights_binding.py`;
- `docs/tasks/E01_3_3_RESULT.md`.

Deferred exactly as requested: dependency digest, active package conflicts,
snapshot checksum, policy/expiry/intended-use/action evaluation, commercial
license decisions, approval gates, readiness, media-byte I/O, storage and UI.

There are no remaining E01.3.3 architecture questions. No later stage was
started.
