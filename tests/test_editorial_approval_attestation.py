"""Fixed independent vectors and regression tests for pure attestation binding."""
import base64
import copy
from contextlib import ExitStack
from dataclasses import fields, replace
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from editorial import codec as c
from editorial import model as m
from editorial.approval_attestation import (
    ApprovalAttestationError,
    canonical_attestation_bytes,
    canonical_signed_bytes,
    compute_attestation_digest,
    validate_attestation_digest,
)
from editorial.schema2_model import ApprovalAuthorityEvidence, Schema2ModelError, Schema2Snapshot
from editorial.versioned_codec import decode_editorial_versioned, encode_editorial_versioned


def uid(number):
    return f'30000000-0000-0000-0000-{number:012d}'


def models(vector):
    approval = copy.deepcopy(vector['approval_record'])
    approval['object_ref']['kind'] = m.ObjectKind(approval['object_ref']['kind'])
    approval['object_ref'] = m.RevisionRef(**approval['object_ref'])
    approval['decision'] = m.ApprovalDecision(approval['decision'])
    approval['review_declarations'] = tuple(approval['review_declarations'])
    evidence = copy.deepcopy(vector['authority_evidence'])
    evidence['declaration_codes'] = tuple(evidence['declaration_codes'])
    return m.ApprovalRecord(**approval), ApprovalAuthorityEvidence(**evidence)


class ApprovalAttestationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fixture = Path(__file__).parent / 'fixtures' / 'editorial_attestation_vectors.json'
        cls.vectors = json.loads(fixture.read_text(encoding='utf-8'))['vectors']

    def setUp(self):
        self.approval, self.evidence = models(self.vectors[0])

    def error(self, function, approval, evidence, code, path):
        with self.assertRaises(ApprovalAttestationError) as caught:
            function(approval, evidence)
        self.assertIsInstance(caught.exception, Schema2ModelError)
        self.assertIs(type(caught.exception.violation), m.Violation)
        self.assertEqual(caught.exception.violation.code, code)
        self.assertEqual(caught.exception.violation.field_path, path)
        return caught.exception.violation

    def test_golden_canonical_bytes(self):
        for vector in self.vectors:
            with self.subTest(vector=vector['name']):
                self.assertEqual(canonical_attestation_bytes(*models(vector)),
                                 bytes.fromhex(vector['canonical_utf8_hex']))

    def test_golden_sha256(self):
        for vector in self.vectors:
            with self.subTest(vector=vector['name']):
                digest = compute_attestation_digest(*models(vector))
                self.assertEqual(digest, vector['sha256'])
                self.assertRegex(digest, r'\A[0-9a-f]{64}\Z')

    def test_golden_signed_bytes(self):
        for vector in self.vectors:
            with self.subTest(vector=vector['name']):
                self.assertEqual(canonical_signed_bytes(*models(vector)),
                                 bytes.fromhex(vector['signed_bytes_hex']))

    def test_validate_all_golden_digests(self):
        for vector in self.vectors:
            with self.subTest(vector=vector['name']):
                self.assertIsNone(validate_attestation_digest(*models(vector)))

    def test_exact_payload_field_sets_and_wire_values(self):
        payload = json.loads(canonical_attestation_bytes(self.approval, self.evidence))
        self.assertEqual(set(payload), {'approval_authority_evidence_schema_version',
                                        'approval_record', 'authority_evidence'})
        self.assertIs(type(payload['approval_authority_evidence_schema_version']), int)
        self.assertEqual(payload['approval_authority_evidence_schema_version'], 1)
        self.assertEqual(payload['approval_record'], self.vectors[0]['approval_record'])
        self.assertEqual(set(payload['approval_record']), {
            'id', 'gate', 'object_ref', 'dependency_digest', 'policy_version',
            'actor', 'timestamp', 'decision', 'reason', 'review_declarations'})
        self.assertEqual(set(payload['authority_evidence']), {
            'approval_id', 'principal_id', 'principal_display_name', 'authority_policy_id',
            'authority_policy_version', 'review_session_id', 'request_id',
            'declaration_codes', 'attested_at', 'reconsiders_record_id'})
        self.assertEqual(set(payload['approval_record']['object_ref']),
                         {'kind', 'id', 'revision', 'content_hash'})
        self.assertEqual(payload['approval_record']['decision'], 'approve')
        self.assertEqual(payload['approval_record']['object_ref']['kind'], 'script')

    def test_deterministic_repeated_calls(self):
        for vector in self.vectors:
            pair = models(vector)
            for _ in range(3):
                self.assertEqual(canonical_attestation_bytes(*pair), bytes.fromhex(vector['canonical_utf8_hex']))
                self.assertEqual(compute_attestation_digest(*pair), vector['sha256'])
                self.assertEqual(canonical_signed_bytes(*pair), bytes.fromhex(vector['signed_bytes_hex']))

    def test_each_approval_core_field_changes_digest(self):
        changes = {
            'gate': 'SCENES',
            'object_ref': replace(self.approval.object_ref, id=uid(777), revision=2, content_hash='f' * 64),
            'dependency_digest': 'f' * 64,
            'policy_version': 'editorial-v2',
            'actor': 'Другой рецензент',
            'timestamp': '2026-11-05T10:00:02Z',
            'decision': m.ApprovalDecision.REJECT,
            'reason': 'Інша причина',
            'review_declarations': ('Другая декларация',),
        }
        self.assertEqual(set(changes) | {'id'}, {field.name for field in fields(m.ApprovalRecord)})
        for name, value in changes.items():
            with self.subTest(field=name):
                self.assertNotEqual(compute_attestation_digest(replace(self.approval, **{name: value}), self.evidence),
                                    self.vectors[0]['sha256'])

    def test_changed_linked_approval_ids_change_digest(self):
        approval = replace(self.approval, id=uid(777))
        evidence = replace(self.evidence, approval_id=approval.id)
        self.assertNotEqual(compute_attestation_digest(approval, evidence), self.vectors[0]['sha256'])

    def test_each_revision_ref_field_changes_digest(self):
        changes = {'kind': m.ObjectKind.SCENE_PLAN, 'id': uid(888),
                   'revision': 8, 'content_hash': 'd' * 64}
        self.assertEqual(set(changes), {field.name for field in fields(m.RevisionRef)})
        for name, value in changes.items():
            with self.subTest(field=name):
                approval = replace(self.approval, object_ref=replace(self.approval.object_ref, **{name: value}))
                self.assertNotEqual(compute_attestation_digest(approval, self.evidence), self.vectors[0]['sha256'])

    def test_each_evidence_core_field_changes_digest(self):
        changes = {
            'principal_id': 'windows-sid:S-1-5-123',
            'principal_display_name': 'Інше ім’я',
            'authority_policy_id': uid(888),
            'authority_policy_version': 'offline-v2',
            'review_session_id': uid(889),
            'request_id': uid(890),
            'declaration_codes': ('NO_UNSUPPORTED_REVIEW_CLAIM',),
            'attested_at': '2026-11-05T10:00:03Z',
            'reconsiders_record_id': uid(891),
        }
        excluded = {'attestation_digest', 'signing_key_id', 'signature_algorithm', 'signature'}
        self.assertEqual(set(changes) | {'approval_id'} | excluded,
                         {field.name for field in fields(ApprovalAuthorityEvidence)})
        for name, value in changes.items():
            with self.subTest(field=name):
                self.assertNotEqual(compute_attestation_digest(self.approval, replace(self.evidence, **{name: value})),
                                    self.vectors[0]['sha256'])

    def test_review_declaration_array_order_preserved(self):
        approval = replace(self.approval, review_declarations=self.approval.review_declarations[::-1])
        payload = json.loads(canonical_attestation_bytes(approval, self.evidence))
        self.assertEqual(payload['approval_record']['review_declarations'], list(approval.review_declarations))
        self.assertNotEqual(compute_attestation_digest(approval, self.evidence), self.vectors[0]['sha256'])

    def test_evidence_declaration_array_order_preserved_without_evaluation(self):
        # Locally valid evidence; cross-model declaration eligibility is outside this API.
        evidence = replace(self.evidence, declaration_codes=self.evidence.declaration_codes[::-1])
        payload = json.loads(canonical_attestation_bytes(self.approval, evidence))
        self.assertEqual(payload['authority_evidence']['declaration_codes'], list(evidence.declaration_codes))
        self.assertNotEqual(compute_attestation_digest(self.approval, evidence), self.vectors[0]['sha256'])

    def test_composed_and_decomposed_golden_vectors_differ(self):
        self.assertNotEqual(self.vectors[2]['canonical_utf8_hex'], self.vectors[3]['canonical_utf8_hex'])
        self.assertNotEqual(self.vectors[2]['sha256'], self.vectors[3]['sha256'])
        for vector in self.vectors[2:]:
            self.assertIn(vector['approval_record']['actor'].encode('utf-8'),
                          canonical_attestation_bytes(*models(vector)))

    def test_no_normalization_of_individual_text_fields(self):
        for name in ('actor', 'reason', 'policy_version'):
            with self.subTest(approval_field=name):
                first = compute_attestation_digest(replace(self.approval, **{name: 'Й'}), self.evidence)
                second = compute_attestation_digest(replace(self.approval, **{name: 'И\u0306'}), self.evidence)
                self.assertNotEqual(first, second)
        for name in ('principal_display_name', 'authority_policy_version'):
            with self.subTest(evidence_field=name):
                first = compute_attestation_digest(self.approval, replace(self.evidence, **{name: 'é'}))
                second = compute_attestation_digest(self.approval, replace(self.evidence, **{name: 'e\u0301'}))
                self.assertNotEqual(first, second)

    def test_unicode_emoji_and_whitespace_preserved(self):
        encoded = canonical_attestation_bytes(self.approval, self.evidence)
        self.assertIn('  Рецензент / Рецензентка Їжак И\u0306 😀  '.encode('utf-8'), encoded)
        self.assertNotIn(b'\\u', encoded)
        payload = json.loads(encoded)
        self.assertEqual(payload['approval_record']['reason'], '  Перевірка / проверка "текст"\n😀  ')
        self.assertEqual(payload['authority_evidence']['authority_policy_version'], '  offline-v1  ')

    def test_whitespace_and_case_changes_are_not_hidden(self):
        for actor in (self.approval.actor.strip(), self.approval.actor.upper()):
            self.assertNotEqual(compute_attestation_digest(replace(self.approval, actor=actor), self.evidence),
                                self.vectors[0]['sha256'])

    def test_null_reconsideration_is_explicit(self):
        encoded = canonical_attestation_bytes(self.approval, self.evidence)
        self.assertIn(b'"reconsiders_record_id":null', encoded)

    def test_non_null_reconsideration_is_exact(self):
        pair = models(self.vectors[1])
        payload = json.loads(canonical_attestation_bytes(*pair))
        self.assertEqual(payload['authority_evidence']['reconsiders_record_id'], uid(999))

    def test_excluded_fields_never_enter_payload(self):
        for vector in self.vectors:
            payload = json.loads(canonical_attestation_bytes(*models(vector)))
            for field in ('attestation_digest', 'signing_key_id', 'signature_algorithm', 'signature'):
                self.assertNotIn(field, payload['authority_evidence'])

    def test_initial_digest_can_be_computed_with_placeholder(self):
        evidence = replace(self.evidence, attestation_digest='0' * 64)
        self.assertEqual(compute_attestation_digest(self.approval, evidence), self.vectors[0]['sha256'])
        self.assertEqual(canonical_attestation_bytes(self.approval, evidence),
                         bytes.fromhex(self.vectors[0]['canonical_utf8_hex']))
        self.assertEqual(canonical_signed_bytes(self.approval, evidence),
                         bytes.fromhex(self.vectors[0]['signed_bytes_hex']))

    def test_signed_unsigned_and_changed_signature_tuples_have_same_digest(self):
        signature = base64.urlsafe_b64encode(bytes([8]) * 64).decode('ascii').rstrip('=')
        pair = models(self.vectors[1])
        evidence_variants = (
            pair[1],
            replace(pair[1], signing_key_id=None, signature_algorithm=None, signature=None),
            replace(pair[1], signing_key_id='another-key', signature=signature),
        )
        for evidence in evidence_variants:
            self.assertEqual(compute_attestation_digest(pair[0], evidence), self.vectors[1]['sha256'])
            self.assertEqual(canonical_signed_bytes(pair[0], evidence),
                             bytes.fromhex(self.vectors[1]['signed_bytes_hex']))

    def test_digest_mismatch_has_exact_structured_path(self):
        evidence = replace(self.evidence, attestation_digest='0' * 64)
        self.error(validate_attestation_digest, self.approval, evidence,
                   'ATTESTATION_DIGEST_MISMATCH', '$.authority_evidence.attestation_digest')
        self.assertEqual(evidence.attestation_digest, '0' * 64)

    def test_changed_core_with_old_digest_fails_closed(self):
        self.error(validate_attestation_digest, replace(self.approval, actor='Другой'), self.evidence,
                   'ATTESTATION_DIGEST_MISMATCH', '$.authority_evidence.attestation_digest')

    def test_id_mismatch_precedes_digest_mismatch_for_every_api(self):
        evidence = replace(self.evidence, approval_id=uid(999), attestation_digest='0' * 64)
        for function in (canonical_attestation_bytes, compute_attestation_digest,
                         validate_attestation_digest, canonical_signed_bytes):
            with self.subTest(api=function.__name__):
                self.error(function, self.approval, evidence, 'APPROVAL_ID_MISMATCH',
                           '$.authority_evidence.approval_id')

    def test_exact_argument_types_for_every_api(self):
        class ApprovalSubclass(m.ApprovalRecord):
            pass

        class EvidenceSubclass(ApprovalAuthorityEvidence):
            pass

        derived_approval = ApprovalSubclass(**{f.name: getattr(self.approval, f.name) for f in fields(self.approval)})
        derived_evidence = EvidenceSubclass(**{f.name: getattr(self.evidence, f.name) for f in fields(self.evidence)})
        for function in (canonical_attestation_bytes, compute_attestation_digest,
                         validate_attestation_digest, canonical_signed_bytes):
            for value in (None, {}, self.vectors[0]['approval_record'], 'approval', True, derived_approval):
                with self.subTest(api=function.__name__, argument='approval', type=type(value)):
                    self.error(function, value, self.evidence, 'INVALID_APPROVAL_TYPE', '$.approval_record')
            for value in (None, {}, self.vectors[0]['authority_evidence'], 'evidence', True, derived_evidence):
                with self.subTest(api=function.__name__, argument='evidence', type=type(value)):
                    self.error(function, self.approval, value, 'INVALID_EVIDENCE_TYPE', '$.authority_evidence')

    def test_invalid_unicode_in_locally_constructible_approval_is_structured(self):
        for field in ('actor', 'reason', 'policy_version'):
            for surrogate in ('\ud800', '\udfff'):
                with self.subTest(field=field, surrogate=repr(surrogate)):
                    approval = replace(self.approval, **{field: 'text' + surrogate})
                    self.error(canonical_attestation_bytes, approval, self.evidence,
                               'UNICODE', f'$.approval_record.{field}')

    def test_invalid_unicode_in_review_declarations_has_index(self):
        approval = replace(self.approval, review_declarations=('valid', '\ud800'))
        self.error(canonical_attestation_bytes, approval, self.evidence,
                   'UNICODE', '$.approval_record.review_declarations[1]')

    def test_weak_legacy_gate_and_timestamp_must_match_wire_contract(self):
        for field, value, code in (('gate', 'UNKNOWN', 'VALUE'),
                                   ('timestamp', '2026-02-30T10:00:00Z', 'DATE'),
                                   ('timestamp', '2026-11-05T12:00:00+02:00', 'DATE')):
            with self.subTest(field=field, value=value):
                self.error(canonical_attestation_bytes, replace(self.approval, **{field: value}),
                           self.evidence, code, f'$.approval_record.{field}')

    def test_serialization_failures_are_structured(self):
        for exception in (TypeError('unsupported'), ValueError('non-finite'), OverflowError('overflow')):
            with self.subTest(exception=type(exception).__name__):
                with patch('editorial.approval_attestation.json.dumps', side_effect=exception):
                    self.error(canonical_attestation_bytes, self.approval, self.evidence,
                               'ATTESTATION_SERIALIZATION_ERROR', '$')

    def test_inputs_unchanged_on_success_and_failure(self):
        before = copy.deepcopy((self.approval, self.evidence))
        canonical_attestation_bytes(self.approval, self.evidence)
        compute_attestation_digest(self.approval, self.evidence)
        canonical_signed_bytes(self.approval, self.evidence)
        validate_attestation_digest(self.approval, self.evidence)
        self.assertEqual((self.approval, self.evidence), before)
        wrong = replace(self.evidence, attestation_digest='0' * 64)
        wrong_before = copy.deepcopy(wrong)
        with self.assertRaises(ApprovalAttestationError):
            validate_attestation_digest(self.approval, wrong)
        self.assertEqual(wrong, wrong_before)

    def test_no_filesystem_network_clock_environment_or_id_generation(self):
        forbidden = ('builtins.open', 'io.open', 'os.open', 'os.listdir', 'os.stat',
                     'os.getenv', 'os.urandom', 'socket.socket', 'socket.create_connection',
                     'time.time', 'time.monotonic', 'time.perf_counter',
                     'uuid.uuid4', 'subprocess.Popen')
        with ExitStack() as stack:
            for target in forbidden:
                stack.enter_context(patch(target, side_effect=AssertionError(f'Forbidden side effect: {target}')))
            datetime = stack.enter_context(patch.object(c, 'datetime', wraps=c.datetime))
            for name in ('now', 'utcnow', 'today'):
                getattr(datetime, name).side_effect = AssertionError('Clock access')
            self.assertEqual(canonical_attestation_bytes(self.approval, self.evidence),
                             bytes.fromhex(self.vectors[0]['canonical_utf8_hex']))
            self.assertEqual(compute_attestation_digest(self.approval, self.evidence), self.vectors[0]['sha256'])
            self.assertIsNone(validate_attestation_digest(self.approval, self.evidence))
            self.assertEqual(canonical_signed_bytes(self.approval, self.evidence),
                             bytes.fromhex(self.vectors[0]['signed_bytes_hex']))
            with self.assertRaises(ApprovalAttestationError):
                validate_attestation_digest(self.approval, replace(self.evidence, attestation_digest='0' * 64))

    def test_schema2_codec_round_trip_preserves_golden_binding(self):
        for vector in self.vectors:
            with self.subTest(vector=vector['name']):
                approval, evidence = models(vector)
                base = m.ContractSnapshot(m.EditorialSnapshot(uid(900), 1, approvals=(approval,)),
                                          (), (), (), (), '0' * 64)
                snapshot = Schema2Snapshot(base, (evidence,))
                encoded = encode_editorial_versioned(snapshot)
                restored = decode_editorial_versioned(encoded)
                pair = (restored.base_snapshot.base.approvals[0], restored.approval_authority_evidence[0])
                self.assertEqual(pair, (approval, evidence))
                self.assertEqual(compute_attestation_digest(*pair), vector['sha256'])
                self.assertEqual(canonical_attestation_bytes(*pair), bytes.fromhex(vector['canonical_utf8_hex']))
                self.assertEqual(encode_editorial_versioned(restored), encoded)

    def test_schema1_codec_behavior_unchanged(self):
        snapshot = m.ContractSnapshot(m.EditorialSnapshot(uid(900), 1, approvals=(self.approval,)),
                                      (), (), (), (), '0' * 64)
        encoded = c.encode_snapshot(snapshot)
        canonical_attestation_bytes(self.approval, self.evidence)
        self.assertEqual(c.decode_snapshot(encoded), snapshot)
        self.assertEqual(encode_editorial_versioned(snapshot), encoded)
        self.assertEqual(decode_editorial_versioned(encoded), snapshot)
        self.assertNotIn('approval_authority_evidence', json.loads(encoded))

    def test_digest_validation_does_not_claim_authority_or_readiness(self):
        evidence = replace(self.evidence, principal_id='windows-sid:S-1-999999',
                           authority_policy_id=uid(987), authority_policy_version='unknown-policy',
                           reconsiders_record_id=uid(986))
        # No policy, target history, signature, trusted head or clock is consulted.
        evidence = replace(evidence, attestation_digest=compute_attestation_digest(self.approval, evidence))
        self.assertIsNone(validate_attestation_digest(self.approval, evidence))
        self.assertIs(type(compute_attestation_digest(self.approval, evidence)), str)
        self.assertIs(type(canonical_signed_bytes(self.approval, evidence)), bytes)

    def test_domain_separator_has_exactly_one_nul_and_no_wrapper(self):
        signed = canonical_signed_bytes(self.approval, self.evidence)
        domain = b'story-studio-approval-attestation-v1\x00'
        self.assertEqual(signed[:len(domain)], domain)
        self.assertEqual(signed[len(domain):], bytes.fromhex(self.vectors[0]['canonical_utf8_hex']))


if __name__ == '__main__':
    unittest.main()
