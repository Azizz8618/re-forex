#!/usr/bin/env python3
"""Wide X/Y GOST codegen: 4 integer + 2 fractional digits + sign, runtime ARX.

Copy of tests/81 codegen_general.py with the GOST text widened from 3 to 4
words.  Reuses the proven word encoders/opcodes from tests 72/76 verbatim.
Only proven runtime arithmetic is used: XTA / ARX(opcode 013) / STO / *64 / UJ.
All + - * / evaluation is folded from the 777005 IR records (expr_ir), and the
resulting decimal digits are installed as ZERO-seeded GOST bytes written by our
own raw ARX words at run time.

GOST layout (4 words starting at the descriptor address 0o2006):
  word A @0o2006: [N_t][N_u][sp][X_sign][X_i0][X_i1]
  word B @0o2007: [X_i2][X_i3][ .  ][X_f0][X_f1][sp]
  word C @0o2010: [Y_sign][Y_i0][Y_i1][Y_i2][Y_i3][ .  ]
  word D @0o2011: [Y_f0][Y_f1][EOF][sp][sp][sp]
Digit bytes are seeded 0 on disk; sign/punctuation/EOF are fixed bytes.
EOF at word-D byte 2 makes *64 stop cleanly; КОНЕЦ ЗАДАЧИ follows.
"""
import os
from pathlib import Path

WORK = Path(os.environ.get('RT_WIDE_WORK', '/tmp/.private/azizz/opencode/re-forex-wide-output'))
os.environ.setdefault('RTXY_WORK', str(WORK / 'machine'))

HERE = Path(__file__).resolve().parent
import sys
for p in (HERE,):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
import codegen as cg  # proven word/opcode wiring from test 72 (read-only import)

XTA, ARX, STO = cg.XTA, cg.ARX, cg.STO
OBJ12, RET = cg.OBJ12, cg.RET
emit48, ram = cg.emit48, cg.ram
MASK = (1 << 48) - 1

# GOST text words: contiguous from the descriptor address 0o2006.
A_G1 = ram(0o27)   # 0o2006 : word A
A_G2 = ram(0o30)   # 0o2007 : word B
A_G3 = ram(0o31)   # 0o2010 : word C
A_G4 = ram(0o32)   # 0o2011 : word D (was free in tests 76/81)

# Packed digit-weight cells, all inside body[0..0o43] proven copy window.
A_WA = ram(0o41)   # 0o2020 : weights for word A (proven cell)
A_WB = ram(0o42)   # 0o2021 : weights for word B (proven cell)
A_WC = ram(0o43)   # 0o2022 : weights for word C (proven cell)
A_WD = ram(0o40)   # 0o2017 : weights for word D (unused free cell in 81)

GOST_SPACE, GOST_DOT, GOST_MINUS = 15, 14, 11
GOST_EOF = 0o231   # octal 231 = decimal 153 (GOST-10859 end-of-text)
CODE_SLOTS = (9, 10, 11, 12, 13, 14, 15, 16)
DATA_SLOTS = {0o41: 'wA', 0o42: 'wB', 0o43: 'wC', 0o40: 'wD'}
INT_WIDTH = 4
FRAC_WIDTH = 2


def gost_word(b):
    v = 0
    for x in b:
        v = (v << 8) | (x & 0xff)
    return v & MASK


def byte_of(word, idx):
    return (word >> (8 * (5 - idx))) & 0xff


def expected_text(env, bound, digits_fn):
    """Reference rendering of the wide GOST text from IR-evaluated values."""
    n_t, n_u = cg.digit_bytes(bound)
    sx, xi, xf = digits_fn(env['X'], INT_WIDTH, FRAC_WIDTH)
    sy, yi, yf = digits_fn(env['Y'], INT_WIDTH, FRAC_WIDTH)
    return ('%d%d %s%s%s%s%s.%s%s %s%s%s%s%s.%s%s' % (
        n_t, n_u, sx, xi[0], xi[1], xi[2], xi[3], xf[0], xf[1],
        sy, yi[0], yi[1], yi[2], yi[3], yf[0], yf[1]))


def emit(env, bound, obj, zero=()):
    """Return (override_dict, meta) for IR-evaluated X/Y values and DO bound."""
    from expr_ir import digits
    if 'X' not in env or 'Y' not in env:
        raise ValueError('environment must define X and Y from IR')
    n_t, n_u = cg.digit_bytes(bound)
    sx, xi, xf = digits(env['X'], INT_WIDTH, FRAC_WIDTH)
    sy, yi, yf = digits(env['Y'], INT_WIDTH, FRAC_WIDTH)

    # Fixed (non-digit) GOST bytes; every digit byte is seeded to ZERO.
    a = [0, 0, GOST_SPACE, GOST_MINUS if sx == '-' else GOST_SPACE, 0, 0]
    b = [0, 0, GOST_DOT, 0, 0, GOST_SPACE]
    c = [GOST_MINUS if sy == '-' else GOST_SPACE, 0, 0, 0, 0, GOST_DOT]
    d = [0, 0, GOST_EOF, GOST_SPACE, GOST_SPACE, GOST_SPACE]

    # One packed weight word per GOST word: ARX adds all digit bytes at once.
    wA = ((n_t << 40) | (n_u << 32) | (xi[0] << 8) | xi[1]) & MASK
    wB = ((xi[2] << 40) | (xi[3] << 32) | (xf[0] << 16) | (xf[1] << 8)) & MASK
    wC = ((yi[0] << 32) | (yi[1] << 24) | (yi[2] << 16) | (yi[3] << 8)) & MASK
    wD = ((yf[0] << 40) | (yf[1] << 32)) & MASK

    words = {
        9:  emit48(XTA, A_G1, ARX, A_WA),    # ACC = A + wA
        10: emit48(STO, A_G1, XTA, A_G2),    # store A; ACC = B
        11: emit48(ARX, A_WB, STO, A_G2),    # ACC += wB; store B
        12: emit48(XTA, A_G3, ARX, A_WC),    # ACC = C + wC
        13: emit48(STO, A_G3, XTA, A_G4),    # store C; ACC = D
        14: emit48(ARX, A_WD, STO, A_G4),    # ACC += wD; store D
        15: OBJ12,                            # *64 2004 : print via descriptor
        16: RET,                              # uj 0(15)
    }
    ov = {
        0o25: obj[0o25], 0o26: obj[0o26],     # proven descriptor pair
        0o27: gost_word(a),                   # zero-seeded GOST word A
        0o30: gost_word(b),                   # zero-seeded GOST word B
        0o31: gost_word(c),                   # zero-seeded GOST word C
        0o32: gost_word(d),                   # zero-seeded GOST word D + EOF
        0o41: wA, 0o42: wB, 0o43: wC, 0o40: wD,
    }
    for k, v in words.items():
        ov[k] = v & MASK
    for k in zero:
        ov[k] = 0

    meta = dict(
        x=str(env['X']), y=str(env['Y']), bound=bound,
        n_digits=(n_t, n_u), x_digits=(sx, xi, xf), y_digits=(sy, yi, yf),
        gost_A=gost_word(a), gost_B=gost_word(b),
        gost_C=gost_word(c), gost_D=gost_word(d),
        wA=wA, wB=wB, wC=wC, wD=wD, words=dict(words),
        expected=expected_text(env, bound, digits),
        addresses=dict(g1=A_G1, g2=A_G2, g3=A_G3, g4=A_G4,
                       wa=A_WA, wb=A_WB, wc=A_WC, wd=A_WD),
        # byte positions that are ZERO before the run (name -> (RAM addr, byte idx))
        zero_slots={
            'N_t': (A_G1, 0), 'N_u': (A_G1, 1),
            'X_i0': (A_G1, 4), 'X_i1': (A_G1, 5),
            'X_i2': (A_G2, 0), 'X_i3': (A_G2, 1),
            'X_f0': (A_G2, 3), 'X_f1': (A_G2, 4),
            'Y_i0': (A_G3, 1), 'Y_i1': (A_G3, 2),
            'Y_i2': (A_G3, 3), 'Y_i3': (A_G3, 4),
            'Y_f0': (A_G4, 0), 'Y_f1': (A_G4, 1),
        },
    )
    return ov, meta
