"""Independent state/fault expectations for the synthetic S1 recovery model."""
import copy
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

from editorial import storage_protocol_v1 as w
from editorial import storage_transaction_model_v1 as m
from tests.test_storage_protocol_v1 import fixtures, KEY, P, M, E, R, ROOT, POLICY, CONNECTION, PRINCIPAL, AT, ACTOR, MACS, c, ref


def uid(n):
    return f'90000000-0000-4000-8000-{n:012d}'


def sealed(value):
    value = copy.deepcopy(value)
    value.pop('snapshot_checksum', None)
    value['snapshot_checksum'] = hashlib.sha256(c(value)).hexdigest()
    return value


def authority(transaction, *, incarnation=CONNECTION):
    f = transaction.command
    q = f['request']
    return m.FixtureAuthority(PRINCIPAL, frozenset([PRINCIPAL]), frozenset([c(f['authorization'])]), incarnation,
            frozenset([q['review_session_id']]) if q['review_session_id'] else frozenset(),
            frozenset([(f['request_sha256'], f['expected_result']['snapshot_file_sha256'])]), True, production_id=q['production_id'])


def genesis(*, image=None, epoch=E, request=R, operation='INITIALIZE_EMPTY', guard=None, extra=None, parents=None):
    image = copy.deepcopy(image or fixtures()['S'])
    image_bytes = c(image)
    guard = copy.deepcopy(guard or {'guard_version': 1, 'continuity': 'CONTINUOUS' if operation == 'INITIALIZE_EMPTY' else 'BASELINE_UNVERIFIED',
                                   'baseline_ref': None, 'ledger_tip': None, 'barrier_tip': None, 'lineage_tip': None})
    blobs = dict(extra or {})
    def put(value):
        raw = c(value); r = ref(value); blobs[r['sha256']] = raw; return r
    image_ref = put(image)
    if operation != 'INITIALIZE_EMPTY':
        evidences = {e['approval_id']: e['attestation_digest'] for e in image.get('approval_authority_evidence', [])}
        inherited = [{'approval_id': a['id'], 'decision_key': {k: a[k] for k in ('gate', 'policy_version', 'object_ref', 'dependency_digest')},
                      'decision': a['decision'], 'approval_record_sha256': w.approval_wire_digest(a), 'evidence_attestation_digest': evidences.get(a['id'])} for a in image['approvals']]
        base = {'blob_version': 1, 'blob_type': 'BASELINE', 'production_id': image['production_id'], 'storage_epoch_id': epoch,
                'source_schema_version': image['editorial_schema_version'], 'source_snapshot_ref': image_ref, 'inherited_approvals': inherited}
        guard['baseline_ref'] = put(base)
        if inherited:
            barriers = [{'decision_key': a['decision_key'], 'barrier_kind': 'UNVERIFIED_HISTORY',
                         'source': {'source_kind': 'BASELINE', 'baseline_ref': guard['baseline_ref'], 'approval_id': a['approval_id'], 'approval_record_sha256': a['approval_record_sha256']}} for a in inherited]
            guard['barrier_tip'] = put({'blob_version': 1, 'blob_type': 'BARRIER_DELTA', 'production_id': image['production_id'],
                                       'storage_epoch_id': epoch, 'previous_ref': None, 'entries': barriers})
    q = {'request_version': 1, 'request_id': request, 'production_id': image['production_id'], 'storage_epoch_id': None,
         'expected_head': None, 'review_session_id': None, 'operation': operation,
         'parameters': {'draft_ref' if operation == 'INITIALIZE_EMPTY' else 'source_ref': image_ref}}
    if operation == 'TRANSFER_BASELINE':
        manifest = {'transfer_manifest_version': 1, 'production_id': image['production_id'], 'source_ref': image_ref,
                    'source_machine_id': None, 'source_epoch_id': None, 'source_head': None, 'source_guard': None}
        q['parameters']['manifest_ref'] = put(manifest)
    auth = copy.deepcopy(fixtures()['F']['authorization'])
    head = {'content_head_version': 1, 'production_id': image['production_id'], 'machine_binding_id': M, 'storage_epoch_id': epoch,
            'editorial_schema_version': image['editorial_schema_version'], 'generation': image['generation'],
            'snapshot_checksum': image['snapshot_checksum'], 'snapshot_file_sha256': image_ref['sha256'], 'snapshot_file_length': len(image_bytes), 'tx_seq': 0}
    f = {'command_version': 1, 'request': q, 'request_sha256': w.request_digest(q), 'key_id': 'fixture-key', 'principal_id': PRINCIPAL,
         'actor': ACTOR, 'at': AT, 'authorization': auth, 'assigned_ids': {'approval_id': None, 'event_id': None},
         'storage_epoch_id': epoch, 'expected_result': head, 'review_snapshot': None}
    init = {'initialization_version': 1, 'request_id': request, 'request_sha256': f['request_sha256'], 'production_id': image['production_id'],
            'machine_binding_id': M, 'storage_epoch_id': epoch, 'managed_root_token': ROOT, 'source_ref': image_ref, 'principal_id': PRINCIPAL,
            'actor': ACTOR, 'at': AT, 'policy_ref': auth['policy_ref'], 'authorization': auth, 'guard_before': guard, 'key_id': 'fixture-key'}
    iw = {'body': init, 'mac': w.initialization_mac(init, KEY)}
    regbody = {'registration_version': 1, 'storage_protocol_version': 1, 'production_id': image['production_id'], 'machine_binding_id': M,
               'storage_epoch_id': epoch, 'managed_root_token': ROOT, 'initialization_ref': put(iw), 'storage_profile_id': 'fixture-profile', 'key_id': 'fixture-key'}
    reg = {'body': regbody, 'mac': w.registration_mac(regbody, KEY)}
    plan = finish_plan(q, f, head, guard, blobs, kind='GENESIS', base=None, observed={'state': 'MISSING'}, seq=0,
                       initialization_ref=regbody['initialization_ref'])
    return m.TransactionInput(plan, f, blobs, reg, parents or {})


def finish_plan(q, f, head, guard, blobs, *, kind, base, observed, seq, initialization_ref=None, bindings=None):
    core = {'receipt_core_version': 1, 'request_id': q['request_id'], 'request_sha256': f['request_sha256'],
            'storage_epoch_id': f['storage_epoch_id'], 'operation': q['operation'], 'tx_seq': seq,
            'status': {'GENESIS': 'INITIALIZED', 'PUBLISH': 'COMMITTED', 'REPAIR_EXACT': 'REPAIRED'}[kind],
            'result_content_head': head, 'approval_ids': [f['assigned_ids']['approval_id']] if f['assigned_ids']['approval_id'] else [],
            'event_ids': [f['assigned_ids']['event_id']] if f['assigned_ids']['event_id'] else [], 'abort_code': None}
    fm = w.frozen_command_mac(f, KEY)
    ledger = {'blob_version': 1, 'blob_type': 'LEDGER_DELTA', 'production_id': q['production_id'], 'storage_epoch_id': f['storage_epoch_id'],
              'previous_ref': guard['ledger_tip'], 'entries': [{'request_id': q['request_id'], 'review_session_id': q['review_session_id'],
              'request_sha256': f['request_sha256'], 'command_mac': fm, 'key_id': 'fixture-key', 'tx_seq': seq,
              'outcome': core['status'], 'receipt_core_sha256': ref(core)['sha256']}]}
    blobs[ref(ledger)['sha256']] = c(ledger)
    after_guard = {**copy.deepcopy(guard), 'ledger_tip': ref(ledger)}
    if bindings and bindings[0]['decision'] != 'approve':
        a = bindings[0]
        entry = {'decision_key': a['decision_key'], 'barrier_kind': a['decision'].upper(),
                 'source': {'source_kind': 'LOCAL_TX', 'storage_epoch_id': f['storage_epoch_id'], 'tx_seq': seq,
                            'approval_id': a['approval_id'], 'approval_record_sha256': a['approval_record_sha256']}}
        barrier = {'blob_version': 1, 'blob_type': 'BARRIER_DELTA', 'production_id': q['production_id'], 'storage_epoch_id': f['storage_epoch_id'],
                   'previous_ref': guard['barrier_tip'], 'entries': [entry]}
        blobs[ref(barrier)['sha256']] = c(barrier); after_guard['barrier_tip'] = ref(barrier)
    plan = {'plan_version': 1, 'kind': kind, 'request_id': q['request_id'], 'review_session_id': q['review_session_id'], 'tx_seq': seq,
            'key_id': 'fixture-key', 'command_ref': ref(f), 'command_mac': fm, 'base_head': base, 'observed_primary': observed,
            'new_content_head': head, 'image_ref': {'sha256': head['snapshot_file_sha256'], 'byte_length': head['snapshot_file_length']},
            'guard_before': guard, 'guard_commit': after_guard, 'expected_commit_receipt': core, 'new_approvals': bindings or [],
            'initialization_ref': initialization_ref, 'storage_profile_id': 'fixture-profile'}
    blobs[ref(f)['sha256']] = c(f); blobs[ref(plan)['sha256']] = c(plan)
    return plan


def publication(store, *, number=1, operation='MIGRATE_SCHEMA', decision=None, reconsiders=None, key=None, assigned_number=None):
    from editorial.schema2_migration import migrate_schema1_to_schema2
    from editorial.versioned_codec import decode_editorial_versioned, encode_editorial_versioned
    ab = json.loads(store.visible.anchor)['body']; base = ab['stable_head']; guard = ab['history_guard']
    old_raw = store.visible.blobs[base['content_head']['snapshot_file_sha256']] if operation == 'RESTORE_EXACT_HEAD' else store.visible.primary
    old = json.loads(old_raw); new = copy.deepcopy(old)
    assigned_number = number if assigned_number is None else assigned_number
    seq = ab['reserved_tx_high_watermark'] + 1 if operation != 'RESTORE_EXACT_HEAD' else None
    ids = {'approval_id': uid(100 + assigned_number) if operation == 'RECORD_DECISION' else None,
           'event_id': uid(200 + assigned_number) if operation != 'RESTORE_EXACT_HEAD' else None}
    epoch = base['content_head']['storage_epoch_id']
    q = {'request_version': 1, 'request_id': uid(number), 'production_id': old['production_id'], 'storage_epoch_id': epoch,
         'expected_head': base, 'review_session_id': uid(300 + number) if operation == 'RECORD_DECISION' else None,
         'operation': operation, 'parameters': {}}
    auth = copy.deepcopy(fixtures()['F']['authorization'])
    auth['command_grants'] = ['PROTECTED_SNAPSHOT_WRITE', 'RECOVERY' if operation == 'RESTORE_EXACT_HEAD' else operation]
    review = None; bindings = []
    if operation == 'MIGRATE_SCHEMA':
        migrated = migrate_schema1_to_schema2(decode_editorial_versioned(store.visible.primary), actor=ACTOR, at=AT, event_id=ids['event_id'])
        new = json.loads(encode_editorial_versioned(migrated.snapshot))
    elif operation == 'RECORD_DECISION':
        from editorial.schema2_model import ApprovalAuthorityEvidence, required_declaration_codes
        from editorial.approval_attestation import compute_attestation_digest
        from editorial import codec
        from editorial.current_package import compute_current_dependency_digest
        current_digest = compute_current_dependency_digest(decode_editorial_versioned(old_raw).base_snapshot, 'SCRIPT', 'fixture-review')
        key = key or {'gate': 'SCRIPT', 'policy_version': 'fixture-review', 'object_ref': old['scripts'][0]['ref'], 'dependency_digest': current_digest}
        q['parameters'] = {'decision_key': key, 'decision': decision, 'reason': 'Synthetic human decision', 'reconsiders_record_id': reconsiders}
        auth['gate_decision_grant'] = {'gate': key['gate'], 'decision': decision}
        codes = list(required_declaration_codes(key['gate'], decision))
        review = {'session_id': q['review_session_id'], 'principal_id': PRINCIPAL, 'policy_ref': auth['policy_ref'], 'decision_key': key,
                  'confirmed_codes': codes, 'review_declarations': ['Synthetic reviewed declaration'], 'reconsiders_record_id': reconsiders,
                  'server_incarnation_id': CONNECTION, 'state': 'READY'}
        a = {'id': ids['approval_id'], **key, 'decision': decision, 'actor': ACTOR, 'timestamp': AT,
             'reason': q['parameters']['reason'], 'review_declarations': review['review_declarations']}
        e = {'approval_id': a['id'], 'principal_id': PRINCIPAL, 'principal_display_name': ACTOR, 'authority_policy_id': POLICY,
             'authority_policy_version': 'fixture-v1', 'review_session_id': q['review_session_id'], 'request_id': q['request_id'],
             'declaration_codes': codes, 'attested_at': AT, 'reconsiders_record_id': reconsiders, 'attestation_digest': '0' * 64,
             'signing_key_id': None, 'signature_algorithm': None, 'signature': None}
        ev = ApprovalAuthorityEvidence(**{**e, 'declaration_codes': tuple(codes)})
        e['attestation_digest'] = compute_attestation_digest(codec._APPROVAL(a, '$'), ev)
        new['approvals'].append(a); new['approval_authority_evidence'].append(e)
        new['events'].append({'id': ids['event_id'], 'actor': ACTOR, 'at': AT, 'action': 'approval_recorded',
                              'refs': [key['object_ref']], 'reason': q['parameters']['reason'], 'error_code': None})
        new['generation'] += 1; new = sealed(new)
        bindings = [{'approval_id': a['id'], 'decision_key': key, 'decision': decision,
                     'approval_record_sha256': w.approval_wire_digest(a), 'evidence_attestation_digest': e['attestation_digest']}]
    elif operation == 'RESTORE_EXACT_HEAD':
        q['parameters'] = {'image_ref': {'sha256': base['content_head']['snapshot_file_sha256'], 'byte_length': base['content_head']['snapshot_file_length']},
                           'expected_observation': m.observation(store.visible.primary)}
    raw = c(new); image_ref = ref(new)
    head = {**base['content_head'], 'editorial_schema_version': new['editorial_schema_version'], 'generation': new['generation'],
            'snapshot_checksum': new['snapshot_checksum'], 'snapshot_file_sha256': image_ref['sha256'], 'snapshot_file_length': len(raw),
            'tx_seq': seq if seq is not None else base['content_head']['tx_seq']}
    f = {'command_version': 1, 'request': q, 'request_sha256': w.request_digest(q), 'key_id': 'fixture-key', 'principal_id': PRINCIPAL,
         'actor': ACTOR, 'at': AT, 'authorization': auth, 'assigned_ids': ids, 'storage_epoch_id': epoch, 'expected_result': head, 'review_snapshot': review}
    blobs = {image_ref['sha256']: raw}
    plan = finish_plan(q, f, head, guard, blobs, kind='REPAIR_EXACT' if operation == 'RESTORE_EXACT_HEAD' else 'PUBLISH',
                       base=base, observed=m.observation(store.visible.primary), seq=seq, bindings=bindings)
    return m.TransactionInput(plan, f, blobs)


def package_image():
    # Reuse valid existing editorial data, not duplicate/redefine its schemas.
    root = str(Path(__file__).resolve().parent)
    sys.path.insert(0, root)
    try:
        from test_editorial_snapshot_integrity import full_snapshot
        from editorial.versioned_codec import encode_editorial_versioned
        old = json.loads(encode_editorial_versioned(full_snapshot()))
    finally:
        sys.path.remove(root)
    old.update(editorial_schema_version=2, generation=1, approvals=[], events=[], approval_authority_evidence=[])
    return sealed(old)


class ModelCase(unittest.TestCase):
    def make(self, transaction=None, state=None):
        t = transaction or genesis()
        store = m.VirtualStore(state)
        model = m.TransactionModel(store, keys={'fixture-key': KEY}, authority=authority(t))
        return store, model, t

    def ready(self, *, populated=False, schema1=False):
        image = package_image() if populated else fixtures()['S']
        if schema1:
            image = dict(image); image.pop('approval_authority_evidence'); image['editorial_schema_version'] = 1; image = sealed(image)
        t = genesis(image=image, operation='IMPORT_BASELINE' if schema1 else 'INITIALIZE_EMPTY')
        s, model, t = self.make(t)
        model.execute(t)
        return s, model, t

    def authorize(self, model, transaction):
        model.authority = authority(transaction)

    def error(self, code, function, *args, **kwargs):
        with self.assertRaises(w.ProtocolError) as caught:
            function(*args, **kwargs)
        self.assertEqual(caught.exception.code, code, str(caught.exception))
        return caught.exception

    def crash_at(self, store, model, transaction, operation, when='after', *, retain=True):
        store.arm(m.Fault(operation, when))
        with self.assertRaises(m.SimulatedCrash):
            model.execute(transaction)
        store.restart(retain_unflushed=retain)
        return model

    def anchor(self, store):
        return json.loads(store.visible.anchor)['body']


class GoldenAndTransitions(ModelCase):
    def test_genesis_exact_golden_anchor_and_receipt(self):
        s, model, t = self.make()
        out = model.execute(t)
        x = fixtures()
        self.assertEqual(s.visible.primary, c(x['S']))
        self.assertEqual(s.visible.anchor, c({'body': x['A1'], 'mac': MACS['A1']}))
        self.assertEqual(out.receipt, c({'body': x['RC'], 'mac': MACS['RC']}))
        self.assertEqual([json.loads(f[8:-32]) for f in s.visible.journal], [x[n] for n in ('J0', 'J1', 'J2')])
        self.assertEqual(s.visible, s.durable)
        self.assertEqual((out.state, out.action), ('FINALIZED', 'COMMIT'))

    def test_genesis_preintent_abort_matches_literal_vector_a(self):
        s, model, t = self.make()
        self.crash_at(s, model, t, 'W3.anchor.flush')
        out = model.recover()
        self.assertEqual((out.state, out.action), ('ABORTED', 'ABORT_PREINTENT'))
        self.assertEqual(s.visible.journal[-1][-32:].hex(), MACS['JA'])
        self.assertEqual(json.loads(s.visible.journal[-1][8:-32]), fixtures()['JA'])
        self.assertEqual(self.anchor(s)['activation'], 'INITIALIZATION_ABORTED')
        self.assertIsNone(self.anchor(s)['stable_head']); self.assertIsNone(s.visible.primary)
        self.assertEqual(model.execute(t).receipt, out.receipt)

    def test_migration_exact_generation_and_order(self):
        s, model, _ = self.ready(schema1=True)
        old = s.visible.primary
        t = publication(s); self.authorize(model, t)
        out = model.execute(t); ab = self.anchor(s)
        self.assertEqual(out.state, 'FINALIZED')
        self.assertEqual(json.loads(s.visible.primary)['generation'], 2)
        self.assertEqual(json.loads(s.visible.primary)['events'][-1]['action'], 'schema_migrated')
        self.assertEqual(ab['stable_head']['content_head']['tx_seq'], 1)
        self.assertEqual(ab['reserved_tx_high_watermark'], 1)
        self.assertEqual(s.visible.backups[hashlib.sha256(old).hexdigest()], old)
        self.assertEqual([json.loads(f[8:-32])['record_type'] for f in s.visible.journal],
                         ['PREPARE', 'PUBLISH_INTENT', 'GENESIS', 'PREPARE', 'PUBLISH_INTENT', 'SNAPSHOT_COMMIT'])

    def test_each_independent_write_and_flush_observable(self):
        s, model, t = self.make()
        self.crash_at(s, model, t, 'W2.PREPARE.append', retain=False)
        self.assertEqual(len(s.visible.journal), 0)
        self.assertTrue(any(n == 'W2.PREPARE.append' for n, _ in s.events))
        self.assertIsNone(s.visible.anchor)

    def test_primary_cp_before_terminal_and_ack_after_w8(self):
        s, model, t = self.make()
        self.crash_at(s, model, t, 'W5.primary.flush')
        self.assertEqual(s.visible.primary, c(fixtures()['S']))
        self.assertEqual(len(s.visible.journal), 2)
        self.assertEqual(self.anchor(s)['pending']['phase'], 'PUBLISH_INTENT')
        self.assertNotIn(('W9.receipt.ack', 'before'), s.events)
        out = model.recover(); self.assertEqual(out.receipt[-10:], c({'body': fixtures()['RC'], 'mac': MACS['RC']})[-10:])

    def test_w8_not_yet_durable_never_acknowledged(self):
        s, model, t = self.make()
        s.arm(m.Fault('W8.anchor.flush', 'before', effect='flush_failed'))
        out = model.execute(t)
        self.assertEqual((out.state, out.receipt), ('PENDING', None))
        self.assertNotEqual(s.visible.anchor, s.durable.anchor)
        self.assertNotIn(('W9.receipt.ack', 'before'), s.events)
        self.assertEqual(model.recover().state, 'FINALIZED')
        self.assertEqual(s.visible.anchor, s.durable.anchor)

    def test_complete_unflushed_intent_reconciles_forward_if_surviving(self):
        s, model, t = self.make()
        self.crash_at(s, model, t, 'W4.INTENT.append', retain=True)
        out = model.recover()
        self.assertEqual(out.action, 'COMPLETE_FORWARD')
        self.assertEqual(len(s.visible.journal), 3)
        self.assertEqual(s.visible.primary, c(fixtures()['S']))

    def test_lost_unflushed_intent_permits_proven_abort(self):
        s, model, t = self.make()
        self.crash_at(s, model, t, 'W4.INTENT.append', retain=False)
        self.assertEqual(model.recover().action, 'ABORT_PREINTENT')
        self.assertIsNone(s.visible.primary)

    def test_complete_terminal_lag_finalizes_without_new_frame(self):
        s, model, t = self.make()
        self.crash_at(s, model, t, 'W7.COMMIT.journal.flush')
        frames = copy.deepcopy(s.visible.journal)
        self.assertEqual(model.recover().action, 'FINALIZE_TERMINAL')
        self.assertEqual(s.visible.journal, frames)

    def test_successful_state_is_read_only_reconciliation(self):
        s, model, t = self.make(); original = model.execute(t)
        state = copy.deepcopy(s.visible)
        self.assertEqual(model.recover().receipt, original.receipt)
        self.assertEqual(s.visible, state)


class IdempotencyAndPermissions(ModelCase):
    def test_identical_request_exact_receipt_before_new_live_policy(self):
        s, model, t = self.make(); out = model.execute(t); state = copy.deepcopy(s.visible)
        model.authority = replace(model.authority, live_authorizations=frozenset())
        self.assertEqual(model.execute(t).receipt, out.receipt)
        self.assertEqual(s.visible, state)

    def test_request_id_other_content_conflict_no_write(self):
        s, model, t = self.make(); model.execute(t); state = copy.deepcopy(s.visible)
        bad = copy.deepcopy(t); bad.command['request']['parameters']['draft_ref']['sha256'] = 'a' * 64
        self.error('IDEMPOTENCY_CONFLICT', model.execute, bad)
        self.assertEqual(s.visible, state)

    def test_request_id_other_principal_denied(self):
        s, model, t = self.make(); model.execute(t)
        model.authority = replace(model.authority, principal_id='windows-sid:S-1-5-99', read_principals=frozenset(['windows-sid:S-1-5-99']))
        self.error('IDEMPOTENCY_CONFLICT', model.execute, t)

    def test_lost_ack_replays_same_terminal_and_ids(self):
        s, model, t = self.make()
        self.crash_at(s, model, t, 'W9.receipt.ack', when='before')
        state = copy.deepcopy(s.visible)
        out = model.execute(t)
        self.assertEqual(out.receipt, c({'body': fixtures()['RC'], 'mac': MACS['RC']}))
        self.assertEqual(s.visible, state)

    def test_preintent_consumes_request_and_sequence_after_abort(self):
        s, model, _ = self.ready(schema1=True); t = publication(s); self.authorize(model, t)
        self.crash_at(s, model, t, 'W3.anchor.flush')
        out = model.recover(); self.assertEqual(out.state, 'ABORTED')
        self.assertEqual(self.anchor(s)['reserved_tx_high_watermark'], 1)
        self.assertEqual(json.loads(s.visible.primary)['generation'], 1)
        t2 = publication(s, number=2); self.authorize(model, t2)
        self.assertEqual(t2.plan['tx_seq'], 2)
        self.assertEqual(model.execute(t2).state, 'FINALIZED')
        self.assertEqual(json.loads(s.visible.primary)['generation'], 2)
        self.assertEqual(model.execute(t).receipt, out.receipt)

    def test_aborted_event_id_cannot_be_reused(self):
        s, model, _ = self.ready(schema1=True); t = publication(s); self.authorize(model, t)
        self.crash_at(s, model, t, 'W3.anchor.flush'); model.recover()
        t2 = publication(s, number=2, assigned_number=1)
        self.authorize(model, t2)
        self.error('IDEMPOTENCY_CONFLICT', model.execute, t2)
        self.assertIn(uid(201), model.inspect().ids)

    def test_missing_live_operation_grants_deny_without_writes(self):
        s, model, t = self.make(); model.authority = replace(model.authority, live_authorizations=frozenset())
        self.error('PERMISSION_DENIED', model.execute, t)
        self.assertEqual(s.visible, m.VirtualState()); self.assertEqual(s.events, [])

    def test_no_implicit_initialization_permission(self):
        s, model, t = self.make(); model.authority = replace(model.authority, initialize_allowed=False)
        self.error('PERMISSION_DENIED', model.execute, t)

    def test_no_automatic_anchor_after_registered_restart(self):
        s, model, t = self.make(); self.crash_at(s, model, t, 'W2.PREPARE.journal.flush')
        self.error('ANCHOR_MISSING', model.recover)
        self.error('ANCHOR_MISSING', model.execute, t)

    def test_disabled_revision_and_conflicting_request_priority(self):
        s, model, t = self.make()
        bad = copy.deepcopy(t)
        bad.command['request'].update(operation='PUBLISH_REVISION', parameters={'proposal_ref': ref({}), 'reason': 'disabled'})
        self.error('OPERATION_NOT_AVAILABLE', model.execute, bad)
        self.assertEqual(s.visible, m.VirtualState())
        model.execute(t)
        self.error('IDEMPOTENCY_CONFLICT', model.execute, bad)

    def test_partial_reconstruction_cannot_be_enabled(self):
        s, model, t = self.make()
        self.error('OPTIONAL_CAPABILITY_DISABLED', m.TransactionModel, s, keys={'fixture-key': KEY}, authority=authority(t), partial_commit_reconstruction=True)

    def test_one_writer_across_model_instances(self):
        s, model, t = self.make(); s.writer_busy = True
        other = m.TransactionModel(s, keys={'fixture-key': KEY}, authority=authority(t))
        self.error('LOCK_BUSY', other.execute, t)


class HistoryAndSessions(ModelCase):
    def decision(self, store, model, number, decision, **kwargs):
        t = publication(store, number=number, operation='RECORD_DECISION', decision=decision, **kwargs)
        self.authorize(model, t)
        return t

    def test_verified_order_uses_sequence_not_equal_timestamp(self):
        s, model, _ = self.ready(populated=True)
        first = self.decision(s, model, 1, 'approve'); model.execute(first)
        second = self.decision(s, model, 2, 'revoke'); model.execute(second)
        key = first.command['request']['parameters']['decision_key']
        latest = model.latest_verified(key)
        self.assertEqual((latest['epoch'], latest['tx_seq'], latest['binding']['decision']), (E, 2, 'revoke'))
        self.assertEqual(json.loads(s.visible.primary)['approvals'][0]['timestamp'], json.loads(s.visible.primary)['approvals'][1]['timestamp'])

    def test_each_negative_barrier_retained_and_exact_reconsideration_required(self):
        for decision in ('reject', 'revise', 'revoke'):
            with self.subTest(decision=decision):
                s, model, _ = self.ready(populated=True)
                t = self.decision(s, model, 1, decision); model.execute(t)
                old_tip = self.anchor(s)['history_guard']['barrier_tip']
                barrier = json.loads(s.visible.blobs[old_tip['sha256']])
                self.assertEqual(barrier['entries'][0]['barrier_kind'], decision.upper())
                invalid = self.decision(s, model, 2, 'approve')
                original = copy.deepcopy(s.visible)
                self.error('RECONSIDERATION_MISMATCH', model.execute, invalid)
                self.assertEqual(s.visible, original)
                valid = self.decision(s, model, 3, 'approve', reconsiders=uid(101)); model.execute(valid)
                self.assertEqual(self.anchor(s)['history_guard']['barrier_tip'], old_tip)
                key = t.command['request']['parameters']['decision_key']
                self.assertEqual(model.latest_verified(key)['binding']['approval_id'], uid(103))
                self.assertIn(old_tip['sha256'], s.visible.blobs)

    def test_old_negative_target_cannot_override_latest(self):
        s, model, _ = self.ready(populated=True)
        for n, decision in [(1, 'reject'), (2, 'revoke')]:
            model.execute(self.decision(s, model, n, decision))
        t = self.decision(s, model, 3, 'approve', reconsiders=uid(101))
        self.error('RECONSIDERATION_MISMATCH', model.execute, t)

    def test_unbound_review_invalid_after_restart(self):
        s, model, _ = self.ready(populated=True)
        t = self.decision(s, model, 1, 'approve')
        model.authority = replace(model.authority, current_incarnation_id=uid(700), live_sessions=frozenset())
        original = copy.deepcopy(s.visible)
        self.error('SESSION_INVALIDATED', model.execute, t)
        self.assertEqual(s.visible, original)

    def test_bound_intent_survives_restart_without_new_grants(self):
        s, model, _ = self.ready(populated=True)
        t = self.decision(s, model, 1, 'approve')
        self.crash_at(s, model, t, 'W4.INTENT.journal.flush')
        model.authority = replace(model.authority, current_incarnation_id=uid(700), live_sessions=frozenset(), live_authorizations=frozenset())
        self.assertEqual(model.recover().action, 'COMPLETE_FORWARD')
        self.assertEqual(model.execute(t).state, 'FINALIZED')
        self.assertEqual(len(json.loads(s.visible.primary)['approvals']), 1)

    def test_admitted_preintent_decision_aborts_after_restart(self):
        s, model, _ = self.ready(populated=True)
        t = self.decision(s, model, 1, 'approve')
        self.crash_at(s, model, t, 'W3.anchor.flush')
        model.authority = replace(model.authority, current_incarnation_id=uid(700), live_sessions=frozenset(), live_authorizations=frozenset())
        self.assertEqual(model.recover().state, 'ABORTED')
        self.assertEqual(json.loads(s.visible.primary)['approvals'], [])
        self.assertIn(uid(101), model.inspect().ids)
        self.assertIn(uid(301), model.inspect().sessions)

    def test_invalid_session_binding_rejected(self):
        s, model, _ = self.ready(populated=True)
        t = self.decision(s, model, 1, 'approve')
        t.command['review_snapshot']['session_id'] = uid(701)
        self.error('SESSION_BINDING_MISMATCH', model.execute, t)

    def test_missing_current_package_fixture_denies(self):
        s, model, _ = self.ready(populated=True)
        t = self.decision(s, model, 1, 'approve'); model.authority = replace(model.authority, verified_packages=frozenset())
        self.error('PERMISSION_DENIED', model.execute, t)

    def test_consumed_session_cannot_bind_new_request(self):
        s, model, _ = self.ready(populated=True)
        t = self.decision(s, model, 1, 'approve'); model.execute(t)
        t2 = self.decision(s, model, 2, 'revoke')
        old_session = t.command['request']['review_session_id']
        q, f = t2.command['request'], t2.command
        q['review_session_id'] = old_session
        f['review_snapshot']['session_id'] = old_session
        f['request_sha256'] = w.request_digest(q)
        # Rebuild all dependent metadata so failure is consumed session, not bad HMAC.
        blobs = dict(t2.blobs)
        plan = finish_plan(q, f, f['expected_result'], t2.plan['guard_before'], blobs, kind='PUBLISH',
                           base=t2.plan['base_head'], observed=t2.plan['observed_primary'], seq=2, bindings=t2.plan['new_approvals'])
        t2 = m.TransactionInput(plan, f, blobs); self.authorize(model, t2)
        self.error('IDEMPOTENCY_CONFLICT', model.execute, t2)

    def test_imported_approval_kept_without_inventing_order(self):
        s, first, _ = self.ready(populated=True)
        t = self.decision(s, first, 1, 'revoke'); first.execute(t)
        imported = genesis(image=json.loads(s.visible.primary), operation='IMPORT_BASELINE', epoch=uid(800), request=uid(801))
        target, model, _ = self.make(imported); model.execute(imported)
        key = t.command['request']['parameters']['decision_key']
        self.assertEqual(json.loads(target.visible.primary)['approvals'], json.loads(s.visible.primary)['approvals'])
        self.assertEqual(model.inspect().ordered, [])
        self.assertEqual(self.anchor(target)['history_guard']['continuity'], 'BASELINE_UNVERIFIED')
        self.error('UNVERIFIED_ORDERING', model.latest_verified, key)
        next_t = self.decision(target, model, 2, 'approve', reconsiders=uid(101), key=key)
        self.error('UNVERIFIED_ORDERING', model.execute, next_t)

    def test_continuity_lost_not_cleared_by_admission(self):
        image = package_image()
        guard = {'guard_version': 1, 'continuity': 'CONTINUITY_LOST', 'baseline_ref': None, 'ledger_tip': None, 'barrier_tip': None, 'lineage_tip': None}
        t = genesis(image=image, guard=guard)
        s, model, _ = self.make(t); model.execute(t)
        next_t = self.decision(s, model, 1, 'approve')
        self.error('HISTORY_CONTINUITY_LOST', model.execute, next_t)
        self.error('HISTORY_CONTINUITY_LOST', model.latest_verified, next_t.command['request']['parameters']['decision_key'])

    def test_transfer_never_authenticates_foreign_order(self):
        t = genesis(operation='TRANSFER_BASELINE', epoch=uid(801))
        s, model, _ = self.make(t); model.execute(t)
        self.assertEqual(self.anchor(s)['history_guard']['continuity'], 'BASELINE_UNVERIFIED')
        self.assertEqual(model.inspect().ordered, [])

    def test_protected_policy_recheck_before_intent_aborts_without_refreezing(self):
        s, model, t = self.make()
        original_authorize = model._authorize
        calls = []
        def recheck(command):
            calls.append(command)
            if len(calls) == 2:
                model.authority = replace(model.authority, live_authorizations=frozenset())
            return original_authorize(command)
        with patch.object(model, '_authorize', side_effect=recheck):
            out = model.execute(t)
        self.assertEqual((out.state, out.action), ('ABORTED', 'ABORT_POLICY_CHANGED'))
        self.assertEqual(json.loads(out.receipt)['body']['core']['abort_code'], 'REVALIDATION_FAILED')
        self.assertNotIn('PUBLISH_INTENT', [json.loads(f[8:-32])['record_type'] for f in s.visible.journal])


class Repair(ModelCase):
    def prepare_repair(self, missing=False):
        s, model, _ = self.ready()
        target = s.visible.primary; head = self.anchor(s)['stable_head']
        s.visible.primary = None if missing else b'corrupted physical file C'
        s.durable = copy.deepcopy(s.visible)
        t = publication(s, operation='RESTORE_EXACT_HEAD'); self.authorize(model, t)
        return s, model, t, target, head

    def test_explicit_exact_head_repair_preserves_original_head_and_order(self):
        s, model, t, target, head = self.prepare_repair()
        c_bytes = s.visible.primary
        out = model.execute(t)
        self.assertEqual(out.state, 'FINALIZED')
        self.assertEqual(s.visible.primary, target)
        self.assertEqual(self.anchor(s)['stable_head'], head)
        self.assertEqual(self.anchor(s)['reserved_tx_high_watermark'], 0)
        self.assertEqual(json.loads(out.receipt)['body']['core']['status'], 'REPAIRED')
        self.assertEqual(s.visible.forensic[hashlib.sha256(c_bytes).hexdigest()], c_bytes)
        self.assertEqual(json.loads(s.visible.journal[-1][8:-32])['record_type'], 'REPAIR_COMMIT')

    def test_missing_primary_can_be_explicitly_repaired(self):
        s, model, t, target, head = self.prepare_repair(True)
        self.assertEqual(model.execute(t).state, 'FINALIZED'); self.assertEqual(s.visible.primary, target)

    def test_repair_intent_completes_only_recorded_observation_or_target(self):
        for retain in (False, True):
            s, model, t, target, head = self.prepare_repair()
            self.crash_at(s, model, t, 'W4.INTENT.journal.flush', retain=retain)
            self.assertEqual(model.recover().action, 'COMPLETE_FORWARD')
            self.assertEqual(self.anchor(s)['stable_head'], head)
            self.assertEqual(s.visible.primary, target)

    def test_repair_changed_c_after_intent_blocks(self):
        s, model, t, target, _ = self.prepare_repair()
        self.crash_at(s, model, t, 'W4.INTENT.journal.flush')
        s.visible.primary = b'new unknown C'
        self.error('ANCHOR_MISMATCH', model.recover)
        self.assertEqual(s.visible.primary, b'new unknown C')

    def test_repair_preintent_abort_preserves_untrusted_c_and_old_head(self):
        s, model, t, target, head = self.prepare_repair()
        wrong = s.visible.primary
        self.crash_at(s, model, t, 'W3.anchor.flush')
        out = model.recover()
        self.assertEqual(out.state, 'ABORTED')
        self.assertEqual(s.visible.primary, wrong)
        self.assertEqual(self.anchor(s)['stable_head'], head)
        self.assertEqual(json.loads(out.receipt)['body']['core']['result_content_head'], head['content_head'])
        self.assertEqual(self.anchor(s)['reserved_tx_high_watermark'], 0)

    def test_stable_wrong_primary_never_automatically_restored(self):
        s, model, t, target, _ = self.prepare_repair()
        self.error('ANCHOR_MISMATCH', model.recover)
        self.assertNotEqual(s.visible.primary, target)


class FailClosed(ModelCase):
    def finalized(self):
        s, model, t = self.make(); model.execute(t)
        return s, model, t

    def test_missing_anchor(self):
        s, model, _ = self.finalized(); s.visible.anchor = None
        self.error('ANCHOR_MISSING', model.recover)

    def test_malformed_anchor(self):
        s, model, _ = self.finalized(); s.visible.anchor = b'{'
        self.error('WIRE_FORMAT', model.recover)

    def test_anchor_wrong_mac(self):
        s, model, _ = self.finalized(); a = json.loads(s.visible.anchor); a['mac'] = '0' * 64; s.visible.anchor = c(a)
        self.error('MAC_MISMATCH', model.recover)

    def test_valid_mac_mismatched_anchor_guard(self):
        s, model, _ = self.finalized(); a = json.loads(s.visible.anchor); a['body']['history_guard']['continuity'] = 'CONTINUITY_LOST'
        a['mac'] = w.anchor_mac(a['body'], KEY); s.visible.anchor = c(a)
        self.error('ANCHOR_MISMATCH', model.recover)

    def test_anchor_ahead_of_chain_not_downgraded(self):
        s, model, _ = self.finalized(); s.visible.journal.pop()
        original = s.visible.anchor
        self.error('ANCHOR_MISMATCH', model.recover); self.assertEqual(s.visible.anchor, original)

    def test_journal_mac_failure_no_magic_scan(self):
        s, model, _ = self.finalized(); f = s.visible.journal[1]; s.visible.journal[1] = f[:-1] + bytes([f[-1] ^ 1])
        original = copy.deepcopy(s.visible)
        self.error('MAC_MISMATCH', model.recover); self.assertEqual(s.visible, original)

    def test_gap_or_fork(self):
        for which in ('gap', 'fork'):
            s, model, _ = self.finalized()
            if which == 'gap':
                del s.visible.journal[1]
            else:
                j = json.loads(s.visible.journal[1][8:-32]); j['previous_record_mac'] = '0' * 64
                s.visible.journal[1] = w.encode_journal_frame(j, KEY)
            self.error('JOURNAL_TRANSITION_INVALID' if which == 'gap' else 'JOURNAL_PREFIX_MISMATCH', model.recover)

    def test_partial_frame_off_never_truncated_or_reconstructed(self):
        for index in (0, 1, 2):
            s, model, _ = self.finalized(); s.visible.journal[index] = s.visible.journal[index][:-1]
            original = copy.deepcopy(s.visible)
            self.error('JOURNAL_TAIL_UNVERIFIABLE', model.recover)
            self.assertEqual(s.visible, original)

    def test_missing_or_substituted_blob(self):
        for mode in ('missing', 'substituted'):
            s, model, t = self.finalized(); sha = t.plan['command_ref']['sha256']
            if mode == 'missing':
                del s.visible.blobs[sha]
            else:
                s.visible.blobs[sha] = b'{}'
            self.error('BLOB_MISSING' if mode == 'missing' else 'BLOB_HASH_MISMATCH', model.recover)

    def test_missing_frozen_authorization_evidence_after_intent(self):
        s, model, t = self.make(); self.crash_at(s, model, t, 'W4.INTENT.journal.flush')
        s.visible.authorization_evidence.clear()
        self.error('AUTHORIZATION_BINDING_MISMATCH', model.recover)

    def test_wrong_pending_primary_blocks_without_substitution(self):
        s, model, t = self.make(); self.crash_at(s, model, t, 'W4.INTENT.journal.flush')
        s.visible.primary = b'unknown C'
        original = copy.deepcopy(s.visible)
        self.error('ANCHOR_MISMATCH', model.recover); self.assertEqual(s.visible, original)

    def test_missing_prepared_image_blocks_forward_recovery(self):
        s, model, t = self.make(); self.crash_at(s, model, t, 'W4.INTENT.journal.flush')
        s.visible.images.clear()
        self.error('BLOB_MISSING', model.recover)

    def test_duplicate_terminal_even_new_correct_mac_is_invalid(self):
        s, model, _ = self.finalized()
        duplicate = json.loads(s.visible.journal[-1][8:-32]); duplicate['record_index'] = 3; duplicate['previous_record_mac'] = s.visible.journal[-1][-32:].hex()
        s.visible.journal.append(w.encode_journal_frame(duplicate, KEY))
        self.error('JOURNAL_TRANSITION_INVALID', model.recover)

    def test_abort_after_intent_even_with_valid_mac_is_invalid(self):
        s, model, t = self.make(); self.crash_at(s, model, t, 'W4.INTENT.journal.flush')
        ja = copy.deepcopy(fixtures()['JA']); ja['record_index'] = 2; ja['previous_record_mac'] = s.visible.journal[-1][-32:].hex()
        # The literal A blob already belongs to a different history; no discarded INTENT.
        x = fixtures(); s.visible.blobs[ref(x['L_abort'])['sha256']] = c(x['L_abort'])
        s.visible.journal.append(w.encode_journal_frame(ja, KEY))
        self.error('JOURNAL_TRANSITION_INVALID', model.recover)

    def test_terminal_without_intent_invalid_even_correct_chain_mac(self):
        s, model, _ = self.finalized()
        j = json.loads(s.visible.journal[-1][8:-32]); j['record_index'] = 1; j['previous_record_mac'] = s.visible.journal[0][-32:].hex()
        # Structural ref indices themselves already contradict the missing INTENT.
        self.error('JOURNAL_TRANSITION_INVALID', w.encode_journal_frame, j, KEY)

    def test_unknown_key_denies_no_regeneration(self):
        s, model, _ = self.finalized(); model.keys.clear()
        self.error('KEY_UNAVAILABLE', model.recover)

    def test_virtual_disk_full_and_flush_failure_pending(self):
        for operation, when, effect in [('W1.blobs.write', 'before', 'disk_full'), ('W4.INTENT.journal.flush', 'before', 'flush_failed'),
                                       ('W7.COMMIT.journal.flush', 'after', 'disk_full'), ('W8.anchor.flush', 'before', 'flush_failed')]:
            with self.subTest(operation=operation):
                s, model, t = self.make(); s.arm(m.Fault(operation, when, effect=effect))
                out = model.execute(t)
                self.assertEqual((out.state, out.receipt), ('PENDING', None))
                self.assertEqual(out.reason, 'DISK_FULL' if effect == 'disk_full' else 'FLUSH_FAILED')
                if s.visible.anchor is not None:
                    self.assertIn(model.recover().state, ('FINALIZED', 'ABORTED'))

    def test_corrupt_barrier_proof_denies_history(self):
        s, model, _ = self.ready(populated=True)
        t = publication(s, operation='RECORD_DECISION', decision='revoke'); self.authorize(model, t); model.execute(t)
        sha = self.anchor(s)['history_guard']['barrier_tip']['sha256']; del s.visible.blobs[sha]
        self.error('BLOB_MISSING', model.recover)


class RetainedEpochs(ModelCase):
    def child(self, *, lost=False, foreign=False):
        old_guard = None
        if lost:
            old_guard = {'guard_version': 1, 'continuity': 'CONTINUITY_LOST', 'baseline_ref': None, 'ledger_tip': None, 'barrier_tip': None, 'lineage_tip': None}
        old_t = genesis(guard=old_guard)
        old, model, _ = self.make(old_t)
        self.crash_at(old, model, old_t, 'W3.anchor.flush'); abort = model.recover()
        old_ab = self.anchor(old)
        epoch = uid(850)
        entry = {'production_id': P, 'machine_binding_id': M, 'storage_epoch_id': E, 'source_snapshot_ref': ref(fixtures()['S']),
                 'parent_head': old_ab['stable_head'], 'parent_guard': old_ab['history_guard'], 'parent_terminal_ref': old_ab['journal_tail'],
                 'order_status': 'UNVERIFIED' if foreign else 'VERIFIED_LOCAL_PARENT'}
        lineage = {'blob_version': 1, 'blob_type': 'LINEAGE_DELTA', 'production_id': P, 'storage_epoch_id': epoch, 'previous_ref': None, 'entries': [entry]}
        guard = {'guard_version': 1, 'continuity': 'CONTINUITY_LOST' if lost else 'CONTINUOUS',
                 'baseline_ref': None, 'ledger_tip': None, 'barrier_tip': None, 'lineage_tip': ref(lineage)}
        child = genesis(epoch=epoch, request=uid(851), guard=guard, extra={ref(lineage)['sha256']: c(lineage)}, parents={E: old.visible} if not foreign else {})
        return old, abort, child

    def test_permitted_new_epoch_after_aborted_initialization_retains_old_receipt(self):
        old, abort, child = self.child()
        s, model, _ = self.make(child); model.execute(child)
        old_request = genesis()
        self.assertEqual(model.execute(old_request).receipt, abort.receipt)
        self.assertIn(R, model.inspect().requests)
        self.assertEqual(self.anchor(s)['storage_epoch_id'], uid(850))
        self.assertEqual(self.anchor(s)['reserved_tx_high_watermark'], 0)
        self.assertEqual(len(s.visible.journal), 3)

    def test_consumed_parent_request_cannot_initialize_new_epoch(self):
        old, _, child = self.child()
        bad = genesis(epoch=uid(850), request=R, guard=child.plan['guard_before'], extra=child.blobs, parents=child.parents)
        s, model, _ = self.make(bad)
        self.error('IDEMPOTENCY_CONFLICT', model.execute, bad)
        self.assertIsNone(s.visible.anchor)

    def test_missing_parent_proof_blocks(self):
        old, _, child = self.child()
        child.parents.clear()
        s, model, _ = self.make(child)
        self.error('BLOB_MISSING', model.execute, child)

    def test_parent_fork_or_nonfinal_boundary_blocks(self):
        old, _, child = self.child()
        parent = child.parents[E]
        parent.anchor = None
        s, model, _ = self.make(child)
        self.error('ANCHOR_MISSING', model.execute, child)

    def test_lost_continuity_survives_permitted_epoch_change(self):
        _, _, child = self.child(lost=True)
        s, model, _ = self.make(child); model.execute(child)
        self.assertEqual(self.anchor(s)['history_guard']['continuity'], 'CONTINUITY_LOST')
        self.error('HISTORY_CONTINUITY_LOST', model.latest_verified, {'gate': 'SCRIPT'})

    def test_unverified_foreign_link_does_not_invent_receipt(self):
        old, _, child = self.child(foreign=True)
        s, model, _ = self.make(child); model.execute(child)
        self.assertNotIn(R, model.inspect().requests)
        self.assertEqual(model.inspect().ordered, [])

    def test_active_registered_epoch_cannot_be_reset(self):
        s, model, t = self.make(); model.execute(t)
        t2 = genesis(epoch=uid(850), request=uid(851)); self.authorize(model, t2)
        state = copy.deepcopy(s.visible)
        self.error('PLAN_INVALID', model.execute, t2)
        self.assertEqual(s.visible, state)


class FaultMatrices(ModelCase):
    def test_all_normal_barriers_before_after_both_survivor_images(self):
        base_store, _, _ = self.ready(schema1=True)
        base = copy.deepcopy(base_store.visible)
        t = publication(base_store)
        probe, model, _ = self.make(t, base); model.execute(t)
        operations = list(dict.fromkeys(name for name, when in probe.events if when == 'before'))
        required = {'W2.PREPARE.append', 'W2.PREPARE.journal.flush', 'W3.anchor.replace', 'W4.INTENT.append',
                    'W4.INTENT.journal.flush', 'W5.primary.replace', 'W6.primary.verify', 'W7.COMMIT.append',
                    'W7.COMMIT.journal.flush', 'W8.anchor.replace', 'W9.receipt.ack'}
        self.assertTrue(required.issubset(operations))
        cases = 0
        for op in operations:
            for when in ('before', 'after'):
                for retain in (False, True):
                    with self.subTest(operation=op, when=when, retain=retain):
                        s, model, _ = self.make(t, base)
                        self.crash_at(s, model, t, op, when, retain=retain)
                        observed = [json.loads(f[8:-32])['record_type'] for f in s.visible.journal[3:]]
                        has_prepare, has_intent = 'PREPARE' in observed, 'PUBLISH_INTENT' in observed
                        out = model.recover(); ab = self.anchor(s)
                        if has_intent:
                            self.assertEqual(out.state, 'FINALIZED')
                            self.assertEqual(s.visible.primary, t.blobs[t.plan['image_ref']['sha256']])
                            self.assertEqual(ab['stable_head']['content_head']['generation'], 2)
                            self.assertEqual(ab['stable_head']['content_head']['tx_seq'], 1)
                            self.assertNotIn('ABORT', [json.loads(f[8:-32])['record_type'] for f in s.visible.journal[3:]])
                        else:
                            self.assertEqual(s.visible.primary, base.primary)
                            self.assertEqual(ab['stable_head'], json.loads(base.anchor)['body']['stable_head'])
                            self.assertEqual(ab['reserved_tx_high_watermark'], 1 if has_prepare else 0)
                            self.assertEqual(out.state, 'ABORTED' if has_prepare else 'FINALIZED')
                            self.assertEqual(uid(1) in model.inspect().requests, has_prepare)
                        self.assertIsNone(ab['pending'])
                        self.assertEqual(s.visible.anchor, s.durable.anchor)
                        self.assertEqual(s.visible.journal, s.durable.journal)
                        self.assertEqual(model.recover().receipt, out.receipt)
                        cases += 1
        self.assertEqual(cases, len(operations) * 4)

    def test_all_genesis_barriers_never_recreate_missing_anchor(self):
        probe, model, t = self.make(); model.execute(t)
        operations = list(dict.fromkeys(name for name, when in probe.events if when == 'before'))
        for op in operations:
            for when in ('before', 'after'):
                with self.subTest(operation=op, when=when):
                    s, model, t = self.make()
                    self.crash_at(s, model, t, op, when, retain=False)
                    state = copy.deepcopy(s.visible)
                    if state.anchor is None:
                        self.error('ANCHOR_MISSING', model.recover)
                        self.assertEqual(s.visible, state)
                        continue
                    types = [json.loads(f[8:-32])['record_type'] for f in s.visible.journal]
                    out = model.recover()
                    if 'PUBLISH_INTENT' in types:
                        self.assertEqual(out.receipt, c({'body': fixtures()['RC'], 'mac': MACS['RC']}))
                    else:
                        self.assertEqual(out.state, 'ABORTED')
                        self.assertEqual(s.visible.journal[-1][-32:].hex(), MACS['JA'])

    def test_repeated_crashes_during_forward_recovery_all_barriers(self):
        initial, first, t = self.make(); self.crash_at(initial, first, t, 'W4.INTENT.journal.flush')
        baseline = copy.deepcopy(initial.visible)
        probe, model, _ = self.make(t, baseline); final = model.recover()
        operations = list(dict.fromkeys(name for name, when in probe.events if when == 'before'))
        for op in operations:
            for when in ('before', 'after'):
                for retain in (False, True):
                    with self.subTest(operation=op, when=when, retain=retain):
                        s, model, _ = self.make(t, baseline)
                        s.arm(m.Fault(op, when))
                        with self.assertRaises(m.SimulatedCrash):
                            model.recover()
                        s.restart(retain_unflushed=retain)
                        # A second interruption at recovery journal flush or ACK, as applicable.
                        if len(s.visible.journal) == 2:
                            s.arm(m.Fault('RECOVERY.journal.flush', 'before'))
                        else:
                            s.arm(m.Fault('W9.receipt.ack', 'before'))
                        with self.assertRaises(m.SimulatedCrash):
                            model.recover()
                        s.restart(retain_unflushed=retain)
                        out = model.recover()
                        self.assertEqual(out.receipt, final.receipt)
                        self.assertEqual(len(s.visible.journal), 3)
                        self.assertNotIn('ABORT', [json.loads(f[8:-32])['record_type'] for f in s.visible.journal])

    def test_repeated_crashes_during_abort_recovery_all_barriers(self):
        initial, first, t = self.make(); self.crash_at(initial, first, t, 'W3.anchor.flush')
        baseline = copy.deepcopy(initial.visible)
        probe, model, _ = self.make(t, baseline); final = model.recover()
        operations = list(dict.fromkeys(name for name, when in probe.events if when == 'before'))
        self.assertIn('ABORT.append', operations)
        for op in operations:
            for when in ('before', 'after'):
                for retain in (False, True):
                    with self.subTest(operation=op, when=when, retain=retain):
                        s, model, _ = self.make(t, baseline)
                        s.arm(m.Fault(op, when))
                        with self.assertRaises(m.SimulatedCrash):
                            model.recover()
                        s.restart(retain_unflushed=retain)
                        out = model.recover()
                        self.assertEqual(out.receipt, final.receipt)
                        self.assertEqual(len(s.visible.journal), 2)
                        self.assertEqual(self.anchor(s)['activation'], 'INITIALIZATION_ABORTED')
                        self.assertIsNone(s.visible.primary)

    def test_recovery_io_failure_after_intent_is_pending_without_ack(self):
        for op in ('RECOVERY.journal.flush', 'RECOVERY.intent_anchor.flush', 'W5.primary.replace', 'W7.COMMIT.append', 'W8.anchor.flush'):
            s, model, t = self.make(); self.crash_at(s, model, t, 'W4.INTENT.journal.flush')
            s.arm(m.Fault(op, 'before', effect='flush_failed'))
            out = model.recover()
            self.assertEqual((out.state, out.receipt, out.reason), ('PENDING', None, 'FLUSH_FAILED'))
            self.assertEqual(model.recover().state, 'FINALIZED')


class RepairFaultMatrix(ModelCase):
    prepare_repair = Repair.prepare_repair
    def test_all_repair_barriers_before_after_both_survivor_images(self):
        initial, _, t, target, head = self.prepare_repair()
        baseline = copy.deepcopy(initial.visible)
        probe, model, _ = self.make(t, baseline); model.execute(t)
        operations = list(dict.fromkeys(name for name, when in probe.events if when == 'before'))
        self.assertIn('W2.forensic.replace', operations)
        for op in operations:
            for when in ('before', 'after'):
                for retain in (False, True):
                    with self.subTest(operation=op, when=when, retain=retain):
                        s, model, _ = self.make(t, baseline)
                        self.crash_at(s, model, t, op, when, retain=retain)
                        types = [json.loads(f[8:-32])['record_type'] for f in s.visible.journal[3:]]
                        if 'PREPARE' not in types:
                            self.error('ANCHOR_MISMATCH', model.recover)
                            self.assertEqual(s.visible.primary, baseline.primary)
                        else:
                            out = model.recover()
                            self.assertEqual(out.state, 'FINALIZED' if 'PUBLISH_INTENT' in types else 'ABORTED')
                            self.assertEqual(s.visible.primary, target if 'PUBLISH_INTENT' in types else baseline.primary)
                        self.assertEqual(self.anchor(s)['stable_head'], head)
                        self.assertEqual(self.anchor(s)['reserved_tx_high_watermark'], 0)


class Purity(ModelCase):
    def test_import_no_os_io_network_or_randomness(self):
        import inspect
        import os
        import socket
        source = inspect.getsource(m)
        namespace = {'__name__': m.__name__, '__package__': 'editorial'}
        with (patch('builtins.open', side_effect=AssertionError('IO')), patch.object(os, 'urandom', side_effect=AssertionError('random')),
              patch.object(socket, 'socket', side_effect=AssertionError('network'))):
            exec(compile(source, '<pure-storage-model-probe>', 'exec'), namespace)

    def test_input_fixture_is_not_mutated(self):
        s, model, t = self.make(); original = copy.deepcopy(t)
        model.execute(t)
        self.assertEqual(t, original)


class AdmissionRegression(ModelCase):
    def test_grants_for_another_production_do_not_authorize_this_request(self):
        s, model, t = self.make()
        model.authority = replace(model.authority, production_id=M)
        self.error('PERMISSION_DENIED', model.execute, t)
        self.assertEqual(s.events, [])
        self.assertEqual(s.visible, m.VirtualState())

    def test_genesis_content_head_must_reserve_sequence_zero(self):
        t = genesis(); f = copy.deepcopy(t.command)
        f['expected_result']['tx_seq'] = 99
        blobs = dict(t.blobs)
        plan = finish_plan(f['request'], f, f['expected_result'], t.plan['guard_before'], blobs,
                           kind='GENESIS', base=None, observed={'state': 'MISSING'}, seq=0,
                           initialization_ref=t.plan['initialization_ref'])
        t = m.TransactionInput(plan, f, blobs, t.registration)
        s, model, _ = self.make(t)
        self.error('JOURNAL_TRANSITION_INVALID', model.execute, t)
        self.assertEqual(s.events, [])
        self.assertIsNone(s.visible.anchor)

    def test_missing_image_proof_blocks_before_recovery_mutates_anchor(self):
        s, model, t = self.make(); self.crash_at(s, model, t, 'W4.INTENT.journal.flush')
        s.visible.images.clear(); state = copy.deepcopy(s.visible)
        self.error('BLOB_MISSING', model.recover)
        self.assertEqual(s.visible, state)

    def test_known_aborted_epoch_cannot_bootstrap_in_place(self):
        s, model, t = self.make(); self.crash_at(s, model, t, 'W3.anchor.flush'); model.recover()
        other = genesis(epoch=uid(900), request=uid(901)); self.authorize(model, other)
        self.error('PLAN_INVALID', model.execute, other)

    def test_frozen_receipt_cannot_claim_other_request_id(self):
        t = genesis(); t.plan['expected_commit_receipt']['request_id'] = uid(999)
        s, model, _ = self.make(t)
        self.error('PLAN_INVALID', model.execute, t)
        self.assertEqual(s.events, [])


if __name__ == '__main__':
    unittest.main()
