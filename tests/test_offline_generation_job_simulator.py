"""Consumer oracles against trusted scripted metadata, never producer qualification."""
from copy import deepcopy
import pytest
from experimental_mvp.offline_execution.contracts import Record, seal
from test_offline_generation_job_controller import Lab, uid, expect_error


def test_lost_submit_ACK_recovery_uses_lookup_same_effect_not_resubmit():
    l=Lab();l.submitting();l.ledger.lose_ack=True;original=l.job().value['effect_token']
    out=l.c.dispatch(l.job_id,l.job().value['revision'],l.worker);expect_error(out,'RESULT_BINDING_MISMATCH')
    assert out['error']['external_effect']=='UNKNOWN' and out['mutation_outcome'] is None
    expect_error(l.c.dispatch(l.job_id,l.job().value['revision'],l.worker),'ATTEMPT_LIMIT')
    assert l.ledger.calls==1
    l.c.contain_uncertainty(l.job_id,l.job().value['revision'],l.mid(),l.worker)
    l.c.contain_uncertainty(l.job_id,l.job().value['revision'],l.mid(),l.worker)
    l.restart(replace_owner=True)
    assert l.c.claim(l.job_id,l.job().value['revision'],l.mid(),uid(201),100)['disposition']=='APPLIED'
    l.worker=l.c.worker_token(l.job_id)
    assert l.c.reserve_read(l.job_id,l.job().value['revision'],l.mid(),l.worker,'LOOKUP',uid(800))['disposition']=='APPLIED'
    a=l.c.read_reserved(l.job_id,l.job().value['revision'],l.worker);assert isinstance(a,Record)
    assert l.c.apply_proof(l.job_id,l.job().value['revision'],l.mid(),l.worker,a)['disposition']=='APPLIED'
    assert l.job().value['state']=='RUNNING' and l.job().value['effect_token']==original and l.ledger.calls==1


def test_each_committed_reservation_read_once_and_failure_consumes_budget():
    l=Lab();l.running();l.c.reserve_read(l.job_id,l.job().value['revision'],l.mid(),l.worker,'POLL',uid(801))
    result=l.c.read_reserved(l.job_id,l.job().value['revision'],l.worker);assert isinstance(result,Record)
    expect_error(l.c.read_reserved(l.job_id,l.job().value['revision'],l.worker),'READ_LIMIT_EXCEEDED')
    assert l.ledger.read_calls==1
    for _ in range(2):
        assert l.c.reserve_read(l.job_id,l.job().value['revision'],l.mid(),l.worker,'POLL',uid(801))['disposition']=='APPLIED'
        l.ledger.read_unavailable=True;expect_error(l.c.read_reserved(l.job_id,l.job().value['revision'],l.worker),'STORE_UNAVAILABLE')
    expect_error(l.c.reserve_read(l.job_id,l.job().value['revision'],l.mid(),l.worker,'POLL',uid(801)),'READ_LIMIT_EXCEEDED')
    assert l.ledger.read_calls==3 and l.ledger.calls==1


def test_E16_fake_result_is_not_mp4_rights_or_completion():
    l=Lab();r=l.result()
    assert r.value['producer_qualification']=='UNQUALIFIED_FAKE_ONLY'
    assert not any(k in r.value for k in ('path','url','asset_id','license','mp4','production_permission'))
    assert l.job().value['state']=='RESULT_AVAILABLE'


def test_unknown_receipt_hash_not_authoritative_provider_evidence():
    l=Lab();l.submitting();a=l.c.dispatch(l.job_id,l.job().value['revision'],l.worker)
    value=a.value;value={k:v for k,v in value.items() if k not in ('kind','version','scope')};value['provider_job_id']=uid(999)
    forged=seal('ProviderAcceptanceReceipt',**value);before=l.store.snapshot()
    expect_error(l.c.apply_proof(l.job_id,l.job().value['revision'],l.mid(),l.worker,forged),'RESULT_BINDING_MISMATCH')
    assert l.store.snapshot()==before


def test_cancel_known_settlement_releases_slot_atomically():
    l=Lab();a=l.running();assert l.c.cancel(l.job_id,l.job().value['revision'],l.mid(),l.worker)['disposition']=='APPLIED'
    j=l.job().value
    proof=seal('CancellationSettlementProof',namespace_ref=l.namespace.ref,generation_operation_id=j['generation_operation_id'],attempt_id=j['attempt_id'],effect_token=j['effect_token'],settlement='CANCELLED',provider_job_id=a.value['provider_job_id'],external_effect='KNOWN',billed_minor=0,settled_tick=l.clock.tick,producer_qualification='UNQUALIFIED_FAKE_ONLY')
    l.ledger.objects[proof.digest]=proof
    assert l.c.apply_proof(l.job_id,l.job().value['revision'],l.mid(),l.worker,proof)['disposition']=='APPLIED'
    assert l.job().value['state']=='CANCELLED' and not l.store.state['slots']


def test_nonacceptance_proof_is_not_another_attempt_authorization():
    l=Lab();l.submitting()
    l.c.contain_uncertainty(l.job_id,l.job().value['revision'],l.mid(),l.worker)
    l.c.contain_uncertainty(l.job_id,l.job().value['revision'],l.mid(),l.worker)
    p,_=l.c._payload(l.store.snapshot(),l.job());v=p.value
    proof=seal('ProviderNonAcceptanceProof',namespace_ref=l.namespace.ref,generation_operation_id=v['generation_operation_id'],attempt_id=v['attempt_id'],effect_token=v['effect_token'],payload_ref=p.ref,ledger_sequence=0,observed_tick=l.clock.tick,outcome='NOT_ACCEPTED',billed_minor=0,producer_qualification='UNQUALIFIED_FAKE_ONLY')
    l.ledger.objects[proof.digest]=proof
    before=l.store.snapshot()
    expect_error(l.c.apply_proof(l.job_id,l.job().value['revision'],l.mid(),l.worker,proof),'ATTEMPT_LIMIT')
    assert l.store.snapshot()==before and l.job().value['state']=='NEEDS_RECONCILIATION'
    expect_error(l.c.prepare_submit(l.job_id,l.job().value['revision'],l.mid(),l.worker),'ILLEGAL_TRANSITION');assert l.ledger.calls==0
    assert l.c.cancel(l.job_id,l.job().value['revision'],l.mid(),l.worker)['disposition']=='APPLIED'
    assert l.c.apply_proof(l.job_id,l.job().value['revision'],l.mid(),l.worker,proof)['disposition']=='APPLIED'
    assert l.job().value['state']=='CANCELLED'


def test_outbox_and_complete_committed_transaction_precede_simulator_call():
    l=Lab();l.submitting();submit=l.ledger.submit;observations=[]
    def checked(payload,tick):
        snapshot=l.store.snapshot()
        assert not snapshot['pending'] and snapshot['outboxes']
        box=next(snapshot['objects'][ref['digest']] for ref in snapshot['outboxes'].values())
        assert box.value['payload_ref']==payload.ref
        event=snapshot['objects'][box.value['owner_event_ref']['digest']]
        proof,_=l.store.inspect_mutation(event.value['mutation_id'])
        assert proof.value['outcome']=='COMMITTED'
        observations.append(proof.ref)
        return submit(payload,tick)
    l.ledger.submit=checked
    assert isinstance(l.c.dispatch(l.job_id,l.job().value['revision'],l.worker),Record)
    assert len(observations)==l.ledger.calls==1


def test_contradictory_no_effect_settlement_cannot_erase_known_acceptance():
    l=Lab();l.running();l.c.cancel(l.job_id,l.job().value['revision'],l.mid(),l.worker)
    j=l.job().value
    proof=seal('CancellationSettlementProof',namespace_ref=l.namespace.ref,generation_operation_id=j['generation_operation_id'],attempt_id=j['attempt_id'],effect_token=j['effect_token'],settlement='NO_EFFECT',provider_job_id=None,external_effect='NONE',billed_minor=0,settled_tick=l.clock.tick,producer_qualification='UNQUALIFIED_FAKE_ONLY')
    l.ledger.objects[proof.digest]=proof;before=l.store.snapshot()
    expect_error(l.c.apply_proof(l.job_id,l.job().value['revision'],l.mid(),l.worker,proof),'RESULT_BINDING_MISMATCH')
    assert l.store.snapshot()==before and l.job().value['state']=='CANCEL_REQUESTED'
