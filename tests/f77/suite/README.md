# Пакет приёмки F77 (E5)

Восемь деков системного ФОРЭКС 2.02, покрывающих confirmation-подмножество
F77; каждый комплект — `*.b6` (дек) + `*.gold` (ожидаемый блок результата).
Все деки грузят `*perso:602300` и содержат `PROGRAM ...`, чтобы один и тот же
исходник можно было скомпилировать `*FTN` для кросс-сверки.

| Случай | Что проверяет |
|---|---|
| `base` | `INTEGER`/`REAL`, счётный `DO`, `FORMAT(I,F)` |
| `blockif` | `BLOCK IF/THEN/ELSE/ENDIF`, вложенный `ELSE` |
| `do2d` | `DIMENSION A(3,4)`, `DATA`, вложенные `DO`, 2D-индексация |
| `dataparam` | `PARAMETER (N=4)`, `DATA` для `INTEGER`/`REAL` |
| `dpcomplex` | `DOUBLE PRECISION` (`D22.15`), `COMPLEX`, `CABS` |
| `intrinsics_ext` | `SQRT`/`ABS`/`AMOD` + внешняя `FUNCTION` в той же деке |
| `listio`, `listio.f77` | list-directed `PRINT *`, пониженный F77PREP (C@-разметка) |
| `charhollerith` | `INTEGER I; DATA I/4HABCD/; FORMAT(1X,A4)` |

`cross-ftn.txt` перечисляет случаи для кросс-сверки с Fortran-ГДР
(`base`, `do2d`, `intrinsics_ext`).

Запуск и отчёт: `../../run-f77-suite.sh`, `../../../docs/plan-f77/12-acceptance.md`,
логи `../../../logs/f77_suite.txt` и `../../../logs/f77_cross_ftn.txt`.

ВАЖНО: комментарии в исходнике деки должны быть только ASCII (латиница и
`c----` в колонке 1); строчные кириллические символы в картах дают
`ОШИБКА` на вводе.
