# SI-E01.2b.2 — Pure Run Provenance Verification

Дата: 2026-11-10. Реализовано в bounded read-only scope; независимая приёмка
этого результата ещё требуется. Consistency verification не доказывает actual
execution, human identity, права или разрешение на production/export.

- Base: `112ebd76b2a08fc2ba44cfcd53a3a2c8979f832c`.
- Source: `docs/story-intelligence-si-e01-2b-1-independent-acceptance`.
- Feature: `feat/story-intelligence-si-e01-2b-2-pure-provenance`.
- Source remote HEAD проверен **до изменений** и совпал с exact base.
- Final commit/remote SHA публикуется после commit/push в handoff; собственный
  commit hash нельзя буквально включить в содержимое того же коммита. Проверяются
  exact parent/base, remote equality и clean worktree.

## Основание и scope

Прочитаны [полный bounded task](STORY_INTELLIGENCE_SI_E01_2B_2_CODEX_TASK.md),
[resolver independent acceptance](STORY_INTELLIGENCE_SI_E01_2B_1_INDEPENDENT_ACCEPTANCE.md),
[local records/F1 acceptance](STORY_INTELLIGENCE_SI_E01_2A_RESUME_F1_INDEPENDENT_ACCEPTANCE.md),
[original](STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md),
[R1](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md),
[R1a](STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md),
[R1b](STORY_INTELLIGENCE_V1_R1B_REVIEWPACKET_FIELD_PATH_CLARIFICATION.md),
[его approval](STORY_INTELLIGENCE_V1_R1B_OWNER_APPROVAL_2026_11_09.md),
[SI-D01–D10 approval](STORY_INTELLIGENCE_V1_OWNER_APPROVAL_2026_11_09.md) и accepted
codec/model/records/resolver/test sources. Приоритет original → precise R1 → R1a →
approved R1b сохранён. RFC `c6923614b932b0dbbb667cdd54dea1646d0a758b` не используется
как база/контракт или implementation dependency. Его предложения не реализованы.

Созданы только четыре новых файла:

| Файл | Назначение |
|---|---|
| `story_intelligence/provenance_v1.py` | Единственный public API verify_si_provenance |
| `tests/test_story_intelligence_provenance_v1.py` | Genuine topological graphs, stage/ancestry/root adversarial cases |
| `tests/test_story_intelligence_provenance_vectors_v1.py` | Девять literal positive bundle/root/manifest byte/hash cases |
| `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_2_RESULT.md` | Этот отчёт |

Нового blocking gap не обнаружено, optional CONTRACT_GAPS не создан. Все изменения
new/A-only; существующие modules/tests/vectors/contracts/approvals/reports, WORKLOG,
config/dependencies/CI, editorial/storage и main не меняются.

## API и порядок проверки

`verify_si_provenance(records, roots) -> list[SIRef]`.

Сначала вызывается принятый `resolve_si_closure` — exact record/ref hashes,
structural validation всего supplied bundle, typed transitive DAG, cycles, missing
refs, canonical Closure, полный Run.input_snapshot. Его errors не заменяются
provenance guesses. Условие входа: caller не меняет данные конкурентно во время
вызова. После resolver используется private detached copy records, indexed по
уже проверенной Header identity; user-supplied mapping keys не считаются proof.

Проверяется **каждый reachable record**. Manifest возвращается detached и canonical
только после успешного завершения всех проверок. Unrelated records имеют лишь
прежнюю structural validation boundary resolver, не provenance certification.
Нет auto-latest, repair/autofill, persistent cache, output issuance или операций.

| Record/origin | Actual generating Run tuple |
|---|---|
| Initial StoryIdea | DISCOVERY / si.discover-local / 1-r1 |
| Initial CreativeAlternative | CREATIVE / si.creative-templates / 1-r1 |
| Initial EvaluationReport | EVALUATION / si.evaluate / 1-r1 |
| Initial ReviewPacket | PACKET_EXPORT / si.review-packet / 1-r1 |
| RULE_DERIVED ProductionBrief | BRIEF_ASSEMBLY / si.brief-assembly / 1-r1 |
| HUMAN_EDIT revision | REVISION / si.human-revision / 1-r1 |

Проверяются реальные поля resolved RunRecord, а не только словарь origin output.
Внутренняя корректность Run.stage/method/version уже проверяется local validator,
но соответствие этого Run **конкретному output mechanism** устанавливается здесь.
У MANUAL_INPUT/USER_IMPORT нет generating Run по strict Header rules. RUN_METADATA
не превращается в доказательство выполнения engine. Run.output_refs не вводятся.

## Полная previous ancestry и Creative dual-run

Все exact previous refs до revision1 разрешены и hash-verified resolver. Нумерация
same type/id/immediate predecessor проверена accepted Header validator; здесь
читаются actual supplied predecessor records, без пропуска/синтеза промежуточной
revision. Данные ancestors не меняются. HUMAN_EDIT не может переиспользовать ни
один ancestral generating Run в качестве текущего generating Run.

Для CreativeAlternative определяется genesis K1 из полной previous chain:
K1.H.origin.run_ref == K1.payload.run_ref и actual stage CREATIVE. У K2/K3/etc
payload.run_ref обязан остаться **тем же exact K1 originating Run**; current
H.origin.run_ref обязан быть отдельным actual REVISION Run. Alien/new CREATIVE,
подставленный REVISION Run и частично переписанная ancestry отклоняются даже
когда все переданные SHA, refs и snapshots self-consistent.

При сохранённом exact root изменение ancestor bytes обнаруживается hashes.
Если caller скоординированно перепишет всю историю и предоставит **новый root**,
это новая self-consistent claim, а не доказуемый trusted historical original.
Без внешнего trust anchor нельзя обещать обнаружение всех coordinated rewrites
или подтвердить actual generation. Tests не подменяют эту границу authenticity.

### HUMAN_EDIT direct roots — не audit snapshot

R1 §2: `REVISE_INPUT — base_ref затем payload refs`, schema order;
R1a §4: H.input_refs начинается с base_ref, затем direct payload refs, включая C.
Run.semantic_input_refs — direct substantive roots операции по R1 §1.3.
По этим однозначным правилам expected list = `[exact H.previous] + direct payload SIRefs`.
Typed payload extraction использует accepted resolver schema walker read-only;
ERefs исключены, повторяющиеся entries semantic arrays не deduplicated.

H.input_refs и actual REVISION Run.semantic_input_refs должны точно совпасть с
этим списком, включая порядок. Наличие previous лишь в Run.input_snapshot или
captured context не заменяет direct semantic input. Actual snapshots остаются
canonical Closure этих declared roots/context и уже проверяются resolver.
Для initial derived outputs DAG/no-output-cycle гарантирует resolver; здесь не
угадываются отсутствующие context/request parameters и новые operation prerequisites.

Ошибки новых cross-record bindings — существующий PROVENANCE_MISMATCH с paths
`$.records[i].H.origin.run_ref`, `.payload.run_ref`, `.H.previous`, `.H.input_refs`
или `$.records[j].payload.semantic_input_refs` generating Run. Missing/hash/type/
cycle и malformed-data errors продолжают приходить из принятых модулей.

## Независимые graphs и vectors

Fixture builder начинает с independent accepted graph test data, затем **topologically
перестраивает весь downstream graph**. Record SHA/root refs, H.previous/origin,
semantic roots, snapshots, Packet manifests/context/privacy digests пересчитаны
stdlib JSON/hashlib, без production SI hash methods и без mocks resolver.
Oracle edges строятся независимым test-only data-ref traversal на авторских closed
fixtures, не production schema walker. Strings не парсятся, ERefs имеют другую форму.
Положительные fixtures содержат все generating stages, manual/import, legal Source
HUMAN_EDIT chain и K1/K2/K3 с одним C и разными R2/R3.

**Девять literal cases:** manual, import, discovery_run, evaluation, creative_initial,
assembly, packet, revision, creative_dual_runs. Файл содержит exact literal input
bundle bytes/SHA (95,920 bytes), отдельные literal roots bytes/SHA и expected canonical
manifest lists/bytes/SHA. Они вычислены отдельно std JSON/hashlib/explicit-edge oracle,
не verifier/resolver/production hash functions. Ожидаемые значения hardcoded, не
создаются вызовом production API при определении tests. Повторный audit через AST
literal parsing + std JSON/hashlib без production imports подтвердил все bytes/SHA.
Generator и runtime logs остаются вне Git. Новых host tools/dependencies не требовалось.

### Adversarial cases с корректными hashes

В каждом provenance-negative graph сначала явно утверждается успешный
**resolve_si_closure** и совпадение с independent Closure oracle, и лишь потом
ожидается PROVENANCE_MISMATCH от нового verifier:

- Все шесть actual generating stages подменяются на другой stage с соответствующим
  **ему** допустимым method/version. Local Run shape и hashes остаются корректны.
- K2 payload original Run меняется на другой actual CREATIVE Run с корректными
  fields/refs; K1 exact original остаётся прежним.
- K3 payload original подменяется actual REVISION Run K2.
- K1 origin/payload скоординированно переписаны на alien CREATIVE Run; downstream
  refs rehashed, но K2 сохраняет несовместимый original. Genesis binding выявляет это.
- K3 повторно использует generating REVISION Run K2.
- Revision Run direct base заменён K1 вместо K2, direct base есть лишь в snapshot
  через context, либо полный direct list переставлен при сохранении snapshot Closure.
- Human output H.input_refs нарушает payload schema order, оставляя previous первым.

Отдельные resolver-negative tests покрывают missing previous/Run, modified ancestor
bytes при сохранённом root, malformed roots/bundle. Проверены positive consistency,
input immutability, detached result, bundle-order independence и scope unrelated records.
Execution/user identity/rights/privacy readiness не утверждаются; старый Selection
не превращается в выбор новой creative revision и не обновляет свои exact target refs.

## Фактические тесты и проверки

Среда: Linux x86_64 / Python 3.12.14, проектный `.venv/bin/python`.
Previous reported baseline: 85 targeted / 927 full; новые counts не предполагались
без запуска. Commands:

```bash
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_provenance*.py' -v
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v
.venv/bin/python -m unittest discover -s tests -v
```

Первоначальная development suite без vectors: 13 OK, 3.023 s, exit0.
Окончательная provenance suite: **15 OK**, 3.856 s, exit0 (13 graph + 2 vector methods).
Окончательная общая SI suite: **100 OK**, 9.071 s, exit0 (прежние 85 + 15 новых).
Полный прогон: **942 OK**, 775.323 s, exit0; failures=0, errors=0, skipped=0,
expectedFailures=0. Это прежние 927 + 15 новых methods. Существующие storage/S1/S2/
D-01/LAB suites прошли; S2.3 дополнительно сообщил 1659 параметризованных сценариев
(не дополнительные unittest methods). test_sprint23_2.Sprint232Tests.test_env_override
прошёл на Linux; baseline ошибок окружения не обнаружено. Все три обязательных
прогона фактически выполнены. Development runs не имели неожиданных failures.

Accepted resolver @ `0c27547377255016ec2fc399090ce99b63d69485`, records/F1 @
`557c1fafac9a8bccd0421164436aa17886b82a77`, прежние 14 foundation / 18+3 record-value /
7 graph vectors сравнены с pinned commits — byte-identical. Перед commit проверены
syntax, report links/fences, git diff --check и staged diff check, exact A-only
allowlist и source/base SHA. Production imports — только copy, accepted model/resolver;
нет editorial/storage или внешних runtime dependencies. Post-push parent/remote
SHA equality и clean worktree проверяются в handoff. Никакого CI/native Windows PASS
из Linux unittest не следует. Итоговый diff: **4 новых файла, 583 additions,
0 deletions**.

## Ограничения, RFC и STOP

Нет semantic currentness/observed active context matching, selection-head readiness,
eligibility/rubric policy/scoring, actual source value/index/text grant verification,
ERef adapter/material verification, human identity/rights/privacy authorization,
request/response, operation execution/idempotency, persistence/storage или export.
Нет lazy loading, SQLite, Asset Registry, semantic evaluator, performance qualification,
Draft/Revision UX или других изменений RFC. Existing codec и его limits не менялись;
SI-F01 worst-case 1 MB integer latency не измерялась, новый digit cap не введён.

Production API использует только stdlib и принятые SI modules, без I/O/network/
Context7/provider/model/GPU/FFmpeg/renderer/clock/UUID allocation/protected writes.
PUBLISH_REVISION DISABLED; partial COMMIT reconstruction OFF; S3.2b BLOCKED_HOST_NOT_PROVIDED.
После публикации — STOP для independent review. SI-E01.2b.3, SI-E02 и RFC implementation
не начаты. PR, merge, release и изменений main нет.
