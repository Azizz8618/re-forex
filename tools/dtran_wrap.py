#!/usr/bin/env python3
"""Дизассемблирование сырого дампа оверлея ФОРЭКС в МАДЛЕН через dtran.

Сырая зона оверлея не является объектным модулем DMS, поэтому вокруг её
команд строится синтетический DMS-модуль: распакованный заголовок (3 слова),
тело оверлея как секция команд, имя и расширенная таблица символов.
Расширенная симтаблица необходима: dtran индексирует её маской 07777,
и при короткой таблице падает с segmentation fault.

Использование:
  tools/dtran_wrap.py build/LO_SYN.words --out disasm/LO_SYN.dtran.madlen
"""

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_DTRAN = "/home/azizz/Yandex.Disk/dtran/dtran"
WORD = 6


def read_words(path: Path) -> list[int]:
    data = path.read_bytes()
    if len(data) % WORD:
        raise ValueError("размер дампа не кратен 6 байтам")
    return [int.from_bytes(data[i:i + WORD], "big") for i in range(0, len(data), WORD)]


def make_dms(words: list[int], sym_len: int = 0o7777) -> list[int]:
    name = words[1]
    code = words[2:]
    head_len = 1
    w0 = (sym_len << 12) | head_len
    w1 = 0
    w2 = len(code)
    # Симтаблица: числовые имена вида NNNNNB вместо пустых «dunno».
    # Формат dtran: (0400 << 15) | значение -> symtab[i] = "%oB".
    symtab = [(0o400 << 15) | i for i in range(sym_len)]
    return [w0, w1, w2] + code + [name] + symtab


def clean(text: str) -> str:
    """Убрать шумные комментарии симтаблицы, оставить заголовок модуля."""
    out = []
    for line in text.splitlines():
        if line.startswith("C ") and (
            "dunno" in line or (line[2:].split(":", 1)[0].strip().isdigit())
        ):
            continue
        out.append(line)
    return "\n".join(out).strip() + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("dump", type=Path)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--dtran", default=os.environ.get("DTRAN", DEFAULT_DTRAN))
    ap.add_argument("--raw", action="store_true", help="не фильтровать комментарии")
    args = ap.parse_args()

    words = read_words(args.dump)
    dms = make_dms(words)
    with tempfile.TemporaryDirectory(prefix="forex-dtran-") as td:
        path = Path(td) / "module.dms"
        path.write_bytes(b"".join(w.to_bytes(WORD, "big") for w in dms))
        r = subprocess.run([args.dtran, "-F", "dms", str(path)],
                           capture_output=True, text=True)
        if r.returncode == 0 and not r.stdout.strip():
            print("dtran не дал вывода", file=sys.stderr)
            return 1
        text = r.stdout
        if args.raw:
            text += "\n" + r.stderr
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(clean(text) if not args.raw else text)
    print(f"{args.dump} -> {args.out}: {len(text.splitlines())} строк МАДЛЕН")
    return 0


if __name__ == "__main__":
    sys.exit(main())
