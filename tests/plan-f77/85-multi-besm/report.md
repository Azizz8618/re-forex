# re-forex: several chained BESM machine inserts and a Fortran-style accumulator read

Date: 22.11.2026. All work is copy-only. Workspace:
`/tmp/.private/azizz/opencode/re-forex-besm-multi/`; emulator disk copies under
`/dev/shm/re-forex-besm-multi/`. No repository file, git index, live disk, tmux
session, process or dispak source was modified. `HOME` and `BESM6_PATH` were
redirected to per-case copies of disks 2048/2053/2099.

## 0. Verdict

**PASS for "multi-insert + accumulator read work".** Four raw 48-bit words from
real edited Fortran cards are installed into the clean high-RAM area (zone
`N+3`), reached by the PC in source order, and executed before a `*64` print.
One card uses an ordinary Fortran assignment to both insert a word and capture
the accumulator into a named body cell; zeroing that one generated store word
changes the printed digit from `07.00` to `04.00`. Changing the second insert's
operand changes `07.00` to `08.00`. Zeroing an inserted word or the entry jump
changes the output as predicted. All 9 cases end with `КОНЕЦ ЗАДАЧИ`; CORE shows
every installed word at its measured address; MTR shows every PC from `30114`
through `30122` being fetched and executed.

The accumulator read uses **Fortran-style assignment only**. No token of the
research document's former empty-assignment spelling appears in any source, IR
record or report artifact.

## 1. Exact supported syntax (FOREX 2.02 fixed form, DECIMAL literals only)

All cards start in column 7, are at most 72 columns long, and contain no `B`
suffix, no octal literal, no `CHARACTER`, and no non-Fortran operator token.

| Card (column 7 onward) | FRONT rule | Meaning |
|:--|:--|:--|
| `BESM(<hi>,<lo>)` | 38 | insert one raw 48-bit word, `word = hi*2**24 + lo`, `0 <= hi,lo <= 2**24-1` |
| `V = BESM(<hi>,<lo>)` | 39 | insert the same raw word first, **then store the current accumulator into named cell `V`** |
| `X = 1.0`, `Y = X+2.0`, ... | 31 | unchanged ordinary assignment |

`V` is one of `X`, `Y`, `N`, `I` (varindex 1, 2, 3, 4). Spaces around `=` are
optional and skipped by the parser. The accumulator read is therefore spelled
as an ordinary Fortran assignment: the right-hand side names the raw-insert
operation, the left-hand side names the destination cell. Its documented
special-case meaning is exactly "insert executes first, then the accumulator is
stored into `V`" (the analogue of the historical empty-assignment idiom, but
written with Fortran tokens only).

Several cards of either kind may appear in one deck. Each is classified
independently in FRONT's `DO 200 I = 1, NL` loop, so each emits its own IR
records carrying its own physical card number as `SEQ`; the `SEQ` values
increase with source line order. That is the program's insertion order.

Real deck used for case C (cards appended after `END`, before `*execute`):

```
      BESM(46091,1032)
      Y = BESM(33804,46091)
      BESM(33800,46090)
      BESM(1032,1032)
```

## 2. IR records

```
777001 <seq> 38|39 <itype>          rule record for each new card
777006 <seq> 1 <hi> <lo>            raw 48-bit word = hi*2**24 + lo
777007 <seq> <varindex>             accumulator store into cell V
```

Record `777007` is the new accumulator-read record (the task's suggested
marker); it is numeric-only and carries `seq` plus `varindex`, never any source
text. Rule 39 emits both `777006` and `777007` for the same card, in that order
(insert, then store). All `777001..777005` records for other cards are
unchanged. Evidence: `evidence/C_three_inserts_ir.txt`:

```
777006 records: [(11,1,46091,1032), (12,1,33804,46091),
                 (13,1,33800,46090), (14,1,1032,1032)]
777007 records: [(12,2)]
```

Byte-identity: original FRONT and patched FRONT on the same 10-card deck with
no BESM cards produced **79 records each, byte-identical** (`ERR=0` both runs;
`evidence/byte_identity.txt`). Full source diff: `evidence/front.diff` (104
lines; only additions and the one exit-target change needed to reach the new
rule). Rule 39 is checked before rule 31 so a `V = BESM(...)` card is never
misread as an ordinary expression assignment; for a deck without BESM cards the
new check always falls through to rule 31.

## 3. Word placement and RAM map (all addresses derived from measured constants)

Constants: `BASE = 0o1757` (body RAM base), `N = 0o2350`
(`*TRANS:OURMRK*,,412350`), and the measured zone-`N+3` map from test 80:
zone `N+3 = 0o2353` word `k` lands at RAM `0o30114 + k` (58 clean words,
`0o30114..0o30205`, not executed by the resident path).

Entry and fall-through guard (body):

| body | RAM | word | role |
|:--|:--|:--|:--|
| 9..13 | `0o1770..0o1774` | unchanged | proven ARX/STO digit-building chain; ends with AU = GOST word C |
| 14 | `0o1775` | `0o0303011400000000` | structured jump (left half `0o03030114`) to `0o30114`; right half 0 |
| 15 | `0o1776` | `OBJ12 = 0o0064200402200000` | unchanged `*64 2004`; prints base value if the entry jump is zeroed |
| 16 | `0o1777` | `RET = 0o6700000002200000` | unchanged `uj 0(15)` |

High-RAM chain (zone `N+3`, word `k` to RAM `0o30114+k`):

| k | RAM | 48-bit word | decoded halfwords | role |
|:--|:--|:--|:--|:--|
| 0 | `0o30114` | `0013201300002010` | `arx 0o2013 / atx 0o2010` | insert 1: add +1 weight to GOST word C, store |
| 1 | `0o30115` | `0010201400132013` | `xta 0o2014 / arx 0o2013` | insert 2: build clean `3*2**40` in AU |
| 2 | `0o30116` | `0000201200002012` | `atx 0o2012 / atx 0o2012` | accumulator read (from `777007`): store AU into Y cell |
| 3 | `0o30117` | `0010201000132012` | `xta 0o2010 / arx 0o2012` | insert 3a: reload GOST C and add Y cell |
| 4 | `0o30120` | `0000201000002010` | `atx 0o2010 / atx 0o2010` | insert 3b: store final GOST C |
| 5 | `0o30121` | `0064200402200000` | `*64 2004 / ...` | print inside high RAM |
| 6 | `0o30122` | `6700000002200000` | `uj 0(15)` | return to resident via M15 |

Data cells inside the proven body window: GOST word C `0o2010` (body `0o31`),
addend `+1` at `0o2013` (body `0o34`, `1<<40`), addend `+2` at `0o2014` (body
`0o35`, `2<<40`), named Y cell at `0o2012` (body `0o33`). Descriptor pair
`0o2004/0o2005` and GOST words A/B/C (`0o2006/0o2007/0o2010`) are byte-for-byte
the proven fixture; only their instruction stream moved to high RAM. All raw
words are emitted verbatim from `777006`/`777007`; no opcode is re-encoded.

## 4. Execution and causal value trace

Starting AU = GOST word C with Y units 3 (built by body 9..13). The MTR window
`30110..30132` records AU **before** each halfword:

```
MTR 30114L arx 2013  AU=060700000114417   ; GOST C, Y units 3 (+ prior build)
MTR 30114R atx 2010  AU=100700000114417   ; +1<<40 -> Y units 4, C stored
MTR 30115L xta 2014  AU=100700000114417
MTR 30115R arx 2013  AU=40000000000000    ; load 2<<40, add 1<<40
MTR 30116L atx 2012  AU=60000000000000    ; ACC = 3<<40 -> stored into Y cell
MTR 30116R atx 2012  AU=60000000000000    ; redundant second store
MTR 30117L xta 2010  AU=60000000000000    ; reload GOST C (Y units 4)
MTR 30117R arx 2012  AU=100700000114417   ; add Y cell 3<<40
MTR 30120L atx 2010  AU=160700000114417   ; final C, Y units 7
MTR 30121L *64 2004  AU=160700000114417   ; prints 21 01.00 07.00
MTR 30122L uj  0(15) AU=160700000114417   ; return, then КОНЕЦ ЗАДАЧИ
```

This is direct evidence that the inserted words were in RAM, their PCs were
reached, the accumulator read captured a clean weight, and the captured value
was added into the printed GOST digit. The three logical inserts are (1) the
`+1` add, (2) the clean-weight build, (3) the reload/add/store pair (two raw
words). They execute in source order because `SEQ` order is the placement order.

## 5. A/B from real edited Fortran decks (all end with `КОНЕЦ ЗАДАЧИ`)

Driver `run_ab.py`; per-case IR, console, CORE and MTR evidence under
`evidence/` and `/dev/shm/re-forex-besm-multi/evidence/`.

| Case | Deck variation | Console print | End | Result |
|:--|:--|:--|:--|:--|
| `A_baseline` | no BESM/assignment cards | `21 01.00 03.00` | yes | OK |
| `B_one_insert` | one `BESM(46091,1032)` | `21 01.00 04.00` | yes | OK |
| `C_three_inserts` | four chained raw words incl. `Y = BESM(...)` | `21 01.00 07.00` | yes | OK |
| `D_acc_read_off` | same deck as C, accumulator-store word zeroed | `21 01.00 04.00` | yes | OK |
| `E_operand_change` | 2nd insert operand `0o2013` to `0o2014` | `21 01.00 08.00` | yes | OK |
| `F_zero_insert1` | 1st inserted word zeroed | `21 01.00 06.00` | yes | OK |
| `F2_zero_insert3b` | final store word zeroed | `21 01.00 04.00` | yes | OK |
| `G_zero_entry` | entry jump at body 14 zeroed (fall-through guard) | `21 01.00 03.00` | yes | OK |
| `H_mtr` | same as C with MTR tracing | `21 01.00 07.00` | yes | OK |

Predictions were fixed before each run from the source operands. `D` is the
clean accumulator-read A/B: the only machine difference from `C` is the single
`777007`-derived word; with it the digit is `07.00`, without it `04.00`. `E`
changes one decimal operand in the second insert card. `F`, `F2` and `G` show
that zeroing an inserted word or the entry jump changes the output without
disturbing the resident print path or the final task end.

## 6. CORE and MTR evidence

CORE dump at entry PC `0o1770` (`BESM6_CORE_ON_PC=1770`, `CORE_SKIP=6`) for every
case: `evidence/<case>_core.txt`. Case C reports
`CORE_WORDS=7 MISMATCH=0`, i.e. all seven high-RAM words (four inserts, one
accumulator store, print, return) were present at `0o30114..0o30122` with the
exact values emitted by FRONT. The zeroed-word cases report the same map with
the one selected word equal to zero. MTR proof is `evidence/H_mtr_mtr.txt`; the
high-RAM PCs observed are `30114, 30115, 30116, 30117, 30120, 30121, 30122`,
exactly the seven installed words. No failing PC or unintended instruction was
seen; the only control that removes the chain is the deliberate zeroing of the
entry jump (case `G`), which falls through to the unchanged body 15 print.

## 7. Reproduce and evidence index

```
cd /tmp/.private/azizz/opencode/re-forex-besm-multi
BESM6_DISK_SHARE=/usr/local/share/besm6 python3 front_multi.py
BESM6_DISK_SHARE=/usr/local/share/besm6 python3 run_ab.py
```

| file | content |
|:--|:--|
| `FRONT.FTN`, `evidence/front.diff` | patched copy and full diff |
| `evidence/byte_identity.txt` | 79/79 identical records for a no-BESM deck |
| `evidence/*_ir.txt` | FRONT records, event placement, expected print |
| `evidence/*_console.txt` | full console per case (all with task end) |
| `evidence/*_core.txt` | CORE readback of every high-RAM word |
| `evidence/H_mtr_mtr.txt` | MTR trace of the high-RAM chain |
| `results.json`, `run_ab.log` | 9/9 cases OK, `VERDICT: PASS` |

DONE
