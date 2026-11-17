# Независимые фиксированные векторы PG-C14N-1 / reference probes

**FREEZE_PROPOSAL — NOT APPROVED.** SI-INTEGRATION-G3.2.0a; 2026-11-17 (Europe/Kyiv).
Base `a28277b4cb68a3db5da52edc598c37ce66314604`, tree `920713b992046dff1f8fc68e40a05bee2f0bcb29`.
Pinned discovery `9551e490dbda11e372b11e758a2a0aafdb740ce1`, tree `dee2c06cc2274a26bb0dc8d3082fc31e16b81b3c`.
Только docs/offline vectors. Направление OD-PG-01–12 принято владельцем, но численные значения, роли, trust policies и operational protocols не утверждены. Нет validators/providers, permissions или qualification.

## Результат и границы независимости

**70 векторов:**23 POSITIVE /24 NEGATIVE /23 BOUNDARY (категории непересекающиеся). У33 есть literal canonical bytes и hashes;34 имеют определённое proposed DENY на своей изолированной стадии;3 контрактно заблокированы (V039, V043, V051). Negative expectations не выполнены PG validator: его нет и он не создавался.

Положительность относится к явно указанному layer: JSON/C14N, ByteRef/raw bytes или полному PG01 field-shape envelope. **Ни один positive не заявляет effective human approval, valid real SI payload или полный PG01–PG05 CONSISTENT verdict.** Minimal envelope E содержит все mandatory fields PG01, но использует синтетический `{}` raw объект и пустые semantic collections; он заведомо не successful full PG01 candidate. Полные positive consistency examples заблокированы unresolved contracts/providers; см.schema matrix. Это ограничение не скрывается за literal SHA.

Метод A: ожидаемые canonical strings/hex/повторения написаны явно из правил C01–C10; для E вручную собран порядок fields и fragments, без production serializer. Метод B: независимый контроль stdlib json.loads + json.dumps(ensure_ascii=False,sort_keys=True,separators=(',',':')) на этих конечных cases; для envelope удаляется только top-level binding_sha256. Python arbitrary precision сохраняет signed64 literal cases; non-BMP sorting и controls проверены отдельно. Ни G1/G2/SI/PG module не импортирован.

Для каждой позитивной последовательности SHA256 пересчитан CPython hashlib и внешним OpenSSL CLI;75 вызова cross-check включая fixture constants/repeated cases, это не число уникальных векторов. Оба hash methods получают уже известные bytes; это **не** независимые реализации canonicalization. Hashlib может использовать тот же libcrypto backend, что OpenSSL CLI; отдельная дополнительная сверка GNU sha256sum выполнена для всех33 literal canonical outputs, RAW и DOMAIN (66 streams). Backend independence не выводится только из разных имён команд. Независимость canonical bytes — manual literal/recipe против stdlib JSON control; она не заменяет третью независимую реализацию всех PG validators. Дополнительно все66 literal RAW/DOMAIN streams прочитаны из этого Markdown и совпали с самостоятельной временной реализацией FIPS180-4 SHA256 на Python integer/struct без вызова crypto libraries. Known-answer controls empty и abc совпали с известными literals. Это независимая реализация **hash computation**, не независимый reviewer и не PG validator. GNU sha256sum в этом executor тоже связан с libcrypto, поэтому отдельность его backend не заявляется. Negative exact error codes — review expectations, не результаты работающего PG.

## Byte language и fixture constants

`hexXX` — указанные bytes, `hex:...` — полная hex sequence. `||` concatenation; `X^n` exactly n copies; slices0-based half-open по **bytes**; ASCII/UTF8 encoding без newline/BOM. replace_once меняет первый exact byte substring, отсутствие substring — ошибка рецепта. All UUIDs ниже — synthetic fixture IDs, не identities/grants/credentials. В recipe text `I`, `H_ENV` означают уже объявленную ASCII строку, без кавычек; `BODY`, `E`, `REF` — bytes. `empty` — zero bytes. Нет внешних hidden files.

- I=`00000000-0000-4000-8000-000000000001`, B=`00000000-0000-4000-8000-000000000002`, P=`00000000-0000-4000-8000-000000000003`.
- Raw object O=hex7b7d (два bytes `{}`), byte_length=2, raw SHA256=`44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a`. Все ByteRef в E указывают на synthetic O; contents не являются real evaluation/license/plan.
- BODY = UTF8 следующей **одной строки**, без завершающего LF:

```json
{"asset_manifest":{"byte_length":2,"media_type":"application/json","object_id":"00000000-0000-4000-8000-000000000002","sha256":"44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"},"created_at":0,"editor_values_sha256":"44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a","editorial_constraints":[],"evaluation_derivation":"RECOMPUTED_FROM_EXACT_INPUTS","evaluation_inputs":{"byte_length":2,"media_type":"application/json","object_id":"00000000-0000-4000-8000-000000000002","sha256":"44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"},"evaluation_observation":{"context_head":{"epoch_id":"00000000-0000-4000-8000-000000000003","head_sha256":"44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a","sequence":0,"stream_id":"00000000-0000-4000-8000-000000000001"},"expected_context":{"byte_length":2,"media_type":"application/json","object_id":"00000000-0000-4000-8000-000000000002","sha256":"44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"},"observed_at":0,"observed_context":{"byte_length":2,"media_type":"application/json","object_id":"00000000-0000-4000-8000-000000000002","sha256":"44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"},"required_current_premise":null,"valid_until":1},"full_evaluation":{"byte_length":2,"media_type":"application/json","object_id":"00000000-0000-4000-8000-000000000002","sha256":"44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"},"linked_decisions":[],"policy":{"id":"00000000-0000-4000-8000-000000000003","sha256":"44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a","version":"fixture-only-not-approved"},"preview_export":[],"product_dossier":{"angle":"a","audience_need":"a","claim_links":[],"constraints":[],"novelty_basis":[],"required_visuals":[],"research_limits":["synthetic schema fixture"],"risks":[],"topic_question":"t","why_film":"w"},"projection_cards":[{"artifact":{"byte_length":2,"media_type":"application/json","object_id":"00000000-0000-4000-8000-000000000002","sha256":"44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"},"locale":"ru"},{"artifact":{"byte_length":2,"media_type":"application/json","object_id":"00000000-0000-4000-8000-000000000002","sha256":"44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"},"locale":"uk"}],"raw_editor_input":{"byte_length":2,"media_type":"application/json","object_id":"00000000-0000-4000-8000-000000000002","sha256":"44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"},"render_plan":{"byte_length":2,"media_type":"application/json","object_id":"00000000-0000-4000-8000-000000000002","sha256":"44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"},"source_identity":{"code_manifest":{"byte_length":2,"media_type":"application/json","object_id":"00000000-0000-4000-8000-000000000002","sha256":"44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a"},"commit_sha1":"a28277b4cb68a3db5da52edc598c37ce66314604","repository":"fixture-not-a-runtime-provider","tree_sha1":"920713b992046dff1f8fc68e40a05bee2f0bcb29"}}
```

C_ENV = ASCII('{"body":') || BODY || ASCII(',"contract":"pg-01/proposal-1","id":"'+I+'","mode":"PREVIEW_ONLY","revision":1}').

H_ENV=`31c0f3af39625dfab812bb6a4317539e9fd1700ac2ecf1d7f59b38beeaf0ca64` (literal domain digest). E=ASCII('{"binding_sha256":"'+H_ENV+'",') || C_ENV[1:].

REF = UTF8 следующей строки:

```json
{"binding_sha256":"31c0f3af39625dfab812bb6a4317539e9fd1700ac2ecf1d7f59b38beeaf0ca64","contract":"pg-01/proposal-1","id":"00000000-0000-4000-8000-000000000001","revision":1}
```

C_ENV2=replace_once(C_ENV,ASCII('"created_at":0'),ASCII('"created_at":1')); H_ENV2=`94ac3e10451c320a978d0f3c2e3368ae5e1fdb10559a081bf3fefae73fb054eb`; E2=ASCII('{"binding_sha256":"'+H_ENV2+'",') || C_ENV2[1:].

Для C14N value probes canonical hash RAW=SHA256(canonical bytes). DOMAIN=SHA256(prefix||canonical bytes) — арифметический domain-separation probe, **не valid PG ID для scalar**. Только E-like envelope DOMAIN есть PG binding. V066 RAW — именно ByteRef raw bytes digest, не envelope binding. При negative/boundary denial canonical bytes/hash **не вычисляется как accepted result**.

## Все векторы

### V001 — object key reordering

- Category/layer: POSITIVE; C14N value probe.
- Exact input: `hex:7b2262223a322c2261223a317d`; wire bytes=13.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `C01–C09`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `hex:7b2261223a312c2262223a327d`; length=13.
- Literal RAW SHA256: `43258cff783fe7036d8a43033f830adfc60ec037382473548ac742b888292777`.
- Literal DOMAIN SHA256: `6615dcd02e518a3f2e3a45425d99dbf047796db6054a5847d70c2dbda0b4e59c`.
- Rationale: isolates object key reordering; no expansion of scope or operational authority.

### V002 — whitespace

- Category/layer: POSITIVE; C14N value probe.
- Exact input: `hex:200a207b20226122203a2031207d2009`; wire bytes=16.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `C01–C09`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `hex:7b2261223a317d`; length=7.
- Literal RAW SHA256: `015abd7f5cc57a2dd94b7590f04ad8084273905ee33ec5cebeae62276a97f862`.
- Literal DOMAIN SHA256: `688372cacd7055dba457342ab006c45c7b8a0124725608c34e1f7a524c51e9ec`.
- Rationale: isolates whitespace; no expansion of scope or operational authority.

### V003 — Unicode literal

- Category/layer: POSITIVE; C14N value probe.
- Exact input: `hex:22d09fd180d0b8d0b2d196d18222`; wire bytes=14.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `C01–C09`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `hex:22d09fd180d0b8d0b2d196d18222`; length=14.
- Literal RAW SHA256: `7877aaaf3c877bdf2bc6f4617694c208edd79bf55438ca0627b9115b5229f4f3`.
- Literal DOMAIN SHA256: `8251907cc2e9730c64dac5150c71614c2fdd7a7c9f6db160622d21e12cfa9fcf`.
- Rationale: isolates Unicode literal; no expansion of scope or operational authority.

### V004 — Unicode escape equivalence

- Category/layer: POSITIVE; C14N value probe.
- Exact input: `hex:225c75303431665c75303434305c75303433385c75303433325c75303435365c753034343222`; wire bytes=38.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `C01–C09`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `hex:22d09fd180d0b8d0b2d196d18222`; length=14.
- Literal RAW SHA256: `7877aaaf3c877bdf2bc6f4617694c208edd79bf55438ca0627b9115b5229f4f3`.
- Literal DOMAIN SHA256: `8251907cc2e9730c64dac5150c71614c2fdd7a7c9f6db160622d21e12cfa9fcf`.
- Rationale: isolates Unicode escape equivalence; no expansion of scope or operational authority.

### V005 — quote/backslash escapes

- Category/layer: POSITIVE; C14N value probe.
- Exact input: `hex:22615c22625c5c6322`; wire bytes=9.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `C01–C09`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `hex:22615c22625c5c6322`; length=9.
- Literal RAW SHA256: `29e409e74462be098277d1428e52e22cd782e73a9f50b4f4f26e6527ab583eca`.
- Literal DOMAIN SHA256: `539d38df4ff2fa58f79f09aa87116104e1432822ad436464bf6e93741ae152bd`.
- Rationale: isolates quote/backslash escapes; no expansion of scope or operational authority.

### V006 — short controls

- Category/layer: POSITIVE; C14N value probe.
- Exact input: `hex:225c625c665c6e5c725c7422`; wire bytes=12.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `C01–C09`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `hex:225c625c665c6e5c725c7422`; length=12.
- Literal RAW SHA256: `88821412381596c0dc2c66e310ae7e66100d7e4196456e2e9f3d261d0b562746`.
- Literal DOMAIN SHA256: `9c39ad913cb59f46ea5532e119e3173a500d9944e24daa730682e05ecedc2a64`.
- Rationale: isolates short controls; no expansion of scope or operational authority.

### V007 — other control

- Category/layer: POSITIVE; C14N value probe.
- Exact input: `hex:225c753030303122`; wire bytes=8.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `C01–C09`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `hex:225c753030303122`; length=8.
- Literal RAW SHA256: `b81cfb0a6715e53b373345b49e8ad94eb55fd777519dc539373d0634973c186e`.
- Literal DOMAIN SHA256: `e023a3464b10799b4f2677189e4941d6b169a773c9b8207ec0c1aa2b8d59a137`.
- Rationale: isolates other control; no expansion of scope or operational authority.

### V008 — solidus unescaped

- Category/layer: POSITIVE; C14N value probe.
- Exact input: `hex:22615c2f6222`; wire bytes=6.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `C01–C09`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `hex:22612f6222`; length=5.
- Literal RAW SHA256: `f5effa31772a3689cb116700c569f4b72d765290968f099016a899ab6c1e4ee3`.
- Literal DOMAIN SHA256: `6667ccb8686ea046e8b1f8de37f8df9acfc55358167246a8f32beabf3c76f077`.
- Rationale: isolates solidus unescaped; no expansion of scope or operational authority.

### V009 — array order

- Category/layer: POSITIVE; C14N value probe.
- Exact input: `hex:5b322c315d`; wire bytes=5.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `C01–C09`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `hex:5b322c315d`; length=5.
- Literal RAW SHA256: `af1a1fc110b6094c48582b0ef83553cb7908d7a4365424eef28e76ef6c88d630`.
- Literal DOMAIN SHA256: `0dc26001dc9c59f1a54ace20c660dfa98f59cc68d92ad26ab35642661a30df8e`.
- Rationale: isolates array order; no expansion of scope or operational authority.

### V010 — different array order

- Category/layer: POSITIVE; C14N value probe.
- Exact input: `hex:5b312c325d`; wire bytes=5.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `C01–C09`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `hex:5b312c325d`; length=5.
- Literal RAW SHA256: `49a64717d5d4cb19952e6eac2946415cf6879adacf9908e7d872332d32c6e684`.
- Literal DOMAIN SHA256: `98381ccd403fc95a28a1537117c6ceca4df48b6ba5e5aec67a07ccec6efcb0a7`.
- Rationale: isolates different array order; no expansion of scope or operational authority.

### V011 — non-BMP key sorting

- Category/layer: POSITIVE; C14N value probe.
- Exact input: `hex:7b22f0908080223a312c22ee8080223a307d`; wire bytes=18.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `C01–C09`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `hex:7b22ee8080223a302c22f0908080223a317d`; length=18.
- Literal RAW SHA256: `8ca131a1542d92ce519ffcd40f16db95f486ac4d19c1de293b537f77b612429d`.
- Literal DOMAIN SHA256: `7a3a756c18102b7c0563eecbf03a889ca6ede5c43c89fdbc4841a401989fdab6`.
- Rationale: isolates non-BMP key sorting; no expansion of scope or operational authority.

### V012 — composed Unicode

- Category/layer: POSITIVE; C14N value probe.
- Exact input: `hex:22c3a922`; wire bytes=4.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `C01–C09`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `hex:22c3a922`; length=4.
- Literal RAW SHA256: `f2886017e9c7abacf804b54d64787dce2b611c9544ba21f3affdd126a6e50086`.
- Literal DOMAIN SHA256: `5f4ba0a80c794b02ef50ec8dbd8afbece9a6ec028b5eaae67625b70dc0272b08`.
- Rationale: isolates composed Unicode; no expansion of scope or operational authority.

### V013 — decomposed Unicode

- Category/layer: POSITIVE; C14N value probe.
- Exact input: `hex:2265cc8122`; wire bytes=5.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `C01–C09`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `hex:2265cc8122`; length=5.
- Literal RAW SHA256: `3d68ce21f2899a475713cdbe7562ba9bdb6b1dfde8af1f221bdff4a0935b53b2`.
- Literal DOMAIN SHA256: `fee3a85f01dda4b6e0f549db9d41eaa81134ef9da4725c9a3d738d775e1583b7`.
- Rationale: isolates decomposed Unicode; no expansion of scope or operational authority.

### V014 — null value

- Category/layer: POSITIVE; C14N value probe.
- Exact input: `hex:6e756c6c`; wire bytes=4.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `C01–C09`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `hex:6e756c6c`; length=4.
- Literal RAW SHA256: `74234e98afe7498fb5daf1f36ac2d78acc339464f950703b8c019892f982b90b`.
- Literal DOMAIN SHA256: `bfca3a01e7ce723c0625c9caffc6a428cfdfb8c6368c63600e99971955ae9ee7`.
- Rationale: isolates null value; no expansion of scope or operational authority.

### V015 — boolean value

- Category/layer: POSITIVE; C14N value probe.
- Exact input: `hex:74727565`; wire bytes=4.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `C01–C09`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `hex:74727565`; length=4.
- Literal RAW SHA256: `b5bea41b6c623f7c09f1bf24dcae58ebab3c0cdd90ad966bc43a45b44867e12b`.
- Literal DOMAIN SHA256: `41411335d16dbbd6d4fea0e0f7ec834838c47c5e0ef595618885a178662915d7`.
- Rationale: isolates boolean value; no expansion of scope or operational authority.

### V016 — negative integer

- Category/layer: POSITIVE; C14N value probe.
- Exact input: `hex:2d3432`; wire bytes=3.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `C01–C09`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `hex:2d3432`; length=3.
- Literal RAW SHA256: `fec80006df0542549b4cbaafb8987eee00bb49bca396eefe9ac8be5b5928e8f6`.
- Literal DOMAIN SHA256: `696293321605cc12598bfc09f7171621e90096748c829d8331d7babd04675228`.
- Rationale: isolates negative integer; no expansion of scope or operational authority.

### V017 — negative zero

- Category/layer: POSITIVE; C14N value probe.
- Exact input: `hex:2d30`; wire bytes=2.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `C01–C09`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `hex:30`; length=1.
- Literal RAW SHA256: `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9`.
- Literal DOMAIN SHA256: `bb73b0a9ea7841431b16caa5efe39a17af87b7632f9964c1b733b6516e47923f`.
- Rationale: isolates negative zero; no expansion of scope or operational authority.

### V018 — raw ByteRef shape

- Category/layer: POSITIVE; C14N value probe.
- Exact input: `hex:7b22627974655f6c656e677468223a322c226d656469615f74797065223a226170706c69636174696f6e2f6a736f6e222c226f626a6563745f6964223a2230303030303030302d303030302d343030302d383030302d303030303030303030303032222c22736861323536223a2234343133366661333535623336373861313134366164313666376538363439653934666234666332316665373765383331306330363066363163616166663861227d`; wire bytes=176.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `C01–C09`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `hex:7b22627974655f6c656e677468223a322c226d656469615f74797065223a226170706c69636174696f6e2f6a736f6e222c226f626a6563745f6964223a2230303030303030302d303030302d343030302d383030302d303030303030303030303032222c22736861323536223a2234343133366661333535623336373861313134366164313666376538363439653934666234666332316665373765383331306330363066363163616166663861227d`; length=176.
- Literal RAW SHA256: `72da07b141b591f76ace981de3d3d04b48e9b8af9f60450ad8a3e61a8ac33ed4`.
- Literal DOMAIN SHA256: `150ce87057a7aaea2120dd84d5cd80cba337348a8c6233cf3c8592dee90ca1ef`.
- Rationale: isolates raw ByteRef shape; no expansion of scope or operational authority.

### V019 — complete field-shape envelope

- Category/layer: POSITIVE; complete PG01 field-shape/C14N envelope; NOT full semantic consistency.
- Exact input: `E`; wire bytes=3290.
- Expected result: canonical bytes verified; PG01 semantic candidacy denied (empty SI/plan fixture); full verdict BLOCKED_CONTRACT; exact error: `not a positive full PG01 verdict`.
- Rule: `C10/E01`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `C_ENV`; length=3206.
- Literal RAW SHA256: `35383fc2952dde8f386f7653eae6793aa43c443c59048d574ec276006e4cdd0c`.
- Literal DOMAIN SHA256: `31c0f3af39625dfab812bb6a4317539e9fd1700ac2ecf1d7f59b38beeaf0ca64`.
- Rationale: isolates complete field-shape envelope; no expansion of scope or operational authority.

### V020 — reordered envelope

- Category/layer: POSITIVE; complete PG01 field-shape/C14N envelope; NOT full semantic consistency.
- Exact input: `ASCII('{"revision":1,"mode":"PREVIEW_ONLY","id":"'+I+'","contract":"pg-01/proposal-1","body":') || BODY || ASCII(',"binding_sha256":"'+H_ENV+'"}')`; wire bytes=3290.
- Expected result: canonical bytes verified; PG01 semantic candidacy denied (empty SI/plan fixture); full verdict BLOCKED_CONTRACT; exact error: `not a positive full PG01 verdict`.
- Rule: `C10/E01`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `C_ENV`; length=3206.
- Literal RAW SHA256: `35383fc2952dde8f386f7653eae6793aa43c443c59048d574ec276006e4cdd0c`.
- Literal DOMAIN SHA256: `31c0f3af39625dfab812bb6a4317539e9fd1700ac2ecf1d7f59b38beeaf0ca64`.
- Rationale: isolates reordered envelope; no expansion of scope or operational authority.

### V021 — whitespace envelope

- Category/layer: POSITIVE; complete PG01 field-shape/C14N envelope; NOT full semantic consistency.
- Exact input: `hex(200a) || E || hex(2009)`; wire bytes=3294.
- Expected result: canonical bytes verified; PG01 semantic candidacy denied (empty SI/plan fixture); full verdict BLOCKED_CONTRACT; exact error: `not a positive full PG01 verdict`.
- Rule: `C10/E01`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `C_ENV`; length=3206.
- Literal RAW SHA256: `35383fc2952dde8f386f7653eae6793aa43c443c59048d574ec276006e4cdd0c`.
- Literal DOMAIN SHA256: `31c0f3af39625dfab812bb6a4317539e9fd1700ac2ecf1d7f59b38beeaf0ca64`.
- Rationale: isolates whitespace envelope; no expansion of scope or operational authority.

### V022 — nested PG ObjectRef; target is E

- Category/layer: POSITIVE; nested reference encoding only; context target=E, not a full PG02 body.
- Exact input: `ASCII('{"subject":{"snapshot":') || REF || ASCII('}}')`; wire bytes=197.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `R01/C10`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `ASCII('{"subject":{"snapshot":') || REF || ASCII('}}')`; length=197.
- Literal RAW SHA256: `769c294c91958abbac6c783bcdafc6e649881ddfd2debe24d71a7ceab0bde0bf`.
- Literal DOMAIN SHA256: `1a6b61a2ecef0f63e902a98cd0aac682d4282dc3bdf6a50dd9024e86a49f75bd`.
- Rationale: isolates nested PG ObjectRef; target is E; no expansion of scope or operational authority.

### V023 — duplicate key

- Category/layer: NEGATIVE; none.
- Exact input: `hex:7b2261223a312c2261223a327d`; wire bytes=13.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `C03`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates duplicate key; no expansion of scope or operational authority.

### V024 — escaped duplicate key

- Category/layer: NEGATIVE; none.
- Exact input: `hex:7b2261223a312c225c7530303631223a327d`; wire bytes=18.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `C03`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates escaped duplicate key; no expansion of scope or operational authority.

### V025 — invalid UTF8

- Category/layer: NEGATIVE; none.
- Exact input: `hex:22ff22`; wire bytes=3.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `C01`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates invalid UTF8; no expansion of scope or operational authority.

### V026 — UTF8 BOM

- Category/layer: NEGATIVE; none.
- Exact input: `hex(efbbbf) || E`; wire bytes=3293.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `C01`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates UTF8 BOM; no expansion of scope or operational authority.

### V027 — lone high surrogate

- Category/layer: NEGATIVE; none.
- Exact input: `hex:225c756438303022`; wire bytes=8.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `C02`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates lone high surrogate; no expansion of scope or operational authority.

### V028 — lone low surrogate

- Category/layer: NEGATIVE; none.
- Exact input: `hex:225c756466666622`; wire bytes=8.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `C02`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates lone low surrogate; no expansion of scope or operational authority.

### V029 — float

- Category/layer: NEGATIVE; none.
- Exact input: `hex:312e30`; wire bytes=3.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `C05`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates float; no expansion of scope or operational authority.

### V030 — exponent

- Category/layer: NEGATIVE; none.
- Exact input: `hex:316530`; wire bytes=3.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `C05`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates exponent; no expansion of scope or operational authority.

### V031 — NaN

- Category/layer: NEGATIVE; none.
- Exact input: `hex:4e614e`; wire bytes=3.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `C05`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates NaN; no expansion of scope or operational authority.

### V032 — Infinity

- Category/layer: NEGATIVE; none.
- Exact input: `hex:496e66696e697479`; wire bytes=8.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `C05`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates Infinity; no expansion of scope or operational authority.

### V033 — bool revision

- Category/layer: NEGATIVE; none.
- Exact input: `replace_once(E,ASCII('"revision":1'),ASCII('"revision":true'))`; wire bytes=3293.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `S01`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates bool revision; no expansion of scope or operational authority.

### V034 — unknown envelope key

- Category/layer: NEGATIVE; none.
- Exact input: `E[0:-1] || ASCII(',"extra":0}')`; wire bytes=3300.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `S01`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates unknown envelope key; no expansion of scope or operational authority.

### V035 — missing revision

- Category/layer: NEGATIVE; none.
- Exact input: `replace_once(E,ASCII(',"revision":1'),empty)`; wire bytes=3277.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `S01`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates missing revision; no expansion of scope or operational authority.

### V036 — null revision

- Category/layer: NEGATIVE; none.
- Exact input: `replace_once(E,ASCII('"revision":1'),ASCII('"revision":null'))`; wire bytes=3293.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `S01`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates null revision; no expansion of scope or operational authority.

### V037 — wrong binding 64 hex

- Category/layer: NEGATIVE; none.
- Exact input: `replace_once(E,ASCII(H_ENV),ASCII('8736f9541f8b25691fee0cffb16f2dea2fd1043fb6ebcabf3f3d752d7ca9169c'))`; wire bytes=3290.
- Expected result: DENY; exact error: `PG_DIGEST`.
- Rule: `C10`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates wrong binding 64 hex; no expansion of scope or operational authority.

### V038 — unknown contract version

- Category/layer: NEGATIVE; none.
- Exact input: `replace_once(E,ASCII('pg-01/proposal-1'),ASCII('pg-01/proposal-99'))`; wire bytes=3291.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `S02`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates unknown contract version; no expansion of scope or operational authority.

### V039 — known wrong mode with stale binding

- Category/layer: NEGATIVE; none.
- Exact input: `replace_once(E,ASCII('PREVIEW_ONLY'),ASCII('PRODUCTION_CANDIDATE'))`; wire bytes=3298.
- Expected result: BLOCKED_CONTRACT; no unique normative verdict; exact error: `BLOCKED_CONTRACT`.
- Rule: `X02`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates known wrong mode with stale binding; no expansion of scope or operational authority.

### V040 — changed revision, old binding

- Category/layer: NEGATIVE; none.
- Exact input: `replace_once(E,ASCII('"revision":1'),ASCII('"revision":2'))`; wire bytes=3290.
- Expected result: DENY; exact error: `PG_DIGEST`.
- Rule: `C10`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates changed revision, old binding; no expansion of scope or operational authority.

### V041 — dangling PG ref

- Category/layer: NEGATIVE; offline reference-resolution probe; objects=[]; ref bytes only, not whole PG envelope.
- Exact input: `REF; context objects=[]`; wire bytes=172.
- Expected result: DENY; exact error: `PG_REFERENCE`.
- Rule: `R01`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates dangling PG ref; no expansion of scope or operational authority.

### V042 — conflicting id/revision

- Category/layer: NEGATIVE; reference probe; objects=[E,E2]; E2 defined in fixture constants; both local digests valid, same id/revision, distinct bytes.
- Exact input: `REF; context objects=[E,E2]`; wire bytes=172.
- Expected result: DENY; exact error: `PG_REFERENCE`.
- Rule: `R02`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates conflicting id/revision; no expansion of scope or operational authority.

### V043 — isolated content-addressed cyclic closure

- Category/layer: NEGATIVE; cannot supply mutually valid literal digest cycle without changing reference semantics; objects=[E]; this actual input is acyclic; no fake cycle PASS claimed.
- Exact input: `REF; context objects=[E]; isolated cyclic fixture unavailable — BLOCKED_CONTRACT, not genuine cycle bytes`; wire bytes=172.
- Expected result: BLOCKED_CONTRACT; no unique normative verdict; exact error: `BLOCKED_CONTRACT`.
- Rule: `X03`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates isolated content-addressed cyclic closure; no expansion of scope or operational authority.

### V044 — unescaped control

- Category/layer: NEGATIVE; none.
- Exact input: `hex:2261016222`; wire bytes=5.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `C02`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates unescaped control; no expansion of scope or operational authority.

### V045 — trailing second JSON value

- Category/layer: NEGATIVE; none.
- Exact input: `hex:302031`; wire bytes=3.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `C01`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates trailing second JSON value; no expansion of scope or operational authority.

### V046 — signed64 minimum

- Category/layer: BOUNDARY; C14N value probe.
- Exact input: `hex:2d39323233333732303336383534373735383038`; wire bytes=20.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `C05`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `hex:2d39323233333732303336383534373735383038`; length=20.
- Literal RAW SHA256: `85386477f3af47e4a0b308ee3b3a688df16e8b2228105dd7d4dcd42a9807cb78`.
- Literal DOMAIN SHA256: `94f45382ca88b583af089134b014e7b7e7df579bf1f734994f321554bf3ae979`.
- Rationale: isolates signed64 minimum; no expansion of scope or operational authority.

### V047 — signed64 maximum

- Category/layer: BOUNDARY; C14N value probe.
- Exact input: `hex:39323233333732303336383534373735383037`; wire bytes=19.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `C05`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `hex:39323233333732303336383534373735383037`; length=19.
- Literal RAW SHA256: `b34a1c30a715f6bf8b7243afa7fab883ce3612b7231716bdcbbdc1982e1aed29`.
- Literal DOMAIN SHA256: `5d165c04ccb44aa2088037927e635df426e72a9c4609fe96624ce109cad62caf`.
- Rationale: isolates signed64 maximum; no expansion of scope or operational authority.

### V048 — signed64 underflow

- Category/layer: BOUNDARY; none.
- Exact input: `hex:2d39323233333732303336383534373735383039`; wire bytes=20.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `C05`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates signed64 underflow; no expansion of scope or operational authority.

### V049 — signed64 overflow

- Category/layer: BOUNDARY; none.
- Exact input: `hex:39323233333732303336383534373735383038`; wire bytes=19.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `C05`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates signed64 overflow; no expansion of scope or operational authority.

### V050 — empty JSON string

- Category/layer: BOUNDARY; C14N allows empty JSON string; NOT required Text field.
- Exact input: `hex:2222`; wire bytes=2.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `C02/S03`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `hex:2222`; length=2.
- Literal RAW SHA256: `12ae32cb1ec02d01eda3581b127c1fee3b0dc53572ed6baf239721a03d82e126`.
- Literal DOMAIN SHA256: `e97cd06a89c3189568b0ea1b1a56b4a3642353460109b5e23d7c7922d3f06f4b`.
- Rationale: isolates empty JSON string; no expansion of scope or operational authority.

### V051 — empty required why_film

- Category/layer: BOUNDARY; none.
- Exact input: `replace_once(E,ASCII('"why_film":"w"'),ASCII('"why_film":""'))`; wire bytes=3289.
- Expected result: BLOCKED_CONTRACT; no unique normative verdict; exact error: `BLOCKED_CONTRACT`.
- Rule: `X01`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates empty required why_film; no expansion of scope or operational authority.

### V052 — max string bytes

- Category/layer: BOUNDARY; C14N value probe.
- Exact input: `hex22 || hex(c3a9)^32768 || hex22`; wire bytes=65538.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `L01`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `hex22 || hex(c3a9)^32768 || hex22`; length=65538.
- Literal RAW SHA256: `d09441e80b8acb08622e939d93e7fa431e85f70580dac9000aabb7bf18155d45`.
- Literal DOMAIN SHA256: `821cd4809b02e5312821b8c46d60b0ccb704afe22439245ae2c4e0a9d86f94c4`.
- Rationale: isolates max string bytes; no expansion of scope or operational authority.

### V053 — max string+1 UTF8 byte

- Category/layer: BOUNDARY; none.
- Exact input: `hex22 || hex(c3a9)^32768 || hex78 || hex22`; wire bytes=65539.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `L01`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates max string+1 UTF8 byte; no expansion of scope or operational authority.

### V054 — max depth64

- Category/layer: BOUNDARY; C14N value probe.
- Exact input: `hex5b^64 || hex30 || hex5d^64`; wire bytes=129.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `L02`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `hex5b^64 || hex30 || hex5d^64`; length=129.
- Literal RAW SHA256: `f0244ae1938270f711155b0a26a4307cde7050495140dd858a88a1cfc378cf40`.
- Literal DOMAIN SHA256: `420a8c71871350da9349071440665be21e86bd662aeec9878c611cb34f88745a`.
- Rationale: isolates max depth64; no expansion of scope or operational authority.

### V055 — depth65

- Category/layer: BOUNDARY; none.
- Exact input: `hex5b^65 || hex30 || hex5d^65`; wire bytes=131.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `L02`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates depth65; no expansion of scope or operational authority.

### V056 — list10000

- Category/layer: BOUNDARY; C14N value probe.
- Exact input: `hex5b || hex30 || (hex2c30)^9999 || hex5d`; wire bytes=20001.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `L03`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `hex5b || hex30 || (hex2c30)^9999 || hex5d`; length=20001.
- Literal RAW SHA256: `7ea81ee0dbbdd45f4ab8993e8f4cf3f0692f71ae74ffdd28518cc1a0a769bb70`.
- Literal DOMAIN SHA256: `c7602fb5151cb8edd07498c550cc0c44e548f0553d453dbaf989e612bc5a103f`.
- Rationale: isolates list10000; no expansion of scope or operational authority.

### V057 — list10001

- Category/layer: BOUNDARY; none.
- Exact input: `hex5b || hex30 || (hex2c30)^10000 || hex5d`; wire bytes=20003.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `L03`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates list10001; no expansion of scope or operational authority.

### V058 — wire envelope exactly8MiB

- Category/layer: BOUNDARY; complete PG01 field-shape/C14N envelope; NOT full semantic consistency.
- Exact input: `E || hex20^(8388608-len(E))`; wire bytes=8388608.
- Expected result: canonical bytes verified; PG01 semantic candidacy denied (empty SI/plan fixture); full verdict BLOCKED_CONTRACT; exact error: `not a positive full PG01 verdict`.
- Rule: `L04/C10`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `C_ENV`; length=3206.
- Literal RAW SHA256: `35383fc2952dde8f386f7653eae6793aa43c443c59048d574ec276006e4cdd0c`.
- Literal DOMAIN SHA256: `31c0f3af39625dfab812bb6a4317539e9fd1700ac2ecf1d7f59b38beeaf0ca64`.
- Rationale: isolates wire envelope exactly8MiB; no expansion of scope or operational authority.

### V059 — wire envelope8MiB+1

- Category/layer: BOUNDARY; none.
- Exact input: `E || hex20^(8388609-len(E))`; wire bytes=8388609.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `L04`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates wire envelope8MiB+1; no expansion of scope or operational authority.

### V060 — timestamp minimum

- Category/layer: BOUNDARY; Instant scalar probe, no clock authenticity.
- Exact input: `hex:30`; wire bytes=1.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `T01`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `hex:30`; length=1.
- Literal RAW SHA256: `5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9`.
- Literal DOMAIN SHA256: `bb73b0a9ea7841431b16caa5efe39a17af87b7632f9964c1b733b6516e47923f`.
- Rationale: isolates timestamp minimum; no expansion of scope or operational authority.

### V061 — timestamp maximum

- Category/layer: BOUNDARY; Instant scalar probe, no clock authenticity.
- Exact input: `hex:323533343032333030373939`; wire bytes=12.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `T01`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `hex:323533343032333030373939`; length=12.
- Literal RAW SHA256: `a70d72e35ddca699c6685e38e1056ce6fff54127e022abc85e9edbefde342ca9`.
- Literal DOMAIN SHA256: `c382d7fa70bad699c8b4551e963ae6fe6e67a2408494ae7df7c9b3a20826501a`.
- Rationale: isolates timestamp maximum; no expansion of scope or operational authority.

### V062 — timestamp maximum+1

- Category/layer: BOUNDARY; Instant field probe; integer itself is valid signed64.
- Exact input: `hex:323533343032333030383030`; wire bytes=12.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `T01`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates timestamp maximum+1; no expansion of scope or operational authority.

### V063 — exclusive expiry now==until

- Category/layer: BOUNDARY; pure supplied-time predicate only; not trusted clock proof.
- Exact input: `hex:7b226e6f77223a31302c2276616c69645f66726f6d223a302c2276616c69645f756e74696c223a31307d`; wire bytes=42.
- Expected result: DENY; exact error: `PG_EXPIRED`.
- Rule: `T02`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates exclusive expiry now==until; no expansion of scope or operational authority.

### V064 — hash63 hex

- Category/layer: BOUNDARY; none.
- Exact input: `replace_once(E,ASCII(H_ENV),ASCII(H_ENV[0:63]))`; wire bytes=3289.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `C10`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates hash63 hex; no expansion of scope or operational authority.

### V065 — hash65 hex

- Category/layer: BOUNDARY; none.
- Exact input: `replace_once(E,ASCII(H_ENV),ASCII(H_ENV+'a'))`; wire bytes=3291.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `C10`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates hash65 hex; no expansion of scope or operational authority.

### V066 — raw ByteRef bytes exactly {}

- Category/layer: BOUNDARY; raw payload bytes SHA256=44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a; byte_length=2; not a PG envelope binding.
- Exact input: `hex:7b7d`; wire bytes=2.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `B01`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `hex:7b7d`; length=2.
- Literal RAW SHA256: `44136fa355b3678a1146ad16f7e8649e94fb4fc21fe77e8310c060f61caaff8a`.
- Literal DOMAIN SHA256: `e37e18794da0f5ccbc97eb4d4506e6bcf80f006cb8342aa9add163fd37d88e22`.
- Rationale: isolates raw ByteRef bytes exactly {}; no expansion of scope or operational authority.

### V067 — valid escaped surrogate pair

- Category/layer: POSITIVE; C14N value probe.
- Exact input: `hex:225c75643833645c756465303022`; wire bytes=14.
- Expected result: canonical bytes verified; no PG authority verdict; exact error: `NONE at this layer`.
- Rule: `C02`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `hex:22f09f988022`; length=6.
- Literal RAW SHA256: `7a0c50b92434b015545fe93ab723db2d4b2cdd14a441405624a9ce8be29f1d5a`.
- Literal DOMAIN SHA256: `b39e0a2b71bf4499567a0e5ccaf0259092ed3c8e604510d39cd8aa99388e8b7f`.
- Rationale: isolates valid escaped surrogate pair; no expansion of scope or operational authority.

### V068 — uppercase64 hash

- Category/layer: BOUNDARY; none.
- Exact input: `replace_once(E,ASCII(H_ENV),ASCII(uppercase(H_ENV)))`; wire bytes=3290.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `C10`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates uppercase64 hash; no expansion of scope or operational authority.

### V069 — negative timestamp

- Category/layer: BOUNDARY; Instant field probe; signed integer value otherwise valid.
- Exact input: `hex:2d31`; wire bytes=2.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `T01`; **APPROVAL_REQUIRED**.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates negative timestamp; no expansion of scope or operational authority.

### V070 — unknown body key

- Category/layer: NEGATIVE; none.
- Exact input: `replace_once(E,BODY,BODY[0:-1] || ASCII(',"extra":0}'))`; wire bytes=3300.
- Expected result: DENY; exact error: `PG_FORMAT`.
- Rule: `S01`; no additional numerical profile assumption; whole contract remains NOT APPROVED.
- Expected canonical bytes: `N/A — no accepted canonical output`.
- Rationale: isolates unknown body key; no expansion of scope or operational authority.

## Заблокированные случаи и owner review

V039: discovery одновременно задаёт mode subset как schema requirement и отдельный PG_MODE semantic error; stale binding создаёт дополнительный PG_DIGEST. Unique precedence до OP-06/X02 не утверждён. V051: Text nonempty → PG_FORMAT, но P01-07 обещает PG_PRODUCT_GAP; нельзя выбрать нормативный ответ без explicit resolution X01. V043: все content-addressed PG links содержат digest самого target; genuine mutually bound cycle с valid digests нельзя честно создать обычной подстановкой нулей. Фактический REF→E input здесь acyclic и **не считается циклическим rejection test**. Изолированный cycle fixture/test model остаётся BLOCKED_CONTRACT X03/OP-08. V041/V042 проверяют только declared reference registry layer с явным offline context, не authenticity.

Никакие BLOCKED cases не записаны как PASS. Параметрические max-size/depth/Instant/expiry probes — conditional APPROVAL_REQUIRED. Необходима независимая проверка ChatGPT literal bytes/hashes и explicit owner выбор unresolved правил. Все временные byte files/scripts вне репозитория, в commit входят только семь Markdown.
