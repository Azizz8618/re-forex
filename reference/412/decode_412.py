#!/usr/bin/env python3
"""M0/M1: decoder and comparator for FOREX 4.12 body in disk 2148 zone 0o1550.

Reads z1550_200z.bin (besmtool dump 2148 --start=01550 --length=200).
Words are 6 bytes big-endian; zone = 1024 words.
No repo files are modified.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = "/home/azizz/Yandex.Disk/re-forex"

TEXT = [" ", ".", "Б", "Ц", "Д", "Ф", "Г", "И", "(", ")", "*", "Й",
        "Л", "Я", "Ж", "/", "0", "1", "2", "3", "4", "5", "6", "7",
        "8", "9", "Ь", ",", "П", "-", "+", "Ы", "З", "A", "B", "C",
        "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
        "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "Ш",
        "Э", "Щ", "Ч", "Ю"]


def td(w):
    return "".join(TEXT[(w >> (42 - 6 * i)) & 0x3F] for i in range(8))


def words_of(path):
    data = open(path, "rb").read()
    return [int.from_bytes(data[i:i + 6], "big") for i in range(0, len(data) - 5, 6)]


def g12(w):
    return [(w >> (36 - 12 * i)) & 0xFFF for i in range(4)]


def main():
    body = open(os.path.join(HERE, "z1550_200z.bin"), "rb").read()
    Bw = words_of(os.path.join(HERE, "z1550_200z.bin"))

    # --- M0: table at zone 0o1550 ---
    table = {}
    for i in range(0, 16, 2):
        name = td(Bw[i]).rstrip()
        table[name] = dict(word=i, name_word=oct(Bw[i]),
                           descriptor=oct(Bw[i + 1]),
                           fields12=[oct(x) for x in g12(Bw[i + 1])])
    print("=== TABLE zone 0o1550 ===")
    print(json.dumps(table, ensure_ascii=False, indent=2))

    # --- body extent ---
    lastz = max(z for z in range(len(Bw) // 1024)
                if any(Bw[z * 1024:(z + 1) * 1024]))
    print(f"\n=== BODY EXTENT: zones 0o1550..0o{0o1550 + lastz:04o} "
          f"({lastz + 1} zones) ===")

    # --- module headers found ---
    mods = {}
    for i, w in enumerate(Bw[:-1]):
        if w in (0o160043, 0o200022, 0o200024):
            mods[td(Bw[i + 1]).rstrip()] = dict(header_word=i, hdr=oct(w),
                                                 name=td(Bw[i + 1]).rstrip())
    print("\n=== MODULE HEADERS ===")
    print(json.dumps(mods, ensure_ascii=False, indent=2))

    # --- extract module regions (as-is from disk) ---
    regions = {
        "forex3_root": (1024, 3136),   # header@1024 .. LO*SYN header
        "lo_syn":      (3136, 18496),  # header@3136 .. LO*GEN header
        "lo_gen":      (18496, 123 * 1024),  # header@18496 .. end-1
    }
    for name, (a, b) in regions.items():
        out = os.path.join(HERE, f"disk412_{name}.words")
        with open(out, "wb") as f:
            for w in Bw[a:b]:
                f.write(w.to_bytes(6, "big"))
        print(f"wrote {out}: words {a}..{b-1} ({b-a} words)")

    # --- M1: compare with our reconstructions ---
    ours = {
        "CORE_ROOT": (os.path.join(REPO, "build/CORE_ROOT.words"), 0, 1030, CR := None),
        "LO_SYN": (os.path.join(REPO, "build/LO_SYN.words"), 23, 3229, None),
        "LO_GEN": (os.path.join(REPO, "build/LO_GEN.words"), 23, 18520, None),
    }
    print("\n=== M1 COMPARISON ===")
    result = {}
    for name, (path, skip, diskstart, _) in ours.items():
        W = words_of(path)
        sub = W[skip:]
        eq = sum(1 for k in range(len(sub))
                 if diskstart + k < len(Bw) and sub[k] == Bw[diskstart + k])
        diffs = [(k, oct(sub[k]), oct(Bw[diskstart + k]))
                 for k in range(min(8, len(sub)))
                 if sub[k] != Bw[diskstart + k]]
        result[name] = dict(file_words=len(W), code_words=len(sub),
                            disk_code_start=diskstart, equal=eq,
                            pct=round(100.0 * eq / len(sub), 1),
                            first_diffs=diffs)
        print(f"  {name}: {eq}/{len(sub)} ({result[name]['pct']}%) equal "
              f"vs disk words {diskstart}..{diskstart+len(sub)-1}")
        for d in diffs[:4]:
            print(f"    idx {d[0]}: our={d[1]} disk={d[2]}")

    with open(os.path.join(HERE, "comparison.json"), "w") as f:
        json.dump({"table": table, "body_extent_zones": lastz + 1,
                   "modules": mods, "comparison": result},
                  f, ensure_ascii=False, indent=2)
    print("\nwrote comparison.json")


if __name__ == "__main__":
    main()
