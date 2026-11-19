#!/usr/bin/env python3
"""Build a PERSO (личная библиотека Монитора-80 Дубна) image containing the
reconstructed FOREX compiler and its runtime.

The image is a raw sequence of 48-bit BESM words (6 bytes, big-endian),
padded to a whole number of 1024-word zones.  Layout:

    word 0        library header (copied from a real PERSO catalog)
    word 1        reserved (0)
    word 2..      catalog: pairs (name_word, record_word)
    word 2048..   object modules (DMS), each aligned to a 32-word boundary
    zero padding up to the zone boundary

PERSO catalog record (48 bits), reverse-engineered from the real /*PASCAL
library on 2348 (122/123 records matched exactly) and cross-checked against
re-siprod/tools/siprod_lib.py and pascal-re/PERSO.md:

    bits 47..36  f3 = (word offset within zone) + 0o2010  -- transfer vector
    bits 35..24  f2 = (zone within library + 0o40) * 0o100
                      + (load_length // 512)
    bits 23..12  f1 = (load_length % 512) * 8
    bits 11..0   f0 = overlay / entry-point offset

PLCATALOG prints f2/f3 as "zone block length", e.g. "014 07 00056".
A missing/zero transfer vector makes the monitor print
"ИСПОРЧЕНЫ ПОДПРОГРАММЫ" for every module except the first.

Modules with a compiled word dump (FOREX*, LO*SYN, LO*GEN, FORMAT, FORTLIBR)
carry the exact tape words wrapped in a DMS header.  OCTTDEC too now uses a
BYTE-EXACT compiled DMS module extracted from the authoritative monsys.9 tape
(words 0o37100..0o37137, see build/RUNTIME_OCTTDEC_ETALON.words).  The remaining
source-only runtime modules (DATAPR*, GIV/PG + its TAK/PG entry) are assembled
from their authoritative MADLEN sources on the fly with the Monitor-80
`*assembler` through dispak, so all nine catalog entries are genuine, loadable
DMS modules.

WHY OCTTDEC IS CATALOGED AS "OCTTDE*"
-------------------------------------
The fixed MONSYS library on disk 2048 already contains a subprogram named
`OCTTDEC` (loaded at 0o3614 by the FOREX loader).  When the PERSO catalog at
0o2300 *also* lists the exact name `OCTTDEC`, the monitor's name resolution
sees a duplicate and prints `ИСПОРЧЕНА ПОДПРОГРАММА` while loading the compiled
task, truncating the 14 result lines.  This is independent of the module body
and of the catalog record: a byte-exact etalon module and every f0/f1/f2/f3
variant were tested; renaming the catalog entry alone makes the very same
module load cleanly.  The PERSO copy therefore carries the alias `OCTTDE*`
(consistent with `DATAPR*`, `FOREX*`); the program itself keeps using the
system `OCTTDEC` at LINK 0o74013, so the result is bit-identical to the etalon.
The module's internal head-section name is patched to the same alias so that
`siprod_lib.Library` still finds a loadable object for every catalog entry.

Output: build/FOREX_PERSO_2300.bin
"""

from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

WORD_BYTES = 6
ZONE_WORDS = 1024
MODULE_ALIGN = 32

# Dubna TEXT (modified ECMA-1), same table as re-siprod/tools/siprod_lib.py.
TEXT = [
    " ", ".", "Б", "Ц", "Д", "Ф", "Г", "И", "(", ")", "*", "Й",
    "Л", "Я", "Ж", "/", "0", "1", "2", "3", "4", "5", "6", "7",
    "8", "9", "Ь", ",", "П", "-", "+", "Ы", "З", "A", "B", "C",
    "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
    "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "Ш",
    "Э", "Щ", "Ч", "Ю",
]
TEXT_INDEX = {c: i for i, c in enumerate(TEXT)}

# Tape coordinates of the authoritative compiled word dumps (octal input).
TAPE = Path("/home/azizz/Yandex.Disk/besm6-new/besm6.net/tapes/monsys.9")
HEADER_WORD = 0o2105000          # catalog word 0 of the GOSTLIB PERSO library

# Transfer-vector biases (see module docstring).
TV_BIAS_F3 = 0o2010
TV_BIAS_F2 = 0o40 * 0o100

# Assembler environment.
SRC_ROOT = Path("/home/azizz/besm6.github.io/sources/dubna")
ETALON = Path("/usr/local/share/besm6/2348")
DISPAK = "/usr/local/bin/dispak"
SIPROD_LIB = Path.home() / "Yandex.Disk/re-siprod/tools/siprod_lib.py"

# Byte-exact compiled OCTTDEC module (full DMS object, 32 words) from the
# authoritative monsys.9 tape, field 4, words 0o37100..0o37137.
# 3-word header + 15 cmd + 12 const + 1 head(name) + 1 sym.
OCTTDEC_ETALON = ROOT / "build/RUNTIME_OCTTDEC_ETALON.words"
# PERSO catalog alias: the system library on disk 2048 already provides
# OCTTDEC; a duplicate name in the PERSO catalog triggers
# "ИСПОРЧЕНА ПОДПРОГРАММА" when the compiled task is loaded.
OCTTDEC_PERSO_NAME = "OCTTDE*"
OCTTDEC_HEAD_INDEX = 30       # internal name word inside the 32-word module

# (catalog name, source file, first line, last line).  TAK/PG is an ENTRY
# inside GIV/PG and is added separately, not assembled on its own.
SOURCE_SLICES = [
    ("DATAPR*", SRC_ROOT / "besmmons/system1.txt", 7645, 7733),
    ("GIV/PG",  SRC_ROOT / "besml21/libra211.l21", 16780, 16836),
]


def text_encode(name: str) -> int:
    v = 0
    for ch in name.ljust(8)[:8]:
        v = (v << 6) | TEXT_INDEX.get(ch, 0)
    return v


def read_words(path: Path) -> list[int]:
    data = path.read_bytes()
    if len(data) % WORD_BYTES:
        raise ValueError(f"{path}: length {len(data)} is not a multiple of {WORD_BYTES}")
    return [int.from_bytes(data[i:i + WORD_BYTES], "big")
            for i in range(0, len(data), WORD_BYTES)]


def tape_words(start: int, count: int) -> list[int]:
    data = TAPE.read_bytes()
    raw = data[start * WORD_BYTES:(start + count) * WORD_BYTES]
    if len(raw) != count * WORD_BYTES:
        raise ValueError(f"short tape read at 0o{start:o}: {len(raw)} bytes")
    return [int.from_bytes(raw[i:i + WORD_BYTES], "big")
            for i in range(0, len(raw), WORD_BYTES)]


def load_octdec_etalon() -> dict:
    """Load the byte-exact compiled OCTTDEC DMS module from monsys.9.

    The word dump is used verbatim; only the internal head-section name is
    rewritten to the PERSO alias so that catalog and object agree (see the
    module docstring for the name-collision explanation).
    """
    words = read_words(OCTTDEC_ETALON)
    if len(words) != 32:
        raise ValueError(f"OCTTDEC etalon: expected 32 words, got {len(words)}")
    h0, h2 = words[0], words[2]
    if (h0 & 0xFFF) != 1 or ((h2) & 0o77777) != 15 or ((h2 >> 30) & 0o77777) != 12:
        raise ValueError("OCTTDEC etalon: unexpected DMS header")
    if words[OCTTDEC_HEAD_INDEX] != text_encode("OCTTDEC"):
        raise ValueError("OCTTDEC etalon: unexpected internal name")
    words[OCTTDEC_HEAD_INDEX] = text_encode(OCTTDEC_PERSO_NAME)
    load = (h2 & 0o77777) + ((h2 >> 15) & 0o77777) + ((h2 >> 30) & 0o77777)
    print(f"  OCTTDEC etalon : body=32 load={load} (monsys.9 0o37100) "
          f"catalog={OCTTDEC_PERSO_NAME}")
    return dict(name=OCTTDEC_PERSO_NAME, body=words, load=load)


def assemble_source(name: str, path: Path, first: int, last: int) -> tuple[list[int], int, int]:
    """Assemble one MADLEN source with Monitor-80 `*assembler` via dispak.

    Returns (dms_body_words, load_length, entry_offset_for_TAK_PG or 0).
    """
    sys.path.insert(0, str(SIPROD_LIB.parent))
    import siprod_lib  # noqa: WPS433 (optional dependency, checked below)

    tmp = Path(tempfile.mkdtemp(prefix="forex-perso-asm-",
                                dir="/tmp/.private/azizz"))
    try:
        shutil.copy(ETALON, tmp / "2348")
        lines = path.read_text(errors="replace").splitlines()[first - 1:last]
        deck = [
            "шифр 419999 зс5^", "лен 40(2348-wr)^", "eeв1а3",
            "*name", "*call yesmemory", "*assembler",
        ] + lines + ["*to perso:402400", "*end file", "``````", "еконец"]
        (tmp / "asm.b6").write_text("\n".join(deck) + "\n", encoding="utf-8")
        env = dict(os.environ,
                   BESM6_PATH=str(tmp) + ":/usr/local/share/besm6")
        r = subprocess.run([DISPAK, "asm.b6"], cwd=tmp, env=env,
                           capture_output=True, text=True)
        if r.returncode:
            raise RuntimeError(f"dispak failed for {name}: {r.stderr[:400]}")
        libfile = tmp / "lib.bin"
        subprocess.run(
            ["besmtool", "dump", "2348", "--start=1280", "--length=3",
             "--to-file=" + str(libfile)],
            cwd=tmp, env=env, capture_output=True, check=True)
        lib = siprod_lib.Library(str(libfile))
        if name not in lib.objects:
            raise RuntimeError(f"{name}: assembler produced no object "
                               f"(catalog={list(lib.catalog)})")
        s, h = lib.objects[name]
        sec = lib.sections(name)
        body = [lib.words[i] for i in range(s, sec["end"])]
        load = h["cmd"] + h["const"] + h["bss"]
        entry = 0
        if name == "GIV/PG":
            rec = lib.catalog.get("TAK/PG")
            if rec is not None:
                entry = rec & 0xFFF  # entry-point offset inside GIV/PG
        print(f"  assembled {name:8s}: body={len(body)} load={load} "
              f"takepg_entry=0o{entry:o}")
        return body, load, entry
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def build() -> Path:
    compiled = [
        ("FOREX*",   ROOT / "build/CORE_ROOT.words",       0o510300,  96),
        ("LO*SYN",   ROOT / "build/LO_SYN.words",          0o241500, 1024),
        ("LO*GEN",   ROOT / "build/LO_GEN.words",          0o277500, 1024),
        ("FORMAT",   ROOT / "build/RUNTIME_FORMAT.words",  0o510443,  61),
        ("FORTLIBR", ROOT / "build/RUNTIME_FORTLIBR.words", 0o510543,  69),
    ]
    modules: list[dict] = []
    for name, local, tape_start, count in compiled:
        words = read_words(local) if local.exists() else tape_words(tape_start, count)
        if len(words) != count:
            raise ValueError(f"{name}: expected {count} words, got {len(words)}")
        # Wrap raw compiled words in a minimal DMS header: head=1, cmd=N,
        # head-section = module name.
        body = [1, 0, len(words)] + words + [text_encode(name)]
        modules.append(dict(name=name, body=body, load=len(words)))

    takepg_entry = 0
    for name, path, first, last in SOURCE_SLICES:
        body, load, entry = assemble_source(name, path, first, last)
        modules.append(dict(name=name, body=body, load=load))
        if name == "DATAPR*":
            # OCTTDEC is taken from the byte-exact compiled dump, not assembled.
            modules.append(load_octdec_etalon())
        if name == "GIV/PG":
            takepg_entry = entry

    # TAK/PG is an entry point inside GIV/PG: catalog-only record, no body.
    modules.append(dict(name="TAK/PG", body=None, load=takepg_entry,
                        entry_of="GIV/PG"))

    # Place module bodies FIRST: the catalog record needs each module's zone
    # and 32-word block inside the library (the transfer vector).
    # The catalog occupies exactly two zones (2048 words); object modules
    # begin at zone Z+2, each aligned to a 32-word boundary.
    nwords = 2 * ZONE_WORDS
    words_buf = [0] * nwords
    bodies: list[tuple[dict, int, list[int] | None]] = []
    for m in modules:
        if m["body"] is None:
            bodies.append((m, 0, None))  # entry point, no placement
            continue
        start = nwords
        body = m["body"]
        for w in body:
            if not 0 <= w < (1 << 48):
                raise ValueError(f"{m['name']}: word out of 48-bit range")
        if start + len(body) > len(words_buf):
            words_buf.extend([0] * (start + len(body) - len(words_buf)))
        for i, w in enumerate(body):
            words_buf[start + i] = w
        nwords = ((start + len(body) + MODULE_ALIGN - 1) // MODULE_ALIGN) * MODULE_ALIGN
        words_buf.extend([0] * (nwords - len(words_buf)))
        bodies.append((m, start, body))

    # Build the catalog now that every body position is known.
    catalog_words: list[int] = [HEADER_WORD, 0]
    for m, start, _body in bodies:
        if m["body"] is None:
            # Entry point: record is just the offset within the parent module.
            catalog_words.append(text_encode(m["name"]))
            catalog_words.append(m["load"] & 0xFFF)
            continue
        zone, off = divmod(start, ZONE_WORDS)
        f3 = (off + TV_BIAS_F3) & 0xFFF
        length = m["load"]
        f2 = (TV_BIAS_F2 + zone * 0o100 + (length // 512)) & 0xFFF
        f1 = ((length % 512) * 8) & 0xFFF
        record = (f3 << 36) | (f2 << 24) | (f1 << 12)  # overlay = 0
        catalog_words.append(text_encode(m["name"]))
        catalog_words.append(record)
    # Real catalogs terminate with an empty name word followed by an all-ones
    # word (verified on GOSTLIB and /*PASCAL catalogs).
    catalog_words.append(0)
    catalog_words.append((1 << 48) - 1)
    if len(catalog_words) > 2 * ZONE_WORDS:
        raise ValueError("catalog overflowed its two zones")
    words_buf[0:len(catalog_words)] = catalog_words

    # Pad to whole zones.
    total = ((nwords + ZONE_WORDS - 1) // ZONE_WORDS) * ZONE_WORDS
    words_buf.extend([0] * (total - len(words_buf)))
    image = b"".join(w.to_bytes(WORD_BYTES, "big") for w in words_buf)

    out = ROOT / "build/FOREX_PERSO_2300.bin"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(image)

    digest = hashlib.sha256(image).hexdigest()
    print(f"image      : {out}")
    print(f"words      : {len(words_buf)} ({total // ZONE_WORDS} zones of {ZONE_WORDS} words)")
    print(f"bytes      : {len(image)}")
    print(f"sha256     : {digest}")
    print("catalog    :")
    for m, start, body in bodies:
        if body is None:
            print(f"  {m['name']:10s} ENTRY of {m['entry_of']} at 0o{m['load']:o}")
        else:
            print(f"  {m['name']:10s} load={m['load']:5d} body={len(body):4d} "
                  f"word={start:5d} (0o{start:o})")
    return out


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.parse_args()
    build()


if __name__ == "__main__":
    main()
