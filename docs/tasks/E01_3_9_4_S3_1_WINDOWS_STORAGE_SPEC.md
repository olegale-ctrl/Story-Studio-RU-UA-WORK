# E01.3.9.4 / S3.1 — Windows Protected Storage Implementation Specification

**Статус: PROPOSAL — НЕ УТВЕРЖДЁН; design-only. Дата: 2026-11-06.**
Этот документ предлагает проверяемую Windows-реализацию уже утверждённого S1.
Он не разрешает S3.2, не утверждает Q1/profiles и не подтверждает production
security, process-crash consistency или power-loss durability.

## 0. Основание, язык гарантий и неизменяемые границы

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Base branch: `docs/editorial-e01-3-9-3-s2-completion-s3-entry-proposal`.
Exact base: `76c3478ed243317acc833eff5cfe2d767e886d11`.
Branch: `docs/editorial-e01-3-9-4-s3-1-windows-storage-spec`.

Приоритет источников:

- [D1–D12](E01_3_9_1B_APPROVED_ARCHITECTURE_DECISION.md) и
  [approved S1b](E01_3_9_2B_S1_APPROVED_CONTRACT.md), утверждающий точную
  [S1a редакцию](E01_3_9_2_S1_STORAGE_COMMAND_CONTRACT_PROPOSAL.md) на
  `83ac4ac3fa5104a9a43bc2fa5f98d735a694f49c`.
- E00: `docs/EDITORIAL_E00_FINAL_SPEC.md` на
  `e520648411b99264688ff66dc61ad0e974201ed3`; [A1–A14](E01_3_7_3_APPROVED_CONTRACT.md),
  [O1–O10](E01_3_8_1_APPROVED_CONTRACT.md); Story Intelligence остаётся non-authoritative.
- [Закрытие S2 / S3 entry](E01_3_9_3_S2_CLOSEOUT_AND_S3_ENTRY_PROPOSAL.md): S2 принят
  только как pure model; reported 808 tests не являются Windows qualification.
  Reviewer не заявлял независимого повторного запуска этих tests.
- [S2.4 / D-01](E01_3_9_3_S2_4_RESULT.md): parent epoch сверяется с authenticated
  registration до наследования history/IDs/order; original reproducer неизменён.
- GitHub policy из отдельного `ceca15c20cedd5277ad0bdafc418eef149e7bc7b`:
  не предполагается merged; keys/protected artifacts/media не публикуются.

Метки во всём документе:

| Метка | Значение |
|---|---|
| F | Документированная возможность/ограничение API; ссылка Microsoft рядом с утверждением. Это не результат наших tests |
| P | Предложенное решение adapter/service, требует approval S3.1 владельцем |
| Q | Экспериментальный qualification gate; до успешного evidence свойство не заявляется |
| I | Уже утверждённый invariant D/S1/E00/A/O; этот документ его не пересматривает |

Для решений `WS01`–`WS12` ниже указаны mechanism, basis, failure, verification,
risk и approval. Конкретизация P не получает статус I по одному упоминанию D.
Если реализация не может выполнить invariant или обнаружено противоречие,
protected operation блокируется; требуется отдельное решение, не тихий fallback.

**I:** один authoritative editorial JSON; CP — primary namespace replacement;
external protected journal/anchor записываются отдельно. Existing schema-1/2,
checksum/digests, closed wire/limits/domains S1 и S2.1–S2.4/golden vectors неизменны.
`PUBLISH_REVISION` — **DISABLED**; partial COMMIT reconstruction — **OFF**.
Нет generic save-json/admin overwrite, активного epoch reset/merge или выдуманного
approval. Authenticated SID, CommandGrant, GateDecisionGrant, editorial approval,
rights и production readiness — разные проверки. HANDOFF только editorial.
Поддерживаемый target class: offline CPU-only Windows 10/11 + local NTFS.
RU/UK (`ru`/`uk`) сохраняются; новые лицензии, media/model dependencies не вводятся.

## 1. WS01 — Windows service и разделение прав

**P / механизм:** отдельный SCM own-process broker `StoryStudioBroker` под
выделенной noninteractive service identity, с service SID; обычный CLI не elevated.
Кандидат — virtual service account `NT SERVICE\StoryStudioBroker`; вариант —
отдельная local service account при принятом lifecycle. LocalSystem не выбирается
как автоматическое решение проблем permissions. Service SID type RESTRICTED —
кандидат hardening, его совместимость с IPC/DPAPI/каталогами должна быть проверена.
Изменение на UNRESTRICTED не допускается как необъявленный fallback.

F: SCM запускает service с account token и загружает профиль; это не доказывает
сохранность DPAPI material при account replacement
([Service user accounts](https://learn.microsoft.com/en-us/windows/win32/services/service-user-accounts)).
Service SID позволяет ACL привязывать к конкретной service
([SERVICE_SID_INFO](https://learn.microsoft.com/en-us/windows/win32/api/winsvc/ns-winsvc-service_sid_info)).

| Роль | Разрешённые действия | Что не следует из роли |
|---|---|---|
| Standard-user CLI/reviewer | Connect к локальному IPC; read/status в своём scope; явно разрешённые commands/gate decisions; drafts | Direct write primary/journal/anchor/key; initialize/recovery/all gates по умолчанию |
| Broker service | Protected I/O после checks; хранение ключа в памяти; exact replay | Самостоятельный human review, новый approval/rights/readiness grant |
| Administrator/installer | Install/update/remove binaries/service; provisioning ACL/account/key; согласованная maintenance | Автоматический editorial APPROVE/REVOKE; erase history/reinitialize production |

Binary/runtime/library search paths и их ancestors — installer-owned, без
standard-user write; абсолютный quoted SCM image path, фиксированный runtime,
без user site-packages/PATH/current-directory module loading. Service object DACL
даёт CLI только нужный query-status доступ, не CHANGE_CONFIG/STOP/DELETE.
SCM config rights — отдельная граница
([Service security](https://learn.microsoft.com/en-us/windows/win32/services/service-security-and-access-rights)).
Привилегии service ограничиваются реально необходимыми, без SeDebug/backup/restore
или volume-wide flush privileges ради удобства. Network work отсутствует.

| Основание | Сбой | Проверка | Остаточный риск | Отдельное approval |
|---|---|---|---|---|
| D1/D9/D12, A1/A2 | Неправильный token/SID, service account или runtime protection → PROTECTION_INVALID, drafts/status only | T01/T03: user/service/admin access matrix, writable DLL/module/config attempts | Admin/kernel/compromised broker вне baseline; account/profile lifecycle | Account, service SID mode, installer/runtime packaging и privilege list — P; principles D1/D9 уже I |

## 2. WS02 — IPC, SID и scoped authorization

**P / транспорт:** локальный versioned named pipe `\\.\pipe\StoryStudioBroker.v1`,
message mode (`PIPE_TYPE_MESSAGE`, `PIPE_READMODE_MESSAGE`, blocking wait на worker),
remote clients rejected (`PIPE_REJECT_REMOTE_CLIENTS`). Первый server handle
использует `FILE_FLAG_FIRST_PIPE_INSTANCE`; collision → stop/busy, не подключение
к чужому endpoint. Он остаётся открыт на lifetime broker; дополнительные instances
создаются только этим broker с тем же explicit descriptor.
F: соответствующие flags предусмотрены
[CreateNamedPipeW](https://learn.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-createnamedpipew).

Pipe DACL: service/SYSTEM могут создавать instances; installed local client group
получает только explicit data read/write, attributes, READ_CONTROL/SYNCHRONIZE,
не FILE_CREATE_PIPE_INSTANCE. Client CreateFile просит согласованный specific mask,
не GENERIC_WRITE: FILE_APPEND_DATA делит bit с CREATE_PIPE_INSTANCE
([Named pipe security](https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-security-and-access-rights)).
Ни default descriptor, ни Everyone/Anonymous full/write access не используются.
Exact access mask/SDDL и session/logon SID ограничения — acceptance fixture T02,
требующий утверждения; строки реальных SIDs в Git не нужны.

Один S1 command message — exact C(Request) ≤1 MiB. Чтение ERROR_MORE_DATA собирает
только этот message с cumulative limit; premature EOF/oversize/unknown fields —
reject, без PREPARE. Response — существующий S1 union, без transport trust flags.
JSON decoding не нормализует Unicode/numbers; U64 не проходит через double.
Не pipelining разных запросов на одном impersonation context. Worker concurrency,
resource/deadline caps — параметры реализации для approval, не новые Q1 defaults. Blocking worker должен иметь supervisor-controlled cancellation:
кандидат CancelSynchronousIo + завершение/close после наблюдаемого completion,
не assumption, что cancel уже завершился. До admission timeout закрывает connection;
после admission disconnect не отменяет transaction/intent. Механизм и race tests
описаны в [Windows I/O cancellation](https://learn.microsoft.com/en-us/windows/win32/fileio/canceling-pending-i-o-operations);
точные time/worker bounds требуют O-WIN-02 до S3.2, бесконечный PIPE_WAIT не принимается.

**P / server authentication перед передачей review data:** client сверяет pipe
owner/DACL с установленным descriptor, получает server PID через
[GetNamedPipeServerProcessId](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getnamedpipeserverprocessid),
сопоставляет с SCM status, удерживает process handle и проверяет trusted image
location/account/service SID. PID alone, имя процесса и приветственный JSON не
достаточны. Повторить identity/liveness checks перед send; недоступный TOKEN_QUERY
или inability to establish endpoint identity → отказ, не ослабление проверки.
Устойчивость к restart/PID reuse и возможность этих checks обычным CLI — Q/T02.
Это OS-bound authentication, не новый cryptographic transport/key exchange.

**P / client authentication на каждом message:** после чтения этого message
ImpersonateNamedPipeClient → проверить success → OpenThreadToken(TOKEN_QUERY) →
GetTokenInformation(TokenUser, TokenType, TokenImpersonationLevel); SID канонически
преобразуется в существующий `windows-sid:...`. Anonymous/непригодный token → deny.
Кандидат client SQOS — SECURITY_IDENTIFICATION: нужен identity query, не delegation;
точный level/privilege contract проверяется T02, не угадывается по elevated token.
F: impersonation failure нельзя продолжать под правами service
([ImpersonateNamedPipeClient](https://learn.microsoft.com/en-us/windows/win32/api/namedpipeapi/nf-namedpipeapi-impersonatenamedpipeclient)).
В finally — проверенный RevertToSelf; при его failure — fail-stop process,
никаких privileged writes на этом worker
([RevertToSelf](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-reverttoself)).
SID извлекается именно из token, не caller JSON/PID/username/env
([GetTokenInformation](https://learn.microsoft.com/en-us/windows/win32/api/securitybaseapi/nf-securitybaseapi-gettokeninformation)).
Storage/DPAPI выполняются только после возврата к service context.

**I / protected lookup:** production + authenticated SID → protected current
PolicyRef + exact minimal CommandGrant set S1 §5.2. RECORD_DECISION дополнительно
требует exact GateDecisionGrant `(gate, decision)`: все 12 пар независимы;
APPROVE не даёт REVOKE/REJECT/REVISE или другой gate. Draft edit не даёт protected
snapshot write. Missing policy/provider/principal/scope → deny. Lookup version/hash
сохраняется как immutable protected evidence; editable snapshot/editorial
policy_version не выбирает authority policy. Policy update сериализуется с W4
recheck+intent barrier. После intent — replay прежнего frozen context; live grant
не создаётся повторно. Read access к request lookup проверяется до выдачи receipt.

| S1 operation | Обязательные command scopes | Gate scope |
|---|---|---|
| INITIALIZE_EMPTY / IMPORT_BASELINE / TRANSFER_BASELINE | PROTECTED_SNAPSHOT_WRITE + INITIALIZE | null |
| MIGRATE_SCHEMA | PROTECTED_SNAPSHOT_WRITE + MIGRATE_SCHEMA | null |
| RESTORE_EXACT_HEAD | PROTECTED_SNAPSHOT_WRITE + RECOVERY | null |
| RECORD_DECISION | PROTECTED_SNAPSHOT_WRITE + RECORD_DECISION | Только exact request gate/decision |
| PUBLISH_REVISION | Не существует разрешающего набора, operation disabled | Никакой grant не включает её |

**P / lock order provider:** writer удерживает production lock, затем берёт
policy-activation gate; W4 recheck и append/flush INTENT выполняются под gate.
Activation нового immutable policy artifact использует только этот gate и никогда
не ждёт production lock под ним. Не вводить обратный порядок locks. После полного
intent gate можно освободить до anchor update: поздняя activation не переписывает
frozen evidence. Protected artifacts прежних версий сохраняются для replay.
Политика live timeout/lock contention не разрешает «сменить policy и продолжить»;
pre-intent ABORT допустим только с доказанным no-intent prefix. Этот provider
mechanism и concurrency tests входят в O-WIN-02/T04, не являются уже реализацией.

**Открытая граница control plane:** S1 Request содержит BlobRef/session ID, но не
определяет complete upload/review-session/diagnostic IPC subprotocol. Здесь не
добавляются команды в S1. Предлагается отдельный versioned local control channel
для bounded staging и explicit confirmations с SID/session binding; его closed
schemas, limits, privacy и test vectors надо утвердить отдельно до operational use.
До этого command channel принимает только уже service-staged проверенные refs в
lab/mock setup; не открывает caller paths/URLs/handles и не имеет generic file-write
endpoint. S3.2 может проверить transport/identity против mock store, а не обходить
незакрытую границу ради production writes. Current-package/authority evaluator не
объявляется реализованным одним OS-token adapter.

| Основание | Сбой | Проверка | Остаточный риск | Отдельное approval |
|---|---|---|---|---|
| S1 §2/§5/§10/§12, A1–A3/A5/A7/A12, D1/D9/D11 | Impersonation/SID/endpoint/policy failure → closed error/connection close без writes; lost response → lookup прежнего request, не новый ID | T02: squatting, remote pipe, anonymous/SQOS, mixed principals/messages, 12 grants; T04: restart/retry/policy race | Same-user malware может действовать от реального SID; UI confirmation не равна cryptographic human intent | Pipe descriptor, SQOS/server checks, control-channel contract и provider deployment — P; S1 scopes уже I |

## 3. WS03 — DPAPI, ключи, maintenance и key loss

**P / механизм:** отдельный protected key registry по S1 key_id; provisioning
ровно 32 random bytes trusted initializer, только после отдельного authorization.
Кандидат persistence — DPAPI **current-user scope service account**, noninteractive
(UI_FORBIDDEN), service-only DACL + SYSTEM на encrypted blob и ancestors.
DPAPI вызовы никогда не выполняются в impersonated client context. Decryption при
startup требует прежней identity/profile; length/key_id/MAC proofs проверяются.
Service SID в DACL и service-account DPAPI credential — разные механизмы.

F: DPAPI user scope обычно связан с credential/machine; machine scope допускает
decryption любым user этой машины, получившим blob. Поэтому LOCAL_MACHINE не
является service isolation и не используется как silent fallback
([CryptProtectData](https://learn.microsoft.com/en-us/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata)).
Конкретный account/profile переживает reboot/update/password lifecycle только
после T03; при неудаче — другой отдельно approved account/protection design.

Ключ plaintext живёт только в isolated broker memory; не в IPC/log/crash dump/Git,
не под экспортным API. Доступ к dumps и diagnostics bundle ограничен; применить
native buffer clearing где возможно. Python-managed copies не позволяют обещать
полное zeroization; необходимость dedicated native key boundary — open risk.
Service storage HMAC не заменяет editorial attestation/signature.

**I:** S1 v1 rotation, key-id rollover, re-sign старой истории и cross-machine key
export **не определены и отключены**. Раздел «rotation» означает запрет операции
до отдельного approved protocol/lifecycle, а не предложенный период ротации.
DPAPI re-protection того же K — только отдельная maintenance proposal после
сохранения rollback-safe profile/access; не автоматическая операция S3.2.
Missing/corrupt DPAPI blob, unknown key_id или MAC mismatch → KEY_UNAVAILABLE/
MAC_MISMATCH, без нового ключа, auto-genesis или переподписания прошлого.
При потере credentials/profile/key data-only backup не возвращает authority.

| Основание | Сбой | Проверка | Остаточный риск | Отдельное approval |
|---|---|---|---|---|
| D3/D6/D9, S1 §3/§7/§11 | No decrypt/unknown key → trust/writes blocked; diagnostics не раскрывают secret | T03: ordinary user decrypt denial, service cold reboot, account/profile change, damaged blob, missing key | Admin/memory compromise; DPAPI profile disaster; Python memory copies | Account/DPAPI mode/provisioning/dump policy — P; rotation/export требуют отдельного будущего контракта, не этого approval |

## 4. WS04 — ACL, managed namespace и native identity

**P / layout на одном проверенном local NTFS volume:** installer-managed root под
ProgramData; отдельные service-owned `Projects/<P>/editorial.json`, `.write.lock`,
backup и sibling staging; `Protected/anchors`, `journals/<P>/<E>`, immutable
images/blobs, registration, policies, keys и recovery quarantine. Это layout
предложение, не дополнительные поля editorial snapshot или S1.

| Объект | Предлагаемый access boundary |
|---|---|
| Root/ancestors, service code/config | SYSTEM/installer owner; service необходимые права; user не может replace/rename ancestors или менять security |
| Primary JSON | Service write/replace; selected client group может получить read-only. Read bytes не даёт authority |
| Primary parent dir/temp/backup | Service/SYSTEM create/write/delete; user не получает DELETE_CHILD, delete или create |
| Journal/anchor/images/blobs/registration/policies/key material | Service/SYSTEM; ordinary client не читает secrets и не пишет protected metadata |
| Policy activation / maintenance | Только approved administrative maintenance, сериализованная с broker; не прямой UI edit |

Explicit protected DACL, без широкого inherited Users/CreatorOwner write;
owner не обычный reviewer. Проверять security descriptor/owner через handles
перед admission и после replacement, не исправлять испорченную protection в
обычном request. F: descriptors наследуются при create, не пересоздаются простым
rename; ACL replacement надо проверять отдельно
([File security](https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights)).

Предлагаемый NativeRootBinding в protected deployment catalog разрешает S1
managed_root_token в pinned root/volume/directory identity. **Его closed deployment
schema должна быть утверждена до real registration; она здесь не изобретается.**
Catalog не третий mutable head и не источник approval: только location/protection
binding, проверяемый вместе с immutable Registration/InitializationAuthorization.
Registry cache/missing index не разрешает recreate anchor.

Path selection: только broker-generated UUID/hash names. Открывать ancestor chain
с OPEN_REPARSE_POINT/для directories BACKUP_SEMANTICS, проверять каждый component,
удерживать directory handles против rename; OPEN_REPARSE_POINT только на final
component не закрывает весь путь. Reparse/junction/symlink/cloud placeholders,
hard links (link count не 1), ADS/device/UNC paths и другой volume — reject.
Volume/dir/file identity проверять через native handles
([GetFileInformationByHandleEx](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-getfileinformationbyhandleex)).
Final path string/prefix и GetDriveType сами по себе недостаточны. File ID primary
может законно меняться при replacement; root identity стабилен, recovery content
сверяется по authenticated hashes, а не по старому primary File ID.

SMB/sync/removable/exFAT/ReFS/WSL roots не поддерживаются. Sync exclusion строится
на managed location + запрете reparse/known sync layouts, не на обещании обнаружить
любой сторонний sync agent. Если native path/handle scheme не исключает TOCTOU
в принятой threat model, writer не принимается; не применять path-only CAS.

| Основание | Сбой | Проверка | Остаточный риск | Отдельное approval |
|---|---|---|---|---|
| D1/D2/D10/D12, S1 §5/§7/§9, A11 | Unexpected owner/DACL/volume/link/root → PROTECTION_INVALID/ANCHOR_UNAVAILABLE, без permission repair | T01/T05: direct writes/DELETE_CHILD/rename/links/ACL inheritance, post-replace DACL and root identity | Privileged namespace tampering вне baseline; unknown sync software | Exact descriptors/layout/NativeRootBinding schema и handle scheme — P/Q; service-only writes уже I |

## 5. WS05 — Отображение W0–W9 на NTFS

**P / общие primitives:** narrow reviewed Win32 adapter, кандидат — явные wide
Win32 calls через standard-library FFI; упаковка и native boundary отдельно
reviewed. Каждый IO call проверяет return, immediate GetLastError и byte count.
Write-new metadata через CREATE_NEW, exact bytes, language buffers flush,
FlushFileBuffers(handle с GENERIC_WRITE), reopen/reread/hash/type verification.
Buffered I/O + explicit flush — кандидат; NO_BUFFERING/alignment не вводится
автоматически для variable-length journal. Данные и namespace имеют разные barriers. Для REPAIR_EXACT strict integrity
проверяется у recorded H/archived target; повреждённый C только fingerprint/forensic
input, не trusted snapshot. Oversized/unsupported C даёт diagnostic block,
не blind overwrite и не объявление его integrity.

Все строки таблицы сохраняют S1 §8/§9; никакие flags не объединяют journal,
primary и anchor в атомарную файловую группу.

| Шаг | Native candidate и обязательный порядок | Failure / проверяемый outcome |
|---|---|---|
| W0 | Authenticate + lookup; per-production lock; validate registration/ACL/key/anchor/full chain/source/CAS; freeze command/IDs/time/B/core/plan; grant recheck boundary подготовлен | Reject до PREPARE без admission. Проверки quotas не обещают отсутствие последующего disk-full |
| W1 | Write-new archive exact A/B, frozen command, plan, guard/ledger blobs; каждый отдельный flush/reread; B sibling temp на том же volume, intended DACL до публикации | Failed/short temp write не публикуется. Orphans не authority; live unresolved artifacts не удаляются guessed cleanup |
| W2 | Exact A → backup temp → flush/verify → same-volume backup replacement/verify; затем один exact PREPARE frame append + journal FlushFileBuffers | Complete authenticated PREPARE consumes request/session/IDs/sequence даже без ответа. Partial journal frame → block. Genesis не имеет A backup; repair сначала forensic C |
| W3 | AnchorBody stable A, guard_before, PREPARED/high watermark/tail: temp write/flush → replace → reopen/flush/reread/MAC | Anchor может отставать от journal. Missing anchor после restart не создаётся из PREPARE. First genesis anchor создаётся только в explicit initialization flow |
| W4 | Under policy update serialization recheck exact frozen PolicyRef/grants; append/flush PUBLISH_INTENT **раньше** anchor pending INTENT replacement/flush/reread | Proven no-intent/policy failure → ABORT(REVALIDATION_FAILED); possible/full intent → unknown/pending/reconcile, не ABORT по одному return code |
| W5 — CP | Проверенный same-volume primary replacement exact B (§6), под lock/protected namespace/source observation CAS | Publication B — CP; это ещё не receipt. Error не доказывает «не committed» |
| W6 | Reopen published object, verify expected B identity/bytes/checksum/full integrity; FlushFileBuffers published handle | Wrong/missing C, unexpected identity, sharing/flush error → pending/block; не подмена другим B/backup |
| W7 | Append ровно один S1 terminal frame с frozen ReceiptCore и existing PREPARE/INTENT refs; journal flush/readback | Complete terminal → exact finalization, не duplicate append. Любой torn terminal → block; reconstruction OFF |
| W8 | Final anchor temp/flush/replace/reopen/flush/reread, tail/guard/head cross-check со всем complete journal | Только теперь finalized. Repair сохраняет original CommittedHead.commit_ref; ABORT не меняет generation |
| W9 | Release lock только после stable finalization либо фиксации blocked/pending disposition; send exact canonical receipt | Lost/partial response → same-request lookup; не новые IDs/time/generation. Никакого success до verified W8 |

Journal append: один serialized writer, checked EOF/offset, один complete bounded
SSJ1 frame; no OS assumption об атомарности append или sector alignment. Short
journal WriteFile/error → stop и сохранение имеющихся bytes; не продолжать tail
«до похожего frame», не truncate/resync. Recovery проверяет весь complete prefix
и uncertain suffix. Для temp файлов можно закончить known short writes до flush,
но неполный journal не исправляется этим как recovery capability.

Пример IO mapping (S1 ErrorCode остаётся закрытым): native disk-full → DISK_FULL;
failed flush → FLUSH_FAILED; publication failure → REPLACE_FAILED или
OUTCOME_UNKNOWN/PENDING согласно phase/proofs; unexpected ACL → PROTECTION_INVALID.
Win32 numeric reason остаётся redacted diagnostic detail, не новым ErrorCode.
Failure после possible intent никогда не выдаёт definitive ABORTED без proofs.

| Основание | Сбой | Проверка | Остаточный риск | Отдельное approval |
|---|---|---|---|---|
| D2/D4/D7/D8/D10, E00 §6, S1 §6–§9/§12 | Каждый IO/flush/replace independently fallible; outcome только exact A/B, pending или block | T06/T07/T08: before/after каждого call/barrier; complete unflushed frames, partial writes, repeated recovery crashes | Native/storage persistence не моделируется S2; indefinite pending при утрате proofs | Adapter API/handle/flush recipe — P/Q; ordering/CP S1 не пересматриваются |

## 6. WS06 — Primary replacement и пределы flush

**P / один candidate algorithm**, согласующийся с architecture proposal §5.4:

1. Под `.write.lock` проверить root identity/DACL, pinned source A (repair — exact C
   observation; genesis — MISSING) и полностью подготовленный B на том же volume.
2. B temp write/flush/reread/full validation; DACL/owner заданы до rename.
   Запомнить native temp File ID; закрыть несовместимые собственные handles перед
   publication. Namespace защищён от стороннего user write и других broker writers.
3. Кандидат — `MoveFileExW` с MOVEFILE_REPLACE_EXISTING и MOVEFILE_WRITE_THROUGH;
   **без** COPY_ALLOWED и DELAY_UNTIL_REBOOT. Archive/backup уже отдельные durable
   prerequisites, а не побочный backup внутри этой операции.
4. Reopen primary с правами для read/flush, verify published File ID/volume/ACL и
   exact B; W6 verification+flush. Удерживаемые reader handles согласовать через
   FILE_SHARE_DELETE; source hash/CAS + exclusive writer/protection не превращают
   сам MoveFileEx в Windows atomic compare-and-swap API.
5. На любой uncertain result под тем же lock прочитать реальные A/B/C и journal:
   exact B → verify/forward finalize; exact A с intent → exact forward B; unknown C
   или missing обычного primary → block. Не retry с другим image/API/permission.

F: MoveFileEx поддерживает replacement и ограниченные write-through semantics;
copy/delete move — отдельный механизм. Его описание не устанавливает универсальный
directory persistence barrier для same-volume rename
([MoveFileExW](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw)).
**P/Q:** one namespace publication point, expected A/B behavior после process kill
и ACL/handle semantics этого recipe должны пройти T05–T08 на NTFS. Даже при
успешном BOOL это не claim о power-loss durability.

F: FlushFileBuffers работает с file handle, требует GENERIC_WRITE; volume-wide
flush требует administrative privilege. Pipe flush имеет другую семантику — ждать
чтения client, а не сделать journal durable
([FlushFileBuffers](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-flushfilebuffers)).
Проект не повышает обычный CLI/service до volume-admin ради flush. Не предполагает,
что directory handle + BACKUP_SEMANTICS даёт поддерживаемый эквивалент POSIX fsync.
Temp flush обеспечивает запрос persistence данных, а не доказанное сохранение
последующего directory entry. Windows/NTFS/controller/caches — отдельный Q gate.

**Альтернатива, не fallback:** ReplaceFileW потребовала бы отдельной квалификации
ACL/metadata merge и неоднозначных error outcomes. REPLACEFILE_WRITE_THROUGH
документирован как unsupported; IGNORE_ACL/MERGE_ERRORS не используются для обхода
protection. См. [ReplaceFileW](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-replacefilew)
и [официальный SDK source](https://raw.githubusercontent.com/MicrosoftDocs/sdk-api/docs/sdk-api-src/content/winbase/nf-winbase-replacefilew.md).
Не включать TxF, undocumented namespace flush или иной rename primitive без нового
adapter review. Если требуемый namespace barrier недостижим на выбранном profile,
POWER_LOSS_QUALIFIED не выдаётся; не ослаблять S1/ACK semantics ради результата.

| Основание | Сбой | Проверка | Остаточный риск | Отдельное approval |
|---|---|---|---|---|
| D2/D8/D12, S1 §8/§9, architecture proposal §5.4 | Sharing/access/replace/flush ambiguity → exact observation + reconcile/block, не chmod/delete/copy fallback | T05–T08: antivirus/indexer/readonly reader/no SHARE_DELETE, all publication windows, real power cuts | API/file-system/hardware могут не обеспечить требуемую persisted namespace ordering | Конкретный recipe — P; каждый real profile — Q; смена primitive требует отдельного review |

## 7. WS07 — Lifecycle, один writer и lock recovery

**P / startup:** START_PENDING → проверить service token/runtime/config/protection →
key/registrations/root handles → per-production OS lock → полный read-only replay
§8 → admissible recovery → только затем writes для данной production.
Проблемная production остаётся blocked, безопасный status остальных не скрывается.
Bound frozen requests не превращаются в новые active review sessions. Process
incarnation генерируется service, unbound sessions старой incarnation invalid.

**I/P / lock:** persistent `.write.lock` по E00 §6, Windows msvcrt byte-range
convention. Кандидат детализации adapter — exclusive nonblocking lock byte [0,1), persistent file,
с approval O-WIN-05 и проверкой interoperability всех callers. Это P, не
утверждение, что E00 задаёт конкретный byte range. Adapter не удаляет,
не заменяет и не «очищает» lock file по PID/mtime. Один writer queue
per production; SCM own-process не заменяет межпроцессный lock против maintenance
или другого broker instance. Busy → LOCK_BUSY, не force unlock. Native LockFileEx
допускается лишь после отдельного доказательства interoperability с E00 convention,
не как незаявленная смена lock protocol.
F: OS byte-range locks не защищают от mapped writes, а release при process death
не означает мгновенную доступность
([LockFileEx](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-lockfileex)).
Поэтому нужны ACL/handles и квалификация, не один lock.

Service STOP: перестать принимать новые admission, не объявлять cancel после
possible intent; текущую операцию закончить exact forward либо оставить recoverable
pending/block с прежними proofs. Stop deadline не оправдывает tail truncate/ABORT.
После process kill/SCM restart reacquire OS lock, проверить actual state заново;
не считать отсутствие старого PID proof отсутствия intent. IPC cancellation не
является cancellation primary replacement: MoveFileEx/ReplaceFile не входят в
обычно отменяемые этим механизмом операции; hung native writer сохраняет pending/
unknown disposition, а не выдуманный ABORT ([ограничения cancellation](https://learn.microsoft.com/en-us/windows/win32/fileio/canceling-pending-i-o-operations)). Bounded restart backoff
и administrative alerts — эксплуатационные параметры для approval, не grant.
Update/uninstall не удаляет keys/history/registration/lock/anchor/profile; binary
rollback должен понимать сохранённую protocol version, иначе safe refusal.

| Основание | Сбой | Проверка | Остаточный риск | Отдельное approval |
|---|---|---|---|---|
| E00 §6, D1/D4/D9/D11, S1 §8–§10 | Busy → LOCK_BUSY; stop timeout/kill → replay, не reset; unsupported version → block | T04/T09: duplicate brokers, service kill/STOP/reboot, stale lock file, session invalidation, update rollback | OS shutdown может не дать finish time; AV/handles могут задержать release | SCM recovery/deadline/packaging choices и native lock interoperability — P/Q; E00 lock не меняется |

## 8. WS08 — Startup replay, lineage, history и D-01

**I / порядок доверия:** protection/key → existing anchor + Registration MAC/
InitializationAuthorization binding → full prefix до anchor tail/stable commit_ref →
contiguous authenticated extension → frozen commands/plans/typed blobs/guards →
exact primary observation. Не выбирать state по max generation, timestamp, UUID,
array position, filename или directory listing. Размеры S1 проверяются до allocation;
hash/length/type/context проверяется при каждом dereference. Проверить весь retained
chain итеративно/с cycle detection, не только последний frame или cached index.

D-01 gate: `LineageEntry.storage_epoch_id` и selector parent container обязаны
совпадать с authenticated parent Registration epoch; parent anchor/journal обязаны
иметь тот же context. До этого parent IDs/order/negative history не используются.
Positive parent_head/guard/terminal/machine/production/final stable boundary и
continuity checks сохраняются. Multiple predecessors/foreign UNVERIFIED links не
создают total order. Old consumed IDs и REJECT/REVISE/REVOKE не исчезают при import,
переключении refs, bootstrap, backup или reinstall.

| Наблюдение после проверки всех proofs | Действие |
|---|---|
| Stable head/tail/pending null и exact primary | Read/операции по текущим permissions; MAC не даёт права автоматически |
| Anchor lag, полный PREPARE, proven no intent/uncertain suffix, exact A | Durable ABORT с consumed IDs/high watermark, затем finalize anchor |
| Complete ABORT, anchor lag | Довести тот же terminal guard/tail/receipt |
| Complete INTENT, primary записанный A либо B, B proofs целы | Exact forward completion с прежними IDs/bytes либо block |
| Complete COMMIT и anchor lag | Verify B и finalize existing terminal, не второй COMMIT |
| Partial/bad MAC/gap/fork/type substitution/wrong epoch | Block/manual diagnostics, не skip/truncate/reconstruct |
| Missing/unavailable/ahead/mismatched anchor | Block, не recreate из journal/backup/registry cache |
| Stable primary стал старым A/backup/C | Только explicit RECOVERY-authorized exact-current-head repair; не автоматический rollback |
| First-init crash до существующего anchor | Не автоматический genesis/replay; operator proof procedure не считается реализованной |

Unbound review после restart invalid; lookup admitted request раньше CAS/live grants.
Accepted intent не отменяется новым policy version, но current authority проверяется
отдельно. Historical APPROVE receipt — старый terminal в retained prefix, а не
текущее решение после REVOKE. Repair сохраняет original commit_ref/seq/generation.

| Основание | Сбой | Проверка | Остаточный риск | Отдельное approval |
|---|---|---|---|---|
| D4–D6/D10/D11, S1 §4/§7/§9–§11, A6/A8–A11/A13, S2.4 | Любой недостающий context/proof → fail closed; partial reconstruction OFF | T07/T10/T11: original D-01 unchanged, parent alias/epoch, typed blob substitution, wrong stable primary, old APPROVE retry after REVOKE | Полный privileged rollback всего согласованного protected set локально не обнаружим | Replay rules уже I; native catalog/handles — P/Q; disaster/legacy repair отдельное approval |

## 9. WS09 — Backup, restore, место и Q1

**P / backup:** только stable finalized production под writer lock. Service создаёт
consistent immutable data/proof bundle: exact primary, registration, complete journal,
receipts, committed images и guard/ledger/barrier/lineage proofs. Validate hashes/
types/chain и manifest, publish complete bundle только после verification; partial
copy никогда не помечается usable. Destination — explicit owner-approved independent
storage с согласованными access/privacy, не Git/LFS/Releases/Actions artifact.
Closed manifest/control-channel format и protected transport tool требуют отдельного
approval до operational backup; S1 этим не расширяется.

Ключи, включая DPAPI-protected key blobs, по умолчанию исключены из application
export. Data-only backup проверяется при наличии прежнего local key/protection;
он не является cross-machine trust restore или гарантией disaster recovery.
System-image/key recovery policy — отдельное решение, не скрытый key export.

**I / restore:** authoritative restore старого head не существует. При valid current
anchor/chain — только exact-current-head repair, с RECOVERY grant и forensic C;
на новый machine — explicit unverified baseline без export MAC key/foreign grants.
Missing key/anchor/negative history → drafts/forensics, не surviving APPROVE.
Если невозможно сохранить known REVOKE/consumed IDs/order uncertainty, restore
блокируется. Full privileged restoration of all old protected state вне baseline
anti-rollback detection. Согласованные старые backups не становятся свежим authority.

**P / admission capacity:** под service identity, после RevertToSelf, запросить
free bytes available to caller через
[GetDiskFreeSpaceExW](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-getdiskfreespaceexw).
Учитывать service/volume quotas и calculated peak: ещё не существующие A/B images,
all blobs, temp/backup/anchor/journal growth и quarantine. Preflight advisory;
другой процесс/OS может занять диск позже. Actual disk-full проверяется на каждом IO.
После intent warning/quota threshold не отменяет completion; actual IO failure
оставляет pending/block. Никогда не prune authenticated active history/images
ради места; unreferenced cleanup только после proof-based reachability и отсутствии
unresolved transaction. New admission не разрешается при невыбранной operational
capacity policy; mock S3.2 не превращает отсутствие Q1 в production default.

**Варианты Q1 — НЕ УТВЕРЖДЕНЫ:**

| Параметр | Q1-A: исторический S1 proposal | Q1-B: owner-sized policy, без встроенных чисел |
|---|---|---|
| Retained capacity / warning | 32 GiB per production / 80% | Явно выбрать L и warning w по workload/storage budget |
| Free-space guard | Peak +64 MiB reserve +2 GiB floor | Явно выбрать reserve R и free-space floor F после измерения peak |
| Backup cadence | Weekly и before maintenance, manual on-demand | Owner выбирает recovery-point target и соответствующее schedule |
| External retention | 4 validated complete bundles | Owner выбирает count/age и independent destination/access |

Оба варианта требуют отдельного approval владельца; числа Q1-A не deploy defaults
и не условие protocol correctness. При недостатке места — блокировка новых writes,
alert/owner capacity change, не eviction. External backup retention не active
journal retention. Старую usable копию нельзя удалять до проверки нового complete
bundle и разрешения принятой retention policy. Timers не задают decision order.

| Основание | Сбой | Проверка | Остаточный риск | Отдельное approval |
|---|---|---|---|---|
| D5–D7/D9, S1 §10/§11/§14, A8/A11/A13 | Partial backup не usable; lost key/anchor/history не восстанавливают trust; disk-full → pending/block согласно phase | T08/T12: full disk каждого boundary, old backup/REVOKE, key loss, incomplete bundle, service-specific quota | Machine/key disaster может оставить только forensic data; ransomware/admin вне baseline | Q1 numbers, schedule/destination/retention, manifest/tool и key-DR policy отдельно; preservation уже I |

## 10. WS10 — Drafts, safe diagnostics и недоступная service

**P:** local drafts в user-owned LocalAppData/явном пользовательском каталоге;
UI/CLI читает и проверяет portable bytes existing codec/integrity, без protected
write и effective authority claim. Service absent/unsupported OS/protection failure
показывает понятный RU/UK status, reason и безопасные действия; не предлагает UAC
как обход missing grant и не запускает same-user local writer.

Service diagnostics — authenticated read scope, redacted structured errors и
доступный ordinary user SCM status. При недоступности protected files safe local
inspection остаётся доступным для выбранной пользователем копии, не путём выдачи
ему прав на key/journal. Read-only failures не лечатся ACL changes/key regeneration.
Не логировать raw keys, SID/token contents, full review texts/source materials или
production snapshots. Diagnostic export требует privacy review; Git содержит
только synthetic fixtures/results, не actual protected logs.

Возврат service не auto-publishes накопленные drafts. Нужны explicit permitted
commands и current CAS/policy/review; PUBLISH_REVISION disabled, поэтому произвольное
редактирование protected snapshot через draft не становится доступной функцией.
Rights/intended-use/license checks и отсутствие render/commercial readiness от
HANDOFF сохраняются. No automatic URL fetch/model downloads/cloud upload.

| Основание | Сбой | Проверка | Остаточный риск | Отдельное approval |
|---|---|---|---|---|
| D1/D9/D12, A11/A14, S1 §1/§5/§12, E00 offline/RU/UK | SERVICE_UNAVAILABLE/protection block → drafts/status, не downgrade storage trust | T13: offline standard user, service removed/crashed, portable invalid/legacy snapshots, no network/GPU | Пользователь может спутать history/integrity с current authority; UI wording важно | Diagnostics/read transport schemas и privacy/retention — P; отсутствие fallback writer уже I |

## 11. WS11 — Threat boundary и failure matrix

**I / доверенная база:** Windows kernel/security subsystem, установленный broker,
его dependencies и защищённый provisioning/policy. Обычный local user/его draft
не контролирует protected roots. Administrator, kernel/service compromise, leaked
key, malicious authorized-user session и coherent full protected rollback не
нейтрализуются этим design. HMAC не доказывает human intent, права на media или
source truth. Threat model — D3/D8/A1/A2/S1 §11, не обещание защиты от владельца ПК.

| Fault/threat | Обязательное поведение | Будущий тест / evidence |
|---|---|---|
| Process kill до complete PREPARE | No admission либо artifacts without authority; no guessed receipt | T06: barrier trace + surviving bytes, source unchanged |
| Kill после PREPARE / до proven intent | Verified ABORT либо block; IDs/high watermark consumed | T07: repeated abort crashes, no reservation reuse |
| Kill после full intent / после CP | Только exact B forward/finalize либо block, не ABORT | T07: repeated forward crashes/ACK loss, exact frozen values |
| Power loss любой boundary, включая после ACK | Нет заранее принятой durability; при заявленном qualified ACK должны сохраниться B/order/receipt; потеря — qualification failure | T08: physical cuts, external ACK observer, exact filesystem/proofs capture |
| Disk full / quota / short write | Не claim no-commit после possible intent; preserve partial suffix, pending/block; no pruning | T08/T12: exhaustion на каждом IO, recovery также прерывается |
| ACCESS_DENIED / changed owner/DACL | Fail closed; no chmod/elevation/ACL-ignore fallback | T01/T05: до/после temp/primary/anchor operations |
| Sharing violation / antivirus / reader без share-delete | Bounded failure/reconcile; no delete-then-copy или reboot move | T05/T06: controlled conflicting handles |
| Partial journal/terminal frame | Block/manual diagnostics; no truncation, magic search или reconstruction | T07/T10: all relevant prefix/bit-flip cases |
| Corrupted MAC / wrong key / typed proof substitution | Reject, no replacement key/proof guessing | T03/T10: individually valid hashes при wrong type/context тоже rejected |
| Wrong epoch / aliased parent container | EPOCH_MISMATCH или existing precise context failure до inheritance/W1 | T11: unchanged D-01 и S2.4 negative fixtures на native adapter |
| Backup A вместо current B / old APPROVE после REVOKE | Anchor mismatch либо history-only receipt; REVOKE не теряется | T10/T12: primary/backup/import/retry permutations |
| Pipe squatting / wrong SID / malformed/oversized command | Не отправлять private review data чужому broker, no admission; client/server deny | T02: first-instance/owner/token/SCM races, fuzzed bounded messages |
| Admin целиком откатывает coherent old state | Baseline может не обнаружить; не заявлять anti-rollback witness | T14: documented limit, без выдуманного trusted counter |

Retries сохраняют original request ID/content, не превращают timeout в новую
операцию. Если нельзя различить safe recovery и corrupted state — block.
No success из exception handler или partial validation. Обнаруженный новый дефект
фиксируется reproducer, не маскируется ослаблением S1.

| Основание | Сбой | Проверка | Остаточный риск | Отдельное approval |
|---|---|---|---|---|
| D3–D8/D11, S1 §9/§12/§15, A6–A11 | Только prescribed state/error; невозможность доказать safety → block | T06–T14: matrix с независимым expected state и failure classification | Unknown hardware faults/privileged attacks; availability не гарантируется | Threat exclusions уже I; retry limits/alerts/fault tooling и qualification envelope — P/Q |

## 12. WS12 — Реальные Windows qualification gates

**P/Q:** S2 — independent logical oracle и неизменяемые golden literals, не OS
эмулятор. Native outcomes сравниваются с allowed S1 actions и exact bytes; не
проверять adapter только вторым вызовом его собственной функции. На каждом
before/after barrier наблюдать syscall result, bytes written, flush, process
termination point, persisted primary/frames/anchor/proofs и receipt delivery.
Не включать production data/keys в тестовый стенд или evidence в Git.

Profiles ниже — **варианты для owner approval**, не certified configurations:

| Кандидат | Нужно выбрать/зафиксировать | Ограничение |
|---|---|---|
| W11-N из S1 §14.2 | Windows 11 edition + exact version/full build/UBR/security updates, Intel CPU/iGPU, RAM, local NTFS/NVMe/driver/firmware/cache | S1 historical 25H2/build-family label не автоматически актуальный/approved profile; проверить support перед стендом |
| W10-S из S1 §14.2 | Windows 10 22H2 edition/full build/UBR, maintained security/ESU entitlement, NTFS/SATA-AHCI, controller/cache | Наличие установленной Windows 10 не доказывает support/licensing/security suitability |
| VM-F | Exact host/hypervisor/guest build + virtual NTFS disk/cache/write ordering | Process/VM-reset/fault simulation не physical SSD power-loss qualification |

Owner выбирает exact hosts и поддержку OS до испытаний; здесь не задаются новые
обязательные RAM/диск/build defaults. Первый native profile ограничить одним local
NTFS volume для primary/temp/protected set; independent backup destination отдельно.
Отчёт pin-ит service/adapter/runtime versions, tests SHA, security descriptors,
privilege masks, volume/controller/driver/firmware и volatile/write cache settings.
Secrets, real machine identifiers и serial numbers не экспортируются в Git.

| Gate | Проверяемый критерий |
|---|---|
| T01 — roles/ACL | Standard user не пишет/заменяет primary/anchor/journal/ancestors, не меняет service config; admin install не получает all-gate grant |
| T02 — IPC/token | First-instance collision, remote/anonymous rejection, SID provenance per message, RevertToSelf fail-stop, server identity/restart/PID reuse, bounded wire и 12 independent decision scopes |
| T03 — key lifecycle | Correct service decrypt после cold reboot/update, wrong user/profile/key denial, no key in IPC/log/dumps/export, no auto-regeneration/rotation |
| T04 — sessions/policy | Unbound restart invalidation, existing request lookup before CAS, frozen after-intent evidence, serialized policy recheck/intent |
| T05 — namespace/handles | Ancestor/reparse/hard-link/ADS/UNC/volume checks, ACL after rename, conflicting reads/sharing, case/Unicode/long paths; exact root/file identity |
| T06 — writer boundaries | Before/after every W0–W9 write/flush/replace/verification/ACK; exact A/B/pending/block, never partial successful receipt |
| T07 — recovery | PREPARE/INTENT/CP/terminal/anchor lag, genesis abort, explicit repair, repeated recovery kills; no duplicate terminal or new IDs; partial reconstruction OFF |
| T08 — capacity/power | Disk full/short writes/flush faults at every boundary; physical power-cut schedule incl. after ACK, independent persisted outcome observer |
| T09 — service lifecycle | Competing process/maintenance writers, persistent lock after crash, STOP/kill/reboot, stable account/profile across upgrades, unsupported rollback safe block |
| T10 — proofs/history | Missing/bad MAC/typed blobs/gaps/forks/partial frames/old backup, preserve REJECT/REVISE/REVOKE and exact receipts |
| T11 — epoch D-01 | Original unchanged reproducer and S2.4 tests ported to native fixture IO: container alias != authenticated registration/anchor/journal → no W1/PREPARE/history inheritance |
| T12 — backup/restore/quota | Consistent snapshot under lock, incomplete bundle not usable, exact-current repair only, data-only backup key loss block, no active proof pruning |
| T13 — offline/drafts/privacy | RU/UK standard-user diagnostics/drafts when broker unavailable; no protected downgrade, no network/GPU/model dependency or sensitive logs |
| T14 — regressions/scope | Existing S2.1/S2.2/S2.3/S2.4 and golden vectors unchanged; known threat exclusions and no production claim from virtual evidence |

Параметры числа повторов, cut schedule, seeds, deadlines и resource bounds
утверждаются **до** qualification run, не выбираются задним числом ради pass.
Каждый failure имеет reproducible fixture/trace; zero silently ignored failures.
Процессный gate: на исправном живом OS/storage после kill только prescribed exact
state или explicit block, finalized receipt только с verified terminal/anchor.
Power-loss gate строже: в выбранном qualified envelope acknowledged B/receipt/order
не могут теряться; «безопасно заблокировались после потери ACKed state» — failure
этого durability gate, даже если authority не выдана ошибочно.

Уровни evidence: **DESIGN_ONLY → PROCESS_QUALIFIED → POWER_LOSS_QUALIFIED** только
по отдельным reports/owner acceptance. Первый не подразумевает второй; VM reset
не подменяет physical cuts. При неизвестном directory persistence barrier или
нестабильном cache profile не выпускать POWER_LOSS claim. Все эти Windows/native
тесты здесь **не запускались**.

| Основание | Сбой | Проверка | Остаточный риск | Отдельное approval |
|---|---|---|---|---|
| D8/D12, S1 §14/§15, S2 closeout | Failed gate/profile mismatch → no corresponding qualification/release, не weaker semantics | T01–T14 с pinned environment и независимыми outputs | Испытания не доказывают защиту от любого лживого controller/firmware | Exact profiles, repetitions/evidence plan и каждого qualification report — owner decision |

## 13. Реестр открытых решений и граница S3.2

| Owner decision | Предложение/варианты | До принятия |
|---|---|---|
| O-WIN-01 / WS01 | Virtual vs dedicated account; RESTRICTED SID; installer/runtime packaging, privileges и upgrade lifecycle | Нет production service deployment |
| O-WIN-02 / WS02 | Pipe DACL/access masks, SQOS/server identity checks, resource bounds; closed upload/review/status control protocol | Только отдельно authorized mock transport tests, не operational S1 writes |
| O-WIN-03 / WS03 | Current-user DPAPI + stable service profile, provisioning/dumps; alternative protection требует review | No real provisioning; rotation/export/key disaster recovery не разрешены |
| O-WIN-04 / WS04 | Exact root/descriptors и closed NativeRootBinding deployment schema | No real managed registration/primary/journal/anchor |
| O-WIN-05 / WS05–WS07 | Win32 FFI/handle/locking/MoveFileEx/flush recipe и qualification plan | Ни executable protected writer, ни автоматический fallback |
| O-WIN-06 / WS09 | Q1-A или explicitly configured Q1-B; backup privacy/destination/manifest/schedule/retention | Нет production quotas/backup tool с предложенными defaults |
| O-WIN-07 / WS10 | Read diagnostics/control schemas, privacy/retention, RU/UK status wording | No protected diagnostic data export |
| O-WIN-08 / WS11–WS12 | Exact Windows/NTFS/hardware profiles, fault schedule/counts и separate acceptance levels | DESIGN_ONLY; no production security/durability certification |

Не требуется переутверждать D1–D12/S1 invariants; требуется одобрить предлагаемые
Windows mechanisms и закрыть применимые open decisions. Неопределённый control
protocol или missing deployment schema — blocker нужной функции, не приглашение
реализовать permissive endpoint. Новые решения при конфликте возвращаются владельцу.

**Предлагаемая первая реализация S3.2 после отдельного approval:** own-process
service lifecycle, explicit pipe descriptors/token/SID separation и bounded S1
command parsing против injected mock store/authorization provider в isolated lab.
Lab service identity/pipe names отделены от production identity/endpoint; обычный
production client должен отвергать mock endpoint, без нового trust flag в S1 wire.
Проверять реальные Windows identity/access failures, но не подписывать mock receipt
как production proof. Синтетический test key не становится fallback service key.
Никаких authoritative filesystem writes, actual DPAPI key provisioning, live
registration/history migration, backup export, render или Story Intelligence modules.
Даже этот skeleton не создаётся этим заданием.

**Позже, отдельные задания/gates:** operational control/provider/native binding
contracts; protected NTFS writer/recovery adapter; managed cutover (strict
source/import integrity, service-owned root и unverified legacy history), backups,
process qualification и отдельно power-loss tests. Reinstall/rollback не стирает
history, raw key или account profile. Downgrade, не понимающий текущий protocol,
отказывает; не превращает portable backup в новый approved head.

**STOP после публикации S3.1.** Owner review/approval нужны перед S3.2. Нет
реализации, PR/merge/release/main changes или самостоятельного утверждения этого
proposal. Windows API references выше проверены по Microsoft documentation на
2026-11-06; чтение документации не является экспериментальной квалификацией.
