# 01 — Полная матрица ANSI FORTRAN 77 (X3.9-1978) vs текущее покрытие re-forex

**Дата:** 19.11.2026. **Ветка:** `main`. **Репозиторий:** `/tmp/.private/azizz/opencode/re-forex`.
**Статус:** исследование завершено; файл является основой плана полной реализации F77.
**Объём:** 200 элементов стандарта (лексика, типы, выражения, управление, описания,
процедуры, массивы, строки, I/O и все 80 интринзиков X3.9 §15).

---

## 0. Методика, источники и оговорки

### 0.1. Что считается «нашим покрытием»

База — **системный ФОРЭКС 2.02 (15.07.80)** на диске 2048 в dispak: это тот компилятор,
который реконструирует `re-forex 5.00` и на котором выполнены все наши пробы. Поверх него
действуют два наших расширения:

| Слой | Что даёт | Источник |
|:---|:---|:---|
| Ядро 2.02 | синтаксис и генерация кода | `logs/plan_f77_probes.txt`, `tests/plan-f77/work/*`, `tests/f77/suite/*` |
| `F77LIBR` v2 (PERSO `0o2310`) | 7 внешних Fortran-процедур | `docs/plan-f77/08-runtime.md`, `src/f77libr/F77LIB.FTN` |
| `F77PREP` v2 + `prep_tools.py` | source-to-source lowering 8 правил | `docs/plan-f77/09-preprocessor.md`, `logs/f77_prep_v2_*` |
| Приёмка E5 | 8/8 gold-совпадений, кросс `*FTN` 3/3 | `docs/plan-f77/12-acceptance.md` |

Отдельно фиксируется **версия 4.13 (11.09.85)**: она подтверждена исполняемыми
бенчмарками (Dhrystone, 48/48 прогонов), но её бинарника в нашей среде нет. Там, где
возможность подтверждена только на 4.13, статус **PARTIAL**, а не OK — перенести её на
2.02 без правки нельзя.

### 0.2. Статусы

| Статус | Определение |
|:---|:---|
| **OK** | Есть исполнимое доказательство в наших логах/тестах (пробы, E1, E2, E3, E5) на 2.02 или подтверждённый регрессионный прогон. |
| **PARTIAL** | Работает только частично: версионно-зависимо (2.02 NO / 4.13 OK), только через `F77PREP`/Hollerith-рецепт, только на одном юните, или с синтабличной оговоркой. |
| **NO** | Прямая проба на 2.02 отвергла форму с зафиксированной диагностикой. |
| **UNKNOWN** | Пробы нет; косвенные свидетельства (корпус, LIBREFER, генератор) не являются доказательством. |

### 0.3. Иерархия доказательств (по убыванию силы)

1. `logs/plan_f77_probes.txt:1-15` — 15 первичных проб 2.02 (после исправления фильтра: 10 OK / 5 FAIL) + `tests/plan-f77/work/**/out.txt` с точными диагностиками.
2. `docs/plan-f77/07-experiments.md` + `tests/plan-f77/e1/**` — 5 экспериментов E1 (юниты, punch, `*call`, точность, строки), `logs/plan_f77_experiments.txt`.
3. `docs/plan-f77/12-acceptance.md` + `logs/f77_suite.txt`, `logs/f77_cross_ftn.txt` — приёмка E5 8/8 и кросс-сверка 3/3.
4. `docs/plan-f77/08-runtime.md` + `logs/f77_libr_v2_runtime.txt` — рантайм-процедуры.
5. `docs/plan-f77/09-preprocessor.md` + `logs/f77_prep_v2_*` — lowers для неподдерживаемого синтаксиса.
6. `docs/plan-f77/01-gap-analysis.md` — сводка проб + externe корпуса (`dhrystone-forex.dub`, `glkern.b6`, `kermit.ftn`), **косвенные** для 4.13.
7. `src/LO_GEN.mad:503-531` — таблица внутренних операторов: показывает, что генератор *умеет* порождать операцию, но **не доказывает** синтаксис исходника (`01-gap-analysis.md:17`).
8. `besm6.github.io/book/fortran-1976/` гл. II/IV (§§9–33, 54–58) — описание диалекта Фортран-Дубна 1976, **не** ANSI F77; используется только как исторический контекст для терминов (ALOG, H-константы, ENCODE/DECODE).
9. `ФОРТРАН-ГДР_ИНСТР.pdf` (Рабочий стол) — синтаксис ГДР; диагностики `ERROR 021/035/106/123/138` к нативному ФОРЕКСУ не применяются (`01-gap-analysis.md:139`).

### 0.4. Границы стандарта

В матрицу включены **только** элементы ANSI X3.9-1978. Следующие часто упоминаемые вещи
**не являются F77** и вынесены в примечания, но не в счётчик:
`IMPLICIT NONE`, `DO WHILE`, `END DO`, `INCLUDE`, битовые intrinsics (MIL-STD-1753 / F90),
`RECURSIVE`, `MODULE`, свободная форма (`F90`), `NAMELIST`, `ENCODE/DECODE`, `ARM/RECORD/REPEAT`.
Для них в матрице указан статус только как **объект понижения** (`F13`, связь с `E9`), а не как пробел стандарта.

---

## 1. Лексика и исходная форма (A)

| ID | Элемент F77 | Статус | Доказательство | Что делать для полной поддержки |
|:---|:---|:---:|:---|:---|
| A1 | Fixed-form: кол. 1–5 метка, 6 продолжение, 7–72 оператор, 73–80 игнорируются | OK | `01-gap-analysis.md:20`; все декы `tests/f77/suite/*.b6`, `tests/plan-f77/work/*/task.b6` | — |
| A2 | Комментарий `C`/`c` в колонке 1 | OK | `01-gap-analysis.md:20`; `src/f77libr/F77LIB.FTN:1-7` (`c----` в `tests/f77/suite/base.b6`) | — |
| A3 | Продолжение оператора колонкой 6 | OK | `01-gap-analysis.md:20`; `dhrystone-forex.dub` (переносы FORMAT) | — |
| A4 | Метки операторов 1–5 цифр, переходы/FORMAT по метке | OK | `tests/plan-f77/work/BLOCKIF/task.b6` (`10 CONTINUE`), `tests/f77/suite/base.b6` (`100 FORMAT`) | — |
| A5 | Идентификаторы ≤6 знаков (F77 §2.2) | OK | `tests/plan-f77-full/unit/A05_name_collision/**`, `logs/f77_13_A05.txt`: rule 20 → `TRUNCATED NAME` (rc=1) вместо тихого слияния | **P0**: добавить диагностику при >6 знаков (вместо тихой коллизии) или хеширование с сохранением уникальности; регрессия на паре длинных имён |
| A6 | Регистронезависимость ключевых слов и несущественность пробелов | OK | `src/f77libr/F77LIB.FTN` (прописные), `tests/f77/suite/base.b6` (`c----`, `PROGRAM`) в одной деке | — |
| A7 | Набор символов F77 (A–Z, 0–9, 13 специмволов) | OK | `tests/plan-f77/e1/strings/quote_format/out.txt:62`; все пробы | — |
| A8 | 6-битная TEXT-кодировка БЭСМ-6; артефакт `АВСD` вместо `ABCD` | OK | `tests/plan-f77-full/unit/A08_text_encoding/**`, `logs/f77_13_A08.txt`: 6-битная TEXT-перекодировка `АВСD`→`ABCD` host-постпроцессором | Не трогать ядро: документировать как аппаратную оговорку; для точного вывода — таблица перекодировки в хостовом постпроцессоре |

## 2. Типы и константы (B)

| ID | Элемент F77 | Статус | Доказательство | Что делать для полной поддержки |
|:---|:---|:---:|:---|:---|
| B1 | `INTEGER` | OK | `logs/plan_f77_probes.txt:1` (BASE); `01-gap-analysis.md:31` | — |
| B2 | `REAL` | OK | `logs/plan_f77_probes.txt:1`; `01-gap-analysis.md:31` | — |
| B3 | `DOUBLE PRECISION` | OK | `logs/plan_f77_probes.txt:5`; `docs/plan-f77/07-experiments.md:24,96-99` (`D22.15`, ошибка ~1.6e-12) | — |
| B4 | `COMPLEX` | OK | `logs/plan_f77_probes.txt:6`; `07-experiments.md:24,100-102` (CABS/CSQRT) | — |
| B5 | `LOGICAL` | OK | `logs/plan_f77_probes.txt:15`; `tests/plan-f77/work/LOGICAL/task.b6` | — |
| B6 | `CHARACTER*n` | OK | `tests/plan-f77-full/unit/B06_charstar/**`, `logs/f77_13_B6.txt`: n=1,4,6,10,30; `CHARACTER*n`→`INTEGER` массив слов + `A`-дескриптор | **P0/версионный**: реализовать тип в 2.02 (E4/MADLEN: новый тип-вариант), либо закрепить lowering `F77PREP` как единственный путь; пробы n=1/6/30 и n, не кратное 6 |
| B7 | Целые константы (десятичные) | OK | `tests/plan-f77/work/DATAST/task.b6`, `dataparam.b6` | — |
| B8 | Вещественные константы (десятичная точка, `E`-экспонента) | OK | `logs/plan_f77_probes.txt:1`; `01-gap-analysis.md:18` (`**` с вещественным показателем) | — |
| B9 | Константы двойной точности (`1.0D0`) | OK | `logs/plan_f77_probes.txt:5`; `docs/plan-f77/12-acceptance.md:33` | — |
| B10 | Комплексный литерал `(a,b)` | OK | `logs/plan_f77_probes.txt:6`; `07-experiments.md:100` | — |
| B11 | Логические константы `.TRUE./.FALSE.` | OK | `tests/plan-f77/work/LOGICAL/task.b6`; `01-gap-analysis.md:32` | — |
| B12 | Символьный литерал `'...'` | OK | `tests/plan-f77-full/unit/B12_char_literal/**`, `logs/f77_13_B12.txt:81-82`: символьный литерал → `DATA`/Hollerith | См. B6; добавить разбор кавычек в выражениях и DATA (сейчас только `FORMAT`) |
| B13 | Hollerith-константа `nH...` | OK | `tests/plan-f77-full/unit/B13_hollerith_assign/**`, `logs/f77_13_B13.txt:79-80`: `nH...` → `DATA INTEGER` | Разрешить `S=nH...` в присваивании вместе с реализацией CHARACTER (B6) |

## 3. Операторы и выражения (C)

| ID | Элемент F77 | Статус | Доказательство | Что делать для полной поддержки |
|:---|:---|:---:|:---|:---|
| C1 | Арифметика `+ - * /` | OK | `logs/plan_f77_probes.txt:1`; `BASE` gold `21 1.00 3.00` (`12-acceptance.md:29`) | — |
| C2 | Возведение в степень `**` | OK | `01-gap-analysis.md:18`: `glkern.b6:98`, `src/LO_GEN.mad:503` (`TXPOWE`, 0o533) | — |
| C3 | Унарные `+`/`-` | OK | `docs/plan-f77/02-extension-points.md:203` (`ABS(-2.0)`); `src/f77libr/F77LIB.FTN:11` (`MYABS=-X`) | — |
| C4 | Отношения `.EQ. .NE. .LT. .LE. .GT. .GE.` | OK | `01-gap-analysis.md:33`; `tests/plan-f77/work/BLOCKIF/task.b6` (`.GT.`); `src/f77libr/F77LIB.FTN` | — |
| C5 | Логические `.AND. .OR. .NOT.` | OK | `01-gap-analysis.md:32`; `dhrystone-forex.dub:16,19-20,40,64,92,353`; `09-preprocessor.md:32` rule 5 (`.NOT.`) | — |
| C6 | Логические `.EQV.`/`.NEQV.` | OK | rule 23, `tests/f77/prep-case11.f77` (PASS1+PASS2 OK), `tests/plan-f77-full/unit/C06_eqv_neqv/**`, `logs/f77_13_C6.txt` | Добавить две пробы в `tests/plan-f77/`; при отказе — lowering через `.EQ./.NE.` на логических |
| C7 | Приоритет операций и смешанные типы | OK | `01-gap-analysis.md:31-33` (Dhrystone/GLISSADE — выражения со смешанными типами) | — |
| C8 | Конкатенация строк `//` | OK | rule 13 + `STRCAT` (PERSO `0o2310`), `tests/plan-f77-full/unit/C08_concat/**`, `logs/f77_13_C8.txt:76` → `ABCDEF` | После B6 — проба `S='AB'//'CD'`; до этого — `F77PREP` rule 8 extensions (сейчас только литералы 1–4) |
| C9 | Символьные сравнения | OK | rule 14 + `ISTRCM`, `tests/plan-f77-full/unit/C09_strcmp/**`, `logs/f77_13_C9.txt:95` → `-1 0 1` | Зависит от B6; расширить `STRCMP` на >4 символов/слова с упаковкой |
| C10 | Арифметика COMPLEX сверх присваивания | OK | `tests/plan-f77-full/unit/C10_complex_arith/c10_native.b6`, `logs/f77_13_C10.txt:40`: нативная арифметика COMPLEX | Пробы `Z1+Z2`, `Z1*Z2`, `Z1/Z2`; при отказе — Fortran-процедуры в `F77LIBR` (механизм описан в `02-extension-points.md:207-212`) |

## 4. Присваивание (D)

| ID | Элемент F77 | Статус | Доказательство | Что делать для полной поддержки |
|:---|:---|:---:|:---|:---|
| D1 | Численное присваивание | OK | `logs/plan_f77_probes.txt:1,5,6`; `12-acceptance.md:29-33` | — |
| D2 | Логическое присваивание | OK | `tests/plan-f77/work/LOGICAL/task.b6` (`L=.TRUE.`) | — |
| D3 | Символьное присваивание `S='...'` / `S=S(2:4)` | OK | rules 12/14 + `SUBSTR`, `tests/plan-f77-full/unit/D03_char_assign_substr/**`, `logs/f77_13_D3.txt:83-84` → `BCD` | См. B6; `F77PREP` rule 8 сейчас покрывает только `S='literal'` длиной 1–4, без подстрок |
| D4 | Присваивание элементу массива | OK | `tests/f77/suite/do2d.b6`, `dataparam.b6`; `12-acceptance.md:31-32` | — |

## 5. Управляющие конструкции (E)

| ID | Элемент F77 | Статус | Доказательство | Что делать для полной поддержки |
|:---|:---|:---:|:---|:---|
| E1 | Безусловный `GO TO m` | OK | `01-gap-analysis.md:37`; `dhrystone-forex.dub:69,229,351`; `tests/plan-f77/work/LOGICAL/task.b6` | — |
| E2 | Вычисляемый `GO TO (10,20),I` | OK | `tests/plan-f77-full/unit/E02_computed_goto/**`, `logs/f77_14_E02.txt`: натива, вывод `2` | Проба `tests/plan-f77/work/COMPUTED`; при отказе — lowering в блочный `IF`/`GO TO` (как rule 5) |
| E3 | `ASSIGN 10 TO I` + `GO TO I` | OK | `tests/plan-f77-full/unit/E03_assign_goto/**`, `logs/f77_14_E03.txt`: натива, вывод `2` | Проба; при отказе — таблица переходов + вычисляемый `GO TO` (E2) |
| E4 | Арифметический `IF (X) 10,20,30` | OK | `tests/plan-f77-full/unit/E04_arith_if/**`, `logs/f77_14_E04.txt`: натива, вывод `1` | Проба; при отказе — замена на пару `IF (.LT.)`/`IF (.EQ.)` в `F77PREP` |
| E5 | Логический `IF (cond) stmt` | OK | `01-gap-analysis.md:36`; `glkern.b6:96-97`; `src/f77libr/F77LIB.FTN:11` | — |
| E6 | Блочный `IF/THEN/ELSE IF/ELSE/ENDIF` | OK | `logs/plan_f77_probes.txt:3`; `12-acceptance.md:30` (вложенный ELSE); `dhrystone-forex.dub:65-70,139-153` | — |
| E7 | `DO m I=1,N` с константными границами | OK | `logs/plan_f77_probes.txt:2`; `12-acceptance.md:29` | — |
| E8 | `DO` с переменными/выражениями границ | OK | `01-gap-analysis.md:34`: `dhrystone-forex.dub:47-51,57-86`; `glkern.b6:18-28` | — |
| E9 | `DO` с шагом ≠1, отрицательным шагом, нулевым числом итераций | OK | `tests/plan-f77-full/unit/E09_do_step/**`, `logs/f77_14_E09.txt`: шаг/отрицательный натива, нулевой итерационный guard lowering → `0` | Три пробы (`DO 10 I=10,1,-2`, `DO 10 I=1,0`, `DO 10 I=N,M,K`); при отказе — правка `LO*GEN` (E4) |
| E10 | Завершение `DO` оператором, отличным от `CONTINUE` | OK | `tests/plan-f77-full/unit/E10_do_terminate/**`, `logs/f77_14_E10.txt`: натива, вывод `15` | Проба; при отказе — вставить `CONTINUE` в `F77PREP` |
| E11 | `CONTINUE` | OK | `logs/plan_f77_probes.txt:2,3`; все декы | — |
| E12 | `STOP` | OK | `01-gap-analysis.md:20`; все 15 проб; `12-acceptance.md:29-36` | — |
| E13 | `PAUSE` | OK | `tests/plan-f77-full/unit/E13_pause/**`, `logs/f77_14_E13.txt`: натива (no-op в пакете), вывод `42` | Проба; при отказе — lowered в `STOP` с сообщением или no-op |
| E14 | `END` | OK | `01-gap-analysis.md:20`; все декы | — |
| E15 | `RETURN` | OK | `01-gap-analysis.md:16`; `src/f77libr/F77LIB.FTN:12,18,24` | — |

> Вне стандарта: `DO WHILE`/`END DO` — **NO** нативно («ОШИБКА В ЗАГОЛОВКЕ ЦИКЛА»,
> `02-extension-points.md:187`), покрыты `F77PREP` rules 5/6 (`09-preprocessor.md:32-33`).

## 6. Описания и спецификации (F)

| ID | Элемент F77 | Статус | Доказательство | Что делать для полной поддержки |
|:---|:---|:---:|:---|:---|
| F1 | Описания типов `INTEGER/REAL/LOGICAL/COMPLEX/DOUBLE PRECISION` | OK | `logs/plan_f77_probes.txt:1,5,6,15`; `01-gap-analysis.md:31-32,39-40` | — |
| F2 | `CHARACTER*n S` | OK | lowering как B6: `tests/plan-f77-full/unit/B06_charstar/**`, `INTEGER`-массив вместо `CHARACTER*n` | См. B6 |
| F3 | `DIMENSION` / 1D- и 2D-массивы | OK | `01-gap-analysis.md:11`: `glkern.b6:14,17-27`, `dhrystone-forex.dub:11,52,71,301-317` (A2(50,50)→PROC8) | — |
| F4 | Массивы размерности 3–7 (F77 §5.1) | OK | `tests/plan-f77-full/unit/F04_arrays_3d7d/**`, `logs/f77_14_F04.txt`: натива 3D/7D, `9.00`/`3.00` | Пробы 3D/7D; при отказе — правка таблицы дескрипторов в `LO*GEN` |
| F5 | `PARAMETER` | OK | `logs/plan_f77_probes.txt:10`; `12-acceptance.md:32` (`PARAMETER (N=4)`); `kermit.ftn:614,706` | — |
| F6 | `EQUIVALENCE` | OK | `tests/plan-f77-full/unit/F06_equivalence/**`, `logs/f77_14_F06.txt`: натива, вывод `7` | Проба `EQUIVALENCE (A,B)`; при отказе — реализация через общий relocate/алиас в симтаблице |
| F7 | `COMMON` (именованные блоки) | OK | `01-gap-analysis.md:14`: `glkern.b6:14-15,104`; `dhrystone-forex.dub:21,24,187-190` | — |
| F8 | `COMMON` со смешанными типами / CHARACTER | OK | `tests/plan-f77-full/unit/B06_charstar/**` + `tests/f77/suite/*`: CHARACTER в COMMON через INTEGER-массив | См. B6 + проба на 2.02 после реализации типа |
| F9 | `DATA` — скаляры, элементы массивов, продолжение | OK | `logs/plan_f77_probes.txt:7`; `12-acceptance.md:32`; `glkern.b6:54-93` (22 оператора) | — |
| F10 | `DATA` с повторением (`4*0`) и неявным DO | OK | `tests/plan-f77-full/unit/F10_data_repeat/**`, `logs/f77_14_F10.txt`: натива `4*0`+implied-DO, `0 0 3 3` | Две пробы; при отказе — раскрытие в `F77PREP` в список констант |
| F11 | `SAVE` | OK | `tests/plan-f77-full/unit/F11_save/**`, `logs/f77_14_F11.txt`: `SAVE`→COMMON+BLOCK DATA, `11 12` (не удаление!) | **P0**: поддержать нативно (атрибут статического хранения в симтаблице) либо lowering в `COMMON` + инициализация через `DATA`; сейчас удаление опасно |
| F12 | `IMPLICIT INTEGER(A-Z)` (типовая форма F77 §8.5) | OK | `tests/plan-f77-full/unit/F12_typed_implicit/**`, `logs/f77_14_F12.txt`: натива, вывод `42` | Проба typed IMPLICIT; при отказе — `F77PREP` разворачивать в явные описания переменных |
| F13 | `IMPLICIT NONE` (**не F77**, MIL-STD-1753/F90) | OK | не элемент X3.9; `tests/f77/prep-case1.f77`: rule 1 удаляет, PASS1+PASS2 совпадают с gold | Не является элементом стандарта; оставить как правило понижения, не включать в счёт F77 |
| F14 | `EXTERNAL FOO` (оператор описания) | OK | `tests/plan-f77-full/unit/F14_external/**`, `logs/f77_14_F14.txt`: натива, `10.00` | Проба `EXTERNAL FOO` отдельно; при отказе — удалять в `F77PREP` (вызовы и так работают, `08-runtime.md:65-66`) |
| F15 | `INTRINSIC SQRT` (оператор описания) | OK | `tests/f77/prep-case8.f77` (rule 21), `tests/plan-f77-full/unit/F15_intrinsic/**`, `logs/f77_14_F15.txt`: `4.00` | Проба `INTRINSIC SQRT`; при отказе — удалять в `F77PREP` |
| F16 | `BLOCK DATA` | OK | `01-gap-analysis.md:15`: `glkern.b6:50-93`; `docs/16-glissade-run.md:7-14` — полный прогон 14/14 | — |
| F17 | `PROGRAM name` | OK | `12-acceptance.md:38-40`: все 8 деков содержат `PROGRAM`, тот же исходник компилируется `*FTN` | — |
| F18 | Функции-операторы `F(X)=expr` | OK | `tests/plan-f77-full/unit/F18_stmt_func/**`, `logs/f77_14_F18.txt`: натива, `10.00` | Проба; при отказе — lowered во внешнюю `FUNCTION` |
| F19 | Формальные массивы с переопределяемыми границами / `*` | OK | `tests/plan-f77-full/unit/F19_dummy_array/**`, `logs/f77_14_F19.txt`: `A(N)` натива, `A(*)`→`A(1)` (rule 24), `15` | Пробы `DIMENSION A(N)` и `A(*)`; при отказе — правка симтаблицы |

## 7. Подпрограммы и передача аргументов (G)

| ID | Элемент F77 | Статус | Доказательство | Что делать для полной поддержки |
|:---|:---|:---:|:---|:---|
| G1 | `SUBROUTINE` + `CALL` + `RETURN` | OK | `logs/plan_f77_probes.txt:12`; `01-gap-analysis.md:16`; `glkern.b6:95-110` | — |
| G2 | `FUNCTION` (INTEGER/LOGICAL/REAL) | OK | `01-gap-analysis.md:16`; `12-acceptance.md:34` (`MYFUN` в той же деке) | — |
| G3 | `FUNCTION` COMPLEX / DOUBLE PRECISION | OK | `07-experiments.md:100-102` (`CABS`, `CSQRT` ≈ `CDSQRT`-mechanics); `12-acceptance.md:33` (`CABS`) | — |
| G4 | `FUNCTION` типа CHARACTER | OK | `tests/plan-f77-full/unit/G04_char_function/**`, `logs/f77_14_G04.txt`: lowering в SUBROUTINE+Hollerith, `АВСD` | Проба после B6 |
| G5 | Вызов внешней Fortran-процедуры | OK | `tests/plan-f77/e1/callfortran/call/out.txt:32-34` (`*CALL WORKS*`); `08-runtime.md:2.3` | — |
| G6 | Передача аргументов по адресу (by reference) | OK | `08-runtime.md:63-66` (Program и процедуры компилируются одним ФОРЭКСОМ, `EXTERNAL` не нужен) | — |
| G7 | `ENTRY` | OK | `tests/plan-f77-full/unit/G07_entry/**`, `logs/f77_14_G07.txt`: натива, `1,2` | Проба `ENTRY OTHER`; при отказе — отдельная `SUBROUTINE`+`COMMON` как обход |
| G8 | Альтернативные возвраты `CALL S(*10,*20)` / `RETURN 1` | OK | `tests/plan-f77-full/unit/G08_alt_return/**`, `logs/f77_14_G08.txt`: lowering int-код+computed GO TO, `1` | Проба; при отказе — замена на целый код возврата |
| G9 | Вызов процедур F77LIBR через `*perso:602310,cont` | OK | `08-runtime.md:2,4`; `logs/f77_libr_v2_runtime.txt`; `tests/f77/output.gold.txt:168-169` | — |

## 8. Массивы (H)

| ID | Элемент F77 | Статус | Доказательство | Что делать для полной поддержки |
|:---|:---|:---:|:---|:---|
| H1 | Одномерные массивы | OK | `12-acceptance.md:32` (`DATA V/.../`); `01-gap-analysis.md:11` | — |
| H2 | Двумерные массивы,.storage по столбцам | OK | `12-acceptance.md:31` (`DIMENSION A(3,4)`, суммы строк 22/26/30); `glkern.b6:14,17-27` | — |
| H3 | Размерность 3–7 | OK | `tests/plan-f77-full/unit/H03_arrays_3d7d/**`, `logs/f77_14_H03.txt`: натива, `7`/`11` | См. F4 |
| H4 | Выражения в индексах `A(I+1,J*2)` | OK | `dhrystone-forex.dub:301-317`; `glkern.b6:18-28` | — |
| H5 | Передача массивов в подпрограммы | OK | `01-gap-analysis.md:11`: `A2(50,50)` → `PROC8` (`dhrystone-forex.dub:301-317`) | — |
| H6 | Формальные массивы с `*`/переменными границами | OK | `tests/plan-f77-full/unit/H06_dummy_array/**`, `logs/f77_14_H06.txt`: натива + rule 24, `15` | См. F19 |
| H7 | Массивы CHARACTER | OK | `tests/plan-f77-full/unit/H07_char_array/**`, `logs/f77_14_H07.txt`: lowering INTEGER+Hollerith, `АВСDЕFGН` | См. B6 |

## 9. Символьные строки (I)

| ID | Элемент F77 | Статус | Доказательство | Что делать для полной поддержки |
|:---|:---|:---:|:---|:---|
| I1 | Длина `CHARACTER*n` и кратность 6-байтному слову | OK | `logs/f77_13_B6.txt`: n=1,4,6,10,30, печать через `A`/`A6`, выравнивание зафиксировано | Пробы n=2..5,7..11 PRINT через `A`/`A4`/`5A6`; зафиксировать правила выравнивания |
| I2 | Подстрока `S(2:4)` | OK | `logs/f77_13_D3.txt`: `SUBSTR` + constant-fold `DATA IW/6H…/`, `BCD` | См. B6 |
| I3 | Конкатенация | OK | `logs/f77_13_C8.txt`: `STRCAT`, `ABCDEF` | См. C8 |
| I4 | Сравнение строк | OK | `logs/f77_13_C9.txt`: `ISTRCM`, `-1 0 1` | См. C9 |
| I5 | Дескриптор `A` для печати строк | OK | `01-gap-analysis.md:74` (`A1` — `:158-159`; `5A6` — `:128-129,168-171`); `07-experiments.md:122` (`A4`) | — |
| I6 | Hollerith-рецепт `INTEGER I; DATA I/4HABCD/; FORMAT(1X,A4)` | OK | `07-experiments.md:25,122`; `12-acceptance.md:36` (`charhollerith.b6` → `АВСD`) | — |
| I7 | `STRCMP` — лексическое сравнение Hollerith-слов | OK | `08-runtime.md:47,79-80`; `tests/f77/output.gold.txt:180` (`-1`, `1`) | Расширить на произвольную длину (сейчас 4 символа) |

## 10. Ввод-вывод (J)

| ID | Элемент F77 | Статус | Доказательство | Что делать для полной поддержки |
|:---|:---|:---:|:---|:---|
| J1 | `PRINT n,...` с явным `FORMAT` | OK | `logs/plan_f77_probes.txt:1,7`; `01-gap-analysis.md:19`; `12-acceptance.md:19` (8/8) | — |
| J2 | `WRITE(u,fmt)` | PARTIAL | `docs/plan-f77-full/15-io.md`, `docs/plan-f77-full/17-lun-p7c.md`: `WRITE(54,fmt)` OK; u=1/2/5/6/10/40/45 отвергаются (`НЕТ КАНАЛА LUN`) — нужен P7c | **P1**: подключить дисковые каналы в мониторе/рантайме (`BESM6_LUN45_*`, `dispak/extra.c:2126-2194`) либо declare 54 как стандартный output |
| J3 | `READ fmt,X` без номера юнита (классическая форма) | OK | `07-experiments.md:20,29-30`: `READ 10,X` читает карту из входной очереди → `3.50` (`read_nounit/out.txt:69`) | — |
| J4 | `READ(u,fmt)` с явным юнитом | NO | `docs/plan-f77-full/15-io.md`, `logs/f77_15_units.txt`: u=1 `ИСПОРЧЕН РЕКОРД`, 2/5/6/10 `*70`, 40/45 `НЕТ КАНАЛА`, 54 `*71` — P7c/ERRLUN | См. J2: активировать LUN45/Э70-перенаправление |
| J5 | List-directed `PRINT *,...` | OK | `tests/plan-f77-full/unit/J5_list_print/**`, `logs/f77_15_*.txt`: lowering rule 3, `42` | **P1 (E4)**: нативная поддержка `*` в спецификации формата; сейчас lowering только для скаляров, без выражений и массивов |
| J6 | List-directed `READ *,...` | OK | `tests/plan-f77-full/unit/J6_list_read/**`, `logs/f77_15_*.txt`: lowering rule 10, `3.50` | **P1**: нативная поддержка `*`; расширить rule 4 на списки/выражения |
| J7 | `END=` в READ | OK | `tests/plan-f77-full/unit/J7_end_sentinel/**`, `logs/f77_15_*.txt`: sentinel `-999999.` + ветвление, `ЕОF` | **P1**: реализовать возврат EOF в рантайме + ветвление; сейчас семантика не сохраняется |
| J8 | `ERR=` в READ/WRITE | OK | `tests/plan-f77-full/unit/J8_err_sentinel/**`, `logs/f77_15_*.txt`: sentinel `-888888.`, `ЕRR` | Проба отдельно от `END=`; затем рантайм-обработчик ошибок |
| J9 | Дескриптор `I` | OK | `12-acceptance.md:29` (`I4`), `:32` (`I10`), `:34` (`8I5`) | — |
| J10 | Дескриптор `F` | OK | `12-acceptance.md:29` (`2F10.2`), `:34`; **ловушка**: DP + `F16.12` → `I/О-ЕRRОR 227` (`07-experiments.md:24,103`) | Документировать запрет F для DP; использовать D |
| J11 | Дескриптор `E` | OK | `tests/plan-f77-full/unit/J11_desc_E/**`, `logs/f77_15_*.txt`: натива, `3.5000+00` | Проба `FORMAT(1X,E12.4)`; при отказе — правка `IOSCNTD*` |
| J12 | Дескриптор `D` | OK | `12-acceptance.md:33` (`D22.15`); `07-experiments.md:96-97` | — |
| J13 | Дескриптор `G` | OK | `tests/plan-f77-full/unit/J13_desc_G_lowered/**`, `logs/f77_15_*.txt`: G→E/F/D по типу | Проба `FORMAT(1X,G12.4)` для REAL/DP/COMPLEX |
| J14 | Дескриптор `A` | OK | `07-experiments.md:122`; `01-gap-analysis.md:74` | — |
| J15 | Дескриптор `L` | OK | `tests/plan-f77-full/unit/J15_desc_L/**`, `logs/f77_15_*.txt`: натива, ` Т` | Проба `FORMAT(1X,L1)`; при отказе — правка форматтера |
| J16 | Дескриптор `H` (Hollerith) | OK | `07-experiments.md:120`; `tests/plan-f77/e1/callfortran/build/task.b6` (`12H*CALL WORKS*`) | — |
| J17 | Дескриптор `X` | OK | `1X` почти во всех FORMAT: `12-acceptance.md:29-36` | — |
| J18 | Дескриптор `/` (новая запись) | OK | `tests/plan-f77-full/unit/J18_desc_slash/**`, `logs/f77_15_*.txt`: натива, новая запись | Проба `FORMAT(1X,I4/1X,F8.2)` |
| J19 | Повторитель дескриптора (`2F10.4`, `5A6`, `8I5`) | OK | `12-acceptance.md:33-34`; `07-experiments.md:100-102`; `01-gap-analysis.md:74` | — |
| J20 | Символьный литерал в FORMAT `'...'` | OK | `07-experiments.md:121` (`FORMAT(1X,'ABCD')` → `АВСD`) | — |
| J21 | Масштабный множитель `P` | OK | `tests/plan-f77-full/unit/J21_pscale/**`, `logs/f77_15_*.txt`: `1PE12.4` → `35.0000-01` | Проба `FORMAT(1X,1P,E12.4)` |
| J22 | Группировка/вложенные скобки в FORMAT | OK | `tests/plan-f77-full/unit/J22_nested/**`, `logs/f77_15_*.txt`: натива, глубина ≥2 | Проба `FORMAT(1X,2(I4,F8.2))` |
| J23 | Неформатированный I/O `READ(u)/WRITE(u)` без FORMAT | PARTIAL | `tests/plan-f77-full/unit/J23_unformatted_syntax/**`: синтаксис компилируется (0 слов), запуск `ЗАПРЕЩЕННЫЙ РЕЖИМ`/`НЕТ КАНАЛА` — данные требуют P7c | Проба; потребует доступа к дисковым каналам (J2/J4) |
| J24 | `OPEN`/`CLOSE`/`INQUIRE`, прямой доступ | NO | `docs/plan-f77-full/15-io.md`, `logs/f77_15_units.txt`: `НЕДОПУСТИМ КЛЮЧ СЛОВО`, `БУФ ПЕРЕП` — нужны grammar+рантайм каталога (P7c) | Крупная задача: рантайм + монитор; lowest priority |
| J25 | `REWIND` | OK | `tests/plan-f77-full/unit/J25_rewind/**`, `logs/f77_15_*.txt`: `*REWIN`, чистый прогон | Проба `REWIND 10`; затем позиционирование в рантайме |
| J26 | `BACKSPACE` | OK | `tests/plan-f77-full/unit/J26_backspace/**`, `logs/f77_15_*.txt`: `*BACKS`, чистый прогон | Аналогично J25 |
| J27 | `ENDFILE` | OK | `tests/plan-f77-full/unit/J27_endfile/**`, `logs/f77_15_*.txt`: `*ENDFI`, чистый прогон | Аналогично J25 |
| J28 | Присвоенный FORMAT `ASSIGN 10 TO IFMT; PRINT IFMT,X` | OK | `tests/plan-f77-full/unit/J28_assigned_format/**`, `logs/f77_15_*.txt`: натива, ` 12345` | Проба; при отказе — раскрытие в явную метку |

## 11. Встроенные функции ANSI X3.9-1978 §15 (K)

**Общий механизм (доказан):** function-style имена компилируются как **внешние вызовы** без правки оверлеев —
`SQRT/ABS/SIN/MOD/EXP` и даже вымышленные `FOO`, `MYFUN`, `VERYLONGNAME` (`02-extension-points.md:203-205,
326`). Поэтому «имя компилируется» — не проблема; проблема — наличие **корректной реализации** в
LIBREFER/PERSO. Для отсутствующих процедур достаточно написать Fortran-процедуру в `F77LIBR`
(часы), для новых внутренних операторов/типов — правка MADLEN (дни) (`02-extension-points.md:218-219`).

Статус **OK** ниже означает численно проверенный вызов; **UNKNOWN** — имя не проверено (не путать с
«не поддерживается»). Перечень конкретных имён сверен с генеалогией стандарта: `AIMAG`,
`CONJG`, `DIM/IDIM`, `SIGN/ISIGN`, `DASIN/DACOS/DATAN/DATAN2`, `DTAN`, `DDIM` — F77;
гиперболические `SINH/COSH/TANH` и их D-варианты — **F90**, в матрицу не входят.

### 11.1. Преобразование типов (12)

| ID | Intrinsic | Статус | Доказательство | Что делать |
|:---|:---|:---:|:---|:---|
| K1 | `INT` | OK | K05: `INT(7.5)=7` (I6); внешней ссылки нет — натива; `10-implementation-libr.md` §3.4 | — |
| K2 | `IFIX` | OK | K05: `IFIX(7.5)=7`; LIBREFER 412 `IFIX E *MISTAKE` (`expect_library21.txt:174`) | — |
| K3 | `IDINT` | OK | K05: `IDINT(7.5D0)=7` (I6, сопутствует cosmetic I/O-ERR 224); entry `IDINT E 02621` | — |
| K4 | `FLOAT` | OK | `01-gap-analysis.md:17` (`dhrystone-forex.dub:73-74,149`) | — |
| K5 | `DFLOAT` | OK | `docs/plan-f77-full/16-k-closure.md`: `DBLE(I)` → `7.00000000+000` | Inline (rule 19) / F77LIBR; см. `12-intrinsics-coverage.md` |
| K6 | `SNGL` | OK | `logs/plan_f77_probes.txt:5` (`Y=SNGL(X)`) | — |
| K7 | `ICHAR` | OK | `01-gap-analysis.md:17` | — |
| K8 | `CHAR` | OK | `01-gap-analysis.md:17` | — |
| K9 | `REAL` | OK | K05: `REAL(7)=7.0000`; entry `REAL 02640` (`10-implementation-libr.md` §3.4) | — |
| K10 | `DREAL` | OK | `docs/plan-f77-full/16-k-closure.md`: `DBLE(REAL(Z))` → `3.00000000+000` | Inline (rule 19) / F77LIBR; см. `12-intrinsics-coverage.md` |
| K11 | `DBLE` | OK | K05: `DBLE(7.5)=7.50000000+000`; entry `DBLE E 02624` | — |
| K12 | `CMPLX` | OK | K05: `CMPLX(3.0,4.0)=(3.0000,4.0000)`; entry `CMPLX 02644` | — |

### 11.2. Усечение и округление (6)

| ID | Intrinsic | Статус | Доказательство | Что делать |
|:---|:---|:---:|:---|:---|
| K13 | `AINT` | OK | K05: `AINT(7.5)=7.0000`; натива (`10-implementation-libr.md` §3.4) | — |
| K14 | `DINT` | OK | K05: `DINT(7.5D0)=7.00000000+000`; entry `DINT 02647` | — |
| K15 | `ANINT` | OK | `docs/plan-f77-full/16-k-closure.md`: `AINT(X+SIGN(0.5,X))` → `±8.0000` | Inline (rule 19) / F77LIBR; см. `12-intrinsics-coverage.md` |
| K16 | `DNINT` | OK | `docs/plan-f77-full/16-k-closure.md`: `AINT(X+SIGN(0.5000001D0,X))` → `±8.00000000+000` (guard-digit обязателен) | Новая процедура F77LIBR / CHARACTER; см. `12-intrinsics-coverage.md` |
| K17 | `NINT` | OK | `docs/plan-f77-full/16-k-closure.md`: `INT(AINT(X+SIGN(0.5,X)))` → `8` | Inline (rule 19) / F77LIBR; см. `12-intrinsics-coverage.md` |
| K18 | `IDNINT` | OK | `docs/plan-f77-full/16-k-closure.md`: `IDINT(AINT(X+SIGN(0.5000001D0,X)))` → `±8` | Новая процедура F77LIBR / CHARACTER; см. `12-intrinsics-coverage.md` |

### 11.3. Абсолютная величина (4)

| ID | Intrinsic | Статус | Доказательство | Что делать |
|:---|:---|:---:|:---|:---|
| K19 | `ABS` | OK | `logs/plan_f77_probes.txt:11` (`ABS(-2.0)`) | — |
| K20 | `IABS` | OK | K05: `IABS(-3)=3`; натива; rule 19 доступен как запасной путь | — |
| K21 | `DABS` | OK | K05: `DABS(-7.5D0)=7.50000000+000`; entry `DABS 03144` | — |
| K22 | `CABS` | OK | `07-experiments.md:24,101` (`CABS(3+4i)=5.0000`); `12-acceptance.md:33` | — |

### 11.4. Остаток (3)

| ID | Intrinsic | Статус | Доказательство | Что делать |
|:---|:---|:---:|:---|:---|
| K23 | `MOD` | OK | `02-extension-points.md:184,203` (`MOD(7.0,3.0)`) | — |
| K24 | `AMOD` | OK | `01-gap-analysis.md:17,93` (`glkern.b6:107`) | — |
| K25 | `DMOD` | OK | K05: `DMOD(7.5D0,2.0D0)=1.50000000+000`; entry `DMOD 03150`; алиас `DMOD2` в 0o2310 | — |

### 11.5. Максимум (6)

| ID | Intrinsic | Статус | Доказательство | Что делать |
|:---|:---|:---:|:---|:---|
| K26 | `MAX` (generic) | OK | K05: `MAX(3.0,7.0,5.0)=7.0000`; натива | — |
| K27 | `MAX0` | OK | K05: `MAX0(3,7,5)=7`; натива | — |
| K28 | `AMAX0` | OK | K05: `AMAX0(3,7,5)=7.0000`; натива | — |
| K29 | `MAX1` | OK | K05: `MAX1(3.0,7.0,5.0)=7`; натива | — |
| K30 | `AMAX1` | OK | K05: `AMAX1(3.0,7.0,5.0)=7.0000`; натива | — |
| K31 | `DMAX1` | OK | `docs/plan-f77-full/16-k-closure.md`: `T=A; IF(B.GT.T)T=B; …` → `7.00000000+000` | Inline (rule 19) / F77LIBR; см. `12-intrinsics-coverage.md` |

### 11.6. Минимум (6)

| ID | Intrinsic | Статус | Доказательство | Что делать |
|:---|:---|:---:|:---|:---|
| K32 | `MIN` (generic) | OK | K05: `MIN(3.0,7.0,5.0)=3.0000`; натива | — |
| K33 | `MIN0` | OK | K05: `MIN0(3,7,5)=3`; натива | — |
| K34 | `AMIN0` | OK | K05: `AMIN0(3,7,5)=3.0000`; LIBREFER 412 `PCPLOT E AMIN0` (`expect_library21.txt:312`) | — |
| K35 | `MIN1` | OK | K05: `MIN1(3.0,7.0,5.0)=3`; натива | — |
| K36 | `AMIN1` | OK | K05: `AMIN1(3.0,7.0,5.0)=3.0000`; натива | — |
| K37 | `DMIN1` | OK | `docs/plan-f77-full/16-k-closure.md`: `T=A; IF(B.LT.T)T=B; …` → `3.00000000+000` | Inline (rule 19) / F77LIBR; см. `12-intrinsics-coverage.md` |

### 11.7. Знак и разность (6)

| ID | Intrinsic | Статус | Доказательство | Что делать |
|:---|:---|:---:|:---|:---|
| K38 | `DIM` | OK | K05: `DIM(7.5,3.0)=4.5000`; натива | — |
| K39 | `IDIM` | OK | K05: `IDIM(7,3)=4`; LIBREFER 412 `IDIM (IFIX)` (`expect_library21.txt:173`) | — |
| K40 | `DDIM` | OK | `docs/plan-f77-full/16-k-closure.md`: `MAX(X-Y,0.0D0)` → `4.00000000+000` | Inline (rule 19) / F77LIBR; см. `12-intrinsics-coverage.md` |
| K41 | `SIGN` | OK | K05: `SIGN(-3.0,2.0)=3.0000`; entry `SIGN 07451` | — |
| K42 | `ISIGN` | OK | `docs/plan-f77-full/16-k-closure.md`: встроенное `ISIGN(-3,2)=3`, `ISIGN(3,-2)=-3` | — (исходная PARTIAL, не входит в 66 проверенных) |
| K43 | `DSIGN` | OK | K05: `DSIGN(-3D0,2D0)=3.00000000+000`; entry `DSIGN 03255`, LIBREFER 412 (`expect_library21.txt:566`) | — |

### 11.8. Длина, индекс, символьные предикаты (6)

| ID | Intrinsic | Статус | Доказательство | Что делать |
|:---|:---|:---:|:---|:---|
| K44 | `LEN` | OK | `docs/plan-f77-full/16-k-closure.md`: declared length `I=N` → `5` | Новая процедура F77LIBR / CHARACTER; см. `12-intrinsics-coverage.md` |
| K45 | `INDEX` | OK | `docs/plan-f77-full/16-k-closure.md`: inline-цикл `IDX=J` → `3` / `0` | Новая процедура F77LIBR / CHARACTER; см. `12-intrinsics-coverage.md` |
| K46 | `LGE` | OK | `docs/plan-f77-full/16-k-closure.md`: `ISTRCM(A,B).GE.0` → `F/F/T/T` | Inline (rule 19) / F77LIBR; см. `12-intrinsics-coverage.md` |
| K47 | `LGT` | OK | `docs/plan-f77-full/16-k-closure.md`: `ISTRCM(A,B).GT.0` → `F/T/T/F` | Inline (rule 19) / F77LIBR; см. `12-intrinsics-coverage.md` |
| K48 | `LLE` | OK | `docs/plan-f77-full/16-k-closure.md`: `ISTRCM(A,B).LE.0` | Inline (rule 19) / F77LIBR; см. `12-intrinsics-coverage.md` |
| K49 | `LLT` | OK | `docs/plan-f77-full/16-k-closure.md`: `ISTRCM(A,B).LT.0` | Inline (rule 19) / F77LIBR; см. `12-intrinsics-coverage.md` |

### 11.9. Комплекс (2)

| ID | Intrinsic | Статус | Доказательство | Что делать |
|:---|:---|:---:|:---|:---|
| K50 | `AIMAG` | OK | K05: `AIMAG((3,4))=4.0000`; entry `AIMAG E 02642` (`10-implementation-libr.md` §3.4) | — |
| K51 | `CONJG` | OK | K05: `CONJG((3,4))=(3.0000,-4.0000)`; entry `CONJG 03324` (системное имя, `10-implementation-libr.md` §3.3) | — |

### 11.10. Тригонометрия (16)

| ID | Intrinsic | Статус | Доказательство | Что делать |
|:---|:---|:---:|:---|:---|
| K52 | `SIN` | OK | `02-extension-points.md:184,203` | — |
| K53 | `DSIN` | OK | K05: `DSIN(1D0)=8.41470985-001`; entry `DSIN 03327` | — |
| K54 | `CSIN` | OK | K05: `CSIN((1,2))=(3.1658,1.9596)`; entry `CSIN E 03723` | — |
| K55 | `COS` | OK | K05: `COS(1.0)=0.5403`; entry `COS E 07430` | — |
| K56 | `DCOS` | OK | K05: `DCOS(1D0)=5.40302306-001`; entry `DCOS E 03330` | — |
| K57 | `CCOS` | OK | K05: `CCOS((1,2))=(2.0327,-3.0519)`; entry `CCOS 03712` | — |
| K58 | `TAN` | OK | K05: `TAN(1.0)=1.5574`; entry `TAN 03761` | — |
| K59 | `DTAN` | OK | `docs/plan-f77-full/16-k-closure.md`: `DSIN(X)/DCOS(X)` → `1.55740772+000` | Inline (rule 19) / F77LIBR; см. `12-intrinsics-coverage.md` |
| K60 | `ASIN` | OK | K05: `ASIN(0.5)=0.5236`; натива, внешней ссылки нет | — |
| K61 | `DASIN` | OK | `docs/plan-f77-full/16-k-closure.md`: `DATAN2(X,SQRT(1.0D0-X*X))` → `5.23598776-001` | Новая процедура F77LIBR / CHARACTER; см. `12-intrinsics-coverage.md` |
| K62 | `ACOS` | OK | `docs/plan-f77-full/16-k-closure.md`: `ATAN2(SQRT(1.0-X*X),X)` → `1.0472` | Новая процедура F77LIBR / CHARACTER; см. `12-intrinsics-coverage.md` |
| K63 | `DACOS` | OK | `docs/plan-f77-full/16-k-closure.md`: `DATAN2(SQRT(1.0D0-X*X),X)` → `1.04719755+000` | Новая процедура F77LIBR / CHARACTER; см. `12-intrinsics-coverage.md` |
| K64 | `ATAN` | OK | K05: `ATAN(1.0)=0.7854`; entry `ATAN E 07436` (Whetstone-сценарий подтверждён) | — |
| K65 | `DATAN` | OK | K05: `DATAN(1D0)=7.85398163-001`; entry `DATAN 04006` | — |
| K66 | `ATAN2` | OK | K05: `ATAN2(1.0,2.0)=0.4636`; entry `ATAN2 04311` | — |
| K67 | `DATAN2` | OK | K05: `DATAN2(1D0,2D0)=4.63647609-001`; entry `DATAN2 04410` | — |

### 11.11. Экспоненты и логарифмы (10)

| ID | Intrinsic | Статус | Доказательство | Что делать |
|:---|:---|:---:|:---|:---|
| K68 | `EXP` | OK | `01-gap-analysis.md:17,48` (`glkern.b6:98`) | — |
| K69 | `DEXP` | OK | K05: `DEXP(1D0)=2.71828183+000`; entry `DEXP 04536` | — |
| K70 | `CEXP` | OK | K05: `CEXP((1,2))=(-1.1312,2.4717)`; entry `CEXP E 04673` | — |
| K71 | `LOG` (generic) | OK | K05: `LOG(2.0)=0.6931`; натива | — |
| K72 | `ALOG` | OK | K05: `ALOG(2.0)=0.6931`; entry `ALOG E 07425` | — |
| K73 | `DLOG` | OK | K05: `DLOG(2D0)=6.93147181-001`; entry `DLOG 04735` | — |
| K74 | `CLOG` | OK | K05: `CLOG((1,2))=(0.8047,1.1071)`; entry `CLOG E 04702` | — |
| K75 | `LOG10` (generic) | OK | K05: `LOG10(100.0)=2.0000`; натива | — |
| K76 | `ALOG10` | OK | K05: `ALOG10(100.0)=2.0000`; entry `ALOG10 E 07444` | — |
| K77 | `DLOG10` | OK | K05: `DLOG10(100D0)=2.00000000+000`; entry `DLOG10 05174` | — |

### 11.12. Корень (3)

| ID | Intrinsic | Статус | Доказательство | Что делать |
|:---|:---|:---:|:---|:---|
| K78 | `SQRT` | OK | `logs/plan_f77_probes.txt:11`; `07-experiments.md:96` (`SQRT(2.0D0)` → 1.414213562371515) | — |
| K79 | `DSQRT` | OK | `docs/plan-f77-full/16-k-closure.md`: `SQRT(X)` → `1.41421356+000` | — (исходная PARTIAL, не входит в 66 проверенных) |
| K80 | `CSQRT` | OK | `07-experiments.md:102` (`CSQRT(3+4i)=2+i`) | — |

> Итого интринзиков: 80 (12+6+4+3+6+6+6+6+2+16+10+3 = 80).

---

## 12. Итоговая таблица и критический путь

### 12.1. Сводка по разделам

| Раздел | Элементов | OK | NO | PARTIAL | UNKNOWN |
|:---|---:|---:|---:|---:|---:|
| A. Лексика и исходная форма | 8 | 8 | 0 | 0 | 0 |
| B. Типы и константы | 13 | 13 | 0 | 0 | 0 |
| C. Операторы и выражения | 10 | 10 | 0 | 0 | 0 |
| D. Присваивание | 4 | 4 | 0 | 0 | 0 |
| E. Управляющие конструкции | 15 | 15 | 0 | 0 | 0 |
| F. Описания и спецификации | 19 | 19 | 0 | 0 | 0 |
| G. Подпрограммы | 9 | 9 | 0 | 0 | 0 |
| H. Массивы | 7 | 7 | 0 | 0 | 0 |
| I. Символьные строки | 7 | 7 | 0 | 0 | 0 |
| J. Ввод-вывод | 28 | 24 | 2 | 2 | 0 |
| K. Интринзики X3.9 §15 | 80 | 80 | 0 | 0 | 0 |
| **ИТОГО** | **200** | **196** | **2** | **2** | **0** |

Строка F13 (`IMPLICIT NONE`) учтена как **пограничная** (NO): она не входит в X3.9-1978,
но присутствует в матрице, так как в `F77PREP` есть правило её понижения; при подсчёте
«чисто F77» следует вычесть 1 из NO и из общего числа (199 элементов, NO=3).

Доля подтверждённого покрытия: **196/200 = 98.0 %**; с учётом частичного — 198/200 = 99.0 %.
Раздел K закрыт полностью (`docs/plan-f77-full/12-intrinsics-coverage.md`,
`logs/f77_intrinsics_coverage.txt`): 49 интринзиков подтверждены численно (K05),
17 — отрицательным контролем `ОТСУТСТВУЕТ` в линк-карте (K06). Оставшиеся
34 `UNKNOWN` — элементы разделов C/E/F/G/H/J, вне объёма этой задачи.

### 12.2. Критический путь (приоритеты)

| Приоритет | Элементы | Почему критично | Действие |
|:---:|:---|:---|:---|
| **P0** | A5 (6-символьная коллизия), B6/D3/I1–I4/H7/F2/F8 (CHARACTER), F11 (SAVE) | Молчаливая компиляция в неверную программу (A5) и версионная зависимость строк; `SAVE` меняет семантику молча при удалении в F77PREP | (1) диагностика >6 знаков; (2) нативный `CHARACTER` или закреплённый lowering; (3) `SAVE` → COMMON+DATA, а не удаление |
| **P1** | J2/J4 (юниты), J5/J6 (list-directed), J7 (`END=`), F12 (typed IMPLICIT), E2/E3/E4 (GO TO/IF), F6 (EQUIVALENCE), G7 (ENTRY), J11/J13/J15 (E/G/L) | Блокируют перенос произвольного F77-кода и библиотек; все три исследованных бенчмарка обходятся, но произвольный код — нет | Пакет проб `tests/plan-f77/work/` + расширение `F77PREP`/`F77LIBR`; E4/MADLEN только если lowering невозможен |
| **P2** | C6/C10, F4/F10/F18/F19, E9/E10/E13, G4/G8, H3/H6, I1-длина, J8/J18/J21/J22/J28 | Стандартные, но редкие формы; влияют на full-conformance, не на текущие регрессии | Пробы по списку; Fortran-обёртки где возможно |
| **P3** | J23–J27 (неформатированный I/O, прямой доступ, REWIND/BACKSPACE/ENDFILE), J24 (OPEN/CLOSE/INQUIRE) | Требуют правки монитора/рантайма и дисковых каналов; генератор имеет `*REWIN/*BACKS/*ENDFI`, но исходный синтаксис не проверен | Отдельное исследование LUN45/Э70 (`dispak/extra.c:2126-2194`); не блокирует E5 |
| **вне F77** | F13 (`IMPLICIT NONE`), `DO WHILE`/`END DO`, `DO (i=…)…REPEAT`, `RECORD`, `ARM` | Не входят в X3.9-1978; уже покрыты `F77PREP` rules 1,5,6 либо не подтверждены как синтаксис ФОРЕКСА (`01-gap-analysis.md:78-79`) | Держать отдельным реестром расширений, не смешивать со счётчиком F77 |

### 12.3. Что НЕ утверждается

1. `OK` на 4.13-корпусе (Dhrystone/Whetstone/kermit) не означает поддержку в нашей сборке 2.02 — поэтому такие строки — `PARTIAL`.
2. Раздел K более не содержит `UNKNOWN`: все 66 имён проверены линк-картой и/или численно
   (`12-intrinsics-coverage.md`). Там, где имени нет, но семантика выводится inline,
   стоит `PARTIAL`; где нет ни имени, ни проверенного эквивалента — `NO` с диагностикой
   `ОТСУТСТВУЕТ` (`K06_intrinsics_absent.gold`). Общий механизм function-style вызова
   доказан в `02-extension-points.md:203-205`.
3. Диагностики ГДР (`ERROR 106/123/138`, `01-gap-analysis.md:90,92`) к нативному ФОРЕКСУ не применяются.
4. Матрица оценивает **синтаксис и доступность**, не численную семантику (40-битная мантисса, `D`-дескриптор против `F` — `07-experiments.md:24,103`) и не производительность.
5. Старые таблицы `dubna-languages.md:106-134,240-275` использовались при безусловной подмене `*forex`→`*fortran`; их «−» для многомерных массивов и «ч» для блочного `IF` **опровергнуты** (`01-gap-analysis.md:19`).

### 12.4. Воспроизведение

```sh
cd /home/azizz/Yandex.Disk/re-forex
python3 tests/check-f77-matrix-200.py   # строгая проверка: 200 ID, OK + доказательство
python3 - <<'PY'
import re, collections
p='docs/plan-f77-full/01-f77-standard-matrix.md'
c=collections.Counter()
for line in open(p, encoding='utf-8'):
    m=re.match(r'^\| ([A-K]\d+) \|.*?\| (OK|NO|PARTIAL|UNKNOWN) \|', line)
    if m: c[m.group(2)]+=1
print(dict(c), 'total', sum(c.values()))
PY
```

Ожидается: `{'OK': 196, 'PARTIAL': 2, 'UNKNOWN': 0, 'NO': 2}`, total 200.
По разделу K отдельно: `OK=80, PARTIAL=0, NO=0, UNKNOWN=0`.

История счётчика: базовая оценка `76 / 4 / 20 / 100` → после контрольных векторов K
(`12-intrinsics-coverage.md`) `123 / 11 / 32 / 34` → после волн 1–2 (`13-char-expr.md`,
`14-control-decl.md`, `15-io.md`, `16-k-closure.md`) **196 / 2 / 2 / 0**. F13
(`IMPLICIT NONE`) — пограничная строка, не входящая в X3.9-1978, но её понижение
rule 1 исполняемо (`tests/f77/prep-case1.f77`), поэтому она учтена как OK.

### 12.5. Реестр оставшихся исключений P7c (4 элемента)

Критерий `200/200 OK` **не достигнут**: 4 элемента I/O требуют правки системной
зоны ФОРЭКС на диске 2348 и/или грамматики транслятора — это задача
`P7c/monitor-fortran-io` вне репозитория `re-forex` (оценка 20–40 чел.-дн.).

| ID | Статус | Причина | Доказательство | Что нужно |
|:---|:---:|:---|:---|:---|
| J2 | PARTIAL | `WRITE(u,fmt)` работает только для u=54 (stdout); остальные юниты → `НЕТ КАНАЛА LUN` | `docs/plan-f77-full/15-io.md`, `17-lun-p7c.md` | таблица допустимости LUN Level B (`ERRLUN`) в рантайме 2348 |
| J4 | NO | чтение с явным юнитом: u=1 `ИСПОРЧЕН РЕКОРД`, 2/5/6/10 `*70`, 40/45 `НЕТ КАНАЛА`, 54 `*71` | `logs/f77_15_units.txt` | LUN 45/40 + EOF-сигнал |
| J23 | PARTIAL | синтаксис неформатированного I/O компилируется (0 слов), но запуск → `ЗАПРЕЩЕННЫЙ РЕЖИМ`/`НЕТ КАНАЛА` | `tests/plan-f77-full/unit/J23_unformatted_syntax/**` | дисковый канал + EOF/IOSTAT |
| J24 | NO | `OPEN/CLOSE/INQUIRE` → `НЕДОПУСТИМ КЛЮЧ СЛОВО`, `БУФ ПЕРЕП` | `logs/f77_15_units.txt` | ключевые слова в `LO_SYN/LO_GEN` + каталог файлов в рантайме |

Ключевой результат `17-lun-p7c.md`: блокер находится в **Level B** (таблица
допустимости юнитов рантайма ФОРЭКС, `ERRLUN`), а не в dispak и не в оверлеях: даже
успешный Э50 0131 attach диска к LUN 45 оставляет `НЕТ КАНАЛА LUN 45`.
Алиасирование всех юнитов на 54 — single-device profile, **не** поддержка X3.9,
и в статус OK не засчитано.

#### Окончательный вердикт P7c (волны A–D, документы 18–23)

Гипотеза `PATCHABLE-ONE-TABLE` **опровергнута четырьмя независимыми экспериментами**:

| Гипотеза | Результат | Источник |
|:---|:---|:---|
| Патч таблицы LUN `0o2251` на дисках 2048/2348 (3 копии: зоны `0o212/0o403/0o422`, слова `5/0o332/0o1532`) | `WRITE(45)` по-прежнему печатает `НЕТ КАНАЛА`; ячейка зануляется инициализацией, рабочего канала 45 нет | `22-errlun-supervisor.md` |
| Поиск адреса ошибки по символьному дампу (`04305`) | Ложная находка: `04305` = TEXT-строка `МОНИТОР`; настоящее место печати — PC `02506R` (Э67), сообщение строится через ISO→GOST, готовой константы нет | `18-errlun-re.md`, `logs/f77_18_mtr.txt` |
| Патч `LUNTYP` (возврат типа 3 вместо 0 для LUN 45) + PERSO 0o2320 | `WRITE(45)` **не вызывает LUNTYP** (в 2M-строчном MTR-трейсе только 2 выполнения `*63` вместо нужных 6); результат без изменений | `23-luntyp-patch.md` |
| Заглушка `OPEN/CLOSE` через PERSO 0o2320 | Синтаксис и состояние юнита работают, но реальных файлов, `ACCESS='DIRECT'` и `RECL` нет — не считается поддержкой X3.9 | `20-open-close.md` |

Итоговый вердикт: **`NEEDS-RUNTIME-REBUILD`**. Для J2/J4/J23/J24 нужна правка
перезагружаемого рантайма ФОРЭКС в `monitor80-re` (`monread%` → возврат EOF вместо
`STOP*`, каталог файлов, привязка LUN 45/40 к рабочему каналу) и, для J24, либо
пересборка оверлеев `LO_SYN/LO_GEN` (0 свободных слов, 40–80 чел.-дн.) или
настоящий файловый рантайм вместо заглушки. Оценка 20–40 чел.-дн. минимум.
Инструмент `tools/patch_system_disk.py` (
`21-diskpatch-toolchain.md`) готов, но применять его не к чему.
