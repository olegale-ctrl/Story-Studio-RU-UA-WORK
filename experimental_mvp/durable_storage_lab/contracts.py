"""Pure DQ.LAB v2 documentary validation; never native evidence authority.

Schemas and semantics follow contract 4a6780bf519e03ddafa5ae9d7ed0f4309bff7c89.
Valid bytes and documentary premises MUST NOT authorize native outcomes.
No filesystem, clock, process, SQLite or provider access occurs here.
"""

from dataclasses import dataclass
import hashlib
import json
import re


VERSION = 2
SCOPE = "DQ_PROCESS_KILL_LAB_ONLY"
MAX_INTEGER = (1 << 63) - 1
MAX_RECORD_BYTES = 4 * 1024 * 1024
MAX_GRAPH_NODES = 8192
MAX_GRAPH_DEPTH = 2048
KINDS = frozenset("DQ.LAB." + name for name in (
    "QualificationProfile", "RootAnchor", "DataObject", "AdmissionKey",
    "WriteSet", "MutationIntent", "ProjectionRoot", "CommitMarker",
    "ControlRoot", "SnapshotEvidence", "OperationTicket", "PrepareEvidence",
    "CommitProof", "AbsenceProof", "HoldEvidence", "RecoveryEvidence", "ProofAck",
))
_DIGEST = re.compile(r"[0-9a-f]{64}\Z")


class WireError(ValueError):
    """Invalid or resource-bounded wire input, without raw input in diagnostics."""


def _check_tree(value):
    # Explicit traversal bounds apply before json.dumps. Only exact JSON types
    # are accepted; custom mappings, integer subclasses and cyclic containers
    # cannot invoke user callbacks or masquerade as canonical data.
    stack = [(value, 0, False)]
    active = set()
    visited = 0
    while stack:
        item, depth, leaving = stack.pop()
        if leaving:
            active.remove(id(item))
            continue
        visited += 1
        if visited > 100000 or depth > 64:
            raise WireError("JSON resource limit.")
        typ = type(item)
        if item is None or typ is bool:
            continue
        if typ is int:
            if not 0 <= item <= MAX_INTEGER:
                raise WireError("Integer outside domain.")
        elif typ is str:
            if any(0xD800 <= ord(c) <= 0xDFFF for c in item):
                raise WireError("Non-scalar Unicode.")
        elif typ in (list, dict):
            if id(item) in active:
                raise WireError("Cyclic JSON input.")
            active.add(id(item))
            stack.append((item, depth, True))
            if typ is dict:
                for key in item:
                    if type(key) is not str or not key.isascii():
                        raise WireError("Keys must be ASCII strings.")
                children = item.values()
            else:
                children = item
            for child in children:
                stack.append((child, depth + 1, False))
        else:
            raise WireError("Unsupported JSON value.")


def canonical_bytes(value):
    """Encode C(value), with no normalization, BOM or trailing newline.

    The local codec envelope bounds JSON nesting to 64 and tree visits to
    100000. These are implementation guards, not evidence schema revisions;
    graph depth has a separate bound and never uses JSON recursion.
    """
    _check_tree(value)
    data = json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(", ", ": "), allow_nan=False).encode("utf-8")
    if len(data) > MAX_RECORD_BYTES:
        raise WireError("Record byte limit.")
    return data


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise WireError("Duplicate JSON key.")
        result[key] = value
    return result


def _invalid_number(_):
    raise WireError("Unsupported JSON number.")


def decode_canonical(data):
    """Require exact canonical UTF-8 bytes, rather than normalizing input."""
    if type(data) is not bytes or len(data) > MAX_RECORD_BYTES:
        raise WireError("Invalid wire bytes.")
    try:
        value = json.loads(data.decode("utf-8", errors="strict"),
                           object_pairs_hook=_pairs, parse_float=_invalid_number,
                           parse_constant=_invalid_number)
        if canonical_bytes(value) != data:
            raise WireError("Noncanonical wire bytes.")
        return value
    except (UnicodeError, RecursionError, json.JSONDecodeError) as exc:
        raise WireError("Invalid JSON encoding.") from exc


def validate_ref(ref):
    """Validate the closed four-field native ref, never a PURE or raw digest."""
    if type(ref) is not dict or set(ref) != {"kind", "version", "scope", "digest"}:
        raise WireError("Invalid reference shape.")
    if (type(ref["kind"]) is not str or ref["kind"] not in KINDS
            or type(ref["version"]) is not int or ref["version"] != VERSION
            or ref["scope"] != SCOPE or type(ref["scope"]) is not str
            or type(ref["digest"]) is not str
            or not _DIGEST.fullmatch(ref["digest"])):
        raise WireError("Invalid reference identity.")


def typed_ref(data):
    """Hash a canonical header-bearing record, WITHOUT validating its schema."""
    record = decode_canonical(data)
    if type(record) is not dict:
        raise WireError("Record must be an object.")
    ref = {"kind": record.get("kind"), "version": record.get("version"),
           "scope": record.get("scope"), "digest": hashlib.sha256(data).hexdigest()}
    validate_ref(ref)
    return ref


def _edges(value):
    stack = [value]
    while stack:
        node = stack.pop()
        if type(node) is list:
            stack.extend(node)
        elif type(node) is dict:
            if "digest" in node:
                validate_ref(node)
                yield node
            else:
                stack.extend(node.values())


def _payload_edges(record):
    if record["kind"] != "DQ.LAB.DataObject":
        return []
    value = record.get("payload_hex")
    if (type(value) is not str or len(value) > 2 * 1024 * 1024
            or not value or len(value) % 2 or re.fullmatch(r"[0-9a-f]+", value) is None):
        raise WireError("Invalid payload bytes.")
    raw = bytes.fromhex(value)
    if (type(record.get("byte_length")) is not int
            or record["byte_length"] != len(raw)
            or record.get("raw_sha256") != hashlib.sha256(raw).hexdigest()):
        raise WireError("Invalid payload hash or length.")
    return list(_edges(decode_canonical(raw)))


@dataclass(frozen=True)
class ByteClosure:
    """Non-authoritative byte-graph statistics; never a native proof."""

    nodes: int
    depth: int


def verify_byte_closure(root_ref, resolve):
    """Verify full typed hash closure iteratively, including payload edges.

    resolve(ref) is a caller-supplied pure lookup returning immutable bytes.
    This validates byte identity and acyclicity only. Schema, binding, roles,
    indices, outcomes and live custody require separate validation.
    """
    validate_ref(root_ref)
    states = {}
    heights = {}
    adjacency = {}
    stack = [(root_ref, False)]
    while stack:
        ref, leaving = stack.pop()
        validate_ref(ref)
        key = (ref["kind"], ref["digest"])
        if leaving:
            heights[key] = 1 + max((heights[(r["kind"], r["digest"])]
                                    for r in adjacency[key]), default=0)
            if heights[key] > MAX_GRAPH_DEPTH:
                raise WireError("Graph depth limit.")
            states[key] = 2
            continue
        if states.get(key) == 1:
            raise WireError("Cyclic reference graph.")
        if states.get(key) == 2:
            continue
        if len(states) >= MAX_GRAPH_NODES:
            raise WireError("Graph node limit.")
        try:
            raw = resolve(dict(ref))
        except (KeyError, LookupError) as exc:
            raise WireError("Unresolved reference.") from exc
        if typed_ref(raw) != ref:
            raise WireError("Reference byte identity mismatch.")
        record = decode_canonical(raw)
        children = list(_edges(record)) + _payload_edges(record)
        adjacency[key] = children
        states[key] = 1
        stack.append((ref, True))
        stack.extend((r, False) for r in reversed(children))
    return ByteClosure(len(states), heights[(root_ref["kind"], root_ref["digest"])])


def _require(condition, message="Document invariant failed."):
    if not condition:
        raise WireError(message)


def _fields(**fields):
    return fields


def _enum(*values):
    return ("enum", values)


def _ref(name):
    return ("ref", "DQ.LAB." + name)


def _nullable(spec):
    return ("nullable", spec)


def _array(spec, low, high, key):
    return ("array", spec, low, high, key)


def _literal(value):
    return ("literal", value)


U, POS, TEXT, UUID, DIGEST, BOOL = "U", "Pos", "Text", "UUID", "Digest", "Bool"
_UUID = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\Z")
STATE = _enum("DRAFT", "LAB_CHECKPOINT", "CANCELLED", "FAILED")
TERMINAL = _enum("CANCELLED", "FAILED")
PHASE = _enum("P", "A", "R")
ROLE = _enum("REQUEST", "MANIFEST", "JOB", "EVENT", "RECEIPT", "ACTIVE_SLOT",
             "OUTBOX", "READ_RESERVATION", "TERMINAL_PROOF")
HOLD_REASON = _enum("COMMIT_ACK_LOST", "PREPARE_UNRESOLVED", "ACK_UNRESOLVED",
                    "STORE_UNAVAILABLE", "STORE_CORRUPT", "STORE_MISSING",
                    "IDENTITY_MISMATCH", "PROFILE_MISMATCH", "STALE_COPY",
                    "CUSTODY_LOST", "PROOF_INCOMPLETE")
DATA, ANCHOR, INTENT = _ref("DataObject"), _ref("RootAnchor"), _ref("MutationIntent")
MARKER, ACK = _nullable(_ref("CommitMarker")), _nullable(_ref("ProofAck"))
NDATA = _nullable(DATA)
IDENTITY = _fields(provider=_enum("POSIX_DEVICE_INODE", "WINDOWS_HANDLE_FILE_ID"),
                   volume_id=TEXT, file_id=TEXT)
CONFIG_VALUES = dict(driver="PYTHON_STDLIB_SQLITE3", wrapper_control="EXPLICIT_SQL_LEGACY",
    transaction_mode="IMMEDIATE", journal_mode="DELETE", synchronous="FULL",
    foreign_keys=True, busy_timeout_ms=250, connect_timeout_ms=250, automatic_retries=0,
    page_size=4096, max_page_count=8192, journal_size_limit_bytes=1048576,
    locking_mode="NORMAL", read_uncommitted=False, trusted_schema=False,
    check_same_thread=True, extension_loading=False, attach_allowed=False,
    temp_store="MEMORY", mmap_size_bytes=0, cache_pages=512, auto_vacuum="NONE", user_version=1)
CONFIG = {k: _literal(v) for k, v in CONFIG_VALUES.items()}
CHECKS = {k: _literal(v) for k, v in dict(sqlite_integrity="ok", foreign_key_errors=0,
    canonical_closure_valid=True, projection_indices_valid=True, marker_chain_valid=True,
    profile_readback_matches=True, complete_snapshot=True).items()}
CUSTODY = _fields(coordinator_run_id=UUID, root_identity=IDENTITY, database_identity=IDENTITY,
    expected_store_epoch=_literal(1), minimum_acknowledged_sequence=U,
    minimum_acknowledged_marker_ref=MARKER, exclusive_controlled_root=_literal(True),
    no_restore_or_replacement_observed=_literal(True))
JOB_INDEX = _fields(job_id=UUID, job_ref=DATA)
ADMISSION_INDEX = _fields(key_ref=_ref("AdmissionKey"), job_id=UUID, receipt_ref=DATA)
SLOT_INDEX = _fields(project_id=UUID, purpose_id=UUID, slot_ref=DATA)
MEMBER_LINK = _fields(mutation_id=UUID, member_ref=DATA)
STAGED_LINK = _fields(mutation_id=UUID, object_ref=DATA)
REGISTRY = _fields(mutation_ref=INTENT,
    phase=_enum("PREPARED", "APPLIED", "RESOLVED_COMMITTED", "RESOLVED_NOT_COMMITTED"),
    marker_ref=MARKER, latest_ack_ref=ACK)


def _ref_key(r):
    return (r["kind"], r["digest"])


SCHEMAS = {
    "QualificationProfile": _fields(profile_id=UUID, python_version=TEXT, python_build=TEXT,
        sqlite_version=TEXT, sqlite_source_id=TEXT,
        compile_options=_array(TEXT, 0, 256, lambda x: x),
        platform=_enum("LINUX_LOCAL", "WINDOWS_NTFS"), os_build=TEXT, filesystem=TEXT,
        configuration=CONFIG, fault_envelope=_literal("WRITER_KILL_COORDINATOR_SURVIVES"),
        schema_version=_literal(1)),
    "RootAnchor": _fields(run_id=UUID, store_id=UUID, namespace_id=UUID,
        store_epoch=_literal(1), schema_version=_literal(1),
        profile_ref=_ref("QualificationProfile"), root_identity=IDENTITY, database_identity=IDENTITY),
    "DataObject": _fields(binding_ref=ANCHOR, object_id=UUID, role=ROLE,
        owner_job_id=_nullable(UUID), payload_hex="Hex", byte_length=POS, raw_sha256=DIGEST),
    "AdmissionKey": _fields(binding_ref=ANCHOR, project_id=UUID, purpose_id=UUID,
        request_ref=DATA, batch_id=UUID, batch_revision=POS, manifest_ref=DATA),
    "WriteSet": _fields(binding_ref=ANCHOR, mutation_id=UUID, job_id=UUID,
        key_ref=_ref("AdmissionKey"), expected_revision=U, resulting_revision=POS, target_state=STATE,
        members=_array(DATA, 1, 16, _ref_key), job_ref=DATA, event_ref=DATA, receipt_ref=NDATA,
        slot_ref=DATA, slot_action=_enum("ACQUIRE", "RETAIN", "RELEASE"), outbox_ref=NDATA,
        read_reservation_ref=NDATA, terminal_proof_ref=NDATA),
    "MutationIntent": _fields(binding_ref=ANCHOR, mutation_id=UUID,
        mutation_kind=_enum("ADMIT", "ADVANCE_MODEL", "ENQUEUE_MODEL", "RESERVE_READ_MODEL", "TERMINAL_MODEL"),
        job_id=UUID, expected_head_ref=MARKER, write_set_ref=_ref("WriteSet")),
    "ProjectionRoot": _fields(binding_ref=ANCHOR, application_sequence=U,
        committed_objects=_array(DATA, 0, 4096, _ref_key),
        jobs=_array(JOB_INDEX, 0, 16, lambda x: x["job_id"]),
        admissions=_array(ADMISSION_INDEX, 0, 16, lambda x: x["key_ref"]["digest"]),
        active_slots=_array(SLOT_INDEX, 0, 16, lambda x: (x["project_id"], x["purpose_id"])),
        events=_array(DATA, 0, 128, _ref_key), outbox=_array(DATA, 0, 32, _ref_key),
        read_reservations=_array(DATA, 0, 128, _ref_key),
        member_links=_array(MEMBER_LINK, 0, 4096, lambda x: (x["mutation_id"], x["member_ref"]["digest"]))),
    "CommitMarker": _fields(binding_ref=ANCHOR, mutation_ref=INTENT, write_set_ref=_ref("WriteSet"),
        application_sequence=POS, previous_marker_ref=MARKER, resulting_root_ref=_ref("ProjectionRoot")),
    "ControlRoot": _fields(binding_ref=ANCHOR, control_generation=U, pending_mutation_id=_nullable(UUID),
        registry=_array(REGISTRY, 0, 128, lambda x: x["mutation_ref"]["digest"]),
        staged_links=_array(STAGED_LINK, 0, 4096, lambda x: (x["mutation_id"], x["object_ref"]["digest"])),
        proof_acks=_array(_ref("ProofAck"), 0, 128, _ref_key)),
    "SnapshotEvidence": _fields(binding_ref=ANCHOR, snapshot_id=UUID, observed_head_ref=MARKER,
        projection_root_ref=_ref("ProjectionRoot"), control_root_ref=_ref("ControlRoot"),
        control_generation=U, custody=CUSTODY, integrity_checks=CHECKS),
    "OperationTicket": _fields(binding_ref=ANCHOR, ticket_id=UUID, coordinator_run_id=UUID,
        mutation_ref=INTENT, phase=PHASE, expected_application_head_ref=MARKER,
        expected_control_generation=U, expected_ack_ref=ACK),
    "PrepareEvidence": _fields(binding_ref=ANCHOR, mutation_ref=INTENT, write_set_ref=_ref("WriteSet"),
        snapshot_ref=_ref("SnapshotEvidence"), staged_member_refs=_array(DATA, 1, 16, _ref_key),
        pending_mutation_id=UUID, prepared_control_generation=POS),
    "CommitProof": _fields(binding_ref=ANCHOR, mutation_ref=INTENT, marker_ref=_ref("CommitMarker"),
        write_set_ref=_ref("WriteSet"), snapshot_ref=_ref("SnapshotEvidence")),
    "AbsenceProof": _fields(binding_ref=ANCHOR, mutation_ref=INTENT, write_set_ref=_ref("WriteSet"),
        snapshot_ref=_ref("SnapshotEvidence"), marker_present=_literal(False),
        any_apply_member_present=_literal(False), any_apply_projection_change_present=_literal(False),
        intent_source=_enum("REGISTERED_DB", "COORDINATOR_TICKET"), registry_present=BOOL,
        ticket_sha256=DIGEST, expected_previous_head_ref=MARKER),
    "HoldEvidence": _fields(binding_ref=ANCHOR, mutation_id=UUID, intent_ref=_nullable(INTENT),
        phase=PHASE, reason=HOLD_REASON, last_qualified_head_ref=MARKER,
        observed_snapshot_ref=_nullable(_ref("SnapshotEvidence")), outcome=_literal("UNKNOWN")),
    "RecoveryEvidence": _fields(binding_ref=ANCHOR, mutation_id=UUID, ticket_sha256=DIGEST,
        prior_hold_ref=_ref("HoldEvidence"), resolution=_enum("COMMITTED", "NOT_COMMITTED", "UNKNOWN"),
        commit_proof_ref=_nullable(_ref("CommitProof")), absence_proof_ref=_nullable(_ref("AbsenceProof")),
        remaining_hold_ref=_nullable(_ref("HoldEvidence"))),
    "ProofAck": _fields(binding_ref=ANCHOR, mutation_ref=INTENT, outcome=_enum("COMMITTED", "NOT_COMMITTED"),
        commit_proof_ref=_nullable(_ref("CommitProof")), absence_proof_ref=_nullable(_ref("AbsenceProof")),
        observed_application_head_ref=MARKER, control_generation=POS),
}
PAYLOADS = {
    "REQUEST": _fields(request_id=UUID, project_id=UUID, purpose_id=UUID, synthetic_input_sha256=DIGEST),
    "MANIFEST": _fields(batch_id=UUID, batch_revision=POS, synthetic_label=TEXT),
    "JOB": _fields(job_id=UUID, request_ref=DATA, state=STATE, revision=POS, cancel_requested=BOOL),
    "EVENT": _fields(event_id=UUID, mutation_id=UUID, job_id=UUID, revision_from=U,
        revision_to=POS, state_from=_nullable(STATE), state_to=STATE),
    "RECEIPT": _fields(receipt_id=UUID, mutation_id=UUID, job_id=UUID, key_ref=_ref("AdmissionKey"),
        request_ref=DATA, accepted_revision=_literal(1)),
    "ACTIVE_SLOT": _fields(store_id=UUID, namespace_id=UUID, project_id=UUID, purpose_id=UUID,
        job_id=UUID, status=_enum("HELD", "RELEASED"), occupied_since_revision=POS,
        released_at_revision=_nullable(POS)),
    "OUTBOX": _fields(outbox_id=UUID, job_id=UUID, effect_token=UUID, request_ref=DATA,
        payload_sha256=DIGEST, dispatch_allowed=_literal(False)),
    "READ_RESERVATION": _fields(reservation_id=UUID, job_id=UUID, checkpoint_id=UUID,
        read_kind=_enum("MODEL_LOOKUP", "MODEL_POLL"), base_cursor=U, call_index=_enum(1, 2, 3)),
    "TERMINAL_PROOF": _fields(proof_id=UUID, job_id=UUID, terminal_state=TERMINAL,
        reason=_literal("NO_EXECUTOR_IN_LAB"), executor_effect=_literal("NONE"),
        evidence_source=_literal("STORAGE_ONLY_POLICY")),
}


def _shape(value, spec):
    if type(spec) is dict:
        _require(type(value) is dict and set(value) == set(spec), "Closed fields mismatch.")
        for key, child in spec.items():
            _shape(value[key], child)
    elif type(spec) is tuple:
        tag = spec[0]
        if tag == "literal":
            _require(type(value) is type(spec[1]) and value == spec[1], "Literal mismatch.")
        elif tag == "enum":
            _require(any(type(value) is type(x) and value == x for x in spec[1]), "Enum mismatch.")
        elif tag == "nullable":
            if value is not None:
                _shape(value, spec[1])
        elif tag == "ref":
            validate_ref(value)
            _require(value["kind"] == spec[1], "Reference kind mismatch.")
        elif tag == "array":
            _require(type(value) is list and spec[2] <= len(value) <= spec[3], "Array bounds.")
            for item in value:
                _shape(item, spec[1])
            keys = [spec[4](x) for x in value]
            _require(keys == sorted(keys) and len(set(keys)) == len(keys), "Unsorted or duplicate set.")
    elif spec in (U, POS):
        _require(type(value) is int and (1 if spec == POS else 0) <= value <= MAX_INTEGER, "Integer bounds.")
    elif spec == BOOL:
        _require(type(value) is bool, "Boolean required.")
    elif spec == TEXT:
        _require(type(value) is str and 1 <= len(value) <= 100000, "Text bounds.")
    elif spec == UUID:
        _require(type(value) is str and _UUID.fullmatch(value) is not None, "Invalid UUID.")
    elif spec == DIGEST:
        _require(type(value) is str and _DIGEST.fullmatch(value) is not None, "Invalid digest.")
    elif spec == "Hex":
        _require(type(value) is str and 0 < len(value) <= 2 * 1024 * 1024 and len(value) % 2 == 0
                 and re.fullmatch(r"[0-9a-f]+", value) is not None, "Invalid payload hex.")
    else:
        raise WireError("Unknown schema descriptor.")


def validate_schema(record):
    """Closed structural validation, not proof qualification or permissions."""
    canonical_bytes(record)
    _require(type(record) is dict, "Record object required.")
    name = record.get("kind", "")
    _require(type(name) is str and name in KINDS, "Unknown record kind.")
    fields = dict(SCHEMAS[name.removeprefix("DQ.LAB.")], kind=_literal(name),
                  version=_literal(VERSION), scope=_literal(SCOPE))
    _shape(record, fields)
    if name == "DQ.LAB.QualificationProfile":
        _require(all(x.isascii() for x in record["compile_options"]), "Non-ASCII compile option.")
    if name == "DQ.LAB.DataObject":
        _payload_edges(record)
        p = decode_canonical(bytes.fromhex(record["payload_hex"]))
        _shape(p, PAYLOADS[record["role"]])
        _require(record["owner_job_id"] == (None if record["role"] in ("REQUEST", "MANIFEST") else p["job_id"]),
                 "Payload ownership mismatch.")


class DocumentGraph:
    """Case-local, immutable-byte graph. Never a native evidence issuer.

    Only explicit root refs and typed edges are resolved. In particular a raw
    ticket_sha256 cannot fetch a missing ticket from the catalogue (C-A01).
    Documentary custody/check fields remain assertions, never measurements.
    """

    def __init__(self, root_refs, resolve):
        self._records = {}
        self._edges = {}
        self._valid = set()
        self._refs = {}
        roots = list(root_refs)
        _require(len(roots) <= MAX_GRAPH_NODES, "Root count limit.")
        todo = list(roots)
        while todo:
            ref = todo.pop()
            validate_ref(ref)
            d = ref['digest']
            if d in self._records:
                _require(self._refs[d] == ref, "Typed identity mismatch.")
                continue
            _require(len(self._records) < MAX_GRAPH_NODES, "Graph node limit.")
            try:
                raw = resolve(dict(ref))
            except LookupError as exc:
                raise WireError("Unresolved case-local bytes.") from exc
            _require(typed_ref(raw) == ref, "Reference byte identity mismatch.")
            r = decode_canonical(raw)
            validate_schema(r)
            edges = list(_edges(r)) + _payload_edges(r)
            self._records[d], self._refs[d], self._edges[d] = r, dict(ref), edges
            todo.extend(edges)
        # Forest depth is measured independently of cached visits: a shared
        # suffix must not hide a longer path from another root.
        for ref in roots:
            self._order(ref)

    def _order(self, ref):
        self.get(ref)
        states, heights, order = {}, {}, []
        todo = [(ref['digest'], False)]
        while todo:
            d, leaving = todo.pop()
            if leaving:
                heights[d] = 1 + max((heights[x['digest']] for x in self._edges[d]), default=0)
                _require(heights[d] <= MAX_GRAPH_DEPTH, "Graph depth limit.")
                states[d] = 2
                order.append(d)
            elif states.get(d) == 1:
                raise WireError("Cyclic reference graph.")
            elif states.get(d) != 2:
                states[d] = 1
                todo.append((d, True))
                todo.extend((x['digest'], False) for x in reversed(self._edges[d]))
        return order

    def get(self, ref):
        validate_ref(ref)
        d = ref['digest']
        _require(d in self._records and self._refs[d] == ref, "Unavailable case-local record.")
        # Do not expose mutable validated state or cached authority.
        return decode_canonical(canonical_bytes(self._records[d]))

    def payload(self, ref, role=None):
        r = self.get(ref)
        _require(r['kind'] == 'DQ.LAB.DataObject' and (role is None or r['role'] == role), "Data role mismatch.")
        return decode_canonical(bytes.fromhex(r['payload_hex']))

    def validate(self, ref):
        """Validate documentary semantics only; return no native proof/permit."""
        for d in self._order(ref):
            if d not in self._valid:
                self._semantic(self._records[d])
                self._valid.add(d)
        return None

    def _ticket_bytes(self, digest, binding, mutation=None):
        _require(digest in self._records, "Original ticket bytes missing.")
        t = self._records[digest]
        _require(t['kind'] == 'DQ.LAB.OperationTicket' and t['binding_ref'] == binding, "Original ticket mismatch.")
        if mutation is not None:
            _require(t['mutation_ref'] == mutation, "Ticket mutation mismatch.")
        return t

    def _prior(self, head, binding):
        if head is not None:
            return self.get(self.get(head)['resulting_root_ref'])
        return dict(binding_ref=binding, application_sequence=0,
                    **{x: [] for x in ('committed_objects', 'jobs', 'admissions', 'active_slots',
                                      'events', 'outbox', 'read_reservations', 'member_links')})

    def _registry(self, control, mutation):
        return next((x for x in control['registry'] if x['mutation_ref'] == mutation), None)

    def _chain(self, head):
        result = []
        while head is not None:
            _require(len(result) < 128, "Marker history limit.")
            result.append(head)
            head = self.get(head)['previous_marker_ref']
        return result

    def _semantic(self, r):
        name = r['kind'].removeprefix('DQ.LAB.')
        binding = r.get('binding_ref')
        if binding is not None:
            # Every typed edge, including decoded payload refs, preserves the
            # binding. Anchor edges use their exact typed ref, not a path/UUID.
            for edge in list(_edges(r)) + _payload_edges(r):
                child = self.get(edge)
                if child['kind'] == 'DQ.LAB.RootAnchor':
                    _require(edge == binding, "Foreign anchor.")
                elif 'binding_ref' in child:
                    _require(child['binding_ref'] == binding, "Foreign binding.")
        if name == 'RootAnchor':
            p = self.get(r['profile_ref'])
            provider = 'POSIX_DEVICE_INODE' if p['platform'] == 'LINUX_LOCAL' else 'WINDOWS_HANDLE_FILE_ID'
            _require(r['root_identity']['provider'] == r['database_identity']['provider'] == provider)
        elif name == 'DataObject':
            p = self.payload(self._refs[hashlib.sha256(canonical_bytes(r)).hexdigest()])
            role = r['role']
            if 'request_ref' in p:
                self.payload(p['request_ref'], 'REQUEST')
            if role == 'RECEIPT':
                key = self.get(p['key_ref'])
                _require(p['request_ref'] == key['request_ref'])
            elif role == 'EVENT':
                _require(p['revision_from'] + 1 == p['revision_to'])
                _require((p['revision_from'] == 0) == (p['state_from'] is None))
            elif role == 'ACTIVE_SLOT':
                a = self.get(binding)
                _require((p['store_id'], p['namespace_id']) == (a['store_id'], a['namespace_id']))
                _require((p['status'] == 'HELD') == (p['released_at_revision'] is None))
                if p['released_at_revision'] is not None:
                    _require(p['released_at_revision'] >= p['occupied_since_revision'])
        elif name == 'AdmissionKey':
            req, man = self.payload(r['request_ref'], 'REQUEST'), self.payload(r['manifest_ref'], 'MANIFEST')
            _require((r['project_id'], r['purpose_id']) == (req['project_id'], req['purpose_id']))
            _require((r['batch_id'], r['batch_revision']) == (man['batch_id'], man['batch_revision']))
        elif name == 'WriteSet':
            self._write_set(r)
        elif name == 'MutationIntent':
            self._intent(r)
        elif name == 'ProjectionRoot':
            self._projection(r)
        elif name == 'CommitMarker':
            i, w, root = self.get(r['mutation_ref']), self.get(r['write_set_ref']), self.get(r['resulting_root_ref'])
            prior = self._prior(r['previous_marker_ref'], binding)
            _require(r['write_set_ref'] == i['write_set_ref'] and r['previous_marker_ref'] == i['expected_head_ref'])
            _require(r['application_sequence'] == prior['application_sequence'] + 1 == root['application_sequence'])
            _require({x['digest'] for x in root['committed_objects']} ==
                     {x['digest'] for x in prior['committed_objects']} | {x['digest'] for x in w['members']})
            links = prior['member_links'] + [dict(mutation_id=i['mutation_id'], member_ref=x) for x in w['members']]
            _require(root['member_links'] == sorted(links, key=lambda x: (x['mutation_id'], x['member_ref']['digest'])))
            # Immutable history determines indices; prevent an unrelated new
            # job/admission/current projection from hiding beside a valid M.
            _require(len(root['events']) == len(prior['events']) + 1)
        elif name == 'ControlRoot':
            self._control(r)
        elif name == 'SnapshotEvidence':
            c, p, a, custody = self.get(r['control_root_ref']), self.get(r['projection_root_ref']), self.get(binding), r['custody']
            _require(r['control_generation'] == c['control_generation'])
            _require(custody['root_identity'] == a['root_identity'] and custody['database_identity'] == a['database_identity'])
            chain = self._chain(r['observed_head_ref'])
            if chain:
                head = self.get(chain[0])
                _require(head['resulting_root_ref'] == r['projection_root_ref'] and head['application_sequence'] == p['application_sequence'])
            else:
                _require(p['application_sequence'] == 0 and not p['committed_objects'])
            minimum = custody['minimum_acknowledged_marker_ref']
            _require(p['application_sequence'] >= custody['minimum_acknowledged_sequence'])
            if minimum is None:
                _require(custody['minimum_acknowledged_sequence'] == 0)
            else:
                _require(minimum in chain and self.get(minimum)['application_sequence'] == custody['minimum_acknowledged_sequence'])
            for row in c['registry']:
                if row['phase'] == 'PREPARED':
                    _require(self.get(row['mutation_ref'])['expected_head_ref'] == r['observed_head_ref'])
                elif row['phase'] == 'APPLIED':
                    _require(row['marker_ref'] == r['observed_head_ref'])
                elif row['marker_ref'] is not None:
                    _require(row['marker_ref'] in chain)
            _require({_ref_key(x['marker_ref']) for x in c['registry'] if x['marker_ref'] is not None}
                     == {_ref_key(x) for x in chain}, 'Registry/marker history mismatch.')
        elif name == 'OperationTicket':
            if r['phase'] == 'R':
                _require(r['expected_ack_ref'] is not None)
                ack = self.get(r['expected_ack_ref'])
                _require(ack['mutation_ref'] == r['mutation_ref'] and ack['control_generation'] == r['expected_control_generation'] + 1)
                _require(ack['observed_application_head_ref'] == r['expected_application_head_ref'])
                proof = self.get(ack['commit_proof_ref'] or ack['absence_proof_ref'])
                _require(self.get(proof['snapshot_ref'])['custody']['coordinator_run_id'] == r['coordinator_run_id'])
            else:
                _require(r['expected_ack_ref'] is None)
                _require(r['expected_application_head_ref'] == self.get(r['mutation_ref'])['expected_head_ref'])
        elif name in ('PrepareEvidence', 'CommitProof', 'AbsenceProof'):
            self._proof(r, name)
        elif name == 'HoldEvidence':
            if r['intent_ref'] is not None:
                _require(self.get(r['intent_ref'])['mutation_id'] == r['mutation_id'])
        elif name == 'RecoveryEvidence':
            hold = self.get(r['prior_hold_ref'])
            _require(hold['mutation_id'] == r['mutation_id'])
            t = self._ticket_bytes(r['ticket_sha256'], binding)
            _require(self.get(t['mutation_ref'])['mutation_id'] == r['mutation_id'] and t['phase'] == hold['phase'])
            field = {'COMMITTED': 'commit_proof_ref', 'NOT_COMMITTED': 'absence_proof_ref', 'UNKNOWN': 'remaining_hold_ref'}[r['resolution']]
            for k in ('commit_proof_ref', 'absence_proof_ref', 'remaining_hold_ref'):
                _require((r[k] is not None) == (k == field))
            p = self.get(r[field])
            _require((p['mutation_id'] if field == 'remaining_hold_ref' else self.get(p['mutation_ref'])['mutation_id']) == r['mutation_id'])
        elif name == 'ProofAck':
            commit = r['outcome'] == 'COMMITTED'
            _require((r['commit_proof_ref'] is not None) == commit and (r['absence_proof_ref'] is not None) != commit)
            proof = self.get(r['commit_proof_ref'] if commit else r['absence_proof_ref'])
            snap = self.get(proof['snapshot_ref'])
            _require(proof['mutation_ref'] == r['mutation_ref'])
            _require(r['control_generation'] == snap['control_generation'] + 1, 'Ack generation must be pre-R G+1.')
            _require(r['observed_application_head_ref'] == snap['observed_head_ref'], 'Stale Ack head.')

    def _write_set(self, w):
        job, event = self.payload(w['job_ref'], 'JOB'), self.payload(w['event_ref'], 'EVENT')
        slot, key = self.payload(w['slot_ref'], 'ACTIVE_SLOT'), self.get(w['key_ref'])
        _require(w['expected_revision'] + 1 == w['resulting_revision'] == job['revision'] == event['revision_to'])
        _require(w['expected_revision'] == event['revision_from'] and event['mutation_id'] == w['mutation_id'])
        _require(job['job_id'] == event['job_id'] == slot['job_id'] == w['job_id'])
        _require(job['state'] == event['state_to'] == w['target_state'] and job['request_ref'] == key['request_ref'])
        _require((slot['project_id'], slot['purpose_id']) == (key['project_id'], key['purpose_id']))
        _require(w['job_ref'] in w['members'] and w['event_ref'] in w['members'])
        for field, role in [('receipt_ref', 'RECEIPT'), ('outbox_ref', 'OUTBOX'),
                            ('read_reservation_ref', 'READ_RESERVATION'), ('terminal_proof_ref', 'TERMINAL_PROOF')]:
            if w[field] is not None:
                p = self.payload(w[field], role)
                _require(p['job_id'] == w['job_id'])
                if 'request_ref' in p:
                    _require(p['request_ref'] == key['request_ref'])
                if role == 'RECEIPT':
                    _require(p['key_ref'] == w['key_ref'])
                else:
                    _require(w[field] in w['members'])
        if w['slot_action'] == 'RETAIN':
            _require(slot['status'] == 'HELD' and w['slot_ref'] not in w['members'])
        else:
            _require(w['slot_ref'] in w['members'])
            _require(slot['status'] == ('HELD' if w['slot_action'] == 'ACQUIRE' else 'RELEASED'))
        if w['slot_action'] == 'RELEASE':
            _require(w['terminal_proof_ref'] is not None and slot['released_at_revision'] == w['resulting_revision'])
            _require(self.payload(w['terminal_proof_ref'])['terminal_state'] == w['target_state'])
        else:
            _require(w['terminal_proof_ref'] is None)

    def _intent(self, i):
        w = self.get(i['write_set_ref']); prior = self._prior(i['expected_head_ref'], i['binding_ref'])
        _require((w['mutation_id'], w['job_id']) == (i['mutation_id'], i['job_id']))
        prior_ids = {x['digest'] for x in prior['committed_objects']}
        _require(not prior_ids.intersection(x['digest'] for x in w['members']), 'Existing objects cannot be new A-members.')
        current = next((x for x in prior['jobs'] if x['job_id'] == i['job_id']), None)
        key, event = self.get(w['key_ref']), self.payload(w['event_ref'])
        allowed = [w['job_ref'], w['event_ref']]
        kind = i['mutation_kind']
        if kind == 'ADMIT':
            _require(current is None and w['expected_revision'] == 0 and w['target_state'] == 'DRAFT')
            _require(w['slot_action'] == 'ACQUIRE' and w['receipt_ref'] is not None)
            _require(self.payload(w['receipt_ref'])['mutation_id'] == i['mutation_id'])
            _require(self.payload(w['slot_ref'])['occupied_since_revision'] == 1)
            _require(not any((x['project_id'], x['purpose_id']) == (key['project_id'], key['purpose_id']) for x in prior['active_slots']))
            _require(not any(x['key_ref'] == w['key_ref'] or x['job_id'] == i['job_id'] for x in prior['admissions']))
            allowed += [w['receipt_ref'], w['slot_ref']]
            allowed += [x for x in (key['request_ref'], key['manifest_ref']) if x['digest'] not in prior_ids]
        else:
            _require(current is not None, 'Missing current job.')
            j = self.payload(current['job_ref'])
            _require(j['revision'] == w['expected_revision'] and j['state'] not in ('CANCELLED', 'FAILED'))
            _require(event['state_from'] == j['state'])
            admission = next(x for x in prior['admissions'] if x['job_id'] == i['job_id'])
            _require(admission['key_ref'] == w['key_ref'])
            if w['receipt_ref'] is not None:
                _require(w['receipt_ref'] == admission['receipt_ref'])
            held = next(x for x in prior['active_slots'] if self.payload(x['slot_ref'])['job_id'] == i['job_id'])
            if kind == 'TERMINAL_MODEL':
                _require(w['slot_action'] == 'RELEASE' and w['target_state'] in ('CANCELLED', 'FAILED'))
                _require(self.payload(w['slot_ref'])['occupied_since_revision'] == self.payload(held['slot_ref'])['occupied_since_revision'])
                allowed += [w['slot_ref'], w['terminal_proof_ref']]
            else:
                _require(w['slot_action'] == 'RETAIN' and w['slot_ref'] == held['slot_ref'])
                if kind == 'ADVANCE_MODEL':
                    _require(j['state'] == 'DRAFT' and w['target_state'] == 'LAB_CHECKPOINT')
                else:
                    _require(w['target_state'] == j['state'])
                    field = 'outbox_ref' if kind == 'ENQUEUE_MODEL' else 'read_reservation_ref'
                    _require(w[field] is not None)
                    allowed.append(w[field])
                    p = self.payload(w[field])
                    if kind == 'ENQUEUE_MODEL':
                        _require(not any(self.payload(x)['job_id'] == i['job_id'] for x in prior['outbox']))
                    else:
                        reads = [self.payload(x) for x in prior['read_reservations']]
                        reads = [x for x in reads if (x['job_id'], x['checkpoint_id']) == (p['job_id'], p['checkpoint_id'])]
                        _require(p['call_index'] == len(reads) + 1 <= 3)
                        _require(all(x['base_cursor'] == p['base_cursor'] for x in reads))
        _require(None not in allowed and {_ref_key(x) for x in allowed} == {_ref_key(x) for x in w['members']}, 'Extraneous or missing member.')

    def _projection(self, r):
        objects = {x['digest']: self.get(x) for x in r['committed_objects']}
        _require(len({x['object_id'] for x in objects.values()}) == len(objects), 'Duplicate immutable object identity.')
        def payloads(role):
            return [(ref, self.payload(ref, role)) for ref in r['committed_objects'] if objects[ref['digest']]['role'] == role]
        links = r['member_links']
        _require(len(links) == len(objects) and {x['member_ref']['digest'] for x in links} == set(objects), 'Unlinked or multiply applied object.')
        mutations = {x['mutation_id'] for x in links}
        _require(r['application_sequence'] == len(mutations))
        jobs = {}
        for ref, p in payloads('JOB'):
            jobs.setdefault(p['job_id'], []).append((ref, p))
        _require({x['job_id'] for x in r['jobs']} == set(jobs))
        _require(len(r['admissions']) == len(jobs))
        for field, role in [('events', 'EVENT'), ('outbox', 'OUTBOX'), ('read_reservations', 'READ_RESERVATION')]:
            _require(r[field] == sorted((ref for ref, _ in payloads(role)), key=_ref_key), 'Projection index incomplete.')
        _require(len({p['event_id'] for _, p in payloads('EVENT')}) == len(r['events']))
        _require(len(r['events']) == r['application_sequence'])
        for mid in mutations:
            events = [p for _, p in payloads('EVENT') if p['mutation_id'] == mid]
            _require(len(events) == 1)
            members = [x['member_ref'] for x in links if x['mutation_id'] == mid]
            _require(all(self.get(x)['owner_job_id'] in (None, events[0]['job_id']) for x in members))
            _require(any(self.get(x)['role'] == 'EVENT' and self.payload(x)['mutation_id'] == mid for x in members))
            changed = [self.payload(x) for x in members if self.get(x)['role'] == 'JOB']
            _require(len(changed) == 1 and changed[0]['job_id'] == events[0]['job_id']
                     and changed[0]['revision'] == events[0]['revision_to'])
            for x in members:
                if self.get(x)['role'] == 'RECEIPT':
                    _require(self.payload(x)['mutation_id'] == mid)
        current = {}
        for job_id, versions in jobs.items():
            versions.sort(key=lambda x: x[1]['revision'])
            _require([p['revision'] for _, p in versions] == list(range(1, len(versions) + 1)))
            _require(all(p['state'] not in ('CANCELLED', 'FAILED') for _, p in versions[:-1]))
            latest_ref, latest = versions[-1]; current[job_id] = latest
            _require(next(x['job_ref'] for x in r['jobs'] if x['job_id'] == job_id) == latest_ref)
            events = sorted([p for _, p in payloads('EVENT') if p['job_id'] == job_id], key=lambda x: x['revision_to'])
            _require(len(events) == len(versions))
            for idx, ((_, j), e) in enumerate(zip(versions, events)):
                _require(e['revision_from'] == idx and e['revision_to'] == idx + 1 and e['state_to'] == j['state'])
                _require(e['state_from'] == (None if idx == 0 else versions[idx-1][1]['state']))
            a = next((x for x in r['admissions'] if x['job_id'] == job_id), None)
            _require(a is not None)
            rec, key = self.payload(a['receipt_ref'], 'RECEIPT'), self.get(a['key_ref'])
            _require(a['receipt_ref']['digest'] in objects and rec['job_id'] == job_id and rec['key_ref'] == a['key_ref'])
            _require(all(j['request_ref'] == rec['request_ref'] == key['request_ref'] for _, j in versions))
            _require(key['request_ref']['digest'] in objects and key['manifest_ref']['digest'] in objects)
            held = [x for x in r['active_slots'] if self.payload(x['slot_ref'], 'ACTIVE_SLOT')['job_id'] == job_id]
            terminal = latest['state'] in ('CANCELLED', 'FAILED')
            _require(len(held) == (0 if terminal else 1))
            if held:
                x = held[0]; s = self.payload(x['slot_ref'])
                _require(x['slot_ref']['digest'] in objects and s['status'] == 'HELD')
                _require((x['project_id'], x['purpose_id']) == (s['project_id'], s['purpose_id']) == (key['project_id'], key['purpose_id']))
            if terminal:
                _require(any(p['job_id'] == job_id and p['terminal_state'] == latest['state'] for _, p in payloads('TERMINAL_PROOF')))
                _require(any(p['job_id'] == job_id and p['status'] == 'RELEASED' and p['released_at_revision'] == latest['revision'] for _, p in payloads('ACTIVE_SLOT')))
        _require(all(x['owner_job_id'] is None or x['owner_job_id'] in jobs for x in objects.values()))
        for x in r['active_slots']:
            _require(x['slot_ref']['digest'] in objects)
            s = self.payload(x['slot_ref'], 'ACTIVE_SLOT')
            _require(s['job_id'] in jobs and s['status'] == 'HELD')
        _require(len(payloads('RECEIPT')) == len(jobs))
        _require(len({p['receipt_id'] for _, p in payloads('RECEIPT')}) == len(jobs))
        for role in ('OUTBOX', 'RECEIPT'):
            _require(all(p['request_ref'] == current[p['job_id']]['request_ref'] for _, p in payloads(role)))
        _require(len({p['job_id'] for _, p in payloads('OUTBOX')}) == len(r['outbox']))
        _require(len({p['effect_token'] for _, p in payloads('OUTBOX')}) == len(r['outbox']))
        _require(len({p['outbox_id'] for _, p in payloads('OUTBOX')}) == len(r['outbox']))
        reservations = {}
        for _, p in payloads('READ_RESERVATION'):
            reservations.setdefault((p['job_id'], p['checkpoint_id']), []).append(p)
        for rows in reservations.values():
            _require(sorted(p['call_index'] for p in rows) == list(range(1, len(rows)+1)) and len(rows) <= 3)
            _require(len({p['base_cursor'] for p in rows}) == 1)

    def _control(self, r):
        mids, pending, expected_acks, cost = set(), [], [], 0
        allowed_staged = {}
        for row in r['registry']:
            i = self.get(row['mutation_ref']); mid = i['mutation_id']
            _require(mid not in mids); mids.add(mid)
            w = self.get(i['write_set_ref'])
            phase = row['phase']; marker, ack = row['marker_ref'], row['latest_ack_ref']
            _require((marker is not None) == (phase in ('APPLIED', 'RESOLVED_COMMITTED')))
            _require((ack is not None) == phase.startswith('RESOLVED_'))
            if marker is not None:
                _require(self.get(marker)['mutation_ref'] == row['mutation_ref'])
            if ack is not None:
                a = self.get(ack); expected_acks.append(ack)
                _require(a['mutation_ref'] == row['mutation_ref'] and phase == 'RESOLVED_' + a['outcome'])
                _require(a['control_generation'] <= r['control_generation'])
            else:
                pending.append(mid)
            if phase == 'PREPARED': cost += 1
            elif phase == 'APPLIED': cost += 2
            elif phase == 'RESOLVED_COMMITTED': cost += 3
            else: cost += 2 if self.get(self.get(ack)['absence_proof_ref'])['registry_present'] else 1
            inputs = self.get(w['key_ref'])
            allowed_staged[mid] = {x['digest'] for x in w['members']} | {inputs['request_ref']['digest'], inputs['manifest_ref']['digest']}
            staged = {x['object_ref']['digest'] for x in r['staged_links'] if x['mutation_id'] == mid}
            _require({x['digest'] for x in w['members']} <= staged)
        _require(len(pending) <= 1 and r['pending_mutation_id'] == (pending[0] if pending else None))
        _require(r['control_generation'] == cost, 'Control generation does not match P/A/R history.')
        _require(r['proof_acks'] == sorted(expected_acks, key=_ref_key))
        for x in r['staged_links']:
            _require(x['mutation_id'] in allowed_staged and x['object_ref']['digest'] in allowed_staged[x['mutation_id']])

    def _proof(self, r, name):
        i, w, s = self.get(r['mutation_ref']), self.get(r['write_set_ref']), self.get(r['snapshot_ref'])
        c, p = self.get(s['control_root_ref']), self.get(s['projection_root_ref'])
        _require(i['write_set_ref'] == r['write_set_ref'])
        row = self._registry(c, r['mutation_ref'])
        if name == 'PrepareEvidence':
            _require(row is not None and row['phase'] == 'PREPARED')
            _require(c['pending_mutation_id'] == r['pending_mutation_id'] == i['mutation_id'])
            _require(r['prepared_control_generation'] == c['control_generation'])
            _require(s['observed_head_ref'] == i['expected_head_ref'] and r['staged_member_refs'] == w['members'])
        elif name == 'CommitProof':
            m = self.get(r['marker_ref'])
            _require(m['mutation_ref'] == r['mutation_ref'] and m['write_set_ref'] == r['write_set_ref'])
            _require(r['marker_ref'] in self._chain(s['observed_head_ref']))
            _require(row is not None and row['phase'] in ('APPLIED', 'RESOLVED_COMMITTED') and row['marker_ref'] == r['marker_ref'])
            _require([x['member_ref'] for x in p['member_links'] if x['mutation_id'] == i['mutation_id']] == w['members'])
            _require({x['digest'] for x in w['members']} <= {x['digest'] for x in p['committed_objects']})
        else:
            t = self._ticket_bytes(r['ticket_sha256'], r['binding_ref'], r['mutation_ref'])
            _require(t['phase'] in ('P', 'A') and t['coordinator_run_id'] == s['custody']['coordinator_run_id'])
            _require(t['expected_application_head_ref'] == r['expected_previous_head_ref'] == i['expected_head_ref'] == s['observed_head_ref'])
            _require(r['registry_present'] == (row is not None))
            _require(r['intent_source'] == ('REGISTERED_DB' if row is not None else 'COORDINATOR_TICKET'))
            _require(row is None or row['phase'] == 'PREPARED')
            _require(t['expected_control_generation'] + (1 if t['phase'] == 'P' and row is not None else 0) == s['control_generation'])
            _require(not {x['digest'] for x in w['members']}.intersection(x['digest'] for x in p['committed_objects']))
            _require(not any(x['mutation_id'] == i['mutation_id'] for x in p['member_links']))
            prior = self._prior(i['expected_head_ref'], r['binding_ref'])
            _require(all(p[k] == prior[k] for k in prior), 'Application projection changed despite absence assertion.')


@dataclass(frozen=True)
class DocumentDecision:
    """Conditional fixture semantics, never a native application outcome."""

    application_outcome: str
    control_generation: object
    namespace_barrier: bool
    resolution_R_outcome: str
    uncertainty_hold: bool
    next_action: str

    @property
    def native_qualified(self):
        return False

    @property
    def native_application_outcome(self):
        return 'UNKNOWN'

    @property
    def execution_authorized(self):
        return False


def evaluate_document_case(inputs, facts, resolve):
    """Evaluate case-local documentary inputs WITHOUT an id or expected answer.

    Facts are explicit conditional premises of a synthetic document case.
    This function cannot establish live custody, checks, retention or native
    COMMITTED/NOT_COMMITTED. All returned native authority fields stay denied.
    """
    known, generation, phase = 'UNKNOWN', None, 'A'

    def result(action='READ_ONLY_BLOCKED', uncertain=True, barrier=True, resolution=None):
        return DocumentDecision(known, generation, barrier,
                                resolution or ('UNKNOWN' if phase == 'R' else 'NOT_STARTED'),
                                uncertain, action)

    try:
        allowed = {'absence', 'snapshot', 'ticket', 'original_ticket', 'prepare', 'candidate_snapshot',
                   'hold', 'expected_binding', 'observed_binding', 'ack_expected', 'proof',
                   'post_snapshot', 'fresh_snapshot', 'ack_observed', 'ack_bytes', 'rejected_absence'}
        _require(type(inputs) is dict and set(inputs) <= allowed)
        factkeys = {'complete_snapshot', 'coordinator_continuous', 'custody_qualified',
                    'expected_ack_retained', 'ticket_retained'}
        _require(type(facts) is dict and factkeys <= set(facts) <= factkeys | {'provided_ack_digest'})
        for k in factkeys:
            _shape(facts[k], BOOL)
        if 'provided_ack_digest' in facts:
            _shape(facts['provided_ack_digest'], DIGEST)
        # Isolate an original valid A proof before loading observed R material.
        # A damaged optional snapshot/Ack must not erase established A knowledge.
        if facts['coordinator_continuous'] and facts['ticket_retained'] and facts['custody_qualified'] and 'ticket' in inputs:
            try:
                # Canonical retained ticket metadata identifies the subject;
                # do not require a damaged future R dependency to revalidate
                # an independently supplied original A proof.
                traw = resolve(dict(inputs['ticket']))
                _require(typed_ref(traw) == inputs['ticket'])
                bt = decode_canonical(traw)
                validate_schema(bt)
                _require(bt['kind'] == 'DQ.LAB.OperationTicket')
                phase = bt['phase']
                base_refs = [inputs['proof']] if 'proof' in inputs else [inputs['ticket']]
                if 'original_ticket' in inputs:
                    base_refs.append(inputs['original_ticket'])
                base = DocumentGraph(base_refs, resolve)
                bp = inputs.get('proof')
                if bp is None and phase == 'R' and facts['expected_ack_retained']:
                    bp = base.get(bt['expected_ack_ref'])['commit_proof_ref']
                if bp is not None:
                    base.validate(bp); bproof = base.get(bp)
                    _require(bproof['kind'] == 'DQ.LAB.CommitProof' and bproof['mutation_ref'] == bt['mutation_ref']
                             and bproof['binding_ref'] == bt['binding_ref'])
                    known = 'COMMITTED'
            except (WireError, LookupError):
                pass
        g = DocumentGraph(inputs.values(), resolve)
        snapref = next((inputs[x] for x in ('post_snapshot', 'fresh_snapshot', 'snapshot', 'candidate_snapshot') if x in inputs), None)
        if snapref is not None:
            snap = g.get(snapref)
            _require(snap['kind'] == 'DQ.LAB.SnapshotEvidence')
            # Observed documentary generation is displayed even for rejected
            # snapshots. It does not imply a qualified snapshot or authority.
            generation = snap['control_generation']
        ticketref = inputs.get('ticket')
        if ticketref is not None:
            ticket = g.get(ticketref)
            _require(ticket['kind'] == 'DQ.LAB.OperationTicket')
            phase = ticket['phase']
        if not facts['coordinator_continuous']:
            generation = None
            return result('BLOCKED_WHOLE_APPLICATION_RECOVERY')
        if not facts['ticket_retained'] or ticketref is None or not facts['custody_qualified']:
            generation = None
            return result()
        if inputs.get('expected_binding') != inputs.get('observed_binding'):
            return result()

        # A previously established documentary A proof is evaluated separately
        # from an invalid observed Ack/current R snapshot. Never downgrade it
        # merely because R ACK is lost or damaged.
        proofref = inputs.get('proof')
        if proofref is None and phase == 'R' and ticket['expected_ack_ref'] is not None and facts['expected_ack_retained']:
            proofref = g.get(ticket['expected_ack_ref'])['commit_proof_ref']
        if proofref is not None:
            g.validate(proofref)
            proof = g.get(proofref)
            _require(proof['kind'] == 'DQ.LAB.CommitProof' and proof['mutation_ref'] == ticket['mutation_ref'])
            known = 'COMMITTED'
        g.validate(ticketref)
        if 'hold' in inputs:
            g.validate(inputs['hold'])
            h = g.get(inputs['hold'])
            _require(h['mutation_id'] == g.get(ticket['mutation_ref'])['mutation_id'] and h['phase'] == phase)
        if not facts['complete_snapshot']:
            if any(x in inputs for x in ('candidate_snapshot', 'ack_observed', 'ack_bytes', 'rejected_absence')):
                return result()
            return result('INSPECT_' + phase)
        if phase != 'R':
            if 'prepare' in inputs:
                g.validate(inputs['prepare']); p = g.get(inputs['prepare']); ps = g.get(p['snapshot_ref'])
                _require(p['mutation_ref'] == ticket['mutation_ref'] and ticket['phase'] == 'A')
                _require(ticket['expected_control_generation'] == p['prepared_control_generation'])
                _require(ticket['expected_application_head_ref'] == ps['observed_head_ref'])
                if 'absence' in inputs:
                    g.validate(inputs['absence'])
                known = 'NOT_ATTEMPTED'
                return result('APPLY_SAME_M_OR_CLOSE_NEGATIVE' if 'absence' in inputs else 'APPLY_SAME_M', False)
            if 'absence' in inputs:
                g.validate(inputs['absence']); ap = g.get(inputs['absence'])
                _require(ap['mutation_ref'] == ticket['mutation_ref'] and ap['ticket_sha256'] == ticketref['digest'])
                known = 'NOT_COMMITTED'
                return result('ACK_NEGATIVE_R', False)
            return result()

        _require(facts['expected_ack_retained'], 'Exact retained R Ack bundle missing.')
        ackref = ticket['expected_ack_ref']; ack = g.get(ackref)
        g.validate(ackref)
        originalproofref = ack['commit_proof_ref'] or ack['absence_proof_ref']
        originalproof = g.get(originalproofref); pre = g.get(originalproof['snapshot_ref'])
        known = ack['outcome']
        if 'provided_ack_digest' in facts:
            _require(facts['provided_ack_digest'] == ackref['digest'])
        supplied = inputs.get('ack_observed') or inputs.get('ack_bytes') or inputs.get('ack_expected')
        if supplied is not None:
            _require(supplied == ackref, 'Observed Ack is not exact retained Ack.')
            g.validate(supplied)
        _require(snapref is not None)
        g.validate(snapref)
        current = g.get(snapref); control = g.get(current['control_root_ref'])
        _require(current['binding_ref'] == ticket['binding_ref'] == pre['binding_ref'])
        _require(current['custody']['coordinator_run_id'] == ticket['coordinator_run_id'])
        _require(current['observed_head_ref'] == pre['observed_head_ref'] == ticket['expected_application_head_ref'])
        _require(current['projection_root_ref'] == pre['projection_root_ref'])
        if 'post_snapshot' in inputs:
            row = g._registry(control, ticket['mutation_ref'])
            _require(row is not None and row['phase'] == 'RESOLVED_' + ack['outcome'] and row['latest_ack_ref'] == ackref)
            _require(control['pending_mutation_id'] is None and ackref in control['proof_acks'])
            _require(current['control_generation'] == ack['control_generation'] == ticket['expected_control_generation'] + 1)
            action = 'NEXT_NEW_M' if known == 'COMMITTED' else ('OLD_M_READ_ONLY' if not originalproof['registry_present'] else 'OLD_M_READ_ONLY_NEW_M_BY_GRANT')
            return result(action, False, False, 'COMMITTED')
        _require(current['control_root_ref'] == pre['control_root_ref'])
        _require(current['control_generation'] == pre['control_generation'] == ticket['expected_control_generation'])
        mid = g.get(ticket['mutation_ref'])['mutation_id']
        _require(control['pending_mutation_id'] == (mid if originalproof['kind'] == 'DQ.LAB.CommitProof' or originalproof['registry_present'] else None))
        _require(ackref not in control['proof_acks'])
        row = g._registry(control, ticket['mutation_ref'])
        _require(row is None or row['latest_ack_ref'] is None)
        if 'fresh_snapshot' in inputs:
            return result('RETRY_EXACT_R', False, True, 'NOT_COMMITTED')
        return result('EXACT_R', False, True, 'NOT_STARTED')
    except (WireError, LookupError):
        return result()
