# MVP-07.1 — независимая приёмка

**READY_FOR_INDEPENDENT_MVP_07_1_REVIEW**. Owner decision: MVP-07 ACCEPTED_WITH_LIMITATIONS, MVP-07.1 AUTHORIZED_EXPERIMENTAL; см. MVP_07_OWNER_APPROVAL.md. **WINDOWS_NOT_RUN**.

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Base commit: `91d274c554433fbc2145d5fc6b6a591199c0243f`.
- Base tree: `38e2579cc3294fa5cf57b4d1bc267a37bfe078f8`.
- Branch: `fix/story-studio-experimental-mvp-07-1-stabilization`.
- Remote main observed before work: `a28277b4cb68a3db5da52edc598c37ce66314604`.
- Exact final commit/tree and changed-file modes, blob SHA-1 and byte SHA-256: **post-commit MVP_07_1_MANIFEST.json accompanying handoff**. Self-referential commit/blob hashes cannot be embedded in their own tracked document. Use that manifest/Git commands for final identity.

## Изменения

| Файл | Изменение |
|---|---|
| pipeline.py | payload/readback/fsync/atomic replace cleanup; per-preview thread-local cancellation context; only-owned Popen terminate/wait/kill fallback; exact registered-folder cleanup; shared controller for movie/scene preview |
| timeline.py | confirmed draft clears approved only after successful save; timeline preview shares context/cleanup |
| timeline_ui.py | late cancel/queued success/closed-panel lock guards; exact returned-result cleanup; no dangling poll/progress timers |
| ui.py | существующая scene-preview кнопка получает STOP; queued canceled main preview не открывается |
| storyboard.py | выбранный output FPS явно задаётся encoder; LOOP integer timebase/PTS без сокращения хвоста/накопления drift |
| test_stabilization.py | 20 new regression tests, including original FAIL reproducers; existing test expectations unchanged |
| reports/evidence/mvp071/run_frame_matrix.py | pure budget + actual A/B/C/D mixed render, count/decode, PTS checks; не новая product feature |
| Шесть обязательных reports + compact evidence | Owner approval, results, defect register, Windows/static audit, limitations, acceptance |

Это минимальная стабилизация существующего экспериментального конвейера. Не добавлены второй механизм history, media-provider правила или architecture MVP-08. Валидные опубликованные experimental JSON совместимы, version не повышается. Non-finite JSON values отклоняются; invalid semantic drafts остаются unapproved и не экспортируются.

## Приёмочные gates

| Gate | Фактический статус |
|---|---|
| Exact base/tree/clean start | PASS; base-verification.json, отдельный worktree от exact SHA |
| Исходный test set | 767 passed / 1 skipped, exit 0 |
| P0 defects D01–D06/D08 | FIXED; minimal RED + GREEN regression и matrix evidence |
| Conflict draft save/reopen/repair/export | PASS, actual Tk + pipeline; forced approved does not bypass conflict preflight |
| Atomic-save refusal | PASS for executed write/flush/close/fsync/readback/replace/readonly faults; previous file intact |
| Preview cancellation | PASS before/during/after commands and queued result; no open/success on cancel, only owned process/folder cleanup |
| Frame budget | A/B/C/D actual render+decoded count+PTS PASS at 160×90; no tolerance increase |
| History + old features | PASS through 61 experimental tests, existing tests unchanged |
| Final full regression | **787 passed, 1 skipped, 3639 subtests passed**, exit **0** |
| Windows/static | STATIC_REVIEW_PASS / portable Linux CROSS_PLATFORM_TEST_PASS; **WINDOWS_NOT_RUN** |
| Human/production gates | NOT_RUN / not authorized; no production claims |

Нет известных незакрытых P0 в выполненной Linux квалификации. Это не закрывает Windows, hostile-filesystem/TOCTOU и production gates. Ограничения в MVP_07_1_LIMITATIONS.md обязательны для интерпретации PASS.

## Пакет

- MVP_07_OWNER_APPROVAL.md — точное решение и запреты владельца.
- MVP_07_1_TEST_RESULTS.md — actual versions/counts/exits и A–D результаты.
- MVP_07_1_DEFECT_REGISTER.md — expected/actual/minimal reproducer/fix/status.
- MVP_07_1_WINDOWS_CHECKLIST.md — static audit, PowerShell и реальные будущие PASS/FAIL критерии.
- MVP_07_1_LIMITATIONS.md — Windows, cancellation bounds, cleanup/FS risks, no 1080p long stress.
- `evidence/mvp071/` — исходные RED logs, GREEN/full logs, version record, matrix snapshots/metadata.
- External workspace archive: `/workspace/work/mvp071-evidence/MVP_07_1_EXTERNAL_EVIDENCE.tar.gz`, 36925922 bytes, SHA-256 `41a67961a07e3c3497b2f5d099029897a3bd980d71fccc71c320b8a04ceaa23a`. **Не опубликован в GitHub**; raw MP4s выдаются как local handoff artifact. 64 payload hashes перечислены в external contents manifest.

## Проверка независимым аудитором

```bash
git rev-parse HEAD HEAD^{tree} HEAD^
git diff --name-status 91d274c554433fbc2145d5fc6b6a591199c0243f HEAD
git diff --check 91d274c554433fbc2145d5fc6b6a591199c0243f HEAD
git diff --binary 91d274c554433fbc2145d5fc6b6a591199c0243f HEAD > exact-mvp071.patch
python -m unittest experimental_mvp.test_stabilization -v
python -m pytest -q -ra tests experimental_mvp
```

Сверить actual byte hashes, owner approval scope, reproducible failures on base и final GREEN. Проверить особенно LOOP packet timeline/decoded frames, а не только metadata count/container duration; cancelled preview folders/processes, save отказ перед replace; UUID siblings не должны удаляться. Повторить реальную Windows/ACL/locked-file/termination квалификацию отдельно.

После публикации feature-ветки — **STOP**. Ожидать независимого аудита ChatGPT и решения владельца. Не выполнять merge/release, не менять main/CI/G3.2.1, не подключать production storage/permissions и не начинать MVP-08 в этой ветке.
