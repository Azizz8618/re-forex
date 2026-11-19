# 19. Вывод текстовых констант в dtran: `-D`, кодировки, сверка с аудитом

Дата: 2026-11-19. Инструмент: `tools/dtran_text.py`.
Лог: `logs/dtran_text_encodings.txt`. Указание пользователя:
«у dtran есть возможность выводить текстовые константы в разных кодировках,
смотри monitor80-re».

---

## 1. Как `-D` задаёт кодировки

Справка `dtran -h`:

```
-D file       read commands, one per line, case-insensitive. Text-encoding
              offsets are set only here:
                iso:<list>   gost:<list>   itm:<list>   text:<list>
                code:<list>  (entry points)   base:<decimal register>
              where <list> is comma-separated octal offsets or start-end ranges
```

- Числа в `<list>` — **восьмеричные** (`80` уже не число: `strtol(..., 8)`
  остановится на `8`; правильно `77`). Диапазон `237-266` включает обе границы.
- `-D` ** supersedes** `-R` и `-E`: базовый регистр сбрасывается в 0, файл
  entry-точек не читается (`dtran.cc:2021-2027`).
- Примеры из monitor80-re:
  - `permanent/newsyste.dtr`: `base:1,0`, `iso:117-121`, `gost:237-266`;
  - `permanent/print8.dtr`: `gost:30-34`;
  - `permanent/monitor%.dtr`: `text:12`;
  - `utility/overlay.dtr`: `base:7,0`, `text:332`, `iso:167-211`.
- Таблицы перекодировки: `monitor80-re/tools/encoding.cpp`, `encoding.h`,
  `gost10859.h` (GOST-10859, 6-битная графика).

### Ключевое ограничение (установлено в этой работе)

`iso:/gost:/itm:/text:` обрабатываются **только Pascal-бэкендами**:

| Бэкенд | Где читаются offsets | Что печатает |
|--------|----------------------|--------------|
| DMS (`-F dms`) | — | `prconst_dms()` → авто-эвристики `dms_is_iso()` / `is_likely_text()`; `,TEXT, 8H…` / `,ISO, 6H…` |
| Pascal-A (`-F pa`) | `gostoff` через `pa_is_gost()` | `,GOST, \|…\|` |
| Pascal-B (`-F pb`) | `gostoff/itmoff/isooff/textoff`, `format_map` | `,GOST, / ,ITM, / ,ISO, / ,TEXT, \|…\|` |

Поэтому на наших DMS-модулях результат `dtran` с `-D` и без `-D`
**побитово совпадает**. Демонстрация (лог, §2): `FOREX_.dms`, файл
`text:42-43` + `gost:30-41` + `iso:40` → `diff` пустой, авто-вывод
`,TEXT, 8HLO*SYN  `, `,TEXT, 8HLO*GEN  `, `,ISO, 6H20 -1+ .…`.

### Как получить все четыре прочтения одного слова

`tools/dtran_text.py` строит синтетический **Pascal-B** контейнер (одна
страница = 0o2000 слов):

- `memory[02000] = 0o0300000000000000` (`UJ 0 / UJ 0`) — останавливает
  линейный обход `find_code_offset()`, иначе все слова помечаются как код;
- слово `9` = 1 (одна страница), проверяемые слова — по адресам `02100+`;
- для каждой кодировки пишется `-D <enc>:2100-…` и запускается
  `dtran -F pb -D …`; из вывода берётся строка `/NNNN:,ENC, |…| octets`.

Контейнер — только «кодировочный стенд»; исходники и дампы не меняются.

```bash
python3 tools/dtran_text.py --word 0o5457126371560000      # 4 кодировки слова
python3 tools/dtran_text.py --module 'FOREX*'               # DMS: что печатает dtran
python3 tools/dtran_text.py --dms build/FOREX_.dms
python3 tools/dtran_text.py --words build/CORE_ROOT.words --offsets 0o45,0o46
python3 tools/dtran_text.py --audit                         # сверка контрольного набора
```

---

## 2. Демонстрация: `-D` на DMS не влияет

```
$ dtran -F dms /tmp/FOREX_.dms > plain.txt
$ dtran -F dms -D /tmp/FOREX_demo.dtr /tmp/FOREX_.dms > D.txt
$ diff -u plain.txt D.txt
(пусто)
 ,ISO, 6H20 -1+ . 062 060 040 055 061 053
 *0042B:,TEXT, 8HLO*SYN
 *0043B:,TEXT, 8HLO*GEN
```

То же на синтетическом DMS из `build/CORE_ROOT.words`
(`dtran_wrap.make_dms`) — `diff` пустой. Синтетический Pascal-B, напротив,
реагирует на `-D` (таблица ниже).

---

## 3. Таблица сверки: модуль → смещение → кодировка → dtran → наше

### 3.1. 6-битные TEXT-константы (`dtran -F dms`: `,TEXT, 8H…`)

Для них `-D text:` на стенде даёт то же, что авто-детект DMS.
«GOST dtran» ниже — что печатает `-D gost:` (байтовая интерпретация):
на 6-битном слове это **мусор**, и он не заменяет наш GOST(6→8).

| Модуль / строка | offset / слово | dtran `-D text:` | наше TEXT (до/после) | dtran `-D gost:` | наш GOST(6→8) |
|---|---|---|---|---|---|
| FOREX_CORE.mad:365 | 0o5457126371560000 | `LO*SYN  ` | `LO*SYN  ` OK | `_262_362_263_346_3400` | `МП+УЩО00` |
| FOREX_CORE.mad:370 | 0o5457124745560000 | `LO*GEN  ` | `LO*GEN  ` OK | `_262_362_247_226_3400` | `МП+ЗЕО00` |
| FOREX_CORE.mad:390 | 0o4657624570120000 | `FOREX*  ` | `FOREX*  ` OK | `_232_374_245_340_2400` | `ЖПТЕШ+00` |
| FOREX_CORE.mad:520 | 0o4556646271120000 | `ENTRY*  ` | `ENTRY*  ` OK | `_226_355Т_344_2400` | `ЕОФТЩ+00` |
| FOREX_CORE.mad:545 | 0o4441644160621200 | `DATAPR* ` | `DATAPR* ` OK | `_222<Б_303В_200` | `ДБФБРТ+0` |
| FOREX_CORE.mad:550 | 0o6441531760470000 | `TAK/PG  ` | `TAK/PG  ` OK | `_322\`_317_302_1600` | `ФБЛ РЗ00` |
| FOREX_CORE.mad:555 | 0o4751661760470000 | `GIV/PG  ` | `GIV/PG  ` OK | `_236_235_217_302_1600` | `ЗЙЦ РЗ00` |
| FOREX_CORE.mad:560 | 0o5743646444454300 | `OCTTDEC ` | `OCTTDEC ` OK | `_276ЮФ_222\|_300` | `ПГФФДЕГ0` |
| FOREX_CORE.mad:565 | 0o4657624570000000 | `FOREX   ` | `FOREX   ` OK | `_232_374_245_34000` | `ЖПТЕШ000` |
| FOREX_CORE.mad:570 | 0o4357566364000000 | `CONST   ` | `CONST   ` OK | `_216_373_263_32000` | `ГПОУФ000` |
| FOREX_CORE.mad:575 | 0o4357554561000000 | `COMEQ   ` | `COMEQ   ` OK | `_216_373_145_30400` | `ГПНЕС000` |
| FOREX_CORE.mad:580 | 0o5760626462000000 | `OPRTR   ` | `OPRTR   ` OK | `_277/_264_31000` | `ПРТФТ000` |
| FOREX_CORE.mad:585 | 0o5457414441564757 | `LOADANGO` | `LOADANGO` OK | `_262_370_144_206_351_357` | `МПБДБОЗП` |
| lib21/XREF.mad:1053 | `8H*INPUT*` | `*INPUT* ` | `*INPUT* ` OK | — | `+ЙОРХФ+0` |
| lib21/XREF.mad:1054 | `8H   INPUT` | `   INPUT` | `INPUT   ` → **`   INPUT`** | — | `ЙОРХФ000` → **`000ЙОРХФ`** |
| lib21/XREF.mad:1055 | `8H*OUTPUT*` | `*OUTPUT*` | `*OUTPUT*` OK | — | `+ПХФРХФ+` |
| lib21/XREF.mad:1056 | `8H  OUTPUT` | `  OUTPUT` | `OUTPUT  ` → **`  OUTPUT`** | — | `ПХФРХФ00` → **`00ПХФРХФ`** |
| F77LIBR `4HABCD` | 0o4142434400000000 | `ABCD    ` | `ABCD    ` OK | `_206И_344000` | `ABCD0000` |

### 3.2. Месяцы DATAPR — настоящие 8-битные GOST-константы

Источник `besmmons/system1.txt:7712-7731`: `,GOST,6HФEBMAP` и т.п.
Здесь авторитетен `-D gost:`; `-D text:` на тех же словах даёт мусор.

| Модуль / строка | смещение (S5) → слово | `-D gost:` | `-D text:` | наше GOST | вердикт |
|---|---|---|---|---|---|
| FOREX_RUNTIME.mad:105 | 7722 → 0o1502244213020060 | `ФЕВМАР` | `ЯБ4BЙБ P` | `ФЕВМАР  ` | подтверждено; добавлено уточнение |
| FOREX_RUNTIME.mad:106 | 7731 → 0o1102245200000000 | `ДЕК000` | `)Б4J    ` | `ДЕК     ` | подтверждено; добавлено уточнение |
| FOREX_RUNTIME.mad:107 | 7724 → 0o1203645512036453 | `ИЮНИЮЛ` | `*ЦTM*ЦTK` | `ИЮНИЮЛ  ` | подтверждено; добавлено уточнение |
| FOREX_DECODER_DISASM.mad:91 | 7714 → 0o1002746013020076 | `АПРМАЯ` | `(БЭPЙБ Ч` | `АПРМАЯ  ` | подтверждено |
| FOREX_RUNTIME.mad:103 | 7721 → `6H'231'  ЯHB` | `'231'  ЯНВ` | — | `''231'  Я'` / `НВ` | подтверждено; добавлено уточнение |

Вывод: в комментариях сохранены GOST-строки как **первичное** чтение
(именно так константы объявлены в исходнике Дубны); добавлена пометка, что
6-битный `TEXT` в этих строках — альтернативная интерпретация байт,
**не** `dtran -D text`.

---

## 4. Что исправлено

1. `src/lib21/XREF.mad:1054,1056` — у двух TEXT-имён секций ведущие пробелы
   были перенесены в конец (`INPUT   ` вместо `   INPUT`, `OUTPUT  ` вместо
   `  OUTPUT`); GOST(6→8)-строки исправлены соответственно. Причина: dtran
   печатает `8H   INPUT` / `8H  OUTPUT`, а машинные слова
   `0o0000005156606564` / `0o0000576564606564` имеют нулевые **старшие**
   6-битные группы.
2. `src/FOREX_RUNTIME.mad:103,105,106,107` — добавлены явные пометки
   `dtran -D gost:` и «приоритет GOST (8 бит/символ)» для месяцев DATAPR.
3. `tools/dtran_text.py` — новый инструмент (стенд `-D` + `--audit`).
4. `tools/extract_codes.py` — добавлен комментарий о границах применимости
   `-D` и о том, что наш `GOST '…'` — это GOST(6→8), а не `dtran -D gost`.
5. `tests/check-extract-codes.sh` — вызов `tools/dtran_text.py --audit`
   и проверка, что leading-space константы XREF не регрессировали.

---

## 5. Проверки

```bash
python3 tools/dtran_text.py --audit
python3 tests/check-source-words.py
bash tests/check-extract-codes.sh
bash tests/check-label-semantics.sh
```

`--audit`: 18 TEXT-констант, расхождений 0; 4 GOST-месяца, расхождений 0.

---

## 6. Выводы

1. `-D text:/gost:/iso:/itm:` в dtran — **Pascal-only**; на DMS (`-F dms`)
   он не влияет. Проверено `diff` на `FOREX_.dms` и синтетическом DMS из
   `CORE_ROOT.words`.
2. Для DMS-модулей авторитетное чтениеTEXT-констант — авто-вывод
   `,TEXT, 8H…`; он совпадает с нашими аннотациями для всех 13 TEXT-имён
   `FOREX_CORE` и для `8H*INPUT*` / `8H*OUTPUT*` в `XREF.mad`.
3. наш secondary `GOST '…'` — 8 шестибитных групп по `gost10859.h`;
   `dtran -D gost:` читает 6 восьмибитных байт. Это разные форматы, и на
   6-битных TEXT-словах dtran даёт «мусор» — комментарии поэтому не были
   заменены мусором.
4. Месяцы DATAPR объявлены в исходнике как `,GOST,` (8 бит/символ);
   `dtran -D gost:` их подтверждает. Добавлены уточнения в комментарии.
5. Две реальные ошибки в `XREF.mad` исправлены; регрессия закрыта тестом.
