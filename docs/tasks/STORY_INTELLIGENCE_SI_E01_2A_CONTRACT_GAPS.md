# SI-E01.2a — Contract gaps

Дата: 2026-11-09. **Статус: BLOCKED_CONTRACT.**
База: `b74d805996e1e9eba65e323f6d1c2995fbb1234f`.
Это фиксация узкого пробела для решения владельцем, не изменение утверждённой
архитектуры, не реализация и не отмена приёмки SI-E01.1.

## SI-E01.2a-G01 — не закрыт wire namespace полей ReviewPacket

### Нормативные основания STOP

[Задание SI-E01.2a](STORY_INTELLIGENCE_SI_E01_2A_CODEX_TASK.md), строка 20:

> Where a required field/type remains genuinely ambiguous, STOP and report a bounded contract issue instead of silently inventing a field/default.

То же задание, строка 35, требует `exact field namespace` в полной локальной
проверке всех 18 типов, включая FieldGrant/FieldView/Omission и ReviewPacket;
строка 49 требует `BLOCKED_CONTRACT` вместо неподтверждённой partial acceptance.

[Утверждённый R1](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md) задаёт:

| Место | Что определено | Чего недостаточно для exact local validator |
|---|---|---|
| §5.1, строки 414–417 | FieldGrant.field_path, FieldView.field_path, Omission.field_path имеют тип Text; DisplayItem имеет source_ref:SIRef | Нет точной грамматики пути и корня, допустимых alias spellings и записи индексов |
| §5.2, строки 453–460 | Semantic TEXT whitelist: StoryIdea(title,summary,viewer_question), CreativeAlternative(title_options[i],chapters[i].heading/chapters[i].purpose) и другие поля; индекс должен существовать | Не задано, является ли строка путём от payload, от полного {H,payload}, именем типа+поля или иной нотацией; не задана база индекса |
| §5.2, строки 461–464 | STATE включает EvaluationEligibility.state и projection review_state/currentness | EvaluationEligibility вложена в EvaluationReport; BriefReviewState вообще не recorded type. Не задан exact source_ref/path namespace для projection fields |
| §4.3, строка 334 | BriefReviewState — read-only value без H/id/SIRef/persistence | Нельзя вывести его собственный SIRef из имеющейся схемы DisplayItem |
| §5.2/§5.3, строки 470–475/489–493 | Grant связан с exact source field value/manifest; Packet имеет детерминированные canonical bytes, поля — schema order/ascending index | Локально разные написания/адресация меняют grant matching и record bytes, даже при одинаковом semantic field |

Поиск всех `field_path`, `FieldGrant`, `FieldView` и `Omission` в исходном proposal,
R1 и R1a не выявил другого определения wire grammar. R1a меняет operation/type
rules и creative provenance; этих clauses о путях он не уточняет. Owner approval
принимает composite без дополнительного определения path grammar.
Product Success Criteria @ `ed1630140a6b9a7089ef04e1c926019c3cb74ed6` прочитан
read-only с отдельной ветки; он не задаёт новую wire-схему и не объединялся с базой.

### Минимальный воспроизводимый пример A — одно поле, разные bytes

Синтетический unresolved SIRef (проверена только форма, не наличие StoryIdea):

```json
{"type":"StoryIdea","id":"11111111-1111-4111-8111-111111111111","revision":1,"sha256":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
```

Пусть semantic field — StoryIdea.title со значением `Історія`.
SHA256(C(value)) =
`ad93c7dce3d3d7b640cbcc7b06f2c2886600f8fb331d82036f4282ce6a19887d`.
При одних source_ref/value_sha256 две возможные строки FieldGrant.field_path:

| Вариант (не утверждён) | SHA256(C(FieldGrant)) |
|---|---|
| `title` — путь от payload | `c9364f8897ff57cb49a45be1d52a0feb50ecf4ecff44d7a14be4976dc12f578f` |
| `payload.title` — путь от полного record | `7ac0275dbd3858a870b745fd94fbf2520846ef43ea51e941509edd251bbefb3a` |

Оба варианта — Text и обозначают один whitelist field при соответствующей
интерпретации корня. Ни один не объявлен утверждённым wire representation.
Bytes независимо построены stdlib JSON (sorted keys, UTF-8, no spaces), SHA —
hashlib; совпадение bytes с принятым SI-E01.1 codec проверено. Это **не** valid
полный typed-record vector и не доказательство source hash/provenance.

Ожидание SI-E01.2a: однозначно принять разрешённый spelling и отвергнуть alias,
не выполняя автоматическую нормализацию. Фактическое состояние контракта:
выбрать между этими результатами либо разрешить оба можно только добавлением
ещё не утверждённого правила. Простая проверка Text не выполняет требование
`exact field namespace`; перенос всей этой проверки в SI-E01.2b также не
соответствует текущему заданию SI-E01.2a.

Для массива аналогичный вопрос: `title_options[0]` или `title_options[1]` для
первого элемента? PosInt chapter_index у VisualRequirement не определяет grammar
field_path. Нельзя переносить правило из другого поля без явного основания.
Проверка существования индекса в другом record сама по себе остаётся для resolver,
но его wire syntax и база нужны локальной schema уже сейчас.

### Минимальный пример B — STATE projection без собственного SIRef

Для `FieldView(kind=STATE, text="READY_FOR_BRIEF_REVIEW")` из BriefReviewState
нужно определить source_ref у содержащего DisplayItem и точный field_path.
Использовать Brief ref и виртуальный путь? Иной snapshot ref? Показывать projection
только в имеющемся review_state_at_capture и исключить её из display_items?
Контракт не выбирает этот mapping. Это варианты вопроса, **не принятые решения**.

Нельзя создать новый RecordType/SIRef для BriefReviewState: R1 явно запрещает ему
record identity. Нельзя автоматически использовать текущий Packet как свой
source_closure_ref: R1 §5.1 исключает Packet и export Run из собственной source
closure. Нельзя молча удалить разрешённые STATE поля из профиля или разрешить
arbitrary virtual paths. Выбор любого из этих путей изменил бы утверждённый scope.

### Минимальное уточнение, необходимое от владельца

Нужна отдельная одобренная узкая спецификация (без изменения кода SI-E01.1):

1. Один точный field_path namespace для FieldGrant/FieldView/Omission: корень,
   separators, array index base/canonical spelling, допустимость H fields при
   REDACTED/Omission, запрет aliases/wildcards/неизвестных полей. Полный mapping
   semantic whitelist к wire paths, включая EvaluationReport.eligibility.state.
2. Точный source_ref/path mapping для projection STATE либо явное правило, что
   projection отображается только через существующий review_state_at_capture.
   Если нужен иной тип/профиль — это отдельное изменение, а не default реализации.
3. Небольшие literal positive/negative examples для каждого затронутого вида пути,
   grant matching и STATE mapping; затем возобновление SI-E01.2a на новой exact базе.

Остальные типы не объявлены дефектными. Никаких общих пересмотров SI-D01–SI-D10,
новых permissions, persistence, providers или редакционных схем не предлагается.
До уточнения нельзя добросовестно заявить полную strict validation всех 18 типов
или 12 корректных typed-record golden vectors, обязательно включающих ReviewPacket.
Production-код и новые executable tests не создавались. SI-F01 остаётся
nonblocking: worst-case 1 MB integer latency не измерялась и новый digit cap не введён.
