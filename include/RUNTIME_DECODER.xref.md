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
