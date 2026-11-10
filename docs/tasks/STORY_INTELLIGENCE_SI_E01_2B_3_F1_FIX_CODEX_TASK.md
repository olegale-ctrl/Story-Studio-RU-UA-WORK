# CODEX TASK — SI-E01.2b.3-F1-FIX: Current producer ERef boundary

**Дата:** 2026-11-10 (Europe/Kyiv).
**Статус:** PREPARED / REQUIRES SEPARATE OWNER HANDOFF AFTER INDEPENDENT REVIEW.
**Authority:** [F1-D1 owner approval](STORY_INTELLIGENCE_SI_E01_2B_3_F1_D1_OWNER_APPROVAL_2026_11_10.md),
APPROVED / OWNER DECISION, D1–D5. **Не выполнять при публикации документа.**

## 1. Точная будущая база и предварительная проверка

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Source branch: `docs/story-intelligence-si-e01-2b-3-f1-d1-approval`.
Exact base SHA: **полный final remote HEAD этой docs-ветки, который владелец передаст
в отдельном FIX handoff после её публикации/review**. Не угадывать и не подставлять
старый diagnostic SHA вместо новой базы с owner approval.
Future branch: `fix/story-intelligence-si-e01-2b-3-f1-current-producer-eref`.

Сначала проверить source remote HEAD на буквальное равенство owner-supplied SHA,
наличие approval/task на этом commit и clean worktree. При несовпадении — STOP
до изменений. Ветку создать строго от точной базы; без main/RFC/старой feature fallback,
merge/cherry-pick или force push. Историческая diagnostic base:
`7c49510b33c87251af415bb060c2fe9eacb8df08`; проверяемая implementation внутри неё:
`c90b94a108ba2ef4b1a4a5ab8226d206b79fbf21`. Они provenance, не будущая FIX base.

Прочитать полностью owner approval, [F1 RESULT](STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_2_F1_RESULT.md),
[F1 GAPS](STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_2_F1_CONTRACT_GAPS.md), original SI/1,
R1, R1a, approved R1b, G01/G02 owner approvals; currentness/resolver/provenance
source и применимые tests/vectors. Diagnostic evidence сохраняется как история;
новый D1 разрешает его конкретный contract blocker, но не доказывает будущий fix.

## 2. Минимальный production fix

В [currentness_v1.py](../../story_intelligence/currentness_v1.py) после принятой
проверки полного reachable audit DAG/hashes/snapshots/provenance обеспечить:

1. Для текущей содержательно проверяемой ревизии определить **actual producing Run**
   по `H.origin.run_ref`. Проверить его непосредственные `H.editorial_refs`
   **до early continue для обычного HUMAN_EDIT**. В текущем pure API validated
   editorial snapshot не поставляется: nonempty список → INVALID / REF_MISSING.
2. У HUMAN_EDIT CreativeAlternative проверить actual REVISION Run из H.origin.run_ref
   **независимо от** original C из payload.run_ref. Нельзя заменить actual producer
   на C и потерять проверку R2/R3. Сохранить существующий guard ERefs original C.
3. Не делать Run/current edit-base required-current domain identities. Не обходить
   previous/input_snapshot/context_snapshot как semantic inputs. ERef исключительно
   в historical-only Run не инвалидирует текущую ревизию автоматически; не сканировать
   все audit nodes на наличие ERef. Если old Run имеет независимую substantive роль,
   нельзя скрывать её под historical exemption.
4. Сохранить public API, exact SIRefs/hashes, G01/G02 projection, direct C ClaimItem
   retention, CURRENT/STALE/INVALID и existing error codes. Никаких snapshot arguments,
   adapters, новых wire fields, latest/rebase, persistence или authority механизмов.

Минимизировать diff; принятые resolver/provenance/codec/models не изменять. Нельзя
ослаблять graph verification, превращать broken ancestry в STALE или возвращать
частичный CURRENT. Не выполнять broader refactor или архитектурный RFC.

## 3. Только разрешённые файлы будущего FIX

**Изменить только:**

- `story_intelligence/currentness_v1.py`;
- `tests/test_story_intelligence_currentness_eref_f1.py`.

**Создать только:**

- `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_F1_FIX_RESULT.md`.

Другие existing/new files запрещены, включая старые F1 RESULT/GAPS, approvals,
этот task, currentness general tests/vector file, все старые golden vectors,
SI/1 foundation/records/resolver/provenance, editorial/storage, RFC, WORKLOG,
README, dependencies и CI/config. Нужен выход за allowlist или возникла новая
существенная неоднозначность → STOP, описать её только в новом FIX_RESULT с
BLOCKED_CONTRACT, без guessed/partial implementation и самостоятельного contract change.

## 4. Обязательные regression cases и red/green

Сохранить genuine canonical graph construction из F1 diagnostic; без mock/patch
resolver/provenance/SHA. Rebuild все downstream hashes/refs/snapshots после synthetic
изменения fixtures; actual C и R должны проходить accepted resolver/provenance.

| Case | Условия | Expected после fix |
| --- | --- | --- |
| T1 baseline | Source S1 → R → S2; ERefs отсутствуют | CURRENT / [] |
| T2 normative regression | Только current actual R.H.editorial_refs содержит unresolved ERef; S2.H=[] и payload ERef=null | INVALID / [REF_MISSING] |
| T3 direct source control | ERef непосредственно в S2.H.editorial_refs | INVALID / [REF_MISSING], прежний отказ сохранён |
| T4 original C control | Original C.H.editorial_refs nonempty; current Creative REVISION Run clean | INVALID / [REF_MISSING], прежний отказ сохранён |
| Creative current R3 | K1→K2→K3; original C clean; ERef только в actual R3.H.editorial_refs, K3 own H/payload без ERef | INVALID / [REF_MISSING] |
| Ordinary historical-only negative control | S1→R2→S2→R3→S3; ERef только в R2.H, R3 и S3 clean; S2/R2 только audit ancestry | CURRENT / [], если остальные required deps active |
| Creative historical-only control | K3 current R3 и original C clean; ERef только в предыдущем R2.H; old K2/R2 не substantive current inputs | CURRENT / [], если остальные required exact deps active |
| Integrity controls | Missing/corrupt historical SIRef/Run/previous/snapshot | INVALID с existing resolver/provenance code, не STALE |

Исторические controls — отрицательные тесты на ошибочное распространение ERef
relevance из всей audit Closure. Они не требуют принимать unvalidated current ERef.
Все substantive original C constraints G01/G02 остаются active/exact; inactive
исторические K1/K2/S1/S2 не назначаются current ради прохождения тестов.

**Порядок:**

1. Сначала в allowlisted F1 test file заменить прежнюю T2 characterization/equality
   с baseline CURRENT на нормативный expected INVALID/REF_MISSING. Обновить T5
   comparison и комментарии, чтобы не сохранять старый CURRENT как approved oracle.
   Не удалять T2, T1/T3/T4 или воспроизводимые input graphs; старые отчёты не менять.
2. Добавить current Creative R3 и historical-only controls. Запустить targeted F1
   tests **на неизменённом production source**. Сохранить red: как минимум T2 и
   Creative R3 обнаруживают actual CURRENT вместо INVALID; history controls должны
   исключать ложный fix «reject every audit ERef». Это expected development failures,
   не PASS baseline и не waiver.
3. Только затем минимально исправить production guard. Повторить тот же набор:
   green, без skips/expectedFailure, подмены assertions или ослабления expected states.
4. Сохранить все существующие **10 literal currentness vectors** byte-for-byte и
   их результаты, G01/G02 scenarios, старые foundation/records/resolver/provenance
   vectors. Проверить detachment/no mutation и отсутствие нового I/O.

Для каждой положительной и valid-history отрицательной fixture сначала требовать
resolver/provenance PASS. Не назначать outcomes вместо вызова checker. Для missing/
corrupt графов зафиксировать реальные существующие codes. CURRENT не доказывает
execution, facts, права, выбор/согласование или production readiness.

## 5. Обязательные тестовые команды и exit evidence

В project `.venv`, Python из окружения (не устанавливать зависимости/менять harness):

```bash
.venv/bin/python -m unittest tests.test_story_intelligence_currentness_eref_f1 -v
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_resolver*.py' -v
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_provenance*.py' -v
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_currentness*.py' -v
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v
.venv/bin/python -m unittest discover -s tests -v
```

Первый command нужен отдельно для red и green. Остальные запустить после fix.
Исторический **Codex-reported** F1 baseline: 5 F1 / 36 currentness / 139 SI / 981 full,
raw и outer exits 0; новые regression cases увеличат фактическое количество.
Не выдавать baseline counts за новый запуск. Указать OS/Python, exact commands,
counts, failures/errors/skips, durations и **отдельно raw Python и outer exits**.
Ожидаемый итог после fix: все final commands exit 0, zero failures/errors/skips.

Raw stdout/stderr сохранять без фильтра вне repo; child status явно печатать и
передавать outer process через sys.exit(returncode). Нет pipe masking, `|| true`,
harness/CI/environment fixes или подавления failures. OK + nonzero exit →
REVIEW_BLOCKED_EVIDENCE, не PASS. Недоступную проверку честно пометить ограничением,
не считать fix принятым. Linux PASS не Windows native qualification.

## 6. RESULT, публикация и STOP будущего FIX

Новый FIX_RESULT должен содержать exact supplied base/branch, причину и минимальный
diff, red/green actual results, таблицу ordinary/Creative actual/historical/original C
cases, graph/context hashes и accepted resolver/provenance checks. Зафиксировать
все final suite counts/exits/durations, unchanged literal vectors, ограничения и
отсутствие новых contract gaps либо конкретный BLOCKED_CONTRACT.

Перед commit проверить exact parent/base, strict three-file allowlist, diff/check,
links и byte identity всех остальных файлов. Опубликовать только новую fix branch,
проверить full commit SHA = remote HEAD, source branch HEAD и clean worktree.
Final SHA сообщить в handoff, не пытаться встроить self-referential hash в RESULT.
Никаких PR, merge, release, main изменений или independent acceptance от самого агента.

**STOP после публикации для независимого review.** SI-E02, RFC/role-map, ERef adapter,
operation execution, persistence/protected writes не начинать. `PUBLISH_REVISION`
DISABLED; partial COMMIT reconstruction OFF; Windows S3.2b BLOCKED_HOST_NOT_PROVIDED.

**Текущая публикация этих двух документов — только подготовка: FIX НЕ ЗАПУСКАТЬ.**
