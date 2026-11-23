#!/usr/bin/env python3
"""Compile the injected FRONT.FTN with SYSTEM FOREX 2.02 on COPIES of the disks.

Deck pattern: tests/plan-f77/t412/run-our-trans.sh, with HOME and BESM6_PATH
redirected to this workspace.  Captures build.out / call.out and extracts the
numeric IR records emitted by FRONT1.
"""
import argparse
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

WS = Path(os.environ.get(
    'FRONT1_WORK', tempfile.mkdtemp(prefix='front1-',
                                    dir=os.environ.get('TMPDIR', '/tmp'))))
SHARE = Path(os.environ.get('BESM6_DISK_SHARE', '/usr/local/share/besm6'))
DISPAK_B = Path(os.environ.get('DISPAK_BUILD',
                               '/home/azizz/Yandex.Disk/dispak/build/dispak'))
DISPAK = Path(os.environ.get('DISPAK_BIN', str(DISPAK_B / 'dispak')))


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', default='canonical')
    a = ap.parse_args()

    work = WS / 'work' / a.mode
    work.mkdir(parents=True, exist_ok=True)
    for f in (DISPAK, SHARE / '2048', SHARE / '2053', SHARE / '2099',
              SHARE / '2148', SHARE / '2348'):
        if not Path(f).exists():
            raise SystemExit('FAIL: missing %s' % f)
    for name in ('2048', '2053', '2099', '2148', '2048-wr'):
        src = SHARE / ('2348' if name in ('2048', '2048-wr') else name)
        dst = work / name
        if not dst.exists():
            shutil.copy(src, dst)
    shutil.copy(DISPAK, work / 'dispak')
    (work / 'dispak').chmod(0o755)
    for prefix in ('build', 'call'):
        shutil.copy(WS / ('%s_%s.deck' % (prefix, a.mode)),
                    work / ('%s.deck' % prefix))

    env = dict(os.environ, HOME=str(work / 'home'), BESM6_PATH=str(work))
    (work / 'home').mkdir(exist_ok=True)

    for deck, outname in (('build.deck', 'build.out'), ('call.deck', 'call.out')):
        with open(work / outname, 'wb') as fout:
            subprocess.run([str(work / 'dispak'), '-l', deck], cwd=work, env=env,
                           stdout=fout, stderr=subprocess.STDOUT, timeout=600)

    build = (work / 'build.out').read_text(errors='replace')
    call = (work / 'call.out').read_text(errors='replace')
    (WS / ('build_%s.out' % a.mode)).write_text(build, errors='replace')
    (WS / ('call_%s.out' % a.mode)).write_text(call, errors='replace')

    recs = []
    for line in call.splitlines():
        m = re.match(r'^\s*(77700[1-4])\s+((?:-?\d+\s*)+)$', line)
        if m:
            recs.append(tuple([int(m.group(1))] +
                              [int(x) for x in m.group(2).split()]))
    (WS / ('ir_%s.txt' % a.mode)).write_text(
        ''.join(''.join('%8d' % v for v in r) + '\n' for r in recs))

    def errs(t):
        return len(re.findall(r'\bERR\b|\bОШИБК', t, re.I))

    print('mode=%s' % a.mode)
    print('build_sha256=%s' % sha(work / 'build.out'))
    print('call_sha256=%s' % sha(work / 'call.out'))
    print('build_bytes=%d call_bytes=%d' % (len(build), len(call)))
    print('build_ERR=%d call_ERR=%d' % (errs(build), errs(call)))
    print('build_tail=%r' % build[-300:])
    print('IR_records=%d' % len(recs))
    for r in recs:
        print('  ' + ''.join('%8d' % v for v in r))
    return 0 if (errs(build) == 0 and errs(call) == 0 and recs) else 1


if __name__ == '__main__':
    sys.exit(main())
