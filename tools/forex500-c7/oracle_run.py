#!/usr/bin/env python3
"""C-dispak oracle (oracle only): MTR/CORE for a given image+deck."""
import os, shutil, subprocess, sys
from pathlib import Path
WS = Path(__file__).resolve().parent.parent
DISPAK = "/home/azizz/Yandex.Disk/dispak/build/dispak/dispak"
SHARE = Path("/usr/local/share/besm6")
case, image, deck = sys.argv[1], sys.argv[2], sys.argv[3]
mtr = sys.argv[4] if len(sys.argv) > 4 else ""
d = WS / "oracle" / case
if d.exists(): shutil.rmtree(d)
(d / "disks").mkdir(parents=True); (d / "home").mkdir()
shutil.copy2(image, d / "disks" / "2048")
for f in ("2053", "2099"):
    shutil.copy2(SHARE / f, d / "disks" / f)
shutil.copy2(deck, d / "job.b6")
env = dict(os.environ, HOME=str(d / "home"), BESM6_PATH=str(d / "disks"),
           BESM6_DD_DEBUG="1", BESM6_CORE_ON_PC="01770", BESM6_CORE_SKIP="6")
if mtr:
    for kv in mtr.split(","):
        k, v = kv.split("=", 1); env[k] = v
with open(d / "out.txt", "wb") as f:
    r = subprocess.run(["timeout", "-s", "KILL", "90", DISPAK, "-l", "job.b6"],
                       cwd=d, env=env, stdout=f, stderr=subprocess.STDOUT)
print("rc", r.returncode, "bytes", (d / "out.txt").stat().st_size)
