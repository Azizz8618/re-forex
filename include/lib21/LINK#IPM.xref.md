# Перекрёстные ссылки модуля `LINK/IPM` (библиотека 21)

**Источник:** `libra212.l21:2304-2499`; проверка — `disasm/lib21/LINK#IPM.madlen`.

## 1. Объявления (NAME / ENTRY / SUBP / COMMON / TEXT / EQU)

| Метка (короткая) | Полное имя (POLN) | Тип | Комментарий |
|---|---|---|---|
| `LINPM` | `LINK_SLASHIPM` | NAME | `.P B C: 3/74` |
| `MONRD` | `MONCARD_SLASH` | LC | `CARD(14)` |
| `REGIM` | `_STARREGIM_SLASH_SLASH` | LC | `REGIM` |
| `NOLISF` | `NO_LIST_FLAG` | LC | `LISTFL` |
| `RM` | `RM_STAR` | LC | `RM` |
| `MONOR` | `MONITOR_STAR` | SUBP | `.` |
| `БEMAP` | `БEMШ_SLASHПAP` | SUBP | `.` |
| `ПAP/MЛ` | `ПAP_SLASHMЛ` | LC | `MAT/N` |
| `GIV/MT` | `GIV_SLASHMT` | SUBP | `.` |
| `READ*` | `READ_STAR` | SUBP | `.` |
| `PRINT8` | `PRINT8_SLASH_SLASH` | SUBP | `.` |
| `DATAPR` | `DATE_PRINT` | SUBP | `.` |
| `LINKED` | `LINKED` | ENTRY | `.ДOП. BXOД` |
| `RETMON` | `RETMON` | BSS | `.` |
| `CONRET` | `CON_SLASHRET` | BSS | `.` |
| `PRINTC` | `PRINT_SLASHC` | BSS | `.ДЛИHHAЯ KAPTA` |
| `S17` | `S17` | BSS | `1.` |
| `LINE` | `LINE` | BSS | `14` |

## 2. Переходы и вызовы

| Строка | Команда | Операнд (короткий) | Направление |
|---|---|---|---|
| 22 | UJ | `BEGIN` | внутренний → `BEGIN` |
| 30 | UZA | `RETMEM` | внутренний → `RETMEM` |
| 41 | UJ | `17B` | внешний/абсолютный → `17B` |
| 44 | UJ | `MONITO` | внешний/абсолютный → `MONITO` |
| 46 | UJ | `CONRET` | внутренний → `CONRET` |
| 47 | Z00 | `RET/67` | внутренний → `RET/67` |
| 55 | UJ | `RETMON` | внутренний → `RETMON` |
| 56 | Z00 | `*+1` | внешний/абсолютный → `*+1` |
| 57 | Z00 | `76000B` | внешний/абсолютный → `76000B` |
| 59 | UIA | `NO` | внешний/абсолютный → `NO` |
| 60 | CALL | `DATAPR` | внешний (объявлен SUBP/TEXT) → `DATAPR` |
| 66 | CALL | `PRINT8` | внешний (объявлен SUBP/TEXT) → `PRINT8` |
| 71 | CALL | `PRINT8` | внешний (объявлен SUBP/TEXT) → `PRINT8` |
| 77 | CALL | `READ*` | внешний (объявлен SUBP/TEXT) → `READ*` |
| 79 | UIA | `NO` | внешний/абсолютный → `NO` |
| 82 | UIA | `NO` | внешний/абсолютный → `NO` |
| 100 | CALL | `PRINT8` | внешний (объявлен SUBP/TEXT) → `PRINT8` |
| 104 | UIA | `PRINTC` | внутренний → `PRINTC` |
| 106 | UJ | `NO` | внешний/абсолютный → `NO` |
| 114 | CALL | `PRINT8` | внешний (объявлен SUBP/TEXT) → `PRINT8` |
| 115 | UJ | `NO` | внешний/абсолютный → `NO` |
| 121 | CALL | `PRINT8` | внешний (объявлен SUBP/TEXT) → `PRINT8` |
| 130 | UIA | `NO` | внешний/абсолютный → `NO` |
| 153 | UIA | `READ/L` | внешний/абсолютный → `READ/L` |
| 155 | UIA | `TO` | внешний/абсолютный → `TO` |
| 156 | VJM | `PRINT8` | внешний/абсолютный → `PRINT8` |
| 158 | CALL | `GIV/MT` | внешний (объявлен SUBP/TEXT) → `GIV/MT` |
| 182 | UJ | `40600B` | внешний/абсолютный → `40600B` |

Всего переходов/вызовов: 28.

## 3. Связи с корнем ФОРЭКС и оверлеями

- `DATAPR*` — печать даты: упоминается в теле модуля.

## Экстракоды

Расшифровки по `rukava.be` (раздел 1.4). Подробности — `docs/lib21/04-extract-codes.md`.

| Код | Информационное слово | Расшифровка | Стр. | Применений | Места |
|-----|----------------------|-------------|------|------------|-------|
| Э57 | 4000 | не найдено в rukava.be | — | 1 | `src/lib21/LINK#IPM.mad:244` |
| Э67 | DEB | не найдено в rukava.be | — | 1 | `src/lib21/LINK#IPM.mad:120` |
| Э70 | 21 | не найдено в rukava.be | — | 1 | `src/lib21/LINK#IPM.mad:237` |
| Э72 | COTK2+NT3 | не найдено в rukava.be | — | 1 | `src/lib21/LINK#IPM.mad:111` |
