"""E01.3.3 Source/Asset to RightsReview subject/material binding tests."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import unittest

from editorial import model as m
from editorial.codec import decode_snapshot, encode_snapshot
from editorial.graph import validate_reference_graph
from editorial.integrity import compute_revision_content_hash
from editorial.rights_binding import (
    MaterialBindingState,
    RightsBindingError,
    validate_all_rights_bindings,
    validate_rights_binding,
)
from test_editorial_codec import HASH, ID, raw, ref, wire


ID2 = '20000000-0000-0000-0000-000000000002'


def _replace_exact_ref_hash(value, identity, digest):
    if type(value) is dict:
        if {'kind', 'id', 'revision', 'content_hash'} <= value.keys():
            key = value['kind'], value['id'], value['revision']
            if key == identity:
                value['content_hash'] = digest
        for child in value.values():
            _replace_exact_ref_hash(child, identity, digest)
    elif type(value) is list:
        for child in value:
            _replace_exact_ref_hash(child, identity, digest)


def fixture_wire(mutate=None):
    value = wire()
    value['sources'][0]['material_digest'] = HASH
    asset_rights = copy.deepcopy(value['rights_reviews'][0])
    asset_rights.update(ref=ref('rights_review', 2), subject_kind='asset',
                        subject_revision=1, material_digest=HASH)
    value['rights_reviews'].append(asset_rights)
    value['assets'][0]['rights_ref'] = ref('rights_review', 2)
    value['active_refs'].update(candidate=value['candidates'][0]['ref'].copy(),
                                scene_plan=value['scene_plans'][0]['ref'].copy())
    if mutate is not None:
        mutate(value)

    for kind in ('genre_profile', 'rights_review', 'source', 'candidate', 'claim',
                 'production', 'script', 'asset', 'scene_plan'):
        snapshot = decode_snapshot(raw(value))
        revisions = tuple(r for r in snapshot.base.revisions if r.ref.kind.value == kind)
        for revision in revisions:
            companions = {
                'source': snapshot.source_details,
                'claim': snapshot.claim_reviews,
                'rights_review': snapshot.rights_details,
            }.get(kind, ())
            companion = next((c for c in companions
                              if (c.owner_ref.kind, c.owner_ref.id, c.owner_ref.revision) ==
                                 (revision.ref.kind, revision.ref.id, revision.ref.revision)), None)
            digest = compute_revision_content_hash(revision, companion)
            _replace_exact_ref_hash(value,
                (revision.ref.kind.value, revision.ref.id, revision.ref.revision), digest)
    return value


def fixture(mutate=None):
    snapshot = decode_snapshot(raw(fixture_wire(mutate)))
    return snapshot, validate_reference_graph(snapshot)


class RightsBindingTests(unittest.TestCase):
    def bad(self, mutate, code, path):
        snapshot, graph = fixture(mutate)
        with self.assertRaises(RightsBindingError) as caught:
            validate_all_rights_bindings(snapshot, graph)
        violation = caught.exception.violation
        self.assertEqual(violation.code, code)
        self.assertEqual(violation.field_path, path)
        return violation

    def test_confirmed_source_and_asset_bindings(self):
        snapshot, graph = fixture()
        results = validate_all_rights_bindings(snapshot, graph)
        self.assertEqual(tuple(result.subject_ref.kind for result in results),
                         (m.ObjectKind.SOURCE, m.ObjectKind.ASSET))
        self.assertTrue(all(result.structural_match for result in results))
        self.assertTrue(all(result.material_state is MaterialBindingState.CONFIRMED
                            for result in results))
        self.assertEqual(results[0].rights_ref.revision, 1)
        self.assertEqual(results[1].rights_ref.revision, 2)

    def test_wrong_subject_kind(self):
        self.bad(lambda value: value['rights_reviews'][0].update(subject_kind='asset'),
                 'SUBJECT_KIND_MISMATCH', '$.rights_reviews[0].subject_kind')

    def test_wrong_subject_id(self):
        self.bad(lambda value: value['rights_reviews'][0].update(subject_id=ID2),
                 'SUBJECT_ID_MISMATCH', '$.rights_reviews[0].subject_id')

    def test_wrong_subject_revision(self):
        self.bad(lambda value: value['rights_reviews'][0].update(subject_revision=2),
                 'SUBJECT_REVISION_MISMATCH', '$.rights_reviews[0].subject_revision')

    def test_material_digest_mismatch(self):
        self.bad(lambda value: value['rights_reviews'][0].update(material_digest='b' * 64),
                 'MATERIAL_DIGEST_MISMATCH', '$.sources[0].material_digest')
        self.bad(lambda value: value['rights_reviews'][1].update(material_digest='b' * 64),
                 'MATERIAL_DIGEST_MISMATCH', '$.assets[0].sha256')

    def test_missing_source_digest_is_unconfirmed_not_error(self):
        def mutate(value):
            value['sources'][0]['material_digest'] = None
            value['rights_reviews'][0]['status'] = 'approved'

        snapshot, graph = fixture(mutate)
        source = next(r for r in snapshot.base.revisions if type(r) is m.SourceRevision)
        result = validate_rights_binding(snapshot, graph, source)
        self.assertTrue(result.structural_match)
        self.assertIs(result.material_state, MaterialBindingState.UNCONFIRMED)
        self.assertFalse(hasattr(result, 'allowed'))
        self.assertFalse(hasattr(result, 'is_permitted'))

    def test_historical_revisions_are_all_checked_and_multiple_reviews_allowed(self):
        def mutate(value):
            second_source = copy.deepcopy(value['sources'][0])
            second_source.update(ref=ref('source', 2), rights_ref=ref('rights_review', 3))
            value['sources'].append(second_source)
            second_rights = copy.deepcopy(value['rights_reviews'][0])
            second_rights.update(ref=ref('rights_review', 3), subject_revision=2)
            value['rights_reviews'].append(second_rights)

        snapshot, graph = fixture(mutate)
        results = validate_all_rights_bindings(snapshot, graph)
        self.assertEqual(tuple((r.subject_ref.kind.value, r.subject_ref.revision) for r in results),
                         (('source', 1), ('source', 2), ('asset', 1)))
        self.assertTrue(all(r.material_state is MaterialBindingState.CONFIRMED for r in results))

    def test_multiple_reviews_for_same_exact_subject_are_allowed(self):
        def mutate(value):
            alternative = copy.deepcopy(value['rights_reviews'][0])
            alternative.update(ref=ref('rights_review', 3), basis='Alternative review')
            value['rights_reviews'].append(alternative)

        snapshot, graph = fixture(mutate)
        source = next(r for r in snapshot.base.revisions if type(r) is m.SourceRevision)
        result = validate_rights_binding(snapshot, graph, source)
        self.assertEqual(result.rights_ref.revision, 1)
        reviews = [r for r, details in zip(snapshot.rights_reviews, snapshot.rights_details)
                   if details.subject_kind is m.ObjectKind.SOURCE and
                      (r.subject_id, r.subject_revision) == (source.ref.id, source.ref.revision)]
        self.assertEqual(len(reviews), 2)

    def test_rights_status_is_data_not_authority(self):
        states = []
        for status in ('approved', 'restricted', 'unknown', 'blocked'):
            snapshot, graph = fixture(
                lambda value, status=status: value['rights_reviews'][0].update(status=status))
            source = next(r for r in snapshot.base.revisions if type(r) is m.SourceRevision)
            result = validate_rights_binding(snapshot, graph, source)
            states.append(result.material_state)
            self.assertFalse(hasattr(result, 'allowed'))
        self.assertEqual(states, [MaterialBindingState.CONFIRMED] * 4)

    def test_no_reverse_dependency_edge_is_added(self):
        snapshot, graph = fixture()
        before = graph.edges
        validate_all_rights_bindings(snapshot, graph)
        self.assertEqual(graph.edges, before)
        rights_keys = {(m.ObjectKind.RIGHTS_REVIEW, ID, 1),
                       (m.ObjectKind.RIGHTS_REVIEW, ID, 2)}
        self.assertFalse(any(edge.source in rights_keys for edge in graph.edges))

    def test_validation_is_pure_and_has_no_io(self):
        snapshot, _ = fixture()
        payload = encode_snapshot(snapshot)
        code = '''
import sys
active = False
def guard(event, args):
    if active and (event == 'open' or event.startswith(('socket.', 'subprocess.', 'os.system'))):
        raise AssertionError(event)
sys.addaudithook(guard)
from editorial.codec import decode_snapshot
from editorial.graph import validate_reference_graph
from editorial.rights_binding import validate_all_rights_bindings
snapshot = decode_snapshot(PAYLOAD)
graph = validate_reference_graph(snapshot)
active = True
results = validate_all_rights_bindings(snapshot, graph)
assert len(results) == 2
'''.replace('PAYLOAD', repr(payload))
        result = subprocess.run([sys.executable, '-B', '-c', code],
            cwd=Path(__file__).resolve().parents[1], capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
