# Перекрёстные ссылки модуля `LFSCAN` (библиотека 21)

**Источник:** `disasm/lib21/LFSCAN.madlen`; проверка — `disasm/lib21/LFSCAN.madlen`.

## 1. Объявления (NAME / ENTRY / SUBP / COMMON / TEXT / EQU)

| Метка (короткая) | Полное имя (POLN) | Тип | Комментарий |
|---|---|---|---|
| `LFSCAN` | `LFSCAN` | NAME | ` NEW DTRAN` |
| `LFDIA` | `_STARLFDIAG_STAR` | LC | `3` |
| `FSSTA` | `F_SLASHSSTART` | SUBP | `` |
| `IPUTS` | `IPUTS` | SUBP | `` |
| `SCANER` | `SCANER` | SUBP | `` |
| `IGETS` | `IGETS` | SUBP | `` |
| `BCDWRT` | `BCDWRIT_STAR` | SUBP | `` |
| `IOCNT` | `IOCONT_STAR` | SUBP | `` |
| `FSRET` | `F_SLASHSRET` | SUBP | `` |
| `IOEND` | `IOEND_STAR` | SUBP | `` |
| `JSEART` | `JSEART` | SUBP | `` |
| `GAN1` | `GAN_SLASH1` | EQU | `*LFDIAG*+0` |
| `IOCTAL` | `IOCTAL` | SUBP | `` |
| `LFCREF` | `LFCREF` | SUBP | `` |
| `LFOPEN` | `LFOPEN` | SUBP | `` |
| `LFCLOS` | `LFCLOS` | SUBP | `` |
| `LFDELF` | `LFDELF` | SUBP | `` |
| `LFRIEN` | `LFRIEN` | SUBP | `` |
| `TAN` | `TEXT_AN` | TEXT | `8HAH` = "АН" (6-бит/GOST; была без метки) |
| `—` | `—` | BSS | `55` |
| `BUF527` | `_STAR0527B` | BSS | `3` |
| `BUF532` | `_STAR0532B` | BSS | `1` |
| `BUF533` | `_STAR0533B` | BSS | `11` |
| `BUF546` | `_STAR0546B` | BSS | `5` |
| `BUF553` | `_STAR0553B` | BSS | `20` |
| `BUF577` | `_STAR0577B` | BSS | `1` |

## 2. Переходы и вызовы

| Строка | Команда | Операнд (короткий) | Направление |
|---|---|---|---|
| 23 | UJ | `FSSTA` | внешний (объявлен SUBP/TEXT) → `FSSTA` |
| 29 | VJM | `IPUTS` | внешний (объявлен SUBP/TEXT) → `IPUTS` |
| 43 | VJM | `SCANER` | внешний (объявлен SUBP/TEXT) → `SCANER` |
| 45 | UJ | `WRA017` | внутренний → `WRA017` |
| 50 | U1A | `IRE024` | внутренний → `IRE024` |
| 56 | UJ | `IRE016` | внутренний → `IRE016` |
| 58 | UJ | `WRA026` | внутренний → `WRA026` |
| 63 | U1A | `IRE033` | внутренний → `IRE033` |
| 69 | UJ | `IRE025` | внутренний → `IRE025` |
| 81 | UZA | `IDX112` | внутренний → `IDX112` |
| 88 | UJ | `WRA046` | внутренний → `WRA046` |
| 93 | U1A | `IRE057` | внутренний → `IRE057` |
| 107 | UJ | `IPUTS` | внешний (объявлен SUBP/TEXT) → `IPUTS` |
| 109 | UJ | `WRA061` | внутренний → `WRA061` |
| 114 | U1A | `IDX103` | внутренний → `IDX103` |
| 131 | VJM | `IGETS` | внешний (объявлен SUBP/TEXT) → `IGETS` |
| 146 | UJ | `IPUTS` | внешний (объявлен SUBP/TEXT) → `IPUTS` |
| 151 | VJM | `BCDWRT` | внешний (объявлен SUBP/TEXT) → `BCDWRT` |
| 156 | VJM | `IOCNT` | внешний (объявлен SUBP/TEXT) → `IOCNT` |
| 158 | UJ | `IOEND` | внешний (объявлен SUBP/TEXT) → `IOEND` |
| 171 | VJM | `SCANER` | внешний (объявлен SUBP/TEXT) → `SCANER` |
| 181 | U1A | `IRE041` | внутренний → `IRE041` |
| 192 | VJM | `JSEART` | внешний (объявлен SUBP/TEXT) → `JSEART` |
| 195 | UZA | `IRE041` | внутренний → `IRE041` |
| 208 | VJM | `SCANER` | внешний (объявлен SUBP/TEXT) → `SCANER` |
| 224 | UZA | `IRE157` | внутренний → `IRE157` |
| 227 | UZA | `IRE157` | внутренний → `IRE157` |
| 230 | U1A | `IRE041` | внутренний → `IRE041` |
| 244 | UJ | `MOD165` | внутренний → `MOD165` |
| 245 | UJ | `IRE041` | внутренний → `IRE041` |
| 253 | UZA | `MOD177` | внутренний → `MOD177` |
| 256 | U1A | `MOD203` | внутренний → `MOD203` |
| 262 | VJM | `IOCTAL` | внешний (объявлен SUBP/TEXT) → `IOCTAL` |
| 277 | U1A | `IRE041` | внутренний → `IRE041` |
| 279 | UJ | `MOD212` | внутренний → `MOD212` |
| 280 | UJ | `IRE041` | внутренний → `IRE041` |
| 293 | UZA | `IRE041` | внутренний → `IRE041` |
| 297 | U1A | `IRE041` | внутренний → `IRE041` |
| 298 | UJ | `IRE277` | внутренний → `IRE277` |
| 304 | UZA | `MOD242` | внутренний → `MOD242` |
| 308 | UZA | `MOD242` | внутренний → `MOD242` |
| 321 | U1A | `IRE041` | внутренний → `IRE041` |
| 325 | U1A | `IRE041` | внутренний → `IRE041` |
| 326 | UJ | `IRE277` | внутренний → `IRE277` |
| 332 | UZA | `JMP255` | внутренний → `JMP255` |
| 336 | U1A | `IRE041` | внутренний → `IRE041` |
| 337 | UJ | `IRE277` | внутренний → `IRE277` |
| 339 | UJ | `MOD256` | внутренний → `MOD256` |
| 340 | UJ | `MOD267` | внутренний → `MOD267` |
| 359 | VJM | `JSEART` | внешний (объявлен SUBP/TEXT) → `JSEART` |
| 362 | UZA | `IRE041` | внутренний → `IRE041` |
| 365 | UZA | `IDX112` | внутренний → `IDX112` |
| 380 | UZA | `IRE041` | внутренний → `IRE041` |
| 382 | UJ | `WRA312` | внутренний → `WRA312` |
| 387 | U1A | `MOD334` | внутренний → `MOD334` |
| 400 | UZA | `MOD334` | внутренний → `MOD334` |
| 418 | UZA | `IRE041` | внутренний → `IRE041` |
| 419 | UJ | `IRE311` | внутренний → `IRE311` |
| 421 | UJ | `MOD334` | внутренний → `MOD334` |
| 422 | UJ | `IDX342` | внутренний → `IDX342` |
| 435 | VJM | `LFCREF` | внешний (объявлен SUBP/TEXT) → `LFCREF` |
| 437 | UJ | `IRE373` | внутренний → `IRE373` |
| 446 | VJM | `LFOPEN` | внешний (объявлен SUBP/TEXT) → `LFOPEN` |
| 448 | UJ | `IRE373` | внутренний → `IRE373` |
| 451 | VJM | `LFCLOS` | внешний (объявлен SUBP/TEXT) → `LFCLOS` |
| 453 | UJ | `IRE373` | внутренний → `IRE373` |
| 458 | VJM | `LFDELF` | внешний (объявлен SUBP/TEXT) → `LFDELF` |
| 460 | UJ | `IRE373` | внутренний → `IRE373` |
| 469 | VJM | `LFRIEN` | внешний (объявлен SUBP/TEXT) → `LFRIEN` |
| 473 | UZA | `JMP403` | внутренний → `JMP403` |
| 478 | VJM | `BCDWRT` | внешний (объявлен SUBP/TEXT) → `BCDWRT` |
| 483 | VJM | `IOCNT` | внешний (объявлен SUBP/TEXT) → `IOCNT` |
| 484 | VJM | `IOEND` | внешний (объявлен SUBP/TEXT) → `IOEND` |
| 485 | UJ | `FSRET` | внешний (объявлен SUBP/TEXT) → `FSRET` |

Всего переходов/вызовов: 74.

## 3. Связи с корнем ФОРЭКС и оверлеями

- Прямых ссылок на корень/оверлеи в теле не обнаружено; связь через LIBREFER/CATALOG.

## 4. Семантическое именование (этап 12)

- Авто-меток вида `W/L/D+NNNN` переименовано: **85**.
- TEXT-констант переименовано по содержимому: **1**.
- Смещений `LABEL+NNNB` → десятичное: **0**.
- Новые имена ≤6 символов, первые 6 уникальны в файле; полное имя — в `POLN:`.
- Таблица «было → стало» и исходные восьмеричные значения: `logs/labels_semantics_lib21_core.txt`.
