"""E01.3.6.1 canonical checksum of the complete editorial snapshot."""
import hashlib
import json

from . import model as m
from .codec import encode_snapshot

__all__ = (
    'SnapshotChecksumError',
    'canonical_snapshot_bytes',
    'compute_snapshot_checksum',
    'verify_snapshot_checksum',
)


class SnapshotChecksumError(m.ModelError):
    """The stored snapshot checksum does not match the canonical envelope."""


def canonical_snapshot_bytes(snapshot: m.ContractSnapshot) -> bytes:
    """Return canonical wire bytes with only root snapshot_checksum omitted."""
    encoded = encode_snapshot(snapshot)
    payload = json.loads(encoded.decode('utf-8'))
    del payload['snapshot_checksum']
    return json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(',', ':'),
        allow_nan=False,
    ).encode('utf-8')


def compute_snapshot_checksum(snapshot: m.ContractSnapshot) -> str:
    """Return lowercase SHA-256 for the canonical snapshot payload."""
    return hashlib.sha256(canonical_snapshot_bytes(snapshot)).hexdigest()


def verify_snapshot_checksum(snapshot: m.ContractSnapshot) -> None:
    """Raise a structured error unless the stored checksum is exact."""
    computed = compute_snapshot_checksum(snapshot)
    if snapshot.snapshot_checksum != computed:
        raise SnapshotChecksumError(m.Violation(
            'SNAPSHOT_CHECKSUM_MISMATCH',
            '$.snapshot_checksum',
            'Stored snapshot_checksum does not match the canonical snapshot payload',
        ))
