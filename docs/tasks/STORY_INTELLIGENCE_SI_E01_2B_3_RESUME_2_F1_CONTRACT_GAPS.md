# SI-E01.2b.3-RESUME-2-F1 — current REVISION Run H.editorial_refs

Дата: 2026-11-10 (Europe/Kyiv). **C — BLOCKED_CONTRACT.**
Implementation base: `c90b94a108ba2ef4b1a4a5ab8226d206b79fbf21`.
Это diagnostic question, не исправление production-кода или утверждённых правил.

## Что фактически доказано

[Reproducer](../../tests/test_story_intelligence_currentness_eref_f1.py) строит новый
canonical Source S1 → actual REVISION Run R → Source S2 граф. В T2 только R объявляет
одну well-formed unresolved ERef; S2.H.editorial_refs=[], S2.payload.editorial_ref=null,
observed active=[exact S2], editorial snapshot UNKNOWN, adapter отсутствует.
После изменения R пересчитаны SHA R/S2 и observed exact ref. Resolver и provenance
проходят; checker фактически возвращает **CURRENT / []**. T3 с той же ERef прямо
в S2.H и T4 в original CREATIVE C.H возвращают **INVALID / [REF_MISSING]**.
Graph/context/root/producer hashes и команды — в [RESULT](STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_2_F1_RESULT.md).

Это доказывает асимметрию обработки. Для CONFIRMED_DEFECT дополнительно необходимо
доказать **обязательную содержательную роль** именно R.H.editorial_refs. Для
CONTRACT_COMPLIANT необходимо доказать её **audit-only роль**. Ни успешные tests,
ни комментарий/условие production-кода, ни наличие finding в review этим proof не являются.

## Сопоставление точных утверждённых clauses

| Нормативный документ | Пункт / строки exact base | Применение и оставшийся вопрос |
| --- | --- | --- |
| [Original SI/1](STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md) | §2.1 H; §8, строки 351–355 | H содержит editorial_refs; ERef без supplied snapshot → REF_MISSING/INVALID. Общее правило не даёт специальной роли ERef текущего REVISION Run после G01 projection |
| [R1](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md) | §1.1, строки 65–72 | H одинаков для Run и domain records, editorial_refs:List<ERef>; поле допустимо и у R, но содержательная роль этой позиции не аннотирована |
| R1 | §1.2, строки 141–144 | «При ERefs нужен supplied exact validated editorial snapshot/hash context, иначе INVALID» — обязательный отказ для relevant ERefs, не доказательство, какие Run header edges current |
| R1 | §1.3, строки 148–150 | Audit Closure следует H/payload SIRefs, ERefs разрешаются отдельно; accepted pure resolver/provenance ERef material не удостоверяют |
| R1 | §4.2, строки 304–315 | SemanticClosure следует содержательным payload refs и origin Run.semantic_input_refs; H.previous, snapshots/декоративная metadata исключаются; отдельный ERef snapshot context обязателен. R.H.editorial_refs явно не классифицирован |
| [R1a](STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md) | §§2–4, особенно строки 91–98 | Current REVISION Run фиксирует base + current payload roots, audit ancestry сохраняется; нет запрета R.H.editorial_refs и нет правила её ERef relevance |
| [G01 approved proposal](STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_DECISION_PROPOSAL.md) | D1–D2, строки 10–18 | Edit-base и metadata edges исключаются *как таковые*, но still-relevant inherited producer refs сохраняются. Это не явное утверждение, что любая ERef на текущем R — metadata-only |
| [G01 owner approval](STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_APPROVAL_2026_11_10.md) | D2/D4, строки 15/19 | Неразрешённая роль требует fail-closed/report; **relevant ERef** без validated snapshot → INVALID. Не задано, относится ли сюда текущий R.H.editorial_refs |
| [G02 owner approval](STORY_INTELLIGENCE_SI_E01_2B_3_G02_OWNER_APPROVAL_2026_11_10.md) | D1–D4, §Contract precedence | Решает только direct original C ClaimItem constraints; не назначает роль ERef REVISION Run |
| [R1b approval](STORY_INTELLIGENCE_V1_R1B_OWNER_APPROVAL_2026_11_09.md) | P01–P05 | Packet field paths/projections; не разрешение обойти ERef и не классификация R header |

G01 не требует R или S1 как **active domain identities**, но исключение их identities
само по себе не доказывает исключение содержащихся в R explicit editorial refs.
В обратную сторону общее «при ERefs» нельзя без уточнения применить ко всем старым
history-only Run refs, игнорируя утверждённую semantic/audit projection. В T2 R —
**текущий** производящий Run, а не произвольный исторический predecessor: его роль
требует конкретного решения. Прямого утверждённого правила/отрицательного запрета для
этого сочетания не найдено. Статус A или B сейчас был бы выбранной агентом политикой.

## Конкретный вопрос владельцу и варианты

Должна ли **каждая ERef непосредственно в H.editorial_refs текущего actual REVISION
Run, указанного в X.H.origin.run_ref, считаться relevant producer dependency X**, даже
когда X.H.editorial_refs пуст и current payload не содержит ERefs?

| Вариант — пока НЕ УТВЕРЖДЁН | Ожидаемый T2 | Последствия |
| --- | --- | --- |
| 1. Да; explicit header ERefs текущего actual producer required, без promotion всей audit Closure (**рекомендация**) | INVALID / REF_MISSING без validated snapshot | Будущий bounded fix должен проверить current R header до ordinary HUMAN_EDIT continue, сохраняя audit-only previous/snapshots. Не требует ERef adapter |
| 2. Нет; для данной ordinary HUMAN_EDIT позиции они явно audit-only | CURRENT при остальных валидных deps | Нужна явная approved exemption, границы по stage/type и объяснение отличия от direct domain/original C header. Нельзя выводить её только из RUN_METADATA mode |

Уточнение должно отдельно зафиксировать, что происходит с ERefs **исторических**
Runs, текущего actual REVISION Run Creative (он отличается от original C), и с
header refs, совпавшими с current domain ERef: mandatory independent refs нельзя
потерять из-за дублирования. Это scope границы будущего решения, не реализация
дополнительных сценариев или нового role map в данном F1.

Рекомендуется вариант 1 как узкий fail-closed policy: explicit declared ERef текущего
producer не игнорируется из-за пустого current payload. Но recommendation — не
owner approval и не основание самостоятельно изменить текущий код/contract.
Если владелец выберет 1, отдельное fix-задание может изменить порядок guard и добавить
нормативный T2 regression с INVALID; в данном F1 такого исправления нет.

До independent review и решения владельца **acceptance SI-E01.2b.3 не заявляется**.
Диагностические PASS подтверждают действительный граф и наблюдаемую асимметрию,
а не contractual compliance CURRENT. G01/G02, код и старые vectors неизменны.
STOP; без PR/merge/release/main, SI-E02, ERef adapter или protected writes.
