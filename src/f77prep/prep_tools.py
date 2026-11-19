#!/usr/bin/env python3
"""Host-side helpers for the two-pass F77PREP pipeline (stage E3).

F77PREP itself is a Fortran program compiled by FOREX 2.02.  This module
only builds the two dispak decks and turns the numeric records printed by
F77PREP back into lowered fixed-form Fortran with C@ source-map anchors.

Subcommands:
    deck1   SRC FTN OUT     pass-1 deck: F77PREP with injected DATA + run
    records IN OUT          parse 777001/777002/777003 records -> JSON
    lower   SRC JSON OUT    apply records to SRC -> lowered.f77
    deck2   LOW OUT         pass-2 deck: compile+run lowered.f77

The injection replaces the `C@@DATA@@` marker in the Fortran source with
`DATA NL /n/` and `DATA C /.../` (card images as ASCII character codes).
No Fortran READ unit is required: E1 has not identified one that consumes
the post-*execute card stream on FOREX 2.02.
"""

import json
import re
import sys

NMAX = 20          # must match C(72,20) in F77PREP.FTN
WIDTH = 72
MARK_REC = 777001
MARK_VAR = 777002
MARK_END = 777003

PASSPORT = [
    "шифр 419999 зс5^",
    "лен 60(2348)^",
    "ееВ1а3",
]


def read_source(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    if len(lines) > NMAX:
        raise SystemExit("too many source lines: %d > %d" % (len(lines), NMAX))
    out = []
    for n, line in enumerate(lines, 1):
        line = line.rstrip()
        if len(line) > WIDTH:
            raise SystemExit("line %d longer than %d columns" % (n, WIDTH))
        out.append(line)
    return out


def card_codes(lines):
    codes = []
    for line in lines:
        c = [ord(ch) & 0x7F for ch in line]
        c += [32] * (WIDTH - len(c))          # pad with ASCII space
        codes += c
    codes += [0] * (NMAX * WIDTH - len(codes))  # DATA must cover whole array
    return codes


def data_statement(name, values, per_line=12):
    chunks = [values[i:i + per_line] for i in range(0, len(values), per_line)]
    out = []
    for i, chunk in enumerate(chunks):
        head = "      DATA %s /" % name if i == 0 else "     1"
        tail = "/" if i == len(chunks) - 1 else ","
        out.append(head + ",".join(str(v) for v in chunk) + tail)
    return "\n".join(out)


def make_deck1(src_path, ftn_path):
    lines = read_source(src_path)
    ftn = open(ftn_path, encoding="utf-8").read()
    if "C@@DATA@@" not in ftn:
        raise SystemExit("F77PREP.FTN has no C@@DATA@@ marker")
    injected = "      DATA NL /%d/\n%s" % (len(lines),
                                            data_statement("C", card_codes(lines)))
    ftn = ftn.replace("C@@DATA@@", injected)
    deck = PASSPORT + [
        "*name Prep1",
        "*call yesmemory",
        "*perso:602300",
        "*no list",
        "*no load list",
        "*forex",
    ]
    return "\n".join(deck + [ftn.rstrip("\n")] +
                     ["*execute", "*end file", "``````", "еконец"]) + "\n"


def parse_records(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    recs, varcodes, summary = [], {}, None
    for line in text.splitlines():
        m = re.match(r"\s*%d\s+(\d+)\s+(\d+)\s+(\d+)\s*$" % MARK_REC, line)
        if m:
            recs.append({"line": int(m.group(1)), "rule": int(m.group(2)),
                         "itype": int(m.group(3))})
            continue
        m = re.match(r"\s*%d\s+(\d+)\s+(\d+)\s+(\d+)\s*$" % MARK_VAR, line)
        if m:
            varcodes.setdefault(int(m.group(1)), {})[int(m.group(2))] = int(m.group(3))
            continue
        m = re.match(r"\s*%d\s+(\d+)\s+(\d+)\s*$" % MARK_END, line)
        if m:
            summary = {"lines": int(m.group(1)), "rewrites": int(m.group(2))}
    if not recs or summary is None:
        raise SystemExit("no F77PREP records found in %s" % path)
    return {"records": recs, "varcodes": varcodes, "summary": summary}


def decode_var(codes):
    return "".join(chr(c) for c in codes if 32 <= c < 127)


def build_lowered(src_path, json_path):
    lines = read_source(src_path)
    data = json.load(open(json_path, encoding="utf-8"))
    rules = {r["line"]: r for r in data["records"]}
    varmap = {int(k): decode_var([v[i] for i in sorted(v)])
              for k, v in data["varcodes"].items()}
    fmt = None
    out = []
    for n, line in enumerate(lines, 1):
        r = rules.get(n, {"rule": 0, "itype": 0})
        rule, itype = r["rule"], r["itype"]
        orig = line.strip()
        if rule == 0:
            out.append(line)
        elif rule in (1, 2):
            out.append("C@ %s -> (removed)" % orig)
        elif rule == 3:
            var = varmap.get(n, "")
            if not var:
                raise SystemExit("no variable codes for PRINT * on line %d" % n)
            new = "PRINT 9000,%s" % var
            out.append("C@ %s -> %s" % (orig, new))
            out.append("      " + new)
            fmt = "9000 FORMAT(1X,%s)" % ("I10" if itype == 1 else "F12.4")
        else:
            raise SystemExit("unknown rule %d on line %d" % (rule, n))
    if fmt:
        anchor = "C@ (end of program) -> %s" % fmt
        # Insert the FORMAT before the final END statement when possible.
        end_at = None
        for i in range(len(out) - 1, -1, -1):
            if out[i].strip().upper().startswith("END"):
                end_at = i
                break
        if end_at is None:
            out += [anchor, " " + fmt]
        else:
            out[end_at:end_at] = [anchor, " " + fmt]
    return "\n".join(out) + "\n"


def make_deck2(low_path):
    low = open(low_path, encoding="utf-8").read()
    deck = PASSPORT + [
        "*name Target",
        "*call yesmemory",
        "*perso:602300",
        "*no list",
        "*no load list",
        "*forex",
    ]
    return "\n".join(deck + [low.rstrip("\n")] +
                     ["*execute", "*end file", "``````", "еконец"]) + "\n"


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: prep_tools.py {deck1|records|lower|deck2} ...")
    cmd = sys.argv[1]
    if cmd == "deck1":
        open(sys.argv[4], "w", encoding="utf-8").write(
            make_deck1(sys.argv[2], sys.argv[3]))
    elif cmd == "records":
        json.dump(parse_records(sys.argv[2]),
                  open(sys.argv[3], "w", encoding="utf-8"), ensure_ascii=False)
    elif cmd == "lower":
        open(sys.argv[4], "w", encoding="utf-8").write(
            build_lowered(sys.argv[2], sys.argv[3]))
    elif cmd == "deck2":
        open(sys.argv[3], "w", encoding="utf-8").write(make_deck2(sys.argv[2]))
    else:
        raise SystemExit("unknown command: " + cmd)


if __name__ == "__main__":
    main()
