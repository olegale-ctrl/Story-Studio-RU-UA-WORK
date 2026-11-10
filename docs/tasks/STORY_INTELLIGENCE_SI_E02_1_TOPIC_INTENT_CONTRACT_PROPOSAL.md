# SI-E02.1 — Durable Topic Intent contract proposal

Дата: 2026-11-10 (Europe/Kyiv).
**PROPOSAL / NOT APPROVED / NOT IMPLEMENTED.**
Base: `a577746f308828d75d2ea7262eaa94ab18a523c1`.
Authority: [P02 owner approval](STORY_INTELLIGENCE_SI_E02_1_OWNER_APPROVAL_2026_11_10.md)
разрешает **design only**. Каждый TI-Pxx ниже — recommendation для отдельного решения,
не текущая SI/1 норма и не разрешение новой operation/schema/persistence.

## 1. Цель и доказанная недостаточность existing Selection

Durable Topic Intent — человеческое намерение относительно **одной exact StoryIdea
revision в конкретном audience/channel context**. Это не approval истинности темы,
не rights grant и не job в производственной очереди.

Existing [records_v1](../../story_intelligence/records_v1.py):

- `_SCOPE.purpose`: только CREATIVE_CHOICE / BRIEF_REVIEW;
- Selection.target_ref: только CreativeAlternative / ProductionBrief;
- choice: только SELECT / REQUEST_CHANGES / WITHDRAW;
- `_local` связывает purpose с допустимым target type.

[R1 §4.1](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md) определяет одну chain
на exact scope, manual human intent и immutable history. [R1a](STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md)
исключает Selection из REVISE_INPUT; это не HUMAN_EDIT record с REVISION Run.
StoryIdea exact ref и CandidateRevision.assessment не содержат durable research/defer/
reject/prioritize decision. Кодировать это в `reason`, `rationale` или существующем
SELECT другого target нельзя: изменяется смысл утверждённых полей.

## 2. Альтернативы и TI-P01 — рекомендуемый minimum

| Вариант | Польза | Недостаток / compatibility cost |
| --- | --- | --- |
| A. Без schema extension: private working note + later existing Creative/Brief selections | Legacy wire не меняется | Не выполняет durable topic intent requirement; note не machine-readable decision и не должен им называться |
| B. Минимально расширить Selection purpose/target/choice под отдельной утверждённой версией | Повторно использует exact refs, chain, manual origin, conflict/idempotency semantics; не создаёт parallel approval | Нужны versioned dispatch/compatibility и новые purpose-specific validation/oracles; нынешний parser отвергнет новые values |
| C. Отдельный TopicIntent record/command | Можно полностью изолировать lifecycle | Новый type увеличивает schema/resolver/export/migration surface; необходимость отдельно доказать, authority всё равно не появляется |

**TI-P01 recommendation: B.** Название Topic Intent в этом документе — concept,
не уже добавленный RecordType. Вариант C оставить только при доказанной невозможности
B, не ради удобства. Никаких изменений кодеков, H.si_version или existing vectors сейчас.
Owner должен отдельно выбрать schema/interface version и old/new reader behavior.
**Unversioned extension SI/1 под видом прежнего контракта не предлагается.**
Новые purposes не передавать текущим accepted resolver/currentness как будто они supported.

## 3. TI-P02 — candidate semantics, НЕ утверждённые wire tokens

Предлагаемые обозначения purpose `TOPIC_INTENT` и actions `RESEARCH`, `DEFER`,
`REJECT`, `PRIORITIZE` — **PROPOSAL ONLY**, не current enums/operation names.
Рекомендуется расширение existing RECORD_SELECTION по purpose в отдельно versioned
contract; отдельный command — альтернатива, exact method name/version не выбран.
В recommended B это кандидаты для purpose-specific `choice`, не новое поле
`action` или новый request envelope. Не добавлять SCIENCE_APPROVE, APPROVE
или production permission.

| Candidate action | Предлагаемый человеческий смысл | Чего не делает |
| --- | --- | --- |
| RESEARCH | Продолжить/начать human research exact темы | Не запускает search/provider, не подтверждает claims |
| DEFER | Отложить дальнейшее рассмотрение | Нет scheduler/deadline/TTL, скрытого автоматического возврата |
| REJECT | Отказаться от разработки этой exact темы/context | Не удаляет тему/источники/history и не является editorial REVOKE/доказательством ложности |
| PRIORITIZE | Явно выделить тему для внимания/research человеком | Не total ordering, automatic rank/tie-break, job assignment или готовность к производству |

Несколько PRIORITIZE допустимы как attention labels в recommended variant; порядок
между ними человек определяет отдельно. Numeric rank, assignee и deadline отсутствуют.
Если нужен durable ordered backlog, это дополнительный contract requirement, не
JSON в reason и не следствие P01. Exact action set/meaning требует owner approval.
Existing Creative/Brief purpose сохраняют прежние choices; REJECT нельзя незаметно
добавить к BRIEF_REVIEW, SELECT нельзя переопределить как «исследовать тему».

## 4. TI-P03 — exact scope, authority и admission

Рекомендуемый scope повторно использует existing fields purpose/idea_ref/audience_ref/
channel_ref с отдельным candidate purpose. Для новой роли target_ref должен быть
**тем же full SIRef**, что scope.idea_ref (type/id/revision/sha256), а не просто тем же id.
Idea genesis/provenance остаётся DISCOVERY или её legal HUMAN_EDIT revision; Topic
Intent не стирает originating Run и не создаёт manual StoryIdea.

Предлагаемый admission порядок (не реализованный API):

1. Version/closed shape/ref types; accepted exact graph/hash/Closure/provenance
   проверки существующих domain inputs. Новые Selection values сначала требуют
   отдельно утверждённого schema/dispatch contract; старый validator не «обходится».
2. Explicit observed active inputs и heads, expected_context_hash; target exact Idea,
   audience/channel должны соответствовать выбранному current view, без latest lookup.
3. G01/G02/F1-D1 currentness для existing domain inputs. INVALID и STALE не принимаются
   как новый current intent. CURRENT сам по себе не означает, что target selected:
   отдельно проверить exact target membership/context, не выводить его из одного id.
4. Человек явно выбирает действие и authored reason. Ни machine score, ни label,
   ни template suggestion не выбирают действие за него. Principal/authority proof
   не придумываются: это untrusted private workspace human-intent assertion, не
   защищённая A1–A14 identity или editorial grant.
5. Compare-and-set exact predecessor/head и idempotency check до append/обновления
   logical head. Persistence/admission atomicity — отдельный SI-D03 contract.

RESEARCH/DEFER/REJECT/PRIORITIZE в recommended variant разрешают research choice
при валидных current **unknown research data**; scientific eligibility при этом
может быть BLOCKED/NEEDS_RESEARCH. Missing SIRef не UNKNOWN. Relevant ERef без validated
snapshot → INVALID/REF_MISSING по действующим правилам; не удалять ERef ради записи.
Порядок и exact mapping response codes нового method ещё требуют approval; reuse
существующих TYPE/REF_*/INPUT_STALE/SELECTION_CONFLICT/REQUEST_CONFLICT предпочтительнее
нового error vocabulary. Это не утверждение, что current operation уже поддержана.

## 5. TI-P04 — immutable chain и head selection

Рекомендуется сохранить R1 exact-scope правило: initial Selection id/revision1,
previous=null; следующее действие **того же exact scope** — тот же Selection id,
revision+1, previous=точный head. Origin остаётся MANUAL_INPUT, без подмены на
HUMAN_EDIT/REVISION Run. Stored record immutable, reason нового действия не стирает старый.

В proposed scope target identity фиксирована через exact idea_ref. Новая Idea revision,
audience или channel reference создаёт новый exact scope/new chain после отдельного
человеческого действия. Старые research/reject/priority intents остаются history,
не переносятся на новую revision автоматически, даже при похожем тексте.
Нет объявленного head → «решения нет» в человеческом представлении, не implicit RESEARCH.
Две heads/fork/conflicting exact identities → отказ, не выбор по clock/max UUID.

Предлагаемый H.input_refs construction order: previous head (если есть), затем
scope Idea/Audience/Channel и target в declared payload order. Repeated exact refs
не удалять из authored arrays; только Closure manifest — unique canonical set.
**Этот новый builder order — recommendation**, его versioned normative spelling
и варианты admission необходимо утвердить; сейчас существующий codec не изменяется.

## 6. TI-P05 — idempotency, retries и currentness

Повторно использовать [R1 §6](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md):
request_id + exact canonical request bytes; все target/scope/action/reason/previous/
expected-context и locale differences существенны, Unicode не нормализуется.
Идентичный retry возвращает прежний exact output ref, без нового UUID/time/revision
и без возврата head назад после более позднего действия. Другие bytes с тем же id →
REQUEST_CONFLICT, без новых outputs. Current applicability пересчитывается отдельно.

Record history validity не равна applicability к сегодняшнему view. Даже если старая
Idea семантически CURRENT по неизменным inputs, intent для другой exact Idea revision
не становится решением о новой. Смена source/check refs может сделать dependent inputs
STALE без изменения frozen record. Изменение topic head **не меняет E1 currentness**
само по себе; не добавлять topic intent в EVALUATE.semantic_input_refs как новый
prerequisite. Used creative Selection Brief и Packet whole-context freshness остаются
по R1; новую topic-head capture/projection integration отдельно согласовать, не
приписывать её current UI/Packet code.

G01 history-only refs не required-current; G02 original C direct claims сохраняются;
F1-D1 actual producer header ERefs и original C relevant, historical-only Run — audit.
Ни rebasing, ни automatic reapproval, ни сохранение CURRENT в качестве authority token.

## 7. TI-P06 — workspace, privacy, retention

Принцип SI-D03 уже approved: private user-owned workspace вне Git/protected roots.
Точные path/atomicity/locking/CAS/idempotency-map integrity/backup/retention/delete
ещё не закрыты. Нужна согласованная atomic запись record + request mapping + logical
head; не заявлять durable transaction/crash safety на основании RAM-only tests.

Intent reason/selector label могут быть private; R1b не даёт права экспортировать
новую тему/choice/label как FieldView по аналогии. Existing redaction/whitelist и
privacy review не обходить, Packet display mapping для новой роли — отдельный gate.
Потеря output/mapping после retention → existing RECORD_UNAVAILABLE/UNAVAILABLE
semantics в будущем контракте, не reconstruction удалённого намерения через retry.
Никаких придуманных TTL/quota/default backup destinations или trusted S1 receipts.
Native S3.2b не prerequisite для pure design, но не доступный protected writer.

## 8. Совместимость, решения и independent oracle requirements

| Proposal choice до реализации | Recommended | Что заблокировано без approval |
| --- | --- | --- |
| TI-P01 format/version | Versioned minimal Selection extension, legacy SI/1 unchanged | Любой новый purpose/action/target и parser dispatch |
| TI-P02 actions/method | Four candidate human actions; purpose-specific existing-command extension | Wire operation names/options и semantics |
| TI-P03 scope/admission/authority | Exact Idea/Audience/Channel + explicit human action, no grants | Признание нового current intent |
| TI-P04 chain/input order | Exact-scope append-only chain, explicit predecessor/CAS | Head mutation, concurrent command behavior |
| TI-P05 replay/applicability | R1 byte-exact retry; no head rollback/auto-transfer | Runtime replay/projection |
| TI-P06 durable lifecycle/privacy | Separate SI-D03/SI-D07 exact contract | Persistence, backup/restore/retention/export |

Будущие **независимые** oracles должны заранее зафиксировать expected refs/states/
existing codes и буквальные canonical hashes, а не копировать результат нового method.
Нужны genuine content-addressed graphs с accepted domain provenance, без hash/resolver
mocks. Для новой роли literal records возможны только после утверждённого wire/version;
нельзя объявлять current SI/1 parser PASS на ещё не поддерживаемом target.

| Oracle case — future requirement, NOT RUN | Что независимо проверить |
| --- | --- |
| Legacy scopes | Старые bytes/hashes/choices и все existing vectors unchanged; new tokens отвергаются legacy reader |
| Four candidate actions | Exact scope/target binding, manual origin, deterministic full bytes; не science/production approval |
| Wrong target/scope/hash/missing ref/cycle | Fail closed, no partial output, no latest fallback |
| Same id, different Idea revision | Нет переноса intent; новая exact chain только explicit human action |
| Conflicting head/concurrent initial requests | Explicit CAS conflict; нет time/UUID tie-break |
| Identical/different request-id retries | Same ref/no new head; REQUEST_CONFLICT при changed canonical bytes |
| Retry old RESEARCH после нового REJECT/DEFER | Старый record возвращается как historical, head не откатывается |
| Changed source/check/context | Honest STALE/INVALID по accepted inputs; нет automatic rebase |
| Topic head change only | E1 semantic currentness прежняя; нет future-selection dependency |
| ERef current producer/history boundary | F1-D1 honored; UNKNOWN/hash не validated material; historical-only не promoted |
| Loss/retention/backup | Нет resurrection deleted outputs/старых heads; guarantees ограничены будущим lifecycle contract |
| Private labels/reason | Нет implicit public export/identity proof; RU/UK exact Unicode и detached read-only results |

**NOT RUN — DOCS ONLY.** Это test-oracle requirements, не executable tests или PASS.
Ни TI-P01–TI-P06, ни новые tokens/type/version не утверждены P02 design approval.
Без отдельного owner approval и exact-base/allowlist implementation task — STOP.
SI-E02.2, UI, persistence/assignment/provider/ERef adapter не начинать. `PUBLISH_REVISION`
DISABLED; partial COMMIT reconstruction OFF; Windows S3.2b BLOCKED_HOST_NOT_PROVIDED.
