# G3.2.0 — фактическая архитектура и contract inventory

**PROPOSAL — OWNER REVIEW REQUIRED.** Дата: 2026-11-17 (Europe/Kyiv). Итог документационного задания: READY_FOR_OWNER_REVIEW; production readiness не заработана.

## 1. Exact identity и метод

| Объект | Commit | Tree |
|---|---|---|
| Approved base и origin/main после fetch | `a28277b4cb68a3db5da52edc598c37ce66314604` | `920713b992046dff1f8fc68e40a05bee2f0bcb29` |
| G3.1 implementation (родитель принятого merge) | `8748ad71a30cc0044920f0051830ccf14d858992` | `920713b992046dff1f8fc68e40a05bee2f0bcb29` |
| G3.0 audit reference, не база | `fbade9e409b3b540afdfd5ff807b4aa60ae368f2` | `39da92547a0b284fc99b58c1efe9d58aacd1f0d5` |
| Deferred PR #11 context, только чтение | `6cfa7b4b535b0171ae2871b7e68e545b48ba332a` | `2850e0977af749569a5d363ffc1f540ffd788f2d` |

Base merge parents: `7166902820731984ceb56d79275a70f83f665b23` и `8748ad71a30cc0044920f0051830ccf14d858992`. До изменений fetch подтвердил exact remote base/tree, checkout чистый, remote docs branch отсутствовала. Создана `docs/g3-2-0-production-gate-contract-discovery` **ровно от base**, без rebase/cherry-pick deferred paths или G3.0 docs.

Выполнено чтение actual base функций, tree entries и pinned historical contracts; source-only материалы прочитаны из investigation archive/Git objects, не добавлены в ветку. Новые PG схемы остаются PROPOSAL и не отменяют approved A1–A14/O1–O10/PD-01–08. Название исторического файла PROPOSAL/APPROVED не заменяет проверку его ограниченного original scope.

## 2. Что существует на base

| Компонент | Фактический интерфейс / поведение | Что отсутствует / запрещённый вывод |
|---|---|---|
| G1 Pure Foundation | SI models/codecs/refs/provenance/currentness, `evaluate_si`, `project_evaluation`; editorial immutable model/graph/package/rights binding, schema2 evidence shape, storage protocol wire | Pure validation не проверяет identity человека/реальные лицензии, не выдаёт production permission, не durable OS storage |
| Evaluation | Полные invocation args; OK/CURRENT с eligibility либо INVALID/STALE с null accepted eligibility/aggregate; detached plain values | CURRENT означает supplied context consistency, не актуальность внешнего мира. Научная истина/rights/пригодность темы не выводятся из score |
| Decision Projection | `project_evaluation(inputs,result,locale)` повторно вызывает evaluator и canonical сравнивает full result; DISPLAYABLE/UNAVAILABLE; private fixed RU/UK explanation | Detached/redacted result нельзя объявить verified. Card не authorisation, не публичный export, не новый ProductionBrief |
| G2 Preview | `preview(data)`, `run(source,output)`; original source_sha256, value input_sha256, private status/evaluation/cards/draft plans; read_plan validation | NOT_ASSESSED, permissions_granted=false; missing inputs не исправляет. Topic metadata не верифицированно связано с SI графом. materials rights reported-only |
| G2 V07 | `_output_path` по компонентам; Windows GetFileAttributesW rejects reparse, POSIX lstat; повторные проверки, private modes где поддержаны, staging/rename | Name-based TOCTOU остаётся; Windows mode bits не NTFS ACL proof; не immutable snapshot/qualified protected writer |
| G3.1 D1 | `topic_to_video.run` только fixed SYNTHETIC_TEST_ONLY permit/scenario/digest; настоящий eval/Projection; generated silence/gradient; две MP4 + локальный manifest | Не вызывает editor_preview. Не общий Production Gate; нет произвольных real inputs. Входной permit публичная константа fixture, не identity grant. D1 output path не защищён V07 |
| First Video | `read_plan` проверяет format; `build` использует supplied local WAV либо optional Silero, generated/local images, core renderer | build принимает вызов независимо от PG/D1; считать его guarded production endpoint нельзя. Наличие optional TTS не license/voice consent |
| FFmpeg renderer | Core project/timeline/media paths/subtitles, CPU libx264/AAC и libass burn-in; subprocess, local tool lookup | Не проверяет editorial/rights approvals, single-use, revocation, executor authenticity или atomic evidence completion |
| Editorial approvals/rights | ApprovalRecord хранит actor/time/decision; ApprovalAuthorityEvidence задаёт структурные principal/policy/session fields; HANDOFF declares NO_RENDER_OR_EXPORT_AUTHORIZATION | Валидная SID/UID строка и signature-shaped поля не OS authentication; RightsBinding.CONFIRMED только совпадение material digest |
| Storage S3 | На base есть storage_protocol_v1 и schema2_model. В deferred source — pure transaction model и portable Windows LAB | В base нет deferred native service/writer; даже source PURE_ONLY не даёт SID/ACL/IPC/DPAPI/NTFS durability. S3.2b host readiness исторически BLOCKED_HOST_NOT_PROVIDED |

### Существенный binding gap G2

Export `evaluation.json` сохраняет `diagnostics=[{code:...}]`, в то время как live Projection получает full in-memory result с field_path/input_ref/message и повторно проверяет PD-01 association. Это intentional privacy boundary, не defect для исправления в G3.2.0. PG-01 collector в будущем не сможет использовать redacted JSON как full authority input. Нужны exact original editor input, pinned code/runtime, повторный full evaluator + Projection и новый immutable binding; unavailable input/runtime/context → deny. No guessing missing diagnostics или переупаковки export в approved full result.

G2 input_sha256 вычисляет canonical JSON values по G2 wire, source_sha256 — raw bounded source bytes; D1 digest связывает другую domain-specific fixture; PG-C14N proposal — отдельный namespace. Эти хеши не взаимозаменяемы и не аутентифицируют автора.

## 3. Три существующих пути и предлагаемая цепочка

```mermaid
flowchart LR
    T[Topic + explicit evidence] --> E[G1 Evaluation]
    E --> P[G1 private Projection]
    P --> V[G2 Preview artifacts]
    V -. PG-01 PROPOSAL .-> S[Snapshot candidate]
    S -. PG-02 PROPOSAL .-> H[Human review]
    H -. PG-03 PROPOSAL .-> A[Asset rights review]
    A -. PG-04 PROPOSAL .-> Q[Authorization candidate]
    Q -. separate qualified admission BLOCKED .-> R[Render]
    R -. PG-05 PROPOSAL .-> X[Execution evidence]
```

Стрелка Projection→Preview означает внутренний вызов Projection самим Preview; отдельного consumer произвольной detached card нет. Исходные данные темы/источников/ratings/findings задаёт редактор, discovery/research не выполняются автоматически. D1 — параллельный существующий synthetic-only test path Eval→Projection→fixed permit→first_video→manifest, не пунктирный production bridge.

| Переход | Implemented | Evidence / gap |
|---|---|---|
| Topic → Evaluation | Только явные SI inputs и ручные metadata | Нет сбора реальных источников/автоматического фактчекинга или доказанной film-worthiness |
| Evaluation → Projection | Да, pinned pure API и full-result re-verification | Не scientific/human/rights authority |
| Projection → Editor Preview | Да, внутри G2 adapter | Export privacy уменьшает diagnostics; immutable protected snapshot отсутствует |
| Preview → Human Approval | Нет PG01/PG02 adapter/provider | Legacy fields/declarations недостаточны для effective authenticated approval |
| Human Approval → Rights Check | Нет PG bridge; base rights_binding pure | Нужны actual terms/usage/assets и qualified reviewer |
| Rights → Render Authorization | Нет | Нет operational issuer/policy/revocation/single-use ledger |
| Authorization → Render | Нет guarded production executor | first_video — техническая утилита, обход которой не запрещён существующим контрактом |
| Render → Evidence | D1 local technical manifest; PG05 не реализован | Нет all-output SHA256/custody/authentic completion/atomic trusted index |

## 4. Проверенные Git entries

Base references ниже присутствуют в approved tree; source-only references ниже **отсутствуют** в base и не копировались. Все SHA — Git blob SHA-1, mode100644.

| Категория | Exact path | Blob SHA-1 | Pinned view |
|---|---|---|---|
| BASE | `scripts/editor_preview.py` | `5204fbfcfa5f84681d80ff23772275381d391fa1` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/a28277b4cb68a3db5da52edc598c37ce66314604/scripts/editor_preview.py) |
| BASE | `tests/test_editor_preview.py` | `5b2861834f86edd23965b9e18cd3203ab43f9827` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/a28277b4cb68a3db5da52edc598c37ce66314604/tests/test_editor_preview.py) |
| BASE | `scripts/topic_to_video.py` | `488cd3dff1d755e6df68f1e4eebf9e094a30526c` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/a28277b4cb68a3db5da52edc598c37ce66314604/scripts/topic_to_video.py) |
| BASE | `tests/test_topic_to_video_d1.py` | `8859199dec4bac75dba7ded38e4e6c8fa4ad550d` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/a28277b4cb68a3db5da52edc598c37ce66314604/tests/test_topic_to_video_d1.py) |
| BASE | `docs/tasks/SI_PRODUCT_02_2_D1_SYNTHETIC_RENDER_PERMIT.md` | `928db7f952c748ab7206427b0a995899b8e46439` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/a28277b4cb68a3db5da52edc598c37ce66314604/docs/tasks/SI_PRODUCT_02_2_D1_SYNTHETIC_RENDER_PERMIT.md) |
| BASE | `scripts/first_video.py` | `b0f60d36bbf16e7cabc609a8393e5e4b9bb0f2e1` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/a28277b4cb68a3db5da52edc598c37ce66314604/scripts/first_video.py) |
| BASE | `core/mp4_render.py` | `860be5c2684cfd189ebef0be414b19b386d1ea2f` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/a28277b4cb68a3db5da52edc598c37ce66314604/core/mp4_render.py) |
| BASE | `core/project_schema.py` | `ef778c579585508c1ee6288cc3bb43723a6fe78f` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/a28277b4cb68a3db5da52edc598c37ce66314604/core/project_schema.py) |
| BASE | `core/media_paths.py` | `61988d73ba05bf3bd96ed59e158bfe98fbe0c218` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/a28277b4cb68a3db5da52edc598c37ce66314604/core/media_paths.py) |
| BASE | `core/subtitles.py` | `1415a74808aabc839dae7f4dcc02094e7302f647` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/a28277b4cb68a3db5da52edc598c37ce66314604/core/subtitles.py) |
| BASE | `story_intelligence/evaluate_v1.py` | `cd9e6c461d7d298ebf03b0c5f5a9e01bbfeab43f` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/a28277b4cb68a3db5da52edc598c37ce66314604/story_intelligence/evaluate_v1.py) |
| BASE | `story_intelligence/decision_projection_v1.py` | `1fbf216d6fd42f6be10228608270a81a50cb09b0` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/a28277b4cb68a3db5da52edc598c37ce66314604/story_intelligence/decision_projection_v1.py) |
| BASE | `story_intelligence/codec_v1.py` | `0adc80d4616d4dfee8f10fe9992055b2bf1b7599` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/a28277b4cb68a3db5da52edc598c37ce66314604/story_intelligence/codec_v1.py) |
| BASE | `editorial/model.py` | `3f74177913f3b70dd55ee38e1ac9e35e7b73d4db` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/a28277b4cb68a3db5da52edc598c37ce66314604/editorial/model.py) |
| BASE | `editorial/package.py` | `1e2adff593b541b9161fd891232669dbc5d3c4a4` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/a28277b4cb68a3db5da52edc598c37ce66314604/editorial/package.py) |
| BASE | `editorial/rights_binding.py` | `1388d69f8d0e29092dd856fbab3591a973caa211` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/a28277b4cb68a3db5da52edc598c37ce66314604/editorial/rights_binding.py) |
| BASE | `editorial/schema2_model.py` | `870980d22ffa377d424402c97ccc5ff9749c839c` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/a28277b4cb68a3db5da52edc598c37ce66314604/editorial/schema2_model.py) |
| BASE | `editorial/storage_protocol_v1.py` | `5484f5f5e7228f6a36bde7e2ce71fcf5feda1598` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/a28277b4cb68a3db5da52edc598c37ce66314604/editorial/storage_protocol_v1.py) |
| BASE | `.github/workflows/tests.yml` | `7ba7beb4a9f5d2e30104b65acf64a7104b5cec7e` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/a28277b4cb68a3db5da52edc598c37ce66314604/.github/workflows/tests.yml) |
| SOURCE ONLY / reference | `docs/tasks/E01_3_4_APPROVED_CONTRACT.md` | `70b6281999d4cb0cea889530197d14babf1b5547` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/6cfa7b4b535b0171ae2871b7e68e545b48ba332a/docs/tasks/E01_3_4_APPROVED_CONTRACT.md) |
| SOURCE ONLY / reference | `docs/tasks/E01_3_7_3_APPROVED_CONTRACT.md` | `279fb004ea2caa3965f550ecbda9d90e5b5eae92` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/6cfa7b4b535b0171ae2871b7e68e545b48ba332a/docs/tasks/E01_3_7_3_APPROVED_CONTRACT.md) |
| SOURCE ONLY / reference | `docs/tasks/E01_3_8_1_APPROVED_CONTRACT.md` | `6e5dcbedbf6b7498534e5c90032c374d61cf3b96` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/6cfa7b4b535b0171ae2871b7e68e545b48ba332a/docs/tasks/E01_3_8_1_APPROVED_CONTRACT.md) |
| SOURCE ONLY / reference | `docs/tasks/STORY_INTELLIGENCE_SI_PRODUCT_01_0_OWNER_DECISIONS.md` | `e04b8c19cc2a74b7f986bfdb3f21eaf5865493b2` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/6cfa7b4b535b0171ae2871b7e68e545b48ba332a/docs/tasks/STORY_INTELLIGENCE_SI_PRODUCT_01_0_OWNER_DECISIONS.md) |
| SOURCE ONLY / reference | `docs/tasks/E01_3_9_4_S3_2A_R1_INDEPENDENT_ACCEPTANCE.md` | `fe59e885972ad3e86234cfae5038cd7d70c2443c` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/6cfa7b4b535b0171ae2871b7e68e545b48ba332a/docs/tasks/E01_3_9_4_S3_2A_R1_INDEPENDENT_ACCEPTANCE.md) |
| SOURCE ONLY / reference | `docs/tasks/E01_3_9_4_S3_2B_PHASE0_HOST_READINESS.md` | `bbad7f4f1c2a30935eec681b0d17e790c3835d8b` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/6cfa7b4b535b0171ae2871b7e68e545b48ba332a/docs/tasks/E01_3_9_4_S3_2B_PHASE0_HOST_READINESS.md) |
| SOURCE ONLY / reference | `docs/tasks/E01_3_9_4_S3_2_OWNER_LAB_DECISIONS.md` | `53bd03ae2a7145802329136cd866f0f59cd88c94` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/6cfa7b4b535b0171ae2871b7e68e545b48ba332a/docs/tasks/E01_3_9_4_S3_2_OWNER_LAB_DECISIONS.md) |
| SOURCE ONLY / reference | `editorial/approval_attestation.py` | `1db1f3d32e93a64c1520978fcdb4859c9c59d040` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/6cfa7b4b535b0171ae2871b7e68e545b48ba332a/editorial/approval_attestation.py) |
| SOURCE ONLY / reference | `editorial/schema2_integrity.py` | `237bd86ff229eed14a850aa0a8e1be2483b0bf6b` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/6cfa7b4b535b0171ae2871b7e68e545b48ba332a/editorial/schema2_integrity.py) |
| SOURCE ONLY / reference | `editorial/storage_transaction_model_v1.py` | `861977f493822f3ced5526c4c4e49c73f394dc32` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/6cfa7b4b535b0171ae2871b7e68e545b48ba332a/editorial/storage_transaction_model_v1.py) |
| SOURCE ONLY / reference | `editorial/windows_lab/dispatcher.py` | `940614d8e55a5a5c2cdec49a309d58133fe58116` | [read](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/6cfa7b4b535b0171ae2871b7e68e545b48ba332a/editorial/windows_lab/dispatcher.py) |

## 5. Evidence scope и ограничения исследования

G3.2.0 выполняет read-only Git/code/docs inspection и создаёт пять Markdown. **Новых unit/full tests, render, Windows/native/rights verification или CI runs для PG нет; NOT_RUN.** Ни одного PG implementation/validator/provider не существует, все оракулы — требования будущего этапа.

Историческая проверка G3.1 на совпадающем tree: [PR #14 packet](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/pull/14), [CI44046622594](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/actions/runs/44046622594): Linux CPython3.10.22/3.13.18, full unittest714 skip1, pytest726 passed/skip1, exit0; D1 positive render реально выполнялся. Это scoped synthetic evidence предыдущего этапа, **не новый PG PASS**, не Windows qualification. Default source permit Markdown hard-break whitespace warning и внешняя cleanup assertion описаны в том packet и не исправлялись здесь.

Historic approved authority/package/schema contracts сохранены в их original scope: A14 HANDOFF editorial-only; optional signature без trusted registry не аутентичность; missing/mismatched protected anchor blocks effective approval. SOURCE ONLY pure models/acceptance не свидетельствуют ready native S3. Никаких host/admin/SCM/ACL/DPAPI или production data operations сейчас.

## 6. Блокировки и готовность

Общий production path BLOCKED до owner выбора конкретных PG schemas, identity/authority/revocation/time providers, qualified issuer/executor и immutable state/content/evidence boundary. Current first_video не обеспечивает неотменяемое enforcement. Real legal/scientific/editorial evidence и полномочия не предоставлены; Windows/NTFS/TOCTOU protection не квалифицированы. Можно review этот discovery без запуска production.

Пять документов образуют единый PROPOSAL: [контракты](G3_2_0_PRODUCTION_GATE_CONTRACT_PROPOSAL.md), [security/rights](G3_2_0_SECURITY_AND_RIGHTS_MATRIX.md), [оракулы/gates](G3_2_0_TEST_ORACLES_AND_GATES.md), [owner choices](G3_2_0_OWNER_DECISIONS.md). Новые решения не отменяют G1/G2/G3.1 или существующие schemas/enums. **STOP после docs commit/handoff; implementation только отдельным решением.**
