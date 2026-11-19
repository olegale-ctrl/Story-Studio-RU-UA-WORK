# Integration inventory

**SP-INTEGRATION-01 · PROPOSAL · 2026-11-19 · no production authority.**

Base: `f0bce140451bf00a86f3939330e77ed63b2c98be`; tree `0b5238611cc84ef0a665f75b552757666935516e`. Clean verified experimental lineage includes MVP-08A and contract-only MVP-08B.1; main ancestor and observed remote main: `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`. Main is not reset or changed. Branch: `feat/sp-integration-01-topic-to-film`. Selection is an integration working base, not an assertion every proposal in its history was approved.

Before editing, recorded remote heads externally in `remote-heads-before.txt`; only MVP-08B.1 Dispatcher contract branch found, no MVP-08B.2 implementation branch. Repository search found no implemented Dispatcher/JobStore. This negative result is scoped to inspected repository and advertised heads, not private/unadvertised work.

Planned/final scope: new `core/topic_to_film.py`, `core/topic_to_film_gates.py`, `scripts/topic_to_film.py`, `tests/test_topic_to_film.py`, seven `schemas/topic-to-film-v1/*.schema.json`, eleven documents in this directory. Existing tracked files unchanged. Exact source blobs/raw SHA-256 and final diff are in external acceptance packet.

|Requirement|Existing implementation|Contract/status|Missing capability|Integration decision|
|---|---|---|---|---|
|Topic evaluation|`story_intelligence/evaluate_v1.py:evaluate_si`|IMPLEMENTED; bounded pure SI evaluation|Facts, editorial selection, live evidence authority|Do not infer facts or call evaluation an approval|
|SI closure/provenance/currentness|`model_v1`, `records_v1`, `resolver_v1`, `provenance_v1`, `currentness_v1`|IMPLEMENTED; exact typed refs, supplied observations|Trusted current-head storage|Reuse identity vocabulary in proposed schemas; no new resolver|
|SI projection|`decision_projection_v1.py:project_evaluation`|IMPLEMENTED G1 pure foundation|Editorial authority/production permission|Presentation only; untouched|
|Editor Preview|`scripts/editor_preview.py:preview/run`|IMPLEMENTED G2 V07|Native trusted snapshots and production grants|Read-only boundary remains; untouched|
|D1 renderer|`scripts/topic_to_video.py:run`|IMPLEMENTED G3.1, only registered D1/purpose/permit digest|General authorization|Never reuse SyntheticRenderPermitV1 for another job|
|First Video|`scripts/first_video.py:read_plan,wav_ms,safe_image,build`|IMPLEMENTED local WAV/Silero renderer|Dispatcher wrapper, execution authorization|Reuse read-only validators; never call build|
|Scene plan|`first_video.read_plan`; no separate scene-plan JSON schema at base|IMPLEMENTED ru/uk,1..20 scenes,text1..2000,image filename|Stable plan identity and mutation broker|Pure compatible field validation plus stricter portable paths; proposal only|
|Project|`core/project_schema.py:Project.from_dict`; `schemas/project-v3.schema.json`|IMPLEMENTED v1/v2 migration and v3 validation|Version-bound storage receipt|Reuse actual Project validation; no replacement schema|
|Media manifest|`core/media_manifest.py:manifest_for_project`|IMPLEMENTED manifest1, scene references image/audio|Complete v3 clips/audio/render job manifest|Do not relabel this as complete v3 inventory|
|Integrity/timeline|`core/bundle_integrity.py:verify_bundle`, `core/timeline_audit.py:audit_timeline`|IMPLEMENTED bundle file checks / warnings|Qualified immutable filesystem snapshots|Reuse timeline; bundle checker not automatically run on arbitrary directories|
|Asset Library|`experimental_mvp/asset_library.py:resolve/resolve_anchor/import_file`|IMPLEMENTED, OWNER_ACCEPTED_WITH_LIMITATIONS|Authenticated rights, idempotent import receipt, cross-resource save CAS|No catalog mutation from CLI; no import/attach bypass|
|MVP-08B|15 reports at base; `MVP_08B_1_ACCEPTANCE.md`|PROPOSED; explicitly NOT_IMPLEMENTED, not approved for implementation|All Dispatcher/JobStore/observer APIs|BLOCKED_DISPATCHER_CONTRACT; empty accepted IDs, exit3|
|Hardware|`core/hardware_profile.py:probe/recommend`, `scripts/check_hardware.py`|IMPLEMENTED passive CPU-first inventory|Qualified per-model runtime/RAM/disk/provider profiles|Pure diagnostic of supplied v1 profile; never execute provider|
|G3 P1|`G3_2_0D_P1_NORMATIVE_CONTRACT.md`, X01-X04 and limited later owner records|CONTRACT_APPROVED only within exact pure-rule scopes; operational work PROPOSED/BLOCKED|Authority/trusted clock/storage/rights/runtime validation|No PG implementation or new grant; no normative edits|
|PG hash domain|P1-05 domain-prefixed canonical envelope vs raw ByteRef|CONTRACT_APPROVED pure distinction|Approved SP-to-PG envelope mapping|SP diagnostic intent hash explicitly NOT PG binding|
|Storage S3 / storage wire|`editorial/storage_protocol_v1.py` (S1 pure wire/MAC), G3 acceptance/qualification limitations|IMPLEMENTED S1 primitives only, not an S3 executor; S3 production qualification BLOCKED|Trusted persistence/authority, publication/recovery/atomicity/permissions|BLOCKED_STORAGE_CONTRACT; no S3 or storage calls|
|Release/editorial suitability|PG discovery/owner decision dossiers|PROPOSED; no approved final release executor|Attestation verifier + human editorial review + final release contract|Pure necessary-condition diagnostics; release_allowed always false|

Status vocabulary is deliberately scoped: IMPLEMENTED is source presence, not qualification; CONTRACT_APPROVED is a narrow documented owner rule; PROPOSED is not approved API; BLOCKED means no safe adapter; NOT_TESTED marks platform/runtime cases not actually executed. Current Linux tests are in IMPLEMENTATION_REPORT; Windows remains NOT_TESTED/WINDOWS_NOT_RUN.

Related exact advertised heads: G1 `28c43eb7670d9f421ad90994529c5b68991a9fc6`; G2 `5b6808b7de7bd7c6746d007e2f7ece455f847131`; G3.1 `8748ad71a30cc0044920f0051830ccf14d858992`; MVP-08A `1ff403e47d35adb34139278de1d056fbbc563e6d`; MVP-08B.1 `f0bce140451bf00a86f3939330e77ed63b2c98be`. Main contains approved G1/G2/G3.1 history; no transfer of deferred PR11 implementation.
