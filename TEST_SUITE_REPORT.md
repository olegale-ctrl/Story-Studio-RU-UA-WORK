# Test suite expansion report (2026-11-16)

## Result

| Metric | Before | After |
|---|---|---|
| Automated tests (unittest) | 116 | **346** |
| Automated tests (pytest) | 119 | **352** (+19 subtests) |
| `core/` coverage per module | 83–100 % | **91–100 %** |
| `scripts/first_video.py` | 69 % | **96 %** |
| `scripts/voice_settings.py` | 0 % | **97 %** |
| `core/hardware_profile.py` | 54 % | **98 %** |
| `scripts/studio_runtime.py` | 0 % | **87 %** |
| `core/project_schema.py` | 92 % | **96 %** |
| `scripts/silero_studio_preview.py` | 0 % | **96 %** |

All tests pass on Windows in `.venv` (Python 3.10.11) and in system Python
3.15.0b1. Suite runtime is under 7 seconds.

## New test files

| File | Tests | Subject |
|---|---|---|
| `tests/test_core_validation.py` | 44 | Schema guard rails, bundle integrity, CLI branches, renderer rejection paths |
| `tests/test_voice_settings.py` | 32 | Voice profile validation, DPAPI credential round-trip, CLI exit codes |
| `tests/test_studio_runtime.py` | 29 | Runtime config, tool paths, Jianying draft discovery, skill lookup |
| `tests/test_first_video_pipeline.py` | 28 | Sprint 26 pipeline: user images, render step, cleanup on failure |
| `tests/test_hardware_and_silero.py` | 27 | Hardware probe failure modes, Silero model-provenance guards |
| `tests/test_edge_voice_demo.py` | 26 | Voice resolution, cache contract, fallback recording, output versioning |
| `tests/test_narrated_demo_pipeline.py` | 20 | Demo builder and the inspector quality gate |
| `tests/test_voice_studio_helpers.py` | 18 | Preview path calculation, file signatures, synthesis metrics |
| `tests/test_silero_studio_preview.py` | 6 | GUI→CLI bridge, trust gate, absolute preview path |

## Defect found and fixed

**`Project.to_dict()` was not accepted by `Project.from_dict()`.**

`to_dict()` returned the raw `dataclasses.asdict()` output, where the five
collection fields stay tuples, while `from_dict()` requires JSON arrays:

```python
>>> Project.from_dict(project.to_dict())
ValueError: scenes must be a list
```

`to_json()` / `from_json()` were never affected, so no shipped artefact was
broken, but the public serialisation API was asymmetric: anyone building a
project programmatically and passing it to `from_dict()` hit the error.

Fix: `to_dict()` now converts `scenes`, `tracks`, `subtitles`, `media` and
`clips` to lists, matching the on-disk format exactly. Regression test
`test_to_dict_roundtrip_is_lossless` in `tests/test_core_validation.py`.

The real pipeline was re-run end to end after the change: identical output
(14.52 s, h264 1280×720, AAC 48 kHz stereo), `core.cli check` → `OK`.

## CI changes

`.github/workflows/tests.yml` gained a `windows-2022` job running the same suite
on Windows 11 across Python 3.10 and 3.13. The Linux job cannot observe Windows
path handling, console encoding or subprocess differences — the Sprint 25.1
Unicode preview bug and the `test_env_override` platform dependence were both
Windows-specific and would not have been caught by the existing matrix.

## Windows-specific note for pytest

pytest derives its temporary directory from `%TEMP%`, which contains the user
profile name. With a non-ASCII profile name the resulting path cannot be
scanned and every test using the `tmp_path` fixture fails with
`PermissionError: [WinError 5]`. This is a pytest/tempdir issue, not a project
defect.

Workaround, documented in `pytest.ini`:

```powershell
python -m pytest -q tests --basetemp C:\Temp\pytest_ascii
```

The standard library runner is unaffected:

```powershell
python -m unittest discover -s tests -v
```

The CI Windows job passes `--basetemp ${{ runner.temp }}\pytest-ascii`.

## Deliberately not covered

- `scripts/voice_studio.py` (30 %) — the Tkinter GUI cannot be driven headless.
  All pure helpers around it are covered separately.
- `integrations/silero_local.py` (56 %) — the uncovered part is the real-model
  synthesis path, which needs the trusted `.pt` file. The provenance, trust and
  path guards around it are covered.
- `scripts/doubao_tts.py`, `setup_dependencies.py`, `bootstrap_environment.py`,
  `check_handoff.py`, `silero_preview*.py` and their `scripts/test_*.py` files
  (0 %) — these are the upstream Chinese modules and their upstream tests. They
  are deliberately left uncovered until the licensing audit of roadmap stage 1
  decides whether they stay, are replaced, or are removed. Writing tests for
  them now would effectively promote code whose distribution rights are
  unresolved.
