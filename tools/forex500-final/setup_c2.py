#!/usr/bin/env python3
"""Isolated SIMH workspace for the ftgost contour experiment.

Every attached disk is a workspace COPY. Stock `attach -n prn0/prn1` lines
are kept verbatim. md41 = our contour image; md45 = copied 2348 named 2048.
"""
import os
import re
import shutil
import sys
from pathlib import Path

WS = Path(__file__).resolve().parent.parent
IMG = WS / "images"
D45 = WS / "disk45"
RUNS = WS / "runs"
BASE = Path("/home/azizz/Yandex.Disk/simh/BESM6/OSZAGR/dispak.ini")
for d in (IMG, D45, RUNS, WS / "tmux"):
    d.mkdir(parents=True, exist_ok=True)

d45img = D45 / "2048"
if not d45img.exists():
    shutil.copy2("/usr/local/share/besm6/2348", d45img)


def make_ini(case, md41_image, trace=False):
    out = []
    for line in BASE.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^(\s*)(;?\s*)(attach\s+\S+\s+\S+\s+)(\S+)(.*)$", line)
        if m:
            ind, com, head, path, tail = m.groups()
            if com.strip():
                out.append(line)
                continue
            if re.search(r"\bprn0\b", head):
                out.append(f"{ind}{com}{head}{RUNS / ('localprn_' + case + '.txt')}{tail}")
                continue
            if re.search(r"\bprn1\b", head):
                out.append(line)  # stock -n prn, untouched
                continue
            if re.search(r"attach\s+-n\s+vu0\b", head):
                out.append(ind + "; " + head + path + tail)  # attach deck later
                continue
            if re.search(r"\bmd41\b", head):
                new = Path(md41_image).resolve()
            elif re.search(r"\bmd45\b", head):
                new = d45img
            else:
                p = Path(os.path.expanduser(path.strip()))
                new = IMG / p.name
                if p.is_file() and not new.exists():
                    shutil.copy2(p, new)
            line = f"{ind}{com}{head}{new}{tail}"
        if re.search(r"^load\s+", line.strip()):
            parts = line.split(None, 1)
            p = Path(os.path.expanduser(parts[1].strip()))
            if p.is_file():
                new = IMG / p.name
                if not new.exists():
                    shutil.copy2(p, new)
                line = "load " + str(new)
        if "console log=" in line:
            # Keep the SIMH console log off: `set cpu debug` echoes into it and
            # produces an 86 MB file. The driver captures the pane via tmux.
            line = "; " + line
        out.append(line)
    if trace:
        out.append(f"set debug {RUNS / ('debug_' + case + '.txt')}")
        out.append("set cpu debug")
    ini = RUNS / f"ini_{case}.ini"
    ini.write_text("\n".join(out) + "\n", encoding="utf-8")
    return ini


if __name__ == "__main__":
    case, md41 = sys.argv[1], sys.argv[2]
    trace = len(sys.argv) > 3 and sys.argv[3] == "trace"
    ini = make_ini(case, md41, trace=trace)
    print(ini)
    for l in ini.read_text().splitlines():
        if re.search(r"attach -e md(41|45)|attach -n prn0|attach -n vu0|^load |set debug|set cpu debug|console log", l):
            print("  " + l)
