#!/usr/bin/env python3
"""Optimized 58/58 chain PLUS on-machine GOST sign, with fold experiments.

Reuses final_build.Stream verbatim; the sign block is inserted after `atx V`
where ACC still holds V (the positive float), so no reload is needed.
"""
import sys, hashlib, shutil
from pathlib import Path
sys.path.insert(0, "/tmp/.private/azizz/opencode/sign-opt/scripts")
import final_build as F
from build_e2e import rz, wz, short, word, f32, MASK, N, Z3, checksum

# opcode aliases not present in final_build
AVX = 0o14
E64 = F.E64

# Sign mechanism cells reuse T[8]/T[9]: within the proven-free body[0o110..0o135]
# range and never indexed by our decks (only tens digits 1..4 are exercised).
CELLS = F.CELLS
LO = dict(F.LO)
LO["SIGNBIT"] = LO["T8"]
LO["SHR22"] = LO["T9"]

def vals():
    v = F.vals()
    v["T8"] = 1 << 40                 # SIGNBIT (float sign, bit 40)
    v["T9"] = (64 + 22) << 41         # SHR22 (asx right-shift 22)
    return v

class S(F.Stream):
    def Z(self, op, name):
        self.E(short(op, LO[name], reg=0))

    def L(self, op, adr, reg=0):
        self.E(short(op, adr, reg=reg))

    def sign_block(self, mode="plain"):
        """ACC holds V (positive float) on entry. Emit machine sign test.
        ACC = -V ; sign bit ; shift to byte3 ; XOR into GOST_A ; store.
        """
        if mode == "plain":
            self.Z(AVX, "SIGNBIT")     # ACC = -V (bit40 set)
            self.Z(F.AAX, "SIGNBIT")   # ACC = 1<<40 (or 0)
            self.Z(F.ASX, "SHR22")     # ACC = 1<<18 (or 0)
            self.L(F.AEX, 0o2006)      # GOST_A ^= 1<<18 -> byte3 15^4=11
            self.L(F.ATX, 0o2006)      # store GOST_A
        elif mode == "noatx":
            # fold attempt: let a later deposit carry the store (not used yet)
            self.Z(AVX, "SIGNBIT")
            self.Z(F.AAX, "SIGNBIT")
            self.Z(F.ASX, "SHR22")
            self.L(F.AEX, 0o2006)
        else:
            raise ValueError(mode)

    def floor_acc(self):
        """floor_int using ACC as input (all call sites leave SCR value in ACC).
        The baseline `xta SCR` reload is dead: `atx SCR` preserves ACC.
        """
        self.Z(F.AEX, "EMASK")
        self.Z(F.EPLUSX, "C105")
        self.Z(F.ATX, "CW")
        self.Z(F.AAX, "M40")
        self.Z(F.ASX, "CW")

    def converter(self, use_sub, sign=None, drop_last_ati=False, floor_acc=False):
        self.Z(0o10, "EST"); self.Z(F.DIV, "TEN"); self.Z(F.ATX, "V")
        if sign:
            self.sign_block(sign)
        fl = self.floor_acc if floor_acc else self.floor
        self.Z(0o10, "V"); self.Z(F.DIV, "TEN"); self.Z(F.ATX, "SCR")
        self.VJM(self.sub_ram) if use_sub else fl()
        self.digit(0o30, "I1f")
        self.Z(0o10, "I1f"); self.Z(F.MUL, "TEN"); self.Z(F.XSUB, "V")
        self.Z(F.ATX, "SCR")
        self.VJM(self.sub_ram) if use_sub else fl()
        self.digit(0o40, "I0f")
        self.Z(0o10, "V"); self.Z(F.MUL, "TEN"); self.Z(F.ATX, "SCR")
        self.Z(0o10, "I1f"); self.Z(F.MUL, "TEN"); self.Z(F.FADD, "I0f")
        self.Z(F.MUL, "TEN"); self.Z(F.XSUB, "SCR"); self.Z(F.FADD, "EPS")
        self.Z(F.ATX, "SCR")
        self.VJM(self.sub_ram) if use_sub else fl()
        self.digit(0o60, "F1f")
        self.Z(0o10, "V"); self.Z(F.MUL, "TEN"); self.Z(F.MUL, "TEN")
        self.Z(F.ATX, "SCR")
        self.Z(0o10, "I1f"); self.Z(F.MUL, "TEN"); self.Z(F.FADD, "I0f")
        self.Z(F.MUL, "TEN"); self.Z(F.FADD, "F1f"); self.Z(F.MUL, "TEN")
        self.Z(F.XSUB, "SCR"); self.Z(F.FADD, "EPS"); self.Z(F.ATX, "SCR")
        self.VJM(self.sub_ram) if use_sub else fl()
        if drop_last_ati:
            # last digit has no `out`; M[5] is never read, so ati 5 is dead
            self.L(F.ASN, 0o70); self.L(F.ARX, 0o2007); self.L(F.ATX, 0o2007)
        else:
            self.digit(0o70)

    def assemble(self, kind="SQRT", two=True, use_sub=True, sign=None,
                 drop_last_ati=False, floor_acc=False):
        if use_sub:
            self.sub_ram = 0
            self.deck_read(two); self.intrinsic(kind)
            self.converter(True, sign, drop_last_ati, floor_acc)
            self.L(E64, 0o2004)
            if len(self.hw) % 2:
                self.E(F.DUMMY)
            self.E(F.UJ15)
            main_len = len(self.hw)
            sub_idx = (main_len + 1) // 2 * 2
            self.sub_ram = 0o30114 + sub_idx // 2
            while len(self.hw) < sub_idx:
                self.E(F.DUMMY)
            for i, x in enumerate(self.hw):
                if (x >> 20) == F.LINK and ((x >> 12) & 0o370) == 0o310:
                    self.hw[i] = F.vjm(self.sub_ram)
            if floor_acc:
                self.floor_acc()
            else:
                self.floor()
            self.E(F.RET_LINK)
        else:
            raise NotImplementedError
        return self.hw

def measure(sign="plain", drop_last_ati=False, floor_acc=False):
    s = S(); hw = s.assemble("SQRT", True, True, sign, drop_last_ati, floor_acc)
    return (len(hw)+1)//2, len(hw), s.sub_ram, s

def build(case, sign="plain", drop_last_ati=False, floor_acc=False, patch=None,
          ws="/tmp/.private/azizz/opencode/sign-opt"):
    ws = Path(ws)
    src = ws / "images/2048_base"
    dst = ws / "images" / f"2048_{case}"
    shutil.copy2(src, dst)
    body = rz(str(dst), N + 1)
    body[0o11] = word(F.long_(0o300, 0o30114, reg=0), F.DUMMY)
    body[0o27] = int.from_bytes(bytes([2, 1, 15, 15, 0, 0]), "big")
    body[0o30] = int.from_bytes(bytes([0, 0, 14, 0, 0, 15]), "big")
    body[0o31] = int.from_bytes(bytes([15, 3, 0, 0, 0, 14]), "big")
    body[0o32] = int.from_bytes(bytes([0, 0, 0o231, 15, 15, 15]), "big")
    v = vals()
    if patch:
        v.update(patch)
    for n, value in v.items():
        body[0o110 + CELLS.index(n)] = value & MASK
    s = S(); hw = s.assemble("SQRT", True, True, sign, drop_last_ati, floor_acc)
    z3 = [0] * 1024
    for i in range(len(hw) // 2):
        z3[i] = word(hw[2*i], hw[2*i+1])
    if len(hw) % 2:
        z3[len(hw)//2] = word(hw[-1], F.DUMMY)
    wz(str(dst), N + 1, body)
    wz(str(dst), Z3, z3)
    sha = hashlib.sha256(dst.read_bytes()).hexdigest()
    print(f"case={case} sign={sign} drop_ati={drop_last_ati} "
          f"floor_acc={floor_acc} sha={sha} "
          f"code={(len(hw)+1)//2} hw={len(hw)} subram={oct(s.sub_ram)}")
    return dst, sha

if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--measure", action="store_true")
    ap.add_argument("--build")
    ap.add_argument("--sign", default="plain")
    ap.add_argument("--drop-last-ati", action="store_true")
    ap.add_argument("--floor-acc", action="store_true")
    a = ap.parse_args()
    if a.measure:
        for sg in ("plain",):
            for da in (False, True):
                for fa in (False, True):
                    c, h, sr, _ = measure(sg, da, fa)
                    print(f"sign={sg:6s} drop_ati={da!s:5s} floor_acc={fa!s:5s} "
                          f"code={c:3d} hw={h:3d} subram={oct(sr):>8} "
                          f"{'OK' if c<=58 else 'OVER %d'%(c-58)}")
    if a.build:
        build(a.build, a.sign, a.drop_last_ati, a.floor_acc)
