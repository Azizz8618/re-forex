#!/usr/bin/env bash
# Прогон вычислительного теста ГЛИССАДЫ с реконструированным ФОРЭКСОМ
# из PERSO зоны 0o2300 рабочей копии диска 2348 и сравнение с эталоном.
#
# Что делает:
#   1. проверяет каталог полного PERSO-образа (9 модулей, transfer vector,
#      завершатель (0, FULWORD)) и пишет его в зону 1216 (=0o2300) СВЕЖЕЙ
#      рабочей копии 2348 (эталон /usr/local/share/besm6/2348 только читается);
#   2. собирает деку *PERSO:602300 + *FOREX + исходник glkern.b6;
#   3. запускает dispak и сохраняет вывод в output.new.txt;
#   4. сравнивает 14 строк результата с output.gold.txt (нормализация дат).
# Все 9 модулей (включая DATAPR*, OCTTDEC, GIV/PG, TAK/PG) грузятся из PERSO.
#
# Выход: exit 0 — результат совпал с эталоном; exit 1 — нет.
#
# Переопределения: DISPAK_BIN, BESMTOOL, ETALON, IMAGE.
set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
ROOT=$(CDPATH= cd -- "$(dirname -- "$SCRIPT_DIR")" && pwd) || exit 1

DISPAK_BIN=${DISPAK_BIN:-/home/azizz/Yandex.Disk/dispak/build/dispak/dispak}
BESMTOOL=${BESMTOOL:-besmtool}
ETALON=${ETALON:-/usr/local/share/besm6/2348}
IMAGE=${IMAGE:-$ROOT/build/FOREX_PERSO_2300.bin}
TEST_DIR="$ROOT/tests/forex-glissade"
GOLD="$TEST_DIR/output.gold.txt"
LOG_DIR="$ROOT/logs"
LOG="$LOG_DIR/glissade_run_full.txt"
OUT="$TEST_DIR/output.new.txt"
ZONE_DEC=1216                       # 0o2300

fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }
info() { printf '%s\n' "$*"; }

[ -x "$DISPAK_BIN" ] || fail "dispak не найден: $DISPAK_BIN"
[ -x "$(command -v "$BESMTOOL")" ] || fail "besmtool не найден: $BESMTOOL"
[ -f "$ETALON" ] || fail "нет эталонного диска: $ETALON"
[ -f "$IMAGE" ] || fail "нет образа PERSO: $IMAGE (сначала tools/build_forex_perso.py)"
[ -f "$TEST_DIR/glkern.b6" ] || fail "нет $TEST_DIR/glkern.b6"
[ -f "$GOLD" ] || fail "нет $GOLD"

TMPROOT=${TMPDIR:-/tmp/.private/azizz/opencode}
[ -d "$TMPROOT" ] || TMPROOT=/tmp
WORK=$(mktemp -d "$TMPROOT/glissade-forex.XXXXXX") || fail "mktemp failed"
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$LOG_DIR" || fail "не удалось создать $LOG_DIR"

# ---------------------------------------------------------------- 1. образ
cp "$ETALON" "$WORK/2348" || fail "не удалось скопировать эталон диска"
cp "$IMAGE" "$WORK/image.bin" || fail "не удалось скопировать PERSO-образ"

# Проверка структуры каталога: 9 модулей, ненулевой transfer vector у всех,
# завершатель — пара (0, FULWORD). Образ НЕ модифицируется.
python3 - "$WORK/image.bin" <<'PY' || fail "PERSO catalog validation failed"
import sys
from pathlib import Path
d = Path(sys.argv[1]).read_bytes()
WB = 6
def getw(i): return int.from_bytes(d[i*WB:i*WB+WB], "big")
TEXT = [" ", ".", "Б", "Ц", "Д", "Ф", "Г", "И", "(", ")", "*", "Й",
        "Л", "Я", "Ж", "/", "0", "1", "2", "3", "4", "5", "6", "7",
        "8", "9", "Ь", ",", "П", "-", "+", "Ы", "З", "A", "B", "C",
        "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
        "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "Ш",
        "Э", "Щ", "Ч", "Ю"]
def dec(w): return "".join(TEXT[(w >> (42 - 6*i)) & 0x3F] for i in range(8)).rstrip()
names = []
for i in range(2, 20, 2):
    n = dec(getw(i))
    if n:
        names.append(n)
        # TAK/PG — точка входа внутри GIV/PG, у неё TV намеренно нулевой.
        if (getw(i+1) >> 24) == 0 and n not in ("TAK/PG", "XTAKPG"):
            raise SystemExit(f"zero transfer vector for {n} at catalog word {i+1}")
print("PERSO catalog (%d modules): %s" % (len(names), " ".join(names)))
if len(names) != 9:
    raise SystemExit("expected 9 modules in full PERSO library")
if getw(20) != 0 or getw(21) != (1 << 48) - 1:
    raise SystemExit("bad catalog terminator (expected 0, FULWORD)")
print("catalog terminator: (0, FULWORD) OK")
PY

BESM6_PATH="$WORK" "$BESMTOOL" write 2348 --from-file="$WORK/image.bin" \
    --start="$ZONE_DEC" >>"$LOG" 2>&1 || fail "besmtool write failed"

# ---------------------------------------------------------------- 2. дека
{
    printf 'шифр 419999 зс5^\n'
    printf 'лен 60(2348)^\n'
    printf 'ееВ1а3\n'
    printf '*name GlkernRec\n'
    printf '*call yesmemory\n'
    printf '*perso:602300\n'
    printf '*     no list\n'
    printf '*full list\n'
    printf '*forex\n'
    sed -n '10,111p' "$TEST_DIR/glkern.b6"
    printf '*execute\n'
    printf '*end file\n'
    printf '``````\n'
    printf 'еконец\n'
} > "$WORK/job.b6"
printf 'job.b6\n' > "$WORK/options.txt"

# ---------------------------------------------------------------- 3. прогон
( cd "$WORK" && BESM6_PATH="$WORK:/usr/local/share/besm6" \
    "$DISPAK_BIN" job.b6 > output.raw 2> stderr.txt ) || fail "dispak завершился ненулевым кодом"
[ -s "$WORK/stderr.txt" ] && { printf 'dispak stderr:\n' >&2; cat "$WORK/stderr.txt" >&2; }

normalize() { sed -E 's/[0-9]{2}\.[0-9]{2}\.[0-9]{2}/##.##.##/g' "$1"; }
normalize "$WORK/output.raw" > "$WORK/output.norm"
normalize "$GOLD" > "$WORK/gold.norm"
cp "$WORK/output.raw" "$OUT"

# 14 строк результата — между концом листинга и "КОНЕЦ ЗАДАЧИ".
result_block() {
    local f="$1" ln
    ln=$(grep -n 'КОНЕЦ ЗАДАЧИ' "$f" | head -1 | cut -d: -f1)
    [ -n "$ln" ] || return 1
    sed -n "$((ln-14)),$((ln-1))p" "$f"
}
result_block "$WORK/gold.norm"   > "$WORK/gold.res"
result_block "$WORK/output.norm" > "$WORK/out.res" \
    || fail "в выводе нет 'КОНЕЦ ЗАДАЧИ' — компилятор/рантайм не сработали"

# ---------------------------------------------------------------- 4. отчёт
{
    printf '=== glissade / reconstructed FOREX from PERSO 0o2300 ===\n'
    printf 'date      : %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf 'dispak    : %s\n' "$DISPAK_BIN"
    printf 'image     : %s\n' "$IMAGE"
    printf 'etalon    : %s\n' "$ETALON"
    printf 'raw bytes : %s (gold %s)\n' "$(wc -c < "$WORK/output.raw")" "$(wc -c < "$GOLD")"
    printf '%s\n' '--- monitor load messages ---'
    sed -n '/^\*NАМЕ/,/^\*FОRЕХ/p' "$WORK/output.norm" | grep -a -E 'PERSO|РЕRSО|LIВRАRУ|ИСПОРЧ|БИБЛИОТ|НЕТ |ОТСУТСТВ' || true
    printf '%s\n' '--- result block (fact) ---'
    cat "$WORK/out.res"
    printf '%s\n' '--- full normalized diff (gold / fact) ---'
    diff -u "$WORK/gold.norm" "$WORK/output.norm" | head -120 || true
} > "$LOG"

if cmp -s "$WORK/gold.res" "$WORK/out.res"; then
    printf 'OK: 14 строк результата совпадают с эталоном (после нормализации даты)\n' | tee -a "$LOG"
    printf 'output: %s\nlog:    %s\n' "$OUT" "$LOG"
    exit 0
fi

printf '%s\n' '--- различия в блоке результата: gold / fact ---' >> "$LOG"
diff -u "$WORK/gold.res" "$WORK/out.res" >> "$LOG" 2>&1 || true
cat "$LOG" >&2
fail "результат отличается от output.gold.txt (см. $LOG)"
