# C4 — INTRINSIC DISPATCH (ABS / SQRT / MOD) from the IR opcode

> РЕЗУЛЬТАТ C4: **PASS** — dispatch intrinsic по коду IR. FRONT НЕ имеет
> эмиттера intrinsic (только LIT=1, VARIABLE=2, binop=3, unary=4), поэтому
> `TO=5/6/7` для ABS/SQRT/MOD — явно помеченный build‑фикстурный код, не
> нативная запись FRONT. SIMH на байтово том же образе: `5→21 3.000.00`,
> `6→21 4.000.00`, `7→21 1.000.00`; правка слова dispatch‑таблицы меняет
> 4 на 3, restore возвращает. Бюджет 34/58 слов, 3 слова таблицы в N+2.
> Нет: нативного эмиттера FRONT, DSQRT, multi‑argument, полного 4‑цифрового
> конвертера (40 слов отдельно).

> **RESULT: PASS.** The contour decodes the opcode of a `777005` IR record, indexes a
> 3-word jump table in zone **N+2**, executes one of three machine routines in zone
> **N+3**, and feeds the on-machine float result into the verbatim docs/105
> float-to-GOST digit path. Full SIMH decisive A/B/A/C: byte-identical image,
> deck opcode `5`->`6`->`7` prints **3 / 4 / 1**; one machine word of OUR dispatch
> patched prints **3** instead of 4; byte-identical restore prints **3** again.
> All five runs reached `КОНЕЦ ЗАДАЧИ`. Budget **34/58 words** in N+3 (24 spare),
> 3 table words in N+2 (offsets 20..22), offsets 526..900 untouched.

Date 23.11.2026. Workspace `/tmp/.private/azizz/opencode/c4-intrdispatch/`
(symlink to `/dev/shm/c4-intrdispatch` because /tmp tmpfs is 100% full). Copies only:
no repo, live disk, tmux session 0 or C `dispak` source edits. Deck contains only
`ДИС 41(2048)^`, `*NAME FRX5XX`, `*TRANS:FRX5*,,412350` plus the `777005` IR card
and standard framing (no `*FOREX`/`*FTN`/`*perso`). Full SIMH ACPU/printer with a
workspace-local `-n prn0/prn1` is authoritative; C `dispak` was **oracle only**
(MTR traces and quick printer previews). No host-computed result digit is stored.

---

## 1. How FRONT encodes intrinsic calls — FACT with file:line citations

### 1.1 The real 777005 contract (FRONT.FTN, read directly)

* `src/newcomp/FRONT.FTN:54` `DATA MR5 /777005/`;
  `:346-350` comment `emit 777005 <seq> <kind> <op> <arg1> <arg2>` and
  `PRINT 9005, MR5, SEQ(I), TK(K), TO(K), TA(K), TB(K)`;
  `:376` `9005 FORMAT(1X,6I8)`.
  => record layout `777005 <seq> <TK> <TO> <TA> <TB>` (6 I8 fields).
* `:208` comment `N1.7: structured RHS IR 777005 for rule 31 (postfix/eval order)`.
* Token kinds emitted by the rule-31 scanner:
  | token | TK | TO | TA | citation |
  |:--|:--:|:--:|:--|:--|
  | LIT (scaled real*100) | 1 | 0 | `SC=VAL*100/FRAC` | `:234-261` |
  | VARIABLE | 2 | 0 | `VIDX` | `:262-276` |
  | binary op `+ - * /` | **3** | **1/2/3/4** | 0 | `:299-305`, `:314-327`, `:335-345` |
  | unary op | 4 | 6 (unary minus), 7 reserved | 0 | `:310-311`, `:322-324`, `:339-341` |

### 1.2 FACT: FRONT has NO intrinsic emitter

I searched the entire `src/newcomp/FRONT.FTN` for `SQRT|ABS|MOD|intrinsic|INTRINSIC`.
The only hits are `:54 DATA MR5 /777005/` and the structural comments at `:208,:346`.
There is **no token path** that emits a function-style intrinsic, no recognition of
the character sequences `SQRT`, `ABS` or `MOD`, and no `TO` code outside 1..7.
FRONT's four token kinds are exactly LIT / VARIABLE / binary-op / unary-op.
This is consistent with `docs/plan-f77/02-extension-points.md:199-205`: ordinary
function-style intrinsics (`SQRT(4.0)`, `ABS(-2.0)`, `MOD(7.0,3.0)`, ...) are
compiled as **external Fortran procedures**, not as new IR opcodes; the verdict
at `:326` is "Fortran procedure suffices; the operator table need not change".

**FACT:** to drive an intrinsic from OUR contour we must supply the IR record from
outside FRONT. It cannot be obtained from the current FRONT emitter.

### 1.3 Documented build-time fixture encoding (TEST FIXTURE, not a native FRONT record)

We keep the exact 6-field `777005` layout and reuse the `TO` field as the intrinsic
opcode, with values FRONT never produces:

```
777005  <seq=6>  <TK=3>  <TO>  <TA=0>  <TB=0>
                         5 = ABS    (fixture-only; FRONT emits 1..4 here)
                         6 = SQRT
                         7 = MOD
```

* `TK=3` is retained as the native "operator" kind so the record stays parseable
  by the existing C3 decode chain (`asx SR40` / `aax M8` / `arx NEG31`, C3 report
  §1 and `build/c4_build.py:C4Stream.decode`).
* `TO=5/6/7` are **outside FRONT's native 1..4 binary-op set**; they are a
  documented test fixture, not a claim that FRONT emits them.
* `TA=TB=0`. The deck card is `  777005       6       3       5|6|7       0       0`
  (one byte differs between the three decks: `make_decks.py`).
* `seq=6` is inherited from the proven C3 deck (`decks/deck_op3.b6`).

---

## 2. Machine implementation (reuse first)

### 2.1 Verbatim reuse

| reused item | source | role |
|:--|:--|:--|
| ABS `avx` (hardware sign change) | docs/95, `/home/azizz/machine-intr-report.md` §1 | `\|X\|` |
| SQRT Newton FPU, 4 iterations | same, `ops_sqrt` | `x=(x+S/x)/2` |
| MOD bitwise-mantissa-mask AINT | same, `ops_mod` | `X-Y*INT(X/Y)` |
| docs/105 float->GOST chain `aex/e+x/aax/asx/asx/arx/*64` | docs/105, machine-intr `converter()` | one integer digit into GOST word A |
| `ARX NEG31` ASCII->digit | docs/98, `final_build.py:51-53` | opcode decode |
| `asx SR40` / `aax M8` opcode decode | docs/111, C3 `evaluator()` | card byte 0 -> digit |
| N+2 base `0o21637`, `UTC 20000`+short ADR, M[7]=0o20000 | docs/109/110, C3 | clean table/operand access |
| FRX5 catalog base image `2f5fcf87...` | docs/108, C3 | `*TRANS:FRX5*,,412350` |
| SIMH driver + ini | C3 workspace (`drive_c4.py`, `gen_ini.py`) | authoritative runs |

### 2.2 New code only (C4-specific)

Build file `build/c4_build.py` (SHA `58cc6c85...`). Machine layout:

```
zone N+3  (RAM 0o30114..):  34 words used, 24 spare (limit 58)
  0o30114..0o30117  DECODE   utc 60000 / xta 64014 / asx SR40 / aax M8
                              / arx NEG31 / ati 6 / vtm 20000(7)
                              / uj (table_base-5)(6)      [4 words]
  0o30120           ABS      xta Xabs(7) / avx SIGN(7) / atx RES(7) / uj COMMON
  0o30122           SQRT     Newton x4, result -> RES, uj COMMON      [13 words]
  0o30137           MOD      bitwise AINT, result -> RES, uj COMMON  [9 words]
  0o30150           COMMON   docs/105 float->GOST digit + *64 2004 + uj 0(15)
                                                                      [6 words]

zone N+2  (RAM 0o21637..):  3 table words + operand/scratch/constants
  offsets 1..18  XABS,XSQRT,XMOD,YMOD,HALF,RES,Q,MASKC,AIQ,PROD,T,
                 SIGN,EMASK,C105,M40,CWL16,EXALLC,CW
  offsets 20..22 TABLE[0..2] = LONG uj <ABS|SQRT|MOD entry>  (RAM 0o21663..65)
  offsets 526..900: NEVER TOUCHED (load-bearing overlay table intact)
```

**Dispatch (FACT, C-oracle MTR below).** The decoder leaves the ASCII digit `d`
in M[6] (`5`,`6`,`7`). `uj (0o21663-5)(6)` = `uj 0o21656(6)` therefore sets
`PC = 0o21656 + d = 0o21663/4/5`, i.e. the three N+2 table words. Each table word
is a one-word trampoline `LONG uj <N+3 routine entry>`; the bodies stay in N+3.

**Word budget:** decode 4 + ABS 2 + SQRT 13 + MOD 9 + COMMON 6 = **34 / 58** words
(68 halfwords incl. 3 placeholders + 1 alignment pad). Measured by
`python3 c4_build.py --measure`.

### 2.3 Why the 4-digit docs/105 converter was NOT used (FACT, measured)

The full 4-digit converter + sign block + `floor_acc`/`drop_last_ati` reclaims +
`floor_int` subroutine and `*64` costs **40 words** (measured with `final_sign.S`).
With decode (4) + ABS (2) + SQRT (13) + MOD (9) this is 68 words > 58. The
58-word hard limit therefore forces the single-digit docs/105 float->GOST chain,
which is the same proven converter used by docs/95 / machine-intr. Consequently
the docs/100 `floor_acc` and `drop_last_ati` reclaims are **not applicable by
construction** (there is no `floor_int` VJM and no dead last `ati` in this path);
the docs/98 `ARX NEG31` one-instruction decode IS reused verbatim.

---

## 3. Decisive SIMH A/B/A/C (authoritative)

All runs used the **same contour image** `2048_A` for A/B/C/RESTORE, differing only
in the one opcode byte of the deck; PATCH uses one changed machine word in OUR N+2
dispatch table. Raw printer line 100 and line 114 in each `runs/localprn_*.txt`:

| gate | image SHA (prefix) | deck TO | raw SIMH ACPU line 100 | completion |
|:--|:--|:--:|:--|:--|
| A (ABS) | `fb4a67b8...` | 5 | ` 21 3.000.00  3000.00` | `КОНЕЦ ЗАДАЧИ` |
| B (SQRT) | `fb4a67b8...` (identical) | 6 | ` 21 4.000.00  3000.00` | `КОНЕЦ ЗАДАЧИ` |
| C (MOD) | `fb4a67b8...` (identical) | 7 | ` 21 1.000.00  3000.00` | `КОНЕЦ ЗАДАЧИ` |
| PATCH (deck SQRT) | `3d9a16a3...` | 6 | ` 21 3.000.00  3000.00` | `КОНЕЦ ЗАДАЧИ` |
| RESTORE (deck ABS) | `fb4a67b8...` (= A) | 5 | ` 21 3.000.00  3000.00` | `КОНЕЦ ЗАДАЧИ` |

Exact printed completion line (all five):
`КОНЕЦ ЗАДАЧИ        +000000000000⏨+00    0003155120000000`.

**Causality (FACT):**
* A vs B vs C: only **one deck byte** changes; images are byte-identical (same
  SHA). The opcode alone selects ABS/SQRT/MOD and produces 3 different values.
* PATCH: N+2 offset 21 (RAM `0o21664`) changed from `uj SQRT_entry (0o30122)` to
  `uj ABS_entry (0o30120)`. Under the SQRT deck the printed value changes
  4 -> 3. `cmp -l` shows **3 byte diffs** (1-based 10419100, 10419132, 10419308):
  one real machine word in the dispatch table plus two zone-N+2 checksum copies.
* RESTORE: image byte-identical to A (`cmp` = 0 diffs, same SHA), value returns to 3.
  (The printer *file* SHAs differ between runs only because of the run timestamp;
  the value lines are identical.)

### Raw C-oracle MTR excerpts (oracle only; `oracle/mtr_*/out.txt`)

ABS (`TO=5`):
```
MTR 30115R aax 2110(0) AU=0000000000065      ; ASCII '5'
MTR 30116R ati 6(0)    AU=0000000000005      ; M[6]=5
MTR 30117R uj  21656(6) AU=0000000000005     ; PC = 0o21656+5
MTR 21663L uj  30120(0)                       ; N+2 table[0] -> ABS
MTR 30120R avx 1653(7) AU=4124000000000000   ; |X|, -3.0 -> +3.0
MTR 30121R uj  30150(0)                       ; -> COMMON converter
MTR 30155L *64 2004(0) AU=40041700607000     ; print
```
SQRT (`TO=6`):
```
MTR 30115R aax 2110(0) AU=0000000000066      ; ASCII '6'
MTR 30116R ati 6(0)    AU=0000000000006
MTR 30117R uj  21656(6) AU=0000000000006
MTR 21664L uj  30122(0)                       ; N+2 table[1] -> SQRT
MTR 30122R atx 1652(7) AU=4250000000000000   ; S=16.0 -> t
MTR 30124R a*x 1644(7) AU=4250400000000000   ; Newton (x+S/x)/2 ...
```
MOD (`TO=7`):
```
MTR 30115R aax 2110(0) AU=0000000000067      ; ASCII '7'
MTR 30116R ati 6(0)    AU=0000000000007
MTR 30117R uj  21656(6) AU=0000000000007
MTR 21665L uj  30137(0)                       ; N+2 table[2] -> MOD
MTR 30137R a/x 1643(7) AU=4211000000000000   ; Q = 9.0/4.0 = 2.25
```

---

## 4. SHAs (SHA-256)

```
a98e81090d4b254554a0cd3ff8611438615de84fc012e8e2b70fbabc2ebdc796  2048_base (repo tool, unchanged)
2f5fcf873d43c2846ee1669669e26202f32fa25e6b71e109fd20ef4452142ff5  2048_base_frx5
fb4a67b8d72104b2cb56a83fd198f243249d4b716f03cd62ad1a01d65483d496  2048_A = B = C = RESTORE
3d9a16a3ca6fc3c733711bca6b6a26e09740d7f9ab7a9efed45595a31fe0fa16  2048_PATCH
f104f21b95c7e11ca4d7b0c30d273c6fc18fcd74b8d09048d466d05284dfec38  deck_abs.b6 (TO=5)
d54da9b1ff6475db2bc17b630ba15862f6b3485c79c7566a1b5eceb931a9cb2c  deck_sqrt.b6 (TO=6)
1d6377f06d203db05a82771892bcd041447c7ca72bc2de1848e734411655b090  deck_mod.b6 (TO=7)
60efd848c996a3a196d13d67a66b9bfeabedc69a26f830cd559f322cc930b488  localprn_A.txt
0c82ce636bbc4857ab5503af2ab70451909d44cbd4911e64ec3713009a244c7e  localprn_B.txt
96023ad63bce2a4f3a6f5b764ad2576e7dafe5844eecc3a45888e29d2783fc82  localprn_C.txt
65ba1b8db05b4d91dfc31fc8b61e3d580495ba5ed8e18e9e8b94735e18253277  localprn_PATCH.txt
2b6a097360596a347df509fdd076428325f1347afc8cb02e0382edfe6b2247da  localprn_RESTORE.txt
58cc6c8594e8cccbfdde0c5a124ba665e647d90f3901acd29c46db5171b9a288  build/c4_build.py
14c407a616398d2e76f4f359431baf8098a703749a09ac986e24e7928d3eb0c9  build/make_decks.py
```

---

## 5. Supported subsets / missing pieces

**Works (FACT):**
* ABS, SQRT, MOD dispatched by the decoded `TO=5/6/7` opcode of a single
  `777005` record; all three compute the result with BESM-6 FPU/bitwise ops in
  OUR contour and print a distinct value; 34/58 words; N+2 table 3 words.
* Single-operand intrinsics only (one value per routine, seeded in N+2).

**Missing / impossible (FACT or stated INFERENCE):**
1. **No native FRONT emitter** for intrinsics (§1.2). The deck record is a build-time
   fixture. A native path would require an external Fortran procedure (docs/111
   §2.а) or a new FRONT token kind + generator support (not in scope).
2. **DSQRT remains impossible.** SIMH has one 48-bit float format, no double FPU
   (`/home/azizz/machine-intr-report.md` §6). A software double Newton path is
   >100 instructions and cannot fit in 58 words (our 4-iteration single-precision
   SQRT already uses 13 words of body).
3. **Argument passing beyond one value is absent.** MOD needs two constants
   (`XMOD`,`YMOD`), both pre-seeded in N+2; there is no arg-block reader, no M16
   calling convention (docs/111 §3), no multi-argument stack.
4. **No postfix scanner / multi-record evaluation.** One IR record is decoded per
   run; no expression tree, no `777001..777004`, no variable name resolution.
5. **Single-digit results only.** The docs/105 single-digit converter prints one
   GOST digit; multi-digit values, negative results and arbitrary exponents are
   not handled. Only the enumerated inputs (ABS -3, SQRT 16, MOD 9/4) were run.
6. **The four-digit docs/105 converter with sign cannot fit** (40 words alone).

## 6. FACT vs INFERENCE

**FACT (observed):** FRONT source contains no intrinsic emitter; the 777005 field
layout and token codes above are read directly from file:line. SIMH ACPU printed
3/4/1 for the three opcodes with a byte-identical image; a one-word dispatch-table
patch changed 4->3; restore was byte-identical and printed 3 again; all reached
КОНЕЦ ЗАДАЧИ. C-oracle MTR shows the decoded digit, the N+2 table trampoline, the
FPU ops and the `*64` deposit at our machine addresses. `cmp` proves 3 patch byte
diffs and 0 restore diffs.

**INFERENCE (not proven):** that other operand values in the same single-digit
range would work; that the fixture `TO=5/6/7` would be accepted by any future
native FRONT/generator (it would not, without an emitter); that a longer Newton
iteration count improves SQRT (not measured). No host computed any printed digit.

## 7. PASS / FAIL

| # | criterion | verdict |
|:--|:--|:--|
| 1 | FRONT encoding with file:line citations; no-intrinsic-emitter FACT stated | PASS |
| 2 | Documented 777005-compatible fixture encoding (TO=5/6/7) | PASS |
| 3 | 3-way dispatch: table in N+2, code in N+3 | PASS |
| 4 | ABS/SQRT/MOD machine routines reuse verbatim | PASS |
| 5 | docs/105 float->GOST digit path fed by chosen result | PASS |
| 6 | N+3 budget 34/58; N+2 table 3 words; 526..900 untouched | PASS |
| 7 | SIMH A/B/C: same image, 3 distinct values 3/4/1, КОНЕЦ ЗАДАЧИ | PASS |
| 8 | SIMH PATCH: one machine word of OUR dispatch -> 4 becomes 3 | PASS |
| 9 | SIMH RESTORE: byte-identical image -> value returns to 3 | PASS |
| 10 | C-oracle MTR confirms digit, table and FPU | PASS |
| 11 | Native FRONT intrinsic emitter | FAIL (absent; §1.2) |
| 12 | DSQRT / double precision | FAIL (infeasible; §5.2) |
| 13 | Multi-argument passing, postfix scanner, full 4-digit converter | FAIL (§5) |

DONE
