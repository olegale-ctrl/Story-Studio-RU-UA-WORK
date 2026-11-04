# E01.3.4 — предложение контракта активного пакета и dependency digest

Статус: **PROPOSAL / NOT APPROVED**. Документ не изменяет E00, E01.1a,
модели или runtime. Каждое правило ниже, помеченное «Рекомендуется», требует
решения владельца проекта до реализации.

## 1. Нормативная база и термины

E00 §3 уже требует canonical dependency object с `gate`, `policy_version`,
`target_ref`, relevant production/profile refs и отсортированным списком точных
transitive RevisionRef. Missing refs, неверные object hashes, cycles, foreign
production и конфликтующие версии в одном активном пакете являются ошибками.
E00 §4 связывает SCRIPT, SCENES и HANDOFF с разными уровнями review, запрещает
автоматически переносить решения на изменённые зависимости и сохраняет старые
approvals как историю.

E01.3.1 определяет content hash одной ревизии. E01.3.2 определяет точные
dependency edges и локальный граф. E01.3.3 проверяет subject/material binding,
но `CONFIRMED` не является разрешением. На этой основе предлагаются термины:

- **historical package** — детерминированное замыкание точного target_ref;
  вычисляется независимо от active refs и ничего не активирует;
- **current package** — historical package, target которого совпадает с
  обязательным active root, а связанные active slots образуют coherent chain;
- **dependency set** — множество точных RevisionRef, достижимых от target по
  утверждённым E01.3.2 dependency edges, без самого target;
- **dependency digest** — SHA-256 canonical package payload; consistency token,
  не approval, подпись, rights grant или readiness;
- **stale approval** — ApprovalRecord, чьи gate/policy/target/digest больше не
  совпадают с выбранным current package. Историческая запись не удаляется.

## 2. Предлагаемые package roots

### SCRIPT

Рекомендуется:

- gate target и root: exact `RevisionRef(kind=script)`;
- historical closure: все E01.3.2 зависимости ScriptRevision — production,
  candidate, profile refs frozen brief/production, claims, sources и их
  RightsReview;
- AssetRevision и ScenePlanRevision не включаются;
- relevant production refs: ровно `script.production_ref`;
- relevant profile refs: точное объединение
  `production.profile_ref` и `script.brief.profile_ref`;
- current SCRIPT package требует non-null active production, candidate и
  script; они должны точно совпадать с `script.production_ref`,
  `script.candidate_ref` и root. active scene_plan может быть null или любым
  отдельно проверяемым downstream selection и на SCRIPT digest не влияет.

Обоснование: E00 прямо говорит, что не связанная с narration смена still image
не меняет SCRIPT gate. Source/claim/profile/rights изменения должны менять
SCRIPT package лишь когда новая точная ревизия вошла в closure нового script.

### SCENES

Рекомендуется:

- gate target и root: exact `RevisionRef(kind=scene_plan)`;
- closure: script closure плюс сам referenced ScriptRevision, scene assets,
  asset RightsReview и любые нормативные зависимости assets;
- relevant production/profile refs выводятся из referenced script так же, как
  для SCRIPT;
- current SCENES package требует coherent non-null active production,
  candidate, script и scene_plan; `scene_plan.script_ref` точно равен active
  script, а script refs равны active production/candidate.

Scene order и asset refs уже входят в ScenePlan content hash. Замена still asset
требует новую ScenePlanRevision с точным asset_ref и меняет SCENES package, но
не SCRIPT package.

### HANDOFF

E00 требует SCRIPT и SCENES approvals, текущие права, frozen assets/config и
повторную проверку перед render. Текущая editorial model содержит scene plan и
assets, но не содержит frozen handoff config/media manifest.

Рекомендуется двухфазное правило:

1. В рамках текущей schema 1 editorial dependency package HANDOFF имеет root
   exact `RevisionRef(kind=scene_plan)`, closure и active coherence как SCENES.
   Из-за разных `gate` и `policy_version` его digest всё равно отличается.
2. Такой digest считать только **editorial HANDOFF dependency digest**, а не
   полной готовностью к видеопроизводству. Будущий handoff manifest/config
   получает отдельный versioned digest или новую версию package contract до
   выдачи production readiness.

Альтернатива — запретить формирование HANDOFF digest до появления manifest.
Она строже, но блокирует фиксацию editorial approval уже сейчас. Выбор требует
утверждения владельца.

## 3. Active refs, история и отсутствующие slots

Рекомендуется разделить две операции:

1. `build_historical_package(gate, policy_version, target_ref)` требует только
   точный target и валидное closure. Active refs не читаются. Это позволяет
   воспроизводить и проверять старый ApprovalRecord.
2. `build_current_package(gate, policy_version)` выбирает только утверждённый
   active root и требует coherent active chain из §2. Отсутствующий обязательный
   slot даёт `INCOMPLETE_ACTIVE_PACKAGE`; никакой latest/default не выбирается.

Исторические ревизии сохраняются и могут образовать historical package. Явное
переключение active refs обратно на полностью coherent старую цепочку может
восстановить тот же dependency digest. Это не оживляет revoked approval и не
обходит текущую rights/policy evaluation: digest доказывает только тождество
зависимостей.

Добавление новой, но нигде не referenced ревизии в историю не меняет текущий
package. «Последняя версия» не имеет особого значения.

## 4. Конфликт версий внутри пакета

Рекомендуется:

- сначала построить exact reachable dependency set;
- повторяющиеся ссылки на одну exact identity дедуплицировать;
- сгруппировать target и dependency set по `(kind, id)`;
- если в одной группе присутствуют разные `revision`, вернуть
  `PACKAGE_VERSION_CONFLICT` до вычисления digest;
- одинаковый UUID у разных ObjectKind конфликтом не считать;
- версии вне closure/target разрешены как snapshot history;
- active refs, не входящие в coherent chain данного gate, не добавлять в пакет
  и не использовать как основание конфликта.

Включение target в проверку конфликта важно: closure не должно одновременно
содержать другую ревизию того же script/scene_plan ID. Сравнение выполняется по
revision, а exact `content_hash` дополнительно проверяется E01.3.2.

## 5. Предлагаемый canonical dependency payload

Предлагается отдельная версия алгоритма, чтобы не смешивать её с
`editorial_schema_version` и content-hash schema:

```json
{
  "dependency_digest_schema_version": 1,
  "gate": "SCRIPT",
  "policy_version": "policy-v1",
  "target_ref": {
    "kind": "script",
    "id": "...",
    "revision": 3,
    "content_hash": "..."
  },
  "production_refs": [
    {"kind":"production","id":"...","revision":2,"content_hash":"..."}
  ],
  "profile_refs": [
    {"kind":"genre_profile","id":"...","revision":4,"content_hash":"..."}
  ],
  "dependencies": [
    {"kind":"candidate","id":"...","revision":1,"content_hash":"..."}
  ]
}
```

Рекомендуемые правила:

- все шесть root keys обязательны; неизвестные keys запрещены;
- `gate` — закрытый SCRIPT|SCENES|HANDOFF;
- `policy_version` — переданный nonempty exact string; выбор действующей policy
  и соответствие GenreProfile.review_policy_version остаются authority/service;
- `target_ref` полный и не повторяется в `dependencies`;
- `dependencies` — всё transitive closure без target, включая production и
  profiles; отдельные `production_refs`/`profile_refs` намеренно повторяют эти
  refs как role bindings, которых требует E00;
- exact duplicates удаляются до сериализации;
- `dependencies`, `production_refs` и `profile_refs` сортируются по
  `(kind.value, id, revision)`; поскольку конфликт ревизий уже исключён,
  `content_hash` не нужен как tie-breaker;
- каждый Ref содержит `content_hash`, проверенный E01.3.1/E01.3.2;
- canonical bytes используют `ensure_ascii=False`, `sort_keys=True`,
  `separators=(',', ':')`, `allow_nan=False`, UTF-8;
- digest — lowercase SHA-256 этих bytes;
- пустые arrays записываются явно, хотя валидные gate packages обычно имеют
  production/profile dependencies.

Не рекомендуется сортировать исходные narrative/scene/evidence arrays:
dependency payload содержит только refs, а их content hashes уже связывают
семантически значимый внутренний порядок.

## 6. Актуальность ApprovalRecord

Рекомендуемый consistency predicate для кандидата ApprovalRecord:

1. `approval.gate == requested gate`;
2. `approval.policy_version == current policy_version`;
3. `approval.object_ref == package.target_ref` полностью, включая hash;
4. `approval.dependency_digest == computed package digest`;
5. package успешно прошёл graph/hash/conflict checks.

Изменение любого canonical поля создаёт другой digest. Однако совпадение этих
пяти условий не означает действующий approve: decision history, revoke/reject,
actor authority, material fact coverage, rights status/expiry/intended_use и
gate ordering проверяются будущим service.

Если immutable source/profile/rights/asset меняется, создаётся новая revision.
Digest меняется только когда точная новая revision становится достижимой из
нового target. Новая невключённая history revision сама по себе не делает
старый exact package другим.

## 7. Rights и materials по gate

Рекомендуемый состав следует только E01.3.2 closure:

| Gate | Source/rights dependencies | Asset/rights dependencies |
| --- | --- | --- |
| SCRIPT | Candidate.source_refs и Claim evidence sources; их exact RightsReview | Нет scene assets |
| SCENES | Весь SCRIPT source/rights closure | Все non-null scene.asset_ref, их exact RightsReview; нормативные asset.script_ref dependencies |
| HANDOFF | Как SCENES | Как SCENES; будущий frozen media/config manifest добавляется отдельно после утверждения контракта |

RightsReview semantic hash включает status, intended_use, allowed_actions,
material_digest и expiry согласно E01.3.1. Поэтому новая referenced rights
revision меняет package. E01.3.3 `CONFIRMED` требуется как structural/material
предусловие для последующей policy evaluation, но не означает разрешённое
действие. `UNCONFIRMED` package можно детерминированно хэшировать для draft и
истории, но нельзя на этом основании объявлять ready/allowed.

Не referenced альтернативный RightsReview не входит в closure и не меняет
digest. Чтобы выбрать его, SourceRevision/AssetRevision должен получить новую
ревизию с новым exact rights_ref; далее меняются все downstream refs до target.

## 8. Сценарии изменения и ожидаемая актуальность

Ниже «stale» означает несовпадение target/digest current package, а не удаление
исторического ApprovalRecord.

| Сценарий | SCRIPT | SCENES | HANDOFF | Причина |
| --- | --- | --- | --- | --- |
| Добавлена SourceRevision v2, но target closure всё ещё ссылается на v1 | актуален | актуален | актуален | Невключённая история не меняет exact package |
| Candidate/Claim и новый Script теперь ссылаются на Source v2 | stale | stale | stale | Новый script target и source closure |
| Изменён текст/segments ScriptRevision | stale | stale | stale | Новый script; старый scene_plan больше не coherent с active script |
| Создан новый ScenePlan для того же exact script | актуален | stale | stale | SCRIPT root/closure прежние, scene root изменён |
| Still Asset заменён новой revision и новый ScenePlan ссылается на неё | актуален | stale | stale | Asset и rights входят только в scene/handoff closure |
| Source/Asset получил новую revision с новым rights_ref | stale только для затронутого script closure | stale | stale | Referenced RightsReview/content hashes изменены |
| Production/Profile revision изменена и новый script связывает её | stale | stale | stale | Production/profile входят во все gate packages |
| Изменён только `policy_version` | stale | stale | stale | policy_version — canonical digest field |
| Active script переключён, active scene_plan оставлен от старого script | current package отсутствует | current package отсутствует | current package отсутствует | Active chain incoherent; historical digest обоих targets вычислим |
| Active refs явно возвращены к прежней coherent цепочке | digest может совпасть со старым | digest может совпасть | digest может совпасть | Нужны отдельные revoke/current-rights checks |
| Изменён только исключённый audit timestamp без смены semantic hash | актуален | актуален | актуален | E01.3.1 content hash намеренно неизменен |

## 9. Связь с production handoff

Предлагаемая цепочка проверки перед будущим render:

1. получить coherent current HANDOFF root без latest fallback;
2. повторно проверить E01.3.1 hashes, E01.3.2 graph и E01.3.3 bindings;
3. построить canonical editorial package и digest;
4. найти соответствующие действующие SCRIPT/SCENES/HANDOFF approvals по точным
   target/digest/policy данным и проверить decision/revocation;
5. применить rights-policy и expiry относительно явного evaluation time;
6. собрать frozen handoff manifest с config и фактическими staged media hashes;
7. непосредственно перед render повторно сверить editorial и manifest digests.

Так pipeline получит именно проверенные script/scene/assets, но существующий
FFmpeg код не меняется и не становится authority. E01.3.4 определяет только
предложение контракта данных для будущей реализации.

## 10. Таблица неоднозначностей и решений для утверждения

| Вопрос | Основание в E00 | Возможные варианты | Рекомендуемое решение | Последствия |
| --- | --- | --- | --- | --- |
| Historical и current package — одна операция? | Exact refs, history retained, active selections | Всегда требовать active; либо разделить | Разделить historical/current builders | Старые approvals воспроизводимы; current требует active coherence |
| Какие active slots обязательны? | Empty drafts допустимы; gates требуют exact script/scenes | Только root; либо полная chain | SCRIPT: production+candidate+script; SCENES/HANDOFF: плюс scene_plan | Missing/incoherent slots дают явную ошибку, без latest |
| Что является SCRIPT root? | Gate SCRIPT требует exact script | active production; script | Exact ScriptRevision | Digest связан с утверждаемым текстом и frozen brief |
| Что является SCENES/HANDOFF root? | SCENES exact coverage; HANDOFF требует scenes/assets | script; scene_plan; manifest | Exact ScenePlanRevision; manifest отдельно | Scene/asset изменения видимы, script closure транзитивен |
| HANDOFF digest сейчас полный? | E00 требует frozen config/assets, модели manifest нет | Запретить; считать editorial subset | Editorial HANDOFF digest сейчас, manifest digest позже | Можно review editorial state, нельзя называть render-ready |
| Входит ли target в dependencies? | E00 отдельно называет target_ref и transitive refs | Включать дважды; исключить | Исключить из dependencies, но включить в conflict grouping | Нет лишнего duplicate, identity target остаётся canonical |
| Production/profile refs дублируются в dependencies? | E00 называет их отдельно и как reachable refs | Исключить из closure list; повторить | Повторить в dependencies и role arrays | Payload самодостаточен; role binding явный, небольшой redundancy |
| Ключ версии digest schema | E00 не задаёт имя | editorial_schema_version; отдельная версия; без версии | `dependency_digest_schema_version=1` | Алгоритм можно версионировать независимо |
| Когда версии конфликтуют? | E00: conflicting versions одного id в active package | Вся history; active slots; closure | Только target+closure, по `(kind,id)` | History разрешена; неоднозначный package отклонён |
| Повтор exact ref — конфликт? | Exact refs, graph допускает повтор ссылок | Считать повтором; дедуплицировать | Дедуплицировать до sorting | Один dependency не влияет на hash числом упоминаний |
| Разные ObjectKind с одним UUID конфликтуют? | E01.3.2 identity включает kind | Глобальный UUID; kind-scoped | Не конфликтуют | Совместимо с принятым Q5/graph identity |
| `policy_version` должен равняться profile value? | Оба поля существуют, equality не определена | Жёсткое equality; service mapping | Digest принимает exact supplied policy_version; authority решает mapping | Не вводится скрытая policy, смена строки всегда меняет digest |
| Какие rights входят в SCRIPT? | SCRIPT проверяет facts/rights; graph closure | Только claim evidence; candidate+claims | Полный script closure, включая candidate sources | Provenance и referenced rights защищены вместе |
| `UNCONFIRMED` запрещает вычислить digest? | Drafts допустимы; не означает права | Запретить package; разрешить draft hash | Digest вычислим, approval/readiness блокируются отдельно | История детерминирована без ложного grant |
| Может старый digest снова стать current? | Explicit old selection allowed; revocations separate | Никогда; при exact coherent возврате | Может совпасть, но authority/revocation/rights проверяются заново | Digest остаётся identity, не оживляет approval |

## 11. Вопросы владельцу проекта

До реализации dependency digest требуется явно утвердить или изменить:

1. Разделение historical package и current package.
2. Обязательные active slots и coherence rules для каждого gate.
3. Roots и closure SCRIPT/SCENES/HANDOFF.
4. Двухфазную трактовку HANDOFF: editorial digest сейчас, manifest/config позже.
5. Canonical payload из §5, включая имя/version key, target exclusion и
   повтор production/profile refs в dependencies.
6. Conflict rule по `(kind,id)` только внутри target+closure и exact-ref dedupe.
7. Полный rights/source/asset состав по таблице §7.
8. Возможность вычислить digest для structurally valid UNCONFIRMED draft без
   права считать его approved/ready.
9. Правило historical reactivation: digest может совпасть после явного возврата
   active chain, но authority/revocation/current rights проверяются заново.
10. Отсутствие обязательного equality между supplied policy_version и
    GenreProfile.review_policy_version на уровне digest builder.

До этих решений документ остаётся предложением. Код E01.3.4 и следующие этапы
не разрешены этим docs-only результатом.
