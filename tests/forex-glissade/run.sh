#!/usr/bin/env bash
# Регрессионный прогон теста ФОРЭКС на исходниках ГЛИССАДЫ-6.
# Компилирует glkern.b6 СИСТЕМНЫМ ФОРЭКСОМ через dispak (диск 2048),
# нормализует дату и сравнивает вывод с output.gold.txt.
set -u

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/../.." && pwd) || exit 1

DISPAK_BIN=${DISPAK_BIN:-/home/azizz/Yandex.Disk/dispak/build/dispak/dispak}
TEST_DIR="$SCRIPT_DIR"
GOLD="$TEST_DIR/output.gold.txt"
LOG_DIR="$ROOT/logs"
LOG="$LOG_DIR/glissade_test.txt"

fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }

[ -x "$DISPAK_BIN" ] || fail "dispak не найден/не исполняем: $DISPAK_BIN"
[ -f "$TEST_DIR/glkern.b6" ] || fail "нет $TEST_DIR/glkern.b6"
[ -f "$TEST_DIR/options.txt" ] || fail "нет $TEST_DIR/options.txt"
[ -f "$GOLD" ] || fail "нет $GOLD"

TMPROOT=${TMPDIR:-/tmp/.private/azizz/opencode}
[ -d "$TMPROOT" ] || TMPROOT=/tmp
TMP=$(mktemp -d "$TMPROOT/re-forex-glissade.XXXXXX") || fail "не удалось создать временный каталог"
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$LOG_DIR" || fail "не удалось создать $LOG_DIR"

cp "$TEST_DIR/glkern.b6" "$TEST_DIR/options.txt" "$TMP/" || fail "копирование входных файлов"

normalize() {
    sed -E 's/[0-9]{2}\.[0-9]{2}\.[0-9]{2}/##.##.##/g' "$1"
}

{
    printf '=== glissade/FOREX regression ===\n'
    printf 'dispak: %s\n' "$DISPAK_BIN"
    printf 'task:   %s\n' "$TEST_DIR/glkern.b6"
    printf 'gold:   %s\n' "$GOLD"
    printf 'date:   %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$LOG"

( cd "$TMP" && "$DISPAK_BIN" glkern.b6 > output.raw 2> stderr.txt )
rc=$?
if [ "$rc" -ne 0 ]; then
    printf 'dispak rc=%d\n' "$rc" >> "$LOG"
    cat "$TMP/stderr.txt" >> "$LOG" 2>/dev/null
    fail "dispak завершился с кодом $rc (см. $LOG)"
fi
if [ -s "$TMP/stderr.txt" ]; then
    printf 'dispak stderr (не пуст):\n' >> "$LOG"
    cat "$TMP/stderr.txt" >> "$LOG"
fi

( cd "$TMP" && "$DISPAK_BIN" glkern.b6 > output2.raw 2> stderr2.txt )
rc2=$?
if [ "$rc2" -ne 0 ]; then
    fail "второй прогон dispak завершился с кодом $rc2"
fi

normalize "$TMP/output.raw" > "$TMP/output.norm" || fail "нормализация вывода"
normalize "$TMP/output2.raw" > "$TMP/output2.norm" || fail "нормализация второго прогона"
normalize "$GOLD" > "$TMP/gold.norm" || fail "нормализация эталона"

printf 'raw bytes:  %s\n' "$(wc -c < "$TMP/output.raw")" >> "$LOG"
printf 'gold bytes: %s\n' "$(wc -c < "$GOLD")" >> "$LOG"

if cmp -s "$TMP/output.norm" "$TMP/output2.norm"; then
    printf 'DETERMINISTIC: два прогона совпадают (после нормализации даты)\n' >> "$LOG"
else
    fail "два прогона dispak дали разный вывод"
fi

if cmp -s "$TMP/gold.norm" "$TMP/output.norm"; then
    printf 'OK: вывод совпадает с эталоном (после нормализации даты)\n' | tee -a "$LOG"
    exit 0
fi

printf '--- первые различия (эталон / факт) ---\n' | tee -a "$LOG"
diff -u "$TMP/gold.norm" "$TMP/output.norm" | head -80 >> "$LOG" 2>&1
cat "$LOG" >&2
fail "вывод dispak отличается от output.gold.txt"
