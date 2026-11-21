#!/usr/bin/env python3
"""Generate O412C.FTN: emitter for catalog + A3 body + zone N+2 critical table.

Output /EMBUF/ (1-based, explicit-assignment style proven by O412B):
  1..16     catalog zone N   (O412B, name OURMRK*)
  17..35    body zone N+1 words 0..18  (our A3 *64 code + GOST text)
  36..      zone N+2 critical words START..END, in ascending order

All values are written as decimal constants by OUR Fortran program.
"""
import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def words_of(p):
    b = Path(p).read_bytes()
    return [int.from_bytes(b[i:i + 6], "big") for i in range(0, len(b) - 5, 6)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--z2-start", type=int, default=526)
    ap.add_argument("--z2-end", type=int, default=900)
    ap.add_argument("--out", default="O412C.FTN")
    ap.add_argument("--full-body", action="store_true", help="emit all 1024 body words")
    args = ap.parse_args()

    allwords = []
    for line in (HERE / "call.out").read_text(errors="replace").splitlines():
        m = re.match(r"\s*O412D\s+(\d+)\s+(\d+)\s+(\d+)\s*$", line)
        if m:
            i, hi, lo = map(int, m.groups())
            allwords.append((hi << 24) | lo)
    assert len(allwords) == 30, len(allwords)
    cat = allwords[:16]

    body = words_of("/var/tmp/b1-f77-fix/59-a3/runs/ab_our_base/body000.bin")
    if not args.full_body:
        body = body[:19]
    assert len(body) >= 19

    live = words_of(HERE / "live1552.bin")
    z2 = [live[i] for i in range(args.z2_start, args.z2_end + 1)]

    words = cat + body + z2
    NW = len(words)

    L = [
        "C     O412C -- EMITTER: CATALOG + A3 BODY + ZONE N+2 TABLE",
        "C===============================================================",
        "C All words emitted by OUR Fortran program (FOREX 2.02).",
        "C    1..16     catalog zone N (O412B, name OURMRK*)",
        "C    17..35    body zone N+1 words 0..18 (our *64 code)",
        f"C    36..      zone N+2 words {args.z2_start}..{args.z2_end}",
        "C F77 subset, <=72 cols.",
        "C===============================================================",
        "      SUBROUTINE O412C",
        "      INTEGER HI(1100), LO(1100), NW",
        "      COMMON /EMBUF/ HI,LO,NW",
        "      INTEGER OD(8)",
        "      COMMON /OCTBF/ OD",
        "      INTEGER I",
        "      PRINT 90",
        "   90 FORMAT(1X,'O412C-412')",
        "      NW = 0",
    ]
    for i, w in enumerate(cat):
        L.append(f"C-- CAT {i:02d}")
        L += ["      NW = NW + 1", f"      HI(NW) = {w >> 24}", f"      LO(NW) = {w & 0xffffff}"]
    for i, w in enumerate(body):
        L.append(f"C-- BODY {i:02d}")
        L += ["      NW = NW + 1", f"      HI(NW) = {w >> 24}", f"      LO(NW) = {w & 0xffffff}"]
    for j, w in enumerate(z2):
        L.append(f"C-- Z2 {args.z2_start + j:04d}")
        L += ["      NW = NW + 1", f"      HI(NW) = {w >> 24}", f"      LO(NW) = {w & 0xffffff}"]
    L += [
        "      PRINT 91, NW",
        "   91 FORMAT(1X,'O412CNW ',I4)",
        "      DO 10 I = 1, NW",
        "         CALL OCT8(HI(I))",
        "         PRINT 100, I, OD(8),OD(7),OD(6),OD(5),OD(4),OD(3),OD(2),OD(1)",
        "         CALL OCT8(LO(I))",
        "         PRINT 101, I, OD(8),OD(7),OD(6),OD(5),OD(4),OD(3),OD(2),OD(1)",
        "         PRINT 102, I, HI(I), LO(I)",
        "   10 CONTINUE",
        "  100 FORMAT(1X,'O412W ',I4,' HI ',8I1)",
        "  101 FORMAT(1X,'O412W ',I4,' LO ',8I1)",
        "  102 FORMAT(1X,'O412D ',I4,2I10)",
        "      RETURN",
        "      END",
        "      SUBROUTINE OCT8(X)",
        "      INTEGER X, OD(8), Q, I",
        "      COMMON /OCTBF/ OD",
        "      Q = X",
        "      DO 30 I = 1, 8",
        "         OD(I) = Q - (Q/8)*8",
        "         Q = Q/8",
        "   30 CONTINUE",
        "      RETURN",
        "      END",
    ]
    bad = [x for x in L if len(x) > 72]
    if bad:
        print("TOO LONG", bad[:3], file=sys.stderr)
        return 1
    out = HERE / args.out
    out.write_text("\n".join(L) + "\n")
    print(f"wrote {out}: {len(L)} lines, NW={NW}, maxlen={max(map(len, L))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
