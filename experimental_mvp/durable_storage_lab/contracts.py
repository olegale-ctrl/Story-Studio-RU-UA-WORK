"""Pure DQ.LAB v2 wire primitives; these do not establish evidence authority.

This increment implements canonical encoding and typed-reference byte closure,
not schema/role/proof validation or native custody. A valid hash, or even a
closed acyclic byte graph, MUST NOT authorize a storage operation or outcome.
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
