#!/usr/bin/env bash
# Проверка комментариев в аннотированных МАДЛЕН-текстах (src/*.mad, src/lib21/*.mad).
#
# КРИТИЧЕСКОЕ ПРАВИЛО: в ДИСПАКе экстракоды — только коды 050..077.
# Коды 020..047 (*20, *21, *33, *36, *46, *47 и др.) — обычные КОМАНДЫ БЭСМ-6;
# они НЕ требуют расшифровки из rukava.be или книги Тюрина.
#
# АВТОРИТЕТНОЕ УТОЧНЕНИЕ (2026-11-19): формат определяется 20-м разрядом
# полуслова (в 0-based это бит 19).  Наши слова имеют 20-й разряд=0 →
# «1-я структура ТО IX, 20-й разряд=0 (в 0-based это бит 19)».
# besm6tape.py:84 проверяет тот же разряд ((h >> 19) & 1), корректно.
# Прежняя формулировка «off-by-one, бит 20» была ошибкой нумерации.
#
# МНЕМОНИКИ В ИСХОДНИКАХ: *20→APX (сбр), *21→AUX (рзб), *33→EXT (увв),
# *36→ASN (сда); *46/*47 остаются (в МАДЛЕН имени нет, неиспользованные коды).
# opcode APX/AUX/EXT/ASN = 0x010000/0x011000/0x01b000/0x01e000 — те же биты,
# что у *20/*21/*33/*36 (disbesm6.c), машинное слово НЕ меняется.
# Имена «э20/э21/счп/соп/э47/втбрз» — внутренние заглушки дизассемблеров;
# «втбрз» — имя подпрограммы gens1.be, НЕ мнемоника opcode.
# Формулировки LONG, «Additional system call», «flush BRZ», «в LONG-формате
# stop/стоп» в активных комментариях НЕДОПУСТИМЫ.
#
# Ожидаемый вид комментария:
#   ". Э50 0131 = ... [rukava.be:2999]"           — экстракод по rukava.be
#   ". Э57 1263 = ..., стр.264 [tyurin1985]"      — экстракод по Тюрину
#   ". Э65 502 = НЕ НАЙДЕНО ни в rukava.be, ни в Тюрине-1985
#      (...; информационное слово — адрес/данные)" — экстракод без расшифровки
#   ". ASN: 4037B → N=0o37(31)=64−33 ⇒ ,ASN,64-33 — сдвиг ВЛЕВО на 33
#      [monitor80-re/chekjob/mvstack.asm:17; Besm6_Instruction_Set.md §6]" — ASN
#     (. опк 36 (...) = ASN (сда): ...; GATAD = N в форме 64+n ... — УСТАРЕЛО)
#
# АРГУМЕНТ ASN: ,ASN,64+N — сдвиг ВПРАВО, ,ASN,64−N — сдвиг ВЛЕВО;
#   N = EA[7:1] — младшие 7 разрядов адреса (Besm6_Instruction_Set.md §6),
#   а НЕ весь адрес.  Требуется явная формула для каждого вхождения.
#
# ЭКСТРАКОДЫ 060/070: класс по Besm6_Instruction_Set.md §6 —
#   060 = I/O control (input), 070 = Memory/register dump;
#   конкретное информационное слово не найдено — сохраняем пометку ОБОИХ
#   справочников и добавляем класс + контекстную интерпретацию слова.
#
# 033 В LO*GEN — STOP (2-я структура, Format 2), не EXT/увв; мнемоника `33`.
#
# КЛАССЫ АРГУМЕНТОВ 020/021 (запрос пользователя 2026-11-19: аргументы APX/AUX
# «нередко работают с текстом»).  Для КАЖДОГО из 307 вхождений APX/AUX
# проверяется явная интерпретация аргумента; класс считается по токену и его
# EQU-значению (``ec.classify_apx_aux_argument``), ожидаемая пометка —
# ``ec.apx_aux_argument_note``:
#   mask-word (text) — НЕ адрес: 8-символьное TEXT/ISO/GOST слово-маска
#     (OCT-слово 0160 3407 0160 34 [star%.masm:490], *0353B [paramt%.masm:365],
#     =6H'…' [edit%%%.asm:996], ETX*-литералы =6H/=:/=NNNN NNNN);
#   immediate-code   — код/счётчик в младших разрядах, не адрес
#     (AUX 25B/43B/44B в DATAPR/OCTTDEC, DV043=MONTHFI, DV044=DATE2);
#   address          — адрес слова-маски, НЕ адрес данных (AC153D, EX4254).
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
w('КРИТИЧЕСКОЕ ПРАВИЛО: коды 020..047 — КОМАНДЫ БЭСМ-6, НЕ экстракоды')
w('ФОРМАТ: ec.FORMAT_LABEL = ' + ec.FORMAT_LABEL + '; besm6tape.py:84 проверяет тот же разряд')
w('Источники расшифровок: rukava.be разд.1.4; Тюрин-1985; приоритет rukava.be > tyurin1985')
w('Команды: ". опк NN (' + ec.FORMAT_LABEL + ') = <мнёмоника> (...); аргумент ... [CmdSheet/disbesm6]"')
w('МНЕМОНИКИ: 020=APX (маска X); 021=AUX (маска X); 033=EXT (увв, привил. ОС), но в LO*GEN 033=STOP (Format 2, мнемоника `33`); 036=ASN (,ASN,64+N — вправо, ,ASN,64−N — влево; N=EA[7:1]); 046/047=*46/*47 (аргумент не интерпретируется)')
w('Запрещены: *20/*21/*33/*36 в коде, LONG, "Additional system call", "flush BRZ", "в LONG-формате stop/стоп", "втбрз"')
w('Экстракоды без расшифровки: "НЕ НАЙДЕНО ни в rukava.be, ни в Тюрине-1985 (...)"')
w('Классы экстракодов: Э60=I/O control (input), Э70=Memory/register dump, Э71=Debug output [Besm6_Instruction_Set.md §6] + контекст информационного слова')
w('')

# 0. Глобальная проверка: в исходниках не осталось команд, названных экстракодами.
STALE_CMD_RE = re.compile(
    r'\. ?Э(?:20|21|33|36|46|47)(?![0-7])|\.Э(?:20|21|33|36|46|47)'
    r'|экстракод \*(?:20|21|33|36|46|47)'
)
# Устаревшие интерпретации кодов (прежняя формулировка «off-by-one, бит 20»).
STALE_SHORT_RE = re.compile(
    r'опк (?:20|21|33|36|46|47) \((?:втбрз|мнемоника)'
    r'|группы LONG|LONG-формате stop|«втбрз»'
    r'|Additional system call|flush BRZ'
    r'|SHORT, бит20=0|\(SHORT, бит ?20'
)
# В коде более НЕ должно быть *20/*21/*33/*36 — только APX/AUX/EXT/ASN.
STALE_MNEM_RE = re.compile(r'\*(20|21|33|36)(?=,)')
EXPECTED_MNEMONIC = dict(ec.OPCODE_MNEMONICS)
EXPECTED_MNEMONIC['46'] = '*46'
EXPECTED_MNEMONIC['47'] = '*47'
stale = []
stale_short = []
stale_mnem = []
stale_033 = []
sources = (sorted((root / 'src').glob('*.mad'))
           + sorted((root / 'src' / 'lib21').glob('*.mad')))
for path in sources:
    for no, line in enumerate(path.read_text(encoding='utf-8', errors='replace').splitlines(), 1):
        if STALE_CMD_RE.search(line):
            stale.append((str(path.relative_to(root)), no, line.strip()[:110]))
        if STALE_SHORT_RE.search(line):
            stale_short.append((str(path.relative_to(root)), no, line.strip()[:110]))
        # только кодовая часть строки (до комментария)
        cut = re.search(r'\s+[.;]', line)
        code_part = line[:cut.start()] if cut else line
        if STALE_MNEM_RE.search(code_part):
            stale_mnem.append((str(path.relative_to(root)), no, line.strip()[:110]))
        # 033 в пользовательском генераторе кода — STOP (Format 2), не EXT/увв.
        if path.name == 'LO_GEN.mad':
            if re.search(r'(?<![A-Za-z0-9_])EXT\s*,', code_part):
                stale_033.append((str(path.relative_to(root)), no,
                                  'EXT — привилегированная команда ОС; в LO*GEN 033 = STOP'))
            if re.search(r',\s*33\s*,', code_part) and 'STOP' not in line:
                stale_033.append((str(path.relative_to(root)), no,
                                  'нет пометки STOP (Format 2)'))
if stale:
    w('FAIL: команды 020..047 всё ещё помечены как экстракоды:')
    for f, n, t in stale:
        w(f'  {f}:{n}: {t}')
    w('')
else:
    w('OK: в исходниках нет команд 020..047, помеченных как экстракоды')
    w('')
if stale_short:
    w('FAIL: в исходниках остались LONG/заглушечные формулировки (бит 19, besm6tape.py:84):')
    for f, n, t in stale_short:
        w(f'  {f}:{n}: {t}')
    w('')
else:
    w('OK: комментарии 020/021/033/036/046/047 используют корректную формулировку формата')
    w('')
if stale_mnem:
    w('FAIL: в коде остались старые мнёмоники *20/*21/*33/*36 (нужны APX/AUX/EXT/ASN):')
    for f, n, t in stale_mnem:
        w(f'  {f}:{n}: {t}')
    w('')
else:
    w('OK: в коде нет *20/*21/*33/*36 — используются APX/AUX/EXT/ASN')
    w('')
if stale_033:
    w('FAIL: в LO*GEN opcode 033 помечен как EXT/увв (должен быть STOP, Format 2):')
    for f, n, t in stale_033:
        w(f'  {f}:{n}: {t}')
    w('')
else:
    w('OK: в LO*GEN opcode 033 = STOP (Format 2), мнемоника `33`, не EXT/увв')
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
        ref = r['command_ref']
        expect = EXPECTED_MNEMONIC.get(norm)
        if norm == '36':
            # Явная формула Монитор-80 для КАЖДОГО вхождения:
            #   ,ASN,64+N → вправо; ,ASN,64−N → влево; N = EA[7:1]
            #   (младшие 7 разрядов адреса, Besm6_Instruction_Set.md §6).
            expected_comment = ec.make_asn_comment(str(r['info']))
            ok = expected_comment in line
            if not ok:
                cmd_bad.append((frel, r['line'], r['code'], r['info'],
                                'нет явной формулы ASN (Монитор-80 64±N)'))
            found = r.get('opcode_mnemonic')
            if found != expect:
                ok = False
                cmd_bad.append((frel, r['line'], r['code'], r['info'],
                                f'мнёмоника {found!r}, ожидалась {expect!r}'))
            formula, N, k, madlen, word = ec.asn_shift(str(r['info']))
            label = f'ASN опк 36: {formula}'
        else:
            # Канонический комментарий целиком (формат, мнёмоника, аргумент, источник).
            canonical = ec.make_command_comment(r['code'])
            marker = f'. опк {norm} ({ec.FORMAT_LABEL}) = '
            ok = marker in line and canonical in line
            if ok:
                meaning = ec.COMMAND_STATEMENTS.get(norm, '')
                if meaning not in line:
                    ok = False
                    cmd_bad.append((frel, r['line'], r['code'], r['info'],
                                    f'нет значения «{meaning}»'))
                found = r.get('opcode_mnemonic')
                if found != expect:
                    ok = False
                    cmd_bad.append((frel, r['line'], r['code'], r['info'],
                                    f'мнёмоника {found!r}, ожидалась {expect!r}'))
                op = r.get('token')
                expected_note = r.get('argument_note')
                if op and expected_note and expected_note not in line:
                    ok = False
                    cmd_bad.append((frel, r['line'], r['code'], r['info'],
                                    f'нет интерпретации аргумента {op} '
                                    f'({r.get("argument_class")})'))
            label = f'{expect} опк {norm} [{ref}]'
        if not ok:
            missing.append((frel, r['line'], r['code'], r['info']))
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
    if ok and r['code'] in ec.EXTRACT_CLASSES:
        # Э60/Э70/Э71: класс экстракода по Besm6_Instruction_Set.md §6
        # и контекстная интерпретация информационного слова обязательны.
        class_comment = ec.make_extract_class_comment(r['code'], str(r['info']))
        if class_comment not in line:
            wrong_source.append((frel, r['line'], r['code'], r['info'],
                                 'нет класса экстракода (Besm6_Instruction_Set.md §6)'))
    if not ok:
        missing.append((frel, r['line'], r['code'], r['info']))
    status = 'OK' if ok else 'FAIL'
    label = src or 'адрес/данные' if ADDR_DATA in line else (src or 'не найдено')
    w(f"{status:4} {frel}:{r['line']}: {r['code']} {r['info']} "
      f"-> {(r['description'] or '—')[:60]} [{label}]")

# ── Классы аргументов APX/AUX: проверяем ВСЕ 307 вхождений ────────────────
# Основной цикл выше видит только аннотированные строки (`. опк ...`), а
# ETX/TL/MAS-операнды в lib21 имеют краткую пометку `; S:NNNN`.  Здесь
# проверка дополнена до всех
# инструкций 020/021 с аргументом, независимо от вида комментария.
argclass_bad = []
argclass_counts = Counter()
argclass_lines = 0
arg_noarg = 0
APX_ARG_RE = re.compile(
    r'(?:(?<=^)|(?<=[,:])|(?<=\s))\s*(APX|AUX)\s*,\s*'
    r'([A-Za-z0-9_#$()+\-=:]+)'
)
APX_NOARG_RE = re.compile(r'(?:^|[,:]|\s)(APX|AUX)\s*,\s*(?=\s|\.|;|$)')
EQU_SIMPLE_RE = re.compile(
    r'^\s*([A-Za-z][A-Za-z0-9_#$]*)\s*,\s*EQU\s*,\s*(.*?)\s*(?:[.;].*)?$'
)
for path in sources:
    frel = str(path.relative_to(root))
    lines = path.read_text(encoding='utf-8', errors='replace').splitlines()
    local_equ = {}
    for ln in lines:
        em = EQU_SIMPLE_RE.match(ln)
        if em:
            local_equ[em.group(1)] = em.group(2).strip()
    for no, line in enumerate(lines, 1):
        head = re.split(r'\s+[.;]', line, maxsplit=1)[0]
        am = APX_ARG_RE.search(head)
        if not am:
            if APX_NOARG_RE.search(head):
                arg_noarg += 1
            continue
        tok = am.group(2)
        info = local_equ.get(tok, '')
        cls = ec.classify_apx_aux_argument(tok, info)
        note = ec.apx_aux_argument_note(tok, info)
        argclass_counts[cls] += 1
        argclass_lines += 1
        if note not in line:
            argclass_bad.append((frel, no, tok, cls))
w('КЛАССЫ АРГУМЕНТОВ 020/021 (APX/AUX)')
for cls in ec.APX_AUX_ARG_CLASSES:
    w(f'  {cls:<18}: {argclass_counts[cls]}')
w(f'  инструкций с аргументом: {argclass_lines}; без аргумента: {arg_noarg}')
if argclass_bad:
    w(f'FAIL: у {len(argclass_bad)} APX/AUX нет явной интерпретации аргумента:')
    for f, n, t, c in argclass_bad:
        w(f'  {f}:{n}: {t} — ожидался класс {c}')
else:
    w('OK: у всех инструкций APX/AUX аргумент явно классифицирован '
      '(mask-word (text) / immediate-code / address)')
w('')
w(f'Вхождений: {len(seen)} (команд 020..047: {n_commands}; экстракодов 050..077: {n_extracts})')
w(f'Уникальных пар экстракодов: {len(pairs_seen)}')
w(f'Расшифровано по rukava.be: {by_source["rukava.be"]}')
w(f'Расшифровано по Тюрину-1985: {by_source["tyurin1985"]}')
w(f'Экстракодов без расшифровки (помечено явно): {by_source[None]}')
w(f'Команд с корректной мнёмоникой и комментарием: {n_commands - len(cmd_bad)}')
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

fail = bool(missing or wrong_source or cmd_bad or stale or stale_short
            or stale_mnem or stale_033 or argclass_bad)
if not fail:
    w('OK: мнёмоники APX/AUX/EXT/ASN, классы аргументов 020/021 '
      '(mask-word (text) / immediate-code / address), явные формулы ASN '
      '(Монитор-80 64±N), классы Э60/Э70/Э71 и 033=STOP в LO*GEN корректны; '
      'экстракоды 050..077 расшифрованы')
else:
    w('FAIL: часть мнёмоник/комментариев отсутствует или неверна')
report.write_text('\n'.join(out) + '\n', encoding='utf-8')
print(f'Отчёт: {report}')
print(out[-1])
sys.exit(1 if fail else 0)
PY
exit $?
