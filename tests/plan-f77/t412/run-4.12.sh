#!/bin/sh
# Live FOREX 4.12 in the C dispak simulator (6-byte words).
# Proves a compiler other than system 2.02 is reachable in our environment:
#   *TRANS:FOREX3*,,411550 -> NEWCOMP* -> body at disk 41 zone 0o1550.
# Disk 2148 MUST be /usr/local/share/besm6/2148 (SHA 75617c04...), not the
# SIMH MD/2148 image: the latter stores the body at zone 0o1240 and yields
# "ОТСУТСТВУЕТ FOREX3*" for address 411550.
set -e

ROOT=$(cd "$(dirname "$0")/../../.." && pwd)
DISPAK=${DISPAK_BIN:-/home/azizz/Yandex.Disk/dispak/build/dispak/dispak}
DISKDIR=/home/azizz/Yandex.Disk/dispak/build/dispak
REF2148=/usr/local/share/besm6/2148

for f in "$DISPAK" "$DISKDIR/2048" "$DISKDIR/2053" "$DISKDIR/2099" "$REF2148"; do
    [ -f "$f" ] || { echo "FAIL: missing $f"; exit 1; }
done

WORK=$(mktemp -d "${TMPDIR:-/var/tmp}/t412.XXXXXX") || exit 1
trap 'rm -rf "$WORK"' EXIT
mkdir -p "$WORK/disks"
cp "$DISKDIR/2048" "$DISKDIR/2053" "$DISKDIR/2099" "$REF2148" "$WORK/disks/"
cp "$DISPAK" "$WORK/dispak"
chmod +x "$WORK/dispak"
cp "$(dirname "$0")/t412.b6" "$WORK/t412.b6"

cd "$WORK"
BESM6_PATH="$WORK/disks" ./dispak -l t412.b6 > t412.out 2>&1
grep -q '4\.12' t412.out || { echo "FAIL: no 4.12 banner"; tail -30 t412.out; exit 1; }
grep -q 'HELLO 412' t412.out || { echo "FAIL: no HELLO 412"; tail -30 t412.out; exit 1; }
echo "OK: FOREX 4.12 banner and HELLO 412 present"
