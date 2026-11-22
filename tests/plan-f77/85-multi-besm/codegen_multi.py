#!/usr/bin/env python3
"""Multi-insert codegen: several 777006 words + 777007 accumulator read.

Placement (all addresses derived from the measured BASE=0o1757 and high-RAM
map of test 80, zone N+3 word k -> RAM 0o30114+k):

  body[9..13]  proven ARX/STO digit-building chain (unchanged)
  body[14]     structured jump to high RAM 0o30114 (entry), M15 kept intact
  body[15]     *64 2004 (unchanged; fall-through print if the jump is zeroed)
  body[16]     uj 0(15) (unchanged; fall-through return)
  H+k          k-th IR event word, in increasing SEQ order:
               777006 -> the exact raw 48-bit word
               777007 -> STO <named cell> / STO <named cell>
  H+n          *64 2004 (print inside the high-RAM routine)
  H+n+1        uj 0(15) (return to resident)

Named accumulator-read cells are body slots (BASE+k):
  X -> 0o2011 (body 0o32), Y -> 0o2012 (body 0o33),
  N -> 0o2015 (body 0o36), I -> 0o2016 (body 0o37).
"""
import os
import re
import sys
from pathlib import Path

W = Path(__file__).resolve().parent
sys.path.insert(0, str(W))
import codegen as cg
import besm_codegen_base as cb

MASK = (1 << 48) - 1
XTA, ARX, STO = cg.XTA, cg.ARX, cg.STO
OBJ12, RET = cg.OBJ12, cg.RET
emit48, ram, digit_bytes = cg.emit48, cg.ram, cg.digit_bytes
BASE = cg.BASE                      # 0o1757
H = 0o30114                         # zone N+3 word 0 -> RAM 0o30114 (test 80)
SLOT_ENTRY = 14                     # body[14] -> RAM 0o1775
A_G3 = cb.A_G3                      # 0o2010 : GOST word C (Y digits)
A_B1 = cb.A_B1                      # 0o2013 : +1 weight
A_B2 = cb.A_B2                      # 0o2014 : +2 weight
VARCELL = {1: ram(0o32), 2: ram(0o33), 3: ram(0o36), 4: ram(0o37)}
VARNAME = {1: 'X', 2: 'Y', 3: 'N', 4: 'I'}
RE_ACC = re.compile(r'^\s*777007\s+(\d+)\s+(\d+)\s*$')


def jump(a):
    """Structured 15-bit UJ/VJM, reg 0 (form proved by test 80 baseline)."""
    return (0x0C << 16) | (((a >> 8) & 0x7f) << 8) | (a & 0xff)


def acc_records(call_text):
    """Decode 777007 <seq> <varindex> emitted by rule 39."""
    out = []
    for line in call_text.splitlines():
        m = RE_ACC.match(line)
        if m:
            seq, vi = (int(v) for v in m.groups())
            if vi not in VARCELL:
                raise ValueError('777007 varindex %d out of range' % vi)
            out.append(dict(seq=seq, varindex=vi, cell=VARCELL[vi],
                            name=VARNAME[vi]))
    return out


def acc_word(varindex):
    """Store accumulator into the named body cell (both halfwords STO cell)."""
    cell = VARCELL[varindex]
    return ((STO | cell) << 24) | (STO | cell)


def plan(call_text, env, bound, obj, zero_body=(), zero_zone=()):
    """Return (body_overrides, zone3_dict, meta) for one IR stream.

    body_overrides extends the proven besm_codegen.emit() body; zone3_dict is
    the zone N+3 word-index -> 48-bit map (word k lands at RAM 0o30114+k).
    """
    besms = cb.besm_records(call_text)       # [{seq,kind,hi,lo,word}, ...]
    accs = acc_records(call_text)            # [{seq,varindex,cell,name}, ...]
    events = []
    for r in besms:
        events.append((r['seq'], 'besm', r))
    for r in accs:
        events.append((r['seq'], 'acc', r))
    events.sort(key=lambda e: e[0])

    body, meta = cb.emit(env, bound, obj, zero=(), besm=None)
    # entry jump replaces the spare body[14]; keep body[15]=*64, body[16]=RET
    body[SLOT_ENTRY] = (jump(H) << 24) & MASK
    for k in zero_body:
        body[k] = 0

    zone = {}
    placed = []
    for k, (seq, kind, r) in enumerate(events):
        if kind == 'besm':
            word = r['word'] & MASK
            detail = cb.decode_raw(word)
        else:
            word = acc_word(r['varindex']) & MASK
            detail = 'sto %04o / sto %04o (%s)' % (r['cell'], r['cell'], r['name'])
        zone[k] = word
        placed.append(dict(slot=k, ram=H + k, seq=seq, kind=kind,
                           word=word, detail=detail))
    n = len(events)
    zone[n] = OBJ12 & MASK
    zone[n + 1] = RET & MASK
    placed.append(dict(slot=n, ram=H + n, seq='print', kind='print',
                       word=OBJ12, detail='*64 2004'))
    placed.append(dict(slot=n + 1, ram=H + n + 1, seq='ret', kind='ret',
                       word=RET, detail='uj 0(15)'))
    for k in zero_zone:
        if k in zone:
            zone[k] = 0
            for p in placed:
                if p['slot'] == k:
                    p['word'] = 0
                    p['detail'] += ' [ZEROED]'
    meta.update(dict(events=placed, n_events=n, H=H,
                     entry_ram=ram(SLOT_ENTRY), entry_word=body[SLOT_ENTRY],
                     n_777006=len(besms), n_777007=len(accs),
                     expected=meta['expected']))
    return body, zone, meta


def raw_word_hi_lo(word):
    return (word >> 24) & 0xffffff, word & 0xffffff
