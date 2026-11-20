"""Effect containment and finite resource boundaries; never call a real provider."""
from pathlib import Path
import ast
import builtins
import io
import os
import socket
import sqlite3
import subprocess
import time
import pytest
from experimental_mvp.offline_execution import contracts, controller, policy, observer, simulator
from experimental_mvp.offline_execution.contracts import ContractError, Record, canonical_bytes, seal
from test_offline_generation_job_controller import Lab, uid, expect_error


def test_E18_guarded_happy_cancel_lost_ack_restart_and_failures(monkeypatch):
    # Import/test-loader I/O is outside the guarded execution region.
    l=Lab();other=Lab()
    hits=[]
    def forbidden(*args,**kwargs):
        hits.append('forbidden');raise AssertionError('Forbidden effect attempted')
    with monkeypatch.context() as m:
        for obj,names in [(builtins,['open']), (io,['open']), (os,['open','system','urandom']),
                          (socket,['socket','create_connection']), (sqlite3,['connect']),
                          (subprocess,['Popen','run','call','check_call','check_output']),
                          (time,['time','monotonic','sleep','perf_counter'])]:
            for name in names:m.setattr(obj,name,forbidden)
        l.result()
        other.submitting();other.ledger.lose_ack=True
        expect_error(other.c.dispatch(other.job_id,other.job().value['revision'],other.worker),'RESULT_BINDING_MISMATCH')
        other.restart(replace_owner=True)
        assert other.c.claim(other.job_id,other.job().value['revision'],other.mid(),uid(201),100)['disposition']=='APPLIED'
        other.worker=other.c.worker_token(other.job_id)
        other.c.cancel(other.job_id,other.job().value['revision'],other.mid(),other.worker)
    assert not hits


def test_import_surface_has_no_native_dependencies_or_dynamic_code():
    allowed={'dataclasses','hashlib','json','math','re','typing','contracts','controller','observer','simulator','policy'}
    for module in (contracts,controller,policy,observer,simulator):
        tree=ast.parse(Path(module.__file__).read_text())
        for node in ast.walk(tree):
            if isinstance(node,ast.Import):assert all(x.name.split('.')[0] in allowed for x in node.names)
            if isinstance(node,ast.ImportFrom):
                assert node.module in allowed or (node.module is None and node.level==1 and all(x.name in allowed for x in node.names))
            if isinstance(node,ast.Call) and isinstance(node.func,ast.Name):
                assert node.func.id not in ('eval','exec','compile','__import__','open')


def test_E19_maximum_jobs_bound_before_any_effect():
    l=Lab();l.admit()
    for i in range(1,16):
        out=l.c.admit(l.variant(i,project=True),l.mid());assert out['disposition']=='ACCEPTED',out
    before=l.store.commits
    expect_error(l.c.admit(l.variant(20,project=True),l.mid()),'RESOURCE_LIMIT')
    assert len(l.store.state['jobs'])==16 and l.store.commits==before and l.ledger.calls==0


def test_E19_event_limit_renew_and_no_silent_counter_reset():
    l=Lab();l.claimed()
    while sum(r.value['kind']=='PURE.StoreEvent' for r in l.store.state['objects'].values())<128:
        l.clock.tick+=1
        out=l.c.renew(l.job_id,l.job().value['revision'],l.mid(),l.worker,100)
        assert out['disposition']=='APPLIED',out
        l.worker=l.c.worker_token(l.job_id)
    before=l.store.snapshot();l.clock.tick+=1
    expect_error(l.c.renew(l.job_id,l.job().value['revision'],l.mid(),l.worker,100),'RESOURCE_LIMIT')
    assert l.store.snapshot()==before


def test_E19_one_worker_and_lease_horizon_bounds():
    l=Lab();l.claimed();other=l.variant(1,project=True)
    out=l.c.admit(other,l.mid());other_id=l.store.state['objects'][out['job_ref']['digest']].value['job_id']
    for target in ('AWAITING_APPROVAL','APPROVED','QUEUED'):
        job=l.store.state['objects'][l.store.state['jobs'][other_id]['digest']]
        assert l.c.advance(other_id,job.value['revision'],l.mid(),target)['disposition']=='APPLIED'
    job=l.store.state['objects'][l.store.state['jobs'][other_id]['digest']]
    expect_error(l.c.claim(other_id,job.value['revision'],l.mid(),uid(201),100),'RESOURCE_LIMIT')
    expect_error(l.c.renew(l.job_id,l.job().value['revision'],l.mid(),l.worker,10000),'RESOURCE_LIMIT')
    l.clock.tick=10001
    expect_error(l.c.renew(l.job_id,l.job().value['revision'],l.mid(),l.worker,100),'CLOCK_UNQUALIFIED')


def test_E19_wire_resource_bound_and_script_limit():
    with pytest.raises(ContractError) as error:canonical_bytes({'prompt':'x'*1048577})
    assert error.value.code=='RESOURCE_LIMIT'
    l=Lab();l.submitting();l.ledger.script_events=64
    expect_error(l.c.dispatch(l.job_id,l.job().value['revision'],l.worker),'RESOURCE_LIMIT')
    assert l.ledger.calls==0


def test_E17_errors_no_false_success_and_NO_wait_or_production_path():
    l=Lab();l.queued();before=l.store.snapshot()
    expect_error(l.c.advance(l.job_id,l.job().value['revision'],l.mid(),'COMPLETED'),'ILLEGAL_TRANSITION')
    assert l.store.snapshot()==before
    assert not hasattr(l.c,'wait') and not hasattr(l.simulator,'render') and not hasattr(l.c,'download')
    assert not any(hasattr(l.c,x) for x in ('save','import_asset','production'))


def test_P011_profile_mismatches_and_cost_quota_fail_before_effect():
    from test_offline_generation_job_contracts import record
    cp=record('CapabilityProfile').value
    for key in ('provider_id','model_id','model_version','region','mode','handler_id'):
        bad=dict(cp);bad[key]='I2V' if key=='mode' else 'unsupported'
        with pytest.raises(ContractError) as exc:policy.profile(bad)
        assert exc.value.code==('OPERATION_NOT_AVAILABLE' if key=='handler_id' else 'PROFILE_UNQUALIFIED')
    l=Lab();l.submitting();l.c.authority=policy.Authority(l.authority.permits,spend_minor=1)
    expect_error(l.c.dispatch(l.job_id,l.job().value['revision'],l.worker),'BUDGET_EXCEEDED')
    l.c.authority=policy.Authority(l.authority.permits,quota=0)
    expect_error(l.c.dispatch(l.job_id,l.job().value['revision'],l.worker),'QUOTA_EXHAUSTED')
    assert l.ledger.calls==0


def test_sequence_overflow_and_all_profile_limits_fail_closed():
    from test_offline_generation_job_contracts import record
    from experimental_mvp.offline_execution.contracts import MAX_INT
    l=Lab();l.store.state['sequence']=MAX_INT;before=l.store.snapshot()
    expect_error(l.c.admit(l.command,l.mid()),'SEQUENCE_EXHAUSTED')
    assert l.store.snapshot()==before and l.ledger.calls==0
    cp=record('CapabilityProfile').value
    for name,value in cp['limits'].items():
        bad=dict(cp);bad['limits']=dict(cp['limits'],**{name:value+1})
        with pytest.raises(ContractError) as exc:policy.profile(bad)
        assert exc.value.code=='PROFILE_UNQUALIFIED'
