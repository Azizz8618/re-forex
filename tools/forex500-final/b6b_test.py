#!/usr/bin/env python3
"""B6a IMPLEMENTATION: real Fortran source TEXT `PRINT n,X` and labeled
`n FORMAT(1X,Fw.d)` are parsed by BESM-6 machine code; the resolved Fw.d drives
the VERBATIM B3 dispatcher at 0o22065 and the verbatim docs/105 GOST converter.

Two passes over the RLE card buffer (RAM 0o64012+):
  Pass L (label/FORMAT pre-scan): scans every card, finds `FORMAT(`, takes the
      statement label accumulated from the first word of that card, parses the
      Fw.d digits after `1X,`, stores (label, w<<8|d) in our label table.
  Pass E (emit+execute): scans the cards again, emits the B2 one-word token
      stream (assignment from source digits, PRINT with FDESC resolved from the
      FORMAT label, FORMAT itself a no-op, END from source), then hands off.

No 777005 IR cards, no pre-seeded expression/print fixtures, no host result
digit.  C dispak is used only as an oracle; all verdicts come from full SIMH.

Reused verbatim: build_e2e (rz/wz/short/long/word/f32), c6_build (N+3 converter,
low-RAM cells), c7_build (width tables), final_sign (LO cells), dispatch_build
(B3 dispatcher + tok() encoder), build_dispatch constants.
"""
import argparse, hashlib, shutil, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import c6_build as C6
import c7_build as C7
import final_sign as FS
import dispatch_build as DB
from build_e2e import rz, wz, short, long_, word, f32, MASK, N, Z3, MAX_WORDS

WS = HERE.parent
N2 = N + 2
N2_RAM0 = 0o21637
CONV_RAM0 = 0o30114
DISP_RAM = N2_RAM0 + DB.CODE_OFF       # 0o22065, verbatim B3 dispatcher entry
TOKBASE = DB.TOKBASE                   # 64
LITBASE = DB.LITBASE                   # 100

# opcodes (verified against SIMH besm6_cpu.c / prior MTR traces)
ATX, AAX, AEX, ARX, ASX = 0o00, 0o11, 0o12, 0o13, 0o26
FADD, MUL, DIV = 0o04, 0o17, 0o16
ATI, ITA, UJ, UZA = 0o40, 0o42, 0o300, 0o260
DUMMY = C6.DUMMY
LINK = 5                               # link register for our two VJM subroutines

# ------------------------------------------------------------------ data map
# All N+2 data cells are < 526 (forbidden band 526..900 untouched).
L_SHRTAB = 2                            # 2..7 : six byte-shift controls
L_M8=8; L_ONE=9; L_SIX=10; L_NEG20=11; L_PD0=12
L_SR24=13; L_SR16=14; L_SR8=15; L_SHL8=16; L_255=17
L_EMASK=18; L_C105=19; L_HUNDRED=20; L_TENF=21
L_ZERO=22; L_CBASE=23
L_EQ=24; L_DOT=25; L_COMMA=26; L_0A=27; L_0X80=28; L_K80=29
L_0XF0=30; L_0X30=31; L_FF=32
# 33 = symbol value word (owned by B3) -- skipped
L_CH_X=34; L_CH_F=35
L_TXT_PRINT=36; L_TXT_FORMAT=37; L_TXT_END=38
L_TWO=39; L_THREE=40; L_FOUR=41
L_TOKPROG=42; L_TOKID0=43; L_TOKREAL=44; L_TOKEOL=45; L_TOKIDX=46
L_TOKEQ=47; L_TOKLIT=48; L_TOKPRINT=49; L_TOKFD=50; L_TOKEND=51
L_FPAY_PATCH=52                         # one-word PATCH target (one's-complement delta)
L_SHL42_CONST=53; L_NEG30=54
C_CURW=55; C_CH=56; C_PREV=57; C_TP=58; C_NUM=59; C_NDIG=60; C_TMP=61
C_LABPACK=62; C_LAB=63
# high data band (low band is full): 500..511
C_PAY=500; C_FOUND=501; C_ATSTART=502; C_LABHIT=503; C_STATE=504
C_W=505; C_D=506; C_PLABPACK=507; C_TOKTMP=508
C_WIN3=509; C_WIN5=510; C_WIN6=511
C_TMP2=512
L_MASK3=513; L_MASK5=514

# ---- B6b intrinsic extension (free cells 515..525 and tail band 927..1023) ----
C_WIN4=515; C_INTR=516
L_TXT_SQRT=517; L_TXT_ABS=518; L_TXT_MOD=519; L_MASK4=520
L_SIGN=521; L_HALF=522; L_MASK40=523; L_EXPALL=524
ITAB0=945; ITAB1=946; ITAB2=947
C_MODA=948; C_MODB=949; C_MODQ=950

# code slots: contiguous low band 300..499, then proven tail band 901..1023.
CODE_REGIONS = [(300, 499), (901, 1023)]


def sub_const(d):
    return (MASK - d) & MASK


def vjm_imm(addr, reg=LINK):
    return (reg << 20) | (0o31 << 15) | (addr & 0o77777)


class LAsm:
    def __init__(self):
        self.hw = []
        self.labels = {}
        self.branches = []             # (hw_index, name, op)
        self.calls = []                # (hw_index, name)
        self.slots = []
        for a, b in CODE_REGIONS:
            self.slots.extend(range(a, b + 1))
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
        i = len(self.hw); self.E(long_(op, 0))
        self.branches.append((i, name, op)); return i
    def call(self, name):
        if len(self.hw) % 2 == 0:
            i = len(self.hw); self.E(vjm_imm(0)); self.E(DUMMY)
        else:
            i = len(self.hw); self.E(vjm_imm(0))
        self.calls.append((i, name)); return i
    def ret(self):
        self.L(UJ, 0, reg=LINK)        # uj 0(5) -> M[5] (VJM return address)
    def ram_of_label(self, name):
        hwidx = self.labels[name]
        off = self.slots[hwidx // 2]
        base = tail_ram(off) if off >= 901 else (N2_RAM0 + off)
        return base + (hwidx % 2)
    def resolve(self):
        for i, name, op in self.branches:
            self.hw[i] = long_(op, self.ram_of_label(name))
        for i, name in self.calls:
            self.hw[i] = vjm_imm(self.ram_of_label(name))
        if len(self.hw) % 2:
            self.E(DUMMY)
        assert (len(self.hw) + 1) // 2 <= len(self.slots), \
            f'LEX code overrun: {(len(self.hw)+1)//2} words > {len(self.slots)}'
    def code_words(self):
        return [(self.slots[i], word(self.hw[2*i], self.hw[2*i+1]))
                for i in range((len(self.hw) + 1) // 2)]


def tail_ram(off):
    return 0o27721 + (off - 901)       # N+2 offsets 901..1023


def rearm(a):
    a.Z(0o10, 'HALF'); a.L(ATI, 12)    # M[12] = 0o20000 (N+2 operand base)
    a.Z(0o10, 'HALF'); a.L(ATI, 7)     # M[7]  = 0o20000 (branch base)


def init_scan(a):
    a.C(0o10, L_CBASE); a.L(ATI, 10)   # M[10] = 0o60000 -> card word 0o64012
    a.L(0o10, 0o4012, 10); a.C(ATX, C_CURW)
    a.C(0o10, L_ZERO); a.L(ATI, 11)    # M[11] = byte index 0
    a.C(0o10, L_ONE); a.C(ATX, C_ATSTART)
    a.C(0o10, L_ZERO); a.C(ATX, C_LABPACK); a.C(ATX, C_LABHIT)
    a.C(ATX, C_WIN4); a.C(ATX, C_INTR)


def emit(a):
    """ACC holds a B2 token word; store to N+2[TOKBASE+C_TP], C_TP++."""
    a.C(ATX, C_TOKTMP)
    a.C(0o10, C_TP); a.L(ATI, 6)
    a.C(0o10, C_TOKTMP)
    a.E(long_(0o220, 0o20000))
    a.L(ATX, 0o1637 + TOKBASE, reg=6)
    a.C(0o10, C_TP); a.C(ARX, L_ONE); a.C(ATX, C_TP)


def emit_const(a, cell):
    a.C(0o10, cell)
    a.call('EMIT')


# ------------------------------------------------------------------ GETCH
def emit_getch(a):
    a.mark('GETCH')
    a.L(ITA, 11); a.C(AEX, L_SIX)
    a.br(UZA, 'GC_NEXTW')
    a.C(0o10, C_CURW)
    a.E(long_(0o220, 0o20000))
    a.C(ASX, L_SHRTAB, reg=11)
    a.C(AAX, L_M8); a.C(ATX, C_CH)
    a.L(ITA, 11); a.C(ARX, L_ONE); a.L(ATI, 11)
    a.ret()
    a.mark('GC_NEXTW')
    # Only a word whose LAST byte is the 0x0a pad ends a card.  FORMAT's label
    # and its keyword may straddle two words of the same card; resetting at
    # every word boundary would lose the label before the keyword completes.
    a.C(0o10, C_CURW); a.C(ASX, L_SHRTAB + 5); a.C(AAX, L_M8)
    a.C(AEX, L_0A); a.br(UZA, 'GC_NEWCARD')
    a.L(ITA, 10); a.C(ARX, L_ONE); a.L(ATI, 10)
    a.L(0o10, 0o4012, 10); a.C(ATX, C_CURW)
    a.C(0o10, L_ZERO); a.L(ATI, 11)
    a.ret()
    a.mark('GC_NEWCARD')
    a.L(ITA, 10); a.C(ARX, L_ONE); a.L(ATI, 10)
    a.L(0o10, 0o4012, 10); a.C(ATX, C_CURW)
    a.C(0o10, L_ZERO); a.L(ATI, 11)
    a.C(0o10, L_ONE); a.C(ATX, C_ATSTART)
    a.C(0o10, L_ZERO); a.C(ATX, C_LABPACK); a.C(ATX, C_LABHIT)
    a.C(ATX, C_WIN4); a.C(ATX, C_INTR)
    a.ret()


def emit_emit(a):
    a.mark('EMIT')
    emit(a)
    a.ret()


# ------------------------------------------- keyword-window test (sliding bytes)
def kwindow(a, eof_label, ws_label, found_print, found_format, found_end):
    """Update the 3/5/6-byte sliding windows and dispatch on keyword matches.
    C_CH holds the current non-whitespace byte.  Falls through to caller code
    when no keyword matched.  Already-reset C_WIN* are kept across statements."""
    # True sliding windows: shift in CH, then mask to 3 / 5 / 6 bytes.
    # (Without the masks a 5-byte window keeps 6 bytes once a 6th char arrives.)
    a.C(0o10, C_WIN3); a.C(ASX, L_SHL8); a.C(ARX, C_CH)
    a.C(AAX, L_MASK3); a.C(ATX, C_WIN3)
    a.C(0o10, C_WIN5); a.C(ASX, L_SHL8); a.C(ARX, C_CH)
    a.C(AAX, L_MASK5); a.C(ATX, C_WIN5)
    a.C(0o10, C_WIN6); a.C(ASX, L_SHL8); a.C(ARX, C_CH); a.C(ATX, C_WIN6)
    # FORMAT (6 bytes) wins over PRINT/END
    a.C(0o10, C_WIN6); a.C(AEX, L_TXT_FORMAT); a.br(UZA, found_format)
    a.C(0o10, C_WIN5); a.C(AEX, L_TXT_PRINT); a.br(UZA, found_print)
    a.C(0o10, C_WIN3); a.C(AEX, L_TXT_END); a.br(UZA, found_end)


def intr_window(a, found_sqrt, found_abs, found_mod):
    """B6b: 4-byte sliding window over source chars; recognise SQRT/ABS/MOD.
    On a match set C_INTR = SUB (2/1/3).  Callers emit the INTR token later."""
    a.C(0o10, C_WIN4); a.C(ASX, L_SHL8); a.C(ARX, C_CH)
    a.C(AAX, L_MASK4); a.C(ATX, C_WIN4)
    a.C(0o10, C_WIN4); a.C(AEX, L_TXT_SQRT); a.br(UZA, found_sqrt)
    a.C(0o10, C_WIN4); a.C(AEX, L_TXT_ABS);  a.br(UZA, found_abs)
    a.C(0o10, C_WIN4); a.C(AEX, L_TXT_MOD);  a.br(UZA, found_mod)


def skip_ws(a, lbl):
    a.C(0o10, C_CH); a.C(AEX, L_0A); a.br(UZA, lbl)
    a.C(0o10, C_CH); a.C(AAX, L_0X80); a.C(AEX, L_K80); a.br(UZA, lbl)


def is_digit(a, lbl):
    a.C(0o10, C_CH); a.C(AAX, L_0XF0); a.C(AEX, L_0X30); a.br(UZA, lbl)


# ------------------------------------------------------------------ Pass L
def emit_passL(a):
    rearm(a); init_scan(a)
    a.C(0o10, L_ZERO)
    a.C(ATX, C_STATE); a.C(ATX, C_FOUND)
    a.C(ATX, C_W); a.C(ATX, C_D)
    a.C(0o10, L_ZERO); a.C(ATX, C_WIN3); a.C(ATX, C_WIN5); a.C(ATX, C_WIN6)
    a.mark('PL_LOOP')
    a.call('GETCH')
    a.C(0o10, C_CH); a.C(AEX, L_FF); a.br(UZA, 'PL_DONE')
    skip_ws(a, 'PL_LOOP')
    # label accumulation only at the first non-space bytes of a card word
    a.C(0o10, C_ATSTART); a.br(UZA, 'PL_NOSTART')
    is_digit(a, 'PL_STARTDIG')
    a.mark('PL_NOSTART')
    a.C(0o10, L_ZERO); a.C(ATX, C_ATSTART)   # first letter ends label area
    kwindow(a, 'PL_DONE', 'PL_LOOP', 'PL_NOP', 'PL_FORMAT', 'PL_NOP')
    a.br(UJ, 'PL_AFTERKW')
    a.mark('PL_STARTDIG')
    a.C(0o10, C_LABPACK); a.C(ASX, L_SHL8); a.C(ARX, C_CH); a.C(ATX, C_LABPACK)
    a.C(0o10, L_ONE); a.C(ATX, C_LABHIT)
    a.br(UJ, 'PL_LOOP')
    a.mark('PL_AFTERKW')
    # state 1: look for the F of Fw.d after FORMAT(
    a.C(0o10, C_STATE); a.br(UZA, 'PL_LOOP')
    a.C(0o10, C_STATE); a.C(AEX, L_ONE); a.br(UZA, 'PL_S1')
    a.C(0o10, C_STATE); a.C(AEX, L_TWO); a.br(UZA, 'PL_S2')
    a.C(0o10, C_STATE); a.C(AEX, L_THREE); a.br(UZA, 'PL_S3')
    a.C(0o10, C_STATE); a.C(AEX, L_FOUR); a.br(UZA, 'PL_S4')
    a.br(UJ, 'PL_LOOP')
    a.mark('PL_S1')
    a.C(0o10, C_CH); a.C(AEX, L_CH_F); a.br(UZA, 'PL_SEEF')
    a.br(UJ, 'PL_LOOP')
    a.mark('PL_SEEF')
    a.C(0o10, L_TWO); a.C(ATX, C_STATE)
    a.br(UJ, 'PL_LOOP')
    a.mark('PL_S2')                         # w digit
    is_digit(a, 'PL_GETW')
    a.br(UJ, 'PL_LOOP')
    a.mark('PL_GETW')
    a.C(0o10, C_CH); a.C(AAX, L_M8); a.C(ARX, L_PD0); a.C(AAX, L_M8)
    a.C(ATX, C_W)
    a.C(0o10, L_THREE); a.C(ATX, C_STATE)
    a.br(UJ, 'PL_LOOP')
    a.mark('PL_S3')                         # '.'
    a.C(0o10, C_CH); a.C(AEX, L_DOT); a.br(UZA, 'PL_SEEDOT')
    a.br(UJ, 'PL_LOOP')
    a.mark('PL_SEEDOT')
    a.C(0o10, L_FOUR); a.C(ATX, C_STATE)
    a.br(UJ, 'PL_LOOP')
    a.mark('PL_S4')                         # d digit
    is_digit(a, 'PL_GETD')
    a.br(UJ, 'PL_LOOP')
    a.mark('PL_GETD')
    a.C(0o10, C_CH); a.C(AAX, L_M8); a.C(ARX, L_PD0); a.C(AAX, L_M8)
    a.C(ATX, C_D)
    # PAY = w<<8 | d
    a.C(0o10, C_W); a.C(ASX, L_SHL8); a.C(ARX, C_D); a.C(ATX, C_PAY)
    a.C(0o10, C_LABPACK); a.C(ATX, C_LAB)   # store label -> table (single entry)
    a.C(0o10, L_ONE); a.C(ATX, C_FOUND)
    a.C(0o10, L_ZERO); a.C(ATX, C_STATE)
    a.br(UJ, 'PL_LOOP')
    a.mark('PL_FORMAT')
    a.C(0o10, L_ZERO); a.C(ATX, C_WIN3); a.C(ATX, C_WIN5); a.C(ATX, C_WIN6)
    a.C(0o10, C_LABHIT); a.br(UZA, 'PL_NOHIT')
    a.C(0o10, C_LABPACK); a.C(ATX, C_LAB)
    a.mark('PL_NOHIT')
    a.C(0o10, L_ONE); a.C(ATX, C_STATE)
    a.br(UJ, 'PL_LOOP')
    a.mark('PL_NOP')
    a.br(UJ, 'PL_AFTERKW')
    a.mark('PL_DONE')


# ------------------------------------------- number -> float (docs/104 chain)
def emit_numfinish(a, done_label):
    a.C(0o10, C_NUM); a.C(ASX, L_SR24); a.C(AAX, L_M8)
    a.C(ARX, L_PD0); a.C(AAX, L_M8); a.L(ATI, 6)
    a.C(0o10, C_NUM); a.C(ASX, L_SR16); a.C(AAX, L_M8)
    a.C(ARX, L_PD0); a.C(AAX, L_M8); a.L(ARX, FS.LO['T0'], reg=6)
    a.Z(0o24, 'EMASK'); a.Z(0o24, 'C105'); a.C(ATX, C_TMP)
    a.C(0o10, C_NUM); a.C(ASX, L_SR8); a.C(AAX, L_M8)
    a.C(ARX, L_PD0); a.C(AAX, L_M8); a.L(ATI, 6)
    a.C(0o10, C_NUM); a.C(AAX, L_M8)
    a.C(ARX, L_PD0); a.C(AAX, L_M8); a.L(ARX, FS.LO['T0'], reg=6)
    a.Z(0o24, 'EMASK'); a.Z(0o24, 'C105'); a.C(ATX, C_TMP2)
    a.C(0o10, C_TMP); a.C(MUL, L_HUNDRED); a.C(FADD, C_TMP2); a.C(ATX, C_TMP)
    a.C(0o10, C_TMP); a.C(DIV, L_TENF); a.C(ATX, C_TMP)
    a.C(0o10, C_TMP); a.C(ATX, LITBASE)    # literal pool word 0 = 10 * value
    a.br(UJ, done_label)


# ------------------------------------------------------------------ Pass E
def emit_passE(a):
    rearm(a); init_scan(a)
    a.C(0o10, L_ZERO); a.C(ATX, C_TP)
    a.C(0o10, L_ZERO); a.C(ATX, C_WIN3); a.C(ATX, C_WIN5); a.C(ATX, C_WIN6)
    # scaffolding tokens (PROGRAM MAIN / REAL X / EOL), as in proven B1/B5
    emit_const(a, L_TOKPROG)
    emit_const(a, L_TOKID0)
    emit_const(a, L_TOKREAL)
    emit_const(a, L_TOKIDX)
    emit_const(a, L_TOKEOL)
    a.mark('PE_LOOP')
    a.call('GETCH')
    a.C(0o10, C_CH); a.C(AEX, L_FF); a.br(UZA, 'PE_DONE')
    a.mark('PE_DISPATCH')
    a.C(0o10, C_FOUND)
    # mode is held in C_STATE: 0 scan, 1 number, 2 print-label, 3 print-var
    a.C(0o10, C_STATE); a.br(UZA, 'PE_SCAN')
    a.C(0o10, C_STATE); a.C(AEX, L_ONE); a.br(UZA, 'PE_NUM')
    a.C(0o10, C_STATE); a.C(AEX, L_TWO); a.br(UZA, 'PE_PLAB')
    a.C(0o10, C_STATE); a.C(AEX, L_THREE); a.br(UZA, 'PE_PVAR')
    a.br(UJ, 'PE_DONE')

    # ---- mode 0: source scan ----
    a.mark('PE_SCAN')
    a.C(0o10, C_CH); a.C(AEX, L_EQ); a.br(UZA, 'PE_FOUND_EQ')
    skip_ws(a, 'PE_LOOP')
    kwindow(a, 'PE_DONE', 'PE_LOOP', 'PE_PRINT', 'PE_FORMAT', 'PE_END')
    a.C(0o10, C_CH); a.C(ATX, C_PREV)
    a.br(UJ, 'PE_LOOP')
    a.mark('PE_NOP')
    a.br(UJ, 'PE_LOOP')

    # ---- assignment '=' ----
    a.mark('PE_FOUND_EQ')
    a.C(0o10, C_PREV); a.C(ARX, L_NEG20); a.C(ASX, L_SHL42_CONST); a.C(ATX, C_TMP)
    a.C(0o10, C_TMP); a.C(ATX, 1)          # symbol name word
    emit_const(a, L_TOKIDX)
    emit_const(a, L_TOKEQ)
    a.C(0o10, L_ZERO); a.C(ATX, C_NUM); a.C(ATX, C_NDIG)
    a.C(0o10, L_ONE); a.C(ATX, C_STATE)
    a.br(UJ, 'PE_LOOP')

    # ---- mode 1: intrinsic name followed by literal digits ----
    a.mark('PE_NUM')
    is_digit(a, 'PE_NUMDIG')
    a.C(0o10, C_CH); a.C(AEX, L_DOT); a.br(UZA, 'PE_LOOP')
    emit_numfinish(a, 'PE_NUMDONE')
    a.mark('PE_NUMDIG')
    a.C(0o10, C_NUM); a.C(ASX, L_SHL8); a.C(ARX, C_CH); a.C(ATX, C_NUM)
    a.C(0o10, C_NDIG); a.C(ARX, L_ONE); a.C(ATX, C_NDIG)
    a.br(UJ, 'PE_LOOP')
    # Name handlers: remember SUB, reset window, keep parsing the argument.
    a.mark('PE_GOT_SQRT')
    a.C(0o10, L_TWO); a.C(ATX, C_INTR)
    a.br(UJ, 'PE_NAME_RESET')
    a.mark('PE_GOT_ABS')
    a.C(0o10, L_ONE); a.C(ATX, C_INTR)
    a.br(UJ, 'PE_NAME_RESET')
    a.mark('PE_GOT_MOD')
    a.C(0o10, L_THREE); a.C(ATX, C_INTR)
    a.mark('PE_NAME_RESET')
    a.C(0o10, L_ZERO); a.C(ATX, C_WIN4)
    a.br(UJ, 'PE_LOOP')
    a.mark('PE_NUMDONE')
    a.mark('PE_NOINTR')
    emit_const(a, L_TOKLIT)
    emit_const(a, L_TOKEOL)
    a.C(0o10, L_ZERO); a.C(ATX, C_STATE)
    a.br(UJ, 'PE_DISPATCH')                # reprocess terminating byte in scan mode

    # ---- PRINT found ----
    a.mark('PE_PRINT')
    a.C(0o10, L_ZERO); a.C(ATX, C_WIN3); a.C(ATX, C_WIN5); a.C(ATX, C_WIN6)
    emit_const(a, L_TOKPRINT)
    a.C(0o10, L_TWO); a.C(ATX, C_STATE)
    a.br(UJ, 'PE_LOOP')
    a.mark('PE_PLAB')                      # collect FORMAT label digits
    is_digit(a, 'PE_PLABDIG')
    a.C(0o10, C_CH); a.C(AEX, L_COMMA); a.br(UZA, 'PE_PLABCOMMA')
    a.br(UJ, 'PE_LOOP')
    a.mark('PE_PLABDIG')
    a.C(0o10, C_PLABPACK); a.C(ASX, L_SHL8); a.C(ARX, C_CH); a.C(ATX, C_PLABPACK)
    a.br(UJ, 'PE_LOOP')
    a.mark('PE_PLABCOMMA')
    # resolve label: compare PRINT's label with the FORMAT label table entry
    a.C(0o10, C_PLABPACK); a.C(AEX, C_LAB); a.br(UZA, 'PE_LABOK')
    # no-go: no FORMAT with this label -> emit END and finish without printing
    emit_const(a, L_TOKEND)
    a.br(UJ, 'PE_DONE')
    a.mark('PE_LABOK')
    # FDESC token: tok(13,1,0,0) + PAY + one-word patch delta
    a.C(0o10, C_PAY); a.C(ARX, L_FPAY_PATCH); a.C(ARX, L_TOKFD)
    a.call('EMIT')
    a.C(0o10, L_THREE); a.C(ATX, C_STATE)
    a.br(UJ, 'PE_LOOP')
    a.mark('PE_PVAR')                      # single-letter variable after comma
    skip_ws(a, 'PE_LOOP')
    emit_const(a, L_TOKIDX)
    emit_const(a, L_TOKEOL)
    a.C(0o10, L_ZERO); a.C(ATX, C_STATE)
    a.C(0o10, L_ZERO); a.C(ATX, C_WIN3); a.C(ATX, C_WIN5); a.C(ATX, C_WIN6)
    a.br(UJ, 'PE_LOOP')

    # ---- FORMAT statement: no-op at execution ----
    a.mark('PE_FORMAT')
    a.C(0o10, L_ZERO); a.C(ATX, C_WIN3); a.C(ATX, C_WIN5); a.C(ATX, C_WIN6)
    a.br(UJ, 'PE_LOOP')
    a.mark('PE_END')
    emit_const(a, L_TOKEND)
    a.mark('PE_DONE')
    a.E(long_(0o300, DISP_RAM))            # hand off to the verbatim B3 dispatcher


AVX, AOX = 0o14, 0o15


def build_intrinsics(ret_ram):
    """ABS / SQRT / MOD machine routines in N+2 tail slots 941..1023.
    ACC on entry = the float argument; each routine leaves its result in ACC
    and executes LONG uj ret_ram.  ITAB trampolines index these by SUB."""
    a = LAsm()
    a.slots = list(range(951, 1024))   # LEX tail ends at 944; ITAB 945..950
    FADD, FSUB = 0o04, 0o06
    DIV, MUL = 0o16, 0o17

    a.mark('I_ABS')                       # true |ACC| using the proven avx
    a.C(ATX, C_TMP2)
    a.C(0o10, C_TMP2); a.C(AAX, L_SIGN)
    a.br(UZA, 'I_ABSPOS')
    a.C(0o10, C_TMP2); a.C(AVX, L_SIGN)
    a.E(long_(UJ, ret_ram, reg=0))
    a.mark('I_ABSPOS')
    a.C(0o10, C_TMP2)
    a.E(long_(UJ, ret_ram, reg=0))

    a.mark('I_SQRT')                      # Newton x4: x=(x+S/x)/2
    a.C(ATX, C_TMP)
    a.C(0o10, C_TMP); a.C(ATX, C_NUM)
    for _ in range(4):
        a.C(0o10, C_TMP); a.C(DIV, C_NUM)
        a.C(FADD, C_NUM); a.C(MUL, L_HALF); a.C(ATX, C_NUM)
    a.C(0o10, C_NUM)
    a.E(long_(UJ, ret_ram, reg=0))

    a.mark('I_MOD')                       # bitwise-AINT remainder (a in ACC)
    a.C(ATX, C_MODA)
    a.C(0o10, C_MODA); a.C(DIV, C_MODB); a.C(ATX, C_MODQ)
    a.C(0o10, L_MASK40); a.C(ASX, C_MODQ); a.C(AEX, L_MASK40)
    a.C(AOX, L_EXPALL); a.C(ATX, C_TMP)
    a.C(0o10, C_MODQ); a.C(AAX, C_TMP); a.C(ATX, C_NUM)
    a.C(0o10, C_MODB); a.C(MUL, C_NUM); a.C(ATX, C_TMP2)
    a.C(0o10, C_MODA); a.C(FSUB, C_TMP2)
    a.E(long_(UJ, ret_ram, reg=0))
    a.resolve()
    return a


def build_lex():
    a = LAsm()
    emit_getch(a)
    emit_emit(a)
    a.mark('START')
    emit_passL(a)
    emit_passE(a)
    a.resolve()
    return a


def consts(body):
    c = {
        L_SHRTAB+0: (64+40) << 41, L_SHRTAB+1: (64+32) << 41,
        L_SHRTAB+2: (64+24) << 41, L_SHRTAB+3: (64+16) << 41,
        L_SHRTAB+4: (64+8) << 41,  L_SHRTAB+5: (64+0) << 41,
        L_M8: 0xff, L_ONE: 1, L_SIX: 6, L_NEG20: sub_const(0x20), L_PD0: 0xd0,
        L_SR24: (64+24) << 41, L_SR16: (64+16) << 41, L_SR8: (64+8) << 41,
        L_SHL8: (64-8) << 41, L_255: 0xff,
        L_SHL42_CONST: (64-42) << 41,
        L_EMASK: 0o177 << 41, L_C105: 0o151 << 41,
        L_HUNDRED: f32(100.0), L_TENF: f32(10.0),
        L_ZERO: 0, L_CBASE: 0o60000,
        L_EQ: 0x3d, L_DOT: 0x2e, L_COMMA: 0x2c, L_0A: 0x0a,
        L_0X80: 0x80, L_K80: 0x80, L_0XF0: 0xf0, L_0X30: 0x30, L_FF: 0xff,
        L_CH_X: 0x58, L_CH_F: 0x46,
        L_TXT_PRINT: 0x5052494e54,        # "PRINT" ASCII
        L_TXT_FORMAT: 0x464f524d4154,     # "FORMAT" ASCII
        L_TXT_END: 0x00454e44,            # "END" ASCII
        L_TWO: 2, L_THREE: 3, L_FOUR: 4,
        L_TOKPROG: DB.tok(10, 30), L_TOKID0: DB.tok(2),
        L_TOKREAL: DB.tok(10, 31), L_TOKEOL: DB.tok(11),
        L_TOKIDX: DB.tok(2, 0, 0, 1), L_TOKEQ: DB.tok(8),
        L_TOKLIT: DB.tok(1), L_TOKPRINT: DB.tok(10, 34),
        L_TOKFD: DB.tok(13, 1, 0, 0), L_TOKEND: DB.tok(10, 37),
        L_FPAY_PATCH: 0,
        L_NEG30: sub_const(0x30),
        L_MASK3: 0xffffff, L_MASK5: (1 << 40) - 1,
        C_CURW: 0, C_CH: 0, C_PREV: 0, C_TP: 0, C_NUM: 0, C_NDIG: 0,
        C_TMP: 0, C_LABPACK: 0, C_LAB: 0,
        C_PAY: 0, C_FOUND: 0, C_ATSTART: 0, C_LABHIT: 0,
        C_STATE: 0, C_W: 0, C_D: 0, C_PLABPACK: 0, C_TOKTMP: 0,
        C_WIN3: 0, C_WIN5: 0, C_WIN6: 0,
        C_TMP2: 0,
        # B6b intrinsics
        C_WIN4: 0, C_INTR: 0,
        L_TXT_SQRT: 0x53515254, L_TXT_ABS: 0x00414253,
        L_TXT_MOD: 0x004d4f44, L_MASK4: 0xffffffff,
        L_SIGN: 1 << 40, L_HALF: f32(0.5),
        L_MASK40: 0xffffffffff, L_EXPALL: (0o177 << 41) | (1 << 40),
    }
    return c


def build(case, src=None, patch_delta=None, patch_off=None, patch_intr=False):
    src = Path(src) if src else WS / 'images/2048_base'
    dst = WS / 'images' / f'2048_{case}'
    shutil.copy2(src, dst)

    a = build_lex()
    entry_ram = a.ram_of_label('START')
    intr = build_intrinsics(a.ram_of_label('PE_NOINTR'))

    # ---- body N+1: GOST seeds + low-RAM converter cells (keeper body[0o26] kept)
    body = rz(str(dst), N + 1)
    body[0o11] = word(long_(0o300, entry_ram, reg=0), DUMMY)  # entry -> our LEX
    body[0o27] = int.from_bytes(bytes([2, 1, 15, 15, 0, 0]), 'big')
    body[0o30] = int.from_bytes(bytes([0, 0, 14, 0, 0, 15]), 'big')
    body[0o31] = int.from_bytes(bytes([15, 3, 0, 0, 0, 14]), 'big')
    body[0o32] = int.from_bytes(bytes([0, 0, 0o231, 15, 15, 15]), 'big')
    for n, value in C6.vals().items():
        body[0o110 + FS.CELLS.index(n)] = value & MASK
    wz(str(dst), N + 1, body)

    # ---- N+3 verbatim converter (40/58) ----
    n3_hw, floor_ram, conv_len, floor_len = C6.build_n3()
    wz(str(dst), Z3, C6.asm_words(n3_hw))

    # ---- N+2: verbatim B3 dispatcher + constants + our source lexer ----
    disp, labels = DB.build_dispatch(CONV_RAM0)
    z2 = rz(str(dst), N2)
    z2[1] = C6.C2.text_word('X       ') & MASK
    z2[33] = f32(0.0)
    for i in range(4):
        z2[LITBASE + i] = f32(0.0)            # literal pool written by our code
    wm, cm, sm = C7.width_tables()
    dconsts = {
        DB.K_BASE: 0o20000, DB.K_ONE: 1,
        DB.K_MTK: 0o7700000000000000, DB.K_MSUB: 0o0077000000000000,
        DB.K_MPAY: 0o0000000077777777,
        DB.K_SR42: (64 + 42) << 41, DB.K_SR36: (64 + 36) << 41,
        DB.K_SR8: (64 + 8) << 41, DB.K_255: 0o377, DB.K_ZERO: 0,
        DB.K_TK10: 10, DB.K_TK2: 2, DB.K_TK11: 11, DB.K_TK12: 12,
        DB.K_TK13: 13,
        DB.K_SUB30: 30, DB.K_SUB31: 31, DB.K_SUB34: 34, DB.K_SUB37: 37,
        DB.K_GOSTA: body[0o27], DB.K_GOSTB: body[0o30],
        DB.K_PRINT_BIAS: f32(0.0),
    }
    for off, v in zip(range(DB.K_WMASK0, DB.K_WMASK0 + 3), wm):
        dconsts[off] = v
    for off, v in zip(range(DB.K_CLEARM0, DB.K_CLEARM0 + 2), cm):
        dconsts[off] = v
    for off, v in zip(range(DB.K_SPACEM0, DB.K_SPACEM0 + 2), sm):
        dconsts[off] = v
    for off, v in dconsts.items():
        z2[off] = v & MASK
    for i in range(len(disp.hw) // 2):
        z2[DB.CODE_OFF + i] = word(disp.hw[2*i], disp.hw[2*i+1])
    if len(disp.hw) % 2:
        z2[DB.CODE_OFF + len(disp.hw)//2] = word(disp.hw[-1], DUMMY)

    c = consts(body)
    if patch_off is not None:
        c[patch_off] = patch_delta
    c[C_MODA] = 0; c[C_MODB] = 0; c[C_MODQ] = 0
    for off, v in c.items():
        z2[off] = v & MASK
    for off, w in a.code_words():
        z2[off] = w & MASK
    for off, w in intr.code_words():
        z2[off] = w & MASK
    # ITAB: LONG uj trampolines; PATCH redirects the SQRT slot to ABS.
    def raddr(name):
        return intr.ram_of_label(name)
    a_ram, s_ram, m_ram = raddr('I_ABS'), raddr('I_SQRT'), raddr('I_MOD')
    z2[ITAB0] = word(long_(UJ, a_ram), DUMMY)
    z2[ITAB1] = word(long_(UJ, a_ram if patch_intr else s_ram), DUMMY)
    z2[ITAB2] = word(long_(UJ, m_ram), DUMMY)
    wz(str(dst), N2, z2)

    sha = hashlib.sha256(dst.read_bytes()).hexdigest()
    used = [off for off, _ in a.code_words()]
    n2used = max(max(used) + 1, DB.CODE_OFF + len(disp.hw)//2 + 1, 512)
    print(f'case={case} sha={sha} N3={len(n3_hw)//2}/{MAX_WORDS}w '
          f'LEX={len(a.hw)}hw ({(len(a.hw)+1)//2}w) '
          f'B3disp={len(disp.hw)//2}w N2used={n2used}/649 '
          f'LEXentry={entry_ram:06o} '
          f'patch={patch_off}:{patch_delta}')
    return dst, sha, len(n3_hw)//2, (len(a.hw)+1)//2, n2used


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--build', required=True)
    ap.add_argument('--src')
    ap.add_argument('--patch-delta', type=int, default=None)
    ap.add_argument('--patch-off', type=int, default=None)
    ap.add_argument('--patch-intr', action='store_true')
    a = ap.parse_args()
    build(a.build, a.src, a.patch_delta, a.patch_off, patch_intr=a.patch_intr)
