# SI-E01.2b.3-F1-D1 — Current producer ERef: owner approval

**Дата:** 2026-11-10 (Europe/Kyiv).
**Статус: APPROVED / OWNER DECISION.**
**Решение владельца:** «F1-D1 APPROVED — 2026-11-10» с правилами D1–D5 ниже.
**Объём текущего этапа:** documentation only / no production implementation.

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Точная база публикации: `7c49510b33c87251af415bb060c2fe9eacb8df08`.
Ветка: `docs/story-intelligence-si-e01-2b-3-f1-d1-approval`.

## Основание и статус предыдущих результатов

Прочитаны [F1 RESULT](STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_2_F1_RESULT.md) и
[F1 CONTRACT_GAPS](STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_2_F1_CONTRACT_GAPS.md),
опубликованные на exact base: настоящий Source S1 → REVISION Run R → S2 graph
в T2 проходит resolver/provenance, но с unresolved R.H.editorial_refs checker
возвращает CURRENT. T3 (direct S2 header) и T4 (original C header) возвращают
INVALID / REF_MISSING. F1 выбрал C — BLOCKED_CONTRACT из-за неуточнённой роли R header.

Владелец теперь явно разрешает **этот конкретный нормативный вопрос**. Прежние
отчёты остаются неизменными историческими фактами; их status, результаты и SHA
не переписываются. Approval не является implementation fix или independent acceptance.
По зафиксированному ниже правилу T2 должен стать INVALID / REF_MISSING; код ещё
не изменён и выполнение будущих regression tests здесь не заявляется.

## Утверждённые правила F1-D1: D1–D5

### D1 — Current producer ERef

Каждая ERef непосредственно в `H.editorial_refs` **фактического производящего Run
текущей ревизии** является релевантной зависимостью.
Без **exact validated editorial snapshot** результат — **INVALID / REF_MISSING**.
Пустой H.editorial_refs/payload самой domain-записи не снимает независимый producer
constraint. UNKNOWN, opaque hash или status не заменяют validated snapshot.

### D2 — HUMAN_EDIT

D1 применяется к текущему `REVISION Run` обычных HUMAN_EDIT записей.
Оно также применяется к **текущему REVISION Run ручной ревизии CreativeAlternative**:
его exact ref находится в `H.origin.run_ref` и не взаимозаменяем с original C
в `payload.run_ref`. При K3 проверяется actual R3, а не только C.

### D3 — Historical boundaries

Исторические Run, `H.previous`, `input_snapshot` и `context_snapshot` сохраняются
для audit/provenance. Их ERefs **не становятся автоматически required-current
исключительно вследствие присутствия в audit Closure**.
Нельзя обходить всю audit Closure и отклонять текущую ревизию из-за любой встреченной
там ERef. Исключение относится к одной лишь исторической роли; оно не отменяет
независимую действующую содержательную связь, если такая действительно существует.

### D4 — Original CREATIVE Run

Сохраняются утверждённые G01/G02 требования к **исходному CREATIVE Run C** и его
содержательным зависимостям. Игнорировать ERefs исходного C запрещено.
Для ручной K2/K3 нужны обе границы: actual R2/R3 по D1–D2 **и** original C по D4.
Проверка одного не заменяет проверку другого; historical-only R2 при проверке K3
сам по себе не превращается в current producer.

### D5 — Compatibility

Нет новых wire fields, error codes, ERef adapter, implicit latest, автоматического
rebasing или изменения файлов существующих утверждённых контрактов.
Это узкое уточнение **F1-D1**; остальные решения G01/G02 сохраняют силу.
Precedence original SI/1 → precise R1 → precise R1a → approved R1b сохраняется;
данное owner decision разрешает только указанную current-producer ERef ambiguity.

Основания: [original SI/1](STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md),
[R1](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md),
[R1a](STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md),
[R1b approval](STORY_INTELLIGENCE_V1_R1B_OWNER_APPROVAL_2026_11_09.md),
[G01 approval](STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_APPROVAL_2026_11_10.md),
[G02 approval](STORY_INTELLIGENCE_SI_E01_2B_3_G02_OWNER_APPROVAL_2026_11_10.md).
SI-D01–SI-D10 и принятые editorial/storage boundaries не пересматриваются.
CURRENT не доказывает факты, execution, identity, права или production permission.

## Отдельное FIX-задание и STOP

Подготовлено [F1 FIX CODEX TASK](STORY_INTELLIGENCE_SI_E01_2B_3_F1_FIX_CODEX_TASK.md)
с закрытым allowlist, red/green, actual Creative REVISION и historical-only controls,
проверкой всех 10 literal vectors и raw/outer exit codes.
Его публикация **не запускает FIX**: после независимого review владелец передаёт
задание отдельно с точным опубликованным SHA этой docs-ветки.

В текущем commit создаются только этот approval и FIX task. Существующие source,
tests, vectors, документы, contracts, RFC и main неизменны. Unit/full suites для
этого documentation-only этапа не запускались; ссылки, diff/allowlist и exact base
проверяются при публикации. Прежние F1 counts — история, не новый test PASS.

**STOP после публикации для independent review.** Никаких FIX, PR, merge, release,
main changes или SI-E02. `PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction
OFF; Windows S3.2b BLOCKED_HOST_NOT_PROVIDED.
