"""Real content-addressed DAGs; independent explicit-edge fixture oracle.

Fixture bytes/refs use only stdlib JSON/hashlib, not SI production hash/resolver.
Explicit dependency lists are independently authored alongside each new record.
"""
import copy
import hashlib
import json
import unittest
from unittest.mock import patch

from story_intelligence import resolver_v1 as r
from story_intelligence.model_v1 import SIValidationError
from tests.test_story_intelligence_records_v1 import fixtures, known, unknown, eref, AT


def c(value):
    return json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()


def digest(value):return hashlib.sha256(c(value)).hexdigest()
def key(ref):return (ref['type'],ref['id'],ref['revision'],ref['sha256'])


class Graph:
    def __init__(self):
        self.records=[];self.refs={};self.dependencies={};self.serial=0

    def add(self,record,deps=(),keep_identity=False):
        record=copy.deepcopy(record)
        if not keep_identity:
            self.serial+=1
            record['H']['id']=f'{self.serial:08x}-2222-4222-8222-222222222222'
        h=record['H']
        ref={'type':h['type'],'id':h['id'],'revision':h['revision'],'sha256':digest(record)}
        self.records.append(record);self.refs[key(ref)]=record
        self.dependencies[key(ref)]=copy.deepcopy(list(deps))
        return ref

    def closure(self,roots):
        # Independent iterative explicit-edge oracle, not production schema walking.
        found={};pending=list(roots)
        while pending:
            ref=pending.pop();k=key(ref)
            if k in found:continue
            found[k]=ref
            pending.extend(self.dependencies[k])
        return [copy.deepcopy(found[k]) for k in sorted(found)]

    def run(self,stage,roots,context=None,rubric=None):
        value=fixtures()['RunRecord'];p=value['payload']
        ctx=copy.deepcopy(context) if context is not None else {
            'context_version':1,'active_input_refs':[],'selection_head_refs':[],
            'editorial_snapshot_sha256':unknown()}
        inputs=roots+ctx['active_input_refs']+ctx['selection_head_refs']
        snapshot=self.closure(inputs)
        methods={'DISCOVERY':'si.discover-local','EVALUATION':'si.evaluate',
            'CREATIVE':'si.creative-templates','REVISION':'si.human-revision',
            'BRIEF_ASSEMBLY':'si.brief-assembly','PACKET_EXPORT':'si.review-packet'}
        p.update(stage=stage,method_id=methods[stage],semantic_input_refs=copy.deepcopy(roots),
            input_snapshot=snapshot,context_snapshot=ctx,rubric_ref=copy.deepcopy(rubric),
            editorial_snapshot_sha256=copy.deepcopy(ctx['editorial_snapshot_sha256']))
        value['H']['input_refs']=copy.deepcopy(snapshot)
        return self.add(value,snapshot+([rubric] if rubric is not None else []))


def graph_fixture():
    t=fixtures();g=Graph();named={}
    i=g.add(t['Intake']);named['manual']=i
    source=g.add(t['SourceItem'])
    claim=g.add(t['ClaimItem'])
    evidence=copy.deepcopy(t['EvidenceItem']);evidence['payload'].update(claim_ref=claim,source_ref=source)
    evidence_ref=g.add(evidence,[claim,source]);named['multilevel']=evidence_ref
    check=copy.deepcopy(t['ClaimCheck']);check['payload'].update(claim_ref=claim,evidence_refs=known([evidence_ref]))
    check_ref=g.add(check,[claim,evidence_ref])
    discovery=g.run('DISCOVERY',[i,source])
    idea=copy.deepcopy(t['StoryIdea']);idea['H']['origin']['run_ref']=discovery
    idea['H']['input_refs']=[i,source];idea['payload'].update(intake_ref=i,source_refs=known([source]))
    idea_ref=g.add(idea,[discovery,i,source]);named['discovery_run']=idea_ref
    audience=copy.deepcopy(t['AudienceHypothesis']);audience['payload']['basis_refs']=[i]
    audience_ref=g.add(audience,[i])
    channel=copy.deepcopy(t['ChannelContext']);channel['payload'].update(audience_ref=audience_ref,
        portfolio=known([{'story_ref':idea_ref,'published_title':'Синтетична історія',
            'published_locator':unknown(),'published_at':unknown(),'angle_notes':'Не публікація',
            'basis_ref':i}]))
    channel_ref=g.add(channel,[audience_ref,idea_ref,i]);named['known_portfolio']=channel_ref
    angle=copy.deepcopy(t['Angle']);angle['payload'].update(idea_ref=idea_ref,audience_ref=audience_ref,claim_refs=[claim])
    angle_ref=g.add(angle,[idea_ref,audience_ref,claim])
    rubric=g.add(t['Rubric'])
    evaluation_roots=[idea_ref,angle_ref,audience_ref,channel_ref,rubric]
    evaluation_run=g.run('EVALUATION',evaluation_roots,rubric=rubric)
    evaluation=copy.deepcopy(t['EvaluationReport']);p=evaluation['payload']
    p.update(idea_ref=idea_ref,angle_ref=angle_ref,audience_ref=audience_ref,
        channel_ref=channel_ref,rubric_ref=rubric,run_ref=evaluation_run)
    p['ratings'][0]['basis_refs']=[audience_ref]
    evaluation['H']['origin']['run_ref']=evaluation_run
    evaluation['H']['input_refs']=evaluation_roots
    evaluation_ref=g.add(evaluation,[evaluation_run]+evaluation_roots)
    creative_roots=[angle_ref,idea_ref,audience_ref,channel_ref,evaluation_ref]
    creative_run=g.run('CREATIVE',creative_roots)
    creative=copy.deepcopy(t['CreativeAlternative']);creative['payload'].update(angle_ref=angle_ref,run_ref=creative_run,hook_claim_refs=[claim])
    creative['payload']['chapters'][0]['claim_refs']=[claim]
    creative['H']['origin']['run_ref']=creative_run;creative['H']['input_refs']=creative_roots
    k1=g.add(creative,[creative_run,claim]+creative_roots)
    prior=k1
    for revision in (2,3):
        roots=[prior,angle_ref,creative_run]
        run=g.run('REVISION',roots)
        value=copy.deepcopy(g.refs[key(prior)])
        value['H'].update(revision=revision,previous=prior,input_refs=roots,
            origin={'mode':'HUMAN_EDIT','run_ref':run,'imported_from':None})
        value['payload']['hook_text']=f'Ручна редакція {revision}: що невідомо?'
        prior=g.add(value,[run,claim]+roots,keep_identity=True)
        named[f'creative_revision_{revision}']=prior
        if revision==3:named['run_snapshot']=run
    k3=prior;named['creative_dual_runs']=k3
    prior=source
    for revision in (2,3):
        run=g.run('REVISION',[prior])
        value=copy.deepcopy(g.refs[key(prior)]);value['H'].update(revision=revision,previous=prior,
            input_refs=[prior],origin={'mode':'HUMAN_EDIT','run_ref':run,'imported_from':None})
        value['payload']['title']=known(f'Джерело редакції {revision}')
        prior=g.add(value,[prior,run],keep_identity=True)
    named['revision']=prior
    visual=copy.deepcopy(t['VisualRequirement']);visual['payload']['source_refs']=[source]
    visual['payload']['asset_ref']=eref('asset')  # Shape only; never SI resolution.
    visual_ref=g.add(visual,[source])
    risk=copy.deepcopy(t['Risk']);risk['payload']['basis_refs']=[claim]
    risk_ref=g.add(risk,[claim])
    brief=copy.deepcopy(t['ProductionBrief']);p=brief['payload']
    p.update(idea_ref=idea_ref,audience_ref=audience_ref,channel_ref=channel_ref,angle_ref=angle_ref,
        evaluation_ref=evaluation_ref,creative_ref=k3,source_refs=[source],claim_refs=[claim],
        claim_check_refs=[check_ref],visual_refs=[visual_ref],risk_refs=[risk_ref],profile_ref=eref('genre_profile'))
    brief_ref=g.add(brief,[idea_ref,audience_ref,channel_ref,angle_ref,evaluation_ref,k3,source,claim,check_ref,visual_ref,risk_ref])
    selection=copy.deepcopy(t['Selection']);selection['payload']['scope'].update(
        idea_ref=idea_ref,audience_ref=audience_ref,channel_ref=channel_ref)
    selection['payload']['target_ref']=k3
    selection_ref=g.add(selection,[idea_ref,audience_ref,channel_ref,k3])
    ctx={'context_version':1,'active_input_refs':[idea_ref,evaluation_ref,k3,brief_ref],
         'selection_head_refs':[selection_ref],'editorial_snapshot_sha256':unknown()}
    roots=[brief_ref]+ctx['active_input_refs']+ctx['selection_head_refs']
    manifest=g.closure(roots)
    export=g.run('PACKET_EXPORT',roots,ctx,rubric)
    packet=copy.deepcopy(t['ReviewPacket']);p=packet['payload']
    p.update(brief_ref=brief_ref,context_snapshot=ctx,source_closure_refs=manifest,
        existing_editorial_refs=[eref('source')],display_items=[
            {'source_ref':source,'fields':[{'field_path':'original_locator','kind':'REDACTED','text':None}]},
            {'source_ref':idea_ref,'fields':[{'field_path':'title','kind':'TEXT','text':idea['payload']['title']}]}],
        omissions=[{'source_ref':source,'field_path':'original_locator','reason_code':'PRIVATE_FIELD'}])
    snapshot={name:p[name] for name in ('context_snapshot','source_closure_refs','existing_editorial_refs')}
    p['source_snapshot_digest']=digest(snapshot)
    p['privacy_grant']={'reviewed_snapshot_digest':p['source_snapshot_digest'],'confirmed':True,
        'allowed_text_fields':[{'source_ref':idea_ref,'field_path':'title','value_sha256':digest(idea['payload']['title'])}]}
    p['review_state_at_capture'].update(context_hash=digest(ctx),evaluation_ref=evaluation_ref,
        creative_ref=k3,brief_ref=brief_ref,selection_head_refs=[selection_ref])
    packet['H']['origin']['run_ref']=export
    packet['H']['input_refs']=roots
    packet['H']['editorial_refs']=[eref('source')]
    named['packet']=g.add(packet,[export]+manifest)
    return g,named


class ResolverTests(unittest.TestCase):
    def rejected(self,records,roots,code,path_contains=None):
        before=copy.deepcopy((records,roots))
        with self.assertRaises(SIValidationError) as caught:r.resolve_si_closure(records,roots)
        self.assertEqual(code,caught.exception.code)
        if path_contains:self.assertIn(path_contains,caught.exception.path)
        self.assertEqual(before,(records,roots))

    def test_real_graph_cases_and_exact_record(self):
        g,named=graph_fixture()
        for name,root in named.items():
            with self.subTest(case=name):
                self.assertEqual(g.closure([root]),r.resolve_si_closure(g.records,[root]))
                self.assertEqual(g.refs[key(root)],r.resolve_si_record(g.records,root))

    def test_canonical_unique_roots_and_bundle_order(self):
        g,named=graph_fixture();roots=[named['revision'],named['manual'],named['revision']]
        expected=g.closure(roots)
        self.assertEqual(expected,r.resolve_si_closure(list(reversed(g.records)),roots))
        self.assertEqual([],r.resolve_si_closure([],[]))
        self.assertEqual([],r.resolve_si_closure(g.records,[]))

    def test_missing_root_wrong_hash_type_and_no_latest(self):
        g,named=graph_fixture();root=named['manual']
        self.rejected(g.records,[{**root,'id':'ffffffff-2222-4222-8222-222222222222'}],'REF_MISSING','$.roots[0]')
        self.rejected(g.records,[{**root,'sha256':'0'*64}],'REF_HASH_MISMATCH','.sha256')
        self.rejected(g.records,[{**root,'type':'SourceItem'}],'REF_TYPE_MISMATCH','.type')
        # Only revision3 supplied: requested previous revision must never be upgraded.
        source=g.refs[key(named['revision'])]
        self.rejected([source],[source['H']['previous']],'REF_MISSING')

    def test_duplicate_conflicting_and_identical_bundle(self):
        g,named=graph_fixture();record=g.refs[key(named['manual'])]
        self.rejected([record,copy.deepcopy(record)],[named['manual']],'TYPE','$.records[1]')
        changed=copy.deepcopy(record);changed['payload']['raw_input']='Інші bytes'
        for records in ([record,changed],[changed,record]):
            self.rejected(records,[named['manual']],'REF_HASH_MISMATCH','$.records[1]')

    def test_duplicate_different_bytes_even_if_digest_provider_collides(self):
        # Defensive byte distinction, not a claim of a real SHA-256 collision.
        g=Graph();root=g.add(fixtures()['Intake']);first=g.records[0]
        changed=copy.deepcopy(first);changed['payload']['raw_input']='Different canonical bytes'
        self.assertNotEqual(c(first),c(changed))
        self.assertNotEqual(digest(first),digest(changed))
        def same_digest(value):
            h=value['H']
            return {'type':h['type'],'id':h['id'],'revision':h['revision'],'sha256':'0'*64}
        with patch.object(r,'si_record_ref',side_effect=same_digest):
            self.rejected([first,changed],[root],'REF_HASH_MISMATCH','$.records[1]')

    def test_missing_previous_origin_and_nested_known(self):
        g,named=graph_fixture()
        root=named['revision'];record=g.refs[key(root)]
        for missing,path in ((record['H']['previous'],'.H.previous'),
                             (record['H']['origin']['run_ref'],'.H.origin.run_ref')):
            records=[v for v in g.records if (v['H']['type'],v['H']['id'],v['H']['revision'])!=tuple(missing[k] for k in ('type','id','revision'))]
            self.rejected(records,[root],'REF_MISSING',path)
        channel=g.refs[key(named['known_portfolio'])]
        missing=channel['payload']['portfolio']['value'][0]['story_ref']
        records=[v for v in g.records if (v['H']['type'],v['H']['id'],v['H']['revision'])!=tuple(missing[k] for k in ('type','id','revision'))]
        self.rejected(records,[named['known_portfolio']],'REF_MISSING','.payload.portfolio.value[0].story_ref')

    def test_missing_context_input(self):
        g,named=graph_fixture()
        value=fixtures()['RunRecord'];ctx={'context_version':1,'active_input_refs':[named['manual']],
            'selection_head_refs':[],'editorial_snapshot_sha256':unknown()}
        run=g.run('DISCOVERY',[],ctx)
        records=[v for v in g.records if v['H']['id']!=named['manual']['id']]
        self.rejected(records,[run],'REF_MISSING')

    def test_nested_wrong_hash_and_tampered_record(self):
        g,named=graph_fixture();channel=copy.deepcopy(g.refs[key(named['known_portfolio'])])
        channel['payload']['portfolio']['value'][0]['story_ref']['sha256']='0'*64
        root={**named['known_portfolio'],'sha256':digest(channel)}
        records=[v for v in g.records if v['H']['id']!=root['id']]+[channel]
        self.rejected(records,[root],'REF_HASH_MISMATCH','.payload.portfolio.value[0].story_ref.sha256')
        g,named=graph_fixture();records=copy.deepcopy(g.records)
        records[0]['payload']['raw_input']='tampered'
        self.rejected(records,[named['manual']],'REF_HASH_MISMATCH')

    def test_snapshot_omitted_transitive_extra_and_order(self):
        for mode in ('omitted','extra','order'):
            g,named=graph_fixture()
            run=copy.deepcopy(g.refs[key(named['run_snapshot'])]);p=run['payload']
            if mode=='omitted':
                roots=p['semantic_input_refs']
                candidate=next(x for x in p['input_snapshot'] if x not in roots)
                p['input_snapshot'].remove(candidate)
            elif mode=='extra':
                p['input_snapshot'].append(named['revision']);p['input_snapshot'].sort(key=key)
            else:p['input_snapshot'].reverse()
            run['H']['input_refs']=copy.deepcopy(p['input_snapshot'])
            ref={**named['run_snapshot'],'sha256':digest(run)}
            # Other unreachable records may still refer to the former Run bytes;
            # they are not roots and cannot silently become certified dependencies.
            records=[v for v in g.records if v['H']['id']!=ref['id']]+[run]
            self.rejected(records,[ref],'TYPE' if mode=='order' else 'PROVENANCE_MISMATCH','.payload.input_snapshot')

    def test_direct_indirect_identity_cycles(self):
        # Negative cycles deliberately contain incorrect edge hashes: solving a
        # SHA fixed point would be impossible as a positive content-addressed DAG.
        a=fixtures()['Intake'];b=copy.deepcopy(a);b['H']['id']='ffffffff-2222-4222-8222-222222222222'
        def claim(value):return {'type':'Intake','id':value['H']['id'],'revision':1,'sha256':'a'*64}
        a['H']['input_refs']=[claim(a)]
        root={**claim(a),'sha256':digest(a)}
        self.rejected([a],[root],'DEPENDENCY_CYCLE','.H.input_refs[0]')
        a['H']['input_refs']=[claim(b)];b['H']['input_refs']=[claim(a)]
        root={**claim(a),'sha256':digest(a)}
        self.rejected([a,b],[root],'DEPENDENCY_CYCLE','.H.input_refs[0]')

    def test_run_self_and_own_output_cycles(self):
        run=fixtures()['RunRecord']
        run_ref={'type':'RunRecord','id':run['H']['id'],'revision':1,'sha256':'a'*64}
        run['payload']['input_snapshot']=[run_ref];run['H']['input_refs']=[run_ref]
        self.rejected([run],[{**run_ref,'sha256':digest(run)}],'DEPENDENCY_CYCLE')
        run=fixtures()['RunRecord'];idea=fixtures()['StoryIdea'];intake=fixtures()['Intake']
        intake_ref={'type':'Intake','id':intake['H']['id'],'revision':1,'sha256':digest(intake)}
        idea['H']['origin']['run_ref']=run_ref;idea['payload'].update(intake_ref=intake_ref,source_refs=unknown())
        idea_ref={'type':'StoryIdea','id':idea['H']['id'],'revision':1,'sha256':digest(idea)}
        run['payload']['semantic_input_refs']=[idea_ref]
        run['payload']['input_snapshot']=[idea_ref];run['H']['input_refs']=[idea_ref]
        actual_run={**run_ref,'sha256':digest(run)}
        self.rejected([run,idea,intake],[actual_run],'DEPENDENCY_CYCLE')

    def test_eref_and_free_text_are_not_si_edges(self):
        g=Graph();value=fixtures()['Intake']
        value['H']['editorial_refs']=[eref('source')]
        value['payload']['raw_input']=json.dumps({'type':'StoryIdea','id':'ffffffff-2222-4222-8222-222222222222','revision':1,'sha256':'a'*64})
        root=g.add(value)
        self.assertEqual([root],r.resolve_si_closure(g.records,[root]))
        with self.assertRaises(SIValidationError):r.resolve_si_closure(g.records,[eref('source')])

    def test_typed_extractor_nested_path_coverage(self):
        g,named=graph_fixture()
        paths=set()
        for value in g.records:paths.update(path for _,path in r._direct_refs(value,'$'))
        for path in ('$.H.previous','$.H.origin.run_ref','$.H.input_refs[0]',
            '$.payload.portfolio.value[0].story_ref','$.payload.portfolio.value[0].basis_ref',
            '$.payload.chapters[0].claim_refs[0]','$.payload.ratings[0].basis_refs[0]',
            '$.payload.context_snapshot.active_input_refs[0]',
            '$.payload.context_snapshot.selection_head_refs[0]',
            '$.payload.privacy_grant.allowed_text_fields[0].source_ref',
            '$.payload.display_items[0].source_ref','$.payload.omissions[0].source_ref',
            '$.payload.review_state_at_capture.evaluation_ref',
            '$.payload.review_state_at_capture.creative_ref',
            '$.payload.review_state_at_capture.brief_ref',
            '$.payload.review_state_at_capture.selection_head_refs[0]',
            '$.payload.scope.idea_ref','$.payload.scope.audience_ref','$.payload.scope.channel_ref'):
            self.assertIn(path,paths)
        self.assertFalse(any('editorial_ref' in path for path in paths))

    def test_no_mutation_and_detached_results(self):
        g,named=graph_fixture();before=copy.deepcopy(g.records);roots=[named['packet']];before_roots=copy.deepcopy(roots)
        result=r.resolve_si_closure(g.records,roots);result[0]['sha256']='0'*64
        record=r.resolve_si_record(g.records,named['manual']);record['payload']['raw_input']='modified result'
        self.assertEqual(before,g.records);self.assertEqual(before_roots,roots)
        self.assertEqual(g.closure(roots),r.resolve_si_closure(g.records,roots))

    def test_unreachable_structural_validation_not_graph_certification(self):
        g=Graph();root=g.add(fixtures()['Intake'])
        # A locally valid orphan may contain unresolved SIRefs. It is not returned
        # or certified when outside the queried closure.
        orphan=fixtures()['EvidenceItem'];g.add(orphan)
        self.assertEqual([root],r.resolve_si_closure(g.records,[root]))
        invalid=copy.deepcopy(orphan);invalid['payload']['extra']=1
        self.rejected(g.records+[invalid],[root],'UNKNOWN_FIELD')

    def test_plain_list_interfaces(self):
        for bad in (None,{},(),iter([])):
            with self.assertRaises(SIValidationError):r.resolve_si_closure(bad,[])
            with self.assertRaises(SIValidationError):r.resolve_si_closure([],bad)
        with self.assertRaises(SIValidationError):r.resolve_si_record([],{'type':'Intake'})

    def test_iterative_chain_no_bundle_record_count_or_aggregate_byte_cap(self):
        g=Graph();prior=None
        for i in range(1100):
            value=fixtures()['Intake'];value['payload']['raw_input']='x'*1000
            value['H']['input_refs']=[] if prior is None else [prior]
            prior=g.add(value,[] if prior is None else [prior])
        self.assertGreater(sum(len(c(value)) for value in g.records),1_000_000)
        self.assertEqual(g.closure([prior]),r.resolve_si_closure(g.records,[prior]))
        self.assertEqual(1100,len(g.records))


if __name__=='__main__':unittest.main()
