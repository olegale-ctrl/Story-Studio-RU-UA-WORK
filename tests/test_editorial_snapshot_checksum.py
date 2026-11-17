"""E01.3.6.1 canonical full-snapshot checksum tests."""
import copy
from dataclasses import replace
import json
from pathlib import Path
import subprocess
import sys
import unittest

from editorial.codec import decode_snapshot, encode_snapshot
from editorial.snapshot_checksum import (
    SnapshotChecksumError,
    canonical_snapshot_bytes,
    compute_snapshot_checksum,
    verify_snapshot_checksum,
)
from test_editorial_codec import HASH, ID, TEXT, raw, ref, wire


ID2 = '20000000-0000-0000-0000-000000000002'
GOLDEN_BYTES = (b'{"active_refs":{"candidate":null,"production":null,"scene_plan":null,'
                b'"script":null},"approvals":[],"assets":[],"candidates":[],"claims":[],'
                b'"editorial_schema_version":1,"events":[],"generation":1,'
                b'"production_id":"10000000-0000-0000-0000-000000000001",'
                b'"production_revisions":[],"profiles":[],"rights_reviews":[],'
                b'"scene_plans":[],"scripts":[],"sources":[]}')
GOLDEN_SHA256 = 'bdf122857990d12c1a64f433c8e5165132ccf660cc92cf05eca226233312f214'


def snapshot(value=None):
    return decode_snapshot(raw(wire() if value is None else value))


def empty_snapshot():
    value = wire()
    for name in ('production_revisions', 'profiles', 'candidates', 'sources', 'claims',
                 'scripts', 'scene_plans', 'assets', 'rights_reviews', 'approvals', 'events'):
        value[name] = []
    value['active_refs'] = dict(production=None, candidate=None, script=None, scene_plan=None)
    return snapshot(value)


class SnapshotChecksumTests(unittest.TestCase):
    def assert_changes(self, mutate):
        value = wire()
        baseline = compute_snapshot_checksum(snapshot(value))
        mutate(value)
        self.assertNotEqual(compute_snapshot_checksum(snapshot(value)), baseline)

    def test_golden_canonical_bytes_and_sha256(self):
        value = empty_snapshot()
        self.assertEqual(canonical_snapshot_bytes(value), GOLDEN_BYTES)
        self.assertEqual(compute_snapshot_checksum(value), GOLDEN_SHA256)

    def test_repeated_computation_is_deterministic(self):
        value = snapshot()
        first = compute_snapshot_checksum(value)
        self.assertEqual(first, compute_snapshot_checksum(value))
        self.assertEqual(len(first), 64)
        self.assertEqual(first, first.lower())

    def test_json_object_key_order_does_not_matter(self):
        value = wire()

        def reverse_objects(item):
            if type(item) is dict:
                return {key: reverse_objects(item[key]) for key in reversed(tuple(item))}
            if type(item) is list:
                return [reverse_objects(child) for child in item]
            return item

        normal = decode_snapshot(raw(value))
        reversed_keys = decode_snapshot(raw(reverse_objects(value)))
        self.assertEqual(compute_snapshot_checksum(normal),
                         compute_snapshot_checksum(reversed_keys))

    def test_generation_changes_checksum(self):
        self.assert_changes(lambda value: value.update(generation=2))

    def test_approval_decision_changes_checksum(self):
        self.assert_changes(lambda value: value['approvals'][0].update(decision='reject'))

    def test_adding_event_changes_checksum(self):
        def mutate(value):
            event = copy.deepcopy(value['events'][0])
            event.update(id=ID2, action='active_selection_changed', reason='Змінено 😀')
            value['events'].append(event)
        self.assert_changes(mutate)

    def test_active_refs_change_checksum(self):
        self.assert_changes(lambda value: value['active_refs'].update(candidate=ref('candidate')))

    def test_every_audit_timestamp_changes_checksum(self):
        cases = (
            lambda value: value['production_revisions'][0].update(created_at='2026-11-04T10:00:01Z'),
            lambda value: value['sources'][0].update(accessed_at='2026-11-04T10:00:01Z'),
            lambda value: value['claims'][0]['evidence_links'][0].update(reviewed_at='2026-11-04T10:00:01Z'),
            lambda value: value['claims'][0].update(reviewed_at='2026-11-04T10:00:01Z'),
            lambda value: value['rights_reviews'][0].update(reviewed_at='2026-11-04T10:00:01Z'),
            lambda value: value['approvals'][0].update(timestamp='2026-11-04T10:00:01Z'),
            lambda value: value['events'][0].update(at='2026-11-04T10:00:01Z'),
        )
        for index, mutate in enumerate(cases):
            with self.subTest(timestamp=index):
                self.assert_changes(mutate)

    def test_companion_metadata_changes_checksum(self):
        cases = (
            lambda value: value['sources'][0].update(access_notes='Нова примітка'),
            lambda value: value['claims'][0].update(qualification='Уточнення'),
            lambda value: value['rights_reviews'][0].update(expires_at='2027-01-01T00:00:00Z'),
        )
        for name, mutate in zip(('source', 'claim', 'rights'), cases):
            with self.subTest(metadata=name):
                self.assert_changes(mutate)

    def test_revision_content_changes_checksum(self):
        self.assert_changes(lambda value: value['scripts'][0]['segments'][0].update(
            text='Змінений сценарій'))

    def test_stored_checksum_is_the_only_excluded_field(self):
        value = snapshot()
        changed = replace(value, snapshot_checksum='0' * 64)
        self.assertNotEqual(value.snapshot_checksum, changed.snapshot_checksum)
        self.assertEqual(canonical_snapshot_bytes(value), canonical_snapshot_bytes(changed))
        self.assertEqual(compute_snapshot_checksum(value), compute_snapshot_checksum(changed))

    def test_verify_accepts_exact_checksum(self):
        value = snapshot()
        valid = replace(value, snapshot_checksum=compute_snapshot_checksum(value))
        self.assertIsNone(verify_snapshot_checksum(valid))

    def test_verify_rejects_mismatch_with_structured_error(self):
        with self.assertRaises(SnapshotChecksumError) as caught:
            verify_snapshot_checksum(snapshot())
        violation = caught.exception.violation
        self.assertEqual(violation.code, 'SNAPSHOT_CHECKSUM_MISMATCH')
        self.assertEqual(violation.field_path, '$.snapshot_checksum')
        self.assertIn('does not match', violation.message)

    def test_unicode_ru_uk_emoji_and_combining_are_preserved(self):
        value = wire()
        value['scripts'][0]['segments'][0]['text'] = 'Русский Українська 😀 е\u0301'
        result = snapshot(value)
        canonical = canonical_snapshot_bytes(result)
        self.assertIn('Русский Українська 😀 е\u0301'.encode('utf-8'), canonical)
        self.assertNotIn(b'\\u', canonical)
        self.assertEqual(decode_snapshot(encode_snapshot(result)), result)

    def test_no_mutation_or_io(self):
        value = snapshot()
        before = copy.deepcopy(value)
        payload = encode_snapshot(value)
        compute_snapshot_checksum(value)
        self.assertEqual(value, before)
        code = '''
import sys
active = False
def guard(event, args):
    if active and (event == 'open' or event.startswith(('socket.', 'subprocess.', 'os.system'))):
        raise AssertionError(event)
sys.addaudithook(guard)
from editorial.codec import decode_snapshot
from editorial.snapshot_checksum import compute_snapshot_checksum
snapshot = decode_snapshot(PAYLOAD)
active = True
checksum = compute_snapshot_checksum(snapshot)
assert len(checksum) == 64
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
