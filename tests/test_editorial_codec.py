"""Synthetic wire data for decoder tests, not a production encoder."""
import copy
from dataclasses import FrozenInstanceError
import json
from pathlib import Path
import subprocess
import sys
import unittest

from editorial import model as m
from editorial.codec import DecodeError, decode_snapshot

ID = '10000000-0000-0000-0000-000000000001'
HASH = 'a' * 64
AT = '2026-11-04T10:00:00Z'
TEXT = '  Україна е\u0301 😀 '
COLLECTIONS = ('production_revisions', 'profiles', 'candidates', 'sources', 'claims',
               'scripts', 'scene_plans', 'assets', 'rights_reviews')


def ref(kind, revision=1):
    return dict(kind=kind, id=ID, revision=revision, content_hash=HASH)


def wire():
    return {
        'editorial_schema_version': 1, 'production_id': ID, 'generation': 1,
        'production_revisions': [dict(ref=ref('production'), title='Тема', profile_ref=ref('genre_profile'),
            content_mode='hybrid', script_locale='uk', narration_locale='uk', subtitle_locale='uk',
            ui_locale='ru', intended_use='test', output_preset='9:16', created_at=AT)],
        'profiles': [dict(ref=ref('genre_profile'), profile_key='science', version='1.0',
            display_name_ru='Наука', display_name_uk='Наука', allowed_modes=['factual', 'hybrid'],
            narrative_structure=['Вопрос', 'Пояснення'], review_policy_version='1',
            rubric=[dict(key='clarity', description='Понятность', rating_min=0, rating_max=5, weight_percent=100)])],
        'candidates': [dict(ref=ref('candidate'), title='Тема', summary='Описание',
            source_refs=[ref('source')], discovery_method='manual_topic', discovery_input='Термос',
            assessment=[dict(criterion_key='clarity', rating=4, reason='Reason')], rationale=None)],
        'sources': [dict(ref=ref('source'), title='Источник', locator='https://example.invalid/source',
            rights_ref=ref('rights_review'), source_type='url', author=None, publisher='Publisher',
            published_at=None, accessed_at=AT, access_notes=None, reliability_notes='Needs review', material_digest=None)],
        'claims': [dict(ref=ref('claim'), statement='Утверждение', claim_type='interpretation',
            materiality='material', evidence_links=[dict(source_ref=ref('source'), relation='context',
                locator='p.1', explanation='Context', reviewer='Owner', reviewed_at=AT)],
            review_status='qualified', qualification='Возможно', reviewer='Owner', reviewed_at=AT, reason='Basis')],
        'scripts': [dict(ref=ref('script'), production_ref=ref('production'), candidate_ref=ref('candidate'),
            brief=dict(revision=1, audience='Аудитория', angle='Angle', promise='Promise',
                must_include_claim_refs=[ref('claim')], must_avoid=[], profile_ref=ref('genre_profile')),
            locale='uk', segments=[dict(id=ID, text=TEXT, role='body', claim_refs=[ref('claim')],
                visual_notes=None, pronunciation_notes=None, disclosure_marker='Драматизация')], claim_refs=[ref('claim')])],
        'scene_plans': [dict(ref=ref('scene_plan'), script_ref=ref('script'), scenes=[dict(id=ID,
            start=0, end=len(TEXT), narration_text=TEXT, visual_kind='still', visual_brief='Градиент',
            asset_ref=ref('asset'), estimate_ms=None)])],
        'assets': [dict(ref=ref('asset'), file_ref='media/кадр.png', sha256=HASH, kind='image',
            rights_ref=ref('rights_review'), scene_id=None, script_ref=None, text_digest=None)],
        'rights_reviews': [dict(ref=ref('rights_review'), subject_kind='source', subject_id=ID,
            subject_revision=1, material_digest=HASH, intended_use='test', allowed_actions=[],
            status='unknown', reviewer='Owner', reviewed_at=AT, basis='Needs review', expires_at=None)],
        'approvals': [dict(id=ID, gate='SCRIPT', object_ref=ref('script'), dependency_digest=HASH,
            policy_version='1', actor='Owner', timestamp=AT, decision='revise', reason='Review', review_declarations=[])],
        'events': [dict(id=ID, actor='Owner', at=AT, action='revision_added', refs=[ref('script')], reason='Saved', error_code=None)],
        'active_refs': dict(production=ref('production'), candidate=None, script=ref('script'), scene_plan=None),
        'snapshot_checksum': HASH,
    }


def raw(value):
    return json.dumps(value, ensure_ascii=False).encode('utf-8')


class DecoderTests(unittest.TestCase):
    def bad(self, value, path=None, code=None):
        with self.assertRaises(DecodeError) as caught:
            decode_snapshot(value if type(value) is bytes else raw(value))
        violation = caught.exception.violation
        self.assertTrue(violation.field_path.startswith('$'))
        if path is not None:
            self.assertEqual(violation.field_path, path)
        if code is not None:
            self.assertEqual(violation.code, code)
        return violation

    def test_full_snapshot_all_collections(self):
        result = decode_snapshot(raw(wire()))
        self.assertIsInstance(result, m.ContractSnapshot)
        self.assertEqual(len(result.base.revisions), 9)
        self.assertEqual(tuple(type(r) for r in result.base.revisions), (
            m.ProductionRevision, m.GenreProfile, m.CandidateRevision, m.SourceRevision,
            m.ClaimRevision, m.ScriptRevision, m.ScenePlanRevision, m.AssetRevision, m.RightsReview))
        self.assertEqual(result.base.revisions[0].content_mode, m.ContentMode.HYBRID)
        self.assertEqual(result.base.revisions[5].locale, m.Locale.UK)
        self.assertEqual(result.base.approvals[0].decision, m.ApprovalDecision.REVISE)

    def test_unicode_preserved_exactly(self):
        result = decode_snapshot(raw(wire()))
        self.assertEqual(result.base.revisions[5].segments[0].text, TEXT)
        self.assertEqual(result.base.revisions[6].scenes[0].narration_text, TEXT)
        escaped = json.dumps(wire(), ensure_ascii=True).encode('ascii')
        self.assertEqual(decode_snapshot(escaped), result)

    def test_companions_preserve_every_metadata_field(self):
        result = decode_snapshot(raw(wire()))
        source = result.source_details[0]
        self.assertIsNone(source.author)
        self.assertEqual(source.publisher, 'Publisher')
        self.assertIsNone(source.published_at)
        self.assertEqual(source.accessed_at, AT)
        self.assertEqual(source.reliability_notes, 'Needs review')
        self.assertIsNone(source.material_digest)
        self.assertEqual(result.claim_reviews[0].qualification, 'Возможно')
        self.assertEqual(result.claim_reviews[0].review_status, 'qualified')
        self.assertEqual(result.rights_details[0].subject_kind, m.ObjectKind.SOURCE)
        self.assertIsNone(result.rights_details[0].expires_at)
        self.assertEqual(result.base.revisions[-1].status, m.RightsStatus.UNKNOWN)

    def test_asset_subject_kind_and_expiry_are_preserved(self):
        value = wire()
        value['rights_reviews'][0].update(subject_kind='asset', expires_at='2000-01-01T00:00:00Z')
        result = decode_snapshot(raw(value))
        self.assertEqual(result.rights_details[0].subject_kind, m.ObjectKind.ASSET)
        self.assertEqual(result.rights_details[0].expires_at, '2000-01-01T00:00:00Z')

    def test_active_refs_slots(self):
        result = decode_snapshot(raw(wire()))
        self.assertEqual(result.base.active_refs, (result.base.revisions[0].ref, result.base.revisions[5].ref))
        self.assertIsNone(result.active_selections.candidate)
        self.assertIsNone(result.active_selections.scene_plan)

    def test_empty_draft_and_unresolved_refs_allowed(self):
        value = wire()
        for name in (*COLLECTIONS, 'approvals', 'events'):
            value[name] = []
        result = decode_snapshot(raw(value))
        self.assertEqual(result.base.revisions, ())
        self.assertEqual(result.active_selections.script.kind, m.ObjectKind.SCRIPT)

    def test_input_bytes_required(self):
        for value in ('{}', bytearray(b'{}'), None, {}):
            with self.subTest(value=type(value).__name__), self.assertRaises(DecodeError):
                decode_snapshot(value)

    def test_utf8_bom_and_invalid_bytes(self):
        self.bad(b'\xef\xbb\xbf' + raw(wire()), '$', 'BOM')
        self.bad(b'\xff', '$', 'UTF8')
        self.bad(json.dumps(wire()).encode('utf-16'), '$', 'UTF8')

    def test_duplicate_keys_root_and_nested_escaped(self):
        source = raw(wire())
        self.bad(source.replace(b'"generation": 1', b'"generation": 1, "generation": 2'), '$.generation', 'DUPLICATE_KEY')
        self.bad(source.replace(b'"subject_kind": "source"',
                               b'"subject_kind": "source", "subject_ki\\u006ed": "asset"'),
                 '$.rights_reviews[0].subject_kind', 'DUPLICATE_KEY')

    def test_forbidden_numbers_with_paths(self):
        for token in (b'NaN', b'Infinity', b'-Infinity', b'1.0', b'1e999', b'-0.0'):
            with self.subTest(token=token):
                self.bad(raw(wire()).replace(b'"generation": 1', b'"generation": ' + token), '$.generation', 'NUMBER')

    def test_invalid_json_not_partially_accepted(self):
        for value in (b'', b'{', raw(wire()) + b'{}', b'{"a":1,}', b'{/*comment*/}', b'[]', b'null'):
            with self.subTest(raw=value[:30]):
                self.bad(value)

    def test_unknown_version_and_bool_integer(self):
        for version in (0, 2, '1', True, None):
            value = wire()
            value['editorial_schema_version'] = version
            self.bad(value, '$.editorial_schema_version')
        value = wire()
        value['generation'] = True
        self.bad(value, '$.generation')

    def test_every_root_key_required(self):
        for key in wire():
            value = wire()
            del value[key]
            with self.subTest(key=key):
                self.bad(value, '$.' + key, 'MISSING_FIELD')

    def test_unknown_fields_at_each_level(self):
        for target, path in ((lambda v: v, '$.extra'),
                             (lambda v: v['scripts'][0], '$.scripts[0].extra'),
                             (lambda v: v['scripts'][0]['segments'][0], '$.scripts[0].segments[0].extra'),
                             (lambda v: v['active_refs'], '$.active_refs.extra')):
            value = wire()
            target(value)['extra'] = 1
            self.bad(value, path, 'UNKNOWN_FIELD')

    def test_all_object_collection_fields_required_and_unknown_rejected(self):
        for name in (*COLLECTIONS, 'approvals', 'events'):
            for key in wire()[name][0]:
                value = wire()
                del value[name][0][key]
                with self.subTest(collection=name, key=key):
                    self.bad(value, f'$.{name}[0].{key}', 'MISSING_FIELD')
            value = wire()
            value[name][0]['unknown'] = 1
            self.bad(value, f'$.{name}[0].unknown', 'UNKNOWN_FIELD')

    def test_missing_subject_kind_has_no_default(self):
        value = wire()
        del value['rights_reviews'][0]['subject_kind']
        self.bad(value, '$.rights_reviews[0].subject_kind', 'MISSING_FIELD')
        for kind in ('script', 'SOURCE', None):
            value = wire()
            value['rights_reviews'][0]['subject_kind'] = kind
            self.bad(value, '$.rights_reviews[0].subject_kind')

    def test_incomplete_companion_metadata(self):
        for name, key in (('sources', 'access_notes'), ('claims', 'reviewed_at'), ('rights_reviews', 'expires_at')):
            value = wire()
            del value[name][0][key]
            self.bad(value, f'$.{name}[0].{key}', 'MISSING_FIELD')

    def test_invalid_nulls_and_collection_types(self):
        for key in COLLECTIONS:
            for bad in (None, {}, '[]'):
                value = wire()
                value[key] = bad
                self.bad(value, '$.' + key, 'TYPE')
        value = wire()
        value['scripts'][0]['segments'][0]['text'] = None
        self.bad(value, '$.scripts[0].segments[0].text', 'TYPE')

    def test_invalid_calendar_dates_and_precision(self):
        for date in ('2026-02-30T00:00:00Z', '2026-11-04', '2026-11-04T00:00:00+00:00',
                     '2026-11-04T00:00:00.000Z', '2026-11-04T24:00:00Z'):
            value = wire()
            value['production_revisions'][0]['created_at'] = date
            self.bad(value, '$.production_revisions[0].created_at', 'DATE')
        value = wire()
        value['claims'][0]['evidence_links'][0]['reviewed_at'] = 'yesterday'
        self.bad(value, '$.claims[0].evidence_links[0].reviewed_at', 'DATE')

    def test_closed_values_and_enums(self):
        for name, key, bad in (('production_revisions', 'intended_use', 'free'),
                               ('production_revisions', 'output_preset', 'square'),
                               ('production_revisions', 'script_locale', 'ua'),
                               ('claims', 'materiality', 'important'),
                               ('rights_reviews', 'allowed_actions', ['execute']),
                               ('approvals', 'gate', 'PUBLISH')):
            value = wire()
            value[name][0][key] = bad
            self.bad(value)

    def test_wrong_reference_kinds(self):
        for name in COLLECTIONS:
            value = wire()
            value[name][0]['ref']['kind'] = 'source' if name != 'sources' else 'claim'
            self.bad(value, f'$.{name}[0].ref.kind', 'REFERENCE_KIND')
        value = wire()
        value['scripts'][0]['brief']['profile_ref']['kind'] = 'claim'
        self.bad(value, '$.scripts[0].brief.profile_ref.kind', 'REFERENCE_KIND')
        value = wire()
        value['active_refs']['script']['kind'] = 'asset'
        self.bad(value, '$.active_refs.script.kind', 'REFERENCE_KIND')

    def test_integer_uuid_and_hash_shape(self):
        for key, bad in (('revision', True), ('id', 'not-uuid'), ('content_hash', 'A' * 64)):
            value = wire()
            value['claims'][0]['ref'][key] = bad
            self.bad(value, f'$.claims[0].ref.{key}')
        value = wire()
        value['scene_plans'][0]['scenes'][0]['start'] = False
        self.bad(value)

    def test_revision_order_and_duplicates_not_sorted_away(self):
        value = wire()
        second = copy.deepcopy(value['sources'][0])
        second['ref']['revision'] = 2
        value['sources'].append(second)
        self.assertEqual(decode_snapshot(raw(value)).source_details[1].owner_ref.revision, 2)
        value['sources'].reverse()
        self.bad(value, '$.sources[1].ref', 'REVISION_ORDER')
        value['sources'] = [copy.deepcopy(second), copy.deepcopy(second)]
        self.bad(value, '$.sources[1].ref', 'REVISION_ORDER')

    def test_source_url_and_local_path_validation(self):
        for locator in ('file:///etc/passwd', 'https://user:pass@example.invalid', 'https://', 'http://x:bad', 'https://x/a b'):
            value = wire()
            value['sources'][0]['locator'] = locator
            self.bad(value, '$.sources[0].locator', 'URL')
        value = wire()
        value['sources'][0].update(source_type='local', locator='../secret')
        self.bad(value, '$.sources[0].locator', 'PATH')
        value['sources'][0]['locator'] = 'sources/джерело.txt'
        self.assertEqual(decode_snapshot(raw(value)).base.revisions[3].locator, 'sources/джерело.txt')

    def test_checksum_is_not_verified_or_computed(self):
        value = wire()
        value['snapshot_checksum'] = '0' * 64
        self.assertEqual(decode_snapshot(raw(value)).snapshot_checksum, '0' * 64)
        value['snapshot_checksum'] = '0'
        self.bad(value, '$.snapshot_checksum', 'HASH_FORMAT')

    def test_depth_limit_and_quoted_brackets(self):
        self.bad(b'[' * 65 + b'0' + b']' * 65, '$', 'LIMIT')
        self.bad(b'[' * 64 + b'0' + b']' * 64, '$', 'TYPE')
        value = wire()
        value['candidates'][0]['summary'] = '[' * 70 + '\\"' + ']' * 70
        self.assertEqual(decode_snapshot(raw(value)).base.revisions[2].summary, value['candidates'][0]['summary'])

    def test_raw_size_limit(self):
        self.bad(b' ' * (32 * 1024 * 1024 + 1), '$', 'LIMIT')

    def test_array_and_segment_limits(self):
        value = wire()
        value['events'] = [None] * 10001
        self.bad(value, '$.events', 'LIMIT')
        value = wire()
        value['scripts'][0]['segments'] *= 1001
        self.bad(value, '$.scripts[0].segments', 'LIMIT')

    def test_total_revision_limit_across_collections(self):
        value = wire()
        p = value['profiles'][0]
        c = value['candidates'][0]
        value['profiles'] = [dict(p, ref=ref('genre_profile', i + 1)) for i in range(5000)]
        value['candidates'] = [dict(c, ref=ref('candidate', i + 1)) for i in range(5001)]
        error = self.bad(value, code='LIMIT')
        self.assertIn('Total revisions', error.message)

    def test_string_size_and_unpaired_surrogate(self):
        value = wire()
        value['candidates'][0]['title'] = 'x' * 100000
        self.assertEqual(len(decode_snapshot(raw(value)).base.revisions[2].title), 100000)
        value['candidates'][0]['title'] += 'x'
        self.bad(value, '$.candidates[0].title', 'LIMIT')
        value = wire()
        value['candidates'][0]['title'] = '\ud800'
        self.bad(json.dumps(value).encode(), '$.candidates[0].title', 'UNICODE')

    def test_constructor_failures_are_structured(self):
        value = wire()
        value['profiles'][0]['rubric'][0]['weight_percent'] = 90
        self.bad(value, '$.profiles[0].rubric', 'MODEL_VALUE')
        value = wire()
        value['claims'][0]['qualification'] = None
        self.bad(value, '$.claims[0].qualification', 'MODEL_VALUE')

    def test_duplicate_record_ids_and_mutable_input_not_changed(self):
        value = wire()
        before = copy.deepcopy(value)
        decode_snapshot(raw(value))
        self.assertEqual(value, before)
        for name in ('approvals', 'events'):
            bad = wire()
            bad[name].append(copy.deepcopy(bad[name][0]))
            self.bad(bad, f'$.{name}[1].id', 'DUPLICATE_VALUE')

    def test_nested_field_sets_and_nullable_metadata(self):
        targets = (
            (lambda v: v['scripts'][0]['brief'], '$.scripts[0].brief'),
            (lambda v: v['scripts'][0]['segments'][0], '$.scripts[0].segments[0]'),
            (lambda v: v['scene_plans'][0]['scenes'][0], '$.scene_plans[0].scenes[0]'),
            (lambda v: v['claims'][0]['evidence_links'][0], '$.claims[0].evidence_links[0]'),
            (lambda v: v['profiles'][0]['rubric'][0], '$.profiles[0].rubric[0]'),
            (lambda v: v['candidates'][0]['assessment'][0], '$.candidates[0].assessment[0]'),
            (lambda v: v['claims'][0]['ref'], '$.claims[0].ref'),
            (lambda v: v['active_refs'], '$.active_refs'),
        )
        for get, path in targets:
            for key in get(wire()):
                value = wire()
                del get(value)[key]
                with self.subTest(path=path, key=key):
                    self.bad(value, f'{path}.{key}', 'MISSING_FIELD')
        value = wire()
        value['profiles'][0]['rubric'] = None
        value['candidates'][0]['assessment'] = None
        value['claims'][0].update(review_status='unreviewed', qualification=None,
                                  reviewer=None, reviewed_at=None, reason=None)
        result = decode_snapshot(raw(value))
        self.assertIsNone(result.base.revisions[1].rubric)
        self.assertIsNone(result.base.revisions[2].assessment)
        self.assertIsNone(result.claim_reviews[0].reviewer)

    def test_returned_model_is_frozen(self):
        result = decode_snapshot(raw(wire()))
        with self.assertRaises(FrozenInstanceError):
            result.snapshot_checksum = HASH
        with self.assertRaises(TypeError):
            result.base.revisions[0] = result.base.revisions[0]

    def test_decode_has_no_file_network_or_process_side_effects(self):
        payload = raw(wire())
        code = '''
import sys
decoding = False
def guard(event, args):
    if event.startswith(('socket.', 'subprocess.', 'os.system', 'os.mkdir', 'os.remove', 'os.rename')):
        raise AssertionError(event)
    if event == 'open':
        mode, flags = args[1], args[2]
        if decoding or (isinstance(mode, str) and any(c in mode for c in 'wax+')) or (isinstance(flags, int) and flags & 3):
            raise AssertionError('unexpected file access')
sys.addaudithook(guard)
from editorial.codec import decode_snapshot
decoding = True
result = decode_snapshot(PAYLOAD)
assert len(result.base.revisions) == 9
assert not any(n.split('.')[0] in {'torch','requests','core','scripts','hashlib'} for n in sys.modules)
'''.replace('PAYLOAD', repr(payload))
        result = subprocess.run([sys.executable, '-B', '-c', code], cwd=Path(__file__).resolve().parents[1],
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
