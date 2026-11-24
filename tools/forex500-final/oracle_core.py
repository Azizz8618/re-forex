#!/usr/bin/env python3
"""C-dispak ORACLE (oracle only): CORE dump at an arbitrary PC."""
import os, shutil, subprocess, sys
from pathlib import Path
WS = Path(__file__).resolve().parent.parent
DISPAK = "/home/azizz/Yandex.Disk/dispak/build/dispak/dispak"
SHARE = Path("/usr/local/share/besm6")
case, image, deck, pc = sys.argv[1:5]
d = WS / "oracle" / case
if d.exists(): shutil.rmtree(d)
(d / "disks").mkdir(parents=True); (d / "home").mkdir()
shutil.copy2(image, d / "disks" / "2048")
for f in ("2053", "2099"): shutil.copy2(SHARE / f, d / "disks" / f)
shutil.copy2(deck, d / "job.b6")
env = dict(os.environ, HOME=str(d / "home"), BESM6_PATH=str(d / "disks"),
           BESM6_DD_DEBUG="1", BESM6_CORE_ON_PC=pc, BESM6_CORE_SKIP="6",
           BESM6_TRACE_COUNTER="0")
with open(d / "out.txt", "wb") as f:
    r = subprocess.run(["timeout", "-s", "KILL", "90", DISPAK, "-l", "job.b6"],
                       cwd=d, env=env, stdout=f, stderr=subprocess.STDOUT)
print("rc", r.returncode, "core", [p.name for p in d.glob("core*")])
