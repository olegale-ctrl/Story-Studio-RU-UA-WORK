"""Synthetic, single-writer, in-memory S1 transaction/recovery model.

No OS identity, real persistence, clock, randomness, or production authority.
All commands, images, policy/package fixtures and keys are explicit inputs.
Visible writes and independently flushed virtual durable fields are distinct.
"""
from copy import deepcopy
from dataclasses import dataclass, field

from . import storage_protocol_v1 as wire


class ModelError(wire.ProtocolError):
    pass


def fail(code, path, reason):
    raise ModelError(code, path, reason)


class SimulatedCrash(RuntimeError):
    """Interruption at an observed virtual operation, not a durability claim."""


class VirtualIOError(RuntimeError):
    def __init__(self, code):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True)
class Fault:
    operation: str
    when: str
    occurrence: int = 1
    effect: str = 'crash'

    def __post_init__(self):
        if self.when not in ('before', 'after') or self.effect not in ('crash', 'disk_full', 'flush_failed') or self.occurrence < 1:
            raise ValueError('Invalid synthetic fault')


@dataclass
class VirtualState:
    primary: bytes | None = None
    journal: list = field(default_factory=list)
    anchor: bytes | None = None
    registration: bytes | None = None
    blobs: dict = field(default_factory=dict)
    images: dict = field(default_factory=dict)
    backups: dict = field(default_factory=dict)
    forensic: dict = field(default_factory=dict)
    authorization_evidence: set = field(default_factory=set)
    # Retained, immutable synthetic epoch containers, not a new protocol wire type.
    parents: dict = field(default_factory=dict)


class VirtualStore:
    """Explicit synthetic write/flush model. Independent fields never commit together."""
    def __init__(self, state=None):
        self.visible = deepcopy(state or VirtualState())
        self.durable = deepcopy(self.visible)
        self.events = []
        self.fault = None
        self._counts = {}
        self.writer_busy = False

    def arm(self, fault):
        self.fault, self._counts = fault, {}

    def _event(self, operation, when):
        self.events.append((operation, when))
        key = (operation, when)
        self._counts[key] = self._counts.get(key, 0) + 1
        f = self.fault
        if f and (f.operation, f.when, f.occurrence) == (operation, when, self._counts[key]):
            self.fault = None
            if f.effect == 'crash':
                raise SimulatedCrash(f'{operation}:{when}')
            raise VirtualIOError('DISK_FULL' if f.effect == 'disk_full' else 'FLUSH_FAILED')

    def operation(self, name, mutation=lambda: None):
        self._event(name, 'before')
        mutation()
        self._event(name, 'after')

    def flush(self, name, field_name):
        self.operation(name, lambda: setattr(self.durable, field_name, deepcopy(getattr(self.visible, field_name))))

    def restart(self, *, retain_unflushed=False):
        """Choose either synthetic survivor image explicitly; neither models Windows."""
        if retain_unflushed:
            self.durable = deepcopy(self.visible)
        self.visible = deepcopy(self.durable)
        self.fault, self._counts = None, {}


@dataclass(frozen=True)
class FixtureAuthority:
    """Injected test assertions; NEVER obtained from a request or production user."""
    principal_id: str
    read_principals: frozenset
    live_authorizations: frozenset
    current_incarnation_id: str
    live_sessions: frozenset = frozenset()
    # Exact (Request digest, result full-file SHA) verified current-package assertions.
    verified_packages: frozenset = frozenset()
    initialize_allowed: bool = False
    production_id: str | None = None


@dataclass(frozen=True)
class TransactionInput:
    plan: dict
    command: dict
    blobs: dict
    registration: dict | None = None
    parents: dict = field(default_factory=dict)


@dataclass(frozen=True)
class Outcome:
    state: str
    action: str
    receipt: bytes | None = None
    reason: str | None = None


@dataclass
class Replay:
    head: dict | None = None
    guard: dict | None = None
    high: int = 0
    pending: dict | None = None
    requests: dict = field(default_factory=dict)
    sessions: set = field(default_factory=set)
    ids: set = field(default_factory=set)
    ordered: list = field(default_factory=list)
    unverified_keys: set = field(default_factory=set)
    checkpoints: dict = field(default_factory=dict)
    tail: dict | None = None
    anchor: dict | None = None
    registration: dict | None = None


def encoded(value):
    return wire.canonical_json(value)


def key_of(value):
    return encoded(value)


def observation(raw):
    return {'state': 'MISSING'} if raw is None else {'state': 'PRESENT', 'file_ref': wire.blob_ref(raw)}


class TransactionModel:
    def __init__(self, store, *, keys, authority, partial_commit_reconstruction=False):
        if partial_commit_reconstruction:
            fail('OPTIONAL_CAPABILITY_DISABLED', '$.capability', 'Partial COMMIT reconstruction is OFF')
        self.store, self.keys, self.authority = store, dict(keys), authority
        self._busy = False

    def _key(self, key_id):
        key = self.keys.get(key_id)
        if type(key) is not bytes or len(key) != 32:
            fail('KEY_UNAVAILABLE', '$.key_id', 'Missing explicit test key')
        return key

    def _blob(self, state, ref, kind=None):
        wire.validate_wire(ref, 'BlobRef')
        raw = state.blobs.get(ref['sha256'])
        if raw is None:
            fail('BLOB_MISSING', '$.blob', 'Required proof blob absent')
        if wire.blob_ref(raw) != ref:
            fail('BLOB_HASH_MISMATCH', '$.blob', 'Substituted proof bytes')
        return wire.verify_blob(raw, ref, kind) if kind else raw

    def _image(self, state, head):
        ref = {'sha256': head['snapshot_file_sha256'], 'byte_length': head['snapshot_file_length']}
        raw = self._blob(state, ref)
        self._snapshot(raw, head)
        return raw

    @staticmethod
    def _snapshot(raw, head):
        from .versioned_codec import decode_editorial_versioned, encode_editorial_versioned
        from .schema2_integrity import validate_schema2_snapshot_integrity
        from .snapshot_integrity import validate_snapshot_integrity
        value = wire.decode_canonical_json(raw)
        required = ('production_id', 'generation', 'snapshot_checksum', 'editorial_schema_version')
        if type(value) is not dict or any(k not in value for k in required):
            fail('EDITORIAL_WIRE_ERROR', '$.primary', 'Incomplete editorial image')
        if (wire.blob_ref(raw) != {'sha256': head['snapshot_file_sha256'], 'byte_length': head['snapshot_file_length']} or
                any(value[k] != head[k] for k in ('production_id', 'generation', 'snapshot_checksum', 'editorial_schema_version'))):
            fail('BLOB_HASH_MISMATCH', '$.primary', 'Image/content head mismatch')
        try:
            snapshot = decode_editorial_versioned(raw)
            if encode_editorial_versioned(snapshot) != raw:
                fail('EDITORIAL_WIRE_ERROR', '$.primary', 'Nonexact editorial round trip')
            if value['editorial_schema_version'] == 2:
                validate_schema2_snapshot_integrity(snapshot)
            else:
                validate_snapshot_integrity(snapshot)
        except wire.ProtocolError:
            raise
        except ValueError as error:
            violation = getattr(error, 'violation', None)
            fail('EDITORIAL_WIRE_ERROR', getattr(violation, 'field_path', '$.primary'), str(error))
        return value

    def _registration(self, state):
        if state.registration is None:
            fail('PROTECTION_INVALID', '$.registration', 'Registration missing')
        reg = wire.decode_canonical_json(state.registration)
        wire.validate_wire(reg, 'Registration')
        b = reg['body']
        wire.verify_mac(b, reg['mac'], self._key(b['key_id']), domain='registration')
        init = self._blob(state, b['initialization_ref'], 'InitializationAuthorization')
        ib = init['body']
        wire.verify_mac(ib, init['mac'], self._key(ib['key_id']), domain='initialize')
        for k in ('production_id', 'machine_binding_id', 'storage_epoch_id', 'managed_root_token', 'key_id'):
            if b[k] != ib[k]:
                fail('PROTECTION_INVALID', '$.registration.' + k, 'Registration/initialization mismatch')
        return b, ib

    def _walk_chain(self, state, tip, kind, production, epoch):
        result, seen = [], set()
        while tip is not None:
            if tip['sha256'] in seen:
                fail('JOURNAL_TRANSITION_INVALID', '$.history_guard', 'Proof cycle')
            seen.add(tip['sha256'])
            blob = self._blob(state, tip, kind)
            if blob['production_id'] != production or blob['storage_epoch_id'] != epoch:
                fail('EPOCH_MISMATCH', '$.history_guard', 'Wrong proof context')
            result.append(blob)
            tip = blob['previous_ref']
        return result

    def _guard(self, state, guard, production, epoch):
        wire.validate_wire(guard, 'HistoryGuard')
        if guard['baseline_ref'] is not None:
            base = self._blob(state, guard['baseline_ref'], 'BaselineBlob')
            if base['production_id'] != production or base['storage_epoch_id'] != epoch:
                fail('EPOCH_MISMATCH', '$.history_guard.baseline_ref', 'Baseline context mismatch')
            self._blob(state, base['source_snapshot_ref'])
        for field_name, kind in (('ledger_tip', 'LedgerBlob'), ('barrier_tip', 'BarrierBlob'), ('lineage_tip', 'LineageBlob')):
            self._walk_chain(state, guard[field_name], kind, production, epoch)

    def _load_plan(self, state, record):
        plan = self._blob(state, record['payload']['plan_ref'], 'TransactionPlan')
        command = self._blob(state, plan['command_ref'], 'FrozenCommand')
        wire.verify_mac(command, plan['command_mac'], self._key(plan['key_id']), domain='command')
        wire.verify_record_plan(record, plan, command=command)
        self._check_plan_core(plan, command)
        if encoded(command['authorization']) not in state.authorization_evidence:
            fail('AUTHORIZATION_BINDING_MISMATCH', '$.authorization', 'Frozen policy evidence absent')
        self._image(state, plan['new_content_head'])
        self._guard(state, plan['guard_before'], record['production_id'], record['storage_epoch_id'])
        self._guard(state, plan['guard_commit'], record['production_id'], record['storage_epoch_id'])
        return plan, command

    @staticmethod
    def _jr(index, frame):
        return {'record_index': index, 'record_mac': frame[-32:].hex()}

    @staticmethod
    def _anchor_body(reg, head, guard, high, tail, pending, aborted=False):
        return {'anchor_version': 1, **{k: reg[k] for k in ('production_id', 'machine_binding_id', 'storage_epoch_id')},
                'activation': 'INITIALIZATION_ABORTED' if aborted else 'ACTIVE' if head is not None else 'INITIALIZING',
                'stable_head': deepcopy(head), 'reserved_tx_high_watermark': high,
                'journal_tail': tail, 'pending': deepcopy(pending), 'history_guard': deepcopy(guard), 'key_id': reg['key_id']}

    def _receipt(self, command, core, terminal, head):
        body = {'receipt_version': 1, 'core': core, 'terminal_ref': terminal, 'result_head': head, 'key_id': command['key_id']}
        return encoded({'body': body, 'mac': wire.receipt_mac(body, self._key(command['key_id']))})

    def _ledger(self, state, plan, command, core, guard):
        old = plan['guard_before']
        if any(guard[k] != old[k] for k in ('continuity', 'baseline_ref', 'lineage_tip')):
            fail('JOURNAL_TRANSITION_INVALID', '$.history_guard', 'Continuity/lineage erased')
        if guard['ledger_tip'] is None or guard['ledger_tip'] == old['ledger_tip']:
            fail('JOURNAL_TRANSITION_INVALID', '$.history_guard.ledger_tip', 'Terminal ledger delta required')
        blob = self._blob(state, guard['ledger_tip'], 'LedgerBlob')
        expected = {'request_id': command['request']['request_id'], 'review_session_id': command['request']['review_session_id'],
                    'request_sha256': command['request_sha256'], 'command_mac': plan['command_mac'], 'key_id': command['key_id'],
                    'tx_seq': plan['tx_seq'], 'outcome': core['status'], 'receipt_core_sha256': wire.blob_ref(encoded(core))['sha256']}
        if blob['previous_ref'] != old['ledger_tip'] or blob['entries'] != [expected]:
            fail('JOURNAL_TRANSITION_INVALID', '$.history_guard.ledger_tip', 'Ledger entry/link mismatch')
        self._guard(state, guard, command['request']['production_id'], command['storage_epoch_id'])

    def _parents(self, state, plan, reg, visited):
        result = Replay()
        entries = [entry for blob in self._walk_chain(state, plan['guard_before']['lineage_tip'], 'LineageBlob', reg['production_id'], reg['storage_epoch_id']) for entry in blob['entries']]
        local = [entry for entry in entries if entry['order_status'] == 'VERIFIED_LOCAL_PARENT']
        if len(local) > 1:
            fail('UNVERIFIED_ORDERING', '$.lineage', 'Multiple local predecessors')
        if local:
            link = local[0]
            parent = state.parents.get(link['storage_epoch_id'])
            if parent is None:
                fail('BLOB_MISSING', '$.lineage', 'Verified parent container absent')
            prev = self._scan(parent, visited)
            if prev.pending is not None or any((link['parent_head'] != prev.head, link['parent_guard'] != prev.guard,
                    link['parent_terminal_ref'] != prev.tail, link['machine_binding_id'] != prev.registration['machine_binding_id'],
                    link['production_id'] != reg['production_id'])):
                fail('UNVERIFIED_ORDERING', '$.lineage', 'Parent is not exact finalized boundary')
            expected_primary = None if prev.head is None else self._image(parent, prev.head['content_head'])
            if parent.primary != expected_primary:
                fail('ANCHOR_MISMATCH', '$.lineage', 'Parent primary does not match its head')
            if prev.guard['continuity'] == 'CONTINUITY_LOST' and plan['guard_before']['continuity'] != 'CONTINUITY_LOST':
                fail('HISTORY_CONTINUITY_LOST', '$.lineage', 'New epoch cannot clear lost continuity')
            if prev.guard['continuity'] == 'BASELINE_UNVERIFIED' and plan['guard_before']['continuity'] == 'CONTINUOUS':
                fail('UNVERIFIED_ORDERING', '$.lineage', 'New epoch cannot manufacture verified history')
            if prev.head is not None:
                if plan['expected_commit_receipt']['operation'] == 'INITIALIZE_EMPTY':
                    fail('PLAN_INVALID', '$.lineage', 'Active parent cannot reset to empty history')
                if self._blob(state, plan['image_ref']) != parent.primary:
                    fail('UNVERIFIED_ORDERING', '$.lineage', 'Parent history not preserved byte-for-byte')
            result.requests = deepcopy(prev.requests)
            result.sessions = set(prev.sessions)
            result.ids = set(prev.ids)
            result.ordered = deepcopy(prev.ordered)
            result.unverified_keys = set(prev.unverified_keys)
        # Unverified foreign history never supplies effective order.
        return result

    def _initial(self, state, plan, command, reg, init, visited):
        if (plan['kind'] != 'GENESIS' or plan['tx_seq'] != 0 or plan['new_content_head']['tx_seq'] != 0 or
                plan['base_head'] is not None or plan['new_approvals'] or plan['observed_primary'] != {'state': 'MISSING'}):
            fail('JOURNAL_TRANSITION_INVALID', '$.plan', 'Invalid genesis')
        if plan['initialization_ref'] != reg['initialization_ref']:
            fail('PROTECTION_INVALID', '$.initialization_ref', 'Different initialization')
        q = command['request']
        if (init['request_id'] != q['request_id'] or init['request_sha256'] != command['request_sha256'] or
                init['authorization'] != command['authorization'] or init['principal_id'] != command['principal_id'] or
                init['actor'] != command['actor'] or init['at'] != command['at'] or init['guard_before'] != plan['guard_before'] or
                init['source_ref'] != plan['image_ref']):
            fail('AUTHORIZATION_BINDING_MISMATCH', '$.initialization', 'Initialization/command proof mismatch')
        image = self._snapshot(self._image(state, plan['new_content_head']), plan['new_content_head'])
        if q['operation'] == 'INITIALIZE_EMPTY':
            if image['editorial_schema_version'] != 2 or image['generation'] != 1 or image['approvals'] or image['approval_authority_evidence']:
                fail('PLAN_INVALID', '$.image', 'Empty initialization contains approval history')
            source_ref = q['parameters']['draft_ref']
        else:
            source_ref = q['parameters']['source_ref']
            if plan['guard_before']['continuity'] != 'BASELINE_UNVERIFIED':
                fail('UNVERIFIED_ORDERING', '$.history_guard', 'Imported history must remain unverified')
        if source_ref != plan['image_ref']:
            fail('PLAN_INVALID', '$.image_ref', 'Baseline must preserve exact source bytes')
        result = self._parents(state, plan, reg, visited)
        base_ref = plan['guard_before']['baseline_ref']
        if q['operation'] != 'INITIALIZE_EMPTY':
            if base_ref is None:
                fail('BLOB_MISSING', '$.history_guard.baseline_ref', 'Imported baseline proof required')
            baseline = self._blob(state, base_ref, 'BaselineBlob')
            evidences = {e['approval_id']: e['attestation_digest'] for e in image.get('approval_authority_evidence', [])}
            expected = [{'approval_id': a['id'], 'decision_key': {k: a[k] for k in ('gate', 'policy_version', 'object_ref', 'dependency_digest')},
                         'decision': a['decision'], 'approval_record_sha256': wire.approval_wire_digest(a),
                         'evidence_attestation_digest': evidences.get(a['id'])} for a in image['approvals']]
            if baseline['inherited_approvals'] != expected or baseline['source_snapshot_ref'] != source_ref or baseline['source_schema_version'] != image['editorial_schema_version']:
                fail('UNVERIFIED_ORDERING', '$.baseline', 'Baseline omitted/changed historical approvals')
            result.unverified_keys.update(key_of(a['decision_key']) for a in expected)
            barriers = [e for b in self._walk_chain(state, plan['guard_before']['barrier_tip'], 'BarrierBlob', reg['production_id'], reg['storage_epoch_id']) for e in b['entries']]
            required = {key_of(a['decision_key']) for a in expected}
            if {key_of(e['decision_key']) for e in barriers if e['barrier_kind'] == 'UNVERIFIED_HISTORY'} != required:
                fail('UNVERIFIED_ORDERING', '$.baseline', 'Inherited key barriers missing')
            if q['operation'] == 'TRANSFER_BASELINE':
                manifest = self._blob(state, q['parameters']['manifest_ref'], 'TransferManifest')
                if manifest['production_id'] != reg['production_id'] or manifest['source_ref'] != source_ref:
                    fail('PLAN_INVALID', '$.manifest', 'Foreign manifest context mismatch')
        result.ids.update(a['id'] for a in image['approvals'])
        result.ids.update(e['id'] for e in image['events'])
        result.guard = deepcopy(plan['guard_before'])
        return result

    def _content_delta(self, state, replay, plan, command):
        q = command['request']
        op = q['operation']
        before = None if replay.head is None else self._image(state, replay.head['content_head'])
        after = self._image(state, plan['new_content_head'])
        if plan['kind'] == 'GENESIS':
            return
        if q['expected_head'] != replay.head or q['storage_epoch_id'] != command['storage_epoch_id']:
            fail('EXPECTED_HEAD_MISMATCH', '$.expected_head', 'Not current exact committed head')
        if plan['kind'] == 'REPAIR_EXACT':
            if q['parameters']['image_ref'] != plan['image_ref'] or q['parameters']['expected_observation'] != plan['observed_primary']:
                fail('PLAN_INVALID', '$.parameters', 'Repair target/observation mismatch')
            if plan['new_approvals'] or command['assigned_ids'] != {'approval_id': None, 'event_id': None}:
                fail('PLAN_INVALID', '$.new_approvals', 'Repair cannot create decisions/events')
            return
        if op == 'MIGRATE_SCHEMA':
            from .schema2_migration import migrate_schema1_to_schema2
            from .versioned_codec import decode_editorial_versioned, encode_editorial_versioned
            if wire.decode_canonical_json(before)['editorial_schema_version'] != 1:
                fail('PLAN_INVALID', '$.operation', 'Migration source must be schema 1')
            migrated = migrate_schema1_to_schema2(decode_editorial_versioned(before), actor=command['actor'], at=command['at'], event_id=command['assigned_ids']['event_id'])
            if encode_editorial_versioned(migrated.snapshot) != after or plan['new_approvals']:
                fail('PLAN_INVALID', '$.image', 'Not the exact approved pure migration')
            return
        if op != 'RECORD_DECISION':
            fail('OPERATION_NOT_AVAILABLE', '$.operation', 'No arbitrary publication')
        a, b = wire.decode_canonical_json(before), wire.decode_canonical_json(after)
        changed = {'generation', 'snapshot_checksum', 'approvals', 'events', 'approval_authority_evidence'}
        if a['editorial_schema_version'] != 2 or b['generation'] != a['generation'] + 1 or any(a[k] != b[k] for k in a if k not in changed):
            fail('PLAN_INVALID', '$.image', 'Decision changed unrelated editorial content')
        for name in ('approvals', 'events', 'approval_authority_evidence'):
            if len(b[name]) != len(a[name]) + 1 or b[name][:-1] != a[name]:
                fail('PLAN_INVALID', '$.' + name, 'Not one append-only decision')
        approval, evidence, event = b['approvals'][-1], b['approval_authority_evidence'][-1], b['events'][-1]
        key = q['parameters']['decision_key']
        if (any(approval[k] != key[k] for k in key) or approval['decision'] != q['parameters']['decision'] or
                approval['id'] != command['assigned_ids']['approval_id'] or approval['actor'] != command['actor'] or
                approval['timestamp'] != command['at'] or approval['reason'] != q['parameters']['reason'] or
                approval['review_declarations'] != command['review_snapshot']['review_declarations'] or
                event['id'] != command['assigned_ids']['event_id'] or event['action'] != 'approval_recorded'):
            fail('PLAN_INVALID', '$.approvals', 'Frozen decision fields differ')
        mapping = {'principal_id': command['principal_id'], 'request_id': q['request_id'], 'review_session_id': q['review_session_id'],
                   'authority_policy_id': command['authorization']['policy_ref']['policy_id'],
                   'authority_policy_version': command['authorization']['policy_ref']['policy_version'], 'attested_at': command['at'],
                   'declaration_codes': command['review_snapshot']['confirmed_codes'], 'reconsiders_record_id': q['parameters']['reconsiders_record_id']}
        if any(evidence[k] != value for k, value in mapping.items()):
            fail('AUTHORIZATION_BINDING_MISMATCH', '$.evidence', 'Evidence differs from frozen context')
        binding = {'approval_id': approval['id'], 'decision_key': key, 'decision': approval['decision'],
                   'approval_record_sha256': wire.approval_wire_digest(approval), 'evidence_attestation_digest': evidence['attestation_digest']}
        if plan['new_approvals'] != [binding]:
            fail('PLAN_INVALID', '$.new_approvals', 'Binding does not match exact record/evidence')
        if replay.guard['continuity'] == 'CONTINUITY_LOST':
            fail('HISTORY_CONTINUITY_LOST', '$.history_guard', 'Known history lost')
        if key_of(key) in replay.unverified_keys:
            fail('UNVERIFIED_ORDERING', '$.decision_key', 'Pre-genesis order unverified')
        negatives = [v for v in replay.ordered if v['binding']['decision_key'] == key and v['binding']['decision'] != 'approve']
        if approval['decision'] == 'approve' and negatives:
            latest = negatives[-1]['binding']['approval_id']
            if q['parameters']['reconsiders_record_id'] != latest:
                fail('RECONSIDERATION_MISMATCH', '$.reconsiders_record_id', 'Must target latest verified negative decision')

    def _barrier_delta(self, state, plan, command, guard, *, aborted=False):
        old = plan['guard_before']['barrier_tip']
        bindings = [] if aborted else plan['new_approvals']
        negative = [a for a in bindings if a['decision'] != 'approve']
        if not negative:
            if guard['barrier_tip'] != old:
                fail('JOURNAL_TRANSITION_INVALID', '$.barrier_tip', 'Unexpected barrier change')
            return
        a = negative[0]
        source = {'source_kind': 'LOCAL_TX', 'storage_epoch_id': command['storage_epoch_id'], 'tx_seq': plan['tx_seq'],
                  'approval_id': a['approval_id'], 'approval_record_sha256': a['approval_record_sha256']}
        entry = {'decision_key': a['decision_key'], 'barrier_kind': a['decision'].upper(), 'source': source}
        blob = self._blob(state, guard['barrier_tip'], 'BarrierBlob')
        if blob['previous_ref'] != old or blob['entries'] != [entry]:
            fail('JOURNAL_TRANSITION_INVALID', '$.barrier_tip', 'Negative history barrier missing/substituted')

    def _scan(self, state=None, visited=frozenset()):
        state = state or self.store.visible
        if state.anchor is None:
            fail('ANCHOR_MISSING', '$.anchor', 'No automatic anchor reconstruction')
        anchor = wire.decode_canonical_json(state.anchor)
        wire.validate_wire(anchor, 'AnchorState')
        ab = anchor['body']
        wire.verify_mac(ab, anchor['mac'], self._key(ab['key_id']), domain='anchor')
        reg, init = self._registration(state)
        epoch = reg['storage_epoch_id']
        if epoch in visited:
            fail('UNVERIFIED_ORDERING', '$.lineage', 'Epoch proof cycle')
        visited = visited | {epoch}
        context = {k: reg[k] for k in ('production_id', 'machine_binding_id', 'storage_epoch_id', 'key_id')}
        if any(ab[k] != value for k, value in context.items()):
            fail('ANCHOR_MISMATCH', '$.anchor', 'Registration context mismatch')
        records = []
        previous = None
        for index, frame in enumerate(state.journal):
            try:
                record = wire.decode_journal_frame(frame, self._key(reg['key_id']), expected_index=index, previous_mac=previous, context=context)
            except wire.StructuralError as error:
                if error.code in ('WIRE_FORMAT', 'LIMIT'):
                    fail('JOURNAL_TAIL_UNVERIFIABLE', '$.journal', str(error))
                raise
            records.append(record)
            previous = frame[-32:].hex()
        result = Replay(registration=reg)
        for index, record in enumerate(records):
            jr = self._jr(index, state.journal[index])
            plan, command = self._load_plan(state, record)
            plan_ref = record['payload']['plan_ref']
            t = record['record_type']
            if t == 'PREPARE':
                if result.pending is not None:
                    fail('JOURNAL_TRANSITION_INVALID', '$.journal', 'Concurrent PREPARE')
                if index == 0:
                    result = self._initial(state, plan, command, reg, init, visited)
                    result.registration = reg
                elif plan['kind'] == 'GENESIS':
                    fail('JOURNAL_TRANSITION_INVALID', '$.journal', 'Repeated genesis in epoch')
                if plan['base_head'] != result.head or plan['guard_before'] != result.guard:
                    fail('JOURNAL_TRANSITION_INVALID', '$.plan', 'Base head/guard mismatch')
                if index and result.head is None:
                    fail('JOURNAL_TRANSITION_INVALID', '$.journal', 'New epoch required after initialization abort')
                seq = 0 if index == 0 else None if plan['kind'] == 'REPAIR_EXACT' else result.high + 1
                if seq is not None and seq > wire.U64_MAX:
                    fail('SEQUENCE_EXHAUSTED', '$.tx_seq', 'No sequence wrap')
                if plan['tx_seq'] != seq:
                    fail('JOURNAL_TRANSITION_INVALID', '$.tx_seq', 'Invalid sequence reservation')
                if plan['kind'] == 'PUBLISH' and (plan['new_content_head']['tx_seq'] != seq or plan['new_content_head']['generation'] != result.head['content_head']['generation'] + 1):
                    fail('PLAN_INVALID', '$.new_content_head', 'Generation/sequence mismatch')
                self._content_delta(state, result, plan, command)
                self._ledger(state, plan, command, plan['expected_commit_receipt'], plan['guard_commit'])
                self._barrier_delta(state, plan, command, plan['guard_commit'])
                q = command['request']
                if q['request_id'] in result.requests or (q['review_session_id'] is not None and q['review_session_id'] in result.sessions):
                    fail('IDEMPOTENCY_CONFLICT', '$.request_id', 'Consumed request/session reused')
                assigned = {v for v in command['assigned_ids'].values() if v is not None}
                if len(assigned) != sum(v is not None for v in command['assigned_ids'].values()) or assigned & result.ids:
                    fail('IDEMPOTENCY_CONFLICT', '$.assigned_ids', 'Reserved ID reused')
                result.ids.update(assigned)
                result.sessions.update([q['review_session_id']] if q['review_session_id'] is not None else [])
                result.requests[q['request_id']] = {'command': command, 'plan': plan, 'receipt': None}
                result.pending = {'plan_ref': plan_ref, 'plan': plan, 'command': command, 'prepare_ref': jr, 'intent_ref': None}
                if seq is not None:
                    result.high = seq
            else:
                pending = result.pending
                if pending is None or pending['plan_ref'] != plan_ref or record['payload']['prepare_ref'] != pending['prepare_ref']:
                    fail('JOURNAL_TRANSITION_INVALID', '$.journal', 'Orphan/forked record')
                if t == 'PUBLISH_INTENT':
                    if pending['intent_ref'] is not None:
                        fail('JOURNAL_TRANSITION_INVALID', '$.journal', 'Duplicate INTENT')
                    pending['intent_ref'] = jr
                else:
                    core = record['payload']['receipt_core']
                    if t == 'ABORT':
                        if pending['intent_ref'] is not None:
                            fail('JOURNAL_TRANSITION_INVALID', '$.journal', 'ABORT after INTENT forbidden')
                        expected = self._abort_core(plan, core['abort_code'])
                        if core != expected:
                            fail('JOURNAL_TRANSITION_INVALID', '$.receipt_core', 'ABORT core changed')
                        guard = record['payload']['result_guard']
                        self._ledger(state, plan, command, core, guard)
                        self._barrier_delta(state, plan, command, guard, aborted=True)
                    else:
                        if pending['intent_ref'] is None or record['payload']['intent_ref'] != pending['intent_ref']:
                            fail('JOURNAL_TRANSITION_INVALID', '$.journal', 'COMMIT without matching INTENT')
                        guard = plan['guard_commit']
                        if plan['kind'] != 'REPAIR_EXACT':
                            result.head = {'committed_head_version': 1, 'content_head': plan['new_content_head'], 'commit_ref': jr}
                        if plan['kind'] == 'PUBLISH':
                            result.ordered.extend({'epoch': epoch, 'tx_seq': plan['tx_seq'], 'binding': binding} for binding in plan['new_approvals'])
                    result.guard = deepcopy(guard)
                    result.requests[command['request']['request_id']]['receipt'] = self._receipt(command, core, jr, result.head)
                    result.pending = None
            result.tail = jr
            pd = None if result.pending is None else {'pending_version': 1,
                    'phase': 'PREPARED' if result.pending['intent_ref'] is None else 'PUBLISH_INTENT',
                    'plan_ref': result.pending['plan_ref'], 'prepare_ref': result.pending['prepare_ref'], 'intent_ref': result.pending['intent_ref']}
            checkpoint = self._anchor_body(reg, result.head, result.guard, result.high, jr, pd,
                                           aborted=result.head is None and t == 'ABORT')
            result.checkpoints[index] = checkpoint
        tail = ab['journal_tail']
        if tail['record_index'] >= len(records):
            fail('ANCHOR_MISMATCH', '$.journal_tail', 'Anchor ahead of complete journal')
        if tail != self._jr(tail['record_index'], state.journal[tail['record_index']]):
            fail('JOURNAL_PREFIX_MISMATCH', '$.journal_tail', 'Anchor references a different chain')
        if ab != result.checkpoints[tail['record_index']]:
            fail('ANCHOR_MISMATCH', '$.anchor', 'Anchor head/guard/pending state mismatch')
        result.anchor = ab
        return result

    @staticmethod
    def _abort_core(plan, code):
        return {**deepcopy(plan['expected_commit_receipt']), 'status': 'ABORTED_PRECOMMIT', 'abort_code': code,
                'result_content_head': None if plan['base_head'] is None else plan['base_head']['content_head'],
                'approval_ids': [], 'event_ids': []}

    def _put_blob(self, raw):
        ref = wire.blob_ref(raw)
        prior = self.store.visible.blobs.get(ref['sha256'])
        if prior is not None and prior != raw:
            fail('BLOB_HASH_MISMATCH', '$.blob', 'Hash collision/mismatching bytes')
        self.store.visible.blobs[ref['sha256']] = raw
        return ref

    def _write_anchor(self, body, phase):
        data = encoded({'body': body, 'mac': wire.anchor_mac(body, self._key(body['key_id']))})
        self.store.operation(phase + '.replace', lambda: setattr(self.store.visible, 'anchor', data))
        self.store.flush(phase + '.flush', 'anchor')

    def _append(self, plan, record_type, payload, phase):
        state = self.store.visible
        head = plan['new_content_head']
        record = {'journal_record_version': 1, **{k: head[k] for k in ('production_id', 'machine_binding_id', 'storage_epoch_id')},
                  'record_index': len(state.journal), 'previous_record_mac': state.journal[-1][-32:].hex() if state.journal else None,
                  'key_id': plan['key_id'], 'record_type': record_type, 'payload': payload}
        frame = wire.encode_journal_frame(record, self._key(plan['key_id']))
        self.store.operation(phase + '.append', lambda: state.journal.append(frame))
        self.store.flush(phase + '.journal.flush', 'journal')
        return self._jr(record['record_index'], frame)

    def _pending_anchor(self, replay, pending, phase):
        body = self._anchor_body(replay.registration, replay.head, replay.guard, replay.high,
                pending['intent_ref'] or pending['prepare_ref'], {'pending_version': 1,
                'phase': 'PUBLISH_INTENT' if pending['intent_ref'] else 'PREPARED', 'plan_ref': pending['plan_ref'],
                'prepare_ref': pending['prepare_ref'], 'intent_ref': pending['intent_ref']})
        self._write_anchor(body, phase)

    def _finalize(self, replay, *, phase='W8.anchor'):
        body = replay.checkpoints[replay.tail['record_index']]
        self._write_anchor(body, phase)
        checked = self._scan()
        if checked.pending is not None or checked.anchor != body:
            fail('ANCHOR_MISMATCH', '$.anchor', 'Finalization not verified')
        return checked

    def _publish(self, plan, phase='W5.primary'):
        state = self.store.visible
        image = self._image(state, plan['new_content_head'])
        target = observation(image)
        if observation(state.primary) not in (plan['observed_primary'], target):
            fail('ANCHOR_MISMATCH', '$.primary', 'Neither recorded A/observation nor exact B')
        if state.images.get(plan['image_ref']['sha256']) != image:
            fail('BLOB_MISSING', '$.prepared_image', 'Exact prepared sibling image missing')
        self.store.operation(phase + '.replace', lambda: setattr(state, 'primary', image))
        self.store.flush(phase + '.flush', 'primary')
        self.store.operation('W6.primary.verify', lambda: self._snapshot(state.primary, plan['new_content_head']))
        self.store.flush('W6.primary.flush', 'primary')

    def _abort(self, replay, code):
        pending = replay.pending
        if pending is None or pending['intent_ref'] is not None:
            fail('JOURNAL_TRANSITION_INVALID', '$.journal', 'ABORT needs proven pre-intent prefix')
        plan, command = pending['plan'], pending['command']
        if observation(self.store.visible.primary) != plan['observed_primary']:
            fail('ANCHOR_MISMATCH', '$.primary', 'Cannot ABORT unknown/changed A')
        core = self._abort_core(plan, code)
        entry = {'request_id': command['request']['request_id'], 'review_session_id': command['request']['review_session_id'],
                 'request_sha256': command['request_sha256'], 'command_mac': plan['command_mac'], 'key_id': command['key_id'],
                 'tx_seq': plan['tx_seq'], 'outcome': 'ABORTED_PRECOMMIT', 'receipt_core_sha256': wire.blob_ref(encoded(core))['sha256']}
        blob = {'blob_version': 1, 'blob_type': 'LEDGER_DELTA', 'production_id': command['request']['production_id'],
                'storage_epoch_id': command['storage_epoch_id'], 'previous_ref': plan['guard_before']['ledger_tip'], 'entries': [entry]}
        raw = encoded(blob)
        guard = {**deepcopy(plan['guard_before']), 'ledger_tip': wire.blob_ref(raw)}
        self.store.operation('ABORT.blob.write', lambda: self._put_blob(raw))
        self.store.flush('ABORT.blob.flush', 'blobs')
        self._append(plan, 'ABORT', {'prepare_ref': pending['prepare_ref'], 'plan_ref': pending['plan_ref'],
                     'abort_code': code, 'receipt_core': core, 'result_guard': guard}, 'ABORT')
        return self._finalize(self._scan())

    def _finish_intent(self, replay):
        pending = replay.pending
        plan = pending['plan']
        if pending['intent_ref'] is None:
            fail('JOURNAL_TRANSITION_INVALID', '$.journal', 'Forward completion requires INTENT')
        image = self._image(self.store.visible, plan['new_content_head'])
        if self.store.visible.images.get(plan['image_ref']['sha256']) != image:
            fail('BLOB_MISSING', '$.prepared_image', 'Exact prepared image absent/substituted')
        self._pending_anchor(replay, pending, 'RECOVERY.intent_anchor')
        self._publish(plan)
        record_type = {'GENESIS': 'GENESIS', 'PUBLISH': 'SNAPSHOT_COMMIT', 'REPAIR_EXACT': 'REPAIR_COMMIT'}[plan['kind']]
        self._append(plan, record_type, {'prepare_ref': pending['prepare_ref'], 'intent_ref': pending['intent_ref'],
                    'plan_ref': pending['plan_ref'], 'receipt_core': plan['expected_commit_receipt']}, 'W7.COMMIT')
        return self._finalize(self._scan())

    def _ack(self, replay, request_id, action):
        receipt = replay.requests[request_id]['receipt']
        if (receipt is None or replay.pending is not None or replay.anchor != replay.checkpoints[replay.tail['record_index']] or
                self.store.visible.anchor != self.store.durable.anchor or self.store.visible.journal != self.store.durable.journal or
                self.store.visible.primary != self.store.durable.primary):
            fail('RECOVERY_REQUIRED', '$.receipt', 'No final receipt before verified W8')
        self.store.operation('W9.receipt.ack')
        core = wire.decode_canonical_json(receipt)['body']['core']
        return Outcome('ABORTED' if core['status'] == 'ABORTED_PRECOMMIT' else 'FINALIZED', action, receipt)

    def _recover(self):
        replay = self._scan()
        pending = replay.pending
        if pending:
            request_id = pending['command']['request']['request_id']
            target = observation(self._image(self.store.visible, pending['plan']['new_content_head']))
            allowed = (pending['plan']['observed_primary'],) if pending['intent_ref'] is None else (pending['plan']['observed_primary'], target)
            if observation(self.store.visible.primary) not in allowed:
                fail('ANCHOR_MISMATCH', '$.primary', 'Unknown pending image')
            self.store.flush('RECOVERY.journal.flush', 'journal')
            if pending['intent_ref'] is None:
                replay = self._abort(replay, 'RECOVERY_PREINTENT_ABORT')
                action = 'ABORT_PREINTENT'
            else:
                replay = self._finish_intent(replay)
                action = 'COMPLETE_FORWARD'
            return self._ack(replay, request_id, action)
        last = self.store.visible.journal[-1]
        record = wire.decode_journal_frame(last, self._key(replay.registration['key_id']))
        plan, command = self._load_plan(self.store.visible, record)
        if record['record_type'] == 'ABORT':
            expected = plan['observed_primary']
        else:
            expected = observation(self._image(self.store.visible, replay.head['content_head']))
        if observation(self.store.visible.primary) != expected:
            fail('ANCHOR_MISMATCH', '$.primary', 'Stable/terminal primary mismatch; explicit repair only')
        lagged = replay.anchor != replay.checkpoints[replay.tail['record_index']]
        if self.store.visible.journal != self.store.durable.journal:
            self.store.flush('RECOVERY.journal.flush', 'journal')
        if self.store.visible.primary != self.store.durable.primary:
            self.store.flush('RECOVERY.primary.flush', 'primary')
        if lagged or self.store.visible.anchor != self.store.durable.anchor:
            replay = self._finalize(replay)
        return self._ack(replay, command['request']['request_id'], 'FINALIZE_TERMINAL' if lagged else 'STABLE')

    def _run(self, function):
        if self._busy or self.store.writer_busy:
            fail('LOCK_BUSY', '$.lock', 'One synthetic writer at a time')
        self._busy = self.store.writer_busy = True
        try:
            return function()
        except VirtualIOError as error:
            # Could have failed after an observable mutation: never assert failure/success.
            return Outcome('PENDING', 'RECONCILE_REQUIRED', reason=error.code)
        finally:
            self._busy = self.store.writer_busy = False

    def recover(self):
        return self._run(self._recover)

    def inspect(self):
        """Read-only replay/proof validation, not effective authority evaluation."""
        return deepcopy(self._scan())

    def latest_verified(self, decision_key):
        replay = self._scan()
        if replay.guard['continuity'] == 'CONTINUITY_LOST':
            fail('HISTORY_CONTINUITY_LOST', '$.history_guard', 'Continuity lost')
        if key_of(decision_key) in replay.unverified_keys:
            fail('UNVERIFIED_ORDERING', '$.decision_key', 'Imported order is unverified')
        if replay.pending is not None or replay.anchor != replay.checkpoints[replay.tail['record_index']]:
            fail('RECOVERY_REQUIRED', '$.journal', 'Pending transaction must be reconciled')
        if replay.head is not None and self.store.visible.primary != self._image(self.store.visible, replay.head['content_head']):
            fail('ANCHOR_MISMATCH', '$.primary', 'Current primary differs from protected head')
        applicable = [v for v in replay.ordered if v['binding']['decision_key'] == decision_key]
        return deepcopy(applicable[-1]) if applicable else None

    def _authorize(self, command):
        a = self.authority
        if (a.production_id != command['request']['production_id'] or a.principal_id != command['principal_id'] or
                encoded(command['authorization']) not in a.live_authorizations):
            fail('PERMISSION_DENIED', '$.authorization', 'Explicit injected principal/operation grants missing')
        q = command['request']
        if q['operation'] in ('INITIALIZE_EMPTY', 'IMPORT_BASELINE', 'TRANSFER_BASELINE') and not a.initialize_allowed:
            fail('PERMISSION_DENIED', '$.authorization', 'Explicit initialization fixture required')
        if q['operation'] == 'RECORD_DECISION':
            review = command['review_snapshot']
            if review['server_incarnation_id'] != a.current_incarnation_id or q['review_session_id'] not in a.live_sessions:
                fail('SESSION_INVALIDATED', '$.review_session_id', 'Unbound session invalid after restart')
            assertion = (command['request_sha256'], command['expected_result']['snapshot_file_sha256'])
            if assertion not in a.verified_packages:
                fail('PERMISSION_DENIED', '$.review_snapshot', 'Verified current-package fixture absent')

    def _check_plan_core(self, plan, command):
        wire.validate_wire(plan, 'TransactionPlan')
        wire.validate_wire(command, 'FrozenCommand')
        wire.verify_mac(command, plan['command_mac'], self._key(plan['key_id']), domain='command')
        q, core = command['request'], plan['expected_commit_receipt']
        expected_status = {'GENESIS': 'INITIALIZED', 'PUBLISH': 'COMMITTED', 'REPAIR_EXACT': 'REPAIRED'}[plan['kind']]
        expected = {'receipt_core_version': 1, 'request_id': q['request_id'], 'request_sha256': command['request_sha256'],
                    'storage_epoch_id': command['storage_epoch_id'], 'operation': q['operation'], 'tx_seq': plan['tx_seq'],
                    'status': expected_status, 'result_content_head': plan['new_content_head'],
                    'approval_ids': [command['assigned_ids']['approval_id']] if command['assigned_ids']['approval_id'] else [],
                    'event_ids': [command['assigned_ids']['event_id']] if command['assigned_ids']['event_id'] else [], 'abort_code': None}
        if core != expected or plan['new_content_head'] != command['expected_result'] or plan['command_ref'] != wire.blob_ref(encoded(command)):
            fail('PLAN_INVALID', '$.expected_commit_receipt', 'Frozen core/command/head mismatch')
        if plan['kind'] != 'GENESIS' and plan['initialization_ref'] is not None:
            fail('PLAN_INVALID', '$.initialization_ref', 'Only genesis has initialization_ref')

    def execute(self, transaction):
        return self._run(lambda: self._execute(deepcopy(transaction)))

    def _execute(self, transaction):
        state = self.store.visible
        command, plan = transaction.command, transaction.plan
        q = command['request']
        # Request/identity lookup precedes current head CAS, live grants or new image admission.
        self._request_shape(q)
        if self.authority.production_id != q['production_id'] or self.authority.principal_id not in self.authority.read_principals:
            fail('PERMISSION_DENIED', '$.principal_id', 'No fixture read access')
        existing = None
        if state.anchor is not None:
            existing = self._scan()
            entry = existing.requests.get(q['request_id'])
            if entry:
                old = entry['command']
                if encoded(q) != encoded(old['request']) or self.authority.principal_id != old['principal_id']:
                    fail('IDEMPOTENCY_CONFLICT', '$.request_id', 'Request bytes/principal reused')
                self._recover()
                finalized = self._scan()
                return self._ack(finalized, q['request_id'], 'REPLAY_RECEIPT')
            if existing.pending is not None:
                fail('RECOVERY_REQUIRED', '$.journal', 'Finish admitted transaction first')
        elif state.journal or state.registration is not None:
            fail('ANCHOR_MISSING', '$.anchor', 'Known lineage without anchor; no new bootstrap')
        if q['operation'] == 'PUBLISH_REVISION':
            fail('OPERATION_NOT_AVAILABLE', '$.operation', 'Reserved operation disabled')
        self._check_plan_core(plan, command)
        self._authorize(command)
        if existing is not None and plan['kind'] == 'GENESIS':
            fail('PLAN_INVALID', '$.kind', 'No reset/merge of a registered epoch')
        if existing is None and plan['kind'] != 'GENESIS':
            fail('ANCHOR_MISSING', '$.anchor', 'Only explicit first initialization can create an anchor')
        candidate = deepcopy(state)
        for sha, raw in transaction.blobs.items():
            if wire.blob_ref(raw)['sha256'] != sha or (sha in candidate.blobs and candidate.blobs[sha] != raw):
                fail('BLOB_HASH_MISMATCH', '$.blobs', 'Invalid supplied blob map')
            candidate.blobs[sha] = raw
        candidate.authorization_evidence.add(encoded(command['authorization']))
        if transaction.parents:
            if existing is not None:
                fail('PLAN_INVALID', '$.parents', 'Cannot reset retained parent epochs')
            candidate.parents = deepcopy(transaction.parents)
        if existing is None:
            if transaction.registration is None:
                fail('PROTECTION_INVALID', '$.registration', 'Initialization registration fixture required')
            candidate.registration = encoded(transaction.registration)
        reg, init = self._registration(candidate)
        context = {k: reg[k] for k in ('production_id', 'machine_binding_id', 'storage_epoch_id', 'key_id')}
        prepare = {'journal_record_version': 1, **context, 'record_index': len(state.journal),
                   'previous_record_mac': state.journal[-1][-32:].hex() if state.journal else None,
                   'record_type': 'PREPARE', 'payload': {'plan_ref': wire.blob_ref(encoded(plan))}}
        self._load_plan(candidate, prepare)
        if existing is None:
            base = self._initial(candidate, plan, command, reg, init, frozenset({reg['storage_epoch_id']}))
        else:
            base = existing
        if plan['base_head'] != base.head or plan['guard_before'] != base.guard:
            fail('EXPECTED_HEAD_MISMATCH', '$.expected_head', 'Not exact current head/guard')
        expected_seq = 0 if existing is None else None if plan['kind'] == 'REPAIR_EXACT' else base.high + 1
        if expected_seq is not None and expected_seq > wire.U64_MAX:
            fail('SEQUENCE_EXHAUSTED', '$.tx_seq', 'No sequence wrap')
        if plan['kind'] == 'PUBLISH' and (plan['new_content_head']['tx_seq'] != expected_seq or
                plan['new_content_head']['generation'] != base.head['content_head']['generation'] + 1):
            fail('PLAN_INVALID', '$.new_content_head', 'Generation/sequence mismatch')
        if plan['tx_seq'] != expected_seq:
            fail('PLAN_INVALID', '$.tx_seq', 'Incorrect reservation')
        if q['request_id'] in base.requests or (q['review_session_id'] is not None and q['review_session_id'] in base.sessions):
            fail('IDEMPOTENCY_CONFLICT', '$.request_id', 'Retained request/session consumed')
        assigned = [v for v in command['assigned_ids'].values() if v is not None]
        if len(set(assigned)) != len(assigned) or any(v in base.ids for v in assigned):
            fail('IDEMPOTENCY_CONFLICT', '$.assigned_ids', 'Assigned ID consumed')
        if observation(state.primary) != plan['observed_primary']:
            fail('EXPECTED_HEAD_MISMATCH', '$.primary', 'Source observation CAS failed')
        if plan['kind'] == 'PUBLISH' and plan['observed_primary'] != observation(self._image(candidate, base.head['content_head'])):
            fail('ANCHOR_MISMATCH', '$.primary', 'Normal publication requires exact A')
        self._content_delta(candidate, base, plan, command)
        self._ledger(candidate, plan, command, plan['expected_commit_receipt'], plan['guard_commit'])
        self._barrier_delta(candidate, plan, command, plan['guard_commit'])
        # W0 has completed; all remaining effects are individually observable.
        self.store.operation('W0.freeze')
        self.store.operation('W1.blobs.write', lambda: setattr(state, 'blobs', deepcopy(candidate.blobs)))
        self.store.flush('W1.blobs.flush', 'blobs')
        self.store.operation('W1.authorization.write', lambda: setattr(state, 'authorization_evidence', deepcopy(candidate.authorization_evidence)))
        self.store.flush('W1.authorization.flush', 'authorization_evidence')
        if existing is None:
            self.store.operation('W1.registration.write', lambda: setattr(state, 'registration', candidate.registration))
            self.store.flush('W1.registration.flush', 'registration')
            self.store.operation('W1.parents.write', lambda: setattr(state, 'parents', deepcopy(candidate.parents)))
            self.store.flush('W1.parents.flush', 'parents')
        image = self._image(candidate, plan['new_content_head'])
        self.store.operation('W1.image.write', lambda: state.images.update({plan['image_ref']['sha256']: image}))
        self.store.flush('W1.image.flush', 'images')
        if state.primary is not None:
            field_name = 'forensic' if plan['kind'] == 'REPAIR_EXACT' else 'backups'
            fingerprint = wire.blob_ref(state.primary)['sha256']
            self.store.operation('W2.' + field_name + '.replace', lambda: getattr(state, field_name).update({fingerprint: state.primary}))
            self.store.flush('W2.' + field_name + '.flush', field_name)
        prep_ref = self._append(plan, 'PREPARE', prepare['payload'], 'W2.PREPARE')
        pending = {'plan_ref': prepare['payload']['plan_ref'], 'plan': plan, 'command': command, 'prepare_ref': prep_ref, 'intent_ref': None}
        base.registration = reg
        base.high = expected_seq if expected_seq is not None else base.high
        self._pending_anchor(base, pending, 'W3.anchor')
        try:
            self._authorize(command)  # Single-writer synthetic policy-update boundary at W4.
        except ModelError:
            checked = self._abort(self._scan(), 'REVALIDATION_FAILED')
            return self._ack(checked, q['request_id'], 'ABORT_POLICY_CHANGED')
        intent = self._append(plan, 'PUBLISH_INTENT', {'prepare_ref': prep_ref, 'plan_ref': pending['plan_ref']}, 'W4.INTENT')
        pending['intent_ref'] = intent
        self._pending_anchor(base, pending, 'W4.anchor')
        self._publish(plan)
        record_type = {'GENESIS': 'GENESIS', 'PUBLISH': 'SNAPSHOT_COMMIT', 'REPAIR_EXACT': 'REPAIR_COMMIT'}[plan['kind']]
        self._append(plan, record_type, {'prepare_ref': prep_ref, 'intent_ref': intent, 'plan_ref': pending['plan_ref'],
                                      'receipt_core': plan['expected_commit_receipt']}, 'W7.COMMIT')
        finalized = self._finalize(self._scan())
        return self._ack(finalized, q['request_id'], 'COMMIT')

    @staticmethod
    def _request_shape(q):
        if type(q) is dict and q.get('operation') == 'PUBLISH_REVISION':
            wire.canonical_json(q, max_bytes=wire.MAX_REQUEST_BYTES)
            wire._check(q, {'request_version': wire._choice(1), 'request_id': wire._uuid, 'production_id': wire._uuid,
                           'storage_epoch_id': wire._nullable(wire._uuid), 'expected_head': wire._nullable('CommittedHead'),
                           'review_session_id': wire._nullable(wire._uuid), 'operation': wire._choice('PUBLISH_REVISION'),
                           'parameters': {'proposal_ref': 'BlobRef', 'reason': wire._nonempty}})
        else:
            wire.validate_wire(q, 'Request')
