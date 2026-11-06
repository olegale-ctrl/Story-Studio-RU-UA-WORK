# E01.3.9.4 / S3.2a — normative byte conflict

Дата: 2026-11-06. Статус: **BLOCKED_CONTRACT_CONFLICT**.
Квалификация: никаких новых PURE_ONLY/S3_2A_PORTABLE_TESTED результатов не получено.

## Base и состав

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Base branch: `docs/editorial-e01-3-9-4-s3-2a-approved-task`.
Exact base: `747ea3de5cb623df8fdfaa5dff6af58f893cc698`; FETCH_HEAD совпал.
Output branch: `feat/editorial-e01-3-9-4-s3-2a-portable-lab-core`.
HEAD до отчётного commit равен base; итоговый полный HEAD и URL публикуются в handoff
после commit/push, поскольку self-reference в содержимом commit невозможен.

Создан только `docs/tasks/E01_3_9_4_S3_2A_RESULT.md` из разрешённого списка.
Его Git blob определяется `git rev-parse HEAD:docs/tasks/E01_3_9_4_S3_2A_RESULT.md`
и сообщается в handoff. Ни одного исполняемого файла не создано/изменено.

## Блокирующее противоречие

Прочитаны полностью owner decision и нормативное S3.2a task, а также split proposal.
Точная база закреплена. На сверке формулы terminal summary обнаружено расхождение:

- [S3.1a §3.3](E01_3_9_4_S3_1A_LAB_EXECUTION_CONTRACT.md), строки 309–312:
  `SHA256(ASCII("story-studio-s3-2-lab-result-v1") || byte 00 || R)`;
  текст явно требует ровно один NUL, без backslash escape bytes.
- [S3.2a §4](E01_3_9_4_S3_2A_CODEX_TASK.md), строка 77:
  `SHA256(b"story-studio-s3-2-lab-result-v1" + b"\\x00" + exact_canonical_internal_receipt_bytes)`.
  В Markdown code span буквально два backslash; Python bytes literal обозначает
  четыре байта backslash/x/0/0, а не один NUL. Markdown не снимает экранирование
  внутри code span.

Owner decision сохраняет exact technical constraints S3.1a, кроме явно описанных
host/hash sequencing amendments. Изменение digest separator им не утверждено.
S3.2a §1 и handoff требуют STOP при нормативном конфликте, без молчаливого расширения
или изменения утверждённого контракта. Поэтому разработка остановлена до создания
LAB protocol/factory/dispatcher/tests. Полное implementation чтение S1/S2 и запуск
acceptance suites ещё не завершались; этот отчёт не выдаёт сверку формулы за них.

## Минимальное воспроизведение

Выполнено на доступном Linux/Python 3.12.14; использованы только искусственные bytes:

```python
import hashlib
prefix = b"story-studio-s3-2-lab-result-v1"
r = b"{}"
for separator in (bytes([0]), b"\\x00"):
    print(separator.hex(), len(separator),
          hashlib.sha256(prefix + separator + r).hexdigest())
```

Буквальный вывод:

```text
00 1 66c044a3fa04b1baa95c05de618167622684843f04c4dde11e70add46870bcea
5c783030 4 8acda446a8aae48decc364502a3b476565fd8e9b3048a950ce6c5ec2e4854e25
```

`{}` здесь только общий byte suffix, не валидный S1 Receipt и не новый golden vector.
Различие separator устанавливается независимо от содержимого receipt. Ни одного
receipt, ключа или production данных для воспроизведения не требуется.

Рекомендуемое уточнение для владельца: явно подтвердить один байт `00` как в S3.1a
и исправить пример S3.2a на Python `bytes([0])` либо `b"\x00"` с одним backslash.
Утверждённые документы в этой ветке не исправлялись. Намерение автора формулы
не заменяет решение о точных криптографических bytes.

## Проверки, покрытие и ограничения

Выполнены сверка base/FETCH_HEAD, чтение конфликтующих строк с `repr`, Python
вычисление выше, проверка локальных Markdown links/fences, `git diff --check`,
состава изменений и размера файла. Нативные действия не выполнялись.

Новые protocol/dispatcher unittest и существующие storage/full discovery в рамках
этого S3.2a запуска **не запускались**: сработало условие STOP до реализации.
Количество новых executable tests: 0; LAB parameterized scenarios: 0.
Три byte oracles, 144-cell matrix (12 allow/132 deny), replay, capacity и faults
**NOT RUN / BLOCKED**, успешные результаты не заявляются.

| LT | Статус |
|---|---|
| LT01 | BLOCKED — native SCM/installation вне S3.2a |
| LT02 | BLOCKED — native lifecycle вне S3.2a |
| LT03 | BLOCKED — native ACL вне S3.2a |
| LT04 | BLOCKED — native server identity вне S3.2a |
| LT05 | BLOCKED — native SID/SQOS вне S3.2a |
| LT06 | BLOCKED — native impersonation вне S3.2a |
| LT07 | BLOCKED — pure codec не реализован; native IO вне scope |
| LT08 | BLOCKED — native cancellation вне S3.2a |
| LT09 | BLOCKED — 144-cell matrix не запускалась |
| LT10 | BLOCKED — mock grant tests не запускались |
| LT11 | BLOCKED — replay/lookup tests не запускались |
| LT12 | BLOCKED — simulated crash/restart tests не запускались |
| LT13 | BLOCKED — capacity tests не запускались |
| LT14 | BLOCKED — нет runtime/audit; native observer вне S3.2a |
| LT15 | BLOCKED — LAB separation/S2 regression suites здесь не запускались |

RISK-01 и RISK-03: BLOCKED native. RISK-02: native BLOCKED, pure codec NOT RUN.
RISK-04: pure subset NOT RUN, native BLOCKED. LAB_SERVICE_TESTED,
PROCESS_QUALIFIED, POWER_LOSS_QUALIFIED не получены.

Нет OS authentication, ACL, native IO, protected writer или persistence. Существующие
S1/S2/D-01/golden и approved decisions не изменены. PUBLISH_REVISION DISABLED;
partial COMMIT reconstruction OFF. Windows HostProfile не требовался и не выдуман.
Нет реальных SID/passwords/keys/manifests/media, новых dependencies или бинарников.
Публикуется только feature branch; без PR/merge/release/main changes.

**STOP до разрешения точного separator conflict. S3.2b/S3.3 не начаты.**
