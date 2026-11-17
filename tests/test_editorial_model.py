"""Focused E01.1 constructor, immutability and isolation tests (stdlib)."""
from dataclasses import FrozenInstanceError, replace
import subprocess
import sys
import unittest
from pathlib import Path

from editorial import (
    ApprovalDecision, ApprovalRecord, ClaimRevision, ClaimType, ContentMode,
    EditorialRevision, EditorialSnapshot, EvidenceLink, EvidenceRelation,
    Locale, ModelError, ObjectKind, ProductionRevision, RevisionRef,
    RightsReview, RightsStatus, SourceRevision, Violation,
)

ID = '10000000-0000-0000-0000-000000000001'
HASH = 'a' * 64


def ref(kind=ObjectKind.PRODUCTION):
    return RevisionRef(kind, ID, 1, HASH)


class EditorialModelTests(unittest.TestCase):
    def production(self):
        return ProductionRevision(ref(), 'Тема', ref(ObjectKind.GENRE_PROFILE),
                                  ContentMode.FACTUAL, Locale.UK, Locale.UK,
                                  Locale.UK, Locale.RU, 'test', '9:16',
                                  '2026-11-04T10:00:00Z')

    def test_valid_ref_preserves_identity(self):
        value = ref()
        self.assertEqual((value.id, value.revision, value.content_hash), (ID, 1, HASH))

    def test_enum_values_and_invalid_values(self):
        for cls, valid in ((ContentMode, 'hybrid'), (Locale, 'uk'),
                           (ObjectKind, 'script'), (ApprovalDecision, 'revoke'),
                           (RightsStatus, 'unknown'), (ClaimType, 'fictional'),
                           (EvidenceRelation, 'contradicts')):
            with self.subTest(enum=cls.__name__):
                self.assertEqual(cls(valid).value, valid)
                with self.assertRaises(ValueError):
                    cls('unsupported')

    def test_revision_strict_positive_integer(self):
        for value in (0, -1, True, False, 1.0, '1', None):
            with self.subTest(value=value), self.assertRaises(ModelError):
                replace(ref(), revision=value)

    def test_uuid_is_not_coerced(self):
        for value in ('', 'title', ID.replace('-', ''), None, 1):
            with self.subTest(value=value), self.assertRaises(ModelError):
                replace(ref(), id=value)

    def test_hash_shape_without_computation(self):
        for value in ('', 'a' * 63, 'A' * 64, 'z' * 64, None):
            with self.subTest(value=value), self.assertRaises(ModelError):
                replace(ref(), content_hash=value)
        self.assertEqual(replace(ref(), content_hash='0' * 64).content_hash, '0' * 64)

    def test_raw_enum_string_not_coerced(self):
        with self.assertRaises(ModelError):
            replace(ref(), kind='production')
        with self.assertRaises(ModelError):
            replace(self.production(), content_mode='factual')
        with self.assertRaises(ModelError):
            replace(self.production(), script_locale='uk')

    def test_valid_production_separates_ui_locale(self):
        value = self.production()
        self.assertEqual(value.script_locale, Locale.UK)
        self.assertEqual(value.ui_locale, Locale.RU)

    def test_required_fields_and_types(self):
        for field, value in (('title', ''), ('title', 123), ('profile_ref', {}),
                             ('created_at', None), ('intended_use', [])):
            with self.subTest(field=field), self.assertRaises(ModelError):
                replace(self.production(), **{field: value})
        with self.assertRaises(TypeError):
            ProductionRevision(ref())

    def test_domain_header_kind(self):
        with self.assertRaises(ModelError):
            replace(self.production(), ref=ref(ObjectKind.CLAIM))

    def test_source_does_not_fetch_url(self):
        source = SourceRevision(ref(ObjectKind.SOURCE), 'Источник',
                                'https://example.invalid/source', ref(ObjectKind.RIGHTS_REVIEW))
        self.assertEqual(source.locator, 'https://example.invalid/source')

    def test_claim_and_evidence(self):
        evidence = EvidenceLink(ref(ObjectKind.SOURCE), EvidenceRelation.CONTEXT,
                                'p. 1', 'Needs review', 'reviewer', '2026-11-04T10:00:00Z')
        claim = ClaimRevision(ref(ObjectKind.CLAIM), 'Факт?', ClaimType.FACTUAL,
                              'material', (evidence,))
        self.assertEqual(claim.evidence_links, (evidence,))
        with self.assertRaises(ModelError):
            replace(evidence, relation='supports')
        with self.assertRaises(ModelError):
            replace(claim, claim_type='factual')

    def test_rights_review_is_data_not_grant(self):
        rights = RightsReview(ref(ObjectKind.RIGHTS_REVIEW), ID, 1, HASH,
                              'test', (), RightsStatus.UNKNOWN, 'owner',
                              '2026-11-04T10:00:00Z', 'Not reviewed')
        self.assertEqual(rights.status, RightsStatus.UNKNOWN)
        with self.assertRaises(ModelError):
            replace(rights, subject_revision=True)
        with self.assertRaises(ModelError):
            replace(rights, status='approved')

    def test_approval_does_not_run_gate(self):
        approval = ApprovalRecord(ID, 'SCRIPT', ref(ObjectKind.SCRIPT), HASH,
                                  '1', 'reviewer', '2026-11-04T10:00:00Z',
                                  ApprovalDecision.REVISE, 'Needs changes')
        self.assertEqual(approval.decision, ApprovalDecision.REVISE)
        with self.assertRaises(ModelError):
            replace(approval, decision='approve')

    def test_snapshot_generation_and_schema(self):
        for field in ('generation', 'editorial_schema_version'):
            for value in (0, -1, True, False, '1', 1.0):
                with self.subTest(field=field, value=value), self.assertRaises(ModelError):
                    replace(EditorialSnapshot(ID, 1), **{field: value})

    def test_snapshot_rejects_mutable_collections(self):
        snapshot = EditorialSnapshot(ID, 1, (self.production(),))
        for field in ('revisions', 'approvals', 'active_refs'):
            with self.subTest(field=field), self.assertRaises(ModelError):
                replace(snapshot, **{field: []})
        with self.assertRaises(ModelError):
            replace(snapshot, revisions=({},))

    def test_objects_and_nested_collections_frozen(self):
        production = self.production()
        snapshot = EditorialSnapshot(ID, 1, (production,), active_refs=(ref(),))
        for obj, name, value in ((production, 'title', 'changed'),
                                 (production.ref, 'revision', 2),
                                 (snapshot, 'generation', 2)):
            with self.subTest(object=type(obj).__name__), self.assertRaises(FrozenInstanceError):
                setattr(obj, name, value)
        with self.assertRaises(TypeError):
            snapshot.revisions[0] = production

    def test_fiction_can_have_empty_evidence(self):
        claim = ClaimRevision(ref(ObjectKind.CLAIM), 'Робот получил письмо.',
                              ClaimType.FICTIONAL, 'context')
        self.assertEqual(claim.evidence_links, ())

    def test_other_values_are_frozen_and_reject_mutable_inputs(self):
        source = SourceRevision(ref(ObjectKind.SOURCE), 'Источник', 'page 1',
                                ref(ObjectKind.RIGHTS_REVIEW))
        evidence = EvidenceLink(source.ref, EvidenceRelation.SUPPORTS, 'p1',
                                'Basis', 'reviewer', '2026-11-04T10:00:00Z')
        claim = ClaimRevision(ref(ObjectKind.CLAIM), 'Claim', ClaimType.FACTUAL,
                              'material', (evidence,))
        rights = RightsReview(ref(ObjectKind.RIGHTS_REVIEW), ID, 1, HASH,
                              'test', ('quote',), RightsStatus.RESTRICTED,
                              'reviewer', '2026-11-04T10:00:00Z', 'Basis')
        approval = ApprovalRecord(ID, 'SCRIPT', ref(ObjectKind.SCRIPT), HASH,
                                  '1', 'reviewer', '2026-11-04T10:00:00Z',
                                  ApprovalDecision.REJECT, 'Reason', ('reviewed',))
        for obj, name in ((source, 'title'), (evidence, 'explanation'),
                          (claim, 'statement'), (rights, 'basis'), (approval, 'reason')):
            with self.subTest(object=type(obj).__name__), self.assertRaises(FrozenInstanceError):
                setattr(obj, name, 'Changed')
        for obj, name in ((claim, 'evidence_links'), (rights, 'allowed_actions'),
                          (approval, 'review_declarations')):
            with self.subTest(field=name), self.assertRaises(ModelError):
                replace(obj, **{name: []})

    def test_common_header_and_required_nested_types(self):
        with self.assertRaises(ModelError):
            EditorialRevision({})
        with self.assertRaises(ModelError):
            EditorialSnapshot(ID, 1, active_refs=('script',))
        with self.assertRaises(ModelError):
            EvidenceLink(ref(ObjectKind.SOURCE), EvidenceRelation.SUPPORTS,
                         'page', None, 'reviewer', 'time')
        with self.assertRaises(TypeError):
            ModelError('not a violation')

    def test_unresolved_refs_are_not_graph_validated(self):
        snapshot = EditorialSnapshot(ID, 1, active_refs=(ref(ObjectKind.SCRIPT),))
        self.assertEqual(snapshot.revisions, ())
        self.assertEqual(EditorialRevision(ref()).ref, ref())

    def test_violation_and_error(self):
        violation = Violation('REQUIRED', 'title', 'Required', ref())
        self.assertEqual(ModelError(violation).violation, violation)
        with self.assertRaises(FrozenInstanceError):
            violation.code = 'OTHER'
        with self.assertRaises(ValueError):
            Violation('', 'title', 'Required')
        with self.assertRaises(ModelError) as caught:
            replace(ref(), revision=True)
        self.assertEqual(caught.exception.violation.field_path, 'revision')

    def test_import_has_no_external_dependencies_or_side_effects(self):
        # Fresh interpreter, bytecode writes disabled. Reads needed by import
        # are allowed; network, process execution and writes are forbidden.
        code = '''
import sys
def guard(event, args):
    if event.startswith(('socket.', 'subprocess.', 'os.system', 'os.mkdir', 'os.remove', 'os.rename')):
        raise AssertionError(event)
    if event == 'open':
        mode, flags = args[1], args[2]
        if (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (isinstance(flags, int) and flags & 3):
            raise AssertionError('write during import')
sys.addaudithook(guard)
import editorial
import editorial.model
for name in sys.modules:
    assert name.split('.')[0] not in {'core','scripts','torch','numpy','requests','ffmpeg','silero','json','hashlib'}
'''
        result = subprocess.run([sys.executable, '-B', '-c', code], cwd=Path(__file__).resolve().parents[1],
                                text=True, capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
