# MVP-07 — фактическая проверка

Дата: 18 ноября 2026. Среда Linux x86_64, CPython **3.12.14**, Tcl/Tk **9.0.4**, FFmpeg/FFprobe **7.1.5-0+deb13u1**, pytest **9.2.0**. GUI: Xvfb 21.1.7 с доступным Cyrillic font path. CPU libx264; GPU, edge-tts и внешние генераторы не требуются.

**WINDOWS_NOT_RUN**. Нет проверки Windows 10/11, Windows shell player, HiDPI, реального non-admin Windows install, человеческого прослушивания/синхронизации или production readiness.

## Команды и exit codes

Команды выполнялись в отдельном worktree feature-ветки от exact base `a80aa0a71a41057bbe031d2a3bbbc1b210f2ab43` / tree `f528421025ee72a2ac70cd484fe4bc12a3b0505d`.

```bash
DISPLAY=:90 python -m unittest experimental_mvp.test_pipeline experimental_mvp.test_media_hub experimental_mvp.test_media_ui experimental_mvp.test_timeline experimental_mvp.test_timeline_ui -v
DISPLAY=:90 PYTHONPATH=<local-pytest-install> python -m pytest -q -ra tests experimental_mvp
DISPLAY=:90 PYTHONPATH=. python experimental_mvp/reports/evidence/mvp07/gui_smoke.py
python -m py_compile experimental_mvp/*.py
git diff --check
```

| Прогон | Реальный результат | Exit |
|---|---|---:|
| До расширения oracles: existing Pipeline + MediaHub tests | 21 tests PASS; original test files unchanged | 0 |
| Final experimental unittest, включая 4 реальные Tk smoke cases | **41 tests PASS**, 0 skips, **49.070 s** | **0** |
| New render-only oracles после добавления отдельного video/audio/frame guard | 5 tests PASS, 10.545 s | 0 |
| Final full pytest | **767 passed**, **1 skipped**, 3616 subtests passed, 269.44 s | **0** |
| Main-window GUI smoke | 7 tabs, RU topic correct, 8 scenes / 31 anchors, measured Audio Map, 515 Canvas items, 0 callback errors | 0 |
| Demo generation (local eSpeak + FFmpeg) | 2 local projects, scripts/cards/clips/audio, explicit timeline editing and JSON reopen | 0 |
| Two long final exports | 1920×1080 H.264/AAC/mov_text, exact frame budget, stream/container checks and complete decode | 0 each |
| 8 prerenders: RU/UA × anchor/scene/position/project | All generated and completely decoded; all independent preview durations within 0.1 s | 0 each |
| Syntax / staged diff whitespace | PASS | 0 |

В ходе разработки новые тестовые fixtures выявили собственные ошибки (неверная ожидаемая пропорция текста и запрещённая попытка перезаписать уже существующие anchors), а Canvas smoke выбирал перекрывающий другой якорь. Они исправлены; существующие опубликованные тестовые ожидания не изменены. При проверке lifecycle устранены dangling Tk timer callbacks. Финальные журналы — без этих development-сбоев. Результаты незавершённого/предыдущего прогона не выдаются за финальный результат.

## Проверенные оракулы

- Pure operation rollback: negative/zero/outside time, incompatible merge, invalid caption, rejected deletion. No partial project/history mutation.
- Create/duplicate stable deterministic new IDs; move/resize retain original IDs. Split/merge keeps actual video source interval semantics and provenance; deletion leaves physical files; Undo/Redo restores references/timing.
- Manual versus estimated scene/caption timing, whole/scene/cache measurements, order recalculation, explicit reconciliation. Repairing one scene succeeds while unrelated conflicts remain visible in another.
- Legacy projects without timeline fields; UTF-8/RU/UA, spaces/Cyrillic media paths; atomic save/reopen; permission-denied replace preserves old bytes; dirty state and stale main-project apply are checked.
- Actual mouse body drag, right-edge resize, keyboard movement, numeric edit, zoom and seek; Cancel on unsaved main-window edits; save-error keeps window open; preview worker cancellation does not mutate source/open a result.
- Real 15/60 FPS inputs, short/long source ranges, explicit HOLD_LAST_FRAME / LOOP, PNG/JPEG/WebP, crop + image motion, corrupted image/video and missing paths.
- Many successive small anchors, cumulative integer frame rounding, full decode and no false complete export.
- A deliberately truncated **0.5-second video** muxed with 2-second audio/subtitles is rejected even though subtitle/container duration can look correct. Duration guard independently checks video stream, audio stream, expected/actual frame count and measured source duration before renaming pending.mp4.
- Preview source project remains unchanged. Long demos have separate anchor/scene/project/seek prerenders and actual expected-duration checks.

## Демонстрационные MP4

| Параметр | RU | UA |
|---|---|---|
| Тема | Почему исчезли древние цивилизации? | Як виникли перші міста? |
| Сцены / якоря | 8 / 31 | 8 / 30 |
| Измеренная source MP3 duration | 220.248 s | 201.024 s |
| Final container duration | 220.248000 s | 201.033333 s |
| Final video duration | 220.233333 s | 201.033333 s |
| Final AAC duration | 220.189000 s | 200.954000 s |
| Video/audio delta | 0.044333 s | 0.079333 s |
| Expected / actual frames, 30 FPS | 6607 / 6607 | 6031 / 6031 |
| Guard tolerance | 0.1 s | 0.1 s |
| FFprobe / full decode exit | 0 / 0 | 0 / 0 |
| SHA-256 | `d74305de401a91710fd7d64cd3a2748edd26bfe4f2360e56193f950acdf4555c` | `a2a226eba1911e1531c5e5bce0f123ab0e62c8644235b570351b8efbac5a03db` |

Проверены отдельные потоки, а не только container duration, которую могут продлевать субтитры. Небольшие различия связаны с frame grid / MP3/AAC padding. Actual snapshots, Audio Timing Maps, duration-check.json, FFprobe, captions, command logs, input hashes and output hashes приложены. Полные review MP4 и previews находятся в workspace и выдаются ссылками handoff; исполняемые программы и binary releases не публикуются.

Для 8 previews независимо проверены expected versus actual duration, включая seek 2000 ms → остаток текущей сцены. Наибольшее отклонение в этом наборе около 40 ms. Final exports используют 1080p; демонстрационные previews — явно выбранную временную копию 640×360/30, без изменения сохранённого проекта.

GUI и отдельный кадр с наложенными subtitles осмотрены визуально. Это **не** полный человеческий просмотр/прослушивание. Произношение, смысловая синхронизация, pacing и историческая/редакционная пригодность остаются NOT_RUN / owner review. New per-cue timing_kind явно отличает сохранённую оценку от явно отредактированного интервала; наличие ручного override не означает проверку на слух.

## Воспроизводимость и ограничения

- `../demos/timeline/` включает готовые portable JSON и их локальные MP3/MP4/PNG. Нужны только Python/Tk и отдельно установленный FFmpeg, не платные аккаунты.
- `prepare_timeline_demos.py --espeak <path> --data <dir> --font <ttf>` заново генерирует fixtures. В этом прогоне использовались ранее документированные eSpeak NG 1.51 Debian packages, не Edge TTS. Script меняет duration и swap через transactional Editor, затем сравнивает saved/reopened JSON.
- Existing original-media notices и лицензии не менялись; новые схемы оригинальные, font binary / eSpeak runtime не поставляются. Условные изображения/видео не являются историческими доказательствами.
- OS player launch Windows, actual Google/API sessions, paid quota consumption, live speech service, ASR alignment, production gates/storage/permissions: NOT_RUN / not part of task.
- Final Git commit/tree и точные изменённые blob SHA содержатся в post-commit handoff manifest; сохранённые evidence относятся к выполненным командам, а не к предполагаемому Windows CI.

## Final full-suite summary

**767 passed, 1 skipped, 1 warning, 3616 subtests passed; exit 0.** Единственный skip: `tests/test_editor_preview.py:280`, Windows junction requires NTFS. Warning: pre-existing environment anyio plugin использует deprecated pytest CallSpec2 alias. Это не failing test. Полные журналы сохранены в evidence/mvp07/acceptance-full-pytest.txt и acceptance-unittest.txt; machine-readable summary — test-summary.json. После этого прогона implementation не менялась.
