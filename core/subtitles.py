"""Editor-independent SRT export and dynamic subtitle chunking for Story Studio RU/UA."""
from __future__ import annotations
import re
from typing import Any, Dict, List
from .project_schema import Project

VOWELS = set('аеєиіїоуюяёыэАЕЄИІЇОУЮЯЁЫЭaeiouyAEIOUY')


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


def chunk_scene_subtitles(
    text: str,
    start_ms: int,
    duration_ms: int,
    max_words: int = 3,
    frame_ms: int = 40,
) -> List[Dict[str, Any]]:
    """Split a scene text into short, natural phrase chunks with proportional syllable timing."""
    raw_words = text.strip().split()
    if not raw_words:
        return []

    chunks: List[str] = []
    current: List[str] = []
    for w in raw_words:
        current.append(w)
        ends_clause = any(w.endswith(p) for p in (',', '.', '!', '?', ';', ':', '—', '…', '-'))
        if len(current) >= max_words or (len(current) >= 2 and ends_clause):
            chunks.append(' '.join(current))
            current = []

    if current:
        if chunks and len(current) == 1:
            chunks[-1] += ' ' + current[0]
        else:
            chunks.append(' '.join(current))

    # Weight each chunk by vowel/syllable count
    weights = [max(1, sum(1 for c in ch if c in VOWELS)) for ch in chunks]
    total_w = sum(weights)

    subtitles: List[Dict[str, Any]] = []
    curr_start = start_ms
    for i, (chunk_text, weight) in enumerate(zip(chunks, weights)):
        if i == len(chunks) - 1:
            dur = (start_ms + duration_ms) - curr_start
        else:
            dur = int(round(duration_ms * (weight / total_w)))
            if frame_ms > 0:
                dur = max(frame_ms, (dur // frame_ms) * frame_ms)
        subtitles.append({
            'text': chunk_text,
            'start_ms': curr_start,
            'duration_ms': max(frame_ms, dur),
        })
        curr_start += dur

    return subtitles


def get_subtitle_style(width: int, height: int) -> str:
    """Generate modern, high-visibility ASS subtitle style for horizontal or vertical video."""
    is_vertical = height > width
    if is_vertical:
        # Vertical Shorts/Reels/TikTok: larger font, lifted from bottom UI buttons
        font_size = max(24, int(height * 0.024))
        margin_v = max(120, int(height * 0.12))
        outline = 2.5
    else:
        # Horizontal 16:9: cinema bottom third
        font_size = max(20, int(height * 0.032))
        margin_v = max(40, int(height * 0.055))
        outline = 2.0

    return (
        f'FontName=Arial,FontSize={font_size},Bold=1,'
        'PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,'
        f'BorderStyle=1,Outline={outline},Shadow=1,Alignment=2,MarginV={margin_v}'
    )
