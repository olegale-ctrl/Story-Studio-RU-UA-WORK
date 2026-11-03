# Story Studio RU/UA — WORK

Private development repository for a Russian/Ukrainian adaptation of [konlu/story-studio](https://github.com/konlu/story-studio).

## Status

Last locally tested milestone: Sprint 25, 2026-11-03. Offline Silero successfully produces a valid WAV, but Voice Studio may falsely display `Preview failed` due to corrupted Cyrillic characters in the path printed by the subprocess. Sprint 25.1 is pending.

**This is a bootstrap repository, not yet a complete deployable snapshot.** The existing local working tree must be imported before full tests or deployment.

## Repository policy

Track source code, tests, setup scripts, examples that do not contain generated media, and project documentation. Exclude Python environments, downloaded TTS models, audio/video output, secrets, logs and caches. Preserve third-party attribution and review dependency licenses before redistribution.

Primary platform: Windows 10/11; preserve portability to macOS/Linux. CPU-only operation must remain possible.
