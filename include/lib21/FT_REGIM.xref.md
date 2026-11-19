# Перекрёстные ссылки модуля `FT*REGIM` (библиотека 21)

**Источник:** `libra211.l21:15713-15871`; проверка — `disasm/lib21/FT_REGIM.madlen`.

## 1. Объявления (NAME / ENTRY / SUBP / COMMON / TEXT / EQU)

| Метка (короткая) | Полное имя (POLN) | Тип | Комментарий |
|---|---|---|---|
| `FTRIM` | `FT_STARREGIM` | NAME | `` |
| `TAPST` | `TAPELIST` | LC | `BUFFO SC/FT SC/EC` |
| `MONCRD` | `_STARMONCRD_STAR` | LC | `PAR` |
| `PRINT8` | `PRINT8` | SUBP | `` |
| `FFP` | `FFP` | EQU | `=:170.CBOБOДHЫ 43-46 ЛИCTЫ` |
| `EXIT` | `EXIT` | BSS | `` |
| `NOBUF` | `NOBUF` | BSS | `` |
| `FB` | `FB` | BSS | `` |
| `WS` | `WS` | BSS | `1` |

## 2. Переходы и вызовы

| Строка | Команда | Операнд (короткий) | Направление |
|---|---|---|---|
| 41 | MTJ | `2.BOЗB` | внешний/абсолютный → `2.BOЗB` |
| 49 | UZA | `FS1` | внутренний → `FS1` |
| 55 | U1A | `FS` | внутренний → `FS` |
| 57 | CALL | `PARAMT` | внешний → `PARAMT` (LINK/имя корня ФОРЭКС) |
| 59 | CALL | `PARAMT` | внешний → `PARAMT` (LINK/имя корня ФОРЭКС) |
| 65 | CALL | `PARAMT` | внешний → `PARAMT` (LINK/имя корня ФОРЭКС) |
| 70 | UZA | `BUF` | внутренний → `BUF` |
| 75 | U1A | `ERRP` | внутренний → `ERRP` |
| 79 | UJ | `STATUS` | внутренний → `STATUS` |
| 88 | UJ | `EC` | внутренний → `EC` |
| 90 | UJ | `STATUS` | внутренний → `STATUS` |
| 92 | UJ | `STATUS` | внутренний → `STATUS` |
| 94 | UJ | `STATUS` | внутренний → `STATUS` |
| 96 | UJ | `STATUS` | внутренний → `STATUS` |
| 98 | UZA | `ABS` | внутренний → `ABS` |
| 101 | MTJ | `14` | внешний/абсолютный → `14` |
| 106 | UJ | `M` | внутренний → `M` |
| 109 | U1A | `NEXT` | внутренний → `NEXT` |
| 118 | UJ | `NEXT` | внутренний → `NEXT` |
| 121 | U1A | `ERRP` | внутренний → `ERRP` |
| 125 | UJ | `NEXT` | внутренний → `NEXT` |
| 135 | U1A | `ERRP` | внутренний → `ERRP` |
| 139 | UJ | `RFT` | внутренний → `RFT` |
| 141 | UJ | `—` | внешний/абсолютный → `—` |
| 148 | UJ | `PRINT8` | внешний (объявлен SUBP/TEXT) → `PRINT8` |
| 151 | MTJ | `13` | внешний/абсолютный → `13` |
| 152 | VJM | `PRINT` | внутренний → `PRINT` |

Всего переходов/вызовов: 27.

## 3. Связи с корнем ФОРЭКС и оверлеями

- Прямых ссылок на корень/оверлеи в теле не обнаружено; связь через LIBREFER/CATALOG.

## Экстракоды

Расшифровки по `rukava.be` (раздел 1.4). Подробности — `docs/lib21/04-extract-codes.md`.

| Код | Информационное слово | Расшифровка | Стр. | Применений | Места |
|-----|----------------------|-------------|------|------------|-------|
| Э57 | -CN1 | не найдено в rukava.be | — | 1 | `src/lib21/FT_REGIM.mad:172` |
| Э63 | CN677 | не найдено в rukava.be | — | 3 | `src/lib21/FT_REGIM.mad:90`, `src/lib21/FT_REGIM.mad:149`, `src/lib21/FT_REGIM.mad:161` |

## Текстовые константы и кодировки

Второй проход аудита (2026-11-19): не расшифрованные ранее текстовые
константы в кодировках ИСО (ISO), ГОСТ, UPP/континуации (CONT).
Первичное чтение — текст литерала из листинга Дубны/dtran; 6-битные
GOST6/TEXT6 — альтернативная интерпретация машиного слова.
Методика и сверка: `docs/19-dtran-text-encodings.md`,
`tools/dtran_text.py --audit`. Полный лог — `logs/text_audit_lib21_2.txt`.

| Метка/литерал | Кодировка | Первичное чтение | Источник |
|---|---|---|---|
| `EC    ` | ISO | `EC    ` | `src/lib21/FT_REGIM.mad:120` |
| `KERR  ` | ISO | `KERR  ` | `src/lib21/FT_REGIM.mad:121` |
| `RERR  ` | ISO | `RERR  ` | `src/lib21/FT_REGIM.mad:122` |
| `TEST  ` | ISO | `TEST  ` | `src/lib21/FT_REGIM.mad:123` |
| `STERR ` | ISO | `STERR ` | `src/lib21/FT_REGIM.mad:124` |
| `BUF   ` | ISO | `BUF   ` | `src/lib21/FT_REGIM.mad:125` |
| `OШИБKA` | ISO | `OШИБKA` | `src/lib21/FT_REGIM.mad:193` |
| `Y MEHЯ` | ISO | `Y MEHЯ` | `src/lib21/FT_REGIM.mad:196` |
| `REGIM   ` | TEXT(=6H) | `REGIM   ` | `src/lib21/FT_REGIM.mad:112` |

Добавлено декодирований: 9.
