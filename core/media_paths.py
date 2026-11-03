"""Portable relative media path validation."""
from pathlib import PurePosixPath
import re
_DRIVE = re.compile(r'^[A-Za-z]:')


def validate_media_path(path: str) -> str:
    if not isinstance(path, str) or not path.strip() or '\x00' in path:
        raise ValueError('media path must be nonempty text without NUL')
    normalized = path.replace('\\', '/')
    if normalized.startswith(('/', '//')) or _DRIVE.match(normalized):
        raise ValueError('absolute media paths are not portable')
    segments = normalized.split('/')
    if any(part in ('', '.', '..') for part in segments):
        raise ValueError('media path contains empty, dot or traversal segment')
    if ':' in normalized or '?' in normalized or '#' in normalized:
        raise ValueError('media path contains unsupported characters')
    return str(PurePosixPath(normalized))


