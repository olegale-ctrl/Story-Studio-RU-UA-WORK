# E01.3.8.6 — Pure In-Memory Schema 1 → Schema 2 Migration

## Git provenance and scope

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Base branch: `feat/editorial-e01-3-8-5-schema2-integrity`.
- Exact base SHA: `c7a6f0956def3fd5c5d905e1490b6fa76b460923`.
- New branch: `feat/editorial-e01-3-8-6-schema2-migration`.
- Final commit SHA: supplied literally in the completion response; it is also
  obtained with `git log -1 --format=%H feat/editorial-e01-3-8-6-schema2-migration -- docs/tasks/E01_3_8_6_RESULT.md`.
  This report is part of that commit and does not attempt to embed its own hash.

Local branch/HEAD and remote base SHA were checked before changes and matched
the exact required base. The starting working tree was clean. The new branch
was created directly from that SHA. No main change, merge, rebase, PR or release
was performed.

Exactly these three files are added:

1. `editorial/schema2_migration.py`
2. `tests/test_editorial_schema2_migration.py`
3. `docs/tasks/E01_3_8_6_RESULT.md`

No existing file, model, codec, integrity implementation, test, contract or
configuration was changed. The requested implementation modules and approved
authority/schema-2 contracts were studied, especially schema-2 §10. E00 was
read from normative documentation commit
`e520648411b99264688ff66dc61ad0e974201ed3` without merging or copying it into the
working branch. Decisions A1–A14 and O1–O10 are unchanged.

## Public API and input/output contract

```python
migrate_schema1_to_schema2(snapshot, *, actor, at, event_id) -> Schema2MigrationResult
```

The frozen result contains `status` and `snapshot`. `Schema2MigrationStatus` has
two distinct string-enum values: `MIGRATED` and `ALREADY_MIGRATED`.

- Exact `ContractSnapshot` input must satisfy the strict schema-1 wire contract
  and complete source integrity. Successful conversion returns `MIGRATED` with
  a new `Schema2Snapshot`.
- Exact `Schema2Snapshot` input returns `ALREADY_MIGRATED` with the identical
  object, without inspection or modification. Unused actor/at/event_id values
  are not validated on this path. It is not an integrity, origin, trust or
  authority attestation. Existing schema-2 data can be checked independently
  with the integrity API.
- Dictionaries, raw bytes, other types and subclasses are rejected with a
  structured `TYPE` violation at `$`.

All event metadata is explicitly required from the caller. No actor, timestamp
or UUID is generated. Actor is descriptive text, not an authenticated principal;
a future authenticated service must establish the provenance of supplied data.

## Validation order and migration algorithm

1. Dispatch only exact input types. The schema-2 no-op returns immediately.
2. For schema 1, call public `encode_snapshot`. The unchanged encoder enforces
   version 1, closed wire rules, exact decode/encode round-trip, collection
   constraints, record validity and uniqueness before any output construction.
3. Call public `validate_snapshot_integrity` for source checksum, complete
   reference graph, every revision content hash including unreferenced history,
   and every rights binding. Existing diagnostic classes/codes/paths propagate.
4. Validate caller metadata by constructing the existing `Schema2Event` and
   reject an event ID that already appears in source events. Model violations
   retain their codes/messages and gain the exact new event wire path.
5. Compute generation + 1 exactly, rejecting an increment that cannot be
   represented by the existing JSON integer conversion rules. There is no
   invented 64-bit upper bound, wrap, reset or clamp.
6. Build new immutable common containers with the increased generation and
   `source.events + (migration_event,)`. All existing revision, approval,
   companion and active-ref objects/tuples are reused unchanged. Wrap the
   common aggregate in `Schema2Snapshot` with empty evidence.
7. Compute the full output checksum only through
   `compute_schema2_snapshot_checksum`. The format-valid source checksum is a
   temporary excluded field during calculation, not the output checksum.
   Store the new checksum in a new immutable container.
8. Call `validate_schema2_snapshot_integrity` on the complete output.
9. Explicitly encode/decode with the versioned codec and require exact
   equality before returning `MIGRATED`.

No partial output is returned if any source, construction, checksum,
postvalidation or round-trip step fails. No source repair is attempted. Source
integrity errors take precedence over unused migration metadata errors.

The exact appended event is:

```text
id         = caller event_id
actor      = caller actor
at         = caller at
action     = schema_migrated
refs       = ()
reason     = Editorial snapshot migrated from schema 1 to schema 2
error_code = None
```

The actual schema-2 wire envelope has `editorial_schema_version = 2`, generation
increased exactly once, mandatory `approval_authority_evidence: []`, and a new
checksum. Every other existing root value stays identical except `events`,
which gains exactly the one appended event. The existing Schema2Snapshot model
continues to keep unchanged schema-1-compatible common data internally; no
model or wire format was redesigned.

All original UUIDs, timestamps, Unicode code points, whitespace, revision
hashes and collection order remain literal. No sorting, normalization, latest
record selection or historical approval rewrite is performed.

## Errors and boundary cases

`Schema2MigrationError` extends `Schema2ModelError` and uses existing immutable
`Violation`. Additional codes are `DUPLICATE_EVENT_ID`, `GENERATION_OVERFLOW`
and `MIGRATION_ROUND_TRIP_MISMATCH`. Model construction failures retain their
original codes/messages/object refs, with JSON-style paths. Existing source and
output codec/integrity exceptions are not replaced by a generic failure.

Generation uses Python arbitrary-precision integers. Tests cover increments
across signed/unsigned 64-bit boundaries and a 101-digit generation. The actual
runtime decimal conversion limit is also exercised: a source at the maximum
permitted decimal length validates, but an increment requiring another digit
fails at `$.generation`. The implementation does not read environment or
change interpreter configuration. If the runtime disables that existing
conversion limit, arbitrary-precision growth remains allowed.

The existing 10,000-event limit is retained. A valid source already at that
limit cannot accept a migration event; conversion raises a structured error at
`$.events`, without discarding events or returning a partial object.

## Legacy, idempotency and history

Migration creates no ApprovalAuthorityEvidence, principal, policy, session,
request, declaration evidence, attestation digest, signature or reconsideration
link. Original approvals remain the exact same objects in the same order.
The schema-2 integrity result classifies them as `UNAUTHENTICATED_LEGACY`, which
does not prove historical origin or establish any effective approval.

Repeated calls on schema-2 input return the same object and preserve generation,
events, checksum, evidence, signatures and encoded bytes. Even an existing
schema-2 checksum mismatch is neither checked nor repaired on the no-op path.
Tests explicitly distinguish `ALREADY_MIGRATED` from integrity success.

History tests preserve APPROVE/REJECT/REVISE/REVOKE fields and order, revocation
projection, conflicting same-time history, and equivalent same-time decisions
without choosing a UUID. They compare the existing public source history
projection with its unchanged pure projection on the preserved output records.
Dependency-consistency tests likewise compare the existing evaluator and
unchanged dependency digest. No downgrade or new schema-2 history/authority
service is implemented; the existing public history/consistency entry points
still retain their schema-1 checksum contract.

## Independent literal checksum vectors

Three fixed migration scenarios have literal expected output checksums:

| Source scenario | Output canonical byte length | Expected schema-2 SHA-256 |
|---|---:|---|
| Empty valid schema-1 draft | 650 | `015e310c17e7e7e47e4c276ce0f54d775fd79356bfaf8f54d1f2a9cca9c72fac` |
| Full graph, rights, revisions and approval history | 8809 | `e71c83e7db4eb3cf57f9fc0a3172d3b82a03c5b773ad202ae21362f290966fb1` |
| Full graph with conflicting same-time decisions | 9301 | `1d547ff6a26f0f018ada3e309af8c60869f260ba550c92a690711e4e29da9aca` |

Method: existing schema-1 fixture builders and the pre-existing schema-1 encoder
provided source wire objects. A separate standalone Node.js script outside the
repository cloned those objects, explicitly changed version/generation, added
empty evidence, independently appended the exact literal event, removed only
root checksum, and recursively serialized sorted keys and unchanged arrays
using JSON.stringify for scalars. It encoded UTF-8 and passed the bytes to
`openssl dgst -sha256 -binary`. The transform did not call the tested migration
function or the new checksum API. Expected values are fixed literals in tests,
not computed by migration during tests. No oracle script or dependency was
added to the repository.

## Actual tests and verification

The new file has 50 unittest methods, with subtests for invalid metadata/types,
generation boundaries, approval decisions and historical scenarios. Coverage
includes every required success/failure case, exact wire transform, retained
object identity, source and output failures, actual event-count exhaustion,
idempotency with existing evidence/signatures, legacy status, no authority
claims, no downgrade, side-effect guards and deterministic bytes.

The subprocess audit-hook test forbids filesystem, socket and subprocess
operations during migration and repeat invocation. Additional patched APIs
guard filesystem access, system clocks, environment reads, random bytes and
UUID generation on success and failure paths. Timestamp parsing remains
allowed; current-time lookup does not.

Commands actually run in the existing Linux cloud checkout with project
`.venv` (Python 3.12.14):

```text
.venv/bin/python -m unittest discover -s tests -p 'test_editorial_schema2_migration.py' -v
Ran 50 tests in 4.084s — OK

.venv/bin/python -m unittest discover -s tests -p 'test_editorial*.py' -v
Ran 528 tests in 21.261s — OK
Failures: 0; errors: 0; skips: 0

.venv/bin/python -m compileall -q editorial tests
exit 0

git diff --check
exit 0

git diff --cached --check
exit 0

git status --short
Only the three allowed additions before commit; clean after commit.

git diff c7a6f0956def3fd5c5d905e1490b6fa76b460923..HEAD --check
exit 0 (published commit)
```

The final `git rev-parse HEAD` is compared with
`git ls-remote origin refs/heads/feat/editorial-e01-3-8-6-schema2-migration`
after publication; the matching literal SHA is reported in the completion
message. The existing 478-test editorial suite remains successful alongside
the 50 new migration tests.

## Trust limits, known issues and stop point

There is no persistence, atomic writer, protected head anchor, OS authentication,
authority policy, signing/verification, review session, write command, automatic
recovery, trust establishment, downgrade, production readiness or commercial
rights authorization. The source approvals remain unchanged, evidence remains
empty, and no trusted head is created or restored.

No unresolved implementation/test failure is known within this scope. Existing
event/byte/integer codec limits remain enforced and can prevent conversion;
they are errors, not permission to truncate source history. Migration success
means structural conversion with verified integrity, not authenticated origin,
verified transaction ordering, effective authority or readiness. Actor supplied
to this pure API is not authenticated by this implementation.

Work stops after E01.3.8.6 publication. Atomic storage, head anchor and all later
stages remain separate tasks requiring independent review and owner decision.
