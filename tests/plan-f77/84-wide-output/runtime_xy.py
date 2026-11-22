#!/usr/bin/env python3
"""limit-lifting step 2: runtime BESM-6 X/Y digits from structured IR tokens.

Proves that the X and Y printed digits can be computed AT RUN TIME by our own
BESM-6 instruction words (raw ARX / opcode 013), driven by a token stream,
instead of being constant-folded into GOST words at emission time (test 74).

Design
------
* GOST words body[0o27]/body[0o30] are seeded with ZERO digit bytes at the X
  (byte 3 of word 1) and Y (byte 2 of word 2) positions.  Before the run the
  printed digits are '0'; they become non-zero only after our ARX words add
  the digit weights from body data cells.
* The N leading digits still use the proven test-72 bound-driven ARX chain.
* Only proven opcodes are used: XTA / ARX / STO / *64 / UJ (test 70/72/74).

Reuse: the zone-2350 install recipe, word encoders and fixtures are imported
verbatim from the proven tests/72-bound-driven modules (read-only import).

Write scope: only this workspace and temp disk copies under TMPDIR.  No repo
edits, no git writes, no live disks/tmux/processes, no dispak C patches.
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
REPO = Path(__file__).resolve().parent.parent.parent.parent
M35 = HERE
sys.path.insert(0, str(M35))
sys.path.insert(0, str(HERE))
import codegen as cg          # proven test-72 word/opcode wiring
import installer as m35       # proven zone-2350 install recipe + helpers
from token_interface import interpret, TOKENS_X1_ADD2, tokens_for

SHARE = Path(os.environ.get('BESM6_DISK_SHARE', '/usr/local/share/besm6'))
DISPAK = Path(os.environ.get('DISPAK_BIN',
                             '/home/azizz/Yandex.Disk/dispak/build/dispak/dispak'))
BESMTOOL = Path(os.environ.get('BESMTOOL',
                               '/home/azizz/Yandex.Disk/dispak/build/besmtool/besmtool'))
WS = Path(os.environ.get(
    'RTXY_WORK', tempfile.mkdtemp(prefix='rtxy-',
                                  dir=os.environ.get('TMPDIR', '/tmp/.private/azizz/opencode'))))
CASES = WS / 'cases'
EVID = WS / 'evidence'
CASES.mkdir(parents=True, exist_ok=True)
EVID.mkdir(parents=True, exist_ok=True)
N = int(os.environ.get('NEWCOMP_ZONE', '02350'), 8)
MASK = (1 << 48) - 1

# --- proven opcode prefixes / words (from test 70/72) -----------------------
XTA, ARX, STO = cg.XTA, cg.ARX, cg.STO
OBJ12 = cg.OBJ12                       # *64 2004 print word
RET = cg.RET                           # uj 0(15)
emit48 = cg.emit48
ram = cg.ram

# --- RAM addresses derived from BASE = 0o1757 -------------------------------
A_G1 = ram(0o27)     # 0o2006 : GOST word 1 (N digits + X digit)
A_G2 = ram(0o30)     # 0o2007 : GOST word 2 (Y digit)
A_DESC = ram(0o25)   # 0o2004 : *64 descriptor
# data cells (all inside the proven body[0..0o43] copy window)
A_NT = ram(0o41)     # 0o2020 : N tens  (word 1 byte 0)
A_NU = ram(0o42)     # 0o2021 : N units (word 1 byte 1)
A_XW1 = ram(0o43)    # 0o2022 : X digit weight for word 1 byte 3
A_XW2 = ram(0o32)    # 0o2011 : X contribution to Y (word 2 byte 2)
A_AW2 = ram(0o33)    # 0o2012 : addend contribution to Y (word 2 byte 2)

# body indices for the runtime instruction words
CODE_SLOTS = [9, 10, 11, 12, 13, 14, 15, 16]
DATA_SLOTS = {'nt': 0o41, 'nu': 0o42, 'xw1': 0o43, 'xw2': 0o32, 'aw2': 0o33}

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

LINE_RE = re.compile(r'^\s*(\d\d\s+\d+\.\d\d\s+\d+\.\d\d)\s*$')


def byte_of(word, idx):
    """GOST byte idx (0..5, MSB first) of a 48-bit word."""
    return (word >> (8 * (5 - idx))) & 0xff


def gost_word(bytes6):
    v = 0
    for b in bytes6:
        v = (v << 8) | (b & 0xff)
    return v & MASK


def digit(x):
    """Round a float token value to its single printed decimal digit."""
    d = int(round(float(x)))
    if not 0 <= d <= 9:
        raise ValueError('value %r is not a single decimal digit' % x)
    return d


def emit(tokens, bound, obj, zero=()):
    """Return (override_dict, meta) for one token program + DO bound.

    The override dict contains ONLY runtime instruction words, data weight
    cells, descriptor and ZERO-seeded GOST words.  X/Y digits are never baked
    into the GOST words here.
    """
    vals = interpret(tokens)
    xd = digit(vals['x'])
    addd = digit(vals['add'])
    yd = xd + addd
    if yd > 9:
        raise ValueError('Y=%d exceeds one printed digit' % yd)
    if bound not in (5, 6):
        raise ValueError('gate bounds are 5 and 6')
    tens, units = cg.digit_bytes(bound)   # 6->(2,1), 5->(1,5)

    # GOST words with ZERO at the X/Y digit positions.
    g1 = gost_word([0, 1, 15, 0, 14, 0])   # '01 0.0' : byte3=0 (X seeded zero)
    g2 = gost_word([0, 15, 0, 14, 0, 0])   # '0 0.00' : byte2=0 (Y seeded zero)

    # data weights (raw byte additions, no inter-byte carry for small values)
    nt = (tens << 40) & MASK
    nu = ((units - 1) << 32) & MASK        # word1 byte1 seeded 1
    xw1 = (xd << 16) & MASK                # word1 byte3
    xw2 = (xd << 24) & MASK                # word2 byte2 : X contribution to Y
    aw2 = (addd << 24) & MASK              # word2 byte2 : addend contribution

    # runtime instruction words (two halfword instructions per 48-bit word)
    words = {
        9:  emit48(XTA, A_G1, ARX, A_NT),    # ACC = G1 + N-tens
        10: emit48(ARX, A_NU, STO, A_G1),    # ACC += N-units; G1 = ACC
        11: emit48(XTA, A_G1, ARX, A_XW1),   # ACC = G1 + X weight (byte3)
        12: emit48(STO, A_G1, XTA, A_G2),    # G1 = ACC; ACC = G2
        13: emit48(ARX, A_XW2, ARX, A_AW2),  # ACC += X + addend (Y, byte2)
        14: emit48(STO, A_G2, STO, A_G2),    # G2 = ACC (redundant store is safe)
        15: OBJ12,                           # *64 2004 : print via descriptor
        16: RET,                             # uj 0(15)
    }

    ov = {
        0o25: obj[0o25], 0o26: obj[0o26],    # proven descriptor pair
        0o27: g1, 0o30: g2,                  # ZERO-seeded GOST words
        0o31: obj[0o31],                     # proven GOST tail / EOF
        0o41: nt, 0o42: nu, 0o43: xw1,
        0o32: xw2, 0o33: aw2,
    }
    for k, v in words.items():
        ov[k] = v & MASK
    for k in zero:
        ov[k] = 0
    meta = dict(x=xd, add=addd, y=yd, bound=bound, tens=tens,
                units=units, g1=g1, g2=g2, words=dict(words),
                data=dict(DATA_SLOTS), addresses=dict(
                    g1=A_G1, g2=A_G2, nt=A_NT, nu=A_NU, xw1=A_XW1,
                    xw2=A_XW2, aw2=A_AW2))
    return ov, meta


def tens_disp(tens_word):
    return byte_of(tens_word, 0)


def printed(out):
    for s in out.splitlines():
        if 'TRANS' in s:
            continue
        m = LINE_RE.match(s)
        if m:
            return ' '.join(m.group(1).split())
    return None


def dump_body(d, tag):
    """Read back the installed body zone from the disk copy, return decoded words."""
    env = dict(os.environ, HOME=str(d / 'home'), BESM6_PATH=str(d / 'disks'))
    out = d / ('readback_%s.bin' % tag)
    r = subprocess.run(
        [str(BESMTOOL), 'dump', '2048', '--start=0%o' % (N + 1), '--length=1',
         '--to-file=%s' % out.name], cwd=d, env=env,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
    if r.returncode:
        raise SystemExit('FAIL dump %s: %s' % (tag, r.stdout.decode('utf-8', 'replace')[:300]))
    raw = out.read_bytes()
    words = [int.from_bytes(raw[i:i + 6], 'big') for i in range(0, len(raw) - 5, 6)]
    return words


def make_case(name, o412, tail, obj, ov, keep=True, timeout=120, note=''):
    d = CASES / name
    if d.exists():
        shutil.rmtree(d)
    (d / 'disks').mkdir(parents=True)
    (d / 'home').mkdir(parents=True)
    for f in ('2048', '2053', '2099'):
        shutil.copy(SHARE / f, d / 'disks' / f)

    images = m35.build_images(o412, tail, obj, bound=6, zero=())
    # override build_images' bound stream fully with our own override dict
    body = [0] * 1024
    body[0:19] = o412[16:35]
    body[19:1024] = tail[0:1005]
    for k, v in ov.items():
        body[k] = v & MASK
    cat = o412[0:16] + [0] * 1008
    z2 = [0] * 1024
    for i, w in enumerate(o412[35:410]):
        z2[526 + i] = w
    images = {'cat': cat, 'body': body, 'z2': z2, 'zero': [0] * 1024}

    for key, words in images.items():
        (d / (key + '.bin')).write_bytes(m35.wb6(words))
    (d / 'overrides.txt').write_text(''.join(
        'body[%-3o] RAM %04o = %016o  bytes=%s\n' % (
            k, 0o1757 + k, v & MASK,
            ' '.join('%2d' % byte_of(v, i) for i in range(6)))
        for k, v in sorted(ov.items())))

    env = dict(os.environ, HOME=str(d / 'home'), BESM6_PATH=str(d / 'disks'))
    zones = [(N, 'cat'), (N + 1, 'body'), (N + 2, 'z2')]
    zones += [(N + i, 'zero') for i in range(3, 41)]
    for z, key in zones:
        r = subprocess.run(
            [str(BESMTOOL), 'write', '2048', '--start=0%o' % z,
             '--from-file=%s.bin' % key], cwd=d, env=env,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120)
        if r.returncode:
            raise SystemExit('FAIL write %o: %s' %
                             (z, r.stdout.decode('utf-8', 'replace')[:300]))

    # PRE-RUN evidence: read back GOST words from the installed disk copy.
    pre = dump_body(d, 'pre')
    (EVID / (name + '_pre.txt')).write_text(
        'case=%s note=%s\nPRE-RUN installed GOST words (from disk copy):\n'
        '  body[0o27] RAM %04o = %016o bytes(dec)=%s\n'
        '  body[0o30] RAM %04o = %016o bytes(dec)=%s\n'
        '  X digit byte (body[0o27] byte3) = %d\n'
        '  Y digit byte (body[0o30] byte2) = %d\n' % (
            name, note, A_G1, pre[0o27] & MASK,
            [byte_of(pre[0o27], i) for i in range(6)],
            A_G2, pre[0o30] & MASK, [byte_of(pre[0o30], i) for i in range(6)],
            byte_of(pre[0o27], 3), byte_of(pre[0o30], 2)))

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
    return dict(name=name, rc=rc, printed=got, end=end,
                pre_g1=pre[0o27] & MASK, pre_g2=pre[0o30] & MASK,
                pre_x=byte_of(pre[0o27], 3), pre_y=byte_of(pre[0o30], 2))


def load_fixtures():
    for f in (DISPAK, BESMTOOL, REPO / 'src/newcomp/O412C.FTN',
              REPO / 'tests/plan-f77/69-full-emitted-body/o412d_words.hex',
              REPO / 'tests/plan-f77/65-m80-install/ovl_our.hex',
              SHARE / '2048', SHARE / '2053', SHARE / '2099'):
        if not Path(f).exists():
            raise SystemExit('FAIL missing %s' % f)
    o412 = m35.parse_o412c()
    tail = m35.words_hex(REPO / 'tests/plan-f77/69-full-emitted-body/o412d_words.hex')
    obj = m35.words_hex(REPO / 'tests/plan-f77/65-m80-install/ovl_our.hex')
    if len(tail) != 1005 or len(obj) != 1024:
        raise SystemExit('FAIL bad fixtures')
    return o412, tail, obj


CASESPEC = [
    # name, tokens, bound, zero-body-words, want
    ('x1_add2',   tokens_for(1, 2), 6, (),       '21 1.00 3.00'),
    ('x2_add2',   tokens_for(2, 2), 6, (),       '21 2.00 4.00'),
    ('x2_add3',   tokens_for(2, 3), 6, (),       '21 2.00 5.00'),
    ('x1_add2_r', tokens_for(1, 2), 6, (),       '21 1.00 3.00'),
    ('zero_x_code', tokens_for(2, 2), 6, (11,),  '21 0.00 4.00'),
    ('zero_y_code', tokens_for(2, 2), 6, (13,),  '21 2.00 0.00'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--only', default=','.join(c[0] for c in CASESPEC))
    ap.add_argument('--keep', action='store_true',
                    help='retain disk copies under cases/ (default: evidence only)')
    args = ap.parse_args()
    o412, tail, obj = load_fixtures()
    print('workspace:', WS)
    print('N=%04o  XTA=%06o ARX=%06o STO=%06o  G1=%04o G2=%04o' %
          (N, XTA, ARX, STO, A_G1, A_G2))

    results = []
    for name, tokens, bound, zero, want in CASESPEC:
        if name not in [c.strip() for c in args.only.split(',')]:
            continue
        ov, meta = emit(tokens, bound, obj, zero=zero)
        res = make_case(name, o412, tail, obj, ov, keep=args.keep,
                        note='X=%d add=%d Y=%d bound=%d zero=%s' % (
                            meta['x'], meta['add'], meta['y'], bound, list(zero)))
        good = (res['printed'] == want) and res['end'] and \
               res['pre_x'] == 0 and res['pre_y'] == 0
        results.append(dict(case=name, want=want, got=res['printed'],
                            end=res['end'], pre_x=res['pre_x'],
                            pre_y=res['pre_y'], ok=good))
        print('%-12s X=%d add=%d Y=%d zero=%-6s pre_x=%d pre_y=%d '
              'printed=%-14r want=%-14r end=%s %s' % (
                  name, meta['x'], meta['add'], meta['y'], list(zero),
                  res['pre_x'], res['pre_y'], res['printed'], want,
                  res['end'], 'OK' if good else 'FAIL'), flush=True)

    (WS / 'results.json').write_text(
        __import__('json').dumps(results, indent=2))
    ok = bool(results) and all(r['ok'] for r in results)
    print('VERDICT:', 'PASS' if ok else 'FAIL')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
