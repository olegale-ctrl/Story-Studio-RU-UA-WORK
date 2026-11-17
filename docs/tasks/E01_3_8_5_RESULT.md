# E01.3.8.5 — Schema-2 Integrity Validation

## Repository, base and files

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Exact base SHA: `350237d0d15b411a429cf93db2a8f2a968a22cbf`.
- Base branch: `feat/editorial-e01-3-8-4-attestation-digest`.
- New branch: `feat/editorial-e01-3-8-5-schema2-integrity`.
- The literal final commit SHA is supplied separately in the completion
  message, as the assignment permits, avoiding a self-referential commit hash.

The local base branch, HEAD and clean working tree were verified before
creating the branch directly from the exact base. The remote base SHA also
matched. Exactly three files are added:

1. `editorial/schema2_integrity.py`
2. `tests/test_editorial_schema2_integrity.py`
3. `docs/tasks/E01_3_8_5_RESULT.md`

No existing files, models, codecs, contracts or configurations were changed.
No main change, merge, rebase, PR or release is part of this task.

The approved authority and schema-2 contracts, all requested implementation
modules, and the relevant existing regression fixtures/tests were read.
The absent E00 document was read directly from normative documentation commit
`e520648411b99264688ff66dc61ad0e974201ed3` at
`docs/EDITORIAL_E00_FINAL_SPEC.md`; it was not copied or merged. All A1–A14 and
O1–O10 decisions remain unchanged.

## Public API and checksum

- `canonical_schema2_snapshot_bytes(snapshot) -> bytes`
- `compute_schema2_snapshot_checksum(snapshot) -> str`
- `validate_schema2_snapshot_integrity(snapshot) -> Schema2IntegrityResult`

The canonical function requires exact `Schema2Snapshot`, invokes the existing
strict `encode_editorial_versioned`, parses the complete schema-2 envelope,
removes only root `snapshot_checksum`, and uses exactly:

```python
json.dumps(
    envelope, ensure_ascii=False, sort_keys=True,
    separators=(',', ':'), allow_nan=False,
).encode('utf-8')
```

Checksum is `hashlib.sha256(canonical_bytes).hexdigest()`. All approvals,
evidence, attestation digests, null and non-null signature fields, real schema-2
events (including `schema_migrated`), generation, active refs and revision data
remain included. No schema-1 checksum function is used by the new module. The
existing encoder's internal mapping of common fields is unchanged; the checksum
is always over its complete schema-2 output, never a truncated schema-1 subset.
No checksum is repaired and no input is mutated.

## Actual validation order and reuse

1. Require exact `Schema2Snapshot`; reject schema 1, dicts, bytes and subclasses.
2. Obtain the full canonical envelope through the existing strict versioned
   encoder. This is the structural boundary: its existing immutable-model and
   codec checks reconfirm evidence-to-approval linkage, evidence order with
   legacy gaps, uniqueness of evidence/session/request IDs, exact gate/decision
   declarations, principal/text/timestamp/signature shapes, and self-reference.
   These checks are reused, not independently reimplemented or weakened.
3. Compare the complete schema-2 checksum. Mismatch raises
   `SNAPSHOT_CHECKSUM_MISMATCH` at `$.snapshot_checksum`.
4. Call public `validate_reference_graph` on the original common aggregate,
   including its real Schema2Event instances. It validates every existing graph
   invariant and, as before, verifies hashes of referenced targets. No checksum
   on that common aggregate is computed or validated.
5. Call public `verify_revision_content_hash` for every revision, including
   unreferenced historical revisions and their original companions. Existing
   snapshot-integrity helpers supply only companion lookup and wire locations;
   they do not perform a second schema-1 integrity pass.
6. Call public `validate_all_rights_bindings` with the validated graph. This
   checks structural/material bindings, not rights permission or readiness.
7. Validate each attestation digest in original evidence order using the public
   E01.3.8.4 API, remapping violations to the exact
   `$.approval_authority_evidence[index].attestation_digest` path.
8. Check reconsideration targets in original evidence order: existence, no self
   link, full exact decision key, and REJECT/REVISE/REVOKE target decision type.
9. Report same-key/same-time history ambiguity and unverified transaction order
   without selecting a latest record.

Structural validity is required to construct checksum bytes; existing structural
failures therefore precede checksum comparison. On structurally valid inputs,
failure priority is checksum → graph → all revision hashes → rights bindings →
attestation digests → reconsideration links. Tests cover simultaneous faults to
confirm this priority. No broad `INVALID_SNAPSHOT` wrapper conceals errors.

`Schema2IntegrityError` extends `Schema2ModelError` and carries `Violation`.
Existing codec/graph/hash/rights errors retain their structured classes, codes
and precise paths. New reconsideration errors are
`RECONSIDERATION_TARGET_MISSING`, `RECONSIDERATION_KEY_MISMATCH` and
`RECONSIDERATION_DECISION_MISMATCH`. Self-reference is normally rejected by the
existing model/codec before semantic integration; its existing diagnostic is
preserved, with an additional defensive self-link check in the link validator.

## Result, legacy and ordering semantics

`Schema2IntegrityResult` is immutable and contains:

- checksum verification, revision/evidence counts and material-binding results;
- approval IDs in original approval order with authority-context classification
  `UNAUTHENTICATED_LEGACY` or `EVIDENCE_PRESENT_UNVERIFIED`;
- supplied reconsideration target IDs and structural link diagnostics;
- structured `history_diagnostics` and `ordering_diagnostics`;
- `transaction_order_status = UNVERIFIED_ORDERING`;
- explicit unverified aspects: transaction order, identity, signatures,
  authority policy and head anchor.

Evidence-free approvals remain readable and unchanged, without synthetic
evidence or claims of migration provenance. Evidence presence never means that
an approval is authenticated or effective.

The exact reconsideration key uses the existing `ApprovalDecisionKey`:
`(gate, policy_version, full object_ref, dependency_digest)`. A structurally
consistent non-null link is classified
`LINK_CONSISTENT_ORDERING_UNVERIFIED`, with `UNVERIFIED_ORDERING` at its exact
field path. Neither a single candidate nor multiple candidates establish
latest applicability or precedence.

For APPROVE with a null link and same-key negative decisions somewhere in
history, the result is `RECONSIDERATION_REQUIREMENT_UNVERIFIED`: without trusted
transaction order, those decisions could precede or follow that APPROVE.
The validator does not invent chronology, silently add a link, or claim the
missing link is justified. Initial null links without such negative records
remain `NO_LINK`, while the global ordering status still stays unverified.

History diagnostics group records by exact key and exact timestamp, without
sorting timestamps, taking a maximum, or selecting a UUID/array position.
Conflicting decisions or materially different actor/reason/review declarations
produce `AMBIGUOUS_HISTORY` Violations at every involved approval timestamp.
Equivalent same-time records are retained without selecting an ID. All groups
are inspected, so a later descriptive timestamp does not suppress an older
conflict. The existing public schema-1 history evaluator is not called: it
requires a schema-1 checksum and performs a timestamp projection, which would
not establish trusted transaction ordering for this task.

Ambiguity and unverified ordering are inspection diagnostics, not claims that
authority passed. The result has no `authorized`, `approved`, `ready`,
`effective` or chosen `latest_record` field. Its checksum-verification flag
means only that exact bytes match a stored checksum.

## Independent fixed checksum values

Tests contain literal expected digests for four fixed snapshots and literal
canonical bytes for the empty snapshot:

| Snapshot | Canonical bytes | SHA-256 |
|---|---:|---|
| Empty schema-2 draft | 386 | `1f2f4eddf534c5546bc729d74ef445f0aee0292a91d2d589cd5456d24e1cc201` |
| Complete historical graph with Unicode evidence | 9243 | `ace06e2eb6ee0a929752c3422589747a5b71224b036e869283e89d9d872f3af5` |
| Same graph with a complete synthetic signature tuple | 9340 | `372407f0d151fc82a6830790fe4844f17df721eaa8ed2a0ed0aee593fb21f96f` |
| Empty graph with a real `schema_migrated` fixture event | 574 | `09a828757ebae10cfc0ba903bc561bfda849f2b58ca5d448ea7f22346e9ae936` |

Method: existing pre-task schema-1 fixtures, hashing and attestation helpers
constructed deterministic source data, and the existing versioned encoder
exported the complete wire objects. None of the new checksum/validation APIs
were called to obtain the expected values. A standalone Node.js script outside
the repository removed only root checksum and recursively serialized sorted
object keys, unchanged arrays and JSON-stringified scalars, then encoded UTF-8.
`openssl dgst -sha256 -binary` calculated each digest from those bytes.
The byte counts/digests were frozen as literals; tests do not calculate their
expected values through the tested API. Node.js and OpenSSL are oracle tools
used during development, not runtime or test dependencies.

The `schema_migrated` fixture is test data, not a migration implementation.
Synthetic signature bytes validate format/coverage only and are not verified.

## Tests and checks

Added 52 unittest methods, including parameterized subtests for every core
evidence field, all gate/decision declaration combinations, signature coverage,
reconsideration exact-key components and all three negative target decisions.
Coverage includes valid/empty snapshots, legacy gaps, multiple ordered evidence,
model-invariant rejection at the integration boundary, checksum tampering,
resealed evidence tampering with stale attestation digest, schema-2 events,
graph/revision-hash/companion/rights regressions, failure priority, dangling/self/
cross-key/wrong-decision links, ambiguous/equivalent histories, no trusted
ordering, input immutability, schema-1 compatibility and repeated round-trips.

Audit-hook and patched-API tests guard filesystem/network/subprocess operations,
clock/environment reads and random ID/byte generation. Timestamp parsing remains
allowed. No dependencies were added.

Actual Linux cloud-environment commands used the existing project `.venv`
(Python 3.12.14):

```text
.venv/bin/python -m unittest discover -s tests -p 'test_editorial_schema2_integrity.py' -v
Ran 52 tests in 6.130s — OK

.venv/bin/python -m unittest discover -s tests -p 'test_editorial*.py' -v
Ran 478 tests in 22.613s — OK
Failures: 0; errors: 0; skips: 0

.venv/bin/python -m compileall -q editorial tests
exit 0

git diff --check
exit 0

git diff --cached --check
exit 0

git status --short
Only the three allowed additions before commit; clean after commit.

git diff 350237d0d15b411a429cf93db2a8f2a968a22cbf..HEAD --check
exit 0 (published commit)
```

Final `git rev-parse HEAD` and
`git ls-remote origin refs/heads/feat/editorial-e01-3-8-5-schema2-integrity`
are compared after publication; the matching literal SHA is supplied in the
completion message. The complete existing 426-test suite remains successful
alongside the 52 new tests.

## Explicit limits and stop point

There is no authority evaluation, authority-policy implementation, OS
authentication, signing/verification, protected head anchor, trusted transaction
sequence, write command, migration, storage, automatic trust recovery,
production readiness or rights authorization. No input is changed and no
filesystem, network or clock state is consulted by the new API.

An editable snapshot can have its hashes/digests/checksum recomputed by an
attacker. Integrity consistency alone proves neither reviewer identity nor
human understanding, origin, authenticity, trusted time, latest applicable
decision, licence rights or permission to render/export/publish commercially.
Authority remains outside this stage even when all integrity checks pass.

Stop after publishing E01.3.8.5. E01.3.8.6 is not started or authorized by this
implementation.
