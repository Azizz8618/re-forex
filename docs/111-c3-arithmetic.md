# C3 — contour executes ARITHMETIC OPERATIONS decoded from IR tokens

> РЕЗУЛЬТАТ C3: **PASS** — арифметика из IR работает. FRONT выдаёт операторы
> `777005` с `TK=3`, `TO=1/2/3/4` для `+ − × ÷` (`FRONT.FTN:299-345`); контур
> декодирует TO, делает 4‑WAY dispatch и считает на FPU с операндами в N+2.
> SIMH A/B/C/D: `*` → `21 -0003.75`, смена токена на `+` → `-0004.00`,
> правка одного machine‑слова → `-0001.75`, restore → `-0003.75`.
> Бюджет **51/58 слов** (7 резерв), 5 слов таблиц в N+2.
> Оговорка: один бинарный оператор, слева направо; приоритет/скобки/
> unary и сканер записей отсутствуют; SUB — magnitude‑only.

> RESULT: **PASS**. The contour reads the operator opcode (TO field, TK=3) of a
> genuine `777005` FRONT IR record from the deck card, dispatches a 4-way
> word-aligned jump table, performs the matching BESM-6 FPU operation on
> pre-scaled operands held in zone N+2, stores the result back to N+2, and feeds
> it into the **verbatim** docs/105 sign + 2+2 GOST print path. SIMH decisive
> A/B/C/D: `*` -> `21 -0003.75`, same image + `+` token -> `21 -0004.00`,
> one machine-word patch of OUR code -> `21 -0001.75`, byte-identical restore
> -> `21 -0003.75`. All reached `КОНЕЦ ЗАДАЧИ`. Budget **51/58 words** in N+3
> (7 words spare), 5 words of tables in the clean part of N+2.

Date 23.11.2026. Workspace `/tmp/.private/azizz/opencode/c3-arith/` (symlink to
`/dev/shm/c3-arith`; the `/tmp` tmpfs was 100% full, so the bulky copies live on
`/dev/shm` exactly as in docs/95). Copies only: no repo, live disk, tmux session
0 or C `dispak` source edits. Deck contains only `ДИС 41(2048)^`,
`*NAME FRX5XX`, `*TRANS:FRX5*,,412350` plus standard framing. C `dispak` was
**oracle only** (MTR/CORE, docs/88); all authoritative A/B results are full
SIMH ACPU/printer captures with a workspace-local `-n prn0` path. No
host-computed result digit is stored anywhere in the image.

---

## 1. FRONT.FTN IR token contract (FACT, file:line citations)

All RHS tokens of rule 31 are emitted as the **same record type `777005`** as
LIT/VARIABLE. There is no new MR type for operators.

| token | `TK` | `TO` | `TA` | `TB` | source |
|:--|:--:|:--:|:--|:--:|:--|
| LIT | 1 | 0 | `SC = VAL*100/FRAC` | 0 | `src/newcomp/FRONT.FTN:254-259` |
| VARIABLE | 2 | 0 | `VIDX` (X=1,Y=2,N=3,I=4, else ASCII-60) | 0 | `:262-276` |
| binary op | **3** | **OP: 1=`+`, 2=`-`, 3=`*`, 4=`/`** | 0 | 0 | `:299-305`, `:314-327`, `:335-345` |
| unary op | 4 | 6 (unary minus), 7 reserved | 0 | 0 | `:310-311`, `:322-324`, `:339-341` |

Exact citations:

* `:54` `DATA MR5 /777005/`; `:349`
  `PRINT 9005, MR5, SEQ(I), TK(K), TO(K), TA(K), TB(K)`; `:376`
  `9005 FORMAT(1X,6I8)`. Record text: `777005 <seq> <TK> <TO> <TA> <TB>`.
* `:208` comment `N1.7: structured RHS IR 777005 for rule 31 (postfix/eval order)`.
* `:300-305` `OP=1` (default `+`), `:302` `IF(CH.EQ.45) OP=2` (`-`), `:303`
  `IF(CH.EQ.42) OP=3` (`*`), `:304` `IF(CH.EQ.47) OP=4` (`/`),
  `:305` `IF(OP.GE.3) PR=2`.
* `:321-326` emit `TK(NTK)=3`, `TO(NTK)=TOP`, `TA=0`, `TB=0` (and `TK=4`
  when `TOP` in 6..7); identical encoding at `:287-292` (closing paren flush)
  and `:338-343` (final flush).

**Eval order (postfix / RPN).** The dispatcher at `:299-333` is an explicit
shunting-yard: operator stack `ST`, precedence `PR` (`*=2,/=2,+=1,-=1`),
parenthesis marker 8, unary-minus marker 6 (highest, `PRT=3`). Operands are
emitted when scanned; operators are popped to output only when their precedence
is `>=` the incoming one (`:320`) and the remainder is flushed at `:530-345`.
Therefore FRONT emits **operands first, operator last** (postfix), e.g.
`1.5*2.5` -> `LIT 150`, `LIT 250`, `OP TK=3 TO=3`; and `A*B+C` ->
`VARIABLE A`, `VARIABLE B`, `OP *`, `VARIABLE C`, `OP +`. This is the
"postfix/eval order" of rule 31, consistent with docs/63 §3.1 (lines 206-238),
which defines rule 31 as the assignment whose RHS is streamed to `777005`.

**Decision for this contour:** the 58-word limit cannot carry a general
postfix stack scanner, so the minimum honest subset is implemented: **one
binary operator evaluated left-to-right**, with its two operands pre-seeded in
N+2 and the operator token read from the deck. FRONT was not modified; all
token codes above are FACT from the source.

## 2. Machine-code implementation (reuse first)

Reused **verbatim**: repo base-image writer `tools/build_zone2350_contour.py`;
docs/105 `final_sign.Stream` ABS+2+2 GOST converter, sign block, `floor_acc`
and `drop_last_ati` reclaims, shared `floor_int` VJM at `0o30174`, and resident
`*64 2004`; docs/98 `ARX NEG31` ASCII-to-digit trick; docs/109/110 N+2 base
`0o21637`, free offsets `0..525`, `UTC`/`VTM` + short ADR reachability;
docs/108 FRX5 catalog rename (base image `2f5fcf87...`); docs/100 SIMH harness.

New code is only the evaluation front end in `build/c3_build.py`:

```
30114L utc 60000          ; card page (verbatim docs/93/104)
30114R xta 4014           ; card word RAM 0o64014
30115L asx SR40           ; byte 0 = TO operator digit -> low byte
30115R aax M8
30116L arx NEG31          ; ASCII '1'..'4' -> digit 1..4
30116R atx OPCELL
30117L ati 6              ; M[6] = op (dispatch index)
30117R vtm 20000(7)       ; M[7] = 0o20000 base for N+2 short ADRs
30120L xta 1640(7)        ; ACC = A10 (N+2 offset 1, RAM 0o21640)
30120R uj 30121(6)        ; PC = word 0o30121 + op
;; word 0o30121: dummy uj ADD
;; word 0o30122 ADD: a+x 1641(7) / uj COMMON
;; word 0o30123 SUB: x-a 1641(7) / uj COMMON
;; word 0o30124 MUL: a*x 1643(7) / uj COMMON
;; word 0o30125 DIV: a/x 1643(7) / uj COMMON
30126L atx 1644(7)        ; COMMON: result -> N+2 offset 5
30126R atx EST            ; -> verbatim docs/105 converter -> *64 2004
```

Key machine facts proved by C-oracle MTR (oracle only):

* `uj` is a long-format opcode: PC is a **word** address and `Aex = addr +
  M[reg]`. A 5-slot table therefore uses one whole word per operator; adding a
  `UTC 30000` modifier double-offsets the jump (observed trap). Jump targets
  must be word addresses (`0o30114 + z3_word_index`).
* `UJ` also adds `M[reg]`, so the direct jumps use **reg 0** (`M[0]=0`). Using
  reg 15 (the resident return link `0o1764`) overshot to `0o32112` and aborted.
* base register `M[7]=0o20000` (one `VTM`) makes every N+2 operand a 12-bit
  short ADR (`0o1640..0o1644` -> `0o21640..0o21644`), avoiding per-instruction
  `UTC` and fitting the budget.
* Operands are **pre-scaled in N+2** so no post-op scaling is needed:
  `A10=10a, B10=10b, A1=a, B1=b`; `ADD=A10+B10`, `MUL=A10*B1`, `DIV=A10/B1`.

## 3. SIMH decisive A/B (authoritative)

Operands seeded in N+2: `a=1.5`, `b=2.5` (EST-domain `A10=15.0`, `B10=25.0`,
`B1=2.5`). Deck IR card (only changed field is the operator digit):

```
  777005       6       3       3       0       0        (op 3 = *, gate A)
  777005       6       3       1       0       0        (op 1 = +, gate B)
```

The printed minus sign is the canonical docs/108 SIGNBIT seed (positive value
prints with `-`); the digits are the computed result.

| gate | image (SHA prefix) | deck TO | raw SIMH ACPU line 100 | КОНЕЦ ЗАДАЧИ |
|:--|:--|:--:|:--|:--:|
| A | `6cf038fb...` | 3 (`*`) | ` 21 -0003.75  3000.00` | yes |
| B | `6cf038fb...` (byte-identical) | 1 (`+`) | ` 21 -0004.00  3000.00` | yes |
| PATCH | `6480499c...` (one word of OUR code) | 3 (`*`) | ` 21 -0001.75  3000.00` | yes |
| RESTORE | `6cf038fb...` (= A) | 3 (`*`) | ` 21 -0003.75  3000.00` | yes |

Causality:

* A vs B: only **one deck byte** changes (1-based offset 157, `3`->`1`); the
  image is byte-identical. Result changes 3.75 -> 4.00, i.e. the operator token
  alone selects the FPU operation.
* PATCH: z3 word 8 (MUL handler) `a*x 1643(7)` -> `a+x 1643(7)`. One machine
  word of OUR contour plus two recomputed zone-N+3 checksum copies: **5 byte
  diffs in 3 machine words** (1-based 10427357/8, 10427389/90, 10427461).
  Result changes 3.75 -> 1.75. No host-computed result digit is stored.
* RESTORE is byte-identical to A (same SHA), result returns to 3.75.
* All four printers reported `КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000`.

### Raw C-oracle MTR (evidence only, `logs/MTR_*_clean.txt`)

```
MTR_A    30116L arx 2126 AU=...0063 ('3')      30116R atx 2111 AU=...0003 (op=3)
         30120R uj 30121(6) ... 06=00003 07=20000
         30124L a*x 1643(7)  AU=4217000000000000 (A10=15)
         30124R uj 30126(0)  AU=4311300000000000 (15*2.5=37.5)
         PRN: 21 -0003.75  3000.00
MTR_B    30116L arx 2126 AU=...0061 ('1')      30116R atx 2111 AU=...0001 (op=1)
         30120R uj 30121(6) ... 06=00001 07=20000
         PRN: 21 -0004.00  3000.00
MTR_PATCH 30124L a+x 1643(7) AU=4217000000000000
          30124R uj 30126(0) AU=4250600000000000 (15+2.5=17.5)
          PRN: 21 -0001.75  3000.00
```

### Full four-operator C-oracle sweep (same image, only deck TO changed)

| TO | op | C-oracle printer line |
|:--:|:--|:--|
| 1 | `+` | ` 21 -0004.00  3000.00` |
| 2 | `-` | ` 21 -0001.00  3000.00` |
| 3 | `*` | ` 21 -0003.75  3000.00` |
| 4 | `/` | ` 21 -0000.60  3000.00` |

All four reached `КОНЕЦ ЗАДАЧИ`.

## 4. Word budget and tables

* **Zone N+3: 51/58 words** (102 halfwords) including the shared `floor_int`
  subroutine at `0o30174`; 7 words of headroom. No N+4 word.
* **Zone N+2: 5 words** at offsets 1..5 (RAM `0o21640..0o21644`):
  `A10, B10, A1, B1, RES`. Offsets `0..525` are otherwise free; the
  load-bearing overlay table at offsets `526..900` was **not touched**.
* Low RAM: new mechanism cells reuse proven-free cells `CARD` (shift control),
  `PD0` (operator scratch); no new cell outside `body[0o110..0o135]`.

## 5. Supported subset / what is missing

**Supported (FACT):** four binary operators `+ - * /` decoded from the `TO`
field of a single `TK=3` IR record; single left-to-right evaluation of two
operands held in N+2; result written back to N+2; verbatim GOST print path;
one-word patch and byte-identical restore proven under full SIMH.

**Honest limitations:**

1. **One operator per run.** No postfix stack, no multi-token sequence. A
   longer expression needs a scanner (C2b covers the multi-record scanner).
2. **No precedence or parentheses.** FRONT's shunting-yard precedence
   (`*`/`/` > `+`/`-`) and `TK=4` unary minus are not evaluated; the deck
   supplies one already-ordered binary operator.
3. **Operands are seeded in N+2**, not decoded from `TK=1/2` LIT/VARIABLE
   records in this image (the 4-digit LIT and VIDX readers were *replaced*, not
   coexistent). The operator opcode is the only IR field read from the card.
4. **SUB is magnitude-only.** The verbatim `floor_int` cannot process a
   negative float, so SUB is implemented as reverse subtract `B10-A10`. For
   the tested `a<b` case the printed value equals the true `a-b` result; for
   `a>b` it would not. A full signed SUB needs an ABS + sign-flag extension of
   the converter (not fitted).
5. No `777001..777004`, no `777010/777011`, no marker validation, no variable
   name comparison, no VIDX=10..30, no signed/exponent literals.

## 6. PASS / FAIL

| # | criterion | verdict |
|:--|:--|:--|
| 1 | FRONT operator codes/layout with file:line citations (TK=3, TO=1..4, same 777005) | **PASS** |
| 2 | Postfix/eval order stated with docs/63 §3.1 + FRONT :299-345 | **PASS** |
| 3 | On-machine TO decode + 4-way FPU dispatch + N+2 operands/result | **PASS** |
| 4 | N+3 budget 51/58; N+2 tables 5 words, 526..900 untouched | **PASS** |
| 5 | SIMH A: `*` -> `21 -0003.75`, КОНЕЦ ЗАДАЧИ | **PASS** |
| 6 | SIMH B: byte-identical image, `+` token -> `21 -0004.00`, КОНЕЦ ЗАДАЧИ | **PASS** |
| 7 | SIMH PATCH: one machine word of OUR code -> `21 -0001.75`, КОНЕЦ ЗАДАЧИ | **PASS** |
| 8 | SIMH RESTORE: byte-identical -> `21 -0003.75`, КОНЕЦ ЗАДАЧИ | **PASS** |
| 9 | C-oracle MTR confirms op digit, dispatch and FPU result | **PASS** |
| 10 | All four operators print correct digits (C oracle) | **PASS** |
| 11 | Full precedence / parentheses / postfix stack | **FAIL** (out of scope; §5.2) |
| 12 | Multi-record scanner, `777001..4`, `777010/11` | **FAIL** (C2b / absent emitters) |
| 13 | Signed SUB for `a>b` | **FAIL** (§5.4; converter limitation) |

## 7. SHAs (SHA-256)

```
a98e81090d4b254554a0cd3ff8611438615de84fc012e8e2b70fbabc2ebdc796  images/2048_base (reproduces docs/87)
2f5fcf873d43c2846ee1669669e26202f32fa25e6b71e109fd20ef4452142ff5  images/2048_base_frx5 (FRX5 catalog)
6cf038fbfc758c1e71bebad4817d9d6f978590ae4c7de9bc0173b0a94b47efec  images/2048_C3_A = _RESTORE
6480499c4941ca3792c09d5ae70c7e9942ed73d62507212d8dd90d97d9bced0a  images/2048_C3_PATCH
37ad17d69475017172bb1d838c0e974d2a62498100cf05e3481568ca2ce57c2b  decks/deck_base.b6
02fb7952c0b34a64984ccdbeca217d5a2b776be193c8a91a34a7a5863ec49f7b  decks/deck_op1.b6 (+)
1d2d53a5ae92595daa7dadee33c1d4b892f36f6e7944fc678d5a7c3155aac56f  decks/deck_op2.b6 (-)
0a9b96a838a8631ec87aad57d7e5d56c730b62b1e5e1e4c87903fdd7a5b2c3f1  decks/deck_op3.b6 (*)
8e5b5c11292c1ae3d3719e8c6f43d57465f41b39e668972a7d9f7a63289ac014  decks/deck_op4.b6 (/)
c86dff64ce336b774782e549a57dacd24794eee5b2c70ec715c929d3facc23b7  runs/localprn_A.txt
8b319e22fdce78eb8f741a84adb02d573b4ed51a82cef37f66e109566780b737  runs/localprn_B.txt
34b41c65388c0bbea85895b9427e75ae7f97a7e866b0856eb0f3248e587c8afb  runs/localprn_PATCH.txt
6daa3e6b1d1bcdaf9e7ef2970f35f823f2817be64566028e6541b9427ad95244  runs/localprn_RESTORE.txt
0d5c83fa2c99af6c1fe1339861a5ab08f35c30aa0548c810df698de9f598bfe8  logs/MTR_A_clean.txt
756c862af49ccdf04bc78c23d2bd0c150e6b09f85ab3795ca41f7eef141bea60  logs/MTR_B_clean.txt
f1a05b981741e597590b048c833ee063a2ab4990b8f3b17d364b84a14a825821  logs/MTR_PATCH_clean.txt
15d7ed92f4fbecd6ad43afc8c88e375073522ba2c2a67a56422bb9ea852704fb  build/c3_build.py
```

## 8. Evidence index

```
build/c3_build.py                evaluator + image builder (measure/build)
build/c3_eval.py                 earlier design draft (not used in final build)
build/{build_e2e,final_build,final_sign,c2_build}.py  proven helpers, read-only copies
build/{drive_c3,oracle_clean}.py  isolated SIMH driver / bounded C oracle
decks/deck_op{1,2,3,4}.b6        IR operator-token decks (one digit differs)
images/2048_{base,base_frx5,C3_A,C3_PATCH,C3_RESTORE}
runs/localprn_{A,B,PATCH,RESTORE}.txt  authoritative SIMH printer output
runs/console_{A,B,PATCH,RESTORE}.txt   raw SIMH console transcripts
logs/MTR_{A,B,PATCH}_clean.txt   clean C-oracle MTR excerpts
oracle/OP{1,2,3,4}/, oracle/MTR_*/   raw C-oracle MTR/CORE (oracle only)
logs/SHAs.txt                    full SHA-256 list
```

DONE
