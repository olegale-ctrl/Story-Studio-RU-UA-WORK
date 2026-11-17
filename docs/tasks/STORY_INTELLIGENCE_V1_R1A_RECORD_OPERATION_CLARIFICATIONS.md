# Story Intelligence V1 R1a — Record Operation Clarifications (SI-R04)

**Дата:** 2026-11-09. **Статус: PROPOSAL / AWAITING OWNER APPROVAL.**
Только узкое additive erratum R04-A/B; не реализация и не утверждение SI V1.

## 1. Основание и приоритет

Точная база: `5f31b4aedc4916573300d204b5f3f52e1369ef80`, ветка-источник
`docs/story-intelligence-v1-r1-independent-acceptance`; remote HEAD проверен и совпадает.
Основания:

- [Исходный proposal](STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md), редакция
  `b7bea3aec1fd533973c1e82ad0bd06cf9dd37412`, §3/§8.
- [R1](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md), редакция
  `978fbed45513a00e851201a9018d17c7da4752be`, §1–2/§6–8.
- [Независимое ревью R1](STORY_INTELLIGENCE_V1_R1_INDEPENDENT_REVIEW.md) и
  [полное задание R1a](STORY_INTELLIGENCE_V1_R1A_CODEX_TASK.md) на точной базе.
- [Согласованная концепция](../architecture/STORY_INTELLIGENCE_ARCHITECTURE_DECISION_2026-11-05.md),
  [ревизия завершённых этапов](STORY_INTELLIGENCE_COMPLETED_STAGES_REVIEW.md),
  [существующая editorial модель](../../editorial/model.py) — read-only границы.

R04-A: общий RecordSet R1 исключал StoryIdea из редактирования после Discovery.
R04-B: ручное создание CreativeAlternative требовало обязательный creative run,
хотя RECORD_INPUT не создаёт RunRecord. Подстановка чужого run или ложного
MANUAL_INPUT не является допустимым решением.

В составном **предложении** этот erratum заменяет только общий RecordSet и две
operation rows R1 §2, уточняет их применение к StoryIdea/CreativeAlternative,
обязательный CreativeAlternative.run_ref и затронутые acceptance cases.
Остальные правила original+R1 сохраняются, включая разрешение SI-R01–03.
Применение в реализации требует независимой проверки и явного owner approval;
сам документ не меняет статус утверждённых контрактов или исходных документов.

## 2. Полные закрытые множества и replacement rows

`CreateableRecordSet` (ровно 12 типов):

```text
Intake, SourceItem, ClaimItem, EvidenceItem, ClaimCheck,
AudienceHypothesis, ChannelContext, Angle, Rubric, VisualRequirement,
Risk, ProductionBrief
```

`RevisableRecordSet` (ровно 14 типов):

```text
Intake, SourceItem, ClaimItem, EvidenceItem, ClaimCheck,
AudienceHypothesis, ChannelContext, Angle, Rubric, VisualRequirement,
Risk, ProductionBrief, StoryIdea, CreativeAlternative
```

Это operation allowlists, не новый RecordType vocabulary. StoryIdea не создаётся
через RECORD_INPUT (включая USER_IMPORT); первая версия — только DISCOVER_LOCAL.
CreativeAlternative не создаётся через RECORD_INPUT (включая USER_IMPORT);
первая версия минимального V1 — только PROPOSE_CREATIVE с template run.
RunRecord, EvaluationReport, Selection, ReviewPacket исключены из обоих множеств:
они по-прежнему создаются своими специальными операциями. Unknown type не проходит
по generic fallback. Поля H/payload и SIRef/ERef остаются закрытыми и обязательными.

Следующие строки целиком заменяют соответствующие строки R1 §2; новые operations,
options, H fields, modes, stages или error codes не добавляются. Method identifiers
и версии R1 сохранены: это уточнение ещё не утверждённого интерфейса, не runtime upgrade.

| Operation / method_id,version | Закрытые options | Outputs / происхождение | Roots / обязательная проверка |
|---|---|---|---|
| RECORD_INPUT / si.record-input,1-r1 | record_type:CreateableRecordSet; working_copy:соответствующий typed payload; input_origin:MANUAL_INPUT либо USER_IMPORT с imported_from по R1 | Один record с новым id, revision=1, previous=null; фактический manual/import origin; Run отсутствует; output_refs=[record_ref] | Все existing payload/provenance refs, schema order; exact resolve/type/hash/limits; нельзя переименовать derived content в ручное |
| REVISE_INPUT / si.human-revision,1-r1 | base_ref:SIRef типа RevisableRecordSet; replacement_payload:полный typed payload того же type | RunRecord stage=REVISION плюс тот же type/id, revision=base.revision+1, previous=base_ref; origin HUMAN_EDIT; output_refs=[revision_run_ref,new_record_ref] | base_ref первым, затем direct replacement payload refs в schema order; полная previous/provenance closure; stage/method/mode/ref validation до принятия |

DISCOVER_LOCAL / `si.discover-local,1-r1` по-прежнему создаёт DISCOVERY run и
StoryIdea revision1 с RULE_DERIVED origin. PROPOSE_CREATIVE /
`si.creative-templates,1-r1` создаёт CREATIVE run и CreativeAlternative revision1
с TEMPLATE_DERIVED origin. Их options, input roots и output ordering R1 неизменны.
REVISION run имеет `method_id=si.human-revision`, `method_version=1-r1`,
`provider=null`; он фиксирует ручную правку, а не новую генерацию template/model.

## 3. StoryIdea: редактирование без разрыва identity

После DISCOVER_LOCAL пользователь может изменить title/summary/viewer_question
или другие разрешённые поля полного StoryIdea payload через REVISE_INPUT.
Нельзя передать новый id/type/revision/previous/origin в replacement_payload:
служебный H строится операцией, а лишние поля отклоняются.

`base_ref` разрешается по полным type/id/revision/sha256; предыдущая версия того же
объекта должна быть доступна и неизменна. Новая revision не перезаписывает старую,
не пропускает номера и не создаёт ветку от старой revision поверх уже принятой
следующей версии. Для нового запроса применяется R1 expected_context_hash; stale
context отклоняется как STALE с пустыми outputs. Попытка принять другую версию
при уже занятой паре (type,id,revision) — INVALID/REF_HASH_MISMATCH, не overwrite.
Исторический exact retry обрабатывается по §5, без движения текущих refs назад.

Новый origin: `{mode:HUMAN_EDIT,run_ref:точный_REVISION_run,imported_from:null}`.
Его Run.semantic_input_refs включает base_ref и refs нового payload; input_snapshot
содержит полную R1 Closure roots+ContextSnapshot. В previous chain остаются исходная
StoryIdea, её DISCOVERY run, исходный Intake и source/import ancestry. Изменение
source_refs не удаляет старые source refs из истории: новые exact refs относятся
к новой версии, прежние доступны через base_ref/closure. UNKNOWN не заменяется
пустым списком или выдуманным evidence. candidate_binding остаётся nullable exact
ERef kind=candidate; операция не создаёт и не правит editorial CandidateRevision.

Смена выбранной Idea revision делает зависимые от прежней Idea Eval/Creative/Brief
устаревшими по R1; они не получают implicit resolve-latest. Текстовая правка не
переносит Selection/approval на новую revision. Новые evaluation/selection при
необходимости выполняются явно. Ручная правка не является fact check или rights grant.

## 4. CreativeAlternative: два разных run refs

`CreativeAlternative.payload.run_ref` остаётся обязательным non-null SIRef типа
RunRecord. Это **исходный создающий CREATIVE run данной identity**, а не run,
породивший bytes каждой последующей ручной версии. `H.origin.run_ref` обозначает
run, непосредственно создавший данную revision. Значения не взаимозаменяемы.

| Версия | H.previous | H.origin.mode / H.origin.run_ref | payload.run_ref |
|---|---|---|---|
| K1: первоначальный template output | null | TEMPLATE_DERIVED / C (CREATIVE) | C |
| K2: ручная правка K1 | exact K1 | HUMAN_EDIT / R2 (REVISION) | exact C, без изменения |
| K3: ручная правка K2 | exact K2 | HUMAN_EDIT / R3 (REVISION) | exact C, без изменения |

Здесь C/K1/R2/K2/R3/K3 — только illustrative aliases, не допустимые wire SIRefs.
В будущих fixtures нужны настоящие UUID, revision и буквальные hashes/bytes.

Для K1 оба refs совпадают и C проходит `si.creative-templates,1-r1` / CREATIVE
проверку; provider=null. Для каждой правки валидатор проходит предыдущую цепочку
до K1, проверяет type/id/последовательность revisions/exact hashes, доступность C,
его method/stage и initial origin. В каждой revision payload.run_ref должен быть
**тем же exact C**, а HUMAN_EDIT origin должен ссылаться на соответствующий
REVISION run. Корректный сам по себе CREATIVE run другой alternative не подходит.
Нельзя заменить C на R2/R3, новый CREATIVE run или null; нельзя обозначить K2/K3
как MANUAL_INPUT, USER_IMPORT или как свежий TEMPLATE_DERIVED output.

Полный replacement_payload обязан явно повторить C; скрытая подстановка или
исправление не допускаются. H.input_refs новой версии начинается с base_ref, затем
идут direct payload refs, включая C; Revision run фиксирует эти roots и request
payload digest. Старая ancestry сохранена через base_ref, а новые angle/claim refs
проходят exact checks. Если angle_ref меняется, прежний угол остаётся в K1 ancestry;
C описывает исходное происхождение, а не доказательство генерации исправленного
угла/текста. SemanticClosure/currentness R1 не превращает history-only зависимости
в текущие inputs. Run не содержит output refs; цикл C→K2→R2 не вводится.

Менять hook/title/chapters разрешено только при сохранении claim qualifications и
остальных factual/rights ограничений. Новый факт требует нового claim/review,
не косметической правки текста. Старый Selection K1 не становится Selection K2;
выбор новой exact alternative и дальнейший Brief требуют явного review по R1.
Изменение только Creative не переписывает Evaluation и не добавляет ему зависимость
от будущего human choice. Зависимые Brief/Packet проверяются по правилам R1.

Standalone hand-authored CreativeAlternative и manual/import StoryIdea creation
**отложены**, недоступны через описанные операции. Если нужны продукту, потребуются
отдельный truthful provenance design и явное owner approval. Фиктивный CREATIVE run,
ослабление обязательного run_ref и заимствование чужого run запрещены.

## 5. Отказы и идемпотентность

Проверки R1 §6 сохраняются. Недопустимый тип для операции → INVALID/TYPE с path
`options.record_type` или `options.base_ref.type`. Unknown/missing fields →
UNKNOWN_FIELD/MISSING_FIELD; неверный вид ref → REF_TYPE_MISMATCH; отсутствие/hash →
REF_MISSING/REF_HASH_MISMATCH; method/stage/mode либо подмена исходного C →
PROVENANCE_MISMATCH; циклы → DEPENDENCY_CYCLE. Paths относятся к фактическому
ошибочному полю, например `options.replacement_payload.run_ref`. Нет accepted
Run/record/partial outputs при INVALID или STALE. Closure/size limits не обходятся
удалением previous. Нет автокоррекции полей или импортируемой provenance.

Exact retry принятого request_id с теми же canonical Request bytes возвращает
ровно сохранённые `[revision_run_ref,new_record_ref]`, даже если текущий context
уже изменился; это historical result, не новое принятие/актуальность/движение head.
Тот же id с другим base_ref/replacement/input revision/expected_context_hash →
REQUEST_CONFLICT, пустые outputs. Новый request_id с другим допустимым exact input
revision проверяется заново против текущего context; новый REVISION run и новая
record revision явно ссылаются на этот input. Старые refs не «обновляются» на месте.
Повреждённый mapping/output → RECORD_UNAVAILABLE/INVALID по R1, без реконструкции
или выдачи новой revision под видом exact retry.

## 6. Будущие acceptance cases R04 (не выполненные тесты)

Во всех случаях проверяются exact bytes/refs, исходные immutable records, отсутствие
editorial/protected writes и переносов grants. Число cases: **10**.

| ID | Вход/действие | Независимое ожидаемое поведение |
|---|---|---|
| R04-T01 | DISCOVER I1, затем REVISE viewer_question | Один новый REVISION run, I2 того же id/revision2; previous exact I1, HUMAN_EDIT; исходные DISCOVERY/Intake/source refs доступны через closure |
| R04-T02 | RECORD_INPUT StoryIdea / CreativeAlternative, отдельно MANUAL_INPUT и USER_IMPORT | Все четыре комбинации INVALID/TYPE; outputs пусты; нет fake run/record |
| R04-T03 | PROPOSE K1 от C, затем ручная K2 и K3 | Таблица §4 совпадает буквально; payload.run_ref=C во всех версиях; origin refs C/R2/R3; предыдущие bytes и hashes неизменны |
| R04-T04 | K2 подменяет C на null, REVISION run или чужой valid CREATIVE run; либо origin manual | null отклоняется TYPE, wrong stage/чужое происхождение — PROVENANCE_MISMATCH; нет принятой K2 |
| R04-T05 | Exact retry принятой правки после принятия следующей revision | Те же сохранённые refs и bytes; ни нового Run/revision, ни возврата current input/head назад |
| R04-T06 | Тот же request_id, но другой exact source/angle input revision | REQUEST_CONFLICT; при новом id/валидном текущем context допустима новая revision с явно новым input, старый source/angle остаётся в previous ancestry |
| R04-T07 | Неверный previous hash/type, missing I1/K1/C, цикл либо попытка ветвления поверх занятой revision | REF_HASH_MISMATCH/REF_TYPE_MISMATCH/REF_MISSING/DEPENDENCY_CYCLE либо STALE по соответствующему входу; нет overwrite, частичных outputs или потери lineage |
| R04-T08 | Unknown payload/H fields; missing run_ref; alias вместо SIRef | UNKNOWN_FIELD/MISSING_FIELD/TYPE по точному path; не исправлять и не достраивать |
| R04-T09 | Активной становится I2; отдельно K2 вместо K1 | Idea change инвалидирует соответствующие domain descendants по R1; Creative-only change не переписывает E1; old SELECT не выбирает новую revision; packet currentness проверяется отдельно |
| R04-T10 | Обычный RECORD_INPUT Intake/SourceItem и REVISE ProductionBrief | Прежние допустимые формы/происхождение/outputs R1; HUMAN_EDIT не стирает imported/derived ancestry; никаких новых authority/renderer прав |

### Покрытие прежних cases без изменения artifacts

Проверены все R1-T01–20 и SI-T01–26. AMEND ниже означает дополнение будущих
assertions этим erratum, RETAIN — вся исходная проверка с уточнениями R1 сохранена.

| Cases | Disposition R1a |
|---|---|
| R1-T01, R1-T02, R1-T03 | RETAIN: assembly/export modes и stage checks не меняются |
| R1-T04 | AMEND: human revision example распространяется на StoryIdea и CreativeAlternative; у Creative payload C отдельно от origin REVISION, R04-T01/T03 |
| R1-T05 | AMEND: previous/C closure и отсутствие output backlink, R04-T07 |
| R1-T06, R1-T07, R1-T08, R1-T09, R1-T10 | RETAIN: eligibility, явные Selection, blockers и withdrawal |
| R1-T11 | AMEND: законный путь Idea revision через REVISE_INPUT; не новый id, R04-T01/T09 |
| R1-T12, R1-T13, R1-T14, R1-T15, R1-T16 | RETAIN: selection conflicts, packet closure/privacy и redacted views |
| R1-T17 | AMEND: exact retry REVISE и changed input revision, R04-T05/T06 |
| R1-T18, R1-T19, R1-T20 | RETAIN: historical packet, unavailable mapping, strict RU/UK illustrative refs |
| SI-T01 | RETAIN: offline manual intake; не manual-create StoryIdea/CreativeAlternative |
| SI-T02 | AMEND: нельзя убрать template ancestry через HUMAN_EDIT; C сохраняется, R04-T03/T04 |
| SI-T03, SI-T04, SI-T05, SI-T06, SI-T07 | RETAIN: evidence/rights/duplicates/freshness/UNKNOWN |
| SI-T08 | AMEND: alternate exact input revision и Idea change по R04-T06/T09; previous остаётся audit ancestry |
| SI-T09, SI-T10, SI-T11, SI-T12, SI-T13 | RETAIN: blockers, qualification, capability, UNKNOWN, locale |
| SI-T14, SI-T15 | AMEND: closed sets, обязательные refs, чужой C, previous/hash/cycle, R04-T02/T04/T07/T08 |
| SI-T16 | RETAIN: HUMAN_EDIT не human-review evidence или approval |
| SI-T17 | AMEND: idempotency REVISE, исторический replay без rewind, R04-T05/T06 |
| SI-T18, SI-T19, SI-T20, SI-T21, SI-T22, SI-T23 | RETAIN: adapter/rights/history/factual wording/licensing/renderer limits |
| SI-T24 | AMEND: новая Idea/Creative revision требует exact dependency/reselection checks R04-T09; не переносить старый SELECT |
| SI-T25, SI-T26 | RETAIN: S1/S2/D-01/golden и RU/UK examples без изменений |

## 7. Границы, проверки и owner gate

RU/UK (`ru`/`uk`), offline Windows CPU-only, приватные local inputs и privacy R1
сохранены. Новых provider/API calls, direct editorial handoff, renderer permission,
schema2 authority, source/editorial schema изменений нет. A/E/O/D/S1 contracts,
S2/D-01/golden vectors неизменны. PUBLISH_REVISION DISABLED, partial COMMIT
reconstruction OFF. S3.2a PURE_ONLY и S3.2b BLOCKED_HOST_NOT_PROVIDED сохраняются;
внешние идеи остаются кандидатами, внедрения нет.

Документационные проверки: source remote HEAD равен точной базе; один новый
allowlisted Markdown; локальные ссылки, уникальность/полнота coverage IDs и
`git diff --check` проверяются перед коммитом. Unit/native tests не запускались:
R04 cases — требования к будущей приёмке, не PASS реализации. Publication SHA,
remote equality и чистота worktree сообщаются отдельно после публикации, чтобы не
вводить self-referential commit hash в документ.

Для владельца остаются SI-D01–SI-D10 из original+R1, включая принятие R1a закрытых
sets, dual-run semantics, version/provenance checks и расширенных acceptance cases
в рамках SI-D02/SI-D10. Standalone manual alternatives/manual StoryIdea — отдельная
отложенная возможность, не условие принятия минимального V1. До независимой проверки
и явного approval статус всего предложения не меняется. Реализация не начата.
