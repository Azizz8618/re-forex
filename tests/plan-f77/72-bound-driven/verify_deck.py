#!/usr/bin/env python3
"""Host-side equivalence check: N3M35.FTN word list == installed word stream.

The deck is a FOREX 2.02 emitter (CODEGEN+EMIT wiring).  This checker folds
its constant arithmetic exactly as FOREX 2.02 would and compares the emitted
words with the stream that installer.py writes to the zone-2350 body, for
both BASE77 gate bounds.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from codegen import stream, gosten, MASK

WS = Path(__file__).resolve().parent
REPO = WS.parent.parent.parent
OBJ_HEX = REPO / 'tests/plan-f77/65-m80-install/ovl_our.hex'
ORDER = (9, 10, 11, 12, 0o25, 0o26, 0o27, 0o30, 0o31, 0o41, 0o42)


def deck_words(bound):
    text = (WS / 'N3M35.FTN').read_text()
    calls = re.findall(r'CALL N3EMIT\(([^,]+),\s*([^)]+)\)', text)
    nb = 0o1757                 # BASE is octal, 1007 decimal
    env = {'NB': str(nb), 'IT': str(bound - 4), 'IU': str(24 - 4 * bound)}
    out = []
    for hi, lo in calls:
        hi, lo = hi.strip(), lo.strip()
        if hi == '3843':        # N3G6 emits the GOST word just before word 8
            out.append(gosten([0, 1, 15, 1, 14, 0]))
        def ev(expr):
            for k, v in env.items():
                expr = expr.replace(k, v)
            return eval(expr, {'__builtins__': {}}, {})
        out.append(((ev(hi) << 24) | ev(lo)) & MASK)
    return out


def installed_words(bound):
    raw = bytes.fromhex(OBJ_HEX.read_text().strip())
    obj = [int.from_bytes(raw[i:i + 6], 'big') for i in range(0, len(raw) - 5, 6)]
    ov = stream(bound, obj)
    return [ov[k] & MASK for k in ORDER]


if __name__ == '__main__':
    ok = True
    for bound in (6, 5):
        deck = deck_words(bound)
        words = installed_words(bound)
        same = deck == words
        ok = ok and same
        print('bound %d: deck=%d words, installed=%d words, %s'
              % (bound, len(deck), len(words), 'MATCH' if same else 'MISMATCH'))
        for k, d, w in zip(ORDER, deck, words):
            if d != w:
                print('  body[%-3o] deck=%016o installed=%016o MISMATCH' % (k, d, w))
    print('VERDICT:', 'PASS' if ok else 'FAIL')
    sys.exit(0 if ok else 1)
