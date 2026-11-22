#!/usr/bin/env python3
"""Phase-4 XY codegen: FRONT.FTN IR rule-31/35 -> emission-time folded GOST words.

The bound-driven leading N digits are still produced at RUN time by the proven
tests/72 ARX chain (codegen.stream).  This module only replaces the two GOST
text words body[0o27] / body[0o30] so that X and Y come from the IR:

  rule 31 ASCII 777002 -> LHS/RHS  -> constant-folded X, Y values
  rule 35 ASCII 777002 -> F10.2    -> number of decimals
  rule 32 ASCII 777002 -> DO bound -> passed to codegen.stream (N digits)

GOST bytes use the authoritative table from src/newcomp/EMIT.FTN (SUBROUTINE
GOSTEN, GT(64)), which equals monitor80-re/tools/encoding.cpp text_to_gost[64]
with index = ASCII - 31 (space -> 15, '.' -> 14, '0'..'9' -> 0..9).

Reuse: codegen.stream / codegen.gosten / codegen.MASK / emit_deck_surface from
the proven test 72 are imported verbatim, not copied.
"""
import ast
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
M35 = HERE.parent / '72-bound-driven'
sys.path.insert(0, str(M35))
import codegen as cg  # proven test-72 CODEGEN/EMIT wiring

MASK = (1 << 48) - 1

# EMIT.FTN SUBROUTINE GOSTEN GT(64), indices 1..64 (index 0 unused).
GT = [15, 0, 0, 0, 0, 0, 0, 0,
      18, 19, 25, 10, 13, 11, 14, 12,
      0, 1, 2, 3, 4, 5, 6, 7,
      8, 9, 0, 0, 0, 0, 0, 0,
      0, 32, 34, 49, 63, 37, 64, 65,
      45, 66, 67, 42, 68, 44, 69, 46,
      48, 70, 71, 72, 50, 73, 74, 75,
      53, 51, 76, 0, 0, 0, 0, 0]
assert len(GT) == 64


def gost_byte(ch):
    """Authoritative GOST-10859 byte for one ASCII character."""
    i = ord(ch) - 31
    if not 1 <= i <= 64:
        raise ValueError('character outside GOST table: %r' % ch)
    return GT[i - 1]


def gost_encode(text):
    return [gost_byte(c) for c in text]


def gosten(text):
    """Pack up to six ASCII chars into one 48-bit GOST word."""
    b = gost_encode(text)
    if len(b) > 6:
        raise ValueError('more than six GOST bytes: %r' % text)
    b += [0] * (6 - len(b))
    return (b[0] << 40) | (b[1] << 32) | (b[2] << 24) | \
           (b[3] << 16) | (b[4] << 8) | b[5]


# ---------------------------------------------------------------- IR parsing
def read_ir(path):
    rows = []
    for line in Path(path).read_text().splitlines():
        p = line.split()
        if len(p) >= 3 and p[0].startswith('777'):
            rows.append([int(x) for x in p])
    return rows


def ir_streams(rows):
    """seq -> (rule, itype, ASCII text) for every 777001 header line."""
    out = {}
    for r in rows:
        if r[0] == 777001:
            out[r[1]] = [r[2], r[3], None]
    for r in rows:
        if r[0] == 777002 and r[1] in out:
            if out[r[1]][2] is None:
                out[r[1]][2] = []
            out[r[1]][2].append(r[3])
    for seq in out:
        t = out[seq][2]
        out[seq][2] = ''.join(chr(c) for c in t) if t is not None else ''
    return out


_BINOPS = {ast.Add: lambda a, b: a + b, ast.Sub: lambda a, b: a - b,
           ast.Mult: lambda a, b: a * b, ast.Div: lambda a, b: a / b}


def eval_rhs(expr, env):
    """Constant-fold a *restricted* arithmetic expression using IR values only.

    Only numeric literals, previously assigned IR variables, + - * / and unary
    sign are accepted.  No deck text outside the IR is ever consulted.
    """
    tree = ast.parse(expr, mode='eval')

    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return float(n.value)
        if isinstance(n, ast.Name):
            if n.id not in env:
                raise ValueError('IR expression references unbound variable %r' % n.id)
            return env[n.id]
        if isinstance(n, ast.BinOp) and type(n.op) in _BINOPS:
            return _BINOPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.USub, ast.UAdd)):
            v = ev(n.operand)
            return -v if isinstance(n.op, ast.USub) else v
        raise ValueError('IR expression uses unsupported syntax: %s' % type(n).__name__)

    return ev(tree)


def parse_xy(rows, x_name='X', y_name='Y'):
    """Derive X, Y and FORMAT decimals from rule-31/rule-35 IR streams."""
    st = ir_streams(rows)
    env = {}
    assignments = []
    fmt = None
    for seq in sorted(st):
        rule, itype, text = st[seq]
        if rule == 31 and text:
            m = re.match(r'^([A-Z])\s*=\s*(.+)$', text.strip())
            if not m:
                raise ValueError('cannot parse IR rule-31 stream %r' % text)
            lhs, rhs = m.group(1), m.group(2).strip()
            env[lhs] = eval_rhs(rhs, env)   # sequential: Y=X+.. sees earlier X
            assignments.append((seq, lhs, rhs, env[lhs]))
        elif rule == 35 and text:
            fmt = text.strip()
    missing = [n for n in (x_name, y_name) if n not in env]
    if missing:
        raise ValueError('IR has no rule-31 assignment for %s' % ','.join(missing))
    if fmt is None:
        raise ValueError('IR has no rule-35 FORMAT stream')
    m = re.search(r'F\d+\.(\d+)', fmt)
    if not m:
        raise ValueError('no F<w>.<d> descriptor in IR FORMAT %r' % fmt)
    decimals = int(m.group(1))
    return {
        'x': env[x_name], 'y': env[y_name], 'decimals': decimals,
        'format': fmt, 'assignments': assignments, 'env': dict(env),
    }


def parse_bound(rows):
    """Derive the counted-DO upper bound from the rule-32 IR ASCII stream."""
    for seq, (rule, itype, text) in sorted(ir_streams(rows).items()):
        if rule == 32 and text:
            m = re.search(r'I\s*=\s*\d+\s*,\s*(\d+)', text)
            if m:
                return int(m.group(1))
    return None


def xy_words(x, y, decimals):
    """Pack the printed N-X-Y string into GOST words for body[0o27]/[0o30].

    The N digits are seeded as '01': the runtime ARX chain (test 72) turns
    them into '21' (bound 6) or '15' (bound 5).  X and Y are folded here.
    """
    xs = ('%.*f' % (decimals, x))
    ys = ('%.*f' % (decimals, y))
    text = '01 ' + xs + ' ' + ys
    if len(text) != 12:
        raise ValueError('GOST text must be exactly 12 chars for this layout: %r' % text)
    return gosten(text[:6]), gosten(text[6:12]), text


def combined_stream(rows, obj, zero=()):
    """Return (bound, xy_info, text, override_dict) from IR + object fixture.

    The N-digit words (9,10,0o41,0o42), descriptor and terminator come from the
    proven codegen.stream; only 0o27/0o30 are replaced with IR-derived X/Y.
    """
    bound = parse_bound(rows)
    if bound not in (5, 6):
        raise ValueError('unsupported IR DO bound %r (gate points are 5 and 6)' % bound)
    info = parse_xy(rows)
    a, b, text = xy_words(info['x'], info['y'], info['decimals'])
    ov = cg.stream(bound, obj)
    ov[0o27] = a & MASK
    ov[0o30] = b & MASK
    for k in zero:
        ov[k] = 0
    return bound, info, text, ov


def set_gost_byte(word, idx, byte):
    """Replace GOST byte idx (0..5, MSB first) of a 48-bit word."""
    if not 0 <= idx <= 5:
        raise ValueError('GOST byte index out of range')
    shift = 8 * (5 - idx)
    return (word & ~(0xff << shift)) | ((byte & 0xff) << shift)


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('ir_file')
    a = ap.parse_args()
    rows = read_ir(a.ir_file)
    info = parse_xy(rows)
    bound = parse_bound(rows)
    wa, wb, text = xy_words(info['x'], info['y'], info['decimals'])
    print('assignments:', info['assignments'])
    print('format=%r decimals=%d x=%s y=%s bound=%s' %
          (info['format'], info['decimals'], info['x'], info['y'], bound))
    print('seeded text=%r' % text)
    print('body[0o27]=%016o bytes=%r' % (wa, gost_encode(text[:6])))
    print('body[0o30]=%016o bytes=%r' % (wb, gost_encode(text[6:])))
