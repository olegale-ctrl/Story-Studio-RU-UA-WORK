"""S2.3: adversarial verification of the unchanged S2.2 model.

Only synthetic in-memory fixtures. The receipt oracle below does not call model
inspect/recover to calculate expected state, and computes SHA/HMAC independently.
"""
from contextlib import contextmanager
from copy import deepcopy
from dataclasses import replace
import hashlib
import hmac
import json
import unittest

from editorial import storage_protocol_v1 as wire
from editorial import storage_transaction_model_v1 as model
from tests.test_storage_protocol_v1 import KEY, PRINCIPAL, CONNECTION, MACS, fixtures
from tests.test_storage_transaction_model_v1 import (
    genesis, publication, authority, uid, finish_plan, sealed, package_image,
)

SCENARIOS = {}


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')


def reference(value):
    raw = value if type(value) is bytes else canonical(value)
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'byte_length': len(raw)}


def signature(domain, raw):
    return hmac.new(KEY, b'story-studio-storage-' + domain.encode('ascii') + b'-v1\0' + raw, hashlib.sha256).digest()


def signed_body(domain, body):
    return canonical({'body': body, 'mac': signature(domain, canonical(body)).hex()})


def signed_frame(record):
    raw = canonical(record)
    header = b'SSJ1' + len(raw).to_bytes(4, 'big')
    return header + raw + signature('journal', header + raw)


def record(frame):
    return json.loads(frame[8:-32])


class AdversarialRecovery(unittest.TestCase):
    @contextmanager
    def scenario(self, **description):
        name = self._testMethodName
        SCENARIOS[name] = SCENARIOS.get(name, 0) + 1
        with self.subTest(**description):
            yield

    def fresh(self, transaction=None, state=None):
        transaction = transaction or genesis()
        store = model.VirtualStore(state)
        machine = model.TransactionModel(store, keys={'fixture-key': KEY}, authority=authority(transaction))
        return store, machine, transaction

    def prepared_base(self, *, editorial=False):
        t = genesis(image=package_image()) if editorial else genesis()
        s, machine, t = self.fresh(t)
        out = machine.execute(t)
        self.assert_receipt(s, out, t.command['request']['request_id'])
        return s, machine

    def decision(self, s, machine, number, decision, **changes):
        t = publication(s, number=number, operation='RECORD_DECISION', decision=decision, **changes)
        machine.authority = authority(t)
        return t

    def stop_at(self, s, machine, transaction, operation, when='after', retain=True):
        s.arm(model.Fault(operation, when))
        with self.assertRaises(model.SimulatedCrash):
            machine.execute(transaction)
        s.restart(retain_unflushed=retain)

    def denied_without_mutation(self, s, operation, allowed_codes):
        visible, durable = deepcopy(s.visible), deepcopy(s.durable)
        with self.assertRaises(wire.ProtocolError) as caught:
            operation()
        self.assertIn(caught.exception.code, allowed_codes)
        self.assertEqual(s.visible, visible)
        self.assertEqual(s.durable, durable)
        return caught.exception

    def assert_receipt(self, s, outcome, request_id):
        """Independent terminal/prefix/anchor/ledger oracle; includes historical receipts."""
        self.assertIn(outcome.state, ('FINALIZED', 'ABORTED'))
        self.assertIsNotNone(outcome.receipt)
        receipt = json.loads(outcome.receipt)
        self.assertEqual(canonical(receipt), outcome.receipt)
        rb = receipt['body']
        self.assertEqual(rb['core']['request_id'], request_id)
        self.assertEqual(receipt['mac'], signature('receipt', canonical(rb)).hex())
        self.assertEqual(s.visible.anchor, s.durable.anchor)
        self.assertEqual(s.visible.journal, s.durable.journal)
        self.assertEqual(s.visible.primary, s.durable.primary)
        anchor = json.loads(s.visible.anchor)
        ab = anchor['body']
        self.assertEqual(anchor['mac'], signature('anchor', canonical(ab)).hex())
        self.assertIsNone(ab['pending'])
        previous, computed_head, computed_guard, high = None, None, None, 0
        terminals, pending = {}, None
        for i, frame in enumerate(s.visible.journal):
            self.assertEqual(frame[:4], b'SSJ1')
            self.assertEqual(int.from_bytes(frame[4:8], 'big'), len(frame) - 40)
            self.assertEqual(signature('journal', frame[:-32]), frame[-32:])
            item = record(frame)
            self.assertEqual(canonical(item), frame[8:-32])
            self.assertEqual(item['record_index'], i)
            self.assertEqual(item['previous_record_mac'], previous)
            self.assertEqual(item['storage_epoch_id'], ab['storage_epoch_id'])
            jr = {'record_index': i, 'record_mac': frame[-32:].hex()}
            previous = jr['record_mac']
            pref = item['payload']['plan_ref']
            raw = s.visible.blobs[pref['sha256']]
            self.assertEqual(reference(raw), pref)
            plan = json.loads(raw)
            kind = item['record_type']
            if kind == 'PREPARE':
                self.assertIsNone(pending)
                pending = (jr, pref, None)
                if plan['tx_seq'] is not None:
                    high = max(high, plan['tx_seq'])
            elif kind == 'PUBLISH_INTENT':
                self.assertIsNotNone(pending)
                self.assertEqual(item['payload']['prepare_ref'], pending[0])
                self.assertIsNone(pending[2])
                pending = (pending[0], pref, jr)
            else:
                self.assertIn(kind, ('GENESIS', 'SNAPSHOT_COMMIT', 'REPAIR_COMMIT', 'ABORT'))
                self.assertIsNotNone(pending)
                self.assertEqual(item['payload']['prepare_ref'], pending[0])
                self.assertEqual(pref, pending[1])
                core = item['payload']['receipt_core']
                if kind == 'ABORT':
                    self.assertIsNone(pending[2])
                    self.assertEqual(core['status'], 'ABORTED_PRECOMMIT')
                    computed_guard = item['payload']['result_guard']
                else:
                    self.assertIsNotNone(pending[2])
                    self.assertEqual(item['payload']['intent_ref'], pending[2])
                    self.assertEqual(core, plan['expected_commit_receipt'])
                    computed_guard = plan['guard_commit']
                    if kind != 'REPAIR_COMMIT':
                        computed_head = {'committed_head_version': 1, 'content_head': core['result_content_head'], 'commit_ref': jr}
                terminals[i] = (jr, core, deepcopy(computed_head), deepcopy(computed_guard))
                pending = None
        self.assertIsNone(pending)
        self.assertEqual(ab['journal_tail'], {'record_index': len(s.visible.journal) - 1, 'record_mac': previous})
        self.assertEqual(ab['stable_head'], computed_head)
        self.assertEqual(ab['history_guard'], computed_guard)
        self.assertEqual(ab['reserved_tx_high_watermark'], high)
        terminal = terminals[rb['terminal_ref']['record_index']]
        self.assertEqual(rb['terminal_ref'], terminal[0])
        self.assertEqual(rb['core'], terminal[1])
        self.assertEqual(rb['result_head'], terminal[2])
        # Current anchor may be newer than a historical receipt; its verified prefix
        # must still contain that exact terminal and the corresponding ledger proof.
        ledger_ref = terminal[3]['ledger_tip']
        ledger_raw = s.visible.blobs[ledger_ref['sha256']]
        self.assertEqual(reference(ledger_raw), ledger_ref)
        entry = json.loads(ledger_raw)['entries'][0]
        self.assertEqual(entry['request_id'], request_id)
        self.assertEqual(entry['receipt_core_sha256'], hashlib.sha256(canonical(rb['core'])).hexdigest())
        if computed_head is not None and outcome.state != 'ABORTED':
            head = computed_head['content_head']
            self.assertEqual(reference(s.visible.primary), {'sha256': head['snapshot_file_sha256'], 'byte_length': head['snapshot_file_length']})

    def test_01_retries_after_each_admission_boundary(self):
        phases = [('W3.anchor.flush', 'ABORTED', 'ABORT'), ('W4.INTENT.journal.flush', 'FINALIZED', 'GENESIS'),
                  ('W7.COMMIT.journal.flush', 'FINALIZED', 'GENESIS'), ('W9.receipt.ack', 'FINALIZED', 'GENESIS')]
        for phase, state, terminal in phases:
            for when in ('before', 'after'):
                with self.scenario(phase=phase, when=when):
                    s, machine, t = self.fresh()
                    self.stop_at(s, machine, t, phase, when)
                    out = machine.execute(t)
                    self.assertEqual(out.state, state)
                    self.assertEqual(record(s.visible.journal[-1])['record_type'], terminal)
                    self.assertEqual(len(s.visible.journal), 2 if terminal == 'ABORT' else 3)
                    self.assert_receipt(s, out, t.command['request']['request_id'])
                    before = deepcopy(s.visible)
                    self.assertEqual(machine.execute(t).receipt, out.receipt)
                    self.assertEqual(s.visible, before)

    def test_02_principal_session_policy_and_request_changes_between_retries(self):
        for phase in ('W3.anchor.flush', 'W4.INTENT.journal.flush', 'W7.COMMIT.journal.flush', 'W9.receipt.ack'):
            for change in ('principal', 'session', 'bytes', 'live_policy'):
                with self.scenario(phase=phase, change=change):
                    s, machine = self.prepared_base(editorial=True)
                    t = self.decision(s, machine, 1, 'approve')
                    self.stop_at(s, machine, t, phase)
                    retry = deepcopy(t)
                    if change == 'principal':
                        other = 'windows-sid:S-1-5-99'
                        machine.authority = replace(machine.authority, principal_id=other, read_principals=frozenset([other]))
                    elif change == 'session':
                        retry.command['request']['review_session_id'] = uid(999)
                    elif change == 'bytes':
                        retry.command['request']['parameters']['reason'] = 'Different request bytes'
                    else:
                        machine.authority = replace(machine.authority, live_authorizations=frozenset())
                    if change == 'live_policy':
                        out = machine.execute(retry)
                        self.assertEqual(out.state, 'ABORTED' if phase == 'W3.anchor.flush' else 'FINALIZED')
                        self.assert_receipt(s, out, t.command['request']['request_id'])
                    else:
                        self.denied_without_mutation(s, lambda: machine.execute(retry), {'IDEMPOTENCY_CONFLICT', 'PERMISSION_DENIED'})

    def test_03_restart_invalid_unbound_and_bound_preintent_sessions(self):
        for bound in (False, True):
            with self.scenario(bound=bound):
                s, machine = self.prepared_base(editorial=True)
                t = self.decision(s, machine, 1, 'approve')
                if bound:
                    self.stop_at(s, machine, t, 'W3.anchor.flush')
                machine.authority = replace(machine.authority, current_incarnation_id=uid(998), live_sessions=frozenset())
                if bound:
                    out = machine.execute(t)
                    self.assertEqual(out.state, 'ABORTED')
                    self.assertEqual(json.loads(s.visible.primary)['approvals'], [])
                    self.assert_receipt(s, out, t.command['request']['request_id'])
                else:
                    self.denied_without_mutation(s, lambda: machine.execute(t), {'SESSION_INVALIDATED'})

    def test_04_intent_forward_completion_never_reauthorizes(self):
        for phase in ('W4.INTENT.journal.flush', 'W5.primary.replace', 'W7.COMMIT.append'):
            for retain in (False, True):
                with self.scenario(phase=phase, retain=retain):
                    s, machine = self.prepared_base(editorial=True)
                    t = self.decision(s, machine, 1, 'approve')
                    self.stop_at(s, machine, t, phase, retain=retain)
                    machine.authority = replace(machine.authority, current_incarnation_id=uid(998), live_sessions=frozenset(),
                                                live_authorizations=frozenset(), verified_packages=frozenset())
                    out = machine.recover()
                    self.assertEqual(out.state, 'FINALIZED')
                    self.assertEqual(json.loads(s.visible.primary)['approvals'][-1]['id'], uid(101))
                    self.assert_receipt(s, out, uid(1))
                    self.assertNotIn('ABORT', [record(frame)['record_type'] for frame in s.visible.journal])

    def test_05_multiple_crashes_inside_abort_and_forward_recovery(self):
        schedules = [('W3.anchor.flush', ['ABORT.append', 'W8.anchor.replace', 'W9.receipt.ack'], 'ABORTED'),
                     ('W4.INTENT.journal.flush', ['RECOVERY.intent_anchor.replace', 'W5.primary.replace', 'W7.COMMIT.append', 'W8.anchor.replace', 'W9.receipt.ack'], 'FINALIZED')]
        for admission, schedule, state in schedules:
            for when in ('before', 'after'):
                for retain in (False, True):
                    with self.scenario(admission=admission, when=when, retain=retain):
                        s, machine, t = self.fresh(); self.stop_at(s, machine, t, admission)
                        for operation in schedule:
                            s.arm(model.Fault(operation, when))
                            with self.assertRaises(model.SimulatedCrash):
                                machine.recover()
                            s.restart(retain_unflushed=retain)
                        out = machine.recover()
                        self.assertEqual(out.state, state)
                        self.assert_receipt(s, out, t.command['request']['request_id'])
                        self.assertEqual(s.visible.journal[-1][-32:].hex(), MACS['JA' if state == 'ABORTED' else 'J2'])

    def test_06_type_substitution_with_correct_hash_and_valid_macs(self):
        for wrong_kind in ('ledger', 'content_head'):
            with self.scenario(wrong_kind=wrong_kind):
                s, machine, t = self.fresh(); self.stop_at(s, machine, t, 'W3.anchor.flush')
                x = fixtures()
                replacement = x['L0'] if wrong_kind == 'ledger' else x['H']
                replacement_ref = reference(replacement)
                s.visible.blobs[replacement_ref['sha256']] = canonical(replacement)
                j = record(s.visible.journal[0]); j['payload']['plan_ref'] = replacement_ref
                s.visible.journal[0] = signed_frame(j)
                ab = json.loads(s.visible.anchor)['body']
                ab['pending']['plan_ref'] = replacement_ref
                ab['pending']['prepare_ref']['record_mac'] = s.visible.journal[0][-32:].hex()
                ab['journal_tail']['record_mac'] = s.visible.journal[0][-32:].hex()
                s.visible.anchor = signed_body('anchor', ab)
                self.assertEqual(reference(s.visible.blobs[replacement_ref['sha256']]), replacement_ref)
                self.denied_without_mutation(s, machine.recover, {'BLOB_TYPE_MISMATCH'})

    def test_07_valid_mac_anchor_and_journal_contradictions(self):
        for change in ('guard', 'reserved_sequence', 'tail_mac', 'stable_head_generation'):
            with self.scenario(change=change):
                s, machine, t = self.fresh(); out = machine.execute(t)
                ab = json.loads(s.visible.anchor)['body']
                if change == 'guard':
                    ab['history_guard']['continuity'] = 'CONTINUITY_LOST'
                elif change == 'reserved_sequence':
                    ab['reserved_tx_high_watermark'] = 7
                elif change == 'tail_mac':
                    ab['journal_tail']['record_mac'] = s.visible.journal[0][-32:].hex()
                else:
                    ab['stable_head']['content_head']['generation'] = 2
                s.visible.anchor = signed_body('anchor', ab)
                self.assertEqual(json.loads(s.visible.anchor)['mac'], signature('anchor', canonical(ab)).hex())
                for frame in s.visible.journal:
                    self.assertEqual(frame[-32:], signature('journal', frame[:-32]))
                self.denied_without_mutation(s, machine.recover, {'ANCHOR_MISMATCH', 'JOURNAL_PREFIX_MISMATCH'})

    def test_08_approval_event_and_sequence_reuse(self):
        for field in ('approval_id', 'event_id', 'tx_seq'):
            with self.scenario(field=field):
                s, machine = self.prepared_base(editorial=True)
                first = self.decision(s, machine, 1, 'approve'); machine.execute(first)
                fresh = self.decision(s, machine, 2, 'revoke')
                f, plan, blobs = deepcopy(fresh.command), deepcopy(fresh.plan), dict(fresh.blobs)
                if field == 'tx_seq':
                    f['expected_result']['tx_seq'] = 1
                else:
                    f['assigned_ids'][field] = first.command['assigned_ids'][field]
                    image = json.loads(blobs[plan['image_ref']['sha256']])
                    if field == 'event_id':
                        image['events'][-1]['id'] = f['assigned_ids']['event_id']
                    # Approval ID reuse is rejected before image dereference by the
                    # reservation set; do not forge a second editorial attestation.
                    image = sealed(image)
                    ir = reference(image); blobs[ir['sha256']] = canonical(image)
                    f['expected_result'].update(snapshot_file_sha256=ir['sha256'], snapshot_file_length=ir['byte_length'], snapshot_checksum=image['snapshot_checksum'])
                seq = 1 if field == 'tx_seq' else 2
                plan = finish_plan(f['request'], f, f['expected_result'], plan['guard_before'], blobs, kind='PUBLISH',
                                   base=plan['base_head'], observed=plan['observed_primary'], seq=seq, bindings=plan['new_approvals'])
                retry = model.TransactionInput(plan, f, blobs); machine.authority = authority(retry)
                self.denied_without_mutation(s, lambda: machine.execute(retry), {'IDEMPOTENCY_CONFLICT', 'PLAN_INVALID', 'EDITORIAL_WIRE_ERROR'})

    def test_09_historical_approve_retry_never_revives_revoked_current_decision(self):
        with self.scenario(path="historical_receipt_and_stale_primary"):
            s, machine = self.prepared_base(editorial=True)
            approve = self.decision(s, machine, 1, 'approve'); old = machine.execute(approve)
            old_image = s.visible.primary
            revoke = self.decision(s, machine, 2, 'revoke'); revocation = machine.execute(revoke)
            state = deepcopy(s.visible)
            historical = machine.execute(approve)
            self.assertEqual(historical.receipt, old.receipt)
            self.assert_receipt(s, historical, uid(1))
            self.assertEqual(s.visible, state)
            self.assertEqual(json.loads(s.visible.primary)['approvals'][-1]['decision'], 'revoke')
            key = approve.command['request']['parameters']['decision_key']
            latest = machine.latest_verified(key)
            self.assertEqual((latest['tx_seq'], latest['binding']['approval_id'], latest['binding']['decision']), (2, uid(102), 'revoke'))
            # Installing the old bytes cannot make that historical receipt current again.
            s.visible.primary = old_image
            self.denied_without_mutation(s, lambda: machine.execute(approve), {'ANCHOR_MISMATCH'})

        with self.scenario(path='fresh_ids_cannot_skip_revoke_reconsideration'):
            s.visible = deepcopy(state)
            retry = self.decision(s, machine, 3, 'approve')
            self.denied_without_mutation(s, lambda: machine.execute(retry), {'RECONSIDERATION_MISMATCH'})
        with self.scenario(path='old_approve_import_is_history_only'):
            imported = genesis(image=json.loads(old_image), operation='IMPORT_BASELINE', epoch=uid(820), request=uid(821))
            target, imported_machine, imported = self.fresh(imported)
            out = imported_machine.execute(imported)
            self.assert_receipt(target, out, uid(821))
            self.assertEqual(json.loads(target.visible.anchor)['body']['history_guard']['continuity'], 'BASELINE_UNVERIFIED')
            self.denied_without_mutation(target, lambda: imported_machine.latest_verified(key), {'UNVERIFIED_ORDERING'})

    def test_10_old_backup_primary_substitution_cannot_auto_rollback(self):
        for operation in ('recover', 'historical_retry'):
            with self.scenario(operation=operation):
                s, machine = self.prepared_base(editorial=True)
                approve = self.decision(s, machine, 1, 'approve'); machine.execute(approve)
                revoke = self.decision(s, machine, 2, 'revoke'); machine.execute(revoke)
                backup_ref = reference(canonical(json.loads(s.visible.backups[revoke.plan['observed_primary']['file_ref']['sha256']])))
                s.visible.primary = s.visible.backups[backup_ref['sha256']]
                call = machine.recover if operation == 'recover' else lambda: machine.execute(approve)
                self.denied_without_mutation(s, call, {'ANCHOR_MISMATCH'})

    def test_11_every_partial_terminal_prefix_blocks_with_capability_off(self):
        s, machine, t = self.fresh(); machine.execute(t)
        baseline = deepcopy(s.visible)
        frame = baseline.journal[-1]
        # Keep a nonempty torn suffix, including all 1..N-1 GENESIS frame lengths.
        for end in range(1, len(frame)):
            with self.scenario(prefix_length=end):
                damaged = deepcopy(baseline)
                damaged.journal[-1] = frame[:end]
                store, machine, _ = self.fresh(t, damaged)
                self.denied_without_mutation(store, machine.recover, {'JOURNAL_TAIL_UNVERIFIABLE'})
        self.assertEqual(len(frame), 1572)
        self.assertEqual(baseline.journal[-1][-32:].hex(), MACS['J2'])

        # Actual SNAPSHOT_COMMIT and REPAIR_COMMIT boundaries in addition to the
        # exhaustive GENESIS prefixes above. These fixtures never touch files.
        for terminal_type in ('SNAPSHOT_COMMIT', 'REPAIR_COMMIT'):
            if terminal_type == 'SNAPSHOT_COMMIT':
                source = fixtures()['S']
                source.pop('approval_authority_evidence')
                source['editorial_schema_version'] = 1
                initial = genesis(image=sealed(source), operation='IMPORT_BASELINE')
                store, machine, initial = self.fresh(initial); machine.execute(initial)
                transaction = publication(store, number=9)
            else:
                store, machine, initial = self.fresh(); machine.execute(initial)
                store.visible.primary = b'synthetic damaged C'
                store.durable = deepcopy(store.visible)
                transaction = publication(store, number=9, operation='RESTORE_EXACT_HEAD')
            machine.authority = authority(transaction)
            out = machine.execute(transaction)
            self.assert_receipt(store, out, uid(9))
            self.assertEqual(record(store.visible.journal[-1])['record_type'], terminal_type)
            baseline = deepcopy(store.visible)
            frame = baseline.journal[-1]
            lengths = sorted({1, 4, 7, 8, 9, len(frame) // 2, len(frame) - 33, len(frame) - 32, len(frame) - 31, len(frame) - 1})
            for end in lengths:
                with self.scenario(terminal_type=terminal_type, prefix_length=end):
                    damaged = deepcopy(baseline); damaged.journal[-1] = frame[:end]
                    broken, reader, _ = self.fresh(transaction, damaged)
                    self.denied_without_mutation(broken, reader.recover, {'JOURNAL_TAIL_UNVERIFIABLE'})
        with self.scenario(terminal_type='capability_enable_attempt'):
            self.denied_without_mutation(broken, lambda: model.TransactionModel(broken, keys={'fixture-key': KEY},
                authority=authority(transaction), partial_commit_reconstruction=True), {'OPTIONAL_CAPABILITY_DISABLED'})

    def test_12_each_successful_receipt_has_terminal_and_final_anchor(self):
        for phase in ('W3.anchor.flush', 'W4.INTENT.journal.flush', 'W5.primary.flush', 'W7.COMMIT.journal.flush', 'W8.anchor.flush', 'W9.receipt.ack'):
            for retain in (False, True):
                with self.scenario(phase=phase, retain=retain):
                    s, machine, t = self.fresh()
                    self.stop_at(s, machine, t, phase, when='after', retain=retain)
                    out = machine.recover()
                    self.assert_receipt(s, out, t.command['request']['request_id'])
                    if out.state == 'FINALIZED':
                        self.assertEqual(out.receipt, canonical({'body': fixtures()['RC'], 'mac': MACS['RC']}))
                    else:
                        self.assertEqual(s.visible.journal[-1][-32:].hex(), MACS['JA'])


    def test_13_retained_parent_epoch_must_match_authenticated_parent_context(self):
        with self.scenario(proof='retained_parent_epoch_alias'):
            parent, parent_machine, parent_transaction = self.fresh()
            self.stop_at(parent, parent_machine, parent_transaction, 'W3.anchor.flush')
            abort = parent_machine.recover()
            self.assert_receipt(parent, abort, parent_transaction.command['request']['request_id'])
            parent_anchor = json.loads(parent.visible.anchor)['body']
            parent_epoch = parent_anchor['storage_epoch_id']
            alias_epoch, child_epoch = uid(920), uid(921)
            entry = {'production_id': parent_anchor['production_id'], 'machine_binding_id': parent_anchor['machine_binding_id'],
                     'storage_epoch_id': alias_epoch, 'source_snapshot_ref': reference(fixtures()['S']),
                     'parent_head': None, 'parent_guard': parent_anchor['history_guard'],
                     'parent_terminal_ref': parent_anchor['journal_tail'], 'order_status': 'VERIFIED_LOCAL_PARENT'}
            lineage = {'blob_version': 1, 'blob_type': 'LINEAGE_DELTA', 'production_id': entry['production_id'],
                       'storage_epoch_id': child_epoch, 'previous_ref': None, 'entries': [entry]}
            lineage_ref = reference(lineage)
            guard = {'guard_version': 1, 'continuity': 'CONTINUOUS', 'baseline_ref': None, 'ledger_tip': None,
                     'barrier_tip': None, 'lineage_tip': lineage_ref}
            child = genesis(epoch=child_epoch, request=uid(922), guard=guard,
                            extra={lineage_ref['sha256']: canonical(lineage)}, parents={alias_epoch: deepcopy(parent.visible)})
            store, child_machine, _ = self.fresh(child)
            self.assertNotEqual(parent_epoch, entry['storage_epoch_id'])
            self.assertEqual(record(parent.visible.journal[-1])['storage_epoch_id'], parent_epoch)
            self.assertEqual(entry['parent_terminal_ref']['record_mac'], parent.visible.journal[-1][-32:].hex())
            # Parent MACs are genuine, but authenticate E, not the alleged alias E'.
            # S1 §2 JournalRef context / §9 / §10 require the exact parent epoch.
            before = deepcopy(store.visible)
            try:
                result = child_machine.execute(child)
            except wire.ProtocolError as error:
                self.assertIn(error.code, {'EPOCH_MISMATCH', 'UNVERIFIED_ORDERING', 'PROTECTION_INVALID', 'JOURNAL_TRANSITION_INVALID'})
                self.assertEqual(store.visible, before)
            else:
                self.fail('S2.3 DEFECT: wrong retained parent epoch accepted: '
                          f'claimed={alias_epoch}, authenticated={parent_epoch}, '
                          f'outcome={result.state}, journal_frames={len(store.visible.journal)}, '
                          f'receipt_present={result.receipt is not None}')


def tearDownModule():
    print('S2.3 parameterized scenarios executed:', sum(SCENARIOS.values()))
    print('S2.3 scenario counts by test:', json.dumps(SCENARIOS, sort_keys=True))


if __name__ == '__main__':
    unittest.main()
