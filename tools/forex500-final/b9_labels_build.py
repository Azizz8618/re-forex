#!/usr/bin/env python3
"""B7: REAL Fortran GOTO + arithmetic IF in the variant-B machine contour.

BASE: 2048_MODFINAL_B2 (all-feature image).  Copies only; no repo/live disk/C patch.
All control flow and all values are on the BESM-6; no IR card, no FRONT, no fixture.

Design (all NEW execution lives in OUR body RAM):
  * LEX emits a LABEL token (TK9, SUB=label, PAY=token index) when it sees a
    two-digit statement label in columns 4..5 (RLE byte 0x83).
  * GOTO is keyword TK10/SUB32, IF is TK10/SUB33 (arithmetic IF, three labels
    packed 8+8+8 in PAY).  Their label numbers are patched later by a machine
    pre-scan/fixup pass over the emitted token stream (before B4 runs).
  * B4 is reused verbatim except for TWO same-size branch replacements: the
    unknown-keyword fallback jumps to our body CONTROL processor, and EV_DONE
    jumps to our body POSTEVAL processor.  B4 stays 203 words.
  * IF condition uses the verbatim shunting-yard (EV_EVAL); POSTEVAL compares
    10*value against a body threshold word (the one-machine-word PATCH target).
"""
import argparse, hashlib, shutil, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import b5_build as B5
import c6_build as C6
import c7_build as C7
import final_sign as FS
from build_e2e import rz, wz, short, long_, word, f32, MASK, N, Z3
import b_final_do_build as BD
import b7_parser as PB7
import parser_build as PB

WS = HERE.parent
N2 = N + 2
N2_RAM0 = 0o21637
CONV_RAM0 = 0o30114
B4_RAM = N2_RAM0 + PB.CODE_OFF

ATX, AAX, AEX, ARX, ASX = 0o00, 0o11, 0o12, 0o13, 0o26
AVX, AOX = 0o14, 0o15
ADD, FSUB, DIV, MUL = 0o04, 0o06, 0o16, 0o17
SUB = 0o05                         # a-x float subtract
ATI, ITA, UJ, UZA = 0o40, 0o42, 0o300, 0o260
DUMMY = C6.DUMMY
UTC_N2 = long_(0o220, 0o20000)
LINK = 5

# ---------------------------------------------------------------- body cells
# Cells 82..95 of N+2 are token slots.  The base LEX kept 14 working cells
# there; with a longer GOTO/IF token stream those slots are overwritten by
# tokens.  Relocate all of them into free body RAM (docs/120), and let LAsm.C
# transparently emit a direct 12-bit ADR for them.
C_PAY=0o540; C_WIN3=0o541; C_WIN5=0o542; C_WIN6=0o543
C_FDESC_IDX=0o544; C_INTR=0o545; C_SQX=0o546
L_TXT_PRINT=0o547; L_TXT_FORMAT=0o550; L_TXT_END=0o551
L_MASK3=0o552; L_MASK5=0o553; L_SHL8=0o554; L_CH_S=0o555
# NEW cells
BW_WIN4=0o556; BW_WINIF=0o557
L_TXT_GOTO=0o560; L_TXT_IF=0o561; L_MASK4=0o562
BW_IFIDX=0o563; BW_GOTOIDX=0o564; BW_IFCOND=0o565; BW_IFNEG=0o566
BW_LBLDIG=0o567; BW_LBLACC=0o570; BW_LBLNUM=0o571
BW_L1=0o572; BW_L2=0o573; BW_L3=0o574
BW_PACK=0o575; BW_FIXIDX=0o576; BW_FIXTOK=0o577; BW_FIXTK=0o600
BW_FIXSUB=0o601; BW_IFACTIVE=0o602
# 0o603 is a zone descriptor and is never touched
BW_THRESH=0o604; BW_SHL36=0o605; BW_SHL16=0o606; BW_SHL8=0o607
BW_SHL4=0o645; BW_SHL24=0o646; BW_SR24=0o647; BW_MPOS=0o650
BW_MASK63=0o610; BW_NOTPAY=0o611
BW_TOKLABEL=0o612; BW_TOKIF=0o613; BW_TOKGOTO=0o614
BW_LBLDIG2=0o615; BW_TMPB=0o616; BW_ZERO=0o617
B7_M18=0o620; B7_M20=0o621; B7_M21=0o622; B7_TEN=0o623; B7_TWO=0o624
B7_TK9=0o625; B7_TK10=0o626; B7_SUB32=0o627; B7_SUB33=0o630
B7_BYTE84=0o631
BW_BYTE81=0o651; BW_BYTE82=0o652; BW_BYTE83=0o653
BW_IFPAY=0o632; BW_IFSUB=0o633
BW_IFVIDX=0o634; BW_IFRES=92
BW_ACC=0o635
BW_T1=0o636; BW_T2=0o637; BW_T3=0o640
BW_SHR16=0o641; BW_SHR8=0o642   # ASX right-shift controls for IF PAY extraction
BW_NLAB=0o643; BW_FOUND=0o644   # dense label table: count and lookup result
BW_TENI=B7_TEN
# Dense label table: LABTAB[0..31] = BCD label numbers, LABTAB[32..63] = token
# indexes.  Supports up to 32 distinct 1..3 digit labels (no 1000-word table).
LABTAB = 0o700
LABNUM = LABTAB
LABTOK = LABTAB + 32
BODY_CELLS = (set(range(0o540, 0o654)) | set(range(LABTAB, LABTAB + 64)))

# NEW machine code goes into free body slots above the label table.
CODE_REGIONS = [
    (901, 1023), (162, 199), (245, 259), (463, 525),
    (BD.BODY_SLOT + BD.BODY_CODE_FIRST, BD.BODY_SLOT + BD.BODY_CODE_LAST),
    (BD.BODY_SLOT + 0o740, BD.BODY_SLOT + 0o1235),
    (BD.BODY_SLOT + 0o1237, BD.BODY_SLOT + 0o1615),
]

class LAsm(BD.LAsm):
    def __init__(self):
        BD.LAsm.__init__(self)
        self.slots = []
        self.guard_targets = {}
        for i, (lo, hi) in enumerate(CODE_REGIONS):
            self.slots.extend(range(lo, hi))   # hi reserved for a LONG UJ guard
            nxt = CODE_REGIONS[i + 1][0] if i + 1 < len(CODE_REGIONS) else lo
            self.guard_targets[hi] = ram_of(nxt)
    def ram_of_label(self, name):
        hwidx = self.labels[name]
        off = self.slots[hwidx // 2]
        return ram_of(off) + (hwidx % 2)
    def resolve(self):
        for i, name, op in self.branches:
            hwidx = self.labels[name]
            off = self.slots[hwidx // 2]
            self.hw[i] = long_(op, ram_of(off) + (hwidx % 2))
        for i, name in self.calls:
            self.hw[i] = ((LINK << 20) | (0o31 << 15) | (self.ram_of_label(name) & 0o77777))
        if len(self.hw) % 2:
            self.E(DUMMY)
        assert (len(self.hw) + 1) // 2 <= len(self.slots), \
            f'LEX code overrun: {(len(self.hw)+1)//2} > {len(self.slots)}'
    def C(self, op, off, reg=12):
        if off in BODY_CELLS:
            return self.L(op, body_ram(off), reg=0)
        return super().C(op, off, reg=reg)

# MEASURED body-index -> RAM mapping (C-oracle CORE marker sweep, 2026-11-24).
# BD.body_ram is linear and is valid only for body[0o224..0o602]; our new data
# (0o604+) and code (0o740+) live in later loader segments with different bases.
def body_ram(idx):
    if idx < 0o604:  return 0o2223 + (idx - 0o224)
    if idx < 0o1236: return 0o2621 + (idx - 0o604)
    if idx < 0o1617: return 0o21066 + (idx - 0o1237)
    if idx < 0o1627: return 0o21452 + (idx - 0o1617)
    return 0o21467 + (idx - 0o1630)

def ram_of(off):
    if off >= BD.BODY_SLOT:
        return body_ram(off - BD.BODY_SLOT)
    return BD.tail_ram(off) if off >= 901 else (N2_RAM0 + off)

# ---------------------------------------------------------------- helpers
def emit_getch(a):
    a.mark('GETCH')
    a.L(ITA, 11); a.C(AEX, B5.L_SIX)
    a.br(UZA, 'GC_NEXTW')
    a.C(0o10, BD.C_CURW); a.E(UTC_N2)
    a.C(ASX, B5.L_SHRTAB, reg=11); a.C(AAX, B5.L_M8); a.C(ATX, BD.C_CH)
    a.L(ITA, 11); a.C(ARX, B5.L_ONE); a.L(ATI, 11)
    a.ret()
    a.mark('GC_NEXTW')
    a.L(ITA, 10); a.C(ARX, B5.L_ONE); a.L(ATI, 10)
    a.L(0o10, 0o4012, 10); a.C(ATX, BD.C_CURW)
    a.C(0o10, B5.L_ZERO); a.L(ATI, 11)
    a.br(UJ, 'GETCH')

def emit_emit(a):
    a.mark('EMIT')
    a.C(ATX, BD.C_TMP)
    a.C(0o10, BD.C_TOKPTR); a.L(ATI, 6)
    a.C(0o10, BD.C_TMP)
    a.E(UTC_N2); a.L(ATX, 0o1637 + B5.TOKBASE, reg=6)
    a.C(0o10, BD.C_TOKPTR); a.C(ARX, B5.L_ONE); a.C(ATX, BD.C_TOKPTR)
    a.ret()

def ec(a, cell):
    a.C(0o10, cell); a.call('EMIT')

def fetch_tok_for_fixup(a):
    """ACC (token index) -> token word in BW_FIXTOK."""
    a.C(ATX, BW_TMPB)
    a.C(0o10, BW_TMPB); a.L(ATI, 6)
    a.C(0o10, BW_TMPB)                  # restore index into ACC (unused here)
    a.E(UTC_N2); a.L(0o10, 0o1637 + B5.TOKBASE, reg=6)
    a.C(ATX, BW_FIXTOK)

def write_tok_for_fixup(a):
    a.C(0o10, BW_TMPB); a.L(ATI, 6)
    a.C(0o10, BW_FIXTOK)
    a.E(UTC_N2); a.L(ATX, 0o1637 + B5.TOKBASE, reg=6)

def skip_ws(a, lbl):
    a.C(0o10, BD.C_CH); a.C(AEX, B5.L_0X0A); a.br(UZA, lbl)
    a.C(0o10, BD.C_CH); a.C(AAX, B5.L_0X80); a.C(AEX, B5.L_0X80); a.br(UZA, lbl)

def is_digit(a, lbl):
    a.C(0o10, BD.C_CH); a.C(AAX, B5.L_0XF0); a.C(AEX, B5.L_0X30); a.br(UZA, lbl)

def reset_windows(a):
    a.C(0o10, B5.L_ZERO)
    a.C(ATX, B5.C_WIN2 if hasattr(B5,'C_WIN2') else 98)
    a.C(ATX, C_WIN3); a.C(ATX, BW_WIN4); a.C(ATX, C_WIN5); a.C(ATX, C_WIN6)
    a.C(ATX, BW_WINIF)

def kwindow(a, found_print, found_format, found_end, found_do, found_if, found_goto):
    a.C(0o10, 98); a.C(ASX, L_SHL8); a.C(ARX, BD.C_CH)
    a.L(AAX, BD.R_MASK2, reg=0); a.C(ATX, 98)
    a.C(0o10, C_WIN3); a.C(ASX, L_SHL8); a.C(ARX, BD.C_CH)
    a.C(AAX, L_MASK3); a.C(ATX, C_WIN3)
    a.C(0o10, BW_WIN4); a.C(ASX, L_SHL8); a.C(ARX, BD.C_CH)
    a.C(AAX, L_MASK4); a.C(ATX, BW_WIN4)
    a.C(0o10, C_WIN5); a.C(ASX, L_SHL8); a.C(ARX, BD.C_CH)
    a.C(AAX, L_MASK5); a.C(ATX, C_WIN5)
    a.C(0o10, C_WIN6); a.C(ASX, L_SHL8); a.C(ARX, BD.C_CH); a.C(ATX, C_WIN6)
    a.C(0o10, BW_WINIF); a.C(ASX, L_SHL8); a.C(ARX, BD.C_CH); a.C(ATX, BW_WINIF)
    a.C(0o10, C_WIN6); a.C(AEX, L_TXT_FORMAT); a.br(UZA, found_format)
    a.C(0o10, C_WIN5); a.C(AEX, L_TXT_PRINT);  a.br(UZA, found_print)
    a.C(0o10, BW_WIN4); a.C(AEX, L_TXT_GOTO); a.br(UZA, found_goto)
    a.C(0o10, 98); a.L(AEX, BD.R_TXT_DO, reg=0); a.br(UZA, found_do)
    a.C(0o10, C_WIN3); a.C(AEX, L_TXT_END);    a.br(UZA, found_end)
    a.C(0o10, BW_WINIF); a.C(AEX, L_TXT_IF);   a.br(UZA, found_if)

# ---------------------------------------------------------------- token stream
# B2 one-word token: (TK<<42)|(SUB<<36)|(POS<<24)|PAY
def tok(tk, sub=0, pos=0, pay=0):
    return ((tk & 0x3f) << 42) | ((sub & 0x3f) << 36) | ((pos & 0xfff) << 24) | (pay & 0xffffff)

T_LABEL = tok(9, 0, 0, 0)
T_GOTO  = tok(10, 32, 0, 0)
T_IF    = tok(10, 33, 0, 0)
MASK_NOTPAY = MASK ^ 0xffffff

def inline_fetchtok(a):
    a.C(ATX, BW_TMPB)
    a.C(0o10, BW_TMPB); a.L(ATI, 6)
    a.E(UTC_N2); a.L(0o10, 0o1637 + B5.TOKBASE, reg=6)
    a.C(ATX, BW_FIXTOK)

def inline_patchtok(a):
    a.C(ATX, BW_TMPB)
    a.C(0o10, BW_TMPB); a.L(ATI, 6)
    a.E(UTC_N2); a.L(0o10, 0o1637 + B5.TOKBASE, reg=6)
    a.C(AAX, BW_NOTPAY) if BW_NOTPAY in BODY_CELLS else a.L(AAX, body_ram(BW_NOTPAY), reg=0)
    a.C(AOX, BW_PACK)
    a.C(ATX, BW_FIXTOK)
    a.C(0o10, BW_TMPB); a.L(ATI, 6)
    a.C(0o10, BW_FIXTOK)
    a.E(UTC_N2); a.L(ATX, 0o1637 + B5.TOKBASE, reg=6)

# =============================================================== LEX
def build_lex(control_ram, posteval_ram, eval_ram):
    a = LAsm()
    emit_getch(a)
    emit_emit(a)
    a.mark('START')
    a.Z(0o10, 'HALF'); a.L(ATI, 12)
    a.Z(0o10, 'HALF'); a.L(ATI, 7)
    a.C(0o10, B5.L_CBASE); a.L(ATI, 10)
    a.L(0o10, 0o4012, 10); a.C(ATX, BD.C_CURW)
    a.C(0o10, B5.L_ZERO); a.L(ATI, 11)
    a.C(ATX, BD.C_TOKPTR); a.C(ATX, BD.C_POOLPTR); a.C(ATX, BD.C_MODE)
    a.C(ATX, C_INTR); a.C(ATX, BD.C_NAMED); a.C(ATX, C_PAY)
    a.C(ATX, BW_IFCOND); a.C(ATX, BW_IFNEG); a.C(ATX, BW_LBLDIG)
    a.C(ATX, BW_LBLACC); a.C(ATX, BW_LBLNUM); a.C(ATX, BW_IFACTIVE)
    reset_windows(a)
    for c in (B5.L_CSPROG, B5.L_CSX, B5.L_CSEOL):
        ec(a, c)

    a.mark('MAIN_LOOP')
    a.call('GETCH')
    a.mark('DISPATCH')
    a.C(0o10, BD.C_MODE); a.br(UZA, 'M_SCAN')
    a.C(0o10, BD.C_MODE); a.C(AEX, B5.L_ONE); a.br(UZA, 'M_EXPR')
    a.C(0o10, BD.C_MODE); a.C(AEX, B5.L_TWO); a.br(UZA, 'M_NUM')
    a.C(0o10, BD.C_MODE); a.C(AEX, BD.L_THREE); a.br(UZA, 'M_PLAB')
    a.C(0o10, BD.C_MODE); a.C(AEX, BD.L_FOUR); a.br(UZA, 'M_S4')
    a.C(0o10, BD.C_MODE); a.C(AEX, BD.L_FIVE); a.br(UZA, 'M_S5')
    a.C(0o10, BD.C_MODE); a.C(AEX, BD.L_SIX); a.br(UZA, 'M_S6')
    a.C(0o10, BD.C_MODE); a.L(AEX, BD.R_EIGHT, reg=0); a.br(UZA, 'M_DOLAB')
    a.C(0o10, BD.C_MODE); a.L(AEX, BD.R_NINE, reg=0); a.br(UZA, 'M_DOBND')
    a.C(0o10, BD.C_MODE); a.L(AEX, BD.R_TENI, reg=0); a.br(UZA, 'M_DOBODY')
    a.C(0o10, BD.C_MODE); a.L(AEX, BD.R_ELEVEN, reg=0); a.br(UZA, 'M_DONUM')
    a.C(0o10, BD.C_MODE); a.L(AEX, BD.R_FOURTEEN, reg=0); a.br(UZA, 'M_MODSTART')
    a.C(0o10, BD.C_MODE); a.L(AEX, BD.R_FIFTEEN, reg=0); a.br(UZA, 'M_MADDIG')
    a.C(0o10, BD.C_MODE); a.L(AEX, BD.R_SIXTEEN, reg=0); a.br(UZA, 'M_MODCOMMA')
    a.C(0o10, BD.C_MODE); a.L(AEX, BD.R_SEVENTEEN, reg=0); a.br(UZA, 'M_MODEND')
    a.C(0o10, BD.C_MODE); a.L(AEX, body_ram(B7_M18), reg=0); a.br(UZA, 'M_IFWAIT')
    a.C(0o10, BD.C_MODE); a.L(AEX, body_ram(B7_M20), reg=0); a.br(UZA, 'M_IFLAB')
    a.C(0o10, BD.C_MODE); a.L(AEX, body_ram(B7_M21), reg=0); a.br(UZA, 'M_GOTOLAB')
    a.br(UJ, 'M_S7')

    # ---- mode 0: scan source ----
    a.mark('M_SCAN')
    # RLE space byte 0x81..0x84 in columns 1..5 introduces a 4..1 digit label.
    for c in (B7_BYTE84, BW_BYTE83, BW_BYTE82, BW_BYTE81):
        a.C(0o10, BD.C_CH); a.L(AEX, body_ram(c), reg=0)
        a.br(UZA, 'LABEL_FOUND')
    a.C(0o10, BD.C_CH); a.C(AEX, B5.L_EQ); a.br(UZA, 'FOUND_EQ')
    skip_ws(a, 'MAIN_LOOP')
    kwindow(a, 'FOUND_PRINT', 'FOUND_FORMAT', 'FOUND_END', 'FOUND_DO',
            'FOUND_IF', 'FOUND_GOTO')
    a.C(0o10, BD.C_CH); a.C(ATX, BD.C_PREV)
    a.br(UJ, 'MAIN_LOOP')

    a.mark('LABEL_FOUND')
    # Consume 1..4 decimal digits with GETCH and accumulate a BCD label number
    # (4 bits per digit; 3 digits fit the 12-bit POS field of a token).
    a.C(0o10, B5.L_ZERO); a.C(ATX, BW_LBLACC)
    a.C(0o10, B5.L_ZERO); a.C(ATX, BW_LBLDIG)
    a.mark('LABEL_DIG_LOOP')
    a.call('GETCH')
    a.C(0o10, BD.C_CH); a.C(AAX, B5.L_0XF0); a.C(AEX, B5.L_0X30)
    a.br(UZA, 'LABEL_DIG_ACC')             # UZA after AEX means IS a digit
    a.br(UJ, 'LABEL_NOTDIG')
    a.mark('LABEL_DIG_ACC')
    a.C(0o10, BW_LBLACC); a.L(ASX, body_ram(BW_SHL4), reg=0); a.C(ATX, BW_LBLACC)
    a.C(0o10, BD.C_CH); a.C(AAX, B5.L_0X0F)
    a.C(ARX, BW_LBLACC); a.C(ATX, BW_LBLACC)
    a.C(0o10, BW_LBLDIG); a.C(ARX, B5.L_ONE); a.C(ATX, BW_LBLDIG)
    a.br(UJ, 'LABEL_DIG_LOOP')
    a.mark('LABEL_NOTDIG')
    # CH is now the delimiter (0x81 space or other).  Emit the LABEL token only
    # when at least one digit was consumed; then dispatch the delimiter.
    a.C(0o10, BW_LBLDIG); a.br(UZA, 'LABEL_DISPATCH')
    a.C(0o10, BW_LBLACC); a.L(ASX, body_ram(BW_SHL24), reg=0)
    a.L(AOX, body_ram(BW_TOKLABEL), reg=0); a.C(ATX, BW_PACK)
    a.C(0o10, BD.C_TOKPTR); a.C(AOX, BW_PACK); a.C(ATX, BW_PACK)
    a.C(0o10, BW_PACK); a.call('EMIT')
    a.mark('LABEL_DISPATCH')
    a.br(UJ, 'DISPATCH')

    # ---- '=' ----
    a.mark('FOUND_EQ')
    a.d(0o10, BD.RD_DOHIT); a.br(UZA, 'EQ_NORMAL')
    a.L(0o10, BD.R_TENI, reg=0); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('EQ_NORMAL')
    a.C(0o10, BD.C_PREV); a.C(ARX, B5.L_0X20)
    a.C(ASX, B5.L_SHL42); a.C(ATX, BD.C_TMP)
    a.C(0o10, BD.C_TMP); a.C(ATX, 1)
    ec(a, B5.L_CSX); ec(a, B5.L_CSEQ)
    a.C(0o10, B5.L_ONE); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'MAIN_LOOP')

    # ---- DO path (verbatim from base) ----
    a.mark('FOUND_DO')
    reset_windows(a)
    a.C(0o10, BD.L_THREE); a.C(ATX, BD.C_TOKPTR)
    a.C(0o10, B5.L_ZERO); a.d(ATX, BD.RD_DOPHASE); a.d(ATX, BD.RD_DOHIT)
    a.L(0o10, BD.R_EIGHT, reg=0); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('M_DOLAB')
    is_digit(a, 'DL_DIG')
    a.d(0o10, BD.RD_DOPHASE); a.br(UZA, 'DL_P0')
    a.C(0o10, BD.C_CH); a.C(AEX, BD.L_COMMA); a.br(UZA, 'DL_COMMA')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('DL_P0')
    a.C(0o10, B5.L_ONE); a.d(ATX, BD.RD_DOPHASE)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('DL_DIG')
    a.d(0o10, BD.RD_DOPHASE); a.br(UZA, 'DL_DIG1')
    a.d(0o10, BD.RD_DOPHASE); a.C(AEX, B5.L_ONE); a.br(UZA, 'DL_DIG2')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('DL_DIG1')
    a.C(0o10, BD.C_CH); a.d(ATX, BD.RD_DOLAB)
    a.C(0o10, B5.L_ONE); a.d(ATX, BD.RD_DOPHASE)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('DL_DIG2')
    a.d(0o10, BD.RD_DOLAB); a.C(ASX, BD.L_SHL8); a.C(ARX, BD.C_CH); a.d(ATX, BD.RD_DOLAB)
    a.C(0o10, BD.L_TWO); a.d(ATX, BD.RD_DOPHASE)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('DL_COMMA')
    a.L(0o10, BD.R_NINE, reg=0); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('M_DOBND')
    is_digit(a, 'DB_DIG')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('DB_DIG')
    a.C(0o10, BD.C_CH); a.C(AAX, B5.L_0X0F); a.d(ATX, BD.RD_BOUND)
    a.L(0o10, BD.R_TENI, reg=0); a.C(ATX, BD.C_MODE)
    a.C(0o10, B5.L_ONE); a.d(ATX, BD.RD_DOHIT)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('M_DOBODY')
    a.C(0o10, BD.C_CH); a.C(AEX, B5.L_PLUS); a.br(UZA, 'DB_PLUS')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('DB_PLUS')
    a.L(0o10, BD.R_ELEVEN, reg=0); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('M_DONUM')
    is_digit(a, 'DN_DIG')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('DN_DIG')
    a.C(0o10, B5.L_ZERO); a.C(ATX, BD.C_F)
    a.C(0o10, B5.L_100); a.C(ATX, BD.C_NFRAC)
    a.C(0o10, B5.L_ZERO); a.C(ATX, BD.C_SEEDOT)
    a.C(0o10, B5.L_TWO); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'M_NUM')

    # ---- MOD state machine (verbatim) ----
    a.mark('M_MODSTART')
    is_digit(a, 'MD_INIT')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('MD_INIT')
    a.C(0o10, B5.L_ZERO); a.C(ATX, BD.C_F)
    a.C(0o10, B5.L_100); a.C(ATX, BD.C_NFRAC)
    a.C(0o10, B5.L_ZERO); a.C(ATX, BD.C_SEEDOT)
    a.L(0o10, BD.R_FIFTEEN, reg=0); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'M_MADDIG')
    a.mark('M_MADDIG')
    is_digit(a, 'MD_DIG')
    a.C(0o10, BD.C_CH); a.C(AEX, B5.L_DOT); a.br(UZA, 'MD_DOT')
    a.br(UJ, 'MD_FINISH')
    a.mark('MD_DOT')
    a.C(0o10, B5.L_ONE); a.C(ATX, BD.C_SEEDOT)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('MD_DIG')
    a.C(0o10, BD.C_CH); a.C(AAX, B5.L_0X0F); a.C(ATX, BD.C_TMP2)
    a.C(0o10, BD.C_SEEDOT); a.br(UZA, 'MD_NOFRAC')
    a.C(0o10, BD.C_NFRAC); a.C(ARX, B5.L_ONE); a.C(ATX, BD.C_NFRAC)
    a.mark('MD_NOFRAC')
    a.C(0o10, BD.C_TMP2); a.Z(0o24, 'EMASK'); a.Z(0o24, 'C105'); a.C(ATX, BD.C_DF)
    a.C(0o10, BD.C_F); a.C(MUL, B5.L_TEN); a.C(ADD, BD.C_DF); a.C(ATX, BD.C_F)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('MD_FINISH')
    a.mark('MD_DIVLOOP')
    a.C(0o10, BD.C_NFRAC); a.C(AEX, B5.L_100); a.br(UZA, 'MD_STORE')
    a.C(0o10, BD.C_F); a.C(DIV, B5.L_TEN); a.C(ATX, BD.C_F)
    a.C(0o10, BD.C_NFRAC); a.C(ARX, B5.L_NEG1); a.C(ATX, BD.C_NFRAC)
    a.br(UJ, 'MD_DIVLOOP')
    a.mark('MD_STORE')
    a.d(0o10, BD.RD_MODARG); a.br(UZA, 'MD_STORE_A')
    a.C(AEX, B5.L_ONE); a.br(UZA, 'MD_STORE_B')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('MD_STORE_A')
    a.C(0o10, BD.C_F); a.d(ATX, BD.RD_MODA)
    a.C(0o10, B5.L_ONE); a.d(ATX, BD.RD_MODARG)
    a.L(0o10, BD.R_SIXTEEN, reg=0); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'DISPATCH')
    a.mark('MD_STORE_B')
    a.C(0o10, BD.C_F); a.d(ATX, BD.RD_MODB)
    a.C(0o10, BD.L_TWO); a.d(ATX, BD.RD_MODARG)
    a.L(0o10, BD.R_SEVENTEEN, reg=0); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'DISPATCH')
    a.mark('M_MODCOMMA')
    a.C(0o10, BD.C_CH); a.C(AEX, BD.L_COMMA); a.br(UZA, 'MC_COMMA')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('MC_COMMA')
    a.L(0o10, BD.R_FOURTEEN, reg=0); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'MAIN_LOOP')

    # ---- expression tokens (verbatim) ----
    a.mark('M_EXPR')
    is_digit(a, 'EXPR_DIGIT')
    a.C(0o10, C_INTR); a.br(UZA, 'EX_NOSQ')
    a.C(0o10, BD.C_CH); a.C(AEX, B5.L_MINUS); a.br(UZA, 'EX_SETNEG')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('EX_SETNEG')
    a.C(0o10, B5.L_ONE); a.d(ATX, BD.RD_NEG)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('EX_NOSQ')
    a.C(0o10, BD.C_NAMED); a.br(UZA, 'EX_CHKS')
    a.br(UJ, 'EX_OPCHK')
    a.mark('EX_CHKS')
    a.C(0o10, BD.C_CH); a.C(AEX, BD.L_CH_S); a.br(UZA, 'EX_GOTSQ')
    a.C(0o10, BD.C_CH); a.L(AEX, BD.R_CH_A, reg=0); a.br(UZA, 'EX_GOTABS')
    a.C(0o10, BD.C_CH); a.L(AEX, BD.R_CH_M, reg=0); a.br(UZA, 'EX_GOTMOD')
    a.br(UJ, 'EX_OPCHK')
    a.mark('EX_GOTSQ')
    a.C(0o10, BD.L_TWO); a.C(ATX, C_INTR)
    a.C(0o10, B5.L_ONE); a.C(ATX, BD.C_NAMED)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('EX_GOTABS')
    a.C(0o10, BD.L_THREE); a.C(ATX, C_INTR)
    a.C(0o10, B5.L_ONE); a.C(ATX, BD.C_NAMED)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('EX_GOTMOD')
    a.C(0o10, B5.L_ZERO); a.d(ATX, BD.RD_MODARG)
    a.L(0o10, BD.R_FOURTEEN, reg=0); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('EXPR_DIGIT')
    a.C(0o10, B5.L_ZERO); a.C(ATX, BD.C_F)
    a.C(0o10, B5.L_100); a.C(ATX, BD.C_NFRAC)
    a.C(0o10, B5.L_ZERO); a.C(ATX, BD.C_SEEDOT)
    a.C(0o10, B5.L_TWO); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'M_NUM')
    a.mark('EX_OPCHK')
    a.C(0o10, BD.C_CH); a.C(AEX, B5.L_PLUS);  a.br(UZA, 'EX_PLUS')
    a.C(0o10, BD.C_CH); a.C(AEX, B5.L_MINUS); a.br(UZA, 'EX_MINUS')
    a.C(0o10, BD.C_CH); a.C(AEX, B5.L_STAR);  a.br(UZA, 'EX_STAR')
    a.C(0o10, BD.C_CH); a.C(AEX, B5.L_SLASH); a.br(UZA, 'EX_SLASH')
    a.C(0o10, BD.C_CH); a.C(AEX, B5.L_LPC);   a.br(UZA, 'EX_LP')
    a.C(0o10, BD.C_CH); a.C(AEX, B5.L_RPC);   a.br(UZA, 'EX_RP')
    a.C(0o10, BD.C_CH); a.C(AEX, B5.L_0X0A);  a.br(UZA, 'EX_END')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('EX_PLUS');  ec(a, B5.L_OP1); a.br(UJ, 'MAIN_LOOP')
    a.mark('EX_MINUS'); ec(a, B5.L_OP2); a.br(UJ, 'MAIN_LOOP')
    a.mark('EX_STAR');  ec(a, B5.L_OP3); a.br(UJ, 'MAIN_LOOP')
    a.mark('EX_SLASH'); ec(a, B5.L_OP4); a.br(UJ, 'MAIN_LOOP')
    a.mark('EX_LP');    ec(a, B5.L_TOKLP); a.br(UJ, 'MAIN_LOOP')
    a.mark('EX_RP');    ec(a, B5.L_TOKRP); a.br(UJ, 'MAIN_LOOP')
    a.mark('EX_END')
    ec(a, B5.L_CSEOL)
    a.C(0o10, B5.L_ZERO); a.C(ATX, BD.C_MODE)
    reset_windows(a)
    a.br(UJ, 'DISPATCH')

    # ---- literal digits ----
    a.mark('M_NUM')
    a.C(0o10, BD.C_CH); a.C(AAX, B5.L_0XF0); a.C(AEX, B5.L_0X30); a.br(UZA, 'NUM_DIGIT')
    a.C(0o10, BD.C_CH); a.C(AEX, B5.L_DOT); a.br(UZA, 'NUM_DOT')
    a.C(0o10, B5.L_ONE); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'NUM_FINISH')
    a.mark('NUM_DOT')
    a.C(0o10, B5.L_ONE); a.C(ATX, BD.C_SEEDOT)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('NUM_DIGIT')
    a.C(0o10, BD.C_CH); a.C(AAX, B5.L_0X0F); a.C(ATX, BD.C_TMP2)
    a.C(0o10, BD.C_SEEDOT); a.br(UZA, 'NUM_NOFRAC')
    a.C(0o10, BD.C_NFRAC); a.C(ARX, B5.L_ONE); a.C(ATX, BD.C_NFRAC)
    a.mark('NUM_NOFRAC')
    a.C(0o10, BD.C_TMP2); a.Z(0o24, 'EMASK'); a.Z(0o24, 'C105'); a.C(ATX, BD.C_DF)
    a.C(0o10, BD.C_F); a.C(MUL, B5.L_TEN); a.C(ADD, BD.C_DF); a.C(ATX, BD.C_F)
    a.br(UJ, 'MAIN_LOOP')

    a.mark('NUM_FINISH')
    a.mark('NUM_DIV_LOOP')
    a.C(0o10, BD.C_NFRAC); a.C(AEX, B5.L_100); a.br(UZA, 'NUM_STORE')
    a.C(0o10, BD.C_F); a.C(DIV, B5.L_TEN); a.C(ATX, BD.C_F)
    a.C(0o10, BD.C_NFRAC); a.C(ARX, B5.L_NEG1); a.C(ATX, BD.C_NFRAC)
    a.br(UJ, 'NUM_DIV_LOOP')
    a.mark('NUM_STORE')
    a.d(0o10, BD.RD_DOHIT); a.br(UZA, 'NS_NORMAL')
    a.br(UJ, 'DO_ITER')
    a.mark('NS_NORMAL')
    a.d(0o10, BD.RD_NEG); a.br(UZA, 'NUM_NONEGCLEAR')
    a.C(0o10, BD.C_F); a.L(AVX, BD.R_SIGN, reg=0); a.C(ATX, BD.C_F)
    a.mark('NUM_NONEGCLEAR')
    a.C(0o10, C_INTR); a.br(UZA, 'NUM_NOSQ')
    a.C(0o10, C_INTR); a.C(AEX, BD.L_TWO); a.br(UZA, 'NUM_DOSQRT')
    a.br(UJ, 'NUM_DOABS')
    a.mark('NUM_DOSQRT')
    a.C(0o10, BD.C_F); a.C(ATX, BD.C_TMP); a.C(ATX, C_SQX)
    for _ in range(6):
        a.C(0o10, BD.C_TMP); a.C(DIV, C_SQX)
        a.C(0o04, C_SQX)
        a.C(MUL, BD.L_HALF); a.C(ATX, C_SQX)
    a.C(0o10, C_SQX); a.C(ATX, BD.C_F)
    a.br(UJ, 'NUM_CLRINTR')
    a.mark('NUM_DOABS')
    a.C(0o10, BD.C_F); a.C(ASX, B5.L_SHRTAB); a.C(AAX, B5.L_ONE)
    a.br(UZA, 'NUM_ABSDONE')
    a.C(0o10, BD.C_F); a.L(AVX, BD.R_SIGN, reg=0); a.C(ATX, BD.C_F)
    a.mark('NUM_ABSDONE')
    a.br(UJ, 'NUM_CLRINTR')
    a.mark('M_MODEND')
    a.C(0o10, BD.C_CH); a.C(AEX, B5.L_RPC); a.br(UZA, 'ME_RP')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('ME_RP')
    a.d(0o10, BD.RD_MODA); a.L(DIV, BD.RD_MODB, reg=0); a.d(ATX, BD.RD_MODQ)
    a.L(0o10, BD.R_MODMASK40, reg=0); a.L(ASX, BD.RD_MODQ, reg=0)
    a.L(AEX, BD.R_MODMASK40, reg=0); a.L(AOX, BD.R_EXPALL, reg=0)
    a.d(ATX, BD.RD_MODTMP)
    a.d(0o10, BD.RD_MODQ); a.L(AAX, BD.RD_MODTMP, reg=0); a.C(ATX, BD.C_F)
    a.d(0o10, BD.RD_MODB); a.C(MUL, BD.C_F); a.C(ATX, BD.C_F)
    a.d(0o10, BD.RD_MODA); a.C(SUB, BD.C_F); a.C(ATX, BD.C_F)
    a.C(0o10, BD.C_F); a.C(MUL, B5.L_TEN); a.C(ATX, 33)
    a.C(0o10, B5.L_ZERO); a.C(ATX, C_INTR); a.C(ATX, BD.C_NAMED)
    a.d(ATX, BD.RD_NEG); a.d(ATX, BD.RD_MODARG)
    a.C(0o10, BD.L_THREE); a.C(ATX, BD.C_TOKPTR)
    a.C(0o10, B5.L_ZERO); a.C(ATX, BD.C_MODE)
    reset_windows(a)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('NUM_CLRINTR')
    a.C(0o10, B5.L_ZERO); a.C(ATX, C_INTR); a.C(ATX, BD.C_NAMED); a.d(ATX, BD.RD_NEG)
    a.mark('NUM_NOSQ')
    a.C(0o10, BD.C_F); a.C(ATX, BD.C_TMP)
    a.C(0o10, BD.C_POOLPTR); a.L(ATI, 6)
    a.C(0o10, BD.C_TMP); a.E(UTC_N2)
    a.L(ATX, 0o1637 + B5.LITBASE, reg=6)
    a.C(0o10, BD.C_POOLPTR); a.C(AEX, B5.L_TOKLIT)
    a.call('EMIT')
    a.C(0o10, BD.C_POOLPTR); a.C(ARX, B5.L_ONE); a.C(ATX, BD.C_POOLPTR)
    # B7: IF condition literal -> emit expression terminator, enter label parser
    a.d(0o10, body_ram(BW_IFCOND)); a.br(UZA, 'NS_NOIF')
    ec(a, B5.L_CSEOL)
    a.C(0o10, B5.L_ZERO); a.d(ATX, body_ram(BW_IFCOND)); a.d(ATX, BD.RD_NEG)
    a.L(0o10, body_ram(B7_M20), reg=0); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('NS_NOIF')
    a.C(0o10, B5.L_ONE); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'DISPATCH')

    # ---- DO countdown (verbatim) ----
    a.mark('DO_ITER')
    a.C(0o10, BD.C_F); a.C(MUL, B5.L_TEN); a.d(ATX, BD.RD_ADDEND)
    a.d(0o10, BD.RD_BOUND); a.d(ATX, BD.RD_CNT)
    a.mark('DO_LOOP')
    a.C(0o10, 33); a.L(ADD, BD.RD_ADDEND, reg=0); a.C(ATX, 33)
    a.d(0o10, BD.RD_CNT); a.L(ARX, BD.R_DECR, reg=0); a.d(ATX, BD.RD_CNT)
    a.d(0o10, BD.RD_CNT); a.C(ASX, B5.L_SHRTAB); a.C(AAX, B5.L_ONE); a.C(AEX, B5.L_ONE)
    a.br(UZA, 'DO_DONE')
    a.br(UJ, 'DO_LOOP')
    a.mark('DO_DONE')
    a.C(0o10, B5.L_ZERO); a.d(ATX, BD.RD_DOHIT)
    a.C(0o10, B5.L_ZERO); a.C(ATX, BD.C_MODE)
    reset_windows(a)
    a.br(UJ, 'MAIN_LOOP')

    # ---- PRINT / FORMAT (verbatim) ----
    a.mark('FOUND_PRINT')
    reset_windows(a)
    ec(a, B5.L_CSPRINT)
    a.C(0o10, BD.L_THREE); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('M_PLAB')
    is_digit(a, 'PLAB_DIG')
    a.C(0o10, BD.C_CH); a.C(AEX, BD.L_COMMA); a.br(UZA, 'PLAB_COMMA')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('PLAB_DIG')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('PLAB_COMMA')
    a.C(0o10, BD.C_TOKPTR); a.C(ATX, C_FDESC_IDX)
    ec(a, BD.L_TOKFD)
    ec(a, B5.L_CSX)
    ec(a, B5.L_CSEOL)
    a.C(0o10, B5.L_ZERO); a.C(ATX, BD.C_MODE)
    reset_windows(a)
    a.br(UJ, 'DISPATCH')
    a.mark('FOUND_FORMAT')
    reset_windows(a)
    a.C(0o10, BD.L_FOUR); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('M_S4')
    a.C(0o10, BD.C_CH); a.C(AEX, BD.L_CH_F); a.br(UZA, 'S4_SEEF')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('S4_SEEF')
    a.C(0o10, BD.L_FIVE); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('M_S5')
    is_digit(a, 'S5_DIG')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('S5_DIG')
    a.C(0o10, BD.C_CH); a.C(AAX, B5.L_0X0F); a.C(ASX, BD.L_SHL8); a.C(ATX, C_PAY)
    a.C(0o10, BD.L_SIX); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('M_S6')
    a.C(0o10, BD.C_CH); a.C(AEX, B5.L_DOT); a.br(UZA, 'S6_SEEDOT')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('S6_SEEDOT')
    a.C(0o10, BD.L_SEVEN); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('M_S7')
    is_digit(a, 'S7_DIG')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('S7_DIG')
    a.C(0o10, BD.C_CH); a.C(AAX, B5.L_0X0F); a.C(ARX, C_PAY); a.C(ATX, C_PAY)
    a.C(0o10, C_FDESC_IDX); a.L(ATI, 6)
    a.C(0o10, BD.L_TOKFD); a.C(ARX, C_PAY)
    a.E(UTC_N2); a.L(ATX, 0o1637 + B5.TOKBASE, reg=6)
    a.C(0o10, B5.L_ZERO); a.C(ATX, BD.C_MODE)
    reset_windows(a)
    a.br(UJ, 'DISPATCH')

    # ================= B7: GOTO / IF keyword emission =================
    a.mark('FOUND_GOTO')
    reset_windows(a)
    a.C(0o10, BD.C_TOKPTR); a.d(ATX, body_ram(BW_GOTOIDX))
    ec(a, BW_TOKGOTO)
    a.C(0o10, B5.L_ZERO); a.d(ATX, body_ram(BW_LBLDIG)); a.d(ATX, body_ram(BW_LBLACC))
    a.L(0o10, body_ram(B7_M21), reg=0); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'MAIN_LOOP')

    a.mark('FOUND_IF')
    reset_windows(a)
    a.C(0o10, BD.C_TOKPTR); a.d(ATX, body_ram(BW_IFIDX))
    ec(a, BW_TOKIF)
    a.C(0o10, B5.L_ZERO); a.d(ATX, body_ram(BW_IFNEG)); a.d(ATX, body_ram(BW_IFCOND))
    a.L(0o10, body_ram(B7_M18), reg=0); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'MAIN_LOOP')

    # mode 18: wait for optional unary minus / first digit of IF condition
    a.mark('M_IFWAIT')
    a.C(0o10, BD.C_CH); a.C(AEX, B5.L_MINUS); a.br(UZA, 'IF_SETNEG')
    is_digit(a, 'IF_DIGIT')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('IF_SETNEG')
    a.C(0o10, B5.L_ONE); a.d(ATX, body_ram(BW_IFNEG))
    a.br(UJ, 'MAIN_LOOP')
    a.mark('IF_DIGIT')
    a.C(0o10, B5.L_ZERO); a.C(ATX, BD.C_F)
    a.C(0o10, B5.L_100); a.C(ATX, BD.C_NFRAC)
    a.C(0o10, B5.L_ZERO); a.C(ATX, BD.C_SEEDOT)
    a.d(0o10, body_ram(BW_IFNEG)); a.br(UZA, 'IF_POS')
    a.C(0o10, B5.L_ONE); a.d(ATX, BD.RD_NEG)
    a.br(UJ, 'IF_STARTNUM')
    a.mark('IF_POS')
    a.C(0o10, B5.L_ZERO); a.d(ATX, BD.RD_NEG)
    a.mark('IF_STARTNUM')
    a.C(0o10, B5.L_ONE); a.d(ATX, body_ram(BW_IFCOND))
    a.C(0o10, B5.L_TWO); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'M_NUM')

    # mode 20: IF labels are 1..3 decimal digits, comma separated.
    a.mark('M_IFLAB')
    is_digit(a, 'IFL_DIG')
    a.C(0o10, BD.C_CH); a.C(AEX, BD.L_COMMA); a.br(UZA, 'IFL_COMMA')
    a.C(0o10, BD.C_CH); a.C(AEX, B5.L_0X0A); a.br(UZA, 'IFL_FINISH')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('IFL_DIG')
    a.C(0o10, BD.C_CH); a.C(AAX, B5.L_0X0F); a.C(ATX, BW_TMPB)
    a.C(0o10, BW_LBLACC); a.L(ASX, body_ram(BW_SHL4), reg=0); a.C(ATX, BW_LBLACC)
    a.C(0o10, BW_TMPB); a.C(ARX, BW_LBLACC); a.C(ATX, BW_LBLACC)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('IFL_COMMA')
    a.C(0o10, BW_LBLNUM); a.br(UZA, 'IFL_ST1')
    a.C(0o10, BW_LBLACC); a.C(ATX, BW_L2)
    a.L(0o10, body_ram(B7_TWO), reg=0); a.C(ATX, BW_LBLNUM)
    a.br(UJ, 'IFL_RESET')
    a.mark('IFL_ST1')
    a.C(0o10, BW_LBLACC); a.C(ATX, BW_L1)
    a.C(0o10, B5.L_ONE); a.C(ATX, BW_LBLNUM)
    a.mark('IFL_RESET')
    a.C(0o10, B5.L_ZERO); a.C(ATX, BW_LBLACC)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('IFL_FINISH')
    a.C(0o10, BW_LBLACC); a.C(ATX, BW_L3)
    a.C(0o10, BW_L1); a.L(ASX, body_ram(BW_SHL16), reg=0); a.C(ATX, BW_PACK)
    a.C(0o10, BW_L2); a.L(ASX, body_ram(BW_SHL8), reg=0)
    a.C(AOX, BW_PACK); a.C(ATX, BW_PACK)
    a.C(0o10, BW_L3); a.C(AOX, BW_PACK); a.C(ATX, BW_PACK)
    a.C(0o10, BW_IFIDX); a.call('PATCHTOK')
    a.C(0o10, B5.L_ZERO); a.C(ATX, BD.C_MODE); a.C(ATX, BW_LBLNUM)
    a.C(ATX, BW_LBLACC)
    a.br(UJ, 'MAIN_LOOP')

    # mode 21: GOTO label is 1..3 decimal digits, terminated by end of card.
    a.mark('M_GOTOLAB')
    is_digit(a, 'GL_DIG')
    a.C(0o10, BD.C_CH); a.C(AEX, B5.L_0X0A); a.br(UZA, 'GL_FINISH')
    a.br(UJ, 'MAIN_LOOP')
    a.mark('GL_DIG')
    a.C(0o10, BD.C_CH); a.C(AAX, B5.L_0X0F); a.C(ATX, BW_TMPB)
    a.C(0o10, BW_LBLACC); a.L(ASX, body_ram(BW_SHL4), reg=0); a.C(ATX, BW_LBLACC)
    a.C(0o10, BW_TMPB); a.C(ARX, BW_LBLACC); a.C(ATX, BW_LBLACC)
    a.br(UJ, 'MAIN_LOOP')
    a.mark('GL_FINISH')
    a.C(0o10, BW_LBLACC); a.C(ATX, BW_PACK)
    a.C(0o10, BW_GOTOIDX); a.call('PATCHTOK')
    a.C(0o10, B5.L_ZERO); a.C(ATX, BD.C_MODE)
    a.br(UJ, 'MAIN_LOOP')

    # PATCHTOK: ACC = token index; BW_PACK = new PAY.  Read-modify-write token.
    a.mark('PATCHTOK')
    a.C(ATX, BW_TMPB)
    a.C(0o10, BW_TMPB); a.L(ATI, 6)
    a.E(UTC_N2); a.L(0o10, 0o1637 + B5.TOKBASE, reg=6)
    a.L(AAX, body_ram(BW_NOTPAY), reg=0)
    a.C(AOX, BW_PACK)
    a.C(ATX, BW_FIXTOK)
    a.C(0o10, BW_TMPB); a.L(ATI, 6)
    a.C(0o10, BW_FIXTOK)
    a.E(UTC_N2); a.L(ATX, 0o1637 + B5.TOKBASE, reg=6)
    a.ret()

    # ================= B9: pre-scan / fixup of 1..3 digit label references ==
    a.mark('FIXUP')
    # PASS 1: collect LABEL tokens into a dense (BCD number, token index) table.
    a.C(0o10, B5.L_ZERO); a.C(ATX, BW_NLAB)
    a.C(0o10, B5.L_ZERO); a.C(ATX, BW_FIXIDX)
    a.mark('FIX1_LOOP')
    a.C(0o10, BW_FIXIDX); a.C(AEX, BD.C_TOKPTR); a.br(UZA, 'FIX_PASS2')
    a.C(0o10, BW_FIXIDX); inline_fetchtok(a)
    a.C(0o10, BW_FIXTOK); a.C(AAX, PB.K_MTK); a.C(ASX, PB.K_SR42); a.C(ATX, BW_FIXTK)
    a.C(0o10, BW_FIXTK); a.L(AEX, body_ram(B7_TK9), reg=0); a.br(UZA, 'FIX1_LABEL')
    a.br(UJ, 'FIX1_NEXT')
    a.mark('FIX1_LABEL')
    a.C(0o10, BW_FIXTOK); a.C(AAX, BW_MPOS)
    a.L(ASX, body_ram(BW_SR24), reg=0); a.C(ATX, BW_TMPB)  # BCD label number
    a.C(0o10, BW_FIXTOK); a.C(AAX, PB.K_MPAY); a.C(ATX, BW_PACK)  # token index
    a.C(0o10, BW_NLAB); a.L(ATI, 6)
    a.C(0o10, BW_TMPB); a.L(ATX, body_ram(LABNUM), reg=6)
    a.C(0o10, BW_PACK); a.L(ATX, body_ram(LABTOK), reg=6)
    a.C(0o10, BW_NLAB); a.C(ARX, B5.L_ONE); a.C(ATX, BW_NLAB)
    a.mark('FIX1_NEXT')
    a.C(0o10, BW_FIXIDX); a.C(ARX, B5.L_ONE); a.C(ATX, BW_FIXIDX)
    a.br(UJ, 'FIX1_LOOP')

    # FIND_LABEL: ACC = BCD label -> BW_FOUND = matching token index (0 if none).
    a.mark('FIND_LABEL')
    a.C(ATX, BW_TMPB)
    a.C(0o10, B5.L_ZERO); a.L(ATI, 6)
    a.mark('FL_LOOP')
    a.L(ITA, 6); a.C(AEX, BW_NLAB); a.br(UZA, 'FL_NOTFOUND')
    a.L(0o10, body_ram(LABNUM), reg=6); a.C(AEX, BW_TMPB); a.br(UZA, 'FL_FOUND')
    a.L(ITA, 6); a.C(ARX, B5.L_ONE); a.L(ATI, 6)
    a.br(UJ, 'FL_LOOP')
    a.mark('FL_FOUND')
    a.L(0o10, body_ram(LABTOK), reg=6); a.C(ATX, BW_FOUND); a.ret()
    a.mark('FL_NOTFOUND')
    a.C(0o10, B5.L_ZERO); a.C(ATX, BW_FOUND); a.ret()

    # PASS 2: patch GOTO/IF label references via the resolved table.
    a.mark('FIX_PASS2')
    a.C(0o10, B5.L_ZERO); a.C(ATX, BW_FIXIDX)
    a.mark('FIX2_LOOP')
    a.C(0o10, BW_FIXIDX); a.C(AEX, BD.C_TOKPTR); a.br(UZA, 'FIX_DONE')
    a.C(0o10, BW_FIXIDX); inline_fetchtok(a)
    a.C(0o10, BW_FIXTOK); a.C(AAX, PB.K_MTK); a.C(ASX, PB.K_SR42); a.C(ATX, BW_FIXTK)
    a.C(0o10, BW_FIXTK); a.L(AEX, body_ram(B7_TK10), reg=0)
    a.br(UZA, 'FIX2_KEY')
    a.br(UJ, 'FIX2_NEXT')
    a.mark('FIX2_KEY')
    a.C(0o10, BW_FIXTOK); a.C(AAX, PB.K_MSUB); a.C(ASX, PB.K_SR36); a.C(ATX, BW_FIXSUB)
    a.C(0o10, BW_FIXSUB); a.L(AEX, body_ram(B7_SUB32), reg=0); a.br(UZA, 'FIX2_GOTO')
    a.C(0o10, BW_FIXSUB); a.L(AEX, body_ram(B7_SUB33), reg=0); a.br(UZA, 'FIX2_IF')
    a.br(UJ, 'FIX2_NEXT')
    a.mark('FIX2_GOTO')
    a.C(0o10, BW_FIXTOK); a.C(AAX, PB.K_MPAY); a.C(ATX, BW_PACK)
    a.call('FIND_LABEL')
    a.C(0o10, BW_FOUND); a.C(ATX, BW_PACK)
    a.C(0o10, BW_FIXIDX); inline_patchtok(a)
    a.br(UJ, 'FIX2_NEXT')
    a.mark('FIX2_IF')
    # one arithmetic IF per program: store resolved targets in BW_T1..T3
    a.C(0o10, BW_L1); a.call('FIND_LABEL'); a.C(0o10, BW_FOUND); a.C(ATX, BW_T1)
    a.C(0o10, BW_L2); a.call('FIND_LABEL'); a.C(0o10, BW_FOUND); a.C(ATX, BW_T2)
    a.C(0o10, BW_L3); a.call('FIND_LABEL'); a.C(0o10, BW_FOUND); a.C(ATX, BW_T3)
    a.mark('FIX2_NEXT')
    a.C(0o10, BW_FIXIDX); a.C(ARX, B5.L_ONE); a.C(ATX, BW_FIXIDX)
    a.br(UJ, 'FIX2_LOOP')
    a.mark('FIX_DONE')
    # FIXUP is entered inline from FOUND_END (not via VJM): FIND_LABEL uses the
    # same link register, so a nested CALL here would lose the return address.
    a.E(long_(UJ, B4_RAM))

    # ================= B7: B4 control processor (body) =================
    a.mark('CONTROL')
    a.C(0o10, PB.C_SUB); a.L(AEX, body_ram(B7_SUB32), reg=0); a.br(UZA, 'CTL_GOTO')
    a.C(0o10, PB.C_SUB); a.L(AEX, body_ram(B7_SUB33), reg=0); a.br(UZA, 'CTL_IF')
    a.E(long_(UJ, B4_RAM))
    a.mark('CTL_GOTO')
    a.C(0o10, PB.C_PAY); a.C(ATX, PB.C_SPC)
    a.E(long_(UJ, B4_RAM))
    a.mark('CTL_IF')
    a.C(0o10, PB.C_PAY); a.C(ATX, BW_IFPAY)      # EVAL overwrites C_PAY/C_SUB
    a.C(0o10, PB.C_SUB); a.C(ATX, BW_IFSUB)
    a.C(0o10, B5.L_ONE); a.d(ATX, body_ram(BW_IFACTIVE))
    a.C(0o10, BW_IFVIDX); a.C(ATX, PB.C_VIDX)   # IF result to N+2[32+60], not X word
    a.E(long_(UJ, eval_ram))

    a.mark('POSTEVAL')
    a.d(0o10, body_ram(BW_IFACTIVE)); a.br(UZA, 'PE_RETURN')
    a.C(0o10, B5.L_ZERO); a.d(ATX, body_ram(BW_IFACTIVE))
    # value - threshold; opcode 0o05 = a-x
    a.C(0o10, BW_IFRES); a.L(SUB, body_ram(BW_THRESH), reg=0)
    a.C(AEX, PB.K_ZERO)                     # logical mode => UZA tests true zero
    a.br(UZA, 'PE_ZERO')                    # exactly zero => second label
    a.C(ASX, B5.L_SHRTAB); a.C(AAX, B5.L_ONE)
    a.br(UZA, 'PE_POS')                     # non-negative => third label
    a.C(0o10, BW_T1); a.C(ATX, PB.C_SPC)   # negative -> first label
    a.E(long_(UJ, B4_RAM))
    a.mark('PE_ZERO')
    a.C(0o10, BW_T2); a.C(ATX, PB.C_SPC)   # zero -> second label
    a.E(long_(UJ, B4_RAM))
    a.mark('PE_POS')
    a.C(0o10, BW_T3); a.C(ATX, PB.C_SPC)   # positive -> third label
    a.mark('PE_RETURN')
    a.E(long_(UJ, B4_RAM))

    # ---- END: emit END, run label fixup, hand off ----
    a.mark('FOUND_END')
    ec(a, B5.L_CSEND)
    a.br(UJ, 'FIXUP')
    a.resolve()
    return a

# ---------------------------------------------------------------- constants
def lex_consts():
    c = BD.lex_consts()
    # remove the cells we relocated to body (they are written separately)
    for k in (C_PAY, C_WIN3, C_WIN5, C_WIN6, C_FDESC_IDX, C_INTR, C_SQX,
              L_TXT_PRINT, L_TXT_FORMAT, L_TXT_END, L_MASK3, L_MASK5,
              L_SHL8, L_CH_S):
        c.pop(k, None)
    c[98] = 0                                   # C_WIN2 remains in N+2
    return c

def body_consts():
    c = {
        C_PAY:0, C_WIN3:0, C_WIN5:0, C_WIN6:0, C_FDESC_IDX:0, C_INTR:0, C_SQX:0,
        L_TXT_PRINT:0x5052494e54, L_TXT_FORMAT:0x464f524d4154, L_TXT_END:0x00454e44,
        L_MASK3:0xffffff, L_MASK5:(1 << 40)-1, L_SHL8:(64-8) << 41, L_CH_S:0x53,
        BW_WIN4:0, BW_WINIF:0,
        L_TXT_GOTO:0x474f544f, L_TXT_IF:0x4946, L_MASK4:0xffffffff,
        BW_IFIDX:0, BW_GOTOIDX:0, BW_IFCOND:0, BW_IFNEG:0,
        BW_LBLDIG:0, BW_LBLACC:0, BW_LBLNUM:0, BW_L1:0, BW_L2:0, BW_L3:0,
        BW_PACK:0, BW_FIXIDX:0, BW_FIXTOK:0, BW_FIXTK:0, BW_FIXSUB:0,
        BW_IFACTIVE:0, BW_THRESH:f32(0.0),
        BW_SHL36:(64-36) << 41, BW_SHL16:(64-16) << 41, BW_SHL8:(64-8) << 41,
        BW_MASK63:0xff, BW_NOTPAY:MASK_NOTPAY,
        BW_TOKLABEL:T_LABEL, BW_TOKIF:T_IF, BW_TOKGOTO:T_GOTO,
        BW_LBLDIG2:0, BW_TMPB:0, BW_ZERO:0,
        B7_M18:18, B7_M20:20, B7_M21:21, B7_TEN:10,
        B7_TK9:9, B7_TK10:10, B7_SUB32:32, B7_SUB33:33,
        B7_BYTE84:0x84,
        BW_IFPAY:0, BW_IFSUB:0,
        BW_IFVIDX:60, BW_ACC:0, BW_T1:0, BW_T2:0, BW_T3:0,
        BW_SHR16:(64+16)<<41, BW_SHR8:(64+8)<<41,
        B7_TWO:2,
        BW_SHL4:(64-4)<<41, BW_SHL24:(64-24)<<41,
        BW_SR24:(64+24)<<41, BW_MPOS:0xfff000000,
        BW_NLAB:0, BW_FOUND:0,
        BW_BYTE81:0x81, BW_BYTE82:0x82, BW_BYTE83:0x83,
    }
    return c

# ---------------------------------------------------------------- build
def build(case, patch=False, src=None):
    src = Path(src) if src else WS / 'images/2048_base'
    dst = WS / 'images' / f'2048_{case}'
    shutil.copy2(src, dst)

    # B4 pass 0: only to learn EVAL's address (length is hook-independent)
    parser0, plabels = PB7.build_parser(CONV_RAM0, control_ram=0, posteval_ram=0)

    # N+1 body: base setup + B7 data/code
    body = rz(str(dst), N + 1)
    body[0o11] = word(long_(0o300, 0), 0)       # patched after LEX layout
    body[0o27] = int.from_bytes(bytes([2,1,15,15,0,0]), 'big')
    body[0o30] = int.from_bytes(bytes([0,0,14,0,0,15]), 'big')
    body[0o31] = int.from_bytes(bytes([15,3,0,0,0,14]), 'big')
    body[0o32] = int.from_bytes(bytes([0,0,0o231,15,15,15]), 'big')
    for n, v in C6.vals().items():
        body[0o110 + FS.CELLS.index(n)] = v & MASK
    for idx in (BD.D_DOLAB, BD.D_DOPHASE, BD.D_DOHIT, BD.D_BOUND, BD.D_CNT,
                BD.D_ADDEND, BD.D_NEG, BD.D_MODARG, BD.D_MODA, BD.D_MODB,
                BD.D_MODQ, BD.D_MODTMP):
        body[idx] = 0
    body[BD.L_SIGN]=1<<40; body[BD.L_CH_A]=0x41; body[BD.L_CH_M]=0x4d
    body[BD.L_TWELVE]=12; body[BD.L_THIRTEEN]=13
    body[BD.L_FOURTEEN]=14; body[BD.L_FIFTEEN]=15; body[BD.L_SIXTEEN]=16
    body[BD.L_SEVENTEEN]=17
    body[BD.L_MODMASK40]=0xffffffffff
    body[BD.L_EXPALL]=(0o177<<41)|(1<<40)
    body[BD.L_EIGHT]=8; body[BD.L_NINE]=9; body[BD.L_TENI]=10
    body[BD.L_ELEVEN]=11; body[BD.L_MASK2]=0xffff
    body[BD.L_TXT_DO]=0x444f; body[BD.L_DECR]=MASK^1
    for idx, v in body_consts().items(): body[idx] = v & MASK
    if patch:
        body[BW_THRESH] = f32(20.0) & MASK

    # Entry address: compute after the LEX is assembled.  The LEX entry must be
    # body[0o11]; find its RAM address from the assembled LEX label START.
    # (control/posteval/eval addresses are B4-relative, independent of LEX.)
    eval_ram = B4_RAM + plabels['EVAL'] // 2
    # Two passes: first assemble with dummy control/posteval RAMs to learn START;
    # control/posteval live in the LEX assembler's body code, so their addresses
    # are known only after assembly.  Use fixed placeholder addresses far away
    # and then fix the long UJ words by label resolution in LAsm.
    a = build_lex(0, 0, eval_ram)
    control_ram = a.ram_of_label('CONTROL')
    posteval_ram = a.ram_of_label('POSTEVAL')
    entry_ram = a.ram_of_label('START')
    # reassemble with correct absolute addresses
    # now build the REAL B4 with the resolved body addresses
    parser, plabels = PB7.build_parser(CONV_RAM0, control_ram, posteval_ram)
    a = build_lex(control_ram, posteval_ram, eval_ram)
    assert a.ram_of_label('CONTROL') == control_ram
    assert a.ram_of_label('POSTEVAL') == posteval_ram
    entry_ram = a.ram_of_label('START')
    body[0o11] = word(long_(0o300, entry_ram, reg=0), 0)
    for off, w in a.code_words():
        if off >= BD.BODY_SLOT:
            body[off - BD.BODY_SLOT] = w & MASK
    wz(str(dst), N + 1, body)

    n3_hw, _, _, _ = C6.build_n3()
    wz(str(dst), Z3, C6.asm_words(n3_hw))

    z2 = rz(str(dst), N2)
    z2[1] = C6.C2.text_word('X       ') & MASK
    z2[33] = f32(0.0)
    for i in range(4): z2[B5.LITBASE+i] = f32(0.0)
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
        PB.K_NEG1:MASK^1, PB.K_TEN:f32(10.0), PB.K_PATCH:f32(0.0),
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

    for i in range(len(parser.hw)//2):
        z2[PB.CODE_OFF+i] = word(parser.hw[2*i], parser.hw[2*i+1])
    if len(parser.hw) % 2:
        z2[PB.CODE_OFF+len(parser.hw)//2] = word(parser.hw[-1], DUMMY)
    for off, v in lex_consts().items(): z2[off] = v & MASK
    for off, w in a.code_words():
        if off < BD.BODY_SLOT: z2[off] = w & MASK
    wz(str(dst), N2, z2)

    sha = hashlib.sha256(dst.read_bytes()).hexdigest()
    n2offsets=[off for off,_ in a.code_words() if off < BD.BODY_SLOT]
    n2used=max(n2offsets)+1 if n2offsets else 0
    bodycode=[off-BD.BODY_SLOT for off,_ in a.code_words() if off >= BD.BODY_SLOT]
    print(f'case={case} sha={sha} N3={len(n3_hw)//2}/58w '
          f'B4={len(parser.hw)//2}w LEX={len(a.hw)//2}hw slots={len(a.slots)} '
          f'N2last={n2used} bodycode={len(bodycode)}w '
          f'bodyfirst={min(bodycode) if bodycode else -1} patch={patch}')
    return dst, sha

if __name__ == '__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--build', required=True)
    ap.add_argument('--patch', action='store_true')
    ap.add_argument('--src')
    x=ap.parse_args()
    build(x.build, patch=x.patch, src=x.src)
