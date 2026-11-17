# E01.3.9.4 / S3.2b Phase 0 — Windows LAB Host Readiness

Дата: **2026-11-09 (Europe/Kyiv)**.
Итог: **BLOCKED_HOST_NOT_PROVIDED**.
Объём: документационная проверка готовности; native coding/install/run не разрешены.
Это inventory/readiness record, **не утверждение HostProfile**.

## 1. Точная база и прочитанные основания

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Source branch: `docs/editorial-e01-3-9-4-s3-2a-accept-s3-2b-phase0`.
Base: `7cf80eaa4ee2de4201f3e77e59707ba8c0f4429d`.
Перед работой выполнены fetch исходной ветки, `git rev-parse FETCH_HEAD` и
`git ls-remote --heads`: remote HEAD совпал с handoff SHA. Сдвига базы не обнаружено.
Output branch: `docs/editorial-e01-3-9-4-s3-2b-phase0-host-readiness`;
до создания её не было локально и на origin; reset/force-push не применяются.
Final commit/remote SHA сообщаются в handoff после публикации, без self-reference.

Прочитаны и сопоставлены документы на exact base:

- [Полное задание Phase 0](E01_3_9_4_S3_2B_PHASE0_CODEX_TASK.md).
- [Independent acceptance](E01_3_9_4_S3_2A_R1_INDEPENDENT_ACCEPTANCE.md):
  S3.2a-R1 принят только как **ACCEPTED / PURE_ONLY**, S32A-R01 закрыт.
- [QA evidence](E01_3_9_4_S3_2A_R1_ACCEPTANCE_EVIDENCE.md) на
  `4d979c5ee73ac64e8153aa061ab1369dca1623f2` и
  [review S32A-R01](E01_3_9_4_S3_2A_INDEPENDENT_REVIEW.md).
- [Owner split/hash sequencing](E01_3_9_4_S3_2A_OWNER_DECISION.md).
- [L-01–L-04 и RISK-01–04](E01_3_9_4_S3_2_OWNER_LAB_DECISIONS.md).
- [S3.1a LAB contract](E01_3_9_4_S3_1A_LAB_EXECUTION_CONTRACT.md),
  approved exact source `cf70b8c0a93841f2bff272b584a2106374e3016f`;
  HostProfile §7.1, LAB_ACL_1/LAB_LIMITS_1, LT01–LT15.
- [Ранний preflight](E01_3_9_4_S3_2_PREFLIGHT.md) и
  [split proposal](E01_3_9_4_S3_2_PHASE0_REVIEW_AND_SPLIT_PROPOSAL.md).
  Исторические STOP/PROPOSAL не отменяют последующее разрешение portable S3.2a;
  они также не дают разрешения на native S3.2b.
- [S3.1 design](E01_3_9_4_S3_1_WINDOWS_STORAGE_SPEC.md): design/API facts не являются
  доказательством native behavior/durability. Operational DPAPI/writer/backup
  sections не входят в первый LAB scope.
- Отдельный external register — точная ревизия и applicability ниже.

Нормативные D/S1/S2, D-01 и golden vectors, LAB_ACL_1/LAB_LIMITS_1 неизменны.
**PUBLISH_REVISION DISABLED; partial COMMIT reconstruction OFF.**

## 2. Метод наблюдения и доверие к фактам

Только read-only inventory доступного executor, metadata текущей managed environment,
Git provenance и документов. Не сканировались чужие сети/хосты, не выполнялись
удалённые логины или Windows-команды. Секреты/credential files не читались.

| Метка | Смысл |
|---|---|
| OBSERVED | Непосредственно прочитанный факт текущей сессии; не переносится на guest VM |
| OWNER_DECLARED | Явное утверждение владельца/approved decision; не наблюдение доступной машины |
| TO_VERIFY | Требует проверки на конкретном guest/runtime после его предоставления |
| NOT_PROVIDED | Данные, доступ или отдельное разрешение не предоставлены |
| BLOCKED | Действие/квалификация не выполнены из-за отсутствующих prerequisites |

OBSERVED: `uname -srm` → **Linux 6.18.57 x86_64**;
`.venv/bin/python --version` → **Python 3.12.14**. Это Codex Linux executor,
не Windows LAB guest, не утверждённый hypervisor/host и не Windows private runtime.
Managed-environment status: running, observations_current=true, network policy
state=enforced. Runtime variables/secrets/outbound identities для VM не настроены.
Startup policy v1: vpn_configured=false, TCP domains/IP ranges пусты. Наличие
shared-desktop capability не является доказательством Windows guest или допуска.
Эти данные не доказывают, что у владельца нигде нет VM: **VM не предоставлена этой
сессии**. Публичный отчёт не содержит персональных executor/host identifiers.

OWNER_DECLARED: approved L-04 target — одна isolated maintained **Windows 11 Pro x64**
VM, CPU-only, **4 vCPU / 8 GiB RAM / 64 GiB virtual local NTFS disk**, offline,
без shared host folders и production data. Это целевые параметры, не OBSERVED values.

## 3. Host inventory / readiness matrix

| Предмет | Статус | Фактическое основание / недостающее evidence |
|---|---|---|
| Неидентифицирующий VM alias и точное соответствие guest/host | NOT_PROVIDED | Нет выбранной VM; alias не придуман |
| Разрешённый guest access method | NOT_PROVIDED | Нет endpoint/канала и scope допуска; credentials только приватно |
| Windows11 Pro edition/version/full build/UBR | NOT_PROVIDED | Нельзя подставить Linux/старый Windows run |
| Guest x64, update/support/licensing | TO_VERIFY | Требуются guest inventory и приватное подтверждение поддержки/лицензии, без product key в Git |
| Hypervisor type/version, distinction host/guest | NOT_PROVIDED | Linux executor не объявляется hypervisor целевой VM |
| Выделенные vCPU/RAM/disk | TO_VERIFY | Сверить approved target; Linux ресурсы не используются вместо guest facts |
| Local NTFS guest volume, disk allocation/type | TO_VERIFY | Нужны guest/VM observations; не UNC/shared/sync/WSL storage |
| Изоляция от production | TO_VERIFY | Нет фактического inventory/owner attestation об отсутствии production data/accounts/keys |
| Offline/network restrictions | TO_VERIFY | Политика Codex egress не является политикой guest; требуется подтверждение на выбранной VM |
| Shared folders, clipboard, host mounts и прочие data bridges | TO_VERIFY | Описать фактические настройки, исключить перенос production/host data; shared folders отсутствуют по target, не по наблюдению |
| Snapshot/rollback и безопасная точка возврата | NOT_PROVIDED | Нужны приватные evidence/процедура, оператор и границы revert; snapshot не доказывает power-loss durability |
| Guest-local service/client accounts и admin authority | NOT_PROVIDED | Design account names утверждены; реальные identities, provisioning и разрешения ещё нет |
| Windows Python3.12 origin/exact version/bitness | NOT_PROVIDED | Linux3.12.14 не кандидатный Windows binary; требуется approved official origin/version и x64 artifact |
| Exact runtime artifact/hash | TO_VERIFY | Windows artifact не предоставлен; SHA не вычислялся, placeholder/нулевой hash не вставляется |
| Private pinned runtime/search paths | TO_VERIFY | План по S3.1a: installer-owned read-only runtime/Bin, private stdlib, без user site/PATH/cwd loading, bytecode writes off |
| Private evidence location/custodian/retention | NOT_PROVIDED | Конкретная приватная location и duration не выбраны; см. план §6 |
| Независимый observer / audit coverage | NOT_PROVIDED | Нет готового проверенного observer, покрытия и artifact; реализация/запуск этим заданием запрещены |
| Source/contract identity для этой проверки | OBSERVED | Exact base закреплён; future native source/artifacts ещё не существуют в этой задаче |
| Разрешение использовать конкретный host и выполнять admin/native operations | NOT_PROVIDED | L-01–L-04 — design approval, не разрешение на неуказанную машину |
| Native readiness / qualification | BLOCKED | Нет VM и необходимых отдельных approvals; ни одного native run |

Windows 10 IoT Enterprise LTSC2021/build19044 из старого portable R1 RESULT
не объявляется целевой Windows11 VM и не даёт readiness нового host.
Ни фактический Windows HostProfile, ни его profile_sha256 сейчас не сформированы.

## 4. Минимальные решения владельца

Ниже checklist для отдельного будущего решения, **не запрос выполнить admin actions
сейчас**. Пароли, токены, реальные SID, private VM paths и product keys не нужны в чате/Git.

| Решение | Минимальные входные сведения / точный вопрос | Gate |
|---|---|---|
| H-01: выбрать один host | Какая isolated Windows11 Pro x64 VM выделяется (публично только alias), как предоставляется approved guest access и приватное соответствие exact machine? Кто подтверждает build/UBR, hypervisor/resources/NTFS, поддержку и лицензию? | До native coding |
| H-02: подтвердить isolation/rollback | Кто подтверждает отсутствие production data/accounts/keys, offline restrictions, shared-folder/clipboard/mount settings; какой приватный snapshot/revert plan и кто оператор? | До native coding |
| H-03: разрешить bounded admin scope | Кто authorised owner/admin этой VM; какие exact операции разрешены: создание/удаление только lab accounts/group, SCM install/start/stop/delete, pipe/process/token/directory ACL setup/tests, injected failures/process stops, observer и rollback/cleanup? | Scope до native coding; установка/run — только после gate §5B |
| H-04: закрепить runtime/source | Какой official Windows Python3.12 x64 artifact/version/source разрешён, кто независимо сверяет runtime hash и private runtime inventory; какой exact source разрешён отдельным native task? | До native coding, повторная pin перед run |
| H-05: утвердить evidence boundary | Где приватно хранится evidence, кто custodian/reviewer, какой срок retention и очистка; каким независимым observer покрываются attempted writes и gaps; какие redacted summaries разрешены публично? | Boundary до coding; observer artifact и exact profile approval до run |

После получения данных требуется документированное решение владельца о пригодности
**конкретной** VM и отдельное scoped задание на native work. Одобрение этого отчёта
или alias само по себе не разрешает service installation. Если owner не владеет
admin authority выбранной машины, требуется отдельное разрешение её администратора.

## 5. Последовательность source/runtime/artifact hashes

**A — до native coding:** privately identify exact VM и verify inventory; owner
утверждает её использование, admin scope, source/runtime identity и evidence boundary.
Phase 0 этого не утверждает и не создаёт код. При отсутствии фактов — STOP.

**B — после отдельно разрешённой native разработки, до любого native run/install:**
получить реальные byte-exact native adapter/test harness/independent observer artifacts,
вычислить SHA-256 по определённым inventories, pin source/runtime. Собрать полный
canonical S3.1a HostProfile по исходной closed schema, независимо проверить hashes
и получить owner approval exact profile/hash и installation/test scope. Hash runtime
вычисляется только по доступному точному артефакту, не по названию версии.
Нет pre-build artifact hashes, self-hashes или выдуманных данных.

**C — любое relevant изменение:** host/build/UBR, runtime/source/artifact/observer
изменились → STOP, re-pin/reverify/reapprove до run. Нельзя повысить privileges,
расширить masks, buffers или deadlines для получения PASS без отдельного review.
S1/S2, LAB_ACL_1/LAB_LIMITS_1 не пересматриваются. Q1 и production profiles не выбраны.

Это approved sequencing из owner decision, не новая поправка HostProfile.
В этом документе нет JSON HostProfile с пустыми/предполагаемыми hashes.

## 6. План observer/evidence — без реализации и запуска

Предлагаемая граница следует S3.1a: отдельный администраторский harness/observer
собирает native API return codes, process/identity verdicts, timings, frame/request/
result hashes и attempted filesystem writes за весь broker lifetime, включая
ACCESS_DENIED и descendants. Отсутствие observer coverage означает BLOCKED;
«writes не замечены» не означает0 attempts. Проверку независимости и полноты
observer требуется отдельно зафиксировать до run; broker не аудирует сам себя.

Кандидатная стандартная location по контракту — lab-private Evidence subtree под
ProgramData/StoryStudioLab/S3_2. Это **план**, не созданный/проверенный каталог.
Фактический приватный путь, доступ и владелец должны быть выбраны и проверены
после approvals. Broker runtime не пишет regular files: installer/harness writes
разделяются по процессу/фазе. Cleanup только lab manifest allowlist и exact identities;
чужие/preexisting объекты не удаляются. Snapshot rollback только для выбранной lab VM.

EvidenceIndex при будущих runs связывает exact HostProfile/source/test/fixture hashes,
case/repetition, PASS/FAIL/BLOCKED и NATIVE/INJECTED/PURE. Native и injected failures
не смешиваются. Закрытый schema/limit S3.1a не расширяется. Private traces/dumps,
manifest и реальные SID/token/account/machine identifiers остаются вне Git.
Публично — только необходимые redacted summaries и hashes; retention/доступ/безопасная
очистка должны быть утверждены H-05. **Observer и EvidenceIndex сейчас не создавались.**

## 7. RISK-01–RISK-04 readiness

| Gate | Native evidence, которое ещё требуется | Сейчас |
|---|---|---|
| RISK-01 | Real dedicated account/restricted service SID, SeChangeNotifyPrivilege-only; identity/impersonation/TokenUser/RevertToSelf/residual-token fail-stop, no privilege fallback | BLOCKED — VM/approval/native adapter отсутствуют |
| RISK-02 | One WriteFile1052672 bytes, buffers4096,4 workers/1 dispatcher/queue2;5s deadlines/slow readers, observed cancellation completion и10 races на ARM/IO/COMPLETE | BLOCKED — native IO не выполнялось |
| RISK-03 | Exact SCM/process/token/pipe LAB_ACL_1 descriptors/masks, client query rights/server authenticity, squatting/PID reuse и forbidden-access checks | BLOCKED — реальных rights/token observations нет |
| RISK-04 | Actual SID→synthetic A/B binding, full bytes/principal/session scopes, replay/LOOKUP/lost ACK, restart UNKNOWN,32/33 | BLOCKED native — принят только прежний portable subset |

## 8. LT01–LT15 readiness (все native runs не выполнены)

| ID | Необходимая будущая проверка / prerequisite | Статус |
|---|---|---|
| LT01 |3 install/start/stop/cleanup cycles; collisions/identity/allowlisted cleanup | BLOCKED |
| LT02 |10 normal и10 forced crash/restart cycles; new incarnation, SCM/token checks | BLOCKED |
| LT03 |A/B/Denied/Admin, exact masks, denied broader pipe/process/token/service rights | BLOCKED |
| LT04 |Pipe squatting, owner/process/account/SV/ImagePath, PID race, production-reference rejection | BLOCKED |
| LT05 |Anonymous/wrong SID/SQOS/remote, controlled handle handoff и ACK identity | BLOCKED |
| LT06 |Native positive impersonation/revert + separately injected fail branches, no residual token | BLOCKED |
| LT07 |Native frame/message boundaries, partial/oversized/max payload/UTF-8/depth; no W1 on parser denial | BLOCKED |
| LT08 |4+1 clients, queue/deadlines/slow reader/max message и cancellation races | BLOCKED |
| LT09 |144 gate/decision cells с actual identity boundary:12 allow/132 deny | BLOCKED native |
| LT10 |B denials,5 CG×6 operations, missing grants, disabled PUBLISH_REVISION | BLOCKED native |
| LT11 |Native delivery/lost ACK/retry/full-byte/session/principal conflict/LOOKUP without new history | BLOCKED |
| LT12 |Service crashes/restarts, old incarnation UNKNOWN; no invented receipt/recovery | BLOCKED |
| LT13 |Pre-admission cold denial/quarantine/32 admissions/33rd refusal, no eviction or extra seed events | BLOCKED native |
| LT14 |Independent whole-lifetime attempted-write observer:0 forbidden attempts/0 protected writes, no audit gaps | BLOCKED — отсутствие измерения не выдаётся за0 |
| LT15 |Unchanged S2/golden/D-01 regressions плюс independent native wrapper/terminal checks | BLOCKED native |

Ранее принятые PURE_ONLY tests не заменяют ни одну native строку. Этот Phase 0
не запускает и не объявляет повторные portable tests PASS.
LAB_SERVICE_TESTED/PROCESS_QUALIFIED/POWER_LOSS_QUALIFIED не получены.

## 9. External-ideas gate и отдельный Windows baseline item

Перед результатом повторно прочитан реестр из отдельной ветки
`docs/external-ideas-adoption-register`, exact SHA
`4ad198a095b155a57d6d0b162fc977260119962b`, файл
`docs/architecture/EXTERNAL_IDEAS_AND_ADOPTION_REGISTER.md` через `git show`.
Merge/cherry-pick и изменение реестра не выполнялись.
Applicability gate 2026-11-09 для exact base: **применимых кандидатов нет**.

| ID / статус | Причина неприменимости |
|---|---|
| EXT-01 VidRusher / CANDIDATE |Media/proxy/scene selection не относится к host readiness |
| EXT-02 WanGP / CANDIDATE |Production workflows/GPU-provider ideas не разрешают storage/native work |
| EXT-03 LTX-Desktop / CANDIDATE |UX/optional generation capabilities не нужны этому preflight |
| EXT-04 Humanizer / CANDIDATE |Draft narration editing RU/UK вне host/security inventory |

Нет OWNER decision на конкретную интеграцию этим заданием; кандидаты не внедрялись,
код/модели/корпуса/зависимости не переносились, новые права/лицензии не утверждались.

Отдельный pending item: `tests.test_sprint23_2.Sprint232Tests.test_env_override`
классифицирован acceptance/QA как **BASELINE_PLATFORM_FAILURE**: literal POSIX path
assertion против Windows separators. Опубликованный Windows run841 OK/1 FAIL не
переписан в PASS; нативный повтор и ограниченное cross-platform test исправление
остаются отдельной задачей. Прежние Linux842 OK и PureWindowsPath diagnostic не
подтверждают реальную Windows11 VM. В Phase 0 тест не запускался и не изменялся.

## 10. Выполненные проверки и итог

Выполнены только read-only Git/docs/environment checks и создание одного Markdown:
точный remote base/HEAD, отсутствие существующей output branch, чтение документов
и реестра на заданном SHA, локальные ссылки/целостность таблиц, allowlist/размер,
`git diff --check` и staged diff. После push проверяются remote SHA и clean worktree.
Python unit tests не требуются документационным заданием и **не запускались**;
вызов `python --version` — только Linux inventory, не native/runtime qualification.

**BLOCKED_HOST_NOT_PROVIDED**: конкретная VM и её factual inventory/access не
предоставлены; отдельно не закрыты H-01–H-05 и будущие authorizations. Готовность
`READY_FOR_OWNER_HOST_APPROVAL` не заявляется. Получение checklist не является
разрешением автоматически создать VM/установить Python/службу или изменить ACL.

**STOP после публикации.** Native implementation, install, service/SCM/account/ACL
operations, observer и native tests не выполнялись. Нет elevated commands, изменений
Windows settings/permissions, protected writer, DPAPI/keys или production data.
Не изменены source/tests/S1/S2/D-01/golden/contracts/registry/dependencies/CI/main.
Без PR/merge/release. S3.2b coding и S3.3 не начаты; следующий owner gate — отдельный.
