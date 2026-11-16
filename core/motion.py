"""Ken Burns motion and camera animation for Story Studio RU/UA.

Adapted and enhanced from upstream konlu-story-studio.
Supports smooth zoom, pan, cut-punch, and alternating cinematic presets
for horizontal (16:9) and vertical (9:16) video formats.
"""
from __future__ import annotations

import math
from typing import Any, Dict, List, Optional, Tuple

DEFAULTS = {
    "cut_punch": True,
    "punch_in": 1.15,
    "punch_in_dur": 1.20,
    "punch_out": 1.10,
    "punch_out_dur": 0.80,
    "default_zoom_in": [1.0, 1.12],
    "default_zoom_out": [1.12, 1.0],
}

# Pre-defined alternating camera directions for automatic cinematic variety
MOTION_PRESETS: List[Dict[str, Any]] = [
    {"name": "zoom_in_center", "zoom": [1.0, 1.12], "pivot_start": [0.5, 0.5], "pivot_end": [0.5, 0.5]},
    {"name": "pan_left", "zoom": [1.10, 1.10], "pivot_start": [0.58, 0.5], "pivot_end": [0.42, 0.5]},
    {"name": "zoom_out_center", "zoom": [1.12, 1.0], "pivot_start": [0.5, 0.5], "pivot_end": [0.5, 0.5]},
    {"name": "pan_right", "zoom": [1.10, 1.10], "pivot_start": [0.42, 0.5], "pivot_end": [0.58, 0.5]},
    {"name": "zoom_in_top", "zoom": [1.0, 1.14], "pivot_start": [0.5, 0.4], "pivot_end": [0.5, 0.35]},
]


def _clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def _finite(value: Any, lo: float, hi: float, name: str, sid: str = "shot") -> float:
    v = float(value)
    if not math.isfinite(v) or not lo <= v <= hi:
        raise ValueError(f"{sid}: {name} must be a finite value in {lo}..{hi}")
    return v


def ease_out_cubic(u: float) -> float:
    u = _clamp(u, 0.0, 1.0)
    return 1.0 - (1.0 - u) ** 3


def ease_in_cubic(u: float) -> float:
    u = _clamp(u, 0.0, 1.0)
    return u ** 3


def smoothstep(u: float) -> float:
    u = _clamp(u, 0.0, 1.0)
    return u * u * (3.0 - 2.0 * u)


def resolve_shot_motion(shot: dict, index: int, total_shots: int, preset_mode: bool = True) -> None:
    """Resolve camera motion parameters for a single shot.

    Mutates shot dictionary in place.
    """
    sid = str(shot.get("id", f"shot_{index}"))
    dur = float(shot.get("duration_s", 0.0))

    if preset_mode and "zoom" not in shot:
        preset = MOTION_PRESETS[index % len(MOTION_PRESETS)]
        shot.setdefault("zoom", list(preset["zoom"]))
        shot.setdefault("pivot_start", list(preset["pivot_start"]))
        shot.setdefault("pivot_end", list(preset["pivot_end"]))

    shot.setdefault("zoom", [1.0, 1.10])
    shot.setdefault("pivot_start", [0.5, 0.5])
    shot.setdefault("pivot_end", [0.5, 0.5])
    shot.setdefault("cut_punch", dur >= 4.0)

    z0 = _finite(shot["zoom"][0], 0.8, 3.0, "zoom[0]", sid)
    z1 = _finite(shot["zoom"][1], 0.8, 3.0, "zoom[1]", sid)
    shot["zoom"] = [z0, z1]

    ps0 = [_finite(shot["pivot_start"][0], 0.0, 1.0, "pivot_start[x]", sid),
           _finite(shot["pivot_start"][1], 0.0, 1.0, "pivot_start[y]", sid)]
    pe0 = [_finite(shot["pivot_end"][0], 0.0, 1.0, "pivot_end[x]", sid),
           _finite(shot["pivot_end"][1], 0.0, 1.0, "pivot_end[y]", sid)]
    shot["pivot_start"] = ps0
    shot["pivot_end"] = pe0

    enabled = bool(shot.get("cut_punch", False))
    pin = _finite(shot.get("punch_in", DEFAULTS["punch_in"]), 1.0, 2.0, "punch_in", sid)
    pout = _finite(shot.get("punch_out", DEFAULTS["punch_out"]), 1.0, 2.0, "punch_out", sid)
    pin_dur = _finite(shot.get("punch_in_dur", DEFAULTS["punch_in_dur"]), 0.0, 3.0, "punch_in_dur", sid)
    pout_dur = _finite(shot.get("punch_out_dur", DEFAULTS["punch_out_dur"]), 0.0, 3.0, "punch_out_dur", sid)

    pin_dur = min(pin_dur, dur * 0.35, 1.8)
    pout_dur = min(pout_dur, dur * 0.25, 1.2)
    if pin_dur + pout_dur > dur * 0.50 and dur > 0:
        scale = (dur * 0.50) / (pin_dur + pout_dur)
        pin_dur *= scale
        pout_dur *= scale

    has_in = enabled and pin > 1.001 and pin_dur >= 0.10 and dur >= 0.55
    has_out = enabled and index < total_shots - 1 and pout > 1.001 and pout_dur >= 0.08 and dur >= 0.70

    shot.update(
        duration_s=dur,
        cut_punch=enabled,
        punch_in=pin,
        punch_out=pout,
        punch_in_dur=pin_dur if has_in else 0.0,
        punch_out_dur=pout_dur if has_out else 0.0,
        has_punch_in=has_in,
        has_punch_out=has_out,
    )


def camera_at(shot: dict, t_rel: float, duration_s: Optional[float] = None) -> Tuple[float, float, float]:
    """Calculate (zoom, pivot_x, pivot_y) at relative time t_rel."""
    dur = float(duration_s if duration_s is not None else shot.get("duration_s", 0.0))
    z0, z1 = float(shot["zoom"][0]), float(shot["zoom"][1])
    if dur <= 0:
        px, py = shot.get("pivot_start", [0.5, 0.5])
        return z0, float(px), float(py)

    t = _clamp(float(t_rel), 0.0, dur)
    progress = smoothstep(t / dur)

    # Base pivot interpolation
    ps = shot.get("pivot_start", [0.5, 0.5])
    pe = shot.get("pivot_end", [0.5, 0.5])
    px = ps[0] + (pe[0] - ps[0]) * progress
    py = ps[1] + (pe[1] - ps[1]) * progress

    # Base zoom
    tin = float(shot.get("punch_in_dur", 0.0)) if shot.get("has_punch_in") else 0.0
    out_len = float(shot.get("punch_out_dur", 0.0)) if shot.get("has_punch_out") else 0.0
    t_out = dur - out_len

    if tin > 1e-6 and t <= tin:
        z_from = z0 * float(shot["punch_in"])
        zoom = z_from + (z0 - z_from) * ease_out_cubic(t / tin)
    elif out_len > 1e-6 and t >= t_out:
        z_to = z1 * float(shot["punch_out"])
        zoom = z1 + (z_to - z1) * ease_in_cubic((t - t_out) / out_len)
    else:
        span = t_out - tin
        if span <= 1e-6:
            zoom = z0
        else:
            zoom = z0 + (z1 - z0) * smoothstep((t - tin) / span)

    return zoom, px, py
