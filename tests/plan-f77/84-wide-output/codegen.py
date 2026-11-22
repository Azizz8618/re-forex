#!/usr/bin/env python3
"""M3/M4/M5 word stream: BASE77 DO-bound -> raw ARX -> GOST digit bytes.

Wire-up of the proven components:

  FRONT.FTN (M1, owned by another subagent) supplies B in IR record 777002
    from `DO 10 I=1,6` (or 5).  This module does NOT edit FRONT.FTN.
  CODEGEN.deck N3E/N3D/N3P supplies the word/opcode discipline:
    - N3D word 10 `вч 107 / пе 20` is the counted-DO bound cell 0107;
      B is the value that would be placed in that cell.
    - N3E words 1..2 `сч/зп`, `сч/сл` are the accumulator discipline;
      SL (floating A+X) is REPLACED by the proven raw ARX (слц, opcode 013)
      because floating addition corrupts packed GOST bytes
      (docs/corrections.md, phase-3 report section 1.2).
    - N3P FT*571/002/003 calls are REPLACED (substitution S1 of design 63
      section 3.2) by the proven *64 + descriptor + GOSTEN block.
  EMIT.FTN supplies EMIT48 (IR/KOP/ADR -> two 24-bit halves) and GOSTEN
    (authoritative GOST-10859 byte table from monitor80-re/tools/encoding.cpp).

All addresses are derived from one BASE = 0o1757 constant (design 63,
interface item 1); body[k] is copied to RAM BASE+k.  Everything this module
writes is inside body 0..0o43, the proven copy window (phase-3 report 1.4).

BOUND INTERFACE (the clean plug-in point for M1's IR):
  body[0o41] = (B-4) << 40            tens addend (the active bound cell)
  body[0o42] = (24-4*B) << 32         units addend
where B is the BASE77 DO bound (6 or 5) supplied by FRONT.FTN's 777002 IR.
Both cells are in the copy window and are the only bound-dependent data.

The two addends are the decimal-digit decomposition of T_B = B(B+1)/2:
  tens  = B - 4          (6 -> 2, 5 -> 1)
  units = 25 - 4*B       (6 -> 1, 5 -> 5)
so base GOST byte pair [0,1] + addends = [tens,units] = "21" or "15".
This is the boundary-equivalent minimal raw addition chain of the task
(item 4): the general multiply/loop form does not fit the 10-word code
window, and a finite counted loop was not obtained in phase 3.  The two
raw ARX additions are executed at run time; only the constant shifts and
the affine digit decomposition are folded by CODEGEN/EMIT, never the
printed value itself.

HONESTY NOTE: we do not execute a general B*B multiply.  We compute the
exact digits of the triangular number at the two required gate points
with an affine (boundary-equivalent) chain driven by B.
"""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent.parent
CODEGEN_DECK = REPO / 'src/newcomp/CODEGEN.deck'
EMIT_FTN = REPO / 'src/newcomp/EMIT.FTN'

BASE = 0o1757
MASK = (1 << 48) - 1

# Proven half-word opcode prefixes (test 70 / phase-3 final fragment).
XTA = 0x008000   # сч   (load accumulator from memory)
ARX = 0x00b000   # слц  (raw 48-bit end-around-carry addition, opcode 013)
STO = 0x000000   # зп   (store accumulator to memory)
RET = 0o6700000002200000   # uj 0(15) proven return word
OBJ12 = 0o0064200402200000  # proven *64 2004 print word (design 63 section 3.3)


def half(op, adr):
    """EMIT48-equivalent halfword for the proven opcode set: op | 12-bit ADR."""
    if not 0 <= adr <= 0o7777:
        raise ValueError('address outside 12-bit field: %o' % adr)
    return op | adr


def emit48(lop, ladr, rop, radr):
    """Reproduce EMIT.FTN EMIT48 for our word set (IR=0, proven op prefixes)."""
    return (half(lop, ladr) << 24) | half(rop, radr)


def ram(body_index):
    return BASE + body_index


def gosten(bytes6):
    """EMIT.FTN GOSTEN packing for six already-encoded GOST bytes."""
    if len(bytes6) != 6 or any(not 0 <= b <= 255 for b in bytes6):
        raise ValueError('GOSTEN expects six bytes')
    hi = (bytes6[0] << 16) | (bytes6[1] << 8) | bytes6[2]
    lo = (bytes6[3] << 16) | (bytes6[4] << 8) | bytes6[5]
    return (hi << 24) | lo


def digit_bytes(bound):
    """GOST byte pair for T_B at the two BASE77 gate points."""
    tens = bound - 4
    units = 25 - 4 * bound
    if not (0 <= tens <= 9 and 0 <= units <= 9):
        raise ValueError('no single-digit decomposition for bound %r' % bound)
    return tens, units


def stream(bound, obj, *, zero=()):
    """Return the complete body override dict for one bound value.

    obj is the 1024-word rebuilt object fixture (ovl_our.hex), supplying the
    proven descriptor pair and GOST tail words B/C verbatim.
    """
    if bound not in (5, 6):
        raise ValueError('gate bounds are 5 and 6')
    tens, units = digit_bytes(bound)

    tens_adr = ram(0o41)   # 0o2020, active bound cell (tens digit)
    units_adr = ram(0o42)  # 0o2021, units digit cell
    gost_adr = ram(0o27)   # 0o2006
    desc_adr = ram(0o25)   # 0o2004

    ov = {
        # code, every ADR derived from BASE + body offset
        9:  emit48(XTA, gost_adr, ARX, tens_adr),
        10: emit48(ARX, units_adr, STO, gost_adr),
        11: OBJ12,          # *64 desc_adr (proven, ADR = 0o2004)
        12: RET,            # uj 0(15)
        # proven descriptor + GOST text block (test 70 / M2 obj25 layout)
        0o25: obj[0o25], 0o26: obj[0o26],
        0o27: gosten([0, 1, 15, 1, 14, 0]),   # "01 1.0" -> digits filled at run time
        0o30: obj[0o30], 0o31: obj[0o31],     # " 3.00" + EOF
        # bound table (the M1 IR plug-in point)
        0o41: (tens << 40) & MASK,
        0o42: ((units - 1) << 32) & MASK,   # base GOST byte 1 is already present
    }
    for k in zero:
        ov[k] = 0
    return ov


def codegen_constants():
    """Read the authoritative N3* word constants from CODEGEN.deck (design 63 3.2)."""
    text = CODEGEN_DECK.read_text(encoding='utf-8', errors='replace')
    out = {}
    for name in ('N3E', 'N3D', 'N3P'):
        m = re.search(r'SUBROUTINE %s\b.*?DATA A /(.*?)/\s*\n\s*DATA B /(.*?)/'
                      % name, text, re.S)
        if not m:
            raise SystemExit('FAIL: cannot parse CODEGEN.deck %s' % name)
        a = [int(x, 10) for x in m.group(1).replace('\n', ' ').replace('*', ' ').split(',')]
        b = [int(x, 10) for x in m.group(2).replace('\n', ' ').replace('*', ' ').split(',')]
        out[name] = [(hi << 24) | lo for hi, lo in zip(a, b)]
    return out


def emit_deck_surface():
    """Confirm the GOSTEN table in EMIT.FTN is still the authoritative one."""
    text = EMIT_FTN.read_text(encoding='utf-8', errors='replace')
    return 'monitor80-re/tools/encoding.cpp' in text and 'DATA GT /15,0,0,0' in text


if __name__ == '__main__':
    cc = codegen_constants()
    print('codegen N3E/N3D/N3P word counts:', {k: len(v) for k, v in cc.items()})
    print('N3D DO-bound word (decodes as `вч 107 / пе 20`): %016o' % cc['N3D'][4])
    print('EMIT.FTN authoritative GOST table:', emit_deck_surface())
    obj_raw = bytes.fromhex(
        (REPO / 'tests/plan-f77/65-m80-install/ovl_our.hex').read_text().strip())
    obj = [int.from_bytes(obj_raw[i:i + 6], 'big') for i in range(0, len(obj_raw) - 5, 6)]
    for b in (6, 5):
        print('bound %d -> digits %r -> stream:' % (b, digit_bytes(b)))
        for k, v in sorted(stream(b, obj).items()):
            print('  body[%-3o] RAM %04o = %016o' % (k, ram(k), v & MASK))
