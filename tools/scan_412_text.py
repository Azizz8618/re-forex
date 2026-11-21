#!/usr/bin/env python3
"""Scan BESM-6 disp-format disk images for runtime module names.

Correct decoding (established by subagents + verified here):
  * on-disk zone_t = 8*8 (z_cwords) + 1024*8 (z_data) = 8256 bytes
  * logical zone L is stored at physical zone P = L + ZONE_OFFSET(4)
  * word value = little-endian uint64 at (P*8256 + 64 + w*8), low 48 bits
  * 6-bit TEXT (Dubna monitor): code -> glyph via TEXT table (code=ASCII-0x20
    for A-Z / digits); word = 8 chars, MSB first
"""
import sys, os, json

TEXT = " .БЦДФГИ()*ЙЛЯЖ/0123456789Ь,П-+ЫЗ" + "ABCDEFGHIJKLMNOPQRSTUVWXYZШЭЩЧЮ"
assert len(TEXT) == 64
ZL = 8256
ZONE_OFFSET = 4

def dec6(w):
    return ''.join(TEXT[(w >> sh) & 0o77] for sh in range(42, -1, -6))

def read_zone(data, phys):
    off = phys * ZL + 64
    if off + 1024*8 > len(data):
        return None
    return [int.from_bytes(data[off+w*8:off+w*8+8], 'little') & ((1<<48)-1)
            for w in range(1024)]

def scan(diskpath, needles):
    data = open(diskpath, 'rb').read()
    nphys = len(data) // ZL
    hits = {n: [] for n in needles}
    for phys in range(nphys):
        words = read_zone(data, phys)
        if words is None:
            continue
        logical = phys - ZONE_OFFSET
        # build a per-zone stream of decoded chars with (word,charpos) map
        stream = []
        posmap = []
        for w, val in enumerate(words):
            s = dec6(val)
            stream.append(s)
            posmap.extend([(w, c) for c in range(8)])
        line = ''.join(stream)
        for n in needles:
            start = 0
            while True:
                i = line.find(n, start)
                if i < 0:
                    break
                if i < len(posmap):
                    w, c = posmap[i]
                    hits[n].append({'zone': logical, 'word': w, 'char': c,
                                    'phys': phys, 'text': line[i:i+len(n)]})
                start = i + 1
    return hits

if __name__ == '__main__':
    needles = [
        'FORMAT', 'FORTLIBR', 'FT*002', 'FT*003', 'FT*571', 'FT*621',
        'FT*521', 'FT*531', 'FT*541', 'FT*561', 'FT*611', 'FT*641', 'FT*721',
        'FT*', 'DATAPR*', 'OCTTDEC', 'PRINT8', 'WRITLIBR', 'INSLIB',
        'LIBREFER', 'GIV/PG', 'TAK/PG', 'FOREX3*', 'FOREX*', 'LO*SYN',
        'LO*GEN', 'NEWCOMP*', 'DATE*', 'PREPDAT', 'DECODER',
    ]
    out = {}
    for d in ['2048', '2053', '2099', '2148']:
        p = os.path.join(os.path.dirname(__file__), 'disks', d)
        out[d] = scan(p, needles)
        print(f'=== disk {d}: hits ===', file=sys.stderr)
        for n in needles:
            hs = out[d][n]
            if hs:
                addrs = ', '.join(f"{h['zone']:04o}.{h['word']:04o}" for h in hs[:60])
                print(f'  {n}: {addrs}' + (f' ...(+{len(hs)-60})' if len(hs)>60 else ''), file=sys.stderr)
    with open(os.path.join(os.path.dirname(__file__), 'scan_text_results.json'), 'w') as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
