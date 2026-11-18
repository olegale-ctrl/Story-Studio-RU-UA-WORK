# MVP-07.1 — реестр дефектов и reproducer

Base: `91d274c554433fbc2145d5fc6b6a591199c0243f` / tree `38e2579cc3294fa5cf57b4d1bc267a37bfe078f8`. Новые oracles: `experimental_mvp/test_stabilization.py`; существующие tests/expectations не изменены.

| ID / приоритет | Минимальный trigger, ожидаемое → фактическое поведение базы | Исправление | Статус |
|---|---|---|---|
| D01 / P0 | Загрузить overlap с прежним approved=True; Editor.save(allow_conflicts=True). Ожидается False → сохранён True. Старый build preflight уже запрещал сам конфликт, но draft approval оставался недостоверным | Только после успешного save draft-copy становится approved=False; не меняет state/saved snapshot при отказе записи | FIXED |
| D02 / P0 | Искусственный OSError в выходе из temp stream context. Ожидаются прежний JSON и cleanup → прежний JSON цел, temp остался | Общий try/finally охватывает создание/write/flush/fsync/close/readback/replace | FIXED |
| D03 / P0 | Fake writer пишет другой, но синтаксически корректный JSON. Ожидается отказ до replace → повреждённое содержимое принято и заменяет прежнее | Payload сериализуется до temp; после закрытия readback bytes сравниваются с payload и JSON разбирается перед replace | FIXED |
| D04 / P0 | Отменить scene preview сразу после render_scene. Ожидается cleanup только своего job → UUID preview folder остаётся | Thread-local preview session регистрирует только созданные данным вызовом folders; cancel/error удаляет их после закрытия/reap команд | FIXED |
| D05 / P0 | Worker поставил успешный path в очередь, затем пользователь отменил до poll. Ожидается no open/no success → результат открывается | Повторная stop-проверка при передаче и poll; lock/closed guard при destroy; exact-result cleanup | FIXED |
| D06 / P0 | LOOP 60→24 FPS, source 200–900 ms, за ним следующий якорь. Ожидаются непрерывные PTS/длина frame budget → цепочка 10.000000 s при 241 кадре (10.041667 s). Полная A дала drift 278.333 ms и была правильно заблокирована прежним guard | Явный encoder/output `-r` из **уже выбранного project FPS**, integer timebase / setpts для LOOP. Не меняется выбранная скорость источника и не увеличивается tolerance | FIXED |
| D08 / P0, stabilization-introduced | Text temp defaults to native newline translation; readback expects UTF-8/LF. Windows CRLF translation model reproduces false corruption refusal (exit 1); not a base-91 defect and not real Windows execution | Explicit newline="" keeps serialized/readback bytes identical; valid old CRLF JSON still loads | FIXED |
| D07 / P1 | Вызвать poll вручную, затем destroy; также destroy при активном progress. Ожидается no after callbacks → остаются poll/ttk timer callbacks | Cancel ранее scheduled poll перед новым; stop progress перед destroy, отмена своего after ID | FIXED |

Дополнительно прежний scene-preview API/main button подключён к тому же cancellable command controller и STOP-кнопке. Это консолидация существующего preview пути, не второй history, не новый player или архитектура MVP-08.

## RED → GREEN доказательства

- `evidence/mvp071/red-reproducers.txt`: 5 tests, **5 FAIL**, process exit **1**; до исправлений D01–D05.
- `red-loop-chain-base.txt`: D06 на **точном исходном base checkout**; 1 FAIL, exit 1. Один standalone loop clip при remux мог маскировать проблему; воспроизводимая минимальная цепочка содержит следующий якорь.
- `red-frame-duration-A.json` / `red-frame-matrix-A.txt`: expected frames 3635 = metadata frames, но video 151.166667 s против audio 151.445 s, delta 278.333 ms; passed=False, final.mp4 не опубликован. Это доказывает необходимость контроля timestamps/decoded frames, а не ослабления guard.
- `red-loop-and-timers.txt`: TimerCleanup oracle FAIL; содержащаяся там первоначальная single-clip probe PASS не выдаётся за reproducer D06.
- `red-windows-newline-model.txt`: additional fault model found during stabilization, ERROR/exit 1 before newline fix. Final portable tests pass; Windows remains NOT_RUN.
- Финальные GREEN: test_stabilization входит в полный experimental и full pytest suite; exact logs/counts/exits в MVP_07_1_TEST_RESULTS.md. A/B/C/D дополнительно прошли настоящий mixed-media render/count/decode и packet PTS checks.

## Сохранение и отмена: дополнительные oracles

Отказы write, flush, fsync, close, byte readback, replace и actual non-root readonly directory сохраняют предыдущий JSON и очищают temp там, где ОС разрешает unlink. Windows locks/antivirus на Linux не квалифицированы. Нельзя гарантировать физическое удаление при отказе самой файловой системы удалять файл.

Отмена проверена до запуска, во время реального FFmpeg, после команды, при queued success, уничтожении Tk panel и повторном запуске. Managed Popen terminate→wait→kill fallback применяется **только к handle процесса, созданного данной командой preview**. Нет kill по имени, PID scan, system-wide signals или удаления siblings. Cache готовой озвучки и пользовательские assets намеренно сохраняются.

Полный контроль main/CI/G3.2.1/providers не менялся. Итоговые commit/tree/blob SHA исправлений находятся в post-commit MVP_07_1_MANIFEST.json accompanying handoff; file list и Git diff позволяют независимо проверить каждое исправление. Известных незакрытых P0 в выполненной Linux-квалификации нет. Неисполненные Windows/human gates перечислены отдельно и не превращены в PASS.
