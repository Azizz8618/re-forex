#!/usr/bin/env bash
# Проверка листингов дизассемблера и кратности дампов 6 байтам (1 слово БЭСМ-6).
set -u

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd) || exit 1

fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }

LSTS=( "$ROOT/disasm/LO_SYN.raw.lst" "$ROOT/disasm/LO_GEN.raw.lst" )
WORDS=( "$ROOT/build/LO_SYN.words" "$ROOT/build/LO_GEN.words" )

status=0
for f in "${LSTS[@]}"; do
    [ -f "$f" ] || { printf 'FAIL: нет листинга %s\n' "$f" >&2; status=1; continue; }
    lines=$(wc -l < "$f")
    printf '%-40s строк=%s\n' "${f#$ROOT/}" "$lines"
    if grep -q 'СТАРТ' "$f"; then printf '  OK   СТАРТ\n'; else printf '  FAIL СТАРТ не найден\n' >&2; status=1; fi
    if grep -q 'ФИНИШ' "$f"; then printf '  OK   ФИНИШ\n'; else printf '  FAIL ФИНИШ не найден\n' >&2; status=1; fi
    if [ "$lines" -ge 900 ]; then
        printf '  OK   строк >= 900\n'
    else
        printf '  FAIL строк %s < 900\n' "$lines" >&2; status=1
    fi
done

for f in "${WORDS[@]}"; do
    [ -f "$f" ] || { printf 'FAIL: нет дампа %s\n' "$f" >&2; status=1; continue; }
    size=$(wc -c < "$f")
    rem=$(( size % 6 ))
    printf '%-40s байт=%s (остаток от 6: %s)\n' "${f#$ROOT/}" "$size" "$rem"
    if [ "$size" -gt 0 ] && [ "$rem" -eq 0 ]; then
        printf '  OK   кратно 6 байтам\n'
    else
        printf '  FAIL размер не кратен 6 байтам\n' >&2; status=1
    fi
done

if [ "$status" -eq 0 ]; then
    printf 'OK: листинги и дампы прошли проверку\n'
else
    printf 'FAIL: проверка дизассембла/дампов не пройдена\n' >&2
fi
exit "$status"
