import copy
import json
import socket
import unittest

from editorial import codec as c
from editorial import model as m
from editorial.schema2_model import Schema2Event, Schema2Snapshot
from editorial.versioned_codec import decode_editorial_versioned, encode_editorial_versioned
from tests.test_editorial_codec import HASH, ID, raw, wire


def eid(last):
    return f'20000000-0000-0000-0000-{last:012d}'


def authority_evidence(approval_id=ID, **changes):
    value = {
        'approval_id': approval_id,
        'principal_id': 'posix-uid:1000@machine:' + 'a' * 32,
        'principal_display_name': 'Рецензент И\u0306 😀',
        'authority_policy_id': eid(10),
        'authority_policy_version': 'offline-v1',
        'review_session_id': eid(11),
        'request_id': eid(12),
        'declaration_codes': ['NO_UNSUPPORTED_REVIEW_CLAIM'],
        'attested_at': '2026-11-05T12:34:56Z',
        'reconsiders_record_id': None,
        'attestation_digest': '0' * 64,
        'signing_key_id': None,
        'signature_algorithm': None,
        'signature': None,
    }
    value.update(changes)
    return value


def wire2(evidence=None):
    value = wire()
    value['editorial_schema_version'] = 2
    value['approval_authority_evidence'] = [] if evidence is None else evidence
    return value


class VersionedCodecTests(unittest.TestCase):
    def bad(self, value, path=None, code=None):
        with self.assertRaises(c.DecodeError) as caught:
            decode_editorial_versioned(value if type(value) is bytes else raw(value))
        if path is not None:
            self.assertEqual(caught.exception.violation.field_path, path)
        if code is not None:
            self.assertEqual(caught.exception.violation.code, code)
        return caught.exception.violation

    def test_schema1_uses_existing_codec(self):
        encoded = raw(wire())
        self.assertEqual(decode_editorial_versioned(encoded), c.decode_snapshot(encoded))
        self.assertEqual(encode_editorial_versioned(c.decode_snapshot(encoded)),
                         c.encode_snapshot(c.decode_snapshot(encoded)))

    def test_schema2_empty_evidence(self):
        result = decode_editorial_versioned(raw(wire2()))
        self.assertIsInstance(result, Schema2Snapshot)
        self.assertEqual(result.approval_authority_evidence, ())
        self.assertEqual(result.editorial_schema_version, 2)
        self.assertEqual(result.base_snapshot.base.editorial_schema_version, 1)

    def test_schema2_populated_evidence(self):
        result = decode_editorial_versioned(raw(wire2([authority_evidence()])))
        self.assertEqual(result.approval_authority_evidence[0].approval_id, ID)
        self.assertIsInstance(result.approval_authority_evidence[0].declaration_codes, tuple)

    def test_mixed_legacy_and_evidence_approvals(self):
        value = wire2([authority_evidence()])
        second = copy.deepcopy(value['approvals'][0])
        second['id'] = eid(2)
        value['approvals'].append(second)
        result = decode_editorial_versioned(raw(value))
        self.assertEqual(len(result.base_snapshot.base.approvals), 2)
        self.assertEqual(len(result.approval_authority_evidence), 1)

    def test_dispatch_is_only_by_version(self):
        self.assertIsInstance(decode_editorial_versioned(raw(wire())), m.ContractSnapshot)
        self.assertIsInstance(decode_editorial_versioned(raw(wire2())), Schema2Snapshot)

    def test_unsupported_versions(self):
        for version in (0, 3, -1):
            value = wire()
            value['editorial_schema_version'] = version
            self.bad(value, '$.editorial_schema_version', 'SCHEMA_VERSION')

    def test_missing_version(self):
        value = wire()
        del value['editorial_schema_version']
        self.bad(value, '$.editorial_schema_version', 'MISSING_FIELD')

    def test_wrong_version_scalar_types(self):
        for version in (True, 2.0, '2'):
            value = wire2()
            value['editorial_schema_version'] = version
            self.bad(value, '$.editorial_schema_version')

    def test_missing_evidence_root(self):
        value = wire2()
        del value['approval_authority_evidence']
        self.bad(value, '$.approval_authority_evidence', 'MISSING_FIELD')

    def test_unknown_root_field(self):
        value = wire2()
        value['base_snapshot'] = {}
        self.bad(value, '$.base_snapshot', 'UNKNOWN_FIELD')

    def test_unknown_evidence_field(self):
        value = wire2([authority_evidence()])
        value['approval_authority_evidence'][0]['extra'] = 1
        self.bad(value, '$.approval_authority_evidence[0].extra', 'UNKNOWN_FIELD')

    def test_missing_every_evidence_field(self):
        for key in authority_evidence():
            value = wire2([authority_evidence()])
            del value['approval_authority_evidence'][0][key]
            with self.subTest(key=key):
                self.bad(value, f'$.approval_authority_evidence[0].{key}', 'MISSING_FIELD')

    def test_wrong_nullable_values(self):
        for key in ('reconsiders_record_id', 'signing_key_id', 'signature_algorithm', 'signature'):
            value = wire2([authority_evidence(**{key: 7})])
            with self.subTest(key=key):
                self.bad(value, f'$.approval_authority_evidence[0].{key}', 'TYPE')

    def test_duplicate_json_keys(self):
        encoded = raw(wire2())
        encoded = encoded.replace(b'"editorial_schema_version": 2',
                                  b'"editorial_schema_version": 2, "editorial_schema_version": 2')
        self.bad(encoded, '$.editorial_schema_version', 'DUPLICATE_KEY')

    def test_bom_and_invalid_utf8(self):
        self.bad(b'\xef\xbb\xbf' + raw(wire2()), '$', 'BOM')
        self.bad(b'\xff', '$', 'UTF8')

    def test_surrogate_rejected(self):
        encoded = raw(wire2([authority_evidence()])).replace(
            'Рецензент'.encode(), b'\\ud800')
        self.bad(encoded, '$.approval_authority_evidence[0].principal_display_name', 'UNICODE')

    def test_float_nan_and_infinity_rejected(self):
        for token in (b'1.5', b'NaN', b'Infinity', b'-Infinity'):
            encoded = raw(wire2()).replace(b'"generation": 1', b'"generation": ' + token)
            with self.subTest(token=token):
                self.bad(encoded, '$.generation', 'NUMBER')

    def test_excessive_depth(self):
        self.bad(b'[' * 65 + b']' * 65, '$', 'LIMIT')

    def test_excessive_size(self):
        self.bad(b' ' * (c.MAX_BYTES + 1), '$', 'LIMIT')

    def test_array_limit(self):
        value = wire2()
        value['approval_authority_evidence'] = [None] * (c.MAX_ITEMS + 1)
        self.bad(raw(value), '$.approval_authority_evidence', 'LIMIT')

    def test_unicode_round_trip_without_normalization(self):
        source = wire2([authority_evidence(principal_display_name='Їжак И\u0306 😀')])
        restored = decode_editorial_versioned(raw(source))
        encoded = encode_editorial_versioned(restored)
        self.assertEqual(decode_editorial_versioned(encoded), restored)
        self.assertIn('Їжак И\u0306 😀'.encode(), encoded)

    def test_evidence_order(self):
        value = wire2()
        second = copy.deepcopy(value['approvals'][0])
        second['id'] = eid(2)
        value['approvals'].append(second)
        first_evidence = authority_evidence()
        second_evidence = authority_evidence(
            approval_id=eid(2), review_session_id=eid(21), request_id=eid(22))
        value['approval_authority_evidence'] = [second_evidence, first_evidence]
        self.bad(value, '$.approval_authority_evidence', 'INVALID_EVIDENCE_ORDER')

    def test_duplicate_approval_evidence(self):
        value = self._two_evidence_wire()
        value['approval_authority_evidence'][1]['approval_id'] = ID
        self.bad(value, '$.approval_authority_evidence[1].approval_id', 'DUPLICATE_EVIDENCE')

    def test_wrong_declaration_order(self):
        value = wire2([authority_evidence(
            declaration_codes=['NO_UNSUPPORTED_REVIEW_CLAIM', 'SCRIPT_EXACT_TEXT_REVIEWED'])])
        self.bad(value, '$.approval_authority_evidence[0].declaration_codes', 'INVALID_DECLARATION')

    def test_duplicate_session_id(self):
        value = self._two_evidence_wire()
        value['approval_authority_evidence'][1]['review_session_id'] = eid(11)
        self.bad(value, '$.approval_authority_evidence[1].review_session_id', 'DUPLICATE_SESSION')

    def test_duplicate_request_id(self):
        value = self._two_evidence_wire()
        value['approval_authority_evidence'][1]['request_id'] = eid(12)
        self.bad(value, '$.approval_authority_evidence[1].request_id', 'DUPLICATE_REQUEST')

    def _two_evidence_wire(self):
        value = wire2()
        second = copy.deepcopy(value['approvals'][0])
        second['id'] = eid(2)
        value['approvals'].append(second)
        value['approval_authority_evidence'] = [authority_evidence(), authority_evidence(
            approval_id=eid(2), review_session_id=eid(21), request_id=eid(22))]
        return value

    def test_dangling_approval_id(self):
        value = wire2([authority_evidence(approval_id=eid(99))])
        self.bad(value, '$.approval_authority_evidence[0].approval_id', 'INVALID_EVIDENCE_ORDER')

    def test_canonical_encoding_stability(self):
        snapshot = decode_editorial_versioned(raw(wire2([authority_evidence()])))
        first = encode_editorial_versioned(snapshot)
        second = encode_editorial_versioned(decode_editorial_versioned(first))
        self.assertEqual(first, second)
        self.assertEqual(first, json.dumps(json.loads(first), ensure_ascii=False, sort_keys=True,
                                           separators=(',', ':'), allow_nan=False).encode())

    def test_snapshot_checksum_is_preserved(self):
        value = wire2()
        value['snapshot_checksum'] = 'b' * 64
        encoded = encode_editorial_versioned(decode_editorial_versioned(raw(value)))
        self.assertEqual(json.loads(encoded)['snapshot_checksum'], 'b' * 64)

    def test_schema_migrated_only_in_schema2(self):
        schema1 = wire()
        schema1['events'][0]['action'] = 'schema_migrated'
        self.bad(schema1, '$.events[0].action')
        schema2 = wire2()
        schema2['events'][0]['action'] = 'schema_migrated'
        restored = decode_editorial_versioned(raw(schema2))
        self.assertIsInstance(restored.base_snapshot.events[0], Schema2Event)
        self.assertEqual(restored.base_snapshot.events[0].action, 'schema_migrated')
        self.assertEqual(decode_editorial_versioned(encode_editorial_versioned(restored)), restored)

    def test_no_automatic_migration(self):
        result = decode_editorial_versioned(raw(wire()))
        self.assertIs(type(result), m.ContractSnapshot)
        self.assertEqual(result.base.editorial_schema_version, 1)

    def test_attestation_digest_is_shape_only(self):
        result = decode_editorial_versioned(raw(wire2([authority_evidence(
            attestation_digest='f' * 64)])))
        self.assertEqual(result.approval_authority_evidence[0].attestation_digest, 'f' * 64)

    def test_codec_does_not_evaluate_identity_or_authority(self):
        value = wire2([authority_evidence(
            principal_id='windows-sid:S-1-999999', authority_policy_version='unknown-policy')])
        self.assertIsInstance(decode_editorial_versioned(raw(value)), Schema2Snapshot)

    def test_invalid_principal_has_exact_path(self):
        self.bad(wire2([authority_evidence(principal_id='user:owner')]),
                 '$.approval_authority_evidence[0].principal_id', 'INVALID_PRINCIPAL')

    def test_partial_signature_rejected(self):
        self.bad(wire2([authority_evidence(signing_key_id='key-1')]),
                 '$.approval_authority_evidence[0].signature', 'INCOMPLETE_SIGNATURE')

    def test_codec_has_no_file_or_network_side_effects(self):
        import builtins
        original_open = builtins.open
        original_socket = socket.socket
        try:
            builtins.open = lambda *args, **kwargs: self.fail('file I/O')
            socket.socket = lambda *args, **kwargs: self.fail('network I/O')
            snapshot = decode_editorial_versioned(raw(wire2([authority_evidence()])))
            encode_editorial_versioned(snapshot)
        finally:
            builtins.open = original_open
            socket.socket = original_socket


if __name__ == '__main__':
    unittest.main()
