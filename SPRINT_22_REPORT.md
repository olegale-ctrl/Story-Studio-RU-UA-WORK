# Sprint 22 — Local Silero adapter

## Confirmed from user's Windows runs
- `silero_preview.py` compiled and catalog contained `ru_dmitriy`.
- Russian `ru_dmitriy` and Ukrainian `ukr_igor`, `ukr_roman` generated playable audio.
- User reports the Russian voice sounds somewhat unnatural.

## Delivered
- `integrations/silero_local.py`: isolated provider API, local-only model loading,
  explicit trust gate, pinned SHA256, 24 kHz mono PCM WAV, atomic output.
- `tests/test_silero_local.py`: small contract tests without model dependency.

## Remaining
- Inspect latest project `Voice Studio` implementation and provider interfaces.
- Wire this adapter to actual provider selection and voice dropdown.
- Run full tests and end-to-end Windows integration.
- Confirm model weights' license, provenance, and commercial usage rights.

## Licensing status
- Third-party model file is not included. Commercial redistribution NOT approved.
