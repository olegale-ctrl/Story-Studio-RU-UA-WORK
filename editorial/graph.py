"""E01.3.2 exact in-snapshot reference graph validation."""
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType

from . import model as m
from .integrity import HashVerificationError, verify_revision_content_hash

__all__ = (
    'DependencyEdge', 'ReferenceGraph', 'GraphValidationError',
    'build_revision_index', 'validate_reference_graph',
)

Identity = tuple[m.ObjectKind, str, int]

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
_EXPECTED_TYPES = dict(m._REVISION_TYPES)


class GraphValidationError(m.ModelError):
    """Deterministic graph failure with a JSON-style field path."""


def _identity(ref):
    return ref.kind, ref.id, ref.revision


def _display(key):
    return f'{key[0].value}:{key[1]}@{key[2]}'


def _fail(path, code, message, ref=None):
    raise GraphValidationError(m.Violation(code, path, message, ref))


@dataclass(frozen=True)
class DependencyEdge:
    source: Identity
    target: Identity
    field_path: str


@dataclass(frozen=True)
class ReferenceGraph:
    index: Mapping[Identity, m.EditorialRevision]
    edges: tuple[DependencyEdge, ...]

    def resolve(self, reference: m.RevisionRef):
        """Return the already-validated exact in-snapshot target."""
        return self.index[_identity(reference)]


def _index_and_locations(snapshot):
    if type(snapshot) is not m.ContractSnapshot:
        _fail('$', 'TYPE', 'Expected ContractSnapshot')
    index = {}
    locations = {}
    counters = {kind: 0 for kind in _COLLECTION_NAMES}
    for position, revision in enumerate(snapshot.base.revisions):
        if not isinstance(revision, m.EditorialRevision):
            _fail(f'$.base.revisions[{position}]', 'UNSUPPORTED_REVISION',
                  'Index accepts only concrete EditorialRevision payloads')
        kind = revision.ref.kind
        collection = _COLLECTION_NAMES.get(kind)
        path = (f'$.base.revisions[{position}]' if collection is None else
                f'$.{collection}[{counters[kind]}]')
        if collection is not None:
            counters[kind] += 1
        expected = _EXPECTED_TYPES.get(kind)
        if expected is None or type(revision) is not expected:
            _fail(f'{path}.ref.kind', 'REVISION_KIND_MISMATCH',
                  'Revision class does not match its declared ObjectKind', revision.ref)
        key = _identity(revision.ref)
        if key in index:
            _fail(f'{path}.ref', 'DUPLICATE_IDENTITY',
                  f'Duplicate exact revision identity {_display(key)}', revision.ref)
        if kind is m.ObjectKind.PRODUCTION and revision.ref.id != snapshot.base.production_id:
            _fail(f'{path}.ref.id', 'FOREIGN_PRODUCTION',
                  'ProductionRevision id must equal snapshot production_id', revision.ref)
        index[key] = revision
        locations[key] = path
    return index, locations


def build_revision_index(snapshot: m.ContractSnapshot):
    """Build a read-only exact `(kind,id,revision)` index for this snapshot."""
    index, _ = _index_and_locations(snapshot)
    return MappingProxyType(index)


def _references(revision, path):
    """Yield (ref, field path, normative target kind) in contract order."""
    if type(revision) is m.ProductionRevision:
        yield revision.profile_ref, f'{path}.profile_ref', m.ObjectKind.GENRE_PROFILE
    elif type(revision) is m.CandidateRevision:
        for i, ref in enumerate(revision.source_refs):
            yield ref, f'{path}.source_refs[{i}]', m.ObjectKind.SOURCE
    elif type(revision) is m.SourceRevision:
        yield revision.rights_ref, f'{path}.rights_ref', m.ObjectKind.RIGHTS_REVIEW
    elif type(revision) is m.ClaimRevision:
        for i, evidence in enumerate(revision.evidence_links):
            yield evidence.source_ref, f'{path}.evidence_links[{i}].source_ref', m.ObjectKind.SOURCE
    elif type(revision) is m.ScriptRevision:
        yield revision.production_ref, f'{path}.production_ref', m.ObjectKind.PRODUCTION
        yield revision.candidate_ref, f'{path}.candidate_ref', m.ObjectKind.CANDIDATE
        yield revision.brief.profile_ref, f'{path}.brief.profile_ref', m.ObjectKind.GENRE_PROFILE
        for i, ref in enumerate(revision.brief.must_include_claim_refs):
            yield ref, f'{path}.brief.must_include_claim_refs[{i}]', m.ObjectKind.CLAIM
        for i, segment in enumerate(revision.segments):
            for j, ref in enumerate(segment.claim_refs):
                yield ref, f'{path}.segments[{i}].claim_refs[{j}]', m.ObjectKind.CLAIM
        for i, ref in enumerate(revision.claim_refs):
            yield ref, f'{path}.claim_refs[{i}]', m.ObjectKind.CLAIM
    elif type(revision) is m.ScenePlanRevision:
        yield revision.script_ref, f'{path}.script_ref', m.ObjectKind.SCRIPT
        for i, scene in enumerate(revision.scenes):
            if scene.asset_ref is not None:
                yield scene.asset_ref, f'{path}.scenes[{i}].asset_ref', m.ObjectKind.ASSET
    elif type(revision) is m.AssetRevision:
        yield revision.rights_ref, f'{path}.rights_ref', m.ObjectKind.RIGHTS_REVIEW
        if revision.script_ref is not None:
            yield revision.script_ref, f'{path}.script_ref', m.ObjectKind.SCRIPT
    # GenreProfile and RightsReview have no dependency edges in schema 1.


def _resolve_existing(index, reference, path):
    key = _identity(reference)
    target = index.get(key)
    if target is not None:
        return target
    same_id = tuple(k for k in index if k[1] == reference.id)
    if any(k[0] is reference.kind for k in same_id):
        _fail(path, 'TARGET_REVISION_MISMATCH',
              f'No exact revision {reference.revision} for {reference.kind.value}:{reference.id}', reference)
    if same_id:
        kinds = ', '.join(sorted({k[0].value for k in same_id}))
        _fail(f'{path}.kind', 'TARGET_KIND_MISMATCH',
              f'UUID exists only with different kind(s): {kinds}', reference)
    _fail(path, 'MISSING_TARGET', f'No target {_display(key)} in this snapshot', reference)


def _detect_cycle(keys, edges):
    adjacent = {key: [] for key in keys}
    for edge in edges:
        adjacent[edge.source].append(edge)
    state = {}
    for root in keys:
        if state.get(root, 0) != 0:
            continue
        state[root] = 1
        path = [root]
        frames = [[root, 0]]
        while frames:
            key, offset = frames[-1]
            if offset == len(adjacent[key]):
                state[key] = 2
                frames.pop()
                path.pop()
                continue
            edge = adjacent[key][offset]
            frames[-1][1] += 1
            target = edge.target
            if state.get(target, 0) == 0:
                state[target] = 1
                path.append(target)
                frames.append([target, 0])
            elif state.get(target) == 1:
                start = path.index(target)
                cycle = path[start:] + [target]
                _fail(edge.field_path, 'DEPENDENCY_CYCLE',
                      'Dependency cycle: ' + ' -> '.join(_display(item) for item in cycle))


def validate_reference_graph(snapshot: m.ContractSnapshot) -> ReferenceGraph:
    """Validate exact local refs/hashes and return immutable dependency graph."""
    index, locations = _index_and_locations(snapshot)
    edge_specs = []
    edges = []
    for key, revision in index.items():
        for reference, path, expected_kind in _references(revision, locations[key]):
            target = _resolve_existing(index, reference, path)
            target_key = _identity(target.ref)
            edges.append(DependencyEdge(key, target_key, path))
            edge_specs.append((reference, path, expected_kind, target))

    # Cycle reporting precedes other errors when a malformed ref creates both.
    _detect_cycle(tuple(index), tuple(edges))

    companion_maps = {
        m.ObjectKind.SOURCE: {_identity(v.owner_ref): v for v in snapshot.source_details},
        m.ObjectKind.CLAIM: {_identity(v.owner_ref): v for v in snapshot.claim_reviews},
        m.ObjectKind.RIGHTS_REVIEW: {_identity(v.owner_ref): v for v in snapshot.rights_details},
    }
    verified = set()

    def validate_target(reference, path, expected_kind=None):
        target = _resolve_existing(index, reference, path)
        key = _identity(target.ref)
        if expected_kind is not None and reference.kind is not expected_kind:
            _fail(f'{path}.kind', 'REFERENCE_KIND_MISMATCH',
                  f'Field requires {expected_kind.value}, got {reference.kind.value}', reference)
        if expected_kind is m.ObjectKind.PRODUCTION and target.ref.id != snapshot.base.production_id:
            _fail(f'{path}.id', 'FOREIGN_PRODUCTION',
                  'production_ref must target this snapshot production_id', reference)
        if reference.content_hash != target.ref.content_hash:
            _fail(f'{path}.content_hash', 'REFERENCE_HASH_MISMATCH',
                  'Reference content_hash differs from exact target ref', reference)
        if key not in verified:
            companion = companion_maps.get(target.ref.kind, {}).get(key)
            try:
                verify_revision_content_hash(target, companion)
            except HashVerificationError as error:
                _fail(f'{locations[key]}.ref.content_hash', 'TARGET_HASH_INVALID',
                      error.violation.message, target.ref)
            verified.add(key)

    for reference, path, expected_kind, _ in edge_specs:
        validate_target(reference, path, expected_kind)

    active = snapshot.active_selections
    for name, expected_kind in (('production', m.ObjectKind.PRODUCTION),
                                ('candidate', m.ObjectKind.CANDIDATE),
                                ('script', m.ObjectKind.SCRIPT),
                                ('scene_plan', m.ObjectKind.SCENE_PLAN)):
        reference = getattr(active, name)
        if reference is not None:
            validate_target(reference, f'$.active_refs.{name}', expected_kind)

    for i, approval in enumerate(snapshot.base.approvals):
        validate_target(approval.object_ref, f'$.approvals[{i}].object_ref')
    for i, event in enumerate(snapshot.events):
        for j, reference in enumerate(event.refs):
            validate_target(reference, f'$.events[{i}].refs[{j}]')

    return ReferenceGraph(MappingProxyType(index), tuple(edges))
