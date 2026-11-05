"""Canonical schema-2 approval binding, without authentication or authority.

All APIs are pure. A matching digest proves only consistency of the supplied
values; even signature-shaped evidence establishes no trust here.
"""
import hashlib
import json

from . import codec as c
from . import model as m
from .schema2_model import ApprovalAuthorityEvidence, Schema2ModelError

__all__ = (
    'ApprovalAttestationError',
    'canonical_attestation_bytes',
    'compute_attestation_digest',
    'validate_attestation_digest',
    'canonical_signed_bytes',
)

_SIGNING_DOMAIN = b'story-studio-approval-attestation-v1\x00'


class ApprovalAttestationError(Schema2ModelError):
    """Attestation failure carrying an immutable Violation and JSON field path."""


def _fail(path, code, message):
    raise ApprovalAttestationError(m.Violation(code, path, message))


def _unicode_fields(value, path):
    """Check exact supplied text, including weak legacy ApprovalRecord fields."""
    if type(value) is str:
        c._unicode(value, path)
    elif type(value) is dict:
        for key, child in value.items():
            _unicode_fields(child, f'{path}.{key}')
    elif type(value) is list:
        for index, child in enumerate(value):
            _unicode_fields(child, f'{path}[{index}]')


def canonical_attestation_bytes(approval, evidence) -> bytes:
    """Return the exact §8.1 payload; the stored digest need not match yet.

Only the supplied pair is bound. Declaration eligibility, policy, history,
snapshot integrity and signature verification belong to separate stages.
"""
    if type(approval) is not m.ApprovalRecord:
        _fail('$.approval_record', 'INVALID_APPROVAL_TYPE', 'Expected exact ApprovalRecord')
    if type(evidence) is not ApprovalAuthorityEvidence:
        _fail('$.authority_evidence', 'INVALID_EVIDENCE_TYPE',
              'Expected exact ApprovalAuthorityEvidence')
    if approval.id != evidence.approval_id:
        _fail('$.authority_evidence.approval_id', 'APPROVAL_ID_MISMATCH',
              'Evidence approval_id must equal ApprovalRecord id')
    if type(approval.object_ref) is not m.RevisionRef:
        _fail('$.approval_record.object_ref', 'INVALID_TYPE', 'Expected exact RevisionRef')
    if type(approval.object_ref.kind) is not m.ObjectKind:
        _fail('$.approval_record.object_ref.kind', 'INVALID_TYPE', 'Expected ObjectKind')
    if type(approval.decision) is not m.ApprovalDecision:
        _fail('$.approval_record.decision', 'INVALID_TYPE', 'Expected ApprovalDecision')
    for value, path in (
        (approval.review_declarations, '$.approval_record.review_declarations'),
        (evidence.declaration_codes, '$.authority_evidence.declaration_codes'),
    ):
        if type(value) is not tuple:
            _fail(path, 'INVALID_TYPE', 'Expected an immutable tuple')

    # Enumerate fields explicitly: future model extensions cannot enter a digest
    # implicitly. Enum values are wire strings; arrays retain their exact order.
    payload = {
        'approval_authority_evidence_schema_version': 1,
        'approval_record': {
            'id': approval.id,
            'gate': approval.gate,
            'object_ref': {
                'kind': approval.object_ref.kind.value,
                'id': approval.object_ref.id,
                'revision': approval.object_ref.revision,
                'content_hash': approval.object_ref.content_hash,
            },
            'dependency_digest': approval.dependency_digest,
            'policy_version': approval.policy_version,
            'actor': approval.actor,
            'timestamp': approval.timestamp,
            'decision': approval.decision.value,
            'reason': approval.reason,
            'review_declarations': list(approval.review_declarations),
        },
        'authority_evidence': {
            'approval_id': evidence.approval_id,
            'principal_id': evidence.principal_id,
            'principal_display_name': evidence.principal_display_name,
            'authority_policy_id': evidence.authority_policy_id,
            'authority_policy_version': evidence.authority_policy_version,
            'review_session_id': evidence.review_session_id,
            'request_id': evidence.request_id,
            'declaration_codes': list(evidence.declaration_codes),
            'attested_at': evidence.attested_at,
            'reconsiders_record_id': evidence.reconsiders_record_id,
        },
    }
    try:
        # Reuse only the unchanged, pure ApprovalRecord wire validator, not a
        # snapshot decoder or an authority/declaration/history evaluator.
        c._APPROVAL(payload['approval_record'], '$.approval_record')
        _unicode_fields(payload, '$')
        return json.dumps(
            payload, ensure_ascii=False, sort_keys=True,
            separators=(',', ':'), allow_nan=False,
        ).encode('utf-8')
    except c.DecodeError as error:
        raise ApprovalAttestationError(error.violation) from None
    except (TypeError, ValueError, OverflowError) as error:
        _fail('$', 'ATTESTATION_SERIALIZATION_ERROR',
              f'Canonical attestation serialization failed ({type(error).__name__})')


def compute_attestation_digest(approval, evidence) -> str:
    """Return lowercase SHA-256 of canonical bytes, without checking stored digest."""
    return hashlib.sha256(canonical_attestation_bytes(approval, evidence)).hexdigest()


def validate_attestation_digest(approval, evidence) -> None:
    """Raise on mismatch; success authenticates neither identity nor authority."""
    computed = compute_attestation_digest(approval, evidence)
    if computed != evidence.attestation_digest:
        _fail('$.authority_evidence.attestation_digest', 'ATTESTATION_DIGEST_MISMATCH',
              'Stored attestation_digest does not match the canonical attestation payload')


def canonical_signed_bytes(approval, evidence) -> bytes:
    """Prepare domain-separated bytes only; do not sign or verify signatures."""
    return _SIGNING_DOMAIN + canonical_attestation_bytes(approval, evidence)
