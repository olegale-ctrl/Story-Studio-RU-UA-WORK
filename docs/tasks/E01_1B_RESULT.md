# E01.1b — первый связный набор типов (E01.1b-1)

Дата: 2026-11-04. База: E01.1 commit33d312a4d61c785fead996cd44fad67a440dcc4e. Ветка feat/editorial-e01-1b-types. Контракт прочитан из E01.1a a097c480bf1ffae2ee0e20a8c9b7900c00e185a0; E00 — e520648411b99264688ff66dc61ad0e974201ed3.

## Явное дополнение E00: Q5

По прямому решению владельца уточняется E00 §3 и E01.1a Q5: привязка проверки прав имеет subject_kind=source|asset, subject_id, subject_revision и material_digest. Глобальная уникальность UUID между ObjectKind не требуется. Ключ разрешения будущего integrity layer — (subject_kind,subject_id,subject_revision), не один UUID.

Конфликта с rights_ref нет: Source/Asset продолжают ссылаться Ref(kind=rights_review) на ревизию проверки прав. Обратная привязка subject остаётся locator, не полным Ref с content_hash, и не становится ребром dependency graph. material_digest относится к материалу, не к hash объекта с rights_ref. Это сохраняет защиту от цикла source/asset→rights→source/asset из E00.

Для совместимости существующий RightsReview не изменяется. Новый frozen RightsDetails(owner_ref, subject_kind, expires_at) хранит явный kind вместе с expiry. Wire будущего codec объединит RightsReview+RightsDetails; subject_kind — обязательный ключ. Значение не выводится из UUID, не получает default source и не теряется при round-trip. Старый RightsReview без companion остаётся допустимым минимальным value, но не полным wire-ready объектом.

В E01.3 full payload hash/digest должен учитывать subject_kind, поскольку поле семантически существенно. owner_ref companion нужен только для join, не входит в свой payload. Никаких вычислений хэша или разрешения ссылок в этой задаче нет. Валидация соответствия owner/subject и текущих прав — последующая задача. Утверждённый файл E00 не переписан; это явное дополнение по указанию владельца.

## Разделение E01.1b

Полный список затрагивает около двадцати value types и несколько независимых наборов инвариантов. Использовано разрешение остановиться на первом логически завершённом наборе:

- E01.1b-1: GenreProfile/RubricCriterion, CandidateRevision/CriterionRating, SourceDetails, ClaimReview, RightsDetails и локальные проверки. Это профили и метаданные evidence/rights до написания текста.
- Предлагаемый E01.1b-2: BriefValue, ScriptSegment, ScriptRevision, Scene, ScenePlanRevision, AssetRevision, Event, ActiveSelections, ContractSnapshot. Их реализация не начата и требует следующей проверки/разрешения. Q1–Q4 приняты, но полный aggregate/checksum остаётся в этой следующей части.

E01.2 не начинать. Existing E01.1 types/constructors сохраняются. Дополнительные поля wire-контракта не отбрасываются и не объявляются уже сериализованными.

## Реализованные файлы и типы

- editorial/model.py: добавлены RubricCriterion, GenreProfile, CriterionRating, CandidateRevision, SourceDetails, ClaimReview, RightsDetails и приватные локальные helpers. Исходная часть E01.1 файла сохранена без изменений.
- editorial/__init__.py: новые типы включены в public exports, старые имена сохранены.
- tests/test_editorial_types.py: 18 новых unit-тестов с положительными и отрицательными случаями.
- docs/tasks/E01_1B_RESULT.md: этот отчёт и явное дополнение Q5.

Локальные проверки: правильный kind собственного ref/owner_ref, типы/tuple, допустимые checked strings, UUID/revision через существующий RevisionRef, числа без bool, ASCII profile keys, Unicode без surrogates, текстовые лимиты, веса rubric=100 и уникальные keys/modes/ratings, обязательные поля review/qualification, точные реальные UTC dates. Неизвестные nullable метаданные сохраняются None; пустой assessment отличается от None. Ни codec, ни hash computation не реализованы.

GenreProfile ref UUID/revision, profile_key и version хранятся отдельно. Candidate.source_refs проверяются только по форме/kind, targets не ищутся. ClaimReview сохраняет basis человека, не утверждает фактическую истинность. RightsDetails не разрешает SOURCE/ASSET автоматически и не выводит subject_kind по совпадению id.

## Фактические проверки

Среда: Linux, Python 3.12.14, существующая .venv; новые зависимости не устанавливались.

1. `.venv/bin/python -m unittest discover -s tests -p test_editorial_types.py -v` — **18 tests, OK**, 0 failures/errors.
2. `.venv/bin/python -m unittest discover -s tests -p test_editorial_model.py -v` — **22 tests, OK**, 0 failures/errors. Старые tests не переписывались. В том числе прошёл import audit в отдельном процессе с запретом write/network/process side effects.

Проверяются legacy RightsReview positional constructor, обязательность subject_kind companion, оба допустимых kinds и запрет чужих kinds/raw strings, одинаковый UUID у разных kinds без искусственного глобального ограничения, отсутствие hash/graph логики, frozen values и вложенные tuples.

Полный suite, Sprint26 regression suites, Windows, реальный рендер/озвучка и codec не запускались в этой задаче. Их успех не заявляется. Тесты времён E01.1 не считаются новыми запусками здесь; повторены именно его 22 model tests.

## Отклонения и остаток

Единственное изменение контракта по существу — Q5 по прямому указанию владельца: subject_kind переносится в обязательный RightsDetails companion и будущий wire join, отказ от global UUID uniqueness. Существующий RightsReview не переписан. Проверка expiry относительно reviewed_at принадлежит последующей проверке связанных values: expires_at и reviewed_at находятся в разных объектах; constructor RightsDetails проверяет только свой timestamp.

Объём разделён на E01.1b-1 / предлагаемую E01.1b-2 согласно разрешению пользователя. Семь новых типов завершены и протестированы; весь E01.1b не объявляется завершённым. Q1–Q4 действуют как принятые решения, но ContractSnapshot, rights_reviews collection representation и snapshot_checksum ещё не реализованы.

Перед E01.2 остаются: завершить недостающие value types и aggregate/active mapping, обеспечить их локальные инварианты и совместимость с E01.1, затем отдельно согласовать codec. Не начинать parsing/serialization под видом новых value types. Source locator совместно с SourceDetails и subject binding разрешаются позднее; эти constructors не делают lookup.

Откат: revert только коммита E01.1b-1, без удаления production/media пользователя. Main, PR5/PR6, E00 branch, Sprint26/core/scripts/tests baseline, timeline v3, зависимости и CI не менялись. Релиз, merge, storage, workflow и E01.2 не выполнялись. После публикации ветки остановиться для проверки владельца.

## E01.1b-2 — завершение value types (2026-11-04)

Отдельная часть разрешена владельцем после принятия E01.1b-1. База ровно16d96d64bad98f2c87a0fd856d2bdff3a0f46f3e, та же ветка feat/editorial-e01-1b-types; предыдущая запись сохранена как история, её «предлагаемая E01.1b-2» больше не означает отсутствие новых типов.

Добавлены девять public immutable типов: BriefValue, ScriptSegment, ScriptRevision, Scene, ScenePlanRevision, AssetRevision, Event, ActiveSelections, ContractSnapshot. Код добавлен после прежних типов; их конструкторы не изменены. Exports дополнены, старые имена сохранены.

Локальные инварианты: правильные kinds ссылок, обязательные поля и tuple types, bool не integer, положительные/неотрицательные offsets, ограничения1..1000 сегментов/сцен, уникальность IDs, sorted unique union claim_refs внутри script, exact Unicode text без нормализации, непрерывность и порядок диапазонов сцен. Равенство narration slice с referenced script не проверяется до E01.5. Лимит20 сцен остаётся downstream capability, не ограничением editorial plan.

AssetRevision сохраняет supplied SHA-256, relative POSIX path с ограничениями Windows reserved names/characters/length и пару script_ref/text_digest. Файлы не читаются, junction/symlink/существование/реальные hashes не проверяются. Учётный kind=video допустим, Scene.visual_kind только still; это не реализация video renderer. Event хранит данные, не исполняет action.

ContractSnapshot(base,source_details,claim_reviews,rights_details,events,snapshot_checksum) сохраняет исходный EditorialSnapshot. Проверяет типы/tuple, формат checksum, локальную уникальность records, concrete revision payloads и нормативный порядок групп/id/revision. Не пересортировывает данные. active_selections — immutable проекция base.active_refs по четырём nullable slots; неизвестные kinds/duplicates/order rejected. rights_reviews — отдельная typed projection, предназначенная для будущей отдельной JSON-коллекции. Код сериализации отсутствует.

Наличие всех companions/targets, совпадение owner payload/hash, целостность графа и approval authority не объявляются проверенными: это следующий уровень. Даже полный по форме aggregate может содержать unresolved refs. Базовый минимальный EditorialSnapshot по-прежнему допускает прежние конструкторы; усиления относятся только к новому ContractSnapshot.

Q5 сохранён: subject_kind обязателен в RightsDetails, без inference и без global UUID uniqueness. Сравнение RightsDetails.expires_at с RightsReview.reviewed_at явно отложено до связанной проверки; constructor не ищет другой объект и не использует текущее время. Wire codec обязан будет объединять companion metadata без потери subject_kind/expiry. Ни E00, ни E01.1a молча не переписаны.

### Файлы E01.1b-2

1. editorial/model.py — новые types/helpers, без правки старой части.
2. editorial/__init__.py — дополнительные public exports.
3. tests/test_editorial_content.py — отдельный тестовый файл для читаемости; старые tests/test_editorial_model.py и test_editorial_types.py не изменены.
4. docs/tasks/E01_1B_RESULT.md — это дополнение.

### Фактическое тестирование E01.1b-2

Linux, Python3.12.14, существующая .venv, без установок. Команды:

- `.venv/bin/python -m unittest discover -s tests -p test_editorial_content.py -v` — **24 tests, OK**.
- `.venv/bin/python -m unittest discover -s tests -p test_editorial_model.py -v` — **22 tests, OK**.
- `.venv/bin/python -m unittest discover -s tests -p test_editorial_types.py -v` — **18 tests, OK**.

Итого **64 tests, OK** (24+22+18). Это число test methods; subTest scenarios не считаются дополнительными самостоятельными tests. Полный suite, Windows, FFmpeg/TTS/render/API не запускались. Старый import-isolation test прошёл повторно.

### Открытые вопросы и границы перед E01.2

Архитектурных изменений сверх принятого Q5 не потребовалось. JSON envelope остаётся отдельными коллекциями E00/E01.1a; общий внутренний tuple не является заменой wire schema. В E01.2 нужно реализовать strict field mapping и обратимый join с companions; вычисление checksum/content_hash/digest не включать. Даты/checked strings старых E01.1 объектов всё ещё могут быть слабее wire contract, поэтому codec обязан диагностировать их явно, без изменения значений.

E01.3 должен проверить exact refs и owner cardinality, материал/права/expiry и hash integrity. E01.5 — полный текст scene↔script и handoff capability. При приёмке не считать constructor ContractSnapshot доказательством этих properties.

E01.2 не начат: parsing/serialization, canonical hashing, graph traversal, save/locks, workflow и медиа отсутствуют. Новый отдельный коммит E01.1b-2 предназначен для review; merge/main/release не выполняются. После результата остановиться для проверки владельца.
