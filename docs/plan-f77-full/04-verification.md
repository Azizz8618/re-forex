# 04 — Система верификации полной реализации FORTRAN 77 (проект)

Дата: 19.11.2026. Версия изделия: **FOREX 5.00 / 19.11.2026 (re-forex)**.
Системный баннер `ВЕРСИЯ 2.02 ОТ 15.07.80` печатается внешним системным
ФОРЭКСОМ диска 2048 и **не является** версией изделия; он часть эталонного
вывода и в gold-сравнении не тронут (`docs/16-glissade-run.md` §6).

Статус: **проект**. Настоящий документ — единственный выходной артефакт
субагента; `src/`, `include/`, `reference/`, `tests/` не изменялись. Все
перечисленные ниже новые пути — предложение для этапа реализации.

## 0. Входные артефакты (прочитаны)

| Источник | Что дал |
|---|---|
| `tests/run-f77-suite.sh` | готовый контур: PERSO `0o2300`, `ZONE_BASE=1216`, нормализация даты, `extract_result()`, `compare_numbers()` с допуском `max(1e-6,1e-5·max)`, генерация `*FTN`-деки, `FATAL`-фильтр, `ОЖИДАЕТСЯ`-ветка |
| `tests/f77/suite/` (8 кейсов) | 8 gold-пар `*.b6`/`*.gold` + `listio.f77` + `cross-ftn.txt` (3 случая) |
| `docs/plan-f77/12-acceptance.md` | 8/8 gold, 3/3 cross, 0 расхождений; 6 известных границ подмножества |
| `tests/plan-f77/probe.sh`, `logs/plan_f77_probes.txt` | 15 проб: 10 OK / 5 FAIL, точные диагностики отказов |
| `tests/plan-f77/e1/**` | 5 экспериментов (I/O-юниты, вставка PERSO, `*call` к Fortran-объекту, DP/COMPLEX, строки); float/строковые контрольные значения |
| `docs/plan-f77/01-gap-analysis.md` | **стандарт-матрица**: 21 подтверждённая позиция §1, 5 `NO` §2.1, 3 `~`, 17 `?` §2.2–2.3, приоритеты P0–P3 |
| `docs/plan-f77/04-assembler-path.md` §5–6 | 16 регрессионных сценариев + 4 новых F77-теста = **20/20 gate**; sliding-window score ≥0.95 |
| `docs/plan-f77/05-decision.md` §5 | 5 уровней проверяемости (SHA → opcode → метки → gold → кросс) |
| `docs/16-glissade-run.md` | 14/14 строк, конфликт `OCTTDEC`→`OCTTDE*`, `%VERSION` баннер 2.02 |
| `tests/run-f77-runtime.sh` | сборка `F77LIB` → `*to perso:602310` (зона `0o2310`), проверка каталога, байтовая неизменность зоны `0o2300` |

---

## 1. Тестовая пирамида

Пять уровней `(a)–(e)` плюс обязательный gate. Каждый уровень имеет свой
артефакт в `logs/` и свой критерий; переход к следующему уровню — только при
прохождении предыдущего.

| Уровень | Назначение | Единица измерения | Объём | Критерий | Лог |
|---|---|---|---:|---|---|
| **L0 (a)** unit-пробы каждой F77-конструкции | компилируемость + базовая семантика одной конструкции | конструкция из стандарт-матрицы | **N = 32** | `32/32 OK`, `ERR/ОШИБКА/НЕДОПУСТИМ/АТТ/ТИП ОП-ДА = 0` | `logs/f77_full_matrix.txt` |
| **L1 (b)** gold-пары program/output | побайтовое совпадение блока результата после нормализации | пара `*.b6` + `*.gold` | **M = 32** | `32/32 gold`, `0 FAIL` | `logs/f77_full_gold.txt` |
| **L2 (c)** кросс-компиляция | одна программа → `*FTN` (Fortran-ГДР, диск 2048) и `*FORTRAN` (Дубна); сравнение чисел | пара «ФОРЭКС ↔ эталонный компилятор» | **K = 8** (4×2) | `8/8`, допуск §1.3 | `logs/f77_cross_ftn.txt`, `logs/f77_cross_fortran.txt` |
| **L3 (d)** реальные программы | сквозная работоспособность на настоящих F77-исходниках | программа | **R = 4** | `4/4`, контрольные числа/строки | `logs/f77_full_real.txt` |
| **L4 (e)** negative cases | ожидаемые отказы и несовпадение типов не должны маскироваться под успех | случай | **NE = 9** | `9/9` «отказ обнаружен и классифицирован» | `logs/f77_full_negative.txt` |
| **Gate G** регрессия | обратная совместимость | сценарий | **20/20** | rc=0 обязателен | `logs/f77_full_gate.txt` |

### 1.1. L0 — unit-пробы

15 существующих проб `tests/plan-f77/probe.sh` сохраняются как есть и
дополняются до 32 слотов стандарт-матрицы (§2). Классификация — строго по
`FATAL`-фильтру сценария E5 (`БЫЛИ ОШИБКИ|НЕДОПУСТИМ|ОШИБКА|ERR n|ОШ. ТРАНСЛЯТОРА|
ТИП ОП-ДА|ОТСУТСТВУЕТ|ИСПОРЧЕН|АТТ `) + признак `КОНЕЦ ЗАДАЧИ`. «Просто
отсутствие ошибки» успехом не считается: требуется ещё и непустой блок результата.

### 1.2. L1 — gold-пары

Формат тот же, что в E5: сравниваются только непустые строки перед `КОНЕЦ ЗАДАЧИ`
(`extract_result` из `run-f77-suite.sh:57-73`), дата `DD.DD.DD → ##.##.##`.
8 пар берутся готовыми из `tests/f77/suite/`, 18 создаются заново по слоту
матрицы. Одна конструкция = одна пара. Баннер 2.02 в блок результата не входит
и потому не нормализуется; при кросс-сравнении (L2) баннеры обеих систем
заменяются на токен `<BANNER>` (см. §3.4).

### 1.3. L2 — кросс с допуском

| Компилятор | Карта в деке | Носитель | Допуск | Доп. критерий |
|---|---|---|---|---|
| `*FTN` (Fortran-ГДР) | `*system`, `*full list`, `*ftn`, `*name F<case>` | диск 2048 | `max(1e-6, 1e-5·max(\|x\|,\|y\|))` — как в E5 | совпадение количества чисел |
| `*FORTRAN` (Дубна) | `*system`, `*full list`, `*fortran`, `*name D<case>` | диск 2048 | `max(1e-4, 1e-4·max(\|x\|,\|y\|))` (иной диалект/форматирование) | sliding window `W=3`, `score ≥ 0.95`, первая и последняя строки совпали (`04-assembler-path.md` §5.4) |

`D`/`d`-экспоненты нормализуются в `E` перед сравнением; `compare_numbers()`
уже делает это в E5. Набор кросс-кейсов: `X01 base`, `X02 do2d`,
`X03 intrinsics_ext`, `X04 dpcomplex` → 4×2 = **K = 8**. `X01–X03` с `*FTN`
уже проходятся (3/3, `logs/f77_cross_ftn.txt`); добавляются `X04` и четыре
прогона `*FORTRAN`. Если `*FORTRAN` в среде недоступен — уровень помечается
`SKIP (нет эталона)` и **не блокирует** приёмку; базовый порог тогда `4/4 *FTN`.

### 1.4. L3 — реальные программы

| Программа | Источник | Контроль | Порог |
|---|---|---|---|
| Глиссада-6 (`glkern.b6`) | `tests/forex-glissade/`, полная PERSO 9 модулей | 14 строк результата | **14/14** побайтово |
| Dhrystone 2.1 (FOREX 4.13-порт) | `besm6.net/examples/dhrystone-forex.dub` | 18 скалярных/массивных control + 4 строковых | **18+4/18+4**, 48/48 прогонов |
| Whetstone (Longbottom) | `besm6.net/examples/whetstone-longbottom-forex.dub` | 8 секций, `0.809 MWIPS` | **8/8**, MWIPS `±5 %` |
| Решето Эратосфена | `reference/forex.b6`, `reference/output.gold.txt` | SHA256 нормализованного вывода | совпадение SHA |

Dhrystone/Whetstone — «внешние» эталоны (4.13/Дубна); если дек недоступен в
данной среде, уровень — `SKIP`, формально не увеличивая R. Глиссада и решето
замкнуты локально и обязательны.

### 1.5. L4 — negative cases

Negative-кейс считается **пройденным**, если контур (1) получил ожидаемую
диагностику или ожидаемо пустой результат и (2) **не** записал его в gold как
успех. Список — §2, таблица `NC01…NC09`.

---

## 2. Конкретные тест-кейсы стандарт-матрицы

Стандарт-матрица = 21 позиция `docs/plan-f77/01-gap-analysis.md` §1 +
5 подтверждённых отказов §2.1 + отобранные `?`-позиции §2.2–2.3, сгруппированные
в **8 групп A–H, всего N = 32 слота**. Имена файлов — предлагаемые пути для
реализации; «существующий» означает, что файл уже есть и переиспользуется.

Обозначения tolerate: `exact` = побайтово после нормализации даты;
`1e-5` / `1e-4` = относительный допуск кросс-сверки; `1e-11` = DP-допуск
(48-битное слово БЭСМ-6); `5e-5` = абсолютный допуск для `F10.4`.

### Группа A — скаляры, типы, арифметика (5)

| ID | Файл (предлагаемый) | Что проверяет | Expected output | Tol |
|---|---|---|---|---|
| A01 | `tests/f77/suite/base.b6` / `.gold` *(сущ.)* | `INTEGER`/`REAL`, присваивание, `FORMAT(I,F)` | `   21      1.00      3.00` | exact; cross `1e-5` |
| A02 | `tests/f77-full/unit/A/a02_logical.b6` / `.gold` | `LOGICAL`, `.TRUE./.FALSE.`, `.AND./.OR./.NOT.`, `FORMAT(L1)` | ` T` | exact |
| A03 | `tests/f77/suite/blockif.b6` / `.gold` *(сущ.)* | отношения `.GT./.LT.` внутри `IF` | `     3.00` / `     4.00` | exact; cross `1e-5` |
| A04 | `tests/f77/suite/dpcomplex.b6` / `.gold` *(сущ.)* | `COMPLEX Z`, `CABS`, `2F10.4` | `    -5.0000   10.0000` / `     5.0000` | `5e-5` |
| A05 | `tests/f77/suite/dpcomplex.b6` + `tests/plan-f77/e1/precision/double/out.txt` | `DOUBLE PRECISION`, `1.0D0`, `D22.15`, `SQRT`/`SNGL` | `  1.414213562371515+000` / `  3.333333333333333-001` | `1e-11` |

### Группа B — управление потоком (4)

| ID | Файл | Что проверяет | Expected output | Tol |
|---|---|---|---|---|
| B01 | `tests/f77/suite/base.b6` *(сущ.)* | счётный `DO 10 I=1,3`, накопление суммы | `21` (внутри A01-блока) | exact |
| B02 | `tests/f77/suite/do2d.b6` / `.gold` *(сущ.)* | вложенные `DO`, индексация 2D | `  1     22.00` / `  2     26.00` / `  3     30.00` | exact; cross `1e-5` |
| B03 | `tests/f77/suite/blockif.b6` / `.gold` *(сущ.)* | `IF/THEN/ELSE/ENDIF`, вложенный `ELSE` | `     3.00` / `     4.00` | exact |
| B04 | `tests/f77-full/unit/B/b04_if_goto.b6` / `.gold` | однооператорный `IF (…) GO TO` (`glkern.b6:96-97`) | `OK 1` | exact |

### Группа C — массивы, DATA, COMMON (5)

| ID | Файл | Что проверяет | Expected output | Tol |
|---|---|---|---|---|
| C01 | `tests/f77-full/unit/C/c01_dim1.b6` | `DIMENSION V(4)`, обращение по индексу | `   10      2.50   4` | exact |
| C02 | `tests/f77/suite/do2d.b6` *(сущ.)* | `DIMENSION A(3,4)`, `DATA` по столбцам | `22.00 / 26.00 / 30.00` | exact; cross `1e-5` |
| C03 | `tests/f77/suite/dataparam.b6` / `.gold` *(сущ.)* | `DATA N/5/`, `DATA V/.../`, `DATA R/2.5/` | `   10      2.50   4` | exact |
| C04 | `tests/f77/suite/dataparam.b6` *(сущ.)* | `PARAMETER (N=4)` | `4` (в блоке C03) | exact |
| C05 | `tests/forex-glissade/glkern.b6` + `output.gold.txt` *(сущ.)* | `COMMON /APGAIN/`, `BLOCK DATA`, 5×5-матрицы, 22 `DATA` | 14 строк усилений | **14/14 exact** |

### Группа D — подпрограммы (3)

| ID | Файл | Что проверяет | Expected output | Tol |
|---|---|---|---|---|
| D01 | `tests/f77/suite/intrinsics_ext.b6` / `.gold` *(сущ.)* | вызов внешней `FUNCTION MYFUN`, определённой в той же деке | `     4.0000    3.5000    1.0000   10.0000` | exact; cross `1e-5` |
| D02 | `tests/plan-f77/e1/callfortran/{build,call}/task.b6` *(сущ.)* | `SUBROUTINE HELLO` → `*to perso:602310` → `*call hello` из зоны `0o2310` | `*CALL WORKS*` | exact |
| D03 | `tests/f77-full/unit/D/d03_external_decl.b6` | операторы `EXTERNAL FOO` / `INTRINSIC SQRT` | `     4.0000` | exact; при отказе → exclude/F77PREP |

### Группа E — встроенные функции (3)

| ID | Файл | Что проверяет | Expected output | Tol |
|---|---|---|---|---|
| E01 | `tests/f77/suite/intrinsics_ext.b6` *(сущ.)* | `SQRT`, `ABS`, `AMOD` | `4.0000  3.5000  1.0000  10.0000` | exact; cross `1e-5` |
| E02 | `tests/plan-f77/e1/precision/double/task.b6` *(сущ.)* | `SQRT(2.0D0)`, `1.0D0/3.0D0`, `F20.15` | `  1.414213562371515` / `    0.333333333333485` | `1e-11` DP, `1e-6` SP |
| E03 | `tests/plan-f77/e1/precision/complex/task.b6` *(сущ.)* | `Z*W`, `CABS`, `CSQRT`, `2F10.4` | `-5.0000 10.0000` / `5.0000` / `2.0000 1.0000` | `5e-5` |

### Группа F — форматированный вывод (5)

| ID | Файл | Что проверяет | Expected output | Tol |
|---|---|---|---|---|
| F01 | `tests/f77/suite/base.b6` + `dataparam.b6` *(сущ.)* | дескрипторы `I`, `F` | `   21      1.00      3.00` | exact; cross `1e-5` |
| F02 | `tests/f77/suite/dpcomplex.b6` *(сущ.)* | дескриптор `D22.15` (не `F` с DP!) | `  1.414213562371515+000` | `1e-11` |
| F03 | `tests/f77/suite/charhollerith.b6` / `.gold` *(сущ.)* | `DATA I/4HABCD/`, `FORMAT(1X,A4)` | ` АВСD` | exact |
| F04 | `tests/f77-full/unit/F/f04_format_l.b6` | дескриптор `L1` | ` T` | exact |
| F05 | `tests/f77-full/unit/F/f05_format_cont.b6` | `/` и продолжение `FORMAT` (как в `glkern.b6`) | 2 строки «CONT OK» | exact |

### Группа G — ввод и list-directed (3)

| ID | Файл | Что проверяет | Expected output | Tol |
|---|---|---|---|---|
| G01 | `tests/plan-f77/e1/units/read_nounit/task.b6` *(сущ.)* | `READ 10,X` + карта данных `3.50` | `     3.50` | exact |
| G02 | `tests/f77/suite/listio.b6` + `listio.f77` *(сущ.)* | `PRINT *,N` → `PRINT 9000,N` через F77PREP; `C@`-разметка в листинге | `         42` | exact |
| G03 | `tests/f77-full/unit/G/g03_read_end.b6` | `READ(*,*,END=99)` после понижения F77PREP | `99 reached` | exact; нативно — exclude |

### Группа H — новые слова и совместимость (4)

| ID | Файл | Что проверяет | Expected output | Tol |
|---|---|---|---|---|
| H01 | `logs/f77_prep_lowered.f77` → `tests/f77-full/unit/H/h01_implicit.b6` | `IMPLICIT NONE` удалён, `C@`-разметка сохранена | `         42` | exact |
| H02 | `tests/f77-full/unit/H/h02_save.b6` | `SAVE N` → `COMMON`-эмуляция либо удаление | `1` | exact |
| H03 | `tests/f77/suite/charhollerith.b6` + `tests/plan-f77/e1/strings/charstar_*` | `CHARACTER`: 2.02 — Hollerith-рецепт; 4.13 — `CHARACTER*30` | ` АВСD` | exact; нативный `CHARACTER` 2.02 — exclude |
| H04 | `tests/f77-full/unit/H/h04_names6.b6` | 7-символьные имена `AAAAAAX`/`AAAAAAY` → уникальные ≤6 (P0) | `1 2` | exact |

**Итого по матрице: 5+4+5+3+3+5+3+4 = 32 слота.**

### Negative cases (NE = 9)

| ID | Файл | Ожидаемая реакция | Классификация |
|---|---|---|---|
| NC01 | `tests/plan-f77/work/CHARSTAR/out.txt` *(сущ.)* | `ТИП ОП-ДА НЕ СООТВЕТ ОПЕРАЦ` | FAIL-как-ожидаемое |
| NC02 | `tests/plan-f77/work/LISTDIR/out.txt` *(сущ.)* | `ОШИБКА В ССЫЛКЕ НА ФОРМАТ` | FAIL-как-ожидаемое |
| NC03 | `tests/plan-f77/work/IMPLICIT/out.txt` *(сущ.)* | `НЕДОПУСТИМ КЛЮЧ СЛОВО` | FAIL-как-ожидаемое |
| NC04 | `tests/plan-f77/work/ENDREAD/out.txt` *(сущ.)* | `НЕДОПУСТИМ СИМВОЛ * В ВЫРАЖ` | FAIL-как-ожидаемое |
| NC05 | `tests/plan-f77/work/SAVE/out.txt` *(сущ.)* | `НЕДОПУСТИМ КЛЮЧ СЛОВО` | FAIL-как-ожидаемое |
| NC06 | `tests/plan-f77/e1/precision/dp_f_format/out.txt` *(сущ.)* | `I/О-ЕRRОR 227 … DЕТЕСТЕD IN IОСОNТD*` | FAIL-как-ожидаемое |
| NC07 | `tests/plan-f77/e1/strings/a4_wrong_type/out.txt` *(сущ.)* | `PRINT 10,12345` + `FORMAT(1X,A4)` → диагностика типов **или** пустой блок; не gold | FAIL-как-ожидаемое |
| NC08 | `tests/forex-glissade/` (контроль `docs/16` §2–3) | дубль `OCTTDEC` → `ИСПОРЧЕНА ПОДПРОГРАММА`; псевдоним `OCTTDE*` → rc=0 | FAIL→OK-переход |
| NC09 | `tests/check-source-words.py --manifest` (контроль `04-assembler-path.md` §5.2) | намеренная правка вне `allow` → rc=1 | FAIL-как-ожидаемое |

---

## 3. Автоматизация

### 3.1. Оркестратор и генератор деков

Предлагается единый сценарий `tests/f77-full/run-f77-full.sh` (по образцу
`tests/run-f77-suite.sh`) с библиотекой `tests/f77-full/mkdeck.sh`. Шаблон деки:

```
шифр 419999 зс5^
лен 41(2048)^
лен 60(2348-wr)^        # -wr только если decks пишут библиотеку
ееВ1а3
*name <CASE>
*call yesmemory
*perso:602300           # базоваяPERSO (зона 0o2300, LUN 60)
*perso:602310,cont      # только для D02/F77LIBR (зона 0o2310)
*no list
*forex                  # либо *ftn / *fortran для кросса
<Fortran-исходник с PROGRAM ...>
*execute
<карты данных, если нужны>
*end file
``````
еконец
```

Правило из `tests/f77/suite/README.md`: комментарии в исходнике — только
ASCII (`c----` в колонке 1); строчные кириллические символы в картах дают
`ОШИБКА` на вводе. Все деки содержат `PROGRAM ...`, чтобы тот же исходник
компилировался `*FTN`/`*FORTRAN` без правки.

### 3.2. Подготовка диска и PERSO зон `0o2300 + 0o2310`

1. `cp /usr/local/share/besm6/2348 $WORK/2348` — эталон не трогается
   (SHA из `docs/06-baseline.md` фиксирован).
2. `BESM6_PATH=$WORK besmtool write 2348 --from-file=build/FOREX_PERSO_2300.bin
   --start=1216` → зона `0o2300` (= 1216 dec).
3. При необходимости F77LIBR: компиляция `src/f77libr/F77LIB.FTN` с `*to perso:602310`
   → зона `0o2310` (= 1224 dec, 4 зоны). **Важно:** `*perso:603100` из плана 05
   адресует зону `0o3100` и даёт `ИСПОРЧЕН КАТАЛОГ PERSONAL LIBRARY`;
   правильная карта — `602310` (`tests/run-f77-runtime.sh:16-18`).
4. Проверка каталога: `besmtool dump 2348 --start=1224 --length=4` + python
   (как в `run-f77-runtime.sh:98-129`): имена `MYABS`, `MYMAX`, `FMTLNK`,
   завершатель `(0, FULWORD)`; базовая зона `0o2300` обязана остаться
   побайтово равной образу (`cmp -s base_readback.bin $IMAGE`).
5. Запуск: `cd $WORK && BESM6_PATH=$WORK:/usr/local/share/besm6 timeout 180
   $DISPAK_BIN job.b6 > case.raw 2> case.err`; `rc≠0` → FAIL + лог stderr.

### 3.3. Нормализация даты и баннера 2.02

* Дата: `sed -E 's/[0-9]{2}\.[0-9]{2}\.[0-9]{2}/##.##.##/g'` (как в E5).
  В `gold` даты нет, поэтому дата никогда не является причиной расхождения.
* Баннер `F О R Е Х … ВЕРСИЯ 2.02 ОТ 15.07.80` — часть эталонного вывода,
  в блок результата не входит. Внутри `L1` он **не нормализуется**; в `L2`
  (при сравнении с `*FTN`/`*FORTRAN`, у которых свои баннеры) обе стороны
  проходят `s/.*ВЕРСИЯ.*/<BANNER>/` и `s/.*М О Н И Т О Р.*/<BANNER>/`.
  Версия изделия `5.00 / 19.11.2026` фиксируется в заголовках `src/f77*/`,
  `tools/build_forex_perso.py` и docs, но **не** подменяет системный баннер.
* Блок результата: `extract_result()` — последние непустые строки перед
  `КОНЕЦ ЗАДАЧИ` (`run-f77-suite.sh:57-73`). diagnosed lines from FATAL
  lead to FAIL before extraction.

### 3.4. Кросс-прогон

Генерация `-deck` для `*FTN` — дословно по `run-f77-suite.sh:202-211`
(`шифр`, `лен 41(2048)`, `лен 60(2348)`, `*name F<case>`, `*system`,
`*full list`, `*ftn`, исходник, `*execute`, `*end file`). Для `*FORTRAN`
меняется только `*ftn → *fortran` и `*name D<case>`. Исходник вырезается из
`.b6` между `*forex` и `*execute` (`extract_source`). Числа сравниваются
`compare_numbers()` (regex `[-+]?(\d+(\.\d*)?|\.\d+)([EDed][-+]?\d+)?`, `D→E`);
для `*FORTRAN` дополнительно sliding-window `W=3` (§1.3). Расхождения пишутся
в `logs/f77_cross_{ftn,fortran}.txt` строками `CROSS FAIL` с обоими наборами.

### 3.5. Сохранение логов и gold

| Категория | Путь | Содержимое |
|---|---|---|
| Матрица | `logs/f77_full_matrix.txt` | 32 строки `OK/FAIL <id> <конструкция> <диагностика>` |
| Gold | `logs/f77_full_gold.txt` | `date`, `dispak`, `etalon`, `image`, `suite`, `gold/fact`, `diff -u` |
| Cross | `logs/f77_cross_ftn.txt`, `logs/f77_cross_fortran.txt` | `CROSS OK/FAIL`, числа, tolerance, sliding score |
| Реальные | `logs/f77_full_real.txt` | 14/14, 18+4, 8/8 + MWIPS, SHA решета |
| Negative | `logs/f77_full_negative.txt` | ожидаемая диагностика, факт, классификация |
| Gate | `logs/f77_full_gate.txt` | 20/20 + 11/11 статических сценариев |
| Manifest | `logs/f77_full.sha256` | SHA256 всех gold, образов и_CONTROLных векторов |

Новые gold-файлы и proposed-деки создаются **на этапе реализации**, не этим
документом. Существующие gold/`reference/` не перезаписываются.

---

## 4. Метрики приёмки

### 4.1. Формула

```
F77 полный = 32/32 конструкций OK,
             32 gold-пар,
             0 FAIL,
             кросс 8/8   (4/4 *FTN + 4/4 *FORTRAN; при SKIP *FORTRAN → 4/4 *FTN),
             4/4 реальные программы,
             9/9 negative,
             20/20 gate
```

Краткая строка для отчёта:
`F77 full = 32/32 constructs, 32 gold pairs, 0 FAIL, cross 8/8, real 4/4, neg 9/9, gate 20/20`.

### 4.2. Пороги

| Метрика | Порог | Основание |
|---|---|---|
| Конструкции | `32/32`, `rc=0`, `ERR/ОШИБКА/НЕДОПУСТИМ/АТТ/ТИП ОП-ДА = 0` | E5 FATAL-фильтр |
| Gold | 100 % побайтово после нормализации даты | E5 8/8 |
| Cross `*FTN` | `max(1e-6, 1e-5·max)`; прежний результат 3/3 | `12-acceptance.md` §3 |
| Cross `*FORTRAN` | `1e-4` + sliding `score ≥ 0.95` + первая/последняя строки | `04-assembler-path.md` §5.4 |
| DP | relative `1e-11` (48-битное слово, 40-битная мантисса) | E1 `1.414213562371515` |
| Глиссада | 14/14 | `docs/16` §1 |
| Dhrystone | 18+4 control; 48/48 прогонов | `01-gap-analysis.md` §3.1 |
| Whetstone | 8/8 секций, 0.809 MWIPS ±5 % | `01-gap-analysis.md` §3.2 |
| Negative | 9/9 «отказ классифицирован», ложных OK = 0 | §2 |
| Регрессия | 20/20, плюс 11/11 статических сценариев `tests/README.md` | §5 |

### 4.3. Exclude-лист (принципиально недостижимо / не относится к F77)

| Исключение | Причина | Что вместо |
|---|---|---|
| Рекурсия (`RECURSIVE`) | F90, не F77; `01-gap-analysis.md` §2.3 | не тестируется |
| `RECORD`, `DO…REPEAT`, `ARM` как синтаксис | не подтверждены как синтаксис ФОРЭКСа; `RECORD`/`REPEAT` в корпусе — идентификаторы; приоритет P3 | не в матрице |
| `DO WHILE`, `END DO` | F90; системный 2.02 не компилирует | только F77PREP-lowering (H-группа) |
| `IMPLICIT NONE` (нативно, 2.02) | `НЕДОПУСТИМ КЛЮЧ СЛОВО`; это F90-расширение | H01 через F77PREP |
| `SAVE` (нативно, 2.02) | `НЕДОПУСТИМ КЛЮЧ СЛОВО` | H02 через F77PREP/COMMON |
| `CHARACTER` как тип (нативно, 2.02) | версионная зависимость: 2.02 `ТИП ОП-ДА`, 4.13 работает | H03 Hollerith `4HABCD` + `A4` |
| List-directed `PRINT *`/`READ *` (нативно, 2.02) | `ОШИБКА В ССЫЛКЕ НА ФОРМАТ`, `НЕДОПУСТИМ СИМВОЛ *` | G02/G03 через F77PREP |
| DP с `F`-дескриптором | `I/О-ЕRRОR 227` (`dp_f_format`) | NC06 + `D22.15` (F02) |
| Байтовая идентичность симтаблицы / полная обратная сборка | `docs/05-roundtrip.md` | многослойная проверка `05-decision.md` §5 (SHA → opcode → метки → gold → cross) |
| Молчаливое слияние имён >6 знаков | 6-символьный лимит МАДЛЕН/TEXT; P0 | H04 — детектируется и понижается манглингом, но «полная уникальность нативным синтаксисом» не достигается |
| `*FORTRAN` (Дубна) как обязательный эталон | расхождения диалекта и форматирования | `SKIP (нет эталона)` не блокирует; базовый порог — `*FTN 4/4` |

Переход любого пункта из exclude в матрицу — только отдельным изменением
плана с новой пробой и новым gold.

---

## 5. Регрессия 20/20 — обязательный gate

Состав (фиксируется `docs/plan-f77/04-assembler-path.md` §5.1 и §6 п.8):

| Часть | Сценарии | Источник | Критерий |
|---|---|---|---|
| 16 базовых | `BASE, DOLOOP, BLOCKIF, CHARSTAR, DOUBLPR, COMPLEX, LOGICAL, INTRINSIC, EXTERNAL, DATAST, PARAMETER, LISTDIR, IMPLICIT, ENDREAD, SAVE` + `GLISSADE` | `tests/plan-f77/probe.sh` + `tests/install-forex-perso.sh && tests/run-glissade-forex.sh` | 15/15 probe + 14/14 строк |
| 4 новых F77-теста | `LISTDIR`, `IMPLICIT`, `ENDREAD`, `SAVE` — положительные golden-деки в `tests/plan-f77/f77/` (сейчас FAIL → после реализации OK) | `04-assembler-path.md` §5.2 | 4/4 rc=0, `НЕДОПУСТИМ КЛЮЧ СЛОВО` отсутствует |

**Gate = 16 + 4 = 20/20, rc=0.** Порядок:

1. до правки зафиксировать базовый прогон (15/15 + 14/14, 4 FAIL ожидаемы);
2. после правки — 20/20; любая новая FAIL-строка или пропажа строки
   останавливает приёмку;
3. дополнительный CI-уровень: 11/11 сценариев `tests/README.md`
   (`run-forex`, `verify-dumps`, `check-annotations`, `check-disasm`,
   `check-dtran`, `check-word-coverage`, `check-labels`, `check-constants`,
   `check-runtime-disasm`, `check-source-words.py`, `run-f77-suite.sh`).

Gate проверяется **до** и **после** полной матрицы: если 20/20 не проходит,
результаты L0–L4 в приёмку не засчитываются.

### 5.1. Итоговый порядок приёмки

```
G0  11/11 статических сценариев  → G  20/20 gate (до правки)
L0  32/32 конструкций            → L1  32 gold-пар, 0 FAIL
L2  8/8 cross (*FTN 4/4, *FORTRAN 4/4) → L3  4/4 реальные программы
L4  9/9 negative                 → G  20/20 gate (после правки)
→ итоговая строка §4.1
```

---

## 6. Воспроизведение (после реализации)

```sh
cd /tmp/.private/azizz/opencode/re-forex
tests/f77-full/run-f77-full.sh
cat logs/f77_full_matrix.txt logs/f77_full_gold.txt \
    logs/f77_cross_ftn.txt logs/f77_cross_fortran.txt \
    logs/f77_full_real.txt logs/f77_full_negative.txt logs/f77_full_gate.txt
```

Переопределения (как в E5/E2): `DISPAK_BIN`, `BESMTOOL`, `ETALON`, `IMAGE`,
`TIMEOUT`, `TMPROOT`. При отсутствии dispak/`besmtool`/эталона/PERSO-образа —
`ОЖИДАЕТСЯ`, `rc=0` (ветка prerequisites сохраняется).
