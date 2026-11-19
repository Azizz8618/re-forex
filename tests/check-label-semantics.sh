#!/usr/bin/env bash
# СТРОГАЯ проверка семантики имён в исходниках МАДЛЕН: src/*.mad и src/lib21/*.mad.
#
# Проверки (любая находка = FAIL):
#   1. АВТО     — автосгенерированные метки
#                (L[0-9]{4,6} | W[0-9]{3,5} | WT[0-9]{3,5} | D[0-9]{4,5} | [A-Z]L[0-9]{4,5}) :
#   2. TEXT     — TEXT-константа с «нумерованным» именем метки (T### / WT### / TXT##…).
#                Проверяется только отсутствие нумерованных паттернов, как разрешено.
#   3. ОКТАЛ+   — восьмеричное смещение массива +N B в операнде (ожидается десятичное +N).
#   4. ДЛИННЫХ  — имя длиннее 6 символов (как в check-label-length.sh).
#   5. КОЛЛИЗИЙ — разные имена с одинаковыми первыми 6 символами (там же).
#
# Устойчивость к отсутствующим файлам: файлы берутся по glob, пропавший между
# glob и чтением файл печатается как «—» и не считается провалом; при полном
# отсутствии исходников проверка откладывается (exit 0).
# Выход: 0 — нарушений нет (или проверка отложена), 1 — найдены нарушения.
set -u

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd) || exit 1
cd "$ROOT" || exit 1

python3 - <<'PY'
import glob
import re
import sys
from collections import defaultdict

FILES = sorted(set(glob.glob('src/*.mad') + glob.glob('src/lib21/*.mad')))

# 1. Автосгенерированные метки — регулярка задана ТОЧНО по ТЗ.
AUTO = re.compile(r'^\s*(L[0-9]{4,6}|W[0-9]{3,5}|WT[0-9]{3,5}|D[0-9]{4,5}|[A-Z]L[0-9]{4,5})\s*:')
# 4/5. Метки и EQU — как в check-label-length.sh (внешние NAME:,SUBP, — не метки).
LABEL = re.compile(r'^([A-Za-z0-9_]+):\s')
EQU = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*)\s*,\s*EQU\b')
# 2. Нумерованное имя TEXT-константы в начале строки.
TEXT_NUM = re.compile(r'^\s*(WT[0-9]{3}|T[0-9]{3}|TXT[0-9]+)\s*:')
# 3. Восьмеричное смещение +N B в операнде.
OCTAL_PLUS = re.compile(r'\+[0-7]+[bB]')
COMMENT_LINE = re.compile(r'^\s*[Сс;]')


def row(*cells):
    print('%-28s | %5s | %5s | %6s | %7s | %8s' % cells)


print('ПРОВЕРКА СЕМАНТИКИ ИМЁН: src/*.mad + src/lib21/*.mad')
row('ФАЙЛ', 'АВТО', 'TEXT', 'ОКТАЛ+', 'ДЛИННЫХ', 'КОЛЛИЗИЙ')
print('-' * 76)

total = dict(auto=0, text=0, oct=0, long=0, coll=0)
details = defaultdict(list)

for f in FILES:
    try:
        with open(f, encoding='utf-8', errors='replace') as fh:
            lines = fh.read().splitlines()
    except OSError as e:
        print('ПРОПУЩЕН %s: %s' % (f, e))
        row(f, '—', '—', '—', '—', '— (нет файла)')
        continue

    auto_hits, text_hits, oct_hits = [], [], []
    names = defaultdict(list)

    for no, line in enumerate(lines, 1):
        m = AUTO.match(line)
        if m:
            auto_hits.append((no, m.group(1)))

        if not COMMENT_LINE.match(line):
            for rx in (LABEL, EQU):
                mm = rx.match(line)
                if mm:
                    names[mm.group(1)].append(no)

        if ',TEXT,' in line:
            tm = TEXT_NUM.match(line)
            if tm:
                text_hits.append((no, tm.group(1)))

        if COMMENT_LINE.match(line):
            continue
        # Тело строки до встроенного комментария ('.' или ';').
        code = re.split(r'[.;]', line, maxsplit=1)[0]
        for om in OCTAL_PLUS.finditer(code):
            oct_hits.append((no, om.group(0)))

    long_names = [(n, v) for n, v in names.items() if len(n) > 6]
    pref = defaultdict(list)
    for n in names:
        pref[n[:6]].append(n)
    collisions = {p: ns for p, ns in pref.items() if len(ns) > 1}

    total['auto'] += len(auto_hits)
    total['text'] += len(text_hits)
    total['oct'] += len(oct_hits)
    total['long'] += len(long_names)
    total['coll'] += len(collisions)

    for no, name in auto_hits:
        details['AUTO'].append('%s:%d:%s' % (f, no, name))
    for no, name in text_hits:
        details['TEXT'].append('%s:%d:%s' % (f, no, name))
    for no, tok in oct_hits:
        details['ОКТАЛ+'].append('%s:%d:%s' % (f, no, tok))
    for n, v in long_names:
        details['ДЛИННЫХ'].append('%s:%s (строки %s)' % (f, n, v[:5]))
    for p, ns in collisions.items():
        details['КОЛЛИЗИЙ'].append('%s:%r: %s' % (f, p, sorted(ns)))

    row(f, len(auto_hits), len(text_hits), len(oct_hits), len(long_names), len(collisions))

print('-' * 76)
row('ИТОГО', total['auto'], total['text'], total['oct'], total['long'], total['coll'])
print()

fail = False
for key in ('AUTO', 'TEXT', 'ОКТАЛ+', 'ДЛИННЫХ', 'КОЛЛИЗИЙ'):
    items = details.get(key, [])
    if items:
        fail = True
        print('FAIL [%s]: %d' % (key, len(items)))
        for it in items:
            print('  ' + it)
    else:
        print('OK   [%s]: 0' % key)

if not FILES:
    print('НЕТ ФАЙЛОВ src/*.mad и src/lib21/*.mad — проверка отложена')
    sys.exit(0)
if fail:
    print('\nFAIL: нарушения семантики имён найдены (см. перечисления выше)')
    sys.exit(1)
print('\nOK: нарушений семантики имён не найдено')
sys.exit(0)
PY
exit $?
