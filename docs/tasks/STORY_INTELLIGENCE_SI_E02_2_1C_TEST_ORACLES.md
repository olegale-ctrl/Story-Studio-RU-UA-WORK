# SI-E02.2.1c — Required-current: proposed independent test oracles

Дата: 2026-11-10. **PROPOSAL / NOT APPROVED / NOT RUN.**
Base: `ba7af2aaf3571fe801ee26b6027fd5b734b50094`.
[Owner approval](STORY_INTELLIGENCE_SI_E02_2_1C_OWNER_APPROVAL_2026_11_10.md) нормативен
только для EVAL-F01–F03. [Local contract](STORY_INTELLIGENCE_SI_E02_2_1C_REQUIRED_CURRENT_CONTRACT_PROPOSAL.md)
и все case fixtures/точные диагностики здесь **не утверждены**. Колонка status
отмечает уже established normative component, а не premature approval всего case.

## Preconditions и независимость

B — будущий genuine SI graph с exact valid/current Idea/Angle/Audience/Channel/Rubric/
source/claim/check roots при необходимости; complete typed ratings/approved findings,
KNOWN local portfolio покрыт, no other blockers/research/duplicate gaps, если case не
задаёт их явно. Все relevant refs exact, graph/provenance accepted. Есть полный supplied
observed context; CURRENT само по себе не доказывает scientific/rights sufficiency.

Для freshness proof положительных cases самостоятельно authored EvidenceItem,
ClaimCheck и material SourceItem имеют настоящие content hashes, поддержанный
review scope и supplied period. Это synthetic human assertions, не научная истина.
Никаких mocks resolver/provenance, fake hashes, auto-created reviewed state или
подстановки findings в existing SI records.

Scores/primary states/codes/paths/period comparisons/expected hashes фиксируются до
implementation; не вызывать evaluator для получения собственного expected result.
Новых golden bytes сейчас нет. Нормативные 42 findings requirements сохраняются с
T25/T27 limitations; эти 34 новые rows их не переписывают и ещё не утверждены.

Условные обозначения: **F** = owner-approved primary rule; **Existing** = ранее
approved SI validation/currentness/R1 правило; **RC** = результат зависит от
неутверждённой конкретизации RC-P01–P06. Отсутствие дополнительного freshness gap
означает ELIGIBLE_FOR_CREATIVE только при всех B premises.

## Literal primary outcomes и proposed diagnostics

| ID | Explicit input / condition | Expected primary outcome и codes | Approval status результата |
| --- | --- | --- | --- |
| C01 | UNDETERMINED, иначе B | NEEDS_INPUT; proposed [EVIDENCE_NEEDED] | F02 primary; RC-P05 codes/paths |
| C02 | REQUIRED; required_data UNKNOWN либо KNOWN [] | NEEDS_INPUT; [EVIDENCE_NEEDED] | F02 missing-spec primary; exact representations RC-P02 |
| C03 | REQUIRED; data spec KNOWN, period UNKNOWN | NEEDS_INPUT; [EVIDENCE_NEEDED] | F02 primary; shape/code RC-P02/P05 |
| C04 | REQUIRED complete; insufficient established freshness | NEEDS_RESEARCH; [EVIDENCE_NEEDED] | F02 primary; adequacy predicate RC-P03/P04 |
| C05 | REQUIRED complete + explicitly adequate exact support/period, all B | ELIGIBLE_FOR_CREATIVE; [] | Existing R1/F02 absence of gap; concrete adequacy/fixture RC |
| C06 | NOT_REQUIRED; all source freshness explicitly NOT_APPLICABLE, B | ELIGIBLE_FOR_CREATIVE; [] | F02 no extra gap; applicability encoding/whole fixture RC |
| C07 | NOT_REQUIRED; APPLICABLE source with UNKNOWN freshness | NEEDS_RESEARCH; [EVIDENCE_NEEDED] | F02 primary; local encoding/diagnostics RC |
| C08 | Missing entire premise / None | NEEDS_INPUT; [EVIDENCE_NEEDED] | F03 primary; None convention/code RC-P01/P05 |
| C09 | Present object omits required_data mandatory field | INVALID/MISSING_FIELD; no accepted eligibility | F03 malformed failure; exact mandatory field/path RC-P01/P05 |
| C10 | Valid exact Source ref, but assessment bound to different/out-of-S subject | INVALID/PROVENANCE_MISMATCH | F03 wrong-binding failure; S rule/code/path RC-P02/P05 |
| C11 | Genuine old source/premise/context; observed selection switched to new Source revision | STALE/INPUT_STALE; no current result | Existing exact currentness/expected-context; RC local binding detail |
| C12 | Genuine binding frozen context A, observed context B | STALE/INPUT_STALE; no current result | Existing/EVAL-P04, proposed local field paths RC |
| C13 | Two sources: A REQUIRED+complete+adequate; B ordinary APPLICABLE+UNKNOWN | NEEDS_RESEARCH; [EVIDENCE_NEEDED]; A not downgraded or used to clear B | F02 per applicable gap; per-source encoding/coverage RC |
| C14 | Explicit essential rights blocking Risk plus UNDETERMINED | BLOCKED; proposed [EVIDENCE_NEEDED,RIGHTS_BLOCKED], input diagnostic retained | Existing R1/F02 priority; base blocker premises explicit, local mapping RC |
| C15 | REQUIRED spec/period incomplete; another ordinary APPLICABLE source UNKNOWN | NEEDS_INPUT; [EVIDENCE_NEEDED] unique; separate input/research diagnostics | F02/R1 precedence; exact union/diagnostics RC-P05 |
| C16 | Exact EVAL-RESUME-G01 graph/ratings/findings + separate determination UNDETERMINED | **NEEDS_INPUT**, not NEEDS_RESEARCH/ELIGIBLE; proposed [EVIDENCE_NEEDED] | F02 exact owner-approved primary; new premise form/diagnostics RC |
| C17 | Exact original reproducer remains byte-identical; no new premise | NEEDS_INPUT, not automatically INVALID | F03 missing determination; code/path RC-P05 |
| C18 | Legitimate current HUMAN_EDIT source S3; S1/S2 audit-only, intact/inactive | No additional freshness coverage gap for S1/S2; existing CURRENT with proper active inputs | Existing G01 ancestry; RC-P02 freshness S projection |
| C19 | Actual current REVISION producer H.editorial_refs unresolved, positive premise | INVALID/REF_MISSING before eligibility | Existing F1-D1; positive F determination cannot waive |
| C20 | Relevant original CREATIVE Run ERef unresolved | INVALID/REF_MISSING at accepted dependency boundary | Existing G01/G02/F1-D1; not a new mandatory Creative input to EVALUATE |
| C21 | Required original C direct Claim ref valid historically but absent active | STALE/INPUT_STALE at accepted dependency boundary | Existing G02; neither freshness proof nor historical exclusion cancels substantive role |
| C22 | Repeat same explicit inputs later in calendar time; compare input copies | Equal detached result, inputs exact bytes unchanged; no clock-dependent expiry | Future pure requirement, implementation tests NOT APPROVED/NOT RUN |
| C23 | Source.freshness_requirement UNKNOWN; NOT_REQUIRED and explicit NOT_APPLICABLE source assessment | No automatic Source edit; no extra freshness gap, eligible only under B | F01/F02 no inference; precise positive scope sufficiency RC-P02/P04 |
| C24 | APPLICABLE ESTABLISHED, evidence [], human reason nonempty | NEEDS_RESEARCH; [EVIDENCE_NEEDED]; not auto adequate | RC-P04 specific minimum-support policy, NOT APPROVED |
| C25 | Evidence material known hash differs from supplied hash | INVALID/REF_HASH_MISMATCH, no research-as-repair | F03 binding failure in principle; exact proof fields/mapping RC-P04/P05 |
| C26 | Graph-valid support has unreviewed ClaimCheck or insufficient relation/unknown locator | NEEDS_RESEARCH; [EVIDENCE_NEEDED], no fabricated review | RC-P04 adequacy rule; existing records remain structurally valid where applicable |
| C27 | Valid proof coverage 2026-11-01..03; review requires 2026-11-01..04 | NEEDS_RESEARCH; [EVIDENCE_NEEDED]; no default extension | RC-P03/P04 interval rule, NOT APPROVED |
| C28 | Supplied period.from_utc > to_utc, or malformed UTC | INVALID/TYPE; not missing freshness | RC-P01/P03 closed local period validation |
| C29 | required_data period changed, old SourceFreshness.requirements_sha256 retained | INVALID/REF_HASH_MISMATCH; no automatic rebind | F03 exact binding principle; digest composition RC-P01/P02 |
| C30 | Two identical or contradictory SourceFreshness for one exact Source | INVALID/TYPE on second item | F03 contradictory binding rejection; uniqueness rule RC-P02/P05 |
| C31 | Present period null instead of Known<Period>, extra local key or bad tag | INVALID/TYPE, UNKNOWN_FIELD or VERSION_UNSUPPORTED at respective field | F03 malformed premise principle; concrete shape/order RC-P01/P05 |
| C32 | Freshness support SIRef missing/hash-corrupt/cyclic | INVALID/REF_MISSING, REF_HASH_MISMATCH or DEPENDENCY_CYCLE; no accepted result | Existing resolver/provenance; proof lookup scope RC |
| C33 | UNDETERMINED with KNOWN required_data list or NOT_REQUIRED with nonempty requirements | INVALID/TYPE per proposed combination rule | **Only RC-P02; F01–F03 do not independently establish this exact rejection** |
| C34 | Coherent proof material has relevant unresolved ERef, another root STALE | INVALID/REF_MISSING takes precedence; no positive freshness result | Existing ERef/INVALID priority; inclusion of explicit proof roots in checks RC-P02/P05 |

## Оригинальный reproducer — точность и отсутствие retroactive PASS

Ссылка: [EVAL-RESUME-G01 §3](STORY_INTELLIGENCE_SI_E02_2_1_RESUME_CONTRACT_GAPS.md).
Остаются 8 records / 8-ref Closure / 6 CURRENT domain roots; no claims/risks/ERefs,
KNOWN empty portfolio, девять KNOWN5/HIGH ratings, пустые legal confidence/pair arrays.
Source.freshness_requirement UNKNOWN; это не missing SIRef или malformed Known.

Неизменные diagnostic identities исходного input:

- records SHA256: `d0629b82eeb589253199ac0dcd9a8ee71bf76a942780dde5fd45bd41c46a8b61`;
- ratings SHA256: `3a3e6fe51ce5715364ba7d7fe83c612749a2528ce44f472c8802e796cec987fd`;
- existing HumanFindingsInput SHA256: `cff2c041ed8a348e52727ea47a26c088aa8aae1b56184fed06ddbe6b304d7eeb`;
- expected/observed ContextSnapshot SHA256: `89c43e0d9c54cb16d749c5acc19f133549c1512fe4effa5de65a335da8a67e5b`.

C16 добавляет отдельную UNDETERMINED premise, не меняя эти четыре values. C17 не
добавляет premise. Новая premise ещё не имеет approved canonical fixture/hash;
не выдумывать его и не переписывать original findings/context ради нового поля.
Owner-approved expected primary outcome C16 — NEEDS_INPUT. Прежнее «eligibility
не вычислялся» остаётся исторически верным: сейчас tests/evaluator тоже не запускались.

## Oracle limits

В будущем literal expected messages/paths/hashes фиксируются независимо до исполнения.
Codes в таблице для новых mappings — conditional RC, даже при approved primary state.
Положительные adequacy cases требуют actual coherent synthetic graph, не boolean
flag, который обходит accepted refs/provenance/currentness. Hash/code equality сама
по себе не доказывает реальную freshness/science/rights/identity.

C18–C21/C34 сохраняют G01/G02/F1-D1, не требуют новых adapters/Creative records для
первой evaluation. C14/C15 — explicit bounded premises, не полный base classifier T25.
Проверки established other blockers/research/duplicate reasons сохраняются, score их
не снимает. Findings contract EVAL-P01–P04 и EVAL-P05 OPEN остаются неизменными.

**Unit tests: NOT RUN — DOCS ONLY.** Ни один case не помечен runtime PASS или новым
утверждённым test artifact. **STOP; implementation NOT AUTHORIZED.**
`PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF;
Windows S3.2b BLOCKED_HOST_NOT_PROVIDED. Без PR/merge/release/main changes.
