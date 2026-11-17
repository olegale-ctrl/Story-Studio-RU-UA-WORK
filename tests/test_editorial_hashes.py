"""E01.3.1 canonical semantic payload and revision hash tests."""
import copy
from dataclasses import replace
import json
from pathlib import Path
import subprocess
import sys
import unittest

from editorial import model as m
from editorial.codec import decode_snapshot
from editorial.integrity import (
    HashVerificationError,
    canonical_revision_bytes,
    compute_revision_content_hash,
    verify_revision_content_hash,
)
from test_editorial_codec import AT, HASH, ID, TEXT, raw, wire


AT2 = '2026-11-05T11:22:33Z'
ID2 = '20000000-0000-0000-0000-000000000002'


class RevisionHashTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = decode_snapshot(raw(wire()))
        self.by_kind = {revision.ref.kind: revision for revision in self.snapshot.base.revisions}

    def companion(self, revision):
        return {
            m.ObjectKind.SOURCE: self.snapshot.source_details[0],
            m.ObjectKind.CLAIM: self.snapshot.claim_reviews[0],
            m.ObjectKind.RIGHTS_REVIEW: self.snapshot.rights_details[0],
        }.get(revision.ref.kind)

    def canonical(self, revision, companion=None):
        return canonical_revision_bytes(revision, companion)

    def digest(self, revision, companion=None):
        return compute_revision_content_hash(revision, companion)

    def test_all_nine_revision_types_have_canonical_payloads(self):
        expected = tuple(kind for kind, _ in m._REVISION_TYPES)
        self.assertEqual(tuple(r.ref.kind for r in self.snapshot.base.revisions), expected)
        for revision in self.snapshot.base.revisions:
            with self.subTest(kind=revision.ref.kind.value):
                encoded = self.canonical(revision, self.companion(revision))
                payload = json.loads(encoded)
                self.assertEqual(payload['editorial_schema_version'], 1)
                self.assertEqual(payload['kind'], revision.ref.kind.value)
                self.assertEqual(payload['id'], revision.ref.id)
                self.assertEqual(payload['revision'], revision.ref.revision)
                self.assertNotIn('ref', payload)
                self.assertNotIn('content_hash', payload)
                self.assertRegex(self.digest(revision, self.companion(revision)), r'^[0-9a-f]{64}$')

    def test_repeated_calculation_is_identical_and_canonical(self):
        revision = self.by_kind[m.ObjectKind.SCRIPT]
        first = self.canonical(revision)
        self.assertEqual(first, self.canonical(revision))
        self.assertEqual(self.digest(revision), self.digest(revision))
        payload = json.loads(first)
        reversed_payload = {key: payload[key] for key in reversed(tuple(payload))}
        reordered = json.dumps(reversed_payload, ensure_ascii=False, sort_keys=True,
                               separators=(',', ':'), allow_nan=False).encode('utf-8')
        self.assertEqual(first, reordered)

    def test_schema1_golden_hash_vectors(self):
        expected = {
            'production': '14da48a7be1878a11f09ed12d95b993dbb6048de5e5d613e3af2187d1154b675',
            'genre_profile': 'fc621df51e0d7d16d8d0e938635fc0eb5bcf80d0d1b4f480711ee50651f7cc31',
            'candidate': '32367070ab4a309c362cff1e16f8c1b6e2f7090d05f62120abb5e31c9268a106',
            'source': '852823e5b249152984ce38868a1cde14ec2f5e8e9b6b22d2f941ca773c0ee6fd',
            'claim': '8ab7f85694bbb1633c62ed71627f3c021fda306b2ed4b3510c4b0ced3834c54f',
            'script': 'f46dcb9e5ab40ef1e114200ae075e0f2f1df4a6fcaddc74021d5f1579813aa08',
            'scene_plan': '15429f0697d1b31f350b07ebf8fed812fe898cfaaa161352640ce683df097fd6',
            'asset': '4c39964a170275165439e6adf7277e67c7943ed8437442876fe340ef06ac8753',
            'rights_review': '6f046e4b9905fb312658955adc7217163b062120d778492521979400ee1ef393',
        }
        actual = {revision.ref.kind.value: self.digest(revision, self.companion(revision))
                  for revision in self.snapshot.base.revisions}
        self.assertEqual(actual, expected)

    def test_semantic_changes_change_hash(self):
        candidate = self.by_kind[m.ObjectKind.CANDIDATE]
        changed = replace(candidate, summary='Другое описание')
        self.assertNotEqual(self.digest(candidate), self.digest(changed))
        # Nested refs are semantic and retain their supplied content hashes.
        changed_ref = replace(candidate.source_refs[0], content_hash='b' * 64)
        changed = replace(candidate, source_refs=(changed_ref,))
        self.assertNotEqual(self.digest(candidate), self.digest(changed))

    def test_closed_audit_timestamp_exclusions_do_not_change_hash(self):
        production = self.by_kind[m.ObjectKind.PRODUCTION]
        self.assertEqual(self.digest(production), self.digest(replace(production, created_at=AT2)))

        source = self.by_kind[m.ObjectKind.SOURCE]
        details = self.snapshot.source_details[0]
        self.assertEqual(self.digest(source, details),
                         self.digest(source, replace(details, accessed_at=AT2)))

        claim = self.by_kind[m.ObjectKind.CLAIM]
        review = self.snapshot.claim_reviews[0]
        self.assertEqual(self.digest(claim, review),
                         self.digest(claim, replace(review, reviewed_at=AT2)))
        evidence = replace(claim.evidence_links[0], reviewed_at=AT2)
        self.assertEqual(self.digest(claim, review),
                         self.digest(replace(claim, evidence_links=(evidence,)), review))

        rights = self.by_kind[m.ObjectKind.RIGHTS_REVIEW]
        self.assertEqual(self.digest(rights, self.snapshot.rights_details[0]),
                         self.digest(replace(rights, reviewed_at=AT2), self.snapshot.rights_details[0]))

    def test_only_approved_timestamp_fields_are_excluded(self):
        source = self.by_kind[m.ObjectKind.SOURCE]
        details = self.snapshot.source_details[0]
        self.assertNotEqual(self.digest(source, details),
                            self.digest(source, replace(details, published_at=AT2)))
        null_payload = json.loads(self.canonical(source, details))
        self.assertIn('published_at', null_payload)
        self.assertIsNone(null_payload['published_at'])
        self.assertNotIn('accessed_at', null_payload)

        rights = self.by_kind[m.ObjectKind.RIGHTS_REVIEW]
        rights_details = self.snapshot.rights_details[0]
        self.assertNotEqual(self.digest(rights, rights_details),
                            self.digest(rights, replace(rights_details, expires_at=AT2)))
        self.assertIsNone(json.loads(self.canonical(rights, rights_details))['expires_at'])

    def test_own_content_hash_is_not_hashed(self):
        profile = self.by_kind[m.ObjectKind.GENRE_PROFILE]
        changed = replace(profile, ref=replace(profile.ref, content_hash='b' * 64))
        self.assertEqual(self.canonical(profile), self.canonical(changed))
        self.assertEqual(self.digest(profile), self.digest(changed))

    def test_asset_identity_and_media_kind_are_distinct_and_semantic(self):
        asset = self.by_kind[m.ObjectKind.ASSET]
        payload = json.loads(self.canonical(asset))
        self.assertEqual(payload['kind'], 'asset')
        self.assertEqual(payload['asset_kind'], 'image')
        self.assertNotIn('content_hash', payload)
        changed = replace(asset, kind='video')
        self.assertNotEqual(self.digest(asset), self.digest(changed))
        self.assertEqual(self.digest(asset), self.digest(copy.deepcopy(asset)))

    def test_subject_kind_id_and_revision_are_semantic(self):
        rights = self.by_kind[m.ObjectKind.RIGHTS_REVIEW]
        details = self.snapshot.rights_details[0]
        asset_details = replace(details, subject_kind=m.ObjectKind.ASSET)
        self.assertNotEqual(self.digest(rights, details), self.digest(rights, asset_details))
        self.assertNotEqual(self.digest(rights, details),
                            self.digest(replace(rights, subject_id=ID2), details))
        self.assertNotEqual(self.digest(rights, details),
                            self.digest(replace(rights, subject_revision=2), details))

    def test_revision_identity_changes_hash(self):
        profile = self.by_kind[m.ObjectKind.GENRE_PROFILE]
        changed_id = replace(profile, ref=replace(profile.ref, id=ID2))
        changed_revision = replace(profile, ref=replace(profile.ref, revision=2))
        self.assertNotEqual(self.digest(profile), self.digest(changed_id))
        self.assertNotEqual(self.digest(profile), self.digest(changed_revision))

    def test_unicode_is_utf8_and_never_normalized(self):
        script = self.by_kind[m.ObjectKind.SCRIPT]
        encoded = self.canonical(script)
        self.assertIn(TEXT.encode('utf-8'), encoded)
        changed_text = TEXT.replace('е\u0301', 'é')
        segment = replace(script.segments[0], text=changed_text)
        changed = replace(script, segments=(segment,))
        self.assertNotEqual(self.digest(script), self.digest(changed))
        self.assertIn(changed_text.encode('utf-8'), self.canonical(changed))

    def test_verify_accepts_exact_and_diagnoses_mismatch(self):
        profile = self.by_kind[m.ObjectKind.GENRE_PROFILE]
        correct = self.digest(profile)
        verified = replace(profile, ref=replace(profile.ref, content_hash=correct))
        self.assertIsNone(verify_revision_content_hash(verified))
        with self.assertRaises(HashVerificationError) as caught:
            verify_revision_content_hash(profile)
        violation = caught.exception.violation
        self.assertEqual(violation.code, 'CONTENT_HASH_MISMATCH')
        self.assertEqual(violation.field_path, '$.ref.content_hash')
        self.assertEqual(violation.object_ref, profile.ref)
        self.assertIn(correct, violation.message)

    def test_companion_is_mandatory_typed_and_exact_owner(self):
        source = self.by_kind[m.ObjectKind.SOURCE]
        for companion in (None, self.snapshot.claim_reviews[0]):
            with self.subTest(companion=type(companion).__name__), self.assertRaises(HashVerificationError) as caught:
                self.canonical(source, companion)
            self.assertEqual(caught.exception.violation.code, 'MISSING_COMPANION')
        wrong = replace(self.snapshot.source_details[0],
                        owner_ref=replace(source.ref, id=ID2))
        with self.assertRaises(HashVerificationError) as caught:
            self.canonical(source, wrong)
        self.assertEqual(caught.exception.violation.code, 'COMPANION_OWNER')
        profile = self.by_kind[m.ObjectKind.GENRE_PROFILE]
        with self.assertRaises(HashVerificationError) as caught:
            self.canonical(profile, self.snapshot.source_details[0])
        self.assertEqual(caught.exception.violation.code, 'UNEXPECTED_COMPANION')

    def test_rights_binding_contains_no_subject_content_hash(self):
        rights = self.by_kind[m.ObjectKind.RIGHTS_REVIEW]
        payload = json.loads(self.canonical(rights, self.snapshot.rights_details[0]))
        self.assertEqual(payload['subject_kind'], 'source')
        self.assertEqual(payload['subject_id'], ID)
        self.assertEqual(payload['subject_revision'], 1)
        self.assertEqual(payload['material_digest'], HASH)
        self.assertNotIn('subject_ref', payload)

    def test_hashing_asset_does_not_read_media_or_use_external_services(self):
        payload = raw(wire())
        code = '''
import sys
active = False
def guard(event, args):
    if active and (event == 'open' or event.startswith(('socket.', 'subprocess.', 'os.system'))):
        raise AssertionError(event)
sys.addaudithook(guard)
from editorial.codec import decode_snapshot
from editorial.integrity import compute_revision_content_hash
snapshot = decode_snapshot(PAYLOAD)
asset = next(r for r in snapshot.base.revisions if r.ref.kind.value == 'asset')
active = True
assert len(compute_revision_content_hash(asset)) == 64
'''.replace('PAYLOAD', repr(payload))
        result = subprocess.run([sys.executable, '-B', '-c', code],
            cwd=Path(__file__).resolve().parents[1], capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
