#!/usr/bin/env python3
"""Decode RLE-packed 8-bit ASCII card buffer at RAM 0o64000+ from a C-oracle CORE dump."""
import sys
from pathlib import Path

core = Path(sys.argv[1]).read_bytes()
assert len(core) == 65536 * 6, len(core)

def word(addr):
    return int.from_bytes(core[addr*6:addr*6+6], "big")

def bytes_of(addr):
    w = word(addr)
    return [(w >> (8*(5-k))) & 0xff for k in range(6)]

start = int(sys.argv[2], 0) if len(sys.argv) > 2 else 0o64000
count = int(sys.argv[3], 0) if len(sys.argv) > 3 else 0o40

for a in range(start, start + count):
    bs = bytes_of(a)
    txt = []
    for b in bs:
        if b == 0x0a:
            txt.append("\\n")
        elif 0x80 <= b <= 0xff:
            txt.append(f"<{b-0x80}sp>")
        elif b == 0:
            txt.append("<NUL>")
        elif 32 <= b < 127:
            txt.append(chr(b))
        else:
            txt.append(f"<{b:02x}>")
    print(f"{a:06o}  {' '.join(f'{b:02x}' for b in bs)}  {''.join(txt)}")
