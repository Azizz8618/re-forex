#!/usr/bin/env python3
"""Host-side helpers for the two-pass F77PREP pipeline (stage E3, v3).

F77PREP itself is a Fortran program compiled by FOREX 2.02.  This module
builds the two dispak decks and turns the numeric records printed by
F77PREP back into lowered fixed-form Fortran with C@ source-map anchors.

Subcommands:
    deck1   SRC FTN OUT      pass-1 deck: F77PREP with injected DATA + run
    records IN OUT           parse 777001/777002/777003/777004 records -> JSON
    lower   SRC JSON OUT     apply records to SRC -> lowered.f77
                             (also writes OUT + ".777004.json" with the host
                              label allocations, record format 777004)
    deck2   LOW OUT [DATA]   pass-2 deck: compile+run lowered.f77,
                              optional data cards between *execute and *end

v3 infrastructure (M1-M4):
  * SEQ: the host writes a stable sequence number for every physical card
    and injects INTEGER SEQ(NLV); F77PREP keys all records by SEQ;
  * continuation: col 6 of a physical card glues cols 7-72 to the previous
    logical line (up to LL=132 chars); materialization re-splits if needed;
  * dynamic labels: generated labels are allocated from 90000..99999 with
    collision checks and logged as 777004 <seq> <rule> <pos> <code>;
  * variable lists: 777002 is kept for v2 compatibility, 777004 carries
    lists of the new rules keyed by (seq, rule).

Rules 0-8 keep their byte-for-byte lowering; rules 9-16/20 are new.
"""

import json
import re
import sys

NMAX = 20                 # legacy default, overridden by injected NLV
LL = 132                  # logical line width (M2)
WIDTH = 72                # physical card width
MARK_REC = 777001
MARK_VAR = 777002
MARK_END = 777003
MARK_AUX = 777004

PASSPORT = [
    "шифр 419999 зс5^",
    "лен 60(2348)^",
    "ееВ1а3",
]

# Legacy label bases (kept so that case1/case2 stay byte-identical).
FMT_BASE = 9000
LOOP_BASE = 7000
READ_BASE = 9500

# New labels (M3): reserved zone, never colliding with source labels.
LABEL_LO = 90000
LABEL_HI = 99999

INT_FIRST = "IJKLMN"       # implicit INTEGER letters -> I10
CHAR_LIMIT = 4             # v2 rule 7/8 limit; v3 rule 12 removes it

# Inline (rule 19) intrinsic families and their v3 rule numbers/ITYPE codes.
MAX_FUNCS = {"MAX", "MAX0", "MAX1", "AMAX0", "AMAX1", "DMAX1"}
MIN_FUNCS = {"MIN", "MIN0", "MIN1", "AMIN0", "AMIN1", "DMIN1"}
ABS_FUNCS = {"ABS", "IABS", "DABS"}
DIM_FUNCS = {"DIM", "IDIM"}
R19_FAMILY = {1: "MAX", 2: "MIN", 3: "ABS", 4: "DIM"}

# Fortran keywords and intrinsics: never treated as a truncatable identifier
# by the rule-20 collision check.
KEYWORDS = {
    "PROGRAM", "SUBROUTINE", "FUNCTION", "INTEGER", "REAL", "LOGICAL",
    "COMPLEX", "DOUBLE", "PRECISION", "CHARACTER", "DIMENSION", "COMMON",
    "DATA", "PARAMETER", "EQUIVALENCE", "ASSIGN", "IMPLICIT", "CONTINUE",
    "FORMAT", "PRINT", "READ", "WRITE", "WHILE", "GOTO", "GO", "STOP",
    "RETURN", "ENDDO", "BLOCK", "EXTERNAL", "INTRINSIC", "SAVE", "NONE", "CALL",
    "IF", "THEN", "ELSE", "ELSEIF", "ENDIF", "DO", "TO", "TYPE",
    "SQRT", "SIN", "COS", "EXP", "ABS", "MOD", "AMOD", "FLOAT", "IFIX",
    "INT", "SNGL", "CABS", "CSQRT", "CONJG", "CMPLX", "MAX", "MIN",
    "MAX0", "MIN0", "AMAX1", "AMIN1", "STRCAT", "SUBSTR", "ISTRCM",
    "F77PREP", "F77PRE",
}


# --------------------------------------------------------------------------
# source cards / logical lines (M1, M2)
# --------------------------------------------------------------------------

def read_cards(path):
    return [ln.rstrip() for ln in open(path, encoding="utf-8").read().splitlines()]


def logical_lines(cards):
    """Return (logical lines, SEQ of first physical card of each line)."""
    out, seqs = [], []
    for i, card in enumerate(cards, 1):
        cont = len(card) > 5 and card[5] != " "
        if cont and out:
            out[-1] = (out[-1] + card[6:WIDTH].rstrip())[:LL]
        else:
            out.append(card[:WIDTH].rstrip())
            seqs.append(i)
    if len(out) > 99999:
        raise SystemExit("too many logical lines: %d" % len(out))
    return out, seqs


def read_source(path):
    lines, _ = logical_lines(read_cards(path))
    return lines


def card_codes(lines, seqs, nlv):
    codes = []
    for line in lines:
        c = [ord(ch) & 0x7F for ch in line[:LL]]
        c += [32] * (LL - len(c))          # pad with ASCII space
        codes += c
    codes += [0] * (nlv * LL - len(codes))  # DATA must cover the whole array
    scodes = list(seqs) + [0] * (nlv - len(seqs))
    return codes, scodes


def data_statement(name, values, per_line=12):
    chunks = [values[i:i + per_line] for i in range(0, len(values), per_line)]
    out = []
    for i, chunk in enumerate(chunks):
        head = "      DATA %s /" % name if i == 0 else "     1"
        tail = "/" if i == len(chunks) - 1 else ","
        out.append(head + ",".join(str(v) for v in chunk) + tail)
    return "\n".join(out)


def make_deck1(src_path, ftn_path):
    cards = read_cards(src_path)
    lines, seqs = logical_lines(cards)
    nlv = max(len(lines), 1)
    ftn = open(ftn_path, encoding="utf-8").read()
    decl = ("      PARAMETER (NLV=%d,LL=%d)\n"
            "      INTEGER C(LL,NLV)\n"
            "      INTEGER SEQ(NLV)\n" % (nlv, LL))
    if "C@@DECL@@" not in ftn or "C@@DATA@@" not in ftn:
        raise SystemExit("F77PREP.FTN has no C@@DECL@@/C@@DATA@@ marker")
    ftn = ftn.replace("C@@DECL@@", decl.rstrip("\n"))
    codes, scodes = card_codes(lines, seqs, nlv)
    injected = "      DATA NL /%d/\n%s\n%s" % (
        nlv, data_statement("SEQ", scodes), data_statement("C", codes))
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


# --------------------------------------------------------------------------
# record parsing
# --------------------------------------------------------------------------

def parse_records(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    recs, varcodes, aux, summary = [], {}, [], None
    for line in text.splitlines():
        m = re.match(r"\s*%d\s+(\d+)\s+(\d+)\s+(\d+)\s*$" % MARK_REC, line)
        if m:
            recs.append({"seq": int(m.group(1)), "line": int(m.group(1)),
                         "rule": int(m.group(2)), "itype": int(m.group(3))})
            continue
        m = re.match(r"\s*%d\s+(\d+)\s+(\d+)\s+(\d+)\s*$" % MARK_VAR, line)
        if m:
            varcodes.setdefault(int(m.group(1)), {})[int(m.group(2))] = int(m.group(3))
            continue
        m = re.match(r"\s*%d\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$" % MARK_AUX, line)
        if m:
            aux.append({"seq": int(m.group(1)), "kind": int(m.group(2)),
                        "pos": int(m.group(3)), "value": int(m.group(4))})
            continue
        m = re.match(r"\s*%d\s+(\d+)\s+(\d+)\s*$" % MARK_END, line)
        if m:
            summary = {"lines": int(m.group(1)), "rewrites": int(m.group(2))}
    if not recs or summary is None:
        raise SystemExit("no F77PREP records found in %s" % path)
    return {"records": recs, "varcodes": varcodes, "aux": aux,
            "summary": summary}


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


def _descriptor(name, char_info, char_rename, dp_vars, typed_int=None):
    if name in char_info:
        _, n, w = char_info[name]
        rest = n - 6 * (w - 1)
        return ",".join(["A6"] * (w - 1) + ["A%d" % rest])
    if name in char_rename:
        return "A4"
    if name in dp_vars:
        return "D22.15"
    base = re.match(r"\s*([A-Za-z]\w*)", name)
    nm = base.group(1).upper() if base else name[0].upper()
    if typed_int and nm in typed_int:
        return "I10"
    return "I10" if nm[:1] in INT_FIRST else "F12.4"


def _outnames(name, char_info, char_rename):
    """Expand a CHARACTER word-array to its INTEGER word names."""
    if name in char_info:
        iname, _, w = char_info[name]
        if w == 1:
            return [iname]
        return ["%s(%d)" % (iname, k + 1) for k in range(w)]
    if name in char_rename:
        return [char_rename[name]]
    return [name]


LAST_LABEL_RECORDS = []       # populated by build_lowered (777004 host records)


def build_lowered(src_path, json_path):
    global LAST_LABEL_RECORDS
    LAST_LABEL_RECORDS = []
    cards = read_cards(src_path)
    lines, seqs = logical_lines(cards)

    def is_comment(ln):
        return ln[:1].upper() in ("C", "*")

    seq_to_line = {s: i for i, s in enumerate(seqs, 1)}
    data = json.load(open(json_path, encoding="utf-8"))
    rules = {}
    for r in data["records"]:
        idx = seq_to_line.get(r.get("seq", r.get("line")), r.get("line"))
        rules[idx] = r

    # F77PREP has no comment awareness: a ':' or a long identifier inside a
    # comment card must not become a rewrite or a rule-20 diagnostic.
    for _idx in range(1, len(lines) + 1):
        if is_comment(lines[_idx - 1]) and _idx in rules:
            rules[_idx]["rule"] = 0

    # ------------------------------------------------------------------
    # v3.1 host-side classification for rules 17/19/21/22.
    #
    # F77PREP.FTN itself is left at v3 byte-for-byte: the FOREX 2.02
    # translator has a hard memory ceiling and even a handful of extra
    # statements/DATA arrays overflow it on larger cases.  The host already
    # holds the full logical-line text and the DO WHILE/END DO structure, so
    # classifying these four constructs here is both cheaper and exact.
    # ------------------------------------------------------------------
    host_rules = {}
    dwh_stack = []
    for _idx, _line in enumerate(lines, 1):
        if is_comment(_line):
            continue
        _s = _line.strip().upper()
        if re.match(r"^DO\s+WHILE\s*\(", _s):
            dwh_stack.append(_idx)
            continue
        if re.match(r"^END\s*DO\b", _s):
            if dwh_stack:
                dwh_stack.pop()
            continue
        if re.match(r"^(EXTERNAL|INTRINSIC)\s", _s):
            host_rules[_idx] = 21
        elif re.search(r"\bCABS\s*\(", _s):
            host_rules[_idx] = 22
        else:
            for _fn in MAX_FUNCS | MIN_FUNCS | ABS_FUNCS | DIM_FUNCS:
                if re.search(r"\b%s\s*\(" % re.escape(_fn), _s):
                    host_rules[_idx] = 19
                    break
    for _idx in dwh_stack:
        host_rules[_idx] = 17
    for _idx, _rule in host_rules.items():
        if rules.get(_idx, {}).get("rule", 0) == 0:
            rules.setdefault(_idx, {"seq": seqs[_idx - 1] if _idx <= len(seqs) else _idx,
                                    "line": _idx, "itype": 0})
            itype = 0
            if _rule == 19:
                _s = lines[_idx - 1].strip().upper()
                for _k, _fam in R19_FAMILY.items():
                    if any(re.search(r"\b%s\s*\(" % re.escape(fn), _s)
                           for fn in (MAX_FUNCS if _fam == "MAX" else
                                      MIN_FUNCS if _fam == "MIN" else
                                      ABS_FUNCS if _fam == "ABS" else DIM_FUNCS)):
                        itype = _k
                        break
            rules[_idx]["rule"] = _rule
            rules[_idx]["itype"] = itype

    varmap = {int(k): decode_var([v[i] for i in sorted(v)]).strip()
              for k, v in data["varcodes"].items()}

    # 777004 aux records, keyed by (line, kind).
    aux4 = {}
    for a in data.get("aux", []):
        idx = seq_to_line.get(a["seq"], a["seq"])
        aux4.setdefault((idx, a["kind"]), {})[a["pos"]] = a["value"]

    def aux_list(idx, kind):
        vals = aux4.get((idx, kind), {})
        return decode_var([vals[p] for p in sorted(vals)]).strip() if vals else ""

    used = _used_labels(lines)

    def alloc(base, step=1):
        n = base
        while n in used or n > 99999:
            n += step
        used.add(n)
        return n

    nxt = [LABEL_LO]

    def dyn_alloc(seq, rule, pos):
        """M3: monotone label from the reserved 90000-99999 zone."""
        while nxt[0] in used and nxt[0] <= LABEL_HI:
            nxt[0] += 1
        if nxt[0] > LABEL_HI:
            raise SystemExit("dynamic label pool exhausted (90000-99999)")
        lab = nxt[0]
        nxt[0] += 1
        used.add(lab)
        LAST_LABEL_RECORDS.append({"seq": seq, "rule": rule,
                                   "pos": pos, "code": lab})
        return lab

    fmt_counter = [FMT_BASE]
    loop_counter = [LOOP_BASE]
    read_counter = [READ_BASE]
    formats = []            # (label, descriptor-without-1X)
    char_rename = {}        # source CHARACTER name -> INTEGER substitute
    char_info = {}          # v3 CHARACTER*n>4: name -> (iname, n, W)
    char_literals = {}      # source name -> last assigned literal (fold substrings)
    dp_vars = set()
    complex_vars = set()    # v3 rule 22: implicit COMPLEX from (a,b) assignment
    explicit_complex = set()
    typed_int = set()       # v3 rule 9: names declared INTEGER explicitly
    assign_map = {}         # v3 rule 15: assign variable -> [labels]
    equiv_map = {}          # v3 rule 16: name -> (base, offset)
    eq_decl_kill = set()
    loop_stack = []         # (top, bottom) of open DO WHILE loops
    out = []

    # ---------------- Pass A: declarations, implicit maps, rename maps -----
    for idx, line in enumerate(lines, 1):
        rule = rules.get(idx, {}).get("rule", 0)
        if rule == 7:
            m = re.search(r"CHARACTER\s*\*\s*(\d+)\s+([A-Za-z]\w*)", line, re.I)
            if m:
                char_rename[m.group(2)] = ("I" + m.group(2))[:6]
        elif rule == 12:
            m = re.search(r"CHARACTER\s*\*\s*(\d+)\s+([A-Za-z]\w*)", line, re.I)
            if not m:
                raise SystemExit("cannot parse CHARACTER on line %d" % idx)
            n = int(m.group(1))
            iname = ("I" + m.group(2))[:6]
            char_info[m.group(2)] = (iname, n, (n + 5) // 6)
            char_rename[m.group(2)] = iname
        if rule == 8:
            lm = re.match(r"\s*([A-Za-z]\w*)\s*=\s*'(.*)'", line)
            if lm:
                char_literals[lm.group(1)] = lm.group(2)
        m = re.search(r"DOUBLE\s+PRECISION\s+([A-Za-z]\w*(?:\s*,\s*[A-Za-z]\w*)*)",
                      line, re.I)
        if m:
            dp_vars.update(v.strip().upper() for v in m.group(1).split(","))
        # F77 implicit typing: VAR=(a,b) makes VAR COMPLEX.  Needed by the
        # rule-22 CABS lowering, which relies on native REAL()/AIMAG().
        for cm in re.finditer(r"(?<![A-Za-z0-9_])([A-Za-z]\w*)\s*=\s*\(([^()]*,[^()]*)\)",
                              line):
            complex_vars.add(cm.group(1).upper())
        dm = re.match(r"\s*COMPLEX\s+([A-Za-z]\w*)", line, re.I)
        if dm:
            explicit_complex.add(dm.group(1).upper())
        m = re.search(r"ASSIGN\s+(\d+)\s+TO\s+([A-Za-z]\w*)", line, re.I)
        if m:
            v = m.group(2).upper()
            lab = int(m.group(1))
            assign_map.setdefault(v, [])
            if lab not in assign_map[v]:
                assign_map[v].append(lab)
        for m in re.finditer(r"EQUIVALENCE\s*\(\s*([A-Za-z]\w*)\s*\(\s*(\d+)\s*\)"
                             r"\s*,\s*([A-Za-z]\w*)\s*\(\s*(\d+)\s*\)\s*\)",
                             line, re.I):
            base, bi, other, oi = m.group(1), int(m.group(2)), m.group(3), int(m.group(4))
            # Same-type check: both names must share the declared type.
            types = {}
            for dm in re.finditer(r"\b(INTEGER|REAL|LOGICAL|COMPLEX|DOUBLE\s+PRECISION)\b"
                                  r"([^\n]*)", "\n".join(lines), re.I):
                typ = "DP" if dm.group(1).upper().startswith("DOUBLE") else dm.group(1).upper()
                for nm in re.findall(r"[A-Za-z]\w*", dm.group(2)):
                    types[nm.upper()] = typ
            tb, to = types.get(base.upper()), types.get(other.upper())
            if tb and to and tb != to:
                raise SystemExit(
                    "EQUIVALENCE type mismatch on line %d: %s(%s) vs %s(%s)"
                    % (idx, base, tb, other, to))
            equiv_map[other.upper()] = (base, bi - oi)
            eq_decl_kill.add(other.upper())

    # ---------------- Pass B: lower each classified line -------------------
    for idx, line in enumerate(lines, 1):
        r = rules.get(idx, {"rule": 0, "itype": 0})
        rule, itype = r["rule"], r["itype"]
        orig = line.strip()
        seq = seqs[idx - 1] if idx <= len(seqs) else idx

        if rule == 0:
            if equiv_map:
                newline = line
                dm = re.match(r"\s*(INTEGER|REAL|LOGICAL|COMPLEX)\s+(.*)$", newline, re.I)
                if dm:
                    # declaration line: only drop the renamed variable, never
                    # rewrite its dimension as an array reference.
                    names = [x for x in re.split(r"\s*,\s*", dm.group(2).strip())
                             if x.split("(")[0].strip().upper() not in equiv_map]
                    newline = "      %s %s" % (dm.group(1), ",".join(names)) if names else \
                              "C@ (removed renamed declaration)"
                else:
                    for nm, (base, off) in equiv_map.items():
                        newline = re.sub(r"\b%s\s*\(\s*(\d+)\s*\)" % re.escape(nm),
                                         lambda mm: "%s(%d)" % (base, int(mm.group(1)) + off),
                                         newline, flags=re.I)
                if newline != line:
                    out.append("C@ %s -> %s" % (orig, newline.strip()))
                out.append(newline)
            else:
                out.append(line)

        elif rule in (1, 2):
            out.append("C@ %s -> (removed)" % orig)

        elif rule == 3:
            varlist = varmap.get(idx, "")
            if not varlist:
                raise SystemExit("no variable codes for PRINT * on line %d" % idx)
            names = [t.strip() for t in varlist.split(",") if t.strip()]
            if not names:
                raise SystemExit("empty variable list for PRINT * on line %d" % idx)
            outnames, specs = [], []
            for v in names:
                outnames += _outnames(v, char_info, char_rename)
                specs += _descriptor(v, char_info, char_rename, dp_vars, typed_int).split(",")
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

        elif rule in (5, 17):
            # rule 17: F77PREP flagged a DO WHILE with no matching END DO.
            # Both rules open the loop identically; unmatched loops (always
            # rule 17 from F77PREP) are closed automatically before END/STOP.
            m = re.search(r"DO\s+WHILE\s*\((.*)\)\s*$", line, re.I)
            if not m:
                raise SystemExit("cannot parse DO WHILE on line %d" % idx)
            cond = m.group(1).strip()
            top = alloc(loop_counter[0], 2)
            used.add(top + 1)
            loop_counter[0] = top + 2
            bottom = top + 1
            new = "%d CONTINUE / IF (.NOT.(%s)) GO TO %d" % (top, cond, bottom)
            out.append("C@ %s -> %s" % (orig, new))
            out.append("%s CONTINUE" % _label_field(top))
            out.append("      IF (.NOT.(%s)) GO TO %d" % (cond, bottom))
            loop_stack.append((top, bottom, rule == 17))

        elif rule == 6:
            if not loop_stack:
                raise SystemExit("END DO without DO WHILE on line %d" % idx)
            top, bottom, _auto = loop_stack.pop()
            new = "GO TO %d / %d CONTINUE" % (top, bottom)
            out.append("C@ %s -> %s" % (orig, new))
            out.append("      GO TO %d" % top)
            out.append("%s CONTINUE" % _label_field(bottom))

        elif rule == 7:
            m = re.search(r"CHARACTER\s*\*\s*(\d+)\s+([A-Za-z]\w*)", line, re.I)
            if not m:
                raise SystemExit("cannot parse CHARACTER on line %d" % idx)
            iname = char_rename[m.group(2)]
            new = "INTEGER %s" % iname
            out.append("C@ %s -> %s" % (orig, new))
            out.append("      " + new)

        elif rule == 8:
            m = re.match(r"\s*([A-Za-z]\w*)\s*=\s*'(.*)'", line)
            if not m:
                raise SystemExit("cannot parse string assignment on line %d" % idx)
            name, literal = m.group(1), m.group(2)
            if name in char_info:
                iname, n, w = char_info[name]
                # Emit all W words (last one padded with blanks) so that
                # CHARACTER*10 -> INTEGER IS(2) is fully initialized.
                words = [literal[6 * k:6 * k + 6].ljust(6) for k in range(w)]
                new = "; ".join("DATA %s(%d)/6H%s/" % (iname, k + 1, word)
                                for k, word in enumerate(words))
                out.append("C@ %s -> %s" % (orig, new))
                for k, word in enumerate(words):
                    out.append("      DATA %s(%d)/6H%s/" % (iname, k + 1, word))
                continue
            if len(literal) < 1 or len(literal) > CHAR_LIMIT:
                raise SystemExit(
                    "string literal on line %d is %d chars (limit 1-%d)"
                    % (idx, len(literal), CHAR_LIMIT))
            iname = char_rename.get(name, ("I" + name)[:6])
            new = "DATA %s/%dH%s/" % (iname, len(literal), literal)
            out.append("C@ %s -> %s" % (orig, new))
            out.append("      " + new)

        elif rule == 9:
            # typed IMPLICIT: drop and materialize explicit declarations
            m = re.search(r"IMPLICIT\s+(\w+)\s*\(([^)]*)\)", line, re.I)
            if not m:
                raise SystemExit("cannot parse IMPLICIT on line %d" % idx)
            typ = m.group(1).upper()
            letters = set()
            for part in m.group(2).split(","):
                if "-" in part:
                    a, b = part.split("-", 1)
                    letters.update(chr(c) for c in range(ord(a.upper()), ord(b.upper()) + 1))
                else:
                    letters.update(part.strip().upper())
            declared = set()
            for ln in lines:
                dm = re.match(r"\s*(INTEGER|REAL|LOGICAL|COMPLEX|DOUBLE\s+PRECISION)"
                              r"\s+([A-Za-z]\w*)", ln, re.I)
                if dm:
                    declared.add(dm.group(2).upper())
            stmts = []
            for ln in lines[1:]:
                for nm in re.findall(r"\b[A-Za-z]\w*\b", ln):
                    u = nm.upper()
                    if u in KEYWORDS or u in declared or u[:1] not in letters:
                        continue
                    if not re.search(r"\b%s\b" % re.escape(nm), ln):
                        continue
                    decl = {"INTEGER": "INTEGER", "REAL": "REAL", "LOGICAL": "LOGICAL",
                            "COMPLEX": "COMPLEX", "DOUBLE": "DOUBLE PRECISION"}.get(
                                typ, "INTEGER")
                    # only names that are actually assigned/used as scalars
                    if re.search(r"\b%s\s*=" % re.escape(nm), ln):
                        stmts.append("      %s %s" % (decl, nm[:6]))
                        declared.add(u)
                        if decl == "INTEGER":
                            typed_int.add(u)
            new = "(removed; explicit decls)"
            out.append("C@ %s -> %s" % (orig, new))
            out.extend(stmts)

        elif rule == 10:
            names = [t.strip() for t in aux_list(idx, 10).split(",") if t.strip()]
            if not names:
                m = re.search(r"READ\s*\(\s*\*\s*,\s*\*\s*\)\s*(.*)", line, re.I)
                raw = m.group(1) if m else re.sub(r"^\s*READ\s*\*\s*", "", line, flags=re.I)
                raw = re.split(r"[()]", raw)[0]
                names = [t.strip() for t in raw.split(",") if t.strip()]
            if not names:
                raise SystemExit("empty variable list for READ * on line %d" % idx)
            lab = dyn_alloc(seq, 10, 0)
            outnames, specs = [], []
            for v in names:
                outnames += _outnames(v, char_info, char_rename)
                specs += _descriptor(v, char_info, char_rename, dp_vars, typed_int).split(",")
            new = "READ %d,%s" % (lab, ",".join(outnames))
            out.append("C@ %s -> %s" % (orig, new))
            out.append("      " + new)
            formats.append((lab, ",".join(specs)))
            # rule 11: END=/ERR= sentinel checks (value emulation, see docs)
            first = outnames[0]
            for kind in (1, 2):
                if (idx, 11) in aux4 and aux4[(idx, 11)].get(kind) is not None:
                    target = aux4[(idx, 11)][kind]
                    sentinel = "-999999." if kind == 1 else "-888888."
                    chk = "IF (%s .EQ. %s) GO TO %d" % (first, sentinel, target)
                    out.append("C@ READ EARLY-EXIT -> %s" % chk)
                    out.append("      " + chk)

        elif rule == 12:
            m = re.search(r"CHARACTER\s*\*\s*(\d+)\s+([A-Za-z]\w*)", line, re.I)
            if not m:
                raise SystemExit("cannot parse CHARACTER on line %d" % idx)
            iname, n, w = char_info[m.group(2)]
            new = "INTEGER %s%s" % (iname, "(%d)" % w if w > 1 else "")
            out.append("C@ %s -> %s" % (orig, new))
            out.append("      " + new)

        elif rule == 13:
            cm = re.match(
                r"\s*([A-Za-z]\w*)\s*=\s*([A-Za-z]\w*)(?:\((\d+)\s*:\s*(\d+)\))?"
                r"\s*//\s*(?:'([^']*)'|([A-Za-z]\w*)(?:\((\d+)\s*:\s*(\d+)\))?)",
                line)
            if not cm:
                raise SystemExit("cannot parse // concatenation on line %d" % idx)
            dst = cm.group(1)
            dname = char_rename.get(dst, ("I" + dst)[:6])

            def operand(name, lo, hi, lit):
                """Resolve one // operand to (INTEGER word, length)."""
                if lit is not None:
                    tname = "IL%d" % (idx % 100)
                    out.append("      DATA %s/%dH%s/" % (
                        tname, len(lit), lit.ljust(6)) if len(lit) == 6 else
                        "      DATA %s/%dH%s/" % (tname, len(lit), lit))
                    return tname, len(lit)
                iname = char_rename.get(name, ("I" + name)[:6])
                if lo is not None:
                    tname = "IW%d" % (idx % 100)
                    call = "CALL SUBSTR(%s,%s,%s,%s)" % (iname, lo, hi, tname)
                    out.append("C@ %s -> %s" % (orig, call))
                    out.append("      " + call)
                    return tname, int(hi) - int(lo) + 1
                n = char_info.get(name, (None, 6, 1))[1]
                return iname, n

            a, la = operand(cm.group(2), cm.group(3), cm.group(4), None)
            b, lb = operand(cm.group(6), cm.group(7), cm.group(8), cm.group(5))
            new = "CALL STRCAT(%s,%s,%s,%d,%d)" % (a, b, dname, la, lb)
            out.append("C@ %s -> %s" % (orig, new))
            out.append("      " + new)

        elif rule == 14:
            m = re.match(r"\s*([A-Za-z]\w*)\s*=\s*([A-Za-z]\w*)\s*\(\s*(\d+)\s*:\s*(\d+)\s*\)",
                         line, re.I)
            if m:
                dst, src, lo, hi = m.group(1), m.group(2), m.group(3), m.group(4)
                new = "CALL SUBSTR(%s,%s,%s,%s)" % (
                    char_rename.get(src, ("I" + src)[:6]), lo, hi,
                    char_rename.get(dst, ("I" + dst)[:6]))
                out.append("C@ %s -> %s" % (orig, new))
                out.append("      " + new)
            else:
                # Substring used as an expression argument, e.g.
                # PRINT 10,S(2:4) -> CALL SUBSTR(IS,2,4,IW) ; PRINT 10,IW.
                sm = re.search(r"\b([A-Za-z]\w*)\s*\(\s*(\d+)\s*:\s*(\d+)\s*\)", line)
                if sm and sm.group(1) in char_info:
                    src, lo, hi = sm.group(1), int(sm.group(2)), int(sm.group(3))
                    tname = "IW%d" % (idx % 100)
                    newline = (line[:sm.start()] + tname + line[sm.end():]).rstrip()
                    lit = char_literals.get(src)
                    if lit is not None and 1 <= lo <= hi <= len(lit):
                        # Fold a substring of a statically known literal into
                        # an nH DATA word.  F77LIBR SUBSTR operates on arrays
                        # of ASCII codes, not on packed nH words, so it is not
                        # applicable to the rule-12 word representation.
                        sub = lit[lo - 1:hi].ljust(6)
                        data = "DATA %s/6H%s/" % (tname, sub)
                        out.append("C@ %s -> %s ; %s" % (orig, data, newline.strip()))
                        out.append("      " + data)
                    else:
                        call = "CALL SUBSTR(%s,%s,%s,%s)" % (
                            char_info[src][0], lo, hi, tname)
                        out.append("C@ %s -> %s ; %s" % (orig, call, newline.strip()))
                        out.append("      " + call)
                    out.append("      " + newline.strip())
                    continue
                cm = re.search(
                    r"IF\s*\(\s*([A-Za-z]\w*)\s*(\.EQ\.|\.NE\.)\s*([A-Za-z]\w*)\s*\)"
                    r"\s*(GO\s+TO\s+\d+)?", line, re.I)
                if not cm:
                    raise SystemExit("cannot parse string rule on line %d" % idx)
                a, op, b, action = (cm.group(1), cm.group(2).upper(),
                                    cm.group(3), cm.group(4))
                cmpvar = "KC%d" % (idx % 100)
                call = "%s = ISTRCM(%s,%s)" % (
                    cmpvar, char_rename.get(a, ("I" + a)[:6]),
                    char_rename.get(b, ("I" + b)[:6]))
                out.append("C@ %s -> %s" % (orig, call))
                out.append("      " + call)
                cond = ".EQ." if op == ".EQ." else ".NE."
                if action:
                    new = "IF (%s %s 0) %s" % (cmpvar, cond, action.upper())
                    out.append("      " + new)
                else:
                    out.append("C@ (action of %s must be lowered separately)" % orig)

        elif rule == 15:
            am = re.match(r"\s*ASSIGN\s+(\d+)\s+TO\s+([A-Za-z]\w*)", line, re.I)
            if am:
                lab, var = int(am.group(1)), am.group(2).upper()
                ordinal = assign_map.get(var, [lab]).index(lab) + 1
                new = "%s = %d" % (am.group(2), ordinal)
                out.append("C@ %s -> %s" % (orig, new))
                out.append("      " + new)
                continue
            gm = re.match(r"\s*GO\s+TO\s*(?:\(\s*([\d\s,]+)\s*\)\s*,\s*)?([A-Za-z]\w*)",
                          line, re.I)
            if not gm:
                raise SystemExit("cannot parse computed GO TO on line %d" % idx)
            var = gm.group(2).upper()
            labels = assign_map.get(var, [])
            if gm.group(1):
                labels = [int(x) for x in re.findall(r"\d+", gm.group(1))]
            if not labels:
                raise SystemExit("GO TO %s without ASSIGN on line %d" % (var, idx))
            out.append("C@ %s -> IF-chain over %s" % (orig, ",".join(map(str, labels))))
            for k, lab in enumerate(labels, 1):
                out.append("      IF (%s .EQ. %d) GO TO %d" % (gm.group(2), k, lab))

        elif rule == 16:
            out.append("C@ %s -> (removed; rename map applied)" % orig)

        elif rule == 19:
            # Inline expansion of MAX/MIN/ABS/DIM (F77PREP ITYPE = family).
            m = re.match(r"\s*([A-Za-z]\w*)\s*=\s*([A-Za-z]\w*)\s*\((.*)\)\s*$",
                         line, re.I)
            if not m:
                out.append(line)
                continue
            dst, fn, raw = m.group(1), m.group(2).upper(), m.group(3)
            args = [a.strip() for a in raw.split(",") if a.strip()]
            fam = R19_FAMILY.get(itype, fn[:3])
            out.append("C@ %s -> inline %s" % (orig, fam))
            if fn in MAX_FUNCS or fam == "MAX":
                a = args[0]
                b = args[1] if len(args) > 1 else a
                out.append("      %s = %s" % (dst, a))
                out.append("      IF (%s .GT. %s) %s = %s" % (b, dst, dst, b))
            elif fn in MIN_FUNCS or fam == "MIN":
                a = args[0]
                b = args[1] if len(args) > 1 else a
                out.append("      %s = %s" % (dst, a))
                out.append("      IF (%s .LT. %s) %s = %s" % (b, dst, dst, b))
            elif fn in ABS_FUNCS or fam == "ABS":
                a = args[0]
                out.append("      %s = %s" % (dst, a))
                out.append("      IF (%s .LT. 0) %s = -%s" % (a, dst, a))
            elif fn in DIM_FUNCS or fam == "DIM":
                if len(args) < 2:
                    out.append(line)
                    continue
                out.append("      %s = %s - %s" % (dst, args[0], args[1]))
                out.append("      IF (%s .LT. 0) %s = 0" % (dst, dst))
            else:
                out.append(line)
            continue

        elif rule == 21:
            out.append("C@ %s -> (removed; EXTERNAL/INTRINSIC declaration)" % orig)

        elif rule == 22:
            # CABS(WC) -> SQRT(REAL(WC)**2 + AIMAG(WC)**2).  REAL/AIMAG are
            # native; complex_vars declarations are materialized in Pass A.
            m = re.match(r"\s*([A-Za-z]\w*)\s*=\s*CABS\s*\(\s*([^()]+)\s*\)",
                         line, re.I)
            if not m:
                out.append(line)
                continue
            dst, z = m.group(1), m.group(2).strip()
            new = "%s = SQRT(REAL(%s)**2 + AIMAG(%s)**2)" % (dst, z, z)
            out.append("C@ %s -> %s" % (orig, new))
            out.append("      " + new)
            continue

        else:
            raise SystemExit("unknown rule %d on line %d" % (rule, idx))

        # rule 0 string comparison lowering (F77PREP has no type knowledge)
        if rule == 0 and char_info:
            cm = re.search(
                r"\b([A-Za-z]\w*)\s*(\.EQ\.|\.NE\.)\s*([A-Za-z]\w*)\b"
                r"\s*(GO\s+TO\s+\d+)?", line, re.I)
            if cm and cm.group(1) in char_info and cm.group(3) in char_info:
                out.pop()  # drop the original line emitted above
                a, op, b, action = (cm.group(1), cm.group(2).upper(),
                                    cm.group(3), cm.group(4))
                call = "KCMP = ISTRCM(%s,%s)" % (char_info[a][0], char_info[b][0])
                out.append("C@ %s -> %s" % (orig, call))
                out.append("      " + call)
                if action:
                    cond = ".EQ." if op == ".EQ." else ".NE."
                    out.append("      IF (KCMP %s 0) %s" % (cond, action.upper()))
                continue

    # rule 22 support: F77 gives an implicitly-REAL variable when the source
    # assigns a complex literal to an undeclared name, so REAL()/AIMAG() would
    # silently discard the imaginary part.  Materialize COMPLEX declarations
    # immediately AFTER the PROGRAM/ENTRY statement (never before it).
    if complex_vars - explicit_complex:
        pos = None
        for i, ln in enumerate(out):
            if re.match(r"\s*(PROGRAM|SUBROUTINE|FUNCTION|ENTRY)\s", ln, re.I):
                pos = i + 1
                break
        if pos is not None:
            ins = []
            for v in sorted(complex_vars - explicit_complex):
                ins.append("C@ implicit COMPLEX %s (rule 22 complex-literal)" % v)
                ins.append("      COMPLEX %s" % v)
            out[pos:pos] = ins

    if loop_stack:
        # rule 17: no matching END DO -- close every open DO WHILE at the
        # END/STOP of the program unit, LIFO, using the allocated labels.
        end_at = None
        for i in range(len(out) - 1, -1, -1):
            if out[i].strip().upper().startswith("END"):
                end_at = i
                break
        close_insert = []
        for top, bottom, _auto in reversed(loop_stack):
            close_insert.append(
                "C@ (rule 17) open DO WHILE -> GO TO %d / %d CONTINUE"
                % (top, bottom))
            close_insert.append("      GO TO %d" % top)
            close_insert.append("%s CONTINUE" % _label_field(bottom))
        if end_at is None:
            out += close_insert
        else:
            out[end_at:end_at] = close_insert
        loop_stack = []

    # Appending all FORMAT statements just before the final END.
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

    # Rule 20: any identifier longer than six characters is a hard error
    # (A5: silent 6-char truncation).  Keywords and the name of the program
    # unit itself are not identifiers subject to the F77 length limit.
    names_by_line = {}
    for (idx, kind), vals in aux4.items():
        if kind != 20:
            continue
        cur = ""
        for pos in sorted(vals):
            if pos == 1 and cur:
                names_by_line.setdefault(idx, []).append(cur)
                cur = ""
            cur += chr(vals[pos])
        if cur:
            names_by_line.setdefault(idx, []).append(cur)
    subprograms = set()
    for ln in lines:
        m = re.search(r"\b(?:PROGRAM|SUBROUTINE|FUNCTION|ENTRY)\s+([A-Za-z]\w*)",
                      ln, re.I)
        if m:
            subprograms.add(m.group(1).upper())
    bad = []
    for idx in sorted(names_by_line):
        if idx <= len(lines) and is_comment(lines[idx - 1]):
            continue
        for nm in names_by_line[idx]:
            u = nm.upper()
            if u in KEYWORDS or u in subprograms or not re.match(r"^[A-Za-z]", u):
                continue
            bad.append((idx, lines[idx - 1].strip() if idx <= len(lines) else "", u))
    if bad:
        by_prefix = {}
        for _, _, u in bad:
            by_prefix.setdefault(u[:6], []).append(u)
        idx, orig, u = bad[0]
        group = sorted(set(by_prefix[u[:6]]))
        if len(group) > 1:
            msg = "TRUNCATED NAME: %s (all -> %s)" % (" / ".join(group), u[:6])
        else:
            msg = "TRUNCATED NAME: %s (%d chars -> %s)" % (u, len(u), u[:6])
        print("C@ %s -> %s" % (orig, msg))
        raise SystemExit(msg)

    # rule 18 (M2): re-split emitted statements longer than 72 columns into
    # fixed-form continuation cards.  F77PREP classifies glued logical lines;
    # without this step a >72-char result would silently lose columns 73+.
    wrapped = []
    for ln in out:
        if len(ln) <= 72 or ln[:1].upper() == "C":
            wrapped.append(ln)
            continue
        chunks = [ln[:72]]
        chunks += [ln[i:i + 66] for i in range(72, len(ln), 66)]
        wrapped.append(chunks[0])
        for ch in chunks[1:]:
            wrapped.append("     1" + ch)
    out = wrapped

    return "\n".join(out) + "\n"


def make_deck2(low_path, data_path=None, sentinels=None):
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
    for s in sentinels or []:
        body.append(s)
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
        text = build_lowered(sys.argv[2], sys.argv[3])
        open(sys.argv[4], "w", encoding="utf-8").write(text)
        json.dump(LAST_LABEL_RECORDS,
                  open(sys.argv[4] + ".777004.json", "w", encoding="utf-8"))
    elif cmd == "deck2":
        data = sys.argv[4] if len(sys.argv) > 4 else None
        open(sys.argv[3], "w", encoding="utf-8").write(make_deck2(sys.argv[2], data))
    else:
        raise SystemExit("unknown command: " + cmd)


if __name__ == "__main__":
    main()
