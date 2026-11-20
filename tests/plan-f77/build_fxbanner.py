#!/usr/bin/env python3
"""Build a minimal PERSO image with only FXBANNER as the head module (M0 proof).

Usage: python3 tests/plan-f77/build_fxbanner.py [output.bin]

The image is written to a COPY of disk 2348 at zone 0o2400 (decimal 1280),
leaving the main FOREX PERSO image at 0o2300 untouched.  The deck is
tests/plan-f77/fxbanner.b6.
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "bfp", ROOT / "tools" / "build_forex_perso.py")
bfp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bfp)

src = ROOT / "src" / "FXBANNER.mad"
out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(
    "/var/tmp/b1-f77-fix/m0-retry/final/M0_PERSO_2400.bin")
out.parent.mkdir(parents=True, exist_ok=True)

body, load, entry = bfp.assemble_source("FXBANNER", src, 1, 10**9)
start = 2 * bfp.ZONE_WORDS          # body at word 2048 -> catalog zone 2
f3 = bfp.TV_BIAS_F3 & 0xFFF
f2 = (bfp.TV_BIAS_F2 + 2 * 0o100 + (load // 512)) & 0xFFF
f1 = ((load % 512) * 8) & 0xFFF
f0 = entry & 0xFFF
record = (f3 << 36) | (f2 << 24) | (f1 << 12) | f0

catalog = [bfp.HEADER_WORD, 0, bfp.text_encode("FXBANNER"), record,
           0, (1 << 48) - 1]
words = [0] * start
words[:len(catalog)] = catalog
words.extend([0] * (start + len(body) - len(words)))
for i, w in enumerate(body):
    words[start + i] = w
total = ((start + len(body) + bfp.ZONE_WORDS - 1) // bfp.ZONE_WORDS) * bfp.ZONE_WORDS
words.extend([0] * (total - len(words)))
out.write_bytes(b"".join(w.to_bytes(6, "big") for w in words))

print(f"image   : {out}")
print(f"zones   : {total // bfp.ZONE_WORDS}")
print(f"FXBANNER: load={load} entry=0o{entry:o} body={len(body)}")
print(f"catalog : f2=0o{f2:o} f3=0o{f3:o} f1=0o{f1:o} f0=0o{f0:o}")
