"""E01.3.5.3 current package active-chain coherence tests."""
import copy
from dataclasses import FrozenInstanceError
from pathlib import Path
import subprocess
import sys
import unittest

from editorial import model as m
from editorial.codec import decode_snapshot, encode_snapshot
from editorial.current_package import (
    CurrentPackage, CurrentPackageError,
    build_current_package, compute_current_dependency_digest,
)
from editorial.dependency_digest import compute_dependency_digest
from editorial.package import PackageGate
from test_editorial_codec import raw, ref
from test_editorial_package import package_wire, revision


ID2 = '20000000-0000-0000-0000-000000000002'


def fixture(mutate=None, active_mutate=None):
    value = package_wire(mutate)
    if active_mutate is not None:
        active_mutate(value['active_refs'])
    return decode_snapshot(raw(value))


def downstream_mismatch(value):
    script2 = copy.deepcopy(value['scripts'][0])
    script2['ref'] = ref('script', 2)
    value['scripts'].append(script2)
    value['scene_plans'][0]['script_ref'] = ref('script', 2)


class CurrentPackageTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = fixture()

    def bad(self, snapshot, gate, code, path=None):
        with self.assertRaises(CurrentPackageError) as caught:
            build_current_package(snapshot, gate)
        violation = caught.exception.violation
        self.assertEqual(violation.code, code)
        self.assertTrue(violation.field_path.startswith('$'))
        if path is not None:
            self.assertEqual(violation.field_path, path)
        return violation

    def test_current_script(self):
        current = build_current_package(self.snapshot, 'SCRIPT')
        self.assertIsInstance(current, CurrentPackage)
        self.assertIs(current.gate, PackageGate.SCRIPT)
        self.assertEqual(current.root_ref, self.snapshot.active_selections.script)
        self.assertEqual(current.historical_package.target_ref, current.root_ref)
        self.assertTrue(current.coherence_verified)
        self.assertFalse(hasattr(current, 'approved'))
        self.assertFalse(hasattr(current, 'ready'))
        with self.assertRaises(FrozenInstanceError):
            current.coherence_verified = False

    def test_current_scenes(self):
        current = build_current_package(self.snapshot, PackageGate.SCENES)
        self.assertIs(current.gate, PackageGate.SCENES)
        self.assertEqual(current.root_ref, self.snapshot.active_selections.scene_plan)
        self.assertEqual(current.historical_package.gate, PackageGate.SCENES)

    def test_current_editorial_handoff(self):
        current = build_current_package(self.snapshot, 'HANDOFF')
        self.assertIs(current.gate, PackageGate.HANDOFF)
        self.assertEqual(current.root_ref.kind, m.ObjectKind.SCENE_PLAN)
        self.assertFalse(hasattr(current, 'manifest'))

    def test_script_allows_null_scene_plan(self):
        snapshot = fixture(active_mutate=lambda active: active.update(scene_plan=None))
        current = build_current_package(snapshot, 'SCRIPT')
        self.assertEqual(current.root_ref, snapshot.active_selections.script)

    def test_script_ignores_incoherent_downstream_scene_plan(self):
        baseline = compute_current_dependency_digest(self.snapshot, 'SCRIPT', 'policy-v1')
        snapshot = fixture(downstream_mismatch)
        current = build_current_package(snapshot, 'SCRIPT')
        self.assertEqual(current.root_ref, snapshot.active_selections.script)
        self.assertEqual(compute_current_dependency_digest(snapshot, 'SCRIPT', 'policy-v1'), baseline)

    def test_missing_required_active_slots(self):
        cases = (
            ('SCRIPT', 'production'), ('SCRIPT', 'candidate'), ('SCRIPT', 'script'),
            ('SCENES', 'scene_plan'), ('HANDOFF', 'scene_plan'),
        )
        for gate, slot in cases:
            snapshot = fixture(active_mutate=lambda active, slot=slot: active.update({slot: None}))
            with self.subTest(gate=gate, slot=slot):
                self.bad(snapshot, gate, 'MISSING_ACTIVE_REF', f'$.active_refs.{slot}')

    def test_active_ref_missing_without_latest_fallback(self):
        def mutate(value):
            script2 = copy.deepcopy(value['scripts'][0])
            script2['ref'] = ref('script', 2)
            value['scripts'].append(script2)

        snapshot = fixture(mutate, lambda active: active.update(script=None))
        self.bad(snapshot, 'SCRIPT', 'MISSING_ACTIVE_REF', '$.active_refs.script')

        missing = fixture(active_mutate=lambda active: active.update(script=ref('script', 99)))
        self.bad(missing, 'SCRIPT', 'ACTIVE_REF_NOT_FOUND', '$.active_refs.script')

    def test_active_root_hash_mismatch(self):
        def change(active):
            active['script'] = dict(active['script'], content_hash='b' * 64)

        snapshot = fixture(active_mutate=change)
        self.bad(snapshot, 'SCRIPT', 'ACTIVE_REF_HASH_MISMATCH',
                 '$.active_refs.script.content_hash')

    def test_script_production_mismatch(self):
        def mutate(value):
            production2 = copy.deepcopy(value['production_revisions'][0])
            production2['ref'] = ref('production', 2)
            value['production_revisions'].append(production2)
            value['active_refs']['production'] = ref('production', 2)

        snapshot = fixture(mutate)
        self.bad(snapshot, 'SCRIPT', 'SCRIPT_PRODUCTION_MISMATCH',
                 '$.active_refs.production')

    def test_script_candidate_mismatch(self):
        def mutate(value):
            candidate2 = copy.deepcopy(value['candidates'][0])
            candidate2['ref'] = ref('candidate', 2)
            value['candidates'].append(candidate2)
            value['active_refs']['candidate'] = ref('candidate', 2)

        snapshot = fixture(mutate)
        self.bad(snapshot, 'SCRIPT', 'SCRIPT_CANDIDATE_MISMATCH',
                 '$.active_refs.candidate')

    def test_scene_plan_script_mismatch(self):
        snapshot = fixture(downstream_mismatch)
        self.bad(snapshot, 'SCENES', 'SCENE_SCRIPT_MISMATCH', '$.active_refs.script')
        self.bad(snapshot, 'HANDOFF', 'SCENE_SCRIPT_MISMATCH', '$.active_refs.script')

    def test_explicit_return_to_old_historical_chain(self):
        def mutate(value):
            script2 = copy.deepcopy(value['scripts'][0])
            script2['ref'] = ref('script', 2)
            value['scripts'].append(script2)

        snapshot = fixture(mutate)
        current = build_current_package(snapshot, 'SCRIPT')
        self.assertEqual(current.root_ref.revision, 1)
        self.assertTrue(any(r.ref.kind is m.ObjectKind.SCRIPT and r.ref.revision == 2
                            for r in snapshot.base.revisions))

    def test_current_digest_equals_historical_digest(self):
        for gate, target in (
            ('SCRIPT', self.snapshot.active_selections.script),
            ('SCENES', self.snapshot.active_selections.scene_plan),
            ('HANDOFF', self.snapshot.active_selections.scene_plan),
        ):
            with self.subTest(gate=gate):
                current = compute_current_dependency_digest(self.snapshot, gate, 'policy-v1')
                historical = compute_dependency_digest(self.snapshot, gate, target, 'policy-v1')
                self.assertEqual(current, historical)

    def test_historical_integrity_failure_is_current_error(self):
        value = package_wire()
        value['sources'][0]['ref']['content_hash'] = 'b' * 64
        # Keep incoming refs equal so E01.3.2 reaches computed-hash validation.
        def rewrite(child):
            if type(child) is dict:
                if ({'kind', 'id', 'revision', 'content_hash'} <= child.keys() and
                        child['kind'] == 'source' and child['revision'] == 1):
                    child['content_hash'] = 'b' * 64
                for nested in child.values():
                    rewrite(nested)
            elif type(child) is list:
                for nested in child:
                    rewrite(nested)
        rewrite(value)
        snapshot = decode_snapshot(raw(value))
        error = self.bad(snapshot, 'SCRIPT', 'HISTORICAL_PACKAGE_INVALID')
        self.assertIn('GRAPH_INVALID', error.message)

    def test_unknown_gate(self):
        self.bad(self.snapshot, 'script', 'GATE', '$.gate')

    def test_no_side_effects_and_snapshot_unchanged(self):
        before = copy.deepcopy(self.snapshot)
        payload = encode_snapshot(self.snapshot)
        compute_current_dependency_digest(self.snapshot, 'HANDOFF', 'policy-v1')
        self.assertEqual(self.snapshot, before)
        code = '''
import sys
active = False
def guard(event, args):
    if active and (event == 'open' or event.startswith(('socket.', 'subprocess.', 'os.system'))):
        raise AssertionError(event)
sys.addaudithook(guard)
from editorial.codec import decode_snapshot
from editorial.current_package import compute_current_dependency_digest
snapshot = decode_snapshot(PAYLOAD)
active = True
digest = compute_current_dependency_digest(snapshot, 'HANDOFF', 'policy-v1')
assert len(digest) == 64
'''.replace('PAYLOAD', repr(payload))
        result = subprocess.run([sys.executable, '-B', '-c', code],
            cwd=Path(__file__).resolve().parents[1], capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
