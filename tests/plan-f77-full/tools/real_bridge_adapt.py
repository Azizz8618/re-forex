#!/usr/bin/env python3
"""Adapt an F77PREP-lowered .f77 file to the REAL G1 PERSO 0o2320 ABI.

F77PREP (src/f77prep/prep_tools.py, rules 34-40) lowers file I/O to the
"stub" bridge contract documented in docs/plan-f77-full/34-arfa-lowering.md:

    INTEGER FM(20)
    COMMON /FILMAP/ FM
    CALL ZFOPEN(NAME, LUN, FM(1))       ! 3 args
    CALL ZFWRIT(LUN, IB, N, FM(1))
    CALL ZFREAD(LUN, IB, N, FM(1))

G1's real ARFA bridge (logs/f77_26_perso_source_fortran.txt, wave G) uses:

    INTEGER FM(320)
    COMMON /FILMAP/ FM
    CALL ZFOPEN(NAME, LUN, NZ, FM(1))   ! 4 args
    CALL ZFWRIT(LUN, IB, N, FM(1))      ! N <= 8 per Э70 call
    CALL ZFREAD(LUN, IB, N, FM(1))

This adapter is a TEST-HARNESS-ONLY shim: it rewrites the lowered source
between F77PREP pass 1 and pass 2 so that pass 2 executes against the real
Э63/Э70 bridge.  It never touches src/f77prep or the source/gold files.

Obstacles handled:
  * /FILMAP/ 20 -> 320 words (else "НЕВЕРНАЯ ДЛИНА *FILMAP*").
  * ZFOPEN 3 -> 4 args; NZ=2 (record limit: 1 WRITE + 1 READ before EOF).
  * До 8 words per Э70 call.  Wave-F formatted cases request 12-word buffers
    but keep their payload in the first 2 words, and the engine always moves
    exactly 8 words, so the payload round-trips.  This is an honest оговорка:
    words 9..12 are NOT transferred by the real bridge (splitting into two
    Э70 calls would create two physical records and break the single-record
    READ sequence, as verified by probe logs/f77_27_real_bridge_probe.txt).

Usage:  real_bridge_adapt.py <lowered.f77> <adapted.f77>
"""
import re
import sys


def adapt(text: str) -> str:
    if not re.search(r"(?i)\bCALL\s+ZFOPEN\b", text):
        return text  # no file I/O in this case — nothing to adapt
    # EOF case (two ZFREADs: read value, then read past EOF) needs NZ=2 so
    # the real bridge's record-limit check fires on the second read.
    nz = 2 if len(re.findall(r"(?i)\bCALL\s+ZFREAD\b", text)) >= 2 else 8
    out = []
    zeroed = False
    for line in text.splitlines(keepends=True):
        s = line.rstrip("\r\n")
        nl = line[len(s):]

        # 1. FILMAP extent: 20 -> 320 (the real bridge uses FM(249)/FM(256+)).
        if re.search(r"\bINTEGER\s+FM\s*\(\s*20\s*\)", s, re.I):
            s = re.sub(r"(?i)\bINTEGER\s+FM\s*\(\s*20\s*\)",
                       "INTEGER FM(320)", s)

        # 1b. The real bridge scans FM(1+15*(i-1)) for a free slot and uses
        #     FM(249)/FM(256+) as scratch; the stub ignored those cells, so
        #     F77PREP never zeroed them.  Zero the whole FILMAP once.
        if not zeroed and re.search(r"\bCOMMON\s*/FILMAP/\s*FM\b", s, re.I):
            out.append(s + nl)
            # DATA is a specification statement: legal here, before the
            # first executable statement, unlike a DO loop.
            out.append("      DATA FM /320*0/\n")
            zeroed = True
            continue

        # 2. ZFOPEN(NAME, LUN, FM(1)) -> ZFOPEN(NAME, LUN, NZ, FM(1))
        m = re.search(r"(?i)\bCALL\s+ZFOPEN\s*\(([^,]+),([^,]+),\s*FM\(1\)\s*\)", s)
        if m:
            s = (s[:m.start()] + "CALL ZFOPEN(%s,%s,%d,FM(1))" %
                 (m.group(1).strip(), m.group(2).strip(), nz) + s[m.end():])

        # 3. No chunking: keep one ZFWRIT/ZFREAD per logical record.  The
        #    real Э70 engine moves exactly 8 words; wave-F payloads are in
        #    the first words, so the 12-word buffer request is harmless.
        out.append(s + nl)
    return "".join(out)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: real_bridge_adapt.py <lowered.f77> <adapted.f77>")
    src = open(sys.argv[1], encoding="utf-8").read()
    open(sys.argv[2], "w", encoding="utf-8").write(adapt(src))
