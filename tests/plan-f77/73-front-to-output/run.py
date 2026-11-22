#!/usr/bin/env python3
"""73 — full chain: Fortran source -> FRONT IR -> bound -> CODEGEN -> *TRANS output.

Unlike test 72 (bound supplied directly), this test derives the bound FROM A
REAL FORTRAN DECK through `src/newcomp/FRONT.FTN`: rule 32 (counted DO) emits an
ASCII stream 777002, from which the upper bound is parsed.  Then test 72's
CODEGEN/EMIT stream is installed at zone 0o2350 and the printed number is
checked.  Changing the source card 6 -> 5 must change the output 21 -> 15.

All compile/install steps run on COPIES with redirected HOME/BESM6_PATH.
"""
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
FRONT1 = ROOT / 'tests/plan-f77/71-front-base77'
M35 = ROOT / 'tests/plan-f77/72-bound-driven'
DECK0 = ROOT / 'docs/plan-f77-full/logs/f77_30_base77_deck_forex.txt'
SHARE = Path(os.environ.get('BESM6_DISK_SHARE', '/usr/local/share/besm6'))
WORK = Path(tempfile.mkdtemp(prefix='front2out-',
                             dir=os.environ.get('TMPDIR', '/tmp')))


def bound_from_deck(bound, tag):
    d = WORK / ('front_' + tag)
    d.mkdir(parents=True, exist_ok=True)
    deck = d / 'base77.b6'
    text = DECK0.read_text(encoding='utf-8')
    if 'DO 10 I=1,6' not in text:
        raise SystemExit('FAIL: canonical deck has no counted DO 6')
    deck.write_text(text.replace('DO 10 I=1,6', 'DO 10 I=1,%d' % bound),
                    encoding='utf-8')
    env = dict(os.environ, FRONT1_WORK=str(d), FRONT1_DECK=str(deck),
               BESM6_DISK_SHARE=str(SHARE))
    for script in ('inject.py', 'compile.py'):
        r = subprocess.run([sys.executable, str(FRONT1 / script), '--mode', 'spec10'],
                           cwd=d, env=env, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=600)
        (d / (script + '.log')).write_bytes(r.stdout)
        if r.returncode:
            raise SystemExit(f'FAIL {script}: {r.stdout.decode("utf-8", "replace")[-500:]}')
    ir = d / 'ir_spec10.txt'
    rows = []
    for line in ir.read_text().splitlines():
        parts = line.split()
        if len(parts) >= 3 and parts[0].startswith('777'):
            rows.append([int(x) for x in parts])
    seq = next(r[1] for r in rows if r[0] == 777001 and r[2] == 32)
    codes = [r[3] for r in rows if r[0] == 777002 and r[1] == seq]
    line = ''.join(chr(c) for c in codes)
    m = re.search(r'I\s*=\s*\d+\s*,\s*(\d+)', line)
    if not m:
        raise SystemExit(f'FAIL: bound not found in IR line {line!r}')
    got = int(m.group(1))
    print(f'{tag}: source bound={bound} IR rule32 line={line!r} parsed={got}',
          flush=True)
    return got


def main():
    for f in (FRONT1 / 'inject.py', FRONT1 / 'compile.py', M35 / 'installer.py',
              M35 / 'codegen.py', DECK0, SHARE / '2048', SHARE / '2053', SHARE / '2099'):
        if not Path(f).exists():
            raise SystemExit(f'FAIL: missing {f}')
    print('workspace:', WORK)
    os.environ['M35_WORK'] = str(WORK / 'install')
    sys.path.insert(0, str(M35))
    import installer as m35

    o412 = m35.parse_o412c()
    tail = m35.words_hex(m35.TAIL_HEX)
    obj = m35.words_hex(m35.OBJ_HEX)
    want = {6: '21 1.00 3.00', 5: '15 1.00 3.00'}
    ok = True
    for bound, tag in ((6, 'b6'), (5, 'b5')):
        got = bound_from_deck(bound, tag)
        res = m35.make_case(tag, o412, tail, obj, got)
        good = (got == bound and res['printed'] == want[bound] and res['end'])
        ok = ok and good
        print(f'{tag}: printed={res["printed"]!r} want={want[bound]!r} '
              f'end={res["end"]} {"OK" if good else "FAIL"}', flush=True)
    print('VERDICT:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
