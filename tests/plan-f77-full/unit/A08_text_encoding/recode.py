#!/usr/bin/env python3
"""A8 host postprocessor: BESM-6 6-bit TEXT -> intended F77 ASCII.

dispak decodes 6-bit TEXT words through the BESM-6 printer table. The 12
Latin letters below are rendered as their Cyrillic homoglyphs; all other
A-Z, a-z (folded to upper) and 0-9 pass through. F77 source is upper-case
by convention, so the inverse map emits upper-case ASCII.
"""
import sys
# observed (U+04xx Cyrillic) -> intended (ASCII)
TABLE = {
    "\u0410":"A", "\u0412":"B", "\u0421":"C", "\u0415":"E",
    "\u041D":"H", "\u041A":"K", "\u041C":"M", "\u041E":"O",
    "\u0420":"P", "\u0422":"T", "\u0425":"X", "\u0423":"Y",
}
def recode(line):
    return "".join(TABLE.get(c, c) for c in line)
if __name__ == "__main__":
    data = sys.stdin.read()
    sys.stdout.write("".join(recode(l) + "\n" for l in data.splitlines()))
