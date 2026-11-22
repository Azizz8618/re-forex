# BESM-style raw machine-word insertion in our `*TRANS` compiler contour

Date: 22.11.2026. All work is copy-only. Workspace:
`/tmp/.private/azizz/opencode/re-forex-besm-impl/`; all emulator disk copies live under
`/dev/shm/re-forex-besm-impl/`. No repository file, git index, live disk, tmux session,
process or dispak source was modified.

## Verdict

**PASS — machine inserts work.** A raw 48-bit word emitted from a real edited Fortran
deck as FRONT IR `777006` was installed into the live execution path of our `*TRANS`
body (RAM `0o1775`), fetched by the PC (MTR), executed, and changed the printed Y digit
by exactly the predicted amount. Changing the raw word's operand in the source changed
the printed value; zeroing the inserted word returned the output to baseline. Every
case ended with `КОНЕЦ ЗАДАЧИ`.

## 1. Interface decision (why two decimal halves)

The research contract proposed `777006 <seq> <kind> <value>` carrying one 48-bit value.
`docs/63-full-compiler-design.md` §"FOREX 2.02" states the FOREX 2.02 INTEGER mantissa is
**40 bits**, and the existing codegen keeps 48-bit words as two 24-bit halves for the same
reason. A single decimal INTEGER therefore cannot hold a raw 48-bit word in FRONT.

Chosen, documented numeric-only spelling (fixed form, DECIMAL literals only):

```
      BESM(<hi>,<lo>)          full word = hi * 2**24 + lo,  0 <= hi,lo <= 2**24-1
```

FRONT emits:

```
777006 <seq> 1 <hi> <lo>
```

`kind=1` still means "raw 48-bit machine word"; the two half-fields are a pure
FOREX-2.02 transport encoding, recombined losslessly by the codegen. No `B` suffix,
octal literal, CHARACTER, or other unsupported syntax is used.

## 2. Source diff (copy of FRONT.FTN)

Full diff: `evidence/front.diff`. Key hunks (original -> copy):

```diff
+      INTEGER MR6
+      INTEGER HI, LO
+      INTEGER PAT38(5)
+      DATA MR6 /777006/
+      DATA PAT38 /66,69,83,77,40/        ! ASCII "BESM("
@@ rule 37 (no existing rule touched) @@
+ 4180 IF (IRULE .NE. 0) GOTO 418
+         MATCH = 1
+         DO 4181 J = 1, 5
+            IF (C(IFIRST+J-1,I) .NE. PAT38(J)) MATCH = 0
+ 4181 CONTINUE
+         IF (MATCH .NE. 1) GOTO 418
+         P = IFIRST + 5
+         HI = 0
+ 4182 CH = C(P,I)
+         IF (CH .LT. 48 .OR. CH .GT. 57) GOTO 4183
+         HI = HI*10 + CH - 48
+         ...
+ 4185 IRULE = 38
+         ITYPE = 1
@@ immediately after "PRINT 9001, MR1, SEQ(I), IRULE, ITYPE" @@
+      IF (IRULE .NE. 38) GOTO 555
+      PRINT 9006, MR6, SEQ(I), 1, HI, LO
+      GOTO 260
+  555 CONTINUE
+ 9006 FORMAT(1X,5I8)
```

No existing statement, DATA, FORMAT, rule 30..37 path or record 777001..777005 writer
was changed. Labels were placed with the last digit in column 5 (column 6 is the
continuation field in FOREX fixed form).

**Compile proof:** `build_ERR=0 call_ERR=0` for every FRONT run. Byte-identity was
checked by running the original and the patched FRONT on the same 10-card no-BESM
deck and diffing all emitted records:

```
orig: ERR=0 records=79
patched: ERR=0 records=79
BYTE-IDENTICAL: True
```

Evidence: `evidence/identical_records.txt`. To preserve byte-identical SEQ numbering,
the main A/B cases append the BESM card after `END` (FRONT still classifies every card);
a supplementary `F_inline` case inserts it before `PRINT` and also passes.

## 3. IR sample

Real deck line (column 7 onward): `      BESM(46091,1032)`.

```
   777001      11      38       1
   777006      11       1   46091    1032
   777003      11       8
```

`46091*2**24 + 1032 = 0xB40B0408 = 0o0013201300002010`, decoded as two 24-bit
halfword instructions:

```
left  half = 0x00B40B = ARX | 0o2013   (add word at RAM 0o2013)
right half = 0x000408 = STO | 0o2010   (store accumulator into GOST word C)
```

The second source spelling `BESM(46092,1032)` gives `0o0013201400002010`
(`ARX 0o2014 / STO 0o2010`), selecting a different data cell.

Evidence: `evidence/B_besm_p1_ir.txt`, `evidence/C_besm_p2_ir.txt`.

## 4. Word placement

The codegen copy (`besm_codegen.py`, diff in `evidence/codegen.diff`) consumes every
`777006` record, validates `kind=1` and the 24-bit halves, and writes the exact
48-bit value into **body[14] (decimal) = RAM 0o1775**, the previously spare slot
between the digit-building chain (body 9..13) and `*64` print / return (body 15..16):

```
body[9..13]  : proven ARX/STO chain builds GOST words A, B, C
body[14]     : RAW 777006 WORD  <-- PC reaches it before *64
body[15]     : *64 2004 (print via descriptor)
body[16]     : uj 0(15)
```

At entry to body[14] the accumulator already holds GOST word C (`RAM 0o2010`, the
`Y` digits). The raw word adds a selected packed weight and stores C back:

```
body[0o34] RAM 0o2013 = 0o0020000000000000   (+1 in GOST byte 0 = Y units)
body[0o35] RAM 0o2014 = 0o0040000000000000   (+2 in GOST byte 0 = Y units)
body[0o31] RAM 0o2010 = GOST word C, zero-seeded, filled by body[12..13]
```

These cells are inside the proven copy window `body[0..0o43]`; ADRs derive from
`BASE=0o1757`; the zone is `N=0o2350`, catalog `*TRANS:OURMRK*,,412350`.

## 5. CORE / RAM evidence

Installed disk-copy readback (`besmtool dump 2048 --start=02351 --length=1` inside each
case), from `B_besm_p1/overrides.txt` and `readback_pre2.bin`:

```
body[16 ] RAM 1775 = 0013201300002010  bytes= 0 180 11  0 4 8   <-- exact raw word
body[34 ] RAM 2013 = 0020000000000000  bytes= 1 0 0 0 0 0
body[35 ] RAM 2014 = 0040000000000000  bytes= 2 0 0 0 0 0
```

(`body[16]`, `body[34]`, `body[35]` are the octal renderings of decimal indices 14,
28, 29 used by the override writer.) Zero-word case:
`body[16 ] RAM 1775 = 0000000000000000`.

## 6. Console A/B (all with `КОНЕЦ ЗАДАЧИ`)

Driver: `run_ab.py`; machine cases under `/dev/shm/re-forex-besm-impl/machine/cases/`;
console evidence under `evidence/*_console.txt`.

| Case | Source BESM | RAM 0o1775 word | Console print | End |
|:--|:--|:--|:--|:--|
| `A_baseline` | none | `0010200600102006` (original spare `XTA A_G1 / XTA A_G1`) | `21 01.00 03.00` | yes |
| `B_besm_p1` | `BESM(46091,1032)` | `0013201300002010` | `21 01.00 04.00` | yes |
| `C_besm_p2` | `BESM(46092,1032)` | `0013201400002010` | `21 01.00 05.00` | yes |
| `D_zero_word` | `BESM(46091,1032)`, body[14]=0 | `0000000000000000` | `21 01.00 03.00` | yes |
| `E_mtr` | `BESM(46091,1032)` | `0013201300002010` | `21 01.00 04.00` | yes |
| `F_inline` (card before PRINT) | `BESM(46091,1032)` | `0013201300002010` | `21 01.00 04.00` | yes |

Predictions were made before each run from the source operand: baseline Y=3, `+1`
weight -> Y=4, `+2` weight -> Y=5, zero word -> baseline (the zero word decodes as
`STO 0 / STO 0`, which writes the accumulator to fast register 0 and is harmless
here). Every prediction matched; `VERDICT: PASS` in `results.json`.

## 7. MTR proof that the raw word executed

`E_mtr` used `BESM6_DD_DEBUG=1`, MTR window `01770..01777`, `SKIP=6`. The trace shows
the PC at the raw-word slot and the two raw halfwords being fetched and executed
(evidence `evidence/mtr_besm.txt`, full trace `evidence/E_mtr_console.txt`):

```
MTR 01775L arx    2013(0) AU=60700000114417 ...
MTR 01775R atx    2010(0) AU=100700000114417 ...
 21  01.00  04.00
```

`01775` is `BASE + 14` decimal. The accumulator delta is
`0o100700000114417 - 0o60700000114417 = 0o20000000000000 = 2**40`, exactly one
increment of GOST byte 0 of word C, i.e. the Y units digit `3 -> 4`. This is direct
evidence that the inserted word was in RAM, its PC was reached, and its `ARX` changed
the value that `*64` subsequently printed.

## 8. Failure-mode note

No failing instruction was encountered. The only control that deliberately broke the
chain was zeroing the inserted word; even that run completed with `КОНЕЦ ЗАДАЧИ`,
returning the baseline value because `STO 0 / STO 0` does not disturb the descriptor or
the GOST print chain. A merely-stored word would not produce the MTR `01775L/R`
fetch lines nor the operand-dependent `03.00/04.00/05.00` changes.

**PASS: machine inserts work.**

DONE
