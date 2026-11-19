#!/usr/bin/env bash
# E5: приёмочный набор F77-деков (tests/f77/suite/*.b6).
#
# Для каждого случая:
#   1. свежая рабочая копия диска 2348 с PERSO-библиотекой ФОРЭКС в зоне
#      0o2300 (build/FOREX_PERSO_2300.bin) — дек использует *perso:602300;
#   2. прогон dispak, нормализация дат DD.DD.DD -> ##.##.##;
#   3. выделение блока результата (строки перед "КОНЕЦ ЗАДАЧИ") и сравнение
#      с <case>.gold; печать OK/FAIL;
#   4. кросс-сверка с Fortran-ГДР (*FTN, диск 2048) для случаев из
#      suite/cross-ftn.txt: тот же исходник компилируется *FTN, числовые
#      значения сравниваются с допуском; расхождения пишутся в лог.
#
# При отсутствии dispak, besmtool, эталона диска или PERSO-образа сценарий
# печатает "ОЖИДАЕТСЯ" и возвращает 0 (не падает).
#
# Выход: 0 — все случаи и все кросс-проверки прошли; 1 — иначе.
# Переопределения: DISPAK_BIN, BESMTOOL, ETALON, IMAGE, TIMEOUT.
set -uo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
ROOT=$(CDPATH= cd -- "$(dirname -- "$SCRIPT_DIR")" && pwd) || exit 1

DISPAK_BIN=${DISPAK_BIN:-/home/azizz/Yandex.Disk/dispak/build/dispak/dispak}
BESMTOOL=${BESMTOOL:-besmtool}
ETALON=${ETALON:-/usr/local/share/besm6/2348}
IMAGE=${IMAGE:-$ROOT/build/FOREX_PERSO_2300.bin}
SUITE="$ROOT/tests/f77/suite"
CROSS="$SUITE/cross-ftn.txt"
ZONE_BASE=1216                      # 0o2300
TIMEOUT=${TIMEOUT:-180}
LOG_DIR="$ROOT/logs"
LOG="$LOG_DIR/f77_suite.txt"
CROSS_LOG="$LOG_DIR/f77_cross_ftn.txt"

mkdir -p "$LOG_DIR" || exit 1
: > "$LOG"
: > "$CROSS_LOG"

emit() { printf '%s\n' "$*" | tee -a "$LOG"; }
log()  { printf '%s\n' "$*" >> "$LOG"; }
cross_log() { printf '%s\n' "$*" | tee -a "$CROSS_LOG" >> "$LOG"; }

# --- отыскание общих прототипов исходников (между *forex и *execute) ---
extract_source() {
    python3 - "$1" "$2" <<'PY'
import sys
src, dst = sys.argv[1], sys.argv[2]
lines = open(src, encoding='utf-8', errors='replace').read().splitlines()
i = next(k for k, l in enumerate(lines) if l.strip() == '*forex')
j = next(k for k, l in enumerate(lines) if l.strip() == '*execute')
open(dst, 'w', encoding='utf-8').write('\n'.join(lines[i + 1:j]) + '\n')
PY
}

# --- выделение блока результата (непустые строки перед КОНЕЦ ЗАДАЧИ) ---
extract_result() {
    python3 - "$1" "$2" <<'PY'
import sys
src, dst = sys.argv[1], sys.argv[2]
lines = open(src, encoding='utf-8', errors='replace').read().splitlines()
idx = next((i for i, l in enumerate(lines) if 'КОНЕЦ ЗАДАЧИ' in l), None)
if idx is None:
    raise SystemExit('нет КОНЕЦ ЗАДАЧИ')
j = idx - 1
while j >= 0 and not lines[j].strip():
    j -= 1
k = j
while k >= 0 and lines[k].strip():
    k -= 1
open(dst, 'w', encoding='utf-8').write('\n'.join(lines[k + 1:j + 1]) + '\n')
PY
}

# --- числовая сверка двух блоков вывода ---
compare_numbers() {
    python3 - "$1" "$2" <<'PY'
import re, sys
pat = re.compile(r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EDed][-+]?\d+)?')
def nums(path):
    out = []
    for line in open(path, encoding='utf-8', errors='replace'):
        out.extend(float(t.replace('D', 'E').replace('d', 'E'))
                   for t in pat.findall(line))
    return out
a, b = nums(sys.argv[1]), nums(sys.argv[2])
if len(a) != len(b):
    print('CROSS FAIL: разное число чисел (%d / %d)' % (len(a), len(b)))
    raise SystemExit(1)
for i, (x, y) in enumerate(zip(a, b)):
    if abs(x - y) > max(1e-6, 1e-5 * max(abs(x), abs(y))):
        print('CROSS FAIL: число %d: %r != %r' % (i + 1, x, y))
        raise SystemExit(1)
print('CROSS OK: %d чисел совпали (допуск 1e-5)' % len(a))
PY
}

# ---------------------------------------------------------------- prerequisites
missing=''
[ -x "$DISPAK_BIN" ] || missing="$missing dispak($DISPAK_BIN)"
command -v "$BESMTOOL" >/dev/null 2>&1 || missing="$missing besmtool"
command -v python3 >/dev/null 2>&1 || missing="$missing python3"
[ -f "$ETALON" ] || missing="$missing etalon($ETALON)"
[ -f "$IMAGE" ] || missing="$missing image($IMAGE)"
[ -d "$SUITE" ] || missing="$missing suite($SUITE)"
if [ -n "$missing" ]; then
    emit "ОЖИДАЕТСЯ: F77 suite не запущен — нет:$missing"
    log "Итог: ОЖИДАЕТСЯ (пропущено 0/0)"
    exit 0
fi

TMPROOT=${TMPDIR:-/tmp/.private/azizz/opencode}
[ -d "$TMPROOT" ] || TMPROOT=/tmp
WORK=$(mktemp -d "$TMPROOT/f77-suite.XXXXXX") || { emit "FAIL: mktemp"; exit 1; }
FTNWORK=$(mktemp -d "$TMPROOT/f77-suite-ftn.XXXXXX") || { rm -rf "$WORK"; emit "FAIL: mktemp (ftn)"; exit 1; }
trap 'rm -rf "$WORK" "$FTNWORK"' EXIT

{
    printf '=== E5: F77 acceptance suite ===\n'
    printf 'date    : %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    printf 'dispak  : %s\n' "$DISPAK_BIN"
    printf 'etalon  : %s\n' "$ETALON"
    printf 'image   : %s\n' "$IMAGE"
    printf 'suite   : %s\n' "$SUITE"
} >> "$LOG"

cp "$ETALON" "$WORK/2348" || { emit "FAIL: не удалось скопировать $ETALON"; exit 1; }
BESM6_PATH="$WORK" "$BESMTOOL" write 2348 --from-file="$IMAGE" \
    --start="$ZONE_BASE" >/dev/null 2>>"$LOG" \
    || { emit "FAIL: besmtool write $IMAGE -> zone $ZONE_BASE"; exit 1; }
printf 'job.b6\n' > "$WORK/options.txt"

FATAL='БЫЛИ ОШИБКИ|НЕДОПУСТИМ|ОШИБКА|ERR [0-9]+|ОШ\. ТРАНСЛЯТОРА|ТИП ОП-ДА|ОТСУТСТВУЕТ|ИСПОРЧЕН|АТТ[[:space:]]'

# ---------------------------------------------------------------- basic cases
total=0
passed=0
declare -a BAD=()
for deck in "$SUITE"/*.b6; do
    [ -f "$deck" ] || continue
    case=$(basename "$deck" .b6)
    total=$((total + 1))
    gold="$SUITE/$case.gold"
    if [ ! -f "$gold" ]; then
        emit "FAIL $case: нет $gold"
        BAD+=("$case")
        continue
    fi
    cp "$deck" "$WORK/job.b6" || { emit "FAIL $case: cp"; BAD+=("$case"); continue; }
    ( cd "$WORK" && BESM6_PATH="$WORK:/usr/local/share/besm6" \
        timeout "$TIMEOUT" "$DISPAK_BIN" job.b6 > "$case.raw" 2> "$case.err" )
    rc=$?
    if [ "$rc" -ne 0 ]; then
        emit "FAIL $case: dispak rc=$rc"
        log "--- stderr ---"; log "$(cat "$WORK/$case.err" 2>/dev/null)"
        BAD+=("$case")
        continue
    fi
    sed -E 's/[0-9]{2}\.[0-9]{2}\.[0-9]{2}/##.##.##/g' \
        "$WORK/$case.raw" > "$WORK/$case.norm" \
        || { emit "FAIL $case: нормализация даты"; BAD+=("$case"); continue; }
    if grep -aqE "$FATAL" "$WORK/$case.norm"; then
        emit "FAIL $case: диагностика ФОРЭКС/монитора"
        log "$(grep -aE "$FATAL" "$WORK/$case.norm" | head -5)"
        BAD+=("$case")
        continue
    fi
    if ! extract_result "$WORK/$case.norm" "$WORK/$case.result"; then
        emit "FAIL $case: нет блока результата"
        BAD+=("$case")
        continue
    fi
    if cmp -s "$gold" "$WORK/$case.result"; then
        emit "OK   $case: $(wc -l < "$WORK/$case.result") строк(и) совпали с gold"
        passed=$((passed + 1))
    else
        emit "FAIL $case: вывод отличается от gold"
        log "--- gold / fact ---"
        diff -u "$gold" "$WORK/$case.result" >> "$LOG" 2>&1 || true
        BAD+=("$case")
    fi
done

# ---------------------------------------------------------------- cross vs FTN
cross_total=0
cross_ok=0
if [ -f "$CROSS" ]; then
    while IFS= read -r c || [ -n "$c" ]; do
        c=${c%%#*}
        c=$(printf '%s' "$c" | tr -d '[:space:]')
        [ -n "$c" ] || continue
        cross_total=$((cross_total + 1))
        deck="$SUITE/$c.b6"
        if [ ! -f "$deck" ] || [ ! -f "$WORK/$c.result" ]; then
            cross_log "CROSS FAIL $c: нет decks или результата ФОРЭКС"
            continue
        fi
        if ! extract_source "$deck" "$FTNWORK/$c.f77"; then
            cross_log "CROSS FAIL $c: не удалось выделить исходник"
            continue
        fi
        {
            printf 'шифр 419999 зс5^\n'
            printf 'лен 41(2048)^\n'
            printf 'eeв1а3\n'
            printf '*name F%s\n' "$(printf '%s' "$c" | tr -cd 'A-Za-z0-9' | cut -c1-5)"
            printf '*call yesmemory\n*no list\n*system\n*full list\n*ftn\n'
            cat "$FTNWORK/$c.f77"
            printf '*execute\n*end file\n``````\nеконец\n'
        } > "$FTNWORK/$c.b6" || { cross_log "CROSS FAIL $c: генерация deck"; continue; }
        printf '%s.b6\n' "$c" > "$FTNWORK/options.txt"
        ( cd "$FTNWORK" && BESM6_PATH="$FTNWORK:/usr/local/share/besm6" \
            timeout "$TIMEOUT" "$DISPAK_BIN" "$c.b6" > "$c.raw" 2> "$c.err" )
        rc=$?
        if [ "$rc" -ne 0 ]; then
            cross_log "CROSS FAIL $c: *FTN rc=$rc"
            continue
        fi
        sed -E 's/[0-9]{2}\.[0-9]{2}\.[0-9]{2}/##.##.##/g' \
            "$FTNWORK/$c.raw" > "$FTNWORK/$c.norm"
        if ! extract_result "$FTNWORK/$c.norm" "$FTNWORK/$c.result"; then
            cross_log "CROSS FAIL $c: *FTN не дал результата (см. $CROSS_LOG)"
            continue
        fi
        if res=$(compare_numbers "$WORK/$c.result" "$FTNWORK/$c.result" 2>&1); then
            cross_log "CROSS OK   $c: $res; FOREX: $(tr '\n' '|' < "$WORK/$c.result")"
            cross_ok=$((cross_ok + 1))
        else
            cross_log "CROSS FAIL $c: $res"
            cross_log "  FOREX: $(tr '\n' '|' < "$WORK/$c.result")"
            cross_log "  FTN:   $(tr '\n' '|' < "$FTNWORK/$c.result")"
            BAD+=("$c")
        fi
    done < "$CROSS"
fi

# ---------------------------------------------------------------- summary
emit "Итог: $passed/$total случаев OK; кросс-сверка *FTN: $cross_ok/$cross_total"
if [ "$passed" -eq "$total" ] && [ "$cross_ok" -eq "$cross_total" ] && [ "$total" -gt 0 ]; then
    emit "OK: F77 suite пройден полностью"
    exit 0
fi
emit "FAIL: случаи с ошибками: ${BAD[*]:-нет}"
exit 1
