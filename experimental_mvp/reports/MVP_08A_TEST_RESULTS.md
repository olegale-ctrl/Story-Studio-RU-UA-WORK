**Status: EXPERIMENTAL — independent owner review required.** Date2026-11-18. Windows: WINDOWS_NOT_RUN.

# MVP-08A — Test results

## Exact environment and scopes

Python 3.12.14 (main, Aug 25 2026, 14:00:49) [Clang 22.1.3 ]; SQLite3.53.1; Tk9.0.4; pytest9.2.0; FFmpeg/FFprobe7.1.5-0+deb13u1; Linux6.18.57/glibc2.41;3logical CPUs; Xvfb:91. No Windows host, native Windows dialogs or NTFS qualification. No provider requests/payments/production permissions.

Source snapshot `code-under-test.json` contains SHA256 of all seven changed/new Python files before the final combined run. Those exact bytes were rechecked after tests. Documentation edits afterward do not change implementation. Exact final Git identity and all changed-file hashes are in external acceptance manifest, avoiding a self-referential commit hash in this document.

| Run / real command | Actual result | Exit code / evidence |
|---|---|---|
|`python -m pytest -q tests experimental_mvp -o faulthandler_timeout=90 --junitxml=...`|837passed, 2skipped, 3683subtests passed;1external-plugin warning|0; full-explicit.log/xml/result.json; 230.654s|
|`python -m unittest experimental_mvp.test_asset_library experimental_mvp.test_asset_ui -v`|51new test methods:50passed,1Windows skip|0; asset-final.log/result.json|
|`python -m unittest discover -s tests -v`|714methods,713passed,1Windows skip|0; core-unittest.log, test-runs.json|
|Initial default `python -m pytest -q`|726passed,1skipped,3614subtests; this config selects tests/ ONLY, **not the full experimental suite**|0; full-pytest.log/xml (filename retained; scope corrected here)|
|Actual main GUI harness|8tabs, Asset Library import/search/review/thumbnail; no callback errors|0; gui-smoke.json/log/png|
|Detailed fault probe|6injected ENOSPC exceptions + real exit73/74; recovery/retry pass|Probe0, intentional children73/74; fault-matrix.json/log|
|Performance harness|9local operations,30records|0; performance.json/log|

51new methods are in test_asset_library.py and test_asset_ui.py. Parameterized subtest assertions are reported separately; do not count subtests as additional independent test methods. Legacy experimental suites (MVP05/06/07/07.1) are included unchanged in the combined run. One warning is PytestRemovedIn10Warning from installed anyio plugin, not a library failure. No passed claim is made for skipped Windows cases.

## Required groups

| Group | Linux result / oracles |
|---|---|
|A Basic import|PASS: valid PNG and MP4, invalid image/video, empty/oversized/unsupported, Unicode/spaces; actual FFprobe/full video decode|
|B Integrity/dedup|PASS: SHA, changed/missing/corrupted objects, same bytes with different provenance/rights, source hash invariant|
|C Atomicity/recovery|PASS: staging/publication/commit faults, real child exit, schema initialization rollback, repeated recovery, concurrent import, no orphan ACTIVE records|
|D Security|PASS within tested local model: traversal/symlink/TOCTOU/metadata limits/invalid tool output/real process timeout. Windows junction **NOT_RUN**|
|E VideoAnchor|PASS: attach/detach, explicit replacement/restoration, stale/deleted/edited anchor, bad rights/technical status, duplicate refusal, retired during attach|
|F Timeline|PASS: actual bound-video preview, missing/corrupt/revoked/revised assets refused, Undo/Redo, stale snapshot, no silent replacement or original mutation|
|G Regression|PASS in combined run: existing conflict drafts, atomic save, cancellation/cleanup, LOOP timing, rendering, captions and Timeline history|
|UI|PASS: real Tk widgets with mocked dialog choices; worker-thread import, GUI-thread apply, metadata review, image poster, attach/detach/retire, stale result and closed panel safety|

## Honest failure history

Preliminary smoke script lacked PYTHONPATH (ModuleNotFoundError, exit1). Initial new unittest had one erroneous tuple assertion for preview's Path return; log retained, test corrected. Two combined new-GUI runs hit native SIGILL during worker garbage collection of prior Tcl resources; implementation corrected as documented in security review. Those shell compound calls ended with `tail`, masking Python's process exit code; evidence records the SIGILL rather than inventing a captured numeric code. Later isolated/combined GUI and final full runs passed. Several successful prefinal combined runs are preserved with prefixes; acceptance numbers above refer only to final run on the source snapshot.

## Not executed / not asserted

Windows10/11, NTFS/reparse/ACL behavior, native PowerShell installation, other Python versions, malicious decoder sandbox qualification, real account/provider model output, payments, external API quota/download/refund, production release, human listening/visual quality or scientific editorial acceptance. The synthetic MP4 mechanically exercises media ingest/preview; it is not production material approval.
