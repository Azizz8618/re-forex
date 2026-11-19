#!/usr/bin/env bash
# Проверка: каждый экстракод с информационным словом в аннотированных
# МАДЛЕН-текстах (src/*.mad, src/lib21/*.mad) имеет встроенный комментарий-
# расшифровку вида ". Э50 0131 = ... [rukava.be:2999]" либо
# ". Э57 6 = НЕ НАЙДЕНО в rukava.be".
#
# Отчёт: logs/extract_codes_check.txt
# Выход: 0 — все вхождения прокомментированы, 1 — есть пропуски.
set -u

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd) || exit 1
cd "$ROOT" || exit 1

REPORT="$ROOT/logs/extract_codes_check.txt"

python3 - "$ROOT" "$REPORT" <<'PY'
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
report = Path(sys.argv[2])
sys.path.insert(0, str(root / 'tools'))
import extract_codes as ec  # noqa: E402

table = ec.parse_table()
rows = ec.scan_sources(root / 'src', table)
cache = {}

def line_of(path, number):
    key = (path, number)
    if key not in cache:
        lines = Path(path).read_text(encoding='utf-8', errors='replace').splitlines()
        cache[key] = lines[number - 1] if 0 < number <= len(lines) else ''
    return cache[key]

out = []
w = out.append
w('ПРОВЕРКА КОММЕНТАРИЕВ-РАСШИФРОВОК ЭКСТРАКОДОВ')
w('Источник: rukava.be, раздел 1.4 (parse: tools/extract_codes.py)')
w('')

seen = set()
missing = []
decoded = 0
notdecoded = 0
for r in rows:
    key = (r['file'], r['line'], r['code'], r['info'])
    if key in seen:
        continue
    seen.add(key)
    r['file'] = str(r['file']).replace(str(root) + '/', '')
    line = line_of(root / r['file'], r['line'])
    marker = f". {r['code']} {r['info']} = "
    ok = marker in line
    status = 'OK' if ok else 'FAIL'
    if r['description'] is not None:
        decoded += 1
    else:
        notdecoded += 1
    if not ok:
        missing.append((r['file'], r['line'], r['code'], r['info']))
    w(f"{status:4} {r['file']}:{r['line']}: {r['code']} {r['info']} "
      f"-> {r['description'] or 'не найдено в rukava.be'}")

w('')
w(f'Вхождений: {len(seen)}')
w(f'Расшифровано по rukava.be: {decoded}')
w(f'Не найдено в rukava.be (помечено явно): {notdecoded}')
w(f'Без комментария-расшифровки: {len(missing)}')
if missing:
    w('')
    w('ПРОПУСКИ:')
    for f, n, c, i in missing:
        w(f'  {f}:{n}: {c} {i}')
    w('FAIL: не у всех экстракодов есть комментарий-расшифровка')
else:
    w('OK: все экстракоды с информационным словом имеют комментарий-расшифровку')

report.write_text('\n'.join(out) + '\n', encoding='utf-8')
print(f'Отчёт: {report}')
print(out[-1])
sys.exit(1 if missing else 0)
PY
exit $?
