# SI-PRODUCT-02.2.2 — Editor Input → Private Card + RU/UK Plan Preview

Implementation scope: PREVIEW_ONLY. Independent review pending; no production authorization.

## Identity and scope

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Exact base/commit parent: `6ecc263ff4eefd5d6c419c36f8ad215540a1e6a4`.
- Branch: `feat/si-product-02-2-2-editor-preview`.
- Result commit: the commit containing this report; full SHA is provided in the
  external handoff/ZIP identity (a commit cannot embed its own SHA).
- New files: `scripts/editor_preview.py`, `tests/test_editor_preview.py`,
  `examples/editor_input_example.json`, `examples/editor_input_incomplete.json`,
  this report. Existing `project-log/WORKLOG.md`: append-only entry.
- Evaluator, Projection, SI/1, A14, D1 permit/generator/renderer/tests, Storage,
  TTS, FFmpeg renderer, dependencies and CI workflow remain unchanged.

## Local command

```text
python scripts/editor_preview.py examples/editor_input_example.json --output-dir output/editor-preview
python scripts/editor_preview.py examples/editor_input_incomplete.json --output-dir output/editor-preview-incomplete
```

Use a new output directory for each run. Existing directories/symlinks are
rejected instead of mixing new data with old evaluation/cards/plans. Parent
folders may be created. All completed artifacts are staged together and renamed
into the requested directory only after `first_video.read_plan` validates every
complete plan. This is a local preview export, not a protected/transactional
production writer or a concurrent-writer/power-loss guarantee.

Exit 0 means a diagnostic preview was written, including NEEDS_INPUT cases;
exit 2 means CLI/I/O/export failure. The console prints only the adapter state
or a fixed error code, never an input filename, exception text or private fragment.

## EditorPreviewInputV1

UTF-8 JSON, unique keys at every depth; no float/NaN/Infinity, surrogates or
non-JSON objects. Maximum input 2,000,000 bytes, nesting 64, integer magnitude
bit length at most 64. No input repairs, normalization or coercion.

Closed top-level keys:

| Field | V1 shape |
|---|---|
| `schema_version` | Exact string `EditorPreviewInputV1` |
| `purpose` | Exact string `PREVIEW_ONLY` |
| `topic` | `{id, text, source_locale}`; nonempty id ≤200 chars, theme ≤2000, locale `ru`/`uk` |
| `audience` | `{description}`; nonempty description ≤4000 chars |
| `evaluation_inputs` | Actual existing evaluator invocation dictionary |
| `scene_drafts` | Object with only optional `ru`, `uk` entries; each `{title?, scenes?}` |
| `materials` | List of `{id, description, kind, rights_status}` |

Sections not yet supplied may be omitted or null. A partially formed typed
metadata object is diagnosed rather than silently completed. Missing/null scenes
or scene text remain partial drafts. No implicit UNKNOWN record, fabricated
rating, finding, evidence, context, SI record, translation or human decision is
inserted into existing schemas. `materials: []` explicitly declares no provided
materials; it does not mean that no materials or rights checks will be needed.

Evaluator invocation has exactly the existing six required named fields:
`records`, `semantic_input_refs`, `observed_context`, `ratings`,
`expected_context`, `human_findings`. Their top-level types must be respectively
list/list/dict/list/dict/dict; missing/null arguments or wrong container types
prevent invocation. Only existing optional `required_current_premise` and
`ui_locale` are accepted. Values are passed unchanged to the existing evaluator;
its structural, exact-ref, provenance, currentness and findings validation remains
authoritative for SI validity. Merely supplying all arguments does not mean they
will pass that validation.

Topic/audience metadata describes what the editor supplied. It is not converted
into SI records and does not replace or authenticate the actual SI Idea/Audience
inside evaluation_inputs. Metadata and the embedded SI graph must be reviewed
for relevance by the editor; this adapter does not invent a semantic alignment.

## Three independent states

1. **Input completeness**: `sections`, `input_completeness` and `adapter_state`.
   Adapter NEEDS_INPUT is separate from evaluator eligibility NEEDS_INPUT.
   INPUT_COMPLETE means the adapter-format sections were supplied; it is not
   accepted SI validity, rights clearance, creative eligibility or production readiness.
   Unknown/malformed/missing data receive closed RU/UK diagnostic codes and actions.
2. **Actual SI evaluation**: NOT_RUN, FAILED, or the actual OK/INVALID/STALE result.
   Missing metadata can coexist with a real evaluation if the separate SI invocation
   is complete. Missing ratings/findings never invoke evaluator or Projection.
   `evaluation.json` contains the actual evaluator result. Each diagnostic is
   exported by its code alone. Projection receives the original result in memory.
   Real INVALID/STALE include `eligibility: null` and `aggregate_tenths: null`;
   neither is converted into a rejection score or accepted eligibility.
   INVALID retains its evaluation file and safe corrective diagnostic, but creates
   no card and does not call Projection. STALE is passed to real Projection for
   its existing freshness explanation, not turned into an eligibility decision.
   For OK, the existing `project_evaluation` is called independently for RU/UK,
   including its required evaluator re-verification. UNAVAILABLE/exception creates
   no card file; the absence and reason are explicit in preview-status.
3. **Production**: always `NOT_ASSESSED`, `permissions_granted: false`, with all
   six bilingual future checks from the task. No existing enum is changed.

Diagnostic vocabulary is closed in the adapter's TEXT catalog. Diagnostics contain
only fixed code/section/locales, material index and controlled RU/UK explanations
and actions, not user identifiers, raw paths, material descriptions or private
exception messages. The evaluation export and authored draft/plan files remain
private. Only the diagnostic codes are exported from the evaluator's diagnostics,
since SI paths can contain editor-supplied keys. No diagnostics/text are routed
into Projection as fabricated findings.

## Plans, rights and binding

A complete draft contains 1–20 scenes with exact nonempty texts ≤2000 characters;
optional image names must be simple filenames, not paths/URLs. Optional title and
all authored scene text, Unicode composition and whitespace are preserved exactly.
The generated `{locale, title?, scenes}` is checked with existing read_plan.
A full plan is labelled DRAFT_PLAN_VALID only, never APPROVED/READY_TO_RENDER.
Locale tags and format validation do not establish that authored text is actually
in the tagged language or factually correct; exact human text approval is still required.
A partial draft is exported separately as `draft-ru.json`/`draft-uk.json`; it is
not a plan. A missing locale gets no file/translation. Malformed draft structures
are diagnosed and not passed off as complete plans.

Materials accept UNKNOWN, PENDING_REVIEW, REPORTED_BY_EDITOR and
VERIFIED_EXTERNALLY only as editor-reported information. Unrecognized/missing
values are safely diagnosed as unknown without echoing arbitrary input. A safe
indexed materials summary preserves the reported state; grants_permission is
always false. VERIFIED_EXTERNALLY is never automatically promoted or treated as
verified policy evidence/permission. The exact materials/usage still need future
rights evaluation; no A14, D1 or production authority is conferred.

`input_sha256` binds canonical JSON values (including exact authored strings and
all supplied SI inputs); `source_sha256` additionally binds exact source bytes.
Changed values have a different binding. Neither digest authenticates an editor,
is an approval, nor permits reuse of an older preview for changed inputs.
For malformed JSON the canonical input hash is null; an exact source-byte hash
is retained only when the entire bounded source was read. Oversize partial reads
are never claimed as exact whole-file hashes.
No outputs from a previous directory are reused. No persistence/authority store
or protected snapshot is written.

Files are created with private POSIX directory mode 0700 / file mode 0600 where
supported. On Windows these mode bits do not establish NTFS ACL qualification;
the editor must choose an appropriately private local output directory. This
module is not a protected Windows service or a new authorization system.

## Examples and evidence

Full example: explicitly synthetic editor metadata, unchanged registered D1 SI
fixture inputs and authored RU/UK scene texts. It contains no render permit,
media, audio or production grant. Reusing synthetic SI data does not transfer D1
permission into this adapter. It demonstrates structure, not scientific evidence,
rights verification, audience demand or a real researched story.

Incomplete example: the question “Почему исчезли древние цивилизации?”, no
submitted audience/evaluation, a partial RU draft, no UK translation and an
UNKNOWN material. This is an editor question, not a historical finding.

Actual CLI smoke outputs are provided in the external evidence ZIP:
- full-preview: `preview-status.json`, `evaluation.json`, `private-card-ru.json`,
  `private-card-uk.json`, `plan-ru.json`, `plan-uk.json`;
- incomplete-preview: `preview-status.json`, `draft-ru.json`, no evaluation/card/UK plan.

## Verification

Execution on Linux before the diagnostic export correction (full commands/streams/exit metadata in the original evidence ZIP):

| Python | Check | Count | Failures/errors/skips | Exit | Wall seconds |
|---|---|---:|---|---:|---:|
| 310 | target | 19 | 0/0/0 | 0 | 15.689 |
| 310 | compile | n/a | n/a | 0 | 0.027 |
| 310 | unittest | 1156 | 0/0/0 | 0 | 1416.850 |
| 310 | pytest | 1169 | 0/0/0 | 0 | 1386.683 |
| 313 | target | 19 | 0/0/0 | 0 | 12.299 |
| 313 | compile | n/a | n/a | 0 | 0.029 |
| 313 | unittest | 1156 | 0/0/0 | 0 | 1031.764 |
| 313 | pytest | 1169 | 0/0/0 | 0 | 1036.942 |

Additional executed pytest subtests (not added to the method/test counts): {"310": 6147, "313": 6147}.

Commands (each venv Python separately):

```text
python -m unittest tests.test_editor_preview tests.test_topic_to_video_d1 -v
python -m compileall -q scripts tests
python -m unittest discover -s tests -v
python -m pytest -q tests
git diff --check
```

Python 310 = CPython 3.10.22; Python 313 = CPython 3.13.5. pytest 9.2.0; exact environment/package versions in the corresponding environment logs. Target count is 16 new + 3 unchanged D1 tests. Repeated full suites overlap and are not summed as unique tests. Both complete unittest and complete pytest ran on each Python version. No source changes after the frozen tested-source hash snapshot.

Remote GitHub Actions: NOT_RUN. The existing workflow remains unchanged with Python 3.10/3.13 and both test commands. The local matching matrix above is compatibility evidence, not a claim of an executed GitHub job. No push or PR was performed.

Final scoped diff checks and staged diff check passed (exit 0); exact six paths verified before commit. All existing source/contract/test files other than the append-only WORKLOG are unchanged. Final working tree is checked clean after local commit.
The existing GitHub workflow already declares both versions and discovers the
new tests in both unittest and pytest. Remote GitHub Actions execution must not
be inferred from local matrix execution; any unrun remote CI is reported as NOT_RUN.

New suite: 16 tests, including full real cards/plans, missing audience, absent/null
ratings/findings, real INVALID, real STALE, unavailable Projection, missing UK,
partial draft exact retention, all four rights statuses and malformed values,
changed binding/determinism/nonmutation, closed schema, invalid plans, private
write/read_plan/no reuse, malformed JSON, failure privacy/staging and CLI safety.
All new tests guard build, renderer, Silero synthesize, subprocess, sockets,
HTTP and WAV creation and assert zero calls. Successful paths use genuine evaluator
and Projection results; mocks inject failures or wrap real calls only.
Existing unchanged D1 tests run separately and exercise their previously authorized
synthetic FFmpeg/WAV path, not the new preview adapter.

The initial new test run failed two assertions which incorrectly expected the
eligibility key to be absent for INVALID/STALE. Actual evaluator returns null;
only the new assertions were corrected to its real format. Evaluator/Projection
were not changed. Initial and corrected logs remain in external evidence.

A subsequent local review corrected malformed-JSON fingerprint reporting: no
canonical hash of a sentinel is emitted. A regression assertion verifies null
canonical hash and the exact raw-byte hash for bounded malformed inputs. The
intermediate full run was interrupted for this correction and is explicitly
marked INTERRUPTED in evidence, not counted as PASS; final matrix runs started
after the change.

## Boundaries

No build call (including render=False), new WAV/MP4/production project, TTS/network
integration, automatic research/translation, production readiness computation,
protected storage, new dependencies or existing contract changes in the adapter.
No SI-PRODUCT-02.3 work, merge, release, tag or main modification.

STOP after the implementation handoff for independent review.
