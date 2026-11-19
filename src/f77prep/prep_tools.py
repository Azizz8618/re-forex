#!/usr/bin/env python3
"""Host-side helpers for the two-pass F77PREP pipeline (stage E3, v2).

F77PREP itself is a Fortran program compiled by FOREX 2.02.  This module
only builds the two dispak decks and turns the numeric records printed by
F77PREP back into lowered fixed-form Fortran with C@ source-map anchors.

Subcommands:
    deck1   SRC FTN OUT      pass-1 deck: F77PREP with injected DATA + run
    records IN OUT           parse 777001/777002/777003 records -> JSON
    lower   SRC JSON OUT     apply records to SRC -> lowered.f77
    deck2   LOW OUT [DATA]   pass-2 deck: compile+run lowered.f77,
                             optional data cards between *execute and *end file

The injection replaces the `C@@DATA@@` marker in the Fortran source with
`DATA NL /n/` and `DATA C /.../` (card images as ASCII character codes).
No Fortran READ unit is required in pass 1.

v2 rule set emitted by F77PREP (777001 <line> <rule> <itype>):
    0 keep, 1 IMPLICIT NONE, 2 SAVE, 3 PRINT *,vars,
    4 READ(*,*,END=LL) var, 5 DO WHILE (cond), 6 END DO,
    7 CHARACTER*n var, 8 var='literal'.
Rule 3 also emits 777002 <pos> <char-code> with the variable list; all
other details are recovered here from the original source line.  Record
formats 777001/777002/777003 and C@ anchors are preserved from v1.
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

# Label ranges reserved by the lowering (source labels are avoided).
FMT_BASE = 9000        # PRINT/READ FORMAT statements
LOOP_BASE = 7000       # DO WHILE top / bottom (two per loop)
READ_BASE = 9500       # unitless READ <fmt>,var (E1: READ 10,X)

INT_FIRST = "IJKLMN"   # implicit INTEGER letters -> I10, otherwise F12.4
CHAR_LIMIT = 4         # only 1..4 character literals are supported


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


def _used_labels(lines):
    used = set()
    for line in lines:
        m = re.match(r"\s*(\d{1,5})\s+\S", line)
        if m:
            used.add(int(m.group(1)))
    return used


def _label_field(number):
    """Right-justified label in fixed-form columns 1-5."""
    if number > 99999:
        raise SystemExit("label too long: %d" % number)
    return "%5d" % number


def build_lowered(src_path, json_path):
    lines = read_source(src_path)
    data = json.load(open(json_path, encoding="utf-8"))
    rules = {r["line"]: r for r in data["records"]}
    varmap = {int(k): decode_var([v[i] for i in sorted(v)]).strip()
              for k, v in data["varcodes"].items()}

    used = _used_labels(lines)

    def alloc(base, step=1):
        n = base
        while n in used or n > 99999:
            n += step
        used.add(n)
        return n

    fmt_counter = [FMT_BASE]
    loop_counter = [LOOP_BASE]
    read_counter = [READ_BASE]
    formats = []            # (label, descriptor-without-1X) collected for END
    char_rename = {}        # source CHARACTER name -> INTEGER substitute
    loop_stack = []         # (top, bottom) of open DO WHILE loops
    out = []

    # Pass A: collect CHARACTER declarations so PRINT can choose A4.
    for n, line in enumerate(lines, 1):
        if rules.get(n, {}).get("rule") == 7:
            m = re.search(r"CHARACTER\s*\*\s*(\d+)\s+([A-Za-z]\w*)", line, re.I)
            if m:
                name = m.group(2)
                char_rename[name] = ("I" + name)[:6]

    # Pass B: lower each classified line.
    for n, line in enumerate(lines, 1):
        r = rules.get(n, {"rule": 0, "itype": 0})
        rule, itype = r["rule"], r["itype"]
        orig = line.strip()

        if rule == 0:
            out.append(line)

        elif rule in (1, 2):
            out.append("C@ %s -> (removed)" % orig)

        elif rule == 3:
            varlist = varmap.get(n, "")
            if not varlist:
                raise SystemExit("no variable codes for PRINT * on line %d" % n)
            names = [t.strip() for t in varlist.split(",") if t.strip()]
            if not names:
                raise SystemExit("empty variable list for PRINT * on line %d" % n)
            outnames, specs = [], []
            for v in names:
                if v in char_rename:
                    outnames.append(char_rename[v])
                    specs.append("A4")
                elif v[0].upper() in INT_FIRST:
                    outnames.append(v)
                    specs.append("I10")
                else:
                    outnames.append(v)
                    specs.append("F12.4")
            lab = alloc(fmt_counter[0])
            fmt_counter[0] = lab + 1
            new = "PRINT %d,%s" % (lab, ",".join(outnames))
            out.append("C@ %s -> %s" % (orig, new))
            out.append("      " + new)
            formats.append((lab, "1X," + ",".join(specs)))

        elif rule == 4:
            m = re.search(r"END\s*=\s*\d+\s*\)\s*([A-Za-z]\w*)", line, re.I)
            var = m.group(1) if m else "X"
            lab = alloc(read_counter[0])
            read_counter[0] = lab + 1
            spec = "I10" if var[0].upper() in INT_FIRST else "F12.4"
            new = "READ %d,%s" % (lab, var)
            out.append("C@ %s -> %s  (END= label removed)" % (orig, new))
            out.append("      " + new)
            formats.append((lab, spec))

        elif rule == 5:
            m = re.search(r"DO\s+WHILE\s*\((.*)\)\s*$", line, re.I)
            if not m:
                raise SystemExit("cannot parse DO WHILE on line %d" % n)
            cond = m.group(1).strip()
            top = alloc(loop_counter[0], 2)
            used.add(top + 1)
            loop_counter[0] = top + 2
            bottom = top + 1
            new = "%d CONTINUE / IF (.NOT.(%s)) GO TO %d" % (top, cond, bottom)
            out.append("C@ %s -> %s" % (orig, new))
            out.append("%s CONTINUE" % _label_field(top))
            out.append("      IF (.NOT.(%s)) GO TO %d" % (cond, bottom))
            loop_stack.append((top, bottom))

        elif rule == 6:
            if not loop_stack:
                raise SystemExit("END DO without DO WHILE on line %d" % n)
            top, bottom = loop_stack.pop()
            new = "GO TO %d / %d CONTINUE" % (top, bottom)
            out.append("C@ %s -> %s" % (orig, new))
            out.append("      GO TO %d" % top)
            out.append("%s CONTINUE" % _label_field(bottom))

        elif rule == 7:
            m = re.search(r"CHARACTER\s*\*\s*(\d+)\s+([A-Za-z]\w*)", line, re.I)
            if not m:
                raise SystemExit("cannot parse CHARACTER on line %d" % n)
            iname = char_rename[m.group(2)]
            new = "INTEGER %s" % iname
            out.append("C@ %s -> %s" % (orig, new))
            out.append("      " + new)

        elif rule == 8:
            m = re.match(r"\s*([A-Za-z]\w*)\s*=\s*'(.*)'", line)
            if not m:
                raise SystemExit("cannot parse string assignment on line %d" % n)
            name, literal = m.group(1), m.group(2)
            if len(literal) < 1 or len(literal) > CHAR_LIMIT:
                raise SystemExit(
                    "string literal on line %d is %d chars (limit 1-%d)"
                    % (n, len(literal), CHAR_LIMIT))
            iname = char_rename.get(name, ("I" + name)[:6])
            new = "DATA %s/%dH%s/" % (iname, len(literal), literal)
            out.append("C@ %s -> %s" % (orig, new))
            out.append("      " + new)

        else:
            raise SystemExit("unknown rule %d on line %d" % (rule, n))

    if loop_stack:
        raise SystemExit("unbalanced DO WHILE / END DO")

    # Append all FORMAT statements just before the final END.
    if formats:
        end_at = None
        for i in range(len(out) - 1, -1, -1):
            if out[i].strip().upper().startswith("END"):
                end_at = i
                break
        insert = []
        for lab, spec in formats:
            fmt = "%d FORMAT(%s)" % (lab, spec)
            insert.append("C@ (end of program) -> %s" % fmt)
            insert.append("%s FORMAT(%s)" % (_label_field(lab), spec))
        if end_at is None:
            out += insert
        else:
            out[end_at:end_at] = insert

    return "\n".join(out) + "\n"


def make_deck2(low_path, data_path=None):
    low = open(low_path, encoding="utf-8").read()
    deck = PASSPORT + [
        "*name Target",
        "*call yesmemory",
        "*perso:602300",
        "*no list",
        "*no load list",
        "*forex",
    ]
    body = deck + [low.rstrip("\n"), "*execute"]
    if data_path:
        body += [ln.rstrip("\n") for ln in open(data_path, encoding="utf-8").read().splitlines()]
    body += ["*end file", "``````", "еконец"]
    return "\n".join(body) + "\n"


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
        data = sys.argv[4] if len(sys.argv) > 4 else None
        open(sys.argv[3], "w", encoding="utf-8").write(make_deck2(sys.argv[2], data))
    else:
        raise SystemExit("unknown command: " + cmd)


if __name__ == "__main__":
    main()
