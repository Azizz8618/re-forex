#!/usr/bin/env python3
"""Minimal BESM-6 half-word assembler for the D1 prototype.

Encodes the opcodes used by the N3 CODEGEN output (authoritative table:
re-siprod/tools/siprod_asm.py).  Each 48-bit word holds two 24-bit halves.
"""
import sys
sys.path.insert(0, "/home/azizz/Yandex.Disk/re-siprod/tools")
import siprod_asm as sa

# 24-bit half-word builders (reg=0, second structure unless noted)
def half(name, arg, reg=0, dms=0):
    d = dict(name=name, kind=sa.OPCODE_BY_NAME[name.upper()][2],
             reg=reg, arg=arg, dms=dms, exp=0, struct=0, op=0, raw=0)
    # derive op from name code via lookup
    code, mask, kind = sa.OPCODE_BY_NAME[name.upper()]
    d["kind"] = kind
    # first-structure opcodes have STRUCT_BIT set in code
    if code & sa.STRUCT_BIT:
        d["struct"] = 1
        d["op"] = (code >> 15) & 0xF
    else:
        d["struct"] = 0
        d["op"] = (code >> 12) & 0o77
    return sa.encode(d)

def word(h1, h2):
    return (h1 << 24) | h2

# Convenience aliases
def s(a):    return half("сч", a)       # read acc <- [a]
def z(a):    return half("зп", a)       # write [a] <- acc
def plus(a): return half("сл", a)       # acc += [a]
def minus(a):return half("вч", a)       # acc -= [a]
def pe(a):   return half("пе", a)       # first-structure branch (arg 15 bit)
def e64(a):  return half("Э64", a)      # extracode 64, descriptor at a
def mod0():  return 0x090000            # "мода 0" padding half
def ret():   return word(half("пб", 0, reg=13), mod0())  # vjm 0(15)

if __name__ == "__main__":
    # sanity: reproduce a3 code words
    w0 = word(e64(0o1772), mod0())
    print("e64 word:", f"{w0:016o}", "expect 0064177202200000")
    w1 = ret()
    print("ret word:", f"{w1:016o}", "expect 6700000002200000")
    # reproduce N3 loop words
    print("loop w:", f"{word(s(0o100), z(0o101)):016o}")
