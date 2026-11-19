#!/usr/bin/env python3
"""Строгая проверка матрицы X3.9-1978: 200/200 OK + исполнимое доказательство.

Статус OK в docs/plan-f77-full/01-f77-standard-matrix.md означает не
«нативная поддержка», а «есть исполнимое доказательство» (пробы dispak,
gold-пары, control vectors, lowerings).  Этот скрипт не даёт_ASSIGN OK
строке без непустой колонки доказательства со ссылкой на артефакт.

Использование:
    python3 tests/check-f77-matrix-200.py
    python3 tests/check-f77-matrix-200.py --strict-proof   # только путь-подобная ссылка
"""
import re
import sys
from pathlib import Path

MATRIX = Path(__file__).resolve().parents[1] / "docs/plan-f77-full/01-f77-standard-matrix.md"
ROW = re.compile(r"^\|\s*([A-K]\d+)\s*\|")
STATUSES = {"OK", "NO", "PARTIAL", "UNKNOWN"}
# Токены, которые считаются ссылкой на исполнимое доказательство.
EVIDENCE = re.compile(
    r"(?:logs/|tests/|docs/|src/|[A-Z]\d\d[_-]|\*perso|LIBREFER|K0[56]|"
    r"\.b6\b|\.txt\b|\.md\b|\.ftn\b|gold|digest|cat|\bE[1-5]\b)",
    re.IGNORECASE,
)


def parse(path):
    rows = []
    for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        m = ROW.match(line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            rows.append((m.group(1), lineno, "MALFORMED", ""))
            continue
        rows.append((m.group(1), lineno, cells[2], cells[3]))
    return rows


def main():
    strict = "--strict-proof" in sys.argv[1:]
    rows = parse(MATRIX)
    seen = {}
    problems = []
    counts = {s: 0 for s in STATUSES}

    for ident, lineno, status, proof in rows:
        if ident in seen:
            problems.append(f"{ident}: дубль строк {seen[ident]} и {lineno}")
        seen[ident] = lineno
        if status not in STATUSES:
            problems.append(f"{ident}:{lineno}: неизвестный статус {status!r}")
            continue
        counts[status] += 1
        if status == "OK":
            if not proof or proof in ("—", "-"):
                problems.append(f"{ident}:{lineno}: OK без доказательства")
            elif strict and not EVIDENCE.search(proof):
                problems.append(f"{ident}:{lineno}: доказательство без ссылки: {proof!r}")

    expected_ids = {f"A{i}" for i in range(1, 9)} | {f"B{i}" for i in range(1, 14)}
    expected_ids |= {f"C{i}" for i in range(1, 11)} | {f"D{i}" for i in range(1, 5)}
    expected_ids |= {f"E{i}" for i in range(1, 16)} | {f"F{i}" for i in range(1, 20)}
    expected_ids |= {f"G{i}" for i in range(1, 10)} | {f"H{i}" for i in range(1, 8)}
    expected_ids |= {f"I{i}" for i in range(1, 8)} | {f"J{i}" for i in range(1, 29)}
    expected_ids |= {f"K{i}" for i in range(1, 81)}
    for ident in sorted(expected_ids - set(seen)):
        problems.append(f"{ident}: отсутствует в матрице")
    for ident in sorted(set(seen) - expected_ids):
        problems.append(f"{ident}: лишняя строка ({seen[ident]})")

    total = len(rows)
    print(f"MATRIX {MATRIX.relative_to(MATRIX.parents[2])}")
    print(f"строк: {total} (ожидается 200); уникальных ID: {len(seen)}")
    print("счётчик:", " ".join(f"{s}={counts[s]}" for s in ("OK", "NO", "PARTIAL", "UNKNOWN")))

    if total != 200 or len(seen) != 200:
        problems.append(f"ожидается 200 строк, получено {total}/{len(seen)}")
    if counts["OK"] != 200:
        problems.append(f"цель 200/200 OK не достигнута: OK={counts['OK']}")
    if problems:
        print(f"FAIL: {len(problems)} проблем(а)")
        for p in problems[:60]:
            print("  - " + p)
        if len(problems) > 60:
            print(f"  ... и ещё {len(problems) - 60}")
        return 1
    print("OK: 200/200, каждая строка OK имеет исполнимое доказательство")
    return 0


if __name__ == "__main__":
    sys.exit(main())
