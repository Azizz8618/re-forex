# RUNTIME_DISASM — перекрёстные ссылки дизассемблированных тел FORMAT / FORTLIBR

Источник: `src/FOREX_RUNTIME_DISASM.mad` (настоящий дизассемблер ленты `monsys.9`),
не путать с `src/FOREX_RUNTIME.mad` (дословная перепечатка листинга `libra211.l21`).

## 1. Границы скомпилированных тел на ленте

| Модуль | Диапазон (слово ленты) | Число слов | Состав |
|---|---|---|---|
| `FORMAT`  | `0o510443` – `0o510537` | 61 | код `0o510443-0o510472` (24), имя `0o510473`, таблица ячеек передачи `0o510474-0o510506` (11), рело-константы `0o510507-0o510522` (12), t6-имена `FT*` `0o510523-0o510535` (11), _END-маркер `0o510536-0o510537` (2) |
| `FORTLIBR`| `0o510543` – `0o510647` | 69 | код `0o510543-0o510623` (49), константы `0o510624-0o510643` (16), ISO-тексты `0o510644-0o510647` (4) |

Проверка: `besm6tape.py dis --start 0o510443 --count 61` и
`--start 0o510543 --count 69`. Соседние области `0o74000..0o77777` — LINK-заглушки
`yta,ati 15`, тел там нет (уточнение родительского агента подтверждено).

## 2. Перекрёстные ссылки FORMAT

- **Кто вызывает:** библиотека `LIBREFER` / каталог `0o502124-0o502127`;
  экспорт 11 символов `FT*002, FT*003, FT*521 … FT*721` (`reference/expect_library21.txt:206-216`).
- **Кого вызывается:** 11 LINK-ячеек старшего поля:

| LINK | Подпрограмма | Ячейка приёма | Источник |
|---|---|---|---|
| `X01` = `0o74001` | `FT*571` (импорт из **ANL**, `S3:1075`) | `D571DS` = `0o77207` | S1:15565-15566 |
| `X02` = `0o74002` | `FT*541` | `D541DS` = `0o77237` | S1:15567-15568 |
| `X03` = `0o74003` | `FT*611` | `D611DS` = `0o77167` | S1:15569-15570 |
| `X04` = `0o74004` | `FT*531` | `D531DS` = `0o77247` | S1:15571-15572 |
| `X05` = `0o74005` | `FT*561` | `D561DS` = `0o77217` | S1:15573-15574 |
| `X06` = `0o74006` | `FT*621` | `D621DS` = `0o77157` | S1:15575-15576 |
| `X07` = `0o74007` | `FT*521` | `D521DS` = `0o77257` | S1:15577-15578 |
| `X10` = `0o74010` | `FT*721` | `D721DS` = `0o77057` | S1:15579-15580 |
| `X11` = `0o74011` | `FT*641` | `D641DS` = `0o77137` | S1:15581-15582 |
| `X12` = `0o74012` | `FT*002` | `D002DS` = `0o77776` | S1:15583-15584 |
| `X13` = `0o74013` | `FT*003` | `D003DS` = `0o77775` | S1:15585-15586 |

- **Внешние адреса с пометкой:** `0o74001-0o74013` — LINK (не код модуля);
  `0o77207 … 0o77776` — ячейки передачи (заполняются диспетчером);
  `0o77766` (`FTBTAB`) — база таблицы передач.

## 3. Перекрёстные ссылки FORTLIBR

- **Кто вызывает:** `PRINT8` — `S3:217`, `S4` (FOREX 4.13) адрес `03324`;
  `WRITLIBR` — `S3:1313` (импорт из FORTLIBR).
- **Кого вызывает:** `WRITLIBR+1` (подготовка буфера, `S1:15603`) и
  `PRINT8` (печать, `S1:15615`) — оба внутри одного модуля; LINK-ячейка
  `X01 = 0o74001` используется как адрес `BUFFER` (`S1:15620`).
- **Внутренние ветвления:** `LIBA10, LIBA23, LIBA27, LIBA32, LIBA36, LIBA42,
  LIBA45, LIBA50, LIBA53` — точки входа/ветвления WRITLIBR; `LIBENT` — PRINT8.

## 4. Таблица «короткое имя ↔ полное описание»

МАДЛЕН различает только первые 6 знаков — поэтому все имена короче или равны 6.

| Короткое | Полное | Роль |
|---|---|---|
| `FMTENT` | FORMAT_ENTRY | вход диспетчера (0o510443) |
| `FMT004` | FMT_LABEL_0004 | точка входа расчёта таблицы |
| `FMT005` | FMT_LABEL_0005 | начало цикла VLM |
| `FMT010` | FMT_LABEL_0010 | расчёт смещения ASN 155B |
| `FMT012` | FMT_LABEL_0012 | запись STX в таблицу |
| `FMT026` | FMT_LABEL_0026 | конец таблицы передач |
| `FMT027` | FMT_LABEL_0027 | константа FTD_CONST |
| `FMTTAB` | FMT_TRANSFER_TABLE | 11 пар UJ/ATX |
| `FMTLST` | FMT_TABLE_END | конец кода |
| `FMTNAM` | FMT_MODULE_NAME | t6 'FORMAT  ' |
| `FMTXLT` | FMT_XLAT_TABLE | 11 адресов ячеек передачи |
| `FMTCST` | FMT_RELOC_CONST | 12 младших 12 бит адресов 77xxxB |
| `FMTXNM` | FMT_EXT_NAMES | 11 t6-имён FT* |
| `FMTEND` | FMT_END_MARKER | _END-маркер библиотеки |
| `FTADR`  | FT_ADDR_FIELD | маска 103B |
| `FTOFSM` | FT_OFFSET_MASK | маска 155B |
| `FTBTAB` | FTD_TABLE_BASE_ADDR | база 77766B |
| `FTLOG`  | FTD_CONST | константа 10000000 00000000 |
| `LIBENT` | FORTLIBR_ENTRY / PRINT8 | вход PRINT8 |
| `LIBA14` | WRITLIBR_ENTRY | вход WRITLIBR (*00014) |
| `LIBA10` | LIB_LABEL_0010 | ветвление PRINT8 |
| `LIBA23` | LIB_LABEL_0023 | проверка знака |
| `LIBA27` | LIB_LABEL_0027 | XOR-цикл сборки слова |
| `LIBA32` | LIB_LABEL_0032 | случай WTC/ARX |
| `LIBA36` | LIB_LABEL_0036 | альтернативный случай |
| `LIBA42` | LIB_LABEL_0042 | сдвиг ISO-кода |
| `LIBA45` | LIB_LABEL_0045 | сравнение мантиссы |
| `LIBA50` | LIB_LABEL_0050 | обработка минуса |
| `LIBA53` | LIB_LABEL_0053 | сборка цифры |
| `BAS61`  | LIB_CONST_BASE | база констант *00061 |
| `C062`…`C077`, `C100`, `C101` | LIB_CONST_0062 … | ячейки констант/текстов |
| `LIBISO` | LIB_ERROR_TEXT | ISO-тексты диагностики |
| `LIBBUF` | LIB_BUFFER_LEN | длина BUFFER (0o2000) |
| `ZERO/ONE/TWO/TRIO/SEVEN` | ZERO / ONE_WORD / TWO / REAL_MODE_3 / DEC_7 | числовые литералы |
| `M1777`  | MASK_1777 | маска 1777B |
| `ISOHI`  | HIGH_BIT_ISO | старший бит ISO-цифры |
| `MSK73`  | SIGN_EXP_MASK | маска 37777774 77777477 |
| `MSK76`  | EXTRACT_MASK | маска 77270707 00000000 |
| `ISOSHF` | ISO_CODE_SHIFT | ASN 54B |
| `ALL1`   | ALL_ONES_MASK | маска 77777B |
| `BAS14/LNK13/WRK07` | BASE_REG14 / RET_LINK_REG / WORK_REG7 | номера регистров |

Проверка имён (≤6 знаков, уникальность первых 6) — в `logs/runtime_disasm_names.txt`.

## 5. Связь с исходником

Дизассемблированный код дословно соответствует `reference/libra211.format.inc`:
FORMAT — `S1:15541-15586`, FORTLIBR — `S1:15594-15690`. Отличия только в
объектной обвязке (LINK-адреса 740xx вместо символических `FT*`, L-адреса
вынесены в рело-таблицу, t6/ASCII-тексты вместо `ISO ,6H...`).

## 6. Текстовые константы и кодировки

Повторный аудит (2026-11-19, `logs/text_audit_compiler2.txt`). Файл
`src/FOREX_RUNTIME_DISASM.mad` не входил в предыдущий проход
(`logs/text_constants_audit.txt`); все текстовые константы проверены впервые.
Методика: `tools/dtran_text.py`, `tools/besm6_text_scan.py`, сверка с лентой
`monsys.9` (адреса 0o510473, 0o510536-0o510537) и `reference/libra211.format.inc`.

| Константа | Источник | Кодировка | Декодирование (UTF-8) | Было → стало |
|---|---|---|---|---|
| t6-имя `FORMAT  ` | `src/FOREX_RUNTIME_DISASM.mad:192`, лента 0o510473 | TEXT (6 бит×8, t6) | `FORMAT  ` | `t6-имя модуля 'FORMAT  '` → + `DEKOD TEXT 'FORMAT  '` |
| END-маркер `GFEDCBA+` | `src/FOREX_RUNTIME_DISASM.mad:196`, лента 0o510536-0o510537 | TEXT (6 бит×8, t6) | `GFEDCBA+` | `END-маркер ('GFEDCBA+')` → + `DEKOD TEXT 'GFEDCBA+'` |
| `C101` / `ERROR` | `src/FOREX_RUNTIME_DISASM.mad:289,388`, S1:15610/15707 | ISO (6 ASCII-байт) | `ERROR  ` | `текст ошибки 'ERROR'` → + `DEKOD ISO 'ERROR  ' / TEXT 'ERROR   '` |
| `,ISO,'ERROR  '` | `src/FOREX_RUNTIME_DISASM.mad:388`, S1:15707 | ISO | `ERROR  ` | расшифровка уже была (`ISO ,6HERROR`) — проверено |
| `,ISO,'IN STA'` | `src/FOREX_RUNTIME_DISASM.mad:390`, S1:15708 | ISO | `IN STA` | расшифровка уже была (`ISO ,6HIN STA`) — проверено |
| `,ISO,'NDART '` | `src/FOREX_RUNTIME_DISASM.mad:391`, S1:15709 | ISO | `NDART` | расшифровка уже была (`ISO ,6HNDART`) — проверено |
| `,ISO,'ARRAY '` | `src/FOREX_RUNTIME_DISASM.mad:392`, S1:15710 | ISO | `ARRAY` | расшифровка уже была (`ISO ,6HARRAY`) — проверено |

Диагностические ISO-строки `ERROR/IN STA/NDART/ARRAY` совпадают с
GOST/TEXT-литералами `6HERROR`, `6HIN STA`, `6HNDART`, `6HARRAY` в
`src/FOREX_RUNTIME.mad:96-98,94` (DEKOD добавлен предыдущим проходом).
