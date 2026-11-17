# E01.3.5.3 — contract errata: число top-level keys

Статус: нормативная терминологическая поправка к E01.3.4a/E01.3.5.2.

Canonical dependency payload содержит **семь**, а не шесть обязательных
top-level keys:

1. `dependency_digest_schema_version`;
2. `gate`;
3. `policy_version`;
4. `target_ref`;
5. `production_refs`;
6. `profile_refs`;
7. `dependencies`.

Фактическая JSON-структура в утверждённом контракте и реализации уже содержит
все семь keys. Поправка изменяет только ошибочное словесное количество.
Canonical bytes, golden vectors, SHA-256, schema version и алгоритм не меняются.
Исторические документы сохраняются без переписывания.
