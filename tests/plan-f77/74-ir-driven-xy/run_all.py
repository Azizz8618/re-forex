#!/usr/bin/env python3
"""Phase-4 XY end-to-end driver: REAL Fortran decks -> FRONT IR -> GOST output.

For every variant a real BASE77 deck is edited, compiled through test 71's
inject/compile (FRONT.FTN rules 30..37), the IR is parsed by codegen_xy, the
combined bound+X/Y stream is installed at zone 0o2350 by installer_xy and the
REAL Fortran run is captured on copies of 2048.

Write scope: only /tmp/.private/azizz/opencode/re-forex-phase4-xy (and temp
copies of the shared disks under TMPDIR).  No repo edits / git writes.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent
FRONT1 = REPO / 'tests/plan-f77/71-front-base77'
CANON = REPO / 'docs/plan-f77-full/logs/f77_30_base77_deck_forex.txt'
SHARE = Path(os.environ.get('BESM6_DISK_SHARE', '/usr/local/share/besm6'))
TMPBASE = Path(os.environ.get('TMPDIR', '/tmp/.private/azizz/opencode'))
BASE = Path(os.environ.get(
    'XY74_WORK', tempfile.mkdtemp(prefix='xy74-', dir=str(TMPBASE))))

sys.path.insert(0, str(HERE))
import codegen_xy as cx
import installer_xy as ix

WORK = BASE / 'work'
IRD = BASE / 'ir'
EVID = BASE / 'evidence'
for d in (WORK, IRD, EVID):
    d.mkdir(parents=True, exist_ok=True)


def make_deck(tag, x, add, bound):
    """Edit the canonical deck; only the X/Y assignment and DO bound change."""
    text = CANON.read_text(encoding='utf-8')
    for old, new in (('DO 10 I=1,6', 'DO 10 I=1,%d' % bound),
                     ('X=1.0', 'X=%s' % x),
                     ('Y=X+2.0', 'Y=X+%s' % add)):
        if text.count(old) != 1:
            raise SystemExit('FAIL deck edit %r count=%d' % (old, text.count(old)))
        text = text.replace(old, new)
    p = WORK / ('%s.b6' % tag)
    p.write_text(text, encoding='utf-8')
    return p


def obtain_ir(tag, deck, mode='spec10'):
    """Run test 71 inject.py + compile.py on copies; return IR rows and log."""
    d = WORK / ('front_' + tag)
    d.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, FRONT1_WORK=str(d), FRONT1_DECK=str(deck),
               BESM6_DISK_SHARE=str(SHARE), TMPDIR=str(TMPBASE))
    log = []
    for script in ('inject.py', 'compile.py'):
        r = subprocess.run([sys.executable, str(FRONT1 / script), '--mode', mode],
                           cwd=d, env=env, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=600)
        log.append('%s rc=%d\n%s' % (script, r.returncode,
                                    r.stdout.decode('utf-8', 'replace')))
        (d / (script + '.log')).write_bytes(r.stdout)
        if r.returncode:
            raise SystemExit('FAIL %s for %s:\n%s' %
                             (script, tag, log[-1][-1000:]))
    irfile = d / ('ir_%s.txt' % mode)
    rows = cx.read_ir(irfile)
    shutil.copy(irfile, IRD / ('%s.txt' % tag))
    (EVID / ('%s_compile.log' % tag)).write_text('\n'.join(log))
    # compile.py copies ~113 MB of disks into d/work; we only need the IR text.
    shutil.rmtree(d / 'work', ignore_errors=True)
    return rows


VARIANTS = [
    dict(tag='canonical', x='1.0', add='2.0', bound=6, want='21 1.00 3.00'),
    dict(tag='x2y2b6',    x='2.0', add='2.0', bound=6, want='21 2.00 4.00'),
    dict(tag='x2y3b6',    x='2.0', add='3.0', bound=6, want='21 2.00 5.00'),
    dict(tag='x2y2b5',    x='2.0', add='2.0', bound=5, want='15 2.00 4.00'),
]


def main():
    os.environ.setdefault('M35XY_WORK', str(WORK / 'install'))
    o412, tail, obj = ix.load_fixtures()
    if not cx.cg.emit_deck_surface():
        raise SystemExit('FAIL: EMIT.FTN GOST table drifted')

    results = []
    ir_by_tag = {}
    for v in VARIANTS:
        deck = make_deck(v['tag'], v['x'], v['add'], v['bound'])
        rows = obtain_ir(v['tag'], deck)
        ir_by_tag[v['tag']] = rows
        bound, info, text, ov = cx.combined_stream(rows, obj)
        # Check the IR-derived bound matches the deck we actually ran.
        if bound != v['bound']:
            raise SystemExit('FAIL %s: IR bound %s != deck %s' %
                             (v['tag'], bound, v['bound']))
        res = ix.make_case(v['tag'], o412, tail, obj, ov,
                           note='IR bound=%d X=%s Y=%s dec=%d text=%r' %
                                (bound, info['x'], info['y'],
                                 info['decimals'], text))
        good = (res['printed'] == v['want']) and res['end']
        results.append(dict(case=v['tag'], kind='source', bound=bound,
                            x=info['x'], y=info['y'], decimals=info['decimals'],
                            seeded=text, want=v['want'], got=res['printed'],
                            end=res['end'], ok=good))
        print('%-12s bound=%d X=%s Y=%s text=%-14r printed=%-14r want=%-14r '
              'end=%s %s' % (v['tag'], bound, info['x'], info['y'], text,
                             res['printed'], v['want'], res['end'],
                             'OK' if good else 'FAIL'), flush=True)

    # ---- mutation cases: one emitted X/Y GOST word zeroed or byte-mutated ----
    rows = ir_by_tag['x2y2b6']   # base seeded text '01 2.00 4.00', bound 6
    bound, info, base_text, base_ov = cx.combined_stream(rows, obj)
    wa0, wb0 = base_ov[0o27], base_ov[0o30]

    muts = []
    ov = dict(base_ov); ov[0o27] = 0
    muts.append(('zero_x_word', ov, 'body[0o27]=0'))
    ov = dict(base_ov); ov[0o30] = 0
    muts.append(('zero_y_word', ov, 'body[0o30]=0'))
    ov = dict(base_ov); ov[0o27] = cx.set_gost_byte(wa0, 3, 9)  # X tens 2 -> 9
    muts.append(('mutate_x_digit', ov, 'X tens byte 2->9'))
    ov = dict(base_ov); ov[0o30] = cx.set_gost_byte(wb0, 2, 8)  # Y ones 4 -> 8
    muts.append(('mutate_y_digit', ov, 'Y ones byte 4->8'))

    base_print = '21 2.00 4.00'
    for name, ov, note in muts:
        res = ix.make_case(name, o412, tail, obj, ov, note=note)
        # Pass iff output changed from base and the task still ended.
        good = (res['printed'] != base_print) and res['end']
        results.append(dict(case=name, kind='mutation', bound=bound,
                            want='!= %s' % base_print, got=res['printed'],
                            end=res['end'], ok=good, note=note))
        print('%-16s printed=%-16r want=%-18r end=%s %s' %
              (name, res['printed'], '!= %s' % base_print, res['end'],
               'OK' if good else 'FAIL'), flush=True)

    (BASE / 'results.json').write_text(json.dumps(results, indent=2))
    ok = all(r['ok'] for r in results)
    print('VERDICT:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
