#!/usr/bin/env python3
"""77 — real FRONT.FTN 777005 tokens drive the RUNTIME X/Y codegen.

Bridges the two newly proven halves:
  test 71/75: Fortran deck -> FRONT.FTN -> IR 777002 + 777005 (postfix RHS)
  test 76:    token stream -> BESM-6 ARX words -> digits appear at run time

The X/Y values and the DO bound are read ONLY from the IR produced by FRONT;
the GOST words installed on disk have zero digit bytes before execution.
Zone 0o2350, deck *TRANS:OURMRK*,,412350, all writes on COPIES.
"""
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent
FRONT1 = REPO / 'tests/plan-f77/71-front-base77'
R76 = HERE.parent / '76-runtime-xy'
CANON = REPO / 'docs/plan-f77-full/logs/f77_30_base77_deck_forex.txt'
SHARE = Path(os.environ.get('BESM6_DISK_SHARE', '/usr/local/share/besm6'))
TMPBASE = Path(os.environ.get('TMPDIR', '/tmp'))
WORK = Path(tempfile.mkdtemp(prefix='ir2rt-', dir=str(TMPBASE)))
sys.path.insert(0, str(R76))
import runtime_xy as rx

VARS = {1: 'X', 2: 'Y', 3: 'N', 4: 'I'}
OPS = {1: '+', 2: '-', 3: '*', 4: '/'}


def front_ir(tag, x, add, bound):
    d = WORK / ('front_' + tag)
    d.mkdir(parents=True, exist_ok=True)
    text = CANON.read_text(encoding='utf-8')
    for old, new in (('X=1.0', 'X=%s' % x), ('Y=X+2.0', 'Y=X+%s' % add),
                     ('DO 10 I=1,6', 'DO 10 I=1,%d' % bound)):
        if text.count(old) != 1:
            raise SystemExit(f'FAIL deck edit {old!r}: {text.count(old)} matches')
        text = text.replace(old, new)
    deck = d / 'base77.b6'
    deck.write_text(text, encoding='utf-8')
    env = dict(os.environ, FRONT1_WORK=str(d), FRONT1_DECK=str(deck),
               BESM6_DISK_SHARE=str(SHARE), TMPDIR=str(TMPBASE))
    for script in ('inject.py', 'compile.py'):
        r = subprocess.run([sys.executable, str(FRONT1 / script), '--mode', 'spec10'],
                           cwd=d, env=env, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=600)
        (d / (script + '.log')).write_bytes(r.stdout)
        if r.returncode:
            raise SystemExit(f'FAIL {script}: {r.stdout.decode("utf-8", "replace")[-500:]}')
    call = (d / 'work/spec10/call.out').read_text(errors='replace')
    ir = (d / 'ir_spec10.txt').read_text()
    return call, ir


def lhs_by_seq(ir_text):
    out = {}
    rows = []
    for line in ir_text.splitlines():
        p = line.split()
        if len(p) >= 4 and p[0] == '777002':
            rows.append((int(p[1]), int(p[3])))
    for seq, code in rows:
        out.setdefault(seq, []).append(chr(code))
    return {seq: ''.join(codes).split('=')[0].strip()
            for seq, codes in out.items() if '=' in ''.join(codes)}


def tokens_from_ir(call, ir):
    recs = []
    for line in call.splitlines():
        m = re.match(r'^\s*777005\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s*$', line)
        if m:
            recs.append([int(v) for v in m.groups()])
    if not recs:
        raise SystemExit('FAIL: no 777005 records in IR')
    lhs = lhs_by_seq(ir)
    tokens = []
    for i, (seq, kind, op, a1, a2) in enumerate(recs):
        if kind == 1:
            tokens.append(('CONST', None, a1 / 100.0))
        elif kind == 2:
            name = VARS.get(a1)
            if not name:
                raise SystemExit(f'FAIL unknown variable index {a1}')
            tokens.append(('VAR', None, name))
        elif kind == 3 and op == 1:
            tokens.append(('ADD', None, None))
        elif kind == 4 and op == 6:
            tokens.append(('NEG', None, None))
        else:
            raise SystemExit(f'FAIL unsupported token kind={kind} op={op}')
        # STORE once, after the final token of each assignment's seq group
        last_in_group = (i + 1 == len(recs)) or (recs[i + 1][0] != seq)
        if last_in_group:
            name = lhs.get(seq)
            if name:
                tokens.append(('STORE', name, None))
    return tokens, recs


def bound_from_ir(ir):
    rows = []
    for line in ir.splitlines():
        p = line.split()
        if len(p) >= 3 and p[0].startswith('777'):
            rows.append([int(x) for x in p])
    seq = next(r[1] for r in rows if r[0] == 777001 and r[2] == 32)
    codes = [r[3] for r in rows if r[0] == 777002 and r[1] == seq]
    line = ''.join(chr(c) for c in codes)
    m = re.search(r'I\s*=\s*\d+\s*,\s*(\d+)', line)
    return int(m.group(1))


def main():
    cases = [('canonical', '1.0', '2.0', 6, '21 1.00 3.00'),
             ('x2y2', '2.0', '2.0', 6, '21 2.00 4.00'),
             ('x2y3', '2.0', '3.0', 6, '21 2.00 5.00'),
             ('x2b5', '2.0', '2.0', 5, '15 2.00 4.00')]
    print('workspace:', WORK)
    o412, tail, obj = rx.load_fixtures()
    ok = True
    for tag, x, add, bound, want in cases:
        call, ir = front_ir(tag, x, add, bound)
        tokens, recs = tokens_from_ir(call, ir)
        b_ir = bound_from_ir(ir)
        ov, meta = rx.emit(tokens, b_ir, obj)
        res = rx.make_case(tag, o412, tail, obj, ov,
                           note='IR-driven X/Y from Fortran deck')
        good = (b_ir == bound and res['printed'] == want and res['end'])
        ok = ok and good
        print(f'{tag:10s} tokens={len(recs):2d} X={meta["x"]:g} add={meta["add"]:g} '
              f'B={b_ir} pre_x={res["pre_x"]} pre_y={res["pre_y"]} '
              f'printed={res["printed"]!r} want={want!r} {"OK" if good else "FAIL"}',
              flush=True)
    print('VERDICT:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
