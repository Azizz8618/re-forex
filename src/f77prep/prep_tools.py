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

# v3.2 rule 23: LOGICAL .EQV./.NEQV. -> C5 primitives (A5 matrix element C6).
# .EQV./.NEQV. are rejected by FOREX 2.02; AND/OR/NOT are native.  The
# expansion below is the byte-exact form proven in
# tests/plan-f77-full/unit/C06_eqv_neqv/c06_lowered.b6 (gold "   0  1").
EQV_OPS = ((".NEQV.", "NE"), (".EQV.", "EQ"))
EQV_OPERAND = r"((?:\.NOT\.\s*)?[A-Za-z]\w*(?:\s*\([^()]*\))?)"


def lower_astar(line):
    """R-ASTAR: assumed-size dummy array A(*) -> A(1); A(lb:*) -> A(lb).

    FOREX 2.02 traps on '*' in a dummy-array bound; a concrete lower bound
    of 1 preserves addressing for the common 1-based case (E-H agent proof:
    tests/plan-f77-full/unit/F19_dummy_array/…astar_lowered.b6 -> 15).
    """
    out = re.sub(r"\(\s*([A-Za-z]\w*\s*:\s*)?\*\s*\)",
                 lambda m: "(" + ((m.group(1) or "").replace(":", "").strip() or "1") + ")",
                 line, flags=re.I)
    return out


def lower_eqv(line):
    """Expand .EQV./.NEQV. using .AND./.OR./.NOT. (rule 23, C6).

    Operands may be names or single-level parenthesised expressions, optionally
    prefixed by .NOT..  A function call with side effects would be emitted
    twice -- document this when using the lowering on such expressions.
    """
    out = line
    for op, kind in EQV_OPS:
        while op in out.upper():
            pos = out.upper().find(op)
            left, right = out[:pos], out[pos + len(op):]
            lm = re.search(EQV_OPERAND + r"\s*$", left)
            rm = re.match(r"\s*" + EQV_OPERAND, right)
            if not lm or not rm:
                break  # unsupported shape; leave for host diagnostics
            a, b = lm.group(1), rm.group(1)
            if kind == "EQ":
                repl = "(%s .AND. %s) .OR. (.NOT.%s .AND. .NOT.%s)" % (a, b, a, b)
            else:
                repl = "(%s .AND. .NOT.%s) .OR. (.NOT.%s .AND. %s)" % (a, b, a, b)
            out = left[:lm.start(1)] + repl + right[rm.end(1):]
    return out

# v3.3 wave-2 host-only rules (F77PREP.FTN is frozen at v3: FOREX 2.02 has a
# hard translation-memory ceiling).  The numbers are local to the host; the
# numeric records printed by F77PREP stay unchanged.
R_E9 = 25        # DO with zero iterations -> guard before / Ls after
R_F11 = 26       # SAVE -> COMMON /<U>SV/ + BLOCK DATA
R_G8 = 27        # CALL S(*L,..) / RETURN j -> INTEGER RC
R_G4 = 28        # CHARACTER*n FUNCTION -> SUBROUTINE + Hollerith DATA
R_H7 = 29        # CHARACTER*n array -> INTEGER array
R13 = 30         # G edit descriptor -> typed E/F/D/L/I
R21 = 31         # 1P, E12.4 -> 1PE12.4
R11 = 32         # END=/ERR= sentinel branch (rule 4 and rule 10)

# Wave F / P7c: F77 file I/O -> PERSO 0o2320 CALL bridge (rules 34-40).
# Rule 33 is intentionally left unused (reserved for the J24 stub of 20-open-close.md).
R_OPEN = 34      # OPEN(...)  -> CALL ZFOPEN
R_CLOSE = 35     # CLOSE(...) -> CALL ZFCLOSE
R_INQ = 36       # INQUIRE(...) -> CALL ZFINQ
R_FWRIT = 37     # WRITE(u,fmt) list -> ENCODE + CALL ZFWRIT
R_FREAD = 38     # READ(u,fmt) list -> CALL ZFREAD + DECODE
R_UWRIT = 39     # WRITE(u) list -> CALL ZFWRIT (unformatted)
R_UREAD = 40     # READ(u) list -> CALL ZFREAD (unformatted)

# PERSO bridge constants (contract with the 0o2320 implementation, doc 34).
#   COMMON /FILMAP/ FM(20): FM(1)=last ISTAT, FM(2)=OPENED, FM(3)=EXIST.
#   ISTAT=-1 means EOF.  FOREX 2.02 returns status via COMMON because scalar
#   actual arguments are passed by value (31-fortran-arfa-bridge.md §2.3).
FILMAP_WORDS = 20
IOBUF_WORDS = 12                 # 12 * 6 = 72 characters per formatted record
NAME_WORDS = 2                   # INTEGER(2); 12 ASCII/GOST bytes (doc 32 H6)
STATUS_CODES = {"UNKNOWN": 0, "OLD": 1, "NEW": 2, "SCRATCH": 3}

# Rules that must replace a non-zero classification produced by F77PREP.FTN
# (CHARACTER*n is currently reported as rule 7/12, SAVE as rule 2).
FORCE_HOST = {R_F11, R_G4, R_H7, R_OPEN, R_CLOSE, R_INQ,
              R_FWRIT, R_FREAD, R_UWRIT, R_UREAD}


def _split_top(s):
    """Split on top-level commas, respecting parentheses."""
    parts, depth, cur = [], 0, ""
    for ch in s:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(cur.strip())
            cur = ""
        else:
            cur += ch
    parts.append(cur.strip())
    return parts


def _implicit_type(name):
    """F77 implicit typing: I-N -> INTEGER, otherwise REAL."""
    return "INTEGER" if name[:1].upper() in INT_FIRST else "REAL"


# --------------------------------------------------------------------------
# file-I/O lowering helpers (rules 34-40, doc 34)
# --------------------------------------------------------------------------

def _io_control(s):
    """Parse the comma-separated control list of OPEN/CLOSE/INQUIRE.

    Returns a dict of upper-cased keyword -> value string.  Positional unit
    (the first item of OPEN/CLOSE) is returned under key 'U'.  Quoted literals
    keep their quotes so that the caller can decide about transcoding.
    """
    m = re.match(r"^[A-Z]+\s*\(([^()]*)\)", s.strip(), re.S)
    if not m:
        return {}
    items, depth, cur, quoted = [], 0, "", False
    for ch in m.group(1):
        if ch == "'":
            quoted = not quoted
        if ch == "(" and not quoted:
            depth += 1
        elif ch == ")" and not quoted:
            depth -= 1
        if ch == "," and depth == 0 and not quoted:
            items.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        items.append(cur.strip())
    out = {}
    pos = 0
    for it in items:
        if "=" in it:
            k, v = it.split("=", 1)
            out[k.strip().upper()] = v.strip()
        else:
            pos += 1
            out["P%d" % pos] = it
            if pos == 1:
                out["U"] = it
    return out


def _io_iostat(ctrl):
    """Name of the user IOSTAT= variable, or None."""
    v = ctrl.get("IOSTAT")
    return v if v and re.match(r"^[A-Za-z]\w*$", v) else None


def _gost_name_words(literal, var):
    """Emit INTEGER(2) DATA words carrying the FILE= name bytes.

    FOREX 2.02 ``nH`` stores 8-bit ASCII bytes, six per 48-bit word
    (10-implementation-libr.md §3.1, proved again by this wave's probe).
    Exact GOST-10859 bytes cannot be materialised from source: GOST codes
    000..011 (digits) map to control characters that dispak's card reader
    mangles.  The host therefore emits the ASCII name; the PERSO ZFOPEN is
    responsible for the ASCII -> GOST-10859 transcode (doc 34 §2, honest
    deviation from doc 32 H6).  Names longer than 12 bytes are a hard error.
    """
    lit = literal.strip()
    if len(lit) >= 2 and lit[0] == "'" and lit[-1] == "'":
        lit = lit[1:-1]
    raw = lit.encode("latin-1", errors="replace")
    if not (1 <= len(raw) <= NAME_WORDS * 6):
        raise SystemExit("FILE= name must be 1..%d bytes, got %d" %
                         (NAME_WORDS * 6, len(raw)))
    padded = raw.ljust(NAME_WORDS * 6)
    hol = "".join(chr(b) if 32 <= b < 127 else " " for b in padded)
    return ["      INTEGER %s(%d)" % (var, NAME_WORDS),
            "      DATA %s /%dH%s/" % (var, NAME_WORDS * 6, hol)]


def _classify_file_io(s):
    """Host classification for rules 34-40 (F77PREP.FTN is frozen)."""
    s = re.sub(r"^\s*\d+\s+", "", s)
    m = re.match(r"^OPEN\s*\(", s)
    if m:
        return R_OPEN
    m = re.match(r"^CLOSE\s*\(", s)
    if m:
        return R_CLOSE
    m = re.match(r"^INQUIRE\s*\(", s)
    if m:
        return R_INQ
    # WRITE(u,fmt[,...]) / READ(u,fmt[,END=,IOSTAT=...]) -> formatted.
    m = re.match(r"^WRITE\s*\(\s*\d+\s*,\s*(\d+|\*)\s*[,)]", s)
    if m:
        return R_FWRIT
    m = re.match(r"^READ\s*\(\s*\d+\s*,\s*(\d+|\*)\s*[,)]", s)
    if m:
        return R_FREAD
    m = re.match(r"^WRITE\s*\(\s*\d+\s*(\)|,\s*(END|IOSTAT|ERR)\s*=)", s)
    if m:
        return R_UWRIT
    m = re.match(r"^READ\s*\(\s*\d+\s*(\)|,\s*(END|IOSTAT|ERR)\s*=)", s)
    if m:
        return R_UREAD
    return None


def _unit_of(lines, idx):
    """Name of the program unit containing logical line idx (1-based)."""
    for j in range(idx - 1, 0, -1):
        m = re.search(r"\b(PROGRAM|SUBROUTINE|FUNCTION|BLOCK\s+DATA)\s+([A-Za-z]\w*)",
                      lines[j - 1], re.I)
        if m:
            return m.group(2).upper()
    return "MAIN"


def _f11_applies(lines, idx):
    """True when SAVE needs the R-F11 COMMON/BLOCK DATA lowering.

    The legacy v1 case (SAVE of a plain main-program variable with no DATA
    initializer) keeps rule 2's byte-identical "(removed)" lowering.  A
    subprogram SAVE, or any SAVE whose variable has a DATA initializer in the
    same unit, gets the standards-correct COMMON + BLOCK DATA form.
    """
    hdr = None
    for j in range(idx - 1, 0, -1):
        if re.match(r"\s*(PROGRAM|SUBROUTINE|FUNCTION|BLOCK\s+DATA)\b",
                    lines[j - 1], re.I):
            hdr = lines[j - 1].strip().upper()
            break
    if hdr and not hdr.startswith("PROGRAM"):
        return True
    m = re.search(r"\bSAVE\s+(.+)$", lines[idx - 1], re.I)
    saved = [t.strip().upper() for t in _split_top(m.group(1))] if m else []
    ustart = idx
    for j in range(idx - 1, 0, -1):
        if re.match(r"\s*(PROGRAM|SUBROUTINE|FUNCTION|BLOCK\s+DATA)\b",
                    lines[j - 1], re.I):
            ustart = j
            break
    for j in range(ustart, len(lines)):
        ln = lines[j]
        if j != ustart and re.match(
                r"\s*(PROGRAM|SUBROUTINE|FUNCTION|BLOCK\s+DATA|END)\b", ln, re.I):
            break
        for nm in saved:
            if re.search(r"\bDATA\s+%s\s*/" % re.escape(nm), ln, re.I):
                return True
    return False


# Fortran keywords and intrinsics: never treated as truncatable identifier
# by the rule-20 collision check.
KEYWORDS = {
    "PROGRAM", "SUBROUTINE", "FUNCTION", "INTEGER", "REAL", "LOGICAL",
    "COMPLEX", "DOUBLE", "PRECISION", "CHARACTER", "DIMENSION", "COMMON",
    "DATA", "PARAMETER", "EQUIVALENCE", "ASSIGN", "IMPLICIT", "CONTINUE",
    "FORMAT", "PRINT", "READ", "WRITE", "WHILE", "GOTO", "GO", "STOP",
    "OPEN", "CLOSE", "INQUIRE", "REWIND", "BACKSPACE", "ENDFILE",
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
        "*perso:602320,cont",   # doc 34 H8: PERSO 0o2320 file bridge
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
    # Wave-2 pre-scan: CHARACTER*n FUNCTION names are needed before the
    # classification loop so their result assignment and call sites can be
    # recognized too (F77PREP misreports all three as rules 7/8/0).
    char_funcs = {}
    for _idx, _line in enumerate(lines, 1):
        if is_comment(_line):
            continue
        _cf = re.search(r"CHARACTER\s*\*\s*(\d+)\s+FUNCTION\s+([A-Za-z]\w*)",
                        _line, re.I)
        if _cf:
            char_funcs[_cf.group(2).upper()] = int(_cf.group(1))

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
        _fio = _classify_file_io(_s)
        if _fio is not None:
            host_rules[_idx] = _fio   # wave F: F77 file I/O -> PERSO bridge
        elif re.match(r"^(\d+\s+)?FORMAT\s*\(", _s) and re.search(r"G\d+\.\d+", _s):
            host_rules[_idx] = R13   # J13: G descriptor -> typed E/F/D/L/I
        elif re.match(r"^(\d+\s+)?FORMAT\s*\(", _s) and re.search(r"\d+P\s*,", _s):
            host_rules[_idx] = R21   # J21: scale factor P with comma is illegal
        elif re.match(r"^DO\s+\d+\s+\w+\s*=", _s):
            host_rules[_idx] = R_E9  # E9: post-test DO, zero iterations
        elif char_funcs and (
                re.match(r"^CHARACTER\s*\*\s*\d+\s+FUNCTION\b", _s) or
                any(re.match(r"^\s*%s\s*=\s*'" % re.escape(fn), _line, re.I)
                    for fn in char_funcs) or
                any(re.search(r"=\s*%s\s*\(" % re.escape(fn), _s)
                    for fn in char_funcs)):
            host_rules[_idx] = R_G4  # G4: character FUNCTION -> SUBROUTINE
        elif re.match(r"^CHARACTER\s*\*\s*\d+\s+[A-Za-z]\w*\s*\(", _s):
            host_rules[_idx] = R_H7  # H7: CHARACTER array -> INTEGER array
        elif re.match(r"^CALL\s+\w+\s*\([^)]*\*\d+", _s) or \
                re.match(r"^RETURN\s+\d+\s*$", _s):
            host_rules[_idx] = R_G8  # G8: alternate returns
        elif re.match(r"^SAVE\s+\w", _s) and _f11_applies(lines, _idx):
            host_rules[_idx] = R_F11  # F11: SAVE -> COMMON + BLOCK DATA
        elif re.match(r"^(EXTERNAL|INTRINSIC)\s", _s):
            host_rules[_idx] = 21
        elif re.search(r"\bCABS\s*\(", _s):
            host_rules[_idx] = 22
        elif re.search(r"\.EQV\.|\.NEQV\.", _s):
            host_rules[_idx] = 23  # C6: LOGICAL equivalence -> C5 primitives
        elif re.match(r"^(INTEGER|REAL|LOGICAL|COMPLEX|DOUBLE|DIMENSION)\b", _s) \
                and re.search(r"\([^()]*\*[^()]*\)", _s):
            host_rules[_idx] = 24  # F19/H6: assumed-size A(*) -> A(1)
        else:
            for _fn in MAX_FUNCS | MIN_FUNCS | ABS_FUNCS | DIM_FUNCS:
                if re.search(r"\b%s\s*\(" % re.escape(_fn), _s):
                    host_rules[_idx] = 19
                    break
    for _idx in dwh_stack:
        host_rules[_idx] = 17
    for _idx, _rule in host_rules.items():
        _prev = rules.get(_idx, {}).get("rule", 0)
        if _prev == 0 or _rule in FORCE_HOST:
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
    # wave-2 host state
    var_types = {}          # R13: declared type of each PRINT variable
    print_vars_by_label = {}  # R13: FORMAT label -> PRINT variable list
    e9_terms = {}           # R-E9: DO line -> index of its terminal line
    e9_after = {}           # terminal line -> [Ls label, ...]
    e9_done = set()
    f11_info = {}           # R-F11: SAVE line -> (block, names, DATA line idxs)
    f11_data_idx = {}       # DATA line -> owning COMMON block
    g8_units = {}           # R-G8: unit -> number of alternate return labels
    g8_calls = {}           # CALL line -> (unit, labels)
    g8_ret_units = {}       # RETURN j line -> unit
    g8_declared = set()
    g4_declared = set()
    # wave F (rules 34-40): declarations are hoisted to the top of the unit
    # (FOREX 2.02 rejects a declaration after an executable statement).
    filmap_units = set()
    iobuf_units = set()
    fname_units = set()
    fio_decls = {}           # program unit -> [declaration / DATA lines]
    out = []

    # ---------------- Pass A: declarations, implicit maps, rename maps -----
    for idx, line in enumerate(lines, 1):
        rule = rules.get(idx, {}).get("rule", 0)

        # ---- wave-2 pre-collection (needs the full source, not the rewrite) ----
        for dm in re.finditer(r"\b(INTEGER|REAL|LOGICAL|COMPLEX|DOUBLE\s+PRECISION)\b"
                              r"([^\n]*)", line, re.I):
            typ = "DP" if dm.group(1).upper().startswith("DOUBLE") else dm.group(1).upper()
            for nm in re.findall(r"[A-Za-z]\w*", dm.group(2)):
                if nm.upper() not in KEYWORDS:
                    var_types[nm.upper()] = typ
        cm = re.search(r"\bCHARACTER\s*\*\s*\d+\s+([A-Za-z]\w*)", line, re.I)
        if cm:
            var_types[cm.group(1).upper()] = "CHAR"
        pm = re.match(r"\s*PRINT\s+(\d+)\s*,\s*(.*)$", line, re.I)
        if pm:
            print_vars_by_label[int(pm.group(1))] = [
                v.strip() for v in _split_top(pm.group(2)) if v.strip()]

        if rule == R_E9:
            dm = re.match(r"\s*DO\s+(\d+)\s+\w+\s*=", line, re.I)
            if dm:
                dlabel = int(dm.group(1))
                for j in range(idx + 1, len(lines) + 1):
                    tm = re.match(r"\s*(\d+)\s+\S", lines[j - 1])
                    if tm and int(tm.group(1)) == dlabel:
                        e9_terms[idx] = j
                        break

        if rule == R_F11:
            sm = re.search(r"\bSAVE\s+(.+)$", line, re.I)
            names = [t.strip() for t in _split_top(sm.group(1)) if t.strip()] if sm else []
            unit = _unit_of(lines, idx)
            block = (unit[:3] + "SV")[:6].upper()
            suffix = 0
            while block in {v[0] for v in f11_info.values()}:
                suffix += 1
                block = ((unit[:2] + str(suffix)) + "SV")[:6].upper()
            ustart = idx
            for j in range(idx - 1, 0, -1):
                if re.match(r"\s*(PROGRAM|SUBROUTINE|FUNCTION|BLOCK\s+DATA)\b",
                            lines[j - 1], re.I):
                    ustart = j
                    break
            dlines = []
            for j in range(ustart, len(lines)):
                if j != ustart and re.match(
                        r"\s*(PROGRAM|SUBROUTINE|FUNCTION|BLOCK\s+DATA|END)\b",
                        lines[j], re.I):
                    break
                for nm in names:
                    if re.search(r"\bDATA\s+%s\s*/" % re.escape(nm), lines[j], re.I):
                        dlines.append(j + 1)
                        break
            f11_info[idx] = (block, names, dlines)
            for j in dlines:
                f11_data_idx[j] = block

        if rule == R_G8:
            if re.match(r"\s*CALL\s", line, re.I):
                labels = [int(x) for x in re.findall(r"\*\s*(\d+)", line)]
                unit = _unit_of(lines, idx)
                g8_calls[idx] = (unit, labels)
                g8_units.setdefault(unit, len(labels))
            elif re.match(r"\s*RETURN\s+\d+", line, re.I):
                unit = _unit_of(lines, idx)
                g8_ret_units[idx] = unit
                g8_units.setdefault(unit, 1)

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

    def emit_e9_after(idx):
        """Place R-E9's Ls CONTINUE right after the DO terminal statement."""
        if idx in e9_after and idx not in e9_done:
            e9_done.add(idx)
            for lab in e9_after[idx]:
                out.append(_label_field(lab) + " CONTINUE")

    def _decl(unit, *lines):
        fio_decls.setdefault(unit, []).extend(lines)

    def emit_filmap(unit):
        """COMMON /FILMAP/ FM(20) once per program unit (doc 34 §2)."""
        if unit in filmap_units:
            return
        filmap_units.add(unit)
        _decl(unit,
              "C@ F77A FILMAP: FM(1)=ISTAT FM(2)=OPENED FM(3)=EXIST",
              "      INTEGER FM(%d)" % FILMAP_WORDS,
              "      COMMON /FILMAP/ FM")

    def emit_iobuf(unit, u):
        """Formatted I/O buffer INTEGER IB<u>(12) once per unit."""
        key = (unit, u)
        if key in iobuf_units:
            return
        iobuf_units.add(key)
        _decl(unit, "      INTEGER IB%s(%d)" % (u, IOBUF_WORDS))

    def io_status(k):
        """Status lvalue: the user's IOSTAT variable, else FM(1)."""
        return k if k else "FM(1)"

    def io_list_format(items):
        """Synthesize a FORMAT label for list-directed WRITE(u,*)/READ(u,*)."""
        names = [t.strip() for t in _split_top(items) if t.strip()]
        specs = []
        for v in names:
            specs += _descriptor(v, char_info, char_rename, dp_vars,
                                 typed_int).split(",")
        lab = alloc(fmt_counter[0])
        fmt_counter[0] = lab + 1
        formats.append((lab, ",".join(specs)))
        out.append("C@ F77A list-directed -> %d FORMAT(%s)" %
                   (lab, ",".join(specs)))
        return lab

    # ---------------- Pass B: lower each classified line -------------------
    for idx, line in enumerate(lines, 1):
        r = rules.get(idx, {"rule": 0, "itype": 0})
        rule, itype = r["rule"], r["itype"]
        orig = line.strip()
        seq = seqs[idx - 1] if idx <= len(seqs) else idx

        # R-F11: a DATA initializer of a SAVEd variable belongs to BLOCK DATA.
        if idx in f11_data_idx:
            out.append("C@ %s -> (moved to BLOCK DATA %s)" %
                       (orig, f11_data_idx[idx]))
            continue

        # R-G8: add RC as the first dummy of every unit with RETURN j / *label.
        hm = re.match(r"\s*(SUBROUTINE|FUNCTION)\s+([A-Za-z]\w*)\s*\((.*)\)\s*$",
                      line, re.I)
        if hm and hm.group(2).upper() in g8_units:
            args = [a.strip() for a in _split_top(hm.group(3)) if a.strip()]
            if not any(a.upper() == "RC" for a in args):
                args = ["RC"] + args
            newline = "      %s %s(%s)" % (hm.group(1).upper(), hm.group(2),
                                           ",".join(args))
            out.append("C@ %s -> %s / INTEGER RC" % (orig, newline.strip()))
            out.append(newline)
            out.append("      INTEGER RC")
            continue

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
            emit_e9_after(idx)

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
            # R11-END (v2 rule 4): the old lowering dropped the END= branch.
            # Keep the legacy anchor text for byte-compatibility with case2,
            # but always materialize the sentinel check after READ.
            m = re.search(r"END\s*=\s*\d+\s*\)\s*([A-Za-z]\w*)", line, re.I)
            var = m.group(1) if m else "X"
            lm = re.search(r"END\s*=\s*(\d+)", line, re.I)
            target = int(lm.group(1)) if lm else None
            lab = alloc(read_counter[0])
            read_counter[0] = lab + 1
            vtyp = var_types.get(var.upper(), _implicit_type(var))
            spec = "I10" if vtyp == "INTEGER" else "F12.4"
            new = "READ %d,%s" % (lab, var)
            out.append("C@ %s -> %s  (END= label removed)" % (orig, new))
            out.append("      " + new)
            formats.append((lab, spec))
            if target is not None:
                sentinel = "-999999" if vtyp == "INTEGER" else "-999999."
                chk = "IF (%s .EQ. %s) GO TO %d" % (var, sentinel, target)
                out.append("C@ R11-END -> %s" % chk)
                out.append("      " + chk)

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
                        dcard = "DATA %s/6H%s/" % (tname, sub)
                        out.append("C@ %s -> %s ; %s" % (orig, dcard, newline.strip()))
                        out.append("      " + dcard)
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

        elif rule == 23:
            # C6: .EQV./.NEQV. -> .AND./.OR./.NOT. (native C5 primitives).
            new = lower_eqv(orig)
            if new == orig:
                out.append(line)
                continue
            out.append("C@ %s -> %s" % (orig, new))
            out.append("      " + new)
            continue

        elif rule == 24:
            # F19/H6: assumed-size dummy array A(*) -> A(1) (no machine trap).
            new = lower_astar(orig)
            if new == orig:
                out.append(line)
                continue
            out.append("C@ %s -> %s" % (orig, new))
            out.append("      " + new)
            continue

        elif rule == R_E9:
            # E9: FOREX DO is post-test, so an empty range runs the body once.
            dm = re.match(r"\s*DO\s+(\d+)\s+([A-Za-z]\w*)\s*=\s*(.+)$", line, re.I)
            if not dm:
                out.append(line)
                continue
            bounds = _split_top(dm.group(3))
            e1 = bounds[0] if bounds else "0"
            e2 = bounds[1] if len(bounds) > 1 else "0"
            e3 = bounds[2] if len(bounds) > 2 else None
            Ls = dyn_alloc(seq, R_E9, 0)
            if idx in e9_terms:
                e9_after.setdefault(e9_terms[idx], []).append(Ls)
            if e3 is None or re.match(r"^\+?\d+$", e3):
                guards = ["IF (%s .GT. %s) GO TO %d" % (e1, e2, Ls)]
            elif re.match(r"^-\d+$", e3):
                guards = ["IF (%s .LT. %s) GO TO %d" % (e1, e2, Ls)]
            elif re.match(r"^[A-Za-z]\w*$", e3):
                Lp = dyn_alloc(seq, R_E9, 1)
                Lb = dyn_alloc(seq, R_E9, 2)
                guards = ["IF (%s .GE. 0) GO TO %d" % (e3, Lp),
                          "IF (%s .LT. %s) GO TO %d" % (e1, e2, Ls),
                          "GO TO %d" % Lb,
                          "%d CONTINUE" % Lp,
                          "IF (%s .GT. %s) GO TO %d" % (e1, e2, Ls),
                          "%d CONTINUE" % Lb]
            else:
                guards = ["IF (%s .GT. %s) GO TO %d" % (e1, e2, Ls)]
            new = "DO %s %s=%s,%s%s" % (dm.group(1), dm.group(2), e1, e2,
                                        ("," + e3) if e3 else "")
            # Keep the anchor short: FOREX 2.02 reads only columns 1-72 of a
            # comment card, the rest would be parsed as a stray card.
            gdesc = guards[0] if len(guards) == 1 else "IF-GUARD(%s)" % e3
            out.append("C@ %s -> %s / %d CONTINUE" % (orig, gdesc, Ls))
            for g in guards:
                out.append(g if re.match(r"^\d+ CONTINUE", g) else "      " + g)
            out.append("      " + new)
            continue

        elif rule == R_F11:
            block, names, _dlines = f11_info[idx]
            new = "COMMON /%s/%s" % (block, ",".join(names))
            out.append("C@ %s -> %s (BLOCK DATA init)" % (orig, new))
            out.append("      " + new)
            continue

        elif rule == R_G8:
            if idx in g8_calls:
                unit, labels = g8_calls[idx]
                cm = re.match(r"\s*CALL\s+(\w+)\s*\((.*)\)\s*$", line, re.I)
                if not cm:
                    out.append(line)
                    continue
                args = [a.strip() for a in _split_top(cm.group(2)) if a.strip()]
                other = [a for a in args if not a.startswith("*")]
                Lb = dyn_alloc(seq, R_G8, 0)
                new = "CALL %s(%s)" % (cm.group(1), ",".join(["RC"] + other))
                out.append("C@ %s -> INTEGER RC / %s" % (orig, new))
                out.append("C@ R-G8 -> GO TO (%s),RC / %d CONTINUE"
                           % (",".join(map(str, labels + [Lb])), Lb))
                if unit not in g8_declared:
                    out.append("      INTEGER RC")
                    g8_declared.add(unit)
                out.append("      " + new)
                out.append("      GO TO (%s),RC" % ",".join(map(str, labels + [Lb])))
                out.append(_label_field(Lb) + " CONTINUE")
                continue
            rm = re.match(r"\s*RETURN\s+(\d+)\s*$", line, re.I)
            if rm:
                out.append("C@ %s -> RC=%s / RETURN" % (orig, rm.group(1)))
                out.append("      RC=%s" % rm.group(1))
                out.append("      RETURN")
                continue
            out.append(line)
            continue

        elif rule == R_G4:
            hm = re.search(r"CHARACTER\s*\*\s*(\d+)\s+FUNCTION\s+([A-Za-z]\w*)"
                           r"\s*\(([^)]*)\)", line, re.I)
            if hm:
                n = int(hm.group(1))
                fname = hm.group(2)
                args = [a.strip() for a in _split_top(hm.group(3)) if a.strip()]
                w = (n + 5) // 6
                newargs = ",".join(["RV"] + args)
                out.append("C@ %s -> SUBROUTINE %s(%s) / INTEGER RV" %
                           (orig, fname, newargs))
                out.append("      SUBROUTINE %s(%s)" % (fname, newargs))
                out.append("      INTEGER RV,IH" if w == 1 else
                           "      INTEGER RV(%d),IH(%d)" % (w, w))
                char_funcs[fname.upper()] = n
                continue
            am = re.match(r"\s*([A-Za-z]\w*)\s*=\s*'([^']*)'\s*$", line)
            if am and am.group(1).upper() in char_funcs:
                lit = am.group(2)
                w = (char_funcs[am.group(1).upper()] + 5) // 6
                words = [lit[6 * k:6 * k + 6].ljust(6) for k in range(w)]
                out.append("C@ %s -> DATA IH/...Hollerith.../ / RV=IH" % orig)
                if w == 1:
                    out.append("      DATA IH/%dH%s/" % (len(words[0].rstrip()),
                                                        words[0].rstrip()))
                else:
                    for k, word in enumerate(words):
                        out.append("      DATA IH(%d)/6H%s/" % (k + 1, word))
                out.append("      RV=IH")
                continue
            cm = re.match(r"\s*([A-Za-z]\w*)\s*=\s*([A-Za-z]\w*)\s*\((.*)\)\s*$",
                          line, re.I)
            if cm and cm.group(2).upper() in char_funcs:
                dst, fname = cm.group(1), cm.group(2).upper()
                args = [a.strip() for a in _split_top(cm.group(3)) if a.strip()]
                unit = _unit_of(lines, idx)
                if re.match(r"^[A-Za-z]\w*$", dst):
                    rv = dst
                    if rv.upper() not in var_types and (unit, rv.upper()) not in g4_declared:
                        out.append("      INTEGER %s" % rv)
                        g4_declared.add((unit, rv.upper()))
                else:
                    rv = ("I" + fname)[:6]
                    if (unit, rv) not in g4_declared:
                        out.append("      INTEGER %s" % rv)
                        g4_declared.add((unit, rv))
                call = "CALL %s(%s%s)" % (fname, rv,
                                          ("," + ",".join(args)) if args else "")
                out.append("C@ %s -> %s" % (orig, call))
                out.append("      " + call)
                continue
            out.append(line)
            continue

        elif rule == R_H7:
            hm = re.match(r"\s*CHARACTER\s*\*\s*(\d+)\s+([A-Za-z]\w*)\s*\((.*)\)\s*$",
                          line, re.I)
            if not hm:
                out.append(line)
                continue
            w = (int(hm.group(1)) + 5) // 6
            dims = _split_top(hm.group(3))
            newdims = ",".join(str(int(d) * w) if re.match(r"^\d+$", d) else d
                               for d in dims)
            new = "INTEGER %s(%s)" % (hm.group(2), newdims)
            out.append("C@ %s -> %s" % (orig, new))
            out.append("      " + new)
            continue

        elif rule == R13:
            fm = re.match(r"\s*(\d+)\s+FORMAT\s*\((.*)\)\s*$", line, re.I)
            if not fm:
                out.append(line)
                continue
            label, spec = int(fm.group(1)), fm.group(2)
            pvars = print_vars_by_label.get(label, [])
            state = [0]

            def gsub(mm):
                cnt, w, d = mm.group(1), mm.group(2), mm.group(3)
                rep = int(cnt) if cnt else 1
                name = pvars[state[0]] if state[0] < len(pvars) else "X"
                state[0] += rep
                base = name.upper().split("(")[0]
                typ = var_types.get(base, _implicit_type(base))
                if typ == "DP":
                    body = "D%s.%s" % (w, d or "0")
                elif typ == "COMPLEX":
                    body = "%dE%s.%s" % (2 * rep, w, d or "0")
                    return body
                elif typ == "INTEGER":
                    body = "I%s" % w
                elif typ == "LOGICAL":
                    body = "L1"
                else:
                    body = "E%s.%s" % (w, d or "0")
                return (cnt or "") + body

            newspec = re.sub(r"(\d+)?G\s*(\d+)(?:\.(\d+))?", gsub, spec, flags=re.I)
            if newspec == spec:
                out.append(line)
                continue
            new = "%d FORMAT(%s)" % (label, newspec)
            out.append("C@ %s -> %s" % (orig, new))
            out.append(_label_field(label) + " FORMAT(%s)" % newspec)
            continue

        elif rule == R21:
            new = re.sub(r"(\d+P)\s*,\s*(?=[EFGDIAL])", r"\1", line, flags=re.I)
            if new == line:
                out.append(line)
                continue
            out.append("C@ %s -> %s" % (orig, new.strip()))
            out.append(new)
            continue

        elif rule in (R_OPEN, R_CLOSE, R_INQ, R_FWRIT, R_FREAD,
                      R_UWRIT, R_UREAD):
            # ---- wave F: F77 file I/O -> PERSO 0o2320 CALL bridge --------
            unit = _unit_of(lines, idx)
            emit_filmap(unit)
            body = re.sub(r"^\s*\d+\s+", "", orig)
            ctrl = _io_control(body)
            u = ctrl.get("UNIT") or ctrl.get("U")
            if not u or not re.match(r"^\d+$", u):
                raise SystemExit("cannot parse unit on line %d: %s" % (idx, orig))
            k = _io_iostat(ctrl)
            if k and k.upper() not in var_types:
                _decl(unit, "      INTEGER %s" % k)
            kv = io_status(k)
            errlab = ctrl.get("ERR")
            endlab = ctrl.get("END")
            out.append("C@ F77A %s -> ZF bridge" % body[:64])
            # Preserve a source statement label (e.g. "90 CLOSE(u)"): the
            # lowered CALL otherwise drops it and GO TO 90 becomes undefined.
            lm = re.match(r"^\s*(\d+)\s+", orig)
            if lm:
                out.append(_label_field(int(lm.group(1))) + " CONTINUE")

            if rule == R_OPEN:
                st = STATUS_CODES.get(
                    (ctrl.get("STATUS") or "'UNKNOWN'").strip("'").upper(), 0)
                ac = 1 if (ctrl.get("ACCESS") or "").strip("'").upper() == "DIRECT" else 0
                fm = 1 if (ctrl.get("FORM") or "").strip("'").upper() == "UNFORMATTED" else 0
                rl = ctrl.get("RECL") or "0"
                # Extra attributes ride in FILMAP slots 4..7: the PERSO API
                # deliberately has only (NAME,LUN,IST) (doc 34 §2).
                out.append("      FM(4)=%d" % st)
                out.append("      FM(5)=%d" % ac)
                out.append("      FM(6)=%d" % fm)
                out.append("      FM(7)=%s" % rl)
                fname = ctrl.get("FILE")
                if fname:
                    nmvar = "FMN%s" % u
                    if (unit, nmvar) not in fname_units:
                        fname_units.add((unit, nmvar))
                        _decl(unit, *_gost_name_words(fname, nmvar))
                    nmarg = nmvar
                else:
                    nmarg = "0"
                out.append("      CALL ZFOPEN(%s,%s,FM(1))" % (nmarg, u))

            elif rule == R_CLOSE:
                delv = 1 if (ctrl.get("STATUS") or "").strip("'").upper() == "DELETE" else 0
                out.append("      CALL ZFCLOSE(%s,%d,FM(1))" % (u, delv))

            elif rule == R_INQ:
                op = ctrl.get("OPENED") or "FM(2)"
                ex = ctrl.get("EXIST") or "FM(3)"
                out.append("      CALL ZFINQ(%s,%s,%s,FM(1))" % (u, op, ex))

            elif rule == R_FWRIT:
                fmt = ctrl.get("P2") or "*"
                items = re.sub(r"^\s*WRITE\s*\([^)]*\)\s*", "", body, flags=re.I).strip()
                if fmt == "*":
                    fmt = str(io_list_format(items))
                emit_iobuf(unit, u)
                out.append("      ENCODE(%d,%s,IB%s) %s" %
                           (IOBUF_WORDS * 6, fmt, u, items))
                out.append("      CALL ZFWRIT(%s,IB%s,%d,FM(1))" %
                           (u, u, IOBUF_WORDS))

            elif rule == R_FREAD:
                fmt = ctrl.get("P2") or "*"
                items = re.sub(r"^\s*READ\s*\([^)]*\)\s*", "", body, flags=re.I).strip()
                if fmt == "*":
                    fmt = str(io_list_format(items))
                emit_iobuf(unit, u)
                out.append("      CALL ZFREAD(%s,IB%s,%d,FM(1))" %
                           (u, u, IOBUF_WORDS))
                if k:
                    out.append("      %s = FM(1)" % k)
                if endlab:
                    out.append("      IF (FM(1) .EQ. -1) GO TO %s" % endlab)
                out.append("      DECODE(%d,%s,IB%s) %s" %
                           (IOBUF_WORDS * 6, fmt, u, items))

            else:  # R_UWRIT / R_UREAD: pack the list into one INTEGER record
                items = re.sub(r"^\s*(WRITE|READ)\s*\([^)]*\)\s*", "",
                               body, flags=re.I).strip()
                vals = [v.strip() for v in _split_top(items) if v.strip()]
                if not vals:
                    raise SystemExit("empty unformatted I/O list on line %d" % idx)
                if len(vals) > IOBUF_WORDS:
                    raise SystemExit("unformatted list > %d words on line %d"
                                     % (IOBUF_WORDS, idx))
                emit_iobuf(unit, u)
                if rule == R_UWRIT:
                    for i, v in enumerate(vals, 1):
                        out.append("      IB%s(%d)=%s" % (u, i, v))
                    out.append("      CALL ZFWRIT(%s,IB%s,%d,FM(1))" %
                               (u, u, len(vals)))
                else:
                    out.append("      CALL ZFREAD(%s,IB%s,%d,FM(1))" %
                               (u, u, len(vals)))
                    if k:
                        out.append("      %s = FM(1)" % k)
                    if endlab:
                        out.append("      IF (FM(1) .EQ. -1) GO TO %s" % endlab)
                    for i, v in enumerate(vals, 1):
                        out.append("      %s=IB%s(%d)" % (v, u, i))

            if k and rule not in (R_FREAD, R_UREAD):
                out.append("      %s = FM(1)" % k)
            if errlab:
                out.append("      IF (%s .NE. 0) GO TO %s" % (kv, errlab))
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
        emit_e9_after(idx)

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

    # wave F (rules 34-40): hoist the FILMAP / buffer / name declarations to
    # the top of each program unit.  FOREX 2.02 rejects a declaration that
    # appears after an executable statement (ERR 04441).
    if fio_decls:
        inserts = []
        for i, ln in enumerate(out):
            hm = re.match(r"\s*(PROGRAM|SUBROUTINE|FUNCTION|BLOCK\s+DATA)\s+([A-Za-z]\w*)",
                          ln, re.I)
            if hm and hm.group(2).upper() in fio_decls:
                inserts.append((i + 1, fio_decls[hm.group(2).upper()]))
        for pos, decls in reversed(inserts):
            out[pos:pos] = decls

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

    # R-F11: one BLOCK DATA per SAVEd unit, appended after the last END.
    # FORMAT/loop-closure insertions above stay before the final END.
    if f11_info:
        out.append("C@ (R-F11) -> BLOCK DATA for SAVEd variables")
        for block, names, dlines in f11_info.values():
            out.append("      BLOCK DATA")
            for nm in names:
                typ = var_types.get(nm.upper(), _implicit_type(nm))
                out.append("      %s %s" % (typ, nm))
            out.append("      COMMON /%s/%s" % (block, ",".join(names)))
            for j in dlines:
                out.append("      " + lines[j - 1].strip())
            out.append("      END")

    # Rule 20: any identifier longer than six characters is a hard error
    # (A5: silent 6-char truncation).  Keywords and the name of the program
    # unit itself are not identifiers subject to the F77 length limit.
    names_by_line = {}
    # 777004 kind=20 carries one char per record (pos = 1..M).  A line may
    # contain several long identifiers, so consume the records in emission
    # order; the pos-keyed aux4 map would overwrite their overlapping chars.
    for a in data.get("aux", []):
        if a["kind"] != 20:
            continue
        idx = seq_to_line.get(a["seq"], a["seq"])
        if a["pos"] == 1 or idx not in names_by_line or not names_by_line[idx][-1]:
            names_by_line.setdefault(idx, []).append("")
        names_by_line[idx][-1] += chr(a["value"])
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
        "*perso:602320,cont",   # doc 34 H8: PERSO 0o2320 file bridge
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
