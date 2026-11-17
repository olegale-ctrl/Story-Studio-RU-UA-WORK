# ADR-0009 — License and Compliance as part of the architecture

Status: IMPLEMENTED (Sprint 28, Stage 2 «Архитектура»).

Date: 2026-11-17

## Context

Sprint 27 (Stage 1) produced the audited registers: `DEPENDENCY_LICENSES.csv`,
`AI_MODELS_AND_SERVICES.csv`, `ASSET_REGISTER.csv`, `THIRD_PARTY_NOTICES.md`.
Until Sprint 28 the license status of a TTS route lived only in documents, so
code could silently pick a provider whose terms were never cleared. The
roadmap also required an SBOM and typed provider contracts before Community 1.0.

## Decisions

1. **Typed provider contract.** Every narration route implements the
   `VoiceProvider` contract in `core/providers.py`: `provider_id`,
   `voices(locale)` and `synthesize(text=, locale=, voice=, output=) -> Path`.
   `first_video.py` validates every adapter with `ensure_voice_provider()`
   before rendering; the two existing routes (`silero_local`, prerecorded WAV)
   already satisfy it structurally — no adapter code changed behaviour.
2. **License metadata is part of the contract.** `ProviderSpec` records the
   commercial state (`APPROVED` / `REVIEW REQUIRED` / `BLOCKED`), data handling
   and status per provider in the `SPECS` registry. The registry mirrors
   `AI_MODELS_AND_SERVICES.csv`; when a register row changes, the code row
   changes in the same commit.
3. **Commercial gate in code, not only in docs.** `require_commercial_use()`
   raises `CommercialUseBlocked` for any provider that is not `APPROVED`.
   Commercial builds must call it; no voice provider is `APPROVED` today, so
   nothing may be commercialized on the current provider set.
4. **No silent voice substitution.** The prerecorded route copies the exact
   user file and fails loudly when it is missing — the same behaviour Sprint 26
   validated, now expressed as a provider (`PreRecordedAudioProvider`).
5. **SBOM from the registers.** `scripts/generate_sbom.py` builds a
   deterministic CycloneDX 1.5 SBOM (`LICENSES/SBOM.cdx.json`) from the three
   Stage 1 CSVs with stdlib only. `--check` compares bytes, so CI can fail when
   the SBOM and the registers drift apart.
6. **Registers remain the single source of truth.** The SBOM is a generated
   view; hand-editing `SBOM.cdx.json` is a defect, not a change.

## Consequences and limits

- Adding a provider means: adapter + `ProviderSpec` row + register row + tests;
  a provider without license metadata cannot be constructed through the gate.
- The SBOM covers Python dependencies, AI models/services and registered
  media assets. FFmpeg and the user-supplied Silero weights stay USER
  RESPONSIBLE (not bundled, not redistributed) and appear as properties, not
  as redistributed components.
- `check_sbom()` is a byte comparison, not a CycloneDX schema validation;
  structure is enforced by the tests instead.
- Commercial clearance still requires the human review documented in
  `COMMERCIAL_VOICE_LICENSE_GATE.md` and `LICENSES/UNRESOLVED_ITEMS.md`; the
  code gate is a guard rail, not a substitute for the audit.
