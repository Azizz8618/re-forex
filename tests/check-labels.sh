#!/bin/bash
# Проверка семантического именования меток и полноты таблиц соответствий.
set -u
cd "$(dirname "$0")/.." || exit 1
rc=0
for pair in \
    "src/LO_SYN.mad:include/LO_SYN.labels.md" \
    "src/LO_GEN.mad:include/LO_GEN.labels.md" \
    "src/FOREX_CORE.mad:include/FOREX.labels.md" \
    "src/FOREX_RUNTIME.mad:include/FOREX.labels.md" \
    "include/FOREX_ROOT.mad:include/FOREX.labels.md"; do
    src=${pair%%:*}
    map=${pair#*:}
    if [ ! -s "$src" ]; then echo "FAIL $src отсутствует"; rc=1; continue; fi
    if [ ! -s "$map" ]; then echo "FAIL $map отсутствует"; rc=1; continue; fi
    # автосгенерированные метки вида W1777: / WT0533: / D00001:
    auto=$(grep -cE '^[[:space:]]*(W[0-9]{3,4}|WT[0-9]{3,4}|D[0-9]{4,5})[[:space:]]*:' "$src" || true)
    if [ "$auto" -gt 0 ]; then
        echo "FAIL $src: осталось $auto автосгенерированных меток" >&2; rc=1
    fi
    n=$(grep -cE '^\|.*\|.*\|' "$map" || true)
    if [ "$n" -lt 10 ]; then
        echo "FAIL $map: слишком мало строк таблицы ($n)" >&2; rc=1
    else
        echo "OK $src: авто-меток 0, в $map $n строк соответствий"
    fi
done
exit $rc
