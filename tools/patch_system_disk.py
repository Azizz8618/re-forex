#!/usr/bin/env python3
"""Безопасный патч системного диска 2348 (БЭСМ-6 / ДИСПАК) и побайтовая регрессия.

Поддерживаемый физический формат диска (simh/dispak "new format", dispak/disk.h):

    зона = 8 служебных слов (uint64) + 1024 информационных слова (uint64)
         = 1032 * 8 = 8256 байт
    слово = uint64 native-endian (на x86 little-endian):
              рр. 0..47  — 48-битное машинное слово БЭСМ-6
              р.  48     — признак свёртки (convolution)
              рр. 49..63 — служебные/зарезервированные
    логическая зона L отображается в физическую L + ZONE_OFFSET (=4),
    т.е. смещение файла = (L + 4) * 8256 байт.

Патч задаётся списком записей:

    {"zone": "0o7000", "word": "0o1777", "old": "0", "new": "0o1234567"}

  zone  — логический номер зоны (как в besmtool / 0o2300); см. --zone-mode=physical
  word  — номер информационного слова 0..1023
  old   — ОБЯЗАТЕЛЬНО ожидаемое 48-битное значение слова (проверка перед записью)
  new   — новое 48-битное значение слова

Числа: int = десятичное; строка "0o.."/"0x.."/"0b.." = восьмеричное/шестнадцатерич-
ное/двоичное; строка из цифр = десятичное. Для зон репозиторий использует
восьмеричную нотацию (0o2300), поэтому в патчах рекомендуется писать "0o...".

При записи сохраняются старшие биты физического слова (свёртка и т.д.) — меняются
только младшие 48 бит. Служебные слова зоны (контрольная сумма) по умолчанию НЕ
пересчитываются; для этого есть флаг --fix-checksum.

Команды:
    snapshot <disk> <out.json>                        — зафиксировать эталон (sha256)
    apply <disk> <patch.json> <out-disk> [opts]       — применить патч на копию, атомарно
    verify <disk> <snapshot.json> [reference-disk]    — побайтовая сверка,.show changed

Ключевые правила безопасности:
  * apply НИКОГДА не пишет в исходный <disk> — только в новый <out-disk>;
  * запись идёт через временный файл + fsync + os.replace (атомарно);
  * несовпадение любого `old` прерывает операцию без создания выходного файла;
  * после apply хэш исходного диска проверяется повторно (он не должен измениться).
"""

import argparse
import hashlib
import json
import os
import re
import struct
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

TOOL_NAME = "patch_system_disk"
TOOL_VERSION = 1

WORD_BYTES = 8          # физическое слово: uint64 (8 байт)
DATA_WORDS = 1024       # информационных слов в зоне
CWORDS = 8              # служебных слов в зоне
HDR_BYTES = CWORDS * WORD_BYTES   # 64
ZONE_BYTES = HDR_BYTES + DATA_WORDS * WORD_BYTES  # 8256
ZONE_OFFSET = 4         # логическая зона L -> физическая L+4
MASK48 = (1 << 48) - 1

_NUM_RE = re.compile(r"^[0-9]+$")


# ----------------------------------------------------------------------------- helpers
def parse_num(value, what="число"):
    """int -> как есть; '0o..'/'0x..'/'0b..' -> с префиксом; голые цифры -> decimal."""
    if isinstance(value, bool):
        raise ValueError(f"{what}: булево значение недопустимо")
    if isinstance(value, int):
        n = value
    elif isinstance(value, str):
        s = value.strip().replace("_", "")
        if s.lower().startswith("0o"):
            n = int(s[2:], 8)
        elif s.lower().startswith("0x"):
            n = int(s[2:], 16)
        elif s.lower().startswith("0b"):
            n = int(s[2:], 2)
        elif _NUM_RE.match(s):
            n = int(s, 10)
        else:
            raise ValueError(f"{what}: не удалось разобрать число {value!r}")
    else:
        raise ValueError(f"{what}: ожидалось int или строка, получено {type(value).__name__}")
    if n < 0:
        raise ValueError(f"{what}: отрицательное значение {n}")
    return n


def fmt_num(n):
    """Читаемый вывод: 0o.. для чисел, удобных в восьмеричной нотации."""
    return f"{n} (0o{n:o}, 0x{n:x})"


def utc_now():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_all(path, label="disk"):
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"{label}: нет файла {p}")
    return p.read_bytes()


def check_size(data, disk):
    if len(data) % ZONE_BYTES != 0:
        raise ValueError(
            f"{disk}: размер {len(data)} не кратен размеру зоны {ZONE_BYTES} "
            f"(возможно, это диск старого формата с 6144 байт/зона)"
        )
    return len(data) // ZONE_BYTES


def zone_slice(data, phys):
    return data[phys * ZONE_BYTES:(phys + 1) * ZONE_BYTES]


def word_offset(phys, word, cword=False):
    if cword:
        return phys * ZONE_BYTES + word * WORD_BYTES
    return phys * ZONE_BYTES + HDR_BYTES + word * WORD_BYTES


def read_word_u64(data, phys, word, cword=False):
    off = word_offset(phys, word, cword)
    return struct.unpack_from("<Q", data, off)[0]


def write_word_u64(data, phys, word, u64, cword=False):
    off = word_offset(phys, word, cword)
    struct.pack_into("<Q", data, off, u64)


def set_word48(data, phys, word, value48):
    """Заменить младшие 48 бит слова, сохранив старшие (свёртку и т.д.)."""
    cur = read_word_u64(data, phys, word)
    new = (cur & ~MASK48) | (value48 & MASK48)
    write_word_u64(data, phys, word, new)
    return cur & MASK48, new & MASK48


def recompute_checksum(data, phys):
    """Пересчёт cwords[3]/cwords[7] по алгоритму dispak/disk.c:disk_writei2."""
    csum = 0
    for w in range(DATA_WORDS):
        csum += read_word_u64(data, phys, w) & MASK48
        csum = (csum & MASK48) + (csum >> 48)
    for idx in (3, 7):
        cur = read_word_u64(data, phys, idx, cword=True)
        write_word_u64(data, phys, idx, (cur & ~MASK48) | (csum & MASK48), cword=True)
    return csum & MASK48


def zone_label(phys):
    logical = phys - ZONE_OFFSET
    if logical >= 0:
        return f"0o{logical:o} (phys 0o{phys:o})"
    return f"phys 0o{phys:o} (logical {logical})"


# ----------------------------------------------------------------------------- snapshot
def cmd_snapshot(args):
    disk = Path(args.disk)
    data = read_all(disk, "disk")
    nzones = check_size(data, disk)
    file_sha = sha256_bytes(data)

    zones = {}
    for phys in range(nzones):
        zones[str(phys)] = sha256_bytes(zone_slice(data, phys))

    snap = {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "created_utc": utc_now(),
        "disk_path": str(disk.resolve()),
        "disk_name": disk.name,
        "size_bytes": len(data),
        "file_sha256": file_sha,
        "format": {
            "zone_bytes": ZONE_BYTES,
            "word_bytes": WORD_BYTES,
            "zone_offset": ZONE_OFFSET,
            "cwords": CWORDS,
            "data_words": DATA_WORDS,
            "zones_physical": nzones,
            "zone_keys": "physical zone number (decimal string); logical = physical - 4",
        },
        "hash": "sha256 of each physical zone (all 8256 bytes, incl. 8 cwords)",
        "zones": zones,
    }
    out = Path(args.out_json)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        json.dump(snap, f, ensure_ascii=False, indent=1)
        f.write("\n")

    print(f"snapshot: {disk}")
    print(f"  size_bytes    : {len(data)}")
    print(f"  zones physical: {nzones}  (logical 0..{nzones - ZONE_OFFSET - 1})")
    print(f"  file sha256   : {file_sha}")
    print(f"  записано      : {out} ({out.stat().st_size} bytes)")
    return 0


# ----------------------------------------------------------------------------- apply
def load_patches(path):
    obj = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(obj, dict):
        if "patches" not in obj or not isinstance(obj["patches"], list):
            raise ValueError("патч-файл: ожидался список или объект с полем 'patches'")
        return obj["patches"], obj
    if isinstance(obj, list):
        return obj, {}
    raise ValueError("патч-файл: ожидался список или объект")


def cmd_apply(args):
    src = Path(args.disk)
    out = Path(args.out_disk)
    if src.resolve() == out.resolve():
        print("ОШИБКА: <disk> и <out-disk> — один и тот же файл; эталон трогать запрещено",
              file=sys.stderr)
        return 1

    patches, meta = load_patches(args.patch_json)
    if not patches:
        print("ОШИБКА: список патчей пуст", file=sys.stderr)
        return 1

    data = bytearray(read_all(src, "disk"))
    nzones = check_size(data, src)
    src_sha_before = sha256_bytes(bytes(data))

    phys_mode = args.zone_mode == "physical"
    seen = set()
    applied = []
    touched_zones = set()

    for i, patch in enumerate(patches, 1):
        if not isinstance(patch, dict):
            raise ValueError(f"патч #{i}: ожидался объект")
        missing = [k for k in ("zone", "word", "old", "new") if k not in patch]
        if missing:
            raise ValueError(f"патч #{i}: отсутствуют поля {missing} (old обязателен!)")

        zone_raw = parse_num(patch["zone"], f"патч #{i} zone")
        word = parse_num(patch["word"], f"патч #{i} word")
        old = parse_num(patch["old"], f"патч #{i} old") & MASK48
        new = parse_num(patch["new"], f"патч #{i} new") & MASK48

        phys = zone_raw if phys_mode else zone_raw + ZONE_OFFSET
        if not (0 <= phys < nzones):
            raise ValueError(f"патч #{i}: зона {zone_raw} (phys {phys}) вне диапазона 0..{nzones - 1}")
        if word >= DATA_WORDS:
            raise ValueError(f"патч #{i}: слово {word} вне диапазона 0..{DATA_WORDS - 1}")

        key = (phys, word)
        if key in seen:
            raise ValueError(f"патч #{i}: дублирование (зона {zone_label(phys)}, слово {word})")
        seen.add(key)

        cur = read_word_u64(data, phys, word) & MASK48
        if cur != old:
            raise ValueError(
                f"патч #{i}: old НЕ СОВПАЛ для зоны {zone_label(phys)} слова {word}: "
                f"ожидалось 0o{old:o} (0x{old:x}), на диске 0o{cur:o} (0x{cur:x})"
            )

        real_old, real_new = set_word48(data, phys, word, new)
        touched_zones.add(phys)
        applied.append({
            "zone": zone_raw,
            "zone_physical": phys,
            "word": word,
            "old": real_old,
            "new": real_new,
        })

    if args.fix_checksum:
        for phys in sorted(touched_zones):
            recompute_checksum(data, phys)

    # Исходный диск не должен измениться ни на байт.
    if sha256_file(src) != src_sha_before:
        print("ОШИБКА: исходный диск изменился во время работы — прерываю", file=sys.stderr)
        return 1

    out.parent.mkdir(parents=True, exist_ok=True)
    fd, tmpname = tempfile.mkstemp(prefix=f".{out.name}.", suffix=".tmp", dir=str(out.parent))
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(data)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmpname, out)
    except BaseException:
        try:
            os.unlink(tmpname)
        except FileNotFoundError:
            pass
        raise

    print(f"apply: {src} -> {out}")
    print(f"  исходный диск sha256 (до/после): {src_sha_before} / {sha256_file(src)}")
    print(f"  применено патчей: {len(applied)}; затронуто зон: {len(touched_zones)}")
    for a in applied:
        print(f"  зона {zone_label(a['zone_physical'])}, слово {a['word']:4d} (0o{a['word']:o}): "
              f"0o{a['old']:o} -> 0o{a['new']:o}")
    if args.fix_checksum:
        print("  контрольные суммы затронутых зон пересчитаны (--fix-checksum)")
    return 0


# ----------------------------------------------------------------------------- verify
def cmd_verify(args):
    disk = Path(args.disk)
    data = read_all(disk, "disk")
    nzones = check_size(data, disk)
    cur_file_sha = sha256_bytes(data)

    snap = json.loads(Path(args.snapshot).read_text(encoding="utf-8"))
    fmt = snap.get("format", {})
    if fmt.get("zone_bytes") != ZONE_BYTES:
        print("ОШИБКА: несовместимый формат зоны в snapshot", file=sys.stderr)
        return 1
    snap_zones = snap.get("zones", {})
    if len(snap_zones) != nzones:
        print(f"ОШИБКА: число зон в snapshot ({len(snap_zones)}) != диску ({nzones})",
              file=sys.stderr)
        return 1

    changed_zones = []
    for phys in range(nzones):
        h = sha256_bytes(zone_slice(data, phys))
        if h != snap_zones.get(str(phys)):
            changed_zones.append(phys)

    # Для показа изменений на уровне слов нужен эталонный файл.
    ref_path = None
    ref_data = None
    if args.reference:
        ref_path = Path(args.reference)
    else:
        candidate = snap.get("disk_path")
        if candidate and Path(candidate).is_file():
            ref_path = Path(candidate)

    ref_ok = False
    if ref_path is not None and ref_path.is_file():
        ref_sha = sha256_file(ref_path)
        if ref_sha == snap.get("file_sha256"):
            ref_data = ref_path.read_bytes()
            ref_ok = True
        else:
            print(f"ВНИМАНИЕ: эталон {ref_path} не совпадает с snapshot "
                  f"({ref_sha} != {snap.get('file_sha256')}) — покажу только зоны")

    changed_words = []
    if ref_ok:
        for phys in changed_zones:
            a = zone_slice(ref_data, phys)
            b = zone_slice(data, phys)
            for word in range(DATA_WORDS):
                ua = struct.unpack_from("<Q", a, HDR_BYTES + word * WORD_BYTES)[0]
                ub = struct.unpack_from("<Q", b, HDR_BYTES + word * WORD_BYTES)[0]
                if ua != ub:
                    changed_words.append({
                        "zone_physical": phys,
                        "zone_label": zone_label(phys),
                        "word": word,
                        "old48": ua & MASK48,
                        "new48": ub & MASK48,
                        "old_u64": ua,
                        "new_u64": ub,
                        "kind": "data",
                    })
            for cw in range(CWORDS):
                ua = struct.unpack_from("<Q", a, cw * WORD_BYTES)[0]
                ub = struct.unpack_from("<Q", b, cw * WORD_BYTES)[0]
                if ua != ub:
                    changed_words.append({
                        "zone_physical": phys,
                        "zone_label": zone_label(phys),
                        "word": cw,
                        "old48": ua & MASK48,
                        "new48": ub & MASK48,
                        "old_u64": ua,
                        "new_u64": ub,
                        "kind": "cword",
                    })

    status = "IDENTICAL" if not changed_zones else "CHANGED"
    print(f"verify: {disk}")
    print(f"  snapshot disk     : {snap.get('disk_path')}")
    print(f"  file sha256       : {cur_file_sha}")
    print(f"  эталон доступен   : {'да' if ref_ok else 'нет'} ({ref_path})")
    print(f"  STATUS            : {status}")
    print(f"  изменённых зон    : {len(changed_zones)}")
    print(f"  изменённых слов   : {len(changed_words) if ref_ok else '? (нет эталона)'}")
    for phys in changed_zones:
        print(f"  ЗОНА  {zone_label(phys)}")
    for c in changed_words:
        print(f"  СЛОВО зона {c['zone_label']} word {c['word']:4d} (0o{c['word']:o}) "
              f"[{c['kind']}]: 0o{c['old48']:o} -> 0o{c['new48']:o} "
              f"(u64 0x{c['old_u64']:x} -> 0x{c['new_u64']:x})")

    result = {
        "tool": TOOL_NAME,
        "version": TOOL_VERSION,
        "checked_utc": utc_now(),
        "disk": str(disk.resolve()),
        "file_sha256": cur_file_sha,
        "status": status,
        "reference": str(ref_path) if ref_path else None,
        "reference_ok": ref_ok,
        "changed_zones_physical": changed_zones,
        "changed_words": changed_words,
    }
    if args.json_out:
        jout = Path(args.json_out)
        jout.parent.mkdir(parents=True, exist_ok=True)
        jout.write_text(json.dumps(result, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"  json-отчёт        : {jout}")

    if args.strict and changed_zones:
        return 2
    return 0


# ----------------------------------------------------------------------------- CLI
def build_parser():
    p = argparse.ArgumentParser(
        prog="patch_system_disk.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = p.add_subparsers(dest="cmd")

    s = sub.add_parser("snapshot", help="снять контрольные суммы всех зон (sha256)")
    s.add_argument("disk")
    s.add_argument("out_json")
    s.set_defaults(func=cmd_snapshot)

    a = sub.add_parser("apply", help="применить патч на копию диска (атомарно, только out-disk)")
    a.add_argument("disk")
    a.add_argument("patch_json")
    a.add_argument("out_disk")
    a.add_argument("--zone-mode", choices=("logical", "physical"), default="logical",
                   help="как понимать zone в патче: логическая (по умолчанию) или физическая")
    a.add_argument("--fix-checksum", action="store_true",
                   help="пересчитать cwords[3]/cwords[7] затронутых зон")
    a.set_defaults(func=cmd_apply)

    v = sub.add_parser("verify", help="побайтовая сверка с snapshot, показать изменённые зоны/слова")
    v.add_argument("disk")
    v.add_argument("snapshot")
    v.add_argument("reference", nargs="?", default=None,
                   help="эталонный диск для показа слов (по умолчанию — путь из snapshot)")
    v.add_argument("--json-out", default=None, help="записать машиночитаемый отчёт")
    v.add_argument("--strict", action="store_true", help="rc=2 при наличии изменений")
    v.set_defaults(func=cmd_verify)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "cmd", None):
        parser.print_help()
        return 1
    try:
        return args.func(args)
    except (ValueError, FileNotFoundError, OSError, json.JSONDecodeError) as e:
        print(f"ОШИБКА: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
