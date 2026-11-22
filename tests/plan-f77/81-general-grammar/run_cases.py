#!/usr/bin/env python3
"""End-to-end A/B: real Fortran deck -> FRONT IR -> general codegen -> console.

Every case writes only under RT_GRAMMAR_WORK and uses temp COPIES of the disks;
HOME/BESM6_PATH are redirected.  No repo edits, git writes, live disks, tmux,
processes or dispak sources.
"""
import json
import os
import re
import shutil
import sys
from pathlib import Path

WORK = Path(os.environ.get('RT_GRAMMAR_WORK', '/tmp/.private/azizz/opencode/re-forex-grammar'))
os.environ.setdefault('RT_GRAMMAR_WORK', str(WORK))
os.environ.setdefault('TMPDIR', '/tmp/.private/azizz/opencode')
os.environ.setdefault('BESM6_DISK_SHARE', '/usr/local/share/besm6')

import expr_ir as ex
import codegen_general as cgen
import front_probe as fp
import runtime_xy as rx

EVID = cgen.WORK / 'evidence'
EVID.mkdir(parents=True, exist_ok=True)

# name, X source, Y source, DO bound, zeroed body words, note
# name, X source, Y source, bound, zeroed words, note, expected-console override
CASES = [
    ('A_mul_add', 'X=2.0', 'Y=X*2.0+1.0', 6, (), 'baseline: IR tokens BIN* + BIN+', None),
    ('B_sub',     'X=2.0', 'Y=X*2.0-1.0', 6, (), 'operator + -> - in IR', None),
    ('B_paren',   'X=2.0', 'Y=(X+1.0)*2.0', 6, (), 'parentheses reorder BIN+ / BIN*', None),
    ('B_x3',      'X=3.0', 'Y=X*2.0+1.0', 6, (), 'X literal operand 2 -> 3', None),
    ('C_div',     'X=1.0', 'Y=X/4.0', 6, (), 'BIN/ and 2-decimal fraction', None),
    ('D_neg',     'X=-1.0', 'Y=X+2.0', 6, (), 'UN NEG (unary minus)', None),
    ('E_wide',    'X=12.0', 'Y=X*2.0+1.0', 6, (), 'two integer digits', None),
    ('F_zero_wA', 'X=2.0', 'Y=X*2.0+1.0', 6, (0o41,), 'A/B: zero data word wA', '00 00.00 05.00'),
    ('G_zero_wC', 'X=2.0', 'Y=X*2.0+1.0', 6, (0o43,), 'A/B: zero data word wC', '21 02.00 00.00'),
    ('H_zero_c13', 'X=2.0', 'Y=X*2.0+1.0', 6, (13,), 'A/B: zero code word body[13]', '21 02.00 00.00'),
    ('M_mtr',     'X=2.0', 'Y=X*2.0+1.0', 6, (), 'MTR trace case', None),
]

LINE = re.compile(r'^\s*(\d\d)\s+([- ]\d\d\.\d\d)\s+([- ]\d\d\.\d\d)\s*$')


def norm(s):
    return ' '.join(s.split())


def parse_printed(out):
    for line in out.splitlines():
        if 'TRANS' in line:
            continue
        m = LINE.match(line)
        if m:
            return norm(line.strip())
    return None


def main():
    o412, tail, obj = rx.load_fixtures()
    print('workspace:', WORK)
    print('machine N=%04o  XTA=%06o ARX=%06o STO=%06o  G1=%04o G2=%04o G3=%04o' %
          (rx.N, cgen.XTA, cgen.ARX, cgen.STO, cgen.A_G1, cgen.A_G2, cgen.A_G3))
    results = []
    only = os.environ.get('RT_GRAMMAR_ONLY')
    for name, xs, ys, bound, zero, note, want_override in CASES:
        if only and name not in only.split(','):
            continue
        d, call, ir, recs = fp.front(name, xs, ys, bound)
        toks, counts = ex.tokens(recs, ir)
        env = ex.evaluate(toks)
        b_ir = ex.bound_from_ir(ir)
        if b_ir != bound:
            raise SystemExit('FAIL %s bound IR=%d want=%d' % (name, b_ir, bound))
        ov, meta = cgen.emit(env, b_ir, obj, zero=zero)

        ir_dump = ['case=%s  %s ; %s' % (name, xs, ys),
                   'DO bound from IR (777001/777002): %d' % b_ir,
                   'LHS from 777002: %r' % ex.lhs_by_seq(ir),
                   '777005 records (seq kind op arg1 arg2):']
        for r in recs:
            ir_dump.append('  ' + ' '.join('%6d' % v for v in r))
        ir_dump.append('decoded tokens (kind, op, arg):')
        for t in toks:
            ir_dump.append('  %r' % (t,))
        ir_dump.append('IR-evaluated env: %s' % {k: str(v) for k, v in env.items()})
        ir_dump.append('expected console: %s' % meta['expected'])
        ir_dump.append('packed weights: wA=%016o wB=%016o wC=%016o' %
                       (meta['wA'], meta['wB'], meta['wC']))
        (EVID / (name + '_ir.txt')).write_text('\n'.join(ir_dump) + '\n')

        # MTR only for the dedicated case.
        if name == 'M_mtr':
            os.environ['BESM6_DD_DEBUG'] = '1'
            # Narrow window over our 8 code words only: a wide window re-arms
            # the MTR tracer after the run and floods the console (cu.c).
            os.environ['BESM6_MTR_LO'] = '01770'
            os.environ['BESM6_MTR_HI'] = '01777'
            os.environ['BESM6_MTR_N'] = '100'
            os.environ['BESM6_MTR_SKIP'] = '6'
        res = rx.make_case(name, o412, tail, obj, ov, keep=True,
                           note='%s | %s | %s | zero=%s' % (xs, ys, note, list(zero)))
        if name == 'M_mtr':
            for k in ('BESM6_DD_DEBUG', 'BESM6_MTR_LO', 'BESM6_MTR_HI',
                      'BESM6_MTR_N', 'BESM6_MTR_SKIP'):
                os.environ.pop(k, None)
        case_dir = cgen.WORK / 'machine' / 'cases' / name
        out_text = (case_dir / 'out.txt').read_text(errors='replace')
        got = parse_printed(out_text)
        want = norm(want_override) if want_override else norm(meta['expected'])
        # Pre-run digit bytes must be zero (checked from the installed disk copy).
        pre = rx.dump_body(case_dir, 'pre2')
        pre_bytes = {n: rx.byte_of(pre[adr - cgen.cg.BASE], off)
                     for n, (adr, off) in meta['zero_slots'].items()}
        pre_ok = all(v == 0 for v in pre_bytes.values())
        good = (got == want) and res['end'] and pre_ok
        results.append(dict(case=name, xs=xs, ys=ys, bound=b_ir,
                            tokens=len(toks), recs=len(recs),
                            env={k: str(v) for k, v in env.items()},
                            expected=want, got=got, end=res['end'],
                            pre_ok=pre_ok, pre_bytes=pre_bytes,
                            zero=list(zero), note=note, ok=good))
        print('%-11s recs=%2d tok=%2d X=%-7s Y=%-7s B=%d zero=%-6s '
              'pre_ok=%s print=%-20r want=%-20r end=%s %s' % (
                  name, len(recs), len(toks), env['X'], env['Y'], b_ir,
                  list(zero), pre_ok, got, want, res['end'], 'OK' if good else 'FAIL'),
              flush=True)
        disks = case_dir / 'disks'
        if disks.exists():
            shutil.rmtree(disks)

    (WORK / 'results.json').write_text(json.dumps(results, indent=2))
    ok = bool(results) and all(r['ok'] for r in results)
    print('VERDICT:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
