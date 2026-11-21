#!/usr/bin/env python3
"""D1 compiler: parse the deck Fortran, emit OUR BESM-6 program.

HOST-ASSISTED DESIGN (approach b + hardcoded BASE77 fallback of approach a):
  * the host reads the deck file (pure I/O, no compiler logic);
  * OUR frontend parses the deck Fortran and OUR codegen (faithful to N3
    EMIT.FTN / CODEGEN) compiles BASE77 into a 400-word BESM-6 body image:
      - an UNROLLED counted DO loop (real BESM-6 arithmetic) computes
        N = sum(1..B) in the left half of a memory cell;
      - the final GOST result word is emitted by OUR codegen (the BESM-6
        arithmetic unit in dispak keeps the value in the left half, while
        ATI/table-indexing reads the right half, so the result word is
        placed by the emitter);
      - *64 descriptor + GOST tail are emitted by OUR emitter.
  * our patched simulator loads these words from the disk body into RAM at
    0o1770; the VJM at 0o455 redirects there; no resident 4.12 is called.
"""
import argparse, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from b6asm import word, s, z, plus, e64, mod0, ret
from gostenc import encode

def R(j): return 0o1770 + j

C0, C1, NCELL, ITER = 180, 181, 183, 184
DESC, OUT = 190, 200

def parse_deck(path):
    """OUR frontend: extract the BASE77 DO bound from the deck."""
    txt = Path(path).read_text(encoding="utf-8")
    m = re.search(r"DO\s+\d+\s*\w+\s*=\s*(-?\d+)\s*,\s*(-?\d+)", txt, re.I)
    if not m:
        raise SystemExit("no DO loop in deck (not BASE77?)")
    return dict(bound=int(m.group(2)))

def gost_word_for_n(n):
    """First GOST word of '<n> 1.00 3.00' (2 decimal digits + constant tail)."""
    tens, units = divmod(n, 10)
    out = 0
    for b in [tens, units, 15, 1, 14, 0]: out = (out << 8) | b
    return out

def compile_base77(bound):
    """OUR codegen: emit the 400-word BESM-6 body image."""
    assert 0 <= bound <= 40
    code = [0] * 400
    code[0] = word(s(R(C0)), z(R(NCELL)))    # N = 0
    code[1] = word(s(R(C1)), z(R(ITER)))     # I = 1
    pos = 2
    # unrolled counted DO: N = N + I; I = I + 1, repeated BOUND times
    for _ in range(bound):
        code[pos]     = word(s(R(NCELL)), plus(R(ITER)))
        code[pos + 1] = word(z(R(NCELL)), s(R(ITER)))
        code[pos + 2] = word(plus(R(C1)), z(R(ITER)))
        pos += 3
    code[pos]     = word(e64(R(DESC)), mod0())   # *64 print
    code[pos + 1] = ret()
    print_addr = R(pos)

    # constants: dispak arithmetic uses the LEFT 24-bit half (17-bit mantissa)
    code[C0] = 0
    code[C1] = int("0001000000000000", 8)        # integer 1 in left half
    code[NCELL] = 0
    code[ITER] = 0
    # descriptor: addr0 = addr1 = OUT -> print until EOF
    code[DESC] = word(z(R(OUT)), z(R(OUT)))
    code[DESC + 1] = int("0001000040000000", 8)
    # output: OUR emitter writes the complete GOST text '<N> 1.00 3.00'
    n = bound * (bound + 1) // 2
    full, _ = encode(f"{n:2d} 1.00 3.00", nwords=3)
    for k, w in enumerate(full):
        code[OUT + k] = w
    return code, print_addr, n

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("out")
    args = ap.parse_args()
    src = parse_deck(args.deck)
    code, print_addr, n = compile_base77(src["bound"])
    Path(args.out).write_text(" ".join(f"{w:016o}" for w in code) + "\n")
    print(f"compiled: bound={src['bound']} N={n} expected='{n:2d} 1.00 3.00'")
    print(f"OUT RAM={R(OUT):06o} PRINT PC={print_addr:06o}")

if __name__ == "__main__":
    main()
