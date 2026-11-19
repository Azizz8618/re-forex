# FOREX_RUNTIME — перекрёстные ссылки

Кто вызывает библиотечные/рантайм-подпрограммы компилятора ФОРЭКС и куда
идут символы `FT*` / RUNTIME. Дополняет `FOREX_ROOT.mad`, `LO_*.xref.md`
и `docs/03-symbols.md` (те не переписываются).

## 1. Обозначения источников

| Ид. | Источник | Роль |
|---|---|---|
| S1 | `libra211.l21:15529-15712` | FORMAT, FORTLIBR (исходник Дубны 4.13) |
| S2 | `monsys.9`, слова `0o510413-0o510522`, `0o512500-0o512537` | скомпилированный корень, таблица входов, каталог |
| S3 | `expect_library21.txt:196-218,1055-1088,1181-1184,1200,1313` | LIBREFER: экспорт/импорт библиотеки 21 |
| S4 | `expect_forex.txt:44,49` | карта адресов сборки 4.13 |
| S5 | `besmmons/system1.txt:7645-7733` | DATAPR* (резидент MONSYS) |
| S6 | `besmmons/system2.txt:5042-5084` | OCTTDEC (реализация DECODER) |
| S7 | `besmtask/exfor.vv:427-459` | OCTTDEC (вариант EXFOR) |

## 2. Сводная таблица подпрограмм

| Символ | Модуль-владелец | Точки входа | Экспорт по S3 | Прямые вызывающие |
|---|---|---|---|---|
| `DATAPR*` | MONSYS, `system1.txt:7645` | `DATAPR*`, `DATE*`, `PREPDAT` | `ALGOL//`, `ALPHA*`, `FOREX*`, `LINK/IPM`, `OCATALOG`, `PASCAL*`, `SERWISM`, `TCATALOG`, `DOS/IAE` (S3:1055-1068) | `INITFOR*` (S1:15479), оверлеи (через 0o77xxx) |
| `DATE*` | DATAPR* | ENTRY (S5:7654) | — | `PREPDAT` (S5:7700) |
| `PREPDAT` | DATAPR* | ENTRY (S5:7698) | `CHEKJOB*`, `COLLECT`, `PRINTFIL`, `SYSLDL` (S3:1203-1207) | внешние модули MONSYS |
| `OCTTDEC` | DECODER (S3:1181), тела S6/S7 | `BEGIN` (S6:5044) | DECODER | `FOREX*`/`RMON` (S1:15498), `TCATALOG`, `OVERLOAD`, `SUMOVER` (S3:1182-1184) |
| `FORMAT` | библиотека 21, `libra211.l21:15529` | dispatching table | `FT*002/003/521/531/541/561/611/621/641/721` (S3:206-216) | Fortran-рантайм (`FTNPRT`, `INTPRT*`) |
| `PRINT8` | FORTLIBR, `libra211.l21:15593` | `PRINT8` | `*DISPAR1` (S3:1200), `FORTLIBR` (S3:217), `FTNPRT`, `FT*REGIM`, др. (S3:221-223) | `FORTLIBR/PRINT8`, широкий круг модулей MONSYS |
| `WRITLIBR` | FORTLIBR, `libra211.l21:15592` | `WRITLIBR` | `FORTLIBR` (S3:1313, 218) | `FORTLIBR/PRINT8` (S1:15603) |
| `GIV/PG`, `TAK/PG` | `libra211.l21:16780-16836` | `GIV/PG`, `TAK/PG` | LIBREFER | `INITFOR*` (S1:15484), `STOP/` (S1:15510) — **уже описаны в `include/FOREX_ROOT.mad:198-254`, здесь не дублируются** |

## 3. Карта вызовов по вызывающему

### 3.1 Корень `FOREX*` (S1:15448-15528; образ S2:0o510300-0o510347)

| Вызывающий | Команда (S1) | Цель | Подтверждение на ленте |
|---|---|---|---|
| `INITFOR*` | `,CALL,DATAPR*` 15479 | DATAPR* | S2:0o510306 `vjm 74010(15)` |
| `INITFOR*` | `,CALL,GIV/PG.` 15484 | GIV/PG | S2:0o510310, см. FOREX_ROOT.mad |
| `LOREX` | `,CALL,LOADANGO.` 15487/15489 | LOADANGO | S2:0o510315/0o510316 |
| `RMON` | `,CALL,OCTTDEC` 15498 | OCTTDEC (DECODER) | S2:0o510322 |
| `STOP/` | `,UJ,TAK/PG.` 15510 | TAK/PG | S2:0o510331, см. FOREX_ROOT.mad |

`RMON` готовит аргумент: `NTR 18`, `A-X TIME`, `A*X =R100.0`, `NTR 3`,
`A+X A/I0`, `AEX A/I0`, затем `CALL OCTTDEC` → 6 ISO-цифр → `APX/AUX/AOX`
разделители → `ATX TIME` (S1:15491-15502). Это «BPEMЯ: 04.12» в S4:28.

### 3.2 Оверлеи `LO*SYN` / `LO*GEN`

Оба оверлея объявляют одни и те же внешние имена:

| Имя | LO*SYN | LO*GEN |
|---|---|---|
| `DATAPR*` | `src/LO_SYN.mad:25` `DATAPR*:,SUBP,` | `src/LO_GEN.mad:29` `X_DATAPRS,SUBP,.` |
| `OCTTDEC` | `src/LO_SYN.mad:28` `OCTTDEC:,SUBP,` | `src/LO_GEN.mad:32` `X_OCTTDEC,SUBP,.` |
| `GIV/PG`, `TAK/PG`, `FOREX`, `CONST`, `COMEQ`, `OPRTR`, `ПP`, `LOADANGO` | `include/LO_SYN.xref.md:180-190` | `include/LO_GEN.xref.md:779-788` |

Переходы идут на абсолютные адреса резидентной памяти `0o77xxx`
(`include/LO_GEN.xref.md` §3.2, `include/LO_SYN.xref.md` §2). Окончательное
сопоставление `0o77xxx → DATAPR*/OCTTDEC` требует карты загрузки MONSYS
и в этом документе не утверждается.

### 3.3 Другие модули библиотеки 21 (LIBREFER)

* `DATAPR*` — один из самых востребованных рантайм-выходов: его используют
  `ALGOL//`, `ALPHA*`, `BEMTOMON`, `DOS/IAE`, `FOREX*`, `ITM/ASS`,
  `LINK/IPM`, `LISP`, `OCATALOG`, `PASCAL*`, `SERWISM`, `TCATALOG` (S3:1055-1068).
* `OCTTDEC` — `FOREX*`, `TCATALOG`, `OVERLOAD`, `SUMOVER` (S3:1181-1184);
  `CLRTRC` (S3:104).
* `PRINT8` — вызывается более чем 40 модулями (`*DISPAR1`, `BIGTITLE`,
  `FTNPRT`, `FT*REGIM`, `IPCREJ`, `MONITOR*`, `PUNM20`, … — S3:1200-1239).
* `WRITLIBR` — экспортируется FORTLIBR (S3:1313). Одноимённая процедура
  в `libra212.l21:3208+` вызывает `PT6/G`, `STATSUM`, `SAVELIST` — это
  **отдельная улика**, не отождествлять с FORTLIBR без сверки адресов.

## 4. Таблица передач FORMAT (11 пар `UJ / ATX`)

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

**Важно:** `FT*571` объявлена в FORMAT как `SUBP` (S1:15530), но по LIBREFER
её экспортирует **ANL** (S3:1075); FORMAT лишь импортирует её. Остальные
десять `FT*` экспортирует FORMAT (S3:206-216).

Соответствие `FT*` → Fortran-подпрограммам (S3:206-216):

| FT* | Экспортируется | Соответствие в LIBREFER |
|---|---|---|
| `FT*002/003` | FORMAT | `INTPRT`, `INTPRT2*` |
| `FT*521` | FORMAT | `INTPRT*` |
| `FT*531` | FORMAT | `INTPRT3*` (INTPRT2*) |
| `FT*541` | FORMAT | `INTPRT5*` (INTPRT2*) |
| `FT*561` | FORMAT | `INTPRTC*` (FTNPRT*) |
| `FT*571` | **ANL** | `INTPRTF*` (FTNPRT*) |
| `FT*611` | FORMAT | `INTPRTV*` (FTNPRT*) |
| `FT*621` | FORMAT | `IPCINI` |
| `FT*641` | FORMAT | `IPCKIL` (IPCINI) |
| `FT*721` | FORMAT | `IPCRCV` (IPCSND) |

## 5. Свидетельства на ленте monsys.9

| Слово | Что найдено | Декод |
|---|---|---|
| 0o510413-0o510420 | таблица входов корня | `ENTRY* FLGEX* NOLISFL* FULISFL* CHECKFL* *DUMON*` |
| **0o510421** | `DATAPR* ` | 6-бит TEXT, `4441644160621200` |
| 0o510422 | `TAK/PG  ` | `6441531760470000` |
| 0o510423 | `GIV/PG  ` | `4751661760470000` |
| **0o510424** | `OCTTDEC ` | `5743646444454300` |
| 0o510425-0o510431 | `FOREX CONST COMEQ OPRTR LOADANGO` | остальные внешние имена корня |
| 0o510443-0o510522 | скомпилированный диспетчер FORMAT | см. §4 |
| **0o512527** | `DATAPR* ` | каталог резидентных модулей MONSYS |
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
| `OCTTDEC` | 04773 | 44 |
| `STOP*` | 02661 | 44 |

## 7. Неясности

1. Нет карты загрузки MONSYS, поэтому переходам оверлеев на `0o77xxx`
   нельзя однозначно приписать `DATAPR*`/`OCTTDEC`.
2. Два тела `OCTTDEC` (S6 — DECODER/MONSYS, S7 — EXFOR); какая из них
   используется в сборке 4.13, требует сверки с адресом 04773.
3. `WRITLIBR` из FORTLIBR и одноимённая процедура из `libra212.l21` —
   разные ли это модули, не проверено.
4. Точная семантика relocate-полей `atx 4015..4027` в диспетчере FORMAT
   требует дескриптора модуля; текущая трактовка — таблица передач.
