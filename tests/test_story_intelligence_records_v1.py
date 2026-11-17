"""Synthetic unresolved SI records: local shape, never proof of facts/rights."""
import copy
import hashlib
import json
import unittest

from story_intelligence import records_v1 as r
from story_intelligence.model_v1 import SIValidationError

TYPES = ('Intake','StoryIdea','SourceItem','ClaimItem','EvidenceItem','ClaimCheck',
    'AudienceHypothesis','ChannelContext','Angle','Rubric','RunRecord','EvaluationReport',
    'CreativeAlternative','VisualRequirement','Risk','ProductionBrief','Selection','ReviewPacket')
IDS = {kind:f'{i:08x}-1111-4111-8111-111111111111' for i,kind in enumerate(TYPES,1)}
AT = '2026-11-09T00:00:00Z'


def c(value):
    """Independent fixture bytes, no SI/S1 production codec."""
    return json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()


def sha(value): return hashlib.sha256(c(value)).hexdigest()
def known(value): return {'state':'KNOWN','value':value}
def unknown(): return {'state':'UNKNOWN','reason':'Не перевірено'}
def ref(kind, revision=1):
    return {'type':kind,'id':IDS[kind],'revision':revision,'sha256':'a'*64}
def eref(kind):
    return {'kind':kind,'id':'eeeeeeee-1111-4111-8111-111111111111','revision':1,'content_hash':'b'*64}
def context():
    return {'context_version':1,'active_input_refs':[],'selection_head_refs':[],
            'editorial_snapshot_sha256':unknown()}
def confidence(): return {'level':'UNKNOWN','basis':'Синтетичний приклад, не оцінка істини'}
def header(kind, revision=1):
    mode={'StoryIdea':'RULE_DERIVED','CreativeAlternative':'TEMPLATE_DERIVED',
        'EvaluationReport':'RULE_DERIVED','ReviewPacket':'RULE_DERIVED','RunRecord':'RUN_METADATA'}.get(kind,'MANUAL_INPUT')
    if revision>1 and kind!='Selection': mode='HUMAN_EDIT'
    run=ref('RunRecord') if mode in ('RULE_DERIVED','TEMPLATE_DERIVED','HUMAN_EDIT') else None
    return {'si_version':1,'type':kind,'id':IDS[kind],'revision':revision,
        'previous':None if revision==1 else ref(kind,revision-1),'created_at':AT,
        'creator_label':{'RunRecord':'SI_ENGINE','ReviewPacket':'SI_EXPORTER'}.get(kind,'Автор'),
        'origin':{'mode':mode,'run_ref':run,'imported_from':None},
        'input_refs':[ref(kind,revision-1)] if revision>1 and kind!='Selection' else [],'editorial_refs':[]}


def fixtures():
    """Construct all payloads by contract, independently of production schema tables."""
    p={}
    p['Intake']={'input_kind':'TOPIC','raw_input':'Історія науки ї є і 😀','locale':'uk',
        'supplied_source_refs':[],'user_goal':unknown()}
    p['StoryIdea']={'intake_ref':ref('Intake'),'title':'Історія','summary':'Гіпотеза',
        'viewer_question':'Що ми знаємо?','source_refs':unknown(),'candidate_binding':None}
    p['SourceItem']={'source_kind':'URL','original_locator':'https://example.invalid/synthetic',
        'title':known('Джерело'),'author':unknown(),'publisher':unknown(),'published_at':unknown(),
        'captured_at':unknown(),'material_sha256':unknown(),'editorial_ref':None,
        'rights_note':unknown(),'freshness_requirement':unknown()}
    p['ClaimItem']={'statement':'Синтетичне неперевірене твердження','claim_kind':'interpretation',
        'materiality':'CONTEXT','evidence_expectation':'Потрібні джерела','editorial_ref':None}
    p['EvidenceItem']={'claim_ref':ref('ClaimItem'),'source_ref':ref('SourceItem'),
        'relation':'insufficient','locator':unknown(),'explanation':'Не підтверджує факт'}
    p['ClaimCheck']={'claim_ref':ref('ClaimItem'),'evidence_refs':unknown(),'state':'unreviewed',
        'qualification':None,'reviewer_label':None,'reviewed_at':None,'reason':None}
    p['AudienceHypothesis']={'locale':'uk','region':unknown(),'knowledge_level':unknown(),
        'motivation':unknown(),'interests':unknown(),'age_range':unknown(),'basis_refs':[],'assumptions':[]}
    p['ChannelContext']={'channel_alias':'Синтетичний канал','purpose':'Наука',
        'audience_ref':ref('AudienceHypothesis'),'constraints':[],'portfolio':unknown(),
        'analytics':unknown(),'capability_notes':known('CPU only')}
    p['Angle']={'idea_ref':ref('StoryIdea'),'audience_ref':ref('AudienceHypothesis'),
        'question':'Що невідомо?','thesis':'Робоча гіпотеза','claim_refs':[],
        'distinction':'Пояснити невизначеність','limitations':[]}
    keys=('audience_interest','channel_fit','angle_novelty','evidence_quality','narrative_potential',
        'visual_feasibility','resource_fit','risk_manageability','portfolio_distinctness')
    weights=(15,10,10,20,15,10,10,5,5)
    p['Rubric']={'method_id':'si-rubric','method_version':'1','criteria':[
        {'key':key,'description':'Евристичний критерій','weight_percent':weight,'min':0,'max':5,
         'direction':'HIGH_IS_BETTER'} for key,weight in zip(keys,weights)],
        'missing_policy':'ALL_REQUIRED','blocker_policy_version':'1'}
    p['RunRecord']={'stage':'DISCOVERY','method_id':'si.discover-local','method_version':'1-r1',
        'request_payload_sha256':'c'*64,'semantic_input_refs':[],'input_snapshot':[],
        'context_snapshot':context(),'editorial_snapshot_sha256':unknown(),'rubric_ref':None,
        'provider':None,'started_at':AT,'finished_at':AT,'confidence':confidence(),
        'fresh_trends':unknown(),'caveats':['Немає мережевого пошуку']}
    p['EvaluationReport']={'idea_ref':ref('StoryIdea'),'angle_ref':ref('Angle'),
        'audience_ref':ref('AudienceHypothesis'),'channel_ref':ref('ChannelContext'),
        'rubric_ref':ref('Rubric'),'run_ref':ref('RunRecord'),'ratings':[
            {'criterion_key':key,'value':unknown(),'basis_refs':[],'explanation':'Немає даних',
             'confidence':confidence()} for key in keys], 'risk_refs':[],
        'eligibility':{'state':'NEEDS_RESEARCH','reason_codes':['EVIDENCE_NEEDED']},
        'aggregate_tenths':unknown(),'caveats':[]}
    p['CreativeAlternative']={'angle_ref':ref('Angle'),'run_ref':ref('RunRecord'),
        'hook_strategy':'QUESTION','hook_text':'Що залишається невідомим?',
        'hook_claim_refs':[],'title_options':['Історія науки','Питання науки'],
        'thumbnail_notes':'Локальна схема','chapters':[{'heading':'Питання','purpose':'Контекст',
            'claim_refs':[],'target_seconds':15},{'heading':'Межі','purpose':'Невизначеність',
            'claim_refs':[],'target_seconds':20}], 'retention_0_30':'Ясне питання',
        'style_constraints':[],'omitted_strategy_reason':None}
    p['VisualRequirement']={'chapter_index':1,'role':'LOCAL','description':'Власна схема',
        'acquisition':'LOCAL_CREATE','source_refs':[],'material_sha256':unknown(),
        'rights_state':'UNKNOWN','intended_use':'Приватне обговорення','licence_basis':unknown(),
        'effort':unknown(),'fallback':known('Текстова картка'),'asset_ref':None}
    p['Risk']={'category':'SCIENTIFIC','severity':'HIGH','blocking':True,'basis_refs':[],
        'description':'Неповні докази','mitigation':'Дослідити','resolution':'OPEN',
        'resolution_basis_refs':[],'owner_role':'Дослідник'}
    p['ProductionBrief']={'idea_ref':ref('StoryIdea'),'audience_ref':ref('AudienceHypothesis'),
        'channel_ref':ref('ChannelContext'),'angle_ref':ref('Angle'),
        'evaluation_ref':ref('EvaluationReport'),'creative_ref':ref('CreativeAlternative'),
        'locale':'uk','content_mode':'factual','intended_use':unknown(),'promise':'Пояснити межі знань',
        'duration_min_s':60,'duration_max_s':120,'intensity':'CALM','source_refs':[],
        'claim_refs':[],'claim_check_refs':[],'visual_refs':[],'risk_refs':[ref('Risk')],
        'required_reviews':['Перевірка фактів'],'must_avoid':['Вигадані факти'],'profile_ref':None,
        'production':{'output_preset':'VERTICAL_720x1280','script_locale':'uk','narration_locale':'uk',
            'subtitle_locale':'uk','tts':'LOCAL_WAV','asr':'NONE','editing':'LOCAL_STILLS_FFMPEG_PLAN',
            'voice_ref':unknown(),'resource_budget':unknown(),'cpu_fallback':'Локальні слайди',
            'optional_provider_notes':[]},'workflow_state':'DRAFT','unresolved':['Немає доказів'],
        'creative_selection_ref':None}
    p['Selection']={'scope':{'purpose':'CREATIVE_CHOICE','idea_ref':ref('StoryIdea'),
        'audience_ref':ref('AudienceHypothesis'),'channel_ref':ref('ChannelContext')},
        'target_ref':ref('CreativeAlternative'),'choice':'REQUEST_CHANGES','selector_label':'Редактор',
        'reason':'Потрібне дослідження'}
    sources=[ref(k) for k in ('StoryIdea','SourceItem','ClaimCheck','CreativeAlternative',
        'Risk','EvaluationReport','ProductionBrief')]
    sources.sort(key=lambda x:(x['type'],x['id'],x['revision'],x['sha256']))
    p['ReviewPacket']={'format_version':'si-review-packet/1-r1','purpose':'DISCUSSION_ONLY',
        'brief_ref':ref('ProductionBrief'),'context_snapshot':context(),'source_closure_refs':sources,
        'existing_editorial_refs':[],'source_snapshot_digest':'0'*64,
        'redaction_profile':'si-packet-redact/1','privacy_grant':{
            'reviewed_snapshot_digest':'0'*64,'allowed_text_fields':[],'confirmed':True},
        'display_items':[],'omissions':[],'unresolved':['EVIDENCE_NEEDED'],
        'review_state_at_capture':{'projection_version':1,'context_hash':sha(context()),
            'evaluation_ref':ref('EvaluationReport'),'creative_ref':ref('CreativeAlternative'),
            'brief_ref':ref('ProductionBrief'),'selection_head_refs':[],'currentness':'CURRENT',
            'review_state':'NEEDS_RESEARCH','reason_codes':['EVIDENCE_NEEDED'],
            'editorial_approval_state':'NOT_EVALUATED'}}
    records={kind:{'H':header(kind),'payload':payload} for kind,payload in p.items()}
    refresh_packet(records['ReviewPacket'])
    return records


def refresh_packet(record):
    p=record['payload']
    p['source_snapshot_digest']=sha({k:p[k] for k in ('context_snapshot','source_closure_refs','existing_editorial_refs')})
    p['privacy_grant']['reviewed_snapshot_digest']=p['source_snapshot_digest']
    p['review_state_at_capture']['context_hash']=sha(p['context_snapshot'])


def packet_with_views():
    record=fixtures()['ReviewPacket'];p=record['payload']
    p['privacy_grant']['allowed_text_fields']=[
        {'source_ref':ref('CreativeAlternative'),'field_path':'title_options[0]','value_sha256':sha('Історія науки')},
        {'source_ref':ref('StoryIdea'),'field_path':'title','value_sha256':sha('Історія')}]
    p['display_items']=[
        {'source_ref':ref('ClaimCheck'),'fields':[{'field_path':'reviewer_label','kind':'REDACTED','text':None}]},
        {'source_ref':ref('CreativeAlternative'),'fields':[{'field_path':'title_options[0]','kind':'TEXT','text':'Історія науки'}]},
        {'source_ref':ref('EvaluationReport'),'fields':[{'field_path':'eligibility.state','kind':'STATE','text':'NEEDS_RESEARCH'}]},
        {'source_ref':ref('Risk'),'fields':[{'field_path':'blocking','kind':'STATE','text':'true'}]},
        {'source_ref':ref('SourceItem'),'fields':[{'field_path':'original_locator','kind':'REDACTED','text':None}]},
        {'source_ref':ref('StoryIdea'),'fields':[{'field_path':'title','kind':'TEXT','text':'Історія'}]}]
    p['omissions']=[{'source_ref':ref(kind),'field_path':field,'reason_code':'PRIVATE_FIELD'}
        for kind,field in (('ClaimCheck','reviewer_label'),('SourceItem','original_locator'))]
    return record


class RecordsTests(unittest.TestCase):
    def reject(self,value,code=None,path=None):
        before=copy.deepcopy(value)
        with self.assertRaises(SIValidationError) as caught:r.validate_si_record(value)
        if code:self.assertEqual(code,caught.exception.code)
        if path:self.assertEqual(path,caught.exception.path)
        self.assertEqual(before,value)

    def test_all_18_positive_detached(self):
        records=fixtures();self.assertEqual(set(TYPES),set(records))
        for kind,value in records.items():
            with self.subTest(kind=kind):
                before=copy.deepcopy(value);out=r.validate_si_record(value)
                self.assertEqual(before,out);self.assertEqual(before,value)
                out['payload'].clear();out['H']['origin']['mode']='bad'
                self.assertEqual(before,value)

    def test_all_18_missing_unknown_wrong_type(self):
        for kind,record in fixtures().items():
            for key in record['payload']:
                with self.subTest(kind=kind,field=key):
                    value=copy.deepcopy(record);del value['payload'][key]
                    self.reject(value,'MISSING_FIELD','$.payload.'+key)
                value=copy.deepcopy(record);value['payload'][key]={'unexpected':0}
                self.reject(value)
            value=copy.deepcopy(record);value['payload']['extra']=None
            self.reject(value,'UNKNOWN_FIELD','$.payload.extra')
            value=copy.deepcopy(record);value['payload']=[];self.reject(value,'TYPE','$.payload')

    def test_root_header_ref_identity(self):
        value=fixtures()['Intake']
        for field in ('H','payload'):
            bad=copy.deepcopy(value);del bad[field];self.reject(bad,'MISSING_FIELD','$.'+field)
        self.reject({**value,'extra':None},'UNKNOWN_FIELD','$.extra')
        value['H']['si_version']=True;self.reject(value,'TYPE','$.H.si_version')
        value=fixtures()['Intake'];expected=r.si_record_ref(value)
        self.assertEqual(expected,r.validate_si_record_ref(value,expected))
        for key,bad in (('type','SourceItem'),('id',IDS['SourceItem']),('revision',2),('sha256','0'*64)):
            supplied={**expected,key:bad}
            with self.assertRaises(SIValidationError) as caught:r.validate_si_record_ref(value,supplied)
            self.assertEqual('$.expected_ref.'+key,caught.exception.path)
            self.assertEqual('REF_TYPE_MISMATCH' if key=='type' else 'REF_HASH_MISMATCH',caught.exception.code)

    def test_claimcheck_review_rules(self):
        for state in ('supported','qualified','disputed','unverified','removed'):
            value=fixtures()['ClaimCheck'];p=value['payload'];p.update(state=state,
                reviewer_label='Дослідник',reviewed_at=AT,reason='Синтетична review assertion',
                qualification='Межі' if state=='qualified' else None,evidence_refs=known([ref('EvidenceItem')]))
            r.validate_si_record(value)
            for key in ('reviewer_label','reviewed_at','reason'):
                bad=copy.deepcopy(value);bad['payload'][key]=None;self.reject(bad,'TYPE')
        value=fixtures()['ClaimCheck'];value['payload']['reviewer_label']='bad';self.reject(value,'TYPE')
        value=fixtures()['ClaimCheck'];value['payload'].update(state='qualified',qualification=None,
            reviewer_label='A',reviewed_at=AT,reason='B',evidence_refs=known([]));self.reject(value,'TYPE')
        value['payload']['qualification']='Обмеження';self.reject(value,'EVIDENCE_NEEDED')
        value['payload']['evidence_refs']=unknown();self.reject(value,'EVIDENCE_NEEDED')

    def test_rubric_ratings_unknown(self):
        value=fixtures()['Rubric'];value['payload']['criteria'][0]['weight_percent']=16;self.reject(value,'TYPE')
        value=fixtures()['Rubric'];value['payload']['criteria'][1]['key']='audience_interest';self.reject(value,'TYPE')
        for key,bad in (('min',False),('max',6),('direction','LOW_IS_BETTER')):
            value=fixtures()['Rubric'];value['payload']['criteria'][0][key]=bad;self.reject(value,'TYPE')
        value=fixtures()['EvaluationReport'];value['payload']['aggregate_tenths']=known(500);self.reject(value,'TYPE')
        value=fixtures()['EvaluationReport'];value['payload']['recommendation']='PROCEED_TO_BRIEF_REVIEW';self.reject(value,'UNKNOWN_FIELD')
        value=fixtures()['EvaluationReport'];value['payload']['ratings'][0]['value']=known(True);self.reject(value,'TYPE')
        value=fixtures()['EvaluationReport'];value['payload']['ratings'][0]['value']['value']=0;self.reject(value,'UNKNOWN_FIELD')

    def test_run_stages_and_local_not_resolution(self):
        methods={'DISCOVERY':'si.discover-local','EVALUATION':'si.evaluate','CREATIVE':'si.creative-templates',
            'BRIEF_ASSEMBLY':'si.brief-assembly','PACKET_EXPORT':'si.review-packet','REVISION':'si.human-revision'}
        for stage,method in methods.items():
            value=fixtures()['RunRecord'];p=value['payload'];p.update(stage=stage,method_id=method)
            if stage in ('EVALUATION','BRIEF_ASSEMBLY','PACKET_EXPORT'):p['rubric_ref']=ref('Rubric')
            r.validate_si_record(value)  # No referenced records supplied/claimed verified.
            p['method_id']='si.other';self.reject(value,'PROVENANCE_MISMATCH')
        value=fixtures()['RunRecord'];value['payload']['output_refs']=[];self.reject(value,'UNKNOWN_FIELD')
        value=fixtures()['RunRecord'];value['payload']['provider']={'id':unknown(),'version':unknown(),
            'model_id':unknown(),'model_version':unknown(),'config_digest':unknown()};self.reject(value,'PROVENANCE_MISMATCH')
        value=fixtures()['RunRecord'];value['payload']['context_snapshot']['active_input_refs']=[ref('Selection')];self.reject(value,'REF_TYPE_MISMATCH')

    def test_initial_and_human_revision(self):
        for kind in ('StoryIdea','CreativeAlternative'):
            value=fixtures()[kind];value['H']['origin']={'mode':'MANUAL_INPUT','run_ref':None,'imported_from':None}
            self.reject(value,'PROVENANCE_MISMATCH')
            value=fixtures()[kind];value['H']=header(kind,2)
            value['H']['origin']['run_ref']['id']='99999999-1111-4111-8111-111111111111'
            r.validate_si_record(value)
            value['H']['previous']['revision']=2;self.reject(value,'PROVENANCE_MISMATCH')
        value=fixtures()['CreativeAlternative'];value['payload']['run_ref']['id']=IDS['Intake'];self.reject(value,'PROVENANCE_MISMATCH')
        value=fixtures()['CreativeAlternative'];value['H']=header('CreativeAlternative',2);self.reject(value,'PROVENANCE_MISMATCH')

    def test_brief_selection_risk_and_languages(self):
        value=fixtures()['ProductionBrief'];value['payload']['duration_max_s']=1;self.reject(value,'TYPE')
        for key in ('script_locale','narration_locale','subtitle_locale'):
            value=fixtures()['ProductionBrief'];value['payload']['production'][key]='ru';self.reject(value,'LOCALE_MISMATCH')
        value=fixtures()['ProductionBrief'];value['payload']['creative_selection_ref']=ref('Risk');self.reject(value,'REF_TYPE_MISMATCH')
        value=fixtures()['Selection'];value['payload']['scope']['purpose']='BRIEF_REVIEW';self.reject(value,'REF_TYPE_MISMATCH')
        value['payload']['target_ref']=ref('ProductionBrief');r.validate_si_record(value)
        value=fixtures()['Risk'];value['payload']['resolution']='MITIGATED';self.reject(value,'TYPE')
        value['payload']['resolution_basis_refs']=[ref('Intake')];r.validate_si_record(value)
        value=fixtures()['CreativeAlternative'];value['payload']['chapters'][0]['target_seconds']=False;self.reject(value,'TYPE')
        value=fixtures()['ProductionBrief'];value['payload']['workflow_state']='IN_REVIEW';self.reject(value,'MISSING_FIELD')
        value['payload']['creative_selection_ref']=ref('Selection');self.reject(value,'PROVENANCE_MISMATCH')
        value['H']['input_refs']=[ref('Selection')];r.validate_si_record(value)
        value=fixtures()['VisualRequirement'];value['payload']['rights_state']='DOCUMENTED';self.reject(value,'RIGHTS_BLOCKED')
        value['payload']['licence_basis']=known('Supplied mock basis, not verified rights');r.validate_si_record(value)

    def test_nested_shapes_typed_refs_nullables(self):
        mutations=[('StoryIdea','candidate_binding',eref('source')),
            ('SourceItem','editorial_ref',eref('asset')),('VisualRequirement','asset_ref',eref('source')),
            ('ProductionBrief','profile_ref',eref('source')),('Angle','claim_refs',[ref('SourceItem')]),
            ('SourceItem','published_at',known('2023-02-29T00:00:00Z')),
            ('AudienceHypothesis','interests',known([1])),('Risk','blocking',1)]
        for kind,key,bad in mutations:
            value=fixtures()[kind];value['payload'][key]=bad;self.reject(value)
        value=fixtures()['ChannelContext'];value['payload']['portfolio']=known([{
            'story_ref':ref('StoryIdea'),'published_title':'Тест','published_locator':unknown(),
            'published_at':unknown(),'angle_notes':'Робочі нотатки','basis_ref':ref('Intake')}]);r.validate_si_record(value)
        value['payload']['portfolio']['value'][0]['extra']=1;self.reject(value,'UNKNOWN_FIELD')

    def test_nested_closed_shapes_all_present_objects(self):
        count=0
        def walk(node, route):
            if type(node) is dict:
                yield route,node
                for key,child in node.items():yield from walk(child,route+[key])
            elif type(node) is list:
                for i,child in enumerate(node):yield from walk(child,route+[i])
        for kind,record in fixtures().items():
            for route,node in walk(record['payload'],['payload']):
                for key in node:
                    value=copy.deepcopy(record);target=value
                    for step in route:target=target[step]
                    del target[key]
                    with self.subTest(kind=kind,route=route,key=key):self.reject(value,'MISSING_FIELD')
                    count+=1
                value=copy.deepcopy(record);target=value
                for step in route:target=target[step]
                target['unexpected']=0
                self.reject(value,'UNKNOWN_FIELD');count+=1
        self.assertGreater(count,500)

    def test_available_local_consistency(self):
        value=fixtures()['RunRecord'];value['payload']['semantic_input_refs']=[ref('Intake')]
        self.reject(value,'REF_MISSING')
        value['payload']['input_snapshot']=[ref('Intake')];value['H']['input_refs']=[ref('Intake')]
        r.validate_si_record(value)
        value=fixtures()['StoryIdea'];value['H']=header('StoryIdea',2);value['H']['input_refs']=[]
        self.reject(value,'PROVENANCE_MISMATCH')
        value=fixtures()['ProductionBrief'];value['payload']['locale']='ru'
        for key in ('script_locale','narration_locale','subtitle_locale'):value['payload']['production'][key]='ru'
        r.validate_si_record(value)
        value=fixtures()['RunRecord'];value['payload']['provider']={'id':unknown(),'version':unknown(),
            'model_id':unknown(),'model_version':unknown(),'config_digest':unknown(),'extra':1}
        self.reject(value,'UNKNOWN_FIELD')

    def test_conflicting_hash_for_one_local_reference_identity(self):
        value=fixtures()['CreativeAlternative'];value['H']=header('CreativeAlternative',2)
        value['H']['origin']['run_ref']['sha256']='b'*64
        self.reject(value,'REF_HASH_MISMATCH')
        value=fixtures()['ProductionBrief'];value['payload']['source_refs']=[ref('SourceItem')]
        value['H']['input_refs']=[{**ref('SourceItem'),'sha256':'c'*64}]
        self.reject(value,'REF_HASH_MISMATCH')
        # Repeating the same exact unresolved ref is fine; no external record needed.
        value['H']['input_refs']=[ref('SourceItem')]
        r.validate_si_record(value)

    def test_limits_and_plain_types(self):
        value=fixtures()['Intake'];value['payload']['raw_input']='a'*100_001;self.reject(value,'LIMIT')
        value=fixtures()['Intake'];value['payload']['raw_input']='\ud800';self.reject(value,'TYPE')
        value=fixtures()['Intake'];value['payload']['user_goal']={'state':'UNKNOWN','reason':'x','value':0};self.reject(value,'UNKNOWN_FIELD')
        value=fixtures()['Intake'];value['payload']['raw_input']=[[[0]]];self.reject(value,'TYPE')
        value=fixtures()['Intake'];deep=0
        for _ in range(33):deep=[deep]
        value['payload']['raw_input']=deep;self.reject(value,'LIMIT')
        value=fixtures()['Intake'];value['payload']['extra']=['a'*100_000]*11;self.reject(value,'LIMIT')


class PacketTests(unittest.TestCase):
    reject = RecordsTests.reject

    def test_P_T01_title_namespace(self):
        r.validate_si_record(packet_with_views())
        for path in ('payload.title','H.title','$.title','StoryIdea.title','title ','summary.bad'):
            value=packet_with_views();value['payload']['display_items'][-1]['fields'][0]['field_path']=path
            self.reject(value,'PRIVACY_BLOCKED')

    def test_P_T02_numeric_index_order_and_aliases(self):
        for path in ('title_options[00]','title_options[*]','title_options[-1]',
                     'title_options[+1]','title_options[]','title_options[1:2]'):
            value=packet_with_views();value['payload']['display_items'][1]['fields'][0]['field_path']=path
            self.reject(value,'PRIVACY_BLOCKED')
        # Source not supplied: existence of [10] explicitly remains unresolved.
        value=packet_with_views();p=value['payload'];item=p['display_items'][1]
        item['fields']=[{'field_path':f'title_options[{i}]','kind':'TEXT','text':'Тест'} for i in (2,10)]
        p['privacy_grant']['allowed_text_fields']=[
            {'source_ref':ref('CreativeAlternative'),'field_path':f'title_options[{i}]','value_sha256':sha('Тест')} for i in (2,10)] + [p['privacy_grant']['allowed_text_fields'][-1]]
        r.validate_si_record(value)
        item['fields'].reverse();self.reject(value,'TYPE')

    def test_P_T03_chapter_paths_schema_before_indices(self):
        value=packet_with_views();p=value['payload'];fields=[
            {'field_path':path,'kind':'TEXT','text':'Тест'} for path in
            ('chapters[0].heading','chapters[0].purpose','chapters[1].heading','chapters[1].purpose')]
        p['display_items'][1]['fields']=fields
        p['privacy_grant']['allowed_text_fields']=[{'source_ref':ref('CreativeAlternative'),
            'field_path':f['field_path'],'value_sha256':sha('Тест')} for f in fields]+[p['privacy_grant']['allowed_text_fields'][-1]]
        r.validate_si_record(value)
        p['display_items'][1]['fields'][0]['field_path']='chapters[0]';self.reject(value,'PRIVACY_BLOCKED')

    def test_P_T04_source_title_value_unresolved(self):
        value=packet_with_views();p=value['payload']
        p['display_items'][4]['fields']=[{'field_path':'title.value','kind':'TEXT','text':'Джерело'}]
        p['privacy_grant']['allowed_text_fields'].insert(1,
            {'source_ref':ref('SourceItem'),'field_path':'title.value','value_sha256':sha('Джерело')})
        p['omissions'].pop();r.validate_si_record(value)
        # No source lookup here: UNKNOWN-vs-KNOWN actual source checked in E01.2b.
        p['display_items'][4]['fields'][0]['field_path']='title';self.reject(value,'PRIVACY_BLOCKED')

    def test_P_T05_eligibility_state_no_grant(self):
        value=packet_with_views();r.validate_si_record(value)
        value['payload']['privacy_grant']['allowed_text_fields'].insert(1,
            {'source_ref':ref('EvaluationReport'),'field_path':'eligibility.state','value_sha256':sha('NEEDS_RESEARCH')})
        self.reject(value,'PRIVACY_BLOCKED')
        value=packet_with_views();value['payload']['display_items'][2]['fields'][0]['field_path']='EvaluationEligibility.state'
        self.reject(value,'PRIVACY_BLOCKED')

    def test_P_T06_boolean_ascii(self):
        for valid in ('true','false'):
            value=packet_with_views();value['payload']['display_items'][3]['fields'][0]['text']=valid
            r.validate_si_record(value)  # Actual source bool not authenticated here.
        for invalid in ('True','False','1','FALSE',None):
            value=packet_with_views();value['payload']['display_items'][3]['fields'][0]['text']=invalid
            self.reject(value,'TYPE')

    def test_P_T07_projection_only(self):
        for source in ('ProductionBrief','EvaluationReport','ReviewPacket'):
            for path in ('review_state','currentness','review_state_at_capture.review_state'):
                value=fixtures()['ReviewPacket'];p=value['payload']
                # For ReviewPacket use another, unresolved ref (not current packet).
                candidate=ref(source)
                if source=='ReviewPacket':candidate['id']='99999999-1111-4111-8111-111111111111'
                if candidate not in p['source_closure_refs']:p['source_closure_refs'].append(candidate)
                p['source_closure_refs'].sort(key=lambda x:(x['type'],x['id'],x['revision'],x['sha256']))
                p['display_items']=[{'source_ref':candidate,'fields':[{'field_path':path,'kind':'STATE','text':'CURRENT'}]}]
                refresh_packet(value);self.reject(value,'PRIVACY_BLOCKED')
        value=fixtures()['ReviewPacket'];value['payload']['review_state_at_capture']['currentness']='STALE'
        r.validate_si_record(value)  # Frozen declared status, no live resolver.

    def test_P_T08_reviewer_redacted_only(self):
        value=packet_with_views();r.validate_si_record(value)
        for kind in ('TEXT','STATE'):
            value=packet_with_views();field=value['payload']['display_items'][0]['fields'][0]
            field.update(kind=kind,text='Секрет');self.reject(value,'PRIVACY_BLOCKED')

    def test_P_T09_locator_withheld_not_granted(self):
        value=packet_with_views();r.validate_si_record(value)
        value['payload']['privacy_grant']['allowed_text_fields'].insert(1,
            {'source_ref':ref('SourceItem'),'field_path':'original_locator','value_sha256':sha('секрет')})
        self.reject(value,'PRIVACY_BLOCKED')
        value=packet_with_views();value['payload']['display_items'][4]['fields'][0]['text']='секрет'
        self.reject(value,'PRIVACY_BLOCKED')

    def test_P_T10_header_and_unknown_paths(self):
        for path in ('creator_label','origin.imported_from','H.creator_label','payload',
                     'H','unknown','title.not_declared','title.value.extra'):
            value=packet_with_views();value['payload']['display_items'][4]['fields'][0]['field_path']=path
            self.reject(value,'PRIVACY_BLOCKED')

    def test_P_T11_duplicates_and_order(self):
        for collection in ('display_items','omissions'):
            value=packet_with_views();p=value['payload'];p[collection].append(copy.deepcopy(p[collection][0]));self.reject(value,'TYPE')
            value=packet_with_views();value['payload'][collection].reverse();self.reject(value,'TYPE')
        value=packet_with_views();p=value['payload'];p['display_items'][0]['fields']*=2;self.reject(value,'TYPE')
        value=packet_with_views();grants=value['payload']['privacy_grant']['allowed_text_fields'];grants.append(copy.deepcopy(grants[0]));self.reject(value,'TYPE')
        value=packet_with_views();value['payload']['privacy_grant']['allowed_text_fields'].reverse();self.reject(value,'TYPE')

    def test_P_T12_frozen_capture_no_currentness_execution(self):
        value=packet_with_views();before=copy.deepcopy(value)
        first=r.si_record_ref(value)
        # External observed-context change is not an argument to local validation.
        observed=context();observed['active_input_refs']=[ref('StoryIdea',2)]
        self.assertNotEqual(sha(observed),value['payload']['review_state_at_capture']['context_hash'])
        self.assertEqual(first,r.si_record_ref(value));self.assertEqual(before,value)

    def test_F1_capture_brief_is_required(self):
        value=fixtures()['ReviewPacket']
        value['payload']['review_state_at_capture']['brief_ref']=None
        self.reject(value,'PROVENANCE_MISMATCH','$.payload.review_state_at_capture.brief_ref')

    def test_F1_capture_creative_is_required(self):
        value=fixtures()['ReviewPacket']
        value['payload']['review_state_at_capture']['creative_ref']=None
        self.reject(value,'PROVENANCE_MISMATCH','$.payload.review_state_at_capture.creative_ref')

    def test_F1_capture_brief_must_match_exact_packet_brief(self):
        value=fixtures()['ReviewPacket']
        value['payload']['review_state_at_capture']['brief_ref']={
            **ref('ProductionBrief'),'id':'99999999-1111-4111-8111-111111111111'}
        self.reject(value,'PROVENANCE_MISMATCH','$.payload.review_state_at_capture.brief_ref')

    def test_F1_valid_packet_remains_accepted_unchanged(self):
        value=fixtures()['ReviewPacket'];before=copy.deepcopy(value)
        result=r.validate_si_record(value)
        self.assertEqual(before,result);self.assertEqual(before,value)
        self.assertIsNot(result,value)
        self.assertEqual(result['payload']['brief_ref'],
                         result['payload']['review_state_at_capture']['brief_ref'])
        self.assertIsNotNone(result['payload']['review_state_at_capture']['creative_ref'])

    def test_F1_general_prebrief_projection_remains_nullable(self):
        # There is no standalone public projection validator. Exercise the existing
        # value schema directly to guard against globally tightening _REVIEW.
        projection=fixtures()['ReviewPacket']['payload']['review_state_at_capture']
        projection.update(brief_ref=None,creative_ref=None,review_state='AWAITING_CREATIVE')
        before=copy.deepcopy(projection)
        r._check(projection,r._REVIEW,'$',{})
        self.assertEqual(before,projection)

    def test_packet_matches_and_tampering(self):
        for change,code in (('missing_grant','PRIVACY_REVIEW_REQUIRED'),('missing_omission','MISSING_FIELD'),
                            ('hash','REF_HASH_MISMATCH'),('false','PRIVACY_REVIEW_REQUIRED')):
            value=packet_with_views();p=value['payload']
            if change=='missing_grant':p['privacy_grant']['allowed_text_fields'].pop()
            elif change=='missing_omission':p['omissions'].pop()
            elif change=='hash':p['privacy_grant']['allowed_text_fields'][0]['value_sha256']='0'*64
            else:p['privacy_grant']['confirmed']=False
            self.reject(value,code)
        value=packet_with_views();value['payload']['source_snapshot_digest']='0'*64;self.reject(value,'REF_HASH_MISMATCH')
        value=packet_with_views();value['payload']['source_closure_refs'].reverse();self.reject(value,'TYPE')
        value=packet_with_views();value['payload']['display_items'][0]['source_ref']=ref('Intake');self.reject(value,'REF_MISSING')
        value=packet_with_views();value['payload']['review_state_at_capture']['context_hash']='0'*64;self.reject(value,'REF_HASH_MISMATCH')
        value=fixtures()['ReviewPacket'];value['H']['creator_label']='person';self.reject(value,'PROVENANCE_MISMATCH')

    def test_redacted_mechanical_leaf_whole_known_and_omission_only(self):
        for valid in ('title','title.state','title.value','published_at','rights_note.reason'):
            value=fixtures()['ReviewPacket'];p=value['payload'];p['omissions']=[{
                'source_ref':ref('SourceItem'),'field_path':valid,'reason_code':'NOT_SELECTED'}]
            r.validate_si_record(value)  # Whole Known or scalar; existence still unknown.
        for invalid in ('chapters','chapters[0]','chapters[0].claim_refs','angle_ref'):
            value=fixtures()['ReviewPacket'];value['payload']['omissions']=[{
                'source_ref':ref('CreativeAlternative'),'field_path':invalid,'reason_code':'NOT_SELECTED'}]
            self.reject(value,'PRIVACY_BLOCKED')
        value=packet_with_views();value['payload']['omissions'].append({
            'source_ref':ref('StoryIdea'),'field_path':'title','reason_code':'NOT_SELECTED'})
        self.reject(value,'PRIVACY_BLOCKED')


if __name__=='__main__':unittest.main()
