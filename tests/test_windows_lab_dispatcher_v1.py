"""Independent authorization/state assertions, synthetic only (PURE_ONLY)."""
import copy
from dataclasses import FrozenInstanceError
import hashlib
import unittest
from unittest.mock import patch
from uuid import UUID, uuid5

from editorial import storage_protocol_v1 as s1
from editorial import storage_transaction_model_v1 as m
from editorial.windows_lab import protocol as p
from editorial.windows_lab.dispatcher import Dispatcher, Caller, DeliveryLost
from editorial.windows_lab.fixtures import Factory, PROBES, ROLES, KEY, PRINCIPALS, c
from tests.test_windows_lab_protocol_v1 import RUN, INC, HELLO

NEW_INC = 'd4444444-4444-4444-8444-444444444444'


class LabDispatcher(unittest.TestCase):
    def make(self, policy='CG_INIT', fault='NONE', incarnation=INC):
        return Dispatcher(RUN,incarnation,policy,fault)

    def send(self, d, probe='INIT_EMPTY', slot=0, actor='A'):
        frame=d.execute_frame(actor,probe,slot)
        return frame,p.decode_lab(d.dispatch(frame,Caller(actor)))

    def lookup(self, frame):
        value=p.decode_lab(frame);q=value['request']
        return p.encode_lab({'lab_version':1,'scope':p.SCOPE,'kind':'LOOKUP','run_id':RUN,
            'incarnation_id':value['incarnation_id'],'request_id':q['request_id'],
            'request_bytes_sha256':hashlib.sha256(c(q)).hexdigest()})

    def events(self,d):
        return {key:tuple(store.events) for key,store in d.factory._stores.items()}

    def assert_no_model_dispatch(self, d, frame, actor='A'):
        before = self.events(d)
        counters = d.admissions, d.model_calls
        with patch.object(m.TransactionModel, 'execute', autospec=True) as execute:
            execute.side_effect = AssertionError('S2 execute called before admission')
            response = d.dispatch(frame, Caller(actor))
            execute.assert_not_called()
        self.assertEqual(self.events(d), before)
        self.assertEqual((d.admissions, d.model_calls), counters)
        return p.decode_lab(response)

    def test_cold_policy_denials_never_seed(self):
        probe = 'GD_SCRIPT_APPROVE'
        for actor, policy in (('B', probe), ('A', 'GD_SCENES_APPROVE'),
                              ('A', 'CG_WRITER_ONLY'), ('A', 'CG_NONE')):
            with self.subTest(actor=actor, policy=policy):
                d = self.make(policy)
                frame = self.make(policy).execute_frame(actor, probe)
                self.assertEqual(d.factory._stores, {})
                result = self.assert_no_model_dispatch(d, frame, actor)
                self.assertEqual(result['error']['code'], 'LAB_POLICY_DENIED')

    def test_cold_missing_grants_never_seed(self):
        probe = 'GD_SCRIPT_APPROVE'
        frame = self.make(probe).execute_frame('A', probe)
        for missing in ('PROTECTED_SNAPSHOT_WRITE', 'RECORD_DECISION', 'gate'):
            with self.subTest(missing=missing):
                d = self.make(probe)
                policy = d.factory.policy('A')
                if missing == 'gate':
                    policy['actor_a_gate_grant'] = None
                else:
                    policy['actor_a_command_grants'].remove(missing)
                with patch.object(d.factory, 'policy', return_value=policy):
                    result = self.assert_no_model_dispatch(d, frame)
                self.assertEqual(result['error']['code'], 'LAB_POLICY_DENIED')

    def test_cold_pre_admission_faults_never_seed(self):
        probe = 'GD_SCRIPT_APPROVE'
        frame = self.make(probe).execute_frame('A', probe)
        faults = {'READ_STALL': 'LAB_BUSY', 'DISPATCH_STALL': 'LAB_BUSY',
                  'PRE_ADMISSION_DENY': 'LAB_POLICY_DENIED',
                  'IMPERSONATE_FALSE': 'LAB_POLICY_DENIED',
                  'THREAD_TOKEN_QUERY_FALSE': 'LAB_POLICY_DENIED',
                  'REVERT_FALSE': 'LAB_POLICY_DENIED',
                  'RESIDUAL_TOKEN': 'LAB_POLICY_DENIED'}
        for fault, code in faults.items():
            with self.subTest(fault=fault):
                d = self.make(probe, fault)
                result = self.assert_no_model_dispatch(d, frame)
                self.assertEqual(result['error']['code'], code)
        d = self.make(probe, 'CRASH_PRE_ADMISSION')
        with patch.object(m.TransactionModel, 'execute', autospec=True) as execute:
            execute.side_effect = AssertionError('S2 execute called before admission')
            with self.assertRaises(DeliveryLost):
                d.dispatch(frame, Caller('A'))
            execute.assert_not_called()
        self.assertEqual((self.events(d), d.admissions, d.model_calls), ({}, 0, 0))

    def test_cold_byte_mismatch_never_seeds(self):
        probe = 'GD_SCRIPT_APPROVE'
        frame = self.make(probe).execute_frame('A', probe)
        for field in ('reason', 'review_session_id'):
            with self.subTest(field=field):
                message = p.decode_lab(frame)
                if field == 'reason':
                    message['request']['parameters']['reason'] = 'Changed synthetic reason'
                else:
                    message['request'][field] = NEW_INC
                d = self.make(probe)
                result = self.assert_no_model_dispatch(d, p.encode_lab(message))
                self.assertEqual(result['error']['code'], 'LAB_FIXTURE_NOT_ALLOWED')

    def test_quarantined_cold_probe_never_seeds(self):
        probe = 'GD_SCRIPT_APPROVE'
        frame = self.make(probe).execute_frame('A', probe)
        d = self.make(probe)
        d._quarantined = True
        result = self.assert_no_model_dispatch(d, frame)
        self.assertEqual(result['error']['code'], 'LAB_BUSY')

    def test_144_gate_cells(self):
        allow=deny=0
        for policy in p.POLICIES[5:]:
            d=self.make(policy)
            for probe in PROBES[5:]:
                with self.subTest(policy=policy,probe=probe):
                    frame=d.execute_frame('A',probe)
                    baseline=self.events(d);calls=d.model_calls;admitted=d.admissions
                    result=p.decode_lab(d.dispatch(frame,Caller('A')))
                    if policy==probe:
                        self.assertEqual(result['outcome'],'MOCK_FINALIZED');allow+=1
                        self.assertEqual(d.model_calls,calls+1)
                    else:
                        self.assertEqual(result['error']['code'],'LAB_POLICY_DENIED');deny+=1
                        self.assertEqual(d.model_calls,calls);self.assertEqual(d.admissions,admitted)
                        self.assertEqual(self.events(d),baseline)
        self.assertEqual((allow,deny),(12,132))

    def test_five_command_policies_six_operations(self):
        probes=('INIT_EMPTY','IMPORT','TRANSFER','MIGRATE','RECOVERY','GD_SCRIPT_APPROVE')
        expected={'CG_INIT':{0,1,2},'CG_MIGRATE':{3},'CG_RECOVERY':{4},'CG_WRITER_ONLY':set(),'CG_NONE':set()}
        cells=0
        for policy in p.POLICIES[:5]:
            d=self.make(policy)
            for i,probe in enumerate(probes):
                with self.subTest(policy=policy,probe=probe):
                    _,result=self.send(d,probe);cells+=1
                    if i in expected[policy]:self.assertEqual(result['outcome'],'MOCK_FINALIZED')
                    else:self.assertEqual(result['error']['code'],'LAB_POLICY_DENIED')
        self.assertEqual(cells,30)

    def test_all_probes_recognized_for_all_policies_and_b_denied(self):
        for policy in p.POLICIES:
            f=Factory(INC,policy)
            for probe in PROBES:
                self.assertEqual(f.locate('A',f.ident('A',probe,0,'request')),(probe,0))
            d=self.make(policy)
            for probe in PROBES:
                frame=d.execute_frame('B',probe);baseline=self.events(d)
                result=p.decode_lab(d.dispatch(frame,Caller('B')))
                self.assertEqual(result['error']['code'],'LAB_POLICY_DENIED')
                self.assertEqual(d.model_calls,0);self.assertEqual(d.admissions,0)
                self.assertEqual(self.events(d),baseline)

    def test_each_missing_command_grant_denied(self):
        for missing in ('PROTECTED_SNAPSHOT_WRITE','INITIALIZE'):
            d=self.make();frame=d.execute_frame('A','INIT_EMPTY');original=d.factory.policy
            def policy(actor):
                value=original(actor)
                value['actor_a_command_grants']=[x for x in value['actor_a_command_grants'] if x!=missing]
                return value
            # Current provider controls admission, never the frozen candidate's minimal grants.
            with patch.object(d.factory,'policy',side_effect=policy):
                frame=d.execute_frame('A','INIT_EMPTY');before=self.events(d)
                result=p.decode_lab(d.dispatch(frame,Caller('A')))
                self.assertEqual(result['error']['code'],'LAB_POLICY_DENIED')
                self.assertEqual(self.events(d),before);self.assertEqual(d.model_calls,0)

    def test_publish_disabled_all_policies(self):
        for policy in p.POLICIES:
            d=self.make(policy);message=p.decode_lab(d.execute_frame('A','INIT_EMPTY'))
            q=message['request'];q['operation']='PUBLISH_REVISION'
            q['parameters']={'proposal_ref':q['parameters']['draft_ref'],'reason':'Synthetic disabled operation'}
            before=self.events(d)
            self.assertEqual(p.decode_lab(d.dispatch(p.encode_lab(message),Caller('A')))['error']['code'],'LAB_POLICY_DENIED')
            self.assertEqual(d.model_calls,0);self.assertEqual(d.admissions,0);self.assertEqual(before,self.events(d))

    def test_uuid_roles_slots_and_determinism(self):
        f=Factory(INC,'GD_SCRIPT_REJECT')
        for role in ROLES:
            part='seed' if role in ('production','machine','epoch','policy') else '7'
            expected=str(uuid5(UUID(INC),f'S32_FIXTURES_1/GD_SCRIPT_REJECT/A/GD_SCRIPT_REJECT/{part}/{role}'))
            self.assertEqual(f.ident('A','GD_SCRIPT_REJECT',7,role),expected)
        for args in [('A','UNKNOWN',0,'request'),('X','INIT_EMPTY',0,'request'),('A','INIT_EMPTY',1,'request'),('A','GD_SCRIPT_REJECT',64,'request'),('A','GD_SCRIPT_REJECT',True,'request'),('A','INIT_EMPTY',0,'unknown')]:
            with self.assertRaises(p.LabError):f.ident(*args)
        a=self.make();b=self.make()
        self.assertEqual(a.execute_frame('A','INIT_EMPTY'),b.execute_frame('A','INIT_EMPTY'))
        with self.assertRaises(p.LabError):Factory(INC,'UNKNOWN')
        with self.assertRaises(p.LabError):Factory(INC,'CG_INIT','UNKNOWN')

    def test_replay_exact_bytes_lookup_and_lost_ack(self):
        d=self.make();frame=d.execute_frame('A','INIT_EMPTY')
        first=d.dispatch(frame,Caller('A'));events=self.events(d)
        # Caller does not acknowledge delivery; pure dispatcher retains the result.
        with patch.object(d.factory,'allowed',side_effect=AssertionError('Replay must not reauthorize')):
            for _ in range(3):
                self.assertEqual(d.dispatch(frame,Caller('A')),first)
                self.assertEqual(d.dispatch(self.lookup(frame),Caller('A')),first)
        self.assertEqual(d.model_calls,1);self.assertEqual(d.admissions,1);self.assertEqual(self.events(d),events)
        with self.assertRaises(FrozenInstanceError):Caller('A').actor='B'
        with self.assertRaises(p.LabError):d.dispatch(frame,{'actor':'A'})

    def test_principal_bytes_session_conflicts_and_digest_only_lookup(self):
        d=self.make('GD_SCRIPT_APPROVE');frame=d.execute_frame('A','GD_SCRIPT_APPROVE');d.dispatch(frame,Caller('A'));events=self.events(d)
        for change in ({'review_session_id':NEW_INC},{'parameters':{**p.decode_lab(frame)['request']['parameters'],'reason':'different'}}):
            msg=p.decode_lab(frame);msg['request'].update(change)
            result=p.decode_lab(d.dispatch(p.encode_lab(msg),Caller('A')))
            self.assertEqual(result['error']['code'],'LAB_IDEMPOTENCY_CONFLICT')
        for raw,actor in [(frame,'B'),(self.lookup(frame),'B')]:
            self.assertEqual(p.decode_lab(d.dispatch(raw,Caller(actor)))['error']['code'],'LAB_IDEMPOTENCY_CONFLICT')
        lookup=p.decode_lab(self.lookup(frame));lookup['request_bytes_sha256']='0'*64
        self.assertEqual(p.decode_lab(d.dispatch(p.encode_lab(lookup),Caller('A')))['error']['code'],'LAB_IDEMPOTENCY_CONFLICT')
        self.assertEqual(d.model_calls,1);self.assertEqual(events,self.events(d))

    def test_run_incarnation_and_rewrapped_old_request(self):
        old=self.make();frame=old.execute_frame('A','INIT_EMPTY');new=self.make(incarnation=NEW_INC)
        for raw in (frame,self.lookup(frame)):
            result=p.decode_lab(new.dispatch(raw,Caller('A')))
            self.assertEqual((result['outcome'],result['mock_admission']),('UNKNOWN_AFTER_RESTART','UNKNOWN'))
        msg=p.decode_lab(frame);msg['incarnation_id']=NEW_INC
        self.assertEqual(p.decode_lab(new.dispatch(p.encode_lab(msg),Caller('A')))['error']['code'],'LAB_FIXTURE_NOT_ALLOWED')
        msg['run_id']=NEW_INC
        self.assertEqual(p.decode_lab(new.dispatch(p.encode_lab(msg),Caller('A')))['error']['code'],'LAB_RUN_MISMATCH')
        self.assertEqual(new.model_calls,0);self.assertEqual(new.admissions,0)
        self.assertEqual(p.decode_lab(new.dispatch(__import__('tests.test_windows_lab_protocol_v1',fromlist=['frame']).frame(HELLO),Caller('A')))['kind'],'HELLO_RESULT')

    def test_capacity_32_then_33_and_no_eviction(self):
        d=self.make('GD_SCRIPT_REJECT');frames=[];responses=[]
        for slot in range(32):
            frame=d.execute_frame('A','GD_SCRIPT_REJECT',slot);frames.append(frame)
            response=d.dispatch(frame,Caller('A'));responses.append(response)
            self.assertEqual(p.decode_lab(response)['outcome'],'MOCK_FINALIZED')
        before=self.events(d)
        extra=d.execute_frame('A','GD_SCRIPT_REJECT',32)
        # Creating an on-demand candidate does not mutate its current seed state.
        self.assertEqual(before,self.events(d))
        self.assertEqual(p.decode_lab(d.dispatch(extra,Caller('A')))['error']['code'],'LAB_CAPACITY')
        self.assertEqual(d.admissions,32);self.assertEqual(d.model_calls,32)
        # Switch the trusted live gate grant so a different, cold probe reaches quota.
        cold_probe = 'GD_SCENES_REJECT'
        helper = self.make('GD_SCRIPT_REJECT')
        policy = helper.factory.policy('A')
        policy['actor_a_gate_grant'] = {'gate': 'SCENES', 'decision': 'reject'}
        with patch.object(helper.factory, 'policy', return_value=policy):
            cold_frame = helper.execute_frame('A', cold_probe)
        self.assertNotIn(('A', cold_probe), d.factory._stores)
        with patch.object(d.factory, 'policy', return_value=policy):
            result = self.assert_no_model_dispatch(d, cold_frame)
        self.assertEqual(result['error']['code'], 'LAB_CAPACITY')
        for frame,response in zip(frames,responses):
            self.assertEqual(d.dispatch(frame,Caller('A')),response)
            self.assertEqual(d.dispatch(self.lookup(frame),Caller('A')),response)
        self.assertEqual(before,self.events(d))

    def test_denials_do_not_grow_cache_and_unknown_lookup(self):
        d=self.make('CG_NONE');frame=d.execute_frame('A','INIT_EMPTY');before=self.events(d)
        for _ in range(100):
            self.assertEqual(p.decode_lab(d.dispatch(frame,Caller('A')))['error']['code'],'LAB_POLICY_DENIED')
        self.assertEqual(d.admissions,0);self.assertEqual(d.model_calls,0);self.assertEqual(before,self.events(d))
        self.assertEqual(p.decode_lab(d.dispatch(self.lookup(frame),Caller('A')))['error']['code'],'LAB_NOT_FOUND')

    def test_prepare_and_intent_pending_never_recover(self):
        for fault,terminal in [('PAUSE_AFTER_RAM_PREPARE','PREPARE'),('PAUSE_AFTER_RAM_INTENT','PUBLISH_INTENT')]:
            d=self.make(fault=fault);frame=d.execute_frame('A','INIT_EMPTY')
            with patch.object(m.TransactionModel,'recover',side_effect=AssertionError('no recovery')):
                response=d.dispatch(frame,Caller('A'));result=p.decode_lab(response)
                self.assertEqual((result['outcome'],result['mock_admission']),('MOCK_PENDING','RAM'))
                self.assertIsNone(result['mock_summary']);self.assertIsNone(result['error'])
                store=d.factory._stores[('A','INIT_EMPTY')]
                records=[s1.decode_journal_frame(raw,KEY)['record_type'] for raw in store.visible.journal]
                self.assertEqual(records[-1],terminal);self.assertNotIn('GENESIS',records)
                events=self.events(d)
                self.assertEqual(d.dispatch(frame,Caller('A')),response)
                self.assertEqual(d.dispatch(self.lookup(frame),Caller('A')),response)
                self.assertEqual(events,self.events(d));self.assertEqual(d.model_calls,1)

    def test_loss_and_crash_cases(self):
        for fault in ('RESPONSE_LOSS','CRASH_AFTER_RAM_FINAL','CRASH_PRE_ADMISSION'):
            d=self.make(fault=fault);frame=d.execute_frame('A','INIT_EMPTY')
            with self.assertRaises(DeliveryLost):d.dispatch(frame,Caller('A'))
            self.assertEqual(d.admissions,0 if fault=='CRASH_PRE_ADMISSION' else 1)
            if fault=='RESPONSE_LOSS':
                self.assertEqual(p.decode_lab(d.dispatch(frame,Caller('A')))['outcome'],'MOCK_FINALIZED')
                self.assertEqual(d.model_calls,1)
            if fault != 'RESPONSE_LOSS':
                with self.assertRaises(DeliveryLost):d.dispatch(frame,Caller('A'))
            restarted=self.make(incarnation=NEW_INC)
            self.assertEqual(p.decode_lab(restarted.dispatch(frame,Caller('A')))['outcome'],'UNKNOWN_AFTER_RESTART')
            self.assertEqual(restarted.admissions,0);self.assertEqual(restarted.model_calls,0)

    def test_pre_admission_pure_faults(self):
        for fault in ('PRE_ADMISSION_DENY','DISPATCH_STALL','READ_STALL','IMPERSONATE_FALSE','THREAD_TOKEN_QUERY_FALSE','REVERT_FALSE','RESIDUAL_TOKEN'):
            d=self.make(fault=fault);frame=d.execute_frame('A','INIT_EMPTY');events=self.events(d)
            result=p.decode_lab(d.dispatch(frame,Caller('A')))
            self.assertIn(result['outcome'],('DENIED','NOT_ADMITTED'))
            self.assertEqual(d.admissions,0);self.assertEqual(d.model_calls,0);self.assertEqual(events,self.events(d))
        d=self.make();frame=d.execute_frame('A','INIT_EMPTY');d._lock.acquire()
        try:self.assertEqual(p.decode_lab(d.dispatch(frame,Caller('A')))['error']['code'],'LAB_BUSY')
        finally:d._lock.release()
        self.assertEqual(d.model_calls,0)

    def test_real_receipt_nul_and_lab_separation(self):
        d=self.make();frame=d.execute_frame('A','INIT_EMPTY');captured=[]
        original=p.lab_summary_sha256
        def capture(raw):captured.append(raw);return original(raw)
        with patch.object(p,'lab_summary_sha256',side_effect=capture):response=d.dispatch(frame,Caller('A'))
        self.assertEqual(len(captured),1);raw=captured[0];receipt=s1.decode_canonical_json(raw)
        s1.validate_wire(receipt,'Receipt');self.assertEqual(s1.canonical_json(receipt),raw)
        s1.verify_mac(receipt['body'],receipt['mac'],KEY,domain='receipt')
        digest=hashlib.sha256(b'story-studio-s3-2-lab-result-v1'+bytes([0])+raw).hexdigest()
        wrong=hashlib.sha256(b'story-studio-s3-2-lab-result-v1'+bytes.fromhex('5c783030')+raw).hexdigest()
        result=p.decode_lab(response)
        self.assertEqual(result['mock_summary']['value_sha256'],digest);self.assertNotEqual(digest,wrong)
        with self.assertRaises(s1.ProtocolError):s1.validate_wire(result,'Receipt')
        for token in (b'"mac"',b'"journal"',b'"anchor"',b'"key_id"',b'"core"',b'"head"',raw):self.assertNotIn(token,response)

    def test_malformed_input_never_calls_model(self):
        d=self.make();frame=d.execute_frame('A','INIT_EMPTY');events=self.events(d)
        for raw in (frame[:-1],frame+b'x',b'SSLB'+(p.MAX_EXECUTE+1).to_bytes(4,'big')):
            with self.assertRaises(p.LabError):d.dispatch(raw,Caller('A'))
        self.assertEqual(events,self.events(d));self.assertEqual(d.admissions,0);self.assertEqual(d.model_calls,0)

    def test_verified_abort_and_bad_terminal_proof(self):
        d=self.make();frame=d.execute_frame('A','INIT_EMPTY')
        original=m.TransactionModel._authorize
        n=[0]
        def revoke(engine,command):
            n[0]+=1
            if n[0]==2:raise m.ModelError('PERMISSION_DENIED','$','Synthetic policy boundary')
            return original(engine,command)
        with patch.object(m.TransactionModel,'_authorize',revoke):
            result=p.decode_lab(d.dispatch(frame,Caller('A')))
        self.assertEqual(result['outcome'],'MOCK_ABORTED')
        self.assertEqual(result['mock_summary']['status'],'ABORTED_PRECOMMIT')
        self.assertEqual(d.admissions,1)
        d=self.make();frame=d.execute_frame('A','INIT_EMPTY')
        with patch.object(m.TransactionModel,'inspect',side_effect=m.ModelError('ANCHOR_MISMATCH','$','Synthetic corruption')):
            response=d.dispatch(frame,Caller('A'))
        result=p.decode_lab(response)
        self.assertEqual(result['outcome'],'MOCK_PENDING');self.assertIsNone(result['mock_summary'])
        self.assertEqual(d.dispatch(frame,Caller('A')),response)
        self.assertEqual(d.model_calls,1);self.assertEqual(d.admissions,1)

    def test_runtime_no_external_effects(self):
        import builtins
        import os
        import socket
        import subprocess
        d=self.make();frame=d.execute_frame('A','INIT_EMPTY')
        deny=AssertionError('Portable runtime attempted external effect')
        with patch.object(builtins,'open',side_effect=deny), patch.object(os,'open',side_effect=deny), patch.object(os,'replace',side_effect=deny), patch.object(socket,'socket',side_effect=deny), patch.object(subprocess,'Popen',side_effect=deny):
            result=p.decode_lab(d.dispatch(frame,Caller('A')))
        self.assertEqual(result['outcome'],'MOCK_FINALIZED')

    def test_preflight_frozen_failure_never_admits(self):
        d=self.make();frame=d.execute_frame('A','INIT_EMPTY');events=self.events(d)
        with patch.object(m.TransactionModel,'_authorize',side_effect=m.ModelError('SESSION_INVALIDATED','$','Synthetic invalid frozen fixture')):
            result=p.decode_lab(d.dispatch(frame,Caller('A')))
        self.assertEqual(result['outcome'],'DENIED')
        self.assertEqual(d.admissions,0);self.assertEqual(self.events(d),events)
