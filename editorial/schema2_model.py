"""Immutable schema-2 value models and local validation only.

This module deliberately provides no wire codec, hashing, migration, authority
evaluation, persistence, clock, filesystem, or network behavior.
"""
from __future__ import annotations

import base64
from dataclasses import dataclass
from datetime import datetime
import re
from uuid import UUID

from . import model as m
from .package import PackageGate

__all__ = (
    'SCRIPT_APPROVE_DECLARATION_CODES',
    'SCENES_APPROVE_DECLARATION_CODES',
    'HANDOFF_APPROVE_DECLARATION_CODES',
    'NON_APPROVE_DECLARATION_CODES',
    'ApprovalAuthorityEvidence',
    'Schema2Event',
    'Schema2ModelError',
    'Schema2Snapshot',
    'required_declaration_codes',
)


SCRIPT_APPROVE_DECLARATION_CODES = (
    'SCRIPT_EXACT_TEXT_REVIEWED',
    'MATERIAL_CLAIMS_REVIEWED',
    'EVIDENCE_AND_QUALIFICATIONS_REVIEWED',
    'FICTION_DISCLOSURES_REVIEWED',
    'LANGUAGE_ALIGNMENT_REVIEWED',
    'SOURCE_RIGHTS_STATUS_ACKNOWLEDGED',
    'NO_UNSUPPORTED_REVIEW_CLAIM',
)
SCENES_APPROVE_DECLARATION_CODES = (
    'CURRENT_SCRIPT_DECISION_REVIEWED',
    'SCENE_TEXT_COVERAGE_REVIEWED',
    'SCENE_VISUAL_MEANING_REVIEWED',
    'ASSET_PROVENANCE_VISIBLE',
    'ASSET_RIGHTS_STATUS_ACKNOWLEDGED',
    'DISCLOSURES_VISIBLE_IN_SCENES',
    'NO_UNSUPPORTED_REVIEW_CLAIM',
)
HANDOFF_APPROVE_DECLARATION_CODES = (
    'EDITORIAL_SCRIPT_AND_SCENES_REVIEWED',
    'EDITORIAL_ASSET_SET_REVIEWED',
    'CURRENT_RECORDED_DECISIONS_VISIBLE',
    'RIGHTS_STATUS_ACKNOWLEDGED_NOT_GRANTED',
    'HANDOFF_IS_EDITORIAL_ONLY',
    'NO_RENDER_OR_EXPORT_AUTHORIZATION',
    'NO_UNSUPPORTED_REVIEW_CLAIM',
)
NON_APPROVE_DECLARATION_CODES = ('NO_UNSUPPORTED_REVIEW_CLAIM',)

_APPROVE_CODES = {
    PackageGate.SCRIPT: SCRIPT_APPROVE_DECLARATION_CODES,
    PackageGate.SCENES: SCENES_APPROVE_DECLARATION_CODES,
    PackageGate.HANDOFF: HANDOFF_APPROVE_DECLARATION_CODES,
}
_ALL_DECLARATION_CODES = frozenset(
    code for values in _APPROVE_CODES.values() for code in values
)
_UUID_RE = re.compile(
    r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'
)
_WINDOWS_PRINCIPAL_RE = re.compile(r'windows-sid:S-[0-9]+(?:-[0-9]+)+')
_POSIX_PRINCIPAL_RE = re.compile(
    r'posix-uid:(?:0|[1-9][0-9]*)@machine:[0-9a-f]{32}'
)
_UTC_SECONDS_RE = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z')
_SHA256_RE = re.compile(r'[0-9a-f]{64}')
_KEY_ID_RE = re.compile(r'[A-Za-z0-9][A-Za-z0-9._:-]{0,127}')
_BASE64URL_RE = re.compile(r'[A-Za-z0-9_-]+')
_MAX_EVIDENCE = 10_000


class Schema2ModelError(m.ModelError):
    """Invalid schema-2 model value with a stable code and field path."""


@dataclass(frozen=True)
class Schema2Event(m.Event):
    """The schema-2-only migration event; legacy actions remain ``m.Event``."""

    def __post_init__(self) -> None:
        m._id(self.id, 'id')
        m._contract_text(self.actor, 'actor')
        m._utc(self.at, 'at')
        m._choice(self.action, ('schema_migrated',), 'action')
        m._tuple(self.refs, m.RevisionRef, 'refs')
        m._contract_text(self.reason, 'reason')
        m._optional_text(self.error_code, 'error_code')


def _fail(path: str, code: str, message: str) -> None:
    raise Schema2ModelError(m.Violation(code, path, message))


def _uuid(value: object, path: str) -> None:
    if type(value) is not str or _UUID_RE.fullmatch(value) is None:
        _fail(path, 'INVALID_UUID', 'Expected a canonical lowercase UUID')
    try:
        parsed = UUID(value)
    except ValueError:
        _fail(path, 'INVALID_UUID', 'Expected a canonical lowercase UUID')
    if str(parsed) != value:
        _fail(path, 'INVALID_UUID', 'Expected a canonical lowercase UUID')


def _unicode_text(value: object, path: str, maximum: int) -> None:
    if type(value) is not str or not value or len(value) > maximum:
        _fail(path, 'INVALID_TEXT', f'Expected 1 to {maximum} Unicode code points')
    if any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        _fail(path, 'INVALID_TEXT', 'Unicode surrogate code points are forbidden')


def _timestamp(value: object, path: str) -> None:
    if type(value) is not str or _UTC_SECONDS_RE.fullmatch(value) is None:
        _fail(path, 'INVALID_TIMESTAMP', 'Expected UTC seconds YYYY-MM-DDTHH:MM:SSZ')
    try:
        datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        _fail(path, 'INVALID_TIMESTAMP', 'Expected a valid UTC calendar timestamp')


def _canonical_signature(value: object, path: str) -> None:
    if type(value) is not str or _BASE64URL_RE.fullmatch(value) is None:
        _fail(path, 'INVALID_SIGNATURE_FORMAT', 'Expected canonical unpadded base64url')
    try:
        decoded = base64.b64decode(value + '=' * (-len(value) % 4), altchars=b'-_', validate=True)
    except (ValueError, base64.binascii.Error):
        _fail(path, 'INVALID_SIGNATURE_FORMAT', 'Expected canonical unpadded base64url')
    canonical = base64.urlsafe_b64encode(decoded).decode('ascii').rstrip('=')
    if canonical != value or len(decoded) != 64:
        _fail(path, 'INVALID_SIGNATURE_FORMAT', 'Expected canonical base64url for exactly 64 bytes')


def required_declaration_codes(gate, decision) -> tuple[str, ...]:
    """Return the closed schema-2 declaration sequence for a gate/decision."""
    if type(gate) is str:
        try:
            gate = PackageGate(gate)
        except ValueError:
            _fail('$.gate', 'INVALID_GATE', 'Expected SCRIPT, SCENES, or HANDOFF')
    elif type(gate) is not PackageGate:
        _fail('$.gate', 'INVALID_GATE', 'Expected PackageGate or its exact string value')

    if type(decision) is str:
        try:
            decision = m.ApprovalDecision(decision)
        except ValueError:
            _fail('$.decision', 'INVALID_DECISION', 'Expected a supported approval decision')
    elif type(decision) is not m.ApprovalDecision:
        _fail('$.decision', 'INVALID_DECISION', 'Expected ApprovalDecision or its exact string value')

    return _APPROVE_CODES[gate] if decision is m.ApprovalDecision.APPROVE else NON_APPROVE_DECLARATION_CODES


@dataclass(frozen=True)
class ApprovalAuthorityEvidence:
    approval_id: str
    principal_id: str
    principal_display_name: str
    authority_policy_id: str
    authority_policy_version: str
    review_session_id: str
    request_id: str
    declaration_codes: tuple[str, ...]
    attested_at: str
    reconsiders_record_id: str | None
    attestation_digest: str
    signing_key_id: str | None
    signature_algorithm: str | None
    signature: str | None

    def __post_init__(self) -> None:
        for name in ('approval_id', 'authority_policy_id', 'review_session_id', 'request_id'):
            _uuid(getattr(self, name), f'$.{name}')
        if self.reconsiders_record_id is not None:
            _uuid(self.reconsiders_record_id, '$.reconsiders_record_id')
            if self.reconsiders_record_id == self.approval_id:
                _fail('$.reconsiders_record_id', 'SELF_REFERENCE', 'Evidence cannot reconsider its own approval')

        if (type(self.principal_id) is not str or
                (_WINDOWS_PRINCIPAL_RE.fullmatch(self.principal_id) is None and
                 _POSIX_PRINCIPAL_RE.fullmatch(self.principal_id) is None)):
            _fail('$.principal_id', 'INVALID_PRINCIPAL', 'Expected a canonical Windows SID or POSIX UID principal')
        _unicode_text(self.principal_display_name, '$.principal_display_name', 256)
        _unicode_text(self.authority_policy_version, '$.authority_policy_version', 128)

        if type(self.declaration_codes) is not tuple:
            _fail('$.declaration_codes', 'INVALID_DECLARATION', 'Expected an immutable tuple')
        if not self.declaration_codes or len(self.declaration_codes) > 16:
            _fail('$.declaration_codes', 'INVALID_DECLARATION', 'Expected 1 to 16 declaration codes')
        seen = set()
        for index, code in enumerate(self.declaration_codes):
            path = f'$.declaration_codes[{index}]'
            if type(code) is not str or code not in _ALL_DECLARATION_CODES:
                _fail(path, 'INVALID_DECLARATION', 'Unknown schema-2 declaration code')
            if code in seen:
                _fail(path, 'DUPLICATE_DECLARATION', 'Declaration code is duplicated')
            seen.add(code)

        _timestamp(self.attested_at, '$.attested_at')
        if type(self.attestation_digest) is not str or _SHA256_RE.fullmatch(self.attestation_digest) is None:
            _fail('$.attestation_digest', 'INVALID_DIGEST', 'Expected 64 lowercase hexadecimal characters')

        signature_values = (self.signing_key_id, self.signature_algorithm, self.signature)
        present = tuple(value is not None for value in signature_values)
        if any(present) and not all(present):
            _fail('$.signature', 'INCOMPLETE_SIGNATURE', 'Signature fields must be all null or all present')
        if all(present):
            if type(self.signing_key_id) is not str or _KEY_ID_RE.fullmatch(self.signing_key_id) is None:
                _fail('$.signing_key_id', 'INVALID_SIGNATURE_FORMAT', 'Invalid signing key identifier')
            if type(self.signature_algorithm) is not str or self.signature_algorithm != 'ed25519':
                _fail('$.signature_algorithm', 'INVALID_SIGNATURE_FORMAT', 'Expected ed25519')
            _canonical_signature(self.signature, '$.signature')


@dataclass(frozen=True)
class Schema2Snapshot:
    """Temporary in-memory schema-2 aggregate, not a schema-2 wire envelope."""

    base_snapshot: m.ContractSnapshot
    approval_authority_evidence: tuple[ApprovalAuthorityEvidence, ...]
    editorial_schema_version: int = 2

    def __post_init__(self) -> None:
        if type(self.base_snapshot) is not m.ContractSnapshot:
            _fail('$.base_snapshot', 'INVALID_TYPE', 'Expected ContractSnapshot')
        if type(self.editorial_schema_version) is not int or self.editorial_schema_version != 2:
            _fail('$.editorial_schema_version', 'SCHEMA_VERSION_UNSUPPORTED', 'Expected integer 2')
        values = self.approval_authority_evidence
        if type(values) is not tuple:
            _fail('$.approval_authority_evidence', 'INVALID_TYPE', 'Expected an immutable tuple')
        if len(values) > _MAX_EVIDENCE:
            _fail('$.approval_authority_evidence', 'EXCESSIVE_COLLECTION_SIZE', 'At most 10000 evidence objects are allowed')
        for index, value in enumerate(values):
            if type(value) is not ApprovalAuthorityEvidence:
                _fail(f'$.approval_authority_evidence[{index}]', 'INVALID_TYPE', 'Expected ApprovalAuthorityEvidence')

        approvals = self.base_snapshot.base.approvals
        if len(values) > len(approvals):
            _fail('$.approval_authority_evidence', 'EXCESSIVE_COLLECTION_SIZE', 'Evidence cannot outnumber approvals')
        approval_positions = {approval.id: index for index, approval in enumerate(approvals)}
        approvals_by_id = {approval.id: approval for approval in approvals}
        seen_approval_ids = set()
        seen_sessions = set()
        seen_requests = set()
        positions = []
        for index, value in enumerate(values):
            path = f'$.approval_authority_evidence[{index}]'
            if value.approval_id in seen_approval_ids:
                _fail(f'{path}.approval_id', 'DUPLICATE_EVIDENCE', 'Approval already has authority evidence')
            if value.review_session_id in seen_sessions:
                _fail(f'{path}.review_session_id', 'DUPLICATE_SESSION', 'Review session is duplicated')
            if value.request_id in seen_requests:
                _fail(f'{path}.request_id', 'DUPLICATE_REQUEST', 'Request is duplicated')
            if value.approval_id not in approval_positions:
                _fail(f'{path}.approval_id', 'INVALID_EVIDENCE_ORDER', 'Evidence must link an existing approval')
            linked = approvals_by_id[value.approval_id]
            expected_codes = required_declaration_codes(linked.gate, linked.decision)
            if value.declaration_codes != expected_codes:
                _fail(f'{path}.declaration_codes', 'INVALID_DECLARATION',
                      'Declarations must exactly match the linked gate and decision')
            seen_approval_ids.add(value.approval_id)
            seen_sessions.add(value.review_session_id)
            seen_requests.add(value.request_id)
            positions.append(approval_positions[value.approval_id])
        if positions != sorted(positions):
            _fail('$.approval_authority_evidence', 'INVALID_EVIDENCE_ORDER', 'Evidence must follow approval order while allowing legacy gaps')
