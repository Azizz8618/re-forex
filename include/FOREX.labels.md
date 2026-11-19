# FOREX — таблица соответствий меток и литералов

Документ фиксирует переименование меток в трёх реконструированных МАДЛЕН-текстах:
`src/FOREX_CORE.mad`, `src/FOREX_RUNTIME.mad`, `include/FOREX_ROOT.mad`.
Исходные имена сохранены в trailing-комментариях (`; (СТАРОЕ)` / `. (СТАРОЕ)`) и в
заголовках разделов — поэтому обязательные символы из `tests/check-annotations.sh`
(INITFOR*, `LOREX`, `STOP/`, `DATAPR`, `OCTTDE`, `GIV/PG`, `TAK/PG`, `LOADAN`,
`LO*SYN`, `LO*GEN`, `*A*`, `ENTRY*`, `*DUMON*`) остаются доступны для поиска.

Правила: не удалялись строки, не изменялись адреса и метки машинных слов
(`С слово NNNN @0o… = 0o…`), адресная колонка ROOT и комментарии-источники `S1:…`.

## 1. Метки → осмысленные имена

### src/FOREX_CORE.mad (корень FOREX*)

| Было | Стало | Назначение / обоснование |
|---|---|---|
| `FXCOR` | `FXCOR` | имя реконструированного модуля (KEEP) |
| `START` | `FXSTR` | ENTRY-псевдоним INITFO; точка входа 0o510303 |
| X_DATAPRS | `DATAPR` | внешнее объявление DATAPR → DATAPR |
| X_TAK_PG | `PAGETK` | внешнее объявление TAK/PG → PAGETK |
| X_GIV_PG | `PAGEGV` | внешнее объявление GIV/PG → PAGEGV |
| X_OCTTDEC | `OCTTDE` | внешнее объявление OCTTDE → OCTTDE |
| X_LOADANGO | `LOADAN` | внешнее объявление LOADAN — загрузчик оверлеев |
| INITFOR | `INITFO` | ENTRY INITFOR*: инициализация корня, 0o510303 |
| `NPR` | `DPRTN` | точка возврата после CALL DATAPR; проверка FULISF |
| `LOREX` | `LODOVL` | ENTRY LOREX: загрузка LO*SYN и LO*GEN, 0o510315 |
| `RMON` | `PRTIME` | ENTRY RMON: печать времени трансляции, 0o510317 |
| `PRIN` | `PRTMSG` | внутренняя печать сообщения (*64 INF), 0o510327 |
| `STOP` | `ERRTRL` | ENTRY STOP/: аварийный выход «ОШ. ТРАНСЛЯТОРА», 0o510332 |
| `ИМЯ_*` | `ИМЯ_*` | EQU-псевдонимы таблицы символов 0o510413..431 (KEEP) |

### src/FOREX_RUNTIME.mad (FORMAT / FORTLIBR / DATAPR / OCTTDE)

| Было | Стало | Назначение / обоснование |
|---|---|---|
| `FORMAT` | `FTDISP` | диспетчер таблицы передач FT* (S1:15529) |
| `*00004` | `FTDTSB` | установка базы таблицы 77766B |
| `*00005` | `FTDLOP` | тело цикла VLM по M12 |
| `*00010` | `FTDOFS` | вычисление смещения пары UJ/ATX |
| `*00012` | `FTDSTO` | запись STX и продвижение указателя |
| `*00026` | `FTDTE` | конец таблицы / FT*003 |
| `*00027` | `FTDCNS` | константа LOG 10000000… |
| FORTLIBR | `FTLIO` | библиотечный вывод PRINT8/WRTLBR (S1:15590) |
| `BUFFER` | `FTLBFR` | PU 2000B — буфер обмена с библиотекой |
| `WRTLBR, PRINT8` | `WRTLBR, PRINT8` | официальные экспортные имена (KEEP) |
| `*00010` | `FLAFT` | возврат после VJM WRTLBR+1 |
| `*00023` | `FLSIGC` | проверка знака/разряда |
| `*00027` | `FLXORL` | цикл AEX/сборки выходного слова |
| `*00032` | `FLWTC` | ветка установки модификатора WTC |
| `*00036` | `FLALT` | альтернативная ветка сборки |
| `*00042` | `FLSHIN` | сдвиг и подстановка разрядов |
| `*00045` | `FLCMPR` | сравнение и проверка маски |
| `*00050` | `FLMASK` | ветка маскирования 77777B |
| `*00053` | `FLASMB` | сборка 8-символьного ISO-слова |
| `*00061` | `FLCON` | база блока LOG-констант |
| `DATAPR` | `DATAPR` | главная точка входа печати даты (S5:7645) |
| `DATE*` | `DGET` | ENTRY FUN 67B — системная дата/время |
| `DARET` | `DPARSE` | разбор FUN 67B, выборка месяца |
| `L1 / L2 / L3` | `DTWTCS / DTENDC / DTSTAD` | внутренние ветки DARET/PREPDAT |
| `B` | `DPREPB` | база preparations даты (13,BAS) |
| PREPDAT | `DPREPA` | ENTRY подготовки даты → DATAPR |
| `MARR` | `MNTHNM` | таблица названий месяцев ЯНВ…ДЕК |
| `DMASK / TMASK / YMASK` | `DYMSK / TIMMSK / YRMSK` | маски DD / HH.MM / YY |
| MONTHFI | `MNTHFD` | поле месяца OCT 00 776 |
| `OCTTDE (S6)` | `OCTTDE` | DECODER: число → 6 ISO-цифр, вызывается PRTIME |
| `C` | `OCTBAS` | база C для адресов DEC-C, INT0-C и т.д. |
| `BEGIN / CYCL / /6SYMB` | `OCTBGN / OCTCYC / OCTSYM` | начало, цикл деления, цикл цифр |
| `OCTTDE (S7)` | `OCTEXF` | альтернативная реализация EXFOR (умножение на 0.1) |
| `L1 / RET (S7)` | `OCTEDL / OCTERT` | цикл цифр и возврат через M15 |

### include/FOREX_ROOT.mad (корень + GIV/PG + TAK/PG)

| Было | Стало | Назначение / обоснование |
|---|---|---|
| INITFOR* | `INITFO` | ENTRY; загрузка по 0o1770 (S1:15466) |
| `NPR` | `DPRTN` | UIA → NPR, возврат из DATAPR |
| `LOREX` | `LODOVL` | ENTRY; XTS LO*SYN/LO*GEN + CALL LOADAN |
| `RMON` | `PRTIME` | ENTRY; печать времени, CALL OCTTDE |
| `PRIN` | `PRTMSG` | общая точка печати для PRTIME и ERRTRL |
| `STOP/` | `ERRTRL` | ENTRY; VTM MIST + UJ PRTMSG |
| `DATAPR (SUBP)` | `DATAPR` | внешняя подпрограмма печати даты |
| `OCTTDE (SUBP)` | `OCTTDE` | внешняя подпрограмма DEC-печати |
| `GIV/PG` | `PAGEGV` | модуль выдачи страницы (S1:16780) |
| `TAK/PG` | `PAGETK` | ENTRY «взять страницу» (S1:16821) |
| `*C` | `PGWRKB` | M12 = база рабочей области PAGEGV |
| `FL*SAV` | `PGFLSA` | сохранённый флаг страницы |
| `COMM / L/S` | `PGCOMM / PGCOPL` | общая подпрограмма и цикл копирования |
| `R17 / Э67 / K67 / GO` | `PGRST7 / PGX67 / PG67CN / PG_GO` | механизм экстракода 67 |
| `*W / *S / Э67*` | `PGSHWD / PGSAVS / PG67SA` | BSS-ячейки PAGEGV |

## 2. КОНСТАНТЫ/ЛИТЕРАЛЫ

Все числовые, вещественные и текстовые литералы в операндах вынесены в
`name ,EQU, value` с комментарием «роль / источник». Блоки расположены в начале
каждого файла (`С ---- КОНСТАНТЫ/ЛИТЕРАЛЫ ----` / `C ---- … ----`).
Значения ниже — дословно из исходника; адреса и слова дампа не переписаны.

### `src/FOREX_CORE.mad`

| Имя константы | Значение | Роль | Источник |
|---|---|---|---|
| `AOC4K` | `0o4000` | . COMMON 2048 слов | FOREX_CORE.mad:43 |
| `AOC50` | `0o50` | . COMMON 40 слов, таблица entry | FOREX_CORE.mad:36 |
| `AI0AD` | `4007B` | константа A/I0 = 1 | FOREX_CORE.mad:153 |
| `BS16A` | `74001B` | база M16 (0o74001) | FOREX_CORE.mad:95 |
| `BS14R` | `14` | номер индексного регистра базы M14 | FOREX_CORE.mad:99 |
| `BUFALN` | `4000B` | COMMON *A*: 2048 слов | FOREX_CORE.mad:344 |
| `CHKAD` | `4005B` | флаг проверки | FOREX_CORE.mad:120 |
| `C11200` | `11200B` | . загрузить индексный регистр [уиа] | FOREX_CORE.mad:343 |
| `CA1200` | `1200B` | . экстракод *62 [э62] | FOREX_CORE.mad:430 |
| `CA1247` | `1247B` | . экстракод *57 [э57] | FOREX_CORE.mad:254 |
| `CA1263` | `1263B` | . экстракод *57 [э57] | FOREX_CORE.mad:249 |
| `C16617` | `16617B` | . переход по индексу (модифицированный) [пино] | FOREX_CORE.mad:439 |
| `CA231` | `231B` | . установить модификатор адреса [рег] | FOREX_CORE.mad:246 |
| `C30453` | `30453B` | . операция [выпр] | FOREX_CORE.mad:242 |
| `C31056` | `31056B` | . переход при нулевом индексе [пио] | FOREX_CORE.mad:245 |
| `C36464` | `36464B` | . переход при нулевом индексе [пио] | FOREX_CORE.mad:444 |
| `C37013` | `37013B` | . безусловный переход [пб] | FOREX_CORE.mad:225 |
| `CA4040` | `4040B` | . записать аккумулятор в память [зп] | FOREX_CORE.mad:279 |
| `CA4041` | `4041B` | . записать аккумулятор в память [зп] | FOREX_CORE.mad:283 |
| `CA4042` | `4042B` | . записать аккумулятор в память [зп] | FOREX_CORE.mad:287 |
| `CA4043` | `4043B` | . записать аккумулятор в память [зп] | FOREX_CORE.mad:291 |
| `CA4044` | `4044B` | . записать аккумулятор в память [зп] | FOREX_CORE.mad:295 |
| `CA4045` | `4045B` | . записать аккумулятор в память [зп] | FOREX_CORE.mad:299 |
| `CA4046` | `4046B` | . записать аккумулятор в память [зп] | FOREX_CORE.mad:307 |
| `CA4047` | `4047B` | . записать аккумулятор в память [зп] | FOREX_CORE.mad:311 |
| `CA4050` | `4050B` | . записать аккумулятор в память [зп] | FOREX_CORE.mad:315 |
| `CA4051` | `4051B` | . записать аккумулятор в память [зп] | FOREX_CORE.mad:319 |
| `CA4052` | `4052B` | . записать аккумулятор в память [зп] | FOREX_CORE.mad:323 |
| `CA4053` | `4053B` | . записать аккумулятор в память [зп] | FOREX_CORE.mad:327 |
| `CA4054` | `4054B` | . записать аккумулятор в память [зп] | FOREX_CORE.mad:331 |
| `CA4055` | `4055B` | . записать аккумулятор в память [зп] | FOREX_CORE.mad:335 |
| `CA4056` | `4056B` | . записать аккумулятор в память [зп] | FOREX_CORE.mad:347 |
| `CA4144` | `4144B` | . экстракод *57 [э57] | FOREX_CORE.mad:469 |
| `C44000` | `44000B` | . переход по индексу (модифицированный); абсолютный адрес 0o044000 [пи | FOREX_CORE.mad:271 |
| `C44745` | `44745B` | . инкремент индексного регистра; абсолютный адрес 0o044745 [слиа] | FOREX_CORE.mad:409 |
| `CA4543` | `4543B` | . переход по индексу (модифицированный) [пино] | FOREX_CORE.mad:421 |
| `C46555` | `46555B` | . загрузить индексный регистр; абсолютный адрес 0o046555 [уиа] | FOREX_CORE.mad:425 |
| `CA5317` | `5317B` | . останов / специальный выход [уим] | FOREX_CORE.mad:434 |
| `C55451` | `55451B` | . переход при нулевом аккумуляторе; абсолютный адрес 0o055451 [по] | FOREX_CORE.mad:417 |
| `CA56` | `56B` | . записать аккумулятор в память [зп] | FOREX_CORE.mad:237 |
| `C61200` | `61200B` | . переход по индексу (модифицированный); абсолютный адрес 0o061200 [пи | FOREX_CORE.mad:426 |
| `CA6264` | `6264B` | . экстракод *36 [втбрз] | FOREX_CORE.mad:464 |
| `CA6441` | `6441B` | . останов / специальный выход [уим] | FOREX_CORE.mad:429 |
| `C70031` | `70031B` | . записать аккумулятор в память; абсолютный адрес 0o070031 [зп] | FOREX_CORE.mad:401 |
| `C70035` | `70035B` | . записать аккумулятор в память; абсолютный адрес 0o070035 [зп] | FOREX_CORE.mad:357 |
| `C70042` | `70042B` | . записать аккумулятор в память; абсолютный адрес 0o070042 [зп] | FOREX_CORE.mad:377 |
| `C70043` | `70043B` | . записать аккумулятор в память; абсолютный адрес 0o070043 [зп] | FOREX_CORE.mad:381 |
| `C70044` | `70044B` | . записать аккумулятор в память; абсолютный адрес 0o070044 [зп] | FOREX_CORE.mad:397 |
| `C70045` | `70045B` | . записать аккумулятор в память; абсолютный адрес 0o070045 [зп] | FOREX_CORE.mad:389 |
| `C70046` | `70046B` | . записать аккумулятор в память; абсолютный адрес 0o070046 [зп] | FOREX_CORE.mad:393 |
| `C70047` | `70047B` | . записать аккумулятор в память; абсолютный адрес 0o070047 [зп] | FOREX_CORE.mad:385 |
| `C70050` | `70050B` | . записать аккумулятор в память; абсолютный адрес 0o070050 [зп] | FOREX_CORE.mad:352 |
| `CA7017` | `7017B` | . экстракод *20 [э20] | FOREX_CORE.mad:238 |
| `C74757` | `74757B` | . экстракод *56; абсолютный адрес 0o074757 [э56] | FOREX_CORE.mad:470 |
| `C75120` | `75120B` | . умножение; абсолютный адрес 0o075120 [умн] | FOREX_CORE.mad:303 |
| `C75451` | `75451B` | . инкремент индексного регистра; абсолютный адрес 0o075451 [слиа] | FOREX_CORE.mad:413 |
| `C75545` | `75545B` | . переход по индексу (модифицированный); абсолютный адрес 0o075545 [пи | FOREX_CORE.mad:459 |
| `C75663` | `75663B` | . переход по индексу (модифицированный); абсолютный адрес 0o075663 [пи | FOREX_CORE.mad:454 |
| `C76245` | `76245B` | . инкремент индексного регистра; абсолютный адрес 0o076245 [слиа] | FOREX_CORE.mad:274 |
| `C76462` | `76462B` | . экстракод *56; абсолютный адрес 0o076462 [э56] | FOREX_CORE.mad:404 |
| `CMOD3` | `3B` | режим 3 (вещественный) | FOREX_CORE.mad:152 |
| `CW001` | `1B` | адрес слова 1 ядра | FOREX_CORE.mad:65 |
| `CW002` | `2B` | адрес слова 2 ядра | FOREX_CORE.mad:365 |
| `CW004` | `4B` | адрес слова 4 ядра | FOREX_CORE.mad:373 |
| `CW005` | `5B` | адрес слова 5 ядра | FOREX_CORE.mad:300 |
| `DPRAD` | `74010B` | внешний адрес DATAPR (DATAPR) | FOREX_CORE.mad:111 |
| `DEC_38` | `38` | . прочитать индексный регистр-модификатор [счим] | FOREX_CORE.mad:241 |
| `DEC_43` | `43` | . прочитать индексный регистр-модификатор [счим] | FOREX_CORE.mad:224 |
| `DMB07` | `40007B` | адрес 0o40007 — база *DUMON* | FOREX_CORE.mad:110 |
| `DMC04` | `4026B` | *DUMON*+4 | FOREX_CORE.mad:105 |
| `DMC05` | `4027B` | *DUMON*+5 | FOREX_CORE.mad:116 |
| `DMC06` | `4030B` | *DUMON*+6 | FOREX_CORE.mad:121 |
| `DUMMYL` | `5` | COMMON *DUMON*: 5 слов | FOREX_CORE.mad:41 |
| `DMTIM` | `4025B` | *DUMON*+3 — время/режим | FOREX_CORE.mad:94 |
| `ENTTA` | `4006B` | база таблицы ENTRY* | FOREX_CORE.mad:100 |
| `ENTTLN` | `50B` | COMMON ENTRY*: 40 слов | FOREX_CORE.mad:280 |
| `X57M6` | `6B` | экстракод *57 / режим 6 | FOREX_CORE.mad:84 |
| `FLGAD` | `4002B` | флаг справки FLGEX* | FOREX_CORE.mad:188 |
| `FMRZB` | `4035B` | маска RZB форматирования | FOREX_CORE.mad:163 |
| `FMSBR` | `4034B` | маска SBR форматирования | FOREX_CORE.mad:162 |
| `FULAD` | `4004B` | флаг «полный листинг» | FOREX_CORE.mad:115 |
| `GATAD` | `7417B` | атрибут GOST-строки для экстракода *36 | FOREX_CORE.mad:219 |
| `INFAD` | `4036B` | дескриптор INF | FOREX_CORE.mad:168 |
| `IC033` | `33B` | константа 33 (S3 0o510302) | FOREX_CORE.mad:74 |
| `IM150` | `1500B` | режим 1500 (S3 0o510302) | FOREX_CORE.mad:73 |
| `IM170` | `1700B` | начальный режим 1700 (S3 0o510301) | FOREX_CORE.mad:69 |
| `LDADDR` | `74022B` | внешний адрес загрузчика оверлеев LOADAN | FOREX_CORE.mad:132 |
| `LGTAD` | `4032B` | TEXT-имя LO*GEN | FOREX_CORE.mad:136 |
| `LSTAD` | `4031B` | TEXT-имя LO*SYN | FOREX_CORE.mad:131 |
| `MK760` | `7760B` | маска 0o7760 | FOREX_CORE.mad:475 |
| `MK761` | `7761B` | маска 0o7761 | FOREX_CORE.mad:483 |
| `MK763` | `7763B` | маска 0o7763 | FOREX_CORE.mad:487 |
| `MISAD` | `40037B` | база сообщения MIST | FOREX_CORE.mad:199 |
| `MRT22` | `22B` | режим реального времени (ntr 22) | FOREX_CORE.mad:142 |
| `ML771` | `7771B` | множитель 0o7771 | FOREX_CORE.mad:479 |
| `NOLAD` | `4003B` | флаг «нет листинга» | FOREX_CORE.mad:104 |
| `OCDAD` | `74013B` | внешний адрес OCTTDE (OCTTDE) | FOREX_CORE.mad:158 |
| `ONEW` | `1` | одно слово / константа 1 | FOREX_CORE.mad:37 |
| `PGVAD` | `74012B` | внешний адрес PAGEGV (GIV/PG) | FOREX_CORE.mad:125 |
| `PTKAD` | `74011B` | внешний адрес PAGETK (TAK/PG) | FOREX_CORE.mad:194 |
| `PRMSAD` | `40023B` | внутренний адрес PRTMSG (PRIN) | FOREX_CORE.mad:205 |
| `R100A` | `4033B` | константа =R100.0 | FOREX_CORE.mad:148 |
| `RZPAG` | `70000B` | нулевая страница резидентной памяти | FOREX_CORE.mad:250 |
| `RETCL` | `4023B` | ячейка адреса возврата RET | FOREX_CORE.mad:80 |
| `RETLR` | `13` | номер индексного регистра связывания M13 | FOREX_CORE.mad:79 |
| `RETMA` | `40050B` | ячейка модификатора возврата | FOREX_CORE.mad:189 |
| `SYMTG` | `65412B` | цель перехода в таблице символов | FOREX_CORE.mad:414 |
| `TIMCL` | `4024B` | счётчик TIME | FOREX_CORE.mad:89 |
| `TTXAD` | `4037B` | дескриптор TTEX | FOREX_CORE.mad:177 |
| `TTXBA` | `40033B` | база текстовых констант TTEX | FOREX_CORE.mad:172 |

### `src/FOREX_RUNTIME.mad`

| Имя константы | Значение | Роль | Источник |
|---|---|---|---|
| `ALLMS` | `77777B` | маска «все единицы» | S1:15677 |
| `BS14R` | `14` | номер индексного регистра базы M14 | S1:15541 |
| `DW0000` | `0000000000077777` | ; S6:5074 MASK15 = 0000000000077777 | S6:5074 |
| `DW0001` | `00000000 00000000` | ; S1:15691 | S1:15691 |
| `DW0002` | `00000000 00000001` | ; S1:15694 | S1:15694 |
| `DW0003` | `00000000 00000002` | ; S1:15703 | S1:15703 |
| `DW0004` | `00000000 00001777` | ; S1:15696 | S1:15696 |
| `DW0005` | `00100000 00000000` | ; S1:15697 | S1:15697 |
| `DW0006` | `17 7777 7777 7777` | ; S7:454 | S7:454 |
| `DW0007` | `37777774 77777477` | ; S1:15701 | S1:15701 |
| `DW0008` | `77270707 00000000` | ; S1:15704 | S1:15704 |
| `DTDAYS` | `64+16` | выделение DD из FUN 67B | S5:7664 |
| `DTMISH` | `64-24` | выделение индекса месяца | S5:7677 |
| `DTMOSH` | `64+35` | выделение MM из FUN 67B | S5:7668 |
| `DTTMSH` | `64-22` | выделение HH.MM из FUN 67B | S5:7684 |
| `DTYRSH` | `64-14` | выделение YY из FUN 67B | S5:7679 |
| `DEC_7` | `7` | ; S1:15596 | S1:15596 |
| `FIXM2` | `2` | режим NTR 2 / шаг 2 | S5:7646 |
| `F002DS` | `77776B` | ячейка передачи FT*002 | S1:15584 |
| `F003DS` | `77775B` | ячейка передачи FT*003 | S1:15586 |
| `F521DS` | `77257B` | ячейка передачи FT*521 | S1:15578 |
| `F531DS` | `77247B` | ячейка передачи FT*531 | S1:15572 |
| `F541DS` | `77237B` | ячейка передачи FT*541 | S1:15568 |
| `F561DS` | `77217B` | ячейка передачи FT*561 | S1:15574 |
| `F571DS` | `77207B` | ячейка передачи FT*571 | S1:15566 |
| `F611DS` | `77167B` | ячейка передачи FT*611 | S1:15570 |
| `F621DS` | `77157B` | ячейка передачи FT*621 | S1:15576 |
| `F641DS` | `77137B` | ячейка передачи FT*641 | S1:15582 |
| `F721DS` | `77057B` | ячейка передачи FT*721 | S1:15580 |
| `FTDTBA` | `77766B` | база таблицы передач FORMAT | S1:15549 |
| `FTADFL` | `103B` | маска поля адреса в FORMAT | S1:15543 |
| `FTOFMK` | `155B` | маска смещения в FORMAT | S1:15559 |
| `GOSTBL` | `6H` | пустой GOST-формат | S7:457 |
| `INTZ` | `0` | целое 0 | S6:5075 |
| `ISOCSH` | `54B` | сдвиг ASN 54B при сборке 8-символьного слова | S1:15685 |
| `ISOWSH` | `64` | сдвиг GOST/ISO-поля на 64 разряда | S5:7676 |
| `LIBBLN` | `2000B` | длина BUFFER PU (0o2000 слов) | S1:15591 |
| `LIT_10` | `10` | ; S6:5067 | S6:5067 |
| `LIT10M` | `10000000 00000000` | ; S1:15587 FTDCNS: LOG 10000000 00000000 | S1:15587 |
| `LIT_2` | `2` | ; S6:5058 | S6:5058 |
| `LIT_3` | `3` | ; S6:5055 | S6:5055 |
| `MODE_6` | `6` | режим NTR 6 | S5:7658 |
| `MNTHIB` | `24` | база индекса месяца | S5:7671 |
| `OCTSDM` | `=777 7777-C` | маска 6 цифр OCTTDE | S6:5047 |
| `ONEW` | `1` | одно слово / константа 1 | S1:15646 |
| `P5` | `100000.0` | вещественный масштаб 10^5 | S6:5077 |
| `RMOD3` | `3` | режим NTR 3 (вещественный) | S1:15612 |
| `RETLR` | `13` | номер индексного регистра связывания M13 | S1:15597 |
| `STKOF1` | `-1` | ; S5:7713 | S5:7713 |
| `STKOF2` | `-2` | ; S5:7662 | S5:7662 |
| `STKOF3` | `-3` | ; S5:7666 | S5:7666 |
| `STKOF4` | `-4` | ; S5:7678 | S5:7678 |
| `STKOF5` | `-5` | ; S5:7712 | S5:7712 |
| `STKOF6` | `-6` | ; S5:7694 | S5:7694 |
| `SOM` | `-8` | ; S5:7688 | S5:7688 |
| `TL0000` | `''000000''` | ; S6:5083 ZERO = 8TEXT «000000» | S6:5083 |
| `TL0001` | `1H'055'` | ; S5:7717 | S5:7717 |
| `TL0002` | `2H '200'` | ; S5:7715 | S5:7715 |
| `TL0003` | `3H00` | ; S5:7718 | S5:7718 |
| `TL0004` | `=6H00` | ; S5:7705 | S5:7705 |
| `TL0005` | `6H0000` | ; S5:7729 | S5:7729 |
| `TL0006` | `6H000000` | ; S7:458 ZERO = ISO 6H000000 | S7:458 |
| `TL0007` | `6H000 00` | ; S5:7719 | S5:7719 |
| `TL0008` | `=6H00/00/` | ; S5:7708 | S5:7708 |
| `TL0009` | `6H03 0` | ; S5:7728 | S5:7728 |
| `TL0010` | `6HABГCEH` | ; S5:7725 | S5:7725 |
| `TL0011` | `6HARRAY` | ; S1:15710 | S1:15710 |
| `TL0012` | `6HAПPMAЯ` | ; S5:7723 | S5:7723 |
| `TL0013` | `6HERROR` | ; S1:15707 | S1:15707 |
| `TL0014` | `6HIN STA` | ; S1:15708 | S1:15708 |
| `TL0015` | `6HNDART` | ; S1:15709 | S1:15709 |
| `TL0016` | `6HOKTHOЯ` | ; S5:7730 | S5:7730 |
| `TL0017` | `6H 00.00` | ; S5:7726 | S5:7726 |
| `TL0018` | `=6H'17''17'''''''''` | ; S5:7704 | S5:7704 |
| `TL0019` | `6H'201'  '200'7` | ; S5:7714 | S5:7714 |
| `TL0020` | `6H'231'  ЯHB` | ; S5:7721 | S5:7721 |
| `TL0021` | `=6H'3''17''''17''17'''` | ; S5:7707 | S5:7707 |
| `TL0022` | `6HФEBMAP` | ; S5:7722 | S5:7722 |
| `TL0023` | `6HДEK` | ; S5:7731 | S5:7731 |
| `TL0024` | `6HИЮHИЮЛ` | ; S5:7724 | S5:7724 |
| `FUNDTM` | `67B.DD.MM.YY.HH.MM` | FUN 67B — системная дата/время | S5:7657 |
| `DBFLN` | `2` | DATA* — 2-словный буфер даты | S5:7646 |
| `MNTHFO` | `00 776` | маска поля месяца в FUN 67B | S5:7732 |
| `OCTISS` | `64-8` | сдвиг ASN ISO-кода цифры | S6:5070 |
| `P4` | `10000.0` | вещественный масштаб 10^4 | S6:5078 |
| `P3` | `1000.0` | вещественный масштаб 10^3 | S6:5079 |
| `P2` | `100.0` | вещественный масштаб 10^2 | S6:5080 |
| `P1` | `10.0` | вещественный масштаб 10^1 | S6:5081 |

### `include/FOREX_ROOT.mad`

| Имя константы | Значение | Роль | Источник |
|---|---|---|---|
| `BS14R` | `14` | номер индексного регистра базы M14 | S1:15474 |
| `BUFALN` | `4000B` | COMMON *A*: 2048 слов | S1:15465 |
| `DEC_15` | `15` | ; S1:16796 | S1:16796 |
| `DUMMYL` | `5` | COMMON *DUMON*: 5 слов | S1:15454 |
| `ENTTLN` | `50B` | COMMON ENTRY*: 40 слов | S1:15449 |
| `ERRTRT` | `18H'200'0OШ. TPAHCЛЯTOPA'231' ; роль: сообщение «ОШ. ТРАНСЛЯТОРА»; источник: FOREX_ROOT.mad:112` | — | — |
| `FIXM2` | `2` | режим NTR 2 / шаг 2 | S1:16801 |
| `GOST_V` | `1H'212'` | GOST-код «В» | S1:15520 |
| `GOSTVR` | `6HBPEMЯ-` | GOST «ВРЕМЯ-» | S1:15521 |
| `GOSTYA` | `1H'231'` | GOST-код «Я» | S1:15523 |
| `MODE_6` | `6` | режим NTR 6 | S1:15469 |
| `MRT22D` | `18` | NTR 18 (десятичное) = 22 восьмеричное — реальное время | S1:15491 |
| `ONEW` | `1` | одно слово / константа 1 | S1:15450 |
| `PG17AD` | `17B` | адрес 17B в механизме страниц | S1:16807 |
| `PGMD73` | `=73401` | режим/маска страницы 73401 | S1:16789 |
| `PGBLKM` | `=4000` | маска блока страницы =4000 | S1:16827 |
| `PG67CD` | `=:11 4037 77` | код экстракода 67 | S1:16793 |
| `PGFLGS` | `64+12` | выделение флага страницы | S1:16790 |
| `PGGO1` | `=:00 2677` | код перехода GO | S1:16829 |
| `PGGO2` | `=:00 6736 77` | код перехода GO (вариант) | S1:16830 |
| `PGWDSH` | `64-20` | выделение слова адреса страницы | S1:16798 |
| `PRBKLN` | `002` | длина блока описания печати INF | S1:15518 |
| `RMOD3` | `3` | режим NTR 3 (вещественный) | S1:15495 |
| `RETLR` | `13` | номер индексного регистра связывания M13 | S1:15467 |
| `RMWD4` | `4` | COMMON RM*: 4 слова | S1:16786 |
| `STKOF2` | `-2` | ; (COMM) ; S1:16800 M14 = -2 (счётчик) | S1:16800 |
| `TXLGEN` | `8HLO*GEN` | TEXT-имя оверлея LO*GEN | S1:15526 |
| `TXLSYN` | `8HLO*SYN` | TEXT-имя оверлея LO*SYN | S1:15525 |
| `TIMSCL` | `=R100.0` | масштаб пересчёта времени в секунды | S1:15494 |
| `TIMSEA` | `=6H'''17''17''17''17''17'` | разделители времени (S1:15499) | S1:15499 |
| `TIMSEB` | `=6H'17''17''17''''17''17'` | разделители времени (S1:15500) | S1:15500 |
| `TIMSEC` | `=6H'''''''16'''''` | разделители времени (S1:15501) | S1:15501 |
| `LNK15` | `15` | номер регистра связывания M15 | S1:16796,16826 |
| `PGSTP2` | `2` | шаг обхода INFLOA в PGCOPL | S1:16801,16804 |

## 3. Оставшиеся литералы и причины

| Что | Где | Почему не вынесено в EQU |
|---|---|---|
| Префиксы индексных регистров `13,`, `14,`, `15,`, `12,`, `7,`, `11,`, `9,`, `8,` | все три файла | Это синтаксис МАДЛЕН (указание модификации адреса), а не операнд-литерал; замена ломает разбор команды. Номер регистра как **операнд** (`ITA,13`, `ATI,15`) вынесен в `RETLR`, `BS14R`, `LNK15`. |
| Экстракоды `*57`, `*64`, `*67`, `*72`, `*20`, `*36`, `*56`, `*60`, `*62`, `*47`, `*70`, `*74`, `Z00` | все три файла | Мнемоники экстракодов, а не числа; их кодировка фиксирована архитектурой. |
| Адресная колонка `0o510300 … 0o510347` | `include/FOREX_ROOT.mad` | Физические адреса ленты monsys.9; сохранены побайтово по условию задачи. |
| Метки слов `С слово NNNN @0o… = 0o…` и `С   → …` | `src/FOREX_CORE.mad` | Проверяются `tests/check-source-words.py` (там — LO_*); по условию задачи не трогаются. |
| Номера строк источников `S1:15529`, `S6:5044`, `; S5:7700` | комментарии | Ссылки на листинг, не операнды. |
| Символические адресные выражения `*DUMON*+3`, `DATA*+1`, `WRTLBR+1`, `RM*+2`, `*00077 - FLCON`, `DEC-OCTBAS` | все три файла | Это адреса относительно меток/баз, а не литералы;адресная арифметика сохранена как часть адресного выражения. |
| Имена директив `BSS`, `LC`, `PU`, `OCT`, `GOST`, `ISO`, `TEXT`, `8TEXT`, `LOG`, `REAL`, `EQU` | все три файла | Мнемоники директив МАДЛЕН. |
| `ИМЯ_*`, `DATAPR`, `TAK/PG`, `GIV/PG`, `FOREX`, `CONST`, `COMEQ`, `OPRTR`, `ПP`, `LOADAN`, `LO*SYN`, `LO*GEN`, `A/I0`, `ENTRY*`, `*DUMON*` | объявления SUBP/COMMON | Официальные имена символов библиотеки 21; сохранены для совместимости с LIBREFER и обязательными символами теста. |

Итог проверки (последний прогон): 0 незаменённых литералов в операндах трёх файлов;
`bash tests/check-annotations.sh` → 0; `python3 tests/check-source-words.py` → 0.

## 4. Короткие имена (≤ 6 символов) → полные имена

Первая колонка — короткое имя (≤ 6 символов, как его видит МАДЛЕН), полное
описательное имя вынесено во вторую колонку обычным текстом (не backticks,
чтобы не восприниматься как МАДЛЕН-имя). Полное имя также сохранено в
trailing-комментарии каждого определения (`; полное имя: …` / `. полное имя: …`).
МАДЛЕН различает только первые 6 знаков, поэтому все имена уникальны по первым 6 символам.

| Короткое имя | Полное имя | Файл |
|---|---|---|
| `*DUMON` | *DUMON* | FOREX_CORE, FOREX_ROOT |
| `AOC4K` | ADDR_OCT_4000 | FOREX_CORE |
| `AOC50` | ADDR_OCT_50 | FOREX_CORE |
| `ALLMS` | ALL_ONES_MASK | FOREX_RUNTIME |
| `AI0AD` | A_I0_ADDR | FOREX_CORE |
| `BS16A` | BASE16_ADDR | FOREX_CORE |
| `BS14R` | BASE_REG14 | FOREX_CORE, FOREX_ROOT, FOREX_RUNTIME |
| `BUFALN` | BUFFER_A_LEN | FOREX_CORE, FOREX_ROOT |
| `CHECKF` | CHECKFL* | FOREX_CORE, FOREX_ROOT |
| `CHKAD` | CHECK_ADDR | FOREX_CORE |
| `C11200` | CORE_ADDR_11200 | FOREX_CORE |
| `CA1200` | CORE_ADDR_1200 | FOREX_CORE |
| `CA1247` | CORE_ADDR_1247 | FOREX_CORE |
| `CA1263` | CORE_ADDR_1263 | FOREX_CORE |
| `C16617` | CORE_ADDR_16617 | FOREX_CORE |
| `CA231` | CORE_ADDR_231 | FOREX_CORE |
| `C30453` | CORE_ADDR_30453 | FOREX_CORE |
| `C31056` | CORE_ADDR_31056 | FOREX_CORE |
| `C36464` | CORE_ADDR_36464 | FOREX_CORE |
| `C37013` | CORE_ADDR_37013 | FOREX_CORE |
| `CA4040` | CORE_ADDR_4040 | FOREX_CORE |
| `CA4041` | CORE_ADDR_4041 | FOREX_CORE |
| `CA4042` | CORE_ADDR_4042 | FOREX_CORE |
| `CA4043` | CORE_ADDR_4043 | FOREX_CORE |
| `CA4044` | CORE_ADDR_4044 | FOREX_CORE |
| `CA4045` | CORE_ADDR_4045 | FOREX_CORE |
| `CA4046` | CORE_ADDR_4046 | FOREX_CORE |
| `CA4047` | CORE_ADDR_4047 | FOREX_CORE |
| `CA4050` | CORE_ADDR_4050 | FOREX_CORE |
| `CA4051` | CORE_ADDR_4051 | FOREX_CORE |
| `CA4052` | CORE_ADDR_4052 | FOREX_CORE |
| `CA4053` | CORE_ADDR_4053 | FOREX_CORE |
| `CA4054` | CORE_ADDR_4054 | FOREX_CORE |
| `CA4055` | CORE_ADDR_4055 | FOREX_CORE |
| `CA4056` | CORE_ADDR_4056 | FOREX_CORE |
| `CA4144` | CORE_ADDR_4144 | FOREX_CORE |
| `C44000` | CORE_ADDR_44000 | FOREX_CORE |
| `C44745` | CORE_ADDR_44745 | FOREX_CORE |
| `CA4543` | CORE_ADDR_4543 | FOREX_CORE |
| `C46555` | CORE_ADDR_46555 | FOREX_CORE |
| `CA5317` | CORE_ADDR_5317 | FOREX_CORE |
| `C55451` | CORE_ADDR_55451 | FOREX_CORE |
| `CA56` | CORE_ADDR_56 | FOREX_CORE |
| `C61200` | CORE_ADDR_61200 | FOREX_CORE |
| `CA6264` | CORE_ADDR_6264 | FOREX_CORE |
| `CA6441` | CORE_ADDR_6441 | FOREX_CORE |
| `C70031` | CORE_ADDR_70031 | FOREX_CORE |
| `C70035` | CORE_ADDR_70035 | FOREX_CORE |
| `C70042` | CORE_ADDR_70042 | FOREX_CORE |
| `C70043` | CORE_ADDR_70043 | FOREX_CORE |
| `C70044` | CORE_ADDR_70044 | FOREX_CORE |
| `C70045` | CORE_ADDR_70045 | FOREX_CORE |
| `C70046` | CORE_ADDR_70046 | FOREX_CORE |
| `C70047` | CORE_ADDR_70047 | FOREX_CORE |
| `C70050` | CORE_ADDR_70050 | FOREX_CORE |
| `CA7017` | CORE_ADDR_7017 | FOREX_CORE |
| `C74757` | CORE_ADDR_74757 | FOREX_CORE |
| `C75120` | CORE_ADDR_75120 | FOREX_CORE |
| `C75451` | CORE_ADDR_75451 | FOREX_CORE |
| `C75545` | CORE_ADDR_75545 | FOREX_CORE |
| `C75663` | CORE_ADDR_75663 | FOREX_CORE |
| `C76245` | CORE_ADDR_76245 | FOREX_CORE |
| `C76462` | CORE_ADDR_76462 | FOREX_CORE |
| `CMOD3` | CORE_MODE3 | FOREX_CORE |
| `CW001` | CORE_WORD1 | FOREX_CORE |
| `CW002` | CORE_WORD2 | FOREX_CORE |
| `CW004` | CORE_WORD4 | FOREX_CORE |
| `CW005` | CORE_WORD5 | FOREX_CORE |
| `DPRAD` | DATAPR_ADDR | FOREX_CORE |
| `DW0000` | DATA_WORD_0000000000077777 | FOREX_RUNTIME |
| `DW0001` | DATA_WORD_00000000_00000000 | FOREX_RUNTIME |
| `DW0002` | DATA_WORD_00000000_00000001 | FOREX_RUNTIME |
| `DW0003` | DATA_WORD_00000000_00000002 | FOREX_RUNTIME |
| `DW0004` | DATA_WORD_00000000_00001777 | FOREX_RUNTIME |
| `DW0005` | DATA_WORD_00100000_00000000 | FOREX_RUNTIME |
| `DW0006` | DATA_WORD_17_7777_7777_7777 | FOREX_RUNTIME |
| `DW0007` | DATA_WORD_37777774_77777477 | FOREX_RUNTIME |
| `DW0008` | DATA_WORD_77270707_00000000 | FOREX_RUNTIME |
| `DBFLN` | DATE_BUF_LEN | FOREX_RUNTIME |
| `DTDAYS` | DATE_DAY_SHIFT | FOREX_RUNTIME |
| `DTENDC` | DATE_END_CHECK | FOREX_RUNTIME |
| `DATEFM` | DATE_FMT | FOREX_CORE/FOREX_RUNTIME/FOREX_ROOT |
| `DGET` | DATE_GET | FOREX_RUNTIME |
| `DTMISH` | DATE_MONTH_INDEX_SHIFT | FOREX_RUNTIME |
| `DTMOSH` | DATE_MONTH_SHIFT | FOREX_RUNTIME |
| `DPARSE` | DATE_PARSE | FOREX_RUNTIME |
| `DPREPA` | DATE_PREPARE | FOREX_RUNTIME |
| `DPREPB` | DATE_PREP_BASE | FOREX_RUNTIME |
| `DATAPR` | DATE_PRINT | FOREX_ROOT, FOREX_RUNTIME |
| `DPRTN` | DATE_PRINT_RETURN | FOREX_CORE, FOREX_ROOT |
| `DTSTAD` | DATE_STACK_ADJUST | FOREX_RUNTIME |
| `DTTMSH` | DATE_TIME_SHIFT | FOREX_RUNTIME |
| `DTWTCS` | DATE_WTC_SET | FOREX_RUNTIME |
| `DTYRSH` | DATE_YEAR_SHIFT | FOREX_RUNTIME |
| `DYMSK` | DAY_MASK | FOREX_RUNTIME |
| `DMB07` | DUMON_BASE_7 | FOREX_CORE |
| `DMC04` | DUMON_CELL4 | FOREX_CORE |
| `DMC05` | DUMON_CELL5 | FOREX_CORE |
| `DMC06` | DUMON_CELL6 | FOREX_CORE |
| `DUMMYL` | DUMON_LEN | FOREX_CORE, FOREX_ROOT |
| `DMTIM` | DUMON_TIME_CELL | FOREX_CORE |
| `ENTTA` | ENTRY_TAB_ADDR | FOREX_CORE |
| `ENTTLN` | ENTRY_TAB_LEN | FOREX_CORE, FOREX_ROOT |
| `ERRTRL` | ERR_TRANSLATOR | FOREX_CORE, FOREX_ROOT |
| `ERRTRT` | ERR_TRANSLATOR_TEXT | FOREX_ROOT |
| `X57M6` | EX57_MODE6 | FOREX_CORE |
| `FIXM2` | FIXED_MODE_2 | FOREX_ROOT, FOREX_RUNTIME |
| `FLGAD` | FLGEX_ADDR | FOREX_CORE |
| `FLAFT` | FL_AFTER_WRITE | FOREX_RUNTIME |
| `FLALT` | FL_ALT_CASE | FOREX_RUNTIME |
| `FLCON` | FL_CONST_BASE | FOREX_RUNTIME |
| `FLWTC` | FL_WTC_CASE | FOREX_RUNTIME |
| `FMRZB` | FMT_RZB_MASK | FOREX_CORE |
| `FMSBR` | FMT_SBR_MASK | FOREX_CORE |
| `FXCOR` | FOREX_CORE | FOREX_CORE |
| `FXSTR` | FOREX_START | FOREX_CORE/FOREX_RUNTIME/FOREX_ROOT |
| `F002DS` | FT002_DISPATCH | FOREX_RUNTIME |
| `F003DS` | FT003_DISPATCH | FOREX_RUNTIME |
| `F521DS` | FT521_DISPATCH | FOREX_RUNTIME |
| `F531DS` | FT531_DISPATCH | FOREX_RUNTIME |
| `F541DS` | FT541_DISPATCH | FOREX_RUNTIME |
| `F561DS` | FT561_DISPATCH | FOREX_RUNTIME |
| `F571DS` | FT571_DISPATCH | FOREX_RUNTIME |
| `F611DS` | FT611_DISPATCH | FOREX_RUNTIME |
| `F621DS` | FT621_DISPATCH | FOREX_RUNTIME |
| `F641DS` | FT641_DISPATCH | FOREX_RUNTIME |
| `F721DS` | FT721_DISPATCH | FOREX_RUNTIME |
| `FTDCNS` | FTD_CONST | FOREX_RUNTIME |
| `FTDLOP` | FTD_LOOP | FOREX_RUNTIME |
| `FTDOFS` | FTD_OFFSET | FOREX_RUNTIME |
| `FTDSTO` | FTD_STORE | FOREX_RUNTIME |
| `FTDTEN` | FTD_TABLE_ | FOREX_CORE/FOREX_RUNTIME/FOREX_ROOT |
| `FTDTSB` | FTD_TABLE_BASE | FOREX_RUNTIME |
| `FTDTBA` | FTD_TABLE_BASE_ADDR | FOREX_RUNTIME |
| `FTDTE` | FTD_TABLE_END | FOREX_RUNTIME |
| `FTADFL` | FT_ADDR_FIELD | FOREX_RUNTIME |
| `FTDISP` | FT_FORMAT_DISPATCH | FOREX_RUNTIME |
| `FTLIO` | FT_LIBRARY_IO | FOREX_RUNTIME |
| `FTLBFR` | FT_LIB_BUFFER | FOREX_RUNTIME |
| `FTOFMK` | FT_OFFSET_MASK | FOREX_RUNTIME |
| `FULISF` | FULISFL* | FOREX_CORE, FOREX_ROOT |
| `FULAD` | FULIS_ADDR | FOREX_CORE |
| `FUNDTM` | FUN_DATE_TIME | FOREX_RUNTIME |
| `GATAD` | GOST_ATTR_ADDR | FOREX_CORE |
| `GOSTBL` | GOST_BLANK | FOREX_RUNTIME |
| `GOSTVR` | GOST_VREMYA | FOREX_ROOT |
| `GOSTYA` | GOST_YA | FOREX_ROOT |
| `IFLOD` | INFLOAD* | FOREX_ROOT |
| `INFAD` | INF_ADDR | FOREX_CORE |
| `IC033` | INIT_CONST_33 | FOREX_CORE |
| `INITFO` | INIT_FOREX | FOREX_CORE, FOREX_ROOT |
| `IM150` | INIT_MODE_1500 | FOREX_CORE |
| `IM170` | INIT_MODE_1700 | FOREX_CORE |
| `INTZ` | INT_ZERO | FOREX_RUNTIME |
| `ISOCSH` | ISO_CODE_SHIFT | FOREX_RUNTIME |
| `ISOWSH` | ISO_WORD_SHIFT | FOREX_RUNTIME |
| `KCNT` | KCOUNT* | FOREX_ROOT |
| `L00023` | L*00023 | FOREX_RUNTIME |
| `L00027` | L*00027 | FOREX_RUNTIME |
| `L00042` | L*00042 | FOREX_RUNTIME |
| `L00045` | L*00045 | FOREX_RUNTIME |
| `L00050` | L*00050 | FOREX_RUNTIME |
| `L00053` | L*00053 | FOREX_RUNTIME |
| `LIBBLN` | LIB_BUFFER_LEN | FOREX_RUNTIME |
| `LNK15` | LINK_REG_15 | FOREX_ROOT |
| `LIT10M` | LIT_10000000_00000000 | FOREX_RUNTIME |
| `LDADDR` | LOADANGO_ADDR | FOREX_CORE |
| `LODOVL` | LOAD_OVERLAYS | FOREX_CORE, FOREX_ROOT |
| `LGTAD` | LO_GEN_TEXT_ADDR | FOREX_CORE |
| `LSTAD` | LO_SYN_TEXT_ADDR | FOREX_CORE |
| `MK760` | MASK_7760 | FOREX_CORE |
| `MK761` | MASK_7761 | FOREX_CORE |
| `MK763` | MASK_7763 | FOREX_CORE |
| `MISAD` | MIST_BASE_ADDR | FOREX_CORE |
| `MRT22` | MODE_RT_OCT22 | FOREX_CORE |
| `MRT22D` | MODE_RT_OCT22_DEC | FOREX_ROOT |
| `MNTHFD` | MONTH_FIELD | FOREX_RUNTIME |
| `MNTHFO` | MONTH_FIELD_OCT | FOREX_RUNTIME |
| `MNTHIB` | MONTH_INDEX_BASE | FOREX_RUNTIME |
| `MNTHNM` | MONTH_NAMES | FOREX_RUNTIME |
| `ML771` | MUL_7771 | FOREX_CORE |
| `NOLISF` | NOLISFL* | FOREX_CORE, FOREX_ROOT |
| `NOLAD` | NOLIS_ADDR | FOREX_CORE |
| `OCTBAS` | OCT_BASE | FOREX_RUNTIME |
| `OCTBGN` | OCT_BEGIN | FOREX_RUNTIME |
| `OCTCYC` | OCT_CYCLE | FOREX_RUNTIME |
| `OCTTDE` | OCT_DEC | FOREX_ROOT, FOREX_RUNTIME |
| `OCDAD` | OCT_DEC_ADDR | FOREX_CORE |
| `OCTEXF` | OCT_DEC_EXFOR | FOREX_RUNTIME |
| `OCTEDL` | OCT_EX_DIGIT_LOOP | FOREX_RUNTIME |
| `OCTERT` | OCT_EX_RETURN | FOREX_RUNTIME |
| `OCTISS` | OCT_ISO_SHIFT | FOREX_RUNTIME |
| `OCTSDM` | OCT_SIX_DIGIT_MASK | FOREX_RUNTIME |
| `OCTSYM` | OCT_SYMBOL | FOREX_RUNTIME |
| `ONEW` | ONE_WORD | FOREX_CORE, FOREX_ROOT, FOREX_RUNTIME |
| `PG17AD` | PAGE17_ADDR | FOREX_ROOT |
| `PAGEGV` | PAGE_GIVE | FOREX_ROOT |
| `PGVAD` | PAGE_GIVE_ADDR | FOREX_CORE |
| `PGMD73` | PAGE_MODE_73401 | FOREX_ROOT |
| `PAGETK` | PAGE_TAKE | FOREX_ROOT |
| `PTKAD` | PAGE_TAKE_ADDR | FOREX_CORE |
| `PGBLKM` | PG_BLOCK_MASK | FOREX_ROOT |
| `PGCOMM` | PG_COMMON | FOREX_ROOT |
| `PGCOPL` | PG_COPY_LOOP | FOREX_ROOT |
| `PGX67` | PG_EX67 | FOREX_ROOT |
| `PG67CD` | PG_EX67_CODE | FOREX_ROOT |
| `PG67CN` | PG_EX67_CONST | FOREX_ROOT |
| `PG67SA` | PG_EX67_SAVE | FOREX_ROOT |
| `PGFLSA` | PG_FLAG_SAVE | FOREX_ROOT |
| `PGFLGS` | PG_FLAG_SHIFT | FOREX_ROOT |
| `PGGO1` | PG_GO_CODE_1 | FOREX_ROOT |
| `PGGO2` | PG_GO_CODE_2 | FOREX_ROOT |
| `PGPGGO` | PG_PG_GO | FOREX_ROOT |
| `PGRST7` | PG_RESTORE17 | FOREX_ROOT |
| `PGSAVS` | PG_SAVE_S | FOREX_ROOT |
| `PGSHWD` | PG_SHIFT_WORD | FOREX_ROOT |
| `PGSTP2` | PG_STEP_2 | FOREX_ROOT |
| `PGWDSH` | PG_WORD_SHIFT | FOREX_ROOT |
| `PGWRKB` | PG_WORK_BASE | FOREX_ROOT |
| `P1` | POW10_1 | FOREX_RUNTIME |
| `P2` | POW10_2 | FOREX_RUNTIME |
| `P3` | POW10_3 | FOREX_RUNTIME |
| `P4` | POW10_4 | FOREX_RUNTIME |
| `P5` | POW10_5 | FOREX_RUNTIME |
| `P10_06` | POW10_6 | FOREX_CORE/FOREX_RUNTIME/FOREX_ROOT |
| `PRBKLN` | PRINT_BLOCK_LEN | FOREX_ROOT |
| `PRTMSG` | PRINT_MESSAGE | FOREX_CORE, FOREX_ROOT |
| `PRMSAD` | PRINT_MESSAGE_ADDR | FOREX_CORE |
| `PRTIME` | PRINT_TIME | FOREX_CORE, FOREX_ROOT |
| `R100A` | R100_ADDR | FOREX_CORE |
| `RMOD3` | REAL_MODE_3 | FOREX_ROOT, FOREX_RUNTIME |
| `RZPAG` | RESIDENT_ZERO_PAGE | FOREX_CORE |
| `RETCL` | RET_CELL | FOREX_CORE |
| `RETLR` | RET_LINK_REG | FOREX_CORE, FOREX_ROOT, FOREX_RUNTIME |
| `RETMA` | RET_MOD_ADDR | FOREX_CORE |
| `RMWD4` | RM_WORDS_4 | FOREX_ROOT |
| `STKOF1` | STACK_OFF_M1 | FOREX_RUNTIME |
| `STKOF2` | STACK_OFF_M2 | FOREX_ROOT, FOREX_RUNTIME |
| `STKOF3` | STACK_OFF_M3 | FOREX_RUNTIME |
| `STKOF4` | STACK_OFF_M4 | FOREX_RUNTIME |
| `STKOF5` | STACK_OFF_M5 | FOREX_RUNTIME |
| `STKOF6` | STACK_OFF_M6 | FOREX_RUNTIME |
| `STKOF7` | STACK_OFF_M7 | FOREX_CORE/FOREX_RUNTIME/FOREX_ROOT |
| `SOM` | STACK_OFF_M8 | FOREX_RUNTIME |
| `SYMTG` | SYMTAB_TARGET | FOREX_CORE |
| `TL0000` | TEXT_LIT_000000 | FOREX_RUNTIME |
| `TL0001` | TEXT_LIT_1H_055 | FOREX_RUNTIME |
| `TL0002` | TEXT_LIT_2H_200 | FOREX_RUNTIME |
| `TL0003` | TEXT_LIT_3H00 | FOREX_RUNTIME |
| `TL0004` | TEXT_LIT_6H00 | FOREX_RUNTIME |
| `TL0005` | TEXT_LIT_6H0000 | FOREX_RUNTIME |
| `TL0006` | TEXT_LIT_6H000000 | FOREX_RUNTIME |
| `TL0007` | TEXT_LIT_6H000_00 | FOREX_RUNTIME |
| `TL0008` | TEXT_LIT_6H00_00 | FOREX_RUNTIME |
| `TL0009` | TEXT_LIT_6H03_0 | FOREX_RUNTIME |
| `TL0010` | TEXT_LIT_6HAB_CEH | FOREX_RUNTIME |
| `TL0011` | TEXT_LIT_6HARRAY | FOREX_RUNTIME |
| `TL0012` | TEXT_LIT_6HA_PMA | FOREX_RUNTIME |
| `TL0013` | TEXT_LIT_6HERROR | FOREX_RUNTIME |
| `TL0014` | TEXT_LIT_6HIN_STA | FOREX_RUNTIME |
| `TL0015` | TEXT_LIT_6HNDART | FOREX_RUNTIME |
| `TL0016` | TEXT_LIT_6HOKTHO | FOREX_RUNTIME |
| `TL0017` | TEXT_LIT_6H_00_00 | FOREX_RUNTIME |
| `TL0018` | TEXT_LIT_6H_17_17 | FOREX_RUNTIME |
| `TL0019` | TEXT_LIT_6H_201_200_7 | FOREX_RUNTIME |
| `TL0020` | TEXT_LIT_6H_231_HB | FOREX_RUNTIME |
| `TL0021` | TEXT_LIT_6H_3_17_17_17 | FOREX_RUNTIME |
| `TL0022` | TEXT_LIT_6H_EBMAP | FOREX_RUNTIME |
| `TL0023` | TEXT_LIT_6H_EK | FOREX_RUNTIME |
| `TL0024` | TEXT_LIT_6H_H | FOREX_RUNTIME |
| `TXLGEN` | TEXT_LO_GEN | FOREX_ROOT |
| `TXLSYN` | TEXT_LO_SYN | FOREX_ROOT |
| `TIMCL` | TIME_CELL | FOREX_CORE |
| `TIMMSK` | TIME_MASK | FOREX_RUNTIME |
| `TIMSCL` | TIME_SCALE | FOREX_ROOT |
| `TIMSEA` | TIME_SEP_A | FOREX_ROOT |
| `TIMSEB` | TIME_SEP_B | FOREX_ROOT |
| `TIMSEC` | TIME_SEP_C | FOREX_ROOT |
| `TTXAD` | TTEX_ADDR | FOREX_CORE |
| `TTXBA` | TTEX_BASE_ADDR | FOREX_CORE |
| `WRTLBR` | WRITLIBR | FOREX_RUNTIME |
| `XCOM` | X_COMEQ | FOREX_CORE/FOREX_RUNTIME/FOREX_ROOT |
| `XCON` | X_CONST | FOREX_CORE/FOREX_RUNTIME/FOREX_ROOT |
| `DATAPR` | X_DATE_PRINT | FOREX_CORE/FOREX_RUNTIME/FOREX_ROOT |
| `XFOR` | X_FOREX | FOREX_CORE/FOREX_RUNTIME/FOREX_ROOT |
| `OCTTDE` | X_OCT_DEC | FOREX_CORE/FOREX_RUNTIME/FOREX_ROOT |
| `XOPR` | X_OPRTR | FOREX_CORE/FOREX_RUNTIME/FOREX_ROOT |
| `LOADAN` | X_OVERLAY_LOADER | FOREX_CORE/FOREX_RUNTIME/FOREX_ROOT |
| `PAGEGV` | X_PAGE_GIVE | FOREX_CORE/FOREX_RUNTIME/FOREX_ROOT |
| `PAGETK` | X_PAGE_TAKE | FOREX_CORE/FOREX_RUNTIME/FOREX_ROOT |
| `YRMSK` | YEAR_MASK | FOREX_RUNTIME |
| `NMCHK` | ИМЯ_CHECK | FOREX_CORE |
| `NMCOM` | ИМЯ_COMEQ | FOREX_CORE |
| `NMCON` | ИМЯ_CONST | FOREX_CORE |
| `NMDPR` | ИМЯ_DATAPR | FOREX_CORE |
| `NMDUM` | ИМЯ_DUMON | FOREX_CORE |
| `NMENT` | ИМЯ_ENTRY | FOREX_CORE |
| `NMFEX` | ИМЯ_FLGEX | FOREX_CORE |
| `NMFOR` | ИМЯ_FOREX | FOREX_CORE |
| `NMFUL` | ИМЯ_FULIS | FOREX_CORE |
| `NMGIV` | ИМЯ_GIVPG | FOREX_CORE |
| `NMLDG` | ИМЯ_LOADANG | FOREX_CORE |
| `NMNOL` | ИМЯ_NOLIS | FOREX_CORE |
| `NMOCT` | ИМЯ_OCTTDEC | FOREX_CORE |
| `NMOPR` | ИМЯ_OPRTR | FOREX_CORE |
| `NMTAK` | ИМЯ_TAKPG | FOREX_CORE |

Всего переименовано: **306** имён; все короткие имена имеют длину ≤ 6
и уникальны по первым 6 символам (проверено `tests/check-label-length.sh`).

## 5. 6-символьное интерфейсное имя → полное интерфейсное имя

Интерфейсные имена (COMMON / SUBP / ENTRY, видимые монитором и оверлеями
LO*SYN / LO*GEN) укорочены до **первых 6 символов исходного имени БЭСМ-6**:
ассемблер и монитор различают только эти 6 знаков, поэтому такое
представление сохраняет linkage между всеми модулями.

| 6-символьное имя | Полное интерфейсное имя | Примечание |
|---|---|---|
| `OCTTDE` | OCTTDEC | внешняя печать числа (DECODER) |
| `DATAPR` | `DATAPR*` | резидентная печать даты (MONSYS) |
| `LOADAN` | LOADANGO | загрузчик оверлеев |
| `NOLISF` | NOLISFL* | COMMON: флаг «нет листинга» |
| `FULISF` | FULISFL* | COMMON: флаг «полный листинг» |
| `CHECKF` | CHECKFL* | COMMON: флаг проверки |
| `*DUMON` | `*DUMON*` | COMMON: рабочие ячейки монитора |
| `INITFO` | INITFOR* | ENTRY корня FOREX* |
| `FOREX*` | FOREX*83 | имя модуля FOREX* (версия 4.13) |
| `ENTRY*` | `ENTRY*` | уже 6 символов — без изменений |

Остальные интерфейсные имена (`*A*`, `FLGEX*`, `A/I0`, `TAK/PG`, `GIV/PG`,
`FOREX`, `CONST`, `COMEQ`, `OPRTR`, `ПP`, `LO*SYN`, `LO*GEN`) уже имеют
длину ≤ 6 и в укорочении не нуждаются.
