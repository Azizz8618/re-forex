#!/usr/bin/env python3
"""B4: machine-code EXPRESSION PARSER WITH PRECEDENCE (shunting-yard).

Reuses the proven B3 statement dispatcher VERBATIM (PROGRAM / REAL / PRINT /
END / statement loop / docs/105 GOST converter in N+3).  Only the assignment
handler is replaced: instead of "ID = LIT" it runs a two-stack shunting-yard
evaluator over the B2 token stream up to EOL, using the proven FPU ops, then
stores 10*result into the symbol value word (the verbatim converter divides by
10).  All numeric values are built/computed by BESM-6 instructions; no
host-computed result digit appears anywhere.

Copies only: no repository / live-disk / tmux-0 / C patch.  C dispak is oracle
only.  The deck still carries TOKEN FIXTURES in N+2, not Fortran source (B1
will later emit tokens from real fixed-form text).
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
CODE_OFF = 256                 # LEX moved to N+1, so 245..259 are free again
CODE_RAM = N2_RAM0 + CODE_OFF
CONV_RAM0 = 0o30114

# opcodes (identical values to the proven B3 / C6 builders)
ATX, AAX, AEX, ARX, ASX = 0o00, 0o11, 0o12, 0o13, 0o26
ADD, FSUB, DIV, MUL = 0o04, 0o06, 0o16, 0o17
AVX, AOX = 0o14, 0o15
ATI, UJ, UZA = 0o40, 0o300, 0o260
DUMMY = C6.FB.DUMMY
UJ15 = C6.FB.UJ15
UTC_N2 = long_(0o220, 0o20000)   # arm M20 = 0o20000 for the next halfword only

# ----------------------------- N+2 map -----------------------------
# (B3 layout preserved for everything except the new evaluator cells/code)
TOKBASE = 64          # 64..95: token words (B2 one-word layout)
LITBASE = 100         # 100..103: literal pool, BESM floats (actual values)
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

# ---- new evaluator work cells / constants (142..159) ----
C_OP, C_A, C_B, C_TOP = 142, 143, 144, 145   # apply scratch
C_SPO, C_SPP, C_MODE = 146, 147, 148         # stack pointers / return mode
K_NEG1, K_TEN, K_PATCH = 149, 150, 151       # -1, float(10), display bias (PATCH target)
K_OPADD, KOPSUB, KOPMUL, KOPDIV = 152, 153, 154, 155
K_TKLIT, K_TKOP, K_TKLP = 156, 157, 158
K_MODE2 = 159                                 # continuation mode 2 (flush)
K_BIAS = 160                                  # stack-pointer bias (avoids -0)
C_PUSHVAL = 161                               # scratch: value across index setup

# ---- B6b intrinsic extension: free cells 98..99 + 901..912 (tail band, freed
# by moving LEX to N+1).  OPR markers: INTR SUB+4 -> ABS=5, SQRT=6, MOD=7.
# Scratch reuses C_A/C_B/C_TOP (143..145).
K_TK5, K_TK6 = 98, 99                           # INTR / marker-6 values
K_TK7 = 901                                     # COMMA value
K_INTRBIAS = 902                                # 4: SUB -> OPR marker
K_SIGN_CELL = 903                               # 1<<40 : avx negate control
K_HALF = 904                                    # f32(0.5) for Newton
K_MASK40 = 905                                  # 0xFFFFFFFFFF (40-bit mantissa)
K_EXPALL = 906                                  # all exponent bits + sign
C_MODA, C_MODB, C_MODQ = 907, 908, 909          # MOD a, b, quotient
ITAB0, ITAB1, ITAB2 = 910, 911, 912             # 3 LONG uj trampoline words

OSTK = 200           # 200..229: operand stack (BESM floats)
OPR = 230            # 230..244: operator stack (SUB codes, 0 = '(' marker)


def tok(tk, sub=0, pos=0, pay=0):
    """B2 token word: (TK<<42)|(SUB<<36)|(POS<<24)|PAY."""
    return ((tk & 0x3f) << 42) | ((sub & 0x3f) << 36) | ((pos & 0xfff) << 24) | (pay & 0xffffff)


# Token fixtures: expression X = 1.5 + 2.5 * 4.0 (A) or ... * 2.0 (B).
# A one-word token change (last LIT PAY 2 -> 3) selects literal index 3 = 2.0.
def fixture(lit_pay=2):
    return [
        tok(10, 30),                      # PROGRAM
        tok(2),                           # name (consumed)
        tok(10, 31),                      # REAL
        tok(2, 0, 0, 1),                  # X (VIDX=1)
        tok(11),                          # EOL
        tok(2, 0, 0, 1),                  # X = (assignment lhs)
        tok(8),                           # =
        tok(1, 0, 0, 0),                  # LIT 1.5   (pool 0)
        tok(3, 1),                        # OP  +
        tok(1, 0, 0, 1),                  # LIT 2.5   (pool 1)
        tok(3, 3),                        # OP  *
        tok(1, 0, 0, lit_pay),            # LIT       (pool 2 = 4.0, pool 3 = 2.0)
        tok(11),                          # EOL (end of expression / assignment)
        tok(10, 34),                      # PRINT
        tok(13, 1, 0, (4 << 8) | 2),      # F4.2
        tok(2, 0, 0, 1),                  # X
        tok(11),                          # EOL
        tok(10, 37),                      # END
    ]


def fixture_parens():
    """X = (1.5 + 2.5) * 4.0  ->  16.00 (proves parentheses override precedence)."""
    return [
        tok(10, 30), tok(2), tok(10, 31), tok(2, 0, 0, 1), tok(11),
        tok(2, 0, 0, 1), tok(8),
        tok(6, 1),                        # '('
        tok(1, 0, 0, 0),                  # 1.5
        tok(3, 1),                        # +
        tok(1, 0, 0, 1),                  # 2.5
        tok(6, 2),                        # ')'
        tok(3, 3),                        # *
        tok(1, 0, 0, 2),                  # 4.0
        tok(11),
        tok(10, 34), tok(13, 1, 0, (4 << 8) | 2), tok(2, 0, 0, 1), tok(11),
        tok(10, 37),
    ]


# ----------------------------- machine code -----------------------------
def build_parser(conv_ram):
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
        c.Z(0o10, 'HALF'); c.L(ATI, 12)     # M[12] = 0o20000 (N+2 data base)
        c.Z(0o10, 'HALF'); c.L(ATI, 7)      # M[7]  = 0o20000 (short-branch base)

    def fetch():
        c.C(0o10, C_SPC); c.L(ATI, 6)        # M[6] = token index
        c.E(UTC_N2)
        c.L(0o10, 0o1637 + TOKBASE, reg=6)   # ACC = token word
        c.C(ATX, C_TOK)
        c.C(0o10, C_SPC); c.C(ARX, K_ONE); c.C(ATX, C_SPC)   # SPC++

    def extract():
        c.C(0o10, C_TOK); c.C(AAX, K_MTK); c.C(ASX, K_SR42); c.C(ATX, C_TK)
        c.C(0o10, C_TOK); c.C(AAX, K_MSUB); c.C(ASX, K_SR36); c.C(ATX, C_SUB)
        c.C(0o10, C_TOK); c.C(AAX, K_MPAY);               c.C(ATX, C_PAY)

    # ---- stack helpers (SP biased by K_BIAS=100; empty == K_BIAS) ----
    # BESM one's complement has 1 + (-1) = -0 (all ones) and UZA does not
    # branch on -0.  With a 100 bias, SP-1 is always a large positive index,
    # so neither the empty test nor the index computation can produce -0.
    # ADR absorbs the bias: 0o1637 + base - K_BIAS, index register = SP.
    OSTK_ADR = 0o1637 + OSTK - 100
    OPR_ADR = 0o1637 + OPR - 100

    def push_o():                 # ACC -> OSTK[SP], SP++  (save value: ATI clobbers ACC)
        c.C(ATX, C_PUSHVAL)
        c.C(0o10, C_SPO); c.L(ATI, 6)
        c.C(0o10, C_PUSHVAL)
        c.E(UTC_N2); c.L(ATX, OSTK_ADR, reg=6)
        c.C(0o10, C_SPO); c.C(ARX, K_ONE); c.C(ATX, C_SPO)

    def pop_o():                  # SP--, OSTK[SP] -> ACC
        c.C(0o10, C_SPO); c.C(ARX, K_NEG1); c.C(ATX, C_SPO)
        c.C(0o10, C_SPO); c.L(ATI, 6)
        c.E(UTC_N2); c.L(0o10, OSTK_ADR, reg=6)

    def push_p():                 # ACC -> OPR[SP], SP++  (save value across ATI)
        c.C(ATX, C_PUSHVAL)
        c.C(0o10, C_SPP); c.L(ATI, 6)
        c.C(0o10, C_PUSHVAL)
        c.E(UTC_N2); c.L(ATX, OPR_ADR, reg=6)
        c.C(0o10, C_SPP); c.C(ARX, K_ONE); c.C(ATX, C_SPP)

    def pop_p():                  # SP--, OPR[SP] -> ACC
        c.C(0o10, C_SPP); c.C(ARX, K_NEG1); c.C(ATX, C_SPP)
        c.C(0o10, C_SPP); c.L(ATI, 6)
        c.E(UTC_N2); c.L(0o10, OPR_ADR, reg=6)

    def peek_p():                 # OPR[SP-1] -> ACC (does not alter SP_P)
        c.C(0o10, C_SPP); c.C(ARX, K_NEG1); c.L(ATI, 6)
        c.E(UTC_N2); c.L(0o10, OPR_ADR, reg=6)

    def empty_p():                # emit AEX K_BIAS; caller follows with br(UZA,...)
        c.C(0o10, C_SPP); c.C(AEX, K_BIAS)

    # ================= B3 dispatcher (verbatim except ASSIGN) =================
    mark('LOOP')
    rearm()
    fetch()
    extract()
    c.C(0o10, C_TK); c.C(AEX, K_TK11); br(UZA, 'LOOP')    # EOL: skip
    c.C(0o10, C_TK); c.C(AEX, K_TK12); br(UZA, 'DONE')    # EOF
    c.C(0o10, C_TK); c.C(AEX, K_TK10); br(UZA, 'KW')      # keyword
    c.C(0o10, C_TK); c.C(AEX, K_TK2);  br(UZA, 'ASSIGN')  # ID -> assignment
    br(UJ, 'LOOP')

    mark('KW')
    c.C(0o10, C_SUB); c.C(AEX, K_SUB30); br(UZA, 'S_PROGRAM')
    c.C(0o10, C_SUB); c.C(AEX, K_SUB31); br(UZA, 'S_REAL')
    c.C(0o10, C_SUB); c.C(AEX, K_SUB34); br(UZA, 'S_PRINT')
    c.C(0o10, C_SUB); c.C(AEX, K_SUB37); br(UZA, 'DONE')
    br(UJ, 'LOOP')

    mark('S_PROGRAM')
    fetch()
    br(UJ, 'LOOP')

    mark('S_REAL')
    mark('REAL_L')
    fetch()
    extract()
    c.C(0o10, C_TK); c.C(AEX, K_TK11); br(UZA, 'LOOP')
    c.C(0o10, C_PAY); c.L(ATI, 6)
    c.C(0o10, K_ZERO)
    c.E(UTC_N2); c.L(ATX, 0o1637 + 32, reg=6)
    br(UJ, 'REAL_L')

    mark('ASSIGN')                             # C_PAY = VIDX of the ID token
    c.C(0o10, C_PAY); c.C(ATX, C_VIDX)
    fetch()                                    # consume '=' token
    br(UJ, 'EVAL')                             # run the expression evaluator

    mark('S_PRINT')
    fetch()                                    # FD token
    extract()
    c.C(0o10, C_PAY); c.C(ASX, K_SR8); c.C(ATX, C_W)
    c.C(0o10, C_PAY); c.C(AAX, K_255); c.C(ATX, C_D)
    fetch()                                    # ID token
    extract()
    c.C(0o10, C_PAY); c.L(ATI, 6)
    c.E(UTC_N2); c.L(0o10, 0o1637 + 32, reg=6); c.Z(ATX, 'EST')   # EST = value (10*P)
    c.Z(0o10, 'EST'); c.C(ADD, K_PRINT_BIAS); c.Z(ATX, 'EST')      # patch target
    c.C(0o10, K_GOSTA); c.L(ATX, 0o2006)
    c.C(0o10, K_GOSTB); c.L(ATX, 0o2007)
    c.C(0o10, C_W); c.L(ATI, 6)
    c.E(UTC_N2); c.L(0o10, 0o1637 + K_WMASK0 - 2, reg=6)
    c.L(AEX, 0o2006); c.L(ATX, 0o2006)
    c.C(0o10, C_D); c.L(ATI, 6)
    c.E(UTC_N2); c.L(0o10, 0o1637 + K_CLEARM0 - 1, reg=6)
    c.L(AAX, 0o2007); c.L(ATX, 0o2007)
    c.E(UTC_N2); c.L(0o10, 0o1637 + K_SPACEM0 - 1, reg=6)
    c.L(ARX, 0o2007); c.L(ATX, 0o2007)
    c.vjmo(conv_ram)                            # verbatim converter -> *64 2004
    rearm()
    br(UJ, 'LOOP')

    # ================ two-stack shunting-yard evaluator =================
    mark('EVAL')
    c.C(0o10, K_BIAS); c.C(ATX, C_SPO)           # biased empty = K_BIAS
    c.C(0o10, K_BIAS); c.C(ATX, C_SPP)           # biased empty = K_BIAS

    mark('EV_SCAN')
    rearm()
    fetch()
    extract()
    c.C(0o10, C_TK); c.C(AEX, K_TKLIT); br(UZA, 'EV_LIT')
    c.C(0o10, C_TK); c.C(AEX, K_TKOP);  br(UZA, 'EV_OP')
    c.C(0o10, C_TK); c.C(AEX, K_TKLP);  br(UZA, 'EV_LR')
    c.C(0o10, C_TK); c.C(AEX, K_TK5);   br(UZA, 'EV_INTR')   # INTR (B6b)
    c.C(0o10, C_TK); c.C(AEX, K_TK7);   br(UZA, 'EV_SCAN')   # COMMA: no-op (B6b)
    c.C(0o10, C_TK); c.C(AEX, K_TK11);  br(UZA, 'EV_EOL')    # EOL ends expression
    br(UJ, 'EV_SCAN')
    mark('EV_LR')                               # '(' / ')' share TK=6; split on SUB
    c.C(0o10, C_SUB); c.C(AEX, K_ONE); br(UZA, 'EV_LP')      # SUB=1 -> '('
    br(UJ, 'EV_RP')                                         # SUB=2 -> ')'

    # ---- INTR prefix marker: SUB+4 -> OPR marker (ABS=5,SQRT=6,MOD=7) ----
    mark('EV_INTR')
    c.C(0o10, C_SUB); c.C(ADD, K_INTRBIAS); push_p()
    br(UJ, 'EV_SCAN')

    mark('EV_LIT')                              # literal -> operand stack
    c.C(0o10, C_PAY); c.L(ATI, 6)
    c.E(UTC_N2); c.L(0o10, 0o1637 + LITBASE, reg=6)
    push_o()
    br(UJ, 'EV_SCAN')

    mark('EV_OP')                               # binary operator: precedence loop
    mark('EV_PREC_LOOP')
    empty_p(); br(UZA, 'EV_PUSH_OP')            # empty OPR -> push incoming
    peek_p()
    br(UZA, 'EV_PUSH_OP')                       # top == '(' marker -> push incoming
    c.C(ATX, C_TOP)                             # top op SUB in C_TOP
    # pop iff NOT(incoming is high-prec AND top is low-prec)
    c.C(0o10, C_SUB); c.C(AEX, KOPMUL); br(UZA, 'EV_IN_HIGH')
    c.C(0o10, C_SUB); c.C(AEX, KOPDIV); br(UZA, 'EV_IN_HIGH')
    br(UJ, 'EV_DO_POP')                         # incoming low -> always pop
    mark('EV_IN_HIGH')
    c.C(0o10, C_TOP); c.C(AEX, KOPMUL); br(UZA, 'EV_DO_POP')
    c.C(0o10, C_TOP); c.C(AEX, KOPDIV); br(UZA, 'EV_DO_POP')
    br(UJ, 'EV_PUSH_OP')                        # high over low -> push incoming
    mark('EV_DO_POP')
    c.C(0o10, K_ZERO); c.C(ATX, C_MODE)         # mode 0 -> return to precedence loop
    br(UJ, 'EV_APPLY')
    mark('EV_PUSH_OP')
    c.C(0o10, C_SUB); push_p()                  # push incoming op SUB
    br(UJ, 'EV_SCAN')

    mark('EV_LP')                               # '(' -> push marker 0
    c.C(0o10, K_ZERO); push_p()
    br(UJ, 'EV_SCAN')

    mark('EV_RP')                               # ')' -> pop until marker
    mark('EV_RP_LOOP')
    empty_p(); br(UZA, 'EV_SCAN')               # unbalanced: just continue
    peek_p()
    br(UZA, 'EV_RP_MARK')                       # marker found
    c.C(0o10, K_ONE); c.C(ATX, C_MODE)          # mode 1 -> return to RP loop
    br(UJ, 'EV_APPLY')
    mark('EV_RP_MARK')
    c.C(0o10, C_SPP); c.C(ARX, K_NEG1); c.C(ATX, C_SPP)   # discard '(' marker
    # B6b: after the matching ')' check for a pending INTR marker underneath.
    empty_p(); br(UZA, 'EV_SCAN')
    peek_p(); c.C(ATX, C_TOP)
    c.C(0o10, C_TOP); c.C(AEX, K_TK5); br(UZA, 'EV_INTR_APPLY')
    c.C(0o10, C_TOP); c.C(AEX, K_TK6); br(UZA, 'EV_INTR_APPLY')
    c.C(0o10, C_TOP); c.C(AEX, K_TK7); br(UZA, 'EV_INTR_APPLY')
    br(UJ, 'EV_SCAN')

    # ===== B6b: apply intrinsic to OSTK operand(s), then dispatch via ITAB =====
    mark('EV_INTR_APPLY')
    pop_p(); c.C(ATX, C_OP)                      # C_OP = 5/6/7 marker
    c.C(0o10, C_OP); c.C(AEX, K_TK7); br(UZA, 'EV_MOD_FETCH')
    pop_o()                                     # ABS/SQRT: one operand in ACC
    br(UJ, 'EV_INTR_DISPATCH')
    mark('EV_MOD_FETCH')
    pop_o(); c.C(ATX, C_MODB)                   # b = top
    pop_o(); c.C(ATX, C_MODA)                   # a = below
    c.C(0o10, C_MODA)                           # ACC = a for the MOD routine
    mark('EV_INTR_DISPATCH')
    c.C(ARX, K_INTRBIAS)                        # 5/6/7 -> 1/2/3
    c.L(ATI, 6)                                 # M[6] = table index
    c.E(long_(UJ, N2_RAM0 + ITAB0 - 1, reg=6))  # uj (ITAB0-1)(6) -> trampoline

    mark('DO_ABS')                              # true |ACC| via proven avx negate
    c.C(ATX, C_A)                               # save operand
    c.C(0o10, C_A); c.C(AAX, K_SIGN_CELL)       # isolate the BESM sign bit (b40)
    br(UZA, 'ABS_POS')                          # already positive -> keep it
    c.C(0o10, C_A); c.C(AVX, K_SIGN_CELL)       # negative -> avx negate
    br(UJ, 'INTR_DONE')
    mark('ABS_POS')
    c.C(0o10, C_A)
    br(UJ, 'INTR_DONE')

    mark('DO_SQRT')                             # Newton x4: x=(x+S/x)/2
    c.C(ATX, C_A)                               # C_A = S
    c.C(0o10, C_A); c.C(ATX, C_B)
    for _ in range(4):
        c.C(0o10, C_A); c.C(DIV, C_B)
        c.C(ADD, C_B);  c.C(MUL, K_HALF); c.C(ATX, C_B)
    c.C(0o10, C_B)
    br(UJ, 'INTR_DONE')

    mark('DO_MOD')                              # bitwise-AINT remainder
    c.C(ATX, C_MODA)                            # a (ACC) -> C_MODA
    c.C(0o10, C_MODA); c.C(DIV, C_MODB); c.C(ATX, C_MODQ)  # Q = a/b
    c.C(0o10, K_MASK40); c.C(ASX, C_MODQ); c.C(AEX, K_MASK40)
    c.C(AOX, K_EXPALL); c.C(ATX, C_A)           # exact-integer mask -> C_A
    c.C(0o10, C_MODQ); c.C(AAX, C_A); c.C(ATX, C_B)         # AINT(Q) -> C_B
    c.C(0o10, C_MODB); c.C(MUL, C_B); c.C(ATX, C_TOP)       # b*AINT(Q)
    c.C(0o10, C_MODA); c.C(FSUB, C_TOP)         # a - b*AINT(a/b)
    mark('INTR_DONE')
    push_o()                                    # intrinsic result -> OSTK
    br(UJ, 'EV_SCAN')

    mark('EV_EOL')                              # flush remaining operators
    mark('EV_FLUSH_LOOP')
    empty_p(); br(UZA, 'EV_DONE')
    peek_p()
    br(UZA, 'EV_FLUSH_MARK')
    c.C(0o10, K_MODE2); c.C(ATX, C_MODE)        # mode 2 -> return to flush loop
    br(UJ, 'EV_APPLY')
    mark('EV_FLUSH_MARK')
    c.C(0o10, C_SPP); c.C(ARX, K_NEG1); c.C(ATX, C_SPP)
    br(UJ, 'EV_FLUSH_LOOP')

    mark('EV_APPLY')                            # pop top op, pop b, pop a, apply
    pop_p(); c.C(ATX, C_OP)
    pop_o(); c.C(ATX, C_B)
    pop_o(); c.C(ATX, C_A)
    c.C(0o10, C_OP); c.C(AEX, K_OPADD); br(UZA, 'EV_ADD')
    c.C(0o10, C_OP); c.C(AEX, KOPSUB);  br(UZA, 'EV_SUB')
    c.C(0o10, C_OP); c.C(AEX, KOPMUL);  br(UZA, 'EV_MUL')
    br(UJ, 'EV_DIV')
    mark('EV_ADD')
    c.C(0o10, C_A); c.C(ADD, C_B); br(UJ, 'EV_STORE_RES')
    mark('EV_SUB')
    c.C(0o10, C_A); c.C(FSUB, C_B); br(UJ, 'EV_STORE_RES')
    mark('EV_MUL')
    c.C(0o10, C_A); c.C(MUL, C_B);  br(UJ, 'EV_STORE_RES')
    mark('EV_DIV')
    c.C(0o10, C_A); c.C(DIV, C_B)
    mark('EV_STORE_RES')
    push_o()                                    # push result back onto OSTK
    c.C(0o10, C_MODE); br(UZA, 'EV_PREC_LOOP')
    c.C(0o10, C_MODE); c.C(AEX, K_ONE); br(UZA, 'EV_RP_LOOP')
    br(UJ, 'EV_FLUSH_LOOP')

    mark('EV_DONE')                             # result = 10*R + bias -> symbol value
    pop_o()                                     # ACC = R
    c.C(MUL, K_TEN)                             # ACC = 10*R (converter divides by 10)
    c.C(ADD, K_PATCH)                           # display bias (PATCH target)
    c.C(ATX, C_PUSHVAL)                         # save result across index setup
    c.C(0o10, C_VIDX); c.L(ATI, 6)
    c.C(0o10, C_PUSHVAL)
    c.E(UTC_N2); c.L(ATX, 0o1637 + 32, reg=6)   # symbol value word
    br(UJ, 'LOOP')

    mark('DONE')
    c.E(UJ15)

    # resolve deferred short branches (reg7 base = 0o20000)
    for i, name, op in branches:
        idx = labels[name]
        assert idx % 2 == 0, (name, idx)
        ram = CODE_RAM + idx // 2
        H[i] = short(op, (ram - 0o20000) & 0o7777, reg=7)
    if len(H) % 2:
        H.append(DUMMY)
    return c, labels


def build(case, lit_pay=2, patch=0.0, parens=False):
    src = WS / 'images/2048_base'
    dst = WS / 'images' / f'2048_{case}'
    shutil.copy2(src, dst)

    body = rz(str(dst), N + 1)
    body[0o11] = word(long_(0o300, CODE_RAM, reg=0), 0)   # contour entry -> our code
    body[0o27] = int.from_bytes(bytes([2, 1, 15, 15, 0, 0]), 'big')
    body[0o30] = int.from_bytes(bytes([0, 0, 14, 0, 0, 15]), 'big')
    body[0o31] = int.from_bytes(bytes([15, 3, 0, 0, 0, 14]), 'big')
    body[0o32] = int.from_bytes(bytes([0, 0, 0o231, 15, 15, 15]), 'big')
    for n, value in C6.vals().items():
        body[0o110 + FS.CELLS.index(n)] = value & MASK
    wz(str(dst), N + 1, body)

    n3_hw, floor_ram, conv_len, floor_len = C6.build_n3()
    wz(str(dst), Z3, C6.asm_words(n3_hw))

    n2, labels = build_parser(CONV_RAM0)
    z2 = rz(str(dst), N2)                       # preserve 526..900 overlay
    # symbol table (reuse proven docs/109/114 layout)
    z2[1] = C6.C2.text_word('X       ') & MASK
    z2[33] = f32(0.0)
    # literal pool: ACTUAL float values (the evaluator scales result by 10 at the end)
    literals = [f32(1.5), f32(2.5), f32(4.0), f32(2.0)]
    for i, v in enumerate(literals):
        z2[LITBASE + i] = v & MASK
    # token fixture (the executed program at this milestone)
    toks = fixture_parens() if parens else fixture(lit_pay=lit_pay)
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
        K_PRINT_BIAS: 0,
        K_NEG1: MASK ^ 1, K_TEN: f32(10.0), K_PATCH: f32(patch),
        K_OPADD: 1, KOPSUB: 2, KOPMUL: 3, KOPDIV: 4,
        K_TKLIT: 1, K_TKOP: 3, K_TKLP: 6, K_MODE2: 2, K_BIAS: 100,
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
                 LITBASE + 4, OPR + 15, C_PUSHVAL + 1, K_SPACEM1 + 1) + 1
    print(f'case={case} sha={sha} N3={len(n3_hw)//2}/{MAX_WORDS}w '
          f'conv={conv_len}hw floor={floor_len}hw N2code={len(hw)}hw '
          f'({(len(hw)+1)//2} words) N2used={n2used}/649 ntok={len(toks)} '
          f'lit_pay={lit_pay} patch={patch} parens={parens} '
          f'CODE_RAM={CODE_RAM:06o} labels={len(labels)}')
    return dst, sha, n2used, len(n3_hw) // 2


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--build', required=True)
    ap.add_argument('--lit-pay', type=int, default=2)
    ap.add_argument('--patch', type=float, default=0.0)
    ap.add_argument('--parens', action='store_true')
    a = ap.parse_args()
    build(a.build, lit_pay=a.lit_pay, patch=a.patch, parens=a.parens)
