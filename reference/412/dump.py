#!/usr/bin/env python3
"""Dump dense 6-byte BESM-6 words from a monsys.9 copy in a file-word address range."""
import sys
from pathlib import Path

d = Path(sys.argv[1]).read_bytes()
W = [int.from_bytes(d[i:i+6], 'big') for i in range(0, len(d), 6)]
a = int(sys.argv[2], 0)
b = int(sys.argv[3], 0)
for i in range(a, b):
    w = W[i]
    print(f"{i:06o} {w:016o}  zone={i//1024:03o}.{i%1024:04o}  dec={w}")
