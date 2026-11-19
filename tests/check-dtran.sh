#!/bin/bash
# Проверка дизассемблирования в МАДЛЕН через dtran.
set -u
cd "$(dirname "$0")/.." || exit 1
rc=0
for pair in "LO_SYN:LO*SYN" "LO_GEN:LO*GEN"; do
    name=${pair%%:*}
    sym=${pair#*:}
    f="disasm/${name}.dtran.madlen"
    if [ ! -s "$f" ]; then
        echo "FAIL $f отсутствует или пуст"
        rc=1
        continue
    fi
    n=$(wc -l < "$f")
    if [ "$n" -lt 1500 ]; then
        echo "FAIL $f слишком короткий: $n строк"
        rc=1
        continue
    fi
    if ! head -1 "$f" | grep -qF "$sym"; then
        echo "FAIL $f: нет имени $sym в первой строке"
        rc=1
        continue
    fi
    if ! grep -q ',VTM,' "$f" || ! grep -q ',VJM,' "$f"; then
        echo "FAIL $f: нет команд VTM/VJM"
        rc=1
        continue
    fi
    echo "OK $f: $n строк, заголовок $sym, VTM/VJM присутствуют"
done
exit $rc
