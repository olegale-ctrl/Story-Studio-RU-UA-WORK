"""Pure fake authority/ownership ports; no native capability implementations."""
from dataclasses import dataclass
from typing import Protocol
from .contracts import ContractError, LIMITS, MAX_INT, require, resolve, validate_shape

PROFILE = dict(handler_id='synthetic.video_anchor',provider_id='OFFLINE_SIMULATOR_V1',
               model_id='SIM_WAN_PROFILE_V1',model_version='1',region='LOCAL_ONLY',mode='T2V')
CLAIM_STATES = frozenset('QUEUED SUBMITTING SUBMISSION_UNCERTAIN RUNNING RETRY_WAIT NEEDS_RECONCILIATION CANCEL_REQUESTED'.split())


class ClockPort(Protocol):
    def instant(self) -> tuple: ...


class OwnershipPort(Protocol):
    def current(self) -> dict: ...
    def worker_dead(self, worker_id: str) -> bool: ...


class StorePort(Protocol):
    def snapshot(self): ...
    def commit(self, plan): ...
    def hold(self, plan): ...
    def inspect_mutation(self, mutation_id): ...
    def acknowledge_resolution(self, mutation_id, proof): ...


@dataclass(frozen=True)
class Authority:
    """Injected test-harness trust list, not a self-asserted issuer string."""
    permits: frozenset
    revoked: frozenset = frozenset()
    can_read: bool = True
    quota: int = 1
    spend_minor: int = 0


def profile(cp):
    require(cp['handler_id']==PROFILE['handler_id'],'OPERATION_NOT_AVAILABLE')
    require(all(cp[n]==v for n,v in PROFILE.items()),'PROFILE_UNQUALIFIED')
    require(cp['limits']==LIMITS,'PROFILE_UNQUALIFIED')


def instant(clock, expected_epoch, minimum=0):
    epoch,tick,qualified=clock.instant()
    require(qualified and epoch==expected_epoch and type(tick) is int and minimum<=tick<=10000,'CLOCK_UNQUALIFIED')
    return tick


def controller_fence(token, ownership, store_id, epoch):
    validate_shape(dict(kind='PURE.ControllerFence',version=1,scope='PURE_FAKE_ONLY',**token))
    current=ownership.current()
    require(current is not None and current==token and token['store_id']==store_id and token['clock_epoch_id']==epoch,'STALE_CONTROLLER_FENCE')


def worker_fence(token, job, controller, tick):
    require(type(token) is dict,'STALE_WORKER_FENCE')
    validate_shape(dict(kind='PURE.WorkerFence',version=1,scope='PURE_FAKE_ONLY',**token))
    require(token['controller']==controller and token['job_id']==job['job_id'] and token['worker_id']==job['worker_id'] and token['lease_epoch']==job['lease_epoch'] and token['lease_until_tick']==job['lease_until_tick'] and job['controller_incarnation']==controller['incarnation'],'STALE_WORKER_FENCE')
    require(tick<job['lease_until_tick'],'LEASE_EXPIRED')


def authorize(permit_ref, manifest_ref, namespace_ref, authority, objects, tick):
    require(permit_ref is not None and permit_ref['digest'] in authority.permits,'AUTHORITY_MISSING')
    permit=resolve(permit_ref,objects)
    require(permit['manifest_ref']==manifest_ref and permit['namespace_ref']==namespace_ref,'AUTHORIZATION_SCOPE_MISMATCH')
    require(permit_ref['digest'] not in authority.revoked,'AUTHORIZATION_REVOKED')
    require(permit['valid_from_tick']<=tick<permit['valid_until_tick'],'AUTHORIZATION_EXPIRED')


def capacity(authority):
    require(authority.spend_minor==0,'BUDGET_EXCEEDED')
    require(type(authority.quota) is int and authority.quota>=1,'QUOTA_EXHAUSTED')


def increment(value):
    require(value<MAX_INT,'SEQUENCE_EXHAUSTED')
    return value+1
