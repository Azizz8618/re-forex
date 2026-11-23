# gost-sign: SIGN handling in the proven on-machine float -> GOST contour

> ГЛАВНЫЙ РЕЗУЛЬТАТ: **PASS** — знак печатается машинно‑кодом контура.
> `avx SIGNBIT` создаёт отрицательное float на машине, `aax SIGNBIT`
> выделяет бит 40, `asx SHR22` сдвигает его в байт знака, `aex GOST_A`
> XOR’ит `15->11` (`GOST_MINUS`). SIMH A/B/C: `21 -0003.00` -> правка
> одного слова `SIGNBIT` -> `21  0003.00` -> restore -> минус возвращается;
> тот же образ с `X=4.0` даёт `21 -0002.00`. 1 цифра + знак = **39/58** слов;
> 2+2 цифры + знак = **62/58**, честный перерасход 4 слова.

Date: 23.11.2026. Workspace: `/tmp/.private/azizz/opencode/gost-sign/`.
Repo, live disks, tmux session 0 and dispak C sources were **never** edited.
Every attached image was a COPY. SIMH used stock `attach -n prn0/prn1`, the
`ДATA:` boot marker via `capture-pane`, all input via `send-keys`, `ДАЙ A0/A1`
/ `НОМВ` before the deck, post-job-start `НОМВ`, isolated tmux socket. C
`dispak` was used **oracle only** (MTR/CORE); all authoritative A/B/C results
are full SIMH ACPU output. Deck: only `ДИС 41(2048)^` and
`*TRANS:OURMRK*,,412350` (plus the standard `PROGRAM MAIN / X=d.0 / END /
*EXECUTE / *END FILE` framing that supplies the literal); no `*FOREX`,
`*FTN`, `*perso`.

## VERDICT

| gate | contour image (SHA prefix) | deck | one change | SIMH ACPU line (verbatim) |
|:--|:--|:--|:--|:--|
| **A** baseline | `2048_A` `c77a8b31...` | `X=9.0` | none | ` 21 -0003.00  3000.00` |
| **B** sign removed | `2048_B` `30cc9daf...` | `X=9.0` | ONE data word: `SIGNBIT 1<<40 -> 0` at zone N+3 word index 37 (short addr `0o161`, RAM `0o30161`) | ` 21  0003.00  3000.00` |
| **C** restore | `2048_RESTORE` `c77a8b31...` | `X=9.0` | byte-identical to A | ` 21 -0003.00  3000.00` |
| extra gate | `2048_A` **byte-identical** | `X=4.0` | only the deck's ASCII digit (`9`->`4`) | ` 21 -0002.00  3000.00` |

All four reached `КОНЕЦ ЗАДАЧИ`; console showed `2048 - 41`,
`B075-1 410300000000`, `ОЗ(075) 410300000000`.

`cmp -l 2048_A 2048_B` = **3 bytes**: the most-significant byte of the one
SIGNBIT BESM word (`1 -> 0` octal, file offset 10427694) plus the two
recomputed zone-checksum copies. `cmp -l 2048_A 2048_RESTORE` is EMPTY.

---

## 1. Minimum machine-code sign test (FACT from the simulator sources)

Facts read from primary sources, not inferred:

* `simh/BESM6/besm6_defs.h:87-89`: `BIT40 = 1<<39` (top mantissa bit),
  `BIT41 = 1<<40` (**the sign**), `BIT42 = 1<<41` (double sign).
* `besm6_arith.c:34-46`: `toalu()` keeps `val & BITS41` (bits 40..0); when
  `mantissa & BIT41` it also sets `BIT42`. `is_negative()` is exactly
  `(mantissa & BIT41) != 0`, i.e. **bit 40 of the 48-bit word is the sign**.
* `besm6_arith.c:446-455`: `avx` (`besm6_cpu.c:1213`) negates ACC iff the
  *operand's* bit 40 is set; `negate()` (lines 48-58) uses two's-complement
  mantissa, which is why docs/95 had to use `avx` for ABS.
* `besm6_cpu.c:1195` `aax`: `ACC &= operand` (logical AND).
  `besm6_cpu.c:1185` `aex`: `ACC ^= operand` (logical XOR).
  `besm6_cpu.c:1338-1345` `asx`: `n = (operand >> 41) - 64; besm6_shift(n)`
  (positive `n` = right shift, `besm6_shift()` at `besm6_arith.c:525-545`).
* `tests/plan-f77/84-wide-output/codegen_wide.py:49`:
  `GOST_SPACE=15, GOST_DOT=14, GOST_MINUS=11`; line 88 puts X_sign in
  **GOST word A byte 3**, seeded 15. `15 ^ 4 = 11`, so a single XOR of
  `4 << 16` (= `1<<18`) into word A byte 3 toggles space -> GOST minus.

Therefore the minimum test is **4 halfwords**: `avx SIGNBIT` (make a
machine negative from the positive float), `aax SIGNBIT` (isolate the float's
own bit 40), `asx SHR22` (right shift 22: `1<<40 -> 1<<18`), `aex GOST_A`
(XOR into the seeded sign byte), plus one store (`atx GOST_A`). No compare,
no branch, no host digit. `SIGNBIT = 1<<40` and `SHR22 = (64+22)<<41` are two
mechanism constants. This reuses docs/90's `aex/e+x/aax/asx` control-word
derivation for the digit path verbatim; only the sign test is new.

`avx` is used only to *create* the negative and to restore the positive before
the digit converter; the sign bit read by `aax` is the bit of the resulting
machine float itself, so it is a real two's-complement float sign, not a flag.

### Raw C-oracle MTR, A (oracle only, `BESM6_MTR_LO=030114`, `HI=030200`, `N=1200`)

```
MTR 30135L xta    150(7) AU=4114000140000600      ; +sqrt(9) on machine
MTR 30135R avx    161(7) AU=4114000140000600      ; SIGNBIT -> negate ACC
MTR 30136L aax    161(7) AU=4123777637777200      ; ACC now NEGATIVE float (bit40 set)
MTR 30136R asx    162(7) AU=20000000000000        ; bit40 isolated
MTR 30137L aex    2006(0) AU=0000001000000        ; 1<<18 (right shift 22)
MTR 30137R atx    2006(0) AU=40041702600000       ; GOST A bytes [2][1][15][11][0][0]
MTR 30143R asn    40(0)  AU=0000000000003         ; digit 3 (machine-computed)
MTR 30144L arx    2007(0) AU=0140000000000         ; digit << 32
MTR 30144R atx    2007(0) AU=0141600000017         ; GOST B [0][3][14][0][0][15]
MTR 30145L *64    2004(0) AU=0141600000017
 21 -0003.00  3000.00
```

`40041702600000` octal decodes to bytes `[2,1,15,11,0,0]`: byte 3 is
`GOST_MINUS = 11` (FACT, computed from the float's sign bit).

### Raw C-oracle MTR, B (same window, SIGNBIT patched to 0)

```
MTR 30135R avx    161(7) AU=4114000140000600      ; operand bit40 = 0 -> NO negate
MTR 30136L aax    161(7) AU=4114000140000600      ; sign bit = 0
MTR 30136R asx    162(7) AU=0000000000000
MTR 30137L aex    2006(0) AU=0000000000000
MTR 30137R atx    2006(0) AU=40041703600000        ; GOST A bytes [2][1][15][15][0][0]
```

Byte 3 stays `GOST_SPACE = 15`. Full files: `oracle/{A,B}/out.txt`.

## 2. Raw SIMH ACPU evidence (authoritative)

`runs/acpu_{A,B,RESTORE,X4}.txt`, line 100 and the completion line:

```
A       : " 21 -0003.00  3000.00"  ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0007777620000000"
B       : " 21  0003.00  3000.00"  ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0007777620000000"
RESTORE : " 21 -0003.00  3000.00"  ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0007777620000000"
X4      : " 21 -0002.00  3000.00"  ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0003014720000000"
```

Each also printed `*NАМЕ ОURМRК` and
`*ТRАNS:ОURМRК*,,412350`. `acpu1_*` are empty; stock `-n prn` output is in
`output.txt`.

Two runs were discarded, not counted as evidence: the first B attempt lost a
SIMH tty port to a concurrent agent (`attach tty23 Line=23,4222`, bind error
98) and produced an instruction-parity stop; the first X4 attempt omitted
`setup_workspace.py X4`, so the driver had no ini and SIMH booted a default
image (it printed `21 2.00 3.00` without our contour). Both were regenerated
and the final A/B/C/X4 above are the clean runs.

## 3. SHAs (SHA-256, re-hashed after the runs)

```
a98e81090d4b254554a0cd3ff8611438615de84fc012e8e2b70fbabc2ebdc796  2048_base (repo tool, unchanged; reproduces docs/87)
c77a8b319141935d7361b7675f4479569846caadec6dcaae62dfb6750b219674  2048_A       (baseline, negative printed)
30cc9daf23eb6736125b53df04eaa5e0c43beff7351525ef3c4aab308b620c03  2048_B       (SIGNBIT = 0, one word patched)
c77a8b319141935d7361b7675f4479569846caadec6dcaae62dfb6750b219674  2048_RESTORE (byte-identical to A)
03245c809b28f69a6184c58532a1479a5ef15a3798feb702602c48e218fe0948  2048_MS      (2+2+sign word-count measurement only)
43950bb4385cf7eb547daab4f317feaeb4f64facb67a6166430ddcc648af6192  decks/deck_x9.b6
51ac42f3fdd5a71a4bda6bcdfa6fc701b84f012e20a11b3f813091150d87567f  decks/deck_x4.b6
1d93c468c1acf7b6c9d7ac5f002336ce4580d6d716fbc1694aabd605c9bbeae2  decks/deck_trans.b6
992d962bec51fd2c1db2134fae75e2a3cd95021fec3859c1d61cab4ab9a038f4  runs/acpu_A.txt
f838ea8f8aea6f25d62ca472e7db86f6868850394f7822bd610667e1b3a89031  runs/acpu_B.txt
7d1348e71a8d5b435c4e337823104092123dc1c178b20b872fc7b104a5217915  runs/acpu_RESTORE.txt
0c75fc38d9d95a0464ae8312f490d4e4e248279ec482cd11e1bcf9852c82e746  runs/acpu_X4.txt
9e6cc76b758bece41a2dadda6230c383a36897e4c002d2c22fffa1d8cf2ad26c  oracle/A/out.txt (C MTR, oracle only)
030725962b681d53adcacae3822292fb2559f6533f8b1a5a1b8d9d5f1d123edd  oracle/B/out.txt (C MTR, oracle only)
```

## 4. Reuse of proven code (hard rule)

Reused verbatim: the repo base-image tool and zone writer/checksum
(`tools/build_zone2350_contour.py`, base SHA `a98e8109...`); the contour-only
deck and SIMH driver pattern (`capture-pane ДATA:`, `send-keys`, `ДАЙ A0/A1`,
`НОМВ`, stock `-n prn`, copies only, isolated tmux); entry substitution
`uj 30114` at RAM `0o1770`; deck card read `utc 60000` + `xta 4012` and
ASCII-to-float chain from docs/96; Newton SQRT (4 iterations) from docs/95;
`aex/e+x/aax/asx` digit derivation with an on-machine-computed control word,
`asn` immediate deposit and `*64 2004` from docs/89/90/96; M[7]=`0o30000`
base addressing from docs/90.

New lines are only: the five halfwords `avx / aax / asx / aex / atx` that
compute and XOR the sign, the two mechanism cells `SIGNBIT` and `SHR22`, and
moving the digit deposit from word A byte 3 to codegen_wide word B byte 1
(`asn 0o40`) so word A byte 3 is free for the sign. No new emulator mechanism.

## 5. Exact word counts; honest overrun for 2+2 digits + sign

Measured by `scripts/build_sign.py measure` (builder assertions, not estimates):

| variant | code words | data words | total | verdict |
|:--|--:|--:|--:|:--|
| **built and run: deck + SQRT + 1 machine digit + sign** | 26 | 13 | **39 / 58** | PASS, A/B/C proven end-to-end |
| docs/96 baseline: deck + SQRT + 1 digit (no sign) | 23 | 12 | 35 / 58 | prior work |
| **2 integer + 2 fractional digits + sign** (docs/90 four-digit stream + our sign block) | 47 | 15 | **62 / 58** | **OVER by 4 words** |

The four-digit converter alone already consumes all 58 words (docs/90:
45 code + 13 data). Our sign block adds 5 halfwords (~3 code words once
halfword parity is included) and 2 data cells, giving 62/58. Per the task this
is **reported, not faked**: the minimum variant that genuinely fits and was
proven under SIMH is **1 machine-computed digit + sign** (39/58). A `vjm`
refactor of the four repeated floor/deposit blocks might recover enough space
(INFERENCE, not attempted). The largest prior honest width without sign was
2+2 digits (docs/90); adding sign to it does not fit the 58-word zone.

## 6. FACT vs INFERENCE

**FACT (observed in this experiment):**
- The sign byte of GOST word A changes from 15 (space) to 11 (`GOST_MINUS`)
  when, and only when, the on-machine float's bit 40 is set. MTR shows the
  exact ACC values at `avx/aax/asx/aex/atx` for both A and B.
- A one-word change in OUR contour (`SIGNBIT` 1<<40 -> 0) changes the printed
  sign from `-` to space; a byte-identical restore returns `-`. The printed
  digit (3) is unchanged by the sign patch, i.e. the two mechanisms are
  independent and the digit still comes from the machine SQRT/converter.
- With the contour image byte-identical, changing only the deck's ASCII digit
  `9`->`4` changes the printed digit `3`->`2` while the minus persists.
- All four SIMH cases reached `КОНЕЦ ЗАДАЧИ` with stock `-n prn` output.
- Base image SHA reproduces docs/87/89/90/95/96 exactly; deck SHAs match
  docs/96.

**INFERENCE / not proven here:**
- That an actual `X=-9.0` deck literal (a minus byte in the card word) would
  work. We used the explicitly permitted "computed negative": the deck
  literal is positive `X=9.0`/`X=4.0`, and `avx` computes the negative float
  on-machine. Parsing a card-byte minus would need a different digit path
  (the ASCII digit sits at card-word byte 3).
- Arbitrary exponents, sign of multi-digit results, and the `vjm` refactor
  that might fit 2+2+sign in 58 words were not exercised.
- Bit-40 semantics were established by reading the simulator primary sources
  and confirmed by MTR for these two values, not for every float encoding.

## 7. Setup literals disclosed (NOT counted as success)

- Deck literals `X=9.0` / `X=4.0`: arguments read from the card image; the
  negative value is computed on-machine from them by `avx`.
- `HALF = f32(0.5)` (Newton half-step), `SIGNBIT = 1<<40`, `SHR22 =
  (64+22)<<41`, `BASE=0o30000`, `SR16`, `MASK8`, `PD0`, `EMASK`, `C105`,
  `M40`: mechanism constants, never result digits.
- Fixed GOST text: line prefix `21`, seeded sign space (15), point (14), Y
  field `3000.00`, EOF (`0o231`). The only GOST digit written at runtime is
  the X units digit from the machine converter; the sign byte is written at
  runtime by `aex` from the machine float's own sign bit.

## 8. Evidence index

```
scripts/build_sign.py          reproducible builders (sign1 + multi_sign) and word-count measure
scripts/setup_workspace.py     per-case SIMH ini (copies, stock -n prn)
scripts/drive_case.py          isolated SIMH driver (ДATA:/send-keys/ДАЙ/НОМВ)
scripts/c_oracle.py            C-dispak oracle (MTR/CORE), oracle only
decks/deck_{x9,x4,trans}.b6    contour-only / literal decks
images/2048_{base,A,B,RESTORE,MS}
runs/acpu_{A,B,RESTORE,X4}.txt raw SIMH ACPU (the printed line is at line 100)
runs/console_{A,B,RESTORE,X4}.txt, runs/ini_*.ini
oracle/{A,B}/out.txt           raw C MTR traces (authoritative SIMH output is above)
logs/drive_{A,B2,RESTORE,X4b}.log, logs/oracle_B.log
```

DONE
