# ADR-0002 — Independent locales and source content
Status: ACCEPTED (2026-10-30)

- Fork is a substantial rework for RU/UA and a different provider/editor stack, not a translation.
- Chinese Writing-DNA, scenario corpora, references: **REPLACE** with independently authored materials or **BLOCKED** from releases; no blanket upstream-MIT assumption.
- `locales/ru` and `locales/uk` contain independent UI strings and prompt templates. UI locale, script locale, speech locale, subtitle locale are separate settings in future config.
- Local AI preferred; provider review matrix must cover ToS, price, region, output rights, data, model weights and voice rights.
- CapCut International is feasibility-only and not in v1 acceptance criteria.
- Dependency audit covers direct, transitive, runtime-downloaded binaries/models.
