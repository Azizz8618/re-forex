#!/usr/bin/env python3
"""B3: STATEMENT DISPATCHER (prototype) from the B2 design.

The contour reads B2-layout token words pre-seeded in zone N+2 (fixture).  B1
will later emit those same token words from real Fortran text; at this milestone
the deck's Fortran body is inert.  Implemented statements: PROGRAM (consume),
REAL (zero value words), NAME=NUMBER (literal pool -> symbol value), PRINT with
an Fw.d width (restricted to the docs/113 w/d masks), END.  Every printed digit
is produced by the verbatim docs/105 GOST converter in N+3, called via VJM.

Copies only, no repo/live-disk/tmux-0/C patches.  C dispak is oracle only.
"""
import argparse
import hashlib
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import c6_build as C6
import c7_build as C7
import final_sign as FS
from build_e2e import rz, wz, short, long_, word, f32, MASK, N, Z3, MAX_WORDS

WS = HERE.parent
N2 = N + 2
N2_RAM0 = 0o21637
CODE_OFF = 150
CODE_RAM = N2_RAM0 + CODE_OFF
CONV_RAM0 = 0o30114

# opcodes (same values as c6_build)
ATX, AAX, AEX, ARX, ASX = 0o00, 0o11, 0o12, 0o13, 0o26
FADD, ATI, UJ, UZA = 0o04, 0o40, 0o300, 0o260
DUMMY = C6.FB.DUMMY
UJ15 = C6.FB.UJ15

# ---- N+2 map (all offsets < 526; forbidden band 526..900 untouched) ----
TOKBASE = 64          # 64..95: token words, one per token (B2 48-bit layout)
LITBASE = 100         # 100..103: literal pool, float = 10 * printed value
C_TOK, C_TK, C_SUB, C_PAY = 104, 105, 106, 107
C_SPC, C_W, C_D, C_VIDX, C_VAL = 108, 109, 110, 111, 112
K_BASE, K_ONE = 113, 114
K_MTK, K_MSUB, K_MPAY = 115, 116, 117
K_SR42, K_SR36, K_SR8, K_255, K_ZERO = 118, 119, 120, 121, 122
K_TK10, K_TK2, K_TK11, K_TK12, K_TK13 = 123, 124, 125, 126, 127
K_SUB30, K_SUB31, K_SUB34, K_SUB37 = 128, 129, 130, 131
K_GOSTA, K_GOSTB, K_PRINT_BIAS = 132, 133, 134
K_WMASK0, K_WMASK1, K_WMASK2 = 135, 136, 137
K_CLEARM0, K_CLEARM1 = 138, 139
K_SPACEM0, K_SPACEM1 = 140, 141


def tok(tk, sub=0, pos=0, pay=0):
    """B2 token word: TK:6(b47..42) SUB:6(b41..36) POS:12(b35..24) PAY:24(b23..0)."""
    return ((tk & 0x3f) << 42) | ((sub & 0x3f) << 36) | ((pos & 0xfff) << 24) | (pay & 0xffffff)


# TK codes (B2 Table 2.2): 1 LIT, 2 ID, 8 EQ, 10 KW, 11 EOL, 12 EOF, 13 FD
# KW SUB: 30 PROGRAM, 31 REAL, 34 PRINT, 37 END
# FD SUB=1 (F), PAY = w<<8 | d
def fixture(lit_pay=0, reorder=False):
    if reorder:
        # PRINT first: variable still 0.0 at that point -> different output
        return [
            tok(10, 34),                       # PRINT
            tok(13, 1, 0, (4 << 8) | 2),       # F4.2
            tok(2, 0, 0, 1),                   # X
            tok(11),                           # EOL
            tok(10, 31),                       # REAL
            tok(2, 0, 0, 1),                   # X
            tok(11),                           # EOL
            tok(2, 0, 0, 1),                   # X =
            tok(8),                            # =
            tok(1, 0, 0, 0),                   # LIT index 0
            tok(11),                           # EOL
            tok(10, 37),                       # END
        ]
    return [
        tok(10, 30),                           # PROGRAM
        tok(2),                                # (name, consumed/ignored)
        tok(10, 31),                           # REAL
        tok(2, 0, 0, 1),                       # X (VIDX=1)
        tok(11),                               # EOL
        tok(2, 0, 0, 1),                       # X =
        tok(8),                                # =
        tok(1, 0, 0, lit_pay),                 # LIT index (0 -> 12.34, 1 -> 56.78)
        tok(11),                               # EOL
        tok(10, 34),                           # PRINT
        tok(13, 1, 0, (4 << 8) | 2),           # F4.2
        tok(2, 0, 0, 1),                       # X
        tok(11),                               # EOL
        tok(10, 37),                           # END
    ]


# ----------------------------- N+2 dispatcher -----------------------------
def build_dispatch(conv_ram):
    c = C6.Code()
    H = c.hw
    labels = {}
    branches = []          # (hw_index, label, op)

    def mark(name):
        if len(H) % 2:
            H.append(DUMMY)
        labels[name] = len(H)

    def br(op, name):
        i = len(H)
        c.L(op, 0, reg=7)
        branches.append((i, name, op))
        return i

    def rearm():
        # converter clobbers base registers; reload from low-RAM HALF (= 0o20000)
        c.Z(0o10, 'HALF')
        c.L(ATI, 12)                  # M[12] = 0o20000 (C() base)
        c.Z(0o10, 'HALF')
        c.L(ATI, 7)                   # M[7]  = 0o20000 (short branch base)

    def fetch():
        c.C(0o10, C_SPC); c.L(ATI, 6)          # M[6] = statement pointer
        c.E(long_(0o220, 0o20000))             # arm M20 for next xta only
        c.L(0o10, 0o1637 + TOKBASE, reg=6)     # ACC = token word
        c.C(ATX, C_TOK)
        c.C(0o10, C_SPC); c.C(ARX, K_ONE); c.C(ATX, C_SPC)   # SPC++

    def extract():
        c.C(0o10, C_TOK); c.C(AAX, K_MTK); c.C(ASX, K_SR42); c.C(ATX, C_TK)
        c.C(0o10, C_TOK); c.C(AAX, K_MSUB); c.C(ASX, K_SR36); c.C(ATX, C_SUB)
        c.C(0o10, C_TOK); c.C(AAX, K_MPAY);               c.C(ATX, C_PAY)

    # ---- interpreted statement loop ----
    mark('LOOP')
    rearm()
    fetch()
    extract()
    c.C(0o10, C_TK); c.C(AEX, K_TK11); br(UZA, 'LOOP')    # EOL: just advance
    c.C(0o10, C_TK); c.C(AEX, K_TK12); br(UZA, 'DONE')    # EOF
    c.C(0o10, C_TK); c.C(AEX, K_TK10); br(UZA, 'KW')      # keyword statement
    c.C(0o10, C_TK); c.C(AEX, K_TK2);  br(UZA, 'ASSIGN')  # ID -> assignment
    br(UJ, 'LOOP')                                        # unknown: skip

    mark('KW')
    c.C(0o10, C_SUB); c.C(AEX, K_SUB30); br(UZA, 'S_PROGRAM')
    c.C(0o10, C_SUB); c.C(AEX, K_SUB31); br(UZA, 'S_REAL')
    c.C(0o10, C_SUB); c.C(AEX, K_SUB34); br(UZA, 'S_PRINT')
    c.C(0o10, C_SUB); c.C(AEX, K_SUB37); br(UZA, 'DONE')   # END
    br(UJ, 'LOOP')

    mark('S_PROGRAM')
    fetch()                                   # consume the program name token
    br(UJ, 'LOOP')

    mark('S_REAL')
    mark('REAL_L')
    fetch()
    extract()
    c.C(0o10, C_TK); c.C(AEX, K_TK11); br(UZA, 'LOOP')    # EOL ends REAL
    c.C(0o10, C_PAY); c.L(ATI, 6)             # M[6] = VIDX
    c.C(0o10, K_ZERO)                          # ACC = 0.0
    c.E(long_(0o220, 0o20000))
    c.L(ATX, 0o1637 + 32, reg=6)              # value word = 0.0
    br(UJ, 'REAL_L')

    mark('ASSIGN')                             # C_PAY = VIDX of the ID token
    c.C(0o10, C_PAY); c.C(ATX, C_VIDX)
    fetch()                                    # EQ token (ignored)
    fetch()                                    # LIT token
    extract()
    c.C(0o10, C_PAY); c.L(ATI, 6)             # M[6] = literal index
    c.E(long_(0o220, 0o20000))
    c.L(0o10, 0o1637 + LITBASE, reg=6); c.C(ATX, C_VAL)
    c.C(0o10, C_VIDX); c.L(ATI, 6)            # M[6] = VIDX
    c.C(0o10, C_VAL)
    c.E(long_(0o220, 0o20000))
    c.L(ATX, 0o1637 + 32, reg=6)              # symbol value = literal
    br(UJ, 'LOOP')

    mark('S_PRINT')
    fetch()                                    # FD token
    extract()
    c.C(0o10, C_PAY); c.C(ASX, K_SR8); c.C(ATX, C_W)   # w = PAY >> 8
    c.C(0o10, C_PAY); c.C(AAX, K_255); c.C(ATX, C_D)   # d = PAY & 255
    fetch()                                    # ID token
    extract()
    c.C(0o10, C_PAY); c.L(ATI, 6)             # M[6] = VIDX
    c.E(long_(0o220, 0o20000))
    c.L(0o10, 0o1637 + 32, reg=6); c.Z(ATX, 'EST')      # EST = value (10*P)
    # one dispatcher word: display bias (patch target)
    c.Z(0o10, 'EST'); c.C(FADD, K_PRINT_BIAS); c.Z(ATX, 'EST')
    # seed GOST print words, then apply the proven docs/113 w/d masks
    c.C(0o10, K_GOSTA); c.L(ATX, 0o2006)
    c.C(0o10, K_GOSTB); c.L(ATX, 0o2007)
    c.C(0o10, C_W); c.L(ATI, 6)               # M[6] = w (2,3,4)
    c.E(long_(0o220, 0o20000))
    c.L(0o10, 0o1637 + K_WMASK0 - 2, reg=6)
    c.L(AEX, 0o2006); c.L(ATX, 0o2006)
    c.C(0o10, C_D); c.L(ATI, 6)               # M[6] = d (1,2)
    c.E(long_(0o220, 0o20000))
    c.L(0o10, 0o1637 + K_CLEARM0 - 1, reg=6)
    c.L(AAX, 0o2007); c.L(ATX, 0o2007)
    c.E(long_(0o220, 0o20000))
    c.L(0o10, 0o1637 + K_SPACEM0 - 1, reg=6)
    c.L(ARX, 0o2007); c.L(ATX, 0o2007)
    c.vjmo(conv_ram)                           # verbatim converter -> *64 2004
    rearm()                                    # converter clobbers base regs
    br(UJ, 'LOOP')

    mark('DONE')
    c.E(UJ15)                                  # LONG uj 0(15) -> resident 0o1764

    # resolve deferred short branches (reg7 base = 0o20000)
    for i, name, op in branches:
        idx = labels[name]
        assert idx % 2 == 0, (name, idx)
        ram = CODE_RAM + idx // 2
        H[i] = short(op, (ram - 0o20000) & 0o7777, reg=7)
    if len(H) % 2:
        H.append(DUMMY)
    return c, labels


def build(case, lit_pay=0, reorder=False, bias=0.0):
    src = WS / 'images/2048_base'
    dst = WS / 'images' / f'2048_{case}'
    shutil.copy2(src, dst)

    body = rz(str(dst), N + 1)
    body[0o11] = word(long_(0o300, CODE_RAM, reg=0), 0)   # contour entry
    body[0o27] = int.from_bytes(bytes([2, 1, 15, 15, 0, 0]), 'big')
    body[0o30] = int.from_bytes(bytes([0, 0, 14, 0, 0, 15]), 'big')
    body[0o31] = int.from_bytes(bytes([15, 3, 0, 0, 0, 14]), 'big')
    body[0o32] = int.from_bytes(bytes([0, 0, 0o231, 15, 15, 15]), 'big')
    for n, value in C6.vals().items():
        body[0o110 + FS.CELLS.index(n)] = value & MASK
    wz(str(dst), N + 1, body)

    n3_hw, floor_ram, conv_len, floor_len = C6.build_n3()
    wz(str(dst), Z3, C6.asm_words(n3_hw))

    n2, labels = build_dispatch(CONV_RAM0)
    z2 = rz(str(dst), N2)                     # preserve 526..900 overlay
    # symbol table: name at VIDX, value at 32+VIDX
    z2[1] = C6.C2.text_word('X       ') & MASK
    z2[33] = f32(0.0)
    # literal pool: value = 10 * printed value (converter divides by 10)
    literals = [f32(123.4), f32(567.8), f32(345.0), f32(901.0)]
    for i, v in enumerate(literals):
        z2[LITBASE + i] = v & MASK
    # token fixture (the executed program at this milestone)
    toks = fixture(lit_pay=lit_pay, reorder=reorder)
    for i, t in enumerate(toks):
        z2[TOKBASE + i] = t & MASK

    wm, cm, sm = C7.width_tables()
    consts = {
        K_BASE: 0o20000, K_ONE: 1,
        K_MTK: 0o7700000000000000, K_MSUB: 0o0077000000000000,
        K_MPAY: 0o0000000077777777,
        K_SR42: (64 + 42) << 41, K_SR36: (64 + 36) << 41,
        K_SR8: (64 + 8) << 41, K_255: 0o377, K_ZERO: 0,
        K_TK10: 10, K_TK2: 2, K_TK11: 11, K_TK12: 12, K_TK13: 13,
        K_SUB30: 30, K_SUB31: 31, K_SUB34: 34, K_SUB37: 37,
        K_GOSTA: body[0o27], K_GOSTB: body[0o30],
        K_PRINT_BIAS: f32(bias),
    }
    for off, v in zip(range(K_WMASK0, K_WMASK0 + 3), wm):
        consts[off] = v
    for off, v in zip(range(K_CLEARM0, K_CLEARM0 + 2), cm):
        consts[off] = v
    for off, v in zip(range(K_SPACEM0, K_SPACEM0 + 2), sm):
        consts[off] = v
    for off, v in consts.items():
        z2[off] = v & MASK

    hw = n2.hw
    for i in range(len(hw) // 2):
        z2[CODE_OFF + i] = word(hw[2 * i], hw[2 * i + 1])
    if len(hw) % 2:
        z2[CODE_OFF + len(hw) // 2] = word(hw[-1], DUMMY)
    wz(str(dst), N2, z2)

    sha = hashlib.sha256(dst.read_bytes()).hexdigest()
    n2used = max(CODE_OFF + (len(hw) + 1) // 2, TOKBASE + len(toks),
                 LITBASE + 4, K_SPACEM1 + 1) + 1
    print(f'case={case} sha={sha} N3={len(n3_hw)//2}/{MAX_WORDS}w '
          f'conv={conv_len}hw floor={floor_len}hw N2code={len(hw)}hw '
          f'({(len(hw)+1)//2} words) N2used={n2used}/649 ntok={len(toks)} '
          f'lit_pay={lit_pay} reorder={reorder} bias={bias} '
          f'CODE_RAM={CODE_RAM:06o} labels={len(labels)}')
    return dst, sha, n2used, len(n3_hw) // 2


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--build', required=True)
    ap.add_argument('--lit-pay', type=int, default=0)
    ap.add_argument('--reorder', action='store_true')
    ap.add_argument('--bias', type=float, default=0.0)
    a = ap.parse_args()
    build(a.build, lit_pay=a.lit_pay, reorder=a.reorder, bias=a.bias)
