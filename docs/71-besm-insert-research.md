# `besm()` machine-insert intrinsic: pascal-re findings and design for our compiler

Research date 2026-11-22. Read-only task; no repository files were changed.
All line numbers below refer to files under `/home/azizz/Yandex.Disk/pascal-re/`
unless the path starts with `/home/azizz/Yandex.Disk/re-forex/`.

---

## 1. Source syntax accepted by pascal-re

### 1.1 Call form and dispatch

`BESM` is a registered **system procedure** (`pascompl.cc:951` declares
`systemProcNames[]`; `AGENTS.md:138`: "BESM(I) — системная процедура; целое
выражение I трактуется как машинная команда ЭВМ БЭСМ-6, вставляемая в объектный
модуль"). It is dispatched as `standProc` case 16 (`pascompl.cc:7549-7553`):

```c
case 16: { /* besm */
    expression();
    (void) formOperator(LITINSN);
    formAndAlign(curVal.i);
} break;
```

So the operand is parsed by the **full Pascal `expression()` grammar**
(`pascompl.cc:6428` expression, `6351` simpleExpression, `6272` term):
unary `+/-`, `+ - * / div mod and or`, parenthesised subexpressions, typed
constants and constant identifiers. Real-valued or non-integer forms are
rejected indirectly: `LITINSN` requires `ilm == ilCONST` and `typ->size == 1`
(`pascompl.cc:5044-5050`).

### 1.2 Literal forms

`INTCONST` lexing (`pascompl.cc:2137-2184`, enum `numberSuffix` at `:805`):

| Spelling | Meaning | Evidence |
|:--|:--|:--|
| `24`, `36`, `63` | decimal integer (no suffix) | `:2157-2159` `suffix=noSuffix` |
| `74000B`, `360100B`, `2200000B`, `630004B` | **octal** (suffix `B`, also KOI `w`) | `:2151-2152`, `:2163-2175` shifts 3 bits per digit; `:2169-2175` forces integer exponent |
| `74000C`, `2200000C` | octal "short address" (suffix `C`/`s`) | `:2153-2154`, `comments.txt:143` |
| `...T` | octal text, left-padded to 16 octal digits | `:2155-2156`, `:2176-2180` |
| identifiers/constants | any compile-time constant, e.g. `ASN64` | `pascompl.b6:35` `ASN64 = 360100B;` (C++ mirror `pascompl.cc:92` `ASN64 = 0360100`) |

Hence expressions such as `ASN64-24`, `ASN64 + 45`, `360100B-36` are all valid
(the literal `24`/`45`/`36` is **decimal**, so `ASN64-24` subtracts octal `030`).

### 1.3 Compile time vs run time

**Compile time.** `expression()` folds constants into an `Expr`;
`formOperator(LITINSN)` calls `genFullExpr()` (`pascompl.cc:4843-4855`) and then
`case LITINSN` requires a folded `ilCONST` value and copies it into `curVal`
(`:5044-5050`):

```c
case LITINSN:
     if (insnList->ilm != ilCONST) error(errNoConstant);       /* err 6 */
     if (insnList->typ->size != 1) error(errConstOfOtherTypeNeeded); /* err 7 */
     curVal = insnList->ilf5;
     break;
```

`errNoConstant = 6` is declared at `pascompl.b6:41` and its message is
"Missing constant" (`pascompl.cc:1151`). A variable operand is therefore a
compile error, not a run-time read. The *resulting instruction* executes at run
time; only its 24-bit value is fixed at compile time.

### 1.4 Relationship to `:=;` (empty assignment, accumulator read)

`assignStatement` (`pascompl.cc:6845-6894`) has an explicit compatibility branch:

```c
} else if (SY == SEMICOLON and allowCompat) {
    (void) formOperator(STORE);      /* store the ACCUMULATOR, no expression */
    bool102z = true;
    curExpr = NULL;
}
```

This is documented in `comments.txt:121-138`. The canonical idiom is:

```pascal
curVal := curVal;        /* load into accumulator                    */
besm(ASN64-24);          /* shift accumulator (raw instruction)      */
curVal := ;              /* store accumulator back                   */
```

A real instance is `pascompl.b6:678-697` inside `form1Insn`, where the high and
low 24-bit halves of a word are extracted with `besm(ASN64-24); leftInsn :=;`
and `besm(ASN64+24); half2 :=;`. Another is `pascompl.b6:3205`
`curVal := curVal;besm(ASN64-24);curVal:=;`.

---

## 2. What the compiler emits

### 2.1 One 24-bit instruction, not one 48-bit word

`formAndAlign(curVal.i)` (`pascompl.cc:1377-1382`, listing `pascompl.b6:758-763`)
calls two procedures:

```c
void form1Insn(int64_t arg) {                 // :1295-1326
    Insn.i = arg;
    opcode.i = Insn.i & ~077777;              // top 9 bits = opcode
    ... UJ peephole ...
    if (putLeft) { leftInsn = Insn.ii << 24; putLeft = false; }
    else         { putLeft = true; storeObjWord(leftInsn | (Insn.ii & halfWord)); }
}
void padToLeft() {                            // :1370-1375
    if (not putLeft) form1Insn(InsnTemp[UTC]);
    prevOpcode = 0;
}
void formAndAlign(int64_t arg) {              // :1377-1382
    form1Insn(arg); padToLeft(); prevOpcode = 1;
}
```

`halfWord = 077777777` (`pascompl.cc:906`) masks **24 bits**: a BESM-6
instruction is one half-word, two per 48-bit word (`comments.txt:394-400`).
Therefore `besm(v)` inserts **one 24-bit raw instruction at the current code
point**, using the low 24 bits of `v` (and updating `prevOpcode` so the UJ
peephole at `:1301-1316` sees a barrier). `formAndAlign` then pads with a UTC
(0o2200000, `pascompl.cc:133` `KUTC = 02200000`) if the raw word landed in the
right half, so **the next generated item starts at a left half-word**. Consequences:

* If the current slot is the left half, the raw instruction plus a UTC pad
  occupy a whole 48-bit word: `besm(ASN64-24)` -> 0o0036005002200000, and
  `besm(2200000B)` -> 0o0220000002200000 (verified by simulating
  `form1Insn`/`formAndAlign`).
* If the current slot is the right half, the raw instruction is packed with the
  preceding instruction in the same word (no pad is needed).
* It is genuinely **inline**: no helper call, no jump. Insertion order is the
  source order; `formAndAlign` guarantees subsequent code is word-aligned.

### 2.2 Object-module encoding

`storeObjWord` (`pascompl.cc:1284-1293`) writes the 48-bit value into
`objBuffer[1..1024]`; `outputObjFile` (`routines.txt:222` `20767 outputObjFile p`)
writes that buffer to the child/object module via `OBPROG`
(`comments.txt:431-436`). No relocation bit is added for a literal `besm`
value; it is an absolute 24-bit pattern exactly as supplied by `curVal`.

### 2.3 Cross-check: `procBESM` location

`routines.txt:214` lists `20031 procBESM` (address 0o20031 in the original
compiler); the decompiled C++ equivalent is the case-16 block above, and the
listing of the compiler's own source at `pascompl.b6:6902` (`16: { (* besm *)`)
matches. `decomp.pl:234` only rewrites the textual literal `(360100B)` to the
symbol `ASN64template`; it does not special-case `besm`.

---

## 3. Concrete real examples (expected words)

`ASN64 = 360100B` (`pascompl.b6:35`); integer subtractends are decimal, so
`ASN64-24 = 0o360100 - 0o30 = 0o360050`. All opcode decodings below use the
authoritative table in `dtran.cc:52-109` (`ARX 0x00b000 = 0o0130000`,
`*63 0x033000 = 0o0630000`, `ASN 0x01e000 = 0o0360000`, `*64 0x034000`).

| # | Source (file:line) | 24-bit inserted value | Word when emitted at a left slot (`+UTC` pad) | Observed behaviour |
|:--|:--|:--|:--|:--|
| 1 | `pascompl.b6:678` `besm(ASN64-24); leftInsn :=;` | 0o0360050 (ASN, shl 24) | 0o0036005002200000 | extract high half of a 48-bit word into `leftInsn` (`:691-694`) |
| 2 | `pascompl.b6:681` `besm(ASN64+24); half2 :=;` | 0o0360130 (ASN, shr 24) | 0o0036013002200000 | extract low half into `half2` (`:695-698`) |
| 3 | `pasdd1.pas:786`, `:801` `besm(360075B); (* SHL 3 *)` (`= ASN64-3`) | 0o0360075 | 0o0036007502200000 | shift accumulator left 3 bits while assembling an octal literal from decimal digit codes (`:783-792`) |
| 4 | `pashelp.pas:400` `besm(360100B-36);` then `work1 := ;` | 0o0360034 (ASN64 - decimal 36 = octal 044) | 0o0036003402200000 | shift ACC to isolate a byte of `fileBind`, read by the following empty assignment (`:401-405`) |
| 5 | `pascompl.b6:1291` `(*=z-*)besm(2200000B);(*=z+*)` (also `:1334`, `:1822`, `:5743`) | 0o2200000 = `KUTC` (`pascompl.cc:133`) | 0o0220000002200000 | UTC used as NOP/barrier under conditional compilation (`comments.txt:99-109`, `:119`) |

Bonus example: `pasdd1.pas:126` `besm(630004B); t:= ;` inserts 0o0630004
(`*63` immediate, `dtran.cc:100`), taking a time/counter word into `t` via the
accumulator, then `time := ord(t) * 0.01999999999999`. `pasdd1.pas:262`
`besm(360072B)` (`= ASN64-6`) is the same left-shift idiom used by the lexer
(`pascompl.b6:1275-1277`).

---

## 4. Minimal design for OUR compiler

### 4.1 Reuse first (hard rule)

Everything needed already exists; no new mechanism is required:

* `src/newcomp/FRONT.FTN` (378 lines) already tokenises fixed-form cards into
  logical lines (`N1.1`, `:65-87`), classifies rules 30..37 (`:124-187`), streams
  `777002` ASCII (`:201-207`), and emits structured RHS `777005` via the
  shunting-yard parser (`:208-350`) with `PRINT 9005` (`:349`). Extend this
  table; do not write a second front-end.
* `src/newcomp/EMIT.FTN` already provides `EMIT48(IR1,K1,A1,IR2,K2,A2)` =
  `HI = IR1*2^21+K1*2^15+A1`, `LO = ...` (`EMIT.FTN:66-74`), i.e. the exact
  24-bit half-word encoder our raw value needs.
* `tests/plan-f77/72-bound-driven/codegen.py` provides `BASE = 0o1757`,
  `XTA=0x008000`, `ARX=0x00b000`, `STO=0x000000`, `emit48()`, `ram()`,
  `OBJ12=0o0064200402200000` (the proven `*64 2004` print word), and
  `RET=0o6700000002200000` (`:52-75`). Tests 76, 77, 81 import them verbatim;
  test 80 adds the 58 clean words at `0o30114` (`80-high-ram-zone/README.md:5-13`).
  Reuse these constants and install recipes unchanged.

### 4.2 New IR record

FOREX 2.02 INTEGER cannot hold a 48-bit value (`docs/63-full-compiler-design.md:197`:
"Do not form a full 48-bit value in one INTEGER; always keep HI and LO separate
24-bit INTEGERs"), so the single `<value>` is spelled as two decimal 24-bit halves:

```
777006 <seq> <kind> <hi> <lo>
```

* `777006` new marker, `DATA MR6 /777006/` next to `MR1..MR5` (`FRONT.FTN:50-54`);
  FORMAT `9006 FORMAT(1X,5I8)` next to `:372-376`.
* `<seq>` source card number, so the record has a defined place in the stream.
* `<kind> 0` = one full 48-bit word, `<hi>` = bits 47..24 (left half),
  `<lo>` = bits 23..0 (right half), both decimal `0..16777215` (= 0o77777777).
  Kind 1 is reserved for "single 24-bit instruction + UTC pad" (the pascal-re
  `formAndAlign` behaviour) but is **not needed for the first implementation**.
* The IR is numeric-only and therefore satisfies `docs/63...:198`.

### 4.3 FRONT.FTN changes (smallest patch)

1. Add `PAT38(4)` = ASCII `B E S M` (66,69,83,77) near `:56-63`.
2. In the classification chain after rule 37 (`:181-187`), test `PAT38` at
   `IFIRST`; on match set `IRULE=38`.
3. For rule 38 only: starting at `IFIRST+4`, skip optional `(`, `=` and spaces;
   parse `<hi>` then a separator (`,` or space) then `<lo>` as **decimal**
   integers using the existing digit loop idiom (`:234-261`). Store in `HI/LO`
   (declare alongside `:35-36`), with range checks against 16777215.
4. At emission (`:200-207`), `IF (IRULE .EQ. 38) PRINT 9006, MR6, SEQ(I), 0, HI, LO`.
5. Count rule 38 in `NR` (`:202`) if the summary is used for validation.

No `777005` token is produced for a rule-38 line: the raw word is a statement,
not an expression RHS.

### 4.4 Codegen: placement and execution

* The codegen `emit()` functions in `tests/plan-f77/{76-runtime-xy,81-general-grammar}`
  read `777006` records the same way `run.py:72-102` reads `777005`. For each
  record compute `word = (hi << 24) | lo` (or call `cg.emit48(h>>15 &63, ...)` if
  re-encoding; direct OR is exact and preserves arbitrary opcodes) and write it
  into a **code slot inside the already-proven executable window** `body[1..0o43]`,
  `BASE=0o1757`. Free slots are `body[0o17..0o24]` and `body[0o34..0o40]`; in
  test 81 `body[14]` is already a spare word (`codegen_general.py:90`). The word
  is copied to RAM `BASE+k` by the proven installer (`76-runtime-xy/runtime_xy.py:211-242`).
* Execution is automatic: the installed stream starts at `body[9]` and runs
  sequentially through the code slots to the `*64` print (`slot 15`) and `RET`
  (`slot 16`) (evidence: `76-runtime-xy/README.md:21-24`, `80-high-ram-zone/README.md:14-16`).
  Place the raw word before the print/RET (and move RET after it if using a new
  slot) so it is executed in order. This is the analogue of pascal-re's "inline
  at the current code point"; our `777006 <seq>` ordering supplies the point.
* Because the GOST words are **zero-seeded before the run** and digits appear
  only through our ARX additions (`76-runtime-xy/README.md:3-6`, `:22-24`), any
  inserted ARX/STO word has an observable, attributable effect on the printout.

### 4.5 A/B that proves OUR inserted instruction changes the output

Primary A/B (raw `ARX`/`STO`, reusing test 81's proven digit machinery):

* Take test 81 case `X=2.0; Y=X*2.0+1.0` -> `21 02.00 05.00`
  (`81-general-grammar/README.md:26`). Its slot 14 is a spare no-op
  (`codegen_general.py:90`). Add a new data cell `A_EX = ram(0o34) = 0o2013`
  containing `1 << 40` (one unit in GOST word B byte 0, the Y-tens digit).
* **B (with our word):** a rule-38 source line supplies the raw word
  `ARX A_EX / STO A_G2`, where `A_G2 = ram(0o30) = 0o2007`:
  high half `0o132013`, low half `0o002007`, full word
  `0o0013201300002007` (decimal `hi=46091, lo=1031`). Install it in slot 14.
  Expected print `21 02.00 06.00`.
* **A (control):** identical deck, IR, descriptor and zero-seeded GOST words,
  but with the `777006` record removed (slot 14 stays the original no-op).
  Expected print `21 02.00 05.00`.
* **A' (poison control):** same record present but the target slot zeroed
  (`zero=(14,)` in the `emit()` signature, `codegen_general.py:65`). Expected
  `21 02.00 05.00`. Additionally, pre-run readback must show the Y digits still
  zero (`runtime_xy.py:244-255`) and the MTR must show the extra ARX at the new
  code address `BASE+14 = 0o1765` (its STO targets `A_G2 = 0o2007`) changing
  the accumulator from seed to the new
  digit (the MTR technique of `76-runtime-xy/README.md:22-24`).

Only the presence of the `777006`-derived word differs between A and B, so a
B-only change from `05.00` to `06.00` proves the inserted instruction, not IR
folding, caused it.

Alternative A/B (raw `*64` with our descriptor): in the 58 clean words at
`0o30114` (`N+3 = 0o2353`, test 80), install a rule-38-supplied `*64 <descriptor>`
word (the proven pattern is `OBJ12 = 0o0064200402200000`, high half `0o642004`)
instead of the hard-coded one, with the descriptor pointing at a GOST pair whose
digits differ. A: omit the raw `*64` word -> no print (test 80 already proves
"zero first word of routine -> no print", `80-high-ram-zone/README.md:32-33`);
B: raw `*64` present -> the new digits print. This is a stronger but more
expensive variant; the ARX A/B above is the recommended first gate.

---

## 5. FOREX 2.02 subset constraint and closest source spelling

`docs/63-full-compiler-design.md:198`: no `CHARACTER`, no `PRINT *`, no `SAVE`,
no `IMPLICIT`, no `nH` literals; names <= 6 chars; fixed form <= 72 columns;
`NLV <= 31`; numeric output only. `docs/63...:197` adds the 24-bit-halfword
mantissa rule. There is **no octal `B` suffix and no `besm()` in FORTRAN 2.02**;
`FRONT.FTN` itself is compiled by SYSTEM FOREX 2.02
(`FRONT.FTN:1-6`, `71-front-base77/inject.py:77-87`), so the directive must be
plain fixed-form text with decimal INTEGERs only.

Recommended source spelling (fits 72 columns, uses only uppercase letters,
digits and spaces, and remains a comment for FOREX):

```fortran
CbESM 46091 1031
```

i.e. column 1 = `C`, text starting at column 7 = `BESM <hi> <lo>`. `FRONT.FTN`
reads only columns 7..72 (`FRONT.FTN:15-16`, `:70-80`), so it sees
`BESM 46091 1031` at `IFIRST=1` and matches rule 38. FOREX ignores the card.

Host-side caveat: `tests/plan-f77/71-front-base77/inject.py:47-48` currently
drops cards whose column 1 is `c`, `C` or `*`. Retain cards beginning with
`CbESM`/`CBESM` in that filter (a one-line host change); no Fortran source or
compiler binary changes are needed. If a host change is undesirable, the
alternative spelling is a plain column-7 card `BESM 46091 1031` (valid as data
for FRONT, not compiled by FOREX in test 71's flow), but the comment-card form
is safer because the same deck stays compilable by FOREX.

Decimal `hi/lo` chosen here encode the raw BESM-6 word; this is the closest
faithful analogue of `besm(2200000B)` under the "decimal literals only" rule.
A convenience extension (FRONT accepting an optional `O` prefix and converting
octal digits to decimal internally) can be added later without changing the IR.

---

## 6. Evidence index (file:line)

* `pascal-re/comments.txt:99-119,121-146,394-400,431-436` - extensions, `:=;`,
  half-word format, object output.
* `pascal-re/AGENTS.md:138` - BESM(I) definition.
* `pascal-re/routines.txt:214,222` - `20031 procBESM`, `20767 outputObjFile`.
* `pascal-re/pascompl.cc:16,7549-7553` - dispatch; `:5044-5050` - constant
  extraction; `:1295-1326,1370-1382` - `form1Insn`/`formAndAlign`; `:906,133,92`
  - masks/UTC/ASN64; `:2137-2184` - numeric suffixes; `:6886-6889` - `:=;`;
  `:4843-4855` - `genFullExpr`; `:1284-1293` - `storeObjWord`.
* `pascal-re/pascompl.b6:35,678-697,6902,1275-1277,1291,3205,8520-8522` -
  real usages. `pasdd1.pas:126,262,786,801`; `pashelp.pas:400`.
* `pascal-re/dtran.cc:52-109` - opcode table; `decomp.pl:234` - ASN64 textual alias.
* `re-forex/src/newcomp/FRONT.FTN:15-31,50-63,65-87,124-207,208-350,372-378`.
* `re-forex/src/newcomp/EMIT.FTN:17-22,66-74`.
* `re-forex/docs/63-full-compiler-design.md:194-200`; `docs/63...:346,360`.
* `re-forex/tests/plan-f77/72-bound-driven/codegen.py:52-75`;
  `76-runtime-xy/runtime_xy.py:56-76,114-170,244-255`;
  `76-runtime-xy/README.md:3-6,21-34`; `77-ir-to-runtime/run.py:72-115`;
  `80-high-ram-zone/README.md:5-13,24-33`;
  `81-general-grammar/codegen_general.py:25-40,65-104`;
  `81-general-grammar/README.md:22-33`.

DONE
