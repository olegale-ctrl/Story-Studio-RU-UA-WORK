# MVP-07.1 — реальные результаты

Дата: 18 ноября 2026. Exact base `91d274c554433fbc2145d5fc6b6a591199c0243f`, tree `38e2579cc3294fa5cf57b4d1bc267a37bfe078f8`. Linux x86_64, UID 1000, CPython **3.12.14**, Tcl/Tk **9.0.4**, FFmpeg/FFprobe **7.1.5-0+deb13u1**, pytest **9.2.0**, Xvfb :91. Actual versions: evidence/mvp071/environment.json. **WINDOWS_NOT_RUN**.

## Наборы и exit codes

| Прогон | Результат | Exit |
|---|---|---:|
| Full suite на неизменённой exact базе, до implementation edits | 767 passed, 1 skipped, 3616 subtests passed; 210.42 s | 0 |
| Minimal initial reproducers, до исправлений D01–D05 | 5 tests, **5 FAIL** | 1 |
| Exact-base loop chain reproducer D06 | 1 FAIL: 10.000000 vs 241/24 = 10.041667 s | 1 |
| Timer cleanup reproducer D07 | FAIL; старый after callback остаётся | 1 |
| Final full pytest | **787 passed, 1 skipped, 1 warning, 3639 subtests passed**; **223.28 s** | **0** |
| Final combined experimental unittest | **61 tests, 0 skips**, **36.076 s** | **0** |
| Полная A/B/C/D mixed-media matrix | 4 real renders, decoded-frame counts + packet PTS + full decode PASS | 0 |
| Syntax / diff check | PASS | 0 |

Единственный full-suite skip: `tests/test_editor_preview.py:280`, **Windows junction requires NTFS**. Environment anyio plugin warning связан с deprecated pytest CallSpec2 alias; это не failing test. Старые test files/ожидания не изменялись; новый test_stabilization.py добавляет 20 tests. Linux POSIX readonly-directory oracle реально выполнялся не под root; Windows execution не выводится из него.

Команды (полные stdout/stderr и .exit.txt в evidence/mvp071):

```bash
# baseline: /workspace/work/mvp07, неизменённый HEAD 91d274c...
DISPLAY=:91 PYTHONPATH=<local-pytest-install> python -m pytest -q -ra tests experimental_mvp
# final: /workspace/work/mvp071
DISPLAY=:91 python -m unittest experimental_mvp.test_pipeline experimental_mvp.test_media_hub experimental_mvp.test_media_ui experimental_mvp.test_timeline experimental_mvp.test_timeline_ui experimental_mvp.test_stabilization -v
DISPLAY=:91 PYTHONPATH=<local-pytest-install> python -m pytest -q -ra tests experimental_mvp
PYTHONPATH=. python experimental_mvp/reports/evidence/mvp071/run_frame_matrix.py --output /workspace/work/mvp071-evidence/accepted-matrix
python -m py_compile experimental_mvp/*.py
git diff --check
```

## P0: конфликтные черновики и сохранение

Полный GUI/API сценарий: correct project → overlap → explicit draft save → destroy/reopen panel → conflict retained and approved=False → forced approved export rejected before final.mp4 → repair → check_project clean → Apply/Save/Reopen → explicit approval → actual successful export. Реальные Tk widgets, file-dialog responses автоматизированы; это не ручной Windows test.

Отдельные GAP/OVERLAP/OUTSIDE_SCENE/manual-map/missing/hash-changed/source-out-of-range drafts сохраняются и восстанавливаются, остаются unapproved и отклоняются preflight даже при принудительном approved=True. Invalid shape и corrupt JSON отвергаются, не повреждая предыдущий файл. Исходные bytes/IDs/provenance/rights сохраняются.

Atomic-save faults: write, flush, fsync, close, valid-JSON silent corruption/readback mismatch, непосредственно replace и actual POSIX non-root write denial. Во всех исполненных случаях прежний JSON неизменён/читается и temp очищен. Readback проверяет точные bytes, не только JSON syntax. Дополнительный Windows CRLF fault model сначала дал ERROR/exit 1; explicit newline="" исправляет его. Это не фактическое Windows execution. Windows real file locks/antivirus/ACL: NOT_RUN.

## P0: отмена preview

Проверены anchor/scene/project/position: cancel before FFmpeg, cancel during реально замедленного FFmpeg, повторный preview после отмены, source snapshot unchanged, no result publication, scoped-folder cleanup, все созданные subprocess handles завершены/reaped. Старый render_preview API также использует этот controller.

GUI late-result race: cancel между queue success и poll больше не открывает result. Destroy во время возврата worker очищает его конкретный результат; unrelated siblings/user files сохраняются. Poll/ttk progress callbacks после destroy очищены. Новый механизм history не создавался.

Измерено для конкретного real FFmpeg test: **0.5658 s** от начала controller-run до возврата, **0.2656 s** от request cancel до exit/reap, 1 owned process reaped. Это измерение данной Linux среды, не universal latency SLA. Independent probe/input-check timeout и OS-level refusal остаются ограничениями, см. LIMITATIONS.

## P0: frame/PTS matrix

Каждый якорь примерно 5–5.102 s, fractional milliseconds. Смешаны PNG motion, 15/60 FPS MP4 при 160×120 / 320×180, source in/out, FIT/CROP, explicit HOLD_LAST_FRAME / LOOP / ERROR+trim. Output — **160×90**. Audio — отдельно созданная инженерная тишина, не тест качества диктора.

| Config | Anchors / FPS | Audio, s | Expected / decoded frames | Video/audio delta, s | Full decode | PTS grid max error |
|---|---:|---:|---:|---:|---|---:|
| A | 30 / 24 | 151.445 | 3635 / 3635 | 0.013333 | PASS, exit 0 | < 0.000001 s |
| B | 60 / 25 | 302.958 | 7574 / 7574 | 0.002000 | PASS, exit 0 | 0 |
| C | 120 / 30 | 606.069 | 18182 / 18182 | 0.002333 | PASS, exit 0 | < 0.000001 s |
| D | 180 / 30 | 909.095 | 27273 / 27273 | 0.005000 | PASS, exit 0 | < 0.000001 s |

Допуск не увеличен: `max(0.1 s, 2/FPS)`. Pure cumulative budgets совпали с actual decoded counts; packet count/PTS проверены отдельно на отсутствие неучтённых gaps/duplicate timestamp, error ≤ 2 μs. Frame metadata само по себе не считается достаточным: исходный LOOP имел nb_frames=121, но nb_read_frames=120; исправление также проверяет реальное декодирование.

A сначала реально отказала: nominal 3635 frames при video 151.166667 s, audio 151.445 s. Guard не допустил final.mp4. Это сохранённое RED evidence D06; исправлены timestamps/output-rate, не tolerance/ожидания. A–D full **1080p stress: NOT_RUN**; 1080p functional compatibility покрыта существующей регрессией, не выдаётся за длинный 1080p benchmark.

## P1 и совместимость

Проверены Move/Resize/Split/Merge/Duplicate/Delete/Scene reorder/Caption edit с Undo/Redo, стабильность ID, provenance и license_status. Apply/Save/Reopen и stale external edit защищены. Whole/scene/cache audio, ручные/оценочные границы, изменение файла/длительности и повторное открытие покрыты старой и новой регрессией; invalid map не исправляется автоматически и не получает measured label без измерения.

MVP-05/06 tests сохраняют manual/compatible-LLM mock, 13-provider catalog, quota planner, media import, legacy JSON, RU/UA cues, WAV/MP3 и прежний FFmpeg. Реальных платных генераций/аккаунтов не было. JSON version не менялась; только non-finite values теперь отклоняются до записи.

## Внешние доказательства

Compact logs/metadata включены в Git-ветку в `evidence/mvp071/`. Полные A–D MP4, local source fixtures и raw snapshots — отдельный **workspace artifact, НЕ GitHub release/upload**:

- Path: `/workspace/work/mvp071-evidence/MVP_07_1_EXTERNAL_EVIDENCE.tar.gz`
- Size: **36925922 bytes**
- SHA-256: `41a67961a07e3c3497b2f5d099029897a3bd980d71fccc71c320b8a04ceaa23a`
- Content manifest: `/workspace/work/mvp071-evidence/EXTERNAL_EVIDENCE_CONTENTS.json` (64 payload files with byte SHA-256; manifest self-hash omitted).

Archive содержит evidence/fixtures/videos, а не документы, содержащие его собственный hash. Exact final Git commit/tree и modified blob hashes даны post-commit handoff manifest. Никакой Windows_PASS, human listening или production readiness не заявляется.
