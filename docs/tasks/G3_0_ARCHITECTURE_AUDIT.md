# G3.0 — Architecture & Scope Audit

Дата аудита: 2026-11-17 (Europe/Kyiv). **G3.0 / DOCS ONLY / READY_FOR_OWNER_REVIEW.**

База: `7166902820731984ceb56d79275a70f83f665b23`; base tree: `504881fec0b293fa1eb0808f666e63cd30bf5c7c`. Исследованный source PR #11: `6cfa7b4b535b0171ae2871b7e68e545b48ba332a`; source tree: `2850e0977af749569a5d363ffc1f540ffd788f2d`.
Все новые рекомендации интеграции — **PROPOSAL**. Этот пакет не утверждает G3 implementation, production permissions, merge или release.

## Вывод

Документационный аудит готов к решению владельца: **READY_FOR_OWNER_REVIEW**. Полная целевая production-цепочка **не готова**. Можно предложить отдельный перенос изолированного D1 synthetic baseline (четыре пути) без изменений G1/G2; это **PROPOSAL**, не принятое интеграционное решение. Общий Production Gate и связь Editor Preview → Gate → Render отсутствуют. Их нельзя получить простым cherry-pick source или включением Storage S3. Исследованный D1 создаёт только фиксированный синтетический тест, не видео по произвольной теме и не реальным материалам.

## Закреплённые доказательства

| Объект | Проверенный SHA / результат |
|---|---|
| Remote origin/main при начале аудита | `7166902820731984ceb56d79275a70f83f665b23` |
| Approved main tree | `504881fec0b293fa1eb0808f666e63cd30bf5c7c` |
| Source commit PR #11 | `6cfa7b4b535b0171ae2871b7e68e545b48ba332a` |
| Source tree | `2850e0977af749569a5d363ffc1f540ffd788f2d` |
| G1 merge/base G2 | `53e4dfa169cf0e8df3ee0b5829e96845383048ed` |
| G2 commit, parent approved main merge | `5b6808b7de7bd7c6746d007e2f7ece455f847131` |
| Approved main merge parents | G1 + G2 commit; tree равен G2 expected tree |
| Main/source tree inventory | 259 / 455 blobs; 254 одинаковых; remaining 201 = 196 A + 5 M; нет удалений |
| G1/G2 no-repeat | 45 G1 + 6 G2, все entry source/main равны, все вне remaining |
| Audit branch | `docs/g3-0-architecture-scope-audit`, основана ровно на approved main |

Сравнение привязано к exact source SHA, не к изменяемому head PR #11. Source прочитан в отдельном scratch archive из Git; реализация не копировалась в audit branch. Исторические статусы source документов — контекст соответствующих старых scopes, а не новое owner approval для G3.

Полный per-path реестр: [G3_0_FILE_REGISTRY.md](G3_0_FILE_REGISTRY.md). Схема и каждый переход: [G3_0_DEPENDENCY_MATRIX.md](G3_0_DEPENDENCY_MATRIX.md). Риски и gates: [G3_0_RISK_AND_GATES.md](G3_0_RISK_AND_GATES.md). Решения: [G3_0_OWNER_DECISIONS.md](G3_0_OWNER_DECISIONS.md).

## Минимальный предлагаемый D1 комплект — PROPOSAL

Все четыре entry source имеют mode `100644`; Git SHA ниже — blob SHA-1, SHA-256 — exact raw file bytes. Это фиксирует кандидат на будущее задание; никакой G3 implementation не staged/committed в G3.0.

| Source path | Git blob SHA-1 | SHA-256 raw bytes |
|---|---|---|
| `docs/tasks/SI_PRODUCT_02_2_D1_SYNTHETIC_RENDER_PERMIT.md` | `928db7f952c748ab7206427b0a995899b8e46439` | `b849855f115ccf2ffcb3f34937c63f8b0bdb808949bbe61977d4a183676d257b` |
| `examples/topic_d1_synthetic.json` | `780a21630ea965070ed351230314f901e7822f33` | `1eba5e74b6a5e8e09e57708cbb66e7bce6e2d0a6690f11fb3770741f06df566f` |
| `scripts/topic_to_video.py` | `488cd3dff1d755e6df68f1e4eebf9e094a30526c` | `4178627ca480812beffd195c91734a7196062beb36c4da6da6cb716019db5549` |
| `tests/test_topic_to_video_d1.py` | `8859199dec4bac75dba7ded38e4e6c8fa4ad550d` | `87240b79ff9308a849b7600eb71388a64d34d409aa0eda9ed7c0d7928312f344` |

Рекомендация: перенести adapter, зарегистрированную fixture, неизменённый regression test и документ synthetic permit вместе только после решения владельца. Правки общих модулей не требуются по static dependency closure: direct runtime deps и все G1/G2 entry уже совпадают с source. Документ permits — необходимый scope constraint, не production grant. Исторические owner/architecture документы можно читать по pinned source URL без массового копирования в main. README/WORKLOG/ROADMAP/ignore source snapshot исключены; любые будущие новые записи готовятся по фактическому результату.

## Что реально проверено запуском в G3.0

Команда из отдельного source archive, по одному процессу на версию:

```text
python -m unittest tests.test_topic_to_video_d1 -v
```

| Tree исполнения | ОС / фактический Python | FFmpeg / ffprobe | Тестов | Fail / error / skip | Exit | Время unittest |
|---|---|---|---:|---|---:|---:|
| Source `2850e097…` | Linux x86_64 / CPython 3.10.22 | 7.1.5-0+deb13u1 | 3 | 0 / 0 / 0 | 0 | 5.280 s |
| Source `2850e097…` | Linux x86_64 / CPython 3.13.18 | 7.1.5-0+deb13u1 | 3 | 0 / 0 / 0 | 0 | 3.985 s |
| Будущий integrated G3 tree | Не создан | — | NOT_RUN | — | — | — |
| Windows 10/11 CPU-only | Не предоставлена этой сессии | — | NOT_RUN | — | — | — |
| Full unittest / pytest G3.0 | Не запускались, docs-only audit | — | NOT_RUN | — | — | — |

Положительный тест выполняет две сборки RU/UK (четыре временных MP4 на версию Python), используя локальную тишину и программный фон. Проверяет настоящий evaluator/Projection, доступность карт, exact scene plan/project locale, subtitle timing, H.264/AAC, длительность 1.4±0.08s и яркие пиксели в subtitle interval. Сравнивает JSON bytes между двумя запусками; **MP4 bytes не сравнивает**, права/смысл/произношение не проверяет. Все generated outputs — во временных каталогах теста, удалены, не опубликованы.

Negative test содержит 15 input mutations + 4 function fault injections: без/изменённого permit, PRODUCTION purpose, другой scenario/текст/локаль, missing findings, INVALID/STALE, внешнее audio/image/TTS поле, изменённый WAV/eval/card/UNAVAILABLE. До `first_video.build` должен быть отказ. Отдельный тест инжектирует сбой второй сборки: финальный result отсутствует, staging очищен. Это scoped synthetic failure evidence, не crash/power-loss/hostile filesystem qualification.

SHA-256 локальных stdout/stderr журналов: 3.10 — `167e2051e6fe47cc7316b1a5c56ce1ecf2d37196923bc8060ffae89990c80c4e`; 3.13 — `9a48215cd61f0806e0aaec17e479061c5ed7c1c5a5eb540cdd1a725c7e51deab`. Сводка и exit codes прочитаны по завершении процессов, не по промежуточной строке OK.

Предыдущий G2 [CI run 44033792948](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/actions/runs/44033792948) и [acceptance packet PR #13](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/pull/13) относятся к G2 tree, совпадающему с approved main: 711 unittest (skip 1) и pytest 723 passed/skip 1 на 3.10.22/3.13.18, exit 0; это **историческое проверенное evidence из предыдущего этапа**, не новый G3.0 full-run. Source D1 сейчас не входит в main. Full source suites и Windows повторно не запускались.

## CI workflow — отдельное решение

Current main blob: `7ba7beb4a9f5d2e30104b65acf64a7104b5cec7e`; source blob: `6f3921c362d2142a362f7905d8e4f7463ba6a9fc`. Оба mode100644. Main уже ставит FFmpeg, pytest и запускает unittest+pytest на Ubuntu Python3.10/3.13; будущий D1 test будет обнаружен автоматически. **Для минимального D1 не требуется менять workflow.** Сейчас workflow не изменялся.

Source дополнительно ограничивает contents:read, отключает checkout credentials, обновляет checkout/setup-python, сверяет SHA, печатает версии, на3.13 отдельно рендерит fixture и загружает JSON/MP4 через upload-artifact. Рекомендуется **DEFER source workflow** и рассмотреть отдельный минимальный CI-hardening change после owner approval. SHA equality с GITHUB_SHA подтверждает checkout, не approval/trust; PR SHA — служебный merge ref.

Artifact upload не нужен для прохождения D1 unit tests. Он создаёт отдельный риск доступа/retention и может раскрыть private evaluation/cards/project data. Source upload расположен **до** full unittest/pytest: наличие artifact не означает успешный полный run. Generic source permit допускает local/CI test assembly, но запрещает публикацию/распространение; выгрузку artifact нельзя считать автоматически разрешённой. Требуется явное разграничение приватного CI evidence и публикации, exact allowlist/доступ/срок хранения/удаление, policy для fork PR и повторная review action versions. Не предлагать real media, credentials или production grants в CI.

## Предлагаемая последовательность — PROPOSAL

1. Владелец выбирает scope: только synthetic D1 baseline или отдельный будущий design полного Preview→Gate bridge. Не обещать полную цепочку по результату D1.
2. Утвердить exact четыре source entries и trusted-output-directory assumption либо сначала заказать отдельную исправляющую ревизию D1 path handling. V07 Preview не защищает D1: он не вызывается из D1.
3. Отдельным implementation заданием собрать новый candidate от актуальной утверждённой базы, проверить no-repeat G1/G2 и все entry; source копировать без mass merge. До этого шага G3 код не переносить.
4. Выполнить D1 targeted и полные unittest/pytest на actual integrated tree в Linux3.10/3.13; current CI без upload достаточно. При блокирующем failure STOP, без изменения утверждённых blobs для получения PASS.
5. Отдельно выполнить Windows CPU-only real FFmpeg/ffprobe run на выбранной Windows10/11 машине; проверить libx264/AAC/libass, кириллицу/субтитры, пути и permissions. Linux не заменяет этот gate.
6. Если нужны CI артефакты — отдельное owner решение; затем отдельный CI-only change. Source workflow не переносить пакетом.
7. Общий Production Gate/rights/human approvals/evidence custody и Preview bridge — отдельный **PROPOSAL** с закрытыми input/output, revocation/freshness и tests. Storage S3 не объявлять доступным; если выбран protected storage — отдельные host/native gates до его использования.

## Передача независимому проверяющему

Проверить source/main SHA и 201-путевый diff; registry 4/193/4; no-repeat51; dynamic/nested imports; direct D1 deps равны base; независимость Preview и D1; ограничения permit и отсутствие общей авторизации; source workflow publication risk; текущие/исторические/NOT_RUN evidence. После doc commit проверить sole parent=approved main, diff ровно пять Markdown и отсутствие других изменений. Commit identity передаётся внешним handoff, без self-hash в документе. Пакет **не является результатом уже состоявшегося независимого ChatGPT аудита**.

## Контроль документационного пакета

Выполнен структурный validation: 201 registry row по одному на remaining path; каждый source blob повторно проверен SHA-1 от Git blob header + exact raw bytes; рекомендации ровно4/193/4; все local Markdown links и ID R/B разрешаются; таблицы синтаксически замкнуты. Проверены51 no-repeat entry и equality всех shared entries. Staged diff: ровно пять новых Markdown из этого пакета; `git diff --cached --check` — exit0. Повторная remote проверка перед commit: main остался `7166902820731984ceb56d79275a70f83f665b23`, выбранная docs branch ещё не существовала. Эти проверки не являются unit/full/native test execution.

**STOP — owner review и независимый аудит; implementation/CI/main/merge/release/production permissions не разрешены этим пакетом.**
