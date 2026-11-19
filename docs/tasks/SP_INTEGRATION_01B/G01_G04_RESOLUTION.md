# G01–G04 resolution

**SP-INTEGRATION-01b · 2026-11-19 · LIMITED_DIAGNOSTIC_IMPLEMENTATION_CANDIDATE · no execution/release authority.**

|Gap|New behavior|Code / schema boundary|Evidence|Disposition|
|---|---|---|---|---|
|G01 route/stages/digest|Both stages require exclusive input type, exact matching route and finite ordered stage list; recompute exact canonical body SHA; fixed blocked status,empty accepted IDs,required blockers|validate_diagnostic(job_intent),_inputs,_intent; job_intent.schema.json|Wrong route/order/digest/unknown/duplicate/omitted stage/conflicting inputs/status/IDs/blockers tests and165-vector corpus|RESOLVED for1.1 only; no Dispatcher added|
|G02 terminal LF|All new hash/UUID end anchors strict; lowercase64hex only; old schemas unchanged|Seven new schemas; existing runtime fullmatch/ref validators; structural interpreter pattern search|Length63/64/65,upper,LF,CRLF,prefix/suffix spaces,Unicode lookalikes;20patterns inspected,14hash/UUID occurrences each terminal probe|RESOLVED for1.1 only; old acknowledged gap preserved|
|G03 schema vs semantics|Explicit mandatory structural then semantic validation; substantive text,locale/scene rules,existing path checks,exact D material profile and map/plan consistency|validate_structure→validate_diagnostic; legacy.validate_plan/validate_materials and core.media_paths; existing filesystem gates read_plan/safe_image|Blank text/title,bad locale,missing/extra fields,traversal,unsupported clips/MP3,missing/extra/mismatched material paths|RESOLVED in bounded declared-input profile; no filesystem/trust claim|
|G04 minimal assertions|Necessary=true only after full1.1 readiness shape+semantics and all required diagnostic conditions; missing/old/wrong axis type cannot satisfy|assess_release validates readiness,then axes/policy/blockers/fallback/assertion conditions|Every required field deletion,each axis type/state,alltrue,unverified flags/extra attestations,bad bindings,version tests|RESOLVED for complete local diagnostics; no trusted verifier|

New schema-valid path strings or cross-field mutations can still fail semantic validation; this is intentional two-stage design, not a claim all rules are expressible in JSON Schema. Only the conjunction is admissibility. Structural interpreter and independent jsonschema agree on the pinned strict-domain structural corpus. Reports/refs/digests are local declarations, not PG grants. All historical G01–G04 probes continue producing their exact old results under old version.

Security limit unchanged: syntax/path checks and separate file reads do not prevent hostile TOCTOU/hardlink/reparse/mount/rename races. Windows not qualified. No direct build,queue/store/retry/recovery/provider or new crypto. Final validation/storage/authority/release blockers remain.
