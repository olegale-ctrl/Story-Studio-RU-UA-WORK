"""Offline Topic-to-Film intent and readiness diagnostics. No execution authority.

SP/1 is a PROPOSAL transport, not a PG envelope, SI record or JobStore.
Digests use the existing SI canonical primitive only for local intent equality.
"""
from copy import deepcopy
from hashlib import sha256
import io
import math
import re
import wave

from core.media_paths import validate_media_path
from story_intelligence.codec_v1 import canonical_si_json, canonical_si_sha256

VERSION = "SP/1-PROPOSAL"
POLICY = "SP-REVIEW-ONLY/1"
AXES = ("script_ready", "facts_reviewed", "rights_cleared",
        "authorized_for_render", "technical_pass", "authorized_for_release")
ROUTES = {
    "A": ["script.draft", "plan.from_script", "plan.validate", "assets.voice", "assets.images", "render.mp4", "gates.technical"],
    "B": ["plan.from_script", "plan.validate", "assets.voice", "assets.images", "render.mp4", "gates.technical"],
    "C": ["plan.validate", "assets.voice", "assets.images", "render.mp4", "gates.technical"],
    "D": ["plan.validate", "render.mp4", "gates.technical"],
}


def classify(*, topic=None, script=None, plan=None, materials=None):
    """Classify a single primary input; supplied-but-empty input is an error."""
    if sum(x is not None for x in (topic, script, plan)) != 1:
        raise ValueError("Exactly one of topic, script or plan is required")
    for value in (topic, script):
        if value is not None and (type(value) is not str or not value.strip()):
            raise ValueError("Topic/script must be nonempty text")
    if materials is not None and (plan is None or type(materials) is not dict or not materials):
        raise ValueError("Materials require a plan and a nonempty declared input map")
    if plan is not None:
        validate_plan(plan)
        return "D" if materials is not None else "C"
    return "A" if topic is not None else "B"


def validate_plan(plan):
    """Pure first_video.read_plan-compatible field rules + portable image paths.

    Actual image safety additionally needs the existing safe_image resolver.
    This does not introduce IDs or silently convert an experimental storyboard.
    """
    if type(plan) is not dict or plan.get("locale") not in ("ru", "uk"):
        raise ValueError("Plan requires locale: ru or uk")
    scenes = plan.get("scenes")
    if type(scenes) is not list or not 1 <= len(scenes) <= 20:
        raise ValueError("Plan requires 1..20 scenes")
    for scene in scenes:
        if type(scene) is not dict or type(scene.get("text")) is not str or not scene["text"].strip() or len(scene["text"]) > 2000:
            raise ValueError("Every scene requires nonempty text of at most 2000 characters")
        if "image" in scene:
            image = validate_media_path(scene["image"])
            if "/" in image or "\\" in scene["image"]:
                raise ValueError("first_video images must be simple filenames")
            if image.lower().rsplit(".", 1)[-1] not in ("png", "jpg", "jpeg", "ppm"):
                raise ValueError("Unsupported first_video image format")
    canonical_si_json(plan)  # bounded strict JSON, no float/NaN/subclass coercion
    return deepcopy(plan)


def observe_bytes(data):
    """Raw bytes observation, not an authorized typed reference or identity."""
    if type(data) is not bytes:
        raise ValueError("Expected bytes")
    return {"sha256": sha256(data).hexdigest(), "byte_length": len(data)}


def validate_materials(materials):
    """Validate supplied declarations only; no paths resolved or bytes trusted."""
    if type(materials) is not dict or not materials:
        raise ValueError("Expected nonempty declared material map")
    for role, binding in materials.items():
        if type(role) is not str or not role.strip() or type(binding) is not dict or set(binding) != {"role", "path", "observation"} or binding["role"] != role:
            raise ValueError("Material requires matching role, path and observation")
        validate_media_path(binding["path"])
        observation = binding["observation"]
        if type(observation) is not dict or set(observation) != {"sha256", "byte_length"}:
            raise ValueError("Invalid byte observation")
        if type(observation["sha256"]) is not str or not re.fullmatch("[0-9a-f]{64}", observation["sha256"]):
            raise ValueError("Invalid SHA-256")
        if type(observation["byte_length"]) is not int or observation["byte_length"] < 0:
            raise ValueError("Invalid byte length")
    canonical_si_json(materials)
    return deepcopy(materials)


def prepare_intent(*, topic=None, script=None, plan=None, materials=None,
                   mode="draft", fallback="none", authorize_render=False,
                   declare_facts_reviewed=False, declare_rights_cleared=False):
    if mode not in ("draft", "production") or fallback not in ("none", "equivalent", "degraded", "placeholder"):
        raise ValueError("Invalid mode/fallback")
    for flag in (authorize_render, declare_facts_reviewed, declare_rights_cleared):
        if type(flag) is not bool:
            raise ValueError("Intent flags must be boolean")
    route = classify(topic=topic, script=script, plan=plan, materials=materials)
    if materials is not None:
        validate_materials(materials)
    body = {"schema_version": VERSION, "policy_version": POLICY,
            "route": route, "mode": mode, "fallback_class": fallback,
            "inputs": deepcopy({k: v for k, v in {
                "topic": topic, "script": script, "plan": plan, "materials": materials}.items() if v is not None}),
            "requested_attestations": {"render": authorize_render,
                "facts": declare_facts_reviewed, "rights": declare_rights_cleared},
            "proposed_job_types": list(ROUTES[route])}
    blockers = ["BLOCKED_DISPATCHER_CONTRACT", "BLOCKED_AUTHORITY_CONTRACT", "BLOCKED_STORAGE_CONTRACT"]
    if route == "A" and mode == "production":
        blockers.append("CLASS_A_PRODUCTION_POLICY_REQUIRED")
    if fallback != "none":
        blockers.append({"equivalent": "COMPATIBILITY_EVIDENCE_REQUIRED",
                         "degraded": "DEGRADATION_POLICY_REQUIRED",
                         "placeholder": "PLACEHOLDER_NOT_AUTHORIZED"}[fallback])
    return {**body, "intent_sha256": canonical_si_sha256(body),
            "status": "BLOCKED_DISPATCHER_CONTRACT", "blockers": blockers,
            "accepted_job_ids": []}


def initial_readiness(intent):
    """Unverified user declarations never become an axis value."""
    return {"schema_version": VERSION, "policy_version": POLICY,
            **{axis: "unknown" for axis in AXES},
            "fallback_class": intent["fallback_class"], "si_eligible": "unknown",
            "release_allowed": False, "blockers": list(intent["blockers"]),
            "evidence_refs": [], "artifact_bindings": []}


def binding_matches(approved, current):
    """Exact, bounded snapshot equality only, never authority verification."""
    return canonical_si_json(approved) == canonical_si_json(current)


def assess_release(mode, readiness, *, bindings_current="unknown", creative_review="unknown"):
    """Deterministic necessary-condition check; never a grant or publication.

    Supplied axis labels are diagnostic assertions, not verified attestations.
    Final authority/attestation/release contracts have no implemented adapter.
    """
    if mode not in ("draft", "production") or type(readiness) is not dict:
        raise ValueError("Invalid mode")
    for value in [readiness.get(a, "unknown") for a in AXES] + [bindings_current, creative_review]:
        if type(value) is not str or value not in ("unknown", "false", "true"):
            raise ValueError("Expected unknown|false|true, not booleans")
    blockers = []
    if mode != "production":
        blockers.append("PRODUCTION_REQUIRED")
    blockers.extend("AXIS_" + a.upper() for a in AXES if readiness.get(a) != "true")
    if readiness.get("fallback_class") not in ("none", "equivalent"):
        blockers.append("FALLBACK_NOT_RELEASE_QUALIFIED")
    if readiness.get("fallback_class") == "equivalent":
        blockers.append("COMPATIBILITY_VERIFIER_UNAVAILABLE")
    if readiness.get("policy_version") != POLICY:
        blockers.append("POLICY_BINDING_MISMATCH")
    if bindings_current != "true":
        blockers.append("EVIDENCE_BINDINGS_UNCONFIRMED")
    if creative_review != "true":
        blockers.append("HUMAN_CREATIVE_REVIEW_REQUIRED")
    if readiness.get("blockers"):
        blockers.append("UNRESOLVED_READINESS_BLOCKERS")
    necessary = not blockers
    blockers.extend(["BLOCKED_ATTESTATION_VERIFIER", "BLOCKED_RELEASE_CONTRACT"])
    return {"schema_version": VERSION, "necessary_conditions_satisfied": necessary,
            "release_allowed": False, "status": "BLOCKED_CONTRACT", "blockers": blockers}


def validate_wav(data):
    """Bounded PCM WAV diagnostic, including truncated declared sample data."""
    if type(data) is not bytes or len(data) > 16 * 1024 * 1024:
        raise ValueError("WAV diagnostic limit is 16 MiB")
    try:
        with wave.open(io.BytesIO(data), "rb") as stream:
            frames, channels, width, rate = (stream.getnframes(), stream.getnchannels(),
                                           stream.getsampwidth(), stream.getframerate())
            if not frames or not rate or not channels or stream.getcomptype() != "NONE":
                raise ValueError("Invalid PCM WAV")
            if len(stream.readframes(frames)) != frames * channels * width:
                raise ValueError("Truncated WAV")
            return {"duration_ms": (frames * 1000 + rate - 1) // rate,
                    "frames": frames, "sample_rate": rate}
    except (wave.Error, EOFError) as exc:
        raise ValueError("Invalid WAV") from exc


def hardware_preflight(profile, *, available_disk_bytes=None, required_ram_gib=4,
                       required_disk_bytes=1_000_000_000):
    """Conservative pure diagnostic of an existing hardware_profile.probe result.

    Thresholds are review-only examples, NOT a qualified workload profile.
    """
    if type(profile) is not dict or profile.get("schema_version") != 1:
        raise ValueError("Expected hardware profile v1")
    blockers = ["BLOCKED_WORKLOAD_QUALIFICATION"]
    ram = profile.get("ram_gib")
    if type(ram) not in (int, float) or not math.isfinite(ram) or ram < required_ram_gib:
        blockers.append("RAM_UNKNOWN_OR_INSUFFICIENT")
    if type(available_disk_bytes) is not int or available_disk_bytes < required_disk_bytes:
        blockers.append("DISK_UNKNOWN_OR_INSUFFICIENT")
    if profile.get("cpu_available") is not True:
        blockers.append("CPU_UNAVAILABLE")
    return {"status": "BLOCKED_CONTRACT", "blockers": blockers,
            "provider_execution_allowed": False}
