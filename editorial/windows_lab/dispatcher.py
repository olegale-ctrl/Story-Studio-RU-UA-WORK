"""Single-writer synthetic RAM dispatcher. No Windows identity or native IO.

Caller is injected by a trusted harness, never constructed from LAB request data.
All fault names simulate observations; no OS fault or durability is qualified.
"""
from dataclasses import dataclass
import hashlib
import threading

from editorial import storage_protocol_v1 as s1
from editorial import storage_transaction_model_v1 as model
from . import protocol as p
from .fixtures import Factory, PRINCIPALS, KEY, c


@dataclass(frozen=True)
class Caller:
    actor: str

    def __post_init__(self):
        p.require(self.actor in ('A', 'B'))


class DeliveryLost(RuntimeError):
    """Synthetic response/crash signal; deliberately carries no receipt."""


class Dispatcher:
    def __init__(self, run_id, incarnation, policy_case='CG_NONE', fault_case='NONE'):
        p.uuid(run_id)
        self.run_id, self.incarnation = run_id, incarnation
        self.factory = Factory(incarnation, policy_case, fault_case)
        self._entries = {}
        self.model_calls = 0
        self._fault_used = False
        self._lock = threading.Lock()
        self._quarantined = False
        self._dead = False

    @property
    def admissions(self):
        return len(self._entries)

    def execute_frame(self, actor, probe, slot=0):
        """Trusted harness helper for the finite synthetic whitelist, not an endpoint."""
        _, transaction = self.factory.candidate(actor, probe, slot)
        return p.encode_lab({'lab_version':1,'scope':p.SCOPE,'kind':'EXECUTE',
            'run_id':self.run_id,'incarnation_id':self.incarnation,'request':transaction.command['request']})

    def _result(self, request, outcome, code=None, summary=None, admission='NONE'):
        return p.encode_lab({'lab_version':1,'scope':p.SCOPE,'kind':'RESULT',
            'run_id':self.run_id,'incarnation_id':self.incarnation,
            'request_id':request.get('request_id'),
            'request_bytes_sha256':hashlib.sha256(c(request)).hexdigest() if request.get('request_version') else request.get('request_bytes_sha256'),
            'outcome':outcome,'mock_admission':admission,'mock_summary':summary,
            'error':None if code is None else {'code':code,'field_path':'$','s1_code':None},'lab_only':True})

    def dispatch(self, frame, caller):
        p.require(type(caller) is Caller)
        if self._dead:
            raise DeliveryLost('Synthetic process is stopped')
        message = p.decode_lab(frame)
        p.require(message['kind'] in ('HELLO','EXECUTE','LOOKUP'))
        request = message.get('request', message if message['kind'] == 'LOOKUP' else {})
        if message['run_id'] != self.run_id:
            return self._result(request,'DENIED','LAB_RUN_MISMATCH')
        if message['kind'] == 'HELLO':
            return p.encode_lab({'lab_version':1,'scope':p.SCOPE,'kind':'HELLO_RESULT',
                'run_id':self.run_id,'incarnation_id':self.incarnation,'nonce':message['nonce'],
                'limits_id':'LAB_LIMITS_1','fixture_set':'S32_FIXTURES_1',
                'fixture_case':{'policy_case':self.factory.policy_case,'fault_case':self.factory.fault_case},'lab_only':True})
        if message['incarnation_id'] != self.incarnation:
            return self._result(request,'UNKNOWN_AFTER_RESTART','LAB_RESTART_UNKNOWN',admission='UNKNOWN')
        if not self._lock.acquire(blocking=False):
            return self._result(request,'NOT_ADMITTED','LAB_BUSY')
        try:
            return self._dispatch(message, request, caller.actor)
        finally:
            self._lock.release()

    def _dispatch(self, message, request, actor):
        lookup = message['kind'] == 'LOOKUP'
        raw = None if lookup else c(request)
        entry = self._entries.get(request['request_id'])
        if entry:
            if entry['actor'] != actor or (raw is not None and raw != entry['bytes']):
                return self._result(request,'DENIED','LAB_IDEMPOTENCY_CONFLICT')
            if lookup and request['request_bytes_sha256'] != hashlib.sha256(entry['bytes']).hexdigest():
                return self._result(request,'DENIED','LAB_IDEMPOTENCY_CONFLICT')
            return entry['response']
        location = self.factory.locate(actor, request['request_id'])
        if not lookup and request['operation'] == 'PUBLISH_REVISION':
            return self._result(request,'DENIED','LAB_POLICY_DENIED')
        if location is None:
            return self._result(request,'DENIED','LAB_FIXTURE_NOT_ALLOWED')
        if lookup:
            return self._result(request,'NOT_ADMITTED','LAB_NOT_FOUND')
        probe, slot = location
        store, transaction = self.factory.candidate(actor, probe, slot)
        if raw != c(transaction.command['request']):
            return self._result(request,'DENIED','LAB_FIXTURE_NOT_ALLOWED')
        if not self.factory.allowed(actor, probe):
            return self._result(request,'DENIED','LAB_POLICY_DENIED')
        if self.admissions >= 32:
            return self._result(request,'NOT_ADMITTED','LAB_CAPACITY')
        if self._quarantined:
            return self._result(request,'NOT_ADMITTED','LAB_BUSY')
        fault = self.factory.fault_case if not self._fault_used else 'NONE'
        if fault != 'NONE':
            self._fault_used = True
        if fault in ('IMPERSONATE_FALSE','THREAD_TOKEN_QUERY_FALSE','REVERT_FALSE','RESIDUAL_TOKEN'):
            # Pure harness denial ONLY. A native adapter must enforce actual fail-stop.
            return self._result(request,'DENIED','LAB_POLICY_DENIED')
        if fault in ('READ_STALL','DISPATCH_STALL'):
            return self._result(request,'NOT_ADMITTED','LAB_BUSY')
        if fault == 'PRE_ADMISSION_DENY':
            return self._result(request,'DENIED','LAB_POLICY_DENIED')
        if fault == 'CRASH_PRE_ADMISSION':
            self._quarantined = True
            self._dead = True
            raise DeliveryLost('Synthetic crash before admission')
        engine = model.TransactionModel(store, keys={'fixture-key':KEY},
                                        authority=self.factory.authority(transaction, actor))
        if fault in ('PAUSE_AFTER_RAM_PREPARE','PAUSE_AFTER_RAM_INTENT'):
            store.arm(model.Fault('W3.anchor.flush' if fault.endswith('PREPARE') else 'W4.INTENT.journal.flush','after'))
        self.model_calls += 1
        before_events = len(store.events)
        try:
            outcome = engine.execute(transaction)
        except model.SimulatedCrash:
            if fault not in ('PAUSE_AFTER_RAM_PREPARE','PAUSE_AFTER_RAM_INTENT'):
                self._quarantined = True
                raise
            response = self._result(request,'MOCK_PENDING',admission='RAM')
            self._quarantined = True
        except s1.ProtocolError:
            if len(store.events) == before_events:
                return self._result(request,'DENIED','LAB_ENGINE_FAILURE')
            # Never claim a terminal status from failed/partial verification.
            self._quarantined = True
            response = self._result(request,'MOCK_PENDING','LAB_ENGINE_FAILURE',admission='UNKNOWN')
        else:
            if outcome.state not in ('FINALIZED','ABORTED') or outcome.receipt is None:
                response = self._result(request,'MOCK_PENDING','LAB_ENGINE_FAILURE',admission='UNKNOWN')
                self._quarantined = True
            else:
                try:
                    checked = engine.inspect()
                    receipt = s1.decode_canonical_json(outcome.receipt)
                    s1.validate_wire(receipt, 'Receipt')
                    s1.verify_mac(receipt['body'], receipt['mac'], KEY, domain='receipt')
                    p.require(checked.pending is None and checked.requests[request['request_id']]['receipt'] == outcome.receipt)
                    p.require(checked.head == receipt['body']['result_head'])
                    summary = {'operation':request['operation'],'status':receipt['body']['core']['status'],
                        'virtual_record_count':len(store.visible.journal),
                        'value_sha256':p.lab_summary_sha256(outcome.receipt)}
                    response = self._result(request,'MOCK_ABORTED' if outcome.state == 'ABORTED' else 'MOCK_FINALIZED',summary=summary,admission='RAM')
                except (s1.ProtocolError, p.LabError, KeyError):
                    self._quarantined = True
                    response = self._result(request,'MOCK_PENDING','LAB_ENGINE_FAILURE',admission='UNKNOWN')
        self._entries[request['request_id']] = {'actor':actor,'bytes':raw,'response':response}
        if fault in ('RESPONSE_LOSS','CRASH_AFTER_RAM_FINAL'):
            if fault == 'CRASH_AFTER_RAM_FINAL':
                self._quarantined = True
                self._dead = True
            raise DeliveryLost('Synthetic lost delivery')
        return response
