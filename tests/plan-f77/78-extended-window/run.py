#!/usr/bin/env python3
"""78 — the `*TRANS` body copy window is NOT capped at body[0o43].

Focused reproduction of docs/64: a sentinel placed at body[0o46] arrives in RAM
at 0o2041 (shift +0o14), and our own instruction reads it to change the printed
digit. The special descriptor words at 0o44/0o223/0o603 are left untouched.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness as h


def main():
    cases = [
        ('baseline', {}, 1, 1, '21 1.00 3.00'),
        ('ext3', {9: h.word(h.XTA, h.GOST, h.ARX, 0o2041), 0o46: 3 << 40,
                  0o41: 0}, 0, 1, '41 1.00 3.00'),
        ('ext5', {9: h.word(h.XTA, h.GOST, h.ARX, 0o2041), 0o46: 5 << 40,
                  0o41: 0}, 0, 1, '61 1.00 3.00'),
        ('ext0', {9: h.word(h.XTA, h.GOST, h.ARX, 0o2041), 0o46: 0,
                  0o41: 0}, 0, 1, '11 1.00 3.00'),
    ]
    print('workspace:', h.WS)
    ok = True
    for name, patch, a1, a2, want in cases:
        r = h.run_case(name, body_patch=patch, a1=a1, a2=a2, core=True)
        ram = h.core_word(r['core'], 0o2041)
        good = (r['printed'] == want) and r['end']
        ok = ok and good
        print(f'{name:9s} printed={r["printed"]!r:18s} want={want!r:18s} '
              f'end={r["end"]} core@2041={"none" if ram is None else "%016o" % ram} '
              f'{"OK" if good else "FAIL"}', flush=True)
    print('VERDICT:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
