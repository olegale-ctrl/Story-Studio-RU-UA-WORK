"""Authored RC C01-C48 and fixed T25 oracles, independent of evaluator internals."""
from copy import deepcopy as cp
import unittest

from story_intelligence.evaluate_v1 import evaluate_si
from story_intelligence.currentness_v1 import check_si_currentness
from story_intelligence.provenance_v1 import verify_si_provenance
from story_intelligence.resolver_v1 import resolve_si_closure
from tests.story_intelligence_evaluate_fixture_support import Fixture, known, un, key, digest, RANGE, WIDE, t25_expected, original_resume_arguments
from tests.test_story_intelligence_currentness_eref_f1 import creative_case
from tests.test_story_intelligence_records_v1 import eref

P='$.required_current_premise'


def period(start, end):
    return {'from_utc':start, 'to_utc':end}


def K(**proof):
    f=Fixture(); f.require(); f.establish(evidence=[f.proof(**proof)])
    return f


class RequiredCurrentOracles(unittest.TestCase):
    def outcome(self, f, state, codes=(), paths=None):
        a=f.arguments() if isinstance(f,Fixture) else f
        before=cp(a); result=evaluate_si(**a)
        self.assertEqual(a,before)
        if state in ('INVALID','STALE'):
            self.assertEqual(result['status'],state,result)
            self.assertIsNone(result['eligibility'])
            self.assertEqual(result['reason_codes'],list(codes),result)
        else:
            self.assertEqual(result['status'],'OK',result)
            self.assertEqual(result['eligibility'],dict(state=state,reason_codes=list(codes)),result)
        if paths is not None:
            self.assertEqual([d['field_path'] for d in result['diagnostics']],paths,result)
        return result

    def research(self,f,paths=None): return self.outcome(f,'NEEDS_RESEARCH',['EVIDENCE_NEEDED'],paths)
    def eligible(self,f): return self.outcome(f,'ELIGIBLE_FOR_CREATIVE',[],[])
    def invalid(self,f,code,path=None): return self.outcome(f,'INVALID',[code],None if path is None else [path])

    def test_T25_complete_literal_four_diagnostics(self):
        f=Fixture(t25=True); self.assertEqual(len(f.g.records),11)
        a=f.arguments()
        # Independently frozen stdlib JSON/SHA-256 bytes; evaluator has no role in
        # these expected hashes. Bind both complete graph and local rating context.
        self.assertEqual(digest(a['records']),'684e05d29daf0900b1e8579cba4afe8367a8261f2effc6bfee4af3cce7900b8f')
        self.assertEqual(digest(a['ratings']),'46b559566d812d98e593aceaf1c118cca51e8fecdd8b6bf855d0f0db7772a6f6')
        self.assertEqual(digest(a['human_findings']['binding']),'7edbcb32f1abcfb3e801eb009ca367f90a3e063ccacc7af317b0723c647b34f8')
        resolve_si_closure(a['records'],a['semantic_input_refs'])
        verify_si_provenance(a['records'],a['semantic_input_refs'])
        r=self.outcome(a,'BLOCKED',['DUPLICATE_REVIEW_NEEDED','EVIDENCE_NEEDED'])
        self.assertEqual(r['diagnostics'],t25_expected(f))
        self.assertEqual(r['aggregate_tenths'],un('At least one required rating is unknown.'))

    def test_T25_bounded_regressions(self):
        f=Fixture(t25=True); f.include_risk=False
        f.active.pop(('Risk',f.n['R']['id']))
        r=self.outcome(f,'NEEDS_INPUT',['DUPLICATE_REVIEW_NEEDED','EVIDENCE_NEEDED'])
        self.assertEqual(r['diagnostics'],t25_expected(f)[1:])
        f=Fixture(t25=True); f.determination='NOT_REQUIRED'
        r=self.outcome(f,'BLOCKED',['DUPLICATE_REVIEW_NEEDED','EVIDENCE_NEEDED'])
        expected=t25_expected(f); del expected[1]; self.assertEqual(r['diagnostics'],expected)
        f=Fixture(t25=True); f.ratings[0]['value']=known(5)
        r=self.outcome(f,'BLOCKED',['DUPLICATE_REVIEW_NEEDED','EVIDENCE_NEEDED'])
        self.assertEqual(r['aggregate_tenths'],known(1000))
        expected=t25_expected(f); del expected[2]; self.assertEqual(r['diagnostics'],expected)
        f=Fixture(t25=True); f.duplicate_outcomes[0]='DISTINCT'
        r=self.outcome(f,'BLOCKED',['EVIDENCE_NEEDED']); self.assertEqual(r['diagnostics'],t25_expected(f)[:3])

    def test_C01_undetermined(self):
        f=Fixture(); f.determination='UNDETERMINED'
        r=self.outcome(f,'NEEDS_INPUT',['EVIDENCE_NEEDED'],[P+'.determination'])
        self.assertEqual(r['diagnostics'],[dict(code='EVIDENCE_NEEDED',field_path=P+'.determination',input_ref=f.n['I'],message='Required-current determination is unresolved.')])

    def test_C02_missing_required_specification(self):
        for required in [un(),known([])]:
            f=Fixture(); f.determination='REQUIRED'; f.requirements=required; f.uncertain()
            self.outcome(f,'NEEDS_INPUT',['EVIDENCE_NEEDED'],[P+'.required_data',P+'.source_freshness[0].outcome'])

    def test_C03_period_unknown(self):
        f=K(); f.require(period=un())
        self.outcome(f,'NEEDS_INPUT',['EVIDENCE_NEEDED'],[P+'.required_data.value[0].period'])

    def test_C04_insufficient(self):
        f=Fixture(); f.require(); f.uncertain(); self.research(f,[P+'.source_freshness[0].outcome'])

    def test_C05_supported(self): self.eligible(K())
    def test_C06_not_required(self): self.eligible(Fixture())

    def test_C07_source_metadata_not_premise(self):
        f=Fixture(); f.uncertain(); self.research(f,[P+'.source_freshness[0].outcome'])

    def test_C08_missing_premise(self):
        f=Fixture(); f.omit_premise=True
        self.outcome(f,'NEEDS_INPUT',['EVIDENCE_NEEDED'],[P])

    def test_C09_missing_field(self):
        a=Fixture().arguments(); a['required_current_premise'].pop('required_data')
        self.invalid(a,'MISSING_FIELD',P+'.required_data')

    def test_C10_wrong_source_role(self):
        f=Fixture(); p=f.source_payload(); other=f.put('Unrelated','SourceItem',**p)
        a=f.arguments(); a['required_current_premise']['source_freshness'][0]['source_ref']=other
        self.invalid(a,'PROVENANCE_MISMATCH',P+'.source_freshness[0].source_ref')

    def test_C11_old_source_revision(self):
        f=K(); a=f.arguments(); f.revise('S',title=known('New source revision'))
        a.update(records=cp(f.g.records),observed_context=f.context())
        self.outcome(a,'STALE',['INPUT_STALE'])

    def test_C12_changed_complete_context(self):
        f=K(); a=f.arguments(); f.put('Unrelated','SourceItem',**f.source_payload())
        a.update(records=cp(f.g.records),observed_context=f.context())
        self.outcome(a,'STALE',['INPUT_STALE'],[P+'.binding.context_snapshot'])

    def two_sources(self, visual=False):
        f=Fixture(visual={} if visual else None); f.add_source(); refs=sorted([f.n['S'],f.n['S2']],key=key)
        f.require(source=refs[0]); f.establish(source=refs[0]); f.uncertain(source=refs[1])
        return f,refs

    def test_C13_second_source_gap(self):
        f,_=self.two_sources(); self.research(f,[P+'.source_freshness[1].outcome'])

    def visual_expected(self,f,tail):
        return [dict(code='EVIDENCE_NEEDED',field_path='$.records[9].payload.blocking',input_ref=f.n['R'],message='An explicit legal risk remains blocking.'),
                dict(code='RIGHTS_BLOCKED',field_path='$.records[8].payload.rights_state',input_ref=f.n['V'],message='Essential material rights are unresolved.')] + tail

    def test_C14_exact_composed_legal_and_rights(self):
        f=Fixture(visual={}); f.determination='UNDETERMINED'
        r=self.outcome(f,'BLOCKED',['EVIDENCE_NEEDED','RIGHTS_BLOCKED'])
        self.assertEqual(r['diagnostics'],self.visual_expected(f,[dict(code='EVIDENCE_NEEDED',field_path=P+'.determination',input_ref=f.n['I'],message='Required-current determination is unresolved.')]))

    def test_C15_input_gap_and_research(self):
        f,refs=self.two_sources(); f.require(source=refs[0],period=un())
        self.outcome(f,'NEEDS_INPUT',['EVIDENCE_NEEDED'],[P+'.required_data.value[0].period',P+'.source_freshness[1].outcome'])

    def test_C16_undetermined_missing_source_review(self):
        a=original_resume_arguments()
        self.assertEqual(digest(a['records']),'d0629b82eeb589253199ac0dcd9a8ee71bf76a942780dde5fd45bd41c46a8b61')
        self.assertEqual(digest(a['ratings']),'3a3e6fe51ce5715364ba7d7fe83c612749a2528ce44f472c8802e796cec987fd')
        self.assertEqual(digest(a['human_findings']),'cff2c041ed8a348e52727ea47a26c088aa8aae1b56184fed06ddbe6b304d7eeb')
        self.assertEqual(digest(a['expected_context']),'89c43e0d9c54cb16d749c5acc19f133549c1512fe4effa5de65a335da8a67e5b')
        self.outcome(a,'NEEDS_INPUT',['EVIDENCE_NEEDED'],[P+'.determination',P+'.source_freshness'])

    def test_C17_none_no_fabricated_source_diagnostics(self):
        a=original_resume_arguments(); a['required_current_premise']=None
        r=self.outcome(a,'NEEDS_INPUT',['EVIDENCE_NEEDED'],[P]); self.assertIsNone(r['diagnostics'][0]['input_ref'])

    def test_C18_history_sources_excluded(self):
        f=Fixture(); old=f.n['S']; f.revise('S',title=known('S2')); f.revise('S',title=known('S3'))
        f.revise('I',source_refs=known([f.n['S']])); f.revise('A',idea_ref=f.n['I'])
        a=f.arguments(); self.assertNotEqual(old,a['required_current_premise']['source_freshness'][0]['source_ref'])
        self.eligible(a)

    def test_C19_current_revision_producer_eref(self):
        # Rebuild all descendants with genuine exact hashes after adding producer ERef.
        from tests.test_story_intelligence_provenance_v1 import rewrite,data_refs
        from tests.test_story_intelligence_resolver_v1 import Graph
        f=Fixture(); f.revise('I',summary='Edited current premise'); f.revise('A',idea_ref=f.n['I'])
        target=f.record(f.n['I'])['H']['origin']['run_ref']; a=f.arguments(); g=Graph(); mapping={}
        for old in a['records']:
            h=old['H']; prior=dict(type=h['type'],id=h['id'],revision=h['revision'],sha256=digest(old))
            value=rewrite(old,mapping)
            if prior==target: value['H']['editorial_refs']=[eref('source')]
            mapping[key(prior)]=g.add(value,data_refs(value),keep_identity=True)
        # Recreate local bindings with rebuilt graph rather than stale digests.
        f.g=g; f.n={n:mapping[key(r)] for n,r in f.n.items()}
        f.active={ident:mapping[key(r)] for ident,r in f.active.items()}
        f.main_sources={key(mapping[key(r)]):mapping[key(r)] for r in f.main_sources.values()}
        self.invalid(f.arguments(),'REF_MISSING')

    def test_C20_original_creative_eref_boundary(self):
        for location in ['original','current','historical']:
            with self.subTest(location=location):
                g,root,active,heads,_=creative_case(location=location)
                resolve_si_closure(g.records,[root]); verify_si_provenance(g.records,[root])
                r=check_si_currentness(g.records,root,active,heads)
                self.assertEqual(r['currentness'],'CURRENT' if location=='historical' else 'INVALID')
                self.assertEqual(r['reason_codes'],[] if location=='historical' else ['REF_MISSING'])

    def test_C21_original_creative_direct_claim_boundary(self):
        g,root,active,heads,n=creative_case(False)
        active=[r for r in active if r!=n['Qa']]
        r=check_si_currentness(g.records,root,active,heads)
        self.assertEqual(r['currentness'],'STALE'); self.assertEqual(r['reason_codes'],['INPUT_STALE'])

    def test_C22_pure_detached_repeat(self):
        a=K().arguments(); before=cp(a); r=evaluate_si(**a); s=evaluate_si(**a)
        self.assertEqual(r,s); r['diagnostics'].append({'mutated':True}); r['ratings'].clear()
        self.assertEqual(evaluate_si(**a),s); self.assertEqual(a,before)

    def test_C23_unknown_source_freshness_is_not_required(self): self.eligible(Fixture())

    def test_C24_no_evidence(self):
        f=Fixture(); f.require(); f.establish(evidence=[]); self.research(f,[P+'.source_freshness[0].outcome'])

    def test_C25_material_hash_mismatch(self):
        a=K().arguments(); a['required_current_premise']['source_freshness'][0]['evidence'][0]['material_sha256']='0'*64
        self.invalid(a,'REF_HASH_MISMATCH',P+'.source_freshness[0].evidence[0].material_sha256')

    def test_C26_inadequate_proof_states(self):
        for options in [dict(state='unreviewed'),dict(relation='insufficient'),dict(locator=un()),dict(material_known=False)]:
            with self.subTest(options=options): self.research(K(**options),[P+'.source_freshness[0].outcome'])

    def test_C27_one_second_short(self):
        self.research(K(coverage=period(RANGE['from_utc'],'2026-11-03T23:59:59Z')),[P+'.source_freshness[0].outcome'])

    def test_C28_reversed_period(self):
        f=K(); f.require(period=known(period('2026-11-04T00:00:01Z',RANGE['to_utc'])))
        self.invalid(f,'TYPE',P+'.required_data.value[0].period.value.to_utc')

    def test_C29_requirements_digest(self):
        a=K().arguments(); a['required_current_premise']['required_data']['value'][0]['period']['value']['to_utc']=WIDE['to_utc']
        self.invalid(a,'REF_HASH_MISMATCH',P+'.source_freshness[0].requirements_sha256')

    def test_C30_duplicate_source(self):
        for outcome in ['ESTABLISHED','UNKNOWN']:
            a=K().arguments(); p=a['required_current_premise']; second=cp(p['source_freshness'][0]); second['outcome']=outcome
            p['source_freshness'].append(second)
            self.invalid(a,'TYPE',P+'.source_freshness[1].source_ref')

    def test_C31_malformed(self):
        for field,value,code,path in [('review_period',None,'TYPE',P+'.source_freshness[0].review_period'),
                                     ('secret-key','private','UNKNOWN_FIELD',P),
                                     ('contract_tag','bad','VERSION_UNSUPPORTED',P+'.contract_tag')]:
            a=K().arguments(); target=a['required_current_premise']
            if field=='review_period': target=target['source_freshness'][0]
            target[field]=value; self.invalid(a,code,path)

    def test_C32_missing_proof_material_normalized_path(self):
        a=K().arguments(); m=a['required_current_premise']['source_freshness'][0]['evidence'][0]['material_ref']
        a['records']=[r for r in a['records'] if (r['H']['type'],r['H']['id'],r['H']['revision'])!=(m['type'],m['id'],m['revision'])]
        r=self.invalid(a,'REF_MISSING',P+'.source_freshness[0].evidence[0].material_ref')
        self.assertEqual(r['diagnostics'][0]['input_ref'],m)

    def test_C33_contradictory_global_combinations(self):
        f=K(); f.determination='UNDETERMINED'; self.invalid(f,'TYPE',P+'.required_data')
        f=Fixture(); f.requirements=un(); self.invalid(f,'TYPE',P+'.required_data')

    def test_C34_invalid_proof_eref_outranks_stale(self):
        f=K(material_external=True); a=f.arguments(); f.revise('S',title=known('Changed'))
        a.update(records=cp(f.g.records),observed_context=f.context())
        r=self.invalid(a,'REF_MISSING')
        self.assertEqual(r['diagnostics'],[dict(code='REF_MISSING',
            field_path=P+'.source_freshness[0].evidence[0].material_ref',
            input_ref=a['required_current_premise']['source_freshness'][0]['evidence'][0]['material_ref'],
            message='Supplied references cannot be validated.')])

    def test_C35_wider_review_and_evidence(self):
        f=Fixture(); f.require(); f.establish(review=WIDE,evidence=[f.proof(coverage=WIDE)]); self.eligible(f)

    def test_C36_partial_overlap(self):
        q=period('2026-11-03T00:00:00Z',WIDE['to_utc']); f=Fixture(); f.require(); f.establish(review=q,evidence=[f.proof(coverage=q)])
        self.research(f,[P+'.source_freshness[0].outcome'])

    def test_C37_disjoint_review(self):
        q=period(WIDE['to_utc'],'2026-11-06T00:00:00Z'); f=Fixture(); f.require(); f.establish(review=q,evidence=[f.proof(coverage=q)])
        self.research(f,[P+'.source_freshness[0].outcome'])

    def test_C38_no_interval_stitching(self):
        f=Fixture(); f.require(); f.establish(evidence=[f.proof(coverage=period(RANGE['from_utc'],'2026-11-02T00:00:00Z')),
                                                     f.proof(coverage=period('2026-11-02T00:00:00Z',RANGE['to_utc']))])
        self.research(f,[P+'.source_freshness[0].outcome'])

    def test_C39_review_wider_than_evidence(self):
        f=Fixture(); f.require(); f.establish(review=WIDE); self.research(f,[P+'.source_freshness[0].outcome'])

    def test_C40_any_single_adequate_evidence(self):
        for reverse in [False,True]:
            f=Fixture(); f.require(); proofs=[f.proof(relation='insufficient'),f.proof(coverage=WIDE)]
            f.establish(evidence=list(reversed(proofs)) if reverse else proofs); self.eligible(f)

    def test_C41_inclusive_degenerate_interval(self):
        f=K(); f.require(period=known(period(RANGE['to_utc'],RANGE['to_utc']))); self.eligible(f)

    def test_C42_multiple_distinct_gaps(self):
        f=Fixture(); f.require(period=un()); f.uncertain(); f.assessments[key(f.n['S'])]['review_period']=un()
        self.outcome(f,'NEEDS_INPUT',['EVIDENCE_NEEDED'],[P+'.required_data.value[0].period',P+'.source_freshness[0].outcome',P+'.source_freshness[0].review_period'])

    def test_C43_invalid_UTC(self):
        for value in ['2026-02-30T00:00:00Z','2026-11-01T00:00:00+02:00','2026-11-01T00:00:60Z']:
            f=K(); f.require(period=known(period(value,RANGE['to_utc'])))
            self.invalid(f,'TYPE',P+'.required_data.value[0].period.value.from_utc')

    def test_C44_exact_composed_rights_and_partial_review(self):
        f,refs=self.two_sources(True)
        f.establish(source=refs[0],review=WIDE,evidence=[f.proof(coverage=WIDE)])
        q=period('2026-11-03T00:00:00Z',WIDE['to_utc']); f.establish(source=refs[1],review=q,evidence=[f.proof(coverage=q)])
        # Both Sources are independently required; canonical requirements authored.
        f.requirements=known([dict(source_ref=r,specification=known('Synthetic data scope'),period=known(cp(RANGE))) for r in refs])
        r=self.outcome(f,'BLOCKED',['EVIDENCE_NEEDED','RIGHTS_BLOCKED'])
        self.assertEqual(r['diagnostics'],self.visual_expected(f,[dict(code='EVIDENCE_NEEDED',field_path=P+'.source_freshness[1].outcome',input_ref=refs[1],message='Source freshness evidence is insufficient.')]))

    def test_C45_private_reason_not_reflected(self):
        f=Fixture(); f.determination='UNDETERMINED'; a=f.arguments()
        a['required_current_premise']['source_freshness'][0]['reason']='PRIVATE TOKEN = secret'
        r=self.outcome(a,'NEEDS_INPUT',['EVIDENCE_NEEDED']); self.assertNotIn('PRIVATE',str(r))
        self.assertEqual(r['diagnostics'][0]['message'],'Required-current determination is unresolved.')

    def test_C46_private_key_not_reflected(self):
        a=Fixture().arguments(); a['required_current_premise']['SECRET_CREDENTIAL']='private'
        r=self.invalid(a,'UNKNOWN_FIELD',P); self.assertNotIn('SECRET_CREDENTIAL',str(r))

    def test_C47_missing_assessment_not_fake_outcome(self):
        a=K().arguments(); a['required_current_premise']['source_freshness']=[]
        self.research(a,[P+'.source_freshness'])

    def test_C48_contradictory_not_applicable(self):
        a=Fixture().arguments(); a['required_current_premise']['source_freshness'][0]['outcome']='ESTABLISHED'
        self.invalid(a,'TYPE',P+'.source_freshness[0].outcome')


if __name__=='__main__': unittest.main()
