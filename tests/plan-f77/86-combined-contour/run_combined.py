#!/usr/bin/env python3
"""A/B proof: wide GOST output AND chained BESM inserts in ONE contour install.

Every case is compiled by the extended FRONT from a real edited fixed-form
deck containing BOTH wide assignments and (except baseline) BESM cards, then
installed on COPIES of disks 2048/2053/2099 with HOME/BESM6_PATH redirected.
No repo edits, git writes, live disks, tmux, processes or dispak C patches.
"""
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

W = Path(__file__).resolve().parent
os.environ.setdefault('BESM6_DISK_SHARE', '/usr/local/share/besm6')
os.environ.setdefault('RE_FOREX_REPO', str(W.parent.parent.parent))
os.environ.setdefault(
    'COMBINED_WORK', tempfile.mkdtemp(prefix='combined86-',
                                      dir=os.environ.get('TMPDIR', '/tmp')))
WS = Path(os.environ['COMBINED_WORK'])
os.environ['COMBINED_CASES'] = str(WS / 'cases')
EVID = WS / 'evidence'
EVID.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(W))

import front_combined as fc
import expr_ir as ex
import codegen_combined as cc
import runner_combined as rm
import runtime_xy as rx

# Raw BESM cards (fixed form, decimal operands).  hi*2**24 + lo is the word.
C1 = '      BESM(33800,46091)'      # xta 2010 / arx 2013 : C + +1 thousands
C2 = '      Y = BESM(1032,33804)'   # sto 2010 / xta 2014 + 777007(Y cell)
C3 = '      BESM(33800,46090)'      # xta 2010 / arx 2012 : C + Y cell
C4 = '      BESM(1032,1032)'        # sto 2010 / sto 2010 : store final C
C2_CHANGED = '      Y = BESM(1032,33803)'  # xta 2013 -> Y cell = +1 thousands

DECKS = {
    'A': ([], 'X=1234.56', 'Y=X*2.0+1.0'),
    'B': ([C1, C2, C3, C4], 'X=1234.56', 'Y=X*2.0+1.0'),
    'E': ([C1, C2_CHANGED, C3, C4], 'X=1234.56', 'Y=X*2.0+1.0'),
    'N': ([C1, C2, C3, C4], 'X=-1234.56', 'Y=X+2.0'),
}

BASE_POS = '21 1234.56 2470.12'
BASE_NEG = '21 -1234.56 -1232.56'


def run_case(tag, deck_key, o412, tail, obj, *, zero_body=(), zero_zone=(),
             mtr=None, core=True, note=''):
    cards, xs, ys = DECKS[deck_key]
    d, call, ir, r5, r6, r7, errs = fc.front(tag, xs, ys, cards)
    if errs:
        raise SystemExit('FAIL %s FRONT ERR=%d' % (tag, errs))
    toks, counts = ex.tokens(ex.records(call), ir)
    env = ex.evaluate(toks)
    bound = ex.bound_from_ir(ir)
    if bound != 6:
        raise SystemExit('FAIL %s bound %d' % (tag, bound))
    body, zone, meta = cc.emit(call, env, bound, obj,
                               zero_body=zero_body, zero_zone=zero_zone)
    # Persist IR + placement evidence.
    (EVID / (tag + '_ir.txt')).write_text(
        'case=%s  %s ; %s\n' % (tag, xs, ys) +
        'cards=%r\n' % (list(cards),) +
        '777005 records (wide IR): %r\n777006 records (BESM): %r\n'
        '777007 records (acc read): %r\n' % (r5, r6, r7) +
        'env=%s bound=%d\n' % ({k: str(v) for k, v in env.items()}, bound) +
        'X digits=%s Y digits=%s\n' % (meta['x_digits'], meta['y_digits'],) +
        'GOST A=%016o B=%016o C=%016o D=%016o\n' % (
            meta['gost_A'], meta['gost_B'], meta['gost_C'], meta['gost_D']) +
        'weights wA=%016o wB=%016o wC=%016o wD=%016o\n' % (
            meta['wA'], meta['wB'], meta['wC'], meta['wD']) +
        'first (wide) print: %s\n' % meta['base_print'] +
        '\n'.join('event slot=%d RAM=%06o seq=%s %-5s %016o %s' % (
            p['slot'], p['ram'], p['seq'], p['kind'], p['word'], p['detail'])
            for p in meta['events']) + '\n' +
        'entry body[16] RAM %04o = %016o\n' % (0o1777, meta['entry_word']))
    res = rm.make_case(tag, o412, tail, obj, body, zone,
                       core=core, mtr=mtr, note=note)

    # Pre-run zero-seed readback of every digit byte (all 14 GOST digit positions).
    case_dir = res['dir']
    pre = rx.dump_body(case_dir, 'pre')
    pre_bytes = {}
    for n, (adr, off) in meta['zero_slots'].items():
        pre_bytes[n] = rx.byte_of(pre[adr - 0o1757], off)
    pre_ok = all(v == 0 for v in pre_bytes.values())
    (EVID / (tag + '_pre.txt')).write_text(
        'case=%s pre_ok=%s\n' % (tag, pre_ok) +
        '\n'.join('  %-5s RAM %04o byte %d = %d' % (n, adr, off, pre_bytes[n])
                  for n, (adr, off) in meta['zero_slots'].items()) + '\n')
    return res, meta, r5, r6, r7, pre_ok


def main():
    o412, tail, obj = rx.load_fixtures()
    print('workspace:', WS)
    print('N=%04o BASE=01757 H=%06o' % (rm.N, cc.H))

    # name, deck, zero_body, zero_zone, mtr, expected printed lines, note
    cases = [
        ('A_baseline', 'A', (), (), None, [BASE_POS],
         'wide output only, no BESM cards, no entry jump'),
        ('B_with_inserts', 'B', (), (), None,
         [BASE_POS, '21 1234.56 5470.12'],
         'wide + 4 BESM cards incl. Y = BESM; second print modified +3000'),
        ('C_operand_change', 'E', (), (), None,
         [BASE_POS, '21 1234.56 4470.12'],
         '2nd insert operand 33804->33803 (xta 2014->xta 2013) -> Y cell +1 not +2 -> +2000'),
        ('D_zero_accstore', 'B', (), (2,), None,
         [BASE_POS, '21 1234.56 3470.12'],
         '777007 accumulator-store word zeroed -> Y cell stays 0'),
        ('E_zero_insert4', 'B', (), (4,), None,
         [BASE_POS, '21 1234.56 3470.12'],
         'final GOST-C store word zeroed -> C keeps only +1 thousands'),
        ('F_zero_entry', 'B', (16,), (), None,
         [BASE_POS],
         'entry jump zeroed -> body[17] guard returns, no BESM, one print'),
        ('G_negative', 'N', (), (), None,
         [BASE_NEG, '21 -1234.56 -4232.56'],
         'negative wide value with inserts: sign byte + digits both correct'),
        ('H_mtr', 'B', (), (), ('30110', '30132', '120', 0),
         [BASE_POS, '21 1234.56 5470.12'],
         'MTR proof: PCs 30114..30122 reached'),
        ('N_core', 'B', (), (), None,
         [BASE_POS, '21 1234.56 5470.12'],
         'CORE dump at PC 1770 proves body + high-RAM words installed'),
    ]

    results = []
    only = os.environ.get('COMBINED_ONLY')
    for name, deck, zb, zz, mtr, want, note in cases:
        if only and name not in only.split(','):
            continue
        res, meta, r5, r6, r7, pre_ok = run_case(
            name, deck, o412, tail, obj, zero_body=zb, zero_zone=zz,
            mtr=mtr, note=note)
        got = res['printed']
        end = res['end']
        core_ok = (res['core_mismatch'] == [])
        # Exact ordered match for non-MTR cases; subsequence for MTR (flooding).
        if mtr:
            it = iter(got)
            value_ok = all(any(x == w for x in it) for w in want)
            pcs = sorted({ln[4:9] for ln in res['mtr_lines']})
            needed = {'30114', '30115', '30116', '30117', '30120', '30121', '30122'}
            mtr_ok = needed.issubset(set(pcs))
        else:
            value_ok = (got == want)
            pcs = []
            mtr_ok = True
        ok = value_ok and end and pre_ok and core_ok and mtr_ok
        results.append(dict(case=name, deck=deck, zero_body=list(zb),
                            zero_zone=list(zz), got=got, want=want,
                            end=end, pre_ok=pre_ok,
                            core_mismatch=res['core_mismatch'],
                            core_ok=core_ok, mtr_pcs=pcs, mtr_ok=mtr_ok,
                            value_ok=value_ok, ok=ok, note=note,
                            n_777006=len(r6), n_777007=len(r7)))
        print('%-17s prints=%-55r end=%-5s pre=%-5s core=%-5s mtr=%s %s' % (
            name, got, end, pre_ok, core_ok,
            ','.join(pcs) if pcs else '-', 'OK' if ok else 'FAIL'), flush=True)
        # Keep textual evidence; remove bulky disk copies.
        disks = res['dir'] / 'disks'
        if disks.exists():
            shutil.rmtree(disks)

    (WS / 'results.json').write_text(json.dumps(results, indent=2))
    ok = bool(results) and all(r['ok'] for r in results)
    print('VERDICT:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
