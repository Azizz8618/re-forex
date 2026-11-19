#!/usr/bin/env bash
# Install the reconstructed FOREX PERSO library into a FRESH working copy of
# disk 2348 (zone 0o2300 = decimal 1216) and verify its catalog.
#
# The etalon /usr/local/share/besm6/2348 is only READ; the image is written to
# an isolated working copy under work/ (or $TMPDIR).  besmtool zone arguments
# are DECIMAL, monitor cards are OCTAL; 0o2300 == 1216 decimal.
#
# Usage:
#   tests/install-forex-perso.sh [--keep] [--disk=/path/to/2348]
#
# Environment:
#   BESMTOOL          besmtool binary (default: besmtool on PATH)
#   ETALON            reference disk (default: /usr/local/share/besm6/2348)
#   SIPROD_LIB        path to siprod_lib.py (default: ~/Yandex.Disk/re-siprod/tools/siprod_lib.py)
set -euo pipefail

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
ROOT=$(CDPATH= cd -- "$(dirname "$SCRIPT_DIR")" && pwd) || exit 1

BESMTOOL=${BESMTOOL:-besmtool}
ETALON=${ETALON:-/usr/local/share/besm6/2348}
SIPROD_LIB=${SIPROD_LIB:-$HOME/Yandex.Disk/re-siprod/tools/siprod_lib.py}
IMAGE="$ROOT/build/FOREX_PERSO_2300.bin"

START_DEC=$((8#2300))       # 0o2300 -> 1216 (besmtool wants decimal)
NZONES=5
KEEP=0
WORK=

fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }
info() { printf '%s\n' "$*"; }

while [ $# -gt 0 ]; do
    case "$1" in
        --keep)        KEEP=1 ;;
        --disk=*)      WORK=${1#*=} ;;
        -h|--help)     sed -n '2,14p' "$0"; exit 0 ;;
        *)             fail "unknown option: $1" ;;
    esac
    shift
done

[ -x "$(command -v "$BESMTOOL")" ] || fail "besmtool not found: $BESMTOOL"
[ -f "$ETALON" ] || fail "etalon disk not found: $ETALON"

# 1. Build the image if necessary (regenerates .words from the tape if absent).
if [ ! -f "$IMAGE" ]; then
    info "image missing -> building $IMAGE"
    python3 "$ROOT/tools/build_forex_perso.py" || fail "build_forex_perso.py failed"
fi
[ -f "$IMAGE" ] || fail "no image at $IMAGE"
IMG_ZONES=$(python3 -c "import os,sys; print(os.path.getsize('$IMAGE')//(1024*6))")
[ "$IMG_ZONES" -eq "$NZONES" ] || fail "image is $IMG_ZONES zones, expected $NZONES"

# 2. Fresh working copy from the etalon.
if [ -z "$WORK" ]; then
    TMPROOT=${TMPDIR:-/tmp/.private/azizz/opencode}
    [ -d "$TMPROOT" ] || TMPROOT=/tmp
    WORKDIR=$(mktemp -d "$TMPROOT/install-forex-perso.XXXXXX") || fail "mktemp failed"
    WORK="$WORKDIR/2348"
    if [ "$KEEP" -eq 0 ]; then
        trap 'rm -rf "$WORKDIR"' EXIT
    fi
fi
WORKDIR_WORK=$(dirname "$WORK")
mkdir -p "$WORKDIR_WORK"
cp "$ETALON" "$WORK" || fail "cannot copy etalon to $WORK"
SHA_ETALON_BEFORE=$(sha256sum "$ETALON" | awk '{print $1}')
SHA_WORK_BEFORE=$(sha256sum "$WORK" | awk '{print $1}')
info "etalon sha256   : $SHA_ETALON_BEFORE"
info "work copy       : $WORK"

# 3. Write the image at zone 0o2300 (decimal 1216).
BESM6_PATH="$WORKDIR_WORK:/usr/local/share/besm6" \
    "$BESMTOOL" write 2348 --from-file="$IMAGE" --start="$START_DEC" \
    || fail "besmtool write failed"
SHA_ETALON_AFTER=$(sha256sum "$ETALON" | awk '{print $1}')
[ "$SHA_ETALON_BEFORE" = "$SHA_ETALON_AFTER" ] || fail "etalon changed!"
SHA_WORK_AFTER=$(sha256sum "$WORK" | awk '{print $1}')
[ "$SHA_WORK_BEFORE" != "$SHA_WORK_AFTER" ] || fail "work copy was not modified"
info "work sha256     : $SHA_WORK_AFTER"
info "etalon unchanged: OK"

# 4. Verify catalog with siprod_lib.Library (or an embedded fallback parser).
DUMP="$WORKDIR_WORK/forex_perso_dump.bin"
BESM6_PATH="$WORKDIR_WORK:/usr/local/share/besm6" \
    "$BESMTOOL" dump 2348 --start="$START_DEC" --length="$NZONES" --to-file="$DUMP" \
    || fail "besmtool dump failed"

python3 - "$DUMP" "$SIPROD_LIB" <<'PY' || fail "catalog verification failed"
import sys
from pathlib import Path

dump, siprod = Path(sys.argv[1]), Path(sys.argv[2])
EXPECTED = ["FOREX*", "LO*SYN", "LO*GEN", "FORMAT", "DATAPR*",
            "OCTTDEC", "GIV/PG", "TAK/PG", "FORTLIBR"]

if siprod.exists():
    sys.path.insert(0, str(siprod.parent))
    import siprod_lib as S
    lib = S.Library(dump)
    catalog = set(lib.catalog)
    objects = set(lib.objects)
    print(f"siprod_lib: {len(catalog)} names in catalog, {len(objects)} objects found")
else:
    # Embedded fallback: Dubna TEXT decoder + DMS 32-word-boundary scanner.
    TEXT = [" ", ".", "Б", "Ц", "Д", "Ф", "Г", "И", "(", ")", "*", "Й",
            "Л", "Я", "Ж", "/", "0", "1", "2", "3", "4", "5", "6", "7",
            "8", "9", "Ь", ",", "П", "-", "+", "Ы", "З", "A", "B", "C",
            "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
            "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "Ш",
            "Э", "Щ", "Ч", "Ю"]
    data = dump.read_bytes()
    w = [int.from_bytes(data[i:i+6], "big") for i in range(0, len(data), 6)]
    dec = lambda x: "".join(TEXT[(x >> (42 - 6*i)) & 0x3F] for i in range(8)).rstrip()
    catalog, objects = set(), set()
    i = 2
    while i + 1 < len(w):
        name = dec(w[i])
        if not name or not all(c.isalnum() or c in "/*" for c in name):
            break
        catalog.add(name)
        i += 2
    M15 = 0o77777  # 15 bits
    for s in range(2, len(w) - 3, 32):
        if (w[s] & 0xFFF) != 1:          # head length == 1
            continue
        cmd = w[s+2] & M15
        const = (w[s+2] >> 30) & M15
        data = (w[s+1] >> 15) & M15
        set_ = w[s+1] & M15
        toff = s + 3 + cmd + const + data + set_
        if toff >= len(w):
            continue
        name = dec(w[toff])
        if name in catalog:
            objects.add(name)
    print(f"fallback parser: {len(catalog)} names, {len(objects)} objects")

# TAK/PG is an ENTRY inside GIV/PG, so it is in the catalog but has no object.
EXPECTED_OBJ = [n for n in EXPECTED if n != "TAK/PG"]
missing_cat = [n for n in EXPECTED if n not in catalog]
missing_obj = [n for n in EXPECTED_OBJ if n not in objects]
print("catalog :", " ".join(sorted(catalog)))
print("objects :", " ".join(sorted(objects)))
if missing_cat:
    print("MISSING in catalog:", missing_cat)
    sys.exit(1)
if missing_obj:
    print("MISSING objects:", missing_obj)
    sys.exit(1)
print("PASS: all expected names in catalog, all modules have loadable objects"
      " (TAK/PG is an entry point of GIV/PG)")
PY

# 4b. Monitor-80 catalog check with PLCATALOG (reads the catalog directly from
#     disk; no *perso preload, which would collide with the system DATAPR*).
DISPAK=${DISPAK:-/usr/local/bin/dispak}
if [ -x "$DISPAK" ]; then
    cat > "$WORKDIR_WORK/catperso.b6" <<EOF
шифр 419999ЗС5^
ОЗУ 32^
дис 40(2348)^
eeв1а3
*name catperso
*libra:23
*        disc:41(2048)/system,lcross
*        file:libra,402300,r
*call plcatalog:402300
*end file
\`\`\`\`\`\`
еконец
EOF
    ( cd "$WORKDIR_WORK" && BESM6_PATH="$WORKDIR_WORK:/usr/local/share/besm6" \
        "$DISPAK" catperso.b6 > plcatalog.out 2> plcatalog.err ) \
        || fail "dispak plcatalog failed"
    if grep -q 'ИСПОРЧЕН' "$WORKDIR_WORK/plcatalog.out"; then
        cat "$WORKDIR_WORK/plcatalog.out" >&2
        fail "PLCATALOG reported corrupt subprograms"
    fi
    for n in 'FОRЕХ*' 'LО*SУN' 'LО*GЕN' 'FОRМАТ' 'DАТАРR*' \
             'ОСТТDЕС' 'GIV/РG' 'ТАК/РG'; do
        grep -Fq "$n" "$WORKDIR_WORK/plcatalog.out" \
            || fail "PLCATALOG did not list module $n"
    done
    info "PLCATALOG: 9 modules listed, no ИСПОРЧЕНЫ ПОДПРОГРАММЫ"
else
    info "dispak not found - Monitor-80 catalog check skipped"
fi

# 5. Verify only zones 0o2300..0o2303 changed (logical-zone dumps).
ETALON_DIR=$(dirname "$ETALON")
for z in $((START_DEC-1)) $START_DEC $((START_DEC+NZONES-1)) $((START_DEC+NZONES)); do
    BESM6_PATH="$ETALON_DIR" "$BESMTOOL" dump 2348 --start=$z --length=1 \
        --to-file="$WORKDIR_WORK/e_$z.bin" >/dev/null 2>&1 \
        || fail "cannot dump etalon zone $z"
    BESM6_PATH="$WORKDIR_WORK" "$BESMTOOL" dump 2348 --start=$z --length=1 \
        --to-file="$WORKDIR_WORK/w_$z.bin" >/dev/null 2>&1 \
        || fail "cannot dump work zone $z"
    oct=$(printf '%o' "$z")
    if [ "$z" -ge "$START_DEC" ] && [ "$z" -lt "$((START_DEC+NZONES))" ]; then
        cmp -s "$WORKDIR_WORK/e_$z.bin" "$WORKDIR_WORK/w_$z.bin" \
            && fail "written zone 0o$oct did not change"
        info "zone 0o$oct: changed (expected)"
    else
        cmp -s "$WORKDIR_WORK/e_$z.bin" "$WORKDIR_WORK/w_$z.bin" \
            || fail "zone 0o$oct outside library changed"
        info "zone 0o$oct: unchanged (expected)"
    fi
done

info "OK: FOREX PERSO library installed at zone 0o2300 and verified"
[ "$KEEP" -eq 1 ] && info "working copy kept at: $WORK"
exit 0
