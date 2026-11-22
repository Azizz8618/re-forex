#!/usr/bin/env python3
"""Real-deck FRONT probe for the COMBINED wide-output + multi-BESM contour.

Copy-only: uses the patched FRONT.FTN (FRONT rules 38/39) and the test-71
inject.py/compile.py copies in ./harness.  The canonical deck is edited in
place on a COPY: X=1.0 / Y=X+2.0 are replaced by the requested wide
assignments, and any number of BESM(...) / V = BESM(...) cards are appended
after END.  FRONT therefore emits, in one compilation, both the ordinary
777005 IR of the wide assignments and the 777006/777007 records of the inserts.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

W = Path(__file__).resolve().parent
HARNESS = W / 'harness'
REPO = Path(os.environ.get('RE_FOREX_REPO', '/home/azizz/Yandex.Disk/re-forex'))
CANON = REPO / 'docs/plan-f77-full/logs/f77_30_base77_deck_forex.txt'
SHARE = Path(os.environ.get('BESM6_DISK_SHARE', '/usr/local/share/besm6'))
WS = Path(os.environ.get(
    'COMBINED_WORK', tempfile.mkdtemp(prefix='combined-p9-',
                                      dir=os.environ.get('TMPDIR', '/tmp'))))


def front(tag, x_src, y_src, extra_cards=(), bound=6, src=None, mode='spec10'):
    """Compile a real edited deck; return (workdir, call, ir, recs5, recs6, recs7, errs)."""
    d = WS / 'front' / tag
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True, exist_ok=True)
    text = CANON.read_text(encoding='utf-8')
    edits = (('X=1.0', x_src), ('Y=X+2.0', y_src),
             ('DO 10 I=1,6', 'DO 10 I=1,%d' % bound))
    for old, new in edits:
        if text.count(old) != 1:
            raise SystemExit('FAIL deck edit %r: %d matches' % (old, text.count(old)))
        text = text.replace(old, new)
    marker = '      END\n'
    if text.count(marker) != 1:
        raise SystemExit('FAIL END marker count %d' % text.count(marker))
    ins = marker + ''.join(c.rstrip('\n') + '\n' for c in extra_cards)
    text = text.replace(marker, ins)
    for card in extra_cards:
        if len(card.rstrip('\n')) > 72:
            raise SystemExit('FAIL card too long: %r' % card)
    deck = d / 'base77.b6'
    deck.write_text(text, encoding='utf-8')
    src_path = src or (W / 'FRONT.FTN')
    env = dict(os.environ, FRONT1_WORK=str(d), FRONT1_DECK=str(deck),
               FRONT1_SRC=str(src_path), BESM6_DISK_SHARE=str(SHARE),
               TMPDIR=str(WS), RE_FOREX_REPO=str(REPO))
    for script in ('inject.py', 'compile.py'):
        r = subprocess.run([sys.executable, str(HARNESS / script), '--mode', mode],
                           cwd=d, env=env, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=900)
        (d / (script + '.log')).write_bytes(r.stdout)
        if r.returncode:
            raise SystemExit('FAIL %s: %s' % (
                script, r.stdout.decode('utf-8', 'replace')[-2500:]))
    call = (d / ('work/%s/call.out' % mode)).read_text(errors='replace')
    build = (d / ('work/%s/build.out' % mode)).read_text(errors='replace')
    ir = (d / ('ir_%s.txt' % mode)).read_text()
    errs = len(re.findall(r'\bERR\b|\bОШИБК', build + call, re.I))
    # Keep only textual evidence; disk copies are large.
    for f in (d / ('work/%s' % mode)).iterdir():
        if f.is_file() and f.name in {'2048', '2053', '2099', '2148',
                                      '2348', '2348-wr', 'dispak'}:
            f.unlink()
    recs5, recs6, recs7 = [], [], []
    for line in call.splitlines():
        m = re.match(r'^\s*777005\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s*$', line)
        if m:
            recs5.append(tuple(int(v) for v in m.groups()))
        m = re.match(r'^\s*777006\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s*$', line)
        if m:
            recs6.append(tuple(int(v) for v in m.groups()))
        m = re.match(r'^\s*777007\s+(-?\d+)\s+(-?\d+)\s*$', line)
        if m:
            recs7.append(tuple(int(v) for v in m.groups()))
    # Persist the real edited deck as evidence.
    (d / 'deck.txt').write_text(text, encoding='utf-8')
    return d, call, ir, recs5, recs6, recs7, errs


if __name__ == '__main__':
    d, call, ir, r5, r6, r7, errs = front(
        'probe', 'X=1234.56', 'Y=X*2.0+1.0',
        ['      BESM(33800,46091)', '      Y = BESM(1032,33804)',
         '      BESM(33800,46090)', '      BESM(1032,1032)'])
    print('ERR', errs)
    for line in call.splitlines():
        if re.match(r'^\s*77700[1-7]', line):
            print(line)
    print('777005:', r5)
    print('777006:', r6)
    print('777007:', r7)
