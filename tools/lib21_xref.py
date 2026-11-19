#!/usr/bin/env python3
"""Глобальный свод перекрёстных ссылок библиотеки 21 (DMS, Дубна).

Инструмент читает sym-секции всех объектных модулей образа ``lib21.bin``
(358 модулей), при необходимости сверяет их с дtran-листингами
``disasm/lib21/*.madlen`` и аннотированными текстами ``src/lib21/*.mad`` /
``include/lib21/*.xref.md``, и строит:

  * таблицу «символ → модули-объявители → модули-вызывающие»;
  * топ внешних символов по числу модулей;
  * граф зависимостей («предоставляет → использует») по entry-точкам
    модулей и COMMON/ENTRY-символам;
  * таблицу «модуль → entry → внешние ссылки»;
  * список модулей-одиночек;
  * проверку 6-символьного правила для аннотированных имён.

Выход: Markdown (``--out``) и/или JSON (``--json``). Лог — ``--log``.
Все таблицы детерминированно сортируются; текущее время не используется.

Пример:
    python3 tools/lib21_xref.py \
        --out docs/lib21/03-crossrefs.md \
        --json > /dev/null \
        --log logs/lib21_xref.txt
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LIB = Path("/home/azizz/Yandex.Disk/besm6-new/DUBNA/BUILD/elements/lib21.bin")
DEFAULT_DISASM = ROOT / "disasm" / "lib21"
DEFAULT_SRC = ROOT / "src" / "lib21"
DEFAULT_INCLUDE = ROOT / "include" / "lib21"
DEFAULT_MODULES_CSV = ROOT / "docs" / "lib21" / "modules.csv"
DEFAULT_OUT = ROOT / "docs" / "lib21" / "03-crossrefs.md"
DEFAULT_LOG = ROOT / "logs" / "lib21_xref.txt"

WORD_BYTES = 6
MODULE_ALIGN = 32

# Кодировка TEXT (8 x 6 бит), та же, что в tools/lib21_parse.py.
TEXT = [
    " ", ".", "Б", "Ц", "Д", "Ф", "Г", "И", "(", ")", "*", "Й",
    "Л", "Я", "Ж", "/", "0", "1", "2", "3", "4", "5", "6", "7",
    "8", "9", "Ь", ",", "П", "-", "+", "Ы", "З", "A", "B", "C",
    "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
    "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "Ш",
    "Э", "Щ", "Ч", "Ю",
]

# Типы записей DMS-симтаблицы (восьмеричные) → категория МАДЛЕН.
SYM_TYPES = {
    0o430: "SUBP", 0o630: "SUBP",                       # EXT_S / EXT_L
    0o414: "ENTRY", 0o614: "ENTRY",                     # ENTRY_S / ENTRY_L
    0o415: "LC", 0o615: "LC",                           # DENTRY_S / DENTRY_L
    0o470: "LC", 0o471: "LC", 0o670: "LC", 0o671: "LC",  # COMMON (dtran → LC)
    0o474: "LC", 0o674: "LC", 0o770: "LC",              # COMMON (др. варианты)
    0o400: "LC", 0o403: "LC", 0o520: "LC", 0o654: "LC",  # ABS / CONST
    0o460: "BSS", 0o660: "BSS", 0o464: "BSS", 0o664: "BSS",
    0o521: "EQU",                                        # EXPRESSION
    0o500: "LC",
}

# Локальные метки dtran (*0004B, 0016B, dunno и т.п.) — не внешние символы.
LOCAL_RE = re.compile(r"^\*[0-7]+B?$|^[0-7]+B$|^\d+$|^dunno$|^[+-]?\d+$")

DECL_RE = re.compile(
    r"^\s*(?P<name>[^\s:,]+)\s*:\s*,\s*"
    r"(?P<kind>NAME|SUBP|LC|BSS|ENTRY|COMMON|EQU|LOG|TEXT|OCT|REAL|GOST|PU)\s*,",
    re.IGNORECASE,
)
ANNOT_LABEL_RE = re.compile(r"^\s*(?P<name>[^\s:,;]+)\s*:")
ANNOT_DECL_RE = re.compile(r"^\s*(?P<name>[^\s:,]+)\s*,\s*(?P<kind>EQU|ENTRY|SUBP)\s*,", re.I)


def text_decode(word: int) -> str:
    """48-битное слово → 8 символов TEXT."""
    return "".join(TEXT[(word >> (42 - 6 * i)) & 0x3F] for i in range(8))


def field(word: int, lo: int, hi: int) -> int:
    return (word >> lo) & ((1 << (hi - lo)) - 1)


def norm_module(name: str) -> str:
    """Имя символа → имя файла/модуля (*→_, /→#), как в disasm/lib21."""
    return name.strip().replace("*", "_").replace("/", "#")


def is_local(name: str) -> bool:
    return not name or bool(LOCAL_RE.match(name.strip()))


# ---------------------------------------------------------------------------
class Lib21Slim:
    """Минимальный корректный разбор DMS-библиотеки (без внешних зависимостей)."""

    def __init__(self, path: Path):
        self.path = Path(path)
        data = self.path.read_bytes()
        if len(data) % WORD_BYTES:
            raise ValueError(f"размер {self.path} не кратен {WORD_BYTES}")
        self.nwords = len(data) // WORD_BYTES
        self.words = [
            int.from_bytes(data[i:i + WORD_BYTES], "big")
            for i in range(0, len(data), WORD_BYTES)
        ]
        self.catalog = self._read_catalog()
        self.objects = self._find_objects()

    def _read_catalog(self) -> list[str]:
        out = []
        i = 2
        while i + 1 < self.nwords:
            name = text_decode(self.words[i]).rstrip()
            if not name or not all(c.isalnum() or c in "/*" for c in name):
                break
            out.append(name)
            i += 2
        return out

    @staticmethod
    def _header(words: list[int], s: int) -> dict:
        w0, w1, w2 = words[s], words[s + 1], words[s + 2]
        return dict(
            head=field(w0, 0, 12), sym=field(w0, 12, 24), debug=field(w0, 36, 48),
            set=field(w1, 0, 15), data=field(w1, 15, 30), long=field(w1, 30, 45),
            cmd=field(w2, 0, 15), bss=field(w2, 15, 30), const=field(w2, 30, 45),
        )

    def _find_objects(self) -> dict[str, dict]:
        names = set(self.catalog)
        objs: dict[str, dict] = {}
        for s in range(0, self.nwords - 3, MODULE_ALIGN):
            h = self._header(self.words, s)
            if h["head"] != 1:
                continue
            toff = s + 3 + h["cmd"] + h["const"] + h["data"] + h["set"]
            if toff >= self.nwords:
                continue
            name = text_decode(self.words[toff]).rstrip()
            if name not in names or name in objs:
                continue
            table_off = toff
            objs[name] = dict(offset=s, header=h, table_off=table_off)
        return objs

    def sym_entries(self, name: str) -> list[dict]:
        """Разобрать sym-секцию модуля: name / kind / addr / value / raw_type."""
        obj = self.objects[name]
        h, base = obj["header"], obj["table_off"]
        s_sym = base + h["head"]
        out = []
        for i in range(h["sym"]):
            w = self.words[s_sym + i]
            typ = field(w, 15, 24)
            ref = field(w, 24, 48)
            addr = field(w, 0, 15)
            if typ & 0o200:  # длинное имя: индекс относительно table_off
                idx = ref & 0o3777
                p = base + idx
                nm = text_decode(self.words[p]).rstrip() if p < self.nwords else ""
            else:
                nm = text_decode(ref).strip()
            nm = nm.strip()
            kind = SYM_TYPES.get(typ & 0o777, "OTHER")
            out.append(dict(name=nm, kind=kind, addr=addr, value=addr,
                            raw_type=f"{typ:03o}", index=i))
        return out


# ---------------------------------------------------------------------------
def parse_madlen(path: Path) -> dict:
    """Разобрать dtran-листинг: объявления и символические операнды."""
    module = path.stem
    decls: dict[str, set[str]] = defaultdict(set)
    refs: Counter = Counter()
    lines = []
    with path.open(encoding="utf-8", errors="replace") as f:
        for line in f:
            lines.append(line)
    if lines:
        m = DECL_RE.match(lines[0])
        if m and m.group("kind").upper() == "NAME":
            module = m.group("name").strip()
    for line in lines:
        m = DECL_RE.match(line)
        if m:
            nm = m.group("name").strip()
            if not is_local(nm):
                decls[m.group("kind").upper()].add(nm)
            continue
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 3:
            continue
        for op in parts[2:]:
            op = op.strip()
            if op and not is_local(op) and re.match(r"^[^\s\d+=-]", op):
                refs[op] += 1
    return dict(module=module, decls=decls, refs=refs)


def parse_annotated(paths: list[Path]) -> tuple[dict[str, set[str]], dict[str, list[str]]]:
    """Собрать объявления и все аннотированные имена для проверки 6-символьного правила."""
    entries: dict[str, set[str]] = defaultdict(set)
    names: dict[str, list[str]] = defaultdict(list)
    for p in paths:
        if not p.exists():
            continue
        for ln, line in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            s = line.strip()
            if not s or s.startswith("C") or s.startswith("#") or s.startswith("|"):
                continue
            # Основная метка: NAME:, / LABEL:, перед двоеточием.
            m = ANNOT_LABEL_RE.match(line)
            if m:
                nm = m.group("name").strip()
                if nm and not nm.startswith(";") and not nm.startswith("*"):
                    names[nm].append(f"{p.name}:{ln}")
            for m in ANNOT_DECL_RE.finditer(line):
                nm = m.group("name").strip()
                names[nm].append(f"{p.name}:{ln}")
    return entries, names


def read_modules_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------------------
def build_model(lib: Lib21Slim, madlen: dict[str, dict], modules_csv: list[dict],
                annotated_names: dict[str, list[str]]) -> dict:
    module_names = sorted(lib.objects)
    csv_names = {row.get("name", "").strip() for row in modules_csv if row.get("name")}
    if csv_names and csv_names != set(module_names):
        # CSV — список модулей этапа 13; расхождения не меняют состав библиотеки.
        pass

    # Объявления из sym-секций (основной источник).
    declared: dict[str, dict[str, set[str]]] = {m: defaultdict(set) for m in module_names}
    for m in module_names:
        for e in lib.sym_entries(m):
            if not e["name"] or is_local(e["name"]):
                continue
            declared[m][e["kind"]].add(e["name"])

    # Дополняем аннотированными MAD-текстами (ENTRY, короткие имена).
    for mod, info in madlen.items():
        if mod not in declared:
            continue
        for kind, syms in info["decls"].items():
            if kind == "NAME":
                continue
            declared[mod][kind].update(syms)

    # ENTRY-символы модуля: имя модуля (NAME) + явные ,ENTRY, из аннотаций.
    entries: dict[str, set[str]] = {m: {m} for m in module_names}
    for m in module_names:
        entries[m].update(declared[m].get("ENTRY", ()))

    # Кто объявляет и кто вызывает каждый символ.
    declared_by: dict[str, set[str]] = defaultdict(set)
    defined_by: dict[str, set[str]] = defaultdict(set)
    called_by: dict[str, set[str]] = defaultdict(set)
    kinds: dict[str, set[str]] = defaultdict(set)
    subp_by: dict[str, set[str]] = defaultdict(set)

    for m in module_names:
        d = declared[m]
        for kind, syms in d.items():
            for s in syms:
                declared_by[s].add(m)
                kinds[s].add(kind)
                if kind in ("LC", "BSS", "ENTRY"):
                    defined_by[s].add(m)
                if kind == "SUBP":
                    subp_by[s].add(m)
                    called_by[s].add(m)
        for s in entries[m]:
            declared_by[s].add(m)
            kinds[s].add("ENTRY")
            defined_by[s].add(m)

    # Вызовы из кода: символические операнды dtran-листингов.
    all_known = set(declared_by) | set(defined_by)
    for mod, info in madlen.items():
        for s, cnt in info["refs"].items():
            if s in all_known:
                called_by[s].add(mod)

    # Внешние символы: SUBP-объявления либо определение в одном модуле,
    # используемое другим. Локальные EQU-псевдонимы dtran (GAK/n, GAL/n)
    # внешними не являются.
    external = set()
    for s in set(declared_by) | set(called_by):
        if len(s) < 2 or not any(ch.isalnum() for ch in s):
            continue
        if subp_by[s] or (defined_by[s] and (called_by[s] - defined_by[s])):
            external.add(s)

    # Граф зависимостей: модуль-поставщик → модуль-потребитель.
    entry_to_module: dict[str, str] = {}
    for m in module_names:
        for e in entries[m]:
            entry_to_module.setdefault(norm_module(e), m)
    edges: dict[tuple[str, str], Counter] = defaultdict(Counter)
    for s in external:
        consumers = set(called_by[s]) | set(subp_by[s])
        providers = set(defined_by[s])
        key = norm_module(s)
        if key in entry_to_module:
            providers.add(entry_to_module[key])
        for p in providers:
            for c in consumers:
                if p != c:
                    edges[(p, c)][s] += 1

    # Проверка 6-символьного правила.
    violations_long, violations_collision = [], []
    for nm, where in sorted(annotated_names.items()):
        if len(nm) > 6:
            violations_long.append((nm, len(nm), where[:3]))
    pref: dict[str, set[str]] = defaultdict(set)
    for nm in annotated_names:
        pref[nm[:6].upper()].add(nm)
    for p6, group in sorted(pref.items()):
        if len(group) > 1:
            violations_collision.append((p6, sorted(group)))

    return dict(
        module_names=module_names,
        declared=declared,
        entries=entries,
        declared_by=declared_by,
        defined_by=defined_by,
        called_by=called_by,
        subp_by=subp_by,
        kinds=kinds,
        external=external,
        edges=edges,
        madlen=madlen,
        modules_csv=modules_csv,
        violations_long=violations_long,
        violations_collision=violations_collision,
        annotated_names=annotated_names,
    )


# ---------------------------------------------------------------------------
def _short(names: set[str] | list[str], n: int = 8) -> str:
    xs = sorted(names)
    if len(xs) <= n:
        return ", ".join(f"`{x}`" for x in xs) if xs else "—"
    return ", ".join(f"`{x}`" for x in xs[:n]) + f" … (+{len(xs) - n})"


def cluster_of(module: str) -> str:
    u = module.upper()
    if u in {"FOREX_", "FORMAT", "FORTLIBR", "FOREX", "FOREX*"}:
        return "FOREX*/FORMAT/FORTLIBR"
    if "DECOD" in u or "LINK" in u or "IPM" in u:
        return "DECODER/LINK/IPM"
    if "PRINT" in u or "PUNCH" in u or "PUNT" in u or "PRIN" in u or "BUFFER" in u:
        return "печать"
    if "TAP" in u or "TAPE" in u or "MT_" in u or "LENT" in u or "DUMP" in u:
        return "лента"
    return "прочее"


def render_markdown(m: dict, meta: dict) -> str:
    L: list[str] = []
    add = L.append
    module_names = m["module_names"]
    declared_by, defined_by, called_by = m["declared_by"], m["defined_by"], m["called_by"]
    subp_by, kinds = m["subp_by"], m["kinds"]
    external = m["external"]

    add("# 03 — Глобальный свод перекрёстных ссылок библиотеки 21")
    add("")
    add("> **Автоматически сгенерировано** `tools/lib21_xref.py`. Не редактировать вручную —")
    add("> перегенерируйте командой из раздела «Воспроизводимость».")
    add("")
    add("## 1. Метод и источники")
    add("")
    add("Sym-секции всех объектных модулей образа `lib21.bin` разбираются напрямую:")
    add("каталог → DMS-заголовок → раздел `sym` (типы `EXT/ENTRY/DENTRY/COMMON/PRIVATE/ABS`)")
    add("→ категории МАДЛЕН `SUBP` / `LC` / `BSS` / `ENTRY`. Символические операнды")
    add("кода берутся из dtran-листингов `disasm/lib21/*.madlen`; имена и явные `,ENTRY,`")
    add("— из аннотированных текстов `src/lib21/*.mad` и `include/lib21/*.xref.md`.")
    add("")
    add("| Показатель | Значение |")
    add("|---|---:|")
    add(f"| Модулей в sym-секциях | **{len(module_names)}** |")
    add(f"| Записей каталога | {meta['catalog_entries']} |")
    add(f"| Листингов dtran | {len(m['madlen'])} |")
    add(f"| Различных символов в sym-секциях | {len(declared_by)} |")
    add(f"| Внешних символов (SUBP / definition+use) | **{len(external)}** |")
    add(f"| Символов-type SUBP | {len(subp_by)} |")
    add(f"| Рёбер графа «поставщик → потребитель» | {sum(len(c) for c in m['edges'].values())} |")
    add(f"| Аннотированных имён (для проверки 6-символьного правила) | {len(m['annotated_names'])} |")
    add("")
    add(f"Источник: `{meta['lib_path']}`; sha256 `{meta['sha256']}`.")
    add("")

    # 2. Топ внешних символов.
    add("## 2. Топ внешних символов по числу модулей")
    add("")
    add("«Объявляют» — модули, в чьей sym-секции есть запись символа; «вызывают» —")
    add("модули с объявлением `SUBP` или символической ссылкой в коде. Ниже — символы,")
    add("задействованные более чем в одном модуле.")
    add("")
    ranked = sorted(external, key=lambda s: (-(len(declared_by[s]) + len(called_by[s])), s))
    add("| Символ | Типы | Объявляют | Модули-объявители | Вызывают | Модули-вызывающие |")
    add("|---|---|---:|---|---:|---|")
    for s in ranked[:60]:
        add(f"| `{s}` | {', '.join(sorted(kinds[s]))} | {len(declared_by[s])} | "
            f"{_short(declared_by[s])} | {len(called_by[s])} | {_short(called_by[s])} |")
    if len(ranked) > 60:
        add("")
        add(f"Полный список — `{meta['json_note']}` (раздел `symbols`).")
    add("")

    # 3. Граф.
    add("## 3. Граф зависимостей")
    add("")
    add("Ребро «объявитель/поставщик → потребитель» проводится, когда символ,")
    add("объявленный (или являющийся entry) в модуле A, используется в модуле B.")
    add("Кластеры: `FOREX*/FORMAT/FORTLIBR` (ядро и рантайм), `DECODER/LINK/IPM`,")
    add("печать и лента. Ниже — рёбра между кластерами (по числу общих символов).")
    add("")
    cluster_edges: dict[tuple[str, str], Counter] = defaultdict(Counter)
    for (a, b), syms in m["edges"].items():
        ca, cb = cluster_of(a), cluster_of(b)
        if ca != cb:
            cluster_edges[(ca, cb)].update(syms)
    add("```mermaid")
    add("graph LR")
    clusters = ["FOREX*/FORMAT/FORTLIBR", "DECODER/LINK/IPM", "печать", "лента", "прочее"]
    for i, c in enumerate(clusters):
        add(f'  subgraph C{i}["{c}"]')
        add("  end")
    for (ca, cb), syms in sorted(
            cluster_edges.items(),
            key=lambda kv: (-sum(kv[1].values()), kv[0][0], kv[0][1]))[:40]:
        ci, cj = clusters.index(ca), clusters.index(cb)
        label = ", ".join(s for s, _ in sorted(
            syms.items(), key=lambda kv: (-kv[1], kv[0]))[:3])
        add(f'  C{ci} -->|"{label}"| C{cj}')
    add("```")
    add("")
    add("Ключевые рёбра «модуль → модуль» (не только между кластерами):")
    add("")
    add("| Поставщик | Потребитель | Символы |")
    add("|---|---|---|")
    edge_list = sorted(m["edges"].items(), key=lambda kv: (-sum(kv[1].values()), kv[0]))
    for (a, b), syms in edge_list[:50]:
        add(f"| `{a}` | `{b}` | {_short(set(syms))} |")
    if len(edge_list) > 50:
        add(f"| … | … | ещё {len(edge_list) - 50} рёбер |")
    add("")

    add("### 3.1 Ключевые символы кластеров")
    add("")
    add("Сводка по символам, связывающим ядро (`FOREX*`, `FORMAT`, `FORTLIBR`)")
    add("с decoder/link/IPM, печатью и лентой. «Объявители» — из sym-секции,")
    add("«вызывающие» — SUBP-объявления и символические ссылки в коде.")
    add("")
    key_symbols = [
        "FT*571", "FT*003", "PRINT8", "PRINT8//", "DATAPR*", "GIV/PG", "TAK/PG",
        "OCTTDEC", "LOADANGO", "MONITOR*", "MONREAD*", "READ*", "DRUMTAP*",
        "DECODER", "LINK/IPM", "PARAMT*", "ISO*TEX*", "BUFFER",
    ]
    add("| Символ | Кластеры-пользователи | Объявители | Вызывающие (пример) |")
    add("|---|---|---|---|")
    for s in key_symbols:
        if s not in declared_by and s not in called_by:
            continue
        clusters = sorted({cluster_of(x) for x in (called_by[s] | declared_by[s])})
        add(f"| `{s}` | {', '.join(clusters)} | {_short(declared_by[s], 4)} | "
            f"{_short(called_by[s], 4)} |")
    add("")

    # 4. Модуль → entry → внешние ссылки.
    add("## 4. Модуль → entry → внешние ссылки")
    add("")
    add("`entry` — имя модуля (символ `NAME`) плюс явные объявления `,ENTRY,`. ")
    add("Внешние ссылки — `SUBP`-объявления sym-секции.")
    add("")
    add("| Модуль | Entry | Внешние ссылки (SUBP) |")
    add("|---|---|---|")
    for mod in module_names:
        subs = set(subp_by_sym(mod, m))
        add(f"| `{mod}` | {_short(m['entries'][mod])} | {_short(subs)} |")
    add("")

    # 5. Модули-одиночки.
    add("## 5. Модули-одиночки")
    add("")
    add("Модули, у которых нет внешних (`SUBP`) ссылок и которые никто не вызывает")
    add("(их entry-символ не встречается среди внешних ссылок других модулей).")
    add("")
    called_modules = set()
    for s in external:
        called_modules.update(called_by[s])
        called_modules.update(defined_by[s])
    loners = [mod for mod in module_names
              if not subp_by_sym(mod, m) and mod not in called_modules]
    if loners:
        add("| Модуль | Entry | Строк в листинге |")
        add("|---|---|---:|")
        for mod in loners:
            lines = m["madlen"].get(mod, {}).get("lines", 0)
            add(f"| `{mod}` | {_short(m['entries'][mod])} | {lines} |")
    else:
        add("Одиночек не обнаружено.")
    add("")

    # 6. 6-символьное правило.
    add("## 6. Проверка 6-символьного правила")
    add("")
    add("МАДЛЕН хранит короткое имя в одном шестисимвольном слове: имя обязано быть")
    add("≤ 6 знаков, а первые 6 знаков разных имён должны различаться. Проверены")
    add("все аннотированные имена из `src/lib21/*.mad` и `include/lib21/*.xref.md`.")
    add("")
    add("| Категория | Нарушений |")
    add("|---|---:|")
    add(f"| имён длиннее 6 знаков | {len(m['violations_long'])} |")
    add(f"| коллизий первых 6 знаков | {len(m['violations_collision'])} |")
    add("")
    add("### 6.1 Имена длиннее 6 знаков")
    add("")
    if m["violations_long"]:
        add("| Имя | Длина | Где объявлено |")
        add("|---|---:|---|")
        for nm, ln, where in m["violations_long"]:
            add(f"| `{nm}` | {ln} | {_short(set(where))} |")
    else:
        add("Нарушений нет — все аннотированные имена укладываются в 6 знаков.")
    add("")
    add("### 6.2 Коллизии первых 6 знаков")
    add("")
    if m["violations_collision"]:
        add("| Первые 6 | Конфликтующие имена |")
        add("|---|---|")
        for p6, group in m["violations_collision"]:
            add(f"| `{p6}` | {_short(set(group))} |")
    else:
        add("Коллизий нет.")
    add("")

    # 7. Воспроизводимость.
    add("## 7. Воспроизводимость")
    add("")
    add("```bash")
    add("cd /tmp/.private/azizz/opencode/re-forex")
    add("python3 tools/lib21_xref.py --out docs/lib21/03-crossrefs.md \\")
    add("    --json --log logs/lib21_xref.txt")
    add("```")
    add("")
    add("Инструмент детерминирован: сортирует все таблицы и не использует текущее")
    add("время — повторный запуск даёт байт-в-байт тот же вывод.")
    add("")
    add("## 8. Связанные документы")
    add("")
    add("- `docs/lib21/01-structure.md`, `docs/lib21/02-disassembly.md` — структура и дизассембл;")
    add("- `disasm/lib21/*.madlen` — dtran-листинги всех 358 модулей;")
    add("- `src/lib21/*.mad`, `include/lib21/*.xref.md` — аннотированные тексты и xref;")
    add("- `docs/09-crossrefs.md` — глобальный свод по компилятору ФОРЭКС;")
    add("- `docs/06-address-map.md` — карта внешних адресов.")
    add("")
    return "\n".join(L)


def subp_by_sym(mod: str, m: dict) -> set[str]:
    return {s for s, mods in m["subp_by"].items() if mod in mods}


def render_json(m: dict, meta: dict) -> dict:
    def sym_rec(s: str) -> dict:
        return dict(
            symbol=s,
            kinds=sorted(m["kinds"][s]),
            declared_by=sorted(m["declared_by"][s]),
            defined_by=sorted(m["defined_by"][s]),
            called_by=sorted(m["called_by"][s]),
            subp_by=sorted(m["subp_by"][s]),
        )
    return dict(
        meta=meta,
        modules=[dict(name=n, entry=sorted(m["entries"][n]),
                      external_refs=sorted(subp_by_sym(n, m)))
                 for n in m["module_names"]],
        symbols=[sym_rec(s) for s in sorted(m["external"])],
        edges=[dict(provider=a, consumer=b, symbols=sorted(syms))
               for (a, b), syms in sorted(m["edges"].items())],
        six_char=dict(
            long=[dict(name=n, length=l, where=w) for n, l, w in m["violations_long"]],
            collisions=[dict(prefix=p, names=g) for p, g in m["violations_collision"]],
        ),
    )


# ---------------------------------------------------------------------------
def write_log(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--lib", type=Path, default=DEFAULT_LIB, help="образ lib21.bin")
    ap.add_argument("--disasm", type=Path, default=DEFAULT_DISASM, help="dtran-листинги")
    ap.add_argument("--src", type=Path, default=DEFAULT_SRC, help="аннотированные МАДЛЕН")
    ap.add_argument("--include", type=Path, default=DEFAULT_INCLUDE, help="аннотированные xref")
    ap.add_argument("--modules-csv", type=Path, default=DEFAULT_MODULES_CSV)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, help="Markdown-свод")
    ap.add_argument("--json", nargs="?", const="-", default=None,
                    help="JSON в файл (или в stdout, если путь не задан)")
    ap.add_argument("--log", type=Path, default=DEFAULT_LOG)
    args = ap.parse_args()

    log: list[str] = []
    def say(s: str = "") -> None:
        log.append(s)
        print(s, file=sys.stderr)  # stdout остаётся чистым для --json

    lib = Lib21Slim(args.lib)
    say(f"ЛИБИОТЕКА 21: {args.lib}")
    say(f"  слов: {lib.nwords}; каталог: {len(lib.catalog)}; объектов: {len(lib.objects)}")
    say(f"  sha256: {__import__('hashlib').sha256(args.lib.read_bytes()).hexdigest()}")

    madlen = {}
    for p in sorted(args.disasm.glob("*.madlen")):
        info = parse_madlen(p)
        info["lines"] = sum(1 for _ in p.open(encoding="utf-8", errors="replace"))
        madlen[info["module"]] = info
    say(f"  dtran-листингов: {len(madlen)}")

    ann_paths = sorted(args.src.glob("*.mad")) + sorted(args.include.glob("*.xref.md"))
    _, annotated_names = parse_annotated(ann_paths)
    say(f"  аннотированных файлов: {len(ann_paths)}; имён: {len(annotated_names)}")

    modules_csv = read_modules_csv(args.modules_csv)
    say(f"  modules.csv: {len(modules_csv)} строк")

    model = build_model(lib, madlen, modules_csv, annotated_names)
    meta = dict(
        lib_path=str(args.lib),
        sha256=__import__('hashlib').sha256(args.lib.read_bytes()).hexdigest(),
        catalog_entries=len(lib.catalog),
        modules=len(model["module_names"]),
        json_note="--json <путь>",
    )

    md = render_markdown(model, meta)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(md, encoding="utf-8")
    say(f"ЗАПИСАНО: {args.out} ({len(md.splitlines())} строк)")

    if args.json is not None:
        obj = render_json(model, meta)
        text = json.dumps(obj, ensure_ascii=False, indent=2) + "\n"
        if args.json == "-":
            sys.stdout.write(text)
        else:
            Path(args.json).write_text(text, encoding="utf-8")
            say(f"ЗАПИСАНО JSON: {args.json}")

    say("")
    say(f"ВНЕШНИХ СИМВОЛОВ: {len(model['external'])}")
    say(f"НАРУШЕНИЙ 6-СИМВОЛЬНОГО ПРАВИЛА: "
        f"{len(model['violations_long'])} long / {len(model['violations_collision'])} collisions")
    write_log(args.log, log)
    return 0


if __name__ == "__main__":
    sys.exit(main())
