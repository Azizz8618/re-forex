# 04. Экстракоды в аннотированных МАДЛЕН-текстах

Источники расшифровок: **rukava.be**, раздел 1.4 «ПЕРЕЧЕНЬ СИСТЕМНЫХ ВЫЗВОВ (ЭКСТРАКОДОВ)» (`/home/azizz/Yandex.Disk/re-dispak/rukava.be`, строки 2967–3198) — первичный; и **Тюрин В. Ф., «Операционная система ДИСПАК», 1985** (`docs/tyurin1985/extract-codes.json`, OCR Приложения П и §2.4) — вторичный. Приоритет: `rukava.be`, затем Тюрин. Оба источника параметризованы в `tools/extract_codes.py` (`--source rukava|tyurin|all`).

Просканировано 51 аннотированный файл (`src/*.mad`, `src/lib21/*.mad`). Найдено **612 вхождений** экстракодов с информационным словом, **297 уникальных пар**: **5 пар расшифровано по rukava.be** (7 применений), **73 пар расшифровано по Тюрину-1985** (113 применений), **219 пар остались нерасшифрованными** (492 применений).

Всего в таблице rukava.be: 185 строк, 173 уникальных ключа (дублирующиеся строки `Э71 А`, `Э72 А`, `Э73 А` объединены описаниями). В таблице Тюрина-1985: 74 записи (PDF-страницы 264–335); для кодов, у которых конкретное информационное слово в книге отсутствует, используется описание класса экстракодов по номеру кода (fallback).

## Коды, встречающиеся в аннотациях

| Код | Информационное слово | Расшифровка (rukava.be) | Стр. | Применений | Путь:строка |
|-----|----------------------|--------------------------|------|------------|-------------|
| Э36 | 75551 | **не найдено в rukava.be** | — | 24 | `src/LO_SYN.mad:838`, `src/LO_SYN.mad:865`, `src/LO_SYN.mad:940`, `src/LO_SYN.mad:1069`, `src/LO_SYN.mad:1144`, `src/LO_SYN.mad:1978`, `src/LO_SYN.mad:2017`, `src/LO_SYN.mad:2104`, `src/LO_SYN.mad:2197`, `src/LO_SYN.mad:2227` … (ещё 14) |
| Э20 | 42440 | **не найдено в rukava.be** | — | 19 | `src/LO_SYN.mad:1585`, `src/LO_SYN.mad:1865`, `src/LO_SYN.mad:2002`, `src/LO_SYN.mad:2183`, `src/LO_SYN.mad:2240`, `src/LO_SYN.mad:2264`, `src/LO_SYN.mad:2287`, `src/LO_SYN.mad:2411`, `src/LO_SYN.mad:2425`, `src/LO_SYN.mad:2476` … (ещё 9) |
| Э65 | 2151 | **не найдено в rukava.be** | — | 19 | `src/LO_SYN.mad:883`, `src/LO_SYN.mad:1237`, `src/LO_SYN.mad:1249`, `src/LO_SYN.mad:1300`, `src/LO_SYN.mad:1333`, `src/LO_SYN.mad:1378`, `src/LO_SYN.mad:1405`, `src/LO_SYN.mad:1447`, `src/LO_SYN.mad:1597`, `src/LO_SYN.mad:1684` … (ещё 9) |
| Э20 | 42544 | **не найдено в rukava.be** | — | 18 | `src/LO_SYN.mad:880`, `src/LO_SYN.mad:1234`, `src/LO_SYN.mad:1246`, `src/LO_SYN.mad:1297`, `src/LO_SYN.mad:1330`, `src/LO_SYN.mad:1375`, `src/LO_SYN.mad:1402`, `src/LO_SYN.mad:1444`, `src/LO_SYN.mad:1594`, `src/LO_SYN.mad:1681` … (ещё 8) |
| Э36 | 70131 | **не найдено в rukava.be** | — | 18 | `src/LO_SYN.mad:881`, `src/LO_SYN.mad:1235`, `src/LO_SYN.mad:1247`, `src/LO_SYN.mad:1298`, `src/LO_SYN.mad:1331`, `src/LO_SYN.mad:1376`, `src/LO_SYN.mad:1403`, `src/LO_SYN.mad:1445`, `src/LO_SYN.mad:1595`, `src/LO_SYN.mad:1682` … (ещё 8) |
| Э36 | 52103 | **не найдено в rukava.be** | — | 17 | `src/LO_SYN.mad:892`, `src/LO_SYN.mad:913`, `src/LO_SYN.mad:1009`, `src/LO_SYN.mad:1042`, `src/LO_SYN.mad:1102`, `src/LO_SYN.mad:1192`, `src/LO_SYN.mad:1201`, `src/LO_SYN.mad:1264`, `src/LO_SYN.mad:1363`, `src/LO_SYN.mad:1390` … (ещё 7) |
| Э65 | 2040 | **не найдено в rukava.be** | — | 9 | `src/LO_SYN.mad:946`, `src/LO_SYN.mad:974`, `src/LO_SYN.mad:998`, `src/LO_SYN.mad:1453`, `src/LO_SYN.mad:1463`, `src/LO_SYN.mad:1964`, `src/LO_SYN.mad:2666`, `src/LO_SYN.mad:2933`, `src/LO_SYN.mad:3068` |
| Э47 | 4520 | **не найдено в rukava.be** | — | 8 | `src/LO_SYN.mad:1958`, `src/LO_SYN.mad:1999`, `src/LO_SYN.mad:2140`, `src/LO_SYN.mad:2204`, `src/LO_SYN.mad:2372`, `src/LO_SYN.mad:2591`, `src/LO_SYN.mad:2626`, `src/LO_SYN.mad:2977` |
| Э36 | 61113 | **не найдено в rukava.be** | — | 7 | `src/LO_SYN.mad:1051`, `src/LO_SYN.mad:1139`, `src/LO_SYN.mad:1187`, `src/LO_SYN.mad:1486`, `src/LO_SYN.mad:1520`, `src/LO_SYN.mad:1616`, `src/LO_SYN.mad:1667` |
| Э64 | IP028 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 7 | `src/lib21/OCATALOG.mad:113`, `src/lib21/OCATALOG.mad:128`, `src/lib21/OCATALOG.mad:172`, `src/lib21/OCATALOG.mad:184`, `src/lib21/OCATALOG.mad:187`, `src/lib21/OCATALOG.mad:197`, `src/lib21/OCATALOG.mad:233` |
| Э65 | 2120 | **не найдено в rukava.be** | — | 6 | `src/LO_SYN.mad:2095`, `src/LO_SYN.mad:2408`, `src/LO_SYN.mad:2524`, `src/LO_SYN.mad:3208`, `src/LO_SYN.mad:3245`, `src/LO_SYN.mad:3308` |
| Э67 | 151 | **не найдено в rukava.be** | — | 6 | `src/LO_SYN.mad:1982`, `src/LO_SYN.mad:2444`, `src/LO_SYN.mad:2560`, `src/LO_SYN.mad:2579`, `src/LO_SYN.mad:2798`, `src/LO_SYN.mad:2810` |
| Э70 | BUF075 | **не найдено в rukava.be** | — | 6 | `src/lib21/LIBDRU_.mad:137`, `src/lib21/LIBDRU_.mad:167`, `src/lib21/LIBDRU_.mad:196`, `src/lib21/LIBDRU_.mad:222`, `src/lib21/LIBDRU_.mad:419`, `src/lib21/LIBDRU_.mad:521` |
| Э20 | 40440 | **не найдено в rukava.be** | — | 5 | `src/LO_SYN.mad:2275`, `src/LO_SYN.mad:2311`, `src/LO_SYN.mad:2329`, `src/LO_SYN.mad:2452`, `src/LO_SYN.mad:2867` |
| Э20 | 62113 | **не найдено в rukava.be** | — | 5 | `src/LO_SYN.mad:1577`, `src/LO_SYN.mad:1757`, `src/LO_SYN.mad:1862`, `src/LO_SYN.mad:1972`, `src/LO_SYN.mad:2836` |
| Э36 | 42440 | **не найдено в rukava.be** | — | 5 | `src/LO_SYN.mad:1679`, `src/LO_SYN.mad:2458`, `src/LO_SYN.mad:2887`, `src/LO_SYN.mad:3184`, `src/LO_SYN.mad:3238` |
| Э36 | 66166 | **не найдено в rukava.be** | — | 5 | `src/LO_SYN.mad:2273`, `src/LO_SYN.mad:2309`, `src/LO_SYN.mad:2327`, `src/LO_SYN.mad:2866`, `src/LO_SYN.mad:3092` |
| Э36 | 66170 | **не найдено в rukava.be** | — | 5 | `src/LO_SYN.mad:932`, `src/LO_SYN.mad:1031`, `src/LO_SYN.mad:1063`, `src/LO_SYN.mad:3053`, `src/LO_SYN.mad:3149` |
| Э47 | 4524 | **не найдено в rukava.be** | — | 5 | `src/LO_SYN.mad:2188`, `src/LO_SYN.mad:2276`, `src/LO_SYN.mad:2312`, `src/LO_SYN.mad:2330`, `src/LO_SYN.mad:2869` |
| Э57 | 6 | ВЫДЕЛЕНИЕ ЦЕЛОЙ ЧАСТИ (ENTIER) / СИСТЕМНАЯ ОПЕРАЦИЯ (ИР 057 A) [tyurin1985] | 264 | 5 | `src/FOREX_CORE.mad:197`, `src/FOREX_CORE.mad:199`, `src/FOREX_CORE.mad:256`, `src/lib21/FOREX_.mad:58`, `src/lib21/FOREX_.mad:83` |
| Э64 | 5505 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 5 | `src/LO_SYN.mad:1984`, `src/LO_SYN.mad:2446`, `src/LO_SYN.mad:2581`, `src/LO_SYN.mad:2800`, `src/LO_SYN.mad:2812` |
| Э64 | INF093 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 5 | `src/lib21/MAKELIBT.mad:372`, `src/lib21/MAKELIBT.mad:743`, `src/lib21/MAKELIBT.mad:853`, `src/lib21/MAKELIBT.mad:857`, `src/lib21/MAKELIBT.mad:863` |
| Э66 | 4513 | **не найдено в rukava.be** | — | 5 | `src/LO_SYN.mad:2297`, `src/LO_SYN.mad:2305`, `src/LO_SYN.mad:2323`, `src/LO_SYN.mad:2647`, `src/LO_SYN.mad:3254` |
| Э67 | 440 | **не найдено в rukava.be** | — | 5 | `src/LO_SYN.mad:1130`, `src/LO_SYN.mad:1178`, `src/LO_SYN.mad:1219`, `src/LO_SYN.mad:3079`, `src/LO_SYN.mad:3100` |
| Э20 | 41524 | **не найдено в rukava.be** | — | 4 | `src/LO_SYN.mad:952`, `src/LO_SYN.mad:1730`, `src/LO_SYN.mad:2815`, `src/LO_SYN.mad:3047` |
| Э20 | 52040 | **не найдено в rukava.be** | — | 4 | `src/LO_SYN.mad:878`, `src/LO_SYN.mad:1207`, `src/LO_SYN.mad:1211`, `src/LO_SYN.mad:1796` |
| Э20 | 64505 | **не найдено в rukava.be** | — | 4 | `src/LO_SYN.mad:1739`, `src/LO_SYN.mad:3188`, `src/LO_SYN.mad:3242`, `src/LO_SYN.mad:3283` |
| Э36 | 20040 | **не найдено в rukava.be** | — | 4 | `src/LO_SYN.mad:901`, `src/LO_SYN.mad:2233`, `src/LO_SYN.mad:2257`, `src/LO_SYN.mad:2965` |
| Э36 | 50115 | **не найдено в rukava.be** | — | 4 | `src/LO_SYN.mad:1037`, `src/LO_SYN.mad:1079`, `src/LO_SYN.mad:1154`, `src/LO_SYN.mad:1529` |
| Э36 | 63517 | **не найдено в rukava.be** | — | 4 | `src/LO_SYN.mad:2378`, `src/LO_SYN.mad:2924`, `src/LO_SYN.mad:3001`, `src/LO_SYN.mad:3011` |
| Э36 | 70120 | **не найдено в rukava.be** | — | 4 | `src/LO_SYN.mad:1435`, `src/LO_SYN.mad:1798`, `src/LO_SYN.mad:2288`, `src/LO_SYN.mad:2960` |
| Э36 | 7417 | **не найдено в rukava.be** | — | 4 | `src/FOREX_CORE.mad:333`, `src/FOREX_CORE.mad:347`, `src/FOREX_CORE.mad:377`, `src/FOREX_CORE.mad:380` |
| Э64 | 2554 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 4 | `src/LO_SYN.mad:994`, `src/LO_SYN.mad:1573`, `src/LO_SYN.mad:1678`, `src/LO_SYN.mad:2999` |
| Э72 | ICC104 | **не найдено в rukava.be** | — | 4 | `src/lib21/OVERLOAD.mad:708`, `src/lib21/OVERLOAD.mad:772`, `src/lib21/OVERLOAD.mad:866`, `src/lib21/OVERLOAD.mad:874` |
| Э20 | 20040 | **не найдено в rukava.be** | — | 3 | `src/LO_SYN.mad:1244`, `src/LO_SYN.mad:2180`, `src/LO_SYN.mad:2512` |
| Э20 | 20143 | **не найдено в rukava.be** | — | 3 | `src/LO_SYN.mad:2126`, `src/LO_SYN.mad:2362`, `src/LO_SYN.mad:2386` |
| Э20 | 42502 | **не найдено в rukava.be** | — | 3 | `src/LO_SYN.mad:3181`, `src/LO_SYN.mad:3202`, `src/LO_SYN.mad:3235` |
| Э20 | 42503 | **не найдено в rukava.be** | — | 3 | `src/LO_SYN.mad:904`, `src/LO_SYN.mad:964`, `src/LO_SYN.mad:2542` |
| Э20 | 44040 | **не найдено в rukava.be** | — | 3 | `src/LO_SYN.mad:1228`, `src/LO_SYN.mad:1276`, `src/LO_SYN.mad:1340` |
| Э36 | 46440 | **не найдено в rukava.be** | — | 3 | `src/LO_SYN.mad:1643`, `src/LO_SYN.mad:2254`, `src/LO_SYN.mad:2704` |
| Э36 | 47524 | **не найдено в rukava.be** | — | 3 | `src/LO_SYN.mad:905`, `src/LO_SYN.mad:965`, `src/LO_SYN.mad:2543` |
| Э36 | 52102 | **не найдено в rukava.be** | — | 3 | `src/LO_SYN.mad:1352`, `src/LO_SYN.mad:1834`, `src/LO_SYN.mad:2075` |
| Э36 | 65040 | **не найдено в rukava.be** | — | 3 | `src/LO_SYN.mad:1889`, `src/LO_SYN.mad:2435`, `src/LO_SYN.mad:3196` |
| Э36 | 66040 | **не найдено в rukava.be** | — | 3 | `src/LO_SYN.mad:1712`, `src/LO_SYN.mad:2060`, `src/LO_SYN.mad:2090` |
| Э56 | 70000 | EXP (ИР 056 A) [tyurin1985] | 264 | 3 | `src/FOREX_CORE.mad:363`, `src/FOREX_CORE.mad:368`, `src/LO_SYN.mad:770` |
| Э63 | CN677 | ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A) [tyurin1985] | 334 | 3 | `src/lib21/FT_REGIM.mad:90`, `src/lib21/FT_REGIM.mad:149`, `src/lib21/FT_REGIM.mad:161` |
| Э65 | 502 | **не найдено в rukava.be** | — | 3 | `src/lib21/CHEKJOB_.mad:339`, `src/lib21/CHEKJOB_.mad:444`, `src/lib21/INPUTCAL.mad:124` |
| Э70 | BUF077 | **не найдено в rukava.be** | — | 3 | `src/lib21/LIBDRU_.mad:250`, `src/lib21/LIBDRU_.mad:432`, `src/lib21/LIBDRU_.mad:465` |
| Э70 | BUF083 | **не найдено в rukava.be** | — | 3 | `src/lib21/LIBTAP_.mad:163`, `src/lib21/LIBTAP_.mad:195`, `src/lib21/LIBTAP_.mad:560` |
| Э70 | BUF132 | **не найдено в rukava.be** | — | 3 | `src/lib21/MAKELIBT.mad:285`, `src/lib21/MAKELIBT.mad:289`, `src/lib21/MAKELIBT.mad:616` |
| Э70 | PLA078 | **не найдено в rukava.be** | — | 3 | `src/lib21/LIBTAP_.mad:508`, `src/lib21/LIBTAP_.mad:569`, `src/lib21/LIBTAP_.mad:576` |
| Э20 | 20102 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:2189`, `src/LO_SYN.mad:3034` |
| Э20 | 20103 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:2314`, `src/LO_SYN.mad:2870` |
| Э20 | 20115 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:1166`, `src/LO_SYN.mad:2534` |
| Э20 | 20117 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:2278`, `src/LO_SYN.mad:3118` |
| Э20 | 40561 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:1727`, `src/LO_SYN.mad:2405` |
| Э20 | 64543 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:2135`, `src/LO_SYN.mad:2828` |
| Э36 | 20143 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:1721`, `src/LO_SYN.mad:2861` |
| Э36 | 20151 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:1591`, `src/LO_SYN.mad:2351` |
| Э36 | 41117 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:889`, `src/LO_SYN.mad:1603` |
| Э36 | 41124 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:1931`, `src/LO_SYN.mad:2348` |
| Э36 | 41524 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:2011`, `src/LO_SYN.mad:3059` |
| Э36 | 41554 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:1424`, `src/LO_SYN.mad:1699` |
| Э36 | 44103 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:3062`, `src/LO_SYN.mad:3269` |
| Э36 | 50110 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:1933`, `src/LO_SYN.mad:2350` |
| Э36 | 50530 | **не найдено в rukava.be** | — | 2 | `src/LO_GEN.mad:635`, `src/LO_GEN.mad:670` |
| Э36 | 52113 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:1046`, `src/LO_SYN.mad:1612` |
| Э36 | 61117 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:910`, `src/LO_SYN.mad:2548` |
| Э36 | 70105 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:2021`, `src/LO_SYN.mad:2078` |
| Э36 | 70151 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:1417`, `src/LO_SYN.mad:1690` |
| Э36 | 73105 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:2216`, `src/LO_SYN.mad:3286` |
| Э46 | 74513 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:1075`, `src/LO_SYN.mad:1150` |
| Э47 | 4576 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:970`, `src/LO_SYN.mad:2249` |
| Э50 | 67 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) [tyurin1985] | 264 | 2 | `src/FOREX_DECODER_DISASM.mad:156`, `src/lib21/LIBTAP_.mad:395` |
| Э57 | 1263 | ВЫДЕЛЕНИЕ ЦЕЛОЙ ЧАСТИ (ENTIER) / СИСТЕМНАЯ ОПЕРАЦИЯ (ИР 057 A) [tyurin1985] | 264 | 2 | `src/FOREX_CORE.mad:362`, `src/LO_SYN.mad:769` |
| Э57 | 4000 | ВЫДЕЛЕНИЕ ЦЕЛОЙ ЧАСТИ (ENTIER) / СИСТЕМНАЯ ОПЕРАЦИЯ (ИР 057 A) [tyurin1985] | 264 | 2 | `src/lib21/BEMSH_.mad:201`, `src/lib21/LINK#IPM.mad:244` |
| Э62 | 102 | ОТМЕНА РЕЖИМА ПРИЕМА С ТЕРМИНАЛА И ПЕРЕХОД В РЕЖИМ ВЫВОДА | ? | 2 | `src/LO_SYN.mad:1864`, `src/LO_SYN.mad:1973` |
| Э63 | 502 | ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A) [tyurin1985] | 334 | 2 | `src/lib21/CHEKJOB_.mad:201`, `src/lib21/LUNTYP.mad:60` |
| Э63 | 7 | ЗАПРОС СВЕДЕНИЙ ОБ ОБЛАСТИ | ? | 2 | `src/lib21/CHEKJOB_.mad:192`, `src/lib21/CHEKJOB_.mad:247` |
| Э63 | CN766 | ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A) [tyurin1985] | 334 | 2 | `src/lib21/EXECUTE.mad:120`, `src/lib21/EXECUTE.mad:261` |
| Э64 | 1101 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 2 | `src/LO_SYN.mad:2099`, `src/LO_SYN.mad:2120` |
| Э64 | 1551 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 2 | `src/LO_SYN.mad:1370`, `src/LO_SYN.mad:1742` |
| Э64 | 510 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 2 | `src/LO_SYN.mad:1418`, `src/LO_SYN.mad:1691` |
| Э64 | 5517 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 2 | `src/LO_SYN.mad:1549`, `src/LO_SYN.mad:2720` |
| Э64 | 7504 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 2 | `src/LO_SYN.mad:2756`, `src/LO_SYN.mad:2777` |
| Э64 | 7515 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 2 | `src/LO_SYN.mad:1382`, `src/LO_SYN.mad:1940` |
| Э64 | 77440 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 2 | `src/LO_SYN.mad:2878`, `src/LO_SYN.mad:3224` |
| Э64 | 77524 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 2 | `src/LO_SYN.mad:2231`, `src/LO_SYN.mad:2255` |
| Э64 | INF | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 2 | `src/FOREX_CORE.mad:292`, `src/lib21/FOREX_.mad:95` |
| Э64 | INF015-C | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 2 | `src/lib21/READ1.mad:114`, `src/lib21/READ2.mad:114` |
| Э65 | 1 | **не найдено в rukava.be** | — | 2 | `src/lib21/CHEKJOB_.mad:347`, `src/lib21/CHEKJOB_.mad:357` |
| Э65 | 70101 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:2134`, `src/LO_SYN.mad:2827` |
| Э65 | 760 | **не найдено в rukava.be** | — | 2 | `src/lib21/CHEKJOB_.mad:345`, `src/lib21/CHEKJOB_.mad:450` |
| Э65 | A | **не найдено в rukava.be** | — | 2 | `src/lib21/INPUTCAL.mad:136`, `src/lib21/INPUTCAL.mad:143` |
| Э66 | 4502 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:1696`, `src/LO_SYN.mad:1763` |
| Э66 | 4515 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:1123`, `src/LO_SYN.mad:1171` |
| Э66 | 6151 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:3049`, `src/LO_SYN.mad:3145` |
| Э67 | 117 | **не найдено в rukava.be** | — | 2 | `src/LO_SYN.mad:2036`, `src/LO_SYN.mad:2353` |
| Э70 | BUF084 | **не найдено в rukava.be** | — | 2 | `src/lib21/LIBTAP_.mad:242`, `src/lib21/LIBTAP_.mad:542` |
| Э70 | BUF134 | **не найдено в rukava.be** | — | 2 | `src/lib21/MAKELIBT.mad:629`, `src/lib21/MAKELIBT.mad:737` |
| Э70 | BUF135 | **не найдено в rukava.be** | — | 2 | `src/lib21/MAKELIBT.mad:700`, `src/lib21/MAKELIBT.mad:739` |
| Э70 | BUF136 | **не найдено в rukava.be** | — | 2 | `src/lib21/MAKELIBT.mad:752`, `src/lib21/MAKELIBT.mad:836` |
| Э70 | INF023-C | **не найдено в rukava.be** | — | 2 | `src/lib21/READ1.mad:87`, `src/lib21/READ2.mad:87` |
| Э70 | XX367 | **не найдено в rukava.be** | — | 2 | `src/lib21/TCATALOG.mad:449`, `src/lib21/TCATALOG.mad:453` |
| Э72 | COTK2+NT3 | **не найдено в rukava.be** | — | 2 | `src/lib21/BEMSH_.mad:203`, `src/lib21/LINK#IPM.mad:111` |
| Э72 | ICC105 | **не найдено в rukava.be** | — | 2 | `src/lib21/OVERLOAD.mad:628`, `src/lib21/OVERLOAD.mad:656` |
| Э72 | ICL106 | **не найдено в rukava.be** | — | 2 | `src/lib21/OVERLOAD.mad:785`, `src/lib21/OVERLOAD.mad:817` |
| Э20 | 20110 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:2857` |
| Э20 | 20113 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3061` |
| Э20 | 20124 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:2332` |
| Э20 | 20142 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3019` |
| Э20 | 20151 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:1756` |
| Э20 | 20160 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:1532` |
| Э20 | 2254 | **не найдено в rukava.be** | — | 1 | `src/LO_GEN.mad:1362` |
| Э20 | 40513 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:856` |
| Э20 | 40520 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3280` |
| Э20 | 42546 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:1036` |
| Э20 | 42560 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:1552` |
| Э20 | 4323 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3795` |
| Э20 | 4405 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3819` |
| Э20 | 44117 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3287` |
| Э20 | 44144 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:1780` |
| Э20 | 45543 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:2026` |
| Э20 | 47440 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:1556` |
| Э20 | 47505 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:1735` |
| Э20 | 47515 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:2713` |
| Э20 | 47547 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:2860` |
| Э20 | 50520 | **не найдено в rukava.be** | — | 1 | `src/LO_GEN.mad:660` |
| Э20 | 53257 | **не найдено в rukava.be** | — | 1 | `src/LO_GEN.mad:631` |
| Э20 | 62101 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3193` |
| Э20 | 64440 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3125` |
| Э20 | 64551 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:2920` |
| Э20 | 64561 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:862` |
| Э20 | 64566 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:2284` |
| Э20 | 7017 | **не найдено в rukava.be** | — | 1 | `src/FOREX_CORE.mad:351` |
| Э20 | 74440 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3094` |
| Э20 | 75505 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:2177` |
| Э20 | 77101 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3241` |
| Э21 | 1016 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3423` |
| Э21 | 1302 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3495` |
| Э21 | 22662 | **не найдено в rukava.be** | — | 1 | `src/LO_GEN.mad:661` |
| Э21 | 326 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3354` |
| Э21 | 4043 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3732` |
| Э33 | 4114 | **не найдено в rukava.be** | — | 1 | `src/LO_GEN.mad:667` |
| Э36 | 1310 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3504` |
| Э36 | 20102 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:1934` |
| Э36 | 20142 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:1318` |
| Э36 | 317 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3339` |
| Э36 | 4037 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3720` |
| Э36 | 4054 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3741` |
| Э36 | 44040 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:1633` |
| Э36 | 44101 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:1870` |
| Э36 | 45440 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:2174` |
| Э36 | 45501 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:1387` |
| Э36 | 45517 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3239` |
| Э36 | 46126 | **не найдено в rukava.be** | — | 1 | `src/LO_GEN.mad:634` |
| Э36 | 501 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3363` |
| Э36 | 50101 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:2687` |
| Э36 | 51105 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:1943` |
| Э36 | 52117 | **не найдено в rukava.be** | — | 1 | `src/LO_GEN.mad:655` |
| Э36 | 52120 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:1883` |
| Э36 | 52514 | **не найдено в rukava.be** | — | 1 | `src/LO_GEN.mad:669` |
| Э36 | 61120 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3185` |
| Э36 | 61154 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:2674` |
| Э36 | 62101 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:1312` |
| Э36 | 62117 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:859` |
| Э36 | 6264 | **не найдено в rukava.be** | — | 1 | `src/FOREX_CORE.mad:577` |
| Э36 | 63551 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:922` |
| Э36 | 66110 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3106` |
| Э36 | 66117 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:2398` |
| Э36 | 66151 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:2944` |
| Э36 | 70055 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:2983` |
| Э46 | 4510 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:1055` |
| Э47 | 4573 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3040` |
| Э50 | 1202 | ГРАФОПОСТРОИТЕЛЬ: ... | ? | 1 | `src/LO_SYN.mad:3474` |
| Э50 | 1311 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) [tyurin1985] | 264 | 1 | `src/LO_SYN.mad:3507` |
| Э50 | 1323 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) [tyurin1985] | 264 | 1 | `src/LO_SYN.mad:3531` |
| Э50 | 1324 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) [tyurin1985] | 264 | 1 | `src/LO_SYN.mad:3534` |
| Э50 | 323 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) [tyurin1985] | 264 | 1 | `src/LO_SYN.mad:3345` |
| Э50 | 4016 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) [tyurin1985] | 264 | 1 | `src/LO_SYN.mad:3672` |
| Э50 | 70022 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) [tyurin1985] | 264 | 1 | `src/LO_GEN.mad:554` |
| Э50 | 70325 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) [tyurin1985] | 264 | 1 | `src/LO_SYN.mad:3351` |
| Э50 | 70504 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) [tyurin1985] | 264 | 1 | `src/LO_SYN.mad:3372` |
| Э50 | 73010 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) [tyurin1985] | 264 | 1 | `src/LO_SYN.mad:3621` |
| Э50 | 73111 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) [tyurin1985] | 264 | 1 | `src/LO_SYN.mad:3642` |
| Э50 | 75 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) [tyurin1985] | 264 | 1 | `src/lib21/TEMP##.mad:62` |
| Э50 | EOC003+SCE003 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) [tyurin1985] | 264 | 1 | `src/lib21/TEMP##.mad:43` |
| Э50 | EOC006+REG004 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) [tyurin1985] | 264 | 1 | `src/lib21/TEMP##.mad:56` |
| Э50 | EOC042+EOC043 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) [tyurin1985] | 264 | 1 | `src/lib21/CHEKJOB_.mad:419` |
| Э52 | R52021 | COS (ИР 052 A) [tyurin1985] | 264 | 1 | `src/lib21/INPUT_.mad:143` |
| Э52 | REF022 | COS (ИР 052 A) [tyurin1985] | 264 | 1 | `src/lib21/INPUT_.mad:150` |
| Э56 | 74757 | EXP (ИР 056 A) [tyurin1985] | 264 | 1 | `src/FOREX_CORE.mad:583` |
| Э56 | 76462 | EXP (ИР 056 A) [tyurin1985] | 264 | 1 | `src/FOREX_CORE.mad:517` |
| Э57 | -CN1 | ВЫДЕЛЕНИЕ ЦЕЛОЙ ЧАСТИ (ENTIER) / СИСТЕМНАЯ ОПЕРАЦИЯ (ИР 057 A) [tyurin1985] | 264 | 1 | `src/lib21/FT_REGIM.mad:172` |
| Э57 | 1247 | ВЫДЕЛЕНИЕ ЦЕЛОЙ ЧАСТИ (ENTIER) / СИСТЕМНАЯ ОПЕРАЦИЯ (ИР 057 A) [tyurin1985] | 264 | 1 | `src/FOREX_CORE.mad:367` |
| Э57 | 4144 | ВЫДЕЛЕНИЕ ЦЕЛОЙ ЧАСТИ (ENTIER) / СИСТЕМНАЯ ОПЕРАЦИЯ (ИР 057 A) [tyurin1985] | 264 | 1 | `src/FOREX_CORE.mad:582` |
| Э57 | 5 | ВЫДЕЛЕНИЕ ЦЕЛОЙ ЧАСТИ (ENTIER) / СИСТЕМНАЯ ОПЕРАЦИЯ (ИР 057 A) [tyurin1985] | 264 | 1 | `src/lib21/TEMP##.mad:45` |
| Э60 | 4002 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3648` |
| Э60 | 4041 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3726` |
| Э60 | 4423 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3843` |
| Э60 | 512 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3390` |
| Э60 | 514 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3396` |
| Э60 | 70312 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3324` |
| Э60 | 70313 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3327` |
| Э60 | 71015 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3420` |
| Э60 | 71105 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3453` |
| Э60 | 71215 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3486` |
| Э60 | 71313 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3513` |
| Э60 | 74030 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3699` |
| Э60 | 74035 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3714` |
| Э60 | 74040 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3723` |
| Э60 | INC | **не найдено в rukava.be** | — | 1 | `src/lib21/INPUT_.mad:83` |
| Э62 | 110 | УСТАНОВКА (ВОССТАНОВЛЕНИЕ) ПАРОЛЯ НА ДОСТУП К МД ИЛИ МЛ | ? | 1 | `src/LO_SYN.mad:1579` |
| Э62 | 115 | СИСТЕМНЫЕ ЭКСТРАКОДЫ УПРАВЛЕНИЯ ЗАДАЧАМИ И ТЕРМИНАЛАМИ (ИР 062 A) [tyurin1985] | 64 | 1 | `src/LO_SYN.mad:2432` |
| Э62 | 1200 | СИСТЕМНЫЕ ЭКСТРАКОДЫ УПРАВЛЕНИЯ ЗАДАЧАМИ И ТЕРМИНАЛАМИ (ИР 062 A) [tyurin1985] | 64 | 1 | `src/FOREX_CORE.mad:543` |
| Э62 | 160 | СИСТЕМНЫЕ ЭКСТРАКОДЫ УПРАВЛЕНИЯ ЗАДАЧАМИ И ТЕРМИНАЛАМИ (ИР 062 A) [tyurin1985] | 64 | 1 | `src/LO_SYN.mad:2837` |
| Э62 | 40 | ЗАПРОС СОСТОЯНИЯ ЗАДАЧИ ПО ШИФРУ | 265 | 1 | `src/LO_SYN.mad:1759` |
| Э62 | 6466 | СИСТЕМНЫЕ ЭКСТРАКОДЫ УПРАВЛЕНИЯ ЗАДАЧАМИ И ТЕРМИНАЛАМИ (ИР 062 A) [tyurin1985] | 64 | 1 | `src/LO_SYN.mad:1007` |
| Э62 | 6552 | СИСТЕМНЫЕ ЭКСТРАКОДЫ УПРАВЛЕНИЯ ЗАДАЧАМИ И ТЕРМИНАЛАМИ (ИР 062 A) [tyurin1985] | 64 | 1 | `src/LO_SYN.mad:2164` |
| Э62 | 70040 | СИСТЕМНЫЕ ЭКСТРАКОДЫ УПРАВЛЕНИЯ ЗАДАЧАМИ И ТЕРМИНАЛАМИ (ИР 062 A) [tyurin1985] | 64 | 1 | `src/LO_SYN.mad:2449` |
| Э63 | -1 | ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A) [tyurin1985] | 334 | 1 | `src/lib21/LUNTYP.mad:90` |
| Э63 | 20 | ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A) [tyurin1985] | 334 | 1 | `src/lib21/LUNTYP.mad:84` |
| Э63 | 274 | ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A) [tyurin1985] | 334 | 1 | `src/LO_SYN.mad:788` |
| Э63 | 504 | ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A) [tyurin1985] | 334 | 1 | `src/lib21/LUNTYP.mad:66` |
| Э63 | 57 | ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A) [tyurin1985] | 334 | 1 | `src/lib21/LUNTYP.mad:70` |
| Э63 | 576 | ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A) [tyurin1985] | 334 | 1 | `src/lib21/LUNTYP.mad:86` |
| Э63 | 760 | ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A) [tyurin1985] | 334 | 1 | `src/lib21/LUNTYP.mad:82` |
| Э63 | 765 | ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A) [tyurin1985] | 334 | 1 | `src/lib21/CHEKJOB_.mad:187` |
| Э64 | 0 | Отмена режима яистования при печати [tyurin1985] | 277 | 1 | `src/FOREX_DECODER_DISASM.mad:199` |
| Э64 | 1571 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 1 | `src/LO_SYN.mad:2735` |
| Э64 | 4037 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 1 | `src/FOREX_CORE.mad:290` |
| Э64 | 5501 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 1 | `src/LO_SYN.mad:2561` |
| Э64 | 7517 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 1 | `src/LO_SYN.mad:2003` |
| Э64 | 7522 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 1 | `src/LO_SYN.mad:1945` |
| Э64 | ADR057 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 1 | `src/lib21/PT6.mad:148` |
| Э64 | AWS047 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 1 | `src/lib21/DISPAC.mad:98` |
| Э64 | GON046 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 1 | `src/lib21/DISPAC.mad:125` |
| Э64 | IC029 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 1 | `src/lib21/OCATALOG.mad:169` |
| Э64 | INF008 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 1 | `src/lib21/PRINTA.mad:52` |
| Э64 | INF018 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 1 | `src/lib21/LIBRARY_.mad:155` |
| Э64 | N00008 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 1 | `src/lib21/PRINTR.mad:78` |
| Э64 | N00009 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 1 | `src/lib21/PRINTR.mad:86` |
| Э64 | PRI028 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) [tyurin1985] | 277 | 1 | `src/lib21/DISPAC.mad:210` |
| Э65 | -20 | **не найдено в rukava.be** | — | 1 | `src/lib21/DISPAC.mad:93` |
| Э65 | 2101 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3191` |
| Э65 | 2110 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:2849` |
| Э65 | 2117 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:1922` |
| Э65 | 40 | **не найдено в rukava.be** | — | 1 | `src/lib21/DISPAC.mad:103` |
| Э65 | 504 | **не найдено в rukava.be** | — | 1 | `src/lib21/DISPAC.mad:100` |
| Э65 | 505 | **не найдено в rukava.be** | — | 1 | `src/lib21/DISPAC.mad:89` |
| Э65 | 546 | **не найдено в rukava.be** | — | 1 | `src/lib21/INPUTCAL.mad:130` |
| Э65 | 560 | **не найдено в rukava.be** | — | 1 | `src/lib21/CHEKJOB_.mad:355` |
| Э65 | 700 | **не найдено в rukava.be** | — | 1 | `src/lib21/LIBTAP_.mad:389` |
| Э65 | 757 | **не найдено в rukava.be** | — | 1 | `src/lib21/LIBTAP_.mad:391` |
| Э65 | 761 | **не найдено в rukava.be** | — | 1 | `src/lib21/CHEKJOB_.mad:350` |
| Э65 | 762 | **не найдено в rukava.be** | — | 1 | `src/lib21/CHEKJOB_.mad:454` |
| Э65 | XNFM | **не найдено в rukava.be** | — | 1 | `src/lib21/INPUTCAL.mad:138` |
| Э66 | 4546 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:1099` |
| Э66 | 74576 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:2192` |
| Э66 | 76131 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:1054` |
| Э67 | DEB | **не найдено в rukava.be** | — | 1 | `src/lib21/LINK#IPM.mad:120` |
| Э67 | DEB010 | **не найдено в rukava.be** | — | 1 | `src/lib21/TEMP##.mad:69` |
| Э67 | DEB021 | **не найдено в rukava.be** | — | 1 | `src/lib21/DISPAC.mad:152` |
| Э67 | DEB022 | **не найдено в rukava.be** | — | 1 | `src/lib21/DISPAC.mad:153` |
| Э67 | DEB023 | **не найдено в rukava.be** | — | 1 | `src/lib21/DISPAC.mad:154` |
| Э70 | 14 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:803` |
| Э70 | 21 | **не найдено в rukava.be** | — | 1 | `src/lib21/LINK#IPM.mad:237` |
| Э70 | 3110 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3639` |
| Э70 | 370 | **не найдено в rukava.be** | — | 1 | `src/LO_GEN.mad:614` |
| Э70 | 4026 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3696` |
| Э70 | 4072 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3750` |
| Э70 | 4311 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3771` |
| Э70 | 71000 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3399` |
| Э70 | 71101 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3447` |
| Э70 | 71326 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3540` |
| Э70 | 71405 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3567` |
| Э70 | 74021 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3681` |
| Э70 | 74075 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3756` |
| Э70 | 74312 | **не найдено в rukava.be** | — | 1 | `src/LO_SYN.mad:3774` |
| Э70 | AEX333 | **не найдено в rukava.be** | — | 1 | `src/lib21/TCATALOG.mad:2741` |
| Э70 | BUF076 | **не найдено в rukava.be** | — | 1 | `src/lib21/LIBDRU_.mad:276` |
| Э70 | BUF133 | **не найдено в rukava.be** | — | 1 | `src/lib21/MAKELIBT.mad:471` |
| Э70 | C070 | **не найдено в rukava.be** | — | 1 | `src/FOREX_RUNTIME_DISASM.mad:367` |
| Э70 | CON070 | **не найдено в rukava.be** | — | 1 | `src/lib21/FORTLIBR.mad:134` |
| Э70 | INF012 | **не найдено в rukava.be** | — | 1 | `src/lib21/TEMP##.mad:61` |
| Э70 | INF048 | **не найдено в rukava.be** | — | 1 | `src/lib21/OCATALOG.mad:106` |
| Э70 | IW053 | **не найдено в rukava.be** | — | 1 | `src/lib21/TEMFILE.mad:400` |
| Э70 | IWN143 | **не найдено в rukava.be** | — | 1 | `src/lib21/MAKELIBT.mad:888` |
| Э70 | RMO042 | **не найдено в rukava.be** | — | 1 | `src/lib21/DISPAC.mad:146` |
| Э70 | TRCALL | **не найдено в rukava.be** | — | 1 | `src/lib21/BEMSH_.mad:163` |
| Э70 | TRP026 | **не найдено в rukava.be** | — | 1 | `src/lib21/DISPAC.mad:157` |
| Э71 | GAO019 | **не найдено в rukava.be** | — | 1 | `src/lib21/PUNCHICT.mad:96` |
| Э72 | 4 | **не найдено в rukava.be** | — | 1 | `src/lib21/CHEKJOB_.mad:476` |
| Э72 | C | **не найдено в rukava.be** | — | 1 | `src/lib21/EXECUTE.mad:278` |
| Э72 | ETX007 | **не найдено в rukava.be** | — | 1 | `src/lib21/TEMP##.mad:60` |
| Э72 | ETX019 | **не найдено в rukava.be** | — | 1 | `src/lib21/DISPAC.mad:137` |
| Э75 | CN1777 | **не найдено в rukava.be** | — | 1 | `src/lib21/BEMSH_.mad:165` |

## Расшифрованные вхождения

| Код | Слово | Описание | Стр. | Источник | Место |
|-----|-------|----------|------|----------|-------|
| Э62 | 110 | УСТАНОВКА (ВОССТАНОВЛЕНИЕ) ПАРОЛЯ НА ДОСТУП К МД ИЛИ МЛ | ? | `rukava.be:3139` | `src/LO_SYN.mad:1579` |
| Э62 | 40 | ЗАПРОС СОСТОЯНИЯ ЗАДАЧИ ПО ШИФРУ | 265 | `rukava.be:3096` | `src/LO_SYN.mad:1759` |
| Э62 | 102 | ОТМЕНА РЕЖИМА ПРИЕМА С ТЕРМИНАЛА И ПЕРЕХОД В РЕЖИМ ВЫВОДА | ? | `rukava.be:3135` | `src/LO_SYN.mad:1864` |
| Э62 | 102 | ОТМЕНА РЕЖИМА ПРИЕМА С ТЕРМИНАЛА И ПЕРЕХОД В РЕЖИМ ВЫВОДА | ? | `rukava.be:3135` | `src/LO_SYN.mad:1973` |
| Э50 | 1202 | ГРАФОПОСТРОИТЕЛЬ: ... | ? | `rukava.be:3024` | `src/LO_SYN.mad:3474` |
| Э63 | 7 | ЗАПРОС СВЕДЕНИЙ ОБ ОБЛАСТИ | ? | `rukava.be:3155` | `src/lib21/CHEKJOB_.mad:192` |
| Э63 | 7 | ЗАПРОС СВЕДЕНИЙ ОБ ОБЛАСТИ | ? | `rukava.be:3155` | `src/lib21/CHEKJOB_.mad:247` |

## Источник: rukava.be / Тюрин-1985

| Источник | Уникальных пар | Применений | Комментарий в `.mad` |
|---|---|---|---|
| `rukava.be` | 5 | 7 | `[rukava.be:N]` |
| `tyurin1985` | 73 | 113 | `[tyurin1985]`, стр. из книги |
| не расшифровано | 219 | 492 | `НЕ НАЙДЕНО в rukava.be` |

### Пары, расшифрованные по Тюрину-1985

| Код | Информационное слово | Описание из Тюрина | Стр. | Применений | Источник | Пример |
|---|---|---|---|---|---|---|
| Э50 | 1311 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) | 264 | 1 | `tyurin1985` | `src/LO_SYN.mad:3507` |
| Э50 | 1323 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) | 264 | 1 | `tyurin1985` | `src/LO_SYN.mad:3531` |
| Э50 | 1324 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) | 264 | 1 | `tyurin1985` | `src/LO_SYN.mad:3534` |
| Э50 | 323 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) | 264 | 1 | `tyurin1985` | `src/LO_SYN.mad:3345` |
| Э50 | 4016 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) | 264 | 1 | `tyurin1985` | `src/LO_SYN.mad:3672` |
| Э50 | 67 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) | 264 | 2 | `tyurin1985` | `src/FOREX_DECODER_DISASM.mad:156` |
| Э50 | 70022 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) | 264 | 1 | `tyurin1985` | `src/LO_GEN.mad:554` |
| Э50 | 70325 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) | 264 | 1 | `tyurin1985` | `src/LO_SYN.mad:3351` |
| Э50 | 70504 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) | 264 | 1 | `tyurin1985` | `src/LO_SYN.mad:3372` |
| Э50 | 73010 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) | 264 | 1 | `tyurin1985` | `src/LO_SYN.mad:3621` |
| Э50 | 73111 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) | 264 | 1 | `tyurin1985` | `src/LO_SYN.mad:3642` |
| Э50 | 75 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) | 264 | 1 | `tyurin1985` | `src/lib21/TEMP##.mad:62` |
| Э50 | EOC003+SCE003 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) | 264 | 1 | `tyurin1985` | `src/lib21/TEMP##.mad:43` |
| Э50 | EOC006+REG004 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) | 264 | 1 | `tyurin1985` | `src/lib21/TEMP##.mad:56` |
| Э50 | EOC042+EOC043 | СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A) | 264 | 1 | `tyurin1985` | `src/lib21/CHEKJOB_.mad:419` |
| Э52 | R52021 | COS (ИР 052 A) | 264 | 1 | `tyurin1985` | `src/lib21/INPUT_.mad:143` |
| Э52 | REF022 | COS (ИР 052 A) | 264 | 1 | `tyurin1985` | `src/lib21/INPUT_.mad:150` |
| Э56 | 70000 | EXP (ИР 056 A) | 264 | 3 | `tyurin1985` | `src/FOREX_CORE.mad:363` |
| Э56 | 74757 | EXP (ИР 056 A) | 264 | 1 | `tyurin1985` | `src/FOREX_CORE.mad:583` |
| Э56 | 76462 | EXP (ИР 056 A) | 264 | 1 | `tyurin1985` | `src/FOREX_CORE.mad:517` |
| Э57 | -CN1 | ВЫДЕЛЕНИЕ ЦЕЛОЙ ЧАСТИ (ENTIER) / СИСТЕМНАЯ ОПЕРАЦИЯ (ИР 057 A) | 264 | 1 | `tyurin1985` | `src/lib21/FT_REGIM.mad:172` |
| Э57 | 1247 | ВЫДЕЛЕНИЕ ЦЕЛОЙ ЧАСТИ (ENTIER) / СИСТЕМНАЯ ОПЕРАЦИЯ (ИР 057 A) | 264 | 1 | `tyurin1985` | `src/FOREX_CORE.mad:367` |
| Э57 | 1263 | ВЫДЕЛЕНИЕ ЦЕЛОЙ ЧАСТИ (ENTIER) / СИСТЕМНАЯ ОПЕРАЦИЯ (ИР 057 A) | 264 | 2 | `tyurin1985` | `src/FOREX_CORE.mad:362` |
| Э57 | 4000 | ВЫДЕЛЕНИЕ ЦЕЛОЙ ЧАСТИ (ENTIER) / СИСТЕМНАЯ ОПЕРАЦИЯ (ИР 057 A) | 264 | 2 | `tyurin1985` | `src/lib21/BEMSH_.mad:201` |
| Э57 | 4144 | ВЫДЕЛЕНИЕ ЦЕЛОЙ ЧАСТИ (ENTIER) / СИСТЕМНАЯ ОПЕРАЦИЯ (ИР 057 A) | 264 | 1 | `tyurin1985` | `src/FOREX_CORE.mad:582` |
| Э57 | 5 | ВЫДЕЛЕНИЕ ЦЕЛОЙ ЧАСТИ (ENTIER) / СИСТЕМНАЯ ОПЕРАЦИЯ (ИР 057 A) | 264 | 1 | `tyurin1985` | `src/lib21/TEMP##.mad:45` |
| Э57 | 6 | ВЫДЕЛЕНИЕ ЦЕЛОЙ ЧАСТИ (ENTIER) / СИСТЕМНАЯ ОПЕРАЦИЯ (ИР 057 A) | 264 | 5 | `tyurin1985` | `src/FOREX_CORE.mad:197` |
| Э62 | 115 | СИСТЕМНЫЕ ЭКСТРАКОДЫ УПРАВЛЕНИЯ ЗАДАЧАМИ И ТЕРМИНАЛАМИ (ИР 062 A) | 64 | 1 | `tyurin1985` | `src/LO_SYN.mad:2432` |
| Э62 | 1200 | СИСТЕМНЫЕ ЭКСТРАКОДЫ УПРАВЛЕНИЯ ЗАДАЧАМИ И ТЕРМИНАЛАМИ (ИР 062 A) | 64 | 1 | `tyurin1985` | `src/FOREX_CORE.mad:543` |
| Э62 | 160 | СИСТЕМНЫЕ ЭКСТРАКОДЫ УПРАВЛЕНИЯ ЗАДАЧАМИ И ТЕРМИНАЛАМИ (ИР 062 A) | 64 | 1 | `tyurin1985` | `src/LO_SYN.mad:2837` |
| Э62 | 6466 | СИСТЕМНЫЕ ЭКСТРАКОДЫ УПРАВЛЕНИЯ ЗАДАЧАМИ И ТЕРМИНАЛАМИ (ИР 062 A) | 64 | 1 | `tyurin1985` | `src/LO_SYN.mad:1007` |
| Э62 | 6552 | СИСТЕМНЫЕ ЭКСТРАКОДЫ УПРАВЛЕНИЯ ЗАДАЧАМИ И ТЕРМИНАЛАМИ (ИР 062 A) | 64 | 1 | `tyurin1985` | `src/LO_SYN.mad:2164` |
| Э62 | 70040 | СИСТЕМНЫЕ ЭКСТРАКОДЫ УПРАВЛЕНИЯ ЗАДАЧАМИ И ТЕРМИНАЛАМИ (ИР 062 A) | 64 | 1 | `tyurin1985` | `src/LO_SYN.mad:2449` |
| Э63 | -1 | ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A) | 334 | 1 | `tyurin1985` | `src/lib21/LUNTYP.mad:90` |
| Э63 | 20 | ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A) | 334 | 1 | `tyurin1985` | `src/lib21/LUNTYP.mad:84` |
| Э63 | 274 | ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A) | 334 | 1 | `tyurin1985` | `src/LO_SYN.mad:788` |
| Э63 | 502 | ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A) | 334 | 2 | `tyurin1985` | `src/lib21/CHEKJOB_.mad:201` |
| Э63 | 504 | ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A) | 334 | 1 | `tyurin1985` | `src/lib21/LUNTYP.mad:66` |
| Э63 | 57 | ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A) | 334 | 1 | `tyurin1985` | `src/lib21/LUNTYP.mad:70` |
| Э63 | 576 | ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A) | 334 | 1 | `tyurin1985` | `src/lib21/LUNTYP.mad:86` |
| Э63 | 760 | ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A) | 334 | 1 | `tyurin1985` | `src/lib21/LUNTYP.mad:82` |
| Э63 | 765 | ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A) | 334 | 1 | `tyurin1985` | `src/lib21/CHEKJOB_.mad:187` |
| Э63 | CN677 | ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A) | 334 | 3 | `tyurin1985` | `src/lib21/FT_REGIM.mad:90` |
| Э63 | CN766 | ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A) | 334 | 2 | `tyurin1985` | `src/lib21/EXECUTE.mad:120` |
| Э64 | 0 | Отмена режима яистования при печати | 277 | 1 | `tyurin1985` | `src/FOREX_DECODER_DISASM.mad:199` |
| Э64 | 1101 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 2 | `tyurin1985` | `src/LO_SYN.mad:2099` |
| Э64 | 1551 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 2 | `tyurin1985` | `src/LO_SYN.mad:1370` |
| Э64 | 1571 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 1 | `tyurin1985` | `src/LO_SYN.mad:2735` |
| Э64 | 2554 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 4 | `tyurin1985` | `src/LO_SYN.mad:994` |
| Э64 | 4037 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 1 | `tyurin1985` | `src/FOREX_CORE.mad:290` |
| Э64 | 510 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 2 | `tyurin1985` | `src/LO_SYN.mad:1418` |
| Э64 | 5501 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 1 | `tyurin1985` | `src/LO_SYN.mad:2561` |
| Э64 | 5505 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 5 | `tyurin1985` | `src/LO_SYN.mad:1984` |
| Э64 | 5517 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 2 | `tyurin1985` | `src/LO_SYN.mad:1549` |
| Э64 | 7504 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 2 | `tyurin1985` | `src/LO_SYN.mad:2756` |
| Э64 | 7515 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 2 | `tyurin1985` | `src/LO_SYN.mad:1382` |
| Э64 | 7517 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 1 | `tyurin1985` | `src/LO_SYN.mad:2003` |
| Э64 | 7522 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 1 | `tyurin1985` | `src/LO_SYN.mad:1945` |
| Э64 | 77440 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 2 | `tyurin1985` | `src/LO_SYN.mad:2878` |
| Э64 | 77524 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 2 | `tyurin1985` | `src/LO_SYN.mad:2231` |
| Э64 | ADR057 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 1 | `tyurin1985` | `src/lib21/PT6.mad:148` |
| Э64 | AWS047 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 1 | `tyurin1985` | `src/lib21/DISPAC.mad:98` |
| Э64 | GON046 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 1 | `tyurin1985` | `src/lib21/DISPAC.mad:125` |
| Э64 | IC029 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 1 | `tyurin1985` | `src/lib21/OCATALOG.mad:169` |
| Э64 | INF | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 2 | `tyurin1985` | `src/FOREX_CORE.mad:292` |
| Э64 | INF008 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 1 | `tyurin1985` | `src/lib21/PRINTA.mad:52` |
| Э64 | INF015-C | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 2 | `tyurin1985` | `src/lib21/READ1.mad:114` |
| Э64 | INF018 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 1 | `tyurin1985` | `src/lib21/LIBRARY_.mad:155` |
| Э64 | INF093 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 5 | `tyurin1985` | `src/lib21/MAKELIBT.mad:372` |
| Э64 | IP028 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 7 | `tyurin1985` | `src/lib21/OCATALOG.mad:113` |
| Э64 | N00008 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 1 | `tyurin1985` | `src/lib21/PRINTR.mad:78` |
| Э64 | N00009 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 1 | `tyurin1985` | `src/lib21/PRINTR.mad:86` |
| Э64 | PRI028 | УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A) | 277 | 1 | `tyurin1985` | `src/lib21/DISPAC.mad:210` |

Описания взяты из `docs/tyurin1985/extract-codes.json` (источник — Exact-совпадение пары «код:слово»; при отсутствии точного совпадения — fallback по номеру экстракода). Страницы соответствуют нумерации PDF книги.
## Полная таблица rukava.be (Э50–Э77)

| Код | Информационное слово | Описание | Стр. | Строка rukava.be |
|-----|----------------------|----------|------|------------------|
| Э50 | 0000 | SIN | 263 | 2967 |
| Э50 | 0001 | COS | 263 | 2968 |
| Э50 | 0002 | SQRT (КВАДРАТНЫЙ КОРЕНЬ) | 263 | 2969 |
| Э50 | 0003 | ARCTAN | 263 | 2970 |
| Э50 | 0004 | ARCSIN | 263 | 2971 |
| Э50 | 0005 | LN | 263 | 2972 |
| Э50 | 0006 | EXP | 263 | 2973 |
| Э50 | 0007 | ENTIER (ВЫДЕЛЕНИЕ ЦЕЛОЙ ЧАСТИ) | 263 | 2974 |
| Э50 | 0010 | ВВОД МАССИВА ДАННЫХ В ПАМЯТЬ ЗАДАЧИ ПОЛЬЗОВАТЕЛЯ | ? | 2975 |
| Э50 | 0100 | ЗАПРОС ШИФРА ЗАДАЧИ | 263 | 2976 |
| Э50 | 0101 | ЗАПРОС НОМЕРА ПРИЧИНЫ АВАРИЙНОЙ СИТУАЦИИ | 269 | 2977 |
| Э50 | 0102 | ЗАДАНИЕ ЧИСЛА РЕАКЦИЙ НА АВОСТ В ЗАДАЧЕ ПОЛЬЗОВАТЕЛЯ | ? | 2978 |
| Э50 | 0103 | УСТАНОВКА АДРЕСА ВХОДА В ПРОГРАММУ РЕАКЦИИ НА АВОСТ | ? | 2979 |
| Э50 | 0104 | ЗАПРОС ИДЕНТИФИКАТОРА ПОЛЬЗОВАТЕЛЯ В ПАМЯТЬ ЗАДАЧИ | ? | 2980 |
| Э50 | 0105 | ЗАПРОС НОМЕРА ТОМА МД ИЛИ МЛ | 278 | 2981 |
| Э50 | 0106 | ЗАПРОС ИДЕНТИФИКАТОРА ПОЛЬЗОВАТЕЛЯ В ПАМЯТЬ ЗАДАЧИ | 263 | 2982 |
| Э50 | 0107 | ЗАПРОС ИДЕНТИФИКАТОРА ПОЛЬЗОВАТЕЛЯ В ПАМЯТЬ ЗАДАЧИ | ? | 2983 |
| Э50 | 0110 | ЗАПРОС ИНФОРМАЦИИ О НАЛИЧИИ ТОМА | 316 | 2984 |
| Э50 | 0112 | ЗАДАНИЕ СМЕЩЕНИЯ (СДВИГА) НА МЛ (МД) | 278 | 2985 |
| Э50 | 0113 | ЗАПРОС ВЕЛИЧИНЫ СМЕЩЕНИЯ (СДВИГА) НА МЛ (МД) | 278 | 2986 |
| Э50 | 0114 | ЗАПРОС ДАТЫ И НОМЕРА ПРОЦЕССОРА | 264 | 2987 |
| Э50 | 0115 | ЗАПРОС МД В МОНОПОЛЬНОЕ ВЛАДЕНИЕ (ENQ) | 284 | 2988 |
| Э50 | 0116 | ОСВОБОЖДЕНИЕ МД ОТ МОНОПОЛЬНОГО ВЛАДЕНИЯ (DEQ) | 284 | 2989 |
| Э50 | 0117 | СОХРАНЕНИЕ (ЗАПРОС) СОДЕРЖИМОГО СУММАТОРА НА СИСТЕМНОМ ПАКЕТЕ ОПЕРАЦИОННОЙ СИСТЕМЫ | 269 | 2990 |
| Э50 | 0120 | ИЗМЕНЕНИЕ ПАРОЛЯ НА ДОСТУП К ПАКЕТУ МД ИЛИ БОБИНЕ МЛ | ? | 2992 |
| Э50 | 0121 | ПОДТВЕРЖДЕНИЕ ПАРОЛЯ НА ДОСТУП К МД И МЛ | 281 | 2993 |
| Э50 | 0123 | ОТКАЗ ОТ ПАРОЛЯ НА ДОСТУП К МД (МЛ) | ? | 2994 |
| Э50 | 0124 | ЗАПРОС НОМЕРА ПРОГРАММНОГО КАНАЛА | 265 | 2995 |
| Э50 | 0125 | УСТАНОВКА И СНЯТИЕ РАЗДЕЛА СПЕЦ | 318 | 2996 |
| Э50 | 0127 | ИНФОРМАЦИЯ О НАЛИЧИИ ПАРОЛЕЙ НА ДОСТУП К МД | ? | 2997 |
| Э50 | 0130 | ВЫДАЧА СЛУЖЕБНЫХ СЛОВ С МЛ (МД) | 288 | 2998 |
| Э50 | 0131 | ДОЗАКАЗ В ПРОЦЕССЕ РЕШЕНИЯ МД (МЛ) | 282 | 2999 |
| Э50 | 0133 | УПРАВЛЕНИЕ АППАРАТУРОЙ ДКС (КАДОПАМ-КРК-ДКС) | 68 | 3000 |
| Э50 | 0135 | ЗАПРОС ФИЗИЧЕСКОГО НОМЕРА ТЕРМИНАЛА ПО ЛОГИЧЕСКОМУ | ? | 3001 |
| Э50 | 0136 | ЗАПРОС ШИФРА ЗАДАЧИ ПО НОМЕРУ ПРОГРАММНОГО КАНАЛА | ? | 3002 |
| Э50 | 0142 | ОТКАЗ ОТ ПАРОЛЯ НА ШИФР ПОЛЬЗОВАТЕЛЯ | 264 | 3003 |
| Э50 | 0143 | УСТАНОВКА ПАРОЛЯ НА ШИФР ПОЛЬЗОВАТЕЛЯ | 264 | 3004 |
| Э50 | 0146 | ЗАПРОС ИСПОЛЬЗОВАННОГО И ОСТАВШЕГОСЯ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ ПО НОМЕРУ ПРОГРАММНОГО КАНАЛА | 267 | 3005 |
| Э50 | 0147 | ЗАПРОС ШИФРА ПО НОМЕРУ ПРОГРАММНОГО КАНАЛА | 316 | 3007 |
| Э50 | 0150 | ПЕРЕВОД ЗАДАЧИ ИЗ РЕЖИМА ОЖИДАНИЯ В РЕЖИМ ГОТОВНОСТИ | 264 | 3008 |
| Э50 | 0151 | ЗАПРОС НОМЕРА ЗАДАЧИ В КАТАЛОГЕ ВВОДА ПО НОМЕРУ ПРОГРАММНОГО КАНАЛА | 265 | 3009 |
| Э50 | 0155 | ЗАПРОС ШИФРОВ И НОМЕРОВ ЗАДАЧ В КАТАЛОГЕ ВВОДА | 265 | 3011 |
| Э50 | 0156 | ЗАПРОС ТОМА МАГНИТНОГО УСТРОЙСТВА | 280 | 3012 |
| Э50 | 0157 | ЗАПРОС ТОМА В МОНОПОЛЬНОЕ ВЛАДЕНИЕ С КОДОМ ОТВЕТА | 284 | 3013 |
| Э50 | 0160 | ОСВОБОЖДЕНИЕ ТОМА, ЗАХВАЧЕННОГО ПОДЧИНЕННОЙ ЗАДАЧЕЙ | 284 | 3014 |
| Э50 | 0162 | ЗАПРОС ТИПА МАГНИТНОЙ ЛЕНТЫ | 280 | 3015 |
| Э50 | 0163 | СМЕНА РЕЖИМА РАБОТЫ С МАГНИТНОЙ ЛЕНТОЙ | 280 | 3016 |
| Э50 | 0164 | ЧТЕНИЕ СТРОКИ ИЗ СПЕЦИАЛЬНОГО КАТАЛОГА ПО ИМЕНИ | 279 | 3017 |
| Э50 | 0165 | ЗАПРОС ВЛАДЕЛЬЦА ЭВМ И НОМЕРА СИСТЕМНОГО ПАКЕТА | 269 | 3018 |
| Э50 | 0200 | ЗАПРОС СОСТОЯНИЯ ЗАДАННОГО ЛИСТА ОПЕРАТИВНОЙ ПАМЯТИ ЗАДАЧИ ПОЛЬЗОВАТЕЛЯ | 268 | 3019 |
| Э50 | 0201 | ЗАПРОС СОСТОЯНИЯ ЛИСТОВ ОПЕРАТИВНОЙ ПАМЯТИ ЗАДАЧИ | 268 | 3021 |
| Э50 | 1200 | РАБОТА С ГРАФОПОСТРОИТЕЛЕМ (ОСНОВНОЙ ЭКСТРАКОД) | ? | 3022 |
| Э50 | 1201 | ГРАФОПОСТРОИТЕЛЬ: ПОДГОТОВКА К ОБМЕНУ | ? | 3023 |
| Э50 | 1202 | ГРАФОПОСТРОИТЕЛЬ: ... | ? | 3024 |
| Э50 | 1203 | ГРАФОПОСТРОИТЕЛЬ: ... | ? | 3025 |
| Э50 | 1204 | ГРАФОПОСТРОИТЕЛЬ: ЗАПИСЬ НА ТАБЛО | ? | 3026 |
| Э50 | 1205 | ГРАФОПОСТРОИТЕЛЬ: ГРАФИК | ? | 3027 |
| Э50 | 1206 | ГРАФОПОСТРОИТЕЛЬ: БЕНСОН | ? | 3028 |
| Э50 | 1207 | ГРАФОПОСТРОИТЕЛЬ: БЕНСОН (ЗАХВАТ) | ? | 3029 |
| Э50 | 1210 | ЭКСТРАКОД ОБМЕНА С НЕСТАНДАРТНЫМ ОБОРУДОВАНИЕМ | 68 | 3030 |
| Э50 | 1212 | ПРОПУСК ИНФОРМАЦИИ ДЛЯ ВЫДАЧИ НА АЦПУ | 313 | 3031 |
| Э50 | 1216 | ГП НИТИ (ДОП. ОБОРУДОВАНИЕ, ВАРИАНТ К-71) | ? | 3032 |
| Э50 | 1217 | ГП НИТИ (ДОП. ОБОРУДОВАНИЕ, ВАРИАНТ К-71) | ? | 3033 |
| Э50 | 4010 | ВВОД МАССИВА С НОМЕРОМ М В ПАМЯТЬ ЗАДАЧИ (M<400) | 270 | 3034 |
| Э50 | 7600 | РАБОТА С ГРАФОПОСТРОИТЕЛЕМ (АЛЬТЕРНАТИВНЫЙ ИНТЕРФЕЙС) | ? | 3035 |
| Э50 | 7700 | УСТАНОВКА ПАУЗЫ ИЛИ БУДИЛЬНИКА ДЛЯ ЗАДАЧИ ПОЛЬЗОВАТЕЛЯ | ? | 3036 |
| Э50 | 7701 | ВВОД ЗАДАЧИ ПОЛЬЗОВАТЕЛЯ ВО ВХОДНУЮ ОЧЕРЕДЬ | ? | 3037 |
| Э50 | 7702 | ЗАПРОС АДРЕСА ПРЕРЫВАНИЯ ЗАДАЧИ ПОЛЬЗОВАТЕЛЯ | 214 | 3038 |
| Э50 | 7703 | ЗАПРОС МАСКИ И РЕЖИМОВ ЭКСТРАКОДОВ | 214 | 3039 |
| Э51 | 0000 | SIN (2) | 263 | 3041 |
| Э51 | 0001 | COS (2) | 283 | 3042 |
| Э52 | 0000 | COS | 263 | 3044 |
| Э52 | 7777 | ДОВЕРЕННАЯ СВЯЗЬ (УПРАВЛЕНИЕ КАДОПАМ) | ? | 3045 |
| Э53 | 0000 | ARCTAN | 263 | 3047 |
| Э53 | 0040 | ЗАПРОС АСТРОНОМИЧЕСКОГО ВРЕМЕНИ | 267 | 3048 |
| Э53 | 0041 | УСТАНОВКА НАЧАЛЬНОГО АДРЕСА ПРОГРАММЫ ДЕШИФРАТОРА АСИНХРОННЫХ ПРОЦЕССОВ И ПОЛЯ УПРЯТЫВАНИЯ | 204 | 3049 |
| Э53 | 0042 | УСТАНОВКА МАСКИ ШКАЛЫ СОБЫТИЙ | 201 | 3051 |
| Э53 | 0043 | ЗАПРЕТ ПЕРЕХОДА НА АСИНХРОННЫЕ ПРОЦЕССЫ ПРИ ПОЯВЛЕНИИ СОБЫТИЙ В ЗАДАЧЕ ПОЛЬЗОВАТЕЛЯ | ? | 3052 |
| Э53 | 0044 | РАЗРЕШЕНИЕ ПЕРЕХОДА НА АСИНХРОННЫЕ ПРОЦЕССЫ | 204 | 3054 |
| Э53 | 0045 | ВОЗВРАТ В ПРЕРВАННОЕ МЕСТО ПРОГРАММЫ | 206 | 3055 |
| Э53 | 0046 | ЗАПРОС ШКАЛЫ СОБЫТИЙ | 203 | 3056 |
| Э53 | 0047 | ЗАКРЫТИЕ ЗАДАЧИ ПО ОЖИДАНИЮ СОБЫТИЙ | 204 | 3057 |
| Э53 | 0050 | ЗАПРОС МАСКИ ШКАЛЫ СОБЫТИЙ | 203 | 3058 |
| Э53 | 0051 | ОБЪЯВЛЕНИЕ ИЛИ ГАШЕНИЕ СОБЫТИЙ | 204 | 3059 |
| Э53 | 0052 | УСТАНОВКА ТАБЛИЦЫ ПОРТОВ | 220 | 3060 |
| Э53 | 0053 | ПЕРЕДАЧА СООБЩЕНИЙ МЕЖДУ ЗАДАЧАМИ | 220 | 3061 |
| Э53 | 0054 | ЗАПРОС МАСКИ ШКАЛЫ СОБЫТИЙ ПОДЧИНЕННОЙ ЗАДАЧИ | 244 | 3062 |
| Э53 | 0056 | ОТКЛЮЧЕНИЕ ОТ ГЛАВНОЙ ЗАДАЧИ | 191 | 3063 |
| Э53 | 0057 | ОЖИДАНИЕ СООБЩЕНИЯ О ВОЗМОЖНОСТИ ПРОДОЛЖЕНИЯ РЕШЕНИЯ ОТ ГЛАВНОЙ ЗАДАЧИ | 191 | 3064 |
| Э53 | 0060 | ПУСК ПОДЧИНЕННОЙ ЗАДАЧИ | 191 | 3066 |
| Э53 | 0061 | ОБЪЯВЛЕНИЕ ИЛИ ГАШЕНИЕ СОБЫТИЙ В ПОДЧИНЕННОЙ ЗАДАЧЕ | ? | 3067 |
| Э53 | 0063 | ЗАПРОС МАСКИ ШКАЛЫ СОБЫТИЙ В ПОДЧИНЕННОЙ ЗАДАЧЕ | 192 | 3068 |
| Э53 | 0065 | ПЕРЕДАЧА ИЛИ ИЗЪЯТИЕ ЛИСТОВ ОПЕРАТИВНОЙ ПАМЯТИ ГЛАВНОЙ ЗАДАЧЕЙ У СВОЕЙ ПОДЧИНЕННОЙ | 193 | 3069 |
| Э53 | 0066 | ЗАПРОС ШКАЛЫ СОБЫТИЙ ПОДЧИНЕННОЙ ЗАДАЧИ | 210 | 3071 |
| Э53 | 0067 | ПЕРЕДАЧА ИЛИ ИЗЪЯТИЕ БОБИНЫ МЛ ИЛИ ПАКЕТА МД У ПОДЧИНЕННОЙ ЗАДАЧИ | ? | 3072 |
| Э53 | 0070 | РАЗРЕШЕНИЕ ПЕРЕХОДА НА АСИНХРОННЫЕ ПРОЦЕССЫ ПРИ НАСТУПЛЕНИИ СОБЫТИЙ В ПОДЧИНЕННОЙ ЗАДАЧЕ | 210 | 3074 |
| Э53 | 0071 | УПРАВЛЕНИЕ СОСТОЯНИЕМ ПОРТА | 221 | 3076 |
| Э53 | 0072 | ЗАПРЕТ ПЕРЕХОДА НА АСИНХРОННЫЕ ПРОЦЕССЫ В ПОДЧИНЕННОЙ ЗАДАЧЕ | 210 | 3077 |
| Э53 | 0073 | УСТАНОВКА НАЧАЛЬНОГО АДРЕСА ПРОГРАММЫ ДЕШИФРАТОРА И АДРЕСА ПОЛЯ УПРЯТЫВАНИЯ В ПОДЧИНЕННОЙ ЗАДАЧЕ | ? | 3079 |
| Э53 | 0075 | ПЕРЕДАЧА СООБЩЕНИЯ ОТ ОДНОЙ ЗАДАЧИ ДРУГОЙ ОТ ИМЕНИ ТРЕТЬЕЙ | 222 | 3081 |
| Э53 | 0076 | ПОДЧИНЕНИЕ С ОЖИДАНИЕМ | 190 | 3083 |
| Э53 | 0077 | ОКОНЧАНИЕ БУДИЛЬНИКА ИЛИ ПАУЗЫ В ПОДЧИНЕННОЙ ЗАДАЧЕ | 317 | 3084 |
| Э54 | 0000 | ARCSIN | 263 | 3086 |
| Э55 | 0000 | LN | ? | 3088 |
| Э57 | 0000 | EXP | 263 | 3090 |
| Э60 | — | ВВОД ОБРАЗА | 270 | 3092 |
| Э62 | 0000 | КОНЕЦ ЗАДАЧИ | 63 | 3094 |
| Э62 | 0010 | ПРОДОЛЖЕНИЕ ВЫПОЛНЕНИЯ РАНЕЕ ПЕРЕХВАЧЕННОГО ЭКСТРАКОДА | ? | 3095 |
| Э62 | 0040 | ЗАПРОС СОСТОЯНИЯ ЗАДАЧИ ПО ШИФРУ | 265 | 3096 |
| Э62 | 0043 | СОХРАНЕНИЕ ЗАДАЧИ НА БУФЕРЕ ВВОДА ПОСЛЕ ОКОНЧАНИЯ ЕЁ РЕШЕНИЯ | 268 | 3097 |
| Э62 | 0044 | ОТКАЗ ОТ ВЫХОДНОГО ПОТОКА ИНФОРМАЦИИ | 277 | 3099 |
| Э62 | 0045 | ОСВОБОЖДЕНИЕ ОПЕРАТИВНОЙ ПАМЯТИ ОТ СТАНДАРТНЫХ ПРОГРАММ | 50 | 3100 |
| Э62 | 0046 | ПЕРЕДАЧА И ИЗЪЯТИЕ ТЕРМИНАЛОВ СИСТЕМНОЙ ЗАДАЧЕЙ | 195 | 3101 |
| Э62 | 0047 | ЗАПИСЬ И СЧИТЫВАНИЕ СПЕЦИАЛЬНЫХ РЕГИСТРОВ М34 И М35 У ПОДЧИНЕННОЙ ЗАДАЧИ | 198 | 3102 |
| Э62 | 0050 | ЗАПИСЬ И СЧИТЫВАНИЕ МОДИФИКАТОРОВ У ПОДЧИНЕННОЙ ЗАДАЧИ | 197 | 3104 |
| Э62 | 0051 | ЗАПИСЬ И СЧИТЫВАНИЕ СМ, РК, РМР, М1, М2 У ПОДЧИНЕННОЙ ЗАДАЧИ | 197 | 3105 |
| Э62 | 0052 | ОБМЕН СЛОВОМ ОПЕРАТИВНОЙ ПАМЯТИ МЕЖДУ ГЛАВНОЙ И ПОДЧИНЕННОЙ ЗАДАЧАМИ | 195 | 3107 |
| Э62 | 0053 | УСТАНОВКА МАСКИ ШКАЛЫ ПЕРЕХВАТЫВАЕМЫХ ЭКСТРАКОДОВ | ? | 3109 |
| Э62 | 0054 | ЗАПРОС ПРИЧИНЫ ОСТАНОВА ПОДЧИНЕННОЙ ЗАДАЧИ | 200 | 3110 |
| Э62 | 0055 | ЗАПРОС АДРЕСА ВХОДА В ПРОГРАММУ АВОСТНОЙ ВЫДАЧИ ПОДЧИНЕННОЙ ЗАДАЧИ | 347 | 3111 |
| Э62 | 0056 | ЗАПРОС ШКАЛЫ ЗАНЯТЫХ ТЕРМИНАЛОВ | 64 | 3113 |
| Э62 | 0057 | ЗАХВАТ СВОБОДНОГО ТЕРМИНАЛА | 61 | 3114 |
| Э62 | 0060 | ЗАПРОС ШКАЛЫ СВОБОДНЫХ ТЕРМИНАЛОВ | 62 | 3115 |
| Э62 | 0061 | ЗАПРОС ПОДЧИНЕННЫХ ЗАДАЧ | 192 | 3116 |
| Э62 | 0063 | УСТАНОВКА ПОЛЯ УПРЯТЫВАНИЯ ГЛАВНОЙ ЗАДАЧЕЙ ДЛЯ СВОЕЙ ПОДЧИНЕННОЙ | 207 | 3117 |
| Э62 | 0064 | ЗАПРОС МАСКИ ШКАЛЫ СОБЫТИЙ ДЛЯ ПОДЧИНЕННОЙ ЗАДАЧИ | ? | 3119 |
| Э62 | 0065 | ЗАПРОС ПРЕДНАЗНАЧЕННОЙ ГЛАВНОЙ ШКАЛЫ СОБЫТИЙ ПОДЧИНЕННОЙ ЗАДАЧИ | 208 | 3120 |
| Э62 | 0066 | ЗАПРОС ПРЕДНАЗНАЧЕННОЙ ГЛАВНОЙ МАСКИ ШКАЛЫ СОБЫТИЙ ПОДЧИНЕННОЙ ЗАДАЧИ | 208 | 3122 |
| Э62 | 0067 | ОБЪЯВЛЕНИЕ ИЛИ ГАШЕНИЕ СОБЫТИЙ В ПОДЧИНЕННОЙ ЗАДАЧЕ | ? | 3124 |
| Э62 | 0070 | ПРОДОЛЖЕНИЕ ВЫПОЛНЕНИЯ РАНЕЕ ПЕРЕХВАЧЕННОГО ЭКСТРАКОДА | ? | 3125 |
| Э62 | 0071 | УСТАНОВКА МАСКИ ПЕРЕХВАТЫВАЕМЫХ ЭКСТРАКОДОВ В ПОДЧИНЕННОЙ ЗАДАЧЕ ДЛЯ ГЛАВНОЙ | ? | 3126 |
| Э62 | 0072 | ОТКЛЮЧЕНИЕ ПОДЧИНЕННОЙ ЗАДАЧИ ИЛИ ПОДКЛЮЧЕНИЕ К ДРУГОЙ | ? | 3128 |
| Э62 | 0073 | ЗАПРОС СОСТОЯНИЯ ЛИСТА ПОДЧИНЕННОЙ ЗАДАЧИ | ? | 3129 |
| Э62 | 0074 | ЗАПРОС ИНФОРМАЦИИ О ЗАХВАТЕ ПАКЕТА МД У ПОДЧИНЕННОЙ ЗАДАЧИ | ? | 3130 |
| Э62 | 0075 | ЗАПРОС ТЕРМИНАЛОВ ПОДЧИНЕННОЙ ЗАДАЧИ | ? | 3132 |
| Э62 | 0076 | ОТКАЗ ОТ РЕЖИМА ИНКО | 286 | 3133 |
| Э62 | 0101 | ЗАПРОС ОСТАНОВЛЕННЫХ ПОДЧИНЕННЫХ ЗАДАЧ | 199 | 3134 |
| Э62 | 0102 | ОТМЕНА РЕЖИМА ПРИЕМА С ТЕРМИНАЛА И ПЕРЕХОД В РЕЖИМ ВЫВОДА | ? | 3135 |
| Э62 | 0103 | ЗАПРОС ЛОГИЧЕСКОГО НОМЕРА ТЕРМИНАЛА ПО ФИЗИЧЕСКОМУ | 61 | 3137 |
| Э62 | 0104 | ОБМЕН ИНФОРМАЦИЕЙ МЕЖДУ ОП ГЛАВНОЙ И ПОДЧИНЕННОЙ ЗАДАЧ | ? | 3138 |
| Э62 | 0110 | УСТАНОВКА (ВОССТАНОВЛЕНИЕ) ПАРОЛЯ НА ДОСТУП К МД ИЛИ МЛ | ? | 3139 |
| Э62 | 0117 | ПЕРЕДАЧА ПОДЧИНЕННОЙ ЗАДАЧЕ ПРИЗНАКА ОПРОСА ТЕРМИНАЛА | ? | 3140 |
| Э62 | 0123 | РАЗРЕШЕНИЕ (ЗАПРЕТ) ВЫВОДА НА ПИ, ПЛ | 278 | 3141 |
| Э62 | 0125 | ЗАПРОС ИНФОРМАЦИИ ОБ ИСПОЛЬЗОВАННЫХ ТРАКТАХ МБ | 268 | 3142 |
| Э62 | 0126 | ОБМЕН ТРАКТАМИ МБ МЕЖДУ ГЛАВНОЙ И ПОДЧИНЕННОЙ ЗАДАЧАМИ | ? | 3143 |
| Э62 | 0130 | ОТКАЗ ОТ ИСПОЛЬЗОВАННЫХ ТРАКТОВ МБ И ПЕРЕДАЧА ИХ В РЕСУРС ЗАДАЧИ | 290 | 3144 |
| Э63 | 01 | СОЗДАНИЕ ОБЛАСТИ | ? | 3149 |
| Э63 | 02 | УНИЧТОЖЕНИЕ ОБЛАСТИ | ? | 3150 |
| Э63 | 03 | УСТАНОВКА, СМЕНА И СНЯТИЕ ПАРОЛЯ НА ОБЛАСТЬ | ? | 3151 |
| Э63 | 04 | ЗАДАНИЕ ПРАВ ДОСТУПА К ОБЛАСТИ | ? | 3152 |
| Э63 | 05 | ПОДТВЕРЖДЕНИЕ ПАРОЛЯ НА ОБЛАСТЬ | ? | 3153 |
| Э63 | 06 | ЗАПРОС СПИСКА ДОПУЩЕННЫХ ЛИЦ | ? | 3154 |
| Э63 | 07 | ЗАПРОС СВЕДЕНИЙ ОБ ОБЛАСТИ | ? | 3155 |
| Э63 | 10 | ЗАПРОС КАТАЛОГА ОБЛАСТЕЙ | ? | 3156 |
| Э63 | 11 | ЗАПРОС КАТАЛОГА ОБЩИХ ОБЛАСТЕЙ | ? | 3157 |
| Э63 | 12 | ДОЗАКАЗ ОБЛАСТИ | ? | 3158 |
| Э63 | 13 | ЗАПРОС ССЫЛКИ ПО ИМЕНИ | ? | 3159 |
| Э63 | 14 | ЗАДАНИЕ СДВИГА ПО ОБЛАСТИ | ? | 3160 |
| Э63 | 15 | ЗАПРОС СДВИГА ОБЛАСТИ | ? | 3161 |
| Э63 | 16 | ПЕРЕХОД В РЕЖИМ АДМИНИСТРАТОРА | ? | 3162 |
| Э63 | 17 | СМЕНА ШИФРА И КЛЮЧА АДМИНИСТРАТОРА | ? | 3163 |
| Э63 | 30 | ЗАХВАТ ОБЛАСТИ | ? | 3164 |
| Э63 | 31 | ОСВОБОЖДЕНИЕ ОБЛАСТИ | ? | 3165 |
| Э64 | А | УСТАНОВКА РЕЖИМА ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (А – АДРЕС ИНФОРМАЦИОННОГО СЛОВА) | 276 | 3167 |
| Э66 | А | ОБРАЩЕНИЕ К СТАНДАРТНЫМ ПРОГРАММАМ | 50 | 3170 |
| Э67 | А | ЭКСТРАКОД ОТЛАДКИ | ? | 3172 |
| Э71 | А | ОБМЕН С ВНЕШНЕЙ ПАМЯТЬЮ / ВЫДАЧА НА ПИ, ПЛ / РАБОТА С МЛ | 284, ?, 56 | 3174 |
| Э72 | А | ЗАДАНИЕ МАСКИ УПРАВЛЕНИЯ ДЛЯ Э74 / ОТКАЗ ОТ НЕИСПОЛЬЗУЕМЫХ ТРАКТОВ МБ / ПЕРЕИМЕНОВАНИЕ МЛ / ОТКАЗ ОТ ЛИСТОВ ОЗУ / ЗАПРОС ЛИСТОВ ОПЕРАТИВН… | 63, 289, ?, 290, 283, 282, 243 | 3178 |
| Э73 | А | ВВОД МАССИВА С НОМЕРОМ M-1 В ПАМЯТЬ ЗАДАЧИ (M<400) / ПРЕКРАЩЕНИЕ ОБМЕНА ПО ВИРТУАЛЬНОМУ НОМЕРУ УСТРОЙСТВА | 270, ? | 3189 |
| Э74 | А | КОНЕЦ ЗАДАЧИ | 63 | 3192 |
| Э75 | А | ЗАПИСЬ КОМАНДЫ В ОПЕРАТИВНУЮ ПАМЯТЬ ЗАДАЧИ ПОЛЬЗОВАТЕЛЯ | 271 | 3194 |
| Э76 | А | СВЯЗЬ БЭСМ-6 С ЭВМ ТИПА М-6000 | 63 | 3196 |
| Э77 | А | ЭКСТРАКОД КВМ | ? | 3198 |

## Воспроизведение

```sh
python3 tools/extract_codes.py --list             # таблица rukava.be + счётчики Тюрина
python3 tools/extract_codes.py --find Э57/1263    # поиск по обоим источникам
python3 tools/extract_codes.py --find Э57/1263 --source tyurin   # только Тюрин
python3 tools/extract_codes.py --find Э62/102 --source rukava    # только rukava.be
python3 tools/extract_codes.py --json             # таблица в JSON
python3 tools/extract_codes.py --scan             # скан .mad-файлов (оба источника)
bash tests/check-extract-codes.sh                 # проверка комментариев (оба источника)
```
