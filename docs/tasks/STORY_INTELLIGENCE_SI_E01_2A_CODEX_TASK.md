# CODEX TASK — SI-E01.2a: pure typed SI/1 payload schemas and record identity

**Date:** 2026-11-09. **Status:** bounded next-task handoff only. **No PR/merge/main.** Work is subject to the owner forwarding this task to Codex. The owner approved SI-D01–SI-D10; this does not approve code outside the bounded task.

## Starting point and sources

Repo: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Source branch: **`docs/story-intelligence-si-e01-1-independent-review`**.
Codex must verify this branch remote HEAD equals the **exact SHA supplied in its handoff** before changes. STOP if not equal; do not switch silently to `main`.
Create **`feat/story-intelligence-si-e01-2a-payload-schemas`** from exact source SHA. No rebase/force, PR/merge/release/main changes.

Binding approved composite (read-only):
- `docs/tasks/STORY_INTELLIGENCE_V1_OWNER_APPROVAL_2026_11_09.md`.
- `docs/tasks/STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md` @ `b7bea3aec1fd533973c1e82ad0bd06cf9dd37412`.
- `docs/tasks/STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md` @ `978fbed45513a00e851201a9018d17c7da4752be`.
- `docs/tasks/STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md` @ `b3f16984edc8daad364f356aa51aeddc2ac0b5b8`.
- `docs/tasks/STORY_INTELLIGENCE_SI_E01_1_INDEPENDENT_ACCEPTANCE.md`, and the SI-E01.1 source/test/RESULT at `61886670fe6d0434df62f6346457f5812f520766`.
- Product success working reference (read-only, **separate branch**, no cherry-pick): `docs/tasks/STORY_INTELLIGENCE_V1_PRODUCT_SUCCESS_CRITERIA_2026_11_09.md` @ `ed1630140a6b9a7089ef04e1c926019c3cb74ed6`.

Precedence: original specification except precise R1 overrides, then precise R1a overrides. Don't introduce new policy from an example alias. Inspect actual existing model/editorial contracts read-only. Where a required field/type remains genuinely ambiguous, STOP and report a bounded contract issue instead of silently inventing a field/default. No unauthorized contract amendment.

## Goal: strict local validation of complete recorded SI objects

Implement **pure typed payload schemas**, field-level semantic checks, and SI record identity primitives based on the already approved 18 RecordTypes. **Every record type** from the approved composite must have a closed payload shape (including amended R1 EvaluationReport, RunRecord, Selection, ProductionBrief with creative_selection_ref, ReviewPacket). Add subtype validators for all nested value types and their versioned fixed enums.

Do not resolve external refs, validate existence of other records, infer facts/rights, execute stage operations, persist records or implement run/selection currentness here. Local `SIRef` shape validation is not proof of content hash or material provenance.

## Exact scope and public APIs

New file **`story_intelligence/records_v1.py`** exports:
- `validate_si_record(value) -> detached plain-value copy`: full strict record shape, using representation **`{H:header, payload:typed payload}`** (matching existing illustrative C(H+payload)); reject unknown/missing fields, wrong type/primitive and local inconsistent fields. Use `model_v1.validate_header` plus record-specific payload checks. `H` exact typed header, no extra fields. No speculative ref resolution.
- `si_record_ref(value) -> SIRef plain dict`: only after `validate_si_record`, SHA256 of **exact `C({H,payload})`** from accepted SI-E01.1 `codec_v1`, returning `{type,id,revision,sha256}`. This attests bytes/shape only, not truth, authority, writer identity or ref existence.
- `validate_si_record_ref(value, expected_ref)`: validate both, compare exact computed SIRef against supplied ref; refuse wrong type/id/revision/hash with stable R1 error code/path (use `REF_HASH_MISMATCH` and `REF_TYPE_MISMATCH` if appropriate). No claim of attached external material hash verification.

Nested records and fields: implement **all** approved original §3 payloads with R1/R1a overrides, including `ProductionOptions`, `Criterion`, `Rating`, `Provider`, `ContextSnapshot`, `EvaluationEligibility`, `SelectionScope`, `PrivacyGrant`, `FieldGrant`, `DisplayItem`, `FieldView`, `Omission`, `BriefReviewState`, `PortfolioEntry`, `Chapter`, `Origin`, `Known<T>`, `Confidence`. Apply explicit local constraints: rubric criterion keys/weights, well-typed known-vs-unknown, chapter time positive, brief min<=max and RU/UK alignment, ClaimCheck reviewer metadata rules, RunRecord local stage/method/mode, valid Selection scopes/target types, packet purpose/format/grant/profile/technical label, exact field namespace, no unknown fields or implicit defaults. Do not assert human identity or grant validity beyond structure.

Treat `UTC` as descriptive UTC seconds (not an ordering proof), bool never int, typed refs only, no implicit latest. Retain SI-E01.1 single-record size/text/depth bounds, no bundle storage or inherited S1 authority. The approved `Code` vocabulary must be used for surfaced SIValidationError. On undecided local semantics (e.g. whether a specific source snapshot has verified human evidence), validate syntax only and leave cross-record proof to next stage.

**IMPORTANT consistency boundary:** validate_si_record checks **local self-contained structure**. Do not mistakenly reject a valid RunRecord merely because referenced objects aren't available, and do not mark an unresolved SIRef as cryptographically verified. Do not add new RunRecord stages, disallow reserved MODEL_DERIVED from the general model except where an explicit V1 record rule forbids it, or promote a human label into an authorization.

## Exact allowlist — five NEW files only

1. `story_intelligence/records_v1.py`
2. `tests/test_story_intelligence_records_v1.py`
3. `tests/test_story_intelligence_record_vectors_v1.py`
4. `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_RESULT.md`
5. `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_CONTRACT_GAPS.md` — **create only if genuine blocking ambiguity is found**, rather than solving it by unapproved policy.

No edits to accepted SI-E01.1 source/tests, original/R1/R1a documents, storage/editorial, dependency/config, other docs, CI or `main`. If this scope needs shared bug fixes, STOP, report exact evidence and request separate permission; do not expand allowlist. If blocking contract ambiguity prevents implementing an accurate full type, prefer **BLOCKED_CONTRACT** with evidence and no partial acceptance claim; no fabricated test PASS.

## Required tests and evidence

- At least **12 independent literal record bytes+hash vectors** covering representative distinct SI record types (including RunRecord, StoryIdea, CreativeAlternative, EvaluationReport, ProductionBrief, Selection and ReviewPacket); literals independently generated without using the production `si_record_ref` in expected-value generation. All expected refs use syntactically valid UUIDs/hashes and obey local typed schemas. Do not use ambiguous or illustrative placeholder record claims as verified facts.
- Positive/negative table-driven tests for **all 18 types** and nested closed value shapes; R1/R1a override cases; ClaimCheck qualifications/reviewer-null rules; ProductionBrief language/duration; rubric weights/UNKNOWN; technical labels; incorrect packet privacy grant shape; wrong hash/ref; unknown fields; limit/depth; exact source/typed-ref shape. Assert no input mutation.
- Test with `unittest`, stdlib only; no network/models/storage. New tests should be proportionate to this pure stage and not require 56 domain acceptance outcomes.
- Execute targeted `python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v` and full `python -m unittest discover -s tests -v`, record actual counts, environment and any baseline failures. Compare old SI-E01.1 31 tests and previously reported full suite 873 (do not assume new total without observing). Independently check byte/hash expected values and compare canonical SI vs existing S1 in tests only where applicable.
- Run `git diff --check`; verify exact allowlist, source/base/remote SHA and clean worktree; report no benchmark claim for 1MB integers unless actually measured. SI-F01 from prior acceptance remains nonblocking but carry forward.

## Prohibited actions / STOP

No standalone UI, importer, persistence, file I/O, network/crawling, provider calls, GitHub-generated media, ID/clock generation inside pure APIs, renderer or production export. No executable `DISCOVER_LOCAL`, `EVALUATE`, `PROPOSE_CREATIVE`, `ASSEMBLE_BRIEF`, `EXPORT_REVIEW_PACKET`, `RECORD_INPUT` or `REVISE_INPUT` operations yet. No authoritative editorial writes, S1/S2 modifications, Windows native LAB work, license gates bypass.

Publish only the bounded feature branch and result, with exact files/base/commit, counts, validation boundary, unresolved issues. STOP after publication. **SI-E01.2b** (pure reference-resolution DAG, method-stage/ancestry and operation prerequisites) will require another independent review and a new task. **SI-E02** product work follows later gates, not automatic approval from this task.
