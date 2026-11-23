# e2e-contour: ONE contour reads a deck literal, computes SQRT on the BESM-6, converts to GOST and prints via *64

> ГЛАВНЫЙ РЕЗУЛЬТАТ: **PASS** — сквозная цепочка на БЭСМ‑6 в одном контуре
> (35/58 слов): слово карты `0o64012` -> ASCII‑цифра -> float -> машинный
> SQRT (Newton, 4 итерации) -> GOST‑цифра -> `*64`. Три гейта SIMH с
> `КОНЕЦ ЗАДАЧИ`: (a) байтово тот же образ, `X=9.0`/`X=4.0` ->
> `21 3.00`/`21 2.00`; (b) правка одного слова контура (`HALF` 0.5->0.4) ->
> `21 2.00`; (c) restore -> `21 3.00`. Никакой питоновской цифры в выводе.
> Полная 2+2‑цифровая интеграция требует 79/58 слов, поэтому честно
> заявлена однозначная печать. DSQRT/знак/`READ(u,fmt)` остаются пределами.

Date: 23.11.2026. Workspace: `/tmp/.private/azizz/opencode/e2e-contour/`.
Repo, live disks, tmux session 0 and the C `dispak` sources were **never** edited.
Every attached image was a COPY; SIMH used stock `attach -n prn0/prn1`, the
`ДATA:` boot marker via `capture-pane`, all input via `send-keys`, `ДАЙ А0` /
`ДАЙ А1` / `НОМВ` before the deck, post-job-start `НОМВ`, and isolated tmux
sockets. C `dispak` was **oracle only** (the only emulator with the MTR/CORE
hooks, docs/88); all authoritative A/B/C results are full SIMH ACPU output.

## VERDICT: PASS (decisive end-to-end A/B/C) - single-digit output, 35/58 words

One contour (one machine image) proves the whole chain in user mode:

```
deck card word at RAM 0o64012  --(utc 60000 + xta 4012)-->
ASCII digit '9'  --(asx/aax/arx/aax + e+x/e+x)-->
BESM float 9.0  --(Newton x=(x+S/x)/2, 4 iters: a/x, a+x, a*x)-->
float ~3.000065  --(aex/e+x/aax/asx/asx)-->
packed GOST digit 3  --(arx/atx 0o2006 + *64 2004)-->
"21 3.00 3.00"
```

All four SIMH cases reached `КОНЕЦ ЗАДАЧИ`.

### Decisive gates (authoritative: SIMH ACPU, stock `-n prn`)

| gate | contour image | deck literal | one change | SIMH ACPU printed line |
|:--|:--|:--|:--|:--|
| **A (baseline)** | `2048_e2e_A` SHA `57ed6a27...` | `X=9.0` | none | ` 21 3.00 3.00` |
| **Gate (a) deck change** | `2048_e2e_A` **byte-identical** (same SHA) | `X=4.0` | **only the deck's ASCII digit** (one byte, 0x39->0x34) | ` 21 2.00 3.00` |
| **Gate (b) code patch** | `2048_e2e_B` SHA `588c7c84...` | `X=9.0` | **one contour word**: Newton half-step `HALF = f32(0.5) -> f32(0.4)` at RAM `0o30160` | ` 21 2.00 3.00` |
| **Gate (c) restore** | `2048_e2e_RESTORE` SHA `57ed6a27...` (byte-identical to A) | `X=9.0` | restored | ` 21 3.00 3.00` |

* Gate (a): the contour image SHA is IDENTICAL in A and gate (a); only the deck
  changes. `cmp -l deck_x9.b6 deck_x4.b6` = exactly one byte (offset `0o210`,
  `0o71`('9') -> `0o64`('4')).
* Gate (b): `cmp -l 2048_e2e_A 2048_e2e_B` = one 6-byte machine word in zone N+3
  plus the two recomputed zone-checksum copies. No host-computed result digit
  is stored anywhere; the printed digit changes because the on-machine Newton
  fixed point changes from sqrt(9)=3 to ~2.45 -> digit 2.
* Gate (c): `cmp 2048_e2e_A 2048_e2e_RESTORE` is EMPTY (byte-identical).

Deck contains only `ДИС 41(2048)^` (translator) and `*TRANS:OURMRK*,,412350`;
standard `PROGRAM MAIN` / `X=d.0` / `END` / `*EXECUTE` / `*END FILE` framing.
No `*FOREX`, `*FTN`, `*perso` (verified by `strings`; grep found NONE).

---

## 1. What the contour actually executes (FACT, raw C-oracle MTR, full excerpt in `logs/MTR_v_A_x9_excerpt.txt`)

Entry is the proven same-length substitution at body `0o11` (RAM `0o1770`):
`LONG uj 30114`. Zone N+3 (RAM `0o30114..0o30205`) holds routine + constants;
M[7]=`0o30000` is the base register (SHORT reg7 operands). The card read is the
only M20=`0o60000` modifier access. AU values are the ACC at each halfword.

```
MTR 30114L utc    30000(0) AU=0000000001146      ; arm base modifier
MTR 30114R xta    30143(0) AU=0000000001146      ; ACC = 0o30000 (BASE cell)
MTR 30115L ati    7(0)     AU=0000000030000      ; M[7] = 0o30000
MTR 30115R utc    60000(0) AU=0000000030000      ; arm card-page modifier
MTR 30116L xta    64012(0) AU=0000000030000      ; ACC = card word (0o60000+0o4012)
MTR 30116R asx    147(7)   AU=4145407516227060   ; card word: bytes 86 58 3d 39 2e 30 ('X=9.0')
MTR 30117L aax    150(7)   AU=0020626036471      ; asx right16 -> digit byte low
MTR 30117R arx    151(7)   AU=0000000000071      ; aax 0o377 -> ASCII '9' (0o71 = 0x39)
MTR 30120L aax    150(7)   AU=0000000000411      ; +0xd0 -> 0x109
MTR 30120R e+x    152(7)   AU=0000000000011      ; aax 0o377 -> integer 9
MTR 30121L e+x    153(7)   AU=1551000000000000   ; +63 normalize
MTR 30121R atx    144(7)   AU=4211000000000000   ; +41 -> BESM float 9.0 (NUM)
MTR 30122R atx    145(7)   AU=4211000000000000   ; x0 = S
MTR 30123R a/x    145(7)   AU=4211000000000000   ; S / x  (FPU divide)
MTR 30124L a+x    145(7)   AU=4050000000000000   ; S/x + x (FLOATING add)
MTR 30124R a*x    146(7)   AU=4212000000000000   ; * 0.5  (HALF)
MTR 30125L atx    145(7)   AU=4152000000000000   ; x1 = 5.0  -> ... 4 iterations ...
MTR 30134R atx    145(7)   AU=4114000140000600   ; EST ~ 3.000065 = sqrt(9) on machine
MTR 30135R aex    152(7)   AU=4114000140000600   ; complement exponent (127-e)
MTR 30136L e+x    153(7)   AU=3654000140000600   ; control exponent = 168-e
MTR 30136R atx    155(7)   AU=6314000140000600   ; store on-machine asx control word
MTR 30137R aax    154(7)   AU=4114000140000600   ; isolate 40-bit mantissa
MTR 30140L asx    155(7)   AU=14000140000600     ; mantissa -> integer digit
MTR 30140R asx    156(7)   AU=0000000000003      ; digit 3 (COMPUTED ON MACHINE)
MTR 30141L arx    2006(0)  AU=0000000600000      ; digit << 16
MTR 30141R atx    2006(0)  AU=40041700607000     ; GOST word A = [2][1][15][3][14][0]
MTR 30142L *64    2004(0)  AU=40041700607000     ; resident print
 21 3.00 3.00
 КОНЕЦ ЗАДАЧИ
```

This closes the full chain: deck -> on-machine digit extraction -> on-machine
float -> on-machine intrinsic -> on-machine float->GOST conversion -> resident
`*64`. Every digit in `3.00` under A/B comes from BESM-6 instructions.

## 2. Raw SIMH ACPU evidence (authoritative)

`runs/acpu_{A_x9,A_x4,B_x9,REST_x9}.txt`, line ~100 and the completion line:

```
A_x9     :  " 21 3.00 3.00"   ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0007777620000000"
A_x4     :  " 21 2.00 3.00"   ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0007777620000000"
B_x9     :  " 21 2.00 3.00"   ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0007777620000000"
REST_x9  :  " 21 3.00 3.00"   ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0007777620000000"
```

`acpu1_*` are empty; stock `-n prn` output is in `output.txt`. Console showed
`B075-1 410300000000` and `ОЗ(075) 410300000000` (md41 = our contour).

## 3. SHAs (SHA-256)

```
a98e81090d4b254554a0cd3ff8611438615de84fc012e8e2b70fbabc2ebdc796  images/2048_base (repo tool, reproduces docs/87)
57ed6a2710a378b2700ef17fd614bef9de13392509ab54281c5f8490eed5b52c  images/2048_e2e_A        (A and gate-(a), byte-identical)
588c7c843e859d6a7c26b10978b0d6d8b8cce7c2556201b24b28e47b1b328021  images/2048_e2e_B        (gate (b), one word patched)
57ed6a2710a378b2700ef17fd614bef9de13392509ab54281c5f8490eed5b52c  images/2048_e2e_RESTORE  (gate (c), = A)
43950bb4385cf7eb547daab4f317feaeb4f64facb67a6166430ddcc648af6192  decks/deck_x9.b6         (X=9.0)
51ac42f3fdd5a71a4bda6bcdfa6fc701b84f012e20a11b3f813091150d87567f  decks/deck_x4.b6         (X=4.0)
1d93c468c1acf7b6c9d7ac5f002336ce4580d6d716fbc1694aabd605c9bbeae2  decks/deck_trans.b6
224c2a0f02780d42f0fdcae8685f02311400c68b18c9ea53bd448d1333c7d61e  runs/acpu_A_x9.txt
c290b5dda535808daf06d3f2539dc932c62d93ffda9138bdc7f7a083e9701a58  runs/acpu_A_x4.txt
53cb4990068fc8001aaae9974e9740180a8c1e055114c0b31562207895941565  runs/acpu_B_x9.txt
1c370d1a64fcf64937dbc55d127230495018af511d2bbb4d127ed6371b4fa929  runs/acpu_REST_x9.txt
816f0ae31b3541de1fd4900a112fcd456de5396feb0187cde8a12253cf7bf18a  oracle/v_A_x9/out.txt (C MTR)
816f0ae31b3541de1fd4900a112fcd456de5396feb0187cde8a12253cf7bf18a  oracle/v_REST_x9/out.txt (= A, byte-identical)
6a9b47a2101e666d1e1184d4e6f0a8b351afd62c354fa49ef50c206aaa2e1a2a  oracle/v_A_x4/out.txt
2b1861cc2c5176a8ec0eba94ac78a3eff16abc46fd635785bcc197a8258d5321  oracle/v_B_x9/out.txt
```

C-oracle MTR window: `BESM6_MTR_LO=030114`, `BESM6_MTR_HI=030200`,
`BESM6_MTR_N=1200`, `BESM6_DD_DEBUG=1`, `BESM6_CORE_ON_PC=01770`,
`BESM6_CORE_SKIP=6`.

## 4. Reuse of proven code (hard rule: reuse, do not reinvent)

| component | proven source | how reused |
|:--|:--|:--|
| base image + zone writer/checksum | `tools/build_zone2350_contour.py`, docs/87 | imported read-only; base SHA `a98e8109...` reproduced exactly |
| entry substitution `uj 30114` at `0o1770` | docs/89, ftgost-contour | verbatim |
| deck card read `utc 60000` + `xta 4012` and ASCII->digit | docs/93, `build_deckargs3.py` | verbatim (`asx right16`, `aax 0o377`, `arx 0xd0`, `aax 0o377`) |
| integer digit -> float via `e+x` normalization | docs/90, `build_own2.py:digit()` | reused mechanism (see bug note in §6) |
| Newton SQRT (a/x, a+x FPU, a*x, 4 iterations) | docs/95, `machine-intr/build.py:ops_sqrt` | verbatim |
| float->GOST converter (aex/e+x/aax/asx/asx/arx/atx/*64) | docs/89, `machine-intr/build.py:converter` | verbatim |
| GOST word A layout (prefix 21, digit byte zeroed) | docs/89/90/95 | verbatim |
| SIMH ini/deck driver (capture-pane ДATA:, send-keys, ДАЙ A0/A1, НОМВ, stock -n prn, copies, isolated tmux) | deck-args / ftgost-multi drivers | copied, only `WS` path adapted |
| C-oracle MTR wrapper | deck-args `c_oracle.py` | copied, only `WS` path adapted |

New lines are limited to: the (b) one-word `HALF` A/B patch, the composition
itself, and the integer->float fix in §6. No new emulator mechanism.

## 5. FACT / INFERENCE

**FACT (observed):**
- All four SIMH cases printed the stated line and reached `КОНЕЦ ЗАДАЧИ`.
- With the contour image SHA byte-identical, changing exactly one deck byte
  (`9`->`4`) changes the printed digit `3`->`2` (gate a).
- Patching exactly one contour word (`HALF` 0.5->0.4) changes the printed digit
  `3`->`2`; restoring the byte-identical image returns `3` (gates b/c).
- C-oracle MTR shows the card word read at `0o64012`, `asx`/`aax`/`arx` producing
  ASCII `0o71` and integer 9, `aex`/`e+x` producing the on-machine control word,
  FPU `a/x`/`a+x`/`a*x` executing, and `asx` producing the integer digit 3.
- MMU page `0o150` (`0o64000>>10`) is readable in user mode; no MMU trap occurred
  in either SIMH or C oracle (consistent with docs/93). Only this page was
  exercised.
- The built contour uses 23 code + 12 data = 35 of 58 words (builder assertion
  and `scripts/budget.py`).

**INFERENCE / not proven:**
- That the same deck path works for other card-buffer pages (only page `0o150`
  tested; docs/88 shows other `utc` targets can trap).
- That arbitrary float exponents/negative inputs work in the converter (only
  positive single-digit results with exponent in the converter window exercised).
- The exact store instruction that filled `0o64000` was not traced; identifying
  the buffer with the `AIO` band rests on `boot.asm:3` + CORE bytes (docs/93).

## 6. Correction to a proven piece (FACT, discovered here)

docs/93 / `build_deckargs3.py` convert the ASCII digit to a BESM float with
`asx left41` + `arx FBASE`. That works ONLY for single-bit digits 1, 2, 4, 8:
the digit's binary bits are added into the 7-bit exponent field. With deck
`X=9.0` the first build produced float 256 (exponent 0o111) and printed `21 ×.00 3.00`
(C-oracle evidence: first oracle run, `logs/oracle_A_x9.log`, GOST byte `0x14`=20).
I replaced those two halfwords with the docs/90 `e+x EMASK; e+x C105` integer->float
normalization (reusing EMASK/C105 already present), which produces exact
`f32(9.0)` = `4211000000000000` on the machine (MTR 30121R). This is the only
functional deviation from the predecessor's digit-to-float step; the final
A/B/C/A is entirely with the corrected contour. A SIMH `set cpu debug` trace
was attempted three ways (bp 0o30114, bp 0o1770, trace-on-start); none caught
the routine at the right instant (routine runs at contour entry, before the
driver's job-start/arm point), so the instruction-level MTR evidence in this
report is from the C oracle (the emulator that has the MTR hooks, docs/88).

## 7. Exact 58-word budget; largest honest subset (task item 4)

`scripts/budget.py` measures the instruction streams of the proven builders:

| variant | code words | data words | total | verdict |
|:--|--:|--:|--:|:--|
| **built: deck + SQRT + 1 GOST digit** | 23 | 12 | **35 / 58** | PASS, fully proven end-to-end |
| deck + SQRT + 2 int + 2 frac GOST digits | 61 | 18 | **79 / 58** | OVER by 21 words |
| deck + ABS + 2 int + 2 frac GOST digits | 51 | 17 | **68 / 58** | OVER by 10 words |

The 4-digit converter alone is 45 code + 13 data = 58 words (measured; reproduces
docs/90), i.e. the full budget. Adding deck-read (9 halfwords + 3 data cells)
and the intrinsic (22 halfwords + 2 data cells for SQRT) cannot fit. Refactoring
the four repeated floor/deposit blocks into a subroutine might save ~20 words but
would still leave the SQRT variant over budget and was not attempted (INFERENCE).
Per the task, I did **not** fake a wider result: the largest honestly working
subset that keeps ALL FOUR links (deck -> intrinsic -> on-machine float->GOST ->
`*64`) is **single-digit output**. The fixed `21` prefix, the `.00` tail, and the
Y field `3.00` are seeded contour literals (as in docs/89/90/95); only the X
integer digit is computed and deposited at runtime.

## 8. Known limits preserved honestly

* **DSQRT infeasible** (docs/95 §6): SIMH has ONE 48-bit float format; no double
  FPU opcode. A real DSQRT needs software hi/lo double arithmetic (>100
  instructions), far beyond 58 words. No DSQRT result was produced.
* **Sign unsupported in converter** (docs/90 §5): the GOST sign byte is the fixed
  seed `GOST_SPACE` (15). Negative values were not exercised; the sign is NOT a
  machine-computed digit here.
* **Descriptor-driven `READ(u,fmt)` blocked** (docs/93 §1.2 + docs/77/78):
  FREXT/IR records (777010/777011) are absent in a deck-only run, and `*50`
  extractcode aborts from the contour under SIMH. Input here is ONLY the raw
  card-buffer literal at `0o64012` via `utc 60000` + `xta 4012`. This contour
  proves *deck-to-contour argument transfer*, NOT that the translator compiles
  the source program (no FRONT/CODEGEN/EMIT records; the routine is hand-built).
* No generic multi-digit claim: the routine was exercised for deck digits 9 and 4
  and HALF 0.5/0.4 only.

## 9. Setup literals disclosed (NOT counted as success arguments)

* Deck literals: `X=9.0` / `X=4.0` (the ASCII digit is the argument, read from the
  card image, not Python-supplied as a result).
* Gate-(b) patch literal: `HALF = f32(0.5)` -> `f32(0.4)` (the Newton half-step
  constant; changing it changes the computed intrinsic result).
* Mechanism constants (not result digits): `BASE=0o30000`, `SR16=(64+16)<<41`,
  `MASK8=0o377`, `PD0=0xD0`, `EMASK=0o177<<41`, `C105=0o151<<41`,
  `MASK40=0xFFFFFFFFFF`, `CWL16=0o60<<41`.
* Fixed GOST text: line prefix `21`, sign space (15), `.00` tail, Y field `3.00`.
* `f32()` in the builder only encodes these disclosed constants; it never
  computes or stores the printed digit.

## 10. Evidence index

```
scripts/build_e2e.py            reproducible contour builder (35/58 words)
scripts/budget.py               exact word-budget measurement
scripts/setup_workspace.py      per-case SIMH ini (copies, stock -n prn)
scripts/drive_case.py           isolated SIMH driver (ДATA:/send-keys/ДАЙ/НОМВ)
scripts/c_oracle.py             C-dispak oracle (MTR/CORE), oracle only
decks/deck_x9.b6 / deck_x4.b6   A/B decks (one byte differs)
images/2048_{base,e2e_A,e2e_B,e2e_RESTORE}
runs/acpu_{A_x9,A_x4,B_x9,REST_x9}.txt    raw SIMH ACPU
runs/console_{A_x9,A_x4,B_x9,REST_x9}.txt raw SIMH console
runs/ini_{A_x9,A_x4,B_x9,REST_x9}.ini     per-case SIMH configs (all copies)
oracle/v_{A_x9,A_x4,B_x9,REST_x9}/out.txt raw C MTR/ACPU logs
logs/MTR_v_A_x9_excerpt.txt     clean full-chain C MTR excerpt (§1)
logs/oracle_A_x9.log            first (buggy) build evidence (§6)
logs/build_base.log, logs/setup_*.log, logs/drive_*.log
```

DONE
