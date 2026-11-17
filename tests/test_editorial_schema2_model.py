import base64
from dataclasses import FrozenInstanceError, replace
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import unittest

from editorial import model as m
from editorial.package import PackageGate
from editorial.schema2_model import (
    ApprovalAuthorityEvidence,
    HANDOFF_APPROVE_DECLARATION_CODES,
    NON_APPROVE_DECLARATION_CODES,
    SCENES_APPROVE_DECLARATION_CODES,
    SCRIPT_APPROVE_DECLARATION_CODES,
    Schema2ModelError,
    Schema2Snapshot,
    required_declaration_codes,
)


ZERO_HASH = '0' * 64
SIGNATURE = base64.urlsafe_b64encode(bytes(range(64))).decode('ascii').rstrip('=')


def uid(number):
    return f'00000000-0000-0000-0000-{number:012d}'


def approval(number=1):
    return m.ApprovalRecord(
        uid(number), 'SCRIPT',
        m.RevisionRef(m.ObjectKind.SCRIPT, uid(100 + number), 1, ZERO_HASH),
        ZERO_HASH, '1', 'Reviewer', '2026-01-01T00:00:00Z',
        m.ApprovalDecision.APPROVE, 'Reviewed', (),
    )


def contract_snapshot(approvals=()):
    return m.ContractSnapshot(
        m.EditorialSnapshot(uid(900), 1, approvals=tuple(approvals)),
        (), (), (), (), ZERO_HASH,
    )


def evidence(number=1, **changes):
    values = dict(
        approval_id=uid(number),
        principal_id='windows-sid:S-1-5-21',
        principal_display_name='Рецензент',
        authority_policy_id=uid(500),
        authority_policy_version='policy-1',
        review_session_id=uid(600 + number),
        request_id=uid(700 + number),
        declaration_codes=SCRIPT_APPROVE_DECLARATION_CODES,
        attested_at='2026-11-05T12:34:56Z',
        reconsiders_record_id=None,
        attestation_digest='a' * 64,
        signing_key_id=None,
        signature_algorithm=None,
        signature=None,
    )
    values.update(changes)
    return ApprovalAuthorityEvidence(**values)


class ApprovalAuthorityEvidenceTests(unittest.TestCase):
    def assert_code(self, code, function):
        with self.assertRaises(Schema2ModelError) as caught:
            function()
        self.assertEqual(caught.exception.violation.code, code)

    def test_unsigned_evidence(self):
        self.assertIsNone(evidence().signature)

    def test_syntactically_signed_evidence(self):
        value = evidence(signing_key_id='offline:key.1',
                         signature_algorithm='ed25519', signature=SIGNATURE)
        self.assertEqual(value.signature, SIGNATURE)

    def test_frozen(self):
        value = evidence()
        with self.assertRaises(FrozenInstanceError):
            value.approval_id = uid(2)

    def test_list_declarations_rejected(self):
        self.assert_code('INVALID_DECLARATION',
                         lambda: evidence(declaration_codes=list(SCRIPT_APPROVE_DECLARATION_CODES)))

    def test_uuid_must_be_canonical(self):
        uppercase = 'AAAAAAAA-0000-0000-0000-000000000001'
        self.assert_code('INVALID_UUID', lambda: evidence(approval_id=uppercase))

    def test_windows_sid(self):
        self.assertEqual(evidence(principal_id='windows-sid:S-1-5-21').principal_id,
                         'windows-sid:S-1-5-21')

    def test_posix_principal(self):
        principal = 'posix-uid:1000@machine:' + 'a' * 32
        self.assertEqual(evidence(principal_id=principal).principal_id, principal)

    def test_posix_zero_uid_is_canonical(self):
        principal = 'posix-uid:0@machine:' + '0' * 32
        self.assertEqual(evidence(principal_id=principal).principal_id, principal)

    def test_bad_principal_prefix_and_leading_zero(self):
        for principal in ('sid:S-1-5', 'windows-sid:s-1-5',
                          'posix-uid:01@machine:' + 'a' * 32):
            with self.subTest(principal=principal):
                self.assert_code('INVALID_PRINCIPAL', lambda p=principal: evidence(principal_id=p))

    def test_unicode_is_not_normalized(self):
        decomposed = 'І' + 'и\u0306'
        self.assertEqual(evidence(principal_display_name=decomposed).principal_display_name,
                         decomposed)

    def test_surrogate_rejected(self):
        self.assert_code('INVALID_TEXT', lambda: evidence(principal_display_name='bad\ud800'))

    def test_display_name_bounds(self):
        for value in ('', 'x' * 257):
            self.assert_code('INVALID_TEXT', lambda v=value: evidence(principal_display_name=v))
        self.assertEqual(len(evidence(principal_display_name='x' * 256).principal_display_name), 256)

    def test_policy_version_bounds_and_surrogate(self):
        for value in ('', 'x' * 129, 'bad\udfff'):
            self.assert_code('INVALID_TEXT', lambda v=value: evidence(authority_policy_version=v))

    def test_digest_is_canonical_sha256(self):
        for value in ('A' * 64, 'a' * 63, 1):
            self.assert_code('INVALID_DIGEST', lambda v=value: evidence(attestation_digest=v))

    def test_utc_seconds(self):
        for value in ('2026-02-29T00:00:00Z', '2026-01-01T00:00:00.1Z',
                      '2026-01-01T00:00:00+00:00'):
            self.assert_code('INVALID_TIMESTAMP', lambda v=value: evidence(attested_at=v))

    def test_signature_all_null(self):
        value = evidence()
        self.assertEqual((value.signing_key_id, value.signature_algorithm, value.signature),
                         (None, None, None))

    def test_signature_all_present(self):
        value = evidence(signing_key_id='key-1', signature_algorithm='ed25519', signature=SIGNATURE)
        self.assertEqual(value.signature_algorithm, 'ed25519')

    def test_incomplete_signature(self):
        self.assert_code('INCOMPLETE_SIGNATURE',
                         lambda: evidence(signing_key_id='key-1'))

    def test_wrong_signature_algorithm(self):
        self.assert_code('INVALID_SIGNATURE_FORMAT', lambda: evidence(
            signing_key_id='key-1', signature_algorithm='Ed25519', signature=SIGNATURE))

    def test_bad_signing_key_id(self):
        self.assert_code('INVALID_SIGNATURE_FORMAT', lambda: evidence(
            signing_key_id=' bad', signature_algorithm='ed25519', signature=SIGNATURE))

    def test_noncanonical_base64url(self):
        self.assert_code('INVALID_SIGNATURE_FORMAT', lambda: evidence(
            signing_key_id='key', signature_algorithm='ed25519', signature=SIGNATURE + '='))

    def test_wrong_signature_length(self):
        short = base64.urlsafe_b64encode(b'x' * 63).decode().rstrip('=')
        self.assert_code('INVALID_SIGNATURE_FORMAT', lambda: evidence(
            signing_key_id='key', signature_algorithm='ed25519', signature=short))

    def test_self_reconsideration_rejected(self):
        self.assert_code('SELF_REFERENCE', lambda: evidence(reconsiders_record_id=uid(1)))

    def test_duplicate_declaration_rejected(self):
        self.assert_code('DUPLICATE_DECLARATION', lambda: evidence(
            declaration_codes=('NO_UNSUPPORTED_REVIEW_CLAIM',) * 2))

    def test_unknown_and_empty_declarations_rejected(self):
        for codes in ((), ('UNKNOWN',)):
            self.assert_code('INVALID_DECLARATION', lambda c=codes: evidence(declaration_codes=c))


class DeclarationVocabularyTests(unittest.TestCase):
    def test_script_approve_vocabulary(self):
        self.assertEqual(required_declaration_codes(PackageGate.SCRIPT, m.ApprovalDecision.APPROVE),
                         SCRIPT_APPROVE_DECLARATION_CODES)

    def test_scenes_approve_vocabulary(self):
        self.assertEqual(required_declaration_codes('SCENES', 'approve'),
                         SCENES_APPROVE_DECLARATION_CODES)

    def test_handoff_approve_vocabulary(self):
        self.assertEqual(required_declaration_codes('HANDOFF', m.ApprovalDecision.APPROVE),
                         HANDOFF_APPROVE_DECLARATION_CODES)

    def test_all_nonapprove_decisions_share_vocabulary(self):
        for decision in (m.ApprovalDecision.REJECT, m.ApprovalDecision.REVISE,
                         m.ApprovalDecision.REVOKE):
            self.assertEqual(required_declaration_codes('SCRIPT', decision),
                             NON_APPROVE_DECLARATION_CODES)

    def test_bad_gate_and_decision_rejected(self):
        with self.assertRaises(Schema2ModelError):
            required_declaration_codes('script', m.ApprovalDecision.APPROVE)
        with self.assertRaises(Schema2ModelError):
            required_declaration_codes('SCRIPT', 'APPROVE')


class Schema2SnapshotTests(unittest.TestCase):
    def assert_code(self, code, function):
        with self.assertRaises(Schema2ModelError) as caught:
            function()
        self.assertEqual(caught.exception.violation.code, code)

    def test_legacy_approvals_need_no_evidence(self):
        value = Schema2Snapshot(contract_snapshot((approval(1),)), ())
        self.assertEqual(value.approval_authority_evidence, ())
        self.assertEqual(value.editorial_schema_version, 2)

    def test_evidence_collection_must_be_tuple(self):
        self.assert_code('INVALID_TYPE',
                         lambda: Schema2Snapshot(contract_snapshot((approval(1),)), [evidence(1)]))

    def test_duplicate_approval_evidence(self):
        snapshot = contract_snapshot((approval(1), approval(2)))
        second = replace(evidence(1), review_session_id=uid(699), request_id=uid(799))
        self.assert_code('DUPLICATE_EVIDENCE',
                         lambda: Schema2Snapshot(snapshot, (evidence(1), second)))

    def test_duplicate_request(self):
        snapshot = contract_snapshot((approval(1), approval(2)))
        second = evidence(2, request_id=evidence(1).request_id)
        self.assert_code('DUPLICATE_REQUEST',
                         lambda: Schema2Snapshot(snapshot, (evidence(1), second)))

    def test_duplicate_review_session(self):
        snapshot = contract_snapshot((approval(1), approval(2)))
        second = evidence(2, review_session_id=evidence(1).review_session_id)
        self.assert_code('DUPLICATE_SESSION',
                         lambda: Schema2Snapshot(snapshot, (evidence(1), second)))

    def test_evidence_order_follows_approvals(self):
        snapshot = contract_snapshot((approval(1), approval(2)))
        self.assert_code('INVALID_EVIDENCE_ORDER',
                         lambda: Schema2Snapshot(snapshot, (evidence(2), evidence(1))))

    def test_legacy_gaps_preserve_relative_order(self):
        snapshot = contract_snapshot((approval(1), approval(2), approval(3)))
        value = Schema2Snapshot(snapshot, (evidence(1), evidence(3)))
        self.assertEqual(tuple(v.approval_id for v in value.approval_authority_evidence),
                         (uid(1), uid(3)))

    def test_evidence_must_link_existing_approval(self):
        self.assert_code('INVALID_EVIDENCE_ORDER',
                         lambda: Schema2Snapshot(contract_snapshot((approval(1),)), (evidence(2),)))

    def test_declarations_match_linked_gate_and_decision(self):
        self.assert_code('INVALID_DECLARATION', lambda: Schema2Snapshot(
            contract_snapshot((approval(1),)),
            (evidence(1, declaration_codes=SCENES_APPROVE_DECLARATION_CODES),)))

    def test_evidence_cannot_outnumber_approvals(self):
        self.assert_code('EXCESSIVE_COLLECTION_SIZE', lambda: Schema2Snapshot(
            contract_snapshot((approval(1),)), (evidence(1), evidence(2))))

    def test_collection_limit(self):
        self.assert_code('EXCESSIVE_COLLECTION_SIZE', lambda: Schema2Snapshot(
            contract_snapshot(), (evidence(1),) * 10_001))

    def test_explicit_schema_version_is_two(self):
        self.assert_code('SCHEMA_VERSION_UNSUPPORTED', lambda: Schema2Snapshot(
            contract_snapshot(), (), editorial_schema_version=1))

    def test_schema1_models_remain_schema1(self):
        base = contract_snapshot()
        self.assertEqual(base.base.editorial_schema_version, 1)
        with self.assertRaises(m.ModelError):
            m.EditorialSnapshot(uid(900), 1, editorial_schema_version=2)

    def test_models_do_not_perform_file_or_network_io(self):
        original_open = open
        original_socket = socket.socket
        try:
            import builtins
            builtins.open = lambda *args, **kwargs: self.fail('unexpected file I/O')
            socket.socket = lambda *args, **kwargs: self.fail('unexpected network I/O')
            Schema2Snapshot(contract_snapshot((approval(1),)), (evidence(1),))
            required_declaration_codes('SCRIPT', 'approve')
        finally:
            builtins.open = original_open
            socket.socket = original_socket

    def test_import_has_no_external_side_effects(self):
        repository = str(Path(__file__).resolve().parents[1])
        script = (
            'import os, socket, sys\n'
            'before=set(os.listdir("."))\n'
            'def audit(event, args):\n'
            '    if event.startswith("socket.") or event.startswith("subprocess.") or event == "os.system":\n'
            '        raise RuntimeError(event)\n'
            'sys.addaudithook(audit)\n'
            'import editorial.schema2_model\n'
            'assert set(os.listdir(".")) == before\n'
        )
        with tempfile.TemporaryDirectory() as directory:
            environment = os.environ.copy()
            environment['PYTHONPATH'] = repository
            result = subprocess.run(
                [sys.executable, '-c', script], cwd=directory, env=environment,
                capture_output=True, text=True, check=False,
            )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == '__main__':
    unittest.main()
