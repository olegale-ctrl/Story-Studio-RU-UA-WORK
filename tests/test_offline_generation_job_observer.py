from experimental_mvp.offline_execution.observer import observe
from experimental_mvp.offline_execution import policy
from test_offline_generation_job_controller import Lab, expect_error


def test_single_shot_snapshot_is_authoritative_and_has_no_writes():
    l=Lab();l.admit();before=l.store.snapshot()
    s=observe(l.namespace,l.store,l.authority,l.job_id,l.clock,l.clock.epoch)
    assert s['job_ref']==l.store.state['jobs'][l.job_id] and s['cursor']==l.store.state['sequence']
    assert s['pipeline_complete'] is False and not s['barriers'] and l.store.snapshot()==before


def test_unknown_commit_visible_even_for_missing_job():
    l=Lab();l.store.fault='during';l.c.admit(l.command,l.mid())
    s=observe(l.namespace,l.store,l.authority,'missing')
    assert s['job_ref'] is None and s['barriers']==['UNKNOWN_COMMIT_OUTCOME']


def test_store_unavailable_and_corrupt_never_not_found():
    l=Lab();l.store.state['available']=False
    expect_error(observe(l.namespace,l.store,l.authority,'missing'),'STORE_UNAVAILABLE')
    l.store.state['available']=True;l.store.state['integrity']=False
    expect_error(observe(l.namespace,l.store,l.authority,'missing'),'STORE_CORRUPT')


def test_known_absence_requires_integral_read_scope():
    l=Lab();expect_error(observe(l.namespace,l.store,l.authority,'missing'),'NOT_FOUND')
    denied=policy.Authority(l.authority.permits,can_read=False)
    expect_error(observe(l.namespace,l.store,denied,'missing'),'READ_SCOPE_DENIED')


def test_qualified_clock_barrier_not_hidden():
    l=Lab();l.admit();l.clock.qualified=False
    s=observe(l.namespace,l.store,l.authority,l.job_id,l.clock,l.clock.epoch)
    assert s['barriers']==['CLOCK_UNQUALIFIED'] and not s['pipeline_complete']


def test_unreadable_pending_commit_is_not_downgraded_to_no_mutation():
    l=Lab();l.store.fault='during';l.c.admit(l.command,l.mid());l.store.state['available']=False
    out=observe(l.namespace,l.store,l.authority,'missing')
    expect_error(out,'STORE_UNAVAILABLE');assert out['mutation_outcome']=='UNKNOWN_COMMIT_OUTCOME'
    assert out['error']['external_effect']=='UNKNOWN'
