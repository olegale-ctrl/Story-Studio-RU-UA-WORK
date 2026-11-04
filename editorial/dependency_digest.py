"""E01.3.5.2 canonical dependency digest for verified historical packages."""
import hashlib
import json

from . import model as m
from .package import build_historical_package

__all__ = (
    'DependencyDigestError', 'canonical_dependency_bytes', 'compute_dependency_digest',
)

DEPENDENCY_DIGEST_SCHEMA_VERSION = 1


class DependencyDigestError(m.ModelError):
    """Invalid digest-specific input or canonical serialization failure."""


def _fail(path, code, message, ref=None):
    raise DependencyDigestError(m.Violation(code, path, message, ref))


def _wire_ref(ref):
    return {'kind': ref.kind.value, 'id': ref.id, 'revision': ref.revision,
            'content_hash': ref.content_hash}


def canonical_dependency_bytes(snapshot: m.ContractSnapshot, gate,
                               target_ref: m.RevisionRef,
                               policy_version: str) -> bytes:
    """Build a verified historical package and return its canonical bytes.

    PackageValidationError intentionally propagates unchanged. No caller can
    provide a preassembled HistoricalPackage and bypass its integrity checks.
    """
    if type(policy_version) is not str or not policy_version.strip():
        _fail('$.policy_version', 'POLICY_VERSION',
              'policy_version must be a nonempty string and is preserved literally')
    package = build_historical_package(snapshot, gate, target_ref)
    payload = {
        'dependency_digest_schema_version': DEPENDENCY_DIGEST_SCHEMA_VERSION,
        'gate': package.gate.value,
        'policy_version': policy_version,
        'target_ref': _wire_ref(package.target_ref),
        'production_refs': [_wire_ref(ref) for ref in package.production_refs],
        'profile_refs': [_wire_ref(ref) for ref in package.profile_refs],
        'dependencies': [_wire_ref(ref) for ref in package.dependencies],
    }
    try:
        return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(',', ':'),
                          allow_nan=False).encode('utf-8')
    except (TypeError, ValueError, UnicodeEncodeError) as error:
        _fail('$', 'CANONICAL_JSON', f'Cannot encode canonical dependency payload: {error}',
              package.target_ref)


def compute_dependency_digest(snapshot: m.ContractSnapshot, gate,
                              target_ref: m.RevisionRef,
                              policy_version: str) -> str:
    """Return lowercase SHA-256 of canonical_dependency_bytes."""
    return hashlib.sha256(
        canonical_dependency_bytes(snapshot, gate, target_ref, policy_version)
    ).hexdigest()
