#!/usr/bin/env python3
"""Causality proof: change ONLY a 777005 IR record after FRONT, deck unchanged.

If the printed value follows the tampered IR, the codegen is genuinely IR-driven
and does not re-read the Fortran deck text for numeric values.
"""
import os
import re
import sys
from pathlib import Path

WORK = Path(os.environ.get('RT_GRAMMAR_WORK', '/tmp/.private/azizz/opencode/re-forex-grammar'))
os.environ.setdefault('RTXY_WORK', str(WORK / 'machine'))
os.environ.setdefault('TMPDIR', '/tmp/.private/azizz/opencode')
os.environ.setdefault('BESM6_DISK_SHARE', '/usr/local/share/besm6')

import expr_ir as ex
import codegen_general as cgen
import runtime_xy as rx
import run_cases as rc

SRC = WORK / 'front' / 'A_mul_add' / 'work' / 'spec10' / 'call.out'


def main():
    call = SRC.read_text(errors='replace')
    ir = (WORK / 'front' / 'A_mul_add' / 'ir_spec10.txt').read_text()
    recs = ex.records(call)
    # Locate the literal token for the trailing "+1.0" of Y=X*2.0+1.0.
    target = (6, 1, 0, 100, 0)
    if target not in recs:
        raise SystemExit('FAIL expected 777005 record %r not found' % (target,))
    idx = recs.index(target)
    new_recs = list(recs)
    new_recs[idx] = (6, 1, 0, 300, 0)   # +1.0 -> +3.0, IR only
    tampered = '\n'.join('    777005 %6d %6d %6d %6d %6d' % r for r in new_recs) + '\n'
    toks, _ = ex.tokens(new_recs, ir)
    env = ex.evaluate(toks)
    bound = ex.bound_from_ir(ir)
    ov, meta = cgen.emit(env, bound, rx.load_fixtures()[2])
    print('deck unchanged: X=2.0 ; Y=X*2.0+1.0 (Y=5)')
    print('IR tampered at record %d: 777005 6 1 0 100 0 -> 777005 6 1 0 300 0 (+1.0 -> +3.0)'
          % idx)
    print('IR-evaluated X=%s Y=%s ; expected console: %s' %
          (env['X'], env['Y'], meta['expected']))
    o412, tail, obj = rx.load_fixtures()
    res = rx.make_case('IR_tamper', o412, tail, obj, ov, keep=True,
                       note='deck unchanged, only 777005 record changed')
    out = (WORK / 'machine' / 'cases' / 'IR_tamper' / 'out.txt').read_text(errors='replace')
    got = rc.parse_printed(out)
    want = rc.norm(meta['expected'])
    print('printed=%r want=%r end=%s' % (got, want, res['end']))
    good = (got == want and res['end'])
    print('VERDICT:', 'PASS' if good else 'FAIL')
    return 0 if good else 1


if __name__ == '__main__':
    sys.exit(main())
