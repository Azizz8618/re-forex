#!/usr/bin/env python3
"""C6: DO-loop fixture driven by IR records, on the proven C2b scanner.

Copies only. Reuses the canonical docs/105 GOST converter + sign block + both
reclaims + shared floor_int VERBATIM in zone N+3 (as a VJM subroutine). The
C2b multi-record scanner/dispatch/readers are reused verbatim in zone N+2;
a third 777005 record (TK=6 TEST FIXTURE, not a native FRONT record) drives a
machine loop whose counter/bound/accumulator live in N+2. The accumulated
result is fed into the verbatim GOST print path.
"""
import argparse, hashlib, shutil, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import final_build as FB
import final_sign as FS
import c2_build as C2
from build_e2e import rz, wz, short, long_, word, f32, MASK, N, Z3, MAX_WORDS

WS = HERE.parent
FS.LO['HUNDRED'] = FS.LO['HALF']   # LIT x100 recombination constant cell
N2 = N + 2
N2_RAM0 = 0o21637
N2_CODE_OFF = 200
N2_CODE_RAM = N2_RAM0 + N2_CODE_OFF          # 0o22003
CONV_RAM0 = 0o30114

# opcodes
ATX, AAX, AEX, ARX, ASX = 0o00, 0o11, 0o12, 0o13, 0o26
DIV, MUL, FADD, FSUB = 0o16, 0o17, 0o04, 0o06
ATI, EPLUSX, E64, ASN, ITA, UJ = 0o40, 0o24, 0o64, 0o36, 0o42, 0o300
UZA, VJM_OP, UTC = 0o260, 0o310, 0o220
DUMMY = FB.DUMMY
UJ15 = FB.UJ15

# link registers (odd, long VJM): outer calls reg=9, inner floor calls reg=11
LINK_OUT = 9
LINK_IN = 11

# N+2 constants (offsets)
K_BASE   = 110   # 0o20000 short-branch base into N+2 code
K_CBASE  = 111   # 0o60000 card buffer base
K_ONE    = 112   # 1
K_FOUR   = 113   # 4
K_MARK   = 114   # marker word 0o823737373030
K_SR24   = 115   # (64+24)<<41
K_28     = 116   # 28
K_SP7    = 117   # 7x 6-bit spaces
K_SHL42  = 118   # (64-42)<<41 = 22<<41
K_NEGONE = 119   # -1
K_HUNDRED = 120  # f32(100.0) for LIT x100 recombination
K_PTR = 121      # persistent card pointer (0o60000 + word offset)
K_GOSTA = 122    # seed for GOST print word A (sign byte = space)
K_GOSTB = 123    # seed for GOST print word B (digit slots zero)
K_TWENTY8 = K_28
# ---- C6 additions (N+2 cells, all inside proven-free offsets 0..525) ----
K_ZERO   = 124   # integer/float zero for accumulator init
K_DECR   = 125   # one's-complement -1: loop counter decrement
K_DO_KIND = 126  # 6: expected TK of the DO fixture record
L_BOUND  = 130   # loop bound, decoded from TA of the TK=6 record
L_STEP   = 131   # loop step, decoded from TB of the TK=6 record
L_CNT    = 132   # live loop counter
L_SUM    = 133   # accumulator (fed to EST -> GOST print)
L_VAL    = 134   # per-iteration addend (f32(10000.0)); PATCH changes this word

# low-RAM extra: HALF cell reused as HUNDRED (f32 100.0)
def ram_n2(off):
    return N2_RAM0 + off

def vjm_imm(addr, reg):
    return (reg << 20) | (0o31 << 15) | (addr & 0o77777)

def ret_imm(reg):
    return (reg << 20) | (0o30 << 15)

def shl42_const():
    # ASX control to shift LEFT 42: n=(C&0o177)-64=-42 -> C&0o177=22
    return (64 - 42) << 41

def spaces7():
    # TEXT code for space = ASCII 0x20 - 0x20 = 0; 7 trailing spaces are zero.
    return 0

class Code:
    def __init__(self):
        self.hw = []
    def E(self, x):
        self.hw.append(x & 0xffffff)
    def L(self, op, adr, reg=0):
        self.E(short(op, adr, reg=reg))
    def Z(self, op, name, reg=0):
        self.L(op, FS.LO[name], reg=reg)
    def C(self, op, koff, reg=12):
        # operand in N+2 constant cell: reg12 holds 0o20000; N2 RAM = 0o20000+0o1637+k
        self.L(op, 0o1637 + koff, reg=reg)
    def uza(self, target_ram, reg=7):
        self.L(UZA, target_ram - 0o20000, reg=reg)
    def vjmo(self, addr):
        if len(self.hw) % 2 == 0:
            self.E(vjm_imm(addr, LINK_OUT)); self.E(DUMMY)
        else:
            self.E(vjm_imm(addr, LINK_OUT))

# ---------------- N+3: converter as VJM subroutine (verbatim chain) ----------------
class Conv(FS.S):
    """Emit the canonical converter into self.hw; calls floor_int via reg11."""
    def VJM(self, addr):
        # override: use inner link register
        if len(self.hw) % 2 == 0:
            self.E(vjm_imm(addr, LINK_IN)); self.E(DUMMY)
        else:
            self.E(vjm_imm(addr, LINK_IN))
    def conv_body(self, floor_ram):
        self.sub_ram = floor_ram
        self.converter(True, 'plain', True, True)   # sign, drop_last_ati, floor_acc
        self.L(E64, 0o2004)
        if len(self.hw) % 2:
            self.E(DUMMY)
        self.E(ret_imm(LINK_OUT))
        return self.hw

def build_n3():
    # floor_int: 5 hw + RET11
    fl = FS.S()
    fl.sub_ram = 0
    fl.floor_acc()
    fl.E(ret_imm(LINK_IN))
    floor_hw = fl.hw[:]
    floor_off_word = None   # computed after conv length known
    # dry run conv with placeholder floor addr
    c = Conv(); c.conv_body(0o30114)
    conv_hw_est = c.hw[:]
    conv_words = (len(conv_hw_est) + 1) // 2
    floor_start_word = conv_words
    floor_ram = CONV_RAM0 + floor_start_word
    # rebuild with correct floor address
    c = Conv(); conv_hw = c.conv_body(floor_ram)
    assert len(conv_hw) == len(conv_hw_est)
    # VJM returns to a WORD boundary: pad so the subroutine starts at its left half.
    if len(conv_hw) % 2:
        conv_hw.append(DUMMY)
    total = conv_hw + floor_hw
    return total, floor_ram, len(conv_hw), len(floor_hw)

# ---------------- N+2: scanner / dispatch / readers ----------------
def build_n2(floor_ram, conv_ram):
    c = Code()
    H = c.hw

    # Base registers are re-armed before every step: the converter clobbers
    # some of them, so persistence lives in the N+2 cell K_PTR and low-RAM HALF.
    def rearm():
        c.Z(0o10, 'HALF')        # HALF = 0o20000 (low RAM, never touched by converter)
        c.L(ATI, 12)             # M[12 dec] = N+2 base 0o20000
        c.C(0o10, K_BASE)        # 0o20000 branch base
        c.L(ATI, 7)
        c.C(0o10, K_PTR)         # persistent card pointer
        c.L(ATI, 10)             # M[10 dec] = card base ptr
    rearm()

    # Labels resolved after emission (patch by index). Branches land on WORD
    # boundaries, so each target must be at an even halfword index.
    labels = {}
    def mark(name):
        if len(H) % 2:
            H.append(DUMMY)
        labels[name] = len(H)

    def emit_scan(tag):
        rearm()
        mark(tag + '_LOOP')
        c.L(0o10, 0o4012, 10)     # card word at M[10]+4012
        c.C(AEX, K_MARK)          # XOR marker
        labels[tag + '_UZA'] = len(H)
        c.L(UZA, 0, reg=7)        # patched: branch to FOUND
        c.L(0o10, 0, 10)          # ACC = ptr
        c.C(ARX, K_ONE)           # +1
        c.L(ATI, 10)
        labels[tag + '_UJ'] = len(H)
        c.L(UJ, 0, reg=7)         # patched: branch to LOOP
        mark(tag + '_FOUND')

    def emit_process(tag):
        rearm()
        # ---- TK from W1 byte4: shift right 8, PD0, mask ----
        c.L(0o10, 0o4013, 10)
        c.Z(ASX, 'SR8')
        c.Z(AAX, 'M8')
        c.Z(ARX, 'PD0')
        c.Z(AAX, 'M8')
        c.L(ATI, 5)               # M[5] = TK
        c.C(AEX, K_ONE)           # TK XOR 1 -> 0 iff LIT
        labels[tag+'_TK_UZA'] = len(H)
        c.L(UZA, 0, reg=7)        # patched: TK==1 -> LIT
        # ---- TK==2: VAR path ----
        # two-digit VIDX at W2 bytes 2,3
        c.L(0o10, 0o4014, 10)
        c.C(ASX, K_SR24); c.Z(AAX, 'M8'); c.Z(ARX, 'PD0'); c.Z(AAX, 'M8')
        c.L(ATI, 6)               # M[6] = tens
        c.L(0o10, 0o4014, 10)
        c.Z(ASX, 'SR16'); c.Z(AAX, 'M8'); c.Z(ARX, 'PD0'); c.Z(AAX, 'M8')
        c.L(ARX, FS.LO['T0'], reg=6)  # ACC += 10*tens
        c.L(ATI, 6)               # M[6] = VIDX
        c.Z(ATX, 'CARD')          # save VIDX in CARD cell
        # expected TEXT name = (VIDX+28)<<42 | SP7
        c.C(ARX, K_28)
        c.C(ASX, K_SHL42)
        c.C(ARX, K_SP7)
        c.Z(ATX, 'NUM')           # expected name in NUM cell
        # actual name word at N+2[VIDX]
        c.E(long_(UTC, 0o20000))
        c.L(0o10, 0o1637, reg=6)
        c.Z(AEX, 'NUM')           # XOR -> 0 if match
        labels[tag+'_NAME_UZA'] = len(H)
        c.L(UZA, 0, reg=7)        # patched: match -> OK
        # mismatch: EST = 0 (prints 0000.00) - detectable
        c.Z(ATX, 'EST')
        labels[tag+'_NAME_UJ'] = len(H)
        c.L(UJ, 0, reg=7)         # patched: -> after OK
        mark(tag+'_NAME_OK')
        # value word at N+2[32+VIDX]
        c.E(long_(UTC, 0o20000))
        c.L(0o10, 0o1637 + 32, reg=6)
        c.Z(DIV, 'TEN')
        c.Z(ATX, 'EST')
        mark(tag+'_PROC_END')
        labels[tag+'_END_UJ'] = len(H)
        c.L(UJ, 0, reg=7)        # patched: skip LIT reader
        # ---- TK==1: LIT 4-digit reader (pointer relative) ----
        mark(tag+'_LIT')
        c.L(0o10, 0o4014, 10)     # W2 card word
        c.Z(ATX, 'CARD')
        # d1*10+d2 -> float 12
        c.C(ASX, K_SR24); c.Z(AAX, 'M8'); c.Z(ARX, 'NEG31')
        c.L(ATI, 6)
        c.Z(0o10, 'CARD'); c.Z(ASX, 'SR16'); c.Z(AAX, 'M8'); c.Z(ARX, 'NEG31')
        c.L(ARX, FS.LO['T0'], reg=6)  # +10*d1
        c.Z(EPLUSX, 'EMASK'); c.Z(EPLUSX, 'C105'); c.Z(ATX, 'NUM')
        # d3*10+d4 -> float 34
        c.Z(0o10, 'CARD'); c.Z(ASX, 'SR8'); c.Z(AAX, 'M8'); c.Z(ARX, 'NEG31')
        c.L(ATI, 6)
        c.Z(0o10, 'CARD'); c.Z(AAX, 'M8'); c.Z(ARX, 'NEG31')
        c.L(ARX, FS.LO['T0'], reg=6)
        c.Z(EPLUSX, 'EMASK'); c.Z(EPLUSX, 'C105'); c.Z(ATX, 'CARD')
        c.Z(0o10, 'NUM'); c.C(MUL, K_HUNDRED)   # x100 via N+2 constant
        c.Z(FADD, 'CARD'); c.Z(ATX, 'NUM')
        c.Z(DIV, 'TEN'); c.Z(ATX, 'EST')
        mark(tag+'_PROC_END2')

    def emit_do():
        """C6: third 777005 record, TK=6 TEST FIXTURE (not native FRONT).

        Layout (verified by C-oracle CORE): W+1 byte4 = TK=6; W+2 byte0 = TO,
        bytes 2,3 = two-digit TA (bound), byte5 = one-digit TB (step).
        Counter/bound/step/accumulator are N+2 cells; the body is executed
        once per iteration and the sum is fed to the verbatim GOST path.
        """
        rearm()                      # converter clobbers base registers
        # advance persistent card pointer from record 2 to record 3
        c.C(0o10, K_PTR); c.C(ARX, K_FOUR); c.C(ATX, K_PTR)
        emit_scan('S3')              # find the third 777005 marker
        rearm()
        # ---- TK from W+1 byte4; verify TK == 6 ----
        c.L(0o10, 0o4013, 10)
        c.Z(ASX, 'SR8'); c.Z(AAX, 'M8'); c.Z(ARX, 'PD0'); c.Z(AAX, 'M8')
        c.C(AEX, K_DO_KIND)          # TK ^ 6 -> 0 iff DO fixture
        labels['DO_TK_UZA'] = len(H)
        c.L(UZA, 0, reg=7)           # patched: match -> DO_DECODE
        # wrong kind: EST = 0 -> prints 0000.00 (machine-visible mismatch)
        c.C(0o10, K_ZERO); c.Z(ATX, 'EST')
        labels['DO_TK_UJ'] = len(H)
        c.L(UJ, 0, reg=7)            # patched: -> DO_PRINT
        mark('DO_DECODE')
        # ---- bound = two-digit TA at W+2 bytes 2,3 (PD0 works for 0) ----
        c.L(0o10, 0o4014, 10)
        c.C(ASX, K_SR24); c.Z(AAX, 'M8'); c.Z(ARX, 'PD0'); c.Z(AAX, 'M8')
        c.L(ATI, 6)                  # M[6] = tens
        c.L(0o10, 0o4014, 10)
        c.Z(ASX, 'SR16'); c.Z(AAX, 'M8'); c.Z(ARX, 'PD0'); c.Z(AAX, 'M8')
        c.L(ARX, FS.LO['T0'], reg=6) # ACC = 10*tens + units = bound
        c.C(ATX, L_BOUND)
        # ---- step = one-digit TB at W+2 byte5 ----
        c.L(0o10, 0o4014, 10)
        c.Z(AAX, 'M8'); c.Z(ARX, 'PD0'); c.Z(AAX, 'M8')
        c.C(ATX, L_STEP)
        # ---- init: CNT = bound, SUM = 0 ----
        c.C(0o10, L_BOUND); c.C(ATX, L_CNT)
        c.C(0o10, K_ZERO); c.C(ATX, L_SUM)
        mark('DO_LOOP')
        # ---- body: SUM += VAL (BESM FPU) ----
        c.C(0o10, L_SUM); c.C(FADD, L_VAL); c.C(ATX, L_SUM)
        # ---- counter: CNT -= 1 ; exit when zero ----
        c.C(0o10, L_CNT); c.C(ARX, K_DECR); c.C(ATX, L_CNT)
        labels['DO_UZA'] = len(H)
        c.L(UZA, 0, reg=7)           # patched: CNT == 0 -> DO_DONE
        labels['DO_UJ'] = len(H)
        c.L(UJ, 0, reg=7)            # patched: -> DO_LOOP
        mark('DO_DONE')
        c.C(0o10, L_SUM); c.Z(ATX, 'EST')
        mark('DO_PRINT')
        c.C(0o10, K_GOSTA); c.L(ATX, 0o2006)
        c.C(0o10, K_GOSTB); c.L(ATX, 0o2007)
        c.vjmo(conv_ram)

    emit_scan('S1')
    emit_process('S1')
    c.C(0o10, K_GOSTA); c.L(ATX, 0o2006)
    c.C(0o10, K_GOSTB); c.L(ATX, 0o2007)
    c.vjmo(conv_ram)              # print record 1
    # advance persistent pointer +4 words
    c.C(0o10, K_PTR); c.C(ARX, K_FOUR); c.C(ATX, K_PTR)
    emit_scan('S2')
    emit_process('S2')
    c.C(0o10, K_GOSTA); c.L(ATX, 0o2006)
    c.C(0o10, K_GOSTB); c.L(ATX, 0o2007)
    c.vjmo(conv_ram)              # print record 2
    emit_do()                     # C6: scan + execute the TK=6 DO fixture
    c.E(UJ15)

    # absolute RAM of labels
    def lab(name):
        idx = labels[name]
        assert idx % 2 == 0, (name, idx)
        return N2_CODE_RAM + idx // 2

    # patch branches
    for tag in ('S1','S2','S3'):
        H[labels[tag+'_UZA']] = short(UZA, 0, reg=7) | ((lab(tag+'_FOUND') - 0o20000) & 0o7777)
        H[labels[tag+'_UJ']]  = short(UJ, 0, reg=7) | ((lab(tag+'_LOOP') - 0o20000) & 0o7777)
    for tag in ('S1', 'S2'):
        H[labels[tag+'_TK_UZA']] = short(UZA, 0, reg=7) | ((lab(tag+'_LIT') - 0o20000) & 0o7777)
        H[labels[tag+'_NAME_UZA']] = short(UZA, 0, reg=7) | ((lab(tag+'_NAME_OK') - 0o20000) & 0o7777)
        H[labels[tag+'_NAME_UJ']] = short(UJ, 0, reg=7) | ((lab(tag+'_PROC_END') - 0o20000) & 0o7777)
        H[labels[tag+'_END_UJ']] = short(UJ, 0, reg=7) | ((lab(tag+'_PROC_END2') - 0o20000) & 0o7777)
    # C6 DO-handler branches
    H[labels['DO_TK_UZA']] = short(UZA, 0, reg=7) | ((lab('DO_DECODE') - 0o20000) & 0o7777)
    H[labels['DO_TK_UJ']]  = short(UJ, 0, reg=7) | ((lab('DO_PRINT') - 0o20000) & 0o7777)
    H[labels['DO_UZA']]    = short(UZA, 0, reg=7) | ((lab('DO_DONE') - 0o20000) & 0o7777)
    H[labels['DO_UJ']]     = short(UJ, 0, reg=7) | ((lab('DO_LOOP') - 0o20000) & 0o7777)
    if len(H) % 2:
        H.append(DUMMY)
    import os
    if os.environ.get('C6_LABELS'):
        for nm in ('DO_TK_UZA','DO_DECODE','DO_LOOP','DO_DONE','DO_PRINT'):
            print('LABEL', nm, oct(lab(nm)))
    return c

# ---------------- image assembly ----------------
def asm_words(hw):
    z = [0] * 1024
    for i in range(len(hw)//2):
        z[i] = word(hw[2*i], hw[2*i+1])
    if len(hw) % 2:
        z[len(hw)//2] = word(hw[-1], DUMMY)
    return z

def vals():
    v = FS.vals()
    v['HALF'] = 0o20000           # N+2 base register source
    return v

def build(case, patch=None, namepatch=None, valpatch=None, decrpatch=None):
    src = WS / 'images/2048_base'
    dst = WS / 'images' / f'2048_{case}'
    shutil.copy2(src, dst)
    body = rz(str(dst), N + 1)
    body[0o11] = word(long_(0o300, N2_CODE_RAM, reg=0), 0)
    body[0o27] = int.from_bytes(bytes([2,1,15,15,0,0]), 'big')
    body[0o30] = int.from_bytes(bytes([0,0,14,0,0,15]), 'big')
    body[0o31] = int.from_bytes(bytes([15,3,0,0,0,14]), 'big')
    body[0o32] = int.from_bytes(bytes([0,0,0o231,15,15,15]), 'big')
    for n, value in vals().items():
        body[0o110 + FS.CELLS.index(n)] = value & MASK
    wz(str(dst), N + 1, body)

    n3_hw, floor_ram, conv_len, floor_len = build_n3()
    wz(str(dst), Z3, asm_words(n3_hw))

    n2 = build_n2(floor_ram, CONV_RAM0)
    z2 = rz(str(dst), N2)   # PRESERVE load-bearing overlay table at offsets 526..900
    # symbol table: name at VIDX, value at 32+VIDX
    symbols = {1: ('X       ', f32(7890.0)),
               2: ('Y       ', f32(1234.0)),
               12: ('H       ', f32(5678.0)),
               13: ('I       ', f32(9012.0))}
    if patch:
        symbols.update(patch)
    for vidx, (nm, val) in symbols.items():
        z2[vidx] = C2.text_word(nm) & MASK
        z2[32 + vidx] = val & MASK
    if namepatch:
        for vidx, nm in namepatch.items():
            z2[vidx] = C2.text_word(nm) & MASK
    # constants
    consts = {
        K_BASE: 0o20000, K_CBASE: 0o60000, K_ONE: 1, K_FOUR: 4,
        K_MARK: 0x823737373030, K_SR24: (64+24)<<41,
        K_28: 28, K_SP7: spaces7(), K_SHL42: shl42_const(),
        K_NEGONE: MASK ^ 1,   # one's-complement -1 (BESM-6 is 1's complement)
        K_HUNDRED: f32(100.0),
        K_PTR: 0o60000,
        K_GOSTA: body[0o27], K_GOSTB: body[0o30],
        # C6 DO-loop constants (mechanism values, no result digits)
        K_ZERO: 0, K_DECR: (MASK ^ decrpatch) if decrpatch else (MASK ^ 1),
        K_DO_KIND: 6,
        L_BOUND: 0, L_STEP: 0, L_CNT: 0, L_SUM: 0,
        # docs/105 prints <= 2 integer digits: EST = SUM must stay < 1000.
        # 200.0 * bound(2|3) = 400|600 -> printed 40.00 | 60.00
        L_VAL: f32(valpatch if valpatch is not None else 200.0),
    }
    for k, v in consts.items():
        z2[k] = v & MASK
    # code at N+2 offset 100
    n2hw = n2.hw
    for i in range(len(n2hw)//2):
        z2[N2_CODE_OFF + i] = word(n2hw[2*i], n2hw[2*i+1])
    if len(n2hw) % 2:
        z2[N2_CODE_OFF + len(n2hw)//2] = word(n2hw[-1], DUMMY)
    wz(str(dst), N2, z2)
    sha = hashlib.sha256(dst.read_bytes()).hexdigest()
    n2used = max(max(symbols)+1, 32+max(symbols)+1, max(consts)+1,
                 N2_CODE_OFF + (len(n2hw)+1)//2) + 1
    print(f'case={case} sha={sha} N3={len(n3_hw)//2}/{MAX_WORDS}w hw={len(n3_hw)} '
          f'conv={conv_len}hw floor={floor_len}hw floor_ram={oct(floor_ram)} '
          f'N2code={len(n2hw)}hw N2used~{n2used}/649')
    return dst, sha

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--build')
    ap.add_argument('--patchvalue', type=int, default=None)
    ap.add_argument('--valpatch', type=float, default=None,
                    help='one-machine-word patch of the N+2 loop addend')
    ap.add_argument('--decrpatch', type=int, default=None,
                    help='one-machine-word patch of the loop counter decrement')
    a = ap.parse_args()
    if a.build:
        patch = None
        if a.patchvalue is not None:
            patch = {12: ('H       ', f32(a.patchvalue))}
        build(a.build, patch=patch, valpatch=a.valpatch, decrpatch=a.decrpatch)
