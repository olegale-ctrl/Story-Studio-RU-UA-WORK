"""Fake-only transaction/ownership/clock/ledger harness and behavioral oracles.

No native database, process lock, media or filesystem is used by these fakes.
They preserve Python values across controller objects, not across real crashes.
"""
from copy import deepcopy
import pytest
from experimental_mvp.offline_execution.contracts import (
    Record, ContractError, require, seal, resolve, validate_record, TERMINAL)
from experimental_mvp.offline_execution.controller import Controller, identifier
from experimental_mvp.offline_execution.simulator import MetadataSimulator
from experimental_mvp.offline_execution import policy
from test_offline_generation_job_contracts import record, vector_records


def uid(n):return '00000000-0000-0000-0000-'+format(n,'012x')


def expect_error(out,code):
    assert type(out) is dict and out['error']['code']==code,out
    return out


class FakeClock:
    def __init__(self):self.epoch=uid(9);self.tick=1;self.qualified=True;self.high=1
    def instant(self):
        if self.tick<self.high:self.qualified=False
        self.high=max(self.high,self.tick)
        return self.epoch,self.tick,self.qualified


class FakeOwnerLock:
    def __init__(self,namespace,clock):
        self.namespace=namespace;self.clock=clock;self.token=None;self.incarnation=0;self.dead=set()
    def acquire(self,controller_id,old_dead=False):
        require(self.token is None or old_dead,'STALE_CONTROLLER_FENCE')
        self.incarnation+=1
        self.token=dict(store_id=self.namespace.value['store_id'],controller_id=controller_id,incarnation=self.incarnation,clock_epoch_id=self.clock.epoch)
        return deepcopy(self.token)
    def current(self):return deepcopy(self.token)
    def worker_dead(self,worker_id):return worker_id in self.dead


class FakeStore:
    """Finite atomic-swap model, including explicit fault injection and evidence.

    commit's validation + single swap is the simulated atomic boundary. A hook
    injects an interleaving BEFORE it, never a fake claim of native thread safety.
    registry is retained by the harness even when no commit marker exists.
    """
    def __init__(self,namespace,objects,owner,clock):
        self.owner=owner;self.clock=clock;self.registry={};self.fault=None;self.hook=None;self.commits=0
        self.state=dict(namespace_ref=namespace.ref,objects=dict(objects),jobs={},receipts={},slots={},outboxes={},mutations={},pending=set(),sequence=0,generation=0,available=True,integrity=True)
    def snapshot(self):return deepcopy(self.state)
    def hold(self,plan):
        mid=plan.mutation.value['mutation_id']
        self.registry.setdefault(mid,plan)
        self.state['mutations'].setdefault(mid,{'intent':plan.mutation.ref,'write_set':None})
        self.state['pending'].add(mid)
    def commit(self,plan):
        if self.hook:
            hook,self.hook=self.hook,None;hook()
        s=self.state;mid=plan.mutation.value['mutation_id'];m=plan.mutation.value
        require(s['available'],'STORE_UNAVAILABLE');require(s['integrity'],'STORE_CORRUPT');require(not s['pending'],'UNKNOWN_COMMIT_OUTCOME')
        prior=s['mutations'].get(mid)
        require(prior is None or prior['intent']==plan.mutation.ref,'OPERATION_ID_CONFLICT')
        if prior and prior['write_set']:
            require(prior['write_set']==plan.write_set.ref,'OPERATION_ID_CONFLICT');return 'COMMITTED'
        policy.controller_fence(plan.controller,self.owner,self.state['namespace_ref'] and self.owner.namespace.value['store_id'],self.clock.epoch)
        members=[r for r in plan.records if r.ref in plan.write_set.value['members']]
        job=next(r for r in members if r.value['kind']=='PURE.JobRecord');j=job.value
        objects={r.digest:r for r in plan.records};validate_record(plan.write_set,objects)
        key=resolve(j['key_ref'],objects);projection=(key['store_id'],key['project_id'],key['purpose_id'])
        if m['mutation_kind']=='ADMIT':
            require(projection not in s['slots'],'ACTIVE_INTENT_CONFLICT')
        else:
            old=s['objects'][s['jobs'][j['job_id']]['digest']].value
            if plan.worker is not None:policy.worker_fence(plan.worker,old,plan.controller,self.clock.instant()[1])
            require(old['revision']==m['expected_revision'],'CAS_CONFLICT')
        require(plan.snapshot_generation==s['generation'],'CAS_CONFLICT')
        self.registry[mid]=plan
        s['mutations'][mid]={'intent':plan.mutation.ref,'write_set':None}
        fault,self.fault=self.fault,None
        if fault=='before':return 'NOT_COMMITTED'
        if fault=='during':self.hold(plan);return 'UNKNOWN_COMMIT_OUTCOME'
        if fault=='partial':
            s['objects'][members[0].digest]=members[0];s['integrity']=False;self.hold(plan);return 'UNKNOWN_COMMIT_OUTCOME'
        new=deepcopy(s)
        new['objects'].update(objects);new['jobs'][j['job_id']]=job.ref
        for r in members:
            v=r.value;k=v['kind']
            if k=='PURE.AcceptanceReceipt':new['receipts'][v['key_ref']['digest']]=r.ref
            elif k=='PURE.OutboxEnvelope':new['outboxes'][v['outbox_id']]=r.ref
            elif k=='PURE.ActiveSlot':
                if v['status']=='HELD':new['slots'][projection]=r.ref
                else:
                    require(new['slots'].get(projection)==old['active_slot_ref'],'STORE_CORRUPT')
                    del new['slots'][projection]
        new['mutations'][mid]['write_set']=plan.write_set.ref
        new['sequence']=plan.write_set.value['store_sequence'];new['generation']+=1
        self.state=new;self.commits+=1
        if fault=='after':raise RuntimeError('scripted lost commit ACK')
        return 'COMMITTED'
    def inspect_mutation(self,mid):
        s=self.state;require(s['available'],'STORE_UNAVAILABLE');require(s['integrity'],'STORE_CORRUPT')
        require(mid in self.registry,'STORE_CORRUPT');plan=self.registry[mid]
        objects=dict(s['objects']);objects[plan.mutation.digest]=plan.mutation
        marker=s['mutations'].get(mid,{}).get('write_set')
        if marker:
            require(marker==plan.write_set.ref and marker['digest'] in objects,'STORE_CORRUPT')
            for ref in plan.write_set.value['members']:resolve(ref,objects)
            validate_record(objects[marker['digest']],objects)
            proof=seal('CommitResolutionProof',namespace_ref=s['namespace_ref'],mutation_ref=plan.mutation.ref,outcome='COMMITTED',write_set_ref=marker,absence_ref=None,snapshot_generation=s['generation'],qualification='FAKE_STORE_READ_ONLY_EVIDENCE')
        else:
            require(not any(ref['digest'] in objects for ref in plan.write_set.value['members']),'STORE_CORRUPT')
            absence=seal('MutationAbsenceProof',namespace_ref=s['namespace_ref'],mutation_ref=plan.mutation.ref,snapshot_generation=s['generation'],lookup_complete=True,marker_present=False,members_for_mutation_present=False,qualification='FAKE_STORE_READ_ONLY_EVIDENCE')
            objects[absence.digest]=absence
            proof=seal('CommitResolutionProof',namespace_ref=s['namespace_ref'],mutation_ref=plan.mutation.ref,outcome='NOT_COMMITTED',write_set_ref=None,absence_ref=absence.ref,snapshot_generation=s['generation'],qualification='FAKE_STORE_READ_ONLY_EVIDENCE')
        objects[proof.digest]=proof;return proof,objects
    def acknowledge_resolution(self,mid,proof):
        current,_=self.inspect_mutation(mid);require(current.ref==proof.ref,'STORE_CORRUPT')
        self.state['pending'].discard(mid)


class ScriptedLedger:
    """Scripted acceptance metadata + read-once reservations; no media producer."""
    def __init__(self,namespace,objects):
        self.namespace=namespace;self.objects=dict(objects);self.accepted={};self.dispatched=set();self.used_reads=set();self.calls=0;self.read_calls=0;self.script_events=0;self.lose_ack=False;self.read_unavailable=False
    def attests(self,receipt,payload):
        return receipt.digest in self.objects and self.objects[receipt.digest].encoded==receipt.encoded
    def _step(self):
        require(self.script_events<64,'RESOURCE_LIMIT');self.script_events+=1
    def submit(self,payload,tick):
        self._step();token=payload.value['effect_token']
        require(token not in self.dispatched,'ATTEMPT_LIMIT')
        self.dispatched.add(token);self.calls+=1;p=payload.value
        receipt=seal('ProviderAcceptanceReceipt',provider_receipt_id=identifier(token+'accept'),namespace_ref=self.namespace.ref,ledger_id=self.namespace.value['ledger_id'],ledger_sequence=self.calls,provider_job_id=identifier(token+'remote'),generation_operation_id=p['generation_operation_id'],attempt_id=p['attempt_id'],effect_token=token,payload_ref=payload.ref,accepted_tick=tick,provider_cursor=1,billed_minor=0,producer_qualification='UNQUALIFIED_FAKE_ONLY')
        self.accepted[token]=receipt;self.objects[payload.digest]=payload;self.objects[receipt.digest]=receipt
        if self.lose_ack:self.lose_ack=False;return None
        return receipt
    def _read(self,reservation):
        require(reservation['digest'] not in self.used_reads,'READ_LIMIT_EXCEEDED')
        self._step();self.used_reads.add(reservation['digest']);self.read_calls+=1
        require(not self.read_unavailable,'STORE_UNAVAILABLE')
    def lookup(self,payload,tick,reservation):
        self._read(reservation)
        receipt=self.accepted.get(payload.value['effect_token'])
        require(receipt is not None,'STORE_UNAVAILABLE')
        return receipt
    def poll(self,payload,cursor,tick,reservation):
        self._read(reservation);p=payload.value
        a=self.accepted.get(p['effect_token']);require(a is not None,'STORE_UNAVAILABLE')
        cp=record('CapabilityProfile');fixture=record('FixtureDescriptor')
        receipt=seal('ProviderResultReceipt',result_id=identifier(p['effect_token']+'result'),acceptance_ref=a.ref,generation_operation_id=p['generation_operation_id'],attempt_id=p['attempt_id'],effect_token=p['effect_token'],provider_job_id=a.value['provider_job_id'],resolved_profile_ref=cp.ref,fixture_ref=fixture.ref,provider_cursor=2,ready_tick=tick,producer_qualification='UNQUALIFIED_FAKE_ONLY')
        self.objects[receipt.digest]=receipt;return receipt


class Lab:
    def __init__(self):
        all_objects=vector_records()
        self.namespace=record('NamespaceBinding')
        # Immutable declarations only; no seeded jobs, effects or previous commits.
        allowed={'FixtureDescriptor','FixtureRegistry','InputManifest','CapabilityProfile','NamespaceBinding','RequestIntent','BatchManifest','BatchPermit','AdmissionKey','AdmissionCommand'}
        self.objects={h:r for h,r in all_objects.items() if r.value['kind'].split('.')[1] in allowed}
        self.command=record('AdmissionCommand');self.clock=FakeClock();self.owner=FakeOwnerLock(self.namespace,self.clock)
        self.token=self.owner.acquire(uid(100));self.store=FakeStore(self.namespace,self.objects,self.owner,self.clock)
        self.ledger=ScriptedLedger(self.namespace,self.objects);self.simulator=MetadataSimulator(self.ledger)
        self.authority=policy.Authority(frozenset([record('BatchPermit').digest]));self.serial=1000;self.restart()
    def mid(self):self.serial+=1;return uid(self.serial)
    def restart(self,replace_owner=False):
        if replace_owner:
            self.owner.dead.add(uid(200));self.token=self.owner.acquire(uid(101),old_dead=True)
        self.c=Controller(self.namespace,self.objects,self.store,self.clock,self.owner,self.token,self.authority,self.simulator)
        return self.c
    def add(self,r):self.objects[r.digest]=r;self.c.objects[r.digest]=r;return r
    def variant(self,n=1,project=False):
        req=record('RequestIntent').value;req={k:v for k,v in req.items() if k not in ('kind','version','scope')}
        req['request']['prompt_reference']='prompt-'+str(n)
        if project:req['identity_context']['purpose_id']=uid(300+n)
        rr=self.add(seal('RequestIntent',**req));ctx=rr.value['identity_context']
        manifest=self.add(seal('BatchManifest',batch_id=uid(400+n),batch_revision=1,entries=[dict(project_id=ctx['project_id'],purpose_id=ctx['purpose_id'],request_ref=rr.ref)],policy=record('BatchManifest').value['policy']))
        permitv=record('BatchPermit').value;permitv={k:v for k,v in permitv.items() if k not in ('kind','version','scope')};permitv.update(permit_id=uid(500+n),manifest_ref=manifest.ref)
        permit=self.add(seal('BatchPermit',**permitv));self.authority=policy.Authority(self.authority.permits|{permit.digest},self.authority.revoked);self.c.authority=self.authority
        key=self.add(seal('AdmissionKey',store_id=self.namespace.value['store_id'],namespace_ref=self.namespace.ref,project_id=ctx['project_id'],purpose_id=ctx['purpose_id'],request_ref=rr.ref,batch_id=manifest.value['batch_id'],batch_revision=1,batch_manifest_ref=manifest.ref))
        return self.add(seal('AdmissionCommand',namespace_ref=self.namespace.ref,key_ref=key.ref,request_ref=rr.ref,permit_ref=permit.ref))
    def job(self):
        return self.store.state['objects'][self.store.state['jobs'][self.job_id]['digest']]
    def admit(self):
        out=self.c.admit(self.command,self.mid());assert out['disposition']=='ACCEPTED',out
        self.job_id=self.store.state['objects'][out['job_ref']['digest']].value['job_id'];return out
    def queued(self):
        self.admit()
        for target in ('AWAITING_APPROVAL','APPROVED','QUEUED'):
            out=self.c.advance(self.job_id,self.job().value['revision'],self.mid(),target);assert out['disposition']=='APPLIED',out
        return self.job()
    def claimed(self):
        self.queued();out=self.c.claim(self.job_id,self.job().value['revision'],self.mid(),uid(200),100);assert out['disposition']=='APPLIED',out
        self.worker=self.c.worker_token(self.job_id);return self.job()
    def submitting(self):
        self.claimed();out=self.c.prepare_submit(self.job_id,self.job().value['revision'],self.mid(),self.worker);assert out['disposition']=='APPLIED',out
        return self.job()
    def running(self):
        self.submitting();a=self.c.dispatch(self.job_id,self.job().value['revision'],self.worker);assert isinstance(a,Record),a
        out=self.c.apply_proof(self.job_id,self.job().value['revision'],self.mid(),self.worker,a);assert out['disposition']=='APPLIED',out
        return a
    def result(self):
        a=self.running();out=self.c.reserve_read(self.job_id,self.job().value['revision'],self.mid(),self.worker,'POLL',uid(600));assert out['disposition']=='APPLIED',out
        result=self.c.read_reserved(self.job_id,self.job().value['revision'],self.worker);assert isinstance(result,Record),result
        out=self.c.apply_proof(self.job_id,self.job().value['revision'],self.mid(),self.worker,result,tuple(self.ledger.objects.values()));assert out['disposition']=='APPLIED',out
        return result


def test_A01_A02_A07_A08_A09_admission_semantics():
    l=Lab();accepted=l.admit();before=l.store.snapshot();n=l.store.commits
    assert l.c.admit(l.command,l.mid())['receipt_ref']==accepted['receipt_ref'];assert l.store.commits==n
    variant=l.variant();expect_error(l.c.admit(variant,l.mid()),'ACTIVE_INTENT_CONFLICT')
    c=variant.value;c['key_ref']=l.command.value['key_ref'];c.pop('kind');c.pop('version');c.pop('scope')
    expect_error(l.c.admit(l.add(seal('AdmissionCommand',**c)),l.mid()),'IDEMPOTENCY_CONFLICT')
    c=variant.value;c['permit_ref']=l.command.value['permit_ref'];c.pop('kind');c.pop('version');c.pop('scope')
    expect_error(l.c.admit(l.add(seal('AdmissionCommand',**c)),l.mid()),'AUTHORIZATION_SCOPE_MISMATCH')
    l.clock.tick=99;l.authority=policy.Authority(l.authority.permits,frozenset([record('BatchPermit').digest]));l.c.authority=l.authority
    assert l.c.admit(l.command,l.mid())['disposition']=='REUSED'
    assert l.store.commits==n


def test_A03_A05_terminal_release_and_old_replay_new_slot():
    l=Lab();old=l.admit();job=l.job();out=l.c.cancel(l.job_id,job.value['revision'],l.mid());assert out['disposition']=='APPLIED',out
    assert not l.store.state['slots'];cmd=l.variant();new=l.c.admit(cmd,l.mid());assert new['disposition']=='ACCEPTED',new
    snapshot=l.store.snapshot();again=l.c.admit(l.command,l.mid());assert again['receipt_ref']==old['receipt_ref'];assert l.store.snapshot()==snapshot


def test_A04_E15_result_available_holds_slot_and_is_not_complete():
    l=Lab();l.result();assert l.job().value['state']=='RESULT_AVAILABLE' and l.store.state['slots']
    expect_error(l.c.admit(l.variant(),l.mid()),'ACTIVE_INTENT_CONFLICT')
    expect_error(l.c.advance(l.job_id,l.job().value['revision'],l.mid(),'COMPLETED'),'ILLEGAL_TRANSITION')


def test_A10_interleaved_candidates_atomic_single_slot():
    l=Lab();other=l.variant();winner=[]
    l.store.hook=lambda:winner.append(l.c.admit(other,l.mid()))
    out=l.c.admit(l.command,l.mid());expect_error(out,'ACTIVE_INTENT_CONFLICT')
    assert winner[0]['disposition']=='ACCEPTED';assert len(l.store.state['jobs'])==len(l.store.state['receipts'])==len(l.store.state['slots'])==1


def test_E13_mutation_identity_conflict():
    l=Lab();mid=l.mid();assert l.c.admit(l.command,mid)['disposition']=='ACCEPTED'
    expect_error(l.c.admit(l.variant(project=True),mid),'OPERATION_ID_CONFLICT')


def test_A09_expired_historical_replay_cannot_refresh_permission():
    l=Lab();l.submitting();before=l.store.snapshot();l.clock.tick=100
    assert l.c.admit(l.command,l.mid())['disposition']=='REUSED'
    expect_error(l.c.dispatch(l.job_id,l.job().value['revision'],l.worker),'AUTHORIZATION_EXPIRED')
    assert l.store.snapshot()==before and l.ledger.calls==0
