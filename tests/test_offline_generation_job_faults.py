"""Fault-boundary oracles. All persistence and crashes here are fake snapshots."""
from copy import deepcopy
import pytest
from experimental_mvp.offline_execution.contracts import Record, ContractError, seal
from test_offline_generation_job_controller import Lab, uid, expect_error


def test_R01_before_commit_complete_absence_not_committed():
    l=Lab();l.store.fault='before';mid=l.mid();out=l.c.admit(l.command,mid)
    expect_error(out,'MUTATION_NOT_COMMITTED');assert out['mutation_outcome']=='NOT_COMMITTED'
    assert not l.store.state['jobs'] and not l.store.state['receipts'] and l.ledger.calls==0
    proof,objects=l.store.inspect_mutation(mid);assert proof.value['outcome']=='NOT_COMMITTED'
    assert l.c.admit(l.command,mid)['disposition']=='ACCEPTED'


def test_R02_R16_lost_commit_ack_restart_resolves_same_mutation():
    l=Lab();mid=l.mid();l.store.fault='after';out=l.c.admit(l.command,mid)
    expect_error(out,'UNKNOWN_COMMIT_OUTCOME');assert len(l.store.state['jobs'])==1
    before=l.store.commits;l.restart();out=l.c.resolve_commit(mid)
    assert out['disposition']=='ACCEPTED' and out['mutation_outcome']=='COMMITTED';assert l.store.commits==before
    replay=l.c.admit(l.command,l.mid());assert replay['receipt_ref']==out['receipt_ref'] and replay['disposition']=='REUSED'


def test_R03_unknown_commit_proven_absent_not_missing_marker_only():
    l=Lab();mid=l.mid();l.store.fault='during';out=l.c.admit(l.command,mid);expect_error(out,'UNKNOWN_COMMIT_OUTCOME')
    l.restart();out=l.c.resolve_commit(mid);expect_error(out,'MUTATION_NOT_COMMITTED')
    assert out['mutation_outcome']=='NOT_COMMITTED' and not l.store.state['pending']
    assert l.c.admit(l.command,mid)['disposition']=='ACCEPTED'


def test_R04_partial_corrupt_view_preserves_unknown():
    l=Lab();mid=l.mid();l.store.fault='partial';l.c.admit(l.command,mid)
    out=l.c.resolve_commit(mid);expect_error(out,'STORE_CORRUPT');assert out['mutation_outcome']=='UNKNOWN_COMMIT_OUTCOME'
    assert mid in l.store.state['pending'] and l.ledger.calls==0
    # Even if a harness mistakenly marks view integral, orphan member forbids absence proof.
    l.store.state['integrity']=True
    expect_error(l.c.resolve_commit(mid),'STORE_CORRUPT');assert mid in l.store.state['pending']


def test_R05_unavailable_never_not_found_or_not_committed():
    l=Lab();mid=l.mid();l.store.fault='after';l.c.admit(l.command,mid);l.store.state['available']=False
    out=l.c.resolve_commit(mid);expect_error(out,'STORE_UNAVAILABLE');assert out['mutation_outcome']=='UNKNOWN_COMMIT_OUTCOME'
    assert mid in l.store.state['pending']


def test_R06_restart_without_retained_operation_identity_holds():
    l=Lab();mid=l.mid();l.store.fault='during';l.c.admit(l.command,mid);l.store.registry.clear();l.restart()
    expect_error(l.c.resolve_commit(mid),'STORE_CORRUPT');assert l.store.state['pending']
    expect_error(l.c.admit(l.command,l.mid()),'UNKNOWN_COMMIT_OUTCOME')


def test_A06_unknown_terminal_commit_cannot_free_slot_or_admit():
    l=Lab();l.admit();mid=l.mid();l.store.fault='during'
    expect_error(l.c.cancel(l.job_id,l.job().value['revision'],mid),'UNKNOWN_COMMIT_OUTCOME')
    assert l.store.state['slots'];before=l.store.commits
    expect_error(l.c.admit(l.variant(),l.mid()),'UNKNOWN_COMMIT_OUTCOME');assert l.store.commits==before
    l.c.resolve_commit(mid);assert l.store.state['slots']


def test_R07_E07_E08_stale_worker_and_cas_never_write_error_or_event():
    l=Lab();l.submitting();old=deepcopy(l.worker);before=l.store.snapshot();before_count=l.store.commits
    stale=deepcopy(old);stale['lease_epoch']+=1
    out=l.c.prepare_submit(l.job_id,0,l.mid(),stale);expect_error(out,'STALE_WORKER_FENCE')
    assert l.store.snapshot()==before and l.store.commits==before_count
    out=l.c.prepare_submit(l.job_id,0,l.mid(),old);expect_error(out,'CAS_CONFLICT');assert l.store.snapshot()==before


def test_R08_E14_new_owner_current_claim_applies_unchanged_old_receipt():
    l=Lab();l.submitting();old_controller=l.c;old_worker=deepcopy(l.worker)
    a=l.c.dispatch(l.job_id,l.job().value['revision'],l.worker);assert isinstance(a,Record)
    identity={k:l.job().value[k] for k in ('generation_operation_id','attempt_id','effect_token')}
    l.restart(replace_owner=True);rev=l.job().value['revision']
    out=l.c.claim(l.job_id,rev,l.mid(),uid(201),100);assert out['disposition']=='APPLIED',out
    l.worker=l.c.worker_token(l.job_id);before=l.store.snapshot()
    expect_error(old_controller.apply_proof(l.job_id,l.job().value['revision'],l.mid(),old_worker,a),'STALE_CONTROLLER_FENCE');assert l.store.snapshot()==before
    out=l.c.apply_proof(l.job_id,l.job().value['revision'],l.mid(),l.worker,a);assert out['disposition']=='APPLIED',out
    assert l.job().value['state']=='RUNNING' and a.digest in l.store.state['objects']
    assert all(l.job().value[k]==v for k,v in identity.items()) and l.ledger.calls==1


def test_R09_cancel_recovered_identity_does_not_clear_cancel():
    l=Lab();l.submitting();l.ledger.lose_ack=True
    expect_error(l.c.dispatch(l.job_id,l.job().value['revision'],l.worker),'RESULT_BINDING_MISMATCH')
    out=l.c.cancel(l.job_id,l.job().value['revision'],l.mid(),l.worker);assert out['disposition']=='APPLIED',out
    # SM30 then recovered identity must use SM31, not SM09.
    out=l.c.contain_uncertainty(l.job_id,l.job().value['revision'],l.mid(),l.worker);assert out['disposition']=='APPLIED',out
    assert l.job().value['state']=='NEEDS_RECONCILIATION'
    out=l.c.reserve_read(l.job_id,l.job().value['revision'],l.mid(),l.worker,'LOOKUP',uid(601));assert out['disposition']=='APPLIED',out
    receipt=l.c.read_reserved(l.job_id,l.job().value['revision'],l.worker);assert isinstance(receipt,Record)
    out=l.c.apply_proof(l.job_id,l.job().value['revision'],l.mid(),l.worker,receipt);assert out['disposition']=='APPLIED',out
    assert l.job().value['state']=='CANCEL_REQUESTED' and l.job().value['cancel_requested']
    expect_error(l.c.dispatch(l.job_id,l.job().value['revision'],l.worker),'ILLEGAL_TRANSITION')


def test_R10_live_owner_lock_cannot_be_stolen_by_ttl():
    l=Lab();l.claimed();l.clock.tick=200
    with pytest.raises(ContractError) as e:l.owner.acquire(uid(102))
    assert e.value.code=='STALE_CONTROLLER_FENCE'


@pytest.mark.parametrize('change',['epoch','rollback','unqualified'])
def test_R11_clock_change_never_forces_expiry_or_claim(change):
    l=Lab();l.claimed();l.clock.tick=2;l.c._now();before=l.store.snapshot()
    if change=='epoch':l.clock.epoch=uid(123)
    elif change=='rollback':l.clock.tick=1
    else:l.clock.qualified=False
    l.restart();expect_error(l.c.claim(l.job_id,l.job().value['revision'],l.mid(),uid(201),10),'CLOCK_UNQUALIFIED')
    assert l.store.snapshot()==before


def test_R12_E09_E10_E11_reserved_calls_survive_crash_restart_and_bound_three():
    l=Lab();l.submitting();checkpoint=uid(700)
    for i in range(3):
        out=l.c.reserve_read(l.job_id,l.job().value['revision'],l.mid(),l.worker,'LOOKUP',checkpoint)
        assert out['disposition']=='APPLIED',out
        l.restart()  # No call: the interruption conservatively consumes the reservation.
        assert l.job().value['read_checkpoint']['calls_used']==i+1
    before=l.store.snapshot();expect_error(l.c.reserve_read(l.job_id,l.job().value['revision'],l.mid(),l.worker,'LOOKUP',checkpoint),'READ_LIMIT_EXCEEDED')
    assert l.store.snapshot()==before and l.ledger.calls==l.ledger.read_calls==0
    expect_error(l.c.reserve_read(l.job_id,l.job().value['revision'],l.mid(),l.worker,'LOOKUP',uid(701)),'CURSOR_MISMATCH')


def test_R13_duplicate_cursor_receipt_never_resets_checkpoint():
    l=Lab();a=l.running();l.c.reserve_read(l.job_id,l.job().value['revision'],l.mid(),l.worker,'POLL',uid(702))
    before=l.store.snapshot();out=l.c.apply_proof(l.job_id,l.job().value['revision'],l.mid(),l.worker,a)
    assert out['disposition']=='OBSERVED' and l.store.snapshot()==before


def test_R14_wrong_payload_proof_rejected():
    l=Lab();l.submitting();a=l.c.dispatch(l.job_id,l.job().value['revision'],l.worker)
    v=a.value;v={k:v for k,v in v.items() if k not in ('kind','version','scope')};v['effect_token']=uid(888)
    bad=seal('ProviderAcceptanceReceipt',**v);before=l.store.snapshot()
    expect_error(l.c.apply_proof(l.job_id,l.job().value['revision'],l.mid(),l.worker,bad),'RESULT_BINDING_MISMATCH')
    assert l.store.snapshot()==before


def test_R15_unknown_claim_commit_permits_no_read_or_effect():
    l=Lab();l.queued();mid=l.mid();l.store.fault='after'
    expect_error(l.c.claim(l.job_id,l.job().value['revision'],mid,uid(200),100),'UNKNOWN_COMMIT_OUTCOME')
    fake_worker=dict(controller=l.token,job_id=l.job_id,worker_id=uid(200),lease_epoch=1,lease_until_tick=101)
    expect_error(l.c.prepare_submit(l.job_id,l.job().value['revision'],l.mid(),fake_worker),'UNKNOWN_COMMIT_OUTCOME')
    assert l.ledger.calls==l.ledger.read_calls==0
    l.c.resolve_commit(mid);assert not l.store.state['pending']


def test_E12_unknown_commit_precedes_logical_admission_conflict():
    l=Lab();l.store.fault='after';l.c.admit(l.command,l.mid())
    expect_error(l.c.admit(l.variant(),l.mid()),'UNKNOWN_COMMIT_OUTCOME')


def test_A06_terminal_committed_lost_ACK_still_blocks_new_admission():
    l=Lab();l.admit();l.store.fault='after';mid=l.mid()
    expect_error(l.c.cancel(l.job_id,l.job().value['revision'],mid),'UNKNOWN_COMMIT_OUTCOME')
    assert not l.store.state['slots']  # Physical commit happened; outcome is still held.
    cmd=l.variant();expect_error(l.c.admit(cmd,l.mid()),'UNKNOWN_COMMIT_OUTCOME')
    assert len(l.store.state['jobs'])==1
    assert l.c.resolve_commit(mid)['disposition']=='APPLIED'
    assert l.c.admit(cmd,l.mid())['disposition']=='ACCEPTED'
