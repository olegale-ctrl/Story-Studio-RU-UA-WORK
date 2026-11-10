# SI-E01.2b.3 — Contract gaps

Дата: 2026-11-10. **Статус: BLOCKED_CONTRACT, implementation not started.**
База: `658212f9a8f5e91a5af9551093cbd85d7512c08a`.
Это узкий вопрос для решения владельцем, не изменение утверждённых contracts,
не отзыв прежних independent acceptances и не реализация RFC.

## SI-E01.2b.3-G01 — role projection для HUMAN_EDIT semantic roots

### Основание STOP

[Полное задание](STORY_INTELLIGENCE_SI_E01_2B_3_CODEX_TASK.md) §3, строка 36:

> Under-specification of active input coverage/identity or causal dependency extraction also requires STOP instead of weaker currentness labels.

§6 того же задания предписывает при недостаточной семантике публиковать только
GAPS + RESULT, без guessed/partial code. [Приёмка provenance/F1](STORY_INTELLIGENCE_SI_E01_2B_2_F1_INDEPENDENT_ACCEPTANCE.md)
принимает supplied cross-record consistency, явно оставляя semantic currentness
для отдельного этапа. Правила observed active set и causal→semantic projection
нельзя выводить из одного факта успешной provenance-проверки.

### Какие правила уже определены

| Источник | Утверждённое правило |
|---|---|
| [R1](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md) §1.2, строки 132–136 | Active set содержит явно выбранные current domain refs, без history-only previous/Run metadata; одна exact revision на (type,id) |
| R1 §1.3, строки 156–158 | Run.semantic_input_refs — direct содержательные roots операции; input_snapshot — полная audit Closure этих roots и context |
| R1 §2, строки 184/199–202 | REVISE_INPUT roots: base_ref, затем payload refs в schema order |
| R1 §4.2, строки 304–308 | SemanticClosure следует substantive payload refs и origin Run.semantic_input_refs; не generic H.previous/input_snapshot/context_snapshot |
| R1 §4.2, строки 311–322 | Required exact semantic refs должны быть current; missing/different active dependency → STALE; required Selection отдельно от active inputs |
| [R1a](STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md) §§2–4, строки 67/92–96/130–137 | HUMAN_EDIT Run содержит exact base и новые payload refs; previous/original CREATIVE ancestry сохраняется; history-only dependencies не превращаются в current inputs |
| Новое задание §3, строки 32–34 | Historical H.previous и Creative.payload.run_ref не становятся domain input автоматически; revised Creative использует substantive current dependencies |

Ни одна из этих clauses не задаёт точную **role-aware projection** mandatory
REVISION edit-base из Run.semantic_input_refs в множество required-current domain
refs: считать ли сам base текущим входом, проходить ли через него как transparent
carrier прежних domain bindings, какие старые зависимости заменяются текущим payload,
какие сохраняются. Просто не обходить generic H.previous edge недостаточно:
**тот же exact ref находится в обязательном direct semantic list Run.**

### Минимальный настоящий ERef-free граф

Использованы существующие, неизменённые fixtures:

```python
from tests.test_story_intelligence_provenance_v1 import provenance_graph
from story_intelligence.provenance_v1 import verify_si_provenance

g, named = provenance_graph()
root = named['revision']
manifest = verify_si_provenance(g.records, [root])
observed_active_input_refs = [root]
observed_selection_head_refs = []
```

Это SourceItem S1→S2→S3, а не illustrative aliases вместо wire refs. Accepted
resolver + provenance фактически подтвердили **5 exact refs**: три Source revisions
и два actual REVISION Runs с точными snapshots. В queried audit closure проверено
**0 actual ERefs**, current payload Source3 не содержит SIRef dependencies.
S1 — USER_IMPORT, S2/S3 — legal HUMAN_EDIT; никакого missing/hash corruption нет.

Один и тот же canonical Source id `00000002-2222-4222-8222-222222222222`:

| Revision | Точный sha256 |
|---|---|
| 1 | `20872a4a229323adcc560e41bcb1163e749e3e43470458d552f03369089987d5` |
| 2 | `ecc75bb3665128f58600bc354da98e95e4412afc637f65d55770edcc0657673e` |
| 3 (root/observed) | `ab692002581a847c2912f1c0feaa81e5eca85c3086aae7593599aaa2a09c6caa` |

R3.semantic_input_refs=[exact S2]; R2.semantic_input_refs=[exact S1].
H.previous и H.input_refs подтверждают те же editing bases, как требует R1a.
Observed set содержит только S3, что соблюдает one-current-revision-per-(type,id).

**Конкурирующие интерпретации, не результаты реализованного checker:**

- A: буквальное рекурсивное следование Run.semantic_input_refs включает S2 и S1
  в required-current refs. Их нет в observed set → STALE, хотя свежий Source3 и
  все его собственные domain fields валидны. Добавить S1/S2 в observed невозможно
  без нарушения правила одной active revision этой identity.
- B: mandatory editing bases считаются audit-only, их identities не required-current;
  у Source3 нет текущих payload SI dependencies → CURRENT. Но для этого нужен
  явный exception/projection для элементов **semantic_input_refs**, не только для
  generic H.previous. Не определён и общий порядок наследования content dependencies.

Эти состояния нельзя объявлять unit-test expected values без выбора новой семантики.
Нельзя замаскировать вопрос как INVALID: граф/hash/provenance/context shapes валидны.
Нельзя объявить обе версии active или разрешить root alias/latest lookup.

### Почему Creative требует не просто «пропустить base»

Второй фактический positive graph, root named['creative_dual_runs']:
`CreativeAlternative`, id `0000000f-2222-4222-8222-222222222222`, revision3,
sha256 `82762da1677de269162e8194da3dcf657d4635ca3b543660f76e43c3392ff2ce`.
Accepted resolver/provenance подтвердили **17 exact refs**.
Observed domain set из него содержит 10 refs после исключения Run metadata и
старых Creative K1/K2; конфликтов (type,id) нет.

R3.semantic_input_refs = [K2, Angle, original C1 Run, Claim, Claim].
K3.payload.run_ref = original C1. Сам payload Creative не имеет EvaluationReport ref.
Но R1 §4.2 требует для Creative exact EvaluationReport и соответствующие context
inputs; они есть в **исходном C1.semantic_input_refs**, не в текущем payload.

Буквальный обход mandatory K2/K1 требует inactive old Creative revisions. Отбрасывание
всего base и original Run целиком теряет требуемый EvaluationReport/Channel/Rubric
binding. Transparent traversal history с исключением только самих old identities
может сохранить их, но при изменённом Angle/Idea нужно утверждённое правило,
какие старые inputs остаются substantive, какие замещаются, когда результат обязан
быть STALE. Самостоятельная подстановка E2/нового Angle из observed — forbidden rebase.
В существующих type shapes нет role annotation, разрешающей выбрать policy молча.

### Минимальное решение владельца

Нужен узкий одобренный semantic-projection erratum, а не реализация RFC:

1. Определить required-current vs causal-edit-base роли в HUMAN_EDIT
   Run.semantic_input_refs. Дать явный алгоритм для base как history-only identity
   и/или transparent source: какой payload/producer traversal наследуется.
2. Задать inheritance/override для Creative K1→K2→K3: original C1 metadata не current
   input, но что происходит с его EvaluationReport/Angle/Audience/Channel/Rubric
   dependencies при неизменных и изменённых explicit fields; запрет implicit latest
   и сохранение exact hashes остаются обязательными.
3. Утвердить маленькую таблицу CURRENT/STALE/INVALID vectors для Source edit,
   text-only Creative edit и changed-Angle/Idea edit, включая exact observed sets.
   Если требуется новый declared binding или shape, это отдельный owner-approved scope,
   а не default реализации в существующем allowlist.

### ERef граница — не выдуманный отдельный блокер

R1 §1.2, строка 143, уже говорит: без supplied exact validated editorial snapshot
при релевантных ERefs — INVALID. Поэтому само отсутствие adapter **не** используется
здесь как доказательство обязательного нового BLOCKED: нельзя ложно говорить, что
R1 вообще не допускает INVALID. Однако relevance/ERef freshness не может заменить
G01 projection; пример выше ERef-free. Snapshot UNKNOWN не подтверждает свежесть,
opaque digest/shape не является validated snapshot. ERef adapter/RFC implementation
не предлагаются и не начинались. Owner clarification должна сохранять этот отказ,
не разрешать CURRENT без нужного proof и не смешивать его с STALE.

До решения G01 нельзя завершить корректный checker и требуемые positive vectors
для revised current inputs без guessed dependencies. Accepted modules остаются
неизменными; currentness_v1.py/tests/vectors не создавались. STOP.
