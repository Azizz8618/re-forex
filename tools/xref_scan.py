#!/usr/bin/env python3
"""Сканер переходов и вызовов в листингах БЭСМ-6.

Поддерживает два формата:
  * disbesm6 .lst  — строки вида `   17 15 31 20116  пв '20116'(М15)`;
  * besm6tape dis  — строки вида `241530  1004104034047554  сл 1040(2),сл 7554(7)`.

Строит таблицу «источник -> цель» и гистограмму целей.
Независимая проверка ручных аннотаций в src/*.mad и include/*.xref.md.
"""

import argparse
import re
from collections import Counter
from pathlib import Path

CONTROL = {
    "пб", "пв", "по", "пе", "пио", "пино", "пио36", "цикл", "выпр", "стоп",
    "uj", "vjm", "uza", "u1a", "vlm", "pio", "pino", "vzm", "vim", "stop",
}
ADDR_RAW = re.compile(r"^\s*([0-7]{1,4})\s")
ADDR_FULL = re.compile(r"^\s*([0-7]{6})\s+[0-9a-fA-F]{16}\s+(.*)$")
TARGET = re.compile(r"(?:'([0-7]+)'|(?<![A-Za-zА-Яа-я])([0-7]{3,6})\b)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("listing", type=Path)
    ap.add_argument("--out", type=Path, help="файл markdown (по умолчанию stdout)")
    args = ap.parse_args()

    rows = []
    cur = 0
    for raw in args.listing.read_text(errors="replace").splitlines():
        if raw.startswith("*"):
            continue
        m = ADDR_FULL.match(raw)
        if m:
            cur = int(m.group(1), 8)
            rest = m.group(2)
            ops = [o.strip().lower() for o in rest.split(",")]
            for op in ops:
                head = op.split()[0] if op.split() else ""
                if head not in CONTROL:
                    continue
                found = TARGET.findall(op)
                tgt = next((a or b for a, b in found if a or b), "")
                rows.append((cur, head, tgt, op))
            continue
        m = ADDR_RAW.match(raw)
        if m:
            cur = int(m.group(1), 8)
        parts = raw.split("\t")
        if len(parts) < 3:
            continue
        op = parts[-2].strip().lower()
        operand = parts[-1].strip()
        if op not in CONTROL:
            continue
        found = TARGET.findall(operand)
        tgt = next((a or b for a, b in found if a or b), "")
        rows.append((cur, op, tgt, operand))

    hist = Counter(r[2] for r in rows if r[2])
    out = [
        "# Переходы и вызовы: " + args.listing.name,
        "",
        f"Всего управляющих команд: **{len(rows)}**; различных целей: **{len(hist)}**.",
        "",
        "| Адрес | Оп | Цель | Операнд |",
        "|---:|:---|:---|---|",
    ]
    for addr, op, tgt, operand in rows:
        out.append(f"| {addr:06o} | {op} | {tgt} | `{operand}` |")
    out += ["", "## Гистограмма целей (топ 40)", "", "| Цель | Число входов |", "|---:|---:|"]
    for tgt, n in hist.most_common(40):
        out.append(f"| {tgt} | {n} |")

    text = "\n".join(out) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text)
        print(f"записано: {args.out} ({len(rows)} строк)")
    else:
        print(text)


if __name__ == "__main__":
    main()
