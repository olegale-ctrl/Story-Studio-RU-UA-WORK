**Status: EXPERIMENTAL — independent owner review required.** Date2026-11-18. Windows: WINDOWS_NOT_RUN.

# MVP-08A — Independent acceptance candidate

**Final status: READY_FOR_INDEPENDENT_MVP_08A_REVIEW.** Candidate prepared by implementer; independent ChatGPT audit and owner decision still required. Not ACCEPTED or PRODUCTION_READY.

## Git identity and controlled scope

Branch `feat/story-studio-experimental-mvp-08a-asset-library` from exact parent `96fcbe7e48bf5d5a6ba0c50dd6ba9eb21712e520`, tree `5dfe9e27b2c9617c6ee6bf8b841c7498d2aa1098`. Research reference `f4661c86103bbcedf304201202203f20f3bb2747`, read directly, not merged. Final commit/tree are the containing Git commit and external `ACCEPTANCE_PACKET.json`; embedding a document's own commit SHA would be circular. External Git blob/SHA256 manifest and exact diff make the candidate independently checkable.

Implementation changes only inside experimental_mvp/: new asset_library.py, asset_ui.py, test_asset_library.py, test_asset_ui.py; integration changes storyboard.py, timeline.py, ui.py. Reports are the nine Markdown documents linked below. No main/CI/normative PG/G3.2.1/production storage or permissions changes. Existing regression tests are unchanged. No MP4/images/user media added to Git.

## Product result

Local SQLite catalog plus streamed content-addressed original files, independent AssetRecords for shared content, metadata history and separate integrity/rights/lifecycle. Safe local import/probe/decode, deterministic search/pages, known-error recovery without guessed originals, explicit retirement and reference detachment, thumbnails as separate derivatives, exact revision binding and stale result refusal. Existing17fields retained. Current rights/revision/integrity are checked before library-bound preview/use; originals never replaced by metadata edits. Timeline changes retain Undo/Redo; JSON membership is authoritative, DB link observations are historical rather than a live global project index.

Unknown rights stay unknown; CLEARED_FOR_EXPERIMENT is a local review label, not legal authenticity or production permission. Manual import is the local ingress for this stage; no external generation/dispatcher is implemented. The approved automation target and ownerD01–D08 are preserved, not replaced with prior Codex proposals.

## Verification summary

Final combined run: **837passed, 2skipped, 3683subtests passed, exit0**. New51methods:50passed,1Windows skip, targeted unittest exit0. Existing core unittest714methods,1skip, exit0. Real process exits73/74, SQLite commit/initialization rollback,6I/O fault phases and concurrent imports verified. Local GUI widgets and main app screenshot inspected; no callback errors. Exact versions, command scopes, warnings, failed preliminary attempts and logs are documented in test report. Linux performance is measured separately and not labelled Windows performance.

## Independent audit navigation

1. [Owner approval, exact D01–D08](MVP_08_OWNER_APPROVAL.md).
2. [Architecture, SQLite fit, publication/project boundaries](MVP_08A_ARCHITECTURE.md).
3. [AssetRecord/API contract](MVP_08A_ASSET_CONTRACT.md).
4. [Actual test results](MVP_08A_TEST_RESULTS.md).
5. [Fault injection and recovery](MVP_08A_FAULT_INJECTION.md).
6. [Security review](MVP_08A_SECURITY_REVIEW.md).
7. [Performance](MVP_08A_PERFORMANCE.md).
8. [Limitations](MVP_08A_LIMITATIONS.md).
9. This acceptance index.

External packet contains exact full-index diff; Git blob/content SHA256 manifest; code-under-test hashes; test logs/JUnit and real exit codes; fault matrix/scripts; environment/performance JSON; small synthetic assets; GUI screenshot; exact research source snapshots/manifests; final commit/tree and remote verification. Reconstruct candidate tree from the exact base with the exported patch and temporary index; see validation evidence. No hidden git merge is required.

## Open limits / remaining qualification

WINDOWS_NOT_RUN; trusted-user filesystem/SQLite only, residual TOCTOU/reparse/hardlink risks; untrusted-media decoder not OS-sandboxed; metadata rights not authenticated; no power-loss/disk-controller claim; pending metadata may need re-entry; orphan binaries retained (no physical garbage collection); historical DB links need not match every saved/undone JSON; optional bindings aren't automatically portable; minimal JSON metadata UI and no instant import cancellation. See limitations for exact limits. No unresolved critical defect was observed in the stated local process-failure model; this is not a claim against hostile OS/permissions or all media/codecs.

## STOP

No MVP-08B implementation, provider calls, accounts, payments, browser automation, production credential management, main/CI changes, merge, release or production permissions. Hand off for independent ChatGPT audit and owner decision; do not start the next implementation stage automatically.
