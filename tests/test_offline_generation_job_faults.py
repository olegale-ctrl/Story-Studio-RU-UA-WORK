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


@pytest.mark.parametrize('boundary,exception_kind,read_fault',[
    ('before','raw','ok'),
    ('before','typed','oserror'),
    ('after','raw','ok'),
    ('after','typed','ok'),
    ('after','typed','oserror'),
    ('after','raw','runtime'),
    ('after','typed','typed'),
    ('after','raw','malformed'),
    ('after','return','unavailable'),
    ('after','return','corrupt'),
    ('after','return','inspect'),
    ('after','return','bad_proof'),
    ('after','return','empty_proof'),
    ('after','return','malformed'),
    ('after','return','missing_job_bytes'),
    ('after','return','missing_slot_index'),
    ('after','return','missing_receipt_index'),
])
def test_F08B3_02_commit_exception_diagnostics_preserve_namespace_hold(
        boundary,exception_kind,read_fault,monkeypatch):
    l=Lab();l.admit();mid=l.mid();before=l.store.snapshot();commits=l.store.commits
    snapshot=l.store.snapshot;commit=l.store.commit;inspect=l.store.inspect_mutation
    def broken_snapshot():
        if read_fault=='oserror':raise OSError('scripted unavailable snapshot')
        if read_fault=='runtime':raise RuntimeError('scripted unavailable snapshot')
        if read_fault=='typed':raise ContractError('STORE_UNAVAILABLE')
        snap=snapshot()
        if read_fault=='malformed':snap.pop('pending')
        if read_fault=='unavailable':snap['available']=False
        if read_fault=='corrupt':snap['integrity']=False
        if read_fault=='missing_job_bytes':snap['objects'].pop(snap['jobs'][l.job_id]['digest'])
        if read_fault=='missing_slot_index':
            # The committed terminal job has a RELEASED slot; injecting an old HELD
            # index must be rejected rather than treated as an authoritative view.
            snap['slots']=before['slots']
        if read_fault=='missing_receipt_index':snap['receipts'].clear()
        return snap
    def broken_inspect(operation):
        if read_fault=='inspect':raise RuntimeError('scripted unavailable proof')
        proof,objects=inspect(operation)
        if read_fault=='empty_proof':return None,objects
        if read_fault=='bad_proof':
            value=proof.value;value={k:v for k,v in value.items() if k not in ('kind','version','scope')}
            value['write_set_ref']={'kind':'PURE.AtomicWriteSet','digest':'f'*64}
            proof=seal('CommitResolutionProof',**value);objects[proof.digest]=proof
        return proof,objects
    def interrupted(plan):
        if boundary=='before':l.store.hold(plan);result=None
        else:result=commit(plan)
        monkeypatch.setattr(l.store,'snapshot',broken_snapshot)
        monkeypatch.setattr(l.store,'inspect_mutation',broken_inspect)
        if exception_kind=='raw':raise RuntimeError('scripted lost COMMIT ACK')
        if exception_kind=='typed':raise ContractError('CAS_CONFLICT')
        return result
    monkeypatch.setattr(l.store,'commit',interrupted)
    out=l.c.cancel(l.job_id,l.job().value['revision'],mid)
    expected=('UNKNOWN_COMMIT_OUTCOME' if exception_kind!='return' else
              'STORE_CORRUPT' if read_fault in ('corrupt','bad_proof','malformed','missing_job_bytes','missing_slot_index','missing_receipt_index') else
              'STORE_UNAVAILABLE' if read_fault in ('unavailable','inspect') else 'UNKNOWN_COMMIT_OUTCOME')
    # Commit exceptions remain UNKNOWN even when the secondary diagnostic also fails.
    expect_error(out,expected)
    assert out['disposition']=='HOLD' and out['mutation_outcome']=='UNKNOWN_COMMIT_OUTCOME'
    assert out['error']['external_effect']=='UNKNOWN'
    assert mid in l.store.state['pending'] and mid in l.c._uncertain
    if boundary=='before':
        assert l.store.state['jobs']==before['jobs'] and l.store.state['slots']==before['slots']
        assert l.store.commits==commits
    else:
        job=l.store.state['objects'][l.store.state['jobs'][l.job_id]['digest']]
        assert job.value['state']=='CANCELLED'
        assert not l.store.state['slots'] and l.store.commits==commits+1
    # Restore read access only. Neither that nor a controller restart resolves M.
    monkeypatch.setattr(l.store,'snapshot',snapshot)
    monkeypatch.setattr(l.store,'inspect_mutation',inspect)
    monkeypatch.setattr(l.store,'commit',commit)
    next_command=l.variant()
    expect_error(l.c.admit(next_command,l.mid()),'UNKNOWN_COMMIT_OUTCOME')
    l.restart();expect_error(l.c.admit(next_command,l.mid()),'UNKNOWN_COMMIT_OUTCOME')
    assert len(l.store.state['jobs'])==1 and l.ledger.calls==l.ledger.read_calls==0
    resolved=l.c.resolve_commit(mid)
    if boundary=='before':
        expect_error(resolved,'MUTATION_NOT_COMMITTED')
        assert l.store.state['slots'] and l.job().value['state']=='DRAFT'
    else:
        assert resolved['disposition']=='APPLIED' and not l.store.state['slots']
        assert l.c.admit(next_command,l.mid())['disposition']=='ACCEPTED'


def test_F08B3_02_typed_exception_only_proven_absence_can_report_not_committed(monkeypatch):
    l=Lab();l.admit();mid=l.mid();before=l.store.snapshot();proof_reads=[]
    inspect=l.store.inspect_mutation
    def no_commit(plan):
        l.store.hold(plan)
        raise ContractError('CAS_CONFLICT')
    def checked(operation):
        proof,objects=inspect(operation);proof_reads.append(proof.value['outcome'])
        return proof,objects
    monkeypatch.setattr(l.store,'commit',no_commit);monkeypatch.setattr(l.store,'inspect_mutation',checked)
    out=l.c.cancel(l.job_id,l.job().value['revision'],mid);expect_error(out,'CAS_CONFLICT')
    assert out['mutation_outcome']=='NOT_COMMITTED' and proof_reads and set(proof_reads)=={'NOT_COMMITTED'}
    assert not l.store.state['pending'] and not l.c._uncertain
    assert l.store.state['jobs']==before['jobs'] and l.store.state['slots']==before['slots']


def test_F08B3_02_failure_of_hold_port_does_not_clear_retained_uncertainty(monkeypatch):
    l=Lab();l.admit();mid=l.mid();commit=l.store.commit;hold=l.store.hold
    def interrupted(plan):
        commit(plan)  # FakeStore retains the operation until proof is acknowledged.
        raise ContractError('STORE_UNAVAILABLE')
    def unavailable_hold(plan):raise OSError('scripted hold-port outage')
    monkeypatch.setattr(l.store,'commit',interrupted);monkeypatch.setattr(l.store,'hold',unavailable_hold)
    out=l.c.cancel(l.job_id,l.job().value['revision'],mid)
    expect_error(out,'UNKNOWN_COMMIT_OUTCOME')
    assert mid in l.store.state['pending'] and mid in l.c._uncertain
    monkeypatch.setattr(l.store,'commit',commit);monkeypatch.setattr(l.store,'hold',hold)
    l.restart();expect_error(l.c.admit(l.variant(),l.mid()),'UNKNOWN_COMMIT_OUTCOME')
    assert l.c.resolve_commit(mid)['disposition']=='APPLIED'


def test_F08B3_02_pending_diagnostic_failure_cannot_enable_submit_or_stale_write(monkeypatch):
    l=Lab();l.submitting();before=l.store.snapshot();mid=l.mid();l.store.fault='after'
    out=l.c.cancel(l.job_id,l.job().value['revision'],mid,l.worker);expect_error(out,'UNKNOWN_COMMIT_OUTCOME')
    snapshot=l.store.snapshot
    def unreadable():raise RuntimeError('scripted snapshot outage')
    monkeypatch.setattr(l.store,'snapshot',unreadable)
    out=l.c.dispatch(l.job_id,0,l.worker);expect_error(out,'STORE_UNAVAILABLE')
    assert out['disposition']=='HOLD' and out['mutation_outcome']=='UNKNOWN_COMMIT_OUTCOME'
    assert out['error']['external_effect']=='UNKNOWN'
    monkeypatch.setattr(l.store,'snapshot',snapshot)
    pending=l.store.snapshot()
    expect_error(l.c.apply_proof(l.job_id,0,l.mid(),dict(l.worker,lease_epoch=999),l.command),'UNKNOWN_COMMIT_OUTCOME')
    assert l.store.snapshot()==pending and l.ledger.calls==0
    assert len(l.store.state['jobs'])==len(before['jobs']) and l.store.state['slots']
