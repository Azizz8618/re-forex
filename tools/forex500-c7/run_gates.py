#!/usr/bin/env python3
"""Run the four decisive SIMH gates for C7 on the isolated tmux socket.

Usage: python3 build/run_gates.py
Copies only; no repo/live-disk/tmux-0/C changes.  Each gate gets its own ini
and workspace-local prn capture; stock -n prn0 semantics are kept.
"""
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
RUNS = WS / 'runs'
TMUXENV = dict(os.environ, TMUX_TMPDIR=str(RUNS / 'tmux'))

GATES = [
    ('C7_A',       'images/2048_C7_A',      'decks/deck_c7_A.b6'),
    ('C7_B',       'images/2048_C7_A',      'decks/deck_c7_B.b6'),
    ('C7_PATCH',   'images/2048_C7_PATCH',  'decks/deck_c7_A.b6'),
    ('C7_RESTORE', 'images/2048_C7_RESTORE','decks/deck_c7_A.b6'),
]
EXPECT_A = ['-0012.34', '-0056.78', '-0003.75', '-0000.40', '-0034.50', '-0040.00']
EXPECT_B = ['-0056.78', '-0056.78', '-0004.00', '-0000.40', '-0034.50', '-0040.00']
EXPECT_PATCH = ['-0012.34', '-0099.99', '-0003.75', '-0000.40', '-0034.50', '-0040.00']


def tmux(*args, check=True):
    r = subprocess.run(['tmux', *args], env=TMUXENV, text=True, capture_output=True)
    if check and r.returncode:
        raise RuntimeError(f'tmux {args}: {r.stderr.strip()}')
    return r.stdout


def main():
    (RUNS / 'tmux').mkdir(parents=True, exist_ok=True)
    results = []
    for case, image, deck in GATES:
        subprocess.run([sys.executable, 'build/setup_c2.py', case, image],
                       cwd=WS, check=True, stdout=subprocess.DEVNULL)
        tmux('kill-server', check=False)
        p = RUNS / f'localprn_{case}.txt'
        if p.exists():
            p.unlink()
        cmd = [sys.executable, 'build/drive_c2.py', '--case', case,
               '--deck', deck, '--timeout', '180']
        r = subprocess.run(cmd, cwd=WS, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, text=True)
        (RUNS / f'drive_{case}.log').write_text(r.stdout)
        txt = p.read_text(errors='replace') if p.exists() else ''
        vals = [re.search(r'21\s+(-?[\d.]+)', l).group(1)
                for l in txt.splitlines() if re.search(r'21\s+-?[\d.]+', l)]
        done = 'КОНЕЦ ЗАДАЧИ' in txt
        exp = {'C7_A': EXPECT_A, 'C7_B': EXPECT_B,
               'C7_PATCH': EXPECT_PATCH, 'C7_RESTORE': EXPECT_A}[case]
        ok = done and vals == exp
        results.append((case, r.returncode, done, vals, ok))
        print(f'{case}: rc={r.returncode} done={done} vals={vals} '
              f'{"PASS" if ok else "FAIL"}', flush=True)
    print('--- SUMMARY ---')
    print('ALL PASS' if all(x[4] for x in results) else 'SOME FAILED')
    return 0 if all(x[4] for x in results) else 1


if __name__ == '__main__':
    sys.exit(main())
