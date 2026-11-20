"""Closed PURE_FAKE_ONLY values. No storage, clocks or provider access.

Pinned contract: 79feb212; owner task/erratum: cdadb11d. This is the local
space-separated JSON codec, deliberately not RFC 8785 JCS.
"""
from dataclasses import dataclass, field
import hashlib
import json
import math
import re

MAX_INT = 9223372036854775807
MAX_BYTES = 1048576
STATES = frozenset('DRAFT AWAITING_APPROVAL APPROVED QUEUED SUBMITTING SUBMISSION_UNCERTAIN RUNNING RESULT_AVAILABLE DOWNLOADING VALIDATING ASSET_COMMITTED ATTACH_PENDING COMPLETED PAUSED_QUOTA PAUSED_BUDGET PAUSED_RIGHTS STALE_TARGET RETRY_WAIT CANCEL_REQUESTED CANCELLED FAILED NEEDS_RECONCILIATION'.split())
TERMINAL = frozenset(('COMPLETED', 'CANCELLED', 'FAILED'))
LIMITS = dict(jobs=16, workers=1, batch_entries=1, attempts=1,
              total_reads_per_checkpoint=3, events=128, outbox=32,
              request_bytes=1048576, script_events=64, virtual_ticks=10000)
MESSAGES = {
    'FORMAT': 'Input format is invalid.',
    'VERSION_UNSUPPORTED': 'Record version is unsupported.',
    'PROFILE_UNQUALIFIED': 'Capability profile is not qualified.',
    'OPERATION_NOT_AVAILABLE': 'Operation is not available in this scope.',
    'NAMESPACE_MISMATCH': 'Namespace does not match.',
    'READ_SCOPE_DENIED': 'Read scope is not authorized.',
    'UNKNOWN_COMMIT_OUTCOME': 'Commit outcome is unknown.',
    'STORE_UNAVAILABLE': 'Store is unavailable.',
    'STORE_CORRUPT': 'Store integrity cannot be established.',
    'IDEMPOTENCY_CONFLICT': 'Idempotency key conflicts with content.',
    'OPERATION_ID_CONFLICT': 'Mutation identity conflicts with intent.',
    'AUTHORITY_MISSING': 'Required authority is missing.',
    'AUTHORIZATION_SCOPE_MISMATCH': 'Authorization scope does not match.',
    'AUTHORIZATION_EXPIRED': 'Authorization is expired.',
    'AUTHORIZATION_REVOKED': 'Authorization is revoked.',
    'ACTIVE_INTENT_CONFLICT': 'An active job already holds this purpose.',
    'CLOCK_UNQUALIFIED': 'Clock is not qualified.',
    'STALE_CONTROLLER_FENCE': 'Controller fence is stale.',
    'STALE_WORKER_FENCE': 'Worker fence is stale.',
    'LEASE_EXPIRED': 'Worker lease is expired.',
    'CAS_CONFLICT': 'Job revision has changed.',
    'ILLEGAL_TRANSITION': 'State transition is not allowed.',
    'BUDGET_EXCEEDED': 'Budget limit is exceeded.',
    'QUOTA_EXHAUSTED': 'Quota is exhausted.',
    'READ_LIMIT_EXCEEDED': 'Read checkpoint limit is exhausted.',
    'ATTEMPT_LIMIT': 'Generation attempt limit is exhausted.',
    'RESULT_BINDING_MISMATCH': 'Result binding does not match.',
    'NOT_FOUND': 'Requested job does not exist.',
    'CURSOR_MISMATCH': 'Provider cursor does not match.',
    'RESOURCE_LIMIT': 'Pure execution resource bound is exceeded.',
    'SEQUENCE_EXHAUSTED': 'Sequence range is exhausted.',
    'MUTATION_NOT_COMMITTED': 'Mutation was not committed.',
}
_FIX = frozenset('FORMAT VERSION_UNSUPPORTED PROFILE_UNQUALIFIED OPERATION_NOT_AVAILABLE IDEMPOTENCY_CONFLICT OPERATION_ID_CONFLICT AUTHORIZATION_SCOPE_MISMATCH RESULT_BINDING_MISMATCH CURSOR_MISMATCH'.split())
_AUTH = frozenset('AUTHORITY_MISSING AUTHORIZATION_EXPIRED AUTHORIZATION_REVOKED READ_SCOPE_DENIED BUDGET_EXCEEDED QUOTA_EXHAUSTED'.split())
_RELOAD = frozenset('ACTIVE_INTENT_CONFLICT CAS_CONFLICT STALE_CONTROLLER_FENCE STALE_WORKER_FENCE LEASE_EXPIRED NOT_FOUND'.split())
_RECONCILE = frozenset('UNKNOWN_COMMIT_OUTCOME STORE_UNAVAILABLE MUTATION_NOT_COMMITTED'.split())
ACTIONS = {c: ('FIX_INPUT' if c in _FIX else 'REAUTHORIZE' if c in _AUTH else
               'RELOAD' if c in _RELOAD else 'RECONCILE' if c in _RECONCILE else 'STOP')
           for c in MESSAGES}


class ContractError(ValueError):
    """Response-only failure; raising it never writes a JobError."""
    def __init__(self, code):
        if code not in MESSAGES:
            raise ValueError('Unknown public error code')
        self.code = code
        super().__init__(MESSAGES[code])


def require(ok, code='FORMAT'):
    if not ok:
        raise ContractError(code)


def response_error(code, operation, external_effect='NONE', billing='ZERO'):
    require(code in MESSAGES)
    value = dict(kind='PURE.ResponseError', version=1, scope='PURE_FAKE_ONLY',
                 code=code, operation=operation, safe_message=MESSAGES[code],
                 external_effect=external_effect, billing=billing,
                 required_action=ACTIONS[code])
    validate_shape(value)
    return value


def _json_value(v, depth=0, count=None):
    if count is None:
        count = [0]
    count[0] += 1
    require(depth <= 64 and count[0] <= MAX_BYTES, 'RESOURCE_LIMIT')
    if v is None or type(v) is bool:
        return
    if type(v) is int:
        require(0 <= v <= MAX_INT)
    elif type(v) is str:
        require(not any(0xD800 <= ord(c) <= 0xDFFF for c in v))
        require(len(v) <= 100000, 'RESOURCE_LIMIT')
    elif type(v) is list:
        require(len(v) <= MAX_BYTES, 'RESOURCE_LIMIT')
        for x in v:
            _json_value(x, depth + 1, count)
    elif type(v) is dict:
        require(all(type(k) is str for k in v))
        for k, x in v.items():
            _json_value(k, depth + 1, count)
            _json_value(x, depth + 1, count)
    else:
        raise ContractError('FORMAT')


def canonical_bytes(value):
    _json_value(value)
    b = json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False).encode('utf-8')
    require(len(b) <= MAX_BYTES, 'RESOURCE_LIMIT')
    return b


def digest(value):
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def decode(data):
    require(type(data) is bytes)
    require(len(data) <= MAX_BYTES, 'RESOURCE_LIMIT')
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result)
            result[key] = value
        return result
    try:
        value = json.loads(data.decode('utf-8'), object_pairs_hook=pairs)
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ContractError('FORMAT') from exc
    _json_value(value)
    return value


@dataclass(frozen=True)
class Record:
    """Immutable bytes; callers receive copies, never mutable internal state."""
    encoded: bytes
    _kind: str = field(init=False,repr=False)
    _digest: str = field(init=False,repr=False)

    def __post_init__(self):
        value = decode(self.encoded)
        validate_shape(value)
        require(value['kind'] in SCHEMAS)
        require(canonical_bytes(value) == self.encoded)
        object.__setattr__(self,'_kind',value['kind'])
        object.__setattr__(self,'_digest',hashlib.sha256(self.encoded).hexdigest())

    def __deepcopy__(self,memo):
        return self  # only immutable bytes/strings; no nested mutable state

    @property
    def value(self):
        return json.loads(self.encoded)  # bytes were checked once; return a detached copy

    @property
    def digest(self):
        return self._digest

    @property
    def ref(self):
        return {'kind': self._kind, 'digest': self.digest}


def seal(name, **fields):
    return Record(canonical_bytes(dict(kind='PURE.' + name, version=1,
                                       scope='PURE_FAKE_ONLY', **fields)))


# Field registry is transcribed from the pinned closed contract tables.
SCHEMAS = {'PURE.FixtureDescriptor': {'fixture_id': 'UUID',
                            'label': 'Text',
                            'content_class': '=SYNTHETIC_METADATA',
                            'producer_qualification': '=UNQUALIFIED_FAKE_ONLY'},
 'PURE.FixtureRegistry': {'registry_id': 'UUID', 'fixtures': 'List1..16<Ref<FixtureDescriptor>>'},
 'PURE.InputManifest': {'manifest_id': 'UUID', 'inputs': 'List1..16<InputItem>'},
 'PURE.CapabilityProfile': {'profile_id': 'UUID',
                            'handler_id': 'Text',
                            'provider_id': 'Text',
                            'model_id': 'Text',
                            'model_version': 'Text',
                            'region': 'Text',
                            'mode': 'T2V|I2V',
                            'registry_ref': 'Ref<FixtureRegistry>',
                            'limits': 'Limits'},
 'PURE.NamespaceBinding': {'store_id': 'UUID',
                           'ledger_id': 'UUID',
                           'root_scope_id': 'UUID',
                           'profile_ref': 'Ref<CapabilityProfile>'},
 'PURE.RequestIntent': {'identity_context': 'IdentityContext',
                        'target_snapshot': 'TargetSnapshot',
                        'request': 'GenerationSpec'},
 'PURE.BatchManifest': {'batch_id': 'UUID',
                        'batch_revision': 'Pos',
                        'entries': 'List1<BatchEntry>',
                        'policy': 'BatchPolicy'},
 'PURE.BatchPermit': {'permit_id': 'UUID',
                      'grant_revision': 'Pos',
                      'manifest_ref': 'Ref<BatchManifest>',
                      'namespace_ref': 'Ref<NamespaceBinding>',
                      'operation': '=SYNTHETIC_GENERATION',
                      'authority_mode': '=FAKE_ONLY',
                      'issuer_ref': '=TRUSTED_TEST_HARNESS',
                      'valid_from_tick': 'U',
                      'valid_until_tick': 'Pos',
                      'rights_context': '=UNVERIFIED_SYNTHETIC_METADATA'},
 'PURE.AdmissionKey': {'store_id': 'UUID',
                       'namespace_ref': 'Ref<NamespaceBinding>',
                       'project_id': 'UUID',
                       'purpose_id': 'UUID',
                       'request_ref': 'Ref<RequestIntent>',
                       'batch_id': 'UUID',
                       'batch_revision': 'Pos',
                       'batch_manifest_ref': 'Ref<BatchManifest>'},
 'PURE.AdmissionCommand': {'namespace_ref': 'Ref<NamespaceBinding>',
                           'key_ref': 'Ref<AdmissionKey>',
                           'request_ref': 'Ref<RequestIntent>',
                           'permit_ref': 'Ref<BatchPermit>'},
 'PURE.StoreMutationIntent': {'mutation_id': 'UUID',
                              'mutation_kind': 'ADMIT|CLAIM|RENEW|STATE_CHANGE|APPLY_PROOF|CANCEL|INCIDENT|READ_RESERVE',
                              'job_id': '?UUID',
                              'expected_revision': 'U',
                              'target_state': '?State',
                              'input_ref': '?Ref<HashKind>',
                              'cancel_requested': 'Bool'},
 'PURE.EffectPayload': {'namespace_ref': 'Ref<NamespaceBinding>',
                        'job_id': 'UUID',
                        'generation_operation_id': 'UUID',
                        'attempt_id': 'UUID',
                        'attempt_number': '=1',
                        'effect_token': 'UUID',
                        'key_ref': 'Ref<AdmissionKey>',
                        'request_ref': 'Ref<RequestIntent>',
                        'permit_ref': 'Ref<BatchPermit>',
                        'fixture_id': 'UUID',
                        'operation': '=SUBMIT_SYNTHETIC'},
 'PURE.StoreEvent': {'event_id': 'UUID',
                     'job_id': 'UUID',
                     'mutation_id': 'UUID',
                     'sequence': 'Pos',
                     'previous_event_ref': '?Ref<StoreEvent>',
                     'state_from': '?State',
                     'state_to': 'State',
                     'revision_from': 'U',
                     'revision_to': 'Pos',
                     'event_type': 'ADMITTED|LEASE_CLAIMED|LEASE_RENEWED|STATE_CHANGED|PROOF_APPLIED|CANCEL_REQUESTED|INCIDENT_RECORDED|READ_RESERVED',
                     'input_ref': '?Ref<HashKind>',
                     'effect_payload_ref': '?Ref<EffectPayload>',
                     'read_reservation': '?ReadReservation'},
 'PURE.AcceptanceReceipt': {'receipt_id': 'UUID',
                            'store_id': 'UUID',
                            'job_id': 'UUID',
                            'created_mutation_id': 'UUID',
                            'key_ref': 'Ref<AdmissionKey>',
                            'request_ref': 'Ref<RequestIntent>',
                            'initial_permit_ref': 'Ref<BatchPermit>',
                            'accepted_job_revision': '=1',
                            'accepted_store_sequence': 'Pos',
                            'acceptance_event_ref': 'Ref<StoreEvent>',
                            'commit_profile': '=FAKE_STORE_NOT_DURABILITY_PROOF'},
 'PURE.OutboxEnvelope': {'outbox_id': 'UUID',
                         'namespace_ref': 'Ref<NamespaceBinding>',
                         'generation_operation_id': 'UUID',
                         'attempt_id': 'UUID',
                         'effect_token': 'UUID',
                         'payload_ref': 'Ref<EffectPayload>',
                         'owner_event_ref': 'Ref<StoreEvent>'},
 'PURE.ProviderAcceptanceReceipt': {'provider_receipt_id': 'UUID',
                                    'namespace_ref': 'Ref<NamespaceBinding>',
                                    'ledger_id': 'UUID',
                                    'ledger_sequence': 'Pos',
                                    'provider_job_id': 'UUID',
                                    'generation_operation_id': 'UUID',
                                    'attempt_id': 'UUID',
                                    'effect_token': 'UUID',
                                    'payload_ref': 'Ref<EffectPayload>',
                                    'accepted_tick': 'U',
                                    'provider_cursor': 'Pos',
                                    'billed_minor': '=0',
                                    'producer_qualification': '=UNQUALIFIED_FAKE_ONLY'},
 'PURE.ProviderResultReceipt': {'result_id': 'UUID',
                                'acceptance_ref': 'Ref<ProviderAcceptanceReceipt>',
                                'generation_operation_id': 'UUID',
                                'attempt_id': 'UUID',
                                'effect_token': 'UUID',
                                'provider_job_id': 'UUID',
                                'resolved_profile_ref': 'Ref<CapabilityProfile>',
                                'fixture_ref': 'Ref<FixtureDescriptor>',
                                'provider_cursor': 'Pos',
                                'ready_tick': 'U',
                                'producer_qualification': '=UNQUALIFIED_FAKE_ONLY'},
 'PURE.ProviderNonAcceptanceProof': {'namespace_ref': 'Ref<NamespaceBinding>',
                                     'generation_operation_id': 'UUID',
                                     'attempt_id': 'UUID',
                                     'effect_token': 'UUID',
                                     'payload_ref': 'Ref<EffectPayload>',
                                     'ledger_sequence': 'U',
                                     'observed_tick': 'U',
                                     'outcome': '=NOT_ACCEPTED',
                                     'billed_minor': '=0',
                                     'producer_qualification': '=UNQUALIFIED_FAKE_ONLY'},
 'PURE.CancellationSettlementProof': {'namespace_ref': 'Ref<NamespaceBinding>',
                                      'generation_operation_id': 'UUID',
                                      'attempt_id': 'UUID',
                                      'effect_token': 'UUID',
                                      'settlement': 'NO_EFFECT|CANCELLED',
                                      'provider_job_id': '?UUID',
                                      'external_effect': 'NONE|KNOWN',
                                      'billed_minor': '=0',
                                      'settled_tick': 'U',
                                      'producer_qualification': '=UNQUALIFIED_FAKE_ONLY'},
 'PURE.JobError': {'error_id': 'UUID',
                   'domain': '=PURE_LOCAL',
                   'code': 'ErrorCode',
                   'occurred_at': '?FakeInstant',
                   'state': '?State',
                   'attempt': '?UUID',
                   'operation': 'ErrorOperation',
                   'retry_class': 'NONE|SAFE_READ|SAFE_LOCAL|RECONCILE_ONLY',
                   'safe_message': 'MessageForCode',
                   'provider_status': '?ProviderStatus',
                   'trace_redacted': '=null',
                   'external_effect': 'NONE|KNOWN|UNKNOWN',
                   'billing': 'ZERO|SETTLED|RESERVED|UNKNOWN',
                   'evidence_ref': '?Ref<HashKind>',
                   'required_action': 'ErrorAction'},
 'PURE.ActiveSlot': {'store_id': 'UUID',
                     'project_id': 'UUID',
                     'purpose_id': 'UUID',
                     'job_id': 'UUID',
                     'key_ref': 'Ref<AdmissionKey>',
                     'status': 'HELD|RELEASED',
                     'occupied_since_revision': 'Pos',
                     'released_at_revision': '?Pos'},
 'PURE.JobRecord': {'job_id': 'UUID',
                    'created_mutation_id': 'UUID',
                    'last_mutation_id': 'UUID',
                    'namespace_ref': 'Ref<NamespaceBinding>',
                    'key_ref': 'Ref<AdmissionKey>',
                    'request_ref': 'Ref<RequestIntent>',
                    'initial_permit_ref': 'Ref<BatchPermit>',
                    'state': 'State',
                    'revision': 'Pos',
                    'cancel_requested': 'Bool',
                    'generation_operation_id': '?UUID',
                    'attempt_id': '?UUID',
                    'effect_token': '?UUID',
                    'last_event_ref': 'Ref<StoreEvent>',
                    'last_error_ref': '?Ref<JobError>',
                    'result_ref': '?Ref<ProviderResultReceipt>',
                    'active_slot_ref': 'Ref<ActiveSlot>',
                    'controller_incarnation': 'U',
                    'worker_id': '?UUID',
                    'lease_epoch': 'U',
                    'lease_until_tick': '?U',
                    'clock_epoch_id': '?UUID',
                    'provider_cursor': 'U',
                    'read_checkpoint': '?ReadCheckpoint'},
 'PURE.AtomicWriteSet': {'mutation_ref': 'Ref<StoreMutationIntent>',
                         'job_id': 'UUID',
                         'base_revision': 'U',
                         'result_revision': 'Pos',
                         'members': 'List1..8<Ref<HashKind>>',
                         'active_slot_action': 'ACQUIRE|RETAIN|RELEASE',
                         'store_sequence': 'Pos'},
 'PURE.MutationAbsenceProof': {'namespace_ref': 'Ref<NamespaceBinding>',
                               'mutation_ref': 'Ref<StoreMutationIntent>',
                               'snapshot_generation': 'U',
                               'lookup_complete': '=true',
                               'marker_present': '=false',
                               'members_for_mutation_present': '=false',
                               'qualification': '=FAKE_STORE_READ_ONLY_EVIDENCE'},
 'PURE.CommitResolutionProof': {'namespace_ref': 'Ref<NamespaceBinding>',
                                'mutation_ref': 'Ref<StoreMutationIntent>',
                                'outcome': 'COMMITTED|NOT_COMMITTED',
                                'write_set_ref': '?Ref<AtomicWriteSet>',
                                'absence_ref': '?Ref<MutationAbsenceProof>',
                                'snapshot_generation': 'U',
                                'qualification': '=FAKE_STORE_READ_ONLY_EVIDENCE'}}

INLINE = {
 'InputItem': dict(role='PROMPT|PROJECT|REFERENCE', object_id='UUID', revision='Pos', locator='Opaque', raw_sha256='Digest', byte_length='U'),
 'IdentityContext': {k: 'UUID' for k in ('project_id','scene_id','anchor_id','purpose_id')},
 'TargetSnapshot': dict(project_locator_ref='Opaque', **{k:'Digest' for k in ('expected_saved_json_sha256','expected_editor_snapshot_sha256','expected_anchor_token','generation_fingerprint','input_manifest_sha256')}),
 'Resolution': dict(width='Pos',height='Pos'), 'Ratio': dict(num='Pos',den='Pos'),
 'ProviderParameters': dict(fixture_id='UUID'),
 'GenerationSpec': dict(provider_id='Text',model_id='Text',model_version='Text',region='Text',mode='T2V|I2V',prompt_reference='Opaque',prompt_sha256='Digest',duration_ms='Pos',resolution='Resolution',aspect_ratio='Ratio',input_assets='List0',provider_parameters='ProviderParameters',capability_profile_ref='UUID',capability_profile_hash='Digest'),
 'BatchEntry': dict(project_id='UUID',purpose_id='UUID',request_ref='Ref<RequestIntent>'),
 'BatchPolicy': dict(max_jobs='=1',max_attempts='=1',currency='=USD',max_job_spend_minor='=0',max_batch_spend_minor='=0',retention='=KEEP_TEST_METADATA'),
 'Limits': {k:'='+str(v) for k,v in LIMITS.items()},
 'FakeInstant': dict(clock_epoch_id='UUID',tick='U'),
 'ReadReservation': dict(checkpoint_id='UUID',read_kind='LOOKUP|POLL',call_index='1..3',base_cursor='U'),
 'ReadCheckpoint': dict(checkpoint_id='UUID',read_kind='LOOKUP|POLL',base_cursor='U',calls_used='0..3',max_calls='=3'),
 'ControllerToken': dict(store_id='UUID',controller_id='UUID',incarnation='Pos',clock_epoch_id='UUID'),
 'WorkerToken': dict(controller='ControllerToken',job_id='UUID',worker_id='UUID',lease_epoch='Pos',lease_until_tick='U'),
 'ResponseFields': dict(code='ErrorCode',operation='ErrorOperation',safe_message='MessageForCode',external_effect='NONE|KNOWN|UNKNOWN',billing='ZERO|SETTLED|RESERVED|UNKNOWN',required_action='ErrorAction'),
}
BOUNDARIES = {
 'PURE.ControllerFence': INLINE['ControllerToken'], 'PURE.WorkerFence': INLINE['WorkerToken'],
 'PURE.DeliveryCommand': dict(outbox_ref='Ref<OutboxEnvelope>',payload_ref='Ref<EffectPayload>',fence='WorkerToken',expected_revision='Pos'),
 'PURE.ReadRequest': dict(payload_ref='Ref<EffectPayload>',effect_token='UUID',checkpoint_id='UUID',read_kind='LOOKUP|POLL',cursor='U',reserved_call_index='1..3',fence='WorkerToken',expected_revision='Pos'),
 'PURE.ResponseError': INLINE['ResponseFields'],
 'PURE.APIOutcome': dict(disposition='ACCEPTED|REUSED|APPLIED|REJECTED|HOLD|OBSERVED',mutation_outcome='?COMMITTED|NOT_COMMITTED|UNKNOWN_COMMIT_OUTCOME',receipt_ref='?Ref<AcceptanceReceipt>',job_ref='?Ref<JobRecord>',error='?ResponseFields'),
 'PURE.ObserverSnapshot': dict(namespace_ref='Ref<NamespaceBinding>',job_ref='?Ref<JobRecord>',cursor='U',barriers='List0..1<Barrier>',pipeline_complete='=false'),
}
ENUMS = {'State': STATES, 'ErrorCode': MESSAGES,
 'ErrorAction': ('FIX_INPUT','REAUTHORIZE','RELOAD','RECONCILE','STOP'),
 'ErrorOperation': 'ADMIT OBSERVE CLAIM RENEW SUBMIT LOOKUP POLL APPLY_PROOF CANCEL RESOLVE_COMMIT INCIDENT'.split(),
 'ProviderStatus': 'ACCEPTED RUNNING RESULT_AVAILABLE NOT_ACCEPTED CANCELLED FAILED UNKNOWN'.split(),
 'Barrier': ('UNKNOWN_COMMIT_OUTCOME','STORE_UNAVAILABLE','STORE_CORRUPT','CLOCK_UNQUALIFIED')}


def _closed(v, fields):
    require(type(v) is dict and set(v) == set(fields))
    for key, typ in fields.items():
        _type(v[key], typ)


def _type(v, typ):
    if typ.startswith('?'):
        if v is None:
            return
        return _type(v, typ[1:])
    if typ.startswith('='):
        token = typ[1:]
        lit = {'null': None, 'true': True, 'false': False}.get(token, token)
        if token.isdecimal():
            lit = int(token)
        require(type(v) is type(lit) and v == lit)
    elif typ in INLINE:
        _closed(v, INLINE[typ])
    elif typ in ENUMS:
        require(type(v) is str and v in ENUMS[typ])
    elif typ.startswith('Ref<'):
        require(type(v) is dict and set(v) == {'kind','digest'})
        _type(v['digest'], 'Digest')
        target = typ[4:-1]
        require(v['kind'] in SCHEMAS and (target == 'HashKind' or v['kind'] == 'PURE.'+target))
    elif typ.startswith('List'):
        m = re.fullmatch(r'List(\d+)(?:\.\.(\d+))?(?:<(.*)>)?',typ)
        require(m is not None)
        lo, hi, item = m.groups(); lo=int(lo); hi=int(hi) if hi else lo
        require(type(v) is list and lo <= len(v) <= hi)
        if item:
            for x in v:
                _type(x,item)
    elif typ in ('Text','Opaque','MessageForCode'):
        require(type(v) is str and 1 <= len(v) <= 100000)
    elif typ == 'UUID':
        require(type(v) is str and re.fullmatch(r'[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}',v) is not None)
    elif typ == 'Digest':
        require(type(v) is str and re.fullmatch(r'[0-9a-f]{64}',v) is not None)
    elif typ in ('U','Pos'):
        require(type(v) is int and (1 if typ=='Pos' else 0) <= v <= MAX_INT)
    elif typ == 'Bool':
        require(type(v) is bool)
    elif re.fullmatch(r'\d+\.\.\d+',typ):
        a,b=map(int,typ.split('..')); require(type(v) is int and a<=v<=b)
    elif '|' in typ:
        require(type(v) is str and v in typ.split('|'))
    else:
        raise AssertionError('Unregistered contract type: '+typ)


def validate_shape(value):
    _json_value(value)
    require(type(value) is dict)
    require('kind' in value and 'version' in value and 'scope' in value)
    require(type(value['version']) is int)
    require(type(value['kind']) is str)
    fields = SCHEMAS.get(value['kind'], BOUNDARIES.get(value['kind']))
    if fields is not None:
        _closed(value, dict(kind='='+value['kind'],version='U',scope='Text',**fields))
    require(value['version'] == 1, 'VERSION_UNSUPPORTED')
    require(value['scope']=='PURE_FAKE_ONLY', 'PROFILE_UNQUALIFIED')
    require(fields is not None,'OPERATION_NOT_AVAILABLE')
    k=value['kind'].removeprefix('PURE.')
    if k=='InputManifest':
        keys=[(x['role'],x['object_id']) for x in value['inputs']]
        require(keys == sorted(set(keys)))
    elif k=='RequestIntent':
        q=value['request']; res=q['resolution']; rat=q['aspect_ratio']
        require(q['duration_ms']<=120000 and all(2<=res[n]<=8192 and res[n]%2==0 for n in ('width','height')))
        require(math.gcd(rat['num'],rat['den'])==1 and res['width']*rat['den']==res['height']*rat['num'])
    elif k=='BatchPermit':
        require(value['valid_from_tick']<value['valid_until_tick'])
    elif k=='ActiveSlot':
        require((value['status']=='HELD') == (value['released_at_revision'] is None))
        if value['released_at_revision'] is not None:
            require(value['released_at_revision']>=value['occupied_since_revision'])
    elif k=='StoreMutationIntent':
        m=value['mutation_kind']; i=value['input_ref']
        if m=='ADMIT':
            require(value['job_id'] is None and value['expected_revision']==0 and value['target_state']=='DRAFT' and not value['cancel_requested'])
            require(i is not None and i['kind']=='PURE.AdmissionCommand')
        else:
            require(value['job_id'] is not None and value['expected_revision']>=1)
            if m in ('CLAIM','RENEW','READ_RESERVE'):
                require(value['target_state'] is None and i is None)
            elif m=='APPLY_PROOF':
                require(i is not None and i['kind'] in ('PURE.ProviderAcceptanceReceipt','PURE.ProviderResultReceipt','PURE.ProviderNonAcceptanceProof','PURE.CancellationSettlementProof'))
            elif m=='INCIDENT':
                require(i is not None and i['kind']=='PURE.JobError')
            elif m=='CANCEL':
                require(value['cancel_requested'] and value['target_state'] in ('CANCEL_REQUESTED','CANCELLED'))
    elif k=='StoreEvent':
        require(value['revision_to']==value['revision_from']+1)
        require((value['event_type']=='READ_RESERVED') == (value['read_reservation'] is not None))
        if value['event_type']=='ADMITTED':
            require(value['sequence']==1 and value['previous_event_ref'] is None and value['state_from'] is None and value['state_to']=='DRAFT' and value['revision_from']==0)
        else:
            require(value['previous_event_ref'] is not None and value['state_from'] is not None)
    elif k=='CancellationSettlementProof':
        require((value['settlement']=='NO_EFFECT' and value['provider_job_id'] is None and value['external_effect']=='NONE') or (value['settlement']=='CANCELLED' and value['provider_job_id'] is not None and value['external_effect']=='KNOWN'))
    elif k in ('JobError','ResponseError'):
        require(value['safe_message']==MESSAGES[value['code']] and value['required_action']==ACTIONS[value['code']])
        if k=='JobError':
            require(value['state'] is not None)
            require(value['occurred_at'] is not None or value['code']=='CLOCK_UNQUALIFIED')
            expected='RECONCILE_ONLY' if value['code'] in ('UNKNOWN_COMMIT_OUTCOME','STORE_UNAVAILABLE','STORE_CORRUPT') else 'SAFE_LOCAL' if value['code']=='MUTATION_NOT_COMMITTED' else 'NONE'
            require(value['retry_class']==expected)
    elif k=='JobRecord':
        present=[value[n] is not None for n in ('generation_operation_id','attempt_id','effect_token')]
        require(all(present) or not any(present))
        leased=[value[n] is not None for n in ('worker_id','lease_until_tick','clock_epoch_id')]
        require(all(leased) or not any(leased))
        require(not all(leased) or value['lease_epoch']>=1)
    elif k=='AtomicWriteSet':
        keys=[(x['kind'],x['digest']) for x in value['members']]
        require(keys==sorted(set(keys)))
        require(value['result_revision']==value['base_revision']+1)
    elif k=='CommitResolutionProof':
        require((value['outcome']=='COMMITTED' and value['write_set_ref'] is not None and value['absence_ref'] is None) or (value['outcome']=='NOT_COMMITTED' and value['write_set_ref'] is None and value['absence_ref'] is not None))
    elif k=='APIOutcome':
        dis=value['disposition']; outcome=value['mutation_outcome']
        if value['error'] is not None:
            err=value['error']; require(err['safe_message']==MESSAGES[err['code']] and err['required_action']==ACTIONS[err['code']])
        if dis=='ACCEPTED': require(outcome=='COMMITTED' and value['receipt_ref'] is not None and value['error'] is None)
        elif dis=='REUSED': require(outcome is None and value['receipt_ref'] is not None and value['error'] is None)
        elif dis=='APPLIED': require(outcome=='COMMITTED' and value['error'] is None)
        elif dis=='REJECTED': require(outcome in (None,'NOT_COMMITTED') and value['error'] is not None)
        elif dis=='HOLD': require(value['error'] is not None)
        elif dis=='OBSERVED': require(outcome is None and value['error'] is None)
        if outcome=='UNKNOWN_COMMIT_OUTCOME':require(dis=='HOLD')
    return value


def walk_refs(value):
    if type(value) is dict:
        if set(value)=={'kind','digest'}:
            yield value
        else:
            for v in value.values(): yield from walk_refs(v)
    elif type(value) is list:
        for v in value: yield from walk_refs(v)


def resolve(ref, objects):
    _type(ref,'Ref<HashKind>')
    require(ref['digest'] in objects, 'STORE_CORRUPT')
    record=objects[ref['digest']]
    require(type(record) is Record and record.digest==ref['digest'] and record.ref==ref,'STORE_CORRUPT')
    return record.value


def validate_record(record, objects):
    """Validate bounded transitive closure and typed associations, without I/O."""
    require(type(record) is Record)
    visiting=set(); done=set()
    def visit(rec):
        require(rec.digest not in visiting,'STORE_CORRUPT')
        if rec.digest in done:return
        require(len(visiting)+len(done)<4096,'RESOURCE_LIMIT')
        visiting.add(rec.digest)
        refs=list(walk_refs(rec.value))
        if rec.value['kind']=='PURE.RequestIntent':
            refs.extend([{'kind':'PURE.CapabilityProfile','digest':rec.value['request']['capability_profile_hash']},{'kind':'PURE.InputManifest','digest':rec.value['target_snapshot']['input_manifest_sha256']}])
        for ref in refs:
            resolve(ref,objects)
            visit(objects[ref['digest']])
        _associations(rec.value,objects)
        visiting.remove(rec.digest);done.add(rec.digest)
    visit(record)
    return record


def _associations(v,objects):
    get=lambda key:resolve(v[key],objects)
    k=v['kind'].removeprefix('PURE.')
    if k=='FixtureRegistry':
        ids=[resolve(x,objects)['fixture_id'] for x in v['fixtures']]
        require(ids==sorted(set(ids)))
    elif k=='RequestIntent':
        q=v['request']; cp=resolve({'kind':'PURE.CapabilityProfile','digest':q['capability_profile_hash']},objects)
        require(q['capability_profile_ref']==cp['profile_id'],'RESULT_BINDING_MISMATCH')
        resolve({'kind':'PURE.InputManifest','digest':v['target_snapshot']['input_manifest_sha256']},objects)
        for n in ('provider_id','model_id','model_version','region','mode'):
            require(q[n]==cp[n],'PROFILE_UNQUALIFIED')
        registry=resolve(cp['registry_ref'],objects)
        require(q['provider_parameters']['fixture_id'] in [resolve(x,objects)['fixture_id'] for x in registry['fixtures']],'RESULT_BINDING_MISMATCH')
    elif k=='BatchManifest':
        for x in v['entries']:
            req=resolve(x['request_ref'],objects)['identity_context']
            require(all(req[n]==x[n] for n in ('project_id','purpose_id')),'RESULT_BINDING_MISMATCH')
    elif k=='AdmissionKey':
        ns=get('namespace_ref');req=get('request_ref');manifest=get('batch_manifest_ref')
        require(v['store_id']==ns['store_id'] and v['batch_id']==manifest['batch_id'] and v['batch_revision']==manifest['batch_revision'],'IDEMPOTENCY_CONFLICT')
        require(all(v[n]==req['identity_context'][n] for n in ('project_id','purpose_id')),'IDEMPOTENCY_CONFLICT')
        require(manifest['entries'][0]=={n:v[n] for n in ('project_id','purpose_id','request_ref')},'IDEMPOTENCY_CONFLICT')
    elif k=='EffectPayload':
        key=get('key_ref');req=get('request_ref');permit=get('permit_ref')
        require(key['namespace_ref']==v['namespace_ref'] and key['request_ref']==v['request_ref'],'RESULT_BINDING_MISMATCH')
        require(permit['manifest_ref']==key['batch_manifest_ref'] and permit['namespace_ref']==v['namespace_ref'],'AUTHORIZATION_SCOPE_MISMATCH')
        require(req['request']['provider_parameters']['fixture_id']==v['fixture_id'],'RESULT_BINDING_MISMATCH')
    elif k=='ActiveSlot':
        key=get('key_ref')
        require(all(v[n]==key[n] for n in ('store_id','project_id','purpose_id')),'STORE_CORRUPT')
    elif k=='StoreEvent' and v['previous_event_ref'] is not None:
        prev=get('previous_event_ref')
        require(prev['job_id']==v['job_id'] and prev['sequence']+1==v['sequence'] and prev['revision_to']==v['revision_from'] and prev['state_to']==v['state_from'],'STORE_CORRUPT')
    elif k=='AcceptanceReceipt':
        ev=get('acceptance_event_ref')
        require(ev['event_type']=='ADMITTED' and ev['job_id']==v['job_id'] and ev['mutation_id']==v['created_mutation_id'],'STORE_CORRUPT')
    elif k=='OutboxEnvelope':
        payload=get('payload_ref');ev=get('owner_event_ref')
        require(ev['effect_payload_ref']==v['payload_ref'] and ev['state_to']=='SUBMITTING','STORE_CORRUPT')
        require(all(v[n]==payload[n] for n in ('namespace_ref','generation_operation_id','attempt_id','effect_token')),'RESULT_BINDING_MISMATCH')
    elif k in ('ProviderAcceptanceReceipt','ProviderNonAcceptanceProof'):
        payload=get('payload_ref');ns=get('namespace_ref')
        require(all(v[n]==payload[n] for n in ('namespace_ref','generation_operation_id','attempt_id','effect_token')),'RESULT_BINDING_MISMATCH')
        if k=='ProviderAcceptanceReceipt':require(ns['ledger_id']==v['ledger_id'],'RESULT_BINDING_MISMATCH')
    elif k=='ProviderResultReceipt':
        a=get('acceptance_ref');payload=resolve(a['payload_ref'],objects);req=resolve(payload['request_ref'],objects)['request'];fixture=get('fixture_ref')
        require(all(v[n]==a[n] for n in ('generation_operation_id','attempt_id','effect_token','provider_job_id')),'RESULT_BINDING_MISMATCH')
        require(v['provider_cursor']>=a['provider_cursor'] and v['ready_tick']>=a['accepted_tick'],'CURSOR_MISMATCH')
        require(v['resolved_profile_ref']['digest']==req['capability_profile_hash'] and fixture['fixture_id']==payload['fixture_id'],'RESULT_BINDING_MISMATCH')
    elif k=='JobRecord':
        event=get('last_event_ref');slot=get('active_slot_ref')
        require(event['job_id']==v['job_id'] and event['revision_to']==v['revision'] and event['state_to']==v['state'] and event['mutation_id']==v['last_mutation_id'],'STORE_CORRUPT')
        require(slot['job_id']==v['job_id'] and slot['key_ref']==v['key_ref'],'STORE_CORRUPT')
        require((v['state'] in TERMINAL)==(slot['status']=='RELEASED'),'STORE_CORRUPT')
        if slot['status']=='RELEASED':require(slot['released_at_revision']==v['revision'],'STORE_CORRUPT')
        key=get('key_ref');permit=get('initial_permit_ref')
        require(key['namespace_ref']==v['namespace_ref'] and key['request_ref']==v['request_ref'] and permit['manifest_ref']==key['batch_manifest_ref'],'STORE_CORRUPT')
    elif k=='AtomicWriteSet':
        m=get('mutation_ref'); members=[resolve(x,objects) for x in v['members']]
        counts={n:sum(x['kind']=='PURE.'+n for x in members) for n in ('StoreEvent','JobRecord','AcceptanceReceipt','ActiveSlot','OutboxEnvelope','JobError')}
        require(counts['StoreEvent']==counts['JobRecord']==1 and sum(counts.values())==len(members),'STORE_CORRUPT')
        event=next(x for x in members if x['kind']=='PURE.StoreEvent');job=next(x for x in members if x['kind']=='PURE.JobRecord')
        require(v['base_revision']==m['expected_revision']==event['revision_from'] and v['result_revision']==event['revision_to']==job['revision'],'STORE_CORRUPT')
        require(event['mutation_id']==m['mutation_id']==job['last_mutation_id'] and v['job_id']==event['job_id']==job['job_id'],'STORE_CORRUPT')
        require(event['input_ref']==m['input_ref'] and job['cancel_requested']==m['cancel_requested'],'STORE_CORRUPT')
        if m['target_state'] is not None:require(event['state_to']==m['target_state'],'STORE_CORRUPT')
        if m['mutation_kind']=='ADMIT':
            require(len(members)==4 and counts['AcceptanceReceipt']==counts['ActiveSlot']==1 and v['active_slot_action']=='ACQUIRE','STORE_CORRUPT')
            receipt=next(x for x in members if x['kind']=='PURE.AcceptanceReceipt')
            require(receipt['accepted_store_sequence']==v['store_sequence'] and all(receipt[n]==job[n] for n in ('job_id','key_ref','request_ref','initial_permit_ref')),'STORE_CORRUPT')
        else:
            require(m['job_id']==v['job_id'] and counts['AcceptanceReceipt']==0,'STORE_CORRUPT')
            require(counts['JobError']==(1 if m['mutation_kind']=='INCIDENT' else 0),'STORE_CORRUPT')
            require(counts['OutboxEnvelope']==(1 if event['state_to']=='SUBMITTING' and event['state_from']=='QUEUED' else 0),'STORE_CORRUPT')
            require(counts['ActiveSlot']==(1 if v['active_slot_action']=='RELEASE' else 0),'STORE_CORRUPT')
    elif k=='CommitResolutionProof':
        proof=get('write_set_ref') if v['outcome']=='COMMITTED' else get('absence_ref')
        require(proof['mutation_ref']==v['mutation_ref'],'STORE_CORRUPT')
        if v['outcome']=='NOT_COMMITTED':require(proof['snapshot_generation']==v['snapshot_generation'],'STORE_CORRUPT')
