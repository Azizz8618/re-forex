# 13 — Перекрёстные ссылки дизассемблированного рантайма ФОРЭКС

Сводит **все** перекрёстные ссылки и константы рантайма: скомпилированные тела
`FORMAT`/`FORTLIBR`, снятые с ленты `monsys.9`, и тела `DATAPR*`/`OCTTDEC`,
полученные компиляцией авторских исходников Дубны через DTRAN с последующей
поразрядной сверкой с листингом дизассемблера. Документ дополняет `docs/09-crossrefs.md`
(глобальный свод) и `include/FOREX_RUNTIME.xref.md` (происхождение S1–S7).

## 0. Источники и соглашение об именах

| Источник | Что даёт |
|---|---|
| `src/FOREX_RUNTIME_DISASM.mad` | машинный код FORMAT/FORTLIBR с ленты, 0o510443-0o510537 и 0o510543-0o510647; 42 `EQU` |
| `src/FOREX_DECODER_DISASM.mad` | DPRNT / OCTDC / OCTEX, скомпилированные из S5/S6/S7; 93 `EQU` |
| `include/RUNTIME_DISASM.xref.md` | LINK-ячейки, ячейки передачи, таблица «короткое имя ↔ полное описание» |
| `include/RUNTIME_DECODER.xref.md` | вызывающие DATAPR*/OCTTDEC, LINK 0o74010/0o74013, потоки данных |
| `src/FOREX_RUNTIME.mad` | дословный листинг S1/S5-S7, 88 `EQU` (эталон смысла) |
| `include/FOREX_ROOT.mad`, `src/FOREX_CORE.mad` | корень: `INITFO`, `PAGEGV`, `PAGETK`, CALL/VJM/UJ |
| `docs/06-address-map.md` §3, §3.1 | подтверждённые LINK-ячейки и 11 адресов `FT*` |

**Правило имён.** МАДЛЕН различает только первые 6 знаков: в таблицах ниже
**основное имя — короткое** (`FMTENT`, `DPRNT`, `X01`, `BW0063`), а полное
смысловое имя и роль вынесены в отдельную колонку или в комментарий.
Источник истины — фактические имена в `src/*.mad`; старые длинные имена
остаются только в `include/*.labels.md` как историческая справка. См.
`docs/10-naming-conventions.md` §6 и `docs/09-crossrefs.md` §7.

## 1. Процедура — entry — вызывающие — вызываемые — внешние адреса — константы

| Процедура (короткое) | Entry | Вызывающие | Вызываемые | Внешние адреса | Константы (`EQU`) | Источник |
|---|---|---|---|---|---|---|
| `FTDISP` / `FMTENT` — FORMAT, диспетчер `FT*` | `FTDISP` (NAME, S1:15529); скомпилированный вход `FMTENT` @0o510443 | Fortran-рантайм `FTNPRT`/`INTPRT*`; каталог LIBREFER `0o502124-0o502127` (S3:206-216) | 11 подпрограмм `FT*571 … FT*003` через LINK `X01..X13`; `FT*571` импортируется из **ANL** (S3:1075) | `X01=0o74001 … X13=0o74013` (LINK, не код); ячейки передачи `D571DS=0o77207 … D003DS=0o77775`; база `FTBTAB=0o77766` | `FTADR 103B`, `FTOFSM 155B`, `FTBTAB 77766B`, `FTLOG 10000000 00000000`, 11×`DnnnDS`, 11×`Xnn` | `src/FOREX_RUNTIME.mad:120`, `src/FOREX_RUNTIME_DISASM.mad:30-74,139` |
| `FTLIO` / `LIBENT` — FORTLIBR, PRINT8/WRITLIBR | `FTLIO` (NAME, S1:15590); `LIBENT` = PRINT8, `LIBA14` = WRITLIBR (*00014) | `PRINT8` — S3:217, сборка 4.13 `03324` (S4:49); `WRITLIBR` — S3:1313 | `WRTLBR+1` (подготовка буфера, S1:15603) и `PRINT8` (печать, S1:15615) — оба внутри модуля | `X01=0o74001` как адрес `BUFFER` (S1:15620); LINK слоты не вызываются, адреса 740xx — заглушки | `ZERO ONE TWO TRIO SEVEN`, `M1777 ISOHI MSK73 MSK76 ISOSHF ALL1 LIBBUF`, данные `C062..C101`, `LIBISO` | `src/FOREX_RUNTIME.mad:193-324`, `src/FOREX_RUNTIME_DISASM.mad:62-74,388` |
| `DATAPR` / `DPRNT` — DATE_PRINT, печать даты DD MON YY HH.MM | `DATAPR` (NAME, S5:7645), вход @S2:0o510421; `DPRNT` (NAME) в дизассембле | `INITFO` → `VJM 0o74010(15)` S1:15479 / S2:0o510306; оверлеи; 12+ модулей LIBREFER | `DGET`/`DP001` (FUN 67B), `DPREPA`/`DP026`, `DPP8`=PRINT8 (макрос `,PRINT,`), `PRINT` | `0o74010` LINK; FUN `67B`; `0o512527` каталог MONSYS; `0o74000..74047` — заглушки | `DR13 DR14 DR15`, `D64P16 D64P35 D64M24 D64M14 D64M22`, `DS00..DS24`, `DN01..DN08`, `DV012..DV777`, `DFUN67`, `DW00..DW20` | `src/FOREX_RUNTIME.mad:329-426`, `src/FOREX_DECODER_DISASM.mad:43-101,143` |
| `DGET` / `DP001` — DATE_GET (DATE*) | `DGET`,ENTRY (S5:7654); `DP001`,ENTRY в дизассембле | `DPREPA`/`DP026` → `VJM` S5:7700; `DPRNT` после FUN 67B | `FUN 67B` — системная дата/время; возврат через M13 | `FUN 67B` (экстракод), `0o74010` (непосредственно не вызывается) | `DV067=67B`, `DFUN67=67`, `DR13`, `DR15` | `src/FOREX_RUNTIME.mad:341`, `src/FOREX_DECODER_DISASM.mad:153` |
| `DPREPA` / `DP026` — DATE_PREPARE (PREPDAT) | `DPREPA`,ENTRY (S5:7698); `DP026`,ENTRY | внешние модули MONSYS: `CHEKJOB*`, `COLLECT`, `PRINTFIL`, `SYSLDL` (S3:1203-1207) | `DGET`/`DP001` → `DATAPR`/`DPRNT` (S5:7700, 7711) | `0o74010` (через DATAPR) | `DN01 DN05`, `DV025 DV026`, `DW17 DW20`, `D64P35`, `D64M14` | `src/FOREX_RUNTIME.mad:389`, `src/FOREX_DECODER_DISASM.mad:205` |
| `OCTTDE` / `OCTDC` — OCT_DEC (DECODER), число → 6 ISO-цифр | `OCTTDE` (NAME, S6:5042); `OCTDC` (NAME) в дизассембле; @S2:0o510424 | `PRINT_TIME` → `VJM 0o74013(15)` S1:15498 / S2:0o510322; `TCATALOG`, `OVERLOAD`, `SUMOVER` (S3:1182-1184), `CLRTRC` (S3:104) | только внутренние метки `OS003` (CYCL), `OS6SY` (/6SYMB); возврат через M13 | `0o74013` LINK; адрес сборки 4.13 `04773` (S4:44); пул `0o411311-0o411333` (EXFOR) | `OR12 OR13 OR14 OR15`, `OI64 OI64M8 O64M24 OI10 OI03 OI02 OI01`, `OV015..OV100`, `OMSK15 OINT0 OREAL1 ORL10..ORL1E5 OZEROS OCTSDM` | `src/FOREX_RUNTIME.mad:432-480`, `src/FOREX_DECODER_DISASM.mad:102-137,248` |
| `OCTEXF` / `OCTEX` — OCT_DEC_EXFOR (EXFOR), альтернатива | `OCTEXF` (NAME, S7:427); `OCTEX` (NAME) | тот же интерфейс; какая реализация соответствует `04773` — не установлено | `OX003` (цикл), `OXRET` (возврат); `C10`, `C1/10`, `B40/1` | пул констант EXFOR `0o411311-0o411333`: B40/1 `0o411316`, C10 `0o411327`, C1/10 `0o411332` | `OXB40`, `OXC10`, `OXC1T`, `OXMSK`, `OXZER`, `ON02..ON04` | `src/FOREX_RUNTIME.mad:485`, `src/FOREX_DECODER_DISASM.mad:297` |
| `PAGEGV` — GIV/PG, выдача страницы | `PAGEGV` NAME (S1:16780) | `INITFO` → `VJM 0o74012(15)` S1:15484 | управление страницами памяти; тело в `include/FOREX_ROOT.mad:235-291`, здесь не дублируется | `0o74012` LINK | константы определены в `include/FOREX_ROOT.mad` (не в рантайме) | `include/FOREX_ROOT.mad:71,97,235` |
| `PAGETK` — TAK/PG, взятие страницы | `PAGETK` ENTRY (S1:16821) | `ERR_TRANSLATOR` → `UJ 0o74011` S1:15510 (возврата нет) | то же, что PAGEGV | `0o74011` LINK | то же | `include/FOREX_ROOT.mad:70,131,276` |

> `FT*571` объявлена в FORMAT как `SUBP`, но экспортирует её **ANL** (S3:1075);
> остальные десять `FT*` экспортирует FORMAT (S3:206-216).

## 2. Граф вызовов: FOREX* → DATAPR*/OCTTDEC/GIV/PG/TAK/PG → FT*/IO* → MONSYS

```text
FOREX* / INITFO (корень, 0o510303)
  ├─ VJM 0o74010(15) ──────────────► DATAPR / DPRNT  (резидент MONSYS)
  │                                    ├─ FUN 67B ──► DGET / DP001 (системная дата)
  │                                    ├─ DPREPA / DP026 ─► DGET ──► DATAPR
  │                                    └─ ,PRINT, ────────► DPP8 = PRINT8 (FORTLIBR)
  ├─ VJM 0o74013(15) ──────────────► OCTTDE / OCTDC (DECODER, 04773)
  │                                    └─ OCTEXF / OCTEX — альтернатива (EXFOR)
  ├─ VJM 0o74012(15) ──────────────► PAGEGV  (GIV/PG)
  ├─ UJ  0o74011 ──────────────────► PAGETK  (TAK/PG, без возврата)
  └─ CALL 0o74022 ─────────────────► LOADANGO ──XTS 0o4031/0o4032──► LO*SYN / LO*GEN
                                                                            │
                                                                            └─ abs 0o4xxxx…0o7xxxx ─► MONSYS / library21

FTDISP / FMTENT (FORMAT)
  └─ UJ ×11 через LINK X01=0o74001 … X13=0o74013 ─► FT*571/541/611/531/561/621/
                                                      521/721/641/002/003
                                                      ─► ячейки 0o77xxx ─► MONSYS / library21
FTLIO (FORTLIBR)
  ├─ VJM WRTLBR+1 (LIBA14) ─► подготовка FT_LIB_BUFFER (0o2000 слов)
  └─ VJM PRINT8 (LIBENT) ───► печать; MONSYS, адрес сборки 03324
LO*SYN / LO*GEN
  └─ VJM/UJ/UZA по 0o77xxx ─► DATE_PRINT (0o74010), OCT_DEC (0o74013),
                              FT*nnn (0o77207 … 0o77775), прочие MONSYS
```

| Откуда | Куда | Механизм | Подтверждение |
|---|---|---|---|
| `INITFO` | `DATAPR`/`DPRNT` | `VJM 0o74010(15)`, S1:15479 | S2:0o510306; docs/06 §3 |
| `INITFO` | `PAGEGV` | `VJM 0o74012(15)`, S1:15484 | S2:0o510314; `FOREX_ROOT.mad` |
| `PRINT_TIME` | `OCTTDE`/`OCTDC` | `VJM 0o74013(15)`, S1:15498 | S2:0o510322; docs/06 §3 |
| `ERR_TRANSLATOR` | `PAGETK` | `UJ 0o74011`, S1:15510 | S2:0o510331 |
| `FTDISP`/`FMTENT` | `FT*nnn` ×11 | `UJ`/LINK `X01..X13`, S1:15565-15586 | S2:0o510457-0o510471 |
| `FTLIO` | `WRTLBR`+1, `PRINT8` | `VJM`, S1:15603/15615 | LIBREFER S3:217/1313 |
| `DPRNT` | `DPP8` | макрос `,PRINT,`, S5:7695 | S5:7693 |
| `LO*SYN`/`LO*GEN` | MONSYS / library21 | абсолютные `0o77xxx` | docs/06 §3.1, §7 |

**Оговорка.** LINK-ячейки `0o74010..0o74013` в корне и в таблице FORMAT
имеют одинаковую нумерацию, но относятся к разным символам: в корне
`0o74010=DATAPR*`, `0o74013=OCTTDEC`, в FORMAT `0o74010=FT*721`,
`0o74013=FT*003`. LINK-ячейки выделяются **пер-модульно** (docs/06 §3.1).
Диапазон `0o74000..0o74047` на ленте — 40 идентичных заглушек
`yta,ati 15`, то есть таблица входов, а не тела подпрограмм.

## 3. Ячейки передачи FORMAT: 11 пар LINK → FT* → 0o77xxx

| LINK (короткое) | Адрес LINK | Подпрограмма | Ячейка передачи (короткое) | Адрес ячейки | Источник |
|---|---|---|---|---|---|
| `X01` | 0o74001 | `FT*571` (импорт из ANL) | `D571DS` | 0o77207 | S1:15565-15566 |
| `X02` | 0o74002 | `FT*541` | `D541DS` | 0o77237 | S1:15567-15568 |
| `X03` | 0o74003 | `FT*611` | `D611DS` | 0o77167 | S1:15569-15570 |
| `X04` | 0o74004 | `FT*531` | `D531DS` | 0o77247 | S1:15571-15572 |
| `X05` | 0o74005 | `FT*561` | `D561DS` | 0o77217 | S1:15573-15574 |
| `X06` | 0o74006 | `FT*621` | `D621DS` | 0o77157 | S1:15575-15576 |
| `X07` | 0o74007 | `FT*521` | `D521DS` | 0o77257 | S1:15577-15578 |
| `X10` | 0o74010 | `FT*721` | `D721DS` | 0o77057 | S1:15579-15580 |
| `X11` | 0o74011 | `FT*641` | `D641DS` | 0o77137 | S1:15581-15582 |
| `X12` | 0o74012 | `FT*002` | `D002DS` | 0o77776 | S1:15583-15584 |
| `X13` | 0o74013 | `FT*003` | `D003DS` | 0o77775 | S1:15585-15586 |

Соответствие `FT*` → Fortran-процедурам (LIBREFER S3:206-216):
`FT*002/003` → `INTPRT`, `INTPRT2*`; `FT*521` → `INTPRT*`; `FT*531` →
`INTPRT3*`; `FT*541` → `INTPRT5*`; `FT*561` → `INTPRTC*`; `FT*571` →
`INTPRTF*` (экспорт ANL); `FT*611` → `INTPRTV*`; `FT*621` → `IPCINI`;
`FT*641` → `IPCKIL`; `FT*721` → `IPCRCV`.

## 4. Все `EQU`-константы рантайма

Имена в таблицах — короткие (≤6 знаков); полное имя и роль даны отдельными
колонками. Значения приведены в том виде, в каком записаны в исходнике
(восьмеричные — с суффиксом `B`, вещественные — с точкой).

### 4.1. `src/FOREX_RUNTIME_DISASM.mad` — скомпилированные FORMAT/FORTLIBR

| Короткое имя | Значение | Полное имя | Роль / источник | Где объявлено |
|---|---|---|---|---|
| `BAS14` | `14` | BASE_REG14 | роль: номер индексного регистра базы таблицы передач M14; S1:15541 | `src/FOREX_RUNTIME_DISASM.mad:30` |
| `LNK13` | `13` | RET_LINK_REG | роль: номер регистра связывания M13; S1:15597 | `src/FOREX_RUNTIME_DISASM.mad:31` |
| `WRK07` | `7` | WORK_REG7 | роль: рабочий регистр FORTLIBR M7; S1:15596 | `src/FOREX_RUNTIME_DISASM.mad:32` |
| `FTADR` | `103B` | FT_ADDR_FIELD | роль: маска поля адреса при выборке дескриптора TRANSFER; S1:15543 | `src/FOREX_RUNTIME_DISASM.mad:34` |
| `FTOFSM` | `155B` | FT_OFFSET_MASK | роль: маска смещения в таблице передач; S1:15559 | `src/FOREX_RUNTIME_DISASM.mad:35` |
| `FTBTAB` | `77766B` | FTD_TABLE_BASE_ADDR | роль: база таблицы передач FORMAT; S1:15549 | `src/FOREX_RUNTIME_DISASM.mad:36` |
| `FTLOG` | `10000000 00000000` | FTD_CONST | роль: константа сложения при расчёте смещения; S1:15587 | `src/FOREX_RUNTIME_DISASM.mad:37` |
| `D571DS` | `77207B` | FT571_DISPATCH | роль: ячейка передачи FT*571 (импорт из ANL); S1:15566 / S3:1075 | `src/FOREX_RUNTIME_DISASM.mad:39` |
| `D541DS` | `77237B` | FT541_DISPATCH | роль: ячейка передачи FT*541; S1:15568 | `src/FOREX_RUNTIME_DISASM.mad:40` |
| `D611DS` | `77167B` | FT611_DISPATCH | роль: ячейка передачи FT*611; S1:15570 | `src/FOREX_RUNTIME_DISASM.mad:41` |
| `D531DS` | `77247B` | FT531_DISPATCH | роль: ячейка передачи FT*531; S1:15572 | `src/FOREX_RUNTIME_DISASM.mad:42` |
| `D561DS` | `77217B` | FT561_DISPATCH | роль: ячейка передачи FT*561; S1:15574 | `src/FOREX_RUNTIME_DISASM.mad:43` |
| `D621DS` | `77157B` | FT621_DISPATCH | роль: ячейка передачи FT*621; S1:15576 | `src/FOREX_RUNTIME_DISASM.mad:44` |
| `D521DS` | `77257B` | FT521_DISPATCH | роль: ячейка передачи FT*521; S1:15578 | `src/FOREX_RUNTIME_DISASM.mad:45` |
| `D721DS` | `77057B` | FT721_DISPATCH | роль: ячейка передачи FT*721; S1:15580 | `src/FOREX_RUNTIME_DISASM.mad:46` |
| `D641DS` | `77137B` | FT641_DISPATCH | роль: ячейка передачи FT*641; S1:15582 | `src/FOREX_RUNTIME_DISASM.mad:47` |
| `D002DS` | `77776B` | FT002_DISPATCH | роль: ячейка передачи FT*002; S1:15584 | `src/FOREX_RUNTIME_DISASM.mad:48` |
| `D003DS` | `77775B` | FT003_DISPATCH | роль: ячейка передачи FT*003; S1:15586 | `src/FOREX_RUNTIME_DISASM.mad:49` |
| `X01` | `74001B` | EXT_LINK_FT571 | роль: LINK-адрес FT*571; лента 0o510457 | `src/FOREX_RUNTIME_DISASM.mad:51` |
| `X02` | `74002B` | EXT_LINK_FT541 | роль: LINK-адрес FT*541; лента 0o510460 | `src/FOREX_RUNTIME_DISASM.mad:52` |
| `X03` | `74003B` | EXT_LINK_FT611 | роль: LINK-адрес FT*611; лента 0o510461 | `src/FOREX_RUNTIME_DISASM.mad:53` |
| `X04` | `74004B` | EXT_LINK_FT531 | роль: LINK-адрес FT*531; лента 0o510462 | `src/FOREX_RUNTIME_DISASM.mad:54` |
| `X05` | `74005B` | EXT_LINK_FT561 | роль: LINK-адрес FT*561; лента 0o510463 | `src/FOREX_RUNTIME_DISASM.mad:55` |
| `X06` | `74006B` | EXT_LINK_FT621 | роль: LINK-адрес FT*621; лента 0o510464 | `src/FOREX_RUNTIME_DISASM.mad:56` |
| `X07` | `74007B` | EXT_LINK_FT521 | роль: LINK-адрес FT*521; лента 0o510465 | `src/FOREX_RUNTIME_DISASM.mad:57` |
| `X10` | `74010B` | EXT_LINK_FT721 | роль: LINK-адрес FT*721; лента 0o510466 | `src/FOREX_RUNTIME_DISASM.mad:58` |
| `X11` | `74011B` | EXT_LINK_FT641 | роль: LINK-адрес FT*641; лента 0o510467 | `src/FOREX_RUNTIME_DISASM.mad:59` |
| `X12` | `74012B` | EXT_LINK_FT002 | роль: LINK-адрес FT*002; лента 0o510470 | `src/FOREX_RUNTIME_DISASM.mad:60` |
| `X13` | `74013B` | EXT_LINK_FT003 | роль: LINK-адрес FT*003; лента 0o510471 | `src/FOREX_RUNTIME_DISASM.mad:61` |
| `ZERO` | `0` | ZERO | роль: нулевая константа / признак «нет знака»; S1:15691 | `src/FOREX_RUNTIME_DISASM.mad:63` |
| `ONE` | `1` | ONE_WORD | роль: единица — приращение/счётчик; S1:15646 | `src/FOREX_RUNTIME_DISASM.mad:64` |
| `TWO` | `2` | TWO | роль: двойка — счётчик разрядов; S1:15703 | `src/FOREX_RUNTIME_DISASM.mad:65` |
| `TRIO` | `3` | REAL_MODE_3 | роль: режим NTR 3 / константа 3; S1:15612 | `src/FOREX_RUNTIME_DISASM.mad:66` |
| `SEVEN` | `7` | DEC_7 | роль: счётчик Cycles PRINT8; S1:15596 | `src/FOREX_RUNTIME_DISASM.mad:67` |
| `M1777` | `1777B` | MASK_1777 | роль: маска 1777B в константе *00066; S1:15696 | `src/FOREX_RUNTIME_DISASM.mad:68` |
| `ISOHI` | `10000000 00000000` | HIGH_BIT_ISO | роль: старший бит для сборки ISO-кода цифры; S1:15697 | `src/FOREX_RUNTIME_DISASM.mad:69` |
| `MSK73` | `37777774 77777477` | SIGN_EXP_MASK | роль: маска знака/порядка числа; S1:15701 | `src/FOREX_RUNTIME_DISASM.mad:70` |
| `MSK76` | `77270707 00000000` | EXTRACT_MASK | роль: маска экстракода *70; S1:15704 | `src/FOREX_RUNTIME_DISASM.mad:71` |
| `ISOSHF` | `54B` | ISO_CODE_SHIFT | роль: сдвиг ASN 54B при сборке 8-символьного слова; S1:15685 | `src/FOREX_RUNTIME_DISASM.mad:72` |
| `ALL1` | `77777B` | ALL_ONES_MASK | роль: маска «все единицы» (XTA 77777B); S1:15677 | `src/FOREX_RUNTIME_DISASM.mad:73` |
| `LIBBUF` | `2000B` | LIB_BUFFER_LEN | роль: длина BUFFER — 0o2000 слов; S1:15591 | `src/FOREX_RUNTIME_DISASM.mad:74` |
| `LIBISO` | `C101` | LIB_ERROR_TEXT | роль: начало блока ISO-текстов диагностики; S1:15707 | `src/FOREX_RUNTIME_DISASM.mad:388` |

> Всего **42** `,EQU,`-констант в `src/FOREX_RUNTIME_DISASM.mad`.


### 4.2. `src/FOREX_DECODER_DISASM.mad` — DPRNT / OCTDC / OCTEX

| Короткое имя | Значение | Полное имя | Роль / источник | Где объявлено |
|---|---|---|---|---|
| `DR13` | `13` | — | M13 — базовый регистр DATE_PRINT; S5:7646 | `src/FOREX_DECODER_DISASM.mad:43` |
| `DR14` | `14` | — | M14 — регистр BASE/DARET; S5:7646 | `src/FOREX_DECODER_DISASM.mad:44` |
| `DR15` | `15` | — | M15 — рабочий регистр; S5:7661 | `src/FOREX_DECODER_DISASM.mad:45` |
| `D64P16` | `64+16` | DATE_DAY_SHIFT | сдвиг DD из FUN 67B; S5:7664 | `src/FOREX_DECODER_DISASM.mad:46` |
| `D64P35` | `64+35` | DATE_MONTH_SHIFT | сдвиг MM из FUN 67B; S5:7668 | `src/FOREX_DECODER_DISASM.mad:47` |
| `D64M24` | `64-24` | DATE_MONTH_INDEX_SHIFT | индекс месяца; S5:7677 | `src/FOREX_DECODER_DISASM.mad:48` |
| `D64M14` | `64-14` | DATE_YEAR_SHIFT | сдвиг YY; S5:7679 | `src/FOREX_DECODER_DISASM.mad:49` |
| `D64M22` | `64-22` | DATE_TIME_SHIFT | сдвиг HH.MM; S5:7684 | `src/FOREX_DECODER_DISASM.mad:50` |
| `DS06` | `6` | — | NTR 6 — число полей даты; S5:7658 | `src/FOREX_DECODER_DISASM.mad:51` |
| `DS03` | `3` | — | NTR 3; S5:7665 | `src/FOREX_DECODER_DISASM.mad:52` |
| `DS02` | `2` | — | NTR 2; S5:7674 | `src/FOREX_DECODER_DISASM.mad:53` |
| `DS01` | `1` | — | UTM 1 / MTJ 13; S5:7690 | `src/FOREX_DECODER_DISASM.mad:54` |
| `DS24` | `24` | — | VTM 24; S5:7673 | `src/FOREX_DECODER_DISASM.mad:55` |
| `DS16` | `16` | — | сдвиг 64+16 компонента; S5:7664 | `src/FOREX_DECODER_DISASM.mad:56` |
| `DS00` | `0` | — | нулевой индекс; S5:7645 | `src/FOREX_DECODER_DISASM.mad:57` |
| `DN02` | `-2` | — | XTS -2 (DATE*); S5:7659 | `src/FOREX_DECODER_DISASM.mad:58` |
| `DN03` | `-3` | — | XTS -3 (MONTHFI); S5:7663 | `src/FOREX_DECODER_DISASM.mad:59` |
| `DN04` | `-4` | — | XTS -4; S5:7676 | `src/FOREX_DECODER_DISASM.mad:60` |
| `DN06` | `-6` | — | UTM -6; S5:7694 | `src/FOREX_DECODER_DISASM.mad:61` |
| `DN08` | `-8` | — | XTS -8; S5:7688 | `src/FOREX_DECODER_DISASM.mad:62` |
| `DN01` | `-1` | — | Z00 -1; S5:7704 | `src/FOREX_DECODER_DISASM.mad:63` |
| `DN05` | `-5` | — | Z00 -5; S5:7703 | `src/FOREX_DECODER_DISASM.mad:64` |
| `DV067` | `67B` | — | *50 67B — FUN 67B системная дата; S5:7657 | `src/FOREX_DECODER_DISASM.mad:65` |
| `DV032` | `32B` | — | XS-индекс DATE0; S5:7659  ; (=0o32) | `src/FOREX_DECODER_DISASM.mad:66` |
| `DV043` | `43B` | — | индекс MONTHFI; S5:7663 | `src/FOREX_DECODER_DISASM.mad:67` |
| `DV033` | `33B` | — | индекс DATE1; S5:7664 | `src/FOREX_DECODER_DISASM.mad:68` |
| `DV047` | `47B` | — | индекс MARR; S5:7670 | `src/FOREX_DECODER_DISASM.mad:69` |
| `DV030` | `30B` | — | VTM 30B; S5:7672 | `src/FOREX_DECODER_DISASM.mad:70` |
| `DV035` | `35B` | — | индекс YMASK; S5:7678 | `src/FOREX_DECODER_DISASM.mad:71` |
| `DV044` | `44B` | — | индекс DATE2; S5:7683 | `src/FOREX_DECODER_DISASM.mad:72` |
| `DV034` | `34B` | — | индекс TMASK; S5:7685 | `src/FOREX_DECODER_DISASM.mad:73` |
| `DV024` | `24B` | — | индекс DATE3; S5:7687 | `src/FOREX_DECODER_DISASM.mad:74` |
| `DV027` | `27B` | — | индекс DATE4; S5:7688 | `src/FOREX_DECODER_DISASM.mad:75` |
| `DV025` | `25B` | — | AUX 25B в PREPDAT; S5:7700 | `src/FOREX_DECODER_DISASM.mad:76` |
| `DV026` | `26B` | — | AOX 26B в PREPDAT; S5:7700 | `src/FOREX_DECODER_DISASM.mad:77` |
| `DV012` | `12B` | — | ATX 12B; S5:7699 | `src/FOREX_DECODER_DISASM.mad:78` |
| `DV013` | `13B` | — | ATX 13B; S5:7701 | `src/FOREX_DECODER_DISASM.mad:79` |
| `DV014` | `14B` | — | UTM 14B; S5:7690 | `src/FOREX_DECODER_DISASM.mad:80` |
| `DV773` | `7773B` | — | AMX 7773B; S5:7708  ; (=0o7773) | `src/FOREX_DECODER_DISASM.mad:81` |
| `DV777` | `7777B` | — | AMX 7777B; S5:7709  ; (=0o7777) | `src/FOREX_DECODER_DISASM.mad:82` |
| `DFUN67` | `67` | — | FUN 67B код экстракода даты; S5:7657 | `src/FOREX_DECODER_DISASM.mad:83` |
| `DW00` | `4020741740003417` | — | ISO '201' '200'7; DATE0; S5:7707 | `src/FOREX_DECODER_DISASM.mad:85` |
| `DW01` | `3700055000000017` | — | ISO '055' + DATE1 '200'; S5:7707-7708 | `src/FOREX_DECODER_DISASM.mad:86` |
| `DW02` | `0000000003600000` | — | CONT 1H'055'; S5:7709 | `src/FOREX_DECODER_DISASM.mad:87` |
| `DW03` | `4620741717426442` | — | ISO '231' ЯHB; MARR; S5:7712 | `src/FOREX_DECODER_DISASM.mad:88` |
| `DW04` | `150224421302006` | — | GOST ФEBMAP; MARR+1; S5:7713 | `src/FOREX_DECODER_DISASM.mad:89` |
| `DW05` | `1720000000000000` | — | GOST АПPMAЯ; MARR+2; S5:7714 | `src/FOREX_DECODER_DISASM.mad:90` |
| `DW06` | `0000000000000000` | — | GOST ИЮHИЮЛ; MARR+3; S5:7715 | `src/FOREX_DECODER_DISASM.mad:91` |
| `DW07` | `1002104314222455` | — | GOST ABГCEH; MARR+4; S5:7716 | `src/FOREX_DECODER_DISASM.mad:92` |
| `DW10` | `0000003600000034` | — | GOST ' 00.00'; DATE3; S5:7718 | `src/FOREX_DECODER_DISASM.mad:93` |
| `DW11` | `0000141700007417` | — | TMASK 6H03 0; S5:7720 | `src/FOREX_DECODER_DISASM.mad:94` |
| `DW12` | `0000000000007417` | — | DMASK (BSS .); S5:7719 | `src/FOREX_DECODER_DISASM.mad:95` |
| `DW13` | `1612221516360000` | — | YMASK 6H0000  .; S5:7721 | `src/FOREX_DECODER_DISASM.mad:96` |
| `DW14` | `1102245203607417` | — | GOST OKTHOЯ; S5:7722 | `src/FOREX_DECODER_DISASM.mad:97` |
| `DW15` | `0000000000000776` | — | MONTHFI OCT 00 776; S5:7724 | `src/FOREX_DECODER_DISASM.mad:98` |
| `DW16` | `0000000000036074` | — | константа 0o36074; S5:7723 | `src/FOREX_DECODER_DISASM.mad:99` |
| `DW17` | `0060740003607400` | — | =6H'3''17''17''17' (PREPDAT); S5:7701 | `src/FOREX_DECODER_DISASM.mad:100` |
| `DW20` | `2020172020172020` | — | =6H'17''17'''''''' (PREPDAT); S5:7700 | `src/FOREX_DECODER_DISASM.mad:101` |
| `OR12` | `12` | — | M12 — база DECODER; S6:5044 | `src/FOREX_DECODER_DISASM.mad:103` |
| `OR13` | `13` | — | M13; S6:5055 | `src/FOREX_DECODER_DISASM.mad:104` |
| `OR14` | `14` | — | M14 — UTC/VLM; S6:5046 | `src/FOREX_DECODER_DISASM.mad:105` |
| `OR15` | `15` | — | M15; S6:5056 | `src/FOREX_DECODER_DISASM.mad:106` |
| `ON02` | `-2` | — | UTM -2 в RET; S7:443 | `src/FOREX_DECODER_DISASM.mad:107` |
| `ON03` | `-3` | — | XTS -3; S7:433 | `src/FOREX_DECODER_DISASM.mad:108` |
| `ON04` | `-4` | — | UTM -4; S7:440 | `src/FOREX_DECODER_DISASM.mad:109` |
| `OI64` | `64` | — | ASN 64 / YTA 64; S6:5049, S7:436 | `src/FOREX_DECODER_DISASM.mad:110` |
| `OI64M8` | `64-8` | — | ASN 64-8 в /6SYMB; S6:5079 | `src/FOREX_DECODER_DISASM.mad:111` |
| `O64M24` | `64-24` | — | ASN 64-24; S7:445 | `src/FOREX_DECODER_DISASM.mad:112` |
| `OI10` | `10` | — | NTR 10; S6:5075 | `src/FOREX_DECODER_DISASM.mad:113` |
| `OI03` | `3` | — | NTR 3; S7:431 | `src/FOREX_DECODER_DISASM.mad:114` |
| `OI02` | `2` | — | NTR 2; S7:447 | `src/FOREX_DECODER_DISASM.mad:115` |
| `OI01` | `1` | — | WTC 1; S7:449 | `src/FOREX_DECODER_DISASM.mad:116` |
| `OV015` | `15B` | — | AAX B40/1; S7:429  ; (=0o15) | `src/FOREX_DECODER_DISASM.mad:117` |
| `OV016` | `16B` | — | A*X C10; S7:437    ; (=0o16) | `src/FOREX_DECODER_DISASM.mad:118` |
| `OV017` | `17B` | — | A*X C1/10; S7:434  ; (=0o17) | `src/FOREX_DECODER_DISASM.mad:119` |
| `OV024` | `24B` | — | AUX 24B; S6:5065 | `src/FOREX_DECODER_DISASM.mad:120` |
| `OV100` | `100B` | — | YTA 100B = 64; S7:436 | `src/FOREX_DECODER_DISASM.mad:121` |
| `OV020` | `20B` | — | AUX 20B; S6:5080 | `src/FOREX_DECODER_DISASM.mad:122` |
| `OV021` | `21B` | — | AOX 21B; S6:5076 | `src/FOREX_DECODER_DISASM.mad:123` |
| `OMSK15` | `0000000000077777` | — | MASK15; S6:5074 | `src/FOREX_DECODER_DISASM.mad:124` |
| `OINT0` | `0` | — | INT 0; S6:5075 | `src/FOREX_DECODER_DISASM.mad:125` |
| `OREAL1` | `2030000000000000` | — | C1 REAL 1.0; S6:5082 | `src/FOREX_DECODER_DISASM.mad:126` |
| `ORL10` | `2112000000000000` | — | REAL 10.0; S6:5081 | `src/FOREX_DECODER_DISASM.mad:127` |
| `ORL100` | `2174400000000000` | — | REAL 100.0; S6:5080 | `src/FOREX_DECODER_DISASM.mad:128` |
| `ORL1K` | `2257500000000000` | — | REAL 1000.0; S6:5079 | `src/FOREX_DECODER_DISASM.mad:129` |
| `ORL10K` | `2351610000000000` | — | REAL 10000.0; S6:5078 | `src/FOREX_DECODER_DISASM.mad:130` |
| `ORL1E5` | `2434152000000000` | — | REAL 100000.0; S6:5077 | `src/FOREX_DECODER_DISASM.mad:131` |
| `OZEROS` | `2020202020200000` | — | ZERO ISO '000000'; S6:5083 | `src/FOREX_DECODER_DISASM.mad:132` |
| `OXB40` | `0017777777777777` | — | B40/1 LOG; S7:454 | `src/FOREX_DECODER_DISASM.mad:133` |
| `OXC10` | `4000000000000012` | — | C10 LOG; S7:455 | `src/FOREX_DECODER_DISASM.mad:134` |
| `OXC1T` | `4001463146314632` | — | C1/10 LOG; S7:456 | `src/FOREX_DECODER_DISASM.mad:135` |
| `OXMSK` | `0360741703607417` | — | MSK GOST 6H' '; S7:457 | `src/FOREX_DECODER_DISASM.mad:136` |
| `OXZER` | `2020202020200000` | — | ZERO ISO 6H000000; S7:458 | `src/FOREX_DECODER_DISASM.mad:137` |

> Всего **93** `,EQU,`-констант в `src/FOREX_DECODER_DISASM.mad`.


### 4.3. `src/FOREX_RUNTIME.mad` — дословный листинг S1/S5–S7 (эталон смысла)

| Короткое имя | Значение | Полное имя | Роль / источник | Где объявлено |
|---|---|---|---|---|
| `ALLMS` | `77777B` | ALL_ONES_MASK | роль: маска «все единицы»; источник: S1:15677 | `src/FOREX_RUNTIME.mad:27` |
| `BS14R` | `14` | BASE_REG14 | роль: номер индексного регистра базы M14; источник: S1:15541 | `src/FOREX_RUNTIME.mad:28` |
| `DW0000` | `0000000000077777` | DATA_WORD_0000000000077777 | роль: ; S6:5074 MASK15 = 0000000000077777; источник: S6:5074 | `src/FOREX_RUNTIME.mad:29` |
| `DW0001` | `00000000 00000000` | DATA_WORD_00000000_00000000 | роль: ; S1:15691; источник: S1:15691 | `src/FOREX_RUNTIME.mad:30` |
| `DW0002` | `00000000 00000001` | DATA_WORD_00000000_00000001 | роль: ; S1:15694; источник: S1:15694 | `src/FOREX_RUNTIME.mad:31` |
| `DW0003` | `00000000 00000002` | DATA_WORD_00000000_00000002 | роль: ; S1:15703; источник: S1:15703 | `src/FOREX_RUNTIME.mad:32` |
| `DW0004` | `00000000 00001777` | DATA_WORD_00000000_00001777 | роль: ; S1:15696; источник: S1:15696 | `src/FOREX_RUNTIME.mad:33` |
| `DW0005` | `00100000 00000000` | DATA_WORD_00100000_00000000 | роль: ; S1:15697; источник: S1:15697 | `src/FOREX_RUNTIME.mad:34` |
| `DW0006` | `17 7777 7777 7777` | DATA_WORD_17_7777_7777_7777 | роль: ; S7:454; источник: S7:454 | `src/FOREX_RUNTIME.mad:35` |
| `DW0007` | `37777774 77777477` | DATA_WORD_37777774_77777477 | роль: ; S1:15701; источник: S1:15701 | `src/FOREX_RUNTIME.mad:36` |
| `DW0008` | `77270707 00000000` | DATA_WORD_77270707_00000000 | роль: ; S1:15704; источник: S1:15704 | `src/FOREX_RUNTIME.mad:37` |
| `DTDAYS` | `64+16` | DATE_DAY_SHIFT | роль: выделение DD из FUN 67B; источник: S5:7664 | `src/FOREX_RUNTIME.mad:38` |
| `DTMISH` | `64-24` | DATE_MONTH_INDEX_SHIFT | роль: выделение индекса месяца; источник: S5:7677 | `src/FOREX_RUNTIME.mad:39` |
| `DTMOSH` | `64+35` | DATE_MONTH_SHIFT | роль: выделение MM из FUN 67B; источник: S5:7668 | `src/FOREX_RUNTIME.mad:40` |
| `DTTMSH` | `64-22` | DATE_TIME_SHIFT | роль: выделение HH.MM из FUN 67B; источник: S5:7684 | `src/FOREX_RUNTIME.mad:41` |
| `DTYRSH` | `64-14` | DATE_YEAR_SHIFT | роль: выделение YY из FUN 67B; источник: S5:7679 | `src/FOREX_RUNTIME.mad:42` |
| `DEC_7` | `7` | — | роль: ; S1:15596; источник: S1:15596 | `src/FOREX_RUNTIME.mad:43` |
| `FIXM2` | `2` | FIXED_MODE_2 | роль: режим NTR 2 / шаг 2; источник: S5:7646 | `src/FOREX_RUNTIME.mad:44` |
| `F002DS` | `77776B` | FT002_DISPATCH | роль: ячейка передачи FT*002; источник: S1:15584 | `src/FOREX_RUNTIME.mad:45` |
| `F003DS` | `77775B` | FT003_DISPATCH | роль: ячейка передачи FT*003; источник: S1:15586 | `src/FOREX_RUNTIME.mad:46` |
| `F521DS` | `77257B` | FT521_DISPATCH | роль: ячейка передачи FT*521; источник: S1:15578 | `src/FOREX_RUNTIME.mad:47` |
| `F531DS` | `77247B` | FT531_DISPATCH | роль: ячейка передачи FT*531; источник: S1:15572 | `src/FOREX_RUNTIME.mad:48` |
| `F541DS` | `77237B` | FT541_DISPATCH | роль: ячейка передачи FT*541; источник: S1:15568 | `src/FOREX_RUNTIME.mad:49` |
| `F561DS` | `77217B` | FT561_DISPATCH | роль: ячейка передачи FT*561; источник: S1:15574 | `src/FOREX_RUNTIME.mad:50` |
| `F571DS` | `77207B` | FT571_DISPATCH | роль: ячейка передачи FT*571; источник: S1:15566 | `src/FOREX_RUNTIME.mad:51` |
| `F611DS` | `77167B` | FT611_DISPATCH | роль: ячейка передачи FT*611; источник: S1:15570 | `src/FOREX_RUNTIME.mad:52` |
| `F621DS` | `77157B` | FT621_DISPATCH | роль: ячейка передачи FT*621; источник: S1:15576 | `src/FOREX_RUNTIME.mad:53` |
| `F641DS` | `77137B` | FT641_DISPATCH | роль: ячейка передачи FT*641; источник: S1:15582 | `src/FOREX_RUNTIME.mad:54` |
| `F721DS` | `77057B` | FT721_DISPATCH | роль: ячейка передачи FT*721; источник: S1:15580 | `src/FOREX_RUNTIME.mad:55` |
| `FTDTBA` | `77766B` | FTD_TABLE_BASE_ADDR | роль: база таблицы передач FORMAT; источник: S1:15549 | `src/FOREX_RUNTIME.mad:56` |
| `FTADFL` | `103B` | FT_ADDR_FIELD | роль: маска поля адреса в FORMAT; источник: S1:15543 | `src/FOREX_RUNTIME.mad:57` |
| `FTOFMK` | `155B` | FT_OFFSET_MASK | роль: маска смещения в FORMAT; источник: S1:15559 | `src/FOREX_RUNTIME.mad:58` |
| `GOSTBL` | `6H` | GOST_BLANK | роль: пустой GOST-формат; источник: S7:457 | `src/FOREX_RUNTIME.mad:59` |
| `INTZ` | `0` | INT_ZERO | роль: целое 0; источник: S6:5075 | `src/FOREX_RUNTIME.mad:60` |
| `ISOCSH` | `54B` | ISO_CODE_SHIFT | роль: сдвиг ASN 54B при сборке 8-символьного слова; источник: S1:15685 | `src/FOREX_RUNTIME.mad:61` |
| `ISOWSH` | `64` | ISO_WORD_SHIFT | роль: сдвиг GOST/ISO-поля на 64 разряда; источник: S5:7676 | `src/FOREX_RUNTIME.mad:62` |
| `LIBBLN` | `2000B` | LIB_BUFFER_LEN | роль: длина BUFFER PU (0o2000 слов); источник: S1:15591 | `src/FOREX_RUNTIME.mad:63` |
| `LIT_10` | `10` | — | роль: ; S6:5067; источник: S6:5067 | `src/FOREX_RUNTIME.mad:64` |
| `LIT10M` | `10000000 00000000` | LIT_10000000_00000000 | роль: ; S1:15587 FTDCNS: LOG 10000000 00000000; источник: S1:15587 | `src/FOREX_RUNTIME.mad:65` |
| `LIT_2` | `2` | — | роль: ; S6:5058; источник: S6:5058 | `src/FOREX_RUNTIME.mad:66` |
| `LIT_3` | `3` | — | роль: ; S6:5055; источник: S6:5055 | `src/FOREX_RUNTIME.mad:67` |
| `MODE_6` | `6` | — | роль: режим NTR 6; источник: S5:7658 | `src/FOREX_RUNTIME.mad:68` |
| `MNTHIB` | `24` | MONTH_INDEX_BASE | роль: база индекса месяца; источник: S5:7671 | `src/FOREX_RUNTIME.mad:69` |
| `OCTSDM` | `=777 7777-C` | OCT_SIX_DIGIT_MASK | роль: маска 6 цифр OCTTDE; источник: S6:5047 | `src/FOREX_RUNTIME.mad:70` |
| `ONEW` | `1` | ONE_WORD | роль: одно слово / константа 1; источник: S1:15646 | `src/FOREX_RUNTIME.mad:71` |
| `P5` | `100000.0` | POW10_5 | роль: вещественный масштаб 10^5; источник: S6:5077 | `src/FOREX_RUNTIME.mad:72` |
| `RMOD3` | `3` | REAL_MODE_3 | роль: режим NTR 3 (вещественный); источник: S1:15612 | `src/FOREX_RUNTIME.mad:73` |
| `RETLR` | `13` | RET_LINK_REG | роль: номер индексного регистра связывания M13; источник: S1:15597 | `src/FOREX_RUNTIME.mad:74` |
| `STKOF1` | `-1` | STACK_OFF_M1 | роль: ; S5:7713; источник: S5:7713 | `src/FOREX_RUNTIME.mad:75` |
| `STKOF2` | `-2` | STACK_OFF_M2 | роль: ; S5:7662; источник: S5:7662 | `src/FOREX_RUNTIME.mad:76` |
| `STKOF3` | `-3` | STACK_OFF_M3 | роль: ; S5:7666; источник: S5:7666 | `src/FOREX_RUNTIME.mad:77` |
| `STKOF4` | `-4` | STACK_OFF_M4 | роль: ; S5:7678; источник: S5:7678 | `src/FOREX_RUNTIME.mad:78` |
| `STKOF5` | `-5` | STACK_OFF_M5 | роль: ; S5:7712; источник: S5:7712 | `src/FOREX_RUNTIME.mad:79` |
| `STKOF6` | `-6` | STACK_OFF_M6 | роль: ; S5:7694; источник: S5:7694 | `src/FOREX_RUNTIME.mad:80` |
| `SOM` | `-8` | STACK_OFF_M8 | роль: ; S5:7688; источник: S5:7688 | `src/FOREX_RUNTIME.mad:81` |
| `TL0000` | `''000000''` | TEXT_LIT_000000 | роль: ; S6:5083 ZERO = 8TEXT «000000»; источник: S6:5083 | `src/FOREX_RUNTIME.mad:82` |
| `TL0001` | `1H'055'` | TEXT_LIT_1H_055 | роль: ; S5:7717; источник: S5:7717 | `src/FOREX_RUNTIME.mad:83` |
| `TL0002` | `2H '200'` | TEXT_LIT_2H_200 | роль: ; S5:7715; источник: S5:7715 | `src/FOREX_RUNTIME.mad:84` |
| `TL0003` | `3H00` | TEXT_LIT_3H00 | роль: ; S5:7718; источник: S5:7718 | `src/FOREX_RUNTIME.mad:85` |
| `TL0004` | `=6H00` | TEXT_LIT_6H00 | роль: ; S5:7705; источник: S5:7705 | `src/FOREX_RUNTIME.mad:86` |
| `TL0005` | `6H0000` | TEXT_LIT_6H0000 | роль: ; S5:7729; источник: S5:7729 | `src/FOREX_RUNTIME.mad:87` |
| `TL0006` | `6H000000` | TEXT_LIT_6H000000 | роль: ; S7:458 ZERO = ISO 6H000000; источник: S7:458 | `src/FOREX_RUNTIME.mad:88` |
| `TL0007` | `6H000 00` | TEXT_LIT_6H000_00 | роль: ; S5:7719; источник: S5:7719 | `src/FOREX_RUNTIME.mad:89` |
| `TL0008` | `=6H00/00/` | TEXT_LIT_6H00_00 | роль: ; S5:7708; источник: S5:7708 | `src/FOREX_RUNTIME.mad:90` |
| `TL0009` | `6H03 0` | TEXT_LIT_6H03_0 | роль: ; S5:7728; источник: S5:7728 | `src/FOREX_RUNTIME.mad:91` |
| `TL0010` | `6HABГCEH` | TEXT_LIT_6HAB_CEH | роль: ; S5:7725; источник: S5:7725 | `src/FOREX_RUNTIME.mad:92` |
| `TL0011` | `6HARRAY` | TEXT_LIT_6HARRAY | роль: ; S1:15710; источник: S1:15710 | `src/FOREX_RUNTIME.mad:93` |
| `TL0012` | `6HAПPMAЯ` | TEXT_LIT_6HA_PMA | роль: ; S5:7723; источник: S5:7723 | `src/FOREX_RUNTIME.mad:94` |
| `TL0013` | `6HERROR` | TEXT_LIT_6HERROR | роль: ; S1:15707; источник: S1:15707 | `src/FOREX_RUNTIME.mad:95` |
| `TL0014` | `6HIN STA` | TEXT_LIT_6HIN_STA | роль: ; S1:15708; источник: S1:15708 | `src/FOREX_RUNTIME.mad:96` |
| `TL0015` | `6HNDART` | TEXT_LIT_6HNDART | роль: ; S1:15709; источник: S1:15709 | `src/FOREX_RUNTIME.mad:97` |
| `TL0016` | `6HOKTHOЯ` | TEXT_LIT_6HOKTHO | роль: ; S5:7730; источник: S5:7730 | `src/FOREX_RUNTIME.mad:98` |
| `TL0017` | `6H 00.00` | TEXT_LIT_6H_00_00 | роль: ; S5:7726; источник: S5:7726 | `src/FOREX_RUNTIME.mad:99` |
| `TL0018` | `=6H'17''17'''''''''` | TEXT_LIT_6H_17_17 | роль: ; S5:7704; источник: S5:7704 | `src/FOREX_RUNTIME.mad:100` |
| `TL0019` | `6H'201'  '200'7` | TEXT_LIT_6H_201_200_7 | роль: ; S5:7714; источник: S5:7714 | `src/FOREX_RUNTIME.mad:101` |
| `TL0020` | `6H'231'  ЯHB` | TEXT_LIT_6H_231_HB | роль: ; S5:7721; источник: S5:7721 | `src/FOREX_RUNTIME.mad:102` |
| `TL0021` | `=6H'3''17''''17''17'''` | TEXT_LIT_6H_3_17_17_17 | роль: ; S5:7707; источник: S5:7707 | `src/FOREX_RUNTIME.mad:103` |
| `TL0022` | `6HФEBMAP` | TEXT_LIT_6H_EBMAP | роль: ; S5:7722; источник: S5:7722 | `src/FOREX_RUNTIME.mad:104` |
| `TL0023` | `6HДEK` | TEXT_LIT_6H_EK | роль: ; S5:7731; источник: S5:7731 | `src/FOREX_RUNTIME.mad:105` |
| `TL0024` | `6HИЮHИЮЛ` | TEXT_LIT_6H_H | роль: ; S5:7724; источник: S5:7724 | `src/FOREX_RUNTIME.mad:106` |
| `FUNDTM` | `67B.DD.MM.YY.HH.MM` | FUN_DATE_TIME | роль: FUN 67B — системная дата/время; источник: S5:7657 | `src/FOREX_RUNTIME.mad:107` |
| `DBFLN` | `2` | DATE_BUF_LEN | роль: DATA* — 2-словный буфер даты; источник: S5:7646 | `src/FOREX_RUNTIME.mad:108` |
| `MNTHFO` | `00 776` | MONTH_FIELD_OCT | роль: маска поля месяца в FUN 67B; источник: S5:7732 | `src/FOREX_RUNTIME.mad:109` |
| `OCTISS` | `64-8` | OCT_ISO_SHIFT | роль: сдвиг ASN ISO-кода цифры; источник: S6:5070 | `src/FOREX_RUNTIME.mad:110` |
| `P4` | `10000.0` | POW10_4 | роль: вещественный масштаб 10^4; источник: S6:5078 | `src/FOREX_RUNTIME.mad:111` |
| `P3` | `1000.0` | POW10_3 | роль: вещественный масштаб 10^3; источник: S6:5079 | `src/FOREX_RUNTIME.mad:112` |
| `P2` | `100.0` | POW10_2 | роль: вещественный масштаб 10^2; источник: S6:5080 | `src/FOREX_RUNTIME.mad:113` |
| `P1` | `10.0` | POW10_1 | роль: вещественный масштаб 10^1; источник: S6:5081 | `src/FOREX_RUNTIME.mad:114` |

> Всего **88** `,EQU,`-констант в `src/FOREX_RUNTIME.mad`.


## 5. 6-символьное правило и проверки

МАДЛЕН различает метки и `EQU`-константы только первыми 6 знаками. Все новые
рантайм-имена короче или равны 6 и уникальны по первым 6; полное описание
вынесено в комментарии `; (полное: …)` и в §4 таблиц настоящего документа.
Автоматическая проверка: `docs/09-crossrefs.md` §7 «НАРУШЕНИЯ 6-СИМВОЛЬНОГО
ПРАВИЛА» и разделы `SIX_CHAR_VIOLATIONS` / `SIX_CHAR_COLLISIONS` лога
`logs/xref_all.txt` (копия — `logs/runtime_xref_global.txt`).
Правила именования и примеры коротких имён — `docs/10-naming-conventions.md` §6.

## 6. Воспроизводимость и связанные документы

```bash
cd /tmp/.private/azizz/opencode/re-forex
python3 tools/xref_all.py --out docs/09-crossrefs.md --log logs/runtime_xref_global.txt
bash tests/check-label-length.sh | tee logs/label_length.txt
```

Связанные документы: `docs/09-crossrefs.md` (глобальный свод),
`docs/10-naming-conventions.md` §6, `docs/06-address-map.md` §3/§3.1,
`docs/07-runtime.md`, `include/FOREX_RUNTIME.xref.md`,
`include/RUNTIME_DISASM.xref.md`, `include/RUNTIME_DECODER.xref.md`,
`include/RUNTIME_DISASM.registers.md`, `logs/runtime_xref_global.txt`.

**Неясности:** (1) нет карты загрузки MONSYS — переходы оверлеев на `0o77xxx`
не приписаны конкретным телам; (2) два тела `OCT_DEC` (S6 DECODER и S7
EXFOR), какое соответствует `04773`, без трассы не установлено; (3) LINK
`0o74010..0o74013` пер-модульные, путаница с FT* таблицей исключена §3.
