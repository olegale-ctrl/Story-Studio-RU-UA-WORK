"""One metadata-only simulator facade over an explicitly injected scripted ledger.

It does not implement storage, generate bytes, access time, or contact providers.
"""
from typing import Protocol
from .contracts import require, validate_record, resolve


class LedgerPort(Protocol):
    def submit(self, payload, tick): ...
    def attests(self, receipt, payload): ...
    def lookup(self, payload, tick, reservation): ...
    def poll(self, payload, cursor, tick, reservation): ...


class MetadataSimulator:
    def __init__(self, ledger):
        self._ledger=ledger

    def attests(self, receipt, payload):
        return self._ledger.attests(receipt,payload)

    def submit(self, payload, objects, tick):
        validate_record(payload,objects)
        require(payload.value['operation']=='SUBMIT_SYNTHETIC','OPERATION_NOT_AVAILABLE')
        return self._ledger.submit(payload,tick)

    def read(self, kind, payload, cursor, objects, tick, reservation):
        validate_record(payload,objects)
        require(kind in ('LOOKUP','POLL'),'OPERATION_NOT_AVAILABLE')
        event=resolve(reservation,objects)
        require(event['kind']=='PURE.StoreEvent' and event['event_type']=='READ_RESERVED','READ_LIMIT_EXCEEDED')
        require(event['job_id']==payload.value['job_id'] and event['read_reservation']['read_kind']==kind and event['read_reservation']['base_cursor']==cursor,'RESULT_BINDING_MISMATCH')
        return self._ledger.lookup(payload,tick,reservation) if kind=='LOOKUP' else self._ledger.poll(payload,cursor,tick,reservation)


def verify_receipt(record, payload, objects):
    validate_record(record,objects)
    value=record.value; expected=payload.value
    require(value['kind'] in ('PURE.ProviderAcceptanceReceipt','PURE.ProviderResultReceipt','PURE.ProviderNonAcceptanceProof','PURE.CancellationSettlementProof'),'RESULT_BINDING_MISMATCH')
    for name in ('generation_operation_id','attempt_id','effect_token'):
        require(value[name]==expected[name],'RESULT_BINDING_MISMATCH')
    if value['kind']=='PURE.ProviderResultReceipt':
        acceptance=resolve(value['acceptance_ref'],objects)
        require(acceptance['payload_ref']==payload.ref,'RESULT_BINDING_MISMATCH')
    elif value['kind']!='PURE.CancellationSettlementProof':
        require(value['payload_ref']==payload.ref and value['namespace_ref']==expected['namespace_ref'],'RESULT_BINDING_MISMATCH')
    else:
        require(value['namespace_ref']==expected['namespace_ref'],'RESULT_BINDING_MISMATCH')
        known=[r.value for r in objects.values() if r.value['kind']=='PURE.ProviderAcceptanceReceipt' and r.value['payload_ref']==payload.ref]
        if value['settlement']=='NO_EFFECT':
            require(not known,'RESULT_BINDING_MISMATCH')
        else:
            require(known and all(a['provider_job_id']==value['provider_job_id'] for a in known),'RESULT_BINDING_MISMATCH')
    return value
