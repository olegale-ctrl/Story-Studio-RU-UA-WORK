# SI-PRODUCT-01.1 — Editorial Decision Projection V1 implementation task draft

Дата: 2026-11-13. **DRAFT / NOT AUTHORIZED FOR EXECUTION.**
Это проект будущего задания, не authorization реализации или публикации. Архитектура
SI-PRODUCT-01.0 утверждена; старт implementation требует отдельного решения владельца.

## 1. Owner handoff gate and exact source

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Frozen proposal/reference: `5e0ddf45aacb2412dd15b9a4923acb40c6a6c7bd`;
evaluator foundation: `35451f6441bd5428e132ae65f2080209b51fe009`.
Нормативный approval: [OWNER_APPROVAL_2026_11_13](STORY_INTELLIGENCE_SI_PRODUCT_01_0_OWNER_APPROVAL_2026_11_13.md).

**Future exact implementation base: TO_BE_PINNED_BY_OWNER.** Владелец должен явно
передать SHA, содержащий recording approval и согласованные документы, разрешённый
файловый scope и publication policy. Не выбирать main, archive-only branch, latest
или один старый proposal commit. До этого этот draft не executable task.
Suggested future branch (также нуждается в handoff):
`feat/story-intelligence-si-product-01-1-projection-v1`.
Remote HEAD проверять только если владелец отдельно опубликует и укажет source branch;
не выполнять push, чтобы самостоятельно удовлетворить preflight.

При будущем старте: clean/unmerged/exact base, same-source evaluator + frozen contract,
все восемь APPROVED и PD-01/PD-05 conditions. Material contradiction или необходимость
изменения accepted evaluator/SI code → STOP с воспроизводимым contract gap; не чинить
за пределами scope и не придумывать подмножество каталога.

## 2. Proposed future file scope — requires explicit task authorization

New files only:

- `story_intelligence/decision_projection_v1.py`
- `tests/test_story_intelligence_decision_projection_v1.py`
- `tests/test_story_intelligence_decision_projection_oracles_v1.py`
- `docs/tasks/STORY_INTELLIGENCE_SI_PRODUCT_01_1_IMPLEMENT_RESULT.md`

Plus append-only `project-log/WORKLOG.md` if included in the owner's future allowlist
under existing repository rules. Данный список — draft task boundary, не разрешение
создать эти файлы сейчас. Existing tests/source/contracts/config/dependencies не менять.
Benchmark helpers размещать только в будущих allowlisted test modules, не в новых
неуказанных scripts/artifact files. Synthetic log outputs — вне Git.

## 3. Intended implementation

Реализовать pure read-only presentation над actual evaluate_si result и exact invocation
arguments согласно [approved contract](STORY_INTELLIGENCE_SI_PRODUCT_01_0_CONTRACT_PROPOSAL.md)
и [approved oracles](STORY_INTELLIGENCE_SI_PRODUCT_01_0_TEST_ORACLES.md). Public function
name определяется future handoff; conceptual arguments остаются evaluation_inputs,
evaluation_result, explicit display_locale. Это local value API, не SI wire registration.

- Разделить OK eligibility и Rejected, DISPLAYABLE/UNAVAILABLE/AdmissionFailure.
- Выполнить safe evaluator re-verification PD-01. Сравнение не заменяет result,
  не меняет inputs и не исправляет findings. No shortcut/digest-only acceptance/cache.
- Закрытый selector/catalog на все 30 families, exact path/type/fixed emitter; никакого
  перевода arbitrary messages или получения class только из reason code.
- Fixed RU/UK strings, source aliases, nine approved criterion labels, five sections,
  exact numeric/UNKNOWN formatting и L1..L6. No added threshold/ranking/probability.
- Preserve every slot/order/blocker, включая lower-priority findings и pair/criterion
  distinctions; no top-N/dedup by visible text, no private Text/technical identifier copy.
- No fabricated science, rights, reviewer identity, audience demand, hooks/assets/Brief.
- CLOCK для измерения допускается только в test harness снаружи pure function; никаких
  filesystem/network/LLM/provider writes/calls в projection, persistence или UI.

## 4. Mandatory executable acceptance, not evaluator-only evidence

Матрица **30 families × 2 locales** должна иметь реально выполненные witnesses:
RC01–RC09; C01–C05; K01–K06; V01; Q01–Q04; F01–F05. В отчёте таблица family→test→RU/UK
результат, каждый family/locale слот покрыт. Отдельно оба K path variants, C05 central/
noncentral и другие approved applicability variants; не выдавать 60 slots за ровно
60 unittest methods или за полную coverage всего evaluator.

Включить P01–P42, family expansions, literal W01 RU/UK, real T25 and C14/C44 preservation,
all five eligibility decisions, actual STALE/INVALID, rejected/null shape, explicit
locale and missing/unsupported inputs, multidiagnostic losslessness, privacy adversaries,
determinism and input/output detachment. Все существенные blocking findings видны;
score1000/positive review не снимают остальные conditions.

Для valid cases использовать настоящие accepted evaluator outputs из genuine synthetic
content-addressed graphs. Expected outputs authored independently from renderer;
не получать expected strings/codes из его собственных helpers. Нельзя mock resolver,
provenance, currentness или verification как «успешные». Для контроля повторного вызова
допускается наблюдать wrapper, который действительно вызывает real evaluator; одного
spy counter без настоящего вызова недостаточно.

Доказать на исполнении: altered supplied score/status/code/message/ref/path либо
удалённый blocker дают отказ, actual recomputation exception не даёт accepted card,
все inputs unchanged; cached/trusted flag не обходит повторную проверку. Не создавать
новую re-verification policy ради прохождения tests. Performance/measurement instrumentation
не меняет function output и не превращает unsafe optimization в допустимую.

## 5. PD-01 performance measurement plan

Вне production pure function измерить stdlib monotonic/perf_counter harness:

- evaluator-only call;
- полный projection call с обязательным real evaluator re-verification;
- минимум B, T25, W01 и genuine multi-finding fixture с несколькими blockers/sources.

Записать OS, Python, CPU и доступные resource limits, records/refs/diagnostics counts,
methodology/warm-up/sample counts, минимум три измеренных повторения на case,
raw durations, min/median/max. Если cost высока — сообщить фактическое ограничение,
не выключать verification и не объявлять measurement performance qualification.
Никаких speed promises, новых numeric latency quotas или performance-based eligibility.
Изменение verification mechanism: **отдельный контракт и owner approval обязательны**.
Точное время не должно появляться в Card/доказательстве scientific/production readiness.

## 6. Commands and report for the future authorized task

После реализации реально выполнить в проектной `.venv`:

```text
python -m unittest discover -s tests -p 'test_story_intelligence_decision_projection*.py' -v
python -m unittest discover -s tests -p 'test_story_intelligence_evaluate*.py' -v
python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v
python -m unittest discover -s tests -v
python -m compileall -q story_intelligence tests
git diff --check
```

Для каждого — actual count, exit code, failures/skips; parameterized scenarios считать
отдельно от unittest methods. Ненулевой exit не PASS даже при строке unittest OK.
Existing evaluator tests — только regressions; они не Projection acceptance.
Невыполненные projection/performance проверки не заменять предположением.

RESULT: exact future base/parent/HEAD, files/stats, executable 30×2 coverage и variant
matrix, P01–P42/W01 outcomes, PD-01 measurement/evidence, privacy/nonmutation findings,
ограничения, отсутствие protected changes. Git clean/allowlist/exact commit checks.
Publication policy должна быть явно задана в отдельном owner task; default no push,
PR/merge/tag/release. Только local artifacts до explicit authorization.

## 7. Immutable boundaries and STOP

No evaluator/SI/1/Request/RunRecord/EvaluationReport changes, no protected storage,
new dependencies, providers, external services, source discovery, generation, production
or authority. RU/UK, CPU-only и лицензии сохраняются. EVAL-P05 OPEN;
PUBLISH_REVISION DISABLED; partial COMMIT reconstruction OFF;
Windows S3.2b BLOCKED_HOST_NOT_PROVIDED.

**THIS DRAFT MUST NOT BE EXECUTED NOW. STOP до отдельного задания владельца.**
