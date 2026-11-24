#!/usr/bin/env python3
"""FINAL INTEGRATED VARIANT-B builder.

ONE image whose deck is REAL fixed-form Fortran source:
  * assignment with expression, precedence and parentheses (verbatim B4 shunting-yard from B5)
  * PRINT n,X with labelled FORMAT(1X,Fw.d) parsed from the source text (B6a idea, single pass)
  * SQRT by name (B6b Newton routine, adapted to B5's pool convention)

Reused verbatim: parser_build.build_parser (B4 evaluator + B3 dispatcher + print),
c6_build N+3 converter, c7_build width tables, final_sign low-RAM cells,
build_e2e zone I/O.  No fixture tokens, no 777005 IR card, no host result digit.
"""
import argparse, hashlib, shutil, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import b5_build as B5
import parser_build as PB
import c6_build as C6
import c7_build as C7
import final_sign as FS
from build_e2e import rz, wz, short, long_, word, f32, MASK, N, Z3

WS = HERE.parent
N2 = N + 2
N2_RAM0 = 0o21637
CONV_RAM0 = 0o30114
B4_RAM = N2_RAM0 + PB.CODE_OFF

ATX, AAX, AEX, ARX, ASX = 0o00, 0o11, 0o12, 0o13, 0o26
ADD, FSUB, DIV, MUL = 0o04, 0o06, 0o16, 0o17
ATI, ITA, UJ, UZA = 0o40, 0o42, 0o300, 0o260
DUMMY = C6.DUMMY
UTC_N2 = long_(0o220, 0o20000)
LINK = 5

def tail_ram(off): return B5.tail_ram(off)

# ---------------------------------------------------------------- new data map
# Free token slots 82..95 (our programs emit <= 22 tokens) and B4 scratch cells
# 104..107 / 110..112 / 142 (B4 rewrites them before use).
C_PAY=82; C_WIN3=83; C_WIN5=84; C_WIN6=85; C_FDESC_IDX=86; C_INTR=87
C_SQX=88; L_TXT_PRINT=89; L_TXT_FORMAT=90; L_TXT_END=91
L_MASK3=92; L_MASK5=93; L_SHL8=94; L_CH_S=95
L_HALF=104; L_THREE=105; L_FOUR=106; L_CH_F=107
C_NAMED=110; L_TOKFD=142; L_COMMA=143
L_FIVE=144; L_SEVEN=145

# B5 data cells (kept)
L_=B5
C_CURW=L_.C_CURW; C_CH=L_.C_CH; C_PREV=L_.C_PREV; C_TOKPTR=L_.C_TOKPTR
C_POOLPTR=L_.C_POOLPTR; C_F=L_.C_F; C_DF=L_.C_DF; C_SEEDOT=L_.C_SEEDOT
C_NFRAC=L_.C_NFRAC; C_TMP=L_.C_TMP; C_TMP2=L_.C_TMP2; C_MODE=L_.C_MODE
L_SHRTAB=L_.L_SHRTAB; L_M8=L_.L_M8; L_ONE=L_.L_ONE; L_SIX=L_.L_SIX
L_NEG1=L_.L_NEG1; L_0X30=L_.L_0X30; L_DOT=L_.L_DOT; L_PLUS=L_.L_PLUS
L_MINUS=L_.L_MINUS; L_STAR=L_.L_STAR; L_SLASH=L_.L_SLASH; L_LPC=L_.L_LPC
L_RPC=L_.L_RPC; L_EQ=L_.L_EQ; L_0X80=L_.L_0X80; L_0X0A=L_.L_0X0A
L_EMASK=L_.L_EMASK; L_C105=L_.L_C105; L_TEN=L_.L_TEN; L_ZERO=L_.L_ZERO
L_CBASE=L_.L_CBASE; L_100=L_.L_100; L_0X20=L_.L_0X20; L_TWO=L_.L_TWO
L_SHL42=L_.L_SHL42; L_0XF0=L_.L_0XF0; L_0X0F=L_.L_0X0F
L_CSPROG=L_.L_CSPROG; L_CSREAL=L_.L_CSREAL; L_CSX=L_.L_CSX
L_CSEQ=L_.L_CSEQ; L_CSEOL=L_.L_CSEOL; L_CSPRINT=L_.L_CSPRINT
L_TOKLIT=L_.L_TOKLIT; L_OP1=L_.L_OP1; L_OP2=L_.L_OP2; L_OP3=L_.L_OP3
L_OP4=L_.L_OP4; L_TOKLP=L_.L_TOKLP; L_TOKRP=L_.L_TOKRP; L_CSEND=L_.L_CSEND

CODE_REGIONS = [(901, 1023), (162, 199), (245, 259), (463, 525)]

def vjm_imm(addr, reg=LINK):
    return (reg << 20) | (0o31 << 15) | (addr & 0o77777)

class LAsm(B5.LAsm):
    def __init__(self):
        super().__init__()
        self.calls = []
        self.ends = {b for _, b in CODE_REGIONS}
    def E(self, x):
        wi = len(self.hw) // 2
        if (len(self.hw) % 2 == 0 and wi < len(self.slots)
                and self.slots[wi] in self.ends and wi + 1 < len(self.slots)):
            # The free N+2 bands are not adjacent.  Never let straight-line
            # execution fall off the end of one band into the next, which
            # contains data or the forbidden zone.
            nxt = self.slots[wi + 1]
            ram = tail_ram(nxt) if nxt >= 901 else (N2_RAM0 + nxt)
            self.hw.append(long_(UJ, ram) & MASK)
            self.hw.append(DUMMY)
        self.hw.append(x & 0xffffff)
    def mark(self, name):
        while len(self.hw) % 2:
            self.E(DUMMY)
        self.labels[name] = len(self.hw)
    def call(self, name):
        i = len(self.hw)
        self.E(vjm_imm(0))
        if i % 2 == 0:
            self.E(DUMMY)
        self.calls.append((i, name))
        return i
    def ret(self):
        self.L(UJ, 0, reg=LINK)
    def ram_of_label(self, name):
        hwidx = self.labels[name]
        off = self.slots[hwidx // 2]
        base = tail_ram(off) if off >= 901 else (N2_RAM0 + off)
        return base + (hwidx % 2)
    def resolve(self):
        B5.LAsm.resolve(self)
        for i, name in self.calls:
            self.hw[i] = vjm_imm(self.ram_of_label(name))

# ------------------------------------------------------------------ subroutines
def emit_getch(a):
    a.mark('GETCH')
    a.L(ITA, 11); a.C(AEX, L_SIX)
    a.br(UZA, 'GC_NEXTW')
    a.C(0o10, C_CURW); a.E(UTC_N2)
    a.C(ASX, L_SHRTAB, reg=11); a.C(AAX, L_M8); a.C(ATX, C_CH)
    a.L(ITA, 11); a.C(ARX, L_ONE); a.L(ATI, 11)
    a.ret()
    a.mark('GC_NEXTW')
    a.L(ITA, 10); a.C(ARX, L_ONE); a.L(ATI, 10)
    a.L(0o10, 0o4012, 10); a.C(ATX, C_CURW)
    a.C(0o10, L_ZERO); a.L(ATI, 11)
    a.br(UJ, 'GETCH')              # re-enter and fetch from the new word

def emit_emit(a):
    a.mark('EMIT')
    a.C(ATX, C_TMP)
    a.C(0o10, C_TOKPTR); a.L(ATI, 6)
    a.C(0o10, C_TMP)
    a.E(UTC_N2); a.L(ATX, 0o1637 + B5.TOKBASE, reg=6)
    a.C(0o10, C_TOKPTR); a.C(ARX, L_ONE); a.C(ATX, C_TOKPTR)
    a.ret()

def ec(a, cell):
    a.C(0o10, cell); a.call('EMIT')

# ------------------------------------------------------------------ sliding windows
def kwindow(a, found_print, found_format, found_end):
    a.C(0o10, C_WIN3); a.C(ASX, L_SHL8); a.C(ARX, C_CH)
    a.C(AAX, L_MASK3); a.C(ATX, C_WIN3)
    a.C(0o10, C_WIN5); a.C(ASX, L_SHL8); a.C(ARX, C_CH)
    a.C(AAX, L_MASK5); a.C(ATX, C_WIN5)
    a.C(0o10, C_WIN6); a.C(ASX, L_SHL8); a.C(ARX, C_CH); a.C(ATX, C_WIN6)
    a.C(0o10, C_WIN6); a.C(AEX, L_TXT_FORMAT); a.br(UZA, found_format)
    a.C(0o10, C_WIN5); a.C(AEX, L_TXT_PRINT);  a.br(UZA, found_print)
    a.C(0o10, C_WIN3); a.C(AEX, L_TXT_END);    a.br(UZA, found_end)

def skip_ws(a, lbl):
    a.C(0o10, C_CH); a.C(AEX, L_0X0A); a.br(UZA, lbl)
    a.C(0o10, C_CH); a.C(AAX, L_0X80); a.C(AEX, L_0X80); a.br(UZA, lbl)

def is_digit(a, lbl):
    a.C(0o10, C_CH); a.C(AAX, L_0XF0); a.C(AEX, L_0X30); a.br(UZA, lbl)

def reset_windows(a):
    a.C(0o10, L_ZERO); a.C(ATX, C_WIN3); a.C(ATX, C_WIN5); a.C(ATX, C_WIN6)

# ------------------------------------------------------------------ main LEX
def build_lex():
    a = LAsm()
    emit_getch(a)
    emit_emit(a)
    a.mark('START')
    # base registers / card pointer
    a.Z(0o10, 'HALF'); a.L(ATI, 12)
    a.Z(0o10, 'HALF'); a.L(ATI, 7)
    a.C(0o10, L_CBASE); a.L(ATI, 10)
    a.L(0o10, 0o4012, 10); a.C(ATX, C_CURW)
    a.C(0o10, L_ZERO); a.L(ATI, 11)
    # pointers, modes, windows, intrinsic flags
    a.C(ATX, C_TOKPTR); a.C(ATX, C_POOLPTR); a.C(ATX, C_MODE)
    a.C(ATX, C_INTR); a.C(ATX, C_NAMED); a.C(ATX, C_PAY)
    reset_windows(a)
    # scaffolding: PROGRAM, name, REAL, X, EOL
    for c in (L_CSPROG, L_CSX, L_CSREAL, L_CSX, L_CSEOL):
        ec(a, c)

    a.mark('MAIN_LOOP')
    a.call('GETCH')
    a.mark('DISPATCH')
    a.C(0o10, C_MODE); a.br(UZA, 'M_SCAN')
    a.C(0o10, C_MODE); a.C(AEX, L_ONE); a.br(UZA, 'M_EXPR')
    a.C(0o10, C_MODE); a.C(AEX, L_TWO); a.br(UZA, 'M_NUM')
    a.C(0o10, C_MODE); a.C(AEX, L_THREE); a.br(UZA, 'M_PLAB')
    a.C(0o10, C_MODE); a.C(AEX, L_FOUR); a.br(UZA, 'M_S4')
    a.C(0o10, C_MODE); a.C(AEX, L_FIVE); a.br(UZA, 'M_S5')
    a.C(0o10, C_MODE); a.C(AEX, L_SIX); a.br(UZA, 'M_S6')
    a.br(UJ, 'M_S7')

    # ---- mode 0: scan source ----
    a.mark('M_SCAN')
    a.C(0o10, C_CH); a.C(AEX, L_EQ); a.br(UZA, 'FOUND_EQ')
    skip_ws(a, 'MAIN_LOOP')
    kwindow(a, 'FOUND_PRINT', 'FOUND_FORMAT', 'FOUND_END')
    a.C(0o10, C_CH); a.C(ATX, C_PREV)
    a.br(UJ, 'MAIN_LOOP')

    # ---- assignment '=' ----
    a.mark('FOUND_EQ')
    a.C(0o10, C_PREV); a.C(ARX, L_0X20)
    a.C(ASX, L_SHL42); a.C(ATX, C_TMP)
    a.C(0o10, C_TMP); a.C(ATX, 1)
    ec(a, L_CSX); ec(a, L_CSEQ)
    a.C(0o10, L_ONE); a.C(ATX, C_MODE)
    a.br(UJ, 'MAIN_LOOP')

    # ---- mode 1: expression tokens ----
    a.mark('M_EXPR')
    is_digit(a, 'EXPR_DIGIT')
    # SQRT name recognition: initial byte S sets C_INTR; the rest of the name
    # and the opening parenthesis are ignored until the first digit arrives.
    a.C(0o10, C_INTR); a.br(UZA, 'EX_NOSQ')
    a.br(UJ, 'MAIN_LOOP')          # inside SQRT name / before its first digit
    a.mark('EX_NOSQ')
    a.C(0o10, C_NAMED); a.br(UZA, 'EX_CHKS')
    a.br(UJ, 'EX_OPCHK')           # name already consumed: normal expression
    a.mark('EX_CHKS')
    a.C(0o10, C_CH); a.C(AEX, L_CH_S); a.br(UZA, 'EX_GOTSQ')
    a.br(UJ, 'EX_OPCHK')
    a.mark('EX_GOTSQ')
    a.C(0o10, L_TWO); a.C(ATX, C_INTR)
    a.C(0o10, L_ONE); a.C(ATX, C_NAMED)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('EXPR_DIGIT')
    a.C(0o10, L_ZERO); a.C(ATX, C_F)
    a.C(0o10, L_100); a.C(ATX, C_NFRAC)
    a.C(0o10, L_ZERO); a.C(ATX, C_SEEDOT)
    a.C(0o10, L_TWO); a.C(ATX, C_MODE)
    a.br(UJ, 'M_NUM')
    # operators
    a.mark('EX_OPCHK')
    a.C(0o10, C_CH); a.C(AEX, L_PLUS);  a.br(UZA, 'EX_PLUS')
    a.C(0o10, C_CH); a.C(AEX, L_MINUS); a.br(UZA, 'EX_MINUS')
    a.C(0o10, C_CH); a.C(AEX, L_STAR);  a.br(UZA, 'EX_STAR')
    a.C(0o10, C_CH); a.C(AEX, L_SLASH); a.br(UZA, 'EX_SLASH')
    a.C(0o10, C_CH); a.C(AEX, L_LPC);   a.br(UZA, 'EX_LP')
    a.C(0o10, C_CH); a.C(AEX, L_RPC);   a.br(UZA, 'EX_RP')
    a.C(0o10, C_CH); a.C(AEX, L_0X0A);  a.br(UZA, 'EX_END')
    a.br(UJ, 'MAIN_LOOP')
    # We must reach EX_OPCHK for non-digit expression bytes.  Patch the branch
    # that follows a non-digit/non-intrinsic decision: use a trampoline at the
    # top of EXPR by rewriting the three "MAIN_LOOP" fall-throughs above via a
    # late-assembled copy (see EXPR_FALL below).
    a.mark('EX_PLUS');  ec(a, L_OP1); a.br(UJ, 'MAIN_LOOP')
    a.mark('EX_MINUS'); ec(a, L_OP2); a.br(UJ, 'MAIN_LOOP')
    a.mark('EX_STAR');  ec(a, L_OP3); a.br(UJ, 'MAIN_LOOP')
    a.mark('EX_SLASH'); ec(a, L_OP4); a.br(UJ, 'MAIN_LOOP')
    a.mark('EX_LP');    ec(a, L_TOKLP); a.br(UJ, 'MAIN_LOOP')
    a.mark('EX_RP');    ec(a, L_TOKRP); a.br(UJ, 'MAIN_LOOP')
    a.mark('EX_END')
    ec(a, L_CSEOL)
    a.C(0o10, L_ZERO); a.C(ATX, C_MODE)
    reset_windows(a)
    a.br(UJ, 'DISPATCH')

    # ---- mode 2: literal digits ----
    a.mark('M_NUM')
    a.C(0o10, C_CH); a.C(AAX, L_0XF0); a.C(AEX, L_0X30); a.br(UZA, 'NUM_DIGIT')
    a.C(0o10, C_CH); a.C(AEX, L_DOT); a.br(UZA, 'NUM_DOT')
    a.C(0o10, L_ONE); a.C(ATX, C_MODE)
    a.br(UJ, 'NUM_FINISH')
    a.mark('NUM_DOT')
    a.C(0o10, L_ONE); a.C(ATX, C_SEEDOT)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('NUM_DIGIT')
    a.C(0o10, C_CH); a.C(AAX, L_0X0F); a.C(ATX, C_TMP2)
    a.C(0o10, C_SEEDOT); a.br(UZA, 'NUM_NOFRAC')
    a.C(0o10, C_NFRAC); a.C(ARX, L_ONE); a.C(ATX, C_NFRAC)
    a.mark('NUM_NOFRAC')
    a.C(0o10, C_TMP2); a.Z(0o24, 'EMASK'); a.Z(0o24, 'C105')
    a.C(ATX, C_DF)
    a.C(0o10, C_F); a.C(MUL, L_TEN); a.C(ADD, C_DF); a.C(ATX, C_F)
    a.br(UJ, 'MAIN_LOOP')

    a.mark('NUM_FINISH')
    a.mark('NUM_DIV_LOOP')
    a.C(0o10, C_NFRAC); a.C(AEX, L_100); a.br(UZA, 'NUM_STORE')
    a.C(0o10, C_F); a.C(DIV, L_TEN); a.C(ATX, C_F)
    a.C(0o10, C_NFRAC); a.C(ARX, L_NEG1); a.C(ATX, C_NFRAC)
    a.br(UJ, 'NUM_DIV_LOOP')
    a.mark('NUM_STORE')
    # SQRT by name: Newton x6 on the machine-derived float (B6b algorithm,
    # adapted: B5's pool already holds the true value, not 10x the value).
    a.C(0o10, C_INTR); a.br(UZA, 'NUM_NOSQ')
    a.C(0o10, C_F); a.C(ATX, C_TMP)
    a.C(ATX, C_SQX)
    for _ in range(6):
        a.C(0o10, C_TMP); a.C(DIV, C_SQX)
        a.C(0o04, C_SQX)
        a.C(MUL, L_HALF); a.C(ATX, C_SQX)
    a.C(0o10, C_SQX); a.C(ATX, C_F)
    a.C(0o10, L_ZERO); a.C(ATX, C_INTR); a.C(ATX, C_NAMED)
    a.mark('NUM_NOSQ')
    a.C(0o10, C_F); a.C(ATX, C_TMP)
    a.C(0o10, C_POOLPTR); a.L(ATI, 6)
    a.C(0o10, C_TMP); a.E(UTC_N2)
    a.L(ATX, 0o1637 + B5.LITBASE, reg=6)
    a.C(0o10, C_POOLPTR); a.C(AEX, L_TOKLIT)
    a.call('EMIT')
    a.C(0o10, C_POOLPTR); a.C(ARX, L_ONE); a.C(ATX, C_POOLPTR)
    a.C(0o10, L_ONE); a.C(ATX, C_MODE)
    a.br(UJ, 'DISPATCH')

    # ---- PRINT keyword ----
    a.mark('FOUND_PRINT')
    reset_windows(a)
    ec(a, L_CSPRINT)
    a.C(0o10, L_THREE); a.C(ATX, C_MODE)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('M_PLAB')
    is_digit(a, 'PLAB_DIG')
    a.C(0o10, C_CH); a.C(AEX, L_COMMA); a.br(UZA, 'PLAB_COMMA')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('PLAB_DIG')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('PLAB_COMMA')
    # FDESC placeholder: PAY is patched later from the FORMAT descriptor.
    a.C(0o10, C_TOKPTR); a.C(ATX, C_FDESC_IDX)
    ec(a, L_TOKFD)
    ec(a, L_CSX)
    ec(a, L_CSEOL)
    a.C(0o10, L_ZERO); a.C(ATX, C_MODE)
    reset_windows(a)
    a.br(UJ, 'DISPATCH')

    # ---- FORMAT keyword / Fw.d digits ----
    a.mark('FOUND_FORMAT')
    reset_windows(a)
    a.C(0o10, L_FOUR); a.C(ATX, C_MODE)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('M_S4')
    a.C(0o10, C_CH); a.C(AEX, L_CH_F); a.br(UZA, 'S4_SEEF')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('S4_SEEF')
    a.C(0o10, L_FIVE); a.C(ATX, C_MODE)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('M_S5')
    is_digit(a, 'S5_DIG')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('S5_DIG')
    a.C(0o10, C_CH); a.C(AAX, L_0X0F); a.C(ASX, L_SHL8); a.C(ATX, C_PAY)
    a.C(0o10, L_SIX); a.C(ATX, C_MODE)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('M_S6')
    a.C(0o10, C_CH); a.C(AEX, L_DOT); a.br(UZA, 'S6_SEEDOT')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('S6_SEEDOT')
    a.C(0o10, L_SEVEN); a.C(ATX, C_MODE)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('M_S7')
    is_digit(a, 'S7_DIG')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('S7_DIG')
    a.C(0o10, C_CH); a.C(AAX, L_0X0F); a.C(ARX, C_PAY); a.C(ATX, C_PAY)
    # patch the reserved FDESC token word
    a.C(0o10, C_FDESC_IDX); a.L(ATI, 6)
    a.C(0o10, L_TOKFD); a.C(ARX, C_PAY)
    a.E(UTC_N2); a.L(ATX, 0o1637 + B5.TOKBASE, reg=6)
    a.C(0o10, L_ZERO); a.C(ATX, C_MODE)
    reset_windows(a)
    a.br(UJ, 'DISPATCH')

    # ---- END keyword: emit END and hand off to verbatim B4 ----
    a.mark('FOUND_END')
    ec(a, L_CSEND)
    a.E(long_(UJ, B4_RAM))
    a.resolve()
    return a

# ------------------------------------------------------------------ constants
def lex_consts():
    c = B5.lex_consts()
    c.update({
        C_PAY:0, C_WIN3:0, C_WIN5:0, C_WIN6:0, C_FDESC_IDX:0,
        C_INTR:0, C_SQX:0,
        L_TXT_PRINT:0x5052494e54,
        L_TXT_FORMAT:0x464f524d4154,
        L_TXT_END:0x00454e44,
        L_MASK3:0xffffff, L_MASK5:(1 << 40)-1,
        L_SHL8:(64-8) << 41,
        L_CH_S:0x53,
        L_HALF:f32(0.5),
        L_THREE:3, L_FOUR:4, L_CH_F:0x46,
        C_NAMED:0, L_TOKFD:PB.tok(13,1,0,0),
        L_COMMA:0x2c, L_FIVE:5, L_SEVEN:7,
    })
    return c

def build(case, patch=0.0, src=None):
    src = Path(src) if src else WS / 'images/2048_base'
    dst = WS / 'images' / f'2048_{case}'
    shutil.copy2(src, dst)

    a = build_lex()
    entry_ram = a.ram_of_label('START')
    body = rz(str(dst), N + 1)
    body[0o11] = word(long_(0o300, entry_ram, reg=0), 0)
    body[0o27] = int.from_bytes(bytes([2,1,15,15,0,0]), 'big')
    body[0o30] = int.from_bytes(bytes([0,0,14,0,0,15]), 'big')
    body[0o31] = int.from_bytes(bytes([15,3,0,0,0,14]), 'big')
    body[0o32] = int.from_bytes(bytes([0,0,0o231,15,15,15]), 'big')
    for n, v in C6.vals().items():
        body[0o110 + FS.CELLS.index(n)] = v & MASK
    wz(str(dst), N + 1, body)

    n3_hw, _, _, _ = C6.build_n3()
    wz(str(dst), Z3, C6.asm_words(n3_hw))

    z2 = rz(str(dst), N2)
    z2[1] = C6.C2.text_word('X       ') & MASK
    z2[33] = f32(0.0)
    for i in range(4):
        z2[B5.LITBASE+i] = f32(0.0)
    wm, cm, sm = C7.width_tables()
    dconsts = {
        PB.K_BASE:0o20000, PB.K_ONE:1,
        PB.K_MTK:0o7700000000000000, PB.K_MSUB:0o0077000000000000,
        PB.K_MPAY:0o0000000077777777,
        PB.K_SR42:(64+42)<<41, PB.K_SR36:(64+36)<<41, PB.K_SR8:(64+8)<<41,
        PB.K_255:0o377, PB.K_ZERO:0,
        PB.K_TK10:10, PB.K_TK2:2, PB.K_TK11:11, PB.K_TK12:12, PB.K_TK13:13,
        PB.K_SUB30:30, PB.K_SUB31:31, PB.K_SUB34:34, PB.K_SUB37:37,
        PB.K_GOSTA:body[0o27], PB.K_GOSTB:body[0o30],
        PB.K_NEG1:MASK^1, PB.K_TEN:f32(10.0), PB.K_PATCH:f32(patch),
        PB.K_OPADD:1, PB.KOPSUB:2, PB.KOPMUL:3, PB.KOPDIV:4,
        PB.K_TKLIT:1, PB.K_TKOP:3, PB.K_TKLP:6, PB.K_MODE2:2, PB.K_BIAS:100,
        PB.C_TOK:0, PB.C_TK:0, PB.C_SUB:0, PB.C_PAY:0, PB.C_OP:0,
        PB.C_A:0, PB.C_B:0, PB.C_TOP:0, PB.C_SPC:0, PB.C_SPP:0,
        PB.C_MODE:0, PB.C_PUSHVAL:0, PB.K_PRINT_BIAS:f32(0.0),
    }
    for off, v in zip(range(PB.K_WMASK0, PB.K_WMASK0+3), wm): dconsts[off]=v
    for off, v in zip(range(PB.K_CLEARM0, PB.K_CLEARM0+2), cm): dconsts[off]=v
    for off, v in zip(range(PB.K_SPACEM0, PB.K_SPACEM0+2), sm): dconsts[off]=v
    for off, v in dconsts.items(): z2[off] = v & MASK

    parser, _ = PB.build_parser(CONV_RAM0)
    for i in range(len(parser.hw)//2):
        z2[PB.CODE_OFF+i] = word(parser.hw[2*i], parser.hw[2*i+1])
    if len(parser.hw) % 2:
        z2[PB.CODE_OFF+len(parser.hw)//2] = word(parser.hw[-1], DUMMY)

    for off, v in lex_consts().items(): z2[off] = v & MASK
    for off, w in a.code_words(): z2[off] = w & MASK
    wz(str(dst), N2, z2)

    sha = hashlib.sha256(dst.read_bytes()).hexdigest()
    n2used = max(off for off, _ in a.code_words()) + 1
    print(f'case={case} sha={sha} N3={len(n3_hw)//2}/58w '
          f'B4={len(parser.hw)//2}w LEX={len(a.hw)//2}w slots={len(a.slots)} '
          f'N2last={n2used} patch={patch}')
    return dst, sha, len(n3_hw)//2, len(a.hw)//2, n2used

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--build', required=True)
    ap.add_argument('--patch', type=float, default=0.0)
    ap.add_argument('--src')
    x = ap.parse_args()
    build(x.build, patch=x.patch, src=x.src)
