#!/usr/bin/env bash
# Проверка: числовые литералы в реконструированных МАДЛЕН-текстах вынесены
# в именованные константы `,EQU,`.
#
# Для каждого файла печатается таблица:
#   ФАЙЛ | EQU | ГОЛЫХ | УНИК | СТАТУС
# где
#   EQU   — число объявлений ,EQU, (forms: `NAME ,EQU, value`,
#           `NAME, EQU, value`, `,EQU,`);
#   ГОЛЫХ — число «голых» восьмеричных литералов в операндах команд —
#           токенов вида `2200B`, `1376B` (цифра на начале, суффикс B),
#           которые НЕ являются символическими именами;
#   УНИК  — число уникальных таких литералов.
#
# Исключаются: целострочные комментарии (`С` в поз.1, `;`) и встроенный
# комментарий (`.`), строки-метки слов (`С--- слово … машинное слово …`,
# `С слово … = 0o…`) и сами объявления EQU.
#
# Критерий: EQU > 0 И уникальных литералов <= ПОРОГ (20) — OK, иначе FAIL.
# Устойчивость к параллельному редактированию: отсутствующий/пустой файл
# печатается как «—» со статусом ОЖИДАЕТСЯ и не считается провалом; сценарий
# никогда не аварийно завершается из-за grep/sed, а печатает текущее состояние.
# Выход: 0 — OK (или проверка отложена), 1 — FAIL.
set -u

# Кириллическая «С» в regex должна быть одним символом — включаем UTF-8 locale.
if locale -a 2>/dev/null | grep -qiE '^(C\.utf8|C\.UTF-8)$'; then
    export LC_ALL=C.UTF-8
fi

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd) || exit 1
cd "$ROOT" || exit 1

THRESHOLD=20

FILES=(
    "src/LO_SYN.mad"
    "src/LO_GEN.mad"
    "src/FOREX_CORE.mad"
    "src/FOREX_RUNTIME.mad"
    "include/FOREX_ROOT.mad"
)

# EQU как отдельный токен: ,EQU, / , EQU, / NAME EQU value — но не EQUX, X_EQU.
EQU_RE='(^|[^[:alnum:]_])EQU([^[:alnum:]_]|$)'
# Голый восьмеричный литерал: цифра 0-7 на начале, суффикс b/B, границы слова
# отсекают имена вроде LOOPB / N123B и префикс 0o.
LIT_RE='\b[0-7]+[bB]\b'

# Поток «кода»: без целострочных комментариев и без встроенного комментария.
code_stream() {
    grep -vE '^[[:space:]]*[Сс;]' "$1" | sed -E 's/[.;].*$//'
}

# Число объявлений EQU.
count_equ() {
    code_stream "$1" | grep -ciE "$EQU_RE" || true
}

# Все голые литералы (по одному на строку); '.' в inline-комментарии уже убран.
bare_literals() {
    code_stream "$1" \
        | grep -viE "$EQU_RE" \
        | grep -oE "$LIT_RE" \
        || true
}

row() {
    printf '%-28s | %5s | %6s | %6s | %s\n' "$@"
}

printf 'ПРОВЕРКА КОНСТАНТ: голые литералы -> ,EQU, (порог уникальных = %d)\n' "$THRESHOLD"
row 'ФАЙЛ' 'EQU' 'ГОЛЫХ' 'УНИК' 'СТАТУС'
printf -- '-----------------------------+-------+--------+--------+--------\n'

status=0
pending=0
for f in "${FILES[@]}"; do
    if [ ! -s "$f" ]; then
        row "$f" '—' '—' '—' 'ОЖИДАЕТСЯ (нет файла)'
        pending=1
        continue
    fi

    equ=$(count_equ "$f")
    lit=$(bare_literals "$f")
    total=$(printf '%s\n' "$lit" | grep -c . || true)
    uniq=$(printf '%s\n' "$lit" | sort -u | grep -c . || true)

    if [ "$equ" -gt 0 ] && [ "$uniq" -le "$THRESHOLD" ]; then
        row "$f" "$equ" "$total" "$uniq" 'OK'
    else
        reason=''
        [ "$equ" -gt 0 ] || reason='нет EQU'
        if [ "$uniq" -gt "$THRESHOLD" ]; then
            reason="${reason:+$reason, }уник>$THRESHOLD"
        fi
        row "$f" "$equ" "$total" "$uniq" "FAIL ($reason)"
        status=1
    fi
done

printf -- '-----------------------------+-------+--------+--------+--------\n'
if [ "$pending" -eq 1 ] && [ "$status" -eq 0 ]; then
    printf 'ОЖИДАЕТСЯ: часть файлов ещё редактируется — проверка отложена\n'
    exit 0
fi
if [ "$status" -eq 0 ]; then
    printf 'OK: все файлы вынесли литералы в ,EQU, (уник <= %d)\n' "$THRESHOLD"
else
    printf 'FAIL: литералы вынесены в ,EQU, не полностью (см. таблицу)\n' >&2
fi
exit "$status"
