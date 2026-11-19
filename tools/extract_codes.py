#!/usr/bin/env python3
"""Парсер таблицы системных вызовов (экстракодов) из rukava.be и книги Тюрина.

КЛАССИФИКАЦИЯ КОДОВ (критическое правило): экстракоды — только 050..077.
Коды 020..047 (*20, *21, *33, *36, *46, *47 и др.) — обычные КОМАНДЫ БЭСМ-6
по таблицам besm6tape.py / disbesm6.c; они НЕ требуют расшифровки из
rukava.be или книги Тюрина.  См. ``classify_opcode()``.

Первичный источник: /home/azizz/Yandex.Disk/re-dispak/rukava.be,
раздел 1.4 «ПЕРЕЧЕНЬ СИСТЕМНЫХ ВЫЗВОВ (ЭКСТРАКОДОВ)».

Вторичный источник: /home/azizz/Yandex.Disk/re-dispak/docs/tyurin1985/extract-codes.json
(описания экстракодов из OCR книги В. Ф. Тюрина «Операционная система
ДИСПАК», 1985, Приложение П и §2.4).  Приоритет: rukava.be, затем Тюрин.

Выбор источника: ``--source rukava|tyurin|all`` (по умолчанию ``all``).

Строки таблицы имеют вид::

    *| Э50 0000     | SIN                          |   263|
    *| Э53 0041     | УСТАНОВКА ...                |   204|
    *|              | ПАКЕТЕ ОПЕРАЦИОННОЙ ...      |      |

Продолжения описаний (пустая колонка кода) приклеиваются к предыдущей
записи.  Ключ словаря — пара (код, информационное слово), например
``('Э50', '0131')``; значение — кортеж ``(описание, страница, номер_строки)``.

Примеры::

    python3 tools/extract_codes.py --list
    python3 tools/extract_codes.py --find Э57/1263
    python3 tools/extract_codes.py --find 'Э53 0041'
    python3 tools/extract_codes.py --find Э57/1263 --source tyurin
    python3 tools/extract_codes.py --json
    python3 tools/extract_codes.py --scan --source all
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_SOURCE = Path("/home/azizz/Yandex.Disk/re-dispak/rukava.be")
DEFAULT_TYURIN = Path("/home/azizz/Yandex.Disk/re-dispak/docs/tyurin1985/extract-codes.json")
SOURCES = ("rukava", "tyurin", "all")

# ── Классификация кодов: экстракоды (050–077) vs команды (020–047) ────────────
# КРИТИЧЕСКОЕ ПРАВИЛО: в ДИСПАКе экстракоды — только коды 050..077.
# Коды 020..047 являются обычными КОМАНДАМИ БЭСМ-6 (в том числе *20, *21,
# *33, *36, *46, *47).  Источники таблиц:
#   /home/azizz/Yandex.Disk/besm6-new/besm6.net/tools/besm6tape.py
#       string 25  — SHORT "*33";   string 26 — SHORT "*46", "*47"
#       string 36  — SHORT_BEMSH "счп" (для *33)
#       string 37  — SHORT_BEMSH "соп", "э47" (для *46, *47)
#       strings 44–45 / 48–49 — LONG и LONG_BEMSH (*20…*37 / э20…цикл)
#   /home/azizz/Yandex.Disk/dispak/disbesm6/disbesm6.c:83–84
#       "Э46" (0x026000) и "Э47" (0x027000) — OPCODE_IMM, BASIC, НЕ экстракоды.
# Значение: (MADLEN-мнемоника, БЭМШ-мнемоника, ссылка на таблицу).
COMMAND_OPCODES: Dict[str, Tuple[str, str, str]] = {
    # LONG 020–037 (besm6tape.py:44–45 / 48–49)
    "20": ("*20", "э20", "besm6tape.py:44,48"),
    "21": ("*21", "э21", "besm6tape.py:44,48"),
    "22": ("utc", "мода", "besm6tape.py:44,48"),
    "23": ("wtc", "мод", "besm6tape.py:44,48"),
    "24": ("vtm", "уиа", "besm6tape.py:44,48"),
    "25": ("utm", "слиа", "besm6tape.py:44,48"),
    "26": ("uza", "по", "besm6tape.py:44,48"),
    "27": ("u1a", "пе", "besm6tape.py:44,48"),
    "30": ("uj", "пб", "besm6tape.py:45,49"),
    "31": ("vjm", "пв", "besm6tape.py:45,49"),
    "32": ("ij", "выпр", "besm6tape.py:45,49"),
    "33": ("*33 / stop", "счп", "besm6tape.py:25,36 (SHORT *33/счп); 45,49 (LONG stop/стоп)"),
    "34": ("vzm", "пио", "besm6tape.py:45,49"),
    "35": ("v1m", "пино", "besm6tape.py:45,49"),
    "36": ("*36", "втбрз", "besm6tape.py:45,49"),
    "37": ("vlm", "цикл", "besm6tape.py:45,49"),
    # SHORT 040–047 (besm6tape.py:26 / 37; 46–47 также disbesm6.c:83–84)
    "40": ("ati", "уи", "besm6tape.py:26,37"),
    "41": ("sti", "уим", "besm6tape.py:26,37"),
    "42": ("ita", "счи", "besm6tape.py:26,37"),
    "43": ("its", "счим", "besm6tape.py:26,37"),
    "44": ("mtj", "уии", "besm6tape.py:26,37"),
    "45": ("j+m", "сли", "besm6tape.py:26,37"),
    "46": ("*46", "соп", "besm6tape.py:26,37; disbesm6.c:83"),
    "47": ("*47", "э47", "besm6tape.py:26,37; disbesm6.c:84"),
}


def classify_opcode(code_octal: str) -> Tuple[str, str]:
    """Классифицировать восьмеричный код команды/экстракода.

    Возвращает ``(категория, мнемоника)``:
      * ``('extract', 'Э50')``  — настоящий экстракод, код 050..077;
      * ``('command', 'втбрз')`` — команда БЭСМ-6, код 020..047
        (мнемоника — БЭМШ-имя из besm6tape.py/disbesm6.c);
      * ``('unknown', '')``     — код вне диапазонов 020..077.

    >>> classify_opcode('36')
    ('command', 'втбрз')
    >>> classify_opcode('050')
    ('extract', 'Э50')
    """
    raw = str(code_octal).strip().upper().lstrip("Э*")
    try:
        value = int(raw, 8)
    except ValueError:
        return ("unknown", "")
    if 0o20 <= value <= 0o47:
        norm = format(value, "02o")
        mnemonic = COMMAND_OPCODES.get(norm, (norm, norm, ""))[1]
        return ("command", mnemonic)
    if 0o50 <= value <= 0o77:
        return ("extract", "Э" + format(value, "02o"))
    return ("unknown", "")


def command_ref(code_octal: str) -> str:
    """Ссылка на таблицу, подтверждающую, что код — команда, а не экстракод."""
    norm = format(int(str(code_octal).strip().lstrip("Э*"), 8), "02o")
    return COMMAND_OPCODES.get(norm, (norm, norm, "besm6tape.py"))[2]


def make_command_comment(code_octal: str, info: str = "") -> str:
    """Канонический комментарий для команды, ошибочно названной экстракодом."""
    kind, mnemonic = classify_opcode(code_octal)
    if kind != "command":
        return ""
    norm = format(int(str(code_octal).strip().lstrip("Э*"), 8), "02o")
    info_part = f" {info}" if info else ""
    return (f". опк {norm} ({mnemonic}){info_part} = КОМАНДА БЭСМ-6 "
            f"«{mnemonic}», не экстракод [{command_ref(norm)}]")

# Ключ: (Э50, 0131).  Значение: (описание, страница, строка файла).
Entry = Tuple[str, str, int]
CodeTable = Dict[Tuple[str, str], Entry]
TyurinData = Dict[str, Any]
# Унифицированная находка: (описание, страница, ссылка, имя_источника).
Found = Tuple[str, str, str, str]

ROW_RE = re.compile(
    r"^\*\|\s*(Э\d{2})(?:\s+([^\s|]+))?\s*\|\s*(.*?)\s*\|\s*([^|]*?)\s*\|\s*$"
)
CONT_RE = re.compile(r"^\*\|\s*\|\s*(.*?)\s*\|\s*([^|]*?)\s*\|\s*$")


def parse_table_rows(path: Path = DEFAULT_SOURCE) -> List[Tuple[str, str, str, str, int]]:
    """Все строки таблицы: (код, и.слово, описание, страница, линия).

    В таблице есть повторяющиеся ключи (например ``Э72 А`` встречается
    10 раз — разные операции выбираются другими параметрами), поэтому
    полный список строк хранится отдельно от словаря.
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    rows: List[Tuple[str, str, str, str, int]] = []
    for lineno, line in enumerate(text.splitlines(), 1):
        m = ROW_RE.match(line)
        if m:
            rows.append((
                m.group(1),
                m.group(2) or "",
                m.group(3).strip(),
                m.group(4).strip(),
                lineno,
            ))
            continue
        c = CONT_RE.match(line)
        if c and rows:
            extra = c.group(1).strip()
            if extra:
                code, info, desc, page, first = rows[-1]
                page2 = c.group(2).strip()
                rows[-1] = (code, info, (desc + " " + extra).strip(),
                            page or page2, first)
    return rows


def parse_table(path: Path = DEFAULT_SOURCE) -> CodeTable:
    """Словарь {(код, и.слово): (описание, страница, линия)}.

    Повторяющиеся строки с одним ключом объединяются: описания через
    « / », страницы через «, », линия берётся от первой строки.
    """
    table: CodeTable = {}
    for code, info, desc, page, lineno in parse_table_rows(path):
        key = (code, info)
        if key not in table:
            table[key] = (desc, page, lineno)
        else:
            old_desc, old_page, old_line = table[key]
            table[key] = (
                f"{old_desc} / {desc}" if desc not in old_desc else old_desc,
                f"{old_page}, {page}" if page and page not in old_page.split(", ") else old_page,
                old_line,
            )
    return table


def norm_info(info: str) -> str:
    """Нормализовать информационное слово: убрать суффикс B и ведущие нули.

    Числа в таблицы rukava.be записаны в восьмеричной системе (0000, 0131,
    1202, 7703), поэтому перевода в десятичную систему НЕ делаем: ``20`` и
    ``0020`` — одно и то же слово, а ``20B`` означает восьмеричное 20.
    """
    info = info.strip().rstrip("B").lstrip("0")
    return info or "0"


def lookup(table: CodeTable, code: str, info: str) -> Optional[Entry]:
    """Найти запись по коду/информационному слову (сравнение по восьмеричному значению)."""
    code = code.strip().upper()
    key = (code, norm_info(info))
    for (c, i), entry in table.items():
        if c == code and norm_info(i) == key[1]:
            return entry
    return None


def format_entry(code: str, info: str, entry: Optional[Entry]) -> str:
    if entry is None:
        return f"{code} {info} -> НЕ НАЙДЕНО в rukava.be"
    desc, page, lineno = entry
    return f"{code} {info} -> {desc} (стр.{page}) [rukava.be:{lineno}]"


# ---------------------------------------------------------------------------
# Второй источник: книга Тюрина (1985).
# ---------------------------------------------------------------------------

def load_tyurin(path: Path = DEFAULT_TYURIN) -> Optional[TyurinData]:
    """Загрузить JSON с описаниями экстракодов из книги Тюрина.

    Формат первого агента: ``{"Э057:0000": {"desc": ..., "page": 264,
    "confidence": ...}, ...}``.  Возвращает ``None``, если файл отсутствует
    или повреждён (тогда работает только rukava.be).
    """
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    return data


# Краткие названия экстракодов по указателю книги (используются как fallback
# по номеру кода, когда конкретное информационное слово в книге не найдено).
TYURIN_CODE_TITLES: Dict[str, str] = {
    "Э50": "СЕРВИСНЫЕ ЭКСТРАКОДЫ И ЭЛЕМЕНТАРНЫЕ ФУНКЦИИ (ИР 050 A)",
    "Э51": "COS (ИР 051 A)",
    "Э52": "COS (ИР 052 A)",
    "Э53": "ARCTAN / СОБЫТИЯ И СВЯЗЬ МЕЖДУ ЗАДАЧАМИ (ИР 053 A)",
    "Э54": "ARCSIN (ИР 054 A)",
    "Э55": "LN (ИР 055 A)",
    "Э56": "EXP (ИР 056 A)",
    "Э57": "ВЫДЕЛЕНИЕ ЦЕЛОЙ ЧАСТИ (ENTIER) / СИСТЕМНАЯ ОПЕРАЦИЯ (ИР 057 A)",
    "Э62": "СИСТЕМНЫЕ ЭКСТРАКОДЫ УПРАВЛЕНИЯ ЗАДАЧАМИ И ТЕРМИНАЛАМИ (ИР 062 A)",
    "Э63": "ЭКСТРАКОДЫ ВРЕМЕНИ РЕШЕНИЯ ЗАДАЧИ (ИР 063 A)",
    "Э64": "УПРАВЛЕНИЕ РЕЖИМОМ ЛИСТОВАНИЯ ПРИ ПЕЧАТИ НА АЦПУ (ИР 064 A)",
    "Э73": "ВВОД МАССИВА С НОМЕРОМ N+1 В ПАМЯТЬ ЗАДАЧИ (ИР 073 A)",
    "Э76": "СВЯЗЬ БЭСМ-6 С ЭВМ М-6000 / Т-1600 (ИР 076 A)",
}


def _tyurin_entries(data: Optional[TyurinData]) -> Dict[Tuple[str, str], Dict[str, Any]]:
    """Индекс записей Тюрина: (код, восьмеричное_слово) -> запись."""
    out: Dict[Tuple[str, str], Dict[str, Any]] = {}
    if not data:
        return out
    for key, val in data.items():
        if ":" not in key or not isinstance(val, dict):
            continue
        raw_code, raw_info = key.split(":", 1)
        code = "Э" + raw_code.lstrip("Э").lstrip("0")
        info = norm_info(raw_info)
        out[(code, info)] = val
    return out


def lookup_tyurin(data: Optional[TyurinData], code: str, info: str) -> Optional[Entry]:
    """Найти описание у Тюрина: сначала пара (код/слово), затем код целиком.

    Возвращает ``(описание, страница, 'tyurin1985')``.
    """
    if not data:
        return None
    code = code.strip().upper()
    entries = _tyurin_entries(data)
    hit = entries.get((code, norm_info(info)))
    if hit is not None:
        desc = str(hit.get("desc", "")).strip()
        page = str(hit.get("page", 264))
        if desc:
            return (desc, page, "tyurin1985")
    # Fallback по номеру экстракода: описание класса экстракодов из книги.
    title = TYURIN_CODE_TITLES.get(code)
    if title is not None:
        pages = [str(v.get("page", 264)) for (c, _), v in sorted(entries.items())
                 if c == code and v.get("page")]
        return (title, pages[0] if pages else "264", "tyurin1985")
    return None


def lookup_all(code: str, info: str, table: CodeTable,
               tyurin: Optional[TyurinData] = None,
               source: str = "all") -> Optional[Found]:
    """Унифицированный поиск с приоритетом rukava.be > Тюрин.

    ``source``: ``rukava`` — только rukava.be, ``tyurin`` — только Тюрин,
    ``all`` — оба (сначала rukava.be).
    """
    if source in ("rukava", "all"):
        entry = lookup(table, code, info)
        if entry is not None:
            return (entry[0], entry[1], f"rukava.be:{entry[2]}", "rukava.be")
    if source in ("tyurin", "all"):
        entry = lookup_tyurin(tyurin, code, info)
        if entry is not None:
            return (entry[0], entry[1], entry[2], "tyurin1985")
    return None


# ---------------------------------------------------------------------------
# Сканирование аннотированных МАДЛЕН-текстов.
# ---------------------------------------------------------------------------

EQU_RE = re.compile(
    r"^\s*([A-Za-z][A-Za-z0-9_#$]*)\s*,\s*EQU\s*,\s*(.*?)\s*(?:[.;].*)?$"
)
# Экстракод в мнемонике: *NN,ARG  (ARG — простой операнд, не метка/литерал).
OPCODE_RE = re.compile(
    r"(?<![A-Za-z0-9_*])\*([0-7]{2})(?![0-7])\s*,\s*([A-Za-z0-9_#$()+\-=:]+)"
)
# Экстракод в тексте: ЭNN ARG.
MNEMO_RE = re.compile(
    r"(?<![A-Za-z0-9_])Э([0-7]{2})(?![0-7])\s+([A-Za-z0-9_#$()+\-=:]+)"
)
NUMBER_RE = re.compile(r"^(?:0o)?([0-7]+)[bB]?$|^\d+$")


def resolve_equ(name: str, equs: Dict[str, str], seen: Optional[set] = None) -> Optional[str]:
    """Разрешить символическое информационное слово в восьмеричную строку.

    Поддерживаются восьмеричные (``502B``, ``0o502``), десятичные (``47``),
    символические ссылки и простые выражения ``A+B`` / ``A-B``.
    Возвращает ``None``, если разрешить значение нельзя (например TEXT-литерал).
    """
    if seen is None:
        seen = set()
    name = name.strip()
    if name in seen:
        return None
    seen.add(name)
    if name.startswith('-'):
        val = resolve_equ(name[1:], equs, seen)
        return ('-' + val) if val is not None else None
    raw = equs.get(name)
    if raw is None:
        return None
    raw = raw.strip()

    def atom(tok: str) -> Optional[int]:
        tok = tok.strip()
        if not tok:
            return None
        m = re.fullmatch(r"([0-7]+)[bB]", tok)
        if m:
            return int(m.group(1), 8)
        m = re.fullmatch(r"0o([0-7]+)", tok)
        if m:
            return int(m.group(1), 8)
        if re.fullmatch(r"\d+", tok):
            return int(tok)
        if re.fullmatch(r"[A-Za-z][A-Za-z0-9_#$]*", tok):
            sub = resolve_equ(tok, equs, seen)
            return int(sub, 8) if sub is not None else None
        return None

    # Унарный минус: -EDC008.
    if raw.startswith('-'):
        val = atom(raw[1:])
        return ('-' + format(val, 'o')) if val is not None else None
    # Простое выражение из двух операндов и одного + или -.
    m = re.fullmatch(r"([^+\-]+)([+\-])(.+)", raw)
    if m:
        a, op, b = atom(m.group(1)), m.group(2), atom(m.group(3))
        if a is not None and b is not None:
            return format(a + b if op == "+" else a - b, "o")
    val = atom(raw)
    return format(val, "o") if val is not None else None


def make_comment(code: str, info: str, table: CodeTable,
                 tyurin: Optional[TyurinData] = None,
                 source: str = "all") -> str:
    """Построить встроенный комментарий для одного кода.

    Для команд (020..047) расшифровка из rukava.be/Тюрина НЕ требуется —
    возвращается пометка «КОМАНДА БЭСМ-6, не экстракод» со ссылкой на таблицу.
    Для настоящих экстракодов (050..077) — расшифровка по источникам.
    """
    kind, _mnemonic = classify_opcode(code)
    if kind == "command":
        return make_command_comment(code, info)
    entry = lookup_all(code, info, table, tyurin, source)
    if entry is None:
        return f". {code} {info} = НЕ НАЙДЕНО в rukava.be"
    desc, page, ref, _src = entry
    return f". {code} {info} = {desc}, стр.{page} [{ref}]"


def scan_line(line: str, equs: Dict[str, str]) -> List[Tuple[str, str, str, str, str]]:
    """Коды с информационным словом в одной строке.

    Возвращает список ``(код, информационное_слово, исходный_токен,
    категория, мнемоника)``.  Категория — ``extract`` (050..077),
    ``command`` (020..047) или ``unknown``.
    """
    out: List[Tuple[str, str, str, str, str]] = []
    # Не сканируем собственные комментарии вида ". Э57 6 = ..." или
    # ". опк 36 (втбрз) 7417 = ...": иначе они сами выглядят как вхождение.
    line = re.split(r"\s+\.\s+(?:Э[0-7]{2}|опк)\s+", line, maxsplit=1)[0]
    for rx in (OPCODE_RE, MNEMO_RE):
        for m in rx.finditer(line):
            raw = m.group(2).strip()
            if not raw or "=" in raw or ":" in raw or "*" in raw:
                continue  # метка/литерал, а не информационное слово
            resolved = resolve_equ(raw, equs)
            code = m.group(1)
            kind, mnemonic = classify_opcode(code)
            out.append(("Э" + code, resolved or raw, raw, kind, mnemonic))
    return out


def scan_sources(root: Path = Path("src"), table: Optional[CodeTable] = None,
                 tyurin: Optional[TyurinData] = None,
                 source: str = "all") -> List[Dict[str, object]]:
    """Просканировать ``src/*.mad`` и ``src/lib21/*.mad``."""
    if table is None:
        table = parse_table()
    found: List[Dict[str, object]] = []
    files = sorted(root.glob("*.mad")) + sorted((root / "lib21").glob("*.mad"))
    for path in files:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        equs: Dict[str, str] = {}
        for line in lines:
            m = EQU_RE.match(line)
            if m:
                equs[m.group(1)] = m.group(2)
        for lineno, line in enumerate(lines, 1):
            for code, info, raw, kind, mnemonic in scan_line(line, equs):
                entry = (None if kind == "command"
                         else lookup_all(code, info, table, tyurin, source))
                found.append({
                    "file": str(path), "line": lineno, "code": code,
                    "info": info, "token": raw,
                    "kind": kind, "mnemonic": mnemonic,
                    "command_ref": command_ref(code) if kind == "command" else None,
                    "description": entry[0] if entry else None,
                    "page": entry[1] if entry else None,
                    "source_line": entry[2] if entry else None,
                    "source": entry[3] if entry else None,
                    "comment": make_comment(code, info, table, tyurin, source),
                })
    return found


def parse_query(q: str) -> Tuple[str, str]:
    q = q.strip().replace("/", " ").replace(",", " ")
    parts = q.split()
    code = parts[0].upper() if parts else ""
    info = parts[1] if len(parts) > 1 else ""
    return code, info


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", choices=SOURCES, default="all",
                    help="источник расшифровок: rukava, tyurin или all "
                         "(по умолчанию all: rukava.be, затем Тюрин)")
    ap.add_argument("--rukava", type=Path, default=DEFAULT_SOURCE,
                    help="путь к rukava.be (по умолчанию %(default)s)")
    ap.add_argument("--tyurin", type=Path, default=DEFAULT_TYURIN,
                    help="путь к JSON Тюрина (по умолчанию %(default)s)")
    ap.add_argument("--list", action="store_true", help="вывести всю таблицу")
    ap.add_argument("--find", metavar="Э57/1263",
                    help="найти код (формы: Э57/1263, 'Э53 0041', Э50)")
    ap.add_argument("--json", action="store_true", help="вывести таблицу в JSON")
    ap.add_argument("--scan", action="store_true",
                    help="просканировать src/*.mad и src/lib21/*.mad")
    ap.add_argument("--root", type=Path, default=Path("src"),
                    help="корень исходников для --scan (по умолчанию %(default)s)")
    args = ap.parse_args(argv)

    try:
        table = parse_table(args.rukava)
    except OSError as exc:
        print(f"ОШИБКА: не удалось прочитать {args.rukava}: {exc}", file=sys.stderr)
        return 2
    tyurin = load_tyurin(args.tyurin) if args.source in ("tyurin", "all") else None

    if args.scan:
        rows = scan_sources(args.root, table, tyurin, args.source)
        if args.json:
            print(json.dumps(rows, ensure_ascii=False, indent=2))
            return 0
        extracts = [r for r in rows if r["kind"] == "extract"]
        commands = [r for r in rows if r["kind"] == "command"]
        hits = sum(1 for r in extracts if r["description"] is not None)
        for r in rows:
            if r["kind"] == "command":
                print(f"{r['file']}:{r['line']}: {r['code']} {r['info']} "
                      f"[{r['token']}] -> КОМАНДА БЭСМ-6 «{r['mnemonic']}», "
                      f"НЕ экстракод [{r['command_ref']}]")
                continue
            mark = "НАЙДЕНО" if r["description"] is not None else "не найдено"
            src = r["source"] or "-"
            print(f"{r['file']}:{r['line']}: {r['code']} {r['info']} "
                  f"[{r['token']}] -> {mark} [{src}]")
        print(f"\nВсего вхождений: {len(rows)}; экстракоды (050..077): "
              f"{len(extracts)} (расшифровано: {hits}, не найдено: "
              f"{len(extracts) - hits}); команды (020..047, НЕ экстракоды): "
              f"{len(commands)} (источник: {args.source})", file=sys.stderr)
        return 0

    if args.json and not args.find:
        out = [
            {"code": code, "info": info, "description": desc,
             "page": page, "source_line": lineno, "source": "rukava.be"}
            for (code, info), (desc, page, lineno) in sorted(table.items())
        ]
        if tyurin:
            for (code, info), val in sorted(_tyurin_entries(tyurin).items()):
                out.append({"code": code, "info": info,
                            "description": val.get("desc", ""),
                            "page": val.get("page", 264),
                            "source_line": None, "source": "tyurin1985"})
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    if args.find:
        code, info = parse_query(args.find)
        found = []
        for (c, i), entry in sorted(table.items()):
            if c == code and (not info or i == info or
                              (info.lstrip("0") and i.lstrip("0") == info.lstrip("0"))):
                found.append((c, i, f"{entry[0]} (стр.{entry[1]}) [rukava.be:{entry[2]}]"))
        # Добавляем результат из Тюрина, если пара ещё не найдена в rukava.be.
        if not found and tyurin:
            entry = lookup_tyurin(tyurin, code, info)
            if entry is not None:
                found.append((code, info,
                              f"{entry[0]} (стр.{entry[1]}) [{entry[2]}]"))
        if not found:
            print(f"Экстракод {args.find}: не найдено ни в rukava.be, ни у Тюрина")
            return 1
        for c, i, text in found:
            print(f"{c} {i} -> {text}")
        return 0

    if args.list or not args.json:
        for (code, info), entry in sorted(table.items()):
            print(format_entry(code, info, entry))
        print(f"\nВсего записей rukava.be: {len(table)}", file=sys.stderr)
        if tyurin:
            print(f"Записей у Тюрина: {len(_tyurin_entries(tyurin))} пар",
                  file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
