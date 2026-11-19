#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""УНИВЕРСАЛЬНЫЙ декодер/сканер текстовых констант БЭСМ-6.

Для любого 48-битного слова инструмент показывает ВСЕ правдоподобные
прочтения в разных кодировках и оценивает каждое по доле печатных символов.

Поддерживаемые кодировки
------------------------
  6 бит / 8 символов на слово (группы Bios 42..0 с шагом 6):
    TEXT        ASCII-0x20 (MADLEN / Тюрин: «8 символов в коде TEXT»)
    TEXT-DUBNA  таблица монитора Дубны text_to_gost (то, что печатает dtran)
    GOST6       GOST-10859, 6-битная графика (gost10859.h), латиница/кириллица
  8 бит / 6 байт на слово (группы 40..0 с шагом 8):
    GOST8       GOST-10859, GOST_LATIN / GOST_CYRILLIC (encoding.cpp)
    UPP         УПП = GOST-10859 + бит чётности в 8-м разряде (ГОСТ 10861-64)
    ISO         ISO Дубны = koi7_to_unicode (dtran get_iso_char)
    KOI-7       KOI-7 Н2 (encoding.cpp:koi7_to_unicode)
    ITM         автокод Чайковского (encoding.cpp:itm_to_gost)
    COSY        COSY-поток = KOI-7 + RLE-пробелы 0x81..0xD3 (CosyCodec)
    ASCII       plain 7-bit ASCII (0x20..0x7E)

Источники таблиц (все проверены 2026-11-19):
  /home/azizz/Yandex.Disk/monitor80-re/tools/gost10859.h
  /home/azizz/Yandex.Disk/monitor80-re/tools/encoding.cpp
  /home/azizz/Yandex.Disk/besm6-new/besm6.net/src/Besm6.Runtime/Devices/PunchCardCodec.cs
  /home/azizz/Yandex.Disk/besm6-new/besm6.net/src/Besm6.Runtime/Encoding/CosyCodec.cs
  /home/azizz/Yandex.Disk/re-dispak/rukava.be (карта зон: «КОДИРОВКА УПП»)
  /home/azizz/Yandex.Disk/re-dispak/docs/tyurin1985/tyurin1985-full.txt
      (прил.: «Код устройства подготовки перфокарт УПП-1 и АЦПУ-128-3»;
       §«Текстовая константа»: 6 символов УПП/ISO или 8 символов TEXT в слове)
  /home/azizz/Yandex.Disk/dtran/dtran.cc (dms_is_iso, is_likely_text, get_iso_char)

МЕТРИКА.  Для каждого прочтения считаются две доли:
  печатная  — доля позиций, где таблица дала видимый глиф (не {\0}/управление);
  уверенность — доля позиций с «уверенным» символом (буква, цифра, пробел,
              базовая пунктуация), плюс маска dtran is_likely_text для 6-битных.
`--threshold` фильтрует по уверенности (по умолчанию 0.60).

ИСПОЛЬЗОВАНИЕ
-------------
  python3 tools/besm6_text_scan.py --word 0o5457126371560000
  python3 tools/besm6_text_scan.py --word 0o1502244213020060 --encoding GOST8 --json
  python3 tools/besm6_text_scan.py --file src/FOREX_CORE.mad
  python3 tools/besm6_text_scan.py --dir src --log logs/besm6_text_scan.txt
  python3 tools/besm6_text_scan.py --list-encodings
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_LOG = ROOT / "logs" / "besm6_text_scan.txt"
WORD_MASK = (1 << 48) - 1

# ── Таблицы ───────────────────────────────────────────────────────────────────

# dtran.cc:59 — таблица TEXT монитора Дубны (code -> глиф, режим GOST_LATIN).
TEXT_DUBNA = " .БЦДФГИ()*ЙЛЯЖ/0123456789Ь,П-+ЫЗ" \
             "ABCDEFGHIJKLMNOPQRSTUVWXYZШЭЩЧЮ"
assert len(TEXT_DUBNA) == 64

# dtran.cc:is_likely_text — «допустимые» коды 6-битного TEXT:
# пробел, '*', '/', цифры, '-', '+', A-Z.  Остальные — кириллица/служебные.
TEXT_VALID_CODES = frozenset(
    [0, 10, 15, *range(16, 26), 29, 30, *range(33, 59)]
)

# gost10859.h / encoding.cpp:gost_to_unicode_cyr[0..127]. 0 = нет глифа.
GOST_CYR = [
    0x30,0x31,0x32,0x33,0x34,0x35,0x36,0x37, 0x38,0x39,0x2b,0x2d,0x2f,0x2c,0x2e,0x20,
    0x23e8,0x2191,0x28,0x29,0xd7,0x3d,0x3b,0x5b, 0x5d,0x2a,0x2018,0x2019,0x2260,0x3c,0x3e,0x3a,
    0x0410,0x0411,0x0412,0x0413,0x0414,0x0415,0x0416,0x0417,
    0x0418,0x0419,0x041a,0x041b,0x041c,0x041d,0x041e,0x041f,
    0x0420,0x0421,0x0422,0x0423,0x0424,0x0425,0x0426,0x0427,
    0x0428,0x0429,0x042b,0x042c,0x042d,0x042e,0x042f,0x44,
    0x46,0x47,0x49,0x4a,0x4c,0x4e,0x51,0x52, 0x53,0x55,0x56,0x57,0x5a,0x203e,0x2a7d,0x2a7e,
    0x2228,0x2227,0x2283,0xac,0xf7,0x2261,0x25,0x25c7,
    0x7c,0x2015,0x5f,0x21,0x22,0x042a,0xb0,0x2032,
] + [0] * 160

# encoding.cpp:gost_to_unicode_lat[0..127] (GOST_LATIN = true по умолчанию).
GOST_LAT = [
    0x30,0x31,0x32,0x33,0x34,0x35,0x36,0x37, 0x38,0x39,0x2b,0x2d,0x2f,0x2c,0x2e,0x20,
    0x23e8,0x2191,0x28,0x29,0xd7,0x3d,0x3b,0x5b, 0x5d,0x2a,0x2018,0x2019,0x2260,0x3c,0x3e,0x3a,
    0x41,0x0411,0x42,0x0413,0x0414,0x45,0x0416,0x0417,
    0x0418,0x0419,0x4b,0x041b,0x4d,0x48,0x4f,0x041f,
    0x50,0x43,0x54,0x59,0x0424,0x58,0x0426,0x0427,
    0x0428,0x0429,0x042b,0x042c,0x042d,0x042e,0x042f,0x44,
    0x46,0x47,0x49,0x4a,0x4c,0x4e,0x51,0x52, 0x53,0x55,0x56,0x57,0x5a,0x203e,0x2a7d,0x2a7e,
    0x2228,0x2227,0x2283,0xac,0xf7,0x2261,0x25,0x25c7,
    0x7c,0x2015,0x5f,0x21,0x22,0x042a,0xb0,0x2032,
] + [0] * 160

# encoding.cpp:koi7_to_unicode[128] (KOI-7 Н2 / «ISO» Дубны).
KOI7 = [
    0,0x01,0x02,0x03,0x04,0x042a,0x06,0xd7,
    0x08,0x09,0x0a,0x0b,0x0c,0x0d,0x2a7d,0x2a7e,
    0x2018,0x11,0x12,0x13,0x14,0x2015,0x2191,0x23e8,
    0x2260,0xb0,0xf7,0x2019,0x2283,0x2261,0x2228,0xac,
    *range(0x20, 0x40), *range(0x40, 0x58),
    0x58,0x59,0x5a,0x5b,0x203e,0x5d,0x7c,0x5f,
    0x042e,0x0410,0x0411,0x0426,0x0414,0x0415,0x0424,0x0413,
    0x0425,0x0418,0x0419,0x041a,0x041b,0x041c,0x041d,0x041e,
    0x041f,0x042f,0x0420,0x0421,0x0422,0x0423,0x0416,0x0412,
    0x042c,0x042b,0x0417,0x0428,0x042d,0x0429,0x0427,0x7f,
]
assert len(KOI7) == 128

# encoding.cpp:text_to_gost[64] — код TEXT Дубны -> код GOST-10859.
TEXT_TO_GOST_OCT = """
0017 0016 0041 0066 0044 0064 0043 0050
0022 0023 0031 0051 0053 0076 0046 0014
0000 0001 0002 0003 0004 0005 0006 0007
0010 0011 0073 0015 0057 0013 0012 0072
0047 0040 0042 0061 0044 0045 0100 0101
0055 0102 0103 0052 0053 0054 0056 0106
0057 0107 0105 0110 0111 0112 0113 0114
0115 0116 0117 0070 0074 0071 0067 0075
""".split()
assert len(TEXT_TO_GOST_OCT) == 64
TEXT_TO_GOST = [int(x, 8) for x in TEXT_TO_GOST_OCT]

# encoding.cpp:itm_to_gost[256] — код автокода Чайковского -> код GOST-10859.
ITM_TO_GOST_OCT = """
000 001 002 003 004 005 006 007 010 011 000 000 000 000 000 017
000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000
017 033 127 132 130 026 015 016 115 023 000 027 036 136 037 025
120 012 126 133 032 037 030 014 013 121 124 000 035 032 022 000
000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000
000 000 000 000 000 000 000 000 000 000 000 000 134 135 000 033
000 000 000 021 000 123 035 036 013 000 034 000 000 000 000 000
000 000 000 000 000 000 000 000 031 000 000 000 000 000 020 000
000 062 000 056 000 055 054 053 000 052 060 043 102 057 061 042
020 114 044 041 110 063 100 124 040 113 103 000 064 106 052 000
000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000
000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000
000 071 000 000 000 000 000 000 000 053 000 043 050 057 066 046
074 047 044 041 070 072 064 073 000 067 051 000 075 076 000 000
000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000
000 000 000 000 000 000 000 000 000 000 000 000 000 000 000 000
""".split()
assert len(ITM_TO_GOST_OCT) == 256
ITM_TO_GOST = [int(x, 8) for x in ITM_TO_GOST_OCT]

# ── Вспомогательное ──────────────────────────────────────────────────────────

SAFE_PUNCT = frozenset(".,-+*/()=:;'\"!?%#&$@_<>[]{}|^~\\`")


def parse_word(s: str) -> int:
    """Восьмеричное (0o... или без префикса), 0x..., 0b... или десятичное слово."""
    t = s.strip().replace("_", "")
    try:
        if t.lower().startswith("0o"):
            v = int(t[2:], 8)
        elif t.lower().startswith("0x"):
            v = int(t, 16)
        elif t.lower().startswith("0b"):
            v = int(t, 2)
        else:
            v = int(t, 8)          # по умолчанию — восьмеричное
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"плохое слово: {s!r}") from exc
    if not 0 <= v <= WORD_MASK:
        raise argparse.ArgumentTypeError(f"слово вне 48 бит: {s!r}")
    return v


def groups6(word: int) -> list[int]:
    return [(word >> s) & 0o77 for s in (42, 36, 30, 24, 18, 12, 6, 0)]


def bytes8(word: int) -> list[int]:
    return [(word >> s) & 0xFF for s in (40, 32, 24, 16, 8, 0)]


def gost_char(code: int, latin: bool = True) -> str:
    table = GOST_LAT if latin else GOST_CYR
    u = table[code & 0xFF] if 0 <= code < 256 else 0
    return chr(u) if u else "\0"


def koi_char(code: int) -> str:
    u = KOI7[code & 0x7F] if 0 <= code < 128 else 0
    # DEL и неопределённые коды считаем непечатными
    return chr(u) if u and u != 0x7f else "\0"


def iso_char(code: int) -> str:
    """dtran get_iso_char: 040..0160 - ASCII, 0160..0176 - кириллица, иначе _NNN."""
    ch = code & 0o177
    if 0o040 <= ch < 0o140:
        return chr(ch)
    if ch < 0o040 or ch >= 0o177:
        return "\0"
    rus = "ЮАБЦДЕФГХИЙКЛМНОПЯРСТУЖВЬЫЗШЭЩЧ\177"
    return rus[2 * (ch - 0o140): 2 * (ch - 0o140) + 2]


def classify(ch: str, code: int | None = None,
             code_mask: frozenset[int] | None = None) -> str:
    """'strong' (уверенный), 'weak' (печатный, но редкий), 'bad' (мусор)."""
    if not ch or ch in ("\0", "\x7f"):
        return "bad"
    if len(ch) > 1:                 # ISO-кириллица в dtran — двухбайтовый глиф
        return "strong"
    if ord(ch) < 0x20:
        return "bad"
    if code_mask is not None:
        return "strong" if code in code_mask else "bad"
    if ch.isalnum() or ch == " " or ch in SAFE_PUNCT:
        return "strong"
    if ch.isprintable():
        return "weak"
    return "bad"


@dataclass
class Reading:
    encoding: str
    width: str
    text: str
    printable: float
    confidence: float
    stars: str
    verdict: str


# ── Декодеры ─────────────────────────────────────────────────────────────────

def dec_text_ascii(word: int) -> tuple[str, list[str]]:
    gs = groups6(word)
    return "".join(chr(c + 0x20) for c in gs), [
        classify(chr(c + 0x20), c, TEXT_VALID_CODES) for c in gs
    ]


def dec_text_dubna(word: int) -> tuple[str, list[str]]:
    gs = groups6(word)
    return "".join(TEXT_DUBNA[c] for c in gs), [
        classify(TEXT_DUBNA[c], c, TEXT_VALID_CODES) for c in gs
    ]


def mark_padding(cls: list[str], codes: list[int], zero: int) -> list[str]:
    """Ведущие/конечные нулевые группы — паддинг, внутренние нули — мусор."""
    first, last = 0, len(cls) - 1
    while first <= last and codes[first] == zero:
        first += 1
    while last >= first and codes[last] == zero:
        last -= 1
    out = list(cls)
    for i in range(first):
        out[i] = "pad"
    for i in range(last + 1, len(out)):
        out[i] = "pad"
    for i in range(first, last + 1):
        if codes[i] == zero:
            out[i] = "bad"
    return out


def dec_gost6(word: int, latin: bool) -> tuple[str, list[str]]:
    gs = groups6(word)
    chars = [gost_char(c, latin) for c in gs]
    return "".join(chars), mark_padding([classify(c) for c in chars], gs, 0)


def dec_bytes(word: int, convert, pad_zero: bool = True) -> tuple[str, list[str]]:
    bs = bytes8(word)
    chars = [convert(b) for b in bs]
    cls = [classify(c) for c in chars]
    return "".join(chars), mark_padding(cls, bs, 0) if pad_zero else cls


def dec_gost8(word: int, latin: bool) -> tuple[str, list[str]]:
    return dec_bytes(word, lambda b: gost_char(b, latin))


def dec_upp(word: int) -> tuple[str, list[str]]:
    """УПП = GOST-10859 (lat) + бит 8 = чётность; сбрасываем бит 7."""
    return dec_bytes(word, lambda b: gost_char(b & 0x7F, True))


def dec_iso(word: int) -> tuple[str, list[str]]:
    return dec_bytes(word, iso_char)


def dec_koi7(word: int) -> tuple[str, list[str]]:
    return dec_bytes(word, koi_char)


def dec_itm(word: int) -> tuple[str, list[str]]:
    # ITM-таблица разрежена: 0 в ITM_TO_GOST означает «нет символа», но
    # GOST-код 0000 — это цифра '0'. Различаем по самому ITM-байту.
    def conv(b: int) -> str:
        g = ITM_TO_GOST[b]
        if g == 0 and not (0 <= b <= 9):
            return "\0"
        return gost_char(g, True)
    return dec_bytes(word, conv)


def dec_cosy(word: int) -> tuple[str, list[str]]:
    """COSY: KOI-7 + RLE 0x81..0xD3 (повтор пробела), как в CosyCodec.DecodeCosy."""
    out: list[str] = []
    cls: list[str] = []
    bs = bytes8(word)
    for b in bs:
        if 0x81 <= b <= 0xD3:
            out.append(" ")
            cls.append("strong")
        else:
            c = koi_char(b)
            out.append(c)
            cls.append(classify(c))
    return "".join(out), mark_padding(cls, bs, 0)


def dec_ascii(word: int) -> tuple[str, list[str]]:
    return dec_bytes(word, lambda b: chr(b) if 0x20 <= b <= 0x7E else "\0")


DECODERS = [
    ("TEXT",            "6x8", dec_text_ascii),
    ("TEXT-DUBNA",      "6x8", dec_text_dubna),
    ("GOST6-LAT",       "6x8", lambda w: dec_gost6(w, True)),
    ("GOST6-CYR",       "6x8", lambda w: dec_gost6(w, False)),
    ("GOST8-LAT",       "8x6", lambda w: dec_gost8(w, True)),
    ("GOST8-CYR",       "8x6", lambda w: dec_gost8(w, False)),
    ("UPP",             "8x6", dec_upp),
    ("ISO",             "8x6", dec_iso),
    ("KOI-7",           "8x6", dec_koi7),
    ("ITM",             "8x6", dec_itm),
    ("COSY",            "8x6", dec_cosy),
    ("ASCII",           "8x6", dec_ascii),
]
DECODER_MAP = {name: fn for name, _, fn in DECODERS}


def make_reading(word: int, name: str, fn) -> Reading:
    from collections import Counter
    text, cls = fn(word)
    eff = [c for c in cls if c != "pad"]
    n = len(eff)
    strong = sum(c == "strong" for c in eff)
    printable = sum(c in ("strong", "weak") for c in eff)
    conf = strong / n if n else 0.0
    pr = printable / n if n else 0.0
    # Анти-маска: слово из повторяющегося символа — не текст, а битовая маска.
    if n and len(text) == len(cls):   # ISO-диграфы меняют длину строки
        counts = Counter(text[i] for i, c in enumerate(cls) if c != "pad")
        if counts and max(counts.values()) / n > 0.40:
            conf *= 0.30
            pr *= 0.60
    stars_n = 0 if conf < 0.34 else (1 if conf < 0.67 else (2 if conf < 0.9 else 3))
    verdict = ("уверенно" if conf >= 0.9 else
               "правдоподобно" if conf >= 0.67 else
               "сомнительно" if conf >= 0.34 else "мусор")
    shown = "".join(c if (c and c.isprintable()) else "·" for c in text)
    width = next(w for nm, w, _ in DECODERS if nm == name)
    return Reading(name, "6 бит×8" if width == "6x8" else "8 бит×6",
                   shown, pr, conf, "★" * stars_n, verdict)


def analyze(word: int, names: list[str] | None = None) -> list[Reading]:
    chosen = [(nm, fn) for nm, _, fn in DECODERS if not names or nm in names]
    return [make_reading(word, nm, fn) for nm, fn in chosen]


def best_reading(word: int, names: list[str] | None = None) -> Reading:
    return max(analyze(word, names), key=lambda r: (r.confidence, r.printable))


# ── Извлечение слов из .mad ──────────────────────────────────────────────────

RE_WORD_EQ = re.compile(r"=\s*0o([0-7]{16})\b")
RE_WORD16 = re.compile(r"(?<![0-7A-Za-z])([0-7]{16})(?![0-7A-Za-z])")
RE_LITERAL = re.compile(r"(?<![A-Za-z0-9_])([1-9])H((?:\'[0-7]{3}\'|\'[^\']*\'|[^\s;,]+)+)")
# Любая расшифровка в комментарии: DEKOD, ссылка на источник, TEXT='...',
# описание «TEXT/GOST/ISO-константа».
ANNOT_RE = re.compile(
    r"DEKOD|\[источник:|TEXT\s*=\s*['\"]|TEXT-константа|TEXT-имени|"
    r"GOST-константа|ISO-константа|UPP-константа|GOST-строка|GOST\(6→8\)"
)
RE_BLOCK_START = re.compile(r"^\s*С[-\s]*слово\b")



def parse_literal(chars: str, width: int) -> int | None:
    """8Hxxx -> 6-битные коды ASCII-0x20; 6Hxxx -> 8-битные байты ASCII."""
    items: list[int] = []
    i = 0
    while i < len(chars) and len(items) < width:
        if chars[i] == "'":
            m = re.match(r"\'([0-7]{3})\'", chars[i:])
            if m:
                items.append(int(m.group(1), 8))
                i += len(m.group(0))
                continue
            m2 = re.match(r"\'([^\']*)\'", chars[i:])
            if m2:
                for c in m2.group(1):
                    items.append(ord(c) & 0xFF)
                i += len(m2.group(0))
                continue
        items.append(ord(chars[i]) & 0xFF)
        i += 1
    if not items:
        return None
    word = 0
    if width == 8:                      # TEXT: 6 бит/символ, code = ASCII-0x20
        for c in items[:8]:
            word = (word << 6) | ((c - 0x20) & 0o77)
        return word << (6 * (8 - min(len(items), 8)))
    for c in items[:6]:                 # 8-бит: байты выравниваются вправо
        word = (word << 8) | (c & 0xFF)
    return word


@dataclass
class FoundWord:
    file: str
    line: int
    word: int
    source: str
    annotated: bool
    reading: str = ""
    encoding: str = ""
    confidence: float = 0.0


def scan_file(path: Path) -> list[FoundWord]:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    found: list[FoundWord] = []
    block_indices: list[int] = []       # слова текущего блока «С слово …»
    rel = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path)

    for idx, line in enumerate(lines, 1):
        is_block_start = bool(RE_BLOCK_START.match(line))
        if is_block_start:
            block_indices = []
        annotated_here = bool(ANNOT_RE.search(line))

        seen: set[int] = set()
        for m in RE_WORD_EQ.finditer(line):
            w = int(m.group(1), 8) & WORD_MASK
            if w not in seen:
                found.append(FoundWord(rel, idx, w, "= 0o...", annotated_here))
                seen.add(w)
                if is_block_start:
                    block_indices.append(len(found) - 1)
        # голые 16-значные восьмеричные слова (EQU, OCT и т.п.)
        for m in RE_WORD16.finditer(line):
            if m.start() > 0 and line[m.start() - 1] in "oO":
                continue
            w = int(m.group(1), 8) & WORD_MASK
            if w and w not in seen:
                found.append(FoundWord(rel, idx, w, "oct16", annotated_here))
                seen.add(w)
                if is_block_start:
                    block_indices.append(len(found) - 1)
        # 8H/6H/1H.. литералы
        for m in RE_LITERAL.finditer(line):
            width = int(m.group(1))
            if width not in (6, 8):
                continue
            w = parse_literal(m.group(2), width)
            if w is not None and w not in seen:
                found.append(FoundWord(rel, idx, w, f"{width}H literal", annotated_here))
                seen.add(w)
                if is_block_start:
                    block_indices.append(len(found) - 1)
        # аннотация «С → … DEKOD …» относится ко всему предыдущему блоку
        if annotated_here and block_indices:
            for i in block_indices:
                found[i].annotated = True
            block_indices = []
    return found


def scan_paths(paths: list[Path], threshold: float, names=None) -> list[FoundWord]:
    out: list[FoundWord] = []
    for p in paths:
        out.extend(scan_file(p))
    for fw in out:
        b = best_reading(fw.word, names)
        fw.encoding = b.encoding
        fw.reading = b.text
        fw.confidence = b.confidence
    return out


# ── Вывод ────────────────────────────────────────────────────────────────────

def print_table(word: int, names=None, threshold: float = 0.0) -> None:
    rows = [r for r in analyze(word, names) if r.confidence >= threshold]
    rows.sort(key=lambda r: -r.confidence)
    print(f"СЛОВО 0o{word:016o}  (0x{word:012x}, {word} dec)")
    print("=" * 100)
    print(f"{'КОДИРОВКА':<12} {'ШИРИНА':<9} {'ПРОЧТЕНИЕ':<26} {'ПЕЧАТН.':>8} {'УВЕРЕН.':>8}  {'ОЦЕНКА':<10} ВЕРДИКТ")
    print("-" * 100)
    for r in rows:
        print(f"{r.encoding:<12} {r.width:<9} |{r.text:<24}| {r.printable:>7.3f} "
              f"{r.confidence:>8.3f}  {r.stars:<10} {r.verdict}")
    if not rows:
        print("  (нет кодировок выше порога)")
    print()


def write_report(paths: list[Path], log: Path, threshold: float, names=None) -> int:
    all_w = scan_paths(paths, threshold, names)
    total = len(all_w)
    annotated = sum(f.annotated for f in all_w)
    unannot = [f for f in all_w if not f.annotated]
    plausible = [f for f in unannot if f.confidence >= threshold]
    plausible.sort(key=lambda f: (-f.confidence, f.file, f.line))

    enc_counts: dict[str, int] = {}
    for f in all_w:
        enc_counts[f.encoding] = enc_counts.get(f.encoding, 0) + 1

    lines: list[str] = []
    ap = lines.append
    ap("# Лог сканера текстовых констант БЭСМ-6")
    ap(f"# Сгенерировано tools/besm6_text_scan.py; порог уверенности = {threshold:.2f}")
    ap(f"# Файлы: {', '.join(str(p) for p in paths)}")
    ap("")
    ap("## Сводка")
    ap(f"  просканировано-word-вхождений : {total}")
    ap(f"  с аннотацией DEKOD            : {annotated}")
    ap(f"  БЕЗ аннотации DEKOD           : {len(unannot)}")
    ap(f"  из них правдоподобных ({threshold:.2f})+ : {len(plausible)}")
    ap("")
    ap("  Лучшая кодировка среди ВСЕХ слов:")
    for enc, cnt in sorted(enc_counts.items(), key=lambda kv: -kv[1]):
        ap(f"    {enc:<12} {cnt:>5}")
    ap("")
    ap("  Примечание: «печатная» доля — доля видимых глифов; «уверенность» —")
    ap("  доля букв/цифр/пробелов/базовой пунктуации (для 6 бит — маска dtran")
    ap("  is_likely_text). Порог применяется к уверенности.")
    ap("")
    ap("## Слова БЕЗ расшифровки в комментариях (отсортированы по убыванию уверенности)")
    ap("")
    ap(f"{'ФАЙЛ:СТРОКА':<44} {'СЛОВО':<20} {'ИСТОЧНИК':<14} {'КОДИР.':<11} {'УВЕР.':>6}  ПРОЧТЕНИЕ")
    ap("-" * 132)
    for f in plausible:
        ap(f"{f.file + ':' + str(f.line):<44} 0o{f.word:016o} {f.source:<14} "
           f"{f.encoding:<11} {f.confidence:>6.3f}  |{f.reading}|")
    ap("-" * 132)
    ap("")

    # Приоритетные находки: TEXT-имя (звёздочка / ПРОПИСНЫЕ) или кириллическое слово.
    def looks_like_name(f: FoundWord) -> bool:
        s = f.reading.strip()
        if f.encoding in ("TEXT", "TEXT-DUBNA"):
            return ("*" in s or (len(s) >= 3 and s.isupper())) and len(s) >= 3
        if f.encoding in ("GOST8-CYR", "GOST8-LAT", "GOST6-CYR", "GOST6-LAT"):
            return len(s) >= 3 and s.replace(" ", "").isalpha()
        return False

    priority = [f for f in plausible if looks_like_name(f)]
    ap(f"## Приоритетные находки ({len(priority)}) — похожи на имена/слова")
    ap("")
    ap(f"{'ФАЙЛ:СТРОКА':<44} {'СЛОВО':<20} {'КОДИР.':<11} {'УВЕР.':>6}  ПРОЧТЕНИЕ")
    ap("-" * 116)
    for f in priority[:300]:
        ap(f"{f.file + ':' + str(f.line):<44} 0o{f.word:016o} {f.encoding:<11} "
           f"{f.confidence:>6.3f}  |{f.reading}|")
    if len(priority) > 300:
        ap(f"… и ещё {len(priority) - 300}")
    ap("-" * 116)
    ap("")
    ap("## Детальные таблицы для 25 наиболее правдоподобных нерасшифрованных слов")
    ap("")
    for f in plausible[:25]:
        ap(f"### {f.file}:{f.line}  0o{f.word:016o}  ({f.source})")
        ap("")
        rows = [r for r in analyze(f.word, names) if r.confidence >= 0.34]
        rows.sort(key=lambda r: -r.confidence)
        ap("| Кодировка | Прочтение | Печатная | Уверенность | Оценка |")
        ap("|---|---|---:|---:|---|")
        for r in rows:
            ap(f"| {r.encoding} | `{r.text}` | {r.printable:.3f} | {r.confidence:.3f} | {r.stars} |")
        ap("")

    log.parent.mkdir(parents=True, exist_ok=True)
    log.write_text("\n".join(lines), encoding="utf-8")
    print(f" Najdeno: всего {total}, с DEKOD {annotated}, без DEKOD {len(unannot)}, "
          f"правдоподобных {len(plausible)}")
    print(f" Лог записан: {log}")
    return total


def collect_inputs(args) -> list[Path]:
    paths: list[Path] = []
    if args.file:
        paths.extend(args.file)
    if args.dir:
        for d in args.dir:
            paths.extend(sorted(d.rglob("*.mad")))
    # дедупликация с сохранением порядка
    seen: set[Path] = set()
    uniq = []
    for p in paths:
        rp = p.resolve()
        if rp not in seen:
            seen.add(rp)
            uniq.append(p)
    return uniq


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--word", action="append", default=[], type=parse_word,
                    help="48-битное слово (0o..., 0x... или восьмеричное); можно повторить")
    ap.add_argument("--file", action="append", type=Path, default=[],
                    help="сканировать один .mad-файл")
    ap.add_argument("--dir", action="append", type=Path, default=[],
                    help="сканировать все *.mad в каталоге рекурсивно")
    ap.add_argument("--encoding", default="",
                    help="только указанные кодировки (через запятую); по умолчанию все")
    ap.add_argument("--json", action="store_true", help="вывод в JSON")
    ap.add_argument("--threshold", type=float, default=0.60,
                    help="минимальная уверенность (по умолчанию 0.60)")
    ap.add_argument("--log", type=Path, default=DEFAULT_LOG,
                    help=f"файл лога сканирования (по умолчанию {DEFAULT_LOG})")
    ap.add_argument("--list-encodings", action="store_true",
                    help="список кодировок и выход")
    args = ap.parse_args()

    if args.list_encodings:
        for nm, w, _ in DECODERS:
            print(f"{nm:<12} {w}  — {DECODER_DESCRIPTIONS.get(nm, '')}")
        return 0

    names = [x.strip() for x in args.encoding.split(",") if x.strip()] or None
    if names:
        bad = [n for n in names if n not in DECODER_MAP]
        if bad:
            raise SystemExit(f"неизвестная кодировка: {', '.join(bad)}; "
                             f"доступные: {', '.join(DECODER_MAP)}")

    if args.word:
        if args.json:
            out = [asdict(r) for w in args.word for r in analyze(w, names)
                   if r.confidence >= args.threshold]
            print(json.dumps(out, ensure_ascii=False, indent=2))
        else:
            for w in args.word:
                print_table(w, names, args.threshold)
        return 0

    paths = collect_inputs(args)
    if not paths:
        raise SystemExit("укажите --word, --file и/или --dir (или --list-encodings)")
    missing = [p for p in paths if not p.is_file()]
    if missing:
        raise SystemExit(f"нет файлов: {', '.join(str(m) for m in missing[:5])}")
    write_report(paths, args.log, args.threshold, names)
    return 0


DECODER_DESCRIPTIONS = {
    "TEXT": "ASCII−0x20, 8 символов/слово (MADLEN/Тюрин)",
    "TEXT-DUBNA": "таблица text_to_gost монитора Дубны (как dtran)",
    "GOST6-LAT": "GOST-10859 6 бит, латинские гомоглифы",
    "GOST6-CYR": "GOST-10859 6 бит, кириллица",
    "GOST8-LAT": "GOST-10859 8 бит, латиница",
    "GOST8-CYR": "GOST-10859 8 бит, кириллица",
    "UPP": "УПП/ГОСТ 10861-64 = GOST-10859 + чётность",
    "ISO": "ISO Дубны (koi7_to_unicode), 6 байт/слово",
    "KOI-7": "KOI-7 Н2",
    "ITM": "автокод Чайковского (itm_to_gost)",
    "COSY": "COSY-поток = KOI-7 + RLE-пробелы",
    "ASCII": "plain 7-bit ASCII",
}


if __name__ == "__main__":
    sys.exit(main())
