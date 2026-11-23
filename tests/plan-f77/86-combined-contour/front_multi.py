#!/usr/bin/env python3
"""Real-deck FRONT probe with the extended (copy-only) FRONT.FTN.

Reuses tests/71's inject.py + compile.py verbatim (copies in ./harness), but
injects our patched FRONT.FTN via FRONT1_SRC.  Any number of BESM(...) cards and
V = BESM(...) assignment cards may be appended to the canonical deck after END; FRONT classifies
every card and emits one 777006 / 777007 record per card with increasing SEQ.
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
CANON = Path(os.environ.get('RE_FOREX_REPO', '/home/azizz/Yandex.Disk/re-forex')) / 'docs/plan-f77-full/logs/f77_30_base77_deck_forex.txt'
SHARE = Path(os.environ.get('BESM6_DISK_SHARE', '/usr/local/share/besm6'))
WS = Path(os.environ.get(
    'BESM_MULTI_WORK', tempfile.mkdtemp(prefix='besm85-',
                                         dir=os.environ.get('TMPDIR', '/tmp'))))


def front(tag, extra_cards=(), src=None, mode='spec10'):
    """Run FRONT on the canonical deck plus extra_cards placed after END.

    extra_cards: sequence of fixed-form card strings, column 7 onward already
                 prefixed with six spaces, e.g. '      BESM(46091,1032)'.
    Returns (workdir, call_text, build_text, ir_text, recs6, recs7, errs).
    """
    d = WS / 'front' / tag
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True, exist_ok=True)
    text = CANON.read_text(encoding='utf-8')
    marker = '      END\n'
    if text.count(marker) != 1:
        raise SystemExit('FAIL END marker count %d' % text.count(marker))
    ins = marker + ''.join(c.rstrip('\n') + '\n' for c in extra_cards)
    text = text.replace(marker, ins)
    deck = d / 'base77.b6'
    deck.write_text(text, encoding='utf-8')
    src_path = src or (W / 'FRONT.FTN')
    env = dict(os.environ, FRONT1_WORK=str(d), FRONT1_DECK=str(deck),
               FRONT1_SRC=str(src_path), BESM6_DISK_SHARE=str(SHARE),
               TMPDIR=str(WS))
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
                                      '2348', '2048-wr', 'dispak'}:
            f.unlink()
    recs6, recs7 = [], []
    for line in call.splitlines():
        m = re.match(r'^\s*777006\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s*$', line)
        if m:
            recs6.append(tuple(int(v) for v in m.groups()))
        m = re.match(r'^\s*777007\s+(-?\d+)\s+(-?\d+)\s*$', line)
        if m:
            recs7.append(tuple(int(v) for v in m.groups()))
    return d, call, build, ir, recs6, recs7, errs


if __name__ == '__main__':
    d, call, build, ir, r6, r7, errs = front(
        'probe', ['      BESM(46091,1032)', '      BESM(46092,1032)',
                  '      Y = BESM(33804,46091)'])
    print('ERR', errs)
    for line in call.splitlines():
        if re.match(r'^\s*77700[1-7]', line):
            print(line)
    print('777006:', r6)
    print('777007:', r7)
