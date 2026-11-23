# B4 — MACHINE-CODE EXPRESSION PARSER WITH PRECEDENCE (shunting-yard)

> РЕЗУЛЬТАТ B4: **PASS** — machine‑парсер выражений с приоритетом.
> Два стека (shunting‑yard), `* /` старше `+ -`, скобки, FPU, печать через
> неизменный GOST. SIMH A/B/PATCH/RESTORE/PARENS: `11.50 / 6.50 / 12.50 /
> 11.50 / 16.00` — все machine‑вычислены, все `КОНЕЦ ЗАДАЧИ`.
> Бюджет 40/58 N+3, 464/649 N+2, keeper и зона 526..900 не тронуты.
> ВАЖНО: пока исполняется fixture токенов в N+2, а не Fortran из дека;
> сквозной прогон B1→B4 следующий шаг.

> СТАТУС: PASS (prototype milestone, not Variant-B acceptance).
> Two-stack shunting-yard evaluator reads B2-layout token words pre-seeded in
> zone N+2, evaluates `+ - * /` with `* /` over `+ -` precedence and left
> associativity (plus parentheses), using the proven FPU ops, and feeds the
> verbatim docs/105 GOST converter in N+3.  Full SIMH A/B/PATCH/RESTORE/PARENS
> gate: every job prints a distinct machine-computed `21` value and reaches
> `КОНЕЦ ЗАДАЧИ`; C dispak (oracle only) reproduces every value.
>
> **MILESTONE LABEL — read this first.** The program executed at this milestone
> is the **pre-seeded token fixture in N+2**, NOT Fortran source.  The deck
> (`decks/deck_fixture.b6`, byte-identical in every gate) carries a
> Fortran-looking body that our code never reads; it is only the loader
> trigger.  B1 will later replace the N+2 fixture with tokens emitted from real
> fixed-form Fortran text (contract in §6).

Discipline (FACT): workspace `/tmp/.private/azizz/opencode/b4-precedence/`
only.  Copies only — no repository edit, no live disk, no tmux session 0, no
SIMH binary or C `dispak` source change.  C `dispak` was oracle only
(MTR/CORE hooks).  All authoritative A/B/A verdicts are full SIMH printer
captures.  Emulator `/home/azizz/Yandex.Disk/simh/BIN/besm6`, SHA-256
`9ef71b260e8a780d12fa63c152c5979dd8dc50e8959a57849bd73fb5252a8254`.
Deck SHA-256 `4618a7eef292fcb509096c520b142ef29fbe3191965a6dcfff748269b07af703`
(invariant across all gates).

---

## 1. VERDICT

**PASS.**  B2 one-word tokens (`TK<<42 | SUB<<36 | POS<<24 | PAY`) are fetched
from N+2, dispatched, and evaluated on two stacks (operand = BESM floats,
operator = SUB codes) with immediate evaluation.  Decisive SIMH result (deck
invariant, image changed by one word at a time):

| gate | image SHA-256 (prefix) | change vs A | printer `21` line | КОНЕЦ | verdict |
|:--|:--|:--|:--|:--|:--|
| A | `c2ff8f44…` | baseline | `-0011.50` | yes | PASS |
| B | `6f5a7c84…` | **one token word** (LIT PAY 2→3, N+2 off 75) | `-0006.50` | yes | PASS |
| PATCH | `06cdf77c…` | **one parser word** (K_PATCH 0→f32(10), N+2 off 151) | `-0012.50` | yes | PASS |
| RESTORE | `c2ff8f44…` | byte-identical to A | `-0011.50` | yes | PASS |
| PARENS (retry) | `f15be8da…` | token fixture: `(1.5+2.5)*4.0` | `-0016.00` | yes | PASS |

(Full SHA-256 values in `evidence/n2_bytediff.json`; per-gate printer/ACPU SHAs
in `evidence/raw_printer_completion.txt`.  Structured SIMH verdict:
`evidence/gates_b4.json` / `evidence/gates_b4_invariants.json`, all invariants
True after the retry.)  The first SIMH PARENS run hit a transient harness
glitch (pre-deck `НОМВ` returned `HET`, no job started, drive `rc=2`, empty
printer); the image was unchanged and an isolated rerun on the identical image
printed `-0016.00` and reached `КОНЕЦ ЗАДАЧИ` (`rc=0`).  The C oracle had
already printed `-0016.00` for that image with `rc=0`.

The `-` sign is the verbatim converter's proven sign-byte convention for a
positive EST (docs/105; docs/119 gate A printed `-0012.34` for a positive
literal).  Interpreted values: A `11.50`, B `6.50`, PATCH `12.50`, PARENS
`16.00`.  A vs naive left-to-right `(1.5+2.5)*4 = 16` proves precedence;
PARENS proves parentheses override it; B proves a single token digit changes
the machine-computed result; PATCH proves a single word of OUR parser changes
it; RESTORE proves byte-identical return.

---

## 2. What was implemented

Reused verbatim from the proven B3 dispatcher (`dispatch_build.py`): the
statement loop, `PROGRAM`/`REAL`/`PRINT`(restricted `Fw.d`)/`END`, the B2 token
fetch + `aax`/`asx` field extraction, the docs/105 converter as a VJM
subroutine in N+3, and the docs/113 width masks.  Only the assignment handler
was replaced by the shunting-yard evaluator (§3).  This is the reuse-hard-rule
path: no parallel print/converter/dispatch mechanism was written.

### 2.1 Token fixture (executed program at this milestone)

Expression fixture for `X = 1.5 + 2.5 * 4.0` (18 tokens at N+2 offsets 64..81):

| idx | RAM | TK | SUB | PAY | meaning |
|--:|:--|--:|--:|--:|:--|
| 64 | 021737 | 10 | 30 | 0 | `PROGRAM` |
| 65 | 021740 | 2 | 0 | 0 | name (consumed) |
| 66 | 021741 | 10 | 31 | 0 | `REAL` |
| 67 | 021742 | 2 | 0 | 1 | `X` (VIDX=1) |
| 68 | 021743 | 11 | 0 | 0 | EOL |
| 69 | 021744 | 2 | 0 | 1 | `X` = |
| 70 | 021745 | 8 | 0 | 0 | `=` |
| 71 | 021746 | 1 | 0 | 0 | LIT pool 0 = 1.5 |
| 72 | 021747 | 3 | 1 | 0 | OP `+` |
| 73 | 021750 | 1 | 0 | 1 | LIT pool 1 = 2.5 |
| 74 | 021751 | 3 | 3 | 0 | OP `*` |
| 75 | 021752 | 1 | 0 | 2 (B: 3) | LIT pool 2 = 4.0 (B: pool 3 = 2.0) |
| 76 | 021753 | 11 | 0 | 0 | EOL (end of expression) |
| 77 | 021754 | 10 | 34 | 0 | `PRINT` |
| 78 | 021755 | 13 | 1 | 1026 | `F4.2` (`4<<8\|2`) |
| 79 | 021756 | 2 | 0 | 1 | `X` |
| 80 | 021757 | 11 | 0 | 0 | EOL |
| 81 | 021760 | 10 | 37 | 0 | `END` |

Literal pool = N+2 offsets 100..103: `f32(1.5), f32(2.5), f32(4.0), f32(2.0)` —
**actual** float values (unlike B3's pre-scaled 10× pool); the evaluator scales
the final result by 10 before storing it to the symbol value word, because the
verbatim converter divides EST by 10.  No result digit is stored anywhere.

### 2.2 Shunting-yard (two-stack, immediate evaluation)

* `OSTK` = N+2 offsets 200..229 (BESM floats); `OPR` = 230..244 (SUB codes,
  marker `0` = `(`).  Stack pointers `C_SPO`/`C_SPP` at N+2 146/147.
* Precedence: `+ -` = 1, `* /` = 2, `(` = 0 (marker, never popped by
  precedence).  Left associativity: on an incoming OP, pop/apply every
  top-of-OPR operator with precedence `>=` incoming, stopping at `(` or empty.
* On `)` pop/apply to the marker and discard it; at EOL flush all operators;
  the single remaining operand is the result.
* Apply dispatching (`EV_APPLY`): pop `b` then `a`, dispatch on SUB:
  1 `a+x`, 2 `a-x`, 3 `a*x`, 4 `a/x` (FPU opcodes from docs/95), push result.

**BESM one's-complement engineering (FACT from MTR, not inference).**  In this
ISA `1 + (-1) = -0` (all ones) and `UZA` does NOT branch on `-0`; an unbiased
stack pointer wrapping below zero therefore never tests empty.  Fix: SP is
biased by `K_BIAS = 100` (empty = 100), so `SP-1` is always a positive index;
the array base ADR absorbs the bias (`0o1637 + base - 100`).  Also `ATI`
overwrites the accumulator, so every push saves its value to a scratch cell
before loading the index register.

### 2.3 Result -> verbatim print path

At EOL/final result: `ACC = result`; `ACC *= f32(10)` (`K_TEN`, N+2 150);
`ACC += K_PATCH` (N+2 151, default `0`, the one-word PATCH target); store to
symbol value word `N+2[32+VIDX]`.  The B3 `PRINT` handler then reads that word
into EST, seeds GOST words, applies the docs/113 width masks, and calls the
verbatim converter via VJM (`mtr_b4_a_parser_curated.txt` shows `a*x 2065`
= K_TEN, `a+x 2066` = K_PATCH at 0o22550/0o22551).

---

## 3. Word budget (exact, measured from the build)

| region | used | limit | note |
|:--|--:|--:|:--|
| N+3 hot path | **40 words** | 58 | verbatim docs/105 converter: 74 converter halfwords + 6 floor halfwords; unchanged from C7/B3 |
| N+2 interpreter code | 203 words (406 halfwords) | — | offsets 260..462, entry RAM `0o22243` |
| N+2 whole footprint | **464 / 649 words** | 649 | symbol table + 18 tokens + 4 literals + constants + 2 stacks + code |
| N+2 forbidden band 526..900 | **0 writes** | 0 | verified by `rz()`/`wz()` round-trip and `evidence/n2_bytediff.json` |
| body N+1 words touched | **35 words** | 999 (with `body[0o26]` keeper) | entry `body[0o11]` + GOST seeds `body[0o27..0o32]` + 30 converter data cells `body[0o110..0o135]`; keeper `body[0o26]` untouched |

No overrun; no N+4 word, no new opcode, no MMU trick beyond the proven
`UTC 20000`/M20.  The 909-word five-range free reservoir of docs/120 was not
needed for this milestone (all interpreter code/data fit in N+2).

---

## 4. PASS/FAIL and raw evidence

All five gates PASS on both SIMH (authoritative) and C oracle.  Raw captures:

* SIMH structured verdict: `evidence/gates_b4.json`,
  `evidence/gates_b4_invariants.json` (all invariants True).
* SIMH printer `21` lines + completion + capture SHAs:
  `evidence/raw_printer_completion.txt`.
* SIMH raw ACPU captures: `runs/acpu_B4_{A,B,PATCH,RESTORE,PARENS_RETRY}.txt`
  (per-gate driver logs `runs/drive_B4_*.log`, console `runs/console_B4_*.txt`,
  printer `runs/localprn_B4_*.txt`).
* C-oracle printed values + SHAs: `evidence/c_oracle_summary.txt` (all `rc 0`).
* C-oracle MTR at our parser PCs: `evidence/mtr_b4_a_parser_curated.txt`
  (entry `0o22243`, token fetch `0o21737`, B2 field extraction, FPU apply
  `a*x 2057` / `a+x 2057`, scaling `a*x 2065`, patch `a+x 2066`, converter
  at `0o30114`).
* N+2 word-level byte diff: `evidence/n2_bytediff.json`:
  A vs B = **1 word** (offset 75); A vs PATCH = **1 word** (offset 151);
  A vs RESTORE = **0 words**; forbidden band unchanged = True.

Byte-diff proof of byte-identical contour: A and B differ in exactly one
N+2 token word and in no other word; RESTORE is byte-identical to A; the deck
and emulator are byte-identical across all gates.

---

## 5. Honest subset / deferred

Implemented: precedence `* /` over `+ -`, left associativity, parentheses,
binary `+ - * /`, real literals and variables (from the symbol table), the
B3 statement subset, restricted `F4.2` print via the verbatim converter.

Deferred or blocked (not achieved here):
* **Fortran source lexing is not implemented** — the deck still holds token
  fixtures; B1 supplies the lexer (§6).
* **Unary minus** (TK=4) and **intrinsics in expressions** (TK=5 ABS/SQRT/MOD):
  token kinds are defined by B2 but not wired into the evaluator.
* **Division by zero, exponentiation, string/boolean ops**: unsupported.
* **Full `Fw.d` semantics**: only `w∈{2,3,4}, d∈{1,2}`, no rounding/E/I/G.
* **`DO`/`CONTINUE`, labeled `FORMAT`, multiple print records, EOF-driven
  statement loop**: B5 scope.
* **DSQRT / double precision** and **formatted READ(u,fmt)**: hard blocked per
  docs/117 §5.3 (no double FPU; monitor-owned input context).
* Negative computed results: the sign block is the verbatim docs/105 path; its
  correctness for a *computed* negative float is a validation gate (docs/117
  §5.3 item 8), not claimed here.

---

## 6. Integration contract for B1 (expression tokens)

B1 must emit, into N+2 token buffer offset `64+i`, one B2 word per token,
`(TK<<42)|(SUB<<36)|(POS<<24)|PAY`, with these exact codes:

1. **Assignment** `V = <expr>`:
   - `ID` (TK=2, PAY=VIDX 1..30) for `V`;
   - `EQ` (TK=8, PAY=0);
   - expression tokens in source order (below);
   - `EOL` (TK=11, PAY=0) terminating the statement.
2. **Expression tokens**:
   - real literal `LIT` (TK=1, PAY = pool index 0..19).  Pool word at N+2
     `100+PAY` must be the **actual** BESM float value (not 10× scaled); the
     evaluator multiplies the final result by 10 itself.
   - variable `ID` (TK=2, PAY=VIDX); its value word at N+2 `32+VIDX`.
   - binary operator `OP` (TK=3, SUB: 1 `+`, 2 `-`, 3 `*`, 4 `/`).
   - parentheses `LP` (TK=6, SUB=1) and `RP` (TK=6, SUB=2).  NOTE: both share
     TK=6 and are distinguished by SUB; B1 must set SUB correctly.
   - `POS` (b35..b24) is laid out but not consumed by B4.
3. **Print** `PRINT` (TK=10, SUB=34), `FD` (TK=13, SUB=1, PAY=`w<<8|d`, w∈{2,3,4},
   d∈{1,2}), `ID` (TK=2, PAY=VIDX), `EOL`; then `END` (TK=10, SUB=37).
4. **Symbol table**: B1 installs the 6-bit TEXT name word at N+2 offset VIDX
   (ASCII-0x20, 8 codes/word, space-padded); the evaluator stores results to
   N+2 `32+VIDX` (B3's `REAL` seeds that word to 0.0).
5. **No result digit is emitted by the host** — only source symbols and pool
   indices.  Every numeric value is built or computed by BESM-6 instructions.

---

## 7. FACT vs INFERENCE

FACT (cited/measured): B2 token layout and extraction masks (docs/117, docs/119);
N+2 free map and forbidden band (docs/110); N+3 40-word converter + GOST/sign
(docs/105, docs/116); FPU opcodes (docs/95); body free reservoir and
`body[0o26]` keeper caveat (docs/120); one's-complement `-0`/UZA and ATI
behaviour (C-oracle MTR, this run); all SHAs, word counts, byte diffs, and
A/B/PATCH/RESTORE/PARENS verdicts (SIMH + C oracle, this run).

INFERENCE / design: the precise N+2 allocation (§3) is a build choice; the
100-biased SP and scratch-cell workaround are local engineering choices that
reproduce correctly on both emulators; the `w/d` mask composition and sign
convention are inherited from B3 (proven there); interpretation of the `-`
sign is inherited from docs/119.  No new architectural claim is made beyond
the measured gate results.

---

DONE
