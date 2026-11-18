# MVP-08.0 — Security, rights and reliability

**Status: PROPOSAL — OWNER REVIEW REQUIRED.** Проверено 2026-11-18.

Контрмеры ниже не реализованы и не квалифицированы. Основания: [код точной базы](MVP_08_0_DISPATCHER_ARCHITECTURE.md) и [официальные источники](MVP_08_0_PROVIDER_INVENTORY.md). H означает проверку текста, а не безопасное исполнение.

| Угроза | Предлагаемый контроль / fail-closed | Остаточный риск / gate |
|---|---|---|
| Компрометация API keys | OS credential store или секрет только в памяти; в job — opaque credential ref; редактирование auth headers, body, URL query и исключений; scoped keys, rotation | Windows Credential Manager не квалифицирован; секреты запрещены в project JSON, отчётах, логах, Git и portable backups |
| Утечка промптов и исходных файлов | Показать получателя, модель, регион, payload hash и retention; минимум PII; upload только утверждённой ревизии | Runway S27 и Arena S08 содержат права использования данных; consent не договор конфиденциальности |
| Непреднамеренная оплата | Provider Free Quota Only (S48), срок quote, job/month caps, decimal reservations, без auto top-up/PAYG; paywall → PAUSED | Локальный cap не контролирует внешние действия аккаунта и неизвестный billing; нужен квалифицированный provider-side cap |
| Double charge, потерянный POST response | Сохранить attempt и reservation до сети; provider idempotency только если документирована; один writer, unique active job; ambiguity → RECONCILIATION_REQUIRED | Exactly-once недоказуем без remote idempotency/lookup; не делать автоматический второй POST |
| SSRF, небезопасный URL, redirect | Allowlist HTTPS origins/ports; проверять каждый redirect и DNS; deny loopback/private/link-local/metadata IP, userinfo и чужие протоколы; не передавать auth CDN | DNS rebinding требует доверенного network executor, одного pure URL validator недостаточно |
| Подмена download | Связать artifact с job/model/plan; ограничить размер, проверить hash и receipt; staging; своё имя файла | SHA-256 после download фиксирует байты, но не доказывает происхождение без доверенного receipt |
| Вредоносный media / decompression bomb | Sandbox FFprobe/FFmpeg без сети и внешних media protocols; лимиты CPU/RAM/time/disk/streams/duration/resolution; актуальные инструменты; без autoplay | Существующий pipeline не является квалифицированным sandbox |
| TOCTOU, symlink, hardlink, Windows reparse | Private directories, no-follow/handle checks где доступны, stable identity/hash, atomic promotion | Злоумышленник с записью в parent dirs может обойти pure checks; Windows junction/reparse/ACL NOT_RUN |
| Потерянный результат, expired URL, partial file | Durable job ID; ограниченный resume с object validator; temp → verified asset; journal recovery; incomplete evidence явно INCOMPLETE | Истёкший результат может быть невосстановим; новая generation — новый расход и consent |
| Подмена модели / router fallback | Pin точного ID/settings/region; requested/resolved model и quote; mismatch блокирует | Реальную внутреннюю модель без provider attestation проверить нельзя |
| Изменение тарифов/API/terms | Версия и срок capabilities/terms/quotes, recheck перед batch; retirement отключает adapter; новый consent при существенной смене | Sora и Veo preview показывают реальный риск устаревшего каталога |
| Нарушение ToS / account ban | Только официальный разрешённый канал; без CAPTCHA/MFA обхода, cookie extraction, account rotation, hidden API; соблюдать 429 | Arena S08 запрещает web automation; C требует письменного разрешения плюс тест; владелец не отменяет provider terms |
| Коммерческие права не подтверждены | Раздельно output licence, input IP, likeness/voice/music/stock, территория, срок, attribution, watermark, revocation; UNKNOWN → RIGHTS_HOLD | Оплата и ownership не гарантия прав; PixVerse S17 требует письменного clarification; агрегатор добавляет договоры |
| Неполный MP4 / evidence | Полный ограниченный decode, probe/SHA/streams/duration; completion marker после asset commit; ошибка не SUCCESS | Технический PASS не подтверждает художественное качество, синхронизацию или научную достоверность |
| Stale anchor / hostile metadata | Exact project/anchor/input revisions; строки и имена недоверенные, без shell interpolation; CAS attach | Late result остаётся unlinked; local admin вне pure threat boundary |
| Retry amplification | Account queue, max attempts/deadline/budget, backoff+jitter, circuit breaker; moderation terminal | Численные rate limits и стоимость ошибок часто UNKNOWN; infinite retry запрещён |
| Поддельный approval/license label, отзыв | Review ref с actor/time/scope/hash, история изменений; повторная проверка перед export | Нет квалифицированных identity, revocation store и trusted time; это не Production Gate |

## Rights gate — предложение

Фраза commercial use allowed не доказывает права на исходники, чужой голос/образ, музыку, эксклюзивность, sublicense клиенту или охраноспособность AI output. Для каждого asset хранить точные provider/model/channel/plan/terms date/order и лицензионное evidence. UNKNOWN watermark блокирует обещание watermark-free. Не удалять watermark без разрешения. Upscale не снимает ограничения; template-only stock licence может запрещать отдельное использование клипа.

Предлагаемый минимум для final export: документированное разрешение на intended distribution; права на все inputs и согласия на голос/образ; лицензии музыки/stock; territory/time/attribution/watermark checks; reviewer. UNKNOWN разрешён только в явно обозначенном экспериментальном preview/quarantine. D05 остаётся решением владельца. Ни документ, ни checksum, ни платный план не выдают production permissions.

Редакционная пригодность: причина выбора темы, источники к сценарию, claims для научной проверки, обязательные визуальные материалы, остаточные риски, ответственное лицо и точный разрешённый scope. Синтетический видеоряд не документальное доказательство. Первые automated quality scorers могут ставить flags, но не утверждать релиз.

## Windows, storage и доверенная граница

Remote API в принципе не требует GPU для локальной генерации; это не Windows PASS. Windows 10/11 TLS, keyring, PowerShell, Tk, пути с кириллицей/пробелами, процессы, FFmpeg codecs, ACL/reparse и CPU performance **NOT_RUN**. Wan/Kandinsky local CPU не benchmarked; практическая пригодность не обещана.

S3 и production storage не вводятся. Существующий trusted-user hash cache не защищает от hostile writers. Signed evidence, защищённые ACL, доверенные identity/time и revocation требуют отдельной квалификации ОС/executor/storage. Pure contracts могут отклонить отсутствующие refs, expired quote, UNKNOWN rights и недопустимые transitions; они не удостоверяют подлинность лицензии, не запрещают удалённое списание и не изолируют decoder. Нормативные PG/G3.2.1 контракты не меняются.

## Gates — PROPOSAL

G0: exact base/docs-only diff. G1: owner D01–D08. G2: действующие model/terms/region/rights и provider-side spending controls. G3: mock fault conformance с ambiguous submit и no-extra-charge assertions. G4: отдельно разрешённый минимальный live pilot с утверждёнными inputs и cost ceiling. G5: независимые Windows проверки. G6: human visual/listening/editorial acceptance. G7: отдельный будущий production authorization process. Ранний gate не разрешает следующий. G4+ здесь не выполнялись.
