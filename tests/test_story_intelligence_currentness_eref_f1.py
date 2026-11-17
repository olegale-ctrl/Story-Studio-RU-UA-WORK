"""F1-D1 regressions: actual producer ERefs versus historical-only audit refs.

Owner-approved D1-D5 supersede the former T2 behavior characterization. The
original diagnostic reports and fixtures remain historical evidence. Only real
canonical records/hashes, accepted resolver/provenance; no patches.
"""
from copy import deepcopy
import unittest

from story_intelligence.currentness_v1 import check_si_currentness
from story_intelligence.model_v1 import SIValidationError
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


def historical_source_case():
    g, s2, _, _, named = source_case('run')
    r3 = g.run('REVISION', [s2])
    value = deepcopy(g.refs[key(s2)])
    value['H'].update(revision=3, previous=s2, input_refs=[s2],
        origin={'mode':'HUMAN_EDIT', 'run_ref':r3, 'imported_from':None})
    value['payload']['title'] = known('Поточна редакція F1 без ERef')
    s3 = g.add(value, data_refs(value), keep_identity=True)
    named.update(R2=named['R'], R=r3, R3=r3, S3=s3)
    return g, s3, [s3], [], named


def creative_case(with_eref=True, location='original'):
    old, names, active = creative_graph('text_only')
    active += [names['Qa']]
    target = names['C']
    if location in ('current', 'historical'):
        creative = names['K3'] if location == 'current' else names['K2']
        target = old.refs[key(creative)]['H']['origin']['run_ref']
    g, mapping = Graph(), {}
    for original in old.records:
        h = original['H']
        before = {'type':h['type'], 'id':h['id'], 'revision':h['revision'],
                  'sha256':digest(original)}
        value = rewrite(original, mapping)
        if key(before) == key(target) and with_eref:
            value['H']['editorial_refs'] = [eref('source')]
        # All downstream exact refs AND frozen snapshots are rebuilt in their
        # original topological order; no mutation of old graph or fake SHA.
        ref = g.add(value, data_refs(value), keep_identity=True)
        mapping[key(before)] = ref
    named = {name:mapping[key(ref)] for name, ref in names.items()}
    named['R2'] = g.refs[key(named['K2'])]['H']['origin']['run_ref']
    named['R3'] = g.refs[key(named['K3'])]['H']['origin']['run_ref']
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
        'actual_producer':g.refs[key(root)]['H']['origin']['run_ref'],
        'actual':actual}


class RevisionRunERefF1Regressions(unittest.TestCase):
    def test_T1_valid_source_baseline(self):
        case = source_case()
        actual = evidence(case)
        self.assertEqual(3, actual['record_count'])
        self.assertEqual(3, actual['closure_count'])
        self.assertEqual({'currentness':'CURRENT', 'reason_codes':[]}, actual['actual'])

    def test_T2_current_revision_run_header_eref_invalid(self):
        case = source_case('run')
        g, root, _, _, n = case
        self.assertEqual([eref('source')], g.refs[key(n['R'])]['H']['editorial_refs'])
        self.assertEqual([], g.refs[key(root)]['H']['editorial_refs'])
        self.assertIsNone(g.refs[key(root)]['payload']['editorial_ref'])
        actual = evidence(case)
        baseline = evidence(source_case())
        self.assertEqual({'currentness':'INVALID', 'reason_codes':['REF_MISSING']}, actual['actual'])
        self.assertEqual('CURRENT', baseline['actual']['currentness'])
        # The exact historical T2 bytes remain the independent reproducer.
        self.assertEqual('87b0f65a5d741ca48b34333f120f41a5b7cbb2c54e2914e954b108528a41f55b', actual['graph_sha256'])
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

    def test_T5_owner_approved_current_producer_boundary_consistent(self):
        no_eref = evidence(source_case())['actual']
        revision = evidence(source_case('run'))['actual']
        direct = evidence(source_case('source'))['actual']
        creative = evidence(creative_case())['actual']
        self.assertEqual({'currentness':'CURRENT', 'reason_codes':[]}, no_eref)
        for result in (revision, direct, creative):
            self.assertEqual({'currentness':'INVALID', 'reason_codes':['REF_MISSING']}, result)

    def test_T6_current_creative_revision_run_eref_invalid(self):
        case = creative_case(location='current')
        g, root, _, _, n = case
        self.assertEqual([], g.refs[key(n['C'])]['H']['editorial_refs'])
        self.assertEqual([], g.refs[key(root)]['H']['editorial_refs'])
        self.assertEqual([eref('source')], g.refs[key(n['R3'])]['H']['editorial_refs'])
        actual = evidence(case)
        self.assertEqual(n['R3'], actual['actual_producer'])
        self.assertNotEqual(n['C'], actual['actual_producer'])
        self.assertEqual({'currentness':'INVALID', 'reason_codes':['REF_MISSING']}, actual['actual'])

    def test_T7_ordinary_historical_run_only_eref_current(self):
        case = historical_source_case()
        g, root, active, _, n = case
        self.assertEqual([eref('source')], g.refs[key(n['R2'])]['H']['editorial_refs'])
        self.assertEqual([], g.refs[key(n['R3'])]['H']['editorial_refs'])
        self.assertNotIn(n['S2'], active)
        self.assertNotIn(n['R2'], active)
        actual = evidence(case)
        self.assertEqual(5, actual['closure_count'])
        self.assertEqual({'currentness':'CURRENT', 'reason_codes':[]}, actual['actual'])

    def test_T8_creative_historical_run_only_eref_current(self):
        case = creative_case(location='historical')
        g, root, active, _, n = case
        self.assertEqual([eref('source')], g.refs[key(n['R2'])]['H']['editorial_refs'])
        self.assertEqual([], g.refs[key(n['R3'])]['H']['editorial_refs'])
        self.assertEqual([], g.refs[key(n['C'])]['H']['editorial_refs'])
        self.assertNotIn(n['K2'], active)
        self.assertNotIn(n['R2'], active)
        self.assertEqual({'currentness':'CURRENT', 'reason_codes':[]}, evidence(case)['actual'])

    def test_T9_history_integrity_still_fails_closed(self):
        for factory in (historical_source_case, lambda:creative_case(location='historical')):
            for corruption in ('missing_run', 'corrupt_run', 'previous', 'snapshot'):
                with self.subTest(factory=factory.__name__, corruption=corruption):
                    g, root, active, heads, n = factory()
                    if corruption == 'missing_run':
                        g.records.remove(g.refs[key(n['R2'])])
                    elif corruption == 'corrupt_run':
                        g.refs[key(n['R2'])]['payload']['caveats'].append('Tampered historical bytes')
                    elif corruption == 'previous':
                        g.refs[key(root)]['H']['previous']['sha256'] = '0' * 64
                    else:
                        g.refs[key(n['R3'])]['payload']['input_snapshot'][0]['sha256'] = '0' * 64
                    code = 'REF_MISSING' if corruption == 'missing_run' else 'REF_HASH_MISMATCH'
                    for validator in (resolve_si_closure, verify_si_provenance):
                        with self.assertRaises(SIValidationError) as caught:
                            validator(g.records, [root] + active + heads)
                        self.assertEqual(code, caught.exception.code)
                    before = deepcopy((g.records, root, active, heads))
                    self.assertEqual({'currentness':'INVALID', 'reason_codes':[code]},
                        check_si_currentness(g.records, root, active, heads))
                    self.assertEqual(before, (g.records, root, active, heads))

    def test_T10_current_dependency_actual_producer_eref_invalid(self):
        # The guard applies to semantic dependencies too, not just queried root.
        g, source, _, _, _ = source_case('run')
        claim = g.add(fixtures()['ClaimItem'])
        value = fixtures()['EvidenceItem']
        value['payload'].update(claim_ref=claim, source_ref=source)
        value['H']['input_refs'] = [claim, source]
        root = g.add(value, data_refs(value))
        case = (g, root, [claim, source], [], {})
        self.assertEqual({'currentness':'INVALID', 'reason_codes':['REF_MISSING']}, evidence(case)['actual'])


if __name__ == '__main__':
    unittest.main()
