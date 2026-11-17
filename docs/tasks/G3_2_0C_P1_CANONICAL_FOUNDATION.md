# P1 — Canonical Foundation: decision-ready proposal

**DECISION_PROPOSAL — NOT APPROVED.** SI-INTEGRATION-G3.2.0c; 2026-11-17 (Europe/Kyiv).
Accepted docs base `0d6d9076ab535c1b258206beb4e4fe9c005e79e1`, tree `e55c00d0e7a95218e0978dd9677172608395ff5f`.

Primary OP-01/02/03/04/05/06/26/27: восемь PURE decision questions. Source rules и exact owner questions находятся в [главном dossier](G3_2_0C_OPEN_PARAMETERS_DECISION_DOSSIER.md). Ниже наиболее подробный пакет для review; **не утверждённый canonical contract и не implementation**. X01/X02 уже OWNER_APPROVED и не переоткрываются. P1 можно рассмотреть без подключения provider, real clock, render или Windows host; operational свойства из одобрения P1 не следуют.

## 1. OP-01 — inclusive wire-input cap

Recommendation: **8MiB = 8,388,608 bytes**, inclusive limit полного wire Envelope до UTF-8 decode. Считаются initial/trailing JSON whitespace и top-level binding_sha256. Canonical no-binding preimage учитывается отдельно; cap нельзя незаметно измерить после whitespace stripping/canonicalization. Все числа — PROPOSED, не safe memory guarantee.

| Вариант | Exact bytes | Security consequence | Product consequence | Recommendation |
|---|---:|---|---|---|
| 4MiB | 4,194,304 | Раньше ограничивает IO/буфер, но не доказывает RAM/CPU bound | Больше rejection больших dossiers; reference-only excerpts чаще | Conservative profile option |
| 8MiB | 8,388,608 | Ограниченный root stream, разумная стартовая совместимость с pinned conditional vectors | Текстовые dossiers допустимы в bounded scope, media не inline | Starting proposal |
| 16MiB | 16,777,216 | Удваивает root IO ceiling, требует отдельного resource profile | Больше больших manifests; не разрешает безлимитные dependencies | Large profile alternative |

### Accounting and exact boundary

- W — **реально полученные bytes**, не Content-Length и не Python character count. W=limit allowed лишь на этом guard; W=limit+1 denies PG_FORMAT на stage1. Это не гарантия, что позже schema/budget/ref/product checks пройдут.
- BOM в начале disallowed, even if otherwise small; UTF-8 строго проверяется, malformed/overlong/surrogate encodings не принимаются. U+FEFF **внутри корректной string** — обычный scalar, не initial BOM; не удалять его normalization.
- Space/TAB/LF/CR вокруг JSON value считаются wire bytes; допустимость whitespace не исключает их из cap. Второй JSON value после первого — grammar failure. Никакого permissive parser fallback.
- Streaming: поддерживать счётчик до увеличения aggregate buffer. Читать bounded chunks, остановиться не позже sentinel limit+1; нельзя сначала allocate advertised/unbounded document и затем проверить размер. **Не обещать zero allocation:** decoder/chunk buffers неизбежны и входят в OP-07. Chunk size/reader implementation и enforcement actual heap remain OPEN.
- Доверять только фактическому EOF/ограниченному stream. Prefix oversized файла не является whole-file hash. Size metadata/header — early hint, не доказательство.
- ByteRef descriptor входит в root W; actual referenced bytes считаются отдельным aggregate budget P3 и проверяются как raw bytes. Descriptor не позволяет загрузить URL/путь или заменить whole material hash частичным.
- Canonical output C и hash preimage length C+domain-prefix не должны повторно сравниваться с wire cap как будто это та же величина. Если full Envelope ровно8MiB за счёт trailing whitespace, compact canonical preimage намного меньше, но stage1 equality остаётся допустима.

Pinned V058/V059 — conditional8MiB probes; P3 другие profiles не меняют их исходные expected literals. Для4/16MiB нужны future separately approved boundary fixtures, здесь они не создаются. No parser benchmark/application test executed.

## 2. OP-02 — nesting without off-by-one ambiguity

Recommendation: depth64; scalar alone0, root object/array1, переход к nested **container** +1. Scalar leaf не добавляет container depth. Examples как детерминированные descriptions, не новые vector IDs:

| Shape | Container depth | Notes |
|---|---:|---|
| `0`, `"x"`, `null` | 0 | C14N probes only; PG root всё равно object |
| `[]`, `{}` | 1 | Empty container counts |
| `[0]`, `{"a":0}` | 1 | Scalar leaves do not increment |
| `[[]]`, `{"a":{}}`, `{"a":[]}` | 2 | Object/array equivalence |
| 64 nested arrays around scalar | 64 | V054 conditional bound |
| 65 nested arrays around scalar | 65 | V055 conditional rejection |

Depth check before pushing another parse/container frame; iterative parser/work queue предпочтительнее reliance на language recursion limit, но implementation здесь отсутствует. JSON depth ≠ reference-closure path depth; отдельный document root сбрасывает JSON container counter, а global P3 budgets продолжают считаться. Protected store depth не доказывается таким счётчиком.

Alternatives32 conservative/96 separately reviewed upper profile. Rejection глубоких легитимных деревьев — явный tradeoff, не повод silently flatten/mutate content. Owner question: утвердить64/counting semantics без утверждения native stack или всей resource модели?

## 3. OP-03 — decoded string bytes

Recommendation: max65,536 **UTF-8 bytes decoded scalar sequence**, отдельно для каждого object key и string value. На source wire escape spellings не применять decoded limit как raw character count; W всё равно ограничен OP-01. Keys и values одинаково ограничены до добавления unbounded decoded material.

| Sequence / representation | Decoded UTF8 bytes | Wire observation |
|---|---:|---|
| ASCII scalar `a` | 1 | Literal1 byte внутри quotes |
| `é` U+00E9 | 2 | Literal2 bytes либо six-byte JSON escape; normalization не проводится |
| `e` + U+0301 | 3 | Не эквивалентно composed bytes для hash |
| `😀` U+1F600 | 4 | Literal4 либо paired escapes12 внутри quotes |
| Escaped U+0001 | 1 | Six ASCII escape bytes, canonical control escaping отдельное правило |
| 32,768 copies U+00E9 | 65,536 | V052: exactly decoded boundary, quotes не часть decoded string |
| Те же copies + ASCII x | 65,537 | V053: boundary+1 |

Worst-case raw escape expansion для65,536 однобайтовых decoded controls:6×65,536+2=393,218 wire bytes включая quotes. Это арифметика encoding, не benchmark и не bound peak memory. Strict unescaping/scalar validation предшествует length acceptance; surrogate pair combined, lone surrogate reject. Duplicate keys сравниваются **после unescape**; `a`/escaped-a duplicate, composed/decomposed keys остаются разными. No trim/casefold/NFC/NFD.

Alternatives32KiB/128KiB as named profiles. Длинные цитаты/лицензии могут требовать ByteRef вместо inline, но descriptor не подтверждает права. Root decoded bytes globally ограничиваются OP-07 отдельно. X01: empty required Text → PG_FORMAT, nonempty but insufficient why_film не становится acceptable от длины; substantive finding идёт на stage6. Whitespace-only text не silently rewritten, human/product policy решает пригодность.

## 4. OP-04 — arrays and global amplification

Recommendation:10,000 elements **per array**, tighter field-specific cardinalities/uniqueness остаются обязательны. Strings/keys/object members не array elements; object member limit — отдельный OP-07 choice. Arrays сохраняют порядок; нельзя silently truncate/deduplicate/sort их ради cap/hash.

`[0,…,0]` с10,000 numbers имеет10,001 JSON value nodes и20,001 lexical tokens по P3 accounting. Поэтому array length не равно node/token count.100 arrays по10,000 scalars обходят только per-array guard, но должны быть ограничены global nodes/tokens/bytes. This is analytical reasoning, **not executed parser test**.

Alternatives2,000 conservative/20,000 named large profile. Публичный safety claim «array cap предотвращает DoS» недопустим без OP-07. V056/V057 относятся только к условному10,000 profile. Validation field semantics (например exactly ru/uk scene-plan set) строже generic max и не заменяется cap.

## 5. OP-05 — canonical byte model cross-check

Предложение: сохранить pinned PG-C14N-1 rules как единый, явно версионируемый byte contract. Не использовать SI/G2/Git hashes как aliases и не применять serializer-dependent escaping. Ни existing vectors, ни их literals не изменяются этим dossier.

| Rule choice | Exact recommendation | Pinned support / limitation |
|---|---|---|
| UTF8/BOM | Strict scalar UTF8/no initial BOM; no normalization | V003/V004/V025–028/V067; partial strings not whole-file proof |
| Integers | Exact signed64, bool not Int, no floats/exponents/NaN/Infinity; minimal decimal; -0 canonical0 | V015–017/V029–033/V046–049; token -0 acceptance is still proposed OP choice |
| Keys | Codepoint lexicographic sorting, not locale/UTF16; duplicates after unescape rejected | V001/V011/V023/V024; scalar validity required before sort |
| Strings | Quote/backslash escapes, short b/f/n/r/t, remaining controls lowercase u00xx; other scalars literal; slash unescaped | V005–008/V044/V067 |
| Arrays | Original element order, no semantic set sorting | V009/V010 distinct hashes |
| Null | Explicit nullable field only; missing and null distinct | V035/V036; C14N null probe не valid PG root |
| Domain | SHA256(UTF8("StoryStudio/PG-C14N-1") + byte00 + canonical envelope without own top-level binding_sha256) | V019–022/V037/V040; nested bindings retained |
| Raw refs | Actual raw byte SHA256 and byte_length; no prefix | V018/V066; object path/name не trusted resolver |

Signed64 parsing proposal: guard numeric token length/range lexically **before** arbitrary-precision conversion/allocation. After JSON sign/leading-zero grammar, at most19 magnitude digits; equal-length compare against9223372036854775807 (positive) or9223372036854775808 (negative). -0 remains proposed canonical0. This is a contract requirement to review, not evidence a current parser implements the guard.

No contradiction found by pinned-text/vector inspection: -0, composed/decomposed Unicode, non-BMP order, escaped controls и signed64 extremes agree with proposed rules. **No canonicalizer/validator invoked here.** Existing B paired mode cases preserve X02: lexical known value differs from allowed contract-mode pair. If external canonical standard выбран вместо custom format, требуется explicit byte compatibility mapping/new namespace, не fallback/re-hash существующих approved objects.

Proposed self-hash exclusion removes **only own** binding field after structural checks. It does not remove similarly named fields in nested ObjectRef or body. Invalid length/case of Hash is schema PG_FORMAT; matching-shape but wrong local digest is stage3 PG_DIGEST. Canonical bytes are not proof of origin, currentness, immutable filesystem or authority.

## 6. OP-06 — remaining error-selection choices, X01/X02 fixed

**Already approved, not reopened:** stages1 bounded decode;2 JSON/schema/types/known enum;3 local binding;4 refs/closure/dependencies;5 mode/subject;6 product/rights/trusted-state;7 execution/evidence. Empty Text stage2 PG_FORMAT; known mode+old digest PG_DIGEST before PG_MODE; known mode+correct binding+forbidden pair PG_MODE after refs; unknown mode enum PG_FORMAT. V039/V051/V071/V073 expectations unchanged.

Only remaining same-stage/multiple-defect choices below are **PROPOSED**. First failing **stage** always wins; a later-stage higher-priority code cannot supersede earlier failure. Recommendation: fixed within-stage code order, then canonical schema field/ref identity order for safe private diagnostics. Alternative: first canonical field/ref walk with code derived from that cause. Owner должен выбрать одну policy, не implementation-specific arbitrary traversal.

| Remaining case | Proposed primary selection | Alternative / rationale | Owner decision needed |
|---|---|---|---|
| Multiple stage1 malformed/size/BOM causes | PG_FORMAT; resource guard before growing/decode | Same public code, private reason order bounded-input then decode | Confirm safe reason ordering without early allocation |
| Multiple schema/type/duplicate failures | PG_FORMAT; canonical declared field order, arrays original index | Source lexical order would vary public diagnostics by whitespace/order | Confirm deterministic diagnostic ordering, no raw private key echo |
| Malformed Hash field and numeric/schema violation | stage2 PG_FORMAT, not stage3 digest math | Already consistent with X02; don't hash invalid structure | Confirm mapping and field ordering |
| Conflicting identity/dangling ref versus resolved ByteRef hash mismatch in stage4 | Proposed within-stage order PG_FORMAT(resource/target shape), PG_REFERENCE(registry/typed link), PG_DIGEST(resolved bytes) | Canonical ref walk first instead of global category order | Choose exact stage4 priority; current source allows different isolated causes |
| Missing dependency versus unavailable trusted service | Missing declared supplied ref stage4 PG_REFERENCE; genuine required operational service unavailable at applicable trusted predicate PG_DEPENDENCY_UNAVAILABLE | Do not fabricate not-found from service outage or treat cached state trusted | Select explicit resolver/provider failure contract later; pure mapping now describes causes only |
| Forbidden mode plus wrong subject at stage5 | Proposed PG_MODE then PG_REFERENCE then PG_SCOPE within stage5 | Canonical field order alternative, still after refs and local hash | Choose deterministic tie policy; paired single-cause B cases unaffected |
| Multiple trusted/product/rights causes at stage6 | Proposed verified-context availability → identity/authority/history → revoke → expiry → evaluation/currentness → product → rights | Other fixed same-stage order acceptable only by explicit owner decision | Choose safe ordered codes on **established** facts; no guessing human finding/provider state |
| Failed run, missing outputs, corrupted evidence at stage7 | Proposed dependency/history loss first, then PG_EXECUTION, PG_INCOMPLETE, PG_DIGEST actual-byte tamper, PG_EVIDENCE unsupported commit claims | Earliest observed failure with immutable causal log; cannot assert observed chronology without evidence | Freeze primary code versus Body05 failure/INDETERMINATE distinction |
| Unknown internal exception | PG_DEPENDENCY_UNAVAILABLE only for actual dependency failure; otherwise stage-specific fixed error when known; no fake success | Generic rejection without public detail; private classified trace | Select safe exception classification protocol, no raw dumps |

This matrix does not invent PG error codes or qualify actual providers. A HUMAN negative finding can be consumed only if supplied under the future review policy; code selection does not evaluate scientific truth. Full semantic/runtime error behavior remains NOT_RUN. Source oracle branches retain original history and B override precedence.

## 7. OP-26 — status boundary

Recommendation: `STRUCTURALLY_VALID` descriptive only, no new machine enum. Pure API result namespace remains `CONSISTENT_NO_AUTHORITY` / `DENY`; Body05.outcome and byte/hash/structural check annotations remain separate concepts. A future status extension requires explicit versioned owner decision, no silent client compatibility assumption. Public-facing message «форма корректна» must not imply «тема одобрена» or «можно рендерить».

## 8. OP-27 — actual 21-code catalogue and safe messages

Catalogue was extracted from the **explicit catalogue sentence** in pinned `G3_2_0A_ERROR_AND_ORACLE_MATRIX.md`, not by counting every PG-like word in reports. Source contains21 unique codes; verification labels and mentions of nonexistent PG_VERSION are excluded. The list below is a proposed fixed RU public-message mapping, **not UI implementation/export permission**. Audience/access policy for exposing even a code remains OP-21/23 operational work; P1 does not require connecting it now.

| Existing proposed code | Proposed fixed safe public message |
|---|---|
| PG_FORMAT | Данные не соответствуют формату. |
| PG_DIGEST | Контрольная сумма не совпала. |
| PG_REFERENCE | Связанные данные не подтверждены. |
| PG_EVALUATION | Оценка не подходит для этого перехода. |
| PG_STALE | Связанные данные требуют обновления. |
| PG_PRODUCT_GAP | Не закрыты содержательные требования. |
| PG_IDENTITY | Личность не подтверждена. |
| PG_AUTHORITY | Полномочия не подтверждены. |
| PG_HISTORY | История решений не подтверждена. |
| PG_REVOKED | Решение нельзя использовать. |
| PG_EXPIRED | Период действия завершён. |
| PG_RIGHTS | Права для заданного использования не подтверждены. |
| PG_SCOPE | Действие выходит за заданные границы. |
| PG_MODE | Режим не подходит для этого контракта. |
| PG_REPLAY | Попытку нельзя повторить этим запросом. |
| PG_PATH | Место выполнения не прошло проверку. |
| PG_TOOLCHAIN | Набор инструментов не подтверждён. |
| PG_EXECUTION | Выполнение не завершилось успешно. |
| PG_INCOMPLETE | Результат неполон. |
| PG_EVIDENCE | Свидетельства выполнения не подтверждены. |
| PG_DEPENDENCY_UNAVAILABLE | Обязательная зависимость недоступна. |

No raw path/secret/material text/reviewer identity/exception interpolation. Private trace может хранить bounded fixed reason identifiers, causal stage и opaque references under separate privacy policy; это не право публиковать private IDs или dumps. Public primary error versus private ordered detail selection — explicit OP-06/27 choice. Alternative: safe ordered error list с тем же earliest-stage primary; без top-N masking blocking product findings в приватном review view.

## 9. P1 approval questions and migration boundary

Рассмотреть вместе восемь отдельных вопросов OP-01…06/26/27 из dossier, не «approve entire production gate». Numeric caps и exact canonical rules при принятии должны получить explicit profile/version and fixture applicability. Existing conditional vectors remain immutable, no retrospective PASS claim. P2/P3 будут использовать выбранные units; P4/P5 supply real policy/trust later. Ни один P1 hard dependency не требует operational provider.

All eight remain OPEN/PROPOSED as source registry specifies; direction and readiness не approval. Existing G1/G2/G3.1/CI/vectors unchanged. **STOP: no validator, integration, render or G3.2.1.**
