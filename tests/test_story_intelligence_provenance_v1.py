"""Independent topological graph rebuilding for supplied provenance claims.

Only stdlib JSON/hashlib construct expected refs. No production resolver/hash
patches; mutated ancestors and every downstream hash/snapshot are rebuilt.
"""
import copy
import unittest

from story_intelligence.provenance_v1 import verify_si_provenance
from story_intelligence.resolver_v1 import resolve_si_closure
from story_intelligence.model_v1 import SIValidationError
from tests.test_story_intelligence_resolver_v1 import Graph, graph_fixture, key, digest, c
from tests.test_story_intelligence_records_v1 import unknown


def data_refs(value):
    """Test-only oracle on these closed fixtures, independent of SI schema walkers.

    The fixture dictionaries with exactly these keys are authored typed refs;
    free-form strings are never parsed, and ERef keys are distinct.
    """
    if type(value) is dict:
        if set(value)=={'type','id','revision','sha256'}:
            return [copy.deepcopy(value)]
        return [ref for child in value.values() for ref in data_refs(child)]
    if type(value) is list:
        return [ref for child in value for ref in data_refs(child)]
    return []


def rewrite(value,mapping):
    if type(value) is dict:
        if set(value)=={'type','id','revision','sha256'}:
            return copy.deepcopy(mapping.get(key(value),value))
        return {field:rewrite(child,mapping) for field,child in value.items()}
    if type(value) is list:return [rewrite(child,mapping) for child in value]
    return value


def provenance_graph(scenario=None):
    old,named=graph_fixture();g=Graph();mapping={};out={};alien=None
    producers={key(v['H']['origin']['run_ref']):v for v in old.records
        if v['H']['origin']['mode']=='HUMAN_EDIT'}
    k1=old.refs[key(named['creative_revision_2'])]['H']['previous']
    original_creative=old.refs[key(k1)]['payload']['run_ref']
    old_brief=old.refs[key(named['packet'])]['payload']['brief_ref']
    methods={'DISCOVERY':'si.discover-local','CREATIVE':'si.creative-templates'}

    def preview(old_record):
        value=rewrite(old_record,mapping);h=value['H'];p=value['payload']
        if h['type']=='CreativeAlternative':
            if scenario=='alien_original_k2' and h['revision']==2:p['run_ref']=copy.deepcopy(alien)
            if scenario=='revision_as_original_k3' and h['revision']==3:
                p['run_ref']=copy.deepcopy(g.refs[key(h['previous'])]['H']['origin']['run_ref'])
            if scenario=='rewritten_genesis' and h['revision']==1:
                h['origin']['run_ref']=copy.deepcopy(alien);p['run_ref']=copy.deepcopy(alien)
        if h['origin']['mode']=='HUMAN_EDIT':
            h['input_refs']=[copy.deepcopy(h['previous'])]+data_refs(p)
            if scenario=='wrong_output_root_order' and h['type']=='CreativeAlternative' and h['revision']==2:
                h['input_refs'][1],h['input_refs'][2]=h['input_refs'][2],h['input_refs'][1]
        return value

    for old_record in old.records:
        old_ref={'type':old_record['H']['type'],'id':old_record['H']['id'],
            'revision':old_record['H']['revision'],'sha256':digest(old_record)}
        value=preview(old_record);h=value['H'];p=value['payload'];kind=h['type']
        if kind=='SourceItem' and h['revision']==1:
            h['origin']={'mode':'USER_IMPORT','run_ref':None,'imported_from':unknown()}
        if kind=='RunRecord':
            if key(old_ref) in producers:
                output=preview(producers[key(old_ref)])
                roots=[output['H']['previous']]+data_refs(output['payload'])
                if output['H']['type']=='CreativeAlternative' and output['H']['revision']==3:
                    if scenario=='wrong_revision_direct_base':
                        previous=g.refs[key(output['H']['previous'])]
                        roots[0]=copy.deepcopy(previous['H']['previous'])
                    elif scenario=='base_only_in_snapshot':
                        p['context_snapshot']['active_input_refs']=[output['H']['previous']]
                        roots=roots[1:]
                    elif scenario=='wrong_revision_root_order':roots=roots[1:]+roots[:1]
                p['semantic_input_refs']=roots
            if scenario=='wrong_stage_'+p['stage']:
                replacement='CREATIVE' if p['stage']=='DISCOVERY' else 'DISCOVERY'
                p['stage']=replacement;p['method_id']=methods[replacement]
            ctx=p['context_snapshot']
            p['input_snapshot']=g.closure(p['semantic_input_refs']+ctx['active_input_refs']+ctx['selection_head_refs'])
            h['input_refs']=copy.deepcopy(p['input_snapshot'])
            p['editorial_snapshot_sha256']=copy.deepcopy(ctx['editorial_snapshot_sha256'])
        if kind=='ProductionBrief' and h['revision']==1:
            roots=data_refs(p)
            assembly=g.run('BRIEF_ASSEMBLY',roots,rubric=p['evaluation_ref'] and
                g.refs[key(p['evaluation_ref'])]['payload']['rubric_ref'])
            if scenario=='wrong_stage_BRIEF_ASSEMBLY':
                run=g.records[-1];old_assembly=copy.deepcopy(assembly)
                run['payload'].update(stage='DISCOVERY',method_id='si.discover-local')
                # This inserted record has no downstream consumers yet.
                del g.refs[key(old_assembly)];deps=g.dependencies.pop(key(old_assembly))
                assembly={**old_assembly,'sha256':digest(run)}
                g.refs[key(assembly)]=run;g.dependencies[key(assembly)]=deps
            h['origin']={'mode':'RULE_DERIVED','run_ref':assembly,'imported_from':None}
            h['input_refs']=roots
        if kind=='CreativeAlternative' and h['revision']==3 and scenario=='reused_revision_run':
            h['origin']['run_ref']=copy.deepcopy(g.refs[key(h['previous'])]['H']['origin']['run_ref'])
        if kind=='ReviewPacket':
            ctx=p['context_snapshot']
            p['source_closure_refs']=g.closure([p['brief_ref']]+ctx['active_input_refs']+ctx['selection_head_refs'])
            p['source_snapshot_digest']=digest({field:p[field] for field in
                ('context_snapshot','source_closure_refs','existing_editorial_refs')})
            p['privacy_grant']['reviewed_snapshot_digest']=p['source_snapshot_digest']
            p['review_state_at_capture']['context_hash']=digest(ctx)
        actual=g.add(value,data_refs(value),keep_identity=True)
        mapping[key(old_ref)]=actual
        if key(old_ref)==key(original_creative):
            # Extra correct-stage CREATIVE Run with real bytes/hash; not a fake ref.
            alien=g.run('CREATIVE',p['semantic_input_refs'])
        if kind=='SourceItem' and h['revision']==1:out['import']=actual
        if kind=='EvaluationReport':out['evaluation']=actual
        if kind=='CreativeAlternative' and h['revision']==1:out['creative_initial']=actual
        if key(old_ref)==key(old_brief):out['assembly']=actual
    for name,ref in named.items():out[name]=mapping[key(ref)]
    out['originating_creative']=mapping[key(original_creative)]
    return g,out


class ProvenanceTests(unittest.TestCase):
    def test_genuine_positive_origins_and_complete_history(self):
        g,named=provenance_graph()
        for name in ('manual','import','discovery_run','evaluation','creative_initial',
                     'assembly','packet','revision','creative_dual_runs'):
            with self.subTest(case=name):
                self.assertEqual(g.closure([named[name]]),verify_si_provenance(g.records,[named[name]]))
        k3=g.refs[key(named['creative_dual_runs'])]
        k2=g.refs[key(k3['H']['previous'])];k1=g.refs[key(k2['H']['previous'])]
        self.assertEqual([1,2,3],[v['H']['revision'] for v in (k1,k2,k3)])
        self.assertEqual(1,len({key(v['payload']['run_ref']) for v in (k1,k2,k3)}))
        self.assertEqual(3,len({key(v['H']['origin']['run_ref']) for v in (k1,k2,k3)}))

    def assert_provenance_only_failure(self,scenario,root_name,field):
        g,named=provenance_graph(scenario);roots=[named[root_name]]
        before=copy.deepcopy((g.records,roots))
        # Must pass accepted exact hashes/DAG/snapshots before new checks reject.
        self.assertEqual(g.closure(roots),resolve_si_closure(g.records,roots))
        with self.assertRaises(SIValidationError) as caught:verify_si_provenance(g.records,roots)
        self.assertEqual('PROVENANCE_MISMATCH',caught.exception.code)
        self.assertIn(field,caught.exception.path)
        self.assertEqual(before,(g.records,roots))

    def test_all_actual_generating_stage_mismatches_with_correct_hashes(self):
        for stage,root in (('DISCOVERY','discovery_run'),('EVALUATION','evaluation'),
            ('CREATIVE','creative_initial'),('BRIEF_ASSEMBLY','assembly'),('PACKET_EXPORT','packet'),
            ('REVISION','revision')):
            with self.subTest(stage=stage):self.assert_provenance_only_failure(
                'wrong_stage_'+stage,root,'.H.origin.run_ref')

    def test_correct_stage_alien_original_k2(self):
        self.assert_provenance_only_failure('alien_original_k2','creative_revision_2','.payload.run_ref')

    def test_k3_carries_k2_revision_run_as_original(self):
        self.assert_provenance_only_failure('revision_as_original_k3','creative_dual_runs','.payload.run_ref')

    def test_rehashed_genesis_rewrite_does_not_launder_descendant_original(self):
        self.assert_provenance_only_failure('rewritten_genesis','creative_revision_2','.payload.run_ref')

    def test_revision_cannot_reuse_ancestral_generating_run(self):
        self.assert_provenance_only_failure('reused_revision_run','creative_dual_runs','.H.origin.run_ref')

    def test_direct_revision_roots_not_snapshot_ancestors(self):
        for scenario in ('wrong_revision_direct_base','base_only_in_snapshot','wrong_revision_root_order'):
            with self.subTest(case=scenario):self.assert_provenance_only_failure(
                scenario,'creative_dual_runs','.payload.semantic_input_refs')

    def test_human_output_direct_root_schema_order(self):
        self.assert_provenance_only_failure('wrong_output_root_order','creative_revision_2','.H.input_refs')

    def test_missing_previous_and_missing_generating_run_propagate(self):
        for field in ('previous','run_ref'):
            g,named=provenance_graph();root=named['creative_dual_runs'];record=g.refs[key(root)]
            missing=record['H']['previous'] if field=='previous' else record['H']['origin']['run_ref']
            records=[v for v in g.records if (v['H']['type'],v['H']['id'],v['H']['revision'])!=tuple(missing[k] for k in ('type','id','revision'))]
            with self.assertRaises(SIValidationError) as caught:verify_si_provenance(records,[root])
            self.assertEqual('REF_MISSING',caught.exception.code)

    def test_exact_previous_hash_not_synthesized_or_repaired(self):
        g,named=provenance_graph();root=named['creative_dual_runs'];records=copy.deepcopy(g.records)
        previous=g.refs[key(root)]['H']['previous']
        next(v for v in records if (v['H']['type'],v['H']['id'],v['H']['revision'])==tuple(previous[k] for k in ('type','id','revision')))['payload']['hook_text']='Changed ancestor bytes'
        with self.assertRaises(SIValidationError) as caught:verify_si_provenance(records,[root])
        self.assertEqual('REF_HASH_MISMATCH',caught.exception.code)

    def test_no_mutation_detached_manifest_and_order(self):
        g,named=provenance_graph();roots=[named['packet'],named['revision']]
        before=copy.deepcopy((g.records,roots));result=verify_si_provenance(g.records,roots)
        self.assertEqual(g.closure(roots),result)
        result[0]['sha256']='0'*64
        self.assertEqual(before,(g.records,roots))
        self.assertEqual(g.closure(roots),verify_si_provenance(list(reversed(g.records)),roots))

    def test_invalid_roots_bundles_are_resolver_errors(self):
        for records,roots in ((None,[]),([],{}),([],[{'kind':'source'}])):
            with self.assertRaises(SIValidationError):verify_si_provenance(records,roots)
        self.assertEqual([],verify_si_provenance([],[]))

    def test_unreachable_provenance_not_certified(self):
        g,named=provenance_graph('wrong_stage_CREATIVE')
        self.assertEqual([named['manual']],verify_si_provenance(g.records,[named['manual']]))


class RubricRunBindingF1Tests(unittest.TestCase):
    @staticmethod
    def graph(mode):
        g,named=provenance_graph()
        original_ref=named['evaluation']
        report=copy.deepcopy(g.refs[key(original_ref)])
        run=g.refs[key(report['payload']['run_ref'])]
        rubric_a=run['payload']['rubric_ref']
        original_manifest=g.closure([original_ref])
        members={key(ref) for ref in original_manifest}
        records=[copy.deepcopy(v) for v in g.records if (
            v['H']['type'],v['H']['id'],v['H']['revision'],digest(v)) in members]
        report_i=next(i for i,v in enumerate(records) if (
            v['H']['type'],v['H']['id'],v['H']['revision'])==tuple(original_ref[k] for k in ('type','id','revision')))
        extra=[]
        if mode!='matching':
            rubric_b=copy.deepcopy(g.refs[key(rubric_a)])
            if mode=='different_record':
                rubric_b['H']['id']='bbbbbbbb-4444-4444-8444-444444444444'
            else:
                revision_run=g.run('REVISION',[rubric_a])
                records.append(copy.deepcopy(g.refs[key(revision_run)]));extra.append(revision_run)
                rubric_b['H'].update(revision=2,previous=copy.deepcopy(rubric_a),
                    input_refs=[copy.deepcopy(rubric_a)],origin={
                        'mode':'HUMAN_EDIT','run_ref':revision_run,'imported_from':None})
                rubric_b['payload']['criteria'][0]['description']='Новая редакция описания критерия'
            h=rubric_b['H']
            ref_b={'type':h['type'],'id':h['id'],'revision':h['revision'],'sha256':digest(rubric_b)}
            records.append(rubric_b);extra.append(ref_b)
            report['payload']['rubric_ref']=ref_b
        else:ref_b=copy.deepcopy(rubric_a)
        root={**original_ref,'sha256':digest(report)}
        records[report_i]=report
        expected=sorted([ref for ref in original_manifest if key(ref)!=key(original_ref)]+[root]+extra,key=key)
        return records,root,expected,rubric_a,ref_b,report_i

    def test_F1_matching_exact_report_run_rubric_accepted_detached(self):
        records,root,expected,a,b,_=self.graph('matching')
        before=copy.deepcopy((records,root))
        self.assertEqual(a,b)
        self.assertEqual(expected,resolve_si_closure(records,[root]))
        result=verify_si_provenance(records,[root])
        self.assertEqual(expected,result)
        result[0]['sha256']='0'*64
        self.assertEqual(before,(records,root))
        self.assertEqual(expected,verify_si_provenance(records,[root]))

    def assert_binding_rejected(self,mode):
        records,root,expected,a,b,report_i=self.graph(mode)
        before=copy.deepcopy((records,root))
        self.assertNotEqual(a,b)
        self.assertEqual(expected,resolve_si_closure(records,[root]))
        with self.assertRaises(SIValidationError) as caught:
            verify_si_provenance(records,[root])
        self.assertEqual('PROVENANCE_MISMATCH',caught.exception.code)
        self.assertEqual(f'$.records[{report_i}].payload.rubric_ref',caught.exception.path)
        self.assertEqual(before,(records,root))
        return a,b

    def test_F1_distinct_real_rubric_rejected_after_resolver_success(self):
        a,b=self.assert_binding_rejected('different_record')
        self.assertNotEqual(a['id'],b['id'])

    def test_F1_same_rubric_new_revision_rejected_after_resolver_success(self):
        a,b=self.assert_binding_rejected('different_revision')
        self.assertEqual(a['id'],b['id'])
        self.assertEqual((1,2),(a['revision'],b['revision']))
        self.assertNotEqual(a['sha256'],b['sha256'])


if __name__=='__main__':unittest.main()
