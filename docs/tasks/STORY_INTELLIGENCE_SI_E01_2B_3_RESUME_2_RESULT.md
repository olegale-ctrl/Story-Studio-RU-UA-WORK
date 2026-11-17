# SI-E01.2b.3-RESUME-2 — Pure Semantic Currentness result

Дата: 2026-11-10 (Europe/Kyiv).
**IMPLEMENTED / PURE_READ_ONLY_CURRENTNESS_ONLY / AWAITING INDEPENDENT REVIEW.**
Это отчёт реализации и фактических локальных проверок, не independent acceptance.

## Git и основание

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Source: `docs/story-intelligence-si-e01-2b-3-g02-approval-resume-2`.
- Exact base: `bd16606b55ecf3ef2e29468a39d40b51e0f4e856`.
- Feature: `feat/story-intelligence-si-e01-2b-3-resume-2-currentness`.
- До изменений remote source HEAD совпал с literal base; новая ветка создана только
  от него. Проверены наличие task/approval и чистота исходного дерева.
- Final commit и remote SHA публикуются в handoff после commit: self-referential
  hash невозможно включить в содержимое того же коммита. Parent должен быть exact base.

Применены [полное задание](STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_2_CODEX_TASK.md),
[owner G02 approval](STORY_INTELLIGENCE_SI_E01_2B_3_G02_OWNER_APPROVAL_2026_11_10.md)
и его [D1–D4 proposal](STORY_INTELLIGENCE_SI_E01_2B_3_G02_OWNER_DECISION_PROPOSAL.md),
[owner G01 approval](STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_APPROVAL_2026_11_10.md)
с D1–D5, original/R1/R1a/approved R1b и SI-D01–D10. Прочитаны independent G02
blocker review, прежние reports/reproducer/tasks, acceptances SI-E01.2a/F1,
SI-E01.2b.1 и SI-E01.2b.2/F1, accepted modules/tests/vectors.
Прежние BLOCKED_CONTRACT reports сохранены неизменными. RFC не является разрешением.
Нового существенного contract gap при реализации этого bounded scope не обнаружено.

## Четыре новых файла — существующие файлы не изменены

| Файл | Назначение |
| --- | --- |
| [currentness_v1.py](../../story_intelligence/currentness_v1.py) | Pure read-only API, typed semantic projection, exact observed comparison |
| [test_story_intelligence_currentness_v1.py](../../tests/test_story_intelligence_currentness_v1.py) | 21 unit-test methods, genuine graph factories, G01/G02/negative cases |
| [test_story_intelligence_currentness_vectors_v1.py](../../tests/test_story_intelligence_currentness_vectors_v1.py) | 10 independent literal graph/context/root vectors, 10 methods |
| Этот RESULT | Evidence, scope, ограничения и STOP |

Нет изменений accepted source/tests/golden, contracts/owner approvals, прежних
GAPS/RESULT, WORKLOG/README/RFC/CI/config/dependencies, editorial/storage/main.
Нового CONTRACT_GAPS нет. Production module не содержит файловых/сетевых операций,
subprocess, mutable global cache, providers или действий при импорте.

## API и порядок проверки

`check_si_currentness(records, root, observed_active_input_refs, observed_selection_head_refs)`
возвращает новый plain dict `{currentness, reason_codes}` с отдельным новым list.
`CURRENT` имеет `[]`; `STALE` — `[INPUT_STALE]`; `INVALID` — существующий Code.
Codes сортируются/уникализируются; новых fields/types/error codes нет.

1. `records` — plain finite list; `root` — один exact domain SIRef (без metadata
   RunRecord/Selection/ReviewPacket); observed arguments — plain lists с exact refs.
   Active — domain refs, heads — Selection. Shape/wrong-role/duplicate identity
   failures поднимают существующий SIValidationError с точным аргументным path.
   Примеры: TYPE `$.records`, TYPE `$.root` для списка roots, TYPE
   `$.observed_active_input_refs[1]` для повторной (type,id), REF_TYPE_MISMATCH
   `$.observed_selection_head_refs[0].type`, SELECTION_CONFLICT при duplicate chain.
   Остальные shape/unknown/missing/ref diagnostics делегированы accepted ref validator.
2. Accepted `verify_si_provenance(records, [root] + active + heads)` проверяет exact
   полный reachable audit DAG, hashes, previous, actual Run stages, frozen snapshots
   и F1 report↔Run Rubric. Он использует принятый resolver. Unrelated bundle records
   сохраняют accepted structural validation boundary; объявленные observed refs
   сами также должны полностью resolve. Невалидный reachable graph возвращает
   INVALID с existing error.code, а не STALE. Minimal result не добавляет graph path;
   exact graph paths доступны в принятых resolver/provenance API. Ошибки не исправляются.
3. Две разные resolved heads одного exact Selection scope → INVALID/SELECTION_CONFLICT.
   Нет выбора по времени, максимальному UUID или revision.
4. Отдельный iterative typed walk по accepted `_SCHEMAS` строит semantic dependencies,
   включая nested Known/list refs. Нет dict-shape/text heuristics. Audit `H.previous`,
   `H.input_refs`, generic origin edge, Run snapshots/context не promoted в current.
   Для HUMAN_EDIT payload проверен provenance; previous/base не обходится как current.
5. Для Creative используется frozen original C. Текущий payload определяет Angle
   и hook/chapter refs. Старый producer Angle, совпавший с genesis angle_ref, не
   required лишь по ancestry; retained exact E1 всё равно сохраняет свою оценённую
   Angle/Idea/Audience. Несовпадение с evaluated bindings даёт STALE даже если обе
   старые/новые domain identities представлены в active set. Каждый direct C
   ClaimItem остаётся самостоятельной required-current dependency по G02; новый
   payload claim не удаляет старую producer constraint.
6. Required domain refs сравниваются с active full `(type,id,revision,sha256)`.
   Used creative Selection Brief сравнивается с observed heads, не с active set.
   Дополнительные unrelated valid records/heads и порядок lists не stale'ят результат.
   Freshness root здесь означает свежесть dependencies, не факт выбора самого output.
7. Relevant typed ERef/current substantive H.editorial_refs без exact validated
   editorial snapshot → INVALID/REF_MISSING, даже если SI hashes корректны.
   В API snapshot/adapter отсутствует; UNKNOWN/opaque digest не даёт доверия.
   INVALID проверяется до финального STALE; частичный CURRENT не возвращается.

Все inputs должны быть стабильными на время вызова, как у accepted resolver.
Обход/read-only индексы локальны вызову; нет изменения данных caller и lazy/latest
lookup. Отдельного UI/Packet whole-context freshness/readiness здесь нет.

## Покрытие G01 и G02

| G01-D5 / требование RESUME | Фактическая проверка |
| --- | --- |
| Source S1→S2→S3 CURRENT, intact inactive edit-bases | `test_G01_source_three_revisions_inactive_bases_current`; source literal vector |
| Missing/corrupt S2 INVALID | `test_G01_missing_or_corrupt_edit_base_invalid`; missing-source vector |
| K1/K2/K3 text-only CURRENT, original C intact; E1 absent/replaced active STALE | `test_G01_G02_text_only_K1_K2_K3_current_without_ancestral_identities`, `test_G01_original_evaluation_missing_active_or_replaced_stale` |
| Incompatible Angle/Idea/claim with frozen E1 STALE | `test_G01_incompatible_new_angle_cannot_rebase_frozen_E1`; literal angle vector |
| E1 independent of future heads; required Idea/Angle/Rubric/Source/Check change STALE | `test_unrelated_selection_heads_never_stale_evaluation_or_creative`, `test_all_required_evaluation_inputs_removed_or_revised_stale` |
| Brief used exact head changes STALE; own WITHDRAW not automatic domain stale | `test_G01_brief_used_selection_head_exact_and_withdraw_own_head`; two Brief vectors |
| Relevant unvalidated ERef INVALID | `test_G01_G02_relevant_eref_invalid_not_stale_or_trusted_digest`; ERef vector |
| All 14 revisable types, malformed lists/refs/duplicates/conflicts/order/copy; immutable audit bytes | `test_all_fourteen_revisable_types_keep_history_out_of_current_set`, override/error-path/detachment/audit tests |

| G02-D3 — все восемь случаев | Фактическая проверка |
| --- | --- |
| Exact Qa/Qb/Qc graph without Qa active → STALE/INPUT_STALE | Published graph/context digests asserted; `g02_stale` literal vector |
| Add exact Qa → CURRENT | Same graph bytes, `g02_current` vector |
| Unchanged text-only K3 CURRENT, K1/K2 inactive | Text-only method/vector |
| Qa shared hook/chapter, new hook Qc → Qa still required | Shared fixture, `test_G02_shared_hook_chapter_claim_and_independent_check_risk` |
| Qa retained through Check/Risk/E1 basis → required | Independent bindings fixture: Evidence, Check, Risk, EVALUATION roots/rating basis |
| Missing/corrupt historical Qa → INVALID | Negative method and corrupt-Qa vector |
| Unrelated Selection head changes do not affect K3 | Same currentness under absent/original/revised unrelated heads |
| Relevant ERef INVALID | ERef method/vector, accepted SI audit graph still passes |

Valid CURRENT и STALE сценарии сначала сравнивают authored explicit-edge Closure
oracle с **обоими** accepted resolver/provenance outputs. Ни одного mock/patch
resolver/hash или invented successful proof нет. Snapshot/ancestor corruption,
F1 mismatch и cycles проверяются как INVALID. Обёртки qualification/eligibility/
rights/execution claims не создаются. Unknown research data остаётся unknown.

## Независимые literal vectors

Десять case names: `source_current`, `source_missing`, `g02_stale`, `g02_current`,
`text_current`, `qa_corrupt`, `angle_stale`, `eref_invalid`, `brief_current`,
`brief_head_stale`. В vector-файле зафиксированы буквальные root type/id/revision/SHA,
SHA canonical record-list bytes, SHA observed `{active_input_refs,selection_head_refs}`
и manually authored expected state/codes по G01/G02. Это локальное test value,
не новый wire ContextSnapshot и не authenticated observation.

Fixture bytes/hash строятся stdlib JSON/hashlib отдельно от currentness/production
codec. Literal constants проверяются как independent fixture digest и отдельно
accepted canonical_si_sha256, не только сравнением двух функций друг с другом.
Ожидаемые states не вычислялись currentness checker. Это независимость oracle от
реализации, не утверждение о независимом внешнем review/запуске.

Exact опубликованный G02 oracle сохранён:

- 19 canonical records, 19 reachable audit refs; original observed 11 identities.
- Graph SHA: `d8f2a8439f9ce3cfa6db385382eb07cbe296e1edc29ccfac5f52a07090be0975`.
- Original context SHA: `2e29b4a85cb640df76ffdbad34214f95f53a5e8fd58d5a298746be2e7ef8be0d`.
- K3 SHA: `7a88b9dadaa313c51e910752a908582e03b1d3c3dcf954640cf38c42e5d8a967`.
- При добавлении exact Qa graph/root bytes те же; context SHA:
  `e2836e519efb567378dacc1e1aa220ef716b5a230310f237e2e131b9e459fde7`.

## Фактические команды и результаты

Среда: Linux x86_64, проектный `.venv/bin/python`, Python 3.12.14.

```bash
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_currentness*.py' -v
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v
.venv/bin/python -m unittest discover -s tests -v
```

| Final suite | Tests | Unittest duration | Raw Python exit | Outer session exit | Skips/errors/failures |
| --- | --- | --- | --- | --- | --- |
| Currentness | 31 / OK | 8.447 s | 0 | 0 | 0/0/0 |
| All SI | 134 / OK | 17.641 s | 0 | 0 | 0/0/0 |
| Full | 976 / OK | 785.500 s | 0 | 0 | 0/0/0 |

Ранний development прогон: 19 currentness methods OK (5.019 s), затем 29 OK
(5.561 s); final 31 включает дополнительные 14-type и payload-override cases.
Ненулевых development test results не было. Baseline 103 SI / 945 full не выдаётся
за новый итог: final фактические counts указаны в таблице.

Каждый command запускается через `subprocess.run` с точным argv, stdout+stderr
без фильтрации сохраняются в `/tmp/si_currentness_resume2_{currentness,si,full}.raw.log`.
Печатаются raw child exit и elapsed time. Для targeted последовательности первый
nonzero немедленно передаётся `sys.exit(result.returncode)`; full — отдельный процесс
с таким же сохранением кода. Нет `|| true`, pipe masking, environment mutation или
поправок unrelated harness. Diagnostic elapsed для targeted: 8.574 s / 17.783 s.
Full diagnostic elapsed: 785.816 s; дополнительно S2.3 сообщил 1659 parameterized
scenarios. Full summary OK согласован с raw Python exit 0 **и** outer session exit 0.
Прежнее историческое OK/exit 1 расхождение не воспроизвелось; причина того старого
запуска не объявляется установленной и прежний отчёт не переписывается.

SHA-256 unfiltered raw logs (вне Git):

- Currentness: `482387e59b2bc4655e57d34d3019ebb3deb65abaa837512d9e0b95eededdeab1`.
- SI: `98e07764f961980ce1f707b85ad5e93b3de58664a1dabbb0493b29db3e9ea0ac`.
- Full: `fef5f108eae5c16b4d821f47f51b49844f681da53b9eea80efd44bf9b2a3644f`.

Tested source SHA-256: `67c035282131bd2f37f2b4a605d28c2ed191eac0a866ff998d1867773d255bed`.
Между final targeted/full прогонами исходники и тесты не менялись, после full
обновлён только RESULT. Никаких тестовых skips/expectedFailure/waivers не добавлено.

## Проверки и оставшиеся ограничения

Выполнены exact A-only four-file allowlist, syntax AST checks, Markdown links/fences
и `git diff --cached --check` / `git diff --check` (exit 0). Все 14 принятых SI
source/test files сравнены byte-for-byte с exact base, включая прежние 14 foundation /
18+3 record-value / 7 resolver / 9 provenance vectors. Других existing-file changes нет.
Source remote повторно равен exact base; main read-only наблюдался на
`e1f4efb0fb5ff290bb198349213c004b4667ef0f`. Parent/base/remote equality и clean
worktree проверяются после publication; exact commit SHA и final diff/stat — в handoff.

G02 намеренно может давать false-stale после benign hook replacement: direct C Qa
остаётся required. Role-map/backlog/RFC не реализованы. CURRENT относится только
к supplied consistent bytes/dependencies относительно explicit observations; caller
не становится trusted harness. Никаких фактических run-execution, truth, rights,
authorization, Selection eligibility или production permission гарантий нет.
Relevant ERef без validated material возвращает INVALID; adapter не добавлен.
Нет UI BriefReviewState, Packet freshness, operation execution, persistence/export,
редакционных/storage/protected writes, provider/network/GPU или новых dependencies.
Performance qualification и SI-F01 hardening не заявляются; Linux tests не Windows
native qualification. Пределы/канонические правила accepted codec не менялись.

Без PR/merge/release/main изменений. SI-E02, RFC и другие этапы не начинались.
`PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF;
Windows S3.2b BLOCKED_HOST_NOT_PROVIDED. После публикации — **STOP для independent review**.
