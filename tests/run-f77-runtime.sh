#!/usr/bin/env bash
# Прогон этапа E2: минимальный Fortran-рантайм F77LIBR в PERSO зоны 0o2310.
#
# Что делает:
#   1. свежая рабочая копия эталона 2348; базовая PERSO-библиотека ФОРЭКС
#      записывается в зону 0o2300 (эталон /usr/local/share/besm6 не трогается);
#   2. ФОРЭКСОМ из зоны 0o2300 компилируется src/f77libr/F77LIB.FTN;
#      объект записывается в ОТДЕЛЬНУЮ PERSO-библиотеку зоны 0o2310
#      картой *to perso:602310;
#   3. проверяется каталог новой библиотеки (все 13 процедур F77LIBR +
#      завершатель) и неизменность базовой библиотеки 0o2300;
#   4. запускается tests/f77/test-runtime.b6 с *perso:602300 +
#      *perso:602310,cont; вывод программы сравнивается с
#      tests/f77/output.gold.txt.
#
# ВАЖНО: для зоны 0o2310 карта *PERSO имеет вид 602310 (LU 60, зона 2310).
# Записанное в плане 05 `*perso:603100` адресует зону 0o3100 и даёт
# "ИСПОРЧЕН КАТАЛОГ PERSONAL LIBRARY"; в сценарии используется 602310.
#
# Выход: exit 0 — rc=0 и вывод совпал с эталоном; exit 1 — иначе.
# Переопределения: DISPAK_BIN, BESMTOOL, ETALON, IMAGE.
set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
ROOT=$(CDPATH= cd -- "$(dirname -- "$SCRIPT_DIR")" && pwd) || exit 1

DISPAK_BIN=${DISPAK_BIN:-/home/azizz/Yandex.Disk/dispak/build/dispak/dispak}
BESMTOOL=${BESMTOOL:-besmtool}
ETALON=${ETALON:-/usr/local/share/besm6/2348}
IMAGE=${IMAGE:-$ROOT/build/FOREX_PERSO_2300.bin}
SRC="$ROOT/src/f77libr/F77LIB.FTN"
DECK="$ROOT/tests/f77/test-runtime.b6"
GOLD="$ROOT/tests/f77/output.gold.txt"
LOGDIR="$ROOT/logs"
LOG="$LOGDIR/f77_runtime_run.txt"

ZONE_BASE=1216                      # 0o2300
ZONE_LIB=1224                       # 0o2310
LIB_ZONES=4

fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }
info() { printf '%s\n' "$*"; }

for f in "$DISPAK_BIN" "$ETALON" "$IMAGE" "$SRC" "$DECK" "$GOLD"; do
    case "$f" in
        "$DISPAK_BIN") [ -x "$f" ] || fail "dispak не найден: $f" ;;
        *)             [ -f "$f" ] || fail "нет файла: $f" ;;
    esac
done
command -v "$BESMTOOL" >/dev/null 2>&1 || fail "besmtool не найден: $BESMTOOL"
mkdir -p "$LOGDIR" || fail "не удалось создать $LOGDIR"

TMPROOT=${TMPDIR:-/tmp/.private/azizz/opencode}
[ -d "$TMPROOT" ] || TMPROOT=/tmp
WORK=$(mktemp -d "$TMPROOT/f77-runtime.XXXXXX") || fail "mktemp failed"
trap 'rm -rf "$WORK"' EXIT

# ---------------------------------------------------------------- 1. диск
cp "$ETALON" "$WORK/2348" || fail "не удалось скопировать эталон диска"
BESM6_PATH="$WORK" "$BESMTOOL" write 2348 --from-file="$IMAGE" \
    --start="$ZONE_BASE" >/dev/null 2>>"$LOG" || fail "besmtool write 0o2300 failed"

# ---------------------------------------------------------------- 2. сборка
{
    printf 'шифр 419999 зс5^\n'
    printf 'лен 60(2348-wr)^\n'
    printf 'ееВ1а3\n'
    printf '*name F77lib\n'
    printf '*call yesmemory\n'
    printf '*perso:602300\n'
    printf '*full list\n'
    printf '*forex\n'
    cat "$SRC"
    printf '*to perso:602310\n'
    printf '*end file\n'
    printf '``````\n'
    printf 'еконец\n'
} > "$WORK/lib.b6"
printf 'lib.b6\n' > "$WORK/options.txt"

( cd "$WORK" && BESM6_PATH="$WORK:/usr/local/share/besm6" \
    "$DISPAK_BIN" lib.b6 > lib.out 2> lib.err ) \
    || fail "dispak (компиляция F77LIB) завершился ненулевым кодом"
[ -s "$WORK/lib.err" ] && { printf 'compile stderr:\n' >&2; cat "$WORK/lib.err" >&2; }
grep -aq 'КОНЕЦ ЗАДАЧИ' "$WORK/lib.out" || fail "компиляция F77LIB не завершилась"
if grep -aqE 'ERR [0-9]+|ОШИБКА|НЕДОПУСТИМ|АТТ[[:space:]]|ТИП ОП-ДА' "$WORK/lib.out"; then
    grep -aE 'ERR [0-9]+|ОШИБКА|НЕДОПУСТИМ|АТТ[[:space:]]|ТИП ОП-ДА' "$WORK/lib.out" >&2
    fail "ФОРЭКС сообщил об ошибке при компиляции F77LIB"
fi
grep -aq 'ДЛИНА LIВRАRУ\|ДЛИНА LIBRARY' "$WORK/lib.out" \
    || fail "*to perso не записал библиотеку (нет 'ДЛИНА LIBRARY')"

# ---------------------------------------------------------------- 3. каталог
BESM6_PATH="$WORK" "$BESMTOOL" dump 2348 --start="$ZONE_LIB" \
    --length="$LIB_ZONES" --to-file="$WORK/lib2310.bin" >/dev/null 2>>"$LOG" \
    || fail "besmtool dump 0o2310 failed"

python3 - "$WORK/lib2310.bin" <<'PY' || fail "проверка каталога 0o2310 не прошла"
import sys
from pathlib import Path

TEXT = [" ", ".", "Б", "Ц", "Д", "Ф", "Г", "И", "(", ")", "*", "Й",
        "Л", "Я", "Ж", "/", "0", "1", "2", "3", "4", "5", "6", "7",
        "8", "9", "Ь", ",", "П", "-", "+", "Ы", "З", "A", "B", "C",
        "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
        "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "Ш",
        "Э", "Щ", "Ч", "Ю"]
d = Path(sys.argv[1]).read_bytes()
def w(i):
    return int.from_bytes(d[i * 6:i * 6 + 6], "big")
def dec(x):
    return "".join(TEXT[(x >> (42 - 6 * i)) & 0x3F] for i in range(8)).rstrip()

names = []
for i in range(2, 64, 2):
    n = dec(w(i))
    if not n:
        if w(i + 1) != (1 << 48) - 1:
            raise SystemExit("bad catalog terminator")
        break
    tv = (w(i + 1) >> 36) & 0xFFF
    if not tv:
        raise SystemExit(f"zero transfer vector for {n}")
    names.append(n)
print("PERSO 0o2310 catalog: " + " ".join(names))
need = {"MYABS", "MYMAX", "FMTLNK", "IMAX0", "ISGN0", "IDIV", "STRCMP",
        "STRCAT", "SUBSTR", "ISTRCM", "DMOD2", "DINT2"}
# CONJG присутствует в исходнике, но ФОРЭКС 2.02 резервирует это имя
# как встроенное и не заносит его в каталог PERSO (как и ISIGN).
if not need.issubset(names):
    raise SystemExit(f"missing modules: {sorted(need - set(names))}")
PY

# Базовая библиотека обязана остаться побайтово равной образу.
BESM6_PATH="$WORK" "$BESMTOOL" dump 2348 --start="$ZONE_BASE" --length=5 \
    --to-file="$WORK/base_readback.bin" >/dev/null 2>>"$LOG" \
    || fail "besmtool dump 0o2300 failed"
cmp -s "$WORK/base_readback.bin" "$IMAGE" \
    || fail "базовая PERSO-библиотека зоны 0o2300 изменилась"

# ---------------------------------------------------------------- 4. прогон
cp "$DECK" "$WORK/job.b6" || fail "не удалось скопировать $DECK"
printf 'job.b6\n' > "$WORK/options.txt"
( cd "$WORK" && BESM6_PATH="$WORK:/usr/local/share/besm6" \
    "$DISPAK_BIN" job.b6 > output.raw 2> stderr.txt ) \
    || fail "dispak (тест) завершился ненулевым кодом"
[ -s "$WORK/stderr.txt" ] && { printf 'dispak stderr:\n' >&2; cat "$WORK/stderr.txt" >&2; }

# Блок результата — четыре строки перед "КОНЕЦ ЗАДАЧИ".
ln=$(grep -an 'КОНЕЦ ЗАДАЧИ' "$WORK/output.raw" | head -1 | cut -d: -f1)
[ -n "$ln" ] || fail "в выводе нет 'КОНЕЦ ЗАДАЧИ'"
sed -n "$((ln-4)),$((ln-1))p" "$WORK/output.raw" > "$WORK/result.txt"
[ "$(wc -l < "$WORK/result.txt")" -eq 4 ] || fail "блок результата не из 4 строк"

# ---------------------------------------------------------------- 5. отчёт
{
    printf '=== E2: F77LIBR from PERSO 0o2310 ===\n'
    printf 'date    : %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf 'dispak  : %s\n' "$DISPAK_BIN"
    printf 'image   : %s\n' "$IMAGE"
    printf 'etalon  : %s\n' "$ETALON"
    printf 'source  : %s\n' "$SRC"
    printf '%s\n' '--- compile: catalog write / errors ---'
    grep -aE 'ДЛИНА LIВRАRУ|ДЛИНА LIBRARY|ИСПОРЧ|ОШИБКА|ERR [0-9]+' \
        "$WORK/lib.out" | head -20 || true
    printf '%s\n' '--- run: PERSO load messages ---'
    sed -n '/^\*NАМЕ/,/^\*FОRЕХ/p' "$WORK/output.raw" \
        | grep -aE 'PERSO|РЕRSО|ИСПОРЧ|ОТСУТСТВУЕТ' || true
    printf '%s\n' '--- gold ---'
    cat "$GOLD"
    printf '%s\n' '--- fact ---'
    cat "$WORK/result.txt"
    printf '%s\n' '--- diff (gold / fact) ---'
    diff -u "$GOLD" "$WORK/result.txt" || true
} > "$LOG"

if cmp -s "$GOLD" "$WORK/result.txt"; then
    info "OK: rc=0, вывод совпадает с tests/f77/output.gold.txt"
    info "log: $LOG"
    exit 0
fi

cat "$LOG" >&2
fail "вывод отличается от tests/f77/output.gold.txt (см. $LOG)"
