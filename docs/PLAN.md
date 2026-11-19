# План дизассемблирования компилятора ФОРЭКС ИПМ АН СССР

**Статус:** план готов к выполнению (разведка этапа 1 проведена субагентами 19.11.2026).
**Цель:** получить аннотированные исходники оверлеев `LO*SYN` / `LO*GEN`
компилятора ФОРЭКС с побайтовой проверкой и эталонным прогоном.
**Репозиторий:** `git@github.com:Azizz8618/re-forex.git` (сейчас пуст; рабочая копия
`/tmp/.private/azizz/opencode/re-forex`).

---

## 1. Установленные факты (не пересматривать без доказательств)

| Факт | Источник |
|---|---|
| Корень компилятора — модуль `FOREX*`, исходник на МАДЛЕН/БЕМШ | `besm6.github.io/sources/dubna/besml21/libra211.l21:15448-15528` |
| Оверлеи `LO*SYN`, `LO*GEN` грузятся `LOADANGO` по одному адресу `0o22654` | `libra211.l21:15485-15489`; `dispak/tests/forex/output.txt:33,59` |
| Внешние подпрограммы корня: `DATAPR*`, `TAK/PG`, `GIV/PG`, `OCTTDEC`, `FOREX`, `CONST`, `COMEQ`, `OPRTR`, `ПP`, `LOADANGO` | `libra211.l21:15456-15464`; `expect_library21.txt:196-205` |
| `LO*SYN`/`LO*GEN` — **не отдельные DMS-модули**, а `TEXT`-константы (имена) в корне; тела лежат на ленте `monsys.9`, зоны 0120 и 0137 | разведка этапа 1; в `librar.12/37` имён нет |
| Баннер `OVERLAY OT 27/04/87 FOREX 412` (слово `0o201762`, зона 64) — **сервисное сообщение монитора, не начало кода** | разведка этапа 1 (корректирует более раннюю гипотезу «код с 202000») |
| Таблицы `STAR*/FT*/IO*/...` в `output.txt:147-183` — MONITOR-80 + рантайм, **не компилятор** | идентичны в `dispak/tests/fortran-dubna/output.txt:272-310` |
| Три сборки: `2.02 от 15.07.80` (dispak), `4.13 от 11.09.85` (Dubna), `FOREX 412` (monsys.9) | `output.txt:36`; `expect_forex.txt:28`; `monsys.9:0o201762` |

## 2. Карта носителя (этап 1 фактически выполнен)

Формат: слово 48 бит = **6 байт big-endian**; зона = 1024 слова = 6144 байт;
`byte = 6*(1024*Z + W)`. Все смещения в `besm6tape.py` — восьмеричные.

| Объект | Зона | Слово | Байт |
|---|---|---|---|
| Каталог имён модулей (`INITFTN`, `FOREX*83`, `LO*SYN`, `LO*GEN`, `PASCAL*` …) | 64 / 0100 | `0o200000-0o200017` | 393216–393420 |
| ASCII-заголовок `FOREX 412` | 64 / 0100 | `0o201762-0o201776` | 399276–399366 |
| **Модуль `LO*SYN`**: маркер + имя | 80 / 0120 | `0o241500`, `0o241501` | **496512**, 496518 |
| **Модуль `LO*GEN`**: маркер + имя | 95 / 0137 | `0o277500`, `0o277501` | **588672**, 588678 |
| Три восстановленных слова (патч 18 байт) | 95 / 0137 | `0o277775-0o277777` | 589806–589823 (`0x8FFEE-0x8FFFF`) |

Сигнатуры поиска:
- маркер начала модуля `000000200003`;
- MADLEN `TEXT` `LO*SYN` = `0o5457126371560000`, `LO*GEN` = `0o5457124745560000`;
- ASCII `OVERLA` = `0o2365310524446101` (сервисные сообщения);
- имя в каталоге `FOREX*83` = `8H` словом `0o4657624570123023`.

Три кодировки текста в образе:
1. **ASCII «Text» монитора** — 6 символов/слово (`--mode ascii`);
2. **MADLEN `TEXT`** — 6 бит/символ, **8 символов/слово**, код = `ASCII − 0x20`
   (имена `LO*SYN/LO*GEN` записаны именно так);
3. **GOST-10859** — таблица `dubna/gost10859.h`; `--mode gost` в `besm6tape.py`
   даёт сдвинутую расшифровку, пользоваться таблицей напрямую.

Декодер MADLEN `TEXT`:
```python
def t6(x):
    out = ''
    for half in ((x >> 24) & 0xffffff, x & 0xffffff):
        for sh in (18, 12, 6, 0):
            c = ((half >> sh) & 0x3f) + 0x20
            out += chr(c) if 32 <= c < 127 else '?'
    return out
```

## 3. Разбиение на этапы

| # | Этап | Время | Вход → действие → выход | Критерий готовности |
|---|---|---|---|---|
| 0 | Организация | 20 мин | Создать `docs/reference/build/disasm/src/verify`, зафиксировать SHA256 `monsys.9` (`e26a2036…1118b`), версии инструментов → `docs/00-charter.md`, `manifest.sha256` | sums и версии записаны |
| 1 | Разведка | ✅ завершён | Каталог зон 64/80/95, сигнатуры, декодер → `docs/PLAN.md` §2 (этот файл) | известны границы обоих оверлеев |
| 2 | Сырой дамп | ✅ завершён | `build/LO_SYN.words`, `build/LO_GEN.words` (6 Б/слово) | `tests/verify-dumps.sh` OK |
| 3 | Границы и символы | ✅ завершён | `docs/03-symbols.md` 37/37 + 14/14; `include/catalog.md`; `include/FOREX_ROOT.mad` | все entry/внешние имена/COMMON найдены |
| 4a | Дизассембл `LO*SYN` | ✅ завершён | `disasm/LO_SYN.dtran.madlen` (2055) + `LO_SYN.bemsh.lst` (1024) | dtran + полный bemsh-листинг |
| 4b | Дизассембл `LO*GEN` | ✅ завершён | `disasm/LO_GEN.dtran.madlen` (1905) + `LO_GEN.bemsh.lst` (1024) | то же |
| 5a | Реконструкция `LO*SYN` | ✅ завершён | `src/LO_SYN.mad` 3122 строки, 1024/1024 слов | `check-word-coverage`, `check-annotations` OK |
| 5b | Реконструкция `LO*GEN` | ✅ завершён | `src/LO_GEN.mad` 3109 строк, 1024/1024 слов | то же |
| 6 | Сборка и сверка | 60 мин | обратная сборка + `verify_dtran.pl` + прогон `forex.b6` → `verify/*.log` | побайтовое совпадение + sha256 эталонного `output.txt` |
| 7 | Публикация | ✅ сделано | README, индекс, STATUS, перенос в GitHub | коммиты `c4bd4e8`, `90618d5`, `9619d54` |
| 8 | Ядро компилятора | ✅ завершён | корень `0o510300..0o510437` восстановлен; тела 5 SUBP отсутствуют на носителях (доказано) — `docs/06-core-modules.md` |
| 9 | Рантайм | ✅ завершён | `src/FOREX_RUNTIME.mad`: `FORMAT`, `FORTLIBR`, `DATAPR*`, `OCTTDEC` |
| 10 | Карта адресов | ✅ завершён | `docs/06-address-map.md`: модель `0o22654`, подтверждённые символы, топ-20 |
| 11 | FOREX3\* | ✅ закрыт | `docs/08-forex3.md`: deck-параметр, отдельная ветка не найдена на 20 образах |
| 12 | Метки и литералы | ✅ завершён | осмысленные имена, все литералы в `EQU`, глобальный xref — `docs/09-crossrefs.md`, `docs/10-naming-conventions.md` |
| 13 | Библиотека 21 | ✅ завершён | 358 dtran-листингов, 45 аннотаций, структура и глобальный xref — `docs/lib21/` |
| 14 | Экстракоды | ✅ завершён | `tools/extract_codes.py`, 612 комментариев, `docs/lib21/04-extract-codes.md` |
| 15 | Семантика имён | ✅ завершён | 0 авто-меток/нумерованных TEXT, десятичные смещения, `tests/check-label-semantics.sh` |

**Параллелизм:** 4a ‖ 4b и 5a ‖ 5b — независимые ветки (разные оверлеи в разные зоны).
Этап 3 можно начинать до полного дампа (DTRAN корня — отдельный deck).

## 4. Команды этапа 2 (команды этапа 1 уже выполнены разведчиком)

```bash
TAPE=/home/azizz/Yandex.Disk/besm6-new/besm6.net/tapes/monsys.9
TOOL=/home/azizz/Yandex.Disk/besm6-new/besm6.net/tools/besm6tape.py

python3 "$TOOL" dis "$TAPE" --start 0o241500 --count 80   # LO*SYN: маркер, имя, заголовок
python3 "$TOOL" dis "$TAPE" --start 0o277500 --count 80   # LO*GEN
python3 "$TOOL" dis "$TAPE" --start 0o277770 --count 8    # 3 восстановленных слова

# после того как определена длина модуля из дескриптора (поле не расшифровано — этап 3):
SYN_START=$((8#241500)); SYN_LEN=$((8#2000))
dd if="$TAPE" of=build/LO_SYN.words bs=6 skip=$SYN_START count=$SYN_LEN status=none
GEN_START=$((8#277500)); GEN_LEN=$((8#2000))
dd if="$TAPE" of=build/LO_GEN.words bs=6 skip=$GEN_START count=$GEN_LEN status=none

disbesm6 -a0 -e0 build/LO_SYN.words > disasm/LO_SYN.lst
disbesm6 -a0 -e0 build/LO_GEN.words > disasm/LO_GEN.lst
python3 "$TOOL" dis "$TAPE" --start 0o241500 --count 200 --bemsh > disasm/LO_SYN_bemsh.txt
```

`SYN_LEN/GEN_LEN = 0o2000` — **временная оценка** (зона 1024 слова); точную длину
взять из дескрипторного слова после имени (кандидаты: `0o5010324211330264` /
`0o5017723772530264`; расшифровка — задача этапа 3).

## 5. Команды этапа 3 (DTRAN корня в dispak)

```
шифр 419999 зс5^
лен 41(2048)^
eeв1а3
*name Dtran
*perso: 411350, cont
*call dtran(forex*,const,comeq,oprtr,пp)
*assem
*read: 1
*end file
```
```bash
cd ~/Yandex.Disk/dispak/tests/dtran
~/Yandex.Disk/dispak/build/dispak/dispak dtran.b6 > /tmp/dtran_run.txt
```
Для Дубны: `*library:23` + `*call dtran(stop*)`; эталон
`besm6-new/dubna/tests/expect_dtran.txt`.

## 6. Чек-лист символов (этап 3) — 37 обязательных + 14 ожидаемых

Источники: `S1 = libra211.l21:15448-15528`, `S3 = expect_library21.txt:182,196-205,376,398,945-1324,1533-1540`.

- **ENTRY `FOREX*`:** `INITFOR*`, `LOREX`, `RMON`, `STOP/`.
- **SUBP/внешние:** `DATAPR*`(E), `TAK/PG`, `GIV/PG`, `OCTTDEC`(E), `FOREX`, `CONST`, `COMEQ`, `OPRTR`, `ПP`, `LOADANGO`(E).
- **COMMON (ноль расхождений):** `NL 02048 *A*`, `L 00040 ENTRY*`, `L 00005 *DUMON*`, `L 00001 A/I0 / FLGEX* / NOLISFL* / FULISFL* / CHECKFL*`.
- **TEXT/GOST:** `LO*SYN`, `LO*GEN`, `ВРЕМЯ-`, `ОШ. ТРАНСЛЯТОРА`, `=R100.0`, литералы `=6H'…'`.
- **Ожидаемо (версионно):** баннеры `2.02 / 4.13 / 412`, адреса `01770 / 0o22654`, `КОМАНД 00067 / КОНСТАНТ 00010`, `ПАМЯТЬ 00150`, `ДЛИНА MAIN 00247`, простые числа 2…97.

Каждая найденная строка листинга помечается `; Sx:nnnn`. Три версии — разные сборки, хранить все эталоны.

## 7. Критерии приёмки и проверки

1. Entry coverage; 2. External resolution; 3. COMMON geometry; 4. TEXT/GOST decode;
5. **Round-trip assembly** (`asm.pl` + `verify_dtran.pl`, `cmp -b` → 0 различий) — главный;
6. `forex.b6` → `output.txt` с совпадающим sha256; 7. LIBREFER diff; 8. происхождение символа.

Независимые проверки:
- **V1** `ctest -R '^forex$'` + sha256 `output.txt`;
- **V2** LIBREFER diff с `expect_library21.txt`;
- **V3** `verify_dtran.pl --gold-file=… --silver-file=… -v`;
- **V4** `whatis monsys` → `OVERLAY … FOREX 412`;
- **V5** сверка баннеров трёх сборок;
- **V6** наложение дизассембла на `libra211.l21`.

## 8. Ловушки

1. 6 байт/слово, big-endian, кратность 6; `dd bs=6`.
2. 6-битная GOST: `FOREX` в DTRAN — это GOST-символы; `strings` ловит только ASCII.
3. Слово = две 24-битные половины `[ИР 3][КОД 6][АДР 15]`.
4. Оверлеи грузятся в один адрес → один статический дамп = только последний; нужны два дампа/трасса `LOADANGO`.
5. Версии не смешивать; баннер `FOREX 412` — не код оверлея.
6. 18 байт `monsys.9` уже восстановлены — не трогать (SHA256 проверяется).
7. Смещения `besm6tape.py` восьмеричные; `dd` → `$((8#…))`.
8. `besmtool dump` только с `--start/--length/--to-file`; `--disk/--zone` устарели.
9. `dubna`/`besm6.net` симуляторы не собраны — дамп памяти только через `dispak`.
10. Не расшифрованы дескрипторные слова каталога (длина оверлеев) — задача этапа 3.

## 9. Структура репозитория

```
re-forex/
├── README.md, docs/{PLAN,SYMBOLS,ACCEPTANCE,SOURCES,VERSIONS}.md
├── reference/   libra211.forex.inc, expect_library21.txt, output.gold.txt,
│                expect_forex.txt, expect_whatis_monsys.txt, forex.b6 (read-only)
├── build/       LO_SYN.words, LO_GEN.words
├── disasm/      LO_SYN.lst, LO_GEN.lst, *_bemsh.txt
├── src/         LO_SYN.be, LO_GEN.be
├── tools/       extract_words.py (t6 decoder), verify scripts
├── verify/      run-forex.sh, check-librefer.sh, roundtrip.sh, check-banner.sh
└── checklist/   STATUS.md, PROVENANCE.md
```

## 10. Распределение по субагентам

**Выполнено (этот заход):** разведка носителя (зоны/сигнатуры/декодер), инструменты и команды, чек-лист символов и критерии приёмки — 4 субагента, результаты включены в план.

**Следующий заход (по готовности):**
- субагент A → этап 4a (`LO*SYN`: дамп + дизассембл + карта вызовов);
- субагент B → этап 4b (`LO*GEN`: то же);
- субагент C → этап 3 (DTRAN корня + дешифровка дескрипторов каталога, уточнение длин оверлеев);
- после их отчётов — этап 5 (параллельно по модулям) и 6 (сверка).
