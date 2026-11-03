# Sprint 23.2

Fixed Windows Cyrillic-path failure by using a persistent ASCII-only model location. No temporary directory or cleanup. UI selects C:\StoryStudioModels\v5_cis_base_nostress.pt by default on Windows; STORY_SILERO_MODEL overrides. Provider retains SHA256 verification and explicit trust requirement. Edge TTS unaffected.

Local unit tests only; user must validate actual PyTorch load and WAV playback on Windows.
