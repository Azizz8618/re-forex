# machine-intr: F77 intrinsics in BESM-6 machine code inside zone-2350 contour

> ГЛАВНЫЙ РЕЗУЛЬТАТ: ABS, SQRT, MOD **PASS** под SIMH машинно‑кодом в
> контуре `0o2350` (A/B/A по одному слову, restore байтово тождествен):
> `3.00→5.00`, `3.00→4.00`, `1.00→2.00` соответственно. DSQRT **FAIL**:
> нет double FPU, софтверная DP требует >100 команд и не помещается в 58
> слов зоны `0o2353`. ABS требует `avx` (аппаратная смена знака), потому что
> отрицательные float на БЭСМ‑6 — дополнительный код мантиссы.

Date: 23.11.2026. Workspace `/tmp/.private/azizz/opencode/machine-intr/`
(bulky files under `/dev/shm/machine-intr/`, symlinked from the `/tmp` path;
the shared `/tmp` tmpfs is 100% full and `/dev/shm` is periodically exhausted by
concurrent agents, so this report lives on the root filesystem and is symlinked
from the required path). Repo, live disks, tmux session 0 and dispak C sources
were never edited. Every attached image was a copy (printer output redirected
to a private `-n prn0/prn1` path to avoid cross-agent clobber). Deck contains
exactly `ДИС 41(2048)^` + `*TRANS:OURMRK*,,412350` (no `*FOREX`/`*FTN`/`*perso`).
SIMH: `ДATA:` boot marker via `capture-pane`, all input via `send-keys`,
`ДАЙ А0` / `ДАЙ А1` / `НОМВ` before deck, post-job-start `НОМВ`, `set cpu debug`
MTR traces. C `dispak` was oracle only (source reading).

## VERDICT

| intrinsic | verdict | decisive A/B/A (printed X digit) |
|:--|:--|:--|
| ABS | **PASS** | `21 3.00 3.00` -> `21 5.00 3.00` -> `21 3.00 3.00` |
| SQRT | **PASS** | `21 3.00 3.00` -> `21 4.00 3.00` -> `21 3.00 3.00` |
| MOD | **PASS** | `21 1.00 3.00` -> `21 2.00 3.00` -> `21 1.00 3.00` |
| DSQRT | **FAIL / infeasible** | concrete blocker in §6; no genuine double result |

All PASS cases reached `КОНЕЦ ЗАДАЧИ`; console showed `2048 - 41` and
`B075-1 410300000000`. Each A/B patches exactly one word (a machine-code
constant) in our contour; restore is byte-identical (same SHA-256).

---

## 1. How it was installed (reusing the proven base verbatim)

Same mechanism as `/tmp/.private/azizz/opencode/ftgost-contour/report.md` and
`docs/89-machine-float-gost-pass.md`:

- single same-length substitution in body zone `0o2351`: `body[0o11]` (RAM
  `0o1770` L) = LONG `uj 30114`, diverting execution into our routine;
- `body[0o27]` (RAM `0o2006`, GOST word A) X-digit byte zeroed, line prefix `2`;
- 58 clean words of zone `N+3` (RAM `0o30114..0o30205`) hold routine +
  constants;
- `utc 30000` in the RIGHT halfword of each word arms M20 for the next LEFT
  halfword (one-instruction modifier; two consecutive `utc` accumulate
  `30000 -> 60000` and trap);
- every intrinsic computes a float with on-machine FPU/bitwise ops, then feeds
  it through the PROVEN converter: `aex/e+x` derives the asx control word from
  the result's own exponent, `aax MASK40` isolates the mantissa, `asx` turns it
  into an integer digit, `asx CW_L16` + `arx 2006` deposits the GOST byte,
  `*64 2004` prints it.

Instruction encodings (verified against `besm6_cpu.c:1125-1410`):
`0o004 a+x` (float add), `0o005 a-x` (float subtract), `0o16 a/x`, `0o17 a*x`,
`0o11 aax`, `0o12 aex`, `0o13 arx` (INTEGER add, used only for GOST deposit),
`0o14 avx` (hardware sign change), `0o15 aox`, `0o24 e+x`, `0o26 asx`.

### ABS machine code (14 words, `30114..30131`)

```
30115 L xta 0160      ; load -X (valid two's-complement negative float)
30116 L avx  0177     ; operand bit40 set -> negate ACC -> +X
30117 L atx  0166     ; store result float
30120 L xta 0166
30121 L aex  0173     ; exponent <- 127-e
30122 L e+x  0174     ; exponent <- 168-e (asx control word)
30123 L atx  0167
30124 L xta 0166
30125 L aax  0175     ; isolate 40-bit mantissa
30126 L asx  0167     ; mantissa -> integer digit
30127 L asx  0176     ; digit << 16 (GOST byte 3)
30127 R arx  2006     ; += GOST word A
30130 L atx  2006
30130 R *64  2004     ; print
30131 L uj   0(15)    ; return to resident at 0o1764
```

### SQRT machine code (35 words): Newton, 4 iterations

```
30115 L xta 0160 ; 30116 L atx 0171        ; x0 = S
loop x4:
  xta 0160 ; a/x 0171 ; a+x 0171 ; a*x 0172 ; atx 0171   ; x = (x + S/x)/2
30143 L xta 0171 ; 30144 L atx 0166        ; result -> converter
... same converter as ABS ...
```
`0o172 = f32(0.5)`. Four iterations: sqrt(9)->3.000065, sqrt(16)->4.003,
both truncate to the correct integer digit.

### MOD machine code (28 words): exact-integer AINT via bitwise mask

```
30115 L xta 0160 ; 30116 L a/x 0161 ; 30117 L atx 0162    ; Q = X/Y
30120 L xta 0175 ; 30121 L asx 0162 ; 30122 L aex 0175    ; mantissa mask bits n..39
30123 L aox 0201 ; 30124 L atx 0163                       ; +all exponent bits/sign -> full mask
30125 L xta 0162 ; 30126 L aax 0163 ; 30127 L atx 0164    ; AINT(Q) = Q & mask (float)
30130 L xta 0161 ; 30131 L a*x 0164 ; 30132 L atx 0165    ; Y*AINT(Q)
30135 L xta 0160 ; 30136 L a-x 0165 ; 30137 L atx 0166    ; X - Y*AINT(Q)
... same converter as ABS ...
```
The mask construction uses Q's own exponent: `asx A_Q` shifts `MASK40` right
by `(e_q-64) = 40-n`, then `aex MASK40` yields exactly bits `n..39` set. This
is exact truncation, not round-to-nearest. For X=9,Y=4: Q=2.25, mask keeps
mantissa bits 38..39, AINT=2, MOD=1. For X=9,Y=7: Q=1.2857, AINT=1, MOD=2.

---

## 2. Decisive A/B/A under full SIMH (raw ACPU)

Raw lines from `runs/acpu_<case>.txt` (`21` line + `КОНЕЦ ЗАДАЧИ`):

```
abs_a       :  21 3.00 3.00      abs_b       :  21 5.00 3.00
abs_restore :  21 3.00 3.00
sqrt_a      :  21 3.00 3.00      sqrt_b      :  21 4.00 3.00
sqrt_restore:  21 3.00 3.00
mod_a       :  21 1.00 3.00      mod_b       :  21 2.00 3.00
mod_restore :  21 1.00 3.00
```
Every case also printed `*NАМЕ ОURМRК`, `*ТRАNS:ОURМRК*,,412350` and ended
`КОНЕЦ ЗАДАЧИ +000000000000⏨+00 0000206320000000`.

The one-word changes (all in zone `N+3`, i.e. OUR contour):
- ABS: RAM `0o30160` negative float `-3.0` -> `-5.0` (f32_neg literals).
- SQRT: RAM `0o30160` argument `9.0` -> `16.0`.
- MOD: RAM `0o30161` divisor `4.0` -> `7.0`.
No host-computed digit is stored anywhere; only the printed digit changes.

## 3. Image SHAs (SHA-256, re-hashed after the runs)

```
a98e81090d4b254554a0cd3ff8611438615de84fc012e8e2b70fbabc2ebdc796  2048_base (repo tool, unchanged)
323c3c58222001dc6682c135d3636ca6a0d9c9d66019765840dcbccef1ec947a  2048_abs_a       (A)
257b001c73a93a7617e786dee96f407b1b9c9ba424a5cbecbcba160c2525bbe5  2048_abs_b       (B)
323c3c58222001dc6682c135d3636ca6a0d9c9d66019765840dcbccef1ec947a  2048_abs_restore (restore)
e05036166748a0d549833478aa5f83aad0e97413008b64f5c08501f88de8ff9d  2048_sqrt_a      (A)
8f404ea476712d943d2945a6e280e8bedd17219322667924fc11490e105ab12b  2048_sqrt_b      (B)
e05036166748a0d549833478aa5f83aad0e97413008b64f5c08501f88de8ff9d  2048_sqrt_restore(restore)
3cbbdba11ee38c8bfe9c37ae4ed391e45b8c7f76d24860bd40bbd88614c16cd8  2048_mod_a       (A)
19d51cd053b0af37d7107029915ad3dc344d919340a9e58234f6f2f9e7b09bfb  2048_mod_b       (B)
3cbbdba11ee38c8bfe9c37ae4ed391e45b8c7f76d24860bd40bbd88614c16cd8  2048_mod_restore (restore)
1d93c468c1acf7b6c9d7ac5f002336ce4580d6d716fbc1694aabd605c9bbeae2  deck_trans.b6
```
Baseline SHA reproduces `docs/89` exactly. Restore SHAs are byte-identical
to A in all three cases. The case images were removed after the runs to free
tmpfs; `scripts/build.py` regenerates each from the SHA-identical base.

## 4. Raw SIMH MTR excerpt (MOD baseline, `set cpu debug`)

Observed in the SIMH debug trace before the routine returned (captured, then
the multi-GB trace file removed to free tmpfs):

```
01770 L: 00 30 30114 пб 30114
30114 L: 00 010 2004 сч 2004
      Memory Read [02004] = 0000 2006 0000 2006
30114 R: 00 22 30000 мода 30000
      M20 = 30000
30115 L: 00 010 0160 сч 160
      Memory Read [30160] = 4211 0000 0000 0000    ; X = 9.0
30116 L: 00 016 0161 дел 161
      Memory Read [30161] = 4150 0000 0000 0000    ; Y = 4.0
      ACC = 4111 0000 0000 0000                    ; 9.0/4.0 = 2.25 (on-machine)
      Memory Write [30162] = 4111 0000 0000 0000   ; Q
30120..30122: xta 0175 / asx 0162 / aex 0175
      Memory Read [30175] = 0017 7777 7777 7777    ; MASK40
      Memory Read [30162] = 4111 0000 0000 0000
      ACC = 0003 7777 7777 7777                    ; MASK40 >> (e_q-64)
      ACC = 0014 0000 0000 0000                    ; mantissa mask bits n..39
30123 L: aox 0201
      Memory Read [30201] = 7760 0000 0000 0000    ; all exponent bits + sign
      ACC = 7774 0000 0000 0000                    ; full AINT mask
30126 L: aax 0163
      ACC = 4110 0000 0000 0000                    ; AINT(Q) = 2.0 float
30131 L: a*x 0164
      ACC = 4210 0000 0000 0000                    ; 4.0*2.0 = 8.0
30136 L: a-x 0165
      ACC = 4110 0000 0000 0000                    ; 9.0 - 8.0 = 1.0
... converter (aex/e+x/aax/asx/asx/arx/*64) deposits digit 1 -> `21 1.00 3.00`
```
This closes the docs/78 blocker for the printed value: the float result is
computed by BESM-6 instructions in OUR contour and converted on-machine.

## 5. Setup literals (disclosed, NOT counted as success)

- ABS inputs: `-3.0` / `-5.0`, constructed by SIMH's two's-complement negate
  routine (`besm6_arith.c:negate`) so they are valid negative BESM-6 floats.
- SQRT argument `9.0` / `16.0`; MOD `X=9.0`, `Y=4.0` / `7.0`; constant `0.5`.
- Mechanism constants (not result digits): `EXP_MASK=0o177<<41`,
  `CONST105=0o151<<41`, `EXP1`, `MASK40=0xFFFFFFFFFF`,
  `EXP_ALL=0o177<<41|1<<40`, `CW_L16=0o60<<41`, `SIGNBIT=1<<40`,
  sign-clear mask (unused after the ABS fix).
- Line prefix `21` (GOST byte 0 of word A) and Y field `3.00` (GOST word B)
  are fixed literals in the contour text. Only the X integer digit is computed.

**Deviation from literal task wording:** ABS uses `avx` (hardware sign change)
rather than `aax` sign-bit clear. BESM-6 negative floats store a TWO'S-COMPLEMENT
mantissa (verified against `besm6_arith.c:negate` and SIMH MTR), so clearing
bit 40 alone yields a different, incorrect value; `avx` is the correct
on-machine absolute-value operation. This was discovered by A/B and fixed;
the final A/B/A is with the corrected `avx` version.

## 6. DSQRT: concrete blocker (FAIL)

- BESM-6 SIMH implements ONE 48-bit float format only: every FPU opcode
  (`a+x`, `a-x`, `a*x`, `a/x`) calls `toalu()` with a single 7-bit exponent and
  40-bit mantissa (`besm6_arith.c:36-43,177-425`). There is no double-precision
  FPU opcode, no 64-bit mantissa and no extended-exponent hardware.
- F77 `DOUBLE PRECISION` in this project is a software construct: `DSQRT` is
  compiled as `X**0.5D0` and routed through the FOREX runtime
  (`docs/81-413-intrinsics.md:92,112-113`; `docs/plan-f77-full/16-k-closure.md`).
  A genuine machine-code DSQRT would need software double add / multiply /
  divide (hi+lo pairs), i.e. well over 100 machine instructions, which cannot
  fit in the 58-word clean zone `N+3` (the largest routine here, SQRT, already
  uses 35 of the 36 words available before the constant area).
- Attempted case: the builder's `dsqrt` kind installs the same single-precision
  Newton path as SQRT on the high word of the argument. Its image for 16.0 is
  byte-identical to `2048_sqrt_b` (SHA `8f404ea4...`), so it can only reproduce
  the single-precision digit 4, never a double-precision result. Two of the
  three reduction runs were also lost to concurrent-SIMH port conflicts
  (`attach tty21 Line=21,4220` from another agent) and stale ACPU copies, so
  they are not evidence. No double-precision DSQRT value was produced.

## 7. FACT vs INFERENCE

**FACT (observed):** A/B/A with one-word changes in OUR contour machine code
changes the printed X digit and restores byte-identically for ABS, SQRT and
MOD. SIMH MTR shows `a/x`, bitwise mask and FPU subtract executing at our
machine addresses with ACC changing to the on-machine result. `arx` is integer
add (SIMH `besm6_cpu.c:1204`), while `0o004`/`0o005` are the float add/subtract
(`besm6_add`). The early bug (using `arx` for float add) produced
`ПЕРЕПОЛНЕНИЕ АУ` and no print; fixing to `0o004` produced the PASS results.

**INFERENCE / not proven:** arbitrary float ranges, negative SQRT/MOD inputs,
multi-digit integer results, and true double precision. Only single-digit
non-negative results with exponent in the converter's working window were
exercised. The A/B changes are setup constants (arguments), not precomputed
result digits.

## 8. Evidence index

- `scripts/build.py` - reproducible builder (same-length substitutions in
  body zone `0o2351`, routine/constants in zone `0o2353`, correct
  RAM-index mapping `zidx(addr)=addr-0o114`).
- `scripts/{setup_workspace,drive_case,trace_case,early_trace,bounded_trace}.py`
  - isolated SIMH drivers (private `-n prn` output, copies only).
- `scripts/{verify_image,dump_code,sim_abs}.py` - code read-back and FPU simulator.
- `logs/build_final2.log` - case SHAs; `logs/drive_*.log` - raw driver logs.
- `runs/acpu_<case>.txt`, `runs/console_<case>.txt` - raw ACPU/console copies.
- `decks/deck_trans.b6` - contour-only deck (SHA in §3).

DONE
