# SI-E01.2b.3-F1-FIX — Current producer ERef guard result

Дата: 2026-11-10 (Europe/Kyiv).
**IMPLEMENTED / AWAITING INDEPENDENT ACCEPTANCE.**
Ниже — фактические проверки агента, не самостоятельное independent acceptance.

## База, ветка и authority

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Source branch: `docs/story-intelligence-si-e01-2b-3-f1-d1-approval`.
- Exact base: `5ade9a3c1798a882c5dc5ead393df73d054f1a39`.
- Fix branch: `fix/story-intelligence-si-e01-2b-3-f1-current-producer-eref`.
- Source remote HEAD до изменений точно совпал с handoff; worktree был clean.
  Ветка создана строго от указанного SHA. Owner сообщил DOCS ACCEPTED и отдельно
  запустил [полное FIX-задание](STORY_INTELLIGENCE_SI_E01_2B_3_F1_FIX_CODEX_TASK.md).
- [F1-D1 approval](STORY_INTELLIGENCE_SI_E01_2B_3_F1_D1_OWNER_APPROVAL_2026_11_10.md)
  D1–D5 обязателен наряду с original/R1/R1a/approved R1b и G01/G02. Предыдущие
  [F1 RESULT](STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_2_F1_RESULT.md) и
  [F1 GAPS](STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_2_F1_CONTRACT_GAPS.md) прочитаны
  и сохранены неизменными: это исторический diagnostic, не исправленный задним числом.
- Финальный commit/remote SHA сообщается после публикации в handoff; parent должен
  равняться exact base. Self-referential hash в содержимое commit не встраивается.

## Причина и минимальная правка

Ordinary HUMAN_EDIT пропускал producer-header check через early continue, а Creative
подставлял original C вместо actual REVISION Run из H.origin.run_ref. Поэтому
current producer R мог иметь unresolved header ERef, но record получал CURRENT.
F1-D1 теперь явно требует INVALID / REF_MISSING для этой позиции без exact validated
editorial snapshot, включая actual Creative R2/R3; original C остаётся независимым.

В [currentness_v1.py](../../story_intelligence/currentness_v1.py) добавлены ровно
**3 строки, 0 удалений**: комментарий и guard непосредственных H.editorial_refs Run,
полученного по H.origin.run_ref. Guard расположен до early HUMAN_EDIT continue
**и до** замены producer на original C. Прежняя проверка C не удалена.

Проверка выполняется в существующем semantic walk, **после** accepted full audit
DAG/hash/snapshot/provenance verification; также действует на содержательные
зависимости root. Новых graph edges/required-current Run identities не добавляется.
Вся audit Closure на ERefs не сканируется. Public API, projection, statuses/codes,
G01/G02, actual Run/C/previous/source hashes и original C direct ClaimItem constraints
не меняются. Нет adapter, snapshot API, новых fields/codes, I/O или broader refactor.

## Strict three-file diff

| Файл | Изменение |
| --- | --- |
| `story_intelligence/currentness_v1.py` | Existing module: +3 / -0, actual producer guard |
| `tests/test_story_intelligence_currentness_eref_f1.py` | Existing F1 diagnostic → approved regressions; fixtures сохранены, T2/T5 updated, новые controls |
| `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_F1_FIX_RESULT.md` | Только этот новый RESULT |

Другие existing/new files не менялись. В частности, старые reports/GAPS/approvals,
контракты, tests/vectors вне allowlist, codec/model/records/resolver/provenance,
RFC, WORKLOG, README, CI/config/dependencies, editorial/storage и main сохранены.
Нового contract gap при этом bounded fix не обнаружено.

## Red до production fix → green

Сначала изменён **только** allowlisted F1 test file: T2 получил нормативный
INVALID/REF_MISSING вместо прежнего CURRENT characterization; T5 больше не
подтверждает старую асимметрию. Добавлены current Creative R3, два historical-only
controls, 8 integrity subcases и transitive current dependency case.

До red bytes production сравнили с exact base; SHA-256:
`67c035282131bd2f37f2b4a605d28c2ed191eac0a866ff998d1867773d255bed`.
Настоящий запуск на старом source: **10 tests, 4 FAIL, 0 errors/skips**,
unittest 1.191 s, diagnostic elapsed 1.320 s, **raw Python exit 1 / outer exit 1**.
Падали T2, T5, T6 и T10: actual CURRENT/[] вместо approved INVALID/[REF_MISSING].
T1/T3/T4, historical controls T7/T8 и integrity T9 проходили уже на старом source.
Это ожидаемый development red, не финальный PASS и не waiver.

Затем внесены только 3 production строки. **Тот же test file без ослабления assertions**:
**10 tests, OK, 0 failures/errors/skips**, unittest 1.256 s,
diagnostic 1.389 s, **raw Python exit 0 / outer exit 0**. Нет skips/expectedFailure.

## Графы, resolver/provenance и результаты случаев

Во всех valid cases используются реальные canonical records и exact SHA. Accepted
si_record_ref проверен против независимого stdlib JSON/hashlib fixture hashing;
explicit-edge Closure oracle равен accepted resolver/provenance manifests.
После добавления synthetic ERef перестроены downstream refs и frozen snapshots.
Нет mock/patch hashes/resolver/provenance или подстановки outcomes вместо вызова API.
Проверяется отсутствие мутации inputs. Observations не становятся trusted authority.

| Case | Где ERef / scope | Audit / provenance | Результат после fix |
| --- | --- | --- | --- |
| T1 | Ordinary Source S1→R→S2, без ERef | PASS, 3 refs | CURRENT / [] |
| T2 | Только current actual R.H; S2 own H пуст/payload ERef=null | PASS, 3 refs | INVALID / [REF_MISSING] |
| T3 | Direct current S2.H ERef | PASS, 3 refs | INVALID / [REF_MISSING], прежний guard сохранён |
| T4 | Original C.H ERef, actual Creative R3 clean | PASS, 19 refs | INVALID / [REF_MISSING], прежний C guard сохранён |
| T5 | Approved boundary comparison T1–T4 | PASS на valid inputs | T1 CURRENT; T2/T3/T4 INVALID |
| T6 | Только actual Creative R3.H ERef; original C и K3 own H clean | PASS, 19 refs | INVALID / [REF_MISSING] |
| T7 | Только historical R2.H ERef, Source S3 current R3 clean; S2/R2 inactive | PASS, 5 refs | CURRENT / [] |
| T8 | Только historical Creative R2.H ERef; current R3 и original C clean; old K2/R2 inactive | PASS, 19 refs | CURRENT / [] |
| T9 | 2 graph families × missing R2 / corrupt R2 / bad previous SHA / bad snapshot SHA | Отказ обоих accepted validators | INVALID: REF_MISSING для missing R2, REF_HASH_MISMATCH для остальных; 8 subcases |
| T10 | Root EvidenceItem сам manual/clean, substantive current Source S2 имеет actual R ERef | PASS, 5 refs | INVALID / [REF_MISSING], проверяется не только root |

В T7/T8 historic-only ERef остаётся в проверенном audit graph и не делает current
revision INVALID; independent substantive constraints не отбрасываются. При этом
missing/corrupt history в T9 не превращается в STALE или разрешённый CURRENT.

### Буквальные graph/context hashes

Graph hash = SHA256(C(records)) в construction order. Context hash =
SHA256(C({active_input_refs,selection_head_refs})); это fixture observation value,
не новый wire ContextSnapshot. Все refs/hash values синтетические, не реальные
editorial material/evidence. T2 graph остаётся **тем же** историческим reproducer.

| Case | Graph SHA-256 | Context SHA-256 |
| --- | --- | --- |
| T1 | `f37a7b1e6414486d4650fb1bdc78ff08799b090ae7ce18a89c992a1e44213311` | `b00fb082d50d60b0c38d9ff3762110ff7a0ff3951b96901d373ac9f693729844` |
| T2 | `87b0f65a5d741ca48b34333f120f41a5b7cbb2c54e2914e954b108528a41f55b` | `c6fb19b10547f9979d02127b54d77036cdf9ef9e88610cdafdaf8249b276e793` |
| T3 | `af4948494a638898bb2b664c2b358dd372b8bdbd6ddaee4570ad7a807ad59dbb` | `d6edefa838d2b62dd12395c3707014f1395959da4ddcd50a02461b9b59f061e9` |
| T4 | `00b76408f63c39fb627ee3e52a72b4534902160ededeca6fff50d0271a64d1ec` | `c8c419a7b7123f921490f5897f07f5cb3b03aef19b35b1e70626aa7c1139fd45` |
| T6 | `9e256aa6839058f9fbcc2d41a24ffbca11dbb6d3faf0d42117e74f14cec062e8` | `2582bb61c4390e2e2cb97ec26e730b9c4284f1f56fe2e8d61256f99233e18a7f` |
| T7 | `890d9c525e911fc60778cbf7fc13ce2ae97a9c695c35cbb35ee594449d9acd62` | `2b8554b1afec1f923142a473a60a559568a352efb029eae9ea87988620db2124` |
| T8 | `753b111c513bb8c03061ebdd9f25a8fbd77810b17a92a5a5ca09ef810c7d4bc0` | `633497c823e6956f3c16df779c08be0614aa5ec99d9b847655ea3327c203ede8` |
| T10 | `873722507d36857b9b47c939988a7a3bda891d173ca62ba2ee52ecbf5b043a47` | `62a4f392f5514faa72e9c36fb53c14c76966619436b2e59134900142058dcab2` |

T6 actual R3 SHA: `2973967a2023d0501f24e76548c3d37e2ab546e5e00016a9fa5f60bdb3e7090b`;
original C SHA: `0099be3529a8f7266f1673abb9b102fceb09061fde6a39fb7f5ff3ab3f84dd58`.
T7 actual R3 SHA: `e84adc31cd25d40c6067c44fb5106486bd158fa6142e98a2ac3defa28f7cd115`.
T8 actual R3 SHA: `52a50aeeadce28dd0063378eaab6d7249bd5d03349f387100c0a30312834e28d`.
Это настоящие record hashes; ERef itself остаётся well-formed unresolved fixture,
без trusted snapshot/adapter. Для воспроизведения доступны source_case,
historical_source_case, creative_case и evidence в allowlisted F1 test file.

## Все обязательные команды и фактические exits

Среда: Linux x86_64, project `.venv/bin/python`, Python 3.12.14.

```bash
.venv/bin/python -m unittest tests.test_story_intelligence_currentness_eref_f1 -v
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_resolver*.py' -v
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_provenance*.py' -v
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_currentness*.py' -v
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v
.venv/bin/python -m unittest discover -s tests -v
```

Первая команда выполнена отдельно red и green. Final suite results:

| Suite | Tests / summary | Unittest duration | Diagnostic elapsed | Raw Python exit | Outer exit | Failures/errors/skips |
| --- | --- | --- | --- | --- | --- | --- |
| F1 green | 10 / OK | 1.256 s | 1.389 s | 0 | 0 | 0/0/0 |
| Resolver | 19 / OK | 3.308 s | 3.451 s | 0 | 0 | 0/0/0 |
| Provenance | 18 / OK | 3.977 s | 4.119 s | 0 | 0 | 0/0/0 |
| Currentness | 41 / OK | 10.501 s | 10.608 s | 0 | 0 | 0/0/0 |
| All SI | 144 / OK | 18.296 s | 18.454 s | 0 | 0 | 0/0/0 |
| Full | 986 / OK | 806.594 s | 806.973 s | 0 | 0 | 0/0/0 |

Каждый command запускался subprocess.run с точным argv, stdout/stderr без фильтра
сохранялись в `/tmp/si_currentness_f1_fix_{red,green,resolver,provenance,currentness,si,full}.raw.log`.
Raw child return code явно напечатан; nonzero передаётся sys.exit(returncode).
Resolver/provenance/currentness/SI шли последовательно в одном outer runner,
он завершился exit 0; red/green/full — отдельные outer processes. Нет pipe masking,
`|| true`, suppressed failure, environment/harness/CI edits или waiver.
Full summary OK согласован с raw Python exit 0 **и** outer exit 0. Дополнительно
S2.3 выполнил 1659 parameterized scenarios. Историческое OK/exit 1 расхождение
не воспроизвелось; причина старого случая этим запуском не объявляется установленной.

SHA-256 unfiltered raw logs (вне Git):

| Log | SHA-256 |
| --- | --- |
| red | `4ea7cc257ed9647831c341b5a675ee79eb8c02db78e2de9ae4d58773e2e0f9d9` |
| green | `7bba7c3ab0e83322a1622b567b082369d39509cc9dc71d1b961047df5a8bb772` |
| resolver | `a63606bbc9ef52c3864a27718648d296884010f3a03dc736339ce755c48c44dd` |
| provenance | `0f87b47307cd1c688ec3f0a954b5c307b92e65e8e66ab292d8f920cffc96aa64` |
| currentness | `07e7197c6673bcb4465461c30c5bfa69b76e1637897621e132a12f6544f50f1d` |
| si | `b38e4952dd1daa054cf47180091a7354c82b3143aa98a394debf22520084adf5` |
| full | `161343876c57ad8903e7f15b93273f5f91dede942c20865dca9a217c4fff0cfe` |

После начала final suites source/test bytes не менялись; после full обновлён
только RESULT. Red exit 1 — зарегистрированный ожидаемый провал до fix; все
final suite exits равны 0. Ни один ненулевой статус не выдан за PASS.

## Golden preservation, QA и ограничения

Выполнены exact M/M/A three-file allowlist, Markdown links/fences, AST syntax checks,
`git diff --cached --check` и `git diff --check` (exit 0). Остальные 16 existing SI
source/test files побайтово совпадают с exact base, включая currentness general/
vector tests, старые foundation/records/resolver/provenance literal vectors.
Все 10 currentness vectors прошли в прежнем suite с unchanged hashes/states.
Source remote повторно равен exact base; main read-only наблюдался на
`e1f4efb0fb5ff290bb198349213c004b4667ef0f`. Parent/remote equality и clean worktree
проверяются после publication; final commit SHA и diff/stat сообщаются в handoff.
Vector file SHA-256: `f05f36abc8840dcc2643d86c43275ea9b08cebdfb7324b837a6c64ab26787d1a`.

Tested fixed production SHA-256:
`b0330175bf0e89debe806f9c3a178c56451e723c0a28be48693b3a738a81932c`.
Test file SHA-256 (одинаковый red/green/final):
`0485e3b76c4a49b6d9c437028ebeea9220292dfe20485a818703e6d365aa0117`.

Scope остаётся pure read-only semantic currentness относительно supplied observations,
не execution/identity/rights/truth/approval certificate. API не принимает validated
editorial snapshot: relevant ERef даёт INVALID/REF_MISSING; adapter не создан.
Исторические источники/Run ancestry по-прежнему полностью проверяются как SI audit.
Нет Packet/UI/readiness, operation execution, persistence, protected writes, network,
providers/GPU, новых dependencies или performance claims. Linux tests не Windows
native qualification. F1-D1 owner decision применён без изменения остальных contracts.

Без PR/merge/release/main изменений, SI-E02/RFC/role-map не начинались.
`PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF;
Windows S3.2b BLOCKED_HOST_NOT_PROVIDED. После publication — **STOP для независимой приёмки**.
