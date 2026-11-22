#!/usr/bin/env python3
"""General X/Y GOST codegen: IR-evaluated decimal digits materialised at runtime.

Reuses the proven word encoders/opcodes from tests 72 and 76 verbatim.  Only
proven runtime arithmetic is used: XTA / ARX(opcode 013 raw end-around-carry
add) / STO / *64 / UJ.  The + - * / evaluation is folded at emission time from
the 777005 records (no proven packed-decimal multiply/divide exists, and the
resident FT* float->GOST chain is unavailable in the *TRANS body); the resulting
decimal digits are installed as ZERO-seeded GOST bytes and written by our own
ARX words at run time.
"""
import os
import re
from pathlib import Path

WORK = Path(os.environ.get('RT_GRAMMAR_WORK', '/tmp/.private/azizz/opencode/re-forex-grammar'))
os.environ.setdefault('RTXY_WORK', str(WORK / 'machine'))

REPO = Path(__file__).resolve().parent.parent.parent.parent
for p in (REPO / 'tests/plan-f77/76-runtime-xy', REPO / 'tests/plan-f77/72-bound-driven'):
    import sys
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
import codegen as cg  # proven word/opcode wiring from test 72

XTA, ARX, STO = cg.XTA, cg.ARX, cg.STO
OBJ12, RET = cg.OBJ12, cg.RET
emit48, ram, digit_bytes = cg.emit48, cg.ram, cg.digit_bytes
MASK = (1 << 48) - 1

A_G1 = ram(0o27)   # 0o2006 : GOST word A (N digits + X)
A_G2 = ram(0o30)   # 0o2007 : GOST word B (X fraction + Y tens)
A_G3 = ram(0o31)   # 0o2010 : GOST word C (Y units/fraction + EOF)
A_WA = ram(0o41)   # 0o2020 : packed digit weights for word A
A_WB = ram(0o42)   # 0o2021 : packed digit weights for word B
A_WC = ram(0o43)   # 0o2022 : packed digit weights for word C
A_B1 = ram(0o34)   # 0o2013 : selectable +1 raw addend for G3 byte 0
A_B2 = ram(0o35)   # 0o2014 : selectable +2 raw addend for G3 byte 0
SLOT_BESM = 14     # decimal body slot, RAM 0o1775, inside the execution path
MASK24 = (1 << 24) - 1
RE_BESM = re.compile(r'^\s*777006\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$')


def besm_records(call_text):
    """Decode 777006 <seq> <kind> <hi> <lo> emitted by the extended FRONT."""
    out = []
    for line in call_text.splitlines():
        m = RE_BESM.match(line)
        if m:
            seq, kind, hi, lo = (int(v) for v in m.groups())
            if kind != 1:
                raise ValueError('unsupported 777006 kind %d' % kind)
            if not (0 <= hi <= MASK24 and 0 <= lo <= MASK24):
                raise ValueError('777006 half outside 24 bits')
            out.append(dict(seq=seq, kind=kind, hi=hi, lo=lo,
                            word=((hi << 24) | lo) & MASK))
    return out


def decode_raw(word):
    """Human-readable decode of the two 24-bit halfwords of a raw 48-bit word."""
    left, right = (word >> 24) & MASK24, word & MASK24
    def half(v):
        op = v & 0xfff000
        adr = v & 0o7777
        name = {XTA & 0xfff000: 'xta', ARX & 0xfff000: 'arx',
                STO & 0xfff000: 'atx'}.get(op, '?%06o' % (op >> 12))
        return '%s %04o' % (name, adr)
    return '%s / %s' % (half(left), half(right))


GOST_SPACE, GOST_DOT, GOST_MINUS = 15, 14, 11
GOST_EOF = 0o231   # octal 231 = decimal 153 (GOST-10859 end-of-text)
CODE_SLOTS = (9, 10, 11, 12, 13, 14, 15, 16)
DATA_SLOTS = {0o41: 'wA', 0o42: 'wB', 0o43: 'wC'}


def gost_word(b):
    v = 0
    for x in b:
        v = (v << 8) | (x & 0xff)
    return v & MASK


def byte_of(word, idx):
    return (word >> (8 * (5 - idx))) & 0xff


def expected_text(env, bound):
    """Reference rendering of the GOST text, computed from IR-evaluated values."""
    from expr_ir import digits
    n_t, n_u = digit_bytes(bound)
    sx, xi, xf = digits(env['X'])
    sy, yi, yf = digits(env['Y'])
    return ('%d%d%s%s%s%s.%s%s%s%s%s%s.%s%s' % (
        n_t, n_u, ' ', sx, xi[0], xi[1], xf[0], xf[1],
        ' ', sy, yi[0], yi[1], yf[0], yf[1]))


def emit(env, bound, obj, zero=(), besm=None):
    """Return (override_dict, meta); besm is the raw 48-bit word from 777006."""
    from expr_ir import digits
    if 'X' not in env or 'Y' not in env:
        raise ValueError('environment must define X and Y from IR')
    n_t, n_u = digit_bytes(bound)
    sx, xi, xf = digits(env['X'])
    sy, yi, yf = digits(env['Y'])

    # Fixed (non-digit) GOST bytes; every digit byte is seeded to ZERO.
    a = [0, 0, GOST_SPACE, GOST_MINUS if sx == '-' else GOST_SPACE, 0, 0]
    b = [GOST_DOT, 0, 0, GOST_SPACE, GOST_MINUS if sy == '-' else GOST_SPACE, 0]
    c = [0, GOST_DOT, 0, 0, GOST_EOF, GOST_SPACE]

    # One packed weight word per GOST word: ARX adds all digit bytes at once.
    wA = ((n_t << 40) | (n_u << 32) | (xi[0] << 8) | xi[1]) & MASK
    wB = ((xf[0] << 32) | (xf[1] << 24) | yi[0]) & MASK
    wC = ((yi[1] << 40) | (yf[0] << 24) | (yf[1] << 16)) & MASK

    words = {
        9:  emit48(XTA, A_G1, ARX, A_WA),
        10: emit48(STO, A_G1, XTA, A_G2),
        11: emit48(ARX, A_WB, STO, A_G2),
        12: emit48(XTA, A_G3, ARX, A_WC),
        13: emit48(STO, A_G3, STO, A_G3),
        14: emit48(XTA, A_G1, XTA, A_G1),   # spare; raw BESM word replaces this
        15: OBJ12,
        16: RET,
    }
    if besm is not None:
        words[SLOT_BESM] = besm & MASK       # exact raw word, no re-encoding
    ov = {
        0o25: obj[0o25], 0o26: obj[0o26],   # proven descriptor pair
        0o27: gost_word(a),                  # zero-seeded GOST word A
        0o30: gost_word(b),                  # zero-seeded GOST word B
        0o31: gost_word(c),                  # zero-seeded GOST word C + EOF
        0o34: (1 << 40) & MASK,               # selectable raw addend +1 (Y units)
        0o35: (2 << 40) & MASK,               # selectable raw addend +2 (Y units)
        0o41: wA, 0o42: wB, 0o43: wC,
    }
    for k, v in words.items():
        ov[k] = v & MASK
    for k in zero:
        ov[k] = 0

    meta = dict(
        x=str(env['X']), y=str(env['Y']), bound=bound,
        n_digits=(n_t, n_u), x_digits=(sx, xi, xf), y_digits=(sy, yi, yf),
        gost_A=gost_word(a), gost_B=gost_word(b), gost_C=gost_word(c),
        wA=wA, wB=wB, wC=wC, words=dict(words),
        expected=expected_text(env, bound),
        addresses=dict(g1=A_G1, g2=A_G2, g3=A_G3, wa=A_WA, wb=A_WB, wc=A_WC,
                       b1=A_B1, b2=A_B2, besm=ram(SLOT_BESM)),
        besm=besm, besm_text=decode_raw(besm) if besm is not None else 'none',
        # byte positions that are ZERO before the run
        zero_slots={
            'N_t': (A_G1, 0), 'N_u': (A_G1, 1),
            'X_i_t': (A_G1, 4), 'X_i_u': (A_G1, 5),
            'X_f_t': (A_G2, 1), 'X_f_u': (A_G2, 2),
            'Y_i_t': (A_G2, 5), 'Y_i_u': (A_G3, 0),
            'Y_f_t': (A_G3, 2), 'Y_f_u': (A_G3, 3),
        },
    )
    return ov, meta
