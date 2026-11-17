"""Executable P01-P42 over real evaluator outputs; no mocked success paths."""
from copy import deepcopy as cp
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
import json
import unittest
from unittest.mock import patch

from story_intelligence.evaluate_v1 import evaluate_si
from story_intelligence import decision_projection_v1 as projection
from story_intelligence.codec_v1 import canonical_si_json
from story_intelligence.provenance_v1 import verify_si_provenance
from tests.story_intelligence_evaluate_fixture_support import Fixture, known, un, key, RANGE, WIDE
from tests.test_story_intelligence_decision_projection_oracles_v1 import (
    EXPECTED, ACTIONS, LIMITS, LABELS, SUMMARIES, INVALID_TEXT, UNAVAILABLE_TEXT,
    family_fixture, w01, multi_finding, W01_CARDS, check_general)


BASE_LINE=('Основание — условия, зафиксированные оценкой переданных данных.',
           'Підстава — умови, зафіксовані оцінкою переданих даних.')
ABSENCE=('В этой оценке не осталось отмеченных условий, препятствующих творческой разработке.',
         'У цій оцінці не залишилося зазначених умов, що перешкоджають творчій розробці.')
CONTINUE=('Редактору следует решить, продолжать ли творческую разработку.',
          'Редактору слід вирішити, чи продовжувати творчу розробку.')


def baseline_card(locale, score=1000):
    i=0 if locale=='ru' else 1
    line=f'Баллы по заданной рубрике: {score} из 1000.' if i==0 else f'Бали за заданою рубрикою: {score} із 1000.'
    return dict(projection_version='editorial-decision-projection/1',display_locale=locale,availability='DISPLAYABLE',
                sections=dict(decision_summary=SUMMARIES['ELIGIBLE_FOR_CREATIVE'][i],
                    reasons=[BASE_LINE[i],line,ABSENCE[i]],blocking_risks_and_gaps=[],next_actions=[CONTINUE[i]],
                    limitations=[value[i] for value in LIMITS]))


def stale_args():
    f=Fixture();a=f.arguments();f.revise('S',title=known('Changed source revision'))
    a.update(records=cp(f.g.records),observed_context=f.context());return a


def selected_fixture():
    from tests.test_story_intelligence_records_v1 import fixtures
    from tests.test_story_intelligence_provenance_v1 import data_refs
    f=Fixture();run=f.g.run('CREATIVE',[f.n['A']]);p=cp(fixtures()['CreativeAlternative']['payload'])
    p.update(angle_ref=f.n['A'],run_ref=run,hook_claim_refs=[])
    for chapter in p['chapters']:chapter['claim_refs']=[]
    creative=f.put('K','CreativeAlternative',_run=run,_inputs=[f.n['A']],**p)
    value=cp(fixtures()['Selection']);value['payload'].update(scope=dict(purpose='CREATIVE_CHOICE',
        idea_ref=f.n['I'],audience_ref=f.n['AU'],channel_ref=f.n['H']),target_ref=creative)
    selection=f.g.add(value,data_refs(value));f.heads=[selection]
    return f,selection


def invalid_case(code):
    f=Fixture();a=f.arguments()
    if code=='TYPE':a['records']=False
    elif code=='LIMIT':a['ratings'][0]['explanation']='x'*100001
    elif code=='UNKNOWN_FIELD':a['required_current_premise']['PRIVATE.KEY_731']=0.5
    elif code=='MISSING_FIELD':del a['human_findings']['binding']
    elif code=='VERSION_UNSUPPORTED':a['human_findings']['contract_tag']='unsupported'
    elif code=='REF_MISSING':a['records']=[r for r in a['records'] if r['H']['id']!=f.n['S']['id']]
    elif code=='REF_TYPE_MISMATCH':a['semantic_input_refs'][0]['type']='SourceItem'
    elif code=='REF_HASH_MISMATCH':a['semantic_input_refs'][0]['sha256']='0'*64
    elif code=='DEPENDENCY_CYCLE':
        run=a['records'][2];run['payload']['input_snapshot'].append(cp(f.n['RD']))
        run['payload']['input_snapshot'].sort(key=key);run['H']['input_refs']=cp(run['payload']['input_snapshot'])
    elif code=='PROVENANCE_MISMATCH':a=Fixture(bad_discovery_stage=True).arguments()
    elif code=='LOCALE_MISMATCH':a['ui_locale']='uk'
    elif code=='SELECTION_CONFLICT':
        f,s=selected_fixture();a=f.arguments();a['observed_context']['selection_head_refs']=[s,s]
    elif code=='EVIDENCE_NEEDED':
        f=Fixture(claim_states=['supported']);a=f.arguments()
        next(r for r in a['records'] if r['H']['id']==f.n['Check0']['id'])['payload']['evidence_refs']=un()
    elif code=='RIGHTS_BLOCKED':a=Fixture(visual={'rights_state':'DOCUMENTED'},risk={'blocking':False}).arguments()
    elif code in ('PRIVACY_REVIEW_REQUIRED','PRIVACY_BLOCKED'):
        from tests.test_story_intelligence_provenance_v1 import provenance_graph
        g,n=provenance_graph();verify_si_provenance(g.records,[n['packet']])
        records=cp(g.records);p=next(r for r in records if r['H']['id']==n['packet']['id'])['payload']
        if code=='PRIVACY_REVIEW_REQUIRED':p['privacy_grant']['confirmed']=False
        else:p['privacy_grant']['allowed_text_fields'][0]['field_path']='PRIVATE.KEY_731'
        a['records']=records
    else:raise AssertionError(code)
    return a


class ProjectionRequirements(unittest.TestCase):
    def render(self,args,locale='ru',result=None):
        result=evaluate_si(**args) if result is None else result
        before=cp((args,result));card=projection.project_evaluation(args,result,locale)
        self.assertEqual((args,result),before)
        check_general(self,args,result,card,locale)
        return result,card

    def unavailable(self,args,result,locale='ru'):
        before_args=cp(args);before_result=result if isinstance(result,BaseException) else cp(result)
        error_args=result.args if isinstance(result,BaseException) else None
        out=projection.project_evaluation(args,result,locale)
        self.assertEqual(args,before_args)
        if isinstance(result,BaseException):
            self.assertIs(result,before_result);self.assertEqual(result.args,error_args)
        else:self.assertEqual(result,before_result)
        i=0 if locale=='ru' else 1
        self.assertEqual(out,dict(projection_version='editorial-decision-projection/1',display_locale=locale,
            availability='UNAVAILABLE',sections=dict(decision_summary=UNAVAILABLE_TEXT[i],reasons=[],
            blocking_risks_and_gaps=[],next_actions=[ACTIONS['A0'][i]],limitations=[x[i] for x in LIMITS])))
        return out

    def test_P01_eligible_literal_card(self):
        a=Fixture().arguments();r=evaluate_si(**a)
        for locale in ('ru','uk'):
            _,c=self.render(a,locale,r);self.assertEqual(c,baseline_card(locale))

    def test_P02_needs_input(self):
        f=Fixture();f.revise('AU',knowledge_level=un());f.revise('H',audience_ref=f.n['AU']);f.revise('A',audience_ref=f.n['AU'])
        r,c=self.render(f.arguments());self.assertEqual(r['eligibility']['state'],'NEEDS_INPUT')
        self.assertEqual(c['sections']['blocking_risks_and_gaps'],['Гипотеза об аудитории 1: '+EXPECTED['Q01'][0]])

    def test_P03_unknown_score(self):
        _,a=family_fixture('F01');r,c=self.render(a)
        self.assertEqual(r['eligibility']['state'],'NEEDS_RESEARCH')
        self.assertEqual(c['sections']['reasons'][1],'Итоговый балл не определён.')
        self.assertIn('Рубрика 1 / Оценка «Интерес аудитории»: '+EXPECTED['F01'][0],c['sections']['reasons'])

    def test_P04_unresolved_portfolio(self):
        _,a=family_fixture('F05');r,c=self.render(a);self.assertEqual(r['eligibility']['state'],'REVIEW_DUPLICATE')
        self.assertEqual(c['sections']['blocking_risks_and_gaps'],['Контекст канала 1 / Сравнение 1: '+EXPECTED['F05'][0]])

    def test_P05_duplicate_is_not_reject(self):
        f=Fixture(portfolio='one');f.duplicate_outcomes[0]='DUPLICATE';a=f.arguments();r,c=self.render(a)
        self.assertEqual(r['eligibility']['state'],'REVIEW_DUPLICATE')
        self.assertEqual(a['human_findings']['duplicate_findings'][0]['outcome'],'DUPLICATE')
        self.assertNotIn('REJECT',str(c))

    def test_P06_blocked_at_max_score(self):
        _,a=family_fixture('K01');r,c=self.render(a)
        self.assertEqual(r['aggregate_tenths'],known(1000));self.assertEqual(c['sections']['decision_summary'],SUMMARIES['BLOCKED'][0])
        self.assertEqual(c['sections']['blocking_risks_and_gaps'],['Риск 1: '+EXPECTED['K01'][0]])

    def test_P07_actual_stale(self):
        a=stale_args();r=evaluate_si(**a);self.assertEqual(r['status'],'STALE')
        for locale in ('ru','uk'):
            _,c=self.render(a,locale,r);self.assertNotIn('1000',str(c));self.assertIsNone(r['eligibility'])

    def test_P08_actual_missing_ref(self):
        a=invalid_case('REF_MISSING');r,c=self.render(a)
        self.assertEqual(r['status'],'INVALID');self.assertEqual(c['sections']['reasons'],[INVALID_TEXT['REF_MISSING'][0]])

    def test_P09_invalid_evidence_is_not_research(self):
        a=invalid_case('EVIDENCE_NEEDED');r,c=self.render(a)
        self.assertEqual(r['status'],'INVALID');self.assertEqual(c['sections']['decision_summary'],SUMMARIES['INVALID'][0])

    def test_P10_invalid_rights_is_not_eligibility(self):
        a=invalid_case('RIGHTS_BLOCKED');r,c=self.render(a)
        self.assertIsNone(r['eligibility']);self.assertEqual(c['sections']['reasons'],[INVALID_TEXT['RIGHTS_BLOCKED'][0]])

    def test_P11_permitted_hypotheses(self):
        f=Fixture(audience_updates=dict(region=un(),age_range=un(),interests=un()),channel_updates=dict(analytics=un()))
        _,c=self.render(f.arguments());self.assertEqual(c,baseline_card('ru'))

    def test_P12_numbers_no_new_threshold(self):
        for values,n in [([0]*9,0),([5]*9,1000),([1,2,3,4,5,0,1,2,3],510)]:
            f=Fixture()
            for v,rating in zip(values,f.ratings):rating['value']=known(v)
            for locale in ('ru','uk'):
                _,c=self.render(f.arguments(),locale);self.assertEqual(c,baseline_card(locale,n))
        f=Fixture();f.ratings[8]['value']=un();_,c=self.render(f.arguments())
        self.assertEqual(c['sections']['reasons'][1],'Итоговый балл не определён.')

    def test_P13_RC_and_existing_C01_C48_projection(self):
        from tests.test_story_intelligence_evaluate_oracles_v1 import RequiredCurrentOracles
        outer=self;calls=[]
        class ProjectedRC(RequiredCurrentOracles):
            def outcome(self,f,state,codes=(),paths=None):
                result=super().outcome(f,state,codes,paths)
                args=f.arguments() if isinstance(f,Fixture) else f
                for locale in ('ru','uk'):outer.render(args,locale,result)
                calls.append(self._testMethodName)
                return result
            def test_C22_pure_detached_repeat(self):
                super().test_C22_pure_detached_repeat()
                f=Fixture();f.require();f.establish();a=f.arguments();r=evaluate_si(**a)
                for locale in ('ru','uk'):
                    first=projection.project_evaluation(a,r,locale)
                    outer.assertEqual(first,projection.project_evaluation(a,r,locale))
                    outer.render(a,locale,r)
                calls.append(self._testMethodName)
        names=[name for name in unittest.defaultTestLoader.getTestCaseNames(RequiredCurrentOracles) if name.startswith('test_C')]
        self.assertEqual(len(names),48)
        for name in names:
            with self.subTest(case=name):getattr(ProjectedRC(name),name)()
        self.assertEqual(len(set(calls)),46)  # C20/C21 are accepted-API boundary-only witnesses.

    def test_P14_full_kind_materiality_review_matrix(self):
        from tests.test_story_intelligence_evaluate_v1 import EvaluateTests
        outer=self;admissions=[]
        class ProjectedClaims(EvaluateTests):
            def accepted(self,f,expected='ELIGIBLE_FOR_CREATIVE',codes=()):
                r=super().accepted(f,expected,codes);a=f.arguments()
                for locale in ('ru','uk'):outer.render(a,locale,r)
                admissions.append(expected);return r
        case=ProjectedClaims('test_q1_kind_materiality_state_matrix');case.test_q1_kind_materiality_state_matrix()
        self.assertEqual(len(admissions),81)
        f=Fixture(claim_states=['supported','disputed']);r,c=self.render(f.arguments())
        self.assertEqual(r['eligibility']['state'],'BLOCKED');self.assertTrue(c['sections']['blocking_risks_and_gaps'])

    def test_P15_risk_variants_no_text_inference(self):
        # All 6x4x2 blocking path variants run in the family/locale matrix.
        for category in ('SCIENTIFIC','LEGAL','ETHICAL','REPUTATIONAL','PRODUCTION','MARKET'):
            f=Fixture(risk=dict(category=category,blocking=False,severity='CRITICAL'))
            _,c=self.render(f.arguments());self.assertEqual(c,baseline_card('ru'))
        f=Fixture(risk={'blocking':True});f.mitigate();_,c=self.render(f.arguments());self.assertEqual(c,baseline_card('ru'))

    def test_P16_C14_full_composition(self):
        f=Fixture(visual={});f.determination='UNDETERMINED';r,c=self.render(f.arguments())
        self.assertEqual(r['eligibility']['reason_codes'],['EVIDENCE_NEEDED','RIGHTS_BLOCKED'])
        self.assertEqual(c['sections']['blocking_risks_and_gaps'],['Риск 1: '+EXPECTED['K02'][0],
            'Материал 1: '+EXPECTED['V01'][0],'Тема 1: '+EXPECTED['RC02'][0]])

    def test_P17_C44_preserves_source2_gap(self):
        f=Fixture(visual={});f.add_source();sources=sorted([f.n['S'],f.n['S2']],key=key)
        f.require(source=sources[0]);f.establish(source=sources[0],review=WIDE,evidence=[f.proof(coverage=WIDE)])
        q=dict(from_utc='2026-11-03T00:00:00Z',to_utc=WIDE['to_utc'])
        f.establish(source=sources[1],review=q,evidence=[f.proof(coverage=q)])
        f.requirements=known([dict(source_ref=s,specification=known('Synthetic data scope'),period=known(cp(RANGE))) for s in sources])
        r,c=self.render(f.arguments());self.assertEqual(r['eligibility']['state'],'BLOCKED')
        self.assertEqual(c['sections']['blocking_risks_and_gaps'],['Риск 1: '+EXPECTED['K02'][0],
            'Материал 1: '+EXPECTED['V01'][0],'Источник 1: '+EXPECTED['RC08'][0]])

    def test_P18_editorial_and_findings_families(self):
        for family in ('Q01','Q02','Q03','Q04','F01','F02','F03','F04','F05'):
            _,a=family_fixture(family)
            for locale in ('ru','uk'):self.render(a,locale)

    def test_P19_nine_confidence_findings_remain_distinct(self):
        a=Fixture(confidence='UNKNOWN').arguments();r,c=self.render(a)
        keys=['angle_novelty','audience_interest','channel_fit','evidence_quality','narrative_potential',
              'portfolio_distinctness','resource_fit','risk_manageability','visual_feasibility']
        self.assertEqual(c['sections']['blocking_risks_and_gaps'],[
            'Рубрика 1 / Оценка «'+LABELS[k][0]+'»: '+EXPECTED['F02'][0] for k in keys])
        self.assertEqual(len(r['diagnostics']),9)

    def test_P20_three_pairs_and_repeated_candidate(self):
        for outcomes,count in [({0:'DISTINCT',1:'DUPLICATE',2:'UNRESOLVED'},2),({0:'DISTINCT',1:'DISTINCT'},1)]:
            f=Fixture(portfolio='one');entries=[cp(f.payload('H')['portfolio']['value'][0]) for _ in range(3)]
            for i,e in enumerate(entries):e['published_title']=f'PRIVATE_TOKEN_731 {i}'
            f.revise('H',portfolio=known(entries));f.duplicate_outcomes=outcomes
            r,c=self.render(f.arguments());self.assertEqual(r['eligibility']['state'],'REVIEW_DUPLICATE')
            self.assertEqual(len(c['sections']['next_actions']),count)
            self.assertIn('Сравнение 3',c['sections']['next_actions'][-1])

    def test_P21_T25_full_literal_as_W01(self):
        a=Fixture(t25=True).arguments();r=evaluate_si(**a)
        for locale in ('ru','uk'):
            _,c=self.render(a,locale,r);self.assertEqual(c,W01_CARDS[locale])

    def test_P22_condition_removal_does_not_clear_others(self):
        for drop in (1,2,3):
            f=Fixture(t25=True)
            if drop==1:f.determination='NOT_REQUIRED'
            elif drop==2:f.ratings[0]['value']=known(5)
            else:f.duplicate_outcomes[0]='DISTINCT'
            for locale in ('ru','uk'):
                r,c=self.render(f.arguments(),locale);expected=cp(W01_CARDS[locale])
                del expected['sections']['reasons'][drop+2]
                del expected['sections']['blocking_risks_and_gaps'][drop]
                del expected['sections']['next_actions'][drop]
                if drop==2:expected['sections']['reasons'][1]=('Баллы по заданной рубрике: 1000 из 1000.' if locale=='ru' else 'Бали за заданою рубрикою: 1000 із 1000.')
                self.assertEqual(c,expected)

    def test_P23_invalid_eref_outranks_stale(self):
        f=Fixture();f.require();f.establish(evidence=[f.proof(material_external=True)]);a=f.arguments()
        f.revise('S',title=known('New source'));a.update(records=cp(f.g.records),observed_context=f.context())
        r,c=self.render(a);self.assertEqual(r['status'],'INVALID');self.assertEqual(r['reason_codes'],['REF_MISSING'])

    def test_P24_historical_only_eref_not_promoted(self):
        f=Fixture(discovery_eref=True);f.revise('S',title=known('S2'));f.revise('S',title=known('S3'))
        f.revise('I',source_refs=known([f.n['S']]));f.revise('A',idea_ref=f.n['I'])
        _,c=self.render(f.arguments());self.assertEqual(c,baseline_card('ru'))

    def test_P25_sixteen_genuine_fatal_code_witnesses(self):
        self.assertEqual(len(INVALID_TEXT),16)
        for code in INVALID_TEXT:
            with self.subTest(code=code):
                a=invalid_case(code);r=evaluate_si(**a)
                self.assertEqual(r['status'],'INVALID',r);self.assertEqual(r['reason_codes'],[code],r)
                for i,locale in enumerate(('ru','uk')):
                    _,c=self.render(a,locale,r);self.assertEqual(c['sections']['reasons'],[INVALID_TEXT[code][i]])

    def test_P26_missing_and_unsupported_values(self):
        a=Fixture().arguments();r=evaluate_si(**a)
        for args,result in [(None,r),({},r),(a,None),(a,RuntimeError('PRIVATE_TOKEN_731'))]:self.unavailable(args,result)
        for keyname in ('records','semantic_input_refs','observed_context','ratings','expected_context','human_findings'):
            partial=cp(a);del partial[keyname];self.unavailable(partial,r)
        f=Fixture();f.omit_premise=True;a=f.arguments();r=evaluate_si(**a);a.pop('required_current_premise')
        actual,card=self.render(a,result=r);self.assertEqual(actual['eligibility']['state'],'NEEDS_INPUT')
        # Unsupported object hooks must not be invoked by copying/validation.
        class Hostile:
            def __deepcopy__(self,memo):raise AssertionError('hook called')
            def __eq__(self,other):raise AssertionError('hook called')
        a=Fixture().arguments();a['records']=Hostile()
        self.assertEqual(projection.project_evaluation(a,r,'ru')['availability'],'UNAVAILABLE')
        class HostileKey:
            calls=0
            def __hash__(self):self.calls+=1;return 1
            def __deepcopy__(self,memo):raise AssertionError('hook called')
        badkey=HostileKey();frame={badkey:'unsupported'};initial=badkey.calls
        self.assertEqual(projection.project_evaluation(frame,r,'ru')['availability'],'UNAVAILABLE')
        self.assertEqual(badkey.calls,initial)
        cycle=[];cycle.append(cycle)
        self.assertEqual(projection.project_evaluation({'records':cycle},r,'ru')['availability'],'UNAVAILABLE')

    def test_P27_locale_no_fallback(self):
        a=Fixture().arguments();r=evaluate_si(**a)
        for locale in (None,'','ua','en','UK',4,True,[]):
            self.assertEqual(projection.project_evaluation(a,r,locale),{'availability':'UNAVAILABLE'})
        self.assertEqual(projection.project_evaluation(),{'availability':'UNAVAILABLE'})

    def test_P28_language_does_not_change_evaluation(self):
        a=Fixture(t25=True).arguments();r=evaluate_si(**a);before=cp((a,r))
        for locale in ('ru','uk'):self.assertEqual(projection.project_evaluation(a,r,locale),W01_CARDS[locale])
        self.assertEqual((a,r),before);self.assertEqual(r['locale'],'ru')

    def test_P29_closed_result_shapes(self):
        a=Fixture().arguments();r=evaluate_si(**a)
        for edit in [lambda v:v.update(status='BLOCKED'),lambda v:v.update(reason_codes=[]),
                     lambda v:v.pop('ratings'),lambda v:v.update(extra='PRIVATE_TOKEN_731'),
                     lambda v:v.update(aggregate_tenths=None)]:
            altered=cp(r);edit(altered);self.unavailable(a,altered)
        a=stale_args();r=evaluate_si(**a);r['eligibility']=dict(state='ELIGIBLE_FOR_CREATIVE',reason_codes=[]);self.unavailable(a,r)

    def test_P30_reverification_detects_each_tamper_and_changed_findings(self):
        a=Fixture(t25=True).arguments();r=evaluate_si(**a)
        edits=[lambda v:v.update(aggregate_tenths=known(1000)),
               lambda v:v['eligibility'].update(state='ELIGIBLE_FOR_CREATIVE'),
               lambda v:v['eligibility'].update(reason_codes=[]),
               lambda v:v['diagnostics'][0].update(code='RIGHTS_BLOCKED'),
               lambda v:v['diagnostics'][0].update(message='PRIVATE_TOKEN_731'),
               lambda v:v['diagnostics'][0].update(input_ref=cp(a['semantic_input_refs'][0])),
               lambda v:v['diagnostics'][0].update(field_path='$.records[999].payload.blocking'),
               lambda v:v['diagnostics'].pop(0),lambda v:v['diagnostics'].reverse()]
        for edit in edits:
            altered=cp(r);edit(altered);self.unavailable(a,altered)
        changed=cp(a);changed['human_findings']['duplicate_findings'][0]['outcome']='DISTINCT';self.unavailable(changed,r)
        with patch.object(projection,'_evaluate',wraps=evaluate_si) as wrapped:
            for _ in range(2):self.assertEqual(projection.project_evaluation(a,r,'ru'),W01_CARDS['ru'])
            self.assertEqual(wrapped.call_count,2)
        # Failure injection only: no mocked successful verification/graph result.
        with patch.object(projection,'_evaluate',side_effect=RuntimeError('PRIVATE_TOKEN_731')):
            output=StringIO()
            with redirect_stdout(output),redirect_stderr(output):self.unavailable(a,r)
            self.assertEqual(output.getvalue(),'')

    def test_P31_unknown_codes_and_verified_flags(self):
        a=Fixture(t25=True).arguments();r=evaluate_si(**a)
        for code in ('CAPABILITY_BLOCKED','HOOK_FACT_CONFLICT','REQUEST_CONFLICT','NEW_CODE'):
            altered=cp(r);altered['diagnostics'][0]['code']=code;self.unavailable(a,altered)
        for keyname in ('verified','trusted','cache','request_id'):
            altered=cp(a);altered[keyname]=True;self.unavailable(altered,r)

    def test_P32_human_reason_private_not_displayed(self):
        f=Fixture(t25=True);a=f.arguments();r,c=self.render(a)
        a['human_findings']['duplicate_findings'][0]['reason']='PRIVATE_TOKEN_731 Name /private/file https://private.invalid 12345678-2222-4222-8222-222222222222'
        output=StringIO()
        with redirect_stdout(output),redirect_stderr(output):newr,newc=self.render(a)
        self.assertEqual(output.getvalue(),'');self.assertEqual(newr,r);self.assertEqual(newc,c)
        self.assertNotIn('private.invalid',str(newc))

    def test_P33_rebuilt_private_metadata_no_leak(self):
        f=Fixture(claim_states=['disputed']);_,before=self.render(f.arguments())
        f.revise('S',title=known('PRIVATE_TOKEN_731'),original_locator='/PRIVATE_TOKEN_731/material')
        f.revise('I',title='PRIVATE_TOKEN_731',source_refs=known([f.n['S']]))
        f.revise('A',idea_ref=f.n['I'])
        f.revise('E',locator=known('PRIVATE_TOKEN_731'),source_ref=f.n['S'])
        f.revise('Check0',reviewer_label='PRIVATE_TOKEN_731',evidence_refs=known([f.n['E']]))
        _,after=self.render(f.arguments());self.assertEqual(before,after)

    def test_P34_private_unknown_key_float(self):
        a=Fixture().arguments();a['required_current_premise']['PRIVATE.KEY_731']=0.5
        r,c=self.render(a);self.assertEqual(r['reason_codes'],['UNKNOWN_FIELD']);self.assertNotIn('PRIVATE',str(c))

    def test_P35_no_diagnostic_html_or_message_echo(self):
        a=Fixture(t25=True).arguments();r=evaluate_si(**a)
        for message in ('PRIVATE_TOKEN_731','<script>bad()</script>','[click](https://private.invalid)'):
            altered=cp(r);altered['diagnostics'][0]['message']=message
            c=self.unavailable(a,altered);self.assertNotIn(message,str(c))

    def test_P36_same_source_identity_two_revisions_not_merged(self):
        f=Fixture();old=f.n['S'];f.revise('S',title=cp(f.payload('S')['title']))
        f.revise('I',source_refs=known([f.n['S']]));f.revise('A',idea_ref=f.n['I'])
        f.extra_roots.append(old);f.main_sources[key(old)]=old;a=f.arguments();a['required_current_premise']['source_freshness']=[]
        r,c=self.render(a);self.assertEqual(r['status'],'OK')
        self.assertEqual(c['sections']['blocking_risks_and_gaps'],['Источник 1: '+EXPECTED['RC06'][0],'Источник 2: '+EXPECTED['RC06'][0]])
        self.assertEqual(old['id'],f.n['S']['id']);self.assertNotEqual(old['revision'],f.n['S']['revision'])

    def test_P37_deterministic_dictionary_order_and_bytes(self):
        def reverse(value):
            if type(value) is dict:return {k:reverse(value[k]) for k in reversed(list(value))}
            if type(value) is list:return [reverse(v) for v in value]
            return value
        _,a=w01();r=evaluate_si(**a)
        for locale in ('ru','uk'):
            first=projection.project_evaluation(a,r,locale);second=projection.project_evaluation(reverse(a),reverse(r),locale)
            self.assertEqual(first,second)
            expected=json.dumps(W01_CARDS[locale],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
            self.assertEqual(canonical_si_json(first),expected)

    def test_P38_exact_unicode_private_reasons(self):
        cards=[];bytes_before=[]
        for reason in ('é','e\u0301'):
            f=Fixture();f.ratings[0]['value']=un(reason);a=f.arguments();bytes_before.append(canonical_si_json(a))
            _,c=self.render(a);cards.append(c)
        self.assertNotEqual(*bytes_before);self.assertEqual(*cards)

    def test_P39_result_detachment(self):
        _,a=w01();r=evaluate_si(**a);before=cp((a,r));first=projection.project_evaluation(a,r,'ru')
        first['sections']['reasons'].clear();first['sections']['next_actions'][0]='mutated';first['sections']['limitations'].clear()
        self.assertEqual(projection.project_evaluation(a,r,'ru'),W01_CARDS['ru']);self.assertEqual((a,r),before)

    def test_P40_long_lists_preserve_every_slot(self):
        f=Fixture(confidence='UNKNOWN')
        for i in range(12):f.add_source('Source'+str(i))
        for i in range(8):
            p=f.risk_payload();p.update(blocking=True,basis_refs=[f.n['A']]);f.put('ExtraRisk'+str(i),'Risk',**p)
        a=f.arguments();a['required_current_premise']['source_freshness']=[]
        for locale in ('ru','uk'):
            r,c=self.render(a,locale);self.assertEqual(r['eligibility']['state'],'BLOCKED')
            self.assertEqual(len(r['diagnostics']),30);self.assertEqual(len(c['sections']['next_actions']),30)
        altered=cp(a);altered['max_items']=3;self.unavailable(altered,evaluate_si(**a))

    def test_P41_recorded_basis_not_real_clearance(self):
        f=Fixture(visual=dict(rights_state='DOCUMENTED',licence_basis=known('PRIVATE_TOKEN_731'),
            material_sha256=Fixture.source_payload()['material_sha256']))
        f.mitigate(visual=True)
        for locale in ('ru','uk'):
            _,c=self.render(f.arguments(),locale);self.assertEqual(c,baseline_card(locale))

    def test_P42_external_approval_not_inferred(self):
        a=Fixture().arguments();r=evaluate_si(**a)
        for external_approvals in ({'present':True},{'present':False}):
            before=cp(external_approvals);_,c=self.render(a,result=r)
            self.assertEqual(external_approvals,before);self.assertEqual(c,baseline_card('ru'))
            self.assertNotIn('согласования отсутствуют',str(c))
        altered=cp(a);altered['external_approvals']={'present':True};self.unavailable(altered,r)


def measure_performance(repeats=3):
    """PD-01 measurements outside pure production code; synthetic cases only."""
    import os
    import platform
    from pathlib import Path
    from statistics import median
    from time import perf_counter
    fixtures=[('B',Fixture().arguments()),('T25',Fixture(t25=True).arguments()),
              ('W01',w01()[1]),('MULTI',multi_finding()[1])]
    environment=dict(python=platform.python_version(),implementation=platform.python_implementation(),
        os=platform.system(),release=platform.release(),machine=platform.machine(),logical_cpus=os.cpu_count())
    cpu=Path('/proc/cpuinfo')
    if cpu.exists():
        environment['cpu_model']=next((line.split(':',1)[1].strip() for line in cpu.read_text().splitlines()
                                      if line.startswith('model name')),'unavailable')
    quota=Path('/sys/fs/cgroup/cpu.max')
    environment['cgroup_cpu_max']=quota.read_text().strip() if quota.exists() else 'unavailable'
    measurements=[]
    for name,args in fixtures:
        expected=evaluate_si(**args)
        evaluate_si(**args)  # One unmeasured warm-up per path.
        warm=projection.project_evaluation(args,expected,'ru');assert warm['availability']=='DISPLAYABLE'
        durations={'evaluator':[],'projection_with_reverification':[]}
        before=cp((args,expected))
        for _ in range(repeats):
            start=perf_counter();actual=evaluate_si(**args);elapsed=perf_counter()-start
            assert actual==expected;durations['evaluator'].append(elapsed)
            start=perf_counter();card=projection.project_evaluation(args,expected,'ru');elapsed=perf_counter()-start
            assert card==warm;durations['projection_with_reverification'].append(elapsed)
        assert (args,expected)==before
        metrics={key:dict(samples_seconds=values,min_seconds=min(values),median_seconds=median(values),
                          max_seconds=max(values)) for key,values in durations.items()}
        measurements.append(dict(case=name,records=len(args['records']),roots=len(args['semantic_input_refs']),
            diagnostics=len(expected['diagnostics']),warmup_each=1,repeats_each=repeats,metrics=metrics))
    return dict(environment=environment,measurements=measurements,
                scope='synthetic Linux CPU-only measurements; not Windows/performance qualification')


if __name__=='__main__':unittest.main()
