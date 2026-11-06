"""Closed LAB/1 byte buffers. This does not implement Windows message transport."""
import hashlib
import json
import re
from uuid import UUID

from editorial import storage_protocol_v1 as s1

SCOPE = 'STORY_STUDIO_S3_2_LAB'
MAX_EXECUTE = 1_052_672
MAX_SMALL = 4096
POLICIES = ('CG_INIT', 'CG_MIGRATE', 'CG_RECOVERY', 'CG_WRITER_ONLY', 'CG_NONE') + tuple(
    f'GD_{gate}_{decision}' for gate in ('SCRIPT', 'SCENES', 'HANDOFF')
    for decision in ('APPROVE', 'REJECT', 'REVISE', 'REVOKE'))
FAULTS = ('NONE', 'IMPERSONATE_FALSE', 'THREAD_TOKEN_QUERY_FALSE', 'REVERT_FALSE',
          'RESIDUAL_TOKEN', 'READ_STALL', 'DISPATCH_STALL', 'RESPONSE_LOSS',
          'CRASH_PRE_ADMISSION', 'CRASH_AFTER_RAM_FINAL', 'PRE_ADMISSION_DENY',
          'PAUSE_AFTER_RAM_PREPARE', 'PAUSE_AFTER_RAM_INTENT')
S1_ERRORS = ('TYPE', 'WIRE_FORMAT', 'UNKNOWN_FIELD', 'MISSING_FIELD', 'VERSION_UNSUPPORTED', 'LIMIT', 'AUTHENTICATION_REQUIRED', 'PERMISSION_DENIED', 'POLICY_UNAVAILABLE', 'OPERATION_NOT_AVAILABLE', 'AUTHORIZATION_BINDING_MISMATCH', 'SERVICE_UNAVAILABLE', 'PROTECTION_INVALID', 'PROFILE_UNQUALIFIED', 'LOCK_BUSY', 'EXPECTED_HEAD_MISMATCH', 'EPOCH_MISMATCH', 'IDEMPOTENCY_CONFLICT', 'SESSION_INVALIDATED', 'SESSION_BINDING_MISMATCH', 'COMMAND_NO_CHANGE', 'PLAN_INVALID', 'SEQUENCE_EXHAUSTED', 'GENERATION_UNREPRESENTABLE', 'EDITORIAL_WIRE_ERROR', 'SNAPSHOT_CHECKSUM_MISMATCH', 'REFERENCE_GRAPH_ERROR', 'REVISION_HASH_ERROR', 'RIGHTS_BINDING_ERROR', 'ATTESTATION_DIGEST_MISMATCH', 'ANCHOR_MISSING', 'ANCHOR_UNAVAILABLE', 'ANCHOR_MISMATCH', 'KEY_UNAVAILABLE', 'MAC_MISMATCH', 'JOURNAL_PREFIX_MISMATCH', 'JOURNAL_TRANSITION_INVALID', 'JOURNAL_TAIL_UNVERIFIABLE', 'BLOB_MISSING', 'BLOB_HASH_MISMATCH', 'BLOB_TYPE_MISMATCH', 'HISTORY_CONTINUITY_LOST', 'UNVERIFIED_ORDERING', 'RECONSIDERATION_MISMATCH', 'QUOTA_EXCEEDED', 'DISK_FULL', 'FLUSH_FAILED', 'REPLACE_FAILED', 'OUTCOME_UNKNOWN', 'RECOVERY_REQUIRED', 'OPTIONAL_CAPABILITY_DISABLED')
ERRORS = ('LAB_POLICY_DENIED', 'LAB_S1_REJECTED', 'LAB_FIXTURE_NOT_ALLOWED',
          'LAB_IDEMPOTENCY_CONFLICT', 'LAB_BUSY', 'LAB_CAPACITY', 'LAB_NOT_FOUND',
          'LAB_RESTART_UNKNOWN', 'LAB_ENGINE_FAILURE', 'LAB_RUN_MISMATCH')
OUTCOMES = ('MOCK_FINALIZED', 'MOCK_ABORTED', 'MOCK_PENDING', 'DENIED',
            'NOT_ADMITTED', 'UNKNOWN_AFTER_RESTART')
OPERATIONS = ('INITIALIZE_EMPTY', 'IMPORT_BASELINE', 'TRANSFER_BASELINE',
              'MIGRATE_SCHEMA', 'RESTORE_EXACT_HEAD', 'RECORD_DECISION')


class LabError(ValueError):
    def __init__(self, code='LAB_S1_REJECTED', path='$'):
        self.code, self.path = code, path
        super().__init__(f'{code} at {path}')


def require(condition, path='$'):
    if not condition:
        raise LabError(path=path)


def uuid(value):
    require(type(value) is str)
    try:
        require(str(UUID(value)) == value)
    except (ValueError, AttributeError):
        raise LabError() from None


def hexdigest(value):
    require(type(value) is str and re.fullmatch('[0-9a-f]{64}', value) is not None)


def shape(value, fields):
    require(type(value) is dict and set(value) == set(fields.split()))


def canonical(value):
    # A LAB root adds one container to S1's unmodified 64-container child bound.
    require(type(value) is dict and all(type(k) is str for k in value))
    try:
        body = b'{' + b','.join(s1.canonical_json(k) + b':' +
                s1.canonical_json(value[k], max_bytes=MAX_EXECUTE)
                for k in sorted(value)) + b'}'
    except s1.ProtocolError:
        raise LabError() from None
    require(len(body) <= MAX_EXECUTE)
    return body


def _parse(body):
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result)
            result[key] = value
        return result

    def forbidden(_):
        raise LabError()

    def integer(text):
        negative = text.startswith('-')
        digits = text[1:] if negative else text
        number = 0
        for i in range(0, len(digits), 9):
            chunk = digits[i:i + 9]
            number = number * 10 ** len(chunk) + int(chunk)
        return -number if negative else number

    try:
        text = body.decode('utf-8')
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
                require(depth <= 65)
            elif char in ']}':
                depth -= 1
        value = json.loads(text, object_pairs_hook=pairs, parse_float=forbidden,
                           parse_constant=forbidden, parse_int=integer)
        require(canonical(value) == body)
        return value
    except (UnicodeError, ValueError, RecursionError) as error:
        if isinstance(error, LabError):
            raise
        raise LabError() from None


def validate(value):
    require(type(value) is dict)
    common = 'lab_version scope kind run_id '
    kind = value.get('kind')
    fields = {
        'HELLO': 'nonce',
        'EXECUTE': 'incarnation_id request',
        'LOOKUP': 'incarnation_id request_id request_bytes_sha256',
        'ACK': 'response_sha256',
        'HELLO_RESULT': 'incarnation_id nonce limits_id fixture_set fixture_case lab_only',
        'RESULT': 'incarnation_id request_id request_bytes_sha256 outcome mock_admission mock_summary error lab_only',
    }
    require(type(kind) is str and kind in fields)
    shape(value, common + fields[kind])
    require(type(value['lab_version']) is int and value['lab_version'] == 1)
    require(value['scope'] == SCOPE)
    uuid(value['run_id'])
    if 'incarnation_id' in value:
        uuid(value['incarnation_id'])
    if kind in ('HELLO', 'HELLO_RESULT'):
        uuid(value['nonce'])
    if kind == 'EXECUTE':
        try:
            validate_request(value['request'])
        except s1.ProtocolError:
            raise LabError() from None
    if kind == 'ACK':
        hexdigest(value['response_sha256'])
    if kind == 'LOOKUP':
        uuid(value['request_id']); hexdigest(value['request_bytes_sha256'])
    if kind == 'HELLO_RESULT':
        require(value['limits_id'] == 'LAB_LIMITS_1' and value['fixture_set'] == 'S32_FIXTURES_1')
        shape(value['fixture_case'], 'policy_case fault_case')
        require(value['fixture_case']['policy_case'] in POLICIES and value['fixture_case']['fault_case'] in FAULTS)
    if kind in ('HELLO_RESULT', 'RESULT'):
        require(value['lab_only'] is True)
    if kind == 'RESULT':
        if value['request_id'] is not None:
            uuid(value['request_id'])
        if value['request_bytes_sha256'] is not None:
            hexdigest(value['request_bytes_sha256'])
        outcome, admission = value['outcome'], value['mock_admission']
        require(outcome in OUTCOMES and admission in ('NONE', 'RAM', 'UNKNOWN'))
        summary, error = value['mock_summary'], value['error']
        if summary is not None:
            shape(summary, 'operation status virtual_record_count value_sha256')
            require(summary['operation'] in OPERATIONS)
            require(summary['status'] in ('INITIALIZED', 'COMMITTED', 'ABORTED_PRECOMMIT', 'REPAIRED'))
            n = summary['virtual_record_count']
            require(type(n) is int and 0 <= n <= s1.U64_MAX)
            hexdigest(summary['value_sha256'])
        if error is not None:
            shape(error, 'code field_path s1_code')
            require(error['code'] in ERRORS)
            path = error['field_path']
            require(type(path) is str and len(path) <= 1024 and path.isascii() and path.startswith('$'))
            # S1's closed error vocabulary is validated through its ReceiptCore schema.
            if error['s1_code'] is not None:
                require(type(error['s1_code']) is str and error['s1_code'] in S1_ERRORS)
        if outcome in ('MOCK_FINALIZED', 'MOCK_ABORTED'):
            require(admission == 'RAM' and summary is not None and error is None)
            require((summary['status'] == 'ABORTED_PRECOMMIT') == (outcome == 'MOCK_ABORTED'))
            if outcome == 'MOCK_FINALIZED':
                expected = 'INITIALIZED' if summary['operation'] in OPERATIONS[:3] else 'REPAIRED' if summary['operation'] == 'RESTORE_EXACT_HEAD' else 'COMMITTED'
                require(summary['status'] == expected)
        elif outcome == 'MOCK_PENDING':
            require(admission in ('RAM', 'UNKNOWN') and summary is None)
            require(error is None or error['code'] == 'LAB_ENGINE_FAILURE')
        elif outcome in ('DENIED', 'NOT_ADMITTED'):
            require(admission == 'NONE' and summary is None and error is not None)
        else:
            require(admission == 'UNKNOWN' and summary is None and error is not None and error['code'] == 'LAB_RESTART_UNKNOWN')
    body = canonical(value)
    require(len(body) <= (MAX_EXECUTE if kind == 'EXECUTE' else MAX_SMALL))
    return body


def encode_lab(value):
    body = validate(value)
    return b'SSLB' + len(body).to_bytes(4, 'big') + body


def decode_lab(frame):
    require(type(frame) is bytes and len(frame) >= 8)
    require(frame[:4] == b'SSLB')
    n = int.from_bytes(frame[4:8], 'big')
    # Check header before slicing/decoding the body.
    require(0 < n <= MAX_EXECUTE and len(frame) == n + 8)
    value = _parse(frame[8:])
    validate(value)
    return value


def response_hash(frame):
    value = decode_lab(frame)
    require(value['kind'] in ('HELLO_RESULT', 'RESULT'))
    return hashlib.sha256(frame[8:]).hexdigest()


def lab_summary_sha256(receipt):
    if type(receipt) is not bytes:
        raise TypeError('Receipt bytes required')
    return hashlib.sha256(b'story-studio-s3-2-lab-result-v1' + bytes([0]) + receipt).hexdigest()


def validate_request(request):
    if type(request) is not dict or request.get('operation') != 'PUBLISH_REVISION':
        return s1.validate_wire(request, 'Request')
    shape(request, 'request_version request_id production_id storage_epoch_id expected_head review_session_id operation parameters')
    require(type(request['request_version']) is int and request['request_version'] == 1)
    for field in ('request_id','production_id'): uuid(request[field])
    for field in ('storage_epoch_id','review_session_id'):
        if request[field] is not None: uuid(request[field])
    if request['expected_head'] is not None: s1.validate_wire(request['expected_head'], 'CommittedHead')
    shape(request['parameters'], 'proposal_ref reason')
    s1.validate_wire(request['parameters']['proposal_ref'], 'BlobRef')
    require(type(request['parameters']['reason']) is str and bool(request['parameters']['reason']))
    s1.canonical_json(request, max_bytes=s1.MAX_REQUEST_BYTES)
