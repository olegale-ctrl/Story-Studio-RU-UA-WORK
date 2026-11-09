# SI-E01.2a-RESUME-F1 — Packet capture consistency

Дата: 2026-11-09. Узкое исправление реализовано; **независимая приёмка ещё требуется**.
SI-E01.2a-RESUME остаётся CHANGES_REQUIRED до независимой проверки F1.

- Base: `f752e9aa5745514677dd1fd9dcf82b915309c3b1`.
- Source: `docs/story-intelligence-si-e01-2a-independent-review`.
- Feature: `fix/story-intelligence-si-e01-2a-resume-f1-packet-capture`.
- Source remote HEAD проверен перед созданием ветки и совпал с exact base.
- Commit/remote SHA сообщается после публикации в handoff (без self-reference
  собственного commit hash внутри этого же коммита).

## Основание и причина

Прочитаны [полное F1 задание](STORY_INTELLIGENCE_SI_E01_2A_RESUME_F1_CODEX_TASK.md),
[независимое ревью F1](STORY_INTELLIGENCE_SI_E01_2A_RESUME_INDEPENDENT_REVIEW_F1.md),
[предыдущий RESULT](STORY_INTELLIGENCE_SI_E01_2A_RESUME_RESULT.md), полные принятые
record source/tests и относящиеся к Packet original/R1/R1b clauses/owner approval.
Порядок original → R1 → R1a → R1b и все утверждённые контракты сохранены.

Общий BriefReviewState имеет nullable brief_ref/creative_ref для этапов до Brief.
Это правильно. Ошибка была в Packet-specific `_packet()`: условие
`brief_ref is not None and brief_ref != Packet.brief_ref` пропускало null;
отдельного запрета null creative_ref в Packet не было. Проверки snapshot/context
hash не помогают: изменение этих capture refs не изменяет соответствующие digest
inputs. Persisted Packet уже имеет обязательный Brief, а у Brief обязателен Creative.

## Минимальное исправление и diff

Изменены только:

| Файл | Изменение |
|---|---|
| `story_intelligence/records_v1.py` | В `_packet()` убран nullable bypass brief equality; добавлен отказ для null creative_ref. Всего 3 additions / 1 deletion |
| `tests/test_story_intelligence_records_v1.py` | Пять F1 regression методов, 34 additions; существующие tests/fixtures не переписаны |
| `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_RESUME_F1_RESULT.md` | Этот новый отчёт |

Packet captured brief_ref теперь всегда точно совпадает с Packet.brief_ref,
поэтому null также отклоняется. Captured creative_ref обязан быть non-null.
Оба отказа используют существующий `PROVENANCE_MISMATCH` и точные paths:
`$.payload.review_state_at_capture.brief_ref` / `.creative_ref`.
Прежняя non-null mismatch проверка, её code/path и сообщение сохранены.
Ничего не подставляется и не пересчитывается в пользовательской projection.
Общая `_REVIEW` schema не изменена. Проверка Creative equality с реальным Brief
не выполняется: без resolver она не доказуема и не входит в F1.

Новых contract gaps не обнаружено, optional F1_CONTRACT_GAPS не создан.
Старые feature/BLOCKED ветки и их commits не переиспользовались и не переписывались.

## Воспроизведение до исправления и regression после

До production edit выполнен exact minimal reproducer: каждый случай начинается
с нового `fixtures()['ReviewPacket']`; изменяется только указанное capture поле.
В different_brief подставлен well-formed ProductionBrief SIRef с другим synthetic
UUID `99999999-1111-4111-8111-111111111111`, не alias и не нарушенный hash shape.

| Случай | До fix | После fix |
|---|---|---|
| Valid Packet | ACCEPTED | ACCEPTED, detached copy |
| Captured brief_ref=null | **Ошибочно ACCEPTED** | PROVENANCE_MISMATCH, exact .brief_ref path |
| Captured creative_ref=null | **Ошибочно ACCEPTED** | PROVENANCE_MISMATCH, exact .creative_ref path |
| Captured brief_ref=другой ProductionBrief | PROVENANCE_MISMATCH, exact .brief_ref path | Тот же отказ/code/path |
| General pre-Brief projection с обоими null | Структурно допустима | По-прежнему допустима |

Во всех случаях проверена неизменность входа. General projection тестируется
на прежней `_REVIEW` value schema через `_check`: отдельного публичного standalone
projection validator нет. Packet-specific правила не переносятся на общий value type.

Пять методов PacketTests:
`test_F1_capture_brief_is_required`, `test_F1_capture_creative_is_required`,
`test_F1_capture_brief_must_match_exact_packet_brief`,
`test_F1_valid_packet_remains_accepted_unchanged`,
`test_F1_general_prebrief_projection_remains_nullable`.

Их командный запуск (каждый selector передан явно):

```bash
.venv/bin/python -m unittest \
 tests.test_story_intelligence_records_v1.PacketTests.test_F1_capture_brief_is_required \
 tests.test_story_intelligence_records_v1.PacketTests.test_F1_capture_creative_is_required \
 tests.test_story_intelligence_records_v1.PacketTests.test_F1_capture_brief_must_match_exact_packet_brief \
 tests.test_story_intelligence_records_v1.PacketTests.test_F1_valid_packet_remains_accepted_unchanged \
 tests.test_story_intelligence_records_v1.PacketTests.test_F1_general_prebrief_projection_remains_nullable -v
```

До fix: **5 executed, 2 failures, 3 OK**, 0.008 s, exit1. Оба failures подтверждают
отсутствие исключения для null; mismatch и два positives уже проходили.
После fix: **5 OK**, 0.009 s, exit0. No skip/expectedFailure/suppression.

## Целевой и полный прогоны

Среда: Linux x86_64, Python 3.12.14, проектный `.venv/bin/python`.
Context7 не требовался: исправление использует существующие локальные API и stdlib,
без новой внешней интеграции. Внешних documentation calls не было.

```bash
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v
.venv/bin/python -m unittest discover -s tests -v
```

Целевой: **66 OK**, 1.343 s, exit0: прежние 61 + 5 новых F1 methods.
Полный: **908 OK**, 846.737 s, exit0; failures=0, errors=0, skipped=0,
expectedFailures=0. Это прежние 903 + 5 новых F1 methods. Все S1/S2/D-01 и LAB
regressions прошли; S2.3 дополнительно сообщил 1659 параметризованных сценариев
(не дополнительные unittest methods). test_sprint23_2.Sprint232Tests.test_env_override
прошёл на Linux. Baseline ошибок окружения не обнаружено.

## Сохранность и пределы

Все 18 literal record и 3 R1b value vectors сохранены byte-for-byte: vectors файл
сравнён с `f19fa33685f05df632222dbcd84abcaca8258547`, не изменялся. Все шесть
принятых SI-E01.1 файлов и storage protocol/transaction/adversarial regression
files сравнены с `61886670fe6d0434df62f6346457f5812f520766`: byte-identical.
Существующие golden values, contracts, tasks/reviews/results, dependencies/config,
editorial/storage и main не менялись. Exact allowlist (2 modified + 1 new), syntax, report links/fences,
`git diff --check` и staged diff --check проверены перед commit. AST общей _REVIEW
schema идентичен базе. Remote source HEAD повторно сверяется с exact base;
post-push HEAD/parent/remote equality и clean worktree проверяются в handoff.
Суммарный diff: **3 файла, 166 additions / 1 deletion**.

Нет resolver/DAG/полной Closure, operation execution, currentness computation,
privacy authorization/export/PII detection, provider, renderer, persistence,
Windows native work или protected writes. Синтетические refs остаются unresolved,
human labels не становятся authority. SI-F01 integer-latency benchmark не выполнялся,
новый digit cap не введён. PUBLISH_REVISION DISABLED; partial COMMIT reconstruction OFF;
S3.2b BLOCKED_HOST_NOT_PROVIDED. Linux tests не квалифицируют native Windows.

После публикации — STOP для независимого ревью F1. SI-E01.2b/SI-E02 не начаты.
PR, merge, release и изменения main не выполнялись.
