# E01.3.9.4 / S3.1a — Result

Дата: 2026-11-06. **PROPOSAL — НЕ УТВЕРЖДЁН.**

## Основание и результат

Базовый commit: `c3f65c5253c5e02be17fcf8676f280e6e83d9e63`.
Ветка: `docs/editorial-e01-3-9-4-s3-1a-lab-execution-contract`.

Подготовлен [Windows Lab Execution Contract](E01_3_9_4_S3_1A_LAB_EXECUTION_CONTRACT.md)
для независимой проверки и решения владельца перед экспериментом S3.2.
Это проектирование; служба, установщик и Windows adapter не создавались.

Созданы только два документа:

- `docs/tasks/E01_3_9_4_S3_1A_LAB_EXECUTION_CONTRACT.md`;
- `docs/tasks/E01_3_9_4_S3_1A_RESULT.md`.

## Что определено

- Отдельные SCM identity, accounts, service SID, pipe, installer/runtime paths,
  защищённый manifest и ограниченная очистка без захвата существующей установки.
- Шесть SDDL templates, конкретные access masks, проверка server process/token,
  SID клиента из impersonated token, запрет anonymous/remote/wrong SID,
  обработка pipe squatting и fail-stop при невозможности восстановить service token.
- Отдельный LAB framing `SSLB`, закрытые message schemas, byte-mode client,
  response ACK, ограничения размеров, четыре workers, один dispatcher, очередь два,
  deadlines и правила cancellation без повторного использования незавершённого IO.
- Только синтетические fixtures: пять CommandGrant policy cases и все 12 независимых
  gate/decision grants. Матрица 12×12 требует 12 разрешений и 132 отказа.
- RAM-only admission/replay cache; после перезапуска UNKNOWN_AFTER_RESTART,
  incarnation-bound request IDs, отсутствие фиктивного durable recovery.
- Lab wrapper не экспортирует S1 Receipt/MAC или protected evidence; production
  acceptance лабораторного endpoint/формата запрещена.
- LT01–LT15: lifecycle, ACL/SID, impersonation/RevertToSelf, malformed/oversized
  frames, concurrency, повторные запросы, потери ответа, crashes и аудит отсутствия
  protected writes. Native, injected и pure observations различаются.

## Проверки и границы доказательств

Выполнены документационные проверки: локальные Markdown-ссылки, уникальность
разделов, баланс fenced blocks, точный состав добавленных файлов и `git diff --check`.
Маски проверены арифметически, SDDL templates — структурно; это не native AccessCheck.
Три синтетических canonical JSON/frame examples проверены Python и независимо
Node.js: длины, заголовки и SHA-256 совпадают с буквальными значениями документа.
Сверены рекомендации с review/lab gate и S3.1; использованы ссылки на документацию
Microsoft по named pipes, tokens, service security и отмене IO.

Windows SCM/pipe/token/ACL tests, ConvertStringSecurityDescriptorToSecurityDescriptor,
AccessCheck, process kill и power-loss experiments **не выполнялись**.
Unittest не запускался: исполняемые файлы и существующие тесты не изменялись.
Golden vectors S2 и утверждённые документы не изменены.
Ни один из labels LAB_SERVICE_TESTED, PROCESS_QUALIFIED, POWER_LOSS_QUALIFIED
этой документационной работой не получен.

## Открытые решения владельца

L-01: отдельная identity/account/SID, privileges, пути и cleanup.
L-02: exact ACL/masks, IPC framing, limits, deadlines и cancellation profile.
L-03: mock fixtures, grant mapping, RAM-only replay и безопасный result wrapper.
L-04: фактический Windows build/UBR, lab profile и evidence/acceptance matrix.

Для каждого приведены конкретная рекомендация, альтернативы, последствия и условия
приёмки. Значения не становятся утверждёнными по умолчанию. Q1 и реальные Windows
production deployment profiles остаются неутверждёнными; native API assumptions
требуют экспериментальной проверки выбранного профиля.

E00/A/O/D/S1, S2.1–S2.4 и S3.1 не изменены. PUBLISH_REVISION — DISABLED;
partial COMMIT reconstruction — OFF. Нет production-кода, зависимостей, ключей,
медиа, protected writes, PR, merge, release или изменений main.

**STOP. S3.2 не начат; нужны независимая проверка и утверждение владельца.**
