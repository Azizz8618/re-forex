#!/usr/bin/env python3
"""A/B proof: multi BESM(...) inserts + Fortran-style accumulator read, real Fortran decks.

Every case is compiled by the extended FRONT (copy-only patch) from a real
edited fixed-form deck, then installed on COPIES of disks 2048/2053/2099 with
HOME/BESM6_PATH redirected.  No repo/git/live-disk/tmux/dispak-source writes.
"""
import json
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

W = Path(__file__).resolve().parent
os.environ.setdefault('BESM6_DISK_SHARE', '/usr/local/share/besm6')
os.environ.setdefault('BESM_MULTI_WORK', tempfile.mkdtemp(prefix='besm85-', dir=os.environ.get('TMPDIR', '/tmp')))
WS = Path(os.environ['BESM_MULTI_WORK'])
EVID = WS / 'evidence'
EVID.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(W))
sys.path.insert(0, str(W.parent / '76-runtime-xy'))

import front_multi as fm
import expr_ir as ex
import codegen_multi as cm
import runner_multi as rm

# Raw words carried by source BESM(hi,lo) cards (decimals, no B suffix).
INS1 = (46091, 1032)          # ARX 0o2013 / STO 0o2010   (+1 weight -> G3)
INS2 = (33804, 46091)         # XTA 0o2014 / ARX 0o2013   (build +2+1 in AU)
INS2_CHANGED = (33804, 46092) # XTA 0o2014 / ARX 0o2014   (build +2+2 in AU)
INS3A = (33800, 46090)        # XTA 0o2010 / ARX 0o2012   (G3 + Ycell -> AU)
INS3B = (1032, 1032)          # STO 0o2010 / STO 0o2010   (store G3 back)
ACC_CARD = '      Y = BESM(33804,46091)'  # rule 39: 2nd insert + store ACC in Y
ACC_CHANGED = '      Y = BESM(33804,46092)'  # 2nd insert operand changed

def card(pair):
    return '      BESM(%d,%d)' % pair

DECKS = {
    'A': [],
    'B': [card(INS1)],
    'C': [card(INS1), ACC_CARD, card(INS3A), card(INS3B)],
    'E': [card(INS1), ACC_CHANGED, card(INS3A), card(INS3B)],
}

LINE = re.compile(r'^\s*(\d\d\s+[- ]\d\d\.\d\d\s+[- ]\d\d\.\d\d)\s*$')


def want_print(y_units):
    return '21 01.00 %02d.00' % y_units


def run_case(tag, deck_key, o412, tail, obj, *, zero_body=(), zero_zone=(),
             mtr=None, note=''):
    d, call, build, ir, r6, r7, errs = fm.front(
        tag, DECKS[deck_key])
    if errs:
        raise SystemExit('FAIL %s FRONT ERR=%d' % (tag, errs))
    toks, counts = ex.tokens(ex.records(call), ir)
    env = ex.evaluate(toks)
    bound = ex.bound_from_ir(ir)
    if bound != 6:
        raise SystemExit('FAIL %s bound %d' % (tag, bound))
    body, zone, meta = cm.plan(call, env, bound, obj,
                               zero_body=zero_body, zero_zone=zero_zone)
    # Persist IR evidence for this deck.
    (EVID / (tag + '_ir.txt')).write_text(
        'case=%s deck=%s extra_cards=%r\n' % (tag, deck_key, DECKS[deck_key]) +
        '777006 records: %r\n777007 records: %r\n' % (r6, r7) +
        'env=%s bound=%d\n' % ({k: str(v) for k, v in env.items()}, bound) +
        'expected print: %s\n' % meta['expected'] +
        '\n'.join('event slot=%d RAM=%06o seq=%s %-5s %016o %s' % (
            p['slot'], p['ram'], p['seq'], p['kind'], p['word'], p['detail'])
            for p in meta['events']) + '\n' +
        'body[14] RAM %04o = %016o\n' % (meta['entry_ram'], meta['entry_word']))
    res = rm.make_case(tag, o412, tail, obj, body, zone,
                       core=True, mtr=mtr, note=note)
    return res, meta, r6, r7


def main():
    o412, tail, obj = rx_fixtures()
    print('workspace:', WS)
    print('N=%04o BASE=%04o H=%06o' % (rm.N, 0o1757, cm.H))

    cases = [
        # name, deck, zero_body, zero_zone, mtr, want, note
        ('A_baseline', 'A', (), (), None, want_print(3), 'no BESM / no accumulator read'),
        ('B_one_insert', 'B', (), (), None, want_print(4), 'one raw insert'),
        ('C_three_inserts', 'C', (), (), None, want_print(7),
         '3 inserts + Fortran assignment store in execution path'),
        ('D_acc_read_off', 'C', (), (2,), None, want_print(4),
         'same deck as C but 777007 word zeroed -> Ycell stays 0'),
        ('E_operand_change', 'E', (), (), None, want_print(8),
         '2nd insert operand 0o2013->0o2014 -> digit 07->08'),
        ('F_zero_insert1', 'C', (), (0,), None, want_print(6),
         '1st insert word zeroed -> base G3, later +3 -> 06.00'),
        ('F2_zero_insert3b', 'C', (), (4,), None, want_print(4),
         'final store word zeroed -> G3 never updated -> 04.00'),
        ('G_zero_entry', 'C', (cm.SLOT_ENTRY,), (), None, want_print(3),
         'entry jump zeroed -> fall-through print, base value'),
        ('H_mtr', 'C', (), (), ('30110', '30132', '100', 0), want_print(7),
         'MTR proof: PCs 30114..30121 reached'),
    ]
    results = []
    for name, deck, zb, zz, mtr, want, note in cases:
        res, meta, r6, r7 = run_case(
            name, deck, o412, tail, obj, zero_body=zb, zero_zone=zz,
            mtr=mtr, note=note)
        got = res['printed']
        end = res['end']
        core_ok = (res['core_mismatch'] == [])
        ok = (got == want) and end and core_ok
        if mtr:
            pcs = sorted({ln[4:9] for ln in res['mtr_lines']})
            needed = {'30114', '30115', '30116', '30117', '30120', '30121'}
            mtr_ok = needed.issubset(set(pcs))
            ok = ok and mtr_ok
        else:
            pcs = []
        results.append(dict(case=name, deck=deck, zero_body=list(zb),
                            zero_zone=list(zz), got=got, want=want,
                            end=end, core_mismatch=res['core_mismatch'],
                            core_ok=core_ok, mtr_pcs=pcs, ok=ok, note=note))
        print('%-17s print=%-14r want=%-14r end=%-5s core=%-5s mtr=%s %s' % (
            name, got, want, end, core_ok,
            ','.join(pcs) if pcs else '-', 'OK' if ok else 'FAIL'),
            flush=True)

    (WS / 'results.json').write_text(json.dumps(results, indent=2))
    ok = bool(results) and all(r['ok'] for r in results)
    print('VERDICT:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


def rx_fixtures():
    import runtime_xy as rx
    return rx.load_fixtures()


if __name__ == '__main__':
    sys.exit(main())
