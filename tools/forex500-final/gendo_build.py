#!/usr/bin/env python3
"""Generalized DO in a SEPARATE N+1 body routine; base contour left byte-identical.

The proven builder b_final_do_build.py is imported unchanged.  Its image is
copied byte-for-byte, then exactly one N+2 word (the FOUND_DO entry) is replaced
by LONG UJ into our own routine in free body[0o604..0o700], with a docs/129
region-end guard.  No LEX/TK/TO slot or table is moved or extended.
"""
import argparse, hashlib, importlib.util, shutil, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = HERE.parent
sys.path.insert(0, str(HERE))

spec = importlib.util.spec_from_file_location('base', HERE / 'b_final_do_build.py')
G = importlib.util.module_from_spec(spec)
spec.loader.exec_module(G)

from build_e2e import rz, wz, N, long_, word, f32, MASK
N2 = N + 2

ATX, AAX, AEX, ARX, ASX, ADD, MUL = 0o00, 0o11, 0o12, 0o13, 0o26, 0o04, 0o17
UJ, UZA = 0o300, 0o260
N1 = N + 1

# docs/120 segment S4: body[0o604..0o1235] -> RAM 0o2621..0o3252
CODE_LO, CODE_HI = 0o604, 0o1000        # 124 words, guard at 0o1000
DATA_LO = 0o1001

def body_ram2(idx):
    return 0o2621 + (idx - 0o604)

# new data cells body[0o701..0o711]
(D_PHASE, D_FIELD, D_INTI, D_LIMI, D_STEPI, D_INIT, D_STEP,
 D_NLIMIT, D_CNT, D_ADDEND, D_GTMP, D_COUNT,
 C_CH_I, C_FONE, C_SIGN, C_ADDBIAS) = range(DATA_LO, DATA_LO + 16)
(R_PHASE, R_FIELD, R_INTI, R_LIMI, R_STEPI, R_INIT, R_STEP,
 R_NLIMIT, R_CNT, R_ADDEND, R_GTMP, R_COUNT,
 R_CH_I, R_FONE, R_SIGN, R_ADDBIAS) = (body_ram2(x) for x in range(DATA_LO, DATA_LO + 16))


def base_asm():
    a = G.build_lex()
    return a

def base_ram(a, label):
    hw = a.labels[label]
    off = a.slots[hw // 2]
    return G.ram_of(off) + (hw % 2)


class GAsm(G.LAsm):
    def __init__(self, extern, guard_target):
        super().__init__()
        self.extern = dict(extern)
        self.slots = list(range(CODE_LO, CODE_HI))
        self.guard_targets = {CODE_HI: guard_target}
        self.calls = []

    def ram_of_label(self, name):
        if name in self.extern:
            return self.extern[name]
        hw = self.labels[name]
        off = self.slots[hw // 2]
        return body_ram2(off) + (hw % 2)

    def resolve(self):
        for i, name, op in self.branches:
            if name in self.extern:
                self.hw[i] = long_(op, self.extern[name])
                continue
            hw = self.labels[name]
            off = self.slots[hw // 2]
            self.hw[i] = long_(op, body_ram2(off) + (hw % 2))
        for i, name in self.calls:
            self.hw[i] = G.vjm_imm(self.ram_of_label(name))
        if len(self.hw) % 2:
            self.E(G.DUMMY)
        assert (len(self.hw) + 1) // 2 <= len(self.slots), \
            f'body routine overrun: {(len(self.hw)+1)//2} > {len(self.slots)}'

    def code_words(self):
        ws = [(self.slots[i], word(self.hw[2*i], self.hw[2*i+1]))
              for i in range(len(self.hw) // 2)]
        for slot, target in self.guard_targets.items():
            ws.append((slot, word(long_(UJ, target), G.DUMMY)))
        return sorted(ws)


def float_from_int(a, src, dst, tag):
    # f32(n) by n FPU additions of f32(1.0); no E+-X exponent word needed.
    a.C(0o10, G.L_ZERO); a.C(ATX, G.C_F)
    a.d(0o10, src); a.d(ATX, R_COUNT)
    a.mark(tag + '_LOOP')
    a.C(0o10, G.C_F); a.L(ADD, R_FONE, reg=0); a.C(ATX, G.C_F)
    a.d(0o10, R_COUNT); a.C(ARX, G.L_NEG1); a.d(ATX, R_COUNT)
    a.d(0o10, R_COUNT); a.br(UZA, tag + '_DONE')       # +0
    a.d(0o10, R_COUNT); a.C(ASX, G.L_SHRTAB); a.C(AAX, G.L_ONE)
    a.C(AEX, G.L_ONE); a.br(UZA, tag + '_DONE')        # -0 / negative
    a.br(UJ, tag + '_LOOP')
    a.mark(tag + '_DONE')
    a.C(0o10, G.C_F); a.d(ATX, dst)


def finish_limit(a, tag):
    a.d(0o10, R_FIELD); a.d(ATX, R_LIMI)
    float_from_int(a, R_LIMI, G.RD_BOUND, tag)
    a.d(0o10, G.RD_BOUND); a.L(G.AVX, R_SIGN, reg=0); a.d(ATX, R_NLIMIT)


def build_routine(extern):
    a = GAsm(extern, guard_target=extern['MAIN_LOOP'])
    a.mark('START')
    # same token drop / state clear as the proven FOUND_DO
    a.C(0o10, G.L_THREE); a.C(ATX, G.C_TOKPTR)
    a.C(0o10, G.L_ZERO); a.d(ATX, R_PHASE); a.d(ATX, G.RD_DOHIT)
    a.d(ATX, R_FIELD)

    # ---- field scan: init (phase 0), limit (1), step (2) ----
    a.mark('SCAN')
    a.call('GETCH')
    a.mark('SCAN_DISPATCH')
    a.C(0o10, G.C_CH); a.C(AAX, G.L_0XF0); a.C(AEX, G.L_0X30)
    a.br(UZA, 'FIELD_DIG')
    a.C(0o10, G.C_CH); a.C(AEX, G.L_COMMA); a.br(UZA, 'FIELD_COMMA')
    a.C(0o10, G.C_CH); a.C(AEX, G.L_0X0A); a.br(UZA, 'FIELD_EOL')
    a.br(UJ, 'SCAN')
    a.mark('FIELD_DIG')
    a.C(0o10, G.C_CH); a.C(AAX, G.L_0X0F); a.d(ATX, R_FIELD)
    a.br(UJ, 'SCAN')

    a.mark('FIELD_COMMA')
    a.d(0o10, R_PHASE); a.br(UZA, 'COMMA_INIT')
    a.d(0o10, R_PHASE); a.C(AEX, G.L_ONE); a.br(UZA, 'COMMA_LIMIT')
    a.br(UJ, 'SCAN')
    a.mark('COMMA_INIT')
    a.d(0o10, R_FIELD); a.d(ATX, R_INTI)
    float_from_int(a, R_INTI, R_INIT, 'FINIT')
    a.C(0o10, G.L_ZERO); a.d(ATX, R_FIELD)
    a.C(0o10, G.L_ONE); a.d(ATX, R_PHASE)
    a.br(UJ, 'SCAN')
    a.mark('COMMA_LIMIT')
    finish_limit(a, 'FLIM')
    a.C(0o10, G.L_ZERO); a.d(ATX, R_FIELD)
    a.C(0o10, G.L_TWO); a.d(ATX, R_PHASE)
    a.br(UJ, 'SCAN')

    a.mark('FIELD_EOL')
    a.d(0o10, R_PHASE); a.br(UZA, 'EOL_LIMIT')
    a.d(0o10, R_PHASE); a.C(AEX, G.L_ONE); a.br(UZA, 'EOL_LIMIT')
    a.d(0o10, R_FIELD); a.d(ATX, R_STEPI)
    float_from_int(a, R_STEPI, R_STEP, 'FSTEP')
    a.br(UJ, 'BODY_ENTER')
    a.mark('EOL_LIMIT')
    finish_limit(a, 'FLIM2')
    a.d(0o10, R_FONE); a.d(ATX, R_STEP)
    a.br(UJ, 'BODY_ENTER')

    # ---- body: S=S+I or S=S+<literal> ----
    a.mark('BODY_ENTER')
    a.C(0o10, G.L_ONE); a.d(ATX, G.RD_DOHIT)
    a.mark('BODY_SCAN')
    a.call('GETCH')
    a.C(0o10, G.C_CH); a.C(AEX, G.L_PLUS); a.br(UZA, 'BODY_PLUS')
    a.br(UJ, 'BODY_SCAN')
    a.mark('BODY_PLUS')
    a.call('GETCH')
    a.C(0o10, G.C_CH); a.L(AEX, R_CH_I, reg=0); a.br(UZA, 'BODY_IS_I')
    a.C(0o10, G.C_CH); a.C(AAX, G.L_0XF0); a.C(AEX, G.L_0X30)
    a.br(UZA, 'BODY_IS_LIT')
    a.br(UJ, 'BODY_PLUS')
    a.mark('BODY_IS_LIT')
    # Re-dispatch the digit to the proven M_DONUM -> M_NUM -> DO_ITER path.
    a.d(0o10, R_LIMI); a.d(ATX, G.RD_BOUND)
    a.br(UJ, 'M_DONUM')
    a.mark('BODY_IS_I')

    # ---- generalized loop ----
    a.d(0o10, R_INIT); a.d(ATX, R_CNT)
    a.mark('ILOOP')
    a.d(0o10, R_CNT); a.C(MUL, G.L_TEN)
    a.L(ADD, R_ADDBIAS, reg=0); a.d(ATX, R_ADDEND)
    a.C(0o10, 33); a.L(ADD, R_ADDEND, reg=0); a.C(ATX, 33)
    a.d(0o10, R_CNT); a.L(ADD, R_STEP, reg=0); a.d(ATX, R_CNT)
    a.d(0o10, R_CNT); a.L(ADD, R_NLIMIT, reg=0); a.d(ATX, R_GTMP)
    a.d(0o10, R_GTMP); a.br(UZA, 'ILOOP')
    a.d(0o10, R_GTMP); a.C(ASX, G.L_SHRTAB); a.C(AAX, G.L_ONE)
    a.br(UZA, 'IDONE')
    a.br(UJ, 'ILOOP')
    a.mark('IDONE')
    a.C(0o10, G.L_ZERO); a.d(ATX, G.RD_DOHIT)
    a.C(0o10, G.L_ZERO); a.C(ATX, G.C_MODE)
    G.reset_windows(a)
    a.br(UJ, 'MAIN_LOOP')
    a.resolve()
    return a


def build(case, src=None):
    src = Path(src) if src else WS / 'images/2048_MODFINAL_B2'
    dst = WS / 'images' / f'2048_{case}'
    shutil.copy2(src, dst)

    ba = base_asm()
    extern = {'GETCH': base_ram(ba, 'GETCH'),
              'MAIN_LOOP': base_ram(ba, 'MAIN_LOOP'),
              'M_DONUM': base_ram(ba, 'M_DONUM')}
    a = build_routine(extern)
    entry = a.ram_of_label('START')

    # N+1: isolated routine in free body words
    body = rz(str(dst), N1)
    for idx, w in a.code_words():
        body[idx] = w & MASK
    for idx in (D_PHASE, D_FIELD, D_INTI, D_LIMI, D_STEPI, D_INIT, D_STEP,
                D_NLIMIT, D_CNT, D_ADDEND, D_GTMP, D_COUNT):
        body[idx] = 0
    body[C_CH_I] = 0x49
    body[C_FONE] = f32(1.0)
    body[C_SIGN] = 1 << 40
    body[C_ADDBIAS] = 0                     # PATCH target: f32(0) -> f32(10.0)
    wz(str(dst), N1, body)

    # N+2: exactly ONE word, the proven FOUND_DO entry, becomes a trampoline.
    z2 = rz(str(dst), N2)
    fo_slot = ba.slots[ba.labels['FOUND_DO'] // 2]
    old = z2[fo_slot]
    z2[fo_slot] = word(long_(UJ, entry), G.DUMMY)
    wz(str(dst), N2, z2)

    sha = hashlib.sha256(dst.read_bytes()).hexdigest()
    print(f'case={case} sha={sha} entry={entry:o} routine_words={len(a.hw)//2} '
          f'fo_slot={fo_slot} old={old:016o} new={z2[fo_slot]:016o}')
    return dst, sha


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--build', required=True)
    ap.add_argument('--src')
    x = ap.parse_args()
    build(x.build, x.src)
