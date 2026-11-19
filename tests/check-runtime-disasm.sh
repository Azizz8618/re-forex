#!/usr/bin/env bash
# Проверка новых дизассемблированных рантайм-модулей FOREX.
#
# Проверяет:
#   1. Наличие и непустоту src/FOREX_RUNTIME_DISASM.mad,
#      src/FOREX_DECODER_DISASM.mad, disasm/RUNTIME_*.madlen,
#      disasm/RUNTIME_*.bemsh.lst;
#   2. В .mad: >20 ,EQU, констант, осмысленные метки (нет Wnnn:, Dnnnnn:,
#      *000NN) и >100 строк комментариев (С / . / ;);
#   3. Размер build/RUNTIME_*.words (если есть) кратен 6 байтам;
#   4. Вызывает tests/check-source-words.py и tests/check-constants.sh
#      и пробрасывает их rc в общий результат;
#   5. Устойчивость к отсутствующим файлам: печать «ОЖИДАЕТСЯ», без падения.
#
# Возврат: 0 — всё пройдено (включая отложенные проверки), 1 — есть FAIL.
set -u

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd) || exit 1
cd "$ROOT" || exit 1

# Кириллическая «С» в regex должна быть одним символом — включаем UTF-8 locale.
if locale -a 2>/dev/null | grep -qiE '^(C\.utf8|C\.UTF-8)$'; then
    export LC_ALL=C.UTF-8
fi

status=0
pending=0

ok()    { printf 'OK        %s\n' "$*"; }
fail()  { printf 'FAIL      %s\n' "$*" >&2; status=1; }
wait_() { printf 'ОЖИДАЕТСЯ %s\n' "$*"; pending=1; }

lines() { wc -l < "$1" 2>/dev/null | tr -d ' '; }

# ---------------------------------------------------------------- 1. файлы
printf '=== 1. Наличие и непустота файлов ===\n'
MAD_FILES=(src/FOREX_RUNTIME_DISASM.mad src/FOREX_DECODER_DISASM.mad)
for f in "${MAD_FILES[@]}"; do
    if [ -s "$f" ]; then
        ok "$f ($(lines "$f") строк)"
    else
        wait_ "$f (нет файла или пуст)"
    fi
done

check_glob() {
    local pattern=$1 matches any=0 f
    matches=$(compgen -G "$pattern" || true)
    if [ -z "$matches" ]; then
        wait_ "$pattern (нет ни одного файла)"
        return
    fi
    while IFS= read -r f; do
        [ -n "$f" ] || continue
        if [ -s "$f" ]; then
            any=1
            ok "$f ($(lines "$f") строк)"
        else
            wait_ "$f (файл есть, но пуст)"
        fi
    done <<< "$matches"
    [ "$any" -eq 1 ] || wait_ "$pattern (все файлы пусты)"
}

check_glob 'disasm/RUNTIME_*.madlen'
check_glob 'disasm/RUNTIME_*.bemsh.lst'

# ------------------------------------------------------- 2. содержимое .mad
printf '\n=== 2. Содержание .mad (EQU / метки / комментарии) ===\n'

# EQU как отдельный токен (не EQUX, X_EQU) — по образцу check-constants.sh.
EQU_RE='(^|[^[:alnum:]_])EQU([^[:alnum:]_]|$)'
# Автосгенерированные метки: W1777:, D00001:, *00012 (только в коде, не в
# комментариях — комментарии отфильтровываются через code_stream).
BAD_LABEL_RE='^[[:space:]]*(W[0-9]{3,4}|D[0-9]{4,5})[[:space:]]*:|^[[:space:]]*\*000[0-9]{2}'
# Комментарии: целострочные С/./; и встроенные . / ;.
COMMENT_RE='^[[:space:]]*(С|\.|;)|[[:space:]]\.[[:space:]]|;[[:space:]]'

check_mad_content() {
    local f=$1 code equ auto comments
    [ -s "$f" ] || return 0   # отсутствие уже сообщено в разделе 1

    code=$(grep -vE '^[[:space:]]*[Сс;.]' "$f" || true)

    equ=$(printf '%s\n' "$code" | grep -ciE "$EQU_RE" || true)
    if [ "$equ" -gt 20 ]; then
        ok "EQU=$equ > 20: $f"
    else
        fail "EQU=$equ <= 20: $f"
    fi

    auto=$(printf '%s\n' "$code" | grep -cE "$BAD_LABEL_RE" || true)
    if [ "$auto" -eq 0 ]; then
        ok "авто-меток 0: $f"
    else
        fail "авто-меток $auto: $f"
    fi

    comments=$(grep -cE "$COMMENT_RE" "$f" || true)
    if [ "$comments" -gt 100 ]; then
        ok "комментариев $comments > 100: $f"
    else
        fail "комментариев $comments <= 100: $f"
    fi
}

for f in "${MAD_FILES[@]}"; do check_mad_content "$f"; done

# --------------------------------- 2b. длина/уникальность имён (6 символов)
# МАДЛЕН различает в метках и ,EQU,-именах только первые 6 символов:
# длинные имена усекаются и коллидируют. Все имена файла (метки + EQU)
# должны иметь длину <= 6 и уникальный префикс из первых 6 символов.
printf '\n=== 2b. Длина и уникальность имён (метки + EQU, первые 6 символов) ===\n'
present=()
for f in "${MAD_FILES[@]}"; do [ -s "$f" ] && present+=("$f"); done
if [ "${#present[@]}" -gt 0 ]; then
    names_out=$(python3 - "${present[@]}" <<'PY'
import sys, re
from collections import defaultdict

# Метка: NAME: в начале строки. EQU: NAME ,EQU, value в начале строки.
LABEL = re.compile(r'^[ \t]*([A-Za-z*][A-Za-z0-9_*/+=]*?)[ \t]*:')
EQU = re.compile(r'^[ \t]*([A-Za-z*][A-Za-z0-9_*/+=]*?)[ \t]*,[ \t]*EQU[ \t]*,', re.I)

rc = 0
for path in sys.argv[1:]:
    names = []
    with open(path, encoding='utf-8', errors='replace') as fh:
        for ln, line in enumerate(fh, 1):
            m = EQU.match(line)
            if m:
                names.append((m.group(1), ln, 'EQU'))
                continue
            m = LABEL.match(line)
            if m:
                names.append((m.group(1), ln, 'метка'))

    longs = [(n, ln) for n, ln, _ in names if len(n) > 6]
    pref = defaultdict(list)
    for n, ln, _ in names:
        pref[n[:6]].append((n, ln))
    colls = {p: v for p, v in pref.items() if len({n for n, _ in v}) > 1}

    short = path.rsplit('/', 1)[-1]
    if not longs and not colls:
        print(f'OK        {short}: {len(names)} имён, все <=6 и уникальны по первым 6')
        continue
    rc = 1
    if longs:
        sample = ', '.join(f'{n}(стр.{ln})' for n, ln in longs[:10])
        more = f' ... и ещё {len(longs) - 10}' if len(longs) > 10 else ''
        print(f'FAIL      {short}: длинных имён >6: {len(longs)} [{sample}{more}]')
    if colls:
        items = sorted(colls.items(), key=lambda kv: -len(kv[1]))
        sample = '; '.join(
            f'{p}: ' + ', '.join(f'{n}(стр.{ln})' for n, ln in v[:4])
            for p, v in items[:10]
        )
        more = f' ... и ещё {len(colls) - 10}' if len(colls) > 10 else ''
        print(f'FAIL      {short}: коллизий первых 6 символов: {len(colls)} [{sample}{more}]')
sys.exit(rc)
PY
)
    rc=$?
    printf '%s\n' "$names_out"
    [ "$rc" -eq 0 ] || status=1
fi

# ------------------------------------------------------------- 3. .words
printf '\n=== 3. build/RUNTIME_*.words: кратность 6 байтам ===\n'
matches=$(compgen -G 'build/RUNTIME_*.words' || true)
if [ -z "$matches" ]; then
    wait_ "build/RUNTIME_*.words (дампов нет — проверка отложена)"
else
    while IFS= read -r f; do
        [ -n "$f" ] || continue
        size=$(wc -c < "$f")
        rem=$(( size % 6 ))
        if [ "$size" -gt 0 ] && [ "$rem" -eq 0 ]; then
            ok "$f: $size байт, остаток от 6 = 0"
        else
            fail "$f: $size байт, остаток от 6 = $rem"
        fi
    done <<< "$matches"
fi

# ------------------------------------- 4. старые регрессии (проброс rc)
printf '\n=== 4. Существующие регрессии (проброс rc) ===\n'
if [ -f tests/check-source-words.py ]; then
    python3 tests/check-source-words.py
    rc=$?
    if [ "$rc" -eq 0 ]; then ok "check-source-words.py rc=0"; else fail "check-source-words.py rc=$rc"; fi
else
    wait_ "tests/check-source-words.py (нет файла)"
fi

if [ -f tests/check-constants.sh ]; then
    bash tests/check-constants.sh
    rc=$?
    if [ "$rc" -eq 0 ]; then ok "check-constants.sh rc=0"; else fail "check-constants.sh rc=$rc"; fi
else
    wait_ "tests/check-constants.sh (нет файла)"
fi

# --------------------------------------------------------------- ИТОГ
printf '\n=== ИТОГ ===\n'
if [ "$status" -ne 0 ]; then
    printf 'FAIL: проверка новых рантайм-модулей не пройдена\n' >&2
    exit 1
fi
if [ "$pending" -eq 1 ]; then
    printf 'ОЖИДАЕТСЯ: новые дизассемблированные файлы ещё не созданы полностью\n'
    printf 'OK (ожидается): регрессия не падает, проверки отложены до появления файлов\n'
else
    printf 'OK: все проверки новых рантайм-модулей пройдены\n'
fi
exit 0
