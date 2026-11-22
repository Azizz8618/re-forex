#!/usr/bin/env python3
"""70 — computed output from our code, fully emitted body, zone 2350.

Combines phase 3 (runtime arithmetic on the GOST digit) with M2/test 69 (every
body word comes from our Fortran emitters). The leading digit is computed at run
time by two raw ARX additions; no static '2' is stored in our fragment.

Install: catalog N=0o2350 from O412C, body 0..18 from O412C, body 19..1023 from
O412D, N+2 words 526..900 from O412C, then our arithmetic/descriptor overrides
inside the copy window (body 0..0o43). All writes to COPIES; HOME/BESM6_PATH
redirected; live disks are never opened for writing.
"""
import argparse
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
TAIL_HEX = ROOT / 'tests/plan-f77/69-full-emitted-body/o412d_words.hex'
OBJ_HEX = ROOT / 'tests/plan-f77/65-m80-install/ovl_our.hex'
N = int(os.environ.get('NEWCOMP_ZONE', '02350'), 8)
RAM_BASE = 0o1757
MASK = (1 << 48) - 1
XTA, ARX, STO = 0x008000, 0x00b000, 0x000000
GOST, A1ADR, A2ADR = 0o2006, 0o2020, 0o2021
RET = 0o6700000002200000
OBJ12 = 0o0064200402200000
WORK = Path(tempfile.mkdtemp(prefix='computed-',
                             dir=os.environ.get('TMPDIR', '/tmp')))
JOB = """шифр 419999 зс5^
DIS 41(2048)^
eeв1а3
*name OURMRK70
*TRANS:OURMRK*,,41%04o
      PROGRAM MAIN
      END
*execute
*end file
``````
ЕКОНЕЦ
""" % N


def words_hex(path):
    raw = bytes.fromhex(Path(path).read_text().strip())
    return [int.from_bytes(raw[i:i + 6], 'big') for i in range(0, len(raw) - 5, 6)]


def wb6(words):
    return b''.join(w.to_bytes(6, 'big') for w in words)


def parse_o412c():
    t = O412C.read_text(encoding='utf-8', errors='replace')
    p = re.findall(r'HI\(NW\)\s*=\s*(\d+)\s*\n\s*LO\(NW\)\s*=\s*(\d+)', t)
    if len(p) != 410:
        raise SystemExit(f'FAIL: O412C expected 410 pairs, got {len(p)}')
    return [(int(h) << 24) | int(l) for h, l in p]


def half(op, adr):
    return op | (adr & 0o7777)


def word(lop, ladr, rop, radr):
    return (half(lop, ladr) << 24) | half(rop, radr)


def gost0():
    # GOSTEN packing of "01 1.0": leading digit code 0, computed at runtime
    return ((0 * 65536 + 1 * 256 + 15) << 24) | (1 * 65536 + 14 * 256 + 0)


def build_images(o412, tail, obj, a1=1, a2=1, zero=()):
    body = [0] * 1024
    body[0:19] = o412[16:35]
    body[19:1024] = tail[0:1005]
    ov = {
        9: word(XTA, GOST, ARX, A1ADR),
        10: word(ARX, A2ADR, STO, GOST),
        11: OBJ12,
        12: RET,
        0o25: obj[0o25], 0o26: obj[0o26], 0o27: gost0(),
        0o30: obj[0o30], 0o31: obj[0o31],
        0o41: (a1 << 40) & MASK, 0o42: (a2 << 40) & MASK,
    }
    for k in zero:
        ov[k] = 0
    for k, v in ov.items():
        body[k] = v & MASK
    cat = o412[0:16] + [0] * 1008
    z2 = [0] * 1024
    for i, w in enumerate(o412[35:410]):
        z2[526 + i] = w
    print('overrides:', {oct(k): '%016o' % v for k, v in sorted(ov.items())})
    return {'cat': cat, 'body': body, 'z2': z2, 'zero': [0] * 1024}


def make_case(name, o412, tail, obj, a1=1, a2=1, zero=()):
    d = WORK / name
    (d / 'home').mkdir(parents=True, exist_ok=True)
    for key, words in build_images(o412, tail, obj, a1, a2, zero).items():
        (d / (key + '.bin')).write_bytes(wb6(words))
    env = dict(os.environ, HOME=str(d / 'home'), BESM6_PATH=str(d / 'disks'))
    for z, key in ([(N, 'cat'), (N + 1, 'body'), (N + 2, 'z2')]
                   + [(N + i, 'zero') for i in range(3, 41)]):
        r = subprocess.run([str(BESMTOOL), 'write', '2048', f'--start=0{z:o}',
                            f'--from-file={key}.bin'], cwd=d, env=env,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=120)
        if r.returncode:
            raise SystemExit(f'FAIL write {z:o}: {r.stdout.decode("utf-8", "replace")[:200]}')
    (d / 'job.b6').write_text(JOB)
    try:
        r = subprocess.run([str(DISPAK), '-l', 'job.b6'], cwd=d, env=env,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=120)
        out = r.stdout.decode('utf-8', 'replace')
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or b'').decode('utf-8', 'replace')
    (d / 'out.txt').write_text(out)
    printed = next((s.strip() for s in out.splitlines()
                    if '1.00 3.00' in s and 'TRANS' not in s), None)
    return printed, 'КОНЕЦ ЗАДАЧИ' in out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', default='normal,plus1,restore,zero_a1,zero_word9,zero_word10')
    args = ap.parse_args()
    for f in (DISPAK, BESMTOOL, O412C, TAIL_HEX, OBJ_HEX, SHARE / '2048',
              SHARE / '2053', SHARE / '2099'):
        if not Path(f).exists():
            raise SystemExit(f'FAIL: missing {f}')
    o412 = parse_o412c()
    tail = words_hex(TAIL_HEX)
    obj = words_hex(OBJ_HEX)
    if len(tail) != 1005 or tail[17] != 0o4000000000500155:
        raise SystemExit('FAIL: bad O412D fixture')
    if len(obj) != 1024 or obj[0o12] != OBJ12:
        raise SystemExit('FAIL: bad rebuilt object fixture')
    print(f'zone N={N:04o} workspace={WORK}')
    cases = {
        'normal': dict(a1=1, a2=1, want='21 1.00 3.00'),
        'plus1': dict(a1=2, a2=1, want='31 1.00 3.00'),
        'restore': dict(a1=1, a2=1, want='21 1.00 3.00'),
        'zero_a1': dict(a1=0, a2=1, want='11 1.00 3.00'),
        'zero_word9': dict(a1=1, a2=1, zero=(9,), want=None),
        'zero_word10': dict(a1=1, a2=1, zero=(10,), want='01 1.00 3.00'),
    }
    ok = True
    for name in [c.strip() for c in args.only.split(',')]:
        c = cases[name]
        # BESM6_PATH needs the copied disks; create them per case
        d = WORK / name
        (d / 'disks').mkdir(parents=True, exist_ok=True)
        for f in ('2048', '2053', '2099'):
            shutil.copy(SHARE / f, d / 'disks' / f)
        printed, end = make_case(name, o412, tail, obj,
                                 a1=c['a1'], a2=c['a2'], zero=c.get('zero', ()))
        good = (printed == c['want']) and end
        ok = ok and good
        print(f'{name:12s} printed={printed!r:24s} want={c["want"]!r:24s} '
              f'end={end} {"OK" if good else "FAIL"}', flush=True)
    print('VERDICT:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
