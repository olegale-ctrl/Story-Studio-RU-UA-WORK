# E01.3.9.4 / S3.1a — Windows Lab Execution Contract

**PROPOSAL — НЕ УТВЕРЖДЁН. Дата: 2026-11-06. Только проектирование.**
Ни служба, ни accounts/ACL/pipe, ни implementation этим документом не создаются.
Приведённые параметры — конкретная рекомендация для L-01–L-04, а не решение
владельца. S3.2 требует независимого review и отдельного approval exact revision.

## 0. Нормативная база и scope

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Base branch: `docs/editorial-e01-3-9-4-s3-1-review-s3-2-lab-gate`.
- Exact base: `c3f65c5253c5e02be17fcf8676f280e6e83d9e63`.
- Branch: `docs/editorial-e01-3-9-4-s3-1a-lab-execution-contract`.
- [Independent S3.1 review / lab gate](E01_3_9_4_S3_1_INDEPENDENT_REVIEW_AND_S3_2_LAB_GATE.md):
  S3.1 complete, mechanisms PROPOSAL, implementation NOT AUTHORIZED.
- [S3.1](E01_3_9_4_S3_1_WINDOWS_STORAGE_SPEC.md),
  [D1–D12](E01_3_9_1B_APPROVED_ARCHITECTURE_DECISION.md),
  [approved S1b](E01_3_9_2B_S1_APPROVED_CONTRACT.md) и exact approved S1a
  `83ac4ac3fa5104a9a43bc2fa5f98d735a694f49c` остаются неизменными.
- E00/A/O, S2.1–S2.4/golden vectors и D-01 binding не пересматриваются.
  GitHub policy берётся из отдельного `ceca15c20cedd5277ad0bdafc418eef149e7bc7b`.

Lab contract — отдельный transport/test protocol **LAB/1**, не новая S1 version.
Внутренний Request проверяется прежним S1 codec; внешние tags/SDDL/limits не
добавляются в editorial snapshot, S1 Request, Receipt или authority evidence.
Нет upload, file-path/handle transfer, review-session creation endpoint, real
registration, production writer, DPAPI, key provisioning, operational backup или
production authority evaluation. `PUBLISH_REVISION` **DISABLED**; partial COMMIT
reconstruction **OFF**. CPU-only/offline, RU/UK (`ru`/`uk`), без media/models.

## 1. L-01 profile — изолированная установка и идентичность

### 1.1 Фиксированные имена и допустимые locations

| Объект | Предлагаемое точное значение |
|---|---|
| SCM service name | `StoryStudioBrokerLab` |
| Display name | `Story Studio S3.2 LAB — NO PRODUCTION STORAGE` |
| Local service account | `SSLabBrokerSvc` (отдельная account, не LocalSystem/production identity) |
| Service SID account name | `NT SERVICE\StoryStudioBrokerLab` |
| Client accounts | `SSLabClientA`, `SSLabClientB`: standard users |
| Outsider account | `SSLabDenied`: standard user, не член client group |
| Local client group | `SSLabClients`: только A/B, не Everyone/Users/Administrators |
| Pipe | `\\.\pipe\StoryStudioBrokerLab.v1` |
| Installer/runtime root | `%ProgramFiles%\StoryStudioLab\S3_2` |
| Lab config/fixture root | `%ProgramData%\StoryStudioLab\S3_2` |
| Private harness evidence | `%ProgramData%\StoryStudioLab\S3_2\Evidence` |
| Mutable store | Только RAM; нет directory, journal, anchor, key или lock files |

Значения known folders разрешает elevated installer, не caller. Запрещены junction/
reparse/UNC/removable/synced/shared roots и collision с production paths. Preexisting
одноимённый account/service/root/pipe не переиспользуется: installation abort для
review, без takeover. Credential provisioning будущего lab account выполняется
администратором, credentials не входят в manifest/log/Git. Account получает только
Log on as a service, с запретом interactive/remote-interactive/batch/network logon.
A/B/Denied не получают service logon или admin membership.

Рекомендация: own-process service, SERVICE_SID_TYPE_RESTRICTED, exact required
privilege list `SeChangeNotifyPrivilege`; без SeDebug/SeBackup/SeRestore и без
автоматического SeImpersonatePrivilege. Identification-level impersonation должна
пройти tests §4; failure не включает привилегию или UNRESTRICTED автоматически.
Service SID и service-account TokenUser — разные SID и проверяются раздельно
([SERVICE_SID_INFO](https://learn.microsoft.com/en-us/windows/win32/api/winsvc/ns-winsvc-service_sid_info)).
SCM загружает account profile, но lab не использует его для DPAPI/ключей
([Service user accounts](https://learn.microsoft.com/en-us/windows/win32/services/service-user-accounts)).

### 1.2 Runtime SID bindings и manifest

Реальные Windows SID нужны только для ephemeral test accounts, а не production
reviewers. Это runtime identity transport; mock principals §6 — отдельные
синтетические значения. В Git нет настоящих host/user SIDs или passwords.

В SDDL ниже placeholders означают **полные SID strings**, не имена accounts:

- `{SA}` — LookupAccountNameW local `SSLabBrokerSvc`.
- `{SV}` — LookupAccountNameW `NT SERVICE\StoryStudioBrokerLab`.
- `{CG}` — SID local `SSLabClients`.
- `SY`, `BA`, `AN`, `NU` — SDDL aliases SYSTEM, Builtin Administrators,
  Anonymous и Network. Не подставлять реального пользователя вместо service.

Installer проверяет существование/тип, local provenance и различность SA/SV/CG,
сохраняет bindings в read-only private lab manifest. Неразрешённый placeholder,
невалидный SID или несовпадение token/SCM/manifest — startup/client failure.
Dictionary key/account display name не доказательство identity (аналог D-01).

Закрытая декларативная schema, все поля обязательны, unknown fields запрещены:

```text
LabInstallManifest = {
  lab_install_version:1, scope:"STORY_STUDIO_S3_2_LAB", run_id:UUID,
  service_name:"StoryStudioBrokerLab", service_account:"SSLabBrokerSvc",
  service_account_sid:SID, service_sid:SID, client_group_sid:SID,
  client_a_sid:SID, client_b_sid:SID, denied_sid:SID,
  pipe_name:"\\.\pipe\StoryStudioBrokerLab.v1",
  install_root:AbsoluteLabPath, config_root:AbsoluteLabPath,
  host_profile_sha256:Hex, runtime_files_sha256:Hex,
  fixture_set:"S32_FIXTURES_1", fixture_case:FixtureCase,
  access_profile:"LAB_ACL_1", limits_profile:"LAB_LIMITS_1"
}
```

UUID/Hex — прежний canonical format; SID проверяется Windows SID APIs. Paths —
только expanded exact roots таблицы, verified owner/volume/file identity, не
произвольные absolute paths. Manifest ≤64 KiB, depth ≤8, строки ≤1024 code points,
без floats/duplicate keys/surrogates, canonical JSON. FixtureCase определён §6.
Hash manifest и runtime files pin-ятся installer/test harness перед run. Не читать
конфигурацию/fixture-case из CLI client, environment или IPC; mutable service state
не объявляется третьим protected head. Patch manifests требует stop/restart и
нового evidence run, не runtime policy command.

Binary/runtime целиком installer-owned и read-only для service/client. Кандидат
ImagePath — quoted private `Runtime\python.exe` и private `Bin\lab_service.py`;
runtime `_pth` допускает только private stdlib + Bin, без `import site`, user paths,
`.pth`/current-directory loading. Bytecode writes отключены. Exact artifacts,
hashes/runtime version должны быть выбраны до S3.2; не системный Python/PATH.
Никаких subprocess/model/network dependencies runtime.

### 1.3 Cleanup и допустимые административные writes

Только будущий elevated installer/harness создаёт lab binaries/config/accounts/
SCM registration, ACL и private evidence. Это **не** protected editorial writes.
Service hot path не пишет regular files даже в lab root; Windows/SCM internal
telemetry не считается broker storage и не используется для восстановления.
Никаких installer/runtime действий этим documentation task не выполняется.

Cleanup: прекратить admission → STOP → дождаться exit → при timeout зафиксировать
failure и завершить только pinned lab process (PID + creation identity + SA/SV),
не процесс по имени/PID alone. DeleteService только если name/ImagePath/account/SID
совпадают с manifest. Pipe исчезает после закрытия всех handles, не удаляется как
файл. Удалить только созданные этим run accounts/group с exact SID/LSA rights.
Файлы удаляются только по allowlist install manifest, с повторной проверкой roots/
reparse, без recursive traversal чужого дерева. Private evidence сначала сохраняет
harness согласно L-04; затем lab VM можно revert. Production service/config/keys/
roots никогда не перечисляются для очистки. Preexisting objects не удаляются.

## 2. LAB_ACL_1 — точные descriptors и access masks

SDDL templates ниже — данные для будущего утверждения, не исполняемый installer.
SID substitutions выполняются installer/service из verified manifest; canonical
owner/DACL/ACE semantics сверяются через GetSecurityInfo, не по строковому alias.
`D:P` означает protected DACL; G/SACL здесь не задаются и не используются как
identity/authorization. Не принимать дополнительные inherited allow ACEs.

### 2.1 Named pipe

```text
O:{SA}D:P(D;;0x001F01FF;;;AN)(D;;0x001F01FF;;;NU)(A;;0x001F01FF;;;SY)(A;;0x001F01FF;;;{SA})(A;;0x001F01FF;;;{SV})(A;;0x00120083;;;{CG})
```

| Mask | Exact meaning |
|---|---|
| `0x001F01FF` | FILE_ALL_ACCESS: server/system only, включая FILE_CREATE_PIPE_INSTANCE |
| `0x00120083` | SYNCHRONIZE `0x00100000` + READ_CONTROL `0x00020000` + FILE_READ_ATTRIBUTES `0x80` + FILE_READ_DATA `0x1` + FILE_WRITE_DATA `0x2` |
| Excluded client bits | FILE_CREATE_PIPE_INSTANCE / FILE_APPEND_DATA `0x4`, DELETE, WRITE_DAC, WRITE_OWNER, GENERIC_WRITE/ALL |

Client CreateFile desired access **ровно 0x00120083**, OPEN_EXISTING, share mode 0,
non-inheritable handle, SECURITY_SQOS_PRESENT + SECURITY_IDENTIFICATION +
SECURITY_CONTEXT_TRACKING (`dwFlagsAndAttributes=0x00150000`), без delegation/overlapped в этом варианте.
Если API на выбранном Windows profile требует иных rights, это failed gate, а
не разрешение добавить GENERIC_WRITE. Последний включает pipe-instance bit
([Named pipe security](https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-security-and-access-rights)).

Server: PIPE_ACCESS_DUPLEX; first instance open-mode `0x00080003`
(FILE_FLAG_FIRST_PIPE_INSTANCE), subsequent instances `0x00000003`.
Pipe mode `0x0000000E` = MESSAGE + READMODE_MESSAGE + REJECT_REMOTE_CLIENTS + WAIT.
Max instances 4, in/out buffers 4096 bytes, WaitNamedPipe default 5000 ms.
Buffers не являются payload limits. Первый handle удерживается весь service
lifetime и переиспользуется через DisconnectNamedPipe; server не закрывает его
ради выдачи чужому creator нового «первого» instance.

**Client остаётся в default byte-read mode.** Он не вызывает
SetNamedPipeHandleState: для duplex документация этого API требует GENERIC_WRITE,
что конфликтует с исключением create-instance bit. Ответы читаются по lab framing
§3, а server читает message-mode boundaries. Это намеренная рекомендация L-02,
не claim, что specific mask эквивалентен GENERIC_WRITE
([SetNamedPipeHandleState](https://learn.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-setnamedpipehandlestate)).

### 2.2 SCM, process/token и filesystem descriptors

| Объект | Exact template |
|---|---|
| Service object | `O:BAD:P(A;;0x000F01FF;;;SY)(A;;0x000F01FF;;;BA)(A;;0x00020005;;;{SA})(A;;0x00020005;;;{SV})(A;;0x00020005;;;{CG})` |
| Broker process | `O:{SA}D:P(A;;0x001FFFFF;;;SY)(A;;0x001FFFFF;;;BA)(A;;0x001FFFFF;;;{SA})(A;;0x001FFFFF;;;{SV})(A;;0x00121000;;;{CG})` |
| Broker primary token | `O:{SA}D:P(A;;0x000F01FF;;;SY)(A;;0x000F01FF;;;BA)(A;;0x000F01FF;;;{SA})(A;;0x000F01FF;;;{SV})(A;;0x00020008;;;{CG})` |
| Lab install/config directory tree | `O:BAD:P(A;OICI;FA;;;SY)(A;OICI;FA;;;BA)(A;OICI;FRFX;;;{SA})(A;OICI;FRFX;;;{SV})(A;OICI;FRFX;;;{CG})` |
| Private Evidence directory | `O:BAD:P(A;OICI;FA;;;SY)(A;OICI;FA;;;BA)` |

Service CG mask `0x00020005` = READ_CONTROL + SERVICE_QUERY_CONFIG `1` +
SERVICE_QUERY_STATUS `4`: **не** START/STOP/CHANGE_CONFIG. SCM connection handle
client просит только SC_MANAGER_CONNECT `1`; existing SCM DACL не ослабляется.
Process CG mask `0x00121000` = READ_CONTROL + SYNCHRONIZE +
PROCESS_QUERY_LIMITED_INFORMATION `0x1000`; нет VM_READ/WRITE/DUP_HANDLE/TERMINATE.
Token CG mask `0x00020008` = READ_CONTROL + TOKEN_QUERY `8`; нет DUPLICATE,
IMPERSONATE/ADJUST. Token objects не поддерживают SYNCHRONIZE.

Client token querying не считается default Windows permission: service до
открытия endpoint устанавливает и проверяет указанные process/token descriptors
на собственных objects. Нет нужных WRITE_DAC/owner rights → startup FAIL, не
SeDebug escalation. Grant TOKEN_QUERY раскрывает только test token metadata
назначенной lab client group; такой grant production service этим не утверждается.
Ограничения documented в [Process rights](https://learn.microsoft.com/en-us/windows/win32/procthread/process-security-and-access-rights),
[Token rights](https://learn.microsoft.com/en-us/windows/win32/secauthz/access-rights-for-access-token-objects),
[OpenProcessToken](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocesstoken),
[Service rights](https://learn.microsoft.com/en-us/windows/win32/services/service-security-and-access-rights).
SDDL грамматика: [Security descriptor strings](https://learn.microsoft.com/en-us/windows/win32/secauthz/security-descriptor-string-format).

## 3. LAB/1 transport — закрытый bounded protocol

### 3.1 Framing и connection state

Каждая frame: ASCII **SSLB** (4 bytes) + uint32_be(N) + ровно N bytes C_lab(object).
Нет MAC/journal trailer. Magic намеренно не SSJ1 и не S1 JSON. C_lab совпадает с
UTF-8/sorted-key/no-whitespace integer-preserving JSON rules, но применяется к
новым закрытым Lab types. Outer depth ≤65; вложенный S1 Request отдельно проверяет
свои depth ≤64, text/bytes/enum limits неизменённым S2.1 API. Duplicate keys,
floats/NaN/Infinity, BOM, surrogates, coercion и unknown fields запрещены на обоих
уровнях. Request byte length — len(C(S1 Request)), не весь lab envelope.

| Limit profile LAB_LIMITS_1 | Предлагаемое значение |
|---|---:|
| S1 Request bytes | 1..1048576 (прежний S1 bound) |
| Lab HELLO/LOOKUP/ACK JSON bytes | 1..4096 |
| Lab EXECUTE JSON bytes | 1..1052672 (S1 +4096 envelope budget) |
| Любой response JSON bytes | 1..4096 |
| Client frames / connection | 2: один HELLO/EXECUTE/LOOKUP, затем один ACK |
| Server frames / connection | 1 |
| Pipe instances / IO workers | 4 / 4, отдельный worker для каждого handle |
| Mock dispatcher / queue | 1 / 2 queued jobs, без unbounded thread pool |
| Client-admitted requests / incarnation | 32, включая aborts; no eviction |
| Request slots / fixture actor/probe | 0..63 |
| Fixture image / total startup fixture bundle | ≤128 KiB / ≤16 MiB |

До прочтения kind принять только header N≤1052672; после decode применять более
строгий kind bound. Zero/oversized length отклоняется до allocation body. Client
пишет целую frame **одним WriteFile**, OS message содержит ровно одну frame.
Server собирает ERROR_MORE_DATA только внутри того же OS message; message boundary
не совпал с header length, trailing bytes или два frames в message → close/no admit.
Нельзя собирать один request из двух OS messages или искать следующий SSLB.

Client byte-read получает header/body exact lengths. Server отвечает одним OS
message/frame. Client проверяет body/type/run/incarnation/correlation, затем
посылает отдельный ACK frame. Server проверяет ACK/SID и disconnect; client до
принятия результата дожидается EOF и отвергает trailing bytes. EOF может быть
BROKEN_PIPE/PIPE_NOT_CONNECTED. Не менять client handle read mode ради этой проверки.
HELLO connection закрывается; EXECUTE/LOOKUP используют **новое** соединение и
заново проверяют server identity. Один connection не принимает два EXECUTE.

ACK подтверждает только получение конкретных lab response bytes, **не** durable
storage/approval. Его отсутствие не откатывает RAM engine. Unread pipe data могут
быть discarded при DisconnectNamedPipe; поэтому disconnect после verified ACK,
либо timeout/unknown delivery, а не обещание доставки одного WriteFile
([DisconnectNamedPipe](https://learn.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-disconnectnamedpipe)).
Никакого FlushFileBuffers на файлах/volume или pipe как durability barrier.

### 3.2 Client schemas

Ниже декларативные schemas, все поля required. `Scope` — literal
`STORY_STUDIO_S3_2_LAB`; UUID/Hex canonical; unknown tags/extra/missing fields denied.

```text
LabHello = {lab_version:1, scope:Scope, kind:"HELLO", run_id:UUID, nonce:UUID}
LabExecute = {lab_version:1, scope:Scope, kind:"EXECUTE", run_id:UUID,
              incarnation_id:UUID, request:existing S1 Request}
LabLookup = {lab_version:1, scope:Scope, kind:"LOOKUP", run_id:UUID,
             incarnation_id:UUID, request_id:UUID, request_bytes_sha256:Hex}
LabAck = {lab_version:1, scope:Scope, kind:"ACK", run_id:UUID,
          response_sha256:Hex}
```

`request_bytes_sha256` = plain SHA256(C(S1 Request)); это не domain-separated S1
Request digest. Server также сравнивает полные bytes и authenticated synthetic
principal, не только hash. ACK.response_sha256 = plain SHA256(exact response JSON
bytes), не hash header, не HMAC и не proof trust. ACK от другого SID, для другого
response/run или второй ACK → close; не ещё одна engine operation.

### 3.3 Server schemas и невозможность production receipt

```text
LabHelloResult = {lab_version:1, scope:Scope, kind:"HELLO_RESULT", run_id:UUID,
  incarnation_id:UUID, nonce:UUID, limits_id:"LAB_LIMITS_1",
  fixture_set:"S32_FIXTURES_1", fixture_case:FixtureCase, lab_only:true}
LabResult = {lab_version:1, scope:Scope, kind:"RESULT", run_id:UUID,
  incarnation_id:UUID, request_id:UUID|null, request_bytes_sha256:Hex|null,
  outcome:LabOutcome, mock_admission:NONE|RAM|UNKNOWN,
  mock_summary:MockSummary|null, error:LabError|null, lab_only:true}
MockSummary = {operation:enabled S1 Operation, status:INITIALIZED|COMMITTED|ABORTED_PRECOMMIT|REPAIRED,
  virtual_record_count:U64, value_sha256:Hex}
LabError = {code:LabErrorCode, field_path:ASCII path <=1024, s1_code:S1 ErrorCode|null}
```

LabOutcome — ровно MOCK_FINALIZED, MOCK_ABORTED, MOCK_PENDING, DENIED,
NOT_ADMITTED, UNKNOWN_AFTER_RESTART. NONE/RAM/UNKNOWN — строки, не bare JSON tokens.
LabErrorCode — ровно LAB_POLICY_DENIED, LAB_S1_REJECTED, LAB_FIXTURE_NOT_ALLOWED,
LAB_IDEMPOTENCY_CONFLICT, LAB_BUSY, LAB_CAPACITY, LAB_NOT_FOUND, LAB_RESTART_UNKNOWN,
LAB_ENGINE_FAILURE, LAB_RUN_MISMATCH. Эти labels **не** добавляются в S1 ErrorCode.
Unrecognized native/internal error не сериализуется arbitrary message/code.

- MOCK_FINALIZED/MOCK_ABORTED: mock_admission RAM, summary non-null, error null;
  internal S2 receipt должен иметь verified terminal/final anchor в **RAM**.
- MOCK_PENDING: summary null, mock_admission RAM либо UNKNOWN; error null либо
  LAB_ENGINE_FAILURE. Никогда не success или durable state.
- DENIED/NOT_ADMITTED: mock_admission NONE (только отклонённые bytes этой попытки), summary null,
  error non-null. Это не отменяет старый уже admitted request с тем же ID.
- UNKNOWN_AFTER_RESTART: mock_admission UNKNOWN, summary null,
  error LAB_RESTART_UNKNOWN; прошлый outcome неизвестен, не объявлен aborted.
- HELLO не содержит model outcome/admission; nonce буквально echo проверенного
  HELLO, run_id берётся из manifest, incarnation_id — только service startup.

`value_sha256 = SHA256(ASCII("story-studio-s3-2-lab-result-v1") || byte 00 || R)`,
где R — exact canonical **internal** S1 Receipt bytes, || — concatenation.
Prefix заканчивается ровно одним NUL, без LF/backslash escape bytes. Это новый
lab digest, не S1 MAC/digest.
Сам Receipt, его MAC, key_id, head, approval evidence и journal не экспортируются
в IPC. Внешний LabResult не проходит S1 Receipt decoder, а из summary нельзя
извлечь S1 signature/MAC. Публичный synthetic key S1 §13 — только RAM fixture,
никогда не provisioning/default/fallback production key. Нет endpoint raw receipt
или dump store. Ни `lab_only`, ни имя pipe сами по себе не являются authentication.

Production client обязан pin production service/endpoint identity и не иметь
fallback на lab. При negative production-profile test: имя lab запрещено,
SA/SV не production identities, SSLB/wrapper не S1 wire; результат rejected **до**
интерпретации mock result. Фактическая production integration вне lab scope;
reference production-verifier test не считается квалификацией отсутствующего
production binary. Даже при ошибочной маршрутизации в lab внешнего S1 Receipt нет.

### 3.4 Restart/idempotency — без скрытой persistence

HELLO возвращает свежий service-generated UUID incarnation на каждом startup.
run_id — постоянный approved lab-run ID, nonce — synthetic client correlation ID.
Использовать случайный UUID для process identity не означает генерацию ключа.

Fixture request/session IDs вычисляются **только** approved factory §6 с namespace
текущей incarnation. Любой EXECUTE/LOOKUP со старой incarnation →
UNKNOWN_AFTER_RESTART без model call. Old request, переупакованный с новой
incarnation, не совпадает с current fixture whitelist → LAB_FIXTURE_NOT_ALLOWED,
не новый admission. Отсутствуют persistent tombstones и «восстановленный» receipt.
Клиент не выбирает новый ID для automatic retry неизвестного старого outcome.

В одной incarnation map только для RAM-admitted requests удерживает principal +
exact request bytes + frozen result до конца incarnation. Denied/not-admitted IDs не резервируются/не добавляются
в ledger; ошибки не создают unbounded cache. Same request/principal/content → тот же lab
result JSON **byte-for-byte** (mock_admission RAM описывает исходный virtual request,
а не второй admission), без нового summary/virtual event. Different content,
principal/session → deny/conflict до новых model events. Identity/read-scope lookup
предшествует раскрытию результата. Live mock-policy change не делается через IPC;
accepted intent replay использует frozen fixture context. LOOKUP только читает
этот RAM map, не запускает execute/recovery заново. Unknown current-whitelisted ID
→ LAB_NOT_FOUND/NOT_ADMITTED; non-whitelisted ID → denied, не обещание старого outcome.

### 3.5 Synthetic byte examples (LAB only, не S1 golden vectors)

Следующие JSON строки — exact canonical UTF-8 без конечного LF. Это примеры
формата, не состоявшийся Windows exchange и не реальные account/run IDs.

**HELLO:**

```json
{"kind":"HELLO","lab_version":1,"nonce":"b2222222-2222-4222-8222-222222222222","run_id":"a1111111-1111-4111-8111-111111111111","scope":"STORY_STUDIO_S3_2_LAB"}
```

**HELLO_RESULT:**

```json
{"fixture_case":{"fault_case":"NONE","policy_case":"CG_NONE"},"fixture_set":"S32_FIXTURES_1","incarnation_id":"c3333333-3333-4333-8333-333333333333","kind":"HELLO_RESULT","lab_only":true,"lab_version":1,"limits_id":"LAB_LIMITS_1","nonce":"b2222222-2222-4222-8222-222222222222","run_id":"a1111111-1111-4111-8111-111111111111","scope":"STORY_STUDIO_S3_2_LAB"}
```

**ACK:**

```json
{"kind":"ACK","lab_version":1,"response_sha256":"812089bdaef8791dd8127ca21bd771e65c48d5c78a41577c125af38f7604f119","run_id":"a1111111-1111-4111-8111-111111111111","scope":"STORY_STUDIO_S3_2_LAB"}
```

| Object | JSON bytes N | Header hex | Full frame bytes | Plain JSON SHA-256 |
|---|---:|---|---:|---|
| HELLO | 159 | `53534c420000009f` | 167 | `b6b3da12fd7423f404ccf700476499c4af9e3a9ba84a6716a02e0ce8b78cdccf` |
| HELLO_RESULT | 357 | `53534c4200000165` | 365 | `812089bdaef8791dd8127ca21bd771e65c48d5c78a41577c125af38f7604f119` |
| ACK | 195 | `53534c42000000c3` | 203 | `ad5152df65e4b22d874736635590a422c780024046598df3fa22deacd7b716d2` |

ACK.response_sha256 совпадает с SHA-256 HELLO_RESULT JSON, а не frame bytes.
S1 tests/golden values не меняются; примеры проверяются отдельно как pure bytes.

## 4. Token identity, server authenticity и fail-stop

### 4.1 Client checks до любого HELLO/private fixture

На **каждом connection**:

1. Открыть только literal lab pipe; выполнить GetSecurityInfo(READ_CONTROL),
   сверить owner SA и exact expanded DACL/protection с manifest.
2. GetNamedPipeServerProcessId → OpenProcess с `0x00121000`, удерживать handle;
   QueryServiceStatusEx/QueryServiceConfigW сверяют service name, PID, own-process
   account, ImagePath. Не доверять приветствию/PID/process filename alone.
3. QueryFullProcessImageNameW + pinned immutable runtime/package hash; process
   creation identity/live state. OpenProcessToken `0x00020008`, TokenUser == SA,
   TokenGroups содержит enabled SV и TokenRestrictedSids содержит SV. Проверить
   отсутствие неожиданного broader account/profile, не читать secret buffers.
4. Повторно проверить pipe server PID, SCM PID и process liveness перед send;
   при restart/PID reuse/невозможности query — disconnect, не fallback.

F: PID можно получить через
[GetNamedPipeServerProcessId](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getnamedpipeserverprocessid),
а OpenProcessToken требует PROCESS_QUERY_LIMITED_INFORMATION
([документация](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openprocesstoken)).
Легитимный server SID/runtime скомпрометированным admin не защищается этим lab.
HELLO.run/nonce/incarnation — correlation после OS checks, не серверный credential.

### 4.2 Server checks каждого complete message, включая ACK

До decode/engine admission: ImpersonateNamedPipeClient проверяется на success;
OpenThreadToken(TOKEN_QUERY, OpenAsSelf=TRUE) → TokenType=Impersonation,
TokenImpersonationLevel=SecurityIdentification **ровно**, TokenUser SID валиден и
равен одному из manifest A/B. Anonymous, NETWORK SID, другие/неопознанные SIDs,
AppContainer/unsupported token context — deny/close. SID не извлекается из JSON,
username, PID, environment или manifest label вместо фактического token.
Reference client включает dynamic context tracking
([CreateFileW SQOS](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew));
LT05 передаёт открытый A handle в controlled Denied process и проверяет отказ
по native sender context. Deliberate delegation static authenticated handles
разрешённым principal вне baseline protection; сервер не выдаёт client-supplied
tracking flag за доказательство human identity.
Каждое message аутентифицируется по последнему прочитанному **тому же OS message**;
не читать следующий до capture/revert. ACK SID должен равняться request SID.

Существующий mapping actual A/B SID → synthetic principal выполняется только после
этих checks. Pipe CG membership позволяет connect, а не Command/Gate grants.
ClientB проходит transport auth, но mock policy обычно не разрешает операции.

F: при неудаче impersonation продолжение могло бы выполняться под service context;
поэтому ни один запрос не исполняется
([ImpersonateNamedPipeClient](https://learn.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-impersonatenamedpipeclient)).
При identification level ниже SecurityImpersonation API документирует отдельный
путь допустимости; это основание пробовать профиль без SeImpersonatePrivilege,
а не Windows acceptance result. SecurityAnonymous/Impersonation/Delegation в этом
рекомендованном lab profile не принимаются даже если SID можно прочитать.

В finally всегда проверенный RevertToSelf, затем OpenThreadToken должен вернуть
ERROR_NO_TOKEN. Только после этого trusted dispatcher получает immutable authn
record. False/exception revert, residual/непроверяемый token → **немедленный
fail-stop всего service process**, закрытие endpoint, без response/engine call/
error-recovery work на impersonated worker. Не TerminateThread и не swallow exception.
Native fail-stop не выполняет Python logging/finalizers под чужим token; внешний
harness наблюдает exit. Это следует безопасной реакции
[RevertToSelf](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-reverttoself).
При impersonation failure также надо доказать restoration/no thread token; иначе
тот же fail-stop. Credential/context leakage между workers не допускается.

## 5. LAB_LIMITS_1 — deadlines, concurrency, cancellation

Все значения ниже **предлагаемые lab test parameters L-02**, не Q1 и не production
profile. Wall clock не определяет request ordering; deadlines — monotonic process time.

| Параметр | Предложение | По истечении |
|---|---:|---|
| Client WaitNamedPipe/connect | 5000 ms | Local unavailable; no admission; no endpoint fallback |
| Complete request/HELLO/LOOKUP frame | 5000 ms с первого byte, не sliding | Close, no response/model call |
| Server identity checks | 5000 ms | Client disconnect до send |
| Queue wait до RAM admission | 2000 ms | LAB_BUSY, mock_admission NONE |
| Mock dispatcher execution | 10000 ms | No final summary unless frozen final result proven; quarantine incarnation, stop admission, unknown/pending delivery |
| Response write / ACK read | 5000 ms отдельно | Delivery unknown; result map не откатывается |
| Client EOF после ACK | 1000 ms | Result не считается transport-validated; retry/lookup original ID |
| IO cancellation completion grace | 1000 ms | Fail-stop process, не thread reuse |
| Installer wait START / STOP | 30000 / 20000 ms | FAIL evidence; no automatic service recovery |
| Harness wait for forced process exit | 5000 ms | FAIL/BLOCKED; не kill произвольного нового PID |

4 IO workers не исполняют mutable model: только один dispatcher, одна bounded queue
(2 jobs). Service принимает максимум 4 clients; запрет pipelining/третьих client
messages и unbounded buffers/thread spawning. Capacity 32 admitted IDs включает
aborts, не eviction; reaching cap → LAB_CAPACITY до нового admission, повторные
lookups/known replies остаются доступны. Startup seeds не являются client requests.
Queued job expiry/cancellation и переход QUEUED→STARTED сериализованы одним
mutex: expired/removed job никогда не доходит до model. При 1 running +2 queued
четвёртый valid execute получает LAB_BUSY; 5-й connection дополнительно ограничен
pipe instance cap. No authentication failure response раскрывает существующий чужой request.

Dedicated synchronous IO worker имеет operation-generation ID и STOP_NEXT latch.
Supervisor вызывает CancelSynchronousIo для **этого** thread, не shared pool.
После cancel worker не начинает следующий IO до completion/cleanup; NOT_FOUND
не доказывает completion. Race cancel-before-call/call-completes-while-cancel
проверяется отдельно: повторные cancel только того же worker/generation в пределах
1000 ms, затем fail-stop. Buffer/thread/handle не переиспользуются раньше observable
completion. Cancellation сама по себе не синхронное доказательство, что IO остановлен
([Windows cancellation](https://learn.microsoft.com/en-us/windows/win32/fileio/canceling-pending-i-o-operations)).

10-second model timeout не прерывает Python thread посредине state transition:
incarnation карантинируется и процесс останавливается без выдачи fabricated result.
Late ACK/connection loss не превращает accepted RAM intent в ABORT. STOP прекращает
new admission, завершает/прекращает lab process в пределах stop policy; после
crash/restart RAM исчезает и применяется §3.4, не native disk recovery.
SCM automatic restart **NONE** в recommended profile: harness выполняет каждый
restart явно и записывает причину. Никакого sleep-and-pretend-success.

## 6. L-03 profile — mock fixtures и authorization injection

### 6.1 FixtureCase и principals

```text
FixtureCase = {policy_case:PolicyCase, fault_case:FaultCase}
PolicyCase = CG_INIT|CG_MIGRATE|CG_RECOVERY|CG_WRITER_ONLY|CG_NONE|
  GD_SCRIPT_APPROVE|GD_SCRIPT_REJECT|GD_SCRIPT_REVISE|GD_SCRIPT_REVOKE|
  GD_SCENES_APPROVE|GD_SCENES_REJECT|GD_SCENES_REVISE|GD_SCENES_REVOKE|
  GD_HANDOFF_APPROVE|GD_HANDOFF_REJECT|GD_HANDOFF_REVISE|GD_HANDOFF_REVOKE
FaultCase = NONE|IMPERSONATE_FALSE|THREAD_TOKEN_QUERY_FALSE|REVERT_FALSE|
  RESIDUAL_TOKEN|READ_STALL|DISPATCH_STALL|RESPONSE_LOSS|
  CRASH_PRE_ADMISSION|CRASH_AFTER_RAM_FINAL|PRE_ADMISSION_DENY|
  PAUSE_AFTER_RAM_PREPARE|PAUSE_AFTER_RAM_INTENT
```

FaultCase — compiled lab-only harness hooks, selected administrator in read-only
manifest **до startup**, один заданный fault на первой соответствующей точке этой
incarnation. Никакого DEBUG/fault activation через IPC. Native positive tests и
injected error-path tests размечаются отдельно; injection не доказывает occurrence
реального Win32 failure. Fault NONE не содержит test fault hook activation.
PAUSE_AFTER_RAM_PREPARE / PAUSE_AFTER_RAM_INTENT — synthetic S2 VirtualStore faults
после W3.anchor.flush / W4.INTENT.journal.flush, без termination native service.
Adapter ловит именно expected SimulatedCrash, сохраняет RAM prefix и caches
MOCK_PENDING (summary/error null, mock_admission RAM). Same-ID retry/LOOKUP только
возвращает этот pending result. Это не real crash recovery и не exposed recovery API.
CRASH_AFTER_RAM_FINAL, напротив, завершает service process после cache final result
до response; на restart этот cache утрачен и outcome неизвестен.

Mapping после OS authentication:

| Actual lab token SID | Mock principal (синтетический, не реальный SID reviewer) |
|---|---|
| Manifest client_a_sid | `windows-sid:S-1-5-21-1000-1000-1000-1001` |
| Manifest client_b_sid | `windows-sid:S-1-5-21-1000-1000-1000-1002` |
| Любой другой | Нет mapping; deny до model |

Нельзя связать произвольный caller SID с A/B по JSON `principal`, actor или client
name. A/B actual account SIDs и runtime token сведения не выводятся в LabResult;
в evidence используются aliases. Installed accounts не являются production
principals или настоящими grants. Admin token без A/B mapping не получает mock
editorial scope от install rights.

### 6.2 CommandGrant и все GateDecisionGrant

Mock provider принимает `(lab production, mapped principal, operation, gate,
decision)`; lookup/table/hash version берётся только из selected FixtureCase.
Synthetic authority policy и editorial policy различаются. Unknown principal,
production, provider, policy/version или scope → deny до model admission.
Synthetic PolicyRef: policy_version `lab-v1`, policy_id — UUIDv5 seed-role policy;
policy_sha256 — SHA256(C(MockPolicy)), где closed MockPolicy =
`{mock_policy_version:1,policy_case:PolicyCase,actor_a_command_grants:[CommandGrant],
actor_a_gate_grant:GateDecisionGrant|null,actor_b_command_grants:[],actor_b_gate_grant:null}`.
Значения A буквально из таблиц ниже; production scope — finite set текущих factory
productions этого actor. Это lab fixture metadata, не новый production policy format.
Для B table пустая во всех policy cases. Для A:

| PolicyCase | Exact command grants | Exact gate grant |
|---|---|---|
| CG_INIT | PROTECTED_SNAPSHOT_WRITE + INITIALIZE | null; только 3 S1 init/import/transfer operations |
| CG_MIGRATE | PROTECTED_SNAPSHOT_WRITE + MIGRATE_SCHEMA | null |
| CG_RECOVERY | PROTECTED_SNAPSHOT_WRITE + RECOVERY | null |
| CG_WRITER_ONLY | Только PROTECTED_SNAPSHOT_WRITE | null; не разрешает ни одну operation |
| CG_NONE | Пустой набор | null |
| Любой GD case | PROTECTED_SNAPSHOT_WRITE + RECORD_DECISION | Только одна пара из таблицы ниже |

| Case | Gate | Decision |
|---|---|---|
| GD_SCRIPT_APPROVE | SCRIPT | approve |
| GD_SCRIPT_REJECT | SCRIPT | reject |
| GD_SCRIPT_REVISE | SCRIPT | revise |
| GD_SCRIPT_REVOKE | SCRIPT | revoke |
| GD_SCENES_APPROVE | SCENES | approve |
| GD_SCENES_REJECT | SCENES | reject |
| GD_SCENES_REVISE | SCENES | revise |
| GD_SCENES_REVOKE | SCENES | revoke |
| GD_HANDOFF_APPROVE | HANDOFF | approve |
| GD_HANDOFF_REJECT | HANDOFF | reject |
| GD_HANDOFF_REVISE | HANDOFF | revise |
| GD_HANDOFF_REVOKE | HANDOFF | revoke |

Grant не наследуется от APPROVE, другого gate, draft edit или administrator.
PUBLISH_REVISION всегда denied, даже если fixture пытается добавить такой grant;
unknown CommandGrant token rejected, не превращается в allow-all.
Отсутствие PROTECTED_SNAPSHOT_WRITE или operation grant независимо закрывает путь.
Сформированный FrozenCommand содержит ровно minimal set approved S1 §5.2, не
весь policy table. Non-allowed lookup не строит permissive FrozenCommand.

### 6.3 Approved factory, model boundary и RAM-only assertions

`S32_FIXTURES_1` — allowlisted compiled factory, versioned/pinned вместе с S2.4 и
fixture-set hash в evidence. Это не import path/module name от client. Единственная
client variable — request из закрытого whitelist текущего case/incarnation/actor/probe.
Нет caller-supplied blobs, arbitrary JSON file, review confirmations или paths.
Factory даёт только synthetic seeded in-memory state и exact frozen fixture inputs:
empty initialization, unverified import/transfer, schema-1 migration, exact-head
repair C→H в RAM, одну decision pair для каждого gate/decision. Current-package /
human-review assertions явно injected, не извлекаются из реального SID как факт.
Нельзя маркировать mock confirmations как действительное human approval.

Для всех generated UUID-valued request/session/approval/event/epoch IDs используется
UUIDv5 с namespace=server incarnation и UTF-8 name:
`S32_FIXTURES_1/<policy_case>/<actor A|B>/<probe>/<slot 0..63>/<role>`.
Role request/session/approval/event использует slot из формулы. Для стабильных
production/machine/epoch/policy role используется literal `seed` вместо slot:
одна production actor/probe не меняется между slots. Role set закрыт этими 8 значениями.
Probe — INIT_EMPTY, IMPORT, TRANSFER, MIGRATE, RECOVERY или одно из 12 GD names.
Первые пять соответствуют пяти non-decision operations; GD probes соответствуют
RECORD_DECISION. У каждого actor/probe собственная RAM production/seed; общий
лимит 32 client admissions на incarnation. Все 17 probes распознаются factory
**при любом policy_case**, иначе cross-grant тест мог бы ложно пройти из-за
whitelist denial вместо authorization denial. LT09/LT10 требуют для такого случая
именно LAB_POLICY_DENIED. Factory перед model call не выводит grants из probe;
нельзя использовать positive-test helper, который выдаёт права по присланной operation.
Templates/seed bundle ≤16 MiB; candidate TransactionInput blob bytes суммарно
≤256 KiB. Generation конкретного candidate — pure bounded computation после
scope check, не заранее materialized 64×17 histories и не произвольный JSON builder.
UUIDv5 не security key и не источник verified decision order. Factory pin-ит
static text/timestamps/declarations, сохраняет exact Unicode; S1 digest/attestation
считаются прежними APIs. HELLO сообщает case/incarnation, поэтому reference lab
client может воспроизвести только approved template для своего actor/slot.
Для INIT_EMPTY/IMPORT/TRANSFER/MIGRATE/RECOVERY probes valid slot только 0;
для GD probes — 0..63 (для capacity test используются repeated REJECT decisions).
Slot разбирается через finite request-ID map, не произвольный input integer.
Native connection ID остаётся transport metadata; internal FrozenCommand connection
ID — явно synthetic fixture value из pinned S2 catalogue, не production auth proof.
Несовпадающие bytes для свободного ID → denied, не auto-build произвольного state.

Обязательный order dispatcher:

1. Authn + successful restoration → run/incarnation → bounded canonical envelope
   и strict S1 shape. Reserved PUBLISH_REVISION shape допускается только для
   lookup/denial, как в S1 §5.3, без dereference proposal.
2. Для existing request ID проверить principal/read scope и полные bytes **до**
   новых live scopes/CAS/fixture matching; changed bytes/session → conflict.
3. Для нового ID — bounded factory Request-template whitelist + mock grants + review/session/package
   fixture checks; только затем вызов unchanged pure model.
4. На pre-admission failure — **zero model W1/PREPARE/events/IDs**, current result
   denied/not-admitted; post-call uncertain error — no invented final receipt.
5. Проверить returned RAM terminal/anchor перед cache LabResult. Никакого native
   protected store adapter в dependency graph; изменение S2 не требуется.

При same-incarnation EXECUTE replay dispatcher возвращает cached LabResult bytes,
не вызывает повторно model.execute. LOOKUP не делает virtual recovery. Если
нужен recovery-oriented seed, он подготовлен factory/harness до обработки IPC и
не является exposed generic recovery command. На restart всё RAM state исчезает;
§3.4 требует UNKNOWN/whitelist denial, не автоматическое восстановление approvals.

**Запрет protected writes:** service runtime не вызывает regular-file create/write/
append/replace/delete, DPAPI/key IO, registry persistence, msvcrt writer locks,
network sockets, subprocess или native production writer. CreateFile только для
своих pipe handles / read-only pinned runtime/manifest/fixture reads; object DACL
на process/token/pipe — kernel object changes, не editorial filesystem writes.
Нет реальных `editorial.json`, journals/anchors/keys ни в production, ни в lab.
Installer/harness writes §1.3 отделены по process/phase и не маскируют runtime IO.

Private RAM trace содержит model phase и request alias, event count before/after;
harness отдельно наблюдает attempted filesystem write APIs и OS file IO по broker
и любым descendants (их создание само по себе FAIL). Любой forbidden attempt,
даже ACCESS_DENIED, проваливает gate. Недостаточное audit coverage → BLOCKED,
не «writes не замечены». Runtime logs — bounded RAM, evidence собирает внешний
admin harness, не service file logger. Production roots не открываются даже read-only.

## 7. L-04 profile — матрица и приёмка

### 7.1 Предлагаемый стенд, не production deployment profile

Рекомендация: isolated x64 Windows 11 Pro VM, 4 vCPU, 8 GiB RAM, 64 GiB virtual
local NTFS disk, CPU-only, offline, без shared host folders, production accounts/
data/keys, snapshots only для lab cleanup. Exact edition/version/full build+UBR,
hypervisor/runtime/artifacts обязаны быть заполнены и approved до coding/run.
Windows support/licensing не предполагаются по имени ISO.

Альтернатива: отдельная поддерживаемая Windows 10 Pro 22H2/ESU VM с теми же lab
ресурсами и pinned full build/UBR; ESU entitlement проверяется владельцем. Третья
альтернатива — две VM и одинаковая matrix; результат каждого profile отдельно.
One Windows 11 run не даёт Windows 10 label. Это lab execution choices, **не**
утверждение W11-N/W10-S/VM-F production profiles или Q1 из S1/S3.1.

Closed HostProfile (canonical JSON ≤16 KiB):

```text
HostProfile = {host_profile_version:1, profile_id:Label,
 os_edition:Label, os_version:Label, build:U32_positive, ubr:U32,
 arch:"x64", filesystem:"NTFS", storage_role:"ISOLATED_LAB_VM",
 vcpu:U32_positive, ram_mib:U32_positive, disk_mib:U32_positive,
 hypervisor:Label, runtime_version:Label, source_sha:GitSHA,
 adapter_artifact_sha256:Hex, test_artifact_sha256:Hex, observer_artifact_sha256:Hex}
```

Label — nonempty ASCII ≤128 `[A-Za-z0-9._:-]` (first alnum); U32 исключает bool/
float/overflow; GitSHA — 40 lowercase hex. Для recommended profile vcpu≥4,
ram_mib≥8192, disk_mib≥65536. Выбранный вариант, реальные build/UBR и его SHA —
approval input L-04, не пустые поля/defaults. Нет serial numbers/real user IDs в Git.

### 7.2 Обязательная matrix

Все below cases выполняются на каждом selected profile. Табличный PASS означает
future acceptance criterion, **не текущий результат**.

| ID | Cases / конкретные повторы | Expected outcome |
|---|---|---|
| LT01 | 3 complete install→start→stop→cleanup cycles; preexisting names/path/identity collisions | Только own-process lab service; collision отказ без takeover; cleanup не касается чужих objects |
| LT02 | 10 normal START/STOP/restart cycles, 10 forced-crash/restart cycles | Deadlines §5, новая incarnation каждый startup, no inherited active sessions; observed SCM/token SID exact |
| LT03 | A/B/Denied/Admin tokens; GENERIC_WRITE/CREATE_PIPE_INSTANCE/WRITE_DAC/VM_WRITE/TOKEN_DUPLICATE requests | Specific allowed masks работают A/B; Denied connect и дополнительные rights rejected; admin install не mock grant |
| LT04 | Squatting до startup; wrong owner/process/account/SV/image; restart/PID race; production reference verifier | Service first-instance failure/clients reject до HELLO; no private data sent; prod profile rejects lab identity/frame/result |
| LT05 | Anonymous, SQOS Anonymous/Impersonation/Delegation, wrong SID и remote connection; client handle handoff на другого SID для ACK | Только exact Identification token A/B; remote denied; wrong ACK closes, no second engine operation |
| LT06 | Impersonate false; TokenUser query false; Revert false; residual token; control positive with actual calls | No admit; revert/residual failure fail-stop process, без response/logging от worker; injected vs native evidence различены |
| LT07 | Header cuts 0..7, body cuts {1,mid,N-1}; N=0/MAX+1; extra frames/bytes; duplicate/unknown/missing fields/version, bad UTF-8/BOM/surrogate/float/NaN; outer depth65/66 и inner64/65 | Canonical/size/schema refusal, no resync/no W1; over-limit до body allocation; valid fixtures проходят unchanged S1 parser |
| LT08 | 4 active instances +5th client, queue full/2000-ms wait, slowloris, 5000-ms write/ACK deadlines; 10 races completion/cancel at each of ARM/IO/COMPLETE | Bounded workers/buffers; no thread/handle reuse до completion; 1000-ms grace иначе fail-stop; no invented result |
| LT09 | 12 GD policy cases ×12 gate/decision probes =144 cells | A: 12 exact allow,132 deny; APPROVE не REVOKE и SCRIPT не SCENES/HANDOFF |
| LT10 | B: 12 exact GD probes; 5 CG cases ×6 enabled S1 operations; remove each required grant; PUBLISH_REVISION in all17 cases | B denies12; CG_INIT allows3, MIGRATE1, RECOVERY1, WRITER_ONLY/NONE0; missing grant/disabled tag no admission |
| LT11 | Same request retry after virtual PREPARE/INTENT/COMMIT and lost response; changed bytes/principal/session; LOOKUP | Same bytes/result stable within incarnation, no duplicate virtual terminal; conflict before new W1; no disclosure чужого result |
| LT12 | Crash before admission, after RAM finalization before reply, lost ACK; reconnect with old incarnation и with new incarnation+old request | UNKNOWN_AFTER_RESTART или whitelist denial, не fresh success/ABORT для утраченного request; new fixture run explicit |
| LT13 | Pre-admission deny fixture, malformed/unauthorized/oversize/capacity errors; 33rd admitted ID | No model W1/events/ID consumption для denied new request; cap no eviction; known replay/lookup остаётся доступным |
| LT14 | Observer/file API guard covers full runtime of all cases, reads/modules/pipe vs regular files separated | 0 forbidden write attempts и 0 protected writes; no keys/DPAPI/network/subprocess/actual registration/history; audit gaps BLOCKED |
| LT15 | Original S2.1–S2.4 + original D-01 regressions/golden vectors against unchanged sources; wrapper independent decode/checks | No contract/golden changes; no raw S1 Receipt/FrozenCommand/MAC/key in response, correct SSLB lengths/hashes/cache bytes |

Для LT07 depth/max-byte fixtures, не являющиеся allowed command templates, parser
boundary проверяется отдельно: прохождение bounded read не означает model admit.
LT13 наполняет 32 admissions через GD_SCRIPT_REJECT и 32 разных slots, затем
slot32 (33-й recognized/authorized request) должен дать LAB_CAPACITY; повторные
MIGRATE no-ops не используются для искусственного заполнения capacity.
Negative fuzz bytes не попадают в journal или protected files. LT11 virtual-phase
states подготавливает pinned factory/host-side fixture, не remote debug API.
10 races каждого LT08 point фиксируются harness operation IDs, не wall-clock lucky
sleep. Любой недетерминированный сбой сохраняется как FAIL, не rerun-until-green.
Тесты начала/конца token impersonation обязаны проверять native thread context,
а не только mock boolean. Revert-failure injection проверяет fail-stop branch,
но не объявляется реальным отказом Windows RevertToSelf.

### 7.3 Evidence и значения labels

Private evidence output harness — canonical index с этой закрытой schema:

```text
EvidenceIndex = {lab_evidence_version:1, scope:Scope, run_id:UUID,
 profile_sha256:Hex, source_base_sha:GitSHA, source_test_sha:GitSHA,
 fixture_set_sha256:Hex,
 tests:[{test_id:LT01..LT15, case_id:Label, repetition:U32_positive,
         result:PASS|FAIL|BLOCKED, observation:NATIVE|INJECTED|PURE,
         trace_sha256:Hex}],
 overall:NOT_RUN|FAIL|LAB_SERVICE_TESTED,
 forbidden_write_attempts:U64, protected_writes:U64,
 process_qualified:false, power_loss_qualified:false}
```

`tests` ≤10000, empty только при overall NOT_RUN, иначе nonempty; no duplicate `(test_id,case_id,repetition)`; все planned
cases/repetitions из matrix обязательны. Static compiler/test runner produces
expected case list до run; complete index coverage сверяется независимо.
Trace — bounded private redacted capture: monotonic timings, native return codes,
process/account **aliases**, endpoint identity verdicts, request/result hashes,
RAM model event counts. Не dump tokens/passwords/full journal/snapshots/real SIDs.
Evidence в Git — только synthetic examples/redacted summaries по отдельному scope;
actual ETW traces, dumps и private manifests остаются вне Git.

`LAB_SERVICE_TESTED(profile_sha256, source_sha)` допустим только после всех PASS,
zero audit gaps/forbidden writes, no skipped cells и независимого review. 3 install
cycles и 10+10 lifecycle cycles должны полностью пройти; превышенный timeout —
failure test, не auto-approved увеличенный limit. Негативный тест с ожидаемым
fail-stop считается PASS только при точном expected outcome и отсутствии side effects.
Этот label относится лишь к SCM/IPC/identity/mock behavior выбранного lab profile.
**PROCESS_QUALIFIED и POWER_LOSS_QUALIFIED остаются false и не выводятся из него.**
Нет real NTFS W0–W9, directory flush, persistent history или power cuts. VM reset
здесь проверяет RAM loss/unknown outcome, не durability storage. Числа Q1 и реальные
Windows deployment profiles этим не выбираются и не утверждаются.

## 8. Owner decision register — L-01–L-04

Все строки — **предложения**. Владелец выбирает exact вариант/параметры и pin-ит
SHA этого контракта до S3.2. Отсутствующее решение не заменяется recommended value.

| ID | Рекомендация с конкретными параметрами | Альтернатива / последствия | Условия приёмки |
|---|---|---|---|
| L-01 | StoryStudioBrokerLab + dedicated SSLabBrokerSvc, RESTRICTED SV, SeChangeNotifyPrivilege only; names/paths/ACL §1/§2; no auto restart | Virtual service account с отдельно подтверждённым TokenUser/SV mapping; либо UNRESTRICTED/SeImpersonate только новым явным choice. Non-SCM harness — preliminary, не SCM label | LT01–LT06: native identity, immutable search paths, no collisions/takeover, reversible cleanup; fail если chosen account не может установить descriptors/identify token |
| L-02 | LAB_ACL_1 masks/SDDL; message server + byte client; SSLB framing, one request+response+ACK per connection; 4 workers/1 dispatcher/queue2, caps/deadlines §3/§5 | Client message-mode with GENERIC_WRITE не рекомендуется из-за create-instance right. Отдельный one-way response pipe/overlapped IO — другой contract revision с собственными masks/framing/cancellation tests, не fallback | LT03–LT08: exact masks, no unknown fields/oversize/pipeline, endpoint identity before send, bounded cancellation; не повышать права ради SetNamedPipeHandleState |
| L-03 | S32_FIXTURES_1, 17 policy cases ×closed FaultCase, SID→synthetic A/B mapping;32 RAM admissions/incarnation; incarnation-scoped UUIDv5; summary digest без Receipt | Parser-only/no engine — меньше риска, но не проверяет idempotency/admission; raw S1 mock receipts запрещены. Persisted mock recovery — вне первого lab и требует другого scope | LT09–LT15:144 GD cells, separate command/read scopes, no W1 on pre-admission deny, stable cache, restart unknown/whitelist denial, no protected IO/production-compatible receipt |
| L-04 | First isolated maintained Win11 Pro x64 VM,4vCPU/8GiB/64GiB NTFS; exact build/UBR approved HostProfile; LT01–LT15, repetitions §7, private EvidenceIndex | Win10 Pro22H2+verified ESU or both VMs, each separate profile result. Physical power-loss/production NTFS tests — отдельная будущая qualification | Complete coverage/all PASS +zero write attempts/audit gaps, independent review before LAB_SERVICE_TESTED; no PROCESS/POWER label; OS licensing/support checked до run |

Если chosen variant требует расширить access mask/privileges, новые message types,
key/provider/persistence или constraints matrix, это новая reviewable contract
revision — не самостоятельная трактовка implementation. Q1, operational NativeRootBinding,
DPAPI/real key disaster policy, native writer/flush/cutover/backup не включены в L-01–L-04.

## 9. Источники, проверяемые факты и STOP

Windows API facts со ссылками выше — documentation evidence, не наблюдённое
поведение нашего adapter. Дополнительные definitions:
[CreateNamedPipeW](https://learn.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-createnamedpipew),
[GetTokenInformation](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-gettokeninformation).
Последствия missing bits/cancellation/query permissions должны быть измерены на
selected lab profile. Нет утверждения, что Windows automatically grants token query
или что любой generic handle mask взаимозаменяем с приведённым specific mask.

SDDL/hex arithmetic, schemas/limits/refs и profile choices проверяются как design;
ConvertStringSecurityDescriptorToSecurityDescriptor/AccessCheck и реальные SID/token/
SCM/pipe tests на Windows этим заданием **не запускались**. Нельзя писать в результате
LAB_SERVICE_TESTED только потому, что этот документ завершён.

После publication — **STOP**. Требуются независимая проверка и owner approval
exact L-01–L-04 перед S3.2. Нет service creation/install, production code,
new dependencies/keys/media, PR/merge/release/main changes.
