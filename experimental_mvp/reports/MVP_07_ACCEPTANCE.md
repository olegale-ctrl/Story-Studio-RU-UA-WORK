# MVP-07 — пакет независимой приёмки

**READY_FOR_INDEPENDENT_MVP_07_REVIEW** — экспериментальная реализация передаётся на аудит, не на merge/release или production. **WINDOWS_NOT_RUN**.

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Exact base commit: `a80aa0a71a41057bbe031d2a3bbbc1b210f2ab43`.
- Exact base tree: `f528421025ee72a2ac70cd484fe4bc12a3b0505d`.
- Feature branch: `feat/story-studio-experimental-mvp-07-visual-timeline`.
- Main observed before work: `a28277b4cb68a3db5da52edc598c37ce66314604`.
- Final commit/tree and changed-file blob SHA-1 + SHA-256 are in the **post-commit MVP_07_MANIFEST.json accompanying the handoff**. A tracked document cannot contain its own final commit/blob hash without self-reference. Use that manifest and Git commands below for exact verification.

## Область изменения

Новые `timeline.py` и `timeline_ui.py` отделяют transactional модель от Tk. Existing pipeline сохранён: изменения добавляют opt-in Audio Timing Map, явные video source/short-clip policies и cumulative frame budget, а не заменяют старый конвейер. `ui.py` подключает вкладку и unsaved-state guard; `media_ui.py` корректно отменяет Tk timers при уничтожении виджетов. Новые тесты и две локальные демонстрации добавлены в experimental_mvp. Существующие тестовые ожидания не изменены.

## Матрица приёмки

| Требование | Реализация / oracle |
|---|---|
| Canvas сцены/audio/anchors/captions, общая длина, указатель, zoom/scroll | TimelinePanel, actual Tk main-window smoke and screenshot, canvas events |
| Состояния imported/waiting/missing/changed/rights/conflict | Текстовые статусы и цвет, coverage overlays; selection status не зависит только от цвета |
| Drag/move/right-edge resize/numeric/keyboard | Canvas widget test: реальные synthetic mouse/key events, stable ID, no partial mutation |
| Create/duplicate/delete/split/merge/Undo/Redo | PureTests: deterministic IDs, preserved files/provenance/source intervals, incompatible/invalid operation rollback |
| Audio Timing Map | FFprobe adapter for whole/scene/cache, pure manual/estimated maps and reordering; unknown planning state явно обозначено |
| Audio changed / conflicts | Нет destructive auto-adjust; keep intervals, explicit reset/redistribute/fallback/trim; regression fixes one scene while other conflicts remain |
| AI short clips | New timeline default ERROR; explicit HOLD_LAST_FRAME/LOOP; source in/out + FIT/CROP; no speed change |
| Preview | Actual anchor, scene, project and position prerenders, separately decoded/duration checked; cancellation and non-mutation tests |
| Captions | captions_by_scene preserved by ID; selected text/time edit and boundary validation; explicit per-cue estimated/manual timing kind |
| Atomic save / unsaved edits | tempfile/replace, simulated denied replace preserves old file; dirty/Undo/Redo; main-window Cancel and failed Save keep it open; stale apply refused |
| Legacy compatibility | Existing experimental test suites unchanged and run; JSON without timeline stays valid through previous paths; old implicit hold logged |
| FFmpeg output | Both long demos actual 1920×1080 H.264/AAC/mov_text, full decode, 15/60 FPS clip normalization and image modes |
| Timing accumulation | Global cumulative integer-frame allocation, exact expected/actual frame counts and separate video/audio duration checks before final.mp4 |
| Failed/incomplete render | Expected short/corrupt/missing failures; deliberately truncated video cannot hide behind subtitle/container duration; no successful final published |
| Windows / system player / human listening | **WINDOWS_NOT_RUN**; shell playback and human listening NOT_RUN, explicit independent checklist |

## Демонстрации

- RU **«Почему исчезли древние цивилизации?»** — 8 сцен, 31 якорь, около 3:40.
- UA **«Як виникли перші міста?»** — 8 сцен, 30 якорей, около 3:21.

Portable projects, source editorial text, original PNG cards, local short MP4s (15/60 FPS) and eSpeak NG narration are in `../demos/timeline/`. `editing-demonstration.json` records explicit duration edits, position swap, manual overrides and save/reopen. No paid credits, media accounts, network TTS or third-party photographs/music are needed. The cards are labelled illustrative, not historical evidence. Content/scientific and listening review remain open.

Full MP4s and previews are separate workspace review artifacts linked in the handoff, not binary releases. FFprobe, Audio Timing Map, copied-input evidence, captions, frame/duration checks, hashes and actual command results are in `evidence/mvp07/` and MVP_07_TEST_RESULTS.md.

## Запуск и практический путь

```bash
python -m experimental_mvp.pipeline
```

Use Демо RU/UA → Временная шкала → Загрузить / Audio Map. Select an anchor/caption. Drag body/right edge or use numeric controls and keyboard. Adjust material source interval/fit/short policy in Интервал клипа. Explicitly reconcile conflicts; use Undo/Redo. Применить transfers the snapshot to the main editor and clears approved; Сохранить JSON writes the timeline snapshot atomically. Import additional media via existing Раскадровка, then apply/reload timeline. A stale snapshot cannot overwrite independently changed main fields.

Preview is temporary prerender; OS player is external. Export requires the existing explicit local experimental checkbox. It conveys no production rights or permissions.

```bash
python -m experimental_mvp.pipeline --project experimental_mvp/demos/timeline/ru.json --workspace <local-output> --approve
python -m experimental_mvp.pipeline --project experimental_mvp/demos/timeline/uk.json --workspace <local-output> --approve
```

## Независимая проверка

1. Verify exact base, parent, changed paths, modes and byte hashes against the post-commit manifest. No changes outside experimental_mvp are authorized.
2. Re-run full and targeted suites from the final exact commit; actual versions/counts/exit codes and known skip are in MVP_07_TEST_RESULTS.md.
3. Inspect both outputs, input hashes, source intervals and individual audio/video frame/duration checks, not only container duration. Decode the complete files.
4. Perform Windows/HiDPI/non-admin/file-dialog/OS-player tests from MVP_07_WINDOWS_CHECKLIST.md. RC-02 Windows baseline remains blocked; Linux results do not close it.
5. Listen to and watch both demonstrations end-to-end; review timing, pronunciation, scientific claims, rights and editorial readiness. These are not established by passing schemas/codecs.
6. Read MVP_07_LIMITATIONS.md: cooperative cancellation, current-scene seek preview, legacy behavior, trusted filesystem/TOCTOU and local evidence limitations.

```bash
git rev-parse HEAD HEAD^{tree} HEAD^
git diff --name-status a80aa0a71a41057bbe031d2a3bbbc1b210f2ab43 HEAD
git diff --check a80aa0a71a41057bbe031d2a3bbbc1b210f2ab43 HEAD
git diff --binary a80aa0a71a41057bbe031d2a3bbbc1b210f2ab43 HEAD > exact-mvp07.patch
git ls-tree -r HEAD -- experimental_mvp
```

**STOP:** независимый аудит ChatGPT и решение владельца. Ни merge, release, CI, main, G3.2.1, нормативные контракты, production storage, ни production permissions не являются частью поставки.
