"""Bounded pure GenerationJob orchestration through injected fake-only ports.

All public mutations return the closed APIOutcome. Only the store port may model
atomic visibility. No module here supplies a real store/lock/clock/worker.
"""
from dataclasses import dataclass
import hashlib
from .contracts import (Record, ContractError, MAX_INT, TERMINAL, require, seal,
                        resolve, validate_record, validate_shape, response_error)
from . import policy
from .simulator import verify_receipt


def identifier(seed):
    """Deterministic internal IDs; no entropy, clock or UUID system calls."""
    h=hashlib.sha256(seed.encode('utf-8')).hexdigest()[:32]
    return h[:8]+'-'+h[8:12]+'-'+h[12:16]+'-'+h[16:20]+'-'+h[20:]


def outcome(disposition, job=None, receipt=None, mutation=None, error=None):
    v=dict(kind='PURE.APIOutcome',version=1,scope='PURE_FAKE_ONLY',
           disposition=disposition,mutation_outcome=mutation,
           job_ref=job.ref if job else None,receipt_ref=receipt.ref if receipt else None,error={k:v for k,v in error.items() if k not in ('kind','version','scope')} if error else None)
    return validate_shape(v)


@dataclass(frozen=True)
class Plan:
    mutation: Record
    write_set: Record
    records: tuple
    snapshot_generation: int
    controller: dict
    worker: object
    tick: int


class Controller:
    def __init__(self, namespace, objects, store, clock, ownership, token, authority, simulator):
        validate_record(namespace,objects)
        self.namespace=namespace; self.objects=dict(objects); self.store=store
        self.clock=clock; self.ownership=ownership; self.token=dict(token)
        self.authority=authority; self.simulator=simulator
        self._last_tick=0
        # A failed diagnostic/hold port must not erase an outcome already unknown.
        # This is a controller-local latch, not a durable store implementation.
        self._uncertain={}
        self._namespace_pending=set()

    def _snapshot(self):
        try:
            snap=self.store.snapshot()
        except ContractError:
            raise
        except Exception as exc:
            raise ContractError('STORE_UNAVAILABLE') from exc
        require(type(snap) is dict,'STORE_CORRUPT')
        required={'available','integrity','namespace_ref','pending','objects','jobs',
                  'receipts','outboxes','mutations','slots','sequence','generation'}
        require(required <= snap.keys(),'STORE_CORRUPT')
        require(type(snap['available']) is bool and type(snap['integrity']) is bool,'STORE_CORRUPT')
        require(type(snap['pending']) in (set,frozenset),'STORE_CORRUPT')
        require(all(type(snap[n]) is dict for n in ('objects','jobs','receipts','outboxes','mutations','slots')),'STORE_CORRUPT')
        # An unqualified read may add a conservative hold hint, never clear one.
        self._namespace_pending.update(snap['pending'])
        require(snap['available'],'STORE_UNAVAILABLE')
        require(snap['integrity'],'STORE_CORRUPT')
        require(snap['namespace_ref']==self.namespace.ref,'NAMESPACE_MISMATCH')
        try:
            objects=snap['objects'];held={};keys=set()
            for jid,ref in snap['jobs'].items():
                job=objects[ref['digest']];validate_record(job,objects);j=job.value
                require(job.ref==ref and j['kind']=='PURE.JobRecord' and j['job_id']==jid and j['namespace_ref']==self.namespace.ref,'STORE_CORRUPT')
                slot=resolve(j['active_slot_ref'],objects);keys.add(j['key_ref']['digest'])
                if slot['status']=='HELD':
                    projection=tuple(slot[n] for n in ('store_id','project_id','purpose_id'))
                    require(projection not in held,'STORE_CORRUPT');held[projection]=j['active_slot_ref']
            require(held==snap['slots'] and keys==set(snap['receipts']),'STORE_CORRUPT')
            for key,ref in snap['receipts'].items():
                rec=objects[ref['digest']];validate_record(rec,objects);v=rec.value
                require(rec.ref==ref and v['kind']=='PURE.AcceptanceReceipt' and v['key_ref']['digest']==key and v['job_id'] in snap['jobs'],'STORE_CORRUPT')
            for oid,ref in snap['outboxes'].items():
                rec=objects[ref['digest']];validate_record(rec,objects);v=rec.value
                require(rec.ref==ref and v['kind']=='PURE.OutboxEnvelope' and v['outbox_id']==oid,'STORE_CORRUPT')
                payload=resolve(v['payload_ref'],objects)
                require(payload['job_id'] in snap['jobs'],'STORE_CORRUPT')
                job=resolve(snap['jobs'][payload['job_id']],objects)
                require(all(payload[n]==job[n] for n in ('job_id','namespace_ref','request_ref','key_ref','generation_operation_id','attempt_id','effect_token')),'STORE_CORRUPT')
        except Exception as exc:
            raise ContractError('STORE_CORRUPT') from exc
        self._namespace_pending=set(snap['pending'])
        return snap

    def _view(self, allow_pending=False):
        require(self.authority.can_read,'READ_SCOPE_DENIED')
        snap=self._snapshot()
        require(allow_pending or not (snap['pending'] or self._uncertain),'UNKNOWN_COMMIT_OUTCOME')
        return snap

    def _objects(self, snap, extra=()):
        objects=dict(self.objects)
        for rec in tuple(snap['objects'].values())+tuple(extra):
            require(type(rec) is Record,'FORMAT')
            require(rec.digest not in objects or objects[rec.digest].encoded==rec.encoded,'STORE_CORRUPT')
            objects[rec.digest]=rec
        return objects

    def _now(self):
        now=policy.instant(self.clock,self.token['clock_epoch_id'],self._last_tick)
        self._last_tick=now
        return now

    def _owner(self):
        policy.controller_fence(self.token,self.ownership,self.namespace.value['store_id'],self.token['clock_epoch_id'])

    def _job(self,snap,job_id):
        require(job_id in snap['jobs'],'NOT_FOUND')
        return snap['objects'][snap['jobs'][job_id]['digest']]

    def _guard(self,job,revision,worker=None,require_worker=False):
        now=self._now(); self._owner()
        if require_worker:
            policy.worker_fence(worker,job.value,self.token,now)
        require(job.value['revision']==revision,'CAS_CONFLICT')
        return now

    def _permit(self,job,objects,now):
        j=job.value;key=resolve(j['key_ref'],objects)
        policy.authorize(j['initial_permit_ref'],key['batch_manifest_ref'],self.namespace.ref,self.authority,objects,now)

    def _effect(self,job_id=None,command=None,mutation_id=None):
        """Classify only a fully bound target; unrelated evidence is never used."""
        try:
            require(self.authority.can_read,'READ_SCOPE_DENIED')
            snap=self._snapshot()
            if snap['pending'] or self._uncertain:
                return 'UNKNOWN'
            objects=self._objects(snap)
            if command is not None:
                require(type(command) is Record and command.value['kind']=='PURE.AdmissionCommand')
                c=command.value
                require(c['namespace_ref']==self.namespace.ref,'NAMESPACE_MISMATCH')
                key=resolve(c['key_ref'],objects)
                require(key['request_ref']==c['request_ref'],'IDEMPOTENCY_CONFLICT')
                validate_record(command,dict(objects,**{command.digest:command}))
                old=snap['receipts'].get(c['key_ref']['digest'])
                if old is None:
                    return 'NONE'  # Complete history has never admitted this key.
                receipt=resolve(old,objects)
                require(receipt['request_ref']==c['request_ref'],'STORE_CORRUPT')
                job_id=receipt['job_id']
            if job_id is None and mutation_id is not None:
                entry=snap['mutations'].get(mutation_id)
                if entry is None:
                    return 'UNKNOWN'  # No proved target, never borrow another job.
                intent=resolve(entry['intent'],objects)
                require(intent['mutation_id']==mutation_id,'STORE_CORRUPT')
                job_id=intent['job_id']
                if job_id is None:
                    ws_ref=entry.get('write_set')
                    if ws_ref is None:
                        return 'UNKNOWN'
                    ws=resolve(ws_ref,objects)
                    require(ws['mutation_ref']==entry['intent'],'STORE_CORRUPT')
                    job_id=ws['job_id']
            if job_id is None:
                return 'UNKNOWN'
            ref=snap['jobs'].get(job_id)
            if ref is None:
                return 'UNKNOWN'  # Absence of an unbound/invalid target is not proof.
            job=objects[ref['digest']];validate_record(job,objects);j=job.value
            require(j['kind']=='PURE.JobRecord' and j['job_id']==job_id and j['namespace_ref']==self.namespace.ref,'STORE_CORRUPT')
            boxes=[]
            for box_ref in snap['outboxes'].values():
                box=objects[box_ref['digest']]
                payload=objects[box.value['payload_ref']['digest']]
                if payload.value['job_id']==job_id:
                    validate_record(box,objects)
                    boxes.append(payload)
            if j['generation_operation_id'] is None:
                return 'UNKNOWN' if boxes else 'NONE'
            if len(boxes)!=1:
                return 'UNKNOWN'
            payload=boxes[0];pv=payload.value
            bindings=('job_id','namespace_ref','generation_operation_id','attempt_id',
                      'effect_token','key_ref','request_ref')
            require(all(pv[n]==j[n] for n in bindings) and pv['permit_ref']==j['initial_permit_ref'],'RESULT_BINDING_MISMATCH')
            for rec in objects.values():
                if rec.value['kind']!='PURE.ProviderAcceptanceReceipt':
                    continue
                if rec.value['payload_ref']!=payload.ref:
                    continue
                verify_receipt(rec,payload,objects)
                if self.simulator.attests(rec,payload):
                    return 'KNOWN'
            return 'UNKNOWN'  # Intent/outbox is not acceptance/nonacceptance proof.
        except Exception:
            # Diagnostic classification must never escape or invent certainty.
            return 'UNKNOWN'

    def _failure(self,code,operation,mutation=None,*,job_id=None,command=None,mutation_id=None):
        effect=self._effect(job_id,command,mutation_id)
        hold=code in ('UNKNOWN_COMMIT_OUTCOME','STORE_UNAVAILABLE','STORE_CORRUPT','CLOCK_UNQUALIFIED','READ_LIMIT_EXCEEDED')
        if mutation=='UNKNOWN_COMMIT_OUTCOME':
            hold=True
        return outcome('HOLD' if hold else 'REJECTED',mutation=mutation,
                       error=response_error(code,operation,effect,'ZERO'))

    def _pending(self,unknown_on_unreadable=False):
        pending=bool(self._uncertain or self._namespace_pending)
        try:
            pending=pending or bool(self._snapshot()['pending'])
        except Exception:
            pending=pending or unknown_on_unreadable  # Never clear known uncertainty.
        return pending

    def _call(self,operation,fn,*,job_id=None,command=None,mutation_id=None):
        try:
            return fn()
        except ContractError as exc:
            return self._failure(exc.code,operation,
                'UNKNOWN_COMMIT_OUTCOME' if self._pending(operation=='RESOLVE_COMMIT') else None,
                job_id=job_id,command=command,mutation_id=mutation_id)

    def _hold(self,plan,code='UNKNOWN_COMMIT_OUTCOME'):
        mid=plan.mutation.value['mutation_id']
        self._uncertain[mid]=plan
        try:
            self.store.hold(plan)
        except Exception:
            pass  # Keep the local fail-closed latch even if the port is down.
        return self._failure(code,'RESOLVE_COMMIT','UNKNOWN_COMMIT_OUTCOME',
                             job_id=plan.write_set.value['job_id'],mutation_id=mid)

    def _proof(self,plan):
        self._view(allow_pending=True)
        proof,objects=self.store.inspect_mutation(plan.mutation.value['mutation_id'])
        require(proof is not None,'UNKNOWN_COMMIT_OUTCOME')
        validate_record(proof,objects)
        value=proof.value
        require(value['namespace_ref']==self.namespace.ref and value['mutation_ref']==plan.mutation.ref,'STORE_CORRUPT')
        if value['outcome']=='COMMITTED':
            require(value['write_set_ref']==plan.write_set.ref,'STORE_CORRUPT')
        return proof,objects

    def _acknowledge(self,mid,proof):
        self.store.acknowledge_resolution(mid,proof)
        self._uncertain.pop(mid,None)
        self._namespace_pending.discard(mid)

    def _commit(self,snap,mutation,members,objects,slot_action,worker=None):
        prior=snap['mutations'].get(mutation.value['mutation_id'])
        require(prior is None or prior['intent']==mutation.ref,'OPERATION_ID_CONFLICT')
        events=[r for r in members if r.value['kind']=='PURE.StoreEvent']
        require(len(events)==1,'STORE_CORRUPT');event=events[0].value
        seq=policy.increment(snap['sequence'])
        ws=seal('AtomicWriteSet',mutation_ref=mutation.ref,job_id=event['job_id'],
                base_revision=event['revision_from'],result_revision=event['revision_to'],
                members=sorted([r.ref for r in members],key=lambda x:(x['kind'],x['digest'])),
                active_slot_action=slot_action,store_sequence=seq)
        records=dict(objects)
        for r in (mutation,*members,ws): records[r.digest]=r
        validate_record(ws,records)
        require(sum(r.value['kind']=='PURE.StoreEvent' for r in snap['objects'].values())<128,'RESOURCE_LIMIT')
        require(sum(r.value['kind']=='PURE.OutboxEnvelope' for r in snap['objects'].values())+sum(r.value['kind']=='PURE.OutboxEnvelope' for r in members)<=32,'RESOURCE_LIMIT')
        plan=Plan(mutation,ws,tuple(records.values()),snap['generation'],dict(self.token),worker,self._now())
        # Retain this exact intent until complete qualified proof, not just an ACK.
        mid=mutation.value['mutation_id']
        failure_context=dict(job_id=event['job_id'],mutation_id=mid)
        if mutation.value['mutation_kind']=='ADMIT':
            failure_context['command']=objects[mutation.value['input_ref']['digest']]
        self._uncertain[mid]=plan
        try:
            result=self.store.commit(plan)
        except ContractError as exc:
            # A typed exception is not rollback evidence. Only a complete
            # same-operation absence proof permits the original no-write error.
            try:
                proof,_=self._proof(plan)
                if proof.value['outcome']=='NOT_COMMITTED':
                    self._acknowledge(mid,proof)
                    return self._failure(exc.code,'RESOLVE_COMMIT','NOT_COMMITTED',
                                         **failure_context)
            except Exception:
                pass
            return self._hold(plan)
        except Exception:
            return self._hold(plan)
        if result=='UNKNOWN_COMMIT_OUTCOME':
            return self._hold(plan)
        if result not in ('COMMITTED','NOT_COMMITTED'):
            return self._hold(plan,'STORE_CORRUPT')
        try:
            proof,_=self._proof(plan)
            require(proof.value['outcome']==result,'STORE_CORRUPT')
            self._acknowledge(mid,proof)
        except ContractError as exc:
            code=exc.code if exc.code in ('STORE_UNAVAILABLE','STORE_CORRUPT','UNKNOWN_COMMIT_OUTCOME') else 'STORE_CORRUPT'
            return self._hold(plan,code)
        except Exception:
            return self._hold(plan,'STORE_UNAVAILABLE')
        if result=='NOT_COMMITTED':
            return self._failure('MUTATION_NOT_COMMITTED','RESOLVE_COMMIT',result,
                                 **failure_context)
        job=next(r for r in members if r.value['kind']=='PURE.JobRecord')
        receipt=next((r for r in members if r.value['kind']=='PURE.AcceptanceReceipt'),None)
        return outcome('ACCEPTED' if receipt else 'APPLIED',job,receipt,'COMMITTED')

    def admit(self,command,mutation_id):
        def run():
            validate_shape(command.value)
            require(command.value['kind']=='PURE.AdmissionCommand','FORMAT')
            c=command.value
            require(c['namespace_ref']==self.namespace.ref,'NAMESPACE_MISMATCH')
            snap=self._view();objects=self._objects(snap,(command,))
            cp=resolve(self.namespace.value['profile_ref'],objects);policy.profile(cp)
            key=resolve(c['key_ref'],objects);request=resolve(c['request_ref'],objects)
            expected=seal('StoreMutationIntent',mutation_id=mutation_id,mutation_kind='ADMIT',job_id=None,
                          expected_revision=0,target_state='DRAFT',input_ref=command.ref,cancel_requested=False)
            prior=snap['mutations'].get(mutation_id)
            require(prior is None or prior['intent']==expected.ref,'OPERATION_ID_CONFLICT')
            # Explicit supplied-key/content mismatch has a distinct public outcome.
            require(key['request_ref']==c['request_ref'],'IDEMPOTENCY_CONFLICT')
            validate_record(command,objects)
            require(request['request']['capability_profile_hash']==self.namespace.value['profile_ref']['digest'],'PROFILE_UNQUALIFIED')
            require(key['namespace_ref']==self.namespace.ref,'NAMESPACE_MISMATCH')
            old=snap['receipts'].get(c['key_ref']['digest'])
            if old:
                receipt=objects[old['digest']];rv=receipt.value
                require(rv['request_ref']==c['request_ref'] and rv['initial_permit_ref']==c['permit_ref'],'IDEMPOTENCY_CONFLICT')
                return outcome('REUSED',self._job(snap,rv['job_id']),receipt)
            now=self._now()
            policy.authorize(c['permit_ref'],key['batch_manifest_ref'],self.namespace.ref,self.authority,objects,now)
            projection=(key['store_id'],key['project_id'],key['purpose_id'])
            require(projection not in snap['slots'],'ACTIVE_INTENT_CONFLICT')
            self._owner();policy.capacity(self.authority)
            require(len(snap['jobs'])<16,'RESOURCE_LIMIT')
            job_id=identifier(mutation_id+'job');ev=seal('StoreEvent',event_id=identifier(mutation_id+'event'),job_id=job_id,
                mutation_id=mutation_id,sequence=1,previous_event_ref=None,state_from=None,state_to='DRAFT',
                revision_from=0,revision_to=1,event_type='ADMITTED',input_ref=command.ref,effect_payload_ref=None,read_reservation=None)
            slot=seal('ActiveSlot',store_id=key['store_id'],project_id=key['project_id'],purpose_id=key['purpose_id'],job_id=job_id,key_ref=c['key_ref'],status='HELD',occupied_since_revision=1,released_at_revision=None)
            receipt=seal('AcceptanceReceipt',receipt_id=identifier(mutation_id+'receipt'),store_id=key['store_id'],job_id=job_id,created_mutation_id=mutation_id,key_ref=c['key_ref'],request_ref=c['request_ref'],initial_permit_ref=c['permit_ref'],accepted_job_revision=1,accepted_store_sequence=policy.increment(snap['sequence']),acceptance_event_ref=ev.ref,commit_profile='FAKE_STORE_NOT_DURABILITY_PROOF')
            job=seal('JobRecord',job_id=job_id,created_mutation_id=mutation_id,last_mutation_id=mutation_id,
                namespace_ref=self.namespace.ref,key_ref=c['key_ref'],request_ref=c['request_ref'],initial_permit_ref=c['permit_ref'],state='DRAFT',revision=1,cancel_requested=False,generation_operation_id=None,attempt_id=None,effect_token=None,last_event_ref=ev.ref,last_error_ref=None,result_ref=None,active_slot_ref=slot.ref,controller_incarnation=self.token['incarnation'],worker_id=None,lease_epoch=0,lease_until_tick=None,clock_epoch_id=None,provider_cursor=0,read_checkpoint=None)
            return self._commit(snap,expected,(ev,slot,receipt,job),objects,'ACQUIRE')
        return self._call('ADMIT',run,command=command,mutation_id=mutation_id)

    def _change(self,snap,job,mutation_id,target,kind,input_record=None,changes=None,event_type='STATE_CHANGED',worker=None,reservation=None,extras=()):
        old=job.value;j=dict(old);j.update(changes or {});j['state']=target;j['revision']=policy.increment(old['revision']);j['last_mutation_id']=mutation_id
        mr=seal('StoreMutationIntent',mutation_id=mutation_id,mutation_kind=kind,job_id=j['job_id'],expected_revision=old['revision'],target_state=None if kind in ('CLAIM','RENEW','READ_RESERVE') else target,input_ref=input_record.ref if input_record else None,cancel_requested=j['cancel_requested'])
        objects=self._objects(snap,tuple(extras)+((input_record,) if input_record else ()))
        ev=seal('StoreEvent',event_id=identifier(mutation_id+'event'),job_id=j['job_id'],mutation_id=mutation_id,
                sequence=policy.increment(resolve(old['last_event_ref'],objects)['sequence']),previous_event_ref=old['last_event_ref'],state_from=old['state'],state_to=target,revision_from=old['revision'],revision_to=j['revision'],event_type=event_type,input_ref=mr.value['input_ref'],effect_payload_ref=input_record.ref if target=='SUBMITTING' and old['state']=='QUEUED' and input_record else None,read_reservation=reservation)
        members=[ev];slot_action='RETAIN'
        if target in TERMINAL:
            slot=resolve(old['active_slot_ref'],objects);slot.pop('kind');slot.pop('version');slot.pop('scope');slot.update(status='RELEASED',released_at_revision=j['revision'])
            released=seal('ActiveSlot',**slot);members.append(released);j['active_slot_ref']=released.ref;slot_action='RELEASE'
        j['last_event_ref']=ev.ref
        members.append(seal('JobRecord',**{k:v for k,v in j.items() if k not in ('kind','version','scope')}))
        if target=='SUBMITTING' and old['state']=='QUEUED':
            payload=input_record.value
            outbox=seal('OutboxEnvelope',outbox_id=identifier(mutation_id+'outbox'),namespace_ref=self.namespace.ref,
                generation_operation_id=payload['generation_operation_id'],attempt_id=payload['attempt_id'],effect_token=payload['effect_token'],payload_ref=input_record.ref,owner_event_ref=ev.ref)
            members.append(outbox)
        return self._commit(snap,mr,tuple(members),objects,slot_action,worker)

    def advance(self,job_id,revision,mutation_id,target):
        def run():
            snap=self._view();job=self._job(snap,job_id);objects=self._objects(snap)
            now=self._guard(job,revision)
            require((job.value['state'],target) in {('DRAFT','AWAITING_APPROVAL'),('AWAITING_APPROVAL','APPROVED'),('APPROVED','QUEUED')},'ILLEGAL_TRANSITION')
            self._permit(job,objects,now);policy.capacity(self.authority)
            permit=objects[job.value['initial_permit_ref']['digest']]
            return self._change(snap,job,mutation_id,target,'STATE_CHANGE',permit)
        return self._call('ADMIT',run,job_id=job_id,mutation_id=mutation_id)

    def claim(self,job_id,revision,mutation_id,worker_id,lease_ticks):
        def run():
            snap=self._view();job=self._job(snap,job_id);j=job.value;now=self._guard(job,revision)
            require(j['state'] in policy.CLAIM_STATES,'ILLEGAL_TRANSITION')
            require(type(lease_ticks) is int and 1<=lease_ticks<=10000 and now+lease_ticks<=10000,'RESOURCE_LIMIT')
            if j['worker_id'] is not None:
                require(j['clock_epoch_id']==self.token['clock_epoch_id'],'CLOCK_UNQUALIFIED')
                require(self.ownership.worker_dead(j['worker_id']) or now>=j['lease_until_tick'],'STALE_WORKER_FENCE')
            # One fake worker globally, not one per job.
            others=[self._job(snap,i).value for i in snap['jobs'] if i!=job_id]
            require(not any(x['worker_id'] is not None and x['state'] not in TERMINAL and x['lease_until_tick']>now and not self.ownership.worker_dead(x['worker_id']) for x in others),'RESOURCE_LIMIT')
            return self._change(snap,job,mutation_id,j['state'],'CLAIM',changes=dict(controller_incarnation=self.token['incarnation'],worker_id=worker_id,lease_epoch=policy.increment(j['lease_epoch']),lease_until_tick=now+lease_ticks,clock_epoch_id=self.token['clock_epoch_id']),event_type='LEASE_CLAIMED')
        return self._call('CLAIM',run,job_id=job_id,mutation_id=mutation_id)

    def worker_token(self,job_id):
        j=self._job(self._view(),job_id).value
        return dict(controller=dict(self.token),job_id=job_id,worker_id=j['worker_id'],lease_epoch=j['lease_epoch'],lease_until_tick=j['lease_until_tick'])

    def renew(self,job_id,revision,mutation_id,worker,lease_ticks):
        def run():
            snap=self._view();job=self._job(snap,job_id);j=job.value;now=self._guard(job,revision,worker,True)
            require(j['state'] in policy.CLAIM_STATES,'ILLEGAL_TRANSITION')
            require(type(lease_ticks) is int and 1<=lease_ticks<=10000 and j['lease_until_tick']<now+lease_ticks<=10000,'RESOURCE_LIMIT')
            return self._change(snap,job,mutation_id,j['state'],'RENEW',changes=dict(lease_until_tick=now+lease_ticks),event_type='LEASE_RENEWED',worker=worker)
        return self._call('RENEW',run,job_id=job_id,mutation_id=mutation_id)

    def prepare_submit(self,job_id,revision,mutation_id,worker):
        def run():
            snap=self._view();job=self._job(snap,job_id);j=job.value;objects=self._objects(snap)
            now=self._guard(job,revision,worker,True)
            require(j['state']=='QUEUED' and not j['cancel_requested'],'ILLEGAL_TRANSITION')
            require(j['generation_operation_id'] is None,'ATTEMPT_LIMIT')
            self._permit(job,objects,now);policy.capacity(self.authority)
            req=resolve(j['request_ref'],objects)['request']
            payload=seal('EffectPayload',namespace_ref=self.namespace.ref,job_id=job_id,generation_operation_id=identifier(job_id+'generation'),attempt_id=identifier(job_id+'attempt'),attempt_number=1,effect_token=identifier(job_id+'effect'),key_ref=j['key_ref'],request_ref=j['request_ref'],permit_ref=j['initial_permit_ref'],fixture_id=req['provider_parameters']['fixture_id'],operation='SUBMIT_SYNTHETIC')
            return self._change(snap,job,mutation_id,'SUBMITTING','STATE_CHANGE',payload,changes={n:payload.value[n] for n in ('generation_operation_id','attempt_id','effect_token')},worker=worker)
        return self._call('SUBMIT',run,job_id=job_id,mutation_id=mutation_id)

    def _payload(self,snap,job):
        boxes=[snap['objects'][r['digest']] for r in snap['outboxes'].values() if snap['objects'][r['digest']].value['effect_token']==job.value['effect_token']]
        require(len(boxes)==1,'STORE_CORRUPT')
        return snap['objects'][boxes[0].value['payload_ref']['digest']],boxes[0]

    def dispatch(self,job_id,revision,worker):
        """Exactly one modelled dispatch, never blind replay after a lost ACK."""
        def run():
            snap=self._view();job=self._job(snap,job_id);objects=self._objects(snap)
            now=self._guard(job,revision,worker,True)
            require(job.value['state']=='SUBMITTING' and not job.value['cancel_requested'],'ILLEGAL_TRANSITION')
            self._permit(job,objects,now);policy.capacity(self.authority)
            payload,box=self._payload(snap,job)
            # The ledger atomically guards immutable effect identity. A repeat is lookup-only.
            try:
                receipt=self.simulator.submit(payload,objects,now)
            except ContractError:
                raise
            except Exception as exc:
                raise ContractError('RESULT_BINDING_MISMATCH') from exc
            require(type(receipt) is Record,'RESULT_BINDING_MISMATCH')
            verify_receipt(receipt,payload,self._objects(snap,(receipt,)))
            require(self.simulator.attests(receipt,payload),'RESULT_BINDING_MISMATCH')
            return receipt
        # Receipt is data, not an APIOutcome or write authority.
        try:return run()
        except ContractError as exc:return self._failure(exc.code,'SUBMIT','UNKNOWN_COMMIT_OUTCOME' if self._pending() else None,job_id=job_id)

    def apply_proof(self,job_id,revision,mutation_id,worker,receipt,extra=()):
        def run():
            snap=self._view();job=self._job(snap,job_id);j=job.value
            self._guard(job,revision,worker,True)
            payload,_=self._payload(snap,job);objects=self._objects(snap,tuple(extra)+(receipt,))
            proof=verify_receipt(receipt,payload,objects)
            require(self.simulator.attests(receipt,payload),'RESULT_BINDING_MISMATCH')
            kind=proof['kind'];target=None;changes={}
            if receipt.digest in snap['objects'] and j['state'] in ('RUNNING','RESULT_AVAILABLE'):
                return outcome('OBSERVED',job)
            if kind=='PURE.ProviderAcceptanceReceipt':
                if j['cancel_requested']:
                    require(j['state'] in ('NEEDS_RECONCILIATION','CANCEL_REQUESTED'),'ILLEGAL_TRANSITION');target='CANCEL_REQUESTED'
                else:
                    require(j['state'] in ('SUBMITTING','NEEDS_RECONCILIATION'),'ILLEGAL_TRANSITION');target='RUNNING'
                changes['provider_cursor']=proof['provider_cursor']
            elif kind=='PURE.ProviderResultReceipt':
                require(j['state']=='RUNNING' and not j['cancel_requested'],'ILLEGAL_TRANSITION')
                require(proof['provider_cursor']>=j['provider_cursor'],'CURSOR_MISMATCH')
                target='RESULT_AVAILABLE';changes.update(result_ref=receipt.ref,provider_cursor=proof['provider_cursor'])
            elif kind=='PURE.CancellationSettlementProof':
                require(j['cancel_requested'] and j['state'] in ('CANCEL_REQUESTED','NEEDS_RECONCILIATION'),'ILLEGAL_TRANSITION');target='CANCELLED'
            else:
                require(j['state']=='NEEDS_RECONCILIATION' or (j['state']=='CANCEL_REQUESTED' and j['cancel_requested']),'ILLEGAL_TRANSITION')
                # The sole attempt is already consumed. SM10 cannot promise a
                # retry checkpoint unless its attempt-eligibility guard holds.
                require(j['cancel_requested'],'ATTEMPT_LIMIT')
                target='CANCELLED'
            if changes.get('provider_cursor',j['provider_cursor'])>j['provider_cursor']:changes['read_checkpoint']=None
            return self._change(snap,job,mutation_id,target,'APPLY_PROOF',receipt,changes=changes,event_type='PROOF_APPLIED',worker=worker,extras=extra)
        return self._call('APPLY_PROOF',run,job_id=job_id,mutation_id=mutation_id)

    def contain_uncertainty(self,job_id,revision,mutation_id,worker):
        """SM07/SM08/SM30: retain the original effect, never infer nonacceptance."""
        def run():
            snap=self._view();job=self._job(snap,job_id);j=job.value
            self._guard(job,revision,worker,True)
            target={'SUBMITTING':'SUBMISSION_UNCERTAIN','SUBMISSION_UNCERTAIN':'NEEDS_RECONCILIATION','CANCEL_REQUESTED':'NEEDS_RECONCILIATION'}.get(j['state'])
            require(target is not None,'ILLEGAL_TRANSITION')
            payload,_=self._payload(snap,job)
            return self._change(snap,job,mutation_id,target,'STATE_CHANGE',payload,worker=worker)
        return self._call('SUBMIT',run,job_id=job_id,mutation_id=mutation_id)

    def cancel(self,job_id,revision,mutation_id,worker=None):
        def run():
            snap=self._view();job=self._job(snap,job_id);j=job.value
            self._guard(job,revision,worker,j['worker_id'] is not None)
            require(j['state'] not in TERMINAL,'ILLEGAL_TRANSITION')
            pre=j['generation_operation_id'] is None
            target='CANCELLED' if pre else 'CANCEL_REQUESTED'
            return self._change(snap,job,mutation_id,target,'CANCEL',changes=dict(cancel_requested=True),event_type='CANCEL_REQUESTED',worker=worker)
        return self._call('CANCEL',run,job_id=job_id,mutation_id=mutation_id)

    def reserve_read(self,job_id,revision,mutation_id,worker,read_kind,checkpoint_id):
        def run():
            snap=self._view();job=self._job(snap,job_id);j=job.value
            self._guard(job,revision,worker,True)
            require(read_kind in ('LOOKUP','POLL'),'OPERATION_NOT_AVAILABLE')
            require(j['state'] in ('SUBMITTING','SUBMISSION_UNCERTAIN','NEEDS_RECONCILIATION','RUNNING','CANCEL_REQUESTED'),'ILLEGAL_TRANSITION')
            cp=j['read_checkpoint']
            if cp is None:cp=dict(checkpoint_id=checkpoint_id,read_kind=read_kind,base_cursor=j['provider_cursor'],calls_used=0,max_calls=3)
            require(cp['checkpoint_id']==checkpoint_id and cp['read_kind']==read_kind,'CURSOR_MISMATCH')
            require(cp['calls_used']<3,'READ_LIMIT_EXCEEDED')
            cp=dict(cp,calls_used=cp['calls_used']+1)
            reservation={k:cp[k] for k in ('checkpoint_id','read_kind','base_cursor')};reservation['call_index']=cp['calls_used']
            return self._change(snap,job,mutation_id,j['state'],'READ_RESERVE',changes=dict(read_checkpoint=cp),event_type='READ_RESERVED',worker=worker,reservation=reservation)
        return self._call('LOOKUP' if read_kind=='LOOKUP' else 'POLL',run,job_id=job_id,mutation_id=mutation_id)

    def read_reserved(self,job_id,revision,worker):
        """One scripted read per committed reservation; its fake ledger consumes it."""
        try:
            snap=self._view();job=self._job(snap,job_id);j=job.value;now=self._guard(job,revision,worker,True)
            cp=j['read_checkpoint'];require(cp is not None and cp['calls_used']>=1,'READ_LIMIT_EXCEEDED')
            payload,_=self._payload(snap,job)
            reservations=[r for r in snap['objects'].values() if r.value['kind']=='PURE.StoreEvent' and r.value['job_id']==job_id and r.value['read_reservation']==dict(checkpoint_id=cp['checkpoint_id'],read_kind=cp['read_kind'],call_index=cp['calls_used'],base_cursor=cp['base_cursor'])]
            require(len(reservations)==1,'STORE_CORRUPT')
            return self.simulator.read(cp['read_kind'],payload,cp['base_cursor'],self._objects(snap),now,reservations[0].ref)
        except ContractError as exc:return self._failure(exc.code,'LOOKUP','UNKNOWN_COMMIT_OUTCOME' if self._pending() else None,job_id=job_id)

    def resolve_commit(self,mutation_id):
        def run():
            snap=self._view(allow_pending=True)
            require(mutation_id in snap['mutations'],'STORE_CORRUPT')
            try:
                proof,objects=self.store.inspect_mutation(mutation_id)
            except ContractError:
                raise
            except Exception as exc:
                raise ContractError('STORE_UNAVAILABLE') from exc
            require(proof is not None,'UNKNOWN_COMMIT_OUTCOME')
            validate_record(proof,objects)
            require(proof.value['namespace_ref']==self.namespace.ref and proof.value['mutation_ref']==snap['mutations'][mutation_id]['intent'],'STORE_CORRUPT')
            plan=self._uncertain.get(mutation_id)
            if plan is not None and proof.value['outcome']=='COMMITTED':
                require(proof.value['write_set_ref']==plan.write_set.ref,'STORE_CORRUPT')
            try:
                self._acknowledge(mutation_id,proof)
            except ContractError:
                raise
            except Exception as exc:
                raise ContractError('STORE_UNAVAILABLE') from exc
            if proof.value['outcome']=='NOT_COMMITTED':
                intent=resolve(proof.value['mutation_ref'],objects)
                command=objects[intent['input_ref']['digest']] if intent['mutation_kind']=='ADMIT' else None
                return self._failure('MUTATION_NOT_COMMITTED','RESOLVE_COMMIT','NOT_COMMITTED',job_id=intent['job_id'],command=command,mutation_id=mutation_id)
            ws=resolve(proof.value['write_set_ref'],objects)
            job=next(objects[x['digest']] for x in ws['members'] if x['kind']=='PURE.JobRecord')
            receipt=next((objects[x['digest']] for x in ws['members'] if x['kind']=='PURE.AcceptanceReceipt'),None)
            return outcome('ACCEPTED' if receipt else 'APPLIED',job,receipt,'COMMITTED')
        return self._call('RESOLVE_COMMIT',run,mutation_id=mutation_id)
