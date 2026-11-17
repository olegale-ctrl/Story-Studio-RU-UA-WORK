# SI-E01.2b.3 — contract-first result

Дата: 2026-11-10. **BLOCKED_CONTRACT — implementation not started.**

- Base: `658212f9a8f5e91a5af9551093cbd85d7512c08a`.
- Source: `docs/story-intelligence-si-e01-2b-2-f1-independent-acceptance`.
- Feature: `feat/story-intelligence-si-e01-2b-3-pure-semantic-currentness`.
- Remote source HEAD проверен до изменений, совпал с exact base. Ветка создана от
  этого SHA, без fallback на main/старую feature/RFC.
- Commit/remote SHA сообщается после публикации в handoff; self-referential hash
  нельзя включить в содержимое того же коммита. Проверяются exact parent и remote.

## Основание и blocker

Прочитаны [полное задание](STORY_INTELLIGENCE_SI_E01_2B_3_CODEX_TASK.md),
[independent F1 acceptance](STORY_INTELLIGENCE_SI_E01_2B_2_F1_INDEPENDENT_ACCEPTANCE.md),
original, R1 §§1–6, approved R1a/R1b и owner approvals, prior acceptance notes и
accepted modules/tests. Нормативный приоритет original → R1 → R1a → approved R1b
не менялся. RFC proposals не реализуются и не являются code base/контрактом.

[SI-E01.2b.3-G01](STORY_INTELLIGENCE_SI_E01_2B_3_CONTRACT_GAPS.md) описывает пробел
role projection mandatory HUMAN_EDIT base из Run.semantic_input_refs в
required-current semantic set. Референс указан как semantic direct input, но
одновременно является editing history; исключение generic H.previous edge не
решает оба пути. Для Creative требуется ещё сохранить/классифицировать evaluation
inputs original C1, отсутствующие в current payload. Нельзя ни превратить audit
Closure в semantic, ни молча удалить обязательные causal bindings, ни rebase их
на observed latest. Задание прямо требует STOP при такой under-specification.

GAPS содержит sections/lines, настоящие SHA/observed-set примеры и минимальные
owner decisions, не утверждая собственный CURRENT/STALE oracle. ERef snapshot
отсутствие не выдано за самостоятельную невозможность INVALID: R1 этот отказ уже
задаёт. Пример G01 специально ERef-free; UNKNOWN/digest не превращены в trust.

## Состав diff и состояние реализации

Созданы только два new/A-only файла из allowlist:

- `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_CONTRACT_GAPS.md`;
- `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_RESULT.md`.

Нет currentness_v1.py, новых executable currentness tests, partial evaluator или
шести выдуманных positive CURRENT vectors. Не менялись accepted modules/vectors/
contracts/WORKLOG/CI/config/dependencies/editorial/storage/main и прежние branches.
Нет semantic engine, UI/BriefReviewState/selection readiness, ERef adapter, Asset
Registry, SQLite/lazy loading, persistence/renderer/provider или RFC implementation.
Прежние acceptances остаются действительными в своих bounded scopes.

## Воспроизведение и фактические проверки

Среда: Linux x86_64 / Python 3.12.14, проектный `.venv/bin/python`.

Read-only reproducer вызвал принятый verify_si_provenance (внутри accepted resolver)
на genuine Source3 graph: verified 5 exact refs и 0 actual ERefs. Предыдущие S2/S1
подтверждены в mandatory REVISION semantic roots, observed содержит один exact S3.
Показаны два competing interpretations CURRENT/STALE, **не результаты нового API**.
Creative K3 graph: verified 17 exact refs, observed 10 distinct domain identities;
R3 roots содержат old K2 и original Run C1, current payload не содержит EvaluationReport.
Все данные synthetic, лишние unrelated rows не объявляются semantic dependencies.

```bash
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_currentness*.py' -v
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v
.venv/bin/python -m unittest discover -s tests -v
```

- Currentness pattern: **0 tests**, `NO TESTS RAN`, exit **5**, 0.000 s. Tests не
  создавались по STOP; это **не PASS** и не BLOCKED_ENV, а отсутствие реализации
  вследствие BLOCKED_CONTRACT. Никаких skips/expectedFailure для вида PASS нет.
- SI baseline: **103 tests, OK, exit 0, 8.120 s**, zero skips.
- Full baseline: unittest summary **945 tests, OK, 791.789 s**, zero skips;
  S2.3 дополнительно сообщил 1659 parameterized scenarios. Однако execution
  session/shell wrapper вернул **exit 1** при summary OK; причина расхождения
  не установлена, общий exit 0/PASS не заявляется. В полном логе нет FAILED,
  ERROR или Traceback. Это ограничение evidence, не исправлялось вне allowlist
  и не объявлено доказанной ошибкой baseline environment.
  Baseline проверяет неизменённые accepted modules, не приёмку SI-E01.2b.3.

Проверки Markdown links/fences и `git diff --check` — OK (exit 0). Все tracked
files byte-for-byte неизменны относительно exact base, включая accepted code
и golden vectors. Публикационный контроль: только два новых документа (A-only),
exact source/base/parent/remote SHA и clean worktree; SHA сообщается в handoff.

## Требуемое решение и STOP

Нужно одобрить узкую causal→semantic role projection/inheritance для HUMAN_EDIT,
особенно original Creative evaluation inputs, с exact observed-set examples.
До этого нельзя честно присвоить требуемые positive currentness states. Ни один
вариант в GAPS не утверждён и существующие contracts не исправлены самостоятельно.

Нет операции/авторизации/проверки прав/истины/grants, внешних calls/Context7/новых
зависимостей или protected writes. PUBLISH_REVISION DISABLED; partial COMMIT
reconstruction OFF; S3.2b BLOCKED_HOST_NOT_PROVIDED. SI-F01 integer performance
note неизменна, benchmark не выполнялся и новый digit cap не вводился.
После публикации — STOP для owner clarification. SI-E02 и RFC не начинались.
PR/merge/release и изменений main нет.
