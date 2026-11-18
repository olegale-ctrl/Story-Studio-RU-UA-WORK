**Status: PROPOSAL — OWNER REVIEW REQUIRED.** Проверено 2026-11-18 (Europe/Kyiv).

Scope: DOCS_ONLY; экспериментальный MVP. Нет production permissions, реализации, покупок, регистрации, платных запросов, CI, merge или release.

# MVP-08.0 — Provider inventory

## Метод и точность

Дата **2026-11-18 относится к каждой строке и каждому источнику ниже**. H = прочитан официальный документ; M = официальный поисковый фрагмент / частично доступная страница; U = UNVERIFIED. H подтверждает опубликованный текст, а не реальную доступность аккаунту. Отдельные поля одной строки могут иметь разные уровни. UNKNOWN не означает нулевую квоту или отсутствие функции. Никакие generation API не вызывались. Документы не являются юридическим заключением.

A/B/C/D/E/F описывают конкретный канал видеогенерации, а не весь бренд. Все рекомендации имеют статус PROPOSAL. Ссылки [Sxx] раскрыты в реестре источников; дата и уровень в строке распространяются на все её факты. Неустановленные поля перечислены явно; маркетинговый максимум не превращён в API capability.

## Идентичность, модели и технические параметры

| ID / официальный сервис, сайт | Наблюдение / источник / confidence | Вывод и архитектурное влияние |
|---|---|---|
| QW — [Qwen](https://qwen.ai/) web | Video Generation обозначен на главной [S01 M]; модель, T2V/I2V API, максимум, resolution, watermark U: SPA не отдаёт текст | D для web; не связывать Qwen Chat с квотой Alibaba. Нужен отдельный channel ID |
| WA — [Alibaba Cloud Model Studio / Wan](https://www.alibabacloud.com/) | Wan 3.0 API [S05 M]; квалифицируемый legacy Wan 2.1–2.6 [S04 H]: T2V; 2.1 turbo/plus фиксированные 5 s, turbo 480/720p; 2.6 2–15 s, до 1080p. I2V — отдельное семейство [S03 H]; API watermark управляем, console watermark [S06 M] | A **только разовый eligible trial выбранной модели**; далее B. Не суммировать trial разных моделей как ежедневный ресурс |
| AR — [Arena Intelligence / Video Arena](https://arena.ai/) (ранее LMArena) | T2V/I2V; два анонимных результата, обычно 5–8 s, нельзя выбрать модель, resolution/watermark U [S07 H]. Не отождествлять с arena.io или get-arena.ai | D; comparison workflow не production supplier. Новый Arena API [S09 H] текстовый, не доказательство video endpoint |
| KL — [Kling AI](https://kling.ai/) | API guides перечисляют 3.0/3.0 Omni/Turbo [S10 M]; актуальный максимум/разрешение конкретного direct endpoint U (JS shell). T2V/I2V direct specs требуют повторной квалификации; не переносить параметры Kling через Runway на direct API | B (M: официальный paid API документирован). Не выбирать автоматически до чтения полного endpoint contract |
| PX — [PixVerse](https://pixverse.ai/) | V6/C1/V6 Max API [S13 H]; V6 T2V/I2V, 1–15 s, 360/540/720/1080p [S14 M/H]. Watermark U на выбранном direct API | B, H. Поля audio/reference меняют цену. Commercial gate не закрыт |
| MM — [MiniMax / Hailuo](https://www.minimax.io/) / [Hailuo web](https://hailuoai.video/) | MiniMax-H3, T2V/I2V/reference; 4–15 s, 768P/2K [S19 H]. Price sheet также H3 Highspeed/Lite/Max [S20 H], их specs отдельно U. Hailuo consumer entitlement не API | B, H. Использовать прямую platform.minimax.io, не похожие minimax.movie / h3minimax.com |
| RW — [Runway](https://runway.com/) / [Runway Dev](https://dev.runwayml.com/) | Gen-4.5 и multi-provider Wan/Kling/Seedance в API [S23 H]; T2V/I2V async examples [S25 H]. Максимум/разрешение Gen-4.5 endpoint U в этой проверке; не выводить из примера | B, H; фиксировать requested и resolved model. Model Router не должен незаметно менять утверждённый scope |
| RF — [Renderforest](https://www.renderforest.com/) | Fast/Pro и партнёрские модели, T2V/I2V web [S29 M]; help Fast 4–10 s [S30 H], marketing whole-video до 12 min [S29 M] — разные объекты. HD720 free marketing [S31 H/M], direct AI API specs U | B для template-render API [S32 H]; **D для web AI clip**, F для AI-clip API. Не выдавать template API за генеративный endpoint |
| FB — [FusionBrain](https://fusionbrain.ai/) / Kandinsky | FusionBrain homepage/API docs 502 [S34 U]. [Kandinsky Lab](https://kandinskylab.ai/) 6.0 Lite/Pro T2V/I2V 5 s, заявлен Full HD; Lite native SD + upscale; 5.0 legacy до 10 s [S35 H] | F для FusionBrain hosted video API. Открытая модель не доказывает бесплатный hosted API или Windows CPU throughput |
| BH — [BotHub](https://bothub.chat/) | Видео API T2V/I2V, async ID/status/unsigned_urls MP4 [S36 H]; Kling 4.0 добавлен 11 Nov [S37 H/M]. Каталог Wan/Hailuo/Runway и цены [S38 M], endpoint-specific max/resolution/watermark U | B, H для paid video workflow. Агрегатор — дополнительный processor и отдельные model rights |
| GF — [Google Flow](https://labs.google/flow/about) | Web: Omni Flash 1.2/Veo 3.1 Lite; Lite 4/6/8 s 720p, Omni до 10 s free, до 15 s subscriber [S40 H]. Не API credit pool | D; manual fallback. Декабрьские retirement notices требуют expiry у catalog observations |
| GO — [Google Gemini API / Omni Flash](https://aistudio.google.com/) | Omni 1.2 T2V/I2V/video editing, 3–15 s, 360/720p; 1080p/4K upscale; API MP4 bytes [S41 H]. Veo preview API закрыт 22 Oct, GA другой канал [S42 H] | B, H [S43]. Не создавать новый adapter на уже закрытый preview |
| SO — [OpenAI ChatGPT / Sora](https://openai.com/) | Web/app закрыты 26 Apr 2026, API 24 Sep 2026 [S45 H]; historical sora-2 listings не актуальная availability | E для Sora video generation. ChatGPT subscription не предоставляет обхода закрытия; ChatGPT text/image не video capability |

## Квоты и цена (каналы нельзя смешивать)

| ID | Бесплатный web; старт / day / month | API free / стоимость | Evidence, вывод, impact |
|---|---|---|---|
| QW | UNVERIFIED / UNKNOWN / UNKNOWN | Free video API не подтверждён; price U | S01–02 M/U; не обещать daily refill |
| WA | Qwen web отдельно U | 50 s разово для wan2.1-t2v-turbo International Singapore; $0.036/s после trial; 90-day expiry. Daily/monthly refill **не заявлен**. wan2.6 free=None | S03 H, S48 H; Free Quota Only по умолчанию выключен — опасность auto PAYG |
| AR | Login, 2 generations / rolling 24 h; оба результата в battle; start/month U | Text API есть, бесплатный video API **не доказан** | S07–09 H; неоднозначность generation/request не считать 4 гарантированных downloads/day |
| KL | Start/day/month U | Paid resource packages, exact price U | S10–12 M/U; trial package нельзя объявить daily free API |
| PX | Web Basic существует; текущие start/day/month U | Free API entitlement U; 225 credits/$1, V6 silent720p 9 credits/s=$0.04/s,1080p18=$0.08/s | S13 H, S15 H; web subscription не API credits |
| MM | Hailuo start/day/month U | H3 PAYG; 768P $0.08/s,2K $0.13/s; reference video input дополнительно, image allowance ≠ video trial | S19–20 H; никакой daily free API throughput не установлен |
| RW | 125 **one-time** web credits; daily/monthly free не заявлены | API paid, $0.01/credit, минимум пополнения $10; rates model-specific, Wan3 720p10 credits/s | S23–24 H, S26 H; free web balance не API balance |
| RF | Противоречие: free unlimited HD marketing vs help Pro/Business only Fast zero-credit; start/day/month U | API render требует active subscription; тестовый ключ по запросу не разрешает render | S29–32 H/M; FREE_UNVERIFIED, не считать unlimited supply |
| FB | Hosted trial/day/month/price U | Video API/free quota U | S34 U; RESEARCH_BLOCKED_SOURCE_ACCESS |
| BH | Free video start/day/month U | Paid usage/caps в video response; точный текущий model rate M: Wan3 $0.08/s, Kling4 $0.24/s catalog; не ценовое обещание | S36 H, S38 M; перед submit точная quote/ledger |
| GF | 50 credits/day, first-generation reset, no rollover; subscriber monthly extras separate | API бесплатно этим балансом не доказан; Veo Lite web10credits/generation non-Ultra | S40 H; UI-only accounting, не dispatcher quota |
| GO | Flow отдельно | Free Tier unavailable; Omni1.2 output720p 5792tokens/s×$12/M≈$0.069504/s **плюс input** | S43 H; pricing unit token, нельзя считать flat all-in second |
| SO | Недоступно для новой generation | Недоступно | S45 H; нулевая новая automatic capacity |

## Условия, регионы, rights и automation

Для **всех** каналов фактическая eligibility данного аккаунта, местонахождение, платёжные ограничения и разрешения на конкретные исходные материалы **UNVERIFIED**: аккаунты не создавались и не проверялись. RU/UA — языки проекта, не доказательство местонахождения. Запрещены VPN/аккаунтные обходы. Автоматический download и async в следующей таблице — только документированные возможности, **NOT_RUN** технически. Успешные retries, отмена и exactly-once charging нигде не доказаны.

| ID | Terms / rights / region observation | Async, MP4, limits, retries / permission | Вывод / impact |
|---|---|---|---|
| QW | S02 M/U, полный terms текст недоступен; commercial/regions U | Web automation permission U; video jobs/download/rate limits U | D; только ручной резерв, rights hold |
| WA | S46 M: input/output clauses, no rights guarantee; region ключа=model=endpoint S04 H | Task ID/poll/video_url MP4 S04 H; numeric limits U; GET retry bounded, submit semantics U | Trial A условен eligibility; commercial clearance отдельно, no automatic spend |
| AR | S08 H §1 internal/personal, §3 ownership не blanket commercial grant, §5 запрет automated access/scraping; третьи model terms | S07 H login/vote, до10min; download-all и export rights U. Text API docs не снимают video web ban | D, **NO WEB AUTOMATION**; не использовать как поставщика для финального фильма без отдельного разрешения |
| KL | S12 M paid API terms commercial use не restricted, IP-risk остаётся; regions U | Official API packages S10 M; async/download/rate/retry full contract U из-за JS shell | B documentary; RESEARCH_BLOCKED_SOURCE_ACCESS для direct specs/legal полного текста |
| PX | S16 H web paid PixVerse models only; S17 H §1.4 written commercial authorization vs §5.3 commercial allowed; S18 M order precedence | ID/poll3–5s/output URL S21 H; account concurrency unknown,500044/backoff S22 H; MP4 download format NOT_RUN | B technical, rights hold до письменного clarification/order. Не разрешать advertising по одному §5.3 |
| MM | S28 M/U input authorization, sanctioned regions включают Crimea/Sevastopol и указанные Donetsk/Luhansk территории; commercial exact grant U | S19 H async task_id/content.url download; numeric rate/cancel/idempotency U | B; data/rights review; запрет трактовать open weights как hosted terms |
| RW | S27 H commercial output не restricted при соблюдении terms; input/output training licence; actual region U | S25 H async task/output; rate tier численно U; cancel/refund U; format verification needed | B; private prompts требуют отдельной оценки; не отправлять secrets |
| RF | S33 H paid commercial/reselling tier ограничения; stock use внутри template не standalone licence | S32 H template render/status/download URLs;60requests/5min; no render без subscription; generative endpoint U | Template B не first-wave clip supplier; rights и free conflict hold |
| FB | S34 U terms/regions/commercial licence/hosted spec недоступны; S35 product не proof FusionBrain API | Hosted async/download/rate/retry/automation U | F; RESEARCH_BLOCKED_SOURCE_ACCESS; self-host option требует hardware+licence audit |
| BH | S39 M terms найдены, specific sublicensing/regions U; underlying model grant не доказан catalog price | S36 H submit/poll10–15s/MP4 URLs; numeric rate/cancel/retry/doublecharge U | B documentary; privacy + model rights + API country access gates |
| GF | Terms/commercial specific entitlement/region eligibility U в этой проверке | S40 H daily UI+peak limits; download-all/permission unattended U | D; no free API assumption |
| GO | Paid API docs H; terms/region entitlement конкретного project U | S41 H programmatic MP4 bytes, async/background/cancel/rate perselectedmode U | B; adapter допускает bytes или remote artifact, а не только URL jobs |
| SO | S45 H sunset; historical rights не grant для нового generation | No current service; retries/download of **new** jobs N/A | E; исключить из selection; старые assets отдельно provenance/rights |

## Реестр официальных источников

Все checked **2026-11-18**. H/M/U здесь относится к доступу к источнику; exact field confidence выше имеет приоритет. Search-index M не заменяет полный договор. URLs — evidence references, не endpoints для запуска запросов. Никакие неофициальные API из поисковой выдачи не использованы.

| Ref | Source | Access / evidence locator |
|---|---|---|
| S01 | https://qwen.ai/ | M indexed video heading; direct open zero readable lines |
| S02 | https://qwen.ai/termsservice | M indexed identity; U full text, zero lines |
| S03 | https://www.alibabacloud.com/help/en/model-studio/model-pricing | H updated Nov18; Wan-T2V Singapore table: turbo50s, newer None; historical index противоречит current table |
| S04 | https://www.alibabacloud.com/help/en/model-studio/legacy-wan-text-to-video-api-reference | H Availability; duration; create task; video_url |
| S05 | https://www.alibabacloud.com/help/en/model-studio/wan3-video-generation-api-reference/ | M indexed Wan3; not qualified model limit |
| S06 | https://www.alibabacloud.com/help/en/model-studio/use-video-generation/ | M indexed console/API watermark distinction |
| S07 | https://help.arena.ai/articles/1544829667-how-to-create-videos-with-video-arena | H Web Notes + steps; 2/24h, anonymous pair,5–8s |
| S08 | https://help.arena.ai/articles/5629909088-terms-of-use | H dated Feb23 2026; §§1,3,5 |
| S09 | https://platform.arena.ai/docs/api | H method list chat/responses/messages/models; no video endpoint in document |
| S10 | https://kling.ai/document-api/quickStart/userManual | M indexed purchase resource packages; direct JS shell |
| S11 | https://kling.ai/document-api/productBilling/billingMethod | M indexed paid table; U extracted rates (one-line shell) |
| S12 | https://kling.ai/document-api/protocols/paidServiceProtocol | M official indexed §6.4; full legal reading pending |
| S13 | https://docs.platform.pixverse.ai/pixverse-api-pricing-2394995m0 | H Billing Overview / V6 table |
| S14 | https://docs.platform.pixverse.ai/v6-released-2056814m0 | M official indexed duration; S14b https://docs.platform.pixverse.ai/text-to-video-13016634e0 H request example |
| S15 | https://docs.platform.pixverse.ai/ | H Billing and Usage, ledger and separate API credits |
| S16 | https://pixverse.ai/en/terms-of-service | H §4 commercial paid/PixVerse-developed models |
| S17 | https://pixverse.ai/en/pixverse-platform-terms-of-service | H §§1.4,5.3 apparent commercial conflict |
| S18 | https://pixverse.ai/en/pixverse-platform-terms-of-paid-services | M official indexed precedence / order document |
| S19 | https://platform.minimax.io/docs/guides/video-generation | H Specs, workflow; H3 PAYG |
| S20 | https://platform.minimax.io/docs/pricing/overview | H Video Generation tables |
| S21 | https://docs.platform.pixverse.ai/query-task-status-2394991m0 | H ID, status1/url, poll3–5s |
| S22 | https://docs.platform.pixverse.ai/concurrency-rules-2394990m0 | H 500044, backoff; numeric entitlement U |
| S23 | https://docs.dev.runwayml.com/guides/pricing/ | H $0.01/credit; model-specific rate table |
| S24 | https://docs.dev.runwayml.com/guides/setup/ | H/M indexed minimum$10; full page accessible |
| S25 | https://docs.dev.runwayml.com/guides/using-the-api/ | H async video examples; no live task |
| S26 | https://runway.com/pricing | H Free125 one-time; consumer plans |
| S27 | https://runway.com/terms-of-use | H Oct23 2026; ownership/commercial/training clauses |
| S28 | https://platform.minimax.io/protocol/terms-of-service | M indexed authorization/sanction clauses; U full extracted text (zero lines) |
| S29 | https://www.renderforest.com/ai-video-generator | M official indexed HD/free/12min marketing |
| S30 | https://help.renderforest.com/support/solutions/articles/72000662238--unlimited-free-ai-video-generation-a-step-by-step-guide- | H Sep23; Pro/Business note;4–10sFast |
| S31 | https://www.renderforest.com/subscription/ | H/M official pricing accessible, free HD720 marketing; not evidence API inclusion |
| S32 | https://developers.renderforest.com/ | H subscription/key/render/status/URLs/rate60per5min |
| S33 | https://www.renderforest.com/terms-and-conditions | H commercial tier/reselling and stock restrictions |
| S34 | https://fusionbrain.ai/ ; https://fusionbrain.ai/docs/doc/api-dokumentaciya/ ; https://fusionbrain.ai/docs/ru/doc/api-dokumentaciya/ | U:502,502,inaccessible respectively; RESEARCH_BLOCKED_SOURCE_ACCESS |
| S35 | https://kandinskylab.ai/models/video/ | H 6.0/5.0 product specs; not hosted service API proof |
| S36 | https://bothub.chat/api/documentation/ru/generation/video_generation | H POST videos/generations; GET videos/id; completed/payment/caps/unsigned_urls |
| S37 | https://bothub.chat/blog/bothub-release-notes--november-11-2026 | H official release, Kling4 API support |
| S38 | https://bothub.chat/models?type=video | M official indexed pricing; direct timeout; RESEARCH_BLOCKED_SOURCE_ACCESS for complete rate card |
| S39 | https://bothub.chat/terms | M indexed agreement; exact video sublicensing U |
| S40 | https://support.google.com/flow/answer/16526234?hl=en | H daily/reset/model costs and retirement notices |
| S41 | https://aistudio.google.com/docs/omni | H model/control/resolution/MP4 bytes examples |
| S42 | https://ai.google.dev/gemini-api/docs/video | H redirected https://aistudio.google.com/docs/video; preview sunset notice |
| S43 | https://aistudio.google.com/docs/pricing | H Omni1.2 paid tier, token rates/output conversion |
| S44 | https://developers.openai.com/api/docs/deprecations | H/M indexed Sep24 Sora shutdown corroboration |
| S45 | https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation | H dates and legacy export separate from generation |
| S46 | https://www.alibabacloud.com/help/en/legal/latest/alibaba-cloud-international-website-product-terms-of-service-v-3-8-0 | M official indexed Model Studio clauses; exact commercial clearance unresolved |
| S47 | https://docs.dev.runwayml.com/guides/outputs/ | U inaccessible; URL-output lifetime not established; RESEARCH_BLOCKED_SOURCE_ACCESS |
| S48 | https://www.alibabacloud.com/help/en/model-studio/new-free-quota | H updated Nov16; Singapore International eligibility, 90 days, auto PAYG, Free Quota Only default disabled |

Неполная проверка regional policies, full legal text и account entitlements отражена как U, а не как подтверждение глобального доступа. Для обязательных провайдеров выполнен поиск официальных документов; наличие блокировки исследования — допустимый результат, не PASS использования сервиса.
