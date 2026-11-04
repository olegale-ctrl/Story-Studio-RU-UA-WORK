# E01.1a — полный контракт модели для будущего JSON codec

Дата: 2026-11-04. Версия проекта контракта: E01.1a/1. **Только спецификация; кода и тестов не добавлено.** Реализация E01.2 не начата. Все формулировки ниже описывают будущие типы, а не уже существующий API.

База: E01.1 [33d312a4d61c785fead996cd44fad67a440dcc4e](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/33d312a4d61c785fead996cd44fad67a440dcc4e/editorial/model.py). Утверждённая [E00/1](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/e520648411b99264688ff66dc61ad0e974201ed3/docs/EDITORIAL_E00_FINAL_SPEC.md), §§2–5, остаётся исходной нормой. [Отчёт E01.1](E01_1_RESULT.md) прямо предупреждает о неполных payloads и отсутствии wire schema.

## 1. Принцип и необходимые уточнения E00

Codec не должен придумывать новые сущности, терять поля или считать EditorialRevision(ref) полноценным Script/Scene. E01.1 не переписывается. Для полного контракта потребуются отдельная согласованная задача добавления value types и companion metadata, затем codec. Это не поручение выполнять обе задачи автоматически.

| Вопрос к E00 | Конкретное основание | Минимальное предлагаемое решение |
|---|---|---|
| Q1: отсутствует коллекция прав | §2 перечисляет envelope без rights_reviews, но объекты Source/Asset имеют rights_ref, а RightsReview — отдельная ревизия | Добавить обязательную коллекцию rights_reviews. Без неё полная round-trip сериализация прав невозможна |
| Q2: checksum не назван полем envelope | §3 требует snapshot checksum, §2 не указывает имя/тип | Добавить обязательное snapshot_checksum: Hash. Codec проверяет форму, E01.3 вычисляет/сверяет; до E01.3 codec не заявляет integrity verification |
| Q3: старый envelope неполон | E01.1 имеет revisions/approvals/active_refs, но не events/checksum/source metadata/claim review; E00 §§2–4 требуют их | Отдельный полный value aggregate ContractSnapshot с сохранённым base:EditorialSnapshot и immutable companions. Не игнорировать поля и не использовать mutable unknown-fields dict |
| Q4: profile id/version | E00 §2 требует UUID для IDs, но профиль назван history_biography и имеет version | UUID/ref — идентичность ревизии; profile_key — семантическое имя; version — явно сохранённая строка версии. Не подменять UUID ключом профиля |
| Q5: права с subject id без kind | E00 §3 и существующий RightsReview имеют subject_id/revision, без subject_kind | IDs уникальны между kinds в одной production; E01.3 разрешает subject только к Source/Asset, material_digest не создаёт обратного hash-edge. Иначе потребуется отдельное расширение subject_kind |

Это **явные предложения уточнения**, не молчаливые изменения утверждённой E00. Приведённая ниже wire schema полностью определена при принятии Q1–Q5. До решения владельца её нельзя объявить утверждённой schema v1 и реализовать как окончательный codec. Бизнес-решения CLI/offline/языки/формат не пересматриваются.

## 2. Общие типы и форма объектов

Обозначения: Text — str с хотя бы одним непробельным code point; String — любая str, включая пустую; UUID — lowercase canonical hyphenated UUID string; Hash — ровно64 lowercase hex; PositiveInt — int>=1 без bool; NonnegativeInt — int>=0 без bool; UTC — существующая календарная дата YYYY-MM-DDTHH:MM:SSZ. Nullable(T) — T или null. List(T) — JSON array, внутри модели tuple[T,...]. Ref — объект строго {kind,id,revision,content_hash}, без иных ключей.

Все строки — Unicode без unpaired surrogates, exact spelling и whitespace сохраняются; нет trim/NFC, locale fallback или coercion. Максимум100000 code points на строковое поле; ограничения E00 32MiB на snapshot,10000 revisions суммарно,1000 segments на Script. Дополнительно safety caps: глубина JSON<=64; до10000 элементов в любой коллекции/вложенном списке, кроме script segments<=1000. Отказ вместо усечения.

Каждая ревизия в wire имеет **ref плюс перечисленные ниже поля**, не плоские копии kind/id/revision/hash. Наследуется E01.1 форма EditorialRevision(ref). Hash semantic payload уточняется E01.3 по E00; codec его не вычисляет. Нельзя сохранять ref-only header в полноценную domain collection.

Существующие enum wire значения:

- ContentMode: factual, fictional, hybrid; Locale: ru, uk (не ua/RU/UK).
- ObjectKind: production, genre_profile, candidate, source, claim, script, scene_plan, asset, rights_review.
- ApprovalDecision: approve, reject, revise, revoke.
- RightsStatus: approved, restricted, unknown, blocked.
- ClaimType: factual, interpretation, fictional.
- EvidenceRelation: supports, contradicts, context, insufficient.

Следующие закрытые значения пока могут быть checked strings, новые enum не обязательны: intended_use=test|personal|commercial; output_preset=9:16|16:9; materiality=material|context; role=opening|body|closing|other; review_status=unreviewed|supported|disputed|unverified|qualified|removed; gate=SCRIPT|SCENES|HANDOFF; source_type=url|local; media kind=image|audio|video. Неизвестные значения codec отклоняет, не заменяет unknown. Смена wire vocabulary требует версионирования.

## 3. Полное сопоставление E00 и E01.1

| Объект E00 | Состояние E01.1 | Определённый целевой носитель |
|---|---|---|
| ProductionRevision | Есть все основные поля | Сохраняется без смены сигнатуры; full codec уточняет допустимые строки/UTC |
| GenreProfile | Есть только ObjectKind | Новый GenreProfile(EditorialRevision), §4 |
| CandidateRevision | Kind без payload | Новый CandidateRevision(EditorialRevision), §4 |
| SourceRevision | title/locator/rights_ref | Старый SourceRevision + SourceDetails companion, §5 |
| ClaimRevision | statement/type/materiality/evidence_links | Старый ClaimRevision + ClaimReview companion, §5 |
| EvidenceLink | Полный минимальный value есть | Сохраняется; внутри Claim, не самостоятельная revision |
| ScriptRevision/ScriptSegment | Только kind script | Новые типы, §4 |
| ScenePlanRevision/Scene | Только kind scene_plan | Новые типы, §4 |
| AssetRevision | Только kind asset | Новый тип, §4 |
| RightsReview | Есть, отсутствует expiry | Старый RightsReview + RightsDetails companion |
| ApprovalRecord | Есть все перечисленные поля | Без изменения; решения — данные, workflow не выполняется codec |
| Event | Нет | Новый Event, §4; не ревизия и не ObjectKind |
| active_refs | tuple[RevisionRef,...] без ролей | Фиксированное positional соответствие ActiveSelections, §6 |
| EditorialSnapshot | Минимальный base envelope | ContractSnapshot(base,source_details,claim_reviews,rights_details,events,snapshot_checksum) |
| Brief | В E00 frozen embedded value | BriefValue внутри ScriptRevision, не отдельная root collection |
| Stage/готовность | Не реализованы | Будущий service; wire не хранит авторитетный approved/stage |
| File locks/save/backup | Не модель | Будущий E02; codec не вызывает filesystem/network |
| Hand-off/render manifest | Не envelope core | Будущий E06/E08; v3 не меняется |

Companion metadata — frozen values с exact owner_ref, не side-effect registry. Для каждой Source/Claim/Rights revision в полном aggregate ровно один соответствующий companion. Их поля сериализуются в тот же wire-объект, а не дополнительные root dictionaries. Metadata ссылается на owner только для join, не создаёт dependency edge обратно к себе. При будущей унификации классов будет нужна отдельная миграционная задача; текущие объекты не изменяются.

## 4. Новые payloads: исчерпывающие поля

Все поля таблиц обязательны как ключи JSON. Nullable означает обязательный ключ с null. Никаких произвольных extras. ref.kind обязан соответствовать имени collection; проверка формы не означает существование targets.

### GenreProfile (ref.kind=genre_profile)

| Поле | Тип / ограничение |
|---|---|
| profile_key | Text; ASCII lower snake_case [a-z][a-z0-9_]{0,63} |
| version | Text, сохраняется отдельно от PositiveInt ref.revision |
| display_name_ru, display_name_uk | Text |
| allowed_modes | List(ContentMode), непустой, без повторов |
| narrative_structure | List(Text), непустой; порядок значим |
| review_policy_version | Text |
| rubric | Nullable(List(RubricCriterion)) |

RubricCriterion строго {key,description,rating_min,rating_max,weight_percent}: key как profile_key, description Text, min=0/max=5 (int, не bool), weight_percent integer0..100. Если rubric не null — непустая, keys уникальны, веса в сумме100. Это конфигурация редакционной оценки, не обученная вероятность. При rubric=null не создаются скрытые defaults.

### CandidateRevision (ref.kind=candidate)

title:Text; summary:Text; source_refs:List(Ref(kind=source)); discovery_method: manual_topic|manual_url|manual_local; discovery_input:Text; assessment:Nullable(List(CriterionRating)); rationale:Nullable(Text).

CriterionRating строго {criterion_key,rating,reason}: key как profile_key, rating integer0..5, reason Text; ключи уникальны. Отсутствие assessment не означает score0. Соответствие rubric выбранного profile проверяется E01.3/service, не угадывается codec. Candidate не дублирует genre/mode Production. manual_url регистрирует строку, сеть не запрашивает.

### BriefValue — embedded в ScriptRevision

Строго {revision,audience,angle,promise,must_include_claim_refs,must_avoid,profile_ref}. revision:PositiveInt; audience/angle/promise:Text; must_include_claim_refs:List(Ref(kind=claim)); must_avoid:List(Text); profile_ref:Ref(kind=genre_profile). Brief не имеет отдельного UUID/root ref: versioned value принадлежит конкретной immutable ScriptRevision; изменение brief требует новой ScriptRevision.

### ScriptSegment

Строго {id,text,role,claim_refs,visual_notes,pronunciation_notes,disclosure_marker}. id:UUID; text:Text; role из §2; claim_refs:List(Ref(kind=claim)); три последних поля Nullable(Text). Segment ID уникален внутри ScriptRevision, сохраняется при редактировании того же фрагмента; не глобальная revision. Поле disclosure не создаёт автоматическую проверку фактов.

### ScriptRevision (ref.kind=script)

Строго ref, production_ref:Ref(production), candidate_ref:Ref(candidate), brief:BriefValue, locale:Locale, segments:List(ScriptSegment), claim_refs:List(Ref(claim)). segments от1 до1000. claim_refs — уникальный список в лексикографическом порядке(kind,id,revision,content_hash), равный объединению segment.claim_refs. Согласованность с источниками и конкретными формулировками — E01.3 и human review, не codec.

Narratable text — точная конкатенация segment.text без добавления пробелов. Не делать отдельного поля text или content_hash помимо ref: вычисляемый текст и hash не должны расходиться с первичными полями.

### Scene

Строго {id,start,end,narration_text,visual_kind,visual_brief,asset_ref,estimate_ms}. id:UUID; start/end:NonnegativeInt, end>start; offsets в script narratable text, Unicode code points, end exclusive. narration_text:Text; visual_kind=still; visual_brief:Text; asset_ref:Nullable(Ref(asset)); estimate_ms:Nullable(PositiveInt). Это MVP scene: AI/video brief не маскируется как still, расширение visual_kind — отдельное решение.

### ScenePlanRevision (ref.kind=scene_plan)

Строго ref, script_ref:Ref(script), scenes:List(Scene), от1 до1000. Порядок scenes — narration order, отдельное order поле не нужно. ID уникальны внутри plan, start первой=0, соседние end/start совпадают. E01.3 разрешает script_ref; E01.5 сверяет final end с длиной referenced script и exact slices. Лимит20 сцен/2000 символов — позже capability/handoff; editorial draft не обрезается codec.

### AssetRevision (ref.kind=asset)

Строго ref, file_ref:Text, sha256:Hash (hash media bytes, не ref.content_hash), kind:image|audio|video, rights_ref:Ref(rights_review), scene_id:Nullable(UUID), script_ref:Nullable(Ref(script)), text_digest:Nullable(Hash). Последние два либо оба null, либо оба заданы; scene_id может быть null для переиспользуемого asset.

file_ref — POSIX relative syntax внутри managed production: без drive, backslash, absolute/UNC, пустых компонентов, . или ..; каждый компонент не Windows reserved name, не заканчивается точкой/пробелом, длина<=100 code points, весь путь<=240. Codec проверяет только строковую форму; actual containment/junction/symlink/media existence/bytes/hash — будущий I/O preflight. kind=video допустим как учётный asset, но не как поддерживаемый still handoff.

### Event — append-only запись данных

Строго {id,actor,at,action,refs,reason,error_code}. id:UUID; actor:Text; at:UTC; action — closed list production_created|revision_added|active_selection_changed|review_recorded|approval_recorded|recovery_recorded|operation_failed; refs:List(Ref); reason:Text; error_code:Nullable(Text). Event не вызывает описанное действие и не является источником workflow authority. Порядок массива events — порядок истории, не сортируется по времени. Обновление vocabulary — schema version change, неизвестное action не игнорируется.

## 5. Существующие объекты и недостающие metadata

### ProductionRevision — wire без перепроектирования

Строго ref,title,profile_ref,content_mode,script_locale,narration_locale,subtitle_locale,ui_locale,intended_use,output_preset,created_at. Типы соответствуют существующим полям; intended_use и output_preset ограничены §2, created_at UTC. Нет скрытых defaults при decode. При создании production defaults9:16 и ru/uk задаёт будущий service; codec не придумывает locale и не исправляет mismatch. Он представляет draft с mismatch, а handoff позже блокирует его.

### SourceRevision + SourceDetails

Wire строго {ref,title,locator,rights_ref,source_type,author,publisher,published_at,accessed_at,access_notes,reliability_notes,material_digest}. Первые четыре соответствуют E01.1. Companion SourceDetails(owner_ref,source_type,author,publisher,published_at,accessed_at,access_notes,reliability_notes,material_digest).

source_type=url|local; author/publisher/access_notes/reliability_notes Nullable(Text); published_at/accessed_at Nullable(UTC); material_digest Nullable(Hash). locator:Text; url означает абсолютный https/http URL без userinfo/control chars, hostname обязателен; fragment разрешён. local locator — managed relative path по правилам Asset.file_ref с необязательным локатором страницы в access_notes. Codec ничего не получает по URL и не канонизирует его молча. Локальная дата без времени не превращается в UTC midnight: остаётся null, буквальное описание даты можно сохранить в access_notes.

### ClaimRevision + ClaimReview

Wire строго {ref,statement,claim_type,materiality,evidence_links,review_status,qualification,reviewer,reviewed_at,reason}. Первые пять соответствуют E01.1. Companion ClaimReview(owner_ref,review_status,qualification,reviewer,reviewed_at,reason).

materiality из §2; qualification/reviewer/reason Nullable(Text); reviewed_at Nullable(UTC). При unreviewed все review metadata null. При остальных status reviewer/reviewed_at/reason обязательны non-null; qualification non-null только для qualified, иначе null. Это локальная согласованность записи review, не доказательство верности утверждения. Fictional claim может оставаться unreviewed с пустыми evidence; отсутствие review не должно порождать fake sources.

EvidenceLink строго {source_ref,relation,locator,explanation,reviewer,reviewed_at}; типы существующего класса, reviewed_at UTC. Пустой evidence_links допустим для draft; codec не присваивает supported по URL.

### RightsReview + RightsDetails

Wire строго {ref,subject_id,subject_revision,material_digest,intended_use,allowed_actions,status,reviewer,reviewed_at,basis,expires_at}. Первые одиннадцать — E01.1; RightsDetails(owner_ref,expires_at:Nullable(UTC)). allowed_actions List(quote|import|render|distribute), без повторов; может быть пустым при unknown/blocked. reviewed_at обязателен UTC, reviewer/basis Text даже для записи «не проверено». Expiry раньше reviewed_at не допускается; срок проверяется относительно явного evaluation time поздним service, не системными часами codec.

subject_id/revision — locator к Source/Asset, не полная Ref; material_digest не включает RightsReview. E01.3 сверяет Source.material_digest либо Asset.sha256 с subject digest при наличии материала. null source material digest означает unresolved material binding, не автоматически approved rights.

### ApprovalRecord

Wire строго {id,gate,object_ref,dependency_digest,policy_version,actor,timestamp,decision,reason,review_declarations}. Типы E01.1; gate из §2, timestamp UTC, review_declarations:List(Text), порядок сохраняется. Existing string gate не превращается в произвольное действие. Codec не выдаёт authority на основании decision=approve. Связь gate→kind (SCRIPT/script, SCENES/scene_plan, HANDOFF/scene_plan) и digest входят в E01.3/service; handoff config/assets ещё проверяются отдельным manifest будущего adapter.

### Violation / ModelError

Не сохраняются как корневые state collections. Диагностический API codec может возвращать существующий Violation; invalid JSON/type/field отмечается точным field_path. Не сериализовать Python exception или stack trace в editorial state. Event.error_code лишь сохраняет результат, без исполнения retry.

## 6. Полный JSON envelope и active_refs

Корневой объект имеет **ровно** следующие ключи; все обязательны:

| Ключ | Wire тип | Источник внутри полного aggregate |
|---|---|---|
| editorial_schema_version | integer1 | base.editorial_schema_version |
| production_id | UUID | base.production_id |
| generation | PositiveInt | base.generation |
| production_revisions | List(ProductionRevision) | base.revisions kind=production |
| profiles | List(GenreProfile) | kind=genre_profile |
| candidates | List(CandidateRevision) | kind=candidate |
| sources | List(full SourceRevision) | kind=source + SourceDetails join |
| claims | List(full ClaimRevision) | kind=claim + ClaimReview join |
| scripts | List(ScriptRevision) | kind=script |
| scene_plans | List(ScenePlanRevision) | kind=scene_plan |
| assets | List(AssetRevision) | kind=asset |
| rights_reviews | List(full RightsReview) | kind=rights_review + RightsDetails join; Q1 |
| approvals | List(ApprovalRecord) | base.approvals |
| events | List(Event) | aggregate.events |
| active_refs | ActiveSelections object | mapping ниже |
| snapshot_checksum | Hash | aggregate.snapshot_checksum; Q2 |

Empty draft arrays допустимы; отсутствие root key или null вместо array недопустимы. Даже пустой draft требует explicit checksum-shaped значение; пока E01.3 отсутствует, такой snapshot считается только syntactically decoded, а не checksum-verified. Codec не создаёт нулевой hash по умолчанию. Авторитетная запись на диск до E02 не обещается.

ActiveSelections имеет ровно {production,candidate,script,scene_plan}; каждый value Nullable(Ref соответствующего kind). profile выбирается через active production.profile_ref; права и источники не выбираются по latest. Нет отдельного active brief, он вложен в active script.

Внутренняя base.active_refs — tuple только non-null slots в фиксированном порядке production,candidate,script,scene_plan. Не более одной Ref каждого slot kind; пропущенный kind означает именно null. Decode реконструирует этот tuple; encode по kind восстанавливает четыре ключа с null. Дубликат/неподдерживаемый kind или неправильный tuple order — ошибка, не автоматическая сортировка. Пустой tuple ↔ все четыре null. Наличие выбранного script без production допустимо как structurally representable draft, но E01.3 выдаёт несогласованную selection; codec не придумывает production.

Revisions во внутреннем base.revisions имеют фиксированный порядок групп из таблицы, внутри — id лексикографически, затем revision по возрастанию. Wire arrays имеют тот же порядок и не допускают duplicate(kind,id,revision). Таким образом group/join обратимы; произвольное interleaving старого E01.1 tuple не теряется молча: encode возвращает NONCANONICAL_REVISION_ORDER. Пользователь может явно собрать корректный full aggregate в будущей model-building задаче. Approvals/events, narrative/scene order не сортируются.

## 7. Null, omission, даты и сохранение информации

- Каждый ключ, перечисленный в контракте, присутствует всегда. «Необязательное поле» означает Nullable или empty list, а не разрешённое отсутствие ключа. Неизвестные поля отклоняются; forward compatibility требует явной версии, не extras bag.
- null означает неизвестно/не применяется в указанном поле. Для annotations и review сохраняется смысл через status/type. Пустой Text запрещён; String используется только там, где отдельно разрешён (ни одно требуемое narration поле не допускает пустоту).
- Empty list — известных элементов пока нет. Отсутствие nullable scalar не заменяется false/0/пустой строкой. Boolean не является int; float, NaN, Infinity запрещены во всём контракте.
- Dates только UTC seconds с Z, никакого auto local timezone, now(), date-only conversion или millisecond truncation. Unknown→null лишь при явном null на входе, не при malformed date.
- Decode enum string вызывает соответствующий существующий enum; case-sensitive. Encode enum выдаёт .value; Python repr/name не wire value. Checked strings остаются str для совместимости E01.1. Input bytes — UTF-8 без BOM; malformed UTF-8/BOM отклоняются, строки и code points не исправляются.
- Hash/UUID сохраняют exact допустимую canonical форму; timestamp/text/array order не нормализуются. JSON whitespace/key order не является domain information; raw JSON bytes не обещаются идентичными после encode.
- Допустимые full aggregates удовлетворяют encode/decode round-trip по всем полям values/metadata/order. Сохранение source/claim/rights companions проверяется явно; codec не отбрасывает неизвестное, чтобы «успешно» загрузить объект.

## 8. Ответственность уровней проверки

| Уровень | Обязательные проверки | Что не делает |
|---|---|---|
| Конструкторы value types | Enum instances, exact базовые типы, UUID/hash shape, positive integers без bool, immutable tuples, nonempty обязательные строки; локальные ranges/types новых nested values | Не ищут targets, не читают files, не вычисляют truth/approvals |
| E01.2 codec | UTF-8/JSON grammar, duplicate keys, exact field sets и nullability, schema version, recursion/size caps, strict dates/checked strings, enum conversion, nested payload dispatch по collection, correct Ref kinds, companion join, canonical grouping order | Не computes/verifies content_hash/checksum/digest, не fetch, не execute, не saves, не runs semantic gates |
| E01.3 integrity | Уникальные identities между kinds, exact refs существуют в этой production, hash совпадает payload, checksum/digest, graph cycles/conflicting refs, companion owner one-to-one, source rights binding, segment/claim consistency, active revision chain, profile rubric keys | Не утверждает факты, не переводит текст, не выдаёт коммерческий grant |
| E01.5 и service позднее | Полное text partition против referenced script, exact narration, capability1–20/2000, languages/preset, human material coverage, approval/revocation/rights readiness | Не подменяет проверки codec формальной «истиной» |
| E02 / production adapter | Atomic save/lock/recovery, file hashes/containment, asset bytes, TTS/render attempts | Не часть model/codec |

Локальные same-object checks (unique segment IDs, allowed_modes/rubric sums, paired nullable fields, end>start) принадлежат модели новых values; codec дополнительно гарантирует, что эти конструкторы вызваны. E01.3 может проверить связь Scene со Script, но acceptance E01.5 остаётся отдельной задачей: такой контроль не является разрешением реализовать её в codec.

Существующие конструкторы E01.1 слабее wire-контракта: например created_at='time' и произвольный intended_use пока представимы. Это не причина менять их здесь. Encode полного schema1 должен отказать с конкретным field_path, а не исправить дату/строку. Raw-string enum в существующий конструктор не передаётся: явное преобразование — задача codec.

## 9. Пошаговое отображение без потери данных

Decode: parse strict envelope → проверить shape/ключи/caps → для каждой коллекции выбрать конкретный полный тип → Source/Claim/Rights разделить на existing value и typed companion → собрать base.revisions в фиксированном порядке → собрать active tuple → ContractSnapshot с events/checksum. Никакого fallback в EditorialRevision(ref) при неизвестном payload.

Encode: проверить допустимый full aggregate → exact one-to-one companion join по owner_ref → dispatch concrete type с совпадающим kind → разложить в отдельные arrays → active slots с explicit null → сохранить approvals/events/order, generation/checksum как supplied values → JSON bytes по отдельному codec API. Ref-only base object, missing companion и неполные старые Source metadata дают INCOMPLETE_MODEL, не guessed values.

Пример безопасного разделения Source: wire author/publisher/dates/notes/material_digest остаются в SourceDetails, а title/locator/rights_ref — в исходном SourceRevision. После обратного join все значения восстановлены. Для Claim аналогично сохраняются review_status/qualification/actor/time/reason. Для Rights expires_at не теряется. Ни один companion не предоставляет approval сам по себе. owner_ref companion — только внутренний ключ join и не отдельное поле wire/hash payload; его включение создало бы самоссылку. E01.3 хэширует полный joined payload по правилам E00 с исключением content_hash и audit timestamps.

## 10. Готовность к следующей задаче и вопросы владельцу

Контракт перечисляет все E00 entities, wire fields/nullable/enums/refs и ответственность уровней. Отсутствующих реализованных типов нельзя компенсировать проектированием внутри codec.

Перед реализацией нужны два явных решения:

1. Принять Q1–Q5 как уточнение E00: rights_reviews, snapshot_checksum, typed full aggregate/companions, profile identity и uniqueness для rights subject. E00 в этой ветке не изменяется.
2. Разрешить отдельную небольшую задачу добавления описанных value types/companions/active mapping либо ограничить E01.2 уже существующим subset и назвать его неполным codec. Рекомендуется сначала добавить полную модель, затем E01.2 без самостоятельного изменения схемы.

E01.1, CLI, renderer и timeline v3 остаются неизменными. Новый JSON, код, тесты, профили, миграции и storage не созданы. Сохранение документа не является разрешением на E01.2. После отчёта остановиться и ждать review.
