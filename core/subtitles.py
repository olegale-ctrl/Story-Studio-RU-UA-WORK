"""Editor-independent SRT export; no external packages or editor promises."""
from __future__ import annotations
from .project_schema import Project


def _timestamp(ms: int) -> str:
    hours, rest = divmod(ms, 3_600_000)
    minutes, rest = divmod(rest, 60_000)
    seconds, milliseconds = divmod(rest, 1000)
    return f'{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}'


def export_srt(project: Project, *, track_id: str) -> str:
    project.validate()
    if not isinstance(track_id, str) or not any(t.id == track_id and t.kind == 'subtitle' for t in project.tracks):
        raise ValueError('unknown subtitle track')
    subs = sorted((s for s in project.subtitles if s.track_id == track_id), key=lambda s: (s.start_ms, s.id))
    blocks = []
    for i, sub in enumerate(subs, 1):
        text = sub.text.replace('\r\n', '\n').replace('\r', '\n').strip()
        blocks.append(f'{i}\n{_timestamp(sub.start_ms)} --> {_timestamp(sub.start_ms + sub.duration_ms)}\n{text}')
    return '\n\n'.join(blocks) + ('\n' if blocks else '')
