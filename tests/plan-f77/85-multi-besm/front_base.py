#!/usr/bin/env python3
"""Real-deck FRONT probe with the extended (copy-only) FRONT.FTN.

Reuses tests/plan-f77/71-front-base77/inject.py + compile.py verbatim (copies),
but injects our patched FRONT.FTN via FRONT1_SRC.  The BESM card is appended
after END so the original 10 cards keep byte-identical 777001..777005 records
and their SEQ numbering.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

W = Path(__file__).resolve().parent
REPO = W.parent.parent.parent
FRONT1 = W / 'harness'
CANON = REPO / 'docs/plan-f77-full/logs/f77_30_base77_deck_forex.txt'
SHARE = Path(os.environ.get('BESM6_DISK_SHARE', '/usr/local/share/besm6'))
WS = Path(os.environ.get(
    'BESM_IMPL_WORK', tempfile.mkdtemp(prefix='besm83-',
                                       dir=os.environ.get('TMPDIR', '/tmp'))))


def front(tag, besm_hi=None, besm_lo=None, with_besm=True, placement='after_end'):
    d = WS / 'front' / tag
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True, exist_ok=True)
    text = CANON.read_text(encoding='utf-8')
    if with_besm:
        if besm_hi is None or besm_lo is None:
            raise ValueError('hi/lo needed when BESM is inserted')
        if placement == 'after_end':
            marker = '      END\n'
            if text.count(marker) != 1:
                raise SystemExit('FAIL END marker count %d' % text.count(marker))
        elif placement == 'inline':
            marker = '      PRINT 100,N,X,Y\n'
            if text.count(marker) != 1:
                raise SystemExit('FAIL PRINT marker count %d' % text.count(marker))
        else:
            raise ValueError('unknown placement %r' % placement)
        card = '      BESM(%d,%d)\n' % (besm_hi, besm_lo)
        if len(card.rstrip('\n')) > 72:
            raise SystemExit('FAIL BESM card too long')
        text = text.replace(marker, marker + card)
    deck = d / 'base77.b6'
    deck.write_text(text, encoding='utf-8')
    env = dict(os.environ, FRONT1_WORK=str(d), FRONT1_DECK=str(deck),
               FRONT1_SRC=os.environ.get('FRONT1_SRC', str(W / 'FRONT.FTN')),
               BESM6_DISK_SHARE=str(SHARE), TMPDIR=str(WS))
    for script in ('inject.py', 'compile.py'):
        r = subprocess.run([sys.executable, str(FRONT1 / script), '--mode', 'spec10'],
                           cwd=d, env=env, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=900)
        (d / (script + '.log')).write_bytes(r.stdout)
        if r.returncode:
            raise SystemExit('FAIL %s: %s' % (
                script, r.stdout.decode('utf-8', 'replace')[-2000:]))
    call = (d / 'work/spec10/call.out').read_text(errors='replace')
    build = (d / 'work/spec10/build.out').read_text(errors='replace')
    ir = (d / 'ir_spec10.txt').read_text()
    errs = len(re.findall(r'\bERR\b|\bОШИБК', build + call, re.I))
    # Disk copies are large; retain only the textual IR evidence.
    for f in (d / 'work/spec10').iterdir():
        if f.is_file() and f.name in {'2048', '2053', '2099', '2148', '2348', '2348-wr', 'dispak'}:
            f.unlink()
    recs6 = []
    for line in call.splitlines():
        m = re.match(r'^\s*777006\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s*$', line)
        if m:
            recs6.append(tuple(int(v) for v in m.groups()))
    return d, call, build, ir, recs6, errs


if __name__ == '__main__':
    d, call, build, ir, recs, errs = front('probe', 46091, 1032)
    print('ERR count:', errs)
    for line in call.splitlines():
        if re.match(r'^\s*77700', line):
            print(line)
    print('777006:', recs)
