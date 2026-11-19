"""Read-only intermediate diagnostics; final execution/validation is blocked.

No decoder, renderer, model, remote service, queue or publication is invoked.
Path checks reduce accidental exposure; they do not qualify hostile OS storage.
"""
import json
from pathlib import Path
import stat

from core.media_paths import validate_media_path
from core.project_schema import Project
from core.timeline_audit import audit_timeline
from core.topic_to_film import VERSION, observe_bytes, validate_plan, validate_wav
from scripts.first_video import read_plan, safe_image, wav_ms


def read_local(path, limit):
    """Read a bounded regular file; reject visible symlink/reparse ancestors.

    This is an observation, not an atomic authorization/execution snapshot.
    Concurrent rename, hardlinks and malicious filesystems need a trusted broker.
    """
    path = Path(path).absolute()
    for part in [path, *path.parents]:
        info = part.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError("Symlink/reparse paths are not accepted")
    if not stat.S_ISREG(path.stat().st_mode):
        raise ValueError("Expected regular file")
    with path.open("rb") as source:
        data = source.read(limit + 1)
    if len(data) > limit:
        raise ValueError("Input exceeds diagnostic limit")
    return data


def read_json(path):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError("Duplicate JSON key")
            result[key] = value
        return result
    return json.loads(read_local(path, 1_000_000).decode("utf-8-sig"), object_pairs_hook=pairs)


def run_gates(route, *, phase="intermediate", plan_path=None, audio_dir=None,
              images_dir=None, project_path=None, mp4_path=None):
    """Observe declared inputs only; never claim complete asset/render PASS.

    Existing first_video fields/WAV/image resolver, Project and timeline audit
    are reused. Image decoding, video/clip qualification and final FFprobe/full
    decode remain Dispatcher-worker proposals; mere presence is not PASS.
    """
    if route not in ("A", "B", "C", "D") or phase not in ("intermediate", "final"):
        raise ValueError("Invalid route/phase")
    checks, blockers, observations = [], [], []

    def check(name, operation):
        try:
            detail = operation()
            checks.append({"check": name, "status": "PASS", "detail": detail})
            return detail
        except (ValueError, OSError, EOFError, TypeError, KeyError) as exc:
            checks.append({"check": name, "status": "FAIL", "detail": str(exc)})
            blockers.append(name.upper() + "_FAILED")
            return None

    plan = None
    if plan_path is not None:
        def inspect_plan():
            value = validate_plan(read_json(plan_path))
            if read_plan(Path(plan_path)) != value:
                raise ValueError("Plan changed between reads")
            observations.append({"role": "plan", **observe_bytes(read_local(plan_path, 1_000_000))})
            return value
        plan = check("plan", inspect_plan)
    elif route in ("C", "D") or phase == "final":
        blockers.append("PLAN_REQUIRED")
    else:
        checks.append({"check": "plan", "status": "NOT_RUN", "detail": "Future stage for route " + route})
    if plan:
        for index, scene in enumerate(plan["scenes"], 1):
            if audio_dir is not None:
                def audio(index=index):
                    path = Path(audio_dir) / f"voice{index}.wav"
                    raw = read_local(path, 16 * 1024 * 1024)
                    result = validate_wav(raw)
                    if wav_ms(path) != result["duration_ms"]:
                        raise ValueError("WAV changed between reads")
                    observations.append({"role": f"voice{index}", **observe_bytes(raw)})
                    return result
                check(f"voice{index}", audio)
            elif route == "D" or phase == "final":
                blockers.append(f"VOICE{index}_REQUIRED")
            if scene.get("image"):
                if images_dir is None:
                    blockers.append(f"IMAGE{index}_REQUIRED")
                else:
                    def image(scene=scene, index=index):
                        name = validate_media_path(scene["image"])
                        raw = read_local(Path(images_dir) / name, 16 * 1024 * 1024)
                        safe_image(Path(images_dir), name)
                        observations.append({"role": f"image{index}", **observe_bytes(raw)})
                        return "PATH_AND_BYTES_ONLY; image decode NOT_RUN"
                    check(f"image{index}", image)
            elif route == "D" or phase == "final":
                blockers.append(f"IMAGE{index}_REQUIRED_NO_IMPLICIT_PLACEHOLDER")
    if project_path is not None:
        check("project", lambda: audit_timeline(Project.from_dict(read_json(project_path))))
    elif phase == "final":
        blockers.append("PROJECT_REQUIRED")
    if mp4_path is not None:
        check("mp4_bytes", lambda: observe_bytes(read_local(mp4_path, 16 * 1024 * 1024)))
    elif phase == "final":
        blockers.append("MP4_REQUIRED")
    if route == "D" or phase == "final":
        blockers.append("BLOCKED_ASSET_DECODER_CONTRACT")
    if phase == "final":
        blockers.extend(["BLOCKED_RENDER_VALIDATION_CONTRACT", "BLOCKED_RESULT_PUBLICATION_CONTRACT"])
    return {"schema_version": VERSION, "route": route, "phase": phase,
            "status": "FAIL" if any(c["status"] == "FAIL" for c in checks) else "BLOCKED" if blockers else "INTERMEDIATE_CHECKS_PASS",
            "checks": checks, "blockers": blockers, "observations": observations,
            "technical_pass": "unknown", "release_allowed": False,
            "not_automatically_proven": ["facts", "rights", "creative_suitability", "subtitle_legibility"]}
