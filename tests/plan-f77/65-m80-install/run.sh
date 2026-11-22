#!/bin/bash
# 65 — negative proof: installing our rebuilt GIVTRAN* into a catalog zone
# does NOT make *TRANS execute our code. COPIES ONLY, nothing is deleted.
set -uo pipefail
HERE=$(cd "$(dirname "$0")" && pwd)
SHARE=${BESM6_DISK_SHARE:-/usr/local/share/besm6}
DISPAK=${DISPAK_BIN:-/home/azizz/Yandex.Disk/dispak/build/dispak/dispak}
BESMTOOL=${BESMTOOL:-/home/azizz/Yandex.Disk/dispak/build/besmtool/besmtool}
ROOT=$(mktemp -d "${TMPDIR:-/tmp}/m80-install.XXXXXX")
export PATH="$(dirname "$DISPAK"):$(dirname "$BESMTOOL"):$PATH"

for f in "$DISPAK" "$BESMTOOL" "$SHARE/2048" "$SHARE/2053" "$SHARE/2099" "$SHARE/2148"; do
    [ -e "$f" ] || { echo "FAIL: missing $f"; exit 2; }
done
xxd -r -p "$HERE/ovl_our.hex" > "$ROOT/ovl_our.bin"
[ "$(stat -c %s "$ROOT/ovl_our.bin")" = 6144 ] || { echo "FAIL: bad overlay size"; exit 2; }

cat > "$ROOT/job.b6" <<'EOF'
шифр 419999 зс5^
DIS 41(2148)^
eeв1а3
*name M80MARK
*TRANS:FOREX3*,,411550
      PROGRAM MAIN
      PRINT 100
  100 FORMAT('SHOULD-NOT-COMPILE-7391')
      END
*execute
*end file
``````
ЕКОНЕЦ
EOF

printf '%-9s %-7s %-7s %-12s %s\n' VARIANT ZONE PREFIX MARKER 'KEY OUTPUT'
any_marker=0

run() {
    name=$1; zone=$2; words=$3
    d="$ROOT/$name"
    mkdir -p "$d/disks" "$d/home"
    cp "$SHARE"/{2048,2053,2099,2148} "$d/disks/"
    cp "$ROOT/job.b6" "$d/job.b6"
    if [ "$words" -gt 0 ]; then
        dd if=/dev/zero bs=192 count=$((words / 32)) of="$d/prefix.bin" status=none
        cat "$d/prefix.bin" "$ROOT/ovl_our.bin" > "$d/install.bin"
    else
        cp "$ROOT/ovl_our.bin" "$d/install.bin"
    fi
    if [ "$zone" != none ]; then
        ( cd "$d" && HOME="$d/home" BESM6_PATH="$d/disks" \
            "$BESMTOOL" write 2048 --start="$zone" --from-file=install.bin ) \
            > "$d/write.log" 2>&1
    fi
    ( cd "$d" && HOME="$d/home" BESM6_PATH="$d/disks" \
        timeout 120 "$DISPAK" -l job.b6 > out.txt 2>&1 ) || true
    m=no
    grep -q '21 1.00 3.00' "$d/out.txt" && { m=YES; any_marker=1; }
    keys=$(grep -oE '4\.12|FORTRAN|SHOULD-NOT-COMPILE-7391|КОНЕЦ ЗАДАЧИ|Interrupt|0070[23]' \
           "$d/out.txt" | sort -u | tr '\n' ',' | head -c 70)
    printf '%-9s %-7s %-7s %-12s %s\n' "$name" "$zone" "$words" "$m" "$keys"
}

mkdir -p "$ROOT/control/disks" "$ROOT/control/home"
cp "$SHARE"/{2048,2053,2099,2148} "$ROOT/control/disks/"
( cd "$ROOT/control" && HOME="$ROOT/control/home" BESM6_PATH="$ROOT/control/disks" \
    timeout 120 "$DISPAK" -l "$ROOT/job.b6" > out.txt 2>&1 ) || true
m=no
grep -q '21 1.00 3.00' "$ROOT/control/out.txt" && { m=YES; any_marker=1; }
keys=$(grep -oE '4\.12|FORTRAN|SHOULD-NOT-COMPILE-7391|КОНЕЦ ЗАДАЧИ|Interrupt|0070[23]' \
       "$ROOT/control/out.txt" | sort -u | tr '\n' ',' | head -c 70)
printf '%-9s %-7s %-7s %-12s %s\n' control none none "$m" "$keys"

run a0354 0354 512
run b0252 0252 384
run c0354 0354 544
run d0204 0204 0

if [ "$any_marker" = 0 ]; then
    echo "VERDICT: REPRODUCED (no catalog install makes *TRANS run our code)"
    exit 0
fi
echo "VERDICT: CHANGED (a marker appeared; re-investigate)"
exit 1
