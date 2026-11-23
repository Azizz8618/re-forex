#!/usr/bin/env python3
"""Rename the contour's catalog entry OURMRK* -> FRX5*.

Copies an existing zone-2350 contour image and rewrites catalog zone N word 2,
recomputing the SIMH zone header/checksum with the proven wz() helper. The rest
of the image (body, overlay, N+3 routine) is left byte-identical.

Usage:
  python3 rename_catalog.py <src_image> <dst_image>
"""
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_e2e import rz, wz, N  # noqa: E402

# FRX5* left-aligned in 6-bit TEXT (docs/14 alphabet): codes 38,50,56,21,10,0,0,0
NAME_WORD = 0o4662702512000000
OLD_WORD = 0o5765625562531200  # OURMRK*

MASK = (1 << 48) - 1


def main():
    if len(sys.argv) != 3:
        raise SystemExit("usage: rename_catalog.py <src> <dst>")
    src, dst = map(Path, sys.argv[1:])
    data = src.read_bytes()
    img = bytearray(data)
    dst.write_bytes(img)
    cat = rz(str(dst), N)
    if cat[2] & MASK != OLD_WORD:
        raise SystemExit(f"unexpected catalog word 2: {cat[2]:o}")
    cat[2] = NAME_WORD
    wz(str(dst), N, cat)
    print(f"{dst} sha={hashlib.sha256(dst.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    main()
