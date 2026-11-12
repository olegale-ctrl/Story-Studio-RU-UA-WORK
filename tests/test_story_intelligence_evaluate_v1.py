"""Independent numeric, findings and approved bounded classifier assertions."""
from copy import deepcopy as cp
import unittest

from story_intelligence.evaluate_v1 import evaluate_si
from story_intelligence.codec_v1 import canonical_si_json
from story_intelligence.resolver_v1 import resolve_si_closure
from story_intelligence.provenance_v1 import verify_si_provenance
from tests.story_intelligence_evaluate_fixture_support import Fixture, known, un, digest, key, KEYS


class EvaluateTests(unittest.TestCase):
    def accepted(self, fixture, expected='ELIGIBLE_FOR_CREATIVE', codes=()):
        args = fixture.arguments()
        resolve_si_closure(args['records'], args['semantic_input_refs'])
        verify_si_provenance(args['records'], args['semantic_input_refs'])
        before = canonical_si_json(args)
        result = evaluate_si(**args)
        self.assertEqual(canonical_si_json(args), before)
        self.assertEqual(result['status'], 'OK', result)
        self.assertEqual(result['eligibility'], {'state': expected, 'reason_codes': list(codes)}, result)
        return result

    def invalid(self, args, code, path=None):
        before = canonical_si_json(args)
        result = evaluate_si(**args)
        self.assertEqual(canonical_si_json(args), before)
        self.assertEqual(result['status'], 'INVALID', result)
        self.assertIsNone(result['eligibility'])
        self.assertIsNone(result['aggregate_tenths'])
        self.assertIn(code, result['reason_codes'], result)
        if path is not None:
            self.assertEqual(result['diagnostics'][0]['field_path'], path, result)
        return result

    def test_numeric_literal_oracles(self):
        for values, expected in [([0]*9, 0), ([5]*9, 1000), ([1,2,3,4,5,0,1,2,3], 510)]:
            with self.subTest(values=values):
                f=Fixture()
                for rating, value in zip(f.ratings, values): rating['value']=known(value)
                r=self.accepted(f)
                self.assertEqual(r['aggregate_tenths'], known(expected))
        f=Fixture(); f.ratings[0]['value']=un()
        r=self.accepted(f, 'NEEDS_RESEARCH', ['EVIDENCE_NEEDED'])
        self.assertEqual(r['aggregate_tenths'], un('At least one required rating is unknown.'))

    def test_confidence_findings_T01_T04(self):
        for outcome, expected in [(None,'NEEDS_RESEARCH'),('SUFFICIENT','ELIGIBLE_FOR_CREATIVE'),('INSUFFICIENT','NEEDS_RESEARCH')]:
            with self.subTest(outcome=outcome):
                f=Fixture(); f.ratings[0]['confidence']['level']='UNKNOWN'
                if outcome: f.confidence_outcomes[KEYS[0]]=outcome
                r=self.accepted(f, expected, [] if outcome=='SUFFICIENT' else ['EVIDENCE_NEEDED'])
                self.assertEqual(r['aggregate_tenths'], known(1000))
                self.assertEqual(r['ratings'][0]['confidence']['level'], 'UNKNOWN')
        f.ratings[0]['value']=un(); f.confidence_outcomes[KEYS[0]]='SUFFICIENT'
        self.accepted(f, 'NEEDS_RESEARCH', ['EVIDENCE_NEEDED'])

    def test_duplicate_confidence_T05_T06(self):
        for outcome in ['SUFFICIENT','INSUFFICIENT']:
            with self.subTest(outcome=outcome):
                f=Fixture(confidence='UNKNOWN'); f.confidence_outcomes[KEYS[0]]='SUFFICIENT'
                a=f.arguments(); item=cp(a['human_findings']['confidence_findings'][0]); item['outcome']=outcome
                a['human_findings']['confidence_findings'].append(item)
                self.invalid(a,'TYPE','$.human_findings.confidence_findings[1]')

    def test_exact_digests_T07_T36(self):
        for field in ['binding_sha256','rating_sha256']:
            f=Fixture(confidence='UNKNOWN'); f.confidence_outcomes[KEYS[0]]='SUFFICIENT'
            a=f.arguments(); a['human_findings']['confidence_findings'][0][field]='0'*64
            self.invalid(a,'REF_HASH_MISMATCH')
        for field in ['explanation','basis_refs','confidence']:
            f=Fixture(confidence='UNKNOWN'); a=f.arguments()
            if field=='explanation': a['ratings'][0][field]='e\u0301'
            elif field=='basis_refs': a['ratings'][0][field]=[f.n['AU']]
            else: a['ratings'][0][field]['basis']='Changed human basis'
            self.invalid(a,'REF_HASH_MISMATCH')

    def test_portfolio_T10_T13_T16_T22(self):
        for outcome, expected in [(None,'REVIEW_DUPLICATE'),('DISTINCT','ELIGIBLE_FOR_CREATIVE'),('DUPLICATE','REVIEW_DUPLICATE'),('UNRESOLVED','REVIEW_DUPLICATE')]:
            with self.subTest(outcome=outcome):
                f=Fixture(portfolio='one'); f.duplicate_outcomes={} if outcome is None else {0:outcome}
                self.accepted(f,expected,[] if outcome=='DISTINCT' else ['DUPLICATE_REVIEW_NEEDED'])
        self.accepted(Fixture())
        self.accepted(Fixture(portfolio='unknown'),'NEEDS_RESEARCH',['EVIDENCE_NEEDED'])

    def test_portfolio_three_entries_T14_T15_T21(self):
        for outcomes, count, state in [({0:'DISTINCT',1:'DUPLICATE',2:'UNRESOLVED'},2,'REVIEW_DUPLICATE'),
                                      ({0:'DISTINCT',1:'DISTINCT'},1,'REVIEW_DUPLICATE'),
                                      ({0:'DISTINCT',1:'DISTINCT',2:'DISTINCT'},0,'ELIGIBLE_FOR_CREATIVE')]:
            f=Fixture(portfolio='one'); entries=[cp(f.payload('H')['portfolio']['value'][0]) for _ in range(3)]
            for i,e in enumerate(entries): e['published_title']=f'Entry {i}'
            f.revise('H',portfolio=known(entries)); f.duplicate_outcomes=outcomes
            r=self.accepted(f,state,[] if count==0 else ['DUPLICATE_REVIEW_NEEDED'])
            self.assertEqual(len(r['diagnostics']),count)

    def test_portfolio_invalid_T18_T20(self):
        for field,value,code in [('portfolio_entry_sha256','0'*64,'REF_HASH_MISMATCH'),
                                 ('candidate_ref',None,'PROVENANCE_MISMATCH'),
                                 ('portfolio_entry_index',True,'TYPE')]:
            f=Fixture(portfolio='one'); a=f.arguments()
            a['human_findings']['duplicate_findings'][0][field]=f.n['I'] if value is None else value
            self.invalid(a,code)
        f=Fixture(portfolio='one'); a=f.arguments()
        a['human_findings']['duplicate_findings']*=2
        self.invalid(a,'TYPE','$.human_findings.duplicate_findings[1]')

    def test_stale_rubric_channel_candidate_T08_T17_T19(self):
        for name,updates in [('G',{'method_version':'1'}),('H',{'purpose':'New purpose'}),('P',{'title':'New title'})]:
            with self.subTest(name=name):
                f=Fixture(portfolio='one'); a=f.arguments(); f.revise(name,**updates)
                a['records']=cp(f.g.records); a['observed_context']=f.context()
                r=evaluate_si(**a)
                self.assertEqual(r['status'],'STALE',r)
                self.assertIsNone(r['eligibility'])

    def test_reject_envelope_tags_unknown_keys_order_T28_T34_T37(self):
        for mutate,code in [
            (lambda a:a['human_findings'].update(request_id='not-approved'),'UNKNOWN_FIELD'),
            (lambda a:a['human_findings'].update(contract_tag='other'),'VERSION_UNSUPPORTED'),
            (lambda a:a['ratings'].reverse(),'TYPE'),
            (lambda a:a['human_findings'].pop('binding'),'MISSING_FIELD')]:
            a=Fixture().arguments(); mutate(a); self.invalid(a,code)
        f=Fixture(confidence='UNKNOWN'); f.confidence_outcomes[KEYS[0]]='SUFFICIENT'
        f.ratings[0]['confidence']['level']='HIGH'; self.invalid(f.arguments(),'TYPE')

    def test_research_preserves_duplicate_diagnostics_T24(self):
        f=Fixture(portfolio='one'); f.ratings[0]['value']=un(); f.duplicate_outcomes[0]='UNRESOLVED'
        r=self.accepted(f,'NEEDS_RESEARCH',['DUPLICATE_REVIEW_NEEDED','EVIDENCE_NEEDED'])
        self.assertEqual([d['code'] for d in r['diagnostics']],['EVIDENCE_NEEDED','DUPLICATE_REVIEW_NEEDED'])
        a=f.arguments(); a['human_findings']['duplicate_findings'][0]['reason']='Changed reason only'
        self.assertEqual(evaluate_si(**a),r)

    def test_missing_hash_type_and_method_T09_T29_T30(self):
        f=Fixture(); a=f.arguments(); a['records']=[r for r in a['records'] if r['H']['id']!=f.n['S']['id']]
        self.invalid(a,'REF_MISSING')
        a=f.arguments(); a['semantic_input_refs'][0]['sha256']='0'*64
        self.invalid(a,'REF_HASH_MISMATCH')
        a=f.arguments(); a['records'][0]['payload']['extra']='not schema'
        self.invalid(a,'UNKNOWN_FIELD')
        f=Fixture(rubric_updates={'method_version':'unsupported'})
        self.invalid(f.arguments(),'VERSION_UNSUPPORTED')
        criteria=cp(Fixture().payload('G')['criteria']); criteria[0]['weight_percent']=10; criteria[1]['weight_percent']=15
        self.invalid(Fixture(rubric_updates={'criteria':criteria}).arguments(),'TYPE')

    def test_q1_kind_materiality_state_matrix(self):
        for kind in ['factual','interpretation','fictional']:
            for materiality in ['CENTRAL','SUPPORTING','CONTEXT']:
                for state in [None,'unreviewed','unverified','supported','qualified','disputed','removed','supported_insufficient','qualified_insufficient']:
                    with self.subTest(kind=kind,materiality=materiality,state=state):
                        actual=state.split('_')[0] if state is not None else None
                        f=Fixture(claim_states=[] if state is None else [actual],claim_kind=kind,materiality=materiality,
                                  relation='insufficient' if state and state.endswith('_insufficient') else 'supports')
                        good=kind=='fictional' or state in ('supported','qualified')
                        central=kind=='factual' and materiality=='CENTRAL'
                        self.accepted(f,'ELIGIBLE_FOR_CREATIVE' if good else 'BLOCKED' if central else 'NEEDS_RESEARCH',
                                      [] if good else ['CENTRAL_CLAIM_UNSUPPORTED'] if central else ['EVIDENCE_NEEDED'])

    def test_q1_no_check_and_independent_conflict(self):
        for states in [[],['supported','disputed'],['qualified','removed']]:
            self.accepted(Fixture(claim_states=states),'BLOCKED',['CENTRAL_CLAIM_UNSUPPORTED'])
        self.accepted(Fixture(claim_states=['supported'],relation='contradicts'),'BLOCKED',['CENTRAL_CLAIM_UNSUPPORTED'])
        f=Fixture(claim_states=['disputed']); f.revise('Check0',**f.check_payload(f.n['Q'],f.n['E'],'supported'))
        self.accepted(f)
        f=Fixture(claim_states=['disputed','disputed']); f.revise('Check0',**f.check_payload(f.n['Q'],f.n['E'],'supported'))
        self.accepted(f,'BLOCKED',['CENTRAL_CLAIM_UNSUPPORTED'])

    def test_q2_six_categories_severity_resolution_matrix(self):
        for category in ['SCIENTIFIC','LEGAL','ETHICAL','REPUTATIONAL','PRODUCTION','MARKET']:
            for severity in ['LOW','MEDIUM','HIGH','CRITICAL']:
                for resolution in ['OPEN','UNRESOLVED','MITIGATED']:
                    with self.subTest(category=category,severity=severity,resolution=resolution):
                        f=Fixture(risk=dict(category=category,severity=severity,resolution=resolution,blocking=True))
                        self.accepted(f,'BLOCKED',['EVIDENCE_NEEDED'])
                        f=Fixture(risk=dict(category=category,severity=severity,resolution=resolution,blocking=False))
                        self.accepted(f)

    def test_q2_genuine_mitigation(self):
        f=Fixture(risk={'blocking':True}); f.mitigate()
        self.accepted(f)

    def test_q2_mitigation_requires_human_revision_and_no_negative_check(self):
        f=Fixture(risk={'blocking':True}); proof=f.mitigate()
        cpayload=cp(f.record(proof['check_ref'])['payload']); cpayload.update(state='disputed',qualification=None)
        f.put('IndependentNegative','ClaimCheck',**cpayload)
        self.accepted(f,'BLOCKED',['EVIDENCE_NEEDED'])
        f=Fixture(risk={'blocking':True}); f.mitigate()
        f.put('R','Risk',**cp(f.payload('R')))
        self.accepted(f,'BLOCKED',['EVIDENCE_NEEDED'])

    def test_q2_documented_does_not_clear_inadequate_material_or_review(self):
        for material in [Fixture.source_payload()['material_sha256'],known('0'*64)]:
            f=Fixture(visual={'rights_state':'DOCUMENTED','licence_basis':known('Recorded scope'),
                              'material_sha256':material},risk={'blocking':False})
            self.accepted(f,'BLOCKED',['RIGHTS_BLOCKED'])
        f=Fixture(visual={'role':'OPTIONAL'})
        self.accepted(f,'BLOCKED',['EVIDENCE_NEEDED'])

    def test_main_current_evidence_preserves_replaced_source_SG2(self):
        f=Fixture(claim_states=['supported']); old=f.n['S']; f.add_source()
        f.revise('I',source_refs=known([f.n['S2']]))
        f.revise('A',idea_ref=f.n['I'])
        self.assertEqual([v['source_ref'] for v in f.arguments()['required_current_premise']['source_freshness']],sorted([old,f.n['S2']],key=key))
        self.accepted(f)

    def test_q2_visual_rights_and_fallback_boundaries(self):
        for role in ['OPTIONAL','LOCAL']:
            f=Fixture(visual={'role':role},risk={'blocking':False})
            self.accepted(f)
        for fallback in [un(),known('Use a hypothetical replacement')]:
            f=Fixture(visual={'fallback':fallback},risk={'blocking':False})
            self.accepted(f,'BLOCKED',['RIGHTS_BLOCKED'])
        f=Fixture(visual={'rights_state':'DOCUMENTED','licence_basis':known('Synthetic recorded scope'),
                          'material_sha256':Fixture.source_payload()['material_sha256']})
        f.mitigate(visual=True); self.accepted(f)

    def test_q3_essential_and_permissible_unknowns(self):
        for field in ['knowledge_level','motivation']:
            self.accepted(Fixture(audience_updates={field:un()}),'NEEDS_INPUT',['EVIDENCE_NEEDED'])
        self.accepted(Fixture(channel_updates={'capability_notes':un()}),'NEEDS_INPUT',['EVIDENCE_NEEDED'])
        for field in ['region','age_range','interests']:
            self.accepted(Fixture(audience_updates={field:un()}))
        self.accepted(Fixture(channel_updates={'analytics':un()}))
        self.accepted(Fixture(idea_updates={'source_refs':un()}))
        self.accepted(Fixture(idea_updates={'source_refs':un()},claim_states=[],claim_kind='factual'),
                      'BLOCKED',['CENTRAL_CLAIM_UNSUPPORTED','EVIDENCE_NEEDED'])

    def test_malformed_contexts_and_nested_private_keys(self):
        a=Fixture().arguments(); a['observed_context']['active_input_refs']*=2
        self.invalid(a,'TYPE')
        a=Fixture().arguments(); a['observed_context']['context_version']=2
        self.invalid(a,'TYPE')
        a=Fixture().arguments(); a['required_current_premise']['required_data']['secret.with.dots']='secret'
        r=self.invalid(a,'UNKNOWN_FIELD','$.required_current_premise.required_data')
        self.assertNotIn('secret',str(r))
        a=Fixture().arguments(); a['required_current_premise']['PRIVATE.KEY']=0.5
        before=cp(a); r=evaluate_si(**a)
        self.assertEqual(a,before)
        self.assertEqual(r['reason_codes'],['UNKNOWN_FIELD'])
        self.assertEqual(r['diagnostics'][0]['field_path'],'$.required_current_premise')
        self.assertNotIn('PRIVATE',str(r))
        a=Fixture().arguments(); a['human_findings']['binding'].pop('angle_ref')
        a['human_findings']['duplicate_findings'].append({'unknown':'bad'})
        self.invalid(a,'MISSING_FIELD','$.human_findings.binding.angle_ref')

    def test_internally_incompatible_binding_is_invalid(self):
        f=Fixture(); a=f.arguments(); a['human_findings']['binding']['idea_ref']=f.n['P']
        self.invalid(a,'PROVENANCE_MISMATCH','$.human_findings.binding')

    def test_q1_old_declared_check_is_stale(self):
        f=Fixture(claim_states=['disputed']); old=f.n['Check0']
        f.revise('Check0',**f.check_payload(f.n['Q'],f.n['E'],'supported'))
        f.extra_roots.append(old)
        r=evaluate_si(**f.arguments()); self.assertEqual(r['status'],'STALE',r)

    def test_genuine_wrong_generator_and_cycle_T30(self):
        f=Fixture(bad_discovery_stage=True); a=f.arguments()
        resolve_si_closure(a['records'],a['semantic_input_refs'])
        self.invalid(a,'PROVENANCE_MISMATCH')
        f=Fixture(); a=f.arguments(); run=a['records'][2]
        selfref=cp(f.n['RD']); run['payload']['input_snapshot'].append(selfref)
        run['payload']['input_snapshot'].sort(key=key); run['H']['input_refs']=cp(run['payload']['input_snapshot'])
        self.invalid(a,'DEPENDENCY_CYCLE')

    def test_unrelated_selection_head_T38(self):
        from tests.test_story_intelligence_records_v1 import fixtures
        from tests.test_story_intelligence_provenance_v1 import data_refs
        f=Fixture(); run=f.g.run('CREATIVE',[f.n['A']])
        payload=cp(fixtures()['CreativeAlternative']['payload'])
        payload.update(angle_ref=f.n['A'],run_ref=run,hook_claim_refs=[])
        for chapter in payload['chapters']: chapter['claim_refs']=[]
        creative=f.put('K','CreativeAlternative',_run=run,_inputs=[f.n['A']],**payload)
        value=cp(fixtures()['Selection'])
        value['payload'].update(scope=dict(purpose='CREATIVE_CHOICE',idea_ref=f.n['I'],
            audience_ref=f.n['AU'],channel_ref=f.n['H']),target_ref=creative)
        first=f.g.add(value,data_refs(value)); f.heads=[first]; a=f.arguments()
        result=evaluate_si(**a); self.assertEqual(result['status'],'OK',result)
        value['H'].update(id=first['id'],revision=2,previous=first)
        value['payload']['choice']='WITHDRAW'
        second=f.g.add(value,data_refs(value),keep_identity=True)
        f.heads=[second]; a.update(records=cp(f.g.records),observed_context=f.context())
        r=evaluate_si(**a); self.assertEqual(r['status'],'STALE',r)
        self.assertEqual(r['reason_codes'],['INPUT_STALE'])

    def test_locales_unicode_and_purity_T26_T35(self):
        for locale in ['ru','uk']:
            f=Fixture(locale=locale); a=f.arguments(); before=canonical_si_json(a)
            first=evaluate_si(**a); second=evaluate_si(**a)
            self.assertEqual(first,second); self.assertEqual(first['locale'],locale)
            first['ratings'][0]['basis_refs'].clear(); first['eligibility']['reason_codes'].append('mutated')
            self.assertEqual(evaluate_si(**a),second); self.assertEqual(canonical_si_json(a),before)
            self.invalid(dict(a,ui_locale='ua'),'LOCALE_MISMATCH')
        for text in ['\u00e9','e\u0301']:
            f=Fixture(); f.ratings[0]['explanation']=text
            a=f.arguments(); self.assertEqual(evaluate_si(**a)['ratings'][0]['explanation'],text)
        self.assertNotEqual(digest('\u00e9'),digest('e\u0301'))

    def test_invalid_outranks_stale_and_producer_erefs(self):
        f=Fixture(discovery_eref=True); a=f.arguments()
        f.revise('S',title=known('New material revision'))
        a['records']=cp(f.g.records); a['observed_context']=f.context()
        self.invalid(a,'REF_MISSING')

    def test_historical_eref_and_source_not_required_current_T31(self):
        f=Fixture(discovery_eref=True)
        f.revise('S',title=known('S2')); f.revise('S',title=known('S3'))
        f.revise('I',source_refs=known([f.n['S']]))
        f.revise('A',idea_ref=f.n['I'])
        self.accepted(f)


if __name__=='__main__': unittest.main()
