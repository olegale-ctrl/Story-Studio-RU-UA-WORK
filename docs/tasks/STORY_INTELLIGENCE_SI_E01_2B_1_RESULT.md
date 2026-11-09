# SI-E01.2b.1 — Pure SIRef Resolver & Canonical Closure

Дата: 2026-11-09. Реализовано в bounded pure in-memory scope; независимая приёмка
этого результата ещё требуется.

- Base: `73c4e519033d27e7ca079570a563d340d1a2f61e`.
- Source branch: `docs/story-intelligence-si-e01-2a-f1-independent-acceptance`.
- Feature branch: `feat/story-intelligence-si-e01-2b-1-pure-resolver-closure`.
- Source remote HEAD проверен до создания feature branch и совпал с exact base.
- Final commit/remote SHA сообщается после publication в handoff: self-referential
  hash нельзя буквально включить в содержимое того же коммита. Проверяются parent,
  `git rev-parse HEAD`, remote equality и clean worktree.

## Основание и точный scope

Прочитаны [полное bounded задание](STORY_INTELLIGENCE_SI_E01_2B_1_CODEX_TASK.md),
[независимая приёмка SI-E01.2a/F1](STORY_INTELLIGENCE_SI_E01_2A_RESUME_F1_INDEPENDENT_ACCEPTANCE.md),
[original](STORY_INTELLIGENCE_V1_SPEC_PROPOSAL.md),
[R1](STORY_INTELLIGENCE_V1_R1_CONTRACT_CLARIFICATIONS.md) §§1–2/4.2/5,
[R1a](STORY_INTELLIGENCE_V1_R1A_RECORD_OPERATION_CLARIFICATIONS.md),
[R1b](STORY_INTELLIGENCE_V1_R1B_REVIEWPACKET_FIELD_PATH_CLARIFICATION.md),
[его approval](STORY_INTELLIGENCE_V1_R1B_OWNER_APPROVAL_2026_11_09.md),
[SI-D01–D10 approval](STORY_INTELLIGENCE_V1_OWNER_APPROVAL_2026_11_09.md) и accepted
codec/model/records/test sources. Приоритет original → precise R1 → precise R1a →
precise R1b сохранён. Никаких wire/operation contract changes нет.

Созданы только четыре новых файла:

| Файл | Назначение |
|---|---|
| `story_intelligence/resolver_v1.py` | Exact SIRef resolution, iterative typed audit DAG и Run snapshot Closure |
| `tests/test_story_intelligence_resolver_v1.py` | Genuine graphs, explicit-edge oracle и fail-closed cases |
| `tests/test_story_intelligence_resolver_vectors_v1.py` | Семь literal canonical graph manifests/bytes/SHA |
| `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_1_RESULT.md` | Этот отчёт |

Все файлы new/A-only; optional CONTRACT_GAPS не создавался: новых blocking gaps
не найдено. Существующие source/tests/contracts/acceptance/results, WORKLOG,
config/dependencies/CI, editorial/storage и main не изменены.

## API и выбранные pure Python правила

`resolve_si_closure(records, roots) -> list[SIRef]` и
`resolve_si_record(records, expected_ref) -> detached complete record`.
Аргументы records/roots — exact plain finite lists; record/ref inputs проверяются
принятыми validators. Это локальный Python API, не новый wire bundle/DTO.

Каждая переданная complete record проходит validate_si_record и si_record_ref;
index строится по `(type,id,revision)`, digest вычисляется из actual canonical bytes.
Разные canonical bytes/digest одной identity → REF_HASH_MISMATCH, без выбора по
позиции. Сравниваются сами C(record) bytes, а не только SHA; identical duplicates
определяются по canonical bytes, не Python key insertion order. Identical
canonical duplicates → TYPE (выбран строгий noncanonical-bundle отказ).
Повторяющиеся exact roots разрешены: Closure по контракту set-valued.
Records list не обязан быть sorted; результат не зависит от его порядка.

Все supplied records валидируются структурно, даже unrelated. Но лишь root-reachable
records/edges и их snapshots получают graph verification. Unrelated valid record
может иметь unresolved refs, не возвращается как часть Closure и не становится
доверенной registry entry. Невалидный unrelated record/identity conflict отклоняет bundle.
Empty records/roots возвращают []; empty roots с valid records также дают [].

Оба API проверяют полный достижимый audit graph; resolve_si_record — не обходной
путь мимо dependencies/snapshot validation. Нет implicit latest, version upgrade,
external fetch, постоянного registry или mutable cache. При missing exact identity
→ REF_MISSING; если для id/revision поставлены только другие types → REF_TYPE_MISMATCH;
неверный expected digest → REF_HASH_MISMATCH. Paths привязаны к $.roots[i],
$.expected_ref и $.records[i] с исходным typed field path.

Возвращаемые refs/records — detached copies. Caller input не меняется, arrays не
пересортировываются и не обрезаются. Канонический manifest — sorted unique exact
SIRefs `(type,id,revision,sha256)` из verified actual bytes, включая сами roots.
Manifest list не кодируется production API как single-record JSON, поэтому
single-record 1 MB codec limit не превращается в скрытый bundle/closure cap.

## Typed edge extraction и DAG

H.previous, H.origin.run_ref, H.input_refs перечисляются явно. Payload обходится
по принятой `_SCHEMAS` vocabulary из records_v1 **read-only**: object/list/nullable/
Known<T>/typed-ref tags. Поддерживаются nested PortfolioEntry/Chapter/ContextSnapshot/
Rating/SelectionScope/FieldGrant/DisplayItem/Omission/BriefReviewState refs.
Unknown future schema tag даёт VERSION_UNSUPPORTED, не silent edge omission.

Не используется dict-shape heuristic или parsing free-form text. Hash strings,
locators, displayed text и Known<Text> с JSON-подобной строкой не становятся edges.
ERefs валидируются accepted record validators локально, но не следуются как SIRefs.
Без editorial snapshot adapter **их actual bytes/material hash не проверены**.
Production module не импортирует editorial/storage runtime.

Обход итеративный (explicit stack/colors), без Python graph recursion. Для негативных
cycle cases используется identity-DAG preflight: root hashes проверяются сначала;
на достижимых существующих identities cycle отклоняется DEPENDENCY_CYCLE до edge-hash
comparison. После успешного DAG обхода **каждый** достижимый edge hash обязан совпасть
с computed record ref, иначе результата нет. Missing/type errors также fail closed.

Это явный local diagnostic priority, не новая SI wire семантика. Настоящий positive
content-addressed cycle требовал бы SHA fixed points; negative cycle fixtures поэтому
содержат синтаксически valid, намеренно неправильные edge hash claims при реальном
root hash. Они не выдаются за hash-consistent positive graphs. Тесты direct/indirect
cycle и Run→own output→Run проверяют именно отказ, без mocked hash functions.

## RunRecord.input_snapshot

Для каждого достижимого Run recomputed roots:
`semantic_input_refs + context_snapshot.active_input_refs + context_snapshot.selection_head_refs`.
На уже verified DAG вычисляется их transitive Closure и exact canonical manifest.
Frozen input_snapshot должен **целиком** равняться этому manifest, не subset.
H.input_refs equality/canonical order продолжают проверяться accepted local validator.
Omitted transitive input / extraneous ref → PROVENANCE_MISMATCH по
`$.records[i].payload.input_snapshot`; неправильный manifest order → existing TYPE.
Self/own-output dependency с обратной ссылкой на Run даёт DEPENDENCY_CYCLE.

Audit Closure включает previous/origin/history и captured heads. Это не semantic
currentness: старые revisions не объявляются active domain inputs. Не выводится,
действительно ли method породил output или верны ли semantic roots операции —
stage/output/provenance/operation certification остаётся для SI-E01.2b.2.
Packet.source_closure_refs следуются как typed edges; их export-scope equality с
полной Closure Brief/context не сертифицируется отдельным Packet exporter. Это не
подмена специальной проверки export/privacy общим graph traversal.

## Genuine graphs и независимые literal vectors

В fixtures complete-record hashes рассчитаны **только stdlib JSON/hashlib**,
без SI production hash functions. Records добавляются topologically с реальными
refs на уже созданные bytes. Независимый oracle хранит вручную объявленные edges,
а не использует production schema extractor или resolver.

Положительные графы включают manual input; Evidence/Claim/Source dependencies;
Discovery Run→StoryIdea; Known portfolio; nested Rating/Chapter refs; Source revisions
1/2/3 с exact previous и REVISION runs; Creative K1/K2/K3 с одним исходным CREATIVE
run и разными REVISION runs; Brief/Selection/Packet с полным source manifest и export
Run, не ссылающимся на свой будущий Packet. Эти fixtures не являются исполнением
операций, доказательством human review/rights или опубликованными материалами.

**Семь literal vectors:** manual, multilevel, discovery_run, run_snapshot, revision,
creative_dual_runs, packet. Каждый содержит буквальные exact root, expected Closure
SIRef list, C(manifest) bytes и SHA-256. Run query включает сам Run и его ancestors;
его input_snapshot отдельно проверяется как Closure inputs без самого Run/outputs.
Expected values получены independent explicit-edge oracle/std JSON/hashlib и все
семь SHA независимо сверены OpenSSL. В тестовых definitions они hardcoded; expected
не вычисляется из resolver или SI hash method. Generator/logs вне Git, OpenSSL не
runtime/test dependency. Production API не имеет serializer для всего bundle.

Негативные случаи: missing root/previous/origin/nested Known/context record,
wrong SHA/tampered bytes, conflicting/identical duplicates, direct/indirect cycles,
Run self/own output, snapshot omission/extra/order, ERef-as-SIRef, no-latest fallback,
непревращение strings в edges, malformed interfaces, invalid unrelated record.
Проверены input immutability и detached outputs; nested typed path coverage имеет
отдельный assertion table. Цепочка **1100 records** с aggregate bytes >1_000_000
прошла без graph recursion и нового count/aggregate-byte cap. Это не latency benchmark.
Лимиты 1 MB/100000 codepoints/32 containers применяются к каждой record прежними
validators. Никакой 1000-record/16 MiB bundle cap не вводился и dependencies не truncating.

## Фактические тесты и проверки

Среда: Linux x86_64 / Python 3.12.14, проектный `.venv/bin/python`.
Предыдущий reported baseline: 66 targeted / 908 full; новые counts не предполагаются
из арифметики без фактического запуска.

```bash
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_resolver_v1.py' -v
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v
.venv/bin/python -m unittest discover -s tests -v
```

Первоначальный resolver-only: **16 OK**, 3.482 s, exit0; initial targeted:
**84 OK**, 5.378 s, exit0. Затем добавлен defensive canonical-byte duplicate case:
при подменённом только в тесте digest provider два разных C(record) всё равно
отклоняются REF_HASH_MISMATCH. Реальные SHA этих records различны; тест не заявляет
реальную SHA collision и не используется для positive graph vectors/cycle cases.
Целевой окончательный: **85 OK**, 5.593 s, exit0: прежние 66 + 19 новых methods
(17 graph + 2 literal-vector methods). Семь literal manifests/bytes/hashes совпали.
Предварительный full discovery прерван SIGINT (exit130) перед этой последней правкой;
он не объявляется PASS. Окончательный полный run запущен заново после правки.
Полный окончательный запуск: **927 OK**, 892.098 s, exit0; failures=0,
errors=0, skipped=0, expectedFailures=0. Это прежние 908 + 19 новых methods.
Все existing S1/S2/D-01/LAB regressions прошли; S2.3 дополнительно сообщил 1659
параметризованных сценариев (не дополнительные unittest methods).
`test_sprint23_2.Sprint232Tests.test_env_override` прошёл на Linux; baseline ошибок
окружения не обнаружено. No native Windows/CI qualification claimed.

Accepted codec/model/records и прежние tests сопоставлены с frozen commits:
14 foundation vectors/исходники @ `61886670fe6d0434df62f6346457f5812f520766`,
18+3 record/value vectors @ `f19fa33685f05df632222dbcd84abcaca8258547`, F1 records/tests
@ `557c1fafac9a8bccd0421164436aa17886b82a77` — byte-identical. Проверяются syntax,
local Markdown links/fences, git diff --check, exact new-file allowlist и base/source
remote. Повторный audit семи literal manifests/std JSON/hashlib/OpenSSL прошёл без
production imports. Production imports ограничены copy и accepted SI modules.
Post-push parent/remote SHA equality и clean worktree проверяются в handoff.
Итоговый diff: **4 new/A-only файла, 803 additions, 0 deletions**.

## Ограничения и STOP

Только pure read-only supplied-bundle SI graph. Никаких workspace/disk/network/
Context7/provider/clock/UUID/key generation, operation execution/dispatcher/replay,
currentness/eligibility engine, actual source field/index/value/privacy review,
ERef material verification, PII detection, trusted rights/identity, persistence,
FFmpeg/renderer/production export или Windows VM. No new dependencies.
SI-F01 worst-case 1 MB integer latency не измерялась; digit cap не вводился.
Ресурсы процесса остаются конечными; memory/time для произвольно большого bundle
не обещаются, но искусственного cap или partial success API не добавляет.

S1/S2/S3/authority не менялись; PUBLISH_REVISION DISABLED, partial COMMIT reconstruction
OFF, S3.2b BLOCKED_HOST_NOT_PROVIDED. Linux tests не являются native Windows qualification.
После publication — STOP для независимой приёмки. SI-E01.2b.2, SI-E02 и persistence/
privacy/export требуют отдельных owner gates. PR/merge/release/main не выполнялись.
