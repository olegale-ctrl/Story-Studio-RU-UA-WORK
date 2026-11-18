# MVP-07 — решение владельца и границы продолжения

Источник: явное решение владельца в задании «MVP-07.1 — Stabilization, Regression Hardening & Owner Approval», полученном 18 ноября 2026 года.

| Объект | Решение владельца |
|---|---|
| MVP-07 | **ACCEPTED_WITH_LIMITATIONS** |
| Windows Acceptance | **WINDOWS_NOT_RUN** |
| MVP-07.1 | **AUTHORIZED_EXPERIMENTAL** |
| MVP-08 | **AUTHORIZED_EXPERIMENTAL** |
| Merge / Release | **STOP** |
| main / CI | **STOP** |
| G3.2.1 | **STOP** |
| Production storage / permissions | **STOP** |

Принятая версия MVP-07: commit `91d274c554433fbc2145d5fc6b6a591199c0243f`, tree `38e2579cc3294fa5cf57b4d1bc267a37bfe078f8`.

Разрешены экспериментальные стабилизация, воспроизведение дефектов, регрессионные тесты, безопасная работа с локальными JSON/preview/FFmpeg и публикация отдельной ветки `fix/story-studio-experimental-mvp-07-1-stabilization` строго от этой базы. Разрешение MVP-08 не означает его реализацию в данной ветке: текущая стадия только MVP-07.1.

Сохраняются ограничения: нет фактической Windows квалификации, human listening / end-to-end editorial acceptance, доверенного production executor/storage и разрешений на выпуск материалов. Старый RC-02 Windows baseline также не объявляется закрытым. Синтетические/локальные тесты и успешный MP4 не являются production permission.

Запрещены merge/release, изменения main/CI/нормативных G3.2.1 contracts, production storage/permissions, автоматическая регистрация сервисов, обход CAPTCHA/MFA, сохранение чужих credentials и реальные платные генерации в обязательных тестах. Правила коммерческого использования моделей/провайдеров не изменяются.

**Каждая следующая стадия требует отдельной независимой приёмки ChatGPT и решения владельца по конкретному commit/tree и пакету доказательств.** После публикации MVP-07.1 — STOP; автоматического перехода к реализации MVP-08 нет.
