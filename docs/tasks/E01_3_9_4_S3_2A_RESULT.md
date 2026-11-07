# E01.3.9.4 / S3.2a — Portable Python LAB Core

Дата: 2026-11-06. Qualification: **PURE_ONLY / S3_2A_PORTABLE_TESTED**.
Итог: все перечисленные acceptance runs прошли; Windows qualification не присваивается.

## Основание и traceability

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Base: `8967e858916bc7884e03c01aff33d5a2b7079612`, branch
`docs/editorial-e01-3-9-4-s3-2a-digest-erratum` (FETCH_HEAD совпал).
Output: `feat/editorial-e01-3-9-4-s3-2a-portable-lab-core-resume`.
Final HEAD сообщается в handoff после commit/push: self-reference SHA в содержимом
собственного commit невозможен. `git rev-parse HEAD` воспроизводит полный SHA.

Предыдущий точный STOP сохранён в Git:
[210229308eb0293f4003c26d4c4e4e51ca18065d](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/commit/210229308eb0293f4003c26d4c4e4e51ca18065d).
Этот файл заменён по прямому разрешению resume handoff. Его прежнее содержимое
доступно в указанном commit; история не переписана.

[Erratum](E01_3_9_4_S3_2A_DIGEST_ERRATUM.md) имеет узкий приоритет над separator
example первоначального [task](E01_3_9_4_S3_2A_CODEX_TASK.md).
[Owner decision](E01_3_9_4_S3_2A_OWNER_DECISION.md) разрешает portable stage без VM.
S3.1a exact source: `cf70b8c0a93841f2bff272b584a2106374e3016f`;
review: `818551171d1e955cf1dca6ddaf8cc54994c7528c`;
approved S1a: `83ac4ac3fa5104a9a43bc2fa5f98d735a694f49c` (S1b owner approval).
Existing source revisions: S2 wire `c91c7b30ff64ce9f83702f3ecd4b2a2c92ca3335`,
transaction/D-01 `21b1f06c1560ff65e6dc9c47ac9a972e5a3f2879`.
E00/A/O/D/S1/S2 и golden bytes не менялись.

## Файлы и API

Ровно исходный allowlist: шесть новых Python files и один обновлённый result.
| File | Bytes | Git blob SHA | SHA-256 |
|---|---:|---|---|
| `editorial/windows_lab/__init__.py` | 108 | `8c3c4faf00f64a79c3ca6ddadc568d7ca3c87f1e` | `15efb775d6ae69493b3955c26be54f4bd0a9b2f04214aa2019fe43568a6e31c2` |
| `editorial/windows_lab/protocol.py` | 10920 | `7fd4443d7b5f05327ef8249847dabbadc0299386` | `9576e5cf26dd6f2dec3f9121f59f298c2aef874057b3b973f91ee049139ed1a7` |
| `editorial/windows_lab/fixtures.py` | 38733 | `31f71411e51fd98e460c424c38a0f34c27b739fe` | `953ccb6aeb3dee1a490f32c92ffd4bcebaafc1d459d8c95020ab61e40d6b5469` |
| `editorial/windows_lab/dispatcher.py` | 8896 | `fc1779af5d1bb1c6a5d6486dd3cba58b7a1518da` | `a50a76f38a5a80c7c0dfb33b4836e1a26024a27b502928b28412d5242d24fd40` |
| `tests/test_windows_lab_protocol_v1.py` | 10329 | `594f9d4312dc4cc35433854c946cabe5fcc0bdd8` | `a2d1cf1b8d2fc1d0a6182bb351aebc260e127c5d78249c5768e899f204e9fe06` |
| `tests/test_windows_lab_dispatcher_v1.py` | 17595 | `84a2224ee0ab033cb9a3fc3d124902a05a62a1be` | `1c85ee39555a65534f8140873fa0d3f81d914ed2bca75234890a3fed2060a00a` |

Result: `docs/tasks/E01_3_9_4_S3_2A_RESULT.md` (updated). Его blob/hash вычисляются после финального текста через `git hash-object` / `sha256sum`; полный HEAD и result blob сообщаются в handoff без self-reference.

- `protocol.encode_lab(value)` / `decode_lab(frame)` проверяют закрытые LAB/1
  schemas и canonical bytes. `SSLB` + uint32_be length; header проверяется до
  slicing/parsing body. Root добавляет один контейнер к прежнему S1 depth64;
  S1 decoder/validator не ослаблен. Request budget 1048576, EXECUTE1052672,
  остальные виды4096; no duplicate/unknown/missing/coercion/floats/BOM/surrogates.
- `Factory(incarnation, policy_case, fault_case)` — фиксированный synthetic case,
  17 policies/17 probes, UUIDv5 finite roles/slots. Все probes распознаются под всеми
  policies; cross-grant отказ после whitelist match — LAB_POLICY_DENIED.
  Закрытая MockPolicy содержит A rights и пустые B rights; policy SHA не является
  real authority. Image bound128KiB, candidate blobs256KiB, bundle bound16MiB.
- `Dispatcher(run_id, incarnation, policy_case, fault_case).dispatch(frame, Caller)`
  получает immutable trusted synthetic Caller от harness. JSON не назначает caller,
  policy или fault. `execute_frame` — только trusted finite-fixture helper, не API
  удалённого клиента. Внешний ввод — bytes; closed wrapper не раскрывает Receipt.
- Один nonblocking RAM writer lock; busy/stall — детерминированная pure simulation.
  Native queue2/workers4/time deadlines не реализованы и не квалифицированы.
- На admission используется прежний TransactionModel/VirtualStore с явно injected
  fixture authority; minimal frozen authorization не заменяет current policy lookup.
  Genesis/publication plan builders адаптированы из прежних S2 synthetic tests,
  не копируют S1 codec или S2 execution/recovery engine. Искусственный package seed
  перенесён из существующего S2 `package_image`; production UUID и его references/
  content hashes пересчитываются existing editorial APIs. Runtime от tests не зависит.
- On-demand seeds ограничены actor/probe; они не materialize 64×17 histories.
  Seed initialization events отделены от client admission events. Whitelist preview
  не означает разрешения команды; denied cells не добавляют events к seed history.

## Семантика и доказательства

Digest: `SHA256(prefix + bytes([0]) + exact_internal_receipt_bytes)`.
Синтетический discriminator R={} совпал с erratum:
`66c044a3fa04b1baa95c05de618167622684843f04c4dde11e70add46870bcea`.
Четырёхбайтовый вариант даёт
`8acda446a8aae48decc364502a3b476565fd8e9b3048a950ce6c5ec2e4854e25` и не равен
правильному digest. Отдельный тест повторяет независимое вычисление на фактическом
canonical internal S1 Receipt с проверенным MAC. Сам Receipt наружу не возвращается.

Три literal S3.1a byte oracles: HELLO159/header53534c420000009f,
HELLO_RESULT357/header53534c4200000165, ACK195/header53534c42000000c3;
полные буквальные JSON, lengths, headers и утверждённые SHA сравниваются независимо
от encode/decode. ACK hash относится к response JSON, не frame или S1 MAC.

Terminal summary возможен только после S2 verified replay/terminal/final head,
канонической Receipt schema и MAC verification. При неподтверждённом terminal proof
возвращается frozen MOCK_PENDING без summary, incarnation карантинируется; повтор
не вызывает модель. W0 rejection без events не занимает admission slot. Никакой
fabricated terminal outcome, восстановления или скрытого writer adapter.

Replay хранит exact request bytes + synthetic actor + exact result bytes.
LOOKUP проверяет actor, stored bytes hash и ID; digest не является авторизацией.
Same-ID bytes/session/principal conflict — до новой модели. Нет denied-cache growth.
32 admissions включают pending/abort; 33-й новый ID отказывается без eviction,
known replay/lookup продолжаются. Старый incarnation — UNKNOWN_AFTER_RESTART;
old Request с новым incarnation — whitelist denial. Никаких persisted tombstones.

Faults: все 13 closed FaultCase покрыты, включая NONE, PREPARE/INTENT pause,
pre-admission deny/stall, response loss и synthetic crash before/after final.
Pending prefixes replay/lookup не запускают recovery. Impersonation/token-named
faults означают исключительно harness denial branch; Windows behavior не имитируется
как доказанный факт. Для verified ABORT отдельный test инжектирует отмену policy на
существующей S2 W4 boundary, не вводя новый wire fault enum.

## Команды и результаты

Linux x86_64, проектная `.venv`, Python **3.12.14**, stdlib only, CPU-only.
Команды из repository root, временные stdout/stderr logs находятся вне Git:

```text
.venv/bin/python -m unittest tests.test_windows_lab_protocol_v1 -v
.venv/bin/python -m unittest tests.test_windows_lab_dispatcher_v1 -v
.venv/bin/python -m unittest tests.test_storage_protocol_v1 tests.test_storage_transaction_model_v1 tests.test_storage_recovery_adversarial_v1 -v
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -m compileall -q editorial/windows_lab tests/test_windows_lab_protocol_v1.py tests/test_windows_lab_dispatcher_v1.py
git diff --check
git diff --cached --check
git status --short
git rev-parse HEAD
```

| Run | Tests | Result | Time / exit |
|---|---:|---|---|
| LAB protocol | 10 | OK | 0.023 s / 0 |
| LAB dispatcher | 19 | OK | 828.894 s / 0 |
| Existing storage suites | 169 | OK | 181.847 s / 0 |
| Full discovery | 837 | OK | 1001.624 s / 0 |

Существующий S2.3 вывод:1659 параметризованных scenarios, включая исходный D-01.
Это не дополнительные unittest methods и не Windows/LAB native cases.
Большое время dispatcher run связано с полной повторной верификацией 32-step
истории в неизменённой S2; производительность будущего broker не квалифицирована.

Матрицы/сценарии (subTests не выдаются за дополнительные unittest methods):

- 12×12 GD: 144 cells, 12 allow /132 LAB_POLICY_DENIED; denied events/admissions/
  model_calls неизменны.
- 5 CG cases×6 operation classes:30 cells; CG_INIT3, MIGRATE1, RECOVERY1,
  WRITER_ONLY/NONE0. Missing writer и operation grant проверяются независимо.
- 17 policies×17 probes:289 ID recognition checks и289 B denials.
- PUBLISH_REVISION denied под всеми17 policies. Unknown selectors/schema fields
  не становятся trusted context. 32 REJECT transactions затем33rd denial.
- Three byte oracles3/3; NUL discriminator и actual Receipt; replay/lookup,
  changed session/principal/full bytes, lost ACK/response, restart, pending и verified
  ABORT проверены independently expected states/bytes, а не только round-trip.

Разработческие прогоны до финальных изменений прерывались; они не учитываются как успешная acceptance-проверка. В ходе разработки исправлены локальные ошибки fixture production-ref rebinding и
передачи ReceiptBody вместо whole Receipt в validator. Они не требовали изменений
S1/S2 или трактовки контрактов. Итоговые failures/скips фиксируются в таблице выше;
нативные проверки не подменяются pure test guards.

## LT01–LT15 / RISK

| ID | Доказательство S3.2a и оставшаяся граница |
|---|---|
| LT01 | BLOCKED native install/cleanup, вне scope |
| LT02 | BLOCKED native SCM lifecycle, вне scope |
| LT03 | BLOCKED SID/ACL/native masks |
| LT04 | BLOCKED native server authentication/squatting |
| LT05 | BLOCKED impersonated SID/SQOS/remote/handoff |
| LT06 | BLOCKED native impersonation/RevertToSelf; только pure deny hooks |
| LT07 | PURE subset: strict buffers/schema/length/depth/UTF-8; at-limit buffer route и over-limit-before-parse. Нет Win32 one-message/WriteFile/EOF доказательства |
| LT08 | BLOCKED native workers/cancellation/deadlines; pure lock/busy hooks только |
| LT09 | PURE subset:144 grant cells; не native authentication |
| LT10 | PURE subset:CG/B/missing-grant/disabled-command cases |
| LT11 | PURE subset:exact replay/lookup/conflicts/lost ACK simulation |
| LT12 | PURE subset:synthetic crash/new incarnation unknown; нет process-kill durability |
| LT13 | PURE subset:32/33 quota, no eviction/denial growth, no extra model events |
| LT14 | PURE subset: runtime guards reject selected file/network/subprocess calls; native independent attempted-write observer BLOCKED |
| LT15 | PURE subset:S2/golden/D-01 unchanged regressions, independent Receipt rejection и digest check; native wrapper/transport BLOCKED |

RISK-01/03 **BLOCKED native**. RISK-02: pure buffer bound subset, native large
WriteFile/4096-buffer/deadline/cancellation **BLOCKED**. RISK-04: pure request identity/
lookup/replay subset проверен; OS identity binding **BLOCKED**. Ни один LT не объявлен
полностью native PASS. Нет Windows HostProfile/EvidenceIndex/native trace hashes.

## Ограничения и STOP

Нет OS authentication/ACL/Win32/SCM/pipe/native IO/DPAPI/protected writer,
persistence/backup или production authority. Synthetic principals/32-byte public
fixture key и policy/declarations — только RAM test data. Внешний caller выбирается
trusted harness, не Windows token. Python-private members не являются security
boundary против кода в том же процессе. Runtime IO guards — ограниченные pure checks,
не независимый аудит OS writes. Нет Windows power-loss/process qualification.

PUBLISH_REVISION **DISABLED**, partial COMMIT reconstruction **OFF**.
Нет новых dependencies, реальных keys/SIDs/passwords, media или тяжёлых binaries.
Уровень только PURE_ONLY; LAB_SERVICE_TESTED/PROCESS_QUALIFIED/POWER_LOSS_QUALIFIED
**не получены**. Native S3.2b и S3.3 не начаты. Main/PR/merge/release не изменялись.
После publication — **STOP для независимой проверки**.

## Проверяемые hashes логов pure runs

Временные логи находятся вне Git; это не native Windows evidence.

| Log | SHA-256 |
|---|---|
| `s32a-protocol-final.log` | `3c258a1518be36bb6ec6d0a1b033fc24fb8bd8c91aeeefc531f1267a0d7a74ff` |
| `s32a-dispatcher-verified.log` | `06d6d0ded04e4b45654e077dd1549532051b887309bfad8a79f025e707949b70` |
| `s32a-storage.log` | `139f9ebbdc03022816996386a50d5d070a48bd22b004be74e1cf749dc421d2a0` |
| `s32a-full-verified.log` | `7b484f5ab61b4e06deb8c78ea5614039746215699c48d9974147f0642ea45ce7` |

## S3.2a-R1 · 2026-11-07

База `c61d82591ec37d1285672f599180aa0c7fa2125c`, HEAD ветки
`docs/editorial-e01-3-9-4-s3-2a-independent-review`. Ветка исправления
`fix/editorial-e01-3-9-4-s3-2a-cold-admission-guard`. Итоговый SHA публикуется
в передаче результата, поскольку запись SHA внутри собственного коммита циклична.
Результаты выше относятся к первоначальной реализации.

### S32A-R01

На базовом коде четыре новых теста дали 15 отказавших проверок: перехватчик
`TransactionModel.execute` обнаружил вызов seed до возврата отказа. Входные
кадры подготовлены отдельным экземпляром dispatcher/Factory. Целевой Factory
не прогревался построением тестовых кадров.

`Factory.candidate()` теперь строит точный шаблон и входные данные чистым
вычислением. Для холодного non-genesis запроса ссылка на ожидаемый terminal head
вычисляется через S1 journal MAC для трёх фиксированных записей synthetic genesis.
При построении шаблона не создаётся VirtualStore и не выполняются операции S2.
Dispatcher сравнивает полные канонические байты и проверяет live grants, квоту,
карантин, pre-admission fault и fixture authority до `Factory.materialize()`.
При допуске холодного запроса Factory выполняет исходный seed неизменённым S2
и сверяет реальный head с ожидаемым. Startup seed отделён от клиентского вызова
и не расходует квоту. Если S2 отклоняет команду до первого события, новое
хранилище не сохраняется. Lookup и точный replay возвращаются до подготовки кандидата.

Изменённые пути и Git blob SHA исходников:

| Path | Blob SHA |
|---|---|
| `editorial/windows_lab/dispatcher.py` | `940614d8e55a5a5c2cdec49a309d58133fe58116` |
| `editorial/windows_lab/fixtures.py` | `a681603403f0d16c3b68ebe95aac979dbee4fb98` |
| `tests/test_windows_lab_dispatcher_v1.py` | `108bbe007fe735df8c9f6890121cc879b658b6d7` |
| `docs/tasks/E01_3_9_4_S3_2A_RESULT.md` | В дереве итогового коммита |

### Проверки R1

Среда: Windows 10 IoT Enterprise LTSC 2021, build 19044, Python 3.12.10 AMD64.
Исходный checkout восстановлен из дерева точного коммита через GitHub API.
Проверены 314 blob SHA, Git tree SHA и SHA базового объекта commit.
Для полного discovery использованы pytest 9.2.0 и реальный FFmpeg 9.0.2 из
изолированного тестового каталога. Зависимости проекта и CI без изменений.

| Команда или проверка | Результат |
|---|---|
| `python -m unittest -v` с четырьмя новыми cold-denial методами на исходном коде | 4 теста, 15 сбоев проверок до исправления, exit 1 |
| `python -m unittest -v` с пятью новыми методами, W0 rejection, CG matrix, replay/LOOKUP и PREPARE/INTENT pending | 9 OK, 10.830 с, exit 0 |
| `python -m unittest tests.test_storage_protocol_v1 tests.test_storage_transaction_model_v1 tests.test_storage_recovery_adversarial_v1 -v` | 169 OK, 291.209 с, exit 0. S2.3: 1659 параметризованных сценариев |
| `python -u -m unittest discover -s tests -v` | 842 выполнено, 841 OK, 1 failure, 0 skipped, 824.871 с, exit 1. Все 34 LAB-теста прошли, включая 32/33 и три byte oracles |
| `python -m unittest -v tests.test_sprint23_2.Sprint232Tests.test_env_override` на точной базе | Тот же failure, exit 1 |
| `git diff --check` | Exit 0 |

Отдельный первоначальный LAB-прогон выявил сохранение пустого store при
W0 rejection. После переноса сохранения к регистрации допуска этот тест
прошёл в целевом и полном прогонах. Единственный failure финального discovery
вне LAB: `test_sprint23_2.Sprint232Tests.test_env_override` ожидает POSIX-разделители,
а Windows возвращает путь с обратными слешами. Ошибка воспроизведена на точной базе.

SHA-256 логов R1 вне Git:

| Log | SHA-256 |
|---|---|
| `s3-red.log` | `d83205d40973c2c8b5824ff50e9c3ef258ef952e0f215137b57b70b79bf53890` |
| `s3-targeted-final.log` | `9d1127862b00d75ee398d5fc60d85208dd61ee358e5ba01598d9584d6d482312` |
| `s3-storage.log` | `a2566992ebd26bb1215524e6300e9a9bc1f43f28dc12416e3eff726f5344f714` |
| `s3-discovery-final.log` | `e92a4ba1a73be0a7135d0c44bba74851178aa22dd86649fd15a5eb39390fc76a` |

В тестах холодного отказа перехватчик проверяет отсутствие любых вызовов
`TransactionModel.execute`, включая временные seed stores. Проверены B,
cross-policy A, CG_WRITER_ONLY, CG_NONE, отсутствие writer/operation/gate grant,
семь denial/stall hooks и crash-before-admission, карантин и несовпадение
reason/session при известном request ID. В проверке квоты после 32 реальных
RAM admissions временно меняется доверенный gate grant, чтобы новый холодный
probe дошёл до `LAB_CAPACITY`. Сохранённые replay и LOOKUP возвращают исходные
байты. Матрица GD дала 12 allow / 132 deny, матрица CG охватила 30 ячеек.

Дополнительное сравнение с базой по SHA-256 охватило 578 холодных EXECUTE
кадров (17 policies × 2 principals × 17 probes, slot 0) и 20 пар разрешённых
EXECUTE/RESULT, включая четыре последовательных GD_SCRIPT_REJECT. Обе
выборки совпали, SHA-256 файла сравнения
`1d192d12240be5cc0af6c750ec3ed75b88bfd286524bd4b5b8a2874099d8c4bd`.

### Квалификация R1 и STOP

Проверки относятся к `PURE_ONLY`. Windows native LT03–LT06/08/14, OS identity,
ACL, SCM/pipe и protected writer вне квалификации. S1/S2, D-01 и golden vectors
в исходном виде. После публикации требуется независимое ревью S32A-R01.
**STOP.**
