#!/bin/sh
# M4d FULL: our Fortran emitter O412B + live 4.12 overlays -> *TRANS invocation.
# Proves our module (named OURMRK*) is loaded by NEWCOMP* and our marker prints.
# NOTE: body zones N+2.. are still LIVE 4.12 overlay words; plan 59 replaces them.
set -e

ROOT=$(cd "$(dirname "$0")/../../.." && pwd)
EMITTER="$ROOT/src/newcomp/O412B.FTN"
DISPAK=${DISPAK_BIN:-/home/azizz/Yandex.Disk/dispak/build/dispak/dispak}
DISKDIR=/home/azizz/Yandex.Disk/dispak/build/dispak
REF2148=/usr/local/share/besm6/2148
REF2348=/usr/local/share/besm6/2348
LIVEBODY="$ROOT/reference/412/disk412_forex3_root.words"

for f in "$EMITTER" "$DISPAK" "$DISKDIR/2048" "$DISKDIR/2053" "$DISKDIR/2099" \
         "$REF2148" "$REF2348" "$LIVEBODY"; do
    [ -f "$f" ] || { echo "FAIL: missing $f"; exit 1; }
done

WORK=$(mktemp -d "${TMPDIR:-/var/tmp}/ourtrans.XXXXXX") || exit 1
if [ -z "${KEEP_WORK:-}" ]; then trap 'rm -rf "$WORK"' EXIT; fi
echo "work: $WORK"
cd "$WORK"

# 1. Compile O412B.FTN with SYSTEM FOREX 2.02 on a copy of disk 2348.
cp "$DISKDIR/2048" "$DISKDIR/2053" "$DISKDIR/2099" "$REF2148" "$REF2348" .
cp "$DISPAK" ./dispak && chmod +x ./dispak
{
  printf 'шифр 419999 зс5^\nлен 41(2048)^\nлен 60(2348-wr)^\nееВ1а3\n'
  printf '*name O412BLD\n*call yesmemory\n*perso:602300\n*no list\n*forex\n'
  cat "$EMITTER"
  printf '*to perso:602406\n*end file\n``````\nеконец\n'
} > build.deck
BESM6_PATH="$PWD" ./dispak -l build.deck > build.out 2>&1

cat > call.deck <<'EOF'
шифр 419999 зс5^
лен 41(2048)^
лен 60(2348)^
ееВ1а3
*name O412CAL
*call yesmemory
*perso:602300
*perso:602406,cont
*call o412b
*execute
*end file
``````
еконец
EOF
BESM6_PATH="$PWD" ./dispak -l call.deck > call.out 2>&1

# 2. Extract the 30 emitted words (O412D index hi lo) and build catalog+body.
cp "$LIVEBODY" live.words
python3 - "$PWD" <<'PY'
import re, sys
from pathlib import Path
W = Path(sys.argv[1]); N=0o1744
words=[]
for line in (W/'call.out').read_text(errors='replace').splitlines():
    m=re.match(r'\s*O412D\s+(\d+)\s+(\d+)\s+(\d+)\s*$',line)
    if m:
        i,hi,lo=map(int,m.groups()); words.append((hi<<24)|lo)
def wb(ws): return b''.join(w.to_bytes(6,'big') for w in ws)
(W/'cat.bin').write_bytes(wb(words[:16]+[0]*1008))
live=(W/'live.words').read_bytes()
lw=[int.from_bytes(live[i:i+6],'big') for i in range(0,len(live)-5,6)]
(W/'body.bin').write_bytes(wb(words[16:]+lw[14:1024]))
PY
# 3. Write to a clean copy of 2148 and fill N+2.. from live 1552..
mkdir -p disk41
cp "$REF2148" disk41/2148
cp "$DISKDIR/2048" "$DISKDIR/2053" "$DISKDIR/2099" disk41/ 2>/dev/null || true
export BESM6_PATH="$PWD/disk41"
besmtool write 2148 --from-file=cat.bin --start=01744 >/dev/null
besmtool write 2148 --from-file=body.bin --start=01745 >/dev/null
i=1
while [ "$i" -lt 40 ]; do
  z=$(printf '%o' $((01551+i)))
  t=$(printf '%o' $((01745+i)))
  besmtool dump 2148 --start="0$z" --length=1 --to-file=z.bin >/dev/null
  besmtool write 2148 --from-file=z.bin --start="0$t" >/dev/null
  i=$((i+1))
done

# 4. Run the deck.
cat > job.b6 <<'EOF'
шифр 419999 зс5^
DIS 41(2148)^
eeв1а3
*name M4DTEST
*TRANS:OURMRK*,,411744
      PROGRAM MAIN
      PRINT 100
  100 FORMAT('M4D-O412B-MARK')
      END
*execute
*end file
``````
ЕКОНЕЦ
EOF
./dispak -l job.b6 > job.out 2>&1
grep -q '4\.12' job.out
grep -q 'M4D-O412B-MARK' job.out
echo "OK: our module via *TRANS prints M4D-O412B-MARK (M4d FULL reproduced)"
