# Перекрёстные ссылки модуля `BEMSH*` (библиотека 21)

**Источник:** `libra211.l21:4095-4245`; проверка — `disasm/lib21/BEMSH_.madlen`.

## 1. Объявления (NAME / ENTRY / SUBP / COMMON / TEXT / EQU)

| Метка (короткая) | Полное имя (POLN) | Тип | Комментарий |
|---|---|---|---|
| `BEMSH*` | `BEMSH_STAR` | NAME | `` |
| `ПAP/MЛ` | `ПAP_SLASHMЛ` | LC | `` |
| `MONOR` | `MONITOR_STAR` | SUBP | `.` |
| `БEMAP` | `БEMШ_SLASHПAP` | SUBP | `` |
| `C` | `C` | LC | `` |
| `EДЫP` | `EДЫP` | EQU | `14 000B` |
| `LДЫP` | `LДЫP` | EQU | `EДЫP-C` |
| `C1` | `C1` | LC | `LДЫP` |
| `READ*` | `READ_STAR` | SUBP | `` |
| `PRINT8` | `PRINT8` | SUBP | `` |
| `GIV/MT` | `GIV_SLASHMT` | SUBP | `` |
| `RM` | `RM_STAR` | LC | `4` |
| `KCNT` | `KCOUNT_STAR` | LC | `4` |
| `ENTRY*` | `ENTRY_TABLE` | LC | `` |
| `FLGEX*` | `FLAG_EX` | LC | `` |
| `FULISF` | `FULL_LIST_FLAG` | LC | `` |
| `NOLISF` | `NO_LIST_FLAG` | LC | `` |
| `BEGIN` | `BEGIN` | BSS | `.` |
| `RETMON` | `RETMON` | BSS | `` |
| `O/KEY` | `O_SLASHKEY` | BSS | `` |
| `SHIFT` | `SHIFT` | BSS | `1.` |

## 2. Переходы и вызовы

| Строка | Команда | Операнд (короткий) | Направление |
|---|---|---|---|
| 48 | UJ | `BEGIN` | внутренний → `BEGIN` |
| 50 | Z00 | `READ*` | внешний (объявлен SUBP/TEXT) → `READ*` |
| 52 | Z00 | `ENTRY*` | внутренний → `ENTRY*` |
| 54 | Z00 | `FLGEX*` | внутренний → `FLGEX*` |
| 56 | Z00 | `NOLISF` | внутренний → `NOLISF` |
| 58 | Z00 | `RETMON` | внутренний → `RETMON` |
| 60 | Z00 | `PRINT8` | внешний (объявлен SUBP/TEXT) → `PRINT8` |
| 62 | Z00 | `FULISF` | внутренний → `FULISF` |
| 79 | CALL | `GIV/MT` | внешний (объявлен SUBP/TEXT) → `GIV/MT` |
| 115 | UZA | `1100B` | внешний/абсолютный → `1100B` |
| 132 | UZA | `RETMEM` | внутренний → `RETMEM` |
| 137 | UJ | `MONITO` | внешний/абсолютный → `MONITO` |
| 139 | UJ | `O/KEY` | внутренний → `O/KEY` |

Всего переходов/вызовов: 13.

## 3. Связи с корнем ФОРЭКС и оверлеями

- Прямых ссылок на корень/оверлеи в теле не обнаружено; связь через LIBREFER/CATALOG.

## Экстракоды

Расшифровки по `rukava.be` (раздел 1.4). Подробности — `docs/lib21/04-extract-codes.md`.

| Код | Информационное слово | Расшифровка | Стр. | Применений | Места |
|-----|----------------------|-------------|------|------------|-------|
| Э57 | 4000 | не найдено в rukava.be | — | 1 | `src/lib21/BEMSH_.mad:201` |
| Э70 | TRCALL | не найдено в rukava.be | — | 1 | `src/lib21/BEMSH_.mad:163` |
| Э72 | COTK2+NT3 | не найдено в rukava.be | — | 1 | `src/lib21/BEMSH_.mad:203` |
| Э75 | CN1777 | не найдено в rukava.be | — | 1 | `src/lib21/BEMSH_.mad:165` |
