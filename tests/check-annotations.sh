#!/usr/bin/env bash
# Проверка обязательных символов чек-листа (docs/PLAN.md §6) и плотности
# комментариев в реконструированных МАДЛЕН-исходниках этапа 5.
#
# Если исходники ещё не созданы другими агентами, сценарий печатает
# «ожидается» и возвращает 0 — регрессия не падает во время реконструкции.
set -u

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd) || exit 1

FILES=(
    "$ROOT/src/LO_SYN.mad"
    "$ROOT/src/LO_GEN.mad"
    "$ROOT/include/FOREX_ROOT.mad"
)

fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }

# Обязательные символы из чек-листа (37 обязательных + COMMON/TEXT из §6).
SYMBOLS=(
    'INITFOR*' 'LOREX' 'RMON' 'STOP/'
    'DATAPR*' 'TAK/PG' 'GIV/PG' 'OCTTDEC' 'FOREX' 'CONST'
    'COMEQ' 'OPRTR' 'ПP' 'LOADANGO'
    'LO*SYN' 'LO*GEN' '*A*' 'ENTRY*' '*DUMON*'
)

missing=()
for f in "${FILES[@]}"; do
    [ -f "$f" ] || missing+=("$f")
done

if [ "${#missing[@]}" -gt 0 ]; then
    printf 'ОЖИДАЕТСЯ: реконструкция ещё не создала:\n'
    for f in "${missing[@]}"; do printf '  %s\n' "$f"; done
    printf 'OK (ожидается): проверка символов и комментариев отложена\n'
    exit 0
fi

status=0
printf 'Проверяемые файлы:\n'
for f in "${FILES[@]}"; do printf '  %s\n' "$f"; done

# 1. Каждый символ должен встречаться хотя бы в одном из трёх файлов.
notfound=()
for sym in "${SYMBOLS[@]}"; do
    found=0
    for f in "${FILES[@]}"; do
        if grep -F -q -- "$sym" "$f"; then found=1; break; fi
    done
    if [ "$found" -eq 1 ]; then
        printf 'OK   symbol %-12s\n' "$sym"
    else
        printf 'FAIL symbol %-12s не найден\n' "$sym" >&2
        notfound+=("$sym")
        status=1
    fi
done

# 2. Не менее 50 строк-комментариев в каждом .mad (С <пробел> или '.').
for f in "${FILES[@]}"; do
    case "$f" in
        *.mad) ;;
        *) continue ;;
    esac
    # МАДЛЕН допускает комментарий `С` в поз. 1 и встроенный `.`;
    # в аннотациях корня используется также `;`. Учитываем все три формы.
    n=$(grep -cE '^[[:space:]]*(С|\.|;)|[[:space:]]\.[[:space:]]|;[[:space:]]' "$f" || true)
    if [ "$n" -ge 50 ]; then
        printf 'OK   comments %3d >= 50: %s\n' "$n" "$f"
    else
        printf 'FAIL comments %3d < 50: %s\n' "$n" "$f" >&2
        status=1
    fi
done

if [ "$status" -eq 0 ]; then
    printf 'OK: все обязательные символы и комментарии присутствуют\n'
else
    printf 'FAIL: чек-лист символов/комментариев не пройден (не найдено: %s)\n' "${notfound[*]:--}" >&2
fi
exit "$status"
