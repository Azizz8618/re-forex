# C7 — FINAL INTEGRATION: one contour, one deck, all proven IR features

> РЕЗУЛЬТАТ C7: **PASS** — все четыре приоритетных уровня собраны в ОДНОМ
> контуре (40/58 слов N+3, 177/649 N+2, общий сканер/GOST/dispatch, без
> конкатенации вариантов). Из одного дека печатаются шесть значений: LIT
> `-0012.34`, VARIABLE `-0056.78`, `*` `-0003.75`, SQRT `-0000.40`, ширина
> `-0034.50`, DO `-0040.00`. SIMH A/B/PATCH/RESTORE PASS, все `КОНЕЦ ЗАДАЧИ`.
> Образ `b3ede988…`, decks `b6e4488a…`/`eb8c86a2…`. Воспроизведение из
> `tools/forex500-c7/` проверено главным агентом: SHA совпали.
> Рекомендация: **отдельный вариант изделия**, не замена канонического
> `f483f6ca…`/`2f5fcf87…` (другой контракт дека: 6 записей/6 печатей).
> Ограничения: FRONT не эмитит intrinsic/DO/FORMAT (фикстуры), DSQRT,
> `READ(u,fmt)`, приоритет/скобки, SUB magnitude‑only.

> **RESULT: PASS.** One integrated contour image and one six-record deck drive
> **all** proven C1-C6 features through ONE shared marker scanner, ONE TK jump
> table and ONE byte-identical docs/105 GOST+sign converter. Full SIMH A/B/A/C
> gates: the same image with two different decks prints six distinct values;
> one machine-word patch changes only the VARIABLE line; byte-identical restore
> returns it; all four jobs reach `КОНЕЦ ЗАДАЧИ`. Budget **40/58 words in N+3**
> and **177/649 words in N+2**; offsets 526..900 are never touched.

Date: 23.11.2026. Workspace `/tmp/.private/azizz/opencode/c7-integrate/`
(symlink to `/dev/shm/c7-integrate`; `/tmp` tmpfs is 100% full). **Copies only**:
no repository, live-disk, tmux-session-0 or C `dispak` source edits. C `dispak`
was used **as an oracle only** (MTR/CORE, docs/88); all authoritative A/B/A
results are full SIMH ACPU/printer captures with a workspace-local `-n prn0`.

Deck contains only `*TRANS:FRX5*,,412350`, `*NAME FRX5XX`, `ДИС 41(2048)^`
plus standard Fortran framing and the six `777005` IR cards; no `*FOREX`,
`*FTN`, `*perso`.

---

## 1. Feature set: maximum honest subset included

All four priority tiers fit. Nothing from (a)-(d) was dropped.

| tier | feature | status | deck record / token | printed value (deck A) |
|:--|:--|:--|:--|:--|
| (a) | multi-record `777005` scanner | **included, PASS** | 6 records, marker-searched | 6 lines |
| (a) | 4-digit LIT decode (docs/104/105) | **included, PASS** | rec 1 `TK=1, arg1=1234` | `-0012.34` |
| (a) | VARIABLE + two-digit VIDX + on-machine TEXT compare (docs/109/114) | **included, PASS** | rec 2 `TK=2, TA=12` (name H) | `-0056.78` |
| (a) | one binary arithmetic op, 4-way TO dispatch (docs/111) | **included, PASS** | rec 3 `TK=3, TO=3` (`*`) | `-0003.75` |
| (a) | machine GOST print with sign (docs/105) | **included, PASS** | all 6 lines | verbatim converter |
| (b) | intrinsic dispatch ABS/SQRT/MOD (docs/112) | **included, PASS** | rec 4 `TK=3, TO=6` (SQRT) | `-0000.40` |
| (c) | FORMAT-like print width w/d (docs/113) | **included, PASS** | rec 5 `TK=5, TO=4, TA=2` | `-0034.50` |
| (d) | DO countdown fixture (docs/115) | **included, PASS** | rec 6 `TK=6, TA=02, TB=1` | `-0040.00` |

ABS (`TO=5`) and MOD (`TO=7`) are implemented in the same dispatch table but
are **not** in the two deck variants; they were separately validated with the
C oracle on fixture decks (`deck_c7_test_ABS.b6` -> `-0003.00` = |−30|/10,
`deck_c7_test_MOD.b6` -> `-0000.10` = (9 mod 4)/10). All three intrinsic
routines are therefore proven; only SQRT is carried in the main deck.

**Why they all fit:** the apparent 10-word overrun of docs/112 §2.3 assumes
the converter and every front-end share N+3. C7 applies the C2b/C6
displacement principle (docs/114 §4.1, docs/115 §2.3): the converter is the
only hot path in N+3; scanner, dispatch, all readers and all feature handlers
live in the 649 proven-free N+2 words. No front-end competes for the 58-word
N+3 ceiling.

---

## 2. Shared architecture (not concatenated variants)

**Zone N+3 (RAM `0o30114..`) — 40/58 words, byte-for-byte verbatim docs/105:**
ABS+2+2 GOST converter, sign block, `floor_acc` and `drop_last_ati` reclaims,
shared `floor_int` VJM at `0o30161`, resident `*64 2004`. 74 converter
halfwords + pad + 6 `floor_int` halfwords = 80 halfwords = 40 words. The
converter is called as a VJM subroutine once per record (outer link M[9]).

**Zone N+2 (RAM `0o21637..`) — 177/649 words changed:**
* one marker scanner (search `0o823737373030`, never a fixed stride);
* one `LONG UJ` TK jump table at offsets 190..195 (TK=1/2/3/5/6);
* one `LONG UJ` TO jump table at offsets 150..156 (TO=1..7: +,−,×,÷,ABS,SQRT,MOD);
* shared LIT, VARIABLE, arithmetic, intrinsic, width and DO handlers;
* symbol table (name at VIDX, value at `32+VIDX`), constants and width masks;
* code at offsets 200..317 (236 halfwords), reached by the body[0o11]
  substitution `long uj 0o22147`.

The scanner persists the found-marker pointer in N+2 `K_PTR` (offset 121) at
every record, so the converter may clobber base registers between records;
`rearm()` reloads M[12]=0o20000 (N+2 base), M[7]=0o20000 (short-branch base)
and M[10]=card pointer on every iteration. All N+2 access uses the proven
`UTC 20000` + short ADR / M[7] base mechanism of docs/110.

**Word accounting (measured, not estimated):**

| resource | used | limit | verdict |
|:--|--:|--:|:--|
| N+3 code (zone `0o30114..`) | 40 words (80 hw) | 58 | **PASS** (18 spare) |
| N+2 code (offsets 200..317) | 118 words (236 hw) | 649 | **PASS** |
| N+2 symbols/constants/tables | offsets 1..195 | 649 | **PASS** |
| N+2 changed words, total | 177 | 649 | **PASS** |
| N+2 offsets 526..900 (load-bearing overlay) | **0 changed** | must be 0 | **PASS** |
| zone N+4 | not used | unavailable | **PASS** |

---

## 3. Decks

Deck A — six records, single-digit `seq` (a two-digit seq shifts every I8
field by a byte and was rejected by an early CORE dump):

```
*NAME FRX5XX
*TRANS:FRX5*,,412350
      PROGRAM MAIN
  777005       1       1       0    1234       0        LIT
  777005       2       2       0      12       0        VARIABLE (VIDX=12, H)
  777005       3       3       3       0       0        binop TO=3 (*)
  777005       4       3       6       0       0        intrinsic TO=6 (SQRT)
  777005       5       5       4       2       0        width w=4 d=2
  777005       6       6       1      02       1        DO bound=2 step=1
      END / *EXECUTE / *END FILE
```

Deck B differs in **exactly 5 bytes / 2 IR records**: `1234 -> 5678` (LIT
arg1, 1-based offsets 162..165) and binop `TO 3 -> 1` (`*` -> `+`, offset 255).

---

## 4. Decisive SIMH acceptance (authoritative ACPU/printer)

Each gate used the isolated tmux socket, `ДATA:` marker via `capture-pane`,
`ДАЙ А0`/`ДАЙ А1`/`НОМВ` before the deck, `at vu0 <deck>` / `d 6 1` / `d 5 10`
/ `set cpu req` / `go`, post-job-start `НОМВ`, stock `attach -n prn0` with only
the capture path changed.

| gate | image SHA-256 (first 12) | deck | printer lines (six values) | КОНЕЦ ЗАДАЧИ | verdict |
|:--|:--|:--|:--|:--|:--|
| **A** | `b3ede98828cd…` | deck A | -0012.34 / -0056.78 / -0003.75 / -0000.40 / -0034.50 / -0040.00 | yes | **PASS** |
| **B** | `b3ede98828cd…` (identical) | deck B | -0056.78 / -0056.78 / **-0004.00** / -0000.40 / -0034.50 / -0040.00 | yes | **PASS** |
| **PATCH** | `229f6afb0bde…` (one N+2 word) | deck A | -0012.34 / **-0099.99** / -0003.75 / -0000.40 / -0034.50 / -0040.00 | yes | **PASS** |
| **RESTORE** | `b3ede98828cd…` (= A, byte-identical) | deck A | same as A | yes | **PASS** |

**Causality (FACT):** with a byte-identical image, changing two IR fields
changes exactly two printed values (LIT 12.34 -> 56.78, MUL 3.75 -> ADD 4.00),
so the values come from the deck IR, not from host-computed digits. Patching
one machine word in N+2 (VIDX-12 symbol value 5678.0 -> 9999.0) changes only
line 2 (56.78 -> 99.99). Byte-identical restore returns line 2 to 56.78. All
four printers end with `КОНЕЦ ЗАДАЧИ +000000000000⏨+00 …`.

**Byte diffs (`cmp -l`):**
* `A` vs `PATCH`: 9 bytes in 3 machine words — 10419100-102 and 10419132-134
  (two recomputed N+2 checksum copies) and 10419492-494 (N+2 offset 44,
  RAM `0o21701`, the VIDX-12 value).
* `A` vs `RESTORE`: **empty** (byte-identical, same SHA).
* `deck A` vs `deck B`: 5 bytes at 1-based 162,163,164,165,255.

### Raw SIMH ACPU value + completion lines (`logs/acpu_C7_*.txt`, extracted from the clean batch printer captures `runs/localprn_C7_*.txt`)

```
A:      21 -0012.34  3000.00 / 21 -0056.78 / 21 -0003.75 / 21 -0000.40 / 21 -0034.50 / 21 -0040.00
B:      21 -0056.78  3000.00 / 21 -0056.78 / 21 -0004.00 / 21 -0000.40 / 21 -0034.50 / 21 -0040.00
PATCH:  21 -0012.34  3000.00 / 21 -0099.99 / 21 -0003.75 / 21 -0000.40 / 21 -0034.50 / 21 -0040.00
REST:   21 -0012.34  3000.00 / 21 -0056.78 / 21 -0003.75 / 21 -0000.40 / 21 -0034.50 / 21 -0040.00
all:    КОНЕЦ ЗАДАЧИ        +000000000000⏨+00    …
```

---

## 5. Raw C-oracle MTR (evidence only; `logs/MTR_C7_clean.txt`)

Window `BESM6_MTR_LO=022233, HI=022276, N=120`, `BESM6_DD_DEBUG=1`,
image `2048_C7_A`, deck A. Excerpt (AU = accumulator before the instruction;
MTR prints effective addresses, reg field in octal, so `(12)` = M[10 dec]):

```
MTR 22233L xta    4014(12) AU=0001600000017   ; TO card byte
MTR 22233R asx    2036(14) AU=1470346041630243; SR40 -> TO byte
MTR 22234L aax    2110(0)  AU=0000000000063   ; ASCII '3'
MTR 22234R arx    2126(0)  AU=0000000000063   ; NEG31 -> digit 3
MTR 22235L ati    6(0)     AU=0000000000003   ; M[6]=TO=3
MTR 22235R uj     22064(6) AU=0000000000003   ; TO dispatch -> table[2]
MTR 22067L uj     22242(0) AU=0000000000003   ; table[2] -> MUL handler
MTR 22242L xta    2053(14) AU=0000000000003   ; A10 = 15.0
MTR 22242R a*x    2056(14) AU=4217000000000000; A10 * B1 (2.5)
MTR 22243L atx    2104(0)  AU=4311300000000000; EST = 37.5 (computed on machine)
MTR 22243R uj     22165(0) AU=4311300000000000; -> shared converter
MTR 22165L vjm    30114(11) AU=4311300000000000 ; verbatim docs/105 converter
MTR 30114L xta    2104(0)  AU=4311300000000000
...
MTR 30121R vjm    30161(13) AU=...             ; shared floor_int
MTR 30122L ati    5(0)     AU=0000000000000   ; digit latch
MTR 30122R asn    30(0)    AU=0000000000000   ; GOST digit deposit
```

The scanner/pointer persistence was traced separately (`oracle/C7_FIXMTR*`):
`ita 12(0)` loads M[10]=0o60001, scan increments the pointer, `FOUND` writes
M[10]+1 back to N+2 `K_PTR` (offset 121), and `arx 2026(14)` (one's-complement
−1) decrements the record count 6->5->...->0. Two latent bugs in the inherited
C6 scan helper were found and fixed here: (1) `xta 0(10)` reads memory *at* the
pointer, not the register — replaced by `ita 10`; (2) the scan's local pointer
was never written back to `K_PTR`, causing record 2 to be reprocessed.

---

## 6. SHAs (SHA-256, full list `logs/sha256.txt`)

```
b3ede98828cd42ccbfe866a0c371f31a07e512d9f45a4b2cc0e11334014a525c  2048_C7_A = 2048_C7_RESTORE
229f6afb0bdebb7df2955f050b03ce0b5cab606c35fcfb0a7f34ef6d3b3848c9  2048_C7_PATCH
b6e4488aff18a3c6707a18c460036d79c4d29b696b42752cb0c1afb415d05a88  deck_c7_A.b6
eb8c86a2d3d46e7979f530203c26c36d4a3634020015c53c6e5e37938f47fb8f  deck_c7_B.b6
2f5fcf873d43c2846ee1669669e26202f32fa25e6b71e109fd20ef4452142ff5  base (FRX5-renamed, docs/108)
e35bc7bacb8088206ddacfa99e794ba1e5481a81af1ea30ce2eca5dbcf6197d9  build/c7_build.py
6a4c7791e1cf83e8b960993d952db6fc7e92b60c4fb0abfdd3f5a6dc3a1a374a  build/make_decks_c7.py
f5878398e9b5d83598064526e7a52e82c95293b74e81e7852f2df78b49f7a280  build/build_all.py
7391850c99d1826c3e6a92725571df534355c1e451e19bb316ed843428bdc037  logs/MTR_C7_clean.txt
```

---

## 7. Reproducible builder and manifest

```
cd /tmp/.private/azizz/opencode/c7-integrate
python3 build/build_all.py        # images + decks, asserts base SHA 2f5fcf87…
python3 build/run_gates.py        # four SIMH gates, checks six printed values
```

Manifest: `logs/sha256.txt`; gate captures: `runs/localprn_C7_*.txt`,
`runs/console_C7_*.txt`, `runs/ini_C7_*.ini`, `runs/drive_*.log`; MTR/CORE:
`oracle/C7_MTR_FINAL/`, `oracle/C7_CORE2/core-pc.bin`, `logs/MTR_C7_clean.txt`;
ABS/MOD fixtures: `decks/deck_c7_test_{ABS,MOD}.b6`, `oracle/C7_ABS2/`,
`oracle/C7_MOD2/`. The builder reuses verbatim `build_zone2350_contour.py`
(zone writer/checksum), `final_sign.py` (converter), `c2_build.py` (TEXT word),
`c6_build.py` (N+3 assembly/helpers), and the proven SIMH harness.

---

## 8. Honest limits (unchanged from the proven pieces)

1. FRONT has **no native intrinsic, DO or FORMAT emitter** (docs/112 §1.2,
   docs/113 §1, docs/115 §1.1). `TO=5/6/7` (intrinsic), `TK=5` (width) and
   `TK=6` (DO) are clearly labelled **build fixtures**, not native FRONT IR.
2. **DSQRT is impossible**: SIMH has one 48-bit float and no double FPU; a
   software DP Newton path exceeds 58 words (docs/112 §5.2).
3. **`READ(u,fmt)` blocked**: `777010` (READ) and `777011` (FORMAT) emitters
   are absent from the repository (docs/104 §3, docs/106); no formatted READ
   was attempted. The width fixture is a layout selector on the proven 2+2
   GOST field, not a general `Fw.d` editor.
4. **No precedence, parentheses or postfix stack.** One binary operator is
   evaluated left-to-right with operands pre-seeded in N+2 (docs/111 §5);
   SUB is magnitude-only (reverse subtract, correct only for A<B).
5. **DO is a fixed-count repeat** of one `SUM += L_VAL` body, countdown step 1
   only; no loop-variable update or body dispatch (docs/115 §4).
6. Width supports `w∈{2,3,4}`, `d∈{1,2}` only; out-of-range digits are not
   validated. SQRT is 4 single-precision Newton iterations; only the
   enumerated operand values were exercised.
7. The sign comes from the float's bit 40 via the canonical SIGNBIT patch, so
   positive values print with `-` (docs/105); no per-record sign field exists.

---

## 9. Recommendation

**Ship as a separate product variant, not as a replacement for the current
canonical `f483f6ca…` / `2f5fcf87…`.** The canonical image is the single-record
LIT+sign reference (57/58 words, one deck). C7 is deliberately a different
artifact: 40/58 words in N+3, 6-record deck, FRX5 catalog, six printed lines.
They are byte-different and serve different purposes. C7 is a strict
superset of proven features but a different input/output contract; replacing
the canonical would change the reference deck, the printer line count and
the completion checksum, so it needs an explicit product decision.

---

## 10. PASS / FAIL

| # | gate | verdict |
|:--|:--|:--|
| 1 | all four priority tiers (a)-(d) coexist in one contour | **PASS** |
| 2 | N+3 40/58 words, converter verbatim | **PASS** |
| 3 | N+2 177/649 words, offsets 526..900 untouched | **PASS** |
| 4 | shared scanner + TK/TO jump tables (no concatenation) | **PASS** |
| 5 | SIMH A: six distinct IR-driven values, КОНЕЦ ЗАДАЧИ | **PASS** |
| 6 | SIMH B: byte-identical image, 5-byte deck diff -> 2 values change | **PASS** |
| 7 | SIMH PATCH: one N+2 word -> VARIABLE line changes | **PASS** |
| 8 | SIMH RESTORE: byte-identical -> original values | **PASS** |
| 9 | C oracle: ABS and MOD intrinsics validated on fixtures | **PASS** |
| 10 | native FRONT intrinsic/DO/FORMAT emitters | **FAIL** (absent; §8.1) |
| 11 | DSQRT / double precision | **FAIL** (infeasible; §8.2) |
| 12 | formatted `READ(u,fmt)` / general `Fw.d` | **FAIL** (§8.3) |
| 13 | precedence / parentheses / postfix stack | **FAIL** (§8.4) |

DONE
