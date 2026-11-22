#!/usr/bin/env python3
"""Combined contour codegen: wide GOST output + chained BESM inserts, ONE install.

Layout (all RAM derived from BASE = 0o1757, zone N=0o2350):

  body[9..14]   wide GOST chain: build words A/B/C/D (codegen_wide, intact)
  body[15]      *64 2004        : FIRST print, the unmodified wide value (intact)
  body[16]      structured UJ   : ENTRY into high RAM (replaces the wide RET)
  body[17]      uj 0(15)        : fall-through guard if body[16] is zeroed
  body[0o25/26] *64 descriptor pair (unchanged)
  body[0o27..32] zero-seeded GOST words A/B/C/D + EOF
  body[0o34/35] BESM data weights: +1<<32 / +2<<32 for GOST C byte 1 (Y thousands)
  body[0o33]    Y accumulator-read cell (init 0, filled by 777007)
  body[0o40..43] wide packed digit weights wD/wA/wB/wC
  zone3[0..]    raw BESM insert words in SEQ order, then *64 print, then uj

The wide output chain therefore stays byte-identical in body[9..15]; only its
final return is replaced by the entry jump, and the return is preserved both at
the end of the high-RAM routine and in the body[17] fall-through guard.

The inserted chain reloads GOST C, adds a packed +1 thousands weight, stores it,
builds a +2 thousands weight in AU (card 2 = V = BESM(...)), captures that AU in
the Y cell via 777007, adds it back to GOST C, stores, prints the MODIFIED wide
value a second time, and returns.  A/B therefore compares the second print.
"""
import os
import sys
from pathlib import Path

W = Path(__file__).resolve().parent
sys.path.insert(0, str(W))
import codegen as cg
import codegen_wide as cw
import codegen_multi as cm
import besm_codegen_base as cb

MASK = (1 << 48) - 1
XTA, ARX, STO = cg.XTA, cg.ARX, cg.STO
OBJ12, RET = cg.OBJ12, cg.RET
ram = cg.ram
BASE = cg.BASE
H = cm.H                         # 0o30114 : zone N+3 word 0
SLOT_ENTRY = 16                  # body[16] -> RAM 0o1777
SLOT_GUARD = 17                  # body[17] -> RAM 0o2000 (free cell)
A_B1 = cb.A_B1                   # 0o2013 : +1 thousands weight (body 0o34)
A_B2 = cb.A_B2                   # 0o2014 : +2 thousands weight (body 0o35)
A_YCELL = ram(0o33)              # 0o2012 : accumulator-read cell for Y


def emit(call_text, env, bound, obj, zero_body=(), zero_zone=()):
    """Return (body_overrides, zone3_dict, meta) for one combined IR stream."""
    # 1. Wide chain and data from the proven 84 codegen (body 9..16 + GOST/weights).
    body, wmeta = cw.emit(env, bound, obj)
    final_base = wmeta['expected']              # first (unmodified) print

    # 4. High-RAM chain from the real 777006/777007 records, in SEQ order.
    besms = cb.besm_records(call_text)
    accs = cm.acc_records(call_text)
    if not besms:
        # Baseline with no BESM cards: body[16] stays the proven wide RET, no
        # high-RAM install, exactly one print from body[15].
        zone = {}
        meta = dict(x=str(env['X']), y=str(env['Y']), bound=bound,
                    base_print=final_base, events=[], n_events=0, H=H,
                    entry_word=body[16], guard_word=None,
                    n_777006=0, n_777007=0, zero_slots=dict(wmeta['zero_slots']),
                    gost_A=wmeta['gost_A'], gost_B=wmeta['gost_B'],
                    gost_C=wmeta['gost_C'], gost_D=wmeta['gost_D'],
                    wA=wmeta['wA'], wB=wmeta['wB'], wC=wmeta['wC'],
                    wD=wmeta['wD'], x_digits=wmeta['x_digits'],
                    y_digits=wmeta['y_digits'])
        return body, zone, meta

    # 2. Entry jump at body[16]; guard RET at body[17].
    body[SLOT_ENTRY] = (cm.jump(H) << 24) & MASK
    body[SLOT_GUARD] = RET & MASK
    # 3. BESM data cells.  Byte 1 of GOST C is Y_i0 (thousands, shift 8*(5-1)=32).
    body[0o34] = (1 << 32) & MASK
    body[0o35] = (2 << 32) & MASK
    body[0o33] = 0

    events = []
    for r in besms:
        events.append((r['seq'], 'besm', r))
    for r in accs:
        events.append((r['seq'], 'acc', r))
    events.sort(key=lambda e: e[0])
    if len(besms) < 2:
        raise ValueError('combined contour needs >=2 BESM cards')
    if not any(r['varindex'] == 2 for r in accs):
        raise ValueError('combined contour needs a Y = BESM(...) card (777007 vi=2)')

    zone = {}
    placed = []
    for k, (seq, kind, r) in enumerate(events):
        if kind == 'besm':
            word = r['word'] & MASK
            detail = cb.decode_raw(word)
        else:
            word = cm.acc_word(r['varindex']) & MASK
            detail = 'sto %04o / sto %04o (%s)' % (r['cell'], r['cell'], r['name'])
        zone[k] = word
        placed.append(dict(slot=k, ram=H + k, seq=seq, kind=kind,
                           word=word, detail=detail))
    n = len(events)
    zone[n] = OBJ12 & MASK
    zone[n + 1] = RET & MASK
    placed.append(dict(slot=n, ram=H + n, seq='print', kind='print',
                       word=OBJ12, detail='*64 2004 (second, modified print)'))
    placed.append(dict(slot=n + 1, ram=H + n + 1, seq='ret', kind='ret',
                       word=RET, detail='uj 0(15)'))

    # 5. A/B zero controls.
    for k in zero_body:
        body[k] = 0
    for k in zero_zone:
        if k in zone:
            zone[k] = 0
            for p in placed:
                if p['slot'] == k:
                    p['word'] = 0
                    p['detail'] += ' [ZEROED]'

    meta = dict(
        x=str(env['X']), y=str(env['Y']), bound=bound,
        n_digits=wmeta['n_digits'], x_digits=wmeta['x_digits'],
        y_digits=wmeta['y_digits'],
        gost_A=wmeta['gost_A'], gost_B=wmeta['gost_B'],
        gost_C=wmeta['gost_C'], gost_D=wmeta['gost_D'],
        wA=wmeta['wA'], wB=wmeta['wB'], wC=wmeta['wC'], wD=wmeta['wD'],
        base_print=final_base,
        events=placed, n_events=n, H=H,
        entry_ram=ram(SLOT_ENTRY), entry_word=body[SLOT_ENTRY],
        guard_ram=ram(SLOT_GUARD), guard_word=body[SLOT_GUARD],
        n_777006=len(besms), n_777007=len(accs),
        zero_slots=dict(wmeta['zero_slots']),
        ycell=A_YCELL, b1=A_B1, b2=A_B2,
    )
    return body, zone, meta
