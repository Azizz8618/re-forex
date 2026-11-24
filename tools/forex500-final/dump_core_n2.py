#!/usr/bin/env python3
import sys
from pathlib import Path
core = Path(sys.argv[1]).read_bytes()
N2 = 0o21637
def w(k):
    return int.from_bytes(core[(N2+k)*6:(N2+k)*6+6], "big")
def tok(v):
    return (v>>42)&0x3f, (v>>36)&0x3f, (v>>24)&0xfff, v&0xffffff
print("N+2[1] name  = %016o" % w(1))
print("N+2[33] val  = %016o" % w(33))
print("N+2[100] lit = %016o" % w(100))
for i in range(64, 78):
    v = w(i); tk, sub, pos, pay = tok(v)
    print(f"N+2[{i}] tok TK={tk:2d} SUB={sub:2d} POS={pos:4d} PAY={pay:6d}  word={v:016o}")
