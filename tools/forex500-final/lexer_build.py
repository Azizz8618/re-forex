#!/usr/bin/env python3
"""B1: machine-code Fortran lexer + NAME=NUMBER assignment contour.

VERBATIM REUSE:
  * canonical docs/105 GOST converter + sign + reclaims + floor_int as a VJM
    subroutine in zone N+3 (c2b_build.build_n3 / asm_words),
  * RLE card-buffer at RAM 0o64000+ (docs/104/114),
  * ASCII->digit / 10*T[] / e+x / *100 chain of docs/104 applied to the NUMBER
    token payload,
  * N+2 free-word reach (M[14]=0o20000 base) and N+2 code execution
    (docs/110/114), low-RAM cell map from final_build.

NEW MACHINE CODE (all in N+2): byte scanner locating '=' in the RLE stream,
NEXTCHAR reader, token emitter, and the NAME=NUMBER handler.

TOKEN FORMAT (N+2 array at offset 200, 2 words per token):
  word A: byte0 = KIND (1=IDENT, 2=NUMBER, else ASCII of single-char token),
          byte1 = LEN (letters/digits; 0 for single-char), bytes2-5 = 0.
  word B: PAYLOAD, ASCII bytes right-aligned ('.' in a number skipped;
          single-char tokens payload = 0).
"""
import argparse, hashlib, shutil, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import c2b_build as CB
import final_build as F
import final_sign as FS
from build_e2e import rz, wz, short, long_, word, f32, MASK, N, Z3, MAX_WORDS

WS = HERE.parent
N2 = N + 2
N2_RAM0 = 0o21637
CONV_RAM0 = 0o30114

ATX, AAX, AEX, ARX, ASX = 0o00, 0o11, 0o12, 0o13, 0o26
MUL, DIV, FADD = 0o17, 0o16, 0o04
ATI, EPLUSX, E64, ITA, UJ, UZA = 0o40, 0o24, 0o64, 0o42, 0o300, 0o260
DUMMY = F.DUMMY
UJ15 = F.UJ15

R_BRANCH, R_CPTR, R_RUN, R_TOK, R_N2, R_LINK = 7, 10, 6, 5, 14, 9

K_ZERO=0; K_BASE=100; K_CBASE=101; K_ONE=102; K_SIX=103
K_M8=104; K_NEG20=105; K_NEG30=106; K_NEG3D=107; K_NEG81=108; K_NEGM1=109
K_SHL8=110; K_SHR40=111; K_SHL6=112; K_SHR24=113; K_SHR16=114; K_SHR8=115
K_SHL40=116; K_SHL32=117; K_MASKC0=118; K_MASKF0=119; K_K40=120; K_K30=121
K_K80=122; K_DOT=123; K_0A=124; K_PD0=125; K_EMASK=126; K_C105=127
K_HUNDRED=128; K_SPACE=129; K_GOSTA=130; K_GOSTB=131
K_IDENT=132; K_NUMBER=133; K_LENTAB=140
C_RUN=160; C_CURW=161; C_CH=162; C_PAY=163; C_NAME=164; C_TMP=165
C_LEN=166; C_NDIG=167; C_SYMNAME=170; C_SYMVAL=171
TOKBASE=200; CODEBASE=250
KIND_IDENT, KIND_NUMBER = 1, 2


def ret_imm(reg):
    return (reg << 20) | (0o30 << 15)


class Asm:
    """Tiny assembler with deferred label/branch patching."""
    def __init__(self):
        self.hw = []
        self.labels = {}
        self.branches = []      # (hw_index, label)
        self.vjm_targets = []   # (hw_index, label)

    def E(self, x):
        self.hw.append(x & 0xffffff); return len(self.hw) - 1

    def L(self, op, adr, reg=0):
        return self.E(short(op, adr, reg=reg))

    def C(self, op, off, reg=R_N2):
        return self.L(op, 0o1637 + off, reg=reg)   # M[14]=0o20000 -> N+2 word off

    def Z(self, op, name):
        return self.L(op, FS.LO[name])

    def T(self, op, idx, reg=0):
        """token array word; UTC modifier supplies 0o20000, reg indexes if needed"""
        self.E(long_(0o220, 0o20000))
        return self.L(op, 0o1637 + TOKBASE + idx, reg=reg)

    def br(self, op, label, reg=R_BRANCH):
        i = self.L(op, 0, reg=reg)
        self.branches.append((i, label))
        return i

    def mark(self, label):
        if len(self.hw) % 2:
            # A right-half pad would be executed on fall-through. Make it a
            # jump to the next word (the label target) instead.
            nxt = N2_RAM0 + CODEBASE + (len(self.hw) + 1) // 2
            self.L(UJ, (nxt - 0o20000) & 0o7777, reg=R_BRANCH)
        self.labels[label] = len(self.hw)

    def markh(self, label):
        self.labels[label] = len(self.hw)

    def call(self, label, reg=R_LINK):
        if len(self.hw) % 2 == 0:
            i = self.E((reg << 20) | (0o31 << 15))   # vjm placeholder, addr 0
            self.E(DUMMY)
        else:
            i = self.E((reg << 20) | (0o31 << 15))
        self.vjm_targets.append((i, label))

    def resolve(self):
        for i, label in self.branches:
            tgt = self.labels[label]
            assert tgt % 2 == 0, (label, tgt)
            ram = N2_RAM0 + CODEBASE + tgt // 2
            self.hw[i] = (self.hw[i] & 0xffff00) | ((ram - 0o20000) & 0o7777)
        for i, label in self.vjm_targets:
            if label == 'CONV':
                ram = CONV_RAM0
            else:
                tgt = self.labels[label]
                assert tgt % 2 == 0, (label, tgt)
                ram = N2_RAM0 + CODEBASE + tgt // 2
            self.hw[i] = (self.hw[i] & 0xfff800) | (ram & 0o77777)


def rearm(a):
    # M[14] is 0 at entry: the first base value must come from directly
    # addressable low RAM (HALF = 0o20000, the c2b/ir4-sign proven cell).
    a.Z(0o10, 'HALF'); a.L(ATI, R_N2)
    a.C(0o10, K_BASE); a.L(ATI, R_BRANCH)
    a.C(0o10, K_CBASE); a.L(ATI, R_CPTR)
    a.C(0o10, K_ZERO); a.C(ATX, C_RUN)
    a.C(0o10, K_ZERO); a.L(ATI, R_TOK)


def emit_next(a):
    """NEXTCHAR: link M[9]. In: C_CURW next byte in byte0, C_RUN pending spaces.
    Out: ACC = byte (0 at pad/end)."""
    a.mark('NEXT')
    a.C(0o10, C_RUN); a.C(AEX, K_ZERO); a.br(UZA, 'FETCH')
    a.C(0o10, C_RUN); a.C(ARX, K_NEGM1); a.C(ATX, C_RUN)
    a.C(0o10, K_SPACE); a.br(UJ, 'RET')
    a.mark('FETCH')
    a.C(0o10, C_CURW); a.C(ASX, K_SHR40); a.C(AAX, K_M8); a.C(ATX, C_CH)
    a.C(0o10, C_CURW); a.C(ASX, K_SHL8); a.C(ATX, C_CURW)
    a.C(0o10, C_CH); a.C(AEX, K_0A); a.br(UZA, 'END')
    a.C(0o10, C_CH); a.C(AEX, K_ZERO); a.br(UZA, 'END')
    a.C(0o10, C_CH); a.C(AAX, K_K80); a.C(AEX, K_K80); a.br(UZA, 'RUNSET')
    a.C(0o10, C_CH); a.br(UJ, 'RET')
    a.mark('RUNSET')
    a.C(0o10, C_CH); a.C(ARX, K_NEG81); a.C(ATX, C_RUN)
    a.C(0o10, K_SPACE); a.br(UJ, 'RET')
    a.mark('END')
    a.C(0o10, K_ZERO)
    a.mark('RET')
    a.E(ret_imm(R_LINK))


def emit_main(a):
    rearm(a)
    # ---- locate '=' ----
    a.mark('SCAN_WORD')
    a.L(0o10, 0o4012, R_CPTR)          # M[10]=0o60000 -> RAM 0o64012 (no UTC)
    a.C(ATX, C_CURW)
    a.C(0o10, K_ZERO); a.L(ATI, R_TOK)      # 6-byte counter in M[5]
    a.mark('SCAN_BYTE')
    a.C(0o10, C_CURW); a.C(ASX, K_SHR40); a.C(AAX, K_M8)
    a.C(AEX, K_NEG3D); a.br(UZA, 'FOUND')
    a.C(0o10, C_CURW); a.C(ASX, K_SHL8); a.C(ATX, C_CURW)
    a.mark('SCAN_CNT')
    a.L(ITA, R_TOK); a.C(ARX, K_ONE); a.L(ATI, R_TOK)
    a.L(ITA, R_TOK); a.C(AEX, K_SIX); a.br(UZA, 'NEXT_WORD')
    a.br(UJ, 'SCAN_BYTE')
    a.mark('NEXT_WORD')
    a.L(ITA, R_CPTR); a.C(ARX, K_ONE); a.L(ATI, R_CPTR)
    a.br(UJ, 'SCAN_WORD')
    a.mark('FOUND')
    a.L(0o10, 0o4012, R_CPTR); a.C(ATX, C_CURW)
    a.C(0o10, K_ZERO); a.C(ATX, C_RUN)
    a.C(0o10, K_ZERO); a.L(ATI, R_TOK)      # token index = 0
    # ---- skip leading spaces ----
    a.mark('SKIP_SP')
    a.call('NEXT'); a.C(ATX, C_CH)
    a.C(0o10, C_CH); a.C(AEX, K_SPACE); a.br(UZA, 'SKIP_SP')
    a.C(0o10, K_ZERO); a.C(ATX, C_PAY)
    a.C(0o10, K_ZERO); a.C(ATX, C_NAME)
    a.C(0o10, K_ZERO); a.C(ATX, C_LEN)
    # ---- identifier ----
    a.mark('IDENT_LOOP')
    a.C(0o10, C_CH); a.C(ARX, K_NEG20); a.C(ATX, C_TMP)
    a.C(0o10, C_NAME); a.C(ASX, K_SHL6); a.C(ARX, C_TMP); a.C(ATX, C_NAME)
    a.C(0o10, C_PAY); a.C(ASX, K_SHL8); a.C(ARX, C_CH); a.C(ATX, C_PAY)
    a.C(0o10, C_LEN); a.C(ARX, K_ONE); a.C(ATX, C_LEN)
    a.call('NEXT'); a.C(ATX, C_CH)
    a.C(0o10, C_CH); a.C(AAX, K_MASKC0); a.C(AEX, K_K40); a.br(UZA, 'IDENT_LOOP')
    # emit IDENT token: word A = (1<<40)|(LEN<<32)
    a.C(0o10, K_IDENT); a.C(ASX, K_SHL40); a.C(ATX, C_TMP)
    a.C(0o10, C_LEN); a.C(ASX, K_SHL32); a.C(ARX, C_TMP); a.C(ATX, C_TMP)
    a.T(ATX, 0); a.C(0o10, C_PAY); a.T(ATX, 1)
    a.L(ITA, R_TOK); a.C(ARX, K_ONE); a.C(ARX, K_ONE); a.L(ATI, R_TOK)
    # ---- '=' token (CH holds '=') ----
    a.C(0o10, C_CH); a.C(ASX, K_SHL40); a.T(ATX, 0)
    a.C(0o10, K_ZERO); a.T(ATX, 1)
    a.L(ITA, R_TOK); a.C(ARX, K_ONE); a.C(ARX, K_ONE); a.L(ATI, R_TOK)
    # ---- number ----
    a.call('NEXT'); a.C(ATX, C_CH)
    a.C(0o10, K_ZERO); a.C(ATX, C_PAY)
    a.C(0o10, K_ZERO); a.C(ATX, C_NDIG)
    a.mark('NUM_LOOP')
    a.C(0o10, C_CH); a.C(AEX, K_DOT); a.br(UZA, 'NUM_AFTER')
    a.C(0o10, C_PAY); a.C(ASX, K_SHL8); a.C(ARX, C_CH); a.C(ATX, C_PAY)
    a.C(0o10, C_NDIG); a.C(ARX, K_ONE); a.C(ATX, C_NDIG)
    a.mark('NUM_AFTER')
    a.call('NEXT'); a.C(ATX, C_CH)
    a.C(0o10, C_CH); a.C(AAX, K_MASKF0); a.C(AEX, K_K30); a.br(UZA, 'NUM_LOOP')
    a.C(0o10, C_CH); a.C(AEX, K_DOT); a.br(UZA, 'NUM_LOOP')
    # emit NUMBER token
    a.C(0o10, K_NUMBER); a.C(ASX, K_SHL40); a.C(ATX, C_TMP)
    a.C(0o10, C_NDIG); a.C(ASX, K_SHL32); a.C(ARX, C_TMP); a.C(ATX, C_TMP)
    a.T(ATX, 0); a.C(0o10, C_PAY); a.T(ATX, 1)
    # ---- handler: verify token kinds ----
    for off, exp, lab in ((0, KIND_IDENT, 'OK0'), (2, 0x3d, 'OK1'), (4, KIND_NUMBER, 'OK2')):
        a.E(long_(0o220, 0o20000))
        a.L(0o10, 0o1637 + TOKBASE + off)
        a.C(ASX, K_SHR40); a.C(AAX, K_M8); a.C(AEX, exp)
        a.br(UZA, lab); a.br(UJ, 'HALT'); a.mark(lab)
    # name word = C_NAME << shift[LEN] (indexed ASX via M[6]=LEN)
    a.C(0o10, C_LEN); a.L(ATI, R_RUN)
    a.C(0o10, C_NAME); a.C(ASX, K_LENTAB, reg=R_RUN); a.C(ATX, C_SYMNAME)
    # number payload -> float (docs/104 chain)
    a.C(0o10, C_PAY); a.C(ASX, K_SHR24); a.C(AAX, K_M8); a.C(ARX, K_PD0); a.C(AAX, K_M8); a.L(ATI, R_RUN)
    a.C(0o10, C_PAY); a.C(ASX, K_SHR16); a.C(AAX, K_M8); a.C(ARX, K_PD0); a.C(AAX, K_M8)
    a.L(ARX, FS.LO['T0'], reg=R_RUN)
    a.C(EPLUSX, K_EMASK); a.C(EPLUSX, K_C105); a.C(ATX, C_TMP)
    a.C(0o10, C_PAY); a.C(ASX, K_SHR8); a.C(AAX, K_M8); a.C(ARX, K_PD0); a.C(AAX, K_M8); a.L(ATI, R_RUN)
    a.C(0o10, C_PAY); a.C(AAX, K_M8); a.C(ARX, K_PD0); a.C(AAX, K_M8)
    a.L(ARX, FS.LO['T0'], reg=R_RUN)
    a.C(EPLUSX, K_EMASK); a.C(EPLUSX, K_C105); a.C(ATX, C_CH)
    a.C(0o10, C_TMP); a.C(MUL, K_HUNDRED); a.C(FADD, C_CH); a.C(ATX, C_SYMVAL)
    # symbol value -> /10 -> EST
    a.C(0o10, C_SYMVAL); a.Z(DIV, 'TEN'); a.Z(ATX, 'EST')
    # GOST seeds + converter
    a.C(0o10, K_GOSTA); a.L(ATX, 0o2006)
    a.C(0o10, K_GOSTB); a.L(ATX, 0o2007)
    a.call('CONV')
    a.E(UJ15)
    a.mark('HALT')
    a.E(UJ15)


def consts(body):
    return {
        K_ZERO:0, K_BASE:0o20000, K_CBASE:0o60000, K_ONE:1, K_SIX:6,
        K_M8:0o377, K_NEG20:(MASK-0x20)&MASK, K_NEG30:(MASK-0x30)&MASK,
        K_NEG3D:0x3d, K_NEG81:(MASK-0x81)&MASK, K_NEGM1:(MASK-1)&MASK,
        K_SHL8:(64-8)<<41, K_SHR40:(64+40)<<41, K_SHL6:(64-6)<<41,
        K_SHR24:(64+24)<<41, K_SHR16:(64+16)<<41, K_SHR8:(64+8)<<41,
        K_SHL40:(64-40)<<41, K_SHL32:(64-32)<<41,
        K_MASKC0:0xc0, K_MASKF0:0xf0, K_K40:0x40, K_K30:0x30, K_K80:0x80,
        K_DOT:0x2e, K_0A:0x0a, K_PD0:0xd0, K_EMASK:0o177<<41,
        K_C105:0o151<<41, K_HUNDRED:f32(100.0), K_SPACE:0x20,
        K_GOSTA:body[0o27], K_GOSTB:body[0o30],
        K_IDENT:KIND_IDENT, K_NUMBER:KIND_NUMBER,
        **{K_LENTAB+i:(64-6*(8-i))<<41 for i in range(8)},
    }


def build(case, src=None):
    src = Path(src) if src else WS / 'images/2048_base'
    dst = WS / 'images' / f'2048_{case}'
    shutil.copy2(src, dst)
    body = rz(str(dst), N + 1)
    body[0o11] = word(long_(0o300, N2_RAM0 + CODEBASE), DUMMY)
    body[0o27] = int.from_bytes(bytes([2, 1, 15, 15, 0, 0]), 'big')
    body[0o30] = int.from_bytes(bytes([0, 0, 14, 0, 0, 15]), 'big')
    body[0o31] = int.from_bytes(bytes([15, 3, 0, 0, 0, 14]), 'big')
    body[0o32] = int.from_bytes(bytes([0, 0, 0o231, 15, 15, 15]), 'big')
    v = FS.vals(); v['HALF'] = 0o20000
    for n, value in v.items():
        body[F.BODY0 + F.CELLS.index(n)] = value & MASK
    wz(str(dst), N + 1, body)

    n3_hw, floor_ram, conv_len, floor_len = CB.build_n3()
    wz(str(dst), Z3, CB.asm_words(n3_hw))

    a = Asm()
    emit_main(a)
    emit_next(a)
    a.resolve()
    hw = a.hw

    z2 = rz(str(dst), N2)
    for k, val in consts(body).items():
        z2[k] = val & MASK
    z2[C_RUN] = 0
    for i in range((len(hw) + 1) // 2):
        z2[CODEBASE + i] = word(hw[2*i], hw[2*i+1] if 2*i+1 < len(hw) else DUMMY)
    wz(str(dst), N2, z2)
    sha = hashlib.sha256(dst.read_bytes()).hexdigest()
    print(f'case={case} sha={sha} N3={len(n3_hw)//2}/{MAX_WORDS}w '
          f'conv={conv_len}hw floor={floor_len}hw N2code={len(hw)}hw '
          f'({(len(hw)+1)//2} words) labels={len(a.labels)}')
    return dst, sha


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--build')
    ap.add_argument('--src')
    a = ap.parse_args()
    if a.build:
        build(a.build, a.src)
