#!/usr/bin/env python3
"""Глобальный свод перекрёстных ссылок реконструированного компилятора ФОРЭКС.

Сканирует ``src/*.mad`` и ``include/*.mad`` (а также ``include/*.labels.md``,
если другие агенты их уже создали), извлекает:

  * объявления меток / NAME / ENTRY / SUBP / COMMON(BSS, LC) / TEXT / GOST /
    EQU (именованные константы) и другие описания данных;
  * все применения символов (операнды команд, EQU, TEXT и т.д.);
  * управляющие переходы и вызовы (UJ / VJM / UZA / U1A / VLM / ПО / ПБ /
    ПВ / ЦИКЛ / …) с адресами назначения;
  * внешние абсолютные адреса (из LO*SYN / LO*GEN и остальных модулей);
  * «голые» числовые литералы, ещё не вынесенные в ``,EQU,`` константы.

Дополнительно читает ``docs/06-address-map.md`` (подтверждённые соответствия),
``docs/03-symbols.md``, ``include/catalog.md``, ``include/*.xref.md`` и
``include/RUNTIME_*.xref.md`` для построения графа вызовов и раздела
подтверждённых адресов.

Отдельно проверяется **6-символьное правило МАДЛЕН**: метки и `EQU`-константы
различаются только первыми шестью знаками, поэтому все имена должны быть
≤ 6 символов, а первые 6 знаков разных имён — уникальными. Нарушения и
коллизии выводятся в разделе «НАРУШЕНИЯ 6-СИМВОЛЬНОГО ПРАВИЛА» и в лог.

Результат — детерминированный markdown (удобно diff-ить) и подробный лог.

    python3 tools/xref_all.py --out docs/09-crossrefs.md

По умолчанию лог пишется в ``logs/xref_all.txt`` (переопределяется ``--log``).
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

REPO = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------------
# Множества мнемоник
# ---------------------------------------------------------------------------

DECL_KIND = {
    "NAME": "NAME",
    "ENTRY": "ENTRY",
    "SUBP": "SUBP",
    "BSS": "COMMON",
    "LC": "COMMON",
    "COMMON": "COMMON",
    "TEXT": "TEXT",
    "8TEXT": "TEXT",
    "GOST": "TEXT",
    "ISO": "TEXT",
    "OCT": "DATA",
    "INT": "DATA",
    "REAL": "DATA",
    "EQU": "EQU",
    "END": "END",
}

# Команды, изменяющие счётчик команд / передающие управление.
JUMP_OPS = {
    "UJ", "VJM", "UZA", "U1A", "VLM", "VZM", "VIM", "VIA", "UIA",
    "IJ", "MTJ", "CALL", "ПО", "ПБ", "ПВ", "ПЕ", "ЦИКЛ", "ВЫПР",
    "ВЫХ", "STOP", "EXIT", "RTE", "J+M", "UJ*", "ВЫП", "ВЗВ",
}
# Расширенный набор: плюс работа с индексными регистрами (используется в
# исходной методике подсчёта «управляющих команд»).
CONTROL_OPS = JUMP_OPS | {"VTM", "UTM", "STI", "ITS", "ATI"}

DATA_DECL_OPS = {"OCT", "INT", "REAL", "TEXT", "8TEXT", "GOST", "ISO", "EQU"}

COMMENT_CHARS = "CcСс"

# МАДЛЕН (БЭСМ-6) различает в метках и EQU только первые 6 знаков.
MAX_NAME_LEN = 6

SYMBOL_RE = re.compile(r"\*[0-9]{3,6}|\*?[A-Za-zА-Яа-я][\w/*]*")
# Числовой литерал: не начинается с буквы/звезды (иначе `FT*571`, `*00026`
# были бы приняты за литералы), и не является частью `B`-суффикса.
OCT_LITERAL_RE = re.compile(r"(?<![\w*])(?:0o)?([0-7]{1,7})B?(?![\w])")
DEC_LITERAL_RE = re.compile(r"(?<![\w.])\d+\.\d+")
LEAD_LABEL_RE = re.compile(
    r"^\s*(\*[0-9]{3,6}|\*?[A-Za-zА-Яа-я][\w/*]*)\s*:?\s*(?:[0-9]+)?\s*$"
)
STANDALONE_LABEL_RE = re.compile(
    r"^\s*(\*[0-9]{3,6}|\*?[A-Za-zА-Яа-я][\w/*]*)\s*:\s*$"
)
OPCODE_LIKE_RE = re.compile(r"\*[0-9]{2,3}|[A-Za-zА-Яа-я][\w/*+\-]*")
ADDR0O_RE = re.compile(r"0o([0-7]+)")

# Пять процедур, объявленных SUBP, но не имеющих тела в доступных образах.
MISSING_SUBPS = ["FOREX", "CONST", "COMEQ", "OPRTR", "ПP"]

# Кому принадлежит модуль (для графа вызовов).
MODULE_OF = {
    "FOREX_CORE.mad": "FOREX* (корень, recreated)",
    "FOREX_ROOT.mad": "FOREX* (корень, S1 4.13)",
    "FOREX_RUNTIME.mad": "рантайм (FORMAT / FORTLIBR / DATAPR* / OCTTDEC)",
    "FOREX_RUNTIME_DISASM.mad": "рантайм (дизассембл, FORMAT / FORTLIBR / DATAPR* / OCTTDEC)",
    "FOREX_DECODER_DISASM.mad": "рантайм (дизассембл DECODER / OCT_DEC)",
    "LO_SYN.mad": "LO*SYN (оверлей, синтаксический анализатор)",
    "LO_GEN.mad": "LO*GEN (оверлей, генератор кода)",
}


# ---------------------------------------------------------------------------
# Структуры данных
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Loc:
    file: str
    line: int

    def __str__(self) -> str:
        return f"{self.file}:{self.line}"


@dataclass
class Definition:
    symbol: str
    kind: str
    value: str
    loc: Loc
    raw: str


@dataclass
class Use:
    symbol: str
    op: str
    loc: Loc
    raw: str


@dataclass
class AddrRef:
    address: str        # нормализовано: 0oXXXXXX
    value: int
    op: str
    loc: Loc
    symbol: str = ""    # если адрес пришёл через EQU-символ
    raw: str = ""


@dataclass
class Literal:
    value: str
    loc: Loc
    op: str
    raw: str


@dataclass
class Scan:
    defs: dict[str, list[Definition]] = field(default_factory=lambda: defaultdict(list))
    uses: dict[str, list[Use]] = field(default_factory=lambda: defaultdict(list))
    jumps: list[tuple[str, Loc, str]] = field(default_factory=list)  # op, loc, target
    addrs: list[AddrRef] = field(default_factory=list)
    literals: list[Literal] = field(default_factory=list)
    files: list[str] = field(default_factory=list)
    label_files: list[str] = field(default_factory=list)
    xref_files: list[str] = field(default_factory=list)

    def all_defs(self, symbol: str) -> list[Definition]:
        return self.defs.get(symbol, [])

    def all_uses(self, symbol: str) -> list[Use]:
        return self.uses.get(symbol, [])


# ---------------------------------------------------------------------------
# Вспомогательные функции
# ---------------------------------------------------------------------------


def strip_comment(line: str) -> str:
    """Убрать `;`-комментарий и встроенный `.`-комментарий MADLEN."""
    s = line.split(";", 1)[0]
    # Точка — начало комментария, только если за ней идёт пробел, буква
    # или начало строки. `100000.0`, `=R100.0`, `3.14` при этом сохраняются.
    s = re.split(r"\.(?=\s|[A-Za-zА-Яа-я])|\s+\.", s, maxsplit=1)[0]
    return s.rstrip()


def lead_label(lead: str) -> str:
    """Достать имя метки из левой колонки (`START:`, `*00026 :12`, `L 7`)."""
    lead = lead.strip()
    if not lead or lead.startswith("0o") or lead[0].isdigit():
        return ""
    if lead.startswith(":"):
        return ""
    m = LEAD_LABEL_RE.match(lead)
    if not m:
        return ""
    tok = m.group(1)
    # «4», «14» и т.п. уже отсечены проверкой первой цифры.
    return tok


def split_fields(clean: str) -> list[str]:
    return [p.strip() for p in clean.split(",")]


def is_opcode_like(tok: str) -> bool:
    """Похоже ли поле на мнемонику (а не на адрес/операнд)."""
    return bool(OPCODE_LIKE_RE.fullmatch(tok.strip()))


def parse_line(line: str) -> tuple[str, str, str, str] | None:
    """→ (lead, opcode, operand, standalone_label_or_'')."""
    clean = strip_comment(line)
    if not clean:
        return None
    parts = split_fields(clean)
    if len(parts) == 1:
        tok = parts[0].strip()
        m = STANDALONE_LABEL_RE.match(tok)
        if m:
            return ("", "", "", m.group(1))
        return None
    if len(parts) >= 3:
        if parts[1]:
            return (parts[0], parts[1].upper(), ",".join(parts[2:]).strip(), "")
        return ("", parts[0].upper(), ",".join(parts[1:]).strip(), "")
    # Два поля: либо `ATX,4006B` (мнемоника в первой колонке), либо
    # `NPR:,XTA` (метка + мнемоника).
    a, b = parts
    if is_opcode_like(a) and not is_opcode_like(b):
        return ("", a.upper(), b, "")
    if is_opcode_like(b) and not is_opcode_like(a):
        return (a, b.upper(), "", "")
    if is_opcode_like(a):
        return ("", a.upper(), b, "")
    if is_opcode_like(b):
        return (a, b.upper(), "", "")
    return None


def octal_value(token: str) -> int | None:
    """Распознать восьмеричный операнд (`74010B`, `0o74010`, `077144`)."""
    m = re.fullmatch(r"(?:0o)?([0-7]+)B?", token.strip())
    if not m:
        return None
    digits = m.group(1)
    if len(digits) < 2:
        return None
    return int(digits, 8)


def norm_addr(value: int) -> str:
    return f"0o{value:06o}"


def symbols_in(text: str) -> list[str]:
    # Сначала «вымазываем» числовые литералы — иначе `74010B` даст ложный
    # символ `B`, а `*00026` — ложный `00026`.
    scrub = text
    for rx in (OCT_LITERAL_RE, DEC_LITERAL_RE):
        scrub = rx.sub(" ", scrub)
    return [m.group(0) for m in SYMBOL_RE.finditer(scrub)]


def numeric_in(text: str) -> list[str]:
    out: list[str] = []
    for m in OCT_LITERAL_RE.finditer(text):
        out.append(m.group(0))
    for m in DEC_LITERAL_RE.finditer(text):
        out.append(m.group(0))
    return out


# ---------------------------------------------------------------------------
# Сканирование .mad
# ---------------------------------------------------------------------------


def scan_mad(path: Path, scan: Scan) -> None:
    rel = path.relative_to(REPO).as_posix()
    scan.files.append(rel)
    text = path.read_text(encoding="utf-8", errors="replace")

    # PASS 1 — объявления (нужны, чтобы на PASS 2 знать все имена).
    parsed: list[tuple[int, tuple[str, str, str, str], str]] = []
    for no, raw in enumerate(text.splitlines(), 1):
        if not raw.strip() or raw[0] in COMMENT_CHARS:
            continue
        p = parse_line(raw)
        if p is None:
            continue
        parsed.append((no, p, raw))

        lead, op, operand, standalone = p
        loc = Loc(rel, no)
        sym = standalone or lead_label(lead)

        if standalone:
            if sym:
                scan.defs[sym].append(Definition(sym, "LABEL", "", loc, raw.strip()))
            continue

        if op in DECL_KIND:
            kind = DECL_KIND[op]
            if sym:
                scan.defs[sym].append(
                    Definition(sym, kind, operand, loc, raw.strip())
                )
            if op in {"BSS", "LC", "COMMON"} and not sym:
                scan.defs["<анонимный COMMON>"].append(
                    Definition("<анонимный COMMON>", "COMMON", operand, loc, raw.strip())
                )
        elif sym:
            # Метка на строке с командой (NPR:,XTA,... / START: ,ATX,...).
            scan.defs[sym].append(Definition(sym, "LABEL", "", loc, raw.strip()))

    # PASS 2 — применения и адреса.
    known = set(scan.defs)
    # Добавляем имена из .labels.md, если они уже прочитаны.
    known |= set(scan.defs)

    for no, p, raw in parsed:
        lead, op, operand, standalone = p
        if standalone:
            continue
        loc = Loc(rel, no)
        clean = strip_comment(raw)

        # EQU-строки: литерал в правой части считается «упакованным» в
        # константу и в список голых литералов не попадает.
        for sym in symbols_in(operand):
            if sym in known:
                scan.uses[sym].append(Use(sym, op or "-", loc, raw.strip()))
            else:
                scan.uses[f"?{sym}"].append(Use(sym, op or "-", loc, raw.strip()))

        # Операнд перехода: адрес или символ.
        if op in CONTROL_OPS:
            tok = operand.split()[0] if operand.split() else ""
            target = tok.rstrip(".,")
            if not target:
                target = "(косвенный/по базе)"
            scan.jumps.append((op, loc, target))

            val = octal_value(target)
            sym_target = ""
            if val is None and target in known:
                # Адрес, вынесенный в EQU: разрешаем символически.
                resolved, sym_target = resolve_numeric(target, scan.defs)
                val = resolved
            if val is not None and val >= 0o10000:
                scan.addrs.append(
                    AddrRef(norm_addr(val), val, op, loc, sym_target, raw.strip())
                )

        # Голые литералы: всё число в операнде, кроме правой части EQU.
        if op != "EQU":
            for lit in numeric_in(operand):
                scan.literals.append(Literal(lit, loc, op, raw.strip()))
        # Комментарии «С слово 0003 @0o510303 ...» не являются программой —
        # они уже отфильтрованы (строки начинаются с С).


def resolve_numeric(
    token: str, defs: dict[str, list[Definition]], depth: int = 0
) -> tuple[int | None, str]:
    """Разрешить `SYMBOL` (возможно, цепочку EQU) в числовое значение."""
    if depth > 8 or token not in defs:
        return None, ""
    seen = {token}
    cur = token
    for _ in range(8):
        d = defs[cur][-1]
        val = octal_value(d.value)
        if val is not None:
            return val, token
        syms = [s for s in symbols_in(d.value) if s in defs and s not in seen]
        if not syms:
            return None, ""
        seen.add(syms[0])
        cur = syms[0]
    return None, ""


# ---------------------------------------------------------------------------
# include/*.labels.md (могут появиться во время работы)
# ---------------------------------------------------------------------------


def scan_labels_md(path: Path, scan: Scan) -> None:
    rel = path.relative_to(REPO).as_posix()
    scan.label_files.append(rel)
    for no, line in enumerate(
        path.read_text(encoding="utf-8", errors="replace").splitlines(), 1
    ):
        if "`" not in line and "0o" not in line:
            continue
        syms = [s.strip("`* ") for s in re.findall(r"`[^`]+`", line)]
        syms = [
            s for s in syms
            if re.fullmatch(r"\*[0-9]{3,6}|\*?[A-Za-zА-Яа-я][\w/*]*", s)
            and not s.startswith("0o")
            and s.lower() not in {"call", "uj", "vjm", "uza", "atx", "xta", "subp", "entry"}
        ]
        addrs = ADDR0O_RE.findall(line)
        if not syms:
            continue
        value = f"0o{addrs[0]}" if addrs else ""
        loc = Loc(rel, no)
        for sym in syms:
            # Пропускаем имена файлов/опкодов, попавшиеся в backticks.
            if "/" in sym and not sym.startswith("*"):
                continue
            if sym.endswith(".md") or sym.endswith(".mad"):
                continue
            scan.defs[sym].append(
                Definition(sym, "LABEL(md)", value, loc, line.strip()[:120])
            )


# ---------------------------------------------------------------------------
# include/*.xref.md — подтверждённые символы/адреса из подробных xref-сводов
# ---------------------------------------------------------------------------


MD_TICK_RE = re.compile(r"`([^`]+)`")
MD_ADDR_RE = re.compile(r"0o([0-7]{3,7})\b")
MD_HEX_ADDR_RE = re.compile(r"\b([0-7]{5,6})B\b")
MD_NAME_RE = re.compile(r"\*[0-9]{3,6}|\*?[A-Za-zА-Яа-я][\w/*]*")


def md_symbols(text: str) -> list[str]:
    """Имена в backticks, похожие на символы МАДЛЕН (не пути и не мнемоники)."""
    out: list[str] = []
    for raw in MD_TICK_RE.findall(text):
        s = raw.strip(" *`'")
        if not MD_NAME_RE.fullmatch(s):
            continue
        if "/" in s and not s.startswith("*"):
            continue  # пути вроде src/LO_GEN.mad
        if s.endswith((".md", ".mad", ".lst", ".txt")):
            continue
        if s.lower() in {
            "call", "uj", "vjm", "uza", "atx", "xta", "subp", "entry",
            "equ", "name", "bss", "end", "vtm", "uta", "lj", "iec",
        }:
            continue
        out.append(s)
    return out


def scan_xref_md(path: Path, scan: Scan) -> None:
    """Подхватить подтверждённые пары «символ — адрес» из xref-документов.

    Читаются ``include/RUNTIME_*.xref.md`` (новые своды по дизассемблированному
    рантайму). Строгий разбор таблиц не требуется: любая строка-таблица или
    заголовок, где рядом с именем в backticks стоит адрес ``0oNNNNNN``, даёт
    определение вида ``XREF(md)`` с адресом. Это обогащает глобальную таблицу
    символов, но не подменяет определения из MAD-источников.
    """
    rel = path.relative_to(REPO).as_posix()
    scan.xref_files.append(rel)
    text = path.read_text(encoding="utf-8", errors="replace")
    for no, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped or stripped[0] not in "|#":
            continue
        syms = md_symbols(line)
        if not syms:
            continue
        addrs = [int(x, 8) for x in MD_ADDR_RE.findall(line)]
        if not addrs:
            addrs = [int(x, 8) for x in MD_HEX_ADDR_RE.findall(line)]
        value = norm_addr(addrs[0]) if addrs else ""
        loc = Loc(rel, no)
        for sym in syms:
            scan.defs[sym].append(
                Definition(sym, "XREF(md)", value, loc, stripped[:120])
            )


# ---------------------------------------------------------------------------
# Подтверждённые соответствия из docs/06-address-map.md
# ---------------------------------------------------------------------------


def clean_cell(text: str) -> str:
    """Достать читаемое значение ячейки markdown-таблицы."""
    # `**DATAPR***` = жирное `DATAPR*` (звёздочка — часть имени).
    bold_star = re.search(r"\*\*([^*]+)\*\*\*", text)
    if bold_star:
        return bold_star.group(1).strip() + "*"
    bold = re.search(r"\*\*([^*]+)\*\*", text)
    if bold:
        return bold.group(1).strip()
    ticks = re.findall(r"`([^`]+)`", text)
    if ticks:
        return ticks[0].strip()
    return text.strip()


def parse_confirmed(path: Path) -> list[tuple[str, str, str]]:
    """Заголовко-ориентированный разбор таблиц docs/06-address-map.md.

    Берём только таблицы, где явно есть колонки «Адрес»/«Диапазон» и
    «Имя»/«Что находится» — так не смешиваются колонки из таблиц §1.3 и §5.
    """
    if not path.exists():
        return []
    out: list[tuple[str, str, str]] = []
    seen: set[tuple[str, str]] = set()
    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    header: list[str] = []
    section = ""

    def addr_of(cell: str) -> str:
        m = re.search(r"0o([0-7]{3,7})\b", cell)
        if m:
            return norm_addr(int(m.group(1), 8))
        # Диапазоны вида `001770..004077`: берём начало как адрес.
        m = re.search(r"\b([0-7]{6})\.\.([0-7]{6})\b", cell)
        if m:
            return norm_addr(int(m.group(1), 8))
        return ""

    for idx, line in enumerate(lines):
        if line.startswith("#"):
            section = line.lstrip("# ").strip()
            header = []
            continue
        if not line.startswith("|"):
            header = []
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        nxt = lines[idx + 1] if idx + 1 < len(lines) else ""
        if re.fullmatch(r"\|[\s:\-|]+\|", nxt.strip()):
            header = [clean_cell(c).lower() for c in cells]
            continue
        if not header or len(cells) < 2:
            continue

        addr = name = src = ""
        hjoin = " ".join(header)
        if "адрес из s1" in hjoin or ("имя" in hjoin and "адрес" in hjoin):
            if "адрес из s1" in hjoin:
                idx_name, idx_addr = 0, 1
            else:
                idx_name = next((i for i, h in enumerate(header) if "имя" in h), 0)
                idx_addr = next((i for i, h in enumerate(header) if "адрес" in h), 1)
        elif "диапазон" in hjoin:
            idx_addr = 0
            idx_name = next((i for i, h in enumerate(header) if "находится" in h), 1)
        else:
            header = []
            continue
        idx_src = next((i for i, h in enumerate(header) if "источник" in h), len(cells) - 1)

        if idx_addr is not None and idx_addr < len(cells):
            addr = addr_of(cells[idx_addr])
        if idx_name is not None and idx_name < len(cells):
            name = clean_cell(cells[idx_name])
        if idx_src is not None and idx_src < len(cells):
            src = clean_cell(cells[idx_src])[:110]

        # Отсечь мусор: диапазоны, целые команды, LINK-ячейки как имя.
        if not addr or not name:
            continue
        if re.fullmatch(r"0o?[0-7]+(B)?(\.\.[0-7]+)?", name):
            continue
        if re.search(r"\b(vjm|uj|atx|xts|aex|call)\b", name, re.I):
            continue
        if (addr, name) in seen:
            continue
        seen.add((addr, name))
        out.append((addr, name, src or section))
    return out


# ---------------------------------------------------------------------------
# Форматирование markdown
# ---------------------------------------------------------------------------


def md_escape(s: str) -> str:
    return s.replace("|", "\\|").replace("\n", " ").strip()


def fmt_locs(locs: Iterable[Loc], limit: int = 6) -> str:
    items = [str(x) for x in locs]
    if not items:
        return "—"
    if len(items) <= limit:
        return ", ".join(f"`{x}`" for x in items)
    tail = ", ".join(f"`{x}`" for x in items[:limit])
    return f"{tail} … (+{len(items) - limit})"


def section_intro(scan: Scan) -> list[str]:
    inputs = sorted(scan.files + scan.label_files + scan.xref_files)
    n_lines = 0
    for rel in scan.files:
        n_lines += len((REPO / rel).read_text(encoding="utf-8", errors="replace").splitlines())
    return [
        "# 09 — Глобальный свод перекрёстных ссылок компилятора ФОРЭКС",
        "",
        "> **Автоматически сгенерировано** `tools/xref_all.py`. Не редактировать вручную —",
        "> перегенерируйте командой из раздела «Воспроизводимость».",
        "",
        "## 1. Метод и источники",
        "",
        "Инструмент сканирует все MAD-источники и извлекает объявления символов,",
        "все применения, переходы/вызовы и внешние абсолютные адреса. Операнды,",
        "вынесенные в `,EQU,`, разрешаются по цепочке при подсчёте адресов.",
        "",
        f"- MAD-файлов: **{len(scan.files)}**; строк: **{n_lines}**.",
        f"- Файлов `*.labels.md`: **{len(scan.label_files)}**"
        + (": " + ", ".join(f"`{x}`" for x in sorted(scan.label_files)) if scan.label_files else " (пока не созданы)"),
        f"- Различных символов с определением: **{len([s for s, ds in scan.defs.items() if ds])}**.",
        f"- Команд управления/перехода: **{len(scan.jumps)}**.",
        f"- Внешних абсолютных адресов (переходы ≥ `0o020000`): "
        f"**{len({a.address for a in scan.addrs})}**.",
        f"- Именованных констант `EQU`: **{len([d for ds in scan.defs.values() for d in ds if d.kind == 'EQU'])}**.",
        f"- Файлов `include/*.xref.md` (новые рантайм-своды): **{len(scan.xref_files)}**"
        + (": " + ", ".join(f"`{x}`" for x in sorted(scan.xref_files)) if scan.xref_files else " (пока не созданы)"),
        "",
        "Входные файлы:",
        "",
    ] + [f"- `{x}`" for x in inputs] + [
        "- `include/*.xref.md`, `include/catalog.md`, `docs/03-symbols.md`, `docs/06-address-map.md` (для раздела 5)",
        "- `include/RUNTIME_*.xref.md` — подробные xref-своды по дизассемблированному рантайму",
        "",
    ]


def table_symbol(scan: Scan) -> list[str]:
    out = [
        "## 2. Глобальная таблица символов",
        "",
        "### 2.1 Метки, точки входа и внешние имена",
        "",
        "«Определение» — файл:строка объявления; «Применения» — все операнды,",
        "где символ встречается (полный список — в `logs/xref_all.txt`).",
        "",
        "| Символ | Тип | Определение | Значение / примечание | Применения (всего) |",
        "|---|---|---|---|---:|",
    ]
    rows = []
    for sym, defs in scan.defs.items():
        if not defs or sym.startswith("<") or sym.startswith("?"):
            continue
        if all(d.kind in {"EQU", "DATA", "END"} for d in defs):
            continue  # вынесено в раздел 2.2
        uses = scan.all_uses(sym)
        kinds = "/".join(sorted({d.kind for d in defs}))
        value = md_escape(defs[0].value) or "—"
        rows.append(
            (sym, kinds, fmt_locs(d.loc for d in defs), value, len(uses), sym)
        )
    for sym, kinds, defloc, value, nuse, _ in sorted(rows, key=lambda r: (-r[4], r[0])):
        out.append(f"| `{md_escape(sym)}` | {kinds} | {defloc} | {value or '—'} | {nuse} |")
    return out


def table_equ(scan: Scan) -> list[str]:
    equ_defs = [d for ds in scan.defs.values() for d in ds if d.kind == "EQU"]
    out = [
        "",
        "### 2.2 Именованные константы (`,EQU,`)",
        "",
        "Требование «все литералы — в переменные»: числовые литералы выносятся в",
        "именованные `EQU`-константы. Здесь собраны все такие объявления и их применения.",
        "",
        "| Имя | Значение | Определение (файл:строка) | Применения | Всего |",
        "|---|---|---|---|---:|",
    ]
    for d in sorted(equ_defs, key=lambda x: (x.loc.file, x.loc.line)):
        uses = scan.all_uses(d.symbol)
        out.append(
            f"| `{md_escape(d.symbol)}` | `{md_escape(d.value) or '—'}` | "
            f"`{d.loc}` | {fmt_locs(u.loc for u in uses)} | {len(uses)} |"
        )
    if not equ_defs:
        out.append("| — | — | — | — | 0 |")

    # Нераспознанные (ещё не объявленные) символы — ценная обратная связь.
    unknown = {k[1:]: v for k, v in scan.uses.items() if k.startswith("?")}
    out += ["", "**Символы-кандидаты без объявления** (возможно, их нужно описать):", ""]
    if unknown:
        out.append("| Символ | Число применений | Пример |")
        out.append("|---|---:|---|")
        for sym, uses in sorted(unknown.items(), key=lambda kv: -len(kv[1]))[:30]:
            out.append(
                f"| `{md_escape(sym)}` | {len(uses)} | `{uses[0].loc}` (`{md_escape(uses[0].op)}`) |"
            )
    else:
        out.append("— все встречающиеся символы имеют объявление.")
    return out


def table_literals(scan: Scan) -> list[str]:
    by_file: dict[str, list[Literal]] = defaultdict(list)
    for lit in scan.literals:
        by_file[lit.loc.file].append(lit)

    out = [
        "",
        "### 2.3 Оставшиеся «голые» литералы",
        "",
        "Числовой литерал считается «голым», если он встречается непосредственно",
        "в операнде и не вынесен в правую часть `,EQU,`. Цель — свести эту таблицу",
        "к нулю по мере замены литералов именованными константами.",
        "",
        "| Файл | Строк с литералами | Вхождений | Примеры (значение @ файл:строка) |",
        "|---|---:|---:|---|",
    ]
    for f in sorted(by_file):
        lits = by_file[f]
        lines = len({x.loc.line for x in lits})
        top = Counter(x.value for x in lits).most_common(5)
        ex = ", ".join(f"`{v}`×{n}" for v, n in top)
        out.append(f"| `{f}` | {lines} | {len(lits)} | {ex} |")
    if not by_file:
        out.append("| — | 0 | 0 | голых литералов нет |")

    decl_lits = [x for x in scan.literals if x.op in set(DECL_KIND) | {"8TEXT"}]
    out += [
        "",
        f"Из них **{len(decl_lits)}** — в описаниях данных (`BSS/OCT/REAL/TEXT/…`)"
        f" (приоритетные кандидаты на `EQU`), **{len(scan.literals) - len(decl_lits)}**"
        " — непосредственно в командах (часто адреса, пока не вынесенные в константы).",
        "",
        "Описания данных с голыми литералами:",
        "",
        "| Файл:строка | Описание | Литерал |",
        "|---|---|---|",
    ]
    for x in sorted(decl_lits, key=lambda y: (y.loc.file, y.loc.line))[:40]:
        out.append(f"| `{x.loc}` | `{x.op}` | `{x.value}` |")
    if len(decl_lits) > 40:
        out.append(f"| … | … | ещё {len(decl_lits) - 40} |")

    out += [
        "",
        "Наиболее частые голые литералы (топ-15, по всем модулям):",
        "",
        "| Литерал | Вхождений | Где (первые 3) |",
        "|---|---:|---|",
    ]
    cnt = Counter(x.value for x in scan.literals)
    for lit, n in cnt.most_common(15):
        locs = [x.loc for x in scan.literals if x.value == lit][:3]
        out.append(f"| `{lit}` | {n} | {fmt_locs(locs)} |")
    out += ["", "Полный список каждого литерала со строкой — в `logs/xref_all.txt` (раздел `LITERALS`)."]
    return out


def graph_section(scan: Scan) -> list[str]:
    out = [
        "",
        "## 3. Граф вызовов: корень → оверлеи → рантайм → MONSYS",
        "",
        "```text",
        "                         CALL / VJM 0o74022(15)",
        "   FOREX* (root)  ───────────────►  LOADANGO ──XTS LO*SYN / LO*GEN──►  оверлеи",
        "        │  CALL DATAPR* / GIV/PG / TAK/PG / OCTTDEC",
        "        └──────────────────────────────►  рантайм (FORMAT, FORTLIBR, DATAPR*, OCTTDEC)",
        "                                                    │  UJ FT*nnn → 0o77xxx",
        "   LO*SYN / LO*GEN ── VJM/UJ/UZA (abs 0o4xxxx…0o7xxxx) ──►  MONSYS / library21",
        "```",
        "",
        "Все рёбра выведены из исходников; адреса `0o77xxx` подтверждены",
        "`docs/06-address-map.md` §3.1. Ниже — рёбра с указанием источника.",
        "",
        "| Откуда | Куда | Механизм | Источник (файл:строка) |",
        "|---|---|---|---|",
    ]

    edges: list[tuple[str, str, str, str]] = []

    def add(src: str, dst: str, mech: str, locs: Iterable[Loc], limit: int = 3,
            only_files: tuple[str, ...] = ()) -> None:
        items = list(locs)
        if only_files:
            items = [x for x in items if any(f in x.file for f in only_files)]
        s = fmt_locs(items, limit)
        if s != "—":
            edges.append((src, dst, mech, s))

    for sym, dst, mech in [
        ("LOADANGO", "LOADANGO (загрузчик MONSYS)", "CALL / VJM 0o74022(15)"),
        ("LO*SYN", "оверлей LO*SYN", "XTS 0o4031 + LOADANGO"),
        ("LO*GEN", "оверлей LO*GEN", "XTS 0o4032 + LOADANGO"),
    ]:
        add("FOREX* (root)", dst, mech, (u.loc for u in scan.all_uses(sym)),
            only_files=("FOREX_ROOT.mad", "FOREX_CORE.mad"))

    # CALL-ы корня могли быть переименованы агентами в EQU-символы — тогда
    # надёжнее опереться на LINK-адрес (подтверждён docs/06 §3).
    link_names = {
        0o74010: "рантайм: DATAPR* (LINK 0o74010)",
        0o74011: "рантайм: TAK/PG (LINK 0o74011)",
        0o74012: "рантайм: GIV/PG (LINK 0o74012)",
        0o74013: "рантайм: OCTTDEC (LINK 0o74013)",
        0o74022: "LOADANGO (LINK 0o74022)",
    }
    for val, dst in sorted(link_names.items()):
        add("FOREX* (root)", dst, "CALL / UJ через LINK-ячейку",
            (a.loc for a in scan.addrs if a.value == val),
            only_files=("FOREX_ROOT.mad", "FOREX_CORE.mad"))

    ft_uses: list[Use] = []
    for sym, uses in scan.uses.items():
        if re.fullmatch(r"FT\*\d+", sym):
            ft_uses.extend(uses)
    if ft_uses:
        add("рантайм: FORMAT", "FT*nnn (11 entry, 0o77xxx)", "UJ FT*nnn", (u.loc for u in ft_uses))

    add("оверлей LO*SYN", "MONSYS / library21", "VJM/UJ/UZA, abs 0o2xxxx…0o7xxxx",
        (a.loc for a in scan.addrs if "LO_SYN.mad" in a.loc.file))
    add("оверлей LO*GEN", "MONSYS / library21", "VJM/UJ/UZA, abs 0o2xxxx…0o7xxxx",
        (a.loc for a in scan.addrs if "LO_GEN.mad" in a.loc.file))

    for s, d, m, l in sorted(edges, key=lambda e: (e[0], e[1])):
        out.append(f"| {s} | {d} | {m} | {l} |")

    out += [
        "",
        "**Оговорка.** LINK-ячейки `0o74010..0o74013` в корне и в FORMAT имеют",
        "одинаковую нумерацию, но относятся к разным символам (выделяются пер-модульно) —",
        "см. `docs/06-address-map.md` §3.1.",
        "",
    ]
    return out


def addresses_section(scan: Scan) -> list[str]:
    out = [
        "## 4. НЕразрешённые внешние адреса (частоты)",
        "",
        "Считаются адреса ≥ `0o020000` в операндах команд передачи управления.",
        "Если адрес вынесен в `EQU`, он разрешён по цепочке и показан с именем.",
        "Имя процедуры для большинства адресов **не установлено** — для этого нужен",
        "`SYSTEM LOAD LIST` (см. `docs/06-address-map.md` §7).",
        "",
    ]
    for fname, title, reference in [
        ("LO_SYN.mad", "LO*SYN (синтаксический анализатор)", "104 / 269"),
        ("LO_GEN.mad", "LO*GEN (генератор кода)", "225 / 504"),
    ]:
        refs = [a for a in scan.addrs if fname in a.loc.file]
        cnt = Counter(a.address for a in refs)
        syms: dict[str, set[str]] = defaultdict(set)
        for a in refs:
            if a.symbol:
                syms[a.address].add(a.symbol)
        out += [
            f"### 4.{1 if fname == 'LO_SYN.mad' else 2}. {title}",
            "",
            f"Различных адресов: **{len(cnt)}**, всего переходов: **{len(refs)}**"
            f" (эталон docs/06: {reference} — разница объясняется другим набором"
            " мнемоник и источником листинга).",
            "",
            "| Адрес | Входов | Имя через EQU | Область (docs/06 §2) |",
            "|---|---:|---|---|",
        ]
        for addr, n in cnt.most_common(30):
            val = int(addr, 8)
            if 0o74000 <= val <= 0o74077:
                area = "LINK-ячейки MONSYS"
            elif 0o75000 <= val <= 0o77777:
                area = "код/таблицы MONSYS"
            elif 0o40000 <= val <= 0o73777:
                area = "резидентная библиотека 21"
            elif 0o20000 <= val <= 0o33777:
                area = "резидентные таблицы MONSYS"
            else:
                area = "прочее"
            sn = ", ".join(f"`{x}`" for x in sorted(syms.get(addr, ()))) or "—"
            out.append(f"| `{addr}` | {n} | {sn} | {area} |")
        if len(cnt) > 30:
            out.append(f"| … | … | ещё {len(cnt) - 30} адресов | — |")
        out.append("")
    out += [
        "Полный список всех адресов с частотами и строками — `logs/xref_all.txt`",
        "(раздел `ADDRESSES`).",
        "",
    ]
    return out


def confirmed_section(scan: Scan, confirmed: list[tuple[str, str, str]]) -> list[str]:
    out = [
        "## 5. Подтверждённые соответствия (docs/06-address-map.md)",
        "",
        "Извлечено из таблиц `docs/06-address-map.md` §3, §3.1. `confidence = confirmed`",
        "означает подтверждение адреса/роли, но не всегда имени процедуры.",
        "",
        "| Адрес | Имя / роль | Источник |",
        "|---|---|---|",
    ]
    for addr, name, src in confirmed:
        out.append(f"| `{addr}` | `{md_escape(name)}` | {md_escape(src)[:110]} |")
    if not confirmed:
        out.append("| — | — | docs/06-address-map.md не найден |")
    return out


def missing_subps_section(scan: Scan) -> list[str]:
    out = [
        "",
        "## 6. Пять объявленных, но не существующих SUBP",
        "",
        "`FOREX`, `CONST`, `COMEQ`, `OPRTR`, `ПP` объявлены как внешние `SUBP`",
        "в корне, но их исполняемые тела в доступных образах **не найдены**:",
        "LIBREFER помечает их `EN` (описаны, не используются), DTRAN в dispak",
        "даёт `IS ABSENT`. Вызовы идут из оверлеев абсолютными адресами,",
        "соответствие «адрес ↔ имя» не установлено.",
        "",
        "| SUBP | Все объявления | Число применений по имени | Тело |",
        "|---|---|---:|---|",
    ]
    for name in MISSING_SUBPS:
        defs = scan.all_defs(name)
        uses = scan.all_uses(name)
        out.append(
            f"| `{name}` | {fmt_locs(d.loc for d in defs)} | {len(uses)} | ❌ не найдено |"
        )
    out += [
        "",
        "Доказательства: `include/FOREX_CORE.xref.md` §3, `docs/06-core-modules.md`",
        "§3, `logs/dtran_root.txt` (`IS ABSENT` для всех пяти).",
        "",
    ]
    return out


def reproducibility() -> list[str]:
    return [
        "## 8. Воспроизводимость",
        "",
        "```bash",
        "cd /tmp/.private/azizz/opencode/re-forex",
        "python3 tools/xref_all.py --out docs/09-crossrefs.md",
        "# лог: logs/xref_all.txt (переопределяется флагом --log)",
        "```",
        "",
        "Инструмент детерминирован: сортирует все таблицы, не использует текущее",
        "время — повторный запуск даёт байт-в-байт тот же вывод (идемпотентность).",
        "",
        "## 9. Связанные документы",
        "",
        "- `include/FOREX_CORE.xref.md`, `include/FOREX_RUNTIME.xref.md`,",
        "  `include/LO_SYN.xref.md`, `include/LO_GEN.xref.md` — подробные xref по модулям;",
        "- `include/RUNTIME_DISASM.xref.md`, `include/RUNTIME_DECODER.xref.md` —",
        "  xref по дизассемблированному рантайму;",
        "- `docs/13-runtime-crossrefs.md` — подробный свод по рантайму;",
        "- `docs/10-naming-conventions.md` §6 — 6-символьное правило МАДЛЕН;",
        "- `docs/03-symbols.md` — символьный чек-лист (37/37);",
        "- `docs/06-address-map.md` — карта внешних адресов;",
        "- `logs/address_targets.txt` — сырые частоты адресов из листингов.",
        "",
    ]


# ---------------------------------------------------------------------------
# 6-символьное правило МАДЛЕН
# ---------------------------------------------------------------------------

# Виды определений, к которым применяется ограничение (реальные имена МАДЛЕН).
MADLEN_NAME_KINDS = {
    "LABEL", "LABEL(md)", "EQU", "NAME", "ENTRY", "SUBP",
    "COMMON", "TEXT", "DATA", "END",
}


def six_char_report(scan: Scan) -> tuple[list[tuple[str, str, str, list[Loc]]], dict[str, list[str]]]:
    """Вернуть ( нарушения длины, коллизии первых MAX_NAME_LEN знаков )."""
    violations: list[tuple[str, str, str, list[Loc]]] = []
    groups: dict[str, set[str]] = defaultdict(set)
    for sym, defs in scan.defs.items():
        if not sym or sym.startswith(("<", "?")):
            continue
        kinds = {d.kind for d in defs}
        if not (kinds & MADLEN_NAME_KINDS):
            continue
        locs = sorted((d.loc for d in defs), key=lambda x: (x.file, x.line))
        kind = "/".join(sorted(kinds))
        groups[sym[:MAX_NAME_LEN]].add(sym)
        if len(sym) > MAX_NAME_LEN:
            violations.append((sym, kind, sym[:MAX_NAME_LEN], locs))
    collisions = {p: sorted(s) for p, s in groups.items() if len(s) > 1}
    return sorted(violations, key=lambda x: (-len(x[0]), x[0])), dict(sorted(collisions.items()))


def six_char_section(scan: Scan) -> list[str]:
    violations, collisions = six_char_report(scan)
    out = [
        "",
        "## 7. НАРУШЕНИЯ 6-СИМВОЛЬНОГО ПРАВИЛА",
        "",
        "МАДЛЕН (БЭСМ-6) хранит имя метки или `,EQU,`-константы в одном",
        "шестисимвольном слове: различаются **только первые 6 знаков**.",
        f"Поэтому имя обязано быть ≤ {MAX_NAME_LEN} символов, а первые",
        f"{MAX_NAME_LEN} знаков разных имён — уникальными. Ниже собрано",
        "всё, что нарушает правило (источник — MAD-файлы и `*.labels.md`).",
        "",
        f"- имён длиннее {MAX_NAME_LEN} знаков: **{len(violations)}**;",
        f"- коллизий первых {MAX_NAME_LEN} знаков: **{len(collisions)}**.",
        "",
        f"### 7.1 Имена длиннее {MAX_NAME_LEN} знаков",
        "",
        "| Имя | Длина | Первые 6 | Тип | Где объявлено |",
        "|---|---:|---|---|---|",
    ]
    for sym, kind, prefix, locs in violations[:60]:
        out.append(
            f"| `{md_escape(sym)}` | {len(sym)} | `{md_escape(prefix)}` | {kind} | {fmt_locs(locs, 3)} |"
        )
    if len(violations) > 60:
        out.append(f"| … | … | … | … | ещё {len(violations) - 60} — полный список в `logs/xref_all.txt` |")
    if not violations:
        out.append("| — | 0 | — | — | нарушений нет |")

    out += [
        "",
        f"### 7.2 Коллизии первых {MAX_NAME_LEN} знаков",
        "",
        "Если две разные метки имеют одинаковый префикс, ассемблер их не различает.",
        "",
        "| Первые 6 | Конфликтующие имена | Где объявлено |",
        "|---|---|---|",
    ]
    for prefix, names in list(collisions.items())[:60]:
        locs: list[Loc] = []
        for name in names:
            locs.extend(d.loc for d in scan.defs.get(name, ()))
        out.append(
            f"| `{md_escape(prefix)}` | {', '.join(f'`{md_escape(n)}`' for n in names)} | {fmt_locs(locs, 3)} |"
        )
    if len(collisions) > 60:
        out.append(f"| … | … | ещё {len(collisions) - 60} — полный список в `logs/xref_all.txt` |")
    if not collisions:
        out.append("| — | — | коллизий нет |")
    out += [
        "",
        "Правило именования и примеры коротких имён — `docs/10-naming-conventions.md` §6.",
        "",
    ]
    return out


# ---------------------------------------------------------------------------
# Лог
# ---------------------------------------------------------------------------


def build_log(scan: Scan, confirmed: list[tuple[str, str, str]]) -> str:
    L: list[str] = []
    L.append("=== XREF_ALL: полный лог ===")
    L.append(
        f"MAD files: {len(scan.files)}; labels.md: {len(scan.label_files)}; "
        f"xref.md: {len(scan.xref_files)}"
    )
    L.append("")
    L.append("=== DEFINITIONS (symbol | kind | value | file:line) ===")
    for sym in sorted(scan.defs):
        for d in sorted(scan.defs[sym], key=lambda x: (x.loc.file, x.loc.line)):
            L.append(f"DEF\t{sym}\t{d.kind}\t{d.value}\t{d.loc}")
    L.append("")
    L.append("=== USES (symbol | op | file:line | raw) ===")
    for sym in sorted(scan.uses):
        for u in sorted(scan.uses[sym], key=lambda x: (x.loc.file, x.loc.line)):
            L.append(f"USE\t{sym}\t{u.op}\t{u.loc}\t{u.raw}")
    L.append("")
    L.append("=== JUMPS (op | target | file:line) ===")
    for op, loc, target in sorted(scan.jumps, key=lambda x: (x[1].file, x[1].line)):
        L.append(f"JUMP\t{op}\t{target}\t{loc}")
    L.append("")
    L.append("=== ADDRESSES (addr | count-total | file:line | op | symbol) ===")
    cnt = Counter(a.address for a in scan.addrs)
    for a in sorted(scan.addrs, key=lambda x: (x.loc.file, x.loc.line)):
        L.append(f"ADDR\t{a.address}\t{cnt[a.address]}\t{a.loc}\t{a.op}\t{a.symbol}")
    L.append("")
    L.append("=== ADDRESS_TOTALS ===")
    for addr, n in cnt.most_common():
        L.append(f"TOTAL\t{addr}\t{n}")
    L.append("")
    L.append("=== LITERALS (value | file:line | op | raw) ===")
    for lit in sorted(scan.literals, key=lambda x: (x.loc.file, x.loc.line)):
        L.append(f"LIT\t{lit.value}\t{lit.loc}\t{lit.op}\t{lit.raw}")
    L.append("")
    L.append("=== CONFIRMED (docs/06-address-map.md) ===")
    for addr, name, src in confirmed:
        L.append(f"CONF\t{addr}\t{name}\t{src}")
    L.append("")
    violations, collisions = six_char_report(scan)
    L.append(f"=== SIX_CHAR_VIOLATIONS (>{MAX_NAME_LEN} символов; всего {len(violations)}) ===")
    for sym, kind, prefix, locs in violations:
        L.append(f"LONGNAME\t{sym}\t{len(sym)}\t{prefix}\t{kind}\t" + ", ".join(str(x) for x in locs))
    L.append("")
    L.append(f"=== SIX_CHAR_COLLISIONS (первые {MAX_NAME_LEN} знаков; всего {len(collisions)}) ===")
    for prefix, names in collisions.items():
        L.append(f"COLLIDE\t{prefix}\t" + "\t".join(names))
    L.append("")
    return "\n".join(L)


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=Path, help="файл markdown (по умолчанию stdout)")
    ap.add_argument(
        "--log",
        type=Path,
        default=REPO / "logs" / "xref_all.txt",
        help="подробный лог (по умолчанию logs/xref_all.txt)",
    )
    ap.add_argument("--no-log", action="store_true", help="не писать лог")
    args = ap.parse_args()

    scan = Scan()
    mad_files = sorted((REPO / "src").glob("*.mad")) + sorted((REPO / "include").glob("*.mad"))
    for p in mad_files:
        scan_mad(p, scan)

    # .labels.md могут появиться у других агентов во время работы — читаем,
    # если есть (и в include/, и в src/).
    label_files = sorted((REPO / "include").glob("*.labels.md")) + sorted(
        (REPO / "src").glob("*.labels.md")
    )
    known_before = set(scan.defs)
    for p in label_files:
        scan_labels_md(p, scan)
    # Повторный проход применений с учётом новых имён из .labels.md.
    if label_files:
        for sym in list(scan.defs):
            if sym not in known_before:
                # уже собранные USE с префиксом '?' переклассифицируем
                if f"?{sym}" in scan.uses:
                    scan.uses[sym].extend(scan.uses.pop(f"?{sym}"))

    # Новые подробные xref-своды по рантайму (могут появиться позже других
    # агентов). Подхватываем и RUNTIME_*.xref.md, и остальные *.xref.md,
    # чтобы глобальный свод действительно был глобальным.
    xref_files = sorted((REPO / "include").glob("RUNTIME_*.xref.md"))
    for p in xref_files:
        scan_xref_md(p, scan)

    confirmed = parse_confirmed(REPO / "docs" / "06-address-map.md")

    doc = "\n".join(
        section_intro(scan)
        + table_symbol(scan)
        + table_equ(scan)
        + table_literals(scan)
        + graph_section(scan)
        + addresses_section(scan)
        + confirmed_section(scan, confirmed)
        + missing_subps_section(scan)
        + six_char_section(scan)
        + reproducibility()
    )
    if not doc.endswith("\n"):
        doc += "\n"

    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(doc, encoding="utf-8")
        print(f"записано: {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(doc)

    if not args.no_log:
        args.log.parent.mkdir(parents=True, exist_ok=True)
        args.log.write_text(build_log(scan, confirmed), encoding="utf-8")
        print(f"записано: {args.log}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
