#!/usr/bin/env bash
# СТРОГАЯ проверка: каждая текстовая константа в src/*.mad и src/lib21/*.mad
# обязана иметь расшифровку в комментарии с указанием кодировки.
#
# Что считается текстовой константой (маркеры из задания):
#   ,TEXT,   8H   nH   =6H   ,GOST,   ,ISO,   ,UPP,   =:...   и кавычки '...' / <<...>>.
# Для каждой такой строки требуется nearby-комментарий:
#   - встроенный после ';' или '.', либо
#   - целострочный (первый непробельный символ 'С' / ';' / '.' / 'C*'),
#   - либо расшифровка строки, на которую ссылается операнд (,GOST,TL0019 -> TL0019).
#     (идентификатор, определённый в том же файле с DEKOD-аннотацией, считается расшифрованным)
# Комментарий обязан содержать:
#   1) ключевое слово кодировки: GOST|ISO|TEXT|УПП|UPP|KOI|ITM|COSY
#   2) непустую расшифровку в кавычках '...' или <<...>>
#   (схема аннотаций `DEKOD GOST '...' / TEXT '...' / ISO '...'`).
#
# Отдельно проверяются CONTROL-константы:
#   LO*SYN, LO*GEN, FOREX, OCTTDEC, LOADANGO, DATAPR*, COREX,
#   месяцы DATAPR, INPUT/OUTPUT, 4HABCD.
#
# Вывод: таблица «ФАЙЛ:СТРОКА | КОНСТАНТ | КОДИРОВКА | СТАТУС» и список FAIL.
# Устойчивость: отсутствующий/пустой файл -> строка «ОЖИДАЕТСЯ» (не FAIL).
# Выход: 0 — OK (или только ОЖИДАЕТСЯ), 1 — есть FAIL.
set -u

# Кириллические 'С'/'УПП' в regex — один символ; нужен UTF-8 locale.
if locale -a 2>/dev/null | grep -qiE '^(C\.utf8|C\.UTF-8)$'; then
    export LC_ALL=C.UTF-8
fi

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd) || exit 1
cd "$ROOT" || exit 1

LOG="$ROOT/logs/text_decoded_check.txt"
mkdir -p "$(dirname -- "$LOG")" || exit 1

exec python3 - "$ROOT" "$LOG" <<'PY'
import glob, os, re, sys

root, logpath = sys.argv[1], sys.argv[2]
os.chdir(root)

out = []
def emit(s=''):
    out.append(s)

# ---正则表达式---------------------------------------------------------------
ENC  = re.compile(r'GOST|ISO|TEXT|УПП|UPP|KOI|ITM|COSY', re.I)
QUOT = re.compile(r"'[^'\n]*'|<<[^>\n]*>>")
NH   = re.compile(r'(?<![A-Za-z0-9_])\d+H(?![A-Za-z_])')

def nonempty_quote(q):
    inner = q[1:-1] if q.startswith("'") else q[2:-2]
    return bool(re.search(r"[^\s.']", inner))

def has_decode(text):
    """Ключевое слово кодировки И непустая расшифровка в кавычках."""
    return bool(ENC.search(text)) and any(nonempty_quote(q) for q in QUOT.findall(text))

def split_comment(line):
    """(код, комментарий). Комментарий: ';' в любом месте, '.' перед пробелом/в конце,
    либо целострочный 'С'/'с'/';'/'.'/'C*' в поз.1."""
    s = line.lstrip()
    if s:
        ch = s[0]
        if ch in 'Сс;.' or (ch == 'C' and (len(s) == 1 or s[1] in '* \t')):
            return '', line
    idx = line.find(';')
    for m in re.finditer(r'\.', line):
        j = m.start()
        prev = line[j-1] if j > 0 else ' '
        nxt = line[j+1] if j+1 < len(line) else ' '
        if prev.isspace() and (nxt.isspace() or not (nxt.isalnum() or nxt == 'о')):
            idx = j if idx < 0 else min(idx, j)
            break
    if idx >= 0:
        return line[:idx], line[idx:]
    return line, ''

def is_candidate(code):
    u = code.upper()
    return (',TEXT,' in u or '=6H' in u or '8H' in u or ',GOST,' in u
            or ',ISO,' in u or ',UPP,' in u or '=:' in code
            or bool(NH.search(code)) or bool(QUOT.search(code)))

def defined_symbols(code):
    out = set()
    m = re.match(r'\s*([A-Za-z_][\w*#/]*)\s*:', code)
    if m:
        out.add(m.group(1).upper())
    for m in re.finditer(r'([A-Za-z_][\w*#/]*)\s*,\s*EQU\s*,', code, re.I):
        out.add(m.group(1).upper())
    return out

def operand_symbols(code):
    out = set()
    for m in re.finditer(r',\s*(?:GOST|ISO|UPP|TEXT|CONT|LOG|AUX|ASN|AOX|STX|BSS|OCT)\s*,\s*([A-Za-z_][\w*#/]*)', code, re.I):
        out.add(m.group(1).upper())
    return out

def constant_token(code):
    m = re.search(r',\s*(?:TEXT|GOST|ISO|UPP)\s*,\s*([^\s,;]+)', code, re.I)
    if m:
        tok = re.sub(r'^=?\d+H', '', m.group(1))
        if tok:
            return tok[:26]
    m = re.search(r'=?\d+H([^\s,;]*)', code)
    if m:
        return (m.group(1) or m.group(0))[:26]
    m = re.search(r'=:\s*([^\s,;]+)', code)
    if m:
        return m.group(1)[:26]
    m = QUOT.search(code)
    if m:
        return m.group(0)[:26]
    return code.strip()[:26]

def encoding_of(comment):
    keys = []
    for m in ENC.finditer(comment):
        k = m.group(0).upper()
        if k not in keys:
            keys.append(k)
    return '/'.join(keys) if keys else '—'

# ---Сбор файлов---------------------------------------------------------------
patterns = ('src/*.mad', 'src/lib21/*.mad')
files = []
for pat in patterns:
    got = sorted(glob.glob(pat))
    if not got:
        emit('ОЖИДАЕТСЯ: нет файлов по шаблону %s (проверка отложена)' % pat)
    files.extend(got)
files = sorted(set(files))

EXPECTED = ('src/FOREX_CORE.mad', 'src/FOREX_RUNTIME.mad',
            'src/LO_SYN.mad', 'src/LO_GEN.mad')
pending = 0
for f in EXPECTED:
    if not os.path.isfile(f) or os.path.getsize(f) == 0:
        emit('ОЖИДАЕТСЯ: %s (отсутствует или пуст)' % f)
        pending += 1
        if f in files:
            files.remove(f)

emit()
emit('ПРОВЕРКА РАСШИФРОВКИ ТЕКСТОВЫХ КОНСТАНТ (src/*.mad, src/lib21/*.mad)')
emit('Критерий: nearby-комментарий с кодировкой (GOST|ISO|TEXT|УПП|UPP|KOI|ITM|COSY)')
emit('          и непустой расшифровкой в кавычках \'...\' / <<...>> (DEKOD ...).')
emit('ФАЙЛ:СТРОКА | КОНСТАНТ | КОДИРОВКА | СТАТУС')
emit('------------------------------+----------------------------+----------+--------')

lines = {}
for f in files:
    with open(f, encoding='utf-8', errors='replace') as fh:
        lines[f] = fh.read().splitlines()

# Какие символы уже расшифрованы где-либо DEKOD-аннотацией (для ,GOST,TLxxxx).
decoded_defs = set()
for ls in lines.values():
    for ln in ls:
        code, cm = split_comment(ln)
        if has_decode(cm):
            decoded_defs |= defined_symbols(code)

rows = []
fails = []
n_ok = n_pending = 0

for f in files:
    if not lines[f]:
        emit('%-28s | %-24s | %-8s | ОЖИДАЕТСЯ (пуст)' % (f, '—', '—'))
        n_pending += 1
        continue
    for i, ln in enumerate(lines[f], 1):
        code, cm = split_comment(ln)
        if not is_candidate(code):
            continue
        status = ''
        enc = encoding_of(cm)
        if has_decode(cm):
            status = 'OK'
        else:
            # расшифровка на соседних комментарных строках (±2)
            near = False
            for j in (i-2, i-1, i+1, i+2):
                if 0 <= j-1 < len(lines[f]) and has_decode(split_comment(lines[f][j-1])[1]):
                    near = True
                    break
            if near:
                status = 'OK (рядом)'
            else:
                ops = operand_symbols(code) & decoded_defs
                if ops:
                    status = 'OK (def:' + sorted(ops)[0] + ')'
                else:
                    status = 'FAIL'
        tok = constant_token(code) or '?'
        rows.append((f, i, tok, enc, status))
        if status == 'FAIL':
            fails.append((f, i, tok, ln.rstrip()))
            n_ok += 0
        elif status.startswith('OK'):
            n_ok += 1
        else:
            n_pending += 1

for f, i, tok, enc, status in rows:
    mark = '' if status == 'FAIL' else ''
    emit('%-28s | %-24s | %-8s | %s%s' % ('%s:%d' % (f, i), tok, enc, status, mark))

emit('------------------------------+----------------------------+----------+--------')
emit('ИТОГО констант: %d  OK: %d  FAIL: %d  ОЖИДАЕТСЯ: %d' %
     (len(rows), n_ok, len(fails), n_pending))

# ---CONTROL-константы-----------------------------------------------------------
emit()
emit('CONTROL-КОНСТАНТЫ (должны иметь DEKOD-расшифровку)')
emit('ФАЙЛ:СТРОКА | КОНСТАНТ | КОДИРОВКА | СТАТУС')
emit('------------------------------+----------------------------+----------+--------')

CONTROL = [
    ('LO*SYN',   r'LO\s*\*\s*SYN'),
    ('LO*GEN',   r'LO\s*\*\s*GEN'),
    ('FOREX',    r'\bFOREX\*?\b'),
    ('OCTTDEC',  r'\bOCTTDEC\b'),
    ('LOADANGO', r'\bLOADANGO\b'),
    ('DATAPR*',  r'\bDATAPR\s*\*'),
    ('COREX',    r'\bCOREX\b'),
    ('INPUT',    r'\bINPUT\b'),
    ('OUTPUT',   r'\bOUTPUT\b'),
    ('4HABCD',   r'\b4HABCD\b'),
]
# Месяцы DATAPR — по кириллическим написаниям в DEKOD-аннотациях
# FOREX_RUNTIME.mad (TL0010/TL0012/TL0016/TL0020/TL0022/TL0023/TL0024).
# 'Я' вместо 'Й' — в источнике 'МАЯ' = «МАЙ».
MONTHS = [
    ('DATAPR:ЯНВ', 'ЯНВ'),
    ('DATAPR:ФЕВ', 'ФЕВ'),
    ('DATAPR:МАР', 'МАР'),
    ('DATAPR:АПР', 'АПР'),
    ('DATAPR:МАЙ', 'МАЯ'),
    ('DATAPR:ИЮН', 'ИЮН'),
    ('DATAPR:ИЮЛ', 'ИЮЛ'),
    ('DATAPR:АВГ', 'АВГ'),
    ('DATAPR:СЕН', 'СЕН'),
    ('DATAPR:ОКТ', 'ОКТ'),
    ('DATAPR:НОЯ', 'НОЯ'),
    ('DATAPR:ДЕК', 'ДЕК'),
]

n_ctrl_fail = 0
for name, pattern in CONTROL + MONTHS:
    rx = re.compile(pattern, re.I)
    found_ok = found_any = None
    for f in files:
        for i, ln in enumerate(lines[f], 1):
            if not rx.search(ln):
                continue
            if found_any is None:
                found_any = (f, i, ln)
            code, cm = split_comment(ln)
            if not (has_decode(cm) or has_decode(ln)):
                continue
            cand = (f, i, ln, encoding_of(cm if has_decode(cm) else ln))
            # Предпочитаем явную DEKOD-аннотацию перед просто «ISO '231'».
            if 'DEKOD' in ln.upper():
                found_ok = cand
                break
            if found_ok is None:
                found_ok = cand
        if found_ok and 'DEKOD' in found_ok[2].upper():
            break
    if found_ok:
        f, i, ln, enc = found_ok
        emit('%-28s | %-24s | %-8s | OK' % ('%s:%d' % (f, i), name, enc))
    elif found_any:
        f, i, ln = found_any
        emit('%-28s | %-24s | %-8s | FAIL (нет DEKOD)' % ('%s:%d' % (f, i), name, '—'))
        n_ctrl_fail += 1
    else:
        emit('%-28s | %-24s | %-8s | ОЖИДАЕТСЯ (не найден)' % ('—', name, '—'))

emit('------------------------------+----------------------------+----------+--------')

# ---Детальный список FAIL------------------------------------------------------
emit()
if fails:
    emit('СПИСОК FAIL (конкретные файлы:строки):')
    for f, i, tok, ln in fails:
        emit('  %s:%d  [%s]  %s' % (f, i, tok, ln[:110]))
    emit()
    emit('FAIL: у %d текстовых констант нет расшифровки с кодировкой.' % len(fails))
else:
    emit('OK: все найденные текстовые константы имеют расшифровку с кодировкой.')

text = '\n'.join(out) + '\n'
sys.stdout.write(text)
try:
    with open(logpath, 'w', encoding='utf-8') as fh:
        fh.write(text)
except OSError as e:
    sys.stderr.write('Не удалось записать лог %s: %s\n' % (logpath, e))

sys.exit(1 if (fails or n_ctrl_fail) else 0)
PY
