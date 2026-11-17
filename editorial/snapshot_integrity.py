"""E01.3.6.2 composition of complete read-only snapshot integrity checks."""
from dataclasses import dataclass

from . import model as m
from .current_package import (
    CurrentPackage,
    build_current_package,
    compute_current_dependency_digest,
)
from .graph import validate_reference_graph
from .integrity import HashVerificationError, verify_revision_content_hash
from .rights_binding import RightsBindingResult, validate_all_rights_bindings
from .snapshot_checksum import verify_snapshot_checksum

__all__ = (
    'SnapshotIntegrityResult',
    'CurrentSnapshotIntegrityResult',
    'SnapshotIntegrityError',
    'validate_snapshot_integrity',
    'validate_current_snapshot_integrity',
)


@dataclass(frozen=True)
class SnapshotIntegrityResult:
    checksum_verified: bool
    revision_count: int
    binding_count: int
    material_bindings: tuple[RightsBindingResult, ...]


@dataclass(frozen=True)
class CurrentSnapshotIntegrityResult:
    snapshot_integrity: SnapshotIntegrityResult
    current_package: CurrentPackage
    dependency_digest: str


class SnapshotIntegrityError(m.ModelError):
    """Invalid input at the integration boundary."""


_COLLECTION_NAMES = {
    m.ObjectKind.PRODUCTION: 'production_revisions',
    m.ObjectKind.GENRE_PROFILE: 'profiles',
    m.ObjectKind.CANDIDATE: 'candidates',
    m.ObjectKind.SOURCE: 'sources',
    m.ObjectKind.CLAIM: 'claims',
    m.ObjectKind.SCRIPT: 'scripts',
    m.ObjectKind.SCENE_PLAN: 'scene_plans',
    m.ObjectKind.ASSET: 'assets',
    m.ObjectKind.RIGHTS_REVIEW: 'rights_reviews',
}


def _identity(ref):
    return ref.kind, ref.id, ref.revision


def _fail(path, code, message, ref=None):
    raise SnapshotIntegrityError(m.Violation(code, path, message, ref))


def _revision_locations(snapshot):
    counters = {kind: 0 for kind in _COLLECTION_NAMES}
    locations = {}
    for position, revision in enumerate(snapshot.base.revisions):
        collection = _COLLECTION_NAMES.get(revision.ref.kind)
        if collection is None:
            path = f'$.base.revisions[{position}]'
        else:
            path = f'$.{collection}[{counters[revision.ref.kind]}]'
            counters[revision.ref.kind] += 1
        locations[_identity(revision.ref)] = path
    return locations


def _companion(snapshot, revision):
    values = {
        m.ObjectKind.SOURCE: snapshot.source_details,
        m.ObjectKind.CLAIM: snapshot.claim_reviews,
        m.ObjectKind.RIGHTS_REVIEW: snapshot.rights_details,
    }.get(revision.ref.kind, ())
    matches = tuple(value for value in values
                    if _identity(value.owner_ref) == _identity(revision.ref))
    return matches[0] if len(matches) == 1 else None


def validate_snapshot_integrity(snapshot: m.ContractSnapshot) -> SnapshotIntegrityResult:
    """Validate checksum, graph, every revision hash, then every rights binding.

    Failure priority is deterministic and follows that order. Existing
    structured exception types propagate unchanged. A revision hash error is
    re-raised as HashVerificationError only to attach its exact wire path.
    """
    if type(snapshot) is not m.ContractSnapshot:
        _fail('$', 'TYPE', 'Expected ContractSnapshot')

    verify_snapshot_checksum(snapshot)
    graph = validate_reference_graph(snapshot)

    locations = _revision_locations(snapshot)
    for revision in snapshot.base.revisions:
        try:
            verify_revision_content_hash(revision, _companion(snapshot, revision))
        except HashVerificationError as error:
            violation = error.violation
            raise HashVerificationError(m.Violation(
                violation.code,
                f'{locations[_identity(revision.ref)]}.ref.content_hash',
                violation.message,
                violation.object_ref,
            )) from None

    bindings = validate_all_rights_bindings(snapshot, graph)
    return SnapshotIntegrityResult(True, len(snapshot.base.revisions),
                                   len(bindings), bindings)


def validate_current_snapshot_integrity(snapshot: m.ContractSnapshot, gate,
                                        policy_version: str) -> CurrentSnapshotIntegrityResult:
    """Validate the full snapshot, coherent current package, and its digest."""
    integrity = validate_snapshot_integrity(snapshot)
    current = build_current_package(snapshot, gate)
    digest = compute_current_dependency_digest(snapshot, gate, policy_version)
    return CurrentSnapshotIntegrityResult(integrity, current, digest)
