# C2b — multi-record `777005` scanner, two-digit VIDX, on-machine TEXT-name compare

> РЕЗУЛЬТАТ C2b: **PASS** — контур сканирует ДВЕ записи `777005` в буфере
> карт `0o64000+`, разбирает LIT (TK=1) и VARIABLE (TK=2) с двухзначным VIDX
> (12/13), сравнивает 6‑битное TEXT‑имя на машине и печатает обе величины.
> SIMH A/B/C/X: `12.34` + `56.78`; смена VIDX `12→13` → `90.12`; правка слова
> N+2 → `99.99`; restore → `56.78`; несовпадение имени → `0000.00`.
> Все `КОНЕЦ ЗАДАЧИ`. Бюджет 40/58 слов N+3, код/данные в N+2,
> офсеты 526..900 не тронуты.

Date: 23.11.2026. Workspace `/tmp/.private/azizz/opencode/c2b-scanner/` (symlink to
`/home/azizz/c2b-scanner-store` because `/tmp` tmpfs was full).
Copies only. The repository, live disks, tmux session 0 and the C `dispak` sources were
never edited; every image/disk/deck is a copy. C `dispak` was used **as oracle only**
(MTR/CORE hooks, docs/88). All authoritative results are full SIMH ACPU/printer captures
with workspace-local `prn0`; stock `attach -n prn0/prn1` semantics were kept (only the
file path changed). Deck contains only `*TRANS:FRX5*,,412350` with `*NAME FRX5XX` and
`ДИС 41(2048)^` plus standard Fortran framing; no `*FOREX`/`*FTN`/`*perso`.

> РЕЗУЛЬТАТ: **PASS**. Контур сканирует два `777005` в буфере колод, разбирает TK/TA,
> обрабатывает LIT (TK=1) и VARIABLE (TK=2) с двухзначным VIDX (12/13), сравнивает
> 6-битное TEXT-имя на машине и печатает **обе** величины. SIMH A/B/C/X:
> `0012.34` + `0056.78`; правка VIDX в деке → `0090.12`; правка одного машинного
> слова значения → `0099.99`; байтово тождественный restore → `0056.78`.
> Все четыре задания дошли до `КОНЕЦ ЗАДАЧИ`.

---

## VERDICT

| gate | image | deck / change | SIMH printer lines 100-101 | verdict |
|:--|:--|:--|:--|:--|
| **A** | `2048_SCAN_FRX5_A` | `LIT 1234`, `VAR VIDX=12` | ` 21 -0012.34  3000.00` / ` 21 -0056.78  3000.00` | **PASS** |
| **X (VIDX)** | same image, byte-identical | deck VIDX `12`→`13` (1 byte) | ` 21 -0012.34` / ` 21 -0090.12` | **PASS** |
| **B (patch)** | `2048_SCAN_FRX5_B` (one N+2 value word) | same deck as A | ` 21 -0012.34` / ` 21 -0099.99` | **PASS** |
| **C (restore)** | `2048_SCAN_FRX5_C` = A byte-for-byte | same deck as A | ` 21 -0012.34` / ` 21 -0056.78` | **PASS** |
| **NAME control** (oracle) | `2048_SCAN_FRX5_NAMEMISMATCH` | same deck as A | ` 21 -0012.34` / ` 21  0000.00` (mismatch detected) | **PASS** |

All five (four SIMH + one oracle) reached `КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000`.

---

## 1. TASK 1 — exact card-buffer layout of TWO `777005` records

### 1.1 Method (FACT)

C-oracle run `oracle/TWO_DUMP/` (deck `decks/deck_two_records.b6`) with
`BESM6_CORE_ON_PC=01770`, `BESM6_CORE_SKIP=6`; CORE is 65536 words, 6 bytes/word,
bytes MSB-first. Raw decode in `logs/card_buffer_two_records.txt`. The card buffer is
RLE-packed 8-bit ASCII at RAM base **0o64000**: byte `0x80+n` = n spaces, `0x0a` pads
the tail of each card word (docs/104 §1, docs/109 §1; this run reproduces both).

### 1.2 Measured layout (FACT)

| RAM word(s) | content (decoded) | role |
|:--|:--|:--|
| `0o64000..0o64002` | `*NAME OURMRK` | job card 1 |
| `0o64003..0o64006` | `*TRANS:OURMRK*,,412350` | job card 2 |
| `0o64007..0o64011` | `      PROGRAM MAIN` | Fortran framing |
| **`0o64012..0o64015`** | `  777005       6       1       0    1234       0` | **IR record 1 (LIT)** |
| **`0o64016..0o64021`** | `  777005       7       2       0       2       0` | **IR record 2 (VARIABLE)** |
| `0o64022` | `      END` | framing |
| `0o64023..0o64024` | `*EXECUTE` | framing |
| `0o64025..0o64026` | `*END FILE` | framing |
| `0o64027` byte 0 | `0xff` (then zeros + `0x0a` pad) | last non-pad byte |

Within a `777005` card, relative to its first word `W`:

| word | decoded bytes | field |
|:--|:--|:--|
| `W`   | `82 37 37 37 30 30` = `  77700` | start marker (2 spaces + first 5 chars) |
| `W+1` | byte0 `35`=`'5'` completes `777005`; byte2 = SEQ; **byte4 = TK** | record kind |
| `W+2` | byte0 = TO; **bytes 2,3 = two-digit TA/VIDX**, or bytes 2..5 = 4-digit LIT | operand |
| `W+3` | tail (`0x0a` pad when the text ends mid-word) | end of card |

FACT details from this CORE dump:

* Record 1 at `0o64012`: `W+1` = `35 87 36 87 31 87` → `5 <7sp> 6 <7sp> 1 <7sp>`
  (SEQ=6 at byte2, **TK=1 at byte4**); `W+2` = `30 84 31 32 33 34` →
  `0 <4sp> 1234` (LIT digits at bytes 2..5).
* Record 2 at `0o64016`: `W+1` = `35 87 37 87 32 87` (SEQ=7, **TK=2**);
  `W+2` = `30 87 32 87 30 a3` → `0 <7sp> 2 <7sp> 0 <35sp>` (single-digit VIDX at
  byte 2 — exactly as docs/109). With two-digit TA `12`, `W+2` =
  `30 86 31 32 87 30` → `0 <6sp> 12 <7sp> 0` (**tens at byte 2, units at byte 3**).
* Each card is padded with `0x0a` to a whole word; the next card starts at the next
  word boundary. There is **no fixed card slot length**: record 1 used 4 words
  (`0o64012..0o64015`), record 2 used 4 words including one all-pad word
  (`0o64016..0o64021`) because its text ended exactly on a word boundary.
* The terminating `0xff` at `0o64027` byte0 is the last non-pad byte after
  `*END FILE`.

### 1.3 FACT vs INFERENCE

* **FACT:** addresses, RLE bytes, marker word `0o823737373030` (`82 37 37 37 30 30`),
  TK at `W+1` byte4, VIDX digits at `W+2` bytes 2/3, the `0x0a` per-word pad,
  and the trailing `0xff`. All read directly from `oracle/TWO_DUMP/core-pc.bin`.
* **INFERENCE (not proven by a third record):** that the *general* rule is
  "records are contiguous RLE cards, each starting on the next word boundary".
  Two records were observed; the scanner therefore searches for the marker rather
  than assuming a fixed stride.
* **INFERENCE:** `0xff` is the GOST/deck EOF sentinel (docs/20: `GOST_EOF = 0xFF`).
  The machine scanner does **not** use it; it processes a fixed count of two records
  (see §5 missing primitives).

---

## 2. TASK 2 — machine-code implementation

### 2.1 Architecture (reuse of proven code)

* **Zone N+3 (RAM `0o30114..`) — 40/58 words, 80 halfwords**, verbatim canonical
  docs/105 converter: ABS+2+2 GOST chain, sign block, both reclaims
  (`floor_acc`, `drop_last_ati`), shared `floor_int` at `0o30161`, resident
  `*64 2004`. The converter is wrapped as a **VJM subroutine called twice**;
  inner `floor_int` calls use link M[11(dec)] (`vjm ... (13)` in MTR), the two
  outer calls use M[9(dec)] (`vjm ... (11)` in MTR). Before each call the main
  resets the two GOST print seed words `0o2006`/`0o2007`, otherwise the second
  call's `arx`-deposits accumulate on the first call's digits (this was found and
  fixed; final MTR shows clean 5,6,7,8 deposits).
* **Zone N+2 (free words)** holds the new code and data: symbols at offsets
  1..45, constants at 110..123, scanner/dispatch/readers at offsets **200..301**
  (RAM `0o22147..0o22295`). Reaching and executing code in N+2 uses the proven
  `UTC`/MMU mechanism of docs/110; a C-oracle MTR experiment proved instruction
  fetch from `0o22003`/`0o22147` (`MTR 22147L uj 30114`). **Offsets 526..900 were
  never written** (verified: 0 changed words in that range).
* Entry substitution at body `0o11` = long `uj 0o22147` (FRX5 catalog variant of
  the canonical image, produced by the repo's `tools/forex500-ir4sign/
  rename_catalog.py`, docs/108).

### 2.2 Scanner (N+2 code)

1. Re-arm base registers: M[12(dec)] = `0o20000` (N+2 base, from low-RAM `HALF`
   cell), M[7] = `0o20000` (short-branch base), M[10(dec)] = persistent card
   pointer from N+2 cell `K_PTR` (initially `0o60000`). Re-arming is repeated at
   every step because the converter clobbers some registers.
2. `xta 4012(reg=10)` reads the card word at `M[10]+0o4012`; `aex MARK` with
   `MARK = 0o823737373030` (N+2 constant); `uza` (logical zero test) branches to
   the record body on an exact marker match, otherwise pointer `+1` and loop.
3. TK from `W+1` byte4: `asx SR8 / aax M8 / arx PD0 / aax M8`, then `aex 1` and
   `uza` dispatch TK=1 → LIT reader, TK=2 → VARIABLE reader.
4. After record 1, `K_PTR += 4` (the observed distance `0o64016-0o64012`), and
   the scan+process sequence is repeated for record 2. (Two iterations are
   unrolled; see §5.)

### 2.3 LIT reader (TK=1) — reused docs/104 chain

`W+2` bytes 2..5 → four ASCII digits via `asx SR24/SR16/SR8`/low byte,
`aax M8`, `arx NEG31`, `10*T[]` assembly with `arx T0(reg=6)`, `e+x EMASK/C105`
normalization, `*100` recombination from N+2 constant `K_HUNDRED=f32(100)`,
`/10`, `atx EST`. MTR proves `1234` → `f32(1234)` → `EST=123.4`.

### 2.4 VARIABLE reader (TK=2) — two-digit VIDX + TEXT-name compare

* `W+2` byte2 → tens via `asx SR24` (N+2 constant), byte3 → units via
  `asx SR16`; each goes through `aax M8 / arx PD0 / aax M8` (works for digit 0,
  unlike the docs/98 `NEG31` trick). `arx T0(reg=M[6]=tens)` then `ati 6` gives
  VIDX = `10*tens + units` (MTR: `vidx = 0o14` = 12 for card `12`).
* **On-machine name compare:** expected 6-bit TEXT code = `VIDX + 28`
  (`arx K_28`), `asx SHL42` (left shift 42), `arx SP7` (7 zero codes), stored in
  `NUM`. Actual name word read from N+2 offset `VIDX` with `utc 20000` +
  `xta 21637(reg=6)`. `aex NUM` XOR; `uza` branches on a match. On mismatch the
  contour sets `EST = 0` so the second line prints `0000.00` with a space sign —
  a machine-visible mismatch signal (C-oracle gate `NAME`).
* Value word at N+2 offset `32+VIDX` is loaded with `utc 20000` +
  `xta 0o1657(reg=6)`, `/10`, `atx EST`, then the same proven converter prints it.

N+2 symbol table (FACT from CORE/print): VIDX 12 → name `H`, value `f32(5678.0)`;
VIDX 13 → name `I`, value `f32(9012.0)`; plus the historical X/Y entries.

### 2.5 Machine-code constants (all mechanism values, no result digits)

`K_BASE=0o20000`, `K_CBASE=0o60000`, `K_ONE=1`, `K_FOUR=4`,
`K_MARK=0o823737373030`, `K_SR24=(64+24)<<41`, `K_28=28`, `K_SP7=0`,
`K_SHL42=(64-42)<<41`, `K_NEGONE=MASK^1` (BESM-6 is one's-complement),
`K_HUNDRED=f32(100)`, `K_PTR=0o60000`, `K_GOSTA/K_GOSTB` = seed words of
`0o2006`/`0o2007`. The digit values themselves are never stored in the image.

---

## 3. TASK 3 — decisive SIMH A/B/C/X (authoritative)

Driver `build/drive_c2.py` (copied from docs/100/104/109), isolated tmux socket,
`ДATA:` marker via `capture-pane`, `ДАЙ А0`/`ДАЙ А1`/`НОМВ` before the deck,
post-job-start `НОМВ`, stock `-n prn0` with only the capture path redirected.
Raw captures `runs/localprn_C2B_{A,V13,B,C}.txt`, lines 98-102 and 115:

```
A    : *NАМЕ FRХ5ХХ / *ТRАNS:FRХ5*,,412350
       21 -0012.34  3000.00
       21 -0056.78  3000.00
       КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000
V13  : 21 -0012.34 / 21 -0090.12 / КОНЕЦ ЗАДАЧИ
B    : 21 -0012.34 / 21 -0099.99 / КОНЕЦ ЗАДАЧИ
C    : 21 -0012.34 / 21 -0056.78 / КОНЕЦ ЗАДАЧИ
```

The FRX5 header cards are printed by the monitor exactly as required; the deck
contains only `ДИС 41(2048)^` and `*TRANS:FRX5*,,412350` as translator controls.

### Causality / byte diffs (`logs/byte_diffs.txt`)

* `cmp A B` = **9 bytes in 3 machine words**: two recomputed N+2 checksum copies
  (offsets 10419100-10419102, 10419132-10419134) and the VIDX-12 value word
  (offsets 10419492-10419494, N+2 offset 44, RAM `0o21701`). `5678.0 → 9999.0`
  changes only the **second** printed value.
* `cmp A C` = empty (byte-identical restore, same SHA).
* `cmp deck_A deck_V13` = **1 byte**, 1-based offset 214: octal `62` (`'2'`) →
  `63` (`'3'`). Same image, second line changes `0056.78 → 0090.12`.
* `cmp A NAMEMISMATCH` changes only the VIDX-12 name word → second line
  `0000.00` (name compare path), oracle only.

### Raw C-oracle MTR (oracle only, `logs/MTR_c2b_scanner.txt`)

Excerpt (AU before each instruction; MTR prints effective addresses):

```
MTR 22155L xta    4012(12) AU=0...60000     ; card word at pointer
MTR 22155R aex    2021(14) AU=4043346715630060 ; marker word
MTR 22156L uza    2161(7)  AU=0             ; match -> record 1 body
MTR 22166R ati    5(0)    AU=1              ; TK=1 -> LIT
...
MTR 22207L xta    4014(12) ...              ; LIT TA digits
MTR 22216R atx    2103(0) AU=4551510000000000 ; f32(1234) on machine
MTR 22217R atx    2104(0) AU=4357331463146315 ; EST=123.4
MTR 22220L vjm    30114(11)                 ; outer call -> converter
...
MTR 22154L xta    2030(14) AU=0...60004     ; K_PTR advanced by 4
MTR 22155L xta    4012(12) ...              ; second marker at 0o64016
MTR 22251R ati    6(0)    AU=1              ; VIDX tens
MTR 22255L ati    6(0)    AU=14             ; VIDX = 12 on machine
MTR 22261L aex    2103(0) AU=5400000000000000 ; TEXT name XOR (H matches)
MTR 222x  a/x/... EST=567.8 -> converter -> *64 prints -0056.78
```

Full clean excerpt and all oracle outputs are in `oracle/` and `logs/`.

---

## 4. TASK 4 — word budget and missing primitives

### 4.1 Exact budget

| resource | used | limit | verdict |
|:--|--:|--:|:--|
| N+3 code (zone `0o30114..0o30205`) | **40 words / 80 halfwords** (CONV 74 hw + pad + `floor_int` 6 hw) | 58 words | **PASS** (18 words free) |
| N+2 total changed words | **161** (symbols 1..45, constants 110..123, code 200..301) | 649 | **PASS** |
| N+2 offsets 526..900 (load-bearing) | **0 changed** | must be untouched | **PASS** |
| low-RAM scratch | proven-free cells only (T[] tables, HALF as N2 base, etc.) | 30 proven-free cells | **PASS** |
| zone N+4 | not used | unavailable | **PASS** |

**Tradeoff / deviation (disclosed):** the scanner, both readers and the name compare
execute from **zone N+2**, not N+3. This is a deliberate architectural choice: it lets
the whole canonical docs/105 converter stay byte-for-byte verbatim in N+3 while the
new scanner lives in the 649 free N+2 words. N+2 code execution was proven by the
C-oracle MTR experiment (`MTR 22147L uj 30114`) and by the final SIMH A/B/C/X runs.
If N+2 code were forbidden, the same 204 halfwords (102 words) would have to be
carved out of the 18 free N+3 words, which is impossible without replacing the
proven converter.

### 4.2 Exact missing primitives (not implemented)

1. **EOF-driven / general loop termination.** The contour processes exactly two
   records (two unrolled scan+process blocks). The `0xff` at `0o64027` is not
   tested, and no `VLM`-style counter drives the loop (short conditional branches
   cannot reach N+3/N+2 code without the M[7] base trick, which is used here only
   for `UZA`/`UJ`).
2. **Other IR record kinds.** `777001..777004` (rule dispatch, per-character
   tables, 777003 loop bounds, 777004 labels) and the absent `777010/777011`
   emitters (docs/104 §3, docs/77) are not parsed.
3. **General VIDX→TEXT-name exception table.** The expected name code is computed
   as `VIDX+28`, the general FRONT rule (`CH = VIDX+60`, code `= CH-0x20`). FRONT
   special-cases X=1, Y=2, N=3, I=4 (docs/109 §1); those four would need a small
   exception table on machine. Our tested VIDX 12/13 use the general rule; VIDX 13
   ('I') is synthetic because real FRONT maps I to 4.
4. **Runtime IR semantics.** Values are seeded in N+2; no operator evaluation or
   assignment is performed.
5. **Sign from IR.** The inherited sign block always produces a minus for positive
   floats (as in docs/105); no per-record sign field is decoded.
6. **FRONT build integration.** The two record cards were authored as deck text
   (layout verified by CORE against docs/104/109 byte positions); no BUILD-time
   FRONT emission of a two-record program was run here.

---

## 5. PASS / FAIL

| # | gate | verdict |
|:--|:--|:--|
| 1 | exact two-record card-buffer layout, CORE evidence + FACT/INFERENCE | **PASS** |
| 2 | scanner walks card buffer, decodes TK/TA of 2 records | **PASS** |
| 3 | two records of different types processed (LIT + VARIABLE) | **PASS** |
| 4 | two-digit VIDX 10..30 decoded on machine (12, 13 exercised) | **PASS** |
| 5 | on-machine 6-bit TEXT-name compare + mismatch signal | **PASS** |
| 6 | N+3 code 40/58 words; N+2 161/649, overlay untouched | **PASS** |
| 7 | SIMH A: both values `0012.34` + `0056.78`, КОНЕЦ ЗАДАЧИ | **PASS** |
| 8 | SIMH X: byte-identical image, deck VIDX 12→13 → `0090.12` | **PASS** |
| 9 | SIMH B: one machine-word value patch → `0099.99` | **PASS** |
| 10 | SIMH C: byte-identical restore → `0056.78` | **PASS** |
| 11 | C-oracle MTR/CORE agree with SIMH; name-mismatch control | **PASS** |
| 12 | EOF-driven loop / `777001..777004` / `777010..777011` | **FAIL** (out of scope; §4.2) |
| 13 | real FRONT BUILD emitting two IR records / runtime IR semantics | **FAIL** (§4.2) |

---

## 6. Reuse (hard rule: reuse, do not reinvent)

| component | proven source | how reused |
|:--|:--|:--|
| canonical image + zone writer/checksum | `tools/build_zone2350_contour.py`, docs/87/105 | imported read-only; reproduction unchanged |
| 4-digit LIT read, `NEG31`/`10*T[]`/`e+x`/`*100` | docs/104, `ir4_build.Stream.ir_read4` | verbatim chain, re-addressed via M[10] |
| VIDX decode + N+2 symbol table | docs/109, `c2_build.VStream.deck_read` | verbatim byte shifts and `32+VIDX` layout |
| ABS+2+2 GOST, sign block, both reclaims, `floor_int`, `*64 2004` | docs/105 `final_sign.py` | verbatim in N+3, wrapped as a VJM subroutine |
| N+2 RAM base / 649 free words / `UTC 20000` reach | docs/110, C1 report | verbatim, including the 526..900 exclusion |
| FRX5 catalog rename + 6-char `*NAME` | docs/108, `rename_catalog.py` | repo tool reused unchanged |
| SIMH ini/destination driver, C-oracle wrapper | docs/100/104/109 | copied, only workspace paths adapted |

New lines are confined to `build/c2b_build.py` (scanner/dispatch/readers, name
compare, GOST seed resets, two-call orchestration) and the gate/probe scripts.
No emulator mechanism, no repository edit, no C patch.

---

## 7. FACT / INFERENCE summary

**FACT:** card-buffer addresses and RLE bytes above; marker word and TK/TA byte
positions; VIDX digits at `W+2` bytes 2/3; `0xff` last non-pad byte; `0` changed words
in N+2 offsets 526..900; 40/58 N+3 words and 204 halfwords of N+2 code; all SIMH
lines and byte diffs; all four SIMH jobs reached `КОНЕЦ ЗАДАЧИ`; A and C byte-identical;
the name-mismatch oracle prints `0000.00`.

**INFERENCE / not proven:** the general "contiguous RLE cards on word boundaries"
rule from only two examples; `0xff` = EOF sentinel (docs/20); N+2 code execution
is proven on this image but is a new architectural use (docs/110 only proved data
read/write); VIDX values other than 12/13; the `VIDX+28` name rule for the four
FRONT special letters; a third or later IR record.

---

## 8. Evidence index / SHAs (SHA-256)

Full list in `logs/sha256.txt`; key artifacts:

```
464e613c4a1b570f4426aa5a10387bb210dc48eea726ec9b6080fbed88cf3a4a  images/2048_SCAN_FRX5_A
39bf08ef59d44678f01c054a4dd9bd7cde12be14d7941275d3122fe867a30558  images/2048_SCAN_FRX5_B
464e613c4a1b570f4426aa5a10387bb210dc48eea726ec9b6080fbed88cf3a4a  images/2048_SCAN_FRX5_C
d8b3b12cec7819f2949b5b8c18a103ef5b10365ffb234c6150318fff0fe7240d  decks/deck_frx5_A.b6
232c5620aa06fa0233f366ef153d98dd96a3b45b77d66a914aed698f011d6bfb  decks/deck_frx5_V13.b6
ffdc03c3e613938ddcfb5459475841092e38d5d698c3cdeee72f650ac88a19ee  runs/localprn_C2B_A.txt
f550556069b84c4affeef8760fa1ebb0d646f740b2b7a6b1ff8e864b4fc66121  runs/localprn_C2B_V13.txt
bae534a429ca6cc3ec67d970238ed298cddd1c841de56a08d97cb13a4ecb3652  runs/localprn_C2B_B.txt
542bfa15f698cf1ce36a3b8fac2faaa39acbdf1153b3e3af986cdd1f6eaccc43  runs/localprn_C2B_C.txt
07d4cd81731e21516f464106e1290eadac91ea70d1a122c11ca30843710532de  oracle/C2B_A/out.txt
b1c615f9cd3493aa04c7960c5128c5c24f1bee52964d6803f53809cb0d293609  oracle/C2B_V13/out.txt
46ea71fcdcbb6674b425c7ce33c9dddf2c67d2d56bfdea77f271c9aace425043  oracle/C2B_B/out.txt
63d333121acc50ff13a332424ac0d6f457d00ba9a68746cc6e2cebeb1f8db5c5  oracle/TWO_DUMP/core-pc.bin
35038e308297147ac764d07e12482f90cd0c78e99b930bc6783baf22f1f3677e  logs/MTR_c2b_scanner.txt
8f01c380fdb2467cc3db52dde0079c346a427e7c99c5d926cacfa8263d4e15da  build/c2b_build.py
```

Artifacts: `build/c2b_build.py`, `build/make_gates_c2b.py`, `build/oracle_run.py`,
`build/drive_c2.py`, `build/setup_c2.py`; `decks/deck_{two_records,scan_A,frx5_A,frx5_V13}.b6`;
`images/2048_SCAN_{A,FRX5_A,FRX5_B,FRX5_C,FRX5_NAMEMISMATCH}`;
`runs/localprn_C2B_*.txt`, `runs/console_C2B_*.txt`, `runs/ini_C2B_*.ini`;
`oracle/C2B_*`, `oracle/TWO_DUMP/`; `logs/{card_buffer_two_records,MTR_c2b_scanner,
byte_diffs,sha256}.txt`.

DONE
