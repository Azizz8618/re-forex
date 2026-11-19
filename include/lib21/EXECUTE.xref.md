# Перекрёстные ссылки модуля `EXECUTE` (библиотека 21)

**Источник:** `libra211.l21:13875-14312`; проверка — `disasm/lib21/EXECUTE.madlen`.

## 1. Объявления (NAME / ENTRY / SUBP / COMMON / TEXT / EQU)

| Метка (короткая) | Полное имя (POLN) | Тип | Комментарий |
|---|---|---|---|
| `EXETE` | `EXECUTE` | NAME | `.30.10.79` |
| `MONOR` | `MONITOR_STAR` | SUBP | `` |
| `/VERE/` | `_SLASHVERE_SLASH` | LC | `(2) STALOA A/CAT INF0` |
| `INFLOD` | `INFLOAD_STAR` | LC | `ALOAD (1) INFMD INFDM` |
| `MAIN*` | `MAIN_STAR` | LC | `1` |
| `ERRLG` | `ERROFLG_STAR` | LC | `1` |
| `LOAIS` | `LOADLIS_STAR` | LC | `1` |
| `RM` | `RM_STAR` | LC | `RM(5)` |
| `KCNT` | `KCOUNT_STAR` | LC | `KC*(4)` |
| `LHEAP*` | `LHEAP_STAR` | LC | `1` |
| `LOADAN` | `LOAD_OVERLAY` | SUBP | `` |
| `BLEIN` | `BLEXPRIN` | SUBP | `` |
| `STOP*` | `STOP_STAR` | SUBP | `` |
| `NEW*OV` | `NEW_STAROV` | BSS | `` |
| `CHMX` | `CHMX` | BSS | `` |
| `MIXAD` | `MIXLOAD` | BSS | `` |
| `PRIOM` | `PRINTCOM` | BSS | `` |
| `CLTMP` | `CLTMP` | BSS | `` |
| `R1Z` | `R1Z` | BSS | `` |
| `—` | `—` | BSS | `` |
| `—` | `—` | BSS | `` |
| `—` | `—` | BSS | `` |
| `X1` | `X1` | BSS | `1` |
| `INFD` | `INFD` | BSS | `1` |
| `INFT` | `INFT` | BSS | `1` |
| `NZ` | `NZ` | BSS | `1` |
| `LPART` | `LPART` | BSS | `1` |
| `LS` | `LS` | BSS | `1` |
| `TFRAG` | `TEXT_FRAG_TPP` | TEXT | `8HFRAG TPП` = "FRAG ТРП" (было `FRAG TPП`) |

## 2. Переходы и вызовы

| Строка | Команда | Операнд (короткий) | Направление |
|---|---|---|---|
| 37 | U1A | `BLEIN` | внешний (объявлен SUBP/TEXT) → `BLEIN` |
| 40 | U1A | `EXEC` | внутренний → `EXEC` |
| 46 | CALL | `PARAMT` | внешний → `PARAMT` (LINK/имя корня ФОРЭКС) |
| 51 | CALL | `PARAMT` | внешний → `PARAMT` (LINK/имя корня ФОРЭКС) |
| 57 | U1A | `OШПAPA` | внешний/абсолютный → `OШПAPA` |
| 66 | UZA | `NEW*OV` | внутренний → `NEW*OV` |
| 70 | U1A | `OШKAЛ` | внутренний → `OШKAЛ` |
| 79 | U1A | `REDOR` | внутренний → `REDOR` |
| 87 | UZA | `MAЛOMЛ` | внешний/абсолютный → `MAЛOMЛ` |
| 134 | UZA | `OLD` | внешний/абсолютный → `OLD` |
| 147 | UIA | `CH` | внешний/абсолютный → `CH` |
| 150 | UZA | `MIXAD` | внутренний → `MIXAD` |
| 171 | CALL | `PRINT8` | внешний → `PRINT8` (LINK/имя корня ФОРЭКС) |
| 177 | U1A | `CLTMP` | внутренний → `CLTMP` |
| 214 | UZA | `TRANS` | внутренний → `TRANS` |
| 228 | UZA | `DRUM.=` | внешний/абсолютный → `DRUM.=` |
| 231 | UZA | `TRANS.` | внешний/абсолютный → `TRANS.` |
| 245 | UZA | `END` | внешний/абсолютный → `END` |
| 288 | UZA | `LOOP.A` | внешний/абсолютный → `LOOP.A` |
| 306 | UJ | `TRANS.` | внешний/абсолютный → `TRANS.` |
| 312 | UJ | `EX` | внешний/абсолютный → `EX` |
| 351 | U1A | `TO` | внешний/абсолютный → `TO` |
| 357 | UJ | `LOADAN` | внешний (объявлен SUBP/TEXT) → `LOADAN` |
| 362 | UJ | `ERROR` | внутренний → `ERROR` |
| 364 | UJ | `ERROR` | внутренний → `ERROR` |
| 371 | CALL | `PRINT8` | внешний → `PRINT8` (LINK/имя корня ФОРЭКС) |

Всего переходов/вызовов: 26.

## 3. Связи с корнем ФОРЭКС и оверлеями

- `LOADANGO` — загрузчик оверлеев: упоминается в теле модуля.

## 4. Семантическое именование (этап 12)

- Авто-меток вида `W/L/D+NNNN` переименовано: **0**.
- TEXT-констант переименовано по содержимому: **2**.
- Смещений `LABEL+NNNB` → десятичное: **0**.
- Новые имена ≤6 символов, первые 6 уникальны в файле; полное имя — в `POLN:`.
- Таблица «было → стало» и исходные восьмеричные значения: `logs/labels_semantics_lib21_core.txt`.

## Экстракоды

Расшифровки по `rukava.be` (раздел 1.4). Подробности — `docs/lib21/04-extract-codes.md`.

| Код | Информационное слово | Расшифровка | Стр. | Применений | Места |
|-----|----------------------|-------------|------|------------|-------|
| Э63 | CN766 | не найдено в rukava.be | — | 2 | `src/lib21/EXECUTE.mad:120`, `src/lib21/EXECUTE.mad:261` |
| Э72 | C | не найдено в rukava.be | — | 1 | `src/lib21/EXECUTE.mad:278` |

## Текстовые константы

Проверено 2 констант модуля `src/lib21/EXECUTE.mad`. Методика: `t6()` из `tools/extract_words.py` (6 бит/символ, 8 символов/слово), GOST-10859 (`gost10859.h`), ISO/ASCII (6 байт/слово). Для ASCII-Hollerith-литералов первичен TEXT-decode; для кириллических GOST-литералов — GOST-decode. Полная таблица с вердиктами — `logs/text_constants_audit.txt`.

| Константа | Декодирование (GOST / TEXT / ISO) | Источник | Вердикт |
|-----------|----------------------------------|----------|---------|
| `8HFRAG TPП` | GOST `ЖТБЗ0ФРЯ` / TEXT `FRAG TP_` / ISO `·(g·L?` | `src/lib21/EXECUTE.mad:190` | добавлено |
| `8HFRAG TPП` | GOST `ЖТБЗ0ФРЯ` / TEXT `FRAG TP_` / ISO `·(g·L?` | `src/lib21/EXECUTE.mad:507` | добавлено |

## Текстовые константы и кодировки

Второй проход аудита (2026-11-19): не расшифрованные ранее текстовые
константы в кодировках ИСО (ISO), ГОСТ, UPP/континуации (CONT).
Первичное чтение — текст литерала из листинга Дубны/dtran; 6-битные
GOST6/TEXT6 — альтернативная интерпретация машиного слова.
Методика и сверка: `docs/19-dtran-text-encodings.md`,
`tools/dtran_text.py --audit`. Полный лог — `logs/text_audit_lib21_2.txt`.

| Метка/литерал | Кодировка | Первичное чтение | Источник |
|---|---|---|---|
| `MIXLOA` | ISO | `MIXLOA` | `src/lib21/EXECUTE.mad:508` |
| `OVERLA` | ISO | `OVERLA` | `src/lib21/EXECUTE.mad:510` |
| `Y BAШ ` | ISO | `Y BAШ ` | `src/lib21/EXECUTE.mad:511` |
| `ПEPECO` | ISO | `ПEPECO` | `src/lib21/EXECUTE.mad:512` |
| `A HE X` | ISO | `A HE X` | `src/lib21/EXECUTE.mad:513` |
| `K COЙД` | ISO | `K COЙД` | `src/lib21/EXECUTE.mad:514` |
| `OШИБKA` | ISO | `OШИБKA` | `src/lib21/EXECUTE.mad:516` |
| `ПЛOXOЙ` | ISO | `ПЛOXOЙ` | `src/lib21/EXECUTE.mad:517` |
| `ПPИ CБ` | ISO | `ПPИ CБ` | `src/lib21/EXECUTE.mad:518` |
| `OC ДYБ  ` | TEXT(=6H) | `OC ДYБ  ` | `src/lib21/EXECUTE.mad:121` |
| `OVERLA  ` | TEXT(=6H) | `OVERLA  ` | `src/lib21/EXECUTE.mad:147` |
| `OC ДYБ  ` | TEXT(=6H) | `OC ДYБ  ` | `src/lib21/EXECUTE.mad:262` |

Добавлено декодирований: 12.
