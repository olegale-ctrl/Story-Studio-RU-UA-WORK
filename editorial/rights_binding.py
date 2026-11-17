"""E01.3.3 pure Source/Asset to RightsReview binding checks."""
from dataclasses import dataclass
from enum import Enum

from . import model as m
from .graph import ReferenceGraph

__all__ = (
    'MaterialBindingState', 'RightsBindingResult', 'RightsBindingError',
    'validate_rights_binding', 'validate_all_rights_bindings',
)

Identity = tuple[m.ObjectKind, str, int]


class MaterialBindingState(str, Enum):
    CONFIRMED = 'confirmed'
    UNCONFIRMED = 'unconfirmed'


@dataclass(frozen=True)
class RightsBindingResult:
    """Structural/material result only; deliberately carries no policy decision."""

    subject_ref: m.RevisionRef
    rights_ref: m.RevisionRef
    structural_match: bool
    material_state: MaterialBindingState


class RightsBindingError(m.ModelError):
    """A structural subject or material mismatch with an exact field path."""


def _identity(ref):
    return ref.kind, ref.id, ref.revision


def _fail(path, code, message, ref=None):
    raise RightsBindingError(m.Violation(code, path, message, ref))


def _subject_path(snapshot, subject):
    kind = subject.ref.kind
    collection = 'sources' if kind is m.ObjectKind.SOURCE else 'assets'
    values = tuple(r for r in snapshot.base.revisions if r.ref.kind is kind)
    try:
        index = values.index(subject)
    except ValueError:
        _fail('$', 'GRAPH_SNAPSHOT_MISMATCH', 'Subject is not in the supplied snapshot', subject.ref)
    return f'$.{collection}[{index}]'


def _companion(values, owner_ref, path, name):
    matches = tuple(value for value in values if _identity(value.owner_ref) == _identity(owner_ref))
    if len(matches) != 1:
        _fail(path, 'COMPANION_BINDING', f'Expected exactly one {name} for the exact revision', owner_ref)
    value = matches[0]
    if value.owner_ref != owner_ref:
        _fail(f'{path}.owner_ref', 'COMPANION_OWNER',
              f'{name} owner_ref must exactly match the revision ref', owner_ref)
    return value


def validate_rights_binding(snapshot: m.ContractSnapshot, graph: ReferenceGraph,
                            subject: m.SourceRevision | m.AssetRevision) -> RightsBindingResult:
    """Validate one historical Source/Asset binding using an E01.3.2 graph.

    CONFIRMED means only that the stored material digest matches. It is never a
    grant, readiness result, expiry check or intended-use policy decision.
    """
    if type(snapshot) is not m.ContractSnapshot:
        _fail('$', 'TYPE', 'Expected ContractSnapshot')
    if type(graph) is not ReferenceGraph:
        _fail('$.graph', 'TYPE', 'Expected a prevalidated ReferenceGraph')
    if type(subject) not in (m.SourceRevision, m.AssetRevision):
        _fail('$.subject', 'TYPE', 'Expected SourceRevision or AssetRevision')

    subject_path = _subject_path(snapshot, subject)
    if graph.index.get(_identity(subject.ref)) is not subject:
        _fail('$.graph', 'GRAPH_SNAPSHOT_MISMATCH',
              'Prevalidated graph does not contain this exact snapshot subject', subject.ref)

    rights = graph.index.get(_identity(subject.rights_ref))
    if type(rights) is not m.RightsReview or rights.ref != subject.rights_ref:
        _fail(f'{subject_path}.rights_ref', 'RIGHTS_TARGET',
              'rights_ref must resolve exactly to RightsReview in the prevalidated graph',
              subject.rights_ref)

    rights_values = tuple(r for r in snapshot.base.revisions
                          if r.ref.kind is m.ObjectKind.RIGHTS_REVIEW)
    try:
        rights_index = rights_values.index(rights)
    except ValueError:
        _fail('$.graph', 'GRAPH_SNAPSHOT_MISMATCH',
              'RightsReview target is not in the supplied snapshot', rights.ref)
    rights_path = f'$.rights_reviews[{rights_index}]'
    details = _companion(snapshot.rights_details, rights.ref, rights_path, 'RightsDetails')

    expected_kind = subject.ref.kind
    if details.subject_kind is not expected_kind:
        _fail(f'{rights_path}.subject_kind', 'SUBJECT_KIND_MISMATCH',
              f'RightsReview describes {details.subject_kind.value}, expected {expected_kind.value}',
              rights.ref)
    if rights.subject_id != subject.ref.id:
        _fail(f'{rights_path}.subject_id', 'SUBJECT_ID_MISMATCH',
              'RightsReview subject_id differs from the bound object UUID', rights.ref)
    if rights.subject_revision != subject.ref.revision:
        _fail(f'{rights_path}.subject_revision', 'SUBJECT_REVISION_MISMATCH',
              'RightsReview subject_revision differs from the bound object revision', rights.ref)

    if type(subject) is m.SourceRevision:
        source_details = _companion(snapshot.source_details, subject.ref,
                                    subject_path, 'SourceDetails')
        material_digest = source_details.material_digest
        if material_digest is None:
            return RightsBindingResult(subject.ref, rights.ref, True,
                                       MaterialBindingState.UNCONFIRMED)
        material_path = f'{subject_path}.material_digest'
    else:
        material_digest = subject.sha256
        material_path = f'{subject_path}.sha256'

    if rights.material_digest != material_digest:
        _fail(material_path, 'MATERIAL_DIGEST_MISMATCH',
              'Subject material digest differs from RightsReview.material_digest', subject.ref)
    return RightsBindingResult(subject.ref, rights.ref, True, MaterialBindingState.CONFIRMED)


def validate_all_rights_bindings(snapshot: m.ContractSnapshot,
                                 graph: ReferenceGraph) -> tuple[RightsBindingResult, ...]:
    """Validate every historical SourceRevision and AssetRevision in tuple order."""
    if type(snapshot) is not m.ContractSnapshot:
        _fail('$', 'TYPE', 'Expected ContractSnapshot')
    subjects = tuple(revision for revision in snapshot.base.revisions
                     if type(revision) in (m.SourceRevision, m.AssetRevision))
    return tuple(validate_rights_binding(snapshot, graph, subject) for subject in subjects)
