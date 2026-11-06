# E01.3.9.4 / S3.2 — Preflight

Дата: 2026-11-06. Статус: **BLOCKED_PRE_IMPLEMENTATION**.

## База и полномочия

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Base branch: `docs/editorial-e01-3-9-4-s3-2-approved-lab-task`.
Exact base: `0fa6b61aebc7689f787e2dd276607a2f0084b7ac` (FETCH_HEAD совпал).
Output branch: `feat/editorial-e01-3-9-4-s3-2-windows-lab-broker`.

Полностью прочитаны [Owner decisions](E01_3_9_4_S3_2_OWNER_LAB_DECISIONS.md),
[нормативное задание](E01_3_9_4_S3_2_CODEX_TASK.md),
[LAB contract](E01_3_9_4_S3_1A_LAB_EXECUTION_CONTRACT.md) и
[independent review](E01_3_9_4_S3_1A_INDEPENDENT_REVIEW.md).
LAB contract идентичен редакции `cf70b8c0a93841f2bff272b584a2106374e3016f`;
review идентичен редакции `818551171d1e955cf1dca6ddaf8cc54994c7528c`.
L-01–L-04 утверждены только в лабораторном объёме: старые PROPOSAL/status строки
исторических документов читаются вместе с последующим owner decision.

Phase 0 §B предписывает: при отсутствии exact HostProfile, решения о sequencing
или разрешения конкретной VM публиковать только preflight/result и остановиться.
Общее одобрение лабораторного проекта не является разрешением установки на
неуказанную машину. Ни одно из трёх условий сейчас не закрыто.

## Фактическая среда и отсутствующий HostProfile

Проверены текущая managed environment и локальная ОС: Linux x86_64,
`uname -s` = Linux; доступный Python и проектная `.venv` — Python 3.12.14.
Environment status: connected/running, observations_current=true; нет настроенных
runtime variables, secrets или outbound identities для Windows VM.
Network policy v1: vpn_configured=false, TCP domains/IP ranges пусты.
Desktop capability сама по себе не является Windows VM или разрешением SCM.
В контексте задачи и нормативных документах нет идентификатора/канала доступа
к отдельно разрешённой Windows VM. Поиск HostProfile/preflight filenames в
репозитории не обнаружил предоставленного фактического профиля. Это не утверждение,
что у владельца нет VM; она не предоставлена для этой сессии.

| Необходимые сведения | Фактический статус |
|---|---|
| Конкретная isolated Windows 11 Pro x64 VM, идентификатор/доступ | Не предоставлены |
| Edition/version/full build/UBR и hypervisor | Не установлены наблюдением |
| 4 vCPU, ≥8192 MiB RAM, ≥65536 MiB local NTFS | Утверждён target, фактические ресурсы не проверены |
| Offline, no shared folders, no production data/accounts/keys | Требуется inventory конкретной VM |
| Поддержка ОС и лицензия | Подтверждение отсутствует |
| Private Windows Python source/version/hash, immutable search paths | Не выбраны/не проверены |
| Admin/install authority и test-account provisioning | Отдельного разрешения нет |
| Private evidence location и независимый attempted-write observer | Не предоставлены/не квалифицированы |
| Exact canonical HostProfile и SHA-256 | Отсутствуют; placeholders не выдаются за профиль |

Linux характеристики не подставлены в Windows HostProfile. Здесь нет вымышленного
build, UBR, SID, UUID установки, runtime/artifact hash или evidence trace.

## Предложение по sequencing — требует решения владельца

S3.1a §7.1 требует полный HostProfile до coding/run, но включает
adapter_artifact_sha256, test_artifact_sha256 и observer_artifact_sha256.
Будущие артефакты до их создания хешировать невозможно. Нормативное задание §B.3
признаёт эту цикличность; самостоятельно менять порядок нельзя.

Предлагается отдельно утвердить следующий порядок:

1. До разработки: определить конкретную VM и privately проверить edition/build/UBR,
   hypervisor/resources/NTFS/isolation, поддержку/лицензию, private runtime origin,
   version/hash, source base, evidence boundary, admin identity и scope установки.
   Утвердить host/runtime/source параметры и явное разрешение начать Phase 1.
   Это approval record, ещё не полный canonical HostProfile.
2. После разрешённой разработки: собрать и зафиксировать adapter/tests/observer,
   определить byte-exact artifact inventories и SHA-256; pin source commit и private
   runtime. Не использовать нулевые/предполагаемые digest и self-referential hash.
3. До любых native испытаний/установки: сформировать полный HostProfile по исходной
   closed schema, независимо проверить hashes, получить approval exact profile/hash
   и отдельное разрешение admin operations на идентифицированной VM.
4. Любое изменение host/build/runtime/artifacts требует нового pin/review до run;
   несовпадение — STOP. Evidence привязывается к фактическому полному профилю.

Это предложение к согласованию, не внесённая поправка S3.1a. Порядок упаковки
артефактов и observer должен быть reviewable до hash approval. Сейчас шаг 1
не выполнен, поэтому Phase 1 не разрешена.

## План native identity/ACL prechecks после разрешения

Администратор предоставляет reversible provisioning только для конкретной VM:
создание SSLabBrokerSvc, SSLabClientA/B/Denied, SSLabClients; logon rights;
SCM registration/start/stop/delete; exact directory/process/token/pipe descriptors;
private observer/evidence и cleanup. Пароли, реальные SID и private manifest — вне Git.
Не запускать provisioning и не искать обход admin gate в текущей среде.

LookupAccountNameW разрешает SA/SV/CG и A/B/Denied в реальные различные local SID;
IsValidSid/тип/provenance и account membership проверяются независимо. Подстановка
только в шесть exact SDDL templates LAB_ACL_1; parse через Windows API, readback
owner/protected DACL/ACE и native positive/negative access checks. Не сравнивать
одни display names. До endpoint проверить SCM own-process/dedicated account,
SERVICE_SID_TYPE_RESTRICTED, enabled/restricted SV, required privilege list только
SeChangeNotifyPrivilege и фактические token privileges. Невозможность корректной
конфигурации означает FAIL/STOP, без SeImpersonate/UNRESTRICTED fallback.

Client mask 0x00120083 без bit 0x4; process 0x00121000, token 0x00020008,
service 0x00020005. Проверять QUERY доступ A/B и отсутствие VM_WRITE/DUP_HANDLE/
TOKEN_DUPLICATE/WRITE_DAC/create-instance grants; Admin не получает editorial grant.
Every-connection client server-auth и every-message server impersonation включают
ACK. RevertToSelf и отсутствие residual token обязательны; failure — fail-stop
процесса без response/model/logging под чужим token. Actual результаты этих проверок
сейчас неизвестны: Windows SCM/SDDL/token/IPC недоступны и не испытаны.

## Test-first план RISK-01–RISK-04

| Gate | Положительные и отрицательные доказательства после разрешения | Сейчас |
|---|---|---|
| RISK-01 | Native account/restricted SID/minimal privileges; A/B Identification; Anonymous/wrong SID/SQOS; injected impersonate/query/revert/residual faults и native restoration; LT01–LT06 | BLOCKED |
| RISK-02 | One WriteFile EXECUTE 1,052,672 bytes, buffers4096; boundary/partial/oversized; slow reader, queue2/workers4+1, exact deadlines; 10 cancellation races каждого ARM/IO/COMPLETE; LT07–LT08 | BLOCKED |
| RISK-03 | Independent SCM/process/token/pipe descriptor readback + allowed QUERY и forbidden broader access; squatting/PID reuse/server mismatch; LT03–LT06 | BLOCKED |
| RISK-04 | Full request/principal/session binding; unauthorized digest-only LOOKUP; exact replay после PREPARE/INTENT/COMMIT/lost ACK, restart UNKNOWN; 32 admissions/33rd denial; LT09–LT13/LT15 | BLOCKED |

Все 144 gate/decision cells и 30 command-policy/operation cells остаются обязательны.
LT14 требует независимый аудит attempted writes, включая ACCESS_DENIED и descendants;
audit gap — BLOCKED. Native и injected наблюдения различаются. Failure любого
параметра — STOP с bounded reproducer/native code, не повышение limits/privileges.
Существующие pure S2 regressions проверяются отдельно; они не заменяют lab tests.

## Выход Phase 0

Созданы только этот документ и [result](E01_3_9_4_S3_2_RESULT.md).
Исполняемый код, service/installer/client/tests для LAB не создавались.
Не выполнены SCM/account/ACL изменения или protected writes; installer/runtime
не запускались. Никакой native qualification и EvidenceIndex не заявлены.
E00/A/O/D/S1/S2/golden/S3.1a неизменны; PUBLISH_REVISION DISABLED,
partial COMMIT reconstruction OFF. Q1/production profiles не утверждались.

**BLOCKED_PRE_IMPLEMENTATION. STOP до отдельного закрытия всех Phase 0 gates;
S3.2 implementation и S3.3 не начаты.**
