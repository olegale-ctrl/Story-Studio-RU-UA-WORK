# MVP-07.1 — Windows static audit и independent checklist

**WINDOWS_NOT_RUN.** Windows 10/11, PowerShell, Windows file locking/antivirus/non-admin profile и native OS-player здесь не выполнялись.

| Категория | Статус | Область доказательства |
|---|---|---|
| Runtime static review | STATIC_REVIEW_PASS | Pathlib, Unicode argv, shell=False, NamedTemporaryFile(delete=False, newline=""), closed handle before Path.replace/os.replace; Popen terminate/kill/wait вместо POSIX signals/groups |
| Portable regression oracles executed Linux | CROSS_PLATFORM_TEST_PASS | Семантика local JSON/preview/timing/history; это не свидетельство исполнения на нескольких ОС |
| Actual POSIX non-root readonly directory | Linux-only test PASS | На Windows этот oracle намеренно skip; проверить ACL/locked file отдельно |
| Windows 10/11 | WINDOWS_NOT_RUN | WINDOWS_PASS разрешён только после исполнения checklist на конкретной версии |

New save readback is explicitly UTF-8/LF: newline="" prevents a Windows CRLF translation mismatch. A portable fault model failed before the fix and passes afterward; this is not Windows execution.

`os.startfile` остаётся внутри `os.name == 'nt'`; xdg-open/open — в соответствующих OS ветках. В runtime нет hard-coded `/workspace` путей; такие пути в evidence — адреса фактически исполненного Linux прогона. Frame runner принимает `--output`, обычные пути с Unicode/пробелами. Новое управление subprocess не использует os.kill, killall, POSIX process groups или завершение посторонних процессов.

## Исполнение владельцем/независимым Windows оператором

Зафиксировать exact final commit/tree из handoff manifest, Windows edition/build, CPU/RAM, Python x64/Tk patchlevel, ffmpeg/ffprobe build, обычный user profile, scale 100/150%, действительные exit codes и артефакты. Версия прошлого Windows RC не является подтверждением нового запуска.

```powershell
$env:STORY_MVP_HOME = Join-Path $env:USERPROFILE 'StoryStudio-MVP071-Independent'
python --version
python -c "import struct,tkinter; r=tkinter.Tk(); print(struct.calcsize('P')*8,r.tk.eval('info patchlevel')); r.destroy()"
ffmpeg -version
ffprobe -version
python -m experimental_mvp.pipeline --check
python -m experimental_mvp.pipeline
python -m unittest experimental_mvp.test_pipeline experimental_mvp.test_media_hub experimental_mvp.test_media_ui experimental_mvp.test_timeline experimental_mvp.test_timeline_ui experimental_mvp.test_stabilization -v
python -m pytest -q -ra tests experimental_mvp
```

1. Создать overlap/GAP/outside черновик → явно save draft → закрыть/открыть → approved=False, IDs/assets/provenance/conflict сохранены. Попытка export должна отказать; даже вручную установленный approved=True не обходит preflight. Исправить → Apply/Save/Reopen → явно подтвердить локальную сборку → успешный MP4.
2. Повторить manual Audio Timing Map mismatch, missing file, changed SHA и source interval вне реального видео. Повреждённый JSON/shape не должны повредить уже сохранённый файл.
3. Проверить Unicode/пробелы, запрет записи через ACL, locked destination, TempFile create/write/close/readback/replace failures. Предыдущий JSON неизменён и читается; inspect temp cleanup. Реальный antivirus/foreign process lock — отдельно, не считать Linux mocks Windows PASS.
4. Для anchor/scene/project/position и старой scene-preview кнопки: cancel до/во время FFmpeg, закрытие во время preview, queued-result cancel, повтор preview. Не должен открываться отменённый result. Проверить reaped managed FFmpeg PID, отсутствие висящего процесса, source project unchanged и cleanup только конкретного UUID job. Записать request→exit latency.
5. Move/Resize/Split/Merge/Duplicate/Delete/Scene reorder/Caption edit → Undo/Redo. Проверить ID, provenance/license_status, atomic failure, unsaved Cancel/Save failure, stale external-project change.
6. Whole/scene/cache audio, ручные/оценочные границы и повторное открытие. Неподготовленная или ошибочная manual map не исправляется молча и не получает measured label без FFprobe.
7. Повторить A/B/C/D при 160×90, затем при желании отдельную 1080p performance qualification. Frame count, packet PTS, source in/out/FIT/CROP/HOLD/LOOP и full decode. Output FPS берётся из явного профиля/задания; AI playback speed не меняется скрыто.

```powershell
$env:PYTHONPATH = '.'
python experimental_mvp/reports/evidence/mvp071/run_frame_matrix.py --output "$env:STORY_MVP_HOME\frame-matrix"
ffprobe -v error -count_frames -select_streams v:0 -show_entries stream=nb_read_frames,nb_frames,duration -of json <final.mp4>
ffmpeg -v error -xerror -i <final.mp4> -f null -
```

PASS только при совпадении фактических кадров с cumulative budget и stream delta в заявленном допуске. FAIL/NOT_RUN сохраняются явно; человеческое прослушивание/просмотр не заменяется codec result. После отчёта — независимый аудит и решение владельца; никакого CI/merge/release/main/G3.2.1/production шага автоматически.
