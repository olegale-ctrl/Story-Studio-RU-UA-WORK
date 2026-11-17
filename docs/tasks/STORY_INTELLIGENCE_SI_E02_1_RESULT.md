# SI-E02.1 — Owner decisions P01–P05 and contract preparation: result

Дата: 2026-11-10 (Europe/Kyiv).
**COMPLETED — DOCS ONLY / PRODUCTION IMPLEMENTATION NOT AUTHORIZED.**

## Git и preflight

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Source: `docs/story-intelligence-si-e02-0-architecture-inventory`.
- Exact base: `a577746f308828d75d2ea7262eaa94ab18a523c1`.
- Publication branch: `docs/story-intelligence-si-e02-1-owner-approval`.
- До изменений source remote HEAD и local commit равнялись exact base; clean
  worktree, unmerged paths/незавершённого merge не было. Ветка создана только от
  указанного commit, без fallback/merge/rebase или main changes.
- Final commit/remote SHA и diff/stat сообщаются после публикации в handoff;
  parent должен быть exact base. Self-referential hash в собственное содержимое
  commit не встраивается.

## Четыре новых документа и раздельные статусы

| Новый файл | Статус и результат |
| --- | --- |
| [OWNER_APPROVAL_2026_11_10](STORY_INTELLIGENCE_SI_E02_1_OWNER_APPROVAL_2026_11_10.md) | **APPROVED / OWNER DECISION** только для P01–P05, выбранные options 1/2/1/1/2 |
| [TOPIC_INTENT_CONTRACT_PROPOSAL](STORY_INTELLIGENCE_SI_E02_1_TOPIC_INTENT_CONTRACT_PROPOSAL.md) | **PROPOSAL / NOT APPROVED**: альтернативы existing Selection extension, exact scope/history/admission/retry/freshness/privacy и независимые oracle requirements |
| [SCIENTIFIC_REVIEW_PROFILE_PROPOSAL](STORY_INTELLIGENCE_SI_E02_1_SCIENTIFIC_REVIEW_PROFILE_PROPOSAL.md) | **PROPOSAL / NOT APPROVED**: reuse evidence/review records, семь proposed coverage labels, blockers/escalation, capture alternatives и oracle requirements |
| Этот RESULT | Фактические документационные проверки, ограничения и STOP |

Утверждено: P01 criterion-by-criterion comparison по прежней SI-D04 rubric, человек
определяет приоритет; P02 только проектирование topic intent; P03 existing SI Brief
для private human-reviewable card; P04 local ERef-free bounded path first, без
очистки existing ERefs; P05 только requirements design science profile.
Automatic ranking/ties/priority execution, новые actions/wire/version, UI/adapters/
persistence/evaluators/production integrations не утверждены.

## Основные предложения, а не новые контракты

Topic proposal доказывает границу existing Selection: scopes Creative/Brief и их
closed choices/targets не выражают intent по StoryIdea. Рекомендован minimum
**versioned** extension Selection, а не parallel approval type. Candidate purpose
TOPIC_INTENT и RESEARCH/DEFER/REJECT/PRIORITIZE — только предложенные обозначения;
current SI/1 должен продолжать отвергать неподдерживаемые values. Numeric rank/
queue/assignee/deadline не входят в предложенный minimum и не возникают из P01.

Предложены exact Idea/Audience/Channel scope, explicit human action, immutable
same-scope chain и новая explicit chain при смене target revision/context. Currentness
root не заменяет проверку target membership. Existing R1 byte-exact idempotency и
no-head-rollback не переутверждаются; будущему extension нужны versioned admission/
head/capture decisions и отдельно concrete SI-D03 lifecycle. Никакого actual operation.

Scientific proposal рекомендует requirements checklist на existing ClaimItem,
SourceItem, EvidenceItem, ClaimCheck, Risk/Creative/Visual/Brief refs. Семь labels
SR-C01–07 покрывают terminology/chronology/competing explanations/counter-evidence/
qualifications/source traceability/intended-use rights, но не являются SI enums,
permission codes или автоматически complete states. Existing qualification/null
metadata и evidence requirements соблюдаются. Отдельного ScientificApproval нет.

Высокие score/confidence не отменяют BLOCKED; scientific truth и credentials не
присваиваются. Profile capture/machine completeness ещё надо утвердить: words в
required_reviews/reason не machine proof, virtual checklist не получает fake SIRef.
Rights/lawful fallback и научные ограничения не снимаются private topic priority.

## Оставшиеся owner decisions до implementation

- TI-P01–TI-P02: формат/version/compatibility dispatch, exact purpose/action set и
  method/operation integration. P02 approval разрешил design, не эти wire tokens.
- TI-P03–TI-P05: exact admission/target/context binding, proposed same-scope chain/
  builder order, replay/applicability integration без изменения принятых R1 правил.
- TI-P06 и SI-D03/SI-D07: конкретная private persistence/atomicity/retention/privacy
  и lost-output behavior до durable implementation/export.
- SR-P01–SR-P04: profile form/version, exact coverage criteria/material traceability,
  human scope/escalation и отдельно machine-verifiable capture/completion mapping.

В обоих proposals есть alternatives, recommended path, compatibility costs и
independent expected-oracle tables. Полные content-addressed vectors/executable
тесты ещё не создавались: новый формат сначала должен быть утверждён. Нельзя
генерировать «правильные» oracle из будущей реализации или патчить resolver/hash.

## Проверки

**Unit tests: NOT RUN — DOCS ONLY.** Ничего не реализовывалось/устанавливалось;
старые test counts не выдаются за новый PASS. Проверены exact base/preflight,
strict four-file A-only allowlist, **40 relative file links** и Markdown fences.
Проверены mapping P01–P05 → 1/2/1/1/2, отдельные NOT APPROVED статусы proposals,
7 proposed coverage labels, compatibility с existing Selection/ClaimCheck/Brief
и неизменность existing source/vocabulary. `git diff --check` и staged diff check —
exit 0; после push проверяются parent/base/remote equality и clean tree.
Фактические публикационные SHA/stat и результаты QA сообщаются в handoff.

Original/R1/R1a/R1b, SI-D04, G01/G02/F1-D1, storage/A/O contracts и existing source,
schemas/tests/golden vectors/config/dependencies/RFC/WORKLOG/main не менялись.
ERef adapter, actual currentness implementation и protected authority не расширялись.
RU/UA сохранён с wire locales ru/uk; CPU-only target и обязательные licensing gates
до коммерческого использования остаются. Китайские корпуса/Writing-DNA не переносятся.
`PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF;
Windows S3.2b BLOCKED_HOST_NOT_PROVIDED.

Без PR/merge/release/main changes. SI-E02.2/implementation не начинались.
**STOP после публикации для independent review.** P02/P05 approval не превращает
два подготовленных PROPOSAL в утверждённые контракты.
