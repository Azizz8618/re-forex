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
#
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
FTN="$ROOT/src/f77prep/F77PREP.FTN"
TOOLS="$ROOT/src/f77prep/prep_tools.py"
CASE1="$ROOT/tests/f77/prep-case.f77"
EXP1_LOW="$ROOT/tests/f77/prep-expected.f77"
EXP1_OUT="$ROOT/tests/f77/prep-expected.out"
CASE2="$ROOT/tests/f77/prep-case2.f77"
EXP2_LOW="$ROOT/tests/f77/prep-case2-expected.f77"
EXP2_OUT="$ROOT/tests/f77/prep-case2-expected.out"
DATA2="$ROOT/tests/f77/prep-case2.data"
LOG_DIR="$ROOT/logs"
LOG="$LOG_DIR/f77_prep_v2_test.txt"
ZONE_DEC=1216                       # 0o2300

fail() { printf 'FAIL: %s\n' "$*" >&2; printf 'FAIL: %s\n' "$*" >> "$LOG"; exit 1; }
info() { printf '%s\n' "$*" | tee -a "$LOG"; }

for f in "$DISPAK_BIN" "$ETALON" "$IMAGE" "$FTN" "$TOOLS" "$CASE1" \
         "$EXP1_LOW" "$EXP1_OUT" "$CASE2" "$EXP2_LOW" "$EXP2_OUT" "$DATA2"; do
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

    # ------------------------------------------------------------- pass 2
    if [ -n "$DATA" ]; then
        python3 "$TOOLS" deck2 "$WORK/${TAG}_lowered.f77" "$WORK/${TAG}_p2.b6" "$DATA" \
            || fail "[$TAG] генерация deck2 не удалась"
    else
        python3 "$TOOLS" deck2 "$WORK/${TAG}_lowered.f77" "$WORK/${TAG}_p2.b6" \
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

info "OK: оба случая пройдены (rc=0)"
exit 0
