# Sprint 12 — Windows verification
Unpack Sprint12.zip in existing project root, replacing files. No binary installation needed.

```powershell
python -m unittest discover -s tests -v
python -m core.cli render-mp4 .\examples\demo_project.json --media-root .\examples\demo_media --output .\demo-s12.mp4 --burn-subtitles --crf 22
```

Open `demo-s12.mp4` and check that subtitles have no offset shadow. The filename overlay from the player is not part of the MP4.

Note: the bundled demo uses a single synthetic audio tone; multiple audio clips are covered by tests and require a suitable timeline JSON to try manually.
