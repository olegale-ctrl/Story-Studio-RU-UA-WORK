# E01.3.9.3 / S2.1 — Pure Storage Protocol Primitives: результат

**Дата:** 2026-11-06. **Статус:** реализованы чистые in-memory wire/crypto primitives;
не защищённое хранилище и не подтверждение production readiness.

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Base: `docs/editorial-e01-3-9-2b-s1-approved-contract`,
  `6f765766248014009527499007948d8817bbca0a`.
- Branch: `feat/editorial-e01-3-9-3-s2-1-storage-wire-crypto`.
- Нормативная редакция S1a: `83ac4ac3fa5104a9a43bc2fa5f98d735a694f49c`,
  утверждённая [S1b](E01_3_9_2B_S1_APPROVED_CONTRACT.md).
- GitHub storage policy учтена непосредственно из отдельного коммита
  `ceca15c20cedd5277ad0bdafc418eef149e7bc7b`, без merge этой ветки.

## Созданные файлы

1. `editorial/storage_protocol_v1.py` — только стандартная библиотека и повторное
   использование существующих редакционных wire validators/declaration codes.
2. `tests/test_storage_protocol_v1.py` — искусственные fixtures, буквальные
   независимые expected values и отрицательные проверки.
3. Этот документ `docs/tasks/E01_3_9_3_S2_1_RESULT.md`.

Существующие файлы, редакционные модели, digest/checksum и утверждённые контракты
не изменены. Реальных ключей, principal, journal/anchor или production данных нет;
SID/UUID/actor взяты из публичного искусственного примера контракта.

## Реализация и границы API

- `canonical_json` / `decode_canonical_json`: точный UTF-8 без BOM, сортировка
  Unicode code points, порядок массивов и исходный Unicode сохранены. Duplicate
  keys, floats, NaN/Infinity, surrogates, неподдерживаемые Python types,
  неканонические bytes и превышение depth/size отклоняются без исправления.
- U64 проверяется без bool/coercion/IEEE-754. Generation не получает искусственный
  U64 cap; большие целые обрабатываются без изменения глобальных Python settings.
- `request_digest`, `approval_wire_digest`; `frozen_command_mac`, `anchor_mac`,
  `receipt_mac`, `initialization_mac`, `registration_mac`, `journal_frame_mac`:
  утверждённые domain bytes и SHA-256/HMAC-SHA-256. Явный ключ ровно 32 bytes;
  отсутствует default/fallback, provisioning, загрузка или сохранение ключей.
- `verify_mac` и `decode_journal_frame` используют `hmac.compare_digest`.
- Закрытые схемы проверяются через `validate_wire`; `blob_ref` / `verify_blob`
  проверяют exact hash/length и ожидаемый тип, без угадывания типа или dereference.
- Journal: `SSJ1 + uint32_be(N) + C(record) + raw HMAC32`, N=1..1048576;
  ровно один полный frame, без trailing bytes, resync, пропуска/усечения хвоста.
  StructuralError и CryptographicError раздельны; ошибки содержат code/path.
- `verify_journal_frames` атомарно проверяет переданную непустую in-memory
  последовательность от index 0, previous MAC, production/machine/epoch/key context.
  `verify_record_plan` отдельно связывает предоставленные plan/command refs,
  context и terminal receipt; сам ничего не загружает.
- MAC/frame/type validity **не** означает authorization, effective approval,
  readiness или полную корректность транзакции. `verify_journal_frames` не
  интерпретирует W0–W9; `verify_record_plan` не заменяет authenticated history,
  policy/provider lookup и replay всех доказательств. Caller обязан отдельно
  проверить MAC предоставленных proofs и полный transition/guard graph на будущем
  этапе; ни один primitive не возвращает флаг trust/authority.

PUBLISH_REVISION отклоняется; generic snapshot writer не создан. Partial COMMIT
reconstruction отсутствует и остаётся OFF. Нет service, DPAPI/ACL/IPC, файловых
операций, сети, key generation или внешних действий при импорте модуля.

## Golden vectors и отрицательные случаи

В тестах воспроизведены положительная история G (`J0 → J1 → J2`) и отдельная
история A (`J0 → JA`). Сравниваются **буквальные** значения утверждённого S1 §13:

- 20 canonical object lengths / SHA-256, включая S/H/Q и все зависимые объекты;
- domain-separated Request digest;
- шесть body HMAC и четыре journal frame HMAC;
- точные headers, payload lengths и full-frame lengths.

Fixtures строятся независимо от MAC functions tested module: stdlib JSON/plain
SHA плюс literal reference MACs из контракта. Все 20 SHA и 10 HMAC literals
дополнительно сверены с текстом approved S1a. Для Approval wire domain добавлен
отдельный synthetic пример с literal expected digest, рассчитанным OpenSSL;
это дополнительная проверка, не новый утверждённый контрактный vector.

Проверены duplicate/unknown/missing fields, version, floats/NaN/Infinity,
неканонический JSON, invalid UTF-8, surrogate keys/values, depth/size, U64
boundaries, Generation в 4501 decimal digits, composed/decomposed Unicode,
length/MAC/key failures, подмена blob type, index gaps/forks/previous MAC/context,
повреждения frame, **каждый proper prefix GENESIS frame**, отсутствие partial
successful chain result и поиск следующего magic, который никогда не выполняется.
Также проверены frozen grant bindings всех 12 gate×decision пар, запрет
неявного grant inheritance, disabled revision и отсутствие I/O/key generation/
network при повторном исполнении тела модуля. Эти scopes синтетические, без
реального authentication/provider/authorization.

## Фактически выполненные проверки

Окружение: Linux cloud workspace, Python 3.12.14, CPU; Windows не использовалась.

| Проверка | Результат |
|---|---|
| `python -m unittest tests.test_storage_protocol_v1 -v` | 69 tests, OK, 0 errors/failures |
| Первый `python -m unittest discover -s tests -v`, системный Python | 701 tests, 1 import error: существующий `test_sprint20` требует отсутствующий в системном Python pytest; storage tests прошли |
| `python -m unittest discover -s tests -v`, с `.venv/bin` первым в PATH | 708 tests, OK, 0 errors/failures; использован уже установленный pytest 9.2.0 |
| Literal expected cross-check с approved S1a | 20 SHA-256 и 10 HMAC присутствуют и совпадают |
| `git diff --check`, staged diff check | Успешно |
| Состав и размеры файлов, repository policy hygiene | Только три разрешённых новых текстовых файла, каждый меньше 10 MiB; `.gitignore` не изменён |

Во время разработки исправлена ошибка названия поля snapshot в test fixture;
финальные expected literals контракта не менялись. Разница 701/708 обусловлена
добавленными тестами и отсутствием placeholder import error в успешном запуске.
Unittest не собирает pytest-style functions; 708 — число именно unittest tests,
не утверждение о запуске отдельного pytest набора. Новых зависимостей не установлено.
Логи остаются вне Git; временные рабочие данные существующих tests не являются
storage implementation этого этапа.

## Неоднозначности и ограничения проверки

Блокирующих противоречий между утверждёнными документами для S2.1 не обнаружено.
S1b снимает исторический PROPOSAL status только с точно указанной S1a редакции;
квоты Q1, конкретные Windows profiles и provider deployment не считаются выбранными.

За пределами этого результата: W0–W9, reconciliation/crash recovery,
полный guard/history replay, idempotency/admission, OS identity/policy lookup,
durable storage, actual Windows tests и process/power-loss qualification.
Admission-only negative cases S1 (например, import старого approval, восстановление
anchor из backup) здесь не объявлены протестированными: этих операций нет в S2.1.
Existing schema-1/2 golden bytes и API сохранены; полный unittest набор прошёл.

После commit/push — **STOP**. S2.2 требует независимой проверки этого результата.
PR, merge, release и изменение main не выполняются.
