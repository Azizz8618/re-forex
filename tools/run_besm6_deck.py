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
    python3 tools/run_besm6_deck.py --source prog.f77 --name HELLO --cipher 410300
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
# Принтер ОС пишет в СТАБИЛЬНУЮ папку ACPU (prn0=output.txt, prn1=output1.txt),
# а не во временный файл, подключённый к prn0: не перехватывать его!
ACPU_DIR = SIMH / "ACPU"
# Разбор выдачи АЦПУ — штатный инструмент re-dispak (docs/MEMORY.md,
# docs/ВВОД_АНАЛИЗ.md §6): подвалы КОНЕЦ ЗАДАЧИ/СБО, маркеры * и 555...
ACPU_ANALYZER = Path("/home/azizz/Yandex.Disk/re-dispak/acpu_analyze.pl")

HELLO = """ШИФР 410300 ЗС5^
ОЗУ 32^АЦП 32^
EEВ1А3
*NAME HELLO
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
    """Подать команду в панель терминала.

    Кириллические директивы ОС (ДАЙ, НОМ, ВЦП, ВЫБ) надёжно идут только
    через pipe-buffer (см. ВВОД_АНАЛИЗ.md §3.4а); send-keys с кириллицей
    искажает символы. Чтение ответа — только через capture-pane (pane()).
    """
    payload = text + ("\r" if enter else "")
    r = subprocess.run(["tmux", "pipe-buffer", "-t", session, "-"],
                       input=payload, text=True, capture_output=True)
    if r.returncode != 0:
        # fallback для ASCII-команд SIMH на старых tmux без pipe-buffer
        tmux("send-keys", "-t", session, text)
        if enter:
            tmux("send-keys", "-t", session, "Enter")


def make_ini(work: Path, prn_path: Path, vu_path: Path, base=None, extra=None) -> Path:
    text = (Path(base) if base else BASE_INI).read_text(encoding="utf-8")
    if extra:
        text += "\n" + "\n".join(extra) + "\n"
    out = []
    for line in text.splitlines():
        if re.search(r"^\s*attach\s+-n\s+vu0\b", line):
            # Не подключаем vu0 при загрузке: SIMH может переоткрыть/обнулить
            # файл. Колода подаётся командой `at vu0` уже после старта ОС.
            out.append("; " + line)
        elif re.search(r"^\s*attach\s+-n\s+prn[01]\b", line):
            out.append(line)  # штатные файлы в папке ACPU — не подменять
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
        f"ОЗУ 32^АЦП {args.acpu}^\n"
        f"EEВ1А3\n"
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
    ap.add_argument("--cipher", default="410300", help="шифр задачи, зарегистрированный в ОС (например 410300)")
    ap.add_argument("--acpu", type=int, default=64, help="метры бумаги АЦПУ")
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    ap.add_argument("--session", default="besm6-deck", help="имя tmux-сессии")
    ap.add_argument("--ini", help="базовый ini вместо OSZAGR/dispak.ini")
    ap.add_argument("--tape", action="store_true",
                    help="ввод с перфоленты: at -t fs0 вместо at vu0 (UVU/*.ini)")
    ap.add_argument("--md", action="append", default=[],
                    help="доп. строка attach для SIMH (можно повторять)")
    ap.add_argument("--keep", action="store_true", help="не убивать сессию после прогона")
    args = ap.parse_args()

    for p in (EMULATOR, BASE_INI):
        if not p.exists():
            sys.exit(f"нет файла: {p}")
    if shutil.which("tmux") is None:
        sys.exit("tmux не найден")

    work = Path(tempfile.mkdtemp(prefix="besm6-deck-", dir="/var/tmp"))
    deck = work / "deck.txt"
    deck.write_text(build_deck(args), encoding="utf-8")
    # Снимок папки ACPU до прогона: после найдём изменившийся файл.
    acpu_before = {p.name: p.stat().st_mtime_ns for p in ACPU_DIR.glob("*")
                   if p.is_file()}
    ini = make_ini(work, None, deck)
    log(f"koloda : {deck} ({deck.stat().st_size} байт)")
    log(f"acpu   : папка {ACPU_DIR} (prn0=output.txt, prn1=output1.txt)")
    log(f"ini    : {ini}")

    if tmux("has-session", "-t", args.session, check=False).strip() and \
            subprocess.run(["tmux", "has-session", "-t", args.session]).returncode == 0:
        sys.exit(f"сессия {args.session} уже есть; убей её или укажи --session другой")

    tmux("new-session", "-d", "-s", args.session, "-x", "200", "-y", "50",
         f"cd {SIMH / 'OSZAGR'} && {EMULATOR} {ini}")
    try:
        log("ждём загрузки ОС (CM1П)...")
        wait_for(args.session, PROMPT_RE, args.timeout, "промпт ОС")

        # Очистка входной очереди от предыдущих зависших задач нашего шифра:
        # НОМ показывает «<шифр> <N>», ВЫБ <N> исключает задачу (1..377).
        send(args.session, "НОМ")
        time.sleep(2.0)
        queued = re.findall(r"%s\s+(\d{1,3})" % re.escape(args.cipher),
                            pane(args.session))
        if queued:
            log(f"очистка очереди: ВЫБ {queued}")
            for n in queued:
                send(args.session, f"ВЫБ {int(n)}")
                time.sleep(0.8)
            send(args.session, "НОМ")
            time.sleep(2.0)

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

        log("Ctrl+G -> sim>, подаём колоду (" +
            ("fs0 -t, перфолента" if args.tape else "vu0, перфокарты") + ") + FS8")
        tmux("send-keys", "-t", args.session, "C-g")
        time.sleep(0.5)
        attach = f"at -t fs0 {deck}" if args.tape else f"at vu0 {deck}"
        for cmd in (attach, "d 6 1", "d 5 10", "set cpu req", "go"):
            send(args.session, cmd)
            time.sleep(0.5)

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

        # Диагностика состояния (ВЦП): «ЗНЕТ» — задач в решении нет,
        # терминал свободен; список — система ещё занята. ВЦП <N канала>
        # дополнительно показывает обмен с МД/МГ (ЗП/ЧТ, зона, бобина).
        # re-dispak/Dispak-operator-guide.md §4.3.1, ВВОД_АНАЛИЗ.md §3.4а.
        if "sim>" in pane(args.session).splitlines()[-1]:
            send(args.session, "go")
            time.sleep(1.0)
        send(args.session, "ВЦП")
        time.sleep(2.0)
        vcp = pane(args.session)
        if re.search(r"ЗНЕТ", vcp):
            log("ВЦП: задач в решении НЕТ (ЗНЕТ) — терминал свободен")
        else:
            log("ВЦП: задачи в решении:")
            for line in vcp.splitlines():
                if re.search(r"ВЦПП|410300|\d{12}|ЗНЕТ", line):
                    log("  " + line.strip())
        send(args.session, "ВЦП Р")
        time.sleep(2.0)
        log("ВЦП Р (ресурсы):")
        for line in pane(args.session).splitlines()[-25:]:
            if re.search(r"ВЦПП|ОЗУ|ТРАКТ|410300|\d{12}", line, re.I):
                log("  " + line.strip())

        # Освобождение буфера вывода (указание пользователя): результат
        # выталкивается из буфера командами НОМ (список задач) и ВЫБ <N>
        # (исключить задачу с буфера, re-dispak/Dispak-operator-guide.md §4.4.5,
        # §5.6). Номер задачи берём из строки КЗ/ОЗ/ЧП вида КЗ(075).
        if "sim>" in pane(args.session).splitlines()[-1]:
            send(args.session, "go")  # вернуть CPU из останова в ОС
            time.sleep(1.0)
        send(args.session, "НОМ")
        time.sleep(2.0)
        status = pane(args.session)
        nums = re.findall(r"[ЧК]З\((\d{1,3})\)|ЧП\((\d{1,3})\)", status)
        targets = [a or b for a, b in nums]
        log(f"НОМ: задачи на буфере: {targets}")
        for n in targets:
            send(args.session, f"ВЫБ {int(n)}")
            time.sleep(2.0)
        if targets:
            send(args.session, "НОМ")
            time.sleep(2.0)

        # АЦПУ — барабанный принтер: запись в файл асинхронна, дать стечь
        time.sleep(5)

        changed = [p for p in ACPU_DIR.glob("*")
                   if p.is_file() and p.stat().st_mtime_ns != acpu_before.get(p.name, -1)]
        changed.sort(key=lambda p: p.stat().st_mtime_ns, reverse=True)
        prn = changed[0] if changed else None
        log(f"изменённые файлы ACPU: {[p.name for p in changed]}")
        if prn:
            print(f"\n===== АЦПУ ({prn.name}, сырая распечатка) =====")
            print(prn.read_text(encoding="utf-8", errors="replace") or "(пусто)")
        if ACPU_ANALYZER.exists() and prn and prn.stat().st_size:
            print("===== разбор выдачи АЦПУ (re-dispak/acpu_analyze.pl) =====")
            for flag in ("--summary", "--jobs", "--errors"):
                r = subprocess.run(["perl", str(ACPU_ANALYZER), str(prn), flag],
                                   text=True, capture_output=True)
                if r.returncode == 0 and r.stdout.strip():
                    print(f"--- {flag} ---")
                    print(r.stdout)
        print("===== transcripts (консоль, последние 120 строк истории) =====")
        print("\n".join(pane(args.session).splitlines()[-120:]))
        return 0 if prn and prn.stat().st_size else 1
    finally:
        if not args.keep:
            tmux("kill-session", "-t", args.session, check=False)
        log(f"рабочий каталог: {work}")


if __name__ == "__main__":
    sys.exit(main())
