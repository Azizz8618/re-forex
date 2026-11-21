#!/usr/bin/env python3
"""GOST-10859 encoder (authoritative GT table from repo src/newcomp/EMIT.FTN)."""
GT = [15,0,0,0,0,0,0,0, 18,19,25,10,13,11,14,12,
      0,1,2,3,4,5,6,7, 8,9,0,0,0,0,0,0,
      0,32,34,49,63,37,64,65, 45,66,67,42,68,44,69,46,
      48,70,71,72,50,73,74,75, 53,51,76,0,0,0,0,0]
EOF = 0o231

def gost_bytes(s):
    out = []
    for ch in s:
        ic = ord(ch) - 31
        out.append(GT[ic-1] if 1 <= ic <= 64 else 0)
    return out

def pack6(bs):
    bs = (bs + [15]*6)[:6]
    return ((bs[0]<<16)|(bs[1]<<8)|bs[2]) << 24 | ((bs[3]<<16)|(bs[4]<<8)|bs[5])

def encode(s, nwords=None, eof=True):
    gb = gost_bytes(s)
    if eof:
        gb = gb + [EOF]
    ws = [pack6(gb[i:i+6]) for i in range(0, len(gb), 6)]
    if nwords and len(ws) < nwords:
        ws += [pack6([15]*6)] * (nwords - len(ws))
    return ws, gb

if __name__ == "__main__":
    # verify against A5 known words: 21 1.00 3.00
    ws, gb = encode("21 1.00 3.00")
    print("A5 '21 1.00 3.00' bytes:", gb)
    for i,w in enumerate(ws): print(f"  w{i}: {w:016o}")
    print("expected:", "0040041700207000", "0000740303400000", "4620741703607417")
    # decode A3 last GOST word for EOF position
    b=open('/var/tmp/b1-f77-fix/59-a3/a3_code.bin','rb').read()
    gost=[int.from_bytes(b[i:i+6],'big') for i in range(4*6,7*6,6)]  # body13..15? actually 13..19=7 words
    print("A3 GOST words body[13..19]:")
    for j,w in enumerate([int.from_bytes(b[i:i+6],'big') for i in range(4*6, 11*6, 6)]):
        bb=[(w>>40)&255,(w>>32)&255,(w>>24)&255,(w>>16)&255,(w>>8)&255,w&255]
        print(f"  body[{13+j}] {w:016o} bytes={bb}")
    # new marker
    print("\nNEW marker 'OUR-CODE-RAN-7391':")
    ws, gb = encode("OUR-CODE-RAN-7391", nwords=7)
    print("bytes:", gb)
    for i,w in enumerate(ws): print(f"  word[{13+i}] : {w:016o}  bytes={[(w>>(40-8*k))&255 for k in range(6)]}")
