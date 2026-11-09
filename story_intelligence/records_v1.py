"""Pure local SI/1 record schemas and byte identity (original + R1/R1a/R1b).

No resolver, operation execution, privacy authorization or authoritative writes.
Schema field order is also the R1b path-order vocabulary; arrays are never sorted.
"""
from copy import deepcopy
from datetime import datetime
import re

from .codec_v1 import canonical_si_json, canonical_si_sha256
from .model_v1 import (SIValidationError, validate_header, validate_si_ref,
                       validate_eref)

__all__ = ['validate_si_record', 'si_record_ref', 'validate_si_record_ref']


def _enum(*values): return ('enum', values)
def _int(low, high=None): return ('int', low, high)
def _list(item): return ('list', item)
def _known(item): return ('known', item)
def _null(item): return ('nullable', item)
def _obj(**fields): return ('object', fields)
def _ref(*types): return ('ref', types)
def _eref(*kinds): return ('eref', kinds)

_TEXT, _HASH, _UTC, _BOOL = ('text',), ('hash',), ('utc',), ('bool',)
_POS = _int(1)
_LOCALE = _enum('ru', 'uk')
_CONFIDENCE = _obj(level=_enum('LOW', 'MEDIUM', 'HIGH', 'UNKNOWN'), basis=_TEXT)
_CODES = _enum('TYPE', 'UNKNOWN_FIELD', 'MISSING_FIELD', 'VERSION_UNSUPPORTED',
    'LIMIT', 'REF_MISSING', 'REF_HASH_MISMATCH', 'REF_TYPE_MISMATCH',
    'DEPENDENCY_CYCLE', 'LOCALE_MISMATCH', 'INPUT_STALE', 'EVIDENCE_NEEDED',
    'CENTRAL_CLAIM_UNSUPPORTED', 'RIGHTS_BLOCKED', 'DUPLICATE_REVIEW_NEEDED',
    'HOOK_FACT_CONFLICT', 'CAPABILITY_BLOCKED', 'UNAVAILABLE_OFFLINE',
    'HANDOFF_ADAPTER_UNAVAILABLE', 'REQUEST_CONFLICT', 'PROVENANCE_MISMATCH',
    'SELECTION_CONFLICT', 'PRIVACY_REVIEW_REQUIRED', 'PRIVACY_BLOCKED',
    'REDACTED_CONTEXT_INCOMPLETE', 'RECORD_UNAVAILABLE')
_ELIGIBILITY_STATES = _enum('BLOCKED', 'NEEDS_INPUT', 'NEEDS_RESEARCH',
    'REVIEW_DUPLICATE', 'ELIGIBLE_FOR_CREATIVE')
_CONTEXT = _obj(context_version=_int(1, 1), active_input_refs=_list(_ref()),
    selection_head_refs=_list(_ref('Selection')), editorial_snapshot_sha256=_known(_HASH))
_PROVIDER = _obj(id=_known(_TEXT), version=_known(_TEXT), model_id=_known(_TEXT),
    model_version=_known(_TEXT), config_digest=_known(_HASH))
_CRITERION = _obj(key=_TEXT, description=_TEXT, weight_percent=_int(0, 100),
    min=_int(0, 0), max=_int(5, 5), direction=_enum('HIGH_IS_BETTER'))
_RATING = _obj(criterion_key=_TEXT, value=_known(_int(0, 5)),
    basis_refs=_list(_ref()), explanation=_TEXT, confidence=_CONFIDENCE)
_PORTFOLIO = _obj(story_ref=_ref('StoryIdea', 'ProductionBrief'), published_title=_TEXT,
    published_locator=_known(_TEXT), published_at=_known(_UTC), angle_notes=_TEXT,
    basis_ref=_ref('Intake', 'SourceItem'))
_CHAPTER = _obj(heading=_TEXT, purpose=_TEXT, claim_refs=_list(_ref('ClaimItem')),
    target_seconds=_POS)
_PRODUCTION = _obj(output_preset=_enum('VERTICAL_720x1280', 'HORIZONTAL_1280x720'),
    script_locale=_LOCALE, narration_locale=_LOCALE, subtitle_locale=_LOCALE,
    tts=_enum('LOCAL_WAV', 'OPTIONAL_SILERO'), asr=_enum('NONE', 'FUTURE_OPTIONAL'),
    editing=_enum('LOCAL_STILLS_FFMPEG_PLAN'), voice_ref=_known(_TEXT),
    resource_budget=_known(_TEXT), cpu_fallback=_TEXT, optional_provider_notes=_list(_TEXT))
_SCOPE = _obj(purpose=_enum('CREATIVE_CHOICE', 'BRIEF_REVIEW'), idea_ref=_ref('StoryIdea'),
    audience_ref=_ref('AudienceHypothesis'), channel_ref=_ref('ChannelContext'))
_REVIEW = _obj(projection_version=_int(1, 1), context_hash=_HASH,
    evaluation_ref=_ref('EvaluationReport'), creative_ref=_null(_ref('CreativeAlternative')),
    brief_ref=_null(_ref('ProductionBrief')), selection_head_refs=_list(_ref('Selection')),
    currentness=_enum('CURRENT', 'STALE', 'INVALID'),
    review_state=_enum('BLOCKED', 'NEEDS_INPUT', 'NEEDS_RESEARCH', 'REVIEW_DUPLICATE',
        'REVISE_CREATIVE', 'AWAITING_CREATIVE', 'AWAITING_CREATIVE_SELECTION',
        'AWAITING_BRIEF', 'AWAITING_BRIEF_SELECTION', 'READY_FOR_BRIEF_REVIEW',
        'CHANGES_REQUESTED', 'WITHDRAWN'), reason_codes=_list(_CODES),
    editorial_approval_state=_enum('NOT_EVALUATED'))
_GRANT = _obj(source_ref=_ref(), field_path=_TEXT, value_sha256=_HASH)
_VIEW = _obj(field_path=_TEXT, kind=_enum('TEXT', 'STATE', 'REDACTED'), text=_null(_TEXT))
_OMISSION = _obj(source_ref=_ref(), field_path=_TEXT,
    reason_code=_enum('PRIVATE_FIELD', 'NOT_SELECTED'))

_SCHEMAS = {
    'Intake': _obj(input_kind=_enum('TOPIC', 'URL_METADATA', 'LOCAL_METADATA'),
        raw_input=_TEXT, locale=_LOCALE, supplied_source_refs=_list(_ref('SourceItem')),
        user_goal=_known(_TEXT)),
    'StoryIdea': _obj(intake_ref=_ref('Intake'), title=_TEXT, summary=_TEXT,
        viewer_question=_TEXT, source_refs=_known(_list(_ref('SourceItem'))),
        candidate_binding=_null(_eref('candidate'))),
    'SourceItem': _obj(source_kind=_enum('URL', 'LOCAL'), original_locator=_TEXT,
        title=_known(_TEXT), author=_known(_TEXT), publisher=_known(_TEXT),
        published_at=_known(_UTC), captured_at=_known(_UTC), material_sha256=_known(_HASH),
        editorial_ref=_null(_eref('source')), rights_note=_known(_TEXT),
        freshness_requirement=_known(_TEXT)),
    'ClaimItem': _obj(statement=_TEXT, claim_kind=_enum('factual', 'interpretation', 'fictional'),
        materiality=_enum('CENTRAL', 'SUPPORTING', 'CONTEXT'), evidence_expectation=_TEXT,
        editorial_ref=_null(_eref('claim'))),
    'EvidenceItem': _obj(claim_ref=_ref('ClaimItem'), source_ref=_ref('SourceItem'),
        relation=_enum('supports', 'contradicts', 'context', 'insufficient'),
        locator=_known(_TEXT), explanation=_TEXT),
    'ClaimCheck': _obj(claim_ref=_ref('ClaimItem'), evidence_refs=_known(_list(_ref('EvidenceItem'))),
        state=_enum('unreviewed', 'supported', 'disputed', 'unverified', 'qualified', 'removed'),
        qualification=_null(_TEXT), reviewer_label=_null(_TEXT), reviewed_at=_null(_UTC),
        reason=_null(_TEXT)),
    'AudienceHypothesis': _obj(locale=_LOCALE, region=_known(_TEXT), knowledge_level=_known(_TEXT),
        motivation=_known(_TEXT), interests=_known(_list(_TEXT)), age_range=_known(_TEXT),
        basis_refs=_list(_ref()), assumptions=_list(_TEXT)),
    'ChannelContext': _obj(channel_alias=_TEXT, purpose=_TEXT, audience_ref=_ref('AudienceHypothesis'),
        constraints=_list(_TEXT), portfolio=_known(_list(_PORTFOLIO)), analytics=_known(_TEXT),
        capability_notes=_known(_TEXT)),
    'Angle': _obj(idea_ref=_ref('StoryIdea'), audience_ref=_ref('AudienceHypothesis'), question=_TEXT,
        thesis=_TEXT, claim_refs=_list(_ref('ClaimItem')), distinction=_TEXT, limitations=_list(_TEXT)),
    'Rubric': _obj(method_id=_TEXT, method_version=_TEXT, criteria=_list(_CRITERION),
        missing_policy=_enum('ALL_REQUIRED'), blocker_policy_version=_TEXT),
    'RunRecord': _obj(stage=_enum('DISCOVERY', 'EVALUATION', 'CREATIVE', 'BRIEF_ASSEMBLY',
        'PACKET_EXPORT', 'REVISION'), method_id=_TEXT, method_version=_TEXT,
        request_payload_sha256=_HASH, semantic_input_refs=_list(_ref()), input_snapshot=_list(_ref()),
        context_snapshot=_CONTEXT, editorial_snapshot_sha256=_known(_HASH),
        rubric_ref=_null(_ref('Rubric')), provider=_null(_PROVIDER), started_at=_UTC,
        finished_at=_UTC, confidence=_CONFIDENCE, fresh_trends=_known(_TEXT), caveats=_list(_TEXT)),
    'EvaluationReport': _obj(idea_ref=_ref('StoryIdea'), angle_ref=_ref('Angle'),
        audience_ref=_ref('AudienceHypothesis'), channel_ref=_ref('ChannelContext'),
        rubric_ref=_ref('Rubric'), run_ref=_ref('RunRecord'), ratings=_list(_RATING),
        risk_refs=_list(_ref('Risk')), eligibility=_obj(state=_ELIGIBILITY_STATES,
        reason_codes=_list(_CODES)), aggregate_tenths=_known(_int(0, 1000)), caveats=_list(_TEXT)),
    'CreativeAlternative': _obj(angle_ref=_ref('Angle'), run_ref=_ref('RunRecord'),
        hook_strategy=_enum('QUESTION', 'HUMAN_STAKES', 'COUNTERINTUITIVE'), hook_text=_TEXT,
        hook_claim_refs=_list(_ref('ClaimItem')), title_options=_list(_TEXT), thumbnail_notes=_TEXT,
        chapters=_list(_CHAPTER), retention_0_30=_TEXT, style_constraints=_list(_TEXT),
        omitted_strategy_reason=_null(_TEXT)),
    'VisualRequirement': _obj(chapter_index=_POS, role=_enum('REQUIRED', 'LOCAL', 'OPTIONAL'),
        description=_TEXT, acquisition=_enum('LOCAL_CREATE', 'USER_SUPPLIED', 'TO_SOURCE'),
        source_refs=_list(_ref('SourceItem')), material_sha256=_known(_HASH),
        rights_state=_enum('UNKNOWN', 'NEEDS_REVIEW', 'DOCUMENTED'), intended_use=_TEXT,
        licence_basis=_known(_TEXT), effort=_known(_enum('LOW', 'MEDIUM', 'HIGH')),
        fallback=_known(_TEXT), asset_ref=_null(_eref('asset'))),
    'Risk': _obj(category=_enum('SCIENTIFIC', 'LEGAL', 'ETHICAL', 'REPUTATIONAL', 'PRODUCTION', 'MARKET'),
        severity=_enum('LOW', 'MEDIUM', 'HIGH', 'CRITICAL'), blocking=_BOOL, basis_refs=_list(_ref()),
        description=_TEXT, mitigation=_TEXT, resolution=_enum('OPEN', 'MITIGATED', 'UNRESOLVED'),
        resolution_basis_refs=_list(_ref()), owner_role=_TEXT),
    'ProductionBrief': _obj(idea_ref=_ref('StoryIdea'), audience_ref=_ref('AudienceHypothesis'),
        channel_ref=_ref('ChannelContext'), angle_ref=_ref('Angle'), evaluation_ref=_ref('EvaluationReport'),
        creative_ref=_ref('CreativeAlternative'), locale=_LOCALE,
        content_mode=_enum('factual', 'fictional', 'hybrid'), intended_use=_known(_TEXT), promise=_TEXT,
        duration_min_s=_POS, duration_max_s=_POS, intensity=_enum('CALM', 'BALANCED', 'DYNAMIC'),
        source_refs=_list(_ref('SourceItem')), claim_refs=_list(_ref('ClaimItem')),
        claim_check_refs=_list(_ref('ClaimCheck')), visual_refs=_list(_ref('VisualRequirement')),
        risk_refs=_list(_ref('Risk')), required_reviews=_list(_TEXT), must_avoid=_list(_TEXT),
        profile_ref=_null(_eref('genre_profile')), production=_PRODUCTION,
        workflow_state=_enum('DRAFT', 'IN_REVIEW', 'WITHDRAWN'), unresolved=_list(_TEXT),
        creative_selection_ref=_null(_ref('Selection'))),
    'Selection': _obj(scope=_SCOPE, target_ref=_ref('CreativeAlternative', 'ProductionBrief'),
        choice=_enum('SELECT', 'REQUEST_CHANGES', 'WITHDRAW'), selector_label=_TEXT, reason=_TEXT),
    'ReviewPacket': _obj(format_version=_enum('si-review-packet/1-r1'), purpose=_enum('DISCUSSION_ONLY'),
        brief_ref=_ref('ProductionBrief'), context_snapshot=_CONTEXT, source_closure_refs=_list(_ref()),
        existing_editorial_refs=_list(_eref()), source_snapshot_digest=_HASH,
        redaction_profile=_enum('si-packet-redact/1'), privacy_grant=_obj(
            reviewed_snapshot_digest=_HASH, allowed_text_fields=_list(_GRANT), confirmed=('true',)),
        display_items=_list(_obj(source_ref=_ref(), fields=_list(_VIEW))),
        omissions=_list(_OMISSION), unresolved=_list(_CODES), review_state_at_capture=_REVIEW),
}


def _fail(code, path, message):
    raise SIValidationError(code, path, message)


def _external(fn, value, path):
    try:
        return fn(value)
    except SIValidationError as error:
        raise SIValidationError(error.code, path + error.path[1:], str(error)) from error


def _remember_ref(value, editorial, path, seen):
    label, digest = ('kind', 'content_hash') if editorial else ('type', 'sha256')
    key = ('E' if editorial else 'SI', value[label], value['id'], value['revision'])
    if key in seen and seen[key] != value[digest]:
        _fail('REF_HASH_MISMATCH', path + '.' + digest, 'Conflicting hashes for one locally declared reference identity')
    seen[key] = value[digest]


def _check(value, schema, path, seen):
    tag = schema[0]
    if tag == 'object':
        if type(value) is not dict: _fail('TYPE', path, 'Expected object')
        fields = schema[1]
        for key in value:
            if key not in fields: _fail('UNKNOWN_FIELD', path + '.' + key, 'Unknown field')
        for key, child in fields.items():
            if key not in value: _fail('MISSING_FIELD', path + '.' + key, 'Required field')
            _check(value[key], child, path + '.' + key, seen)
    elif tag == 'list':
        if type(value) is not list: _fail('TYPE', path, 'Expected list')
        for i, child in enumerate(value): _check(child, schema[1], f'{path}[{i}]', seen)
    elif tag == 'nullable':
        if value is not None: _check(value, schema[1], path, seen)
    elif tag == 'known':
        if type(value) is not dict: _fail('TYPE', path, 'Expected Known union')
        if 'state' not in value: _fail('MISSING_FIELD', path + '.state', 'Required state')
        if value['state'] == 'KNOWN': _check(value, _obj(state=_enum('KNOWN'), value=schema[1]), path, seen)
        elif value['state'] == 'UNKNOWN': _check(value, _obj(state=_enum('UNKNOWN'), reason=_TEXT), path, seen)
        else: _fail('TYPE', path + '.state', 'Invalid Known state')
    elif tag in ('ref', 'eref'):
        _external(validate_si_ref if tag == 'ref' else validate_eref, value, path)
        _remember_ref(value, tag == 'eref', path, seen)
        key = 'type' if tag == 'ref' else 'kind'
        if schema[1] and value[key] not in schema[1]:
            _fail('REF_TYPE_MISMATCH', path + '.' + key, 'Wrong reference type')
    elif tag == 'int':
        if type(value) is not int or value < schema[1] or (schema[2] is not None and value > schema[2]):
            _fail('TYPE', path, 'Integer outside declared range (bool forbidden)')
    elif tag == 'enum':
        if type(value) is not str or value not in schema[1]: _fail('TYPE', path, 'Unknown enum')
    elif tag == 'text':
        if type(value) is not str or not value: _fail('TYPE', path, 'Expected nonempty Text')
    elif tag == 'hash':
        if type(value) is not str or re.fullmatch('[0-9a-f]{64}', value) is None:
            _fail('TYPE', path, 'Expected lowercase SHA-256')
    elif tag == 'utc':
        if type(value) is not str or re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z', value) is None:
            _fail('TYPE', path, 'Expected UTC seconds')
        try: datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError: _fail('TYPE', path, 'Invalid calendar date')
    elif tag == 'bool':
        if type(value) is not bool: _fail('TYPE', path, 'Expected bool')
    elif tag == 'true':
        if value is not True: _fail('PRIVACY_REVIEW_REQUIRED', path, 'Explicit true required')
    else: raise AssertionError('Internal schema tag')


def _ref_key(ref): return (ref['type'], ref['id'], ref['revision'], ref['sha256'])


def _manifest(refs, path):
    keys = [_ref_key(r) for r in refs]
    if keys != sorted(set(keys)):
        _fail('TYPE', path, 'Expected unique canonical manifest order')
    identities = [(r['type'], r['id'], r['revision']) for r in refs]
    if len(set(identities)) != len(identities):
        _fail('REF_HASH_MISMATCH', path, 'Conflicting hashes for one identity')


def _context(context, path):
    identities = [(r['type'], r['id']) for r in context['active_input_refs']]
    if len(set(identities)) != len(identities): _fail('TYPE', path + '.active_input_refs', 'Ambiguous active revision')
    for i, ref in enumerate(context['active_input_refs']):
        if ref['type'] in ('RunRecord', 'Selection', 'ReviewPacket'):
            _fail('REF_TYPE_MISMATCH', f'{path}.active_input_refs[{i}].type', 'Not a domain active input')
    heads = [(r['type'], r['id']) for r in context['selection_head_refs']]
    if len(set(heads)) != len(heads): _fail('SELECTION_CONFLICT', path + '.selection_head_refs', 'Duplicate head')


_METHODS = {'DISCOVERY':'si.discover-local', 'EVALUATION':'si.evaluate',
    'CREATIVE':'si.creative-templates', 'BRIEF_ASSEMBLY':'si.brief-assembly',
    'PACKET_EXPORT':'si.review-packet', 'REVISION':'si.human-revision'}


def _local(header, p):
    kind, origin = header['type'], header['origin']
    base = '$.payload'
    if origin['mode'] == 'HUMAN_EDIT' and (not header['input_refs'] or header['input_refs'][0] != header['previous']):
        _fail('PROVENANCE_MISMATCH', '$.H.input_refs', 'Human edit roots must start with exact previous')
    if kind == 'ClaimCheck':
        for key in ('reviewer_label', 'reviewed_at', 'reason'):
            if (p[key] is None) != (p['state'] == 'unreviewed'):
                _fail('TYPE', base + '.' + key, 'Review metadata inconsistent with state')
        if (p['qualification'] is not None) != (p['state'] == 'qualified'):
            _fail('TYPE', base + '.qualification', 'Qualification only and required for qualified')
        if p['state'] in ('supported', 'qualified') and (p['evidence_refs']['state'] != 'KNOWN' or not p['evidence_refs']['value']):
            _fail('EVIDENCE_NEEDED', base + '.evidence_refs', 'Nonempty known evidence required, not verified here')
    elif kind == 'Rubric':
        keys = [c['key'] for c in p['criteria']]
        if len(set(keys)) != len(keys): _fail('TYPE', base + '.criteria', 'Duplicate criterion key')
        if sum(c['weight_percent'] for c in p['criteria']) != 100:
            _fail('TYPE', base + '.criteria', 'Weights must sum to 100')
    elif kind == 'RunRecord':
        if p['method_id'] != _METHODS[p['stage']] or p['method_version'] != '1-r1':
            _fail('PROVENANCE_MISMATCH', base + '.method_id', 'Stage/method/version mismatch')
        if p['provider'] is not None: _fail('PROVENANCE_MISMATCH', base + '.provider', 'Offline V1 provider must be null')
        if p['stage'] in ('EVALUATION', 'BRIEF_ASSEMBLY', 'PACKET_EXPORT') and p['rubric_ref'] is None:
            _fail('MISSING_FIELD', base + '.rubric_ref', 'Stage requires exact rubric ref')
        _manifest(p['input_snapshot'], base + '.input_snapshot')
        _context(p['context_snapshot'], base + '.context_snapshot')
        snapshot_keys = {_ref_key(ref) for ref in p['input_snapshot']}
        roots = p['semantic_input_refs'] + p['context_snapshot']['active_input_refs'] + p['context_snapshot']['selection_head_refs']
        if any(_ref_key(ref) not in snapshot_keys for ref in roots):
            _fail('REF_MISSING', base + '.input_snapshot', 'Declared roots missing from run snapshot')
        if any(ref['type'] == header['type'] and ref['id'] == header['id'] for ref in p['input_snapshot']):
            _fail('DEPENDENCY_CYCLE', base + '.input_snapshot', 'Run cannot include itself as input')
        if header['input_refs'] != p['input_snapshot']:
            _fail('PROVENANCE_MISMATCH', '$.H.input_refs', 'Run input refs must equal input snapshot')
        if p['editorial_snapshot_sha256'] != p['context_snapshot']['editorial_snapshot_sha256']:
            _fail('PROVENANCE_MISMATCH', base + '.editorial_snapshot_sha256', 'Context snapshot mismatch')
    elif kind == 'EvaluationReport':
        if p['run_ref'] != origin['run_ref']:
            _fail('PROVENANCE_MISMATCH', base + '.run_ref', 'Evaluation run refs differ')
        keys = [r['criterion_key'] for r in p['ratings']]
        if len(set(keys)) != len(keys): _fail('TYPE', base + '.ratings', 'Duplicate rating key')
        if any(r['value']['state'] == 'UNKNOWN' for r in p['ratings']) and p['aggregate_tenths']['state'] != 'UNKNOWN':
            _fail('TYPE', base + '.aggregate_tenths', 'UNKNOWN rating cannot produce known aggregate')
    elif kind == 'CreativeAlternative':
        if header['revision'] == 1 and p['run_ref'] != origin['run_ref']:
            _fail('PROVENANCE_MISMATCH', base + '.run_ref', 'Initial creative run refs differ')
        if origin['mode'] == 'HUMAN_EDIT' and p['run_ref'] == origin['run_ref']:
            _fail('PROVENANCE_MISMATCH', base + '.run_ref', 'Original creative run cannot be current revision run')
    elif kind == 'VisualRequirement':
        if p['rights_state'] == 'DOCUMENTED' and p['licence_basis']['state'] != 'KNOWN':
            _fail('RIGHTS_BLOCKED', base + '.licence_basis', 'DOCUMENTED requires supplied basis, not a verified rights grant')
    elif kind == 'Risk':
        if p['resolution'] == 'MITIGATED' and not p['resolution_basis_refs']:
            _fail('TYPE', base + '.resolution_basis_refs', 'MITIGATED requires recorded basis')
    elif kind == 'ProductionBrief':
        selection = p['creative_selection_ref']
        if selection is None and p['workflow_state'] != 'DRAFT':
            _fail('MISSING_FIELD', base + '.creative_selection_ref', 'Null creative selection is allowed for DRAFT only')
        if selection is not None and selection not in header['input_refs']:
            _fail('PROVENANCE_MISMATCH', '$.H.input_refs', 'Used creative Selection must be an explicit input')
        if p['duration_min_s'] > p['duration_max_s']: _fail('TYPE', base + '.duration_max_s', 'Duration bounds reversed')
        for key in ('script_locale', 'narration_locale', 'subtitle_locale'):
            if p['production'][key] != p['locale']:
                _fail('LOCALE_MISMATCH', base + '.production.' + key, 'Brief language mismatch')
    elif kind == 'Selection':
        expected = 'CreativeAlternative' if p['scope']['purpose'] == 'CREATIVE_CHOICE' else 'ProductionBrief'
        if p['target_ref']['type'] != expected:
            _fail('REF_TYPE_MISMATCH', base + '.target_ref.type', 'Target differs from selection purpose')
    elif kind == 'ReviewPacket':
        _packet(header, p)


_TEXT_PATHS = {
    'StoryIdea': ('title', 'summary', 'viewer_question'), 'SourceItem': ('title.value',),
    'ClaimItem': ('statement',), 'ClaimCheck': ('qualification',),
    'Angle': ('question', 'thesis', 'distinction'),
    'CreativeAlternative': ('hook_text', 'title_options[]', 'thumbnail_notes',
        'chapters[].heading', 'chapters[].purpose', 'retention_0_30'),
    'VisualRequirement': ('description', 'fallback.value'), 'Risk': ('description', 'mitigation'),
    'ProductionBrief': ('promise', 'must_avoid[]', 'required_reviews[]')}
_STATE_PATHS = {
    'ClaimCheck': {'state': _SCHEMAS['ClaimCheck'][1]['state']},
    'Risk': {k:_SCHEMAS['Risk'][1][k] for k in ('category', 'severity', 'blocking', 'resolution')},
    'VisualRequirement': {k:_SCHEMAS['VisualRequirement'][1][k] for k in ('role', 'rights_state')},
    'ProductionBrief': {k:_SCHEMAS['ProductionBrief'][1][k] for k in ('locale', 'content_mode', 'workflow_state')},
    'EvaluationReport': {'eligibility.state': _ELIGIBILITY_STATES}}
_SEGMENT = re.compile(r'([a-z][a-z0-9_]*)(?:\[(0|[1-9][0-9]*)\])?\Z')
_REF_FIELDS = _obj(type=_TEXT, id=_TEXT, revision=_POS, sha256=_HASH)
_EREF_FIELDS = _obj(kind=_TEXT, id=_TEXT, revision=_POS, content_hash=_HASH)


def _path(kind, field, view_kind, path):
    """Return schema order rank without resolving any source value/index."""
    parts, canonical, rank = field.split('.'), [], []
    schema = _SCHEMAS[kind]
    if kind == 'ReviewPacket' and field in ('review_state_at_capture.review_state', 'review_state_at_capture.currentness'):
        _fail('PRIVACY_BLOCKED', path, 'Projection-only fields cannot be source paths')
    for part in parts:
        match = _SEGMENT.fullmatch(part)
        if match is None: _fail('PRIVACY_BLOCKED', path, 'Noncanonical field path')
        key, index = match.groups()
        while schema[0] == 'nullable': schema = schema[1]
        if schema[0] == 'known': schema = _obj(state=_enum('KNOWN', 'UNKNOWN'), value=schema[1], reason=_TEXT)
        if schema[0] == 'ref': schema = _REF_FIELDS
        if schema[0] == 'eref': schema = _EREF_FIELDS
        if schema[0] != 'object' or key not in schema[1]:
            _fail('PRIVACY_BLOCKED', path, 'Path not declared by source payload schema')
        rank.append(list(schema[1]).index(key))
        schema = schema[1][key]
        canonical.append(key)
        if index is not None:
            while schema[0] == 'nullable': schema = schema[1]
            if schema[0] != 'list': _fail('PRIVACY_BLOCKED', path, 'Index on non-array')
            # Numeric ordering without decimal-to-int guards or huge integer allocation.
            rank.append((len(index), index))
            canonical[-1] += '[]'
            schema = schema[1]
    while schema[0] == 'nullable': schema = schema[1]
    if schema[0] in ('object', 'list', 'ref', 'eref'):
        _fail('PRIVACY_BLOCKED', path, 'Only scalar leaf or whole Known may be withheld')
    template = '.'.join(canonical)
    if view_kind == 'TEXT' and template not in _TEXT_PATHS.get(kind, ()):
        _fail('PRIVACY_BLOCKED', path, 'Field not in TEXT whitelist')
    if view_kind == 'STATE' and field not in _STATE_PATHS.get(kind, {}):
        _fail('PRIVACY_BLOCKED', path, 'Field not in STATE whitelist')
    return tuple(rank)


def _packet(header, p):
    base = '$.payload'
    _context(p['context_snapshot'], base + '.context_snapshot')
    refs = p['source_closure_refs']
    _manifest(refs, base + '.source_closure_refs')
    manifest = {_ref_key(r):i for i, r in enumerate(refs)}
    for i, r in enumerate(refs):
        if (r['type'], r['id']) in ((header['type'], header['id']),
                (header['origin']['run_ref']['type'], header['origin']['run_ref']['id'])):
            _fail('DEPENDENCY_CYCLE', f'{base}.source_closure_refs[{i}]', 'Packet/export Run excluded from source closure')
    roots = [p['brief_ref']] + p['context_snapshot']['active_input_refs'] + p['context_snapshot']['selection_head_refs']
    if any(_ref_key(r) not in manifest for r in roots):
        _fail('REF_MISSING', base + '.source_closure_refs', 'Explicit packet roots missing from manifest')
    snapshot = {k:p[k] for k in ('context_snapshot', 'source_closure_refs', 'existing_editorial_refs')}
    if canonical_si_sha256(snapshot) != p['source_snapshot_digest']:
        _fail('REF_HASH_MISMATCH', base + '.source_snapshot_digest', 'Snapshot digest differs from local manifest')
    if p['privacy_grant']['reviewed_snapshot_digest'] != p['source_snapshot_digest']:
        _fail('PRIVACY_REVIEW_REQUIRED', base + '.privacy_grant.reviewed_snapshot_digest', 'Grant snapshot mismatch')
    review = p['review_state_at_capture']
    if canonical_si_sha256(p['context_snapshot']) != review['context_hash']:
        _fail('REF_HASH_MISMATCH', base + '.review_state_at_capture.context_hash', 'Captured context digest mismatch')
    if review['selection_head_refs'] != p['context_snapshot']['selection_head_refs']:
        _fail('SELECTION_CONFLICT', base + '.review_state_at_capture.selection_head_refs', 'Capture heads differ from context')
    if review['brief_ref'] != p['brief_ref']:
        _fail('PROVENANCE_MISMATCH', base + '.review_state_at_capture.brief_ref', 'Captured Brief differs')
    if review['creative_ref'] is None:
        _fail('PROVENANCE_MISMATCH', base + '.review_state_at_capture.creative_ref', 'Packet capture requires Creative ref')
    capture_refs = [review['evaluation_ref']] + [review[key] for key in ('creative_ref', 'brief_ref') if review[key] is not None] + review['selection_head_refs']
    if any(_ref_key(ref) not in manifest for ref in capture_refs):
        _fail('REF_MISSING', base + '.review_state_at_capture', 'Capture references absent from source manifest')
    if review['currentness'] != 'CURRENT' and not review['reason_codes']:
        _fail('TYPE', base + '.review_state_at_capture.reason_codes', 'Noncurrent projection requires diagnostics')

    def position(source, field, view_kind, path):
        key = _ref_key(source)
        if key not in manifest: _fail('REF_MISSING', path, 'Source absent from packet manifest')
        return (manifest[key], _path(source['type'], field, view_kind, path))

    def ordered_unique(positions, path):
        if positions != sorted(set(positions)):
            _fail('TYPE', path, 'Duplicate or noncanonical schema/index order')

    grants, grant_order = {}, []
    for i, grant in enumerate(p['privacy_grant']['allowed_text_fields']):
        path = f'{base}.privacy_grant.allowed_text_fields[{i}]'
        source, field = grant['source_ref'], grant['field_path']
        pos = position(source, field, 'TEXT', path + '.field_path')
        key = (_ref_key(source), field)
        if key in grants: _fail('TYPE', path, 'Duplicate FieldGrant')
        grants[key] = grant['value_sha256']; grant_order.append(pos)
    ordered_unique(grant_order, base + '.privacy_grant.allowed_text_fields')
    displayed, text_keys, redacted_keys, item_order = {}, set(), set(), []
    for i, item in enumerate(p['display_items']):
        source = item['source_ref']; source_key = _ref_key(source)
        if source_key not in manifest: _fail('REF_MISSING', f'{base}.display_items[{i}].source_ref', 'Source absent')
        item_order.append(manifest[source_key]); field_order = []
        for j, field in enumerate(item['fields']):
            path = f'{base}.display_items[{i}].fields[{j}]'
            kind, name, text = field['kind'], field['field_path'], field['text']
            field_order.append(position(source, name, kind, path + '.field_path')[1])
            key = (source_key, name)
            if key in displayed: _fail('TYPE', path, 'Duplicate field view')
            displayed[key] = kind
            if kind == 'REDACTED':
                if text is not None: _fail('PRIVACY_BLOCKED', path + '.text', 'Redacted text must be null')
                redacted_keys.add(key)
            elif text is None: _fail('TYPE', path + '.text', 'Visible field requires text')
            elif kind == 'TEXT':
                if key not in grants: _fail('PRIVACY_REVIEW_REQUIRED', path, 'Missing exact text grant')
                if canonical_si_sha256(text) != grants[key]:
                    _fail('REF_HASH_MISMATCH', path + '.text', 'Displayed text inconsistent with grant digest (source unresolved)')
                text_keys.add(key)
            else:
                state_schema = _STATE_PATHS[source['type']][name]
                values = ('true', 'false') if state_schema[0] == 'bool' else state_schema[1]
                if text not in values: _fail('TYPE', path + '.text', 'Invalid STATE scalar spelling')
        ordered_unique(field_order, f'{base}.display_items[{i}].fields')
    ordered_unique(item_order, base + '.display_items')
    if set(grants) != text_keys:
        _fail('PRIVACY_BLOCKED', base + '.privacy_grant.allowed_text_fields', 'Grant does not correspond to selected TEXT')
    omissions, omission_order = set(), []
    for i, omission in enumerate(p['omissions']):
        path = f'{base}.omissions[{i}]'
        source, name = omission['source_ref'], omission['field_path']
        omission_order.append(position(source, name, 'REDACTED', path + '.field_path'))
        key = (_ref_key(source), name)
        if key in omissions: _fail('TYPE', path, 'Duplicate omission')
        if key in displayed and displayed[key] != 'REDACTED':
            _fail('PRIVACY_BLOCKED', path, 'Visible field also omitted')
        omissions.add(key)
    ordered_unique(omission_order, base + '.omissions')
    if not redacted_keys <= omissions:
        _fail('MISSING_FIELD', base + '.omissions', 'Redacted view requires exact Omission')


def validate_si_record(value):
    """Return detached full typed record copy; all external SIRefs remain unresolved."""
    canonical_si_json(value)  # Accepted SI-E01.1 exact types/Unicode/size/depth.
    if type(value) is not dict: _fail('TYPE', '$', 'Expected {H,payload}')
    for key in value:
        if key not in ('H', 'payload'): _fail('UNKNOWN_FIELD', '$.' + key, 'Unknown record field')
    for key in ('H', 'payload'):
        if key not in value: _fail('MISSING_FIELD', '$.' + key, 'Required record field')
    header = _external(validate_header, value['H'], '$.H')
    seen = {}
    for key in ('previous',):
        if header[key] is not None: _remember_ref(header[key], False, '$.H.' + key, seen)
    if header['origin']['run_ref'] is not None:
        _remember_ref(header['origin']['run_ref'], False, '$.H.origin.run_ref', seen)
    for key, editorial in (('input_refs', False), ('editorial_refs', True)):
        for i, ref in enumerate(header[key]): _remember_ref(ref, editorial, f'$.H.{key}[{i}]', seen)
    _check(value['payload'], _SCHEMAS[header['type']], '$.payload', seen)
    _local(header, value['payload'])
    return deepcopy(value)


def si_record_ref(value):
    """SIRef of validated bytes/shape only, not content truth or authority."""
    record = validate_si_record(value)
    header = record['H']
    return {'type':header['type'], 'id':header['id'], 'revision':header['revision'],
            'sha256':canonical_si_sha256(record)}


def validate_si_record_ref(value, expected_ref):
    """Return a detached expected SIRef after exact local record/ref comparison."""
    actual = si_record_ref(value)
    expected = _external(validate_si_ref, expected_ref, '$.expected_ref')
    for key in ('type', 'id', 'revision', 'sha256'):
        if actual[key] != expected[key]:
            code = 'REF_TYPE_MISMATCH' if key == 'type' else 'REF_HASH_MISMATCH'
            _fail(code, '$.expected_ref.' + key, 'Supplied SIRef differs from validated record bytes')
    return expected
