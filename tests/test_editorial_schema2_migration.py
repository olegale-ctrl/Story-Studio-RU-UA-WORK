"""Pure migration regressions and independently fixed output checksum vectors."""
import copy
from contextlib import ExitStack
from dataclasses import FrozenInstanceError, fields, replace
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

from editorial import codec as c
from editorial import model as m
from editorial.approval_consistency import evaluate_all_approval_consistency, _evaluate
from editorial.approval_history import _project, evaluate_approval_history, ApprovalHistoryState
from editorial.current_package import compute_current_dependency_digest
from editorial.graph import GraphValidationError
from editorial.integrity import HashVerificationError
from editorial.rights_binding import RightsBindingError
from editorial.schema2_integrity import (
    Schema2IntegrityError, compute_schema2_snapshot_checksum, validate_schema2_snapshot_integrity,
)
from editorial.schema2_migration import (
    Schema2MigrationError, Schema2MigrationResult, Schema2MigrationStatus as Status,
    migrate_schema1_to_schema2,
)
from editorial.schema2_model import Schema2Event, Schema2Snapshot
from editorial.snapshot_checksum import SnapshotChecksumError, compute_snapshot_checksum
from editorial.snapshot_integrity import validate_current_snapshot_integrity
from editorial.versioned_codec import decode_editorial_versioned, encode_editorial_versioned
from test_editorial_snapshot_integrity import full_snapshot, empty_snapshot, add_unreferenced_source
from test_editorial_approval_history import history_snapshot


ACTOR = '  Рецензент / Рецензентка И\u0306 Ї 😀  '
AT = '2026-11-05T13:00:00Z'
EVENT_ID = '50000000-0000-0000-0000-000000000900'
REASON = 'Editorial snapshot migrated from schema 1 to schema 2'
# Independent Node.js transform/serializer plus OpenSSL SHA-256; fixed literals.
GOLDEN_EMPTY = '015e310c17e7e7e47e4c276ce0f54d775fd79356bfaf8f54d1f2a9cca9c72fac'
GOLDEN_FULL = 'e71c83e7db4eb3cf57f9fc0a3172d3b82a03c5b773ad202ae21362f290966fb1'
GOLDEN_AMBIGUOUS = '1d547ff6a26f0f018ada3e309af8c60869f260ba550c92a690711e4e29da9aca'


def migrate(snapshot, **changes):
    values = dict(actor=ACTOR, at=AT, event_id=EVENT_ID)
    values.update(changes)
    return migrate_schema1_to_schema2(snapshot, **values)


def seal1(snapshot):
    return replace(snapshot, snapshot_checksum=compute_snapshot_checksum(snapshot))


def unchecked(value, **changes):
    result = object.__new__(type(value))
    for field in fields(value):
        object.__setattr__(result, field.name, changes.get(field.name, getattr(value, field.name)))
    return result


def ambiguous_source():
    return history_snapshot(((m.ApprovalDecision.REJECT, '2026-11-05T12:00:00Z'),
                             (m.ApprovalDecision.REVOKE, '2026-11-05T12:00:00Z')))[0]


class Schema2MigrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = full_snapshot()

    def error(self, source, cls, code, path, **kwargs):
        with self.assertRaises(cls) as caught:
            migrate(source, **kwargs)
        violation = caught.exception.violation
        self.assertIs(type(violation), m.Violation)
        self.assertEqual(violation.code, code)
        self.assertEqual(violation.field_path, path)
        return violation

    def test_empty_snapshot_migration_and_literal_checksum(self):
        source = empty_snapshot()
        result = migrate(source)
        self.assertIs(type(result), Schema2MigrationResult)
        self.assertIs(result.status, Status.MIGRATED)
        self.assertIs(type(result.snapshot), Schema2Snapshot)
        self.assertEqual(result.snapshot.base_snapshot.snapshot_checksum, GOLDEN_EMPTY)
        self.assertEqual(result.snapshot.base_snapshot.base.generation, 2)
        self.assertEqual(result.snapshot.approval_authority_evidence, ())
        self.assertTrue(validate_schema2_snapshot_integrity(result.snapshot).checksum_verified)

    def test_full_snapshot_migration_and_literal_checksum(self):
        result = migrate(self.source)
        self.assertEqual(result.snapshot.base_snapshot.snapshot_checksum, GOLDEN_FULL)
        integrity = validate_schema2_snapshot_integrity(result.snapshot)
        self.assertEqual(integrity.revision_count, len(self.source.base.revisions))
        self.assertEqual(len(integrity.material_bindings), 2)
        self.assertEqual(integrity.evidence_count, 0)

    def test_ambiguous_history_literal_checksum_and_preservation(self):
        source = ambiguous_source()
        result = migrate(source)
        self.assertEqual(result.snapshot.base_snapshot.snapshot_checksum, GOLDEN_AMBIGUOUS)
        self.assertEqual(result.snapshot.base_snapshot.base.approvals, source.base.approvals)
        integrity = validate_schema2_snapshot_integrity(result.snapshot)
        self.assertEqual(tuple(v.code for v in integrity.history_diagnostics), ('AMBIGUOUS_HISTORY',) * 2)
        self.assertEqual(integrity.transaction_order_status, 'UNVERIFIED_ORDERING')

    def test_exact_wire_transform_changes_only_four_existing_fields_and_adds_evidence(self):
        source_wire = json.loads(c.encode_snapshot(self.source))
        output_wire = json.loads(encode_editorial_versioned(migrate(self.source).snapshot))
        self.assertEqual(set(output_wire) - set(source_wire), {'approval_authority_evidence'})
        self.assertEqual(set(source_wire) - set(output_wire), set())
        changed_fields = {key for key in source_wire if source_wire[key] != output_wire[key]}
        self.assertEqual(changed_fields, {'editorial_schema_version', 'generation', 'events', 'snapshot_checksum'})
        self.assertEqual(output_wire['editorial_schema_version'], 2)
        self.assertEqual(output_wire['approval_authority_evidence'], [])
        self.assertEqual(output_wire['events'][:-1], source_wire['events'])

    def test_every_approval_field_is_preserved_literally(self):
        original = self.source.base.approvals[0]
        records = tuple(replace(original, id=f'50000000-0000-0000-0000-{n:012d}',
                                decision=decision, actor=ACTOR, reason='  Перевірка И\u0306 😀  ',
                                review_declarations=('  Декларація  ', 'Проверка е\u0301'))
                        for n, decision in enumerate(m.ApprovalDecision, 1))
        source = seal1(replace(self.source, base=replace(self.source.base, approvals=records)))
        output = migrate(source).snapshot.base_snapshot.base.approvals
        self.assertIs(output, source.base.approvals)
        for before, after in zip(records, output):
            self.assertIs(before, after)
            for field in fields(m.ApprovalRecord):
                self.assertEqual(getattr(before, field.name), getattr(after, field.name))

    def test_approval_order_is_neither_sorted_nor_resolved_by_uuid_or_time(self):
        original = self.source.base.approvals[0]
        records = tuple(replace(original, id=f'50000000-0000-0000-0000-{n:012d}', timestamp=timestamp)
                        for n, timestamp in ((9, '2026-11-05T12:00:00Z'),
                                             (1, '2026-11-05T10:00:00Z'),
                                             (7, '2026-11-05T11:00:00Z')))
        source = seal1(replace(self.source, base=replace(self.source.base, approvals=records)))
        self.assertEqual(migrate(source).snapshot.base_snapshot.base.approvals, records)

    def test_original_revisions_hashes_active_refs_and_companions_are_shared_unchanged(self):
        converted = migrate(self.source).snapshot.base_snapshot
        self.assertIs(converted.base.revisions, self.source.base.revisions)
        self.assertIs(converted.base.active_refs, self.source.base.active_refs)
        for field in ('source_details', 'claim_reviews', 'rights_details'):
            self.assertIs(getattr(converted, field), getattr(self.source, field))
        self.assertEqual(tuple(r.ref.content_hash for r in converted.base.revisions),
                         tuple(r.ref.content_hash for r in self.source.base.revisions))

    def test_old_events_keep_exact_order_fields_and_references(self):
        first = self.source.events[0]
        events = (replace(first, id='50000000-0000-0000-0000-000000000009', reason='  Перше 😀  '),
                  replace(first, id='50000000-0000-0000-0000-000000000001', reason='Второе И\u0306'))
        source = seal1(replace(self.source, events=events))
        output = migrate(source).snapshot.base_snapshot.events
        self.assertEqual(output[:-1], events)
        self.assertTrue(all(before is after for before, after in zip(events, output)))

    def test_migration_event_has_exact_explicit_fields(self):
        result = migrate(self.source)
        events = result.snapshot.base_snapshot.events
        self.assertEqual(len(events), len(self.source.events) + 1)
        event = events[-1]
        self.assertIs(type(event), Schema2Event)
        self.assertEqual(event, Schema2Event(EVENT_ID, ACTOR, AT, 'schema_migrated', (), REASON, None))
        self.assertEqual(sum(e.action == 'schema_migrated' for e in events), 1)

    def test_generation_increments_once_from_non_default_value(self):
        source = seal1(replace(self.source, base=replace(self.source.base, generation=41)))
        self.assertEqual(migrate(source).snapshot.base_snapshot.base.generation, 42)
        self.assertEqual(source.base.generation, 41)

    def test_generation_is_not_artificially_capped_at_64_bits(self):
        for generation in (2**63 - 1, 2**64 - 1, 10**100):
            with self.subTest(generation=generation):
                source = seal1(replace(empty_snapshot(), base=replace(empty_snapshot().base, generation=generation)))
                self.assertEqual(migrate(source).snapshot.base_snapshot.base.generation, generation + 1)

    def test_unrepresentable_generation_increment_fails_without_wrap_or_repair(self):
        maximum_digits = sys.get_int_max_str_digits()
        if maximum_digits == 0:
            # No decimal cap is configured: arbitrary-precision growth is valid.
            generation = 10**5000 - 1
            source = seal1(replace(empty_snapshot(), base=replace(empty_snapshot().base, generation=generation)))
            self.assertEqual(migrate(source).snapshot.base_snapshot.base.generation, generation + 1)
            return
        generation = 10**maximum_digits - 1
        source = seal1(replace(empty_snapshot(), base=replace(empty_snapshot().base, generation=generation)))
        self.error(source, Schema2MigrationError, 'GENERATION_OVERFLOW', '$.generation')
        self.assertEqual(source.base.generation, generation)

    def test_empty_evidence_and_legacy_status_never_authenticate_approvals(self):
        result = migrate(self.source)
        self.assertEqual(result.snapshot.approval_authority_evidence, ())
        integrity = validate_schema2_snapshot_integrity(result.snapshot)
        self.assertTrue(all(s.authority_status == 'UNAUTHENTICATED_LEGACY' for s in integrity.approval_statuses))
        self.assertEqual(integrity.unverified_aspects,
                         ('transaction_order', 'identity', 'signatures', 'authority_policy', 'head_anchor'))
        for value in (result, integrity):
            for field in ('authorized', 'authenticated', 'approved', 'effective', 'trusted_head', 'ready'):
                self.assertFalse(hasattr(value, field), field)

    def test_no_authority_evidence_fields_are_invented(self):
        output = json.loads(encode_editorial_versioned(migrate(self.source).snapshot))
        self.assertEqual(output['approval_authority_evidence'], [])
        self.assertEqual(output['approvals'], json.loads(c.encode_snapshot(self.source))['approvals'])
        for key in ('principal_id', 'authority_policy', 'review_session_id', 'request_id',
                    'attestation_digest', 'signature', 'reconsiders_record_id', 'head_anchor'):
            self.assertNotIn(key, output)
            self.assertNotIn(key, output['events'][-1])

    def test_new_checksum_uses_full_schema2_envelope(self):
        output = migrate(self.source).snapshot
        self.assertEqual(output.base_snapshot.snapshot_checksum, compute_schema2_snapshot_checksum(output))
        self.assertNotEqual(output.base_snapshot.snapshot_checksum, self.source.snapshot_checksum)
        self.assertTrue(validate_schema2_snapshot_integrity(output).checksum_verified)

    def test_schema2_output_round_trips_canonically(self):
        output = migrate(self.source).snapshot
        encoded = encode_editorial_versioned(output)
        self.assertEqual(decode_editorial_versioned(encoded), output)
        self.assertEqual(encode_editorial_versioned(decode_editorial_versioned(encoded)), encoded)

    def test_idempotent_call_returns_same_object_unchanged(self):
        output = migrate(self.source).snapshot
        before = encode_editorial_versioned(output)
        result = migrate(output, actor='Другой', at='2026-11-06T13:00:00Z',
                         event_id='50000000-0000-0000-0000-000000000901')
        self.assertIs(result.status, Status.ALREADY_MIGRATED)
        self.assertIs(result.snapshot, output)
        self.assertEqual(encode_editorial_versioned(result.snapshot), before)
        self.assertEqual(len(result.snapshot.base_snapshot.events), len(self.source.events) + 1)

    def test_already_migrated_skips_unused_event_parameter_validation(self):
        output = migrate(self.source).snapshot
        result = migrate(output, actor=None, at=object(), event_id=False)
        self.assertIs(result.snapshot, output)
        self.assertIs(result.status, Status.ALREADY_MIGRATED)

    def test_already_migrated_does_not_validate_or_repair_checksum(self):
        output = migrate(self.source).snapshot
        corrupt = replace(output, base_snapshot=replace(output.base_snapshot, snapshot_checksum='0' * 64))
        before = encode_editorial_versioned(corrupt)
        with patch('editorial.schema2_migration.validate_schema2_snapshot_integrity',
                   side_effect=AssertionError('No validation on no-op')):
            result = migrate(corrupt)
        self.assertIs(result.snapshot, corrupt)
        self.assertEqual(encode_editorial_versioned(result.snapshot), before)
        with self.assertRaises(Schema2IntegrityError):
            validate_schema2_snapshot_integrity(result.snapshot)

    def test_already_migrated_preserves_existing_evidence_and_signature(self):
        from test_editorial_schema2_integrity import populated, seal2
        output = seal2(populated(signed=True))
        before = encode_editorial_versioned(output)
        result = migrate(output)
        self.assertIs(result.snapshot, output)
        self.assertIs(result.snapshot.approval_authority_evidence, output.approval_authority_evidence)
        self.assertEqual(encode_editorial_versioned(result.snapshot), before)

    def test_migration_result_is_immutable(self):
        result = migrate(empty_snapshot())
        with self.assertRaises(FrozenInstanceError):
            result.status = Status.ALREADY_MIGRATED
        with self.assertRaises(FrozenInstanceError):
            result.snapshot = None

    def test_input_types_and_subclasses_are_rejected(self):
        class Derived1(m.ContractSnapshot):
            pass

        class Derived2(Schema2Snapshot):
            pass

        first = Derived1(**{f.name: getattr(self.source, f.name) for f in fields(self.source)})
        second = Derived2(self.source, ())
        for value in (None, {}, [], True, c.encode_snapshot(self.source), self.source.base, first, second):
            with self.subTest(type=type(value)):
                self.error(value, Schema2MigrationError, 'TYPE', '$')

    def test_wrong_embedded_schema_version_rejected_by_strict_source_codec(self):
        base = unchecked(self.source.base, editorial_schema_version=2)
        source = unchecked(self.source, base=base)
        self.error(source, c.EncodeError, 'INVALID_VALUE', '$.editorial_schema_version')

    def test_corrupt_source_checksum_is_not_repaired(self):
        source = replace(self.source, snapshot_checksum='0' * 64)
        self.error(source, SnapshotChecksumError, 'SNAPSHOT_CHECKSUM_MISMATCH', '$.snapshot_checksum')
        self.assertEqual(source.snapshot_checksum, '0' * 64)

    def test_invalid_graph_fails_before_conversion(self):
        source = full_snapshot(after=lambda wire: wire['candidates'][0]['source_refs'][0].update(revision=99))
        self.error(source, GraphValidationError, 'TARGET_REVISION_MISMATCH', '$.candidates[0].source_refs[0]')

    def test_referenced_revision_hash_failure_is_preserved(self):
        source = full_snapshot(after=lambda wire: wire['sources'][0].update(title='Changed source'))
        self.error(source, GraphValidationError, 'TARGET_HASH_INVALID', '$.sources[0].ref.content_hash')

    def test_unreferenced_revision_hash_failure_is_preserved(self):
        source = full_snapshot(after=lambda wire: add_unreferenced_source(wire))
        self.error(source, HashVerificationError, 'CONTENT_HASH_MISMATCH', '$.sources[1].ref.content_hash')

    def test_rights_binding_failure_is_preserved(self):
        source = full_snapshot(lambda wire: wire['assets'][0].update(sha256='b' * 64))
        self.error(source, RightsBindingError, 'MATERIAL_DIGEST_MISMATCH', '$.assets[0].sha256')

    def test_source_wire_contract_failure_has_exact_path(self):
        original = self.source.base.approvals[0]
        approval = replace(original, gate='UNKNOWN')
        source = replace(self.source, base=replace(self.source.base, approvals=(approval,)))
        self.error(source, c.EncodeError, 'INVALID_VALUE', '$.approvals[0].gate')

    def test_duplicate_source_records_rejected_by_strict_codec(self):
        source = unchecked(self.source, events=(self.source.events[0],) * 2)
        self.error(source, c.EncodeError, 'INVALID_VALUE', '$.events[1].id')

    def test_source_validation_precedes_event_and_output_construction(self):
        source = replace(self.source, snapshot_checksum='0' * 64)
        with patch('editorial.schema2_migration.Schema2Event') as event:
            self.error(source, SnapshotChecksumError, 'SNAPSHOT_CHECKSUM_MISMATCH',
                       '$.snapshot_checksum', actor=None, at=None, event_id=None)
        event.assert_not_called()

    def test_invalid_event_id(self):
        path = f'$.events[{len(self.source.events)}].id'
        for value in (None, True, 1, '', 'not-uuid', 'ABCDEFAB-CDEF-ABCD-EFAB-CDEFABCDEFAB'):
            with self.subTest(value=value):
                self.error(self.source, Schema2MigrationError, 'INVALID_VALUE', path, event_id=value)

    def test_event_id_conflict(self):
        self.error(self.source, Schema2MigrationError, 'DUPLICATE_EVENT_ID',
                   f'$.events[{len(self.source.events)}].id', event_id=self.source.events[0].id)

    def test_invalid_actor(self):
        for value in (None, True, 1, '', '  ', 'bad\ud800', 'x' * 100001):
            with self.subTest(type=type(value), length=len(value) if type(value) is str else None):
                self.error(self.source, Schema2MigrationError, 'INVALID_VALUE',
                           f'$.events[{len(self.source.events)}].actor', actor=value)

    def test_invalid_utc_timestamp_without_conversion(self):
        for value in (None, True, '', '2026-02-30T13:00:00Z', '2026-11-05T15:00:00+02:00',
                      '2026-11-05T13:00:00.000Z', '2026-11-05 13:00:00Z'):
            with self.subTest(value=value):
                self.error(self.source, Schema2MigrationError, 'INVALID_VALUE',
                           f'$.events[{len(self.source.events)}].at', at=value)

    def test_unicode_and_whitespace_preserved_everywhere(self):
        output = migrate(self.source).snapshot
        wire1 = json.loads(c.encode_snapshot(self.source))
        wire2 = json.loads(encode_editorial_versioned(output))
        for key in ('production_revisions', 'profiles', 'candidates', 'sources', 'claims',
                    'scripts', 'scene_plans', 'assets', 'rights_reviews', 'approvals'):
            self.assertEqual(wire2[key], wire1[key])
        self.assertEqual(wire2['events'][-1]['actor'], ACTOR)
        self.assertIn(ACTOR.encode('utf-8'), encode_editorial_versioned(output))

    def test_output_construction_error_is_structured_and_no_output_returns(self):
        violation = m.Violation('OUTPUT_SHAPE', '$.approval_authority_evidence', 'Injected constructor failure')
        with patch('editorial.schema2_migration.Schema2Snapshot', side_effect=m.ModelError(violation)):
            self.error(self.source, Schema2MigrationError, 'OUTPUT_SHAPE', '$.approval_authority_evidence')

    def test_unrepresentable_final_checksum_is_structured(self):
        with patch('editorial.schema2_migration.compute_schema2_snapshot_checksum', return_value='invalid'):
            self.error(self.source, Schema2MigrationError, 'INVALID_VALUE', '$.snapshot_checksum')

    def test_output_integrity_failure_propagates_without_partial_result(self):
        violation = m.Violation('SNAPSHOT_CHECKSUM_MISMATCH', '$.snapshot_checksum', 'Injected output failure')
        failure = Schema2IntegrityError(violation)
        before = copy.deepcopy(self.source)
        with patch('editorial.schema2_migration.validate_schema2_snapshot_integrity', side_effect=failure):
            with self.assertRaises(Schema2IntegrityError) as caught:
                migrate(self.source)
        self.assertIs(caught.exception, failure)
        self.assertEqual(self.source, before)

    def test_output_round_trip_failure_is_closed(self):
        with patch('editorial.schema2_migration.decode_editorial_versioned', return_value=self.source):
            self.error(self.source, Schema2MigrationError, 'MIGRATION_ROUND_TRIP_MISMATCH', '$')

    def test_output_event_collection_limit_is_not_silently_truncated(self):
        first = self.source.events[0]
        events = tuple(replace(first, id=f'60000000-0000-0000-0000-{n:012d}') for n in range(10000))
        source = seal1(replace(empty_snapshot(), events=tuple(replace(event, refs=()) for event in events)))
        self.error(source, Schema2MigrationError, 'INVALID_VALUE', '$.events')
        self.assertEqual(len(source.events), 10000)

    def test_input_is_unchanged_on_success_and_failures(self):
        before = copy.deepcopy(self.source)
        source_bytes = c.encode_snapshot(self.source)
        migrate(self.source)
        self.assertEqual(self.source, before)
        self.assertEqual(c.encode_snapshot(self.source), source_bytes)
        with self.assertRaises(Schema2MigrationError):
            migrate(self.source, actor=' ')
        self.assertEqual(self.source, before)

    def test_repeated_migration_of_same_source_is_deterministic(self):
        first = migrate(self.source)
        second = migrate(self.source)
        self.assertEqual(first, second)
        self.assertEqual(encode_editorial_versioned(first.snapshot), encode_editorial_versioned(second.snapshot))

    def test_schema1_codec_remains_unchanged_and_rejects_schema2(self):
        before = c.encode_snapshot(self.source)
        output = migrate(self.source).snapshot
        self.assertEqual(c.encode_snapshot(self.source), before)
        self.assertEqual(c.decode_snapshot(before), self.source)
        with self.assertRaises(c.DecodeError) as caught:
            c.decode_snapshot(encode_editorial_versioned(output))
        # The unchanged schema-1 codec checks closed root fields before version.
        self.assertEqual(caught.exception.violation.code, 'UNKNOWN_FIELD')
        self.assertEqual(caught.exception.violation.field_path, '$.approval_authority_evidence')
        unsupported = json.loads(before)
        unsupported['editorial_schema_version'] = 2
        with self.assertRaises(c.DecodeError) as caught:
            c.decode_snapshot(json.dumps(unsupported).encode('utf-8'))
        self.assertEqual(caught.exception.violation.field_path, '$.editorial_schema_version')

    def test_schema1_snapshot_cannot_contain_schema_migrated(self):
        event = Schema2Event(EVENT_ID, ACTOR, AT, 'schema_migrated', (), REASON, None)
        source = replace(self.source, events=self.source.events + (event,))
        self.error(source, c.EncodeError, 'INVALID_VALUE', f'$.events[{len(self.source.events)}].action')

    def test_no_automatic_downgrade_or_repeated_generation_increment(self):
        output = migrate(self.source).snapshot
        for _ in range(3):
            result = migrate(output)
            self.assertIs(result.snapshot, output)
            self.assertEqual(json.loads(encode_editorial_versioned(result.snapshot))['editorial_schema_version'], 2)
            self.assertEqual(result.snapshot.base_snapshot.base.generation, self.source.base.generation + 1)

    def test_recorded_history_projection_and_ambiguity_are_unchanged(self):
        for decisions in (
            ((m.ApprovalDecision.APPROVE, '2026-11-05T10:00:00Z'), (m.ApprovalDecision.REVOKE, '2026-11-05T11:00:00Z')),
            ((m.ApprovalDecision.REJECT, '2026-11-05T12:00:00Z'), (m.ApprovalDecision.REVOKE, '2026-11-05T12:00:00Z')),
            ((m.ApprovalDecision.REVISE, '2026-11-05T12:00:00Z'), (m.ApprovalDecision.REVISE, '2026-11-05T12:00:00Z')),
        ):
            source, target, digest, _ = history_snapshot(decisions)
            before = evaluate_approval_history(source, 'SCRIPT', 'policy-v1', target, digest)
            output = migrate(source).snapshot
            # Existing public history API requires schema 1; compare its exact
            # unchanged pure projection on the preserved records, without downgrade.
            after = _project(before.key, output.base_snapshot.base.approvals)
            self.assertEqual(after, before)
            if before.state is ApprovalHistoryState.AMBIGUOUS_HISTORY:
                self.assertIsNone(after.latest_record)

    def test_dependency_consistency_is_unchanged_without_granting_authority(self):
        source, _, _, _ = history_snapshot(((m.ApprovalDecision.APPROVE, '2026-11-05T10:00:00Z'),))
        before = evaluate_all_approval_consistency(source, 'SCRIPT', 'policy-v1')
        current = validate_current_snapshot_integrity(source, 'SCRIPT', 'policy-v1')
        output = migrate(source).snapshot
        after = tuple(_evaluate(record, current, 'policy-v1') for record in output.base_snapshot.base.approvals)
        self.assertEqual(after, before)
        self.assertEqual(compute_current_dependency_digest(output.base_snapshot, 'SCRIPT', 'policy-v1'),
                         compute_current_dependency_digest(source, 'SCRIPT', 'policy-v1'))
        self.assertEqual(validate_schema2_snapshot_integrity(output).approval_statuses[0].authority_status,
                         'UNAUTHENTICATED_LEGACY')

    def test_no_io_network_or_subprocess_side_effects(self):
        payload = c.encode_snapshot(self.source)
        code = '''
import sys
active = False
def guard(event, args):
    if active and (event == 'open' or event.startswith(('socket.', 'subprocess.', 'os.system'))):
        raise AssertionError(event)
sys.addaudithook(guard)
from editorial.codec import decode_snapshot
from editorial.schema2_migration import migrate_schema1_to_schema2
source = decode_snapshot(PAYLOAD)
active = True
first = migrate_schema1_to_schema2(source, actor=ACTOR, at=AT, event_id=EVENT_ID)
assert first.status.value == 'MIGRATED'
second = migrate_schema1_to_schema2(first.snapshot, actor=None, at=None, event_id=None)
assert second.snapshot is first.snapshot
'''.replace('PAYLOAD', repr(payload)).replace('ACTOR', repr(ACTOR)).replace('AT,', repr(AT) + ',').replace('EVENT_ID)', repr(EVENT_ID) + ')')
        result = subprocess.run([sys.executable, '-B', '-c', code], cwd=Path(__file__).resolve().parents[1],
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '')

    def test_no_clock_environment_uuid_generation_or_randomness(self):
        import editorial.schema2_model as s2
        with ExitStack() as stack:
            for target in ('builtins.open', 'io.open', 'os.open', 'os.getenv', 'os.urandom',
                           'uuid.uuid4', 'uuid.uuid1', 'time.time', 'time.monotonic', 'time.perf_counter',
                           'socket.socket', 'subprocess.Popen'):
                stack.enter_context(patch(target, side_effect=AssertionError(f'Forbidden: {target}')))
            for module in (c, s2):
                datetime = stack.enter_context(patch.object(module, 'datetime', wraps=module.datetime))
                for method in ('now', 'utcnow', 'today'):
                    getattr(datetime, method).side_effect = AssertionError('Clock access')
            first = migrate(self.source)
            self.assertIs(migrate(first.snapshot).snapshot, first.snapshot)
            with self.assertRaises(Schema2MigrationError):
                migrate(self.source, event_id='not-uuid')


if __name__ == '__main__':
    unittest.main()
