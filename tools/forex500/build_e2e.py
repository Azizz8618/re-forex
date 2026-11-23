#!/usr/bin/env python3
"""ONE zone-2350 contour: deck literal -> on-machine SQRT -> on-machine float->GOST -> *64.

Reuses verbatim the proven machine-code chains:
  * deck card-word read at RAM 0o64012 via `utc 60000` + short `xta 4012` (docs/93,
    deck-args/build_deckargs3.py) and ASCII digit -> BESM float via asx/aax/arx;
  * Newton SQRT with FPU a/x, a+x, a*x and bitwise helper ops (docs/95,
    machine-intr/build.py ops_sqrt);
  * float -> single GOST digit via aex/e+x/aax/asx with an on-machine computed
    control word, asx/arx/atx deposit, resident *64 (docs/89,
    machine-intr/build.py converter).

Zone N+3 (RAM 0o30114..0o30205) is reached with M[7]=0o30000 as base register
(one SHORT halfword per high-RAM operand, ftgost-multi/build_own2.py pattern).
The card read is the only M20=0o60000 modifier access. Every edit is a
same-length machine-word substitution; the printed digit is never computed by
Python. Setup literals (0.5 / 0.4, FBASE, shift constants) are disclosed in the
report; they are arguments/mechanism constants, not result digits.

Usage:
  build_e2e.py case [--half 0.5|0.4]
"""
import argparse
import hashlib
import shutil
import sys
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
REPO = WS / "fixtures" / "repo"
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_zone2350_contour import checksum  # proven, read-only

MASK = (1 << 48) - 1
N = 0o2350
Z3 = 0o2353
ZONE_SIZE = 8256
DATA0 = 64
MAX_WORDS = 58
Z3_RAM0 = 0o30114

# ---- halfword encoders (verified against SIMH besm6_cpu.c:1049-1062) ----
def rz(path, logical):
    b = Path(path).read_bytes()
    base = (logical + 4) * ZONE_SIZE
    return [int.from_bytes(b[base + DATA0 + 8*i: base + DATA0 + 8*i + 6], "little")
            for i in range(1024)]


def wz(path, logical, words):
    phys = logical + 4
    base = phys * ZONE_SIZE
    b = bytearray(Path(path).read_bytes())
    for i, w in enumerate(words):
        off = base + DATA0 + 8*i
        b[off:off+6] = (w & MASK).to_bytes(6, "little")
        b[off+6:off+8] = b"\x00\x00"
    hdr = [((phys << 36) | 0x038ca3c918), 0x000005f1c7800000,
           0x0000410300000000, checksum(words)]
    for k in range(8):
        val = hdr[k % 4]
        if k >= 4 and k in (4, 6):
            val = (val & ~(0xfff << 36)) | (((phys + 1) << 36) & (0xfff << 36))
        off = base + 8*k
        b[off:off+6] = val.to_bytes(6, "little")
        b[off+6:off+8] = b"\x00\x00"
    Path(path).write_bytes(b)


def short(op, adr, reg=0):
    return (reg << 20) | (op << 12) | (adr & 0o7777)


def long_(op, adr, reg=0):
    return (reg << 20) | (op << 12) | (adr & 0o77777)


def word(l, r):
    return ((l & 0xffffff) << 24) | (r & 0xffffff)


def f32(value):
    if value == 0:
        return 0
    import math
    m, e = math.frexp(value)
    mant = int(round(m * (1 << 40)))
    exp = e + 64
    assert 1 << 39 <= mant < 1 << 40 and 0 <= exp < 128
    return ((exp << 41) | mant) & MASK


# opcodes (verified against SIMH besm6_cpu.c and predecessor MTR traces)
ATX, AAX, AEX, ARX, ASX = 0o00, 0o11, 0o12, 0o13, 0o26
DIV, MUL, FADD = 0o16, 0o17, 0o04
ATI, EPLUSX, E64 = 0o40, 0o24, 0o64
UTC = long_(0o220, 0o30000)      # arm M20 = 0o30000 (base) for next halfword
UTC6 = long_(0o220, 0o60000)     # arm M20 = 0o60000 (card page) for next halfword
UJ15 = 0o67000000                # LONG uj 0(15) return to resident at 0o1764
GOST_A, DESC = 0o2006, 0o2004
CARD_WORD = 0o4012               # short reg0 address under M20=0o60000 -> 0o64012

# mechanism constants (NOT result digits)
BASE_CONST = 0o30000
SR16 = (64 + 16) << 41           # asx right 16: card digit byte -> low byte
MASK8 = 0o377                    # isolate ASCII digit byte
PD0 = 0xD0                       # ASCII 0x3x + 0xd0 -> 0x1NN, low byte = digit
EMASK = 0o177 << 41
C105 = 0o151 << 41
M40 = 0xFFFFFFFFFF
CWL16 = 0o60 << 41               # asx left 16 -> GOST word A byte 3

ALL_CELLS = ["BASE", "NUM", "EST", "HALF", "SR16", "M8", "PD0",
             "EMASK", "C105", "M40", "CW", "CWL16"]
DATA = {}
HW = []


def Z(op, name):
    """High-RAM operand via M[7]=0o30000 base."""
    HW.append(("z", op, name))


def L(op, adr, reg=0):
    HW.append(("l", op, adr, reg))


# ---- prologue: install M[7] = 0o30000 ----
HW.append(("u", 0o10, "BASE"))    # utc 30000 ; xta BASE(reg0) -> ACC = 0o30000
L(ATI, 7)                        # M[7] = 0o30000

# ---- deck literal -> float N (docs/93 chain) ----
HW.append(("u6",))                # utc 60000
L(0o10, CARD_WORD, 0)            # xta 4012 (reg0) -> ACC = card word at 0o64012
Z(ASX, "SR16")                   # right 16 -> ASCII digit in low byte
Z(AAX, "M8")                     # isolate ASCII digit
Z(ARX, "PD0")                    # +0xd0 -> 0x1NN
Z(AAX, "M8")                     # -> integer digit 0..9
# integer digit -> BESM float via e+x normalization (docs/90, proven for any
# integer 0..99). The predecessor's `asx left41 + arx FBASE` shortcut only
# works for single-bit digits (1,2,4,8): digit 9 spills into the exponent field.
Z(EPLUSX, "EMASK")               # +63 and normalize
Z(EPLUSX, "C105")                # +41 -> float N (exponent 65+floor(log2 N))
Z(ATX, "NUM")                    # store N

# ---- SQRT(N): 4 Newton iterations, result stays in EST (docs/95 chain) ----
Z(0o10, "NUM")
Z(ATX, "EST")
for _ in range(4):
    Z(0o10, "NUM")               # ACC = S
    Z(DIV, "EST")                # ACC = S/x
    Z(FADD, "EST")               # ACC = S/x + x (FLOATING add)
    Z(MUL, "HALF")               # ACC = (S/x + x)*HALF
    Z(ATX, "EST")                # x = new estimate

# ---- float(EST) -> one GOST digit and *64 (docs/89 chain) ----
Z(0o10, "EST")
Z(AEX, "EMASK")                  # complement exponent field
Z(EPLUSX, "C105")                # on-machine control exponent = 168 - e
Z(ATX, "CW")                     # store computed asx control word
Z(0o10, "EST")                   # reload float result
Z(AAX, "M40")                    # isolate 40-bit mantissa
Z(ASX, "CW")                     # shift mantissa -> integer digit
Z(ASX, "CWL16")                  # digit << 16 (GOST byte 3)
L(ARX, GOST_A)                   # += GOST word A
L(ATX, GOST_A)                   # store GOST word A
L(E64, DESC)                     # resident *64 prints
HW.append(("uj",))               # return

# ---- resolve halfwords / layout ----
NCODE = (len(HW) + 1) // 2
for i, name in enumerate(ALL_CELLS):
    DATA[name] = 0o114 + NCODE + i          # short address under M[7]
assert max(DATA.values()) <= 0o7777
assert NCODE + len(ALL_CELLS) <= MAX_WORDS, (NCODE, len(ALL_CELLS), MAX_WORDS)

resolved = []
for h in HW:
    if h[0] == "z":
        resolved.append(short(h[1], DATA[h[2]], reg=7))
    elif h[0] == "ub":
        raise ValueError(h)
    elif h[0] == "u":
        resolved.append(UTC)
        resolved.append(short(h[1], DATA[h[2]], reg=0))
    elif h[0] == "u6":
        resolved.append(UTC6)
    elif h[0] == "l":
        resolved.append(short(h[1], h[2], reg=h[3]))
    elif h[0] == "uj":
        resolved.append(UJ15)
    else:
        raise ValueError(h)


def vals(half):
    return {
        "BASE": BASE_CONST, "NUM": 0, "EST": 0, "HALF": f32(half),
        "SR16": SR16, "M8": MASK8, "PD0": PD0,
        "EMASK": EMASK, "C105": C105, "M40": M40, "CW": 0, "CWL16": CWL16,
    }


def build(case, half=0.5, inplace_src=None):
    src = WS / "images/2048_base"
    dst = WS / "images" / f"2048_{case}"
    shutil.copy2(src, dst)
    body = rz(dst, N + 1)
    z3 = [0] * 1024

    # same-length substitution: contour entry at RAM 0o1770 -> our routine
    body[0o11] = word(long_(0o300, 0o30114, reg=0), 0o777700000000 & 0xffffff)
    # GOST word A: line prefix 21, X digit byte zeroed (filled at runtime)
    ba = bytearray(body[0o27].to_bytes(6, "big"))
    ba[0], ba[3] = 2, 0
    body[0o27] = int.from_bytes(ba, "big")

    hw = resolved[:]
    if len(hw) % 2:
        hw.append(0o777700000000 & 0xffffff)
    for i in range(len(hw) // 2):
        z3[i] = word(hw[2*i], hw[2*i+1])
    v = vals(half)
    for nm, value in v.items():
        z3[DATA[nm] - 0o114] = value & MASK  # zone index = short addr - 0o114

    wz(dst, N + 1, body)
    wz(dst, Z3, z3)
    sha = hashlib.sha256(dst.read_bytes()).hexdigest()
    print(f"case={case} half={half} sha={sha} code_words={NCODE} "
          f"data={len(ALL_CELLS)} total={NCODE + len(ALL_CELLS)}/{MAX_WORDS} "
          f"hw={len(HW)} HALF={v['HALF']:016o}")
    return dst, sha


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("case")
    ap.add_argument("--half", type=float, default=0.5)
    a = ap.parse_args()
    build(a.case, a.half)
