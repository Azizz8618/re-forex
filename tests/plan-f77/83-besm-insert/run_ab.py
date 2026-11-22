#!/usr/bin/env python3
"""A/B proof: real Fortran deck -> FRONT 777006 -> raw word installed -> executed.

All disk copies live under /dev/shm/re-forex-besm-impl.  Repository files are
read-only; no live disks, tmux, processes or dispak sources are touched.
"""
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

W = Path(__file__).resolve().parent
WS = Path(os.environ.get(
    'BESM_IMPL_WORK', tempfile.mkdtemp(prefix='besm83-',
                                       dir=os.environ.get('TMPDIR', '/tmp'))))
os.environ['BESM_IMPL_WORK'] = str(WS)
os.environ.setdefault('TMPDIR', str(WS))
os.environ.setdefault('BESM6_DISK_SHARE', '/usr/local/share/besm6')
os.environ.setdefault('RT_GRAMMAR_WORK', str(WS / 'grammar'))
os.environ['RTXY_WORK'] = str(WS / 'machine')
EVID = WS / 'evidence'
EVID.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(W))
import front_besm as fb
import expr_ir as ex
import besm_codegen as cgen

REPO = W.parent.parent.parent
sys.path.insert(0, str(REPO / 'tests/plan-f77/76-runtime-xy'))
import runtime_xy as rx

MASK = (1 << 48) - 1
LINE = re.compile(r'^\s*(\d\d\s+[- ]\d\d\.\d\d\s+[- ]\d\d\.\d\d)\s*$')


def raw_word(addend_adr):
    """ARX <addend cell> / STO <G3>: raw 48-bit instruction word from 777006."""
    return cgen.emit48(cgen.ARX, addend_adr, cgen.STO, cgen.A_G3) & MASK


def norm(s):
    return ' '.join(s.split())


def printed(text):
    for line in text.splitlines():
        if 'TRANS' in line:
            continue
        m = LINE.match(line)
        if m:
            return norm(m.group(1))
    return None


def main():
    o412, tail, obj = rx.load_fixtures()
    words = {
        'p1': raw_word(cgen.A_B1),
        'p2': raw_word(cgen.A_B2),
    }
    print('raw words (hi,lo) for source BESM(hi,lo):')
    for k, w in words.items():
        print('  %s: %d,%d  RAM %04o = %016o  %s' % (
            k, w >> 24, w & 0xffffff, cgen.ram(cgen.SLOT_BESM), w,
            cgen.decode_raw(w)))
    print('N=%04o  B1=%04o B2=%04o G3=%04o' %
          (rx.N, cgen.A_B1, cgen.A_B2, cgen.A_G3))

    # name, X src, Y src, bound, BESM source key or None, zero slots, want, MTR,
    # placement of the BESM card in the real deck
    cases = [
        ('A_baseline', 'X=1.0', 'Y=X+2.0', 6, None, (), '21 01.00 03.00',
         False, 'after_end'),
        ('B_besm_p1', 'X=1.0', 'Y=X+2.0', 6, 'p1', (), '21 01.00 04.00',
         False, 'after_end'),
        ('C_besm_p2', 'X=1.0', 'Y=X+2.0', 6, 'p2', (), '21 01.00 05.00',
         False, 'after_end'),
        ('D_zero_word', 'X=1.0', 'Y=X+2.0', 6, 'p1', (cgen.SLOT_BESM,),
         '21 01.00 03.00', False, 'after_end'),
        ('E_mtr', 'X=1.0', 'Y=X+2.0', 6, 'p1', (), '21 01.00 04.00',
         True, 'after_end'),
        ('F_inline', 'X=1.0', 'Y=X+2.0', 6, 'p1', (), '21 01.00 04.00',
         False, 'inline'),
    ]
    results = []
    for name, xs, ys, bound, key, zero, want, mtr, placement in cases:
        besm = words[key] if key else None
        d, call, build, ir, _raw_recs, errs = fb.front(
            name, besm >> 24 if besm else None,
            besm & 0xffffff if besm else None, with_besm=besm is not None,
            placement=placement)
        recs6 = cgen.besm_records(call)
        if errs:
            raise SystemExit('FAIL %s FRONT ERR=%d' % (name, errs))
        toks, counts = ex.tokens(ex.records(call), ir)
        env = ex.evaluate(toks)
        b_ir = ex.bound_from_ir(ir)
        if b_ir != bound:
            raise SystemExit('FAIL bound %d != %d' % (b_ir, bound))
        if key:
            if len(recs6) != 1 or recs6[0]['word'] != besm:
                raise SystemExit('FAIL %s 777006 record %r' % (name, recs6))
        elif recs6:
            raise SystemExit('FAIL baseline has 777006 record')
        ov, meta = cgen.emit(env, b_ir, obj, zero=zero, besm=besm)

        if mtr:
            for k in ('BESM6_DD_DEBUG', 'BESM6_MTR_LO', 'BESM6_MTR_HI',
                      'BESM6_MTR_N', 'BESM6_MTR_SKIP'):
                os.environ[k] = {'BESM6_DD_DEBUG': '1', 'BESM6_MTR_LO': '01770',
                                 'BESM6_MTR_HI': '01777', 'BESM6_MTR_N': '100',
                                 'BESM6_MTR_SKIP': '6'}[k]
        res = rx.make_case(name, o412, tail, obj, ov, keep=True,
                           note='%s;%s;%s;BESM=%s;zero=%s' %
                                (xs, ys, key, str(besm), list(zero)))
        if mtr:
            for k in ('BESM6_DD_DEBUG', 'BESM6_MTR_LO', 'BESM6_MTR_HI',
                      'BESM6_MTR_N', 'BESM6_MTR_SKIP'):
                os.environ.pop(k, None)
        case_dir = WS / 'machine' / 'cases' / name
        out = (case_dir / 'out.txt').read_text(errors='replace')
        # Installed-word evidence: read the body copy straight off the disk.
        pre = rx.dump_body(case_dir, 'pre2')
        installed = pre[cgen.SLOT_BESM] & MASK
        want_word = 0 if cgen.SLOT_BESM in zero else (besm if besm is not None
                     else cgen.emit48(cgen.XTA, cgen.A_G1, cgen.XTA, cgen.A_G1))
        word_ok = installed == want_word
        mtr_lines = [ln for ln in out.splitlines() if 'MTR 01775' in ln]
        got = printed(out)
        ok = got == norm(want) and res['end'] and word_ok
        if mtr:
            hit_l = [ln for ln in mtr_lines if 'arx' in ln and '2013' in ln]
            hit_r = [ln for ln in mtr_lines if 'atx' in ln and '2010' in ln]
            ok = ok and bool(hit_l) and bool(hit_r)
            mtr_lines = hit_l[:1] + hit_r[:1]
        (EVID / (name + '_ir.txt')).write_text(
            'case=%s %s %s placement=%s\n' % (name, xs, ys, placement) +
            '777006 records: %r\n' % recs6 +
            'decoded tokens: %r\n' % toks +
            'env: %s\n' % {k: str(v) for k, v in env.items()} +
            'DO bound from IR: %d\n' % b_ir +
            'expected print: %s\n' % meta['expected'] +
            'slot14 RAM %04o raw word=%016o (%s)\n' %
            (cgen.ram(cgen.SLOT_BESM), want_word, cgen.decode_raw(want_word)))
        (EVID / (name + '_console.txt')).write_text(out)
        results.append(dict(case=name, besm=key, placement=placement, zero=list(zero),
                            installed_word=installed, want_word=want_word,
                            word_ok=word_ok, got=got, want=norm(want),
                            end=res['end'], mtr_lines=mtr_lines[:2], ok=ok))
        print('%-12s BESM=%-4s zero=%-4s RAM01775=%016s word_ok=%s '
              'print=%-14r want=%-14r end=%s mtr=%s %s' % (
                  name, str(key), list(zero), format(installed, '016o'),
                  word_ok, got, norm(want), res['end'], len(mtr_lines),
                  'OK' if ok else 'FAIL'), flush=True)
        disks = case_dir / 'disks'
        if disks.exists():
            shutil.rmtree(disks)

    (WS / 'results.json').write_text(json.dumps(results, indent=2))
    ok = bool(results) and all(r['ok'] for r in results)
    print('VERDICT:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
