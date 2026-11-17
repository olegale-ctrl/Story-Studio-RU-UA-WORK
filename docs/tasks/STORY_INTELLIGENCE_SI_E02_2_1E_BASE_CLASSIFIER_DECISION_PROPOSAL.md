# SI-E02.2.1e — Q1–Q3 closed base-classifier decision proposal

Дата: 2026-11-12 (Europe/Kyiv).
**PROPOSAL / Q1–Q3 NOT APPROVED. DOCS ONLY / NO IMPLEMENTATION.**
Base: `1c4724da06c087374ac5a7098554760d5752f9fd`.
[RC approval](STORY_INTELLIGENCE_SI_E02_2_1E_RC_OWNER_APPROVAL_2026_11_12.md) не утверждает
эти matrices. Ниже — конкретная recommended policy, alternatives/limitations для
owner decision. [Original](STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md)/
[R1 §3.2](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md) precedence и closed Code
не меняются; новые application predicates/mappings требуют отдельного approval.

## 1. Shared boundary and diagnostics

Все SI shapes/refs/hash/DAG/provenance/currentness и local bindings проверяются до
eligibility. Broken/missing refs → INVALID, changed valid context → STALE/INPUT_STALE,
INVALID важнее STALE. Ни один graph error не переименовывать в research.

Main semantic domain projection M повторяет accepted typed roles/G01/G02/F1-D1 и
RC source traversal; это не full audit Closure, не весь supplied bundle и не все
observed inputs автоматически. Explicit observed input set — выбранный caller view,
не доверенный immutable реестр. Main root roles и exact frozen context задаются явно.
Premise proof-only claims не main claims только из-за проверки proof; если есть main
semantic path к тому же exact claim, его review уже нельзя скрыть label «proof-only».

Generated reason_codes — unique ASCII lexical union; diagnostics — existing
(code,field_path,input_ref,message), упорядочены по condition class
BLOCKED→NEEDS_INPUT→NEEDS_RESEARCH→REVIEW_DUPLICATE, затем code/path/C(ref)/message.
All applicable reasons сохраняются, не только winning state. Валидационные отказы не
создают accepted eligibility. Никаких новых condition/error wire enums.

Diagnostic labels BQ1/BQ2/BQ3 ниже documentary, не codes. Records index i — actual
supplied ordered records[i]; evaluator не сортирует/не мутирует records. Text messages
фиксированы, не echo source.reason/title/private label. Technical refs/codes не продукт;
SI-PRODUCT-01 требует будущих понятных editor explanations без raw SIRef/hash/codes.
Projection/UI не реализуется. Оригинальные RC D01–D16 не изменяются.

## 2. Q1-A — Main claim/check/evidence applicability

### Declared current scope

1. C = all exact ClaimItem refs в M: explicit main Claim roots, current Angle.claim_refs,
   applicable producer/main Check/Evidence/Risk typed dependencies. H.previous, historical
   Run snapshots, unrelated observed claims и proof-only freshness claims не добавлять.
2. Для q∈C применимы main semantic ClaimChecks q плюс все explicitly observed active
   ClaimChecks, чьё claim_ref **равно exact q**. Это proposed reverse lookup по typed
   claim_ref, не поиск Text и не latest. Неприменимы historical-only check revisions.
3. Если declared main check является old revision, а view выбирает другую exact revision
   той же check identity, результат STALE/INPUT_STALE, а не выбор победителя по времени.
   Для проверки applicability main checks должны быть явно выбраны active exact refs;
   отсутствие такого выбора при intact graph предлагается считать STALE/INPUT_STALE.
   Это evaluator admission policy, **не изменение** root-membership semantics existing
   check_si_currentness. Historical-only edit-base не становится main check.
4. Applicable Evidence = exact evidence refs применимых checks плюс explicitly main
   semantic/observed active EvidenceItems с claim_ref=q. Unrelated other-claim evidence
   не применяется. Missing any declared ref INVALID. Cross-claim evidence в Check →
   PROVENANCE_MISMATCH; wrong typed ref → REF_TYPE_MISMATCH. Не исправлять evidence list.

Эта scope/completeness policy Q1-A ещё NOT APPROVED. Caller может скрыть независимый
check, переписав весь свой untrusted view; SI/1 не имеет protected complete-check registry.
Pure module гарантирует только consistency/coverage **явно объявленного** view, не
глобальное обнаружение удалённых/несообщённых отрицательных решений.

### Coherent positive recorded review

Check supported/qualified даёт positive recorded support только если KNOWN nonempty
evidence_refs, все exact claim/source relationships корректны, есть хотя бы один
relation=supports с KNOWN locator и Source.material_sha256 KNOWN; остальные declared
refs тоже valid. Qualified сохраняет non-null qualification; metadata invariants
existing validator обязательны. Locator/material snapshot Unknown означает insufficient
support, не guessed verification. Hash — record/material binding, не proof actual reading.

Ни count URL, ни reviewer_label, ни confidence, ни explanation не заменяют этого.
Одно positive check не отменяет отдельного applicable negative check/evidence.

### Complete state × kind × materiality matrix — Q1-B

B=BLOCKED/CENTRAL_CLAIM_UNSUPPORTED; R=NEEDS_RESEARCH/EVIDENCE_NEEDED;
A=no additional claim-review gap (не automatic approval).

| Applicable Check condition | factual CENTRAL | factual SUPPORTING | factual CONTEXT | interpretation CENTRAL | interpretation SUPPORTING/CONTEXT | fictional any materiality |
| --- | --- | --- | --- | --- | --- | --- |
| No applicable check | B | R | R | R | R | A |
| unreviewed | B | R | R | R | R | A |
| unverified | B | R | R | R | R | A |
| disputed | B | R | R | R | R | A |
| supported + coherent positive support | A | A | A | A | A | A |
| qualified + coherent support/nonnull qualification | A | A | A | A | A | A |
| supported/qualified but insufficient support/locator/material digest | B | R | R | R | R | A |
| removed but q still in C | B | R | R | R | R | A (no factual-evidence requirement) |

Missing/UNKNOWN evidence union, insufficient relation or locator не ноль/known empty;
они попадают в insufficient positive support row, не в A. Malformed unreviewed metadata
или supported+UNKNOWN evidence — local validation failure по existing code, не R.
Applicable explicit Evidence.relation=contradicts для factual CENTRAL даёт B даже при
другом supported Check; для других non-fictional claims — R. Для fictional материал
не превращается в факт; любое explicit Risk всё равно применимо. Fictional A не
означает scientific verification и не разрешает неправильно маркировать реальные факты.

Multiple checks: apply every applicable row, worst condition wins by R1, all diagnostics
survive. **Disputed central factual remains blocking even with supported elsewhere.**
Unreviewed/removed/insufficient independent checks тоже не исчезают благодаря одному A.
Это proposed conservative aggregation, не owner-approved equivalence всех review states.

Qualified A относится к recorded claim review только. Проверка сохранности qualification
в future hook/Brief остаётся обязательной отдельно; evaluator не может доказать это
по arbitrary Angle.thesis и не должен объявлять будущий текст approved. Если фактическая
формулировка меняется, требуется explicit new claim/check/Angle revision, не silent fix.
Removed q исчезает из applicability только после explicit current semantic edit всех
его main roles; old claim/check bytes остаются в audit. Main Risk q может сохранить q
применимым независимо от удаления одного Angle ref.

### Human resolution without provenance deletion — Q1-C

Рекомендуется existing REVISE_INPUT: тот же ClaimCheck id, revision+1, previous exact,
HUMAN_EDIT/REVISION Run с base-first/full payload inputs, updated exact evidence/reason/
review metadata. View и main roots явно выбирают новый check; старый disputed revision
остаётся intact audit. Если current contradictory evidence также объявлен, требуется
явная человеческая evidence/claim revision и rebinding всех затронутых roles, а не
одна фраза «решено» в reason. Другой independent disputed check продолжает блокировать.

**SI/1 limitation:** нет `supersedes_check_ref`/resolution registry. Check B другой
identity не может машинно отменить current disputed A по reason/label/date. Нужно
ревизовать A либо отдельно утверждать truthful resolution contract. Не добавлять поле,
не кодировать cross-identity supersession hidden JSON и не удалять A из истории.
Реальное авторство/правомочия reviewer этим не доказываются.

### Q1 diagnostic mapping

| Condition | code / class | path / input_ref | Fixed message |
| --- | --- | --- | --- |
| q central factual lacks applicable review | CENTRAL_CLAIM_UNSUPPORTED / BLOCKED | $.records[i].payload.materiality / q | A central factual claim lacks applicable support. |
| Negative/insufficient applicable Check c for central q | CENTRAL_CLAIM_UNSUPPORTED / BLOCKED | $.records[i].payload.state / c | A central factual claim has unresolved review. |
| Noncentral/interpretation gap in Check c | EVIDENCE_NEEDED / NEEDS_RESEARCH | $.records[i].payload.state / c | Claim review requires further research. |
| Noncentral/interpretation no Check | EVIDENCE_NEEDED / NEEDS_RESEARCH | $.records[i].payload.evidence_expectation / q | Claim support requires research. |
| Applicable contradicts Evidence e | CENTRAL_CLAIM_UNSUPPORTED if factual CENTRAL, else EVIDENCE_NEEDED; corresponding class | $.records[i].payload.relation / e | Recorded evidence remains in conflict. |

No check diagnostic придуманный с fake SIRef; q используется при отсутствии Check.
При одном Check с несколькими недостатками одна state diagnostic, exact graph errors
всегда раньше. Все эти mappings/aggregation NOT APPROVED.

## 3. Q2 — Complete explicit Risk/visual/capability proposal

### Q2-A Applicable records and state predicate

Applicable risks = Risk refs в M плюс explicitly active Risk, имеющие basis_ref в M;
второе правило — proposed typed applicability extension. Unrelated/audit-only Risk
не блокирует оценку сам по себе. Applicable visuals = main explicit/current Visual
refs или relevant typed Risk/Brief paths в M; future Brief не prerequisite EVALUATE.
Все declared refs проверяются даже при nonblocking Risk. No inference из description.

| Risk fields (all six categories, all LOW/MEDIUM/HIGH/CRITICAL) | Proposed effect |
| --- | --- |
| blocking=false; OPEN/UNRESOLVED/MITIGATED | No automatic eligibility blocker; preserve recorded risk for review, not clearance |
| blocking=true; OPEN or UNRESOLVED | BLOCKED regardless severity/score |
| blocking=true; MITIGATED with coherent recorded resolution review below | No additional Risk blocker, not proof actual mitigation |
| blocking=true; MITIGATED with insufficient review/basis | Still BLOCKED (unestablished mitigation), not auto clearance |
| Missing/hash-corrupt basis or resolution ref | INVALID before any above condition |

Severity alone не добавляет/снимает blocker. Q2-A includes explicit blocking MARKET и
REPUTATIONAL: это choice категории с человеческим blocking flag, не автоматический
market predictor или порог по severity. Full category applicability требует approval.

Recommended recorded resolution predicate Q2-M: exact current resolution_basis_refs
включают supported/qualified ClaimCheck с coherent positive evidence по Q1, связывая
его с этим Risk через declared resolution_basis_refs; все referenced facts/basis текущие,
no unresolved applicable negative check на тот же exact claim. Сам Risk явно revised
в MITIGATED человеком. Free-text mitigation/owner_role и просто nonempty refs не proof.
Это **recorded human assertion/coherence**, не установленная машиной truth/legality.
Нет отдельного RiskReview type; если нужен независимый authenticated/staging verdict,
его existing SI/1 не даёт. Q2-M — proposed limited advisory acceptance, не approval.

### Q2-C Exact category mappings for still-blocking Risk

Recommended alternative **A**: use existing EVIDENCE_NEEDED как общий код необходимости
human risk review, class BLOCKED; code не определяет класс. Specific established claim/
visual conditions дают дополнительные более точные diagnostics, а не стираются generic.

| category | Generic code / exact path | input_ref / fixed message |
| --- | --- | --- |
| SCIENTIFIC | EVIDENCE_NEEDED / $.records[i].payload.blocking | RiskRef / An explicit scientific risk remains blocking. |
| LEGAL | EVIDENCE_NEEDED / $.records[i].payload.blocking | RiskRef / An explicit legal risk remains blocking. |
| ETHICAL | EVIDENCE_NEEDED / $.records[i].payload.blocking | RiskRef / An explicit ethical risk remains blocking. |
| REPUTATIONAL | EVIDENCE_NEEDED / $.records[i].payload.blocking | RiskRef / An explicit reputational risk remains blocking. |
| PRODUCTION | EVIDENCE_NEEDED / $.records[i].payload.blocking | RiskRef / An explicit production risk remains blocking. |
| MARKET | EVIDENCE_NEEDED / $.records[i].payload.blocking | RiskRef / An explicit market risk remains blocking. |

Если MITIGATED остаётся blocking по недостаточной resolution review, тот же category
code/message, path **$.records[i].payload.resolution_basis_refs**, ref=RiskRef.

Это **не однозначный existing normative mapping** для generic ETHICAL/REPUTATIONAL/
MARKET и других arbitrary Risks. Owner должен выбрать A (полная recommended table)
либо alternative **B**: вернуть точную category/condition-specific таблицу существующих
codes до implementation. B не является runtime fallback, разрешением пропустить Risk
или выдавать TYPE для valid data. Подбор RIGHTS_BLOCKED для всех LEGAL или
CAPABILITY_BLOCKED для всех PRODUCTION может исказить смысл; без явного решения так
не делать. Новые dedicated codes запрещены в этом этапе. Q2-C OPEN до owner decision. Если Q2 table A принята, C14/C44 дополнительно
сверяются с новым applicable Risk diagnostic set: RC-related ожидания неизменны,
все новые base diagnostics, включая BX, ещё условны до Q2 approval.

### Q2-V Essential/optional materials and usable fallback

| Current Visual / role | Proposed condition | Result / diagnostic |
| --- | --- | --- |
| REQUIRED; rights UNKNOWN/NEEDS_REVIEW | Unresolved essential rights, fallback только Text/plan или отсутствует | BLOCKED/RIGHTS_BLOCKED, $.records[i].payload.rights_state, VisualRef, "Essential material rights are unresolved." |
| REQUIRED; DOCUMENTED + KNOWN licence_basis + matching known material digest/current Source refs, coherent human resolution review | Recorded rights consideration complete, no extra visual-rights gap | No grant/production permission; explicit other Risk still applies |
| REQUIRED; DOCUMENTED but material identity/recorded review insufficient | Rights not established for exact intended material/use | BLOCKED/RIGHTS_BLOCKED, same path/ref/message |
| DOCUMENTED + UNKNOWN licence_basis | Existing local invariant broken | INVALID/RIGHTS_BLOCKED by validator, not a valid unresolved Visual |
| OPTIONAL with unresolved rights | Not an essential input requirement | No automatic essential-rights blocker; cannot use material in production without later rights review/exclusion |
| LOCAL role | Not automatically lawful/available | No automatic clearance; explicit blocking Risk applies; no fabricated essentialness from local acquisition label |

Recommended fallback path for first bounded version: **explicit new current Visual
revision** describes chosen lawful replacement, source_refs/material_sha256/licence_basis/
intended_use/rights_state updated coherently and recorded review linked via Risk resolution.
Old unresolved Visual/Risk remain audit. Merely KNOWN fallback description cannot clear
current unresolved REQUIRED material. This avoids treating a future plan as staged bytes.
No machine inference that local-create means licensed.

Exact representation limit: SI SourceItem/hash/ClaimCheck do not prove actual staged
bytes, access, licence validity/expiry or real CPU execution. Proposed coherent human
review can be used only as advisory recorded basis, not filesystem/authority proof.
If owner requires actual staged-asset/rights verification, that is not expressible as
this pure guarantee; no new staged flag/Asset Registry/adapter is invented here.

### Q2-K Capability versus preference

Nonblocking PRODUCTION/effort HIGH/resource preference is not capability failure.
Explicit blocking PRODUCTION Risk still BLOCKED under Q2-C, even if generic code is
EVIDENCE_NEEDED. There is no structured `capability_gap` discriminator in Risk and
Channel.capability_notes is Text; do not infer CAPABILITY_BLOCKED from keywords.
Dedicated CAPABILITY_BLOCKED is reserved for an independently established applicable
capability condition under an exact approved role mapping. This proposal recommends
no automatic subtype inference; if owner needs that subtype from generic PRODUCTION,
choose exact category/condition mapping in alternative B or a separate truthful input
contract. The blocker is not dropped while its specific subtype remains unproved.

## 4. Q3 — Field-level framing/audience/channel decision matrix

All missing required records/ref targets → REF_MISSING/INVALID; absent schema fields
→ MISSING_FIELD/INVALID; wrong shape/value → existing TYPE/etc. Never turn empty Text,
null вместо Known или missing SIRef into NEEDS_INPUT. Genuine changed selected context
→ STALE/INPUT_STALE. Rows below concern otherwise valid/current records only.

Recommended Q3-A: knowledge_level/motivation and capability_notes are explicit human
specifications needed by first bounded evaluation. Their honest UNKNOWN is NEEDS_INPUT,
not guessed demographics. Q3-B: other optional metadata/hypotheses below remain visible
as UNKNOWN, not automatic readiness blocker. These choices still require approval.

| Record.field (every payload field covered) | Present valid-value policy |
| --- | --- |
| StoryIdea.intake_ref | Exact required Intake, no implicit local path fetch |
| StoryIdea.title, summary, viewer_question | Required nonempty Text; no semantic completeness inferred from words/TBD templates; missing/empty is shape failure, not guessed framing |
| StoryIdea.source_refs | UNKNOWN→research only when main C contains factual/interpretation claims; KNOWN[] has no auto gap for empty/fictional C. Q1 support rules still apply; no fabricated sources |
| StoryIdea.candidate_binding | null allowed; relevant ERef without snapshot INVALID/REF_MISSING |
| Angle.idea_ref, audience_ref | Exact role equality with binding; genuine old scope STALE, incompatible current bindings validation failure |
| Angle.question, thesis, distinction | Nonempty authored framing; not factual proof/duplicate resolution. No keyword readiness rule |
| Angle.claim_refs | Exact main claim roots; [] allowed, no hidden minimum count; Q1 governs declared claims |
| Angle.limitations | Empty/nonempty permitted; not a machine resolution/approval |
| AudienceHypothesis.locale | Exact ru/uk context match, else LOCALE_MISMATCH |
| AudienceHypothesis.knowledge_level | UNKNOWN→NEEDS_INPUT; KNOWN Text supplies editorial level, not measured audience fact |
| AudienceHypothesis.motivation | UNKNOWN→NEEDS_INPUT; KNOWN Text supplies editorial question/motivation |
| AudienceHypothesis.region, age_range, interests | UNKNOWN permissible hypothesis; no default region/age/interests; KNOWN[] interests not silent demographic inference |
| AudienceHypothesis.basis_refs | Exact refs if present; [] permissible for explicit manual hypothesis, not evidence of statistics |
| AudienceHypothesis.assumptions | Authored list preserved; not inferred true from nonempty Text, no hidden minimum length |
| ChannelContext.channel_alias, purpose | Required nonempty Text, no name/keyword threshold |
| ChannelContext.audience_ref | Exact selected Audience binding; no latest |
| ChannelContext.constraints | Authored []/Text list allowed; not verified capability or permission |
| ChannelContext.portfolio | EVAL-P03 unchanged: UNKNOWN research; KNOWN[] no local pair gap; all KNOWN entries require exact findings |
| ChannelContext.analytics | UNKNOWN allowed as unmeasured editorial hypothesis, not invented statistics. Rating/confidence/evidence findings remain independent |
| ChannelContext.capability_notes | UNKNOWN→NEEDS_INPUT for missing human production-constraint specification; KNOWN Text not actual CPU measurement/clearance |
| Rubric.method_id, method_version, blocker_policy_version | Exact supported profile tuple must be pinned by owner; recommended Q3-R=(si-rubric,1,1), not inferred from arbitrary Text |
| Rubric.criteria | Approved nine keys/order/weights 15/10/10/20/15/10/10/5/5, min0/max5/HIGH_IS_BETTER; mismatch invalid evaluation, no renormalization |
| Rubric.missing_policy | ALL_REQUIRED; UNKNOWN rating remains UNKNOWN and research |
| ContextSnapshot.context_version | Existing 1 only, unsupported existing version fails validation |
| ContextSnapshot.active_input_refs | Explicit exact domain choices, one identity/revision per view; wrong graph INVALID, genuine changed binding STALE |
| ContextSnapshot.selection_head_refs | Explicit heads if any, no future Selection prerequisite EVALUATE; preserve used/unrelated head semantics |
| ContextSnapshot.editorial_snapshot_sha256 | UNKNOWN allowed for ERef-free; opaque hash alone never validates relevant ERef |

Q3-R is proposed support whitelist for the first pure profile, **not** change to SI/1
Rubric Text schema or operation version. Other valid record tuple could return invalid
evaluation/VERSION_UNSUPPORTED at actual profile field while remaining valid SI data.
The literal candidate comes from existing rubric fixture/default vocabulary; fixture
itself is not normative authority. Owner can choose another explicit approved profile
spelling before implementation. All nine criterion semantics/weights remain unchanged.

### Q3 exact diagnostics (PROPOSAL)

| Condition | Existing code / class | path / input_ref | Fixed message |
| --- | --- | --- | --- |
| Audience knowledge UNKNOWN | EVIDENCE_NEEDED / NEEDS_INPUT | $.records[i].payload.knowledge_level / AudienceRef | Audience knowledge level is unspecified. |
| Audience motivation UNKNOWN | EVIDENCE_NEEDED / NEEDS_INPUT | $.records[i].payload.motivation / AudienceRef | Audience motivation is unspecified. |
| Channel capability_notes UNKNOWN | EVIDENCE_NEEDED / NEEDS_INPUT | $.records[i].payload.capability_notes / ChannelRef | Production constraints are unspecified. |
| Applicable StoryIdea.source_refs UNKNOWN | EVIDENCE_NEEDED / NEEDS_RESEARCH | $.records[i].payload.source_refs / IdeaRef | Source research is incomplete. |
| Required rating.value UNKNOWN | EVIDENCE_NEEDED / NEEDS_RESEARCH | $.ratings[k].value / RubricRef | A required rating is unknown. |
| Portfolio pair UNRESOLVED | DUPLICATE_REVIEW_NEEDED / REVIEW_DUPLICATE | $.human_findings.duplicate_findings[k].outcome / ChannelRef | A portfolio comparison is unresolved. |

Last two rows pin future literal fixture strings/paths consistent with existing
findings codes, not changes to HumanFindingsInput. Existing RC D01–D16 apply unchanged.

## 5. Owner decision register and readiness

| Decision NOT APPROVED | Exact recommendation / alternative | Impact |
| --- | --- | --- |
| Q1-A/B/C | Main C and all applicable current checks; worst-state matrix; same-identity explicit human revision, no cross-identity override | Claim/evidence classifier and resolution handling |
| Q2-A/M | Explicit blocking flag/resolution table for all severities/categories; coherent recorded resolution review predicate | Generic Risk blocker versus unestablished mitigation |
| Q2-C | Alternative A complete generic EVIDENCE_NEEDED BLOCKED mappings; or owner-returned exact alternative B code matrix | Ethical/legal/reputational/market/production diagnostics; no new codes |
| Q2-V/K | Current revised documented material rather than fallback Text; no staged/capability proof or keyword subtype inference | Rights/fallback and capability boundaries; BX remains conditional |
| Q3-A/B/R | Explicit essential human specs versus permissible hypotheses; exact supported profile tuple | Framing/UNKNOWN/profile admission and literal messages |

If these choices are approved exactly, remaining work is bounded implementation and
independent genuine fixtures, not new SI records/operations/services. Until then full
EVALUATE **NOT READY FOR IMPLEMENTATION**. Existing SI/1 cannot prove complete world
check registry, cross-id supersession, real licence/staging/CPU availability or actual
human identity; those guarantees are not silently included in this proposal.

[T25 oracle](STORY_INTELLIGENCE_SI_E02_2_1E_T25_TEST_ORACLE.md) is complete for its
specified synthetic input under recommended choices, **CONDITIONAL — OWNER APPROVAL
REQUIRED** wherever Q1/Q2/Q3 apply. No executable PASS/golden vector claimed.
RC-P01–P06 and C01–C48 are approved only per
[owner approval scope](STORY_INTELLIGENCE_SI_E02_2_1E_RC_OWNER_APPROVAL_2026_11_12.md).
**Unit tests: NOT RUN — DOCS ONLY.** RU/UA wire `ru/uk`, CPU-only/licensing gates,
G01/G02/F1-D1/R1 precedence unchanged. EVAL-P05 OPEN; PUBLISH_REVISION DISABLED;
partial COMMIT reconstruction OFF; Windows S3.2b BLOCKED_HOST_NOT_PROVIDED.
STOP; no code/tests/PR/merge/release/main changes.
