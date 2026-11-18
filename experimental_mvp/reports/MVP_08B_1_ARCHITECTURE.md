**Status: PROPOSAL — CONTRACT_PREPARATION_ONLY.** Date: 2026-11-18. All future behavior below is NOT_IMPLEMENTED / NOT_RUN.

**Evidence labels used throughout:** EXISTING = inspected at base `1ff403e47d35adb34139278de1d056fbbc563e6d`, not re-executed here; APPROVED = owner task plus unchanged D01–D08 in [owner record](MVP_08_OWNER_APPROVAL.md); PROPOSED = this new contract, not implementation authority; OPEN = unresolved gates in [decision register](MVP_08B_1_OPEN_DECISIONS.md). Windows qualification remains WINDOWS_NOT_RUN. No runtime, live adapter, downloader, executable tests, API calls, payments or production permissions are introduced.

# Offline Dispatcher architecture and exact interface audit

## Baseline and source authority

Base commit `1ff403e47d35adb34139278de1d056fbbc563e6d`, tree `2fecb71e711861431a775f4aa3764d771f35ecb5`; branch `docs/story-studio-experimental-mvp-08b-1-dispatcher-contract`. Clean branch created from exact base. Research source `f4661c86103bbcedf304201202203f20f3bb2747`, eight exact `MVP_08_0_*.md` Git blobs read directly, not merged. Existing provider research is historical evidence, not current terms/account/model qualification. No Wan version is approved merely because it appeared in research.

Exact source blobs/SHA256/byte sizes and snapshots are in external `source-reference-inventory.json` and sources/. Source locators below are symbols at the pinned base; all existing behavior is source-inspected, no new runtime test claim. The inventory also includes MVP-08A architecture/contract/security/limitations/acceptance/test/fault reports and unchanged owner decisions. Prior837passed/2 skipped is historical MVP-08A evidence only.

| Ref / existing API | Input → output | Mutation / errors / atomicity | Reuse / future decision |
|---|---|---|---|
|I01 asset_library.encoded, anchor_token, find_anchor|JSON dictionary → canonical string/hash/unique anchor|Pure encoding; find_anchor raises STALE_TARGET for missing/ambiguous ID; token covers all dictionary fields|Use for exact editing snapshot; not monotonic edit counter, authenticated identity or storyboard generation fingerprint |
|I02 AssetLibrary(root,create=...) / connection|Local absolute root → per-operation connection|Schema1,JSON1 required; transactional DDL, FULL sync, BEGIN IMMEDIATE for writers; timeout90s; LibraryError/OSError/sqlite errors|Local catalog only; no queue transactions/worker fences shared with Dispatcher |
|I03 import_file(source,provenance,rights,tags)|Absolute local source → new AssetRecord revision1|Durable PENDING intent; stream/hash/fsync/probe/decode; object publish then transactional record/COMMITTED; no cross-FS/SQLite atomicity; abort/retained orphan on crash|Reuse local registration, content dedup. No caller import idempotency key or unique job→asset receipt; lost-return ambiguity needs OD02 |
|I04 technical / _run|Local staged media → technical dictionary|FFprobe nb_frames parsed, optionalUNKNOWN; fullvideo/oneframeimage decode exit status, not independently counted frames; default128MiB,120s,32Mpixels/8192dimension,≤8streams,onevideo;20s per child; spooled output cap1MiB|Reuse baseline decoder check, add separate future decoded-frame evidence (P1-01); not qualified OS sandbox |
|I05 get / search|asset ID/revision or exact filters/page → detached records|Read current metadata by default; status cached, not live verification; search current revisions only, stable asset-ID ordering,limit≤200; project/anchor search includes historical links|Exact pinned revision and full pagination mandatory; tags candidates not authoritative import receipt |
|I06 update_metadata / retire|ID+expected_revision → new metadata/current state|Metadata CAS appends revision, original/source hash fixed; retire operational state, no physical delete; STALE_REVISION|Never clear rights or upgrade a pinned scene implicitly; caller must interpret policy outside metadata text |
|I07 verify_asset/library / recover_incomplete_imports|ID or library → integrity/lifecycle/aborted-intent lists|Writes observed statuses; pending imports aborted, reserved staging cleaned; orphan binaries retained; does not reconstruct source or resume metadata|Reuse explicit verification; not a Dispatcher recovery journal or proof an unknown import never committed |
|I08 resolve / resolve_anchor|Exact ID/rev/action or anchor → local path|Checks latest rev equals pin, integrity,ACTIVE,technicalVALID,rights fields/expiry; binding/path/hash match; writes integrity observations; LibraryError incl ASSET_REVISION_CHANGED,RIGHTS_NOT_CLEARED|Mandatory before local use, not authenticated legal proof or in-flight revocation fence |
|I09 attach / detach|Mutable project+target+asset exactrev+anchor token → binding / mutation|Checks token/replacement/rights; commits links before mutating dictionary; linkUUID historical; detach restores prior fields, no binary delete|Prepare on copy; GUI/project CAS and durable save receipt remain separate P1-03 boundary |
|I10 thumbnail|ID/rev,size16–512 → DERIVED descriptor|Local FFmpeg first frame/cache; original unchanged; independent derivative metadata; timeout/error|Optional catalog view, never validation of artistic quality or exact framecount |
|I11 storyboard.VideoAnchor / fingerprint|17fields / generation subset + reference bytes → prompt hash|Existing fingerprint omits arbitrary editing fields; reads reference file; import_asset is legacy path flow separate from Library; validate/video_spec/render resolve bindings and copy/hash inputs|Keep dataclass17fields unchanged; use BOTH editing token and full immutable request hash; no Dispatcher calls legacy import as a hidden bypass |
|I12 timeline.Editor.asset_change, undo/redo/save|Candidate+expected encoded project → editor mutation/history; path→save|CAS against editor snapshot; structural validate; history100,approved=False; save delegates pipeline.save; no monotonic project revision or cross-DB transaction|Reuse GUI-thread transactional apply; raw saved-file hash and stable project identity need future broker/OD03 |
|I13 timeline.preview / pipeline preview_session/build|Project/timing/localworkspace → temporary prerender path|Copied project, cooperative/process cleanup inherited07.1, bound inputs validated; errors/cancellation not success|Optional post-attach inspection, not automatic publication, evidence of scientific truth or sound-quality acceptance |
|I14 pipeline.save/load/file_digest|Path/project → atomic JSON replacement / loaded dictionary / streaminghash|Temp serialize/readback/fsync/replace, exceptions preserve prior file; no expected-disk-hash CAS; load may assign IDs and resolve some relative paths|Do not call save as if it were concurrency CAS. Broker must qualify exact disk/editor revisions and read back binding; raw file authoritative |
|I15 asset_ui.AssetLibraryPanel|GUI callbacks/plain-data workers → queued GUI updates|Threads,80ms polling, GC/finalizer handling; closed panel ignores callbacks; project snapshot CAS; topic-based project namespace not globally stable|Reuse patterns only; P1-02 stays open. No existing durable Dispatcher queue or saved-project receipt |
|I16 ui.launch / apply_edit|Collected project → main UI state|Tabs,explicit project save; apply_edit changes memory, not durable JSON|Long-lived worker owner must be independent of panel; saved confirmation separate from apply callback |

## Proposed architecture

VideoAnchor snapshot → immutable GenerationJob + bounded batch permit → persistent controller/outbox → qualified **offline simulator only** → result receipt → local quarantine/validation → recoverable Asset Library saga → exact asset revision → GUI CAS → explicit saved-project readback → Timeline. Manual download/re-import is not the target product flow. A user may approve a bounded batch once and save an assembled project explicitly; this does not require manually generating/downloading each clip.

Proposed components: JobStore/events/outbox; ApprovalVerifier; BudgetQuotaLedger; Lease/FenceCoordinator; ProviderAdapter; deterministic SimulatorStore; ArtifactStore/ValidationManifest; IngestionSaga; GUI bridge/ProjectSaveReceipt; reconciliation inspector. No component is implemented here. Queue, simulator ledger, files, library DB, editor and JSON are distinct resources, never one assumed atomic transaction.

## Invariants and authority

G01 — in the first proposed execution profile only the separately authorized offline simulator may execute under$0; live master switch remains disabled regardless of “free” marketing.
G02 — immutable request/auth snapshot and idempotency identity; modified scope means new job/reapproval, not mutation of sent request.
G03 — one fenced controller per job; stale worker cannot write state/effects. Local fence cannot retroactively stop a provider call already accepted.
G04 — no external submit before durable intent/reservation; unknown outcome never another possibly billable submit.
G05 — same bytes≠same provenance/rights; exact import receipt, result identity and validation required.
G06 — reuse committed asset after attachment failure; never re-generate for a GUI/save problem.
G07 — saved JSON is current-binding authority; DB links and GUI success are not completion evidence.
G08 — no stale overwrite; asset revision/rights rechecked; old results retained unlinked.
G09 — technical/schema PASS≠artistic/scientific/commercial/production approval.
G10 — final status receipts are historically scoped; later user edits do not falsify the old receipt or authorize restoring old binding.

## D01–D08 traceability

|Decision|Contract application|
|---|---|
|D01|Wan target, future Runway/MiniMax; exact live model unresolved; simulator uses distinct synthetic identity|
|D02|Budget ceiling0; simulator charge0; no live activation or paid fallback|
|D03|No browser automation; a future written permission would still need separate qualification|
|D04|PAUSED_QUOTA, preserved job; alternative requires already valid scope or new job approval|
|D05|Documented intended-use/input/voice/music/territory/expiry/attribution/watermark review; text is not authentic proof|
|D06|30% planning assumption with10–50%sensitivity; no measured throughput claims or retries without caps|
|D07|Batch content digest,expiry,spend/data-scope consent; reapprove material changes|
|D08|Future adapter+durable queue+spend controls+safe ingestion+Library+fault tests; stage gates, no current implementation|

## P1 traceability and OPEN

P1-01: ingestion DFE-v1, T041–T043. P1-02: worker/panel lifetime protocol in security/rights, T064–T067. P1-03: saga/save readback and historical reconciliation, T050–T056/T068–T070. OD01–OD08 remain proposals; offline core can be specified without resolving live credentials/model. Some future handoff/Windows/live implementation gates remain blocked, not the preparation of this documentation.
