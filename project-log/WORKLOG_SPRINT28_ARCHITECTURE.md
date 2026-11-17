# Worklog Sprint 28 — Stage 2 Architecture (typed providers, ADR-0009, SBOM)

**Started:** 2026-11-17 (after Sprint 27 Stage 1 License Audit completed)

## Goal
Close the roadmap Stage 2 blockers: typed provider interfaces, SBOM, ADR-0009
(License and Compliance).

## Delivered

### 1. Typed provider contracts — `core/providers.py`
- `VoiceProvider`: runtime-checkable Protocol (`provider_id`, `voices(locale)`,
  `synthesize(text=, locale=, voice=, output=) -> Path`).
- `ensure_voice_provider()`: structural validation; `first_video.build()` calls
  it for every adapter, so a non-conforming provider fails before any file is
  written.
- `ProviderSpec` (frozen dataclass) + `SPECS` registry with license metadata:
  - `silero_local`: REVIEW REQUIRED (v5_cis_base_nostress — MIT per LICENSE_CIS
    or CC BY-NC-SA; re-audit exact weights before commercial use)
  - `edge`: BLOCKED (MIT package, but no confirmed Read Aloud commercial grant)
  - `prerecorded`: REVIEW REQUIRED (rights to user recordings are the user's)
- `require_commercial_use()` raises `CommercialUseBlocked`; **no voice provider
  is APPROVED today**, the commercial gate is closed by construction.
- `PreRecordedAudioProvider`: copies user WAV files through the same interface;
  keeps Sprint 26 semantics (missing file -> FileNotFoundError 'Missing audio:
  <path>', traversal/extension -> ValueError, no silent substitution).

### 2. `scripts/first_video.py` unified
- Both narration routes (user WAV dir, local Silero) now go through the
  VoiceProvider contract; CLI options and outputs unchanged.
- One pre-existing Sprint 26 test updated: its injected fake provider lacked
  `provider_id`/`voices` and now satisfies the ADR-0009 contract (test intent
  unchanged: failed runs leave no partial output tree).

### 3. SBOM — `scripts/generate_sbom.py` + `LICENSES/SBOM.cdx.json`
- Deterministic CycloneDX 1.5 BOM built from `DEPENDENCY_LICENSES.csv`
  (library components), `AI_MODELS_AND_SERVICES.csv` (machine-learning-model
  components) and `ASSET_REGISTER.csv` (file components); stdlib only.
- `serialNumber` derived from SHA-256 of the canonical component list; output
  is byte-stable, so `--check` (byte comparison) can gate CI on drift.
- Duplicate bom-refs are rejected; empty spreadsheet rows are skipped.
- Registers stay the single source of truth; hand-editing the SBOM is a defect
  (ADR-0009).

### 4. Documentation
- `docs/ADR-0009-LICENSE-AND-COMPLIANCE.md` — decisions and limits.
- `project-log/DECISIONS.md`, `ROADMAP_STATUS.md` (Stage 2 -> COMPLETED),
  `STATUS.md`, `NEXT_SESSION.md` updated.

## Verification
- `python -m pytest -q tests --basetemp C:\Temp\pytest_ascii` (Windows, .venv
  Python 3.10.11): **374 passed, 19 subtests passed** (was 373+19; +18 Sprint 28
  tests, 1 legacy fake provider updated).
- `python -m unittest discover -s tests -q`: **Ran 368 tests — OK** (exit 0).
- `python scripts/generate_sbom.py` then `--check`: SBOM WRITTEN / SBOM OK.
- No behavior change in the first-video pipeline: existing Sprint 26/26.1
  pipeline tests pass unmodified except the fake-provider contract fix.

## Limits / next
- Image-provider contract intentionally deferred until Stage 5.
- SBOM check is a byte comparison, not a CycloneDX schema validation.
- Stage 3 (RU/UA scenarios) is next: original verified example library.
