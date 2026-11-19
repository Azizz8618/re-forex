#!/usr/bin/env bash
# Проверка ДРАКОН-схем проекта: docs/drakon/*.drakon и их производных
#   docs/drakon/markup/<имя>.txt   — разметка *RED (эталон drakon_markup.py)
#   docs/drakon/printed/<имя>.txt  — реальная печать БЭСМ-редактора ДРАКОН
#
# Для каждого .drakon печатается таблица:
#   ФАЙЛ | ИКОН | МАРКИРОВКА | СТАТУС
#
# Проверки:
#   1. схема непустая; есть ЗАГОЛОВОК, хотя бы одна ВЕТКА верхнего уровня
#      и КОНЕЦ; икон (строк с ключевыми словами) >= 15; строк длиной > 80 нет;
#   2. вложенных ВЕТКА нет (ВЕТКА только без ведущих пробелов);
#   3. есть непустой markup/<имя>.txt, начинающийся с *RED;
#   4. идемпотентность: повторный запуск drakon_markup.py даёт тот же sha256,
#      что и сохранённая разметка;
#   5. есть непустой printed/<имя>.txt с иконами (+----, |---, (, /)
#      и без диагностики ОШИБКА / ERROR / Illegal.
#
# Устойчивость к параллельному редактированию: если схема есть, а markup/
# или printed/ ещё нет — строка получает статус ОЖИДАЕТСЯ и не считается
# провалом (rc=0). Нарушения в существующих файлах — FAIL (rc=1).
# Генератор ищется по $DRAKON_MARKUP, в tools/ этого репозитория и в
# соседнем проекте re-siprod; при отсутствии проверка (4) — ОЖИДАЕТСЯ.
set -u

# Кириллица в regex и подсчёт «знаков», а не байтов.
if locale -a 2>/dev/null | grep -qiE '^(C\.utf8|C\.UTF-8|ru_RU\.UTF-8)$'; then
    export LC_ALL=C.UTF-8
fi

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd) || exit 1
ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd) || exit 1
cd "$ROOT" || exit 1

DRAKON_DIR="$ROOT/docs/drakon"
MARKUP_DIR="$DRAKON_DIR/markup"
PRINTED_DIR="$DRAKON_DIR/printed"

WORK=$(mktemp -d "${TMPDIR:-/tmp/.private/azizz/opencode}/drakon-check.XXXXXX") || exit 1
trap 'rm -rf "$WORK"' EXIT

# ------------------------------------------------------------- генератор ---
find_generator() {
    local c
    for c in "${DRAKON_MARKUP:-}" \
             "$ROOT/tools/drakon_markup.py" \
             "$ROOT/drakon_markup.py" \
             "$(dirname -- "$ROOT")/re-siprod/tools/drakon_markup.py" \
             "/home/azizz/Yandex.Disk/re-siprod/tools/drakon_markup.py"; do
        if [ -n "$c" ] && [ -f "$c" ]; then
            printf '%s\n' "$c"
            return 0
        fi
    done
    c=$(find /home/azizz/Yandex.Disk -maxdepth 4 -type f \
            -name drakon_markup.py -print 2>/dev/null | head -n 1)
    [ -n "$c" ] && { printf '%s\n' "$c"; return 0; }
    return 1
}
GEN=$(find_generator || true)

# ---------------------------------------------------------- метрики схемы ---
# Печатает «ИКОН МАКС_ДЛИНА»; длина считается в символах UTF-8, а не в байтах.
metrics() {
    python3 - "$1" <<'PY'
import sys, re
KW = ("ЗАГОЛОВОК ЗГ ВЕТКА ВТ ДЕЙСТВИЕ ДС КОММЕНТАРИЙ КМ ЕСЛИ ЕС ЦИКЛ ЦИ "
      "ВЫБОР ВБ ВАРИАНТ ВА АДРЕС АД КОНЕЦ КЦ ИНАЧЕ ИН ПОЛКА ПЛ ПАРАМ ПМ "
      "ВЫВОД ВД ВВОД ВВ ПАУЗА ПЗ ПЕРИОД ПР ПУСК ПУ СИНХРО СН ПАРАЛ ПП "
      "ПЕТЛЯ ПТ ГРЕБЕНКА ГР ВСТАВКА ВС ТО ДЛЯ КДЛ ПКОМ ЛКОМ").split()
pat = re.compile(r"^\s*(?:" + "|".join(KW) + r")\b")
try:
    lines = open(sys.argv[1], encoding="utf-8").read().splitlines()
except Exception:
    print("0 0")
    raise SystemExit
icons = sum(1 for l in lines
            if l.strip() and not l.lstrip().startswith("*") and pat.match(l))
longest = max((len(l) for l in lines), default=0)
print(icons, longest)
PY
}

sha256() { sha256sum "$1" 2>/dev/null | awk '{print $1}'; }
row() { printf '%-24s | %5s | %11s | %s\n' "$@"; }

printf 'ПРОВЕРКА ДРАКОН-СХЕМ (docs/drakon)\n'
printf 'Генератор разметки: %s\n' "${GEN:-НЕ НАЙДЕН (проверка идемпотентности отложена)}"
printf 'Пороги: икон >= 15, длина строки <= 80 знаков\n'
printf '\n'
row 'ФАЙЛ' 'ИКОН' 'МАРКИРОВКА' 'СТАТУС'
printf -- '-------------------------+-------+-------------+-----------------------------------------------\n'

shopt -s nullglob
files=( "$DRAKON_DIR"/*.drakon )
shopt -u nullglob

status=0
pending=0

if [ ${#files[@]} -eq 0 ]; then
    row '—' '—' '—' 'ОЖИДАЕТСЯ (нет .drakon)'
    pending=1
fi

for f in "${files[@]}"; do
    base=${f##*/}
    base=${base%.drakon}
    hard=()      # нарушения в существующих файлах
    wait=()      # ещё не созданные артефакты
    n_icons='—'
    m_status='—'

    fail()  { hard+=("$1"); }
    later() { wait+=("$1"); }

    if [ ! -s "$f" ]; then
        fail "пустая схема"
        row "$base" '—' '—' "FAIL (${hard[*]})"
        status=1
        continue
    fi

    read -r n_icons maxlen <<<"$(metrics "$f")"

    # 1. обязательные иконки и длина строк
    grep -qE '^[[:space:]]*(ЗАГОЛОВОК|ЗГ)([[:space:]]|:|$)' "$f" \
        || fail "нет ЗАГОЛОВОК"
    grep -qE '^(ВЕТКА|ВТ)([[:space:]]|:|$)' "$f" \
        || fail "нет ВЕТКА верхнего уровня"
    grep -qE '^[[:space:]]*(КОНЕЦ|КЦ)([[:space:]]|:|$)' "$f" \
        || fail "нет КОНЕЦ"
    [ "$n_icons" -ge 15 ] \
        || fail "икон $n_icons < 15"
    [ "$maxlen" -le 80 ] \
        || fail "строка $maxlen знаков > 80"

    # 2. вложенные ВЕТКА запрещены
    if grep -qE '^[[:space:]]+(ВЕТКА|ВТ)([[:space:]]|:|$)' "$f"; then
        fail "есть вложенная ВЕТКА"
    fi

    # 3. разметка *RED
    m="$MARKUP_DIR/$base.txt"
    m_bad=0
    if [ ! -s "$m" ]; then
        m_status='—'
        later "нет markup/$base.txt"
        m_bad=1
    else
        IFS= read -r first_line < "$m" || true
        case "$first_line" in
            \*RED*) ;;
            *) fail "markup не начинается с *RED"; m_bad=1 ;;
        esac

        # 4. идемпотентность / совпадение с эталонным генератором
        if [ -z "$GEN" ]; then
            later "нет drakon_markup.py"
            m_bad=1
        else
            python3 "$GEN" "$f" > "$WORK/gen1.txt" 2>"$WORK/gen1.err"
            python3 "$GEN" "$f" > "$WORK/gen2.txt" 2>"$WORK/gen2.err"
            h1=$(sha256 "$WORK/gen1.txt")
            h2=$(sha256 "$WORK/gen2.txt")
            hm=$(sha256 "$m")
            if [ -z "$h1" ] || [ "$h1" != "$h2" ]; then
                fail "генератор не детерминирован"
                m_bad=1
            elif [ "$h1" != "$hm" ]; then
                fail "markup != drakon_markup.py"
                m_bad=1
            fi
        fi
        if [ "$m_bad" -eq 0 ]; then m_status='OK'; else m_status='FAIL'; fi
    fi

    # 5. реальная печать ДРАКОН-редактора
    p="$PRINTED_DIR/$base.txt"
    if [ ! -s "$p" ]; then
        later "нет printed/$base.txt"
    else
        grep -qF -- '+--' "$p" || fail "печать: нет +----"
        # В GOST-печати боковина иконы — '|' (рамка страницы — 'I').
        if ! grep -qF -- '|' "$p" && ! grep -qF -- 'I' "$p"; then
            fail "печать: нет вертикальной черты иконы (|---)"
        fi
        grep -qF -- '(' "$p"  || fail "печать: нет ("
        grep -qF -- '/' "$p"  || fail "печать: нет /"
        # Диагностика конвейера, а не подписи икон: строки с рисунком
        # (+ | / ( )) отбрасываем — там ОШИБКА/ERROR могут быть текстом схемы.
        diag=$(grep -Ei 'ОШИБКА|ERROR|Illegal' "$p" \
               | grep -vE '[+|/()]' || true)
        if [ -n "$diag" ]; then
            fail "печать: диагностика ($(printf '%s' "$diag" | head -n 1))"
        fi
    fi

    if [ ${#hard[@]} -eq 0 ] && [ ${#wait[@]} -eq 0 ]; then
        row "$base" "$n_icons" "$m_status" 'OK'
        continue
    fi

    reasons=("${hard[@]}" "${wait[@]}")
    if [ ${#hard[@]} -gt 0 ]; then
        row "$base" "$n_icons" "$m_status" "FAIL (${reasons[*]})"
        status=1
    else
        row "$base" "$n_icons" "$m_status" "ОЖИДАЕТСЯ (${reasons[*]})"
        pending=1
    fi
done

printf -- '-------------------------+-------+-------------+-----------------------------------------------\n'
if [ "$status" -ne 0 ]; then
    printf 'FAIL: ДРАКОН-схемы не прошли проверку (см. таблицу)\n' >&2
elif [ "$pending" -eq 1 ]; then
    printf 'ОЖИДАЕТСЯ: часть артефактов (markup/printed) ещё не создана\n'
else
    printf 'OK: все ДРАКОН-схемы, разметка и печать прошли проверку\n'
fi
exit "$status"
