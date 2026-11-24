#!/usr/bin/env python3
"""D1: on-machine formatted-input primitive for the variant-B contour.

BASE: byte-identical copy of 2048_B9_A (SHA 81d7790f...).  The only image
edits are a contour-entry trampoline and a machine-code scanner in the
proven-free N+1 body band body[0o1300..0o1600] (docs/120).  The untouched
LEX/parser is re-entered at its original address RAM 0o27740.

The scanner walks the raw card buffer 0o64000+k, finds the F8.2 DATA card by
its ASCII '.' at byte 3, decodes the four digits with the verbatim B1/B5
digit path, divides by 10 twice and stores the value into the contour's X
cell (N+2[33]) before the source is compiled.  PRINT then uses the proven
GOST path.  No host value, no 777005, no system compiler.
"""
import argparse, hashlib, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from build_e2e import rz, wz, short, long_, word, f32, MASK, N

WS = HERE.parent
SRC = WS / "images" / "2048_B9_A"
LEX_ENTRY = 0o27740

ATX, AAX, AEX, ARX, ASX = 0o00, 0o11, 0o12, 0o13, 0o26
E24, MUL, DIV, ADD = 0o24, 0o17, 0o16, 0o04
ATI, ITA, UJ, UZA = 0o40, 0o42, 0o300, 0o260
DUMMY = 0

def ram2body(ram):
    return 0o1237 + (ram - 0o21066)

CODE_RAM = 0o21200
DATA_RAM = 0o21300

class Asm:
    def __init__(self):
        self.hw = []; self.labels = {}; self.fixups = []
    def E(self, x): self.hw.append(x & 0xffffff)
    def L(self, op, adr, reg=0): self.E(short(op, adr, reg=reg))
    def C(self, op, cell, reg=12): self.L(op, cell - 0o20000, reg=reg)
    def mark(self, name):
        while len(self.hw) % 2: self.E(DUMMY)
        self.labels[name] = len(self.hw)
    def br(self, op, name):
        i = len(self.hw); self.E(long_(op, 0)); self.fixups.append((i, name, op))
    def ram_of_label(self, name):
        j = self.labels[name]
        return CODE_RAM + j // 2 + (j % 2)
    def resolve(self):
        for i, name, op in self.fixups:
            self.hw[i] = long_(op, self.ram_of_label(name))
    def words(self):
        if len(self.hw) % 2: self.E(DUMMY)
        return [word(self.hw[2*i], self.hw[2*i+1]) for i in range(len(self.hw)//2)]

def build(case, src=SRC, scale=10):
    src = Path(src)
    a = Asm()
    names = ["N2BASE", "CBASE", "ZERO", "ONE", "POSLIM", "WORD", "SR16",
             "SR32", "SR24", "SR8", "SR0", "MFF", "M0F", "DOT", "EMASK",
             "C105", "TEN", "SCALE", "DIG", "DF", "F"]
    A = {n: DATA_RAM + i for i, n in enumerate(names)}  # one word per RAM address

    # prologue: load the N+2 base through the one-shot UTC modifier first;
    # every later data access may then use reg=12 (M[12]=0o20000).
    a.E(long_(0o220, 0o20000))       # utc 20000
    a.L(0o10, A["N2BASE"] - 0o20000, reg=0)   # xta 1300 -> RAM 0o21300
    a.L(ATI, 12)                     # M[12] = 0o20000
    a.C(0o10, A["ZERO"]);   a.L(ATI, 11)

    # scan card words 0o64000+k for ASCII '.' at byte 3.  The card page is
    # armed by a one-shot UTC immediately before every read (docs/93/94).
    a.mark("SCAN")
    a.E(long_(0o220, 0o60000))
    a.L(0o10, 0o4000, reg=11)
    a.C(ATX, A["WORD"])
    a.C(ASX, A["SR16"]); a.C(AAX, A["MFF"]); a.C(AEX, A["DOT"])
    a.br(UZA, "FOUND")
    a.L(ITA, 11); a.C(ARX, A["ONE"]); a.L(ATI, 11)
    a.L(ITA, 11); a.C(AEX, A["POSLIM"])   # logical XOR: zero exactly at k=32
    a.br(UZA, "NOFIELD")
    a.br(UJ, "SCAN")

    # decode 4 digits with the verbatim B1/B5 path
    a.mark("FOUND")
    def digit(shift):
        a.C(0o10, A["WORD"]); a.C(ASX, A[shift]); a.C(AAX, A["M0F"]); a.C(ATX, A["DIG"])
        a.C(0o10, A["DIG"]); a.C(E24, A["EMASK"]); a.C(E24, A["C105"]); a.C(ATX, A["DF"])
        a.C(0o10, A["F"]); a.C(MUL, A["TEN"]); a.C(ADD, A["DF"]); a.C(ATX, A["F"])
    digit("SR32"); digit("SR24"); digit("SR8"); digit("SR0")
    a.C(0o10, A["F"]); a.C(DIV, A["TEN"]); a.C(ATX, A["F"])
    a.C(0o10, A["F"]); a.C(DIV, A["TEN"]); a.C(ATX, A["F"])
    a.C(0o10, A["F"]); a.C(MUL, A["SCALE"]); a.C(ATX, A["F"])  # contour stores 10x
    a.C(0o10, A["F"]); a.C(ATX, 0o21700)   # variable X: N+2 base 0o21677 + VIDX 1
    a.br(UJ, "DONE")

    a.mark("NOFIELD"); a.mark("DONE")
    a.E(long_(UJ, LEX_ENTRY))

    a.resolve()
    code = a.words()
    ncode = len(code)
    assert CODE_RAM + ncode <= DATA_RAM, oct(CODE_RAM + ncode)

    vals = {
        "N2BASE": 0o20000, "CBASE": 0o60000, "ZERO": 0, "ONE": 1,
        "POSLIM": 0o40, "WORD": 0,
        "SR16": (64+16) << 41, "SR32": (64+32) << 41,
        "SR24": (64+24) << 41, "SR8": (64+8) << 41, "SR0": 64 << 41,
        "MFF": 0xff, "M0F": 0x0f, "DOT": 0x2e,
        "EMASK": 0o177 << 41, "C105": 0o151 << 41,
        "TEN": f32(10.0), "SCALE": f32(10.0 if scale == 10 else 11.0),
        "DIG": 0, "DF": 0, "F": 0,
    }
    dst = WS / "images" / case
    shutil.copy2(src, dst)
    body = rz(str(dst), N + 1)
    body[0o11] = word(long_(UJ, CODE_RAM, reg=0), 0)
    for i, w in enumerate(code):
        body[ram2body(CODE_RAM + i)] = w & MASK
    for n, v in vals.items():
        body[ram2body(A[n])] = v & MASK
    wz(str(dst), N + 1, body)
    sha = hashlib.sha256(dst.read_bytes()).hexdigest()
    print(f"case={case} sha={sha} code_words={ncode} code={oct(CODE_RAM)}.."
          f"{oct(CODE_RAM+ncode-1)} data={oct(DATA_RAM)}.."
          f"{oct(DATA_RAM+len(names)-1)}")
    return dst, sha

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--build", required=True)
    ap.add_argument("--src", default=str(SRC))
    ap.add_argument("--scale", type=int, default=10)
    x = ap.parse_args()
    build(x.build, src=x.src, scale=x.scale)
