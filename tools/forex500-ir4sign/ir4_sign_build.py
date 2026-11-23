#!/usr/bin/env python3
"""Zone-2350 contour: FULL 4-digit IR LIT reader PLUS on-machine GOST SIGN.

Combines, verbatim:
  * ir4_build.Stream.ir_read4() + intrinsic()  (docs/104 + ir-parser report):
    FRONT-emitted `777005` arg1 4-digit decode on BESM-6, fed to ABS+2+2 GOST
    chain printing 2+2 with NO /10 scaling;
  * final_sign.sign_block() (docs/100 + sign-opt report): avx/aax/asx/aex/atx
    sign mechanism, constants in T[8]/T[9] free low-RAM cells.

Reclaims: floor_acc (dead xta SCR in floor_int) + drop_last_ati (dead ati 5
in last digit). Sign constants live in T[8]/T[9], never indexed by our decks
(only tens digits 1..4 are exercised). No host-computed digit or minus byte.
"""
import argparse
import hashlib
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ir4_build as I
from build_e2e import rz, wz, word, short, f32, MASK, N, Z3, MAX_WORDS

WS = HERE.parent

# AVX opcode (not in ir4_build's alias list); reuse all others from I.
AVX = 0o14
CELLS = I.CELLS
LO = dict(I.LO)
LO["SIGNBIT"] = LO["T8"]
LO["SHR22"] = LO["T9"]


def vals():
    v = I.vals()
    v["T8"] = 1 << 40                 # SIGNBIT (float sign, bit 40)
    v["T9"] = (64 + 22) << 41         # SHR22 (asx right-shift 22)
    return v


class S(I.Stream):
    def Z(self, op, name):
        self.E(short(op, LO[name], reg=0))

    def sign_block(self):
        # ACC holds V (positive float) on entry after `atx V` in converter.
        self.Z(AVX, "SIGNBIT")        # ACC = -V (bit40 set)
        self.Z(I.AAX, "SIGNBIT")      # ACC = 1<<40 (or 0)
        self.Z(I.ASX, "SHR22")        # ACC = 1<<18 (or 0)
        self.L(I.AEX, 0o2006)         # GOST_A ^= 1<<18 -> byte3 15^4=11
        self.L(I.ATX, 0o2006)         # store GOST_A

    def converter(self, use_sub, floor_acc=False, drop_last_ati=False, sign=False):
        self.Z(0o10, "EST"); self.Z(I.DIV, "TEN"); self.Z(I.ATX, "V")
        if sign:
            self.sign_block()
        fl = self.floor_acc if floor_acc else self.floor
        self.Z(0o10, "V"); self.Z(I.DIV, "TEN"); self.Z(I.ATX, "SCR")
        self.VJM(self.sub_ram) if use_sub else fl()
        self.digit(0o30, "I1f")
        self.Z(0o10, "I1f"); self.Z(I.MUL, "TEN"); self.Z(I.XSUB, "V")
        self.Z(I.ATX, "SCR")
        self.VJM(self.sub_ram) if use_sub else fl()
        self.digit(0o40, "I0f")
        self.Z(0o10, "V"); self.Z(I.MUL, "TEN"); self.Z(I.ATX, "SCR")
        self.Z(0o10, "I1f"); self.Z(I.MUL, "TEN"); self.Z(I.FADD, "I0f")
        self.Z(I.MUL, "TEN"); self.Z(I.XSUB, "SCR"); self.Z(I.FADD, "EPS")
        self.Z(I.ATX, "SCR")
        self.VJM(self.sub_ram) if use_sub else fl()
        self.digit(0o60, "F1f")
        self.Z(0o10, "V"); self.Z(I.MUL, "TEN"); self.Z(I.MUL, "TEN")
        self.Z(I.ATX, "SCR")
        self.Z(0o10, "I1f"); self.Z(I.MUL, "TEN"); self.Z(I.FADD, "I0f")
        self.Z(I.MUL, "TEN"); self.Z(I.FADD, "F1f"); self.Z(I.MUL, "TEN")
        self.Z(I.XSUB, "SCR"); self.Z(I.FADD, "EPS"); self.Z(I.ATX, "SCR")
        self.VJM(self.sub_ram) if use_sub else fl()
        self.digit(0o70, no_ati=drop_last_ati)

    def assemble(self, floor_acc=False, drop_last_ati=False, sign=False):
        self.sub_ram = 0
        self.ir_read4(); self.intrinsic()
        self.converter(True, floor_acc, drop_last_ati, sign)
        self.L(I.E64, 0o2004)
        if len(self.hw) % 2:
            self.E(I.DUMMY)
        self.E(I.UJ15)
        main_len = len(self.hw)
        sub_idx = (main_len + 1) // 2 * 2
        self.sub_ram = 0o30114 + sub_idx // 2
        while len(self.hw) < sub_idx:
            self.E(I.DUMMY)
        for i, x in enumerate(self.hw):
            if (x >> 20) == I.LINK and ((x >> 12) & 0o370) == 0o310:
                self.hw[i] = self.vjm(self.sub_ram)
        if floor_acc:
            self.floor_acc()
        else:
            self.floor()
        self.E(I.RET_LINK)
        return self.hw


def measure(floor_acc=False, drop_last_ati=False, sign=False):
    s = S(); hw = s.assemble(floor_acc, drop_last_ati, sign)
    return (len(hw) + 1) // 2, len(hw), s.sub_ram


def build(case, floor_acc=False, drop_last_ati=False, sign=False, patch=None,
          src=None):
    src = Path(src) if src else WS / "images/2048_base"
    dst = WS / "images" / f"2048_{case}"
    shutil.copy2(src, dst)
    body = rz(str(dst), N + 1)
    body[0o11] = word(I.long_(0o300, 0o30114, reg=0), I.DUMMY)
    body[0o27] = int.from_bytes(bytes([2, 1, 15, 15, 0, 0]), "big")
    body[0o30] = int.from_bytes(bytes([0, 0, 14, 0, 0, 15]), "big")
    body[0o31] = int.from_bytes(bytes([15, 3, 0, 0, 0, 14]), "big")
    body[0o32] = int.from_bytes(bytes([0, 0, 0o231, 15, 15, 15]), "big")
    v = vals()
    if patch:
        v.update(patch)
    for n, value in v.items():
        body[I.BODY0 + CELLS.index(n)] = value & MASK
    s = S(); hw = s.assemble(floor_acc, drop_last_ati, sign)
    z3 = [0] * 1024
    for i in range(len(hw) // 2):
        z3[i] = word(hw[2 * i], hw[2 * i + 1])
    if len(hw) % 2:
        z3[len(hw) // 2] = word(hw[-1], I.DUMMY)
    wz(str(dst), N + 1, body)
    wz(str(dst), Z3, z3)
    sha = hashlib.sha256(dst.read_bytes()).hexdigest()
    print(f"case={case} sha={sha} words={(len(hw)+1)//2}/{MAX_WORDS} "
          f"hw={len(hw)} sign={sign} floor_acc={floor_acc} "
          f"drop_ati={drop_last_ati} subram={oct(s.sub_ram)}")
    return dst, sha


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--measure", action="store_true")
    ap.add_argument("--build")
    ap.add_argument("--sign", action="store_true")
    ap.add_argument("--floor-acc", action="store_true")
    ap.add_argument("--drop-last-ati", action="store_true")
    ap.add_argument("--patch-signbit", action="store_true",
                    help="set T8 SIGNBIT to 0 (one machine-word patch gate)")
    a = ap.parse_args()
    if a.measure or not a.build:
        for sg in (False, True):
            for fa in (False, True):
                for da in (False, True):
                    c, h, sr = measure(fa, da, sg)
                    print(f"sign={sg!s:5s} floor_acc={fa!s:5s} "
                          f"drop_ati={da!s:5s} words={c}/{MAX_WORDS} "
                          f"hw={h} subram={oct(sr)} "
                          f"{'OK' if c <= MAX_WORDS else 'OVER %d' % (c-MAX_WORDS)}")
    if a.build:
        patch = {"T8": 0} if a.patch_signbit else None
        build(a.build, a.floor_acc, a.drop_last_ati, a.sign, patch)
