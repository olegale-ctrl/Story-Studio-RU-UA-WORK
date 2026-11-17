"""Independent checksum oracles and read-only schema-2 integration regressions."""
import base64
import copy
from contextlib import ExitStack
from dataclasses import FrozenInstanceError, fields, replace
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from editorial import codec as c
from editorial import model as m
from editorial.approval_attestation import compute_attestation_digest
from editorial.graph import GraphValidationError
from editorial.integrity import HashVerificationError
from editorial.rights_binding import MaterialBindingState, RightsBindingError
from editorial.schema2_integrity import (
    Schema2IntegrityError, Schema2IntegrityResult,
    canonical_schema2_snapshot_bytes, compute_schema2_snapshot_checksum,
    validate_schema2_snapshot_integrity,
)
from editorial.schema2_model import (
    ApprovalAuthorityEvidence, Schema2Event, Schema2ModelError, Schema2Snapshot,
    required_declaration_codes,
)
from editorial.snapshot_checksum import compute_snapshot_checksum
from editorial.snapshot_integrity import validate_snapshot_integrity
from editorial.versioned_codec import decode_editorial_versioned, encode_editorial_versioned
from test_editorial_snapshot_integrity import full_snapshot, empty_snapshot, add_unreferenced_source


def uid(number):
    return f'40000000-0000-0000-0000-{number:012d}'


def evidence_for(record, number=1, **changes):
    values = dict(
        approval_id=record.id, principal_id='posix-uid:1000@machine:' + 'a' * 32,
        principal_display_name='  Рецензент / Рецензентка Ї И\u0306 😀  ',
        authority_policy_id=uid(100), authority_policy_version='offline-v1',
        review_session_id=uid(200 + number), request_id=uid(300 + number),
        declaration_codes=required_declaration_codes(record.gate, record.decision),
        attested_at='2026-11-05T12:00:00Z', reconsiders_record_id=None,
        attestation_digest='0' * 64, signing_key_id=None, signature_algorithm=None, signature=None,
    )
    values.update(changes)
    evidence = ApprovalAuthorityEvidence(**values)
    return replace(evidence, attestation_digest=compute_attestation_digest(record, evidence))


def seal2(snapshot):
    checksum = compute_schema2_snapshot_checksum(snapshot)
    return replace(snapshot, base_snapshot=replace(snapshot.base_snapshot, snapshot_checksum=checksum))


def populated(signed=False):
    base = full_snapshot()
    evidence = evidence_for(base.base.approvals[0])
    if signed:
        evidence = replace(evidence, signing_key_id='test-key:1', signature_algorithm='ed25519',
                           signature=base64.urlsafe_b64encode(bytes([7]) * 64).decode('ascii').rstrip('='))
    return Schema2Snapshot(base, (evidence,))


def migrated_empty():
    event = Schema2Event(uid(500), 'Рецензент 😀', '2026-11-05T12:00:00Z',
                         'schema_migrated', (), 'Schema 1 → 2', None)
    return Schema2Snapshot(replace(empty_snapshot(), events=(event,)), ())


def unchecked(value, **changes):
    """Fresh hostile input for testing the boundary, never mutate a valid input."""
    result = object.__new__(type(value))
    for field in fields(value):
        object.__setattr__(result, field.name, changes.get(field.name, getattr(value, field.name)))
    return result


# Independently calculated by a standalone Node.js sorted-key serializer and
# OpenSSL dgst -sha256 -binary, not by the tested checksum API. Fixed literals.
EMPTY_CANONICAL = (
    b'{"active_refs":{"candidate":null,"production":null,"scene_plan":null,"script":null},'
    b'"approval_authority_evidence":[],"approvals":[],"assets":[],"candidates":[],"claims":[],'
    b'"editorial_schema_version":2,"events":[],"generation":1,'
    b'"production_id":"10000000-0000-0000-0000-000000000001",'
    b'"production_revisions":[],"profiles":[],"rights_reviews":[],"scene_plans":[],"scripts":[],"sources":[]}'
)
GOLDEN_EMPTY = '1f2f4eddf534c5546bc729d74ef445f0aee0292a91d2d589cd5456d24e1cc201'
GOLDEN_POPULATED = 'ace06e2eb6ee0a929752c3422589747a5b71224b036e869283e89d9d872f3af5'
GOLDEN_SIGNED = '372407f0d151fc82a6830790fe4844f17df721eaa8ed2a0ed0aee593fb21f96f'
GOLDEN_MIGRATED = '09a828757ebae10cfc0ba903bc561bfda849f2b58ca5d448ea7f22346e9ae936'


class Schema2IntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.template = full_snapshot()

    def setUp(self):
        self.snapshot = seal2(Schema2Snapshot(self.template, (evidence_for(self.template.base.approvals[0]),)))

    def violation(self, snapshot, cls, code, path):
        with self.assertRaises(cls) as caught:
            validate_schema2_snapshot_integrity(snapshot)
        violation = caught.exception.violation
        self.assertIs(type(violation), m.Violation)
        self.assertEqual(violation.code, code)
        self.assertEqual(violation.field_path, path)
        return violation

    def history(self, decisions, links=None, evidenced=True):
        records = []
        original = self.template.base.approvals[0]
        for index, item in enumerate(decisions):
            decision, timestamp = item[:2]
            records.append(replace(original, id=uid(index + 1), decision=decision,
                                   timestamp=timestamp, actor=item[2] if len(item) > 2 else 'Owner'))
        base = replace(self.template, base=replace(self.template.base, approvals=tuple(records)))
        links = links or {}
        evidence = tuple(evidence_for(record, index + 1, reconsiders_record_id=links.get(index))
                         for index, record in enumerate(records)) if evidenced else ()
        return seal2(Schema2Snapshot(base, evidence))

    def test_golden_empty_bytes_and_checksum(self):
        snapshot = Schema2Snapshot(empty_snapshot(), ())
        self.assertEqual(canonical_schema2_snapshot_bytes(snapshot), EMPTY_CANONICAL)
        self.assertEqual(compute_schema2_snapshot_checksum(snapshot), GOLDEN_EMPTY)
        result = validate_schema2_snapshot_integrity(seal2(snapshot))
        self.assertEqual((result.revision_count, result.evidence_count), (0, 0))

    def test_golden_populated_checksum(self):
        self.assertEqual(compute_schema2_snapshot_checksum(populated()), GOLDEN_POPULATED)
        self.assertTrue(validate_schema2_snapshot_integrity(seal2(populated())).checksum_verified)

    def test_golden_signed_checksum(self):
        self.assertEqual(compute_schema2_snapshot_checksum(populated(signed=True)), GOLDEN_SIGNED)
        self.assertTrue(validate_schema2_snapshot_integrity(seal2(populated(signed=True))).checksum_verified)

    def test_golden_schema_migrated_checksum(self):
        self.assertEqual(compute_schema2_snapshot_checksum(migrated_empty()), GOLDEN_MIGRATED)
        self.assertTrue(validate_schema2_snapshot_integrity(seal2(migrated_empty())).checksum_verified)

    def test_valid_full_snapshot_has_integrity_only_result(self):
        result = validate_schema2_snapshot_integrity(self.snapshot)
        self.assertIs(type(result), Schema2IntegrityResult)
        self.assertTrue(result.checksum_verified)
        self.assertEqual(result.revision_count, 10)
        self.assertEqual(len(result.material_bindings), 2)
        self.assertEqual(result.evidence_count, 1)
        self.assertEqual(result.approval_statuses[0].authority_status, 'EVIDENCE_PRESENT_UNVERIFIED')
        self.assertEqual(result.history_diagnostics, ())
        self.assertEqual(result.transaction_order_status, 'UNVERIFIED_ORDERING')
        self.assertEqual(result.unverified_aspects,
                         ('transaction_order', 'identity', 'signatures', 'authority_policy', 'head_anchor'))
        for name in ('authorized', 'approved', 'ready', 'effective', 'latest_record', 'commercial_allowed'):
            self.assertFalse(hasattr(result, name), name)
        with self.assertRaises(FrozenInstanceError):
            result.checksum_verified = False

    def test_exact_schema2_type_required_for_all_apis(self):
        class Derived(Schema2Snapshot):
            pass

        derived = Derived(self.snapshot.base_snapshot, self.snapshot.approval_authority_evidence)
        for api in (canonical_schema2_snapshot_bytes, compute_schema2_snapshot_checksum,
                    validate_schema2_snapshot_integrity):
            for value in (None, {}, self.template, derived, encode_editorial_versioned(self.snapshot)):
                with self.subTest(api=api.__name__, type=type(value)), self.assertRaises(Schema2IntegrityError) as caught:
                    api(value)
                self.assertEqual(caught.exception.violation.code, 'TYPE')
                self.assertEqual(caught.exception.violation.field_path, '$')

    def test_empty_evidence_preserves_legacy_without_origin_claim(self):
        snapshot = seal2(Schema2Snapshot(self.template, ()))
        result = validate_schema2_snapshot_integrity(snapshot)
        self.assertEqual(result.evidence_count, 0)
        self.assertEqual(result.approval_statuses[0].authority_status, 'UNAUTHENTICATED_LEGACY')
        self.assertEqual(snapshot.base_snapshot.base.approvals, self.template.base.approvals)
        self.assertEqual(snapshot.approval_authority_evidence, ())
        self.assertFalse(hasattr(result.approval_statuses[0], 'migrated'))

    def test_multiple_evidence_and_legacy_gaps_follow_approval_order(self):
        original = self.template.base.approvals[0]
        records = tuple(replace(original, id=uid(n)) for n in (9, 1, 8, 2, 7))
        base = replace(self.template, base=replace(self.template.base, approvals=records))
        evidence = (evidence_for(records[1], 1), evidence_for(records[3], 2))
        snapshot = seal2(Schema2Snapshot(base, evidence))
        result = validate_schema2_snapshot_integrity(snapshot)
        self.assertEqual(tuple(s.approval_id for s in result.approval_statuses), tuple(r.id for r in records))
        self.assertEqual(tuple(s.authority_status for s in result.approval_statuses),
                         ('UNAUTHENTICATED_LEGACY', 'EVIDENCE_PRESENT_UNVERIFIED', 'UNAUTHENTICATED_LEGACY',
                          'EVIDENCE_PRESENT_UNVERIFIED', 'UNAUTHENTICATED_LEGACY'))
        self.assertEqual(snapshot.approval_authority_evidence, evidence)

    def test_each_locally_valid_core_evidence_change_is_detected(self):
        evidence = self.snapshot.approval_authority_evidence[0]
        changes = {
            'principal_id': 'windows-sid:S-1-5-42', 'principal_display_name': 'Інший рецензент',
            'authority_policy_id': uid(999), 'authority_policy_version': 'offline-v2',
            'review_session_id': uid(998), 'request_id': uid(997),
            'attested_at': '2026-11-05T12:00:01Z', 'reconsiders_record_id': uid(996),
        }
        self.assertEqual(set(changes) | {'approval_id', 'declaration_codes'}, {
            'approval_id', 'principal_id', 'principal_display_name', 'authority_policy_id',
            'authority_policy_version', 'review_session_id', 'request_id', 'declaration_codes',
            'attested_at', 'reconsiders_record_id'})
        for field, value in changes.items():
            with self.subTest(field=field):
                changed = replace(self.snapshot, approval_authority_evidence=(replace(evidence, **{field: value}),))
                self.assertNotEqual(compute_schema2_snapshot_checksum(changed),
                                    self.snapshot.base_snapshot.snapshot_checksum)
                self.violation(changed, Schema2IntegrityError, 'SNAPSHOT_CHECKSUM_MISMATCH', '$.snapshot_checksum')
                self.violation(seal2(changed), Schema2IntegrityError, 'ATTESTATION_DIGEST_MISMATCH',
                               '$.approval_authority_evidence[0].attestation_digest')

    def test_changed_approval_link_with_old_attestation_is_detected(self):
        original = self.template.base.approvals[0]
        second = replace(original, id=uid(2))
        base = replace(self.template, base=replace(self.template.base, approvals=(original, second)))
        evidence = replace(evidence_for(original), approval_id=second.id)
        snapshot = seal2(Schema2Snapshot(base, (evidence,)))
        self.violation(snapshot, Schema2IntegrityError, 'ATTESTATION_DIGEST_MISMATCH',
                       '$.approval_authority_evidence[0].attestation_digest')

    def test_declaration_change_rejected_at_existing_boundary(self):
        evidence = self.snapshot.approval_authority_evidence[0]
        evidence = replace(evidence, declaration_codes=('SCRIPT_EXACT_TEXT_REVIEWED',))
        with self.assertRaises(Schema2ModelError):
            replace(self.snapshot, approval_authority_evidence=(evidence,))
        hostile = unchecked(self.snapshot, approval_authority_evidence=(evidence,))
        self.violation(hostile, c.EncodeError, 'INVALID_VALUE', '$.approval_authority_evidence[0].declaration_codes')

    def test_snapshot_checksum_and_attestation_digest_have_separate_coverage(self):
        evidence = replace(self.snapshot.approval_authority_evidence[0], attestation_digest='f' * 64)
        changed = replace(self.snapshot, approval_authority_evidence=(evidence,))
        self.assertNotEqual(compute_schema2_snapshot_checksum(changed), self.snapshot.base_snapshot.snapshot_checksum)
        self.violation(seal2(changed), Schema2IntegrityError, 'ATTESTATION_DIGEST_MISMATCH',
                       '$.approval_authority_evidence[0].attestation_digest')

    def test_signature_fields_are_in_checksum_but_not_attestation_digest(self):
        signed = seal2(populated(signed=True))
        evidence = signed.approval_authority_evidence[0]
        signature = base64.urlsafe_b64encode(bytes([8]) * 64).decode('ascii').rstrip('=')
        variants = (replace(evidence, signing_key_id='test-key:2'), replace(evidence, signature=signature),
                    replace(evidence, signing_key_id=None, signature_algorithm=None, signature=None))
        for value in variants:
            with self.subTest(signature=value.signature, key=value.signing_key_id):
                changed = replace(signed, approval_authority_evidence=(value,))
                self.violation(changed, Schema2IntegrityError, 'SNAPSHOT_CHECKSUM_MISMATCH', '$.snapshot_checksum')
                self.assertTrue(validate_schema2_snapshot_integrity(seal2(changed)).checksum_verified)
                self.assertEqual(value.attestation_digest, evidence.attestation_digest)

    def test_partial_or_unknown_signature_algorithm_rejected_by_existing_boundary(self):
        for changes, path in (({'signing_key_id': 'key'}, 'signature'),
                              ({'signature_algorithm': 'rsa'}, 'signature')):
            evidence = unchecked(self.snapshot.approval_authority_evidence[0], **changes)
            hostile = unchecked(self.snapshot, approval_authority_evidence=(evidence,))
            self.violation(hostile, c.EncodeError, 'INVALID_VALUE', f'$.approval_authority_evidence[0].{path}')
        signed = seal2(populated(signed=True))
        evidence = unchecked(signed.approval_authority_evidence[0], signature_algorithm='rsa')
        self.violation(unchecked(signed, approval_authority_evidence=(evidence,)), c.EncodeError,
                       'INVALID_VALUE', '$.approval_authority_evidence[0].signature_algorithm')

    def test_only_root_checksum_is_excluded_and_not_repaired(self):
        changed = replace(self.snapshot, base_snapshot=replace(self.snapshot.base_snapshot, snapshot_checksum='f' * 64))
        self.assertEqual(canonical_schema2_snapshot_bytes(changed), canonical_schema2_snapshot_bytes(self.snapshot))
        self.assertEqual(compute_schema2_snapshot_checksum(changed), self.snapshot.base_snapshot.snapshot_checksum)
        self.violation(changed, Schema2IntegrityError, 'SNAPSHOT_CHECKSUM_MISMATCH', '$.snapshot_checksum')
        self.assertEqual(changed.base_snapshot.snapshot_checksum, 'f' * 64)

    def test_approval_record_changes_are_covered(self):
        approval = self.snapshot.base_snapshot.base.approvals[0]
        base = replace(self.snapshot.base_snapshot, base=replace(
            self.snapshot.base_snapshot.base, approvals=(replace(approval, actor='Другой'),)))
        changed = replace(self.snapshot, base_snapshot=base)
        self.violation(changed, Schema2IntegrityError, 'SNAPSHOT_CHECKSUM_MISMATCH', '$.snapshot_checksum')
        self.violation(seal2(changed), Schema2IntegrityError, 'ATTESTATION_DIGEST_MISMATCH',
                       '$.approval_authority_evidence[0].attestation_digest')

    def test_schema_migrated_event_exact_action_and_fields_are_covered(self):
        snapshot = seal2(migrated_empty())
        canonical = canonical_schema2_snapshot_bytes(snapshot)
        self.assertIn(b'"action":"schema_migrated"', canonical)
        self.assertNotIn(b'operation_failed', canonical)
        for field, value in (('reason', 'Друга причина'), ('actor', 'Інший'),
                              ('at', '2026-11-05T12:00:01Z')):
            with self.subTest(field=field):
                event = replace(snapshot.base_snapshot.events[0], **{field: value})
                changed = replace(snapshot, base_snapshot=replace(snapshot.base_snapshot, events=(event,)))
                self.violation(changed, Schema2IntegrityError, 'SNAPSHOT_CHECKSUM_MISMATCH', '$.snapshot_checksum')
                self.assertTrue(validate_schema2_snapshot_integrity(seal2(changed)).checksum_verified)

    def test_generation_and_active_refs_are_covered(self):
        for changes in ({'generation': 2}, {'active_refs': ()}):
            base = replace(self.snapshot.base_snapshot, base=replace(self.snapshot.base_snapshot.base, **changes))
            self.violation(replace(self.snapshot, base_snapshot=base), Schema2IntegrityError,
                           'SNAPSHOT_CHECKSUM_MISMATCH', '$.snapshot_checksum')

    def test_graph_missing_target_regression(self):
        base = full_snapshot(after=lambda wire: wire['candidates'][0]['source_refs'][0].update(revision=99))
        self.violation(seal2(Schema2Snapshot(base, ())), GraphValidationError, 'TARGET_REVISION_MISMATCH',
                       '$.candidates[0].source_refs[0]')

    def test_graph_reference_hash_regression(self):
        base = full_snapshot(after=lambda wire: wire['active_refs']['script'].update(content_hash='f' * 64))
        self.violation(seal2(Schema2Snapshot(base, ())), GraphValidationError, 'REFERENCE_HASH_MISMATCH',
                       '$.active_refs.script.content_hash')

    def test_graph_referenced_revision_hash_regression(self):
        base = full_snapshot(after=lambda wire: wire['sources'][0].update(title='Changed title'))
        self.violation(seal2(Schema2Snapshot(base, ())), GraphValidationError, 'TARGET_HASH_INVALID',
                       '$.sources[0].ref.content_hash')

    def test_unreferenced_historical_hash_is_checked(self):
        base = full_snapshot(after=lambda wire: add_unreferenced_source(wire))
        self.violation(seal2(Schema2Snapshot(base, ())), HashVerificationError, 'CONTENT_HASH_MISMATCH',
                       '$.sources[1].ref.content_hash')

    def test_unreferenced_companion_hash_is_checked(self):
        def mutate(wire):
            add_unreferenced_source(wire, valid_hash=True)
            wire['sources'][1]['reliability_notes'] = 'Changed notes'
        self.violation(seal2(Schema2Snapshot(full_snapshot(after=mutate), ())), HashVerificationError,
                       'CONTENT_HASH_MISMATCH', '$.sources[1].ref.content_hash')

    def test_rights_material_and_subject_binding_regressions(self):
        cases = (
            (lambda wire: wire['sources'][0].update(material_digest='b' * 64),
             'MATERIAL_DIGEST_MISMATCH', '$.sources[0].material_digest'),
            (lambda wire: wire['assets'][0].update(sha256='b' * 64),
             'MATERIAL_DIGEST_MISMATCH', '$.assets[0].sha256'),
            (lambda wire: wire['rights_reviews'][0].update(subject_id=uid(999)),
             'SUBJECT_ID_MISMATCH', '$.rights_reviews[0].subject_id'),
        )
        for mutate, code, path in cases:
            with self.subTest(code=code, path=path):
                self.violation(seal2(Schema2Snapshot(full_snapshot(mutate), ())), RightsBindingError, code, path)

    def test_unconfirmed_material_binding_remains_draft_inspection(self):
        base = full_snapshot(lambda wire: wire['sources'][0].update(material_digest=None))
        result = validate_schema2_snapshot_integrity(seal2(Schema2Snapshot(base, ())))
        self.assertIn(MaterialBindingState.UNCONFIRMED, tuple(b.material_state for b in result.material_bindings))

    def test_checksum_precedes_graph_and_attestation_failures(self):
        base = full_snapshot(after=lambda wire: wire['active_refs']['script'].update(content_hash='f' * 64))
        snapshot = Schema2Snapshot(base, (replace(evidence_for(base.base.approvals[0]), attestation_digest='f' * 64),))
        self.violation(snapshot, Schema2IntegrityError, 'SNAPSHOT_CHECKSUM_MISMATCH', '$.snapshot_checksum')
        self.violation(seal2(snapshot), GraphValidationError, 'REFERENCE_HASH_MISMATCH',
                       '$.active_refs.script.content_hash')

    def test_rights_precede_attestation_failures(self):
        base = full_snapshot(lambda wire: wire['assets'][0].update(sha256='b' * 64))
        evidence = replace(evidence_for(base.base.approvals[0]), attestation_digest='f' * 64)
        snapshot = seal2(Schema2Snapshot(base, (evidence,)))
        self.violation(snapshot, RightsBindingError, 'MATERIAL_DIGEST_MISMATCH', '$.assets[0].sha256')

    def test_existing_join_order_and_uniqueness_invariants_apply_at_boundary(self):
        original = self.template.base.approvals[0]
        second = replace(original, id=uid(2))
        base = replace(self.template, base=replace(self.template.base, approvals=(original, second)))
        first_evidence, second_evidence = evidence_for(original, 1), evidence_for(second, 2)
        snapshot = Schema2Snapshot(base, (first_evidence, second_evidence))
        cases = (
            ((second_evidence, first_evidence), '$.approval_authority_evidence'),
            ((first_evidence, replace(second_evidence, approval_id=original.id)), '$.approval_authority_evidence[1].approval_id'),
            ((first_evidence, replace(second_evidence, review_session_id=first_evidence.review_session_id)),
             '$.approval_authority_evidence[1].review_session_id'),
            ((first_evidence, replace(second_evidence, request_id=first_evidence.request_id)),
             '$.approval_authority_evidence[1].request_id'),
            ((replace(first_evidence, approval_id=uid(999)), second_evidence), '$.approval_authority_evidence[0].approval_id'),
        )
        for values, path in cases:
            with self.subTest(path=path):
                with self.assertRaises(Schema2ModelError):
                    replace(snapshot, approval_authority_evidence=values)
                self.violation(unchecked(snapshot, approval_authority_evidence=values), c.EncodeError, 'INVALID_VALUE', path)

    def test_all_gate_decision_declarations_are_reused_without_new_vocabulary(self):
        original = self.template.base.approvals[0]
        for gate in ('SCRIPT', 'SCENES', 'HANDOFF'):
            for decision in m.ApprovalDecision:
                with self.subTest(gate=gate, decision=decision):
                    record = replace(original, gate=gate, decision=decision)
                    base = replace(self.template, base=replace(self.template.base, approvals=(record,)))
                    evidence = evidence_for(record)
                    self.assertTrue(validate_schema2_snapshot_integrity(seal2(Schema2Snapshot(base, (evidence,)))).checksum_verified)
                    invalid_codes = ('SCRIPT_EXACT_TEXT_REVIEWED',) if decision is not m.ApprovalDecision.APPROVE else ('NO_UNSUPPORTED_REVIEW_CLAIM',)
                    invalid = replace(evidence, declaration_codes=invalid_codes)
                    with self.assertRaises(Schema2ModelError):
                        Schema2Snapshot(base, (invalid,))

    def test_reordered_approve_declarations_rejected_at_boundary(self):
        record = replace(self.template.base.approvals[0], decision=m.ApprovalDecision.APPROVE)
        base = replace(self.template, base=replace(self.template.base, approvals=(record,)))
        evidence = evidence_for(record)
        snapshot = Schema2Snapshot(base, (evidence,))
        evidence = replace(evidence, declaration_codes=evidence.declaration_codes[::-1])
        self.violation(unchecked(snapshot, approval_authority_evidence=(evidence,)), c.EncodeError,
                       'INVALID_VALUE', '$.approval_authority_evidence[0].declaration_codes')

    def test_valid_reconsideration_after_each_negative_decision_remains_unverified(self):
        for decision in (m.ApprovalDecision.REJECT, m.ApprovalDecision.REVISE, m.ApprovalDecision.REVOKE):
            with self.subTest(target=decision):
                snapshot = self.history(((decision, '2026-11-05T10:00:00Z'),
                                         (m.ApprovalDecision.APPROVE, '2026-11-05T11:00:00Z')), {1: uid(1)})
                result = validate_schema2_snapshot_integrity(snapshot)
                self.assertEqual(result.reconsiderations[1].target_record_id, uid(1))
                self.assertEqual(result.reconsiderations[1].link_status, 'LINK_CONSISTENT_ORDERING_UNVERIFIED')
                self.assertEqual(result.reconsiderations[1].transaction_order_status, 'UNVERIFIED_ORDERING')
                self.assertEqual(result.ordering_diagnostics[0].field_path,
                                 '$.approval_authority_evidence[1].reconsiders_record_id')

    def test_dangling_reconsideration_target(self):
        record = self.template.base.approvals[0]
        evidence = evidence_for(record, reconsiders_record_id=uid(999))
        self.violation(seal2(Schema2Snapshot(self.template, (evidence,))), Schema2IntegrityError,
                       'RECONSIDERATION_TARGET_MISSING', '$.approval_authority_evidence[0].reconsiders_record_id')

    def test_self_reference_rejected_by_model_and_integration_boundary(self):
        evidence = self.snapshot.approval_authority_evidence[0]
        with self.assertRaises(Schema2ModelError):
            replace(evidence, reconsiders_record_id=evidence.approval_id)
        hostile = unchecked(evidence, reconsiders_record_id=evidence.approval_id)
        self.violation(unchecked(self.snapshot, approval_authority_evidence=(hostile,)), c.EncodeError,
                       'INVALID_VALUE', '$.approval_authority_evidence[0].reconsiders_record_id')

    def test_cross_key_reconsideration_checks_every_key_component(self):
        target = replace(self.template.base.approvals[0], id=uid(1), decision=m.ApprovalDecision.REVOKE)
        source = replace(target, id=uid(2), decision=m.ApprovalDecision.APPROVE)
        changes = {'gate': 'SCENES', 'policy_version': 'different-policy',
                   'object_ref': self.template.active_selections.scene_plan, 'dependency_digest': 'f' * 64}
        for field, value in changes.items():
            with self.subTest(field=field):
                changed = replace(source, **{field: value})
                base = replace(self.template, base=replace(self.template.base, approvals=(target, changed)))
                snapshot = seal2(Schema2Snapshot(base, (evidence_for(changed, reconsiders_record_id=target.id),)))
                self.violation(snapshot, Schema2IntegrityError, 'RECONSIDERATION_KEY_MISMATCH',
                               '$.approval_authority_evidence[0].reconsiders_record_id')

    def test_reconsideration_cannot_target_approve(self):
        snapshot = self.history(((m.ApprovalDecision.APPROVE, '2026-11-05T10:00:00Z'),
                                 (m.ApprovalDecision.APPROVE, '2026-11-05T11:00:00Z')), {1: uid(1)})
        self.violation(snapshot, Schema2IntegrityError, 'RECONSIDERATION_DECISION_MISMATCH',
                       '$.approval_authority_evidence[1].reconsiders_record_id')

    def test_attestation_failure_precedes_invalid_reconsideration(self):
        record = self.template.base.approvals[0]
        evidence = replace(evidence_for(record), reconsiders_record_id=uid(999))
        snapshot = seal2(Schema2Snapshot(self.template, (evidence,)))
        self.violation(snapshot, Schema2IntegrityError, 'ATTESTATION_DIGEST_MISMATCH',
                       '$.approval_authority_evidence[0].attestation_digest')

    def test_no_uuid_timestamp_or_array_order_establishes_latest_target(self):
        # Link to a later array element with a later descriptive timestamp.
        snapshot = self.history(((m.ApprovalDecision.APPROVE, '2026-11-05T10:00:00Z'),
                                 (m.ApprovalDecision.REVOKE, '2026-11-05T12:00:00Z')), {0: uid(2)})
        result = validate_schema2_snapshot_integrity(snapshot)
        self.assertEqual(result.reconsiderations[0].target_record_id, uid(2))
        self.assertEqual(result.reconsiderations[0].transaction_order_status, 'UNVERIFIED_ORDERING')
        self.assertFalse(hasattr(result.reconsiderations[0], 'latest_record'))

    def test_multiple_targets_do_not_upgrade_a_supplied_link_to_latest(self):
        snapshot = self.history(((m.ApprovalDecision.REJECT, '2026-11-05T10:00:00Z'),
                                 (m.ApprovalDecision.REVOKE, '2026-11-05T11:00:00Z'),
                                 (m.ApprovalDecision.APPROVE, '2026-11-05T12:00:00Z')), {2: uid(1)})
        result = validate_schema2_snapshot_integrity(snapshot)
        self.assertEqual(result.reconsiderations[2].target_record_id, uid(1))
        self.assertEqual(result.reconsiderations[2].link_status, 'LINK_CONSISTENT_ORDERING_UNVERIFIED')
        self.assertEqual(result.ordering_diagnostics[0].code, 'UNVERIFIED_ORDERING')

    def test_missing_link_with_negative_history_is_explicitly_unverified(self):
        for decisions in (
            ((m.ApprovalDecision.REVOKE, '2026-11-05T10:00:00Z'), (m.ApprovalDecision.APPROVE, '2026-11-05T11:00:00Z')),
            ((m.ApprovalDecision.APPROVE, '2026-11-05T10:00:00Z'), (m.ApprovalDecision.REVOKE, '2026-11-05T11:00:00Z')),
        ):
            result = validate_schema2_snapshot_integrity(self.history(decisions))
            self.assertIn('RECONSIDERATION_REQUIREMENT_UNVERIFIED', tuple(r.link_status for r in result.reconsiderations))
            self.assertEqual(result.ordering_diagnostics[0].code, 'UNVERIFIED_ORDERING')

    def test_legacy_reconsideration_target_is_not_authenticated(self):
        snapshot = self.history(((m.ApprovalDecision.REVOKE, '2026-11-05T10:00:00Z'),
                                 (m.ApprovalDecision.APPROVE, '2026-11-05T11:00:00Z')), {1: uid(1)})
        snapshot = seal2(replace(snapshot, approval_authority_evidence=snapshot.approval_authority_evidence[1:]))
        result = validate_schema2_snapshot_integrity(snapshot)
        self.assertEqual(result.approval_statuses[0].authority_status, 'UNAUTHENTICATED_LEGACY')
        self.assertEqual(result.reconsiderations[0].transaction_order_status, 'UNVERIFIED_ORDERING')

    def test_ambiguous_same_timestamp_preserved_as_exact_violations(self):
        snapshot = self.history(((m.ApprovalDecision.REJECT, '2026-11-05T10:00:00Z'),
                                 (m.ApprovalDecision.REVOKE, '2026-11-05T10:00:00Z'),
                                 (m.ApprovalDecision.APPROVE, '2026-11-05T11:00:00Z')), {2: uid(1)})
        result = validate_schema2_snapshot_integrity(snapshot)
        self.assertEqual(tuple(v.code for v in result.history_diagnostics), ('AMBIGUOUS_HISTORY',) * 2)
        self.assertEqual(tuple(v.field_path for v in result.history_diagnostics),
                         ('$.approvals[0].timestamp', '$.approvals[1].timestamp'))
        self.assertEqual(result.reconsiderations[2].transaction_order_status, 'UNVERIFIED_ORDERING')
        self.assertFalse(hasattr(result, 'latest_record'))

    def test_same_decision_different_metadata_is_ambiguous(self):
        snapshot = self.history(((m.ApprovalDecision.REVISE, '2026-11-05T10:00:00Z', 'One'),
                                 (m.ApprovalDecision.REVISE, '2026-11-05T10:00:00Z', 'Two')), evidenced=False)
        self.assertEqual(len(validate_schema2_snapshot_integrity(snapshot).history_diagnostics), 2)

    def test_equivalent_same_time_records_do_not_select_a_uuid(self):
        snapshot = self.history(((m.ApprovalDecision.REVISE, '2026-11-05T10:00:00Z'),
                                 (m.ApprovalDecision.REVISE, '2026-11-05T10:00:00Z')), evidenced=False)
        result = validate_schema2_snapshot_integrity(snapshot)
        self.assertEqual(result.history_diagnostics, ())
        self.assertEqual(tuple(s.approval_id for s in result.approval_statuses), (uid(1), uid(2)))
        self.assertEqual(result.transaction_order_status, 'UNVERIFIED_ORDERING')

    def test_different_exact_keys_are_not_same_time_conflict(self):
        snapshot = self.history(((m.ApprovalDecision.REVISE, '2026-11-05T10:00:00Z'),
                                 (m.ApprovalDecision.REVOKE, '2026-11-05T10:00:00Z')), evidenced=False)
        records = snapshot.base_snapshot.base.approvals
        base = replace(snapshot.base_snapshot, base=replace(snapshot.base_snapshot.base,
                       approvals=(records[0], replace(records[1], policy_version='other'))))
        self.assertEqual(validate_schema2_snapshot_integrity(seal2(replace(snapshot, base_snapshot=base))).history_diagnostics, ())

    def test_all_history_groups_inspected_without_timestamp_latest_selection(self):
        snapshot = self.history(((m.ApprovalDecision.REJECT, '2026-11-05T10:00:00Z'),
                                 (m.ApprovalDecision.REVISE, '2026-11-05T10:00:00Z'),
                                 (m.ApprovalDecision.REVOKE, '2026-11-05T12:00:00Z')), evidenced=False)
        self.assertEqual(len(validate_schema2_snapshot_integrity(snapshot).history_diagnostics), 2)

    def test_schema1_checksum_and_validation_remain_unchanged(self):
        before = compute_snapshot_checksum(self.template)
        schema1_bytes = c.encode_snapshot(self.template)
        validate_schema2_snapshot_integrity(self.snapshot)
        self.assertEqual(compute_snapshot_checksum(self.template), before)
        self.assertEqual(c.encode_snapshot(self.template), schema1_bytes)
        self.assertTrue(validate_snapshot_integrity(self.template).checksum_verified)
        self.assertEqual(decode_editorial_versioned(schema1_bytes), self.template)

    def test_schema2_checksum_is_not_schema1_checksum_of_common_subset(self):
        self.assertNotEqual(compute_schema2_snapshot_checksum(self.snapshot),
                            compute_snapshot_checksum(self.snapshot.base_snapshot))
        payload = json.loads(canonical_schema2_snapshot_bytes(self.snapshot))
        self.assertEqual(payload['editorial_schema_version'], 2)
        self.assertEqual(len(payload['approval_authority_evidence']), 1)
        self.assertEqual(payload['approval_authority_evidence'][0]['attestation_digest'],
                         self.snapshot.approval_authority_evidence[0].attestation_digest)

    def test_input_immutability_determinism_and_round_trip(self):
        before = copy.deepcopy(self.snapshot)
        first = validate_schema2_snapshot_integrity(self.snapshot)
        self.assertEqual(first, validate_schema2_snapshot_integrity(self.snapshot))
        restored = decode_editorial_versioned(encode_editorial_versioned(self.snapshot))
        self.assertEqual(validate_schema2_snapshot_integrity(restored), first)
        self.assertEqual(self.snapshot, before)
        self.assertEqual(restored.base_snapshot.base.revisions, before.base_snapshot.base.revisions)

    def test_failure_does_not_mutate_inputs(self):
        evidence = replace(self.snapshot.approval_authority_evidence[0], principal_display_name='Changed')
        snapshot = seal2(replace(self.snapshot, approval_authority_evidence=(evidence,)))
        before = copy.deepcopy(snapshot)
        with self.assertRaises(Schema2IntegrityError):
            validate_schema2_snapshot_integrity(snapshot)
        self.assertEqual(snapshot, before)

    def test_no_authority_identity_signature_or_anchor_claims(self):
        record = self.template.base.approvals[0]
        evidence = evidence_for(record, principal_id='windows-sid:S-1-999999',
                                authority_policy_version='unknown-policy')
        result = validate_schema2_snapshot_integrity(seal2(Schema2Snapshot(self.template, (evidence,))))
        self.assertEqual(result.approval_statuses[0].authority_status, 'EVIDENCE_PRESENT_UNVERIFIED')
        self.assertEqual(result.transaction_order_status, 'UNVERIFIED_ORDERING')

    def test_no_io_network_or_subprocess_side_effects(self):
        payload = encode_editorial_versioned(self.snapshot)
        code = '''
import sys
active = False
def guard(event, args):
    if active and (event == 'open' or event.startswith(('socket.', 'subprocess.', 'os.system'))):
        raise AssertionError(event)
sys.addaudithook(guard)
from editorial.versioned_codec import decode_editorial_versioned
from editorial.schema2_integrity import canonical_schema2_snapshot_bytes, compute_schema2_snapshot_checksum, validate_schema2_snapshot_integrity
snapshot = decode_editorial_versioned(PAYLOAD)
active = True
assert canonical_schema2_snapshot_bytes(snapshot)
assert len(compute_schema2_snapshot_checksum(snapshot)) == 64
assert validate_schema2_snapshot_integrity(snapshot).checksum_verified
'''.replace('PAYLOAD', repr(payload))
        result = subprocess.run([sys.executable, '-B', '-c', code],
                                cwd=Path(__file__).resolve().parents[1], capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '')

    def test_no_clock_environment_random_ids_or_filesystem_writes(self):
        import editorial.schema2_model as s2
        with ExitStack() as stack:
            for target in ('builtins.open', 'io.open', 'os.open', 'os.getenv', 'os.urandom',
                           'uuid.uuid4', 'time.time', 'time.monotonic', 'time.perf_counter',
                           'socket.socket', 'subprocess.Popen'):
                stack.enter_context(patch(target, side_effect=AssertionError(f'Forbidden: {target}')))
            for module in (c, s2):
                datetime = stack.enter_context(patch.object(module, 'datetime', wraps=module.datetime))
                for method in ('now', 'utcnow', 'today'):
                    getattr(datetime, method).side_effect = AssertionError('Clock access')
            self.assertTrue(validate_schema2_snapshot_integrity(self.snapshot).checksum_verified)
            wrong = replace(self.snapshot, base_snapshot=replace(self.snapshot.base_snapshot, snapshot_checksum='0' * 64))
            with self.assertRaises(Schema2IntegrityError):
                validate_schema2_snapshot_integrity(wrong)


if __name__ == '__main__':
    unittest.main()
