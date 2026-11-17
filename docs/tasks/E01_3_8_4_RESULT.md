# E01.3.8.4 — Canonical Approval Attestation and SHA-256 Digest

## Provenance and scope

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Base branch: `fix/editorial-e01-3-8-3a-event-codec`.
- Exact base SHA: `0e6a0522bd7842ddc9fd5d9ee09c5c0490c48122`.
- Implementation branch: `feat/editorial-e01-3-8-4-attestation-digest`.
- Final commit SHA: resolve with
  `git log -1 --format=%H feat/editorial-e01-3-8-4-attestation-digest -- docs/tasks/E01_3_8_4_RESULT.md`.
  The literal final SHA is also supplied in the completion message. This report
  belongs to that commit and cannot embed its own SHA without changing it.

The local base branch and HEAD matched the required SHA and the working tree
was clean before creating the new branch directly from that commit. The remote
base branch was also checked and matched. No merge, rebase, PR, release or main
change was performed.

Normative documents read: the approved E01.3.7.3 authority contract and the
approved E01.3.8.1 schema-2 contract, especially §8. Decisions A1–A14 and O1–O10
are unchanged. `docs/EDITORIAL_E00_FINAL_SPEC.md` is not in the base tree; it was
read directly from the preserved documentation commit
`e520648411b99264688ff66dc61ad0e974201ed3`, identified by the existing
`E01_1_RESULT.md`. No documentation branch was merged or checked out and no
existing file was copied or changed.

Exactly four files are added:

1. `editorial/approval_attestation.py`
2. `tests/test_editorial_approval_attestation.py`
3. `tests/fixtures/editorial_attestation_vectors.json`
4. `docs/tasks/E01_3_8_4_RESULT.md`

## Implemented API and errors

- `canonical_attestation_bytes(approval, evidence) -> bytes`: returns exact
  canonical UTF-8 bytes, regardless of whether the stored digest matches.
- `compute_attestation_digest(approval, evidence) -> str`: returns
  `hashlib.sha256(canonical_attestation_bytes(...)).hexdigest()`.
- `validate_attestation_digest(approval, evidence) -> None`: checks the stored
  digest and returns no authority or readiness result.
- `canonical_signed_bytes(approval, evidence) -> bytes`: returns exactly
  `b"story-studio-approval-attestation-v1\x00" + canonical_attestation_bytes(...)`.

`ApprovalAttestationError` extends the existing `Schema2ModelError` and carries
the existing immutable `Violation`. Exact argument types are required;
dictionaries and subclasses are rejected with `INVALID_APPROVAL_TYPE` at
`$.approval_record` or `INVALID_EVIDENCE_TYPE` at `$.authority_evidence`.
An ID mismatch yields `APPROVAL_ID_MISMATCH` at
`$.authority_evidence.approval_id`, before digest comparison. A wrong digest
yields `ATTESTATION_DIGEST_MISMATCH` at
`$.authority_evidence.attestation_digest`. Digests are never repaired.

The unchanged pure `codec._APPROVAL` parser validates the explicitly mapped
ApprovalRecord wire shape, including the weak legacy constructor's gate and
timestamp fields. No snapshot codec is invoked by the attestation API. Existing
codec violations retain their exact codes and paths within the new error type.
Text is checked with the existing pure Unicode validator, including legacy
fields and indexed review declarations. Serialization failures produce a
deterministic `ATTESTATION_SERIALIZATION_ERROR` at `$` without including input
contents in the message.

No evidence declaration eligibility, authority-policy evaluation or
reconsideration-history evaluation is added. Evidence uses the existing
immutable model's local invariants.

## Exact canonical payload and §8 compliance

The payload is built by explicit field enumeration, with exactly these fields:

```text
approval_authority_evidence_schema_version: integer 1
approval_record:
  id, gate, object_ref, dependency_digest, policy_version, actor, timestamp,
  decision, reason, review_declarations
  object_ref: kind, id, revision, content_hash
authority_evidence:
  approval_id, principal_id, principal_display_name, authority_policy_id,
  authority_policy_version, review_session_id, request_id, declaration_codes,
  attested_at, reconsiders_record_id
```

Only `attestation_digest`, `signing_key_id`, `signature_algorithm` and
`signature` are excluded from evidence. Enum members map to exact wire values;
tuple fields map to arrays with their original order. Null reconsideration is
explicit JSON null. Future model fields cannot enter the payload implicitly.

Serialization is exactly:

```python
json.dumps(
    payload,
    ensure_ascii=False,
    sort_keys=True,
    separators=(',', ':'),
    allow_nan=False,
).encode('utf-8')
```

The SHA-256 digest contains exactly 64 lowercase hex characters. Unicode code
points, whitespace, case, timestamps and array order are preserved. Surrogates
are rejected rather than replaced. No normalization, trim, hidden defaults,
timezone conversion, IDs, UI state or clock values are introduced. Signed
bytes add only the exact ASCII domain followed by one NUL byte, without any
wrapper, length prefix, extra separator or terminator. This implements schema-2
§8.1 and the byte-preparation portion of §8.2.

## Independent golden vectors

The fixture contains four fixed vectors with complete source ApprovalRecord and
ApprovalAuthorityEvidence objects, literal canonical UTF-8 hex, literal SHA-256
and literal domain-separated signed-byte hex:

| Vector | Canonical byte length | SHA-256 |
|---|---:|---|
| SCRIPT approve, POSIX principal, RU/UK, emoji, combining text, null reconsideration, unsigned | 1485 | `029430847edc657793b89022f761ec7db2671af0c275b2c81f0e9a4312d65cd4` |
| SCENES reject, Windows principal, non-null reconsideration, complete signature tuple | 1244 | `3eb0e6db34c5c92ff04191d93a47d73ada13bc417005810391050a5ec757b93e` |
| HANDOFF approve with composed text | 1388 | `b61fbc970f3e4db7cfa31c14ad54cfa1fdc3ffa467c360a3e4cc3f829e3fbaee` |
| Otherwise identical HANDOFF with decomposed text | 1394 | `2231619b0e56986abf2e2e3bbc6abec6bb2ae0314711c94311664ea883ddf329` |

An independent standalone Node.js script outside the repository generated the
fixture without importing any project code. It serialized separately supplied
wire objects recursively: sorted ASCII object keys, JSON.stringify for keys
and scalar values, unchanged array order, and explicit commas/colons/brackets.
It converted that text with Buffer UTF-8 encoding and passed those bytes to
`openssl dgst -sha256 -binary`. Signed bytes were independently assembled with
Buffer concatenation and converted to hex. All resulting expected values were
saved as literals. The tests read those literals; they do not invoke the tested
API to manufacture expected bytes or digests. The signature bytes are synthetic
format-valid test data and are not an actual signature or identity proof.

## Tests and actual validation results

The new module contains 35 unittest methods, with subtests covering every
ApprovalRecord field, every core evidence field, and every RevisionRef field.
Coverage includes all golden bytes/digests/signed bytes, determinism, order,
RU/UK/emoji/combining text, composed/decomposed differences, whitespace/case,
null and non-null reconsideration, excluded fields, changed signature tuples,
placeholder digests, strict argument types, mismatch precedence, structured
errors, malformed Unicode, legacy gate/timestamp validation, serialization
failures, input immutability, and the exact domain separator.

Side-effect guards cover filesystem access, network access, clock reads,
environment reads, random ID generation, subprocesses and random bytes on both
success and digest-failure paths. Timestamp parsing is allowed; current-time
lookup is not. Schema-1 direct/versioned codec equivalence and schema-2
round-trips are checked, including all four golden vector pairs. Successful
digest validation is explicitly tested without known authority policy or
resolvable reconsideration history; this establishes no authority claim.

Actual commands run on Linux:

```text
python -m unittest tests.test_editorial_approval_attestation -v
Ran 35 tests — OK

python -m unittest discover -s tests -p "test_editorial*.py" -v
Ran 426 tests in 16.077s — OK
Failures: 0; errors: 0; skips: 0

python -m compileall -q editorial tests
exit 0

git diff --check
exit 0

git status --short
Only the four allowed additions are staged before commit.
```

The complete existing 391-test editorial suite remains successful alongside
the 35 new tests. No schema-1/schema-2 codec, model, checksum, contract,
configuration, snapshot or existing test was edited. No dependencies were
added. The final status and remote SHA are verified after publication and
reported in the completion message.

## Security limits and next stage

There is no Ed25519 signing or verification, trusted key registry, identity
authentication, authority evaluation, policy-file access, trusted time, storage,
migration, snapshot integrity validation or protected head anchor in this
implementation. The APIs perform no filesystem or network operations and do
not mutate their input objects. A digest can be recomputed by anyone who can
edit the supplied values; digest validity proves neither original authorship
nor human review, factual truth, rights, readiness or permission to render,
export, publish or use commercially. A signature-shaped tuple adds no trust.

E01.3.8.5 remains a separate, unstarted task: schema-2 integrity composition,
evidence joins/order, declaration eligibility and reconsideration checks to the
extent supported by verified history. It requires independent review and an
owner decision before execution. Work stops after E01.3.8.4 publication.
