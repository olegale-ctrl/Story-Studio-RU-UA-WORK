"""Independent LAB byte oracles and fail-closed buffer tests (PURE_ONLY)."""
import copy
import hashlib
import json
import unittest
from unittest.mock import patch

from editorial import storage_protocol_v1 as s1
from editorial.windows_lab import protocol as p
from tests.test_storage_protocol_v1 import fixtures

RUN = 'a1111111-1111-4111-8111-111111111111'
INC = 'c3333333-3333-4333-8333-333333333333'
HELLO = b'{"kind":"HELLO","lab_version":1,"nonce":"b2222222-2222-4222-8222-222222222222","run_id":"a1111111-1111-4111-8111-111111111111","scope":"STORY_STUDIO_S3_2_LAB"}'
HELLO_RESULT = b'{"fixture_case":{"fault_case":"NONE","policy_case":"CG_NONE"},"fixture_set":"S32_FIXTURES_1","incarnation_id":"c3333333-3333-4333-8333-333333333333","kind":"HELLO_RESULT","lab_only":true,"lab_version":1,"limits_id":"LAB_LIMITS_1","nonce":"b2222222-2222-4222-8222-222222222222","run_id":"a1111111-1111-4111-8111-111111111111","scope":"STORY_STUDIO_S3_2_LAB"}'
ACK = b'{"kind":"ACK","lab_version":1,"response_sha256":"812089bdaef8791dd8127ca21bd771e65c48d5c78a41577c125af38f7604f119","run_id":"a1111111-1111-4111-8111-111111111111","scope":"STORY_STUDIO_S3_2_LAB"}'


def frame(raw):
    return b'SSLB' + len(raw).to_bytes(4, 'big') + raw


def wire(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


class LabProtocol(unittest.TestCase):
    def test_three_literal_oracles(self):
        vectors = [(HELLO,159,'53534c420000009f','b6b3da12fd7423f404ccf700476499c4af9e3a9ba84a6716a02e0ce8b78cdccf'),
                   (HELLO_RESULT,357,'53534c4200000165','812089bdaef8791dd8127ca21bd771e65c48d5c78a41577c125af38f7604f119'),
                   (ACK,195,'53534c42000000c3','ad5152df65e4b22d874736635590a422c780024046598df3fa22deacd7b716d2')]
        for raw,n,header,digest in vectors:
            with self.subTest(kind=json.loads(raw)['kind']):
                self.assertEqual(len(raw),n)
                self.assertEqual(hashlib.sha256(raw).hexdigest(),digest)
                self.assertEqual(p.encode_lab(json.loads(raw)),bytes.fromhex(header)+raw)
                self.assertEqual(p.decode_lab(bytes.fromhex(header)+raw),json.loads(raw))
        self.assertEqual(p.response_hash(frame(HELLO_RESULT)),json.loads(ACK)['response_sha256'])
        self.assertNotEqual(p.response_hash(frame(HELLO_RESULT)),hashlib.sha256(frame(HELLO_RESULT)).hexdigest())

    def test_nul_discriminator(self):
        self.assertEqual(p.lab_summary_sha256(b'{}'),'66c044a3fa04b1baa95c05de618167622684843f04c4dde11e70add46870bcea')
        wrong = hashlib.sha256(b'story-studio-s3-2-lab-result-v1'+bytes.fromhex('5c783030')+b'{}').hexdigest()
        self.assertEqual(wrong,'8acda446a8aae48decc364502a3b476565fd8e9b3048a950ce6c5ec2e4854e25')
        self.assertNotEqual(p.lab_summary_sha256(b'{}'),wrong)
        for value in ('{}',bytearray(b'{}'),None):
            with self.assertRaises(TypeError):p.lab_summary_sha256(value)

    def test_frames_reject_before_parse(self):
        invalid = [b'', b'SSLB', b'SSJ1'+len(HELLO).to_bytes(4,'big')+HELLO,
                   b'SSLB'+bytes(4),b'SSLB'+(p.MAX_EXECUTE+1).to_bytes(4,'big'),
                   frame(HELLO)[:-1],frame(HELLO)+b'x',frame(HELLO)*2]
        with patch.object(p,'_parse',side_effect=AssertionError('must not parse')):
            for raw in invalid:
                with self.subTest(raw=raw[:8]),self.assertRaises(p.LabError):p.decode_lab(raw)

    def test_strict_json_negatives(self):
        raws = [b'\xef\xbb\xbf'+HELLO,b'\xff',HELLO+b' ',HELLO.replace(b'1,',b'1.0,',1),
                HELLO.replace(b'1,',b'true,',1),HELLO.replace(b'1,',b'NaN,',1),
                HELLO.replace(b'1,',b'Infinity,',1),HELLO.replace(b'1,',b'-Infinity,',1),
                HELLO.replace(b'{',b'{"kind":"HELLO",',1),HELLO.replace(b'"HELLO"',b'"\\ud800"'),
                b'{ "kind":"HELLO"}',b'[]',b'null',b'{"n":-0}',b'{"n":01}']
        for raw in raws:
            with self.subTest(raw=raw[:50]),self.assertRaises(p.LabError):p.decode_lab(frame(raw))

    def test_all_schemas_closed(self):
        request = fixtures()['Q']
        messages = [json.loads(HELLO),json.loads(HELLO_RESULT),json.loads(ACK),
            {'lab_version':1,'scope':p.SCOPE,'kind':'EXECUTE','run_id':RUN,'incarnation_id':INC,'request':request},
            {'lab_version':1,'scope':p.SCOPE,'kind':'LOOKUP','run_id':RUN,'incarnation_id':INC,'request_id':request['request_id'],'request_bytes_sha256':'0'*64},
            {'lab_version':1,'scope':p.SCOPE,'kind':'RESULT','run_id':RUN,'incarnation_id':INC,'request_id':None,'request_bytes_sha256':None,
             'outcome':'DENIED','mock_admission':'NONE','mock_summary':None,'error':{'code':'LAB_POLICY_DENIED','field_path':'$','s1_code':None},'lab_only':True}]
        for message in messages:
            self.assertEqual(p.decode_lab(p.encode_lab(message)),message)
            for key in message:
                bad=copy.deepcopy(message);del bad[key]
                with self.subTest(kind=message['kind'],missing=key),self.assertRaises(p.LabError):p.encode_lab(bad)
            for key,value in [('extra',0),('principal','A'),('policy_case','CG_INIT'),('fault_case','NONE'),('fixture','any')]:
                bad={**message,key:value}
                with self.assertRaises(p.LabError):p.encode_lab(bad)
        for field,value in [('lab_version',True),('lab_version',2),('run_id',RUN.upper()),('scope','production'),('kind','INVALID')]:
            bad=json.loads(HELLO);bad[field]=value
            with self.assertRaises(p.LabError):p.encode_lab(bad)

    def test_nested_s1_and_unicode(self):
        value={'lab_version':1,'scope':p.SCOPE,'kind':'EXECUTE','run_id':RUN,'incarnation_id':INC,'request':fixtures()['Q']}
        for change in ({'request_version':True},{'unknown':0},{'operation':'UNKNOWN'},{'request_id':None}):
            bad=copy.deepcopy(value);bad['request'].update(change)
            with self.assertRaises(p.LabError):p.encode_lab(bad)
        for text in ['Ї','И\u0306','é','e\u0301']:
            q=copy.deepcopy(value);q['request']['operation']='PUBLISH_REVISION';q['request']['parameters']={'reason':text,'proposal_ref':{'sha256':'0'*64,'byte_length':1}}
            self.assertEqual(p.decode_lab(p.encode_lab(q)),q)
        self.assertNotEqual(p.canonical({'s':'é'}),p.canonical({'s':'e\u0301'}))

    def test_container_depth_bounds(self):
        def nested(n):
            v=0
            for _ in range(n):v=[v]
            return v
        self.assertEqual(p._parse(p.canonical({'x':nested(64)})),{'x':nested(64)})
        with self.assertRaises(p.LabError):p.canonical({'x':nested(65)})
        with self.assertRaises(p.LabError):p._parse(b'{"x":'+b'['*65+b'0'+b']'*65+b'}')
        with self.assertRaises(s1.ProtocolError):s1.canonical_json({'x':nested(64)})

    def test_sizes_types_and_summary_relations(self):
        with self.assertRaises(p.LabError):p.decode_lab(bytearray(frame(HELLO)))
        with self.assertRaises(p.LabError):p.encode_lab({**json.loads(HELLO),'nonce':'x'*4097})
        for bad in [1.5,object(),{1:'x'}, {'x':'\ud800'}]:
            with self.assertRaises(p.LabError):p.canonical(bad)
        result={'lab_version':1,'scope':p.SCOPE,'kind':'RESULT','run_id':RUN,'incarnation_id':INC,'request_id':None,'request_bytes_sha256':None,
                'outcome':'MOCK_FINALIZED','mock_admission':'RAM','mock_summary':{'operation':'RECORD_DECISION','status':'COMMITTED','virtual_record_count':2**64-1,'value_sha256':'0'*64},'error':None,'lab_only':True}
        self.assertEqual(p.decode_lab(p.encode_lab(result)),result)
        for n in [True,-1,2**64,1.0]:
            bad=copy.deepcopy(result);bad['mock_summary']['virtual_record_count']=n
            with self.assertRaises(p.LabError):p.encode_lab(bad)
        for field,value in [('lab_only',1),('mock_admission','NONE'),('outcome','MOCK_ABORTED'),('error',{'code':'UNKNOWN','field_path':'$','s1_code':None})]:
            with self.assertRaises(p.LabError):p.encode_lab({**result,field:value})
        with self.assertRaises(s1.ProtocolError):s1.validate_wire(result,'Receipt')

    def test_exact_max_frame_boundary_and_small_kind_budget(self):
        body=b' '*p.MAX_EXECUTE
        with patch.object(p,'_parse',side_effect=p.LabError()) as parse:
            with self.assertRaises(p.LabError):p.decode_lab(frame(body))
            parse.assert_called_once_with(body)
        # At-limit buffer reaches parsing; over-limit header never does.
        with patch.object(p,'_parse',side_effect=AssertionError('over-limit parse')):
            with self.assertRaises(p.LabError):p.decode_lab(frame(body+b' '))
        # Canonical padding cannot enlarge a closed small message into EXECUTE budget.
        hello=json.loads(HELLO)
        hello['padding']='x'*4096
        with self.assertRaises(p.LabError):p.decode_lab(frame(wire(hello)))
        execute={'lab_version':1,'scope':p.SCOPE,'kind':'EXECUTE','run_id':RUN,'incarnation_id':INC,'request':fixtures()['Q']}
        execute['request']['parameters']['draft_ref']['byte_length']=2**64
        with self.assertRaises(p.LabError):p.encode_lab(execute)

    def test_nested_result_error_and_case_schemas(self):
        hello=json.loads(HELLO_RESULT)
        for field,value in [('policy_case','unknown'),('fault_case','unknown'),('extra',1)]:
            bad=copy.deepcopy(hello);bad['fixture_case'][field]=value
            with self.assertRaises(p.LabError):p.encode_lab(bad)
        result={'lab_version':1,'scope':p.SCOPE,'kind':'RESULT','run_id':RUN,'incarnation_id':INC,'request_id':None,'request_bytes_sha256':None,
                'outcome':'UNKNOWN_AFTER_RESTART','mock_admission':'UNKNOWN','mock_summary':None,
                'error':{'code':'LAB_RESTART_UNKNOWN','field_path':'$','s1_code':'OUTCOME_UNKNOWN'},'lab_only':True}
        self.assertEqual(p.decode_lab(p.encode_lab(result)),result)
        for field,value in [('code','arbitrary'),('s1_code','arbitrary'),('field_path',''),('field_path','é'),('field_path','$'+'x'*1024),('extra',0)]:
            bad=copy.deepcopy(result);bad['error'][field]=value
            with self.assertRaises(p.LabError):p.encode_lab(bad)
        bad=copy.deepcopy(result);bad['error']['code']='LAB_ENGINE_FAILURE'
        with self.assertRaises(p.LabError):p.encode_lab(bad)
