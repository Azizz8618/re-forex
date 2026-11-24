#!/usr/bin/env python3
"""One-machine-word patch of OUR lexer constant table (N+2 offset 272 = L_PD0).

PD0 0xd0 -> 0xcf makes the on-machine ASCII->digit extraction return d-1,
changing the Fortran-derived literal without touching the deck or the image's
rest. Restoring the word gives byte-identical image A again.
"""
import hashlib, shutil, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_e2e import rz, wz, N
WS = HERE.parent
src = WS / "images/2048_B1B3_A"
dst = WS / ("images/" + sys.argv[1])
shutil.copy2(src, dst)
z2 = rz(str(dst), N + 2)
off = int(sys.argv[2], 0)
val = int(sys.argv[3], 0)
old = z2[off]
z2[off] = val
wz(str(dst), N + 2, z2)
print(f"{dst.name} N2[{off}]: {old:016o} -> {val:016o} "
      f"sha={hashlib.sha256(dst.read_bytes()).hexdigest()}")
