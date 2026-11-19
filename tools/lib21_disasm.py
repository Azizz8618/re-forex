#!/usr/bin/env python3
"""Массовое дизассемблирование DMS-библиотеки lib21 через dtran.

Для каждого объекта библиотеки извлекается объектный образ (секции cmd..debug,
без comment), записывается во временный .dms в build/ и разбирается
`dtran -F dms`.  Результат сохраняется в disasm/lib21/<имя>.madlen.

Имена модулей преобразуются: '/' -> '#', '*' -> '_'  (например, GIV/PG ->
GIV#PG, FOREX* -> FOREX_).  Если dtran падает или даёт пустой вывод, в
disasm/lib21 пишется пустой файл, а модуль перечисляется в логе.

Использование:
    tools/lib21_disasm.py                       # все 358 модулей
    tools/lib21_disasm.py --module FOREX*
    tools/lib21_disasm.py --limit 10
    tools/lib21_disasm.py --out /tmp/disasm --dtran /path/to/dtran
"""

import argparse
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = Path("/home/azizz/Yandex.Disk/besm6-new/DUBNA/BUILD/elements/lib21.bin")
SIPROD_TOOLS = Path("/home/azizz/Yandex.Disk/re-siprod/tools")
DEFAULT_OUT = ROOT / "disasm" / "lib21"
DEFAULT_LOG = ROOT / "logs" / "lib21_disasm.txt"
DEFAULT_DTRAN = "/home/azizz/Yandex.Disk/dtran/dtran"
BUILD = ROOT / "build"


def load_library():
    """Импортировать парсер siprod_lib и прочитать библиотеку."""
    if str(SIPROD_TOOLS) not in sys.path:
        sys.path.insert(0, str(SIPROD_TOOLS))
    try:
        import siprod_lib
    except ImportError as exc:
        raise SystemExit(f"не найден парсер siprod_lib.py в {SIPROD_TOOLS}: {exc}")
    return siprod_lib.Library(str(LIB))


def find_dtran(path=None):
    if path:
        return path
    found = shutil.which("dtran")
    if found:
        return found
    for candidate in (DEFAULT_DTRAN, "/home/azizz/Yandex.Disk/monitor80-re/dtran/dtran"):
        if os.path.exists(candidate):
            return candidate
    return None


def safe_name(name):
    """Имя файла для модуля: '/'-'#' и '*'-'_'."""
    return name.replace("/", "#").replace("*", "_")


def object_image(lib, name):
    """Объектный образ модуля: с заголовка по debug включительно, без comment."""
    s, h = lib.objects[name]
    sec = lib.sections(name)
    end = sec["debug"] + h["debug"]
    return b"".join(w.to_bytes(6, "big") for w in lib.words[s:end])


def disassemble(dtran, image, dms_path):
    """Прогнать dtran; вернуть (текст, число строк, сообщение об ошибке)."""
    dms_path.write_bytes(image)
    try:
        r = subprocess.run([dtran, "-F", "dms", str(dms_path)],
                           capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return "", 0, "dtran timeout"
    except OSError as exc:
        return "", 0, f"dtran OSError: {exc}"
    # Убрать служебные строки 'C ...' (счётчики разделов, симтаблица):
    # первым должен идти 'FOREX*  :,NAME, NEW DTRAN'.
    lines = [line for line in r.stdout.splitlines() if not line.startswith("C ")]
    text = ("\n".join(lines).strip() + "\n") if lines else ""
    if r.returncode != 0:
        err = (r.stderr or "").strip().splitlines()
        msg = "dtran rc=%d" % r.returncode
        if err:
            msg += ": " + err[-1][:160]
        return "", 0, msg
    if not text:
        return "", 0, "пустой вывод dtran"
    return text, len(text.splitlines()), ""


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--module", action="append", metavar="ИМЯ",
                    help="разобрать только указанный модуль (можно повторить)")
    ap.add_argument("--limit", type=int, metavar="N",
                    help="разобрать только первые N модулей")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, metavar="DIR",
                    help="каталог для *.madlen (по умолчанию disasm/lib21)")
    ap.add_argument("--dtran", default=None, metavar="PATH",
                    help="путь к dtran (по умолчанию ищется автоматически)")
    ap.add_argument("--log", type=Path, default=DEFAULT_LOG, metavar="FILE",
                    help="файл лога (по умолчанию logs/lib21_disasm.txt)")
    args = ap.parse_args()

    dtran = find_dtran(args.dtran)
    if not dtran:
        raise SystemExit("не найден dtran (укажите --dtran=PATH)")
    if not LIB.exists():
        raise SystemExit(f"нет библиотеки {LIB}")

    lib = load_library()
    names = sorted(lib.objects)
    if args.module:
        missing = [m for m in args.module if m not in lib.objects]
        if missing:
            raise SystemExit("нет модулей в библиотеке: " + ", ".join(missing))
        names = [m for m in names if m in set(args.module)]
    if args.limit is not None:
        names = names[:args.limit]

    args.out.mkdir(parents=True, exist_ok=True)
    BUILD.mkdir(parents=True, exist_ok=True)
    args.log.parent.mkdir(parents=True, exist_ok=True)

    log = []
    log.append("Дизассемблирование lib21.bin — " + datetime.now().isoformat(timespec="seconds"))
    log.append(f"библиотека: {LIB}")
    log.append(f"dtran: {dtran}")
    log.append(f"выход: {args.out}")
    log.append(f"модулей выбрано: {len(names)} (в библиотеке {len(lib.objects)})")
    log.append("")

    empty = []       # (имя, причина)
    sizes = []
    dms_path = BUILD / "_lib21_module.dms"
    for idx, name in enumerate(names, 1):
        image = object_image(lib, name)
        text, nlines, err = disassemble(dtran, image, dms_path)
        out_file = args.out / (safe_name(name) + ".madlen")
        out_file.write_text(text, encoding="utf-8")
        if err:
            empty.append((name, err))
            status = "EMPTY " + err
        else:
            sizes.append(nlines)
            status = f"{nlines:5d} строк"
        line = f"[{idx:3d}/{len(names)}] {name:12s} -> {out_file.name:24s} {status}"
        log.append(line)
        if idx % 50 == 0:
            print(line, file=sys.stderr, flush=True)

    if dms_path.exists():
        dms_path.unlink()

    avg = sum(sizes) / len(sizes) if sizes else 0.0
    log.append("")
    log.append("=== СВОДКА ===")
    log.append(f"обработано модулей:        {len(names)}")
    log.append(f"с непустым листингом:      {len(sizes)}")
    log.append(f"с пустым выводом / ошибкой:{len(empty)}")
    log.append(f"средний размер листинга:   {avg:.1f} строк")
    log.append(f"мин / макс строк:          {min(sizes) if sizes else 0} / {max(sizes) if sizes else 0}")
    log.append("")
    if empty:
        log.append("Модули с пустым выводом или ошибкой dtran:")
        for name, err in empty:
            log.append(f"  {name:12s} {err}")
    else:
        log.append("Модулей с пустым выводом или ошибкой dtran: нет")

    args.log.write_text("\n".join(log) + "\n", encoding="utf-8")
    print(f"готово: {len(sizes)} разобрано, {len(empty)} пустых/ошибок, "
          f"средний размер {avg:.1f} строк; лог: {args.log}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
