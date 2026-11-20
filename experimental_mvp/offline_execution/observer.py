"""Single-shot authoritative fake-store observation. No polling or wait API."""
from .contracts import ContractError, require, validate_shape, validate_record, response_error
from .controller import outcome


def observe(namespace, store, authority, job_id, clock=None, epoch=None):
    snapshot=None
    try:
        require(authority.can_read,'READ_SCOPE_DENIED')
        snapshot=store.snapshot()
        require(snapshot['namespace_ref']==namespace.ref,'NAMESPACE_MISMATCH')
        require(snapshot['available'],'STORE_UNAVAILABLE')
        require(snapshot['integrity'],'STORE_CORRUPT')
        barrier='UNKNOWN_COMMIT_OUTCOME' if snapshot['pending'] else None
        if not barrier and clock is not None:
            ce,tick,qualified=clock.instant()
            if not qualified or ce!=epoch:barrier='CLOCK_UNQUALIFIED'
        ref=snapshot['jobs'].get(job_id)
        require(barrier is not None or ref is not None,'NOT_FOUND')
        if ref:
            validate_record(snapshot['objects'][ref['digest']],snapshot['objects'])
        return validate_shape(dict(kind='PURE.ObserverSnapshot',version=1,scope='PURE_FAKE_ONLY',
                  namespace_ref=namespace.ref,job_ref=ref,cursor=snapshot['sequence'],
                  barriers=[barrier] if barrier else [],pipeline_complete=False))
    except ContractError as exc:
        return outcome('HOLD' if exc.code in ('STORE_UNAVAILABLE','STORE_CORRUPT','CLOCK_UNQUALIFIED') else 'REJECTED',
                       mutation='UNKNOWN_COMMIT_OUTCOME' if snapshot and snapshot['pending'] and exc.code in ('STORE_UNAVAILABLE','STORE_CORRUPT','CLOCK_UNQUALIFIED') else None,
                       error=response_error(exc.code,'OBSERVE','UNKNOWN','ZERO'))
