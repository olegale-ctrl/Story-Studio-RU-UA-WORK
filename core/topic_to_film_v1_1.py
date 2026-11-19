"""SP/1.1 local diagnostics: structural + semantic checks, never authority.

Legacy SP/1 and its evidence are unchanged. There is no implicit object upgrade.
Only repository-owned schemas in this module's fixed profile may be interpreted.
"""
from copy import deepcopy
import json
from pathlib import Path
import re

from core import topic_to_film as legacy
from core.media_paths import validate_media_path
from story_intelligence.codec_v1 import canonical_si_json, canonical_si_sha256
from story_intelligence.model_v1 import validate_si_ref, validate_eref

VERSION = "SP/1.1-DIAGNOSTIC"
POLICY = "SP-DIAGNOSTIC/1.1"
AXES = legacy.AXES
ROUTES = deepcopy(legacy.ROUTES)
SCHEMAS = Path(__file__).resolve().parents[1] / "schemas" / "topic-to-film-v1-1"
KINDS = ("route", "readiness", "jobs", "artifact_manifest", "job_intent",
         "technical_gate_report", "production_readiness_report")
BODY_FIELDS = ("schema_version", "policy_version", "route", "mode", "fallback_class",
               "inputs", "requested_attestations", "proposed_job_types")


class DiagnosticValidationError(ValueError):
    def __init__(self, code, path, message):
        self.code, self.path = code, path
        super().__init__(f"{code} at {path}: {message}")


def _fail(code, path, message):
    raise DiagnosticValidationError(code, path, message)


def _shape(schema, value, path):
    """Fixed structural profile of the seven local schemas; no plugin/ref loading.

    Not a general JSON Schema engine. Unsupported keywords fail closed, including
    $ref. Schema meta-validation/differential tests use jsonschema as test tooling;
    runtime keeps the repository's stdlib-only CLI dependency boundary.
    """
    supported = {"$schema", "title", "description", "type", "additionalProperties",
                 "required", "properties", "enum", "const", "items", "maxItems",
                 "minItems", "maxLength", "minLength", "pattern", "minimum",
                 "minProperties", "propertyNames", "oneOf", "anyOf", "not"}
    if set(schema) - supported:
        _fail("SCHEMA_PROFILE", path, "Unsupported structural keyword")
    if "const" in schema and (type(value) is not type(schema["const"]) or value != schema["const"]):
        _fail("STRUCTURE", path, "Wrong constant/version")
    if "enum" in schema and not any(type(value) is type(x) and value == x for x in schema["enum"]):
        _fail("STRUCTURE", path, "Outside enum")
    types = {"object": dict, "array": list, "string": str, "integer": int, "boolean": bool}
    if "type" in schema and (schema["type"] not in types or type(value) is not types[schema["type"]]):
        _fail("STRUCTURE", path, "Wrong JSON type")
    for keyword, count in (("oneOf", 1), ("anyOf", None)):
        if keyword in schema:
            matches = 0
            for option in schema[keyword]:
                try:
                    _shape(option, value, path)
                    matches += 1
                except DiagnosticValidationError as exc:
                    if exc.code == "SCHEMA_PROFILE":
                        raise
            if (count is not None and matches != count) or (count is None and matches == 0):
                _fail("STRUCTURE", path, "Wrong input alternative")
    if "not" in schema:
        try:
            _shape(schema["not"], value, path)
        except DiagnosticValidationError as exc:
            if exc.code == "SCHEMA_PROFILE":
                raise
        else:
            _fail("STRUCTURE", path, "Forbidden input combination")
    if type(value) is dict:
        if not set(schema.get("required", ())).issubset(value):
            _fail("STRUCTURE", path, "Missing field")
        if len(value) < schema.get("minProperties", 0):
            _fail("STRUCTURE", path, "Empty object")
        props = schema.get("properties", {})
        for key, item in value.items():
            if "propertyNames" in schema:
                _shape(schema["propertyNames"], key, path)
            if key in props:
                _shape(props[key], item, path + "." + key)
            elif schema.get("additionalProperties") is False:
                _fail("STRUCTURE", path + "." + key, "Unknown field")
            elif type(schema.get("additionalProperties")) is dict:
                _shape(schema["additionalProperties"], item, path + "." + key)
    if type(value) is list:
        if not schema.get("minItems", 0) <= len(value) <= schema.get("maxItems", 10000):
            _fail("STRUCTURE", path, "Array length")
        for i, item in enumerate(value):
            _shape(schema.get("items", {}), item, f"{path}[{i}]")
    if type(value) is str:
        if not schema.get("minLength", 0) <= len(value) <= schema.get("maxLength", 100000):
            _fail("STRUCTURE", path, "Text length")
        if "pattern" in schema and re.search(schema["pattern"], value) is None:
            _fail("STRUCTURE", path, "Text pattern")
    if type(value) is int and value < schema.get("minimum", value):
        _fail("STRUCTURE", path, "Integer range")


def validate_structure(kind, value):
    if kind not in KINDS:
        _fail("SCHEMA_KIND", "$", "Unknown diagnostic artifact")
    # Bound/reject non-plain values before walking untrusted containers.
    canonical_si_json(value)
    schema = json.loads((SCHEMAS / (kind + ".schema.json")).read_text(encoding="utf-8"))
    _shape(schema, value, "$")
    return deepcopy(value)


def _path(value):
    normalized = validate_media_path(value)
    if value != normalized:
        _fail("PATH", "$", "Use canonical portable relative path; no implicit normalization")
    return value


def _inputs(inputs):
    route = legacy.classify(**inputs)
    if "materials" in inputs:
        legacy.validate_materials(inputs["materials"])
        plan = inputs["plan"]
        expected = {}
        for i, scene in enumerate(plan["scenes"], 1):
            if not scene.get("image"):
                _fail("MATERIALS", "$.inputs.plan", "Route D requires explicit images, no implicit placeholder")
            expected[f"voice{i}"] = f"voice{i}.wav"
            expected[f"image{i}"] = scene["image"]
        if set(inputs["materials"]) != set(expected):
            _fail("MATERIALS", "$.inputs.materials", "Require exactly voiceN/imageN for each scene")
        for role, binding in inputs["materials"].items():
            _path(binding["path"])
            if binding["path"] != expected[role]:
                _fail("MATERIALS", "$.inputs.materials." + role, "Material does not match plan/profile")
    return route


def _intent(kwargs):
    # Build a fresh diagnostic request using existing pure rules. Never accept or
    # relabel a legacy object as a new object; new version/policy enter the hash.
    value = legacy.prepare_intent(**kwargs)
    value["schema_version"], value["policy_version"] = VERSION, POLICY
    value["intent_sha256"] = canonical_si_sha256({k: value[k] for k in BODY_FIELDS})
    return value


def validate_diagnostic(kind, value):
    """Both stages mandatory. Returns detached diagnostic data, never a receipt."""
    value = validate_structure(kind, value)
    try:
        if kind == "job_intent":
            route = _inputs(value["inputs"])
            if value["route"] != route or value["proposed_job_types"] != ROUTES[route]:
                _fail("ROUTE_STAGES", "$", "Exact route and ordered stage list required")
            expected = _intent({**value["inputs"], "mode": value["mode"],
                "fallback": value["fallback_class"],
                "authorize_render": value["requested_attestations"]["render"],
                "declare_facts_reviewed": value["requested_attestations"]["facts"],
                "declare_rights_cleared": value["requested_attestations"]["rights"]})
            if value["intent_sha256"] != expected["intent_sha256"]:
                _fail("DIGEST", "$.intent_sha256", "Canonical intent digest mismatch")
            if value["blockers"] != expected["blockers"]:
                _fail("BLOCKERS", "$.blockers", "Required diagnostic blockers cannot be omitted/reordered")
        for ref in value.get("evidence_refs", []):
            (validate_si_ref if "type" in ref else validate_eref)(ref)
        for binding in value.get("artifact_bindings", value.get("artifacts", [])):
            if not binding["role"].strip():
                _fail("TEXT", "$", "Blank artifact role")
            _path(binding["path"])
        if kind in ("readiness", "artifact_manifest"):
            bindings = value.get("artifact_bindings", value.get("artifacts", []))
            if len({x["role"] for x in bindings}) != len(bindings):
                _fail("BINDINGS", "$", "Duplicate artifact role")
        if any(not x.strip() for x in value.get("blockers", [])):
            _fail("TEXT", "$.blockers", "Blank blocker")
    except DiagnosticValidationError:
        raise
    except ValueError as exc:
        _fail("SEMANTIC", "$", str(exc))
    return value


def prepare_intent(**kwargs):
    return validate_diagnostic("job_intent", _intent(kwargs))


def initial_readiness(intent):
    intent = validate_diagnostic("job_intent", intent)
    value = legacy.initial_readiness(intent)
    value["schema_version"], value["policy_version"] = VERSION, POLICY
    return validate_diagnostic("readiness", value)


def assess_release(mode, readiness, *, bindings_current="unknown", creative_review="unknown"):
    if mode not in ("draft", "production"):
        _fail("MODE", "$", "Invalid mode")
    for state in (bindings_current, creative_review):
        if type(state) is not str or state not in ("unknown", "false", "true"):
            _fail("STATE", "$", "Expected tri-state assertion")
    blockers = []
    try:
        readiness = validate_diagnostic("readiness", readiness)
    except ValueError:
        blockers.append("INVALID_READINESS")
    if not blockers:
        if mode != "production":
            blockers.append("PRODUCTION_REQUIRED")
        blockers.extend("AXIS_" + a.upper() for a in AXES if readiness[a] != "true")
        if readiness["fallback_class"] != "none":
            blockers.append("FALLBACK_NOT_QUALIFIED")
        if readiness["blockers"]:
            blockers.append("UNRESOLVED_READINESS_BLOCKERS")
        if bindings_current != "true":
            blockers.append("EVIDENCE_BINDINGS_UNCONFIRMED")
        if creative_review != "true":
            blockers.append("HUMAN_CREATIVE_REVIEW_REQUIRED")
    necessary = not blockers
    blockers.extend(["BLOCKED_ATTESTATION_VERIFIER", "BLOCKED_RELEASE_CONTRACT"])
    return validate_diagnostic("production_readiness_report", {
        "schema_version": VERSION, "necessary_conditions_satisfied": necessary,
        "release_allowed": False, "status": "BLOCKED_CONTRACT", "blockers": blockers})


def run_gates(*args, **kwargs):
    from core.topic_to_film_gates import run_gates as observe
    # A newly generated observation, not conversion/acceptance of stored SP/1.
    report = observe(*args, **kwargs)
    report["schema_version"] = VERSION
    return validate_diagnostic("technical_gate_report", report)
