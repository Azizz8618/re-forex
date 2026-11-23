# Variant B — machine-code Fortran-77 source parser for the zone-2350 contour

> СТАТУС: **проект, не приёмка**. B2 дал формат токена (одно 48‑битное слово:
> TK/SUB/POS/PAY), shunting‑yard с двумя стеками в N+2 и dispatch операторов
> `PROGRAM/REAL/= /PRINT/FORMAT/DO/CONTINUE/END`. FRONT полностью вне target‑path.
> Всё, что касается суммарного бюджета ~515 слов N+2 и композиции width/sign,
> помечено INFERENCE и подлежит проверке гейтами B3–B5. Главный открытый
> пункт — цикл по операторам, управляемый EOF.

DESIGN ONLY. No SIMH run, no repo edit, no disk/image/deck write was made for this
report. Everything below is either cited FACT from the repository docs or an
explicitly labelled INFERENCE / design choice.

Deliverable feeds B1 (lexer) and B3-B5. "Variant B" = the target deck carries
**real fixed-form Fortran source** (cols 7..72), our zone-2350 machine code reads
and executes it. There are **no 777005 IR cards** in the target deck, no
`*FOREX`/`*FTN`, no `*perso` on the main path. FRONT is not on the target path at
all; it is at most a build-time helper and is irrelevant to this design.

---

## 0. What is fact vs what is being designed

| tag | meaning |
|:--|:--|
| **[FACT]** | read directly from a cited file/line or a proven SIMH/C-oracle result |
| **[INFERENCE]** | extrapolation from measured building blocks; not built or run here |
| **[DESIGN]** | a choice of this report; to be frozen jointly with B1/B3-B5 before code |

The proven building blocks are real and measured, but the *composition* into a
source-to-execution parser is new. The largest risk is not feasibility of any
single block (all are proven) but the word budget of the combined interpreter
(Section 3.5) and the absence of an EOF-driven statement loop (Section 5.2).

---

## 1. FACT baseline (grounding)

### 1.1 Entry and memory

* **[FACT]** The contour is entered at RAM `0o1770` by a same-length substitution
  in body zone `0o2351`, `body[0o11] = LONG UJ 0o30114`
  (docs/89:37-41; docs/95:42-43; docs/116:79-80).
* **[FACT]** Zone N+3 word `k` maps to RAM `0o30114 + k`; only **58 clean words**
  `0o30114..0o30205` arrive at our entry. Zones N+4..N+40 have no RAM image at
  our entry (docs/65:28-48; docs/101:36-38; docs/106 §1).
* **[FACT]** Zone N+2 free words: offsets `0..525` -> RAM `0o21637..0o22654`
  (526 words) and offsets `901..1023` -> RAM `0o27721..0o30113` (123 words),
  **649 total**. Offsets `526..900` are load-bearing overlay data and must never
  be written (docs/110:64-69, :94). Recommended conservative table range:
  N+2 offsets `0..255` -> RAM `0o21637..0o21736` (docs/110:85-93).
* **[FACT]** A bare 12-bit ADR cannot reach these addresses; the proven mechanism
  is `UTC 20000` arming M20 for exactly the next instruction, followed by a short
  ADR (`xta 1637` -> `0o21637`), or installing M[7]=0o20000 as a short-ADR base
  (`vtm 20000(7)`; `xta 1640(7)` -> `0o21640`) (docs/110:96-111; docs/111:117;
  docs/113:90-93). The modifier is consumed by one instruction.
* **[FACT]** N+3 hot path in the canonical product: the verbatim docs/105 ABS +
  2+2 GOST + sign converter is **40 words / 80 halfwords** (74 converter
  halfwords + pad + 6 `floor_int` halfwords), called as a VJM subroutine; resident
  `*64 2004` prints (docs/105:45-56; docs/116:67-71). This leaves **18 words**
  (36 halfwords) of N+3 for an entry stub.
* **[FACT]** Link-register convention that avoids collisions: outer calls use
  M[9(dec)] (`(11)` in MTR), the converter's internal `floor_int` uses M[11(dec)]
  (`(13)`), and M15 is the resident return link `0o1764` (docs/114:112-115).

### 1.2 Card buffer and source layout

* **[FACT]** The dispak card buffer is RLE-packed 8-bit ASCII at RAM `0o64000+`,
  6 bytes per 48-bit machine word; byte `0x80+n` denotes `n` spaces; `0x0a` pads
  the tail of a card to a word; `0xff` is the last non-pad byte after `*END FILE`
  (docs/114:45-51, :85-90; docs/104:64-68).
* **[FACT]** Cards are contiguous; each starts at the next word boundary; there
  is **no fixed stride**. The proven scanner searches for the marker word
  `0o823737373030` rather than assuming a stride (docs/114:76-90, :92-103,
  :132-138).
* **[FACT]** FRONT (build-time) reads physical columns `7..72` (`LW=72`), with
  continuation when physical column 6 is nonblank (`FRONT.FTN:15-16`, `:70-80`,
  cited in docs/71:308-309; `src/newcomp/FRONT.FTN` lines 70-92). In the RLE
  buffer a normal source card therefore begins with a `0x86` run (6 spaces) in
  byte 0 of its first word, then the statement text.
* **[FACT]** A real Fortran source card in the buffer decodes as e.g.
  `0o64007..0o64011 = "      PROGRAM MAIN"` (docs/114:59-61).

### 1.3 Proven machine primitives we will reuse (not reinvent)

| primitive | fact source |
|:--|:--|
| 6-bit TEXT names: 8 codes per word, code = ASCII-0x20, padded with `0o40` (space) | docs/109:99-100; docs/20:26,44,54 |
| N+2 symbol table: name at offset `VIDX`, value at `32+VIDX`, VIDX 1..30, X=1/Y=2/N=3/I=4 else ASCII-60 | docs/109:47-60, :81-104; docs/114:167-168 |
| On-machine 6-bit name compare: expected code = `VIDX+28`, `asx SHL42`, `arx SP7`, XOR, `uza` | docs/114:154-163 |
| 4-digit literal read and float build: `asx SR24/SR16/SR8`, `aax M8`, `arx NEG31`, `10*T[]`, `e+x`, `*100`, `/10` | docs/104:30-38; docs/114:145-150 |
| FPU dispatch by opcode: 4-way word-aligned `uj` jump table, `uj (base)(reg)` word-addressed | docs/111:86-104, :106-113 |
| ABS `avx` (NOT sign-bit clear; negative floats are two's-complement mantissa), SQRT Newton x4 (13 words), MOD bitwise AINT (9 words) | docs/95:61-108, :199-204 |
| float -> GOST: `aex`/`e+x` derive asx control, `aax MASK40`, `asx` digit, `asx CW_L16`, `arx 2006`, `*64 2004` | docs/89:43-88; docs/95:50-54; docs/105:104-118 |
| GOST sign from float bit 40, flipping GOST byte 3 (`15` space <-> `11` minus) | docs/105:29-43, :119-120; docs/90 sign not implemented without it |
| Multi-record RLE card scanner, re-arming M[12]/M[7]/M[10] every step | docs/114:130-143; docs/116:82-86 |

### 1.4 Proven word budgets (measured, not estimated)

| configuration | N+3 | N+2 | source |
|:--|--:|--:|:--|
| canonical 4-digit LIT + sign | 57/58 | small | docs/105:45-56 |
| LIT + VARIABLE + `*` (C3) | 51/58 | 5 words | docs/111:179-185 |
| intrinsic dispatch ABS/SQRT/MOD (C4) | 34/58 | 3 + operands | docs/112:105-132 |
| FORMAT width w/d (C5) | 54/58 | 8 words | docs/113:150-155 |
| multi-record scanner + two-digit VIDX (C2b) | 40/58 | 161 words | docs/114:241-248 |
| DO countdown fixture (C6) | 40/58 | 165 words | docs/115:152-160 |
| **all C1-C6 integrated (C7)** | **40/58** | **177/649** | docs/116:88-97 |

C7 is the decisive precedent: **all front ends fit when only the converter stays
in N+3 and everything else is displaced into (free) N+2** (docs/116:56-61). This
is the architecture adopted here.

---

## 2. Token format and symbol table (contract for B1)

### 2.1 Token word — [DESIGN, to be frozen with B1]

One token = **one 48-bit BESM word = two 24-bit halfwords**. Fields are aligned
so extraction uses only the proven `aax` (AND) + `asx` (shift) primitives.

```
48-bit word, bits b47 (MSB) .. b0 (LSB); L half = b47..b24, R half = b23..b0

  b47..b42 (6 bits)  TK     token kind            (1..14, Table 2.2)
  b41..b36 (6 bits)  SUB    subcode               (op / intrinsic / stmt / editor id)
  b35..b24 (12 bits) POS    source position       b35..b30 = line 0..63
                                                   b29..b24 = col-7 0..65 (cols 7..72)
  b23..b0  (24 bits) PAY    payload               VIDX, literal-pool index, label,
                                                   packed w/d, or small integer

Word layout by halfword:
  L = {TK:6, SUB:6, POS:12}
  R = {PAY:24}
```

Extraction (instruction-level, proven shift-control form `(64+n)<<41`):

```
; mask constants (48-bit octal, 16 octal digits)
M_TK   = 0o7700000000000000        ; b47..b42
M_SUB  = 0o0077000000000000        ; b41..b36
M_POS  = 0o0000777700000000        ; b35..b24  (written as 0o0000777700000000)
M_PAY  = 0o0000000077777777        ; b23..b0
SR42   = (64+42)<<41  ; SR36=(64+36)<<41 ; SR24=(64+24)<<41

  xta TOKEN(7)                    ; word from token buffer (M[7]=0o20000 base)
   aax M_TK                       ; isolate TK
   asx SR42                       ; TK in low 6 bits
   atx TKCELL
   xta TOKEN(7)
   aax M_SUB
   asx SR36                       ; SUB in low 6 bits
   atx SUBCELL
   xta TOKEN(7)
   aax M_PAY                      ; PAY (24 bits) - no shift needed
   atx PAYCELL
```

**[INFERENCE]** All three masks are plain bit patterns; `aax`/`asx` with a
control word are proven in docs/109:114-119 and docs/114:147-149. No new opcode
is introduced.

### 2.2 Token kinds — [DESIGN]

| TK | name | SUB | PAY |
|--:|:--|:--|:--|
| 1 | LIT (real literal) | 0 | index into literal pool (N+2 array of BESM floats, pre-scaled for the converter) |
| 2 | ID (variable) | 0 | VIDX 1..30 |
| 3 | OP (binary) | 1 `+`, 2 `-`, 3 `*`, 4 `/` | 0 |
| 4 | UOP (unary) | 6 unary `-`, 7 reserved | 0 |
| 5 | INTR | 1 ABS, 2 SQRT, 3 MOD, 4 DSQRT(unsupported) | 0 |
| 6 | LP / RP | 1 `(`, 2 `)` | 0 |
| 7 | COMMA | 0 | 0 |
| 8 | EQ (assignment `=`) | 0 | 0 |
| 9 | LABEL | 0 | label number (integer < 2^24) |
| 10 | KW (statement keyword) | 30 PROGRAM, 31 REAL, 32 DO, 33 CONTINUE, 34 PRINT, 35 FORMAT, 36 STOP, 37 END | 0 |
| 11 | EOL (end of logical statement) | 0 | 0 |
| 12 | EOF | 0 | 0 |
| 13 | FDESC (format descriptor) | 1 `F`, 2 `I`, 3 `E`, 4 `G`(unsupported) | `w<<8 | d` (w<=4, d<=2 for the feasible subset) |
| 14 | INT (integer literal) | 0 | integer (DO bound/step, repeat count) |

Rationale: TK/SUB reuse the FRONT token *numbers* where they already exist
(LIT=1, VARIABLE=2, binary op=3, unary=4; docs/111:38-45) so a future migration
to IR cards is not foreclosed, but the source parser is independent of FRONT.
**[FACT]** FRONT has no intrinsic/DO/FORMAT emitter (docs/112:49-55,
docs/115:36-53, docs/113:47-53); therefore TK 5/9/10/13 are new codes owned by
this parser, not claimed to be FRONT records.

### 2.3 Symbol table in N+2 — reuse of the proven layout [FACT layout, DESIGN allocation]

Identical to docs/109 / docs/114, so the proven two-digit-VIDX reader and
name-compare chain are reused verbatim:

```
For identifier VIDX v (1..30):
  name word : N+2 offset  v       -> RAM 0o21637 + v      (6-bit TEXT, 8 codes, ASCII-0x20, space-padded)
  value word: N+2 offset  32 + v  -> RAM 0o21677 + v      (BESM float, the variable's current value)
```

**[FACT]** Example from docs/109:96-100 / :171-178:
`TEXTA X       = 0o0700000000000000`, `TEXTA Y = 0o0710000000000000`;
X value float(7890), Y value float(1234). **[DESIGN]** At declaration (`REAL A,B`)
we install the name word (built from ASCII by the same `VIDX+28` / `asx SHL42`
chain of docs/114:158-161, or a small constant table for A..Z) and seed the
value word with `0.0` float. Lookup on an ID token is `utc 20000` + `xta
(32+VIDX)(reg)`.

### 2.4 N+2 allocation plan — [DESIGN / INFERENCE from measured C7 layout]

All ranges are N+2 offsets (RAM = `0o21637 + offset`); offsets `526..900`
are forbidden and untouched.

| offsets | words | role |
|--:|--:|:--|
| 1..63 | 63 | symbol table (name v, value 32+v, as in §2.3) |
| 64..180 | 117 | token stream buffer (1 word/token; 117 statements/tokens adequate for a test deck) |
| 181..200 | 20 | literal pool (BESM floats, pre-scaled for docs/105 converter) |
| 201..230 | 30 | operand stack `OSTK` |
| 231..245 | 15 | operator stack `OPR` |
| 246..255 | 10 | constants (shifts, masks, one's-complement −1, zero, precedence table) |
| 260..~520 | ~260 | interpreter code (lexer, parser, dispatcher, handlers) |
| 526..900 | 0 | **never written** |
| 901..1023 | (spare) | optional overflow if code exceeds 520; execution not yet proven |

**[INFERENCE]** Total ≈ 63+117+20+30+15+10+260 = **515 words < 649**
(plus 0 in the forbidden band). C7 measured 177 changed words for a comparable
set of handlers; the extra ~340 words here pay for the source lexer and the
interpreted statement loop. This is a projection, not a built result.

---

## 3. Expression parser WITH PRECEDENCE

### 3.1 Choice: two-stack shunting-yard with immediate evaluation [DESIGN]

We do **not** build a postfix IR stream (that would recreate the 777005 path we
are deliberately avoiding). Instead a single left-to-right scan maintains:

* `OSTK` — operand stack of BESM floats in N+2 offsets 201..230;
* `OPR` — operator stack of packed `TK/SUB` codes in N+2 offsets 231..245;
* stack pointers `SP_O`, `SP_P` in low-RAM scratch cells (proven-free
  `body[0o110..0o135]`, docs/98/105).

Precedence table [DESIGN, matches FRONT `PRT` of docs/111:58-62]:

```
'('   = 0   (marker, never popped by precedence)
'+'   = 1, '-' = 1
'*'   = 2, '/' = 2
unary '-' = 3
INTR  = 3   (applied immediately to the single top operand)
```

Left-associativity: when an incoming OP has precedence `p`, pop and apply every
top-of-OPR operator with precedence `>= p` (stopping at `(` or empty stack), then
push the incoming OP. This reproduces `1+2*3 = 7` and `(1+2)*3 = 9`, the
capability explicitly *missing* in C3 (docs/111:196-205, :228), without any IR.

### 3.2 Instruction-level pseudocode

Registers at entry (re-arm on every statement, after every converter call, as in
docs/114:132-136):
`M[7] = 0o20000` (N+2 short base), `M[12] = 0o20000`, `M[10] = token pointer`,
`M[6] = stack index`, M15 preserved for the resident return.

```
;; --- main scan -----------------------------------------------------------
E_SCAN:
   xta  TOKPTR              ; current token index
   utc  20000 / xta TOKBASE(6)        ; fetch token word (modifier + index)
   atx  TOK                 ; TOK = token word
   aax  M_TK / asx SR42 / atx TKCELL
   aax  M_SUB / asx SR36 / atx SUBCELL
   aax  M_PAY / atx PAYCELL

   ; dispatch on TK via word-aligned table (same technique as docs/111:96-104)
   utc  20000 / xta TKTAB(6)          ; LONG UJ table word
   uj   TKTAB(6)                      ; PC = table_base + TK

T_LIT:   ; TK=1: PAY = literal pool index -> float -> OSTK
   utc 20000 / xta LITBASE(6) / atx VAL       ; VAL = float
   uj  PUSH_O

T_ID:    ; TK=2: value word 32+VIDX -> OSTK
   utc 20000 / xta SYMVAL(6) / atx VAL        ; 0o21677 + VIDX
   uj  PUSH_O

T_INTR:  ; TK=5: apply ABS/SQRT/MOD in place on top of OSTK
   uj  (intrinsic table)(SUB)                  ; docs/112:126-128 trampoline
   ; each routine stores its result back to OSTK top
   uj  E_NEXT

T_LP:    ; '(' -> push marker onto OPR
   ati  P=0 ; uj PUSH_P

T_RP:    ; ')' -> pop OPR until marker, applying each
   uj  POP_TO_MARK

T_OP:    ; TK=3/4: precedence loop
   xta SUBCELL / atx INCOMING
   xta PRECTAB(6)                    ; precedence of incoming
   atx PIN
P_LOOP:
   utc 20000 / xta OPR(6)            ; top of operator stack
   uza E_PUSH_OP                     ; empty -> push incoming
   aax M_SUB / asx SR36 / atx PTOP
   xta PRECTAB(6) / atx PTOPP
   ; compare PTOPP >= PIN  (integer compare via arx/uza, one's-complement aware)
   arx NEG_PIN / uza E_PUSH_OP        ; if PTOPP < PIN -> push incoming
   uj  APPLY_TOP                      ; else apply top and loop
E_PUSH_OP:
   ; push incoming TK/SUB onto OPR
   ati  ... ; uj PUSH_P
E_NEXT:
   utc 20000 / xta TOKPTR / arx K_ONE / atx TOKPTR
   uj  E_SCAN

;; --- end of expression / ')': flush -------------------------------------
FLUSH:
   utc 20000 / xta OPR(6) / uza DONE_EXPR
   uj  APPLY_TOP / uj FLUSH
DONE_EXPR:
   utc 20000 / xta OSTK(6) / atx RESULT       ; single value left on OSTK
   ...

;; --- apply one operator --------------------------------------------------
APPLY_TOP:
   ; pop b = OSTK[--SP_O], a = OSTK[--SP_O]
   utc 20000 / xta OSTK(6) / atx B
   utc 20000 / xta OSTK(6) / atx A
   ; 4-way dispatch by SUB (word-aligned, docs/111)
   uj  (optab_base)(SUB)
OPTAB:  LONG UJ ADD / LONG UJ SUB / LONG UJ MUL / LONG UJ DIV
ADD:  utc 20000 / xta A(7) / a+x B(7) / uj STORE_R
SUB:  utc 20000 / xta A(7) / a-x B(7) / uj STORE_R
MUL:  utc 20000 / xta A(7) / a*x B(7) / uj STORE_R
DIV:  utc 20000 / xta A(7) / a/x B(7) / uj STORE_R
STORE_R:
   utc 20000 / atx OSTK(6)                    ; push result
   ...
```

FPU opcodes are **[FACT]** from docs/95:56-59: `0o004 a+x`, `0o005 a-x`,
`0o16 a/x`, `0o17 a*x`. Loading a float from N+2 uses `utc 20000` + `xta
addr(7)`; the modifier is consumed by the one `xta` and the following `a+x` is
unaffected (docs/110:107-111).

### 3.3 Negative numbers and unary minus [DESIGN, validation needed]

* A leading `-` is token UOP/SUB=6, applied with `avx` (hardware sign change),
  exactly the ABS fix of docs/95:199-204. BESM negative floats are
  two's-complement mantissas, so a bare sign-bit clear is wrong.
* Binary `a-x` is a legal FPU op on two's-complement floats; **[INFERENCE]**
  printing a negative result requires the docs/105 sign block to read bit 40 and
  emit the GOST minus byte. C3 reported "SUB magnitude-only"
  (docs/111:206-210), but that was in the `/10`-scaled EST domain with
  `floor_int`, which cannot handle a negative float. The canonical docs/105
  converter with sign is a different path; this must be validated at B2.
* **[FACT]** FRONT never emits a negative literal (`SC=VAL*100/FRAC` is
  nonnegative; docs/106 §6.6). Variant B is free of that restriction because
  `-` is a token, not baked into the literal.

### 3.4 Linkage to the print path

The result float is deposited into the EST input cell and the converter is
called as a VJM subroutine:

```
   utc 20000 / xta RESULT / atx EST           ; EST = expression value
   vjm 30114(11)                              ; outer link M[9]; converter -> *64 2004
   uza/uj ... re-arm M[7], M[12], M[10] after return
```

**[FACT]** This is the exact C7 pattern (docs/116:67-71, :82-86): converter 40
words in N+3, called once per record via VJM; the only special care is reseeding
GOST words `0o2006`/`0o2007` before each call so digit deposits do not accumulate
(docs/114:113-119).

### 3.5 Word budget estimate — [INFERENCE, derived from measured halfword costs]

| component | measured analogue | estimate (halfwords) | words |
|:--|:--|--:|--:|
| token fetch + field extract | docs/114:147-149 (asx/aax/arx) | 12 | 6 |
| TK jump table | docs/111:96-104 (4 word table) | 8 (4 words) | 4 |
| LIT + ID push | docs/109:113-123, docs/114:145-150 | 16 | 8 |
| intrinsic call (table + 3 routines reused) | docs/112:105-132 | 8 + reuse | 4 |
| precedence loop + compare | docs/111:58-62 (precedence) | 20 | 10 |
| 4-way OP dispatch + apply + push | docs/111:96-104 | 24 | 12 |
| `(`/`)` handling + flush | new | 12 | 6 |
| **expression evaluator subtotal** | | **100** | **50** |

So the precedence evaluator costs roughly **50 N+2 words**. N+3 is **unchanged
at 40/58** (converter) plus the stub of Section 4.5. No N+4 word, no new opcode,
no MMU trick beyond the proven `UTC`/M20.

---

## 4. Statement dispatcher

### 4.1 Dispatch on TK=10/SUB (keyword) [DESIGN]

One word-aligned `LONG UJ` table indexed by SUB gives the statement handlers:

```
KTAB: LONG UJ S_PROGRAM  ; 30
      LONG UJ S_REAL     ; 31
      LONG UJ S_DO       ; 32
      LONG UJ S_CONT     ; 33
      LONG UJ S_PRINT    ; 34
      LONG UJ S_FORMAT   ; 35
      LONG UJ S_STOP     ; 36
      LONG UJ S_END      ; 37
```

### 4.2 Feasibility matrix in 58 + 649 words

| statement | subset implemented | feasibility | notes / citations |
|:--|:--|:--|:--|
| `PROGRAM name` | consume keyword + name, no semantics | **feasible** (~2-4 words) | no code generation needed; analogous to docs/71:294 name limits (<=6 chars) |
| `REAL A,B,...` | install name word + seed value 0.0 in N+2 symbol table | **feasible** (~10-15 words) | reuses docs/109 layout + name code chain |
| assignment `V = expr` | parse expression with precedence, store result to V's value word | **feasible** (~10 words + §3) | the core of the machine parser |
| `PRINT n` / `n FORMAT(...)` | PRINT resolves label `n`, fetches FD tokens, evaluates the print list, calls converter with width w/d | **feasible, restricted** (~25-35 words) | subset w∈{2,3,4}, d∈{1,2} proven in docs/113:156-162; full `Fw.d` (rounding, w>4, E/I/G editors) deferred |
| `DO i = init, lim, step` | counted repeat of the statement range DO..CONTINUE, step=1 only, one level | **feasible, restricted** (~25-35 words) | docs/115:248-270 proves fixed-count countdown; body here is the interpreted statement range (new) |
| `CONTINUE` | loop terminator; decrement counter, rewind statement pointer to DO body | **feasible** (~8-10 words) | general loop variable update deferred |
| `END` | stop interpretation, `uj 0(15)` back to resident | **feasible** (~2 words) | proven return mechanism docs/65:85, :95 |
| `STOP` | treat as END | **feasible** (~2 words) | |
| multiple statements | statement pointer (`SPC`) into token buffer advanced at EOL | **feasible** (~6 words) | this is the interpreted program counter; replaces the fixed 2/6-record unrolled loops of docs/114/116 |
| intrinsics `SQRT/ABS/MOD` | apply on operand stack | **feasible** | docs/95/112 |
| `DSQRT` | **deferred / blocked** | no | Section 5.3 |
| formatted `READ(u,fmt)` | **deferred / blocked** | no | Section 5.3 |

### 4.3 PRINT/FORMAT design [DESIGN]

* Each FORMAT statement's label is stored in a small label table in N+2
  (label number -> token index of its first FD token). PRINT `n` looks it up.
* FD token `F` with `PAY = w<<8|d` drives the proven width masks of docs/113:
  offsets 0..2 (XOR masks for GOST word A leading zeros), 3..4 (AND clear for
  F2), 5..6 (ADD space) are indexed by `w`/`d`.
* The value to print comes from the operand stack (or a variable's value word),
  is fed to EST, and the verbatim converter plus width masks produce e.g.
  `-0034.50` / `-  34.50` / `-0034.5 ` (docs/113:116-121).
* **[INFERENCE]** Combining width masks with the sign block is untested; the
  masks act on seeded GOST byte positions, so they should compose, but this is a
  B4 gate.

### 4.4 DO/CONTINUE design [DESIGN]

N+2 cells (mirroring docs/115:110-124): `L_BOUND`, `L_CNT`, `L_STEP`, `L_BODY`
(token index of first body statement), `L_END` (token index of CONTINUE).

```
S_DO:
   parse INT init -> (optional) set loop variable
   parse INT lim  -> L_BOUND
   parse INT step -> L_STEP   ; only step=1 supported
   L_CNT = L_BOUND
   L_BODY = SPC after DO statement
   SPC = L_BODY

S_CONT:
   L_CNT = L_CNT + K_DECR      ; K_DECR = MASK^1 (one's-complement -1)
   uza S_AFTER_LOOP            ; exit on zero (also -0)
   SPC = L_BODY
   uj NEXT_STATEMENT
S_AFTER_LOOP:
   SPC = token index after CONTINUE
```

**[FACT]** The countdown and `uza` termination (including `-0`) are proven in
docs/115:125-145, :210-233. **[INFERENCE]** Applying it to a *range of
interpreted statements* (rather than one hard-wired `SUM += L_VAL`) is the new
part; it needs `SPC` rewinding and a label/body table, which is why this is B5.

### 4.5 N+3 entry stub (the 18 free words) [DESIGN]

```
0o30162L  atx SAV15           ; preserve resident return link (M15)
0o30162R  utc 20000           ; re-arm M20 for N+2
0o30163L  xta BASE(0)         ; load N+2 base 0o20000
0o30163R  ati 12              ; M[12] = N+2 base
0o30164L  ...                 ; M[7] = 0o20000, M[10] = first card pointer
0o30165L  vjm 0o22147(11)     ; outer call (M[9]) into N+2 interpreter
0o30166L  xta SAV15 / ati 15  ; restore return link
0o30167L  uj 0(15)            ; return to resident
0o30170..0o30205              ; spare / constants (12 words)
```

Entry substitution becomes `body[0o11] = LONG UJ 0o30162` (was `0o30114`).
**[FACT]** VJM link convention and M15 preservation: docs/114:112-115,
docs/65:90-95.

---

## 5. Staged implementation B1..B5, gates, hard blockers

### 5.1 Stages and go/no-go gates

Each gate is **full SIMH A/B/A** with a deck-only change and an image-only
one-word patch, plus C-oracle MTR/CORE, all reaching `КОНЕЦ ЗАДАЧИ`; N+3
`<=58`; N+2 `<=649` with **0 changed offsets 526..900**. (This acceptance
discipline is **[FACT]** from docs/74/75, docs/110 §6, docs/114 §3, docs/116.)

| stage | content | go/no-go gate (decisive observable) |
|:--|:--|:--|
| **B1** | RLE card-buffer reader (cols 7..72) + token emitter + symbol-table seed. | A deck source statement changed by one byte changes the emitted token dump / a token-derived print; byte-identical image. MTR shows `asx`/`aax` extraction at our addresses. **No-go** if RLE expansion or col-7 skip is wrong. |
| **B2** | Expression parser with precedence + FPU + intrinsics; `X = expr`. | Byte-identical image: `X=1+2*3` prints `7`, `X=(1+2)*3` prints `9` (or truncated digits within the 2+2 field). **No-go** if precedence or signed SUB fails; this is where docs/111's missing capability is closed. |
| **B3** | Keyword dispatcher, `PROGRAM`, `REAL`, multiple assignments, `END`. | Two assignments where the second reads the first variable; change the first literal and both prints change. `END` returns cleanly. **No-go** if symbol install/lookup breaks. |
| **B4** | Labeled `PRINT`/`FORMAT`, restricted w/d. | Change a FORMAT `w`/`d` digit in the deck -> printed spacing changes (`-0034.50` vs `-  34.50`), image byte-identical. **No-go** if width masks and sign block conflict. |
| **B5** | `DO`/`CONTINUE` (step=1, one level), full multi-statement deck. | Change DO bound -> different number of accumulated sums; patch `K_DECR` -> fewer iterations; restore byte-identical. **No-go** if statement-pointer rewind or loop termination fails. |

### 5.2 Open items that must be solved inside these stages (not blockers, but work)

* **[FACT]** The proven scanners process a fixed count of records (two in C2b,
  six in C7) and do **not** test `0xff` or drive a loop counter (docs/114:260-266).
  Variant B needs an EOF/EOL-driven statement loop; B1 must add a marker search
  that stops at the `*EXECUTE`/EOF card (the `0xff` sentinel of docs/114:89-101).
* **[FACT]** `0xff` as EOF sentinel is an inference (docs/114:101); the scanner
  currently ignores it. Use the physical card sequence and `*END FILE` framing
  as the reliable terminator, with `0xff` as a secondary check.
* Continuation cards (column 6 nonblank) are **[FACT]** handled in FRONT
  (`FRONT.FTN:70-80`); B1 should either implement them or explicitly reject
  continued statements in the supported subset.

### 5.3 Hard blockers (explicit list)

1. **DSQRT / double precision — DEFERRED/BLOCKED.** **[FACT]** SIMH has one
   48-bit float format, no double FPU; software DP needs >100 instructions and
   was declared infeasible in the 58-word N+3 context (docs/95:206-225;
   docs/106 §2; docs/112:240-243). **[INFERENCE / honest nuance]** the ">100
   instructions" argument weakens under the C7 displacement principle because a
   software-double routine could live in N+2, but no such routine exists and it
   is not in the agreed B1..B5 scope. Treat as blocked until separately
   specified and proven.
2. **Formatted `READ(u,fmt)` — BLOCKED.** **[FACT]** `э52` vectors to `0o0552`,
   privilege-bit branch gives `ЗАПРЕЩ.ЭКСТРАКОД`; the input context is created by
   monitor overlay `INPUT*`, not installed by `*TRANS`; only raw card-buffer
   literal input (`utc 60000` + `xta 4012`) works, which is not READ
   (docs/106 §3; docs/91/92/94). Variant B's reading of *source* from the card
   buffer is fine; reading *runtime data* via READ is not.
3. **Resident FT*002/003/571 (MMU) — BLOCKED.** **[FACT]** 15-bit addressing
   works but SIMH MMU blocks pages `0o77776`/`0o74012`
   (`Число/Команда в чужом листе`); the runtime float-to-GOST converter is
   therefore unavailable and we use our own machine converter (docs/106 §4;
   docs/88). This is not a variant-B blocker because we already have the
   converter, but it prevents falling back to the runtime.
4. **No native FRONT emitter needed anymore — NOT a blocker.** **[FACT]**
   FRONT has no intrinsic/DO/FORMAT IR emitters (docs/112 §1.2, docs/115 §1.1,
   docs/113 §1); in variant B that is irrelevant: we parse the Fortran source
   directly. FRONT is not on the target path; no build-time FRONT card is
   required for the product. (FRONT remains usable only as a build/validation
   tool, as in docs/71/83/85/86, but is not needed by this design.)
5. **No IR cards on the target path — by user decision.** **[DESIGN]** No
   `777005` records, no `*FOREX`/`*FTN`, no `*perso` for the main translator.
   The only deck controls are `ДИС 41(2048)^`, `*NAME`, `*TRANS:OURMRK*,,412350`
   plus the Fortran source (docs/110:18-21, docs/114:17-18).
6. **58-word N+3 ceiling / no N+4 — HARD LIMIT.** **[FACT]** descriptor fields
   cannot be changed without `НЕТ РАЗДЕЛА` or a hung copy loop (docs/106 §1;
   docs/65:38-48). All new code must be displaced into N+2 as in C7.
7. **Full `Fw.d` semantics — DEFERRED.** **[FACT]** only w∈{2,3,4}, d∈{1,2}
   layout selection is proven (docs/113:156-162); rounding, justification,
   E/I/G editors and arbitrary exponent/range floats are out of scope.
8. **Negative-literal GOST print — VALIDATION GATE, not a proven blocker.**
   **[INFERENCE]** canonical sign block handles bit 40 (docs/105) but was only
   A/B-tested for a positive value with a SIGNBIT patch; B2 must confirm a
   computed negative result prints with the minus byte.

---

## 6. FACT / INFERENCE summary

**FACT (cited, measured):**
* entry at `0o1770`, 58 clean N+3 words `0o30114..0o30205`, no N+4 (docs/65,
  docs/106, docs/101).
* N+2 649 free words at offsets `0..525` + `901..1023`, `526..900` forbidden,
  reached by `UTC 20000` + short ADR / M[7]=0o20000 (docs/110).
* RLE 8-bit ASCII card buffer at `0o64000+`, `0x80+n` spaces, `0x0a` pad, `0xff`
  last byte, marker-searched rather than fixed-stride, FRONT cols 7..72
  (docs/114, docs/104, FRONT.FTN:15-16/70-80).
* 6-bit TEXT names (ASCII-0x20, 8 codes/word), name at VIDX / value at
  32+VIDX, on-machine name compare (docs/109, docs/114, docs/20).
* FPU opcodes and 4-way dispatch; operands in N+2 (docs/111, docs/95).
* ABS `avx`, SQRT Newton, MOD AINT; DSQRT infeasible (docs/95, docs/112).
* float->GOST with sign, 40-word converter as VJM subroutine, GOST seed resets,
  `*64 2004` (docs/89, docs/90, docs/105, docs/116).
* precedence/parentheses/unary and multi-record evaluation are exactly what C3
  lacked; C7 integrated all C1-C6 in 40/58 + 177/649 (docs/111, docs/116).
* formatted READ, FT* MMU pages, descriptor changes are hard blocked
  (docs/106).

**INFERENCE / DESIGN (not built or run here):**
* the concrete token-word bit layout and TK/SUB table (§2.1-2.2); must be frozen
  with B1 before code;
* the N+2 region allocation (§2.4) and the ~515-word total; extrapolated from
  C7's 177-word measurement plus new lexer/loop costs;
* the two-stack shunting-yard pseudocode and its ~50-word estimate (§3);
* composition of width masks with the sign block (§4.3), EOF-driven statement
  loop (§5.2), and interpreted DO body (§4.4);
* claim that a computed negative result prints correctly with the canonical
  sign block (§5.3 item 8).

No host-computed result digit is proposed anywhere: the token stream carries
source symbols and indices only; all numeric values are built or computed by
BESM-6 instructions, preserving the user's "всё считается на БЭСМ-6" rule
(docs/corrections.md, docs/106 §7, docs/corrections entry 2026-11-23).

DONE
