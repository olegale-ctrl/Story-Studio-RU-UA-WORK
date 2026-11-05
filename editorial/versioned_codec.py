"""Strict version dispatch and schema-2 JSON codec.

Schema 1 delegates to ``editorial.codec``. Schema 2 reuses that codec for the
unchanged flat envelope and adds authority evidence without migration, hashing,
authority evaluation, or I/O.
"""
from dataclasses import replace
import json

from . import codec as c
from . import model as m
from .schema2_model import (
    ApprovalAuthorityEvidence,
    Schema2Event,
    Schema2ModelError,
    Schema2Snapshot,
)

__all__ = (
    'decode_editorial_versioned',
    'encode_editorial_versioned',
)


_EVIDENCE_FIELDS = {
    'approval_id': c._uuid,
    'principal_id': c._text,
    'principal_display_name': c._text,
    'authority_policy_id': c._uuid,
    'authority_policy_version': c._text,
    'review_session_id': c._uuid,
    'request_id': c._uuid,
    'declaration_codes': c._array(c._text, 16),
    'attested_at': c._utc,
    'reconsiders_record_id': c._nullable(c._uuid),
    'attestation_digest': c._hash,
    'signing_key_id': c._nullable(c._text),
    'signature_algorithm': c._nullable(c._text),
    'signature': c._nullable(c._text),
}
_SCHEMA1_ROOT_FIELDS = tuple(name for name, _ in c._COLLECTIONS) + (
    'editorial_schema_version', 'production_id', 'generation', 'approvals',
    'events', 'active_refs', 'snapshot_checksum',
)
_SCHEMA2_ROOT_FIELDS = frozenset((*_SCHEMA1_ROOT_FIELDS, 'approval_authority_evidence'))


def _parsed_document(raw: bytes):
    if type(raw) is not bytes:
        c._error('$', 'TYPE', 'Expected bytes')
    if len(raw) > c.MAX_BYTES:
        c._error('$', 'LIMIT', 'Snapshot exceeds 32 MiB')
    if raw.startswith(b'\xef\xbb\xbf'):
        c._error('$', 'BOM', 'UTF-8 BOM is forbidden')
    try:
        text = raw.decode('utf-8', errors='strict')
    except UnicodeDecodeError:
        c._error('$', 'UTF8', 'Invalid UTF-8 bytes')
    c._depth(text)
    try:
        parsed = json.loads(
            text,
            object_pairs_hook=c._Pairs,
            parse_float=c._ForbiddenNumber,
            parse_constant=c._ForbiddenNumber,
        )
    except (ValueError, RecursionError):
        c._error('$', 'JSON', 'Invalid JSON syntax or integer token')
    return c._walk(parsed, '$')


def _version(data):
    if type(data) is not dict:
        c._error('$', 'TYPE', 'Expected an object')
    if 'editorial_schema_version' not in data:
        c._error('$.editorial_schema_version', 'MISSING_FIELD', 'Required field is absent')
    value = c._integer(data['editorial_schema_version'], '$.editorial_schema_version')
    if value not in (1, 2):
        c._error('$.editorial_schema_version', 'SCHEMA_VERSION', 'Unsupported editorial schema version')
    return value


def _evidence(value, path):
    fields = c._object(value, _EVIDENCE_FIELDS, path)
    try:
        return ApprovalAuthorityEvidence(**fields)
    except Schema2ModelError as error:
        suffix = error.violation.field_path
        if suffix.startswith('$.'):
            suffix = suffix[2:]
        field_path = f'{path}.{suffix}' if suffix else path
        c._error(field_path, error.violation.code, error.violation.message)


def _schema2_event(event):
    return Schema2Event(
        event.id, event.actor, event.at, 'schema_migrated', event.refs,
        event.reason, event.error_code,
    )


def _decode_schema2(data) -> Schema2Snapshot:
    missing = _SCHEMA2_ROOT_FIELDS - data.keys()
    extra = data.keys() - _SCHEMA2_ROOT_FIELDS
    if missing:
        c._error(c._field('$', sorted(missing)[0]), 'MISSING_FIELD', 'Required field is absent')
    if extra:
        c._error(c._field('$', sorted(extra)[0]), 'UNKNOWN_FIELD', 'Unknown field')

    evidence = c._array(_evidence)(
        data['approval_authority_evidence'], '$.approval_authority_evidence'
    )

    schema1_wire = dict(data)
    del schema1_wire['approval_authority_evidence']
    schema1_wire['editorial_schema_version'] = 1
    migrated_positions = []
    events = []
    for index, event in enumerate(schema1_wire['events'] if type(schema1_wire['events']) is list else ()):
        if type(event) is dict and event.get('action') == 'schema_migrated':
            event = dict(event)
            event['action'] = 'operation_failed'
            migrated_positions.append(index)
        events.append(event)
    if type(schema1_wire['events']) is list:
        schema1_wire['events'] = events

    base_bytes = json.dumps(
        schema1_wire, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False,
    ).encode('utf-8')
    base_snapshot = c.decode_snapshot(base_bytes)
    if migrated_positions:
        restored_events = list(base_snapshot.events)
        for index in migrated_positions:
            restored_events[index] = _schema2_event(restored_events[index])
        base_snapshot = replace(base_snapshot, events=tuple(restored_events))
    try:
        return Schema2Snapshot(base_snapshot, evidence, editorial_schema_version=2)
    except Schema2ModelError as error:
        c._error(error.violation.field_path, error.violation.code, error.violation.message)


def decode_editorial_versioned(data: bytes) -> m.ContractSnapshot | Schema2Snapshot:
    """Strictly decode schema 1 or 2 based only on the required root version."""
    parsed = _parsed_document(data)
    version = _version(parsed)
    if version == 1:
        return c.decode_snapshot(data)
    return _decode_schema2(parsed)


def _wire_evidence(value):
    return {
        'approval_id': value.approval_id,
        'principal_id': value.principal_id,
        'principal_display_name': value.principal_display_name,
        'authority_policy_id': value.authority_policy_id,
        'authority_policy_version': value.authority_policy_version,
        'review_session_id': value.review_session_id,
        'request_id': value.request_id,
        'declaration_codes': list(value.declaration_codes),
        'attested_at': value.attested_at,
        'reconsiders_record_id': value.reconsiders_record_id,
        'attestation_digest': value.attestation_digest,
        'signing_key_id': value.signing_key_id,
        'signature_algorithm': value.signature_algorithm,
        'signature': value.signature,
    }


def _schema1_encodable(snapshot):
    migrated_positions = []
    events = []
    for index, event in enumerate(snapshot.events):
        if type(event) is Schema2Event and event.action == 'schema_migrated':
            migrated_positions.append(index)
            event = m.Event(
                event.id, event.actor, event.at, 'operation_failed', event.refs,
                event.reason, event.error_code,
            )
        events.append(event)
    return replace(snapshot, events=tuple(events)), tuple(migrated_positions)


def encode_editorial_versioned(snapshot: m.ContractSnapshot | Schema2Snapshot) -> bytes:
    """Encode schema 1 or 2 canonically without changing stored checksums."""
    if type(snapshot) is m.ContractSnapshot:
        return c.encode_snapshot(snapshot)
    if type(snapshot) is not Schema2Snapshot:
        c._encode_error('$', 'TYPE', 'Expected ContractSnapshot or Schema2Snapshot')

    base, migrated_positions = _schema1_encodable(snapshot.base_snapshot)
    encoded_base = c.encode_snapshot(base)
    envelope = json.loads(encoded_base.decode('utf-8'))
    envelope['editorial_schema_version'] = 2
    envelope['approval_authority_evidence'] = [
        _wire_evidence(value) for value in snapshot.approval_authority_evidence
    ]
    for index in migrated_positions:
        envelope['events'][index]['action'] = 'schema_migrated'
    try:
        encoded = json.dumps(
            envelope, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False,
        ).encode('utf-8')
    except (TypeError, ValueError, OverflowError) as error:
        c._encode_error('$', 'INTERNAL_SHAPE', f'Unsupported schema-2 value: {error}')
    try:
        restored = decode_editorial_versioned(encoded)
    except c.DecodeError as error:
        violation = error.violation
        raise c.EncodeError(m.Violation(
            'INVALID_VALUE', violation.field_path, violation.message,
        )) from None
    if restored != snapshot:
        c._encode_error('$', 'NON_REVERSIBLE', 'Schema-2 snapshot cannot round-trip without information loss')
    return encoded
