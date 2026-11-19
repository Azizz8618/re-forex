#!/bin/bash
# Проверка дизассемблирования и аннотации библиотеки 21.
set -u
cd "$(dirname "$0")/.." || exit 1
rc=0
SRC=/home/azizz/Yandex.Disk/besm6-new/DUBNA/BUILD/elements/lib21.bin
[ -s "$SRC" ] || { echo "ОЖИДАЕТСЯ: нет $SRC"; exit 0; }

n=$(find disasm/lib21 -name '*.madlen' -type f 2>/dev/null | wc -l)
echo "листингов dtran: $n / 358"
[ "$n" -ge 300 ] || { echo "FAIL: слишком мало листингов" >&2; rc=1; }

# Модули с cmd=0 — чисто данные (таблицы/константы); у них нет мнемоник,
# это корректно. Требуем мнемоники только для модулей с cmd>0.
bad=0
for f in disasm/lib21/*.madlen; do
    [ -s "$f" ] || continue
    head -1 "$f" | grep -q ',NAME,' || { bad=$((bad+1)); continue; }
    base=$(basename "$f" .madlen)
    mod=$(printf '%s' "$base" | sed -e 's/#/\//g' -e 's/_/*/g')
    cmd=$(awk -F, -v m="$mod" 'NR>1 && $1==m {print $3; exit}' docs/lib21/modules.csv)
    lines=$(wc -l < "$f")
    if [ -n "$cmd" ] && [ "$cmd" -gt 0 ] && [ "$lines" -gt 5 ]; then
        # у модулей с cmd=1 может быть всего одна команда (напр. STOP/Э-код)
        grep -qE 'VTM|XTA|ATX|UJ|VJM|STOP|Э[0-9]+|,[A-ZА-Я][A-ZА-Я0-9*/]*,[0-9A-ZА-Я*]' "$f" || bad=$((bad+1))
    fi
done
echo "листингов с ошибками NAME/мнемоник (кроме cmd=0): $bad"
[ "$bad" -eq 0 ] || { echo "FAIL: $bad листингов с cmd>0 без мнемоник" >&2; rc=1; }

a=$(find src/lib21 -name '*.mad' -type f 2>/dev/null | wc -l)
echo "аннотированных модулей: $a"
[ "$a" -ge 20 ] || { echo "FAIL: аннотаций меньше 20" >&2; rc=1; }

for t in tools/lib21_parse.py tools/lib21_disasm.py tools/lib21_xref.py \
         docs/lib21/01-structure.md docs/lib21/02-disassembly.md \
         docs/lib21/03-crossrefs.md docs/lib21/modules.csv; do
    [ -s "$t" ] || { echo "FAIL: нет $t" >&2; rc=1; }
done

if [ "$rc" -eq 0 ]; then echo "OK: библиотека 21 разобрана и аннотирована"; fi
exit $rc
