"""Local SI/1 structure only. Public validators return detached plain-value copies.

References are supplied claims, not resolved records or evidence of authority.
No payload, run-stage, hash-against-record or provenance ancestry resolution here.
"""
from copy import deepcopy
from datetime import datetime
import re


__all__ = ['SIValidationError', 'validate_si_ref', 'validate_eref',
           'validate_known', 'validate_origin', 'validate_header']

_RECORD_TYPES = frozenset(('Intake', 'StoryIdea', 'SourceItem', 'ClaimItem',
    'EvidenceItem', 'ClaimCheck', 'AudienceHypothesis', 'ChannelContext', 'Angle',
    'Rubric', 'RunRecord', 'EvaluationReport', 'CreativeAlternative',
    'VisualRequirement', 'Risk', 'ProductionBrief', 'Selection', 'ReviewPacket'))
# Exact read-only ObjectKind vocabulary; deliberately no editorial runtime import.
_EDITORIAL_KINDS = frozenset(('production', 'genre_profile', 'candidate', 'source',
    'claim', 'script', 'scene_plan', 'asset', 'rights_review'))
_MODES = frozenset(('MANUAL_INPUT', 'USER_IMPORT', 'RULE_DERIVED',
    'TEMPLATE_DERIVED', 'MODEL_DERIVED', 'HUMAN_EDIT', 'RUN_METADATA'))
_DERIVED = frozenset(('RULE_DERIVED', 'TEMPLATE_DERIVED', 'MODEL_DERIVED', 'HUMAN_EDIT'))
_UUID = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\Z')
_HASH = re.compile(r'[0-9a-f]{64}\Z')
_UTC = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z\Z')


class SIValidationError(ValueError):
    """Non-authorizing structural failure; code/path are stable public diagnostics."""

    def __init__(self, code, path, message):
        self.code = code
        self.path = path
        super().__init__(f'{code} at {path}: {message}')


def _fail(code, path, message):
    raise SIValidationError(code, path, message)


def _shape(value, fields, path):
    if type(value) is not dict:
        _fail('TYPE', path, 'Expected plain object')
    for key in value:
        if type(key) is not str:
            _fail('TYPE', path, 'Expected string keys')
        if key not in fields:
            _fail('UNKNOWN_FIELD', f'{path}.{key}', 'Unknown field')
    for key in fields:
        if key not in value:
            _fail('MISSING_FIELD', f'{path}.{key}', 'Required field')


def _text(value, path):
    if type(value) is not str or not value:
        _fail('TYPE', path, 'Expected nonempty Text')
    if len(value) > 100_000:
        _fail('LIMIT', path, 'Text exceeds 100000 codepoints')
    if any(0xD800 <= ord(c) <= 0xDFFF for c in value):
        _fail('TYPE', path, 'Surrogate forbidden')


def _choice(value, choices, path):
    if type(value) is not str or value not in choices:
        _fail('TYPE', path, 'Unknown closed vocabulary value')


def _positive(value, path):
    if type(value) is not int or value < 1:
        _fail('TYPE', path, 'Expected positive integer, excluding bool')


def _pattern(value, pattern, path, message):
    if type(value) is not str or not pattern.fullmatch(value):
        _fail('TYPE', path, message)


def _ref(value, editorial, path):
    label, digest = ('kind', 'content_hash') if editorial else ('type', 'sha256')
    _shape(value, (label, 'id', 'revision', digest), path)
    _choice(value[label], _EDITORIAL_KINDS if editorial else _RECORD_TYPES, f'{path}.{label}')
    _pattern(value['id'], _UUID, f'{path}.id', 'Expected canonical lowercase UUID')
    _positive(value['revision'], f'{path}.revision')
    _pattern(value[digest], _HASH, f'{path}.{digest}', 'Expected lowercase SHA-256 hex')


def _known(value, validator, path):
    if type(value) is not dict:
        _fail('TYPE', path, 'Expected Known object')
    if 'state' not in value:
        _fail('MISSING_FIELD', f'{path}.state', 'Required field')
    _choice(value['state'], ('KNOWN', 'UNKNOWN'), f'{path}.state')
    if value['state'] == 'KNOWN':
        _shape(value, ('state', 'value'), path)
        validator(value['value'], f'{path}.value')
    else:
        _shape(value, ('state', 'reason'), path)
        _text(value['reason'], f'{path}.reason')


def _origin(value, path):
    _shape(value, ('mode', 'run_ref', 'imported_from'), path)
    mode = value['mode']
    _choice(mode, _MODES, f'{path}.mode')
    if mode in _DERIVED:
        _ref(value['run_ref'], False, f'{path}.run_ref')
        if value['run_ref']['type'] != 'RunRecord':
            _fail('REF_TYPE_MISMATCH', f'{path}.run_ref.type', 'Expected RunRecord')
    elif value['run_ref'] is not None:
        _fail('PROVENANCE_MISMATCH', f'{path}.run_ref', 'This mode has no run')
    if mode == 'USER_IMPORT':
        _known(value['imported_from'], _text, f'{path}.imported_from')
    elif value['imported_from'] is not None:
        _fail('PROVENANCE_MISMATCH', f'{path}.imported_from', 'Only USER_IMPORT has imported_from')


def _header(value, path):
    fields = ('si_version', 'type', 'id', 'revision', 'previous', 'created_at',
              'creator_label', 'origin', 'input_refs', 'editorial_refs')
    _shape(value, fields, path)
    if type(value['si_version']) is not int:
        _fail('TYPE', f'{path}.si_version', 'Expected integer version')
    if value['si_version'] != 1:
        _fail('VERSION_UNSUPPORTED', f'{path}.si_version', 'Expected SI/1')
    _choice(value['type'], _RECORD_TYPES, f'{path}.type')
    _pattern(value['id'], _UUID, f'{path}.id', 'Expected canonical lowercase UUID')
    _positive(value['revision'], f'{path}.revision')
    previous = value['previous']
    if value['revision'] == 1:
        if previous is not None:
            _fail('PROVENANCE_MISMATCH', f'{path}.previous', 'Initial revision has no previous')
    else:
        _ref(previous, False, f'{path}.previous')
        for key in ('type', 'id'):
            if previous[key] != value[key]:
                _fail('PROVENANCE_MISMATCH', f'{path}.previous.{key}', 'Previous identity differs')
        if previous['revision'] != value['revision'] - 1:
            _fail('PROVENANCE_MISMATCH', f'{path}.previous.revision', 'Expected exact preceding revision')
    _pattern(value['created_at'], _UTC, f'{path}.created_at', 'Expected UTC seconds')
    try:
        datetime.strptime(value['created_at'], '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        _fail('TYPE', f'{path}.created_at', 'Invalid calendar time')
    _text(value['creator_label'], f'{path}.creator_label')
    _origin(value['origin'], f'{path}.origin')
    for key, editorial in (('input_refs', False), ('editorial_refs', True)):
        if type(value[key]) is not list:
            _fail('TYPE', f'{path}.{key}', 'Expected plain list')
        for i, ref in enumerate(value[key]):
            _ref(ref, editorial, f'{path}.{key}[{i}]')
    kind, mode, initial = value['type'], value['origin']['mode'], value['revision'] == 1
    if kind == 'RunRecord':
        if not initial or mode != 'RUN_METADATA':
            _fail('PROVENANCE_MISMATCH', f'{path}.origin.mode', 'RunRecord is initial RUN_METADATA')
        if value['creator_label'] != 'SI_ENGINE':
            _fail('PROVENANCE_MISMATCH', f'{path}.creator_label', 'RunRecord label must be SI_ENGINE')
    else:
        if kind == 'ReviewPacket' and value['creator_label'] != 'SI_EXPORTER':
            _fail('PROVENANCE_MISMATCH', f'{path}.creator_label', 'ReviewPacket label must be SI_EXPORTER')
        if kind == 'StoryIdea':
            allowed = ('RULE_DERIVED',) if initial else ('HUMAN_EDIT',)
        elif kind == 'CreativeAlternative':
            allowed = ('TEMPLATE_DERIVED',) if initial else ('HUMAN_EDIT',)
        elif kind in ('EvaluationReport', 'ReviewPacket'):
            allowed = ('RULE_DERIVED',) if initial else ()
        elif kind == 'Selection':
            allowed = ('MANUAL_INPUT',)
        elif kind == 'ProductionBrief':
            allowed = ('MANUAL_INPUT', 'USER_IMPORT', 'RULE_DERIVED') if initial else ('HUMAN_EDIT', 'RULE_DERIVED')
        else:
            allowed = ('MANUAL_INPUT', 'USER_IMPORT') if initial else ('HUMAN_EDIT',)
        if mode not in allowed:
            _fail('PROVENANCE_MISMATCH', f'{path}.origin.mode', 'Mode incompatible with type/revision')


def _validated(value, checker):
    # Single-object limits and exact plain types apply equally to model inputs.
    # Lazy import breaks the codec/error-type dependency without import-time work.
    from .codec_v1 import canonical_si_json
    canonical_si_json(value)
    checker(value, '$')
    return deepcopy(value)


def validate_si_ref(value):
    """Validate unresolved SIRef structure and return a detached copy."""
    return _validated(value, lambda v, p: _ref(v, False, p))


def validate_eref(value):
    """Validate editorial ref shape, not the referenced revision or authority."""
    return _validated(value, lambda v, p: _ref(v, True, p))


def validate_known(value, value_validator):
    """Validate union and return a copy; callback takes T, raises on invalid T.

    Callback return values are ignored (no coercion). It receives a detached copy;
    it must be a pure validator. Callback SIValidationError paths are rebased below
    $.value; other callback exceptions propagate as supplied by the caller.
    """
    if not callable(value_validator):
        _fail('TYPE', '$', 'Expected callable value validator')

    def check(v, p):
        def check_value(child, child_path):
            try:
                value_validator(deepcopy(child))
            except SIValidationError as error:
                suffix = error.path[1:] if error.path.startswith('$') else '.' + error.path
                raise SIValidationError(error.code, child_path + suffix, str(error)) from error
        _known(v, check_value, p)
    return _validated(value, check)


def validate_origin(value):
    """Validate mode/ref shape only; actual generating Run stage is unresolved."""
    return _validated(value, _origin)


def validate_header(value):
    """Validate H only, never a full record/payload or an authenticated identity."""
    return _validated(value, _header)
