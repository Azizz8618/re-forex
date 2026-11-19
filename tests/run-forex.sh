#!/usr/bin/env bash
# Регрессия FOREX 2.02: прогон reference/forex.b6 на dispak и сравнение вывода
# с эталоном reference/output.gold.txt.
#
# В эталоне строка даты заwildcard'ена как "##.##.##"; перед сравнением обе
# стороны нормализуются: последовательности DD.DD.DD заменяются на ##.##.##.
# Это единственная разрешённая нормализация — остальной вывод сравнивается
# побайтово.
set -u

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd) || exit 1

DISPAK_BIN=${DISPAK_BIN:-/home/azizz/Yandex.Disk/dispak/build/dispak/dispak}
REF="$ROOT/reference"
GOLD="$REF/output.gold.txt"

fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }

[ -x "$DISPAK_BIN" ] || fail "dispak не найден/не исполняем: $DISPAK_BIN (переопределите DISPAK_BIN)"
[ -f "$REF/forex.b6" ] || fail "нет $REF/forex.b6"
[ -f "$REF/options.txt" ] || fail "нет $REF/options.txt"
[ -f "$GOLD" ] || fail "нет $GOLD"

TMPROOT=${TMPDIR:-/tmp/.private/azizz/opencode}
[ -d "$TMPROOT" ] || TMPROOT=/tmp
TMP=$(mktemp -d "$TMPROOT/re-forex-run.XXXXXX") || fail "не удалось создать временный каталог"
trap 'rm -rf "$TMP"' EXIT

cp "$REF/forex.b6" "$REF/options.txt" "$TMP/" || fail "не удалось скопировать входные файлы"

printf 'dispak: %s\n' "$DISPAK_BIN"
printf 'task:   %s\n' "$REF/forex.b6"
printf 'gold:   %s\n' "$GOLD"

( cd "$TMP" && "$DISPAK_BIN" forex.b6 > output.raw 2> stderr.txt )
rc=$?
if [ "$rc" -ne 0 ]; then
    printf '--- stderr ---\n' >&2
    cat "$TMP/stderr.txt" >&2
    fail "dispak завершился с кодом $rc"
fi
[ -s "$TMP/stderr.txt" ] && printf 'dispak stderr (не пуст):\n' >&2 && cat "$TMP/stderr.txt" >&2

normalize() {
    sed -E 's/[0-9]{2}\.[0-9]{2}\.[0-9]{2}/##.##.##/g' "$1"
}

normalize "$TMP/output.raw" > "$TMP/output.norm" || fail "нормализация вывода"
normalize "$GOLD" > "$TMP/gold.norm" || fail "нормализация эталона"

printf 'raw bytes:  %s\n' "$(wc -c < "$TMP/output.raw")"
printf 'gold bytes: %s\n' "$(wc -c < "$GOLD")"

if cmp -s "$TMP/gold.norm" "$TMP/output.norm"; then
    printf 'OK: FOREX 2.02 вывод совпадает с эталоном (после нормализации даты)\n'
    exit 0
fi

printf '--- первые различия (эталон / факт) ---\n' >&2
diff -u "$TMP/gold.norm" "$TMP/output.norm" | head -80 >&2
fail "вывод dispak отличается от reference/output.gold.txt"
