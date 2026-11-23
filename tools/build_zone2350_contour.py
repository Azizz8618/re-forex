#!/usr/bin/env python3
"""Build a SIMH-format disk 2048 copy with OUR contour at zone 0o2350.

Copied verbatim from the proven stage builder
`/tmp/.private/azizz/opencode/re-forex-413-io/work/build_contour_simh.py`
(the only change is an explicit output directory instead of a hard-coded
workspace path). Reuses the proven test-70/84 generators read-only. SIMH zone
header/checksum recipe from docs/74-simh-verification.md section 3.

Usage: build_zone2350_contour.py <case> [--out DIR] [zero_word_indices...]
"""
import argparse
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
T84 = REPO / "tests/plan-f77/84-wide-output"
sys.path.insert(0, str(T84))
import installer as inst  # noqa: E402

N = 0o2350
ZONE = 8256
DATA0 = 64
MASK = (1 << 48) - 1


def words_hex(path):
    raw = bytes.fromhex(Path(path).read_text().strip())
    return [int.from_bytes(raw[i:i + 6], "big") for i in range(0, len(raw) - 5, 6)]


def checksum(words):
    s = 0
    for w in words:
        s += w
        while s >> 48:
            s = (s & MASK) + (s >> 48)
    return s & MASK


def write_zone(buf, logical, words, w1=0x000005f1c7800000,
               w2=0x0000410300000000):
    assert len(words) == 1024
    phys = logical + 4
    base = phys * ZONE
    for i, w in enumerate(words):
        off = base + DATA0 + 8 * i
        buf[off:off + 6] = w.to_bytes(6, "little")
        buf[off + 6:off + 8] = b"\x00\x00"
    ck = checksum(words)
    hdr = [((phys << 36) | 0x038ca3c918), w1, w2, ck]
    for k in range(8):
        val = hdr[k % 4]
        if k >= 4:
            val = ((val & ~(0xfff << 36)) | (((phys + 1) << 36) & (0xfff << 36))) if k in (4, 6) else val
        buf[base + 8 * k:base + 8 * k + 6] = val.to_bytes(6, "little")
        buf[base + 8 * k + 6:base + 8 * k + 8] = b"\x00\x00"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("case")
    ap.add_argument("--out", default=None, help="output directory (default: $TMPDIR/zone2350)")
    ap.add_argument("zero", nargs="*", help="body word indices to zero (octal or 0x)")
    a = ap.parse_args()

    import os
    out = Path(a.out) if a.out else Path(os.environ.get("TMPDIR", "/tmp")) / "zone2350"
    out.mkdir(parents=True, exist_ok=True)
    zero = tuple(int(x, 0) for x in a.zero)

    o412 = inst.parse_o412c()
    tail = words_hex(REPO / "tests/plan-f77/69-full-emitted-body/o412d_words.hex")
    obj = words_hex(REPO / "tests/plan-f77/65-m80-install/ovl_our.hex")
    images, ov = inst.build_images(o412, tail, obj, 6, zero=zero)
    dst = out / f"2048_{a.case}"
    shutil.copy2("/usr/local/share/besm6/2048", dst)
    buf = bytearray(dst.read_bytes())
    write_zone(buf, N, images["cat"])
    write_zone(buf, N + 1, images["body"])
    write_zone(buf, N + 2, images["z2"])
    write_zone(buf, N + 3, images["zero"])
    dst.write_bytes(buf)
    print(f"case={a.case} zero={zero} dst={dst} sha={inst.sha(dst)[:16]}")
    for k, v in sorted(ov.items()):
        print(f"  override body[{k:o}] RAM {0o1757 + k:04o} = {v & MASK:016o}")


if __name__ == "__main__":
    main()
