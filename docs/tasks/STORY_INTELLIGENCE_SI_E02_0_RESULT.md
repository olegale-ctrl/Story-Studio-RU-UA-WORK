# SI-E02.0 — Architecture inventory & contract gap mapping: result

Дата: 2026-11-10 (Europe/Kyiv).
**COMPLETED — DOCS ONLY / OWNER PROPOSALS AWAIT REVIEW / NO IMPLEMENTATION.**

## Git и preflight

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Source branch: `docs/story-intelligence-si-e01-2b-3-acceptance-e02-planning`.
- Exact base: `9a631ebca2bccdd8e0157528b20080380ba8dcfe`.
- New branch: `docs/story-intelligence-si-e02-0-architecture-inventory`.
- До изменений source remote HEAD точно совпал с supplied SHA; commit fetched.
  Working tree clean, unmerged paths/незавершённого merge нет. Новая ветка создана
  строго от exact base, без main/RFC/старой feature fallback.
- На exact commit проверено наличие [SI-E01.2b.3 final acceptance](STORY_INTELLIGENCE_SI_E01_2B_3_FINAL_ACCEPTANCE_2026_11_10.md)
  и [SI-E02 Planning Proposal](STORY_INTELLIGENCE_SI_E02_PLANNING_PROPOSAL_2026_11_10.md).
  Accepted currentness — pure read-only scope; independent runtime НЕ RE-RUN.
  Planning Proposal не принят как полный SI-E02 implementation contract.
- Final commit/remote SHA и diff/stat сообщаются после публикации в handoff;
  parent обязан быть exact base. Self-referential commit hash сюда не встраивается.

## Созданы только четыре документа

1. [ARCHITECTURE_INVENTORY](STORY_INTELLIGENCE_SI_E02_0_ARCHITECTURE_INVENTORY.md) —
   карта с IMPLEMENTED / CONTRACT_APPROVED / PROPOSAL / MISSING / BLOCKED и evidence
   по конкретным files/classes/functions. Слои schema/policy/runtime разделены.
2. [CONTRACT_GAP_MATRIX](STORY_INTELLIGENCE_SI_E02_0_CONTRACT_GAP_MATRIX.md) —
   повторное применение 18 SI типов, editorial counterparts, refs/currentness,
   human boundary, rubric/evidence/rights, audience/duration/visual/competition gaps.
3. [OWNER_DECISION_PROPOSAL](STORY_INTELLIGENCE_SI_E02_0_OWNER_DECISION_PROPOSAL.md) —
   только material owner choices P01–P05, alternatives/recommendations/blocked scope;
   конкретная RU science card, без полного сценария/новых wire types.
4. Этот RESULT.

Source/schemas/tests/config/dependencies, existing docs/контракты/RFC, WORKLOG,
editorial/storage и main не менялись. Никакого создания SI records, evaluator,
Discovery, UI, production assignment, ERef adapter, providers или реальных материалов.

## Основные выводы

- Принятый SI фундамент уже реализован: local types/canonical bytes/SHA, exact
  resolver/audit Closure, supplied provenance и semantic currentness G01/G02/F1-D1.
  Это не execution/evidence truth/rights/authority/production gate.
- Topic Discovery, EVALUATE, PROPOSE_CREATIVE, RECORD_SELECTION, ASSEMBLE_BRIEF и
  packet export имеют approved contracts/data shapes, но runtime executors отсутствуют.
  Source/claim/rating/creative/brief fields не доказывают существование engines.
- Девять criteria, weights и UNKNOWN/blocker priority уже утверждены SI-D04/R1.
  Новый ranking/tie/priority policy не утверждён; quantitative score не probability.
- SI ProductionBrief уже существует и покрывает pre-script card. Нового Brief wire
  не требуется; editorial BriefValue меньше и не взаимозаменяем с ним. Missing —
  builder/consumer/handoff, не название ещё одной схемы.
- SI Selection не поддерживает StoryIdea target: durable topic decision — реальный
  conditional gap. ProductionRevision не assignment queue; assignee/deadline/ack
  или автоматический job execution не представлены существующим workflow.
- Требуются separately scoped executable method postconditions/oracles; durable
  workspace lifecycle SI-D03 и ERef/adapter contracts — до соответствующих runtime
  путей. Текущий relevant ERef без validated material остаётся INVALID/REF_MISSING.
- Editorial packages/consistency/history/rights material binding реализованы как
  pure checks. S1 и D1–D12 approved, S2/portable LAB реализованы только в RAM/fixtures;
  native Windows service/protected writer не готов. Historical concept review
  2026-11-05 не отменяет более поздних approvals.
- Переписывание завершённых этапов не требуется. Недостаточность existing SI/1 типов
  для самой карточки/scoring data/Brief не доказана; новые roles/operations допустимы
  только после конкретного owner requirement и отдельного contract approval.

## Вопросы для owner review — не новые утверждения

- P01: criterion comparison/manual priority или отдельно спроектированный automatic
  cross-candidate ranking; approved Rubric weights не пересматриваются.
- P02: нужен ли durable intent именно по теме; если да — отдельный minimum scope/
  operation proposal на existing identities, не editorial APPROVE и не скрытый reason blob.
- P03: первый consumer — private human-readable existing Brief или отдельный будущий
  automated handoff/assignment contract; рекомендуется private Brief first.
- P04: ERef-free local SI deliverable первым либо приоритет отдельному read-only
  exact editorial snapshot adapter contract; rules fail-closed уже обязательны.
- P05: дополнительный science-specific review coverage/profile до production brief
  readiness; general evidence/rights blockers не предлагается отменять.

Пример «Почему исчезли древние цивилизации?» описан как conceptual research draft:
ru, научно-популярный стиль, 480–720 s, BALANCED, audience assumption/UNKNOWNs,
центральный вопрос, 3 hooks, 7 chapters с суммой target 600 s, visuals и риски.
Ожидаемый BLOCKED — policy illustration, не вычисленный результат method; SIRefs,
цитаты, лицензии или фактологические подтверждения не выдуманы. Это не полный script.

## Проверки и ограничения evidence

**Unit tests: NOT RUN — DOCS ONLY.** Результаты прежних 986 тестов не объявляются
новым запуском или независимым runtime proof. Ничего не устанавливалось/рендерилось;
новых тестов/моделей/медиа/ключей/реальных персональных данных нет.

Выполнены: exact four-file A-only allowlist; relative links/fences; проверка
**87 file links и 34 named Python symbols** по существующим files/AST. Historical
E00 Git object проверен по exact commit и не представлен как current-tree файл.
Проверены 9 weights sum 100, 7 chapters sum 600, пять material owner questions,
G01/G02/F1-D1 consistency и отсутствие existing-file изменений.
`git diff --check` / `git diff --cached --check` — exit 0.
После commit/push проверяются exact parent/base, remote equality и clean worktree.
Фактические QA результаты сообщаются в handoff. Документационный QA не является
runtime/Windows/security/license qualification или утверждением новых proposals.

Обязательные ограничения сохранены: wire ru/uk при пользовательском RU/UA;
CPU-only target; лицензии и intended-use clearance до коммерческого использования;
без китайских корпусов/Writing-DNA auto-adoption. `PUBLISH_REVISION` DISABLED;
partial COMMIT reconstruction OFF; Windows S3.2b BLOCKED_HOST_NOT_PROVIDED.
Без PR/merge/release/main изменений. SI-E02.1/E02.2 и реализация не начинались.
**STOP после публикации для независимого review.**
