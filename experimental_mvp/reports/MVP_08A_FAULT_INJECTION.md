# MVP-08A — Fault injection and recovery evidence

**Status: EXPERIMENTAL — independent review required.** Date2026-11-18. Windows/NTFS: WINDOWS_NOT_RUN. All sources are synthetic local fixtures; no API/storage service involved.

## Executed failure model

`test_asset_library.py` exercises before/after publication, staging corruption, source substitution, read errors, SQLite rollback and actual child termination. External `fault_matrix.py` independently records8 detailed scenarios into `fault-matrix.json/log`: six injected ENOSPC exceptions and two actual process exits. Injected ENOSPC simulates an I/O failure; it does **not** claim the filesystem was physically filled. Child termination tests exercise real SQLite rollback-journal recovery after `os._exit`, not just a mocked exception.

| Failure / oracle | Execution evidence | Required observed outcome |
|---|---|---|
| Source read failure | patch os.open for source only | Exception, no new catalog record, source retained |
| Interrupted copy / failed write | exception at copy_chunk; actual child exit74 during copy | No ACTIVE record; incomplete staging cleaned; retry succeeds from explicit source |
| Flush/staging failure / simulated disk full | ENOSPC at staging_written | Exception, staging cleanup, no new record; original unchanged |
| Corrupted staging | replace staged bytes before validation; corrupt abandoned staging after crash | Reject/quarantine by absence of ACTIVE record; recovery never fabricates success |
| Verification failure | invalid image/video, mismatched tool JSON, pixel/duration limit | No publication as ACTIVE; no source mutation |
| Before publication | injected exception | No new ACTIVE record, staging cleaned |
| After publication before catalog commit | exception plus real child exit73 | Complete object may remain; zero ACTIVE records; durable PENDING intent aborted on recovery; verified explicit retry reuses object |
| SQLite transaction failure | injected OperationalError before commit | Rollback all new asset/revision writes; object retained safely if already published |
| Actual connection commit call failure | connection proxy raises at final commit, delegates real rollback | Zero new catalog records, source preserved; recovery/retry valid |
| Restart + repeated recovery | fresh AssetLibrary connection after exit73/74 | First recovery aborts one pending intent; second none; stable final data; no automatic reconstruction |
| Missing / changed / corrupt original | remove or alter published file, including same-size replacement | MISSING vs CORRUPTED separately; use refused; affected asset not ACTIVE after verification |
| Unsafe object symlink | replace managed object with symlink | Mark CORRUPTED without reading linked source; resolve refused |
| Concurrent imports |4 independent connections/writers |4 distinct AssetRecords, shared single object, independent provenance |
| Source TOCTOU | swap file after stat; mutate during copy | SOURCE_CHANGED; no attachment/publication as ACTIVE |
| Child timeout | real Python sleeping child under .05s timeout; simulated probe timeout | PROCESS_TIMEOUT; subprocess.run kills/waits direct child; no successful import |
| Stale/deleted target / retired during attach | edit or remove anchor, retire in before_attach fault | STALE_TARGET / ASSET_UNAVAILABLE; no late overwrite |
| Rights / pinned revision / binding mismatch | revoke metadata, change revision/path/hash | Resolve/preview fails, no implicit latest version or alternate material |
| Corrupt thumbnail | alter only derivative | Regenerate fixed-tool identical SHA; original bytes/metadata revision unchanged |
| Schema initialization failure | inject exception after real transactional CREATE TABLE | Rollback all tables/version; clean reinitialization succeeds, no implicit partial schema |
| Unknown database version | set user_version2 then reopen | SCHEMA_VERSION, original version2 retained; no implicit downgrade/migration |

## State assertions

Every controlled import failure is checked against catalog count and source bytes. Tests compare exact SHA/content before and after. Recovery verifies every catalogued object; it does not activate orphan files or retrieve replacements from the internet. Incomplete intents become ABORTED, not COMMITTED. No physical object deletion or external user-file cleanup exists. A shared object survives retire/detach. Existing user-notes in staging outside the reserved UUID pattern are retained.

SQLite links record observed association history, not atomic project saves. If a background result becomes stale, the catalogued asset and possible link observation may remain; the changed project is not overwritten and the binary is not deleted. Undo/Redo may restore an earlier binding but current integrity/revision/rights checks still apply. This is the explicitly bounded loss model, not a two-phase commit spanning every JSON project.

## What is not proven

No power-cut, controller failure, physical disk exhaustion, corrupted SQLite page repair, hostile parent-directory writer, privileged inode manipulation, Windows reparse/ACL semantics, network-share locking or OS sandbox qualification. Hash/stat checks are not a complete TOCTOU defence. Missing/corrupt originals are reported, never rebuilt from thumbnails or guessed paths. Retained orphan objects consume disk space; no garbage collection promise.

Final counts/exit codes are in [MVP_08A_TEST_RESULTS.md](MVP_08A_TEST_RESULTS.md) and external machine-readable logs. Failed preliminary GUI/fixture attempts are retained as failures, not counted as acceptance passes.
