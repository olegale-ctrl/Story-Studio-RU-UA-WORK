# SI-E01.2b.3-RESUME-2-F1 — independent finding verification result

Дата: 2026-11-10 (Europe/Kyiv).
**Обязательный итог: C — BLOCKED_CONTRACT / DIAGNOSTIC ONLY / NO PRODUCTION FIX.**
Наблюдаемое CURRENT в T2 воспроизведено. Не доказано, что R.H.editorial_refs по
утверждённому контракту обязательно substantive либо исключительно audit-only;
поэтому ни CONFIRMED_DEFECT, ни CONTRACT_COMPLIANT не заявляются.

## Git и authority

- Repository: `olegale-ctrl/Story-Studio-RU-UA-WORK`.
- Implementation/source branch: `feat/story-intelligence-si-e01-2b-3-resume-2-currentness`.
- Exact base: `c90b94a108ba2ef4b1a4a5ab8226d206b79fbf21`.
- Diagnostic branch: `test/story-intelligence-si-e01-2b-3-resume-2-f1-eref`.
- Review branch: `docs/story-intelligence-si-e01-2b-3-resume-2-independent-review`;
  exact review SHA: `9c9aa7824b1d218fdb39215cecce745532d1b4f5`.
- Прочитан [полный independent review](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/9c9aa7824b1d218fdb39215cecce745532d1b4f5/docs/tasks/STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_2_INDEPENDENT_REVIEW_2026_11_10.md).
  До изменений оба remote HEAD совпали с handoff, implementation HEAD/base проверен,
  дерево чистое. Новая ветка создана строго от implementation SHA. Review docs
  прочитаны через git show, **не merged/cherry-picked/copied в рабочее дерево**.
- Прочитаны original/R1/R1a/R1b/owner approvals, G01 D1–D5, G02 D1–D4,
  accepted resolver/provenance contracts и проверяемый код. Finding не считался
  доказанным до настоящего воспроизведения.
- Final commit/remote SHA сообщаются после публикации в handoff; собственный SHA
  нельзя включить в bytes того же commit. Parent должен быть exact base.

## Только три новых файла

- [test_story_intelligence_currentness_eref_f1.py](../../tests/test_story_intelligence_currentness_eref_f1.py)
  — пять diagnostic test methods, реальные T1–T4 graphs и T5 comparison.
- Этот RESULT.
- [F1 CONTRACT_GAPS](STORY_INTELLIGENCE_SI_E01_2B_3_RESUME_2_F1_CONTRACT_GAPS.md)
  — точные clauses, unresolved role и минимальные варианты для владельца.

Production currentness_v1.py и все existing files, tests, golden vectors, approved
contracts, RFC, editorial/storage/main не изменяются. Нет fix, adapter, новой
семантики, error code или dependency. Диагностический тест T2 характеризует existing
behavior; зелёный test не означает, что это поведение approved/корректно по contract.

## Фактические T1–T5

| Case | Размещение ERef / setup | Resolver | Provenance | Actual check_si_currentness |
| --- | --- | --- | --- | --- |
| T1 | S1 → R → S2, ERefs нигде нет; observed=[S2] | PASS, 3 refs | PASS | CURRENT / [] |
| T2 | Одна ERef только в R.H.editorial_refs; S2.H=[] и payload.editorial_ref=null | PASS, 3 refs | PASS | CURRENT / [] |
| T3 | Та же ERef прямо в S2.H.editorial_refs; R.H=[] | PASS, 3 refs | PASS | INVALID / [REF_MISSING] |
| T4 | Одна ERef в original C.H.editorial_refs; K1→K2→K3 frozen C; все required SI deps active | PASS, 19 refs | PASS | INVALID / [REF_MISSING] |
| T4 baseline | Тот же authored Creative graph без ERef | PASS, 19 refs | PASS | CURRENT / [] |
| T5 | Контрактное сопоставление T1–T4 | Runtime asymmetry установлена | Не определяет ERef relevance | C — BLOCKED_CONTRACT |

Использована исключительно synthetic ERef:
`{kind:source,id:eeeeeeee-1111-4111-8111-111111111111,revision:1,content_hash:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb}`.
Это well-formed **неразрешённая ссылка**, не существующий material hash/evidence.
Snapshot остаётся UNKNOWN; ссылки не разрешаются в adapter и не получают trust.

Records строятся в топологическом порядке; SHA стандартным JSON/hashlib helper
сравнивается с accepted si_record_ref для каждой записи. Run snapshots — полные
canonical transitive audit manifests, independent explicit-edge oracle равен
accepted resolver и provenance. В T2 R/S2 SHA и observed S2 ref пересчитаны после
изменения R.H. В T4 перестроены все downstream refs и snapshots, включая оба
REVISION Runs и K1/K2/K3. Никакого mock/patch resolver/provenance/SHA, assignment
результата вместо вызова API или production mutation нет. Inputs также проверены
на отсутствие изменения после всех API calls.

### Буквальные SHA графов и observed context

Graph = `SHA256(C(records))` в construction order; context =
`SHA256(C({active_input_refs,selection_head_refs}))`. Это test observation value,
не новый wire envelope и не доказательство доверенной актуальности.

| Case | Graph SHA-256 | Context SHA-256 |
| --- | --- | --- |
| T1 | `f37a7b1e6414486d4650fb1bdc78ff08799b090ae7ce18a89c992a1e44213311` | `b00fb082d50d60b0c38d9ff3762110ff7a0ff3951b96901d373ac9f693729844` |
| T2 | `87b0f65a5d741ca48b34333f120f41a5b7cbb2c54e2914e954b108528a41f55b` | `c6fb19b10547f9979d02127b54d77036cdf9ef9e88610cdafdaf8249b276e793` |
| T3 | `af4948494a638898bb2b664c2b358dd372b8bdbd6ddaee4570ad7a807ad59dbb` | `d6edefa838d2b62dd12395c3707014f1395959da4ddcd50a02461b9b59f061e9` |
| T4 | `00b76408f63c39fb627ee3e52a72b4534902160ededeca6fff50d0271a64d1ec` | `c8c419a7b7123f921490f5897f07f5cb3b03aef19b35b1e70626aa7c1139fd45` |
| T4 baseline | `3422c69e7e26f32ba540c7828f2a22f73f1aa32e02fb4650d22e469dcf2335c3` | `7da7145991eb45d168017adcfeead3eaa2cd3da7ebddd3a1db267dde87444d73` |

T1–T3 Source S2: type=SourceItem, id=00000001-2222-4222-8222-222222222222,
revision=2; R: type=RunRecord, id=00000002-2222-4222-8222-222222222222, revision=1.

| Case | Root S2 SHA | Producer R SHA |
| --- | --- | --- |
| T1 | `7c17130e4a5a6811295525fe8c264bb10f8809b4192bcca550182d25e8626ba5` | `0676374769d39d66811094b540e8446951b409c5a567393a88497e63bd6fe60c` |
| T2 | `650e8cd4fbfc33ed44113ff70b0bd6111575acaf498022891ee69a34c3566462` | `26bc04e5f7ea5b0f2deb65f0d95562ac0e2e3414cbb7a6bb77f6fe83031e3c4d` |
| T3 | `6d57c7418144f1bcd2fa93b7c3b344308c744f245bdf693df1ca50a7b38e5601` | `0676374769d39d66811094b540e8446951b409c5a567393a88497e63bd6fe60c` |

T4 root K3: CreativeAlternative/0000000f-2222-4222-8222-222222222222/revision3,
SHA `07409b3d0e747746cf3b05be78cc7cd6ccb3f473ca15daf4a64bf4d00690fd0b`.
Original C: RunRecord/0000000e-2222-4222-8222-222222222222/revision1,
SHA `3abf1d026bf8024b338e52fc9a248c68296a9e594f20efc54cd5a659467bd031`.

Воспроизведение без дополнительных файлов:

```bash
.venv/bin/python -m unittest tests.test_story_intelligence_currentness_eref_f1 -v
```

Для печати evidence, а не подстановки expected outcomes:

```python
from tests.test_story_intelligence_currentness_eref_f1 import source_case, creative_case, evidence
for case in (source_case(), source_case('run'), source_case('source'), creative_case()):
    print(evidence(case))  # actual API result + independently computed input hashes
```

## T5 — что следует из контрактов и из source

GAPS приводит clauses original §8, R1 §§1.1–1.3/4.2, R1a §§2–4, G01 D1–D4,
G02 и R1b с exact-base line references. Broad ERef snapshot requirement сохраняется;
G01 исключает edit-base/metadata identities, но не назначает явно роль каждого
R.H.editorial_refs. Нельзя ни выдать такое exclusion за blanket ERef exemption,
ни автоматически признать любую историческую audit ERef текущим constraint.
Нужен узкий owner decision про **current actual REVISION Run**.

Непосредственная причина наблюдаемой асимметрии в неизменённом source: ordinary
HUMAN_EDIT делает continue в currentness_v1.py:178–181 до producer H.editorial_refs
check:182–183. У Creative producer берётся из payload.run_ref=C (строки 171–173),
guard не пропускается. Это описание механизма, не доказательство нормативной роли.
Comments implementation/старый RESULT не использованы как authority.

Минимальная рекомендация: утвердить direct header ERefs текущего actual producer
как relevant; тогда в отдельном fix-задании проверить header до early continue и
закрепить T2 INVALID/REF_MISSING. Альтернатива — явная audit-only exemption с
точной областью. Ни один вариант в F1 не утверждён, production fix не применён.

## Реальные прогоны

Linux x86_64, project `.venv/bin/python`, Python 3.12.14.

```bash
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_currentness*.py' -v
.venv/bin/python -m unittest discover -s tests -p 'test_story_intelligence_*.py' -v
.venv/bin/python -m unittest discover -s tests -v
```

| Suite | Tests / summary | Duration | Raw Python exit | Outer exit | Failures/errors/skips |
| --- | --- | --- | --- | --- | --- |
| F1 direct | 5 / OK | 0.482 s | 0 | 0 | 0/0/0 |
| All currentness | 36 / OK | 9.286 s | 0 | 0 | 0/0/0 |
| All SI | 139 / OK | 17.843 s | 0 | 0 | 0/0/0 |
| Full | 981 / OK | 794.064 s | 0 | 0 | 0/0/0 |

Currentness/SI diagnostic elapsed: 9.414 / 17.974 s. Каждый child запускается
subprocess.run с unfiltered stdout+stderr в `/tmp/si_currentness_eref_f1_*.raw.log`;
печатается raw Python return code, любой nonzero передаётся в sys.exit. Full идёт
отдельным процессом с тем же сохранением exit code. Нет pipeline/`|| true`, skips,
expectedFailure, harness/environment mutation или автоматического waiver.
Full diagnostic elapsed: 794.395 s. Summary OK, raw Python exit 0 и outer exit 0
согласованы. Дополнительно S2.3 выполнил 1659 parameterized scenarios. Историческое
OK/exit 1 расхождение не воспроизвелось, его причина этим запуском не установлена.

SHA-256 unfiltered raw logs (вне Git):

- Currentness: `fbbd160bb457804dea133de07f5eb0c7c7a6dffd7a7ff74a43ff8e81879351ce`.
- SI: `e53cd60dcf2e04e249e9be2c7e6344a9df375a592fab97454e9ba9940ee390a5`.
- Full: `369e361300730b07e03f7581a61319fb8435fd96bfb81767eeda9ea01b7d8267`.
Зелёные diagnostic suites не являются доказательством contract compliance T2
и не снимают withheld independent acceptance.

## QA, ограничения и STOP

Проверены exact three-new-file A-only allowlist, Markdown links/fences и
`git diff --cached --check` / `git diff --check` (exit 0). Все 17 existing SI
source/test files byte-identical exact implementation base, включая прежние
foundation/records/resolver/provenance и 10 currentness literal vectors.
Других existing-file изменений нет. Source remote повторно совпал с base;
main read-only наблюдался на `e1f4efb0fb5ff290bb198349213c004b4667ef0f`.
Parent/remote equality и clean worktree проверяются после publication; final
commit SHA и diff/stat сообщаются в handoff.
Существующий currentness module SHA-256 должен оставаться
`67c035282131bd2f37f2b4a605d28c2ed191eac0a866ff998d1867773d255bed`.

Отчёт не security audit и не independent acceptance реализации SI-E01.2b.3. Настоящие
runtime результаты obtained in this diagnostic, а не скопированы из review/baseline.
Нет доказательства фактического выполнения Run или editorial material/rights/identity.
Оставшийся вопрос — relevance current R header ERef, сформулирован в GAPS. До owner
решения статус **C — BLOCKED_CONTRACT**. Проверяемая реализация не исправлялась.

После publication — STOP для independent review. Нет PR/merge/release/main,
SI-E02, ERef adapter, persistence или protected writes. `PUBLISH_REVISION` DISABLED;
partial COMMIT reconstruction OFF; Windows S3.2b BLOCKED_HOST_NOT_PROVIDED.
