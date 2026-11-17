"""E01.3.7.2 approval decision history and revocation projection tests."""
import copy
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import subprocess
import sys
import unittest

from editorial import model as m
from editorial.approval_history import (
    ApprovalHistoryDiagnostic as Diagnostic,
    ApprovalHistoryState as State,
    evaluate_approval_history,
    evaluate_current_approval_history,
)
from editorial.codec import encode_snapshot
from editorial.current_package import CurrentPackageError, compute_current_dependency_digest
from editorial.graph import GraphValidationError
from editorial.snapshot_checksum import SnapshotChecksumError
from test_editorial_approval_consistency import (
    add_script_two,
    matching_approval,
    snapshot,
    with_approvals,
)
from test_editorial_codec import ID, ref


AT1 = '2026-11-05T10:00:00Z'
AT2 = '2026-11-05T11:00:00Z'
AT3 = '2026-11-05T12:00:00Z'


def uid(number):
    return f'{number:08x}-0000-0000-0000-000000000001'


def history_snapshot(decisions, gate='SCRIPT', policy='policy-v1'):
    value = snapshot()
    records = []
    for index, item in enumerate(decisions, 1):
        decision, timestamp = item[:2]
        actor = item[2] if len(item) > 2 else 'Owner'
        reason = item[3] if len(item) > 3 else 'Recorded decision'
        record = matching_approval(
            value, gate, policy, decision, approval_id=uid(index))
        records.append(replace(record, timestamp=timestamp, actor=actor, reason=reason))
    value = with_approvals(value, records)
    target = value.active_selections.script if gate == 'SCRIPT' else value.active_selections.scene_plan
    digest = compute_current_dependency_digest(value, gate, policy)
    return value, target, digest, tuple(records)


def historical(value, gate='SCRIPT', policy='policy-v1', target=None, digest=None):
    if target is None:
        target = value.active_selections.script if gate == 'SCRIPT' else value.active_selections.scene_plan
    if digest is None:
        digest = compute_current_dependency_digest(value, gate, policy)
    return evaluate_approval_history(value, gate, policy, target, digest)


class ApprovalHistoryTests(unittest.TestCase):
    def test_no_records_for_exact_key(self):
        value = with_approvals(snapshot(), ())
        result = historical(value)
        self.assertIs(result.state, State.NO_DECISION)
        self.assertEqual(result.record_ids, ())
        self.assertIsNone(result.latest_record)
        self.assertIsNone(result.decision)

    def test_single_approve(self):
        value, _, _, records = history_snapshot(((m.ApprovalDecision.APPROVE, AT1),))
        result = historical(value)
        self.assertIs(result.state, State.RECORDED_APPROVE)
        self.assertEqual(result.latest_record, records[0])
        self.assertFalse(hasattr(result, 'approved'))
        self.assertFalse(hasattr(result, 'ready'))

    def test_single_reject(self):
        value, _, _, _ = history_snapshot(((m.ApprovalDecision.REJECT, AT1),))
        self.assertIs(historical(value).state, State.RECORDED_REJECT)

    def test_single_revise(self):
        value, _, _, _ = history_snapshot(((m.ApprovalDecision.REVISE, AT1),))
        self.assertIs(historical(value).state, State.RECORDED_REVISE)

    def test_single_revoke(self):
        value, _, _, _ = history_snapshot(((m.ApprovalDecision.REVOKE, AT1),))
        self.assertIs(historical(value).state, State.RECORDED_REVOKE)

    def test_approve_then_revoke(self):
        value, _, _, records = history_snapshot((
            (m.ApprovalDecision.APPROVE, AT1),
            (m.ApprovalDecision.REVOKE, AT2),
        ))
        result = historical(value)
        self.assertIs(result.state, State.RECORDED_REVOKE)
        self.assertEqual(result.latest_record, records[1])

    def test_approve_then_reject(self):
        value, _, _, _ = history_snapshot((
            (m.ApprovalDecision.APPROVE, AT1),
            (m.ApprovalDecision.REJECT, AT2),
        ))
        self.assertIs(historical(value).state, State.RECORDED_REJECT)

    def test_approve_then_revise(self):
        value, _, _, _ = history_snapshot((
            (m.ApprovalDecision.APPROVE, AT1),
            (m.ApprovalDecision.REVISE, AT2),
        ))
        self.assertIs(historical(value).state, State.RECORDED_REVISE)

    def test_revoke_then_newer_approve(self):
        value, _, _, records = history_snapshot((
            (m.ApprovalDecision.REVOKE, AT1),
            (m.ApprovalDecision.APPROVE, AT2),
        ))
        result = historical(value)
        self.assertIs(result.state, State.RECORDED_APPROVE)
        self.assertEqual(result.latest_record, records[1])
        self.assertFalse(hasattr(result, 'human_review_verified'))

    def test_sequential_approves_select_latest_timestamp(self):
        value, _, _, records = history_snapshot((
            (m.ApprovalDecision.APPROVE, AT1),
            (m.ApprovalDecision.APPROVE, AT2),
            (m.ApprovalDecision.APPROVE, AT3),
        ))
        self.assertEqual(historical(value).latest_record, records[2])

    def test_repeated_same_decision_is_preserved_as_history(self):
        value, _, _, records = history_snapshot((
            (m.ApprovalDecision.REJECT, AT1),
            (m.ApprovalDecision.REJECT, AT2),
        ))
        result = historical(value)
        self.assertEqual(result.record_ids, tuple(record.id for record in records))
        self.assertIs(result.state, State.RECORDED_REJECT)

    def test_array_order_is_not_chronology(self):
        value, _, _, records = history_snapshot((
            (m.ApprovalDecision.REVOKE, AT3),
            (m.ApprovalDecision.APPROVE, AT1),
            (m.ApprovalDecision.REJECT, AT2),
        ))
        result = historical(value)
        self.assertIs(result.state, State.RECORDED_REVOKE)
        self.assertEqual(result.latest_record, records[0])
        self.assertEqual(result.record_ids, tuple(record.id for record in records))

    def test_conflicting_decisions_at_same_timestamp_are_ambiguous(self):
        value, _, _, _ = history_snapshot((
            (m.ApprovalDecision.APPROVE, AT2),
            (m.ApprovalDecision.REVOKE, AT2),
        ))
        result = historical(value)
        self.assertIs(result.state, State.AMBIGUOUS_HISTORY)
        self.assertIsNone(result.latest_record)
        self.assertIsNone(result.decision)
        self.assertEqual(result.diagnostics,
                         (Diagnostic.CONFLICTING_DECISIONS_SAME_TIMESTAMP,))

    def test_equivalent_same_decisions_at_same_timestamp_are_safely_collapsed(self):
        value, _, _, _ = history_snapshot((
            (m.ApprovalDecision.APPROVE, AT2),
            (m.ApprovalDecision.APPROVE, AT2),
        ))
        result = historical(value)
        self.assertIs(result.state, State.RECORDED_APPROVE)
        self.assertIs(result.decision, m.ApprovalDecision.APPROVE)
        self.assertIsNone(result.latest_record)
        self.assertEqual(result.diagnostics,
                         (Diagnostic.EQUIVALENT_DECISIONS_SAME_TIMESTAMP,))

    def test_same_decision_same_timestamp_different_metadata_is_ambiguous(self):
        value, _, _, _ = history_snapshot((
            (m.ApprovalDecision.APPROVE, AT2, 'Owner A', 'Reason A'),
            (m.ApprovalDecision.APPROVE, AT2, 'Owner B', 'Reason B'),
        ))
        result = historical(value)
        self.assertIs(result.state, State.AMBIGUOUS_HISTORY)
        self.assertIs(result.decision, m.ApprovalDecision.APPROVE)
        self.assertEqual(result.diagnostics,
                         (Diagnostic.NON_EQUIVALENT_RECORDS_SAME_TIMESTAMP,))

    def test_policy_versions_are_independent_exact_keys(self):
        value = snapshot()
        first = matching_approval(value, 'SCRIPT', 'policy-v1', approval_id=uid(1))
        second = matching_approval(value, 'SCRIPT', 'політика-v2',
                                   m.ApprovalDecision.REJECT, uid(2))
        first = replace(first, timestamp=AT1)
        second = replace(second, timestamp=AT2)
        value = with_approvals(value, (first, second))
        self.assertIs(historical(value, policy='policy-v1').state,
                      State.RECORDED_APPROVE)
        self.assertIs(historical(value, policy='політика-v2').state,
                      State.RECORDED_REJECT)

    def test_exact_target_refs_are_independent_keys(self):
        value, target, digest, records = history_snapshot(
            ((m.ApprovalDecision.APPROVE, AT1),))
        other = replace(records[0], id=uid(2), object_ref=value.active_selections.scene_plan,
                        decision=m.ApprovalDecision.REJECT, timestamp=AT2)
        value = with_approvals(value, (records[0], other))
        result = evaluate_approval_history(value, 'SCRIPT', 'policy-v1', target, digest)
        self.assertIs(result.state, State.RECORDED_APPROVE)
        self.assertEqual(result.record_ids, (records[0].id,))

    def test_dependency_digests_are_independent_keys(self):
        value, target, digest, records = history_snapshot(
            ((m.ApprovalDecision.APPROVE, AT1),))
        other = replace(records[0], id=uid(2), dependency_digest='0' * 64,
                        decision=m.ApprovalDecision.REVOKE, timestamp=AT2)
        value = with_approvals(value, (records[0], other))
        result = evaluate_approval_history(value, 'SCRIPT', 'policy-v1', target, digest)
        self.assertIs(result.state, State.RECORDED_APPROVE)

    def test_gates_are_independent_keys(self):
        script, _, _, records = history_snapshot(
            ((m.ApprovalDecision.APPROVE, AT1),), gate='SCRIPT')
        scenes_record = matching_approval(
            script, 'SCENES', 'policy-v1', m.ApprovalDecision.REJECT, uid(2))
        scenes_record = replace(scenes_record, timestamp=AT2)
        value = with_approvals(script, (records[0], scenes_record))
        self.assertIs(historical(value, 'SCRIPT').state, State.RECORDED_APPROVE)
        self.assertIs(historical(value, 'SCENES').state, State.RECORDED_REJECT)

    def test_historical_key_survives_active_switch(self):
        original, old_target, old_digest, records = history_snapshot(
            ((m.ApprovalDecision.APPROVE, AT1),))
        changed = with_approvals(snapshot(add_script_two), records)
        result = evaluate_approval_history(
            changed, 'SCRIPT', 'policy-v1', old_target, old_digest)
        self.assertIs(result.state, State.RECORDED_APPROVE)
        self.assertIs(evaluate_current_approval_history(
            changed, 'SCRIPT', 'policy-v1').state, State.NO_DECISION)

    def test_return_to_revoked_coherent_chain_stays_revoked(self):
        value, _, _, records = history_snapshot((
            (m.ApprovalDecision.APPROVE, AT1),
            (m.ApprovalDecision.REVOKE, AT2),
        ))

        def history(wire_value):
            script = copy.deepcopy(wire_value['scripts'][0])
            script['ref'] = ref('script', 2)
            script['segments'][0]['text'] += ' Historical alternative'
            wire_value['scripts'].append(script)

        returned = with_approvals(snapshot(history), records)
        result = evaluate_current_approval_history(returned, 'SCRIPT', 'policy-v1')
        self.assertIs(result.state, State.RECORDED_REVOKE)

    def test_current_script(self):
        value, _, _, _ = history_snapshot(((m.ApprovalDecision.APPROVE, AT1),))
        self.assertIs(evaluate_current_approval_history(
            value, 'SCRIPT', 'policy-v1').state, State.RECORDED_APPROVE)

    def test_current_scenes(self):
        value, _, _, _ = history_snapshot(
            ((m.ApprovalDecision.REVISE, AT1),), gate='SCENES')
        self.assertIs(evaluate_current_approval_history(
            value, 'SCENES', 'policy-v1').state, State.RECORDED_REVISE)

    def test_current_editorial_handoff(self):
        value, _, _, _ = history_snapshot(
            ((m.ApprovalDecision.REJECT, AT1),), gate='HANDOFF')
        result = evaluate_current_approval_history(value, 'HANDOFF', 'policy-v1')
        self.assertIs(result.state, State.RECORDED_REJECT)
        self.assertFalse(hasattr(result, 'ready'))

    def test_checksum_mismatch_blocks_projection(self):
        value, target, digest, _ = history_snapshot(
            ((m.ApprovalDecision.APPROVE, AT1),))
        corrupt = replace(value, snapshot_checksum='0' * 64)
        with self.assertRaises(SnapshotChecksumError):
            evaluate_approval_history(corrupt, 'SCRIPT', 'policy-v1', target, digest)

    def test_graph_failure_blocks_projection(self):
        def change(wire_value):
            wire_value['candidates'][0]['source_refs'][0] = ref('source', 99)
        value = snapshot(after=change)
        with self.assertRaises(GraphValidationError):
            evaluate_approval_history(
                value, 'SCRIPT', 'policy-v1', value.active_selections.script, '0' * 64)

    def test_missing_current_chain_blocks_current_projection(self):
        value = snapshot(after=lambda wire_value:
            wire_value['active_refs'].update(script=None))
        with self.assertRaises(CurrentPackageError):
            evaluate_current_approval_history(value, 'SCRIPT', 'policy-v1')

    def test_unicode_reason_and_actor_are_preserved(self):
        value, _, _, records = history_snapshot((
            (m.ApprovalDecision.APPROVE, AT1,
             'Рецензент Україна 😀', 'Причина е\u0301'),
        ))
        result = historical(value)
        self.assertEqual(result.latest_record.actor, records[0].actor)
        self.assertEqual(result.latest_record.reason, records[0].reason)

    def test_repeated_calls_are_deterministic(self):
        value, _, _, _ = history_snapshot((
            (m.ApprovalDecision.APPROVE, AT1),
            (m.ApprovalDecision.REVOKE, AT2),
        ))
        self.assertEqual(historical(value), historical(value))
        self.assertEqual(
            evaluate_current_approval_history(value, 'SCRIPT', 'policy-v1'),
            evaluate_current_approval_history(value, 'SCRIPT', 'policy-v1'),
        )

    def test_results_and_key_are_immutable(self):
        value, _, _, _ = history_snapshot(((m.ApprovalDecision.APPROVE, AT1),))
        result = historical(value)
        with self.assertRaises(FrozenInstanceError):
            result.state = State.NO_DECISION
        with self.assertRaises(FrozenInstanceError):
            result.key.gate = 'SCENES'

    def test_no_mutation_or_io(self):
        value, _, _, _ = history_snapshot(((m.ApprovalDecision.APPROVE, AT1),))
        before = copy.deepcopy(value)
        payload = encode_snapshot(value)
        historical(value)
        evaluate_current_approval_history(value, 'SCRIPT', 'policy-v1')
        self.assertEqual(value, before)
        code = '''
import sys
active = False
def guard(event, args):
    if active and (event == 'open' or event.startswith(('socket.', 'subprocess.', 'os.system'))):
        raise AssertionError(event)
sys.addaudithook(guard)
from editorial.codec import decode_snapshot
from editorial.approval_history import evaluate_current_approval_history
snapshot = decode_snapshot(PAYLOAD)
active = True
result = evaluate_current_approval_history(snapshot, 'SCRIPT', 'policy-v1')
assert result.state.value == 'RECORDED_APPROVE'
'''.replace('PAYLOAD', repr(payload))
        result = subprocess.run(
            [sys.executable, '-B', '-c', code],
            cwd=Path(__file__).resolve().parents[1],
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
