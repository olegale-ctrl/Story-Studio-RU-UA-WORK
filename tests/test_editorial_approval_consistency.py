"""E01.3.7.1 stored ApprovalRecord dependency-consistency tests."""
import copy
from dataclasses import FrozenInstanceError, replace
from pathlib import Path
import subprocess
import sys
import unittest

from editorial import model as m
from editorial.approval_consistency import (
    ApprovalConsistencyError,
    ApprovalConsistencyReason as Reason,
    evaluate_all_approval_consistency,
    evaluate_approval_consistency,
)
from editorial.codec import decode_snapshot, encode_snapshot
from editorial.current_package import CurrentPackageError, compute_current_dependency_digest
from editorial.graph import GraphValidationError
from editorial.integrity import HashVerificationError
from editorial.snapshot_checksum import SnapshotChecksumError
from test_editorial_codec import ID, raw, ref
from test_editorial_package import package_wire
from test_editorial_snapshot_integrity import add_unreferenced_source, seal


ID2 = '20000000-0000-0000-0000-000000000002'
ID3 = '30000000-0000-0000-0000-000000000003'
ID4 = '40000000-0000-0000-0000-000000000004'


def snapshot(mutate=None, after=None):
    value = package_wire(mutate)
    if after is not None:
        after(value)
    return seal(decode_snapshot(raw(value)))


def with_approvals(value, approvals):
    return seal(replace(value, base=replace(value.base, approvals=tuple(approvals))))


def matching_approval(value, gate, policy_version, decision=m.ApprovalDecision.APPROVE,
                      approval_id=ID):
    active = value.active_selections
    target = active.script if gate == 'SCRIPT' else active.scene_plan
    digest = compute_current_dependency_digest(value, gate, policy_version)
    return replace(
        value.base.approvals[0],
        id=approval_id,
        gate=gate,
        object_ref=target,
        dependency_digest=digest,
        policy_version=policy_version,
        decision=decision,
    )


def approved_snapshot(gate='SCRIPT', policy_version='policy-v1', decision=None):
    value = snapshot()
    approval = matching_approval(
        value, gate, policy_version,
        m.ApprovalDecision.APPROVE if decision is None else decision,
    )
    return with_approvals(value, (approval,)), approval


def add_script_two(value):
    script = copy.deepcopy(value['scripts'][0])
    script['ref'] = ref('script', 2)
    script['segments'][0]['text'] += ' Нова версія.'
    value['scripts'].append(script)
    value['active_refs']['script'] = ref('script', 2)


def add_scene_plan_two(value, script_revision=1, asset_revision=1):
    plan = copy.deepcopy(value['scene_plans'][0])
    plan['ref'] = ref('scene_plan', 2)
    plan['script_ref'] = ref('script', script_revision)
    plan['scenes'][0]['asset_ref'] = ref('asset', asset_revision)
    value['scene_plans'].append(plan)
    value['active_refs']['scene_plan'] = ref('scene_plan', 2)


def add_claim_chain(value):
    claim = copy.deepcopy(value['claims'][0])
    claim['ref'] = ref('claim', 2)
    claim['statement'] += ' Updated'
    value['claims'].append(claim)
    script = copy.deepcopy(value['scripts'][0])
    script['ref'] = ref('script', 2)
    script['brief']['must_include_claim_refs'] = [ref('claim', 2)]
    script['segments'][0]['claim_refs'] = [ref('claim', 2)]
    script['claim_refs'] = [ref('claim', 2)]
    value['scripts'].append(script)
    value['active_refs']['script'] = ref('script', 2)


def add_profile_chain(value):
    profile = copy.deepcopy(value['profiles'][0])
    profile['ref'] = ref('genre_profile', 2)
    profile['version'] = '2.0'
    value['profiles'].append(profile)
    production = copy.deepcopy(value['production_revisions'][0])
    production['ref'] = ref('production', 2)
    production['profile_ref'] = ref('genre_profile', 2)
    value['production_revisions'].append(production)
    script = copy.deepcopy(value['scripts'][0])
    script['ref'] = ref('script', 2)
    script['production_ref'] = ref('production', 2)
    script['brief']['profile_ref'] = ref('genre_profile', 2)
    value['scripts'].append(script)
    value['active_refs'].update(production=ref('production', 2), script=ref('script', 2))


def add_source_chain(value, change_rights=False):
    rights = copy.deepcopy(value['rights_reviews'][0])
    rights['ref'] = ref('rights_review', 3)
    rights['subject_revision'] = 2
    if change_rights:
        rights['basis'] = 'Updated rights review'
    value['rights_reviews'].append(rights)
    source = copy.deepcopy(value['sources'][0])
    source['ref'] = ref('source', 2)
    source['rights_ref'] = ref('rights_review', 3)
    if not change_rights:
        source['title'] += ' Updated'
    value['sources'].append(source)
    candidate = copy.deepcopy(value['candidates'][0])
    candidate['ref'] = ref('candidate', 2)
    candidate['source_refs'] = [ref('source', 2)]
    value['candidates'].append(candidate)
    claim = copy.deepcopy(value['claims'][0])
    claim['ref'] = ref('claim', 2)
    claim['evidence_links'][0]['source_ref'] = ref('source', 2)
    value['claims'].append(claim)
    script = copy.deepcopy(value['scripts'][0])
    script['ref'] = ref('script', 2)
    script['candidate_ref'] = ref('candidate', 2)
    script['brief']['must_include_claim_refs'] = [ref('claim', 2)]
    script['segments'][0]['claim_refs'] = [ref('claim', 2)]
    script['claim_refs'] = [ref('claim', 2)]
    value['scripts'].append(script)
    value['active_refs'].update(candidate=ref('candidate', 2), script=ref('script', 2))


def add_asset_chain(value):
    rights = copy.deepcopy(value['rights_reviews'][1])
    rights['ref'] = ref('rights_review', 3)
    rights['ref']['id'] = ID3
    rights['subject_revision'] = 2
    rights['subject_kind'] = 'asset'
    rights['basis'] = 'Updated asset rights'
    value['rights_reviews'].append(rights)
    asset = copy.deepcopy(value['assets'][0])
    asset['ref'] = ref('asset', 2)
    asset['rights_ref'] = ref('rights_review', 3)
    asset['rights_ref']['id'] = ID3
    asset['file_ref'] = 'media/updated.png'
    value['assets'].append(asset)
    add_scene_plan_two(value, asset_revision=2)


class ApprovalConsistencyTests(unittest.TestCase):
    def assert_stale_after(self, gate, mutate, expected=None):
        _, approval = approved_snapshot(gate)
        changed = snapshot(mutate)
        changed = with_approvals(changed, (approval,))
        result = evaluate_approval_consistency(changed, approval.id, gate, 'policy-v1')
        self.assertFalse(result.dependency_consistent)
        if expected is not None:
            self.assertEqual(result.reasons, expected)
        return result

    def test_exact_script_match(self):
        value, approval = approved_snapshot('SCRIPT')
        result = evaluate_approval_consistency(value, approval.id, 'SCRIPT', 'policy-v1')
        self.assertTrue(result.dependency_consistent)
        self.assertEqual(result.reasons, ())
        self.assertEqual(result.decision, m.ApprovalDecision.APPROVE)
        self.assertFalse(hasattr(result, 'approved'))
        self.assertFalse(hasattr(result, 'ready'))

    def test_exact_scenes_match(self):
        value, approval = approved_snapshot('SCENES')
        self.assertTrue(evaluate_approval_consistency(
            value, approval.id, 'SCENES', 'policy-v1').dependency_consistent)

    def test_exact_handoff_match(self):
        value, approval = approved_snapshot('HANDOFF')
        self.assertTrue(evaluate_approval_consistency(
            value, approval.id, 'HANDOFF', 'policy-v1').dependency_consistent)

    def test_gate_mismatch(self):
        value, approval = approved_snapshot('SCRIPT')
        stale = replace(approval, gate='SCENES')
        value = with_approvals(value, (stale,))
        result = evaluate_approval_consistency(value, stale.id, 'SCRIPT', 'policy-v1')
        self.assertEqual(result.reasons, (Reason.GATE_MISMATCH,))

    def test_policy_version_mismatch(self):
        value, approval = approved_snapshot('SCRIPT')
        stale = replace(approval, policy_version='old-policy')
        value = with_approvals(value, (stale,))
        result = evaluate_approval_consistency(value, stale.id, 'SCRIPT', 'policy-v1')
        self.assertEqual(result.reasons, (Reason.POLICY_VERSION_MISMATCH,))

    def test_target_ref_mismatch(self):
        value, approval = approved_snapshot('SCRIPT')
        stale = replace(approval, object_ref=value.active_selections.scene_plan)
        value = with_approvals(value, (stale,))
        result = evaluate_approval_consistency(value, stale.id, 'SCRIPT', 'policy-v1')
        self.assertEqual(result.reasons, (Reason.TARGET_REF_MISMATCH,))

    def test_dependency_digest_mismatch(self):
        value, approval = approved_snapshot('SCRIPT')
        stale = replace(approval, dependency_digest='0' * 64)
        value = with_approvals(value, (stale,))
        result = evaluate_approval_consistency(value, stale.id, 'SCRIPT', 'policy-v1')
        self.assertEqual(result.reasons, (Reason.DEPENDENCY_DIGEST_MISMATCH,))

    def test_multiple_staleness_reasons_have_fixed_order(self):
        value, approval = approved_snapshot('SCRIPT')
        stale = replace(approval, gate='HANDOFF', policy_version='old',
                        object_ref=value.active_selections.scene_plan,
                        dependency_digest='0' * 64)
        value = with_approvals(value, (stale,))
        result = evaluate_approval_consistency(value, stale.id, 'SCRIPT', 'policy-v1')
        self.assertEqual(result.reasons, (
            Reason.GATE_MISMATCH,
            Reason.POLICY_VERSION_MISMATCH,
            Reason.TARGET_REF_MISMATCH,
            Reason.DEPENDENCY_DIGEST_MISMATCH,
        ))

    def test_new_current_script_makes_old_record_stale(self):
        result = self.assert_stale_after('SCRIPT', add_script_two)
        self.assertIn(Reason.TARGET_REF_MISMATCH, result.reasons)
        self.assertIn(Reason.DEPENDENCY_DIGEST_MISMATCH, result.reasons)

    def test_new_current_scene_plan_makes_old_record_stale(self):
        result = self.assert_stale_after('SCENES', add_scene_plan_two)
        self.assertIn(Reason.TARGET_REF_MISMATCH, result.reasons)

    def test_new_referenced_source_makes_old_record_stale(self):
        self.assert_stale_after('SCRIPT', add_source_chain)

    def test_new_referenced_claim_makes_old_record_stale(self):
        self.assert_stale_after('SCRIPT', add_claim_chain)

    def test_new_referenced_profile_makes_old_record_stale(self):
        self.assert_stale_after('SCRIPT', add_profile_chain)

    def test_new_referenced_rights_review_makes_old_record_stale(self):
        self.assert_stale_after('SCRIPT', lambda value: add_source_chain(value, True))

    def test_new_referenced_asset_makes_scenes_and_handoff_stale(self):
        for gate in ('SCENES', 'HANDOFF'):
            with self.subTest(gate=gate):
                self.assert_stale_after(gate, add_asset_chain)

    def test_unreferenced_history_does_not_make_record_stale(self):
        _, approval = approved_snapshot('SCRIPT')

        def mutate(value):
            source = copy.deepcopy(value['sources'][0])
            source['ref'] = ref('source', 2)
            source['rights_ref'] = ref('rights_review', 3)
            value['sources'].append(source)
            rights = copy.deepcopy(value['rights_reviews'][0])
            rights['ref'] = ref('rights_review', 3)
            rights['subject_revision'] = 2
            value['rights_reviews'].append(rights)

        changed = with_approvals(snapshot(mutate), (approval,))
        result = evaluate_approval_consistency(changed, approval.id, 'SCRIPT', 'policy-v1')
        self.assertTrue(result.dependency_consistent)

    def test_script_ignores_downstream_scene_plan_change(self):
        _, approval = approved_snapshot('SCRIPT')
        changed = with_approvals(snapshot(add_scene_plan_two), (approval,))
        result = evaluate_approval_consistency(changed, approval.id, 'SCRIPT', 'policy-v1')
        self.assertTrue(result.dependency_consistent)

    def test_explicit_return_to_previous_coherent_chain_can_match(self):
        _, approval = approved_snapshot('SCRIPT')

        def history(value):
            script = copy.deepcopy(value['scripts'][0])
            script['ref'] = ref('script', 2)
            script['segments'][0]['text'] += ' Historical alternative'
            value['scripts'].append(script)

        changed = with_approvals(snapshot(history), (approval,))
        result = evaluate_approval_consistency(changed, approval.id, 'SCRIPT', 'policy-v1')
        self.assertTrue(result.dependency_consistent)
        self.assertFalse(hasattr(result, 'authority'))

    def test_all_decisions_are_evaluated_and_preserved(self):
        value = snapshot()
        approvals = tuple(matching_approval(
            value, 'SCRIPT', 'policy-v1', decision, approval_id)
            for decision, approval_id in zip(
                tuple(m.ApprovalDecision), (ID, ID2, ID3, ID4)))
        value = with_approvals(value, approvals)
        results = evaluate_all_approval_consistency(value, 'SCRIPT', 'policy-v1')
        self.assertEqual(tuple(result.decision for result in results),
                         tuple(m.ApprovalDecision))
        self.assertTrue(all(result.dependency_consistent for result in results))

    def test_empty_approval_collection_returns_empty_tuple(self):
        value = with_approvals(snapshot(), ())
        self.assertEqual(evaluate_all_approval_consistency(
            value, 'SCRIPT', 'policy-v1'), ())

    def test_unknown_approval_id_is_structured(self):
        value = snapshot()
        with self.assertRaises(ApprovalConsistencyError) as caught:
            evaluate_approval_consistency(value, ID4, 'SCRIPT', 'policy-v1')
        self.assertEqual(caught.exception.violation.code, 'APPROVAL_NOT_FOUND')
        self.assertEqual(caught.exception.violation.field_path, '$.approval_id')

    def test_checksum_mismatch_blocks_evaluation(self):
        value, approval = approved_snapshot('SCRIPT')
        corrupt = replace(value, snapshot_checksum='0' * 64)
        with self.assertRaises(SnapshotChecksumError):
            evaluate_approval_consistency(corrupt, approval.id, 'SCRIPT', 'policy-v1')

    def test_graph_failure_blocks_evaluation(self):
        def change(value):
            value['candidates'][0]['source_refs'][0] = ref('source', 99)
        value = snapshot(after=change)
        with self.assertRaises(GraphValidationError):
            evaluate_approval_consistency(value, ID, 'SCRIPT', 'policy-v1')

    def test_unreferenced_content_hash_failure_blocks_evaluation(self):
        value = snapshot(after=lambda wire_value: add_unreferenced_source(wire_value))
        with self.assertRaises(HashVerificationError):
            evaluate_approval_consistency(value, ID, 'SCRIPT', 'policy-v1')

    def test_incoherent_active_chain_blocks_evaluation(self):
        def mutate(value):
            production = copy.deepcopy(value['production_revisions'][0])
            production['ref'] = ref('production', 2)
            value['production_revisions'].append(production)
            value['active_refs']['production'] = ref('production', 2)
        value = snapshot(mutate)
        with self.assertRaises(CurrentPackageError):
            evaluate_approval_consistency(value, ID, 'SCRIPT', 'policy-v1')

    def test_bulk_preserves_snapshot_order(self):
        value = snapshot()
        approvals = (
            matching_approval(value, 'SCRIPT', 'policy-v1', approval_id=ID3),
            matching_approval(value, 'SCRIPT', 'policy-v1', approval_id=ID),
            matching_approval(value, 'SCRIPT', 'policy-v1', approval_id=ID4),
        )
        value = with_approvals(value, approvals)
        results = evaluate_all_approval_consistency(value, 'SCRIPT', 'policy-v1')
        self.assertEqual(tuple(result.approval_id for result in results),
                         (ID3, ID, ID4))

    def test_unicode_policy_is_preserved_literally(self):
        policy = 'політика-Русский-😀-е\u0301'
        value, approval = approved_snapshot('SCRIPT', policy)
        result = evaluate_approval_consistency(value, approval.id, 'SCRIPT', policy)
        self.assertTrue(result.dependency_consistent)
        self.assertNotEqual(result.current_dependency_digest,
                            compute_current_dependency_digest(value, 'SCRIPT', policy + ' '))

    def test_results_are_immutable(self):
        value, approval = approved_snapshot('SCRIPT')
        result = evaluate_approval_consistency(value, approval.id, 'SCRIPT', 'policy-v1')
        with self.assertRaises(FrozenInstanceError):
            result.dependency_consistent = False

    def test_no_mutation_or_io(self):
        value, approval = approved_snapshot('SCRIPT')
        before = copy.deepcopy(value)
        payload = encode_snapshot(value)
        evaluate_approval_consistency(value, approval.id, 'SCRIPT', 'policy-v1')
        evaluate_all_approval_consistency(value, 'SCRIPT', 'policy-v1')
        self.assertEqual(value, before)
        code = '''
import sys
active = False
def guard(event, args):
    if active and (event == 'open' or event.startswith(('socket.', 'subprocess.', 'os.system'))):
        raise AssertionError(event)
sys.addaudithook(guard)
from editorial.codec import decode_snapshot
from editorial.approval_consistency import evaluate_all_approval_consistency
snapshot = decode_snapshot(PAYLOAD)
active = True
results = evaluate_all_approval_consistency(snapshot, 'SCRIPT', 'policy-v1')
assert len(results) == 1
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
