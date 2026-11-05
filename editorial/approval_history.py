"""E01.3.7.2 deterministic projection of stored approval decision history."""
from dataclasses import dataclass
from enum import Enum
import re

from . import model as m
from .approval_consistency import evaluate_all_approval_consistency
from .package import PackageGate
from .snapshot_integrity import (
    validate_current_snapshot_integrity,
    validate_snapshot_integrity,
)

__all__ = (
    'ApprovalDecisionKey',
    'ApprovalHistoryState',
    'ApprovalHistoryDiagnostic',
    'ApprovalHistoryResult',
    'ApprovalHistoryError',
    'evaluate_approval_history',
    'evaluate_current_approval_history',
)


@dataclass(frozen=True)
class ApprovalDecisionKey:
    gate: str
    policy_version: str
    target_ref: m.RevisionRef
    dependency_digest: str


class ApprovalHistoryState(str, Enum):
    NO_DECISION = 'NO_DECISION'
    RECORDED_APPROVE = 'RECORDED_APPROVE'
    RECORDED_REJECT = 'RECORDED_REJECT'
    RECORDED_REVISE = 'RECORDED_REVISE'
    RECORDED_REVOKE = 'RECORDED_REVOKE'
    AMBIGUOUS_HISTORY = 'AMBIGUOUS_HISTORY'


class ApprovalHistoryDiagnostic(str, Enum):
    CONFLICTING_DECISIONS_SAME_TIMESTAMP = 'CONFLICTING_DECISIONS_SAME_TIMESTAMP'
    NON_EQUIVALENT_RECORDS_SAME_TIMESTAMP = 'NON_EQUIVALENT_RECORDS_SAME_TIMESTAMP'
    EQUIVALENT_DECISIONS_SAME_TIMESTAMP = 'EQUIVALENT_DECISIONS_SAME_TIMESTAMP'


@dataclass(frozen=True)
class ApprovalHistoryResult:
    key: ApprovalDecisionKey
    record_ids: tuple[str, ...]
    latest_record: m.ApprovalRecord | None
    decision: m.ApprovalDecision | None
    state: ApprovalHistoryState
    diagnostics: tuple[ApprovalHistoryDiagnostic, ...]


class ApprovalHistoryError(m.ModelError):
    """Invalid exact historical decision key after snapshot validation."""


_STATES = {
    m.ApprovalDecision.APPROVE: ApprovalHistoryState.RECORDED_APPROVE,
    m.ApprovalDecision.REJECT: ApprovalHistoryState.RECORDED_REJECT,
    m.ApprovalDecision.REVISE: ApprovalHistoryState.RECORDED_REVISE,
    m.ApprovalDecision.REVOKE: ApprovalHistoryState.RECORDED_REVOKE,
}


def _fail(path, code, message):
    raise ApprovalHistoryError(m.Violation(code, path, message))


def _parse_gate(value):
    if type(value) is PackageGate:
        return value.value
    if type(value) is str:
        try:
            return PackageGate(value).value
        except ValueError:
            pass
    _fail('$.gate', 'GATE', 'Expected SCRIPT, SCENES or HANDOFF')


def _key(gate, policy_version, target_ref, dependency_digest):
    parsed_gate = _parse_gate(gate)
    if type(policy_version) is not str or not policy_version.strip():
        _fail('$.policy_version', 'POLICY_VERSION',
              'policy_version must be a nonempty string and is preserved literally')
    if type(target_ref) is not m.RevisionRef:
        _fail('$.target_ref', 'TYPE', 'Expected exact RevisionRef')
    if (type(dependency_digest) is not str or
            re.fullmatch('[0-9a-f]{64}', dependency_digest) is None):
        _fail('$.dependency_digest', 'HASH_FORMAT',
              'Expected 64 lowercase hexadecimal characters')
    return ApprovalDecisionKey(parsed_gate, policy_version, target_ref, dependency_digest)


def _matches(approval, key):
    return (approval.gate == key.gate and
            approval.policy_version == key.policy_version and
            approval.object_ref == key.target_ref and
            approval.dependency_digest == key.dependency_digest)


def _equivalent_metadata(records):
    values = {(record.actor, record.reason, record.review_declarations)
              for record in records}
    return len(values) == 1


def _project(key, records):
    record_ids = tuple(record.id for record in records)
    if not records:
        return ApprovalHistoryResult(
            key, record_ids, None, None, ApprovalHistoryState.NO_DECISION, ())

    latest_at = max(record.timestamp for record in records)
    latest = tuple(record for record in records if record.timestamp == latest_at)
    if len(latest) == 1:
        record = latest[0]
        return ApprovalHistoryResult(
            key, record_ids, record, record.decision, _STATES[record.decision], ())

    decisions = {record.decision for record in latest}
    if len(decisions) != 1:
        return ApprovalHistoryResult(
            key, record_ids, None, None, ApprovalHistoryState.AMBIGUOUS_HISTORY,
            (ApprovalHistoryDiagnostic.CONFLICTING_DECISIONS_SAME_TIMESTAMP,))

    decision = latest[0].decision
    if not _equivalent_metadata(latest):
        return ApprovalHistoryResult(
            key, record_ids, None, decision, ApprovalHistoryState.AMBIGUOUS_HISTORY,
            (ApprovalHistoryDiagnostic.NON_EQUIVALENT_RECORDS_SAME_TIMESTAMP,))

    return ApprovalHistoryResult(
        key, record_ids, None, decision, _STATES[decision],
        (ApprovalHistoryDiagnostic.EQUIVALENT_DECISIONS_SAME_TIMESTAMP,))


def evaluate_approval_history(snapshot: m.ContractSnapshot, gate, policy_version: str,
                              target_ref: m.RevisionRef,
                              dependency_digest: str) -> ApprovalHistoryResult:
    """Project stored decisions for one exact historical key without active refs."""
    validate_snapshot_integrity(snapshot)
    key = _key(gate, policy_version, target_ref, dependency_digest)
    records = tuple(record for record in snapshot.base.approvals if _matches(record, key))
    return _project(key, records)


def evaluate_current_approval_history(snapshot: m.ContractSnapshot, gate,
                                      policy_version: str) -> ApprovalHistoryResult:
    """Project only dependency-consistent records for the exact current package."""
    current = validate_current_snapshot_integrity(snapshot, gate, policy_version)
    consistency = evaluate_all_approval_consistency(snapshot, gate, policy_version)
    matching_ids = {result.approval_id for result in consistency
                    if result.dependency_consistent}
    key = ApprovalDecisionKey(
        current.current_package.gate.value,
        policy_version,
        current.current_package.root_ref,
        current.dependency_digest,
    )
    records = tuple(record for record in snapshot.base.approvals
                    if record.id in matching_ids)
    return _project(key, records)
