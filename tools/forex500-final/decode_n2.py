#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_e2e import rz, N, Z3
img = sys.argv[1]
lo = int(sys.argv[2], 0) if len(sys.argv) > 2 else 250
hi = int(sys.argv[3], 0) if len(sys.argv) > 3 else 300
z = rz(img, N + 2)
NAMES = {0:'atx',4:'a+x',6:'a-x',0o10:'xta',0o11:'aax',0o12:'aex',0o13:'arx',
         0o14:'avx',0o16:'a/x',0o17:'a*x',0o24:'e+x',0o26:'asx',0o30:'utc',
         0o36:'asn',0o40:'ati',0o42:'ita',0o64:'*64',0o220:'utc',0o260:'uza',
         0o270:'u1a',0o300:'uj',0o310:'vjm'}
for k in range(lo, hi):
    w = z[k]
    for half, sh in (('L',24), ('R',0)):
        h = (w >> sh) & 0xffffff
        reg = h >> 20
        op = (h >> 12) & 0o77
        adr = h & 0o7777
        lnk = (h >> 15) & 0o177
        print(f'N2[{k:04d}] {half} {h:06o} reg={reg:o} op={op:03o}({NAMES.get(op,"?")}) adr={adr:04o} lnk={lnk:o}')
