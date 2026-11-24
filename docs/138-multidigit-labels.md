# B9: multi-digit F77 statement labels in GOTO / IF / FORMAT, and a CALL/COMMON binding attempt

> РЕЗУЛЬТАТ: Task 1 **PASS** под SIMH (13/13) — 1–3‑значные метки в GOTO/IF/FORMAT,
> образ `81d7790f…`: `GOTO 100→21 -0012.34`, `GOTO 200→-0056.78` при байтово том же
> образе; PATCH/RESTORE, T1/T5/B7 без регрессии. Task 2 (CALL/SUBROUTINE)
> **BLOCKED**: `SUBR`‑окно не совпадает, `BW_NSUB=0`, PAY CALL не резолвится,
> `КОНТРОЛЬ КОМАНДЫ`. Причина — состояние ячеек в body gap `0o670..0o677`
> и N+2 `153..155`; нужен marker sweep по docs/120.

## 0. Verdict

* **Task 1 (multi-digit labels): PASS, authoritative full-SIMH.** A byte-identical image prints
  `21 -0012.34` for `GOTO 100` and `21 -0056.78` for `GOTO 200`; a one-machine-word PATCH of
  OUR threshold flips `IF (1.0) 200,200,100` from `12.34` to `56.78`; byte-identical RESTORE
  returns it. T1/T5, B7 A/B and backward compatibility all reach `КОНЕЦ ЗАДАЧИ`.
* **Task 2 (CALL/SUBROUTINE name binding): BLOCKED at runtime**, with an exact failure chain
  and word-budget headroom explicitly shown below. The build assembles and fits, but the
  SUBROUTINE keyword window never matches on the C oracle, so no name is bound and B4 dies with
  `КОНТРОЛЬ КОМАНДЫ`. No CALL is faked with a host/compiler.

Discipline: workspace `/tmp/.private/azizz/opencode/b9-labels/` only; copies of every builder,
deck, image and harness. No repository file, live disk, tmux session 0, SIMH binary or C
`dispak` source was modified. C `dispak` was used only as an advisory oracle (MTR/CORE); every
product verdict below is an isolated full-SIMH `prn0` capture.

SIMH binary verified on every run:
`d058305796bcd0aaf108056f595ee2a222762abe31cf3bb59f1697c9473ca675`.

## 1. Artifacts (SHA-256)

```
81d7790f7541ebcfee248c5fc5264b74c6b82c942b57d79f5b3e07046cd8eb7acbcc  images/2048_B9_A (A=B=RESTORE)
72800718de9355a81766e8214121aab06d388cf5acd492dfae58e7137e2b9c67      images/2048_B9_PATCH
c073dc2f592fcb549c71a0e5f7c39e7c62baca86333ab3c068c08a473bc080e8      images/2048_B9C_A (CALL attempt, NOT passing)
561a4e0e099403be2543a5815ed5c1334ce6f2d535740329a349f14a7bb2f375      images/2048_B7_A (base control)
4abc1d38696c0f955dad7c58a0090cb2bbf4bb5f8ac6ded70018566dff1cf7da      decks/deck_B9_A.b6 (GOTO 100)
b565498fb6d362c67584d93d34028a2a4799b6f2789f4c61fa9ebd33ef591006      decks/deck_B9_B.b6 (GOTO 200)
94ec164850332b9b903e86b4015fa4ce3a8958ba09eba957d0958cef383cbbc7      decks/deck_B9_IF.b6
48921fd9edcc3fde5e4d3b90d5e73e430f63e55c2ceba955f8390dbbde45bf19      decks/deck_B9_2D.b6
c55ff5abd2b115e9a0b7670d4871b9a8d6102e719ec21ef92ce1817eea8bc204      decks/deck_B9C_CALL.b6
```

Builder: `build/b9_labels_build.py` (derived from `b7_control_build.py`, only the label/Task-1
changes). Harness: copies of `b-final-do/harness/{drive_b,setup_b}.py`.

## 2. Task 1: what changed in the machine contour

All new execution remains in OUR N+1 body RAM / N+2 contour; B4, the docs/105 converter and all
arithmetic are the proven machine code. Four defects/extension points were fixed:

1. **Label pre-scan, 1-3 digits.** RLE space bytes `0x81..0x84` in columns 1-5 introduce a
   4..1 digit label. `LABEL_FOUND` now consumes digits with `GETCH` and accumulates a **BCD**
   label (4 bits/digit, e.g. `100` -> `0x100`) using `ASX` left-shift-4 + `ARX` add. No host
   arithmetic. The label number is stored in the token **POS** field (12 bits, supports 1..999)
   instead of the old 6-bit SUB field, with PAY = token index.
2. **Digit test polarity.** The first build inverted the `UZA after AEX` test in
   `LABEL_DIG_LOOP`; valid digits were rejected and "FORMAT" letters were accumulated as digits
   (C-oracle MTR proved `BW_LBLACC` reaching `0o674550510`). Fixed by branching to an explicit
   accumulation label on `UZA`.
3. **Dense label table + 1-3 digit GOTO/IF references.** `LABTAB` is now a dense
   `(BCD label, token index)` table (32 pairs) with a machine `FIND_LABEL` linear search; GOTO
   accumulates BCD digits to newline, IF accumulates 1..3 digits per comma-separated label.
   `FIND_LABEL` is called with FIXUP entered **inline** from `FOUND_END` (not via `VJM`), because
   nested calls clobber the single link register M[5]; before this fix FIXUP returned into its
   own search loop and the oracle ran away to ~157k tokens.
4. **FORMAT labels.** `PRINT 400,X` / `400 FORMAT(...)` are handled by the existing single-pass
   FDESC mechanism; the numeric label is now also emitted as a LABEL token and therefore
   participates in the same dense table. Single-digit FORMAT labels still work (backward
   compatible).

A critical environment detail: the harness must shift **every** `attach ttyN Line=N,PORT` to
`6300+N` (docs/135/137) and must **not** send an artificial `go` at `>>> MUX: clear` (that nudge
breaks boot; the proven b-final-do harness has none). The workspace also had to use the proven
`2253` md07 system-disk copy; a stock `2253` stalls OS boot at `MUX: clear`.

## 3. Task 1: decisive SIMH gates (prn0, all with `КОНЕЦ ЗАДАЧИ`)

| Gate | image | deck | prn0 `21` line | Verdict |
|:--|:--|:--|:--|:--|
| A | `2048_B9_A` | `deck_B9_A.b6` (`GOTO 100`) | ` 21 -0012.34  3000.00` | PASS |
| B | `2048_B9_A` (byte-identical) | `deck_B9_B.b6` (`GOTO 200`) | ` 21 -0056.78  3000.00` | PASS |
| PATCH | `2048_B9_PATCH` | `deck_B9_IF.b6` | ` 21 -0056.78  3000.00` | PASS |
| RESTORE | `2048_B9_A` (byte-identical to A) | `deck_B9_IF.b6` | ` 21 -0012.34  3000.00` | PASS |
| IF 3-digit | `2048_B9_A` | `deck_B9_IF.b6` | ` 21 -0012.34  3000.00` | PASS |
| 2-digit | `2048_B9_A` | `deck_B9_2D.b6` (`GOTO 20`) | ` 21 -0056.78  3000.00` | PASS |
| T1 non-regression | `2048_B9_A` | `T1_lit_A.b6` | ` 21 -0012.34  3000.00` | PASS |
| T5 non-regression | `2048_B9_A` | `T5_do_2.b6` | ` 21 -0040.00  3000.00` | PASS |
| B7 A | `2048_B7_A` | `deck_B7_A.b6` | ` 21 -0012.34  3000.00` | PASS |
| B7 B | `2048_B7_A` | `deck_B7_B.b6` | ` 21 -0056.78  3000.00` | PASS |
| B7 deck on B9 image | `2048_B9_A` | `deck_B7_A.b6` | ` 21 -0012.34  3000.00` | PASS |
| MIN_X / MIN_G100 | `2048_B9_A` | minimal decks | ` 21 -0012.34  3000.00` | PASS |

All 13 verdict JSONs are in `harness/runs/verdict_*.json` with `plumbing=PASS`,
`result_21_line=true`, `completion_marker=true`.

**Causality.** A vs B: image SHA identical; only the GOTO label bytes in the deck differ
(`100` -> `200`); the printed value changes. PATCH: deck frozen, one 6-byte machine word
(`BW_THRESH`, f32(0) -> f32(20.0)) plus the two recomputed zone checksums; `12.34 -> 56.78`.
RESTORE: byte-identical to A; value returns. GOTO/IF/FORMAT label resolution, digit accumulation
and all arithmetic are executed by BESM-6 code; no IR card, no FRONT, no host-computed digit.

`cmp -l 2048_B9_A 2048_B9_PATCH` differs in 9 bytes (3 machine words: threshold + two checksums).
`cmp 2048_B9_A 2048_B9_RESTORE`: 0 differences.

## 4. Word budget / invariants (Task 1 image vs `2048_base`)

| resource | used | limit | verdict |
|:--|--:|--:|:--|
| N+3 converter | 55 | 58 | PASS |
| N+2 changed words | 543 | 649 | PASS |
| N+2 forbidden band 526..900 | 0 | 0 | PASS |
| body N+1 changed words | 483 | 998 | PASS |
| keeper `body[0o26]` | `0o1000040000000` | preserved | PASS |
| LEX code | 605 hw | 829 slots | PASS |

## 5. Task 2: attempted CALL/SUBROUTINE binding, and the exact blocker

`build/b9_call_build.py` adds, entirely in machine code: 4-byte keyword windows for `CALL`,
`SUBR` (SUBROUTINE prefix) and `RETURN`; modes 22/23 that pack an ASCII name into a 6-bit TEXT
word (ASCII-0x20, shifted left 6 per char, docs/109/114); a 2-entry body-resident
`(TEXT name, entry token index)` table written at `SUBROUTINE NAME`; a `FIND_SUB` linear XOR
compare in FIXUP that patches the CALL token PAY with the resolved entry index; and CONTROL
handlers for SUB35 (CALL: save C_SPC in `BW_RETADDR`, jump to PAY), SUB36 (no-op header) and
SUB40 (RETURN: C_SPC = `BW_RETADDR`).

**Build succeeds and the budget allows it:** `LEX=720 hw / 829 slots`, N+2 543/649,
body 488/998, forbidden band untouched. So the blocker is **not** the word budget.

**Runtime blocker (C oracle, deterministic, `images/2048_B9C_A` + `deck_B9C_CALL.b6`):**

1. `FOUND_CALL` is reached; the CALL token (TK10/SUB35) is emitted at token index 7.
2. The `SUBR` keyword window **never matches**: MTR of 23 `AEX` comparisons against the
   `0x53554252` constant shows no window ever equals `SUBR`; the `FOUND_SUBR` address
   (`0o3102`) is never executed.
3. Consequently `BW_NSUB = 0`, `FIND_SUB` returns 0, and the CALL token's PAY stays `0`.
4. CORE at the failure shows `C_SPC = 0`; B4 fetches token 0 repeatedly and the CPU runs through
   zero words at RAM `0o41764..0o41777`, ending in `КОНТРОЛЬ КОМАНДЫ` at PC `0o42000`
   (`uj 0`), with no `21` line.

Root cause of the window/name-table state corruption is **not isolated** within this effort. The
new cells sit in the body gap `0o670..0o677` / `0o677,0o716` and N+2 offsets `153..155`; a
dedicated body/N+2 marker sweep (the docs/120 method) is needed to prove those cells survive
LEX/B4 execution before this path can be trusted. This image (`2048_B9C_A`) is therefore
evidence of an attempt, **not** a delivered feature. No SUBROUTINE/CALL gate is claimed.

## 6. Supported / unsupported F77 subset (honest)

**Supported and SIMH-proved:** assignments with literals and `+ - * /` and parentheses;
`PRINT <label>,X` with `Fw.d` FORMAT (w=2/4); SQRT/ABS/MOD; fixed-count and generalised DO
(from base images); 1..3 digit decimal statement labels in columns 1-5; arithmetic
`IF (<real>) l1,l2,l3` with 1..3 digit labels (one IF per program, label value <= 255 for the
8-bit PACK fields); `GOTO <1..3 digit label>`; multi-label FORMAT references; `END`.

**Not supported:** CALL/SUBROUTINE/COMMON name binding (Task 2 blocked); nested/computed GOTO,
logical IF, variable/expression IF operands, more than one IF per program; arrays, COMPLEX,
double precision, DSQRT; `READ`, `OPEN/CLOSE/INQUIRE`, `END=/ERR=/IOSTAT`; nested DO with
arbitrary body; full 5-digit labels (POS field holds <= 99999 in principle but the scanner's
digit loop is proven only to 3 digits here).

## 7. Reproduce

```
cd /tmp/.private/azizz/opencode/b9-labels
python3 build/b9_labels_build.py --build B9_A
python3 build/b9_labels_build.py --build B9_PATCH --patch
cp images/2048_B9_A images/2048_B9_RESTORE
python3 harness/drive_b.py --case A --deck decks/deck_B9_A.b6 --image images/2048_B9_A --session bh-A
python3 harness/drive_b.py --case B --deck decks/deck_B9_B.b6 --image images/2048_B9_A --session bh-B
python3 harness/drive_b.py --case P --deck decks/deck_B9_IF.b6 --image images/2048_B9_PATCH --session bh-P
python3 harness/drive_b.py --case R --deck decks/deck_B9_IF.b6 --image images/2048_B9_A --session bh-R
# Call attempt (fails as documented):
python3 build/b9_call_build.py --build B9C_A
python3 build/oracle_run.py CALL images/2048_B9C_A decks/deck_B9C_CALL.b6
```

BLOCKED
