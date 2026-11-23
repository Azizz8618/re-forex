# B1 -> B3 integration: machine-code lexer reads REAL Fortran text, emits the B2 one-word token, B3 prints it

> ПЕРВЫЙ НАСТОЯЩИЙ ВАРИАНТ Б: **PASS**. Лексер machine‑кодом читает текст
> Fortran из колоды (`RAM 0o64012`), выводит однословный токен B2 в N+2[64..]
> и передаёт управление dispatchеру B3 (`LONG UJ 0o22065`), печать идёт через
> неизменный GOST. SIMH (b‑harness): `X=12.34 → 21 -0012.34`, `X=56.78 →
> -0056.78` при байтово том же образе; правка machine‑слова → `-0001.23`;
> restore → исходное. Все `КОНЕЦ ЗАДАЧИ`. Бюджет 40/58 N+3, 370/649 N+2,
> 526..900 не тронуты. Ограничение: пока только `NAME=NUMBER`; операторы,
> скобки, многобуквенные имена и метки отложены (B2/B4).

**Date:** 23.11.2026. **Workspace:** `/tmp/.private/azizz/opencode/b1-lexer/`.
**Discipline:** copies only of every disk/image/deck/emulator; no repository edit,
no git write, no live disk, no tmux session 0, no C `dispak` patch. C `dispak`
was **oracle only** (MTR + CORE hooks); all authoritative A/B/PATCH/RESTORE
results are full SIMH ACPU/printer captures from the b-harness. Emulator
`/home/azizz/Yandex.Disk/simh/BIN/besm6`, SHA-256 prefix `9ef71b26` (verified by
`drive_b.py` on every run).

The target deck contains **no IR cards**: `*NAME FRX5XX`, `*TRANS:FRX5*,,412350`
and the Fortran body `PROGRAM MAIN / X=12.34|56.78 / END` (statement in columns
7..72). The card buffer at RAM `0o64012..0o64013` decodes to
`86 58 3d 31 32 2e` / `33 34 c6 0a 0a 0a`, i.e. RLE `<6 spaces>X=12.<34><70 spaces>`.
The digit bytes are real Fortran source, read by BESM-6 instructions; no
`777005`, no `*FOREX`/`*FTN`/`*perso`.

---

## VERDICT

| gate | verdict |
|:--|:--|
| B1 lexer reads real Fortran card text and derives name + literal on machine | **PASS** |
| Token output converted to the B2 one-word layout (`TK/SUB/POS/PAY`) | **PASS** |
| Plug-in to verbatim B3 dispatcher at `0o22065` | **PASS** |
| Decisive SIMH A/B: byte-identical image, `X=12.34` vs `X=56.78` | **PASS** |
| One machine-word patch of OUR lexer table changes printed value | **PASS** |
| Byte-identical restore returns | **PASS** |
| All four jobs reach `КОНЕЦ ЗАДАЧИ` | **PASS** |
| Word budgets N+3 <= 58, N+2 <= 649, offsets 526..900 untouched | **PASS** |
| Full B1 token-class set (OP/LP/RP/COMMA/UOP/INTR, 1..6-letter IDs, labels) | **FAIL** (deferred to B2; §6) |

---

## 1. Token format now emitted (B2 contract, docs/117 §2.1-2.2 + docs/119 §1)

One 48-bit word, **no second word**:

```
bits 47..42  TK    (6)  token kind
bits 41..36  SUB   (6)  subcode
bits 35..24  POS   (12) source position (laid out; B3 does not consume it)
bits 23..0   PAY   (24) payload
word = (TK<<42)|(SUB<<36)|(POS<<24)|PAY
```

Builder encoder reused verbatim: `dispatch_build.tok(tk, sub, pos, pay)`.
Token array = N+2 offsets **64..95** (RAM `0o21737 + i`), one word per token.
The lexer (re)writes the assignment tokens it owns:

| N+2 idx | TK/SUB/PAY | word (octal) | source |
|--:|:--|:--|:--|
| 69 | 2 / 0 / 1 (ID X, VIDX=1) | `0200000000000001` | from Fortran identifier at RAM `0o64013` byte1 |
| 70 | 8 / 0 / 0 (`=`) | `1000000000000000` | from Fortran `=` at RAM `0o64012` byte2 (byte scan found it) |
| 71 | 1 / 0 / 0 (LIT pool idx 0) | `0100000000000000` | literal pool word 0 is overwritten from the Fortran digits |

The surrounding statement scaffolding (PROGRAM/REAL/PRINT/FDESC/END/EOL,
N+2[64..68], [72..77]) is the proven B3 fixture, left byte-identical; B3's
dispatcher consumes the token stream exactly as documented in docs/119 §1.
No 2-word token remains anywhere in this build (`build/lexer_build.py` was the
old prototype; the integrated product is `build/b1_b3_build.py`).

**Symbol table** (docs/109/114 layout): name word at N+2[1] (VIDX=1) is built by
the lexer as ASCII `X` (0x58) minus 0x20 = 0x38, shifted left 42 ->
`0o7000000000000000`. Value word at N+2[33] is written by B3's assignment from
the machine-derived literal pool word at N+2[100].

**Literal**: the four Fortran digit bytes `31 32 2e 33 34` are decoded on the
machine by the docs/104 chain (`asx` byte shifts + `aax 0xff` + `arx 0xd0` +
`aax 0xff` -> `10*T[]` -> `e+x EMASK/C105` -> `*100`) to float `1234.0`, divided
by the on-machine `TEN` cell to `123.4` = **10 x printed value**, and stored at
N+2[100]. The verbatim docs/105 converter divides by 10 on print.

---

## 2. Plug-in contract with B3 (how B1 hands off)

* Image built from FRX5 base `2f5fcf873d...`; contour entry `body[0o11] = LONG UJ 0o22313` = our lexer (`LEX_RAM`).
* Our lexer code/data: N+2 offsets 260..298 (constants) and **300..368** (137 halfwords / 69 words).
* N+3: verbatim B3/C6 converter + `floor_int` as a VJM subroutine, **40/58 words**.
* B3 dispatcher is `dispatch_build.build_dispatch(CONV_RAM0)` reused **verbatim**, code at N+2 offsets **150..254**, entry RAM `0o22065`.
* After writing tokens, name, and literal, our lexer executes `LONG UJ 0o22065`; B3 re-arms M[12]/M[7] from low-RAM `HALF` (docs/119 §5 item 5) and runs unchanged.
* Base registers used by our lexer: M[12]=0o20000 (N+2 operand base), M[7]=0o20000 (short branch base), M[10]=0o60000 (card word pointer, no extra UTC on card reads), M[11]=byte index into the six RLE bytes, M[6]=digit index into the low-RAM `T[]` table.
* Indexed N+2 access (the RLE shift-control table) uses `UTC 20000` + `ASX <ctrl>(reg=11)`, because a short instruction adds only one index register; verified in raw MTR (`MTR 22320R utc 20000` / `MTR 22321L asx 22243(13)`).

---

## 3. Decisive SIMH A/B/PATCH/RESTORE (authoritative, b-harness, prn0)

Driver: `/tmp/.private/azizz/opencode/b-harness/drive_b.py` (isolated tmux socket,
`ДATA:` via `capture-pane`, `ДАЙ А0`/`ДАЙ А1`/`НОМВ`, post-job-start `НОМВ`,
stock `attach -n prn0/prn1`). Harness `product_gate=PASS` and `plumbing=PASS` for
all four cases. Authoritative prn0 lines (line 100 and line 114):

| case | image SHA (first 16) | deck | prn line 100 | line 114 | verdict |
|:--|:--|:--|:--|:--|:--|
| A | `06132d14d87e77f6` | `X=12.34` | ` 21 -0012.34  3000.00` | `КОНЕЦ ЗАДАЧИ ... 0000206320000000` | PASS |
| B | `06132d14d87e77f6` (byte-identical) | `X=56.78` | ` 21 -0056.78  3000.00` | same | PASS |
| PATCH | `821f74ad527bd8d6` | `X=12.34` | ` 21 -0001.23  3000.00` | same | PASS |
| RESTORE | `06132d14d87e77f6` (= A) | `X=12.34` | ` 21 -0012.34  3000.00` | same | PASS |

Byte diffs (`cmp -l`):
* `deck_A` vs `deck_B`: **4 bytes** at 1-based 134,135,137,138, octal `61 62`->`65 66` and `63 67`->`67 70` (the Fortran digits). Everything else in both decks identical.
* image A vs PATCH: **3 bytes** in one machine word plus the two recomputed zone-N+2 checksum copies: offsets `10419097` (`0o106`->`0o105`), `10419129` (`0o106`->`0o105`), `10421313` (`0o320`->`0o317`). The changed data word is **N+2[272] = `L_PD0`**, our lexer's ASCII-to-digit mechanism constant, `0xd0` -> `0xcf`; the deck is unchanged.
* image A vs RESTORE: **empty** (same SHA, byte-identical restore).

Causality: with the image frozen, changing only the four Fortran digit bytes
changes the printed value `12.34 -> 56.78`. With the deck frozen, changing only
one machine word of OUR lexer table changes `12.34 -> 1.23`. Restoring the exact
image restores `12.34`. The digits are therefore machine-derived from the
Fortran text through our lexer + B3, not host-substituted.

---

## 4. Raw ACPU and C-oracle evidence

Raw SIMH (prn0 capture, authoritative):

```
B1X_A      : " 21 -0012.34  3000.00"  ...  " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
B1X_B      : " 21 -0056.78  3000.00"  ...  " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
B1X_PATCH  : " 21 -0001.23  3000.00"  ...  " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
B1X_RESTORE: " 21 -0012.34  3000.00"  ...  " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
```

C `dispak` oracle reproduces all four printed values (oracle only; `rc 0`):
`oracle/TRY_A/out.txt` `21 -0012.34`, `oracle/TRY_B/out.txt` `21 -0056.78`,
`oracle/TRY_PATCH/out.txt` `21 -0001.23`.
C CORE dumps taken **after the lexer, at dispatcher PC `0o22065`**
(`oracle/CORE_A/core-pc.bin`, `oracle/CORE_B/core-pc.bin`) show the machine
state handed to B3:

```
                    deck X=12.34        deck X=56.78
N+2[1]  name word   7000000000000000   7000000000000000   ('X' 6-bit TEXT code)
N+2[100] literal    4357331463146315   4510676314631463   (f32(123.4) / f32(567.8))
N+2[69] ID token    0200000000000001   0200000000000001   (TK2/SUB0/PAY1)
N+2[70] '=' token   1000000000000000   1000000000000000   (TK8)
N+2[71] LIT token   0100000000000000   0100000000000000   (TK1/PAY0)
```

Raw C MTR excerpt of OUR lexer (`logs/mtr_b1_lexer_excerpt.txt`, window
`BESM6_MTR_LO=022300,HI=022500,N=100`, AU printed before each instruction):

```
MTR 22316R atx    2303(14) AU=4145407514231056  ; card word = 86 58 3d 31 32 2e
MTR 22320R utc    20000(0)  ...                 ; + index for SHRTAB
MTR 22321L asx    22243(13) AU=4145407514231056 ; byte i -> low byte
MTR 22322L aex    2251(14) AU=0000000000206     ; byte0 (0x86) XOR 0x3d != 0
... (i=1: 0x58 != '=')
MTR 22322L aex    2251(14) AU=0000000000075     ; byte2 = 0x3d ('=')
MTR 22322R uza    2331(7)  AU=0000000000000     ; match -> FOUND
MTR 22336L aax    2252(14) AU=0000000103130     ; identifier byte 'X' = 0x58
MTR 22337R arx    2256(14) AU=0000000000130     ; -0x20 -> 0x38
MTR 22340R atx    2306(14) AU=7000000000000000  ; name word = 0x38<<42
MTR 22341R atx    1640(14) AU=7000000000000000  ; store to N+2[1]
MTR 22350R asx    22243(13) ...                 ; number bytes 3,4 + word 0o64013 bytes 0,1
...  MTR ... arx/aax/e+x/a*x/a+x               ; docs/104 chain -> f32(1234) -> /10
MTR ... atx    2300(14) ...                     ; literal -> N+2[100]
```

---

## 5. Word budget (FACT)

| resource | used | limit | verdict |
|:--|--:|--:|:--|
| N+3 hot path (verbatim converter + floor_int) | **40 words** (74 + 6 halfwords) | 58 | PASS (18 free) |
| N+2 lexer constants + code | offsets 260..368 = **109 words** | 649 total | PASS |
| N+2 whole footprint (B3 dispatcher + tokens + literals + our lexer) | **370 words** (highest changed offset 368) | 649 | PASS |
| changed N+2 words vs base image | 249 (offsets 1..368) | - | PASS |
| N+2 forbidden band offsets 526..900 | **0 changed** | 0 | PASS |
| zone N+4 | not used | unavailable | PASS |

---

## 6. Honest subset / what is NOT in this B1 (FACT)

The integrated lexer recognises and derives exactly what the `X=NUMBER` gate
needs: the RLE space run is skipped by byte-scanning for `=`, the identifier
byte immediately before `=` becomes the 6-bit TEXT name word, the digits and
`.` after `=` become the literal pool float, and `=`, ID and LIT are emitted as
B2 one-word tokens. It does **not** yet:

1. Encode **multi-letter identifiers (2..6 letters)** or statement labels: only the single byte before `=` is read; a label or a 2-letter name would be mis-decoded. (B2 scope.)
2. Emit B2 **TK 3/4 OP** (`+ - * /`), **TK 6 LP/RP**, **TK 7 COMMA**, **TK 4 UOP**, **TK 5 INTR**, **TK 9 LABEL**, **TK 14 INT** tokens. Those classes are defined in docs/117 §2.2 but no Fortran statement in the decisive deck exercises them and B3 does not consume them. (B2 scope; B3 itself only executes the fixture shapes of docs/119 §5.)
3. Drive a general statement loop from EOF: the token stream handed to B3 is the fixed B3 shape (docs/119 §1) with the assignment tokens rewritten from the text; there is no per-statement Fortran lexer loop beyond the single `X=...` statement.
4. Parse `REAL`, `PRINT`, `FORMAT`, `DO` from source: those KW/FD tokens are the proven B3 scaffolding constants, not derived from this deck (which has no such statements).

These are reported as **FAIL** for the original "recognise at minimum" sub-gate;
they are deferred to B2/B4 and do not affect the end-to-end B1->B3 gate, which
proves that real Fortran digits in the deck become the printed value through
our machine code.

---

## 7. FACT / INFERENCE

**FACT:** card-buffer byte layout at `0o64012/0o64013` (C CORE dump); RLE `0x86`
= 6 spaces and `0xc6` = 70 spaces; the four deck digit bytes are the only deck
difference; the image is byte-identical between A and B; one N+2 word patch
changes the printed value; A and RESTORE are byte-identical; all four SIMH jobs
reach `КОНЕЦ ЗАДАЧИ`; C MTR shows the byte scan, name-word construction and
literal store; C CORE at `0o22065` shows the literal differing with the deck;
N+3=40/58, N+2=370/649, zero writes to 526..900.

**INFERENCE / limits:** the RLE "contiguous cards on word boundaries" rule is
extrapolated from the observed cards (docs/114 §1.3); B2 token POS is laid out
but not consumed by B3 (docs/119 §1); the six shift-control cells and the
indexed `UTC+ASX` reach are machine-proven here but remain a local convention of
this build; literal scaling assumes exactly two fractional digits (`12.34`,
`56.78`) as in docs/104 (`SC = VAL*100/FRAC`); `K_PRINT_BIAS` and the `L_PD0`
patch are mechanism words, not Fortran features.

---

## 8. SHAs (SHA-256)

```
06132d14d87e77f69f61d0b4139634686a730fda39d44b07e9874f88cf7614c1  2048_B1B3_A  (A, B, RESTORE; byte-identical)
821f74ad527bd8d6445feeb591034e1ced8e28d0a3fdcfb2513f37e9d84c0db9  2048_B1B3_PATCH  (N+2[272] 0xd0->0xcf)
2f5fcf873d43c2846ee1669669e26202f32fa25e6b71e109fd20ef4452142ff5  2048_base (FRX5 base, unchanged)
4618a7eef292fcb509096c520b142ef29fbe3191965a6dcfff748269b07af703  deck_A.b6  (X=12.34)
014d52c6612df164a7e476b498f1736618785c38b1bc299e779530963a7feeb2  deck_B.b6  (X=56.78)
7603839cd1cfb1f741c98790c37610d692d154f4bc5dba00f885d62b0f702c29  oracle/TRY_A/out.txt
5d2b7203cb7e3180b68abad95cd42081b3ddb65e5c4f746c55eb0bfc3a87d5f9  oracle/TRY_B/out.txt
7c428a8c0c351e8d71beaf33f7f730466c88bd662b46a5d8e66f58d2fa61ef7e  oracle/TRY_PATCH/out.txt
67537c1a9775bcac782b07011c4e88b79a6e89cc94fa774ee06a6f2431072234  oracle/CORE_A/core-pc.bin
26b8809e71a29437ec098d7afeb8acb94f089c5a7e2b4d96b261d6b7d2b85b8e  oracle/CORE_B/core-pc.bin
bd8fe895d4e04cc6beb08da48808cbf09da098bafbe84a64cd4ef0d5b3117fd6  logs/mtr_b1_lexer_excerpt.txt
b5857df19e1b3521a12708be8327cdc486d3017c297dad170da1bb385e4f62b8  b-harness/runs/localprn_B1X_A.txt
9b6e99c656e084deef41b85938b2aa3259d319d4025576c4cb8a3512245bbcd9  b-harness/runs/localprn_B1X_B.txt
c15fcc48524fdfc1b891e2f14735c2054d911c9d9603cb2fcb038c0f1365ccf4  b-harness/runs/localprn_B1X_PATCH.txt
f36ed27687137a60d20bedaa8680e7c7e051c2510135ab19cb1f46de241cc3ad  b-harness/runs/localprn_B1X_RESTORE.txt
```

---

## 9. Evidence index

```
build/b1_b3_build.py          integrated builder (lexer + verbatim B3 + verbatim converter)
build/dispatch_build.py       verbatim B3 dispatcher + tok() encoder (copied from b3-dispatch)
build/c6_build.py             verbatim N+3 converter, Code, vals (copied from b3-dispatch)
build/patch_b1.py             one-machine-word patch of N+2[272] L_PD0
build/oracle_core.py          C-oracle CORE dump at an arbitrary PC (oracle only)
build/dump_core_n2.py         decode N+2 tokens/literals from a CORE dump
build/dump_cardbuf.py         decode RLE card buffer from a CORE dump
logs/mtr_b1_lexer_excerpt.txt raw C MTR of our lexer at 0o22313
images/2048_B1B3_{A,PATCH,RESTORE}
decks/deck_{A,B}.b6           real Fortran source, 4 digit bytes differ
oracle/{TRY_A,TRY_B,TRY_PATCH}/out.txt   C-oracle printed values
oracle/{CORE_A,CORE_B}/core-pc.bin       CORE at B3 entry 0o22065
/tmp/.private/azizz/opencode/b-harness/runs/{localprn,console,verdict}_B1X_*.txt|json
```

DONE
