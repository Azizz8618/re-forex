# ABS from real Fortran source under SIMH: root cause found and fixed

> РЕЗУЛЬТАТ: **PASS**. Причина `КОНТРОЛЬ КОМАНДЫ` в ABS — allocator N+2
> перепрыгивал с слота 499 (RAM `0o22622`) на слот 901 (`0o27721`), а PC БЭСМ‑6
> идёт по непрерывному адресу: третий halfword `uj PE_NAME_LOCK` оказался
> за запретной дырой, CPU провалился в нулевое слово и ушёл на PC 0.
> Исправление: двухсловная подстановка ветки + sign‑aware ABS с `avx` и
> структурная guard. SIMH: `ABS(-16)→16.00`, `ABS(-9)→9.00`, patch→`17.00`,
> restore→`16.00`, SQRT `4.00/3.00` без регрессии. 55/58 N+3, 499/649 N+2,
> 526..900 = 0 записей, keeper сохранён.

**VERDICT: PASS.** `Y=ABS(-16.0)` prints ` 21 -0016.00  3000.00`, `Y=ABS(-9.0)` prints
` 21 -0009.00  3000.00` on a byte-identical image; a single halfword patch of OUR
ABS routine changes `16.00 -> 17.00`; byte-identical restore returns `16.00`;
SQRT is unchanged (`4.00 / 3.00`). All six full-SIMH runs reached `КОНЕЦ ЗАДАЧИ`.

Discipline: workspace `/tmp/.private/azizz/opencode/b6b-abs-fix/` only; copies of
every image, deck and script. No repository edit, no live disk, no tmux session 0,
no C `dispak` patch, no change to the `b6b-intr` workspace. C `dispak` was oracle
only (MTR/CORE); the authoritative verdicts are full-SIMH printer captures.

SIMH binary verified on every run:
`d058305796bcd0aaf108056f595ee2a222762abe31cf3bb59f1697c9473ca675  /home/azizz/Yandex.Disk/simh/BESM6/BIN/besm6`

---

## 1. Root cause of `КОНТРОЛЬ КОМАНДЫ` (exact PC)

The C oracle reproduces the failure on the *original* image `2048_B6B_A` with
`Y=ABS(16.00)` and with `Y=ABS(-16.0)`. Raw MTR (`evidence/abs_wide_mtr.txt`):

```
MTR 22564R uza    22620(0) AU=0012304010007      ; SQRT name: no match
MTR 22566L uza    22622(0) AU=0000000000000      ; ABS name: MATCH -> 0o22622
MTR 22622L xta    1650(14) AU=0000000000000      ; ACC = 1 (L_ONE)
MTR 22622R atx    2643(14) AU=0000000000001      ; C_INTR = 1
MTR 22623L atx    0(0) AU=0000000000001          ; <-- fall-through into ZERO WORD
MTR 22623R atx    2002(0) AU=0000000000001
...
MTR 22640R vlm    77777(17) AU=0000000000001
MTR 77777L atx    0(0) AU=0000000000001
MTR 00020L *74    0(0) AU=0000000000001
 КОНТРОЛЬ КОМАНДЫ
 00000  00 000 0000  atx
```

**Cause.** The B6b LEX uses a virtual slot list `CODE_REGIONS = [(300,499),(901,1023)]`.
Slot 499 is RAM `0o22622` and slot 901 is RAM `0o27721`: the allocator skips the
forbidden band 526..900, but the BESM-6 PC advances by *contiguous RAM address*.
`PE_GOT_SQRT` (slot 497/498) ends with its `uj PE_NAME_LOCK` **before** the hole, so
SQRT worked. `PE_GOT_ABS` (slot 499) executes `xta L_ONE` at `0o22622L` and
`atx C_INTR` at `0o22622R`; its third halfword (the `uj PE_NAME_LOCK`) was placed at
slot 901 / RAM `0o27721`, which the CPU never reaches. It fell through into
`0o22623` = N+2 offset 500 (`C_PAY`), zero at that time, and ran away to PC 0.
The ABS machine routine was never entered; the OS control check was unrelated to
`avx` and to the name compare.

### Minimal machine-word demonstration of the root cause (2 words)

With the original builder, replacing exactly two halfwords in the generated LEX
(`build/b6b_absfix_build.py`, copied to image `2048_ABS_FIX`, SHA
`5165521d…`):

1. slot 499 R (`0o22622R`): `atx C_INTR` -> `uj PE_NAME_LOCK` (branch out of the hole);
2. `PE_NAME_LOCK` L: `xta L_ONE` -> `atx C_INTR` (store ACC, already 1/2/3, into `C_INTR`).

C oracle: `Y=ABS(16.00)` -> ` 21 -0016.00  3000.00` + `КОНЕЦ ЗАДАЧИ`;
`Y=SQRT(16.0)` -> `4.00`, `Y=SQRT(09.0)` -> `3.00` (no SQRT regression).
This isolates the control-check root cause to the two machine words above.

---

## 2. Why more was needed for the *specified* decks

The defect report's decks use `Y=ABS(-16.0)` / `Y=ABS(-9.0)` (one fractional digit
and a unary minus), while the contour's number scanner accepted only two
fractional digits and ignored `-`. With only the 2-word fix those decks printed
`21 -00  .00` (garbage). The final build (`build/b6b_absfix_full.py`, diff against
the original in `evidence/b6b_build_fix.diff`) therefore adds, all in OUR contour:

* `C_FRAC`/`L_ASCII0` cells + a padding loop: a packed literal is extended with
  ASCII `0` until it has exactly four digits (`16.0` -> `1600`), so one-digit
  fractions parse to `10 x` in the literal pool.
* unary minus: `-` in number mode sets `C_NEG`; after `emit_numfinish` the positive
  float is negated with `avx SIGN` (two's-complement mantissa, docs/95 §1), so the
  pool word holds a genuine negative BESM-6 float.
* correct ABS: the routine tests the sign bit (`asx` by 40 + `aax 1` + `uza`) and
  applies `avx SIGN` only when negative. MTR below shows `-160.0 -> +160.0`.
  Positive input is still `16.00`, not a faked result.
* structural gap guard: an explicit `uj GAP_CROSS` before the 499/901 hole plus
  padding to hw 400, so *no* basic block can ever fall through the forbidden band
  again (the 2-word fix above is also retained, harmlessly, as a belt-and-braces
  measure).
* layout: LEX now ends at N+2 offset 986; ITAB moved to 987..989 and the three
  intrinsic routines to 990..1023 (no overlap; forbidden band 526..900 untouched).
  SQRT iterations reduced 7 -> 4 (docs/95: 4 iterations suffice; verified below).

No IR card, no fixture, no host-computed digit. Every printed digit comes from the
BESM-6 FPU / bitwise ops and the verbatim B3 dispatcher + docs/105 converter.

---

## 3. Decisive gates

### 3.1 C `dispak` oracle (advisory)

| gate | image | deck | printer line | completion |
|:--|:--|:--|:--|:--|
| A | `2048_ABS_FINAL` | `Y=ABS(-16.0)` | ` 21 -0016.00  3000.00` | `КОНЕЦ ЗАДАЧИ` |
| B | `2048_ABS_FINAL` (byte-identical) | `Y=ABS(-09.0)` | ` 21 -0009.00  3000.00` | `КОНЕЦ ЗАДАЧИ` |
| POS | same | `Y=ABS(16.00)` | ` 21 -0016.00  3000.00` | `КОНЕЦ ЗАДАЧИ` |
| SQRT A | same | `Y=SQRT(16.0)` | ` 21 -0004.00  3000.00` | `КОНЕЦ ЗАДАЧИ` |
| SQRT B | same | `Y=SQRT(09.0)` | ` 21 -0003.00  3000.00` | `КОНЕЦ ЗАДАЧИ` |
| PATCH | `2048_ABS_PATCH3` | `Y=ABS(-16.0)` | ` 21 -0017.00  3000.00` | `КОНЕЦ ЗАДАЧИ` |
| RESTORE | `2048_ABS_FINAL` (= A) | `Y=ABS(-16.0)` | ` 21 -0016.00  3000.00` | `КОНЕЦ ЗАДАЧИ` |

### 3.2 Full SIMH (authoritative, b-harness, run sequentially)

| gate | image | deck | prn0 `21` line | plumbing | product |
|:--|:--|:--|:--|:--|:--|
| A | `2048_ABS_FINAL` | `Y=ABS(-16.0)` | ` 21 -0016.00  3000.00` | PASS | **PASS** |
| B | `2048_ABS_FINAL` (same SHA) | `Y=ABS(-09.0)` | ` 21 -0009.00  3000.00` | PASS | **PASS** |
| PATCH | `2048_ABS_PATCH3` | `Y=ABS(-16.0)` | ` 21 -0017.00  3000.00` | PASS | **PASS** |
| RESTORE | `2048_ABS_FINAL` (same SHA as A) | `Y=ABS(-16.0)` | ` 21 -0016.00  3000.00` | PASS | **PASS** |
| SQRT A | `2048_ABS_FINAL` | `Y=SQRT(16.0)` | ` 21 -0004.00  3000.00` | PASS | **PASS** |
| SQRT B | `2048_ABS_FINAL` | `Y=SQRT(09.0)` | ` 21 -0003.00  3000.00` | PASS | **PASS** |

All six prn0 captures also contain
`КОНЕЦ ЗАДАЧИ        +000000000000⏨+00    0000206320000000`.
Raw captures: `build/runs/{console,localprn,acpu,verdict}_ABS_FINAL_{A,B,PATCH,RESTORE,SQRTA,SQRTB}.*`.
The shared `SIMH/ACPU/output.txt` is written by other agents too, so the harness's
per-run ACPU copies are not a reliable product observable; the private printer
capture (`-n prn0`) is authoritative, as in docs/127.

**Causality.** A/B: image SHA identical, only two digit bytes of the Fortran card
differ (1-based offsets 139/140: `1->0`, `6->9`), value `16.00 -> 9.00`.
PATCH: deck frozen, **one halfword** in OUR ABS routine
(RAM `0o30056L`: `xta C_MODA` -> `a+x L_TENF`) changes `16.00 -> 17.00`.
RESTORE: image byte-identical to A, value returns to `16.00`.

---

## 4. Raw MTR (C oracle, final image, `Y=ABS(-16.0)`)

Source-side sign and dispatch (`evidence/mtr_dispatch.txt`):

```
MTR 27770L atx    2637(14) AU=4412000000000000  ; positive float 10*16.0
MTR 27771L uza    27773(0) AU=0000000000001      ; C_NEG = 1 -> negate
MTR 27772L avx    2652(14) AU=4412000000000000  ; avx SIGN (two's complement)
MTR 27772R atx    2637(14) AU=4426000000000000  ; = -160.0
MTR 27773R atx    2003(14) AU=4426000000000000  ; literal pool word 0
MTR 27774L xta    2643(14) AU=4426000000000000  ; C_INTR = 1
MTR 27774R uza    30000(0) AU=0000000000001
MTR 27775L ati    6(0) AU=0000000000001          ; M[6] = SUB = 1
MTR 27776L uj     30046(6) AU=4426000000000000  ; ITAB0 -> ABS trampoline
```

ABS routine (`evidence/mtr_abs.txt`):

```
MTR 30052L atx    2056(14) AU=4426000000000000  ; X = -160.0
MTR 30053L asx    2011(14) AU=4426000000000000  ; shift sign bit into bit 0
MTR 30053R aax    1650(14) AU=0000000000221
MTR 30054L uza    30056(0) AU=0000000000001      ; negative -> negate
MTR 30055L avx    2652(14) AU=4426000000000000
MTR 30055R atx    2056(14) AU=4412000000000000  ; +160.0
MTR 30056R uj     27777(0) AU=4412000000000000  ; back to token path
MTR 27777L atx    2003(14) AU=4412000000000000  ; result written to pool word 0
```

(All `AU` values are octal, as printed by the C oracle.)

---

## 5. SHAs (SHA-256)

```
e10d9477c149e85e9959a0cb6806af599f1f510c5bd8503ee1fdaadd3bd00ab2  2048_ABS_FINAL (A = B = RESTORE = SQRT A/B)
667c602ef4390d911fc7ed4db263dfbd6c2cd8530fe5e869edb24e604d76469b  2048_ABS_PATCH3 (one-halfword patch)
5165521db14f1b5b0c31c77bc2f88e70a074b0cbe867732b857648f4b55e4596  2048_ABS_FIX (minimal 2-word root-cause fix)
b9f26d2c3fa45e25d992522c133ca21474ea37f2296615d1e459f188f24b1a6e  2048_ABS_FULL4 (intermediate, ITAB overlap; superseded)
1c1a29bd3135d6e0e919504c754ca7a65a3d23eec318e0042ca85c4ec8537fe5  2048_B6B_A (original failing image)
fe0e154f806a251f8f5bc9a002247c8c56a7c3db87b8953657115570a0fe252a  deck_ABS_NEG16.b6
15e427637ee19be2651808f09e020e275591c06f8adfb6f83d82afed0fb55763  deck_ABS_NEG09.b6
18110274b2230c0bd563b29bbbb6bb10f8e07b59935936623ac6275a78034e76  deck_SQRT.b6
0a50b2a5749059f8e93086cdc4e86311faf633f04adab10eb5ba8c255989b56d  deck_SQRT_B.b6
d058305796bcd0aaf108056f595ee2a222762abe31cf3bb59f1697c9473ca675  SIMH besm6 (verified)
```

Byte diff `2048_ABS_FINAL` vs `2048_ABS_PATCH3` (`cmp -l`, 6 bytes = one halfword
plus two zone checksum words):
```
10419100 314 122
10419101 133  33
10419132 314 122
10419133 133  33
10427092  56 264
10427093 204 103
```
`cmp` FINAL vs RESTORE: 0 differences (the restore runs reuse the identical file).

---

## 6. Word budget (measured against `2048_base`)

| resource | used | limit | verdict |
|:--|--:|--:|:--|
| N+3 converter + cells (build reports converter 40/58) | 55 changed words | 58 | PASS |
| N+2 changed words (low 382 + high 117) | 499 | 649 | PASS |
| N+2 forbidden band 526..900 | 0 writes | 0 | PASS |
| N+1 body changed words | 6 | 998 | PASS |
| keeper `body[0o26]` | unchanged (`0o1000040000000`) | preserved | PASS |

Build line: `N3=40/58w LEX=572hw (286w) B3disp=105w N2used=987/649`.
ITAB 987..989, intrinsics 990..1017, LEX tail ends 986: no overlap.

---

## 7. PASS / FAIL summary

| # | criterion | verdict |
|:--|:--|:--|
| 1 | Root cause isolated to an exact PC/instruction (fall-through into the 526..900 hole) | PASS |
| 2 | Minimal 2-word machine fix removes `КОНТРОЛЬ КОМАНДЫ` for ABS | PASS |
| 3 | `Y=ABS(-16.0)` -> `16.00` on full SIMH | PASS |
| 4 | `Y=ABS(-9.0)` -> `9.00` on byte-identical image | PASS |
| 5 | One-halfword patch changes value (`16.00 -> 17.00`) on full SIMH | PASS |
| 6 | Byte-identical restore returns `16.00` on full SIMH | PASS |
| 7 | SQRT no regression (`4.00 / 3.00`) on full SIMH | PASS |
| 8 | All six runs reach `КОНЕЦ ЗАДАЧИ`; plumbing PASS | PASS |
| 9 | Genuine negative float (two's complement) constructed by on-machine `avx` | PASS (MTR) |
| 10 | Word budgets and forbidden band / keeper preserved | PASS |
| 11 | MOD two-argument from source | not attempted (out of scope) |
| 12 | DSQRT | infeasible (single 48-bit FPU, docs/95 §6) |

DONE
