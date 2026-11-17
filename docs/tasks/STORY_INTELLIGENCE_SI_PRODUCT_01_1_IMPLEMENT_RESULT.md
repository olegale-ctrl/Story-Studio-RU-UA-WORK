# SI-PRODUCT-01.1 — Editorial Decision Projection V1 implementation result

Дата: 2026-11-13 (Europe/Kyiv). **STATUS: READY_FOR_INDEPENDENT_REVIEW.**
Qualification: PURE_PRIVATE_DECISION_PROJECTION_ONLY; independent acceptance pending.
Owner implementation authorization separately granted in chat for this exact scope.

## 1. Git and immutable scope

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Feature: `feat/story-intelligence-si-product-01-1-projection-v1`.
Exact base / single parent of the implementation commit:
`f56f4ea2a7c7584a6b8b8c236d0b4a54e946485d`.
Approved reference ancestry: `f56f4ea2` → `5e0ddf45aacb2412dd15b9a4923acb40c6a6c7bd`
→ evaluator foundation `35451f6441bd5428e132ae65f2080209b51fe009`.
Preflight: exact base present, clean worktree, no unmerged paths, target branch new;
owner approval/contract/oracles/draft read. PD-01–PD-08 and conditions PD-01/PD-05
preserved. Source/main/archive branch not substituted. Implementation commit SHA and
final clean-tree evidence are supplied in the handoff after commit (no self-SHA embedded).

Only authorized changes:

| Path | Change |
| --- | --- |
| `story_intelligence/decision_projection_v1.py` | New pure module, frozen RU/UK vocabulary, real evaluator re-verification, exact selector matching and deterministic Card |
| `tests/test_story_intelligence_decision_projection_v1.py` | New executable P01–P42, genuine negative/status/purity witnesses and external performance harness |
| `tests/test_story_intelligence_decision_projection_oracles_v1.py` | New 30×2 executable matrix/variants, independent literal catalog expectations and full literal W01 cards |
| `docs/tasks/STORY_INTELLIGENCE_SI_PRODUCT_01_1_IMPLEMENT_RESULT.md` | This report |
| `project-log/WORKLOG.md` | Append-only entry |

No existing evaluator/SI/1/test/config/approved-contract changes. No new dependencies.
The generated constants are literal approved-specification data; runtime does not
read Markdown/files or use test helpers. Expected test strings are independent
literal specification copies, not imported from renderer internals/output.

## 2. Public API and behavior

```python
project_evaluation(evaluation_inputs=None, evaluation_result=None, display_locale=None)
```

Invocation frame: six required evaluate_si arguments; only optional
required_current_premise/ui_locale may be omitted with existing None defaults.
Explicit display_locale ru/uk, independent of evaluator locale. Unsupported locale
returns exactly `{availability:UNAVAILABLE}`. Other admission failure with a valid
locale returns the full approved UNAVAILABLE Card with U0/A0 and six limitations.
No invented evaluator status/reason code/authority or repaired result.

PD-01: every otherwise admissible call invokes the unchanged real evaluator with
copied exact invocation values. Canonical supplied/recomputed result bytes must match;
no cache, trusted flag, digest-only acceptance, replacement result or shortcut.
Unsupported object hooks are rejected before copying/looking up untrusted keys;
malformed builtin data producing genuine evaluator INVALID can be safely explained.
Only failure-injection tests replace evaluator with an exception; every successful
Card executes the real evaluator. A real-call wrapper proves two repeated calls
cause two verifications. Exception text/diagnostics are never logged or echoed.

Actual status/result shapes retained: OK with nested eligibility/codes, or STALE/
INVALID with null eligibility/score and top-level codes. Closed 30-family selector
uses code/path/exact typed subject/static emitter and exact invocation context.
Code EVIDENCE_NEEDED alone does not determine severity. All slots/ordering/gaps/actions
survive; private refs/hash/path/Text are replaced by fixed aliases/criterion labels.
Every Card has five sections and six fixed limitations. Scores stay exact integer
or UNKNOWN; no new thresholds, probability, scientific claim, rights grant or job.
Result detached; no mutation, clock, I/O, network/provider, UI, persistence or cache
in the production module. Benchmark clock/environment reads live only in test harness.

## 3. Executed 30-family × 2-locale matrix

Actual successful slots from test-run coverage output; no missing family/locale.
Matrix has 30 collected methods, 60 unique family/locale slots, and **146** successful
Projection calls after severity/path/C05 expansions. These are different counts.
Risk expansions: 6 categories × 4 severities × 2 paths × 2 locales = 96 calls.
C05 covers both central and noncentral relation conflicts. Existing evaluator suite
alone is not used as Projection evidence.

| Family | RU | UK | Executable test |
| --- | --- | --- | --- |
| RC01 | PASS | PASS | `FamilyLocaleMatrix.test_family_RC01` |
| RC02 | PASS | PASS | `FamilyLocaleMatrix.test_family_RC02` |
| RC03 | PASS | PASS | `FamilyLocaleMatrix.test_family_RC03` |
| RC04 | PASS | PASS | `FamilyLocaleMatrix.test_family_RC04` |
| RC05 | PASS | PASS | `FamilyLocaleMatrix.test_family_RC05` |
| RC06 | PASS | PASS | `FamilyLocaleMatrix.test_family_RC06` |
| RC07 | PASS | PASS | `FamilyLocaleMatrix.test_family_RC07` |
| RC08 | PASS | PASS | `FamilyLocaleMatrix.test_family_RC08` |
| RC09 | PASS | PASS | `FamilyLocaleMatrix.test_family_RC09` |
| C01 | PASS | PASS | `FamilyLocaleMatrix.test_family_C01` |
| C02 | PASS | PASS | `FamilyLocaleMatrix.test_family_C02` |
| C03 | PASS | PASS | `FamilyLocaleMatrix.test_family_C03` |
| C04 | PASS | PASS | `FamilyLocaleMatrix.test_family_C04` |
| C05 | PASS | PASS | `FamilyLocaleMatrix.test_family_C05` |
| K01 | PASS | PASS | `FamilyLocaleMatrix.test_family_K01` |
| K02 | PASS | PASS | `FamilyLocaleMatrix.test_family_K02` |
| K03 | PASS | PASS | `FamilyLocaleMatrix.test_family_K03` |
| K04 | PASS | PASS | `FamilyLocaleMatrix.test_family_K04` |
| K05 | PASS | PASS | `FamilyLocaleMatrix.test_family_K05` |
| K06 | PASS | PASS | `FamilyLocaleMatrix.test_family_K06` |
| V01 | PASS | PASS | `FamilyLocaleMatrix.test_family_V01` |
| Q01 | PASS | PASS | `FamilyLocaleMatrix.test_family_Q01` |
| Q02 | PASS | PASS | `FamilyLocaleMatrix.test_family_Q02` |
| Q03 | PASS | PASS | `FamilyLocaleMatrix.test_family_Q03` |
| Q04 | PASS | PASS | `FamilyLocaleMatrix.test_family_Q04` |
| F01 | PASS | PASS | `FamilyLocaleMatrix.test_family_F01` |
| F02 | PASS | PASS | `FamilyLocaleMatrix.test_family_F02` |
| F03 | PASS | PASS | `FamilyLocaleMatrix.test_family_F03` |
| F04 | PASS | PASS | `FamilyLocaleMatrix.test_family_F04` |
| F05 | PASS | PASS | `FamilyLocaleMatrix.test_family_F05` |

## 4. P01–P42 and W01

Every row below executed in the new Projection suite. Nested old test cases are
additional parameterized witnesses, not extra collected unittest methods.

| Requirement | Result | Executable test |
| --- | --- | --- |
| P01 | PASS | `test_P01_eligible_literal_card` |
| P02 | PASS | `test_P02_needs_input` |
| P03 | PASS | `test_P03_unknown_score` |
| P04 | PASS | `test_P04_unresolved_portfolio` |
| P05 | PASS | `test_P05_duplicate_is_not_reject` |
| P06 | PASS | `test_P06_blocked_at_max_score` |
| P07 | PASS | `test_P07_actual_stale` |
| P08 | PASS | `test_P08_actual_missing_ref` |
| P09 | PASS | `test_P09_invalid_evidence_is_not_research` |
| P10 | PASS | `test_P10_invalid_rights_is_not_eligibility` |
| P11 | PASS | `test_P11_permitted_hypotheses` |
| P12 | PASS | `test_P12_numbers_no_new_threshold` |
| P13 | PASS | `test_P13_RC_and_existing_C01_C48_projection` |
| P14 | PASS | `test_P14_full_kind_materiality_review_matrix` |
| P15 | PASS | `test_P15_risk_variants_no_text_inference` |
| P16 | PASS | `test_P16_C14_full_composition` |
| P17 | PASS | `test_P17_C44_preserves_source2_gap` |
| P18 | PASS | `test_P18_editorial_and_findings_families` |
| P19 | PASS | `test_P19_nine_confidence_findings_remain_distinct` |
| P20 | PASS | `test_P20_three_pairs_and_repeated_candidate` |
| P21 | PASS | `test_P21_T25_full_literal_as_W01` |
| P22 | PASS | `test_P22_condition_removal_does_not_clear_others` |
| P23 | PASS | `test_P23_invalid_eref_outranks_stale` |
| P24 | PASS | `test_P24_historical_only_eref_not_promoted` |
| P25 | PASS | `test_P25_sixteen_genuine_fatal_code_witnesses` |
| P26 | PASS | `test_P26_missing_and_unsupported_values` |
| P27 | PASS | `test_P27_locale_no_fallback` |
| P28 | PASS | `test_P28_language_does_not_change_evaluation` |
| P29 | PASS | `test_P29_closed_result_shapes` |
| P30 | PASS | `test_P30_reverification_detects_each_tamper_and_changed_findings` |
| P31 | PASS | `test_P31_unknown_codes_and_verified_flags` |
| P32 | PASS | `test_P32_human_reason_private_not_displayed` |
| P33 | PASS | `test_P33_rebuilt_private_metadata_no_leak` |
| P34 | PASS | `test_P34_private_unknown_key_float` |
| P35 | PASS | `test_P35_no_diagnostic_html_or_message_echo` |
| P36 | PASS | `test_P36_same_source_identity_two_revisions_not_merged` |
| P37 | PASS | `test_P37_deterministic_dictionary_order_and_bytes` |
| P38 | PASS | `test_P38_exact_unicode_private_reasons` |
| P39 | PASS | `test_P39_result_detachment` |
| P40 | PASS | `test_P40_long_lists_preserve_every_slot` |
| P41 | PASS | `test_P41_recorded_basis_not_real_clearance` |
| P42 | PASS | `test_P42_external_approval_not_inferred` |

Additional details:

- P13 executes all 48 existing RC oracle cases. 46 cases also invoke Projection;
  C20/C21 remain accepted-currentness boundary-only witnesses, as in their contract.
  C22 additionally tests genuine eligible proof-graph Projection repeat/detachment.
- P14 projects every one of 81 kind/materiality/review fixtures in RU and UK, plus
  independent supported/disputed conflict. P15 and matrix cover required Risk paths,
  severities, nonblocking/mitigation cases without keyword inference.
- P16/P17 preserve generic LEGAL and specific Visual rights plus required-current
  input/research diagnostics (C14/C44). P19 retains all nine confidence slots; P20
  preserves per-entry comparisons even with one repeated exact candidate.
- P25 constructs genuine evaluator INVALID witnesses for all 16 cataloged fatal
  codes in RU/UK. Inherited privacy failures are record-validation failures, not
  scientific verdicts. They are not forged accepted result dictionaries.
- P30 tests every result-field tamper/missing blocker/changed finding, real-call
  wrapper without caching, and injected recomputation exception. P32–P35 capture
  output and verify no private text/key/path/message echo.
- P36 uses two exact Source revisions with one identity in a genuine valid declared
  view: aliases remain distinct. P40 retains 30 simultaneous conditions, including
  eight blocking Risks, thirteen source gaps and nine confidence gaps, without top-N.
- `LiteralWorkedExample.test_W01_full_RU_UK`: complete exact Card dictionaries in
  both languages, including summary, all reasons/actions, order and all limitations.
  Fixture record count=17; independent records/ratings SHA-256 match the approved
  literal values. T25 produces the same generic private Card and preserves all four
  independent diagnostics. Synthetic civilisations topic is not historical evidence.

Development: first P01–P42 run collected 42 methods and had 2 test-harness failures
(C22 projection coverage accounting and deepcopy equality of exception objects).
Both corrected only in the new tests; isolated rerun: 2 tests, OK, exit 0. Final
suite results below apply to the completed code/tests, not that development run.
No test disabled/skipped/expectedFailure; no approved expected outputs altered.

## 5. Actual regression commands

Project `.venv`, Python 3.12.14, Linux CPU-only. Counts are collected methods;
parameterized family/variant/native-oracle witnesses are described separately.

| Command | Tests | Failures/errors/skips | Exit | Outcome |
| --- | ---: | --- | ---: | --- |
| `.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_decision_projection*.py' -v` | 73 | 0 / 0 / 0 | 0 | OK, 103.795 s |
| `.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_evaluate*.py' -v` | 78 | 0 / 0 / 0 | 0 | OK, 47.217 s |
| `.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v` | 295 | 0 / 0 / 0 | 0 | OK, 171.341 s |
| `.venv/bin/python -m unittest discover -s tests -v` | 1137 | 0 / 0 / 0 | 0 | OK, 967.966 s |
| `.venv/bin/python -m compileall -q story_intelligence tests` | — | — | 0 | OK |
| `git diff --check` / staged / committed diff | — | — | 0 | PASS; final committed check repeated before ZIP handoff |

Full-suite success is declared only after process exit 0, not from a unittest OK
line alone. Existing SI/evaluator/golden suites and storage/D-01 remain unchanged.
No Windows native qualification/production execution is claimed.

## 6. PD-01 measurements (outside production logic)

Measured after full discovery, no test runner running concurrently. Environment: CPython 3.12.14, Linux 6.18.57, x86_64; CPU model AMD EPYC 9V74 80-Core Processor; 3 visible logical CPUs, cgroup cpu.max `200000 100000` (2 CPU quota).

Harness: `tests.test_story_intelligence_decision_projection_v1.measure_performance(3)`.
Command: `.venv/bin/python` importing/calling that harness; actual process exit 0.
One unmeasured warm-up per path/case; three measured repetitions per path/case.
Expected result preparation outside timing. Projection timing includes full real
evaluator re-verification/canonical comparison/selector matching and rendering.
All measured outputs checked against genuine expected results; original inputs unchanged.

| Fixture | Records / roots / diagnostics | Path | Repeats | Min s | Median s | Max s |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| B | 11 / 5 / 0 | evaluator | 3 | 0.087679086 | 0.092065079 | 0.097894598 |
| B | 11 / 5 / 0 | projection_with_reverification | 3 | 0.094454528 | 0.102548607 | 0.105641983 |
| T25 | 11 / 6 / 4 | evaluator | 3 | 0.097350456 | 0.100948714 | 0.110070180 |
| T25 | 11 / 6 / 4 | projection_with_reverification | 3 | 0.110753485 | 0.115892859 | 0.128189672 |
| W01 | 17 / 6 / 4 | evaluator | 3 | 0.190993003 | 0.192508107 | 0.199751228 |
| W01 | 17 / 6 / 4 | projection_with_reverification | 3 | 0.197120674 | 0.199643124 | 0.199775886 |
| MULTI | 16 / 7 / 10 | evaluator | 3 | 0.173411144 | 0.181882575 | 0.182478647 |
| MULTI | 16 / 7 / 10 | projection_with_reverification | 3 | 0.185703893 | 0.186251151 | 0.200249737 |

Table durations rounded to nine decimals for readability; raw observed samples (s):

```text
B evaluator: [0.08767908600020746, 0.09206507899943972, 0.09789459800049372]
B projection_with_reverification: [0.09445452799991472, 0.1056419830001687, 0.10254860699933488]
T25 evaluator: [0.0973504560006404, 0.11007018000054813, 0.10094871399996919]
T25 projection_with_reverification: [0.1158928590011783, 0.1281896720010991, 0.11075348499980464]
W01 evaluator: [0.1997512279995135, 0.19250810700032162, 0.1909930029996758]
W01 projection_with_reverification: [0.19977588599977025, 0.19712067399996158, 0.19964312400043127]
MULTI evaluator: [0.18247864699878846, 0.1818825749996904, 0.17341114400005608]
MULTI projection_with_reverification: [0.18570389300111856, 0.20024973699946713, 0.18625115100076073]
```

Measurements are synthetic observations, not performance qualification, guarantees,
latency quotas or decision thresholds. No verification optimization/bypass is used.
Any mechanism change still requires a separate contract and owner approval.

## 7. Review artifact, limits and STOP

ZIP contains exact committed versions of the five changed paths, including this
RESULT and append-only WORKLOG. Archive written outside repository; CRC and each
entry compared to Git blobs after local commit. No models/media/keys/personal data.
Code/constants and synthetic tests only. Main/source refs and approved files preserved.

No blocking contract contradictions found in the executed scope. Guarantees concern
consistency of declared inputs and safe private explanation, not world completeness,
authenticated human decisions, scientific truth, licence validity, actual assets/CPU
availability, editorial approval or production/publication permission. Returned
structure is private local presentation, not public export authorization or SI record.

EVAL-P05 OPEN; PUBLISH_REVISION DISABLED; partial COMMIT reconstruction OFF;
Windows S3.2b BLOCKED_HOST_NOT_PROVIDED. No protected writes, source discovery,
creative/Brief generation, new authority or execution integration. **No push/PR/merge/
tag/release. LOCAL COMMIT AND REVIEW ZIP ONLY. STOP for independent review.**
