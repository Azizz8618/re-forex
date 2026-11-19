#!/usr/bin/env python3
"""E1 experiments from docs/plan-f77/03-fortran-path.md Appendix B.

Regenerates every deck under tests/plan-f77/e1/ and runs it through dispak,
capturing stdout+stderr into out.txt next to each task.b6.

Usage:  python3 tests/plan-f77/e1/make_experiments.py
"""
from pathlib import Path
import os
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[3]          # re-forex
E1 = ROOT / "tests" / "plan-f77" / "e1"
LOG = ROOT / "logs" / "plan_f77_experiments.txt"
DISPAK = os.environ.get(
    "DISPAK_BIN", "/home/azizz/Yandex.Disk/dispak/build/dispak/dispak")
ETALON = Path(os.environ.get("ETALON", "/usr/local/share/besm6/2348"))
TMPROOT = Path(os.environ.get(
    "TMPROOT", "/tmp/.private/azizz/opencode"))

# All FOREX / Monitor-80 error spellings found so far (see plan 03, §0).
ERR_RE = re.compile(
    r"ERR\s+\d+|ОШИБКА|НЕДОПУСТИМ|АТТ\s+\d+|ТИП ОП-ДА|ДОЛЖНА БЫТЬ|"
    r"I/О-ЕRRОR|I/O-ERROR|ОШ\.В ИНФ|ОШ\. ТРАНСЛЯТОРА|НЕТ КАНАЛА|"
    r"ИСПОРЧЕН РЕКОРД|ОШИБКА УПП|ОШИБКА СПЕЦИФИКАЦИИ|UNRECOGNIZED|"
    r"БЫЛИ ОШИБКИ"
)

header = (
    "шифр 419999 зс5^\n"
    "лен 41(2048)^\n"
    "eeв1а3\n"
    "*name {name}\n"
    "*call yesmemory\n"
)


def deck(name, fortran, *, after="*execute\n", extra="", path=None):
    """Build a standard deck text."""
    text = header.format(name=name) + extra + "*no list\n*forex\n"
    text += "".join(line + "\n" for line in fortran)
    text += after + "*end file\n``````\nеконец\n"
    d = path or (E1 / "_scratch" / name)
    d.mkdir(parents=True, exist_ok=True)
    p = d / "task.b6"
    p.write_text(text, encoding="utf-8")
    return d


def run(d, *, env=None, args=None, diskdir=None):
    """Run dispak in d, save out.txt, return combined output + return code."""
    e = os.environ.copy()
    if diskdir:
        e["BESM6_PATH"] = str(diskdir) + ":/usr/local/share/besm6"
    if env:
        e.update(env)
    cmd = [DISPAK] + (args or []) + ["task.b6"]
    r = subprocess.run(cmd, cwd=str(d), env=e, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
    out = r.stdout.decode("utf-8", "replace")
    (d / "out.txt").write_text(out, encoding="utf-8")
    return out, r.returncode


def classify(out):
    m = ERR_RE.search(out)
    if m:
        return "ERROR: " + m.group(0).strip()
    if "КОНЕЦ ЗАДАЧИ" in out:
        return "OK (no error form, task end)"
    return "???? no result"


def report(case, out, rc, note=""):
    marks = sorted(set(m.group(0).strip() for m in ERR_RE.finditer(out)))
    lines = [out.strip()]
    log.append(
        "=== %s ===\n  rc=%d  verdict=%s\n  error forms: %s\n  %s\n"
        % (case, rc, classify(out), ", ".join(marks) or "-", note)
    )
    return lines


log = []

# ---------------------------------------------------------------- experiment 1
# 1a. Canonical FORTRAN card read: READ <fmt> (no unit) after *execute.
d = deck("read_nounit", [
    "      READ 10,X", "   10 FORMAT(F8.2)",
    "      PRINT 20,X", "   20 FORMAT(1X,F8.2)",
    "      STOP", "      END",
], after="*execute\n  3.50\n", path=E1 / "units" / "read_nounit")
out, rc = run(d)
report("E1/units/read_nounit", out, rc, "карта 3.50 прочитана, напечатано 3.50")
for i, line in enumerate(out.splitlines(), 1):
    if "3.50" in line:
        log.append("  evidence: %s/out.txt:%d %s\n"
                   % (d.relative_to(ROOT), i, line.strip()[:100]))
        break

# 1b. Explicit unit READ after *execute: units 1,2,5,6,10,40 (+45,54 control).
for u in (1, 2, 5, 6, 10, 40, 45, 54):
    d = deck("read_u%d" % u, [
        "      READ(%d,10) X" % u, "   10 FORMAT(F8.2)",
        "      PRINT 20,X", "   20 FORMAT(1X,F8.2)",
        "      STOP", "      END",
    ], after="*execute\n  3.50\n", path=E1 / "units" / ("read_u%d" % u))
    out, rc = run(d)
    report("E1/units/read_u%d" % u, out, rc, "READ(%d,10), карта данных 3.50" % u)
    found = False
    for i, line in enumerate(out.splitlines(), 1):
        if any(k in line for k in ("ИСПОРЧЕН РЕКОРД", "ОШ.В ИНФ.СЛ.ЭКСТ",
                                   "НЕТ КАНАЛА", "LUN 1 ")):
            log.append("  evidence: %s/out.txt:%d %s\n"
                       % (d.relative_to(ROOT), i, line.strip()[:100]))
            found = True
            break
    if not found:
        log.append("  evidence: %s/out.txt (3.50 не напечатано)\n"
                   % d.relative_to(ROOT))

# 1c. Explicit unit WRITE. Units 1,2,5,6,10,40,45,54.
for u in (1, 2, 5, 6, 10, 40, 45, 54):
    d = deck("write_u%d" % u, [
        "      WRITE(%d,10) 12345" % u, "   10 FORMAT(1X,I6)",
        "      STOP", "      END",
    ], path=E1 / "units" / ("write_u%d" % u))
    out, rc = run(d)
    report("E1/units/write_u%d" % u, out, rc, "WRITE(%d,10) 12345" % u)
    for i, line in enumerate(out.splitlines(), 1):
        if "12345" in line or ERR_RE.search(line):
            log.append("  evidence: %s/out.txt:%d %s\n"
                       % (d.relative_to(ROOT), i, line.strip()[:100]))
            break

# 1d. Host-level redirection of the terminal unit 54 (shell > and dispak -o).
d = deck("write_redirect", [
    "      WRITE(54,10) 12345", "   10 FORMAT(1X,I6)",
    "      PRINT 20, 6789", "   20 FORMAT(1X,I6)",
    "      STOP", "      END",
], path=E1 / "units" / "write_redirect")
out, rc = run(d, args=["-o", "dispak_o.txt"])
(d / "shell_redirect.txt").write_text(out, encoding="utf-8")
report("E1/units/write_redirect", out, rc,
       "shell '>' captured both WRITE(54) and PRINT; dispak -o creates no file "
       "in this build (pout_file is used only by --decode-output)")
for i, line in enumerate(out.splitlines(), 1):
    if "12345" in line:
        log.append("  evidence: %s/out.txt:%d %s (PRINT 6789 on next line)\n"
                   % (d.relative_to(ROOT), i, line.strip()[:100]))
        break

# ---------------------------------------------------------------- experiment 2
GOST_TAB = {}
_rows = [
    "0017 0133 0134 0034 0127 0126 0121 0033",
    "0022 0023 0031 0012 0015 0013 0016 0014",
    "0000 0001 0002 0003 0004 0005 0006 0007",
    "0010 0011 0037 0026 0035 0025 0036 0136",
    "0021 0040 0042 0061 0077 0045 0100 0101",
    "0055 0102 0103 0052 0104 0054 0105 0056",
    "0060 0106 0107 0110 0062 0111 0112 0113",
    "0065 0063 0114 0027 0175 0030 0115 0132",
    "0032 0040 0042 0061 0077 0045 0100 0101",
    "0055 0102 0103 0052 0104 0054 0105 0056",
    "0060 0106 0107 0110 0062 0111 0112 0113",
    "0065 0063 0114 0125 0017 0123 0017",
]
for i, row in enumerate(_rows):
    for j, tok in enumerate(row.split()):
        GOST_TAB[0x20 + 8 * i + j] = int(tok, 8)


def oddpar(c):
    c = (c ^ (c >> 4)) & 0xF
    c = (c ^ (c >> 2)) & 0x3
    c = (c ^ (c >> 1)) & 0x1
    return 0 if c else 1


SRC = ["      X=1.0", "      PRINT 10,X", "   10 FORMAT(1X,F8.2)",
       "      STOP", "      END"]

# 2a. plain ASCII text in punch.in0
d = E1 / "punchinsert" / "text_ascii"
d.mkdir(parents=True, exist_ok=True)
(d / "punch.in0").write_bytes(
    b"".join(s.ljust(120)[:120].encode("ascii") for s in SRC))
(d / "task.b6").write_text(
    header.format(name="PUNCHASCII") + "*no list\n*forex\n`0\n"
    "*execute\n*end file\n``````\nеконец\n", encoding="utf-8")
out, rc = run(d)
report("E1/punchinsert/text_ascii", out, rc, "punch.in0 = plain ASCII 120-byte records")
for i, line in enumerate(out.splitlines(), 1):
    if "ОШИБКА" in line:
        log.append("  evidence: %s/out.txt:%d %s\n"
                   % (d.relative_to(ROOT), i, line.strip()[:100]))
        break

# 2b. GOST bytes + odd parity in punch.in1
d = E1 / "punchinsert" / "text_gost"
d.mkdir(parents=True, exist_ok=True)
raw = b""
for s in SRC:
    for c in s.ljust(120)[:120]:
        g = GOST_TAB.get(ord(c), 0x17)
        raw += bytes((g | (oddpar(g) << 7),))
(d / "punch.in1").write_bytes(raw)
(d / "task.b6").write_text(
    header.format(name="PUNCHGOST") + "*no list\n*forex\n`1\n"
    "*execute\n*end file\n``````\nеконец\n", encoding="utf-8")
out, rc = run(d)
report("E1/punchinsert/text_gost", out, rc,
       "punch.in1 = GOST-10859 bytes with odd parity, 120-byte records")
for i, line in enumerate(out.splitlines(), 1):
    if "ОШИБКА" in line:
        log.append("  evidence: %s/out.txt:%d %s\n"
                   % (d.relative_to(ROOT), i, line.strip()[:100]))
        break

# 2c. control: dispak-generated binary punch object in punch.in3
d = E1 / "punchinsert" / "bin_control"
d.mkdir(parents=True, exist_ok=True)
(d / "gen_punch.b6").write_text(
    header.format(name="PUNCHGEN") + "*punch\n*no list\n*forex\n"
    + "".join(s + "\n" for s in SRC)
    + "*execute\n*end file\n``````\nеконец\n", encoding="utf-8")
e = os.environ.copy()
r = subprocess.run([DISPAK, "--punch-binary", "-c", "punch.in3", "gen_punch.b6"],
                   cwd=str(d), env=e, stdout=subprocess.PIPE,
                   stderr=subprocess.STDOUT)
(d / "gen_punch.out.txt").write_text(r.stdout.decode("utf-8", "replace"),
                                     encoding="utf-8")
(d / "task.b6").write_text(
    header.format(name="PUNCHBIN") + "*no list\n*forex\n"
    + "".join(s + "\n" for s in SRC)
    + "*execute\n`3\n*end file\n``````\nеконец\n", encoding="utf-8")
out, rc = run(d)
report("E1/punchinsert/bin_control", out, rc,
       "punch.in3 produced by dispak --punch-binary (binary punch object)")
for i, line in enumerate(out.splitlines(), 1):
    if line.strip() == "1.00":
        log.append("  evidence: %s/out.txt:%d %s\n"
                   % (d.relative_to(ROOT), i, line.strip()[:100]))
        break

# ---------------------------------------------------------------- experiment 3
d = E1 / "callfortran"
d.mkdir(parents=True, exist_ok=True)
workdisk = d / "2348"
if not workdisk.exists():
    r = subprocess.run(["bash", str(ROOT / "tests" / "install-forex-perso.sh"),
                        "--keep", "--disk=" + str(workdisk)],
                       cwd=str(ROOT), stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT)
    (d / "install.log").write_text(r.stdout.decode("utf-8", "replace"),
                                   encoding="utf-8")
    if r.returncode:
        log.append("E1/callfortran: install-forex-perso.sh rc=%d\n" % r.returncode)

b = deck("build_object", [
    "      SUBROUTINE HELLO", "      PRINT 10",
    "   10 FORMAT(1X,12H*CALL WORKS*)", "      RETURN", "      END",
], extra="*perso:602300\n",
    path=d / "build")
# the build deck needs the writable disk mounted on LUN 60
t = (d / "build" / "task.b6").read_text(encoding="utf-8")
t = t.replace("лен 41(2048)^\n", "лен 41(2048)^\nлен 60(2348-wr)^\n")
t = t.replace("*execute\n", "*to perso:602310\n")
(d / "build" / "task.b6").write_text(t, encoding="utf-8")
out, rc = run(d / "build", diskdir=d)
report("E1/callfortran/build_object", out, rc,
       "*forex -> Fortran subroutine HELLO -> *to perso:602310")
for i, line in enumerate(out.splitlines(), 1):
    if "004 ЗОН" in line or "004 ZON" in line:
        log.append("  evidence: %s/out.txt:%d %s\n"
                   % ((d / "build").relative_to(ROOT), i, line.strip()[:100]))
        break

c = deck("call_object", [
    "      CONTINUE",
], extra="*perso:602300\n*perso:602310,cont\n",
    path=d / "call")
t = (d / "call" / "task.b6").read_text(encoding="utf-8")
t = t.replace("лен 41(2048)^\n", "лен 60(2348)^\n")
t = t.replace("*no list\n*forex\n      CONTINUE\n", "*call hello\n")
(d / "call" / "task.b6").write_text(t, encoding="utf-8")
out, rc = run(d / "call", diskdir=d)
report("E1/callfortran/call_object", out, rc,
       "*call hello на Fortran-DMS-объекте из 0o2310 (без *forex)")
for i, line in enumerate(out.splitlines(), 1):
    if "WОRКS" in line or ("WORKS" in line and "NАМЕ" not in line):
        log.append("  evidence: %s/out.txt:%d %s\n"
                   % ((d / "call").relative_to(ROOT), i, line.strip()[:100]))
        break

# ---------------------------------------------------------------- experiment 4
dp = deck("double_precision", [
    "      DOUBLE PRECISION X,Y,Z", "      X=2.0D0", "      Y=SQRT(X)",
    "      Z=1.0D0/3.0D0", "      S=SQRT(2.0)", "      T=1.0/3.0",
    "      PRINT 10,Y", "   10 FORMAT(1X,D22.15)",
    "      PRINT 11,Z", "   11 FORMAT(1X,D22.15)",
    "      PRINT 20,S", "   20 FORMAT(1X,F20.15)",
    "      PRINT 21,T", "   21 FORMAT(1X,F20.15)",
    "      STOP", "      END",
], path=E1 / "precision" / "double")
out, rc = run(dp)
report("E1/precision/double", out, rc,
       "DSQRT через SQRT(DOUBLE), 1/3 в DP и SP; D22.15 / F20.15")
for i, line in enumerate(out.splitlines(), 1):
    if re.match(r"\s+1\.4142|\s+3\.3333|\s+0\.3333", line):
        log.append("  evidence: %s/out.txt:%d %s\n"
                   % (dp.relative_to(ROOT), i, line.strip()[:100]))

dpf = deck("dp_f_format", [
    "      DOUBLE PRECISION X", "      X=2.0D0",
    "      PRINT 10,X", "   10 FORMAT(1X,F16.12)",
    "      STOP", "      END",
], path=E1 / "precision" / "dp_f_format")
out, rc = run(dpf)
report("E1/precision/dp_f_format", out, rc,
       "FORMAT F с DOUBLE PRECISION — проверка дескриптора")
for i, line in enumerate(out.splitlines(), 1):
    if "I/О-ЕRRОR" in line:
        log.append("  evidence: %s/out.txt:%d %s\n"
                   % (dpf.relative_to(ROOT), i, line.strip()[:100]))
        break

cx = deck("complex_intrinsics", [
    "      COMPLEX Z,W", "      Z=(1.0,2.0)", "      W=(3.0,4.0)",
    "      Z=Z*W", "      PRINT 10,Z", "   10 FORMAT(1X,2F10.4)",
    "      Z=(3.0,4.0)", "      R=CABS(Z)", "      PRINT 11,R",
    "   11 FORMAT(1X,F10.4)", "      Z=CSQRT(Z)",
    "      PRINT 12,Z", "   12 FORMAT(1X,2F10.4)",
    "      STOP", "      END",
], path=E1 / "precision" / "complex")
out, rc = run(cx)
report("E1/precision/complex", out, rc,
       "(1+2i)*(3+4i) = -5+10i; CABS(3+4i)=5; CSQRT(3+4i)=2+i")
for i, line in enumerate(out.splitlines(), 1):
    if re.match(r"\s+-?5\.0000|\s+5\.0000|\s+2\.0000", line):
        log.append("  evidence: %s/out.txt:%d %s\n"
                   % (cx.relative_to(ROOT), i, line.strip()[:100]))

# ---------------------------------------------------------------- experiment 5
cases = {
    "charstar_original": [
        "      CHARACTER*10 S", "      S='ABCDE'", "      PRINT 10,S(2:4)",
        "   10 FORMAT(1X,A4)", "      STOP", "      END",
    ],
    "charstar_fixed": [
        "      CHARACTER*4 S", "      S='ABCD'", "      PRINT 10,S",
        "   10 FORMAT(1X,A4)", "      STOP", "      END",
    ],
    "hollerith_format": [
        "      PRINT 10", "   10 FORMAT(1X,4HABCD)",
        "      STOP", "      END",
    ],
    "quote_format": [
        "      PRINT 10", "   10 FORMAT(1X,'ABCD')",
        "      STOP", "      END",
    ],
    "hollerith_data_a4": [
        "      INTEGER I", "      DATA I/4HABCD/", "      PRINT 10,I",
        "   10 FORMAT(1X,A4)", "      STOP", "      END",
    ],
    "char_data_a4": [
        "      CHARACTER*4 S", "      DATA S/4HABCD/", "      PRINT 10,S",
        "   10 FORMAT(1X,A4)", "      STOP", "      END",
    ],
    "a4_wrong_type": [
        "      PRINT 10, 12345", "   10 FORMAT(1X,A4)",
        "      STOP", "      END",
    ],
}
for name, src in cases.items():
    d = deck(name, src, path=E1 / "strings" / name)
    out, rc = run(d)
    report("E1/strings/" + name, out, rc, " | ".join(src))
    for i, line in enumerate(out.splitlines(), 1):
        if ERR_RE.search(line) or "АВСD" in line or "ABCD" in line:
            log.append("  evidence: %s/out.txt:%d %s\n"
                       % (d.relative_to(ROOT), i, line.strip()[:100]))
            break

# ---------------------------------------------------------------- write log
LOG.parent.mkdir(parents=True, exist_ok=True)
LOG.write_text(
    "Лог E1-экспериментов (Приложение B, docs/plan-f77/03-fortran-path.md:450-461)\n"
    "Дата: 2026-11-19. dispak: %s\n"
    "Фильтр ошибкообнаружения: %s\n\n%s\n"
    % (DISPAK, ERR_RE.pattern, "\n".join(log)), encoding="utf-8")
print("done; log:", LOG)
print("\n".join(log[:40]))
