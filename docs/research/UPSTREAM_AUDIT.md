# Независимая проверка китайского оригинала

Дата: 2026-11-04. Объект: [konlu/story-studio, 87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1](https://github.com/konlu/story-studio/tree/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1).
HEAD/main совпали с pinned revision; отдельного stable tag не установлено. Исследование статическое: оригинальный код, его тесты, установщики, модели и сервисы не запускались.

## Инвентаризация

Собственный Git/tree/JSON/AST подсчёт:

- 608 tree entries, включая каталоги; 576 файлов, 20 Python-файлов.
- 57 historical catalog rows; source_url, published_at, collected_updated_at во всех null.
- Метрики: likes/saves/comments/shares; нет views, impressions, watch-time и retention curves.
- Все fact_status = 未整体核实, то есть целиком не проверены.
- Есть video_id, исходные пути и SHA-256. Отсутствие URL не означает отсутствие вообще каких-либо идентификаторов.
- 296 новых биографических *_project.md.
- Шесть test-файлов, 87 test-методов: 10+11+7+29+18+12. Это не 87 успешно выполненных тестов.

Пример структуры и отсутствующих источников: [catalog.json](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/modules/history-writing/corpus/catalog.json#L3-L28). Итоговые количества получены чтением JSON/tree, не запуском history_tool.

## Discovery и ranking

[records()](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/modules/history-writing/scripts/history_tool.py#L24-L25) читает локальный corpus/catalog.json. [search()](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/modules/history-writing/scripts/history_tool.py#L49-L87):

1. Фильтрует era/person/template/account/conflict/cluster и исключённый cluster.
2. Требует присутствия поисковых слов в текстовых полях.
3. Даёт +3 за слово в заголовке, иначе +1 за совпадение.
4. Жадно выбирает релевантные записи с бонусами +2 за новый cluster и +1 за новый account.
5. Прямо сообщает: rank is relevance and diversity, not predicted performance.

Engagement metrics в score не участвуют. В исследованных 20 Python-файлах сетевые операции найдены в bootstrap/dependencies и TTS; самостоятельного crawler/RSS/news aggregator, ML training или A/B engine не найдено. Это граница найденного кода: агент с внешним web tool теоретически способен искать дополнительно.

Малое несоответствие: eligibility нормализует casefold, title bonus использует исходный регистр (L69–71). Для будущих RU/UA/Latin материалов нужна единая нормализация; это не причина переписывать рабочий Sprint 26.

## Narrative / Writing-DNA / evidence

Оригинал содержит редакционные структуры, hooks, примеры и агентные инструкции. В [hook_analysis.json](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/modules/history-writing/corpus/hook_analysis.json#L1-L3) автор прямо указывает ручную разметку, отсутствие аудиотаймкодов и retention data, субъективную/зависимую выборку.

Следовательно, [«4 из 5 → viral potential»](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/modules/characterstory-writing/%E9%80%89%E9%A2%98%E7%AD%96%E7%95%A5DNA.md#L659-L669) и [«TOP3 по конверсии»](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/modules/characterstory-writing/%E9%80%89%E9%A2%98%E7%AD%96%E7%95%A5DNA.md#L720-L726) остаются неподтверждёнными эвристиками. Селекция популярных сценариев без знаменателя и контролей не доказывает причинного эффекта конструкции.

Подтверждён документальный дефект: [DNA](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/modules/characterstory-writing/%E9%80%89%E9%A2%98%E7%AD%96%E7%95%A5DNA.md#L11-L18) заявляет 315, но перечисляет 63+78+79+37+34+19=310. [Corpus README](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/modules/characterstory-writing/corpus/README.md#L11-L21) даёт 296 новых+19 старых=315. Это несогласованная отчётность, не доказательство отсутствия материалов.

Сильный контрпример против чрезмерно негативного вывода: [GUIDE](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/modules/history-writing/GUIDE.md#L5-L27) различает лайки, истинность и охват; требует evidence до hook. [Правила фактов](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/modules/history-writing/references/%E5%8F%B2%E5%AE%9E%E4%B8%8E%E7%B4%A0%E6%9D%90.md#L5-L69) предусматривают claim ledger, точный локатор, поддержку и опровержения. Hash validation не объявляется исторической истиной.

Рекомендуется самостоятельно реализовать эти контракты на оригинальных RU/UA материалах. Корпуса, формулировки и DNA не переносить и не переводить целиком без прав.

## Сильные media-механизмы

| Механизм | Evidence | Что доказано / граница |
|---|---|---|
| Audio-first alignment | [align_with_coli.py](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/modules/render-history-video/scripts/align_with_coli.py#L24-L102) | Проверка timestamps, полного текста, повторов и границ; RU/UA качество конкретного ASR не проверено |
| Версия медиа и review | [check_handoff.py](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/scripts/check_handoff.py#L49-L124) | Hash/duration/review linkage, не автоматическая семантическая экспертиза |
| Защита платного TTS | [doubao_tts.py](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/scripts/doubao_tts.py#L175-L249) | Confirmation, existing-output protection, полный decode; live сервис не вызывался |
| Staging/backup export | [export_jianying.py](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/modules/render-history-video/scripts/export_jianying.py#L173-L286) | Реальные механизмы staging и сохранения старого draft; полная транзакционность при любом sidecar failure не доказана |

## Перепроверка R1–R6

| ID | Статус и impact | Evidence / контрпример | Минимальная мера и acceptance |
|---|---|---|---|
| R1 aspect ratio | SOURCE-CONFIRMED причина; renderer не запускался | [scale=w:h, setsar=1](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/modules/render-history-video/scripts/render.py#L104-L113). Для 640×480→1080×1920 отношение осей круга станет 0.421875 | Explicit contain/cover; после разрешения синтетический круг и измерение осей |
| R2 SRT | SOURCE-CONFIRMED неполный контроль | [handoff](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/scripts/check_handoff.py#L70-L78) смотрит max end, не порядок start/end. [parse_srt](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/modules/render-history-video/scripts/export_jianying.py#L120-L134) пропускает часть плохих cues | Строгий parser, start<end, диапазоны, политика overlap; ошибки не исчезают молча |
| R3 TTS cache | Архитектурный пробел, не доказанный баг | [L215–237](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/scripts/doubao_tts.py#L215-L237) защищает путь, не глобально ищет text+voice+model+params | Content-addressed cache, explicit rebilling policy |
| R4 audio/metadata | RISK: fault injection не проводился | [L239–249](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/scripts/doubao_tts.py#L239-L249) публикует MP3 перед voice.json | Staged manifest/recovery; отказ метаданных не должен повторять платный вызов |
| R5 CRF type | SOURCE-CONFIRMED validation defect | [L35–41](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/modules/render-history-video/scripts/render.py#L35-L41): собственное выражение даёт TypeError для None/строки, bool проходит числовую проверку | Integer guard с запретом bool, диагностическая ошибка до FFmpeg |
| R6 editor | UNTESTED interoperability, не установленный баг | [Serializer tests](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/modules/render-history-video/scripts/test_export_jianying.py#L11-L59) не открывают реальный редактор | Конкретная Windows editor version: открыть, сохранить, экспортировать, прослушать |

Это находки в upstream; они не приписываются автоматически рабочему RU/UA renderer.

## Лицензия

[Upstream LICENSE](https://github.com/konlu/story-studio/blob/87c2bbf7093d7817d28a0f2b32cf21bb857b7cc1/LICENSE#L1-L66) объявляет CC BY-NC-SA4.0, но текст модифицирован/сокращён: ссылка на отсутствующий §6(a), завершение на §5, собственные ограничения paid-course/software-service. [Стандартный SPDX текст](https://github.com/spdx/license-list-data/blob/31846481de7ea17d92f2f46fad76abe58b2e9bb0/text/CC-BY-NC-SA-4.0.txt#L109-L158) имеет другую структуру.

Точный статус: declared NC/SA, nonstandard license text; commercial import BLOCKED pending clarification/permission/independent replacement. Историческая MIT-копия не является разрешением на все поздние файлы; её отдельные уже предоставленные права также нельзя автоматически объявлять отозванными. Нужен пофайловый provenance и отдельная оценка данных/весов/зависимостей.

## Сопоставление со Sprint 26

[first_video.py](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/e1f4efb0fb5ff290bb198349213c004b4667ef0f/scripts/first_video.py#L72-L152) уже принимает scene-plan + WAV/Silero + images, создаёт v3 и вызывает FFmpeg. Будущий editorial слой должен выдавать этот контракт.

[Schema v3](https://github.com/olegale-ctrl/Story-Studio-RU-UA-WORK/blob/e1f4efb0fb5ff290bb198349213c004b4667ef0f/core/project_schema.py#L202-L234) проверяет точные поля; evidence, experiments и публикации лучше хранить отдельно с version/hash linkage. Наш текущий gap — discovery/evidence/ranking/narrative/outcome feedback; сохранение media-конвейера важнее замены на чужую платформу.
