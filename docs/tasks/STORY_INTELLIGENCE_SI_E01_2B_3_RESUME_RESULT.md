# SI-E01.2b.3-RESUME — result

Дата: 2026-11-10. **BLOCKED_CONTRACT / NO IMPLEMENTATION.**

## Git и нормативная база

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Source: `docs/story-intelligence-si-e01-2b-3-g01-approval-resume`.
- Exact base: `e735d729f6dad8ff874a92d52b37f4a95bb8fc20`.
- New branch: `feat/story-intelligence-si-e01-2b-3-resume-currentness`.
- Source remote HEAD проверен до изменений: точное совпадение. Ветка создана от
  указанной базы, без main/старой blocked feature/RFC fallback.
- Final commit/remote SHA сообщается после публикации отдельно от self-referential
  содержимого; parent обязан быть exact base.

Прочитаны [owner approval](STORY_INTELLIGENCE_SI_E01_2B_3_G01_OWNER_APPROVAL_2026_11_10.md),
[полное задание RESUME](STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_CODEX_TASK.md), G01 proposal/
independent blocker review, прежние GAPS/RESULT, original/R1/R1a/R1b и owner approvals,
предыдущие acceptances и accepted model/codec/records/resolver/provenance/tests.
D1–D5 **утверждены и не пересматриваются**; D6 остаётся scope/STOP gate.

## Новый узкий blocker G02

[CONTRACT_GAPS](STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_CONTRACT_GAPS.md) содержит полный
reproducer и literal hashes ERef-free графа. Затруднение не в исторической базе:
D1 исключает прежние K1/K2 из active dependencies, сохраняя audit integrity.
Проблема — direct ClaimItem в C.semantic_input_refs не имеет role annotation.
Совпадение с genesis hook доказывает использование в hook, но не то, что producer
root не является также самостоятельным inherited constraint. При замене hook Qa→Qc
правила «override этой роли» и «сохранить still-applicable producer bindings» требуют
уточнения, какая именно роль назначена плоскому C-root.

Валидация воспроизведения: **19 records / 19 exact reachable refs / 11 distinct
observed active identities / 0 ERefs**, accepted resolver и provenance — OK, exit 0.
Angle/Idea/E1/Channel неизменны; старые creative versions не active. Qa исторически
существует с правильным hash, но не active. Вариант mapping A даёт CURRENT, B —
STALE; это proposed policy outcomes, **не выводы реализованного checker**.
Нельзя считать SHA проверкой exclusivity роли или вернуть INVALID вместо owner
decision по валидному графу. RESUME §3 Boundary of D2/D3 и §5 требуют STOP именно
при таком multiple-same-type mapping gap, до partial implementation.

## Состав изменений и невыполненный implementation scope

Только два новых файла из allowlist:

- `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_CONTRACT_GAPS.md`;
- `docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_RESULT.md`.

Currentness module/tests не создавались. Минимум шесть approved expected-state
literal vectors и восемь D5 test groups **не реализованы/не пройдены**, а не заменены
вымышленными oracle. Literal graph/context digests в GAPS — воспроизводимое blocker
evidence, не выполненная currentness acceptance. Нет изменений принятых modules,
исходных contracts, прежних reports/golden vectors/RFC/WORKLOG/config/dependencies/
editorial/storage/main. Immutable C и R2/R3 в synthetic graph проверены без их правки.

## Фактические тесты и диагностика exit codes

Linux x86_64; project `.venv/bin/python`, Python 3.12.14. Точные test commands:

```bash
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_currentness*.py' -v
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v
.venv/bin/python -m unittest discover -s tests -v
```

| Suite | Методы / summary | Raw Python exit | Duration | Skips |
| --- | --- | --- | --- | --- |
| Currentness | 0 / NO TESTS RAN | 5 (также direct shell exit 5) | 0.000 s unittest | 0 |
| Existing SI baseline | 103 / OK | 0 | 8.711 s unittest; 8.849 s diagnostic | 0 |
| Full baseline | 945 / OK; 1659 S2.3 parameterized scenarios | 0; outer session exit 0 | 800.231 s unittest; 800.558 s diagnostic | 0 |

Currentness exit 5 — **не PASS**, consequence contract STOP, не waiver тестирования.
SI/full проверяют неизменённый baseline, а не приёмку этой стадии.

Для full-suite exit anomaly запущен read-only diagnostic: `subprocess.run` получает
точный argv с `.venv/bin/python`, stdout и stderr без фильтра сохраняются в один raw
log `/tmp/si_currentness_resume_full.raw.log`. После завершения печатается
`RAW_PYTHON_RETURN_CODE`, elapsed time; outer Python делает `sys.exit(child.returncode)`.
Нет pipe/`|| true`, environment mutation или исправления unrelated harness/tests.
Целевой diagnostic отдельно напечатал каждый raw exit; currentness команда также
выполнена напрямую с наблюдаемым exit 5. Ни один nonzero code не объявлен успехом.
Полный запуск завершился с raw process exit 0 **и** outer session exit 0.
Старое расхождение 945 OK / exit 1 на этом запуске не воспроизвелось; его
историческая причина не установлена, прежний отчёт не переписан и не waived.
Этот full **baseline** — PASS; implementation acceptance остаётся BLOCKED_CONTRACT.

SHA-256 raw logs (диагностические файлы вне Git, не protected data):

- Full: `4ec627c2a5b264c3e907e6b2057b5ddbaab6376cc4f3d541248294f97a32fecb`.
- SI: `8031c27b6bc980f713037e04f1cbe273ed62472cdb8d563cdebdb7e9ef45a592`.
- Currentness: `e70fec2825d9bf206d27463a792768195039599cb39bcca66339f47283f84cce`.

Полный diagnostic запускался так; sys.exit сохраняет raw child status:

```python
import subprocess, sys, time, json
cmd = [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"]
print("EXACT_INVOCATION", json.dumps(cmd), flush=True)
start = time.monotonic()
with open("/tmp/si_currentness_resume_full.raw.log", "wb") as log:
    p = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT)
print("RAW_PYTHON_RETURN_CODE", p.returncode, flush=True)
print("ELAPSED_SECONDS", round(time.monotonic() - start, 3), flush=True)
sys.exit(p.returncode)
```

Запускающий interpreter — `.venv/bin/python`; фактический argv child:
`["/workspace/Story-Studio-RU-UA-WORK/.venv/bin/python", "-m", "unittest", "discover", "-s", "tests", "-v"]`.

## Проверки и решение владельца

Выполнены: Markdown links/fences, воспроизведение GAPS snippet (exit 0), exact
two-file A-only allowlist, `git diff --check` (exit 0). Все 14 accepted SI source/test
files дополнительно сравнены byte-for-byte с exact base, включая прежние
14 foundation / 18+3 record-value / 7 resolver / 9 provenance literal vectors.
Других tracked изменений нет. Source remote HEAD повторно совпал с base;
main наблюдался read-only на `e1f4efb0fb5ff290bb198349213c004b4667ef0f`.
Post-publication контроль remote/base/parent/clean worktree и точный diff/stat
сообщаются в handoff; commit SHA не встраивается в собственное содержимое.

Для resume нужен точный алгоритм распределения direct C claim roots по заменяемым
hook/chapter и retained constraint roles, с expected state для exact G02 graph.
GAPS перечисляет минимальные варианты без самостоятельного approval и без новых
обязательных wire fields. D1–D5, ERef INVALID boundary и отсутствие implicit latest
сохраняются. Нет semantic truth/eligibility/rights/identity/execution claims.

Нет PR/merge/release/main изменений, ERef adapter, persistence/protected writes,
RFC или SI-E02. `PUBLISH_REVISION` DISABLED; partial COMMIT reconstruction OFF;
S3.2b BLOCKED_HOST_NOT_PROVIDED. Linux baseline не Windows native qualification.
После публикации — **STOP для независимого review и owner clarification G02**.
