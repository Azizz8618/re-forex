#!/usr/bin/env python3
"""Phase-4 XY installer: install the IR-derived override stream at zone 0o2350.

Adapts the proven tests/72 installer.py recipe verbatim (catalog/body/overlay
zones, *TRANS:OURMRK*,,412350), but accepts a caller-built override dict so the
X/Y GOST words come from FRONT.FTN IR instead of the static O412D tail.

All disk writes go to COPIES under this workspace; HOME/BESM6_PATH redirected.
No repo edits, no git writes, no live disks/tmux/processes.
"""
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent
M35 = HERE.parent / '72-bound-driven'
sys.path.insert(0, str(M35))
import installer as m35  # proven zone/install recipe + parse_o412c/words_hex/wb6

from codegen_xy import MASK

WS = Path(os.environ.get(
    'M35XY_WORK', tempfile.mkdtemp(prefix='xy-',
                                    dir=os.environ.get('TMPDIR', '/tmp'))))
SHARE = Path(os.environ.get('BESM6_DISK_SHARE', '/usr/local/share/besm6'))
DISPAK = Path(os.environ.get(
    'DISPAK_BIN', '/home/azizz/Yandex.Disk/dispak/build/dispak/dispak'))
BESMTOOL = Path(os.environ.get(
    'BESMTOOL', '/home/azizz/Yandex.Disk/dispak/build/besmtool/besmtool'))
O412C = REPO / 'src/newcomp/O412C.FTN'
TAIL_HEX = REPO / 'tests/plan-f77/69-full-emitted-body/o412d_words.hex'
OBJ_HEX = REPO / 'tests/plan-f77/65-m80-install/ovl_our.hex'
CASES = WS / 'cases'
EVID = WS / 'evidence'
N = int(os.environ.get('NEWCOMP_ZONE', '02350'), 8)

JOB = """шифр 419999 зс5^
DIS 41(2048)^
eeв1а3
*name OURMRKXY
*TRANS:OURMRK*,,41%04o
       PROGRAM MAIN
       END
*execute
*end file
``````
ЕКОНЕЦ
""" % N

LINE_RE = re.compile(r'^\s*(\d{2}\s+\d+\.\d+\s+\d+\.\d+)\s*$')


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def printed(out):
    """Extract the GOST print line (never the *TRANS deck echo)."""
    for s in out.splitlines():
        if 'TRANS' in s:
            continue
        m = LINE_RE.match(s)
        if m:
            return ' '.join(m.group(1).split())
    return None


def build_images(o412, tail, obj, ov):
    body = [0] * 1024
    body[0:19] = o412[16:35]
    body[19:1024] = tail[0:1005]
    for k, v in ov.items():
        body[k] = v & MASK
    cat = o412[0:16] + [0] * 1008
    z2 = [0] * 1024
    for i, w in enumerate(o412[35:410]):
        z2[526 + i] = w
    return {'cat': cat, 'body': body, 'z2': z2, 'zero': [0] * 1024}


def make_case(name, o412, tail, obj, ov, keep=False, timeout=120, note=''):
    d = CASES / name
    if d.exists():
        shutil.rmtree(d)
    (d / 'disks').mkdir(parents=True)
    (d / 'home').mkdir(parents=True)
    for f in ('2048', '2053', '2099'):
        shutil.copy(SHARE / f, d / 'disks' / f)

    images = build_images(o412, tail, obj, ov)
    for key, words in images.items():
        (d / (key + '.bin')).write_bytes(m35.wb6(words))
    (d / 'overrides.txt').write_text(''.join(
        'body[%-3o] RAM %04o = %016o\n' % (k, 0o1757 + k, v & MASK)
        for k, v in sorted(ov.items())))

    env = dict(os.environ, HOME=str(d / 'home'), BESM6_PATH=str(d / 'disks'))
    zones = [(N, 'cat'), (N + 1, 'body'), (N + 2, 'z2')]
    zones += [(N + i, 'zero') for i in range(3, 41)]
    for z, key in zones:
        r = subprocess.run([str(BESMTOOL), 'write', '2048', '--start=0%o' % z,
                            '--from-file=%s.bin' % key], cwd=d, env=env,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=120)
        if r.returncode:
            raise SystemExit('FAIL write %o: %s' %
                             (z, r.stdout.decode('utf-8', 'replace')[:300]))

    (d / 'job.b6').write_text(JOB)
    try:
        r = subprocess.run([str(DISPAK), '-l', 'job.b6'], cwd=d, env=env,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=timeout)
        out = r.stdout.decode('utf-8', 'replace')
        rc = r.returncode
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or b'').decode('utf-8', 'replace')
        rc = 'TIMEOUT'
    (d / 'out.txt').write_text(out)

    got = printed(out)
    end = 'КОНЕЦ ЗАДАЧИ' in out
    EVID.mkdir(parents=True, exist_ok=True)
    (EVID / (name + '.txt')).write_text(
        'case=%s note=%s rc=%s\nconsole line: %r\nend_of_task=%s\n\n'
        % (name, note, rc, got, end) + out)
    if not keep:
        shutil.rmtree(d)
    return dict(name=name, printed=got, end=end, rc=rc,
                out_sha=sha(EVID / (name + '.txt')))


def load_fixtures():
    for f in (DISPAK, BESMTOOL, O412C, TAIL_HEX, OBJ_HEX, SHARE / '2048',
              SHARE / '2053', SHARE / '2099'):
        if not Path(f).exists():
            raise SystemExit('FAIL: missing %s' % f)
    o412 = m35.parse_o412c()
    tail = m35.words_hex(TAIL_HEX)
    obj = m35.words_hex(OBJ_HEX)
    if len(tail) != 1005 or tail[17] != 0o4000000000500155:
        raise SystemExit('FAIL: bad O412D fixture')
    if len(obj) != 1024 or obj[0o12] != 0o0064200402200000:
        raise SystemExit('FAIL: bad rebuilt object fixture')
    return o412, tail, obj


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', required=True)
    ap.add_argument('--keep', action='store_true')
    a = ap.parse_args()
    o412, tail, obj = load_fixtures()
    print('workspace:', WS)
    # Minimal smoke case: canonical stream from the canonical IR.
    sys.path.insert(0, str(HERE))
    from codegen_xy import read_ir, combined_stream
    ir = HERE.parent / 'ir' / 'canonical.txt'
    bound, info, text, ov = combined_stream(read_ir(ir), obj)
    res = make_case(a.only, o412, tail, obj, ov, keep=a.keep,
                    note='bound=%d text=%r' % (bound, text))
    print(a.only, res)
