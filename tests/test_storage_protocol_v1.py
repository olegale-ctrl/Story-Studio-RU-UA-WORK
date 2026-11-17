"""S1 §13 literal synthetic oracles and fail-closed primitives (no live store)."""
import copy
import hashlib
import hmac
import json
import unittest
from unittest.mock import patch

from editorial import storage_protocol_v1 as p

# Public synthetic mock, defined by S1 §13; never a fallback/production key.
KEY = hashlib.sha256(b'story-studio-public-test-vector-key-v1').digest()
P = '11111111-1111-4111-8111-111111111111'
M = '22222222-2222-4222-8222-222222222222'
E = '33333333-3333-4333-8333-333333333333'
R = '44444444-4444-4444-8444-444444444444'
ROOT = '55555555-5555-4555-8555-555555555555'
POLICY = '66666666-6666-4666-8666-666666666666'
CONNECTION = '77777777-7777-4777-8777-777777777777'
PRINCIPAL = 'windows-sid:S-1-5-21-1000-1000-1000-1001'
AT = '2026-11-05T00:00:00Z'
ACTOR = 'Тест Ї И\u0306 😀'
CHECKSUM = 'c557fdd9634346a6e14fb74f9507cbc89a2a58678a08b6c29cda5f18df9e25f6'
S_SHA = '03f8d66b009768dbba012d051ae466457f6f95903b57c4a62bdce236174d49c0'
Q_DIGEST = 'c93b117738a670e0f117cd1acffb9a24dda7cf72f7fbb35c49ac369c3178bbe0'

# Independent test-fixture construction uses stdlib JSON/plain SHA and the literal
# frame/body MACs below, never a MAC produced by the module under test.
def c(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def ref(value):
    data = c(value)
    return {'sha256': hashlib.sha256(data).hexdigest(), 'byte_length': len(data)}


def fixtures():
    s = {'editorial_schema_version': 2, 'production_id': P, 'generation': 1,
         **{k: [] for k in ('production_revisions', 'profiles', 'candidates', 'sources', 'claims', 'scripts',
                           'scene_plans', 'assets', 'rights_reviews', 'approvals', 'events', 'approval_authority_evidence')},
         'active_refs': dict.fromkeys(('production', 'candidate', 'script', 'scene_plan')),
         'snapshot_checksum': CHECKSUM}
    head = {'content_head_version': 1, 'production_id': P, 'machine_binding_id': M, 'storage_epoch_id': E,
            'editorial_schema_version': 2, 'generation': 1, 'snapshot_checksum': CHECKSUM,
            'snapshot_file_sha256': S_SHA, 'snapshot_file_length': 473, 'tx_seq': 0}
    q = {'request_version': 1, 'request_id': R, 'production_id': P, 'storage_epoch_id': None,
         'expected_head': None, 'review_session_id': None, 'operation': 'INITIALIZE_EMPTY', 'parameters': {'draft_ref': ref(s)}}
    policy = {'policy_id': POLICY, 'policy_version': 'fixture-v1', 'policy_sha256': '0' * 64}
    auth = {'policy_ref': policy, 'principal_id': PRINCIPAL, 'authenticated_connection_id': CONNECTION,
            'command_grants': ['PROTECTED_SNAPSHOT_WRITE', 'INITIALIZE'], 'gate_decision_grant': None}
    f = {'command_version': 1, 'request': q, 'request_sha256': Q_DIGEST, 'key_id': 'fixture-key',
         'principal_id': PRINCIPAL, 'actor': ACTOR, 'at': AT, 'authorization': auth,
         'assigned_ids': {'approval_id': None, 'event_id': None}, 'storage_epoch_id': E,
         'expected_result': head, 'review_snapshot': None}
    core = {'receipt_core_version': 1, 'request_id': R, 'request_sha256': Q_DIGEST, 'storage_epoch_id': E,
            'operation': 'INITIALIZE_EMPTY', 'tx_seq': 0, 'status': 'INITIALIZED', 'result_content_head': head,
            'approval_ids': [], 'event_ids': [], 'abort_code': None}
    ledger = {'blob_version': 1, 'blob_type': 'LEDGER_DELTA', 'production_id': P, 'storage_epoch_id': E,
              'previous_ref': None, 'entries': [{'request_id': R, 'review_session_id': None, 'request_sha256': Q_DIGEST,
              'command_mac': MACS['F'], 'key_id': 'fixture-key', 'tx_seq': 0, 'outcome': 'INITIALIZED', 'receipt_core_sha256': ref(core)['sha256']}]}
    g0 = {'guard_version': 1, 'continuity': 'CONTINUOUS', 'baseline_ref': None, 'ledger_tip': None, 'barrier_tip': None, 'lineage_tip': None}
    g1 = {**g0, 'ledger_tip': ref(ledger)}
    i0 = {'initialization_version': 1, 'request_id': R, 'request_sha256': Q_DIGEST, 'production_id': P,
          'machine_binding_id': M, 'storage_epoch_id': E, 'managed_root_token': ROOT, 'source_ref': ref(s),
          'principal_id': PRINCIPAL, 'actor': ACTOR, 'at': AT, 'policy_ref': policy, 'authorization': auth,
          'guard_before': g0, 'key_id': 'fixture-key'}
    iw = {'body': i0, 'mac': MACS['I0']}
    t0 = {'registration_version': 1, 'storage_protocol_version': 1, 'production_id': P, 'machine_binding_id': M,
          'storage_epoch_id': E, 'managed_root_token': ROOT, 'initialization_ref': ref(iw), 'storage_profile_id': 'fixture-profile', 'key_id': 'fixture-key'}
    plan = {'plan_version': 1, 'kind': 'GENESIS', 'request_id': R, 'review_session_id': None, 'tx_seq': 0,
            'key_id': 'fixture-key', 'command_ref': ref(f), 'command_mac': MACS['F'], 'base_head': None,
            'observed_primary': {'state': 'MISSING'}, 'new_content_head': head, 'image_ref': ref(s),
            'guard_before': g0, 'guard_commit': g1, 'expected_commit_receipt': core, 'new_approvals': [],
            'initialization_ref': ref(iw), 'storage_profile_id': 'fixture-profile'}
    jr = lambda name, index: {'record_index': index, 'record_mac': MACS[name]}
    def record(index, previous, kind, payload):
        return {'journal_record_version': 1, 'production_id': P, 'machine_binding_id': M, 'storage_epoch_id': E,
                'record_index': index, 'previous_record_mac': previous, 'key_id': 'fixture-key', 'record_type': kind, 'payload': payload}
    j0 = record(0, None, 'PREPARE', {'plan_ref': ref(plan)})
    j1 = record(1, MACS['J0'], 'PUBLISH_INTENT', {'plan_ref': ref(plan), 'prepare_ref': jr('J0', 0)})
    j2 = record(2, MACS['J1'], 'GENESIS', {'plan_ref': ref(plan), 'prepare_ref': jr('J0', 0), 'intent_ref': jr('J1', 1), 'receipt_core': core})
    ch = {'committed_head_version': 1, 'content_head': head, 'commit_ref': jr('J2', 2)}
    a0 = {'anchor_version': 1, 'production_id': P, 'machine_binding_id': M, 'storage_epoch_id': E, 'activation': 'INITIALIZING',
          'stable_head': None, 'reserved_tx_high_watermark': 0, 'journal_tail': jr('J0', 0),
          'pending': {'pending_version': 1, 'phase': 'PREPARED', 'plan_ref': ref(plan), 'prepare_ref': jr('J0', 0), 'intent_ref': None},
          'history_guard': g0, 'key_id': 'fixture-key'}
    a1 = {**a0, 'activation': 'ACTIVE', 'stable_head': ch, 'journal_tail': jr('J2', 2), 'pending': None, 'history_guard': g1}
    rc = {'receipt_version': 1, 'core': core, 'terminal_ref': jr('J2', 2), 'result_head': ch, 'key_id': 'fixture-key'}
    ca = {**core, 'status': 'ABORTED_PRECOMMIT', 'result_content_head': None, 'abort_code': 'RECOVERY_PREINTENT_ABORT'}
    la = {**ledger, 'entries': [{**ledger['entries'][0], 'outcome': 'ABORTED_PRECOMMIT', 'receipt_core_sha256': ref(ca)['sha256']}]}
    ja = record(1, MACS['J0'], 'ABORT', {'prepare_ref': jr('J0', 0), 'plan_ref': ref(plan), 'abort_code': 'RECOVERY_PREINTENT_ABORT',
                                     'receipt_core': ca, 'result_guard': {**g0, 'ledger_tip': ref(la)}})
    return dict(S=s, H=head, Q=q, F=f, C0=core, L0=ledger, I0=i0, I=iw, T0=t0, T=plan, J0=j0, J1=j1, J2=j2,
                CH=ch, A0=a0, A1=a1, RC=rc, C_abort=ca, L_abort=la, JA=ja)

# Literal outputs from the approved S1a §13 (not calculated at test time).
EXPECTED = {
    'F': (1629, 'a6746a97b88d1837e97b4dd9a42242405410971aadbafcc291bf0abc9678d2c6'),
    'C0': (817, 'a677d7c51ecfde869cf2a0cf8711c2be35f98d27d1f364c9717b1a1e0475017e'),
    'L0': (581, 'c216ee03e00bf197987469f8c1148841d21e21fe082404533fc463fa7648781a'),
    'I0': (1373, '3b80f73d520191a3a8d0fcce3a04655ab8e08c90fe2b2bf045cf9d82ca9a327c'),
    'I': (1455, '0ea34d03ade7acc68577a80f9575b6abfcb2023d83a57ac546c47e5ed595cad6'),
    'T0': (468, '143ec2963aa12b36c777f246043e7e512dde6d410faaec6809931ce96cbe11f1'),
    'T': (2365, '827c61894419f8fb1a8f8ac628f797fb0743be651ea4e4ea71d4738cbfc0582a'),
    'J0': (412, 'd21691c38834df252c82b75733566f8903c2a8ff67b04c1b711e07aa3efcf3bf'),
    'J1': (594, 'cdce641252af9dc8d175a06d8515632e83133f6e0700ecbf1d2dca19420d3ecb'),
    'J2': (1532, '4e495831ac683ed673c1ad444e15d380df04f3f80a5fc8005e377cc31d0297d1'),
    'CH': (614, 'dbd9a7294834d1a1fd6996209717a8f62663fd25b4b11779e33cd50e65d37d05'),
    'A0': (836, 'bb768ad978fdc95172617791c7850235c3e06909c66b072a067712fb911a1fe7'),
    'A1': (1256, '4984943c3c76c81580b686edd4ece03d38f7054472ba7aafc2264a6f82062472'),
    'RC': (1612, 'a0e53e1207b99e33cef88abbd94eab34b49dece1a419160dcc61f30cb7f5e17b'),
    'C_abort': (391, '30846a5bbae224f4bd1d319fcebe010b5755d16f17ba2368c1ec3903b94b3327'),
    'L_abort': (587, '8c4aeec32367511467e3a17aec76b9d336cedd3f618fde5c0fd99a3626a05c0a'),
    'JA': (1260, '587ec273360978aed78818d4f30868193d3d9fd837afb394985b95ca2f34403d'),
    'S': (473, '03f8d66b009768dbba012d051ae466457f6f95903b57c4a62bdce236174d49c0'),
    'H': (458, '38c51edfa1db01c9c3d9e4b81311dd49cadeb5b5f4d29469565035d0721036b3'),
    'Q': (352, '1620bcf520a6c44fe250b3178a5cb0877f632410f82a4187c9c5fefa5d6b7dba'),
}
MACS = {
    'F': 'b60a2346904d2bed9b69280ef808a5ae366f151de93675df0620d2552c175ac2',
    'I0': '7a6e46914a816cf7e29d16c3370d6750cd1c94c4f97c58f3dd23d805f77f4c6b',
    'T0': '2bbf41c650a957ada9abdf1cf0671cd5593fdd3d05f5aca7e405b6775a30e888',
    'J0': '4e8ebffc3ffcb8972b15dbc901d3ca8e4a7806a838bd785780b1f3b867b79a13',
    'J1': 'def73c97f59e3e2a544f30acacc593dc7ffc2826733465748dbfea69579b25de',
    'J2': 'a1b89141d2676cdfebaf341dc2a509e7c641ac0165901fcde46111d9b7f3630f',
    'A0': '2338e85beda320de081478fc6a271c850c8a8dd34653c9bc375c5106b03932f5',
    'A1': '7ade0e3cac5cf9b884bc7eaa73d63cc4fa3c00b313eff991ef0d1a127690cefa',
    'RC': '1ee63df031daabfda27c2550b61888081b03309bb6039653471b7603a6e937a0',
    'JA': '7526b984a77b5bd45ea35eb9548cd923e6d671e139e9c3c7654baa6f85e2f5fa',
}
FRAMES = {
    'J0': ('53534a310000019c', 412, 452),
    'J1': ('53534a3100000252', 594, 634),
    'J2': ('53534a31000005fc', 1532, 1572),
    'JA': ('53534a31000004ec', 1260, 1300),
}


class ProtocolTestCase(unittest.TestCase):
    def setUp(self):
        self.x = fixtures()

    def error(self, code, function, *args, **kwargs):
        with self.assertRaises(p.ProtocolError) as caught:
            function(*args, **kwargs)
        self.assertEqual(caught.exception.code, code)
        return caught.exception

    def frame(self, name):
        # Craft authenticated adversarial frames independently of tested encoder.
        raw = c(self.x[name]) if isinstance(name, str) else c(name)
        return self.raw_frame(raw)

    def raw_frame(self, raw):
        header = b'SSJ1' + len(raw).to_bytes(4, 'big')
        signature = hmac.new(KEY, b'story-studio-storage-journal-v1\0' + header + raw, hashlib.sha256).digest()
        return header + raw + signature


class GoldenVectors(ProtocolTestCase):
    def test_all_twenty_canonical_object_lengths_and_sha_literals(self):
        for name, (length, digest) in EXPECTED.items():
            with self.subTest(object=name):
                raw = p.canonical_json(self.x[name])
                self.assertEqual(len(raw), length)
                self.assertEqual(hashlib.sha256(raw).hexdigest(), digest)
                self.assertEqual(p.decode_canonical_json(raw), self.x[name])

    def test_snapshot_checksum_unchanged(self):
        s = dict(self.x['S']); del s['snapshot_checksum']
        self.assertEqual(hashlib.sha256(p.canonical_json(s)).hexdigest(), CHECKSUM)

    def test_request_domain_digest_literal(self):
        self.assertEqual(p.request_digest(self.x['Q']), Q_DIGEST)
        self.assertNotEqual(Q_DIGEST, EXPECTED['Q'][1])

    def test_all_six_body_mac_literals(self):
        for name, function, domain in [('F', p.frozen_command_mac, 'command'), ('I0', p.initialization_mac, 'initialize'),
                ('T0', p.registration_mac, 'registration'), ('A0', p.anchor_mac, 'anchor'),
                ('A1', p.anchor_mac, 'anchor'), ('RC', p.receipt_mac, 'receipt')]:
            with self.subTest(object=name):
                self.assertEqual(function(self.x[name], KEY), MACS[name])
                self.assertIsNone(p.verify_mac(self.x[name], MACS[name], KEY, domain=domain))

    def test_four_frame_literals_headers_sizes_mac(self):
        for name, (header, payload_length, full_length) in FRAMES.items():
            with self.subTest(frame=name):
                frame = p.encode_journal_frame(self.x[name], KEY)
                self.assertEqual(frame[:8].hex(), header)
                self.assertEqual(len(frame[8:-32]), payload_length)
                self.assertEqual(len(frame), full_length)
                self.assertEqual(frame[-32:].hex(), MACS[name])
                self.assertEqual(p.journal_frame_mac(self.x[name], KEY), MACS[name])
                self.assertEqual(p.decode_journal_frame(frame, KEY), self.x[name])

    def test_positive_genesis_complete_chain(self):
        frames = [self.frame(n) for n in ('J0', 'J1', 'J2')]
        self.assertEqual(p.verify_journal_frames(frames, KEY), [self.x[n] for n in ('J0', 'J1', 'J2')])
        for n in ('J0', 'J1', 'J2'):
            p.verify_record_plan(self.x[n], self.x['T'], command=self.x['F'])

    def test_alternative_abort_complete_chain(self):
        self.assertEqual(p.verify_journal_frames([self.frame('J0'), self.frame('JA')], KEY), [self.x['J0'], self.x['JA']])
        p.verify_record_plan(self.x['JA'], self.x['T'], command=self.x['F'])
        self.assertEqual(self.x['C_abort']['status'], 'ABORTED_PRECOMMIT')
        self.assertIsNone(self.x['C_abort']['result_content_head'])

    def test_typed_golden_blobs(self):
        for n, kind in [('H', 'ContentHead'), ('F', 'FrozenCommand'), ('C0', 'ReceiptCore'), ('L0', 'LedgerBlob'),
                        ('I0', 'InitializationBody'), ('I', 'InitializationAuthorization'), ('T0', 'RegistrationBody'),
                        ('T', 'TransactionPlan'), ('CH', 'CommittedHead'), ('A0', 'AnchorBody'), ('A1', 'AnchorBody'),
                        ('RC', 'ReceiptBody'), ('C_abort', 'ReceiptCore'), ('L_abort', 'LedgerBlob')]:
            with self.subTest(kind=kind):
                raw = c(self.x[n])
                self.assertEqual(p.verify_blob(raw, ref(self.x[n]), kind), self.x[n])


class CanonicalJSON(ProtocolTestCase):
    def test_exact_sorted_unicode_and_array_order(self):
        v = {'ї': ['😀', 'И\u0306'], 'a': [2, 1], '\ue000': 'x', '𐀀': 'y'}
        expected = '{"a":[2,1],"ї":["😀","Й"],"\ue000":"x","𐀀":"y"}'.encode()
        self.assertEqual(p.canonical_json(v), expected)
        self.assertEqual(p.decode_canonical_json(expected), v)

    def test_u64_precision_above_double(self):
        for n in (2**53 + 1, p.U64_MAX):
            head = {**self.x['H'], 'tx_seq': n}
            p.validate_wire(head, 'ContentHead')
            self.assertEqual(p.decode_canonical_json(p.canonical_json(head))['tx_seq'], n)

    def test_generation_has_no_u64_or_python_digit_cap(self):
        head = {**self.x['H'], 'generation': 10**4500}
        p.validate_wire(head, 'ContentHead')
        raw = p.canonical_json(head)
        self.assertIn(b'"generation":1' + b'0' * 4500 + b',', raw)
        self.assertEqual(p.decode_canonical_json(raw)['generation'], 10**4500)

    def test_negative_generic_integer_but_unsigned_schema_rejects(self):
        self.assertEqual(p.decode_canonical_json(b'-123'), -123)
        self.error('SEQUENCE_EXHAUSTED', p.validate_wire, {**self.x['H'], 'tx_seq': -1}, 'ContentHead')

    def test_duplicate_nested_key_exact_path(self):
        err = self.error('DUPLICATE_KEY', p.decode_canonical_json, b'{"a":{"b":1,"b":2}}')
        self.assertEqual(err.path, '$.a.b')

    def test_escaped_duplicate_keys(self):
        self.error('DUPLICATE_KEY', p.decode_canonical_json, br'{"a":1,"\u0061":2}')

    def test_forbidden_python_types(self):
        for v in (1.0, float('nan'), float('inf'), {1: 'x'}, (1,), b'a', {1}, object()):
            with self.subTest(type=type(v)):
                self.error('TYPE', p.canonical_json, v)

    def test_type_subclasses_are_not_coerced(self):
        class Int(int):
            pass
        self.error('TYPE', p.canonical_json, Int(1))

    def test_float_and_nonfinite_json(self):
        for raw in (b'1.0', b'1e1', b'NaN', b'Infinity', b'-Infinity', b'{"n":1.5}'):
            with self.subTest(raw=raw):
                self.error('TYPE', p.decode_canonical_json, raw)

    def test_noncanonical_variants(self):
        for raw in (b' {"a":1}', b'{"b":2,"a":1}', b'{"a": 1}', b'{}\n', b'-0', br'"\u0061"', br'"\/"', b'\xef\xbb\xbf{}'):
            with self.subTest(raw=raw):
                self.error('WIRE_FORMAT', p.decode_canonical_json, raw)

    def test_invalid_json(self):
        for raw in (b'{', b'[1,]', b'01', b'{}{}', b'"unterminated'):
            with self.subTest(raw=raw):
                self.error('WIRE_FORMAT', p.decode_canonical_json, raw)

    def test_bad_utf8(self):
        for raw in (b'"\xff"', b'"\xc0\xaf"', b'"\xed\xa0\x80"'):
            self.error('WIRE_FORMAT', p.decode_canonical_json, raw)

    def test_surrogates_in_keys_values_and_escaped_wire(self):
        for v in ('\ud800', {'\udfff': 'x'}, {'a': '\udc00'}):
            self.error('WIRE_FORMAT', p.canonical_json, v)
        self.error('WIRE_FORMAT', p.decode_canonical_json, br'"\ud800"')

    def test_container_depth_boundary(self):
        raw = b'[' * 64 + b'0' + b']' * 64
        p.decode_canonical_json(raw)
        self.error('LIMIT', p.decode_canonical_json, b'[' + raw + b']')
        v = 0
        for _ in range(65):
            v = [v]
        self.error('LIMIT', p.canonical_json, v)

    def test_quoted_brackets_do_not_change_depth(self):
        text = '[' * 100 + '\\"' + ']' * 100
        self.assertEqual(p.decode_canonical_json(c(text)), text)

    def test_cycles_fail_bounded(self):
        v = []; v.append(v)
        self.error('LIMIT', p.canonical_json, v)

    def test_size_and_text_bounds(self):
        self.assertEqual(p.canonical_json('abc', max_bytes=5), b'"abc"')
        self.error('LIMIT', p.canonical_json, 'abc', max_bytes=4)
        self.error('LIMIT', p.decode_canonical_json, b'"abc"', max_bytes=4)
        self.error('LIMIT', p.canonical_json, 'x' * 100_001)
        self.error('LIMIT', p.decode_canonical_json, b'"' + b'x' * 100_001 + b'"')

    def test_composed_and_decomposed_unicode_differ(self):
        a, b = 'Й', 'И\u0306'
        self.assertNotEqual(p.canonical_json(a), p.canonical_json(b))
        f = copy.deepcopy(self.x['F']); f['actor'] = ACTOR.replace(b, a)
        self.assertNotEqual(p.frozen_command_mac(f, KEY), MACS['F'])
        self.assertEqual(f['actor'], ACTOR.replace(b, a))


class ClosedSchemas(ProtocolTestCase):
    def test_unknown_and_missing_request_fields(self):
        for v, code, path in [({**self.x['Q'], 'actor': 'caller'}, 'UNKNOWN_FIELD', '$.actor'),
                              ({k: v for k, v in self.x['Q'].items() if k != 'request_id'}, 'MISSING_FIELD', '$.request_id')]:
            err = self.error(code, p.request_digest, v); self.assertEqual(err.path, path)

    def test_unknown_nested_parameter(self):
        q = copy.deepcopy(self.x['Q']); q['parameters']['draft_ref']['path'] = 'ignored.json'
        self.error('UNKNOWN_FIELD', p.request_digest, q)

    def test_unknown_missing_and_version_all_journal_payloads(self):
        for name in ('J0', 'J1', 'J2', 'JA'):
            for where in ('outer', 'payload'):
                record = copy.deepcopy(self.x[name]); target = record if where == 'outer' else record['payload']
                target['extra'] = True
                self.error('UNKNOWN_FIELD', p.decode_journal_frame, self.frame(record), KEY)
                del target['extra']; del target[next(iter(target))]
                self.error('MISSING_FIELD', p.decode_journal_frame, self.frame(record), KEY)
        record = {**self.x['J0'], 'journal_record_version': 2}
        self.error('VERSION_UNSUPPORTED', p.decode_journal_frame, self.frame(record), KEY)

    def test_unknown_record_type(self):
        record = {**self.x['J0'], 'record_type': 'ADMIN_OVERRIDE'}
        self.error('TYPE', p.encode_journal_frame, record, KEY)

    def test_disabled_publish_revision_no_digest_or_mac(self):
        q = {**self.x['Q'], 'operation': 'PUBLISH_REVISION', 'parameters': {'proposal_ref': ref(self.x['S']), 'reason': 'test'}}
        self.error('OPERATION_NOT_AVAILABLE', p.request_digest, q)
        f = {**self.x['F'], 'request': q}
        self.error('OPERATION_NOT_AVAILABLE', p.frozen_command_mac, f, KEY)

    def test_u64_overflow_negative_bool_float(self):
        for value, code in [(p.U64_MAX + 1, 'SEQUENCE_EXHAUSTED'), (-1, 'SEQUENCE_EXHAUSTED'), (True, 'TYPE'), (1.0, 'TYPE')]:
            record = {**self.x['J0'], 'record_index': value}
            self.error(code, p.encode_journal_frame, record, KEY)

    def test_invalid_identifiers_labels_hex_and_calendar(self):
        for field, value in [('principal_id', 'caller'), ('key_id', '../key'), ('at', '2026-02-30T00:00:00Z')]:
            f = {**self.x['F'], field: value}
            self.error('TYPE', p.frozen_command_mac, f, KEY)
        q = {**self.x['Q'], 'request_id': R.replace('4', 'A', 1)}
        self.error('TYPE', p.request_digest, q)
        h = {**self.x['H'], 'snapshot_checksum': 'A' * 64}
        self.error('TYPE', p.validate_wire, h, 'ContentHead')

    def test_frozen_grant_binding_and_request_digest(self):
        for change in ({'command_grants': ['INITIALIZE']}, {'command_grants': ['PROTECTED_SNAPSHOT_WRITE', 'INITIALIZE', 'RECOVERY']},
                       {'principal_id': 'windows-sid:S-1-5-99'}, {'gate_decision_grant': {'gate': 'SCRIPT', 'decision': 'approve'}}):
            f = copy.deepcopy(self.x['F']); f['authorization'].update(change)
            self.error('AUTHORIZATION_BINDING_MISMATCH', p.frozen_command_mac, f, KEY)
        f = {**self.x['F'], 'request_sha256': '0' * 64}
        self.error('BLOB_HASH_MISMATCH', p.frozen_command_mac, f, KEY)

    def test_old_authorization_token_not_accepted(self):
        f = copy.deepcopy(self.x['F']); f['authorization']['permission'] = 'INITIALIZE'
        self.error('UNKNOWN_FIELD', p.frozen_command_mac, f, KEY)

    def test_initialization_binding(self):
        i = copy.deepcopy(self.x['I0']); i['authorization']['policy_ref']['policy_version'] = 'wrong'
        # Deepcopy preserves shared policy object: replace to force mismatch.
        i['policy_ref'] = self.x['I0']['policy_ref']
        self.error('AUTHORIZATION_BINDING_MISMATCH', p.initialization_mac, i, KEY)

    def test_typed_blob_substitution(self):
        raw = c(self.x['L0'])
        self.error('BLOB_TYPE_MISMATCH', p.verify_blob, raw, ref(self.x['L0']), 'BaselineBlob')
        self.error('BLOB_TYPE_MISMATCH', p.verify_blob, raw, ref(self.x['L0']), 'UnknownBlob')

    def test_typed_blob_hash_and_length(self):
        raw = c(self.x['L0'])
        for reference in ({**ref(self.x['L0']), 'sha256': '0' * 64}, {**ref(self.x['L0']), 'byte_length': len(raw) + 1}):
            self.error('BLOB_HASH_MISMATCH', p.verify_blob, raw, reference, 'LedgerBlob')
        self.error('LIMIT', p.validate_wire, {'sha256': '0' * 64, 'byte_length': 0}, 'BlobRef')
        self.error('LIMIT', p.validate_wire, {'sha256': '0' * 64, 'byte_length': p.MAX_BLOB_BYTES + 1}, 'BlobRef')

    def test_plan_ref_hash_of_wrong_blob_cannot_pass(self):
        j = copy.deepcopy(self.x['J0']); j['payload']['plan_ref'] = ref({})
        p.decode_journal_frame(self.frame(j), KEY)  # MAC/record alone cannot prove a referenced plan.
        self.error('BLOB_TYPE_MISMATCH', p.verify_blob, b'{}', ref({}), 'TransactionPlan')
        self.error('BLOB_HASH_MISMATCH', p.verify_record_plan, j, self.x['T'])

    def test_plan_context_and_terminal_binding(self):
        j = {**self.x['J0'], 'production_id': M}
        self.error('JOURNAL_TRANSITION_INVALID', p.verify_record_plan, j, self.x['T'])
        j = copy.deepcopy(self.x['J2']); j['payload']['receipt_core']['request_id'] = ROOT
        self.error('JOURNAL_TRANSITION_INVALID', p.verify_record_plan, j, self.x['T'])

    def test_unknown_wire_type(self):
        self.error('BLOB_TYPE_MISMATCH', p.validate_wire, {}, 'AUTO')


class JournalFailures(ProtocolTestCase):
    def test_every_proper_genesis_frame_prefix_rejected(self):
        frame = self.frame('J2')
        for end in range(len(frame)):
            with self.subTest(end=end), self.assertRaises(p.StructuralError):
                p.decode_journal_frame(frame[:end], KEY)

    def test_bad_magic_no_resynchronization(self):
        j0 = self.frame('J0')
        for raw in (b'BAD!' + j0[4:], b'corruption' + j0, b'SSJ0' + j0[4:]):
            self.error('WIRE_FORMAT', p.decode_journal_frame, raw, KEY)

    def test_invalid_declared_lengths(self):
        frame = self.frame('J0')
        for n in (0, p.MAX_FRAME_PAYLOAD + 1, 2**32 - 1):
            self.error('LIMIT', p.decode_journal_frame, frame[:4] + n.to_bytes(4, 'big') + frame[8:], KEY)
        self.error('WIRE_FORMAT', p.decode_journal_frame, frame[:4] + (413).to_bytes(4, 'big') + frame[8:], KEY)

    def test_extra_bytes_and_concatenated_frames_rejected(self):
        j0 = self.frame('J0')
        for raw in (j0 + b'\n', j0 + b'\0', j0 + self.frame('J1')):
            self.error('WIRE_FORMAT', p.decode_journal_frame, raw, KEY)

    def test_mac_corruption_is_cryptographic_error(self):
        frame = self.frame('J0'); frame = frame[:-1] + bytes([frame[-1] ^ 1])
        with self.assertRaises(p.CryptographicError) as caught:
            p.decode_journal_frame(frame, KEY)
        self.assertEqual(caught.exception.code, 'MAC_MISMATCH')

    def test_payload_corruption_even_valid_json_is_not_accepted(self):
        frame = self.frame('J0').replace(P.encode(), M.encode(), 1)
        self.error('MAC_MISMATCH', p.decode_journal_frame, frame, KEY)

    def test_structural_precedence_before_crypto(self):
        bad = copy.deepcopy(self.x['J0']); bad['extra'] = True
        self.error('UNKNOWN_FIELD', p.decode_journal_frame, self.frame(bad), None)
        self.error('WIRE_FORMAT', p.decode_journal_frame, self.raw_frame(b'{}\n'), None)

    def test_duplicate_frame_keys_even_with_valid_mac(self):
        raw = c(self.x['J0']).replace(b'"record_index":0', b'"record_index":0,"record_index":0')
        self.error('DUPLICATE_KEY', p.decode_journal_frame, self.raw_frame(raw), KEY)

    def test_frame_noncanonical_utf8_and_float(self):
        self.error('WIRE_FORMAT', p.decode_journal_frame, self.raw_frame(b'\xff'), KEY)
        self.error('WIRE_FORMAT', p.decode_journal_frame, self.raw_frame(c(self.x['J0']) + b'\n'), KEY)
        raw = c(self.x['J0']).replace(b'"record_index":0', b'"record_index":0.0')
        self.error('TYPE', p.decode_journal_frame, self.raw_frame(raw), KEY)

    def test_missing_and_wrong_length_keys(self):
        for key in (None, b'', b'x' * 31, b'x' * 33, 'x' * 32):
            self.error('KEY_UNAVAILABLE', p.decode_journal_frame, self.frame('J0'), key)
            self.error('KEY_UNAVAILABLE', p.frozen_command_mac, self.x['F'], key)

    def test_wrong_key_and_body_mac(self):
        self.error('MAC_MISMATCH', p.decode_journal_frame, self.frame('J0'), b'x' * 32)
        self.error('MAC_MISMATCH', p.verify_mac, self.x['F'], '0' * 64, KEY, domain='command')
        self.error('TYPE', p.verify_mac, self.x['F'], 'bad', KEY, domain='command')

    def test_constant_time_comparison_used(self):
        original = hmac.compare_digest
        with patch.object(p.hmac, 'compare_digest', wraps=original) as compare:
            p.decode_journal_frame(self.frame('J0'), KEY)
            p.verify_mac(self.x['F'], MACS['F'], KEY, domain='command')
            self.assertEqual(compare.call_count, 2)

    def test_index_gap_and_duplicate_terminal(self):
        for names in (('J0', 'J2'), ('J0', 'J1', 'J2', 'J2'), ('J0', 'JA', 'J1')):
            self.error('JOURNAL_TRANSITION_INVALID', p.verify_journal_frames, [self.frame(n) for n in names], KEY)

    def test_previous_mac_wrong_even_with_valid_signature(self):
        j = {**self.x['J1'], 'previous_record_mac': '0' * 64}
        self.error('JOURNAL_PREFIX_MISMATCH', p.verify_journal_frames, [self.frame('J0'), self.frame(j)], KEY)

    def test_epoch_context_change(self):
        j = {**self.x['J1'], 'storage_epoch_id': ROOT}
        self.error('JOURNAL_TRANSITION_INVALID', p.verify_journal_frames, [self.frame('J0'), self.frame(j)], KEY)

    def test_explicit_context_checked(self):
        context = {k: self.x['J0'][k] for k in ('production_id', 'machine_binding_id', 'storage_epoch_id', 'key_id')}
        p.decode_journal_frame(self.frame('J0'), KEY, expected_index=0, previous_mac=None, context=context)
        context['key_id'] = 'other-key'
        self.error('JOURNAL_TRANSITION_INVALID', p.decode_journal_frame, self.frame('J0'), KEY, context=context)

    def test_first_record_and_null_previous_rules(self):
        bad = {**self.x['J0'], 'previous_record_mac': '0' * 64}
        self.error('JOURNAL_TRANSITION_INVALID', p.encode_journal_frame, bad, KEY)
        bad = {**self.x['J1'], 'previous_record_mac': None}
        self.error('MISSING_FIELD', p.encode_journal_frame, bad, KEY)

    def test_abort_core_mismatch(self):
        bad = copy.deepcopy(self.x['JA']); bad['payload']['abort_code'] = 'REVALIDATION_FAILED'
        self.error('JOURNAL_TRANSITION_INVALID', p.decode_journal_frame, self.frame(bad), KEY)

    def test_frame_size_bound_during_encoding(self):
        # Bound independently exercisable without expanding any closed record schema.
        with patch.object(p, 'MAX_FRAME_PAYLOAD', 411):
            self.error('LIMIT', p.encode_journal_frame, self.x['J0'], KEY)

    def test_no_successful_result_on_partial_chain_validation(self):
        broken = self.frame('J2')[:-1]
        self.error('WIRE_FORMAT', p.verify_journal_frames, [self.frame('J0'), self.frame('J1'), broken], KEY)


class AdditionalPrimitives(ProtocolTestCase):
    def test_approval_wire_digest_independent_literal(self):
        # Additional public fixture, expected SHA computed independently by OpenSSL.
        value = {'id': R, 'gate': 'SCRIPT', 'object_ref': {'kind': 'script', 'id': P, 'revision': 1, 'content_hash': '0' * 64},
                 'dependency_digest': '1' * 64, 'policy_version': 'fixture-review-v1', 'actor': ACTOR,
                 'timestamp': AT, 'decision': 'approve', 'reason': 'synthetic only',
                 'review_declarations': ['NO_UNSUPPORTED_REVIEW_CLAIM']}
        original = copy.deepcopy(value)
        self.assertEqual(p.approval_wire_digest(value), '7198d68c971f75a7a7f70afe6b4ce6eb7408c706b4b68910d7f37cfc662a0d57')
        self.assertEqual(value, original)
        self.error('UNKNOWN_FIELD', p.approval_wire_digest, {**value, 'authorized': True})

    def test_exact_all_twelve_gate_decision_frozen_scopes(self):
        from editorial.schema2_model import required_declaration_codes
        for gate in ('SCRIPT', 'SCENES', 'HANDOFF'):
            for decision in ('approve', 'reject', 'revise', 'revoke'):
                with self.subTest(gate=gate, decision=decision):
                    f = copy.deepcopy(self.x['F'])
                    key = {'gate': gate, 'policy_version': 'fixture-review-v1',
                           'object_ref': {'kind': 'script', 'id': P, 'revision': 1, 'content_hash': '0' * 64}, 'dependency_digest': '1' * 64}
                    q = f['request']
                    q.update(operation='RECORD_DECISION', storage_epoch_id=E, expected_head=self.x['CH'], review_session_id=ROOT,
                             parameters={'decision_key': key, 'decision': decision, 'reason': 'synthetic', 'reconsiders_record_id': None})
                    f['request_sha256'] = p.request_digest(q)
                    f['assigned_ids'] = {'approval_id': POLICY, 'event_id': CONNECTION}
                    f['expected_result'] = {**f['expected_result'], 'generation': 2, 'tx_seq': 1}
                    f['authorization'].update(command_grants=['PROTECTED_SNAPSHOT_WRITE', 'RECORD_DECISION'],
                                              gate_decision_grant={'gate': gate, 'decision': decision})
                    f['review_snapshot'] = {'session_id': ROOT, 'principal_id': PRINCIPAL, 'policy_ref': f['authorization']['policy_ref'],
                                            'decision_key': key, 'confirmed_codes': list(required_declaration_codes(gate, decision)),
                                            'review_declarations': ['synthetic confirmation'], 'reconsiders_record_id': None,
                                            'server_incarnation_id': CONNECTION, 'state': 'READY'}
                    p.frozen_command_mac(f, KEY)  # Structural evidence, not a real policy grant.
                    bad = copy.deepcopy(f); bad['authorization']['gate_decision_grant'] = None
                    self.error('AUTHORIZATION_BINDING_MISMATCH', p.frozen_command_mac, bad, KEY)
                    bad = copy.deepcopy(f); bad['authorization']['gate_decision_grant']['decision'] = 'approve' if decision != 'approve' else 'revoke'
                    self.error('AUTHORIZATION_BINDING_MISMATCH', p.frozen_command_mac, bad, KEY)
                    bad = copy.deepcopy(f); bad['review_snapshot']['confirmed_codes'] = ['UNKNOWN_CODE']
                    self.error('TYPE', p.frozen_command_mac, bad, KEY)

    def test_body_keys_are_explicit_for_every_mac_domain(self):
        for name, function in [('F', p.frozen_command_mac), ('I0', p.initialization_mac), ('T0', p.registration_mac),
                               ('A1', p.anchor_mac), ('RC', p.receipt_mac), ('J0', p.journal_frame_mac)]:
            self.error('KEY_UNAVAILABLE', function, self.x[name], None)

    def test_import_executes_no_io_key_generation_or_network(self):
        import inspect
        import os
        import socket
        source = inspect.getsource(p)
        namespace = {'__name__': 'editorial.storage_protocol_v1_probe', '__package__': 'editorial'}
        with patch('builtins.open', side_effect=AssertionError('file IO')), \
             patch.object(os, 'urandom', side_effect=AssertionError('key generation')), \
             patch.object(socket, 'socket', side_effect=AssertionError('network')):
            exec(compile(source, '<storage-protocol-import-probe>', 'exec'), namespace)

    def test_mac_functions_do_not_mutate_inputs(self):
        original = copy.deepcopy(self.x)
        p.frozen_command_mac(self.x['F'], KEY)
        p.initialization_mac(self.x['I0'], KEY)
        p.encode_journal_frame(self.x['J0'], KEY)
        self.assertEqual(self.x, original)

    def test_reference_indices_must_precede_terminal(self):
        j = copy.deepcopy(self.x['J2']); j['payload']['intent_ref']['record_index'] = 2
        self.error('JOURNAL_TRANSITION_INVALID', p.decode_journal_frame, self.frame(j), KEY)

    def test_input_and_bound_types_are_strict(self):
        self.error('TYPE', p.decode_canonical_json, '{}')
        self.error('TYPE', p.decode_journal_frame, bytearray(self.frame('J0')), KEY)
        self.error('LIMIT', p.canonical_json, {}, max_bytes=True)
        self.error('LIMIT', p.decode_canonical_json, b'')
        self.error('TYPE', p.verify_journal_frames, [], KEY)
        self.error('TYPE', p.blob_ref, 'bytes')

    def test_file_observation_closed_contract_shape(self):
        p.validate_wire({'state': 'PRESENT', 'file_ref': ref(self.x['S'])}, 'FileObservation')
        self.error('UNKNOWN_FIELD', p.validate_wire, {'state': 'PRESENT', **ref(self.x['S'])}, 'FileObservation')


if __name__ == '__main__':
    unittest.main()
