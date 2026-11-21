#!/usr/bin/env python3
"""Faithful LINEAR BESM-6 disassembler using dtran.cc opcode table.
Decodes every word (two 24-bit halves), ignores reachability.
"""
import re, sys
from pathlib import Path

# (name, pattern, mask, type) copied verbatim from /home/azizz/Yandex.Disk/dtran/dtran.cc
OP = [
 ("ATX",0x000000,0x0bf000,"STR1"),("STX",0x001000,0x0bf000,"STR1"),
 ("XTS",0x003000,0x0bf000,"STR1"),("A+X",0x004000,0x0bf000,"STR1"),
 ("A-X",0x005000,0x0bf000,"STR1"),("X-A",0x006000,0x0bf000,"STR1"),
 ("AMX",0x007000,0x0bf000,"STR1"),("XTA",0x008000,0x0bf000,"STR1"),
 ("AAX",0x009000,0x0bf000,"STR1"),("AEX",0x00a000,0x0bf000,"STR1"),
 ("ARX",0x00b000,0x0bf000,"STR1"),("AVX",0x00c000,0x0bf000,"STR1"),
 ("AOX",0x00d000,0x0bf000,"STR1"),("A/X",0x00e000,0x0bf000,"STR1"),
 ("A*X",0x00f000,0x0bf000,"STR1"),("APX",0x010000,0x0bf000,"STR1"),
 ("AUX",0x011000,0x0bf000,"STR1"),("ACX",0x012000,0x0bf000,"STR1"),
 ("ANX",0x013000,0x0bf000,"STR1"),("E+X",0x014000,0x0bf000,"STR1"),
 ("E-X",0x015000,0x0bf000,"STR1"),("ASX",0x016000,0x0bf000,"STR1"),
 ("XTR",0x017000,0x0bf000,"STR1"),("RTE",0x018000,0x0bf000,"IMM"),
 ("YTA",0x019000,0x0bf000,"IMM64"),("E+N",0x01c000,0x0bf000,"IMM64"),
 ("E-N",0x01d000,0x0bf000,"IMM64"),("ASN",0x01e000,0x0bf000,"IMM64"),
 ("NTR",0x01f000,0x0bf000,"IMM"),("ATI",0x020000,0x0bf000,"REG1"),
 ("STI",0x021000,0x0bf000,"REG1"),("ITA",0x022000,0x0bf000,"REG1"),
 ("ITS",0x023000,0x0bf000,"REG1"),("MTJ",0x024000,0x0bf000,"REG1"),
 ("J+M",0x025000,0x0bf000,"REG1"),
 ("*50",0x028000,0x0bf000,"IMMEX"),("*51",0x029000,0x0bf000,"IMMEX"),
 ("*52",0x02a000,0x0bf000,"IMMEX"),("*53",0x02b000,0x0bf000,"IMMEX"),
 ("*54",0x02c000,0x0bf000,"IMMEX"),("*55",0x02d000,0x0bf000,"IMMEX"),
 ("*56",0x02e000,0x0bf000,"IMMEX"),("*57",0x02f000,0x0bf000,"IMMEX"),
 ("*60",0x030000,0x0bf000,"ADDREX"),("*61",0x031000,0x0bf000,"ADDREX"),
 ("*62",0x032000,0x0bf000,"IMMEX"),("*63",0x033000,0x0bf000,"IMMEX"),
 ("*64",0x034000,0x0bf000,"ADDREX"),("*65",0x035000,0x0bf000,"IMMEX"),
 ("*66",0x036000,0x0bf000,"IMMEX"),("*67",0x037000,0x0bf000,"ADDREX"),
 ("*70",0x038000,0x0bf000,"ADDREX"),("*71",0x039000,0x0bf000,"ADDREX"),
 ("*72",0x03a000,0x0bf000,"ADDREX"),("*73",0x03b000,0x0bf000,"ADDREX"),
 ("*74",0x03c000,0x0bf000,"STOP"),("CTX",0x03d000,0x0bf000,"ADDREX"),
 ("*76",0x03e000,0x0bf000,"IMMEX"),("*77",0x03f000,0x0bf000,"IMMEX"),
 ("UTC",0x090000,0x0f8000,"ADDRMOD"),("WTC",0x098000,0x0f8000,"ADDRMOD"),
 ("VTM",0x0a0000,0x0f8000,"REG2"),("UTM",0x0a8000,0x0f8000,"REG2"),
 ("UZA",0x0b0000,0x0f8000,"BRANCH"),("U1A",0x0b8000,0x0f8000,"BRANCH"),
 ("UJ", 0x0c0000,0x0f8000,"JUMP"),("VJM",0x0c8000,0x0f8000,"CALL"),
 ("VZM",0x0e0000,0x0f8000,"BRANCH"),("V1M",0x0e8000,0x0f8000,"BRANCH"),
 ("VLM",0x0f8000,0x0f8000,"BRANCH"),
]

def dec24(op):
    for name,pat,mask,typ in OP:
        if (op & mask)==pat: return name,typ
    return f"?{op:06o}","ILLEGAL"

def half(op):
    reg = op >> 20
    arg1 = (op & 0o7777) + (0o70000 if (op & 0o040000) else 0)
    arg2 = op & 0o77777
    struc = bool(op & 0o2000000)
    name,typ = dec24(op)
    if typ=="ILLEGAL" and struc:
        name = f"E{((op>>15)&0o37):02o}"  # extractcode-ish
    # operand
    if struc:
        opd = f"'{arg2:05o}'"
    elif arg1>=0o74000:
        opd = f"C/{arg1&0o3777:04o}"
    elif arg1:
        if typ=="IMM64":
            opd = f"{arg1-64:+d}"
        elif typ in ("REG1",) or arg1<8:
            opd = f"{arg1}"
        else:
            opd = f"{arg1:o}B"
    else:
        opd = ""
    prefix = f"M{reg}," if reg else ""
    return f"{name} {prefix}{opd}".strip()

def word(w):
    return half(w>>24), half(w&0xffffff)

if __name__=='__main__':
    d=Path(sys.argv[1]).read_bytes()
    A=int(sys.argv[2],0)
    W=[int.from_bytes(d[i:i+6],'big') for i in range(0,len(d),6)]
    for j,w in enumerate(W):
        hi,lo=word(w)
        print(f"{A+j:06o} {w:016o}  {hi:<28} | {lo}")
