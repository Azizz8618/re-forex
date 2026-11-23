# C6 — contour executes a `DO` loop driven by IR records (build-time fixture)

> РЕЗУЛЬТАТ C6: **PASS** (честное подмножество). FRONT имеет rule 32 для DO,
> но НЕ эмитит структурированную `777005` для цикла; `TK=6, TO=1,
> TA=<bound>, TB=<step>` — build‑фикстура. Контур сканирует ТРИ записи,
> счётчик/граница/накопитель в N+2, тело `SUM += L_VAL` повторяется.
> SIMH: `TA=02 → 21 -0040.00`, `TA=03 → -0060.00`, правка слова счётчика
> → `-0020.00`, restore → `-0040.00`. 40/58 слов N+3, 165/649 N+2,
> 526..900 не тронуты. Нет обновления переменной цикла и dispatch тела.

Date: 23.11.2026. Workspace `/tmp/.private/azizz/opencode/c6-do/` (symlink to
`/home/azizz/c6-do-store`; `/tmp` tmpfs был 100 % заполнен, как в docs/111–114).
Copies only: репозиторий, живые диски, tmux session 0 и C‑исходники `dispak`
не правились; C `dispak` использовался **только как oracle** (MTR/CORE,
docs/88). Авторитетные результаты — полные SIMH ACPU/printer‑захваты с
локальным `-n prn0`. Колода содержит только `ДИС 41(2048)^`, `*NAME FRX5XX`,
`*TRANS:FRX5*,,412350` плюс стандартную Fortran‑обвязку и три IR‑карты;
ни `*FOREX`, ни `*FTN`, ни `*perso`.

---

## VERDICT

| gate | image | deck / change | SIMH printer line 102 | verdict |
|:--|:--|:--|:--|:--|
| **A** | `2048_C6_FRX5_A` | `TA=02` (bound 2) | ` 21 -0040.00  3000.00` | **PASS** |
| **B** | `2048_C6_FRX5_A` (byte-identical) | `TA=03` (bound 3, 1 deck byte) | ` 21 -0060.00  3000.00` | **PASS** |
| **PATCH** | `2048_C6_FRX5_PATCH` (one N+2 counter word) | same deck as A | ` 21 -0020.00  3000.00` | **PASS** |
| **RESTORE** | `2048_C6_FRX5_RESTORE` = A byte-for-byte | same deck as A | ` 21 -0040.00  3000.00` | **PASS** |

All four printers ended with:
` КОНЕЦ ЗАДАЧИ        +000000000000⏨+00    0000206320000000` (prn line 116).

---

## 1. TASK 1 — how FRONT encodes `DO` (FACT, file:line citations)

### 1.1 What FRONT really emits for a counted `DO`

`src/newcomp/FRONT.FTN` recognises a counted `DO` as **rule 32**, but emits **no
structured `777005` IR** for it:

| statement | citation |
|:--|:--|
| `N1.4 IR emission: 777001/777002/777003/777004, all numeric, PRINT + I8` | `FRONT.FTN:20` |
| `M1 rules 30..37: … 32 counted DO …` | `FRONT.FTN:21-22` |
| IR contract lists `777001`, `777002`, `777003`, `777004` only; `777005` is not a DO record | `FRONT.FTN:26-30` |
| rule 32 recognition: `C(IFIRST)= 'D'` (68), `C(IFIRST+1)= 'O'` (79) → `IRULE=32, ITYPE=1` | `FRONT.FTN:137-142` |
| rules 31/32/34/35 stream the **raw logical line** into `777002` ASCII | `FRONT.FTN:188-199` |
| `777005` structured postfix RHS is emitted **only for `IRULE=31`** (assignment) | `FRONT.FTN:208-209`, `:352` |
| `777005 <seq> <TK> <TO> <TA> <TB>` via `PRINT 9005` / `9005 FORMAT(1X,6I8)` | `FRONT.FTN:346-350`, `:376` |
| native token kinds of the `777005` emitter: TK=1 LIT, TK=2 VARIABLE, TK=3/4 operators | `FRONT.FTN:254-259`, `:262-276`, `:299-345` |
| rule 32 additionally requests a `777004` label (kind 21) | `FRONT.FTN:353-368` |

Therefore a `DO` line yields `777001(<seq>,32,1)` + `777002` ASCII chunks +
`777004` label request, **never** a TK/TO/TA/TB loop record. This is exactly the
boundary recorded in `docs/73-release-report.md` §4.3: *«DO‑guard F77PREP, тело
цикла … нашим кодом не исполняются»* (FACT). A native DO IR would require
editing FRONT/F77PREP, which is outside this contour task.

### 1.2 Documented build-time fixture (NOT native FRONT)

We keep the proven `1X,6I8` `777005` card and reuse its fields with a TK value
FRONT never produces, exactly as C4 used `TO=5/6/7` (docs/112 §1.3) and C5 used
`TK=5` (docs/113 §1):

```
  777005       8       6       1      02       1
                |       |       |       |       |
               SEQ     TK=6   TO=1   TA=02   TB=1
                       fixture body selector  bound  step
```

* **TK=6** — loop record. FRONT emits only TK=1..4 (`FRONT.FTN:254-345`); TK=6
  is a **build-time test fixture**, not a native FRONT record.
* **TO=1** — body selector. The deck supplies `1`; the only implemented body
  is `ADD`. TO is **not** decoded into a dispatch and is **not** a general jump
  target (honest limitation, §4.3).
* **TA=02 / TA=03** — two-digit loop bound, decoded on machine into `L_BOUND`
  (N+2 offset 130). This is the deck A/B difference (one byte, `2`→`3`).
* **TB=1** — one-digit step, decoded into `L_STEP` (N+2 offset 131); the loop
  implementation is a countdown with decrement 1, so step=1 is the only
  supported value (§4).

The card layout was verified on-machine from the C‑oracle CORE dump at contour
entry (`oracle/C6_FRX5_A/core-pc.bin`; decoded in §3.1): record 3 occupies
`0o64022..0o64025`, `W+1` byte4 = `'6'` (TK), `W+2` byte0 = `'1'` (TO),
bytes 2/3 = `'0','2'` (TA), byte5 = `'1'` (TB).

---

## 2. TASK 2 — machine implementation (reuse first)

### 2.1 Verbatim reuse

| component | proven source | how reused |
|:--|:--|:--|
| canonical zone writer / checksum | `tools/build_zone2350_contour.py`, `build/build_e2e.py::rz/wz` | unchanged |
| multi‑record `777005` scanner, TK/TA decode, LIT/VARIABLE readers, on‑machine TEXT compare | docs/114, `build/c2b_build.py` | reused verbatim for records 1 and 2, and extended by a third scan for record 3 |
| ABS+2+2 GOST, sign block, both reclaims, shared `floor_int`, resident `*64 2004` | docs/105 `final_sign.py` | verbatim in N+3, wrapped as a VJM subroutine, three calls |
| N+2 free word map / `UTC 20000` reach / 526..900 exclusion | docs/110 (C1) | verbatim |
| FRX5 catalog rename + 6‑char `*NAME` | docs/108, `tools/forex500-ir4sign/rename_catalog.py` | repo tool reused unchanged |
| SIMH ini/destination driver and C‑oracle wrapper | docs/100/104/109/114 | copied, only workspace paths adapted |

New code is confined to `build/c6_build.py` (`emit_do()` and three N+2 branches)
and `build/make_decks_c6.py` (fixture decks). No emulator mechanism, no C patch.

### 2.2 The loop

Zone N+2 cells (RAM `0o21637+k`, all inside the clean free range):

| offset(s) | role |
|:--|:--|
| 1..45 | C2b symbol table (name at VIDX, value at `32+VIDX`) |
| 110..123 | C2b constants |
| **124** | `K_ZERO = 0` |
| **125** | `K_DECR = MASK^1` (one's-complement −1). **PATCH changes this one word** to `MASK^2` (−2) |
| **126** | `K_DO_KIND = 6` (expected TK) |
| **130 / 131** | `L_BOUND` / `L_STEP` decoded from TA / TB of the `TK=6` record |
| **132 / 133** | `L_CNT` (live counter) / `L_SUM` (accumulator) |
| **134** | `L_VAL = f32(200.0)` (per‑iteration addend; mechanism constant, not a result digit) |
| 200..340 | scanner + dispatch + readers + DO handler (282 halfwords = 141 words) |
| 526..900 | **never written** (load‑bearing overlay; verified 0 changed words) |

Machine sequence (`0o22336..0o22362`, from `logs/MTR_C6_clean.txt`):

```
22336L uza  -> DO_DECODE          ; TK ^ 6 == 0 (TK=6 fixture)
22340..22345  two-digit TA -> ACC = 10*tens + units
22346L atx  L_BOUND              ; ACC=2 for deck A, 3 for deck B
22347..22350  one-digit TB -> ACC = step
22350R atx  L_STEP               ; ACC=1
22351R atx  L_CNT                ; CNT = bound
22352R atx  L_SUM                ; SUM = 0
22353L xta  L_SUM                ; LOOP:
22353R a+x  L_VAL                ;   body: SUM += 200.0   (FPU)
22354L atx  L_SUM                ;   store accumulator in N+2
22355L arx  K_DECR               ;   CNT -= 1
22355R atx  L_CNT
22356L uza  -> DO_DONE           ;   exit when CNT == 0 (also on −0)
22356R uj   -> LOOP
22357R atx  EST                  ; DO_DONE: EST = SUM (N+2 -> EST)
22360/22361  reseed 0o2006/0o2007
22362L vjm  30114                ; verbatim docs/105 converter -> *64 2004
```

`EST = SUM` is machine‑derived: MTR shows the FPU sums
`0 → 0o4414400000000000 (f32 200.0) → 0o4454400000000000 (f32 400.0)`.
The converter divides by 10 and prints `40.00` (docs/105 scaling, same path as
the proven `0012.34` / `0056.78` lines). No host computed any printed digit.

### 2.3 Word budget

| resource | used | limit | verdict |
|:--|--:|--:|:--|
| N+3 code (`0o30114..0o30205`) | **40 words** (80 hw: converter 74 hw + pad + `floor_int` 6 hw) | 58 | **PASS** (18 free) |
| N+2 changed words | **165** (max offset 340) | 649 | **PASS** |
| N+2 offsets 526..900 | **0 changed** | must be untouched | **PASS** |
| low‑RAM scratch | only proven‑free cells (`EST`, `CARD`, `T[]`, `HALF`) | 30 proven‑free cells | **PASS** |
| zone N+4 | not used | unavailable | **PASS** |

The GOST‑converter stays byte‑for‑byte verbatim in N+3; the scanner and the
new loop live in free N+2 words, exactly the architectural tradeoff disclosed
in docs/114 §4.1 (N+2 code execution is proven there and here).

---

## 3. TASK 3 — decisive SIMH A/B/PATCH/RESTORE (authoritative)

Driver `build/drive_c2.py` (copied from docs/100/104/109/114), isolated tmux
socket, `ДATA:` marker via `capture-pane`, `ДАЙ А0` / `ДАЙ А1` / `НОМВ` before
the deck, post‑job‑start `НОМВ`, stock `attach -n prn0` with only the capture
path redirected.

### 3.1 Raw ACPU/printer (lines 99–102 and 116 of `runs/localprn_C6_*.txt`)

```
A       : *NAME FRX5XX / *TRANS:FRX5*,,412350
           21 -0012.34  3000.00
           21 -0056.78  3000.00
           21 -0040.00  3000.00          <-- bound 2, two body executions
           КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000
B       : 21 -0012.34 / 21 -0056.78 / 21 -0060.00 / КОНЕЦ ЗАДАЧИ
PATCH   : 21 -0012.34 / 21 -0056.78 / 21 -0020.00 / КОНЕЦ ЗАДАЧИ
RESTORE : 21 -0012.34 / 21 -0056.78 / 21 -0040.00 / КОНЕЦ ЗАДАЧИ
```

Raw SIMH ACPU device logs (`runs/acpu_C6_*.txt`) are byte‑identical across the
four runs (SHA `ae565a30…`); the value lines above are from the printer device
`localprn_C6_*.txt` (the authoritative print capture in docs/100/114).

### 3.2 Causality / byte diffs

* `cmp deck_A deck_B` = **1 byte**, 1‑based offset 263, octal `62` (`'2'`) →
  `63` (`'3'`) in TA. Image byte‑identical (same SHA). With the same image the
  result changes `40.00 → 60.00`: the IR bound field alone selects the
  iteration count.
* `cmp image_A image_PATCH` = **3 bytes in 3 machine words**:
  `10419097, 10419129` (two recomputed N+2 checksum copies) and `10420137`
  (octal `376`→`375`, i.e. `K_DECR` = −1 → −2 at N+2 offset 125).
  With deck A (bound 2) the counter reaches zero after one body execution, so
  the result changes `40.00 → 20.00`. This is a one‑word patch of **our own
  counter constant**, not of a precomputed result.
* `cmp image_A image_RESTORE` = empty (same SHA), result returns to `40.00`.
* Card layout at contour entry (C‑oracle CORE, FACT): `0o64012` record 1 LIT,
  `0o64016` record 2 VARIABLE, `0o64022` record 3 `TK=6` fixture; each card
  starts on a word boundary and the scanner finds the marker rather than
  assuming a stride (docs/114 §1.3).

### 3.3 Raw C‑oracle MTR (oracle only, `logs/MTR_C6_clean.txt`)

Excerpt (AU before each instruction; effective addresses; deck A):

```
MTR 22340L xta  4014(12) AU=...        ; W+2 of record 3
MTR 22341R arx  2111(0)  AU=...0060    ; TA tens ASCII '0' (0o60)
MTR 22345R arx  2127(6)  AU=0000000000002
MTR 22346L atx  2041(14) AU=0000000000002   ; L_BOUND = 2 (from deck)
MTR 22350R atx  2042(14) AU=0000000000001   ; L_STEP = 1 (from deck)
MTR 22351R atx  2043(14) AU=0000000000002   ; L_CNT = bound
MTR 22352R atx  2044(14) AU=0000000000000   ; L_SUM = 0
MTR 22353R a+x  2045(14) AU=0000000000000   ; iter 1 body
MTR 22354L atx  2044(14) AU=4414400000000000
MTR 22355L arx  2034(14) AU=0000000000002   ; CNT before decrement
MTR 22355R atx  2043(14) AU=0000000000001
MTR 22356L uza  2357(7)  AU=0000000000001   ; not done -> loop
MTR 22353R a+x  2045(14) AU=4414400000000000 ; iter 2 body
MTR 22354L atx  2044(14) AU=4454400000000000 ; SUM = f32(400.0)
MTR 22355R atx  2043(14) AU=7777777777777777 ; CNT = −0
MTR 22356L uza  2357(7)  AU=7777777777777777 ; exit
MTR 22357R atx  2104(0)  AU=4454400000000000 ; EST = SUM -> GOST
MTR 22362L vjm  30114(11)                     ; verbatim converter
```

`M[12]=0o60010` is the advanced card pointer (record 3), `M[14]=0o20000` the
N+2 base, `M[7]=0o20000` the short‑branch base (all as in docs/114).

---

## 4. Honest subset / exact overrun (no faking)

**Implemented (FACT):** a fixed‑count repeat of **one** IR operation — FPU
`SUM += L_VAL` — with the bound decoded from `TA` of a `TK=6` fixture record,
counter/bound/step/accumulator held in N+2, result fed into the verbatim
docs/105 GOST print. Bound 2 and 3 were executed; the countdown and the one‑word
counter patch were proved under full SIMH.

**Not implemented / exact limits:**

1. **No native FRONT DO IR exists** (§1.1). A general DO driven by native FRONT
   output is blocked by the absent emitter, independently of the word budget.
   Our `TK=6` card is a clearly labelled build fixture, not a FRONT record.
2. **Step > 1 is not supported.** The step digit TB is decoded and stored in
   `L_STEP`, but termination is countdown‑to‑zero with decrement 1; any step
   other than 1 (or a bound not divisible by the step) would not terminate
   correctly. This is a fixed‑count repeat, not a general `DO var=init,lim,step`.
3. **No body‑target dispatch.** TO=1 is accepted as the only body (`ADD`); the
   loop variable is not updated, there is no label/branch target from TB, and
   no arbitrary IR operation sequence may be placed in the body.
4. **Exact overrun for a combined general body.** Reusing the full 4‑digit
   converter (40 words) together with C4's intrinsic dispatch (decode 4 + ABS 2
   + SQRT 13 + MOD 9 = 28 words) needs **68 words in N+3, i.e. 10 words over**
   the 58‑word ceiling (measured in docs/112 §2.3). A general postfix stack
   scanner likewise does not fit in 58 words (docs/111 §1/§5.1). Our design
   avoids this by keeping the converter verbatim in N+3 and all new code in the
   649 free N+2 words.
5. **Print range.** The docs/105 2+2 field prints at most two integer digits;
   the addend is therefore `f32(200.0)` so `bound × addend` stays ≤ 600 (EST
   ≤ 600, printed 20/40/60). A larger addend overflows the field (observed and
   corrected during development); it is not silently claimed to work.

---

## 5. PASS / FAIL

| # | criterion | verdict |
|:--|:--|:--|
| 1 | FRONT DO encoding with file:line citations; no native `777005` DO IR stated | **PASS** |
| 2 | documented `777005` fixture `TK=6, TA=bound, TB=step`, clearly labelled | **PASS** |
| 3 | C2b scanner extended to a third record; TA/TB decoded on machine | **PASS** |
| 4 | counter/bound/step/accumulator in N+2; body re‑executed; sum in N+2 | **PASS** |
| 5 | verbatim docs/105 GOST print path used (3 VJM calls) | **PASS** |
| 6 | N+3 40/58; N+2 165/649; offsets 526..900 untouched | **PASS** |
| 7 | SIMH A: bound 2 → `21 -0040.00`, КОНЕЦ ЗАДАЧИ | **PASS** |
| 8 | SIMH B: byte‑identical image, 1 deck byte → `21 -0060.00`, КОНЕЦ ЗАДАЧИ | **PASS** |
| 9 | SIMH PATCH: one machine word of OUR counter → `21 -0020.00`, КОНЕЦ ЗАДАЧИ | **PASS** |
| 10 | SIMH RESTORE: byte‑identical image → `21 -0040.00`, КОНЕЦ ЗАДАЧИ | **PASS** |
| 11 | C‑oracle MTR/CORE agree; values machine‑derived only | **PASS** |
| 12 | native FRONT DO IR / general DO (variable step, body target, loop variable) | **FAIL** (absent emitter, §4.1–4.3; overrun §4.4) |
| 13 | general FORMAT/runtime semantics / `777001..777004` executed by our code | **FAIL** (out of scope; docs/73 §4.3, docs/114 §4.2) |

---

## 6. FACT / INFERENCE

**FACT (observed):** FRONT source lines above; `DO` produces no `777005`;
CORE card layout of three records; MTR bound 2/3 decode, two body iterations,
counter decrement and `EST=SUM`; four SIMH printer lines and completion lines;
`cmp` 1 deck byte / 3 image bytes / 0 restore bytes; 40/58 and 165/649 budgets;
0 changed overlay words.

**INFERENCE (not proven):** that a third record always starts exactly 4 words
after the second (we observed one 3‑record deck; the scanner searches for the
marker, so a different stride would still be found, but was not tested);
that a `TK=6` record could be consumed by any future FRONT/generator (it cannot,
without an emitter); that step values other than 1 would work (they would not,
§4.2); that a general body could be fitted by further N+2 displacement (not
attempted; the measured N+3 overrun for C4 coexistence is 10 words).

---

## 7. SHA‑256 (full list `logs/sha256.txt`)

```
dd2c145d8a26319fc5edfce8aa1499055ce2dbd37b3834850509e37b7e763b78  images/2048_C6_A
d69ca74745ebf783e9cf83cce236f8248b5aa9e5b48be575df1304d9e61dd782  images/2048_C6_FRX5_A = _RESTORE
a66f4d46cd9d3a153b3ed3caf4ff288bedc3d11450a7b7ddefe8076ab89409ab  images/2048_C6_FRX5_PATCH
58de170c9694fcd7ae31483b5928f07d3c843b9139cf4aeffbc980269f07e1fa  decks/deck_c6_A.b6
e1e0091f9bbbf6bd4f69242e4428e09d1722d17685eefd2a0a2c61fdfb86b295  decks/deck_c6_B.b6
5ec72896b10079b7e2fcf3f7afd85b7c5b598e50f123d2913a01304d40ae2290  runs/localprn_C6_A.txt
52521036084c9d0db3bbd992cea2a6bc53c50c62745b493787e08886b406b2ea  runs/localprn_C6_B.txt
79f7259eed497ef066d52287a13ef3f2d4e4a0f7829aa78d5877b03ee71fbffc  runs/localprn_C6_PATCH.txt
9bf6c7286133145d6fb68b71921b473fa364287fba7af2b5f6ef6e3a8b0b1c5c  runs/localprn_C6_RESTORE.txt
ae565a30e562f8e9443fbd4a48c43ffb1e15458b769679087f4287bd73f8fdfb  runs/acpu_C6_{A,B,PATCH,RESTORE}.txt
4f92c80cb7f06afca75dd402831348b2eb99ce7f65f862f749955d18d22470e2  logs/MTR_C6_clean.txt
ff49f1d94c9ef8d5db8fea28a5d1a65dda4ed81e4169c7b10e6ce9a9a41e9cf4  build/c6_build.py
c7178e66fa356eda55f7462c4d3b19dbe56cbe5ae8ceb978e62a417dfdffb308  build/make_decks_c6.py
```

---

## 8. Evidence index

```
build/c6_build.py                 loop builder (reuses c2b_build.py verbatim parts)
build/make_decks_c6.py            fixture decks (TA 02 vs 03, 1 byte apart)
decks/deck_c6_{A,B}.b6            IR fixture decks (only *TRANS:FRX5*,,412350)
images/2048_C6_FRX5_{A,PATCH,RESTORE}
runs/localprn_C6_{A,B,PATCH,RESTORE}.txt   authoritative SIMH printer captures
runs/acpu_C6_*.txt                raw SIMH ACPU device logs
runs/console_C6_*.txt, runs/ini_C6_*.ini   raw consoles and per-case configs
oracle/{C6_FRX5_A,C6_DECODE}/     raw C-oracle MTR/CORE (oracle only)
logs/MTR_C6_clean.txt             clean MTR excerpt
logs/sha256.txt                   full SHA-256 inventory
```

DONE
