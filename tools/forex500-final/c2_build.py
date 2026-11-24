#!/usr/bin/env python3
"""C2: minimal VARIABLE-token support for the contour (copies only).

Reuses the canonical docs/105 chain verbatim (final_sign.S: converter, sign
block, both reclaims, shared floor_int VJM). The only new machine code is a
9-halfword IR variable reader that turns the `TA=VIDX` digit of a
`777005 ... 2 ...` record into an indexed read from a 6-bit TEXT symbol table
in zone N+2.

Symbol table (zone N+2 = disk logical 0o2352, RAM 0o21637+k; offsets 0..525
are all-zero and free, 526..900 = required overlay table, docs/63):

    offset VIDX       : 6-bit TEXT name word, e.g. 'Y       '
    offset 32 + VIDX  : value word (BESM float, literal scaled x100)

No host-computed digit is stored in the image.
"""
import argparse, hashlib, shutil, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import final_sign as FS
from build_e2e import rz, wz, word, f32, MASK, N, Z3, MAX_WORDS, long_

WS = HERE.parent
F = FS.F
UTC6 = F.UTC6
N2 = N + 2                       # 0o2352
N2_RAM0 = 0o21637                # FACT: measured by C-oracle CORE sentinel scan
N2_NAME = 0                      # name words at offsets VIDX (1..30)
N2_VAL = 32                      # value words at offsets 32+VIDX
N2_VAL_RAM = N2_RAM0 + N2_VAL     # 0o21677
SR24 = (64 + 24) << 41

# T[7] is unused by the variable path (the LIT 10*T[] assembly was removed),
# so the right-shift-24 control word reuses that proven-free low-RAM cell.
FS.LO["SR24"] = FS.LO["T7"]


def utc(adr):
    return long_(0o220, adr)


def text_word(s):
    """8 six-bit TEXT codes (ASCII-0x20), MSB first, padded with spaces."""
    s = (s + " " * 8)[:8]
    codes = [ord(c) - 0x20 for c in s]
    assert all(0 <= c < 64 for c in codes)
    v = 0
    for c in codes:
        v = (v << 6) | c
    return v & MASK


class VStream(FS.S):
    def deck_read(self, two=True):
        # Card `777005 <seq> 2 0 <VIDX> 0`; C-oracle CORE at entry shows the
        # TA digit at byte 2 (shift 24) of RAM 0o64014 (RLE card buffer):
        #   064014  30 87 32 87 30 a3   = '0' <7sp> '2' <7sp> '0' <35sp>
        self.E(UTC6)
        self.L(0o10, 0o4014, 0)         # ACC = card word 0o64014
        self.Z(F.ASX, "SR24")           # shift ASCII '2' into low byte
        self.Z(F.AAX, "M8")             # isolate ASCII 0o62
        self.Z(F.ARX, "NEG31")          # end-around carry: 0o62-0o31 -> 2
        self.L(F.ATI, 6)                # M[6] = VIDX
        self.E(utc(N2_VAL_RAM))         # arm address modifier 0o21677
        self.L(0o10, 0, 6)              # ACC = M[0o21677 + VIDX] = value float

    def intrinsic(self, kind):
        # value word holds the literal scaled x100 (1234.0 for Y=12.34).
        # Same one-instruction /10 as the LIT path: EST = 123.4, the
        # converter's own /10 then yields V = 12.34 (docs/104/105).
        self.Z(F.DIV, "TEN")
        self.Z(F.ATX, "EST")


def measure(sign="plain", drop_last_ati=True, floor_acc=True):
    s = VStream()
    hw = s.assemble("ABS", True, True, sign, drop_last_ati, floor_acc)
    return (len(hw) + 1) // 2, len(hw), s


def build(case, patch=None, sign="plain", src=None):
    src = Path(src) if src else WS / "images/2048_base"
    dst = WS / "images" / f"2048_{case}"
    shutil.copy2(src, dst)
    body = rz(str(dst), N + 1)
    body[0o11] = word(long_(0o300, 0o30114, reg=0), F.DUMMY)
    body[0o27] = int.from_bytes(bytes([2, 1, 15, 15, 0, 0]), "big")
    body[0o30] = int.from_bytes(bytes([0, 0, 14, 0, 0, 15]), "big")
    body[0o31] = int.from_bytes(bytes([15, 3, 0, 0, 0, 14]), "big")
    body[0o32] = int.from_bytes(bytes([0, 0, 0o231, 15, 15, 15]), "big")
    v = FS.vals()
    v["T7"] = SR24                     # shift-24 control cell (T7 reused)
    for n, value in v.items():
        body[F.BODY0 + F.CELLS.index(n)] = value & MASK

    # zone N+2 symbol table (no overlay-table offsets touched)
    z2 = rz(str(dst), N2)
    tab = {1: ("X       ", f32(7890.0)),
           2: ("Y       ", f32(1234.0))}
    if patch:
        tab.update(patch)
    for vidx, (nm, val) in tab.items():
        z2[N2_NAME + vidx] = text_word(nm)
        z2[N2_VAL + vidx] = val & MASK
    wz(str(dst), N2, z2)

    words, hw_count, s = measure(sign, True, True)
    hw = s.hw
    z3 = [0] * 1024
    for i in range(len(hw) // 2):
        z3[i] = word(hw[2*i], hw[2*i+1])
    if len(hw) % 2:
        z3[len(hw)//2] = word(hw[-1], F.DUMMY)
    wz(str(dst), N + 1, body)
    wz(str(dst), Z3, z3)
    sha = hashlib.sha256(dst.read_bytes()).hexdigest()
    print(f"case={case} sha={sha} words={words}/{MAX_WORDS} hw={hw_count} "
          f"subram={oct(s.sub_ram)} N2VAL_RAM=0o{N2_VAL_RAM:o}")
    return dst, sha


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--measure", action="store_true")
    ap.add_argument("--build")
    a = ap.parse_args()
    if a.measure:
        w, h, s = measure()
        print(f"sign=plain words={w}/{MAX_WORDS} hw={h} subram={oct(s.sub_ram)} "
              f"{'OK' if w <= MAX_WORDS else 'OVER %d' % (w - MAX_WORDS)}")
    if a.build:
        build(a.build)
