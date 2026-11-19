# Topic-to-Film integration readiness

**2026-11-19 · READ_ONLY_AUDIT / DOCS_ONLY · no implementation or production authorization.**

SP/1.1 is used only as diagnostic requirements at16d28ec,not an API or grant. All routes currently BLOCKED_CONTRACT for execution integration.

|Route|Required stages|Dispatcher support|Problems|
|---|---|---|---|
|A|Topic→Script→Plan→Assets→Render→Gates|No GenerationJob API/type registry found|Draft authoring not implemented by video jobs;facts/editorial policy and every executor/storage/authority bridge absent|
|B|Script→Plan→Assets→Render→Gates|None verified|No approved script-to-plan/voice/image/render handlers or composite receipt|
|C|Plan→Assets→Render→Gates|None verified|Existing plan validation is a local diagnostic;no submitted asset/render jobs|
|D|Plan+prepared assets→Render→Gates|None verified|First Video exists directly but forbidden bypass;no authorized render handler/final validator/storage receipt|

1. **General DAG:** B.1 proposes specialized T2V/I2V video-generation jobs for an anchor/clip→Library→saved project. It does not specify or implement a universal DAG. LAB storage protocol is not either model. No generic DAG engine becomes mandatory from the four routes.
2. **Specialized bridge:** a qualified bridge may cover a bounded clip/asset operation later;it is not proven sufficient for complete A/B/C/D film assembly. Start requirements reconciliation from the smallest needed D operation;decide exact handler/receipt scope before implementation. Whole-film render.mp4 is not automatically the same as T2V/I2V clip generation.
3. **Actual registered types:** no MVP registry found. script.draft,plan.from_script,plan.validate,assets.voice,assets.images,render.mp4,gates.technical remain proposed SP labels. LAB six storage operations are not aliases.
4. **Authority:** CLI flags express intent only;rights/actor/evidence/scope/expiry/revocation/currentness remain separate verified sources. Draft or Synthetic D1 permission does not authorize a different render. Release remains false.
5. **Identity/receipts:** need immutable project/purpose/batch/request identity and raw input hashes,versioned policy/approval,exact output validation/import/save receipts. SP digest,S1 MAC,PG binding and proposed08Bdigest cannot be interchanged.
6. **Completion/currentness:** authoritative job revision+matching result+saved JSON receipt and rechecked rights are needed. Later user edits mean divergence,not automatic restoration. Neither cached LAB result nor Library link confirms current saved film.
7. **--wait:** requires an approved authoritative observation API by accepted job ID/state revision,deadline and timeout semantics. Current SP correctly blocks immediately;no private polling/retry/mirror is introduced.
8. **Repeat request:** must obtain atomic accepted/reused/conflict receipt under approved idempotency scope. Repeating local intent hash or LAB lookup is not durable submission dedup. Unknown ACK/publication outcome cannot justify resubmit/regenerate.

No SP-OD01–09 expansion. Current task-reported SP01b ACCEPTED_WITH_LIMITATIONS is scoped to diagnostics;no new freeze approval/JobStore payload inferred. Production/rights/editorial/native storage qualification and final release verifier remain independent blockers.
