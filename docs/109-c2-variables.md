# C2 - contour IR support from LITERALS to VARIABLES (6-bit TEXT symbol table in zone N+2)

> РЕЗУЛЬТАТ C2: **PASS** — переменные в IR работают. FRONT выдаёт
> `777005 <seq> 2 0 <VIDX> 0` (X=1, Y=2, …, ASCII−60), контур декодирует VIDX
> и индексирует таблицу в зоне N+2. SIMH A/B/C/X: `Y → 21 -0012.34`,
> правка слова → `-0056.78`, restore → `-0012.34`, тот же образ с токеном X →
> `-0078.90`. Бюджет 45/58 слов, 13 слов резерва.
> ВАЖНАЯ КОРРЕКТИКА: RAM‑база зоны N+2 — `0o21637`, а не `0o1746`
> (последнее — номер дисковой зоны в docs/63). Свободны офсеты 0..525 и
> 901..1023; 526..900 заняты обязательной таблицей оверлея.
> Не сделано: двухзначный VIDX (10..30), сравнение TEXT‑имён на машине,
> сканер нескольких IR‑записей.

Date: 23.11.2026. Workspace `/tmp/.private/azizz/opencode/c2-vars/` (copies only).
The repository, live disks, tmux session 0 and the C `dispak` sources were **never**
edited. Every image/disk/deck is a COPY. SIMH used an isolated tmux socket
(`runs/tmux/`, `TMUX_TMPDIR`) and a workspace-local `prn0` capture
(`runs/localprn_*.txt`); stock `attach -n` semantics were kept, only the path
changed. C `dispak` was **oracle only** (the only emulator with MTR/CORE hooks,
docs/88); all authoritative A/B/C results are full SIMH ACPU output.
Deck contains only `ДИС 41(2048)^` / `*TRANS:OURMRK*,,412350` plus standard
Fortran framing; no `*FOREX`/`*FTN`/`*perso`.

## VERDICT: PASS - indexed VARIABLE lookup works; 45/58 words, 13 words headroom

A real `777005` VARIABLE token (`TK=2`, `TA=VIDX`) is read from the card buffer,
`VIDX` is decoded on machine, and it indexes a symbol table in zone N+2. The
value word (a BESM float of the literal x100) is loaded from the table and fed
into the verbatim docs/105 ABS + 2+2 GOST + machine-sign chain. The printed
value is derived entirely on machine; no host-computed digit is stored in the
image.

| gate | image | deck token | one change | SIMH printed line |
|:--|:--|:--|:--|:--|
| **A** | `2048_VAR_A` | Y (VIDX=2) | none | ` 21 -0012.34  3000.00` |
| **B** | `2048_VAR_B` | Y (VIDX=2) | one machine word: Y value `1234.0 -> 5678.0` | ` 21 -0056.78  3000.00` |
| **C** | `2048_VAR_C` (= A) | Y (VIDX=2) | byte-identical restore | ` 21 -0012.34  3000.00` |
| **X** | `2048_VAR_A` (byte-identical to A) | X (VIDX=1) | deck digit `2 -> 1` only | ` 21 -0078.90  3000.00` |

All four reached `КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000`.
Gate X is the decisive proof that the lookup is **indexed by VIDX** and not a
fixed absolute cell: the image is byte-identical to A, only the deck token
changes, and the value switches from Y's cell to X's cell.

---

## 1. FRONT variable-token encoding (FACT, file:line)

`src/newcomp/FRONT.FTN`:

* `:54` `DATA MR5 /777005/`; `:349` `PRINT 9005, MR5, SEQ(I), TK(K), TO(K), TA(K), TB(K)`;
  `:376` `9005 FORMAT(1X,6I8)`. Emitted record: `777005 <seq> <TK> <TO> <TA> <TB>`.
* `:262` comment `C-- variable: X=1 Y=2 N=3 I=4, other upper-case letters ASCII-60`;
  `:263-269`: `VIDX=0; IF(CH.EQ.88) VIDX=1` (X), `89 -> 2` (Y), `78 -> 3` (N),
  `73 -> 4` (I), else `VIDX = CH - 60` (A=65 -> 5 ... Z=90 -> 30).
* `:271-274`: `TK(NTK)=2`, `TO(NTK)=0`, `TA(NTK)=VIDX`, `TB(NTK)=0`.
* `:234-259` (LIT, for contrast): `TK=1`, `TO=0`, `TA=SC=VAL*100/FRAC`, `TB=0`.

So a variable record is exactly `777005 <seq> 2 0 <VIDX> 0`, with VIDX in 1..30.
**FACT:** for Y, VIDX=2; for X, VIDX=1. `FRONT.FTN` was not modified.

### Card-buffer byte layout (FACT, C-oracle CORE, `oracle/vardump/core-pc.bin`)

The dispak card buffer is RLE-packed 8-bit ASCII, 6 bytes per machine word
(`0x80+n` = n spaces). For the deck card
`  777005       6       2       0       2       0` (48 chars), the CORE at our
entry PC `01770` (SKIP=6) shows:

```
064012  82 37 37 37 30 30   <2sp> 7 7 7 0 0
064013  35 87 36 87 32 87   5 <7sp> 6 <7sp> 2 <7sp>   <- TK=2 at byte 4
064014  30 87 32 87 30 a3   0 <7sp> 2 <7sp> 0 <35sp>   <- VIDX=2 at byte 2
```

The single-digit VIDX lands at **byte 2 of word `0o64014`**, the same byte that
held the first LIT digit in docs/104. It is reached by `utc 60000` +
`xta 4014` + `asx (64+24)<<41` + `aax 0o377` + `arx NEG31` (one's-complement
end-around carry: `0o62 - 0o31 -> 2`, docs/98 trick). MTR confirms the machine
values: `arx ... AU=...0062` (ASCII '2') then `ati 6(0) AU=...0002` (VIDX=2).

## 2. Zone N+2 symbol table (design + FACT)

Zone N+2 is disk logical `0o2352`. **Correction to the task's address claim:**
the RAM base is **0o21637**, not 0o1746 (0o1746 is the disk-zone number in the
2148/full-compiler setup of docs/63). This was measured by planting distinct
sentinels at N+2 offsets 0,1,2,4,8,...,0o400 in a copy and scanning the C-oracle
CORE: word k lands at RAM `0o21637 + k` with no holes (`build/probe_n2.py`,
`oracle/n2map/`). This is a FACT for our entry.

Layout (offsets relative to zone N+2; **0..525 are all-zero and free** in the
base image, **526..900 hold the required overlay table and were not touched**,
901..1023 free; docs/63):

| VIDX | name word (offset = VIDX) | value word (offset = 32+VIDX) |
|:--:|:--|:--|
| 1 (X) | `0o21640` = TEXT `X       ` = `0700000000000000` | `0o21700` = float(7890.0) `4657322000000000` |
| 2 (Y) | `0o21641` = TEXT `Y       ` = `0710000000000000` | `0o21701` = float(1234.0) `4551510000000000` |

6-bit TEXT is 8 codes per 48-bit word, code = ASCII-0x20, MSB first
(docs/20:26,44,54): X=0o70, Y=0o71, padded with 0o40 (space).
Values use the LIT convention (literal x100), so the unchanged converter's
`/10` yields 12.34 / 56.78 / 78.90. CORE verification of all four words is in
§4. The name words are seeded and CORE-verified but are **metadata only** in
this minimal contour; the machine lookup key is VIDX (see §5).

## 3. Minimal machine-code addition (10 halfwords; verbatim reuse otherwise)

Reused verbatim from the canonical docs/105 chain (`final_sign.S`): ABS+2+2 GOST
converter, `floor_acc` and `drop_last_ati` reclaims, shared `floor_int` VJM at
`0o30166`, sign block (`avx/aax/asx/aex/atx`, SIGNBIT/SHR22 in T8/T9), and
resident `*64 2004`. The only new stream is the variable reader (MTR addresses):

```
30114L utc 60000          ; arm card page for next instruction only
30114R xta 4014           ; ACC = card word RAM 0o64014
30115L asx SR24           ; T[7] reused: (64+24)<<41 (T[] unused by var path)
30115R aax M8             ; isolate ASCII byte 0o62
30116L arx NEG31          ; VIDX = 2
30116R ati 6              ; M[6] = VIDX
30117L utc 21677          ; arm modifier = 0o21637 + 32
30117R xta 0(6)           ; ACC = M[0o21677 + VIDX] = value word
30120L a/x TEN            ; same /10 as docs/104 LIT intrinsic
30120R atx EST            ; feed proven converter
```

Measured budget (`python3 build/c2_build.py --measure`): **90 halfwords =
45/58 zone words (13 words headroom); subroutine at 0o30166**. The canonical
LIT contour is 57/58; the 4-digit LIT reader (34 hw) was replaced by this
10-hw variable reader. No N+4 word, no new emulator mechanism, no C patch.
`T[7]` is reclaimed (the LIT 10*T[] assembly is gone); no low-RAM cell outside
the proven free `body[0o110..0o135]` range was used.

## 4. Raw evidence

### SIMH ACPU (authoritative, `runs/localprn_{A,B,C,X}.txt`, lines 100 / 114)

```
A   : " 21 -0012.34  3000.00" ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
B   : " 21 -0056.78  3000.00" ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
C   : " 21 -0012.34  3000.00" ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
X   : " 21 -0078.90  3000.00" ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
```

Console showed `ДATA:23.11.26`, `ДАЙ А0`, `ДАЙ А1`, `НОМВ` before the deck,
`БОБ:2048 :30(41)-0004, 2048 :41(41)`, `410300000000 ЗС5`, post-job-start `НОМВ`.

### Raw C-oracle MTR (oracle only, `logs/MTR_c2_excerpts.txt`, AU before each instruction)

```
===== MTR_A (Y=1234) =====                 ===== MTR_B (Y=5678) =====
30114L utc    60000   AU=...1146           30114L utc    60000   AU=...1146
30114R xta    64014   AU=...1146           30114R xta    64014   AU=...1146
30115L asx    2136    AU=1410346241630243  30115L asx    2136    AU=1410346241630243
30115R aax    2110    AU=0000014103462     30115R aax    2110    AU=0000014103462
30116L arx    2126    AU=0000000000062     30116L arx    2126    AU=0000000000062
30116R ati    6       AU=0000000000002     30116R ati    6       AU=0000000000002
30117L utc    21677   AU=0000000000002     30117L utc    21677   AU=0000000000002
30117R xta    21677(6)AU=0000000000002     30117R xta    21677(6)AU=0000000000002
30120L a/x    2116    AU=4551510000000000  30120L a/x    2116    AU=4653056000000000
30120R atx    2104    AU=4357331463146315  30120R atx    2104    AU=4510676314631463
30121L xta    2104    AU=4357331463146315  30121L xta    2104    AU=4510676314631463
30164R *64    2004    AU=20101600602017    30164R *64    2004    AU=120301601604017

===== MTR_X (X=7890, byte-identical image to A) =====
30115R aax    2110    AU=0000014103461     ; ASCII '1' -> VIDX=1
30116R ati    6       AU=0000000000001
30120L a/x    2116    AU=4657322000000000  ; X value loaded from 0o21700
30164R *64    2004    AU=160401602200017
```

### CORE symbol-table words (`oracle/c2A_F/core-pc.bin`)

```
VIDX=1 name RAM 0o21640 = 7000000000000000 (TEXT 'X')
VIDX=1 value RAM 0o21700 = 4657322000000000 (float 7890)
VIDX=2 name RAM 0o21641 = 7100000000000000 (TEXT 'Y')
VIDX=2 value RAM 0o21701 = 4551510000000000 (float 1234)
```

### Byte diffs

```
cmp 2048_VAR_A 2048_VAR_B = 9 bytes in 3 machine words:
  10419100-10419102, 10419132-10419134  (two recomputed zone-N+2 checksum copies)
  10419412-10419414                     (Y value word, zone N+2 offset 34)
cmp 2048_VAR_A 2048_VAR_C = EMPTY (byte-identical)
cmp deck_varY.b6 deck_varX.b6 = 1 byte, 1-based offset 167: octal 62 ('2') -> 61 ('1')
```

## 5. Maximum achieved, tradeoff, exact missing primitives

**Maximum achieved (FACT):** indexed lookup by a **single-decimal-digit VIDX**
using two seeded symbols (X=1, Y=2), with a one-machine-word patch changing the
selected variable's value and a one-deck-byte change selecting a different
variable. This is strictly more than the "single fixed variable by absolute
cell" fallback: gate X proves address = base + VIDX, not a fixed cell.

**Tradeoff:** the 4-digit LIT reader of docs/104/105 is **replaced**, not coexistent;
this image accepts VARIABLE records only. It is not a space constraint (13 words
are free): a TK-dispatch variant carrying both readers would still fit (rough
estimate 50/58, INFERENCE, not built).

**Exact missing primitives (not implemented, minimal task):**
1. **Two-digit VIDX assembly.** VIDX=10..30 (letters A..Z except X/Y/N/I) is
   emitted as two I8 digits; RLE places them at bytes 2 and 3 of `0o64014`.
   This reader consumes only byte 2 (would read the tens digit as VIDX).
   Needed: one more `asx SR16 / aax M8 / arx NEG31 / arx T(6)` chain (the proven
   docs/98 10*T[] trick) plus a 1..30 range check, about 5 zone words. It fits
   in the 13-word headroom (INFERENCE from measured halfword cost, not built).
2. **6-bit TEXT name comparison.** The name word is present but never compared;
   the contour trusts VIDX. A genuine symbol-resolution check needs an XOR of
   the table name word against the expected TEXT constant (e.g. `0o7100...`
   for Y) and a mismatch branch.
3. **Multi-record IR scanner.** Only one `777005` record (one card word) is
   consumed. `777001..777004`, record loops (777003), label allocation
   (777004), and `777010/777011` emitters (absent from the repo, docs/77) need
   a card-word scanner, record-kind dispatch and writable scratch across
   records; this is the remaining full-compiler gap (docs/104 §3).
4. **Runtime assignment.** Values are seeded into N+2 at build time; no IR
   operator evaluation (`+`, `-`, ...) is performed on machine.

## 6. Reuse (hard rule: reuse, do not reinvent)

| component | proven source | how reused |
|:--|:--|:--|
| base image + zone writer/checksum | `tools/build_zone2350_contour.py`, docs/87 | imported read-only; base SHA `a98e8109...` reproduced |
| converter, sign block, both reclaims, shared `floor_int`, `*64 2004` | docs/100/105 `final_sign.py` | imported verbatim as base class |
| card read `utc 60000` + `xta 4014`, `asx`/`aax`/`arx NEG31`, `/10` intrinsic | docs/93/98/104/105 | verbatim, shifted to the VIDX byte |
| low-RAM cells and T[] reclamation | docs/98/100 | verbatim mapping; T[7] reused as SR24 |
| SIMH ini/deck driver | docs/100/104/105 drivers | copied, WS path adapted, prn0 workspace-local |
| C-oracle MTR/CORE wrapper | docs/104/105 `oracle_run.py` | copied, WS path adapted |

New lines: only `c2_build.py` (the 10-halfword reader + N+2 table writer) and
the gate/probe scripts. No emulator mechanism, no repo edit, no C patch.

## 7. SHAs (SHA-256)

```
78990bd42e7366d39d85c3bf2608971e8535b300488a6dff1e86fe01db90815d  images/2048_VAR_A  (A, C, X; byte-identical)
799781cc2875c445d782a08454d6b4179b31566194de4bb6156b2431a802e106  images/2048_VAR_B  (one machine-word patch)
78990bd42e7366d39d85c3bf2608971e8535b300488a6dff1e86fe01db90815d  images/2048_VAR_C  (= A, restore)
91651687bc386ecc60d7e2fb9d1d5eece151c4c6490ebe38a12661c725352747  decks/deck_varY.b6 (Y token, VIDX=2)
315d23f396cedbdbf48b1f50f5dac72f534482e03476e34a410ddaefb485549c  decks/deck_varX.b6 (X token, VIDX=1)
388e6da393727e33d73d6e12c1bb32355f1538b16abc864583281f09c6d28c02  decks/deck_ir1234.b6 (source LIT deck)
802a081e801209f941c1dc6718fd380ac4fecd8432fad56339ad3ceba444f82a  runs/localprn_A.txt (SIMH ACPU)
cf7d6af87a47169b7249d8a8c4eb7f7d9e965e7e90b7d914ae8158557e034911  runs/localprn_B.txt
874a44db2042d78fda9c31db043e286047b6045ef2af9ecfd008b1f03d472f1c  runs/localprn_C.txt
3b2290d2754a57bcca37e488c124351514a3c9ec3029c434f24d06ac71f81f15  runs/localprn_X.txt
b72bee90457934d3801ad5993597e15ec8c518cd3b85dfc7f45cecbb0c790a7c  logs/MTR_c2_excerpts.txt
9e3311aa299be69634666c1ceec0fe7bc932327b78eb801cf222e2805fffcd28  oracle/MTR_A/out.txt (C MTR, oracle only)
58c5b08de3deab1a3b3e0305b226fe39df4467a4d607e44fadd60499f4cee1d4  oracle/MTR_B/out.txt
7b9ad54294cc2b7c1d401da3f28553d48ec2492267659298abf193780c28e2da  oracle/MTR_X/out.txt
16bb78104579f9845ab9463fa8bb717ab708f38ee4d049bb5b047a88e9b80903  oracle/c2A_F/core-pc.bin (CORE, oracle only)
5196e2b031c1dcd9ec161260b52292c1255e779f383b3d547c061b6c94c28c82  build/c2_build.py
```

## 8. PASS / FAIL

| # | gate | verdict |
|:--|:--|:--|
| 1 | FRONT variable encoding decoded with file:line citations (TK=2, TA=VIDX, X=1/Y=2/N=3/I=4, other ASCII-60) | **PASS** |
| 2 | Zone N+2 RAM base 0o21637 measured; table avoids offsets 526..900 | **PASS** |
| 3 | 6-bit TEXT name word + value word per variable, CORE-verified | **PASS** |
| 4 | On-machine VIDX read + indexed N+2 lookup + proven GOST path | **PASS** |
| 5 | Word count 45/58 (13 words headroom), no N+4, no dropped proven feature other than the replaced LIT reader | **PASS** |
| 6 | SIMH A: Y=12.34 -> `21 -0012.34`, КОНЕЦ ЗАДАЧИ | **PASS** |
| 7 | SIMH B: one machine-word patch Y=56.78 -> `21 -0056.78`, КОНЕЦ ЗАДАЧИ | **PASS** |
| 8 | SIMH C: byte-identical restore -> `21 -0012.34`, КОНЕЦ ЗАДАЧИ | **PASS** |
| 9 | SIMH X: byte-identical image, X token -> `21 -0078.90` (indexed lookup) | **PASS** |
| 10 | C-oracle MTR/CORE agree with SIMH | **PASS** |
| 11 | VIDX=10..30 (two-digit) decoded | **FAIL** (exact missing primitive in §5.1; fits in headroom, not built) |
| 12 | On-machine 6-bit TEXT name comparison | **FAIL** (§5.2) |
| 13 | `777001..777004`, multi-record scan, `777010/777011` | **FAIL** (out of scope; §5.3) |
| 14 | Runtime IR expression evaluation / assignment | **FAIL** (§5.4) |

## 9. FACT / INFERENCE

**FACT:** the source lines and CORE/MTR/SIMH results above; N+2 base 0o21637;
offsets 0..525 zero and 526..900 = overlay table; VIDX byte position; 45/58
words; one-word patch changes only the value plus two checksum copies; A and
restore byte-identical; all four jobs reached КОНЕЦ ЗАДАЧИ.

**INFERENCE / not proven:** the RAM base mapping was measured for offsets up to
0o400 only (we use 1,2,33,34, well inside that range); the two-digit VIDX cost
and the both-readers-dispatch estimate in §5 are halfword-count projections,
not built or run; VIDX values other than 1 and 2 were never exercised; the
name words are not compared on machine; FRONT was not rebuilt with a variable
expression (the emitted record was derived from source lines 262-274 and the
format at 349/376, and its card-buffer bytes were verified by CORE).

## 10. Evidence index

```
build/c2_build.py            minimal variable reader + N+2 table builder
build/make_gates.py          A/B/C images and Y/X decks
build/probe_n2.py            C-oracle sentinel CORE scan -> RAM 0o21637
build/oracle_run.py          C-dispak oracle wrapper (MTR/CORE only)
build/setup_c2.py            isolated SIMH ini, workspace-local prn0
build/drive_c2.py            SIMH driver (ДATA:/send-keys/ДАЙ/НОМВ)
images/2048_{VAR_A,VAR_B,VAR_C}
decks/deck_{varY,varX,ir1234}.b6
runs/localprn_{A,B,C,X}.txt  raw SIMH ACPU (authoritative)
runs/console_{A,B,C,X}.txt   raw SIMH console
oracle/{c2A_F,MTR_A,MTR_B,MTR_X,vardump,n2map}/  raw C MTR/CORE (oracle only)
logs/MTR_c2_excerpts.txt     clean MTR excerpts used in §4
```

DONE
