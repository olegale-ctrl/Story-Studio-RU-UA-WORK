"""E01.3.5.1 historical package closure and full integrity tests."""
import copy
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import subprocess
import sys
import unittest

from editorial import model as m
from editorial.codec import decode_snapshot, encode_snapshot
from editorial.integrity import compute_revision_content_hash
from editorial.package import (
    HistoricalPackage, PackageGate, PackageValidationError, build_historical_package,
)
from editorial.rights_binding import MaterialBindingState
from test_editorial_codec import HASH, ID, raw, ref
from test_editorial_rights_binding import fixture_wire


ID2 = '20000000-0000-0000-0000-000000000002'


def package_wire(mutate=None):
    value = fixture_wire(mutate)
    # A valid SCENES package cannot contain two revisions of one RightsReview
    # identity. Give the Asset review its own UUID, then rebuild affected hashes.
    value['rights_reviews'][1]['ref']['id'] = ID2
    value['assets'][0]['rights_ref']['id'] = ID2
    value['rights_reviews'].sort(key=lambda item: (item['ref']['id'], item['ref']['revision']))
    for kind in ('rights_review', 'asset', 'scene_plan'):
        snapshot = decode_snapshot(raw(value))
        revisions = tuple(r for r in snapshot.base.revisions if r.ref.kind.value == kind)
        for item in revisions:
            if kind == 'rights_review' and item.ref.id != ID2:
                continue
            companions = snapshot.rights_details if kind == 'rights_review' else ()
            companion = next((c for c in companions
                              if (c.owner_ref.kind, c.owner_ref.id, c.owner_ref.revision) ==
                                 (item.ref.kind, item.ref.id, item.ref.revision)), None)
            digest = compute_revision_content_hash(item, companion)
            _replace_exact_hash(value, (item.ref.kind.value, item.ref.id, item.ref.revision), digest)
    return value


def fixture(mutate=None):
    return decode_snapshot(raw(package_wire(mutate)))


def revision(snapshot, kind, revision_number=1):
    return next(value for value in snapshot.base.revisions
                if value.ref.kind is kind and value.ref.revision == revision_number)


def _replace_exact_hash(value, identity, digest):
    if type(value) is dict:
        if {'kind', 'id', 'revision', 'content_hash'} <= value.keys():
            if (value['kind'], value['id'], value['revision']) == identity:
                value['content_hash'] = digest
        for child in value.values():
            _replace_exact_hash(child, identity, digest)
    elif type(value) is list:
        for child in value:
            _replace_exact_hash(child, identity, digest)


class HistoricalPackageTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = fixture()

    def bad(self, snapshot, gate, target_ref, code, path=None):
        with self.assertRaises(PackageValidationError) as caught:
            build_historical_package(snapshot, gate, target_ref)
        violation = caught.exception.violation
        self.assertEqual(violation.code, code)
        self.assertTrue(violation.field_path.startswith('$'))
        if path is not None:
            self.assertEqual(violation.field_path, path)
        return violation

    def test_script_historical_closure_and_roles(self):
        script = revision(self.snapshot, m.ObjectKind.SCRIPT)
        package = build_historical_package(self.snapshot, 'SCRIPT', script.ref)
        self.assertIsInstance(package, HistoricalPackage)
        self.assertIs(package.gate, PackageGate.SCRIPT)
        self.assertEqual(package.target_ref, script.ref)
        self.assertEqual(tuple(ref.kind for ref in package.dependencies), (
            m.ObjectKind.CANDIDATE, m.ObjectKind.CLAIM, m.ObjectKind.GENRE_PROFILE,
            m.ObjectKind.PRODUCTION, m.ObjectKind.RIGHTS_REVIEW, m.ObjectKind.SOURCE))
        self.assertEqual(package.production_refs, (script.production_ref,))
        self.assertEqual(package.profile_refs, (script.brief.profile_ref,))
        self.assertTrue(package.integrity_verified)
        self.assertEqual(len(package.material_bindings), 1)
        self.assertIs(package.material_bindings[0].material_state, MaterialBindingState.CONFIRMED)
        self.assertFalse(hasattr(package, 'approved'))
        self.assertFalse(hasattr(package, 'allowed'))
        self.assertFalse(hasattr(package, 'ready'))

    def test_scenes_closure_contains_script_assets_and_rights(self):
        scene_plan = revision(self.snapshot, m.ObjectKind.SCENE_PLAN)
        package = build_historical_package(self.snapshot, PackageGate.SCENES, scene_plan.ref)
        kinds = tuple(ref.kind for ref in package.dependencies)
        self.assertIn(m.ObjectKind.SCRIPT, kinds)
        self.assertIn(m.ObjectKind.ASSET, kinds)
        self.assertEqual(kinds.count(m.ObjectKind.RIGHTS_REVIEW), 2)
        self.assertEqual(tuple(r.subject_ref.kind for r in package.material_bindings),
                         (m.ObjectKind.ASSET, m.ObjectKind.SOURCE))

    def test_handoff_is_editorial_closure_only(self):
        scene_plan = revision(self.snapshot, m.ObjectKind.SCENE_PLAN)
        scenes = build_historical_package(self.snapshot, 'SCENES', scene_plan.ref)
        handoff = build_historical_package(self.snapshot, 'HANDOFF', scene_plan.ref)
        self.assertIs(handoff.gate, PackageGate.HANDOFF)
        self.assertEqual(handoff.target_ref, scenes.target_ref)
        self.assertEqual(handoff.dependencies, scenes.dependencies)
        self.assertEqual(handoff.production_refs, scenes.production_refs)
        self.assertEqual(handoff.profile_refs, scenes.profile_refs)
        self.assertFalse(hasattr(handoff, 'manifest'))

    def test_historical_package_ignores_absent_active_refs(self):
        script = revision(self.snapshot, m.ObjectKind.SCRIPT)
        snapshot = replace(self.snapshot,
                           base=replace(self.snapshot.base, active_refs=()))
        package = build_historical_package(snapshot, 'SCRIPT', script.ref)
        self.assertEqual(package.target_ref, script.ref)

    def test_missing_root(self):
        script = revision(self.snapshot, m.ObjectKind.SCRIPT)
        missing = replace(script.ref, id=ID2)
        self.bad(self.snapshot, 'SCRIPT', missing, 'ROOT_NOT_FOUND', '$.target_ref')

    def test_wrong_root_kind(self):
        source = revision(self.snapshot, m.ObjectKind.SOURCE)
        self.bad(self.snapshot, 'SCRIPT', source.ref, 'ROOT_KIND', '$.target_ref.kind')
        script = revision(self.snapshot, m.ObjectKind.SCRIPT)
        self.bad(self.snapshot, 'SCENES', script.ref, 'ROOT_KIND', '$.target_ref.kind')

    def test_external_root_hash_must_match_exact_target(self):
        script = revision(self.snapshot, m.ObjectKind.SCRIPT)
        wrong = replace(script.ref, content_hash='b' * 64)
        self.bad(self.snapshot, 'SCRIPT', wrong, 'ROOT_HASH_MISMATCH',
                 '$.target_ref.content_hash')

    def test_target_own_computed_hash_is_checked(self):
        value = package_wire()
        value['scene_plans'] = []
        value['assets'] = []
        value['approvals'] = []
        value['events'] = []
        value['active_refs'] = dict(production=None, candidate=None, script=None, scene_plan=None)
        value['scripts'][0]['ref']['content_hash'] = 'b' * 64
        snapshot = decode_snapshot(raw(value))
        script = revision(snapshot, m.ObjectKind.SCRIPT)
        self.bad(snapshot, 'SCRIPT', script.ref, 'PACKAGE_HASH_INVALID',
                 '$.scripts[0].ref.content_hash')

    def test_invalid_hash_of_included_revision_is_rejected(self):
        value = package_wire()
        _replace_exact_hash(value, ('source', ID, 1), 'b' * 64)
        snapshot = decode_snapshot(raw(value))
        script = revision(snapshot, m.ObjectKind.SCRIPT)
        error = self.bad(snapshot, 'SCRIPT', script.ref, 'GRAPH_INVALID')
        self.assertIn('TARGET_HASH_INVALID', error.message)

    def test_missing_or_wrong_companion_is_rejected(self):
        script = revision(self.snapshot, m.ObjectKind.SCRIPT)
        missing = replace(self.snapshot, source_details=())
        error = self.bad(missing, 'SCRIPT', script.ref, 'GRAPH_INVALID')
        self.assertIn('TARGET_HASH_INVALID', error.message)
        wrong_details = replace(self.snapshot.source_details[0],
                                owner_ref=replace(self.snapshot.source_details[0].owner_ref, id=ID2))
        wrong = replace(self.snapshot, source_details=(wrong_details,))
        error = self.bad(wrong, 'SCRIPT', script.ref, 'GRAPH_INVALID')
        self.assertIn('TARGET_HASH_INVALID', error.message)

    def test_version_conflict_inside_closure(self):
        def mutate(value):
            source2 = copy.deepcopy(value['sources'][0])
            source2.update(ref=ref('source', 2), rights_ref=ref('rights_review', 3))
            value['sources'].append(source2)
            rights3 = copy.deepcopy(value['rights_reviews'][0])
            rights3.update(ref=ref('rights_review', 3), subject_revision=2)
            value['rights_reviews'].append(rights3)
            value['candidates'][0]['source_refs'].append(ref('source', 2))

        snapshot = fixture(mutate)
        script = revision(snapshot, m.ObjectKind.SCRIPT)
        self.bad(snapshot, 'SCRIPT', script.ref, 'PACKAGE_VERSION_CONFLICT',
                 '$.dependencies')

    def test_multiple_versions_outside_closure_are_allowed(self):
        def mutate(value):
            source2 = copy.deepcopy(value['sources'][0])
            source2.update(ref=ref('source', 2), rights_ref=ref('rights_review', 3))
            value['sources'].append(source2)
            rights3 = copy.deepcopy(value['rights_reviews'][0])
            rights3.update(ref=ref('rights_review', 3), subject_revision=2)
            value['rights_reviews'].append(rights3)

        snapshot = fixture(mutate)
        script = revision(snapshot, m.ObjectKind.SCRIPT)
        package = build_historical_package(snapshot, 'SCRIPT', script.ref)
        self.assertFalse(any(ref.kind is m.ObjectKind.SOURCE and ref.revision == 2
                             for ref in package.dependencies))

    def test_repeated_exact_dependency_is_deduplicated(self):
        script = revision(self.snapshot, m.ObjectKind.SCRIPT)
        package = build_historical_package(self.snapshot, 'SCRIPT', script.ref)
        identities = tuple((ref.kind, ref.id, ref.revision, ref.content_hash)
                           for ref in package.dependencies)
        self.assertEqual(len(identities), len(set(identities)))
        self.assertEqual(sum(ref.kind is m.ObjectKind.CLAIM for ref in package.dependencies), 1)

    def test_unconfirmed_source_is_explicit_and_not_a_grant(self):
        snapshot = fixture(lambda value: value['sources'][0].update(material_digest=None))
        script = revision(snapshot, m.ObjectKind.SCRIPT)
        package = build_historical_package(snapshot, 'SCRIPT', script.ref)
        self.assertEqual(len(package.material_bindings), 1)
        binding = package.material_bindings[0]
        self.assertIs(binding.material_state, MaterialBindingState.UNCONFIRMED)
        self.assertFalse(hasattr(binding, 'allowed'))
        self.assertFalse(hasattr(package, 'approved'))

    def test_dependencies_and_roles_are_deterministic_and_sorted(self):
        scene_plan = revision(self.snapshot, m.ObjectKind.SCENE_PLAN)
        first = build_historical_package(self.snapshot, 'SCENES', scene_plan.ref)
        second = build_historical_package(self.snapshot, 'SCENES', scene_plan.ref)
        self.assertEqual(first, second)
        key = lambda ref: (ref.kind.value, ref.id, ref.revision)
        self.assertEqual(first.dependencies, tuple(sorted(first.dependencies, key=key)))
        self.assertEqual(first.production_refs, tuple(sorted(first.production_refs, key=key)))
        self.assertEqual(first.profile_refs, tuple(sorted(first.profile_refs, key=key)))
        with self.assertRaises(FrozenInstanceError):
            first.integrity_verified = False

    def test_invalid_gate_is_structured(self):
        script = revision(self.snapshot, m.ObjectKind.SCRIPT)
        self.bad(self.snapshot, 'script', script.ref, 'GATE', '$.gate')

    def test_no_io_and_snapshot_is_unchanged(self):
        before = copy.deepcopy(self.snapshot)
        scene_plan = revision(self.snapshot, m.ObjectKind.SCENE_PLAN)
        payload = encode_snapshot(self.snapshot)
        build_historical_package(self.snapshot, 'SCENES', scene_plan.ref)
        self.assertEqual(self.snapshot, before)
        code = '''
import sys
active = False
def guard(event, args):
    if active and (event == 'open' or event.startswith(('socket.', 'subprocess.', 'os.system'))):
        raise AssertionError(event)
sys.addaudithook(guard)
from editorial.codec import decode_snapshot
from editorial.package import build_historical_package
snapshot = decode_snapshot(PAYLOAD)
target = next(r.ref for r in snapshot.base.revisions if r.ref.kind.value == 'scene_plan')
active = True
package = build_historical_package(snapshot, 'HANDOFF', target)
assert package.integrity_verified
'''.replace('PAYLOAD', repr(payload))
        result = subprocess.run([sys.executable, '-B', '-c', code],
            cwd=Path(__file__).resolve().parents[1], capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
