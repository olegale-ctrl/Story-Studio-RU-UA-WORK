"""E01.3.5.2 canonical dependency payload and digest tests."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

from editorial import model as m
from editorial.codec import decode_snapshot, encode_snapshot
from editorial.dependency_digest import (
    DependencyDigestError, canonical_dependency_bytes, compute_dependency_digest,
)
from editorial.package import PackageValidationError
from test_editorial_codec import ID, TEXT, raw, ref
from test_editorial_package import package_wire, revision


ID2 = '20000000-0000-0000-0000-000000000002'


def fixture(mutate=None):
    return decode_snapshot(raw(package_wire(mutate)))


class DependencyDigestTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = fixture()
        self.script = revision(self.snapshot, m.ObjectKind.SCRIPT)
        self.scene_plan = revision(self.snapshot, m.ObjectKind.SCENE_PLAN)

    def canonical(self, gate='SCRIPT', target=None, policy='policy-v1', snapshot=None):
        return canonical_dependency_bytes(snapshot or self.snapshot, gate,
                                          target or self.script.ref, policy)

    def digest(self, gate='SCRIPT', target=None, policy='policy-v1', snapshot=None):
        return compute_dependency_digest(snapshot or self.snapshot, gate,
                                         target or self.script.ref, policy)

    def test_script_golden_canonical_bytes_and_hash(self):
        encoded = self.canonical()
        self.assertEqual(encoded, EXPECTED_SCRIPT_BYTES)
        self.assertEqual(self.digest(), EXPECTED_SCRIPT_HASH)
        self.assertEqual(len(self.digest()), 64)
        self.assertEqual(self.digest(), self.digest().lower())

    def test_scenes_and_editorial_handoff_golden_vectors(self):
        self.assertEqual(self.digest('SCENES', self.scene_plan.ref), EXPECTED_SCENES_HASH)
        self.assertEqual(self.digest('HANDOFF', self.scene_plan.ref), EXPECTED_HANDOFF_HASH)

    def test_payload_has_exact_six_fields_and_role_arrays(self):
        payload = json.loads(self.canonical())
        self.assertEqual(set(payload), {
            'dependency_digest_schema_version', 'gate', 'policy_version', 'target_ref',
            'production_refs', 'profile_refs', 'dependencies',
        })
        self.assertEqual(payload['dependency_digest_schema_version'], 1)
        self.assertEqual(payload['gate'], 'SCRIPT')
        self.assertEqual(payload['policy_version'], 'policy-v1')
        self.assertEqual(payload['target_ref']['kind'], 'script')
        self.assertEqual(len(payload['production_refs']), 1)
        self.assertEqual(len(payload['profile_refs']), 1)
        dependency_refs = {(r['kind'], r['id'], r['revision'], r['content_hash'])
                           for r in payload['dependencies']}
        for ref_value in (*payload['production_refs'], *payload['profile_refs']):
            self.assertIn((ref_value['kind'], ref_value['id'], ref_value['revision'],
                           ref_value['content_hash']), dependency_refs)
        self.assertNotIn((payload['target_ref']['kind'], payload['target_ref']['id'],
                          payload['target_ref']['revision'], payload['target_ref']['content_hash']),
                         dependency_refs)

    def test_repeated_calls_are_deterministic(self):
        self.assertEqual(self.canonical(), self.canonical())
        self.assertEqual(self.digest(), self.digest())

    def test_input_json_key_order_does_not_change_bytes(self):
        value = package_wire()
        reordered = {key: value[key] for key in reversed(tuple(value))}
        reordered['scripts'][0] = {key: reordered['scripts'][0][key]
                                   for key in reversed(tuple(reordered['scripts'][0]))}
        snapshot = decode_snapshot(raw(reordered))
        script = revision(snapshot, m.ObjectKind.SCRIPT)
        self.assertEqual(self.canonical(), self.canonical(target=script.ref, snapshot=snapshot))

    def test_policy_version_is_literal_and_changes_digest(self):
        self.assertNotEqual(self.digest(policy='policy-v1'), self.digest(policy='policy-v2'))
        spaced = self.canonical(policy=' policy-v1 ')
        self.assertEqual(json.loads(spaced)['policy_version'], ' policy-v1 ')
        self.assertNotEqual(self.canonical(), spaced)
        for invalid in ('', '   ', None, 1):
            with self.subTest(invalid=invalid), self.assertRaises(DependencyDigestError) as caught:
                self.canonical(policy=invalid)
            self.assertEqual(caught.exception.violation.code, 'POLICY_VERSION')

    def test_gate_changes_digest_for_same_scene_plan(self):
        scenes = self.digest('SCENES', self.scene_plan.ref)
        handoff = self.digest('HANDOFF', self.scene_plan.ref)
        self.assertNotEqual(scenes, handoff)
        self.assertEqual(json.loads(self.canonical('HANDOFF', self.scene_plan.ref))['gate'], 'HANDOFF')

    def test_referenced_source_claim_profile_and_rights_changes_affect_digest(self):
        baseline = self.digest()
        mutations = (
            lambda value: value['sources'][0].update(title='Другой источник'),
            lambda value: value['claims'][0].update(statement='Другое утверждение'),
            lambda value: value['profiles'][0].update(display_name_uk='Інший профіль'),
            lambda value: value['rights_reviews'][0].update(basis='Другая проверка'),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                snapshot = fixture(mutate)
                script = revision(snapshot, m.ObjectKind.SCRIPT)
                self.assertNotEqual(baseline, self.digest(target=script.ref, snapshot=snapshot))

    def test_unused_historical_revision_does_not_change_digest(self):
        def mutate(value):
            source2 = copy.deepcopy(value['sources'][0])
            source2.update(ref=ref('source', 2), rights_ref=ref('rights_review', 3))
            value['sources'].append(source2)
            rights3 = copy.deepcopy(value['rights_reviews'][0])
            rights3.update(ref=ref('rights_review', 3), subject_revision=2)
            value['rights_reviews'].append(rights3)

        snapshot = fixture(mutate)
        script = revision(snapshot, m.ObjectKind.SCRIPT)
        self.assertEqual(self.digest(), self.digest(target=script.ref, snapshot=snapshot))

    def test_excluded_audit_timestamp_does_not_change_digest(self):
        snapshot = fixture(lambda value: value['production_revisions'][0].update(
            created_at='2026-11-05T11:22:33Z'))
        script = revision(snapshot, m.ObjectKind.SCRIPT)
        self.assertEqual(self.digest(), self.digest(target=script.ref, snapshot=snapshot))

    def test_dependencies_are_unique_and_sorted(self):
        payload = json.loads(self.canonical('SCENES', self.scene_plan.ref))
        refs = payload['dependencies']
        identities = [(r['kind'], r['id'], r['revision'], r['content_hash']) for r in refs]
        self.assertEqual(len(identities), len(set(identities)))
        sort_keys = [(r['kind'], r['id'], r['revision']) for r in refs]
        self.assertEqual(sort_keys, sorted(sort_keys))

    def test_package_errors_propagate_without_fake_digest(self):
        missing = m.RevisionRef(m.ObjectKind.SCRIPT, ID2, 1, '0' * 64)
        with self.assertRaises(PackageValidationError) as caught:
            self.digest(target=missing)
        self.assertEqual(caught.exception.violation.code, 'ROOT_NOT_FOUND')
        wrong_kind = revision(self.snapshot, m.ObjectKind.SOURCE).ref
        with self.assertRaises(PackageValidationError) as caught:
            self.digest(target=wrong_kind)
        self.assertEqual(caught.exception.violation.code, 'ROOT_KIND')
        wrong_hash = m.RevisionRef(m.ObjectKind.SCRIPT, self.script.ref.id,
                                   self.script.ref.revision, 'b' * 64)
        with self.assertRaises(PackageValidationError) as caught:
            self.digest(target=wrong_hash)
        self.assertEqual(caught.exception.violation.code, 'ROOT_HASH_MISMATCH')

    def test_package_version_conflict_blocks_digest(self):
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
        with self.assertRaises(PackageValidationError) as caught:
            self.digest(target=script.ref, snapshot=snapshot)
        self.assertEqual(caught.exception.violation.code, 'PACKAGE_VERSION_CONFLICT')

    def test_unconfirmed_draft_has_digest_but_no_authority(self):
        snapshot = fixture(lambda value: value['sources'][0].update(material_digest=None))
        script = revision(snapshot, m.ObjectKind.SCRIPT)
        digest = self.digest(target=script.ref, snapshot=snapshot)
        self.assertRegex(digest, r'^[0-9a-f]{64}$')
        payload = json.loads(self.canonical(target=script.ref, snapshot=snapshot))
        self.assertNotIn('approved', payload)
        self.assertNotIn('allowed', payload)
        self.assertNotIn('ready', payload)

    def test_unicode_is_preserved_without_normalization(self):
        policy = 'політика е\u0301 😀'
        encoded = self.canonical(policy=policy)
        self.assertIn(policy.encode('utf-8'), encoded)
        self.assertNotEqual(self.digest(policy=policy), self.digest(policy=policy.replace('е\u0301', 'é')))

        def mutate(value):
            value['scripts'][0]['segments'][0]['text'] = TEXT.replace('е\u0301', 'é')

        snapshot = fixture(mutate)
        script = revision(snapshot, m.ObjectKind.SCRIPT)
        self.assertNotEqual(self.digest(), self.digest(target=script.ref, snapshot=snapshot))

    def test_no_io_and_snapshot_is_unchanged(self):
        before = copy.deepcopy(self.snapshot)
        payload = encode_snapshot(self.snapshot)
        self.digest('HANDOFF', self.scene_plan.ref)
        self.assertEqual(self.snapshot, before)
        code = '''
import sys
active = False
def guard(event, args):
    if active and (event == 'open' or event.startswith(('socket.', 'subprocess.', 'os.system'))):
        raise AssertionError(event)
sys.addaudithook(guard)
from editorial.codec import decode_snapshot
from editorial.dependency_digest import compute_dependency_digest
snapshot = decode_snapshot(PAYLOAD)
target = next(r.ref for r in snapshot.base.revisions if r.ref.kind.value == 'scene_plan')
active = True
digest = compute_dependency_digest(snapshot, 'HANDOFF', target, 'policy-v1')
assert len(digest) == 64
'''.replace('PAYLOAD', repr(payload))
        result = subprocess.run([sys.executable, '-B', '-c', code],
            cwd=Path(__file__).resolve().parents[1], capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '')


# Filled from the approved synthetic fixture and locked as schema-1 vectors.
EXPECTED_SCRIPT_BYTES = (
    b'{"dependencies":[{"content_hash":"4ffea2010baeb441582a86b21cfe0248766f78dcb5d8a4710ab8bd1563e82d83",'
    b'"id":"10000000-0000-0000-0000-000000000001","kind":"candidate","revision":1},'
    b'{"content_hash":"972ee3870d01646bd5be7481f57d2e09b0ccaa3b2eadb1db97e6864fef9f4d73",'
    b'"id":"10000000-0000-0000-0000-000000000001","kind":"claim","revision":1},'
    b'{"content_hash":"fc621df51e0d7d16d8d0e938635fc0eb5bcf80d0d1b4f480711ee50651f7cc31",'
    b'"id":"10000000-0000-0000-0000-000000000001","kind":"genre_profile","revision":1},'
    b'{"content_hash":"d9b2e672f947befb306ac2fa2b535caa5581ca3753a7fcd0e8ba22957080da21",'
    b'"id":"10000000-0000-0000-0000-000000000001","kind":"production","revision":1},'
    b'{"content_hash":"6f046e4b9905fb312658955adc7217163b062120d778492521979400ee1ef393",'
    b'"id":"10000000-0000-0000-0000-000000000001","kind":"rights_review","revision":1},'
    b'{"content_hash":"39c36db97dccd5fb1aa64d27a50d9decfd017fc8151d9bd4b7619a2331d3f417",'
    b'"id":"10000000-0000-0000-0000-000000000001","kind":"source","revision":1}],'
    b'"dependency_digest_schema_version":1,"gate":"SCRIPT","policy_version":"policy-v1",'
    b'"production_refs":[{"content_hash":"d9b2e672f947befb306ac2fa2b535caa5581ca3753a7fcd0e8ba22957080da21",'
    b'"id":"10000000-0000-0000-0000-000000000001","kind":"production","revision":1}],'
    b'"profile_refs":[{"content_hash":"fc621df51e0d7d16d8d0e938635fc0eb5bcf80d0d1b4f480711ee50651f7cc31",'
    b'"id":"10000000-0000-0000-0000-000000000001","kind":"genre_profile","revision":1}],'
    b'"target_ref":{"content_hash":"57600db6c66b619a6a8b2e8e5b619f7ab549e6f3fcdbcefe12a5071480a9ab15",'
    b'"id":"10000000-0000-0000-0000-000000000001","kind":"script","revision":1}}'
)
EXPECTED_SCRIPT_HASH = 'b966e03318f4b3f9f486f80196df93e327a16e7daaafa691bfb3ee80aae7e934'
EXPECTED_SCENES_HASH = 'bb40e9c27dacff469e1380a9037a57c3aa6aafb7040f8eeffa9fe9e34268e9b8'
EXPECTED_HANDOFF_HASH = 'c42fcbcaba3535abb3c937861d13310fec7d73e5d0ea74a7e0b814bbfdeba161'


if __name__ == '__main__':
    unittest.main()
