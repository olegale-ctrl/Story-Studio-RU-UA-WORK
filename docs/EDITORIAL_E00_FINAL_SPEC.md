# E00 — финальная спецификация Universal Editorial Engine

Дата: 2026-11-04. Версия спецификации: E00/1. Статус: шесть продуктовых решений приняты владельцем; ниже уточнён инженерный контракт. Реализация E01 и последующих этапов **не разрешена этим документом**.

Основание: [аудит F01–F14](CODEX_EDITORIAL_FEASIBILITY_AUDIT.md), [план MVP](EDITORIAL_MVP_IMPLEMENTATION_PLAN.md), сохранённые на commit260a142401b45707b2b9ed650b0dbc6ab8ca8632. Рабочий код Sprint26 остаётся e1f4efb0fb5ff290bb198349213c004b4667ef0f. Этот документ имеет приоритет над предложенными defaults двух исходных отчётов; исторический текст не переписывается.

## 1. Принятые решения

| Решение владельца | Нормативный контракт |
|---|---|
| CLI-first | Первый интерфейс — отдельный локальный CLI; GUI позже, домен не зависит от CLI |
| Единый JSON snapshot | Один authoritative editorial.json с immutable revisions и approvals; атомарное сохранение, межпроцессный writer lock и expected_generation |
| Совпадение языков | Для первого handoff script_locale=narration_locale=subtitle_locale, только ru или uk. UI locale независимо. UK означает код uk, не ua |
| Формат | Новый editorial production по умолчанию 9:16:720×1280. Явный 16:9:1280×720. Старые defaults first_video не меняются |
| Факты, права, утверждения | Material facts требуют явного human review; права ограничены intended-use; export принимает только актуальный утверждённый dependency snapshot |
| Offline-first | Ручные темы/URL metadata, evidence, сценарий и сцены работают без сети, LLM и paid API. URL не вызывает автоматический fetch |

Универсальность реализуется versioned GenreProfile как данными. Genre и content_mode независимы: factual/fictional/hybrid. Три исходных профиля — history_biography, science_technology, fiction_storytelling; general_custom использует тот же контракт. Новые профили не являются исполняемыми plugins.

## 2. Минимальный snapshot

Envelope: editorial_schema_version=1, production_id, generation (целое >=1), production_revisions, profiles, candidates, sources, claims, scripts, scene_plans, assets, approvals, events, active_refs. Все коллекции содержат только данные одной production. Empty draft collections допустимы. schema_version timeline v3 не используется для editorial envelope.

Общая RevisionRef: kind, id, revision (целое >=1), content_hash. Все ссылки разрешаются точно; floating latest в зависимостях запрещён. ID — UUID, не имя файла или заголовок. Hash — SHA-256 lowercase hex64. История не удаляется при переключении active_refs.

| Объект | Обязательные поля/правила |
|---|---|
| ProductionRevision | id/revision, title, profile_ref, content_mode, script/narration/subtitle/UI locales, intended_use, output_preset, created_at. Активные ссылки — в envelope, изменение выбора не переписывает старый payload |
| GenreProfile | id/version, ru/uk display names, allowed_modes, narrative structure, review_policy_version; rubric optional, не prediction |
| CandidateRevision | id/revision, title/summary, source_refs[], manual provenance, optional assessment/rationale; один выбранный candidate достаточен |
| SourceRevision | id/revision, title, URL либо безопасный local locator, известные/null автор и даты, rights_ref, access/review notes. Source production-scoped, reusable |
| ClaimRevision | id/revision, statement, factual/interpretation/fictional, materiality, review decision/qualification, reviewer/time/reason, evidence_links[] |
| EvidenceLink | source_ref, relation supports/contradicts/context/insufficient, точный locator, explanation, reviewer/time; source/claim не объединяются |
| ScriptRevision | id/revision, production_ref, candidate_ref, frozen brief, locale, ordered segments, exact claim_refs, content_hash. Brief — вложенный versioned value без отдельного сервиса |
| ScriptSegment | id, exact narration text, role, claim_refs[], optional visual/pronunciation notes; вымысел/интерпретация помечены явно |
| ScenePlanRevision | id/revision, script_ref, ordered scenes, content_hash. Scene: stable id, ranges по script text, narration_text, still brief, optional asset_ref, estimate_ms/null |
| AssetRevision | id/revision, relative file_ref, sha256, kind, rights_ref, optional scene/text binding. Не хранит бинарные данные внутри JSON |
| RightsReview | id/revision, exact material/source hash/ref, intended_use, allowed_actions, approved/restricted/unknown/blocked, reviewer/time/basis, optional expiry. Review не создаёт отсутствующие права |
| ApprovalRecord | id, gate, object_ref, dependency_digest, policy_version, actor, timestamp, approve/reject/revise/revoke, reason, review declarations |

Event — минимальная запись изменения внутри snapshot: id, actor/time, action, refs, reason/error. Не нужен отдельный event-sourcing server, SQLite, очередь jobs или journal authority. Assets и media paths не становятся полями v3.

## 3. Валидация и хэширование

UTF-8 без BOM при записи; формат UTC timestamp YYYY-MM-DDTHH:MM:SSZ. Невалидные даты отклоняются, неизвестные остаются null. Strict JSON: duplicate keys, NaN/Infinity, неизвестная schema version/fields и bool вместо integer отклоняются. Текст сохраняется без неявного trim, NFC, перевода и перестановки; для проверки непустоты используется отдельный predicate.

E01 limits: snapshot до32MiB, до10000 revisions суммарно, отдельное текстовое поле до100000 code points, до1000 narration segments. Превышение — понятная ошибка, не truncation. Лимит handoff2000 символов/scene применяется отдельно; большой editorial draft разрешён до production adaptation.

Canonical bytes: json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8'). Hash computed over exact immutable semantic payload с kind/id/revision/schema; content_hash и audit timestamps вне этого payload. MVP не использует floats в hashed contract: estimates/ratings — integers, unknown=null. Отдельный snapshot checksum охватывает всё envelope без самого checksum, включая generation, approvals и events.

Dependency digest: SHA-256 canonical объекта с gate/policy_version, target_ref, relevant production/profile refs и отсортированным по(kind,id,revision) списком точных transitive RevisionRef. Конфликтующие версии одного id в одном активном пакете отклоняются. Cycle, missing ref, foreign production и неверный hash — ошибки. Это consistency check, не цифровая подпись или автоматический фактчекинг.

RightsReview связывается с subject id/revision и material_digest исходных bytes/цитируемого материала, а не с полным Source/Asset hash, уже содержащим rights_ref. Это исключает взаимную хэш-ссылку source→rights→source. Проверка subject binding обязательна; такой обратный locator не является ребром transitive revision graph. Snapshot checksum считается после завершения всех object hashes; approvals не входят в hash утверждаемого payload, но входят в checksum snapshot. JSON floats в контракте E01 отклоняются рекурсивно, не только при сериализации.

## 4. Approvals и существенные факты

Gate SCRIPT требует: exact script; человек подтвердил покрытие всех material assertions; factual claims supported либо qualified с утверждённой формулировкой; visible contradictions; права intended-use допустимы; языки совпадают. Простого claim_id или URL недостаточно. Removed claim не оправдывает оставшуюся в тексте фактическую фразу. Disputed material claim блокирует gate до qualification/removal и повторного review.

Fictional assertions не требуют ссылок и не получают вымышленных evidence. Реальные факты внутри fiction/hybrid проверяются обычным образом. Hybrid требует disclosure художественных реконструкций; это часть approved текста/metadata.

Gate SCENES требует актуального SCRIPT approval и точного покрытия narration. Gate HANDOFF требует обоих approvals, текущих rights и frozen asset hashes/config. Никакое status=approved или переданное CLI поле не создаёт approval. Stage/readiness — вычисляемые проекции.

Значимое изменение source, claim, profile, языка, intended-use или script создаёт новую revision. Старые approvals остаются историческими, но active downstream пакет stale, пока не создан coherent новый набор и не пройден review. Зависимые decisions не переносятся по совпадению текста. Не связанная с narration замена still image не меняет SCRIPT gate, но меняет SCENES/HANDOFF rights/assets digest. Выбор старой согласованной версии допускается только явно, с проверкой текущих прав и revocations.

Повторный approve того же gate/ref/digest идемпотентен; reject/revise/revoke для него не игнорируется по более раннему approve. Revoked digest нельзя оживить простым изменением status; нужен новый human review. Actor — локально указанный reviewer, не доказанная identity service.

## 5. Точное покрытие текста

Narratable text = конкатенация ordered segment.text без автоматически вставленных separators. Разделительные пробелы/переносы входят в утверждённые segments. Offsets — Unicode code points, start inclusive/end exclusive; не байты и не UTF-16. Тексты с unpaired surrogates отклоняются.

Scene ranges должны идти подряд от0 доlen(text), не пересекаться, не оставлять gaps и не иметь нулевой длины. narration_text каждой сцены равен exact slice; конкатенация сцен равна approved text. Перестановка/перефразирование возвращает workflow к новой ScriptRevision. Empty/whitespace-only сцена блокирует handoff; пробелы перераспределяются через корректное изменение ranges, не скрыто удаляются.

## 6. Хранение и конкурентная запись (E02, контракт фиксируется сейчас)

Single local writer на production. Постоянный lock file использует OS lock: Windows msvcrt, POSIX flock; OS adapter изолирован, shared/network filesystems вне MVP. Lock удерживается на read-check-write transaction, освобождается при выходе/смерти процесса. Не удалять lock path на каждом save: inode replacement может нарушить взаимное исключение. Busy lock даёт LOCK_BUSY, не force unlock по возрасту/PID.

save(expected_generation): acquire lock → reread/validate current → сравнить generation → сформировать next_generation=current+1 в сохраняемом envelope → validate new snapshot → записать sibling temp → flush/fsync → сохранить предыдущий валидный snapshot через atomic backup replace → os.replace temp→editorial.json. Commit point — замена primary. Failure до неё не меняет primary; отказ после неё требует reread generation/checksum, не blind retry. Directory fsync на поддерживаемых POSIX; Windows power-loss guarantees не обещаются без испытаний.

Reader видит старый или новый целый snapshot, сверяет checksum. Повреждение primary → явный recovery из валидного backup с сообщением о более ранней generation; не silent restore и не автоматическое approved. Orphan temps не становятся current. Memory-only unsaved edits не выдаются за durable state. File-in-use/disk-full/permission failure возвращают structured error, старые данные сохраняются где commit point ещё не пройден.

## 7. Production handoff

Существующие ограничения проверены по [first_video.py](../scripts/first_video.py)25–39/72–152, [schema](../core/project_schema.py)202–234 и [renderer](../core/mp4_render.py)42–74. Старый код не изменяется.

- Экспортировать только title, locale, scenes с text и optional image. Metadata/evidence/approvals — в sidecar; timeline v3 остаётся прежним.
- 1–20 сцен, непустой text до2000 code points, только still images PNG/JPG/JPEG/PPM с simple filenames. AI/imported MP4 отклоняется явно; gradient fallback только по явному выбору.
- Default720×1280, alternate1280×720 передаются wrapper через --width/--height; существующий default1280×720 не переписывается.
- Ровно один audio source: voice1.wav... по scene order либо уже установленный явно доверенный Silero с подходящим голосом. WAV manifest связывает scene/text/audio hashes. Язык/смысл existing WAV подтверждает человек.
- Фактический timing: WAV milliseconds +400ms, округление вверх к40ms/25fps. Estimate хранится отдельно; не неподдерживаемый --duration.
- Frozen handoff имеет script/scene/config/assets digest. Повторная проверка непосредственно перед стартом. Managed staging с проверенными hashes; writer не изменяет его во время render. Для пользовательских внешних files абсолютная защита от внешнего конкурентного writer не обещается: копировать в staging и проверять до/после, при mismatch результат rejected.
- Каждый запуск имеет новый attempt directory. Existing output не перезаписывается; failed partial output не считается ready; approved editorial state не теряется, старые файлы пользователя не удаляются.

## 8. Права и пути

Production intended_use=test/personal/commercial не означает grant. RightsReview оценивает конкретные действия (quote/import/render/distribute), материал и scope; unknown/blocked/expired запрещают соответствующее действие, не обязательно мешают сохранить draft. Тестовое разрешение не переносится на commercial export.

UUID-based managed paths; UTF-8, pathlib, запрет traversal, absolute/drive/UNC refs, reserved Windows names, symlink/junction escape. Разрешённый внешний media source импортируется отдельно в staging. Credentials, полные приватные тексты и binaries не попадают в logs/Git. Сеть/LLM/model downloads не выполняются побочно от чтения production.

## 9. Закрытие F01–F14 на уровне спецификации

| Finding | Нормативное решение | Будущий acceptance |
|---|---|---|
| F01 | §1/7 одинаковые языки | ru/uk проходит, mismatch blocked |
| F02 | §3/4 dependency digest | source edit при том же script делает gate stale |
| F03 | §2 точные immutable refs | latest/dangling/conflicting revisions rejected |
| F04 | §4 human material coverage | URL/id без review не открывает gate |
| F05 | §5 точные ranges | gap/overlap/rewrite/reorder rejected |
| F06 | §6 единый atomic snapshot | crash до commit сохраняет old, после — valid new |
| F07 | §7 frozen package/recheck | asset mutation блокирует acceptance |
| F08 | §7 estimate отдельно | actual WAV timing не подменяется estimate |
| F09 | §1/7 dimensions передаются явно | default9:16, explicit16:9 |
| F10 | §7 attempts | partial output не overwrites и не ready |
| F11 | §1/4 mode не genre | fiction без fake evidence, реальные facts reviewed |
| F12 | §2/4 production-scoped sources/profile | reuse без копирования, смена профиля создаёт revision |
| F13 | §4 approvals authority | forged approved/stage не открывают gate |
| F14 | §8 scoped rights | personal grant не разрешает commercial |

«Закрыто» здесь означает определённый контракт, не пройденные runtime тесты. [E01](EDITORIAL_E01_IMPLEMENTATION_PLAN.md) реализует только pure model/validation после отдельного разрешения. Store — E02, service/gates — E03/E04, handoff/render — E06/E08; полноценный GUI, models, поиск, analytics и publishing позже.
