# Lifting the 2+2 digit output limit of our `*TRANS` contour

Date: 22.11.2026. All artifacts live only under
`/tmp/.private/azizz/opencode/re-forex-wide-output/`; emulator disk copies live in
`/dev/shm/re-forex-wide-machine/`. All runs are on COPIES of disks 2048/2053/2099
with per-case `HOME`/`BESM6_PATH` redirection. No repo edits, no git writes, no
live disks/tmux/processes, no dispak C patches. Zone `0o2350`
(`*TRANS:OURMRK*,,412350`) is used throughout. `КОНЕЦ ЗАДАЧИ` is present in all
10 machine cases; `rc=0` in all cases.

Toolchain caveat: the reused test-71 `inject.py`/`compile.py` FRONT pipeline
rewrites timestamped logs under the repo's `logs/` directory as a side effect.
The working tree already carried unrelated pre-existing modifications before
this task; none were reverted or staged, no source file was edited, and no git
write or commit was performed by this task. All authored files are in the temp
workspace above.

## 1. Result

**VERDICT: PASS.** The output width is lifted from 2 integer + 2 fractional
digits (`|v| <= 99.99`) to **4 integer + 2 fractional digits plus sign**
(`|v| <= 9999.99`). Real edited Fortran decks were compiled by FRONT test-71's
`inject.py --mode spec10` + `compile.py`, their `777005` IR was evaluated, and
the values were materialised at run time by OUR raw BESM-6 ARX (opcode 013)
words. `X=1234.56` prints `21 1234.56 2470.12`; `-1234.56` prints with both signs;
`9999.99` prints at the ceiling. 10/10 machine cases pass, with pre-run
zero-seed readback, CORE and MTR evidence. Values beyond `9999.99` raise
`OverflowError` (no silent wrap).

Reused unchanged: test-71 inject/compile, test-72 `codegen.py` word encoders /
opcodes / `digit_bytes`, test-76 `runtime_xy.py` zone-2350 install + console
runner, test-81 `expr_ir.py` IR evaluator, and the proven descriptor pair from
`ovl_our.hex`. New code is only `codegen_wide.py` (4-word GOST layout + wider
ARX chain) and `run_wide.py` (orchestration/A-B). The high-RAM 58-word area
(test 80) and raw BESM insert (test 83) were NOT needed; no extra instruction
was required.

## 2. New GOST layout (4 words from the descriptor address 0o2006)

Byte codes: digit `d` -> `d`, space -> 15, `.` -> 14, `-` -> 11,
EOF -> octal 231 (153). Digit bytes are seeded 0 on disk; sign, punctuation and
EOF are fixed bytes derived from IR. The descriptor pair at body `0o25/0o26`
still has `addr0 = addr1 = 0o2006` and was NOT changed: `*64` prints
sequentially from `0o2006` until the EOF byte, so extending the text by one word
only required moving EOF into the new last word.

```
word A @0o2006: [N_t][N_u][sp][X_sign][X_i0][X_i1]     digits: N_t,N_u,X_i0,X_i1
word B @0o2007: [X_i2][X_i3][ .  ][X_f0][X_f1][sp]      digits: X_i2,X_i3,X_f0,X_f1
word C @0o2010: [Y_sign][Y_i0][Y_i1][Y_i2][Y_i3][ .  ]  digits: Y_i0..Y_i3
word D @0o2011: [Y_f0][Y_f1][EOF][sp][sp][sp]           digits: Y_f0,Y_f1
```

Text = `NN<sp>XsXXXX.XX<sp>YsYYYY.YY<EOF>` (21 bytes, EOF at word-D byte 2).
N stays 2 digits and bound-driven (`B=6 -> 21`) as in tests 72/76/81.

A zero-seeded word set and its post-ARX result for `X=1234.56, Y=2470.12`:

| word | RAM | zero-seeded on disk | after our ARX words |
|:--|:--|:--|:--|
| A | 0o2006 | `[0,0,15,15,0,0]` | `[2,1,15,15,1,2]` |
| B | 0o2007 | `[0,0,14,0,0,15]` | `[3,4,14,5,6,15]` |
| C | 0o2010 | `[15,0,0,0,0,14]` | `[15,2,4,7,0,14]` |
| D | 0o2011 | `[0,0,153,15,15,15]` | `[1,2,153,15,15,15]` |

## 3. Word placement (all addresses derived from BASE = 0o1757)

| body | RAM | role |
|:--|:--|:--|
| 0o25 / 0o26 | 0o2004 / 0o2005 | proven `*64` descriptor pair (unchanged) |
| 0o27 | 0o2006 | GOST word A (zero-seeded) |
| 0o30 | 0o2007 | GOST word B (zero-seeded) |
| 0o31 | 0o2010 | GOST word C (zero-seeded) |
| 0o32 | 0o2011 | GOST word D + EOF (zero-seeded; free in tests 76/81) |
| 0o41 | 0o2020 | packed weight wA = `N_t<<40 | N_u<<32 | X_i0<<8 | X_i1` |
| 0o42 | 0o2021 | packed weight wB = `X_i2<<40 | X_i3<<32 | X_f0<<16 | X_f1<<8` |
| 0o43 | 0o2022 | packed weight wC = `Y_i0<<32 | Y_i1<<24 | Y_i2<<16 | Y_i3<<8` |
| 0o40 | 0o2017 | packed weight wD = `Y_f0<<40 | Y_f1<<32` (unused free cell in 81) |

All GOST/weight cells are inside the proven copy window `body[0..0o43]`. One
packed 48-bit weight per word (digit at byte k -> shift `8*(5-k)`) keeps the ARX
chain short and avoids inter-byte carry (`d <= 9 < 16`).

Runtime word stream (only `XTA / ARX / STO / *64 / UJ`, all in `body[9..16]`):

```
body[9]  = XTA 2006 / ARX 2020   ; ACC = word A + wA
body[10] = STO 2006 / XTA 2007   ; store A; ACC = word B
body[11] = ARX 2021 / STO 2007   ; ACC += wB; store B
body[12] = XTA 2010 / ARX 2022   ; ACC = word C + wC
body[13] = STO 2010 / XTA 2011   ; store C; ACC = word D
body[14] = ARX 2017 / STO 2011   ; ACC += wD; store D
body[15] = *64 2004              ; proven print
body[16] = uj 0(15)              ; proven return
```

## 4. Console A/B (all end with `КОНЕЦ ЗАДАЧИ`)

Driver: `run_wide.py`; per-case console + pre-run dumps in `evidence/*.txt`;
summary in `evidence/digest.txt` and `results.json`. `pre_ok=True` means all
14 digit bytes were ZERO on the installed disk copy before the run.

| Case | Source change | IR X / Y | Console | Result |
|:--|:--|:--|:--|:--|
| A_wide_pos | `X=1234.56 ; Y=X*2.0+1.0` | 1234.56 / 2470.12 | `21 1234.56 2470.12` | OK |
| B_neg | `X=-1234.56 ; Y=X+2.0` | -1234.56 / -1232.56 | `21 -1234.56 -1232.56` | OK (both signs) |
| C_lit_change | literal `2.0` -> `3.0` in Y | 1234.56 / 3704.68 | `21 1234.56 3704.68` | OK (digits change) |
| D_zero_wB | zero data word `body[0o42]` | 1234.56 / 2470.12 | `21 1200.00 2470.12` | OK (breaks) |
| E_zero_wD | zero data word `body[0o40]` | 1234.56 / 2470.12 | `21 1234.56 2470.00` | OK (breaks) |
| F_zero_code11 | zero code word `body[11]` | 1234.56 / 2470.12 | `21 1200.00 2470.12` | OK (breaks) |
| G_restore | restore wB/code[11] (same deck as A) | 1234.56 / 2470.12 | `21 1234.56 2470.12` | OK (restored) |
| M_wide_mtr | baseline with MTR | 1234.56 / 2470.12 | `21 1234.56 2470.12` | OK |
| N_wide_core | baseline with CORE | 1234.56 / 2470.12 | `21 1234.56 2470.12` | OK |
| L_maxval | `X=9999.99 ; Y=X-1.0` | 9999.99 / 9998.99 | `21 9999.99 9998.99` | OK (ceiling) |

All `pre_ok=True`. The double spaces in the raw console (`21  1234.56  2470.12`)
are collapsed to single spaces by `norm()` in the table, exactly as in test 81.

## 5. CORE / MTR evidence

CORE dump triggered at PC `0o1770` (entry `body[9]`), `evidence/N_wide_core_core.txt`:

```
A   RAM 2006 = 0000001703600000     wA  RAM 2020 = 0040040000000402
B   RAM 2007 = 0000001600000017     wB  RAM 2021 = 0060200001203000
C   RAM 2010 = 0360000000000016     wC  RAM 2022 = 0000100401600000
D   RAM 2011 = 0000023103607417     wD  RAM 2017 = 0020100000000000
```

MTR window `01770..01777`, `N=120`, `SKIP=6`; the first clean arm is in
`evidence/mtr_clean_wide.txt` (`AU` is the accumulator BEFORE the instruction):

```
MTR 01770L xta 2006(0) AU=0000000001146        ; seed word A
MTR 01770R arx 2020(0) AU=0001703600000        ; + wA
MTR 01771L atx 2006(0) AU=40041703600402       ; A = digits "21..12"
MTR 01771R xta 2007(0) AU=40041703600402
MTR 01772L arx 2021(0) AU=0001600000017        ; + wB
MTR 01772R atx 2007(0) AU=60201601203017       ; B = "34.56 "
MTR 01773L xta 2010(0) AU=60201601203017
MTR 01773R arx 2022(0) AU=360000000000016      ; + wC
MTR 01774L atx 2010(0) AU=360100401600016      ; C = " 2470."
MTR 01774R xta 2011(0) AU=360100401600016
MTR 01775L arx 2017(0) AU=0023103607417        ; + wD
MTR 01775R atx 2011(0) AU=20123103607417       ; D = "12<EOF>"
MTR 01776L *64  2004(0) AU=20123103607417      ; print -> 21 1234.56 2470.12
MTR 01777L uj   0(15)  AU=20123103607417
```

This confirms the PC reaches all four raw ARX additions (2020/2021/2022/2017)
and the accumulator transitions from zero-seeded bytes to the final digits.
Note: a wide MTR window re-arms in `cu.c` and floods the console with resident
passes through `01770..01777` (test 81 recorded the same effect); the quoted
first arm is the authoritative trace of OUR chain.

## 6. Exact remaining limits (no value is faked)

* **Magnitude:** 4 integer + 2 fractional digits, i.e. `|v| <= 9999.99` in
  steps of `0.01`. `10000.0` and `-10000.0` raise `OverflowError` in
  `expr_ir.digits(value, int_width=4)` instead of printing a wrapped value:
  `OverflowError: value 10000.00 needs more than 4 integer digits`.
  Values below `0.01` round to `0000.00` (F10.2 behaviour).
* **Missing primitive for a 5th integer digit:** one more GOST word (e.g.
  body `0o33` / RAM `0o2012`), one more packed weight word, one more
  `XTA/ARX/STO` pair in the chain, and EOF moved one word later. The descriptor
  needs NO change (it prints to EOF). The code window `body[9..16]` is full;
  the proven fallback for the extra code is the 58 clean words at RAM
  `0o30114..0o30205` (zone N+3, test 80), called from `body[9]`. This extension
  was not attempted and is not claimed as done.
* **N** remains 2 digits and bound-driven, unchanged from tests 72/76/81.
* Folded (not runtime) multiply/divide; no arrays/functions/`**`/exponents
  (inherited from test 81). Fixed-width fields print leading zeros, e.g.
  `-12.34` renders as `-0012.34` at 4-digit width; this is correct numeric
  value, not byte-identical to FOREX's right-justified F10.2 spacing.

## 7. Reproduce / evidence index

```
cd /tmp/.private/azizz/opencode/re-forex-wide-output
python3 run_wide.py                  # 10 cases -> results.json
```

| path | content |
|:--|:--|
| `codegen_wide.py`, `run_wide.py` | new wide layout + A/B orchestration |
| `expr_ir.py`, `front_probe.py`, `runtime_xy.py`, `codegen.py`, `installer.py` | copied proven modules (patched only for copy-relative paths) |
| `evidence/*_ir.txt` | FRONT 777005 records, tokens, digits, weights per case |
| `evidence/*.txt`, `evidence/digest.txt`, `results.json` | console + pre-run + A/B |
| `evidence/N_wide_core_core.txt` | CORE dump of installed GOST/weight words |
| `evidence/mtr_clean_wide.txt` | MTR trace of the 4-word ARX chain |

DONE
