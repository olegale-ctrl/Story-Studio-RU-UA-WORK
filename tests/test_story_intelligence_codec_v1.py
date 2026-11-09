"""Literal SI/1 byte/hash oracles and strict single-object codec boundaries."""
import copy
import hashlib
import sys
import unittest

from editorial.storage_protocol_v1 import canonical_json as storage_canonical_json
from story_intelligence.codec_v1 import (canonical_si_json as encode,
    decode_canonical_si_json as decode, canonical_si_sha256 as digest)
from story_intelligence.model_v1 import SIValidationError

# Fixed literals generated once via stdlib json (not SI/S1), manually checked
# for ordering/Unicode; every digest independently cross-checked with openssl
# dgst -sha256. No golden calculation/import of production code at definition.
VECTORS = [
    ('null', None, b'null', '74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b'),
    ('bool', True, b'true', 'b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b'),
    ('empty_object', {}, b'{}', '44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a'),
    ('ru', {'тема': 'История'}, b'{"\xd1\x82\xd0\xb5\xd0\xbc\xd0\xb0":"\xd0\x98\xd1\x81\xd1\x82\xd0\xbe\xd1\x80\xd0\xb8\xd1\x8f"}', '6f01df1fb172b95c2a75ff3cfa19b99f4fe0d94e3c0251b074fb9debe386e40a'),
    ('uk', {'мова': 'українська', 'текст': 'ї є і ґ'}, b'{"\xd0\xbc\xd0\xbe\xd0\xb2\xd0\xb0":"\xd1\x83\xd0\xba\xd1\x80\xd0\xb0\xd1\x97\xd0\xbd\xd1\x81\xd1\x8c\xd0\xba\xd0\xb0","\xd1\x82\xd0\xb5\xd0\xba\xd1\x81\xd1\x82":"\xd1\x97 \xd1\x94 \xd1\x96 \xd2\x91"}', 'fe18d33c100403ab259f25eefeca016022f9114f03f8b05ab8df00dd61c220d1'),
    ('emoji', '🎬😀', b'"\xf0\x9f\x8e\xac\xf0\x9f\x98\x80"', '82a9b898dfbc0ca24e6ffe78bbda640742135813ef6af94722e45d9b70f30e91'),
    ('nested', {'z': [{'b': 2, 'a': 1}], 'a': {'я': 'є', 'b': False}}, b'{"a":{"b":false,"\xd1\x8f":"\xd1\x94"},"z":[{"a":1,"b":2}]}', '7caf087dc8a9ef28a945db13274c4c49c8acd14cd862d95c6502d3205857c944'),
    ('ordered_array', [3, 1, 2, None, False], b'[3,1,2,null,false]', '59ae47319921f2bbfc45d566ef89f64e4df537f9a47987c8c72c1ff4ee0e6c88'),
    ('nfc', 'é', b'"\xc3\xa9"', 'f2886017e9c7abacf804b54d64787dce2b611c9544ba21f3affdd126a6e50086'),
    ('nfd', 'é', b'"e\xcc\x81"', '3d68ce21f2899a475713cdbe7562ba9bdb6b1dfde8af1f221bdff4a0935b53b2'),
    ('large_integer', 9007199254740993123456789, b'9007199254740993123456789', '789f9bdb4eb978eaca4e54b39d93c41454082f195c5cabc01825ef437d8ca1a4'),
    ('negative_integer', -18446744073709551617, b'-18446744073709551617', 'd827571c52ff0e00bedd6c601b24e451806ad410464f906fc38a46423e634053'),
    ('escapes', '"\\\n\t\x00', b'"\\"\\\\\\n\\t\\u0000"', 'c90e7596e2a2517e70d0077002a923dde70e01ccedef2db7da7985d1f54a7c85'),
    ('synthetic_header_payload', {'H': {'si_version': 1, 'type': 'Intake', 'id': '11111111-1111-4111-8111-111111111111', 'revision': 1, 'previous': None, 'created_at': '2026-11-09T00:00:00Z', 'creator_label': 'Автор', 'origin': {'mode': 'MANUAL_INPUT', 'run_ref': None, 'imported_from': None}, 'input_refs': [], 'editorial_refs': []}, 'payload': {'note': 'synthetic JSON only; NOT typed record validation'}}, b'{"H":{"created_at":"2026-11-09T00:00:00Z","creator_label":"\xd0\x90\xd0\xb2\xd1\x82\xd0\xbe\xd1\x80","editorial_refs":[],"id":"11111111-1111-4111-8111-111111111111","input_refs":[],"origin":{"imported_from":null,"mode":"MANUAL_INPUT","run_ref":null},"previous":null,"revision":1,"si_version":1,"type":"Intake"},"payload":{"note":"synthetic JSON only; NOT typed record validation"}}', '863bf574f6768027a703cc822c09ea2e3f9d4401048764db93bbec83d67ba7d2'),
]


class CodecTests(unittest.TestCase):
    def rejected(self, fn, value, code='TYPE', path=None):
        with self.assertRaises(SIValidationError) as caught:
            fn(value)
        self.assertEqual(code, caught.exception.code)
        if path is not None:
            self.assertEqual(path, caught.exception.path)

    def test_literal_vectors(self):
        self.assertEqual(14, len(VECTORS))
        for name, value, wire, sha in VECTORS:
            with self.subTest(vector=name):
                self.assertEqual(wire, encode(value))
                self.assertEqual(sha, digest(value))
                self.assertEqual(value, decode(wire))
                self.assertEqual(wire, encode(decode(wire)))
                # Additional reference SHA computation, not expected-value creation.
                self.assertEqual(sha, hashlib.sha256(wire).hexdigest())

    def test_shared_storage_subset_parity(self):
        for name, value, wire, _ in VECTORS:
            with self.subTest(vector=name):
                self.assertEqual(wire, storage_canonical_json(value))
                self.assertEqual(storage_canonical_json(value), encode(value))

    def test_unicode_is_not_normalized(self):
        self.assertNotEqual(encode('é'), encode('e\u0301'))
        self.assertNotEqual(digest('é'), digest('e\u0301'))
        # Unicode codepoint ordering, including astral vs BMP keys.
        self.assertEqual('{"\ue000":1,"😀":2}'.encode(), encode({'😀':2,'\ue000':1}))

    def test_invalid_and_noncanonical_bytes(self):
        cases = [b'', b'\xff', b'\xef\xbb\xbf{}', b' {}', b'{}\n',
            b'{"b":1,"a":2}', b'{"a": 1}', b'"\\u0061"',
            b'"\\/"', b'-0', b'01', b'+1', b'1.0', b'1e2',
            b'NaN', b'Infinity', b'-Infinity', b'null null',
            b'{"a":1,"a":2}', b'{"a":1,"\\u0061":2}',
            b'"\\ud800"', b'"\\udc00"', b'"\\ud83d\\ude00"',
            b'"\xed\xa0\x80"', b'[1,]', b'{', b'"\x01"']
        for wire in cases:
            with self.subTest(wire=wire):
                self.rejected(decode, wire)

    def test_exact_types_and_subclasses(self):
        class D(dict): pass
        class L(list): pass
        class S(str): pass
        class I(int): pass
        class B(bytes): pass
        for value in (0.0, float('nan'), float('inf'), (), set(), b'{}',
                      D(), L(), S('a'), I(1), {1:'x'}, {S('a'):1}):
            with self.subTest(value=type(value)):
                self.rejected(encode, value)
        for data in ('{}', bytearray(b'{}'), memoryview(b'{}'), B(b'{}')):
            self.rejected(decode, data)
        self.assertEqual(b'[true,1,false,0,null]', encode([True,1,False,0,None]))

    def test_surrogates_and_error_path(self):
        for value in ('\ud800', '\udfff', {'\ud800':1}):
            self.rejected(encode, value)
        self.rejected(encode, {'a':[{'b':0.5}]}, path='$.a[0].b')
        self.rejected(decode, b'{"a":{"b":1,"b":2}}', path='$.a.b')

    def test_text_and_key_codepoint_limits(self):
        self.assertEqual('ї'*100_000, decode(encode('ї'*100_000)))
        self.assertEqual({'a'*100_000:0}, decode(encode({'a'*100_000:0})))
        for value in ('a'*100_001, {'a'*100_001:0}):
            self.rejected(encode, value, 'LIMIT')
        self.rejected(decode, b'"'+b'a'*100_001+b'"', 'LIMIT')
        self.rejected(decode, b'{"'+b'a'*100_001+b'":0}', 'LIMIT')

    def test_exact_byte_budget(self):
        # 10 strings, each within Text limit; exact total 1000000 bytes.
        value = ['a'*100_000]*9 + ['b'*99_969]
        wire = encode(value)
        self.assertEqual(1_000_000, len(wire))
        self.assertEqual(value, decode(wire))
        oversized = value[:-1]+[value[-1]+'b']
        self.rejected(encode, oversized, 'LIMIT')
        self.rejected(decode, wire+b' ', 'LIMIT')
        # SI byte cap is intentionally stricter than S1 reference cap.
        self.assertEqual(1_000_001, len(storage_canonical_json(oversized)))

    def test_depth_boundary_and_cycles(self):
        value = 0
        for _ in range(32): value = [value]
        self.assertEqual(value, decode(encode(value)))
        self.rejected(encode, [value], 'LIMIT')
        self.rejected(decode, b'['*33+b'0'+b']'*33, 'LIMIT')
        self.assertEqual(encode(value), storage_canonical_json(value))
        self.assertTrue(storage_canonical_json([value]))
        cycle = []; cycle.append(cycle)
        self.rejected(encode, cycle, 'LIMIT')
        self.assertEqual('[{]}\\"', decode(encode('[{]}\\"')))

    def test_arbitrary_integer_beyond_python_decimal_guard(self):
        before = sys.get_int_max_str_digits()
        number = 10**5000 + 123
        expected = b'1'+b'0'*4997+b'123'
        self.assertEqual(expected, encode(number))
        self.assertEqual(number, decode(expected))
        self.assertEqual(b'-'+expected, encode(-number))
        self.assertEqual(-number, decode(b'-'+expected))
        self.assertEqual(before, sys.get_int_max_str_digits())
        self.rejected(encode, 1 << 4_000_001, 'LIMIT')

    def test_input_immutability(self):
        value={'я':[{'b':2,'a':1},True,None,'ї']}
        before=copy.deepcopy(value)
        encode(value); digest(value)
        self.assertEqual(before,value)
        self.assertEqual(['я'],list(value))
        self.assertEqual(['b','a'],list(value['я'][0]))


if __name__ == '__main__':
    unittest.main()
