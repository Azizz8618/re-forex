#!/usr/bin/env python3
"""Fully-resolved optimized contour: SQRT/ABS + 2-digit deck + 2+2 GOST in 58 words.

Zone N+3 holds CODE ONLY; all constants/scratch go to proven-free low-RAM
body cells (12-bit reg=0 ADR).  floor_int is a VJM subroutine; VJM is placed
in the RIGHT half of a word (simh: M[link]=PC+1 skips the right half when the
call is in the left half).
"""
import sys, hashlib, shutil
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_e2e import rz, wz, short, word, f32, MASK, N, Z3, MAX_WORDS, checksum

# ---- encoders ----
ATX, AAX, AEX, ARX, ASX = 0o00, 0o11, 0o12, 0o13, 0o26
DIV, MUL, FADD, XSUB = 0o16, 0o17, 0o04, 0o06
ATI, EPLUSX, E64, ITA, ASN = 0o40, 0o24, 0o64, 0o42, 0o36
UTC6 = (0o220 << 12) | 0o60000
UJ15 = 0o67000000          # uj 0(13 decimal = octal 15) : return to resident
# VJM must not clobber M[13] (the resident return link).  Long-format
# instructions need an ODD reg field (simh: RK & BBIT(20)); M[11] is unused.
LINK = 11                   # decimal 11 = octal 13
RET_LINK = (LINK << 20) | (0o30 << 15)   # uj 0(11) : subroutine return
DUMMY = 0o777700000000 & 0xffffff  # never executed (skipped by VJM)
CARD_WORD = 0o4012

def vjm(addr):
    # long VJM, reg14 link, opcode 0o310, 15-bit word address
    return (LINK << 20) | (0o31 << 15) | (addr & 0o77777)

# ---- low-RAM data cells (proven-free body[0o110..]) ----
# FACT (C-oracle CORE at PC 01770): *TRANS maps body[0..0o77] to RAM 0o1757+k,
# but body[0o100..] to RAM 0o1757+0o14+k (the tail copy has a 12-word offset).
CELLS = ["NUM", "EST", "HALF", "SR16", "SR8", "M8", "PD0", "EMASK",
         "C105", "M40", "CW", "TEN", "V", "SCR", "I1f", "I0f", "F1f",
         "EPS", "CARD", "NEG31"] + ["T%d" % d for d in range(10)]
BODY0 = 0o110
RAM_SHIFT = 0o14
LO = {n: 0o1757 + RAM_SHIFT + BODY0 + i for i, n in enumerate(CELLS)}

def vals():
    return {
        "NUM": 0, "EST": 0, "HALF": f32(0.5),
        "SR16": (64 + 16) << 41, "SR8": (64 + 8) << 41,
        "M8": 0o377, "PD0": 0xD0,
        "EMASK": 0o177 << 41, "C105": 0o151 << 41,
        "M40": 0xFFFFFFFFFF, "CW": 0,
        "TEN": f32(10.0), "V": 0, "SCR": 0,
        "I1f": 0, "I0f": 0, "F1f": 0,
        "EPS": f32(2.0 ** -18), "CARD": 0,
        # ARX NEG31 = ASCII(d) + (-0x31) with ARX end-around carry -> digit d,
        # valid for d=1..9 (our deck literals 12/34 use only non-zero digits).
        "NEG31": (-0x31) & MASK,
        # TABLE[d] = d*10 (integer): indexed by M[6]=tens digit in ARX T(6)
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
    def VJM(self, addr):
        # simh: M[link]=PC+1 (next WORD), so a call in the LEFT half skips
        # the right half on return.  Put a dummy there (never executed).
        if len(self.hw) % 2 == 0:
            self.E(vjm(addr))
            self.E(DUMMY)      # right half, skipped by the jump
        else:
            self.E(vjm(addr))  # right half: return goes to next word left
    def deck_read(self, two=True):
        self.E(UTC6)
        self.L(0o10, CARD_WORD, 0)
        if two:
            self.Z(ATX, "CARD")        # preserve card word for digit 2
        self.Z(ASX, "SR16"); self.Z(AAX, "M8")
        self.Z(ARX, "NEG31")   # one-instruction ASCII->digit (d=1..9)
        if not two:
            self.Z(EPLUSX, "EMASK"); self.Z(EPLUSX, "C105")
            self.Z(ATX, "NUM")
        else:
            # tens*10 + units via low-RAM table indexed by M[6]=tens:
            # ACC=units; ARX T(6) adds TABLE[tens]=tens*10.
            self.L(ATI, 6)
            self.Z(0o10, "CARD")       # reload card word
            self.Z(ASX, "SR8"); self.Z(AAX, "M8")
            self.Z(ARX, "NEG31")
            self.L(ARX, LO["T0"], reg=6)   # ACC += T[tens]
            self.Z(EPLUSX, "EMASK"); self.Z(EPLUSX, "C105")
            self.Z(ATX, "NUM")
    def intrinsic(self, kind):
        # ACC still holds float(N) from the deck read's final atx NUM,
        # so store it directly to EST without a reload (saves one halfword).
        self.Z(ATX, "EST")
        if kind == "SQRT":
            for _ in range(4):
                self.Z(0o10, "NUM"); self.Z(DIV, "EST")
                self.Z(FADD, "EST"); self.Z(MUL, "HALF")
                self.Z(ATX, "EST")
    def floor(self):
        self.Z(0o10, "SCR"); self.Z(AEX, "EMASK")
        self.Z(EPLUSX, "C105"); self.Z(ATX, "CW")
        self.Z(AAX, "M40"); self.Z(ASX, "CW")
    def digit(self, shift, out=None):
        self.L(ATI, 5); self.L(ASN, shift)
        self.L(ARX, 0o2007); self.L(ATX, 0o2007)
        if out:
            self.L(ITA, 5)
            self.Z(EPLUSX, "EMASK"); self.Z(EPLUSX, "C105")
            self.Z(ATX, out)
    def converter(self, use_sub):
        # The intrinsic result lives in EST (docs/95 chain), not NUM.
        self.Z(0o10, "EST"); self.Z(DIV, "TEN"); self.Z(ATX, "V")
        # tens
        self.Z(0o10, "V"); self.Z(DIV, "TEN"); self.Z(ATX, "SCR")
        self.VJM(self.sub_ram) if use_sub else self.floor()
        self.digit(0o30, "I1f")
        # units
        self.Z(0o10, "I1f"); self.Z(MUL, "TEN"); self.Z(XSUB, "V")
        self.Z(ATX, "SCR")
        self.VJM(self.sub_ram) if use_sub else self.floor()
        self.digit(0o40, "I0f")
        # tenths
        self.Z(0o10, "V"); self.Z(MUL, "TEN"); self.Z(ATX, "SCR")
        self.Z(0o10, "I1f"); self.Z(MUL, "TEN"); self.Z(FADD, "I0f")
        self.Z(MUL, "TEN"); self.Z(XSUB, "SCR"); self.Z(FADD, "EPS")
        self.Z(ATX, "SCR")
        self.VJM(self.sub_ram) if use_sub else self.floor()
        self.digit(0o60, "F1f")
        # hundredths
        self.Z(0o10, "V"); self.Z(MUL, "TEN"); self.Z(MUL, "TEN")
        self.Z(ATX, "SCR")
        self.Z(0o10, "I1f"); self.Z(MUL, "TEN"); self.Z(FADD, "I0f")
        self.Z(MUL, "TEN"); self.Z(FADD, "F1f"); self.Z(MUL, "TEN")
        self.Z(XSUB, "SCR"); self.Z(FADD, "EPS"); self.Z(ATX, "SCR")
        self.VJM(self.sub_ram) if use_sub else self.floor()
        self.digit(0o70)
    def assemble(self, kind, two=True, use_sub=True):
        # We need the subroutine RAM address before emitting calls.
        # Compute it by a dry run: main stream length, then round up to word.
        if use_sub:
            # dry run to learn main hw length
            dry = Stream(); dry.deck_read(two); dry.intrinsic(kind)
            dry.converter(False)  # inline floors for length only? no: need VJM len
            # Instead: build main with placeholder sub_ram=0, count, then rebuild.
            self.sub_ram = 0
            self.deck_read(two); self.intrinsic(kind); self.converter(True)
            self.L(E64, 0o2004)
            # *64 is an EXTRACODE: it sets M[ERET]=PC+1 and returns to the
            # next WORD, skipping the right half of its own word.
            if len(self.hw) % 2:
                self.E(DUMMY)
            self.E(UJ15)
            main_len = len(self.hw)
            # subroutine starts at next word boundary
            sub_idx = (main_len + 1) // 2 * 2
            self.sub_ram = 0o30114 + sub_idx // 2
            # pad to sub_idx
            while len(self.hw) < sub_idx:
                self.E(DUMMY)
            # rebuild calls with correct address by patching the VJM halfwords
            for i, x in enumerate(self.hw):
                if (x >> 20) == LINK and ((x >> 12) & 0o370) == 0o310:
                    self.hw[i] = vjm(self.sub_ram)
            self.floor(); self.E(RET_LINK)
        else:
            self.deck_read(two); self.intrinsic(kind); self.converter(False)
            self.L(E64, 0o2004)
            if len(self.hw) % 2:
                self.E(DUMMY)
            self.E(UJ15)
        return self.hw

def measure(kind, two, use_sub):
    s = Stream(); hw = s.assemble(kind, two, use_sub)
    code = (len(hw) + 1) // 2
    return code, len(hw), s.sub_ram

def build(case, kind="SQRT", two=True, use_sub=True, patch=None,
          ws="/tmp/.private/azizz/opencode/budget-opt"):
    """Build a complete contour image; patch = {cell_name: value} overrides."""
    import shutil
    ws = Path(ws)
    src = ws / "images/2048_base"
    dst = ws / "images" / f"2048_{case}"
    shutil.copy2(src, dst)
    body = rz(str(dst), N + 1)
    # entry substitution: long uj 30114
    body[0o11] = word(long_(0o300, 0o30114, reg=0), DUMMY)
    # codegen_wide GOST layout: prefix 21, zero seed digit bytes, fixed text
    body[0o27] = int.from_bytes(bytes([2, 1, 15, 15, 0, 0]), "big")
    body[0o30] = int.from_bytes(bytes([0, 0, 14, 0, 0, 15]), "big")
    body[0o31] = int.from_bytes(bytes([15, 3, 0, 0, 0, 14]), "big")
    body[0o32] = int.from_bytes(bytes([0, 0, 0o231, 15, 15, 15]), "big")
    # low-RAM data cells
    v = vals()
    if patch:
        v.update(patch)
    for n, value in v.items():
        body[0o110 + CELLS.index(n)] = value & MASK
    # zone N+3: code + optional subroutine
    s = Stream(); hw = s.assemble(kind, two, use_sub)
    z3 = [0] * 1024
    for i in range(len(hw) // 2):
        z3[i] = word(hw[2*i], hw[2*i+1])
    if len(hw) % 2:
        z3[len(hw)//2] = word(hw[-1], DUMMY)
    wz(str(dst), N + 1, body)
    wz(str(dst), Z3, z3)
    sha = hashlib.sha256(dst.read_bytes()).hexdigest()
    print(f"case={case} kind={kind} two={two} sub={use_sub} sha={sha} "
          f"code={(len(hw)+1)//2} hw={len(hw)} subram={oct(s.sub_ram) if s.sub_ram else '-'}")
    return dst, sha


def long_(op, adr, reg=0):
    return (reg << 20) | (op << 12) | (adr & 0o77777)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--measure", action="store_true")
    ap.add_argument("--build")
    ap.add_argument("--kind", default="SQRT")
    ap.add_argument("--one-digit", action="store_true")
    ap.add_argument("--no-sub", action="store_true")
    a = ap.parse_args()
    if a.measure or not a.build:
        for kind in ("ABS", "SQRT"):
            for two in (False, True):
                for sub in (True, False):
                    c, h, sr = measure(kind, two, sub)
                    print(f"{kind:4s} {'2dig' if two else '1dig'} "
                          f"{'SUB ' if sub else 'INL '} code={c:3d} hw={h:3d} "
                          f"subram={sr if sr else '-':>7} "
                          f"{'OK' if c<=58 else 'OVER %d'%(c-58)}")
    if a.build:
        build(a.build, kind=a.kind, two=not a.one_digit, use_sub=not a.no_sub)
