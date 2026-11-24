#!/usr/bin/env python3
"""B5 INTEGRATION: a machine-code lexer reads REAL fixed-form Fortran text from
the card buffer at RAM 0o64012, emits the B2 one-word token stream into N+2[64..]
together with machine-derived literal floats, then hands control to the VERBATIM
B4 shunting-yard parser + B3 print path (N+3 verbatim GOST converter).

Everything numeric is derived by BESM-6 instructions from the Fortran digits in
the deck.  No 777005 IR cards, no fixtures for the expression, no host values.

Reused verbatim:
  * parser_build.build_parser (B4 shunting-yard + B3 dispatcher + print),
  * c6_build.build_n3 (docs/105 GOST converter in N+3),
  * c7_build.width_tables, final_sign.CELLS/LO (low-RAM converter cells),
  * DB.tok() B2 token encoder and the B4 constant layout.

Copies only: workspace /tmp/.private/azizz/opencode/b5-source-expr.
"""
import argparse, hashlib, shutil, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import c6_build as C6
import c7_build as C7
import final_sign as FS
import dispatch_build as DB
import parser_build as PB
from build_e2e import rz, wz, short, long_, word, f32, MASK, N, Z3, MAX_WORDS

WS = HERE.parent
N2 = N + 2
N2_RAM0 = 0o21637          # N+2 offsets 0..525
TAIL_RAM0 = 0o27721        # N+2 offsets 901..1023 (docs/110 line 72)
CONV_RAM0 = 0o30114
B4_RAM = N2_RAM0 + PB.CODE_OFF       # 0o22243, B4 parser entry

# opcodes
ATX, AAX, AEX, ARX, ASX = 0o00, 0o11, 0o12, 0o13, 0o26
ADD, FSUB, DIV, MUL = 0o04, 0o06, 0o16, 0o17
ATI, ITA, UJ, UZA, E24 = 0o40, 0o42, 0o300, 0o260, 0o24
DUMMY = C6.DUMMY

TOKBASE = 64
LITBASE = 100

# ---------------- N+2 DATA cells (low band 2..61, never 33) ----------------
L_SHRTAB = 2       # 2..7 : six byte-shift controls for card bytes 0..5
L_M8      = 8
L_ONE     = 9
L_SIX     = 10
L_NEG1    = 11
L_0X30    = 12
L_DOT     = 13
L_PLUS    = 14
L_MINUS   = 15
L_STAR    = 16
L_SLASH   = 17
L_LPC     = 18
L_RPC     = 19
L_EQ      = 20
L_0X80    = 21
L_0X0A    = 22
L_EMASK   = 23
L_C105    = 24
L_TEN     = 25
L_ZERO    = 26
L_CBASE   = 27
L_64      = 28
L_100     = 29
L_0X20    = 30
L_SHL42   = 31
L_0XF0    = 32
# 33 is the symbol VALUE word (owned by B4) - skipped
L_CSPROG  = 34
L_CSREAL  = 35
L_CSX     = 36
L_CSEQ    = 37
L_CSEOL   = 38
L_CSPRINT = 39
L_CSFD    = 40
L_CSEND   = 41
L_TOKLIT  = 42
L_TOKOP   = 43
L_TOKLP   = 44
L_TOKRP   = 45
L_OP1     = 46
L_OP2     = 47
L_OP3     = 48
L_OP4     = 49
C_CURW    = 50
C_CH      = 51
C_PREV    = 52
C_TOKPTR  = 53
C_POOLPTR = 54
C_F       = 55
C_DF      = 56
C_SEEDOT  = 57
C_NFRAC   = 58
C_NAME    = 59
C_TMP     = 60
C_TMP2    = 61
C_MODE    = 62
L_TWO     = 63
L_NEG30   = 96       # (unused) kept for slot stability
L_0X0F    = 97       # low-nibble mask: ASCII digit 0x3d -> digit d directly

# code regions (free N+2 low-band words + tail band). Long branches reach all.
CODE_REGIONS = [(901, 1023), (162, 199), (245, 259), (463, 525)]


def tail_ram(off):
    return TAIL_RAM0 + (off - 901)


def ram_of(off):
    return tail_ram(off) if off >= 901 else (N2_RAM0 + off)


class LAsm:
    """Assembler for LEX: operand cells via reg12 (low band), branches LONG/abs."""
    def __init__(self):
        self.hw = []
        self.labels = {}
        self.branches = []
        self.slots = []
        for a, b in CODE_REGIONS:
            self.slots.extend(range(a, b + 1))
        self.wordidx = 0

    def E(self, x):
        self.hw.append(x & 0xffffff)

    def L(self, op, adr, reg=0):
        self.E(short(op, adr, reg=reg))

    def C(self, op, off, reg=12):
        self.L(op, 0o1637 + off, reg=reg)

    def Z(self, op, name):
        self.L(op, FS.LO[name])

    def mark(self, name):
        if len(self.hw) % 2:
            self.E(DUMMY)
        self.labels[name] = len(self.hw)

    def br(self, op, name):
        i = len(self.hw)
        self.E(long_(op, 0))
        self.branches.append((i, name, op))
        return i

    def resolve(self):
        for i, name, op in self.branches:
            hwidx = self.labels[name]
            off = self.slots[hwidx // 2]
            ram = ram_of(off) + (hwidx % 2)
            self.hw[i] = long_(op, ram)
        if len(self.hw) % 2:
            self.E(DUMMY)
        assert (len(self.hw) + 1) // 2 <= len(self.slots), \
            f'LEX code overrun: {len(self.hw)//2} words > {len(self.slots)}'

    def code_words(self):
        return [(self.slots[i], word(self.hw[2*i], self.hw[2*i+1]))
                for i in range((len(self.hw) + 1) // 2)]


def rearm_lex(a):
    a.Z(0o10, 'HALF'); a.L(ATI, 12)          # M[12] = 0o20000 (N+2 low band)
    a.Z(0o10, 'HALF'); a.L(ATI, 7)           # M[7]  = 0o20000
    a.C(0o10, L_CBASE); a.L(ATI, 10)         # M[10] = 0o60000 (card pointer)
    a.C(0o10, L_ZERO); a.L(ATI, 11)          # byte index = 0 (proven B1 pattern)
    a.L(0o10, 0o4012, 10); a.C(ATX, C_CURW)  # load first card word 0o64012


def getch(a, ret):
    """Fetch next card byte into C_CH; advance M[11]/M[10] as needed; -> ret."""
    a.mark('_GETCH_' + ret)
    a.L(ITA, 11); a.C(AEX, L_SIX)
    a.br(UZA, '_NEXTW_' + ret)
    a.C(0o10, C_CURW)
    a.E(long_(0o220, 0o20000))
    a.C(ASX, L_SHRTAB, reg=11)
    a.C(AAX, L_M8)
    a.C(ATX, C_CH)
    a.L(ITA, 11); a.C(ARX, L_ONE); a.L(ATI, 11)
    a.br(UJ, ret)
    a.mark('_NEXTW_' + ret)
    a.L(ITA, 10); a.C(ARX, L_ONE); a.L(ATI, 10)
    a.L(0o10, 0o4012, 10)
    a.C(ATX, C_CURW)
    a.C(0o10, L_ZERO); a.L(ATI, 11)
    a.br(UJ, '_GETCH_' + ret)


def emit_tok(a):
    """ACC (token word) -> N+2[TOKPTR], TOKPTR++."""
    a.C(ATX, C_TMP)
    a.C(0o10, C_TOKPTR); a.L(ATI, 6)
    a.C(0o10, C_TMP)
    a.E(long_(0o220, 0o20000))
    a.L(ATX, 0o1637 + TOKBASE, reg=6)
    a.C(0o10, C_TOKPTR); a.C(ARX, L_ONE); a.C(ATX, C_TOKPTR)


def emit_const(a, cell):
    a.C(0o10, cell)
    emit_tok(a)


def build_lex():
    a = LAsm()
    rearm_lex(a)
    # token/pool pointers are RELATIVE indices (ADR already carries the base)
    a.C(0o10, L_ZERO); a.C(ATX, C_TOKPTR)
    a.C(0o10, L_ZERO); a.C(ATX, C_POOLPTR)
    a.C(0o10, L_ZERO); a.C(ATX, C_MODE)

    # ---- scaffolding keywords (PROGRAM MAIN / REAL X / EOL) ----
    for c in (L_CSPROG, L_CSX, L_CSREAL, L_CSX, L_CSEOL):
        emit_const(a, c)

    # ---- unified character loop ----
    a.mark('MAIN_LOOP')
    getch(a, 'DISPATCH')
    a.mark('DISPATCH')
    a.C(0o10, C_MODE); a.br(UZA, 'M_SCAN')
    a.C(0o10, C_MODE); a.C(AEX, L_ONE); a.br(UZA, 'M_EXPR')
    a.br(UJ, 'M_NUM')

    # ---- mode 0: scan source for '=' ----
    a.mark('M_SCAN')
    a.C(0o10, C_CH); a.C(AEX, L_EQ); a.br(UZA, 'FOUND_EQ')
    a.C(0o10, C_CH); a.C(ATX, C_PREV)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('FOUND_EQ')
    a.C(0o10, C_PREV); a.C(ARX, L_0X20)   # ASCII - 0x20 -> 6-bit code
    a.C(ASX, L_SHL42); a.C(ATX, C_NAME)
    a.C(0o10, C_NAME); a.C(ATX, 1)         # symbol name word N+2[1]
    emit_const(a, L_CSX)                   # assignment ID (VIDX=1)
    emit_const(a, L_CSEQ)
    a.C(0o10, L_ONE); a.C(ATX, C_MODE)     # mode 1 = expression
    a.br(UJ, 'MAIN_LOOP')

    # ---- mode 1: expression tokens ----
    a.mark('M_EXPR')
    a.C(0o10, C_CH); a.C(AAX, L_0XF0); a.C(AEX, L_0X30)
    a.br(UZA, 'EXPR_DIGIT')
    a.C(0o10, C_CH); a.C(AEX, L_PLUS);  a.br(UZA, 'EX_PLUS')
    a.C(0o10, C_CH); a.C(AEX, L_MINUS); a.br(UZA, 'EX_MINUS')
    a.C(0o10, C_CH); a.C(AEX, L_STAR);  a.br(UZA, 'EX_STAR')
    a.C(0o10, C_CH); a.C(AEX, L_SLASH); a.br(UZA, 'EX_SLASH')
    a.C(0o10, C_CH); a.C(AEX, L_LPC);   a.br(UZA, 'EX_LP')
    a.C(0o10, C_CH); a.C(AEX, L_RPC);   a.br(UZA, 'EX_RP')
    a.C(0o10, C_CH); a.C(AEX, L_0X0A);  a.br(UZA, 'EX_END')
    a.C(0o10, C_CH); a.C(AAX, L_0X80); a.C(AEX, L_0X80)
    a.br(UZA, 'EX_END')
    a.br(UJ, 'MAIN_LOOP')                 # ignore other chars (spaces, letters)
    a.mark('EXPR_DIGIT')
    a.C(0o10, L_ZERO); a.C(ATX, C_F)
    # NFRAC is biased by 100 so its zero test never sees one's-complement -0
    a.C(0o10, L_100); a.C(ATX, C_NFRAC)
    a.C(0o10, L_ZERO); a.C(ATX, C_SEEDOT)
    a.C(0o10, L_TWO); a.C(ATX, C_MODE)     # mode 2 = number
    a.br(UJ, 'M_NUM')                      # process the SAME digit (no refetch)

    # ---- mode 2: accumulate a real literal ----
    a.mark('M_NUM')
    a.C(0o10, C_CH); a.C(AAX, L_0XF0); a.C(AEX, L_0X30)
    a.br(UZA, 'NUM_DIGIT')
    a.C(0o10, C_CH); a.C(AEX, L_DOT); a.br(UZA, 'NUM_DOT')
    a.C(0o10, L_ONE); a.C(ATX, C_MODE)    # back to expression, re-dispatch char
    a.br(UJ, 'NUM_FINISH')
    a.mark('NUM_DOT')
    a.C(0o10, L_ONE); a.C(ATX, C_SEEDOT)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('NUM_DIGIT')
    a.C(0o10, C_CH); a.C(AAX, L_0X0F); a.C(ATX, C_TMP2)   # ASCII low nibble = digit
    a.C(0o10, C_SEEDOT); a.br(UZA, 'NUM_NOFRAC')
    a.C(0o10, C_NFRAC); a.C(ARX, L_ONE); a.C(ATX, C_NFRAC)
    a.mark('NUM_NOFRAC')
    # integer digit -> BESM float via the proven docs/104 e+x normalisation
    a.C(0o10, C_TMP2); a.Z(E24, 'EMASK'); a.Z(E24, 'C105')
    a.C(ATX, C_DF)
    a.C(0o10, C_F); a.C(MUL, L_TEN); a.C(ADD, C_DF); a.C(ATX, C_F)
    a.br(UJ, 'MAIN_LOOP')

    # ---- finalize literal: F / 10**nfrac -> pool, LIT token ----
    a.mark('NUM_FINISH')
    a.mark('NUM_DIV_LOOP')
    a.C(0o10, C_NFRAC); a.C(AEX, L_100); a.br(UZA, 'NUM_STORE')
    a.C(0o10, C_F); a.C(DIV, L_TEN); a.C(ATX, C_F)
    a.C(0o10, C_NFRAC); a.C(ARX, L_NEG1); a.C(ATX, C_NFRAC)
    a.br(UJ, 'NUM_DIV_LOOP')
    a.mark('NUM_STORE')
    a.C(0o10, C_F); a.C(ATX, C_TMP)
    a.C(0o10, C_POOLPTR); a.L(ATI, 6)
    a.C(0o10, C_TMP)
    a.E(long_(0o220, 0o20000))
    a.L(ATX, 0o1637 + LITBASE, reg=6)
    a.C(0o10, C_POOLPTR)              # relative pool index = LIT PAY
    a.C(AEX, L_TOKLIT)                # bitwise OR (disjoint fields) via XOR
    emit_tok(a)
    a.C(0o10, C_POOLPTR); a.C(ARX, L_ONE); a.C(ATX, C_POOLPTR)
    a.br(UJ, 'DISPATCH')

    # ---- operator / parenthesis tokens ----
    a.mark('EX_PLUS')
    emit_const(a, L_OP1); a.br(UJ, 'MAIN_LOOP')
    a.mark('EX_MINUS')
    emit_const(a, L_OP2); a.br(UJ, 'MAIN_LOOP')
    a.mark('EX_STAR')
    emit_const(a, L_OP3); a.br(UJ, 'MAIN_LOOP')
    a.mark('EX_SLASH')
    emit_const(a, L_OP4); a.br(UJ, 'MAIN_LOOP')
    a.mark('EX_LP')
    emit_const(a, L_TOKLP); a.br(UJ, 'MAIN_LOOP')
    a.mark('EX_RP')
    emit_const(a, L_TOKRP); a.br(UJ, 'MAIN_LOOP')

    # ---- end of statement: tail tokens, then hand off to B4 ----
    a.mark('EX_END')
    for c in (L_CSEOL, L_CSPRINT, L_CSFD, L_CSX, L_CSEOL, L_CSEND):
        emit_const(a, c)
    a.E(long_(0o300, B4_RAM))
    a.resolve()
    return a


def sub_const(d):
    return (MASK - d) & MASK


def lex_consts():
    c = {
        L_SHRTAB + 0: (64 + 40) << 41,
        L_SHRTAB + 1: (64 + 32) << 41,
        L_SHRTAB + 2: (64 + 24) << 41,
        L_SHRTAB + 3: (64 + 16) << 41,
        L_SHRTAB + 4: (64 + 8) << 41,
        L_SHRTAB + 5: (64 + 0) << 41,
        L_M8: 0xff, L_ONE: 1, L_SIX: 6, L_NEG1: sub_const(1),
        L_0X30: 0x30, L_NEG30: sub_const(0x30), L_0X0F: 0x0f,
        L_DOT: 0x2e, L_PLUS: 0x2b, L_MINUS: 0x2d,
        L_STAR: 0x2a, L_SLASH: 0x2f, L_LPC: 0x28, L_RPC: 0x29,
        L_EQ: 0x3d, L_0X80: 0x80, L_0X0A: 0x0a,
        L_EMASK: 0o177 << 41, L_C105: 0o151 << 41,
        L_TEN: f32(10.0), L_ZERO: 0, L_CBASE: 0o60000,
        L_64: 64, L_100: 100, L_0X20: sub_const(0x20), L_TWO: 2,
        L_SHL42: (64 - 42) << 41, L_0XF0: 0xf0,
        L_CSPROG: DB.tok(10, 30), L_CSREAL: DB.tok(10, 31),
        L_CSX: DB.tok(2, 0, 0, 1), L_CSEQ: DB.tok(8), L_CSEOL: DB.tok(11),
        L_CSPRINT: DB.tok(10, 34), L_CSFD: DB.tok(13, 1, 0, (4 << 8) | 2),
        L_CSEND: DB.tok(10, 37),
        L_TOKLIT: DB.tok(1), L_TOKOP: DB.tok(3),
        L_TOKLP: DB.tok(6, 1), L_TOKRP: DB.tok(6, 2),
        L_OP1: DB.tok(3, 1), L_OP2: DB.tok(3, 2),
        L_OP3: DB.tok(3, 3), L_OP4: DB.tok(3, 4),
        C_CURW: 0, C_CH: 0, C_PREV: 0, C_TOKPTR: 0, C_POOLPTR: 0,
        C_F: 0, C_DF: 0, C_SEEDOT: 0, C_NFRAC: 0, C_NAME: 0,
        C_TMP: 0, C_TMP2: 0, C_MODE: 0,
    }
    return c


def build(case, patch=0.0, src=None, lex_code=None):
    src = Path(src) if src else WS / 'images/2048_base'
    dst = WS / 'images' / f'2048_{case}'
    shutil.copy2(src, dst)

    # ---- body N+1 (GOST seeds + converter low-RAM cells) ----
    body = rz(str(dst), N + 1)
    body[0o11] = word(long_(0o300, tail_ram(901)), 0)  # contour entry -> LEX
    body[0o27] = int.from_bytes(bytes([2, 1, 15, 15, 0, 0]), 'big')
    body[0o30] = int.from_bytes(bytes([0, 0, 14, 0, 0, 15]), 'big')
    body[0o31] = int.from_bytes(bytes([15, 3, 0, 0, 0, 14]), 'big')
    body[0o32] = int.from_bytes(bytes([0, 0, 0o231, 15, 15, 15]), 'big')
    for n, value in C6.vals().items():
        body[0o110 + FS.CELLS.index(n)] = value & MASK
    wz(str(dst), N + 1, body)

    # ---- N+3 verbatim converter ----
    n3_hw, floor_ram, conv_len, floor_len = C6.build_n3()
    wz(str(dst), Z3, C6.asm_words(n3_hw))

    # ---- N+2 ----
    z2 = rz(str(dst), N2)
    z2[1] = C6.C2.text_word('X       ') & MASK   # symbol name (LEX overwrites)
    z2[33] = f32(0.0)                            # symbol value (B4 writes)
    for i in range(4):
        z2[LITBASE + i] = f32(0.0)               # LEX overwrites from digits
    wm, cm, sm = C7.width_tables()
    dconsts = {
        PB.K_BASE: 0o20000, PB.K_ONE: 1,
        PB.K_MTK: 0o7700000000000000, PB.K_MSUB: 0o0077000000000000,
        PB.K_MPAY: 0o0000000077777777,
        PB.K_SR42: (64 + 42) << 41, PB.K_SR36: (64 + 36) << 41,
        PB.K_SR8: (64 + 8) << 41, PB.K_255: 0o377, PB.K_ZERO: 0,
        PB.K_TK10: 10, PB.K_TK2: 2, PB.K_TK11: 11, PB.K_TK12: 12, PB.K_TK13: 13,
        PB.K_SUB30: 30, PB.K_SUB31: 31, PB.K_SUB34: 34, PB.K_SUB37: 37,
        PB.K_GOSTA: body[0o27], PB.K_GOSTB: body[0o30],
        PB.K_NEG1: MASK ^ 1, PB.K_TEN: f32(10.0), PB.K_PATCH: f32(patch),
        PB.K_OPADD: 1, PB.KOPSUB: 2, PB.KOPMUL: 3, PB.KOPDIV: 4,
        PB.K_TKLIT: 1, PB.K_TKOP: 3, PB.K_TKLP: 6, PB.K_MODE2: 2,
        PB.K_BIAS: 100,
        # B4 parser constants also referenced by its code:
        PB.C_TOK: 0, PB.C_TK: 0, PB.C_SUB: 0, PB.C_PAY: 0,
        PB.C_OP: 0, PB.C_A: 0, PB.C_B: 0, PB.C_TOP: 0,
        PB.C_SPO: 0, PB.C_SPP: 0, PB.C_MODE: 0,
        PB.C_PUSHVAL: 0,
        PB.K_PRINT_BIAS: f32(0.0),
    }
    for off, v in zip(range(PB.K_WMASK0, PB.K_WMASK0 + 3), wm):
        dconsts[off] = v
    for off, v in zip(range(PB.K_CLEARM0, PB.K_CLEARM0 + 2), cm):
        dconsts[off] = v
    for off, v in zip(range(PB.K_SPACEM0, PB.K_SPACEM0 + 2), sm):
        dconsts[off] = v
    for off, v in dconsts.items():
        z2[off] = v & MASK

    # B4 parser code verbatim
    n2, labels = PB.build_parser(CONV_RAM0)
    for i in range(len(n2.hw) // 2):
        z2[PB.CODE_OFF + i] = word(n2.hw[2*i], n2.hw[2*i+1])
    if len(n2.hw) % 2:
        z2[PB.CODE_OFF + len(n2.hw)//2] = word(n2.hw[-1], DUMMY)

    # LEX data + code
    for off, v in lex_consts().items():
        z2[off] = v & MASK
    a = lex_code or build_lex()
    for off, w in a.code_words():
        z2[off] = w & MASK

    wz(str(dst), N2, z2)
    sha = hashlib.sha256(dst.read_bytes()).hexdigest()
    n2used = max(off for off, _ in a.code_words()) + 1
    print(f'case={case} sha={sha} N3={len(n3_hw)//2}/{MAX_WORDS}w '
          f'LEX={len(a.hw)}hw ({(len(a.hw)+1)//2}w) '
          f'B4={len(n2.hw)//2}hw ({len(n2.hw)//2}w) '
          f'LEXentry={tail_ram(901):06o} N2last={n2used}/1024 patch={patch}')
    return dst, sha, len(n3_hw)//2, len(a.hw)//2, n2used


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--build', required=True)
    ap.add_argument('--patch', type=float, default=0.0)
    ap.add_argument('--src')
    a = ap.parse_args()
    build(a.build, patch=a.patch, src=a.src)
