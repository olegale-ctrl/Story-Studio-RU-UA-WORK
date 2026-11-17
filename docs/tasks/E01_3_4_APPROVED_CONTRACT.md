# E01.3.4a — утверждённый контракт package и dependency digest

Статус: **APPROVED** владельцем проекта 2026-11-04.

Этот документ является отдельным нормативным уточнением E00 §3–4 на основе
`E01_3_4_PACKAGE_CONTRACT_PROPOSAL.md`. E00 и E01.1a сохраняются без изменений
как исторические нормативные документы. Контракт разрешает последующую отдельную
задачу реализации только после явного поручения; сам документ ничего не
реализует.

## 1. Термины и границы

- **Historical package** — exact target и его детерминированное транзитивное
  замыкание по закрытому графу E01.3.2. Active refs не читаются.
- **Current package** — historical package для обязательного active root при
  coherent active chain данного gate.
- **Dependency set** — множество точных RevisionRef, достижимых от target по
  нормативным dependency edges E01.3.2, без самого target.
- **Dependency digest** — lowercase SHA-256 canonical package payload. Это
  consistency token, не цифровая подпись, approval, rights grant или readiness.
- **Stale approval** в контексте dependency consistency — ApprovalRecord, у
  которого gate, policy_version, target_ref или dependency_digest не совпадает
  с пересчитанным current package. Историческая запись не удаляется.

Historical и current package являются разными операциями. Ни одна операция не
выбирает latest revision, не подставляет отсутствующую ссылку и не изменяет
snapshot.

## 2. Roots, active chain и closure

### SCRIPT

- Root и `target_ref`: exact ScriptRevision.
- Closure строится только по E01.3.2 edges и включает referenced production,
  candidate, production/brief profiles, claims, sources и RightsReview.
- ScenePlan и Asset не входят в SCRIPT package.
- `production_refs`: ровно `script.production_ref`.
- `profile_refs`: дедуплицированное точное объединение
  `production.profile_ref` и `script.brief.profile_ref`.
- Current SCRIPT требует non-null active production, candidate и script.
  Active script равен root; его `production_ref` и `candidate_ref` полностью
  равны соответствующим active refs. Active scene_plan на SCRIPT digest не
  влияет.

### SCENES

- Root и `target_ref`: exact ScenePlanRevision.
- Closure строится только по E01.3.2 edges: referenced script и весь SCRIPT
  closure, non-null scene assets, их RightsReview и нормативные asset
  dependencies.
- Production/profile role refs выводятся из referenced script по правилам
  SCRIPT.
- Current SCENES требует non-null coherent active production, candidate,
  script и scene_plan. Active scene_plan равен root, `scene_plan.script_ref`
  равен active script, а script refs равны active production/candidate.

### HANDOFF

- Root, closure, role refs и active coherence совпадают со SCENES.
- Результат называется только **editorial HANDOFF dependency digest**.
- Он не является production readiness, окончательным frozen handoff digest или
  подтверждением неизменности реальных media/config.
- Полный frozen media/config manifest, его versioned digest и pre-render
  проверка определяются отдельным будущим контрактом.

### Отсутствующие и исторические refs

Historical builder требует exact root и полное валидное closure, но не требует
active refs. Current builder возвращает явную ошибку при отсутствующем или
incoherent обязательном slot; автоматический выбор запрещён.

Историческая revision вне target/closure не влияет на package. Явный возврат
active refs к прежней coherent цепочке может восстановить прежний digest. Это
не отменяет revocation и не освобождает от проверки текущих прав и authority.

## 3. Полная integrity-проверка пакета

`validate_reference_graph()` является необходимым, но не достаточным
предусловием. Его нельзя описывать как полную SHA-256 проверку всех исторических
ревизий.

Перед вычислением package digest builder обязан:

1. проверить exact root и нормативный E01.3.2 graph;
2. построить closure только по утверждённым edges;
3. проверить существование и точность каждой зависимости;
4. отдельно пересчитать E01.3.1 `content_hash` target и **каждой включённой
   revision**, используя обязательные Source/Claim/Rights companion metadata;
5. проверить, что каждый полный RevisionRef в target, closure и role arrays
   совпадает с ref целевого объекта;
6. применить E01.3.3 subject/material binding ко всем включённым Source/Asset;
7. проверить version conflicts до canonical serialization.

Будущие approval/readiness операции обязаны вызывать отдельную полную
integrity-проверку непосредственно для пакета. Они не могут считать ранее
полученный ReferenceGraph доказательством hashes всех snapshot-history объектов.

Source с `MaterialBindingState.UNCONFIRMED` может входить в структурно валидный
draft package и digest. Это состояние не разрешает approval, render,
distribution или коммерческое использование.

## 4. Конфликты и дедупликация

- Exact duplicate dependencies дедуплицируются по
  `(kind, id, revision, content_hash)` перед сортировкой.
- Для version-conflict проверки target и dependency set группируются по
  `(kind, id)`.
- Две разные `revision` одной группы дают `PACKAGE_VERSION_CONFLICT` до
  вычисления digest.
- Target участвует в conflict grouping, но не включается в `dependencies`.
- Одинаковый UUID у разных ObjectKind не является конфликтом.
- Revisions вне target/closure являются историей и не участвуют ни в конфликте,
  ни в digest.
- Active refs, не входящие в обязательную coherent chain gate, не расширяют
  closure и не создают конфликт.

При валидном E01.3.2 graph один exact `(kind,id,revision)` не может иметь два
разных допустимых content_hash. Любое такое расхождение является integrity
ошибкой, а не отдельной зависимостью.

## 5. Canonical dependency payload

Payload имеет ровно шесть обязательных keys:

```json
{
  "dependency_digest_schema_version": 1,
  "gate": "SCRIPT",
  "policy_version": "policy-v1",
  "target_ref": {
    "kind": "script",
    "id": "00000000-0000-0000-0000-000000000000",
    "revision": 1,
    "content_hash": "0000000000000000000000000000000000000000000000000000000000000000"
  },
  "production_refs": [],
  "profile_refs": [],
  "dependencies": []
}
```

Нормативные правила:

- `dependency_digest_schema_version` — integer 1;
- `gate` — exact string SCRIPT, SCENES или HANDOFF;
- `policy_version` — переданный nonempty exact string;
- `target_ref` — полный exact RevisionRef требуемого root kind;
- `production_refs` и `profile_refs` — полные role refs из §2;
- `dependencies` — полное transitive closure без target, включая production и
  profiles, которые также присутствуют в role arrays;
- все arrays присутствуют, включая пустые;
- exact refs дедуплицируются;
- `dependencies`, `production_refs`, `profile_refs` сортируются лексикографически
  по `(kind.value, id, revision)`;
- неизвестные root keys и неполные refs запрещены;
- смысловой порядок внутри revision payload не пересортировывается: он уже
  связан проверенным `RevisionRef.content_hash`.

Canonical bytes:

```python
json.dumps(
    payload,
    ensure_ascii=False,
    sort_keys=True,
    separators=(',', ':'),
    allow_nan=False,
).encode('utf-8')
```

`dependency_digest = hashlib.sha256(canonical_bytes).hexdigest()`.

Dependency digest и `snapshot_checksum` являются разными значениями. Builder не
вычисляет, не подставляет и не проверяет snapshot checksum.

## 6. Policy version и актуальность ApprovalRecord

Digest builder принимает supplied `policy_version` буквально. Он не требует
равенства `GenreProfile.review_policy_version` и не выбирает действующую policy.
Policy mapping и authority относятся к будущему service. Изменение supplied
policy_version всегда меняет canonical payload и digest.

Dependency-consistency совпадение ApprovalRecord требует одновременно:

1. совпадающий gate;
2. совпадающий policy_version;
3. полный exact `approval.object_ref == package.target_ref`;
4. `approval.dependency_digest == package.dependency_digest`;
5. успешно пройденную полную package integrity из §3.

Даже полное совпадение этих условий не означает действующий approve. Decision
history, reject/revise/revoke, actor authority, review declarations, rights
policy/expiry/intended_use, material-fact coverage и gate ordering проверяются
отдельно.

## 7. Rights, Source и Asset composition

Dependencies определяются только closure E01.3.2; скрытые edges запрещены.

| Gate | Source/Rights | Asset/Rights |
| --- | --- | --- |
| SCRIPT | Candidate.source_refs, Claim evidence sources и их exact RightsReview | Scene assets не входят |
| SCENES | Полный SCRIPT Source/Rights closure | Non-null scene.asset_ref, exact Asset RightsReview и нормативный nullable asset.script_ref |
| HANDOFF | Как SCENES | Как SCENES; media/config manifest остаётся отдельным будущим слоем |

RightsReview subject locator не является reverse graph edge. Альтернативный
RightsReview вне closure не влияет на digest. Для его выбора SourceRevision или
AssetRevision создаёт новую revision с новым exact rights_ref, после чего новые
refs должны дойти до нового package target.

E01.3.3 `CONFIRMED` подтверждает только совпадение сохранённого material digest.
Status approved/restricted/unknown/blocked, intended_use, allowed_actions и
expires_at не оцениваются builder как разрешение. Rights policy service не
реализуется этим контрактом.

## 8. Staleness rules

- Новая, но не referenced history revision не меняет package.
- Новая referenced Source/Claim/Profile/Rights revision меняет SCRIPT и все
  downstream packages через новый exact target/closure.
- Новый ScriptRevision меняет SCRIPT, SCENES и HANDOFF packages.
- Новый ScenePlanRevision при прежнем script не меняет SCRIPT, но меняет SCENES
  и HANDOFF.
- Новая referenced AssetRevision не меняет SCRIPT, но меняет SCENES/HANDOFF.
- Новый supplied policy_version меняет digest соответствующего gate.
- Incoherent или неполная active chain означает отсутствие current package, но
  не мешает воспроизводить historical package по exact target.
- Возврат к прежней exact coherent chain может дать прежний digest, но требует
  новой проверки revocation, current rights и authority.
- Изменение поля, исключённого E01.3.1 из semantic hash, не меняет dependency
  digest, если все RevisionRef.content_hash остаются теми же.

## 9. Связь с production handoff

Editorial HANDOFF dependency digest связывает точные production/profile,
script, scenes, sources, rights и assets редакционной модели. Перед будущим
render дополнительно обязательны действующие approvals, rights/expiry policy,
frozen media/config manifest, проверка реальных staged bytes и повторная сверка
непосредственно перед запуском.

Существующий FFmpeg pipeline не изменяется и не становится источником approval
authority. Этот контракт не определяет readiness и не разрешает коммерческое
использование.

## 10. Отложенные реализации

Документ не реализует dependency digest. Отдельного разрешения требуют:

- historical/current package builders;
- full package integrity API;
- canonical serialization и SHA-256 dependency digest;
- сопоставление ApprovalRecord и decision/revocation authority;
- snapshot checksum;
- rights policy и expiry evaluation;
- frozen handoff manifest и production readiness.
