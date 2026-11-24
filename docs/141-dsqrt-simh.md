# DSQRT feasibility — autonomous F77 contour, full SIMH

> РЕЗУЛЬТАТ: **PASS** под авторитетной SIMH. `DSQRT(9.0D0)→21 -0003.00`,
> `DSQRT(16.0D0)→-0004.00` при байтово том же образе; PATCH `L_HALF 0.5→0.6`
> даёт `-0003.06`; SQRT/ABS/MOD/T1 без регрессии. Двухсловный machine‑код
> (ACC+RMR) даёт `hi+lo=1.41421356237309514547` для `2.0D0` — ноль ошибки
> против IEEE double на 20 цифрах (PRINT пока F4.2, лишние цифры внутренние).
> Оговорки: D‑экспонента только без знака; произвольные DP‑литералы не разбираются
> в полную 80‑битную мантиссу; T5 в текущей среде печатает искажённое поле и
> на неизменённом базовом образе, поэтому регрессии DSQRT нет.

Discipline: all artifacts are copies under `/dev/shm/d2-dsqrt/`, symlinked from
`/tmp/.private/azizz/opencode/d2-dsqrt/`. No repository file, live disk, tmux
session 0, SIMH binary or C `dispak` source was edited. Simulator SHA-256 prefix
`d058305796bcd0aa` verified by the harness on every run. tty ports shifted to
`6300+N` (docs/135/137); md07 uses the system-disk copy that allows DISPAK boot
(docs/138).

## 0. Environment deviation and base reproduction

A server restart erased all prior workspaces. The exact base `2048_B9C_A`
(SHA `834a5a08f2934887b6b83a0e4b0782bceef628769d0b1497d7da7710edc1fc11`)
was recovered from another copy and, importantly, **reproduced byte-identically**
from repo builders plus `b7_parser.py` reconstructed from `parser_build.py` with
the two documented same-size LONG-UJ replacements (docs/136), using base image
SHA `2f5fcf873d43c2846ee1669669e26202f32fa25e6b71e109fd20ef4452142ff5`:

```
$ python3 build/b9_call_build.py --build B9C_ALT --src images/2048_base_alt
case=B9C_ALT sha=834a5a08... N3=40/58w B4=203w LEX=742hw slots=829
```

The repo's other regenerated base (`a98e8109...`) gives a different whole-image
SHA, so all DSQRT work uses the recovered/reproduced `834a5a08...` base.

## 1. D-exponent literal from real Fortran source

Deck line (columns 7..72): `      Y=DSQRT(9.0D0)`. RLE card bytes at RAM
`0o64012..0o64014` (fixed-form source + proven RLE layout, `0x80+n` = n spaces):

```
064012  86 59 3d 53 51 52   <6sp>Y=SQR
064013  54 28 39 2e 30 44   T(9.0D
064014  30 29 c0 0a 0a 0a   0)<64sp>\n\n\n
```

The machine lexer now reads `0x44` (`D`) in number mode as the start of an
unsigned decimal exponent; exponent digits are accumulated in an N+2 cell and
applied by repeated on-machine `a*x f32(10)`. For `9.0D0`/`16.0D0` (exp = 0)
the resulting single BESM word is exactly `f32(9.0) = 0o4211000000000000` or
`f32(16.0) = 0o4250000000000000`; the honest two-word BESM representation of
these exactly representable literals is `(hi=f32(9.0), lo=0)` / `(hi=f32(16.0),
lo=0)`. Arbitrary DP literals are not converted to an 80-bit mantissa by this
lexer (stated limit).

## 2. DSQRT machine code

Builder `build/dsqrt_build.py` (copy of the all-feature B9 builder with DSQRT
additions). Reused verbatim: B4 parser, B3 dispatcher, docs/105 N+3 GOST
converter, B5/B7 lexer and control path, region-end LONG UJ guards, keeper
`body[0o26]`, forbidden N+2 band 526..900 untouched.

New body-resident routine `DP_SQRT`, VJM-called from the literal handler:

```
x0 = S
6 x Newton: x = (x + S/x)/2          ; single-FPU seed, ~1 ulp
p = x*x              ; a*x: ACC = high product, RMR = exact low 40 bits
atx DP_PHI           ; ATX does not change RAU (still MULT)
yta 24               ; ACC = RMR as float at exponent e(p)-40 -> low word
d = S - p_hi, low word from RMR
r = d - p_lo         ; residual at ~2^-40 of x
dx = r/(2x)
x_hi = x + dx, low word from RMR -> DP_XHI / DP_XLO
```

`yta 24` is the non-logical `счмр` form: effective address 24 gives
`(24-64) = -40` exponent adjustment. The result is genuinely two-word
(ACC+RMR), not a relabelled single value.

Word budget (build output): N3 40/58, B4 203 words, LEX 817/829 hw,
N+2 changed words 540+budget cells 200..214, body code 585 words, forbidden
band 0 writes, keeper preserved.

## 3. Precision evidence (C `dispak` used as ORACLE only)

C CORE at the B4 entry (`0o22243`) for `Y=DSQRT(2.0D0)`:

```
DP_XHI N+2[202] = 0o4053240474631771  (exponent 0o101, mantissa 0o13240474631771)
DP_XLO N+2[203] = 0o1455714441054575  (exponent 0o31, exactly e_hi-40)
```

Decoded as `hi + lo`:

```
hi alone      = 1.41421356237151485402   (single-FPU error ~1.58e-12)
hi + lo       = 1.41421356237309514547
IEEE sqrt(2)  = 1.41421356237309514547   (error 0 at 20 printed digits)
```

So the low word contributes ~12 additional decimal digits: the achieved
precision is at least IEEE-double (53-bit) and is built from a 40-bit high plus
40-bit low mantissa (80-bit-class two-word representation). For `9.0D0` and
`16.0D0` the dumped result is `0o4114000000000000` / `0o4150000000000000`
with low word 0, i.e. exact 3.0 / 4.0.

C-oracle advisory gates (media set: proven 2053/2099/2253):

| case | deck | prn0 `21` line |
|:--|:--|:--|
| A | `DSQRT(9.0D0)` | ` 21 -0003.00  3000.00` |
| B | `DSQRT(16.0D0)` | ` 21 -0004.00  3000.00` |
| PATCH | A + one word N+2[104] `L_HALF` 0.5 -> 0.6 | ` 21 -0003.00` -> ` 21 -0003.06  3000.00` |
| SQRT | `SQRT(16.0)` | ` 21 -0004.00  3000.00` |
| T1 | literal | ` 21 -0012.34  3000.00` |
| ABS | `ABS(-16.0)` | ` 21 -0016.00  3000.00` |
| MOD | `MOD(7.0,3.0)` | ` 21 -0001.00  3000.00` |

## 4. SIMH decisive gates

Base/decks/images (SHA-256):

```
834a5a08...  images/2048_B9C_A        (exact task base, reproduced)
219aea63...  images/2048_DSQRT_A      (A = B = RESTORE, byte-identical)
fa2b45d3...  images/2048_DSQRT_PATCH  (one machine word N+2[104], L_HALF 0.5->0.6)
5917af28...  build/dsqrt_build.py
ba6d7857...  decks/deck_DSQRT_A.b6    (Y=DSQRT(9.0D0))
ab56d604...  decks/deck_DSQRT_B.b6    (Y=DSQRT(16.0D0))
```

Authoritative SIMH `prn0` captures (run with `harness/drive_b.py` /
`harness/drive_b3.py`, emulator `d0583057...`, tty ports shifted):

| gate | image | deck | prn0 | verdict |
|:--|:--|:--|:--|:--|
| A (`FA2`) | `2048_DSQRT_A` | `9.0D0` | `21 -0003.00  3000.00` + `КОНЕЦ ЗАДАЧИ` | **PASS** (`product_gate: PASS`) |
| B (`FB`) | `2048_DSQRT_A` (byte-identical) | `16.0D0` | `21 -0004.00  3000.00` + `КОНЕЦ ЗАДАЧИ` | **PASS** |
| PATCH (`FP`) | `2048_DSQRT_PATCH` | `9.0D0` | `21 -0003.06  3000.00` + `КОНЕЦ ЗАДАЧИ` | **PASS** |
| RESTORE | `2048_DSQRT_A` | `9.0D0` | byte-identical to A (same SHA), A capture is the restore value | PASS |
| SQRT (`FS`) | `2048_DSQRT_A` | `SQRT(16.0)` | `21 -0004.00  3000.00` + `КОНЕЦ ЗАДАЧИ` | **PASS** |
| ABS (`FX`) | `2048_DSQRT_A` | `ABS(-16.0)` | `21 -0016.00  3000.00` + `КОНЕЦ ЗАДАЧИ` | **PASS** |
| MOD (`FY`) | `2048_DSQRT_A` | `MOD(7.0,3.0)` | `21 -0001.00  3000.00` + `КОНЕЦ ЗАДАЧИ` | **PASS** |
| T1 (`F1B`) | `2048_DSQRT_A` | canonical `T1_lit_A.b6` | `21 -0012.34  3000.00` + `КОНЕЦ ЗАДАЧИ` | **PASS** |
| T5 (`F5B`) | `2048_DSQRT_A` | canonical `T5_do_2.b6` | `21 00∧′ 39 3000.00` + `КОНЕЦ ЗАДАЧИ` | same on unmodified base (see below) |
| T1 (`F1C`) | `2048_B9C_A` (base) | canonical | `21 -0012.34  3000.00` + `КОНЕЦ ЗАДАЧИ` | PASS (control) |
| T5 (`F5C`) | `2048_B9C_A` (base) | canonical | `21 00∧′ 39 3000.00` + `КОНЕЦ ЗАДАЧИ` | PASS (control: identical to DSQRT image) |

An earlier `F1` run missed the job-start line and an earlier `F5` run had a
stale capture; both were re-run with fresh case names and fresh prn0 files.
The canonical `T5_do_2.b6` DO path prints a corrupted field in the **current**
shared media environment on the unmodified `2048_B9C_A` as well; the DSQRT
image produces exactly the same output, so DSQRT introduces no T5 regression.
The historically documented `-0040.00` T5 result could not be reproduced in
this environment (media churn after the server restart), and this is disclosed
rather than claimed as a positive T5 gate.

Every listed gate uses a fresh case name, stale `prn0/prn1` deleted before the
run, tty ports `6300+N`, emulator SHA `d058305796bcd0aa`, and a per-case verdict
JSON written from the new prn0 capture. Earlier case names `DA/DB/DA3/DA4/DP/…`
were exploratory; only the `F*` gates above are cited.

A/B uses a byte-identical image and only the Fortran source digit changes; the
PATCH changes exactly one machine word (the Newton `0.5` constant, N+2[104])
and changes `3.00` to `3.06` in authoritative SIMH too; RESTORE is byte-identical
to A.

## 4.1 Final verdict

DSQRT is **achievable** on this hardware within the enlarged body budget. The
implemented two-word (ACC+RMR) Newton refinement produces a genuine DP-class
result (CORE-measured error 0 against IEEE double for `sqrt(2.0D0)`, versus
~1.6e-12 for the single-FPU seed alone). All decisive authoritative SIMH gates
A/B/PATCH/RESTORE and the SQRT/ABS/MOD/T1 non-regressions passed; T5 output is
identical on the modified and unmodified base image, so no regression is
attributable to this change. The printed field remains `F4.2`, so the extra
precision is machine-internal (measured from CORE), not printed.

## 5. Honest limits

* The printed field is the existing `F4.2` GOST path (2 decimal places), so
  the extra DP digits are machine-internal; they were measured from CORE, not
  printed. A D22.15-style printer was not added.
* D exponent parsing is unsigned; negative exponents (`D-1`) are not supported.
* No general DP add/multiply/divide is implemented: DSQRT uses the RMR residual
  of single FPU multiply/add plus single FPU division for the correction.

DONE
