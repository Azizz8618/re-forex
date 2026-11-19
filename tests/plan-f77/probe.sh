#!/bin/bash
# Пробы: какие конструкции FORTRAN 77 реально компилирует ФОРЭКС.
# Используется системный ФОРЭКС 2.02 на диске 2048 (эталонная среда).
set -u
cd "$(dirname "$0")/../.." || exit 1
DISPAK=${DISPAK_BIN:-/home/azizz/Yandex.Disk/dispak/build/dispak/dispak}
OUT=logs/plan_f77_probes.txt
mkdir -p logs tests/plan-f77/work
: > "$OUT"

probe() {
    name=$1; shift
    d=tests/plan-f77/work/$name
    mkdir -p "$d"
    {
        printf 'шифр 419999 зс5^\nлен 41(2048)^\neeв1а3\n'
        printf '*name %s\n*call yesmemory\n*no list\n*forex\n' "$name"
        printf '%s\n' "$@"
        printf '*execute\n*end file\n``````\nеконец\n'
    } > "$d/task.b6"
    (cd "$d" && "$DISPAK" task.b6 > out.txt 2>&1)
    # ФОРЭКС печатает ошибки разными словами: ERR nn, АТТ, ТИП ОП-ДА, ОШИБКА,
    # НЕДОПУСТИМ. «КОНЕЦ ЗАДАЧИ» НЕ является признаком успеха.
    if grep -qE 'ERR [0-9]+|ОШИБКА|ОШ\. ТРАНСЛЯТОРА|НЕДОПУСТИМ|АТТ[[:space:]]|ТИП ОП-ДА|UNRECOGNIZED' "$d/out.txt"; then
        printf 'FAIL %-14s %s\n' "$name" "$(grep -m1 -E 'ERR [0-9]+|ОШИБКА|ОШ\. ТРАНСЛЯТОРА|НЕДОПУСТИМ|АТТ[[:space:]]|ТИП ОП-ДА|UNRECOGNIZED' "$d/out.txt")" >> "$OUT"
    elif grep -q 'КОНЕЦ ЗАДАЧИ' "$d/out.txt"; then
        printf 'OK   %-14s compiled+ran\n' "$name" >> "$OUT"
    else
        printf '???? %-14s no result\n' "$name" >> "$OUT"
    fi
}

probe BASE       '      X=1.0' '      Y=X+2.0' '      PRINT 10,Y' '   10 FORMAT(1X,F8.2)' '      STOP' '      END'
probe DOLOOP     '      DO 10 I=1,5' '   10 CONTINUE' '      STOP' '      END'
probe BLOCKIF    '      X=1.0' '      IF (X .GT. 0.0) THEN' '        Y=2.0' '      ELSE' '        Y=3.0' '      ENDIF' '      STOP' '      END'
probe CHARSTAR   '      CHARACTER*10 S' "      S='ABCDE'" '      PRINT 10,S(2:4)' '   10 FORMAT(1X,A4)' '      STOP' '      END'
probe DOUBLPR    '      DOUBLE PRECISION X' '      X=1.0D0' '      Y=SNGL(X)' '      STOP' '      END'
probe COMPLEX    '      COMPLEX Z' '      Z=(1.0,2.0)' '      STOP' '      END'
probe LISTDIR    '      N=5' '      PRINT *,N' '      STOP' '      END'
probe DATAST     '      DATA N/5/' '      PRINT 10,N' '   10 FORMAT(1X,I4)' '      STOP' '      END'
probe IMPLICIT   '      IMPLICIT NONE' '      INTEGER N' '      N=5' '      STOP' '      END'
probe PARAMETER  '      PARAMETER (N=5)' '      PRINT 10,N' '   10 FORMAT(1X,I4)' '      STOP' '      END'
probe INTRINSIC  '      X=SQRT(4.0)' '      Y=ABS(-2.0)' '      STOP' '      END'
probe EXTERNAL   '      X=FOO(2.0)' '      STOP' '      END'
probe ENDREAD    '      READ(*,*,END=99) X' '   99 CONTINUE' '      STOP' '      END'
probe SAVE       '      SUBROUTINE SUB(X)' '      SAVE N' '      N=1' '      X=N' '      RETURN' '      END'
probe LOGICAL    '      LOGICAL L' '      L=.TRUE.' '      IF (L) GOTO 10' '   10 CONTINUE' '      STOP' '      END'

cat "$OUT"
