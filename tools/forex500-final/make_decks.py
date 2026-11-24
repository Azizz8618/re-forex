#!/usr/bin/env python3
"""Generate the FINAL system-test decks: REAL fixed-form Fortran source only.
No 777005 IR card, no fixture, no host-computed result."""
from pathlib import Path
import hashlib

WS = Path(__file__).resolve().parent.parent
D = WS / 'decks'
D.mkdir(exist_ok=True)

HEAD = """ШИФР 410300 ЗС5^
ДИС 41(2048)^
ОЗУ 32^АЦП 32^
ЕЕВ1А3
*NAME FRX5XX
*TRANS:FRX5*,,412350
"""

TAIL = """*EXECUTE
*END FILE
``````
ЕКОНЕЦ
"""

# case -> list of Fortran source cards (columns 1..72, label in 1..5)
CASES = {
    'T1_lit_A':      ['      PROGRAM MAIN', '      X=12.34', '      PRINT 100,X', '  100 FORMAT(1X,F4.2)', '      END'],
    'T1_lit_B':      ['      PROGRAM MAIN', '      X=56.78', '      PRINT 100,X', '  100 FORMAT(1X,F4.2)', '      END'],
    'T2_expr_A':     ['      PROGRAM MAIN', '      X=1.5+2.5*4.0', '      PRINT 100,X', '  100 FORMAT(1X,F4.2)', '      END'],
    'T2_expr_B':     ['      PROGRAM MAIN', '      X=1.5+2.5*2.0', '      PRINT 100,X', '  100 FORMAT(1X,F4.2)', '      END'],
    'T2_parens':     ['      PROGRAM MAIN', '      X=(1.5+2.5)*4.0', '      PRINT 100,X', '  100 FORMAT(1X,F4.2)', '      END'],
    'T3_w4':         ['      PROGRAM MAIN', '      X=34.50', '      PRINT 100,X', '  100 FORMAT(1X,F4.2)', '      END'],
    'T3_w2':         ['      PROGRAM MAIN', '      X=34.50', '      PRINT 100,X', '  100 FORMAT(1X,F2.2)', '      END'],
    'T4_sqrt_A':     ['      PROGRAM MAIN', '      Y=SQRT(16.0)', '      PRINT 100,Y', '  100 FORMAT(1X,F4.2)', '      END'],
    'T4_sqrt_B':     ['      PROGRAM MAIN', '      Y=SQRT(09.0)', '      PRINT 100,Y', '  100 FORMAT(1X,F4.2)', '      END'],
    'T5_do_2':       ['      PROGRAM MAIN', '      S=0.0', '      DO 10 I=1,2', '      S=S+20.00', '   10 CONTINUE',
                      '      PRINT 100,S', '  100 FORMAT(1X,F4.2)', '      END'],
    'T5_do_3':       ['      PROGRAM MAIN', '      S=0.0', '      DO 10 I=1,3', '      S=S+20.00', '   10 CONTINUE',
                      '      PRINT 100,S', '  100 FORMAT(1X,F4.2)', '      END'],
}

for name, src in CASES.items():
    (D / f'{name}.b6').write_text(HEAD + '\n'.join(src) + '\n' + TAIL, encoding='utf-8')

# Negative control: same payload, wrong TRANS marker -> program must be absent.
neg = HEAD.replace('*TRANS:FRX5*,,412350', '*TRANS:OURMRK*') + '\n'.join(CASES['T2_expr_A']) + '\n' + TAIL
(D / 'T6_negative.b6').write_text(neg, encoding='utf-8')

for p in sorted(D.glob('T*.b6')):
    print(hashlib.sha256(p.read_bytes()).hexdigest(), p.name)
