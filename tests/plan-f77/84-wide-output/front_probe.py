#!/usr/bin/env python3
"""Probe FRONT.FTN 777005 IR for arbitrary assignment RHS from a real deck.

Only writes under RT_GRAMMAR_WORK and temp disk copies; repo files are read-only.
"""
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent.parent
FRONT1 = REPO / 'tests/plan-f77/71-front-base77'
CANON = REPO / 'docs/plan-f77-full/logs/f77_30_base77_deck_forex.txt'
SHARE = Path(os.environ.get('BESM6_DISK_SHARE', '/usr/local/share/besm6'))
WORK = Path(os.environ.get('RT_GRAMMAR_WORK', '/tmp/.private/azizz/opencode/re-forex-grammar'))

VARS = {1: 'X', 2: 'Y', 3: 'N', 4: 'I'}
OPS = {0: 'LIT', 1: '+', 2: '-', 3: '*', 4: '/', 6: 'NEG'}


def front(tag, x_src, y_src, bound=6):
    d = WORK / 'front' / tag
    if d.exists():
        import shutil
        shutil.rmtree(d)
    d.mkdir(parents=True, exist_ok=True)
    text = CANON.read_text(encoding='utf-8')
    for old, new in (('X=1.0', x_src), ('Y=X+2.0', y_src),
                     ('DO 10 I=1,6', 'DO 10 I=1,%d' % bound)):
        if text.count(old) != 1:
            raise SystemExit('FAIL deck edit %r: %d matches' % (old, text.count(old)))
        text = text.replace(old, new)
    deck = d / 'base77.b6'
    deck.write_text(text, encoding='utf-8')
    env = dict(os.environ, FRONT1_WORK=str(d), FRONT1_DECK=str(deck),
               BESM6_DISK_SHARE=str(SHARE), TMPDIR=str(WORK))
    for script in ('inject.py', 'compile.py'):
        r = subprocess.run([sys.executable, str(FRONT1 / script), '--mode', 'spec10'],
                           cwd=d, env=env, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=600)
        (d / (script + '.log')).write_bytes(r.stdout)
        if r.returncode:
            raise SystemExit('FAIL %s: %s' % (script, r.stdout.decode('utf-8', 'replace')[-800:]))
    call = (d / 'work/spec10/call.out').read_text(errors='replace')
    ir = (d / 'ir_spec10.txt').read_text()
    # Disk copies are large; keep only the textual IR evidence.
    for f in (d / 'work/spec10').iterdir():
        if f.is_file() and f.name in {'2048', '2053', '2099', '2148', '2348', '2048-wr', 'dispak'}:
            f.unlink()
    recs = []
    for line in call.splitlines():
        m = re.match(r'^\s*777005\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s*$', line)
        if m:
            recs.append([int(v) for v in m.groups()])
    return d, call, ir, recs


def show(tag, x_src, y_src):
    d, call, ir, recs = front(tag, x_src, y_src)
    print('=== %s : %s ; %s ===' % (tag, x_src, y_src))
    print('777005 records (seq kind op arg1 arg2):')
    for seq, kind, op, a1, a2 in recs:
        if kind == 1:
            meaning = 'LIT %.2f' % (a1 / 100.0)
        elif kind == 2:
            meaning = 'VAR %s' % VARS.get(a1, '?' + str(a1))
        elif kind == 3:
            meaning = 'BIN %s' % OPS.get(op, '?' + str(op))
        else:
            meaning = 'UN %s' % OPS.get(op, '?' + str(op))
        print('  %3d %d %d %6d %d   %s' % (seq, kind, op, a1, a2, meaning))
    return recs


if __name__ == '__main__':
    for t, x, y in [
        ('base', 'X=1.0', 'Y=X+2.0'),
        ('mul_add', 'X=2.0', 'Y=X*2.0+1.0'),
        ('paren', 'X=2.0', 'Y=(X+1.0)*2.0'),
        ('frac_div', 'X=1.0', 'Y=X/4.0'),
        ('neg', 'X=-1.0', 'Y=X+2.0'),
        ('multidigit', 'X=12.0', 'Y=X*2.0+1.0'),
    ]:
        show(t, x, y)
