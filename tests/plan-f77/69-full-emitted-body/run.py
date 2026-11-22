#!/usr/bin/env python3
"""69 — full *TRANS body emitted by our own Fortran (zone 2350).

M2 gate: every body word 19..1023 comes verbatim from the 1005 words emitted by
O412D.FTN; catalog and N+2 words come from O412C.FTN. No live-root word is read.
The compiler catalog/body are installed at zone N=0o2350 (deck ,,412350), as
requested for the new compiler; zones 0o2300..0o2347 remain reserved for the old
PERSO experiments.

All writes go to COPIES under a temp workspace; HOME/BESM6_PATH are redirected.
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

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
SHARE = Path(os.environ.get('BESM6_DISK_SHARE', '/usr/local/share/besm6'))
DISPAK = Path(os.environ.get(
    'DISPAK_BIN', '/home/azizz/Yandex.Disk/dispak/build/dispak/dispak'))
BESMTOOL = Path(os.environ.get(
    'BESMTOOL', '/home/azizz/Yandex.Disk/dispak/build/besmtool/besmtool'))
O412C = ROOT / 'src/newcomp/O412C.FTN'
TAIL_HEX = HERE / 'o412d_words.hex'
OBJ_HEX = ROOT / 'tests/plan-f77/65-m80-install/ovl_our.hex'
N = int(os.environ.get('NEWCOMP_ZONE', '02350'), 8)
WORK = Path(tempfile.mkdtemp(prefix='full-emitted-',
                             dir=os.environ.get('TMPDIR', '/tmp')))
CASES = WORK / 'cases'
EVID = WORK / 'evidence'
JOB = """шифр 419999 зс5^
DIS 41(2048)^
eeв1а3
*name OURMRK69
*TRANS:OURMRK*,,41%04o
      PROGRAM MAIN
      END
*execute
*end file
``````
ЕКОНЕЦ
""" % N


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def wb6(words):
    return b''.join(w.to_bytes(6, 'big') for w in words)


def words_hex(path):
    raw = bytes.fromhex(Path(path).read_text().strip())
    return [int.from_bytes(raw[i:i + 6], 'big') for i in range(0, len(raw) - 5, 6)]


def parse_o412c():
    t = O412C.read_text(encoding='utf-8', errors='replace')
    p = re.findall(r'HI\(NW\)\s*=\s*(\d+)\s*\n\s*LO\(NW\)\s*=\s*(\d+)', t)
    if len(p) != 410:
        raise SystemExit(f'FAIL: O412C expected 410 pairs, got {len(p)}')
    return [(int(h) << 24) | int(l) for h, l in p]


def build_images(o412, tail, obj, zero36=False):
    if len(o412) != 410 or len(tail) != 1005 or len(obj) != 1024:
        raise SystemExit(f'FAIL sizes {len(o412)}/{len(tail)}/{len(obj)}')
    body = [0] * 1024
    body[0:19] = o412[16:35]
    body[19:1024] = tail[0:1005]
    body[15] = obj[0o27]
    body[16] = obj[0o30]
    body[17] = obj[0o31]
    if zero36:
        body[36] = 0
    cat = o412[0:16] + [0] * 1008
    z2 = [0] * 1024
    for i, w in enumerate(o412[35:410]):
        z2[526 + i] = w
    return {'cat': cat, 'body': body, 'z2': z2, 'zero': [0] * 1024}


def make_case(name, o412, tail, obj, *, zero36=False, no_install=False,
              sanitize_2148=False, omit_2148=False):
    d = CASES / name
    (d / 'disks').mkdir(parents=True, exist_ok=True)
    (d / 'home').mkdir(parents=True, exist_ok=True)
    for f in ('2048', '2053', '2099'):
        shutil.copy(SHARE / f, d / 'disks' / f)
    dst2148 = d / 'disks' / '2148'
    if not omit_2148:
        shutil.copy(SHARE / '2148', dst2148)
        if sanitize_2148:
            with open(dst2148, 'r+b') as f:
                for zone in (0o1551, 0o1552):
                    f.seek((zone + 4) * 8256 + 64)
                    f.write(b'\x00' * (1024 * 8))
    for key, words in build_images(o412, tail, obj, zero36).items():
        (d / (key + '.bin')).write_bytes(wb6(words))
    env = dict(os.environ, HOME=str(d / 'home'), BESM6_PATH=str(d / 'disks'))
    if not no_install:
        zones = [(N, 'cat'), (N + 1, 'body'), (N + 2, 'z2')]
        zones += [(N + i, 'zero') for i in range(3, 41)]
        for z, key in zones:
            r = subprocess.run([str(BESMTOOL), 'write', '2048',
                                f'--start=0{z:o}', f'--from-file={key}.bin'],
                               cwd=d, env=env, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, timeout=120)
            if r.returncode:
                raise SystemExit(f'FAIL write zone {z:o}: '
                                 f'{r.stdout.decode("utf-8", "replace")[:300]}')
    (d / 'job.b6').write_text(JOB)
    timed_out = False
    try:
        r = subprocess.run([str(DISPAK), '-l', 'job.b6'], cwd=d, env=env,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=90)
        out = r.stdout.decode('utf-8', 'replace')
        rc = r.returncode
    except subprocess.TimeoutExpired as e:
        timed_out = True
        out = (e.stdout or b'').decode('utf-8', 'replace')
        rc = 'TIMEOUT'
    (d / 'out.txt').write_text(out)
    return dict(marker='21 1.00 3.00' in out, endtask='КОНЕЦ ЗАДАЧИ' in out,
                timed_out=timed_out, rc=rc, sha=sha(d / 'out.txt'), dir=str(d))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', default='normal,zero36,restore,no_install,nosan,no2148')
    args = ap.parse_args()
    for f in (DISPAK, BESMTOOL, O412C, TAIL_HEX, OBJ_HEX, SHARE / '2048',
              SHARE / '2053', SHARE / '2099', SHARE / '2148'):
        if not Path(f).exists():
            raise SystemExit(f'FAIL: missing {f}')
    o412 = parse_o412c()
    tail = words_hex(TAIL_HEX)
    obj = words_hex(OBJ_HEX)
    if len(tail) != 1005 or tail[17] != 0o4000000000500155:
        raise SystemExit('FAIL: bad O412D tail fixture')
    if len(obj) != 1024 or obj[0o12] != 0o0064200402200000:
        raise SystemExit('FAIL: bad rebuilt object fixture')
    EVID.mkdir(parents=True, exist_ok=True)
    print(f'zone N={N:04o} workspace={WORK}')
    cases = {'normal': {}, 'zero36': {'zero36': True}, 'restore': {},
             'no_install': {'no_install': True},
             'nosan': {'sanitize_2148': True},
             'no2148': {'omit_2148': True}}
    res = {}
    for name in [c.strip() for c in args.only.split(',')]:
        r = make_case(name, o412, tail, obj, **cases[name])
        res[name] = r
        print(f'{name:12s} rc={str(r["rc"]):7s} marker={"YES" if r["marker"] else "no":3s} '
              f'endtask={"YES" if r["endtask"] else "no":3s} sha={r["sha"][:16]}',
              flush=True)
    want = ('normal', 'zero36', 'restore', 'no_install')
    ok = all(k in res for k in want) and (
        res['normal']['marker'] and res['normal']['endtask']
        and not res['zero36']['marker'] and res['zero36']['timed_out']
        and res['restore']['marker'] and res['restore']['endtask']
        and not res['no_install']['marker']
        and res['nosan']['marker'] and res['nosan']['sha'] == res['normal']['sha']
        and res['no2148']['marker'] and res['no2148']['sha'] == res['normal']['sha'])
    print('VERDICT:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
