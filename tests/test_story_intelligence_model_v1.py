"""SI-E01.1 local structure, diagnostics, copy semantics and deferred boundaries."""
import copy
import unittest

from editorial.model import ObjectKind
from story_intelligence import model_v1 as m

ID = '11111111-1111-4111-8111-111111111111'
OTHER_ID = '22222222-2222-4222-8222-222222222222'
HASH = 'a'*64  # Synthetic supplied digest; no claim of resolved record content.
TYPES = ('Intake', 'StoryIdea', 'SourceItem', 'ClaimItem', 'EvidenceItem',
    'ClaimCheck', 'AudienceHypothesis', 'ChannelContext', 'Angle', 'Rubric',
    'RunRecord', 'EvaluationReport', 'CreativeAlternative', 'VisualRequirement',
    'Risk', 'ProductionBrief', 'Selection', 'ReviewPacket')


def ref(kind='Intake', revision=1):
    return {'type':kind,'id':ID,'revision':revision,'sha256':HASH}


def eref(kind='source'):
    return {'kind':kind,'id':ID,'revision':1,'content_hash':HASH}


def origin(mode='MANUAL_INPUT'):
    return {'mode':mode,'run_ref':ref('RunRecord') if mode in
        ('RULE_DERIVED','TEMPLATE_DERIVED','MODEL_DERIVED','HUMAN_EDIT') else None,
        'imported_from':{'state':'UNKNOWN','reason':'Невідомо'} if mode=='USER_IMPORT' else None}


def header(kind='Intake', revision=1):
    mode = {'StoryIdea':'RULE_DERIVED','CreativeAlternative':'TEMPLATE_DERIVED',
        'EvaluationReport':'RULE_DERIVED','ReviewPacket':'RULE_DERIVED',
        'RunRecord':'RUN_METADATA'}.get(kind,'MANUAL_INPUT')
    if revision>1 and kind!='Selection': mode='HUMAN_EDIT'
    return {'si_version':1,'type':kind,'id':ID,'revision':revision,
        'previous':None if revision==1 else ref(kind,revision-1),
        'created_at':'2024-02-29T23:59:59Z',
        'creator_label':{'RunRecord':'SI_ENGINE','ReviewPacket':'SI_EXPORTER'}.get(kind,'Автор ї є і 😀'),
        'origin':origin(mode),'input_refs':[ref('SourceItem'),ref('Intake')],
        'editorial_refs':[eref('source'),eref('candidate')]}


class ModelTests(unittest.TestCase):
    def rejected(self, fn, value, code, path):
        before=copy.deepcopy(value)
        with self.assertRaises(m.SIValidationError) as caught: fn(value)
        self.assertEqual(code,caught.exception.code)
        self.assertEqual(path,caught.exception.path)
        self.assertEqual(before,value)

    def test_all_si_ref_types(self):
        for kind in TYPES:
            with self.subTest(kind=kind):
                value=ref(kind)
                self.assertEqual(value,m.validate_si_ref(value))
                self.assertIsNot(value,m.validate_si_ref(value))
        self.rejected(m.validate_si_ref,ref('Unknown'),'TYPE','$.type')

    def test_editorial_vocabulary_matches_actual_model(self):
        self.assertEqual({'production','genre_profile','candidate','source','claim',
            'script','scene_plan','asset','rights_review'},{kind.value for kind in ObjectKind})
        for kind in ObjectKind:
            self.assertEqual(eref(kind.value),m.validate_eref(eref(kind.value)))
        self.rejected(m.validate_eref,eref('StoryIdea'),'TYPE','$.kind')
        self.rejected(m.validate_si_ref,eref(),'UNKNOWN_FIELD','$.kind')
        self.rejected(m.validate_eref,ref(),'UNKNOWN_FIELD','$.type')

    def test_ref_uuid_and_hash_formats(self):
        for fn,base,digest in ((m.validate_si_ref,ref(),'sha256'),
                              (m.validate_eref,eref(),'content_hash')):
            for bad in ('I1','11111111111141118111111111111111',
                        'AAAAAAAA-AAAA-4AAA-8AAA-AAAAAAAAAAAA','{'+ID+'}',12):
                value={**base,'id':bad}
                self.rejected(fn,value,'TYPE','$.id')
            for bad in ('a'*63,'a'*65,'A'*64,'g'*64,64,None):
                self.rejected(fn,{**base,digest:bad},'TYPE','$.'+digest)
            # Large exact revisions must not be narrowed to float/U64.
            value={**base,'revision':2**80+1}
            self.assertEqual(value,fn(value))

    def test_bool_and_nonpositive_revisions(self):
        for fn,value in ((m.validate_si_ref,ref()),(m.validate_eref,eref()),
                         (m.validate_header,header())):
            for bad in (True,False,0,-1,1.0,'1',None):
                self.rejected(fn,{**value,'revision':bad},'TYPE','$.revision')

    def test_closed_shapes_and_missing_keys(self):
        for fn,value in ((m.validate_si_ref,ref()),(m.validate_eref,eref()),
                         (m.validate_origin,origin()),(m.validate_header,header())):
            self.rejected(fn,{**value,'extra':0},'UNKNOWN_FIELD','$.extra')
            for key in value:
                bad=copy.deepcopy(value);del bad[key]
                with self.subTest(fn=fn.__name__,key=key):
                    self.rejected(fn,bad,'MISSING_FIELD','$.'+key)
            for bad in ([],None,'x'):
                self.rejected(fn,bad,'TYPE','$')

    def test_known_branches_and_no_coercion(self):
        callback_calls=[]
        def boolean(value):
            callback_calls.append(value)
            if type(value) is not bool: raise m.SIValidationError('TYPE','$','bool required')
        known={'state':'KNOWN','value':False}
        self.assertEqual(known,m.validate_known(known,boolean))
        unknown={'state':'UNKNOWN','reason':'Не перевірено'}
        self.assertEqual(unknown,m.validate_known(unknown,boolean))
        self.assertEqual([False],callback_calls)
        self.rejected(lambda v:m.validate_known(v,boolean),
                      {'state':'KNOWN','value':0},'TYPE','$.value')
        # A successful callback validates, it does not replace/normalize T.
        self.assertEqual(known,m.validate_known(known,lambda _:True))

    def test_known_invalid_unions(self):
        fn=lambda v:m.validate_known(v,lambda _:None)
        for value,code,path in [({},'MISSING_FIELD','$.state'),
            ({'state':'MAYBE'},'TYPE','$.state'),
            ({'state':'KNOWN'},'MISSING_FIELD','$.value'),
            ({'state':'UNKNOWN'},'MISSING_FIELD','$.reason'),
            ({'state':'KNOWN','value':None,'reason':'x'},'UNKNOWN_FIELD','$.reason'),
            ({'state':'UNKNOWN','reason':'x','value':0},'UNKNOWN_FIELD','$.value'),
            ({'state':'UNKNOWN','reason':''},'TYPE','$.reason')]:
            self.rejected(fn,value,code,path)
        with self.assertRaises(m.SIValidationError): m.validate_known({'state':'KNOWN','value':1},None)

    def test_known_callback_isolation_and_nested_diagnostic(self):
        value={'state':'KNOWN','value':[{'a':1}]};before=copy.deepcopy(value)
        def mutate(child): child[0]['a']=9
        self.assertEqual(before,m.validate_known(value,mutate))
        self.assertEqual(before,value)
        nested={'state':'KNOWN','value':{**ref(),'revision':False}}
        self.rejected(lambda v:m.validate_known(v,m.validate_si_ref),nested,'TYPE','$.value.revision')

    def test_all_origin_modes(self):
        for mode in ('MANUAL_INPUT','USER_IMPORT','RULE_DERIVED','TEMPLATE_DERIVED',
                     'MODEL_DERIVED','HUMAN_EDIT','RUN_METADATA'):
            value=origin(mode)
            self.assertEqual(value,m.validate_origin(value))
        value=origin('USER_IMPORT');value['imported_from']={'state':'KNOWN','value':'Локальний імпорт'}
        self.assertEqual(value,m.validate_origin(value))

    def test_origin_binding_failures(self):
        self.rejected(m.validate_origin,{**origin(),'mode':'AUTOMATIC'},'TYPE','$.mode')
        for mode in ('RULE_DERIVED','TEMPLATE_DERIVED','MODEL_DERIVED','HUMAN_EDIT'):
            self.rejected(m.validate_origin,{**origin(mode),'run_ref':None},'TYPE','$.run_ref')
            self.rejected(m.validate_origin,{**origin(mode),'run_ref':ref('Intake')},
                          'REF_TYPE_MISMATCH','$.run_ref.type')
        for mode in ('MANUAL_INPUT','USER_IMPORT','RUN_METADATA'):
            self.rejected(m.validate_origin,{**origin(mode),'run_ref':ref('RunRecord')},
                          'PROVENANCE_MISMATCH','$.run_ref')
        self.rejected(m.validate_origin,{**origin(),'imported_from':{'state':'UNKNOWN','reason':'x'}},
                      'PROVENANCE_MISMATCH','$.imported_from')
        self.rejected(m.validate_origin,{**origin('USER_IMPORT'),'imported_from':None},
                      'TYPE','$.imported_from')
        self.rejected(m.validate_origin,{**origin('USER_IMPORT'),
            'imported_from':{'state':'KNOWN','value':0}},'TYPE','$.imported_from.value')

    def test_headers_all_types(self):
        for kind in TYPES:
            with self.subTest(kind=kind):
                value=header(kind)
                self.assertEqual(value,m.validate_header(value))
        for kind in ('StoryIdea','CreativeAlternative','Intake','Selection','ProductionBrief'):
            self.assertEqual(header(kind,2),m.validate_header(header(kind,2)))
        brief=header('ProductionBrief',2);brief['origin']=origin('RULE_DERIVED')
        self.assertEqual(brief,m.validate_header(brief))
        for mode in ('MANUAL_INPUT','USER_IMPORT','RULE_DERIVED'):
            brief=header('ProductionBrief');brief['origin']=origin(mode)
            self.assertEqual(brief,m.validate_header(brief))

    def test_version_and_time(self):
        self.rejected(m.validate_header,{**header(),'si_version':True},'TYPE','$.si_version')
        self.rejected(m.validate_header,{**header(),'si_version':2},'VERSION_UNSUPPORTED','$.si_version')
        for bad in ('2023-02-29T00:00:00Z','2026-11-31T00:00:00Z','0000-01-01T00:00:00Z',
                    '2026-11-09T24:00:00Z','2026-11-09T00:00:60Z','2026-1-09T00:00:00Z',
                    '2026-11-09T00:00:00.000Z','2026-11-09T00:00:00+00:00',None):
            self.rejected(m.validate_header,{**header(),'created_at':bad},'TYPE','$.created_at')
        self.assertEqual('0001-01-01T00:00:00Z',m.validate_header(
            {**header(),'created_at':'0001-01-01T00:00:00Z'})['created_at'])

    def test_previous_chain(self):
        self.rejected(m.validate_header,{**header(),'previous':ref()},'PROVENANCE_MISMATCH','$.previous')
        self.rejected(m.validate_header,{**header(revision=2),'previous':None},'TYPE','$.previous')
        for key,bad in (('type','SourceItem'),('id',OTHER_ID),('revision',2)):
            value=header(revision=2);value['previous'][key]=bad
            self.rejected(m.validate_header,value,'PROVENANCE_MISMATCH','$.previous.'+key)
        value=header(revision=2);value['previous']['sha256']='z'*64
        self.rejected(m.validate_header,value,'TYPE','$.previous.sha256')

    def test_runrecord_local_rules(self):
        value=header('RunRecord');value['creator_label']='user'
        self.rejected(m.validate_header,value,'PROVENANCE_MISMATCH','$.creator_label')
        value=header('RunRecord');value['origin']=origin('MANUAL_INPUT')
        self.rejected(m.validate_header,value,'PROVENANCE_MISMATCH','$.origin.mode')
        value=header('RunRecord',2);value['origin']=origin('RUN_METADATA')
        self.rejected(m.validate_header,value,'PROVENANCE_MISMATCH','$.origin.mode')
        value=header();value['origin']=origin('RUN_METADATA')
        self.rejected(m.validate_header,value,'PROVENANCE_MISMATCH','$.origin.mode')

    def test_packet_technical_label(self):
        value=header('ReviewPacket');value['creator_label']='user'
        self.rejected(m.validate_header,value,'PROVENANCE_MISMATCH','$.creator_label')

    def test_initial_derived_and_human_edit_rules(self):
        for kind in ('StoryIdea','CreativeAlternative'):
            for bad_mode in ('MANUAL_INPUT','USER_IMPORT','HUMAN_EDIT','MODEL_DERIVED'):
                value=header(kind);value['origin']=origin(bad_mode)
                self.rejected(m.validate_header,value,'PROVENANCE_MISMATCH','$.origin.mode')
            value=header(kind,2);value['origin']=origin('RULE_DERIVED')
            self.rejected(m.validate_header,value,'PROVENANCE_MISMATCH','$.origin.mode')
        value=header();value['origin']=origin('HUMAN_EDIT')
        self.rejected(m.validate_header,value,'PROVENANCE_MISMATCH','$.origin.mode')
        for kind in ('EvaluationReport','ReviewPacket'):
            self.rejected(m.validate_header,header(kind,2),'PROVENANCE_MISMATCH','$.origin.mode')

    def test_lists_and_exact_nested_paths(self):
        value=header();value['input_refs'][1]['revision']=False
        self.rejected(m.validate_header,value,'TYPE','$.input_refs[1].revision')
        value=header();value['editorial_refs'][0]['kind']='unknown'
        self.rejected(m.validate_header,value,'TYPE','$.editorial_refs[0].kind')
        for key in ('input_refs','editorial_refs'):
            value=header();value[key]=()
            self.rejected(m.validate_header,value,'TYPE','$.'+key)
        self.rejected(m.validate_header,{**header(),'creator_label':''},'TYPE','$.creator_label')

    def test_copy_and_input_order(self):
        for fn,value in ((m.validate_si_ref,ref()),(m.validate_eref,eref()),
                         (m.validate_origin,origin('USER_IMPORT')),(m.validate_header,header())):
            before=copy.deepcopy(value);result=fn(value)
            self.assertEqual(before,value);self.assertEqual(before,result)
            self.assertIsNot(value,result)
            result.clear();self.assertEqual(before,value)
        value=header();result=m.validate_header(value)
        result['input_refs'][0]['id']=OTHER_ID
        result['origin']['mode']='bad'
        self.assertEqual(header(),value)
        self.assertEqual(['SourceItem','Intake'],[v['type'] for v in value['input_refs']])

    def test_header_is_not_full_record_or_resolution(self):
        value=header('CreativeAlternative')
        self.assertEqual(value,m.validate_header(value))  # No run exists in resolver.
        self.rejected(m.validate_header,{**value,'payload':{}},'UNKNOWN_FIELD','$.payload')
        self.assertFalse(hasattr(m,'validate_record'))
        self.assertFalse(hasattr(m,'record_ref'))

    def test_model_limits_and_exact_plain_types(self):
        class D(dict): pass
        class S(str): pass
        class I(int): pass
        self.rejected(m.validate_si_ref,D(ref()),'TYPE','$')
        self.rejected(m.validate_si_ref,{**ref(),'id':S(ID)},'TYPE','$.id')
        self.rejected(m.validate_si_ref,{**ref(),'revision':I(1)},'TYPE','$.revision')
        self.rejected(m.validate_header,{**header(),'creator_label':'a'*100_001},'LIMIT','$.creator_label')
        self.rejected(m.validate_header,{**header(),'creator_label':'\ud800'},'TYPE','$.creator_label')


if __name__ == '__main__':
    unittest.main()
