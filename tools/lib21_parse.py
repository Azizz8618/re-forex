#!/usr/bin/env python3
"""Полный разбор библиотеки 21 (DMS, Мониторная система Дубна).

Источник (только для чтения):
    /home/azizz/Yandex.Disk/besm6-new/DUBNA/BUILD/elements/lib21.bin
    1 271 808 байт = 211 968 слов по 6 байт big-endian = 207 зон по 1024 слова.

Структура образа:

    слова  0..1      служебное слово и ноль
    слова  2..1203   каталог: 601 запись по 2 слова (имя 8x6 бит + запись)
    слова  1204..    нулевое слово и маркер 0o7777777777777777
    слова  2016..    объектные модули, каждый начинается на границе 32 слов
    слова  163840..  точная копия слов 0..48127 (повтор хвоста носителя)

Заголовок DMS (распакованный, 3 слова, 15-битные поля + зарезервированные биты):

    S+0  bits  0..11  head_len    bits 12..23 sym_len
         bits 24..35  резерв      bits 36..47 debug_len
    S+1  bits  0..14  set_len     bits 15..29 data_len
         bits 30..44  long_len    bits 45..47 резерв
    S+2  bits  0..14  cmd_len     bits 15..29 bss_len
         bits 30..44  const_len   bits 45..47 резерв

Порядок разделов: cmd, const, data, set, head, sym, long, debug, comment.
Длина раздела comment в заголовке не хранится; она вычисляется как зазор
до начала следующего модуля.

Запись каталога (48 бит):

    bits  0..14  ссылка (индекс каталога) для псевдонима; 0 для объекта
    bits 15..29  длина модуля = cmd + const + bss (в словах)
    bits 30..44  адрес/связь DMS: (row << 11) | (0o1040 + zone)
    bits 45..47  тип: 2 или 3 для объекта, 0 для псевдонима

Использование:
    tools/lib21_parse.py                       # каталог + все модули
    tools/lib21_parse.py --module FOREX*       # один модуль подробно
    tools/lib21_parse.py --check               # проверки целостности
    tools/lib21_parse.py --stats               # статистика
    tools/lib21_parse.py --json                # весь разбор в JSON
    tools/lib21_parse.py --csv docs/lib21/modules.csv
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

DEFAULT_LIB = Path("/home/azizz/Yandex.Disk/besm6-new/DUBNA/BUILD/elements/lib21.bin")
WORD_BYTES = 6
ZONE_WORDS = 1024
MODULE_ALIGN = 32

TEXT = [
    " ", ".", "Б", "Ц", "Д", "Ф", "Г", "И", "(", ")", "*", "Й",
    "Л", "Я", "Ж", "/", "0", "1", "2", "3", "4", "5", "6", "7",
    "8", "9", "Ь", ",", "П", "-", "+", "Ы", "З", "A", "B", "C",
    "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
    "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "Ш",
    "Э", "Щ", "Ч", "Ю",
]

SECTIONS = ("cmd", "const", "data", "set", "head", "sym", "long", "debug")


def text_decode(word: int) -> str:
    """Слово -> 8 символов кодировки TEXT (8 x 6 бит)."""
    return "".join(TEXT[(word >> (42 - 6 * i)) & 0x3F] for i in range(8))


def field(word: int, lo: int, hi: int) -> int:
    return (word >> lo) & ((1 << (hi - lo)) - 1)


class Lib21:
    """Образ библиотеки 21: слова, каталог, объекты, псевдонимы."""

    def __init__(self, path: Path):
        self.path = Path(path)
        self.data = self.path.read_bytes()
        self.nwords = len(self.data) // WORD_BYTES
        self.words = [
            int.from_bytes(self.data[i * WORD_BYTES:(i + 1) * WORD_BYTES], "big")
            for i in range(self.nwords)
        ]
        self.sha256 = hashlib.sha256(self.data).hexdigest()
        self.period = self._detect_period()
        self.unique_words = self.period or self.nwords
        self.catalog = self._read_catalog()
        self.objects = self._find_objects()
        self._next_start = self._build_next_start()

    # --- общая структура ----------------------------------------------------
    def _detect_period(self) -> int | None:
        """Найти период повтора хвоста: W[i] == W[i+p] для всех i < N-p."""
        for p in range(ZONE_WORDS, self.nwords - ZONE_WORDS + 1, ZONE_WORDS):
            n = self.nwords - p
            if n < ZONE_WORDS:
                break
            step = max(1, n // 64)
            if all(self.words[i] == self.words[i + p] for i in range(0, n, step)):
                if all(self.words[i] == self.words[i + p] for i in range(n)):
                    return p
        return None

    # --- каталог ------------------------------------------------------------
    def _read_catalog(self) -> list[dict]:
        cat = []
        i = 2
        while i + 1 < self.nwords:
            name = text_decode(self.words[i]).rstrip()
            if not name or not all(c.isalnum() or c in "/*" for c in name):
                break
            rec = self.words[i + 1]
            cat.append(dict(
                index=len(cat), word=i, name=name, rec=rec,
                link=field(rec, 0, 15),
                length=field(rec, 15, 30),
                addr=field(rec, 30, 45),
                attr=field(rec, 45, 48),
            ))
            i += 2
        return cat

    def catalog_by_name(self, name: str) -> dict | None:
        for e in self.catalog:
            if e["name"] == name:
                return e
        return None

    # --- объектные модули ---------------------------------------------------
    @staticmethod
    def _header(words: list[int], s: int) -> dict:
        w0, w1, w2 = words[s], words[s + 1], words[s + 2]
        return dict(
            head=field(w0, 0, 12), sym=field(w0, 12, 24), debug=field(w0, 36, 48),
            set_=field(w1, 0, 15), data=field(w1, 15, 30), long=field(w1, 30, 45),
            cmd=field(w2, 0, 15), bss=field(w2, 15, 30), const=field(w2, 30, 45),
        )

    def _find_objects(self) -> dict[str, dict]:
        names = {e["name"] for e in self.catalog}
        cands = []
        for s in range(MODULE_ALIGN, self.unique_words - 3, MODULE_ALIGN):
            h = self._header(self.words, s)
            if h["head"] != 1:
                continue
            toff = s + 3 + h["cmd"] + h["const"] + h["data"] + h["set_"]
            if toff >= self.unique_words:
                continue
            name = text_decode(self.words[toff]).rstrip()
            if name not in names:
                continue
            cands.append((s, name, h))

        objects = {}
        limit = 0
        for s, name, h in cands:
            if s < limit or name in objects:
                continue
            sec = self._section_offsets(s, h)
            objects[name] = dict(offset=s, header=h, sections=sec, end=sec["comment"])
            limit = sec["comment"]
        return objects

    @staticmethod
    def _section_offsets(s: int, h: dict) -> dict:
        # ключ заголовка 'set_' соответствует разделу 'set'
        keys = ("cmd", "const", "data", "set_", "head", "sym", "long", "debug")
        names = ("cmd", "const", "data", "set", "head", "sym", "long", "debug")
        p = s + 3
        out = {"header": s, "cmd": p}
        for key, name in zip(keys, names):
            p += h[key]
            out[name + "_end"] = p
            if name != "debug":
                out[names[names.index(name) + 1]] = p
        out["comment"] = p
        out["end"] = p
        return out

    def _build_next_start(self) -> dict[str, int | None]:
        rows = sorted((v["offset"], k) for k, v in self.objects.items())
        out = {}
        for i, (s, name) in enumerate(rows):
            out[name] = rows[i + 1][0] if i + 1 < len(rows) else None
        return out

    def sections(self, name: str) -> dict:
        return self.objects[name]["sections"]

    # --- псевдонимы ---------------------------------------------------------
    def aliases(self) -> list[dict]:
        out = []
        for e in self.catalog:
            if e["name"] in self.objects:
                continue
            target, chain, resolved = e["index"], [], False
            seen = set()
            while target in range(len(self.catalog)) and target not in seen:
                seen.add(target)
                te = self.catalog[target]
                chain.append(te["name"])
                if te["name"] in self.objects:
                    resolved = True
                    break
                if te["attr"] != 0:
                    break
                target = te["link"]
            out.append(dict(name=e["name"], index=e["index"], link=e["link"],
                            attr=e["attr"], chain=chain, resolved=resolved))
        return out

    # --- проверки -----------------------------------------------------------
    def check(self) -> list[str]:
        problems = []
        for name, obj in self.objects.items():
            s, h, sec = obj["offset"], obj["header"], obj["sections"]
            if h["head"] != 1:
                problems.append(f"{name}: head={h['head']} != 1")
            w0, w1, w2 = self.words[s:s + 3]
            if field(w0, 24, 36) or field(w1, 45, 48) or field(w2, 45, 48):
                problems.append(f"{name}: ненулевой резерв в заголовке")
            ce = self.catalog_by_name(name)
            if ce is None:
                problems.append(f"{name}: нет записи в каталоге")
            elif ce["length"] != h["cmd"] + h["const"] + h["bss"]:
                problems.append(
                    f"{name}: длина каталога {ce['length']} != "
                    f"cmd+const+bss {h['cmd'] + h['const'] + h['bss']}")
            nxt = self._next_start[name]
            if nxt is not None and sec["comment"] > nxt:
                problems.append(f"{name}: конец {sec['comment']} > начало следующего {nxt}")
        for a in self.aliases():
            if a["attr"] == 0 and not a["resolved"]:
                problems.append(f"псевдоним {a['name']}: цепочка не ведёт к объекту")
        return problems

    def anomalies(self) -> list[str]:
        """Не фатальные отклонения: каталожные записи без объекта."""
        out = []
        for a in self.aliases():
            if a["attr"] != 0:
                out.append(f"{a['name']}: запись cat[{a['index']}] имеет тип {a['attr']}, "
                           f"но объект не найден")
        return out

    # --- статистика ---------------------------------------------------------
    def stats(self) -> dict:
        hs = [v["header"] for v in self.objects.values()]
        binned = {}
        bins = ((0, 0, "0"), (1, 9, "1-9"), (10, 49, "10-49"),
                (50, 99, "50-99"), (100, 199, "100-199"), (200, 10 ** 9, "200+"))
        for key in ("cmd", "const", "bss"):
            c = Counter()
            for h in hs:
                for lo, hi, label in bins:
                    if lo <= h[key] <= hi:
                        c[label] += 1
                        break
            binned[key] = dict(c)
        largest = sorted(
            ((n, v["header"]["cmd"] + v["header"]["const"] + v["header"]["bss"])
             for n, v in self.objects.items()), key=lambda x: -x[1])[:15]
        return dict(
            nwords=self.nwords, zones=self.nwords // ZONE_WORDS,
            catalog_entries=len(self.catalog), objects=len(self.objects),
            aliases=len(self.catalog) - len(self.objects),
            duplicate_tail=(self.nwords - self.period, self.period)
            if self.period else None,
            totals={k: sum(h[k] for h in hs) for k in ("cmd", "const", "bss", "sym", "long", "debug")},
            nonzero={"cmd": sum(1 for h in hs if h["cmd"] > 0),
                     "const": sum(1 for h in hs if h["const"] > 0),
                     "bss": sum(1 for h in hs if h["bss"] > 0),
                     "data": sum(1 for h in hs if h["data"] > 0),
                     "set": sum(1 for h in hs if h["set_"] > 0),
                     "head": sum(1 for h in hs if h["head"] > 0),
                     "sym": sum(1 for h in hs if h["sym"] > 0),
                     "long": sum(1 for h in hs if h["long"] > 0),
                     "debug": sum(1 for h in hs if h["debug"] > 0)},
            distribution=binned,
            largest=largest,
            data_only=sorted(n for n, v in self.objects.items() if v["header"]["cmd"] == 0),
            attr=Counter(self.catalog_by_name(n)["attr"] for n in self.objects),
            service_names=sum(1 for n in self.objects if n.startswith("Ь")),
            service_catalog=sum(1 for e in self.catalog if e["name"].startswith("Ь")),
            debug_modules=sorted(n for n, v in self.objects.items() if v["header"]["debug"] > 0),
        )


# --- печать -----------------------------------------------------------------
def print_catalog(lib: Lib21) -> None:
    print(f"\nКАТАЛОГ ({len(lib.catalog)} записей, слова 2..{2 + 2 * len(lib.catalog) - 1})")
    print("  #    имя         запись (восьмеричное)    ссылка  длина  адрес   тип  объект/цепочка")
    for e in lib.catalog:
        if e["name"] in lib.objects:
            kind = f"объект @{lib.objects[e['name']]['offset']}"
        elif e["attr"] == 0:
            a = next((x for x in lib.aliases_cache if x["index"] == e["index"]), None)
            kind = " -> ".join(a["chain"]) if a else "псевдоним"
        else:
            kind = "?"
        print(f"  {e['index']:4d} {e['name']:11s} 0o{e['rec']:016o} "
              f"{e['link']:6d} {e['length']:6d} 0o{e['addr']:06o} "
              f"{e['attr']:3d}  {kind}")


def print_modules(lib: Lib21) -> None:
    print(f"\nОБЪЕКТНЫЕ МОДУЛИ ({len(lib.objects)})")
    hdr = "  имя          hdr@    " + "  ".join(f"{k:>13s}" for k in ("cmd", "const", "data", "set")) \
        + "  " + "  ".join(f"{k:>13s}" for k in ("head", "sym", "long", "debug", "comment"))
    print(hdr)
    for name, obj in sorted(lib.objects.items(), key=lambda kv: kv[1]["offset"]):
        h, sec = obj["header"], obj["sections"]
        cells = "  ".join(f"{sec[k]:5d}+{h['cmd' if k == 'cmd' else 'const' if k == 'const' else 'data' if k == 'data' else 'set_' if k == 'set' else k]:<6d}"
                          for k in ("cmd", "const", "data", "set", "head", "sym", "long", "debug"))
        gap = (lib._next_start[name] or lib.unique_words) - sec["comment"]
        print(f"  {name:11s} {obj['offset']:6d}  {cells}  {sec['comment']:5d}+{gap:<6d}")


def print_module_detail(lib: Lib21, name: str) -> None:
    if name not in lib.objects:
        print(f"модуль {name!r} не найден", file=sys.stderr)
        known = [n for n in lib.objects if name.lower() in n.lower()]
        if known:
            print("похожие: " + ", ".join(known[:20]), file=sys.stderr)
        return
    obj = lib.objects[name]
    s, h, sec = obj["offset"], obj["header"], obj["sections"]
    ce = lib.catalog_by_name(name)
    print(f"МОДУЛЬ {name}")
    print(f"  смещение: {s} (0o{s:06o}), зона {s // ZONE_WORDS}, слово в зоне {s % ZONE_WORDS}")
    print(f"  каталог: индекс {ce['index']}, запись 0o{ce['rec']:016o}, "
          f"длина {ce['length']}, адрес 0o{ce['addr']:06o}, тип {ce['attr']}")
    print("  заголовок (распакованные поля):")
    w0, w1, w2 = lib.words[s:s + 3]
    print(f"    S+0 0o{w0:016o}: head={h['head']} sym={h['sym']} "
          f"резерв={field(w0, 24, 36)} debug={h['debug']}")
    print(f"    S+1 0o{w1:016o}: set={h['set_']} data={h['data']} "
          f"long={h['long']} резерв={field(w1, 45, 48)}")
    print(f"    S+2 0o{w2:016o}: cmd={h['cmd']} bss={h['bss']} "
          f"const={h['const']} резерв={field(w2, 45, 48)}")
    print("  разделы (смещение + длина в словах):")
    for k in ("cmd", "const", "data", "set", "head", "sym", "long", "debug", "comment"):
        length = (h["set_"] if k == "set" else h[k]) if k != "comment" else (
            (lib._next_start[name] or lib.unique_words) - sec["comment"])
        print(f"    {k:8s} @{sec[k]:6d} +{length:<5d} .. {sec[k] + length:6d}")
    print(f"  длина по каталогу (cmd+const+bss): "
          f"{h['cmd'] + h['const'] + h['bss']}")
    print(f"  первые слова cmd: " + " ".join(
        f"0o{w:016o}" for w in lib.words[sec["cmd"]:sec["cmd"] + 8]))


def print_stats(lib: Lib21) -> None:
    st = lib.stats()
    print("\nСТАТИСТИКА")
    print(f"  слов в образе: {st['nwords']} ({st['zones']} зон)")
    print(f"  каталог: {st['catalog_entries']} записей")
    print(f"  объектов: {st['objects']}; псевдонимов: {st['aliases']}")
    if st["duplicate_tail"]:
        n, p = st["duplicate_tail"]
        print(f"  повтор хвоста: {n} слов = копия слов 0..{n - 1}")
    print(f"  суммарные длины: {st['totals']}")
    print(f"  модули с секцией > 0: {st['nonzero']}")
    for key in ("cmd", "const", "bss"):
        print(f"  распределение {key:5s}: {st['distribution'][key]}")
    print("  крупнейшие модули (cmd+const+bss):")
    for name, val in st["largest"]:
        print(f"    {name:12s} {val:5d}")
    print(f"  модули с cmd=0 ({len(st['data_only'])}): "
          + ", ".join(st["data_only"]))
    print(f"  модули с debug>0 ({len(st['debug_modules'])}): "
          + ", ".join(st["debug_modules"]))
    print(f"  тип catalog=2/3: {dict(st['attr'])}")
    print(f"  имён с Ь: каталог {st['service_catalog']}, объекты {st['service_names']} "
          f"({100 * st['service_names'] / st['objects']:.1f}%)")


def to_json(lib: Lib21) -> dict:
    return dict(
        source=str(lib.path), sha256=lib.sha256,
        nwords=lib.nwords, zones=lib.nwords // ZONE_WORDS,
        period=lib.period, unique_words=lib.unique_words,
        catalog=[dict(e) for e in lib.catalog],
        objects={
            name: dict(offset=v["offset"], header=v["header"],
                       sections=v["sections"], end=v["end"],
                       next_start=lib._next_start[name])
            for name, v in lib.objects.items()
        },
        aliases=lib.aliases(),
        stats=lib.stats(),
        check=lib.check(), anomalies=lib.anomalies(),
    )


def write_csv(lib: Lib21, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(("name", "offset", "cmd", "const", "bss", "sym", "long", "debug"))
        for name in sorted(lib.objects):
            h = lib.objects[name]["header"]
            w.writerow((name, lib.objects[name]["offset"], h["cmd"], h["const"],
                        h["bss"], h["sym"], h["long"], h["debug"]))


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--path", type=Path, default=DEFAULT_LIB, help="образ библиотеки")
    p.add_argument("--module", metavar="ИМЯ", help="подробный разбор одного модуля")
    p.add_argument("--json", action="store_true", help="весь разбор в JSON")
    p.add_argument("--check", action="store_true", help="проверки целостности")
    p.add_argument("--stats", action="store_true", help="статистика")
    p.add_argument("--csv", type=Path, metavar="ПУТЬ", help="записать список модулей в CSV")
    p.add_argument("--no-catalog", action="store_true", help="не печатать каталог")
    p.add_argument("--no-modules", action="store_true", help="не печатать модули")
    args = p.parse_args()

    lib = Lib21(args.path)
    lib.aliases_cache = lib.aliases()  # for print_catalog

    if args.json:
        json.dump(to_json(lib), sys.stdout, ensure_ascii=False, indent=2,
                  default=lambda o: dict(o) if isinstance(o, Counter) else str(o))
        print()
        return
    if args.module:
        print_module_detail(lib, args.module)
        return

    print(f"БИБЛИОТЕКА 21: {lib.path}")
    print(f"  размер: {len(lib.data)} байт = {lib.nwords} слов = "
          f"{lib.nwords // ZONE_WORDS} зон")
    print(f"  sha256: {lib.sha256}")
    print(f"  каталог: {len(lib.catalog)} записей; объектов: {len(lib.objects)}; "
          f"псевдонимов: {len(lib.catalog) - len(lib.objects)}")
    if lib.period:
        print(f"  хвост: слова {lib.period}..{lib.nwords - 1} — точная копия "
              f"слов 0..{lib.nwords - lib.period - 1}")
    if args.stats:
        print_stats(lib)
    if args.check:
        problems = lib.check()
        print(f"\nПРОВЕРКА: {'OK' if not problems else 'ОШИБКИ'}")
        if problems:
            for msg in problems[:50]:
                print("  ! " + msg)
            if len(problems) > 50:
                print(f"  ... и ещё {len(problems) - 50}")
        else:
            print("  длина каталога = cmd+const+bss у всех модулей")
            print("  разделы каждого модуля укладываются до следующего модуля")
            print("  резервные биты заголовков нулевые")
            print("  все псевдонимы разрешаются в объекты")
        for msg in lib.anomalies():
            print("  ~ " + msg)
    if not args.no_catalog:
        print_catalog(lib)
    if not args.no_modules:
        print_modules(lib)
    if args.csv:
        write_csv(lib, args.csv)
        print(f"\nCSV записан: {args.csv} ({len(lib.objects)} строк)")


if __name__ == "__main__":
    main()
