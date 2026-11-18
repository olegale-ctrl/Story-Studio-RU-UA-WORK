**Status: EXPERIMENTAL — independent owner review required.** Date: 2026-11-18. No production readiness or permissions. Windows: WINDOWS_NOT_RUN.

# MVP-08A — Local AssetRecord contract v1

Implemented experimental schema, not a normative Production Gate contract. `AssetLibrary.get(id, revision=None)` returns a detached JSON-safe dictionary. `revision=None` explicitly requests current metadata; bindings always specify a positive exact integer revision. Each metadata update is compare-and-swap on expected_revision; no in-place revision editing API.

| Group | Required fields / representation | Validation / unknown |
|---|---|---|
|Identity|asset_id UUIDhex; schema_version1; revision positiveint; sha256 lowerhex64; byte_size; media_type image/video; original_filename; storage_reference; created_at/updated_at UTCISO|Measured on streamed local bytes; internally generated managed paths; no traversal or external storage reference |
|Technical video|container,video_codec,width,height,frame_rate rationalstring,duration seconds,frame_count,audio_streams,technical_status|FFprobe + full decode within duration/size/time limits. Only measured nb_frames used; never estimate framecount as FPS×duration. Missing values literal UNKNOWN |
|Technical image|image_format,width,height,color_mode(pixel format),technical_status|Extension/decodedcodec must agree; FFprobe+one-frame decode. No EXIF interpretation or colour-managed display guarantee |
|Provenance|source_type,provider,model,provider_job_id,generation_timestamp,prompt_reference,input_asset_references,source_sha256,import_timestamp|MANUAL/AI_GENERATED/DERIVED/EXTERNAL_LICENSED/UNKNOWN. source_sha256 is measured from the imported source bytes; supplied mismatch is rejected. Other unknown source fields remain UNKNOWN; accepting supplied metadata is not verification of provider identity |
|Rights|rights_status,license_reference,commercial_use,attribution_required,territory,expiration,watermark_status,review_reference|UNKNOWN/PENDING_REVIEW/CLEARED_FOR_EXPERIMENT/RESTRICTED/REJECTED. Boolean fields bool or UNKNOWN; expiry timezoneISO, UNKNOWN or explicit NOT_APPLICABLE |
|Lifecycle|lifecycle_status ACTIVE/QUARANTINED/MISSING/CORRUPTED/RETIRED|Operational overlay, separate from metadata rights and integrity; retired never automatically reactivates |
|Integrity|integrity_status VALID/MISSING/CORRUPTED|Recomputed on verify/recovery/resolve. A valid checksum is not source authenticity or licence proof |
|Catalog|tags sortedunique strings; current_revision overlay|Stable sort asset_id, offset/limit1–200; deterministic for fixed catalog snapshot |

Metadata accepts only specified provenance/rights fields, bounded strings/lists, known enums and finite JSON. Invalid metadata is rejected before import. New records default unknown provenance/rights. Local experimental attach/export resolution requires current exact revision, VALID technical/integrity, ACTIVE lifecycle, CLEARED_FOR_EXPERIMENT, non-UNKNOWN licence/review/territory/watermark and commercial/attribution/expiry applicability, non-expired rights. This is a fail-closed **local review-state check**, not automated legal adjudication. Supplied refs remain untrusted statements until human review. No action string PRODUCTION is accepted. CLEARED_FOR_EXPERIMENT cannot grant production permission.

## API surface

- `import_file(absolute_source, provenance=None, rights=None, tags=None) → AssetRecord`; supports png/jpg/jpeg/webp/bmp and mp4/mov/mkv/webm, one visual stream. AI/derived provenance is a local registration only, no provider calls.
- `get(asset_id, revision=None)`, `update_metadata(..., expected_revision=...)`, `retire(asset_id)`; retire retains files/revisions/links.
- `search(offset=0, limit=50, asset_id/media_type/provider/model/date_from/date_to/rights_status/technical_status/sha256/project_id/anchor_id/tag=...)`; exact matches except date interval. Dates are compared as stored UTCISO strings, caller should supply UTCISO boundaries. No AI/fuzzy search; query values parameterized.
- `verify_asset`, `verify_library`, `recover_incomplete_imports`, `list_missing_assets`, `list_corrupted_assets`.
- `resolve(asset_id,revision,action=EXPERIMENTAL_PREVIEW|EXPERIMENTAL_EXPORT) → managed path`.
- `attach(project,project_id,anchor_id,asset_id,revision,expected_anchor=anchor_token(anchor),replace=False)`; `detach(... expected_anchor=...)`. The explicit project_id supplied by caller is a local association namespace, not authenticated identity. UI uses experimental topic namespace; topics need not be globally unique. Search therefore reflects association labels, not a production project registry.
- `thumbnail(asset_id,revision,size=256) → DERIVED descriptor`; unknown rights may be inspected locally without granting attachment/export.

Optional binding fields: library_root,asset_id,revision,sha256,link_id,project_id,previous. Previous contains only prior material/provenance/binding fields and is restored on explicit detach. Project portability requires the same explicitly managed library to be available; no auto-relocation or remote resolution. `resolve_anchor` refuses binding/path/hash disagreement. An edited anchor token, absent or ambiguous anchor is STALE_TARGET; current asset metadata changing gives ASSET_REVISION_CHANGED, not a silent upgrade. Metadata/lifecycle revocation continues to block even old saved projects.

## Errors and recovery semantics

LibraryError.code includes UNSAFE_PATH, UNSAFE_STORAGE_REFERENCE, UNSAFE_FILENAME, UNSAFE_SOURCE, UNSUPPORTED_FORMAT, SIZE_LIMIT, INVALID_METADATA, SOURCE_CHANGED, STAGING_CORRUPTED, OBJECT_CORRUPTED, MEDIA_LIMIT, MEDIA_VALIDATION_FAILED, INVALID_TOOL_OUTPUT, PROCESS_TIMEOUT, INVALID_SEARCH, ASSET_NOT_FOUND, REVISION_NOT_FOUND, INVALID_REVISION, STALE_REVISION, ASSET_UNAVAILABLE, ASSET_REVISION_CHANGED, RIGHTS_NOT_CLEARED, RIGHTS_EXPIRED, PRODUCTION_NOT_AUTHORIZED, STALE_TARGET, EXPLICIT_REPLACE_REQUIRED, BINDING_MISMATCH, NOT_ATTACHED and WRONG_LIBRARY. OSError/sqlite3 errors remain explicit exceptions, not success. GUI surfaces errors, does not label failed import/export as completed.

Recovery aborts incomplete intents; it does not reconstruct originals from thumbnails, user filenames, remote URLs or guessed sources. Missing/corrupted results are separate. Orphan binaries are retained for later verified explicit reuse; no cleanup deletes external user source files. See fault report for tested versus unqualified failure modes.
