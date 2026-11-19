# FOREX_RUNTIME — перекрёстные ссылки

Кто вызывает библиотечные/рантайм-подпрограммы компилятора ФОРЭКС и куда
идут символы `FT*` / RUNTIME. Дополняет `FOREX_ROOT.mad`, `LO_*.xref.md`
и `docs/03-symbols.md` (те не переписываются).

## 0. Именование меток (этап «осмысленные имена»)

Все переходы и вызовы ниже используют новые имена. Старые имена сохранены в
`include/FOREX.labels.md` и в trailing-комментариях исходников.

| Старое имя | Новое имя | Старое имя | Новое имя |
|---|---|---|---|
| `INITFOR*` | `INITFO` | `LOREX` | `LODOVL` |
| `RMON` | `PRTIME` | `NPR` | `DPRTN` |
| `PRIN` | `PRTMSG` | `STOP/` | `ERRTRL` |
| `DATAPR` | `DATAPR` | `OCTTDE` | `OCTTDE` |
| `GIV/PG` | `PAGEGV` | `TAK/PG` | `PAGETK` |
| `FORMAT` | `FTDISP` | `FORTLIBR` | `FTLIO` |
| `DATE*` | `DGET` | `PREPDAT` | `DPREPA` |
| `DARET` | `DPARSE` | `BEGIN` | `OCTBGN` |

---

## 1. Обозначения источников

| Ид. | Источник | Роль |
|---|---|---|
| S1 | `libra211.l21:15529-15712` | FTDISP, FTLIO (исходник Дубны 4.13) |
| S2 | `monsys.9`, слова `0o510413-0o510522`, `0o512500-0o512537` | скомпилированный корень, таблица входов, каталог |
| S3 | `expect_library21.txt:196-218,1055-1088,1181-1184,1200,1313` | LIBREFER: экспорт/импорт библиотеки 21 |
| S4 | `expect_forex.txt:44,49` | карта адресов сборки 4.13 |
| S5 | `besmmons/system1.txt:7645-7733` | DATAPR (резидент MONSYS) |
| S6 | `besmmons/system2.txt:5042-5084` | OCTTDE (реализация DECODER) |
| S7 | `besmtask/exfor.vv:427-459` | OCTTDE (вариант EXFOR) |

## 2. Сводная таблица подпрограмм

| Символ | Модуль-владелец | Точки входа | Экспорт по S3 | Прямые вызывающие |
|---|---|---|---|---|
| `DATAPR` | MONSYS, `system1.txt:7645` | `DATAPR`, `DGET`, `DPREPA` | `ALGOL//`, `ALPHA*`, `FOREX*`, `LINK/IPM`, `OCATALOG`, `PASCAL*`, `SERWISM`, `TCATALOG`, `DOS/IAE` (S3:1055-1068) | `INITFO` (S1:15479), оверлеи (через 0o77xxx) |
| `DGET` | DATAPR | ENTRY (S5:7654) | — | `DPREPA` (S5:7700) |
| `DPREPA` | DATAPR | ENTRY (S5:7698) | `CHEKJOB*`, `COLLECT`, `PRINTFIL`, `SYSLDL` (S3:1203-1207) | внешние модули MONSYS |
| `OCTTDE` | DECODER (S3:1181), тела S6/S7 | `OCTBGN` (S6:5044) | DECODER | `FOREX*`/`PRTIME` (S1:15498), `TCATALOG`, `OVERLOAD`, `SUMOVER` (S3:1182-1184) |
| `FTDISP` | библиотека 21, `libra211.l21:15529` | dispatching table | `FT*002/003/521/531/541/561/611/621/641/721` (S3:206-216) | Fortran-рантайм (`FTNPRT`, `INTPRT*`) |
| `PRINT8` | FTLIO, `libra211.l21:15593` | `PRINT8` | `*DISPAR1` (S3:1200), `FTLIO` (S3:217), `FTNPRT`, `FT*REGIM`, др. (S3:221-223) | `FTLIO/PRINT8`, широкий круг модулей MONSYS |
| `WRTLBR` | FTLIO, `libra211.l21:15592` | `WRTLBR` | `FTLIO` (S3:1313, 218) | `FTLIO/PRINT8` (S1:15603) |
| `PAGEGV`, `PAGETK` | `libra211.l21:16780-16836` | `PAGEGV`, `PAGETK` | LIBREFER | `INITFO` (S1:15484), `ERRTRL` (S1:15510) — **уже описаны в `include/FOREX_ROOT.mad:198-254`, здесь не дублируются** |

## 3. Карта вызовов по вызывающему

### 3.1 Корень `FOREX*` (S1:15448-15528; образ S2:0o510300-0o510347)

| Вызывающий | Команда (S1) | Цель | Подтверждение на ленте |
|---|---|---|---|
| `INITFO` | `,CALL,DATAPR` 15479 | DATAPR | S2:0o510306 `vjm 74010(15)` |
| `INITFO` | `,CALL,PAGEGV.` 15484 | PAGEGV | S2:0o510310, см. FOREX_ROOT.mad |
| `LODOVL` | `,CALL,LOADAN.` 15487/15489 | LOADAN | S2:0o510315/0o510316 |
| `PRTIME` | `,CALL,OCTTDE` 15498 | OCTTDE (DECODER) | S2:0o510322 |
| `ERRTRL` | `,UJ,PAGETK.` 15510 | PAGETK | S2:0o510331, см. FOREX_ROOT.mad |

`PRTIME` готовит аргумент: `NTR 18`, `A-X TIME`, `A*X =R100.0`, `NTR 3`,
`A+X A/I0`, `AEX A/I0`, затем `CALL OCTTDE` → 6 ISO-цифр → `APX/AUX/AOX`
разделители → `ATX TIME` (S1:15491-15502). Это «BPEMЯ: 04.12» в S4:28.

### 3.2 Оверлеи `LO*SYN` / `LO*GEN`

Оба оверлея объявляют одни и те же внешние имена:

| Имя | LO*SYN | LO*GEN |
|---|---|---|
| `DATAPR` (`DATAPR`) | `src/LO_SYN.mad:25` `DATAPR:,SUBP,` | `src/LO_GEN.mad:29` `X_DATAPRS,SUBP,.` |
| `OCTTDE` (`OCTTDE`) | `src/LO_SYN.mad:28` `OCTTDE:,SUBP,` | `src/LO_GEN.mad:32` `X_OCTTDEC,SUBP,.` |
| `PAGEGV`, `PAGETK`, `FOREX`, `CONST`, `COMEQ`, `OPRTR`, `ПP`, `LOADAN` | `include/LO_SYN.xref.md:180-190` | `include/LO_GEN.xref.md:779-788` |

Переходы идут на абсолютные адреса резидентной памяти `0o77xxx`
(`include/LO_GEN.xref.md` §3.2, `include/LO_SYN.xref.md` §2). Окончательное
сопоставление `0o77xxx → DATAPR/OCTTDE` требует карты загрузки MONSYS
и в этом документе не утверждается.

### 3.3 Другие модули библиотеки 21 (LIBREFER)

* `DATAPR` — один из самых востребованных рантайм-выходов: его используют
  `ALGOL//`, `ALPHA*`, `BEMTOMON`, `DOS/IAE`, `FOREX*`, `ITM/ASS`,
  `LINK/IPM`, `LISP`, `OCATALOG`, `PASCAL*`, `SERWISM`, `TCATALOG` (S3:1055-1068).
* `OCTTDE` — `FOREX*`, `TCATALOG`, `OVERLOAD`, `SUMOVER` (S3:1181-1184);
  `CLRTRC` (S3:104).
* `PRINT8` — вызывается более чем 40 модулями (`*DISPAR1`, `BIGTITLE`,
  `FTNPRT`, `FT*REGIM`, `IPCREJ`, `MONITOR*`, `PUNM20`, … — S3:1200-1239).
* `WRTLBR` — экспортируется FTLIO (S3:1313). Одноимённая процедура
  в `libra212.l21:3208+` вызывает `PT6/G`, `STATSUM`, `SAVELIST` — это
  **отдельная улика**, не отождествлять с FTLIO без сверки адресов.

## 4. Таблица передач FTDISP (11 пар `UJ / ATX`)

Источник S1:15565-15586; скомпилированный вид на ленте S2:0o510457-0o510471
(пары) и S2:0o510510-0o510522 (константы `77xxxB`).

| # | S1 строка | Подпрограмма | Ячейка передачи |Пара на ленте | Константа на ленте |
|---|---|---|---|---|---|
| 1 | 15565 | `FT*571` | `77207B` | 0o510457 `uj 74001,atx 4015` | 0o510510 `amx 7207` |
| 2 | 15567 | `FT*541` | `77237B` | 0o510460 `uj 74002,atx 4016` | 0o510511 `amx 7237` |
| 3 | 15569 | `FT*611` | `77167B` | 0o510461 `uj 74003,atx 4017` | 0o510512 `amx 7167` |
| 4 | 15571 | `FT*531` | `77247B` | 0o510462 `uj 74004,atx 4020` | 0o510513 `amx 7247` |
| 5 | 15573 | `FT*561` | `77217B` | 0o510463 `uj 74005,atx 4021` | 0o510514 `amx 7217` |
| 6 | 15575 | `FT*621` | `77157B` | 0o510464 `uj 74006,atx 4022` | 0o510515 `amx 7157` |
| 7 | 15577 | `FT*521` | `77257B` | 0o510465 `uj 74007,atx 4023` | 0o510516 `amx 7257` |
| 8 | 15579 | `FT*721` | `77057B` | 0o510466 `uj 74010,atx 4024` | 0o510517 `amx 7057` |
| 9 | 15581 | `FT*641` | `77137B` | 0o510467 `uj 74011,atx 4025` | 0o510520 `amx 7137` |
| 10 | 15583 | `FT*002` | `77776B` | 0o510470 `uj 74012,atx 4026` | 0o510521 `amx 7776` |
| 11 | 15585 | `FT*003` | `77775B` | 0o510471 `uj 74013,atx 4027` | 0o510522 `amx 7775` |

**Важно:** `FT*571` объявлена в FTDISP как `SUBP` (S1:15530), но по LIBREFER
её экспортирует **ANL** (S3:1075); FTDISP лишь импортирует её. Остальные
десять `FT*` экспортирует FTDISP (S3:206-216).

Соответствие `FT*` → Fortran-подпрограммам (S3:206-216):

| FT* | Экспортируется | Соответствие в LIBREFER |
|---|---|---|
| `FT*002/003` | FTDISP | `INTPRT`, `INTPRT2*` |
| `FT*521` | FTDISP | `INTPRT*` |
| `FT*531` | FTDISP | `INTPRT3*` (INTPRT2*) |
| `FT*541` | FTDISP | `INTPRT5*` (INTPRT2*) |
| `FT*561` | FTDISP | `INTPRTC*` (FTNPRT*) |
| `FT*571` | **ANL** | `INTPRTF*` (FTNPRT*) |
| `FT*611` | FTDISP | `INTPRTV*` (FTNPRT*) |
| `FT*621` | FTDISP | `IPCINI` |
| `FT*641` | FTDISP | `IPCKIL` (IPCINI) |
| `FT*721` | FTDISP | `IPCRCV` (IPCSND) |

## 5. Свидетельства на ленте monsys.9

| Слово | Что найдено | Декод |
|---|---|---|
| 0o510413-0o510420 | таблица входов корня | `ENTRY* FLGEX* NOLISF FULISF CHECKF *DUMON` (*DUMON*) |
| **0o510421** | `DATAPR ` | 6-бит TEXT, `4441644160621200` |
| 0o510422 | `PAGETK  ` | `6441531760470000` |
| 0o510423 | `PAGEGV  ` | `4751661760470000` |
| **0o510424** | `OCTTDE ` | `5743646444454300` |
| 0o510425-0o510431 | `FOREX CONST COMEQ OPRTR LOADAN` | остальные внешние имена корня |
| 0o510443-0o510522 | скомпилированный диспетчер FTDISP | см. §4 |
| **0o512527** | `DATAPR ` | каталог резидентных модулей MONSYS |
| 0o512511 | `ITM/ASS ` | соседняя каталожная запись |

Декодирование через `tools/extract_words.py` (`t6`: 8 шестибитных символов
на слово, код = ASCII − 0x20). Команды — `python3 besm6tape.py dis ... --start 0o...`.

## 6. Адреса сборки 4.13 (S4)

| Символ | Адрес | Строка S4 |
|---|---|---|
| `FT*571` | 01665 E | 48 |
| `FT*621` | 01016 E | 45 |
| `FT*611` | 01022 E | 47 |
| `FT*561` | 01027 E | 48 |
| `PRINT8` | 03324 | 49 |
| `OCTTDE` | 04773 | 44 |
| `STOP*` | 02661 | 44 |

## 7. Неясности

1. Нет карты загрузки MONSYS, поэтому переходам оверлеев на `0o77xxx`
   нельзя однозначно приписать `DATAPR`/`OCTTDE`.
2. Два тела `OCTTDE` (S6 — DECODER/MONSYS, S7 — EXFOR); какая из них
   используется в сборке 4.13, требует сверки с адресом 04773.
3. `WRTLBR` из FTLIO и одноимённая процедура из `libra212.l21` —
   разные ли это модули, не проверено.
4. Точная семантика relocate-полей `atx 4015..4027` в диспетчере FTDISP
   требует дескриптора модуля; текущая трактовка — таблица передач.
## 8. Адреса внешних вызовов с пометкой

| Вызывающий (новое имя) | Вызываемый (новое имя) | Адрес/команда | Пометка |
|---|---|---|---|
| `INITFO` (`INITFOR*`) | `DATAPR` (`DATAPR`) | `VJM 0o74010(15)`, S1:15479 / S2:0o510306 | резидент MONSYS; таблица входов `0o510421` |
| `INITFO` | `PAGEGV` (`GIV/PG`) | `VJM 0o74012(15)`, S1:15484 | текст в `include/FOREX_ROOT.mad` |
| `LODOVL` (`LOREX`) | `LOADAN` | `VJM 0o74022(15)`, S1:15487/15489 | загружает `LO*SYN`/`LO*GEN` по `0o22654` |
| `PRTIME` (`RMON`) | `OCTTDE` (`OCTTDE`) | `VJM 0o74013(15)`, S1:15498 / S2:0o510322 |реализует DECODER; адрес сборки 04773 (S4:44) |
| `ERRTRL` (`STOP/`) | `PAGETK` (`TAK/PG`) | `UJ 0o74011`, S1:15510 | передача управления, возврата нет |
| `FTDISP` (`FORMAT`) | `FT*571 … FT*003` | `UJ` ×11, S1:15565-15586 | адреса ячеек передач `77xxxB` см. §4 |
| `FTLIO/PRINT8` | `WRTLBR+1`, `PRINT8` | `VJM`, S1:15603/15615 | внутренние вызовы в модуле |
| `DPREPA` → `DGET` → `DATAPR` | — | S5:7700/7711 | `FUN 67B` — системная дата |

Оговорка: `0o74010/0o74011/0o74012/0o74013/0o74022` — адреса таблицы входов
резидентной памяти, а **не** физические адреса тел подпрограмм; соответствие
`адрес ↔ имя` дано LIBREFER и таблицей символов корня `0o510413..0o510431`.

## 9. Кто вызывает LO*SYN/LO*GEN и кто вызывается из них

| Связь | Механизм | Где зафиксировано |
|---|---|---|
| `LODOVL` (`LOREX` в `FOREX_ROOT.mad`) → `LO*SYN` | `XTS 0o4031` (TEXT `0o510345`) + `CALL LOADAN` | `FOREX_CORE.xref.md` §8/§9; `FOREX_ROOT.mad` |
| `LODOVL` → `LO*GEN` | `XTS 0o4032` (TEXT `0o510346`) + `CALL LOADAN` | там же |
| `LOADAN` → память | загрузка обоих оверлеев по `0o22654` | `include/catalog.md`, `docs/03-symbols.md` |
| `LO*SYN`, `LO*GEN` → `DATAPR`, `OCTTDE`, `PAGEGV`, `PAGETK` | абсолютные цели `0o77xxx` резидентной памяти | `LO_*.xref.md` §2/§3.2 |
| `LO*SYN`, `LO*GEN` → `FOREX`, `CONST`, `COMEQ`, `OPRTR`, `ПP` | абсолютные VJM по тем же `0o77xxx`; тела не найдены | `FOREX_CORE.xref.md` §3 |
| `LO*SYN`, `LO*GEN` → `LOADAN` | косвенно: инициатор загрузки — `LODOVL` | `FOREX_ROOT.mad` |

Обратных переходов из оверлеев в `FOREX_ROOT.mad` по символическим именам нет:
оверлеи оперируют абсолютными адресами, поэтому направление «кто вызывает»
устанавливается только по корню (`LODOVL`), а «кто вызывается» — по
таблицам внешних ссылок оверлеев.

## 10. FORTLIBR: авто-метки → осмысленные имена

Авто-метки `L00023`…`L00053` в `src/FOREX_RUNTIME.mad` переименованы в
6-символьные имена (первые 6 уникальны). Полное имя вынесено в
`POLN:`-комментарий строки; историческое имя сохранено в `include/FOREX.labels.md` §1/§4.

| Было | Стало | POLN (полное имя) | Источник |
|---|---|---|---|
| `L00023` / `L*00023` | `FLSIGC` | `FL_SIGN_CHECK_62` | S1:15631 |
| `L00027` / `L*00027` | `FLXORL` | `FL_XOR_LOOP_63` | S1:15639 |
| `L00042` / `L*00042` | `FLSHIN` | `FL_SHIFT_IN_71` | S1:15661 |
| `L00045` / `L*00045` | `FLCMPR` | `FL_COMPARE_72` | S1:15667 |
| `L00050` / `L*00050` | `FLMASK` | `FL_MASK_ALL_72` | S1:15673 |
| `L00053` / `L*00053` | `FLASMB` | `FL_ASSEMBLE_65` | S1:15679 |

Все эти точки — внутренние ветви `WRTLBR`/`PRINT8`; ссылок по имени в операндах
(кроме самих определений) в реконструкции нет: переходы идут по абсолютным
адресам `*000NN`, поэтому переименование не изменило ни одного машинного слова.


## Текстовые константы

Проверено 25 констант модуля `src/FOREX_RUNTIME.mad`. Методика: `t6()` из `tools/extract_words.py` (6 бит/символ, 8 символов/слово), GOST-10859 (`gost10859.h`), ISO/ASCII (6 байт/слово). Для ASCII-Hollerith-литералов первичен TEXT-decode; для кириллических GOST-литералов — GOST-decode. Полная таблица с вердиктами — `logs/text_constants_audit.txt`.

| Константа | Декодирование (GOST / TEXT / ISO) | Источник | Вердикт |
|-----------|----------------------------------|----------|---------|
| `''000000''` | GOST `ееееее00` / TEXT `000000  ` / ISO `A··A··` | `src/FOREX_RUNTIME.mad:83` | ДОБАВЛЕНО повторным аудитом (2026-11-19, compiler2): было без DEKOD; то же слово 0o2020202020200000, что у `6H000000`; dtran -D text подтверждает `000000  ` |
| `6H` | GOST `` / TEXT `` / ISO `` | `src/FOREX_RUNTIME.mad:60` | добавлено |
| `1H'055'` | GOST `7е==7000` / TEXT `'055'   ` / ISO `··U···` | `src/FOREX_RUNTIME.mad:84` | добавлено |
| `2H '200'` | GOST `7(ее7000` / TEXT `'200'   ` / ISO `·$····` | `src/FOREX_RUNTIME.mad:85` | добавлено |
| `3H00` | GOST `ее000000` / TEXT `00      ` / ISO `A·····` | `src/FOREX_RUNTIME.mad:86` | добавлено |
| `=6H00` | GOST `ее000000` / TEXT `00      ` / ISO `A·····` | `src/FOREX_RUNTIME.mad:87` | добавлено |
| `6H0000` | GOST `ееее0000` / TEXT `0000    ` / ISO `A·····` | `src/FOREX_RUNTIME.mad:88` | добавлено |
| `6H000000` | GOST `ееееее00` / TEXT `000000  ` / ISO `A··A··` | `src/FOREX_RUNTIME.mad:89` | добавлено |
| `6H000 00` | GOST `еее0ее00` / TEXT `000 00  ` / ISO `A··A··` | `src/FOREX_RUNTIME.mad:90` | добавлено |
| `=6H00/00/` | GOST `ее ее 00` / TEXT `00/00/  ` / ISO `A··@··` | `src/FOREX_RUNTIME.mad:91` | добавлено |
| `6H03 0` | GOST `е)0е0000` / TEXT `03 0    ` / ISO `A0····` | `src/FOREX_RUNTIME.mad:92` | добавлено |
| `6HABГCEH` | GOST `АВГСЕН  ` / TEXT `@BCQEM//` / ISO `·(····` | `src/FOREX_RUNTIME.mad:93` | добавлено |
| `6HARRAY` | GOST `БТТБЩ000` / TEXT `ARRAY   ` / ISO `·,····` | `src/FOREX_RUNTIME.mad:94` | добавлено |
| `6HAПPMAЯ` | GOST `АПРМАЯ  ` / TEXT `@OPL@_//` / ISO `··,···` | `src/FOREX_RUNTIME.mad:95` | добавлено |
| `6HERROR` | GOST `ЕТТПТ000` / TEXT `ERROR   ` / ISO `·,····` | `src/FOREX_RUNTIME.mad:96` | добавлено |
| `6HIN STA` | GOST `ЙО0УФБ00` / TEXT `IN STA  ` / ISO `··3···` | `src/FOREX_RUNTIME.mad:97` | добавлено |
| `6HNDART` | GOST `ОДБТФ000` / TEXT `NDART   ` / ISO `·Hr···` | `src/FOREX_RUNTIME.mad:98` | добавлено |
| `6HOKTHOЯ` | GOST `ОКТНОЯ  ` / TEXT `NJRMN_//` / ISO `······` | `src/FOREX_RUNTIME.mad:99` | добавлено |
| `6H 00.00` | GOST `ее.ее000` / TEXT `00.00   ` / ISO `A··@··` | `src/FOREX_RUNTIME.mad:100` | добавлено |
| `=6H'17''17'''''''''` | GOST `7@[77@[7` / TEXT `'17''17'` / ISO `······` | `src/FOREX_RUNTIME.mad:101` | добавлено |
| `6H'201'  '200'7` | GOST `7(е@7007` / TEXT `'201'  '` / ISO `·$····` | `src/FOREX_RUNTIME.mad:102` | добавлено |
| `6H'231'  ЯHB` | GOST `'231'  Я` / TEXT `;"#!;//_` / ISO `l ·l··` | `src/FOREX_RUNTIME.mad:103` | добавлено |
| `=6H'3''17''''17''17'''` | GOST `7)77@[77` / TEXT `'3''17''` / ISO `·1·Eq·` | `src/FOREX_RUNTIME.mad:104` | добавлено |
| `6HФEBMAP` | GOST `ФЕВМАР  ` / TEXT `TEBL@P//` / ISO `·X····` | `src/FOREX_RUNTIME.mad:105` | добавлено |
| `6HДEK` | GOST `ДЕК     ` / TEXT `DEJ/////` / ISO `·Z·<··` | `src/FOREX_RUNTIME.mad:106` | добавлено |
| `6HИЮHИЮЛ` | GOST `ИЮНИЮЛ  ` / TEXT `H^MH^K//` / ISO `··h···` | `src/FOREX_RUNTIME.mad:107` | добавлено |

