#!/usr/bin/env bash
# E3: двухпроходная проверка минимального Fortran-preprocessor F77PREP.
#
#   проход 1: ФОРЭКС компилирует F77PREP (исходник с инъецированными DATA
#             с картами исходника) и запускает его; программа печатает
#             числовые записи 777001/777002/777003; host-скрипт собирает
#             из них lowered.f77 с C@-якорями source map;
#   проход 2: ФОРЭКС компилирует и запускает lowered.f77; результат
#             сравнивается с tests/f77/prep-expected.out.
#
# Дополнительно lowered.f77 сверяется с tests/f77/prep-expected.f77.
# Каталог PERSO зоны 0o2300 НЕ изменяется: в рабочую копию диска 2348
# записывается уже собранный build/FOREX_PERSO_2300.bin (как в run-glissade).
#
# Выход: 0 — оба прохода и обе сверки успешны; 1 — иначе.
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
CASE_SRC="$ROOT/tests/f77/prep-case.f77"
EXPECT_LOW="$ROOT/tests/f77/prep-expected.f77"
EXPECT_OUT="$ROOT/tests/f77/prep-expected.out"
LOG_DIR="$ROOT/logs"
LOG1="$LOG_DIR/f77_prep_pass1.txt"
LOG2="$LOG_DIR/f77_prep_pass2.txt"
LOG="$LOG_DIR/f77_prep_test.txt"
ZONE_DEC=1216                       # 0o2300

fail() { printf 'FAIL: %s\n' "$*" >&2; printf 'FAIL: %s\n' "$*" >> "$LOG"; exit 1; }
info() { printf '%s\n' "$*" | tee -a "$LOG"; }

for f in "$DISPAK_BIN" "$ETALON" "$IMAGE" "$FTN" "$TOOLS" "$CASE_SRC" \
         "$EXPECT_LOW" "$EXPECT_OUT"; do
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
    printf '=== F77PREP two-pass test (E3) ===\n'
    printf 'date    : %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf 'dispak  : %s\n' "$DISPAK_BIN"
    printf 'source  : %s\n' "$CASE_SRC"
    printf 'ftn     : %s\n' "$FTN"
} > "$LOG"

cp "$ETALON" "$WORK/2348" || fail "не удалось скопировать эталон диска"
cp "$IMAGE" "$WORK/image.bin" || fail "не удалось скопировать PERSO-образ"
BESM6_PATH="$WORK" "$BESMTOOL" write 2348 --from-file="$WORK/image.bin" \
    --start="$ZONE_DEC" >> "$LOG" 2>&1 || fail "besmtool write failed"
printf 'job options\n' > "$WORK/options.txt"

# ---------------------------------------------------------------- 1. pass1
python3 "$TOOLS" deck1 "$CASE_SRC" "$FTN" "$WORK/pass1.b6" \
    || fail "генерацияdeck1 не удалась"
( cd "$WORK" && BESM6_PATH="$WORK:/usr/local/share/besm6" \
    timeout 180 "$DISPAK_BIN" pass1.b6 > pass1.out 2> pass1.err ) \
    || fail "pass1 dispak завершился ненулевым кодом"
cp "$WORK/pass1.out" "$LOG1"
cp "$WORK/pass1.err" "$LOG_DIR/f77_prep_pass1.err.txt"

# ФОРЭКС печатает фатальные ошибки этими словами.  "АТТ: <имя> УКОРОЧЕН"
# — benign-диагностика листинга (программа при этом работает корректно).
FATAL='БЫЛИ ОШИБКИ ВВОДА|БЫЛИ ОШИБКИ ПРИ ТРАНСЛЯЦИИ|ПЕРЕПОЛНЕНА ПАМЯТЬ|ОШИБКА СПЕЦИФИКАЦИИ ФОРМАТА|НЕДОПУСТИМ'
if grep -aqE "$FATAL" "$WORK/pass1.out"; then
    info "--- pass1 fatal diagnostics ---"
    grep -aE "$FATAL" "$WORK/pass1.out" | head -10 | tee -a "$LOG"
    fail "ошибки компиляции/ввода в pass1 (см. $LOG1)"
fi

python3 "$TOOLS" records "$WORK/pass1.out" "$WORK/recs.json" \
    || fail "не удалось разобрать записи F77PREP (см. $LOG1)"
python3 "$TOOLS" lower "$CASE_SRC" "$WORK/recs.json" "$WORK/lowered.f77" \
    || fail "не удалось собрать lowered.f77"
cp "$WORK/lowered.f77" "$LOG_DIR/f77_prep_lowered.f77"

if ! cmp -s "$EXPECT_LOW" "$WORK/lowered.f77"; then
    info "--- lowered.f77: expected / fact ---"
    diff -u "$EXPECT_LOW" "$WORK/lowered.f77" | head -80 | tee -a "$LOG"
    fail "lowered.f77 отличается от $EXPECT_LOW"
fi
info "PASS1 OK: lowering совпал с эталоном ($(wc -l < "$WORK/lowered.f77") строк)"

# ---------------------------------------------------------------- 2. pass2
python3 "$TOOLS" deck2 "$WORK/lowered.f77" "$WORK/pass2.b6" \
    || fail "генерация deck2 не удалась"
( cd "$WORK" && BESM6_PATH="$WORK:/usr/local/share/besm6" \
    timeout 180 "$DISPAK_BIN" pass2.b6 > pass2.out 2> pass2.err ) \
    || fail "pass2 dispak завершился ненулевым кодом"
cp "$WORK/pass2.out" "$LOG2"
cp "$WORK/pass2.err" "$LOG_DIR/f77_prep_pass2.err.txt"

if grep -aqE "$FATAL" "$WORK/pass2.out"; then
    info "--- pass2 fatal diagnostics ---"
    grep -aE "$FATAL" "$WORK/pass2.out" | head -10 | tee -a "$LOG"
    fail "ошибки компиляции в pass2 (см. $LOG2)"
fi

# Блок результата: между картой *execute и "КОНЕЦ ЗАДАЧИ".
sed -n '/ЕХЕСUТЕ/,/КОНЕЦ ЗАДАЧИ/p' "$WORK/pass2.out" \
    | sed '1d;$d' | sed '/^[[:space:]]*$/d' > "$WORK/result.txt" \
    || fail "не удалось выделить блок результата"
cp "$WORK/result.txt" "$LOG_DIR/f77_prep_result.txt"

if ! cmp -s "$EXPECT_OUT" "$WORK/result.txt"; then
    info "--- program output: expected / fact ---"
    diff -u "$EXPECT_OUT" "$WORK/result.txt" | head -60 | tee -a "$LOG"
    fail "вывод программы отличается от $EXPECT_OUT"
fi
info "PASS2 OK: результат ($(cat "$WORK/result.txt" | tr -d '\n')) совпал с эталоном"
info "OK: обе проверки пройдены (rc=0)"
exit 0
