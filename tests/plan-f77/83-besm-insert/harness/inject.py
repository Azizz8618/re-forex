#!/usr/bin/env python3
"""Host injection for FRONT.FTN, following src/f77prep/prep_tools.py:385-410.

Reads FRONT.FTN (with C@@DECL@@ / C@@DATA@@ markers) and builds a standalone
FOREX 2.02 program plus build.deck / call.deck.  Two source variants:

  canonical : the 11 physical source cards from f77_30_base77_deck_forex.txt
  spec10    : the same deck with the loop-body card "N=N+I" removed, which is
              the 10-line source implied by docs/63 section 3.1's IR listing.
"""
import argparse
import hashlib
import os
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
WS = Path(os.environ.get(
    'FRONT1_WORK', tempfile.mkdtemp(prefix='front1-',
                                    dir=os.environ.get('TMPDIR', '/tmp'))))
DECK = Path(os.environ.get(
    'FRONT1_DECK', ROOT / 'docs/plan-f77-full/logs/f77_30_base77_deck_forex.txt'))
FTN = Path(os.environ.get(
    'FRONT1_SRC', str(Path(__file__).resolve().parent.parent / 'FRONT.FTN')))
LW, LL = 72, 132


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def data_statement(name, values, per_line=12):
    chunks = [values[i:i + per_line] for i in range(0, len(values), per_line)]
    out = []
    for i, chunk in enumerate(chunks):
        head = '      DATA %s /' % name if i == 0 else '     1'
        tail = '/' if i == len(chunks) - 1 else ','
        out.append(head + ','.join(str(v) for v in chunk) + tail)
    return '\n'.join(out)


def source_cards(mode):
    lines = DECK.read_text(encoding='utf-8').splitlines()
    i = next(n for n, ln in enumerate(lines) if ln.startswith('*forex'))
    j = next(n for n, ln in enumerate(lines) if n > i and ln.startswith('*execute'))
    cards = [ln.rstrip() for ln in lines[i + 1:j]
             if ln and ln[0] not in 'cC*']
    if mode == 'spec10':
        cards = [ln for ln in cards if ln.strip() != 'N=N+I']
    assert len(cards) in ((10, 11) if mode == 'spec10' else (11, 12)), cards
    return cards


def tag_for(src, mode):
    return mode if src == 'FRONT.FTN' else '%s_%s' % (mode, Path(src).stem)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', choices=('canonical', 'spec10', 'legacy'),
                    default='canonical')
    ap.add_argument('--src', default='FRONT.FTN')
    a = ap.parse_args()

    if a.mode == 'legacy':
        cards = ['      PROGRAM TST', '      S=1', '      PRINT *,S', '      END']
    else:
        cards = source_cards(a.mode)
    nc = len(cards)
    raw = []
    for card in cards:
        c = [ord(ch) & 0x7F for ch in card[:LW]]
        c += [32] * (LW - len(c))
        raw += c

    ftn = FTN.read_text(encoding='utf-8')
    decl = ('      PROGRAM FRONT1\n'
            '      PARAMETER (NC=%d,NLV=%d,LL=%d,LW=%d)\n'
            '      INTEGER RAW(LW,NC)\n'
            '      INTEGER C(LL,NLV)\n'
            '      INTEGER SEQ(NLV)\n' % (nc, nc, LL, LW))
    assert ftn.count('C@@DECL@@') == 1 and ftn.count('C@@DATA@@') == 1
    ftn = ftn.replace('C@@DECL@@', decl.rstrip('\n'))
    ftn = ftn.replace('C@@DATA@@', '      DATA SEQ /%s/\n%s' % (
        ','.join(str(i + 1) for i in range(nc)),
        data_statement('RAW', raw)))

    tag = tag_for(a.src, a.mode)
    out = WS / ('FRONT_%s_injected.FTN' % tag)
    out.write_text(ftn + '\n', encoding='utf-8')
    bad = [(n, len(ln), ln) for n, ln in enumerate(out.read_text().splitlines(), 1)
           if len(ln) > 72 and not ln.startswith('C')]
    if bad:
        raise SystemExit('non-comment line over 72 columns: %r' % bad[:3])

    (WS / ('build_%s.deck' % tag)).write_text(
        'шифр 419999 зс5^\n'
        'лен 41(2048)^\n'
        'лен 60(2048-wr)^\n'
        'ееВ1а3\n'
        '*name FRONBLD\n'
        '*call yesmemory\n'
        '*perso:602300\n'
        '*no list\n'
        '*forex\n'
        + ftn +
        '*to perso:602406\n'
        '*end file\n'
        '``````\n'
        'еконец\n', encoding='utf-8')
    (WS / ('call_%s.deck' % tag)).write_text(
        'шифр 419999 зс5^\n'
        'лен 41(2048)^\n'
        'лен 60(2048)^\n'
        'ееВ1а3\n'
        '*name FRONCAL\n'
        '*call yesmemory\n'
        '*perso:602300\n'
        '*perso:602406,cont\n'
        '*call front1\n'
        '*execute\n'
        '*end file\n'
        '``````\n'
        'еконец\n', encoding='utf-8')

    print('mode=%s ncards=%d raw_values=%d' % (a.mode, nc, len(raw)))
    print('source=%s lines=%d sha256=%s' % (out.name, len(out.read_text().splitlines()), sha(out)))
    for n, card in enumerate(cards, 1):
        print('  card %2d: %r' % (n, card))
    return 0


if __name__ == '__main__':
    sys.exit(main())
