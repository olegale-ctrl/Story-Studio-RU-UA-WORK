# Sprint 23 — Voice Studio Silero integration

- Voice Studio now selects Edge or local Silero, language and voices.
- Local model load requires explicit trust checkbox.
- New subprocess CLI bridges UI to existing `SileroLocalProvider`.
- Edge speed/pitch and strict fallback behavior preserved.
- Silero speed/pitch unavailable (disabled).
- Audio preview saved under `examples/voice_previews/`.
- Model files not included. Commercial licensing/provenance unresolved.
- Windows GUI and real synthesis need user smoke test.
