"""Pure schema-1 to schema-2 conversion, without persistence or trust creation.

Actor/time/ID are caller-supplied descriptive event data. This module does not
authenticate their origin. Existing approvals gain no authority evidence.
"""
from dataclasses import dataclass, replace
from enum import Enum

from . import model as m
from .codec import encode_snapshot
from .schema2_integrity import (
    compute_schema2_snapshot_checksum,
    validate_schema2_snapshot_integrity,
)
from .schema2_model import Schema2Event, Schema2ModelError, Schema2Snapshot
from .snapshot_integrity import validate_snapshot_integrity
from .versioned_codec import decode_editorial_versioned, encode_editorial_versioned

__all__ = (
    'Schema2MigrationStatus',
    'Schema2MigrationResult',
    'Schema2MigrationError',
    'migrate_schema1_to_schema2',
)

_MIGRATION_REASON = 'Editorial snapshot migrated from schema 1 to schema 2'


class Schema2MigrationStatus(str, Enum):
    MIGRATED = 'MIGRATED'
    ALREADY_MIGRATED = 'ALREADY_MIGRATED'


@dataclass(frozen=True)
class Schema2MigrationResult:
    status: Schema2MigrationStatus
    snapshot: Schema2Snapshot


class Schema2MigrationError(Schema2ModelError):
    """Migration input/construction failure carrying an exact field path."""


def _fail(path, code, message):
    raise Schema2MigrationError(m.Violation(code, path, message))


def _construction_error(error, prefix='$'):
    violation = error.violation
    path = violation.field_path
    if not path.startswith('$'):
        path = f'{prefix}.{path}'
    return Schema2MigrationError(m.Violation(
        violation.code, path, violation.message, violation.object_ref,
    ))


def migrate_schema1_to_schema2(snapshot, *, actor, at, event_id) -> Schema2MigrationResult:
    """Validate schema 1 fully, convert, postvalidate, and return an immutable result.

    Exact Schema2Snapshot input is an unconditional identity-preserving no-op,
    even when its integrity is invalid or unused event parameters are invalid.
    ALREADY_MIGRATED attests only that no conversion occurred. Use the separate
    integrity API to check existing schema-2 data.
    """
    if type(snapshot) is Schema2Snapshot:
        return Schema2MigrationResult(Schema2MigrationStatus.ALREADY_MIGRATED, snapshot)
    if type(snapshot) is not m.ContractSnapshot:
        _fail('$', 'TYPE', 'Expected exact ContractSnapshot or Schema2Snapshot')

    # Public strict encoder checks schema version 1, the entire closed wire
    # contract, uniqueness, and exact decode/encode round-trip before output.
    encode_snapshot(snapshot)
    validate_snapshot_integrity(snapshot)

    event_path = f'$.events[{len(snapshot.events)}]'
    try:
        event = Schema2Event(event_id, actor, at, 'schema_migrated', (), _MIGRATION_REASON, None)
    except m.ModelError as error:
        raise _construction_error(error, event_path) from None
    if any(existing.id == event.id for existing in snapshot.events):
        _fail(f'{event_path}.id', 'DUPLICATE_EVENT_ID', 'Migration event id already exists')

    # The approved contract has no 64-bit ceiling. Python integers do not wrap.
    # An increment that cannot be represented by the existing JSON integer
    # encoder's decimal conversion limit must still fail, never clamp/reset.
    try:
        generation = snapshot.base.generation + 1
        str(generation)
    except (ValueError, OverflowError):
        _fail('$.generation', 'GENERATION_OVERFLOW',
              'Incremented generation cannot be represented by the existing wire integer rules')

    try:
        common = replace(snapshot, base=replace(snapshot.base, generation=generation),
                         events=snapshot.events + (event,))
        converted = Schema2Snapshot(common, ())
    except m.ModelError as error:
        raise _construction_error(error) from None

    # The source checksum is merely a format-valid temporary field excluded
    # from this computation. Only the new complete schema-2 checksum is saved.
    checksum = compute_schema2_snapshot_checksum(converted)
    try:
        converted = replace(converted, base_snapshot=replace(common, snapshot_checksum=checksum))
    except m.ModelError as error:
        raise _construction_error(error) from None
    validate_schema2_snapshot_integrity(converted)
    restored = decode_editorial_versioned(encode_editorial_versioned(converted))
    if restored != converted:
        _fail('$', 'MIGRATION_ROUND_TRIP_MISMATCH', 'Migrated snapshot did not round-trip exactly')
    return Schema2MigrationResult(Schema2MigrationStatus.MIGRATED, converted)
