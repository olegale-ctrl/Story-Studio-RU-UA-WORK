# MVP-08B.4-DQ-00-RESOLVE-01 — Final Handoff

**READY_FOR_INDEPENDENT_CONTRACT_RE_REVIEW.** Режим DOCS_ONLY / CONTRACT_RESOLUTION, 2026-11-20 (Europe/Kiev). Все native technical changes — PROPOSAL / NOT_APPROVED, implementation не разрешена.

## Exact source / publication

Repository: olegale-ctrl/Story-Studio-RU-UA-WORK.
Branch: `docs/mvp-08b-4-dq-00-resolve-01`.
Base commit: `0b61892fc4156251b19e5c529c71a6ce783b838d`.
Base tree: `7119aa23c700e484cb5c69e24063be67ddef6c6b`.
Исходный HEAD/tree совпал, worktree был чистым. Final commit/tree, full patch, SHA-256/Git blobs пяти changed files и проверка private-index reconstruction — во внешнем publication-manifest.json и итоговом ответе. Self hash в создающем его файле не подставляется.

## Точный разрешённый diff

Только пять существующих Markdown:

1. [DURABLE_STORAGE_CONTRACT_PROPOSAL.md](DURABLE_STORAGE_CONTRACT_PROPOSAL.md)
2. [NATIVE_EVIDENCE_CONTRACT_PROPOSAL.md](NATIVE_EVIDENCE_CONTRACT_PROPOSAL.md)
3. [FAULT_INJECTION_MATRIX.md](FAULT_INJECTION_MATRIX.md)
4. [DQ_01_IMPLEMENTATION_TASK.md](DQ_01_IMPLEMENTATION_TASK.md)
5. [FINAL_HANDOFF.md](FINAL_HANDOFF.md)

Новых Git files нет. OWNER_APPROVAL, SQLITE_QUALIFICATION_PROFILE, TEST_ROOT_SECURITY_CONTRACT, OWNER_DECISION_PACKAGE, Python/tests/CI/dependencies и G1–G6 не изменены. OD4-01–OD4-07 остаются OWNER_APPROVED_CONTRACT_ONLY. Уточнённый native evidence/data draft имеет version 2 в силу version policy; SQLite layout/schema/user_version остаётся 1. Old native-v1 wording в неизменённом OWNER_DECISION_PACKAGE — superseded unapproved technical recommendation; новые CP permissions по-прежнему отсутствуют.

## Mapping замечаний

| Замечание | Resolution proposal | Canonical/check materials |
|---|---|---|
| DQ-F01 | Conjunctive custody/ticket/continuous coordinator/identity/complete A absence; prepared cache != apply. Whole-app recovery не квалифицируется; missing evidence => UNKNOWN/HOLD | F01-P01–P03/N01–N06; P0/C0/C1, TP/TA, PE/AP/AP0, negative close ACKN1/ACKN2, partial/identity specimens |
| DQ-F02 | Pre-R G / exact Ack G+1 / post-R G+1; separate A-vs-R outcome; same-M/exact-Ack R retry only after qualified R absence; no pre/post hash cycle | F02-P01–P07/N01–N07, SA/CP/ACK3/TR/C3/SR/SRA, corrupt/foreign/generation/head negatives; DAG check and deliberately cyclic abstract graph rejection |
| DQ-F03 | Observe call, ACK, software kill, unavailable internal VFS/fsync and power loss separately; only COMMIT_RACE_WINDOW coverage, missing checkpoint not PASS | FI-01–FI-22 retained; FI-07 and CW-01–CW-05 exact oracles/STOP; no native execution |

## Что вычислено и что не проверялось

Native proposal содержит **58 canonical entries (57 distinct preimages)** с byte lengths/SHA-256 и **23 nonhashable DOC.ORACLE cases** с точными input refs/generations/outcomes/barrier/allowed-next. Profile values DOCUMENT_FIXTURE и SQLite 3.35.0 — синтетические константы, не измерения. Альтернативные branches не выдаются за одну физическую DB history. Source literals перечисляют negative specimens, которые могут hash/shape-валидироваться, но семантически отвергаются.

Внешний review packet: build_vectors.py, check_vectors.py и их outputs; canonical-vectors.json (text/UTF-8 hex/length/hash/full refs), data-payloads.json, oracle-cases.json; source-manifest.json; documentation-checks.json; findings-map.json; full changes.patch/publication-manifest и safe verifier.

Локальный верификатор проверяет document arithmetic, closed field sets/payload shapes, actual typed ref/byte binding, graph acyclicity и declared generation/oracle consistency. Это **не Python implementation native store/adapter**, не SQLite/test-process execution и **не независимая проверка вычисленных векторов**. Ни один literal Checks=true не выдается за измеренный native факт. Native qualification/test cases NOT_RUN.

Проверки Markdown/links, FI-01–FI-22 completeness, future allowlist consistency, unchanged G1–G6/source blobs, diff/SHAs и main state фиксируются внешними материалами. Main читается read-only; update/merge не выполняются.

## Review / STOP

Независимый reviewer должен проверить mathematical preimages/digests и semantic premises каждого case отдельно от работы локального скрипта. Особое внимание: missing ticket нельзя восстановить каталогом; отсутствие marker не отсутствие A; negative unprepared closure не доказывает committed P; known A не понижается из-за unknown R; Ack не пересчитывается от fresh Snapshot; post-R root не попадает в pre-R hash chain; race-window не internal VFS/power loss.

Не выявлено необходимости менять ранее утверждённые G1–G6/OD4; native proposal исправляется до их отдельной реализации. Самостоятельно закрытой независимой приёмкой DQ-F01/F02/F03 этот report не является. Windows/native storage/engine/path qualification остаются NOT_RUN; owner root/limits/process/write/allowlist/programming grants не выданы.

**STOP после публикации.** Ожидать независимой контрактной re-review и отдельного решения владельца. Никаких SQLite execution/DB creation/native kill/process tests/Python implementation, merge/main update, provider/render/production или автоматического перехода к DQ-01.
