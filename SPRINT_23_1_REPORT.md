# Sprint 23.1 — Windows Cyrillic path fix

- Root cause confirmed by user: original model exists, but `torch.package.PackageImporter` fails to open a Cyrillic path; an ASCII path works.
- Changed full file `integrations/silero_local.py` to use an automatically cleaned-up temporary ASCII-only model copy on Windows.
- Existing trust opt-in and SHA256 verification remain enforced; copied model is also SHA256-checked.
- Added `tests/test_sprint23_1.py` (3 tests: 2 passed on Linux; Windows-only integration test skipped). Windows runtime audio test remains pending.
- No model weights or dependencies included.
