#!/usr/bin/env python3
"""Zone-2350 contour: FULL multi-digit LIT operand of a FRONT 777005 IR record.

Reads four decimal digits of `arg1` (e.g. 1234 for X=12.34) from the card
buffer word RAM 0o64014, assembles the integer on the BESM-6, normalizes it
to a BESM float, then feeds the PROVEN docs/98 ABS + 2+2 GOST chain.

Machine-code reuse (verbatim chains, docs/98/100):
  * UTC6 + xta 4014 card read (docs/93/99),
  * ARX NEG31 one-instruction ASCII->digit and 10*T[] table assembly (docs/98),
  * e+x EMASK / e+x C105 integer->float (docs/90),
  * shared floor_int VJM subroutine, 4 GOST deposits, resident *64 2004 (docs/98).

Only mechanism constants live in low RAM. No host-computed result digit is
stored anywhere in the image.
"""
import argparse
import hashlib
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_e2e import rz, wz, short, word, f32, MASK, N, Z3, MAX_WORDS, long_, checksum

WS = HERE.parent

ATX, AAX, AEX, ARX, ASX = 0o00, 0o11, 0o12, 0o13, 0o26
DIV, MUL, FADD, XSUB = 0o16, 0o17, 0o04, 0o06
ATI, EPLUSX, E64, ASN, ITA = 0o40, 0o24, 0o64, 0o36, 0o42
UTC6 = (0o220 << 12) | 0o60000
UJ15 = 0o67000000
LINK = 11                                   # decimal 11 = octal 13 (odd reg)
RET_LINK = (LINK << 20) | (0o30 << 15)      # uj 0(11)
DUMMY = 0o777700000000 & 0xffffff
CARD_WORD = 0o4014                          # 0o60000 + 0o4014 = 0o64014

CELLS = ["NUM", "EST", "HUNDRED", "SR24", "SR16", "SR8", "M8", "EMASK",
         "C105", "M40", "CW", "TEN", "V", "SCR", "I1f", "I0f", "F1f",
         "EPS", "CARD", "NEG31"] + ["T%d" % d for d in range(10)]
BODY0 = 0o110
RAM_SHIFT = 0o14
LO = {n: 0o1757 + RAM_SHIFT + BODY0 + i for i, n in enumerate(CELLS)}


def vals():
    return {
        "NUM": 0, "EST": 0, "HUNDRED": f32(100.0),
        "SR24": (64 + 24) << 41, "SR16": (64 + 16) << 41,
        "SR8": (64 + 8) << 41,
        "M8": 0o377, "EMASK": 0o177 << 41, "C105": 0o151 << 41,
        "M40": 0xFFFFFFFFFF, "CW": 0, "TEN": f32(10.0),
        "V": 0, "SCR": 0, "I1f": 0, "I0f": 0, "F1f": 0,
        "EPS": f32(2.0 ** -18), "CARD": 0,
        "NEG31": (-0x31) & MASK,
        **{"T%d" % d: d * 10 for d in range(10)},
    }


class Stream:
    def __init__(self):
        self.hw = []
        self.sub_ram = None

    def E(self, x):
        self.hw.append(x & 0xffffff)

    def Z(self, op, name):
        self.E(short(op, LO[name], reg=0))

    def L(self, op, adr, reg=0):
        self.E(short(op, adr, reg=reg))

    def vjm(self, addr):
        return (LINK << 20) | (0o31 << 15) | (addr & 0o77777)

    def VJM(self, addr):
        # VJM sets M[link]=PC+1 (next WORD); a call in the LEFT half skips
        # the right half on return -> put a dummy there (never executed).
        if len(self.hw) % 2 == 0:
            self.E(self.vjm(addr)); self.E(DUMMY)
        else:
            self.E(self.vjm(addr))

    def ir_read4(self):
        # Card word 0o64014, arg1 bytes [2..5] (COSY RLE decoded):
        #   '1','2','3','4' at byte 2,3,4,5 (d1..d4, shifts 24,16,8,0).
        self.E(UTC6)
        self.L(0o10, CARD_WORD, 0)
        self.Z(ATX, "CARD")                     # preserve card word
        # d1*10 + d2 -> float 12 -> NUM
        self.Z(ASX, "SR24"); self.Z(AAX, "M8"); self.Z(ARX, "NEG31")
        self.L(ATI, 6)
        self.Z(0o10, "CARD"); self.Z(ASX, "SR16"); self.Z(AAX, "M8")
        self.Z(ARX, "NEG31")
        self.L(ARX, LO["T0"], reg=6)            # ACC += T[d1] = d1*10
        self.Z(EPLUSX, "EMASK"); self.Z(EPLUSX, "C105")
        self.Z(ATX, "NUM")
        # d3*10 + d4 -> float 34 -> CARD (card word no longer needed)
        self.Z(0o10, "CARD"); self.Z(ASX, "SR8"); self.Z(AAX, "M8")
        self.Z(ARX, "NEG31")
        self.L(ATI, 6)
        self.Z(0o10, "CARD"); self.Z(AAX, "M8"); self.Z(ARX, "NEG31")
        self.L(ARX, LO["T0"], reg=6)
        self.Z(EPLUSX, "EMASK"); self.Z(EPLUSX, "C105")
        self.Z(ATX, "CARD")
        # NUM*100 + CARD -> full arg1 as integer-valued float
        self.Z(0o10, "NUM"); self.Z(MUL, "HUNDRED")
        self.Z(FADD, "CARD"); self.Z(ATX, "NUM")

    def intrinsic(self):
        # ABS of arg1/10: ACC holds float(arg1) from ir_read4's final atx NUM.
        # arg1 is the literal scaled by 100; one on-machine /10 (the same TEN
        # constant the GOST converter uses) gives arg1/10, and the converter's
        # own /10 then yields the original literal as V (e.g. 1234 -> 12.34).
        self.Z(DIV, "TEN")
        self.Z(ATX, "EST")

    def floor(self):
        self.Z(0o10, "SCR"); self.Z(AEX, "EMASK")
        self.Z(EPLUSX, "C105"); self.Z(ATX, "CW")
        self.Z(AAX, "M40"); self.Z(ASX, "CW")

    def floor_acc(self):
        # docs/100 reclaim: atx SCR preserves ACC, so the subroutine needs
        # no xta SCR; it starts with aex EMASK.
        self.Z(AEX, "EMASK"); self.Z(EPLUSX, "C105")
        self.Z(ATX, "CW"); self.Z(AAX, "M40"); self.Z(ASX, "CW")

    def digit(self, shift, out=None, no_ati=False):
        if not no_ati:
            self.L(ATI, 5)
        self.L(ASN, shift)
        self.L(ARX, 0o2007); self.L(ATX, 0o2007)
        if out:
            self.L(ITA, 5)
            self.Z(EPLUSX, "EMASK"); self.Z(EPLUSX, "C105")
            self.Z(ATX, out)

    def converter(self, use_sub, floor_acc=False, drop_last_ati=False):
        self.Z(0o10, "EST"); self.Z(DIV, "TEN"); self.Z(ATX, "V")
        fl = self.floor_acc if floor_acc else self.floor
        self.Z(0o10, "V"); self.Z(DIV, "TEN"); self.Z(ATX, "SCR")
        self.VJM(self.sub_ram) if use_sub else fl()
        self.digit(0o30, "I1f")
        self.Z(0o10, "I1f"); self.Z(MUL, "TEN"); self.Z(XSUB, "V")
        self.Z(ATX, "SCR")
        self.VJM(self.sub_ram) if use_sub else fl()
        self.digit(0o40, "I0f")
        self.Z(0o10, "V"); self.Z(MUL, "TEN"); self.Z(ATX, "SCR")
        self.Z(0o10, "I1f"); self.Z(MUL, "TEN"); self.Z(FADD, "I0f")
        self.Z(MUL, "TEN"); self.Z(XSUB, "SCR"); self.Z(FADD, "EPS")
        self.Z(ATX, "SCR")
        self.VJM(self.sub_ram) if use_sub else fl()
        self.digit(0o60, "F1f")
        self.Z(0o10, "V"); self.Z(MUL, "TEN"); self.Z(MUL, "TEN")
        self.Z(ATX, "SCR")
        self.Z(0o10, "I1f"); self.Z(MUL, "TEN"); self.Z(FADD, "I0f")
        self.Z(MUL, "TEN"); self.Z(FADD, "F1f"); self.Z(MUL, "TEN")
        self.Z(XSUB, "SCR"); self.Z(FADD, "EPS"); self.Z(ATX, "SCR")
        self.VJM(self.sub_ram) if use_sub else fl()
        self.digit(0o70, no_ati=drop_last_ati)

    def assemble(self, use_sub=True, floor_acc=False, drop_last_ati=False):
        self.sub_ram = 0
        self.ir_read4(); self.intrinsic(); self.converter(True, floor_acc, drop_last_ati)
        self.L(E64, 0o2004)
        if len(self.hw) % 2:
            self.E(DUMMY)
        self.E(UJ15)
        main_len = len(self.hw)
        sub_idx = (main_len + 1) // 2 * 2
        self.sub_ram = 0o30114 + sub_idx // 2
        while len(self.hw) < sub_idx:
            self.E(DUMMY)
        for i, x in enumerate(self.hw):
            if (x >> 20) == LINK and ((x >> 12) & 0o370) == 0o310:
                self.hw[i] = self.vjm(self.sub_ram)
        if floor_acc:
            self.floor_acc()
        else:
            self.floor()
        self.E(RET_LINK)
        return self.hw


def measure(floor_acc=False, drop_last_ati=False):
    s = Stream(); hw = s.assemble(True, floor_acc, drop_last_ati)
    return (len(hw) + 1) // 2, len(hw), s.sub_ram


def build(case, floor_acc=False, drop_last_ati=False, patch=None, src=None):
    src = Path(src) if src else WS / "images/2048_base"
    dst = WS / "images" / f"2048_{case}"
    shutil.copy2(src, dst)
    body = rz(str(dst), N + 1)
    body[0o11] = word(long_(0o300, 0o30114, reg=0), DUMMY)
    # Proven codegen_wide GOST text (docs/89/90/98): prefix 21, zero digit
    # seeds, fixed Y field and format tail.
    body[0o27] = int.from_bytes(bytes([2, 1, 15, 15, 0, 0]), "big")
    body[0o30] = int.from_bytes(bytes([0, 0, 14, 0, 0, 15]), "big")
    body[0o31] = int.from_bytes(bytes([15, 3, 0, 0, 0, 14]), "big")
    body[0o32] = int.from_bytes(bytes([0, 0, 0o231, 15, 15, 15]), "big")
    v = vals()
    if patch:
        v.update(patch)
    for n, value in v.items():
        body[BODY0 + CELLS.index(n)] = value & MASK
    s = Stream(); hw = s.assemble(True, floor_acc, drop_last_ati)
    z3 = [0] * 1024
    for i in range(len(hw) // 2):
        z3[i] = word(hw[2 * i], hw[2 * i + 1])
    if len(hw) % 2:
        z3[len(hw) // 2] = word(hw[-1], DUMMY)
    wz(str(dst), N + 1, body)
    wz(str(dst), Z3, z3)
    sha = hashlib.sha256(dst.read_bytes()).hexdigest()
    print(f"case={case} sha={sha} words={(len(hw)+1)//2}/{MAX_WORDS} "
          f"hw={len(hw)} floor_acc={floor_acc} drop_ati={drop_last_ati} "
          f"subram={oct(s.sub_ram)}")
    return dst, sha


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--measure", action="store_true")
    ap.add_argument("--build")
    ap.add_argument("--floor-acc", action="store_true")
    ap.add_argument("--drop-last-ati", action="store_true")
    ap.add_argument("--patch-t1", type=int, default=None,
                    help="override T[1] (one machine-word patch gate)")
    a = ap.parse_args()
    if a.measure or not a.build:
        for fa in (False, True):
            for da in (False, True):
                c, h, sr = measure(fa, da)
                print(f"floor_acc={fa!s:5s} drop_ati={da!s:5s} "
                      f"words={c}/{MAX_WORDS} hw={h} subram={oct(sr)} "
                      f"{'OK' if c <= MAX_WORDS else 'OVER %d' % (c-MAX_WORDS)}")
    if a.build:
        patch = {"T1": a.patch_t1} if a.patch_t1 is not None else None
        build(a.build, a.floor_acc, a.drop_last_ati, patch)
