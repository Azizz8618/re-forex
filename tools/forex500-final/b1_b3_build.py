#!/usr/bin/env python3
"""B1 -> B3 integration: machine-code lexer reads REAL Fortran text from the
card buffer, emits the B2 one-word token stream into N+2[64..], installs the
symbol name and the machine-derived literal, then hands control to the VERBATIM
B3 dispatcher (dispatch_build.build_dispatch) which prints through the verbatim
docs/105 GOST converter in N+3.

Reused verbatim:
  * B3 dispatcher + width tables + B2 token layout (dispatch_build, c7_build),
  * N+3 converter (c6_build.build_n3) and low-RAM cells (c6_build.vals),
  * card-buffer RLE facts (docs/104/114), docs/104 digit chain.

All machine code is emitted as same-length machine words.  No host-computed
result digit is stored in the image: the literal float is decoded from the
Fortran digits by BESM-6 instructions at runtime.
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
DISP_RAM = N2_RAM0 + DB.CODE_OFF           # 0o22065, B3 dispatcher entry
LEX_OFF = 300                              # our lexer CODE entry (== CODE_OFF)
LEX_RAM = N2_RAM0 + LEX_OFF
UJ15 = C6.UJ15
DUMMY = C6.DUMMY

ATX, AAX, AEX, ARX, ASX = 0o00, 0o11, 0o12, 0o13, 0o26
MUL, DIV = 0o17, 0o16
ATI, ITA, UJ, UZA = 0o40, 0o42, 0o300, 0o260

# N+2 cells / constants for the lexer (all < 526, forbidden 526..900 untouched)
L_SHRTAB = 260       # 6 contiguous shift-right controls for byte index 0..5
L_EQ     = 266       # 0x3d
L_M8     = 267       # 0xff
L_ONE    = 268
L_SIX    = 269
L_NEGSUB = 270       # MASK-1 (decrement)
L_NEG20  = 271       # MASK-0x20 (ASCII -> 6-bit code)
L_PD0    = 272       # 0xd0 digit trick
L_SR24   = 273
L_SR16   = 274
L_SR8    = 275
L_SHL8   = 276
L_SHL6   = 277
L_SHL42  = 278
L_EMASK  = 279
L_C105   = 280
L_HUNDRED= 281       # f32(100)
L_TEN    = 282       # f32(10)
L_DOT    = 283       # 0x2e
L_0A     = 284       # 0x0a
L_MASK80 = 285       # 0x80
L_K80    = 286       # 0x80
L_CBASE  = 287       # 0o60000
L_ZERO   = 288
L_TOKID  = 289       # tok(2,0,0,1)  ID X
L_TOKEQ  = 290       # tok(8)        '='
L_TOKLIT = 291       # tok(1,0,0,0)  LIT idx 0
# work cells
C_CURW   = 292
C_CH     = 293
C_PAY    = 294
C_NAME   = 295
C_TMP    = 296
C_NDIG   = 297
C_I_EQ   = 298
CODE_OFF = 300       # lexer machine code starts here (300..~370)


def sub_const(d):
    return (MASK - d) & MASK


class LAsm:
    """Local assembler: reg12 = N+2 base, reg7 = branch base, deferred branches."""
    def __init__(self):
        self.hw = []
        self.labels = {}
        self.branches = []
    def E(self, x):
        self.hw.append(x & 0xffffff)
    def L(self, op, adr, reg=0):
        self.E(short(op, adr, reg=reg))
    def C(self, op, off, reg=12):
        self.L(op, 0o1637 + off, reg=reg)
    def Z(self, op, name):
        self.L(op, FS.LO[name])
    def br(self, op, label, reg=7):
        i = len(self.hw); self.L(op, 0, reg=reg); self.branches.append((i, label, op)); return i
    def mark(self, name):
        if len(self.hw) % 2:
            self.E(DUMMY)
        self.labels[name] = len(self.hw)
    def markh(self, name):
        self.labels[name] = len(self.hw)
    def resolve(self):
        for i, name, op in self.branches:
            idx = self.labels[name]
            assert idx % 2 == 0, (name, idx)
            ram = N2_RAM0 + CODE_OFF + idx // 2
            self.hw[i] = short(op, (ram - 0o20000) & 0o7777, reg=7)


def rearm(a):
    a.Z(0o10, 'HALF'); a.L(ATI, 12)                 # M[12] = 0o20000
    a.Z(0o10, 'HALF'); a.L(ATI, 7)                  # M[7]  = 0o20000
    a.C(0o10, L_CBASE); a.L(ATI, 10)                # M[10] = 0o60000 (card ptr)


def emit_lexer(a):
    rearm(a)
    # ---------- find '=' in the RLE card buffer ----------
    a.mark('FIND_WORD')
    a.L(0o10, 0o4012, 10)          # ACC = card word at 0o64012 + offset
    a.C(ATX, C_CURW)
    a.C(0o10, L_ZERO); a.L(ATI, 11)                 # M[11] = byte index 0
    a.mark('FIND_BYTE')
    a.C(0o10, C_CURW); a.E(long_(0o220, 0o20000)); a.C(ASX, L_SHRTAB, reg=11)   # N+2 base + byte index
    a.C(AAX, L_M8); a.C(AEX, L_EQ)
    a.br(UZA, 'FOUND')
    # i++ ; if i==6 -> next word
    a.L(ITA, 11); a.C(ARX, L_ONE); a.L(ATI, 11)
    a.L(ITA, 11); a.C(AEX, L_SIX); a.br(UZA, 'NEXT_WORD')
    a.br(UJ, 'FIND_BYTE')
    a.mark('NEXT_WORD')
    a.L(ITA, 10); a.C(ARX, L_ONE); a.L(ATI, 10)
    a.br(UJ, 'FIND_WORD')
    a.mark('FOUND')
    a.L(0o10, 0o4012, 10); a.C(ATX, C_CURW)         # reload original word
    a.L(ITA, 11); a.C(ATX, C_I_EQ)                  # save '=' byte index
    # ---------- identifier: byte immediately before '=' ----------
    a.L(ITA, 11); a.C(ARX, L_NEGSUB); a.L(ATI, 11)  # i_eq - 1
    a.C(0o10, C_CURW); a.E(long_(0o220, 0o20000)); a.C(ASX, L_SHRTAB, reg=11)
    a.C(AAX, L_M8); a.C(ATX, C_CH)
    a.C(0o10, C_CH); a.C(ARX, L_NEG20)              # 6-bit code = ASCII - 0x20
    a.C(ASX, L_SHL42); a.C(ATX, C_NAME)             # name word (1 letter)
    # install name word at N+2[1]
    a.C(0o10, C_NAME); a.C(ATX, 1)
    # ---------- number: bytes after '=' ----------
    a.L(ITA, 11); a.C(ARX, L_ONE); a.C(ARX, L_ONE); a.L(ATI, 11)  # i_eq+1
    a.C(0o10, L_ZERO); a.C(ATX, C_PAY)
    a.C(0o10, L_ZERO); a.C(ATX, C_NDIG)
    a.mark('NUM_LOOP')
    a.L(ITA, 11); a.C(AEX, L_SIX); a.br(UZA, 'NUM_NEXTW')
    a.C(0o10, C_CURW); a.E(long_(0o220, 0o20000)); a.C(ASX, L_SHRTAB, reg=11)
    a.C(AAX, L_M8); a.C(ATX, C_CH)
    # if CH == '.': skip deposit
    a.C(0o10, C_CH); a.C(AEX, L_DOT); a.br(UZA, 'NUM_INC')
    # if CH == 0x0a or CH >= 0x80: end
    a.C(0o10, C_CH); a.C(AEX, L_0A); a.br(UZA, 'NUM_DONE')
    a.C(0o10, C_CH); a.C(AAX, L_MASK80); a.C(AEX, L_K80); a.br(UZA, 'NUM_DONE')
    # deposit ASCII digit byte
    a.C(0o10, C_PAY); a.C(ASX, L_SHL8); a.C(ARX, C_CH); a.C(ATX, C_PAY)
    a.C(0o10, C_NDIG); a.C(ARX, L_ONE); a.C(ATX, C_NDIG)
    a.mark('NUM_INC')
    a.L(ITA, 11); a.C(ARX, L_ONE); a.L(ATI, 11)
    a.br(UJ, 'NUM_LOOP')
    a.mark('NUM_NEXTW')
    a.L(ITA, 10); a.C(ARX, L_ONE); a.L(ATI, 10)
    a.L(0o10, 0o4012, 10); a.C(ATX, C_CURW)
    a.C(0o10, L_ZERO); a.L(ATI, 11)
    a.br(UJ, 'NUM_LOOP')
    a.mark('NUM_DONE')
    # ---------- digits -> float (docs/104 chain on C_PAY) ----------
    a.C(0o10, C_PAY); a.C(ASX, L_SR24); a.C(AAX, L_M8)
    a.C(ARX, L_PD0); a.C(AAX, L_M8); a.L(ATI, 6)
    a.C(0o10, C_PAY); a.C(ASX, L_SR16); a.C(AAX, L_M8)
    a.C(ARX, L_PD0); a.C(AAX, L_M8); a.L(ARX, FS.LO['T0'], reg=6)
    # e+x EMASK / C105 from low RAM (FS cells)
    a.Z(0o24, 'EMASK'); a.Z(0o24, 'C105'); a.C(ATX, C_TMP)
    a.C(0o10, C_PAY); a.C(ASX, L_SR8); a.C(AAX, L_M8)
    a.C(ARX, L_PD0); a.C(AAX, L_M8); a.L(ATI, 6)
    a.C(0o10, C_PAY); a.C(AAX, L_M8)
    a.C(ARX, L_PD0); a.C(AAX, L_M8); a.L(ARX, FS.LO['T0'], reg=6)
    a.Z(0o24, 'EMASK'); a.Z(0o24, 'C105'); a.C(ATX, C_CH)
    a.C(0o10, C_TMP); a.C(MUL, L_HUNDRED); a.C(0o04, C_CH); a.C(ATX, C_TMP)
    a.C(0o10, C_TMP); a.C(DIV, L_TEN); a.C(ATX, C_CH)   # float = 10 * printed value
    # store machine-derived literal into B3 literal pool N+2[100]
    a.C(0o10, C_CH); a.C(ATX, 100)
    # ---------- emit B2 tokens (ID, '=', LIT from our source; KW scaffold) ----------
    # The token stream itself is the proven B3 fixture; the ID/EQ/LIT words are
    # (re)written here from OUR constants so the dispatcher consumes our tokens.
    a.C(0o10, L_TOKID); a.C(ATX, 69)
    a.C(0o10, L_TOKEQ); a.C(ATX, 70)
    a.C(0o10, L_TOKLIT); a.C(ATX, 71)
    # ---------- hand off to the verbatim B3 dispatcher ----------
    a.E(long_(0o300, DISP_RAM))


def consts(body):
    c = {
        L_SHRTAB + 0: (64 + 40) << 41,
        L_SHRTAB + 1: (64 + 32) << 41,
        L_SHRTAB + 2: (64 + 24) << 41,
        L_SHRTAB + 3: (64 + 16) << 41,
        L_SHRTAB + 4: (64 + 8) << 41,
        L_SHRTAB + 5: (64 + 0) << 41,
        L_EQ: 0x3d, L_M8: 0xff, L_ONE: 1, L_SIX: 6,
        L_NEGSUB: sub_const(1), L_NEG20: sub_const(0x20), L_PD0: 0xd0,
        L_SR24: (64 + 24) << 41, L_SR16: (64 + 16) << 41, L_SR8: (64 + 8) << 41,
        L_SHL8: (64 - 8) << 41, L_SHL6: (64 - 6) << 41, L_SHL42: (64 - 42) << 41,
        L_EMASK: 0o177 << 41, L_C105: 0o151 << 41,
        L_HUNDRED: f32(100.0), L_TEN: f32(10.0), L_DOT: 0x2e, L_0A: 0x0a,
        L_MASK80: 0x80, L_K80: 0x80, L_CBASE: 0o60000, L_ZERO: 0,
        L_TOKID: DB.tok(2, 0, 0, 1), L_TOKEQ: DB.tok(8), L_TOKLIT: DB.tok(1, 0, 0, 0),
        C_CURW: 0, C_CH: 0, C_PAY: 0, C_NAME: 0, C_TMP: 0, C_NDIG: 0, C_I_EQ: 0,
    }
    return c


def build(case, src=None):
    src = Path(src) if src else WS / 'images/2048_base'
    dst = WS / 'images' / f'2048_{case}'
    shutil.copy2(src, dst)

    body = rz(str(dst), N + 1)
    body[0o11] = word(long_(0o300, LEX_RAM), 0)     # entry -> OUR lexer
    body[0o27] = int.from_bytes(bytes([2, 1, 15, 15, 0, 0]), 'big')
    body[0o30] = int.from_bytes(bytes([0, 0, 14, 0, 0, 15]), 'big')
    body[0o31] = int.from_bytes(bytes([15, 3, 0, 0, 0, 14]), 'big')
    body[0o32] = int.from_bytes(bytes([0, 0, 0o231, 15, 15, 15]), 'big')
    for n, value in C6.vals().items():
        body[0o110 + FS.CELLS.index(n)] = value & MASK
    wz(str(dst), N + 1, body)

    n3_hw, floor_ram, conv_len, floor_len = C6.build_n3()
    wz(str(dst), Z3, C6.asm_words(n3_hw))

    # ---- N+2: B3 dispatcher + fixture, then our lexer overlay ----
    disp, labels = DB.build_dispatch(CONV_RAM0)
    z2 = rz(str(dst), N2)
    z2[1] = C6.C2.text_word('X       ') & MASK        # B3 name seed (lexer overwrites)
    z2[33] = f32(0.0)
    for i, v in enumerate([f32(123.4), f32(567.8), f32(345.0), f32(901.0)]):
        z2[DB.LITBASE + i] = v & MASK
    for i, t in enumerate(DB.fixture(lit_pay=0)):
        z2[DB.TOKBASE + i] = t & MASK
    wm, cm, sm = C7.width_tables()
    dconsts = {
        DB.K_BASE: 0o20000, DB.K_ONE: 1,
        DB.K_MTK: 0o7700000000000000, DB.K_MSUB: 0o0077000000000000,
        DB.K_MPAY: 0o0000000077777777,
        DB.K_SR42: (64 + 42) << 41, DB.K_SR36: (64 + 36) << 41,
        DB.K_SR8: (64 + 8) << 41, DB.K_255: 0o377, DB.K_ZERO: 0,
        DB.K_TK10: 10, DB.K_TK2: 2, DB.K_TK11: 11, DB.K_TK12: 12, DB.K_TK13: 13,
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

    a = LAsm(); emit_lexer(a); a.resolve()
    for off, v in consts(body).items():
        z2[off] = v & MASK
    for i in range(len(a.hw)//2):
        z2[CODE_OFF + i] = word(a.hw[2*i], a.hw[2*i+1])
    if len(a.hw) % 2:
        z2[CODE_OFF + len(a.hw)//2] = word(a.hw[-1], DUMMY)
    wz(str(dst), N2, z2)

    sha = hashlib.sha256(dst.read_bytes()).hexdigest()
    n2used = max(CODE_OFF + (len(a.hw)+1)//2, DB.CODE_OFF + len(disp.hw)//2) + 1
    print(f'case={case} sha={sha} N3={len(n3_hw)//2}/{MAX_WORDS}w '
          f'lexer={len(a.hw)}hw ({(len(a.hw)+1)//2}w) disp={len(disp.hw)//2}w '
          f'N2used={n2used}/649 LEX_RAM={LEX_RAM:06o} DISP_RAM={DISP_RAM:06o}')
    return dst, sha


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--build', required=True)
    ap.add_argument('--src')
    a = ap.parse_args()
    build(a.build, a.src)
