# S3.2a-R1 — Acceptance evidence and Windows baseline triage

Дата проверки: 2026-11-09 (Europe/Kyiv). Qualification: **PURE_ONLY**.
Рекомендация: **READY_FOR_INDEPENDENT_ACCEPTANCE — только PURE_ONLY**.

## 1. База, ветка и нормативные основания

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Exact base / проверяемый R1: `13ed35db93e05641631ad3fa4a0d2ea3475c6719`.
Source branch: `fix/editorial-e01-3-9-4-s3-2a-cold-admission-guard`.
Evidence branch: `test/editorial-e01-3-9-4-s3-2a-r1-acceptance-evidence`.
До начала работы такой ветки локально и на origin не обнаружено. Она создана
непосредственно от exact base, не от main. Final HEAD сообщается в handoff после
commit/push; self-reference в собственном документе не используется.

Проверены [independent review](E01_3_9_4_S3_2A_INDEPENDENT_REVIEW.md),
[исторический RESULT с дополнением R1](E01_3_9_4_S3_2A_RESULT.md),
[LAB contract](E01_3_9_4_S3_1A_LAB_EXECUTION_CONTRACT.md),
[owner decision](E01_3_9_4_S3_2A_OWNER_DECISION.md),
[S1b](E01_3_9_2B_S1_APPROVED_CONTRACT.md) и существующие S1/S2 API/tests.
LAB contract идентичен `cf70b8c0a93841f2bff272b584a2106374e3016f`;
approved S1 source — `83ac4ac3fa5104a9a43bc2fa5f98d735a694f49c`.
NUL erratum сохраняет один байт00. PUBLISH_REVISION DISABLED;
partial COMMIT reconstruction OFF. S3.2b/S3.3 не разрешены этой проверкой.

## 2. Diff исходного R1

Immediate pre-R1: `c61d82591ec37d1285672f599180aa0c7fa2125c`.
Предыдущая implementation revision: `b27a084c99510406c407d5785328a31eb5f1df94`;
между ней и R1-parent добавлен только independent review.

`git diff 13ed35d^ 13ed35d`: четыре файла,276 insertions/46 deletions:
`editorial/windows_lab/dispatcher.py`, `editorial/windows_lab/fixtures.py`,
`tests/test_windows_lab_dispatcher_v1.py`, `docs/tasks/E01_3_9_4_S3_2A_RESULT.md`.
Проверен сам diff, не только RESULT. `git diff 13ed35d^ 13ed35d --check` — exit0.
Нет изменений approved contracts, protocol.py, S1/S2 или их tests/golden.

R1 разделяет pure `candidate()` и stateful `materialize()`. Предсказанный seed head
вычисляется через существующий S1 journal MAC codec; это построение bytes, не
исполнение W0–W9. При разрешённом materialize существующая S2-модель исполняет seed,
а фактический stable head сравнивается с expected_head клиентского fixture Request.
`retain()` вызывается после model outcome; ранний W0 rejection без events не
сохраняет временный пустой store. Исправление здесь повторно не выполнялось.

## 3. S32A-R01: source review и независимый probe

Порядок `_dispatch`: existing ID/replay → whitelist location → pure candidate и
полное byte match → live grants → quota → quarantine → pre-admission fault →
independent frozen authority → materialize → model execution → retain/result.
`candidate()` не создаёт VirtualStore/TransactionModel, не вызывает execute и не
сохраняет images/stores. Его чтение существующей истории не является recovery.
Builder конструирует только synthetic dictionaries/bytes и S1 MACs.

Кроме обязательных unittest запущен отдельный временный `cold_probe.py` вне Git.
Входные frames получены отдельным helper instance; target исходно имеет `_stores={}`.
Перехвачены **оба** `TransactionModel.execute` и `VirtualStore`, а на отказах также
`Factory.materialize`: любой вызов приводит к AssertionError. Probe подтвердил:

- Все17 probes проходят `candidate()` без S2 execute/store allocation; stores пусты.
- B, cross-policy A, CG_WRITER_ONLY и CG_NONE:4 cold denials, LAB_POLICY_DENIED.
- READ_STALL, DISPATCH_STALL, PRE_ADMISSION_DENY:3 cold denials без materialize.
- Altered reason/session:2 cold byte-mismatch denials, LAB_FIXTURE_NOT_ALLOWED.
- Quarantined cold target:LAB_BUSY без allocation/events/admissions.
- Разрешённый cold GD request:ровно2 execute — seed и клиентская команда;
  MOCK_FINALIZED,1 admission. Replay и LOOKUP byte-identical без execute/materialize.

Дополнительно `cold_differential.py` выполнен в обоих checkout: на pre-R1 тот же
cold B request обнаружил1 попытку execute(INITIALIZE_EMPTY), перехваченную до её
исполнения; на R1 ответ DENIED/LAB_POLICY_DENIED,0 execute,0 admissions,0 stores.
Команды: `$PY /workspace/work/s32a-r1-acceptance/cold_differential.py 0` в R1,
и абсолютный тот же Python/script с аргументом1 в pre-R1 cwd. Аргумент — ожидаемое
число intercepted calls diagnostic probe, не изменение какого-либо теста проекта.

Это 17 candidate checks,10 cold-denial checks и один positive/replay probe;
это дополнительные проверки, не новые committed unittest methods.

## 4. Матрица инвариантов

| Инвариант | Проверка / наблюдение | Результат |
|---|---|---|
| candidate без S2 seed effects | Source + independent execute/VirtualStore traps,17 probes | PASS PURE |
| Authorization раньше materialize | Source + cold policy/missing-grant tests и independent materialize trap | PASS PURE |
| Нет скрытого execute на cold denial | Отдельный helper; target не прогрет; original R1 tests инструментируют и seed execute | PASS PURE |
| Denial не создаёт events/admissions | Counters, `_stores`, events до/после | PASS PURE |
| Authorized cold startup проверен | Unchanged S2 seed execution + actual_head equality; independent2-execute probe | PASS PURE |
| W0 reject не сохраняет пустой store | `test_preflight_frozen_failure_never_admits`, source early return до retain | PASS PURE |
| Replay/LOOKUP не строят историю | Cached exact bytes; independent execute/materialize traps | PASS PURE |
| 32/33, replay после cap | 32 real GD_SCRIPT_REJECT admissions +33rd refusal, no eviction; cold-probe quota test | PASS PURE |
| Quarantine до materialize | Dedicated cold test + independent trap; pending prefix tests | PASS PURE |
| 144 GD cells | Exact12 allow/132 deny assertions; no model effects на132 denials | PASS PURE |
| CG/B/disabled command | 30 CG cells, B cases, independent missing grants, PUBLISH_REVISION denial | PASS PURE |
| NUL separator / byte oracles |10 protocol tests + actual Receipt discriminator в dispatcher tests | PASS PURE |
| S1/S2/D-01/golden unchanged | Byte diff +169 existing storage tests | PASS PURE |

Cold-probe quota branch использует доверенную подмену gate grant в test harness,
чтобы другой cold probe дошёл до LAB_CAPACITY. Это изолированная проверка порядка
ветвлений; она не утверждает поддержку реального runtime policy-update API или
Windows authorization. Native admission/timing/IO этим не квалифицируются.

## 5. Среда, команды и результаты

Фактически: Linux x86_64, kernel6.18.57, glibc2.41, Python3.12.14,
проектный `/workspace/Story-Studio-RU-UA-WORK/.venv/bin/python`.
Зависимости/CI/исходники/tests не менялись. Suites выполнялись отдельными процессами;
длительные прогоны дождались завершения. Временные logs/metadata вне Git:
`/workspace/work/s32a-r1-acceptance/`.

Команды из root R1 checkout, `PY=.venv/bin/python`:

```text
$PY -m unittest tests.test_windows_lab_protocol_v1 -v
$PY -m unittest tests.test_windows_lab_dispatcher_v1 -v
$PY -m unittest tests.test_storage_protocol_v1 tests.test_storage_transaction_model_v1 tests.test_storage_recovery_adversarial_v1 -v
$PY -m unittest tests.test_sprint23_2.Sprint232Tests.test_env_override -v
$PY -m unittest discover -s tests -v
$PY /workspace/work/s32a-r1-acceptance/cold_probe.py
```

| Run (Linux3.12.14) | Tests | Result | unittest seconds / exit |
|---|---:|---|---|
| Protocol |10|OK|0.032 /0|
| Dispatcher |24|OK|766.373 /0|
| Storage |169|OK|263.433 /0|
| env_override R1 |1|OK|0.001 /0|
| Full discovery | 842 | OK | 938.355 /0 |

S2.3 отдельно напечатал1659 параметризованных сценариев, включая исходный D-01.
Они не прибавляются к unittest method count; повтор в полном discovery не является
новым набором уникальных scenarios. Native Windows LT01–LT15 не запускались. Длительность dispatcher run —
измерение pure verification model; это не подтверждение native deadlines.

## 6. Windows baseline: независимый differential triage

Классификация: **BASELINE_PLATFORM_FAILURE** — прежняя зависимость test assertion
от представления пути. Native Windows повтор этой сессии **BLOCKED**: разрешённый
Windows executor не предоставлен. Linux и PureWindowsPath evidence различаются.

Опубликованный R1 RESULT сообщает Windows10 IoT Enterprise LTSC2021/build19044,
Python3.12.10 AMD64:842 tests/841 OK/1 failure, exit1. Это **предыдущий отчёт**, не
наблюдённая нами Windows-среда или самостоятельно проверенные private Windows logs.
Его failure не переименован в PASS и не исключён из истории.

Для независимого сравнения создан detached worktree вне repository:

```text
git worktree add --detach /workspace/work/s32a-r1-acceptance/pre-r1 c61d82591ec37d1285672f599180aa0c7fa2125c
```

В нём и на R1 с тем же абсолютным интерпретатором запущен исходный
`-m unittest tests.test_sprint23_2.Sprint232Tests.test_env_override -v`.
Дополнительно в каждом cwd выполнен:

```text
/workspace/Story-Studio-RU-UA-WORK/.venv/bin/python /workspace/work/s32a-r1-acceptance/baseline_probe.py
```

Probe не меняет expected или исходник теста. Только в отдельном процессе временно
подставляет `scripts.voice_studio.Path = pathlib.PureWindowsPath`, затем запускает
тот же unittest и сохраняет его **FAIL**. Это semantic emulation только одного
path conversion, не Windows OS/platform execution.

| Checkout | Native Linux unit | Native actual `--model-path` | PureWindowsPath unit |
|---|---|---|---|
| pre-R1 c61d825 |1 OK,0.001s, exit0 | `/custom/v5_cis_base_nostress.pt` |1 FAIL,0.001s |
| R1 13ed35d |1 OK,0.001s, exit0 | `/custom/v5_cis_base_nostress.pt` |1 FAIL,0.001s |

Неизменённый expected: `/custom/v5_cis_base_nostress.pt`.
В обоих semantic probes actual: `\custom\v5_cis_base_nostress.pt`.
Внешний probe exit0 означает, что **ожидаемый diagnostic failure воспроизведён**,
а не что исходный unittest прошёл. Windows version такого probe отсутствует:
он выполнен на Linux/Python3.12.14.

Git blobs до R1 / на R1 совпадают:

- `tests/test_sprint23_2.py`: `5aa5dc884f7225ddd12ef63963566c8b6b5152c9`;
- `scripts/voice_studio.py`: `d30ed3c01acb4947c7a890a9a455cd46c3d509e9`.

Причина: функция строит `str(Path(STORY_SILERO_MODEL))`, а assertion требует
буквальный POSIX string в argv. Windows path flavor меняет separators. R1 меняет
только LAB, его test и RESULT; функция и тест не зависят от LAB. Доказательств
storage/LAB regression от этого path mismatch нет; isolated byte-identical source
и повторённая path semantics подтверждают baseline provenance.

Рекомендуется отдельная ограниченная cross-platform задача: уточнить проверку
семантики override-пути и проверить её на Linux/Windows, сохранив production
поведение и trusted-model guard. В текущем задании ни тест, ни expected, ни функция
не исправлялись. Native Windows rerun остаётся открытым evidence item, не blocker
для честно ограниченной PURE_ONLY передачи на независимую приёмку.

## 7. Сохранность и applicability gate

R1 diff и текущая QA-ветка не меняют S1/S2/D-01/golden, approved decisions,
dependencies или CI.169 storage tests реально запущены; actual Receipt MAC/NUL и
три literal byte oracles проверяются существующими LAB tests. Нет нового writer,
production keys/registration, native Windows API или ослабления grants/limits.

Реестр прочитан через `git show`, без merge/cherry-pick:
`docs/external-ideas-adoption-register` /
`4ad198a095b155a57d6d0b162fc977260119962b`,
`docs/architecture/EXTERNAL_IDEAS_AND_ADOPTION_REGISTER.md`.
Applicability gate 2026-11-09, exact R1 base: **применимых кандидатов нет**.

| ID | Applicability для R1 QA |
|---|---|
| EXT-01 VidRusher | Media/proxy/clip proposals; storage acceptance вне области |
| EXT-02 WanGP | Future shot/take/workflows/GPU adapter; не разрешает storage change |
| EXT-03 LTX-Desktop | Production UX/providers/availability; не применимо к этим инвариантам |
| EXT-04 Humanizer | Draft narration rules RU/UK; не применяется к byte/authority protocol |

Все четыре остаются CANDIDATE; новых OWNER decisions по интеграции нет.
Никакой внешний код, зависимости, модели или корпуса не перенесены. Реестр не
редактировался; этот gate не является license/adoption approval.

## 8. Итог и границы

**READY_FOR_INDEPENDENT_ACCEPTANCE (PURE_ONLY).** S32A-R01 подтверждён на pre-R1
и не воспроизводится на exact R1; все обязательные suites в доступной среде
завершились exit0. Новых дефектов в проверенном объёме не обнаружено.
Windows baseline классифицирован BASELINE_PLATFORM_FAILURE с явным ограничением
нативной перепроверки; отдельное platform-тестовое исправление следует оформить
отдельной задачей. Это рекомендация передать evidence на независимую приёмку,
а не самостоятельное утверждение следующего этапа.

PURE_ONLY не даёт LAB_SERVICE_TESTED/PROCESS_QUALIFIED/POWER_LOSS_QUALIFIED.
Windows SCM/SID/ACL/impersonation/named pipes/protected writes и power-loss tests
вне этой работы. Новых production capabilities нет. RISK-01/03 и native RISK-02
BLOCKED, RISK-04 покрыт только portable subset. Native Windows baseline повтор
тоже BLOCKED; опубликованный Windows failure остаётся failure.

Создан только этот новый документ. Source/tests исправления R1 сохранены как есть.
PR/merge/release/main не изменяются. После publication — **STOP**;
следующий шаг определяет владелец после независимого review. S3.2b/S3.3 не начаты.

## 9. SHA-256 logs (вне Git)

| Log (вне Git) | SHA-256 |
|---|---|
| `cold-pre.log` | `e1899c01815db4f23359e68566b19572eb989f0696aa40658f8541f7ee1ecd6f` |
| `cold-probe.log` | `675ced020f7e08dfed57f0d7a70bee410bd24ec0eb73ab8f8d7535047f4e916c` |
| `cold-r1.log` | `90014fd55e857c1da4dae874f31762bf5584be5dae0db5b041b267e45e93c914` |
| `dispatcher.log` | `586b127e5f43d4e331eace4e5046f93b4a707918e6e207160029d42215efe8b8` |
| `env-pre.log` | `e796f04c4f1fa92b3835b9c56bea0d67aee37c4c5e230f15892bcc630184e609` |
| `env-r1.log` | `e796f04c4f1fa92b3835b9c56bea0d67aee37c4c5e230f15892bcc630184e609` |
| `full.log` | `524e2712fceb89fcf063df7efe5645c4c6eea94ebe7c082663ccd22e15d23102` |
| `path-pre.log` | `1a1d261be6ccfc6b66824d14c484d99a70993a79fc9cd246b5db6bf58a897dab` |
| `path-r1.log` | `0c89574e5d35ec77d0c99587c9ca7c35f770c2d0a50a407d7906141bfe25cf88` |
| `protocol.log` | `9ffee22ef3a84171067ca91c7c39c1a6d2626fd0fb138e6c6e0e2e32256ffe33` |
| `storage.log` | `c8ae15ec84a730e44fd96cad36e45ce73d1d9f28c15e5bc5f494e3a5a37e3019` |

Командные metadata (`protocol.json`, `dispatcher.json`, `storage.json`,
`env-r1.json`, `full.json`) сохраняют argv, cwd, exit, wall-clock elapsed и log hash.
Для baseline probes исходники временных диагностических scripts сохранены в той же
директории вне Git. SHA логов emulation сохраняет исходный FAIL, не скрывая его.
