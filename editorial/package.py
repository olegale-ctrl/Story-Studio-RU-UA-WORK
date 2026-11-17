"""E01.3.5.1 deterministic historical packages; no digest or active logic."""
from dataclasses import dataclass
from enum import Enum

from . import model as m
from .graph import GraphValidationError, validate_reference_graph
from .integrity import HashVerificationError, verify_revision_content_hash
from .rights_binding import RightsBindingError, RightsBindingResult, validate_rights_binding

__all__ = (
    'PackageGate', 'HistoricalPackage', 'PackageValidationError',
    'build_historical_package',
)

Identity = tuple[m.ObjectKind, str, int]


class PackageGate(str, Enum):
    SCRIPT = 'SCRIPT'
    SCENES = 'SCENES'
    HANDOFF = 'HANDOFF'


@dataclass(frozen=True)
class HistoricalPackage:
    gate: PackageGate
    target_ref: m.RevisionRef
    dependencies: tuple[m.RevisionRef, ...]
    production_refs: tuple[m.RevisionRef, ...]
    profile_refs: tuple[m.RevisionRef, ...]
    material_bindings: tuple[RightsBindingResult, ...]
    integrity_verified: bool


class PackageValidationError(m.ModelError):
    """Historical package failure with a stable code and exact field path."""


_ROOT_KINDS = {
    PackageGate.SCRIPT: m.ObjectKind.SCRIPT,
    PackageGate.SCENES: m.ObjectKind.SCENE_PLAN,
    PackageGate.HANDOFF: m.ObjectKind.SCENE_PLAN,
}
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


def _sort_ref(ref):
    return ref.kind.value, ref.id, ref.revision


def _fail(path, code, message, ref=None):
    raise PackageValidationError(m.Violation(code, path, message, ref))


def _parse_gate(value):
    if type(value) is PackageGate:
        return value
    if type(value) is str:
        try:
            return PackageGate(value)
        except ValueError:
            pass
    _fail('$.gate', 'GATE', 'Expected SCRIPT, SCENES or HANDOFF')


def _locations(snapshot):
    counters = {kind: 0 for kind in _COLLECTION_NAMES}
    result = {}
    for position, revision in enumerate(snapshot.base.revisions):
        kind = revision.ref.kind
        if kind in _COLLECTION_NAMES:
            result[_identity(revision.ref)] = f'$.{_COLLECTION_NAMES[kind]}[{counters[kind]}]'
            counters[kind] += 1
        else:
            result[_identity(revision.ref)] = f'$.base.revisions[{position}]'
    return result


def _companion(snapshot, revision):
    values = {
        m.ObjectKind.SOURCE: snapshot.source_details,
        m.ObjectKind.CLAIM: snapshot.claim_reviews,
        m.ObjectKind.RIGHTS_REVIEW: snapshot.rights_details,
    }.get(revision.ref.kind, ())
    key = _identity(revision.ref)
    matches = tuple(value for value in values if _identity(value.owner_ref) == key)
    return matches[0] if len(matches) == 1 else None


def _closure(graph, root):
    adjacent = {}
    for edge in graph.edges:
        adjacent.setdefault(edge.source, []).append(edge.target)
    root_key = _identity(root.ref)
    found = set()
    pending = list(adjacent.get(root_key, ()))
    while pending:
        key = pending.pop()
        if key == root_key or key in found:
            continue
        found.add(key)
        pending.extend(adjacent.get(key, ()))
    return found


def _check_conflicts(refs):
    versions = {}
    for ref in refs:
        key = ref.kind, ref.id
        revisions = versions.setdefault(key, set())
        revisions.add(ref.revision)
        if len(revisions) > 1:
            values = ', '.join(str(value) for value in sorted(revisions))
            _fail('$.dependencies', 'PACKAGE_VERSION_CONFLICT',
                  f'Package contains revisions {values} of {ref.kind.value}:{ref.id}', ref)


def _roles(gate, target, graph, dependency_keys):
    if gate is PackageGate.SCRIPT:
        script = target
    else:
        script = graph.index.get(_identity(target.script_ref))
        if type(script) is not m.ScriptRevision or script.ref != target.script_ref:
            _fail('$.target_ref', 'ROLE_REF', 'ScenePlan script_ref is not an exact ScriptRevision')
    production = graph.index.get(_identity(script.production_ref))
    if type(production) is not m.ProductionRevision or production.ref != script.production_ref:
        _fail('$.production_refs', 'ROLE_REF', 'Script production_ref is not exact')
    production_refs = (script.production_ref,)
    profile_values = {production.profile_ref, script.brief.profile_ref}
    profile_refs = tuple(sorted(profile_values, key=_sort_ref))
    for path, refs in (('$.production_refs', production_refs), ('$.profile_refs', profile_refs)):
        for ref in refs:
            if _identity(ref) not in dependency_keys:
                _fail(path, 'ROLE_REF_OUTSIDE_CLOSURE',
                      'Role reference must also be present in transitive closure', ref)
            target_value = graph.index.get(_identity(ref))
            if target_value is None or target_value.ref != ref:
                _fail(path, 'ROLE_REF', 'Role reference does not exactly match its target', ref)
    return production_refs, profile_refs


def build_historical_package(snapshot: m.ContractSnapshot, gate,
                             target_ref: m.RevisionRef) -> HistoricalPackage:
    """Build and fully verify one exact historical package.

    This function does not read active refs for package selection, calculate a
    dependency digest, evaluate rights policy, or mutate the snapshot.
    """
    if type(snapshot) is not m.ContractSnapshot:
        _fail('$', 'TYPE', 'Expected ContractSnapshot')
    parsed_gate = _parse_gate(gate)
    if type(target_ref) is not m.RevisionRef:
        _fail('$.target_ref', 'TYPE', 'Expected exact RevisionRef')
    expected_kind = _ROOT_KINDS[parsed_gate]
    if target_ref.kind is not expected_kind:
        _fail('$.target_ref.kind', 'ROOT_KIND',
              f'{parsed_gate.value} requires {expected_kind.value}', target_ref)

    target = next((revision for revision in snapshot.base.revisions
                   if _identity(revision.ref) == _identity(target_ref)), None)
    if target is None:
        _fail('$.target_ref', 'ROOT_NOT_FOUND', 'Exact root is absent from snapshot', target_ref)
    if target.ref != target_ref:
        _fail('$.target_ref.content_hash', 'ROOT_HASH_MISMATCH',
              'Supplied root content_hash differs from exact target ref', target_ref)
    expected_type = m.ScriptRevision if parsed_gate is PackageGate.SCRIPT else m.ScenePlanRevision
    if type(target) is not expected_type:
        _fail('$.target_ref.kind', 'ROOT_KIND', 'Root payload type does not match gate', target_ref)

    try:
        graph = validate_reference_graph(snapshot)
    except GraphValidationError as error:
        violation = error.violation
        _fail(violation.field_path, 'GRAPH_INVALID',
              f'{violation.code}: {violation.message}', violation.object_ref)

    if graph.index.get(_identity(target_ref)) is not target:
        _fail('$.target_ref', 'GRAPH_INVALID', 'Validated graph does not retain exact root object', target_ref)

    dependency_keys = _closure(graph, target)
    dependency_values = tuple(sorted((graph.index[key] for key in dependency_keys),
                                     key=lambda value: _sort_ref(value.ref)))
    dependencies = tuple(value.ref for value in dependency_values)
    _check_conflicts((target.ref, *dependencies))
    production_refs, profile_refs = _roles(parsed_gate, target, graph, dependency_keys)

    locations = _locations(snapshot)
    included = (target, *dependency_values)
    for revision in included:
        companion = _companion(snapshot, revision)
        try:
            verify_revision_content_hash(revision, companion)
        except HashVerificationError as error:
            path = f'{locations[_identity(revision.ref)]}.ref.content_hash'
            _fail(path, 'PACKAGE_HASH_INVALID', error.violation.message, revision.ref)

    bindings = []
    for revision in sorted(included, key=lambda value: _sort_ref(value.ref)):
        if type(revision) in (m.SourceRevision, m.AssetRevision):
            try:
                bindings.append(validate_rights_binding(snapshot, graph, revision))
            except RightsBindingError as error:
                violation = error.violation
                _fail(violation.field_path, 'PACKAGE_RIGHTS_BINDING',
                      f'{violation.code}: {violation.message}', violation.object_ref)

    return HistoricalPackage(parsed_gate, target.ref, dependencies, production_refs,
                             profile_refs, tuple(bindings), True)
