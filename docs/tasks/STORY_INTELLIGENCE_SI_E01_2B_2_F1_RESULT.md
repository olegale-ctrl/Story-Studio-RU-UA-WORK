# SI-E01.2b.2-F1 — EvaluationReport Rubric Binding Fix

Дата: 2026-11-10. Узкий F1 исправлен; **независимая приёмка ещё требуется**.
Статус независимого ревью SI-E01.2b.2 остаётся CHANGES_REQUIRED до проверки fix.

- Code base: `9a2999bae72b1d6bd6784e7df305f59dea1bfd2e`.
- Source feature: `feat/story-intelligence-si-e01-2b-2-pure-provenance`.
- Fix branch: `fix/story-intelligence-si-e01-2b-2-f1-rubric-run-binding`.
- Task/review documentation HEAD: `8a055dae91d65cb00fa55abda24553b128fee413`,
  branch `docs/story-intelligence-si-e01-2b-2-independent-review-f1`.
- Оба remote HEAD проверены до изменений и совпали с handoff. Code branch создана
  именно от 9a2999b, **не** от docs/RFC/main; docs прочитаны через git show без merge.
- Final commit/remote SHA сообщается после push в handoff; self-referential commit
  hash нельзя буквально включить в содержимое того же коммита. Проверяются exact
  parent/base, remote SHA equality и clean worktree.

## Нормативное основание и причина

Прочитаны полные
[F1 task](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/8a055dae91d65cb00fa55abda24553b128fee413/docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_2_F1_CODEX_TASK.md)
и [independent F1 review](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/8a055dae91d65cb00fa55abda24553b128fee413/docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_2_INDEPENDENT_REVIEW_F1.md)
из отдельной docs branch. Эти файлы отсутствуют в исходной feature base, поэтому
не копировались в worktree вопреки allowlist. Также прочитаны
[R1](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md) §§1–3.1,
[R1a](STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md),
[исходный bounded task](STORY_INTELLIGENCE_SI_E01_2B_2_CODEX_TASK.md),
[предыдущий RESULT](STORY_INTELLIGENCE_SI_E01_2B_2_RESULT.md), provenance source/tests.
Порядок original → precise R1 → R1a → approved R1b сохранён.

R1 §3.1: **«Payload.run_ref = H.origin.run_ref; rubric/method refs совпадают с
RunRecord.»** В прежней версии проверялся actual Run stage/method/version, но точное
равенство report Rubric и actual generating Run Rubric было пропущено. Это
cross-record binding, а не расширение в scoring/rubric-policy/eligibility.
Resolver правильно подтверждает обе существующие Rubrics и DAG, но не обязан
устанавливать равенство разных semantic role refs; ответственность — provenance.

## Минимальный production diff

После resolver и успешной проверки actual EVALUATION / si.evaluate / 1-r1 добавлен
ровно один guard в verify_si_provenance: полный typed SIRef
`EvaluationReport.payload.rubric_ref != actual Run.payload.rubric_ref`
→ `PROVENANCE_MISMATCH` по `$.records[i].payload.rubric_ref`.

Сравниваются все поля type/id/revision/sha256, не только id или semantic equivalence
criteria. Нет latest fallback, coercion, repair/autofill или новой error vocabulary.
Actual Run stage/method, history, K1/K2/K3 и HUMAN_EDIT root checks не менялись.
Ни один из ref не переписывается; validator не вызывает execution и не меняет input.

Изменены только разрешённые файлы:

| Файл | Diff |
|---|---|
| `story_intelligence/provenance_v1.py` | 2 additions: один exact binding guard |
| `tests/test_story_intelligence_provenance_v1.py` | 70 additions: isolated F1 class, independent graph helper и три tests; прежние tests/factory не переписаны |
| `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_2_F1_RESULT.md` | Этот новый отдельный отчёт |

Другие файлы, contracts, vectors, accepted code, WORKLOG, configs/dependencies,
editorial/storage и main не изменены. RFC proposals не затрагивались.

## Genuine graph и red/green

Каждый case начинается с true content-addressed graph. Берётся реальный EVALUATION
Run и EvaluationReport с Rubric A. Bundle ограничен нужной audit Closure, чтобы
не содержать stale downstream refs после изменения report. Expected manifests
и новые record/root hashes считаются **stdlib JSON/hashlib** fixture helpers,
без production hashing/resolver mocks. Actual Run ref не меняется и его snapshot
остаётся exact Closure declared roots с Rubric A.

В mismatch cases report меняется на реальный B ref, затем recomputed report/root
hash. В bundle одновременно находятся actual A и B и все необходимые ancestors:

| Case | Данные | До fix | После fix |
|---|---|---|---|
| matching | Report=A, Run=A (exact SIRef) | Resolver/Verifier ACCEPTED | ACCEPTED, detached result |
| different_record | B — отдельная valid Rubric с другим UUID и real SHA | Resolver ACCEPTED, verifier **ошибочно ACCEPTED** | PROVENANCE_MISMATCH |
| different_revision | B — revision2 того же Rubric id, exact previous=A и actual REVISION Run; другой SHA | Resolver ACCEPTED, verifier **ошибочно ACCEPTED** | PROVENANCE_MISMATCH |

В revision case не создаётся конфликт двух bytes одной identity: B имеет revision2,
valid HUMAN_EDIT metadata, direct base=A и real REVISION snapshot. Все критерии и
weights остаются structurally valid; описательный текст изменён как synthetic edit,
не новая scoring policy. В каждом mismatch test **сначала** asserted успешный
`resolve_si_closure` и exact independent manifest, затем exact provenance error.
Ни stale hashes, ни missing refs, ни wrong stage не маскируют F1.

Точный ожидаемый путь в обоих fixtures — `$.records[10].payload.rubric_ref`;
assertion вычисляет index output record из фактического bundle. Проверены input
immutability и detached successful manifest. Полное равенство refs подтверждается
отдельным same-id/different-revision/hash adversarial case.

Новые методы класса `RubricRunBindingF1Tests`:

- `test_F1_matching_exact_report_run_rubric_accepted_detached`;
- `test_F1_distinct_real_rubric_rejected_after_resolver_success`;
- `test_F1_same_rubric_new_revision_rejected_after_resolver_success`.

Focused command:

```bash
.venv/bin/python -m unittest tests.test_story_intelligence_provenance_v1.RubricRunBindingF1Tests -v
```

**Red:** до production edit прямой reproducer показал resolver ACCEPTED и verifier
ACCEPTED во всех трёх cases, в том числе при different refs. Regression suite:
**3 executed, 2 failures, 1 OK**, 0.142 s, exit1; оба failures — исключение не raised.
**Green:** после двухстрочного guard **3 OK**, 0.150 s, exit0. Tests не ослаблялись,
skips/expectedFailure/suppression не добавлялись.

## Полные проверки и immutable vectors

Среда: Linux x86_64 / Python 3.12.14, проектный `.venv/bin/python`.

```bash
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_provenance*.py' -v
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v
.venv/bin/python -m unittest discover -s tests -v
```

- Provenance: **18 OK**, 4.108 s, exit0 (previous 15 + 3 F1 methods).
- All SI: **103 OK**, 8.830 s, exit0 (previous 100 + 3).
- Full: **945 OK**, 791.696 s, exit0 (previous 942 + 3), failures=0,
  errors=0, skipped=0, expectedFailures=0. Все existing S1/S2/D-01/LAB regressions
  прошли; дополнительно S2.3 сообщил 1659 параметризованных сценариев (не
  дополнительные unittest methods). test_sprint23_2.Sprint232Tests.test_env_override
  прошёл на Linux, baseline ошибок окружения не обнаружено.

Побайтно проверены все прежние literal vector files: 14 foundation @
`61886670fe6d0434df62f6346457f5812f520766`; 18+3 record/value @
`f19fa33685f05df632222dbcd84abcaca8258547`; семь resolver @
`0c27547377255016ec2fc399090ce99b63d69485`; девять provenance @
`9a2999bae72b1d6bd6784e7df305f59dea1bfd2e` — unchanged. Новых literal values
в эти файлы не добавлялось. F1 graph oracles находятся только в разрешённом tests файле.
Перед commit проверены syntax, exact 2M+1A allowlist, git diff --check и staged
check, report links/fences, source/base SHA. Post-push parent/remote equality и
clean worktree проверяются в handoff. Linux unittest не является CI/native Windows
qualification. Итоговый diff: **3 файла, 218 additions, 0 deletions**.

## Ограничения и STOP

Guard подтверждает только consistency двух supplied exact refs. Не проверяет
criteria/weights, eligibility, score, actual Run execution, editor identity,
review rights, source truth, license/privacy или authority. ERef adapter, semantic
currentness/gates, operations, persistence/storage/export, performance optimizations
и RFC implementation не добавлены. Existing limits и SI-F01 note не менялись.
PUBLISH_REVISION DISABLED; partial COMMIT reconstruction OFF; S3.2b BLOCKED_HOST_NOT_PROVIDED.
После publication — STOP для независимой F1 приёмки. SI-E01.2b.3/SI-E02 не начинались.
PR/merge/release и изменений main нет.
