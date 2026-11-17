"""Closed synthetic fixture factory; no production principals, keys or storage.

Plan builders adapted from the existing S2 synthetic test builders (pinned base).
They feed the unchanged TransactionModel; they do not implement transaction checks.
The embedded package is artificial test data, not editorial user content.
"""
import copy
import hashlib
import json
from uuid import UUID, uuid5
from editorial import storage_protocol_v1 as w
from editorial import storage_transaction_model_v1 as m
from .protocol import POLICIES, FAULTS, require

KEY = hashlib.sha256(b'story-studio-public-test-vector-key-v1').digest()
CONNECTION = '77777777-7777-4777-8777-777777777777'
ROOT = '55555555-5555-4555-8555-555555555555'
AT = '2026-11-05T00:00:00Z'
ACTOR = 'Synthetic LAB reviewer'
PRINCIPALS = {'A':'windows-sid:S-1-5-21-1000-1000-1000-1001',
              'B':'windows-sid:S-1-5-21-1000-1000-1000-1002'}
PROBES = ('INIT_EMPTY','IMPORT','TRANSFER','MIGRATE','RECOVERY') + POLICIES[5:]
ROLES = ('request','session','approval','event','production','machine','epoch','policy')
OPS = dict(zip(PROBES[:5], ('INITIALIZE_EMPTY','IMPORT_BASELINE','TRANSFER_BASELINE','MIGRATE_SCHEMA','RESTORE_EXACT_HEAD')))

def c(value):
    return w.canonical_json(value)

def ref(value):
    return w.blob_ref(c(value))

SEED = {'active_refs': {'candidate': {'content_hash': '4ffea2010baeb441582a86b21cfe0248766f78dcb5d8a4710ab8bd1563e82d83',
                               'id': '10000000-0000-0000-0000-000000000001',
                               'kind': 'candidate',
                               'revision': 1},
                 'production': {'content_hash': 'd9b2e672f947befb306ac2fa2b535caa5581ca3753a7fcd0e8ba22957080da21',
                                'id': '10000000-0000-0000-0000-000000000001',
                                'kind': 'production',
                                'revision': 1},
                 'scene_plan': {'content_hash': '33ddbf376b9ed36a939991a4ede72704260260fb714af8c7120bfb8b9a6a6579',
                                'id': '10000000-0000-0000-0000-000000000001',
                                'kind': 'scene_plan',
                                'revision': 1},
                 'script': {'content_hash': '57600db6c66b619a6a8b2e8e5b619f7ab549e6f3fcdbcefe12a5071480a9ab15',
                            'id': '10000000-0000-0000-0000-000000000001',
                            'kind': 'script',
                            'revision': 1}},
 'approval_authority_evidence': [],
 'approvals': [],
 'assets': [{'file_ref': 'media/кадр.png',
             'kind': 'image',
             'ref': {'content_hash': 'a592fa1bb7657e34f4ecca1267f36a0f060a3ded5a52d186e733d6a514673f43',
                     'id': '10000000-0000-0000-0000-000000000001',
                     'kind': 'asset',
                     'revision': 1},
             'rights_ref': {'content_hash': '2e710af646a98b1ed7f922acb4c8df2740a76cd194fb480e6fe3a68b87c205cd',
                            'id': '20000000-0000-0000-0000-000000000002',
                            'kind': 'rights_review',
                            'revision': 2},
             'scene_id': None,
             'script_ref': None,
             'sha256': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
             'text_digest': None}],
 'candidates': [{'assessment': [{'criterion_key': 'clarity', 'rating': 4, 'reason': 'Reason'}],
                 'discovery_input': 'Термос',
                 'discovery_method': 'manual_topic',
                 'rationale': None,
                 'ref': {'content_hash': '4ffea2010baeb441582a86b21cfe0248766f78dcb5d8a4710ab8bd1563e82d83',
                         'id': '10000000-0000-0000-0000-000000000001',
                         'kind': 'candidate',
                         'revision': 1},
                 'source_refs': [{'content_hash': '39c36db97dccd5fb1aa64d27a50d9decfd017fc8151d9bd4b7619a2331d3f417',
                                  'id': '10000000-0000-0000-0000-000000000001',
                                  'kind': 'source',
                                  'revision': 1}],
                 'summary': 'Описание',
                 'title': 'Тема'}],
 'claims': [{'claim_type': 'interpretation',
             'evidence_links': [{'explanation': 'Context',
                                 'locator': 'p.1',
                                 'relation': 'context',
                                 'reviewed_at': '2026-11-04T10:00:00Z',
                                 'reviewer': 'Owner',
                                 'source_ref': {'content_hash': '39c36db97dccd5fb1aa64d27a50d9decfd017fc8151d9bd4b7619a2331d3f417',
                                                'id': '10000000-0000-0000-0000-000000000001',
                                                'kind': 'source',
                                                'revision': 1}}],
             'materiality': 'material',
             'qualification': 'Возможно',
             'reason': 'Basis',
             'ref': {'content_hash': '972ee3870d01646bd5be7481f57d2e09b0ccaa3b2eadb1db97e6864fef9f4d73',
                     'id': '10000000-0000-0000-0000-000000000001',
                     'kind': 'claim',
                     'revision': 1},
             'review_status': 'qualified',
             'reviewed_at': '2026-11-04T10:00:00Z',
             'reviewer': 'Owner',
             'statement': 'Утверждение'}],
 'editorial_schema_version': 2,
 'events': [],
 'generation': 1,
 'production_id': '10000000-0000-0000-0000-000000000001',
 'production_revisions': [{'content_mode': 'hybrid',
                           'created_at': '2026-11-04T10:00:00Z',
                           'intended_use': 'test',
                           'narration_locale': 'uk',
                           'output_preset': '9:16',
                           'profile_ref': {'content_hash': 'fc621df51e0d7d16d8d0e938635fc0eb5bcf80d0d1b4f480711ee50651f7cc31',
                                           'id': '10000000-0000-0000-0000-000000000001',
                                           'kind': 'genre_profile',
                                           'revision': 1},
                           'ref': {'content_hash': 'd9b2e672f947befb306ac2fa2b535caa5581ca3753a7fcd0e8ba22957080da21',
                                   'id': '10000000-0000-0000-0000-000000000001',
                                   'kind': 'production',
                                   'revision': 1},
                           'script_locale': 'uk',
                           'subtitle_locale': 'uk',
                           'title': 'Тема',
                           'ui_locale': 'ru'}],
 'profiles': [{'allowed_modes': ['factual', 'hybrid'],
               'display_name_ru': 'Наука',
               'display_name_uk': 'Наука',
               'narrative_structure': ['Вопрос', 'Пояснення'],
               'profile_key': 'science',
               'ref': {'content_hash': 'fc621df51e0d7d16d8d0e938635fc0eb5bcf80d0d1b4f480711ee50651f7cc31',
                       'id': '10000000-0000-0000-0000-000000000001',
                       'kind': 'genre_profile',
                       'revision': 1},
               'review_policy_version': '1',
               'rubric': [{'description': 'Понятность',
                           'key': 'clarity',
                           'rating_max': 5,
                           'rating_min': 0,
                           'weight_percent': 100}],
               'version': '1.0'}],
 'rights_reviews': [{'allowed_actions': [],
                     'basis': 'Needs review',
                     'expires_at': None,
                     'intended_use': 'test',
                     'material_digest': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
                     'ref': {'content_hash': '6f046e4b9905fb312658955adc7217163b062120d778492521979400ee1ef393',
                             'id': '10000000-0000-0000-0000-000000000001',
                             'kind': 'rights_review',
                             'revision': 1},
                     'reviewed_at': '2026-11-04T10:00:00Z',
                     'reviewer': 'Owner',
                     'status': 'unknown',
                     'subject_id': '10000000-0000-0000-0000-000000000001',
                     'subject_kind': 'source',
                     'subject_revision': 1},
                    {'allowed_actions': [],
                     'basis': 'Needs review',
                     'expires_at': None,
                     'intended_use': 'test',
                     'material_digest': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
                     'ref': {'content_hash': '2e710af646a98b1ed7f922acb4c8df2740a76cd194fb480e6fe3a68b87c205cd',
                             'id': '20000000-0000-0000-0000-000000000002',
                             'kind': 'rights_review',
                             'revision': 2},
                     'reviewed_at': '2026-11-04T10:00:00Z',
                     'reviewer': 'Owner',
                     'status': 'unknown',
                     'subject_id': '10000000-0000-0000-0000-000000000001',
                     'subject_kind': 'asset',
                     'subject_revision': 1}],
 'scene_plans': [{'ref': {'content_hash': '33ddbf376b9ed36a939991a4ede72704260260fb714af8c7120bfb8b9a6a6579',
                          'id': '10000000-0000-0000-0000-000000000001',
                          'kind': 'scene_plan',
                          'revision': 1},
                  'scenes': [{'asset_ref': {'content_hash': 'a592fa1bb7657e34f4ecca1267f36a0f060a3ded5a52d186e733d6a514673f43',
                                            'id': '10000000-0000-0000-0000-000000000001',
                                            'kind': 'asset',
                                            'revision': 1},
                              'end': 15,
                              'estimate_ms': None,
                              'id': '10000000-0000-0000-0000-000000000001',
                              'narration_text': '  Україна е́ 😀 ',
                              'start': 0,
                              'visual_brief': 'Градиент',
                              'visual_kind': 'still'}],
                  'script_ref': {'content_hash': '57600db6c66b619a6a8b2e8e5b619f7ab549e6f3fcdbcefe12a5071480a9ab15',
                                 'id': '10000000-0000-0000-0000-000000000001',
                                 'kind': 'script',
                                 'revision': 1}}],
 'scripts': [{'brief': {'angle': 'Angle',
                        'audience': 'Аудитория',
                        'must_avoid': [],
                        'must_include_claim_refs': [{'content_hash': '972ee3870d01646bd5be7481f57d2e09b0ccaa3b2eadb1db97e6864fef9f4d73',
                                                     'id': '10000000-0000-0000-0000-000000000001',
                                                     'kind': 'claim',
                                                     'revision': 1}],
                        'profile_ref': {'content_hash': 'fc621df51e0d7d16d8d0e938635fc0eb5bcf80d0d1b4f480711ee50651f7cc31',
                                        'id': '10000000-0000-0000-0000-000000000001',
                                        'kind': 'genre_profile',
                                        'revision': 1},
                        'promise': 'Promise',
                        'revision': 1},
              'candidate_ref': {'content_hash': '4ffea2010baeb441582a86b21cfe0248766f78dcb5d8a4710ab8bd1563e82d83',
                                'id': '10000000-0000-0000-0000-000000000001',
                                'kind': 'candidate',
                                'revision': 1},
              'claim_refs': [{'content_hash': '972ee3870d01646bd5be7481f57d2e09b0ccaa3b2eadb1db97e6864fef9f4d73',
                              'id': '10000000-0000-0000-0000-000000000001',
                              'kind': 'claim',
                              'revision': 1}],
              'locale': 'uk',
              'production_ref': {'content_hash': 'd9b2e672f947befb306ac2fa2b535caa5581ca3753a7fcd0e8ba22957080da21',
                                 'id': '10000000-0000-0000-0000-000000000001',
                                 'kind': 'production',
                                 'revision': 1},
              'ref': {'content_hash': '57600db6c66b619a6a8b2e8e5b619f7ab549e6f3fcdbcefe12a5071480a9ab15',
                      'id': '10000000-0000-0000-0000-000000000001',
                      'kind': 'script',
                      'revision': 1},
              'segments': [{'claim_refs': [{'content_hash': '972ee3870d01646bd5be7481f57d2e09b0ccaa3b2eadb1db97e6864fef9f4d73',
                                            'id': '10000000-0000-0000-0000-000000000001',
                                            'kind': 'claim',
                                            'revision': 1}],
                            'disclosure_marker': 'Драматизация',
                            'id': '10000000-0000-0000-0000-000000000001',
                            'pronunciation_notes': None,
                            'role': 'body',
                            'text': '  Україна е́ 😀 ',
                            'visual_notes': None}]}],
 'snapshot_checksum': '5ef1b3079a0386f57e710575f19768dfe149c630e21b6c969917ea37bb956f95',
 'sources': [{'access_notes': None,
              'accessed_at': '2026-11-04T10:00:00Z',
              'author': None,
              'locator': 'https://example.invalid/source',
              'material_digest': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
              'published_at': None,
              'publisher': 'Publisher',
              'ref': {'content_hash': '39c36db97dccd5fb1aa64d27a50d9decfd017fc8151d9bd4b7619a2331d3f417',
                      'id': '10000000-0000-0000-0000-000000000001',
                      'kind': 'source',
                      'revision': 1},
              'reliability_notes': 'Needs review',
              'rights_ref': {'content_hash': '6f046e4b9905fb312658955adc7217163b062120d778492521979400ee1ef393',
                             'id': '10000000-0000-0000-0000-000000000001',
                             'kind': 'rights_review',
                             'revision': 1},
              'source_type': 'url',
              'title': 'Источник'}]}

def sealed(value):
    value = copy.deepcopy(value)
    value.pop('snapshot_checksum', None)
    value['snapshot_checksum'] = hashlib.sha256(c(value)).hexdigest()
    return value


def finish_plan(q, f, head, guard, blobs, *, kind, base, observed, seq, initialization_ref=None, bindings=None):
    core = {'receipt_core_version': 1, 'request_id': q['request_id'], 'request_sha256': f['request_sha256'],
            'storage_epoch_id': f['storage_epoch_id'], 'operation': q['operation'], 'tx_seq': seq,
            'status': {'GENESIS': 'INITIALIZED', 'PUBLISH': 'COMMITTED', 'REPAIR_EXACT': 'REPAIRED'}[kind],
            'result_content_head': head, 'approval_ids': [f['assigned_ids']['approval_id']] if f['assigned_ids']['approval_id'] else [],
            'event_ids': [f['assigned_ids']['event_id']] if f['assigned_ids']['event_id'] else [], 'abort_code': None}
    fm = w.frozen_command_mac(f, KEY)
    ledger = {'blob_version': 1, 'blob_type': 'LEDGER_DELTA', 'production_id': q['production_id'], 'storage_epoch_id': f['storage_epoch_id'],
              'previous_ref': guard['ledger_tip'], 'entries': [{'request_id': q['request_id'], 'review_session_id': q['review_session_id'],
              'request_sha256': f['request_sha256'], 'command_mac': fm, 'key_id': 'fixture-key', 'tx_seq': seq,
              'outcome': core['status'], 'receipt_core_sha256': ref(core)['sha256']}]}
    blobs[ref(ledger)['sha256']] = c(ledger)
    after_guard = {**copy.deepcopy(guard), 'ledger_tip': ref(ledger)}
    if bindings and bindings[0]['decision'] != 'approve':
        a = bindings[0]
        entry = {'decision_key': a['decision_key'], 'barrier_kind': a['decision'].upper(),
                 'source': {'source_kind': 'LOCAL_TX', 'storage_epoch_id': f['storage_epoch_id'], 'tx_seq': seq,
                            'approval_id': a['approval_id'], 'approval_record_sha256': a['approval_record_sha256']}}
        barrier = {'blob_version': 1, 'blob_type': 'BARRIER_DELTA', 'production_id': q['production_id'], 'storage_epoch_id': f['storage_epoch_id'],
                   'previous_ref': guard['barrier_tip'], 'entries': [entry]}
        blobs[ref(barrier)['sha256']] = c(barrier); after_guard['barrier_tip'] = ref(barrier)
    plan = {'plan_version': 1, 'kind': kind, 'request_id': q['request_id'], 'review_session_id': q['review_session_id'], 'tx_seq': seq,
            'key_id': 'fixture-key', 'command_ref': ref(f), 'command_mac': fm, 'base_head': base, 'observed_primary': observed,
            'new_content_head': head, 'image_ref': {'sha256': head['snapshot_file_sha256'], 'byte_length': head['snapshot_file_length']},
            'guard_before': guard, 'guard_commit': after_guard, 'expected_commit_receipt': core, 'new_approvals': bindings or [],
            'initialization_ref': initialization_ref, 'storage_profile_id': 'fixture-profile'}
    blobs[ref(f)['sha256']] = c(f); blobs[ref(plan)['sha256']] = c(plan)
    return plan


def relocate_image(image, production):
    from editorial.versioned_codec import decode_editorial_versioned
    from editorial.integrity import compute_revision_content_hash
    old = image['production_id']
    def replace(value, predicate, replacement):
        if type(value) is dict:
            if predicate(value): value.update(replacement)
            for child in value.values(): replace(child, predicate, replacement)
        elif type(value) is list:
            for child in value: replace(child, predicate, replacement)
    image['production_id'] = production
    replace(image, lambda v: v.get('kind') == 'production' and v.get('id') == old, {'id':production})
    # Resolve synthetic content hashes in a bounded fixed point over this finite DAG.
    for _ in range(32):
        snapshot = decode_editorial_versioned(c(image)).base_snapshot
        changes = []
        companions = snapshot.source_details + snapshot.claim_reviews + snapshot.rights_details
        for revision in snapshot.base.revisions:
            companion = next((x for x in companions if x.owner_ref == revision.ref), None)
            digest = compute_revision_content_hash(revision, companion)
            if digest != revision.ref.content_hash:
                changes.append((revision.ref, digest))
        if not changes: return sealed(image)
        for oldref, digest in changes:
            replace(image, lambda v: v.get('kind') == oldref.kind.value and v.get('id') == oldref.id and v.get('revision') == oldref.revision, {'content_hash':digest})
    raise ValueError('Synthetic DAG did not stabilize')


def seed_head(plan):
    """Derive the fresh seed's committed head using the S1 journal codec."""
    head = plan['new_content_head']
    context = {key: head[key] for key in ('production_id', 'machine_binding_id', 'storage_epoch_id')}
    plan_ref = ref(plan)

    def record_ref(index, kind, previous, payload):
        record = {'journal_record_version': 1, **context, 'record_index': index,
                  'previous_record_mac': previous, 'key_id': plan['key_id'],
                  'record_type': kind, 'payload': payload}
        return {'record_index': index, 'record_mac': w.journal_frame_mac(record, KEY)}

    prepare = record_ref(0, 'PREPARE', None, {'plan_ref': plan_ref})
    intent = record_ref(1, 'PUBLISH_INTENT', prepare['record_mac'],
                        {'plan_ref': plan_ref, 'prepare_ref': prepare})
    terminal = record_ref(2, 'GENESIS', intent['record_mac'],
                           {'plan_ref': plan_ref, 'prepare_ref': prepare, 'intent_ref': intent,
                            'receipt_core': plan['expected_commit_receipt']})
    return {'committed_head_version': 1, 'content_head': head, 'commit_ref': terminal}


class Builder:
    def __init__(self, factory, actor, probe, slot, *, policy=None):
        self.factory, self.actor, self.probe, self.slot = factory, actor, probe, slot
        self.principal = PRINCIPALS[actor]
        self.machine, self.epoch = self.ident('machine'), self.ident('epoch')
        if policy is None:
            policy = factory._case_policy(actor)
        self.policy_ref = {'policy_id':self.ident('policy'), 'policy_version':'lab-v1',
                           'policy_sha256':hashlib.sha256(c(policy)).hexdigest()}

    def ident(self, role):
        return self.factory.ident(self.actor, self.probe, self.slot, role)

    def image(self):
        return relocate_image(copy.deepcopy(SEED), self.ident('production'))

    def authorization(self, operation):
        grant = 'INITIALIZE' if operation in ('INITIALIZE_EMPTY','IMPORT_BASELINE','TRANSFER_BASELINE') else 'RECOVERY' if operation == 'RESTORE_EXACT_HEAD' else operation
        pair = None if operation != 'RECORD_DECISION' else dict(zip(('gate','decision'), self.probe.split('_')[1:]))
        if pair: pair['decision'] = pair['decision'].lower()
        return {'policy_ref':copy.deepcopy(self.policy_ref), 'principal_id':self.principal,
                'authenticated_connection_id':CONNECTION,
                'command_grants':['PROTECTED_SNAPSHOT_WRITE',grant], 'gate_decision_grant':pair}

    def genesis(self, *, image=None, epoch=None, request=None, operation='INITIALIZE_EMPTY', guard=None, extra=None, parents=None):
        M, PRINCIPAL, POLICY = self.machine, self.principal, self.policy_ref['policy_id']
        epoch = epoch or self.epoch
        request = request or self.ident('request')
        image = self.image() if image is None else image
        image_bytes = c(image)
        guard = copy.deepcopy(guard or {'guard_version': 1, 'continuity': 'CONTINUOUS' if operation == 'INITIALIZE_EMPTY' else 'BASELINE_UNVERIFIED',
                                       'baseline_ref': None, 'ledger_tip': None, 'barrier_tip': None, 'lineage_tip': None})
        blobs = dict(extra or {})
        def put(value):
            raw = c(value); r = ref(value); blobs[r['sha256']] = raw; return r
        image_ref = put(image)
        if operation != 'INITIALIZE_EMPTY':
            evidences = {e['approval_id']: e['attestation_digest'] for e in image.get('approval_authority_evidence', [])}
            inherited = [{'approval_id': a['id'], 'decision_key': {k: a[k] for k in ('gate', 'policy_version', 'object_ref', 'dependency_digest')},
                          'decision': a['decision'], 'approval_record_sha256': w.approval_wire_digest(a), 'evidence_attestation_digest': evidences.get(a['id'])} for a in image['approvals']]
            base = {'blob_version': 1, 'blob_type': 'BASELINE', 'production_id': image['production_id'], 'storage_epoch_id': epoch,
                    'source_schema_version': image['editorial_schema_version'], 'source_snapshot_ref': image_ref, 'inherited_approvals': inherited}
            guard['baseline_ref'] = put(base)
            if inherited:
                barriers = [{'decision_key': a['decision_key'], 'barrier_kind': 'UNVERIFIED_HISTORY',
                             'source': {'source_kind': 'BASELINE', 'baseline_ref': guard['baseline_ref'], 'approval_id': a['approval_id'], 'approval_record_sha256': a['approval_record_sha256']}} for a in inherited]
                guard['barrier_tip'] = put({'blob_version': 1, 'blob_type': 'BARRIER_DELTA', 'production_id': image['production_id'],
                                           'storage_epoch_id': epoch, 'previous_ref': None, 'entries': barriers})
        q = {'request_version': 1, 'request_id': request, 'production_id': image['production_id'], 'storage_epoch_id': None,
             'expected_head': None, 'review_session_id': None, 'operation': operation,
             'parameters': {'draft_ref' if operation == 'INITIALIZE_EMPTY' else 'source_ref': image_ref}}
        if operation == 'TRANSFER_BASELINE':
            manifest = {'transfer_manifest_version': 1, 'production_id': image['production_id'], 'source_ref': image_ref,
                        'source_machine_id': None, 'source_epoch_id': None, 'source_head': None, 'source_guard': None}
            q['parameters']['manifest_ref'] = put(manifest)
        auth = self.authorization('INITIALIZE_EMPTY')
        head = {'content_head_version': 1, 'production_id': image['production_id'], 'machine_binding_id': M, 'storage_epoch_id': epoch,
                'editorial_schema_version': image['editorial_schema_version'], 'generation': image['generation'],
                'snapshot_checksum': image['snapshot_checksum'], 'snapshot_file_sha256': image_ref['sha256'], 'snapshot_file_length': len(image_bytes), 'tx_seq': 0}
        f = {'command_version': 1, 'request': q, 'request_sha256': w.request_digest(q), 'key_id': 'fixture-key', 'principal_id': PRINCIPAL,
             'actor': ACTOR, 'at': AT, 'authorization': auth, 'assigned_ids': {'approval_id': None, 'event_id': None},
             'storage_epoch_id': epoch, 'expected_result': head, 'review_snapshot': None}
        init = {'initialization_version': 1, 'request_id': request, 'request_sha256': f['request_sha256'], 'production_id': image['production_id'],
                'machine_binding_id': M, 'storage_epoch_id': epoch, 'managed_root_token': ROOT, 'source_ref': image_ref, 'principal_id': PRINCIPAL,
                'actor': ACTOR, 'at': AT, 'policy_ref': auth['policy_ref'], 'authorization': auth, 'guard_before': guard, 'key_id': 'fixture-key'}
        iw = {'body': init, 'mac': w.initialization_mac(init, KEY)}
        regbody = {'registration_version': 1, 'storage_protocol_version': 1, 'production_id': image['production_id'], 'machine_binding_id': M,
                   'storage_epoch_id': epoch, 'managed_root_token': ROOT, 'initialization_ref': put(iw), 'storage_profile_id': 'fixture-profile', 'key_id': 'fixture-key'}
        reg = {'body': regbody, 'mac': w.registration_mac(regbody, KEY)}
        plan = finish_plan(q, f, head, guard, blobs, kind='GENESIS', base=None, observed={'state': 'MISSING'}, seq=0,
                           initialization_ref=regbody['initialization_ref'])
        return m.TransactionInput(plan, f, blobs, reg, parents or {})


    def publication(self, base, guard, high, primary, old_raw, *, number=1, operation='MIGRATE_SCHEMA', decision=None, reconsiders=None, key=None, assigned_number=None):
        PRINCIPAL, POLICY = self.principal, self.policy_ref['policy_id']
        uid = lambda n: self.ident('approval' if n >= 100 and n < 200 else 'event' if n >= 200 and n < 300 else 'session' if n >= 300 else 'request')
        from editorial.schema2_migration import migrate_schema1_to_schema2
        from editorial.versioned_codec import decode_editorial_versioned, encode_editorial_versioned
        old = json.loads(old_raw); new = copy.deepcopy(old)
        assigned_number = number if assigned_number is None else assigned_number
        seq = high + 1 if operation != 'RESTORE_EXACT_HEAD' else None
        ids = {'approval_id': uid(100 + assigned_number) if operation == 'RECORD_DECISION' else None,
               'event_id': uid(200 + assigned_number) if operation != 'RESTORE_EXACT_HEAD' else None}
        epoch = base['content_head']['storage_epoch_id']
        q = {'request_version': 1, 'request_id': uid(number), 'production_id': old['production_id'], 'storage_epoch_id': epoch,
             'expected_head': base, 'review_session_id': uid(300 + number) if operation == 'RECORD_DECISION' else None,
             'operation': operation, 'parameters': {}}
        auth = self.authorization(operation)
        auth['command_grants'] = ['PROTECTED_SNAPSHOT_WRITE', 'RECOVERY' if operation == 'RESTORE_EXACT_HEAD' else operation]
        review = None; bindings = []
        if operation == 'MIGRATE_SCHEMA':
            migrated = migrate_schema1_to_schema2(decode_editorial_versioned(primary), actor=ACTOR, at=AT, event_id=ids['event_id'])
            new = json.loads(encode_editorial_versioned(migrated.snapshot))
        elif operation == 'RECORD_DECISION':
            from editorial.schema2_model import ApprovalAuthorityEvidence, required_declaration_codes
            from editorial.approval_attestation import compute_attestation_digest
            from editorial import codec
            from editorial.current_package import compute_current_dependency_digest
            current_digest = compute_current_dependency_digest(decode_editorial_versioned(old_raw).base_snapshot, 'SCRIPT', 'fixture-review')
            key = key or {'gate': 'SCRIPT', 'policy_version': 'fixture-review', 'object_ref': old['scripts'][0]['ref'], 'dependency_digest': current_digest}
            q['parameters'] = {'decision_key': key, 'decision': decision, 'reason': 'Synthetic human decision', 'reconsiders_record_id': reconsiders}
            auth['gate_decision_grant'] = {'gate': key['gate'], 'decision': decision}
            codes = list(required_declaration_codes(key['gate'], decision))
            review = {'session_id': q['review_session_id'], 'principal_id': PRINCIPAL, 'policy_ref': auth['policy_ref'], 'decision_key': key,
                      'confirmed_codes': codes, 'review_declarations': ['Synthetic reviewed declaration'], 'reconsiders_record_id': reconsiders,
                      'server_incarnation_id': CONNECTION, 'state': 'READY'}
            a = {'id': ids['approval_id'], **key, 'decision': decision, 'actor': ACTOR, 'timestamp': AT,
                 'reason': q['parameters']['reason'], 'review_declarations': review['review_declarations']}
            e = {'approval_id': a['id'], 'principal_id': PRINCIPAL, 'principal_display_name': ACTOR, 'authority_policy_id': POLICY,
                 'authority_policy_version': 'lab-v1', 'review_session_id': q['review_session_id'], 'request_id': q['request_id'],
                 'declaration_codes': codes, 'attested_at': AT, 'reconsiders_record_id': reconsiders, 'attestation_digest': '0' * 64,
                 'signing_key_id': None, 'signature_algorithm': None, 'signature': None}
            ev = ApprovalAuthorityEvidence(**{**e, 'declaration_codes': tuple(codes)})
            e['attestation_digest'] = compute_attestation_digest(codec._APPROVAL(a, '$'), ev)
            new['approvals'].append(a); new['approval_authority_evidence'].append(e)
            new['events'].append({'id': ids['event_id'], 'actor': ACTOR, 'at': AT, 'action': 'approval_recorded',
                                  'refs': [key['object_ref']], 'reason': q['parameters']['reason'], 'error_code': None})
            new['generation'] += 1; new = sealed(new)
            bindings = [{'approval_id': a['id'], 'decision_key': key, 'decision': decision,
                         'approval_record_sha256': w.approval_wire_digest(a), 'evidence_attestation_digest': e['attestation_digest']}]
        elif operation == 'RESTORE_EXACT_HEAD':
            q['parameters'] = {'image_ref': {'sha256': base['content_head']['snapshot_file_sha256'], 'byte_length': base['content_head']['snapshot_file_length']},
                               'expected_observation': m.observation(primary)}
        raw = c(new); image_ref = ref(new)
        head = {**base['content_head'], 'editorial_schema_version': new['editorial_schema_version'], 'generation': new['generation'],
                'snapshot_checksum': new['snapshot_checksum'], 'snapshot_file_sha256': image_ref['sha256'], 'snapshot_file_length': len(raw),
                'tx_seq': seq if seq is not None else base['content_head']['tx_seq']}
        f = {'command_version': 1, 'request': q, 'request_sha256': w.request_digest(q), 'key_id': 'fixture-key', 'principal_id': PRINCIPAL,
             'actor': ACTOR, 'at': AT, 'authorization': auth, 'assigned_ids': ids, 'storage_epoch_id': epoch, 'expected_result': head, 'review_snapshot': review}
        blobs = {image_ref['sha256']: raw}
        plan = finish_plan(q, f, head, guard, blobs, kind='REPAIR_EXACT' if operation == 'RESTORE_EXACT_HEAD' else 'PUBLISH',
                           base=base, observed=m.observation(primary), seq=seq, bindings=bindings)
        return m.TransactionInput(plan, f, blobs)


class Factory:
    """A fixed policy/fault case, finite whitelist, bounded on-demand RAM seeds."""
    def __init__(self, incarnation, policy_case='CG_NONE', fault_case='NONE'):
        from .protocol import uuid
        uuid(incarnation)
        require(policy_case in POLICIES and fault_case in FAULTS)
        self.incarnation, self.policy_case, self.fault_case = incarnation, policy_case, fault_case
        self._stores = {}

    def ident(self, actor, probe, slot, role):
        require(actor in PRINCIPALS and probe in PROBES and role in ROLES)
        require(type(slot) is int and 0 <= slot <= 63 and (probe.startswith('GD_') or slot == 0))
        part = 'seed' if role in ('production','machine','epoch','policy') else str(slot)
        return str(uuid5(UUID(self.incarnation), f'S32_FIXTURES_1/{self.policy_case}/{actor}/{probe}/{part}/{role}'))

    def policy(self, actor):
        """Return the live policy used for admission and authority."""
        return self._case_policy(actor)

    def _case_policy(self, actor):
        require(actor in PRINCIPALS)
        grants, pair = [], None
        if self.policy_case != 'CG_NONE':
            grants = ['PROTECTED_SNAPSHOT_WRITE']
        if self.policy_case in ('CG_INIT','CG_MIGRATE','CG_RECOVERY'):
            grants.append({'CG_INIT':'INITIALIZE','CG_MIGRATE':'MIGRATE_SCHEMA','CG_RECOVERY':'RECOVERY'}[self.policy_case])
        if self.policy_case.startswith('GD_'):
            grants.append('RECORD_DECISION')
            _, gate, decision = self.policy_case.split('_')
            pair = {'gate':gate,'decision':decision.lower()}
        return {'mock_policy_version':1,'policy_case':self.policy_case,
                'actor_a_command_grants':grants,
                'actor_a_gate_grant':pair, 'actor_b_command_grants':[], 'actor_b_gate_grant':None}

    def allowed(self, actor, probe, *, grants=None):
        require(actor in PRINCIPALS and probe in PROBES)
        policy = self.policy(actor)
        actual = policy['actor_a_command_grants'] if grants is None else grants
        operation = OPS.get(probe, 'RECORD_DECISION')
        grant = 'INITIALIZE' if probe in PROBES[:3] else 'RECOVERY' if probe == 'RECOVERY' else operation
        pair = None if not probe.startswith('GD_') else dict(zip(('gate','decision'), (probe.split('_')[1],probe.split('_')[2].lower())))
        return actor == 'A' and 'PROTECTED_SNAPSHOT_WRITE' in actual and grant in actual and (pair is None or pair == policy['actor_a_gate_grant'])

    def locate(self, actor, request_id):
        require(actor in PRINCIPALS)
        for probe in PROBES:
            for slot in range(64 if probe.startswith('GD_') else 1):
                if self.ident(actor, probe, slot, 'request') == request_id:
                    return probe, slot
        return None

    def candidate(self, actor, probe, slot=0):
        """Build exact fixture inputs without allocating or mutating a store."""
        self.ident(actor, probe, slot, 'request')
        builder = Builder(self, actor, probe, slot)
        seed = None
        if probe in PROBES[:3]:
            transaction = builder.genesis(operation=OPS[probe])
        else:
            store = self._stores.get((actor, probe))
            if store is None:
                image = builder.image()
                if probe == 'MIGRATE':
                    image.pop('approval_authority_evidence')
                    image['editorial_schema_version'] = 1
                    image = sealed(image)
                seed = builder.genesis(image=image, request='44444444-4444-4444-8444-444444444444',
                                       operation='IMPORT_BASELINE' if probe == 'MIGRATE' else 'INITIALIZE_EMPTY')
                base, guard, high = seed_head(seed.plan), seed.plan['guard_commit'], 0
                source = seed.blobs[seed.plan['image_ref']['sha256']]
                primary = b'corrupt synthetic image' if probe == 'RECOVERY' else source
            else:
                anchor = json.loads(store.visible.anchor)['body']
                base, guard, high = anchor['stable_head'], anchor['history_guard'], anchor['reserved_tx_high_watermark']
                primary = store.visible.primary
                source = store.visible.blobs[base['content_head']['snapshot_file_sha256']] if probe == 'RECOVERY' else primary
            if probe in ('MIGRATE', 'RECOVERY'):
                transaction = builder.publication(base, guard, high, primary, source, operation=OPS[probe])
            else:
                from editorial.current_package import compute_current_dependency_digest
                from editorial.versioned_codec import decode_editorial_versioned
                _, gate, decision = probe.split('_')
                image = json.loads(source)
                target = image['active_refs'][{'SCRIPT':'script','SCENES':'scene_plan','HANDOFF':'production'}[gate]]
                digest = compute_current_dependency_digest(decode_editorial_versioned(source).base_snapshot, gate, 'fixture-review')
                dk = {'gate':gate,'policy_version':'fixture-review','object_ref':target,'dependency_digest':digest}
                transaction = builder.publication(base, guard, high, primary, source,
                                                  operation='RECORD_DECISION', decision=decision.lower(), key=dk)
        require(transaction.plan['image_ref']['byte_length'] <= 128 * 1024)
        require(sum(map(len, transaction.blobs.values())) <= 256 * 1024)
        return seed, transaction

    def materialize(self, actor, probe, seed, transaction):
        """Run synthetic startup only for a candidate past pre-admission checks."""
        key = actor, probe
        store = self._stores.get(key)
        retained_bytes = sum(len(raw) for s in self._stores.values() for raw in s.visible.blobs.values())
        seed_bytes = sum(map(len, seed.blobs.values())) if seed is not None else 0
        require(retained_bytes + seed_bytes <= 16 * 1024 * 1024)
        if store is None:
            store = m.VirtualStore()
            if seed is not None:
                engine = m.TransactionModel(store, keys={'fixture-key': KEY}, authority=self.seed_authority(seed))
                result = engine.execute(seed)
                require(result.state == 'FINALIZED')
                actual_head = json.loads(store.visible.anchor)['body']['stable_head']
                require(actual_head == transaction.command['request']['expected_head'])
                if probe == 'RECOVERY':
                    store.visible.primary = b'corrupt synthetic image'
                    store.durable.primary = store.visible.primary
        return store

    def retain(self, actor, probe, store):
        self._stores[(actor, probe)] = store

    @staticmethod
    def seed_authority(transaction):
        command = transaction.command
        request = command['request']
        return m.FixtureAuthority(command['principal_id'], frozenset([command['principal_id']]),
            frozenset([c(command['authorization'])]), CONNECTION,
            frozenset([request['review_session_id']]) if request['review_session_id'] else frozenset(),
            frozenset([(command['request_sha256'],command['expected_result']['snapshot_file_sha256'])]),
            True, production_id=request['production_id'])

    def authority(self, transaction, actor):
        """Current provider lookup, independent of the proposed frozen grant bytes."""
        require(actor in PRINCIPALS)
        command, request = transaction.command, transaction.command['request']
        location = self.locate(actor, request['request_id'])
        require(location is not None and self.allowed(actor, location[0]))
        probe, slot = location
        live_policy = self.policy(actor)
        expected = Builder(self, actor, probe, slot, policy=live_policy).authorization(request['operation'])
        require(command['principal_id'] == PRINCIPALS[actor] and c(command['authorization']) == c(expected))
        # Only the independently selected current policy can issue this live assertion.
        return m.FixtureAuthority(PRINCIPALS[actor], frozenset([PRINCIPALS[actor]]),
            frozenset([c(expected)]), CONNECTION,
            frozenset([request['review_session_id']]) if request['review_session_id'] else frozenset(),
            frozenset([(command['request_sha256'],command['expected_result']['snapshot_file_sha256'])]),
            'INITIALIZE' in live_policy['actor_a_command_grants'],
            production_id=self.ident(actor, probe, slot, 'production'))
