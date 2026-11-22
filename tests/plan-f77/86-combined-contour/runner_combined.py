#!/usr/bin/env python3
"""Machine runner for the combined contour: zone-2350 body + zone N+3 chain.

Reuses the proven test-84 installer and test-80/85 CORE/MTR technique on COPIES
of disks 2048/2053/2099.  HOME/BESM6_PATH are redirected per case.  No repo
edits, git writes, live disks, tmux sessions, processes or dispak C patches.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

W = Path(__file__).resolve().parent
REPO = Path(os.environ.get('RE_FOREX_REPO', '/home/azizz/Yandex.Disk/re-forex'))
sys.path.insert(0, str(W))
import installer as inst
import runtime_xy as rx

SHARE = Path(os.environ.get('BESM6_DISK_SHARE', '/usr/local/share/besm6'))
DISPAK = Path(os.environ.get('DISPAK_BIN',
                             '/home/azizz/Yandex.Disk/dispak/build/dispak/dispak'))
BESMTOOL = Path(os.environ.get('BESMTOOL',
                               '/home/azizz/Yandex.Disk/dispak/build/besmtool/besmtool'))
WS = Path(os.environ.get(
    'COMBINED_WORK', tempfile.mkdtemp(prefix='combined-p9-',
                                      dir=os.environ.get('TMPDIR', '/tmp'))))
CASES = Path(os.environ.get('COMBINED_CASES', '/dev/shm/re-forex-combined/cases'))
EVID = WS / 'evidence'
CASES.mkdir(parents=True, exist_ok=True)
EVID.mkdir(parents=True, exist_ok=True)
N = rx.N                                  # 0o2350
MASK = rx.MASK
BASE = 0o1757

JOB = """шифр 419999 зс5^
DIS 41(2048)^
eeв1а3
*name OURMRKRT
*TRANS:OURMRK*,,41%04o
       PROGRAM MAIN
       END
*execute
*end file
``````
ЕКОНЕЦ
""" % N

LINE = re.compile(r'^\s*(\d\d\s+\S+\s+\S+)\s*$')


def printed_all(text):
    """All wide output lines from the console, in order."""
    out = []
    for line in text.splitlines():
        if 'TRANS' in line:
            continue
        m = LINE.match(line) if '.' in line else None
        if m:
            out.append(' '.join(m.group(1).split()))
    return out


def core_word(path, addr):
    if not path or not Path(path).exists():
        return None
    data = Path(path).read_bytes()
    off = addr * 6
    if off + 6 > len(data):
        return None
    return int.from_bytes(data[off:off + 6], 'big')


def make_case(name, o412, tail, obj, body_ov, zone3, *, keep=True,
              core=True, mtr=None, timeout=180, note=''):
    """Install body overrides + zone N+3 and run one dispak case."""
    d = CASES / name
    if d.exists():
        shutil.rmtree(d)
    (d / 'disks').mkdir(parents=True)
    (d / 'home').mkdir(parents=True)
    for f in ('2048', '2053', '2099'):
        shutil.copy(SHARE / f, d / 'disks' / f)

    body = [0] * 1024
    body[0:19] = o412[16:35]
    body[19:1024] = tail[0:1005]
    for k, v in body_ov.items():
        body[k] = v & MASK
    cat = o412[0:16] + [0] * 1008
    z2 = [0] * 1024
    for i, w in enumerate(o412[35:410]):
        z2[526 + i] = w
    z3 = [0] * 1024
    for k, v in zone3.items():
        z3[k] = v & MASK
    images = {'cat': cat, 'body': body, 'z2': z2, 'z3': z3}
    for key, words in images.items():
        (d / (key + '.bin')).write_bytes(inst.wb6(words))

    env = dict(os.environ, HOME=str(d / 'home'), BESM6_PATH=str(d / 'disks'))
    zones = [(N, 'cat'), (N + 1, 'body'), (N + 2, 'z2'), (N + 3, 'z3')]
    zones += [(N + i, 'zero') for i in range(4, 41)]
    (d / 'zero.bin').write_bytes(inst.wb6([0] * 1024))
    for z, key in zones:
        r = subprocess.run(
            [str(BESMTOOL), 'write', '2048', '--start=0%o' % z,
             '--from-file=%s.bin' % key], cwd=d, env=env,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
        if r.returncode:
            raise SystemExit('FAIL write zone %o: %s' % (
                z, r.stdout.decode('utf-8', 'replace')[:300]))
    (d / 'overrides.txt').write_text(
        'note=%s\n' % note +
        '\n'.join('body[%-3o] RAM %04o = %016o' % (k, BASE + k, v & MASK)
                  for k, v in sorted(body_ov.items())) + '\n' +
        '\n'.join('zone3[%03o] RAM %06o = %016o' % (k, 0o30114 + k, v & MASK)
                  for k, v in sorted(zone3.items())) + '\n')

    if mtr:
        env['BESM6_DD_DEBUG'] = '1'
        env['BESM6_MTR_LO'], env['BESM6_MTR_HI'], env['BESM6_MTR_N'] = [
            str(x) for x in mtr[:3]]
        env['BESM6_MTR_SKIP'] = str(mtr[3] if len(mtr) > 3 else 0)
    if core:
        env['BESM6_DD_DEBUG'] = '1'
        if not mtr:
            env['BESM6_MTR_N'] = '0'
        env['BESM6_CORE_ON_PC'] = '1770'
        env['BESM6_CORE_SKIP'] = '6'

    (d / 'job.b6').write_text(JOB)
    try:
        r = subprocess.run([str(DISPAK), '-l', 'job.b6'], cwd=d, env=env,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=timeout)
        out, rc = r.stdout.decode('utf-8', 'replace'), r.returncode
    except subprocess.TimeoutExpired as e:
        out, rc = (e.stdout or b'').decode('utf-8', 'replace'), 'TIMEOUT'
    (d / 'out.txt').write_text(out)
    (EVID / (name + '_console.txt')).write_text(out)

    cp = d / 'core-pc.bin'
    core_mismatch = None
    if cp.exists():
        lines = ['case=%s note=%s' % (name, note)]
        bad = []
        for k, v in sorted(body_ov.items()):
            got = core_word(cp, BASE + k)
            if got != (v & MASK):
                bad.append(('body', k))
            lines.append('body[%-3o] RAM %04o want=%016o got=%016o' % (
                k, BASE + k, v & MASK, got if got is not None else -1))
        for k, v in sorted(zone3.items()):
            got = core_word(cp, 0o30114 + k)
            if got != (v & MASK):
                bad.append(('zone3', k))
            lines.append('zone3[%03o] RAM %06o want=%016o got=%016o' % (
                k, 0o30114 + k, v & MASK, got if got is not None else -1))
        lines.append('CORE_CHECKED=%d MISMATCH=%d' % (
            len(body_ov) + len(zone3), len(bad)))
        (EVID / (name + '_core.txt')).write_text('\n'.join(lines) + '\n')
        core_mismatch = bad

    mtr_lines = [ln for ln in out.splitlines() if ln.startswith('MTR ')]
    if mtr:
        (EVID / (name + '_mtr.txt')).write_text('\n'.join(mtr_lines) + '\n')
    if not keep:
        shutil.rmtree(d)
    return dict(name=name, rc=rc, printed=printed_all(out),
                end='КОНЕЦ ЗАДАЧИ' in out, core_mismatch=core_mismatch,
                mtr_lines=mtr_lines, dir=d)
