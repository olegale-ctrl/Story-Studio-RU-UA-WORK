# E01.3.2 — exact revision references and dependency graph

## Scope and approved rules

Branch: `feat/editorial-e01-3-2-reference-graph`.
Base: `876549006c698d09509401c1dc6a0fcca69ccfec` (accepted E01.3.1).

The owner approved these E01.3.2 rules before implementation:

- history may contain multiple revisions of one `(kind, UUID)`; only an exact
  duplicate `(kind, UUID, revision)` is invalid;
- different reachable revisions of one UUID are not yet an active-package
  conflict;
- explicit ownership is limited to ProductionRevision IDs and production_ref;
- shared GenreProfile must be an exact local snapshot revision;
- dependency edges use the closed field list below;
- a cycle repeats one exact identity along directed dependency edges.

No package-root, implicit ownership, latest-version or completeness rule is
introduced. E00/E01.1a are not silently changed.

## API

```python
from editorial.graph import (
    GraphValidationError,
    build_revision_index,
    validate_reference_graph,
)

index = build_revision_index(snapshot)
graph = validate_reference_graph(snapshot)
```

`build_revision_index` returns a read-only mapping keyed by
`(ObjectKind, UUID, revision)`. It checks exact duplicates, concrete class/kind
agreement and ProductionRevision ownership.

`validate_reference_graph` returns an immutable `ReferenceGraph` containing the
read-only index and ordered tuple of `DependencyEdge(source, target,
field_path)`. It resolves every dependency edge, active ref, approval object_ref
and event ref only inside the supplied ContractSnapshot. It never mutates the
snapshot or selects a replacement revision.

For every resolved reference it checks exact kind/id/revision, equality of the
reference hash with the target ref, and the target's freshly computed E01.3.1
semantic hash. Target hash computation uses the matching SourceDetails,
ClaimReview or RightsDetails from the same snapshot and is cached per exact
identity during a validation run.

`GraphValidationError` extends ModelError and carries the existing immutable
Violation with stable code, exact JSON-style field path, explanation and, when
available, affected RevisionRef.

## Closed dependency-edge list

| Source type | Traversed RevisionRef fields |
| --- | --- |
| ProductionRevision | `profile_ref` |
| GenreProfile | none |
| CandidateRevision | `source_refs[]` |
| SourceRevision | `rights_ref` |
| ClaimRevision | `evidence_links[].source_ref` |
| ScriptRevision | `production_ref`, `candidate_ref`, `brief.profile_ref`, `brief.must_include_claim_refs[]`, `segments[].claim_refs[]`, `claim_refs[]` |
| ScenePlanRevision | `script_ref`, non-null `scenes[].asset_ref` |
| AssetRevision | `rights_ref`, non-null `script_ref` |
| RightsReview | none |

Nullable references with null values produce no edge and no error. Repeated
exact links in distinct fields remain distinct permitted edges. Identity refs
and active refs are not edges. Approval/Event refs are resolved but are not
edges because those records are not revision nodes.

RightsReview subject_kind/subject_id/subject_revision/material_digest remains a
non-edge binding. Therefore Source/Asset → RightsReview does not acquire a false
reverse edge and cannot create the prohibited rights hash cycle.

Active slots are checked separately and exactly. No missing slot is inferred.
Every production_ref must target a ProductionRevision whose ID equals
snapshot.production_id. Objects without owner fields receive no invented
ownership checks. Shared profiles are local exact targets like every other ref.

## Error codes

| Code | Meaning |
| --- | --- |
| `DUPLICATE_IDENTITY` | repeated exact `(kind,id,revision)` |
| `REVISION_KIND_MISMATCH` | concrete payload class disagrees with own ref.kind |
| `FOREIGN_PRODUCTION` | explicit production identity/ref leaves snapshot production |
| `MISSING_TARGET` | UUID has no local target |
| `TARGET_KIND_MISMATCH` | UUID exists only under other ObjectKind values |
| `TARGET_REVISION_MISMATCH` | kind/UUID exists but requested revision does not |
| `REFERENCE_KIND_MISMATCH` | field's closed target kind is violated |
| `REFERENCE_HASH_MISMATCH` | nested supplied hash differs from exact target ref |
| `TARGET_HASH_INVALID` | target ref hash fails E01.3.1 recomputation |
| `DEPENDENCY_CYCLE` | DFS reaches an active exact identity again |

Cycle detection is iterative, deterministic and safe for the 10000-revision
limit. The schema-1 normative type graph is acyclic; the negative test uses a
malformed weak legacy SourceRevision link that forms a self-cycle. Cycle
diagnosis intentionally precedes the accompanying field-kind diagnosis so the
cycle guard remains directly testable and effective for malformed in-memory
objects.

## Tests and actual result

The positive fixture starts from all nine revision types and computes correct
content hashes in dependency order with E01.3.1. Old placeholder hashes are not
treated as valid.

Tests cover:

- valid nine-type index and 13 normative edges;
- exact resolution and immutable index;
- missing target, wrong kind, wrong revision and mismatched reference hash;
- target hash that no longer matches its semantic payload;
- duplicate identity and class/kind mismatch;
- diagnosed cycle;
- two valid revisions of one UUID in history;
- RightsReview subject binding without a reverse edge;
- complete, missing and nullable active slots;
- explicit production ownership only;
- Approval/Event exact resolution without dependency edges;
- snapshot immutability and absence of file/network/process access;
- all previous editorial tests.

Environment: Linux, Python 3.12.14, existing `.venv`; no dependencies or
external services added.

```sh
.venv/bin/python -m unittest discover -s tests -p 'test_editorial_*.py' -q
```

Result: **142 tests passed in 2.613 seconds** — 15 new graph tests and all 127
previous editorial tests.

## Files and deferred checks

Only `editorial/graph.py`, `tests/test_editorial_graph.py` and this report are
added. Integrity hashing, codec, models, Sprint 26, timeline v3 and renderer are
unchanged.

Deferred by explicit scope:

- active package roots and conflicting reachable revisions;
- dependency digest and sorted transitive package;
- snapshot checksum;
- RightsReview subject/material binding and expiry evaluation (E01.3.3);
- ownership not represented by a model field;
- approval authority, fact/rights decisions and readiness;
- narration coverage, filesystem/media preflight, storage and CLI.

There are no open E01.3.2 architecture questions after the owner's six
decisions. E01.3.3 has not started.
