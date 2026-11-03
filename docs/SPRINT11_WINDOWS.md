# Sprint 11 — Windows instructions

The renderer now discovers a locally installed `tools/ffmpeg/bin/ffmpeg.exe` automatically; PATH is not required. FFmpeg is NOT bundled in this update.

From the project root, run:

```powershell
python -m unittest discover -s tests -v
python -m core.cli render-mp4 .\examples\demo_project.json --media-root .\examples\demo_media --output .\demo-subtitled.mp4 --burn-subtitles --crf 22
```

Open `demo-subtitled.mp4`. Three Ukrainian captions should be visible on the three colored frames. The original sound remains a synthetic tone. Separate SRT is also exported.

If FFmpeg reports missing `subtitles` filter, use a build with libass. If output exists, choose a different filename; this tool never overwrites existing MP4 files.

Limits: one subtitle track for burn-in; sequential stills, one audio clip, fixed project resolution/FPS. Multiple audio segments and narrative demo are NOT implemented yet. Third-party FFmpeg binary remains user-managed; the GPL-enabled gyan.dev build must not be redistributed with the app without compliance review.
