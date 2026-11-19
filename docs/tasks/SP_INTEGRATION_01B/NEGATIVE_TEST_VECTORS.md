# Negative test vectors and exact outcomes

**SP-INTEGRATION-01b · 2026-11-19 · LIMITED_DIAGNOSTIC_IMPLEMENTATION_CANDIDATE · no execution/release authority.**

New replay artifact: new-vectors.json contains165 full input/expected/actual cases; schema-validation.json contains1041 independently checked assertions and20pattern inventory. Structural corpus is compared with jsonschema4.26.0; semantic checks remain separately mandatory. Positive A/B/C/D objects and seven transport fixtures for each route are included. Historical46vectors and117assertions remain unchanged under SP/1.

|Family / exact mutation|Expected structural result|Expected full admissibility / diagnostic outcome|
|---|---|---|
|G01 route D on topic input;stages reversed;duplicate render.mp4;empty stage list|true for these field-shaped mutations|false,ROUTE_STAGES|
|G01 intent_sha256=64zeroes on otherwise valid intent|true|false,DIGEST|
|G01 proposed_job_types=[unknown]|false|false|
|G01 inputs topic+script or no primary|false|false|
|G01 status=ACCEPTED or accepted_job_ids=[x]|false|false|
|G01 blockers=[] on prepared job intent|true|false,BLOCKERS|
|G02 exactly64lowercase a characters|true hash syntax|Full intent false if digest is not recomputed; syntax is not authenticity|
|G02 63/65a;64uppercase A;64a+LF;64a+CRLF;leading/trailing space;64Cyrillic а|false|false|
|G02 exact UUID/hash with terminal LF/CRLF in related ref|false|false|
|G03 topic/script/scene/title only whitespace|false where structural text pattern applies|false|
|G03 locale ua;empty/missing scenes;unknown plan fields|false|false|
|G03 scene image ../x.png|true as structural string|false using existing path validator|
|G03 image1 path other.png while plan image frame1.png|true|false,MATERIALS|
|G03 clip1 role;incomplete/extra per-scene materials;voice1.mp3|false for unsupported role;some incomplete/path shapes true|false;no implicit substitute|
|G04 every required readiness field removed one at a time|false|necessary=false,release=false|
|G04 any axis JSON true,false,null,1 or string TRUE|false|necessary=false,release=false|
|G04 any required axis unknown or false string|true valid tri-state|necessary=false,release=false|
|G04 full1.1,all axes true,blockers[],fallback none,bindings_current=true,creative_review=true,production|true|necessary=true,release=false,status=BLOCKED_CONTRACT|
|G04 same object in draft or with equivalent/degraded/placeholder|true|necessary=false,release=false|
|G04 flags declare facts/rights/render|true intent flags|initial axes all unknown;no attestation proof|
|G04 extra attestations={trusted:true} on readiness|false|necessary=false;no manufactured receipt|
|Old schema_version/policy with1.1 consumer|false|false;no auto upgrade|
|Any readiness/gate/report release_allowed=true|false|false;no release path|

The all-true case is a fixture of **unverified assertions**, not a trusted attestation or evidence record. Empty declared evidence is permitted by the local schema and proves nothing. No test creates a signature,receipt,issuer or production permission. Independent canonical byte/hash recomputation checks determinism; changed version/policy/body changes digest. Repeated preparation is not job idempotency.
