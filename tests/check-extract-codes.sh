#!/usr/bin/env bash
# Проверка: каждый экстракод с информационным словом в аннотированных
# МАДЛЕН-текстах (src/*.mad, src/lib21/*.mad) имеет встроенный комментарий-
# расшифровку. Источники (по приоритету): rukava.be, затем книга Тюрина 1985.
#
# Ожидаемый вид комментария:
#   ". Э50 0131 = ... [rukava.be:2999]"  — расшифровка по rukava.be
#   ". Э57 1263 = ..., стр.264 [tyurin1985]" — расшифровка по Тюрину
#   ". Э57 6 = НЕ НАЙДЕНО в rukava.be" — нет ни в одном источнике
#
# Отчёт: logs/extract_codes_check.txt
# Выход: 0 — все вхождения прокомментированы, 1 — есть пропуски/неверные источники.
set -u

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd) || exit 1
cd "$ROOT" || exit 1

REPORT="$ROOT/logs/extract_codes_check.txt"

python3 - "$ROOT" "$REPORT" <<'PY'
import re
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
report = Path(sys.argv[2])
sys.path.insert(0, str(root / 'tools'))
import extract_codes as ec  # noqa: E402

table = ec.parse_table()
tyurin = ec.load_tyurin()
rows = ec.scan_sources(root / 'src', table, tyurin, 'all')
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
w('Источники: rukava.be разд.1.4 (parse: tools/extract_codes.py); '
  'Тюрин-1985 (docs/tyurin1985/extract-codes.json); приоритет rukava.be > tyurin1985')
w('')

seen = set()
pairs_seen = set()
missing = []
wrong_source = []
by_source = Counter()
for r in rows:
    key = (r['file'], r['line'], r['code'], r['info'])
    if key in seen:
        continue
    seen.add(key)
    r['file'] = str(r['file']).replace(str(root) + '/', '')
    line = line_of(root / r['file'], r['line'])
    marker = f". {r['code']} {r['info']} = "
    ok = marker in line
    src = r['source']
    pair_key = (r['code'], r['info'])
    if pair_key not in pairs_seen:
        pairs_seen.add(pair_key)
        by_source[src] += 1
    # Проверяем, что комментарий соответствует найденному источнику.
    if ok:
        if src == 'rukava.be' and f"[{r['source_line']}]" not in line:
            wrong_source.append((r['file'], r['line'], r['code'], r['info'], 'rukava.be'))
        elif src == 'tyurin1985' and '[tyurin1985]' not in line:
            wrong_source.append((r['file'], r['line'], r['code'], r['info'], 'tyurin1985'))
        elif src is None and 'НЕ НАЙДЕНО в rukava.be' not in line:
            wrong_source.append((r['file'], r['line'], r['code'], r['info'], 'нет источника'))
    if not ok:
        missing.append((r['file'], r['line'], r['code'], r['info']))
    status = 'OK' if ok else 'FAIL'
    label = src or 'не найдено'
    w(f"{status:4} {r['file']}:{r['line']}: {r['code']} {r['info']} "
      f"-> {(r['description'] or '—')[:60]} [{label}]")

w('')
w(f'Вхождений: {len(seen)}')
w(f'Уникальных пар: {len(pairs_seen)}')
w(f'Расшифровано по rukava.be: {by_source["rukava.be"]}')
w(f'Расшифровано по Тюрину-1985: {by_source["tyurin1985"]}')
w(f'Не расшифровано ни в одном источнике (помечено явно): {by_source[None]}')
w(f'Без комментария-расшифровки: {len(missing)}')
w(f'Комментарий с неверной ссылкой на источник: {len(wrong_source)}')
if missing:
    w('')
    w('ПРОПУСКИ:')
    for f, n, c, i in missing:
        w(f'  {f}:{n}: {c} {i}')
if wrong_source:
    w('')
    w('НЕСООТВЕТСТВИЕ ИСТОЧНИКА:')
    for f, n, c, i, s in wrong_source:
        w(f'  {f}:{n}: {c} {i} — ожидался {s}')
if not missing and not wrong_source:
    w('OK: все экстракоды с информационным словом имеют корректный комментарий-расшифровку')
else:
    w('FAIL: часть комментариев отсутствует или ссылается на неверный источник')

report.write_text('\n'.join(out) + '\n', encoding='utf-8')
print(f'Отчёт: {report}')
print(out[-1])
sys.exit(1 if (missing or wrong_source) else 0)
PY
exit $?
