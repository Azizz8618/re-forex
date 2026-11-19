#!/usr/bin/env python3
"""Извлечение слов оверлеев FOREX из ленты monsys.9 и декодирование констант.

Формат: 48-битное слово = 6 байт big-endian; зона = 1024 слова.
Все номерá зон/слов в аргументах и выводе ВОСЬМЕРИЧНЫЕ.
"""

import argparse
import hashlib
from pathlib import Path

DEFAULT_TAPE = "/home/azizz/Yandex.Disk/besm6-new/besm6.net/tapes/monsys.9"
WORD_BYTES = 6
ZONE_WORDS = 1024


def words_from_tape(path: Path, start_word: int, count: int) -> list[int]:
    with path.open("rb") as f:
        f.seek(start_word * WORD_BYTES)
        data = f.read(count * WORD_BYTES)
    if len(data) != count * WORD_BYTES:
        raise ValueError(f"короткое чтение: {len(data)} байт вместо {count * WORD_BYTES}")
    return [int.from_bytes(data[i:i + WORD_BYTES], "big") for i in range(0, len(data), WORD_BYTES)]


def t6(word: int) -> str:
    """MADLEN TEXT: 8 шестибитных символов на слово, код = ASCII - 0x20."""
    out = []
    for half in ((word >> 24) & 0xFFFFFF, word & 0xFFFFFF):
        for shift in (18, 12, 6, 0):
            code = ((half >> shift) & 0x3F) + 0x20
            out.append(chr(code) if 32 <= code < 127 else "?")
    return "".join(out)


def octal_words(words: list[int], limit: int = 8) -> str:
    return " ".join(f"{w:o}" for w in words[:limit])


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--tape", type=Path, default=Path(DEFAULT_TAPE))
    p.add_argument("--start", type=lambda s: int(s, 8), required=True,
                   help="начальное слово (восьмеричное), например 241500")
    p.add_argument("--count", type=lambda s: int(s, 8), default=ZONE_WORDS,
                   help="число слов (восьмеричное), по умолчанию 2000")
    p.add_argument("--out", type=Path, help="записать сырые слова в файл")
    p.add_argument("--decode-text", action="store_true",
                   help="показать первые слова как MADLEN TEXT")
    args = p.parse_args()

    words = words_from_tape(args.tape, args.start, args.count)
    print(f"лента      : {args.tape}")
    print(f"начало     : 0o{args.start:o}, слов: {args.count} (0o{args.count:o})")
    print(f"байт offset: {args.start * WORD_BYTES}")
    print(f"sha256     : {hashlib.sha256(b''.join(w.to_bytes(WORD_BYTES, 'big') for w in words)).hexdigest()}")
    print(f"маркеры    : {[i for i, w in enumerate(words) if w == 0o200003]}")
    print(f"первые words: {octal_words(words)}")
    if args.decode_text:
        for i, w in enumerate(words[:16]):
            print(f"  +{i:04o}  0o{w:016o}  TEXT={t6(w)!r}")
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_bytes(b"".join(w.to_bytes(WORD_BYTES, "big") for w in words))
        print(f"записано   : {args.out}")


if __name__ == "__main__":
    main()
