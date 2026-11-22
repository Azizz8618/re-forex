#!/usr/bin/env python3
"""End-to-end A/B for the WIDE GOST contour: real Fortran deck -> FRONT IR ->
wide codegen -> console.  All machine cases run on COPIES of disks 2048/2053/2099
in /dev/shm with HOME/BESM6_PATH redirected.  No repo edits, git writes, live
disks, tmux, processes or dispak C patches.
"""
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

WORK = Path(os.environ.get(
    'RT_WIDE_WORK', tempfile.mkdtemp(prefix='wide84-',
                                     dir=os.environ.get('TMPDIR', '/tmp'))))
SHM = WORK / 'machine'
os.environ['RT_WIDE_WORK'] = str(WORK)
os.environ['RTXY_WORK'] = str(SHM)
os.environ['RT_GRAMMAR_WORK'] = str(WORK)
os.environ.setdefault('TMPDIR', '/dev/shm')
os.environ.setdefault('BESM6_DISK_SHARE', '/usr/local/share/besm6')

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import expr_ir as ex
import codegen_wide as cgen
import front_probe as fp
import runtime_xy as rx

EVID = WORK / 'evidence'
EVID.mkdir(parents=True, exist_ok=True)
SHM.mkdir(parents=True, exist_ok=True)

# name, X source, Y source, bound, zeroed body words, note, expected override
CASES = [
    ('A_wide_pos',  'X=1234.56',  'Y=X*2.0+1.0',  6, (),
     'baseline: 4 integer digits, X=1234.56 Y=2470.12', None),
    ('B_neg',       'X=-1234.56', 'Y=X+2.0',      6, (),
     'negative X and Y, sign bytes must print', None),
    ('C_lit_change','X=1234.56',  'Y=X*3.0+1.0',  6, (),
     'change literal 2.0 -> 3.0 in Y source', None),
    ('D_zero_wB',   'X=1234.56',  'Y=X*2.0+1.0',  6, (0o42,),
     'zero data word wB (body 0o42) -> X fraction/high digits break',
     '21 1200.00 2470.12'),
    ('E_zero_wD',   'X=1234.56',  'Y=X*2.0+1.0',  6, (0o40,),
     'zero data word wD (body 0o40) -> Y fraction breaks',
     '21 1234.56 2470.00'),
    ('F_zero_code11','X=1234.56', 'Y=X*2.0+1.0',  6, (11,),
     'zero code word body[11] -> word B never stored',
     '21 1200.00 2470.12'),
    ('G_restore',   'X=1234.56',  'Y=X*2.0+1.0',  6, (),
     'restore wB / code[11]: identical to baseline', None),
    ('M_wide_mtr',  'X=1234.56',  'Y=X*2.0+1.0',  6, (),
     'MTR trace of raw ARX chain', None),
    ('N_wide_core', 'X=1234.56',  'Y=X*2.0+1.0',  6, (),
     'CORE dump at PC 1770 to prove installed words', None),
    ('L_maxval',   'X=9999.99',  'Y=X-1.0',      6, (),
     'full 4-digit capacity at the 9999.99 ceiling', None),
]

# N N  X...  Y...   (sign may be '-' and digits have leading zeros)
LINE = re.compile(r'^\d\d\s+\S+\s+\S+$')


def norm(s):
    return ' '.join(s.split())


def parse_printed(out):
    for line in out.splitlines():
        if 'TRANS' in line:
            continue
        s = line.strip()
        if LINE.match(s) and '.' in s:
            return norm(s)
    return None


def core_word(path, addr):
    if not path or not Path(path).exists():
        return None
    data = Path(path).read_bytes()
    off = addr * 6
    if off + 6 > len(data):
        return None
    return int.from_bytes(data[off:off + 6], 'big')


def main():
    o412, tail, obj = rx.load_fixtures()
    print('workspace:', WORK)
    print('machine N=%04o XTA=%06o ARX=%06o STO=%06o '
          'G1=%04o G2=%04o G3=%04o G4=%04o WA=%04o WB=%04o WC=%04o WD=%04o' %
          (rx.N, cgen.XTA, cgen.ARX, cgen.STO,
           cgen.A_G1, cgen.A_G2, cgen.A_G3, cgen.A_G4,
           cgen.A_WA, cgen.A_WB, cgen.A_WC, cgen.A_WD))

    results = []
    only = os.environ.get('RT_WIDE_ONLY')
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
                   'DO bound from IR: %d' % b_ir,
                   '777005 records:']
        for r in recs:
            ir_dump.append('  ' + ' '.join('%6d' % v for v in r))
        ir_dump.append('tokens: %s' % (toks,))
        ir_dump.append('env: %s' % {k: str(v) for k, v in env.items()})
        ir_dump.append('X digits: %s' % (meta['x_digits'],))
        ir_dump.append('Y digits: %s' % (meta['y_digits'],))
        ir_dump.append('GOST A=%016o B=%016o C=%016o D=%016o' %
                       (meta['gost_A'], meta['gost_B'], meta['gost_C'], meta['gost_D']))
        ir_dump.append('weights wA=%016o wB=%016o wC=%016o wD=%016o' %
                       (meta['wA'], meta['wB'], meta['wC'], meta['wD']))
        ir_dump.append('expected console: %s' % meta['expected'])
        (EVID / (name + '_ir.txt')).write_text('\n'.join(ir_dump) + '\n')

        # Machine tracing / core controls.
        for k in ('BESM6_DD_DEBUG', 'BESM6_MTR_LO', 'BESM6_MTR_HI',
                  'BESM6_MTR_N', 'BESM6_MTR_SKIP', 'BESM6_CORE_ON_PC',
                  'BESM6_CORE_SKIP'):
            os.environ.pop(k, None)
        if name == 'M_wide_mtr':
            os.environ['BESM6_DD_DEBUG'] = '1'
            os.environ['BESM6_MTR_LO'] = '01770'
            os.environ['BESM6_MTR_HI'] = '01777'
            os.environ['BESM6_MTR_N'] = '120'
            os.environ['BESM6_MTR_SKIP'] = '6'
        if name == 'N_wide_core':
            os.environ['BESM6_DD_DEBUG'] = '1'
            os.environ['BESM6_MTR_N'] = '0'
            os.environ['BESM6_CORE_ON_PC'] = '1770'
            os.environ['BESM6_CORE_SKIP'] = '6'

        res = rx.make_case(name, o412, tail, obj, ov, keep=True,
                           note='%s | %s | %s | zero=%s' % (xs, ys, note, list(zero)))
        for k in ('BESM6_DD_DEBUG', 'BESM6_MTR_LO', 'BESM6_MTR_HI',
                  'BESM6_MTR_N', 'BESM6_MTR_SKIP', 'BESM6_CORE_ON_PC',
                  'BESM6_CORE_SKIP'):
            os.environ.pop(k, None)

        case_dir = SHM / 'cases' / name
        out_text = (case_dir / 'out.txt').read_text(errors='replace')
        got = parse_printed(out_text)
        want = norm(want_override) if want_override else norm(meta['expected'])

        # Pre-run installed-disk evidence: every digit byte must be ZERO.
        pre = rx.dump_body(case_dir, 'pre2')
        pre_bytes = {n: rx.byte_of(pre[adr - cgen.cg.BASE], off)
                     for n, (adr, off) in meta['zero_slots'].items()}
        pre_ok = all(v == 0 for v in pre_bytes.values())

        # CORE evidence for the dedicated case.
        core = {}
        if name == 'N_wide_core':
            cp = case_dir / 'core-pc.bin'
            for label, addr in (('A', cgen.A_G1), ('B', cgen.A_G2),
                                ('C', cgen.A_G3), ('D', cgen.A_G4),
                                ('wA', cgen.A_WA), ('wB', cgen.A_WB),
                                ('wC', cgen.A_WC), ('wD', cgen.A_WD)):
                core[label] = '%016o' % core_word(cp, addr) if core_word(cp, addr) is not None else 'NO_DUMP'
            (EVID / (name + '_core.txt')).write_text(
                'core dump at PC 0o1770:\n' +
                '\n'.join('  %-3s RAM %04o = %s' %
                          (label, {'A': cgen.A_G1, 'B': cgen.A_G2,
                                   'C': cgen.A_G3, 'D': cgen.A_G4,
                                   'wA': cgen.A_WA, 'wB': cgen.A_WB,
                                   'wC': cgen.A_WC, 'wD': cgen.A_WD}[label], v)
                          for label, v in core.items()) + '\n')

        good = (got == want) and res['end'] and pre_ok
        results.append(dict(case=name, xs=xs, ys=ys, bound=b_ir, zero=list(zero),
                            note=note, env={k: str(v) for k, v in env.items()},
                            expected=want, got=got, end=res['end'],
                            pre_ok=pre_ok, pre_bytes=pre_bytes, core=core,
                            ok=good))
        print('%-12s X=%-10s Y=%-10s zero=%-6s pre_ok=%s print=%-26r '
              'want=%-26r end=%s %s' %
              (name, env['X'], env['Y'], list(zero), pre_ok, got, want,
               res['end'], 'OK' if good else 'FAIL'), flush=True)

        # Keep textual evidence; remove bulky disk copies.
        disks = case_dir / 'disks'
        if disks.exists():
            shutil.rmtree(disks)

    (WORK / 'results.json').write_text(json.dumps(results, indent=2))
    ok = bool(results) and all(r['ok'] for r in results)
    print('VERDICT:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
