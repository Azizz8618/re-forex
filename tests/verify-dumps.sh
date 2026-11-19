#!/usr/bin/env bash
# Повторная выгрузка оверлеев LO*SYN / LO*GEN из ленты monsys.9 и сверка
# sha256 с зафиксированными дампами build/LO_*.words.
set -u

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd) || exit 1

TAPE=${MONSYS_TAPE:-/home/azizz/Yandex.Disk/besm6-new/besm6.net/tapes/monsys.9}
BUILD="$ROOT/build"

fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }

[ -f "$TAPE" ] || fail "лента не найдена: $TAPE (переопределите MONSYS_TAPE)"

TMPROOT=${TMPDIR:-/tmp/.private/azizz/opencode}
[ -d "$TMPROOT" ] || TMPROOT=/tmp
TMP=$(mktemp -d "$TMPROOT/re-forex-dumps.XXXXXX") || fail "не удалось создать временный каталог"
trap 'rm -rf "$TMP"' EXIT

# имя | восьмеричное смещение (слово на ленте) | ожидаемый sha256
OVERLAYS="
LO_SYN 241500 83a7e962a9db89e62b856b7461ce2aba91239957931a03e1520fb4d228459366
LO_GEN 277500 4f4d8e4cc8fff1ec9742fe8be0a0c5f797716ab1bd085a1625d37569d222cbfd
"

printf 'tape: %s\n' "$TAPE"
status=0
printf '%s\n' "$OVERLAYS" | while read -r name oct expect; do
    [ -n "${name:-}" ] || continue
    out="$TMP/$name.words"
    # 6 байт/слово, big-endian; смещения в восьмеричной системе → $((8#...))
    dd if="$TAPE" of="$out" bs=6 skip=$((8#$oct)) count=1024 status=none \
        || { printf 'FAIL: dd для %s\n' "$name" >&2; exit 1; }

    size=$(wc -c < "$out")
    got=$(sha256sum "$out" | awk '{print $1}')
    printf '%-6s offset=0o%-7s size=%-6s sha256=%s\n' "$name" "$oct" "$size" "$got"

    [ "$size" -eq 6144 ] || { printf 'FAIL: %s: размер %s вместо 6144\n' "$name" "$size" >&2; exit 1; }
    [ "$got" = "$expect" ] || {
        printf 'FAIL: %s: sha256 не совпадает (ожидалось %s)\n' "$name" "$expect" >&2
        exit 1
    }
    if [ -f "$BUILD/$name.words" ]; then
        cmp -s "$BUILD/$name.words" "$out" \
            || { printf 'FAIL: %s: выгрузка отличается от build/%s.words\n' "$name" "$name" >&2; exit 1; }
        printf '       побайтовая сверка с build/%s.words: OK\n' "$name"
    else
        printf '       build/%s.words отсутствует — сравнение только по sha256\n' "$name"
    fi
done
rc=$?
[ "$rc" -eq 0 ] || fail "выгрузка оверлеев не прошла проверку"
printf 'OK: оверлеи LO*SYN и LO*GEN выгружены и сверены\n'
exit 0
