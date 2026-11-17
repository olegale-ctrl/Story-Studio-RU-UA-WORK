# G3.0 — риски, security, rights и обязательные gates

Дата: 2026-11-17 (Europe/Kyiv). **G3.0 / DOCS ONLY / READY_FOR_OWNER_REVIEW.**

Base `7166902820731984ceb56d79275a70f83f665b23`, tree `504881fec0b293fa1eb0808f666e63cd30bf5c7c`. Source PR #11 `6cfa7b4b535b0171ae2871b7e68e545b48ba332a`, tree `2850e0977af749569a5d363ffc1f540ffd788f2d`.

Это выявленные границы и **PROPOSAL** будущих gates, а не новое разрешение. Готовность аудита не означает готовность production-цепочки. Реестр: [G3_0_FILE_REGISTRY.md](G3_0_FILE_REGISTRY.md); решения: [G3_0_OWNER_DECISIONS.md](G3_0_OWNER_DECISIONS.md).

## Риски и последствия для решения

| ID | Риск / серьёзность | Основание в source/base | Реальная проверка | Gate / рекомендуемое действие — PROPOSAL |
|---|---|---|---|---|
| K01 | Критический: принять synthetic admission за production authority | D1 VERSION= SyntheticRenderPermitV1, PURPOSE=SYNTHETIC_TEST_ONLY; exact registered digest; G2 всегда permissions_granted=false. Existing first_video.build не требует D1 permit | D1 negatives отклоняют PRODUCTION и изменённые/отсутствующие permit до build; нет теста общей production authority, потому что её нет | Запрет production сохраняется. G3-SCOPE должен отдельно ограничить D1; общий Gate требует отдельного контракта, не автоповышение synthetic token |
| K02 | Высокий: заявить сквозной Preview→Render, которого нет | topic_to_video импортирует evaluator/Projection/first_video, но не editor_preview. Формат D1 fixture другой | Static imports + сравнение examples: evaluation_inputs равны, plans vs scene_drafts не равны; исходные D1 tests не проходят через Preview | Разделить synthetic baseline и будущий bridge. До нового exact binding/contract/tests целевая единая цепочка BLOCKED |
| K03 | Высокий: выход через неподконтрольную цепочку путей / гонки | D1 проверяет output.exists и output.parent.is_dir, staging рядом, повтор exists перед rename; не проверяет каждый parent на POSIX symlink или Windows reparse. G2 V07 helper не вызывается | Static source review. Hostile-path exploitation/race stress в G3.0 NOT_RUN; успешный temp-dir test не квалифицирует чужую цепочку | До интеграции выбрать owner assumption: только полностью подконтрольный private local parent либо отдельно заказать исправление и negative tests. Даже с повторными name checks TOCTOU не исчезает |
| K04 | Высокий: публикация private карточек/планов/MP4 под видом CI evidence | Source upload включает output-d1/*.json, project JSON, два MP4. Permit разрешает assembly local/CI, но запрещает публикацию/распространение | Workflow diff прочитан; artifact upload в G3.0 NOT_RUN | Workflow DEFER. До upload owner определяет readers, exposure для fork PR, exact file allowlist, private/public boundary, retention, deletion/custodian. Тестовый scope не даёт общего права публикации |
| K05 | Средний/высокий: supply chain, расход CPU/диска, ложная успешность artifact | Apt FFmpeg и pytest range не pinned; Actions version tags. Source render/upload находятся до full tests, разрешения contents:read и persist-credentials:false — отдельные hardening improvements | Current G2 CI успешно; source workflow на новом G3 tree NOT_RUN | Существующий workflow достаточен для auto-discovered D1 tests. Hardening отдельно review. Если owner разрешит upload, связать evidence с exact tested tree, tool versions и итогом run; не доверять одному наличию artifact |
| K06 | Высокий для Windows release: CPU portability не равна native qualification | D1 использует libx264/AAC/libass, ffprobe; first_video optional Silero branch не нужен. В source нет Windows CI job | Свежие source Linux3.10.22/3.13.18 D1: по3 tests PASS; Windows NOT_RUN. Исторический V07 Windows отчёт не запуск на current integrated G3 | Отдельный выбранный Windows10/11 CPU-only host, реальные versions/tool codecs/fonts, fresh path, Cyrillic subtitles and playback checks. Не требуется GPU/TTS, но нужны установленные инструменты |
| K07 | Критический при неправильной зависимости: объявить Storage S3 готовым | storage_transaction_model — RAM model; windows_lab dispatcher получает Caller от harness; нет native IPC authentication/ACL/service/NTFS writer | Прочитаны module docs, imports, PURE_ONLY acceptance и host readiness; native в G3.0 NOT_RUN | DEFER все S3 implementation paths. Protected production storage требует отдельные machine/admin/runtime/observer/profile approvals; без них BLOCKED. Synthetic D1 не должен зависеть от S3 |
| K08 | Высокий: hashes/consistency/migration превратить в доверие/права | approval_attestation прямо исключает authentication; schema2 integrity/migration pure; G1 rights_binding подтверждает binding, не законность лицензии | Static review функций/imports/границ и исторических контрактов; дополнительные storage suites не запускались | Digest служит соответствию bytes, не выдаче доверия. Нужна отдельная authoritative проверка identity/rights/intended use/revocation для real materials |
| K09 | Средний: массово перенести исторический scope и повторно G1/G2 | 201 remaining, из них162 docs; source README/ROADMAP/WORKLOG описывают другие даты/ветки/широкие suites | Полный Git inventory; no-repeat51; 4 INCLUDE /193 DEFER /4 EXCLUDE | Перенос только по будущему утверждённому allowlist. Старые отчёты не переписывать и не выдавать за новый execution/owner decision |
| K10 | Средний: считать медиа/факты полностью подтверждёнными тестом | Inspect_video измеряет streams/duration и ≥20 bright pixels в нижней половине кадра; test сравнивает JSON bytes | Source tests PASS, MP4 binary equality/semantic OCR/правильность исторических утверждений NOT_TESTED | Evidence claims ограничить фактически измеренным. Смысл, читаемость, редакционное согласование и real rights — отдельный review |

## SyntheticRenderPermitV1: точная граница

Source: `scripts/topic_to_video.py` blob `488cd3dff1d755e6df68f1e4eebf9e094a30526c`; permit contract blob `928db7f952c748ab7206427b0a995899b8e46439` на указанном source SHA. Контракт исторически помечен OWNER_APPROVED_FOR_SYNTHETIC_TEST_SCOPE для SI-PRODUCT-02.2.1, исходная база в нём `784ddaf82fda5b13dfa31b4b379fabb83da5a908`. Эта метка не является утверждением нового переноса/новой публикации.

Разрешён единственный scenario `si-product-02.2.1-d1`, purpose `SYNTHETIC_TEST_ONLY`, version `SyntheticRenderPermitV1`, digest `469e3db84ee2d97ed76460a684d2cb4b5977e2b493084a0d4bfc0bdb373a71a8`.

Связка canonical SHA-256 включает version, scenario, purpose, полные evaluator inputs, фактический evaluation, обе actual Projection cards, RU/UK plans и SHA-256 каждого generated WAV. Планы закрыты: ровно ru/uk, каждый с locale/title и одной text-only scene, без external image/audio/TTS settings. Реальные WAV bytes сверяются с generated mono PCM16/24kHz/1s silence. После реального evaluator/Projection и проверки bindings вызывается build; случай произвольной темы или изменённого текста не подходит под registered digest.

Input parser ограничивает чтение 1,000,000 bytes, отклоняет duplicate JSON keys и вызывает canonical_si_json validation. Это не основание добавлять произвольные поля/планы или считать JSON trusted. Даже валидный permit — открытое константное соответствие известной fixture, не secret, signature, одноразовая capability или аутентификация автора. Любой может скопировать fixture; это не наделяет production authority. D1 не проверяет весь мир и не запрещает вызвать существующий renderer напрямую.

Нельзя автоматически создавать permit из HANDOFF, evaluator OK, creative eligibility, DISPLAYABLE card, APPROVED или score. Он не переносится на реальные материалы, произвольные WAV/voice weights/изображения, другую тему/usage; повтор той же exact fixture в новом временном каталоге допустим в ограниченном тестовом scope. Отказ до build допускает временную подготовку локальной synthetic staging, но не финальный result; тесты не доказывают crash durability этой очистки.

## Права на материалы

| Материал / предмет | D1 фактический источник | Статус для real production / чего недостаёт |
|---|---|---|
| RU/UK тексты | Фиксированные synthetic fixture scenes, bound digest | Не замена human editorial approval фактического RU/UK текста; перевод/точность языка не квалифицированы автоматическим test |
| Изображения | Программный gradient first_video.make_background; D1 не допускает image field | Для внешних фото/видео/иллюстраций нужны точный asset/content digest, происхождение, license/owner, territory/expiry/intended use и human review. Source факт не даёт права на изображение |
| Музыка | Не подаётся и отдельного music поля нет | Для реальной музыки отдельно composition/recording/performance/sync/usage rights по выбранным условиям; отсутствие музыки в fixture не подтверждает чужую лицензию |
| WAV/голос | Локальная тишина, не TTS и не запись человека | Для чужого WAV/человеческого голоса — происхождение, согласие/voice rights и применимая license/privacy review. Для TTS — точные weights/model/voice и terms, отдельно commercial scope |
| Silero/Edge/другие провайдеры | Не используются D1; source не загружает weights или online TTS | Наличие старого provider не разрешает коммерческий голос. Source owner decision сохраняет BLOCKED_ENVIRONMENT/weights-rights restrictions; любые реальные полномочия не выданы G3.0 |
| Шрифты и инструменты | FFmpeg/libass + доступные runtime fonts; стиль запрашивает Arial, возможен fallback | Проверить доступность и лицензии выбранного font/runtime/binary, если их распространяют; Linux rendering test не доказывает Windows font installation и не разрешает bundle |
| SI источники/утверждения | Синтетические records и заданные findings | Нужны реальные источники, даты получения, проверяемые фрагменты, claim-evidence binding и независимый human review для реальной темы. Synthetic label не превращает произвольный input в надёжный fixture |

G2 material states UNKNOWN/PENDING_REVIEW/REPORTED_BY_EDITOR/VERIFIED_EXTERNALLY — editor-reported data; grants_permission всегда false. Существующий editorial rights-binding CONFIRMED означает соответствие stored digest, не лицензионный допуск. Ни один такой label не закрывает перечисленные real production gates.

## Storage S3 и Windows

S3 здесь — внутренний трек Windows protected storage E01.3.9, не Amazon S3. D1 импортирует только уже имеющиеся renderer/SI modules. Никакого rationale добавлять 15 editorial modules и их suites ради D1 нет. Если владелец выберет в будущем обязательное protected persistence для production, это изменит scope и потребует отдельного решения; отсутствие S3 нельзя скрыть заглушкой или pure model.

Pinned source документы `E01_3_9_4_S3_2A_R1_INDEPENDENT_ACCEPTANCE.md` и `E01_3_9_4_S3_2B_PHASE0_HOST_READINESS.md` показывают PURE_ONLY acceptance и BLOCKED_HOST_NOT_PROVIDED. Native service, SID/token identity, SCM, ACL/SDDL, named pipe transport, DPAPI keys, NTFS write/recovery, independent attempted-write observer не квалифицированы. L-01–L-04 — ограниченные LAB design choices, не admin/install permission конкретной машины. PUBLISH_REVISION остаётся DISABLED, partial COMMIT reconstruction OFF; Q1/production deployment profiles не выбираются этим пакетом.

Для будущего native S3 нужны exact machine/VM и host profile, версия/build/runtime/source/artifact hashes, isolation/rollback, authorised administrator, bounded service/account/ACL operations, evidence custodian и независимый observer. Это отдельный project; G3.0 не создаёт VM, accounts, services, keys, ACL или production data.

Windows synthetic MVP не требует такого service и может быть отдельным user-level CPU-only run. Но текущая сессия Linux; исторические Windows3.12.10/V07 и separator-sensitive Silero failure не переименовываются в PASS нового G3. Windows junction/symlink privileges и NTFS ACL проверки тоже отдельны; skip winerror1314 не квалифицирует безопасность. V07 защищает только Preview по своему user-controlled-path assumption; source D1 эту защиту не наследует.

## Рекомендуемые gates — все новые решения PROPOSAL

| Gate | До какого действия | Требуемое доказательство | Сейчас |
|---|---|---|---|
| G3-SCOPE | Любая G3 implementation integration | Owner утвердил четыре source blobs/синтетический scope либо иной отдельно описанный scope; no-repeat51 | PENDING OWNER; готов только аудит |
| G3-PATH | Утверждение D1 для запуска | Выбран trusted private output-chain assumption или отдельно исправленный candidate + негативные path tests; остаточные гонки явно приняты в тестовом scope | PENDING OWNER; source boundary выявлена |
| G3-LINUX | Acceptance будущего integrated candidate | Target/full actual tree на3.10/3.13; exact Python/tools/tests/skips/exits; no source-scope pollution | SOURCE TARGET PASS; integrated tree NOT_CREATED/NOT_RUN |
| G3-WINDOWS | Заявление Windows CPU-only compatibility | Реальный выбранный Windows10/11 host, exact runtime/tool capabilities, кириллица/subtitle/render/playback/path checks | NOT_RUN; host not provided |
| G3-CI-EVIDENCE | Любая upload-artifact/public evidence | Явный owner scope, права доступа/retention/redaction/allowlist, provenance и финальный CI verdict, допустимость распространения synthetic media | NOT_AUTHORIZED by G3.0; workflow unchanged |
| G3-BRIDGE | Реализация Preview→Gate adapter | Closed interfaces + exact binding to Preview inputs/results/plans/materials, freshness/revocation/denial semantics, человеческие approvals и тестовые negative cases | PROPOSAL; интерфейс не выбран |
| G3-PRODUCTION | Реальные материалы/production render или публикация | Scientific/editorial review, реальные rights/intended use, authority/identity, exact unchanged assets/texts/audio, chosen trust/storage model и отдельное разрешение | BLOCKED / NOT_AUTHORIZED |
| S3-NATIVE | Если выбран native protected storage | Отдельные host/admin/profile/runtime/observer/native qualification approvals | BLOCKED; не prerequisite D1 |

## STOP conditions

Несовпадение approved base/tree/source, неучтённые пути, повтор G1/G2, отсутствие source blob, вывод прав из synthetic permit/hash/score, попытка artifact публикации без выбранного scope, попытка объявить Windows/native/full-chain PASS без реального run → STOP с фактами. Никаких автоматических расширений permit, generic production mode, смены fixture digest, правок A14/G1/G2 или обхода denial ради успеха.

**STOP после docs commit и передачи owner/ChatGPT пакета.**
