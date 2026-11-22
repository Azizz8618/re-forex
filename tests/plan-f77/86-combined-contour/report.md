# re-forex P9: one contour with BOTH wide output AND chained BESM inserts

Date: 22.11.2026. All authored files live only under
`/tmp/.private/azizz/opencode/re-forex-combined/`. Emulator disk copies were made
under `/dev/shm/re-forex-combined/cases/` with per-case `HOME`/`BESM6_PATH`
redirection; the bulky disk images were removed after each run, only textual
evidence was retained. No repository file was edited, no git write, no live
disk, no tmux session, no process and no dispak C source was touched. Zone
`N = 0o2350` (`*TRANS:OURMRK*,,412350`) is used throughout. Copies of disks
2048/2053/2099 were used in every machine case.

Toolchain note: the reused test-71 `inject.py`/`compile.py` FRONT pipeline can
rewrite timestamped logs under the repo's `logs/` directory as a side effect.
The working tree already carried unrelated pre-existing modifications before
this task (`tools/run_besm6_deck.py` modified 20.11, `tests/plan-f77/64-monitor-patch/`
untracked 22.11 01:49, both predating this workspace's 22.11 23:10 creation).
None were reverted or staged; no source file was edited by this task.

## 0. Verdict

**PASS for "both features work in one compilation".** A single real edited
Fortran deck produces, in ONE FRONT compilation, the wide `777005` IR for
`X=1234.56 ; Y=X*2.0+1.0` AND four raw `777006` insert records plus one
`777007` accumulator-read record (`Y = BESM(...)`). One contour install prints
the unmodified wide value (`21 1234.56 2470.12`) from the intact body chain and
then, after the chained BESM words execute in high RAM, prints the MODIFIED wide
value (`21 1234.56 5470.12`). 9/9 machine cases pass, all with `КОНЕЦ ЗАДАЧИ`,
CORE `MISMATCH=0`, and pre-run zero-seed readback. Changing one BESM operand,
zeroing the accumulator-store word, zeroing an inserted word, zeroing the entry
jump and using a negative wide value all produce the exact predicted changes.

## 1. The real conflict and the minimal fix

The two proven layouts collide in the 8-word body instruction window:

| body | RAM | test 84 (wide) | test 85 (multi-BESM) |
|:--|:--|:--|:--|
| 9..13 | 1770..1774 | build GOST A, B, C | same (unchanged) |
| 14 | 1775 | `ARX 2017 / STO 2011` (build GOST D fraction) | **entry jump to 0o30114** |
| 15 | 1776 | `*64 2004` (wide print) | fall-through print |
| 16 | 1777 | `uj 0(15)` (return) | fall-through return |

A naive merge would put the entry jump at body[14], destroying the ARX word that
writes GOST word D. GOST D would stay all-zero digits, so the wide value could
not print. That is the exact conflict.

**Minimal fix (no wide word changed):** place the entry jump at **body[16] /
RAM 0o1777**, which is only the wide test's *return*, not part of the digit
chain. The return is preserved twice: at the end of the high-RAM routine
(`0o30122`) and as a fall-through guard in the free cell **body[17] / RAM
0o2000**. Body[9..15] (all six digit-building words plus the `*64` print) stays
byte-for-byte identical to test 84. Cost: one relocated word (the return) plus
one new guard word.

## 2. Combined layout (explicit documented split)

All RAM addresses derive from `BASE = 0o1757`; zone `N+3` word `k` lands at RAM
`0o30114 + k` (58 clean words `0o30114..0o30205`).

Low window (body[1..0o43]):

| body | RAM | role | provenance |
|:--|:--|:--|:--|
| 9 | 1770 | `XTA 2006 / ARX 2020` | 84, intact |
| 10 | 1771 | `STO 2006 / XTA 2007` | 84, intact |
| 11 | 1772 | `ARX 2021 / STO 2007` | 84, intact |
| 12 | 1773 | `XTA 2010 / ARX 2022` | 84, intact |
| 13 | 1774 | `STO 2010 / XTA 2011` | 84, intact |
| 14 | 1775 | `ARX 2017 / STO 2011` | 84, intact (conflict avoided) |
| 15 | 1776 | `*64 2004` | 84, intact: FIRST print |
| 16 | 1777 | `0o0303011400000000` | structured UJ to 0o30114 (entry) |
| 17 | 2000 | `uj 0(15)` | guard if body[16] zeroed (free cell) |
| 25/26 | 2004/2005 | proven `*64` descriptor pair | unchanged |
| 27/30/31/32 | 2006/2007/2010/2011 | zero-seeded GOST A/B/C/D + EOF | 84 |
| 33 | 2012 | Y accumulator-read cell (init 0) | 85 idiom |
| 34 | 2013 | BESM weight `1<<32` (Y thousands) | new data |
| 35 | 2014 | BESM weight `2<<32` (Y thousands) | new data |
| 40/41/42/43 | 2017/2020/2021/2022 | wide digit weights wD/wA/wB/wC | 84 |

GOST C byte 1 is `Y_i0` (thousands digit, shift `8*(5-1)=32`), so each inserted
weight of `k<<32` adds `k * 1000` to the printed wide Y without touching the
sign byte (byte 0) or the fixed dot (byte 5).

High-RAM chain (zone `N+3`, source SEQ order):

| k | RAM | word | decoded | role |
|:--|:--|:--|:--|:--|
| 0 | 30114 | `0010201000132013` | `xta 2010 / arx 2013` | insert 1: reload GOST C, add +1 thousands |
| 1 | 30115 | `0000201000102014` | `atx 2010 / xta 2014` | store C; build +2 thousands in AU |
| 2 | 30116 | `0000201200002012` | `atx 2012 / atx 2012` | **777007 (Y = BESM)**: AU -> Y cell |
| 3 | 30117 | `0010201000132012` | `xta 2010 / arx 2012` | reload C, add Y cell |
| 4 | 30120 | `0000201000002010` | `atx 2010 / atx 2010` | store final GOST C |
| 5 | 30121 | `0064200402200000` | `*64 2004` | SECOND print (modified wide value) |
| 6 | 30122 | `6700000002200000` | `uj 0(15)` | return to resident |

## 3. Real Fortran deck and IR samples (one compilation)

Deck (canonical deck edited on a copy; BESM cards appended after `END`):

```
      X=1234.56
      Y=X*2.0+1.0
      BESM(33800,46091)
      Y = BESM(1032,33804)
      BESM(33800,46090)
      BESM(1032,1032)
```

FRONT (patched copy, rules 38/39) emits both streams in the SAME `call.out`:

```
777005 5 1 0 123456 0        wide literal 1234.56
777005 6 2 0 1 0             Y = X
777005 6 1 0 200 0           * 2.0
777005 6 3 3 0 0             +
777005 6 1 0 100 0           + 1.0
777006 11 1 33800 46091      xta 2010 / arx 2013
777006 12 1 1032 33804       sto 2010 / xta 2014
777007 12 2                  accumulator store into Y (varindex 2)
777006 13 1 33800 46090      xta 2010 / arx 2012
777006 14 1 1032 1032        sto 2010 / sto 2010
```

Evaluated IR: `env = {X: 1234.56, Y: 2470.12}`, bound 6;
X digits `(' ',[1,2,3,4],[5,6])`, Y digits `(' ',[2,4,7,0],[1,2])`.
A no-BESM deck produced zero `777006`/`777007` records and the single wide
print (case A). Byte-identity of rules 30..37 for decks without BESM cards is
inherited from test 85's `evidence/byte_identity.txt` (79/79 records).

## 4. Causal value trace

Entry to high RAM leaves AU = GOST D (from body[14]) after the first print. The
chain reloads GOST C (Y integer digits `2 4 7 0`) before modifying it:

```
MTR 30114L xta 2010  AU=20123103607417   ; GOST C, Y=2470 (first print already done)
MTR 30114R arx 2013  AU=360100401600016   ; +1<<32 -> Y thousands digit 2->3
MTR 30115L atx 2010  AU=360140401600016   ; C stored: Y=3470.12
MTR 30115R xta 2014  AU=360140401600016   ; load +2<<32 weight
MTR 30116L atx 2012  AU=0100000000000     ; 777007: Y cell = 2<<32
MTR 30117L xta 2010  AU=0100000000000     ; reload C (Y=3470)
MTR 30117R arx 2012  AU=360140401600016   ; + Y cell -> thousands 3+2=5
MTR 30120L atx 2010  AU=360240401600016   ; final C: Y=5470.12
MTR 30121L *64 2004  AU=360240401600016   ; print -> 21 1234.56 5470.12
MTR 30122L uj 0(15)  AU=360240401600016   ; return, КОНЕЦ ЗАДАЧИ
```

## 5. A/B table (exact console lines; all end with `КОНЕЦ ЗАДАЧИ`)

Driver `run_combined.py`; per-case IR, console, CORE, MTR and pre-run evidence
under `evidence/`; summary in `results.json`. `pre_ok=True` means all 14 GOST
digit bytes were ZERO on the installed disk copy before the run. Raw console
uses double spaces (`21  1234.56  2470.12`); the table collapses them.

| Case | Real-deck variation | Console print(s) | End | Pre | CORE | Result |
|:--|:--|:--|:--|:--|:--|:--|
| A_baseline | wide only, no BESM cards / no jump | `21 1234.56 2470.12` | yes | ok | 0 | OK |
| B_with_inserts | wide + 4 BESM cards (incl. `Y=BESM`) | `21 1234.56 2470.12` ; `21 1234.56 5470.12` | yes | ok | 0 | OK |
| C_operand_change | 2nd insert `33804`->`33803` (`xta 2014`->`xta 2013`) | `21 1234.56 2470.12` ; `21 1234.56 4470.12` | yes | ok | 0 | OK |
| D_zero_accstore | B deck, `777007` word (slot 2) zeroed | `21 1234.56 2470.12` ; `21 1234.56 3470.12` | yes | ok | 0 | OK |
| E_zero_insert4 | B deck, final store word (slot 4) zeroed | `21 1234.56 2470.12` ; `21 1234.56 3470.12` | yes | ok | 0 | OK |
| F_zero_entry | B deck, entry jump body[16] zeroed | `21 1234.56 2470.12` | yes | ok | 0 | OK |
| G_negative | `X=-1234.56 ; Y=X+2.0` + BESM cards | `21 -1234.56 -1232.56` ; `21 -1234.56 -4232.56` | yes | ok | 0 | OK |
| H_mtr | B deck, MTR window 30110..30132 | `21 1234.56 2470.12` ; `21 1234.56 5470.12` | yes | ok | 0 | OK |
| N_core | B deck, CORE at PC 1770 | `21 1234.56 2470.12` ; `21 1234.56 5470.12` | yes | ok | 0 | OK |

Predictions were fixed before each run from the source operands. `B` proves the
combined effect: the first print is the intact wide value, the second is the
modified value (+3000). `C` changes one BESM operand and the second print moves
from `5470.12` to `4470.12` (Y cell +1 not +2 thousands). `D` is the clean
Fortran-assignment A/B: the only machine difference from `B` is the single
`777007`-derived word; with it `5470.12`, without it `3470.12`. `E` zeroes an
inserted word. `F` zeroes the entry jump: the guard at body[17] returns, so the
inserts never run and only the wide print remains (it does NOT hang or corrupt
the print path). `G` proves a negative wide value with inserts keeps both sign
bytes and widened digits correct.

## 6. CORE and MTR evidence

CORE dump at PC `0o1770`, `CORE_SKIP=6`, case `N_core`
(`evidence/N_core_core.txt`): `CORE_CHECKED=29 MISMATCH=0`. It confirms the wide
chain is still installed byte-for-byte at RAM 1770..1776, the entry jump is at
RAM 1777 and the guard at RAM 2000, the four wide GOST words and four weights are
present, and all seven high-RAM words are present at 0o30114..0o30122:

```
body[17] RAM 1776 want=0064200402200000 got=0064200402200000   ; *64 print (wide)
body[20] RAM 1777 want=0303011400000000 got=0303011400000000   ; entry UJ
body[21] RAM 2000 want=6700000002200000 got=6700000002200000   ; guard RET
zone3[000] RAM 030114 want=0010201000132013 got=0010201000132013
zone3[002] RAM 030116 want=0000201200002012 got=0000201200002012 ; 777007 word
zone3[004] RAM 030120 want=0000201000002010 got=0000201000002010
zone3[005] RAM 030121 want=0064200402200000 got=0064200402200000
zone3[006] RAM 030122 want=6700000002200000 got=6700000002200000
```

(body indices in the dump are printed in octal, e.g. `body[20]` = decimal 16.)

MTR window `30110..30132`, `N=120`, `SKIP=0`, case `H_mtr`
(`evidence/H_mtr_mtr.txt`) shows every high-RAM PC `30114, 30115, 30116, 30117,
30120, 30121, 30122` being fetched and executed with the AU transitions quoted
in section 4. With `SKIP=6` the first six triggers (the first three inserted
words) were skipped, so `SKIP=0` is the authoritative trace. A wide MTR window
re-arms in `cu.c` and floods the console with resident passes; the quoted first
arm is the authoritative trace of OUR chain.

## 7. Reproduce and evidence index

```
cd /tmp/.private/azizz/opencode/re-forex-combined
TMPDIR=/tmp/.private/azizz/opencode python3 run_combined.py   # 9 cases -> results.json
```

| path | content |
|:--|:--|
| `front_combined.py`, `FRONT.FTN`, `harness/*` | real edited-deck FRONT probe + patched compiler copies |
| `codegen_combined.py` | combined body/zone layout (this task's new code) |
| `runner_combined.py` | zone-2350 + zone N+3 install, CORE/MTR, /dev/shm copies |
| `run_combined.py` | A/B orchestration |
| `codegen_wide.py`, `codegen_multi.py`, `besm_codegen_base.py`, `runtime_xy.py`, `codegen.py`, `expr_ir.py`, `installer.py`, `token_interface.py` | copied proven modules (path patches only) |
| `evidence/*_ir.txt` | FRONT 777005/777006/777007, digits, weights, event placement |
| `evidence/*_console.txt` | full console per case, all with `КОНЕЦ ЗАДАЧИ` |
| `evidence/*_core.txt` | CORE readback of installed body + high-RAM words |
| `evidence/H_mtr_mtr.txt` | MTR trace of the high-RAM chain |
| `evidence/*_pre.txt` | pre-run zero-seed readback |
| `results.json` | 9/9 cases OK, `VERDICT: PASS` |

Limitations (not faked): as in test 84, magnitude is `|v| <= 9999.99`; the
`777007` store is a Fortran-style assignment with the documented special meaning
"insert executes first, then the accumulator is stored into V"; multiply/divide
are folded from IR; no arrays/functions/`**`. The high-RAM chain is driven by the
raw `777006`/`777007` records, no opcode is re-encoded.

DONE
