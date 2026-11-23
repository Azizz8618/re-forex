#!/usr/bin/env python3
"""C7 decks: six 777005 records, one per integrated feature.

Deck A = baseline; Deck B changes two IR records only:
  * LIT operand      1234 -> 5678  (record 1, arg1 digits)
  * binary-op token  TO=3 (*)  -> TO=1 (+) (record 3, TO field)
The image is byte-identical between the two decks.
"""
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
seed = (WS / "decks/deck_seed.b6").read_bytes().splitlines(keepends=True)
assert seed[7] == b"  777005       6       1       0    1234       0\n"
assert seed[14].startswith(b"\xd0\x95\xd0\x9a")  # trailing framing line


def field(x):
    return f"{x:>8}" if isinstance(x, str) else f"{x:8d}"


def rec(seq, tk, to, ta, tb):
    """1X-less FRONT 1X,6I8 card: 2sp + 777005 + five I8 fields (48 chars)."""
    return "  777005" + "".join(field(x) for x in (seq, tk, to, ta, tb))


# seq must be ONE digit: a two-digit seq shifts every following I8 field by a
# byte, moving TK off W+1 byte4 and TO off W+2 byte0 (verified by CORE dump).
BASE = [
    rec(1, 1, 0, 1234, 0),    # 1 LIT       (1234 -> 12.34)
    rec(2, 2, 0, 12, 0),      # 2 VARIABLE  (VIDX=12, name H -> 56.78)
    rec(3, 3, 3, 0, 0),       # 3 binary op TO=3 (*)  -> 03.75
    rec(4, 3, 6, 0, 0),       # 4 intrinsic TO=6 (SQRT) -> 04.00
    rec(5, 5, 4, 2, 0),       # 5 FORMAT width w=4 d=2 -> 34.50
    rec(6, 6, 1, "02", 1),    # 6 DO bound=2 step=1 -> 40.00
]


def make(name, records):
    lines = seed[:7] + [f"{r}\n".encode() for r in records] + seed[10:]
    out = WS / "decks" / name
    out.write_bytes(b"".join(lines))
    print(name, len(out.read_bytes()))
    for r in records:
        print("   ", repr(r))


make("deck_c7_A.b6", BASE)
B = list(BASE)
B[0] = rec(1, 1, 0, 5678, 0)     # LIT 1234 -> 5678
B[2] = rec(3, 3, 1, 0, 0)        # binary-op TO 3 (*) -> 1 (+)
make("deck_c7_B.b6", B)
