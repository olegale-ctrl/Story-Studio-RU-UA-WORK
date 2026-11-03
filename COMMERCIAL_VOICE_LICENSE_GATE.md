# MANDATORY RELEASE GATE — voice licenses

**Status: BLOCKER for any commercial release, paid service, monetized distribution, or bundled models.**

The user approved all voices for research and noncommercial development, but this does **not** grant commercial rights.

Before commercialization, re-audit *each exact model weight/version*, upstream code license, redistribution terms, attribution, derivative/voice-output rights, commercial service restrictions, data/privacy terms, regional availability and any provider ToS. Keep evidence and review date in `project-log/` and require explicit approval.

- Silero `v5_cis_base` and `v5_cis_base_nostress`: upstream README identifies MIT license (`LICENSE_CIS`). Reverify weight and redistribution scope.
- Silero `v5_6_ru`, `v4_ua` and other non-MIT models: upstream indicates CC BY-NC; **do not bundle or enable commercially without separate authorization**.
- Edge TTS: verify provider service terms, commercial use and voice-output rights separately; code package license is not a service license.
- Model `random` is not a stable individual voice; do not count it as a distinct guaranteed speaker.

Default distribution: do not bundle downloaded weights. Model downloads are opt-in. No automatic substitution of a different gender or speaker without disclosure/consent.

Source: https://github.com/snakers4/silero-models (README, LICENSE, LICENSE_CIS, models.yml), reviewed 2026-11-02.
