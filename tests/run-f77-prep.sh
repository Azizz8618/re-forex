#!/usr/bin/env bash
# E3/v2: двухпроходная проверка F77PREP на двух тестовых случаях.
#
#   проход 1: ФОРЭКС компилирует F77PREP (исходник с инъецированными DATA
#             с картами исходника) и запускает его; программа печатает
#             числовые записи 777001/777002/777003; host-скрипт собирает
#             из них lowered.f77 с C@-якорями source map;
#   проход 2: ФОРЭКС компилирует и запускает lowered.f77; результат
#             сравнивается с prep-expected.out / prep-case2-expected.out.
#
# Случай 1 (prep-case.f77)   — правила v1: IMPLICIT NONE, SAVE, PRINT *,N.
# Случай 2 (prep-case2.f77)  — правила v2: DO WHILE/END DO, READ END=,
#                              CHARACTER*4, PRINT с двумя переменными.
# Для случая 2 после *execute подаются две карты данных (prep-case2.data).
# Случаи 8/9/10 (v3.1)      — F03 EXTERNAL/INTRINSIC, I02 CHARACTER*10,
#                              K03 CABS -> SQRT/REAL/AIMAG.
# Правила 17/18/19 (autoclose DO WHILE, continuation >72/20, inline
# MAX/MIN/ABS/DIM) классифицируются host-частью prep_tools.py:<F77PREP.FTN>
# компилируется ФОРЭКСОМ с жёстким лимитом памяти, поэтому новые правила
# не добавляются в его собственный исходник.
# Случаи 12-22 (v3.3) — wave-2: rule 25 DO-zero, 26 SAVE, 27 alt return,
# 28 CHARACTER FUNCTION, 29 CHARACTER array, 30 G, 21 P, 4/10 END=/ERR=.
# case19/case20 подают на READ карту-сентинал (-999999. / -888888.).
#
# Случаи 23-26 (v3.4 / волна F / волна G) проверяют rules 34-40:
# F77 file I/O -> PERSO 0o2320 CALL-мост (ZFOPEN/ZFCLOSE/ZFINQ/ZFWRIT/ZFREAD).
# ПО УМОЛЧАНИЮ pass 2 выполняется с РЕАЛЬНЫМ PERSO-мостом АРФЫ агента G1:
#   ZF_IMAGE = tests/plan-f77-full/arfa/FOREX_ARFA_2320.zone  (24 Kb = зона 0o2320 финального
#   образа /var/tmp/p7c-arfa-lib/disks/2348, 13 модулей, Э63+Э70, CV1..CV15).
# Реальный мост использует другой ABI, чем F77PREP-lowering (FM(320) vs
# FM(20); ZFOPEN(NAME,LUN,NZ,IST) vs 3 арг.).  Хостовый адаптер
# tests/plan-f77-full/tools/real_bridge_adapt.py (только в харнессе, НЕ в
# src/f77prep) приводит lowered.f77 к реальному ABI перед pass 2.
#PASS1-сверка lowered.f77 с эталоном при этом сохраняется.
# Оговорка: Э70 переносит ровно 8 слов за вызов; 12-словные буферы кейсов
# 24/26 несут полезную нагрузку в первых 2 словах, поэтому round-trip корректен
# (логи/f77_27_real_bridge_probe.txt).  Старый stub доступен через ZF_STUB=1.
# Каталог PERSO зоны 0o2300 НЕ изменяется: в рабочую копию диска 2348
# записывается уже собранный build/FOREX_PERSO_2300.bin (как в run-glissade).
#
# Выход: 0 — оба прохода обоих случаев и все сверки успешны; 1 — иначе.
# Переопределения: DISPAK_BIN, BESMTOOL, ETALON, IMAGE.
set -uo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
ROOT=$(CDPATH= cd -- "$(dirname -- "$SCRIPT_DIR")" && pwd) || exit 1

DISPAK_BIN=${DISPAK_BIN:-/home/azizz/Yandex.Disk/dispak/build/dispak/dispak}
BESMTOOL=${BESMTOOL:-besmtool}
ETALON=${ETALON:-/usr/local/share/besm6/2348}
IMAGE=${IMAGE:-$ROOT/build/FOREX_PERSO_2300.bin}
# Реальный PERSO 0o2320 (G1, волна G).  Путь можно переопределить, например
# ZF_IMAGE=/var/tmp/p7c-arfa-lib/disks/2348 (весь диск) — тогда зона 0o2320
# вынимается besmtool'ом.  По умолчанию — стабильная копия зоны в репозитории.
ZF_IMAGE=${ZF_IMAGE:-$ROOT/tests/plan-f77-full/arfa/FOREX_ARFA_2320.zone}
ZF_STUB=${ZF_STUB:-0}
REAL_ADAPT="$ROOT/tests/plan-f77-full/tools/real_bridge_adapt.py"
FTN="$ROOT/src/f77prep/F77PREP.FTN"
TOOLS="$ROOT/src/f77prep/prep_tools.py"
CASE1="$ROOT/tests/f77/prep-case.f77"
EXP1_LOW="$ROOT/tests/f77/prep-expected.f77"
EXP1_OUT="$ROOT/tests/f77/prep-expected.out"
CASE2="$ROOT/tests/f77/prep-case2.f77"
EXP2_LOW="$ROOT/tests/f77/prep-case2-expected.f77"
EXP2_OUT="$ROOT/tests/f77/prep-case2-expected.out"
DATA2="$ROOT/tests/f77/prep-case2.data"
# v3.1 cases: F03 EXTERNAL/INTRINSIC, I02 CHARACTER*10, K03 CABS.
CASE8="$ROOT/tests/f77/prep-case8.f77"
EXP8_LOW="$ROOT/tests/f77/prep-case8-expected.f77"
EXP8_OUT="$ROOT/tests/f77/prep-case8-expected.out"
CASE9="$ROOT/tests/f77/prep-case9.f77"
EXP9_LOW="$ROOT/tests/f77/prep-case9-expected.f77"
EXP9_OUT="$ROOT/tests/f77/prep-case9-expected.out"
CASE10="$ROOT/tests/f77/prep-case10.f77"
EXP10_LOW="$ROOT/tests/f77/prep-case10-expected.f77"
EXP10_OUT="$ROOT/tests/f77/prep-case10-expected.out"
# v3.2 case: C6 LOGICAL .EQV./.NEQV. -> AND/OR/NOT (rule 23).
CASE11="$ROOT/tests/f77/prep-case11.f77"
EXP11_LOW="$ROOT/tests/f77/prep-case11-expected.f77"
EXP11_OUT="$ROOT/tests/f77/prep-case11-expected.out"
# v3.3 wave-2 host-only lowerings (rules 25-32).
CASE12="$ROOT/tests/f77/prep-case12.f77"
EXP12_LOW="$ROOT/tests/f77/prep-case12-expected.f77"
EXP12_OUT="$ROOT/tests/f77/prep-case12-expected.out"
CASE13="$ROOT/tests/f77/prep-case13.f77"
EXP13_LOW="$ROOT/tests/f77/prep-case13-expected.f77"
EXP13_OUT="$ROOT/tests/f77/prep-case13-expected.out"
CASE14="$ROOT/tests/f77/prep-case14.f77"
EXP14_LOW="$ROOT/tests/f77/prep-case14-expected.f77"
EXP14_OUT="$ROOT/tests/f77/prep-case14-expected.out"
CASE15="$ROOT/tests/f77/prep-case15.f77"
EXP15_LOW="$ROOT/tests/f77/prep-case15-expected.f77"
EXP15_OUT="$ROOT/tests/f77/prep-case15-expected.out"
CASE16="$ROOT/tests/f77/prep-case16.f77"
EXP16_LOW="$ROOT/tests/f77/prep-case16-expected.f77"
EXP16_OUT="$ROOT/tests/f77/prep-case16-expected.out"
CASE17="$ROOT/tests/f77/prep-case17.f77"
EXP17_LOW="$ROOT/tests/f77/prep-case17-expected.f77"
EXP17_OUT="$ROOT/tests/f77/prep-case17-expected.out"
CASE18="$ROOT/tests/f77/prep-case18.f77"
EXP18_LOW="$ROOT/tests/f77/prep-case18-expected.f77"
EXP18_OUT="$ROOT/tests/f77/prep-case18-expected.out"
CASE19="$ROOT/tests/f77/prep-case19.f77"
EXP19_LOW="$ROOT/tests/f77/prep-case19-expected.f77"
EXP19_OUT="$ROOT/tests/f77/prep-case19-expected.out"
DATA19="$ROOT/tests/f77/prep-case19.data"
CASE20="$ROOT/tests/f77/prep-case20.f77"
EXP20_LOW="$ROOT/tests/f77/prep-case20-expected.f77"
EXP20_OUT="$ROOT/tests/f77/prep-case20-expected.out"
DATA20="$ROOT/tests/f77/prep-case20.data"
CASE21="$ROOT/tests/f77/prep-case21.f77"
EXP21_LOW="$ROOT/tests/f77/prep-case21-expected.f77"
EXP21_OUT="$ROOT/tests/f77/prep-case21-expected.out"
CASE22="$ROOT/tests/f77/prep-case22.f77"
EXP22_LOW="$ROOT/tests/f77/prep-case22-expected.f77"
EXP22_OUT="$ROOT/tests/f77/prep-case22-expected.out"
# v3.4 wave F: file I/O -> PERSO 0o2320 bridge (rules 34-40).
CASE23="$ROOT/tests/f77/prep-case23.f77"
EXP23_LOW="$ROOT/tests/f77/prep-case23-expected.f77"
EXP23_OUT="$ROOT/tests/f77/prep-case23-expected.out"
CASE24="$ROOT/tests/f77/prep-case24.f77"
EXP24_LOW="$ROOT/tests/f77/prep-case24-expected.f77"
EXP24_OUT="$ROOT/tests/f77/prep-case24-expected.out"
CASE25="$ROOT/tests/f77/prep-case25.f77"
EXP25_LOW="$ROOT/tests/f77/prep-case25-expected.f77"
EXP25_OUT="$ROOT/tests/f77/prep-case25-expected.out"
CASE26="$ROOT/tests/f77/prep-case26.f77"
EXP26_LOW="$ROOT/tests/f77/prep-case26-expected.f77"
EXP26_OUT="$ROOT/tests/f77/prep-case26-expected.out"
LOG_DIR="$ROOT/logs"
LOG="$LOG_DIR/f77_prep_v2_test.txt"
ZONE_DEC=1216                       # 0o2300

fail() { printf 'FAIL: %s\n' "$*" >&2; printf 'FAIL: %s\n' "$*" >> "$LOG"; exit 1; }
info() { printf '%s\n' "$*" | tee -a "$LOG"; }

[ "$ZF_STUB" = 1 ] || [ -f "$ZF_IMAGE" ] || fail "ZF_IMAGE не найден: $ZF_IMAGE"
for f in "$DISPAK_BIN" "$ETALON" "$IMAGE" "$FTN" "$TOOLS" "$REAL_ADAPT" "$CASE1" \
         "$EXP1_LOW" "$EXP1_OUT" "$CASE2" "$EXP2_LOW" "$EXP2_OUT" "$DATA2" \
         "$CASE8" "$EXP8_LOW" "$EXP8_OUT" "$CASE9" "$EXP9_LOW" "$EXP9_OUT" \
         "$CASE10" "$EXP10_LOW" "$EXP10_OUT" \
         "$CASE11" "$EXP11_LOW" "$EXP11_OUT" \
         "$CASE12" "$EXP12_LOW" "$EXP12_OUT" \
         "$CASE13" "$EXP13_LOW" "$EXP13_OUT" \
         "$CASE14" "$EXP14_LOW" "$EXP14_OUT" \
         "$CASE15" "$EXP15_LOW" "$EXP15_OUT" \
         "$CASE16" "$EXP16_LOW" "$EXP16_OUT" \
         "$CASE17" "$EXP17_LOW" "$EXP17_OUT" \
         "$CASE18" "$EXP18_LOW" "$EXP18_OUT" \
         "$CASE19" "$EXP19_LOW" "$EXP19_OUT" "$DATA19" \
         "$CASE20" "$EXP20_LOW" "$EXP20_OUT" "$DATA20" \
         "$CASE21" "$EXP21_LOW" "$EXP21_OUT" \
         "$CASE22" "$EXP22_LOW" "$EXP22_OUT" \
         "$CASE23" "$EXP23_LOW" "$EXP23_OUT" \
         "$CASE24" "$EXP24_LOW" "$EXP24_OUT" \
         "$CASE25" "$EXP25_LOW" "$EXP25_OUT" \
         "$CASE26" "$EXP26_LOW" "$EXP26_OUT"; do
    [ -f "$f" ] || fail "нет файла: $f"
done
[ -x "$DISPAK_BIN" ] || fail "dispak не исполняем: $DISPAK_BIN"
command -v "$BESMTOOL" >/dev/null 2>&1 || fail "besmtool не найден: $BESMTOOL"
command -v python3 >/dev/null 2>&1 || fail "python3 не найден"

TMPROOT=${TMPDIR:-/tmp/.private/azizz/opencode}
[ -d "$TMPROOT" ] || TMPROOT=/tmp
WORK=$(mktemp -d "$TMPROOT/f77-prep.XXXXXX") || fail "mktemp failed"
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$LOG_DIR" || fail "не удалось создать $LOG_DIR"

{
    printf '=== F77PREP v2 two-pass test ===\n'
    printf 'date    : %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf 'dispak  : %s\n' "$DISPAK_BIN"
    printf 'ftn     : %s\n' "$FTN"
    printf 'case1   : %s\n' "$CASE1"
    printf 'case2   : %s\n' "$CASE2"
} > "$LOG"

cp "$ETALON" "$WORK/2348" || fail "не удалось скопировать эталон диска"
cp "$IMAGE" "$WORK/image.bin" || fail "не удалось скопировать PERSO-образ"
BESM6_PATH="$WORK" "$BESMTOOL" write 2348 --from-file="$WORK/image.bin" \
    --start="$ZONE_DEC" >> "$LOG" 2>&1 || fail "besmtool write failed"
printf 'job options\n' > "$WORK/options.txt"

# --- PERSO 0o2320: real G1 ARFA bridge by default, stub via ZF_STUB=1 ------
if [ "$ZF_STUB" != 1 ]; then
    [ -f "$ZF_IMAGE" ] || fail "ZF_IMAGE не найден: $ZF_IMAGE"
    ZFSIZE=$(wc -c < "$ZF_IMAGE")
    if [ "$ZFSIZE" -gt 1048576 ]; then
        # Whole 2348 disk (e.g. /var/tmp/p7c-arfa-lib/disks/2348):
        # extract the 4-zone 0o2320 PERSO image.
        ZF2320="$WORK/zf2320_from_disk.bin"
        BESM6_PATH=$(dirname "$ZF_IMAGE") BESMTOOL="$BESMTOOL" \
            "$BESMTOOL" dump "$(basename "$ZF_IMAGE")" --start=1232 \
            --length=4 --to-file="$ZF2320" >> "$LOG" 2>&1 \
            || fail "не удалось вынуть зону 0o2320 из $ZF_IMAGE"
    else
        ZF2320="$ZF_IMAGE"
    fi
    REAL_MODE=1
    printf 'ZF bridge  : РЕАЛЬНЫЙ PERSO АРФЫ (G1), image=%s sha256=%s\n' \
        "$ZF_IMAGE" "$(sha256sum "$ZF2320" | cut -d' ' -f1)" >> "$LOG"
    printf 'ZF bridge  : РЕАЛЬНЫЙ PERSO АРФЫ (G1), image=%s\n' "$ZF_IMAGE" | tee -a "$LOG"
else
    REAL_MODE=0
    printf 'ZF bridge  : ZF-stub (ZF_STUB=1)\n' | tee -a "$LOG"
    cat > "$WORK/zfstub.FTN" <<'ZFSTUB_EOF'
c---- Test-only PERSO 0o2320 bridge for F77 file-I/O lowering (doc 34).
c---- Five ZF* entries share COMMON /FILMAP/ FM(20) with the caller.
      SUBROUTINE ZFOPEN(NA,LU,IS)
      INTEGER NA(2),LU,IS
      INTEGER FM(20)
      COMMON /FILMAP/ FM
      FM(1)=0
      FM(2)=1
      FM(3)=1
      FM(8)=0
      END
      SUBROUTINE ZFCLOSE(LU,DL,IS)
      INTEGER LU,DL,IS
      INTEGER FM(20)
      COMMON /FILMAP/ FM
      FM(2)=0
      FM(8)=0
      FM(1)=0
      END
      SUBROUTINE ZFINQ(LU,OP,EX,IS)
      INTEGER LU,OP,EX,IS
      INTEGER FM(20)
      COMMON /FILMAP/ FM
      OP=FM(2)
      EX=FM(3)
      FM(1)=0
      END
      SUBROUTINE ZFWRIT(LU,BU,N,IS)
      INTEGER LU,BU(20),N,IS
      INTEGER FM(20)
      COMMON /FILMAP/ FM
      INTEGER I
      DO 10 I=1,N
        FM(8+I)=BU(I)
   10 CONTINUE
      FM(8)=N
      FM(1)=0
      END
      SUBROUTINE ZFREAD(LU,BU,N,IS)
      INTEGER LU,BU(20),N,IS
      INTEGER FM(20)
      COMMON /FILMAP/ FM
      INTEGER I
      IF (FM(8) .EQ. 0) GO TO 30
      DO 20 I=1,N
        BU(I)=FM(8+I)
   20 CONTINUE
      FM(8)=0
      FM(1)=0
      RETURN
   30 FM(1)=-1
      END
ZFSTUB_EOF
    {
        printf 'шифр 419999 зс5^\n'
        printf 'лен 60(2348-wr)^\n'
        printf 'ееВ1а3\n'
        printf '*name ZFSTUB\n'
        printf '*call yesmemory\n'
        printf '*perso:602300\n'
        printf '*full list\n'
        printf '*forex\n'
        cat "$WORK/zfstub.FTN"
        printf '*to perso:602320\n'
        printf '*end file\n'
        printf '``````\n'
        printf 'еконец\n'
    } > "$WORK/zflib.b6"
    printf 'zflib.b6\n' > "$WORK/zflib.options"
    ( cd "$WORK" && BESM6_PATH="$WORK:/usr/local/share/besm6" \
        timeout 180 "$DISPAK_BIN" zflib.b6 > zflib.out 2> zflib.err ) \
        || fail "сборка PERSO ZF-stub завершилась ненулевым кодом"
    grep -aq 'ДЛИНА LIВRАRУ\|ДЛИНА LIBRARY' "$WORK/zflib.out" \
        || fail "*to perso:602320 не записал ZF-stub"
    ZF2320="$WORK/zf2320.bin"
    BESM6_PATH="$WORK" "$BESMTOOL" dump 2348 --start=1232 --length=4 \
        --to-file="$ZF2320" >> "$LOG" 2>&1 || fail "besmtool dump 0o2320 failed"
fi
BESM6_PATH="$WORK" "$BESMTOOL" write 2348 --from-file="$ZF2320" \
    --start=1232 >> "$LOG" 2>&1 || fail "besmtool write 0o2320 failed"

# ФОРЭКС печатает фатальные ошибки этими словами.  "АТТ: <имя> УКОРОЧЕН"
# — benign-диагностика листинга (программа при этом работает корректно).
FATAL='БЫЛИ ОШИБКИ ВВОДА|БЫЛИ ОШИБКИ ПРИ ТРАНСЛЯЦИИ|ПЕРЕПОЛНЕНА ПАМЯТЬ|ОШИБКА СПЕЦИФИКАЦИИ ФОРМАТА|НЕДОПУСТИМ|ОШИБКА ВВОДА|НЕТ КАНАЛА|I/О-ЕRRОR'

run_case() {
    local TAG=$1 SRC=$2 EXP_LOW=$3 EXP_OUT=$4 DATA=$5
    local CLOG="$LOG_DIR/f77_prep_v2_${TAG}.txt"
    local P1LOG="$LOG_DIR/f77_prep_v2_pass1_${TAG}.txt"
    local P2LOG="$LOG_DIR/f77_prep_v2_pass2_${TAG}.txt"
    local LOWLOG="$LOG_DIR/f77_prep_v2_lowered_${TAG}.f77"
    local RESLOG="$LOG_DIR/f77_prep_v2_result_${TAG}.txt"

    {
        printf '=== F77PREP v2 case %s ===\n' "$TAG"
        printf 'date    : %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
        printf 'source  : %s\n' "$SRC"
        printf 'data    : %s\n' "${DATA:-(none)}"
    } > "$CLOG"

    # ------------------------------------------------------------- pass 1
    python3 "$TOOLS" deck1 "$SRC" "$FTN" "$WORK/${TAG}_p1.b6" \
        || fail "[$TAG] генерация deck1 не удалась"
    ( cd "$WORK" && BESM6_PATH="$WORK:/usr/local/share/besm6" \
        timeout 180 "$DISPAK_BIN" "${TAG}_p1.b6" > "${TAG}_p1.out" 2> "${TAG}_p1.err" ) \
        || fail "[$TAG] pass1 dispak завершился ненулевым кодом"
    cp "$WORK/${TAG}_p1.out" "$P1LOG"
    cp "$WORK/${TAG}_p1.err" "$LOG_DIR/f77_prep_v2_pass1_${TAG}.err.txt"

    if grep -aqE "$FATAL" "$WORK/${TAG}_p1.out"; then
        info "[$TAG] --- pass1 fatal diagnostics ---"
        grep -aE "$FATAL" "$WORK/${TAG}_p1.out" | head -10 | tee -a "$LOG" "$CLOG"
        fail "[$TAG] ошибки компиляции/ввода в pass1 (см. $P1LOG)"
    fi

    python3 "$TOOLS" records "$WORK/${TAG}_p1.out" "$WORK/${TAG}_recs.json" \
        || fail "[$TAG] не удалось разобрать записи F77PREP"
    python3 "$TOOLS" lower "$SRC" "$WORK/${TAG}_recs.json" "$WORK/${TAG}_lowered.f77" \
        || fail "[$TAG] не удалось собрать lowered.f77"
    cp "$WORK/${TAG}_lowered.f77" "$LOWLOG"

    if ! cmp -s "$EXP_LOW" "$WORK/${TAG}_lowered.f77"; then
        info "[$TAG] --- lowered.f77: expected / fact ---"
        diff -u "$EXP_LOW" "$WORK/${TAG}_lowered.f77" | head -80 | tee -a "$LOG" "$CLOG"
        fail "[$TAG] lowered.f77 отличается от $EXP_LOW"
    fi
    info "[$TAG] PASS1 OK: lowering совпал с эталоном ($(wc -l < "$WORK/${TAG}_lowered.f77") строк)"

    # Реальный PERSO 0o2320 имеет иной ABI, чем F77PREP-lowering.  Адаптер
    # применяется ТОЛЬКО здесь (в харнессе) после PASS1-сверки с эталоном.
    P2SRC="$WORK/${TAG}_lowered.f77"
    if [ "${REAL_MODE:-0}" = 1 ]; then
        python3 "$REAL_ADAPT" "$WORK/${TAG}_lowered.f77" "$WORK/${TAG}_adapted.f77" \
            || fail "[$TAG] real-bridge адаптация не удалась"
        P2SRC="$WORK/${TAG}_adapted.f77"
        cp "$P2SRC" "$LOG_DIR/f77_27_real_adapted_${TAG}.f77"
    fi

    # ------------------------------------------------------------- pass 2
    if [ -n "$DATA" ]; then
        python3 "$TOOLS" deck2 "$P2SRC" "$WORK/${TAG}_p2.b6" "$DATA" \
            || fail "[$TAG] генерация deck2 не удалась"
    else
        python3 "$TOOLS" deck2 "$P2SRC" "$WORK/${TAG}_p2.b6" \
            || fail "[$TAG] генерация deck2 не удалась"
    fi
    ( cd "$WORK" && BESM6_PATH="$WORK:/usr/local/share/besm6" \
        timeout 180 "$DISPAK_BIN" "${TAG}_p2.b6" > "${TAG}_p2.out" 2> "${TAG}_p2.err" ) \
        || fail "[$TAG] pass2 dispak завершился ненулевым кодом"
    cp "$WORK/${TAG}_p2.out" "$P2LOG"
    cp "$WORK/${TAG}_p2.err" "$LOG_DIR/f77_prep_v2_pass2_${TAG}.err.txt"

    if grep -aqE "$FATAL" "$WORK/${TAG}_p2.out"; then
        info "[$TAG] --- pass2 fatal diagnostics ---"
        grep -aE "$FATAL" "$WORK/${TAG}_p2.out" | head -10 | tee -a "$LOG" "$CLOG"
        fail "[$TAG] ошибки компиляции в pass2 (см. $P2LOG)"
    fi

    sed -n '/ЕХЕСUТЕ/,/КОНЕЦ ЗАДАЧИ/p' "$WORK/${TAG}_p2.out" \
        | sed '1d;$d' | sed '/^[[:space:]]*$/d' > "$WORK/${TAG}_result.txt" \
        || fail "[$TAG] не удалось выделить блок результата"
    cp "$WORK/${TAG}_result.txt" "$RESLOG"

    if ! cmp -s "$EXP_OUT" "$WORK/${TAG}_result.txt"; then
        info "[$TAG] --- program output: expected / fact ---"
        diff -u "$EXP_OUT" "$WORK/${TAG}_result.txt" | head -60 | tee -a "$LOG" "$CLOG"
        fail "[$TAG] вывод программы отличается от $EXP_OUT"
    fi
    info "[$TAG] PASS2 OK: результат совпал с эталоном ($(wc -l < "$WORK/${TAG}_result.txt") строк)"

    printf 'OK: case %s: обе проверки пройдены\n' "$TAG" >> "$CLOG"
}

run_case case1 "$CASE1" "$EXP1_LOW" "$EXP1_OUT" ""
run_case case2 "$CASE2" "$EXP2_LOW" "$EXP2_OUT" "$DATA2"
run_case case8 "$CASE8" "$EXP8_LOW" "$EXP8_OUT" ""
run_case case9 "$CASE9" "$EXP9_LOW" "$EXP9_OUT" ""
run_case case10 "$CASE10" "$EXP10_LOW" "$EXP10_OUT" ""
run_case case11 "$CASE11" "$EXP11_LOW" "$EXP11_OUT" ""
run_case case12 "$CASE12" "$EXP12_LOW" "$EXP12_OUT" ""
run_case case13 "$CASE13" "$EXP13_LOW" "$EXP13_OUT" ""
run_case case14 "$CASE14" "$EXP14_LOW" "$EXP14_OUT" ""
run_case case15 "$CASE15" "$EXP15_LOW" "$EXP15_OUT" ""
run_case case16 "$CASE16" "$EXP16_LOW" "$EXP16_OUT" ""
run_case case17 "$CASE17" "$EXP17_LOW" "$EXP17_OUT" ""
run_case case18 "$CASE18" "$EXP18_LOW" "$EXP18_OUT" ""
run_case case19 "$CASE19" "$EXP19_LOW" "$EXP19_OUT" "$DATA19"
run_case case20 "$CASE20" "$EXP20_LOW" "$EXP20_OUT" "$DATA20"
run_case case21 "$CASE21" "$EXP21_LOW" "$EXP21_OUT" ""
run_case case22 "$CASE22" "$EXP22_LOW" "$EXP22_OUT" ""
run_case case23 "$CASE23" "$EXP23_LOW" "$EXP23_OUT" ""
run_case case24 "$CASE24" "$EXP24_LOW" "$EXP24_OUT" ""
run_case case25 "$CASE25" "$EXP25_LOW" "$EXP25_OUT" ""
run_case case26 "$CASE26" "$EXP26_LOW" "$EXP26_OUT" ""

if [ "${REAL_MODE:-0}" = 1 ]; then
    info "OK: все случаи пройдены на РЕАЛЬНОМ PERSO-мосте АРФЫ G1 (rc=0)"
else
    info "OK: все случаи пройдены на ZF-stub (rc=0)"
fi
exit 0
