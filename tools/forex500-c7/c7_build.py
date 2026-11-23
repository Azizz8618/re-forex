#!/usr/bin/env python3
"""C7: ONE integrated contour -- shared scanner/dispatch over all proven IR features.

Architecture (the C2b/C6 displacement principle, reused verbatim):
  * Zone N+3 = the canonical docs/105 GOST converter + sign block + both
    reclaims + shared floor_int VJM, byte-for-byte verbatim (40 words, 80 hw).
    The converter is the ONLY hot path kept in N+3.
  * Zone N+2 = the 649 proven-free words. ALL feature front-ends live here:
    one shared marker scanner, one TK jump table, LIT/VARIABLE readers (docs
    104/109/114), a TO dispatch for binary ops (C3) and intrinsics (C4), a
    FORMAT-width layout selector (C5) and the DO countdown fixture (C6).
    Offsets 526..900 (load-bearing overlay) are NEVER written.

Deck: six 777005 records (one per feature).  All six IR tokens drive printed
values through the single verbatim converter; the host stores no result digit.

Copies only: no repo/live-disk/tmux-0/C changes.  C dispak is an oracle only.
"""
import argparse
import hashlib
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import c6_build as C6
from build_e2e import rz, wz, short, long_, word, f32, MASK, N, Z3, MAX_WORDS

WS = HERE.parent

# ---- reuse proven N+3 converter and helpers verbatim ----
build_n3 = C6.build_n3
asm_words = C6.asm_words
vals = C6.vals
vjm_imm = C6.vjm_imm
ret_imm = C6.ret_imm
Code = C6.Code

N2_RAM0 = 0o21637
N2_CODE_OFF = 200
N2_CODE_RAM = N2_RAM0 + N2_CODE_OFF
CONV_RAM0 = 0o30114
ADR_BASE = N2_RAM0 - 0o20000            # 0o1637

# opcode aliases (same values as c6_build / c4_build)
ATX, AAX, AEX, ARX, ASX = 0o00, 0o11, 0o12, 0o13, 0o26
DIV, MUL, FADD = 0o16, 0o17, 0o04
XSUB = 0o06                             # C3 reverse-subtract opcode
FSUB = 0o05                             # C4 MOD subtract opcode
AVX, AOX, ATI, EPLUSX, ITA = 0o14, 0o15, 0o40, 0o24, 0o42
UZA, VJM_OP, UTC, UJ = 0o260, 0o310, 0o220, 0o300
DUMMY = C6.FB.DUMMY
UJ15 = C6.FB.UJ15
LINK_OUT = 9

# ---- N+2 cell map (all offsets <= 199, well below the 526..900 exclusion) ----
K_BASE, K_CBASE, K_ONE, K_FOUR = 110, 111, 112, 113
K_MARK, K_SR24, K_28, K_SP7 = 114, 115, 116, 117
K_SHL42, K_NEGONE, K_HUNDRED, K_PTR = 118, 119, 120, 121
K_GOSTA, K_GOSTB = 122, 123
K_ZERO, K_DECR, K_DO_KIND = 124, 125, 126
K_SR40 = 127                            # (64+40)<<41 : TO byte (byte 0) -> low byte
K_NREC = 128                            # number of IR records to process (6)
L_BOUND, L_STEP, L_CNT, L_SUM, L_VAL = 130, 131, 132, 133, 134
# arithmetic operands (pre-scaled per docs/111 C3)
AR_A10, AR_B10, AR_A1, AR_B1 = 140, 141, 142, 143
# TO dispatch table, 7 words: TO=1..7 -> LONG UJ handler   (RAM 0o21637+150..156)
OT_BASE = 150
# intrinsic mechanism constants (docs/112 C4, re-addressed to N+2)
IX_ABS, IX_SQRT, IX_MOD, IX_YMOD = 160, 161, 162, 163
IX_HALF, IX_Q, IX_MASKC, IX_AIQ = 164, 165, 166, 167
IX_PROD, IX_T, IX_SIGN, IX_EMASK = 168, 169, 170, 171
IX_C105, IX_M40, IX_CWL16, IX_EXALL, IX_CW = 172, 173, 174, 175, 176
# width layout masks (docs/113 C5)
W_MASK_BASE, W_CLEAR_BASE, W_SPACE_BASE, W_OPERAND = 180, 183, 185, 187
# TK dispatch table, 6 words: TK=1..6 -> LONG UJ handler   (RAM 0o21637+190..195)
TK_BASE = 190


def adr(off):
    return ADR_BASE + off


def long_uj(addr, reg=0):
    return long_(UJ, addr, reg=reg)


# ----------------------------- integrated N+2 code -----------------------------
def build_n2(floor_ram, conv_ram):
    c = Code()
    H = c.hw
    labels = {}

    def rearm():
        # converter clobbers base registers, so re-arm every step
        c.Z(0o10, 'HALF')               # HALF (low RAM) = 0o20000
        c.L(ATI, 12)                    # M[12] = N+2 base
        c.C(0o10, K_BASE)
        c.L(ATI, 7)                     # M[7]  = short-branch base 0o20000
        c.C(0o10, K_PTR)
        c.L(ATI, 10)                    # M[10] = card pointer

    def mark(name):
        if len(H) % 2:
            H.append(DUMMY)
        labels[name] = len(H)

    # ---- shared scan loop (re-arm registers every iteration: the converter
    #      clobbers the base registers, so pointer persistence lives in K_PTR) ----
    mark('LOOP')
    rearm()
    mark('SCAN_LOOP')
    c.L(0o10, 0o4012, 10)               # card word at M[10]+0o4012
    c.C(AEX, K_MARK)
    labels['SCAN_UZA'] = len(H)
    c.L(UZA, 0, reg=7)                  # patched: marker -> FOUND
    c.L(ITA, 10)                        # ACC = M[10] (card pointer), NOT xta 0(10)
    c.C(ARX, K_ONE)
    c.L(ATI, 10)
    labels['SCAN_UJ'] = len(H)
    c.L(UJ, 0, reg=7)                   # patched: -> SCAN_LOOP
    mark('FOUND')
    # persist the pointer AT the found marker +1 (skip this marker next time);
    # the scan's local M[10] increments must not be lost across the converter.
    c.L(ITA, 10)
    c.C(ARX, K_ONE)
    c.C(ATX, K_PTR)

    # ---- decode TK at W+1 byte4 -> M[6] ----
    c.L(0o10, 0o4013, 10)
    c.Z(ASX, 'SR8')
    c.Z(AAX, 'M8')
    c.Z(ARX, 'PD0')
    c.Z(AAX, 'M8')
    c.L(ATI, 6)                         # M[6] = TK

    # ---- reseed GOST print seeds before every record (width handler edits them) ----
    c.C(0o10, K_GOSTA); c.L(ATX, 0o2006)
    c.C(0o10, K_GOSTB); c.L(ATX, 0o2007)

    # ---- dispatch on TK via the N+2 jump table ----
    labels['TK_UJ'] = len(H)
    c.E(long_(UJ, N2_RAM0 + TK_BASE - 1, reg=6))  # LONG UJ: PC=(RAM base-1)+TK

    mark('HANDLER_RETURN')
    c.vjmo(conv_ram)                    # verbatim converter -> *64 2004

    # ---- record counter / loop (pointer already persisted at FOUND) ----
    c.C(0o10, K_NREC); c.C(ARX, K_NEGONE); c.C(ATX, K_NREC)  # one's-complement -1
    labels['END_UZA'] = len(H)
    c.L(UZA, 0, reg=7)                  # patched: all records done -> DONE
    labels['END_UJ'] = len(H)
    c.L(UJ, 0, reg=7)                   # patched: -> LOOP
    mark('DONE')
    c.E(UJ15)

    # ---------------------------- TK=1 : LIT reader ----------------------------
    mark('H_LIT')
    c.L(0o10, 0o4014, 10)
    c.Z(ATX, 'CARD')
    c.C(ASX, K_SR24); c.Z(AAX, 'M8'); c.Z(ARX, 'NEG31')
    c.L(ATI, 6)
    c.Z(0o10, 'CARD'); c.Z(ASX, 'SR16'); c.Z(AAX, 'M8'); c.Z(ARX, 'NEG31')
    c.L(ARX, C6.C2.FS.LO['T0'], reg=6)
    c.Z(EPLUSX, 'EMASK'); c.Z(EPLUSX, 'C105'); c.Z(ATX, 'NUM')
    c.Z(0o10, 'CARD'); c.Z(ASX, 'SR8'); c.Z(AAX, 'M8'); c.Z(ARX, 'NEG31')
    c.L(ATI, 6)
    c.Z(0o10, 'CARD'); c.Z(AAX, 'M8'); c.Z(ARX, 'NEG31')
    c.L(ARX, C6.C2.FS.LO['T0'], reg=6)
    c.Z(EPLUSX, 'EMASK'); c.Z(EPLUSX, 'C105'); c.Z(ATX, 'CARD')
    c.Z(0o10, 'NUM'); c.C(MUL, K_HUNDRED)
    c.Z(FADD, 'CARD'); c.Z(ATX, 'NUM')
    c.Z(DIV, 'TEN'); c.Z(ATX, 'EST')
    c.E(long_uj(conv_ram))              # placeholder -> HANDLER_RETURN, patched below
    LIT_RET = len(H) - 1

    # -------------------------- TK=2 : VARIABLE reader --------------------------
    mark('H_VAR')
    c.L(0o10, 0o4014, 10)
    c.C(ASX, K_SR24); c.Z(AAX, 'M8'); c.Z(ARX, 'PD0'); c.Z(AAX, 'M8')
    c.L(ATI, 6)                         # tens
    c.L(0o10, 0o4014, 10)
    c.Z(ASX, 'SR16'); c.Z(AAX, 'M8'); c.Z(ARX, 'PD0'); c.Z(AAX, 'M8')
    c.L(ARX, C6.C2.FS.LO['T0'], reg=6)
    c.L(ATI, 6)                         # VIDX
    c.Z(ATX, 'CARD')
    c.C(ARX, K_28); c.C(ASX, K_SHL42); c.C(ARX, K_SP7)
    c.Z(ATX, 'NUM')                     # expected TEXT name
    c.E(long_(UTC, 0o20000))
    c.L(0o10, adr(0), reg=6)            # actual name at N+2[VIDX]
    c.Z(AEX, 'NUM')
    labels['VAR_UZA'] = len(H)
    c.L(UZA, 0, reg=7)                  # patched: match -> OK
    c.C(0o10, K_ZERO); c.Z(ATX, 'EST')  # mismatch: EST=0
    labels['VAR_UJ'] = len(H)
    c.L(UJ, 0, reg=7)                   # patched: -> end
    mark('VAR_OK')
    c.E(long_(UTC, 0o20000))
    c.L(0o10, adr(32), reg=6)           # value at N+2[32+VIDX]
    c.Z(DIV, 'TEN'); c.Z(ATX, 'EST')
    mark('VAR_END')
    c.E(long_uj(conv_ram))
    VAR_RET = len(H) - 1

    # --------------- TK=3 : binary op / intrinsic, decoded by TO ----------------
    mark('H_OP')
    c.L(0o10, 0o4014, 10)               # TO at card byte 0
    c.C(ASX, K_SR40); c.Z(AAX, 'M8'); c.Z(ARX, 'NEG31')
    c.L(ATI, 6)                         # M[6] = TO (1..7)
    c.E(long_(UJ, N2_RAM0 + OT_BASE - 1, reg=6))  # LONG UJ: PC=(RAM base-1)+TO

    # TO=1 ADD
    mark('OP_ADD')
    c.C(0o10, AR_A10); c.C(FADD, AR_B10); c.Z(ATX, 'EST')
    c.E(long_uj(conv_ram)); RET_ADD = len(H) - 1
    # TO=2 SUB (magnitude-only reverse subtract, docs/111)
    mark('OP_SUB')
    c.C(0o10, AR_A10); c.C(XSUB, AR_B10); c.Z(ATX, 'EST')
    c.E(long_uj(conv_ram)); RET_SUB = len(H) - 1
    # TO=3 MUL
    mark('OP_MUL')
    c.C(0o10, AR_A10); c.C(MUL, AR_B1); c.Z(ATX, 'EST')
    c.E(long_uj(conv_ram)); RET_MUL = len(H) - 1
    # TO=4 DIV
    mark('OP_DIV')
    c.C(0o10, AR_A10); c.C(DIV, AR_B1); c.Z(ATX, 'EST')
    c.E(long_uj(conv_ram)); RET_DIV = len(H) - 1
    # TO=5 ABS (hardware sign change)
    mark('OP_ABS')
    c.C(0o10, IX_ABS); c.C(AVX, IX_SIGN); c.Z(ATX, 'EST')
    c.E(long_uj(conv_ram)); RET_ABS = len(H) - 1
    # TO=6 SQRT (Newton x4)
    mark('OP_SQRT')
    c.C(0o10, IX_SQRT); c.C(ATX, IX_T)
    for _ in range(4):
        c.C(0o10, IX_SQRT); c.C(DIV, IX_T)
        c.C(FADD, IX_T); c.C(MUL, IX_HALF)
        c.C(ATX, IX_T)
    c.C(0o10, IX_T); c.Z(ATX, 'EST')
    c.E(long_uj(conv_ram)); RET_SQRT = len(H) - 1
    # TO=7 MOD (X - Y*INT(X/Y) via bitwise mantissa mask)
    mark('OP_MOD')
    c.C(0o10, IX_MOD); c.C(DIV, IX_YMOD); c.C(ATX, IX_Q)
    c.C(0o10, IX_M40); c.C(ASX, IX_Q); c.C(AEX, IX_M40)
    c.C(AOX, IX_EXALL); c.C(ATX, IX_MASKC)
    c.C(0o10, IX_Q); c.C(AAX, IX_MASKC); c.C(ATX, IX_AIQ)
    c.C(0o10, IX_YMOD); c.C(MUL, IX_AIQ); c.C(ATX, IX_PROD)
    c.C(0o10, IX_MOD); c.C(FSUB, IX_PROD); c.Z(ATX, 'EST')
    c.E(long_uj(conv_ram)); RET_MOD = len(H) - 1

    # ---------------------- TK=5 : FORMAT width (fixture) ----------------------
    mark('H_WIDTH')
    c.L(0o10, 0o4014, 10)
    c.Z(ATX, 'CARD')
    c.C(ASX, K_SR40); c.Z(AAX, 'M8'); c.Z(ARX, 'NEG31')
    c.L(ATI, 6)                         # M[6] = w
    c.Z(0o10, 'CARD')
    c.C(ASX, K_SR24); c.Z(AAX, 'M8'); c.Z(ARX, 'NEG31')
    c.L(ATI, 5)                         # M[5] = d (NOT M[7] = branch base)
    # GOST word A: XOR selected leading-zero padding mask
    c.E(long_(UTC, 0o20000)); c.L(0o10, adr(W_MASK_BASE) - 2, reg=6)
    c.L(AEX, 0o2006); c.L(ATX, 0o2006)
    # GOST word B: clear the F2 byte when d=1
    c.E(long_(UTC, 0o20000)); c.L(0o10, adr(W_CLEAR_BASE) - 1, reg=5)
    c.L(AAX, 0o2007); c.L(ATX, 0o2007)
    # GOST word B: add GOST space at the cleared byte
    c.E(long_(UTC, 0o20000)); c.L(0o10, adr(W_SPACE_BASE) - 1, reg=5)
    c.L(ARX, 0o2007); c.L(ATX, 0o2007)
    # feed pre-seeded operand into the verbatim converter
    c.E(long_(UTC, 0o20000)); c.L(0o10, adr(W_OPERAND)); c.Z(ATX, 'EST')
    c.E(long_uj(conv_ram)); RET_WIDTH = len(H) - 1

    # ------------------------- TK=6 : DO loop (fixture) -------------------------
    mark('H_DO')
    # bound = two-digit TA at W+2 bytes 2,3
    c.L(0o10, 0o4014, 10)
    c.C(ASX, K_SR24); c.Z(AAX, 'M8'); c.Z(ARX, 'PD0'); c.Z(AAX, 'M8')
    c.L(ATI, 6)
    c.L(0o10, 0o4014, 10)
    c.Z(ASX, 'SR16'); c.Z(AAX, 'M8'); c.Z(ARX, 'PD0'); c.Z(AAX, 'M8')
    c.L(ARX, C6.C2.FS.LO['T0'], reg=6)
    c.C(ATX, L_BOUND)
    # step = one-digit TB at W+2 byte5
    c.L(0o10, 0o4014, 10)
    c.Z(AAX, 'M8'); c.Z(ARX, 'PD0'); c.Z(AAX, 'M8')
    c.C(ATX, L_STEP)
    # init CNT=bound, SUM=0
    c.C(0o10, L_BOUND); c.C(ATX, L_CNT)
    c.C(0o10, K_ZERO); c.C(ATX, L_SUM)
    mark('DO_LOOP')
    c.C(0o10, L_SUM); c.C(FADD, L_VAL); c.C(ATX, L_SUM)
    c.C(0o10, L_CNT); c.C(ARX, K_DECR); c.C(ATX, L_CNT)
    labels['DO_UZA'] = len(H)
    c.L(UZA, 0, reg=7)                  # patched: CNT==0 -> DO_DONE
    labels['DO_UJ'] = len(H)
    c.L(UJ, 0, reg=7)                   # patched: -> DO_LOOP
    mark('DO_DONE')
    c.C(0o10, L_SUM); c.Z(ATX, 'EST')
    c.E(long_uj(conv_ram)); RET_DO = len(H) - 1

    if len(H) % 2:
        H.append(DUMMY)

    # ---- resolve labels ----
    def lab(name):
        idx = labels[name]
        assert idx % 2 == 0, (name, idx)
        return N2_CODE_RAM + idx // 2

    def retlab(idx):
        # a placeholder LONG UJ at halfword index idx; replace with a jump to
        # the HANDLER_RETURN word address
        return N2_CODE_RAM + labels['HANDLER_RETURN'] // 2

    # scan / loop branches
    H[labels['SCAN_UZA']] = short(UZA, 0, reg=7) | ((lab('FOUND') - 0o20000) & 0o7777)
    H[labels['SCAN_UJ']] = short(UJ, 0, reg=7) | ((lab('SCAN_LOOP') - 0o20000) & 0o7777)
    H[labels['END_UZA']] = short(UZA, 0, reg=7) | ((lab('DONE') - 0o20000) & 0o7777)
    H[labels['END_UJ']] = short(UJ, 0, reg=7) | ((lab('LOOP') - 0o20000) & 0o7777)
    H[labels['VAR_UZA']] = short(UZA, 0, reg=7) | ((lab('VAR_OK') - 0o20000) & 0o7777)
    H[labels['VAR_UJ']] = short(UJ, 0, reg=7) | ((lab('VAR_END') - 0o20000) & 0o7777)
    H[labels['DO_UZA']] = short(UZA, 0, reg=7) | ((lab('DO_DONE') - 0o20000) & 0o7777)
    H[labels['DO_UJ']] = short(UJ, 0, reg=7) | ((lab('DO_LOOP') - 0o20000) & 0o7777)
    # all handler "return to common print" placeholders
    for idx in (LIT_RET, VAR_RET, RET_ADD, RET_SUB, RET_MUL, RET_DIV,
                RET_ABS, RET_SQRT, RET_MOD, RET_WIDTH, RET_DO):
        H[idx] = long_uj(retlab(idx)) & 0xffffff
    # TK dispatch table (entries patched in build() once z2 layout is known):
    #   table word = LONG UJ <handler RAM address>
    # OP dispatch table likewise.
    for tk, handler in ((1, 'H_LIT'), (2, 'H_VAR'), (3, 'H_OP'),
                        (4, None), (5, 'H_WIDTH'), (6, 'H_DO')):
        pass  # built as data in build()
    c.tk_handlers = {1: lab('H_LIT'), 2: lab('H_VAR'), 3: lab('H_OP'),
                     5: lab('H_WIDTH'), 6: lab('H_DO')}
    c.op_handlers = {1: lab('OP_ADD'), 2: lab('OP_SUB'), 3: lab('OP_MUL'),
                     4: lab('OP_DIV'), 5: lab('OP_ABS'), 6: lab('OP_SQRT'),
                     7: lab('OP_MOD')}
    return c


# ----------------------------- image assembly -----------------------------
GOST_SPACE = 0o17


def gost_char(ci, v):
    return (v & 0o77) << (8 * (5 - ci))


def width_tables():
    wm = [gost_char(4, GOST_SPACE) | gost_char(5, GOST_SPACE),
          gost_char(4, GOST_SPACE), 0]
    allones = sum(0o77 << (8 * (5 - j)) for j in range(6))
    cm = [allones ^ gost_char(4, 0o77), allones]
    sm = [gost_char(4, GOST_SPACE), 0]
    return wm, cm, sm


def build(case, patch_value=None, patch_op=None, nrec=6):
    src = WS / 'images/2048_base'
    dst = WS / 'images' / f'2048_{case}'
    shutil.copy2(src, dst)
    body = rz(str(dst), N + 1)
    # entry: long uj to N+2 code (verbatim C6 mechanism)
    body[0o11] = word(long_(0o300, N2_CODE_RAM, reg=0), 0)
    body[0o27] = int.from_bytes(bytes([2, 1, 15, 15, 0, 0]), 'big')
    body[0o30] = int.from_bytes(bytes([0, 0, 14, 0, 0, 15]), 'big')
    body[0o31] = int.from_bytes(bytes([15, 3, 0, 0, 0, 14]), 'big')
    body[0o32] = int.from_bytes(bytes([0, 0, 0o231, 15, 15, 15]), 'big')
    for n, value in vals().items():
        body[0o110 + C6.C2.FS.CELLS.index(n)] = value & MASK
    wz(str(dst), N + 1, body)

    n3_hw, floor_ram, conv_len, floor_len = build_n3()
    wz(str(dst), Z3, asm_words(n3_hw))

    n2 = build_n2(floor_ram, CONV_RAM0)
    z2 = rz(str(dst), C6.N2)             # preserve load-bearing overlay 526..900
    # C2b symbol table (name at VIDX, value at 32+VIDX)
    symbols = {1: ('X       ', f32(7890.0)),
               2: ('Y       ', f32(1234.0)),
               12: ('H       ', f32(patch_value if patch_value is not None else 5678.0)),
               13: ('I       ', f32(9012.0))}
    for vidx, (nm, val) in symbols.items():
        z2[vidx] = C6.C2.text_word(nm) & MASK
        z2[32 + vidx] = val & MASK
    wm, cm, sm = width_tables()
    consts = {
        K_BASE: 0o20000, K_CBASE: 0o60000, K_ONE: 1, K_FOUR: 4,
        K_MARK: 0x823737373030, K_SR24: (64 + 24) << 41,
        K_28: 28, K_SP7: 0, K_SHL42: (64 - 42) << 41,
        K_NEGONE: MASK ^ 1, K_HUNDRED: f32(100.0), K_PTR: 0o60000,
        K_GOSTA: body[0o27], K_GOSTB: body[0o30],
        K_ZERO: 0, K_DECR: MASK ^ 1, K_DO_KIND: 6,
        K_SR40: (64 + 40) << 41, K_NREC: nrec,
        L_BOUND: 0, L_STEP: 0, L_CNT: 0, L_SUM: 0, L_VAL: f32(200.0),
        # arithmetic (a=1.5, b=2.5, pre-scaled per docs/111)
        AR_A10: f32(15.0), AR_B10: f32(25.0),
        AR_A1: f32(1.5), AR_B1: f32(2.5),
        # intrinsics (mechanism constants, no result digit)
        IX_ABS: C4_neg(30.0), IX_SQRT: f32(16.0),
        IX_MOD: f32(9.0), IX_YMOD: f32(4.0), IX_HALF: f32(0.5),
        IX_SIGN: 1 << 40, IX_EMASK: 0o177 << 41,
        IX_C105: 0o151 << 41, IX_M40: 0xFFFFFFFFFF,
        IX_CWL16: 0o60 << 41,
        IX_EXALL: (0o177 << 41) | (1 << 40),
        # width operand + masks
        W_OPERAND: f32(345.0),
    }
    for offset, value in zip(range(W_MASK_BASE, W_MASK_BASE + 3), wm):
        consts[offset] = value
    for offset, value in zip(range(W_CLEAR_BASE, W_CLEAR_BASE + 2), cm):
        consts[offset] = value
    for offset, value in zip(range(W_SPACE_BASE, W_SPACE_BASE + 2), sm):
        consts[offset] = value
    # TK jump table: each word = LONG UJ <handler RAM addr>
    for tk, handler in n2.tk_handlers.items():
        consts[TK_BASE + tk - 1] = word(long_uj(handler), DUMMY)
    # TO jump table
    for to, handler in n2.op_handlers.items():
        consts[OT_BASE + to - 1] = word(long_uj(handler), DUMMY)
    for k, v in consts.items():
        z2[k] = v & MASK

    n2hw = n2.hw
    for i in range(len(n2hw) // 2):
        z2[N2_CODE_OFF + i] = word(n2hw[2 * i], n2hw[2 * i + 1])
    if len(n2hw) % 2:
        z2[N2_CODE_OFF + len(n2hw) // 2] = word(n2hw[-1], DUMMY)
    wz(str(dst), C6.N2, z2)
    sha = hashlib.sha256(dst.read_bytes()).hexdigest()
    n2used = N2_CODE_OFF + (len(n2hw) + 1) // 2
    print(f'case={case} sha={sha} N3={len(n3_hw)//2}/{MAX_WORDS}w '
          f'conv={conv_len}hw floor={floor_len}hw N2code={len(n2hw)}hw '
          f'N2used~{n2used}/649 nrec={nrec}')
    return dst, sha


def C4_neg(value):
    """Valid negative BESM-6 float (verbatim from docs/112 C4)."""
    B42, B41 = (1 << 42) - 1, (1 << 41) - 1
    w = f32(value)
    mant = w & B41
    exp = (w >> 41) & 0o177
    mant = (~mant + 1) & B42
    if ((mant >> 1) ^ mant) & (1 << 40):
        mant >>= 1
        exp += 1
    return ((exp << 41) | (mant & B41)) & MASK


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--build', required=True)
    ap.add_argument('--patch-value', type=float, default=None)
    ap.add_argument('--patch-op', type=str, default=None)
    a = ap.parse_args()
    build(a.build, patch_value=a.patch_value, patch_op=a.patch_op)
