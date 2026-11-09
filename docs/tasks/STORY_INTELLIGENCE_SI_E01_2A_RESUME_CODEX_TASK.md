# CODEX TASK — SI-E01.2a-RESUME: strict typed SI/1 records after approved R1b

**Date:** 2026-11-09  
**Status:** **READY FOR OWNER HANDOFF — BOUNDED IMPLEMENTATION TASK; NOT STARTED**  
**Owner gate:** R1b-P01–P05 **APPROVED**, per `docs/tasks/STORY_INTELLIGENCE_V1_R1B_OWNER_APPROVAL_2026_11_09.md`, approval commit `418becfa88e4e8f5ba4a293247c293988f7d5742`.  
**No PR, merge, release or main changes. STOP after publication.**

## 1. Entry point — mandatory exact-base check

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.

**Source documentation branch:** `docs/story-intelligence-v1-r1b-approval-si-e01-2a-resume`. The owner handoff will supply its **exact final remote HEAD SHA** after this task file is published. **Verify the remote HEAD equals that exact SHA** before creating any feature branch. Do not use the older base `b74d805996e1e9eba65e323f6d1c2995fbb1234f`, the blocked feature commit, `main`, or a moving default branch. If SHA mismatch, STOP and report.

Create a **new** branch from the verified handoff SHA:

`feat/story-intelligence-si-e01-2a-resume-payload-schemas`

Do not reuse, reset, amend, rebase or force-push the historical blocked branch `feat/story-intelligence-si-e01-2a-payload-schemas` (commit `18163478f2204c3dd3d3f9bd742c49ea8253506e`). It remains immutable evidence of `BLOCKED_CONTRACT`. No PR/merge/release or changes to `main`.

## 2. Binding specification and precedence

Read **all** of the following, before editing:

1. `docs/tasks/STORY_INTELLIGENCE_V1_OWNER_APPROVAL_2026_11_09.md` — SI-D01–SI-D10.
2. `docs/tasks/STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md` — original @ `b7bea3aec1fd533973c1e82ad0bd06cf9dd37412`.
3. `docs/tasks/STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md` — R1 @ `978fbed45513a00e851201a9018d17c7da4752be`.
4. `docs/tasks/STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md` — R1a @ `b3f16984edc8daad364f356aa51aeddc2ac0b5b8`.
5. `docs/tasks/STORY_INTELLIGENCE_V1_R1B_REVIEWPACKET_FIELD_PATH_CLARIFICATION.md` — **now approved** R1b @ `5fdd1d8f72ccec37730c8f4c271450e4e95f8de1`, plus its explicit owner approval @ `418becfa88e4e8f5ba4a293247c293988f7d5742`.
6. `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_CONTRACT_GAPS.md` and `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_RESULT.md` @ `18163478f2204c3dd3d3f9bd742c49ea8253506e`: read-only evidence; **do not edit**.
7. `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_CODEX_TASK.md` — previous full bounded assignment, **inherited except superseded entrypoint, allowlist/result filenames and R1b scope in this task**.
8. `docs/tasks/STORY_INTELLIGENCE_SI_E01_1_INDEPENDENT_ACCEPTANCE.md` and accepted SI-E01.1 code/tests @ `61886670fe6d0434df62f6346457f5812f520766`.

**Precedence:** original, then R1's exact overrides, then R1a's exact overrides, then **R1b only for ReviewPacket wire field-path spelling, source/STATE projection mapping, redaction and field ordering**. Do not silently replace other requirements. The product success working reference at `d15cab43849c82f4a880f9fcb772c1c1bfc56622` is **read-only on a separate branch**, not an implementation dependency or permission to merge.

## 3. Bounded goal and public API

Implement exactly the previously scoped **pure, complete, strict local typed record validation** for **all 18 SI/1 RecordTypes** and local byte-derived SIRef identity. New module `story_intelligence/records_v1.py` exports:

- `validate_si_record(value) -> detached plain-value copy`: exact top-level `{H: header, payload: typed payload}`, using accepted `model_v1.validate_header` and strict type-specific closed payload schemas, with all original+R1+R1a+R1b local rules; reject unknown/missing keys, type mismatches, invalid enum/union/nullable forms and self-contained contradictions.
- `si_record_ref(value) -> SIRef plain dict`: validate record first; compute `sha256(C({H,payload}))` using **existing accepted** `codec_v1`; return exact `{type,id,revision,sha256}` from H and digest.
- `validate_si_record_ref(value, expected_ref)`: validate record and ref; compare type/id/revision/hash exactly and fail with approved `SIValidationError` code and meaningful field path; no authority/truth/existence claim.

Implement closed nested value types, including `Known<T>`, `Origin`, `Confidence`, `Criterion`, `Rating`, `Provider`, `ContextSnapshot`, `EvaluationEligibility`, `SelectionScope`, `PrivacyGrant`, `FieldGrant`, `DisplayItem`, `FieldView`, `Omission`, `BriefReviewState`, `PortfolioEntry`, `Chapter`, `ProductionOptions`. Check local rubric weights/criteria, positive durations, locale matching, reviewer-null/qualification, run stage/method/mode, revised EvaluationReport eligibility (not obsolete recommendation), selection/creative-selection ref, R1a initial/edit revision modes and creative originating-run distinction **only as far as local fields permit**. No fake cross-record proof.

**Validation boundary:** a source SIRef shape is an unresolved claim; validating a `FieldGrant` does not establish that the source record exists or that its hash/value/privacy review is authentic. Cross-record resolution, DAG/closure, run-stage binding, history, currentness, idempotency, grant-to-actual-value matching, packet export and operations are reserved for separately authorized SI-E01.2b/later stages. Locally available exact `source_closure_refs` membership and uniqueness/order may be checked where approved; never fetch records or invent absent data.

## 4. Mandatory approved R1b implementation

Apply all **R1b-P01–P05**, not only a regex:

- **P01** `FieldGrant.field_path`, `FieldView.field_path`, `Omission.field_path` use **payload-relative** canonical paths, dot segments, zero-based bracketed decimal indices without leading zeros. Reject `payload.title`, `H.*`, `$.title`, type prefixes, wildcard, negative index, `[00]`, aliases, arbitrary paths, noncanonical spellings. The path must be allowed for the exact `source_ref.type` and view kind; a generic valid string is insufficient.
- **P02** closed TEXT whitelist per approved R1b table: `StoryIdea.title` represented as `title`; `SourceItem.title.value` as `title.value`; `CreativeAlternative.title_options[0]`, `chapters[1].purpose`; other enumerated fields. TEXT non-null, with explicit FieldGrant syntax and matching rules; do not release protected private fields.
- **P03** STATE whitelist with source `EvaluationReport` / `eligibility.state`, `Risk.blocking` ASCII lowercase `true`/`false`, etc. STATE has **no text grant**. `BriefReviewState.review_state/currentness` appear only in `ReviewPacket.payload.review_state_at_capture`, not in DisplayItem, Omission or synthetic SIRef.
- **P04** REDACTED has `text=null`, with exact corresponding Omission `source_ref+field_path`; omission-only closed fields allowed. Header H is excluded from display and omission paths. Sensitive payload fields (e.g. `original_locator`, `reviewer_label`, `selector_label`) may be named only as REDACTED/Omission, never TEXT/STATE. For REDACTED/Omission use **declared payload leaf/whole-Known field vocabulary**, not arbitrary nested objects or free-form paths. Actual source value existence/index and any private-content detection require later resolver/privacy review; structural validation must not pretend to have inspected a missing record.
- **P05** reject duplicate DisplayItems per source_ref, duplicate FieldViews per item path, duplicate FieldGrants and duplicate Omission pairs; enforce approved manifest/schema-field/ascending-numeric-index order for fields/grants/omissions. Do not sort lists silently. Validate local grant/source/path compatibility and required structural matches where all necessary fields are in the same packet; **do not** claim source text/value hashes or privacy authorization verified without the source record. No grant for STATE/REDACTED/projection-only paths.

R1b P-T01–P-T12 are mandatory test cases. **Do not misinterpret** the R1b golden-vector sentence: `title` and `title_options[0]` are TEXT **FieldGrant** examples; `eligibility.state` is a **STATE FieldView** example and must **not** be granted. Provide independently computed canonical bytes/hash for representative `FieldGrant` and `FieldView` values without inventing an unauthorized STATE grant. No invented new error code or privacy profile.

## 5. Exact implementation allowlist — new files only

1. `story_intelligence/records_v1.py`
2. `tests/test_story_intelligence_records_v1.py`
3. `tests/test_story_intelligence_record_vectors_v1.py`
4. `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_RESUME_RESULT.md`
5. `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_RESUME_CONTRACT_GAPS.md` — **optional, only if a genuinely new blocking contract gap is found**.

**Critical collision avoidance:** the old `STORY_INTELLIGENCE_SI_E01_2A_RESULT.md` and `STORY_INTELLIGENCE_SI_E01_2A_CONTRACT_GAPS.md` **already exist** and are frozen. Never overwrite or edit them. If blocked again, write the distinct `_RESUME_` gap and result files, do not fabricate code or claim partial acceptance.

No edits to any other files, including SI-E01.1 modules/tests, original/R1/R1a/R1b contracts, approval note, old task/blocked results, editorial/storage, dependencies/config/CI or `main`. If a shared fix is necessary, STOP and request separately scoped permission.

## 6. Test and publication gates

- At least **12 independent literal complete SI record canonical bytes + SHA-256 golden vectors**, covering representative distinct types and **RunRecord, StoryIdea, CreativeAlternative, EvaluationReport, ProductionBrief, Selection, ReviewPacket**. Expected literals must be generated independently of production `si_record_ref`; use syntactically valid complete H/payload, typed refs, no fictional truth/authority assertion.
- Positive and negative tests for **all 18 types** and nested closed shapes, strict wrong-field/wrong-type/nullable/UNKNOWN/limit cases, exact R1/R1a changes, initial/revision local rules, reviewer requirements, rubric weights, locale/duration, packet grant/field path/STATE/REDACTED/omission/ordering/duplicates and P-T01–P-T12. Verify input immutability and returned detached copy. Tests must distinguish structural local acceptance from unresolved source-record validation.
- Execute `python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v` and `python -m unittest discover -s tests -v` using the project environment. Report exact interpreter/OS, commands, exit status, counts and failures; previous baseline was **31 targeted / 873 full** on Linux, **not** a guarantee of future totals. If full suite cannot run, report BLOCKED_ENV rather than PASS.
- Run `git diff --check`; independently compare expected literal vectors with stdlib JSON/hashlib or another independent implementation; verify exact allowlist and no unrelated changes, clean worktree and remote HEAD after push. Do not claim native Windows qualification or benchmark of worst-case 1 MB integers; SI-F01 remains a nonblocking note.
- Report exact base SHA, final commit/remote SHA, files, additions/deletions, actual tests, known limitations and **structural vs cross-record validation boundary** in the new `_RESUME_RESULT.md`.

## 7. Explicit STOP conditions and exclusions

If a **new** material contract ambiguity prevents complete correct validation, **STOP before implementation or acceptance**, create only `_RESUME_CONTRACT_GAPS.md` and `_RESUME_RESULT.md`, with source sections, minimal competing wire examples and owner choices; do not invent defaults or alter approved decisions.

No persistence/workspace/file I/O in production API, networking, scraping, provider/LLM, GPU requirement, auto-discovery/evaluation/creative, stage dispatcher, execution of `DISCOVER_LOCAL`/`EVALUATE`/`PROPOSE_CREATIVE`/`ASSEMBLE_BRIEF`/`EXPORT_REVIEW_PACKET`/`RECORD_INPUT`/`REVISE_INPUT`, reviewer identity attestation, privacy export, editorial approval, renderer, production handoff, S1/S2/storage authority or Windows VM work. `PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF; S3.2b `BLOCKED_HOST_NOT_PROVIDED`.

Publish **only** the fresh bounded feature branch, no PR/merge/release/main. **STOP** and hand back the exact result for independent review. SI-E01.2b and SI-E02 require **separate** owner gates; do not start them.
