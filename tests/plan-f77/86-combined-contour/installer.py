#!/usr/bin/env python3
"""M3/M4/M5 installer: zone-2350 *TRANS, bound-driven GOST output.

Reuses verbatim the proven test-70 install recipe:
  catalog zone N       = O412C.FTN words 0..15
  body    zone N+1 0..18 = O412C.FTN words 16..34
  body    zone N+1 19..1023 = O412D emitted tail (1005 words)
  overlay zone N+2 526..900 = O412C.FTN words 35..409
  zones N+3..N+40 = zero
  deck: *TRANS:OURMRK*,,412350
All disk writes go to COPIES under this workspace; HOME and BESM6_PATH are
redirected.  No repo edits, no git writes, no live disk/tmux/processes.

Usage:
  python3 installer.py                       # full A/B matrix
  python3 installer.py --only bound6,bound5  # subset
  python3 installer.py --only bound6 --keep  # retain disk copies in cases/
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
sys.path.insert(0, str(HERE))

from codegen import stream, codegen_constants, emit_deck_surface, MASK

WS = Path(os.environ.get(
    'M35_WORK', tempfile.mkdtemp(prefix='bound-',
                                 dir=os.environ.get('TMPDIR', '/tmp'))))
REPO = Path(os.environ.get('RE_FOREX_REPO', '/home/azizz/Yandex.Disk/re-forex'))
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
*name OURMRKM35
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


def build_images(o412, tail, obj, bound, zero=()):
    body = [0] * 1024
    body[0:19] = o412[16:35]
    body[19:1024] = tail[0:1005]
    ov = stream(bound, obj, zero=zero)
    for k, v in ov.items():
        body[k] = v & MASK
    cat = o412[0:16] + [0] * 1008
    z2 = [0] * 1024
    for i, w in enumerate(o412[35:410]):
        z2[526 + i] = w
    return {'cat': cat, 'body': body, 'z2': z2, 'zero': [0] * 1024}, ov


def printed(out):
    return next((s.strip() for s in out.splitlines()
                 if '1.00 3.00' in s and 'TRANS' not in s), None)


def make_case(name, o412, tail, obj, bound, zero=(), keep=False, timeout=120):
    d = CASES / name
    if d.exists():
        shutil.rmtree(d)
    (d / 'disks').mkdir(parents=True)
    (d / 'home').mkdir(parents=True)
    for f in ('2048', '2053', '2099'):
        shutil.copy(SHARE / f, d / 'disks' / f)

    images, ov = build_images(o412, tail, obj, bound, zero)
    for key, words in images.items():
        (d / (key + '.bin')).write_bytes(wb6(words))
    (d / 'overrides.txt').write_text(''.join(
        'body[%-3o] RAM %04o = %016o\n' % (k, 0o1757 + k, v & MASK)
        for k, v in sorted(ov.items())))

    env = dict(os.environ, HOME=str(d / 'home'), BESM6_PATH=str(d / 'disks'))
    zones = [(N, 'cat'), (N + 1, 'body'), (N + 2, 'z2')]
    zones += [(N + i, 'zero') for i in range(3, 41)]
    for z, key in zones:
        r = subprocess.run([str(BESMTOOL), 'write', '2048', f'--start=0{z:o}',
                            f'--from-file={key}.bin'], cwd=d, env=env,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=120)
        if r.returncode:
            raise SystemExit(f'FAIL write {z:o}: {r.stdout.decode("utf-8", "replace")[:300]}')

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

    EVID.mkdir(parents=True, exist_ok=True)
    (EVID / (name + '.txt')).write_text(
        'case=%s bound=%s zero=%r rc=%s\nconsole line: %r\nend_of_task=%s\n\n'
        % (name, bound, list(zero), rc, printed(out), 'КОНЕЦ ЗАДАЧИ' in out)
        + out)
    if not keep:
        shutil.rmtree(d)
    return dict(name=name, bound=bound, zero=tuple(zero), rc=rc,
                printed=printed(out), end='КОНЕЦ ЗАДАЧИ' in out,
                out_sha=sha(EVID / (name + '.txt')))


CASESPEC = {
    'bound6':      dict(bound=6, want='21 1.00 3.00'),
    'bound5':      dict(bound=5, want='15 1.00 3.00'),
    'restore6':    dict(bound=6, want='21 1.00 3.00'),
    'zero_tens':   dict(bound=6, zero=(0o41,), want='01 1.00 3.00'),
    'zero_units':  dict(bound=5, zero=(0o42,), want='11 1.00 3.00'),
    'zero_code9':  dict(bound=6, zero=(9,), want=None),
    'zero_code10': dict(bound=6, zero=(10,), want='01 1.00 3.00'),
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', default=','.join(CASESPEC))
    ap.add_argument('--keep', action='store_true')
    args = ap.parse_args()

    for f in (DISPAK, BESMTOOL, O412C, TAIL_HEX, OBJ_HEX, SHARE / '2048',
              SHARE / '2053', SHARE / '2099'):
        if not Path(f).exists():
            raise SystemExit(f'FAIL: missing {f}')

    cc = codegen_constants()
    if not emit_deck_surface():
        raise SystemExit('FAIL: EMIT.FTN GOST table drifted')
    o412 = parse_o412c()
    tail = words_hex(TAIL_HEX)
    raw = bytes.fromhex(OBJ_HEX.read_text().strip())
    obj = [int.from_bytes(raw[i:i + 6], 'big') for i in range(0, len(raw) - 5, 6)]
    if len(tail) != 1005 or tail[17] != 0o4000000000500155:
        raise SystemExit('FAIL: bad O412D fixture')
    if len(obj) != 1024 or obj[0o12] != 0o0064200402200000:
        raise SystemExit('FAIL: bad rebuilt object fixture')
    print(f'zone N={N:04o}  O412C_sha={sha(O412C)[:12]}  tail_sha={sha(TAIL_HEX)[:12]}')
    print('CODEGEN N3E/N3D/N3P counts:', {k: len(v) for k, v in cc.items()},
          'N3D DO-bound word=%016o' % cc['N3D'][4])
    print('EMIT.FTN authoritative GOST table: YES')

    results = {}
    for name in [c.strip() for c in args.only.split(',')]:
        spec = CASESPEC[name]
        res = make_case(name, o412, tail, obj, spec['bound'],
                        spec.get('zero', ()), keep=args.keep)
        good = (res['printed'] == spec['want']) and res['end']
        results[name] = (good, res)
        print(f'{name:12s} B={res["bound"]} zero={res["zero"]!s:8s} '
              f'printed={res["printed"]!r:20s} want={spec["want"]!r:20s} '
              f'end={res["end"]} rc={res["rc"]} {"OK" if good else "FAIL"}',
              flush=True)

    ok = all(g for g, _ in results.values())
    print('VERDICT:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
