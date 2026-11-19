#!/usr/bin/env bash
# Проверка комментариев в аннотированных МАДЛЕН-текстах (src/*.mad, src/lib21/*.mad).
#
# КРИТИЧЕСКОЕ ПРАВИЛО: в ДИСПАКе экстракоды — только коды 050..077.
# Коды 020..047 (*20, *21, *33, *36, *46, *47 и др.) — обычные КОМАНДЫ БЭСМ-6
# по таблицам besm6tape.py / disbesm6.c; они НЕ требуют расшифровки из
# rukava.be или книги Тюрина.
#
# Ожидаемый вид комментария:
#   ". Э50 0131 = ... [rukava.be:2999]"           — экстракод по rukava.be
#   ". Э57 1263 = ..., стр.264 [tyurin1985]"      — экстракод по Тюрину
#   ". Э65 502 = НЕ НАЙДЕНО ни в rukava.be, ни в Тюрине-1985
#      (...; информационное слово — адрес/данные)" — экстракод без расшифровки
#   ". опк 36 (втбрз) 7417 = КОМАНДА БЭСМ-6 «втбрз», не экстракод
#      [besm6tape.py:45,49]"                       — команда, НЕ экстракод
#
# Старая формулировка "НЕ НАЙДЕНО в rukava.be" считается FAIL.
# Отчёт: logs/extract_codes_check.txt
# Выход: 0 — все вхождения корректно помечены, 1 — есть пропуски/ошибки.
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
NEW_NOT_FOUND = 'ни в rukava.be, ни в Тюрине-1985'
STALE_NOT_FOUND = 'НЕ НАЙДЕНО в rukava.be'
ADDR_DATA = 'информационное слово — адрес/данные'
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
w('ПРОВЕРКА КОММЕНТАРИЕВ: ЭКСТРАКОДЫ (050..077) И КОМАНДЫ (020..047)')
w('КРИТИЧЕСКОЕ ПРАВИЛО: коды 020..047 (*20,*21,*33,*36,*46,*47 и др.) — КОМАНДЫ БЭСМ-6, НЕ экстракоды')
w('Источники расшифровок: rukava.be разд.1.4; Тюрин-1985; приоритет rukava.be > tyurin1985')
w('Команды: ". опк NN (мнемоника) <слово> = КОМАНДА БЭСМ-6 «...», не экстракод [таблица]" — без справочников')
w('Экстракоды без расшифровки: "НЕ НАЙДЕНО ни в rukava.be, ни в Тюрине-1985 (...)"')
w('')

# 0. Глобальная проверка: в исходниках не осталось команд, названных экстракодами.
STALE_CMD_RE = re.compile(
    r'\. ?Э(?:20|21|33|36|46|47)(?![0-7])|\.Э(?:20|21|33|36|46|47)'
    r'|экстракод \*(?:20|21|33|36|46|47)'
)
stale = []
sources = (sorted((root / 'src').glob('*.mad'))
           + sorted((root / 'src' / 'lib21').glob('*.mad')))
for path in sources:
    for no, line in enumerate(path.read_text(encoding='utf-8', errors='replace').splitlines(), 1):
        if STALE_CMD_RE.search(line):
            stale.append((str(path.relative_to(root)), no, line.strip()[:110]))
if stale:
    w('FAIL: команды 020..047 всё ещё помечены как экстракоды:')
    for f, n, t in stale:
        w(f'  {f}:{n}: {t}')
    w('')
else:
    w('OK: в исходниках нет команд 020..047, помеченных как экстракоды')
    w('')

seen = set()
pairs_seen = set()
missing = []
wrong_source = []
cmd_bad = []
by_source = Counter()
by_code = Counter()
n_commands = 0
n_extracts = 0

for r in rows:
    key = (r['file'], r['line'], r['code'], r['info'])
    if key in seen:
        continue
    seen.add(key)
    frel = str(r['file']).replace(str(root) + '/', '')
    line = line_of(root / frel, r['line'])
    kind = r['kind']
    by_code[r['code']] += 1
    status = 'OK'
    label = ''

    if kind == 'command':
        n_commands += 1
        norm = format(int(r['code'].lstrip('Э*'), 8), '02o')
        mnem = r['mnemonic']
        ref = r['command_ref']
        marker = f'. опк {norm} ({mnem})'
        ok = marker in line
        if ok:
            checks = ('КОМАНДА БЭСМ-6' in line and 'не экстракод' in line
                      and f'[{ref}]' in line)
            if not checks:
                ok = False
                cmd_bad.append((frel, r['line'], r['code'], r['info'],
                                'нет «КОМАНДА БЭСМ-6 … не экстракод [таблица]»'))
        if not ok:
            missing.append((frel, r['line'], r['code'], r['info']))
        label = f'КОМАНДА «{mnem}» [{ref}]'
        status = 'OK' if ok else 'FAIL'
        w(f"{status:4} {frel}:{r['line']}: опк {norm} {r['info']} -> {label}")
        continue

    if kind != 'extract':
        continue

    n_extracts += 1
    marker = f". {r['code']} {r['info']} = "
    ok = marker in line
    src = r['source']
    pair_key = (r['code'], r['info'])
    if pair_key not in pairs_seen:
        pairs_seen.add(pair_key)
        by_source[src] += 1
    if ok:
        if src == 'rukava.be' and f"[{r['source_line']}]" not in line:
            wrong_source.append((frel, r['line'], r['code'], r['info'], 'rukava.be'))
        elif src == 'tyurin1985' and '[tyurin1985]' not in line:
            wrong_source.append((frel, r['line'], r['code'], r['info'], 'tyurin1985'))
        elif src is None:
            # Экстракод без расшифровки: либо явная пометка ОБОИХ источников,
            # либо (для адреса/данных) пометка «информационное слово — адрес/данные».
            both = NEW_NOT_FOUND in line and STALE_NOT_FOUND not in line
            addr = ADDR_DATA in line and STALE_NOT_FOUND not in line
            if not (both or addr):
                wrong_source.append((frel, r['line'], r['code'], r['info'],
                                     'нет «ни в rukava.be, ни в Тюрине-1985» или «адрес/данные»'))
    if not ok:
        missing.append((frel, r['line'], r['code'], r['info']))
    status = 'OK' if ok else 'FAIL'
    label = src or 'адрес/данные' if ADDR_DATA in line else (src or 'не найдено')
    w(f"{status:4} {frel}:{r['line']}: {r['code']} {r['info']} "
      f"-> {(r['description'] or '—')[:60]} [{label}]")

w('')
w(f'Вхождений: {len(seen)} (команд 020..047: {n_commands}; экстракодов 050..077: {n_extracts})')
w(f'Уникальных пар экстракодов: {len(pairs_seen)}')
w(f'Расшифровано по rukava.be: {by_source["rukava.be"]}')
w(f'Расшифровано по Тюрину-1985: {by_source["tyurin1985"]}')
w(f'Экстракодов без расшифровки (помечено явно): {by_source[None]}')
w(f'Команд, помеченных как КОМАНДА БЭСМ-6: {n_commands - len(cmd_bad)}')
for code, count in sorted(by_code.items()):
    w(f'  {code}: {count}')

w(f'Без корректного комментария: {len(missing)}')
w(f'Неверная ссылка на источник: {len(wrong_source)}')
w(f'Неверная пометка команды: {len(cmd_bad)}')
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
if cmd_bad:
    w('')
    w('НЕВЕРНАЯ ПОМЕТКА КОМАНДЫ:')
    for f, n, c, i, s in cmd_bad:
        w(f'  {f}:{n}: {c} {i} — {s}')

fail = bool(missing or wrong_source or cmd_bad or stale)
if not fail:
    w('OK: команды 020..047 помечены как команды; экстракоды 050..077 имеют корректную расшифровку')
else:
    w('FAIL: часть комментариев отсутствует или неверна')
report.write_text('\n'.join(out) + '\n', encoding='utf-8')
print(f'Отчёт: {report}')
print(out[-1])
sys.exit(1 if fail else 0)
PY
exit $?
