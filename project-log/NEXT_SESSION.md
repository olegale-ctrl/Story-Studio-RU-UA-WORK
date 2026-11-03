# Next session — Sprint 26 first-video pipeline (2026-11-03)

Windows Sprint 25.1 Silero Ukrainian preview verified by user: Preview ready, WAV 2.2 s, synthesis 11.2 s, RTF 5.17, playback reported working.

Current work: `scripts/first_video.py` builds an offline narrated MP4 from a RU/UA JSON scene plan with local Silero or existing WAVs, optional local images, generated gradient fallbacks, scene subtitles and existing FFmpeg renderer. See `docs/SPRINT26_FIRST_VIDEO_WINDOWS.md`.

**Next user validation gate:** On Windows run `scripts/first_video.py --plan examples/first_video_plan_uk.json --silero-model C:\StoryStudioModels\v5_cis_base_nostress.pt --voice ukr_igor --output-dir output/first-video-uk`, then inspect `output/first-video-uk/first-video.mp4` for spoken audio, subtitles, picture and timing. Output directory must not exist already.

No full Chinese original code was executed or included in the pipeline; upstream rights and provider terms remain gated. CI and local synthetic tests must be checked before claiming verified status.

# Next session — after Sprint 25.1 (2026-11-03)

Repository: https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK

- Complete upstream Chinese original is pinned as a Git submodule at `upstream/konlu-full`; engineering files also preserved in `upstream/konlu-story-studio/`. Do not overwrite the RU/UA implementation from upstream.
- Our RU/UA Sprint 25 code baseline has been imported to GitHub. Sprint 25.1 fixes Voice Studio's Unicode console-path preview failure by determining the expected output path before synthesis; adds UTF-8 subprocess environment and synthesis metrics in the UI.
- Next on Windows: install `Sprint_25_1.zip` OVER the current local project, keeping `.venv`, models and other local assets; run `python -m unittest discover -s tests -v`; start Voice Studio via `scripts/run_voice_studio.ps1`; generate Ukrainian Silero preview and confirm `Preview ready`, audio playback and time metrics. Test Edge TTS too if internet access permits.
- Do not upload, distribute, or commercialize Chinese corpora/media and current upstream CC BY-NC-SA 4.0 source without legal review. Historical local MIT license provenance differs from current upstream license.
- Tests run on Linux Python 3.13: 106 passed, 0 failed. Windows GUI + actual Silero model were NOT tested in the CI/container environment. Save Windows test outcome in next worklog entry.


# Next session — after Sprint 12
1. Windows: unpack Sprint12.zip into project root with replacement; keep FFmpeg user-managed.
2. Render demo with `--burn-subtitles --crf 22` to a NEW output name; verify thin outline and no shadow.
3. Run `python -m unittest discover -s tests -v`; report actual result.
4. Test real two-clip audio timeline and then move toward meaningful voiced demo.
5. License gate: GPL-enabled Gyan FFmpeg build is not to be redistributed inside project ZIP; Chinese corpora/assets remain blocked.

## Sprint 14 next actions
1. Install Sprint14 overlay and check Windows SAPI voices (uk/ru).
2. Generate local narrated demo and run render command from docs/SPRINT14_WINDOWS.md.
3. Confirm speech is intelligible, subtitles synchronized, and final video plays.
4. If language voice unavailable, investigate local TTS alternatives with model/license review before integrating.

## Sprint 15 next actions
1. Unpack Sprint15.zip after Sprint14. Run `scripts/run_narrated_demo.ps1 -ListVoices` and report voice names/languages.
2. If uk/ru voice exists, run `-Locale uk` or `-Locale ru` and confirm speech, subtitle sync and MP4 playback.
3. If none exists, compare license-cleared offline TTS engines before integrating any external models.

## Sprint 16 next
- User installs Sprint16.zip and runs `powershell -NoProfile -ExecutionPolicy Bypass -File .\scripts\run_edge_demo.ps1 -Locale uk -Gender female`.
- Confirm MP4 speech, captions and synchronization. Then test RU male and UK male.
- Review provider terms; Edge TTS is an experimental consumer endpoint, not approved for commercial distribution.
- Next sprint: provider abstraction, caching, voice previews, GUI and local TTS options.


Sprint 16 hotfix: test ru female and ru male; failures should now give clean message and no empty cached MP3. Confirm full render on Windows.

## Sprint 17 follow-up
Проверить мужской ru-RU-DmitryNeural после установки патча. Далее: каталог голосов, preview, надёжная синхронизация.
