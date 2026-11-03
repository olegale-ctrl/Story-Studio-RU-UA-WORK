"""SHA-256 manifest and integrity verification for portable bundles (stdlib only)."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
from core.media_paths import validate_media_path

def _hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def make_integrity_manifest(bundle_root: str | Path) -> dict:
    root = Path(bundle_root).resolve(strict=True)
    entries = []
    for file in sorted(root.rglob('*')):
        if not file.is_file():
            continue
        if file.is_symlink() or root not in file.resolve().parents:
            raise ValueError('unsafe bundle file')
        relative = file.relative_to(root).as_posix()
        if relative == 'integrity.json':
            continue
        validate_media_path(relative)
        entries.append({'path': relative, 'bytes': file.stat().st_size, 'sha256': _hash_file(file)})
    return {'algorithm': 'sha256', 'files': entries}

def verify_bundle(bundle_root: str | Path) -> list[str]:
    root = Path(bundle_root).resolve(strict=True)
    manifest = json.loads((root / 'integrity.json').read_text(encoding='utf-8'))
    if manifest.get('algorithm') != 'sha256' or not isinstance(manifest.get('files'), list):
        raise ValueError('unsupported integrity manifest')
    errors = []
    seen = set()
    for entry in manifest['files']:
        if not isinstance(entry, dict) or set(entry) != {'path', 'bytes', 'sha256'}:
            raise ValueError('invalid integrity entry')
        rel = validate_media_path(entry['path'])
        if rel in seen:
            raise ValueError('duplicate integrity path')
        seen.add(rel)
        target = (root / rel).resolve()
        if root not in target.parents or not target.is_file():
            errors.append(f'missing/unsafe: {rel}')
        elif target.stat().st_size != entry['bytes'] or _hash_file(target) != entry['sha256']:
            errors.append(f'checksum mismatch: {rel}')
    actual = {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.name != 'integrity.json'}
    for rel in sorted(actual - seen):
        errors.append(f'unlisted file: {rel}')
    return errors
