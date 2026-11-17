# E01.3.1 — нормативное уточнение semantic payload для schema 1

Статус: утверждено владельцем проекта 2026-11-04 как уточнение E00 §3.
Сам документ E00 не изменяется. Это уточнение закрывает неоднозначность термина
`audit timestamps` для `editorial_schema_version=1`.

## Общая форма

Semantic payload каждой из девяти ревизионных сущностей — плоский JSON object:

```json
{
  "editorial_schema_version": 1,
  "kind": "...",
  "id": "...",
  "revision": 1,
  "...": "все семантические поля конкретного типа"
}
```

Собственный `RevisionRef.content_hash` не входит в payload. Внутренний
`companion.owner_ref` служит только для точного join и тоже не входит. Все
вложенные RevisionRef сохраняются полностью, включая их `content_hash`.

SourceRevision объединяется с SourceDetails, ClaimRevision — с ClaimReview,
RightsReview — с RightsDetails. Поля с `null` включаются явно. Порядок
семантически значимых массивов сохраняется. Unicode, регистр, пробелы и
комбинируемые символы не нормализуются.

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

`RevisionRef.content_hash` равен lowercase SHA-256 hex этих bytes.

## Закрытый перечень audit timestamp исключений

Для schema 1 из semantic payload соответствующей ревизии исключаются только:

1. `ProductionRevision.created_at`;
2. `SourceDetails.accessed_at`;
3. `ClaimReview.reviewed_at`;
4. `EvidenceLink.reviewed_at`;
5. `RightsReview.reviewed_at`.

Эти значения продолжают храниться в полном JSON snapshot. Изменение одного из
них не меняет content hash соответствующей ревизии.

`SourceDetails.published_at` и `RightsDetails.expires_at` являются
семантическими полями и входят в payload, включая явное значение `null`.
Reviewer, status, qualification, reason, notes и все остальные нетемпоральные
metadata также входят.

`ApprovalRecord.timestamp` и `Event.at` не являются полями отдельной ревизии и
не участвуют в её content hash. Их будущая роль в snapshot checksum не входит в
E01.3.1.

## Точное содержимое по типам

Кроме общей identity-части `editorial_schema_version`, `kind`, `id`, `revision`:

| Тип | Поля semantic payload |
| --- | --- |
| ProductionRevision | title, profile_ref, content_mode, script_locale, narration_locale, subtitle_locale, ui_locale, intended_use, output_preset |
| GenreProfile | profile_key, version, display_name_ru, display_name_uk, allowed_modes, narrative_structure, review_policy_version, rubric |
| CandidateRevision | title, summary, source_refs, discovery_method, discovery_input, assessment, rationale |
| SourceRevision + SourceDetails | title, locator, rights_ref, source_type, author, publisher, published_at, access_notes, reliability_notes, material_digest |
| ClaimRevision + ClaimReview | statement, claim_type, materiality, evidence_links без каждого reviewed_at, review_status, qualification, reviewer, reason |
| ScriptRevision | production_ref, candidate_ref, brief, locale, segments, claim_refs |
| ScenePlanRevision | script_ref, scenes |
| AssetRevision | file_ref, sha256, asset_kind, rights_ref, scene_id, script_ref, text_digest |
| RightsReview + RightsDetails | subject_kind, subject_id, subject_revision, material_digest, intended_use, allowed_actions, status, reviewer, basis, expires_at |

Nested values используют полное нормативное wire-представление E01.1a/E01.2,
за исключением пяти явно перечисленных timestamp-полей.

### Коллизия `AssetRevision.kind`

В JSON snapshot E01.2 поле `AssetRevision.kind` продолжает означать тип медиа
`image|audio|video`. В плоском semantic payload общий ключ `kind` занят identity
ревизии и для AssetRevision всегда равен `asset`. Поэтому только в canonical
semantic payload исходный тип медиа записывается под ключом `asset_kind`.
Decoder, encoder, wire-контракт и модель этим переименованием не изменяются.

## Защита от циклического хэширования прав

SourceRevision и AssetRevision включают полный `rights_ref`. RightsReview не
включает полный Ref проверяемого Source/Asset. Его обратная привязка состоит
только из `subject_kind + subject_id + subject_revision + material_digest`.
Поэтому цепочка Source/Asset → RightsReview не замыкается обратно через
`content_hash` Source/Asset.

`AssetRevision.sha256`, `RightsReview.material_digest`,
`ApprovalRecord.dependency_digest` и `snapshot_checksum` не подменяют
`RevisionRef.content_hash`. E01.3.1 вычисляет и проверяет только последний.
