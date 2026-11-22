#!/usr/bin/env python3
"""Synthetic structured-IR token interface for X/Y (limit-lifting step 2).

A token is a 3-tuple ``(kind, op, arg)`` produced in evaluation order by a
stack machine.  This is the plug-in point the lead will drive from the real
Fortran IR 777005 records; nothing in FRONT.FTN is edited here.

Token kinds
-----------
``('CONST', None, <float>)``   push a numeric literal
``('VAR',   None, <str>)``     push the current value of a variable
``('STORE', <str>, None)``     pop a value into the named variable
``('ADD',   None, None)``      pop two values, push their sum

The canonical token program for the Fortran statements

        X = 1.0
        Y = X + 2.0

is ``TOKENS_X1_ADD2`` below.  The interpreter only accepts expressions of the
form ``Y = X + <literal>`` so that the digit weights can be split into an X
contribution and an addend contribution that the BESM-6 ARX chain adds into
the GOST words at run time.
"""

# --- canonical synthetic token programs ------------------------------------
# (kind, op, arg)
TOKENS_X1_ADD2 = [
    ('CONST', None, 1.0),       # X = 1.0
    ('STORE', 'X', None),
    ('VAR',   None, 'X'),       # Y = X + 2.0
    ('CONST', None, 2.0),
    ('ADD',   None, None),
    ('STORE', 'Y', None),
]


def tokens_for(x_value, add_value):
    """Build a token program for ``X=<x_value>; Y=X+<add_value>``."""
    return [
        ('CONST', None, float(x_value)),
        ('STORE', 'X', None),
        ('VAR',   None, 'X'),
        ('CONST', None, float(add_value)),
        ('ADD',   None, None),
        ('STORE', 'Y', None),
    ]


def interpret(tokens, x_name='X', y_name='Y'):
    """Run the token stack machine.

    Returns ``dict(x=..., y=..., add=..., x_const=..., add_const=...)`` where
    ``add`` is the literal addend used in the Y=X+add expression.  The call
    rejects programs whose Y definition is not exactly ``X + literal`` so the
    runtime decomposition stays honest.
    """
    stack = []
    env = {}
    # Track provenance of pushed values: ('X', None) or ('CONST', value).
    prov = []
    for kind, op, arg in tokens:
        if kind == 'CONST':
            stack.append(float(arg))
            prov.append(('CONST', float(arg)))
        elif kind == 'VAR':
            if arg not in env:
                raise ValueError('token VAR references unbound %r' % arg)
            stack.append(env[arg])
            prov.append((arg, None))
        elif kind == 'STORE':
            if not stack:
                raise ValueError('token STORE with empty stack')
            env[op] = stack.pop()
            prov.pop()
        elif kind == 'ADD':
            if len(stack) < 2:
                raise ValueError('token ADD with <2 stack values')
            b = stack.pop(); pb = prov.pop()
            a = stack.pop(); pa = prov.pop()
            stack.append(a + b)
            # record a minimal additive provenance (left + right)
            prov.append(('ADD', (pa, pb)))
        else:
            raise ValueError('unknown token kind %r' % kind)
    if x_name not in env or y_name not in env:
        raise ValueError('token program must define %s and %s' % (x_name, y_name))

    # Recover the additive structure from the last STORE of Y.  The canonical
    # program pushes VAR X then CONST add then ADD; find that pattern on Y.
    y_def = None
    for i, (kind, op, arg) in enumerate(tokens):
        if kind == 'STORE' and op == y_name:
            # walk backwards: ADD, CONST, VAR X
            j = i - 1
            if j >= 0 and tokens[j][0] == 'ADD':
                rb = tokens[j - 1]; ra = tokens[j - 2]
                if rb[0] == 'CONST' and ra[0] == 'VAR' and ra[2] == x_name:
                    y_def = (x_name, float(rb[2]))
    if y_def is None:
        raise ValueError('Y must be defined as X + <literal> in the token stream')

    return {'x': env[x_name], 'y': env[y_name], 'add': y_def[1],
            'x_const': y_def[1] * 0 + env[x_name]}


if __name__ == '__main__':
    for toks in (TOKENS_X1_ADD2, tokens_for(2, 2), tokens_for(2, 3)):
        print(interpret(toks))
