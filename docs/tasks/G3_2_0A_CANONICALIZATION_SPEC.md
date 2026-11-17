# PG-C14N-1 — proposed exact canonicalization

**FREEZE_PROPOSAL — NOT APPROVED.** SI-INTEGRATION-G3.2.0a; 2026-11-17 (Europe/Kyiv).
Base `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`.
Pinned discovery `9551e490dbda11e372b11e758a2a0aafdb740ce1`, tree `dee2c06cc2274a26bb0dc8d3082fc31e16b81b3c`.
Только docs/offline vectors. Направление OD-PG-01–12 принято владельцем, но численные значения, роли, trust policies и operational protocols не утверждены. Нет validators/providers, permissions или qualification.

## Область и ошибки до digest

Спецификация детерминирована **под предложенными решениями**, но не утверждена. C14N value probe может быть JSON scalar/array/object; настоящий PG input всегда closed Envelope. Positive value probe не означает valid PG contract. Никакой serializer не импортирован из G1/G2/SI/PG; production PG serializer отсутствует.

| Rule | Предлагаемое точное правило | Отказ |
|---|---|---|
| C01 | Input bytes строго UTF-8, без BOM; ровно одно JSON value, разрешён только JSON whitespace20/09/0A/0D до/после; no trailing second value. Raw wire size проверяется до decode | PG_FORMAT до digest |
| C02 | После decode только Unicode scalar values. Literal unescaped controls запрещены JSON syntax. Escaped surrogate pair превращается в один scalar; lone high/low surrogate reject. Никакой NFC/NFD/trim/casefold | PG_FORMAT для ill-formed; разные нормальные формы остаются разными bytes |
| C03 | Duplicate keys проверять после unescaping keys, включая a и \u0061; не last-key-wins. Unknown/missing keys — schema checks отдельно | PG_FORMAT до digest |
| C04 | Object key sorting — lexicographic sequence Unicode scalar codepoints, не locale/UTF16/UTF8 byte collation; prefix shorter first. Array order preserved, не сортировать как set | Invalid scalar → PG_FORMAT |
| C05 | Token integer grammar -?(0\|[1-9][0-9]*), exact signed64. Bool не Int, float/exponent/NaN/Infinity reject даже если value математически целое. Canonical decimal minimal; token -0 → bytes0 предлагается отдельно OP-05 | Out of range/type/token PG_FORMAT |
| C06 | Canonical JSON без BOM, spaces/newline outside strings; true/false/null literals. Scalars allowed only in value-probe layer, не полноценный PG envelope | Envelope root не object → PG_FORMAT |
| C07 | Strings UTF8 в double quotes; quote как backslash+quote, backslash как два backslash. U+0008/000C/000A/000D/0009 как \b/\f/\n/\r/\t; остальные00…1F как lowercase \u00xx. Остальные scalar literal, slash не escape | Не допускается serializer-dependent escape alternative в canonical bytes |
| C08 | Null отличен от отсутствия поля. Только T\|null разрешает null; optional omission отсутствует в Record. Empty JSON string допустим C14N, но required Text непуст | PG_FORMAT по schema; конфликт product-gap см.X01 |
| C09 | Input whitespace/key order/escape spelling меняются без изменения parsed value → те же canonical bytes. Raw byte hash исходного файла при этом отличается | Не смешивать raw hash с PG binding |
| C10 | H=SHA256(UTF8("StoryStudio/PG-C14N-1") \|\| hex00 \|\| canonical(Envelope без собственного top-level binding_sha256)). Исключается только это одно поле, **не вложенные ObjectRef.binding_sha256**. Остальные contract/id/revision/mode/body целиком включены | binding_sha256 обязательно64 lowercasehex; malformed PG_FORMAT, mismatch PG_DIGEST |
| B01 | ByteRef.sha256=SHA256 реальных raw bytes без prefix, byte_length=len(bytes), media_type не меняет bytes и не позволяет сеть. URI/path не resolver | length/hash mismatch PG_DIGEST; unavailable content PG_REFERENCE либо provider unavailable по stage |
| E01 | Fixture E содержит full PG01 field-shape envelope, но synthetic raw contents не дают full semantic consistency; no authority verdict | Only canonical/field-shape evidence, not PG PASS |
| S01 | Envelope ровно contract,id,revision,mode,body,binding_sha256; все mandatory. Revision Int≥1; id lowercase UUID. Body закрытый Record для exact contract | Unknown/missing/type/null violation PG_FORMAT |
| S02 | Schema IDs ровно pg-01/proposal-1 … pg-05/proposal-1. Version alias/latest/proposal-99 не поддержан | PG_FORMAT, не новый PG_VERSION namespace |
| S03 | Text непустой scalar sequence; длина в UTF8 bytes; список пуст только если нет дополнительного invariant. Empty why_film conflict с discovery oracle остаётся X01 | BLOCKED_CONTRACT для спорного precedence |
| R01 | ObjectRef exact contract/id/revision/binding, target найден в supplied closure, locally hashed. No latest fallback | Missing/dangling/hash reference mismatch → proposed PG_REFERENCE |
| R02 | Один (contract,id,revision) не может разрешаться к разным bytes/digests; одинаковый exact object повторно не новый объект | PG_REFERENCE; registry conflict до semantic use |
| R03 | Проверять типы refs, predecessor scope и acyclic declared dependency graph; ByteRef opaque bytes — не автоматически semantic edge | Scope edges/closure/cycle staging требуют OP-08/09; см.X03 |
| L01 | Предлагается maximum decoded string65536 UTF8 bytes (keys и values), а не число codepoints/escaped input characters | >limit PG_FORMAT, APPROVAL_REQUIRED |
| L02 | Предлагается max nesting64; scalar depth0, root object/array depth1, вложенный container+1; scalar leaf не добавляет depth | >64 PG_FORMAT, APPROVAL_REQUIRED |
| L03 | Предлагается max list length10000 для каждого массива до allocation; field-specific minima/uniqueness дополнительно | >limit PG_FORMAT, APPROVAL_REQUIRED |
| L04 | Предлагается max **полного input Envelope bytes**, включая binding_sha256 и разрешённый внешний whitespace, 8388608. Equality allowed; +1 deny. Canonical no-binding bytes — другая длина | >limit PG_FORMAT до decode/hash, APPROVAL_REQUIRED |
| T01 | Предлагается Instant exact integer0…253402300799 UTC epoch seconds; не locale/timezone string. Timestamp test — только supplied-value domain | Out-of-domain PG_FORMAT, APPROVAL_REQUIRED |
| T02 | Предлагается [valid_from,valid_until), exclusive expiry; now==until expired. now из supplied offline context не trusted clock | PG_EXPIRED в predicate probe; operational clock qualification отсутствует |

Граница stage precedence: bounded decode → JSON grammar/duplicates/types/schema → local envelope digest → reference registry/closure → cross-object mode/subject/product consistency → trusted operational context → execution/evidence. Это proposed resolution, не silent patch discovery. Unknown keys/missing revision/bool revision не доходят до hash. Для mode/body empty contradictions X01/X02 не закрепляется единственный normative error до owner решения.

## Self-hash и nested bindings

В full input binding_sha256 присутствует и валидируется. Для hash preimage удаляется **top-level** поле по имени после successful duplicate/unknown-key проверки. Не удаляются остальные occurrence этого имени. Не вставлять zero hash в preimage; не hash-ить собственный digest как nested body bytes. ObjectRef связывает целый target envelope без его self-binding поля, не только target.body. Domain prefix hex `53746f727953747564696f2f50472d4331344e2d3100` фиксирован, последний00 обязателен.

SHA1 Git blob, G2 wire value hash/source SHA256 и SI canonical hash не взаимозаменяемы с PG. Разница source whitespace может не менять PG semantic value, но всегда отражается raw ByteRef bytes binding.

## Параметры и контекст

Все L01–04, T01–02, parser allocation/CPU/object-count limits и graph closure bound относятся к [реестру открытых параметров](G3_2_0A_OPEN_PARAMETERS_AND_OWNER_DECISIONS.md). Conditional vectors показывают результат **если** предложенный профиль выбран. Они не устанавливают approved production constants. Receipt schemas/identity/history providers не определяются canonical JSON и не подменяются строкой/подписью.

Нельзя утверждать CONSISTENT_NO_AUTHORITY для произвольного C14N scalar, schema-shaped envelope или неподтверждённого provider context. STRUCTURALLY_VALID — только описательный уровень отчёта; новый machine-readable status не вводится. Результаты pure PG из discovery: CONSISTENT_NO_AUTHORITY/DENY; operational authority отсутствует.
