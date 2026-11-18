# MVP-05/06 implementation, boundaries and next priorities

Status: EXPERIMENTAL / independent owner review required. All new code and generated demonstrations are confined to `experimental_mvp/`. No G3.2.1 validator, normative schema, workflow, main, merge, production storage or production permissions changes.

| Component | Implemented | Actual validation / limit |
|---|---|---|
| Editorial module | Manual mode and configurable OpenAI-compatible/local HTTP interface; structured RU/UK drafts, claims/risks, distinct explicit apply; bounded response, timeout, redirect refusal; provenance and prompt version | Local HTTP mock over real sockets, unavailable service and malformed response tested. Real external LLM / real local model quality NOT_RUN. Facts always UNVERIFIED |
| Existing Story Intelligence | Existing optional Editor Preview input path retained | Uses existing schema only. No fabricated evaluation, synthetic approval, or mapping that claims LLM text is a verified Evaluation |
| VideoAnchor | All 17 requested fields, stable IDs, scene links, relative-ms coverage, reorder, explicit split, separate narration/visuals, immutable imported-byte cache, SHA-256 and provenance | Roundtrip/reorder/text-edit preservation, gaps/overlap/tamper, reusable paths, different durations tested. Extra `asset_sha256`, provenance, priority, source offsets and optional text font support are experimental fields only |
| Storyboard GUI | Nested scene/anchor list and relative-time columns, scrollbar, field form + advanced editor, prompts, provider assignment, import, system player, reorder/split/save | Linux real Tk smoke + widget regression. No draggable graphical timeline; form and advanced JSON remain simple experimental UI |
| Visual renderer | Imported videos/stills, pan/zoom, local text animation, explicit placeholder; scale/pad/FPS normalize; trim/hold-last-frame; copied-input hash check | MP3/WAV and short/long 15/60-FPS clips normalized to 24-FPS output; full decode tested. MAP/INFOGRAPHIC require authored imports, not automatic cartographic/data generation |
| Media Hub | Catalog of 13 official services, official browser entry, manual account state/quota editor, instructions, prompt copy/import | No provider credentials/session collection. State is self-reported, not a verified API connection. No media API adapters, authenticated quota discovery, web automation or automatic paid generation implemented |
| Quota Planner | Type/duration candidates, priority ordering, finite manually confirmed balance/cost, expiration/reset, budget within queue, reuse and fallback suggestion, no repeated generation | Planning deterministic and non-mutating. READY does not reserve actual provider credits. All eight requested status values are represented in the anchor model; automatic transitions to GENERATING/FAILED from external APIs are intentionally absent; manual status edits/import are supported |
| Demonstrations | Original manual editorial lesson, local original diagrams + eSpeak NG speech, RU/UK portable inputs; explicit unapproved initial state | Actual 3–5 minute CPU renders and complete decode. Pronunciation, pacing and final editorial suitability still need human review; not a production permission |
| Evidence | Input snapshot, audio/visual/caption hashes, tool versions, output SHA, logs, timing, incomplete/completed status | Experimental evidence, not PG-05 implementation, signed evidence, audit-trusted storage or a rights certificate |

## Remaining risks and gates

- Windows 10/11 / CPU / symlink/reparse behavior and Credential Manager have not been qualified here. Linux screenshots and virtual display results cannot close Windows acceptance.
- Local filesystem is trusted-user experimental storage. Hash checks detect changed imports at validation/copy time; they do not eliminate TOCTOU, hard links, reparse points, parent directory replacement, hostile concurrent writers, malicious FFmpeg inputs or forged account/rights metadata. No qualified protected storage, sandboxed executor or revocable production authorization is provided.
- Common audio uses estimated word-weighted scene boundaries. Exact anchor coverage is checked against measured audio milliseconds, not semantic timing. Retiming is manual. Encoder frame quantization can extend visual duration slightly; full-demo MP4 durations and measured audio are reported separately.
- Cancellation is cooperative, checked between commands/anchors, not instantaneous process termination. Audio cache is resumable; video segments rebuild. Disk quotas, FFmpeg resource isolation, transactional audit evidence, project schema migration and concurrent editing are not qualified.
- Missing imported files fail; fallback must be chosen explicitly for missing not-yet-imported material. Unknown rights are recorded and require review; experimental export does not certify licenses or block every unqualified asset as a production gate would.
- Catalog observations are dated public-source research, with unresolved fields UNKNOWN. They do not guarantee eligibility, a free balance, watermark-free downloads or commercial use. Recraft official quota pages disagree; Pika Free includes no monthly credits in its reviewed pricing table. Media generation is manual only, without automatic calls, stored browser sessions or credit spending.
- No real credentials, Google login, generation, payments, quota consumption or provider outage probing against live accounts were exercised. A refused local mock service tests failure handling, not every provider's behavior.

## Next priorities (proposals; no automatic next stage)

1. Independent Windows 10/11 execution and human editorial/listening review of both demos at this exact commit.
2. Improve storyboard ergonomics (zoomable visual timeline, guided timing edits, asset library thumbnails) and accessibility/scaling checks.
3. Select any official media API adapter only after owner approval of current terms, rights, credential storage, budget reservation/cancellation and per-job cost confirmation. Free web credits must not be assumed API credits.
4. Qualify external LLM quality with factual-source and scientific-review oracles; do not replace editorial judgement with schema validity.
5. Any production gate, protected storage, revocation, signed evidence or release is a separate owner-approved task. This branch does not start it.
