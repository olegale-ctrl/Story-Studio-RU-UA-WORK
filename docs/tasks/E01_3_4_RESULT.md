# E01.3.4 — результат docs-only проектирования package contract

## Выполнено

Подготовлен нормативный proposal
`docs/tasks/E01_3_4_PACKAGE_CONTRACT_PROPOSAL.md` на базе E00, E01.1a и принятых
результатов E01.3.1–E01.3.3. E00 и исторические документы не изменялись.

Proposal определяет рекомендуемые:

- exact roots и transitive closure для SCRIPT, SCENES и HANDOFF;
- различие historical и current packages;
- обязательные active slots и coherent chains;
- границу version conflict внутри target+closure без запрета snapshot history;
- точный canonical dependency payload и сортировку refs;
- связь target/content hashes с staleness ApprovalRecord;
- rights/source/asset зависимости каждого gate;
- ограниченную роль MaterialBindingState.CONFIRMED;
- будущую связку editorial digest с frozen handoff manifest и render preflight.

Документ содержит 11 сценариев изменения зависимостей и таблицу из 15
неоднозначностей: основание E00, варианты, рекомендацию и последствия.

## Главные выводы

SCRIPT package предлагается строить от exact ScriptRevision. SCENES и editorial
HANDOFF — от exact ScenePlanRevision. Все зависимости берутся только из
проверенного E01.3.2 graph; RightsReview subject binding не становится edge.

Новая history revision не меняет package, пока точная ссылка на неё не вошла в
closure нового target. Поэтому digest фиксирует фактически выбранные immutable
данные, а не условную latest version.

Dependency digest предлагается считать consistency token. Даже полное
совпадение gate/policy/target/digest не выдаёт approval authority, rights grant
или production readiness.

Текущая модель не содержит frozen handoff config/media manifest. Рекомендуется
считать HANDOFF digest editorial subset и позже связать его с отдельным
versioned manifest digest. Это решение особенно требует утверждения владельца.

## Требуется утверждение

В proposal отдельно перечислены десять групп решений. Ключевые из них:

- historical/current builders и active coherence;
- roots/closure трёх gates;
- трактовка HANDOFF до появления manifest;
- exact JSON shape и version key;
- target/dependency duplication и role arrays;
- conflict/dedup rules;
- rights composition и UNCONFIRMED draft behavior;
- historical reactivation и policy_version mapping.

Ни одна рекомендация не объявлена принятой нормой. Реализацию dependency digest
начинать нельзя до решения владельца.

## Изоляция изменений

Ветка: `docs/editorial-e01-3-4-package-contract`.
База: `b00fa95f9e8aeb7666188a9e0d4f278161bd6736`.

Добавлены только:

- `docs/tasks/E01_3_4_PACKAGE_CONTRACT_PROPOSAL.md`;
- `docs/tasks/E01_3_4_RESULT.md`.

Python-код и тесты не создавались и не изменялись. Модели, codec, integrity,
graph, rights_binding, Sprint 26, timeline v3, renderer и FFmpeg pipeline не
затронуты. Dependency digest, snapshot checksum, approval authority, expiry,
rights policy и readiness не реализованы.

Тесты не запускались: этап изменяет только документацию и не меняет executable
поведение. Выполнена проверка whitespace/patch через `git diff --check` перед
commit.

После публикации docs-only ветки работа останавливается для независимой проверки
и решения владельца. PR, merge и release не выполняются.
