# Diagnostic contract1.1

**SP-INTEGRATION-01b · 2026-11-19 · LIMITED_DIAGNOSTIC_IMPLEMENTATION_CANDIDATE · no execution/release authority.**

Version `SP/1.1-DIAGNOSTIC`; policy `SP-DIAGNOSTIC/1.1`. Runtime: `core/topic_to_film_v1_1.py`; seven new structural schemas: `schemas/topic-to-film-v1-1/`. No central version registry at the verified base prohibits this owner-proposed form; existing contracts use module constants/schema consts. Separate constants, directory and explicit CLI selector provide the migration model. No existing version is changed.

Public pure APIs: prepare_intent, initial_readiness, validate_structure, validate_diagnostic, assess_release. validate_structure is **stage1 only** and cannot recognize a semantically admissible object. validate_diagnostic performs **both** stages and returns a detached diagnostic value or raises ValueError. New failures normally use DiagnosticValidationError(code,path,message); reused SI/plain-value/path validators can raise their existing ValueError subclasses. No success object is an accepted job, proof, permit or receipt.

Structural stage interprets only the fixed keyword profile actually used in these seven repository-owned schemas. Unsupported keywords/kinds fail closed; no $ref/network resolver or user-provided schema loader exists. JSON types are exact plain dict/list/str/int/bool; bounded existing SI codec rejects floats/subclasses/surrogates and caps1MB/32container-depth/100ktext before recursive walking. jsonschema is independent **test tooling**, not a new runtime dependency. This helper is not a general JSON Schema implementation. Full JSON Schema engine parity is asserted only for the pinned structural profile and tested strict-value corpus; domain bounds/semantic checks are additional mandatory constraints.

Semantic stage validates the route/input/stage/hash/blocker relations, material scope/paths, typed SI/E references through existing model_v1 validators, unique artifact roles and nonblank blockers. Schemas deliberately leave filesystem/path and cross-field checks to stage2; schema success alone remains insufficient. Raw byte declarations are not fetched or authenticated.

## Intent

Exactly one primary input: nonblank topic→A, nonblank script→B, validated scene plan→C, scene plan+complete declared supported material map→D. Locale ru/uk;1..20 scenes; text1..2000 meaningful characters; optional meaningful title. New plan/scene structural objects reject extra fields; they remain the First Video dialect, not experimental storyboard conversion.

Ordered stage lists remain exactly legacy ROUTES: A script.draft/plan.from_script/plan.validate/assets.voice/assets.images/render.mp4/gates.technical; B omits script.draft; C begins plan.validate; D plan.validate/render.mp4/gates.technical. Unknown/extra/duplicate/missing/reordered stages are invalid. This is validation of a finite list, not a DAG scheduler/type registration.

Diagnostic status must be BLOCKED_DISPATCHER_CONTRACT; accepted_job_ids must be []; generated blocker list must be preserved exactly, including authority/storage blockers and route A production/fallback additions. No readiness or flag can remove those job-preparation blockers.

intent_sha256 is lowercase exact64hex SHA256 of existing canonical_si_json over BODY_FIELDS: schema_version,policy_version,route,mode,fallback_class,inputs,requested_attestations,proposed_job_types. Own digest/status/blockers/IDs excluded. Version/policy enter the bytes. No normalization, no PG domain substitution, no JobStore key/idempotency claim. Hashes and related UUID patterns use strict end `(?![\s\S])`, not terminal `$` acceptance. New runtime reuses existing fullmatch hash/ref validators as applicable.

## Supported material declarations

Route D accepts exactly voiceN/imageN for every scene1..N. Each scene must explicitly name its image; voiceN path is voiceN.wav, imageN path equals scene.image. Material role must match map key; no missing/extra/clip/provider/file URL roles. Voice is local PCM-WAV profile only; PNG/JPG/JPEG/PPM images follow existing pure plan/safe_image contract. This deliberately bounded prepared-material profile does not claim arbitrary MP3/clip/experimental-storyboard support. Those routes require a separate contract; unsupported inputs are rejected rather than silently converted or regenerated.

Paths use core.media_paths.validate_media_path; transport requires returned canonical portable relative string equal to supplied string. No second path parser is added. Plan image rules reuse legacy.validate_plan. Actual read-only gates reuse read_plan,safe_image,wav_ms,Project and timeline through existing observer. Pure intent checks do not access materials or establish bytes/rights; CLI does not resolve the declared map into execution inputs.

## Readiness and necessary conditions

All full schema fields required, including schema/policy, six axis strings, fallback_class,si_eligible,release_allowed,blockers,evidence_refs,artifact_bindings. Flags initially leave all axes/SI unknown. Existing SI/ERef structure validation does not establish closure, currentness, provenance authenticity or authority. Empty refs/bindings explicitly mean no evidence supplied; no fake required attestations are generated.

assess_release first performs both readiness stages. Missing/old/malformed objects produce necessary=false with INVALID_READINESS. Necessary=true requires full admissible1.1 object, production mode, all six axis strings true, no blockers, fallback none, bindings_current and creative_review supplied as true. Equivalent/degraded/placeholder remain unqualified here. These additional assertions are still unverified diagnostics. A full user-supplied all-true record with empty evidence can satisfy these **asserted diagnostic conditions**; it proves no underlying rights, currentness, human identity or suitability. There is no evidence minimum or trusted-attestation profile approved by this task to invent.

Always release_allowed=false, status=BLOCKED_CONTRACT, blockers include BLOCKED_ATTESTATION_VERIFIER and BLOCKED_RELEASE_CONTRACT. No permission is issued, including when necessary=true. Draft never meets production prerequisite. MP4/technical/ SI success cannot promote facts/rights/release.

Other transport artifacts (route/jobs/manifest/gate/report) require their fixed closed shapes and applicable semantic checks. A route projection cannot by itself prove agreement with another artifact; no aggregate storage transaction or result verifier is created. Fresh gate observations are labeled1.1 by explicit adapter, not by accepting/relabeling stored SP/1 objects. Final gates still technical unknown/blocked.
