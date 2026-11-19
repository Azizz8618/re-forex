#!/usr/bin/env python3
"""Парсер таблицы системных вызовов (экстракодов) из rukava.be.

Источник: /home/azizz/Yandex.Disk/re-dispak/rukava.be,
раздел 1.4 «ПЕРЕЧЕНЬ СИСТЕМНЫХ ВЫЗВОВ (ЭКСТРАКОДОВ)».

Строки таблицы имеют вид::

    *| Э50 0000     | SIN                          |   263|
    *| Э53 0041     | УСТАНОВКА ...                |   204|
    *|              | ПАКЕТЕ ОПЕРАЦИОННОЙ ...      |      |

Продолжения описаний (пустая колонка кода) приклеиваются к предыдущей
записи.  Ключ словаря — пара (код, информационное слово), например
``('Э50', '0131')``; значение — кортеж ``(описание, страница, номер_строки)``.

Примеры::

    python3 tools/extract_codes.py --list
    python3 tools/extract_codes.py --find Э50/0000
    python3 tools/extract_codes.py --find 'Э53 0041'
    python3 tools/extract_codes.py --json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

DEFAULT_SOURCE = Path("/home/azizz/Yandex.Disk/re-dispak/rukava.be")

# Ключ: (Э50, 0131).  Значение: (описание, страница, строка файла).
Entry = Tuple[str, str, int]
CodeTable = Dict[Tuple[str, str], Entry]

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


def make_comment(code: str, info: str, table: CodeTable) -> str:
    """Построить встроенный комментарий-расшифровку для одного экстракода."""
    entry = lookup(table, code, info)
    if entry is None:
        return f". {code} {info} = НЕ НАЙДЕНО в rukava.be"
    desc, page, lineno = entry
    return f". {code} {info} = {desc}, стр.{page} [rukava.be:{lineno}]"


def scan_line(line: str, equs: Dict[str, str]) -> List[Tuple[str, str, str]]:
    """Экстракоды со информационным словом в одной строке.

    Возвращает список ``(код, информационное_слово, исходный_токен)``.
    """
    out: List[Tuple[str, str, str]] = []
    # Не сканируем собственные комментарии-расшифровки вида ". Э57 6 = ...":
    # иначе они сами начинают выглядеть как ещё одно вхождение экстракода.
    line = re.split(r"\s+\.\s+Э[0-7]{2}\s+", line, maxsplit=1)[0]
    for rx in (OPCODE_RE, MNEMO_RE):
        for m in rx.finditer(line):
            raw = m.group(2).strip()
            if not raw or "=" in raw or ":" in raw or "*" in raw:
                continue  # метка/литерал, а не информационное слово
            resolved = resolve_equ(raw, equs)
            out.append(("Э" + m.group(1), resolved or raw, raw))
    return out


def scan_sources(root: Path = Path("src"), table: Optional[CodeTable] = None
                 ) -> List[Dict[str, object]]:
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
            for code, info, raw in scan_line(line, equs):
                entry = lookup(table, code, info)
                found.append({
                    "file": str(path), "line": lineno, "code": code,
                    "info": info, "token": raw,
                    "description": entry[0] if entry else None,
                    "page": entry[1] if entry else None,
                    "source_line": entry[2] if entry else None,
                    "comment": make_comment(code, info, table),
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
    ap.add_argument("--source", type=Path, default=DEFAULT_SOURCE,
                    help="путь к rukava.be (по умолчанию %(default)s)")
    ap.add_argument("--list", action="store_true", help="вывести всю таблицу")
    ap.add_argument("--find", metavar="Э50/0000",
                    help="найти код (формы: Э50/0000, 'Э50 0000', Э50)")
    ap.add_argument("--json", action="store_true", help="вывести таблицу в JSON")
    ap.add_argument("--scan", action="store_true",
                    help="просканировать src/*.mad и src/lib21/*.mad")
    ap.add_argument("--root", type=Path, default=Path("src"),
                    help="корень исходников для --scan (по умолчанию %(default)s)")
    args = ap.parse_args(argv)

    try:
        table = parse_table(args.source)
    except OSError as exc:
        print(f"ОШИБКА: не удалось прочитать {args.source}: {exc}", file=sys.stderr)
        return 2

    if args.scan:
        rows = scan_sources(args.root, table)
        if args.json:
            print(json.dumps(rows, ensure_ascii=False, indent=2))
            return 0
        hits = sum(1 for r in rows if r["description"] is not None)
        for r in rows:
            mark = "НАЙДЕНО" if r["description"] is not None else "не найдено"
            print(f"{r['file']}:{r['line']}: {r['code']} {r['info']} "
                  f"[{r['token']}] -> {mark}")
        print(f"\nВсего вхождений: {len(rows)}, расшифровано: {hits}, "
              f"не найдено: {len(rows) - hits}", file=sys.stderr)
        return 0

    if args.json and not args.find:
        out = [
            {"code": code, "info": info, "description": desc,
             "page": page, "source_line": lineno}
            for (code, info), (desc, page, lineno) in sorted(table.items())
        ]
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0

    if args.find:
        code, info = parse_query(args.find)
        found = []
        for (c, i), entry in sorted(table.items()):
            if c == code and (not info or i == info or
                              (info.lstrip("0") and i.lstrip("0") == info.lstrip("0"))):
                found.append((c, i, entry))
        if not found:
            print(f"Экстракод {args.find}: не найдено в rukava.be")
            return 1
        for c, i, entry in found:
            print(format_entry(c, i, entry))
        return 0

    if args.list or not args.json:
        for (code, info), entry in sorted(table.items()):
            print(format_entry(code, info, entry))
        print(f"\nВсего записей: {len(table)}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
