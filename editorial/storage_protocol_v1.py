"""S1 v1 pure wire/crypto primitives, without persistence or authority evaluation.

Schema checks establish wire validity only. A valid MAC is not authorization.
Keys and optional context/plan proofs are explicit inputs; there is no key lookup,
repair, admission, W0–W9 machine, OS adapter, or import-time action here.
"""
import hashlib
import hmac
import json
import re
from datetime import datetime
from uuid import UUID

MAX_BLOB_BYTES = 33_554_432
MAX_FRAME_PAYLOAD = MAX_REQUEST_BYTES = 1_048_576
MAX_COMMAND_BYTES = 2_097_152
MAX_DEPTH = 64
U64_MAX = 18_446_744_073_709_551_615
_MAGIC = b'SSJ1'
_UNSET = object()
_DOMAINS = {name: ('story-studio-storage-' + name + '-v1\0').encode('ascii')
            for name in ('request', 'command', 'journal', 'anchor', 'receipt',
                         'initialize', 'registration', 'approval')}


class ProtocolError(ValueError):
    """A complete, failed check, carrying a stable code and offending field path."""
    def __init__(self, code, path, message):
        self.code, self.path = code, path
        super().__init__(f'{code} at {path}: {message}')


class StructuralError(ProtocolError):
    """Malformed bytes/schema/context; never a successful partial result."""


class CryptographicError(ProtocolError):
    """Unavailable key or mismatched digest/MAC."""


def _fail(code, path, message):
    raise StructuralError(code, path, message)


def _limit(limit):
    if type(limit) is not int or not 1 <= limit <= MAX_BLOB_BYTES:
        _fail('LIMIT', '$', 'Invalid byte bound')


def _text(v, p, nonempty=False, maximum=100_000):
    if type(v) is not str:
        _fail('TYPE', p, 'Expected string')
    if len(v) > maximum:
        _fail('LIMIT', p, 'Text too long')
    if any(0xD800 <= ord(c) <= 0xDFFF for c in v):
        _fail('WIRE_FORMAT', p, 'Surrogates forbidden')
    if nonempty and not v:
        _fail('TYPE', p, 'Empty text')


def _decimal(n):
    # No process-global int conversion setting and no artificial Generation cap.
    if n < 0:
        return '-' + _decimal(-n)
    chunks = []
    while n >= 1_000_000_000:
        n, part = divmod(n, 1_000_000_000)
        chunks.append(f'{part:09d}')
    return str(n) + ''.join(reversed(chunks))


def canonical_json(value, *, max_bytes=MAX_BLOB_BYTES):
    """Exact S1 C(x); plain JSON types only, bounded containers/UTF-8 output."""
    _limit(max_bytes)
    parts, size = [], 0

    def emit(s):
        nonlocal size
        b = s.encode('utf-8')
        size += len(b)
        if size > max_bytes:
            _fail('LIMIT', '$', 'Canonical bytes exceed bound')
        parts.append(b)

    def walk(v, p, depth):
        t = type(v)
        if t in (dict, list):
            if depth >= MAX_DEPTH:
                _fail('LIMIT', p, 'Nesting exceeds 64 containers')
            if t is dict:
                for k in v:
                    _text(k, p)
                emit('{')
                for i, k in enumerate(sorted(v)):
                    if i:
                        emit(',')
                    emit(json.dumps(k, ensure_ascii=False)); emit(':')
                    walk(v[k], f'{p}.{k}', depth + 1)
                emit('}')
            else:
                emit('[')
                for i, child in enumerate(v):
                    if i:
                        emit(',')
                    walk(child, f'{p}[{i}]', depth + 1)
                emit(']')
        elif t is str:
            _text(v, p); emit(json.dumps(v, ensure_ascii=False))
        elif t is int:
            if v.bit_length() > max_bytes * 4:
                _fail('LIMIT', p, 'Integer cannot fit byte bound')
            emit(_decimal(v))
        elif t is bool:
            emit('true' if v else 'false')
        elif v is None:
            emit('null')
        else:
            _fail('TYPE', p, 'Only exact JSON types; no floats or coercion')
    walk(value, '$', 0)
    return b''.join(parts)


def _scan_depth(text):
    quoted = escaped = False
    depth = 0
    for c in text:
        if quoted:
            if escaped:
                escaped = False
            elif c == '\\':
                escaped = True
            elif c == '"':
                quoted = False
        elif c == '"':
            quoted = True
        elif c in '[{':
            depth += 1
            if depth > MAX_DEPTH:
                _fail('LIMIT', '$', 'Nesting exceeds 64 containers')
        elif c in ']}':
            depth -= 1


class _Pairs(list):
    pass


def decode_canonical_json(data, *, max_bytes=MAX_BLOB_BYTES):
    """Reject noncanonical encodings rather than silently canonicalizing them."""
    _limit(max_bytes)
    if type(data) is not bytes:
        _fail('TYPE', '$', 'Expected bytes')
    if not data or len(data) > max_bytes:
        _fail('LIMIT', '$', 'Invalid byte length')
    try:
        text = data.decode('utf-8', errors='strict')
    except UnicodeDecodeError:
        _fail('WIRE_FORMAT', '$', 'Invalid UTF-8')
    _scan_depth(text)

    def forbidden(_):
        _fail('TYPE', '$', 'Float/NaN/Infinity forbidden')

    def integer(s):
        neg = s.startswith('-')
        digits = s[1:] if neg else s
        n = 0
        for i in range(0, len(digits), 9):
            chunk = digits[i:i + 9]
            n = n * (10 ** len(chunk)) + int(chunk)
        return -n if neg else n

    try:
        raw = json.loads(text, object_pairs_hook=_Pairs, parse_int=integer,
                         parse_float=forbidden, parse_constant=forbidden)
    except (ValueError, RecursionError) as error:
        if isinstance(error, ProtocolError):
            raise
        _fail('WIRE_FORMAT', '$', 'Invalid JSON')

    def unpack(v, p):
        if isinstance(v, _Pairs):
            result = {}
            for k, child in v:
                if k in result:
                    _fail('DUPLICATE_KEY', f'{p}.{k}', 'Duplicate key')
                result[k] = unpack(child, f'{p}.{k}')
            return result
        if type(v) is list:
            return [unpack(child, f'{p}[{i}]') for i, child in enumerate(v)]
        return v
    value = unpack(raw, '$')
    if canonical_json(value, max_bytes=max_bytes) != data:
        _fail('WIRE_FORMAT', '$', 'Noncanonical JSON bytes')
    return value


def _uint(v, p, minimum=0, maximum=U64_MAX):
    if type(v) is not int:
        _fail('TYPE', p, 'Expected integer, not bool/float')
    if v < minimum or (maximum is not None and v > maximum):
        _fail('SEQUENCE_EXHAUSTED' if maximum == U64_MAX else 'LIMIT', p, 'Integer out of bounds')


def _hex(v, p):
    _text(v, p)
    if re.fullmatch('[0-9a-f]{64}', v) is None:
        _fail('TYPE', p, 'Expected lowercase SHA-256 hex')


def _uuid(v, p):
    _text(v, p)
    try:
        good = str(UUID(v)) == v
    except ValueError:
        good = False
    if not good:
        _fail('TYPE', p, 'Expected canonical UUID')


def _principal(v, p):
    _text(v, p)
    if re.fullmatch(r'(?:windows-sid:S-[0-9]+(?:-[0-9]+)+|posix-uid:(?:0|[1-9][0-9]*)@machine:[0-9a-f]{32})', v) is None:
        _fail('TYPE', p, 'Expected existing tagged principal syntax')


def _utc(v, p):
    _text(v, p)
    if re.fullmatch(r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z', v) is None:
        _fail('TYPE', p, 'Expected UTC calendar timestamp')
    try:
        datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        _fail('TYPE', p, 'Invalid calendar timestamp')


def _label(v, p):
    _text(v, p)
    if re.fullmatch('[A-Za-z0-9][A-Za-z0-9._:-]{0,127}', v) is None:
        _fail('TYPE', p, 'Invalid label')


def _choice(*values):
    def check(v, p):
        if type(v) is not type(values[0]) or v not in values:
            _fail('VERSION_UNSUPPORTED' if values == (1,) else 'TYPE', p, 'Unsupported value')
    return check


def _nullable(check):
    return lambda v, p: None if v is None else _check(v, check, p)


def _array(check, minimum=0, maximum=None):
    def validate(v, p):
        if type(v) is not list:
            _fail('TYPE', p, 'Expected array')
        if len(v) < minimum or (maximum is not None and len(v) > maximum):
            _fail('LIMIT', p, 'Invalid array length')
        for i, child in enumerate(v):
            _check(child, check, f'{p}[{i}]')
    return validate


def _check(v, schema, p='$'):
    if isinstance(schema, str):
        schema = _SCHEMAS[schema]
    if callable(schema):
        schema(v, p)
        return
    if type(v) is not dict:
        _fail('TYPE', p, 'Expected object')
    for k in sorted(v):
        if k not in schema:
            _fail('UNKNOWN_FIELD', f'{p}.{k}', 'Unknown field')
    for k, check in schema.items():
        if k not in v:
            _fail('MISSING_FIELD', f'{p}.{k}', 'Required field')
        _check(v[k], check, f'{p}.{k}')


_nonempty = lambda v, p: _text(v, p, nonempty=True)
_generation = lambda v, p: _uint(v, p, 1, None)
_blob_length = lambda v, p: _uint(v, p, 1, MAX_BLOB_BYTES)
_gate = _choice('SCRIPT', 'SCENES', 'HANDOFF')
_decision = _choice('approve', 'reject', 'revise', 'revoke')
_abort = _choice('CANCELLED_BEFORE_INTENT', 'SESSION_INVALIDATED', 'REVALIDATION_FAILED', 'RECOVERY_PREINTENT_ABORT')
_operations = ('INITIALIZE_EMPTY', 'IMPORT_BASELINE', 'TRANSFER_BASELINE', 'RECORD_DECISION', 'MIGRATE_SCHEMA', 'RESTORE_EXACT_HEAD')


def _editorial_ref(v, p):
    # Reuse the approved editorial wire schema/model; never round-trip to coerce it.
    from . import codec
    try:
        codec._ref()(v, p)
    except codec.DecodeError as error:
        _fail(error.violation.code, error.violation.field_path, error.violation.message)


def _declaration(v, p):
    from .schema2_model import _ALL_DECLARATION_CODES
    _choice(*sorted(_ALL_DECLARATION_CODES))(v, p)


def _approval(v, p):
    from . import codec
    try:
        codec._APPROVAL(v, p)
    except codec.DecodeError as error:
        _fail(error.violation.code, error.violation.field_path, error.violation.message)


_SCHEMAS = {
    'BlobRef': {'sha256': _hex, 'byte_length': _blob_length},
    'JournalRef': {'record_index': _uint, 'record_mac': _hex},
    'PolicyRef': {'policy_id': _uuid, 'policy_version': lambda v, p: _text(v, p, True, 128), 'policy_sha256': _hex},
    'ContentHead': {'content_head_version': _choice(1), 'production_id': _uuid, 'machine_binding_id': _uuid,
                    'storage_epoch_id': _uuid, 'editorial_schema_version': _choice(1, 2), 'generation': _generation,
                    'snapshot_checksum': _hex, 'snapshot_file_sha256': _hex, 'snapshot_file_length': _blob_length, 'tx_seq': _uint},
    'CommittedHead': {'committed_head_version': _choice(1), 'content_head': 'ContentHead', 'commit_ref': 'JournalRef'},
    'HistoryGuard': {'guard_version': _choice(1), 'continuity': _choice('CONTINUOUS', 'BASELINE_UNVERIFIED', 'CONTINUITY_LOST'),
                     **{k: _nullable('BlobRef') for k in ('baseline_ref', 'ledger_tip', 'barrier_tip', 'lineage_tip')}},
    'DecisionKey': {'gate': _gate, 'policy_version': _nonempty, 'object_ref': _editorial_ref, 'dependency_digest': _hex},
    'GateDecisionGrant': {'gate': _gate, 'decision': _decision},
    'Authorization': {'policy_ref': 'PolicyRef', 'principal_id': _principal, 'authenticated_connection_id': _uuid,
                      'command_grants': _array(_choice('PROTECTED_SNAPSHOT_WRITE', 'INITIALIZE', 'RECOVERY', 'MIGRATE_SCHEMA', 'RECORD_DECISION')),
                      'gate_decision_grant': _nullable('GateDecisionGrant')},
    'ReviewSnapshot': {'session_id': _uuid, 'principal_id': _principal, 'policy_ref': 'PolicyRef', 'decision_key': 'DecisionKey',
                       'confirmed_codes': _array(_declaration), 'review_declarations': _array(_nonempty),
                       'reconsiders_record_id': _nullable(_uuid), 'server_incarnation_id': _uuid, 'state': _choice('READY')},
    'AssignedIds': {'approval_id': _nullable(_uuid), 'event_id': _nullable(_uuid)},
    'FrozenCommand': {'command_version': _choice(1), 'request': lambda v, p: _request(v, p), 'request_sha256': _hex,
                      'key_id': _label, 'principal_id': _principal, 'actor': _nonempty, 'at': _utc, 'authorization': 'Authorization',
                      'assigned_ids': 'AssignedIds', 'storage_epoch_id': _uuid, 'expected_result': 'ContentHead', 'review_snapshot': _nullable('ReviewSnapshot')},
    'ReceiptCore': {'receipt_core_version': _choice(1), 'request_id': _uuid, 'request_sha256': _hex, 'storage_epoch_id': _uuid,
                    'operation': _choice(*_operations), 'tx_seq': _nullable(_uint),
                    'status': _choice('INITIALIZED', 'COMMITTED', 'ABORTED_PRECOMMIT', 'REPAIRED'),
                    'result_content_head': _nullable('ContentHead'), 'approval_ids': _array(_uuid), 'event_ids': _array(_uuid), 'abort_code': _nullable(_abort)},
    'ReceiptBody': {'receipt_version': _choice(1), 'core': 'ReceiptCore', 'terminal_ref': 'JournalRef', 'result_head': _nullable('CommittedHead'), 'key_id': _label},
    'Pending': {'pending_version': _choice(1), 'phase': _choice('PREPARED', 'PUBLISH_INTENT'), 'plan_ref': 'BlobRef',
                'prepare_ref': 'JournalRef', 'intent_ref': _nullable('JournalRef')},
    'AnchorBody': {'anchor_version': _choice(1), 'production_id': _uuid, 'machine_binding_id': _uuid, 'storage_epoch_id': _uuid,
                   'activation': _choice('INITIALIZING', 'ACTIVE', 'INITIALIZATION_ABORTED'), 'stable_head': _nullable('CommittedHead'),
                   'reserved_tx_high_watermark': _uint, 'journal_tail': 'JournalRef', 'pending': _nullable('Pending'), 'history_guard': 'HistoryGuard', 'key_id': _label},
    'InitializationBody': {'initialization_version': _choice(1), 'request_id': _uuid, 'request_sha256': _hex,
                           'production_id': _uuid, 'machine_binding_id': _uuid, 'storage_epoch_id': _uuid,
                           'managed_root_token': _uuid, 'source_ref': 'BlobRef', 'principal_id': _principal,
                           'actor': _nonempty, 'at': _utc, 'policy_ref': 'PolicyRef', 'authorization': 'Authorization', 'guard_before': 'HistoryGuard', 'key_id': _label},
    'RegistrationBody': {'registration_version': _choice(1), 'storage_protocol_version': _choice(1), 'production_id': _uuid,
                         'machine_binding_id': _uuid, 'storage_epoch_id': _uuid, 'managed_root_token': _uuid,
                         'initialization_ref': 'BlobRef', 'storage_profile_id': _label, 'key_id': _label},
    'ApprovalRecord': _approval,
}


def _request(v, p):
    base = {'request_version': _choice(1), 'request_id': _uuid, 'production_id': _uuid, 'storage_epoch_id': _nullable(_uuid),
            'expected_head': _nullable('CommittedHead'), 'review_session_id': _nullable(_uuid),
            'operation': _choice(*_operations, 'PUBLISH_REVISION'), 'parameters': lambda v, p: None}
    _check(v, base, p)
    op = v['operation']
    if op == 'PUBLISH_REVISION':
        _check(v['parameters'], {'proposal_ref': 'BlobRef', 'reason': _nonempty}, p + '.parameters')
        _fail('OPERATION_NOT_AVAILABLE', p + '.operation', 'PUBLISH_REVISION is disabled')
    params = {'INITIALIZE_EMPTY': {'draft_ref': 'BlobRef'}, 'IMPORT_BASELINE': {'source_ref': 'BlobRef'},
              'TRANSFER_BASELINE': {'source_ref': 'BlobRef', 'manifest_ref': 'BlobRef'}, 'MIGRATE_SCHEMA': {},
              'RESTORE_EXACT_HEAD': {'image_ref': 'BlobRef', 'expected_observation': lambda v, p: _observation(v, p)},
              'RECORD_DECISION': {'decision_key': 'DecisionKey', 'decision': _decision, 'reason': _nonempty, 'reconsiders_record_id': _nullable(_uuid)}}
    _check(v['parameters'], params[op], p + '.parameters')
    initial = op in ('INITIALIZE_EMPTY', 'IMPORT_BASELINE', 'TRANSFER_BASELINE')
    if (v['storage_epoch_id'] is None) != initial or (v['expected_head'] is None) != initial:
        _fail('TYPE', p + '.expected_head', 'Invalid genesis/non-genesis binding')
    if (v['review_session_id'] is not None) != (op == 'RECORD_DECISION'):
        _fail('SESSION_BINDING_MISMATCH', p + '.review_session_id', 'Session required only for decision')


def _observation(v, p):
    if type(v) is not dict or 'state' not in v:
        _fail('MISSING_FIELD', p + '.state', 'Observation tag required')
    _check(v, {'state': _choice('MISSING')} if v['state'] == 'MISSING' else
           {'state': _choice('PRESENT'), 'file_ref': 'BlobRef'}, p)


_SCHEMAS['Request'] = _request


def validate_wire(value, kind):
    """Validate a supported closed wire type, without claiming graph/authority validity."""
    if type(kind) is not str or kind not in _SCHEMAS:
        _fail('BLOB_TYPE_MISMATCH', '$', 'Unknown wire type')
    bound = MAX_REQUEST_BYTES if kind == 'Request' else MAX_COMMAND_BYTES if kind == 'FrozenCommand' else MAX_BLOB_BYTES
    canonical_json(value, max_bytes=bound)
    _check(value, kind)
    _bindings(value, kind)


def _bindings(v, kind):
    if kind == 'FrozenCommand':
        q, a = v['request'], v['authorization']
        op = q['operation']
        needed = ('INITIALIZE' if op in ('INITIALIZE_EMPTY', 'IMPORT_BASELINE', 'TRANSFER_BASELINE') else
                  'RECOVERY' if op == 'RESTORE_EXACT_HEAD' else op)
        grant = None if op != 'RECORD_DECISION' else {'gate': q['parameters']['decision_key']['gate'], 'decision': q['parameters']['decision']}
        if (a['principal_id'] != v['principal_id'] or a['command_grants'] != ['PROTECTED_SNAPSHOT_WRITE', needed]
                or a['gate_decision_grant'] != grant):
            _fail('AUTHORIZATION_BINDING_MISMATCH', '$.authorization', 'Incorrect frozen grants/principal')
        if v['request_sha256'] != request_digest(q):
            raise CryptographicError('BLOB_HASH_MISMATCH', '$.request_sha256', 'Request digest mismatch')
        initial = op in ('INITIALIZE_EMPTY', 'IMPORT_BASELINE', 'TRANSFER_BASELINE')
        expected_ids = (False, False) if initial or op == 'RESTORE_EXACT_HEAD' else (op == 'RECORD_DECISION', True)
        actual_ids = tuple(v['assigned_ids'][k] is not None for k in ('approval_id', 'event_id'))
        if actual_ids != expected_ids:
            _fail('TYPE', '$.assigned_ids', 'IDs do not match operation')
        if v['storage_epoch_id'] != v['expected_result']['storage_epoch_id'] or q['production_id'] != v['expected_result']['production_id']:
            _fail('EPOCH_MISMATCH', '$.expected_result', 'Command/head context mismatch')
        if not initial and q['storage_epoch_id'] != v['storage_epoch_id']:
            _fail('EPOCH_MISMATCH', '$.storage_epoch_id', 'Request epoch mismatch')
        r = v['review_snapshot']
        if op == 'RECORD_DECISION':
            if r is None:
                _fail('MISSING_FIELD', '$.review_snapshot', 'Decision requires READY review')
            if (r['principal_id'] != v['principal_id'] or r['policy_ref'] != a['policy_ref'] or
                    r['session_id'] != q['review_session_id'] or r['decision_key'] != q['parameters']['decision_key'] or
                    r['reconsiders_record_id'] != q['parameters']['reconsiders_record_id']):
                _fail('SESSION_BINDING_MISMATCH', '$.review_snapshot', 'Review/request binding mismatch')
            from .schema2_model import required_declaration_codes
            codes = list(required_declaration_codes(r['decision_key']['gate'], q['parameters']['decision']))
            if r['confirmed_codes'] != codes:
                _fail('TYPE', '$.review_snapshot.confirmed_codes', 'Wrong declaration codes/order')
        elif r is not None:
            _fail('SESSION_BINDING_MISMATCH', '$.review_snapshot', 'Review only for decision')
    if kind in ('AnchorState', 'Receipt', 'InitializationAuthorization', 'Registration'):
        body_kind = {'AnchorState': 'AnchorBody', 'Receipt': 'ReceiptBody',
                     'InitializationAuthorization': 'InitializationBody', 'Registration': 'RegistrationBody'}[kind]
        _bindings(v['body'], body_kind)
    if kind == 'ReceiptBody':
        _bindings(v['core'], 'ReceiptCore')
        if v['result_head'] is not None and v['core']['result_content_head'] != v['result_head']['content_head']:
            _fail('TYPE', '$.result_head', 'Receipt head/core mismatch')
    if kind == 'ReceiptCore':
        aborted = v['status'] == 'ABORTED_PRECOMMIT'
        if aborted != (v['abort_code'] is not None) or (aborted and (v['approval_ids'] or v['event_ids'])):
            _fail('TYPE', '$.abort_code', 'Invalid abort receipt')
        if not aborted and v['result_content_head'] is None:
            _fail('MISSING_FIELD', '$.result_content_head', 'Successful receipt requires content head')
    if kind == 'TransactionPlan':
        head = v['new_content_head']
        if v['image_ref'] != {'sha256': head['snapshot_file_sha256'], 'byte_length': head['snapshot_file_length']}:
            _fail('PLAN_INVALID', '$.image_ref', 'Image/head mismatch')
        if v['kind'] == 'GENESIS':
            good = v['base_head'] is None and v['tx_seq'] == 0 and v['initialization_ref'] is not None
        elif v['kind'] == 'REPAIR_EXACT':
            good = v['base_head'] is not None and v['tx_seq'] is None and head == v['base_head']['content_head']
        else:
            good = (v['base_head'] is not None and v['tx_seq'] is not None and
                    head['generation'] == v['base_head']['content_head']['generation'] + 1)
        if not good:
            _fail('PLAN_INVALID', '$.kind', 'Plan kind/head/sequence mismatch')
        _bindings(v['expected_commit_receipt'], 'ReceiptCore')
    if kind == 'InitializationBody':
        a = v['authorization']
        if (a['principal_id'] != v['principal_id'] or a['policy_ref'] != v['policy_ref']
                or a['command_grants'] != ['PROTECTED_SNAPSHOT_WRITE', 'INITIALIZE'] or a['gate_decision_grant'] is not None):
            _fail('AUTHORIZATION_BINDING_MISMATCH', '$.authorization', 'Incorrect initialization binding')
    if kind == 'AnchorBody':
        pending = v['pending']
        if pending and ((pending['phase'] == 'PREPARED') != (pending['intent_ref'] is None)):
            _fail('TYPE', '$.pending.intent_ref', 'Phase/reference mismatch')
        if v['activation'] == 'ACTIVE' and v['stable_head'] is None:
            _fail('MISSING_FIELD', '$.stable_head', 'Active anchor requires head')
        if v['activation'] == 'INITIALIZATION_ABORTED' and (v['stable_head'] is not None or pending is not None):
            _fail('TYPE', '$.activation', 'Aborted genesis cannot be active/pending')


def blob_ref(data):
    if type(data) is not bytes:
        _fail('TYPE', '$', 'Expected blob bytes')
    if not 1 <= len(data) <= MAX_BLOB_BYTES:
        _fail('LIMIT', '$', 'Invalid blob bytes')
    return {'sha256': hashlib.sha256(data).hexdigest(), 'byte_length': len(data)}


def verify_blob(data, reference, kind):
    """Check exact bytes/ref plus expected closed type; no lookup or type guessing."""
    _check(reference, 'BlobRef')
    actual = blob_ref(data)
    if actual != reference:
        raise CryptographicError('BLOB_HASH_MISMATCH', '$', 'Blob hash/length mismatch')
    value = decode_canonical_json(data)
    if type(kind) is not str or kind not in _SCHEMAS:
        _fail('BLOB_TYPE_MISMATCH', '$', 'Unsupported expected type')
    try:
        validate_wire(value, kind)
    except StructuralError as error:
        raise StructuralError('BLOB_TYPE_MISMATCH', error.path, str(error)) from error
    return value


def _key(key):
    if type(key) is not bytes or len(key) != 32:
        raise CryptographicError('KEY_UNAVAILABLE', '$.key', 'Explicit 32-byte key required')


def _mac(domain, data, key):
    _key(key)
    return hmac.new(key, _DOMAINS[domain] + data, hashlib.sha256).hexdigest()


def request_digest(value):
    validate_wire(value, 'Request')
    return hashlib.sha256(_DOMAINS['request'] + canonical_json(value)).hexdigest()


def approval_wire_digest(value):
    validate_wire(value, 'ApprovalRecord')
    return hashlib.sha256(_DOMAINS['approval'] + canonical_json(value)).hexdigest()


def _body_mac(value, kind, domain, key):
    validate_wire(value, kind)
    return _mac(domain, canonical_json(value), key)


def frozen_command_mac(value, key):
    return _body_mac(value, 'FrozenCommand', 'command', key)


def anchor_mac(value, key):
    return _body_mac(value, 'AnchorBody', 'anchor', key)


def receipt_mac(value, key):
    return _body_mac(value, 'ReceiptBody', 'receipt', key)


def initialization_mac(value, key):
    return _body_mac(value, 'InitializationBody', 'initialize', key)


def registration_mac(value, key):
    return _body_mac(value, 'RegistrationBody', 'registration', key)


def verify_mac(value, supplied_mac, key, *, domain):
    """Validate body/schema then compare the selected MAC in constant time."""
    functions = {'command': frozen_command_mac, 'anchor': anchor_mac, 'receipt': receipt_mac,
                 'initialize': initialization_mac, 'registration': registration_mac}
    if domain not in functions:
        _fail('TYPE', '$.domain', 'Unsupported body MAC domain')
    _hex(supplied_mac, '$.mac')
    expected = functions[domain](value, key)
    if not hmac.compare_digest(expected, supplied_mac):
        raise CryptographicError('MAC_MISMATCH', '$.mac', 'MAC mismatch')


def _journal(v, p):
    _check(v, {'journal_record_version': _choice(1), 'production_id': _uuid, 'machine_binding_id': _uuid,
               'storage_epoch_id': _uuid, 'record_index': _uint, 'previous_record_mac': _nullable(_hex),
               'key_id': _label, 'record_type': _choice('PREPARE', 'PUBLISH_INTENT', 'SNAPSHOT_COMMIT', 'GENESIS', 'REPAIR_COMMIT', 'ABORT'),
               'payload': lambda v, p: None}, p)
    t, payload = v['record_type'], v['payload']
    schema = {'plan_ref': 'BlobRef'}
    if t != 'PREPARE':
        schema['prepare_ref'] = 'JournalRef'
    if t in ('SNAPSHOT_COMMIT', 'GENESIS', 'REPAIR_COMMIT'):
        schema.update(intent_ref='JournalRef', receipt_core='ReceiptCore')
    if t == 'ABORT':
        schema.update(abort_code=_abort, receipt_core='ReceiptCore', result_guard='HistoryGuard')
    _check(payload, schema, p + '.payload')
    if v['record_index'] == 0:
        if t != 'PREPARE' or v['previous_record_mac'] is not None:
            _fail('JOURNAL_TRANSITION_INVALID', p + '.record_index', 'First record must be genesis PREPARE')
    elif v['previous_record_mac'] is None:
        _fail('MISSING_FIELD', p + '.previous_record_mac', 'Nonfirst record requires previous MAC')
    if t != 'PREPARE' and payload['prepare_ref']['record_index'] >= v['record_index']:
        _fail('JOURNAL_TRANSITION_INVALID', p + '.payload.prepare_ref', 'PREPARE must precede this record')
    if 'intent_ref' in payload and not payload['prepare_ref']['record_index'] < payload['intent_ref']['record_index'] < v['record_index']:
        _fail('JOURNAL_TRANSITION_INVALID', p + '.payload.intent_ref', 'INTENT must lie between PREPARE and terminal')
    if 'receipt_core' in payload:
        _bindings(payload['receipt_core'], 'ReceiptCore')
        core = payload['receipt_core']
        if core['storage_epoch_id'] != v['storage_epoch_id']:
            _fail('EPOCH_MISMATCH', p + '.payload.receipt_core.storage_epoch_id', 'Wrong epoch')
        if t == 'ABORT':
            if core['status'] != 'ABORTED_PRECOMMIT' or core['abort_code'] != payload['abort_code'] or core['approval_ids'] or core['event_ids']:
                _fail('JOURNAL_TRANSITION_INVALID', p + '.payload.receipt_core', 'Invalid abort core')
        else:
            status, seq = {'GENESIS': ('INITIALIZED', 0), 'SNAPSHOT_COMMIT': ('COMMITTED', _UNSET), 'REPAIR_COMMIT': ('REPAIRED', None)}[t]
            if core['status'] != status or core['abort_code'] is not None or (seq is not _UNSET and core['tx_seq'] != seq):
                _fail('JOURNAL_TRANSITION_INVALID', p + '.payload.receipt_core', 'Invalid commit core')


_SCHEMAS['JournalRecord'] = _journal


def _context(record, expected_index, previous_mac, context):
    if expected_index is not None:
        _uint(expected_index, '$.expected_index')
        if record['record_index'] != expected_index:
            _fail('JOURNAL_TRANSITION_INVALID', '$.record_index', 'Index gap/fork')
    if previous_mac is not _UNSET:
        if previous_mac is not None:
            _hex(previous_mac, '$.previous_mac')
        if record['previous_record_mac'] != previous_mac:
            _fail('JOURNAL_PREFIX_MISMATCH', '$.previous_record_mac', 'Previous frame mismatch')
    if context is not None:
        _check(context, {'production_id': _uuid, 'machine_binding_id': _uuid, 'storage_epoch_id': _uuid, 'key_id': _label})
        for field, value in context.items():
            if record[field] != value:
                _fail('JOURNAL_TRANSITION_INVALID', '$.' + field, 'Context mismatch')


def journal_frame_mac(record, key):
    validate_wire(record, 'JournalRecord')
    payload = canonical_json(record, max_bytes=MAX_FRAME_PAYLOAD)
    header = _MAGIC + len(payload).to_bytes(4, 'big')
    return _mac('journal', header + payload, key)


def encode_journal_frame(record, key, *, expected_index=None, previous_mac=_UNSET, context=None):
    validate_wire(record, 'JournalRecord')
    _context(record, expected_index, previous_mac, context)
    payload = canonical_json(record, max_bytes=MAX_FRAME_PAYLOAD)
    header = _MAGIC + len(payload).to_bytes(4, 'big')
    return header + payload + bytes.fromhex(_mac('journal', header + payload, key))


def decode_journal_frame(frame, key, *, expected_index=None, previous_mac=_UNSET, context=None):
    """Verify exactly one complete frame; never scan, skip, repair, or return a prefix."""
    if type(frame) is not bytes:
        _fail('TYPE', '$', 'Expected frame bytes')
    if len(frame) < 8 or frame[:4] != _MAGIC:
        _fail('WIRE_FORMAT', '$.header', 'Bad/incomplete header')
    n = int.from_bytes(frame[4:8], 'big')
    if not 1 <= n <= MAX_FRAME_PAYLOAD:
        _fail('LIMIT', '$.header.payload_length', 'Payload outside wire bound')
    if len(frame) != 8 + n + 32:
        _fail('WIRE_FORMAT', '$', 'Incomplete frame or extra trailing bytes')
    record = decode_canonical_json(frame[8:8 + n], max_bytes=MAX_FRAME_PAYLOAD)
    validate_wire(record, 'JournalRecord')
    _key(key)
    expected = bytes.fromhex(_mac('journal', frame[:8 + n], key))
    if not hmac.compare_digest(expected, frame[8 + n:]):
        raise CryptographicError('MAC_MISMATCH', '$.mac', 'Frame MAC mismatch')
    _context(record, expected_index, previous_mac, context)
    return record


def verify_journal_frames(frames, key, *, context=None):
    """Check a complete in-memory sequence from index zero, atomically.

    This checks wire/MAC chain/context, not W0–W9 transitions or dereferenced
    plans/guards. Those require the separately reviewed S2.2 model.
    """
    if type(frames) is not list or not frames:
        _fail('TYPE', '$', 'Nonempty list of complete frame bytes required')
    records, previous = [], None
    for index, frame in enumerate(frames):
        record = decode_journal_frame(frame, key, expected_index=index, previous_mac=previous, context=context)
        if context is None:
            context = {k: record[k] for k in ('production_id', 'machine_binding_id', 'storage_epoch_id', 'key_id')}
        previous = frame[-32:].hex()
        records.append(record)
    return records

# Typed proof blobs: schema validity is separate from walking retained chains.
_SCHEMAS.update({
    'FileObservation': _observation,
    'InheritedApproval': {'approval_id': _uuid, 'decision_key': 'DecisionKey', 'decision': _decision,
                          'approval_record_sha256': _hex, 'evidence_attestation_digest': _nullable(_hex)},
    'BaselineBlob': {'blob_version': _choice(1), 'blob_type': _choice('BASELINE'), 'production_id': _uuid,
                     'storage_epoch_id': _uuid, 'source_schema_version': _choice(1, 2), 'source_snapshot_ref': 'BlobRef',
                     'inherited_approvals': _array('InheritedApproval', maximum=10_000)},
    'LedgerEntry': {'request_id': _uuid, 'review_session_id': _nullable(_uuid), 'request_sha256': _hex, 'command_mac': _hex,
                    'key_id': _label, 'tx_seq': _nullable(_uint), 'outcome': _choice('INITIALIZED', 'COMMITTED', 'ABORTED_PRECOMMIT', 'REPAIRED'), 'receipt_core_sha256': _hex},
    'BarrierEntry': {'decision_key': 'DecisionKey', 'barrier_kind': _choice('REJECT', 'REVISE', 'REVOKE', 'UNVERIFIED_HISTORY'),
                     'source': lambda v, p: _decision_source(v, p)},
    'LineageEntry': {'production_id': _uuid, 'machine_binding_id': _nullable(_uuid), 'storage_epoch_id': _nullable(_uuid),
                     'source_snapshot_ref': 'BlobRef', 'parent_head': _nullable('CommittedHead'), 'parent_guard': _nullable('HistoryGuard'),
                     'parent_terminal_ref': _nullable('JournalRef'), 'order_status': _choice('UNVERIFIED', 'VERIFIED_LOCAL_PARENT')},
    'TransferManifest': {'transfer_manifest_version': _choice(1), 'production_id': _uuid, 'source_ref': 'BlobRef',
                         'source_machine_id': _nullable(_uuid), 'source_epoch_id': _nullable(_uuid), 'source_head': _nullable('CommittedHead'), 'source_guard': _nullable('HistoryGuard')},
    'ApprovalBinding': {'approval_id': _uuid, 'decision_key': 'DecisionKey', 'decision': _decision, 'approval_record_sha256': _hex, 'evidence_attestation_digest': _hex},
    'TransactionPlan': {'plan_version': _choice(1), 'kind': _choice('GENESIS', 'PUBLISH', 'REPAIR_EXACT'),
                        'request_id': _uuid, 'review_session_id': _nullable(_uuid), 'tx_seq': _nullable(_uint), 'key_id': _label,
                        'command_ref': 'BlobRef', 'command_mac': _hex, 'base_head': _nullable('CommittedHead'), 'observed_primary': 'FileObservation',
                        'new_content_head': 'ContentHead', 'image_ref': 'BlobRef', 'guard_before': 'HistoryGuard', 'guard_commit': 'HistoryGuard',
                        'expected_commit_receipt': 'ReceiptCore', 'new_approvals': _array('ApprovalBinding', maximum=1),
                        'initialization_ref': _nullable('BlobRef'), 'storage_profile_id': _label},
    'InitializationAuthorization': {'body': 'InitializationBody', 'mac': _hex},
    'Registration': {'body': 'RegistrationBody', 'mac': _hex},
    'AnchorState': {'body': 'AnchorBody', 'mac': _hex},
    'Receipt': {'body': 'ReceiptBody', 'mac': _hex},
})
for _name, _tag, _entry in (('LedgerBlob', 'LEDGER_DELTA', 'LedgerEntry'),
                             ('BarrierBlob', 'BARRIER_DELTA', 'BarrierEntry'),
                             ('LineageBlob', 'LINEAGE_DELTA', 'LineageEntry')):
    _SCHEMAS[_name] = {'blob_version': _choice(1), 'blob_type': _choice(_tag), 'production_id': _uuid,
                       'storage_epoch_id': _uuid, 'previous_ref': _nullable('BlobRef'), 'entries': _array(_entry, 1, 10_000)}
del _name, _tag, _entry


def _decision_source(v, p):
    if type(v) is not dict or 'source_kind' not in v:
        _fail('MISSING_FIELD', p + '.source_kind', 'Source tag required')
    schema = {'source_kind': _choice('LOCAL_TX'), 'storage_epoch_id': _uuid, 'tx_seq': _uint} if v['source_kind'] == 'LOCAL_TX' else {
        'source_kind': _choice('BASELINE'), 'baseline_ref': 'BlobRef'}
    _check(v, {**schema, 'approval_id': _uuid, 'approval_record_sha256': _hex}, p)


def verify_record_plan(record, plan, *, command=None):
    """Check supplied dereferenced plan/context bindings, without fetching anything.

    Does not replace full transition/guard/history replay; the caller must supply
    all required proofs to the later state machine before trusting a transaction.
    """
    validate_wire(record, 'JournalRecord')
    validate_wire(plan, 'TransactionPlan')
    if record['payload']['plan_ref'] != blob_ref(canonical_json(plan)):
        raise CryptographicError('BLOB_HASH_MISMATCH', '$.payload.plan_ref', 'Plan reference mismatch')
    head = plan['new_content_head']
    for field in ('production_id', 'machine_binding_id', 'storage_epoch_id'):
        if record[field] != head[field]:
            _fail('JOURNAL_TRANSITION_INVALID', '$.' + field, 'Plan context mismatch')
    if record['key_id'] != plan['key_id']:
        _fail('JOURNAL_TRANSITION_INVALID', '$.key_id', 'Plan key mismatch')
    t = record['record_type']
    if record['record_index'] == 0 and plan['kind'] != 'GENESIS':
        _fail('JOURNAL_TRANSITION_INVALID', '$.record_index', 'First PREPARE requires genesis plan')
    if t in ('GENESIS', 'SNAPSHOT_COMMIT', 'REPAIR_COMMIT'):
        required_kind = {'GENESIS': 'GENESIS', 'SNAPSHOT_COMMIT': 'PUBLISH', 'REPAIR_COMMIT': 'REPAIR_EXACT'}[t]
        if plan['kind'] != required_kind or record['payload']['receipt_core'] != plan['expected_commit_receipt']:
            _fail('JOURNAL_TRANSITION_INVALID', '$.payload.receipt_core', 'Terminal/plan mismatch')
    if command is not None:
        validate_wire(command, 'FrozenCommand')
        if plan['command_ref'] != blob_ref(canonical_json(command)):
            raise CryptographicError('BLOB_HASH_MISMATCH', '$.command_ref', 'Command reference mismatch')
        q = command['request']
        kind = ('GENESIS' if q['operation'] in ('INITIALIZE_EMPTY', 'IMPORT_BASELINE', 'TRANSFER_BASELINE') else
                'REPAIR_EXACT' if q['operation'] == 'RESTORE_EXACT_HEAD' else 'PUBLISH')
        if (plan['kind'] != kind or plan['request_id'] != q['request_id'] or plan['review_session_id'] != q['review_session_id']
                or plan['new_content_head'] != command['expected_result'] or plan['key_id'] != command['key_id']):
            _fail('JOURNAL_TRANSITION_INVALID', '$.command_ref', 'Command context mismatch')
