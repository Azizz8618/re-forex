#!/usr/bin/env python3
"""Minimal SIMH driver: exact operator sequence proven to launch the queued job.

Boots with the port-shifted ini, attaches the deck, then uses the DISPAK operator
sequence ДАЙ А0 / НОМВ after job-start.  Polls prn0 (not the console) for the
product result and never sends more input once the job is launched.
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import setup_b

WS = Path(__file__).resolve().parent
SIMH = Path("/home/azizz/Yandex.Disk/simh/BESM6")
EMULATOR = SIMH / "BIN" / "besm6"
RUNS = WS / "runs"
BOOT = re.compile(r"[ДD]ATA:")
JOB = re.compile(r"B075|ОЗ\s*\(")
RESULT = re.compile(r"(?m)^\s*21\s+\S")
DONE = "КОНЕЦ ЗАДАЧИ"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", required=True)
    ap.add_argument("--deck", required=True)
    ap.add_argument("--image", required=True)
    ap.add_argument("--session", default=None)
    ap.add_argument("--timeout", type=int, default=400)
    a = ap.parse_args()
    sha = hashlib.sha256(EMULATOR.read_bytes()).hexdigest()[:16]
    assert sha.startswith("d0583057"), sha
    deck = Path(a.deck).resolve()
    prn = RUNS / f"localprn_{a.case}.txt"
    for stale in (prn, RUNS / f"localprn1_{a.case}.txt"):
        if stale.is_file():
            stale.unlink()
    ini = setup_b.make_ini(a.case, a.image)
    session = a.session or f"dm-{a.case}"
    env = dict(os.environ, TMUX_TMPDIR=str(RUNS / "tmux"))
    (RUNS / "tmux").mkdir(parents=True, exist_ok=True)
    if subprocess.run(["tmux", "has-session", "-t", session], env=env,
                      capture_output=True).returncode == 0:
        subprocess.run(["tmux", "kill-session", "-t", session], env=env)

    def tmux(*args, check=False):
        r = subprocess.run(["tmux", *args], text=True, capture_output=True, env=env)
        if check and r.returncode:
            raise RuntimeError(f"tmux {args}: {r.stderr.strip()}")
        return r.stdout

    def pane(h=2000):
        return tmux("capture-pane", "-p", "-S", str(-h), "-t", session)

    def send(text):
        tmux("send-keys", "-t", session, "-l", text)
        tmux("send-keys", "-t", session, "Enter")

    def send_slow(text):
        for ch in text:
            tmux("send-keys", "-t", session, "-l", ch)
            time.sleep(0.12)
        tmux("send-keys", "-t", session, "Enter")

    console = ""
    boot = started = launched = False
    tmux("new-session", "-d", "-s", session, "-x", "200", "-y", "50",
         f"cd {SIMH / 'OSZAGR'} && {EMULATOR} {ini}", check=True)
    try:
        deadline = time.time() + a.timeout
        while time.time() < deadline and not boot:
            boot = bool(BOOT.search(pane()))
            time.sleep(0.5)
        print(f"[{a.case}] boot={boot}", flush=True)
        time.sleep(3.0)
        for cmd in ("ДАЙ А0", "ДАЙ А1"):
            send_slow(cmd); time.sleep(2.0)
        send_slow("НОМВ"); time.sleep(2.0)

        tmux("send-keys", "-t", session, "C-g")
        for _ in range(40):
            lines = [l for l in pane(h=200).splitlines() if l.strip()]
            if lines and lines[-1].strip().endswith("sim>"):
                break
            time.sleep(0.5)
        for cmd in (f"at vu0 {deck}", "d 6 1", "d 5 10", "set cpu req"):
            send(cmd); time.sleep(0.7)
        send("go"); time.sleep(1.0)
        print(f"[{a.case}] deck launched", flush=True)

        deadline = time.time() + a.timeout
        while time.time() < deadline and not started:
            started = bool(JOB.search(pane()))
            time.sleep(0.5)
        print(f"[{a.case}] job-start={started}", flush=True)

        # The exact sequence that was observed to launch the queued job.
        time.sleep(8.0)
        send_slow("ДАЙ А0"); time.sleep(3.0)
        send_slow("НОМВ"); launched = True
        print(f"[{a.case}] operator handoff sent", flush=True)

        # Poll prn0 ONLY.  No further console input.
        deadline = time.time() + a.timeout
        while time.time() < deadline:
            txt = prn.read_text(encoding="utf-8", errors="replace") if prn.is_file() else ""
            if DONE in txt and RESULT.search(txt):
                break
            time.sleep(2.0)
        console = pane()
    finally:
        (RUNS / f"console_{a.case}.txt").write_text(console, encoding="utf-8")
        subprocess.run(["tmux", "kill-session", "-t", session], env=env)

    prn_txt = prn.read_text(encoding="utf-8", errors="replace") if prn.is_file() else ""
    ok = bool(DONE in prn_txt and RESULT.search(prn_txt))
    verdict = {
        "case": a.case, "deck": str(deck), "image": str(Path(a.image).resolve()),
        "emulator_sha": sha, "boot": boot, "job_start": started,
        "operator_handoff": launched, "result_21_line": bool(RESULT.search(prn_txt)),
        "completion_marker": DONE in prn_txt, "product_gate": "PASS" if ok else "N/A",
        "prn0": str(prn), "console": str(RUNS / f"console_{a.case}.txt"),
    }
    (RUNS / f"verdict_{a.case}.json").write_text(
        json.dumps(verdict, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"===== {a.case} ===== product={verdict['product_gate']}", flush=True)
    for line in prn_txt.splitlines():
        if RESULT.match(line) or DONE in line:
            print("  " + line.strip(), flush=True)
    return 0 if ok else 3


if __name__ == "__main__":
    sys.exit(main())
