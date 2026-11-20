# DQ-00-C-A01 — Contract Resolution / Final Handoff

**READY_FOR_INDEPENDENT_C_A01_REVIEW.** DOCS_ONLY / CONTRACT_FIX.
Дата: 2026-11-20 (Europe/Kiev). Это подготовленное исправление для независимой
приёмки, не самостоятельно объявленная независимая приёмка C-A01.

## Точные исходные ревизии

Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
Branch: `docs/mvp-08b-4-dq00-c-a01-resolution`.
Contract base commit: `c15ac152258586be1ed1b57f205830edfffc9ae1`.
Contract base tree: `19192e46ad0f3b3cc9d9bc9809d3896e1e13e639`.
Finding source commit: `6190dc50bd13bbb34e0adcc57ddc219a4c5cd44d`.
Finding source tree: `68554f3fc4f4ef560a0ce3502b58b820d5c12f5d`.
Обе пары commit/tree проверены по Git objects. Создан отдельный чистый worktree
от exact contract base; feature branch не checkout/reset/merge-илась.

Итоговые commit/tree и blob SHA этого handoff указаны в публикационном ответе:
файл не содержит собственного self hash. Проверка: `git rev-parse HEAD HEAD^{tree}`.
Точный полный diff:
`git diff --binary c15ac152258586be1ed1b57f205830edfffc9ae1 HEAD`.

## C-A01 и минимальное исправление

Finding: положительные F01-P03/F02-P07 ожидали закрытый отрицательный исход A,
но explicit inputs/typed closure содержали ticket_R без исходного ticket,
канонический hash которого требовал AbsenceProof. `ticket_retained=true`
не определял обязательные bytes. Прежняя неоднозначность описана в finding
source, `docs/tasks/MVP_08B_4_DQ_01/RESULT.md`.

В [NATIVE_EVIDENCE_CONTRACT_PROPOSAL.md](NATIVE_EVIDENCE_CONTRACT_PROPOSAL.md):

- В F01-P03 добавлен только `inputs.original_ticket` — typed ref на V-TP.
- В F02-P07 добавлен только `inputs.original_ticket` — typed ref на V-TA.
- В разделе 9 уточнён строго case-local input set. Catalogue resolver
  обслуживает только явные typed refs и их closure; отсутствующий input
  нельзя восстановить global lookup, поиском по UUID/M или одним Digest.
- Для qualified absence обязательны фактические canonical bytes исходного
  ticket, exact typed identity/hash/closure и binding/M/исходный контекст.
  Флаг `ticket_retained=true` сам по себе не является доказательством.
- Ticket_R не заменяет original ticket. Добавленный input не подтверждает
  custody/непрерывность coordinator и не отменяет остальные native checks.

| Case | Original ticket ref (kind DQ.LAB.OperationTicket, version 2, scope DQ_PROCESS_KILL_LAB_ONLY) | Исходная phase | Case-local closure |
|---|---|---|---|
| F01-P03 | 07b38b65c665b6348837c7826110fa05e8bd08bf6b441508fc9648c0dae14831 (V-TP) | P | TP присутствует; 20 record nodes |
| F02-P07 | 4c0e03133930623d16d0f40ca977e13ffc9d46be9599b82a5227a8aaad3af14a (V-TA) | A | TA присутствует; 20 record nodes |

Для обоих H(original_ticket) точно совпадает с AbsenceProof.ticket_sha256;
binding и mutation_ref совпадают с proof и ticket_R. Существующие ticket_R
refs, все остальные inputs, facts и expected outcomes сохранены.

## Фактически выполненные документальные проверки

In-memory verifier запущен через `python -B` с
`PYTHONDONTWRITEBYTECODE=1`; Python **3.12.14**, exit code **0**. Читались pinned
Git blobs и два разрешённых Markdown; отдельные verifier/evidence/temp files
не создавались. Старый внешний document verifier и Stage A implementation
не запускались. Алгоритм и raw stdout находятся в execution-tool records;
ниже перечислены проверенные assertions, а не native test результаты.

| Проверка | Фактический результат |
|---|---|
| 58 canonical entries | До/после совпадают точные raw UTF-8 bytes, заявленные lengths/SHA-256; повторно вычисленные lengths/hash совпадают |
| 57 distinct preimages | Сохранены; HT/HC остаются alias одинаковых bytes |
| Canonical encoding | Повторная C(record) совпадает с literal bytes; никаких новых preimages |
| 23 DOC.ORACLE cases | IDs/order/структуры/facts/expected/outcomes совпали с base после удаления только двух новых inputs.original_ticket |
| Typed refs и decoded payload refs | Exact kind/version/scope/hash resolution; исходный record DAG: 57 nodes, 230 edges, max depth 14 |
| Циклы | Не обнаружены; новые nonhashable case inputs лишь выбирают существующие TP/TA, не меняют record DAG |
| Два positive ticket prerequisites | Original ticket bytes доступны локально, exact hash/binding/M совпадают; ticket_R остаётся phase R |
| F01-N01/F01-N02 | Ticket отсутствует в local closure; UNKNOWN, barrier=true, uncertainty_hold=true сохранены; lookup из соседних cases не выполняется |
| Дополнительные in-memory negatives | Удаление original_ticket при true flag, false retention, false custody, подмена original_ticket на ticket_R не проходят documentary ticket prerequisite |
| Native version / physical schema | DQ.LAB version 2, RootAnchor/Profile.schema_version 1, Config.user_version 1 — без изменений |
| Allowlist / Git / Markdown | Только два существующих Markdown, без новых Git files; diff --check и относительная ссылка handoff проверены |

Documentary ticket prerequisite не является qualified absence: проверка
синтетических input bytes/условных facts не устанавливает реальные custody,
SQLite integrity или native authority. Все 23 официальных semantic DOC.ORACLE
не объявляются исполненными Stage A тестами. Проверены их сохранность и
указанная минимальная C-A01 коррекция, а не вся будущая реализация.

## Exact changed files и hashes

Ровно два пути, оба mode 100644:

1. `docs/tasks/MVP_08B_4_DQ_00/NATIVE_EVIDENCE_CONTRACT_PROPOSAL.md`:
   Git blob SHA-1 `10fce2362d1649efe0a2b47a47bf523819099bc2`;
   raw SHA-256 `a395951c100346a96eb6249f55c097db953e1dbf3d225bc0a360893379cd0a5c`.
   Diff: две normative paragraphs и два six-line typed refs, всего 16 добавленных строк.
2. `docs/tasks/MVP_08B_4_DQ_00/FINAL_HANDOFF.md`: текущий handoff заменяет
   прежний report; final blob/SHA-256 — в публикационном ответе для исключения
   self-hash cycle.

Все остальные tracked paths совпадают с exact base. G1–G6, OD4 и CP decisions
не изменяются и не расширяются. Native root/pre-write gate остаётся отдельной
границей; этот docs fix не выдаёт новых permissions и не меняет реализацию.

До публикации read-only GitHub refs: main
`a28277b4cb68a3db5da52edc598c37ce66314604`, implementation feature
`6190dc50bd13bbb34e0adcc57ddc219a4c5cd44d`. После push проверяются те же
refs и точный опубликованный docs commit; результат указан в ответе.

## Независимая приёмка / STOP

Reviewer должен проверить exact diff, два original_ticket refs, неизменность
58 preimages и 23 expected outcomes, case-local отсутствие ticket в negatives,
отсутствие hash cycles и подмены custody. Исправление передаётся на независимую
приёмку C-A01; собственный verifier не называется независимой проверкой.

SQLite connections/DB/root/journal/native logs/native tests/fault injection,
worker spawn/kill, Windows qualification, provider/render/production не
выполнялись. Main и feature branch не изменялись; merge/release/CI отсутствуют.

**STOP после публикации.** Не возвращаться к Stage A programming до независимой
проверки C-A01. Этот пакет не утверждает STAGE_A_PURE_READY и не снимает
NATIVE_BLOCKED_PRE_WRITE_GATE.
