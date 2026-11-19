# Routing and job matrix

**SP-INTEGRATION-01 · PROPOSAL · 2026-11-19 · no production authority.**

|Route|Input|Proposed ordered stages|Implemented execution support|
|---|---|---|---|
|A|Topic|script.draft → plan.from_script → plan.validate → assets.voice → assets.images → render.mp4 → gates.technical|NONE; draft default, production policy missing|
|B|Script|plan.from_script → plan.validate → assets.voice → assets.images → render.mp4 → gates.technical|NONE|
|C|Scene plan|plan.validate → assets.voice → assets.images → render.mp4 → gates.technical|NONE|
|D|Plan + declared materials|plan.validate → render.mp4 → gates.technical|NONE; declarations do not prove complete/usable assets|

These are intent labels, not existing registered Dispatcher types. Existing MVP-08B.1 GenerationJob covers a proposed video-generation lifecycle; it is not an implemented general DAG engine and does not approve these seven labels. No Dispatcher extension implemented here.

Required separate API proposal: immutable request with supported job type/version + declared exact inputs + policy/auth snapshot; atomic accepted/reused/conflict receipt keyed by approved idempotency scope; authoritative JobStore observation by exact job ID/revision; bounded observer deadline/cancellation; durable job result/publication receipt; qualified Library ingestion/save receipt where needed. API signatures, errors, supported dependency DAG and observation ordering require owner approval and implemented conformance tests first. No duck-typed or dynamically imported pretend backend is supplied.

Oracles for future API: same intent cannot duplicate effects; changed input/policy cannot reuse an old grant; accepted is not completed; stale mirror never overrides JobStore; unknown submission/publication outcomes reconcile rather than retry; job completion before artifact publication is not film completion; observer timeout is not job failure; interruption preserves authoritative state; no queue or recovery mechanism may live in CLI. These runtime oracles are NOT_RUN because no API exists.

Without `--wait`, only genuinely accepted job IDs could be returned by a future API. Current preparation always returns empty IDs and BLOCKED. With `--wait`, no API means immediate BLOCKED, not fallback execution. Jobs schema deliberately disallows a fake local mirror.
