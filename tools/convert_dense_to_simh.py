#!/usr/bin/env python3
"""Convert a dense 6-byte-word BESM-6 tape image into a SIMH 8-byte tagged disk image.

Source facts:
  - TapeImage.cs:9-11,43,53  -- dense layout, 1024 words/page, 6 bytes/word big-endian
  - besm6_defs.h:49-57      -- one zone = 8 system words + 1024 data words,
                               each stored as an 8-byte little-endian t_value:
                               bits 0..47 = word, bits 48..49 = tag
                               (PARITY_INSN=1, PARITY_NUMBER=2)
  - dubna/besm6_arch.h:50,55 -- DISK_ZONE_NWORDS=1032, DISK_ZONE_OFFSET=4
  - DUBNA/BUILD/data/mons9.d9 -- reference conversion of monsys.9,
                               288 zones, headers at zone start,
                               every data word tagged 1 (PARITY_INSN).
"""
import argparse
import struct
from pathlib import Path

ZONE_WORDS = 8 + 1024
N_ZONES = 1000
DISK_ZONE_OFFSET = 4
TAG_INSN = 1
TAG_NUMBER = 2


def read_dense_zones(path: Path):
    data = path.read_bytes()
    if len(data) % 6:
        raise ValueError(f"{path}: size {len(data)} is not a multiple of 6")
    words = [int.from_bytes(data[i:i + 6], "big") for i in range(0, len(data), 6)]
    if len(words) % 1024:
        raise ValueError(f"{path}: {len(words)} words is not a multiple of 1024")
    return [words[i:i + 1024] for i in range(0, len(words), 1024)]


def tagged(word: int, tag: int) -> bytes:
    return struct.pack("<Q", (tag << 48) | (word & ((1 << 48) - 1)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dense", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--headers", type=Path, default=None,
                    help="optional reference tagged image (mons9.d9) to copy 8 system words from")
    ap.add_argument("--header-tag", type=int, default=TAG_NUMBER)
    ap.add_argument("--data-tag", type=int, default=TAG_INSN)
    args = ap.parse_args()

    zones = read_dense_zones(args.dense)
    if len(zones) + DISK_ZONE_OFFSET > N_ZONES:
        raise ValueError(f"too many zones: {len(zones)} + {DISK_ZONE_OFFSET} > {N_ZONES}")

    ref = args.headers.read_bytes() if args.headers else None
    if ref and len(ref) < ZONE_WORDS * 8:
        raise ValueError("reference header image too short")

    out = bytearray(N_ZONES * ZONE_WORDS * 8)
    for zi, words in enumerate(zones):
        pz = zi + DISK_ZONE_OFFSET
        base = pz * ZONE_WORDS * 8
        if ref:
            # Copy 8 system words verbatim from the reference image.
            out[base:base + 8 * 8] = ref[zi * ZONE_WORDS * 8:zi * ZONE_WORDS * 8 + 8 * 8]
        else:
            # Synthesize a minimal SIMH-like header: zone number, magic, checksums.
            val = 2 * pz
            out[base:base + 8] = tagged(val << 36, args.header_tag)
            out[base + 8:base + 16] = tagged((0o1370707 << 24) | (2209 << 12), args.header_tag)
            out[base + 16:base + 24] = tagged(0, args.header_tag)
            out[base + 24:base + 32] = tagged(0, args.header_tag)
        dw = base + 8 * 8
        for wi, word in enumerate(words):
            out[dw + wi * 8:dw + wi * 8 + 8] = tagged(word, args.data_tag)

    args.out.write_bytes(out)
    print(f"wrote {args.out}: {len(out)} bytes, {N_ZONES} zones, "
          f"{len(zones)} tape zones at physical zones {DISK_ZONE_OFFSET}.."
          f"{DISK_ZONE_OFFSET + len(zones) - 1}")


if __name__ == "__main__":
    main()
