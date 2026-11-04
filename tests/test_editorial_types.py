"""E01.1b-1: local value invariants, without codec or reference resolution."""
from dataclasses import FrozenInstanceError, replace
import unittest

from editorial import (
    CandidateRevision, ClaimReview, ContentMode, CriterionRating, GenreProfile,
    ModelError, ObjectKind, RevisionRef, RightsDetails, RightsReview,
    RightsStatus, RubricCriterion, SourceDetails,
)

ID = '10000000-0000-0000-0000-000000000001'
HASH = 'a' * 64
AT = '2026-11-04T10:00:00Z'


def ref(kind):
    return RevisionRef(kind, ID, 1, HASH)


def profile():
    return GenreProfile(ref(ObjectKind.GENRE_PROFILE), 'science_technology', '0.1',
                        'Наука', 'Наука', (ContentMode.FACTUAL,),
                        ('Вопрос', 'Пояснення'), '1', None)


def candidate():
    return CandidateRevision(ref(ObjectKind.CANDIDATE), 'Тема', 'Описание', (),
                             'manual_topic', 'Ручная тема', None, None)


def source_details():
    return SourceDetails(ref(ObjectKind.SOURCE), 'url', None, None, None,
                         None, None, None, None)


class EditorialTypesTests(unittest.TestCase):
    def rejects(self, obj, field, values):
        for value in values:
            with self.subTest(field=field, value=value), self.assertRaises(ModelError):
                replace(obj, **{field: value})

    def test_profile_keeps_identity_key_and_version_distinct(self):
        p = profile()
        self.assertEqual(p.ref.id, ID)
        self.assertEqual(p.ref.revision, 1)
        self.assertEqual(p.profile_key, 'science_technology')
        self.assertEqual(p.version, '0.1')
        self.assertIsNone(p.rubric)

    def test_rubric_bounds(self):
        r = RubricCriterion('clarity', 'Понятность', 0, 5, 100)
        self.rejects(r, 'rating_min', (True, 1, -1, 0.0))
        self.rejects(r, 'rating_max', (False, 4, 6, '5'))
        self.rejects(r, 'weight_percent', (True, -1, 101, 1.5))

    def test_rubric_weights_and_unique_keys(self):
        a = RubricCriterion('clarity', 'Clarity', 0, 5, 50)
        b = RubricCriterion('evidence', 'Evidence', 0, 5, 50)
        p = replace(profile(), rubric=(a, b))
        self.assertEqual(sum(x.weight_percent for x in p.rubric), 100)
        self.rejects(p, 'rubric', ((), [], (a,), (a, a)))

    def test_profile_modes_and_structure(self):
        p = profile()
        self.rejects(p, 'allowed_modes', ((), [], ('factual',),
                                        (ContentMode.FACTUAL, ContentMode.FACTUAL)))
        self.rejects(p, 'narrative_structure', ((), [], ('',), (None,)))
        for mode in ContentMode:
            self.assertEqual(replace(p, allowed_modes=(mode,)).allowed_modes, (mode,))

    def test_keys_and_unicode_text(self):
        p = profile()
        self.rejects(p, 'profile_key', ('', 'Science', 'наука', 'a-b', 'a' * 65, None))
        self.rejects(p, 'display_name_uk', (' ', 1, '\ud800', 'a' * 100001))
        text = '  Україна: е\u0301 😀  '
        self.assertEqual(replace(p, display_name_uk=text).display_name_uk, text)

    def test_revision_kind_and_number(self):
        p = profile()
        self.rejects(p, 'ref', (ref(ObjectKind.SOURCE), None, {}))
        with self.assertRaises(ModelError):
            replace(p.ref, revision=True)

    def test_candidate_can_be_manual_and_have_unknown_assessment(self):
        c = candidate()
        self.assertEqual(c.source_refs, ())
        self.assertIsNone(c.assessment)
        self.assertEqual(replace(c, assessment=()).assessment, ())
        self.assertIsNone(c.rationale)

    def test_candidate_source_ref_shape_not_existence(self):
        c = replace(candidate(), source_refs=(ref(ObjectKind.SOURCE),))
        self.assertEqual(c.source_refs[0].id, ID)
        self.rejects(c, 'source_refs', ([], ('source',), (ref(ObjectKind.SCRIPT),)))

    def test_candidate_intake_no_fetch(self):
        c = replace(candidate(), discovery_method='manual_url',
                    discovery_input='https://example.invalid/never-fetched')
        self.assertTrue(c.discovery_input.startswith('https://'))
        self.rejects(c, 'discovery_method', ('scrape', '', None))
        self.rejects(c, 'title', (' ', 1))

    def test_candidate_ratings(self):
        a = CriterionRating('clarity', 5, 'Clear')
        c = replace(candidate(), assessment=(a,), rationale='Review')
        self.rejects(a, 'rating', (-1, 6, True, 1.0, '1'))
        self.rejects(a, 'reason', ('', None))
        self.rejects(c, 'assessment', ([], (a, a), ('rating',)))
        self.rejects(c, 'rationale', (' ', False))

    def test_source_optional_values_are_preserved(self):
        d = source_details()
        self.assertIsNone(d.published_at)
        self.assertIsNone(d.material_digest)
        d = replace(d, source_type='local', author='Автор', published_at=AT,
                    accessed_at=AT, material_digest=HASH)
        self.assertEqual(d.published_at, AT)
        self.rejects(d, 'owner_ref', (ref(ObjectKind.CLAIM), None))
        self.rejects(d, 'source_type', ('other', False))
        self.rejects(d, 'author', ('', 0))
        self.rejects(d, 'material_digest', ('0', 'A' * 64, 1))

    def test_dates_are_exact_valid_utc(self):
        d = source_details()
        self.rejects(d, 'published_at', ('2026-02-30T00:00:00Z', '2026-11-04',
                                       '2026-11-04T10:00:00+00:00',
                                       '2026-11-04T10:00:00.000Z',
                                       '2026-11-04T24:00:00Z', '', True))
        self.assertEqual(replace(d, published_at='2024-02-29T23:59:59Z').published_at,
                         '2024-02-29T23:59:59Z')

    def test_unreviewed_has_no_invented_reviewer(self):
        c = ClaimReview(ref(ObjectKind.CLAIM), 'unreviewed', None, None, None, None)
        self.assertIsNone(c.reviewed_at)
        self.rejects(c, 'reviewer', ('invented', 1))
        self.rejects(c, 'review_status', ('approved', None))

    def test_reviewed_claim_fields_required(self):
        for status in ('supported', 'disputed', 'unverified', 'removed'):
            c = ClaimReview(ref(ObjectKind.CLAIM), status, None, 'Reviewer', AT, 'Basis')
            for field in ('reviewer', 'reviewed_at', 'reason'):
                self.rejects(c, field, (None, ''))
            self.rejects(c, 'qualification', ('Not applicable',))

    def test_qualified_requires_exact_qualification(self):
        c = ClaimReview(ref(ObjectKind.CLAIM), 'qualified', 'Возможно', 'Reviewer', AT, 'Basis')
        self.assertEqual(c.qualification, 'Возможно')
        self.rejects(c, 'qualification', (None, ''))
        self.rejects(c, 'owner_ref', (ref(ObjectKind.SOURCE),))

    def test_rights_kind_is_explicit_and_limited(self):
        for kind in (ObjectKind.SOURCE, ObjectKind.ASSET):
            self.assertEqual(RightsDetails(ref(ObjectKind.RIGHTS_REVIEW), kind, None).subject_kind, kind)
        d = RightsDetails(ref(ObjectKind.RIGHTS_REVIEW), ObjectKind.SOURCE, None)
        self.rejects(d, 'subject_kind', ('source', None, True, ObjectKind.CLAIM))
        self.rejects(d, 'owner_ref', (ref(ObjectKind.SOURCE),))
        self.rejects(d, 'expires_at', ('yesterday',))
        self.assertEqual(replace(d, expires_at=AT).expires_at, AT)

    def test_existing_rights_constructor_unchanged_no_kind_inference(self):
        r = RightsReview(ref(ObjectKind.RIGHTS_REVIEW), ID, 1, HASH,
                         'test', (), RightsStatus.UNKNOWN, 'Owner', AT, 'Unreviewed')
        self.assertFalse(hasattr(r, 'subject_kind'))
        source = RightsDetails(r.ref, ObjectKind.SOURCE, None)
        asset = RightsDetails(r.ref, ObjectKind.ASSET, None)
        self.assertNotEqual(source, asset)
        self.assertEqual(r.subject_id, ID)
        # A future graph layer handles pairing; these constructors do not resolve it.
        self.assertEqual(ref(ObjectKind.SOURCE).id, ref(ObjectKind.ASSET).id)

    def test_new_values_are_frozen(self):
        objects = ((profile(), 'version'), (candidate(), 'title'),
                   (CriterionRating('clarity', 1, 'Basis'), 'rating'),
                   (RubricCriterion('clarity', 'Basis', 0, 5, 100), 'weight_percent'),
                   (source_details(), 'author'),
                   (ClaimReview(ref(ObjectKind.CLAIM), 'unreviewed', None, None, None, None), 'reason'),
                   (RightsDetails(ref(ObjectKind.RIGHTS_REVIEW), ObjectKind.SOURCE, None), 'subject_kind'))
        for obj, field in objects:
            with self.subTest(type=type(obj).__name__), self.assertRaises(FrozenInstanceError):
                setattr(obj, field, None)
        with self.assertRaises(TypeError):
            profile().allowed_modes[0] = ContentMode.HYBRID


if __name__ == '__main__':
    unittest.main()
