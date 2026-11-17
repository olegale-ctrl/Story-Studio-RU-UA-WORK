"""E01.3.1 canonical revision hashes; no graph, storage or checksum work."""
import hashlib
import json

from . import model as m
from .codec import _wire_revision

__all__ = (
    'HashVerificationError',
    'canonical_revision_bytes',
    'compute_revision_content_hash',
    'verify_revision_content_hash',
)

SCHEMA_VERSION = 1


class HashVerificationError(m.ModelError):
    """Invalid hash input or supplied content hash, with a structured path."""


def _fail(path, code, message, revision=None):
    ref = revision.ref if isinstance(revision, m.EditorialRevision) else None
    raise HashVerificationError(m.Violation(code, path, message, ref))


def _joined_record(revision, companion):
    if not isinstance(revision, m.EditorialRevision):
        _fail('$', 'TYPE', 'Expected an EditorialRevision')
    try:
        record = _wire_revision(revision)
    except (AttributeError, TypeError, ValueError) as error:
        _fail('$', 'INVALID_REVISION', f'Cannot map revision payload: {error}', revision)

    expected = None
    if type(revision) is m.SourceRevision:
        expected = m.SourceDetails
        if type(companion) is expected:
            record.update({'source_type': companion.source_type, 'author': companion.author,
                'publisher': companion.publisher, 'published_at': companion.published_at,
                'accessed_at': companion.accessed_at, 'access_notes': companion.access_notes,
                'reliability_notes': companion.reliability_notes,
                'material_digest': companion.material_digest})
    elif type(revision) is m.ClaimRevision:
        expected = m.ClaimReview
        if type(companion) is expected:
            record.update({'review_status': companion.review_status,
                'qualification': companion.qualification, 'reviewer': companion.reviewer,
                'reviewed_at': companion.reviewed_at, 'reason': companion.reason})
    elif type(revision) is m.RightsReview:
        expected = m.RightsDetails
        if type(companion) is expected:
            record.update({'subject_kind': companion.subject_kind.value,
                           'expires_at': companion.expires_at})

    if expected is not None:
        if type(companion) is not expected:
            _fail('$.companion', 'MISSING_COMPANION',
                  f'{expected.__name__} is required for {type(revision).__name__}', revision)
        if companion.owner_ref != revision.ref:
            _fail('$.companion.owner_ref', 'COMPANION_OWNER',
                  'Companion owner_ref must exactly match the revision ref', revision)
    elif companion is not None:
        _fail('$.companion', 'UNEXPECTED_COMPANION',
              f'{type(revision).__name__} has no companion payload', revision)
    return record


def _semantic_payload(revision, companion):
    record = _joined_record(revision, companion)
    ref = record.pop('ref')
    # AssetRevision.kind is the media type in E01.2 wire JSON. In the flat
    # semantic payload the common identity owns "kind", so schema 1 gives the
    # media field the unambiguous hash-only name "asset_kind".
    if type(revision) is m.AssetRevision:
        record['asset_kind'] = record.pop('kind')
    payload = {'editorial_schema_version': SCHEMA_VERSION,
               'kind': ref['kind'], 'id': ref['id'], 'revision': ref['revision'], **record}

    # Closed schema-1 audit exclusions. These fields remain in snapshot JSON.
    if type(revision) is m.ProductionRevision:
        payload.pop('created_at')
    elif type(revision) is m.SourceRevision:
        payload.pop('accessed_at')
    elif type(revision) is m.ClaimRevision:
        payload.pop('reviewed_at')
        for evidence in payload['evidence_links']:
            evidence.pop('reviewed_at')
    elif type(revision) is m.RightsReview:
        payload.pop('reviewed_at')
    return payload


def canonical_revision_bytes(revision: m.EditorialRevision, companion=None) -> bytes:
    """Return schema-1 canonical semantic payload bytes for one revision.

    SourceRevision, ClaimRevision and RightsReview require their exact typed
    companion. The function does not resolve references or mutate any object.
    """
    payload = _semantic_payload(revision, companion)
    try:
        return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(',', ':'),
                          allow_nan=False).encode('utf-8')
    except (TypeError, ValueError, UnicodeEncodeError) as error:
        _fail('$', 'CANONICAL_JSON', f'Cannot encode canonical semantic payload: {error}', revision)


def compute_revision_content_hash(revision: m.EditorialRevision, companion=None) -> str:
    """Compute lowercase SHA-256 hex over canonical_revision_bytes."""
    return hashlib.sha256(canonical_revision_bytes(revision, companion)).hexdigest()


def verify_revision_content_hash(revision: m.EditorialRevision, companion=None) -> None:
    """Raise HashVerificationError unless supplied ref.content_hash is exact."""
    actual = compute_revision_content_hash(revision, companion)
    if revision.ref.content_hash != actual:
        _fail('$.ref.content_hash', 'CONTENT_HASH_MISMATCH',
              f'Supplied content_hash {revision.ref.content_hash} does not match computed {actual}',
              revision)
