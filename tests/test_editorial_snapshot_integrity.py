"""E01.3.6.2 complete snapshot and current-package integrity tests."""
import copy
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import subprocess
import sys
import unittest

from editorial import model as m
from editorial.codec import EncodeError, decode_snapshot, encode_snapshot
from editorial.current_package import CurrentPackageError, compute_current_dependency_digest
from editorial.graph import GraphValidationError
from editorial.integrity import HashVerificationError, compute_revision_content_hash
from editorial.rights_binding import MaterialBindingState, RightsBindingError
from editorial.snapshot_checksum import (
    SnapshotChecksumError,
    compute_snapshot_checksum,
)
from editorial.snapshot_integrity import (
    CurrentSnapshotIntegrityResult,
    SnapshotIntegrityResult,
    validate_current_snapshot_integrity,
    validate_snapshot_integrity,
)
from test_editorial_codec import HASH, ID, raw, ref, wire
from test_editorial_current_package import downstream_mismatch
from test_editorial_package import package_wire


ID2 = '20000000-0000-0000-0000-000000000002'


def seal(snapshot):
    return replace(snapshot, snapshot_checksum=compute_snapshot_checksum(snapshot))


def full_snapshot(mutate=None, after=None):
    value = package_wire(mutate)
    if after is not None:
        after(value)
    return seal(decode_snapshot(raw(value)))


def empty_snapshot():
    value = wire()
    for name in ('production_revisions', 'profiles', 'candidates', 'sources', 'claims',
                 'scripts', 'scene_plans', 'assets', 'rights_reviews', 'approvals', 'events'):
        value[name] = []
    value['active_refs'] = dict(production=None, candidate=None, script=None, scene_plan=None)
    return seal(decode_snapshot(raw(value)))


def add_production_two(value):
    second = copy.deepcopy(value['production_revisions'][0])
    second['ref'] = ref('production', 2)
    value['production_revisions'].append(second)
    value['active_refs']['production'] = ref('production', 2)


def add_unreferenced_source(value, valid_hash=False):
    second = copy.deepcopy(value['sources'][0])
    second['ref'] = ref('source', 2)
    value['sources'].append(second)
    if valid_hash:
        temporary = decode_snapshot(raw(value))
        revision = next(r for r in temporary.base.revisions
                        if r.ref.kind is m.ObjectKind.SOURCE and r.ref.revision == 2)
        companion = next(c for c in temporary.source_details
                         if c.owner_ref.kind is m.ObjectKind.SOURCE and c.owner_ref.revision == 2)
        second['ref']['content_hash'] = compute_revision_content_hash(revision, companion)


class SnapshotIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = full_snapshot()

    def test_valid_empty_draft_snapshot(self):
        result = validate_snapshot_integrity(empty_snapshot())
        self.assertEqual(result, SnapshotIntegrityResult(True, 0, 0, ()))

    def test_valid_snapshot_with_complete_history(self):
        result = validate_snapshot_integrity(self.snapshot)
        self.assertTrue(result.checksum_verified)
        self.assertEqual(result.revision_count, len(self.snapshot.base.revisions))
        self.assertEqual(result.binding_count, 2)
        self.assertEqual(len(result.material_bindings), 2)
        self.assertTrue(all(binding.structural_match for binding in result.material_bindings))
        self.assertFalse(hasattr(result, 'approved'))
        self.assertFalse(hasattr(result, 'ready'))
        self.assertFalse(hasattr(result, 'commercial_allowed'))
        with self.assertRaises(FrozenInstanceError):
            result.checksum_verified = False

    def test_valid_current_script(self):
        result = validate_current_snapshot_integrity(self.snapshot, 'SCRIPT', 'policy-v1')
        self.assertIsInstance(result, CurrentSnapshotIntegrityResult)
        self.assertEqual(result.current_package.root_ref,
                         self.snapshot.active_selections.script)

    def test_valid_current_scenes(self):
        result = validate_current_snapshot_integrity(self.snapshot, 'SCENES', 'policy-v1')
        self.assertEqual(result.current_package.root_ref,
                         self.snapshot.active_selections.scene_plan)

    def test_valid_editorial_handoff(self):
        result = validate_current_snapshot_integrity(self.snapshot, 'HANDOFF', 'policy-v1')
        self.assertEqual(result.current_package.gate.value, 'HANDOFF')
        self.assertFalse(hasattr(result, 'ready'))
        self.assertFalse(hasattr(result.current_package, 'manifest'))

    def test_corrupt_snapshot_checksum_has_first_priority(self):
        corrupt = replace(self.snapshot, snapshot_checksum='0' * 64)
        with self.assertRaises(SnapshotChecksumError) as caught:
            validate_snapshot_integrity(corrupt)
        self.assertEqual(caught.exception.violation.field_path, '$.snapshot_checksum')

    def test_generation_change_without_checksum_is_rejected(self):
        changed = replace(self.snapshot, base=replace(self.snapshot.base, generation=2))
        with self.assertRaises(SnapshotChecksumError):
            validate_snapshot_integrity(changed)

    def test_approval_change_without_checksum_is_rejected(self):
        approval = replace(self.snapshot.base.approvals[0], reason='Changed')
        changed = replace(self.snapshot, base=replace(
            self.snapshot.base, approvals=(approval,)))
        with self.assertRaises(SnapshotChecksumError):
            validate_snapshot_integrity(changed)

    def test_event_change_without_checksum_is_rejected(self):
        event = replace(self.snapshot.events[0], reason='Changed')
        with self.assertRaises(SnapshotChecksumError):
            validate_snapshot_integrity(replace(self.snapshot, events=(event,)))

    def test_bad_exact_graph_reference_after_resealed_checksum(self):
        changed = full_snapshot(after=lambda value:
            value['candidates'][0]['source_refs'].__setitem__(0, ref('source', 99)))
        with self.assertRaises(GraphValidationError) as caught:
            validate_snapshot_integrity(changed)
        self.assertEqual(caught.exception.violation.code, 'TARGET_REVISION_MISMATCH')
        self.assertEqual(caught.exception.violation.field_path,
                         '$.candidates[0].source_refs[0]')

    def test_bad_active_revision_hash_after_resealed_checksum(self):
        def change(value):
            value['active_refs']['script']['content_hash'] = 'b' * 64
        changed = full_snapshot(after=change)
        with self.assertRaises(GraphValidationError) as caught:
            validate_snapshot_integrity(changed)
        self.assertEqual(caught.exception.violation.code, 'REFERENCE_HASH_MISMATCH')
        self.assertEqual(caught.exception.violation.field_path,
                         '$.active_refs.script.content_hash')

    def test_bad_unreferenced_historical_hash_is_checked(self):
        changed = full_snapshot(after=lambda value: add_unreferenced_source(value))
        with self.assertRaises(HashVerificationError) as caught:
            validate_snapshot_integrity(changed)
        self.assertEqual(caught.exception.violation.code, 'CONTENT_HASH_MISMATCH')
        self.assertEqual(caught.exception.violation.field_path,
                         '$.sources[1].ref.content_hash')

    def test_bad_unreferenced_companion_content_is_checked(self):
        def change(value):
            add_unreferenced_source(value, valid_hash=True)
            value['sources'][1]['reliability_notes'] = 'Changed companion metadata'
        changed = full_snapshot(after=change)
        with self.assertRaises(HashVerificationError) as caught:
            validate_snapshot_integrity(changed)
        self.assertEqual(caught.exception.violation.field_path,
                         '$.sources[1].ref.content_hash')

    def test_invalid_companion_owner_is_rejected_at_checksum_encoding(self):
        details = replace(
            self.snapshot.source_details[0],
            owner_ref=replace(self.snapshot.source_details[0].owner_ref, id=ID2),
        )
        malformed = replace(self.snapshot, source_details=(details,))
        with self.assertRaises(EncodeError) as caught:
            validate_snapshot_integrity(malformed)
        self.assertEqual(caught.exception.violation.code, 'COMPANION_OWNER')
        self.assertEqual(caught.exception.violation.field_path, '$.sources[0].ref')

    def test_source_material_digest_mismatch(self):
        changed = full_snapshot(
            lambda value: value['sources'][0].update(material_digest='b' * 64))
        with self.assertRaises(RightsBindingError) as caught:
            validate_snapshot_integrity(changed)
        self.assertEqual(caught.exception.violation.code, 'MATERIAL_DIGEST_MISMATCH')
        self.assertEqual(caught.exception.violation.field_path, '$.sources[0].material_digest')

    def test_asset_material_digest_mismatch(self):
        changed = full_snapshot(lambda value: value['assets'][0].update(sha256='b' * 64))
        with self.assertRaises(RightsBindingError) as caught:
            validate_snapshot_integrity(changed)
        self.assertEqual(caught.exception.violation.code, 'MATERIAL_DIGEST_MISMATCH')
        self.assertEqual(caught.exception.violation.field_path, '$.assets[0].sha256')

    def test_unconfirmed_source_binding_is_valid_draft_state(self):
        changed = full_snapshot(
            lambda value: value['sources'][0].update(material_digest=None))
        result = validate_snapshot_integrity(changed)
        source = next(binding for binding in result.material_bindings
                      if binding.subject_ref.kind is m.ObjectKind.SOURCE)
        self.assertIs(source.material_state, MaterialBindingState.UNCONFIRMED)
        self.assertFalse(hasattr(source, 'allowed'))

    def test_missing_active_script_allows_full_draft_but_blocks_current(self):
        changed = full_snapshot(after=lambda value: value['active_refs'].update(script=None))
        self.assertTrue(validate_snapshot_integrity(changed).checksum_verified)
        with self.assertRaises(CurrentPackageError) as caught:
            validate_current_snapshot_integrity(changed, 'SCRIPT', 'policy-v1')
        self.assertEqual(caught.exception.violation.code, 'MISSING_ACTIVE_REF')

    def test_incoherent_active_production_script_blocks_current(self):
        changed = full_snapshot(add_production_two)
        self.assertTrue(validate_snapshot_integrity(changed).checksum_verified)
        with self.assertRaises(CurrentPackageError) as caught:
            validate_current_snapshot_integrity(changed, 'SCRIPT', 'policy-v1')
        self.assertEqual(caught.exception.violation.code, 'SCRIPT_PRODUCTION_MISMATCH')

    def test_script_digest_ignores_downstream_active_scene_plan(self):
        baseline = validate_current_snapshot_integrity(
            self.snapshot, 'SCRIPT', 'policy-v1').dependency_digest
        changed = full_snapshot(downstream_mismatch)
        result = validate_current_snapshot_integrity(changed, 'SCRIPT', 'policy-v1')
        self.assertEqual(result.dependency_digest, baseline)

    def test_scenes_and_handoff_require_active_scene_plan(self):
        changed = full_snapshot(after=lambda value:
            value['active_refs'].update(scene_plan=None))
        for gate in ('SCENES', 'HANDOFF'):
            with self.subTest(gate=gate), self.assertRaises(CurrentPackageError) as caught:
                validate_current_snapshot_integrity(changed, gate, 'policy-v1')
            self.assertEqual(caught.exception.violation.code, 'MISSING_ACTIVE_REF')

    def test_scenes_and_handoff_require_coherent_scene_plan(self):
        changed = full_snapshot(downstream_mismatch)
        for gate in ('SCENES', 'HANDOFF'):
            with self.subTest(gate=gate), self.assertRaises(CurrentPackageError) as caught:
                validate_current_snapshot_integrity(changed, gate, 'policy-v1')
            self.assertEqual(caught.exception.violation.code, 'SCENE_SCRIPT_MISMATCH')

    def test_current_digest_equals_existing_standalone_builder(self):
        for gate in ('SCRIPT', 'SCENES', 'HANDOFF'):
            with self.subTest(gate=gate):
                integrated = validate_current_snapshot_integrity(
                    self.snapshot, gate, 'policy-v1')
                standalone = compute_current_dependency_digest(
                    self.snapshot, gate, 'policy-v1')
                self.assertEqual(integrated.dependency_digest, standalone)

    def test_audit_timestamp_changes_checksum_not_revision_hash(self):
        production = next(r for r in self.snapshot.base.revisions
                          if type(r) is m.ProductionRevision)
        original_hash = compute_revision_content_hash(production)
        changed = full_snapshot(after=lambda value:
            value['production_revisions'][0].update(created_at='2026-11-05T10:00:00Z'))
        changed_production = next(r for r in changed.base.revisions
                                  if type(r) is m.ProductionRevision)
        self.assertEqual(compute_revision_content_hash(changed_production), original_hash)
        self.assertEqual(changed_production.ref.content_hash, production.ref.content_hash)
        self.assertNotEqual(changed.snapshot_checksum, self.snapshot.snapshot_checksum)
        self.assertTrue(validate_snapshot_integrity(changed).checksum_verified)

    def test_repeated_validation_is_deterministic(self):
        first = validate_snapshot_integrity(self.snapshot)
        second = validate_snapshot_integrity(self.snapshot)
        self.assertEqual(first, second)
        current_first = validate_current_snapshot_integrity(
            self.snapshot, 'HANDOFF', 'policy-v1')
        current_second = validate_current_snapshot_integrity(
            self.snapshot, 'HANDOFF', 'policy-v1')
        self.assertEqual(current_first, current_second)

    def test_snapshot_is_not_mutated(self):
        before = copy.deepcopy(self.snapshot)
        validate_snapshot_integrity(self.snapshot)
        validate_current_snapshot_integrity(self.snapshot, 'SCENES', 'policy-v1')
        self.assertEqual(self.snapshot, before)

    def test_production_api_has_no_io_or_subprocess_side_effects(self):
        payload = encode_snapshot(self.snapshot)
        code = '''
import sys
active = False
def guard(event, args):
    if active and (event == 'open' or event.startswith(('socket.', 'subprocess.', 'os.system'))):
        raise AssertionError(event)
sys.addaudithook(guard)
from editorial.codec import decode_snapshot
from editorial.snapshot_integrity import validate_current_snapshot_integrity
snapshot = decode_snapshot(PAYLOAD)
active = True
result = validate_current_snapshot_integrity(snapshot, 'HANDOFF', 'policy-v1')
assert result.snapshot_integrity.checksum_verified
assert len(result.dependency_digest) == 64
'''.replace('PAYLOAD', repr(payload))
        result = subprocess.run(
            [sys.executable, '-B', '-c', code],
            cwd=Path(__file__).resolve().parents[1],
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
