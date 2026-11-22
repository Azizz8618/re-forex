# General postfix expression grammar for X/Y: IR-driven codegen (A/B proof)

Date: 22.11.2026. All artifacts live only under
`/tmp/.private/azizz/opencode/re-forex-grammar/`. No repo edits, no git writes,
no live disks/tmux/processes, no dispak C patches. `HOME` and `BESM6_PATH` were
redirected to per-case temp copies of disks 2048/2053/2099; zone `0o2350`
(`*TRANS:OURMRK*,,412350`) was used throughout.

## 1. Result

**Supported grammar is lifted from `Y = X + <literal>` to the full postfix RHS
that FRONT already emits in `777005`.** Real edited Fortran decks were compiled
by FRONT (test 71's `inject.py --mode spec10` + `compile.py`), the resulting
`777005` records were decoded and evaluated, and the values were materialised
at run time by our own BESM-6 ARX words. 11/11 machine cases pass with
`КОНЕЦ ЗАДАЧИ`; an extra IR-tamper case proves the numbers come from IR, not
from deck text. **VERDICT: PASS** within the stated capacity limits (§7).

Reused unchanged: `tests/71`'s inject/compile, `tests/72`'s `codegen.py`
(word encoders / opcodes / `digit_bytes`), `tests/76`'s `runtime_xy.py`
(zone-2350 install, desc/GOST fixture, console runner), and the proven
descriptor/EOF words from `ovl_our.hex`. New code is only the IR evaluator,
the wider GOST layout and the orchestration under this temp folder.

## 2. Supported grammar (what FRONT 777005 actually emits)

Verified with real decks (evidence: `evidence/*_ir.txt`):

| Feature | IR encoding | Example source | Postfix tokens |
|:--|:--|:--|:--|
| unsigned decimal literal | `kind=1, arg1 = real*100` | `2.0`, `12.0`, `0.25` | `LIT 200`, `LIT 1200`, `LIT 25` |
| variable | `kind=2, arg1`: X=1,Y=2,N=3,I=4 | `X` | `VAR X` |
| binary `+ - * /` | `kind=3, op=1/2/3/4` | `X*2.0+1.0` | `VAR X LIT 200 BIN* LIT 100 BIN+` |
| unary minus | `kind=4, op=6` | `X=-1.0` | `LIT 100 UN NEG` |
| parentheses | no token, precedence in FRONT's shunting-yard | `(X+1.0)*2.0` | `VAR X LIT 100 BIN+ LIT 200 BIN*` |

Not supported by FRONT today (so not by the consumer): arrays, functions,
`**`, multi-letter names, exponential literals. The consumer rejects any
unknown `kind/op` instead of guessing.

Evaluation is a postfix stack machine driven **only** by
`777005` records; LHS names come from `777002`, and the DO bound `B` (used for
the two leading `NN` digits, as in tests 72/76/77) from `777001/777002`.
`Decimal` arithmetic with `ROUND_HALF_UP` to 2 decimals reproduces F10.2
rounding; division by zero and stack underflow are hard errors.

## 3. Codegen strategy: folded arithmetic, runtime digit materialisation

### 3.1 Why folding (and not a runtime multiply opcode)

* The only proven runtime arithmetic on packed GOST bytes in this codebase is
  raw `слц`/ARX (opcode 013, end-around-carry add). Test 72/76 word encoders
  are reused verbatim.
* Floating `сл` (A+X) corrupts packed GOST words — recorded in
  `docs/corrections.md` (2026-11-22 16:00). CODEGEN.deck's N3E `сл` is replaced
  by ARX for the same reason.
* No proven packed-decimal multiply/divide opcode exists in CODEGEN.deck,
  EMIT.FTN or the design docs; the resident `FT*571/002/003` float→GOST chain
  cannot be called from the `*TRANS` body (LINK not patched, test 57/63 §3.2).
* Therefore `+ - * /` and unary minus are evaluated at **emission time from the
  IR records**; the resulting decimal digits are installed as ZERO-seeded GOST
  bytes and written by our own ARX words at run time. The MTR (§6) shows the
  accumulator changing from the seed to the final digits. No numeric value is
  baked into the printed GOST bytes before the run.

Causality is additionally proven by tampering with one `777005` record **after**
FRONT while leaving the Fortran deck untouched:
`777005 6 1 0 100 0` → `777005 6 1 0 300 0` (`+1.0` → `+3.0`).
Deck still says `Y=X*2.0+1.0`; console changed from `21 02.00 05.00` to
`21 02.00 07.00`. `VERDICT: PASS`.

### 3.2 GOST layout (3 words at RAM `0o2006/0o2007/0o2010`)

Descriptor pair at body `0o25/0o26` (`addr0=addr1=0o2006`) is the proven one.
Byte values are GOST-10859 codes: digit `d`→`d`, space→15, `.`→14, `-`→11,
EOF→**octal 231** (decimal 153). Byte 4 of word C is EOF, so printing stops
cleanly and `КОНЕЦ ЗАДАЧИ` follows.

```
word A @0o2006: [N_t][N_u][sp][X_sign][X_i_t][X_i_u]
word B @0o2007: [ .  ][X_f_t][X_f_u][sp][Y_sign][Y_i_t]
word C @0o2010: [Y_i_u][ .  ][Y_f_t][Y_f_u][EOF][sp]
```

Digital slots (10) are seeded to byte 0 on disk; sign, punctuation and EOF are
fixed bytes derived from IR. One packed 48-bit weight per GOST word (digit at
byte k → shift `8*(5-k)`) keeps the ARX chain short and avoids inter-byte carry.

### 3.3 Runtime word stream (all addresses derived from BASE `0o1757`)

```
body[9]  = XTA 2006 / ARX 2020   ; load word A, add packed N+X-integer digits
body[10] = STO 2006 / XTA 2007   ; store A, load word B
body[11] = ARX 2021 / STO 2007   ; add X-fraction + Y-tens digits, store B
body[12] = XTA 2010 / ARX 2022   ; load word C, add Y-units/fraction digits
body[13] = STO 2010 / STO 2010   ; store C
body[14] = XTA 2006 / XTA 2006   ; harmless spare (intentionally does not store C)
body[15] = *64 2004              ; proven print
body[16] = uj 0(15)              ; proven return
data: body[0o41]=wA @2020, body[0o42]=wB @2021, body[0o43]=wC @2022
```

Only `XTA/ARX/STO/*64/UJ` are used. Everything fits in the clean window
`body[1..0o43]` (RAM `0o1760..0o2022`); the extended/shifted window and high RAM
were not needed.

## 4. IR samples (from real Fortran decks)

`X=2.0 ; Y=X*2.0+1.0` (7 records, 10 tokens):
```
777005  2 1 0    0 0     LIT 0.00   (N=0)
777005  5 1 0  200 0     LIT 2.00   (X)
777005  6 2 0    1 0     VAR X
777005  6 1 0  200 0     LIT 2.00
777005  6 3 3    0 0     BIN *
777005  6 1 0  100 0     LIT 1.00
777005  6 3 1    0 0     BIN +
```
Operator A/B (`+`→`-`): last record becomes `777005 6 3 2 0 0` (`BIN -`).
Parentheses A/B (`Y=(X+1.0)*2.0`): token order becomes
`VAR X, LIT 100, BIN+, LIT 200, BIN*` (op tokens swap position in the records).
Division (`X=1.0 ; Y=X/4.0`, 5 records): `LIT 100, VAR X, LIT 400, BIN/`.
Unary (`X=-1.0 ; Y=X+2.0`, 6 records): `LIT 100, UN NEG (kind 4 op 6), ...`.
Multi-digit (`X=12.0`): literal record `arg1=1200`.

## 5. Console A/B (all end with `КОНЕЦ ЗАДАЧИ`)

| Case | Source change | IR-evaluated X,Y | Console | Result |
|:--|:--|:--|:--|:--:|
| A_mul_add | baseline `X*2.0+1.0` | 2, 5 | `21 02.00 05.00` | OK |
| B_sub | operator `+`→`-` | 2, 3 | `21 02.00 03.00` | OK |
| B_paren | `(X+1.0)*2.0` | 2, 6 | `21 02.00 06.00` | OK |
| B_x3 | operand `X=2.0`→`3.0` | 3, 7 | `21 03.00 07.00` | OK |
| C_div | `Y=X/4.0` | 1, 0.25 | `21 01.00 00.25` | OK |
| D_neg | `X=-1.0` (unary) | -1, 1 | `21 -01.00 01.00` | OK |
| E_wide | `X=12.0` | 12, 25 | `21 12.00 25.00` | OK |
| F_zero_wA | zero data word `body[0o41]` | 2, 5 | `00 00.00 05.00` | OK |
| G_zero_wC | zero data word `body[0o43]` | 2, 5 | `21 02.00 00.00` | OK |
| H_zero_c13 | zero code word `body[13]` | 2, 5 | `21 02.00 00.00` | OK |
| M_mtr | baseline with MTR | 2, 5 | `21 02.00 05.00` | OK |
| IR_tamper | deck unchanged, IR literal 100→300 | 2, 7 | `21 02.00 07.00` | OK |

Pre-run readback of the installed disks shows **all ten digit bytes = 0** in
every case (`pre_ok=True`); the digits appear only after our ARX words execute.
Zeroing the spare word `body[14]` was explicitly avoided in the A/B because it
is a benign reload, not a digit materialiser.

## 6. MTR trace (case M_mtr)

Obtained with `BESM6_DD_DEBUG=1 BESM6_MTR_LO=01770 BESM6_MTR_HI=01777
BESM6_MTR_N=100 BESM6_MTR_SKIP=6` (narrow window; a wide window re-arms the
tracer in `cu.c` and floods the console). `AU` is the accumulator **before**
the instruction. Clean block (`mtr_clean.txt`):

```
MTR 01770L xta 2006(0) AU=0000000001146      ; seed word A (digit bytes 0)
MTR 01770R arx 2020(0) AU=0001703600000      ; + wA (N=21, X tens/units)
MTR 01771L atx 2006(0) AU=40041703600002     ; A = digits "21..02"
MTR 01771R xta 2007(0) AU=40041703600002
MTR 01772L arx 2021(0) AU=340000003607400    ; + wB (X fraction, Y tens)
MTR 01772R atx 2007(0) AU=340000003607400
MTR 01773L xta 2010(0) AU=340000003607400
MTR 01773R arx 2022(0) AU=0700000114417      ; + wC (Y units/fraction)
MTR 01774L atx 2010(0) AU=120700000114417
MTR 01775L xta 2006(0) AU=120700000114417    ; spare, harmless
MTR 01776L *64  2004(0) AU=40041703600002    ; print -> 21 02.00 05.00
MTR 01777L uj   0(15)  AU=40041703600002
```

This confirms execution of our raw ARX additions at 2020/2021/2022 and the
accumulator transition from zero-seeded bytes to the final decimal digits.

## 7. Exact capacity limit (no value is faked)

* X and Y: **2 integer digits + 2 fractional digits plus a sign**, i.e.
  `|value| <= 99.99` in steps of `0.01`; `100.0` and `-100.0` raise
  `OverflowError` in `expr_ir.digits()` instead of printing a wrapped value.
  Values below `0.01` round to `00.00` (F10.2 behaviour).
* N: 2 digits, still bound-driven (`B=6 → 21`, `B=5 → 15`) as in tests 72/76;
  changing the DO bound in the deck changes `NN` through IR, not through text.
* The GOST text is exactly 3 words (16 text bytes + EOF at byte 16 + padding).
  To exceed `99.99` one needs one more digit slot per extra integer digit,
  i.e. more GOST words plus a repointed descriptor and a data area outside
  `body[0o43]`. The proven place for that is zone `N+3` (58 clean words at
  RAM `0o30114..0o30165`, test 80): move the GOST text and descriptor there,
  add the extra packed weight words and ARX halfwords, and set descriptor
  word 0's `addr0/addr1` to the new start. That is a separate, untested step;
  it was not needed for any case here, so it was not claimed as done.

Formatting note: integer fields are fixed-width, so small values print with a
leading zero (`02.00`, `-01.00`). This matches the numeric Fortran value; it is
not byte-identical to FOREX's right-justified F10.2 spacing.

## 8. Reproduce

```
cd /tmp/.private/azizz/opencode/re-forex-grammar
python3 front_probe.py                       # FRONT 777005 for all grammars
python3 run_cases.py                         # 11 cases -> results.json
python3 ir_tamper_proof.py                   # IR-only causality
```
Evidence: `evidence/*_ir.txt` (FRONT records + decoded tokens),
`machine/evidence/*.txt` (per-case console + pre-run dumps), `mtr_clean.txt`,
`results.json`.

## 9. Verdict and remaining limits

PASS for the full FRONT postfix grammar (literals, X/Y/N/I variables, `+ - * /`,
unary minus, parentheses) within the 2-integer/2-fraction-digit GOST capacity,
with IR-sourced values, runtime ARX materialisation, MTR confirmation and A/B
causality including zeroed code/data words. Remaining limits: folded (not
runtime) multiply/divide, no arrays/functions/`**`/exponents, fixed-width
leading zeros, and the `99.99` magnitude ceiling whose extension needs the
high-RAM descriptor work described in §7.

DONE
