#!/usr/bin/env python3
"""General postfix expression evaluation driven ONLY by real FRONT 777005 IR.

No value is read from the Fortran deck text here: the caller edits the deck to
make FRONT emit records, and every numeric value used below comes from the
777005 / 777002 / 777001 records in the captured FRONT call output.
"""
from decimal import Decimal, ROUND_HALF_UP
import re

VARS = {1: 'X', 2: 'Y', 3: 'N', 4: 'I'}
OPNAMES = {1: '+', 2: '-', 3: '*', 4: '/', 6: 'NEG'}
CENT = Decimal('0.01')


def lhs_by_seq(ir_text):
    """LHS name per logical-line seq, from the 777002 ASCII stream (as in test 77)."""
    rows = []
    for line in ir_text.splitlines():
        p = line.split()
        if len(p) >= 4 and p[0] == '777002':
            rows.append((int(p[1]), int(p[3])))
    by_seq = {}
    for seq, code in rows:
        by_seq.setdefault(seq, []).append(chr(code))
    return {seq: ''.join(codes).split('=')[0].strip()
            for seq, codes in by_seq.items() if '=' in ''.join(codes)}


def bound_from_ir(ir_text):
    """DO bound B from the 777001/777002 stream of the DO statement (as in test 77)."""
    rows = []
    for line in ir_text.splitlines():
        p = line.split()
        if len(p) >= 3 and p[0].startswith('777'):
            rows.append([int(x) for x in p])
    seq = next(r[1] for r in rows if r[0] == 777001 and r[2] == 32)
    codes = [r[3] for r in rows if r[0] == 777002 and r[1] == seq]
    line = ''.join(chr(c) for c in codes)
    m = re.search(r'I\s*=\s*\d+\s*,\s*(\d+)', line)
    if not m:
        raise ValueError('no DO bound in IR: %r' % line)
    return int(m.group(1))


def records(call_text):
    out = []
    for line in call_text.splitlines():
        m = re.match(r'^\s*777005\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s*$', line)
        if m:
            out.append(tuple(int(v) for v in m.groups()))
    if not out:
        raise ValueError('no 777005 records in FRONT output')
    return out


def tokens(recs, ir_text):
    """Decode 777005 records into (kind, op, arg) tokens in evaluation order.

    A STORE is appended after the last token of each seq (assignment) group.
    Returns (token_list, per_seq_record_counts).
    """
    lhs = lhs_by_seq(ir_text)
    toks = []
    counts = {}
    for i, (seq, kind, op, a1, a2) in enumerate(recs):
        counts[seq] = counts.get(seq, 0) + 1
        if kind == 1:
            toks.append(('CONST', None, Decimal(a1) / 100))
        elif kind == 2:
            if a1 not in VARS:
                raise ValueError('unsupported variable index %d' % a1)
            toks.append(('VAR', None, VARS[a1]))
        elif kind == 3:
            if op not in (1, 2, 3, 4):
                raise ValueError('unsupported binary op %d' % op)
            toks.append(('BIN', op, None))
        elif kind == 4 and op == 6:
            toks.append(('NEG', None, None))
        else:
            raise ValueError('unsupported token kind=%d op=%d' % (kind, op))
        last = (i + 1 == len(recs)) or (recs[i + 1][0] != seq)
        if last and seq in lhs:
            toks.append(('STORE', lhs[seq], None))
    return toks, counts


def token_program(call_text, ir_text):
    """Convenience wrapper returning (tokens, recs, bound)."""
    recs = records(call_text)
    toks, counts = tokens(recs, ir_text)
    return toks, recs, count_bound(call_text, ir_text), counts


def count_bound(call_text, ir_text):
    return bound_from_ir(ir_text)


def evaluate(toks):
    """Run the postfix stack machine; return the variable environment (Decimal)."""
    stack = []
    env = {}
    for kind, op, arg in toks:
        if kind == 'CONST':
            stack.append(arg)
        elif kind == 'VAR':
            if arg not in env:
                # I is set by the DO statement, not by an assignment record.
                env[arg] = Decimal(0)
            stack.append(env[arg])
        elif kind == 'NEG':
            if not stack:
                raise ValueError('NEG with empty stack')
            stack.append(-stack.pop())
        elif kind == 'BIN':
            if len(stack) < 2:
                raise ValueError('BIN with <2 stack values')
            b, a = stack.pop(), stack.pop()
            if op == 1:
                stack.append(a + b)
            elif op == 2:
                stack.append(a - b)
            elif op == 3:
                stack.append(a * b)
            elif op == 4:
                if b == 0:
                    raise ZeroDivisionError('division by zero in IR expression')
                stack.append((a / b).quantize(CENT, rounding=ROUND_HALF_UP))
            else:
                raise ValueError('unknown binary op')
        elif kind == 'STORE':
            if not stack:
                raise ValueError('STORE with empty stack')
            env[op] = stack.pop()
        else:
            raise ValueError('unknown token %r' % (kind,))
    if stack:
        raise ValueError('non-empty stack after token program: %r' % stack)
    return env


def digits(value, int_width=2, frac_width=2):
    """Return (sign_code, [int digits], [frac digits]) for a Decimal value.

    sign_code is '-' (GOST 11) for negative, ' ' (GOST 15) otherwise.
    Magnitude is limited to int_width integer digits after rounding.
    """
    v = Decimal(value).quantize(CENT, rounding=ROUND_HALF_UP)
    neg = v < 0
    a = -v if neg else v
    if a >= Decimal(10) ** int_width:
        raise OverflowError('value %s needs more than %d integer digits' %
                            (v, int_width))
    scaled = int((a * (10 ** frac_width)).quantize(Decimal(1), rounding=ROUND_HALF_UP))
    s = str(scaled).zfill(int_width + frac_width)
    ints = [int(c) for c in s[:int_width]]
    fracs = [int(c) for c in s[int_width:]]
    return ('-' if neg else ' '), ints, fracs
