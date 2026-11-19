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


def t6_encode(text: str) -> int:
    """MADLEN TEXT: 8 символов по 6 бит (код = ASCII - 0x20)."""
    codes = [ord(c) - 0x20 if 32 <= ord(c) < 127 else 0
             for c in text.upper().ljust(8)[:8]]
    hi = lo = 0
    for c in codes[:4]:
        hi = (hi << 6) | c
    for c in codes[4:]:
        lo = (lo << 6) | c
    return (hi << 24) | lo


def load_symbols(path: Path | None) -> dict[int, str]:
    """TSV: адрес (восьмеричный) <tab или пробел> имя процедуры."""
    out: dict[int, str] = {}
    if not path:
        return out
    for line in path.read_text(errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.replace("\t", " ").split()
        if len(parts) >= 2:
            try:
                addr = int(parts[0], 8)
            except ValueError:
                continue
            out[addr & 0o3777] = parts[1]
    return out


def make_dms(words: list[int], sym_len: int = 0o7777,
             symbols: dict[int, str] | None = None) -> list[int]:
    name = words[1]
    code = words[2:]
    head_len = 1
    w0 = (sym_len << 12) | head_len
    w1 = 0
    w2 = len(code)
    # Симтаблица: числовые имена вида NNNNNB вместо пустых «dunno»;
    # для известных адресов подставляется настоящее имя процедуры.
    symtab = [(0o400 << 15) | i for i in range(sym_len)]
    for idx, text in (symbols or {}).items():
        if 0 <= idx < sym_len:
            symtab[idx] = t6_encode(text)
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
    ap.add_argument("--symbols", type=Path,
                    help="TSV с соответствием адрес(8) -> имя процедуры")
    args = ap.parse_args()

    words = read_words(args.dump)
    dms = make_dms(words, symbols=load_symbols(args.symbols))
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
