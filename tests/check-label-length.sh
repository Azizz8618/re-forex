#!/usr/bin/env bash
# Проверка: все локальные метки и EQU в src/LO_SYN.mad имеют длину <= 6
# символов и уникальные первые 6 символов (МАДЛЕН различает только первые 6).
# Остальные .mad-файлы пока не переведены на 6-символьные имена и не проверяются.
set -u
cd "$(dirname "$0")/.." || exit 1

python3 - <<'PY'
import re
import sys
from collections import defaultdict
from pathlib import Path

path = Path('src/LO_SYN.mad')
# метка: имя, затем ':' и пробел (внешние объявления вида NAME:,SUBP, — не метки)
LABEL = re.compile(r'^([A-Za-z0-9_]+):\s')
EQU = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*)\s*,\s*EQU\b')

if not path.is_file():
    print(f'FAIL {path} отсутствует', file=sys.stderr)
    sys.exit(1)

names = defaultdict(list)
for no, line in enumerate(path.read_text(errors='replace').splitlines(), 1):
    if re.match(r'^\s*[Сс;]', line):
        continue
    for rx in (LABEL, EQU):
        m = rx.match(line)
        if m:
            names[m.group(1)].append(no)

long_names = [(n, v) for n, v in names.items() if len(n) > 6]
pref = defaultdict(list)
for n in names:
    pref[n[:6]].append(n)
collisions = {p: ns for p, ns in pref.items() if len(ns) > 1}
if long_names or collisions:
    print(f'FAIL {path}: длинных имён: {len(long_names)}, коллизий первых 6: {len(collisions)}', file=sys.stderr)
    for n, v in long_names[:20]:
        print(f'  LONG   {n!r} строки {v}', file=sys.stderr)
    for p, ns in list(collisions.items())[:20]:
        print(f'  PREFIX {p!r}: {ns}', file=sys.stderr)
    sys.exit(1)

print(f'OK {path}: {len(names)} символов, все <=6, коллизий первых 6 нет')
PY
exit $?
