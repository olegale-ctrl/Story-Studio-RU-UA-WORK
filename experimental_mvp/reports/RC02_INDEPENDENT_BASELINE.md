# RC-02 independent baseline — 2026-11-18

**Scope:** independent Linux reproduction in this task. **Windows 10/11: NOT_RUN**, no Windows machine was available. This is not Windows acceptance.

- Exact detached baseline: `1f27a9bb024b4e2ad18121843f14fe57d0522f17`.
- Tree: `2fd1e0f9f121016827f726606b821b510f6806e3`.
- Parent: `0dc314311b1f6ae2d0a0ed51aaabe3406badcbec`.
- Separate experimental worktree/branch created from that commit; main never checked out or modified.
- Python 3.12.14, Linux x86_64, FFmpeg/ffprobe 7.1.5-0+deb13u1, Tk 9.0.4. No edge-tts installed.

| Check | Linux actual result | Exit | Windows |
|---|---|---:|---|
| Original `python -m unittest experimental_mvp.test_pipeline -v` | 9 tests, 0 skips, PASS (3.593 s) | 0 | NOT_RUN |
| RU/UK JSON roundtrip; stable scenes; manual subtitle edit/reorder | Original unit oracles PASS; not a human GUI exercise | 0 | NOT_RUN |
| Imported WAV, interrupted build/resume, audio cache reuse | Original FFmpeg-backed tests PASS | 0 | NOT_RUN |
| Missing edge adapter CLI / help | Isolated package subprocess oracle PASS; missing synthesis gives actionable MP3/WAV error | 0 test harness | NOT_RUN |
| Exact original RC-02 `--check` with Linux Xvfb | Tk, 1080p H.264/AAC/mov_text, burned-caption scene preview PASS; no online request | 0 | NOT_RUN |
| New implementation `--check` before virtual display | Media checks PASS, Tk FAIL (no DISPLAY) | 1 | NOT_RUN |
| Windows GUI editing/save/reopen, MP3/WAV selection, manual captions, player, stop/resume, Cyrillic paths | NOT_RUN on Windows; see Linux integrated tests in TEST_RESULTS | N/A | NOT_RUN |

Linux-specific finding: `os.startfile` was unconditional in the baseline GUI. Experimental UI now uses `os.startfile` on Windows and an argument-array `xdg-open`/`open` on Linux/macOS. External desktop-player launch is not verified here. GUI font selection now prefers an available Cyrillic-capable family. The bare test X server initially lacked Cyrillic fonts; adding test-only fonts and visually checking the interface resolved that environment defect.

Original normative Story Intelligence, Production Gate proposals, CI and production storage are outside this branch's modifications. Windows acceptance remains a required independent follow-up; Linux PASS does not close it.
