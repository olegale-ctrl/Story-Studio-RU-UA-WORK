# MVP-08B.3 — Independent Acceptance Record

Дата записи: 2026-11-20 (Europe/Kiev). Режим: **DOCS_ONLY / ACCEPTANCE_RECORD / ARCHITECTURE_PREPARATION**.

Точный исходный commit: `8a2164c54c97ba97d7d3a321cf4084a0926dc48c`, tree: `2b98fc63e034f3530d33d9adeb9d694f340b3a3d`. Запись приёмки ниже относится только к MVP-08B.3. Все новые решения MVP-08B.4 имеют статус **PROPOSAL / NOT_APPROVED**. Разрешения на реализацию, merge, release или production этим пакетом не создаются.

## Решение и происхождение записи

**MVP-08B.3 — ACCEPTED_WITH_LIMITATIONS.**

Это принятое ChatGPT решение передано владельцем в приложенном задании «MVP-08B.3-ACCEPTANCE / MVP-08B.4-ARCH-00». Codex фиксирует предоставленное решение, не выдаёт собственную проверку за новую независимую приёмку и не создаёт цифровую подпись либо удостоверение личности проверяющего. Полный отдельный протокол независимого аудита не приложен; основание записано в пределах формулировок задания.

Указанное владельцем основание: независимая проверка GitHub-ревизии, полного diff, исходного кода, новых тестовых сценариев и опубликованного отчёта Codex. **ChatGPT проверил код и тестовые сценарии, но не выполнял собственный независимый запуск pytest.** Числа ниже — фактические результаты Codex, а не независимый повторный запуск ChatGPT.

| Предмет | Принятое состояние | Предел |
|---|---|---|
| F-08B3-01 | CLOSED | Атрибуция эффекта конкретному job/request/mutation в принятом PURE-профиле |
| F-08B3-02 | CLOSED в пределах pure test model | Исключения COMMIT/диагностики и namespace HOLD в модели; не durable/OS qualification |
| G1–G6 | Ранее утверждённые контрактные решения | Не пересматриваются; не расширяются до native infrastructure или иных EC/OD |
| Исправление | Выполнено без расширения утверждённой области | Пять разрешённых существующих файлов; прежняя область PURE |
| Merge / production | NOT_AUTHORIZED | Приёмка ветки не разрешает слияние, выпуск или эксплуатацию |

Повторный аудит F-08B3-01/02 в этом DOCS_ONLY-задании не проводился. Исторический статус READY_FOR_RE_REVIEW в исходном RESULT остаётся без изменений; эта новая запись фиксирует последующее решение.

## Точная принятая ревизия

- Branch: `fix/mvp-08b-3-independent-acceptance-01`.
- Accepted commit: `8a2164c54c97ba97d7d3a321cf4084a0926dc48c`; tree: `2b98fc63e034f3530d33d9adeb9d694f340b3a3d`.
- Previous implementation: `ea4df639e24950cde5f925975949751f9805a8e6`.
- Tested code checkpoint: `9a01050b07482eed304ae388e886f77eb48d6ff9`, tree `359e1cc50a52b24e696839bde5d152cf960e4b3d`.
- [Опубликованный RESULT](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/8a2164c54c97ba97d7d3a321cf4084a0926dc48c/docs/tasks/MVP_OFFLINE_CORE_IMPLEMENTATION/RESULT.md); [точный controller.py](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/8a2164c54c97ba97d7d3a321cf4084a0926dc48c/experimental_mvp/offline_execution/controller.py).

Между tested checkpoint и принятой ревизией изменён только RESULT.md. Blob SHA и SHA-256 13 исходных файлов реализации/тестов/отчёта сохранены во внешнем source-manifest.json. Новая документационная ветка создаётся от accepted commit, а не от main.

## Фактические ранее выполненные проверки Codex

| Проверка | Python 3.10.22 | Python 3.13.18 |
|---|---:|---:|
| Pure core, все шесть модулей | 203 PASS | 203 PASS |
| SP regression, тестовые методы | 69 PASS | 69 PASS |
| SP subtests | 110 PASS | 110 PASS |
| FAIL / ERROR / SKIP | 0 / 0 / 0 | 0 / 0 / 0 |
| Exit codes всех соответствующих запусков | 0 | 0 |
| Таймауты | Нет | Нет |

pytest 9.2.0, Linux-6.18.57-x86_64-with-glibc2.41. SP даёт 179 JUnit records = 69 методов + 110 subtests, а не 179 отдельных методов. Все 164 исходных pure-теста сохранены; добавлены 39 кейсов исправления. Источник этих чисел — закреплённый RESULT; в текущем задании pytest не запускался. Собственная документационная проверка SHA/diff/ссылок не считается runtime-тестом.

## Ограничения принятия

Не квалифицированы Windows, NTFS/reparse/OS ownership, SQLite/долговременное хранение, реальный crash/power loss, реальные генераторы, media bytes/decoder/rights, Asset Library/save и production. FakeStore и retained Python objects не являются durable-хранилищем. **RESULT_AVAILABLE ≠ COMPLETED**; приёмка не ослабляет доказательства сохранённого проекта и остальных downstream-условий COMPLETED.

Смежные записи: [accepted baseline](ACCEPTED_BASELINE.md), [новая архитектурная граница](../MVP_08B_4_ARCHITECTURE/ARCHITECTURE_BOUNDARY.md). Статус архитектурной подготовки — READY_FOR_OWNER_ARCHITECTURE_DECISION, не IMPLEMENTATION_AUTHORIZED.
