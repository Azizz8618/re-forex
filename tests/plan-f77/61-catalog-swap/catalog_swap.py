#!/usr/bin/env python3
"""M3 EXP B reproduced: swap catalog name at 2148 zone 0o1550 word 2.

FOREX3* -> OURCOM*, then *TRANS:OURCOM*,,411550 loads the SAME live 4.12
compiler. Proves the catalog zone (not LINK table / TTABLE) controls which
compiler is selected by *TRANS. Never touches live disks: BESM6_PATH to a copy.
"""
import os, shutil, struct, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SHARE = Path(os.environ.get('BESM6_DISK_SHARE', '/usr/local/share/besm6'))
WORK = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/var/tmp/b1-f77-fix/tmp/catswap')
MASK = (1 << 48) - 1
TXT = " .БЦДФГИ()*ЙЛЯЖ/0123456789Ь,П-+ЫЗABCDEFGHIJKLMNOPQRSTUVWXYZШЭЩЧЮ"

def enc(s):
    w = 0
    for c in s.ljust(8)[:8]:
        w = (w << 6) | TXT.index(c)
    return w

if WORK.exists():
    shutil.rmtree(WORK)
WORK.mkdir(parents=True)
for d in ('2048', '2053', '2099', '2148'):
    shutil.copy(SHARE / d, WORK / d)
disk = WORK / '2148'
data = bytearray(disk.read_bytes())
off = (0o1550 + 4) * 8256 + 64 + 2 * 8
q = struct.unpack_from('<Q', data, off)[0]
assert (q & MASK) == enc('FOREX3*'), f'unexpected old word {q & MASK:o}'
struct.pack_into('<Q', data, off, (q & ~MASK) | enc('OURCOM*'))
disk.write_bytes(data)

(WORK / 'job.b6').write_text("""шифр 419999 зс5^
DIS 41(2148)^
eeв1а3
*name CATSWAP
*TRANS:OURCOM*,,411550
      PROGRAM MAIN
      PRINT 100
  100 FORMAT('CATALOG-SWAP-7391')
      END
*execute
*end file
``````
ЕКОНЕЦ
""")
disp = Path(os.environ.get('DISPAK_BIN', '/home/azizz/Yandex.Disk/dispak/build/dispak/dispak'))
if not disp.exists():
    print('FAIL: dispak binary not found:', disp)
    sys.exit(2)
r = subprocess.run([str(disp), '-l', 'job.b6'], cwd=WORK,
                   env=dict(os.environ, BESM6_PATH=str(WORK)),
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60)
out = r.stdout.decode('utf-8', 'replace')
(WORK / 'out.txt').write_text(out)
ok = '4.12' in out and 'CATALOG-SWAP-7391' in out and 'ОТСУТСТВУЕТ' not in out
print('rc', r.returncode, 'PASS' if ok else 'FAIL')
for line in out.splitlines():
    if any(k in line for k in ('4.12', 'CATALOG-SWAP', 'ОТСУТСТВУЕТ', 'КОНЕЦ')):
        print(' |' + line)
sys.exit(0 if ok else 1)
