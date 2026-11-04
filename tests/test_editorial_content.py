"""Local script/scene/asset/aggregate invariants; no media or codec."""
from dataclasses import FrozenInstanceError, replace
import unittest

from editorial import (
    ActiveSelections, AssetRevision, BriefValue, CandidateRevision, ClaimRevision,
    ClaimReview, ClaimType, ContentMode, ContractSnapshot, EditorialRevision,
    EditorialSnapshot, Event, GenreProfile, Locale, ModelError, ObjectKind,
    ProductionRevision, RevisionRef, RightsDetails, RightsReview, RightsStatus,
    Scene, ScenePlanRevision, ScriptRevision, ScriptSegment, SourceDetails, SourceRevision,
)

ID = '10000000-0000-0000-0000-000000000001'
ID2 = '10000000-0000-0000-0000-000000000002'
HASH = 'a' * 64
AT = '2026-11-04T10:00:00Z'


def ref(kind, id=ID):
    return RevisionRef(kind, id, 1, HASH)


def brief():
    return BriefValue(1, 'Аудитория', 'Ракурс', 'Обещание', (), (), ref(ObjectKind.GENRE_PROFILE))


def segment(text='  Україна е\u0301 😀 ', id=ID, claims=()):
    return ScriptSegment(id, text, 'body', claims, None, None, None)


def script():
    return ScriptRevision(ref(ObjectKind.SCRIPT), ref(ObjectKind.PRODUCTION),
                          ref(ObjectKind.CANDIDATE), brief(), Locale.UK, (segment(),), ())


def scene(start=0, end=3, id=ID):
    return Scene(id, start, end, '😀 е\u0301', 'still', 'Градиент', None, None)


def plan():
    return ScenePlanRevision(ref(ObjectKind.SCENE_PLAN), ref(ObjectKind.SCRIPT), (scene(),))


def asset():
    return AssetRevision(ref(ObjectKind.ASSET), 'media/кадр.png', HASH, 'image',
                         ref(ObjectKind.RIGHTS_REVIEW), None, None, None)


def event():
    return Event(ID, 'Owner', AT, 'revision_added', (ref(ObjectKind.SCRIPT),), 'Saved', None)


def complete():
    production = ProductionRevision(ref(ObjectKind.PRODUCTION), 'Тема', ref(ObjectKind.GENRE_PROFILE),
                                    ContentMode.FACTUAL, Locale.UK, Locale.UK, Locale.UK,
                                    Locale.RU, 'test', '9:16', AT)
    profile = GenreProfile(ref(ObjectKind.GENRE_PROFILE), 'science', '1', 'Наука', 'Наука',
                           (ContentMode.FACTUAL,), ('Вопрос',), '1', None)
    candidate = CandidateRevision(ref(ObjectKind.CANDIDATE), 'Тема', 'Описание', (),
                                   'manual_topic', 'Тема', None, None)
    source = SourceRevision(ref(ObjectKind.SOURCE), 'Источник', 'page1', ref(ObjectKind.RIGHTS_REVIEW))
    claim = ClaimRevision(ref(ObjectKind.CLAIM), 'Утверждение', ClaimType.FACTUAL, 'material')
    rights = RightsReview(ref(ObjectKind.RIGHTS_REVIEW), ID, 1, HASH, 'test', (),
                          RightsStatus.UNKNOWN, 'Owner', AT, 'Not reviewed')
    revisions = (production, profile, candidate, source, claim, script(), plan(), asset(), rights)
    base = EditorialSnapshot(ID, 1, revisions, active_refs=(production.ref, script().ref))
    return ContractSnapshot(base,
                            (SourceDetails(source.ref, 'local', None, None, None, None, None, None, None),),
                            (ClaimReview(claim.ref, 'unreviewed', None, None, None, None),),
                            (RightsDetails(rights.ref, ObjectKind.SOURCE, None),), (event(),), HASH)


class EditorialContentTests(unittest.TestCase):
    def rejects(self, obj, field, values):
        for value in values:
            with self.subTest(field=field, value=value), self.assertRaises(ModelError):
                replace(obj, **{field: value})

    def test_brief_local_types(self):
        b = brief()
        self.rejects(b, 'revision', (0, -1, True, 1.0, '1'))
        self.rejects(b, 'audience', (' ', None, 1))
        self.rejects(b, 'profile_ref', (ref(ObjectKind.SOURCE), None))
        self.rejects(b, 'must_include_claim_refs', ([], (ref(ObjectKind.SOURCE),)))
        self.rejects(b, 'must_avoid', ([], ('',)))

    def test_text_preserved_exactly(self):
        s = segment()
        self.assertEqual(s.text, '  Україна е\u0301 😀 ')
        self.assertNotEqual(s.text, s.text.strip())
        self.assertIsNone(s.visual_notes)
        self.assertEqual(script().segments[0].text, s.text)

    def test_segment_invalid_values(self):
        s = segment()
        self.rejects(s, 'id', ('bad', None))
        self.rejects(s, 'text', ('', '\ud800', True, 'a' * 100001))
        self.rejects(s, 'role', ('intro', None))
        self.rejects(s, 'claim_refs', ([], (ref(ObjectKind.ASSET),)))
        self.rejects(s, 'visual_notes', (' ', False))

    def test_script_refs_and_locale(self):
        s = script()
        for field, bad in (('ref', ObjectKind.SOURCE), ('production_ref', ObjectKind.CANDIDATE),
                           ('candidate_ref', ObjectKind.PRODUCTION)):
            self.rejects(s, field, (ref(bad), None))
        self.rejects(s, 'locale', ('uk', 'ua', None))
        self.rejects(s, 'brief', ({}, None))

    def test_script_count_and_duplicate_ids(self):
        s = script()
        self.rejects(s, 'segments', ((), [], (s.segments[0], s.segments[0])))
        many = tuple(segment(id=f'10000000-0000-0000-0000-{i:012x}') for i in range(1000))
        self.assertEqual(len(replace(s, segments=many).segments), 1000)
        self.rejects(s, 'segments', (many + (segment(id=ID2),),))

    def test_script_claim_union_is_local_not_graph(self):
        a, b = ref(ObjectKind.CLAIM), ref(ObjectKind.CLAIM, ID2)
        s = replace(script(), segments=(segment(claims=(b, a, a)),), claim_refs=(a, b))
        self.assertEqual(s.claim_refs, (a, b))
        self.rejects(s, 'claim_refs', ((), (b, a), (a, a, b)))

    def test_scene_offsets_and_estimates(self):
        s = scene()
        self.assertIsNone(s.estimate_ms)
        self.rejects(s, 'start', (-1, True, 0.0, '0'))
        self.rejects(s, 'end', (0, -1, True, 3.0))
        self.rejects(s, 'estimate_ms', (0, -1, False, 1.0))
        self.assertEqual(replace(s, estimate_ms=100).estimate_ms, 100)

    def test_scene_is_still_only_and_nullable(self):
        s = scene()
        self.rejects(s, 'visual_kind', ('video', 'ai_video', None))
        self.rejects(s, 'asset_ref', (ref(ObjectKind.SCRIPT), 'asset'))
        self.assertIsNone(s.asset_ref)
        self.assertEqual(replace(s, asset_ref=ref(ObjectKind.ASSET)).asset_ref.kind, ObjectKind.ASSET)

    def test_plan_continuity_and_order(self):
        p = replace(plan(), scenes=(scene(), scene(3, 6, ID2)))
        self.assertEqual(p.scenes[-1].end, 6)
        self.rejects(p, 'scenes', ((scene(1, 3),), (scene(), scene(4, 6, ID2)),
                                  (scene(), scene(2, 6, ID2)), tuple(reversed(p.scenes)),
                                  (scene(), scene(3, 6)), (), []))

    def test_plan_does_not_resolve_or_compare_script(self):
        p = replace(plan(), scenes=(replace(scene(), end=999, narration_text='Другой текст'),))
        self.assertEqual(p.scenes[0].end, 999)
        self.rejects(p, 'script_ref', (ref(ObjectKind.ASSET),))
        many = tuple(scene(i, i + 1, f'10000000-0000-0000-0000-{i:012x}') for i in range(1000))
        self.assertEqual(len(replace(p, scenes=many).scenes), 1000)
        self.rejects(p, 'scenes', (many + (scene(1000, 1001, ID2),),))

    def test_asset_valid_unicode_path_and_no_disk_lookup(self):
        a = asset()
        self.assertEqual(a.file_ref, 'media/кадр.png')
        self.assertEqual(replace(a, kind='video').kind, 'video')
        self.assertEqual(replace(a, file_ref='not-existing/😀.png').file_ref, 'not-existing/😀.png')

    def test_asset_unsafe_paths(self):
        self.rejects(asset(), 'file_ref', ('/abs.png', '../x', 'a/../x', './x', 'a//x',
                                          'C:/x', '\\server\\x', 'a\\b', 'CON.png',
                                          'media/LPT1.txt', 'aux', 'COM¹.txt', 'x.',
                                          'a /b', 'x\x00.png', 'a?b', 'x' * 101,
                                          '/'.join(['x' * 90] * 3)))

    def test_asset_binding_and_hash(self):
        a = asset()
        self.rejects(a, 'sha256', ('a', 'A' * 64, True))
        self.rejects(a, 'rights_ref', (ref(ObjectKind.SOURCE),))
        self.rejects(a, 'kind', ('still', None))
        self.rejects(a, 'scene_id', ('title', True))
        self.rejects(a, 'script_ref', (ref(ObjectKind.SCRIPT),))
        self.rejects(a, 'text_digest', (HASH,))
        bound = replace(a, script_ref=ref(ObjectKind.SCRIPT), text_digest=HASH, scene_id=ID)
        self.assertEqual(bound.text_digest, HASH)
        self.rejects(bound, 'script_ref', (None, ref(ObjectKind.CLAIM)))
        self.rejects(bound, 'text_digest', ('bad', None))

    def test_event_is_data_with_valid_action_and_time(self):
        e = event()
        self.assertEqual(e.action, 'revision_added')
        self.assertIsNone(e.error_code)
        self.rejects(e, 'action', ('execute', None))
        self.rejects(e, 'at', ('2026-02-30T00:00:00Z', 'today'))
        self.rejects(e, 'refs', ([], ('ref',)))
        self.rejects(e, 'error_code', ('', True))

    def test_active_selections_typed_nullable_slots(self):
        a = ActiveSelections(None, None, ref(ObjectKind.SCRIPT), None)
        self.assertIsNone(a.production)
        for field, wrong in (('production', ObjectKind.SCRIPT), ('candidate', ObjectKind.ASSET),
                             ('script', ObjectKind.CLAIM), ('scene_plan', ObjectKind.PRODUCTION)):
            self.rejects(a, field, (ref(wrong), 'ref'))

    def test_full_snapshot_retains_all_payloads_and_companions(self):
        c = complete()
        self.assertEqual(len(c.base.revisions), 9)
        self.assertEqual(c.active_selections, ActiveSelections(ref(ObjectKind.PRODUCTION), None,
                                                              ref(ObjectKind.SCRIPT), None))
        self.assertEqual(c.rights_reviews, (c.base.revisions[-1],))
        self.assertIsNone(c.rights_details[0].expires_at)
        self.assertEqual(c.rights_details[0].subject_kind, ObjectKind.SOURCE)
        self.assertEqual(c.snapshot_checksum, HASH)

    def test_snapshot_checksum_shape_only(self):
        c = complete()
        self.assertEqual(replace(c, snapshot_checksum='0' * 64).snapshot_checksum, '0' * 64)
        self.rejects(c, 'snapshot_checksum', ('', 'A' * 64, None, False))

    def test_snapshot_tuple_shape(self):
        c = complete()
        for field in ('source_details', 'claim_reviews', 'rights_details', 'events'):
            self.rejects(c, field, ([], (None,)))
        self.rejects(c, 'base', ({}, None))

    def test_snapshot_rejects_duplicate_local_records(self):
        c = complete()
        for field in ('source_details', 'claim_reviews', 'rights_details', 'events'):
            value = getattr(c, field)[0]
            self.rejects(c, field, ((value, value),))
        self.rejects(c, 'base', (replace(c.base, revisions=c.base.revisions + (c.base.revisions[-1],)),))

    def test_snapshot_rejects_headers_and_wrong_order(self):
        c = complete()
        self.rejects(c, 'base', (replace(c.base, revisions=(EditorialRevision(ref(ObjectKind.SCRIPT)),)),
                                replace(c.base, revisions=tuple(reversed(c.base.revisions)))))

    def test_companion_identity_and_event_order(self):
        c = complete()
        d = c.source_details[0]
        changed_hash = replace(d, owner_ref=replace(d.owner_ref, content_hash='b' * 64))
        self.rejects(c, 'source_details', ((d, changed_hash),))
        later_in_array = replace(event(), id=ID2, at='2000-01-01T00:00:00Z')
        value = replace(c, events=(event(), later_in_array))
        self.assertEqual(value.events, (event(), later_in_array))

    def test_snapshot_active_order_and_duplicates(self):
        c = complete()
        for values in ((ref(ObjectKind.SCRIPT), ref(ObjectKind.PRODUCTION)),
                       (ref(ObjectKind.SCRIPT), ref(ObjectKind.SCRIPT)), (ref(ObjectKind.ASSET),)):
            self.rejects(c, 'base', (replace(c.base, active_refs=values),))

    def test_snapshot_does_not_implement_graph_or_clock_checks(self):
        c = complete()
        # Missing targets/companions and expired rights are later integrity gates.
        empty = ContractSnapshot(EditorialSnapshot(ID, 1, active_refs=(ref(ObjectKind.SCRIPT),)),
                                 (), (), (), (), HASH)
        self.assertEqual(empty.active_selections.script, ref(ObjectKind.SCRIPT))
        expiry = replace(c.rights_details[0], expires_at='2000-01-01T00:00:00Z')
        self.assertEqual(replace(c, rights_details=(expiry,)).rights_details[0], expiry)

    def test_new_types_frozen_including_nested_tuples(self):
        values = ((brief(), 'audience'), (segment(), 'text'), (script(), 'locale'),
                  (scene(), 'start'), (plan(), 'scenes'), (asset(), 'file_ref'),
                  (event(), 'action'), (ActiveSelections(None, None, None, None), 'script'),
                  (complete(), 'snapshot_checksum'))
        for obj, field in values:
            with self.subTest(type=type(obj).__name__), self.assertRaises(FrozenInstanceError):
                setattr(obj, field, None)
        with self.assertRaises(TypeError):
            complete().base.revisions[0] = script()


if __name__ == '__main__':
    unittest.main()
