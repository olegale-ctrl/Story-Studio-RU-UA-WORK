"""E01.2.1 strict decoder only; no encoding, hashing, I/O or graph lookup."""
import json
import re
from datetime import datetime
from urllib.parse import urlsplit
from uuid import UUID

from . import model as m

__all__ = ('decode_snapshot', 'DecodeError')

MAX_BYTES = 32 * 1024 * 1024
MAX_DEPTH = 64
MAX_ITEMS = 10_000
MAX_TEXT = 100_000


class DecodeError(m.ModelError):
    """Atomic decode failure; violation.field_path is a JSON-style path."""


def _error(path, code, message):
    raise DecodeError(m.Violation(code, path, message))


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
