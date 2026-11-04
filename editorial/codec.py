"""E01.2.1 strict decoder only; no encoding, hashing, I/O or graph lookup."""
import json
import re
from datetime import datetime
from enum import Enum
from urllib.parse import urlsplit
from uuid import UUID

from . import model as m

__all__ = ('decode_snapshot', 'encode_snapshot', 'DecodeError', 'EncodeError')

MAX_BYTES = 32 * 1024 * 1024
MAX_DEPTH = 64
MAX_ITEMS = 10_000
MAX_TEXT = 100_000


class DecodeError(m.ModelError):
    """Atomic decode failure; violation.field_path is a JSON-style path."""


class EncodeError(m.ModelError):
    """Atomic encode failure; violation.field_path identifies invalid input."""


def _error(path, code, message):
    raise DecodeError(m.Violation(code, path, message))


def _encode_error(path, code, message):
    raise EncodeError(m.Violation(code, path, message))


def _field(path, name):
    return f'{path}.{name}' if re.fullmatch('[A-Za-z_][A-Za-z0-9_]*', name) else f'{path}[{name!r}]'


class _Pairs(tuple):
    """Retain duplicate keys until their full field path is known."""


class _ForbiddenNumber(str):
    pass


def _unicode(value, path):
    if len(value) > MAX_TEXT:
        _error(path, 'LIMIT', 'String exceeds 100000 code points')
    if any(0xD800 <= ord(c) <= 0xDFFF for c in value):
        _error(path, 'UNICODE', 'Unpaired surrogate is not permitted')


def _walk(value, path):
    if isinstance(value, _ForbiddenNumber):
        _error(path, 'NUMBER', 'Floating point, NaN and Infinity are not permitted')
    if isinstance(value, _Pairs):
        result = {}
        for key, child in value:
            key_path = _field(path, key)
            _unicode(key, key_path)
            if key in result:
                _error(key_path, 'DUPLICATE_KEY', 'Duplicate JSON object key')
            result[key] = _walk(child, key_path)
        return result
    if type(value) is list:
        if len(value) > MAX_ITEMS:
            _error(path, 'LIMIT', 'Array exceeds 10000 items')
        return [_walk(child, f'{path}[{i}]') for i, child in enumerate(value)]
    if type(value) is str:
        _unicode(value, path)
    return value


def _depth(text):
    # Count containers before invoking json's recursive parser. Quoted brackets
    # and escapes are not nesting; syntax itself is validated by json.loads.
    depth = 0
    quoted = escaped = False
    for char in text:
        if quoted:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == '"':
                quoted = False
        elif char == '"':
            quoted = True
        elif char in '[{':
            depth += 1
            if depth > MAX_DEPTH:
                _error('$', 'LIMIT', 'JSON container nesting exceeds 64')
        elif char in ']}':
            depth -= 1


def _object(value, schema, path):
    if type(value) is not dict:
        _error(path, 'TYPE', 'Expected an object')
    missing = schema.keys() - value.keys()
    extra = value.keys() - schema.keys()
    if missing:
        _error(_field(path, sorted(missing)[0]), 'MISSING_FIELD', 'Required field is absent')
    if extra:
        _error(_field(path, sorted(extra)[0]), 'UNKNOWN_FIELD', 'Unknown field')
    return {name: parser(value[name], _field(path, name)) for name, parser in schema.items()}


def _text(value, path):
    if type(value) is not str or not value.strip():
        _error(path, 'TYPE', 'Expected a nonempty string')
    return value


def _integer(value, path):
    if type(value) is not int:
        _error(path, 'TYPE', 'Expected an integer, not bool')
    return value


def _positive(value, path):
    value = _integer(value, path)
    if value < 1:
        _error(path, 'RANGE', 'Expected a positive integer')
    return value


def _uuid(value, path):
    value = _text(value, path)
    try:
        valid = str(UUID(value)) == value
    except ValueError:
        valid = False
    if not valid:
        _error(path, 'UUID', 'Expected a canonical lowercase hyphenated UUID')
    return value


def _hash(value, path):
    if type(value) is not str or re.fullmatch('[0-9a-f]{64}', value) is None:
        _error(path, 'HASH_FORMAT', 'Expected 64 lowercase hex characters; content is not verified')
    return value


def _utc(value, path):
    value = _text(value, path)
    if re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z', value) is None:
        _error(path, 'DATE', 'Expected UTC seconds YYYY-MM-DDTHH:MM:SSZ')
    try:
        datetime.fromisoformat(value[:-1] + '+00:00')
    except ValueError:
        _error(path, 'DATE', 'Invalid calendar date or time')
    return value


def _choice(*options):
    def parse(value, path):
        if type(value) is not str or value not in options:
            _error(path, 'VALUE', 'Value is not in the closed vocabulary')
        return value
    return parse


def _enum(cls):
    def parse(value, path):
        if type(value) is not str:
            _error(path, 'TYPE', 'Expected an enum string')
        try:
            return cls(value)
        except ValueError:
            _error(path, 'ENUM', 'Unknown enum value')
    return parse


def _nullable(parser):
    return lambda value, path: None if value is None else parser(value, path)


def _array(parser, maximum=MAX_ITEMS, unique=False):
    def parse(value, path):
        if type(value) is not list:
            _error(path, 'TYPE', 'Expected an array')
        if len(value) > maximum:
            _error(path, 'LIMIT', f'Array exceeds {maximum} items')
        result = tuple(parser(item, f'{path}[{i}]') for i, item in enumerate(value))
        if unique and len(set(result)) != len(result):
            _error(path, 'DUPLICATE_VALUE', 'Array values must be unique')
        return result
    return parse


def _make(cls, fields, path):
    try:
        return cls(**fields)
    except m.ModelError as error:
        field = error.violation.field_path
        # Companion owner_ref is the same wire ref, not an extra JSON field.
        if field == 'owner_ref':
            field = 'ref'
        if field in ('rubric.keys', 'assessment.keys', 'segments.id', 'scenes.id'):
            field = field.split('.')[0]
        if '/' in field:
            options = field.split('/')
            field = next((key for key in options if not fields.get(key)), options[0])
        _error(f'{path}.{field}', 'MODEL_VALUE', error.violation.message)


def _ref(kind=None):
    def parse(value, path):
        data = _object(value, {'kind': _enum(m.ObjectKind), 'id': _uuid,
                               'revision': _positive, 'content_hash': _hash}, path)
        if kind is not None and data['kind'] is not kind:
            _error(f'{path}.kind', 'REFERENCE_KIND', f'Expected {kind.value}')
        return _make(m.RevisionRef, data, path)
    return parse


def _typed(cls, schema, kind=None):
    if kind is not None:
        schema = {'ref': _ref(kind), **schema}
    def parse(value, path):
        return _make(cls, _object(value, schema, path), path)
    return parse


def _texts(names):
    return {name: _text for name in names.split()}


_USE = _choice('test', 'personal', 'commercial')
_ACTION = _choice('quote', 'import', 'render', 'distribute')
_RUBRIC = _typed(m.RubricCriterion, {**_texts('key description'),
    'rating_min': _integer, 'rating_max': _integer, 'weight_percent': _integer})
_RATING = _typed(m.CriterionRating, {**_texts('criterion_key reason'), 'rating': _integer})
_PRODUCTION = _typed(m.ProductionRevision, {**_texts('title'),
    'profile_ref': _ref(m.ObjectKind.GENRE_PROFILE), 'content_mode': _enum(m.ContentMode),
    **{key: _enum(m.Locale) for key in ('script_locale', 'narration_locale', 'subtitle_locale', 'ui_locale')},
    'intended_use': _USE, 'output_preset': _choice('9:16', '16:9'), 'created_at': _utc}, m.ObjectKind.PRODUCTION)
_PROFILE = _typed(m.GenreProfile, {**_texts('profile_key version display_name_ru display_name_uk review_policy_version'),
    'allowed_modes': _array(_enum(m.ContentMode)), 'narrative_structure': _array(_text),
    'rubric': _nullable(_array(_RUBRIC))}, m.ObjectKind.GENRE_PROFILE)
_CANDIDATE = _typed(m.CandidateRevision, {**_texts('title summary discovery_input'),
    'source_refs': _array(_ref(m.ObjectKind.SOURCE)),
    'discovery_method': _choice('manual_topic', 'manual_url', 'manual_local'),
    'assessment': _nullable(_array(_RATING)), 'rationale': _nullable(_text)}, m.ObjectKind.CANDIDATE)
_BRIEF = _typed(m.BriefValue, {'revision': _positive, **_texts('audience angle promise'),
    'must_include_claim_refs': _array(_ref(m.ObjectKind.CLAIM)), 'must_avoid': _array(_text),
    'profile_ref': _ref(m.ObjectKind.GENRE_PROFILE)})
_SEGMENT = _typed(m.ScriptSegment, {'id': _uuid, 'text': _text,
    'role': _choice('opening', 'body', 'closing', 'other'), 'claim_refs': _array(_ref(m.ObjectKind.CLAIM)),
    **{key: _nullable(_text) for key in ('visual_notes', 'pronunciation_notes', 'disclosure_marker')}})
_SCRIPT = _typed(m.ScriptRevision, {'production_ref': _ref(m.ObjectKind.PRODUCTION),
    'candidate_ref': _ref(m.ObjectKind.CANDIDATE), 'brief': _BRIEF, 'locale': _enum(m.Locale),
    'segments': _array(_SEGMENT, 1000), 'claim_refs': _array(_ref(m.ObjectKind.CLAIM))}, m.ObjectKind.SCRIPT)
_SCENE = _typed(m.Scene, {'id': _uuid, 'start': _integer, 'end': _integer,
    **_texts('narration_text visual_brief'), 'visual_kind': _choice('still'),
    'asset_ref': _nullable(_ref(m.ObjectKind.ASSET)), 'estimate_ms': _nullable(_positive)})
_PLAN = _typed(m.ScenePlanRevision, {'script_ref': _ref(m.ObjectKind.SCRIPT),
    'scenes': _array(_SCENE, 1000)}, m.ObjectKind.SCENE_PLAN)
_ASSET = _typed(m.AssetRevision, {'file_ref': _text, 'sha256': _hash,
    'kind': _choice('image', 'audio', 'video'), 'rights_ref': _ref(m.ObjectKind.RIGHTS_REVIEW),
    'scene_id': _nullable(_uuid), 'script_ref': _nullable(_ref(m.ObjectKind.SCRIPT)),
    'text_digest': _nullable(_hash)}, m.ObjectKind.ASSET)
_EVIDENCE = _typed(m.EvidenceLink, {'source_ref': _ref(m.ObjectKind.SOURCE),
    'relation': _enum(m.EvidenceRelation), **_texts('locator explanation reviewer'), 'reviewed_at': _utc})
_APPROVAL = _typed(m.ApprovalRecord, {'id': _uuid, 'gate': _choice('SCRIPT', 'SCENES', 'HANDOFF'),
    'object_ref': _ref(), 'dependency_digest': _hash, **_texts('policy_version actor reason'),
    'timestamp': _utc, 'decision': _enum(m.ApprovalDecision), 'review_declarations': _array(_text)})
_EVENT = _typed(m.Event, {'id': _uuid, **_texts('actor reason'), 'at': _utc,
    'action': _choice('production_created', 'revision_added', 'active_selection_changed',
                      'review_recorded', 'approval_recorded', 'recovery_recorded', 'operation_failed'),
    'refs': _array(_ref()), 'error_code': _nullable(_text)})


def _source(value, path):
    data = _object(value, {'ref': _ref(m.ObjectKind.SOURCE), **_texts('title locator'),
        'rights_ref': _ref(m.ObjectKind.RIGHTS_REVIEW), 'source_type': _choice('url', 'local'),
        **{key: _nullable(_text) for key in ('author', 'publisher', 'access_notes', 'reliability_notes')},
        'published_at': _nullable(_utc), 'accessed_at': _nullable(_utc), 'material_digest': _nullable(_hash)}, path)
    locator_path = f'{path}.locator'
    if data['source_type'] == 'url':
        try:
            url = urlsplit(data['locator'])
            valid = (url.scheme in ('http', 'https') and url.hostname and
                     url.username is None and url.password is None and
                     not any(ord(c) <= 32 or ord(c) == 127 for c in data['locator']))
            url.port  # Validate malformed/out-of-range ports, without any request.
        except ValueError:
            valid = False
        if not valid:
            _error(locator_path, 'URL', 'Expected an absolute http(s) URL without userinfo/control characters')
    else:
        try:
            m._relative_path(data['locator'])
        except m.ModelError:
            _error(locator_path, 'PATH', 'Expected a safe managed relative path')
    base_keys = ('ref', 'title', 'locator', 'rights_ref')
    base = _make(m.SourceRevision, {k: data[k] for k in base_keys}, path)
    details = _make(m.SourceDetails, {'owner_ref': base.ref,
                    **{k: v for k, v in data.items() if k not in base_keys}}, path)
    return base, details


def _claim(value, path):
    data = _object(value, {'ref': _ref(m.ObjectKind.CLAIM), 'statement': _text,
        'claim_type': _enum(m.ClaimType), 'materiality': _choice('material', 'context'),
        'evidence_links': _array(_EVIDENCE),
        'review_status': _choice('unreviewed', 'supported', 'disputed', 'unverified', 'qualified', 'removed'),
        **{key: _nullable(_text) for key in ('qualification', 'reviewer', 'reason')},
        'reviewed_at': _nullable(_utc)}, path)
    base_keys = ('ref', 'statement', 'claim_type', 'materiality', 'evidence_links')
    base = _make(m.ClaimRevision, {k: data[k] for k in base_keys}, path)
    review = _make(m.ClaimReview, {'owner_ref': base.ref,
                   **{k: v for k, v in data.items() if k not in base_keys}}, path)
    return base, review


def _subject_kind(value, path):
    kind = _enum(m.ObjectKind)(value, path)
    if kind not in (m.ObjectKind.SOURCE, m.ObjectKind.ASSET):
        _error(path, 'REFERENCE_KIND', 'Rights subject must be source or asset')
    return kind


def _rights(value, path):
    data = _object(value, {'ref': _ref(m.ObjectKind.RIGHTS_REVIEW), 'subject_kind': _subject_kind,
        'subject_id': _uuid, 'subject_revision': _positive, 'material_digest': _hash,
        'intended_use': _USE, 'allowed_actions': _array(_ACTION, unique=True),
        'status': _enum(m.RightsStatus), **_texts('reviewer basis'),
        'reviewed_at': _utc, 'expires_at': _nullable(_utc)}, path)
    base = _make(m.RightsReview, {k: v for k, v in data.items() if k not in ('subject_kind', 'expires_at')}, path)
    details = _make(m.RightsDetails, {'owner_ref': base.ref, 'subject_kind': data['subject_kind'],
                    'expires_at': data['expires_at']}, path)
    return base, details


_COLLECTIONS = (
    ('production_revisions', _PRODUCTION), ('profiles', _PROFILE), ('candidates', _CANDIDATE),
    ('sources', _source), ('claims', _claim), ('scripts', _SCRIPT),
    ('scene_plans', _PLAN), ('assets', _ASSET), ('rights_reviews', _rights),
)
_ACTIVE = {'production': _nullable(_ref(m.ObjectKind.PRODUCTION)),
           'candidate': _nullable(_ref(m.ObjectKind.CANDIDATE)),
           'script': _nullable(_ref(m.ObjectKind.SCRIPT)),
           'scene_plan': _nullable(_ref(m.ObjectKind.SCENE_PLAN))}


def decode_snapshot(raw: bytes) -> m.ContractSnapshot:
    """Decode all or raise DecodeError; checksums/targets remain unverified.

    Requires bytes (not str/bytearray), schema 1 and every documented key,
    including nullable keys and Q5 subject_kind. No missing-value defaults.
    """
    if type(raw) is not bytes:
        _error('$', 'TYPE', 'Expected bytes')
    if len(raw) > MAX_BYTES:
        _error('$', 'LIMIT', 'Snapshot exceeds 32 MiB')
    if raw.startswith(b'\xef\xbb\xbf'):
        _error('$', 'BOM', 'UTF-8 BOM is forbidden')
    try:
        text = raw.decode('utf-8', errors='strict')
    except UnicodeDecodeError:
        _error('$', 'UTF8', 'Invalid UTF-8 bytes')
    _depth(text)
    try:
        parsed = json.loads(text, object_pairs_hook=_Pairs,
                            parse_float=_ForbiddenNumber, parse_constant=_ForbiddenNumber)
    except (ValueError, RecursionError):
        _error('$', 'JSON', 'Invalid JSON syntax or integer token')
    data = _walk(parsed, '$')
    # Scalars/collections below are parsed explicitly, not returned partially.
    root_fields = {name: lambda v, p: v for name, _ in _COLLECTIONS}
    root_fields.update({key: lambda v, p: v for key in (
        'editorial_schema_version', 'production_id', 'generation', 'approvals',
        'events', 'active_refs', 'snapshot_checksum')})
    _object(data, root_fields, '$')
    version = _integer(data['editorial_schema_version'], '$.editorial_schema_version')
    if version != 1:
        _error('$.editorial_schema_version', 'SCHEMA_VERSION', 'Only editorial schema version 1 is supported')
    production_id = _uuid(data['production_id'], '$.production_id')
    generation = _positive(data['generation'], '$.generation')
    checksum = _hash(data['snapshot_checksum'], '$.snapshot_checksum')
    revisions = []
    companions = {'sources': [], 'claims': [], 'rights_reviews': []}
    for name, parser in _COLLECTIONS:
        values = _array(parser)(data[name], f'$.{name}')
        previous = None
        for i, value in enumerate(values):
            revision, companion = value if name in companions else (value, None)
            key = (revision.ref.id, revision.ref.revision)
            if previous is not None and key <= previous:
                _error(f'$.{name}[{i}].ref', 'REVISION_ORDER', 'Revisions must be unique and ordered by id/revision')
            previous = key
            revisions.append(revision)
            if len(revisions) > MAX_ITEMS:
                _error(f'$.{name}', 'LIMIT', 'Total revisions exceed 10000')
            if companion is not None:
                companions[name].append(companion)
    approvals = _array(_APPROVAL)(data['approvals'], '$.approvals')
    events = _array(_EVENT)(data['events'], '$.events')
    for name, values in (('approvals', approvals), ('events', events)):
        seen = set()
        for i, value in enumerate(values):
            if value.id in seen:
                _error(f'$.{name}[{i}].id', 'DUPLICATE_VALUE', 'Record id must be unique')
            seen.add(value.id)
    active = _object(data['active_refs'], _ACTIVE, '$.active_refs')
    base = _make(m.EditorialSnapshot, {'production_id': production_id, 'generation': generation,
        'revisions': tuple(revisions), 'approvals': approvals,
        'active_refs': tuple(v for v in active.values() if v is not None),
        'editorial_schema_version': version}, '$')
    return _make(m.ContractSnapshot, {'base': base, 'source_details': tuple(companions['sources']),
        'claim_reviews': tuple(companions['claims']), 'rights_details': tuple(companions['rights_reviews']),
        'events': events, 'snapshot_checksum': checksum}, '$')


def _enum_value(value):
    """Preserve weak legacy values so strict decode can reject them with a path."""
    return value.value if isinstance(value, Enum) else value


def _wire_ref(value):
    return {'kind': _enum_value(value.kind), 'id': value.id, 'revision': value.revision,
            'content_hash': value.content_hash}


def _wire_rubric(value):
    return {'key': value.key, 'description': value.description, 'rating_min': value.rating_min,
            'rating_max': value.rating_max, 'weight_percent': value.weight_percent}


def _wire_rating(value):
    return {'criterion_key': value.criterion_key, 'rating': value.rating, 'reason': value.reason}


def _wire_brief(value):
    return {'revision': value.revision, 'audience': value.audience, 'angle': value.angle,
            'promise': value.promise,
            'must_include_claim_refs': [_wire_ref(r) for r in value.must_include_claim_refs],
            'must_avoid': list(value.must_avoid), 'profile_ref': _wire_ref(value.profile_ref)}


def _wire_segment(value):
    return {'id': value.id, 'text': value.text, 'role': value.role,
            'claim_refs': [_wire_ref(r) for r in value.claim_refs],
            'visual_notes': value.visual_notes, 'pronunciation_notes': value.pronunciation_notes,
            'disclosure_marker': value.disclosure_marker}


def _wire_scene(value):
    return {'id': value.id, 'start': value.start, 'end': value.end,
            'narration_text': value.narration_text, 'visual_kind': value.visual_kind,
            'visual_brief': value.visual_brief,
            'asset_ref': None if value.asset_ref is None else _wire_ref(value.asset_ref),
            'estimate_ms': value.estimate_ms}


def _wire_evidence(value):
    return {'source_ref': _wire_ref(value.source_ref), 'relation': _enum_value(value.relation),
            'locator': value.locator, 'explanation': value.explanation, 'reviewer': value.reviewer,
            'reviewed_at': value.reviewed_at}


def _wire_revision(value):
    common = {'ref': _wire_ref(value.ref)}
    if type(value) is m.ProductionRevision:
        return common | {'title': value.title, 'profile_ref': _wire_ref(value.profile_ref),
            'content_mode': _enum_value(value.content_mode),
            'script_locale': _enum_value(value.script_locale),
            'narration_locale': _enum_value(value.narration_locale),
            'subtitle_locale': _enum_value(value.subtitle_locale), 'ui_locale': _enum_value(value.ui_locale),
            'intended_use': value.intended_use, 'output_preset': value.output_preset,
            'created_at': value.created_at}
    if type(value) is m.GenreProfile:
        return common | {'profile_key': value.profile_key, 'version': value.version,
            'display_name_ru': value.display_name_ru, 'display_name_uk': value.display_name_uk,
            'allowed_modes': [_enum_value(v) for v in value.allowed_modes],
            'narrative_structure': list(value.narrative_structure),
            'review_policy_version': value.review_policy_version,
            'rubric': None if value.rubric is None else [_wire_rubric(v) for v in value.rubric]}
    if type(value) is m.CandidateRevision:
        return common | {'title': value.title, 'summary': value.summary,
            'source_refs': [_wire_ref(v) for v in value.source_refs],
            'discovery_method': value.discovery_method, 'discovery_input': value.discovery_input,
            'assessment': None if value.assessment is None else [_wire_rating(v) for v in value.assessment],
            'rationale': value.rationale}
    if type(value) is m.SourceRevision:
        return common | {'title': value.title, 'locator': value.locator,
                         'rights_ref': _wire_ref(value.rights_ref)}
    if type(value) is m.ClaimRevision:
        return common | {'statement': value.statement, 'claim_type': _enum_value(value.claim_type),
            'materiality': value.materiality,
            'evidence_links': [_wire_evidence(v) for v in value.evidence_links]}
    if type(value) is m.ScriptRevision:
        return common | {'production_ref': _wire_ref(value.production_ref),
            'candidate_ref': _wire_ref(value.candidate_ref), 'brief': _wire_brief(value.brief),
            'locale': _enum_value(value.locale), 'segments': [_wire_segment(v) for v in value.segments],
            'claim_refs': [_wire_ref(v) for v in value.claim_refs]}
    if type(value) is m.ScenePlanRevision:
        return common | {'script_ref': _wire_ref(value.script_ref),
                         'scenes': [_wire_scene(v) for v in value.scenes]}
    if type(value) is m.AssetRevision:
        return common | {'file_ref': value.file_ref, 'sha256': value.sha256, 'kind': value.kind,
            'rights_ref': _wire_ref(value.rights_ref), 'scene_id': value.scene_id,
            'script_ref': None if value.script_ref is None else _wire_ref(value.script_ref),
            'text_digest': value.text_digest}
    if type(value) is m.RightsReview:
        return common | {'subject_id': value.subject_id, 'subject_revision': value.subject_revision,
            'material_digest': value.material_digest, 'intended_use': value.intended_use,
            'allowed_actions': list(value.allowed_actions), 'status': _enum_value(value.status),
            'reviewer': value.reviewer, 'reviewed_at': value.reviewed_at, 'basis': value.basis}
    _encode_error('$.base.revisions', 'UNSUPPORTED_TYPE', 'Unsupported revision payload type')


def _wire_approval(value):
    return {'id': value.id, 'gate': value.gate, 'object_ref': _wire_ref(value.object_ref),
            'dependency_digest': value.dependency_digest, 'policy_version': value.policy_version,
            'actor': value.actor, 'timestamp': value.timestamp, 'decision': _enum_value(value.decision),
            'reason': value.reason, 'review_declarations': list(value.review_declarations)}


def _wire_event(value):
    return {'id': value.id, 'actor': value.actor, 'at': value.at, 'action': value.action,
            'refs': [_wire_ref(v) for v in value.refs], 'reason': value.reason,
            'error_code': value.error_code}


def _companions(revisions, values, collection, internal_name):
    if type(values) is not tuple:
        _encode_error(f'$.{internal_name}', 'TYPE', 'Companion collection must be an immutable tuple')
    if len(values) != len(revisions):
        index = min(len(values), len(revisions))
        _encode_error(f'$.{collection}[{index}]', 'COMPANION_COUNT',
                      'Exactly one companion is required for every revision')
    for i, (revision, companion) in enumerate(zip(revisions, values)):
        if companion.owner_ref != revision.ref:
            _encode_error(f'$.{collection}[{i}].ref', 'COMPANION_OWNER',
                          'Companion owner_ref must exactly match the revision ref in the same position')
    return values


def encode_snapshot(snapshot: m.ContractSnapshot) -> bytes:
    """Return deterministic normative JSON bytes or raise EncodeError.

    The supplied checksum is retained, never computed or verified. The complete
    wire value is validated through the strict decoder before bytes are returned.
    """
    if type(snapshot) is not m.ContractSnapshot:
        _encode_error('$', 'TYPE', 'Expected ContractSnapshot')
    try:
        revisions = tuple(snapshot.base.revisions)
        ranks = {kind: rank for rank, (kind, _) in enumerate(m._REVISION_TYPES)}
        try:
            order = tuple((ranks[v.ref.kind], v.ref.id, v.ref.revision) for v in revisions)
        except (AttributeError, KeyError):
            _encode_error('$.base.revisions', 'UNSUPPORTED_TYPE', 'Revision has no supported typed ref')
        if order != tuple(sorted(order)) or len(order) != len(set(order)):
            _encode_error('$.base.revisions', 'REVISION_ORDER',
                          'Revisions must use contract collection/id/revision order without duplicates')
        grouped = {kind: tuple(v for v in revisions if v.ref.kind is kind)
                   for kind, _ in m._REVISION_TYPES}
        sources = grouped[m.ObjectKind.SOURCE]
        claims = grouped[m.ObjectKind.CLAIM]
        rights = grouped[m.ObjectKind.RIGHTS_REVIEW]
        source_details = _companions(sources, snapshot.source_details, 'sources', 'source_details')
        claim_reviews = _companions(claims, snapshot.claim_reviews, 'claims', 'claim_reviews')
        rights_details = _companions(rights, snapshot.rights_details, 'rights_reviews', 'rights_details')

        collections = {name: [_wire_revision(v) for v in grouped[kind]] for name, kind in (
            ('production_revisions', m.ObjectKind.PRODUCTION), ('profiles', m.ObjectKind.GENRE_PROFILE),
            ('candidates', m.ObjectKind.CANDIDATE), ('sources', m.ObjectKind.SOURCE),
            ('claims', m.ObjectKind.CLAIM), ('scripts', m.ObjectKind.SCRIPT),
            ('scene_plans', m.ObjectKind.SCENE_PLAN), ('assets', m.ObjectKind.ASSET),
            ('rights_reviews', m.ObjectKind.RIGHTS_REVIEW))}
        for record, details in zip(collections['sources'], source_details):
            record.update({'source_type': details.source_type, 'author': details.author,
                'publisher': details.publisher, 'published_at': details.published_at,
                'accessed_at': details.accessed_at, 'access_notes': details.access_notes,
                'reliability_notes': details.reliability_notes, 'material_digest': details.material_digest})
        for record, review in zip(collections['claims'], claim_reviews):
            record.update({'review_status': review.review_status, 'qualification': review.qualification,
                'reviewer': review.reviewer, 'reviewed_at': review.reviewed_at, 'reason': review.reason})
        for record, details in zip(collections['rights_reviews'], rights_details):
            record.update({'subject_kind': _enum_value(details.subject_kind),
                           'expires_at': details.expires_at})

        active = snapshot.active_selections
        envelope = {'editorial_schema_version': snapshot.base.editorial_schema_version,
            'production_id': snapshot.base.production_id, 'generation': snapshot.base.generation,
            **collections, 'approvals': [_wire_approval(v) for v in snapshot.base.approvals],
            'events': [_wire_event(v) for v in snapshot.events],
            'active_refs': {name: None if value is None else _wire_ref(value) for name, value in (
                ('production', active.production), ('candidate', active.candidate),
                ('script', active.script), ('scene_plan', active.scene_plan))},
            'snapshot_checksum': snapshot.snapshot_checksum}
        encoded = json.dumps(envelope, ensure_ascii=False, sort_keys=True, separators=(',', ':'),
                             allow_nan=False).encode('utf-8')
    except EncodeError:
        raise
    except (AttributeError, TypeError, ValueError, OverflowError) as error:
        _encode_error('$', 'INTERNAL_SHAPE', f'Unsupported or malformed internal value: {error}')
    try:
        restored = decode_snapshot(encoded)
    except DecodeError as error:
        violation = error.violation
        raise EncodeError(m.Violation('INVALID_VALUE', violation.field_path, violation.message)) from None
    if restored != snapshot:
        _encode_error('$', 'NON_REVERSIBLE', 'Internal snapshot cannot round-trip without information loss')
    return encoded
