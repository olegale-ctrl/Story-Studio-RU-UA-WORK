# Actual test report — 2026-11-18

Environment: Linux x86_64; CPython **3.12.14**; Tk **9.0.4**; FFmpeg and ffprobe **7.1.5-0+deb13u1**; pytest **9.2.0** installed separately in a test workspace. edge-tts **not installed**. GUI checks use a separate Xvfb 21.1.7 virtual display, with test-only Cyrillic-capable font paths. Windows 10/11, Python 3.10/3.13 and Windows Credential Manager were **NOT_RUN** in this task.

| Actual command / check | Result | Skips | Exit |
|---|---|---:|---:|
| Original RC-02 `unittest experimental_mvp.test_pipeline -v` | 9 tests PASS, 3.593 s | 0 | 0 |
| Final `unittest experimental_mvp.test_pipeline experimental_mvp.test_media_hub experimental_mvp.test_media_ui -v` with display | 22 tests PASS, 9.555 s | 0 | 0 |
| Final `pytest -q -ra tests experimental_mvp` with display | **748 passed**, 3616 subtests passed, 206.47 s | **1** | **0** |
| Exact baseline RC-02 `--check` under Xvfb | Tk, local 1080p codec/subtitle mux and burned-caption preview PASS | 0 | 0 |
| New `--check` before display setup | Tk FAIL: no DISPLAY; media checks PASS | N/A | 1 |
| Final new `--check` under Xvfb | Tk, FFmpeg, ffprobe, local 1080p H.264/AAC/mov_text and caption preview PASS; no Edge required | 0 | 0 |
| Full Tk `reports/evidence/gui_smoke.py` | Six tabs; RU 8 scenes/40 anchors; field form, storyboard save/reopen; UA 8 scenes; no callback errors | 0 | 0 |
| Final catalog planner regression | 2 tests PASS | 0 | 0 |
| Demo preparation using local eSpeak NG 1.51 and FFmpeg | RU/UK cards and MP3 created; no external inference/generation | 0 | 0 |
| FFprobe + complete FFmpeg decode of both long demos | H.264/AAC/mov_text, 640×360, 24 FPS; decode stderr empty | 0 | 0 |
| Compile and `git diff --check` | PASS | N/A | 0 |

The single pytest skip is `tests/test_editor_preview.py:280`: **Windows junction requires NTFS**. The one warning is an existing environment anyio pytest plugin deprecation (`CallSpec2` alias with pytest 9), not a failed test. Full logs and machine-readable counts are in evidence/. Earlier development runs included a case-sensitive error-message assertion failure and an initial smoke-harness lookup error; these were corrected and re-run. Only final passing runs are used as acceptance results.

## Windows / Linux coverage matrix

| Scenario | Linux actual evidence | Windows 10/11 |
|---|---|---|
| GUI launch, RU/UK projects, save/reopen, scene/anchor display | Real Tk smoke and widget test; screenshots visually inspected after font setup | NOT_RUN |
| Scene text edit, stable identities, scene/anchor reorder, no silent asset deletion | Unit/roundtrip tests and widget save/reopen | NOT_RUN |
| WAV and MP3, manual subtitle validation, shortened-audio rejection, scene/movie render | Real FFmpeg-backed integration / RC02 tests | NOT_RUN |
| Cancel/resume, audio cache reuse, failed/incomplete export history | Original retained integration oracles PASS; not an OS player test | NOT_RUN |
| Different clip lengths / 15 and 60 FPS / different resolutions | Generated short and long MP4s normalized to 24 FPS; decoded | NOT_RUN |
| Missing files, tampered imports, Cyrillic names, unsupported paths | File/hash/error oracles PASS | NOT_RUN |
| Coverage gaps/overlap and explicit missing-media fallback | Export refusal for gaps; explicit placeholder succeeds | NOT_RUN |
| Native text animation and pan/zoom original diagrams | Real local renders PASS | NOT_RUN |
| Quota UNKNOWN/exhausted/expired/non-daily reset, absent provider/account, declined login | Planner/manual-state oracles; no browser login attempted | NOT_RUN |
| LLM manual, compatible protocol, unavailable/malformed provider | Real local HTTP **mock**, not model inference; unverified-draft and explicit apply oracles PASS | NOT_RUN |
| No accounts or Edge; manual/offline demonstrations | Real local builds using included assets/audio; network isolation qualification below | NOT_RUN |
| Credential storage, Google login, account authentication, paid/free credit consumption | NOT_RUN; manual media workflow only | NOT_RUN |
| Human listening, real desktop playback, scientific/editorial acceptance | NOT_RUN; technical decode and sample frame inspection only | NOT_RUN |

## Long-form demonstrations

| Locale | Measured source MP3 | Actual MP4 | Scenes / anchors | FFprobe / full decode exit | MP4 SHA-256 |
|---|---:|---:|---:|---|---|
| RU | 244.224 s | 244.291667 s (4:04) | 8 / 40 | 0 / 0 | `d9c0e6cc24b1d5f6c72d961a4e44aac5f534e3c1870a8d2ea26dedf204672bda` |
| UK | 219.624 s | 219.666667 s (3:39) | 8 / 36 | 0 / 0 | `7283ee3a99aacb872c40de3423027fdf7b380187492c1e09771dd50caa845c78` |

Both are an original manual editorial lesson about checking a story before turning it into video, not a scientific fact certificate. No paid services, real provider accounts, third-party media or Edge TTS were used. Scene boundaries are word-weighted estimates from imported whole narration; slight MP4 extension is encoder/frame quantization. A full decode establishes technical readability, not meaningful narration alignment or pronunciation. Independent human review remains open.

Portable inputs are under ../demos/media_hub/. FFprobe, captions, timing, execution evidence, hashes and decode summary are in evidence/. Review MP4s themselves are separate workspace artifacts linked in the final handoff, not published binary releases. Rebuild with:

```bash
python -m experimental_mvp.pipeline --project experimental_mvp/demos/media_hub/ru.json --workspace <local-output> --approve
python -m experimental_mvp.pipeline --project experimental_mvp/demos/media_hub/uk.json --workspace <local-output> --approve
ffprobe -v error -show_streams -show_format -of json <final.mp4>
ffmpeg -v error -xerror -i <final.mp4> -f null -
```

`--approve` is explicit consent to a local experimental render only. No production permissions or qualified Production Gate evidence is created.

## Offline fault-injection qualification

The complete RU demo was additionally built with strace 6.13 following Python and FFmpeg children, injecting `ENETDOWN` for `socket` and `ENETUNREACH` for `connect` syscalls. Build exit **0**; trace observed **zero socket and connect calls**; output SHA-256 matches the RU video above. This is an actual process-tree network-denial test, not merely a UI “offline” label. `offline-results.json`, raw trace and render log are included. A network namespace attempt (`unshare -n true`) returned **1**, “Operation not permitted”; no namespace or physical-network-disconnection claim is made. No escalation was needed for fault injection.
