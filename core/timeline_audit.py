"""Non-mutating timeline diagnostics; overlapping video/audio clips are allowed."""
from core.project_schema import Project

def audit_timeline(project: Project) -> list[dict]:
    project.validate()
    issues = []
    by_track = {}
    for clip in project.clips:
        by_track.setdefault(clip.track_id, []).append(clip)
    for track_id, clips in sorted(by_track.items()):
        ordered = sorted(clips, key=lambda c: (c.start_ms, c.id))
        for a, b in zip(ordered, ordered[1:]):
            if a.start_ms + a.duration_ms > b.start_ms:
                issues.append({"code": "CLIP_OVERLAP", "track_id": track_id, "clip_ids": [a.id, b.id], "severity": "warning"})
    for clip in project.clips:
        if clip.source_in_ms > 0:
            issues.append({"code": "SOURCE_OFFSET_UNVERIFIED", "clip_id": clip.id, "severity": "info"})
    return issues
