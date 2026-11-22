# Honest stratification of the 200-element F77 matrix (re-forex, F2)

Scope: read-only analysis of `docs/plan-f77-full/01-f77-standard-matrix.md` (200 rows,
all marked OK), `docs/plan-f77/12-acceptance.md` §4, `docs/plan-f77-full/00-master-plan.md`
§2/§5, `03-fortran-path.md` §0/§3, `04-verification.md` §4, the wave documents
`12-intrinsics-coverage.md`, `13-char-expr.md`, `14-control-decl.md`, `15-io.md`,
`16-k-closure.md`, and the cited logs/cases. No repository file was edited.

## 1. The core inconsistency

The matrix has three mutually incompatible statements about what `OK` means:

1. `01-f77-standard-matrix.md:36` defines `OK` as an executable proof on 2.02 and
   `:37` defines `PARTIAL` for, among other cases, "only through F77PREP/Hollerith
   recipe for 2.02".
2. `01-f77-standard-matrix.md:438` (§12.3 item 1) repeats that `OK` on 2.02 via
   Hollerith/lowering "does NOT mean native support in base 4.13, therefore such
   rows are PARTIAL", while §12.1 (`:397-410`) reports 200 OK / 0 PARTIAL.
3. §12.1 (`:412-414`) says F13 `IMPLICIT NONE` is a boundary row counted as NO,
   but the table at `:157` marks it OK and §12.4 (`:473-475`) counts it as OK.

The wave documents that produced the OK rows kept the distinction explicitly:
`13-char-expr.md:235` reports 1 native / 7 lowering / 1 F77PREP diagnostic /
1 hardware caveat; `14-control-decl.md:67-69` reports 13 pure native /
3 native core plus lowering boundary / 5 lowering only; `15-io.md:39,65-66`
uses `OK*` for 5 lowering-only rows and PARTIAL/NO for 4 more;
`12-intrinsics-coverage.md:75-80` has categories (a), (a'), (b), (c), (c'), (d);
`16-k-closure.md:26-48,50` states that all 21 closed K rows are inline lowering
(except the built-in `ISIGN`). §12.1 collapsed all of these into one undifferentiated
`OK`, which is the source of the overclaim.

## 2. Classification rules used here

* **(a) native executable proof** = the F77 source text was compiled and run by a
  compiler available here (system FOREX 2.02 on disk 2048/2348, the E1/E5 decks,
  the 2.02 glissade regression, or our *TRANS contour), with no F77PREP rewrite,
  F77LIBR procedure, Hollerith source workaround or host adapter in the path.
  Calls resolved by the system library (LIBREFER/FORTLIBR) and numerically
  verified in K05 are included: the compiler and its runtime are executable here.
* **(b) lowering proof** = the element is executable here only after F77PREP rules,
  F77LIBR/PERSO procedures, a Hollerith source recipe, inline rule 19 rewriting,
  or the ARFA PERSO G1 host bridge. Rows where the F77 core is native but at
  least one F77-relevant boundary needs lowering (E9, F19, H6) are counted here.
* **(c) cross-only proof** = the row has no FOREX executable evidence and rests
  only on the `*FTN` cross-check.
* **(d) boundary** = not an X3.9-1978 element but counted in the 200.

## 3. Counts by section

| Section | OK total | (a) native 2.02/*TRANS | (b) lowering/recipe/library | (c) cross-only *FTN | (d) outside X3.9 |
|:---|---:|---:|---:|---:|---:|
| A. Lexics | 8 | 7 | 1 | 0 | 0 |
| B. Types and constants | 13 | 10 | 3 | 0 | 0 |
| C. Operators and expressions | 10 | 7 | 3 | 0 | 0 |
| D. Assignment | 4 | 3 | 1 | 0 | 0 |
| E. Control | 15 | 14 | 1 | 0 | 0 |
| F. Declarations | 19 | 13 | 5 | 0 | 1 |
| G. Procedures | 9 | 6 | 3 | 0 | 0 |
| H. Arrays | 7 | 5 | 2 | 0 | 0 |
| I. Character strings | 7 | 0 | 7 | 0 | 0 |
| J. I/O | 28 | 18 | 10 | 0 | 0 |
| K. Intrinsics | 80 | 60 | 20 | 0 | 0 |
| **TOTAL** | **200** | **143** | **56** | **0** | **1** |

Section-by-section ID mapping (all 200 rows):

* A: (a) A1, A2, A3, A4, A6, A7, A8. (b) A5.
* B: (a) B1, B2, B3, B4, B5, B7, B8, B9, B10, B11. (b) B6, B12, B13.
* C: (a) C1, C2, C3, C4, C5, C7, C10. (b) C6, C8, C9.
* D: (a) D1, D2, D4. (b) D3.
* E: (a) E1, E2, E3, E4, E5, E6, E7, E8, E10, E11, E12, E13, E14, E15. (b) E9.
* F: (a) F1, F3, F4, F5, F6, F7, F9, F10, F12, F14, F16, F17, F18.
  (b) F2, F8, F11, F15, F19. (d) F13.
* G: (a) G1, G2, G3, G5, G6, G7. (b) G4, G8, G9.
* H: (a) H1, H2, H3, H4, H5. (b) H6, H7.
* I: (b) I1, I2, I3, I4, I5, I6, I7.
* J: (a) J1, J3, J9, J10, J11, J12, J15, J16, J17, J18, J19, J20, J21, J22,
  J25, J26, J27, J28. (b) J2, J4, J5, J6, J7, J8, J13, J14, J23, J24.
* K: (a) K1, K2, K3, K4, K6, K7, K8, K9, K11, K12, K13, K14, K19, K20, K21,
  K22, K23, K24, K25, K26, K27, K28, K29, K30, K32, K33, K34, K35, K36, K38,
  K39, K41, K42, K43, K50, K51, K52, K53, K54, K55, K56, K57, K58, K60, K64,
  K65, K66, K67, K68, K69, K70, K71, K72, K73, K74, K75, K76, K77, K78, K80.
  (b) K5, K10, K15, K16, K17, K18, K31, K37, K40, K44, K45, K46, K47, K48,
  K49, K59, K61, K62, K63, K79.

## 4. Most important entries by class, with evidence

### Class (a), native executable proof, 143 rows

| Entry | Matrix line | Decisive evidence |
|:---|---:|:---|
| B1/B2/A1/C1/D1/E7/E11/J1/J12 | 80, 81, 67, 98, 113, 128, 132, 207, 218 | `logs/plan_f77_probes.txt:1,2` (BASE/DOLOOP compiled+ran); `12-acceptance.md:29` gold `21 1.00 3.00` |
| B3/B9/K6/K78 | 82, 88, 258, 385 | `logs/plan_f77_probes.txt:5` (DOUBLPR), `07-experiments.md:24,96` (`SQRT(2D0)` ~1.414213562371515) |
| B4/B10/C10/K22/K80 | 83, 89, 107, 284, 387 | `logs/plan_f77_probes.txt:6`; `13-char-expr.md:143` "Нативно работает без всякого lowering-а" for `+ - * /` on COMPLEX; `logs/f77_13_C10.txt:40` |
| B5/B11/D2/C5 | 84, 90, 114, 102 | `logs/plan_f77_probes.txt:15` (LOGICAL compiled+ran); `01-gap-analysis.md:32` |
| E2/E3/E4/E10/E13 | 123, 124, 125, 131, 134 | `14-control-decl.md:43-48` marks all five "натива"; `logs/f77_14_E02.txt` ... `E13.txt` |
| E6 (block IF) | 127 | `logs/plan_f77_probes.txt:3` plus `12-acceptance.md:30` (nested ELSE) |
| F4/H3 (3D/7D arrays) | 148, 185 | `14-control-decl.md:49,61` "натива"; `logs/f77_14_F04.txt`, `H03.txt` |
| F6/F7/F10/F16/H1/H2/H5 | 150, 151, 154, 160, 183, 184, 187 | 2.02 glissade regression `glkern.b6:14-27,50-93,107`, `docs/16-glissade-run.md:7-14` (14/14), `logs/plan_f77_probes.txt:7,10` |
| G7 (ENTRY) | 175 | `14-control-decl.md:59` "натива (две точки входа)", `logs/f77_14_G07.txt` |
| J11/J15/J18/J21/J22/J28 | 217, 221, 224, 227, 228, 234 | `logs/f77_15_gold.txt` rows with `FATAL` empty and `OK`; `15-io.md:51,53-56,62` calls them native, 0 words patched |
| K05 block, 47 names | 253-379 (subset) | `12-intrinsics-coverage.md:75` category (a), `logs/f77_intrinsics_coverage.txt` K05 run `rc=0`, `tests/plan-f77-full/unit/K05_intrinsics_numeric/K05_intrinsics_numeric.gold` |
| K42 ISIGN | 324 | `16-k-closure.md:37,89-91`: built-in name, numerically verified, "lowering не нужен" |

Caveats inside class (a), not reclassified: A8 native output is `АВСD` because of
the 6-bit TEXT hardware artifact (`logs/f77_13_A08.txt:16-30`), exact `ABCD`
needs the host `recode.py`. J25/J26 compile and run on 2.02 but their gold is an
`IOXNSWAP` block, not the printed `POS OK` (see flags). J21 was probed as
`1PE12.4`, and the canonical comma spelling `1P,E12.4` needs rule R21.

### Class (b), lowering / recipe / library only, 56 rows

| Entry | Matrix line | Decisive evidence |
|:---|---:|:---|
| A5 (>6 char diagnostic) | 71 | `logs/f77_13_A05.txt:49-51`: `TRUNCATED NAME ... (all -> AAAAAA)`, rc=1. Native 2.02 silently merges (`01-gap-analysis.md:80-81`), wave 13 calls it F77PREP diagnostic |
| B6/F2/F8/H7/G4/I1/I2 | 85, 146, 152, 189, 172, 195, 196 | `13-char-expr.md:42,235`: B6 "lowering rule 12"; `14-control-decl.md:58,63,67-69`: G4/H7 "только lowering"; `16-k-closure.md:83-88` (LEN, INDEX depend on rule 12) |
| B12/B13/C8/C9/D3 | 91, 92, 105, 106, 115 | `logs/f77_13_B12.txt:81-82`, `B13.txt:79-80`, `C8.txt:76`, `C9.txt:95`, `D3.txt:83-84`; rules 8/12/13/14 plus F77LIBR `STRCAT`, `ISTRCM`, `SUBSTR` |
| C6 EQV/NEQV | 103 | `13-char-expr.md:45,114`: native rejected, boolean-formula lowering, `logs/f77_13_C6.txt:89` |
| E9 zero-trip DO | 130 | `14-control-decl.md:46`: native for step and negative step, lowering guard `IF (e1>e2/e1<e2) GO TO after` for zero iterations |
| F11 SAVE | 155 | `14-control-decl.md:52`: native probe rejected, lowering to `COMMON` + `BLOCK DATA`, `logs/f77_14_F11.txt` |
| F15 INTRINSIC, F19/H6 `A(*)`, G8 alternate return | 159, 163, 188, 176 | `14-control-decl.md:55,57,60,62`: rule 21 deletion, `A(*)→A(1)`, integer return code plus computed GO TO |
| I5/I6/J14 (A descriptor, Hollerith recipe) | 199, 200, 220 | `07-experiments.md:25,122`: working recipe `INTEGER I; DATA I/4HABCD/; FORMAT(1X,A4)`, but `12-acceptance.md:61-64`: native CHARACTER does not compile on 2.02 |
| I7 STRCMP | 201 | `08-runtime.md:47,79-80`: F77LIBR/PERSO procedure, not an intrinsic of 2.02 |
| J5/J6/J7/J8/J13 | 211, 212, 213, 214, 219 | `15-io.md:47-52` marks all five `OK*` (lowering, not native semantics); native probes fail in `logs/f77_15_probes.txt` rows `J5_list_native`, `J6_list_native`, `J7_END_native`, `J8_ERR_native`, `J13_G_native` |
| J2/J4/J23/J24 | 208, 210, 229, 230 | `01-f77-standard-matrix.md:477-503` §12.5: F77PREP rules 34-40 plus real ARFA G1 bridge; `logs/f77_prep_v2_result_case23-26.txt`; `:516-521` native verdict `NEEDS-RUNTIME-REBUILD` |
| G9 F77LIBR calls | 177 | `08-runtime.md:2,4`, `logs/f77_libr_v2_runtime.txt`, PERSO `0o2310` |
| K20 inline-lowering rows | 257, 262, 272-275, 303, 314, 322, 331-336, 356, 358-360, 386 | `16-k-closure.md:26-48`: explicit exact rule-19 expressions for each; note K79 `DSQRT` is rewritten to generic `SQRT`, K44 `LEN` is substituted at compile time, K45 `INDEX` is an inline loop |

### Class (c), cross-only with `*FTN`, 0 rows

`12-acceptance.md:18,42-57` records a 3/3 cross-check with Fortran-GDR for
`base`, `do2d`, `intrinsics_ext`. The same eight decks are compiled and executed
by FOREX 2.02 first (`12-acceptance.md:16-17`). The only matrix row that mentions
`*FTN` in its evidence is F17 (`01-f77-standard-matrix.md:161`), and it cites
`12-acceptance.md:38-40`, where the statement is that the same source compiles
under both compilers. That is a corroborating oracle, not the sole proof, so
F17 stays in (a). There is no row whose only executable evidence is `*FTN`.

### Class (d), outside X3.9-1978, 1 row

F13 `IMPLICIT NONE` (`01-f77-standard-matrix.md:157`): MIL-STD-1753/F90 extension,
`01-gap-analysis.md:87` records native 2.02 rejection `НЕДОПУСТИМ КЛУЧ СЛОВО`,
`tests/f77/prep-case.f77` plus F77PREP rule 1 remove it. It is counted as OK only
because the lowering exists.

## 5. Proposed exact replacement text for §12.1

Replace the block at `01-f77-standard-matrix.md:412-424` (the paragraphs after
the 200/200 table) with:

> Сводка §12.1 описывает **исполнимую доступность элемента в доступном контуре**:
> системный ФОРЭКС 2.02 на дисках 2048/2348, F77PREP/F77LIBR, PERSO-зоны `0o2300`
> и `0o2310`, мост АРФЫ G1 и наш контур `*TRANS`. Она не утверждает ни нативную
> поддержку ядром FOREX 4.13, ни полную X3.9-семантику для всех вариантов
> конструкции. Исполняемого 4.13-бинарника в среде нет (`00-master-plan.md:41-44`,
> `03-fortran-path.md:44-51`), 4.13 служит исходником и gold.
>
> Счётчик 200/200 сохраняется как «полный F77 в доступном контуре», но он
> стратифицирован по силе доказательства:
>
> | Класс | Что означает | A | B | C | D | E | F | G | H | I | J | K | Всего |
> |:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
> | (a) | нативная исполняемая проба 2.02 или нашего `*TRANS` | 7 | 10 | 7 | 3 | 14 | 13 | 6 | 5 | 0 | 18 | 60 | **143** |
> | (b) | только F77PREP/F77LIBR/Hollerith-рецепт/inline rule 19/мост G1 | 1 | 3 | 3 | 1 | 1 | 5 | 3 | 2 | 7 | 10 | 20 | **56** |
> | (c) | только кросс `*FTN`, без executable-доказательства ФОРЭКСА | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |
> | (d) | вне X3.9-1978, учтено только как объект понижения | 0 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | **1** |
> | **ИТОГО OK** | | **8** | **13** | **10** | **4** | **15** | **19** | **9** | **7** | **7** | **28** | **80** | **200** |
>
> Класс (b) включает строки с нативной основной формой и lowering-ом для
> граничного случая (E9 нуль итераций, F19/H6 `A(*)`, A5 диагностика >6 знаков).
> Кросс-сверка `*FTN` 3/3 в E5 (`12-acceptance.md:18,42-57`) является
> дополнительным oracle, а не самостоятельным доказательством: те же декы
> исполняются ФОРЭКСОМ 2.02 (`12-acceptance.md:16-17`).
>
> F13 (`IMPLICIT NONE`) является пограничной строкой класса (d): она не входит в
> X3.9-1978 и учтена в 200 только потому, что F77PREP rule 1 исполнимо удаляет её
> (`tests/f77/prep-case.f77`). При подсчёте «чисто X3.9» вычитаем 1 из OK и из
> общего числа: 199/199, из них натива 143.
>
> Доля подтверждённой доступности: **200/200 = 100 % в доступном контуре**; из
> них 143/200 (71,5 %) подтверждены нативной executable-пробой, 56/200 (28,0 %)
> только через понижение, библиотеку или мост, 1/200 вне стандарта. PERSO-мост
> АРФЫ для J2/J4/J23/J24 даёт профильное подтверждение (IOSTAT 0/−1, не более
> 8 слов на Э70, `ACCESS='DIRECT'`/`RECL` не проверены), а не полную
> X3.9-семантику (`§12.5`). Раздел K: 49 интринзиков численно в K05, 17
> отрицательным контролем K06, 12 базовыми пробами и корпусом, 20 имён закрыты
> inline-lowering rules 19 (`16-k-closure.md:26-48`) и не являются нативными
> именами 2.02.

## 6. Proposed exact replacement text for §12.3

Replace `01-f77-standard-matrix.md:436-446` with:

> ### 12.3. Что НЕ утверждается (уточнённая редакция)
>
> 1. Статус OK в §12.1 означает «есть исполнимое доказательство в доступном
>    контуре» по определению §0.2. Он **не** означает «нативная поддержка
>    ядром FOREX 4.13»: исполняемого 4.13-бинарника в среде нет, а 56 строк
>    класса (b) доказаны только через F77PREP/F77LIBR, Hollerith-рецепт, inline
>    rule 19 или PERSO-мост АРФЫ на 2.02. По исходному определению §0.2 и по
>    исходному §12.3 п.1 эти 56 строк были бы PARTIAL; в исправленной сводке они
>    остаются OK в счётчике доступности, но явно помечены классом (b).
> 2. Раздел K не содержит UNKNOWN, но 20 из 80 интринзиков обязаны своим статусом
>    inline-lowering rule 19 (`16-k-closure.md:26-48`), в том числе `DFLOAT`,
>    `DREAL`, `ANINT`, `DNINT`, `NINT`, `IDNINT`, `DMAX1`, `DMIN1`, `DDIM`,
>    `DTAN`, `DASIN`, `ACOS`, `DACOS`, `LEN`, `INDEX`, `LGE`, `LGT`, `LLE`,
>    `LLT` и `DSQRT` (переписан в generic `SQRT`). Это численно проверенные
>    выражения на 2.02, а не нативные entry 2.02. K42 `ISIGN` нативен
>    (`16-k-closure.md:37,89-91`).
> 3. Кросс `*FTN` 3/3 (`12-acceptance.md:18,42-57`) не является отдельным
>    классом доказательства: FOREX 2.02 исполняет те же восемь деков. Строк,
>    подтверждённых только `*FTN`, нет. Диагностики ГДР (`ERROR 106/123/138`,
>    `01-gap-analysis.md:90,92`) к нативному ФОРЭКСУ не применяются.
> 4. Пограничные и профильные оговорки сохраняются: F13 не входит в X3.9;
>    J7/J8 реализованы sentinel-переменными, исходная EOF/ERR-семантика не
>    сохраняется (`15-io.md:49-50`); J2/J4/J23/J24 подтверждены через мост G1
>    с profile-IOSTAT и без прямого доступа, нативный путь имеет вердикт
>    `NEEDS-RUNTIME-REBUILD` (`§12.5`, `:516-521`); J25/J26/J27 работают только
>    на отдельных LUN, а в gold J25/J26 зафиксирован блок `IOXNSWAP`, а не
>    проверка позиционирования.
> 5. Матрица оценивает синтаксис и доступность, а не полную численную семантику
>    (40-битная мантисса, `DP` с `F16.12` даёт `I/О-ЕRRОR 227`,
>    `07-experiments.md:24,103`) и не производительность. Старые таблицы
>    `dubna-languages.md:106-134,240-275` использовались только при безусловной
>    подмене `*forex` на `*fortran`; их «−» для многомерных массивов и «ч» для
>    блочного IF опровергнуты исполняемыми пробами (`01-gap-analysis.md:19`).

## 7. Proposed one-sentence product claim (README / STATUS)

> FOREX 5.00 закрывает всю матрицу F77 в доступном контуре (2.02 + F77PREP/F77LIBR + PERSO-мост АРФЫ): 200/200 элементов исполнимо здесь, из них 143 нативно, 56 только через понижение, 1 вне X3.9, и это не утверждение о нативной поддержке полного F77 в 4.13.

Alternative English variant if the product wording is English:

> FOREX 5.00 covers all 200 F77 matrix elements in the available 2.02-based contour (143 native, 56 lowered via F77PREP/F77LIBR, 1 outside X3.9), which is not a claim of native full F77 support in FOREX 4.13.

## 8. Flagged rows: evidence missing, stale, or ambiguous

### 8.1 Structural, not row-specific

* `01-f77-standard-matrix.md:3` names the repo as `/tmp/.private/azizz/opencode/re-forex`;
  the live tree is `/home/azizz/Yandex.Disk/re-forex`. All relative evidence paths
  must be read against the current tree.
* §0.2 (`:36-37`), §12.1 (`:410,412-414`) and §12.3 (`:438`) disagree about the
  meaning of OK/PARTIAL. Detailed in section 1 above.
* `01-f77-standard-matrix.md:424` says 34 UNKNOWN remain in C/E/F/G/H/J, which
  contradicts the 200/0/0/0 table at `:410` and the history at `:468-475`. Stale text.
* `01-f77-standard-matrix.md:422-423` says 49 numeric plus 17 negative-control
  rows, then silently reinterprets the 17 `ОТСУТСТВУЕТ` diagnostics as coverage, which
  `12-intrinsics-coverage.md:23-36` justifies only as an indirect "native or inline"
  signal. Needs the explicit K05/K06/16-k-closure breakdown proposed in §12.1 above.

### 8.2 Rows with missing or wrong paths

| Row | Matrix line | Problem |
|:---|---:|:---|
| F13 | 157 | Cites `tests/f77/prep-case1.f77`, which does not exist. The real file is `tests/f77/prep-case.f77` (it contains `IMPLICIT NONE`, `SAVE`, `PRINT *`). Also counted inconsistently (see §8.1). |
| G9 | 177 | Cites `tests/f77/output.gold.txt:168-169`, but that file has 4 lines. The cited link-map block appears to be `reference/output.gold.txt:168-169`. |
| I7 | 201 | Cites `tests/f77/output.gold.txt:180`, out of range (file has 4 lines). The `-1 / 1` values are actually on line 3 of that small file. |
| K2 | 254 | `expect_library21.txt:174` is given without `reference/`; line 174 matches `IFIX E *MISTAKE`. |
| K34 | 311 | `expect_library21.txt:312` is off by one and contains `BCDENC*`; the `PCPLOT E AMIN0` entry is line 311. |
| K43 | 325 | `expect_library21.txt:566` is off by one and contains garbage; `DSIGN E ...` is line 565. |
| K4, K7, K8 | 256, 259, 260 | Evidence `01-gap-analysis.md:17` points to probe 11, but `tests/plan-f77/work/INTRINSIC/task.b6` computes only `SQRT(4.0)` and `ABS(-2.0)`. `FLOAT`, `ICHAR`, `CHAR` are absent from `logs/plan_f77_probes.txt`, K05 (`logs/f77_intrinsics_coverage.txt:29`) and `logs/plan_f77_points.txt:45` (SINMOD only). No 2.02 numeric proof for these three rows. |

### 8.3 Rows whose cited evidence exists but does not prove what the label claims

| Row | Matrix line | Problem |
|:---|---:|:---|
| A5 | 71 | Cited `TRUNCATED NAME` is a F77PREP diagnostic with rc=1, not native F77 behaviour. Native 2.02 silently merges long names (`01-gap-analysis.md:80-81`). Matrix "What to do" column still asks for this diagnostic as P0 work. |
| A6 | 72 | Evidence is only "uppercase library source plus lowercase comment in one deck"; no dedicated case-insensitivity probe. Weak, not wrong. |
| A8 | 74 | Native output is `АВСD`, not `ABCD`; exact output requires host `recode.py` (`logs/f77_13_A08.txt:16-30`). Hardware caveat, not a compiler capability. |
| C3 | 100 | Evidence is `ABS(-2.0)` plus a library source line `MYABS=-X`; no isolated unary `+`/`-` probe. |
| C7 | 104 | Evidence is mostly 4.13 Dhrystone corpus; only the glissade part is a 2.02 executable proof. |
| E13 | 134 | `PAUSE` is accepted but is a no-op in a batch deck (`14-control-decl.md:48`); F77 operator-intervention semantics are not demonstrated. |
| F5 | 149 | Cites `kermit.ftn:614,706`; that file was not found in the repository or in the local corpus. The valid part of the evidence is `logs/plan_f77_probes.txt:10` (PARAMETER compiled+ran). |
| F17 | 161 | `*FTN` is mentioned as cross-check only; keep as class (a) but the wording must not suggest cross-only proof. |
| G3 | 171 | "COMPLEX / DOUBLE PRECISION FUNCTION" is evidenced by intrinsic `CABS`/`CSQRT` calls (`07-experiments.md:100-102`, `12-acceptance.md:33`), not by a user-declared COMPLEX or DP FUNCTION. No dedicated probe located. |
| G6 | 174 | By-reference is inferred from the mechanism description in `08-runtime.md:63-66`, not from an isolated argument-mutation test. |
| I5, I6, J14 | 199, 200, 220 | `A` descriptor and Hollerith recipe work on 2.02 only with `INTEGER` + `nH` data. Native `CHARACTER` is rejected on 2.02 and works only on 4.13 (`12-acceptance.md:61-64`, `01-gap-analysis.md:87`). |
| J7, J8 | 213, 214 | Sentinel `-999999.` / `-888888.` branching; matrix itself says "семантика не сохраняется". Not X3.9 `END=`/`ERR=`. |
| J11 | 217 | Native in `15-io.md:51` and `logs/f77_15_gold.txt`, but `03-fortran-path.md:415-419` still lists `E` as requiring an assembler patch. Documentation contradiction; the executable probe wins. |
| J21 | 227 | Probe used `1PE12.4`; `15-io.md:56` itself requires rule R21 to rewrite the canonical comma form `1P,E12.4`. |
| J25, J26 | 231, 232 | Deck prints `POS OK`, but gold `tests/plan-f77-full/unit/J25_rewind/J25_rewind.gold` and `J26_backspace/J26_backspace.gold` contain only a 6-line `IOXNSWAP` block (`logs/f77_15_gold.txt` rows J25/J26, `logs/f77_15_probes.txt` `POSW_REWIND_1`, `POSW_BACKSPACE_1`). No demonstrated rewind/backspace semantics; other LUNs give `НЕТ КАНАЛА` or `ЗАПРЕЩЕННЫЙ РЕЖИМ`. Matrix phrase "чистый прогон" is misleading. |
| J27 | 233 | Clean `РОS ОК` only for LUN 54; LUN 40/45 give `НЕТ КАНАЛА` (`logs/f77_15_probes.txt` `POS_ENDFILE_40/45`). |
| K31, K37 | 303, 314 | `12-intrinsics-coverage.md:76,144,155` records `DMAX1` garbage with 2 arguments and `DMIN1` always zero; wave 16 replaced them with inline expressions. Matrix OK hides that history. |
| K79 | 386 | OK is for the rewritten call `SQRT(X)` (`16-k-closure.md:48`), not for native `DSQRT`. |

### 8.4 Documented external evidence not present in this tree

`dhrystone-forex.dub` (used by rows C2, C5, E1, E6, E8, F3, F7, F9, K4) exists
only in the external corpus `/home/azizz/Yandex.Disk/besm6-new/besm6.net/examples/`,
not in the repository. `glkern.b6` is present at `tests/forex-glissade/glkern.b6`
but the matrix cites it by bare filename. These are historical 4.13 or 2.02
regression artifacts, not reproducible from this tree alone; the 2.02 primary
probes cited alongside most of them remain in-tree.

DONE
