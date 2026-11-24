#!/usr/bin/env python3
"""Run one deck under full BESM-6 SIMH on an isolated tmux socket.

Console via capture-pane /ДATA:/ marker only; input via send-keys only.
Copies only; no live disk, no tmux session 0, no repo/git writes, no C patch.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

SIMH = Path("/home/azizz/Yandex.Disk/simh/BESM6")
EMULATOR = Path("/home/azizz/Yandex.Disk/simh/BIN/besm6")
WS = Path(__file__).resolve().parent.parent
RUNS = WS / "runs"
BOOT_MARKER = re.compile(r"[ДD]ATA:")


def tmux(env, *args, check=True):
    r = subprocess.run(["tmux", *args], text=True, capture_output=True, env=env)
    if check and r.returncode:
        raise RuntimeError(f"tmux {' '.join(args)}: {r.stderr.strip()}")
    return r.stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", required=True)
    ap.add_argument("--deck", default=str(WS / "decks/deck_trans.b6"))
    ap.add_argument("--session", default=None)
    ap.add_argument("--timeout", type=int, default=240)
    ap.add_argument("--trace-on-start", action="store_true")
    ap.add_argument("--trace-wide", action="store_true",
                    help="trace from boot (ini already has set debug + set cpu debug)")
    ap.add_argument("--bp", default=None, help="breakpoint address (octal) to arm trace at")
    ap.add_argument("--steps", type=int, default=0, help="half-instruction steps to trace after bp")
    ap.add_argument("--skip-bp", type=int, default=0, help="ignore this many breakpoint hits")
    a = ap.parse_args()
    deck = Path(a.deck).resolve()
    session = a.session or ("ftg-" + a.case)
    env = dict(os.environ, TMUX_TMPDIR=str(RUNS / "tmux"))
    (RUNS / "tmux").mkdir(exist_ok=True)
    ini = RUNS / f"ini_{a.case}.ini"

    if subprocess.run(["tmux", "has-session", "-t", session], env=env,
                      capture_output=True).returncode == 0:
        tmux(env, "kill-session", "-t", session, check=False)

    def pane(history=2000):
        return tmux(env, "capture-pane", "-p", "-S", str(-history),
                    "-t", session, check=False)

    def send(text, enter=True, slow=False):
        if slow:
            for ch in text:
                tmux(env, "send-keys", "-t", session, "-l", ch)
                time.sleep(0.12)
        else:
            tmux(env, "send-keys", "-t", session, "-l", text)
        if enter:
            tmux(env, "send-keys", "-t", session, "Enter")

    def lastline():
        lines = [l for l in pane(history=200).splitlines() if l.strip()]
        return lines[-1].strip() if lines else ""

    def to_sim():
        for _ in range(20):
            if lastline().endswith("sim>"):
                return True
            time.sleep(0.5)
        return False

    transcript = []
    tmux(env, "new-session", "-d", "-s", session, "-x", "200", "-y", "50",
         f"cd {SIMH / 'OSZAGR'} && {EMULATOR} {ini}")
    try:
        deadline = time.time() + a.timeout
        booted = False
        while time.time() < deadline:
            if BOOT_MARKER.search(pane()):
                booted = True
                break
            time.sleep(0.5)
        if not booted:
            transcript.append(pane())
            raise TimeoutError("no ДATA: boot marker in capture-pane")
        print("BOOT marker ДATA: seen", flush=True)
        time.sleep(6.0)
        for cmd in ("ДАЙ А0", "ДАЙ А1"):
            send(cmd, slow=True)
            time.sleep(2.0)
        send("НОМВ", slow=True)
        time.sleep(2.0)
        print("НОМВ before deck:", repr(pane(history=30)[-300:]), flush=True)
        tmux(env, "send-keys", "-t", session, "C-g")
        if not to_sim():
            raise RuntimeError("no sim> prompt after C-g")
        for cmd in (f"at vu0 {deck}", "d 6 1", "d 5 10", "set cpu req"):
            send(cmd)
            time.sleep(0.8)
        if a.bp:
            send(f"break {a.bp}")
            time.sleep(0.5)
        send("go")
        time.sleep(1.0)

        # Post-deck НОМВ only after a confirmed job-start line.
        for _ in range(int(a.timeout / 2)):
            if re.search(r"B075|ОЗ\s*\(|КЗ\s*\(", pane(history=200)):
                break
            time.sleep(0.5)
        send("НОМВ", slow=True)
        time.sleep(1.0)
        print("post-deck НОМВ sent after job-start line", flush=True)

        traced = False
        if a.bp:
            hits = 0
            armed = False
            while not armed:
                for _ in range(int(a.timeout / 2)):
                    if lastline().endswith("sim>"):
                        break
                    time.sleep(0.5)
                hits += 1
                bp_lines = [l for l in pane(history=60).splitlines() if "Точка останова" in l]
                bp_line = bp_lines[-1] if bp_lines else ""
                print(f"bp hit #{hits}: {bp_line.strip()!r}", flush=True)
                if hits <= a.skip_bp:
                    send("go")
                    for _ in range(20):
                        if not lastline().endswith("sim>"):
                            break
                        time.sleep(0.5)
                    continue
                armed = True
            print("arming trace after bp hits:", hits, flush=True)
            send(f"set debug {RUNS / ('debug_' + a.case + '.txt')}")
            time.sleep(0.3)
            send("set cpu debug")
            time.sleep(0.3)
            traced = True
            if a.steps:
                for _ in range(a.steps):
                    send("step")
                    time.sleep(0.08)
                send("set cpu nodebug")
                time.sleep(0.3)
                send("set nodebug")
                time.sleep(0.3)
            send("go")

        if a.trace_on_start:
            for _ in range(int(a.timeout / 2)):
                if re.search(r"B075|ОЗ\s*\(|КЗ\s*\(", pane(history=200)):
                    break
                time.sleep(0.4)
            print("job-start line seen:", repr(pane(history=12)[-300:]), flush=True)
            tmux(env, "send-keys", "-t", session, "C-g")
            to_sim()
            send(f"set debug {RUNS / ('debug_' + a.case + '.txt')}")
            send("set cpu debug")
            send("go")
            print("trace armed at job start", flush=True)
            for _ in range(int(a.timeout / 2)):
                if re.search(r"КОНЕЦ ЗАДАЧИ|[КK]З\s*\(|ОЗ\s*\(", pane(history=200)):
                    break
                if lastline().endswith("sim>"):
                    send("go")
                time.sleep(0.6)
            tmux(env, "send-keys", "-t", session, "C-g")
            to_sim()
            send("set cpu nodebug")
            send("set nodebug")
            send("go")
            print("trace disarmed", flush=True)

        # Post-deck НОМВ only after a confirmed job-start / completion line.
        deadline = time.time() + a.timeout
        done = False
        while time.time() < deadline:
            txt = pane()
            if re.search(r"КОНЕЦ ЗАДАЧИ|[КK]З\s*\(|ОЗ\s*\(|СБО", txt):
                done = True
                break
            if txt.rstrip().endswith("sim>"):
                send("go")
            time.sleep(1.5)
        print("JOB completion marker:", done, flush=True)
        time.sleep(6.0)
        transcript.append(pane())
    finally:
        (RUNS / f"console_{a.case}.txt").write_text("\n".join(transcript))
        acpu_dir = SIMH / "ACPU"
        for p, name in ((acpu_dir / "output.txt", "acpu"),
                        (acpu_dir / "output1.txt", "acpu1")):
            if p.exists():
                shutil.copy2(p, RUNS / f"{name}_{a.case}.txt")
        tmux(env, "kill-session", "-t", session, check=False)

    devices = [RUNS / f"localprn_{a.case}.txt"]
    devices = [p for p in devices if p.exists() and p.stat().st_size]
    prn = devices[0] if devices else None
    if prn:
        acpu = prn.read_text(encoding="utf-8", errors="replace")
        print("===== ACPU =====")
        print(acpu[-3000:])
    return 0 if "КОНЕЦ ЗАДАЧИ" in (prn.read_text(errors="replace") if prn else "") else 2


if __name__ == "__main__":
    sys.exit(main())
