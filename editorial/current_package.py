"""E01.3.5.3 current package selection from coherent active refs."""
from dataclasses import dataclass

from . import model as m
from .dependency_digest import compute_dependency_digest
from .package import HistoricalPackage, PackageGate, PackageValidationError, build_historical_package

__all__ = (
    'CurrentPackage', 'CurrentPackageError',
    'build_current_package', 'compute_current_dependency_digest',
)


@dataclass(frozen=True)
class CurrentPackage:
    gate: PackageGate
    root_ref: m.RevisionRef
    historical_package: HistoricalPackage
    coherence_verified: bool


class CurrentPackageError(m.ModelError):
    """Missing or incoherent active-chain state with an exact field path."""


_REQUIRED = {
    PackageGate.SCRIPT: ('production', 'candidate', 'script'),
    PackageGate.SCENES: ('production', 'candidate', 'script', 'scene_plan'),
    PackageGate.HANDOFF: ('production', 'candidate', 'script', 'scene_plan'),
}
_KINDS = {
    'production': m.ObjectKind.PRODUCTION,
    'candidate': m.ObjectKind.CANDIDATE,
    'script': m.ObjectKind.SCRIPT,
    'scene_plan': m.ObjectKind.SCENE_PLAN,
}


def _identity(ref):
    return ref.kind, ref.id, ref.revision


def _fail(path, code, message, ref=None):
    raise CurrentPackageError(m.Violation(code, path, message, ref))


def _parse_gate(value):
    if type(value) is PackageGate:
        return value
    if type(value) is str:
        try:
            return PackageGate(value)
        except ValueError:
            pass
    _fail('$.gate', 'GATE', 'Expected SCRIPT, SCENES or HANDOFF')


def _resolve_active(snapshot, slot, reference):
    path = f'$.active_refs.{slot}'
    expected_kind = _KINDS[slot]
    if reference.kind is not expected_kind:
        _fail(f'{path}.kind', 'ACTIVE_KIND_MISMATCH',
              f'{slot} requires {expected_kind.value}', reference)
    target = next((revision for revision in snapshot.base.revisions
                   if _identity(revision.ref) == _identity(reference)), None)
    if target is None:
        _fail(path, 'ACTIVE_REF_NOT_FOUND', 'Exact active revision is absent', reference)
    if target.ref != reference:
        _fail(f'{path}.content_hash', 'ACTIVE_REF_HASH_MISMATCH',
              'Active ref content_hash differs from exact target ref', reference)
    return target


def _coherent_selection(snapshot, gate):
    active = snapshot.active_selections
    resolved = {}
    for slot in _REQUIRED[gate]:
        reference = getattr(active, slot)
        if reference is None:
            _fail(f'$.active_refs.{slot}', 'MISSING_ACTIVE_REF',
                  f'{gate.value} requires non-null active {slot}')
        resolved[slot] = _resolve_active(snapshot, slot, reference)

    script = resolved['script']
    if type(script) is not m.ScriptRevision:
        _fail('$.active_refs.script', 'ACTIVE_KIND_MISMATCH',
              'Active script must resolve to ScriptRevision', active.script)
    if script.production_ref != active.production:
        _fail('$.active_refs.production', 'SCRIPT_PRODUCTION_MISMATCH',
              'Active production does not equal script.production_ref', active.production)
    if script.candidate_ref != active.candidate:
        _fail('$.active_refs.candidate', 'SCRIPT_CANDIDATE_MISMATCH',
              'Active candidate does not equal script.candidate_ref', active.candidate)

    if gate is PackageGate.SCRIPT:
        return active.script
    scene_plan = resolved['scene_plan']
    if type(scene_plan) is not m.ScenePlanRevision:
        _fail('$.active_refs.scene_plan', 'ACTIVE_KIND_MISMATCH',
              'Active scene_plan must resolve to ScenePlanRevision', active.scene_plan)
    if scene_plan.script_ref != active.script:
        _fail('$.active_refs.script', 'SCENE_SCRIPT_MISMATCH',
              'Active script does not equal scene_plan.script_ref', active.script)
    return active.scene_plan


def build_current_package(snapshot: m.ContractSnapshot, gate) -> CurrentPackage:
    """Select a coherent active root and delegate full integrity to historical builder."""
    if type(snapshot) is not m.ContractSnapshot:
        _fail('$', 'TYPE', 'Expected ContractSnapshot')
    parsed_gate = _parse_gate(gate)
    root_ref = _coherent_selection(snapshot, parsed_gate)
    try:
        historical = build_historical_package(snapshot, parsed_gate, root_ref)
    except PackageValidationError as error:
        violation = error.violation
        _fail(violation.field_path, 'HISTORICAL_PACKAGE_INVALID',
              f'{violation.code}: {violation.message}', violation.object_ref)
    return CurrentPackage(parsed_gate, root_ref, historical, True)


def compute_current_dependency_digest(snapshot: m.ContractSnapshot, gate,
                                      policy_version: str) -> str:
    """Check current coherence, then delegate to the canonical digest implementation."""
    current = build_current_package(snapshot, gate)
    return compute_dependency_digest(snapshot, current.gate, current.root_ref, policy_version)
