"""F1 diagnostics on unchanged c90b94a: observed behavior, not owner policy.

T2 is a characterization of the actual implementation, NOT an assertion that
CURRENT is contractually correct for a current REVISION Run header ERef.
Only real canonical records/hashes, accepted resolver/provenance; no patches.
"""
from copy import deepcopy
import unittest

from story_intelligence.currentness_v1 import check_si_currentness
from story_intelligence.records_v1 import si_record_ref
from story_intelligence.resolver_v1 import resolve_si_closure
from story_intelligence.provenance_v1 import verify_si_provenance
from tests.test_story_intelligence_records_v1 import fixtures, known, unknown, eref
from tests.test_story_intelligence_resolver_v1 import Graph, digest, key
from tests.test_story_intelligence_provenance_v1 import data_refs, rewrite
from tests.test_story_intelligence_currentness_v1 import creative_graph


def source_case(location=None):
    g = Graph()
    original = fixtures()['SourceItem']
    s1 = g.add(original)
    run = fixtures()['RunRecord']
    snapshot = g.closure([s1])
    run['H']['input_refs'] = deepcopy(snapshot)
    run['H']['editorial_refs'] = [eref('source')] if location == 'run' else []
    run['payload'].update(stage='REVISION', method_id='si.human-revision',
        semantic_input_refs=[s1], input_snapshot=snapshot, rubric_ref=None,
        context_snapshot={'context_version':1, 'active_input_refs':[],
            'selection_head_refs':[], 'editorial_snapshot_sha256':unknown()},
        editorial_snapshot_sha256=unknown())
    r = g.add(run, data_refs(run))
    current = deepcopy(g.refs[key(s1)])
    current['H'].update(revision=2, previous=s1, input_refs=[s1],
        origin={'mode':'HUMAN_EDIT', 'run_ref':r, 'imported_from':None},
        editorial_refs=[eref('source')] if location == 'source' else [])
    current['payload']['title'] = known('Синтетична ручна редакція F1')
    s2 = g.add(current, data_refs(current), keep_identity=True)
    return g, s2, [s2], [], {'S1':s1, 'R':r, 'S2':s2}


def creative_case(with_eref=True):
    old, names, active = creative_graph('text_only')
    active += [names['Qa']]
    g, mapping = Graph(), {}
    for original in old.records:
        h = original['H']
        before = {'type':h['type'], 'id':h['id'], 'revision':h['revision'],
                  'sha256':digest(original)}
        value = rewrite(original, mapping)
        if key(before) == key(names['C']) and with_eref:
            value['H']['editorial_refs'] = [eref('source')]
        # All downstream exact refs AND frozen snapshots are rebuilt in their
        # original topological order; no mutation of old graph or fake SHA.
        ref = g.add(value, data_refs(value), keep_identity=True)
        mapping[key(before)] = ref
    named = {name:mapping[key(ref)] for name, ref in names.items()}
    return g, named['K3'], rewrite(active, mapping), [], named


def evidence(case):
    """Run real APIs before reporting literal input digests and actual result."""
    g, root, active, heads, named = case
    before = deepcopy((g.records, root, active, heads))
    expected = g.closure([root] + active + heads)
    resolved = resolve_si_closure(g.records, [root] + active + heads)
    proven = verify_si_provenance(g.records, [root] + active + heads)
    assert expected == resolved == proven
    for record in g.records:
        h = record['H']
        assert si_record_ref(record) == {'type':h['type'], 'id':h['id'],
            'revision':h['revision'], 'sha256':digest(record)}
    actual = check_si_currentness(g.records, root, active, heads)
    assert before == (g.records, root, active, heads)
    return {'record_count':len(g.records), 'closure_count':len(resolved),
        'graph_sha256':digest(g.records),
        'context_sha256':digest({'active_input_refs':active, 'selection_head_refs':heads}),
        'root':root, 'producer':named.get('R', named.get('C')),
        'actual':actual}


class RevisionRunERefF1Diagnostics(unittest.TestCase):
    def test_T1_valid_source_baseline(self):
        case = source_case()
        actual = evidence(case)
        self.assertEqual(3, actual['record_count'])
        self.assertEqual(3, actual['closure_count'])
        self.assertEqual({'currentness':'CURRENT', 'reason_codes':[]}, actual['actual'])

    def test_T2_observe_current_revision_run_header_eref(self):
        case = source_case('run')
        g, root, _, _, n = case
        self.assertEqual([eref('source')], g.refs[key(n['R'])]['H']['editorial_refs'])
        self.assertEqual([], g.refs[key(root)]['H']['editorial_refs'])
        self.assertIsNone(g.refs[key(root)]['payload']['editorial_ref'])
        actual = evidence(case)
        baseline = evidence(source_case())
        # Characterize the asymmetry, without declaring the policy correct.
        self.assertEqual(baseline['actual'], actual['actual'])
        self.assertNotEqual(baseline['graph_sha256'], actual['graph_sha256'])
        self.assertNotEqual(baseline['producer']['sha256'], actual['producer']['sha256'])
        self.assertNotEqual(baseline['root']['sha256'], actual['root']['sha256'])

    def test_T3_direct_source_header_eref_control(self):
        actual = evidence(source_case('source'))
        self.assertEqual({'currentness':'INVALID', 'reason_codes':['REF_MISSING']}, actual['actual'])

    def test_T4_original_creative_header_eref_control(self):
        baseline = evidence(creative_case(False))
        actual = evidence(creative_case(True))
        self.assertEqual({'currentness':'CURRENT', 'reason_codes':[]}, baseline['actual'])
        self.assertEqual({'currentness':'INVALID', 'reason_codes':['REF_MISSING']}, actual['actual'])
        self.assertNotEqual(baseline['producer']['sha256'], actual['producer']['sha256'])
        self.assertNotEqual(baseline['root']['sha256'], actual['root']['sha256'])

    def test_T5_behavior_comparison_is_not_contract_adjudication(self):
        no_eref = evidence(source_case())['actual']
        revision = evidence(source_case('run'))['actual']
        direct = evidence(source_case('source'))['actual']
        creative = evidence(creative_case())['actual']
        self.assertEqual(no_eref, revision)
        self.assertEqual(direct, creative)
        self.assertNotEqual(revision, direct)
        # Contract interpretation is documented in RESULT/GAPS, not manufactured
        # as a successful runtime proof by changing checker or accepted contracts.


if __name__ == '__main__':
    unittest.main()
