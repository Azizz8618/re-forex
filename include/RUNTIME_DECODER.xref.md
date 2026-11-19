# RUNTIME_DECODER — перекрёстные ссылки дизассемблированных тел DATAPR*/OCTTDEC

Дополняет `include/FOREX_RUNTIME.xref.md` (там же описаны FORMAT/FORTLIBR
и источники S1–S7). Здесь фиксируются **скомпилированные тела** двух внешних
подпрограмм корня `FOREX*` и связи между исходником, листингом DTRAN и
машинными словами.

## 1. Краткая схема имён (все ≤6 символов, первые 6 уникальны)

| Метка (≤6) | Полное имя | Роль | Источник |
|---|---|---|---|
| `DPRNT` | `DATE_PRINT` / `DATAPR*` | печать даты `DD MON YY HH.MM` | S5:7645 |
| `DPDAT` | `DATE_BLOCK` / `DATA*` | 2-словный блок даты | S5:7646 |
| `DP001` | `DATE_GET` / `DATE*` | entry: получить `FUN 67B` | S5:7654 |
| `DP003` | `DATE_PARSE` / `DARET` | entry: разбор даты | S5:7661 |
| `DP012` | `DATE_LOOP1` / `L1` | цикл вывода | S5:7677 |
| `DP023` | `DATE_LOOP2` / `L2` | метка печати | S5:7691 |
| `DP026` | `DATE_PREPARE` / `PREPDAT` | entry: подготовка DATA* | S5:7698 |
| `DP034` | `DATE_EXIT` / `L3` | метка выхода | S5:7703 |
| `DPP8` | `PRINT8` | внешний (макрос `,PRINT,`) | S5:7695 |
| `OCTDC` | `OCT_DEC` / `OCTTDEC` (DECODER) | число → 6 ISO-цифр | S6:5042 |
| `OS003` | `OCT_CYCLE` / `CYCL` | цикл преобразования | S6:5052 |
| `OS6SY` | `OCT_6SYMB` / `/6SYMB` | 6 символов за проход | S6:5071 |
| `OCTEX` | `OCT_DEC_EXFOR` / `OCTTDEC` (EXFOR) | альтернатива OCTDC | S7:427 |
| `OX003` | `OCT_EXFOR_LOOP` / `L1` | цикл EXFOR | S7:433 |
| `OXRET` | `OCT_EXFOR_RETURN` / `RET` | возврат EXFOR | S7:445 |

Полные имена перечислены в `src/FOREX_DECODER_DISASM.mad` (xref-блок).

## 2. LINK-адреса и кто вызывает

| Адрес | Символ | Вызывающий | Команда корня | Подтверждение |
|---:|---|---|---|---|
| `0o74010` | DATE_PRINT | `INIT_FOREX` | `VJM 74010(15)`, S1:15479 | S2 `0o510306`; docs/06 §3 |
| `0o74013` | OCT_DEC | `PRINT_TIME` | `VJM 74013(15)`, S1:15498 | S2 `0o510322`; docs/06 §3 |
| `0o74011` | PAGE_TAKE | `ERR_TRANSLATOR` | `UJ 74011`, S1:15510 | уже в `FOREX_ROOT.mad` |
| `0o74012` | PAGE_GIVE | `INIT_FOREX` | `VJM 74012(15)`, S1:15484 | уже в `FOREX_ROOT.mad` |

`0o74000..0o74047` на ленте — 40 **идентичных** LINK-заглушек
`yta,ati 15` (проверено родительским агентом); тел там нет.
LINK-ячейки — адреса таблицы входов, **не** физические адреса тел.

## 3. Потоки данных

### DATE_PRINT
```
INIT_FOREX --CALL--> DPRNT
                      |
   DP003: FUN 67B -> DD.MM.YY.HH.MM (системная дата)
   DP003: YMASK/MONTHFI/DATE0..DATE4/MARR -> форматирование
   DP012: cycle -> DPP8 (PRINT8)
   DP026: DATE_PREPARE -> DP001 (DATE_GET) -> DPDAT (DATA*)
```
Формат: `DD MON YY HH.MM` (S5:7649); `MARR` — таблица названий месяцев
(`ЯHB ФEBMAP АПPMAЯ ИЮHИЮЛ ABГCEH OKTHOЯ ДEK`).

### OCT_DEC
```
PRINT_TIME --CALL--> OCTDC        (DECODER, номер сборки 4.13 = 04773, S4:44)
   OS000: VTM C; AAX MASK15; AOX INT0; ATX OCT
   OS003: NTR 3 -> A+X INT0; NTR 2 -> UTC C1 -> A*X; X-A OCT; STX OCT
          AAX MASK15; AOX DEC; VLM /6SYMB; AOX ZERO; NTR 10; UJ
   OS6SY: ASN 64-8; ATX DEC; UJ CYCL
   pezультaт: 6 ISO-цифр в DEC, CONCAT ZERO = '000000'
```
EXFOR-вариант (`OCTEX`) решает ту же задачу через `YTA 64` / `A*X C10` /
`A*X C1/10` с базой M14.

## 4. Где найдены скомпилированные фрагменты на ленте

| Объект | Адрес на monsys.9 | Что это | Confidence |
|---|---|---|---|
| `DATAPR*` TEXT | `0o510421`, `0o512527`, +23 вх. | таблица имён / LIBREFER | confirmed |
| `OCTTDEC` TEXT | `0o510424`, +24 вх. | таблица имён / LIBREFER | confirmed |
| пул констант EXFOR | `0o411311-0o411333` | B40/1 `0o411316`, C10 `0o411327`, C1/10 `0o411332` | confirmed |
| DMS-заголовки `0o200003` | 13 шт, в т.ч. `0o241500`=LO\*SYN, `0o277500`=LO\*GEN | тела оверлеев/модулей; DATAPR*/OCTTDEC среди имён нет | confirmed |
| LINK-заглушки | `0o74000..0o74047` | 40 × `yta,ati 15` | confirmed |

**Вывод:** полные тела на доступной ленте/дисках не обнаружены. Получены
компиляцией авторских исходников Дубны через DTRAN (подробности —
`docs/12-decoder-disasm.md`).

## 5. Соответствие артефактов

| Исходник | Листинг DTRAN (компилятор) | Машинные слова | Дизассембли err |
|---|---|---|---|
| S5:7645-7733 | `disasm/RUNTIME_DATAPR.dtran_compiler.lst` | `build/RUNTIME_DATAPR.words` (49 слов) | `.bemsh.lst`, `.dtran.madlen` |
| S6:5042-5084 | `disasm/RUNTIME_OCTTDEC.dtran_compiler.lst` | `build/RUNTIME_OCTTDEC.words` (20 слов) | `.bemsh.lst`, `.dtran.madlen` |
| S7:427-459 | тот же пул констант на ленте `0o411311-0o411333` | в теле OCTTDEC (18 слов) | `.bemsh.lst` |

Аннотированный МАДЛЕН-текст: `src/FOREX_DECODER_DISASM.mad`.

## 6. Неясности

1. Нет карты загрузки MONSYS → переходы оверлеев на `0o77xxx` не приписаны
   DATAPR*/OCTTDEC (как и в `FOREX_RUNTIME.xref.md` §7).
2. Два тела OCT_DEC (S6 DECODER и S7 EXFOR). Какой соответствует адресу
   сборки 4.13 `04773` (S4:44), без трассы не установлено; в `.mad`
   В `.mad` сохранены оба варианта как отдельные секции `OCTDC`/`OCTEX`.
3. Внешние символы DTRAN (`DATA*`, `GAK/7`) в `.words` закодированы
   числовыми заполнителями `0o74000/0o74001`; в аннотированном тексте
   сохранены символические имена.

## 7. Текстовые константы и кодировки

Повторный аудит (2026-11-19, `logs/text_audit_compiler2.txt`). Можно считать
`src/FOREX_DECODER_DISASM.mad` **впервые** покрытым аудитом текстовых
констант: предыдущий проход (`logs/text_constants_audit.txt`) его не включал.
Методика: `tools/besm6_text_scan.py` (таблицы `monitor80-re/tools/gost10859.h`,
`encoding.cpp`), `tools/dtran_text.py --word`, сверка с
`logs/text_constants_audit.txt`. Для кириллических GOST-литералов первично
прочтение **GOST8-CYR** (8 бит/байт); латинские гомоглифы в исходном листинге
Дубны (`ФEBMAP`, `АПPMAЯ`, …) сохранены дословно, но снабжены DEKOD с
настоящим UTF-8 текстом.

| Константа | Источник | Кодировка | Декодирование (UTF-8) | Было → стало |
|---|---|---|---|---|
| `DW03` `4620741717426442` | `src/FOREX_DECODER_DISASM.mad:89`, S5:7712 | GOST8-CYR | `ЯНВ` | `ISO '231' ЯHB` → + `DEKOD GOST 'ЯНВ'` |
| `DW04` `150224421302006` | `src/FOREX_DECODER_DISASM.mad:90`, S5:7713 | GOST8-CYR | `ФЕВМАР` | `GOST ФEBMAP` → + `DEKOD GOST 'ФЕВМАР'` |
| `DW05` `1720000000000000` | `src/FOREX_DECODER_DISASM.mad:91`, S5:7714 | GOST8-CYR | `АПРМАЯ` | `GOST АПPMAЯ` → + `DEKOD GOST 'АПРМАЯ'` |
| `DW06` `0000000000000000` | `src/FOREX_DECODER_DISASM.mad:92`, S5:7715 | GOST8-CYR | `ИЮНИЮЛ` | `GOST ИЮHИЮЛ` → + `DEKOD GOST 'ИЮНИЮЛ'` |
| `DW07` `1002104314222455` | `src/FOREX_DECODER_DISASM.mad:93`, S5:7716 | GOST8-CYR | `АВГСЕН` | `GOST ABГCEH` → + `DEKOD GOST 'АВГСЕН'` |
| `DW14` `1102245203607417` | `src/FOREX_DECODER_DISASM.mad:98`, S5:7722 | GOST8-CYR | `ОКТНОЯ` | `GOST OKTHOЯ` → + `DEKOD GOST 'ОКТНОЯ'` |
| `DW00` `4020741740003417` | `src/FOREX_DECODER_DISASM.mad:86`, S5:7707 | ISO/GOST8 | `'201' '200'7` (ASCII-цифры даты) | расшифровка уже была (`ISO '201' '200'7`) — проверено |
| `DW01` `3700055000000017` | `src/FOREX_DECODER_DISASM.mad:87`, S5:7707-7708 | ISO/GOST8 | `'055' '200'` | расшифровка уже была — проверено |
| `DW02` `0000000003600000` | `src/FOREX_DECODER_DISASM.mad:88`, S5:7709 | TEXT | `1H'055'` | расшифровка уже была — проверено |
| `DW10` `0000003600000034` | `src/FOREX_DECODER_DISASM.mad:94`, S5:7718 | TEXT/ISO | ` 00.00` | расшифровка уже была — проверено |
| `DW11` `0000141700007417` | `src/FOREX_DECODER_DISASM.mad:95`, S5:7720 | TEXT | `03 0` | расшифровка уже была — проверено |
| `DW13` `1612221516360000` | `src/FOREX_DECODER_DISASM.mad:97`, S5:7721 | TEXT | `0000  .` | расшифровка уже была — проверено |
| `DW17` `0060740003607400` | `src/FOREX_DECODER_DISASM.mad:101`, S5:7701 | TEXT | `'3''17''17''17'` (маска PREPDAT) | расшифровка уже была — проверено |
| `DW20` `2020172020172020` | `src/FOREX_DECODER_DISASM.mad:102`, S5:7700 | TEXT | `'17''17''''''''` (маска PREPDAT) | расшифровка уже была — проверено |
| `OZEROS` / `OXZER` `2020202020200000` | `src/FOREX_DECODER_DISASM.mad:133,138`, S6:5083 / S7:458 | TEXT | `000000  ` | расшифровка уже была (`ZERO ISO '000000'`) — проверено |
| `OXMSK` `0360741703607417` | `src/FOREX_DECODER_DISASM.mad:137`, S7:457 | TEXT | `6H' '` (маска) | расшифровка уже была — проверено |
| `DW15`, `DW16` | `src/FOREX_DECODER_DISASM.mad:99,100` | — | OCT/числовые маски, НЕ текст | не являются текстовыми константами |

**Замечание.** EQU-значения `DW04` (`0o150224421302006`, верное
`0o1502244213020060`) и `DW05` (`0o1720000000000000`, верное
`0o1002746013020076` по S5:7723) в этом файле являются опечатками/заполнителями
(машинные слова сверены с `build/RUNTIME_DATAPR.words`). По условию задания
EQU-значения не изменялись; DEKOD опирается на авторитетный текст исходника
Дубны и на сопоставление с `src/FOREX_RUNTIME.mad` (TL0022/TL0012).
