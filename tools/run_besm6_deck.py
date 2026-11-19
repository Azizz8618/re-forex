#!/usr/bin/env python3
"""Подать колоду перфокарт в полноценную ОС ДИСПАК под SIMH и забрать вывод АЦПУ.

Работает НАПРЯМУЮ, без системы КРАБ: колода подаётся на устройство vu0,
сигнал FS8 формируется командами `d 6 1` / `d 5 10` / `set cpu req` / `go`,
результат читается из файла, подключённого к prn0 (АЦПУ).

Источник механизма: simh/BESM6/docs/ВВОД_АНАЛИЗ.md §§3.2, 9.2, 9.3.
Эталонная колода: там же §9.2 (минимальная Fortran-программа HELLO WORLD).

Примеры:
    python3 tools/run_besm6_deck.py --hello
    python3 tools/run_besm6_deck.py --deck myjob.txt --timeout 120
    python3 tools/run_besm6_deck.py --source prog.f77 --name HELLO --cipher 123456
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SIMH = Path("/home/azizz/Yandex.Disk/simh/BESM6")
BASE_INI = SIMH / "OSZAGR/dispak.ini"
EMULATOR = SIMH / "BIN/besm6"
# Разбор выдачи АЦПУ — штатный инструмент re-dispak (docs/MEMORY.md,
# docs/ВВОД_АНАЛИЗ.md §6): подвалы КОНЕЦ ЗАДАЧИ/СБО, маркеры * и 555...
ACPU_ANALYZER = Path("/home/azizz/Yandex.Disk/re-dispak/acpu_analyze.pl")

HELLO = """ШИФР 123456 ЗС5^
ОЗУ 16^АЦП 32^
ЕЕВ1А3
*NAME HELLO
*CALL YESMEMORY
*FTN
      PROGRAM MAIN
      PRINT 100
  100 FORMAT('HELLO WORLD')
      END
*EXECUTE
*END FILE
``````
ЕКОНЕЦ
"""

DEFAULT_TIMEOUT = 180
PROMPT_RE = re.compile(r"CM1П|CM1П:", re.I)
DONE_RE = re.compile(r"КОНЕЦ ЗАДАЧИ|КЗ\s*\(|\*\*\*", re.I)


def log(msg):
    print(msg, flush=True)


def tmux(*args, check=True):
    cmd = ["tmux", *args]
    r = subprocess.run(cmd, text=True, capture_output=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"tmux {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout


def pane(session, history=2000):
    return tmux("capture-pane", "-p", "-S", str(-history), "-t", session, check=False)


def send(session, text, enter=True):
    tmux("send-keys", "-t", session, text)
    if enter:
        tmux("send-keys", "-t", session, "Enter")


def make_ini(work: Path, prn_path: Path, vu_path: Path) -> Path:
    text = BASE_INI.read_text(encoding="utf-8")
    out = []
    for line in text.splitlines():
        if re.search(r"^\s*attach\s+-n\s+vu0\b", line):
            # Не подключаем vu0 при загрузке: SIMH может переоткрыть/обнулить
            # файл. Колода подаётся командой `at vu0` уже после старта ОС.
            out.append("; " + line)
        elif re.search(r"^\s*attach\s+-n\s+prn0\b", line):
            out.append(f"attach -n prn0 {prn_path}")
        else:
            out.append(line)
    ini = work / "deck.ini"
    ini.write_text("\n".join(out) + "\n", encoding="utf-8")
    return ini


def wait_for(session, pattern, timeout, label):
    end = time.time() + timeout
    while time.time() < end:
        if pattern.search(pane(session)):
            return True
        time.sleep(0.5)
    raise TimeoutError(f"не дождались {label} за {timeout} c")


def build_deck(args) -> str:
    if args.hello:
        return HELLO
    if args.deck:
        return Path(args.deck).read_text(encoding="utf-8")
    src = Path(args.source).read_text(encoding="utf-8")
    body = "\n".join("      " + l.strip() if l.strip() else "" for l in src.splitlines())
    return (
        f"ШИФР {args.cipher} ЗС5^\n"
        f"ОЗУ 16^АЦП {args.acpu}^\n"
        f"ЕЕВ1А3\n"
        f"*NAME {args.name}\n"
        f"*FTN\n{body}\n"
        f"*EXECUTE\n"
        f"*END FILE\n"
        f"``````\nЕКОНЕЦ\n"
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--hello", action="store_true", help="эталонная колода HELLO WORLD")
    src.add_argument("--deck", help="готовый файл колоды")
    src.add_argument("--source", help="Fortran-исходник (простая программа)")
    ap.add_argument("--name", default="HELLO", help="*NAME для --source")
    ap.add_argument("--cipher", default="123456", help="шифр задачи (не 419999!)")
    ap.add_argument("--acpu", type=int, default=64, help="метры бумаги АЦПУ")
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    ap.add_argument("--session", default="besm6-deck", help="имя tmux-сессии")
    ap.add_argument("--keep", action="store_true", help="не убивать сессию после прогона")
    args = ap.parse_args()

    for p in (EMULATOR, BASE_INI):
        if not p.exists():
            sys.exit(f"нет файла: {p}")
    if shutil.which("tmux") is None:
        sys.exit("tmux не найден")

    work = Path(tempfile.mkdtemp(prefix="besm6-deck-", dir="/var/tmp"))
    deck = work / "deck.txt"
    prn = work / "acpu.txt"
    deck.write_text(build_deck(args), encoding="utf-8")
    prn.touch()
    ini = make_ini(work, prn, deck)
    log(f"koloda : {deck} ({deck.stat().st_size} байт)")
    log(f"acpu   : {prn}")
    log(f"ini    : {ini}")

    if tmux("has-session", "-t", args.session, check=False).strip() and \
            subprocess.run(["tmux", "has-session", "-t", args.session]).returncode == 0:
        sys.exit(f"сессия {args.session} уже есть; убей её или укажи --session другой")

    tmux("new-session", "-d", "-s", args.session, "-x", "200", "-y", "50",
         f"cd {SIMH / 'OSZAGR'} && {EMULATOR} {ini}")
    try:
        log("ждём загрузки ОС (CM1П)...")
        wait_for(args.session, PROMPT_RE, args.timeout, "промпт ОС")

        # КЛЮЧЕВОЕ (re-dispak/docs/DISPAK_AGENT.md §6): сообщение
        # «ОСВОБ БУФ.ВЫВ» означает, что устройства вывода НЕ в конфигурации.
        # Операторская директива ДАЙ А0/А1 подключает АЦПУ; без неё задача
        # завершается, но АЦПУ пуст. СБО без параметров применять нельзя.
        log("оператор: ДАЙ А0 / ДАЙ А1 (подключить АЦПУ к конфигурации)")
        for cmd in ("ДАЙ А0", "ДАЙ А1"):
            send(args.session, cmd)
            time.sleep(1.0)
        conf = pane(args.session)
        if "ЕСТЬ" not in conf:
            log("ВНИМАНИЕ: ответа ЕСТЬ на ДАЙ А0/A1 нет — АЦПУ может быть не подключён")

        log("Ctrl+G -> sim>, подаём колоду на vu0 + FS8")
        tmux("send-keys", "-t", args.session, "C-g")
        time.sleep(0.5)
        for cmd in (f"at vu0 {deck}",
                    "d 6 1", "d 5 10", "set cpu req", "go"):
            send(args.session, cmd)
            time.sleep(0.3)

        log(f"ждём КОНЕЦ ЗАДАЧИ (до {args.timeout} c)...")
        done = False
        end = time.time() + args.timeout
        while time.time() < end:
            if DONE_RE.search(pane(args.session)):
                done = True
                break
            time.sleep(1.0)
        if not done:
            log("ВНИМАНИЕ: КОНЕЦ ЗАДАЧИ не появился — см. transcript ниже")

        # АЦПУ — барабанный принтер: запись в файл асинхронна, дать стечь
        time.sleep(5)

        print("\n===== АЦПУ (prn0, сырая распечатка) =====")
        print(prn.read_text(encoding="utf-8", errors="replace") or "(пусто)")
        if ACPU_ANALYZER.exists() and prn.stat().st_size:
            print("===== разбор выдачи АЦПУ (re-dispak/acpu_analyze.pl) =====")
            for flag in ("--summary", "--jobs", "--errors"):
                r = subprocess.run(["perl", str(ACPU_ANALYZER), str(prn), flag],
                                   text=True, capture_output=True)
                if r.returncode == 0 and r.stdout.strip():
                    print(f"--- {flag} ---")
                    print(r.stdout)
        print("===== transcripts (консоль, последние 120 строк истории) =====")
        print("\n".join(pane(args.session).splitlines()[-120:]))
        return 0 if done and prn.stat().st_size else 1
    finally:
        if not args.keep:
            tmux("kill-session", "-t", args.session, check=False)
        log(f"рабочий каталог: {work}")


if __name__ == "__main__":
    sys.exit(main())
