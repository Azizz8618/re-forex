#!/usr/bin/env python3
"""Two-stage trampoline on COPIES: our rebuilt *TRANS body runs multiple words.

Adapted from /home/azizz/Yandex.Disk/re-forex/tests/plan-f77/66-newcomp-ourcode/run.py.
The NEWCOMP 4.12 catalog/body install path is unchanged; only the placement of
the rebuilt GIVTRAN* words is now by meaningful role.

Memory model (proven by test 66): body[k] -> RAM 0o1757+k.  The compiler enters
at RAM 0o1770 = body[9].  The rebuilt object was assembled with that same origin,
so every object word's ADR resolves when the word is put at body[index] == obj index.

Placements (obj index -> body index -> RAM):
    stage1 *64      obj 0o12 -> body 9    -> 0o1770   ADR 0o2007 = body 0o30
    UJ stage2       obj 0o13 -> body 10   -> 0o1771   ADR 0o2003 = body 0o24
    guard (return)  test-66 word -> body 11 -> 0o1772  (unreachable when UJ works)
    stage2 *64      obj 0o24 -> body 0o24 -> 0o2003   ADR 0o2014 = body 0o35
    ret after st2   obj 0o25 -> body 0o25 -> 0o2004
    descriptor1     obj 0o30..0o34 -> body 0o30..0o34 -> 0o2007..0o2013
    descriptor2     obj 0o35..0o41 -> body 0o35..0o41 -> 0o2014..0o2022

The jump ADR needs NO adjustment: 0o2003 is exactly RAM(0o1757+0o24), the body
slot chosen for STAGE2.  The guard word is placed immediately AFTER the UJ so it
is dead code in the normal path; it stops a fall-through from reaching STAGE2
when the UJ is zeroed in control (a).  It is the proven "13,UJ,." return word of
test 66 (0o6700000002200000).

Control (c), zeroing only stage1's *64, cannot suppress stage2 in this design:
a zero body[9] is a harmless store, so execution falls straight into the intact
UJ at body[10].  This is recorded honestly, and an extra control (c') zeroes
stage1 AND the UJ to show that the pair is necessary and sufficient.
"""
import hashlib
import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = Path('/home/azizz/Yandex.Disk/re-forex')
SHARE = Path(os.environ.get('BESM6_DISK_SHARE', '/usr/local/share/besm6'))
DISPAK = os.environ.get(
    'DISPAK_BIN', '/home/azizz/Yandex.Disk/dispak/build/dispak/dispak')
BESMTOOL = os.environ.get(
    'BESMTOOL', '/home/azizz/Yandex.Disk/dispak/build/besmtool/besmtool')
O412B = ROOT / 'src/newcomp/O412B.FTN'
OBJ = HERE / 'ovl_stage2.hex'
WORK = Path(os.environ.get(
    'PHASE1_WORK', tempfile.mkdtemp(prefix='stage2-evidence-',
                                    dir=os.environ.get('TMPDIR', '/tmp'))))
EVIDENCE = WORK / 'evidence'
EVIDENCE.mkdir(parents=True, exist_ok=True)
N = 0o1744
RAM_BASE = 0o1757
RET = 0o6700000002200000   # test-66 return word, used as fall-through guard

# (role, object index, body index)
PLACEMENTS = [
    ('stage1_*64',      0o12,  9),
    ('jump_to_stage2',  0o13, 10),
    ('ret_after_st1',   0o14, 0o14),   # unreachable, kept for fidelity
    ('stage2_*64',      0o24, 0o24),
    ('ret_after_st2',   0o25, 0o25),
    ('desc1',           0o30, 0o30),
    ('desc1b',          0o31, 0o31),
    ('gost1a',          0o32, 0o32),
    ('gost1b',          0o33, 0o33),
    ('desc1tail',       0o34, 0o34),
    ('desc2',           0o35, 0o35),
    ('desc2b',          0o36, 0o36),
    ('gost2a',          0o37, 0o37),
    ('gost2b',          0o40, 0o40),
    ('desc2tail',       0o41, 0o41),
]
GUARD_BODY = 11

ZERO_TARGETS = {
    'zero_jump':     ['jump_to_stage2'],
    'zero_stage2':   ['stage2_*64'],
    'zero_stage1':   ['stage1_*64'],
    'zero_both':     ['stage1_*64', 'jump_to_stage2'],
}

JOB = """шифр 419999 зс5^
DIS 41(2048)^
eeв1а3
*name OURMRK72
*TRANS:OURMRK*,,411744
      PROGRAM MAIN
      END
*execute
*end file
``````
ЕКОНЕЦ
"""


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def readw6(path):
    p = Path(path)
    if p.suffix == '.hex':
        d = bytes.fromhex(p.read_text().strip())
    else:
        d = p.read_bytes()
    return [int.from_bytes(d[i:i + 6], 'big') for i in range(0, len(d) - 5, 6)]


def wb6(words):
    return b''.join(w.to_bytes(6, 'big') for w in words)


def zone_from_disk(disk, zone):
    b = Path(disk).read_bytes()
    out = []
    for w in range(1024):
        off = (zone + 4) * 8256 + 64 + 8 * w
        out.append(int.from_bytes(b[off:off + 8], 'little') & ((1 << 48) - 1))
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
    roles = {r: (oi, bi) for r, oi, bi in PLACEMENTS}
    placed = {}
    for role, oi, bi in PLACEMENTS:
        body[bi] = obj[oi]
        placed[role] = (oi, bi, obj[oi])
    body[GUARD_BODY] = RET
    placed['guard'] = (None, GUARD_BODY, RET)
    for role in ZERO_TARGETS.get(variant, []):
        oi, bi = roles[role]
        body[bi] = 0
        placed[role] = (oi, bi, 0)
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

    (d / 'job.b6').write_text(JOB)
    try:
        r = subprocess.run([DISPAK, '-l', 'job.b6'], cwd=d, env=env,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=180)
        out = r.stdout.decode('utf-8', 'replace')
    except subprocess.TimeoutExpired as e:
        out = (e.stdout or b'').decode('utf-8', 'replace')
    (d / 'out.txt').write_text(out)

    ev = EVIDENCE / name
    ev.mkdir(parents=True, exist_ok=True)
    shutil.copy(d / 'out.txt', ev / 'out.txt')
    shutil.copy(d / 'body.bin', ev / 'body.bin')
    (ev / 'placement.tsv').write_text('\n'.join(
        f'{role}\tobj={"none" if oi is None else format(oi, "04o")}\t'
        f'body={bi:04o}\tram={RAM_BASE+bi:04o}\tword={val:016o}'
        for role, (oi, bi, val) in sorted(placed.items())) + '\n')
    shutil.rmtree(d)      # disks are bulky; evidence is preserved above
    return out, placed


def main():
    for f in (DISPAK, BESMTOOL, O412B, OBJ, SHARE / '2048', SHARE / '2148'):
        if not Path(f).exists():
            raise SystemExit(f'FAIL: missing {f}')

    obj = readw6(OBJ)
    if len(obj) != 1024:
        raise SystemExit(f'FAIL: object has {len(obj)} words')
    expect = {
        0o12: 0o0064200702200000,   # stage1 *64, ADR 0o2007
        0o13: 0o0300200367000000,   # UJ STAGE2, ADR 0o2003
        0o24: 0o0064201402200000,   # stage2 *64, ADR 0o2014
        0o30: 0o0000201100002011,   # descriptor1 -> GOST1 at 0o2011
        0o35: 0o0000201600002016,   # descriptor2 -> GOST2 at 0o2016
    }
    for idx, val in expect.items():
        if obj[idx] != val:
            raise SystemExit(f'FAIL: obj[{idx:04o}]={obj[idx]:016o}, expected {val:016o}')
    assert (obj[0o12] >> 24) & 0o7777 == 0o2007 == RAM_BASE + 0o30
    assert (obj[0o13] >> 24) & 0o7777 == 0o2003 == RAM_BASE + 0o24
    assert (obj[0o24] >> 24) & 0o7777 == 0o2014 == RAM_BASE + 0o35
    assert (obj[0o30] >> 24) & 0o7777 == 0o2011 == RAM_BASE + 0o32
    assert (obj[0o35] >> 24) & 0o7777 == 0o2016 == RAM_BASE + 0o37

    o412 = parse_o412b()
    base = Path(tempfile.mkdtemp(prefix='stage2-final-',
                                 dir=os.environ.get('TMPDIR', '/tmp')))
    live1551 = zone_from_disk(SHARE / '2148', 0o1551)
    live1552 = zone_from_disk(SHARE / '2148', 0o1552)
    print('object:', OBJ, sha256(OBJ))
    print('workspace:', base)

    cases = [
        ('normal', 'normal'),
        ('a_zero_jump', 'zero_jump'),
        ('b_zero_stage2', 'zero_stage2'),
        ('c_zero_stage1', 'zero_stage1'),
        ('c2_zero_both', 'zero_both'),
        ('d_no_install', 'no_install'),
    ]
    results = {}
    for name, variant in cases:
        out, placed = make_case(base, name, variant, obj, o412, live1551, live1552)
        s1 = '21 1.00 3.00' in out
        s2 = 'STAGE2-7391' in out
        results[name] = (s1, s2)
        keys = re.findall(r'21 1\.00 3\.00|STAGE2-7391|КОНЕЦ ЗАДАЧИ', out)
        print(f'{name:16s} stage1={s1!s:5s} stage2={s2!s:5s}  {" | ".join(keys)}  '
              f'out_sha={sha256(EVIDENCE/name/"out.txt")[:16]}', flush=True)
        if name == 'normal':
            (WORK / 'console_normal.txt').write_text(out)

    ok = (results['normal'] == (True, True)
          and results['a_zero_jump'] == (True, False)
          and results['b_zero_stage2'] == (True, False)
          and results['c_zero_stage1'] == (False, True)   # documented fall-through
          and results['c2_zero_both'] == (False, False)
          and results['d_no_install'] == (False, False))
    print('VERDICT:', 'PASS' if ok else 'FAIL')
    (WORK / 'verdict.txt').write_text(
        '\n'.join(f'{k}: stage1={v[0]} stage2={v[1]}' for k, v in results.items())
        + f'\nVERDICT: {"PASS" if ok else "FAIL"}\n')
    print('evidence:', WORK)
    return 0 if ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
