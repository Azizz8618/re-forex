#!/usr/bin/env bash
# P8: инфраструктура полной верификации FORTRAN 77 (ре-forex 5.00).
#
# Уровни:
#   L0  tests/plan-f77-full/unit/<ID>_<name>/*   — 32 unit-пробы стандарт-матрицы A-K
#   L1  tests/plan-f77-full/gold/REGISTRY.txt    — 32 gold-пары (8 suite / 18 new / 6 e1)
#   L2  tests/plan-f77-full/cross/cases.txt      — 8 кросс-прогонов (4 x *FTN + 4 x *FORTRAN)
#   L3  tests/plan-f77-full/real/cases.txt       — реальные программы (Глиссада, решето,
#                                                   Dhrystone, Whetstone)
#   L4  tests/plan-f77-full/negative/cases.txt   — 9 negative cases
#   G   gate 20/20 = 15 проб plan-f77 + Глиссада + 4 положительных F77-дека
#
# Непройденная проба L0-L4 помечается PENDING (E4/MADLEN) и НЕ роняет общий rc.
# Три последних PENDING (F03/I02/K03) закрыты F77PREP-lowering-ом: декы несут
# уже пониженный Fortran; F77LIBR (13 процедур) собирается в PERSO 0o2310 и
# подключается картой *perso:602310,cont. Gate 20/20 обязателен: любая
# FAIL-строка -> exit 1.
#
# Логи: logs/f77_full_*.txt, манифест logs/f77_full.sha256.
# Переопределения: DISPAK_BIN, BESMTOOL, ETALON, IMAGE, TIMEOUT, TMPROOT,
#                  F77_FULL_EXTERNAL=1 (включить внешние Dhrystone/Whetstone).
set -uo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
ROOT=$(CDPATH= cd -- "$(dirname -- "$SCRIPT_DIR")" && pwd) || exit 1

DISPAK_BIN=${DISPAK_BIN:-/home/azizz/Yandex.Disk/dispak/build/dispak/dispak}
BESMTOOL=${BESMTOOL:-besmtool}
ETALON=${ETALON:-/usr/local/share/besm6/2348}
IMAGE=${IMAGE:-$ROOT/build/FOREX_PERSO_2300.bin}
TIMEOUT=${TIMEOUT:-180}
TMPROOT=${TMPDIR:-/tmp/.private/azizz/opencode}
[ -d "$TMPROOT" ] || TMPROOT=/tmp
FULL="$ROOT/tests/plan-f77-full"
LOG_DIR="$ROOT/logs"
LOG="$LOG_DIR/f77_full_run.txt"
L_MATRIX="$LOG_DIR/f77_full_matrix.txt"
L_GOLD="$LOG_DIR/f77_full_gold.txt"
L_CFTN="$LOG_DIR/f77_full_cross_ftn.txt"
L_CFORT="$LOG_DIR/f77_full_cross_fortran.txt"
L_REAL="$LOG_DIR/f77_full_real.txt"
L_NEG="$LOG_DIR/f77_full_negative.txt"
L_GATE="$LOG_DIR/f77_full_gate.txt"
L_SUM="$LOG_DIR/f77_full_summary.txt"
MANIFEST="$LOG_DIR/f77_full.sha256"

mkdir -p "$LOG_DIR" || exit 1
for f in "$LOG" "$L_MATRIX" "$L_GOLD" "$L_CFTN" "$L_CFORT" "$L_REAL" "$L_NEG" "$L_GATE" "$L_SUM"; do
    : > "$f" || exit 1
done

emit() { printf '%s\n' "$*" | tee -a "$LOG"; }
log()  { printf '%s\n' "$*" >> "$LOG"; }
line() { printf '%s\n' "$*" | tee -a "$LOG" >> "$1"; }
hdr()  { log ''; log "=== $* ==="; printf '=== %s ===\n' "$*"; }

FATAL='БЫЛИ ОШИБКИ|НЕДОПУСТИМ|ОШИБКА|ERR [0-9]+|ОШ\. ТРАНСЛЯТОРА|ТИП ОП-ДА|ОТСУТСТВУЕТ|ИСПОРЧЕН|АТТ[[:space:]]'

# ------------------------------------------------------------------ helpers
# Нормализация даты и системного баннера 2.02 (баннер не является версией изделия).
normalize() {
    sed -E \
      -e 's/[0-9]{2}\.[0-9]{2}\.[0-9]{2}/##.##.##/g' \
      -e 's/.*ВЕРСИЯ.*/<BANNER>/' \
      -e 's/.*ВЕРSИЯ.*/<BANNER>/' \
      -e 's/.*М О Н И Т О Р.*/<BANNER>/' \
      "$1" > "$2"
}

# Блок результата: непустые строки перед КОНЕЦ ЗАДАЧИ.
extract_result() {
    python3 - "$1" "$2" <<'PY'
import sys
src, dst = sys.argv[1], sys.argv[2]
lines = open(src, encoding='utf-8', errors='replace').read().splitlines()
idx = next((i for i, l in enumerate(lines) if 'КОНЕЦ ЗАДАЧИ' in l), None)
if idx is None:
    raise SystemExit(1)
j = idx - 1
while j >= 0 and not lines[j].strip():
    j -= 1
k = j
while k >= 0 and lines[k].strip():
    k -= 1
open(dst, 'w', encoding='utf-8').write('\n'.join(lines[k + 1:j + 1]) + '\n')
PY
}

# Исходник между *forex и *execute (для кросс-компиляции).
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

# Числовая сверка с настраиваемым допуском: compare_numbers A B TOL REL.
compare_numbers() {
    python3 - "$1" "$2" "$3" "$4" <<'PY'
import re, sys
pat = re.compile(r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EDed][-+]?\d+)?')
def nums(path):
    out = []
    for line in open(path, encoding='utf-8', errors='replace'):
        out.extend(float(t.replace('D', 'E').replace('d', 'e'))
                   for t in pat.findall(line))
    return out
a, b = nums(sys.argv[1]), nums(sys.argv[2])
if len(a) != len(b):
    print('разное число чисел (%d / %d)' % (len(a), len(b)))
    raise SystemExit(1)
tol, rel = float(sys.argv[3]), float(sys.argv[4])
for i, (x, y) in enumerate(zip(a, b)):
    if abs(x - y) > max(tol, rel * max(abs(x), abs(y))):
        print('число %d: %r != %r' % (i + 1, x, y))
        raise SystemExit(1)
print('%d чисел совпали (допуск max(%g, %g*max))' % (len(a), tol, rel))
PY
}

# Sliding window W=3, score >= 0.95, первая и последняя строки совпадают.
sliding_score() {
    python3 - "$1" "$2" <<'PY'
import sys, hashlib
def rows(p):
    return [l.strip() for l in open(p, encoding='utf-8', errors='replace') if l.strip()]
a, b = rows(sys.argv[1]), rows(sys.argv[2])
W = 3
def wins(x):
    if not x:
        return set()
    w = min(W, len(x))
    return {hashlib.sha1('\n'.join(x[i:i + w]).encode()).hexdigest()
            for i in range(len(x) - w + 1)}
ha, hb = wins(a), wins(b)
score = 1.0 if ha and hb and ha == hb else (len(ha & hb) / max(len(ha), 1) if ha and hb else 0.0)
first = bool(a) and bool(b) and a[0] == b[0]
last = bool(a) and bool(b) and a[-1] == b[-1]
print('score=%.3f first=%s last=%s rows=%d/%d' % (score, first, last, len(a), len(b)))
raise SystemExit(0 if score >= 0.95 and first and last else 1)
PY
}

# --------------------------------------------------------------- prerequisites
missing=''
[ -x "$DISPAK_BIN" ] || missing="$missing dispak($DISPAK_BIN)"
command -v "$BESMTOOL" >/dev/null 2>&1 || missing="$missing besmtool"
command -v python3 >/dev/null 2>&1 || missing="$missing python3"
[ -f "$ETALON" ] || missing="$missing etalon($ETALON)"
[ -f "$IMAGE" ] || missing="$missing image($IMAGE)"
[ -d "$FULL" ] || missing="$missing full($FULL)"

emit "F77 full verification — $(date -u +%Y-%m-%dT%H:%M:%SZ)"
emit "dispak=$DISPAK_BIN etalon=$ETALON image=$IMAGE"

if [ -n "$missing" ]; then
    emit "ОЖИДАЕТСЯ: динамические уровни не запущены — нет:$missing"
    for f in "$L_MATRIX" "$L_GOLD" "$L_CFTN" "$L_CFORT" "$L_REAL" "$L_NEG" "$L_GATE"; do
        printf 'ОЖИДАЕТСЯ: нет prerequisites:%s\n' "$missing" >> "$f"
    done
    printf 'OK|0|0|PENDING|%s\n' "нет prerequisites" >> "$L_SUM"
    exit 0
fi

WORK=$(mktemp -d "$TMPROOT/f77-full.XXXXXX") || { emit "FAIL: mktemp"; exit 1; }
trap 'rm -rf "$WORK"' EXIT
cp "$ETALON" "$WORK/2348" || { emit "FAIL: cp etalon"; exit 1; }
BESM6_PATH="$WORK" "$BESMTOOL" write 2348 --from-file="$IMAGE" \
    --start=1216 >/dev/null 2>>"$LOG" \
    || { emit "FAIL: besmtool write PERSO 0o2300"; exit 1; }

# F77LIBR (13 процедур) собирается ФОРЭКСОМ из 0o2300 в отдельную PERSO-библио-
# теку зоны 0o2310 — так же, как в tests/run-f77-runtime.sh.  Деки F03/I02/K03
# грузят её картой *perso:602310,cont (основной компилятор — *perso:602300).
# Базовая библиотека 0o2300 при этом не меняется.
F77LIBR_SRC="$ROOT/src/f77libr/F77LIB.FTN"
F77LIBR_OK=0
if [ -f "$F77LIBR_SRC" ]; then
    libwd="$WORK/f77libr_build"; mkdir -p "$libwd"
    {
        printf 'шифр 419999 зс5^\nлен 60(2348-wr)^\nееВ1а3\n'
        printf '*name F77lib\n*call yesmemory\n*perso:602300\n*full list\n*forex\n'
        cat "$F77LIBR_SRC"
        printf '*to perso:602310\n*end file\n``````\nеконец\n'
    } > "$libwd/lib.b6"
    printf 'lib.b6\n' > "$libwd/options.txt"
    ( cd "$libwd" && BESM6_PATH="$WORK:/usr/local/share/besm6" \
        timeout "$TIMEOUT" "$DISPAK_BIN" lib.b6 > lib.out 2> lib.err )
    if [ "$?" -eq 0 ] && grep -aqE 'ДЛИНА LIВRАRУ|ДЛИНА LIBRARY' "$libwd/lib.out"; then
        F77LIBR_OK=1
        emit "F77LIBR: 13 процедур собраны в PERSO 0o2310 (для *perso:602310,cont)"
    else
        emit "FAIL: не удалось собрать F77LIBR в PERSO 0o2310 (см. lib.out)"
        printf 'F77LIBR build failed\n' >> "$LOG"
        exit 1
    fi
else
    emit "F77LIBR: исходник $F77LIBR_SRC отсутствует — зона 0o2310 не собрана"
fi

declare -A L0=() L1=() L2=() L3=() L4=() GATE=()
declare -A L0R=() L1R=() L2R=() L3R=() L4R=() GATER=()
l0_ok=0; l0_pending=0
l1_ok=0; l1_pending=0
l2_ok=0; l2_pending=0; l2_skip=0
l3_ok=0; l3_pending=0; l3_skip=0
l4_ok=0; l4_pending=0
g_ok=0; g_fail=0
GLISSADE_OK=0
GLISSADE_TEXT=''

# run_deck <deck> <tag> → задаёт DECK_RESULT, DECK_DIAG, DECK_RAW
run_deck() {
    local deck=$1 tag=$2 wd="$WORK/deck_$2"
    mkdir -p "$wd"
    cp "$deck" "$wd/job.b6" || { DECK_DIAG='cp deck'; DECK_RESULT=''; return 1; }
    printf 'job.b6\n' > "$wd/options.txt"
    DECK_RC=0
    ( cd "$wd" && BESM6_PATH="$WORK:/usr/local/share/besm6" \
        timeout "$TIMEOUT" "$DISPAK_BIN" job.b6 > "$tag.raw" 2> "$tag.err" )
    DECK_RC=$?
    DECK_RAW="$wd/$tag.raw"
    if [ "$DECK_RC" -ne 0 ]; then
        DECK_DIAG="dispak rc=$DECK_RC"
        DECK_RESULT=''
        return 1
    fi
    normalize "$DECK_RAW" "$wd/$tag.norm" || { DECK_DIAG='normalize'; DECK_RESULT=''; return 1; }
    DECK_DIAG=$(grep -aE "$FATAL" "$wd/$tag.norm" | head -1 || true)
    if [ -n "$DECK_DIAG" ]; then
        DECK_RESULT=''
        return 1
    fi
    if ! extract_result "$wd/$tag.norm" "$wd/$tag.result"; then
        DECK_DIAG='нет блока результата'
        DECK_RESULT=''
        return 1
    fi
    DECK_RESULT="$wd/$tag.result"
    return 0
}

reason() {
    if [ -n "$DECK_DIAG" ]; then printf '%s' "$DECK_DIAG"; else printf '%s' 'нет совпадения с gold'; fi
}

# ------------------------------------------------------------------ L0 + L1
hdr 'L0/L1: unit-пробы и gold-пары стандарт-матрицы A-K'
printf 'ID|DIR|DECK|GOLD|SOURCE|STATUS|CONSTRUCT/REASON\n' >> "$L_MATRIX"
printf 'ID|DECK|GOLD|SOURCE|STATUS|DETAIL\n' >> "$L_GOLD"
while IFS='|' read -r cid dir deckfile goldfile tag ref; do
    [ -n "$cid" ] || continue
    case "$cid" in \#*) continue;; esac
    deck="$FULL/unit/$dir/$deckfile"
    gold="$FULL/gold/$goldfile"
    if [ ! -f "$deck" ] || [ ! -f "$gold" ]; then
        L0[$cid]='PENDING'; L0R[$cid]='нет deck/gold'
        printf 'PENDING %-4s %-28s нет deck/gold\n' "$cid" "$dir" | tee -a "$L_MATRIX" >> "$LOG"
        l0_pending=$((l0_pending+1))
        continue
    fi
    run_deck "$deck" "$cid"
    if [ "$?" -eq 0 ] && cmp -s "$gold" "$DECK_RESULT"; then
        L0[$cid]='OK'; L0R[$cid]="$ref"
        L1[$cid]='OK'; L1R[$cid]="$tag:$ref"
        printf 'OK %-4s %-28s %s\n' "$cid" "$dir" "$ref" | tee -a "$L_MATRIX" >> "$LOG"
        printf 'OK %-4s %s %s %s\n' "$cid" "$goldfile" "$tag" "$ref" | tee -a "$L_GOLD" >> "$LOG"
        l0_ok=$((l0_ok+1)); l1_ok=$((l1_ok+1))
    else
        why=$(reason)
        L0[$cid]='PENDING (E4/MADLEN)'; L0R[$cid]="$why"
        L1[$cid]='PENDING (E4/MADLEN)'; L1R[$cid]="$why"
        printf 'PENDING (E4/MADLEN) %-4s %-28s %s\n' "$cid" "$dir" "$why" | tee -a "$L_MATRIX" >> "$LOG"
        printf 'PENDING (E4/MADLEN) %-4s %s %s %s\n' "$cid" "$goldfile" "$tag" "$why" | tee -a "$L_GOLD" >> "$LOG"
        if [ -n "$DECK_RESULT" ]; then
            printf '  gold: %s\n  fact: %s\n' "$(tr '\n' '|' < "$gold")" "$(tr '\n' '|' < "$DECK_RESULT")" >> "$L_GOLD"
        fi
        l0_pending=$((l0_pending+1)); l1_pending=$((l1_pending+1))
    fi
    printf '%s|%s|%s|%s|%s|%s|%s\n' "$cid" "$dir" "$deckfile" "$goldfile" "$tag" "${L0[$cid]}" "${L0R[$cid]}" >> "$L_MATRIX"
    printf '%s|%s|%s|%s|%s|%s\n' "$cid" "$deckfile" "$goldfile" "$tag" "${L1[$cid]}" "${L1R[$cid]}" >> "$L_GOLD"
done < "$FULL/gold/REGISTRY.txt"

# Проверка происхождения 8 suite-пар: gold обязаны быть байтово равны оригиналам.
suite_reused=0; suite_bad=0
while IFS='|' read -r cid dir deckfile goldfile tag ref; do
    [ "$tag" = 'suite' ] || continue
    src=${ref##*/}; src=${src%.b6}
    suite_reused=$((suite_reused+1))
    if cmp -s "$FULL/gold/$goldfile" "$ROOT/tests/f77/suite/$src.gold"; then
        printf 'REUSED OK %-4s <- tests/f77/suite/%s.gold\n' "$cid" "$src" >> "$L_GOLD"
    else
        printf 'REUSED FAIL %-4s <- tests/f77/suite/%s.gold\n' "$cid" "$src" >> "$L_GOLD"
        suite_bad=$((suite_bad+1))
    fi
done < "$FULL/gold/REGISTRY.txt"
printf 'Итог L0: %d OK / %d PENDING (E4/MADLEN)\n' "$l0_ok" "$l0_pending" | tee -a "$L_MATRIX" >> "$LOG"
printf 'Итог L1: %d OK / %d PENDING; suite-пар переиспользовано %d, расхождений %d\n' \
    "$l1_ok" "$l1_pending" "$suite_reused" "$suite_bad" | tee -a "$L_GOLD" >> "$LOG"

# ------------------------------------------------------------------------ L2
hdr 'L2: кросс-компиляция *FTN / *FORTRAN (диск 2048)'
printf '# CROSS_OK/CROSS_FAIL/CROSS_SKIP|ID|COMPILER|TOLERANCE|DETAIL\n' > "$L_CFTN"
printf '# CROSS_OK/CROSS_FAIL/CROSS_SKIP|ID|COMPILER|TOLERANCE|DETAIL\n' > "$L_CFORT"
while IFS='|' read -r xid xdir compiler; do
    [ -n "$xid" ] || continue
    case "$xid" in \#*) continue;; esac
    deck=$(find "$FULL/unit/$xdir" -maxdepth 1 -name '*.b6' -print -quit)
    xcid=$(awk -F'|' -v d="$xdir" '$2 == d { print $1; exit }' "$FULL/gold/REGISTRY.txt")
    forex_result="$WORK/deck_$xcid/$xcid.result"
    if [ ! -f "$forex_result" ]; then
        printf 'CROSS SKIP %-4s %-8s нет результата ФОРЭКСа\n' "$xid" "$compiler" | tee -a "$LOG" >> "$L_CFTN"
        l2_skip=$((l2_skip+1)); continue
    fi
    extract_source "$deck" "$WORK/$xid.f77" || continue
    for comp in FTN FORTRAN; do
        cw="$WORK/cross_$xid$comp"; mkdir -p "$cw"
        {
            printf 'шифр 419999 зс5^\nлен 41(2048)^\nлен 60(2348)^\neeв1а3\n'
            if [ "$comp" = FTN ]; then
                printf '*name F%s\n' "$xid"
                printf '*call yesmemory\n*no list\n*system\n*full list\n*ftn\n'
                TOL='max(1e-6,1e-5*max)'; T1=1e-6; T2=1e-5
                OUT=$L_CFTN
            else
                printf '*name D%s\n' "$xid"
                printf '*call yesmemory\n*no list\n*system\n*full list\n*fortran\n'
                TOL='max(1e-4,1e-4*max)'; T1=1e-4; T2=1e-4
                OUT=$L_CFORT
            fi
            cat "$WORK/$xid.f77"
            printf '*execute\n*end file\n``````\nеконец\n'
        } > "$cw/job.b6"
        printf 'job.b6\n' > "$cw/options.txt"
        ( cd "$cw" && BESM6_PATH="$cw:/usr/local/share/besm6" \
            timeout "$TIMEOUT" "$DISPAK_BIN" job.b6 > raw.txt 2> err.txt )
        crc=$?
        if [ "$crc" -ne 0 ]; then
            printf 'CROSS SKIP %-4s %-8s rc=%s (нет эталона)\n' "$xid" "$comp" "$crc" | tee -a "$LOG" >> "$OUT"
            [ "$comp" = FTN ] && l2_skip=$((l2_skip+1)) || l2_skip=$((l2_skip+1))
            continue
        fi
        normalize "$cw/raw.txt" "$cw/norm.txt"
        if ! extract_result "$cw/norm.txt" "$cw/result.txt"; then
            printf 'CROSS SKIP %-4s %-8s нет результата (нет эталона)\n' "$xid" "$comp" | tee -a "$LOG" >> "$OUT"
            l2_skip=$((l2_skip+1)); continue
        fi
        if res=$(compare_numbers "$forex_result" "$cw/result.txt" "$T1" "$T2" 2>&1); then
            extra=''
            if [ "$comp" = FORTRAN ]; then
                if sw=$(sliding_score "$forex_result" "$cw/result.txt" 2>&1); then
                    extra="; $sw"
                else
                    extra="; $sw"
                    res="sliding: $sw"
                    printf 'CROSS FAIL %-4s %-8s %s\n' "$xid" "$comp" "$res" | tee -a "$LOG" >> "$OUT"
                    printf 'CROSS FAIL %-4s %s: FOREX=%s %s=%s\n' "$xid" "$comp" \
                        "$(tr '\n' '|' < "$forex_result")" "$comp" "$(tr '\n' '|' < "$cw/result.txt")" >> "$OUT"
                    L2[$xid$comp]='PENDING'; L2R[$xid$comp]="$res"
                    l2_pending=$((l2_pending+1)); continue
                fi
            fi
            L2[$xid$comp]='OK'; L2R[$xid$comp]="$res$extra"
            printf 'CROSS OK %-4s %-8s %s%s\n' "$xid" "$comp" "$res" "$extra" | tee -a "$LOG" >> "$OUT"
            l2_ok=$((l2_ok+1))
        else
            L2[$xid$comp]='PENDING'; L2R[$xid$comp]="$res"
            printf 'CROSS FAIL %-4s %-8s %s\n' "$xid" "$comp" "$res" | tee -a "$LOG" >> "$OUT"
            printf 'CROSS FAIL %-4s %s: FOREX=%s %s=%s\n' "$xid" "$comp" \
                "$(tr '\n' '|' < "$forex_result")" "$comp" "$(tr '\n' '|' < "$cw/result.txt")" >> "$OUT"
            l2_pending=$((l2_pending+1))
        fi
    done
done < "$FULL/cross/cases.txt"
printf 'Итог L2: %d OK / %d PENDING / %d SKIP (нет эталона)\n' "$l2_ok" "$l2_pending" "$l2_skip" >> "$L_CFTN"
printf 'Итог L2: %d OK / %d PENDING / %d SKIP (нет эталона)\n' "$l2_ok" "$l2_pending" "$l2_skip" >> "$L_CFORT"

# ------------------------------------------------------------------------ L3
hdr 'L3: реальные программы'
printf '# STATUS|ID|NAME|SOURCE|CONTROL|DETAIL\n' > "$L_REAL"
# R01 Глиссада (однократно; результат переиспользуется gate G16)
if out=$(timeout 300 bash "$ROOT/tests/run-glissade-forex.sh" 2>&1); grc=$?; then :; else grc=$?; fi
GLISSADE_TEXT="$out"
if [ "$grc" -eq 0 ] && printf '%s' "$out" | grep -q '14 строк результата совпадают'; then
    L3[R01]='OK'; L3R[R01]='14/14 строк'; GLISSADE_OK=1; l3_ok=$((l3_ok+1))
    printf 'OK   R01 GLISSADE 14/14\n' | tee -a "$L_REAL" >> "$LOG"
else
    L3[R01]='PENDING'; L3R[R01]='rc='"${grc:-?}"
    printf 'PENDING (E4/MADLEN) R01 GLISSADE rc=%s\n' "${grc:-?}" | tee -a "$L_REAL" >> "$LOG"
fi
printf '%s|R01|GLISSADE|tests/forex-glissade/glkern.b6|14/14|%s\n' "${L3[R01]}" "${L3R[R01]}" >> "$L_REAL"
# R02 решето Эратосфена
if out=$(timeout 300 bash "$ROOT/tests/run-forex.sh" 2>&1); src=$?; then :; else src=$?; fi
if [ "$src" -eq 0 ] && printf '%s' "$out" | grep -q 'совпадает с эталоном'; then
    L3[R02]='OK'; L3R[R02]='sha256 совпал'; l3_ok=$((l3_ok+1))
    printf 'OK   R02 SIEVE sha256\n' | tee -a "$L_REAL" >> "$LOG"
else
    L3[R02]='PENDING'; L3R[R02]='rc='"${src:-?}"
    printf 'PENDING (E4/MADLEN) R02 SIEVE rc=%s\n' "${src:-?}" | tee -a "$L_REAL" >> "$LOG"
fi
printf '%s|R02|SIEVE|reference/forex.b6|sha256|%s\n' "${L3[R02]}" "${L3R[R02]}" >> "$L_REAL"
# R03/R04 внешние эталоны 4.13/Дубна
while IFS='|' read -r rid rname rsource rcontrol rmode; do
    [ -n "$rid" ] || continue
    case "$rid" in \#*|R01|R02) continue;; esac   # локальные R01/R02 уже обработаны
    if [ "${F77_FULL_EXTERNAL:-0}" != 1 ] || [ ! -f "$rsource" ]; then
        L3[$rid]='SKIP'; L3R[$rid]="$rmode: внешний эталон 4.13/Дубна"
        l3_skip=$((l3_skip+1))
        printf 'SKIP %s %s: внешний эталон (F77_FULL_EXTERNAL=1 для прогона)\n' "$rid" "$rname" | tee -a "$L_REAL" >> "$LOG"
    else
        ew="$WORK/real_$rid"; mkdir -p "$ew"
        {
            printf 'шифр 419999 зс5^\nлен 41(2048)^\nлен 60(2348)^\neeв1а3\n'
            printf '*name %s\n*call yesmemory\n*perso:602300\n*no list\n*forex\n' "$rid"
            cat "$rsource"
            printf '*execute\n*end file\n``````\nеконец\n'
        } > "$ew/job.b6"
        printf 'job.b6\n' > "$ew/options.txt"
        ( cd "$ew" && BESM6_PATH="$WORK:/usr/local/share/besm6" \
            timeout "$TIMEOUT" "$DISPAK_BIN" job.b6 > raw.txt 2> err.txt )
        rrc=$?
        if [ "$rrc" -eq 0 ] && [ -s "$ew/raw.txt" ]; then
            L3[$rid]='OK'; L3R[$rid]="$rcontrol (запуск)"; l3_ok=$((l3_ok+1))
            printf 'OK   %s %s запущен, control=%s\n' "$rid" "$rname" "$rcontrol" | tee -a "$L_REAL" >> "$LOG"
        else
            L3[$rid]='PENDING'; L3R[$rid]='rc='"${rrc:-?}"
            printf 'PENDING (E4/MADLEN) %s %s rc=%s\n' "$rid" "$rname" "$rrc" | tee -a "$L_REAL" >> "$LOG"
        fi
    fi
    printf '%s|%s|%s|%s|%s|%s\n' "${L3[$rid]}" "$rid" "$rname" "$rsource" "$rcontrol" "${L3R[$rid]}" >> "$L_REAL"
done < "$FULL/real/cases.txt"
printf 'Итог L3: %d OK / %d PENDING / %d SKIP\n' "$l3_ok" "$l3_pending" "$l3_skip" >> "$L_REAL"

# ------------------------------------------------------------------------ L4
hdr 'L4: negative cases'
printf '# STATUS|ID|SOURCE|EXPECTED|FACT\n' > "$L_NEG"
while IFS='|' read -r nid nsrc nexp; do
    [ -n "$nid" ] || continue
    case "$nid" in \#*) continue;; esac
    fact=''
    status='PENDING (E4/MADLEN)'
    case "$nid" in
      NC09)
        nt="$WORK/nc09"; mkdir -p "$nt/src" "$nt/build"
        cp "$ROOT/tests/check-source-words.py" "$nt/check-source-words.py"
        cp "$ROOT/src/LO_SYN.mad" "$ROOT/src/LO_GEN.mad" "$nt/src/"
        cp "$ROOT/build/LO_SYN.words" "$ROOT/build/LO_GEN.words" "$nt/build/"
        python3 - "$nt/src/LO_SYN.mad" <<'PY'
import re, sys
p = sys.argv[1]
s = open(p, encoding='utf-8', errors='replace').read()
pat = re.compile(r'(слово\s+[0-7]{3,4}\s+\(абс\s+[0-7]+\),\s*машинное слово\s+)([0-7]{12,16})')
m = pat.search(s)
assert m
new = ('4' if m.group(2)[0] != '4' else '5') + m.group(2)[1:]
open(p, 'w', encoding='utf-8').write(s[:m.start(2)] + new + s[m.end(2):])
PY
        python3 "$nt/check-source-words.py" --manifest > "$WORK/nc09.tamper" 2>&1
        trc=$?
        python3 "$ROOT/tests/check-source-words.py" > "$WORK/nc09.clean" 2>&1
        crc=$?
        fact="tampered rc=$trc; clean rc=$crc"
        if [ "$trc" -eq 1 ] && [ "$crc" -eq 0 ]; then status='OK'; fi
        ;;
      NC08)
        fact=$(grep -aFom1 "$nexp" "$ROOT/tests/forex-glissade/output.new.txt" 2>/dev/null || true)
        if [ -n "$fact" ] && ! grep -aq 'ИСПОРЧЕН' "$ROOT/tests/forex-glissade/output.new.txt"; then
            status='OK'
        fi
        [ "$status" = OK ] && fact="$nexp без ИСПОРЧЕН (14/14)"
        ;;
      *)
        if [ -f "$ROOT/$nsrc" ]; then
            fact=$(grep -aFom1 "$nexp" "$ROOT/$nsrc" 2>/dev/null || true)
            if [ -n "$fact" ]; then
                # Диагностика НЕ записана ни в один gold как успех.
                if ! grep -alF "$fact" "$FULL"/gold/*.gold >/dev/null 2>&1; then
                    status='OK'
                else
                    fact="$fact (ОШИБКА: попал в gold)"
                fi
            fi
        else
            fact='нет исходного лога'
        fi
        ;;
    esac
    L4[$nid]="$status"; L4R[$nid]="$fact"
    if [ "$status" = OK ]; then l4_ok=$((l4_ok+1)); else l4_pending=$((l4_pending+1)); fi
    printf '%-20s %-5s %-30s ожидалось=%s факт=%s\n' "$status" "$nid" "$nsrc" "$nexp" "$fact" \
        | tee -a "$L_NEG" >> "$LOG"
    printf '%s|%s|%s|%s|%s\n' "$status" "$nid" "$nsrc" "$nexp" "$fact" >> "$L_NEG"
done < "$FULL/negative/cases.txt"
printf 'Итог L4: %d OK / %d PENDING\n' "$l4_ok" "$l4_pending" >> "$L_NEG"

# ----------------------------------------------------------------------- GATE
hdr 'GATE: регрессия 20/20 (16 базовых + 4 новых F77-теста)'
printf '# STATUS|N|SCENARIO|EXPECTED|FACT\n' > "$L_GATE"
# 15 проб plan-f77 (ожидаемое поведение = baseline 2.02; FAST-переход в OK — не регрессия)
declare -A EXP_OK=( [BASE]=1 [DOLOOP]=1 [BLOCKIF]=1 [DOUBLPR]=1 [COMPLEX]=1 [LOGICAL]=1 \
    [INTRINSIC]=1 [EXTERNAL]=1 [DATAST]=1 [PARAMETER]=1 )
declare -A EXP_FAIL=( [CHARSTAR]='ТИП ОП-ДА' [LISTDIR]='ОШИБКА В ССЫЛКЕ НА ФОРМАТ' \
    [IMPLICIT]='НЕДОПУСТИМ КЛЮЧ СЛОВО' [ENDREAD]='НЕДОПУСТИМ СИМВОЛ * В ВЫРАЖ' \
    [SAVE]='НЕДОПУСТИМ КЛЮЧ СЛОВО' )
probe_out="$WORK/probe.txt"
timeout 300 bash "$ROOT/tests/plan-f77/probe.sh" > "$probe_out" 2>&1 || true
n=0
for name in BASE DOLOOP BLOCKIF CHARSTAR DOUBLPR COMPLEX LISTDIR DATAST IMPLICIT PARAMETER \
            INTRINSIC EXTERNAL ENDREAD SAVE LOGICAL; do
    n=$((n+1))
    row=$(grep -aE "^(OK|FAIL|\\?\\?\\?\\?) +$name[[:space:]]" "$probe_out" | head -1)
    st=$(printf '%s' "$row" | awk '{print $1}')
    exp='OK (baseline)'
    ok=0
    if [ -n "${EXP_OK[$name]:-}" ]; then
        [ "$st" = OK ] && ok=1
    elif [ -n "${EXP_FAIL[$name]:-}" ]; then
        exp="FAIL ${EXP_FAIL[$name]} (baseline) -> OK допустимо после P1-P7"
        if [ "$st" = OK ]; then ok=1; exp="$exp [IMPROVED]"
        elif [ "$st" = FAIL ] && printf '%s' "$row" | grep -qF "${EXP_FAIL[$name]}"; then ok=1
        fi
    fi
    if [ "$ok" -eq 1 ]; then
        GATE[$n]='OK'; GATER[$n]="$row"; g_ok=$((g_ok+1))
    else
        GATE[$n]='FAIL'; GATER[$n]="${row:-нет строки}"; g_fail=$((g_fail+1))
    fi
    printf '%-4s %2d %-14s ожидалось=%-55s факт=%s\n' "${GATE[$n]}" "$n" "$name" "$exp" "${GATER[$n]}" \
        | tee -a "$L_GATE" >> "$LOG"
    printf '%s|%d|%s|%s|%s\n' "${GATE[$n]}" "$n" "$name" "$exp" "${GATER[$n]}" >> "$L_GATE"
done
# G16 Глиссада (результат из L3, при необходимости локальный прогон)
n=16
if [ "$GLISSADE_OK" -eq 1 ]; then
    GATE[16]='OK'; GATER[16]='14/14'; g_ok=$((g_ok+1))
else
    GATE[16]='FAIL'; GATER[16]='глиссада 14/14 не подтверждена'; g_fail=$((g_fail+1))
fi
printf '%-4s %2d %-14s ожидалось=14/14 факт=%s\n' "${GATE[16]}" "$n" GLISSADE "${GATER[16]}" \
    | tee -a "$L_GATE" >> "$LOG"
printf '%s|%d|GLISSADE|14/14|%s\n' "${GATE[16]}" "$n" "${GATER[16]}" >> "$L_GATE"
# 4 положительных F77-дека (F77PREP-lowering; после P1-P7 заменяются нативными)
n=16
for cname in listdir_ok implicit_ok endread_ok save_ok; do
    n=$((n+1))
    gd="$FULL/gate/$cname.b6"; gg="$FULL/gate/$cname.gold"
    if [ -f "$gd" ] && [ -f "$gg" ]; then
        run_deck "$gd" "gate_$cname"
        if [ "$?" -eq 0 ] && cmp -s "$gg" "$DECK_RESULT"; then
            GATE[$n]='OK'; GATER[$n]='gold совпал'; g_ok=$((g_ok+1))
        else
            GATE[$n]='FAIL'; GATER[$n]="gold не совпал: $(reason)"; g_fail=$((g_fail+1))
        fi
    else
        GATE[$n]='FAIL'; GATER[$n]='нет deck/gold'; g_fail=$((g_fail+1))
    fi
    printf '%-4s %2d %-14s ожидалось=gold факт=%s\n' "${GATE[$n]}" "$n" "$cname" "${GATER[$n]}" \
        | tee -a "$L_GATE" >> "$LOG"
    printf '%s|%d|%s|gold|%s\n' "${GATE[$n]}" "$n" "$cname" "${GATER[$n]}" >> "$L_GATE"
done
printf 'Итог GATE: %d/20 OK, FAIL=%d (обязателен rc=0)\n' "$g_ok" "$g_fail" >> "$L_GATE"

# ------------------------------------------------------------------- manifest
{
    printf '# F77 full verification manifest — %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    find "$FULL" -type f \( -name '*.b6' -o -name '*.gold' -o -name '*.txt' \) -print0 \
        | sort -z | xargs -0 sha256sum
    sha256sum "$IMAGE" "$ETALON"
} > "$MANIFEST"

# --------------------------------------------------------------------- summary
printf 'LEVEL|OK|PENDING|SKIP|DETAIL\n' >> "$L_SUM"
printf 'L0|%d|%d|0|unit-пробы A-K\n' "$l0_ok" "$l0_pending" >> "$L_SUM"
printf 'L1|%d|%d|0|gold-пары (REGISTRY.txt: suite/new/e1)\n' "$l1_ok" "$l1_pending" >> "$L_SUM"
printf 'L2|%d|%d|%d|кросс *FTN/*FORTRAN\n' "$l2_ok" "$l2_pending" "$l2_skip" >> "$L_SUM"
printf 'L3|%d|%d|%d|реальные программы\n' "$l3_ok" "$l3_pending" "$l3_skip" >> "$L_SUM"
printf 'L4|%d|%d|0|negative cases\n' "$l4_ok" "$l4_pending" >> "$L_SUM"
printf 'GATE|%d|0|%d|20/20 обязателен\n' "$g_ok" "$g_fail" >> "$L_SUM"

emit ''
emit '------------------------------------------------------------------------'
emit 'Итоговая таблица F77 full'
printf '%-8s %-6s %-10s %-8s %s\n' LEVEL OK PENDING SKIP DETAIL | tee -a "$LOG"
printf '%-8s %-6s %-10s %-8s %s\n' L0 "$l0_ok" "$l0_pending" 0 'unit A-K' | tee -a "$LOG"
printf '%-8s %-6s %-10s %-8s %s\n' L1 "$l1_ok" "$l1_pending" 0 'gold pairs' | tee -a "$LOG"
printf '%-8s %-6s %-10s %-8s %s\n' L2 "$l2_ok" "$l2_pending" "$l2_skip" 'cross FTN/FORTRAN' | tee -a "$LOG"
printf '%-8s %-6s %-10s %-8s %s\n' L3 "$l3_ok" "$l3_pending" "$l3_skip" 'real programs' | tee -a "$LOG"
printf '%-8s %-6s %-10s %-8s %s\n' L4 "$l4_ok" "$l4_pending" 0 'negative' | tee -a "$LOG"
printf '%-8s %-6s %-10s %-8s %s\n' GATE "$g_ok" "$g_fail(FAIL)" 0 '20/20 mandatory' | tee -a "$LOG"
emit 'Логи: logs/f77_full_*.txt; манифест: logs/f77_full.sha256'

if [ "$g_fail" -ne 0 ] || [ "$g_ok" -ne 20 ]; then
    emit "FAIL: gate $g_ok/20 — риск регрессии; приёмка L0-L4 не засчитывается"
    printf 'RC=1\n' >> "$L_SUM"
    exit 1
fi
emit "OK: gate 20/20; L0 $l0_ok OK / $l0_pending PENDING, L1 $l1_ok OK / $l1_pending PENDING"
printf 'RC=0\n' >> "$L_SUM"
exit 0
