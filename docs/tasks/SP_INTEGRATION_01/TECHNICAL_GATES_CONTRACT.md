# Technical gates contract

**SP-INTEGRATION-01 · PROPOSAL · 2026-11-19 · no production authority.**

`core.topic_to_film_gates.run_gates(route,phase=intermediate,...)` is implemented as bounded read-only **partial diagnostics**. It reuses `read_plan`, `wav_ms`, `safe_image`, `Project.from_dict`, `audit_timeline` and `validate_media_path`; pure plan prevalidation adds portable Windows-path rejection. It does not run a renderer, decoder or shell. Direct named inputs only, no directory scan or mutation. Files are capped at1MB JSON/16MiB media for diagnostics, not production support limits.

|Gate|Implemented check|Not proven / blocker|
|---|---|---|
|Plan|ru/uk;1..20 scenes; nonempty text≤2000; existing read_plan agreement; simple image names/suffixes and portable-path constraints|Exact stable plan identity/storage snapshot; conversion from arbitrary storyboard dialect|
|Assets|For declared First Video audio directory: voiceN.wav exists, PCM WAV header/rate/frame count and complete declared sample bytes; duration agreement with wav_ms; image regular bytes/path resolved through safe_image|Image decode/dimensions, clips, reference completeness, licenses, hostile decoder isolation: BLOCKED_ASSET_DECODER_CONTRACT|
|Project|Existing Project.from_dict migrations/schema and timeline diagnostics|Warnings not all hard errors; no artistic/subtitle readability proof; project/media/render binding verifier missing|
|Render|MP4 regular-file bounded byte observation only|MP4 decode, H264/AAC/subtitle stream/duration/dimensions/exact expected-output verification NOT_RUN; BLOCKED_RENDER_VALIDATION_CONTRACT|
|Publication|No filesystem writes|BLOCKED_RESULT_PUBLICATION_CONTRACT; no completion receipt or recovery|

Route A/B intermediate may lack plan (NOT_RUN future stage); C/D require plan now. D requires voice/image inputs now; final requires plan, all voice/image inputs, project and MP4 for every route. No implicit image generation. Missing inputs are blockers; parser/validator errors give FAIL. D and final stay blocked on unimplemented asset qualification even if local path/WAV checks pass. MP4 presence never produces technical_pass true. Intermediate status INTERMEDIATE_CHECKS_PASS means only checks performed; technical_pass remains unknown and release_allowed false. Final report can never PASS under missing worker contracts.

Proposed future render worker: use existing project/media/integrity validators over an immutable declared snapshot, bounded FFprobe for expected stream/codecs/dimensions/subtitle/duration and full FFmpeg decode, tool/version/exit-code evidence, expected result bindings, fail closed on missing/partial files, warnings interpreted by approved profile. Existing D1 inspect_video assumes its fixed1.4s synthetic scenario and is unsuitable as a general gate. Bundle verify_bundle is scoped to its bundle manifest, not an automatic scan over arbitrary user roots. No new FFmpeg CI/artifact publication is enabled.

False technical PASS must be impossible on decode error, interrupted render, missing final artifacts, stale observation, unbound output or partial evidence. Those executor fault tests remain NOT_RUN. Facts, rights, aesthetic quality and subtitle legibility require accountable human/qualified review independent of technical checks.

Security boundary: lstat rejects visible links/reparse ancestors, then bounded regular-file read. There is no claim these separate checks/read operations prevent hostile TOCTOU, Windows junction races, hardlinks, mount changes or parser/native decoder attacks. Stable trusted local storage is assumed for diagnostics only. Rechecks reduce accidental changes, not OS qualification; no authorization is derived from them.
