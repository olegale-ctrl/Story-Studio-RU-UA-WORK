"""E01.3.7.1 dependency consistency for stored ApprovalRecord values."""
from dataclasses import dataclass
from enum import Enum

from . import model as m
from .snapshot_integrity import (
    CurrentSnapshotIntegrityResult,
    validate_current_snapshot_integrity,
)

__all__ = (
    'ApprovalConsistencyReason',
    'ApprovalConsistencyResult',
    'ApprovalConsistencyError',
    'evaluate_approval_consistency',
    'evaluate_all_approval_consistency',
)


class ApprovalConsistencyReason(str, Enum):
    GATE_MISMATCH = 'GATE_MISMATCH'
    POLICY_VERSION_MISMATCH = 'POLICY_VERSION_MISMATCH'
    TARGET_REF_MISMATCH = 'TARGET_REF_MISMATCH'
    DEPENDENCY_DIGEST_MISMATCH = 'DEPENDENCY_DIGEST_MISMATCH'


@dataclass(frozen=True)
class ApprovalConsistencyResult:
    approval_id: str
    decision: m.ApprovalDecision
    dependency_consistent: bool
    reasons: tuple[ApprovalConsistencyReason, ...]
    current_target_ref: m.RevisionRef
    current_dependency_digest: str


class ApprovalConsistencyError(m.ModelError):
    """Invalid approval lookup input after current snapshot validation."""


def _fail(path, code, message):
    raise ApprovalConsistencyError(m.Violation(code, path, message))


def _evaluate(approval: m.ApprovalRecord,
              current: CurrentSnapshotIntegrityResult,
              policy_version: str) -> ApprovalConsistencyResult:
    gate = current.current_package.gate.value
    target = current.current_package.root_ref
    digest = current.dependency_digest
    reasons = []
    if approval.gate != gate:
        reasons.append(ApprovalConsistencyReason.GATE_MISMATCH)
    if approval.policy_version != policy_version:
        reasons.append(ApprovalConsistencyReason.POLICY_VERSION_MISMATCH)
    if approval.object_ref != target:
        reasons.append(ApprovalConsistencyReason.TARGET_REF_MISMATCH)
    if approval.dependency_digest != digest:
        reasons.append(ApprovalConsistencyReason.DEPENDENCY_DIGEST_MISMATCH)
    values = tuple(reasons)
    return ApprovalConsistencyResult(
        approval.id,
        approval.decision,
        not values,
        values,
        target,
        digest,
    )


def evaluate_approval_consistency(snapshot: m.ContractSnapshot, approval_id: str,
                                  gate, policy_version: str) -> ApprovalConsistencyResult:
    """Evaluate one stored approval after complete current-snapshot validation."""
    current = validate_current_snapshot_integrity(snapshot, gate, policy_version)
    if type(approval_id) is not str or not approval_id:
        _fail('$.approval_id', 'APPROVAL_ID', 'approval_id must be a nonempty string')
    approval = next((item for item in snapshot.base.approvals
                     if item.id == approval_id), None)
    if approval is None:
        _fail('$.approval_id', 'APPROVAL_NOT_FOUND',
              'No ApprovalRecord with this id exists in the validated snapshot')
    return _evaluate(approval, current, policy_version)


def evaluate_all_approval_consistency(snapshot: m.ContractSnapshot, gate,
                                      policy_version: str) -> tuple[ApprovalConsistencyResult, ...]:
    """Evaluate every stored approval in snapshot order after one validation."""
    current = validate_current_snapshot_integrity(snapshot, gate, policy_version)
    return tuple(_evaluate(approval, current, policy_version)
                 for approval in snapshot.base.approvals)
