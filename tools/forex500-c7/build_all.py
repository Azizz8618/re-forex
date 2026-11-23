#!/usr/bin/env python3
"""C7 reproducible builder: images + decks (no SIMH invoked here).

Run from the workspace root:
  python3 build/build_all.py

Inputs (vendored copies, no repo/live-disk edits):
  images/2048_base          = repo-generated base a98e8109... then FRX5-renamed 2f5fcf87...
  build/{final_build,final_sign,c2_build,c6_build,build_e2e}.py  verbatim proven helpers
Outputs:
  images/2048_C7_{A,PATCH,RESTORE}
  decks/deck_c7_{A,B}.b6
"""
import hashlib
import subprocess
import sys
from pathlib import Path

WS = Path(__file__).resolve().parent.parent


def run(*args):
    print('+', ' '.join(str(a) for a in args), flush=True)
    r = subprocess.run([sys.executable, *[str(a) for a in args]], cwd=WS)
    if r.returncode:
        raise SystemExit(r.returncode)


def sha(p):
    return hashlib.sha256((WS / p).read_bytes()).hexdigest()


def main():
    # prerequisites: FRX5-renamed base image (byte-neutral catalog rename, docs/108)
    base = WS / 'images/2048_base'
    assert hashlib.sha256(base.read_bytes()).hexdigest() == (
        '2f5fcf873d43c2846ee1669669e26202f32fa25e6b71e109fd20ef4452142ff5'), \
        'images/2048_base must be the FRX5-renamed base (2f5fcf87...)'
    run('build/make_decks_c7.py')
    run('build/c7_build.py', '--build', 'C7_A')
    run('build/c7_build.py', '--build', 'C7_PATCH', '--patch-value', '9999')
    run('build/c7_build.py', '--build', 'C7_RESTORE')
    print('\n--- artifact SHAs (SHA-256) ---')
    for p in ('images/2048_base', 'images/2048_C7_A',
              'images/2048_C7_PATCH', 'images/2048_C7_RESTORE',
              'decks/deck_c7_A.b6', 'decks/deck_c7_B.b6',
              'build/c7_build.py'):
        print(sha(p), p)


if __name__ == '__main__':
    main()
