"""E01.2.2 deterministic encoder and lossless round-trip tests."""
import copy
from dataclasses import replace
import json
from pathlib import Path
import subprocess
import sys
import unittest

from editorial import model as m
from editorial.codec import DecodeError, EncodeError, decode_snapshot, encode_snapshot
from test_editorial_codec import AT, HASH, ID, TEXT, raw, ref, wire


ID2 = '20000000-0000-0000-0000-000000000002'


class EncoderTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = decode_snapshot(raw(wire()))

    def bad(self, snapshot, path=None, code=None):
        with self.assertRaises(EncodeError) as caught:
            encode_snapshot(snapshot)
        violation = caught.exception.violation
        self.assertTrue(violation.field_path.startswith('$'))
        if path is not None:
            self.assertEqual(violation.field_path, path)
        if code is not None:
            self.assertEqual(violation.code, code)
        return violation

    def test_full_encode_decode_all_types(self):
        encoded = encode_snapshot(self.snapshot)
        self.assertIs(type(encoded), bytes)
        self.assertFalse(encoded.startswith(b'\xef\xbb\xbf'))
        self.assertEqual(decode_snapshot(encoded), self.snapshot)
        value = json.loads(encoded)
        self.assertEqual(tuple(len(value[name]) for name in (
            'production_revisions', 'profiles', 'candidates', 'sources', 'claims',
            'scripts', 'scene_plans', 'assets', 'rights_reviews')), (1,) * 9)

    def test_decode_encode_decode_normative_wire(self):
        original = decode_snapshot(raw(wire()))
        self.assertEqual(decode_snapshot(encode_snapshot(original)), original)

    def test_deterministic_bytes_and_fixed_json_rules(self):
        first = encode_snapshot(self.snapshot)
        self.assertEqual(first, encode_snapshot(self.snapshot))
        self.assertIn(TEXT.encode('utf-8'), first)
        self.assertNotIn(b': ', first)
        self.assertEqual(first, json.dumps(json.loads(first), ensure_ascii=False, sort_keys=True,
                         separators=(',', ':'), allow_nan=False).encode('utf-8'))

    def test_input_key_order_does_not_change_output(self):
        value = wire()
        reversed_value = {key: value[key] for key in reversed(tuple(value))}
        reversed_value['scripts'][0] = {key: reversed_value['scripts'][0][key]
                                        for key in reversed(tuple(reversed_value['scripts'][0]))}
        left = encode_snapshot(decode_snapshot(raw(value)))
        right = encode_snapshot(decode_snapshot(raw(reversed_value)))
        self.assertEqual(left, right)

    def test_unicode_nullable_and_companions_are_exact(self):
        restored = decode_snapshot(encode_snapshot(self.snapshot))
        self.assertEqual(restored.base.revisions[5].segments[0].text, TEXT)
        self.assertEqual(restored.source_details, self.snapshot.source_details)
        self.assertEqual(restored.claim_reviews, self.snapshot.claim_reviews)
        self.assertEqual(restored.rights_details, self.snapshot.rights_details)
        value = json.loads(encode_snapshot(self.snapshot))
        self.assertIsNone(value['sources'][0]['author'])
        self.assertIsNone(value['scripts'][0]['segments'][0]['visual_notes'])
        self.assertIsNone(value['rights_reviews'][0]['expires_at'])
        self.assertEqual(value['rights_reviews'][0]['subject_kind'], 'source')

    def test_approvals_events_and_nested_sequences_keep_order(self):
        value = wire()
        approval = copy.deepcopy(value['approvals'][0])
        approval.update(id=ID2, reason='Second')
        event = copy.deepcopy(value['events'][0])
        event.update(id=ID2, reason='Second')
        value['approvals'].append(approval)
        value['events'].append(event)
        value['scripts'][0]['segments'].append(dict(value['scripts'][0]['segments'][0], id=ID2))
        value['scene_plans'][0]['scenes'].append(dict(value['scene_plans'][0]['scenes'][0],
            id=ID2, start=len(TEXT), end=len(TEXT) * 2))
        snapshot = decode_snapshot(raw(value))
        restored = decode_snapshot(encode_snapshot(snapshot))
        self.assertEqual(tuple(v.reason for v in restored.base.approvals), ('Review', 'Second'))
        self.assertEqual(tuple(v.reason for v in restored.events), ('Saved', 'Second'))
        self.assertEqual(tuple(v.id for v in restored.base.revisions[5].segments), (ID, ID2))
        self.assertEqual(tuple(v.id for v in restored.base.revisions[6].scenes), (ID, ID2))

    def test_checksum_is_supplied_not_invented(self):
        changed = replace(self.snapshot, snapshot_checksum='0' * 64)
        encoded = encode_snapshot(changed)
        self.assertEqual(json.loads(encoded)['snapshot_checksum'], '0' * 64)
        self.assertEqual(decode_snapshot(encoded).snapshot_checksum, '0' * 64)

    def test_missing_extra_and_mismatched_companions_rejected(self):
        self.bad(replace(self.snapshot, source_details=()), '$.sources[0]', 'COMPANION_COUNT')
        extra = self.snapshot.source_details + self.snapshot.source_details
        # Constructor normally blocks duplicates; exercise the encoder's corrupted-input boundary.
        corrupted = copy.copy(self.snapshot)
        object.__setattr__(corrupted, 'source_details', extra)
        self.bad(corrupted, '$.sources[1]', 'COMPANION_COUNT')
        wrong_ref = m.RevisionRef(m.ObjectKind.SOURCE, ID2, 1, HASH)
        wrong = replace(self.snapshot.source_details[0], owner_ref=wrong_ref)
        self.bad(replace(self.snapshot, source_details=(wrong,)), '$.sources[0].ref', 'COMPANION_OWNER')

    def test_missing_rights_subject_kind_rejected(self):
        self.bad(replace(self.snapshot, rights_details=()), '$.rights_reviews[0]', 'COMPANION_COUNT')

    def test_weak_legacy_values_rejected_with_wire_path(self):
        production = replace(self.snapshot.base.revisions[0], intended_use='free')
        revisions = (production,) + self.snapshot.base.revisions[1:]
        changed = replace(self.snapshot, base=replace(self.snapshot.base, revisions=revisions))
        self.bad(changed, '$.production_revisions[0].intended_use', 'INVALID_VALUE')
        approval = replace(self.snapshot.base.approvals[0], gate='PUBLISH')
        changed = replace(self.snapshot, base=replace(self.snapshot.base, approvals=(approval,)))
        self.bad(changed, '$.approvals[0].gate', 'INVALID_VALUE')

    def test_unsupported_revision_and_non_snapshot_rejected(self):
        self.bad(None, '$', 'TYPE')
        header = m.EditorialRevision(self.snapshot.base.revisions[0].ref)
        corrupted_base = copy.copy(self.snapshot.base)
        object.__setattr__(corrupted_base, 'revisions', (header,) + self.snapshot.base.revisions[1:])
        corrupted = copy.copy(self.snapshot)
        object.__setattr__(corrupted, 'base', corrupted_base)
        self.bad(corrupted, '$.base.revisions', 'UNSUPPORTED_TYPE')

    def test_invalid_internal_order_is_rejected(self):
        corrupted_base = copy.copy(self.snapshot.base)
        object.__setattr__(corrupted_base, 'revisions', tuple(reversed(self.snapshot.base.revisions)))
        corrupted = copy.copy(self.snapshot)
        object.__setattr__(corrupted, 'base', corrupted_base)
        self.bad(corrupted, '$.base.revisions', 'REVISION_ORDER')

    def test_encode_has_no_file_network_or_process_side_effects(self):
        code = '''
import sys
active = False
def guard(event, args):
    if event.startswith(('socket.', 'subprocess.', 'os.system', 'os.mkdir', 'os.remove', 'os.rename')):
        raise AssertionError(event)
    if event == 'open':
        mode, flags = args[1], args[2]
        if active or (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (isinstance(flags, int) and flags & 3):
            raise AssertionError('unexpected file access')
sys.addaudithook(guard)
from editorial.codec import decode_snapshot, encode_snapshot
active = True
snapshot = decode_snapshot(PAYLOAD)
assert decode_snapshot(encode_snapshot(snapshot)) == snapshot
'''.replace('PAYLOAD', repr(raw(wire())))
        result = subprocess.run([sys.executable, '-B', '-c', code,
            ], cwd=Path(__file__).resolve().parents[1], capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
