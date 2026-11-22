#!/usr/bin/env python3
"""Zone-2350 *TRANS install harness with CORE-dump probe support.

Derived verbatim from tests/plan-f77/70-computed-output/run.py + 72-bound-driven
installer.py.  Every case uses COPIES of the disks, redirects HOME/BESM6_PATH,
and never touches the repo, git, live disks, tmux, processes or dispak sources.
"""
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS = Path(os.environ.get(
    'WIN78_WORK', tempfile.mkdtemp(prefix='win78-',
                                   dir=os.environ.get('TMPDIR', '/tmp'))))
REPO = Path(os.environ.get('REPO_ROOT', str(HERE.parent.parent.parent)))
SHARE = Path(os.environ.get('BESM6_DISK_SHARE', '/usr/local/share/besm6'))
DISPAK = Path(os.environ.get(
    'DISPAK_BIN', '/home/azizz/Yandex.Disk/dispak/build/dispak/dispak'))
BESMTOOL = Path(os.environ.get(
    'BESMTOOL', '/home/azizz/Yandex.Disk/dispak/build/besmtool/besmtool'))
O412C = REPO / 'src/newcomp/O412C.FTN'
TAIL_HEX = REPO / 'tests/plan-f77/69-full-emitted-body/o412d_words.hex'
OBJ_HEX = REPO / 'tests/plan-f77/65-m80-install/ovl_our.hex'

N = int(os.environ.get('NEWCOMP_ZONE', '02350'), 8)
BASE = 0o1757
MASK = (1 << 48) - 1
XTA, ARX, STO = 0x008000, 0x00b000, 0x000000
GOST, A1ADR, A2ADR = 0o2006, 0o2020, 0o2021
RET = 0o6700000002200000
OBJ12 = 0o0064200402200000

JOB = """шифр 419999 зс5^
DIS 41(2048)^
eeв1а3
*name OURMRKLW
*TRANS:OURMRK*,,41%04o
       PROGRAM MAIN
       END
*execute
*end file
``````
ЕКОНЕЦ
""" % N


def wb6(words):
    return b''.join(w.to_bytes(6, 'big') for w in words)


def words_hex(path):
    raw = bytes.fromhex(Path(path).read_text().strip())
    return [int.from_bytes(raw[i:i + 6], 'big') for i in range(0, len(raw) - 5, 6)]


def parse_o412c():
    t = O412C.read_text(encoding='utf-8', errors='replace')
    p = re.findall(r'HI\(NW\)\s*=\s*(\d+)\s*\n\s*LO\(NW\)\s*=\s*(\d+)', t)
    if len(p) != 410:
        raise SystemExit('FAIL: O412C expected 410 pairs, got %d' % len(p))
    return [(int(hi) << 24) | int(lo) for hi, lo in p]


def half(op, adr):
    return op | (adr & 0o7777)


def word(lop, ladr, rop, radr):
    return (half(lop, ladr) << 24) | half(rop, radr)


def gost0():
    return ((0 * 65536 + 1 * 256 + 15) << 24) | (1 * 65536 + 14 * 256 + 0)


def build_images(o412, tail, obj, *, a1=1, a2=1, body_patch=None,
                 cat_patch=None, z2_patch=None):
    """body_patch/cat_patch/z2_patch: dict word-index -> 48-bit value."""
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
    for k, v in ov.items():
        body[k] = v & MASK
    cat = o412[0:16] + [0] * 1008
    z2 = [0] * 1024
    for i, w in enumerate(o412[35:410]):
        z2[526 + i] = w
    for patch, arr in ((body_patch, body), (cat_patch, cat), (z2_patch, z2)):
        if patch:
            for k, v in patch.items():
                if not 0 <= k < 1024:
                    raise ValueError('patch index %o out of range' % k)
                arr[k] = v & MASK
    return {'cat': cat, 'body': body, 'z2': z2, 'zero': [0] * 1024}


def probe_word(off):
    """Distinctive sentinel: high half 0o7777, low half = body offset."""
    return (0o7777 << 24) | (off & 0o7777)


def core_word(path, addr):
    if not path or not path.exists():
        return None
    data = path.read_bytes()
    off = addr * 6
    if off + 6 > len(data):
        return None
    return int.from_bytes(data[off:off + 6], 'big')


def run_case(name, *, body_patch=None, cat_patch=None, z2_patch=None,
             a1=1, a2=1, core=True, core_skip=6, timeout=150, keep=True,
             mtr=None, zone_patches=None):
    d = WS / 'cases' / name
    if d.exists():
        shutil.rmtree(d)
    (d / 'disks').mkdir(parents=True)
    (d / 'home').mkdir(parents=True)
    for f in ('2048', '2053', '2099'):
        shutil.copy(SHARE / f, d / 'disks' / f)

    o412 = parse_o412c()
    tail = words_hex(TAIL_HEX)
    obj = words_hex(OBJ_HEX)
    images = build_images(o412, tail, obj, a1=a1, a2=a2,
                          body_patch=body_patch, cat_patch=cat_patch,
                          z2_patch=z2_patch)
    for key, words in images.items():
        (d / (key + '.bin')).write_bytes(wb6(words))
    (d / 'patches.txt').write_text(
        'body_patch=%r\ncat_patch=%r\nz2_patch=%r\n' %
        (body_patch or {}, cat_patch or {}, z2_patch or {}))

    env = dict(os.environ, HOME=str(d / 'home'), BESM6_PATH=str(d / 'disks'))
    zones = [(N, 'cat'), (N + 1, 'body'), (N + 2, 'z2')]
    zones += [(N + i, 'zero') for i in range(3, 41)]
    if zone_patches:
        for i, patch in zone_patches.items():
            words = [0] * 1024
            for k, v in patch.items():
                words[k] = v & MASK
            key = 'z%d' % i
            (d / (key + '.bin')).write_bytes(wb6(words))
            zones = [(zz, key if zz == N + i else kk) for zz, kk in zones]
    for z, key in zones:
        r = subprocess.run([str(BESMTOOL), 'write', '2048', '--start=0%o' % z,
                            '--from-file=%s.bin' % key],
                           cwd=d, env=env, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, timeout=120)
        if r.returncode:
            raise RuntimeError('write zone %o: %s' %
                               (z, r.stdout.decode('utf-8', 'replace')[:300]))

    (d / 'job.b6').write_text(JOB)
    if mtr:
        env['BESM6_DD_DEBUG'] = '1'
        env['BESM6_MTR_LO'], env['BESM6_MTR_HI'], env['BESM6_MTR_N'] = [str(x) for x in mtr[:3]]
        env['BESM6_MTR_SKIP'] = str(mtr[3] if len(mtr) > 3 else 0)
    if core:
        env['BESM6_DD_DEBUG'] = '1'
        if not mtr:
            env['BESM6_MTR_N'] = '0'
        env['BESM6_CORE_ON_PC'] = '1770'
        env['BESM6_CORE_SKIP'] = str(core_skip)
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

    printed = next((s.strip() for s in out.splitlines()
                    if '1.00 3.00' in s and 'TRANS' not in s), None)
    end = 'КОНЕЦ ЗАДАЧИ' in out
    cp = d / 'core-pc.bin'
    return dict(name=name, rc=rc, printed=printed, end=end,
                core=cp if cp.exists() else None, dir=d,
                out=out, images=images)


def ram_at(res, offsets):
    return {'%04o' % off: '%016o' % core_word(res['core'], BASE + off)
            if core_word(res['core'], BASE + off) is not None else 'NO_DUMP'
            for off in offsets}


def short(res):
    return '%-22s rc=%-7s print=%-16r end=%-5s core=%s' % (
        res['name'], res['rc'], res['printed'], res['end'],
        bool(res['core']))
