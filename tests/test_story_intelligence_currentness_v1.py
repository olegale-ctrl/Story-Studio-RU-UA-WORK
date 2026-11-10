"""Independent authored graphs/edges; no production hash or resolver patches."""
from copy import deepcopy as cp
import unittest

from story_intelligence.currentness_v1 import check_si_currentness
from story_intelligence.model_v1 import SIValidationError
from story_intelligence.provenance_v1 import verify_si_provenance
from story_intelligence.resolver_v1 import resolve_si_closure
from tests.test_story_intelligence_records_v1 import fixtures, known, unknown, eref
from tests.test_story_intelligence_resolver_v1 import Graph, key, digest
from tests.test_story_intelligence_provenance_v1 import data_refs


def revise(g, prior, **updates):
    value = cp(g.refs[key(prior)])
    value['payload'].update(updates)
    roots = [prior] + data_refs(value['payload'])
    run = g.run('REVISION', roots)
    value['H'].update(revision=prior['revision'] + 1, previous=prior, input_refs=roots,
        origin={'mode':'HUMAN_EDIT', 'run_ref':run, 'imported_from':None})
    return g.add(value, data_refs(value), keep_identity=True)


def source_graph():
    g = Graph()
    v = fixtures()['SourceItem']
    v['H']['origin'] = {'mode':'USER_IMPORT', 'run_ref':None, 'imported_from':unknown()}
    s1 = g.add(v)
    s2 = revise(g, s1, title=known('Джерело редакції 2'))
    s3 = revise(g, s2, title=known('Джерело редакції 3'))
    return g, {'S1':s1, 'S2':s2, 'S3':s3}, [s3]


def creative_graph(mode='changed_hook', bindings=False, external=False, audit_only=False):
    """Default exactly reproduces published G02 bytes, 19 records, in order.

    Direct C inputs and current payload roles are authored independently of the
    implementation. Optional graphs are rebuilt topologically, never rehashed by
    the checker and never disguised as valid by mocks.
    """
    t, g, n = fixtures(), Graph(), {}

    def put(name, kind, **updates):
        v = cp(t[kind]); v['payload'].update(updates)
        ref = g.add(v, data_refs(v)); n[name] = ref
        return ref

    i = put('I', 'Intake')
    s = put('S', 'SourceItem', **({'editorial_ref':eref('source')} if external else {}))
    qa = put('Qa', 'ClaimItem', statement='Синтетична гіпотеза A', claim_kind='fictional')
    qb = put('Qb', 'ClaimItem', statement='Синтетична гіпотеза B', claim_kind='fictional')
    qc = put('Qc', 'ClaimItem', statement='Синтетична гіпотеза C', claim_kind='fictional')
    d = g.run('DISCOVERY', [i, s])
    v = cp(t['StoryIdea']); v['H']['origin']['run_ref'] = d; v['H']['input_refs'] = [i, s]
    v['payload'].update(intake_ref=i, source_refs=known([s]))
    idea = g.add(v, data_refs(v)); n['Idea'] = idea
    au = put('Audience', 'AudienceHypothesis')
    ch = put('Channel', 'ChannelContext', audience_ref=au)
    a = put('Angle', 'Angle', idea_ref=idea, audience_ref=au, claim_refs=[])
    ru = put('Rubric', 'Rubric')
    extra = []
    if bindings:
        ev = put('Evidence', 'EvidenceItem', claim_ref=qa, source_ref=s)
        check = put('Check', 'ClaimCheck', claim_ref=qa, evidence_refs=known([ev]))
        risk = put('Risk', 'Risk', basis_refs=[qa], resolution_basis_refs=[])
        extra = [check, risk]
    eroots = [idea, a, au, ch, ru] + extra
    er = g.run('EVALUATION', eroots, rubric=ru)
    v = cp(t['EvaluationReport']); v['H']['origin']['run_ref'] = er; v['H']['input_refs'] = eroots
    v['payload'].update(idea_ref=idea, angle_ref=a, audience_ref=au,
                        channel_ref=ch, rubric_ref=ru, run_ref=er)
    if bindings:
        v['payload']['ratings'][0]['basis_refs'] = [n['Check']]
        v['payload']['risk_refs'] = [n['Risk']]
    e = g.add(v, data_refs(v)); n['E1'] = e
    ctx = None
    if audit_only:
        other = put('AuditOnlySource', 'SourceItem', title=known('Лише audit context'))
        ctx = {'context_version':1, 'active_input_refs':[other],
               'selection_head_refs':[], 'editorial_snapshot_sha256':unknown()}
    croots = [a, idea, au, ch, e, qa, qb] + extra
    c = g.run('CREATIVE', croots, ctx); n['C'] = c
    v = cp(t['CreativeAlternative']); v['H']['origin']['run_ref'] = c; v['H']['input_refs'] = croots
    v['payload'].update(angle_ref=a, run_ref=c, hook_claim_refs=[qa])
    v['payload']['chapters'][0]['claim_refs'] = [qa if mode == 'shared' else qb]
    prior = g.add(v, data_refs(v)); n['K1'] = prior
    for revision in (2, 3):
        updates = {'hook_claim_refs':[qa if mode == 'text_only' else qc],
                   'hook_text':f'Уявний сюжет, редакція {revision}'}
        if mode == 'changed_angle' and revision == 3:
            v = cp(g.refs[key(idea)]); v['payload']['title'] = 'Інша постановка'
            new_idea = g.add(v, data_refs(v)); n['NewIdea'] = new_idea
            new_a = put('NewAngle', 'Angle', idea_ref=new_idea, audience_ref=au, claim_refs=[qc])
            updates['angle_ref'] = new_a
        prior = revise(g, prior, **updates); n[f'K{revision}'] = prior
    active = [n[name] for name in ('I', 'S', 'Idea', 'Audience', 'Channel', 'Angle',
                                  'Rubric', 'E1', 'Qb', 'Qc', 'K3')]
    active += [n[name] for name in ('Evidence', 'Check', 'Risk', 'NewIdea', 'NewAngle') if name in n]
    return g, n, sorted(active, key=key)


def add_selection(g, n, target, purpose='CREATIVE_CHOICE', previous=None):
    v = fixtures()['Selection']
    v['payload']['scope'].update(purpose=purpose, idea_ref=n['Idea'],
                                audience_ref=n['Audience'], channel_ref=n['Channel'])
    v['payload']['target_ref'] = target
    if previous is not None:
        v['H'].update(id=previous['id'], revision=previous['revision'] + 1, previous=previous)
    return g.add(v, data_refs(v), keep_identity=previous is not None)


def brief_graph():
    g, n, active = creative_graph()
    active += [n['Qa']]
    selected = add_selection(g, n, n['K3']); n['Selected'] = selected
    v = fixtures()['ProductionBrief']; p = v['payload']
    p.update(idea_ref=n['Idea'], audience_ref=n['Audience'], channel_ref=n['Channel'],
             angle_ref=n['Angle'], evaluation_ref=n['E1'], creative_ref=n['K3'],
             source_refs=[n['S']], claim_refs=[n['Qa'], n['Qb'], n['Qc']],
             claim_check_refs=[], visual_refs=[], risk_refs=[], profile_ref=None,
             creative_selection_ref=selected)
    roots = data_refs(p)
    run = g.run('BRIEF_ASSEMBLY', roots, rubric=n['Rubric'])
    v['H']['origin'] = {'mode':'RULE_DERIVED', 'run_ref':run, 'imported_from':None}
    v['H']['input_refs'] = roots
    brief = g.add(v, data_refs(v)); n['B1'] = brief
    active.append(brief)
    return g, n, sorted(active, key=key), [selected]


class CurrentnessTests(unittest.TestCase):
    def assert_state(self, g, root, active, heads, state, codes=()):
        before = cp((g.records, root, active, heads))
        # Independent explicit-edge oracle and BOTH accepted APIs. Positive and
        # STALE cases must be genuine valid bundles, not fake hash successes.
        self.assertEqual(g.closure([root] + active + heads),
                         resolve_si_closure(g.records, [root] + active + heads))
        self.assertEqual(g.closure([root] + active + heads),
                         verify_si_provenance(g.records, [root] + active + heads))
        result = check_si_currentness(g.records, root, active, heads)
        self.assertEqual({'currentness':state, 'reason_codes':list(codes)}, result)
        self.assertEqual(before, (g.records, root, active, heads))
        return result

    def test_G01_source_three_revisions_inactive_bases_current(self):
        g, n, active = source_graph()
        self.assertEqual(5, len(g.records))
        self.assert_state(g, n['S3'], active, [], 'CURRENT')

    def test_G01_missing_or_corrupt_edit_base_invalid(self):
        for corrupt in (False, True):
            g, n, active = source_graph()
            if corrupt: g.refs[key(n['S2'])]['payload']['title'] = known('Corrupted')
            else: g.records.remove(g.refs[key(n['S2'])])
            self.assertEqual({'currentness':'INVALID', 'reason_codes':[
                'REF_HASH_MISMATCH' if corrupt else 'REF_MISSING']},
                check_si_currentness(g.records, n['S3'], active, []))

    def test_G02_exact_published_graph_and_stale_or_current(self):
        g, n, active = creative_graph()
        self.assertEqual('d8f2a8439f9ce3cfa6db385382eb07cbe296e1edc29ccfac5f52a07090be0975', digest(g.records))
        self.assertEqual('2e29b4a85cb640df76ffdbad34214f95f53a5e8fd58d5a298746be2e7ef8be0d',
                         digest({'active_input_refs':active, 'selection_head_refs':[]}))
        self.assert_state(g, n['K3'], active, [], 'STALE', ['INPUT_STALE'])
        self.assert_state(g, n['K3'], active + [n['Qa']], [], 'CURRENT')

    def test_G01_G02_text_only_K1_K2_K3_current_without_ancestral_identities(self):
        g, n, active = creative_graph('text_only')
        active += [n['Qa']]
        for version in ('K1', 'K2', 'K3'):
            self.assert_state(g, n[version], active, [], 'CURRENT')
        self.assertNotIn(n['K1'], active); self.assertNotIn(n['K2'], active)
        for version in ('K1', 'K2', 'K3'):
            self.assertEqual(n['C'], g.refs[key(n[version])]['payload']['run_ref'])

    def test_G02_shared_hook_chapter_claim_and_independent_check_risk(self):
        for mode, bindings in (('shared', False), ('changed_hook', True)):
            g, n, active = creative_graph(mode, bindings)
            self.assert_state(g, n['K3'], active, [], 'STALE', ['INPUT_STALE'])
            self.assert_state(g, n['K3'], active + [n['Qa']], [], 'CURRENT')

    def test_G02_missing_or_corrupt_original_claim_invalid(self):
        for corrupt in (False, True):
            g, n, active = creative_graph()
            record = g.refs[key(n['Qa'])]
            if corrupt: record['payload']['statement'] = 'Changed immutable bytes'
            else: g.records.remove(record)
            self.assertEqual({'currentness':'INVALID', 'reason_codes':[
                'REF_HASH_MISMATCH' if corrupt else 'REF_MISSING']},
                check_si_currentness(g.records, n['K3'], active, []))

    def test_G01_incompatible_new_angle_cannot_rebase_frozen_E1(self):
        g, n, active = creative_graph('changed_angle')
        # Both old and new angles/ideas active: dependency presence alone is not
        # enough to hide incompatibility with exact frozen E1's evaluated angle.
        self.assert_state(g, n['K3'], active + [n['Qa']], [], 'STALE', ['INPUT_STALE'])
        self.assertEqual(n['Angle'], g.refs[key(n['E1'])]['payload']['angle_ref'])
        self.assertEqual(n['NewAngle'], g.refs[key(n['K3'])]['payload']['angle_ref'])

    def test_G01_original_evaluation_missing_active_or_replaced_stale(self):
        g, n, active = creative_graph('text_only'); active += [n['Qa']]
        active.remove(n['E1'])
        self.assert_state(g, n['K3'], active, [], 'STALE', ['INPUT_STALE'])
        # New genuine evaluation identity, never an implicit replacement for E1.
        value = cp(g.refs[key(n['E1'])]); other = g.add(value, data_refs(value))
        self.assert_state(g, n['K3'], active + [other], [], 'STALE', ['INPUT_STALE'])

    def test_unrelated_selection_heads_never_stale_evaluation_or_creative(self):
        g, n, active, heads = brief_graph()
        new = add_selection(g, n, n['K3'], previous=heads[0])
        for root in (n['E1'], n['K3']):
            for observed in ([], heads, [new]):
                self.assert_state(g, root, active, observed, 'CURRENT')

    def test_G01_brief_used_selection_head_exact_and_withdraw_own_head(self):
        g, n, active, heads = brief_graph()
        self.assert_state(g, n['B1'], active, heads, 'CURRENT')
        new = add_selection(g, n, n['K3'], previous=heads[0])
        self.assert_state(g, n['B1'], active, [new], 'STALE', ['INPUT_STALE'])
        self.assert_state(g, n['B1'], active, [], 'STALE', ['INPUT_STALE'])
        withdraw = fixtures()['Selection']; withdraw['payload'].update(
            scope={'purpose':'BRIEF_REVIEW', 'idea_ref':n['Idea'],
                   'audience_ref':n['Audience'], 'channel_ref':n['Channel']},
            target_ref=n['B1'], choice='WITHDRAW')
        other = g.add(withdraw, data_refs(withdraw))
        self.assert_state(g, n['B1'], active, heads + [other], 'CURRENT')

    def test_G01_G02_relevant_eref_invalid_not_stale_or_trusted_digest(self):
        g, n, active = creative_graph(external=True)
        # Resolver/provenance certify SI bytes only, not editorial material.
        for root in (n['E1'], n['K3']):
            self.assert_state(g, root, active + [n['Qa']], [], 'INVALID', ['REF_MISSING'])

    def test_all_required_evaluation_inputs_removed_or_revised_stale(self):
        for field in ('Idea', 'Angle', 'Rubric', 'S', 'Check'):
            g, n, active = creative_graph(bindings=True); active += [n['Qa']]
            original = n[field]; active.remove(original)
            self.assert_state(g, n['E1'], active, [], 'STALE', ['INPUT_STALE'])
            changed = revise(g, original)
            self.assertNotEqual(original['sha256'], changed['sha256'])
            self.assert_state(g, n['E1'], active + [changed], [], 'STALE', ['INPUT_STALE'])

    def test_evaluation_missing_historical_ref_and_corruption_invalid(self):
        for corrupt in (False, True):
            g, n, active = creative_graph(bindings=True)
            old = g.refs[key(n['S'])]
            if corrupt: old['payload']['title'] = known('Tampered')
            else: g.records.remove(old)
            self.assertEqual({'currentness':'INVALID', 'reason_codes':[
                'REF_HASH_MISMATCH' if corrupt else 'REF_MISSING']},
                check_si_currentness(g.records, n['E1'], active, []))

    def test_audit_context_is_not_required_current_input(self):
        g, n, active = creative_graph('text_only', audit_only=True)
        self.assertNotIn(n['AuditOnlySource'], active)
        self.assertIn(n['AuditOnlySource'], g.closure([n['C']]))
        self.assert_state(g, n['K3'], active + [n['Qa']], [], 'CURRENT')

    def test_all_fourteen_revisable_types_keep_history_out_of_current_set(self):
        g, n, active = creative_graph('text_only', bindings=True)
        active += [n['Qa']]
        visual = fixtures()['VisualRequirement']; visual['payload']['source_refs'] = [n['S']]
        vr = g.add(visual, data_refs(visual)); active.append(vr)
        brief = fixtures()['ProductionBrief']; brief['payload'].update(
            idea_ref=n['Idea'], audience_ref=n['Audience'], channel_ref=n['Channel'],
            angle_ref=n['Angle'], evaluation_ref=n['E1'], creative_ref=n['K3'],
            source_refs=[n['S']], claim_refs=[n['Qa']], claim_check_refs=[n['Check']],
            visual_refs=[vr], risk_refs=[n['Risk']], profile_ref=None, creative_selection_ref=None)
        br = g.add(brief, data_refs(brief)); active.append(br)
        bases = [n[k] for k in ('I', 'S', 'Qa', 'Evidence', 'Check', 'Audience',
                                'Channel', 'Angle', 'Rubric', 'Risk', 'Idea', 'K3')] + [vr, br]
        for base in bases:
            with self.subTest(kind=base['type']):
                current = revise(g, base)
                observed = [r for r in active if (r['type'], r['id']) != (base['type'], base['id'])] + [current]
                self.assert_state(g, current, observed, [], 'CURRENT')
                self.assertNotIn(base, observed)

    def test_current_payload_source_override_not_obsolete_producer_history(self):
        g, n, active = creative_graph(bindings=True)
        value = fixtures()['SourceItem']; value['payload']['title'] = known('Нове джерело')
        new_source = g.add(value)
        for base, updates, required in (
                (n['Idea'], {'source_refs':known([new_source])}, [n['I'], new_source]),
                (n['Evidence'], {'source_ref':new_source}, [n['Qa'], new_source])):
            current = revise(g, base, **updates)
            self.assert_state(g, current, required + [current], [], 'CURRENT')
            self.assertNotIn(n['S'], required)

    def test_order_detached_results_no_mutation_and_exact_repeated_calls(self):
        g, n, active, heads = brief_graph()
        result = self.assert_state(g, n['B1'], active, heads, 'CURRENT')
        result['reason_codes'].append('TYPE'); result['currentness'] = 'INVALID'
        expected = {'currentness':'CURRENT', 'reason_codes':[]}
        self.assertEqual(expected, check_si_currentness(list(reversed(g.records)), n['B1'], list(reversed(active)), heads))
        self.assertEqual(expected, check_si_currentness(g.records, n['B1'], active, heads))

    def test_plain_list_ref_roles_duplicate_conflicts_exact_paths(self):
        g, n, active, heads = brief_graph()
        cases = [
            (((), n['B1'], active, heads), 'TYPE', '$.records'),
            ((g.records, [n['B1'], n['B1']], active, heads), 'TYPE', '$.root'),
            ((g.records, n['B1'], tuple(active), heads), 'TYPE', '$.observed_active_input_refs'),
            ((g.records, n['B1'], active, iter(heads)), 'TYPE', '$.observed_selection_head_refs'),
            ((g.records, n['B1'], [heads[0]], heads), 'REF_TYPE_MISMATCH', '$.observed_active_input_refs[0].type'),
            ((g.records, n['B1'], [n['C']], heads), 'REF_TYPE_MISMATCH', '$.observed_active_input_refs[0].type'),
            ((g.records, n['B1'], active, [n['Qa']]), 'REF_TYPE_MISMATCH', '$.observed_selection_head_refs[0].type'),
            ((g.records, n['C'], active, heads), 'REF_TYPE_MISMATCH', '$.root.type'),
            ((g.records, n['B1'], [n['Qa'], n['Qa']], heads), 'TYPE', '$.observed_active_input_refs[1]'),
            ((g.records, n['B1'], active, heads + heads), 'SELECTION_CONFLICT', '$.observed_selection_head_refs[1]'),
            ((g.records, n['B1'], [{'type':'SourceItem'}], heads), 'MISSING_FIELD', '$.observed_active_input_refs[0].id'),
        ]
        other = revise(g, n['Qa'])
        cases.append(((g.records, n['B1'], [n['Qa'], other], heads), 'TYPE', '$.observed_active_input_refs[1]'))
        for args, code, path in cases:
            with self.subTest(code=code, path=path):
                with self.assertRaises(SIValidationError) as caught: check_si_currentness(*args)
                self.assertEqual((code, path), (caught.exception.code, caught.exception.path))

    def test_conflicting_declared_scope_heads_invalid(self):
        g, n, active, heads = brief_graph()
        other = add_selection(g, n, n['K3'])  # same exact scope, different chain id
        self.assert_state(g, n['B1'], active, heads + [other], 'INVALID', ['SELECTION_CONFLICT'])

    def test_observed_exact_hash_and_no_latest_missing_revision_invalid(self):
        g, n, active = source_graph()
        for bad, code in (({**n['S3'], 'sha256':'0'*64}, 'REF_HASH_MISMATCH'),
                          ({**n['S3'], 'revision':4}, 'REF_MISSING')):
            self.assertEqual({'currentness':'INVALID', 'reason_codes':[code]},
                check_si_currentness(g.records, n['S3'], [bad], []))

    def test_provenance_and_cycles_invalid_even_when_dependencies_not_active(self):
        from tests import test_story_intelligence_provenance_v1 as p
        records, root, _, _, _, _ = p.RubricRunBindingF1Tests.graph('different_record')
        resolve_si_closure(records, [root])
        self.assertEqual({'currentness':'INVALID', 'reason_codes':['PROVENANCE_MISMATCH']},
                         check_si_currentness(records, root, [], []))
        g = Graph(); value = fixtures()['Intake']
        fake = {'type':'Intake', 'id':value['H']['id'], 'revision':1, 'sha256':'0'*64}
        value['H']['input_refs'] = [fake]
        root = g.add(value, [fake], keep_identity=True)
        self.assertEqual({'currentness':'INVALID', 'reason_codes':['DEPENDENCY_CYCLE']},
                         check_si_currentness(g.records, root, [], []))


if __name__ == '__main__':
    unittest.main()
