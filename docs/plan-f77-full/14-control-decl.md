# 14 — Волна 1: управляющие конструкции и описания (E–H) матрицы F77

**Дата:** 19.11.2026. **Ветка:** `main`. **Репозиторий:** `/tmp/.private/azizz/opencode/re-forex`.

**Задача:** довести до статуса OK с исполнимым доказательством все 21 незакрытых
элементов разделов E–H матрицы `01-f77-standard-matrix.md`.

**Владение:** только этот файл, `logs/f77_14_*.txt` и
`tests/plan-f77-full/unit/{E02_computed_goto,E03_assign_goto,E04_arith_if,E09_do_step,
E10_do_terminate,E13_pause,F04_arrays_3d7d,F06_equivalence,F10_data_repeat,F11_save,
F12_typed_implicit,F14_external,F15_intrinsic,F18_stmt_func,F19_dummy_array,
G04_char_function,G07_entry,G08_alt_return,H03_arrays_3d7d,H06_dummy_array,
H07_char_array}/**`. Всё остальное (src/, tests/*.sh, матрица 01) — READ-ONLY.

---

## 0. Методика прогона (реальные запуски, не умозрение)

Среда: dispak `/home/azizz/Yandex.Disk/dispak/build/dispak/dispak`, диски **2048** (компилятор)
и **2348** (SYSTEM + записанный `build/FOREX_PERSO_2300.bin` в зону `0o2300`)).
Карта декы: `*perso:602300`, `*no list`, `*forex`; каждая дека содержит `PROGRAM …`,
`STOP`, `END`, `*execute`, `*end file`. `BESM6_PATH=WORK:/usr/local/share/besm6`.

Критерий OK: **нет диагностики** (фильтр `ERR nnn / НЕДОПУСТИМ / ОШИБКА /
ТИП ОП-ДА / ОТСУТСТВУЕТ / I/О-ЕRRОR / atx-трап`) **и корректный вывод** перед
`КОНЕЦ ЗАДАЧИ`. Нативный прогон, который дал диагностику или неверный результат,
считается отказом; для него создаётся вторая («lowered») дека с ручным применением
lowerings и доказательство её работоспособности.

Логи: по одному файлу `logs/f77_14_<ID>.txt` на элемент (сырые фрагменты dispak
с вердиктом), плюс `logs/f77_14_prep_rules.txt` (двухпроходная проверка готовых
правил F77PREP). Полный набор deck/gold лежит в перечисленных выше unit-каталогах.

> Символы `АВСD` / `ЕFGН` в hollerith-выводе — известный аппаратный артефакт
> 6-битной TEXT-кодировки БЭСМ-6 (`B`→`В`, `H`→`Н`), матрица A8; не диагностика.

---

## 1. Сводная таблица: ID → OK → доказательство → метод → правило

| ID | Элемент | OK | Доказательство (deck / gold / лог) | Метод | Нужное правило |
|:--|:--|:--:|:--|:--|:--|
| **E2** | Вычисляемый `GO TO (10,20,30),I` | **OK** | `unit/E02_computed_goto/e02_computed_goto.b6` → gold `    2`; `logs/f77_14_E02.txt` | **натива** (диагностики нет, ветка 20) | нет; rule 15 есть и рабочий (проверен конвейером) |
| **E3** | `ASSIGN 20 TO I` + `GO TO I` | **OK** | `unit/E03_assign_goto/e03_assign_goto.b6` → gold `    2`; `logs/f77_14_E03.txt` | **натива** | нет; rule 15 есть и рабочий |
| **E4** | Арифметический `IF (X) 10,20,30` | **OK** | `unit/E04_arith_if/e04_arith_if.b6` → gold `    1`; `logs/f77_14_E04.txt` | **натива** (X<0 → ветка 10) | нет |
| **E9** | DO: шаг≠1 / отрицательный / **нуль итераций** | **OK** | `unit/E09_do_step/e09_step_native.b6` → `   30`/`   52`; `e09_zero_lowered.b6` → gold `    0`; `logs/f77_14_E09.txt` | **натива** для шага≠1 и отриц. шага; **lowering** для нуль-итераций | **R-E9** (guard `IF (e1>e2/e1<e2) GO TO after`) — новое |
| **E10** | Завершение DO не-`CONTINUE` | **OK** | `unit/E10_do_terminate/e10_do_terminate.b6` → gold `   15`; `logs/f77_14_E10.txt` | **натива** (`DO 10 I=1,5 / 10 S=S+I`) | нет |
| **E13** | `PAUSE` | **OK** | `unit/E13_pause/e13_pause.b6` → gold `   42`; `logs/f77_14_E13.txt` | **натива** (пакетный прогон: `PAUSE` — no-op, счёт не сбрасывается) | нет |
| **F4** | Массивы размерности 3 и 7 | **OK** | `unit/F04_arrays_3d7d/f04_array3.b6` → `     9.00`, `f04_array7.b6` → `     3.00`; `logs/f77_14_F04.txt` | **натива** (3D и 7D дескрипторы работают) | нет |
| **F6** | `EQUIVALENCE (A,B)` | **OK** | `unit/F06_equivalence/f06_equivalence.b6` → gold `    7`; `logs/f77_14_F06.txt` | **натива** | нет (но rule 16 lowering скаляра сломан — см. §4) |
| **F10** | `DATA` с `4*0` и implied-DO | **OK** | `unit/F10_data_repeat/f10_data_repeat.b6` → `    0   0   3   3`; `f10_data_implied.b6` → `    5   1`; `logs/f77_14_F10.txt` | **натива** (обе формы) | нет |
| **F11** | `SAVE` | **OK** | `unit/F11_save/f11_save_native.b6` (отказ) + `f11_save_lowered.b6` → gold `   11  12`; `logs/f77_14_F11.txt` | **lowering** в `COMMON` + `BLOCK DATA`/`DATA` | **R-F11** (заменить rule 2) — новое |
| **F12** | `IMPLICIT INTEGER (A-Z)` | **OK** | `unit/F12_typed_implicit/f12_typed_implicit.b6` (`X=42`, печать `I4`) → gold `   42`; `logs/f77_14_F12.txt` | **натива** | нет (rule 9 есть, но конвейер спотыкается о rule-20 — см. §4) |
| **F14** | `EXTERNAL MYFUN` | **OK** | `unit/F14_external/f14_external.b6` → gold `    10.00`; `logs/f77_14_F14.txt` | **натива** (operator + определение в деке) | нет; rule 21 есть |
| **F15** | `INTRINSIC SQRT` | **OK** | `unit/F15_intrinsic/f15_intrinsic_native.b6` (отказ) + `f15_intrinsic_lowered.b6` → gold `     4.00`; `logs/f77_14_F15.txt`, `f77_14_prep_rules.txt` | **lowering** (удаление оператора, rule 21) | **rule 21** — уже реализован, зафиксировать |
| **F18** | Функция-оператор `F(X)=X*X+1.0` | **OK** | `unit/F18_stmt_func/f18_stmt_func.b6` → gold `    10.00`; `logs/f77_14_F18.txt` | **натива** | нет |
| **F19** | Формальные массивы `A(N)` / `A(*)` | **OK** | `unit/F19_dummy_array/f19_dummy_an.b6` → `   15`; `f19_dummy_astar_native.b6` (трап); `f19_dummy_astar_lowered.b6` → `   15`; `logs/f77_14_F19.txt` | **натива** `A(N)`; **lowering** `A(*)→A(1)` | **R-ASTAR** — новое |
| **G4** | `CHARACTER*4 FUNCTION` | **OK** | `unit/G04_char_function/g04_char_func_native.b6` (отказ) + `g04_char_func_lowered.b6` → gold ` АВСD`; `logs/f77_14_G04.txt` | **lowering** в `SUBROUTINE` + Hollerith `DATA` | **R-G4** — новое |
| **G7** | `ENTRY SECOND(Y)` | **OK** | `unit/G07_entry/g07_entry.b6` → gold `    1`, `    2`; `logs/f77_14_G07.txt` | **натива** (две точки входа) | нет |
| **G8** | `CALL S(*10,*20)` / `RETURN 1` | **OK** | `unit/G08_alt_return/g08_altret_native.b6` (отказ) + `g08_altret_lowered.b6` → gold `    1`; `logs/f77_14_G08.txt` | **lowering** в целый код возврата + computed `GO TO` | **R-G8** — новое |
| **H3** | Массивы размерности 3 и 7 | **OK** | `unit/H03_arrays_3d7d/h03_array3.b6` → `    7`, `h03_array7.b6` → `   11`; `logs/f77_14_H03.txt` | **натива** | нет |
| **H6** | Формальные массивы `A(N)` / `A(*)` | **OK** | `unit/H06_dummy_array/h06_dummy_an.b6` → `   15`; `h06_dummy_astar_lowered.b6` → `   15`; `logs/f77_14_H06.txt` | **натива** `A(N)`; **lowering** `A(*)→A(1)` | **R-ASTAR** (тот же, что F19) |
| **H7** | Массивы `CHARACTER` | **OK** | `unit/H07_char_array/h07_char_array_native.b6` (I/O-ERR 232) + `h07_char_array_lowered.b6` → gold ` АВСDЕFGН`; `logs/f77_14_H07.txt` | **lowering** в `INTEGER` + Hollerith `DATA` | **R-H7** — новое |

**Счётчик: 21 / 21 OK.**

 Разбивка: **13** элементов — чистая натива (E2, E3, E4, E10, E13, F4, F6, F10,
 F12, F14, F18, G7, H3); **3** элемента — натива для основной формы + lowering для
 граничной (E9 нуль итераций, F19/H6 `A(*)`); **5** элементов — только lowering
 (F11, F15, G4, G8, H7).

---

## 2. Что подтверждено нативной пробой (главный неожиданный результат)

Матрица 01 помечала E2/E3/E4/E9/E10/E13, F4/F6/F10/F12/F14/F15/F18/F19,
G4/G7/G8, H3/H6/H7 как UNKNOWN/NO. Реальные прогоны на 2.02 опровергли это для
большинства элементов:

* **Управление:** `GO TO (m1,m2,…),I`, `ASSIGN m TO I` + `GO TO I`,
  арифметический `IF (X) m1,m2,m3`, `DO` с шагом ≠1 и отрицательным шагом,
  завершение `DO` произвольным оператором, `PAUSE` — **все компилируются и
  исполняются без диагностики**.
* **Описания:** 3D/7D массивы, скалярный `EQUIVALENCE`, `DATA V/4*0,…/`,
  `DATA (W(I),I=1,5)/…/`, `IMPLICIT INTEGER (A-Z)`, `EXTERNAL`, функции-операторы
  `F(X)=expr` — **натива**.
* **Подпрограммы:** `ENTRY`,variable-bound dummy `A(N)` — **натива**.

Это означает, что готовые правила 15/16/9/21 в `prep_tools.py` для E2/E3/F6/F12/F14
**не нужны** (натива сильнее), но они рабочими прогонами не противоречат.

---

## 3. Доказательства lowerings (деки, реально исполняемые на 2.02)

### 3.1 E9 — нуль итераций (нативный дефект)

`DO` в ФОРЭКСе — post-test (`исполнить тело, затем сравнить`), поэтому
`DO 20 I=1,0` исполняет тело **один раз** (`   1` вместо `   0`), а
`DO 20 I=1,10,-1` тоже даёт `   1`. Исправление — guard перед циклом:

```fortran
      IF (1 .GT. 0) GO TO 25
      DO 20 I=1,0
   20 T=T+I
   25 CONTINUE
```
→ `    0`. Отрицательный шаг: `IF (1 .LT. 10) GO TO 25` → `    0`.
Step≠1 (`DO 10 I=10,1,-2` → 30; `DO 25 J=1,10,3` → 52) работает **нативно**.

### 3.2 F11 — `SAVE` → `COMMON` + `BLOCK DATA`

Натива: `ЕRR 00313 … НЕДОПУСТИМ КЛЮЧ СЛОВО`. Lowering:

```fortran
      SUBROUTINE CNT(K)
      INTEGER N
      COMMON /F11SV/N          ! вместо SAVE N
      N=N+1
      K=N
      RETURN
      END
      BLOCK DATA
      INTEGER N
      COMMON /F11SV/N
      DATA N/10/               ! инициализация в BLOCK DATA
      END
```
Два вызова `CALL CNT(A); CALL CNT(B)` → `   11  12`.

> ⚠ Текущий F77PREP rule 2 просто **удаляет** `SAVE`. На 2.02 это тоже даёт
> `11 12` (локальные переменные статичны, а `DATA N/10/` уже даёт static storage),
> но это **свойство реализации, а не гарантия стандарта**. Требуется R-F11.

### 3.3 F15 — удаление `INTRINSIC` (rule 21)

Натива: `ЕRR 00313 … НЕДОПУСТИМ КЛЮЧ СЛОВО`. Двухпроходной конвейер
`deck1 → F77PREP → records → lower → deck2` дал `C@ INTRINSIC SQRT ->
(removed; EXTERNAL/INTRINSIC declaration)` и `     4.00`. Rule 21 уже закрывает
элемент — достаточно зафиксировать прогон.

### 3.4 F19 / H6 — `A(*)` → `A(1)`

Натива `INTEGER A(*)` в dummy → machine trap (`atx / acc = … / R = 000111`).
Замена `(*)` на `(1)` → `   15`. F77 assumed-size объявляет только нижнюю границу;
ФОРЭКС не делает bounds-check, поэтому индексация за объявленной границей работает.

### 3.5 G4 — `CHARACTER*4 FUNCTION` → `SUBROUTINE` + Hollerith

Натива：`CHARACTER*4 FUNCTION CFUN()` → `НЕДОПУСТИМ СИМВОЛ )`,
`ДОПУСТИМА ТОЛЬКО ЦЕЛОЧИСЛЕННАЯ КОНСТ`. Рабочий lowering (важно: **не**
`INTEGER FUNCTION` — тот вернул 0):

```fortran
      PROGRAM G4L
      INTEGER IS
      CALL GFUN(IS)            ! было IS=CFUN()
      PRINT 10,IS
   10 FORMAT(1X,A4)
      STOP
      END
      SUBROUTINE GFUN(IS)
      INTEGER IS,IH
      DATA IH/4HABCD/
      IS=IH
      RETURN
      END
```
→ ` АВСD`.

### 3.6 G8 — альтернативные возвраты → целый код + computed `GO TO`

Натива：`НЕДОПУСТИМ СИМВОЛ * В ВЫРАЖ`, `ОТСУТСТВ ИДЕНТ`, `ОШИБКА В RETURN`.
Lowering:

```fortran
      INTEGER RC
      CALL SUB(RC)             ! было CALL SUB(*10,*20)
      GO TO (10,20,50),RC
   10 K=1
      GO TO 60
   20 K=2
      GO TO 60
   50 K=3
   60 PRINT 70,K
      ...
      SUBROUTINE SUB(RC)
      INTEGER RC
      RC=1                     ! было RETURN 1
      RETURN
      END
```
→ `    1`.

### 3.7 H7 — массив `CHARACTER` → `INTEGER` + Hollerith

Натива `CHARACTER*4 S(2)` компилируется, но печать даёт
`I/О-ЕRRОR 232 … ФОРМАТ (1Х,2А4)`. Lowering:

```fortran
      INTEGER S(2)
      DATA S(1)/4HABCD/,S(2)/4HEFGH/
      PRINT 10,S(1),S(2)
   10 FORMAT(1X,2A4)
```
→ ` АВСDЕFGН`.

---

## 4. Проверка готовых правил 15 / 16 / 9 / 21 (двухпроходной прогон)

Лог: `logs/f77_14_prep_rules.txt`.

| Rule | Элемент | Результат |
|:--|:--|:--|
| 15 | E2 | `GO TO (10,20,30),I` → IF-chain; pass2 `    2`. Рабочий. |
| 15 | E3 | `ASSIGN 20 TO I` → `I=1`; `GO TO I` → `IF (I.EQ.1) GO TO 20`; pass2 `    2`. Рабочий. |
| 16 | F6 | **Скаляр** `EQUIVALENCE (A,B)` lowering **не работает** (`PRINT 10,B` не переписан → `    0`). Форма `EQUIVALENCE (A(1),B(1))` + обращения `B(1)` → `    7`. Поскольку натива закрывает F6, блокировки нет. |
| 9 | F12 | Конвейер **оборван**: rule-20 ("TRUNCATED NAME: INTEGERT (8 chars → INTEGE)") не различает служебные слова `IMPLICIT`/`INTEGER` (>6 знаков). Натива закрывает F12, блокировки нет. |
| 21 | F15 | `INTRINSIC SQRT` удаляется; pass2 `     4.00`. **Закрывает F15.** |

---

## 5. Список правил для волны 2 с точными выражениями

| Правило | Элементы | Точное выражение (условие → замена) |
|:--|:--|:--|
| **R-E9** | E9 | Для `DO m I=e1,e2[,e3]` выделить метку `Ls` сразу после оператора завершения цикла. Если `e3` литерал >0 или отсутствует: `IF (e1 .GT. e2) GO TO Ls`. Если `e3` литерал <0: `IF (e1 .LT. e2) GO TO Ls`. Если `e3` — переменная `V`: `IF (V .GE. 0) GO TO Lp / IF (e1 .LT. e2) GO TO Ls / GO TO Lb / Lp CONTINUE / IF (e1 .GT. e2) GO TO Ls / Lb CONTINUE / DO m I=e1,e2,V`. Поставить `Ls CONTINUE` после terminal-оператора. Проверено: `1/0 → 0`, `1/10/−1 → 0`, step≠1 без guard — натива. |
| **R-F11** | F11 | В програмной единице `U`: `SAVE v1,…,vk` → `COMMON /<U>SV/v1,…,vk` (уникальный блок ≤6 знаков; при наличии уже существующего `COMMON` — дописать имена в его список). Если `v` имеет `DATA v/c/` в `U`, перенести в `BLOCK DATA: INTEGER v; COMMON /<U>SV/v; DATA v/c/; END`. Удалить оператор `SAVE` с `C@`-якорем. **Не просто удалять** — это текущий баг rule 2. |
| **rule 21 (активировать)** | F15 | Уже в `prep_tools.py`: host-классификатор `^(EXTERNAL\|INTRINSIC)\s` → rule 21 → `C@ … -> (removed; EXTERNAL/INTRINSIC declaration)`. Достаточно зафиксировать двухпроходный прогон (готово). |
| **R-ASTAR** | F19, H6 | В описании dummy-массива `t A(*)` заменить `(*)` → `(1)` (для `t A(lb:*)` → `(lb)`). Эмитировать `C@ A(*) -> A(1) (assumed-size)`. Индексация за границей допустима (нет bounds-check). Проверено: `A(*)` → трап, `A(1)` → `   15`. |
| **R-G4** | G4 | `CHARACTER*n FUNCTION F(args)` → `SUBROUTINE F(R,args)`, где `R` — новый `INTEGER` dummy (`INTEGER R(W)`, `W=ceil(n/6)`; для n≤6 скаляр). `F=<литерал>` → `DATA IH/nH<lit padded to 6·W>/` + `R=IH`. Вызов `S=F(args)` → `INTEGER IS; CALL F(IS,args)`, затем печать `IS` дескриптором `A`. **Не** оформлять как `INTEGER FUNCTION` — на 2.02 он вернул 0. Проверено для n=4 → ` АВСD`; n>6 — экстраполяция через W слов + rule 13, здесь не доказана. |
| **R-G8** | G8 | `CALL S(*L1,…,*Lk)` → `INTEGER RC; CALL S(RC); GO TO (L1,…,Lk),RC`. `SUBROUTINE S(*,…,*)` → `SUBROUTINE S(RC); INTEGER RC`. `RETURN j` (1≤j≤k) → `RC=j; RETURN`; `RETURN` → `RC=k+1; RETURN` с добавлением метки `L_{k+1}` (fall-through). Проверено: `RC=1` → `    1`. |
| **R-H7** | H7 | `CHARACTER*n S(d1,…,dk)` → `INTEGER S(d1,…,dk)` (или `…,dk*W` при n>6). Hollerith-инициализаторы `DATA S(i)/nH…/` оставить без изменений. Печать дескриптором `A`/`A4`. Проверено: `INTEGER S(2)` + `DATA S(1)/4HABCD/,S(2)/4HEFGH/` + `FORMAT(1X,2A4)` → ` АВСDЕFGН`. |
| **fix rule 16** | (F6, опционально) | Добавить скалярную ветвь в regex Pass A: текущий шаблон `EQUIVALENCE\s*\(\s*(\w+)\s*\(\s*(\d+)\s*\)\s*,\s*(\w+)\s*\(\s*(\d+)\s*\)\s*\)` не ловит `(A,B)`; нужен альтернативный шаблон `EQUIVALENCE\s*\(\s*(\w+)\s*,\s*(\w+)\s*\)` → `equiv_map[other]=(base,0)` и переписывание **скалярных** обращений `B` → `A` (сейчас переписываются только `B(n)`). |
| **fix rule 9 / rule-20** | (F12, опционально) | В проверке long-name (prep_tools.py ~890) добавить `IMPLICIT`, `INTEGER`, `REAL`, `LOGICAL`, `COMPLEX`, `DOUBLE`, `PRECISION` в `KEYWORDS`, иначе `lower` абортируется на `IMPLICIT INTEGER (A-Z)`. |

---

## 6. Честные оговорки (что НЕ утверждается)

1. **E9 zero-iteration — реальный семантический дефект 2.02.** Нативная форма
   исполняет тело один раз при `init>limit` (положительный шаг) или `init<limit`
   (отрицательный). lowering R-E9 обязателен для F77-совместимого кода.
2. **F11** — простое удаление `SAVE` (rule 2) на 2.02 случайно даёт верный результат
   из-за статических локальных, но не является корректным lowering; R-F11 обязателен.
3. **G4** доказан только для `n=4` (одно 6-битное слово). Для `n>6` требуется
   `W=ceil(n/6)` слов + `STRCAT` (rule 13) — это экстраполяция, отдельно не прогонялась.
4. **H7** доказан для `CHARACTER*4` (одно слово).hollerith-вывод даёт `АВСDЕFGН`
   вместо `ABCDEFGH` из-за аппаратной 6-битной кодировки (матрица A8) — не ошибка компилятора.
5. **F15** — `EXTERNAL` работает нативно, `INTRINSIC` нет; rule 21 закрывает только
   `INTRINSIC`. `ОТСУТСТВУЕТ FOO` в `F14b` — ошибка линковки при отсутствии
   определения, а не отказ синтаксиса `EXTERNAL`.
6. **rule 16 / rule 9** — сломанные lowering-пути для F6/F12, но оба элемента
   закрыты нативой, поэтому это не блокирует волну 1; отмечено для волны 2.
7. G8-lower использует нативно работающий computed `GO TO` (E2) — зависимость
   от E2, которая подтверждена исполняемым прогоном.

---

## 7. Итог

**Все 21 элементов разделов E–H доведены до OK с исполнимым доказательством.**
Из них 13 — нативная поддержка 2.02 (matrix UNKNOWN/NO сняты реальными прогонами),
3 — натива для основной формы + точный lowering для граничной, 5 — только lowering.
Для волны 2 подготовлены 7 новых правил (R-E9, R-F11, R-ASTAR, R-G4, R-G8, R-H7,
плюс активация rule 21) и 2 исправления существующих (rule 16, rule 9/rule-20).

**Счётчик: 21 / 21.**
