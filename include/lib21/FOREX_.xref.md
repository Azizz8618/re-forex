# Перекрёстные ссылки модуля `FOREX*` (библиотека 21)

**Источник:** `libra211.l21:15448-15528`; проверка — `disasm/lib21/FOREX_.madlen`.

## 1. Объявления (NAME / ENTRY / SUBP / COMMON / TEXT / EQU)

| Метка (короткая) | Полное имя (POLN) | Тип | Комментарий |
|---|---|---|---|
| `FOREX*` | `FOREX_STAR` | NAME | `` |
| `ENTRY*` | `ENTRY_TABLE` | LC | `50B.` |
| `FLGEX*` | `FLAG_EX` | LC | `1.` |
| `NOLISF` | `NO_LIST_FLAG` | LC | `1.` |
| `FULISF` | `FULL_LIST_FLAG` | LC | `1.` |
| `CHECKF` | `CHECK_FLAG` | LC | `1.` |
| `*DUMON` | `DUMMY_COMMON` | LC | `5.` |
| `A/I0` | `ACCUM_INIT` | LC | `1.` |
| `DATAPR` | `DATE_PRINT` | SUBP | `.` |
| `PAGETK` | `PAGE_TAKE` | SUBP | `.` |
| `PAGEGV` | `PAGE_GIVE` | SUBP | `.` |
| `OCTTDE` | `OCT_TO_DEC` | SUBP | `.` |
| `FOREX` | `FOREX` | SUBP | `` |
| `CONST` | `CONST` | SUBP | `` |
| `COMEQ` | `COMEQ` | SUBP | `` |
| `OPRTR` | `OPRTR` | SUBP | `.` |
| `ПP` | `ПP` | SUBP | `` |
| `*A*` | `BUFFER_A` | LC | `4000B.` |
| `INITFO` | `INIT_FOREX` | ENTRY | `.` |
| `LOREX` | `LOREX` | ENTRY | `.` |
| `RMON` | `RMON` | ENTRY | `.` |
| `ERRTRL` | `STOP_TRANSLATOR` | ENTRY | `.` |
| `TSYN` | `TEXT_OVERLAY_SYN` | TEXT | `8HLO*SYN` = "LO*SYN" (было `LO*SYN`) |
| `TGEN` | `TEXT_OVERLAY_GEN` | TEXT | `8HLO*GEN` = "LO*GEN" (было `LO*GEN`) |
| `RET` | `RET` | BSS | `1.` |

## 2. Переходы и вызовы

| Строка | Команда | Операнд (короткий) | Направление |
|---|---|---|---|
| 31 | UIA | `NPR` | внутренний → `NPR` |
| 32 | CALL | `DATAPR` | внешний (объявлен SUBP/TEXT) → `DATAPR` |
| 37 | CALL | `PAGEGV` | внешний (объявлен SUBP/TEXT) → `PAGEGV` |
| 40 | CALL | `LOADAN` | внешний → `LOADAN` (LINK/имя корня ФОРЭКС) |
| 42 | CALL | `LOADAN` | внешний → `LOADAN` (LINK/имя корня ФОРЭКС) |
| 51 | CALL | `OCTTDE` | внешний (объявлен SUBP/TEXT) → `OCTTDE` |
| 63 | UJ | `PAGETK` | внешний (объявлен SUBP/TEXT) → `PAGETK` |
| 68 | UJ | `PRIN` | внутренний → `PRIN` |

Всего переходов/вызовов: 8.

## 3. Связи с корнем ФОРЭКС и оверлеями

- `FOREX*` — корневой модуль: упоминается в теле модуля.
- `TSYN` (`LO*SYN`) — оверлей синтаксиса: упоминается в теле модуля.
- `TGEN` (`LO*GEN`) — оверлей генерации: упоминается в теле модуля.
- `DATAPR*` — печать даты: упоминается в теле модуля.
- `GIV/PG` — выдача страницы: упоминается в теле модуля.
- `TAK/PG` — взятие страницы: упоминается в теле модуля.
- `OCTTDEC` — OCT→DEC: упоминается в теле модуля.
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
| Э57 | 6 | не найдено в rukava.be | — | 2 | `src/lib21/FOREX_.mad:58`, `src/lib21/FOREX_.mad:83` |
| Э64 | INF | не найдено в rukava.be | — | 1 | `src/lib21/FOREX_.mad:95` |
