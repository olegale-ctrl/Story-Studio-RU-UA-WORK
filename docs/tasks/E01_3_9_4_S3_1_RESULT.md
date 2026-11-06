# E01.3.9.4 / S3.1 — Результат Windows storage specification

**Дата:** 2026-11-06. **Статус:** design-only PROPOSAL, не утверждён и не реализован.

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Base branch: `docs/editorial-e01-3-9-3-s2-completion-s3-entry-proposal`.
- Exact base: `76c3478ed243317acc833eff5cfe2d767e886d11`.
- Branch: `docs/editorial-e01-3-9-4-s3-1-windows-storage-spec`.

## Созданные файлы

1. [E01_3_9_4_S3_1_WINDOWS_STORAGE_SPEC.md](E01_3_9_4_S3_1_WINDOWS_STORAGE_SPEC.md).
2. Этот `E01_3_9_4_S3_1_RESULT.md`.

Существующие файлы, implementation S2.1–S2.4, tests/golden vectors и E00/A/O/D/S1
не изменены. Policy GitHub прочитана непосредственно из отдельного коммита
`ceca15c20cedd5277ad0bdafc418eef149e7bc7b`; её merge не предполагался.

## Что подготовлено

Спецификация содержит все 12 обязательных областей, обозначенных WS01–WS12.
Для каждой указаны concrete mechanism, основание, failure behavior, способ
проверки, residual risk и необходимость отдельного approval. Отдельно маркируются:

- **I** — уже approved invariant, не пересматриваемый этим proposal.
- **F** — документированный Windows API факт со ссылкой на первичный источник.
- **P** — проектное решение, ещё требующее согласования.
- **Q** — требование квалификации с actual Windows evidence, которого сейчас нет.

Определены service/user/admin границы, named-pipe authentication и SID provenance,
CommandGrant отдельно от каждой GateDecisionGrant, protected policy lookup,
freeze/recheck/activation lock order и controlled impersonation/RevertToSelf.
DPAPI current-user service account — кандидат с qualification gate; machine scope
не объявляется service isolation. Rotation, key export и auto-key regeneration
не допускаются по S1 v1.

Подробно отображены W0–W9 на независимые file/journal/anchor operations. Для primary
предложен same-volume MoveFileExW recipe, соответствующий earlier architecture
proposal; это кандидат на испытания, не доказанная atomic/power-safe операция.
Flush temp, live namespace CP, final anchor и delivered receipt разделены.
Explicit backup/forensic C, uncertain IO outcome, journal partial writes и failure
после intent не смешиваются с successful finalization.

Отдельно зафиксированы: отсутствие общего Windows directory fsync promise,
unsupported REPLACEFILE_WRITE_THROUGH, ограниченные MoveFileEx write-through
semantics, sharing/ACL/identity checks и отсутствие silent fallback к другому API.
Ни file flush, ни «успешный BOOL», ни process-kill test не подтверждают power loss.

Startup/replay сохраняют D-01 binding: lineage/container selector сверяется с
actual authenticated parent epoch до наследования history/IDs/order. Старый
APPROVE receipt после REVOKE — history, не renewed authority. Missing anchor,
corrupt proof, wrong epoch, partial COMMIT и unknown primary дают block, а не
fabricated recovery. PUBLISH_REVISION DISABLED; reconstruction OFF.

## Открытые решения владельцу

Реестр O-WIN-01–O-WIN-08 в спецификации охватывает:

1. Service account/SID mode/privileges, runtime/installer/update packaging.
2. Pipe descriptor/masks, SQOS/server identity, time/resource bounds и closed
   upload/review/status control protocol; конкретный protected policy provider.
3. DPAPI/profile/provisioning/dump policy; separate key-disaster decisions.
4. Managed layout/security descriptors и closed native root binding schema.
5. Win32 handle/replace/flush recipe, E00-compatible byte-range lock convention.
6. **Q1-A либо Q1-B**, backup destination/privacy/manifest/cadence/retention.
   S1 предложения 32 GiB / 80% / 64 MiB / 2 GiB / weekly / 4 copies не defaults.
7. Safe read diagnostics/RU-UK messages и privacy/retention.
8. Exact Windows/NTFS/hardware profiles и qualification plan/acceptance levels.

Windows 10/11/VM templates остаются вариантами: edition/full build/UBR, поддержка
OS/ESU, driver/firmware/controller/cache должны быть выбраны отдельно. Исторический
build-family label S1 не превращается в автоматически одобренный актуальный host.

S1 не содержит complete IPC control-plane и native deployment catalog schemas.
Они явно отмечены как functional blockers до approval, а не заполнены permissive
paths/overrides. Это открытые implementation решения, не основание менять S1.

## Граница первой реализации и qualification

Предложенный S3.2 после **отдельного approval** ограничен service lifecycle,
IPC/identity/access и bounded protocol parsing с mock store/provider в isolated
Windows lab. Никаких production keys, protected writer, real registration или
live history migration. Operational writer/backup/cutover — отдельные задания
после применимых контрактов и выбранного стенда.

14 gates T01–T14 охватывают SID/ACL/IPC/key, W0–W9, process kill/repeated recovery,
power cut, disk-full/partial write, access denied, malformed MAC/type/epoch,
D-01, old backup/REVOKE, sessions/policy/locks, lifecycle и offline drafts.
Qualification levels разделены: DESIGN_ONLY, PROCESS_QUALIFIED и отдельно
POWER_LOSS_QUALIFIED. Потеря acknowledged B/order/receipt — failure power-loss gate,
даже если recovery безопасно заблокировал authority.

## Фактически выполненные проверки

- Exact base FETCH_HEAD/HEAD совпал с заданным SHA; исходное дерево было чистым.
- Изучены approved D/S1, E00 на указанном commit, A/O, S2 closeout и D-01 result.
- Windows API assertions сверены с Microsoft Learn и официальным MicrosoftDocs
  SDK source. В спецификации 19 уникальных primary-source URLs; некорректные
  предварительные header-path URLs заменены правильными canonical references.
- Проверены sections 0–13, все 12 decision cards с необходимыми полями, одна
  таблица W0–W9, gates T01–T14 и полный реестр O-WIN-01–O-WIN-08.
- Проверены local Markdown links, status/disabled gates, fence balance и отсутствие
  утверждённых numeric Q1/platform defaults.
- Проверены diff whitespace, exact staged file list, размеры обоих новых текстовых
  файлов (<10 MiB каждый), отсутствие других additions/modifications и отсутствие
  изменений golden/code/contracts. `.gitignore` проверен и не изменён.

Unit tests, service install, IPC/DPAPI/ACL experiments, native writer tests и
Windows/process/power-loss qualification **не запускались**: executable код не
менялся и среда этого задания — Linux. Число 808 tests в S2 closeout — прежний
reported результат S2.4, а не новый прогон этого documentation task.

## Ограничения и STOP

Спецификация проверяема через named gates, но ещё не прошла owner approval или
экспериментальную квалификацию. Не заявляются production security, Windows
process-crash consistency или power-loss durability. Admin/service compromise,
coherent full protected rollback и key/profile disaster остаются описанными рисками.

Только два docs additions. Нет executable service/IPC/writer, новых dependencies,
реальных ключей/защищённых данных, media/models, PR/merge/release/main changes.
S3.2 не начинался. После публикации — **STOP**, дальнейшая реализация требует
отдельного утверждения.
