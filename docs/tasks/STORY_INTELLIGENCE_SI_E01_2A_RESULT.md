# SI-E01.2a — результат pre-implementation проверки

Дата: 2026-11-09. **Статус: BLOCKED_CONTRACT — implementation not started.**
Ветка: `feat/story-intelligence-si-e01-2a-payload-schemas`.
Точная база: `b74d805996e1e9eba65e323f6d1c2995fbb1234f`.
Remote HEAD `docs/story-intelligence-si-e01-1-independent-review` проверен до
создания ветки и совпал с базой. Итоговый commit SHA сообщается после публикации
в handoff, без self-reference в содержимом коммита.

## Основание и найденный блокер

Прочитаны [независимая приёмка SI-E01.1](STORY_INTELLIGENCE_SI_E01_1_INDEPENDENT_ACCEPTANCE.md),
[полное задание](STORY_INTELLIGENCE_SI_E01_2A_CODEX_TASK.md), owner approval и
binding original+R1+R1a; принятые SI-E01.1 модули/тесты/RESULT и existing editorial
ref vocabulary использованы read-only. Приоритет clauses не менялся.
Product Success Criteria прочитан отдельно через git show точного коммита
`ed1630140a6b9a7089ef04e1c926019c3cb74ed6`; его ветка не объединялась с рабочей.

[SI-E01.2a-G01](STORY_INTELLIGENCE_SI_E01_2A_CONTRACT_GAPS.md) фиксирует недостающий
exact wire namespace ReviewPacket field_path и source_ref mapping projection STATE.
R1 задаёт semantic whitelist и field_path:Text, но не выбирает точные root/index
правила; BriefReviewState не имеет SIRef. Задание требует exact field namespace,
all-18 schemas и STOP вместо самостоятельного добавления недостающего правила.
В GAPS приведены source sections/lines, две несовпадающие canonical grant hashes,
projection example и минимальные решения для владельца. Это contract gap, не
обнаруженный runtime-дефект SI-E01.1 и не отказ от утверждённой архитектуры.

## Состав diff

Созданы только два разрешённых документа:

- `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_CONTRACT_GAPS.md`;
- `docs/tasks/STORY_INTELLIGENCE_SI_E01_2A_RESULT.md`.

Условный GAPS файл создан из-за реального blocker по правилу задания. Не созданы
records_v1.py, новые record tests и partial schemas. Нет новых APIs, typed-record
identity/ref validation или 12 утверждаемых record golden vectors. Существующие
исходники, SI-E01.1 31 тест, contracts, Storage/editorial, зависимости/config и
main не изменены. Рабочие логи вне Git, только синтетические входы в примерах.

## Выполненные проверки

Среда: Linux x86_64 / Python 3.12.14, проектный `.venv/bin/python`.

```bash
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v
.venv/bin/python -m unittest discover -s tests -v
```

- Целевой baseline: **31 OK**, 0.338 s, exit 0. Это принятые SI-E01.1 tests;
  новых tests SI-E01.2a нет и их PASS не заявляется.
- Полный baseline: **873 OK**, 840.100 s, exit 0; failures=0, errors=0,
  skipped=0. Число совпало с ранее наблюдавшимся 873, новых tests не добавлено.
  Существующие storage/D-01/golden/LAB suites прошли; S2.3 дополнительно сообщил
  1659 параметризованных сценариев, не дополнительных unittest methods.
  test_sprint23_2.Sprint232Tests.test_env_override прошёл; baseline ошибок
  окружения в текущем Linux-запуске нет. Это не Windows native qualification.
- Пример G01 независимо рассчитан stdlib JSON/hashlib и сопоставлен с принятым
  SI canonical codec: при одном semantic field/value разные path strings дают
  разные exact bytes и SHA. Это воспроизведение неоднозначности, не новый golden
  vector утверждённой record schema и не проверка существования source record.

Документационные проверки перед коммитом: git diff --check и staged diff --check
прошли; exact A-only allowlist содержит ровно два указанных документа, Markdown
links/fences валидны, source remote SHA совпал с exact base. Утверждённые original,
R1, R1a и все шесть принятых файлов SI-E01.1 побайтно совпали с pinned commits.
Между принятым SI-E01.1 и новой базой добавлены только два документа handoff/review.
После push remote commit SHA, точный parent и чистота worktree проверяются отдельно
и сообщаются в handoff. Нового record implementation PASS здесь нет.

## Границы и дальнейшее решение

SI-E01.1 остаётся ACCEPTED / PURE_FOUNDATION_ONLY. Не реализованы resolver/DAG,
run-stage ancestry, operations, storage/persistence, Discovery/Evaluation/Creative,
Production Brief/ReviewPacket execution, UI, provider/renderer или protected writes.
S3.2a PURE_ONLY; S3.2b BLOCKED_HOST_NOT_PROVIDED. PUBLISH_REVISION DISABLED,
partial COMMIT reconstruction OFF. A/E/O/D/S1/S2 и прежние golden vectors не менялись.
Native Windows не тестировался. SI-F01 остаётся nonblocking: 1 MB integer latency
не измерялась, performance claim и новый digit cap отсутствуют.

Нужен одобренный узкий path/mapping erratum и новое разрешение возобновить
SI-E01.2a на точной базе. Никакой вариант в GAPS не утверждён автоматически.
После публикации — STOP. SI-E01.2b/SI-E02, PR/merge/release не начинались.
