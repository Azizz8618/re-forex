# B3 — STATEMENT DISPATCHER (prototype, parallel to B1 lexer)

> СТАТУС: **PASS** (прототип, не приёмка варианта Б). Dispatcher на machine‑коде
> читает токены B2 из N+2 и исполняет PROGRAM/REAL/NAME=NUMBER/PRINT/END,
> печатая через неизменный GOST‑конвертер. SIMH A/B/PATCH/RESTORE/ORDER PASS,
> все `КОНЕЦ ЗАДАЧИ`; N+3 40/58, N+2 256/649, 526..900 не тронуты.
> ВАЖНО: исполняется пока **fixture токенов в N+2**, а не Fortran из дека;
> тело дека — только триггер загрузки. Интеграционный риск: B1 пока выдаёт
> 2‑словный токен, нужно привести к одному слову B2 перед подключением.

## VERDICT: PASS

A machine-code statement dispatcher reads **B2-layout token words pre-seeded in
zone N+2** and executes `PROGRAM` (consume), `REAL` (seed value words to 0.0),
`NAME=NUMBER` (literal-pool float into the symbol table), and `PRINT` with a
restricted `Fw.d` width, feeding the value into the verbatim docs/105 GOST
converter in N+3. Full SIMH A/B/PATCH/RESTORE/ORDER pass; all five jobs reach
`КОНЕЦ ЗАДАЧИ`; C dispak (oracle only) reproduces every printed value and shows
the dispatcher executing at our N+2 addresses. Budgets: **N+3 = 40/58 words,
N+2 = 256/649 words, zero writes to offsets 526..900**.

**MILESTONE LABEL — read this first.** The program actually executed at this
milestone is the **pre-seeded token fixture in N+2**, *not* Fortran source. The
deck (`decks/deck_fixture.b6`, byte-identical in every gate) carries a
Fortran-looking body (`PROGRAM MAIN / X=12.34 / END`) that our dispatcher never
reads; it is only a loader trigger. B1 will later replace the N+2 fixture with
tokens emitted from real fixed-form Fortran text. No Fortran parsing exists in
B3.

Copies only: no repository edit, no live/tmux-0/C patch. C `dispak` was oracle
only (MTR/CORE hooks); all authoritative A/B/A results are full SIMH printer
captures. Emulator `/home/azizz/Yandex.Disk/simh/BIN/besm6`, SHA-256 prefix
`9ef71b26` (verified by the driver each run).

---

## 1. Token fixture layout (exact, B2 §2.1)

One token = one 48-bit word: `word = (TK<<42) | (SUB<<36) | (POS<<24) | PAY`.
TK=6 bits (b47..42), SUB=6 (b41..36), POS=12 (b35..24), PAY=24 (b23..0).
Extraction in the dispatcher is exactly the B2 `aax`/`asx` chain with masks
`0o7700000000000000` (TK, SR42), `0o0077000000000000` (SUB, SR36),
`0o0000000077777777` (PAY); POS is laid out but not consumed by B3.

Token buffer = N+2 offsets **64..95**, RAM `0o21737 + i`, one word per token.
Image A fixture, dumped from the disk (RAM / word / decoded fields):

| idx | RAM | TK | SUB | POS | PAY | word (octal) | meaning |
|--:|:--|--:|--:|--:|--:|:--|:--|
| 64 | 021737 | 10 | 30 | 0 | 0 | 1236000000000000 | `PROGRAM` |
| 65 | 021740 | 2 | 0 | 0 | 0 | 0200000000000000 | name (consumed, ignored) |
| 66 | 021741 | 10 | 31 | 0 | 0 | 1237000000000000 | `REAL` |
| 67 | 021742 | 2 | 0 | 0 | 1 | 0200000000000001 | ID X (VIDX=1) |
| 68 | 021743 | 11 | 0 | 0 | 0 | 1300000000000000 | EOL |
| 69 | 021744 | 2 | 0 | 0 | 1 | 0200000000000001 | ID X = |
| 70 | 021745 | 8 | 0 | 0 | 0 | 1000000000000000 | `=` |
| 71 | 021746 | 1 | 0 | 0 | 0 | 0100000000000000 | LIT index 0 (A) / 1 (B) |
| 72 | 021747 | 11 | 0 | 0 | 0 | 1300000000000000 | EOL |
| 73 | 021750 | 10 | 34 | 0 | 0 | 1242000000000000 | `PRINT` |
| 74 | 021751 | 13 | 1 | 0 | 1026 | 1501000000002002 | F descriptor, PAY = `4<<8|2` (F4.2) |
| 75 | 021752 | 2 | 0 | 0 | 1 | 0200000000000001 | ID X |
| 76 | 021753 | 11 | 0 | 0 | 0 | 1300000000000000 | EOL |
| 77 | 021754 | 10 | 37 | 0 | 0 | 1245000000000000 | `END` |

Literal pool = N+2 offsets 100..103 (RAM `0o21703..`), each word a BESM float
equal to **10 × printed value** (the verbatim converter divides EST by 10):
`float(123.4)`, `float(567.8)`, `float(345.0)`, `float(901.0)`. The LIT token's
PAY selects the index; no host-computed result digit is stored anywhere.

Symbol table reuses the proven docs/109/114 layout: name word at N+2 offset
`VIDX`, value word at `32+VIDX`. X = VIDX 1: name at offset 1
(`0o0700000000000000`), value at offset 33.

N+2 constant cells: 104..112 (work), 113..134 (masks/shifts/KW codes/GOST
seeds/**K_PRINT_BIAS**), 135..137 (w masks), 138..139 (d clear), 140..141 (d
space). Dispatcher code = offsets **150..254** (105 words, entry RAM
`0o22065`); entry substitution `body[0o11] = LONG UJ 0o22065`.

---

## 2. Decisive SIMH A/B/PATCH/RESTORE/ORDER

One invariant deck (`decks/deck_fixture.b6`); only the image changes.

| gate | image SHA-256 | change vs A | printer `21` line | КОНЕЦ | verdict |
|:--|:--|:--|:--|:--|:--|
| A | `6421e501219a10d0…` | baseline | `21 -0012.34  3000.00` | yes | PASS |
| B | `e44eb5ca78f9ca49…` | **one token word**: LIT PAY 0→1 at N+2 off 71 / RAM `0o21746` | `21 -0056.78  3000.00` | yes | PASS |
| PATCH | `a40983c5ed7945ab…` | **one dispatcher word**: K_PRINT_BIAS `0`→`float(10.0)` at N+2 off 134 / RAM `0o22045` | `21 -0013.34  3000.00` | yes | PASS |
| RESTORE | `6421e501219a10d0…` | byte-identical to A | `21 -0012.34  3000.00` | yes | PASS |
| ORDER | `249e027a2fe557fb…` | token order: PRINT moved before REAL/assignment (12 token words changed) | `21  0000.00  3000.00` | yes | PASS |

Byte-diff verification (`evidence/`-grade, whole disk images, N+2 words):
RESTORE vs A = **0** differing words; B vs A = **1** word (the token LIT PAY);
PATCH vs A = **1** word (the dispatcher bias constant). A vs B image SHA differs
while every other N+2 word is identical. All invariants in
`evidence/gates_b3_invariants.json` = True. Machine-derived values only: the
printed digits come from the BESM FPU + verbatim GOST converter, never from the
host.

### Raw evidence
* per-gate structured results: `evidence/gates_b3.json`,
  `evidence/gates_b3_invariants.json`
* authoritative printer `21` lines + `КОНЕЦ ЗАДАЧИ`, with capture SHAs:
  `evidence/raw_printer_completion.txt`
* full `runs/localprn_B3_{A,B,PATCH,RESTORE,ORDER}.txt` (prn0),
  `runs/console_B3_*.txt`, `runs/acpu_B3_*.txt`, `runs/drive_B3_*.log`
* C-oracle printed values: A `-0012.34`, B `-0056.78`, PATCH `-0013.34`
  (`oracle/B3_ORA_{A,B,PATCH}/out.txt`, grep `^  21`); all `rc 0`
* C-oracle MTR excerpt at our dispatcher PCs: `evidence/mtr_b3_a_dispatcher.txt`
  (423 lines in MTR window `022000..023000`, e.g.
  `MTR 22065L xta 2105(0)` / `MTR 22065R ati 14(0)` = rearm M[12],
  `MTR 22070L utc 20000` + `MTR 22070R xta 21737(6)` = B2 token fetch at
  RAM `0o21737`, `MTR 22071L atx 2007(14)` = save token, followed by
  `aax 2022(14)` / `asx 2025(14)` / `atx 2010(14)` = TK field extraction).
  CORE dump taken at PC `01770` (`oracle/B3_ORA_A/core-pc.bin`, 393216 bytes =
  65536×6).

---

## 3. Word budget

| region | used | limit | note |
|:--|--:|--:|:--|
| N+3 (hot path) | **40 words** (74 converter hw + 6 floor hw) | 58 | verbatim docs/105 converter, unchanged from C7 |
| N+2 dispatcher code | 105 words (210 halfwords) | 649 total | offsets 150..254 |
| N+2 whole footprint | **256 words** | 649 | symbol table + 14 tokens + 4 literals + constants + code |
| N+2 forbidden band 526..900 | **0 writes** | 0 | preserved by `rz()`/`wz()` round-trip |

No overrun. Full `Fw.d` semantics were the only budget risk; they are handled
as an honest subset below, not by exceeding the ceiling.

---

## 4. Honest subset / what B3 does not do

* **PRINT width**: implemented for `w∈{2,3,4}, d∈{1,2}` using the proven docs/113
  masks (GOST A leading-zero XOR, GOST B clear/space ADD). Only F descriptors
  (`SUB=1`). No rounding, no `w>4`, no E/I/G editors, no arbitrary exponent or
  justification. This is the B2 §5.3 item-7 deferral, not an N+3 overrun.
* **`REAL`**: seeds the value word to 0.0 for each ID token until EOL. The
  6-bit TEXT **name word is fixture-seeded** (X at offset 1); B3 does not build
  it from ASCII. B1 must install name words (contract below).
* **assignment**: `NAME=NUMBER` only (ID, `=`, LIT). The B2 §3 shunting-yard
  expression evaluator (precedence, parentheses, intrinsics) is B2/B4 scope and
  is not implemented here; POS is ignored.
* **`PROGRAM`** consumes the following name token with no semantics. **`END`**
  returns via `LONG UJ 0(15)` to resident `0o1764`.
* **`DO`/`CONTINUE`**, labeled `FORMAT` lookup, `STOP`, multiple print records,
  and EOF-driven re-entry after `END` are deferred to B4/B5 per the B2 stage
  plan. `PROGRAM/REAL/=/PRINT/FORMAT/DO/CONTINUE/END` is the B2 target set; B3
  delivers its minimum (`REAL`, `=`, `PRINT`, `END`, plus `PROGRAM`).
* **`K_PRINT_BIAS`** is a deliberate dispatcher display-offset constant used as
  the one-word patch target; default 0. It is a mechanism/argument word, not a
  source-level Fortran feature.

---

## 5. Integration contract with B1 (what B1 must emit)

1. **Token form**: emit exactly the B2 §2.1 48-bit word
   `(TK<<42)|(SUB<<36)|(POS<<24)|PAY` into N+2 offset `64+i`, one word per
   token, with the TK/SUB codes of B2 Table 2.2 (used here: 1 LIT, 2 ID, 8 EQ,
   10 KW, 11 EOL, 12 EOF, 13 FDESC; KW SUB 30/31/34/37; FD SUB=1,
   PAY=`w<<8|d`). B3 reads POS-layout but does not depend on it.
2. **Statement shapes** B3 accepts (tokens in order, each terminated by EOL):
   `KW(30), ID(name)`; `KW(31), ID..., EOL`; `ID, EQ, LIT, EOL`;
   `KW(34), FD, ID, EOL`; `KW(37)`. EOL tokens may be emitted by B3's main loop
   as no-ops if B1 omits them between statements, but the declared-ID loop and
   the PRINT handler consume one EOL each.
3. **Symbol table**: B1 must install the 6-bit TEXT name word at N+2 offset
   `VIDX` (ASCII-0x20, 8 codes/word, space-padded). B3's `REAL` only zeroes
   N+2[`32+VIDX`]; the value word is a BESM float = 10 × printed value.
4. **Literator**: B1's literal token PAY must be an index into the literal pool
   at N+2 offsets 100..103, each pool word a BESM float = 10 × the printed
   value. B3 adds no scaling; the docs/105 converter divides by 10.
5. **Re-arm**: B3 re-loads M[12] and M[7] from low-RAM HALF after every
   converter call; B1 need not preserve base registers across a VJM.
6. **OPEN INTEGRATION RISK**: the current parallel B1 prototype
   (`b1-lexer/build/lexer_build.py:16-20,192-216`) emits a **different, 2-word
   token format** (word A = KIND/LEN, word B = ASCII payload) into N+2 offset
   200. That format is not the B2 layout used here. Before B1 plugs in, B1 must
   either adopt the B2 one-word layout of §1 or supply a translation step into
   N+2[64+i]; B3 will not be changed to read the 2-word format. This was not
   patched here (parallel scopes) and is the single item requiring joint
   freeze.

All numeric values were built or computed by BESM-6 instructions; no
host-computed result digit appears in any fixture or report value.

DONE
