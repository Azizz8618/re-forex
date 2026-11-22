#!/usr/bin/env python3
"""66 — our rebuilt GIVTRAN*/SETTRAN* code executes via *TRANS.

The monitor's own overlay loaders (OCATALOG / sv_load) cannot install our
rebuilt GIVTRAN* body: that module is resident, linked at load time from the
zone-0200 LINK table.  The working path is NEWCOMP*'s 4.12 compiler catalog:
place a fresh name/descriptor catalog at zone N on a COPY of disk 2048, put our
rebuilt code words in the body at N+1, keep the live overlay words at N+2,
then invoke `*TRANS:OURMRK*,,41/N`.

Everything is done on copies; HOME and BESM6_PATH are redirected per case.
The four negative controls zero the *64 word, its descriptor, its GOST text,
or skip the install; all must lose the marker.
"""
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
DISPAK = os.environ.get('DISPAK_BIN', '/home/azizz/Yandex.Disk/dispak/build/dispak/dispak')
BESMTOOL = os.environ.get('BESMTOOL', '/home/azizz/Yandex.Disk/dispak/build/besmtool/besmtool')
O412B = ROOT / 'src/newcomp/O412B.FTN'
OVL_HEX = ROOT / 'tests/plan-f77/65-m80-install/ovl_our.hex'
N = 0o1744
MASK = (1 << 48) - 1


def readw6(path):
    d = Path(path).read_bytes()
    return [int.from_bytes(d[i:i + 6], 'big') for i in range(0, len(d) - 5, 6)]


def wb6(words):
    return b''.join(w.to_bytes(6, 'big') for w in words)


def zone_from_disk(disk, zone):
    """8-byte LE disk words -> 6-byte BE overlay words."""
    b = Path(disk).read_bytes()
    out = []
    for w in range(1024):
        off = (zone + 4) * 8256 + 64 + 8 * w
        out.append(int.from_bytes(b[off:off + 8], 'little') & MASK)
    return out


def parse_o412b():
    t = O412B.read_text(encoding='utf-8', errors='replace')
    pairs = re.findall(r'HI\(NW\)\s*=\s*(\d+)\s*\n\s*LO\(NW\)\s*=\s*(\d+)', t)
    if len(pairs) != 30:
        raise SystemExit(f'FAIL: O412B: expected 30 HI/LO pairs, got {len(pairs)}')
    return [(int(hi) << 24) | int(lo) for hi, lo in pairs]


def make_case(base, name, variant, obj, o412, live1551, live1552):
    d = base / name
    (d / 'disks').mkdir(parents=True)
    (d / 'home').mkdir(parents=True)
    for f in ('2048', '2053', '2099', '2148'):
        shutil.copy(SHARE / f, d / 'disks' / f)

    body = o412[16:25] + [0] * 1024
    body[9] = obj[0o12]                       # rebuilt *64, ADR unchanged
    body[10] = 0o6700000002200000             # uj 0(15) return
    for k, src in enumerate(range(0o25, 0o32)):
        body[0o25 + k] = obj[src]             # descriptor + GOST, unchanged
    if variant == 'zero_w9':
        body[9] = 0
    elif variant == 'zero_desc':
        body[0o25] = 0
    elif variant == 'zero_gost':
        body[0o27] = 0
    body = body[:1024]
    for i in range(22, 1024):
        if body[i] == 0:
            body[i] = live1551[i]

    cat = o412[:16] + [0] * 1008
    images = {'cat': cat, 'body': body, 'z2': live1552, 'zero': [0] * 1024}
    for key, words in images.items():
        (d / (key + '.bin')).write_bytes(wb6(words))

    env = dict(os.environ, HOME=str(d / 'home'), BESM6_PATH=str(d / 'disks'))
    if variant != 'no_install':
        zones = [(N, 'cat'), (N + 1, 'body'), (N + 2, 'z2')]
        zones += [(N + i, 'zero') for i in range(3, 41)]
        for z, key in zones:
            r = subprocess.run([BESMTOOL, 'write', '2048', f'--start=0{z:o}',
                                f'--from-file={key}.bin'], cwd=d, env=env,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                               timeout=120)
            if r.returncode:
                print('FAIL: besmtool write', oct(z), r.stdout.decode('utf-8', 'replace')[:300])
                raise SystemExit(2)

    (d / 'job.b6').write_text("""шифр 419999 зс5^
DIS 41(2048)^
eeв1а3
*name OURMRK66
*TRANS:OURMRK*,,411744
      PROGRAM MAIN
      END
*execute
*end file
``````
ЕКОНЕЦ
""")
    try:
        r = subprocess.run([DISPAK, '-l', 'job.b6'], cwd=d, env=env,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=180)
        out = r.stdout.decode('utf-8', 'replace')
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or b'').decode('utf-8', 'replace')
    (d / 'out.txt').write_text(out)
    return d, '21 1.00 3.00' in out


def main():
    for f in (DISPAK, BESMTOOL, O412B, OVL_HEX, SHARE / '2048', SHARE / '2148'):
        if not Path(f).exists():
            raise SystemExit(f'FAIL: missing {f}')
    raw = bytes.fromhex(OVL_HEX.read_text().strip())
    obj = [int.from_bytes(raw[i:i + 6], 'big') for i in range(0, len(raw) - 5, 6)]
    if len(obj) != 1024 or obj[0] != 0o166 or obj[1] != 0o4751666462415612:
        raise SystemExit('FAIL: unexpected rebuilt object')
    if obj[0o12] != 0o64200402200000:
        raise SystemExit('FAIL: unexpected *64 word in rebuilt object')

    o412 = parse_o412b()
    base = Path(tempfile.mkdtemp(prefix='newcomp-our-', dir=os.environ.get('TMPDIR', '/tmp')))
    live1551 = zone_from_disk(SHARE / '2148', 0o1551)
    live1552 = zone_from_disk(SHARE / '2148', 0o1552)
    print(f'workspace: {base}')

    cases = [('normal', 'normal'), ('zero_w9', 'zero_w9'),
             ('zero_desc', 'zero_desc'), ('zero_gost', 'zero_gost'),
             ('no_install', 'no_install')]
    results = {}
    for name, variant in cases:
        d, marker = make_case(base, name, variant, obj, o412, live1551, live1552)
        results[name] = marker
        keys = sorted(set(re.findall(
            r'21 1\.00 3\.00|4\.12|ОТСУТСТВУЕТ|Interrupt \d+|КОНЕЦ ЗАДАЧИ',
            (d / 'out.txt').read_text(errors='replace'))))
        print(f'{name:12s} marker={"YES" if marker else "no ":3s}  {", ".join(keys)}')

    ok = (results['normal'] and not any(results[k] for k in
          ('zero_w9', 'zero_desc', 'zero_gost', 'no_install')))
    print('VERDICT:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
