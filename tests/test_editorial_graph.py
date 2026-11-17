"""E01.3.2 exact reference index and dependency graph tests."""
import copy
from dataclasses import replace
import json
from pathlib import Path
import subprocess
import sys
import unittest

from editorial import model as m
from editorial.codec import decode_snapshot, encode_snapshot
from editorial.graph import GraphValidationError, build_revision_index, validate_reference_graph
from editorial.integrity import compute_revision_content_hash
from test_editorial_codec import HASH, ID, raw, wire


ID2 = '20000000-0000-0000-0000-000000000002'


def _replace_ref_hashes(value, kind, digest):
    if type(value) is dict:
        if {'kind', 'id', 'revision', 'content_hash'} <= value.keys() and value['kind'] == kind:
            value['content_hash'] = digest
        for child in value.values():
            _replace_ref_hashes(child, kind, digest)
    elif type(value) is list:
        for child in value:
            _replace_ref_hashes(child, kind, digest)


def valid_wire():
    value = wire()
    value['active_refs'].update(candidate=value['candidates'][0]['ref'].copy(),
                                scene_plan=value['scene_plans'][0]['ref'].copy())
    order = ('genre_profile', 'rights_review', 'source', 'candidate', 'claim',
             'production', 'script', 'asset', 'scene_plan')
    for kind in order:
        snapshot = decode_snapshot(raw(value))
        revision = next(r for r in snapshot.base.revisions if r.ref.kind.value == kind)
        companion = {
            'source': snapshot.source_details[0],
            'claim': snapshot.claim_reviews[0],
            'rights_review': snapshot.rights_details[0],
        }.get(kind)
        _replace_ref_hashes(value, kind, compute_revision_content_hash(revision, companion))
    return value


def valid_snapshot():
    return decode_snapshot(raw(valid_wire()))


class ReferenceGraphTests(unittest.TestCase):
    def setUp(self):
        self.snapshot = valid_snapshot()

    def bad(self, snapshot, code=None, path=None):
        with self.assertRaises(GraphValidationError) as caught:
            validate_reference_graph(snapshot)
        violation = caught.exception.violation
        self.assertTrue(violation.field_path.startswith('$'))
        if code is not None:
            self.assertEqual(violation.code, code)
        if path is not None:
            self.assertEqual(violation.field_path, path)
        return violation

    def revision(self, kind):
        return next(r for r in self.snapshot.base.revisions if r.ref.kind is kind)

    def with_revision(self, old, new):
        revisions = tuple(new if item is old else item for item in self.snapshot.base.revisions)
        return replace(self.snapshot, base=replace(self.snapshot.base, revisions=revisions))

    def test_valid_all_nine_type_graph_and_exact_index(self):
        before = copy.deepcopy(self.snapshot)
        graph = validate_reference_graph(self.snapshot)
        self.assertEqual(len(graph.index), 9)
        self.assertEqual(len(graph.edges), 13)
        for revision in self.snapshot.base.revisions:
            self.assertIs(graph.resolve(revision.ref), revision)
        self.assertEqual(self.snapshot, before)
        with self.assertRaises(TypeError):
            graph.index[('x', ID, 1)] = None
        self.assertEqual(build_revision_index(self.snapshot), graph.index)

    def test_missing_target(self):
        candidate = self.revision(m.ObjectKind.CANDIDATE)
        missing = replace(candidate.source_refs[0], id=ID2)
        changed = replace(candidate, source_refs=(missing,))
        self.bad(self.with_revision(candidate, changed), 'MISSING_TARGET',
                 '$.candidates[0].source_refs[0]')

    def test_wrong_normative_target_kind(self):
        production = self.revision(m.ObjectKind.PRODUCTION)
        wrong = self.revision(m.ObjectKind.SOURCE).ref
        changed = replace(production, profile_ref=wrong)
        self.bad(self.with_revision(production, changed), 'REFERENCE_KIND_MISMATCH',
                 '$.production_revisions[0].profile_ref.kind')

    def test_wrong_revision_number(self):
        candidate = self.revision(m.ObjectKind.CANDIDATE)
        wrong = replace(candidate.source_refs[0], revision=99)
        changed = replace(candidate, source_refs=(wrong,))
        self.bad(self.with_revision(candidate, changed), 'TARGET_REVISION_MISMATCH',
                 '$.candidates[0].source_refs[0]')

    def test_reference_content_hash_must_match_target(self):
        candidate = self.revision(m.ObjectKind.CANDIDATE)
        wrong = replace(candidate.source_refs[0], content_hash='b' * 64)
        changed = replace(candidate, source_refs=(wrong,))
        self.bad(self.with_revision(candidate, changed), 'REFERENCE_HASH_MISMATCH',
                 '$.candidates[0].source_refs[0].content_hash')

    def test_target_supplied_hash_must_match_computed_hash(self):
        value = valid_wire()
        _replace_ref_hashes(value, 'source', 'b' * 64)
        snapshot = decode_snapshot(raw(value))
        self.bad(snapshot, 'TARGET_HASH_INVALID', '$.sources[0].ref.content_hash')

    def test_duplicate_exact_identity_is_rejected(self):
        corrupted_base = copy.copy(self.snapshot.base)
        object.__setattr__(corrupted_base, 'revisions',
                           self.snapshot.base.revisions + (self.snapshot.base.revisions[-1],))
        corrupted = copy.copy(self.snapshot)
        object.__setattr__(corrupted, 'base', corrupted_base)
        self.bad(corrupted, 'DUPLICATE_IDENTITY')

    def test_revision_class_must_match_declared_kind(self):
        production = self.revision(m.ObjectKind.PRODUCTION)
        header = m.EditorialRevision(production.ref)
        corrupted_base = copy.copy(self.snapshot.base)
        object.__setattr__(corrupted_base, 'revisions',
                           (header,) + self.snapshot.base.revisions[1:])
        corrupted = copy.copy(self.snapshot)
        object.__setattr__(corrupted, 'base', corrupted_base)
        self.bad(corrupted, 'REVISION_KIND_MISMATCH',
                 '$.production_revisions[0].ref.kind')

    def test_cycle_is_diagnosed_before_kind_error(self):
        source = self.revision(m.ObjectKind.SOURCE)
        cyclic = replace(source, rights_ref=source.ref)
        error = self.bad(self.with_revision(source, cyclic), 'DEPENDENCY_CYCLE',
                         '$.sources[0].rights_ref')
        self.assertIn('source:', error.message)

    def test_multiple_revisions_of_one_uuid_are_valid_history(self):
        source = self.revision(m.ObjectKind.SOURCE)
        details = self.snapshot.source_details[0]
        draft_ref = replace(source.ref, revision=2, content_hash='0' * 64)
        draft = replace(source, ref=draft_ref)
        draft_details = replace(details, owner_ref=draft_ref)
        digest = compute_revision_content_hash(draft, draft_details)
        final_ref = replace(draft_ref, content_hash=digest)
        second = replace(draft, ref=final_ref)
        second_details = replace(draft_details, owner_ref=final_ref)
        revisions = list(self.snapshot.base.revisions)
        position = revisions.index(source) + 1
        revisions.insert(position, second)
        changed = replace(self.snapshot,
            base=replace(self.snapshot.base, revisions=tuple(revisions)),
            source_details=(details, second_details))
        graph = validate_reference_graph(changed)
        self.assertEqual(len(graph.index), 10)
        self.assertIs(graph.resolve(second.ref), second)

    def test_rights_subject_binding_is_not_dependency_edge(self):
        graph = validate_reference_graph(self.snapshot)
        rights_key = (m.ObjectKind.RIGHTS_REVIEW, ID, 1)
        self.assertFalse(any(edge.source == rights_key for edge in graph.edges))
        source_key = (m.ObjectKind.SOURCE, ID, 1)
        self.assertTrue(any(edge.source == source_key and edge.target == rights_key
                            for edge in graph.edges))

    def test_active_refs_are_exact_and_nullable_slots_are_allowed(self):
        self.assertIsNotNone(validate_reference_graph(self.snapshot))
        active = list(self.snapshot.base.active_refs)
        active[0] = replace(active[0], id=ID2)
        changed = replace(self.snapshot, base=replace(self.snapshot.base, active_refs=tuple(active)))
        self.bad(changed, 'MISSING_TARGET', '$.active_refs.production')
        only_script = replace(self.snapshot.base, active_refs=(self.snapshot.active_selections.script,))
        self.assertIsNotNone(validate_reference_graph(replace(self.snapshot, base=only_script)))

    def test_production_ownership_checks_only_explicit_fields(self):
        production = self.revision(m.ObjectKind.PRODUCTION)
        foreign = replace(production, ref=replace(production.ref, id=ID2))
        corrupted_base = copy.copy(self.snapshot.base)
        object.__setattr__(corrupted_base, 'revisions',
                           (foreign,) + self.snapshot.base.revisions[1:])
        corrupted = copy.copy(self.snapshot)
        object.__setattr__(corrupted, 'base', corrupted_base)
        self.bad(corrupted, 'FOREIGN_PRODUCTION', '$.production_revisions[0].ref.id')

    def test_approval_and_event_refs_resolve_but_are_not_edges(self):
        graph = validate_reference_graph(self.snapshot)
        self.assertFalse(any(edge.field_path.startswith(('$.approvals', '$.events'))
                             for edge in graph.edges))
        approval = replace(self.snapshot.base.approvals[0],
                           object_ref=replace(self.snapshot.base.approvals[0].object_ref, id=ID2))
        changed = replace(self.snapshot,
                          base=replace(self.snapshot.base, approvals=(approval,)))
        self.bad(changed, 'MISSING_TARGET', '$.approvals[0].object_ref')

    def test_validation_has_no_io_or_side_effects(self):
        payload = encode_snapshot(self.snapshot)
        code = '''
import sys
active = False
def guard(event, args):
    if active and (event == 'open' or event.startswith(('socket.', 'subprocess.', 'os.system'))):
        raise AssertionError(event)
sys.addaudithook(guard)
from editorial.codec import decode_snapshot
from editorial.graph import validate_reference_graph
snapshot = decode_snapshot(PAYLOAD)
active = True
graph = validate_reference_graph(snapshot)
assert len(graph.index) == 9
'''.replace('PAYLOAD', repr(payload))
        result = subprocess.run([sys.executable, '-B', '-c', code],
            cwd=Path(__file__).resolve().parents[1], capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
