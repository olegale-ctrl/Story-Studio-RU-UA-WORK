# Sprint 26 — Windows validation report (2026-11-16)

Validated on the user machine (Windows, `win32`), Python 3.10.11 in `.venv`
(torch 2.14.1+cpu), FFmpeg in `tools/ffmpeg/bin/`.

## Test suite

| Environment | Result |
|---|---|
| `.venv` (Python 3.10.11) | **116 tests, OK** |
| system Python 3.15.0b1 | 116 tests, OK |

Two pre-existing test defects were fixed during this validation:

1. `tests/test_sprint20.py` imported `pytest`, so `python -m unittest discover -s tests`
   failed to collect it on a machine without pytest. Rewritten as a plain
   `unittest.TestCase`; pytest still collects it unchanged.
2. `tests/test_sprint23_2.py::test_env_override` asserted a POSIX path string
   against a `list` argument (`assertIn` checks element equality, not substring)
   and was platform-dependent. Now compares the `--model-path` argument with
   normalised separators.

## Real end-to-end runs

### Ukrainian, local Silero (`ukr_igor`)

```
.\.venv\Scripts\python.exe .\scripts\first_video.py `
  --plan .\examples\first_video_plan_uk.json `
  --silero-model C:\StoryStudioModels\v5_cis_base_nostress.pt `
  --voice ukr_igor --output-dir .\output\first-video-uk
```

- RENDER: duration 14520 ms, 3 image clips, burned subtitles, CRF 22, 1280x720
- `ffprobe`: h264 (High) 1280x720 @ 25 fps + AAC 48000 Hz stereo, 14.52 s
- `ffmpeg volumedetect`: mean -27.5 dB, max -8.5 dB — speech present, not silence
- `python -m core.cli check project.json` → `OK: schema v3, locale=uk, clips=6`

### Russian, local Silero (`ru_igor`)

- RENDER: duration 13280 ms, 3 image clips, burned subtitles
- `core.cli check` → `OK: schema v3, locale=ru, clips=6`

### Existing WAV + user images

`--audio-dir` with three WAV files and `--images-dir` with three JPGs produced a
valid 14.52 s MP4. The 4:3 source images were correctly pillarboxed into the
16:9 frame by the renderer's `scale=...:force_original_aspect_ratio=decrease,pad`
rule.

## Subtitle timing verification

Frame sampling with FFmpeg and pixel counting in the bottom 20 % of the frame
confirms the burned captions match the project timeline exactly:

| Subtitle | Expected window (ms) | Sampled times | Bright pixels |
|---|---|---|---|
| s1 | 0 – 4725 | 0.5, 2.0, 4.0 | 6280 (constant) |
| s2 | 5160 – 10198 | 6.0, 7.5, 9.0 | 6694 (constant) |
| s3 | 10600 – 14088 | 11.0, 13.0 | 5648 (constant) |
| — | after 14088 | 14.2 | 0 |

Constant pixel counts inside a window and different counts between windows mean
three distinct captions appear exactly at their planned times and disappear
after the last scene.

Visual check of extracted frames: white text, thin dark outline, `Shadow=0`,
no shadow, no filename overlay, correct aspect ratio.

## Defect found and fixed

**Partial output directory left behind on runtime failure.**
`build()` created `--output-dir` and its `media/` subfolder before synthesis
started. When synthesis failed (for example an unsupported voice), the script
exited with an error but left the half-written tree in place. A retry with the
same `--output-dir` then failed with `Output directory already exists`, forcing
the user to delete the folder by hand.

Fix: `scripts/first_video.py` now runs the build inside `try/except BaseException`
and removes the output tree with `shutil.rmtree(..., ignore_errors=True)` before
re-raising. Regression test `test_failed_run_leaves_no_output_directory` in
`tests/test_sprint26.py` covers it.

## Error handling checks

| Case | Behaviour |
|---|---|
| `--output-dir` already exists | `ERROR: Output directory already exists: ...`, exit 2 |
| both `--audio-dir` and `--silero-model` | argparse: `not allowed with argument` |
| neither audio source | argparse: `one of the arguments ... is required` |
| unsupported voice | `ERROR: Unsupported voice 'bad_voice' for locale 'uk'` |
| missing `voiceN.wav` | `FileNotFoundError: Missing audio: ...` |
| image path traversal | `ValueError: Image must be a simple filename, not a path` |

## Still outstanding

- **Playback was not audited by ear.** Loudness and speech presence were measured
  programmatically; intelligibility, pronunciation quality and speaker
  consistency still need a human listening check in VLC.
- Subtitle timing is scene-level, not word-level forced alignment.
- Vertical 1080x1920 output was not exercised in this run.
- `python -m pytest -q tests` was not executed (pytest is not installed in the
  local venv); the CI workflow installs it explicitly and remains the pytest gate.

## Result

The Sprint 26 first-video pipeline is **verified on Windows** for Ukrainian and
Russian narration with local Silero, for user-supplied WAV files and images,
including burned subtitles with correct timing and clean error handling.
