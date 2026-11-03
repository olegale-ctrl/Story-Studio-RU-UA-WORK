# Sprint 25.1 — Unicode-safe Voice Studio preview and GitHub source baseline

Date: 2026-11-03

## Completed
- Full upstream original: pinned Git submodule in the private project repository, isolated from working RU/UA runtime; 40 original engineering files preserved verbatim under a separate path.
- RU/UA Sprint 25 baseline: 148 text project files imported to GitHub.
- Voice Studio no longer parses child stdout to discover the preview path. The application derives the expected Silero WAV or Edge MP3 output path from language, voice, text and settings, which works with Cyrillic Windows profile names even if console output is corrupted.
- Subprocesses explicitly request UTF-8 I/O; completed Silero previews are checked for a new file and sufficient size; existing Edge MP3 cache remains supported.
- Synthesis time, audio duration (for WAV) and real-time factor are displayed in the GUI and log.
- Portable tests generate their own temporary PPM images and WAV, so large demo assets are no longer required in source control.
- The obsolete Sprint 23.1 temp-model-copy tests were corrected to match later Sprint 23.2 path policy, without adding unexpected model copies.

## Validation
- `python -m compileall`: passed.
- `python -m unittest discover -s tests -v`: **106 tests OK, 0 errors/failures, Linux Python 3.13**.
- Windows 10/11 GUI + actual Silero model: **NOT TESTED in this environment**, must be confirmed by the user.

## Licensing
- The current pinned original is under CC BY-NC-SA 4.0. Historical local archive carried an MIT copy; source provenance and commercial rights unresolved. Separate original and RU/UA code; no commercial distribution clearance implied.

## Next
- Windows validate Silero/Edge Voice Studio and synthesis metrics; next Sprint 26 should review reuse of original editing/audio-alignment/rendering technology with license and integration gates.
