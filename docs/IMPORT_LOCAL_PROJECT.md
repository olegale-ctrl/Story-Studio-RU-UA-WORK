# Import local working project

The existing local folder `C:\Users\Олег\Downloads\Story-Studio-RU-UA` is the current source of truth.

Do not overwrite it by cloning this repository into the same location. Back up the folder first. Exclude `.venv`, Silero model weights, secrets, generated audio/video, caches and downloaded tools.

Recommended approach: copy only vetted source directories and project documents into a **fresh clone** of this repository, inspect `git status`, then commit and push. Never use `git add -f` for ignored files.

Once the source tree is imported, run the project's existing unit tests and Windows voice preview checks before labeling a release.
