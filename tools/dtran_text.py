#!/usr/bin/env python3
"""Кросс-проверка TEXT/ISO/GOST-констант через	dtran -D.

ЗАЧЕМ
-----
dtran умеет печатать постоянные в разных кодировках.  Команды задаются файлом
`-D` (см. `dtran -h`, `monitor80-re/permanent/*.dtr`)::

    text:2100-2105      # 6-битный TEXT БЭСМ-6 (8 символов на слово)
    gost:2100-2105      # GOST-10859, 8-битные байты (Pascal-B)
    iso:2100-2105       # ISO, 8-битные байты (Pascal-B)
    itm:2100-2105       # ITM, 8-битные байты (Pascal-B)
    code:2100           # точки входа
    base:8              # базовый регистр

ВАЖНОЕ ОГРАНИЧЕНИЕ (установлено 2026-11-19)
--------------------------------------------
Опции `iso:/gost:/itm:/text:` обрабатываются только бэкендами Pascal-A/B.
В DMS-бэкенде (`prconst_dms`) они НЕ используются: константы auto-детектятся
эвристиками `dms_is_iso`/`is_likely_text`.  Поэтому для DMS-модулей результат
`dtran -F dms` с `-D` и без `-D` совпадает, а главным авторитетным чтением
наших 6-битных констант является строка `,TEXT, 8H...`.

Чтобы всё-таки получить все четыре прочтения одного и того же машинного слова,
этот инструмент строит синтетический Pascal-B контейнер: слово `UJ 0,UJ 0`
по адресу 02000 останавливает линейный обход кода, проверяемые слова кладутся
по адресам 02100+, а `-D <enc>:2100-...` заставляет dtran напечатать их в
нужной кодировке.  Синтетический контейнер — только «кодировочный стенд», он
не изменяет ни исходники, ни дампы.

GOST-строки в наших комментариях — это 8 шестибитных групп слова, прочитанных
по gost10859.h (6-битная графика ГОСТ).  dtran's `gost:` читает слово как 6
8-битных байт (Pascal), поэтому на 6-битных TEXT-словах он даёт «мусор».  Оба
прочтения выводятся в отчёте; это НЕ ошибка комментария, а разница форматов.

ИСПОЛЬЗОВАНИЕ
-------------
    tools/dtran_text.py --audit                    # сверка ключевых констант
    tools/dtran_text.py --word 0o5457126371560000   # все кодировки для слова
    tools/dtran_text.py --dms build/FOREX_.dms      # DMS: what dtran prints
    tools/dtran_text.py --module 'FOREX*'           # модуль из lib21.bin
    tools/dtran_text.py --words build/CORE_ROOT.words --offsets 0o45,0o46
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DTRAN = "/home/azizz/Yandex.Disk/dtran/dtran"
LIB = Path("/home/azizz/Yandex.Disk/besm6-new/DUBNA/BUILD/elements/lib21.bin")
SIPROD_TOOLS = Path("/home/azizz/Yandex.Disk/re-siprod/tools")

# dtran.cc:183 — 6-битный TEXT БЭСМ-6 (совпадает с таблицей Дубны).
TEXT = list(" .БЦДФГИ()*ЙЛЯЖ/0123456789Ь,П-+ЫЗ"
            "ABCDEFGHIJKLMNOPQRSTUVWXYZШЭЩЧЮ")
assert len(TEXT) == 64

# gost10859.h — 6-битная графика ГОСТ, как её читает наш аудит.
GOST6 = list("0123456789+-/,.[⏨↑()×=;[]*`'#<>:" + "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯDFGIJLNQR"
             + "SUVWZ^≤≥∨&⊃~÷≡%|—_!\"Ъ?′")
GOST6[15] = " "  # код 015 — пробел
GOST6 = GOST6[:64]
assert len(GOST6) == 64

# Гомоглифы, которыми gost10859.h подписывает коды (-used в наших комментариях).
GOST_ALIASES = {
    "е": 0o20, "e": 0o20, "@": 0o21, "x": 0o24,
    "A": 0o40, "B": 0o42, "E": 0o45, "H": 0o55, "K": 0o52,
    "M": 0o54, "O": 0o56, "P": 0o57, "C": 0o61, "T": 0o62,
    "Y": 0o63, "X": 0o65, "D": 0o77,
}
_GOST_CODE = {ch: i for i, ch in enumerate(GOST6)}
_GOST_CODE.update(GOST_ALIASES)

WORD = 6
BASE = 0o2100  # сюда кладутся проверяемые слова
PB_WORDS = 0o2000  # одна страница Pascal-B


def t6decode(word: int) -> str:
    """6-битный TEXT (8 символов), как его печатает dtran."""
    return "".join(TEXT[(word >> shift) & 0o77]
                   for shift in (42, 36, 30, 24, 18, 12, 6, 0))


def gost6decode(word: int) -> str:
    """8 шестибитных групп как GOST-10859 — наша вторичная интерпретация."""
    return "".join(GOST6[(word >> shift) & 0o77]
                   for shift in (42, 36, 30, 24, 18, 12, 6, 0))


def parse_word(text: str) -> int:
    t = text.strip()
    if t.lower().startswith("0o"):
        return int(t[2:], 8)
    if t.lower().startswith("0x"):
        return int(t, 16)
    return int(t, 8)


def make_pb(words: list[int]) -> bytes:
    """Синтетический Pascal-B: 02000=UJ 0 (стоп обхода), слова с 02100."""
    mem = [0] * PB_WORDS
    mem[9] = 1                         # memory[02011] = число страниц
    mem[0] = 0o0300000000000000        # UJ 0 / UJ 0
    for i, w in enumerate(words):
        if BASE + i >= 0o4000:
            raise ValueError("слишком много слов для одной страницы")
        mem[0o100 + i] = w & 0xffffffffffff
    mem[-1] = 1                        # total_len не должен схлопнуться
    return b"".join(w.to_bytes(WORD, "big") for w in mem)


CONST_RE = re.compile(r"^\s*/(\d+):,(TEXT|GOST|ISO|ITM),\s*\|(.*?)\|\s*([0-7 ]*)$")


def dtran_decodings(words: list[int], dtran: str,
                    encodings=("text", "gost", "iso", "itm")) -> dict:
    """Прогнать dtran -D для каждой кодировки; вернуть {(enc, word): (str, octets)}."""
    if not words:
        return {}
    out: dict = {}
    with tempfile.TemporaryDirectory(prefix="forex-dtran-text-") as td:
        tmp = Path(td)
        pb = tmp / "probe.pb"
        pb.write_bytes(make_pb(words))
        offsets = ",".join(format(BASE + i, "o") for i in range(len(words)))
        for enc in encodings:
            cmd = tmp / f"{enc}.dtr"
            cmd.write_text(f"{enc}:{offsets}\n", encoding="ascii")
            r = subprocess.run([dtran, "-F", "pb", "-D", str(cmd), str(pb)],
                               capture_output=True, text=True, timeout=120)
            if r.returncode != 0:
                raise RuntimeError(f"dtran -D {enc}: rc={r.returncode}: {r.stderr.strip()}")
            found = 0
            for line in r.stdout.splitlines():
                m = CONST_RE.match(line)
                if not m:
                    continue
                addr = int(m.group(1), 10)   # dtran печатает метки в десятичной системе
                idx = addr - BASE
                if 0 <= idx < len(words):
                    out[(enc, words[idx])] = (m.group(3), m.group(4).strip())
                    found += 1
            if found != len(words):
                raise RuntimeError(f"dtran -D {enc}: найдено {found}/{len(words)} констант")
    return out


DMS_CONST_RE = re.compile(r",(TEXT|GOST|ISO|ITM),\s*(8H.*|6H.*|\|.*?\|.*)$")


def dms_constants(dms: Path, dtran: str) -> list[tuple[str, str]]:
    """Что dtran реально печатает для DMS-модуля (с -D и без — одинаково)."""
    r = subprocess.run([dtran, "-F", "dms", str(dms)],
                       capture_output=True, text=True, timeout=120)
    if r.returncode != 0:
        raise RuntimeError(f"dtran -F dms: rc={r.returncode}: {r.stderr.strip()}")
    return [(m.group(1), m.group(2).strip())
            for line in r.stdout.splitlines() if (m := DMS_CONST_RE.search(line))]


def lib_image(name: str) -> Path:
    """Извлечь объектный образ модуля lib21 во временный .dms."""
    if str(SIPROD_TOOLS) not in sys.path:
        sys.path.insert(0, str(SIPROD_TOOLS))
    import siprod_lib  # noqa: E402
    lib = siprod_lib.Library(str(LIB))
    if name not in lib.objects:
        raise SystemExit(f"нет модуля {name} в {LIB}")
    start, hdr = lib.objects[name]
    sec = lib.sections(name)
    end = sec["debug"] + hdr["debug"]
    path = Path(tempfile.gettempdir()) / f"forex-{name.replace('*', '_')}.dms"
    path.write_bytes(b"".join(w.to_bytes(WORD, "big") for w in lib.words[start:end]))
    return path


# ── Контрольный набор: ключевые 6-битные TEXT-константы аудита ───────────────
# (источник, слово, GOST(6→8, наш), TEXT(наш), ISO(наш))
# dtran печатает их как `,TEXT, 8H...` — это авторитетное чтение для DMS.
MANIFEST: list[tuple[str, int, str, str, str]] = [
    ("FOREX_CORE.mad:365 LO*SYN",   0o5457126371560000, "МП+УЩО00", "LO*SYN  ", "······"),
    ("FOREX_CORE.mad:370 LO*GEN",   0o5457124745560000, "МП+ЗЕО00", "LO*GEN  ", "······"),
    ("FOREX_CORE.mad:390 FOREX*",   0o4657624570120000, "ЖПТЕШ+00", "FOREX*  ", "······"),
    ("FOREX_CORE.mad:520 ENTRY*",   0o4556646271120000, "ЕОФТЩ+00", "ENTRY*  ", "··2···"),
    ("FOREX_CORE.mad:545 DATAPR*",  0o4441644160621200, "ДБФБРТ+0", "DATAPR* ", "··!·\"·"),
    ("FOREX_CORE.mad:550 TAK/PG",   0o6441531760470000, "ФБЛ РЗ00", "TAK/PG  ", "····p·"),
    ("FOREX_CORE.mad:555 GIV/PG",   0o4751661760470000, "ЗЙЦ РЗ00", "GIV/PG  ", "····p·"),
    ("FOREX_CORE.mad:560 OCTTDEC",  0o5743646444454300, "ПГФФДЕГ0", "OCTTDEC ", "·=4·X·"),
    ("FOREX_CORE.mad:565 FOREX",    0o4657624570000000, "ЖПТЕШ000", "FOREX   ", "······"),
    ("FOREX_CORE.mad:570 CONST",    0o4357566364000000, "ГПОУФ000", "CONST   ", "······"),
    ("FOREX_CORE.mad:575 COMEQ",    0o4357554561000000, "ГПНЕС000", "COMEQ   ", "··e···"),
    ("FOREX_CORE.mad:580 OPRTR",    0o5760626462000000, "ПРТФТ000", "OPRTR   ", "······"),
    ("FOREX_CORE.mad:585 LOADANGO", 0o5457414441564757, "МПБДБОЗП", "LOADANGO", "··d···"),
    ("XREF.mad:1053 *INPUT*",       0o1251566065641200, "+ЙОРХФ+0", "*INPUT* ", "*···B·"),
    ("XREF.mad:1054    INPUT",      0o0000005156606564, "000ЙОРХФ", "   INPUT", "··5···"),
    ("XREF.mad:1055 *OUTPUT*",      0o1257656460656412, "+ПХФРХФ+", "*OUTPUT*", "*·t·]·"),
    ("XREF.mad:1056   OUTPUT",      0o0000576564606564, "00ПХФРХФ", "  OUTPUT", "·]0·@·"),
    ("F77LIBR 4HABCD",              0o4142434400000000, "ABCD0000", "ABCD    ", "AB····"),
]

# ── Месяцы DATAPR: это 8-битные GOST-константы (S5:7712-7731), НЕ TEXT ───────
# Слова собраны из 6 байт GOST-10859; dtran -D gost: reading их однозначно.
# Наши вторичные TEXT-строки в комментариях — 6-битная интерпретация байт,
# она не совпадает с dtran TEXT намеренно (см. docs/19).
GOST_MONTHS: list[tuple[str, int, str]] = [
    ("S5:7722 ФЕВМАР", 0o1502244213020060, "ФЕВМАР"),
    ("S5:7723 ДЕК",    0o1102245200000000, "ДЕК"),
    ("S5:7724 ИЮНИЮЛ", 0o1203645512036453, "ИЮНИЮЛ"),
    ("S5:7723 АПРМАЯ", 0o1002746013020076, "АПРМАЯ"),
]


def gost_word(codes: list[int]) -> int:
    """6 GOST-байт -> 48-битное слово."""
    word = 0
    for c in codes:
        word = (word << 8) | c
    return word


def audit(dtran: str) -> int:
    words = [w for _, w, *_ in MANIFEST]
    dec = dtran_decodings(words, dtran, encodings=("text", "gost", "iso"))
    print("МОДУЛЬ                         СЛОВО             КОДИР.  dtran                    НАШЕ")
    print("-" * 108)
    bad = 0
    for src, word, gost, text, iso in MANIFEST:
        dt_text = dec[("text", word)][0]
        dt_gost = dec[("gost", word)][0]
        status = "OK" if dt_text == text else "DIFF"
        if status != "OK":
            bad += 1
        print(f"{src:30s} 0o{word:016o}  TEXT   |{dt_text}|  |{text}| {status}")
        # dtran's byte-GOST is informational only (see module docstring).
        print(f"{'':30s} {'':18s}  GOST   |{dt_gost}|  |{gost}| (6→8)")
    print("-" * 108)
    print(f"проверено TEXT: {len(MANIFEST)}, расхождений: {bad}")
    print("GOST dtran (8-бит) на 6-битных словах ожидаемо не совпадает с GOST(6→8):")
    print("это разные форматы, а не ошибка комментария (см. docs/19-dtran-text-encodings.md).")

    # Месяцы DATAPR — настоящие 8-битные GOST-константы: здесь dtran -D gost:
    # является авторитетным чтением и должен совпадать с нашим GOST.
    gost_words = [w for _, w, _ in GOST_MONTHS]
    gdec = dtran_decodings(gost_words, dtran, encodings=("gost", "text"))
    print()
    print("МЕСЯЦЫ DATAPR (GOST 8 бит/символ, S5:7712-7731):")
    gbad = 0
    for src, word, ours in GOST_MONTHS:
        dt_gost = gdec[("gost", word)][0]
        dt_text = gdec[("text", word)][0]
        ok = dt_gost.rstrip("0") == ours.rstrip(" ")
        if not ok:
            gbad += 1
        print(f"  {src:20s} 0o{word:016o}  -D gost: |{dt_gost}|  наш '{ours}' "
              f"{'OK' if ok else 'DIFF'}   (-D text: |{dt_text}| — неприменимо)")
    print(f"проверено GOST: {len(GOST_MONTHS)}, расхождений: {gbad}")
    return 1 if (bad or gbad) else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dtran", default=DEFAULT_DTRAN)
    ap.add_argument("--word", action="append", default=[], type=parse_word,
                    help="восьмеричное слово (можно повторить)")
    ap.add_argument("--words", type=Path, help="дамп слов (6 байт/слово)")
    ap.add_argument("--offsets", default="", help="смещения слов в дампе (восьмеричные)")
    ap.add_argument("--dms", type=Path, help="DMS-модуль: что печатает dtran")
    ap.add_argument("--module", help="имя модуля в lib21.bin")
    ap.add_argument("--audit", action="store_true", help="сверка контрольного набора")
    args = ap.parse_args()

    if args.audit:
        return audit(args.dtran)

    if args.module:
        args.dms = lib_image(args.module)
    if args.dms:
        print(f"DMS {args.dms}: (dtran -F dms; -D на DMS не влияет)")
        for kind, text in dms_constants(args.dms, args.dtran):
            print(f"  ,{kind}, {text}")
        return 0

    words = list(args.word)
    if args.words:
        data = args.words.read_bytes()
        if len(data) % WORD:
            raise SystemExit("дамп не кратен 6 байтам")
        raw = [int.from_bytes(data[i:i + WORD], "big") for i in range(0, len(data), WORD)]
        if args.offsets:
            for off in args.offsets.replace(",", " ").split():
                idx = int(off, 8)
                if idx >= len(raw):
                    raise SystemExit(f"нет слова {idx:o} в {args.words}")
                words.append(raw[idx])
        else:
            words.extend(raw[:32])
    if not words:
        raise SystemExit("укажите --word / --words / --dms / --module / --audit")

    dec = dtran_decodings(words, args.dtran)
    print("СЛОВО              КОДИР.  dtran                           octets")
    print("-" * 88)
    for w in words:
        for enc in ("text", "gost", "iso", "itm"):
            text, octets = dec.get((enc, w), ("<нет>", ""))
            print(f"0o{w:016o}  {enc:5s}  |{text}|  {octets}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
