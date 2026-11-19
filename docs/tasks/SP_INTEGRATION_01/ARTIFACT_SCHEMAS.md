# Artifact schemas

**SP-INTEGRATION-01 · PROPOSAL · 2026-11-19 · no production authority.**

All seven JSON Schema draft2020-12 files in `../../../schemas/topic-to-film-v1/` are PROPOSAL diagnostic transports, version `SP/1-PROPOSAL`, policy `SP-REVIEW-ONLY/1`. They are not PG/SI envelopes or a new persistent storage/identity system. Closed report/intent outer objects; required fields explicit; unknown readiness is a string, not JSON null/boolean. Arrays capped at10000; strict canonical helper adds 1MB/32-depth/string bounds for intent inputs. Future worker resource budgets remain unapproved.

|Logical future artifact|Schema|Current status|
|---|---|---|
|meta/route.json|route.schema.json|Projection of route/mode/intent digest, BLOCKED only|
|meta/readiness.json|readiness.schema.json|Six independent axes, evidence refs, bindings, blockers; release false|
|meta/jobs.json|jobs.schema.json|No approved JobStore API, empty IDs/observations; not a local state mirror|
|meta/artifact_manifest.json|artifact_manifest.schema.json|Declared-input diagnostic observations; publication blocked|
|job intent/payload|job_intent.schema.json|Prepared request only; not accepted GenerationJob or serialized queue payload|
|technical gate report|technical_gate_report.schema.json|Read-only partial diagnostics; technical_pass unknown|
|Production Readiness Report|production_readiness_report.schema.json|Necessary-condition diagnostic; never release permission|

No meta files are automatically written. Schema validity alone is neither execution authorization nor factual/right/creative readiness. `detail` is a diagnostic value, not trusted evidence; reports require semantic validators. Plan uses existing First Video dialect, not experimental storyboard VideoAnchor schema. Text must also be nonblank; image paths use validate_media_path plus simple-filename/suffix constraints; JSON Schema alone does not prove path safety. Material map key must equal role; path must be portable; declared hashes must be measured independently. Intent hash must be recomputed; schema cannot prove it.

SIRef `{type,id,revision,sha256}` and ERef `{kind,id,revision,content_hash}` vocabularies mirror existing model_v1. They are claims requiring existing structural validators, resolver, provenance/currentness where relevant. Merely fitting their schema proves no record closure, registry authority or permission. PG typed references/ByteRef binding and approved prefix domain are not replaced by `{role,path,observation}`. That structure is explicitly a local byte observation; PG mapping is an OPEN contract. No UUID for projects/jobs/assets is invented by this feature.

Raw SHA-256 uses exact bytes; canonical intent comparison uses existing SI canonical byte serialization. PG P1 own binding removal/domain prefix and raw ByteRef are separate approved domains; no claim SP hash can substitute. Policy changes require new intent/review; input byte changes invalidate exact snapshot comparisons. `binding_matches` is equality only, not a verifier of scope, grant issuer, revocation or currentness.

Future publication must reserve new destinations, validate complete results, write evidence atomically under approved storage contracts and reconcile through Dispatcher. Unknown publication outcome must not trigger private retry/cleanup. This feature implements no storage transactions, deletion, recovery, overwrites or artifact downloads.
