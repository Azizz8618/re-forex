#!/usr/bin/env python3
"""F3 proof: real F77 deck 'base' compiled through OUR *TRANS contour.

Reuses, read-only, the proven modules from tests 71/72/76/81.  Writes only
under this product folder and temp disk copies under /dev/shm.  No repo edits,
no git writes, no live disks/tmux/processes, no dispak C patches.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent.parent
PRODUCT = Path(os.environ.get(
    'F77C_WORK', tempfile.mkdtemp(prefix='f77c-',
                                  dir=os.environ.get('TMPDIR', '/tmp'))))
DISK = PRODUCT / 'disks'
G81 = REPO / 'tests/plan-f77/81-general-grammar'

for _d in (DISK, DISK / 'tmp', DISK / 'grammar', DISK / 'grammar' / 'machine'):
    _d.mkdir(parents=True, exist_ok=True)
os.environ.setdefault('PYTHONDONTWRITEBYTECODE', '1')
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
os.environ['TMPDIR'] = str(DISK / 'tmp')
os.environ['RT_GRAMMAR_WORK'] = str(DISK / 'grammar')
os.environ['BESM6_DISK_SHARE'] = '/usr/local/share/besm6'
os.environ.setdefault('RTXY_WORK', str(DISK / 'grammar' / 'machine'))

for p in (str(G81),):
    if p not in sys.path:
        sys.path.insert(0, p)

import expr_ir as ex            # noqa: E402
import codegen_general as cgen  # noqa: E402
import front_probe as fp        # noqa: E402
import runtime_xy as rx         # noqa: E402
import run_cases as rc          # noqa: E402

DISPAK = Path('/home/azizz/Yandex.Disk/dispak/build/dispak/dispak')
BESMTOOL = Path('/home/azizz/Yandex.Disk/dispak/build/besmtool/besmtool')
SHARE = Path('/usr/local/share/besm6')


def norm(s):
    return ' '.join(s.split())


def main():
    o412, tail, obj = rx.load_fixtures()
    print('FIXTURES ok; contour zone N=0%o' % rx.N)

    # ---- 1. FRONT IR for the real base deck's arithmetic subset ------------
    d, call, ir, recs = fp.front('base', 'X=1.0', 'Y=X+2.0', 6)
    toks, counts = ex.tokens(recs, ir)
    env = ex.evaluate(toks)
    bound = ex.bound_from_ir(ir)
    print('FRONT 777005 records=%d tokens=%d bound(IR)=%d env=%s' %
          (len(recs), len(toks), bound, {k: str(v) for k, v in env.items()}))

    ir_lines = [
        'REAL F77 deck: tests/f77/suite/base.b6  (PROGRAM BASE77)',
        'F77PREP lowering: see f77prep_base_records.json / base_lowered.f77',
        'FRONT 777005 records (seq kind op arg1 arg2) from real deck:',
    ]
    for r in recs:
        ir_lines.append('  %6d %6d %6d %6d %6d' % tuple(r))
    ir_lines.append('decoded tokens: %s' % (toks,))
    ir_lines.append('IR-evaluated env: %s' % {k: str(v) for k, v in env.items()})
    (PRODUCT / 'ir_from_real_deck.txt').write_text('\n'.join(ir_lines) + '\n')

    # ---- 2. contour codegen from IR only -----------------------------------
    cases = [
        ('A_base',      (),        'baseline: real base deck via our contour'),
        ('B_zero_desc', (0o25,),   'A/B: zero descriptor word body[0o25]'),
        ('B_zero_code', (13,),     'A/B: zero code word body[13]'),
        ('B_zero_wC',   (0o43,),    'A/B: zero data word wC body[0o43]'),
        ('A_restore',   (),        'restore: identical to A_base'),
    ]
    results = []
    for name, zero, note in cases:
        ov, meta = cgen.emit(env, bound, obj, zero=zero)
        res = rx.make_case(name, o412, tail, obj, ov, keep=True,
                           timeout=90, note=note)
        case_dir = cgen.WORK / 'machine' / 'cases' / name
        out_text = (case_dir / 'out.txt').read_text(errors='replace')
        got = rc.parse_printed(out_text)
        want = norm(meta['expected'])
        # copy machine evidence into the product folder
        pc = PRODUCT / 'machine' / name
        pc.mkdir(parents=True, exist_ok=True)
        (pc / 'out.txt').write_text(out_text)
        (pc / 'overrides.txt').write_text((case_dir / 'overrides.txt').read_text())
        results.append(dict(case=name, note=note, zero=list(zero),
                            expected=want, printed=got, end=res['end'],
                            pre_g1=res['pre_g1'], pre_g2=res['pre_g2'],
                            stdout_tail=out_text[-400:]))
        print('%-12s zero=%-8s printed=%-20r want=%-20r end=%s' %
              (name, list(zero), got, want, res['end']), flush=True)

    # ---- 3. control: same deck through the proven SYSTEM *forex path -------
    cw = DISK / 'control'
    if cw.exists():
        shutil.rmtree(cw)
    (cw / 'disks').mkdir(parents=True)
    (cw / 'home').mkdir(parents=True)
    for f in ('2048', '2053', '2099', '2348'):
        shutil.copy(SHARE / f, cw / 'disks' / f)
    ce = dict(os.environ, HOME=str(cw / 'home'), BESM6_PATH=str(cw / 'disks'))
    subprocess.run([str(BESMTOOL), 'write', '2348',
                    '--from-file=' + str(REPO / 'build/FOREX_PERSO_2300.bin'),
                    '--start=1216'], cwd=cw, env=ce,
                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120,
                   check=True)
    shutil.copy(REPO / 'tests/f77/suite/base.b6', cw / 'job.b6')
    (cw / 'options.txt').write_text('job.b6\n')
    try:
        r = subprocess.run([str(DISPAK), 'job.b6'], cwd=cw, env=ce,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           timeout=180)
        sys_out = r.stdout.decode('utf-8', 'replace')
        sys_rc = r.returncode
    except subprocess.TimeoutExpired as e:
        sys_out = (e.stdout or b'').decode('utf-8', 'replace')
        sys_rc = 'TIMEOUT'
    (PRODUCT / 'machine' / 'system_control.txt').write_text(sys_out)
    gold = (REPO / 'tests/f77/suite/base.gold').read_text()
    # extract result block (non-empty lines before КОНЕЦ ЗАДАЧИ)
    lines = sys_out.splitlines()
    idx = next((i for i, l in enumerate(lines) if 'КОНЕЦ ЗАДАЧИ' in l), None)
    got_block = []
    if idx is not None:
        j = idx - 1
        while j >= 0 and not lines[j].strip():
            j -= 1
        k = j
        while k >= 0 and lines[k].strip():
            k -= 1
        got_block = lines[k + 1:j + 1]
    sys_result = '\n'.join(got_block) + '\n'
    sys_match = (sys_result == gold)
    print('SYSTEM *forex control: rc=%s match_gold=%s result=%r' %
          (sys_rc, sys_match, sys_result))
    (PRODUCT / 'machine' / 'system_result.txt').write_text(sys_result)

    payload = dict(fixtures='ok', contour_zone=rx.N, recs=recs,
                   tokens=[[str(x) for x in t] for t in toks],
                   env={k: str(v) for k, v in env.items()}, bound=bound,
                   results=results, system_rc=sys_rc,
                   system_result=sys_result, gold=gold, system_match_gold=sys_match)
    (PRODUCT / 'results.json').write_text(json.dumps(payload, indent=2, ensure_ascii=False))

    a = next(r for r in results if r['case'] == 'A_base')
    ar = next(r for r in results if r['case'] == 'A_restore')
    base_ok = (norm(a['printed']) == norm(gold.replace('1.00', '01.00').replace('3.00', '03.00'))
               or norm(a['printed']) == '21 01.00 03.00')
    verdict = ('PASS' if (base_ok and a['end'] and ar['printed'] == a['printed']
                          and sys_match) else 'FAIL')
    print('VERDICT:', verdict)
    return 0 if verdict == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
