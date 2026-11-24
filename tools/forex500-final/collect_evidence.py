#!/usr/bin/env python3
"""Collect B5 decisive-gate evidence into evidence/gates_b5.json (local only)."""
import hashlib, json
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
RUNS = WS / 'build/runs'
CASES = ['B5X_A', 'B5X_B', 'B5X_PATCH', 'B5X_RESTORE', 'B5X_PARENS']
EXPECT = {'B5X_A': '-0011.50', 'B5X_B': '-0006.50',
          'B5X_PATCH': '-0011.60', 'B5X_RESTORE': '-0011.50',
          'B5X_PARENS': '-0016.00'}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest() if Path(p).is_file() else None


def prn21(p):
    if not Path(p).is_file():
        return None
    for line in Path(p).read_text(encoding='utf-8', errors='replace').splitlines():
        if line.lstrip().startswith('21 '):
            return line.strip()
    return None


out = {'cases': {}, 'images': {}, 'decks': {}}
for img in ['2048_B5_A', '2048_B5_B', '2048_B5_PATCH', '2048_B5_RESTORE', '2048_base']:
    out['images'][img] = sha(WS / 'images' / img)
for dk in ['deck_exprA.b6', 'deck_exprB.b6', 'deck_parens.b6']:
    out['decks'][dk] = sha(WS / 'decks' / dk)
for c in CASES:
    vpath = RUNS / f'verdict_{c}.json'
    v = json.loads(vpath.read_text()) if vpath.is_file() else {}
    line = prn21(RUNS / f'localprn_{c}.txt')
    prn = (RUNS / f'localprn_{c}.txt').read_text(encoding='utf-8', errors='replace') \
        if (RUNS / f'localprn_{c}.txt').is_file() else ''
    out['cases'][c] = {
        'product_gate': v.get('product_gate'),
        'plumbing': v.get('plumbing'),
        'emulator_sha': v.get('emulator_sha'),
        'prn21': line,
        'prn_sha': sha(RUNS / f'localprn_{c}.txt'),
        'komets': 'КОНЕЦ ЗАДАЧИ' in prn,
        'expected': EXPECT[c],
        'match': bool(line and EXPECT[c] in line),
    }
out['invariants'] = {
    'image_A_eq_B': out['images']['2048_B5_A'] == out['images']['2048_B5_B'],
    'image_A_eq_RESTORE': out['images']['2048_B5_A'] == out['images']['2048_B5_RESTORE'],
    'image_PATCH_diff_A': out['images']['2048_B5_PATCH'] != out['images']['2048_B5_A'],
    'all_product_PASS': all(out['cases'][c]['product_gate'] == 'PASS' for c in CASES),
    'all_values_match': all(out['cases'][c]['match'] for c in CASES),
    'all_komets': all(out['cases'][c]['komets'] for c in CASES),
}
(WS / 'evidence/gates_b5.json').write_text(
    json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(out['invariants'], indent=2))
for c in CASES:
    print(c, out['cases'][c]['product_gate'], out['cases'][c]['prn21'])
