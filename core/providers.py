"""Typed voice-provider contracts and the license registry (ADR-0009).

Every narration route in the project speaks through one small interface:
`voices(locale)` plus `synthesize(text=..., locale=..., voice=..., output=...)`.
Three routes exist today:

- silero_local  local PyTorch Silero, noncommercial until weights are re-audited
- edge          experimental online Edge TTS, COMMERCIAL BLOCKED
- prerecorded   user-supplied WAV files, rights stay with the user

License metadata travels with the contract: `require_commercial_use()` reads
the registry, so a commercial build cannot silently pick a provider whose
terms were never cleared. Adapters stay where they belong (integrations/),
this module only defines the contract, the metadata and one local adapter.
"""
from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, runtime_checkable

APPROVED = 'APPROVED'
REVIEW_REQUIRED = 'REVIEW REQUIRED'
BLOCKED = 'BLOCKED'
_COMMERCIAL_STATES = (APPROVED, REVIEW_REQUIRED, BLOCKED)


class CommercialUseBlocked(PermissionError):
    """Raised when a provider is not approved for commercial distribution."""


@dataclass(frozen=True)
class ProviderSpec:
    """License and data-handling metadata for one voice provider."""

    provider_id: str
    title: str
    kind: str  # 'local' | 'online' | 'prerecorded'
    commercial_use: str
    data_handling: str
    status: str

    def validate(self) -> None:
        if not isinstance(self.provider_id, str) or not self.provider_id.strip():
            raise ValueError('invalid provider id')
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError('invalid provider title')
        if self.kind not in ('local', 'online', 'prerecorded'):
            raise ValueError('unsupported provider kind: ' + str(self.kind))
        if self.commercial_use not in _COMMERCIAL_STATES:
            raise ValueError('unsupported commercial_use value: ' + str(self.commercial_use))
        if not isinstance(self.data_handling, str) or not self.data_handling.strip():
            raise ValueError('invalid data_handling')
        if not isinstance(self.status, str) or not self.status.strip():
            raise ValueError('invalid status')


SPECS: dict[str, ProviderSpec] = {}
for _spec in (
    ProviderSpec(
        provider_id='silero_local',
        title='Silero TTS (local PyTorch)',
        kind='local',
        commercial_use=REVIEW_REQUIRED,
        data_handling='Local inference only; no data leaves the machine',
        status='REVIEW REQUIRED — v5_cis_base_nostress may be MIT (LICENSE_CIS) or '
               'CC BY-NC-SA; re-audit the exact weights before commercial use. '
               'Weights are never bundled; user loads .pt with trusted=True and SHA256 check.',
    ),
    ProviderSpec(
        provider_id='edge',
        title='Edge TTS (online)',
        kind='online',
        commercial_use=BLOCKED,
        data_handling='Text is sent to a Microsoft cloud endpoint',
        status='COMMERCIAL BLOCKED — package is MIT but the Read Aloud service grant is '
               'not confirmed; experimental personal prototype only',
    ),
    ProviderSpec(
        provider_id='prerecorded',
        title='Pre-recorded WAV files',
        kind='prerecorded',
        commercial_use=REVIEW_REQUIRED,
        data_handling='Local file copy only',
        status='USER CLEARANCE REQUIRED — rights to the recordings are the user\'s responsibility',
    ),
):
    _spec.validate()
    SPECS[_spec.provider_id] = _spec


def get_spec(provider_id: str) -> ProviderSpec:
    """Return the license metadata for a known provider id."""
    try:
        return SPECS[provider_id]
    except (KeyError, TypeError):
        raise ValueError(
            'Unknown voice provider: ' + str(provider_id)
            + '; known: ' + ', '.join(sorted(SPECS))) from None


def commercial_use_allowed(provider_id: str) -> bool:
    return get_spec(provider_id).commercial_use == APPROVED


def require_commercial_use(provider_id: str) -> None:
    """Gate for commercial builds: raise unless the provider is APPROVED."""
    spec = get_spec(provider_id)
    if spec.commercial_use != APPROVED:
        raise CommercialUseBlocked(
            'Commercial use of ' + repr(provider_id) + ' is not approved ('
            + spec.commercial_use + '). See COMMERCIAL_VOICE_LICENSE_GATE.md'
            ' and LICENSES/UNRESOLVED_ITEMS.md')


@runtime_checkable
class VoiceProvider(Protocol):
    """Structural contract every narration adapter must satisfy."""

    provider_id: str

    def voices(self, locale: str) -> tuple[str, ...]:
        """Speakers available for the locale, empty tuple if none."""
        ...

    def synthesize(self, *, text: str, locale: str, voice: str,
                   output: str | Path) -> Path:
        """Produce a WAV file at `output`; return the written path."""
        ...


def ensure_voice_provider(provider: object) -> None:
    """Fail early when an adapter does not satisfy the VoiceProvider contract."""
    if not isinstance(provider, VoiceProvider):
        raise TypeError(
            'Provider does not satisfy the VoiceProvider contract (needs '
            'provider_id, voices(locale) and synthesize(text=, locale=, voice=, output=)): '
            + type(provider).__name__)


def _safe_source_file(source_dir: Path, filename: str) -> Path:
    name = Path(filename)
    if name.is_absolute() or name.name != filename or filename in ('.', '..'):
        raise ValueError('Audio source must be a simple filename, not a path')
    if name.suffix.lower() != '.wav':
        raise ValueError('Audio source must be a WAV file')
    path = source_dir / filename
    if not path.is_file():
        raise FileNotFoundError('Missing audio: ' + str(path))
    return path


class PreRecordedAudioProvider:
    """Narration from user-supplied WAV files (voice1.wav, voice2.wav, ...).

    Nothing is synthesized: the requested file is copied from the source
    directory. A missing file fails loudly instead of being replaced with a
    different voice, matching the Sprint 26 first-video route exactly.
    """

    provider_id = 'prerecorded'

    def __init__(self, source_dir: str | Path):
        self.source_dir = Path(source_dir)
        if not self.source_dir.is_dir():
            raise FileNotFoundError('Audio directory missing: ' + str(self.source_dir))

    def voices(self, locale: str) -> tuple[str, ...]:
        return ()

    def synthesize(self, *, text: str, locale: str, voice: str,
                   output: str | Path) -> Path:
        source = _safe_source_file(self.source_dir, voice)
        target = Path(output)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        return target
