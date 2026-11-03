# Sprint 25 — Hardware diagnostics in Voice Studio

- Adds hardware information and manual refresh in the Voice Studio UI.
- Detects hardware in a background thread so UI remains responsive.
- Keeps CPU as the safe default, never infers GPU acceleration from GPU name.
- Measures actual synthesis wall time, WAV duration, and real-time factor.
- MP3 duration is deliberately not guessed.
- Existing Edge/Silero commands and trust checks remain unchanged.
- No network transfer of hardware details.

## Verification
4 Sprint 25 tests passed; 4 Sprint 24 tests passed; 4 Sprint 23.2 tests passed in build environment. Actual Windows GUI requires user verification.

## Limitations
This is diagnostic display and benchmarking, not automatic provider switching. Real automatic selection will require measured per-engine performance and user preferences; never disable a working engine solely from CPU/GPU model.
