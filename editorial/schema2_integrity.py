"""Read-only schema-2 integrity, with no effective authority or trusted ordering.

Structural failures and integrity mismatches raise structured errors. History
ambiguity and ordering limitations remain explicit diagnostics in the result;
they never select a latest record or grant permission.
"""
from dataclasses import dataclass
import hashlib
import json

from . import model as m
from .approval_attestation import ApprovalAttestationError, validate_attestation_digest
from .approval_history import ApprovalDecisionKey
from .graph import validate_reference_graph
from .integrity import HashVerificationError, verify_revision_content_hash
from .rights_binding import RightsBindingResult, validate_all_rights_bindings
from .schema2_model import Schema2ModelError, Schema2Snapshot
from .snapshot_integrity import _companion, _identity, _revision_locations
from .versioned_codec import encode_editorial_versioned

__all__ = (
    'ApprovalEvidenceStatus',
    'ReconsiderationIntegrity',
    'Schema2IntegrityResult',
    'Schema2IntegrityError',
    'canonical_schema2_snapshot_bytes',
    'compute_schema2_snapshot_checksum',
    'validate_schema2_snapshot_integrity',
)

_UNVERIFIED_ASPECTS = (
    'transaction_order', 'identity', 'signatures', 'authority_policy', 'head_anchor',
)
_RECONSIDERABLE_DECISIONS = frozenset((
    m.ApprovalDecision.REJECT, m.ApprovalDecision.REVISE, m.ApprovalDecision.REVOKE,
))


class Schema2IntegrityError(Schema2ModelError):
    """Schema-2 integrity failure with an exact JSON-style Violation path."""


@dataclass(frozen=True)
class ApprovalEvidenceStatus:
    approval_id: str
    authority_status: str


@dataclass(frozen=True)
class ReconsiderationIntegrity:
    approval_id: str
    target_record_id: str | None
    link_status: str
    transaction_order_status: str


@dataclass(frozen=True)
class Schema2IntegrityResult:
    checksum_verified: bool
    revision_count: int
    material_bindings: tuple[RightsBindingResult, ...]
    evidence_count: int
    approval_statuses: tuple[ApprovalEvidenceStatus, ...]
    reconsiderations: tuple[ReconsiderationIntegrity, ...]
    history_diagnostics: tuple[m.Violation, ...]
    ordering_diagnostics: tuple[m.Violation, ...]
    transaction_order_status: str
    unverified_aspects: tuple[str, ...]


def _fail(path, code, message):
    raise Schema2IntegrityError(m.Violation(code, path, message))


def _require_schema2(snapshot):
    if type(snapshot) is not Schema2Snapshot:
        _fail('$', 'TYPE', 'Expected exact Schema2Snapshot')


def canonical_schema2_snapshot_bytes(snapshot) -> bytes:
    """Canonicalize the complete strict schema-2 envelope, minus root checksum.

    The existing versioned encoder confirms model/wire invariants at this
    boundary, including evidence joins/order/uniqueness/declarations. No
    schema-1 checksum, truncated envelope or invented Event action is used.
    """
    _require_schema2(snapshot)
    envelope = json.loads(encode_editorial_versioned(snapshot).decode('utf-8'))
    del envelope['snapshot_checksum']
    return json.dumps(
        envelope, ensure_ascii=False, sort_keys=True,
        separators=(',', ':'), allow_nan=False,
    ).encode('utf-8')


def compute_schema2_snapshot_checksum(snapshot) -> str:
    """Return lowercase SHA-256 without verifying or repairing the stored value."""
    return hashlib.sha256(canonical_schema2_snapshot_bytes(snapshot)).hexdigest()


def _decision_key(record):
    return ApprovalDecisionKey(record.gate, record.policy_version,
                               record.object_ref, record.dependency_digest)


def _history_diagnostics(approvals):
    # All same-key/same-time groups are examined. There is deliberately no
    # max(timestamp), timestamp sorting, latest record, or tie-breaking choice.
    groups = {}
    for index, record in enumerate(approvals):
        groups.setdefault((_decision_key(record), record.timestamp), []).append((index, record))
    diagnostics = []
    for group in groups.values():
        decisions = {record.decision for _, record in group}
        metadata = {(record.actor, record.reason, record.review_declarations)
                    for _, record in group}
        if len(decisions) > 1 or len(metadata) > 1:
            for index, record in group:
                diagnostics.append(m.Violation(
                    'AMBIGUOUS_HISTORY', f'$.approvals[{index}].timestamp',
                    'Same exact decision key and timestamp have conflicting decisions or metadata; '
                    'no transaction order or latest record is established', record.object_ref,
                ))
    return tuple(diagnostics)


def _reconsiderations(approvals, evidence_values):
    by_id = {record.id: record for record in approvals}
    keys_with_negative_decisions = {_decision_key(record) for record in approvals
                                   if record.decision in _RECONSIDERABLE_DECISIONS}
    results = []
    diagnostics = []
    for index, evidence in enumerate(evidence_values):
        record = by_id[evidence.approval_id]  # Join already checked by strict codec.
        path = f'$.approval_authority_evidence[{index}].reconsiders_record_id'
        target_id = evidence.reconsiders_record_id
        if target_id is not None:
            # Self-reference is also rejected by the existing model/codec.
            if target_id == record.id:
                _fail(path, 'RECONSIDERATION_SELF_REFERENCE', 'A record cannot reconsider itself')
            target = by_id.get(target_id)
            if target is None:
                _fail(path, 'RECONSIDERATION_TARGET_MISSING', 'Reconsideration target does not exist')
            if _decision_key(record) != _decision_key(target):
                _fail(path, 'RECONSIDERATION_KEY_MISMATCH',
                      'Reconsideration must preserve gate, policy_version, full object_ref and dependency_digest')
            if target.decision not in _RECONSIDERABLE_DECISIONS:
                _fail(path, 'RECONSIDERATION_DECISION_MISMATCH',
                      'Reconsideration target must record REJECT, REVISE or REVOKE')
            status = 'LINK_CONSISTENT_ORDERING_UNVERIFIED'
            diagnostics.append(m.Violation(
                'UNVERIFIED_ORDERING', path,
                'Link shape, exact key and target decision are consistent; '
                'target precedence and latest applicability require a trusted transaction sequence',
            ))
        elif (record.decision is m.ApprovalDecision.APPROVE and
              _decision_key(record) in keys_with_negative_decisions):
            # A negative record could precede OR follow this APPROVE. Neither
            # absence nor requiredness of a link can be decided from timestamps.
            status = 'RECONSIDERATION_REQUIREMENT_UNVERIFIED'
            diagnostics.append(m.Violation(
                'UNVERIFIED_ORDERING', path,
                'Same-key negative decisions exist; whether this APPROVE requires a '
                'reconsideration link cannot be established without trusted transaction order',
            ))
        else:
            status = 'NO_LINK'
        results.append(ReconsiderationIntegrity(record.id, target_id, status, 'UNVERIFIED_ORDERING'))
    return tuple(results), tuple(diagnostics)


def validate_schema2_snapshot_integrity(snapshot) -> Schema2IntegrityResult:
    """Validate structure, checksum, graph, hashes, rights, digests and links.

    The strict full-envelope checksum mapping first reuses all existing model
    invariants. On structurally valid inputs, integrity failure priority is
    checksum, graph, all revision hashes, rights bindings, attestation digests,
    then reconsideration links. Ambiguity is diagnostic, never a chosen record.
    """
    _require_schema2(snapshot)
    computed = compute_schema2_snapshot_checksum(snapshot)
    base = snapshot.base_snapshot
    if computed != base.snapshot_checksum:
        _fail('$.snapshot_checksum', 'SNAPSHOT_CHECKSUM_MISMATCH',
              'Stored snapshot_checksum does not match the full canonical schema-2 envelope')

    # This is the real unchanged common graph, including real Schema2Events.
    # Its schema-1 checksum is deliberately never evaluated or substituted.
    graph = validate_reference_graph(base)
    locations = _revision_locations(base)
    for revision in base.base.revisions:
        try:
            verify_revision_content_hash(revision, _companion(base, revision))
        except HashVerificationError as error:
            violation = error.violation
            raise HashVerificationError(m.Violation(
                violation.code, f'{locations[_identity(revision.ref)]}.ref.content_hash',
                violation.message, violation.object_ref,
            )) from None
    bindings = validate_all_rights_bindings(base, graph)

    approvals = base.base.approvals
    by_id = {record.id: record for record in approvals}
    for index, evidence in enumerate(snapshot.approval_authority_evidence):
        try:
            validate_attestation_digest(by_id[evidence.approval_id], evidence)
        except ApprovalAttestationError as error:
            violation = error.violation
            suffix = violation.field_path.removeprefix('$.authority_evidence')
            raise Schema2IntegrityError(m.Violation(
                violation.code, f'$.approval_authority_evidence[{index}]{suffix}',
                violation.message, violation.object_ref,
            )) from None

    reconsiderations, ordering_diagnostics = _reconsiderations(
        approvals, snapshot.approval_authority_evidence)
    evidenced = {evidence.approval_id for evidence in snapshot.approval_authority_evidence}
    statuses = tuple(ApprovalEvidenceStatus(
        record.id, 'EVIDENCE_PRESENT_UNVERIFIED' if record.id in evidenced else 'UNAUTHENTICATED_LEGACY',
    ) for record in approvals)
    return Schema2IntegrityResult(
        True, len(base.base.revisions), bindings, len(evidenced), statuses,
        reconsiderations, _history_diagnostics(approvals), ordering_diagnostics,
        'UNVERIFIED_ORDERING', _UNVERIFIED_ASPECTS,
    )
