**Status: EXPERIMENTAL — independent owner review required.** Date: 2026-11-18. No production readiness or permissions. Windows: WINDOWS_NOT_RUN.

# MVP-08A — Security review

Scope: trusted-user local experimental workspace. No authenticated provider, secret storage, S3, production executor or permission implementation. Review covers current code and executed Linux tests; not independent penetration certification.

| Threat | Implemented guard | Residual limit |
|---|---|---|
|Traversal, symlink, junction|Absolute paths, reject `..`/UNC, inspect ancestors and reparse flag, regular file checks, final O_NOFOLLOW where available, generated storage names|Windows native handle semantics NOT_RUN; hostile parent replacement/hardlinks/ACL changes remain TOCTOU risk |
|Source substitution while copying|Compare dev/inode/size/mtime_ns/ctime_ns before/open/after, fstat opened handle, compare source path again, hash staging before/after validation|Cannot defeat hostile concurrent writers restoring metadata or privileged filesystem attacks; not absolute protection |
|Partial import / crash|Private staging namespace, streaming/fsync, SQLite intent and transaction, serialized writes, verify publication before ACTIVE; fail cleans staging; crash recovery aborts pending|Directory fsync/power-loss and filesystem corruption not qualified; retain orphan binaries, no secure erase |
|Malformed/oversized media|128MiB input default;120s video;8192 max dimension/32M pixels;≤8streams and onevideo; extension/codec checks; full bounded decode;20s child timeout; stdout/stderr spooled|FFmpeg native memory/CPU not sandboxed. Child may allocate before probe; timeout/size limits not a hardened parser boundary |
|Execution/network through imported media|No shell interpolation, subprocess arglists, -nostdin, file/pipe protocol whitelist; no autoplay or execution, only local decoder|No formal OS network sandbox. Malicious decoder vulnerabilities require separate qualification/updates |
|False rights clearance|DefaultUNKNOWN, explicit review state and refs, revisions pinned, current revocation/retire checks, production action rejected|Text refs/checkboxes not authentic licences. Human review of source/music/voice/likeness and intended use required; no production authorization |
|Shared bytes/licence confusion|New UUID record per import, content dedup only, separate provenance/rights revisions|Source/provider claims remain self-reported; dedup doesn't validate origin |
|Broken preview/corrupt original|Original never replaced by API; derivative record/hash separate; regenerated poster deterministic under pinned tools; verify before resolution|Local user can still alter files directly. SHA proves byte identity, not provenance or adversarial immutability |
|Stale asynchronous result|Anchor/project snapshot compare; exact asset revision; no automatic latest/path fallback|Project JSON and SQLite history aren't atomic together; DB may show unapplied historical link. Files retained, never deleted based on link count |
|Tk thread lifecycle|Plain-data worker closures, queue results, GUI-only updates/commits/finalizers, GUI-thread collection of prior Tcl garbage before workers|Native Tcl9 crash was reproduced then corrected; no Windows/HiDPI or prolonged stress qualification; other existing modules not globally redesigned |
|SQL injection / metadata abuse|Parameterized search values, fixed field mapping, bounds/enums, immutable version rows via API|SQLite file itself is trusted local metadata; tampering is not authenticated audit history |

## Reproduced issues addressed

During new tests: a test harness initially treated preview Path as tuple (corrected test only); a combined GUI run exposed native Tcl finalization on worker GC, including exit132/SIGILL. Isolated GUI passed, but combined reproduction did not; implementation was adjusted to remove Tk captures, release image/variables on close in GUI thread and collect abandoned Tcl garbage before spawning a worker. Full combined verification is recorded in final test report, with failed attempts retained outside Git. No failed attempt is relabelled PASS.

Review also made schema DDL initialization transactional, rejected implicit schema downgrades, preserved measured source hashes across metadata updates, tightened invalid metadata types, and tightened unsafe-object verification (marks CORRUPTED without following symlink), final lifecycle check during attach, and restoration of exact previous binding after explicit replacement/detach. These are covered by regression tests. No changes to normative contracts or production architecture.

## STOP boundaries

No live generation, quota calls, account registration, payments, browser automation, keys, CI, main, merge, release, G3.2.1 or production storage/permissions. Local previews are experimental inspection, not scientific/artistic approval. Any hostile filesystem, high-assurance rights enforcement, protected storage, signed evidence or production release requires a separate authorized task and qualified OS/executor/storage.
