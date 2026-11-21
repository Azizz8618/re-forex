#!/usr/bin/env bash
# FINAL proof: OUR Fortran-77 compiler (D1 codegen) invoked through *TRANS
# with a PATCHED MONITOR, computing BASE77 (21 / 15) via OUR *64 descriptor.
#
# The monitor patch is `cu.c.patched`: in addition to C3's VJM redirect, it
# loads 400 words (not 11) from disk 2148 zone 0o1745 into RAM 0o1770 before
# the jump. This models a boot image that puts OUR body into executable RAM.
# Only local COPIES of disks are used; live /usr/local/share/besm6 untouched.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SHARE="${BESM6_DISK_SHARE:-/usr/local/share/besm6}"
WORK="$(mktemp -d "${TMPDIR:-/var/tmp}/monbase77.XXXXXX")"
trap 'python3 -c "import shutil,sys;shutil.rmtree(sys.argv[1],ignore_errors=True)" "$WORK"' EXIT
KEEP="${KEEP_WORK:-0}"; [ "$KEEP" = 1 ] && trap - EXIT
echo "WORK=$WORK"

# 1. Build patched dispak from the C3 source tree (use repo's 59-c3 src as base,
#    overlay our 400-word cu.c), or reuse a prebuilt binary if provided.
SRC="${DISPAK_SRC:-$HERE/../59-c3/src}"
BIN="${DISPAK_C3_BIN:-}"
if [ -z "$BIN" ]; then
    cp -r "$SRC" "$WORK/src"
    cp "$HERE/cu.c.patched" "$WORK/src/dispak/cu.c"
    cmake -S "$WORK/src" -B "$WORK/build" -DCMAKE_BUILD_TYPE=Release >/dev/null 2>&1
    cmake --build "$WORK/build" --target dispak -j4 >/dev/null 2>&1
    BIN="$WORK/build/dispak/dispak"
fi
echo "BIN=$BIN"

# 2. Prepare disks copy and our body (catalog 0o1744, body 0o1745 with our code at word 9).
mkdir -p "$WORK/disks"
for d in 2048 2053 2099 2148; do cp "$SHARE/$d" "$WORK/disks/"; done
export BESM6_PATH="$WORK/disks"

python3 - "$HERE" "$WORK" <<'PY'
import sys, subprocess
from pathlib import Path
HERE, WORK = Path(sys.argv[1]), Path(sys.argv[2])
TXT = " .БЦДФГИ()*ЙЛЯЖ/0123456789Ь,П-+ЫЗABCDEFGHIJKLMNOPQRSTUVWXYZШЭЩЧ Ю"
def enc(s):
    v=0
    for c in s.ljust(8)[:8]: v=(v<<6)|TXT.index(c)
    return v
cat=[0]*1024; cat[0]=0o5557565164576212; cat[1]=0o370
cat[2]=enc('OURMRK*'); cat[3]=0o0400402757101760
(WORK/'cat.bin').write_bytes(b''.join(w.to_bytes(6,'big') for w in cat))
code=[int(x,8) for x in (HERE/'code_base77.txt').read_text().split()]
assert len(code)==400, len(code)
body=[0]*1024; body[0]=0o1600043
for j,w in enumerate(code): body[9+j]=w & ((1<<48)-1)
(WORK/'body.bin').write_bytes(b''.join(w.to_bytes(6,'big') for w in body))
for z,f in ((0o1744,'cat.bin'),(0o1745,'body.bin')):
    subprocess.run(['besmtool','write','2148',f'--from-file={WORK/f}',f'--start=0{z:o}'],
                   check=True, capture_output=True)
PY

cat > "$WORK/job.b6" <<'EOF'
шифр 419999 зс5^
DIS 41(2148)^
eeв1а3
*name MONBASE
*TRANS:OURMRK*,,411744
      PROGRAM MAIN
      PRINT 100
  100 FORMAT('IGNORED-BY-RESIDENT')
      END
*execute
*end file
``````
ЕКОНЕЦ
EOF
cd "$WORK"
"$BIN" -l job.b6 > out.txt 2>&1
if grep -q '21 1.00 3.00' out.txt && ! grep -q '4.12' out.txt; then
    echo "PASS: our compiler computed BASE77 (21), no 4.12 banner"
else
    echo "FAIL"; tail -20 out.txt; exit 1
fi
# A/B: bound 5 -> 15
python3 - "$HERE" "$WORK" <<'PY'
import sys, subprocess
from pathlib import Path
HERE, WORK = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(HERE))
from gen_d1 import compile_base77
code,_,_=compile_base77(5)
body=[0]*1024; body[0]=0o1600043
for j,w in enumerate(code): body[9+j]=w&((1<<48)-1)
(WORK/'body.bin').write_bytes(b''.join(w.to_bytes(6,'big') for w in body))
subprocess.run(['besmtool','write','2148',f'--from-file={WORK}/body.bin','--start=01745'],check=True,capture_output=True)
PY
"$BIN" -l job.b6 > out5.txt 2>&1
if grep -q '15 1.00 3.00' out5.txt; then
    echo "PASS A/B: bound 5 -> 15"
else
    echo "FAIL A/B"; tail -20 out5.txt; exit 1
fi
echo "RESULT: PASS (our compiler via *TRANS with patched monitor)"
