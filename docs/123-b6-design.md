# B6: DESIGN ONLY. SOURCE-TEXT `PRINT`/`FORMAT`, `SQRT`/`ABS`/`MOD`, and `DO` into the proven B2/B3/B4 pipeline

> СТАТУС: **проект, не приёмка**. B6 описывает токены для `PRINT/FORMAT`,
> `SQRT/ABS/MOD` по имени из Fortran‑текста и `DO`; двухпроходный цикл
> по операторам (pre‑scan меток/FORMAT + основной проход) с обработкой EOF.
> Бюджет‑прогноз 40/58 N+3 + ~518/649 N+2 + ~167/998 body — INFERENCE,
> гейты B6a/B6b/B6c описаны, но не прогонялись.

> **СТАТУС: DESIGN ONLY.** No SIMH run, no repository edit, no disk/deck/image write, no C-patch. This report
> specifies B6; B5 is concurrently integrating source-text expressions. Everything below is tagged
> **[FACT]** (read from a cited doc or measured in a cited gate), **[INFERENCE]** (extrapolation from measured
> blocks), or **[DESIGN]** (a choice of this report to be frozen with B5 before code). Authoritative evidence in
> all later gates remains full SIMH printer captures; C `dispak` is oracle only.

---

## 0. Grounding and reuse rules

### 0.1 Proven inputs (all **[FACT]**)

| item | fact | citation |
|:--|:--|:--|
| B2 token word | one 48-bit word `TK(6)/SUB(6)/POS(12)/PAY(24)`, `word=(TK<<42)\|(SUB<<36)\|(POS<<24)\|PAY`; fields extracted by `aax`/`asx` masks; POS `b35..b30`=line 0..63, `b29..b24`=col-7 0..65 | docs/117 §2.1; docs/119 §1; docs/121 §1 |
| B2 token kinds | `1 LIT, 2 ID, 3 OP, 4 UOP, 5 INTR, 6 LP/RP, 7 COMMA, 8 EQ, 9 LABEL, 10 KW, 11 EOL, 12 EOF, 13 FDESC, 14 INT` | docs/117 §2.2 |
| KW subcodes | `30 PROGRAM, 31 REAL, 32 DO, 33 CONTINUE, 34 PRINT, 35 FORMAT, 36 STOP, 37 END` | docs/117 §2.2, §4.1 |
| INTR subcodes | `1 ABS, 2 SQRT, 3 MOD, 4 DSQRT(unsupported)` | docs/117 §2.2 |
| FDESC | `SUB=1 F`, PAY=`w<<8\|d`; proven masks only for `w∈{2,3,4}, d∈{1,2}` | docs/117 §2.2; docs/113 §4, §5 |
| B3 PRINT shape | `KW(34), FD(13,SUB=1), ID(2), EOL(11)`; dispatcher at N+2 off 150..254 / RAM `0o22065` | docs/119 §1, §2 |
| B4 shunting-yard | two stacks `OSTK` N+2 200..229 (floats), `OPR` 230..244; biased SP (`K_BIAS=100`) because `1+(-1)=-0` and `UZA` does not branch on `-0`; precedence `+ - =1, * / =2, '('=0`; left-associative; result × f32(10) → symbol word | docs/122 §2.2, §2.3 |
| B4 operand scaling | literal pool words are **actual** floats; evaluator multiplies final result by 10 before storing to N+2 `32+VIDX`; converter divides EST by 10 | docs/122 §2.1, §2.3 |
| Intrinsics machine routines | ABS `avx` 2 words, SQRT Newton×4 13 words, MOD bitwise AINT 9 words; 3-word N+2 `LONG UJ` dispatch table indexed by opcode; 34/58 N+3 in C4 | docs/95 §1, §4; docs/112 §2.2, §3 |
| 6-bit TEXT names | 8 codes/word, code=ASCII−0x20, space padded `0o40`; expected single-letter code = `VIDX+28`, `asx SHL42`, `arx SP7`, `aex NUM`, `uza` | docs/109 §2; docs/114 §2.4; docs/20 |
| Symbol table | name at N+2 offset `VIDX`, value at `32+VIDX`, VIDX 1..30 (X=1,Y=2,N=3,I=4 else ASCII−60) | docs/109 §1/§2; docs/117 §2.3 |
| Card buffer | RLE 8-bit ASCII at `0o64000+`, `0x80+n`=n spaces, `0x0a` pad to word, `0xff` last non-pad byte after `*END FILE`; cards contiguous on word boundaries, no fixed stride; source cols 7..72 (RLE prefix `0x86`) | docs/114 §1.1-1.3; docs/121 §1; FRONT.FTN:15-16/70-80 |
| B1 lexer reality | machine lexer reads real Fortran at `0o64012`, emits B2 one-word tokens to N+2[64..], installs name word, builds literal float, hands off via `LONG UJ 0o22065`; multi-letter names, labels, OP/LP/RP/COMMA/INTR not yet emitted | docs/121 §1, §2, §6 |
| DO countdown | `L_CNT=L_BOUND`, `arx K_DECR` (`MASK^1`, one's-complement −1), `atx L_CNT`, `uza` exit (also on `-0`); bound 2→40.00, 3→60.00, `K_DECR` patch→20.00 | docs/115 §2.2, §3.2 |
| Memory limits | N+3 58 clean words (`0o30114..0o30205`), converter 40, no N+4; N+2 649 free (0..525, 901..1023), 526..900 forbidden, short ADR via `utc 20000`/M[7]=0o20000 | docs/117 §1.1; docs/110; docs/116 |
| Body N+1 reservoir | 999/1024 words survive zero A/B (25 load-bearing); 5 largest contiguous ranges = 909 words; zeroing all 999 FAILS, keeping `body[0o26]` + zeroing 998 PASSES; all body RAM ≤ `0o21636` reachable by direct 12-bit ADR; trampolines and 8-word chains execute | docs/120 §5-§9 |

### 0.2 Reuse decisions (hard rule: reuse, do not reinvent) **[DESIGN]**

1. **B3 PRINT handler stays byte-for-byte.** All label/FORMAT work is done *before* execution; the executable
   token stream handed to B3 is exactly `KW(34), FD(13,1,w<<8|d), ID, EOL` (docs/119 §1).
2. **B4 shunting-yard stays the evaluator.** B6 adds only the INTR/COMMA cases to its dispatch; the FPU apply
   path, biased stacks, and the ×10 store are reused unchanged.
3. **Intrinsic bodies are copied verbatim** from docs/112/C4 into free N+2, not re-derived; only the *front end*
   (6-bit name compare) and the *destination* (OSTK instead of GOST print) change. This is the C7 displacement
   principle (docs/116 §1): converter alone stays in N+3.
4. **DO countdown is copied verbatim** from docs/115; only the body becomes an interpreted statement range.
5. **No new token kind is introduced** (§1.5), no new opcode, no MMU trick beyond proven `UTC`/M[7], no IR card
   on the target deck.

---

## 1. Token sequences the SOURCE-TEXT lexer must emit

### 1.1 Contract recap **[FACT]**

```
word = (TK<<42) | (SUB<<36) | (POS<<24) | PAY
POS  = (line<<6) | (col-7)        ; line 0..63, col-7 0..65
```

The encoder `dispatch_build.tok(tk,sub,pos,pay)` of docs/121 §1 is reused for every emitted word. All tables
below use the B2 kinds of docs/117 §2.2; POS is filled from the RLE byte position and is laid out but not
consumed by B3/B4 (docs/119 §1, docs/122 §6).

### 1.2 Two streams: the key interface decision **[DESIGN]**

* **RAW stream**: what the source lexer recognizes while scanning cards. It may contain `LABEL(9)`, `LP/RP(6)`,
  `COMMA(7)`, `INT(14)`, `FDESC(13)`, `INTR(5)` etc. This stream is *not* fed wholesale to B3.
* **NORMALIZED stream**: what B3/B4 actually execute. `LABEL`, `LP/RP` around FORMAT, `1X`, and FORMAT's own
  `FDESC` are consumed by the pre-pass into tables; `PRINT`'s label reference is replaced by a resolved
  `FDESC` token. The normalized stream therefore has exactly the shapes of docs/119 §1 and docs/122 §6.

This is what lets the proven handlers run unchanged while the source still says `PRINT 100,X` and
`100 FORMAT(1X,F8.2)`.

### 1.3 `PRINT 100,X` and `100 FORMAT(1X,F8.2)`

Assume `X` has VIDX 1 (first `REAL`/assignment variable, docs/109 §1). Assume FORMAT label 100 carries
`F8.2` and the projection rule of §1.5 gives `w_eff=4, d_eff=2`, PAY `4<<8|2 = 1026`.

**RAW (emitted by lexer, Pass 1):**

```
PRINT 100,X:
  KW(10, SUB=34, PAY=0)          ; PRINT
  LABEL(9, SUB=0, PAY=100)       ; format-label reference (statement label, not INT)
  COMMA(7, SUB=0, PAY=0)
  ID(2, SUB=0, PAY=1)            ; X
  EOL(11, SUB=0, PAY=0)

100 FORMAT(1X,F8.2):
  LABEL(9, SUB=0, PAY=100)       ; defining label, first token of statement
  KW(10, SUB=35, PAY=0)          ; FORMAT
  LP(6, SUB=1, PAY=0)
  FDESC(13, SUB=1, PAY=1026)     ; F8.2 projected to F4.2 (§1.5)
  RP(6, SUB=2, PAY=0)
  EOL(11, SUB=0, PAY=0)
```

`1X` is recognized and discarded (§1.5). The pre-pass stores `LABEL 100 -> packed w/d = 1026` in the label
table (§3.3); the FORMAT statement itself is a **no-op** at execution (`S_FORMAT`: skip to EOL, 2 words,
reusing the proven EOL skip).

**NORMALIZED (feeds B3 verbatim):**

```
KW(10,34,0)
FDESC(13,1,1026)                 ; resolved from label 100, NOT from inline source digits
ID(2,0,1)
EOL(11,0,0)
```

Rationale for using `LABEL(9)` rather than `INT(14)` for the `100` in `PRINT 100,X`: B2 defines TK=14 as
"integer literal (DO bound/step, repeat count)" and TK=9 as "label number" (docs/117 §2.2). A FORMAT
reference is a statement label. B3 never sees either token, so this choice costs nothing at execution.

### 1.4 Intrinsic assignments

Assume `Y` is VIDX 2, `X` is VIDX 1, literal pool index 0 holds actual float `3.0` (B4 pool convention,
docs/122 §2.1). All four assignments use the same normalized shape as B4's assignment fixture
(docs/122 §6 item 1): `ID(target), EQ, <expr tokens>, EOL`.

```
Y=SQRT(X):
  ID(2,0,2), EQ(8,0,0),
  INTR(5,SUB=2,PAY=0), LP(6,1,0), ID(2,0,1), RP(6,2,0),
  EOL(11,0,0)

Y=ABS(X):
  ID(2,0,2), EQ(8,0,0),
  INTR(5,SUB=1,PAY=0), LP(6,1,0), ID(2,0,1), RP(6,2,0),
  EOL(11,0,0)

Y=MOD(X,3.0):
  ID(2,0,2), EQ(8,0,0),
  INTR(5,SUB=3,PAY=0), LP(6,1,0), ID(2,0,1),
  COMMA(7,0,0),
  LIT(1,0,PAY=pool_index_of_3.0),
  RP(6,2,0),
  EOL(11,0,0)
```

These RAW and NORMALIZED streams are identical for assignments; B5's source-expression lexer is expected to
emit exactly these shapes (this is the joint B5/B6 freeze item). `DSQRT` would map to `INTR(SUB=4)` but is
recognized only to be rejected (§2.1, §7).

### 1.5 `DO 10 I=1,2` and `10 CONTINUE`

Assume `I` is VIDX 4 (FRONT special case, docs/109 §1). Bounds/step are TK=14 INT; the terminating label is
TK=9 LABEL (not INT).

```
DO 10 I=1,2:
  KW(10, SUB=32, PAY=0)          ; DO
  LABEL(9, SUB=0, PAY=10)        ; terminating statement label
  ID(2, SUB=0, PAY=4)            ; I
  EQ(8, SUB=0, PAY=0)
  INT(14, SUB=0, PAY=1)          ; init
  COMMA(7, SUB=0, PAY=0)
  INT(14, SUB=0, PAY=2)          ; limit
  EOL(11, SUB=0, PAY=0)

... body statements (each with its own EOL) ...

10 CONTINUE:
  LABEL(9, SUB=0, PAY=10)        ; same label; label table maps 10 -> this token index
  KW(10, SUB=33, PAY=0)          ; CONTINUE
  EOL(11, SUB=0, PAY=0)
```

Normalized stream: unchanged, except the LABEL tokens are kept as **no-ops** in the execution stream so that
the label table can point at the CONTINUE statement's LABEL token (§3.5). B3/B4 have no LABEL handler yet; a
2-word `TK=9` no-op case is added to the TK jump table (docs/117 §4.1 shape, one more table word).

### 1.6 "New token kinds?": none; three explicit DESIGN reductions

1. **No new TK/SUB for intrinsics.** B2 already defines `INTR(5)` with SUB 1/2/3. The lexer only has to
   *recognize* `SQRT`/`ABS`/`MOD` and emit the existing token (§2).
2. **No new TK for statement labels or FORMAT.** `LABEL(9)`, `KW(10,SUB=35)`, `FDESC(13)` already exist.
   `COMMA(7)` serves both FORMAT lists and `MOD` argument separation.
3. **No X-editor token for `1X`.** **[DESIGN]** `1X` is consumed by the pre-pass and discarded, because the
   GOST line already prints a separator after `21` (docs/113 §2) and adding a blank would require changing the
   proven seeded GOST word A and a new B4 gate with no benefit to the decisive observable. This is an honest
   subset reduction, not full Fortran FORMAT semantics.

**F8.2 projection (important, explicit).** **[FACT]** only `w∈{2,3,4}, d∈{1,2}` mask layouts are proven
(docs/113 §4/§5); the converter's GOST field is 2 integer + 2 fractional digits plus sign. **[DESIGN]**
`w_eff = min(w,4)`, `d_eff = min(d,2)`, with `d_eff ≤ w_eff`; `F8.2` therefore normalizes to PAY `4<<8|2`.
A genuine 8-column field needs four extra blank GOST positions and new masks; that is a future B4-type gate,
not invented here. The same rule applies to `F8.1` → `4<<8|1` (used by gate B6a-B).

---

## 2. Machine-code design: recognizing intrinsic NAMES and emitting INTR tokens

### 2.1 6-bit TEXT constants for the three names **[DESIGN, mechanism from FACT]**

Code = ASCII−0x20, 8 codes per 48-bit word, MSB first (docs/109 §2, docs/20). Padded with space code `0o40`.
Computed constants (each 6-bit code is two octal digits):

```
TXT_ABS  = 0o4142634040404040     ; A=0o41, B=0o42, S=0o63, then 5 spaces
TXT_SQRT = 0o6361626440404040     ; S=0o63, Q=0o61, R=0o62, T=0o64, then 4 spaces
TXT_MOD  = 0o5557444040404040     ; M=0o55, O=0o57, D=0o44, then 5 spaces
```

These are the direct generalization of docs/114 §2.4: that report computed the expected code as `VIDX+28`
for one-letter names; for 3-4 letter names we store the expected word as an inline N+2 constant. The
**compare instruction chain is identical** (`aex` XOR, `uza` match), so no new opcode and no new addressing
mechanism is introduced.

### 2.2 Recognition in the lexer **[DESIGN]**

1. While scanning bytes of a statement (§3.2), an alphabetic run of ≥3 characters followed (after RLE spaces)
   by `(` is an intrinsic *candidate*. Single-letter names continue on the proven `VIDX+28` path.
2. Build a 48-bit TEXT word from the next 8 source bytes: for byte `i`, `code = byte − 0x20` (reuse the
   `aax M8`/`arx NEG31`-style ASCII-to-value chain of docs/114 §2.3), shift left by `6*(7−i)` using
   `asx (64−6*(7−i))<<41` (the `K_SHL42=(64-42)<<41` idiom of docs/114 §2.5) and OR with `aox`
   (`0o15 aox`, proven in docs/95 §1 MOD mask construction). Missing bytes at a word tail are padded with
   `0o40`, not with `0x0a` pad. **[INFERENCE]** the specific shift-control encoding for 6-bit steps is
   extrapolated from the cited 42-bit idiom; verify at B6b with C-oracle MTR.
3. Compare the built word against `TXT_SQRT`, `TXT_ABS`, `TXT_MOD` with three `aex`/`uza` pairs (or a 3-word
   expected-value table and one loop, same technique as docs/112's 3-word dispatch table). Cost estimate
   **[INFERENCE]**: ~12-16 halfwords (6-8 N+2 words) plus the 3 constants.
4. On match `i`, emit `INTR(5,SUB=i,PAY=0)` with the proven `tok()` encoder, then continue lexing `(`,
   arguments, `)`. No VIDX is allocated and no symbol-table name word is installed for an intrinsic name.
   `DSQRT(SUB=4)` is recognized and routed to a deferred/reject stub (§7), never executed.
5. **Disambiguation**: if the 3-4 letter name does not match any constant, it is treated as an unknown
   identifier (VIDX lookup path) and the following `(` is a syntax error in the supported subset
   **[DESIGN]**. Fortran's "intrinsics as external procedures" route (docs/112 §1.2) is out of scope.

### 2.3 Feeding the INTR token into the shunting-yard **[DESIGN, extends B4 minimally]**

B2 §3.1 said `INTR=3` "applied immediately to the single top operand". **[DESIGN refinement]** Fortran
function syntax is `NAME(args)`, so INTR is a **prefix operator bound to the matching `)`**, with arity from
SUB: ABS/SQRT arity 1, MOD arity 2. This is required for `MOD(X,3.0)` and does not change the arithmetic
precedence of operators *inside* the parentheses.

Minimal B4 changes:

* **OPR entries become full token words** (`TK<<8 | SUB`, or simply the B2 word) instead of bare SUB codes.
  The existing 15-word `OPR` stack is reused; no new stack. **[INFERENCE]** this is necessary because bare
  SUB codes collide: intrinsic ABS SUB=1 would be indistinguishable from binary `+` SUB=1. The B2 token
  already carries TK+SUB, so this is a 1-2 word change per push/pop site.
* `LP` pushes marker `TK=6,SUB=1` (precedence 0); `RP` pops/applies to the marker, discards it, then if the
  next OPR entry is an INTR marker, pops it and applies the intrinsic to the OSTK top(s).
* `COMMA(TK=7)`: no-op for the operator stack (just `uj E_NEXT`) **[DESIGN]**; it separates MOD's two
  operands, which both remain on OSTK (`X` below, `3.0` on top). Ignored harmlessly elsewhere; COMMA outside
  an intrinsic is not diagnosed in the subset.
* Precedence table extended: `INTR` marker = 4 (highest), applied only at its matching `RP`; `'+' '-' = 1`,
  `'*' '/' = 2`, `'(' = 0` unchanged (docs/122 §2.2). Left associativity unchanged.

At `RP` for `MOD(X,3.0)`: pop `b=3.0`, `a=X`, compute `a mod b` with the verbatim MOD bitwise-AINT path
(docs/95 §1), push result back on OSTK. For ABS/SQRT: pop/operate/push one value.

### 2.4 Intrinsic dispatch table and routine placement **[DESIGN]**

* 3-word N+2 table `ITAB[0..2] = LONG UJ <ABS|SQRT|MOD entry>`, indexed by token SUB (`ITAB_base−1 + SUB`),
  reusing docs/112 §2.2's `uj (base)(reg)` trampoline technique.
* Routine bodies live in **N+2**, copied verbatim from C4: ABS 2 words, SQRT 13 words, MOD 9 words
  (27 words + the 3 table words). **[FACT]** C4 measured these sizes; **[FACT]** N+2 instruction fetch is
  proven (`MTR 22147L uj 30114`, docs/114 §2.1; B3/B4 execute entirely from N+2). They are **not** placed in
  N+3: converter 40 + decode 4 + ABS 2 + SQRT 13 + MOD 9 = 68 > 58 (docs/115 §4.4 item 4).
* Operands and temporaries reuse the N+2 cells of C4 (`XABS/XSQRT/XMOD/YMOD/RES/Q/MASKC/...`); a MOD call
  takes `b` from OSTK top and `a` from OSTK top−1, storing them into those cells before the verbatim routine.
* Registers M[7]/M[12] are rearmed from low-RAM `HALF` after every converter call, exactly as B3/B4 do
  (docs/119 §5, docs/121 §2).

### 2.5 Where results land: precise contract **[DESIGN]**

1. **Immediate destination: OSTK top.** Each intrinsic ends with `atx OSTK(SP_O)` (after re-arming M[7]),
   *not* with a GOST conversion and *not* with `atx EST`. No `vjm 30114` occurs inside an intrinsic.
2. **Assignment destination: symbol table.** At the assignment's `EOL`, B4's unchanged finalization
   multiplies the single OSTK result by `K_TEN` (f32(10)) and stores it to N+2 `32+VIDX_Y`
   (docs/122 §2.3). Thus `Y=MOD(X,3.0)` with X=7.0 leaves `N+2[34] = f32(10.0)`.
3. **Print destination: EST only via B3.** The subsequent `PRINT 100,Y` reads `N+2[32+VIDX_Y]` into EST,
   seeds GOST words `0o2006/0o2007`, applies the resolved width masks, and calls the verbatim converter
   through VJM (docs/119 §3.4, docs/113 §2). The sign convention is the inherited one (docs/122 §5).
4. **[FACT]** No host-computed digit appears anywhere: every printed digit comes from the BESM-6 FPU/bitwise
   routines and the verbatim converter.

---

## 3. Statement-loop design: next statement, labels, EOF (closes the B2 open item)

### 3.1 Two passes over the card buffer **[DESIGN]**

B2 §5.2 records the open item: proven scanners process a fixed count of records and never test `0xff`. B6
closes it with two linear passes, both driven by a card-word pointer `C_PTR` held in an N+2 cell:

* **Pass L (label/FORMAT pre-scan).** Walk all source cards; decode only leading labels, `FORMAT` keywords,
  and `Fw.d` digits. Fill the label table. Emit nothing. This solves "FORMAT after PRINT" without changing
  B3's PRINT handler.
* **Pass E (emit + execute).** Walk the same cards again, emitting B2 tokens into the token buffer and then
  executing the normalized stream with `SPC` as program counter.

Cost **[INFERENCE]**: Pass L reuses the docs/104 digit chain and the docs/114 marker/byte scanners; ~40-70
N+2 words. The card buffer is read-only throughout.

### 3.2 Finding the next statement after end-of-line **[DESIGN, built on FACT]**

Registers: `M[10]=C_PTR` (start `0o60000`, so `xta 4012(10)` reads RAM `0o64012`), `M[11]`=byte index into
the fetched word, `M[12]=M[7]=0o20000` (N+2 base / short-branch base). This is exactly the B1/B2/C2b wiring
(docs/121 §2, docs/114 §2.2).

Per card word:

```
NEXT_CARD:
  xta 4012(10)                 ; current card word (C_PTR holds card-word address - 0o40000)
  ... test 6 bytes for 0xff -> CARD_EOF (§3.4)
  ; first word of a statement: byte0 should be 0x86 (6 blanks = cols 1..6)
  ; decode bytes 1..5 (then subsequent words) through the proven byte-extraction table
  ;   utc 20000 + asx SHRTAB(13) for N+2 tables; card bytes via M[11] index
  ; RLE: byte 0x80+n means n spaces; advance logical column by n
  ; emit tokens for non-space bytes; maintain COL (starts at 7) -> POS
  ; when byte 0x0a (word pad) is seen: emit EOL, C_PTR += 1, uj NEXT_CARD
```

Facts behind each rule:

* **[FACT]** cards are contiguous with no fixed stride; each starts at the next word boundary, padded with
  `0x0a` (docs/114 §1.2). Therefore "advance to the first word containing a `0x0a` pad, then +1" lands on the
  next card without assuming a stride.
* **[FACT]** a normal source card starts with RLE `0x86` (6 spaces) in byte 0 (docs/121 §1: `86 58 3d ...`
  for `X=12.34`). Byte 1 is physical column 7.
* **[FACT]** trailing spaces are one RLE byte (e.g. `0xc6`=70 spaces, docs/121 §1) immediately before `0x0a`,
  so the end-of-card test still sees `0x0a` in the same word.
* **[DESIGN]** continuation cards (physical col 6 nonblank, i.e. byte0 ≠ `0x86`) are **rejected** in the B6
  subset: detect byte0 `0x85` + nonblank and stop with a machine-visible no-go. The supported deck has one
  statement per card in cols 7..72. Supporting continuation later means withholding EOL and continuing the
  same statement across cards, with a token-buffer overflow check.

### 3.3 Statement labels **[DESIGN]**

* At `COL=7`, accumulate consecutive digit bytes using the proven 4-digit chain of docs/104/114
  (`asx SR24/SR16/SR8`, `aax M8`, `arx NEG31`, `10*T[]`). When a non-digit is reached, emit
  `LABEL(9,SUB=0,PAY=label)` as the statement's first token.
* **Label table** in N+2 (and/or mirrored in N+1 bulk, §4): pairs `(label, token_index_of_statement_start)`.
  Pass L fills it; Pass E uses it:
  * `PRINT n` → look up `n`, fetch the stored packed `w/d` → emit `FDESC(13,1,packed)` in the normalized
    stream (§1.2). Missing label = machine-visible no-go.
  * `DO n` → store `L_END = token_index(LABEL n)` in the DO control cells.
  * A `LABEL` token in the execution stream is a no-op; it exists so `L_END` has a concrete target.
* **[FACT]** the on-machine digit-to-value chain and the 2-digit VIDX/name compare are proven in
  docs/114 §2.3-2.4; labels are integers <2^24 and fit PAY (docs/117 §2.2).

### 3.4 Reaching EOF **[DESIGN, closes B2 §5.2]**

Two independent terminators, both returning to the resident via the proven `uj 0(15)` path (docs/119 §4):

1. **Logical**: execution of `KW(37) END` (or `STOP` treated as END) stops interpretation. This is the normal
   path and already proven in B3/B4.
2. **Physical**: while advancing `C_PTR`, test each fetched word's six bytes for `0xff`. On a match, jump to
   `CARD_EOF`: finish tokenizing any partial statement, then take the same return path even if no `END` card
   was present. **[FACT]** `0xff` is the last non-pad byte after `*END FILE` (docs/114 §1.2, :89-101).
   **[INFERENCE]** `0xff` is also the RLE encoding of a 127-space run (`0x80+127`); that run cannot occur in
   cols 7..72 of our decks, and the `*END FILE` framing is the primary terminator, so the overload is safe
   here. This nuance must be re-checked if arbitrary decks are admitted.
3. **Guard**: a hard cap on scanned card words (e.g. 1024) prevents an unterminated scan from looping forever.
   This is a mechanism guard, not a Fortran feature.

### 3.5 The execution-side statement loop and DO rewind **[DESIGN]**

* `SPC` = token index into the token buffer. At `EOL`, the dispatcher increments `SPC` and jumps to the token
  fetch (B3's proven loop, docs/119 §4.2 "multiple statements"). This is the interpreted program counter that
  replaces the fixed 2/6-record unrolled loops of C2b/C7.
* `S_DO` consumes `LABEL, ID, EQ, INT, COMMA, INT, EOL`: set `L_BOUND=limit`, `L_STEP=1`, `L_CNT=L_BOUND`,
  optionally seed the loop variable's value word to `f32(10*init)` (symbol words hold 10× value, §0.1);
  set `L_BODY = SPC after DO` and `L_END` from the label table (§3.3); `SPC=L_BODY`.
* `S_CONT` (docs/115 §2.2 verbatim): `L_CNT = L_CNT + K_DECR` (`K_DECR=MASK^1`); `uza S_AFTER_LOOP`
  (terminates also on `-0`); else optionally add `f32(10)` to the loop variable, then `SPC=L_BODY`.
  `S_AFTER_LOOP`: `SPC = L_END + 2` (past CONTINUE's LABEL and EOL).
* **[FACT]** countdown/`uza`/-0 behaviour proven in docs/115 §2.2/§3.2. **[INFERENCE]** applying it to an
  interpreted *range* with `SPC` rewinding is new; step>1 and nested DO are deferred (§7).

---

## 4. Word-budget projection: body N+1 (998) + N+2 (649) + N+3 (58)

### 4.1 FACT baselines

| region | measured fact | source |
|:--|:--|:--|
| N+3 | 58 clean words; canonical converter 40/58 (34+? in C4 variant); converter 40 + C4 intrinsics 34 would need 68 → overrun | docs/117 §1.1; docs/112 §2.3; docs/115 §4.4 |
| N+2 | 649 free, 526..900 forbidden (0 writes); measured footprints C2b 161, C6 165, C7 177, B3 256, B1+B3 370, B4 464 | docs/110; docs/114 §4.1; docs/115 §2.3; docs/116 §2; docs/119 §3; docs/121 §5; docs/122 §3 |
| N+1 | 999/1024 survive zero A/B; 25 load-bearing; 5 largest ranges 282+239+239+104+45=909; zero-all-999 FAILS, `body[0o26]` kept + 998 zeroed PASSES; max RAM `0o21636` ≤ `0o7777`; trampolines + 8-word chains execute | docs/120 §5-§9 |
| N+1 currently used by our contour | entry `body[0o11]`, GOST seeds `body[0o27..0o32]`, 30 converter data cells `body[0o110..0o135]`; keeper `body[0o26]` preserved | docs/122 §3; docs/120 §8 |

### 4.2 B6 allocation **[INFERENCE / DESIGN, not built]**

| region | allocation | words | tag |
|:--|:--|--:|:--|
| N+3 | verbatim docs/105 converter + `floor_int` at `0o30114`, unchanged; 18 spare as reserve | 40 / 58 | FACT baseline, DESIGN placement |
| N+2 hot data | symbol table 63, OSTK 30, OPR 15, constants 30 (masks, shifts, bias, K_TEN, K_DECR, TEXT names, ITAB) | ~138 | INFERENCE from docs/117 §2.4 + docs/122 §3 |
| N+2 hot code | B4 evaluator + B3 dispatcher (reused, ~203), source lexer ~70, label/FORMAT pre-pass ~40, intrinsic name compare ~10, intrinsic routines 27 + ITAB 3, DO handler ~20, TK=9 no-op/entry glue ~8 | ~380 | INFERENCE from docs/122 §3 (203 measured) + C4 §2.2 (27 measured) |
| N+2 subtotal | hot data + hot code, all within offsets 0..525 | **~518 / 526 contiguous free** | INFERENCE |
| N+1 bulk | token buffer 117 + label/FORMAT table 30 → `body[0224..0602]` (239 free, RAM `0o2223..0o2601`); literal pool 20 + overflow code → `body[0604..1235]` (282 free, RAM `0o2621..0o3252`); direct 12-bit ADR, no UTC needed | **~167 / 998** | INFERENCE from docs/120 §6/§9 |
| N+1 preserved | all 25 load-bearing words and keeper `body[0o26]` untouched; zone checksum recomputed by the proven `wz()` writer | 0 changed in forbidden set | FACT rule, DESIGN compliance |
| N+2 forbidden band 526..900 | never written | 0 / 0 | FACT rule |
| N+2 high band 901..1023 | spare spill if N+2 code exceeds 526; reachable by M[7]=0o20000 short ADR (docs/110) | 0 planned | INFERENCE |

**Total projection: N+3 40/58, N+2 ~518/649 (of which ~518 in the contiguous 0..525 band), N+1 ~167/998,
0 writes to 526..900 or to the 25 load-bearing body words.** All numbers except the cited baselines are
**[INFERENCE]** and must be replaced by measured build counts at B6a/B6b/B6c.

### 4.3 Risk statement **[INFERENCE]**

* If B5's source-expression lexer exceeds ~70 words, N+2 hot code crosses 526 and must spill to 901..1023
  (proven reachable but not yet used for code in a product) or into N+1. B6a must measure before B6b starts.
* Full N+1 program executability was proven only for 8-word chains, not a 282-word program (docs/120 §7/§10);
  placing *bulk data* (token/label/literal tables) there is low-risk, placing large *code* there is the
  unproven fallback. This design keeps all hot code in N+2 to avoid that inference.
* The docs/120 aggregate caveat is respected by preserving `body[0o26]` and writing real code/data rather than
  blanket zero fill.

---

## 5. Staged gates B6a → B6c with decisive deck A/B criteria

### 5.1 Common gate discipline **[FACT from docs/74/75/110/114/116/118]**

Each gate is full SIMH A/B/PATCH/RESTORE (+ ORDER where noted) with the b-harness (`drive_b.py`,
product_gate and plumbing PASS), one invariant deck, image changed one word at a time, every job ending in
`КОНЕЦ ЗАДАЧИ`. Budgets: N+3 ≤ 58, N+2 ≤ 649 with 0 changed offsets 526..900, N+1 keeper and 25 load-bearing
words preserved. C-oracle MTR/CORE is advisory evidence only. No host-computed result digit anywhere. The
printer `21` line and its spacing are the decisive observable.

### 5.2 B6a: source `PRINT`/`FORMAT`, label resolution

Deck (real Fortran, cols 7..72, no IR cards) includes `X=12.34`, `PRINT 100,X`, `100 FORMAT(1X,F8.2)`,
`END`. FORMAT is placed *after* PRINT to prove the pre-pass.

| gate | change | decisive printer line | verdict |
|:--|:--|:--|:--|
| A | baseline deck | `21 -0012.34  3000.00` (+ `КОНЕЦ ЗАДАЧИ`) | PASS |
| B | **byte-identical image**; one deck digit `F8.2`→`F8.1` (projected `F4.1`) | `21 -0012.3   3000.00` (spacing changes) | PASS |
| PATCH | deck A; one N+2 width-mask word `0→0o7417` (w=2 mask, docs/113 §2) | `21 -  12.34  3000.00` | PASS |
| RESTORE | image byte-identical to A, deck A | `21 -0012.34  3000.00` | PASS |

**Decisive criterion:** with the image frozen, changing only FORMAT digits in the source changes printed
spacing; with the deck frozen, changing only one mask word of OUR table changes it; restore returns.
**No-go** if the label-100 resolution is wrong, if `1X` handling shifts the sign byte, or if F8.2 projection
is not exactly the agreed `4<<8|2`.

### 5.3 B6b: source-text intrinsic names

Three sub-cases reuse the B6a print path unchanged.

| gate | deck source (image byte-identical for A/B) | printer line | verdict |
|:--|:--|:--|:--|
| SQRT A | `X=16.0`, `Y=SQRT(X)`, `PRINT 100,Y` | `21 -0004.00  3000.00` | PASS |
| SQRT B | one deck digit `16.0`→`9.0` | `21 -0003.00  3000.00` | PASS |
| NAME B' | `SQRT`→`ABS` (same X=16.0), proves the 6-bit name compare, not just the value | `21 -0016.00  3000.00` | PASS |
| ABS A | `X=0.0-9.0`, `Y=ABS(X)` (binary minus produces the negative float; no unary-minus dependency) | `21 -0009.00  3000.00` | PASS |
| MOD A | `X=7.0`, `Y=MOD(X,3.0)` | `21 -0001.00  3000.00` | PASS |
| MOD B | one deck digit `3.0`→`4.0` | `21 -0003.00  3000.00` | PASS |
| PATCH | deck SQRT A; one N+2 `ITAB[1]` word changed from SQRT trampoline to ABS trampoline | `21 -0016.00  3000.00` | PASS |
| RESTORE | byte-identical to A | `21 -0004.00  3000.00` | PASS |

**Decisive criterion:** changing the *source name* changes which of the three verbatim machine routines runs;
changing one dispatch-table word changes the result under a frozen deck; values are computed by BESM FPU
bits (MTR must show `avx` / Newton `a/x,a+x,a*x` / bitwise AINT at our N+2 PCs). **No-go** if the 6-bit
compare misidentifies a name, if OPR entry collision (SUB=1 `+` vs ABS) appears, or if a result is printed
from inside the intrinsic instead of via the assignment/PRINT path.

### 5.4 B6c: source `DO`/`CONTINUE`, statement loop, EOF

Deck:

```
      PROGRAM MAIN
      S=0.0
      DO 10 I=1,2
      S=S+2.0
   10 CONTINUE
      PRINT 100,S
  100 FORMAT(1X,F8.2)
      END
```

| gate | change | decisive printer line | verdict |
|:--|:--|:--|:--|
| A | bound 2 | `21 -0004.00  3000.00` | PASS |
| B | **byte-identical image**; one deck digit bound `2`→`3` | `21 -0006.00  3000.00` | PASS |
| PATCH | deck A; one N+2 `K_DECR` word `MASK^1`→`MASK^2` (docs/115 §3.2) | `21 -0002.00  3000.00` | PASS |
| RESTORE | byte-identical to A | `21 -0004.00  3000.00` | PASS |
| EOF case | same deck with `END` removed, image unchanged | job still reaches `КОНЕЦ ЗАДАЧИ` via the `0xff`/`*END FILE` scan, with the same value line | PASS |

**Decisive criterion:** the iteration count comes from the source bound and from OUR counter word; `SPC`
rewinds to `L_BODY` and exits at `L_END`; the EOF case proves the B2 open item is closed. **No-go** on a
hang, on missing `КОНЕЦ ЗАДАЧИ`, on an off-by-one iteration, or on any write to N+2 526..900 / to a
load-bearing body word.

### 5.5 Stage order and freeze points

* **B6a first** because it fixes the RAW→NORMALIZED stream contract and measures the real lexer/pre-pass
  word count (§4.3). B5 must have frozen the expression token shapes (§1.4) before B6a runs.
* **B6b second** because it depends on B4's OPR-entry extension (§2.3); if B5 implemented a different pending-
  intrinsic mechanism, B6b is where the joint contract is verified, not assumed.
* **B6c last** because it exercises the full statement loop, label table, and EOF together.

---

## 6. FACT / INFERENCE summary

**FACT (cited or measured):** B2 token word/kinds/KW codes; B3 PRINT shape and dispatcher; B4 two-stack
evaluator, biased SP, ×10 store; ABS `avx` / SQRT Newton / MOD AINT and 3-word dispatch; 6-bit TEXT names,
`VIDX+28` expected code and `aex`/`uza` compare; N+2 symbol layout and 649/526..900 map; RLE card buffer,
`0x86` prefix, `0x0a` pad, `0xff` last byte, no fixed card stride; N+3 58/40 limits and N+1 999/998/25/909
measurements; DO countdown and one-word counter patch; all cited gate SHAs, byte diffs, and printed lines.

**INFERENCE / DESIGN (not built here):** RAW vs NORMALIZED two-stream architecture; F8.2→F4.2 projection and
`1X` suppression; inline TEXT constants for SQRT/ABS/MOD and the 6-bit shift-control encoding; OPR entries as
full token words and INTR-as-prefix-with-arity; two-pass card scan, `C_PTR`+`0x0a` next-card rule, label
table, EOF scan and 1024-word guard; DO over an interpreted range with `SPC` rewind and optional loop-variable
update; all B6 word-count projections and the N+1 placement; all B6a/B6b/B6c expected printer lines.

**Not claimed:** any SIMH result, any repository/disk/deck write, any implementation of Fortran source parsing
in this report, full `Fw.d` semantics, general DO (step≠1, nesting), DSQRT, formatted READ, continuation cards,
or a native FRONT intrinsic/FORMAT/DO emitter.

---

## 7. Deferrals and hard limits carried forward **[FACT, from docs/106/112/115/117]**

1. DSQRT/double precision: no double FPU, software DP >100 instructions, out of scope.
2. Formatted `READ(u,fmt)`: monitor-owned input context, blocked.
3. Resident FT* MMU pages: blocked; we use our own N+3 converter.
4. Full `Fw.d`: only `w∈{2,3,4}, d∈{1,2}`; F8.2 is projected (§1.6).
5. DO step≠1, nested loops, general loop-variable semantics: deferred; countdown only.
6. Continuation cards and arbitrary decks: rejected/diagnosed in the B6 subset (§3.2).

DONE
