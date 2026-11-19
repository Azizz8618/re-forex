# 07. Реализация Fortran-пути: F77PREP v3 (этапы P1–P4, P6)

Дата: 19.11.2026. Версия изделия: **FOREX 5.00 / 19.11.2026 (re-forex)**.
Статус: реализовано и проверено; исходники — `src/f77prep/F77PREP.FTN` (337
строк, без изменений с v3) и `src/f77prep/prep_tools.py`. Обратная
совместимость с v1/v2 полная: `tests/run-f77-prep.sh` rc=0 для
`prep-case.f77` и `prep-case2.f77`. В v3.1 добавлены правила 17/18/19/21/22
(host-классификация), в v3.2 — 23/24, в v3.3 (волна 2) — правила 25–32
(см. §7). `run-f77-full.sh`: L0 51/51, L1 51/51, 0 PENDING, GATE 20/20, rc=0.

Объект работ — только `src/f77prep/`, `tests/f77/prep-*`,
`docs/plan-f77/09-preprocessor.md` и настоящий документ. `src/f77libr`,
`src/lib21`, `include/`, `reference/`, `docs/drakon` не изменялись.

---

## 1. Инфраструктура P2 (M1–M4)

| Механизм | Реализация |
|---|---|
| **M1 SEQ** | host пишет стабильный SEQ каждой физической карты и инъецирует `PARAMETER (NLV=…,LL=132)`, `INTEGER C(LL,NLV)`, `INTEGER SEQ(NLV)`; F77PREP печатает `777001 <seq> <rule> <itype>` вместо индекса массива |
| **M2 Continuation** | непустая кол. 6 склеивает кол. 7–72 в логическую строку до `LL=132`; карта `SEQ → логическая строка` сохраняется для якорей `C@` |
| **M3 Динамические метки** | единый аллокатор из зоны **90000–99999** с проверкой коллизий с метками исходника; каждое выделение фиксируется записью `777004 <seq> <rule> <pos> <code>` (файл `*.lowered.f77.777004.json`) |
| **M4 Список переменных** | старый `777002 <seq> <pos> <code>` сохранён для rule 3; новый `777004 <seq> <rule> <pos> <code>` несёт списки правил 10/11 и диагностику правила 20; `varmap` ключуется парой `(seq, rule)` |

Форматы `777001`/`777002`/`777003` и `C@`-якоря сохранены без изменений.
F77PREP по-прежнему компилируется ФОРЭКСОМ 2.02: fixed-form 72 колонки,
без `IMPLICIT`/`SAVE`/`CHARACTER`/`PRINT *`/`READ` в собственном исходнике,
штамп `FOREX 5.00 / 19.11.2026 (re-forex)` — 46 знаков.

---

## 2. Таблица правил 9–20

| rule | Конструкция |Lowering| Статус |
|---:|---|---|---|
| **9** | `IMPLICIT t(a-z,…)` | оператор удаляется; для каждого неявно типизированного имени, не объявленного явно, эмитируется `INTEGER X` / `REAL X` / …; якорь `C@ … -> (removed; explicit decls)` | ✅ P3 |
| **10** | `READ *, v1..vk`, `READ(*,*) v1..vk`, `READ(*,*,ERR=LL) …` | `READ <fmt>,v1,…,vk` **без номера юнита**; `<fmt>` — динамическая метка 90000+, дескриптор по каждой переменной (`I10`/`F12.4`/`D22.15`/`A6…`); список из `777004` | ✅ P3, P6 |
| **11** | `END=` / `ERR=` | после READ: `IF (V .EQ. -999999.) GO TO <END>` / `IF (V .EQ. -888888.) GO TO <ERR>`; метка из `777004 kind=11` | ✅ P3, P6 (эмуляция EOF по значению; `END=` в канонической форме rule 4 сохраняет v2-поведение ради совместимости) |
| **12** | `CHARACTER*n`, n>4 | `INTEGER IS(W)`, `W=ceil(n/6)`; литерал → `DATA IS(k)/6H…/` (последнее слово с паддингом); печать `A6`×`W-1` + `A<ost>` | ✅ P4 |
| **13** | `A // B` | `CALL STRCAT(IA,IB,IC,LA,LB)`; если левый операнд — подстрока, сначала `CALL SUBSTR(...)`; строковый литерал → `DATA ILn/kH…/` | ✅ lowering P4; **зависит от F77LIBR** |
| **14** | `S(i:j)`, `IF (S .EQ. T)` | `CALL SUBSTR(IS,i,j,IT)`; сравнение → `KCn = ISTRCM(IS,IT)` + `IF (KCn .EQ. 0) GO TO LL` | ✅ lowering P4; **зависит от F77LIBR** |
| **15** | `ASSIGN ll TO I`, `GO TO I`, `GO TO (l1,…,lk),I` | `ASSIGN` → `I = ordinal`; `GO TO I` → цепочка `IF (I .EQ. j) GO TO L_I[j]`; для computed GO TO метки берутся из списка | ✅ P3 |
| **16** | `EQUIVALENCE (A(i),B(j))` (однотипные) | rename-карта `B(k) → A(k+i-j)`, объявление `B` удаляется, оператор заменяется якорем; разнотипный случай — `SystemExit` с диагностикой | ✅ P3 |
| **17** | `DO WHILE` без `END DO` | host-классификатор (`prep_tools.py`) помечает незакрытые `DO WHILE` по LIFO-стеку; аллокатор выдаёт пару меток `top/bottom`, перед `END`/`STOP` вставляется `GO TO top` + `bottom CONTINUE`. Вложенные циклы закрываются в обратном порядке по номеру метки | ✅ P5/v3.1 (host) |
| **18** | continuation / SEQ для строк >72 и >20 | M1/M2 в `make_deck1()` (SEQ, `LL=132`, склейка кол. 6), плюс n3.1: эмитируемые операторы длиннее 72 кол. разбиваются обратно на fixed-form карты с маркером продолжения в кол. 6; комментарии `C@`/`C` не трогаются | ✅ P1 + v3.1 |
| **19** | inline `MAX/MIN/ABS/DIM` | `DST=AMAX1(A,B)` → `DST=A; IF (B .GT. DST) DST=B`; для `MIN` — `.LT.`, для `ABS` — `IF (A .LT. 0) DST=-A`, для `DIM` — `DST=A-B; IF (DST .LT. 0) DST=0`. ITYPE семьи (1..4) выставляется host-классификатором | ✅ P5/v3.1 (host) |
| **20** | идентификатор >6 знаков | F77PREP эмитирует `777004 <seq> 20 <pos> <ASCII>` для каждого такого имени; host печатает `C@ <orig> -> TRUNCATED NAME: …` и завершается ошибкой. Ключевые слова и имя program unit-а исключены. `AAAAAAX`/`AAAAAY` → FAIL/diagnostic, молчаливого слияния нет | ✅ P1 |
| **21** | `EXTERNAL FOO` / `INTRINSIC SQRT` как объявления | host-классификатор помечает оператор, lowering удаляет его с якорем `C@ … -> (removed; EXTERNAL/INTRINSIC declaration)`; вызов внешней функции и нативный `SQRT` работают без объявлений | ✅ v3.1 (F03) |
| **22** | `CABS(WC)` | `R=CABS(WC)` → `R=SQRT(REAL(WC)**2+AIMAG(WC)**2)`; `REAL`/`AIMAG`/`SQRT` нативные. Для переменной, которой присвоен комплексный литерал `(a,b)`, host materializует `COMPLEX WC` сразу после `PROGRAM` (иначе неявный `REAL` отбрасывает мнимую часть) | ✅ v3.1 (K03) |

Правила 0–8 (v1/v2) сохранены побайтово: `IMPLICIT NONE`, `SAVE`,
`PRINT *`, `READ(*,*,END=LL)`, `DO WHILE`/`END DO`, `CHARACTER*1..4`,
`S='literal'`.

---

## 3. Примеры lowering

### 3.1 Rule 10 + динамическая метка

```fortran
      READ *, N, M
```
↓
```fortran
C@ READ *, N, M -> READ 90000,N,M
      READ 90000,N,M
C@ (end of program) -> 90000 FORMAT(I10,I10)
 90000 FORMAT(I10,I10)
```
`777004`: `90000 10 0` (seq, rule, pos, code).

### 3.2 Rule 11 (ERR= sentinel) + rule 15 + DP D22.15

```fortran
      READ(*,*,ERR=99) N
```
↓
```fortran
C@ READ(*,*,ERR=99) N -> READ 90000,N
      READ 90000,N
C@ READ EARLY-EXIT -> IF (N .EQ. -888888.) GO TO 99
      IF (N .EQ. -888888.) GO TO 99
```
DP-печать: `PRINT *, X` (`DOUBLE PRECISION X`) → `9000 FORMAT(1X,D22.15)`.

### 3.3 Rule 9 + rule 16

```fortran
      IMPLICIT INTEGER (A-Z)
      INTEGER IA(10), IB(5)
      EQUIVALENCE (IA(2),IB(1))
      IB(1) = 7
```
↓
```fortran
C@ IMPLICIT INTEGER (A-Z) -> (removed; explicit decls)
      INTEGER X
C@ INTEGER IA(10), IB(5) -> INTEGER IA(10)
      INTEGER IA(10)
C@ EQUIVALENCE (IA(2),IB(1)) -> (removed; rename map applied)
C@ IB(1) = 7 -> IA(2) = 7
      IA(2) = 7
```

### 3.4 Rules 12/13/14 (CHARACTER*10)

```fortran
      CHARACTER*10 S
      CHARACTER*6 T
      S='ABCDEF'
      T = S(2:4) // 'XY'
      IF (S .EQ. T) GO TO 99
```
↓
```fortran
      INTEGER IS(2)
      INTEGER IT
      DATA IS(1)/6HABCDEF/
C@ T = S(2:4)//'XY' -> CALL SUBSTR(IS,2,4,IW5)
      CALL SUBSTR(IS,2,4,IW5)
      DATA IL5/2HXY/
C@ T = S(2:4)//'XY' -> CALL STRCAT(IW5,IL5,IT,3,2)
      CALL STRCAT(IW5,IL5,IT,3,2)
C@ IF (S .EQ. T) GO TO 99 -> KC6 = ISTRCM(IS,IT)
      KC6 = ISTRCM(IS,IT)
      IF (KC6 .EQ. 0) GO TO 99
C@ PRINT *, S -> PRINT 9000,IS(1),IS(2)
 9000 FORMAT(1X,A6,A4)
```

**Соглашение по F77LIBR (для другого агента):** имена ровно `STRCAT`,
`SUBSTR`, `ISTRCM` (≤6 знаков, не системные), сигнатуры:

```
SUBROUTINE STRCAT(A,B,C,LA,LB)   ! A,B - 6-битные слова, LA/LB - длины
SUBROUTINE SUBSTR(A,I,J,C)       ! C = A(I:J), 1-based
INTEGER FUNCTION ISTRCM(A,B)     ! -1 / 0 / +1 по TEXT-кодам
```

До появления этих процедур в PERSO `0o2310` тест `prep-case7` проверяется
только на проходе 1 (lowering); проход 2 ожидаемо даёт
`ОТСУТСТВУЕТ STRCAT / SUBSTR / ISTRCM`. Это граница lowering-а, не ошибка
препроцессора.

---

## 4. Тесты

| Файл | Что проверяет | Проход 2 |
|---|---|---|
| `prep-case.f77`, `prep-case2.f77` | регрессия v1/v2 (правила 1–8) | ✅ эталоны |
| `prep-case3.f77` (+`.data`) | rule 10, список из двух переменных, метка 90000 | ✅ `10 20` |
| `prep-case4.f77` | rule 15 (ASSIGN, computed GO TO) | ✅ `1.0000` |
| `prep-case5.f77` | rules 9 + 16 (IMPLICIT, EQUIVALENCE) | ✅ `7 3` |
| `prep-case6.f77` (+`.data`) | rules 10/11 + `D22.15` | ✅ DP + `5` |
| `prep-case7.f77` | rules 12/13/14 | только проход 1 (F77LIBR) |
| `prep-trunc.f77` | rule 20, negative: `AAAAAAX`/`AAAAAY` → `TRUNCATED NAME`, rc≠0 | ожидаемый FAIL |
| `prep-case8.f77` | **F03**: rule 21, `EXTERNAL MYFUN` / `INTRINSIC SQRT` удаляются | ✅ `4.0000` |
| `prep-case9.f77` | **I02**: rule 12 + подстрока с constant-folding (`S(2:4)` → `DATA IW5/6HBCD   /`) | ✅ ` ВСD` (A4) |
| `prep-case10.f77` | **K03**: rule 22, `CABS` → `SQRT(REAL**2+AIMAG**2)` + `COMPLEX WC` | ✅ `5.0000` |

Кейсы 8–10 добавлены в `tests/run-f77-prep.sh`; старые кейсы 1–2 сохранены
побайтово. `F77PREP.FTN` остаётся на v3 без изменений: ФОРЭКС 2.02 имеет жёсткий
лимит памяти трансляции, поэтому правила 17/18/19/21/22 классифицируются
host-частью `prep_tools.py`, которая держит полный текст логических строк и
структуру `DO WHILE`/`END DO`. Это не меняет формат записей `777001`/
`777004` и не ломает обратную совместимость.

Примечание по I02: `A`-дескриптор ФОРЭКСа 2.02 декодирует TEXT-коды через
собственную таблицу, поэтому ASCII `BCD` печатается как ` ВСD` — то же
поведение зафиксировано в `prep-case2-expected.out`. Эталон `I02_charstar.gold`
обновлён под фактический вывод 2.02.

---

## 5. Результаты проверок

```
tests/run-f77-prep.sh          rc=0   (case1 11/11, case2 29/29, case8 14/14,
                                        case9 13/13, case10 11/11; вывод 1/1, 3/3,
                                        1/1, 1/1, 1/1)
tests/run-f77-full.sh          rc=0   (L0 32/32, L1 32/32, L2 8/8, L3 2/2+2 skip,
                                       L4 9/9, GATE 20/20, 0 PENDING)
python3 tests/check-source-words.py  rc=0  (LO*SYN, LO*GEN: 1024/1024 слов)
tests/check-label-semantics.sh rc=0   (0 AUTO/TEXT/ОКТАЛ+/ДЛИННЫХ/КОЛЛИЗИЙ)
tests/check-constants.sh       rc=0
tests/check-text-decoded.sh    rc=0
tests/run-glissade-forex.sh    rc=0   (14/14 строк)
```

---

## 6. Что осталось за границей Fortran-пути

* **F77LIBR**: `STRCAT`, `SUBSTR`, `ISTRCM` (правила 13/14), затем проход 2
  для `prep-case7`; при необходимости зоны `0o2314..0o2317`.
* **P5 закрыт** (v3.1): rule 17 (`DO WHILE` без `END DO`), rule 18 (continuation/
  SEQ >72 и >20), rule 19 (inline `MAX/MIN/ABS/DIM`) и правила 21/22
  (`EXTERNAL`/`INTRINSIC`, `CABS`) реализованы в host-части `prep_tools.py`.
  `F03`/`I02`/`K03` переведены из PENDING в OK; `run-f77-full.sh` даёт
  L0 32/32, L1 32/32, 0 PENDING, gate 20/20, rc=0.
* **E4 / МАДЛЕН-spine** (`03-fortran-path.md` §3): новые FORMAT-дескрипторы
  (`E`, `ES`, `G`, `A` без ширины, `T/TR/BN`), unformatted I/O, `REWIND`/
  `BACKSPACE`/`ENDFILE`, настоящий тип-вариант `CHARACTER` в GENERATOR,
  подлинный `IOSTAT`/EOF; только type-preserving `EQUIVALENCE` и sentinel
  `END=`/`ERR=` не дают полной F77-семантики.
* Сентинал END=/ERR= — **эмуляция по значению**, число задаётся host и не
  должно встречаться в данных; документировано в `03-fortran-path.md` §2.4.

---

## 7. Волна 2 (v3.3): host-lowerings 23–32

`F77PREP.FTN` остаётся на v3 без изменений (ФОРЭКС 2.02: жёсткий лимит
памяти трансляции). Все новые правила классифицируются и применяются в
`src/f77prep/prep_tools.py`; каждое имеет `C@`-якорь и двухпроходной тест
`tests/f77/prep-caseNN.f77` → `prep-caseNN-expected.f77` +
`prep-caseNN-expected.out` (прогон `tests/run-f77-prep.sh`, rc=0).

| rule / правило | Конструкция | Lowering (host) | Тест | rc |
|---:|---|---|---|:--:|
| **23** | `A .EQV. B`, `A .NEQV. B` | `(A .AND. B) .OR. (.NOT.A .AND. .NOT.B)` / `…AND.NOT.B…` (нативные C5) | case11 | 0 |
| **24** | `A(*)`, `A(lb:*)` | `A(1)` / `A(lb)` (F19/H6) | smoke + case14 (косв.) | 0 |
| **25 / R-E9** | `DO m I=e1,e2[,e3]`, нуль итераций | перед DO guard `IF (e1 .GT. e2) GO TO Ls` (шаг ≥0) или `IF (e1 .LT. e2) GO TO Ls` (шаг <0); после terminal `Ls CONTINUE`. Переменный шаг: `IF (V .GE. 0) GO TO Lp / IF (e1 .LT. e2) GO TO Ls / GO TO Lb / Lp CONTINUE / IF (e1 .GT. e2) GO TO Ls / Lb CONTINUE`. Метки Ls/Lp/Lb — `dyn_alloc` из зоны 90000–99999 | case12 (литерал), case21 (переменный шаг, обе ветви) | 0 |
| **26 / R-F11** | `SAVE v1,…,vk` | `COMMON /<U>SV/v1,…,vk` + `BLOCK DATA` с `INTEGER v` / `COMMON` / перенесёнными `DATA v/c/`; блок ≤6 знаков. Легаси-случай (главная программа без `DATA`) сохраняет rule 2 побайтово (case1) | case13 (`11 12`) | 0 |
| **27 / R-G8** | `CALL S(*L1,…,*Lk)`, `RETURN j` | `INTEGER RC; CALL S(RC); GO TO (L1,…,Lk,Lb),RC; Lb CONTINUE`; `SUBROUTINE S(RC)` получает `INTEGER RC`; `RETURN j` → `RC=j; RETURN`. Lb — `dyn_alloc` | case14 (`1`) | 0 |
| **28 / R-G4** | `CHARACTER*n FUNCTION F(args)` | `SUBROUTINE F(RV,args)` + `INTEGER RV,IH` (`RV(W),IH(W)` при n>6); `F='lit'` → `DATA IH/nH…/` + `RV=IH`; вызов `S=F(args)` → `INTEGER S; CALL F(S,args)` (не `INTEGER FUNCTION` — на 2.02 он вернул 0) | case15 (` АВСD`) | 0 |
| **29 / R-H7** | `CHARACTER*n S(d1,…)` | `INTEGER S(d1*W,…)`, `W=ceil(n/6)`; Hollerith-`DATA` не меняется | case16 (` АВСDЕFGН`) | 0 |
| **30 / R13** | `G w.d` в FORMAT | по типу PRINT-переменной: REAL→`E w.d`, DP→`D w.d`, COMPLEX→`2E w.d`, LOGICAL→`L1`, INTEGER→`Iw`; тип берётся из объявлений/неявного typing, FORMAT переписывается по метке | case17 (REAL+DP), case22 (COMPLEX) | 0 |
| **31 / R21** | `1P, E12.4` | `1PE12.4` (запятая после P ломает формат 2.02) | case18 (`   35.0000-01`) | 0 |
| **4 + 11 / R11-END** | `READ(*,*,END=LL) v` | `READ <fmt>,v` + `IF (v .EQ. -999999[.]) GO TO LL`; раньше метка `END=` просто терялась. Для INTEGER сентинал без точки | case19 (` ЕОF`, карта `-999999.`); case2 — регрессия | 0 |
| **10 + 11 / R11-ERR** | `READ(*,*,ERR=LL) v` | `READ <fmt>,v` + `IF (v .EQ. -888888.) GO TO LL` (метка из `777004 kind=11 pos=2`) | case20 (` ЕRR`, карта `-888888.`) | 0 |

Побочные исправления host-части, сделанные в этой волне:

* разбор `777004 kind=20` теперь идёт **в порядке эмиссии** (раньше
  `pos`-ключевая карта перезаписывала символы второго длинного имени на той
  же строке — из-за этого `CHARACTER*n FUNCTION` абортировался как
  `TRUNCATED NAME: FUNCTIONR`);
* локальная переменная `data` в rule 14 переименована в `dcard` (она
  затеняла JSON-структуру с `777004` и ломала rule 20 в case9);
* якоря `C@` новых правил короче 72 колонок (иначе ФОРЭКС читает хвост
  комментария как отдельную карту).

### 7.1 Результаты проверок v3.3

```
tests/run-f77-prep.sh          rc=0   (17 кейсов: case1/2/8..22, PASS1/PASS2)
tests/run-f77-full.sh          rc=0   (L0 51/51, L1 51/51, L2 8/8, L3 2+2 skip,
                                       L4 9/9, GATE 20/20, 0 PENDING)
python3 tests/check-source-words.py  rc=0  (LO*SYN, LO*GEN: 1024/1024)
tests/check-label-semantics.sh rc=0   (0 нарушений)
tests/check-constants.sh       rc=0
tests/check-text-decoded.sh    rc=0
```

Логи волны: `logs/f77_lower2_*.txt` (сырые протоколы dispak по каждому
правилу и сводные прогоны).

### 7.2 Честные оговорки

* R-E9/R-F11/R-G8/R-G4/R-H7/R13/R21/R11 — это **lowerings под профиль
  FOREX 5.00 / 2.02**, а не полная семантика X3.9. В частности, `END=`/`ERR=`
  остаются эмуляцией EOF по значению (сентинная карта подаётся host-ом), а
  точный автовыбор G-дескриптора (F vs E) не реализован — профиль фиксирует
  конкретный тип-зависимый выбор.
* R-G4/R-H7 доказаны executable-прогоном для `n=4` (одно 6-битное слово);
  вариант `W=ceil(n/6)>1` реализован по той же схеме, но отдельного deck'а
  не имеет.
