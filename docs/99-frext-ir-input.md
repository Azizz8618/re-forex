# FREXT/IR input to the zone-2350 contour: build-time FRONT records consumed on-machine

> ГЛАВНЫЙ РЕЗУЛЬТАТ: **PASS** для узкого утверждения. FRONT запущен как
> BUILD‑шаг системным ФОРЭКСОМ (0 ERR) и выдал IR‑запись `777005 6 1 0
> 900 0`; она введена в дек как карта, операнд попал в ОЗУ `0o64014`.
> Контур, отличающийся от `docs/96` двумя константами (`4012->4014`,
> `right16->right24`), читает её и гонит SQRT+GOST. SIMH A/B/C: `900 ->
> 21 3.00`, `400 -> 21 2.00` при том же образе (1 байт в деке), HALF‑патч
> -> `21 2.00`, restore -> `21 3.00`.
> Оговорка: декодируется только ведущая цифра LIT ×100; `777001..777004`
> не парсятся, `777010/777011` в репозитории отсутствуют. Полная компиляция
> ещё не доказана.

Date: 23.11.2026. Workspace `/tmp/.private/azizz/opencode/frext-input/`.
Repo, live disks, tmux session 0 and the C `dispak` sources were never edited.
Every attached disk is a COPY. C `dispak` is the **oracle only** (the only
emulator with MTR/CORE hooks, docs/88); authoritative A/B/C results are full
SIMH ACPU output. SIMH printer files were redirected to workspace-local files
because other concurrent sessions contend for the shared `ACPU/output.txt`
(the same disclosure as docs/94).

## VERDICT: PASS for the stated narrow claim

A single contour image reads a **FRONT-emitted IR record** from the target
deck's card buffer, decodes its LIT operand on the BESM-6, and drives the
proven docs/95/96 SQRT+GOST path. Four SIMH gates reached `КОНЕЦ ЗАДАЧИ`:

| gate | contour image | IR record card (only deck difference) | SIMH ACPU line |
|:--|:--|:--|:--|
| A baseline | `2048_irA` SHA `0c311170…` | `777005 6 1 0 900 0` (X=9.0) | ` 21 3.00 3.00` |
| (a) operand change | `2048_irA` **byte-identical** | `777005 6 1 0 400 0` (X=4.0) | ` 21 2.00 3.00` |
| (b) machine-word patch | `2048_irB` SHA `9249039d…` | same as A (X=9.0) | ` 21 2.00 3.00` |
| (c) restore | `2048_irRESTORE` SHA `0c311170…` (= A) | same as A (X=9.0) | ` 21 3.00 3.00` |

* Deck A vs (a): `cmp -l` = exactly **one byte** (1-based position `165`,
  zero-based `0o244`; octal `71`('9') → `64`('4')). This byte is the leading
  digit of the IR operand field `arg1`, produced by FRONT at BUILD time.
* Image A vs B: exactly **two machine words** (the `HALF` constant
  `f32(0.5)→f32(0.4)` plus the two recomputed zone-checksum copies). No
  host-computed result digit is stored anywhere.
* Image A vs RESTORE: byte-identical.
* Target deck contains **only** `*TRANS:OURMRK*,,412350` as translator;
  verified by grep: no `*FOREX`, `*FTN`, `*perso` (`§6`). The FRONT compile ran
  as a separate BUILD step on copies (system FOREX, explicitly allowed); its
  emitted IR text was injected as a deck card.

---

## 1. Exact layout of the IR records as emitted by FRONT (FACT)

All numeric IR records are printed by `src/newcomp/FRONT.FTN` as **text** by
system FOREX at BUILD time. Source citations (repo file, fixed-form lines):

| record | emitter | FORMAT | fields |
|:--|:--|:--|:--|
| `777001 <seq> <rule> <itype>` | `FRONT.FTN:50` (`DATA MR1 /777001/`), `:201` (`PRINT 9001, MR1, SEQ(I), IRULE, ITYPE`) | `:372` `9001 FORMAT(1X,4I8)` | 1 leading space + four 8-col right-justified decimal ints |
| `777002 <seq> <pos> <code>` | `FRONT.FTN:51`, `:206` | `:373` `9002 FORMAT(1X,4I8)` | same layout; `code` = ASCII of logical-line character |
| `777003 <nlines> <nrewrites>` | `FRONT.FTN:52`, `:371` | `:374` `9003 FORMAT(1X,3I8)` | 1 space + three I8 |
| `777004 <seq> 21 0 <label>` | `FRONT.FTN:53`, `:368` | `:375` `9004 FORMAT(1X,5I8)` | 1 space + five I8 |
| `777005 <seq> <kind> <op> <arg1> <arg2>` | `FRONT.FTN:54` (`MR5 /777005/`), `:349` | `:376` `9005 FORMAT(1X,6I8)` | 1 space + six I8 |

`arg1` of the `777005` LIT is the literal scaled by 100:
`FRONT.FTN:254` `SC = VAL*100/FRAC`, `:258` `TA(NTK) = SC`, and the LIT token is
`TK=1, TO=0` at `:255-259`. So `X=9.0` produces `arg1 = 900` and `X=4.0`
produces `arg1 = 400`. This is emitted for rule 31 assignments
(`:209 IF (IRULE .NE. 31) GOTO 560`).

**Observed output (FACT, from the real BUILD run, not inference).**
`frontbuild/x9/call_canonical.out:72` and `frontbuild/x4/call_canonical.out:72`,
verified byte-for-byte with `od -An -tx1`:

```
  777005       6       1       0     900       0     ; X=9.0
  777005       6       1       0     400       0     ; X=4.0
```

Byte columns (0-based, 49 chars including newline): pos 0 = space (1X),
pos 1..8 = `  777005`, pos 9..16 = seq `       6`, 17..24 = kind `       1`,
25..32 = op `       0`, **33..40 = `     900` / `     400` (arg1)**,
41..48 = `       0`. The `900`/`400` digits are at char positions **38,39,40**
(ASCII `0x39/0x30/0x30` or `0x34/0x30/0x30`).

**FREXT 777010 / 777011: not present in this repo (FACT).**
The only in-repo mention is `docs/77-onmachine-format-limit.md:7,25`:
`777011 <seq> <i> <K> <R> <W> <D>` (FORMAT descriptors) and
`READ X/1.0/ → 777010` were in a *copy* of FRONT.FTN in the now-absent
workspace `/tmp/.private/azizz/opencode/re-forex-io/`. A repository-wide grep
(`--include=*.FTN|*.md|*.py|*.txt|*.deck`) finds no emitter for 777010/777011;
`FRONT.FTN` emits only 777001..777005. **INFERENCE** (not reproducible here):
their text shape follows the same `1X,NI8` family, so they would be injected
as deck cards the same way. No claim is made about their exact field widths.

## 2. Where the records land in the card buffer at contour entry (FACT)

In the deck-only runs of docs/93/96 the FRONT stage was never run, so the
card buffer at RAM `0o64000..` contained only raw source text and no IR
records (`docs/93-deck-args-pass.md:107-113`, `docs/96-e2e-machine-contour.md:229`).
**FACT:** in our target deck the IR record is injected as a literal card; the
C-oracle CORE dump at contour entry (`BESM6_CORE_ON_PC=01770`, SKIP=6)
`oracle/dump_ir9/core-pc.bin`, decoded in `logs/card_buffer_ir9_at_entry.txt`,
shows (COSY RLE: `0x82`=2 spaces, `0x85`=5 spaces, `0x87`=7 spaces):

```
064012  82 37 37 37 30 30   .77700        <- marker 777005 (first 5 chars)
064013  35 87 36 87 31 87   5.6.1.        <- '5', seq 6, kind 1
064014  30 85 39 30 30 87   0.900.        <- arg1 = 900 at bytes 2,3,4
064015  30 a3 0a 0a 0a 0a   0.....
```

So the operand's leading digit (`'9'`=`0x39`, or `'4'`=`0x34` in deck (a)) is
**byte 2 of the word at 0o64014**. Page `0o64000>>10 = 0o150` is readable in
user mode (no MMU trap), as proven in docs/93/94. The contour reads it with
`utc 60000` + short `xta 4014` (effective `0o60000+0o4014 = 0o64014`),
`asx right24` (shift constant `(64+24)<<41`; SIMH `besm6_arith.c:525` shows
positive n = right shift), `aax 0o377`, `arx 0xD0`, `aax 0o377` → integer 9/4,
then the proven `e+x EMASK; e+x C105` integer→float normalization
(docs/90/96 §6), then verbatim docs/95 Newton SQRT and docs/89 GOST deposit.
Contour size: 23 code + 12 data = **35/58 words** (builder assertion).

**FACT (C-oracle MTR, `logs/MTR_irA_x9_excerpt.txt`, `logs/MTR_gates_excerpt.txt`):**

```
MTR 30115R utc    60000(0) AU=0000000030000     ; arm card-page modifier
MTR 30116L xta    64014(0) AU=0000000030000     ; address the IR operand word
MTR 30116R asx    147(7) AU=1410247114030207    ; card word 0o64014 = 0.900.
MTR 30117R arx    151(7) AU=0000000000071       ; ASCII '9' (0o71)  [x4: 0o64 '4']
MTR 30120R e+x    152(7) AU=0000000000011       ; integer 9          [x4: 11]
MTR 30121R atx    144(7) AU=4211000000000000    ; float 9.0          [x4: 4150...=4.0]
... a/x, a+x, a*x FPU ... aex/e+x/aax/asx/asx ...
MTR 30140R asx    156(7) AU=0000000000003       ; digit 3 COMPUTED ON MACHINE
MTR 30142L *64    2004(0)                        ; resident print
```

## 3. Minimum build-time step and deck cards (tested on copies)

1. **BUILD (system FOREX, allowed):** reuse
   `tests/plan-f77/71-front-base77/inject.py` + `compile.py` with a source deck
   whose only changed line is `X=9.0` (or `X=4.0`). The generated
   `build_canonical.deck` uses `*forex` + system FOREX 2.02
   (`inject.py:97-111`) and `compile.py:56-59` runs the C oracle on copies;
   `compile.py:68` parses `77700[1-4]` (the `777005` records were read directly
   from `call_canonical.out:72`). Result: 0 ERR on both build and call;
   emitted `  777005       6       1       0     900       0` (x9) / `400` (x4).
2. **Inject the emitted record verbatim as a deck card:**
   ```
   *NAME OURMRK
   *TRANS:OURMRK*,,412350
         PROGRAM MAIN
     777005       6       1       0     900       0
         END
   *EXECUTE
   *END FILE
   ```
   (`decks/deck_ir9.b6` / `deck_ir4.b6`; byte-identical except the `9`→`4`.)
3. **TARGET:** run only `*TRANS:OURMRK*,,412350`; no `*FOREX`/`*FTN`/`*perso`.

No monitor, loader, disk or emulator patch is needed. The contour image is
built by `scripts/build_ir.py`, which is `scripts/build_e2e.py` (docs/96)
with exactly two constant changes: `CARD_WORD 0o4012→0o4014` and
`SR16→SR24 (64+24)<<41`. All machine-code chains are reused verbatim.

## 4. Raw evidence and SHAs (SHA-256)

```
a98e81090d4b254554a0cd3ff8611438615de84fc012e8e2b70fbabc2ebdc796  images/2048_base (repo tool)
0c311170ee2f899bf0b832917125dee15e2067bf0d9b406de63164742190541f  images/2048_irA  (A, gate a, restore)
9249039d420946b64efeb35de3ae655376c032d85ef108781cbd223da8d343af  images/2048_irB  (gate b)
0c311170ee2f899bf0b832917125dee15e2067bf0d9b406de63164742190541f  images/2048_irRESTORE
8ae5f07a798b4a8c22af8e3d707f966812b3baf8ce78ed4b5e33fcf6a543b920  decks/deck_ir9.b6
bc93f4747656d69a63bb5b4ecba61be4e02ef8ecdc7582e20d447f4c1ea885bc  decks/deck_ir4.b6
95dd97350b179c1d9ba1319a236479a66dabbe23d92ad3f084868bf9a2b6eb6e  frontbuild/x9/FRONT_canonical_injected.FTN
d34e4c695e6827d03e8920ca6f4644aa619ee5053f27bd7c82e532ceb1caba2b  frontbuild/x4/FRONT_canonical_injected.FTN
0e5ec38c028706bb26d67376a5f9246bc9e61a1cbb16895b0d2165cd67918b1e  frontbuild/x9/build_canonical.out
16ad9856b700e05465c2570b0c77f29d876c4098c95153323a862907c13a3337  frontbuild/x9/call_canonical.out
35b3461df8a04d886a462a37cf57cfdba51f7c15ac75da5c92addd2538c69fdc  runs/localprn_irA_x9_local.txt   ACPU: 21 3.00 3.00
4df44a517399c8a931211f0d2f14db1c8406fe815e715dc3a020933019dc4d13  runs/localprn_irA_x4.txt       ACPU: 21 2.00 3.00
5a2e13680ac0474e39eb9996352209d8d69dcd1ca32a05410a1858a9bd3a9513  runs/localprn_irB_x9.txt       ACPU: 21 2.00 3.00
fcc1e40556b650aa4488fe89a6e071e9851359ee87e2cb4b10989235856ce7c2  runs/localprn_irREST_x9.txt    ACPU: 21 3.00 3.00
0aca55c99c86353e94685846bbef618e86916ccba677f922a8818bd83661eebc  oracle/irA_x9/out.txt (= MTR_rest)
86bbe8d0203c6f2101fcbcd95abfc52df2f788dc462ddd1415355d5f3a887469  oracle/MTR_x4/out.txt
2af19071c61579296031e57520dfd4d68cc00ab925f4159cb31d7b216096847d  oracle/MTR_b9/out.txt
1db5081c26fae7b746e7cd6e61ff07e3b636c754db1e46b2f14c30a121d8e098  logs/MTR_irA_x9_excerpt.txt
a0153535ce6a4ed8dfd7f7f7e94cd03563a1bc029f36ab87055d04a54f19fe76  logs/MTR_gates_excerpt.txt
da7abee3c0c0bd245699e42c995b9280c10383d6a9e503223d2636ae7516bfed  logs/card_buffer_ir9_at_entry.txt
```

C-oracle MTR window: `BESM6_MTR_LO=030114`, `BESM6_MTR_HI=030200`,
`BESM6_MTR_N=1200`, `BESM6_CORE_ON_PC=01770`, `BESM6_CORE_SKIP=6`.
The full ACPU files contain the literal lines ` 21 3.00 3.00` /
` 21 2.00 3.00` at line ~100 and ` КОНЕЦ ЗАДАЧИ` at line ~114.

## 5. FACT vs INFERENCE

| # | statement | marker |
|:--|:--|:--|
| 1 | FRONT emits 777001..777005 as `1X,NI8` decimal text; `777005` LIT `arg1 = literal*100` | FACT (`FRONT.FTN:50-54,201,206,349,368,371,372-376,254,258`) |
| 2 | Real BUILD run emitted `777005 6 1 0 900 0` / `... 400 0`, 0 ERR | FACT (`call_canonical.out:72`, build logs) |
| 3 | Target deck-only runs contain no IR records; they must be injected | FACT (docs/93/96; absent FRONT invocation) |
| 4 | Injected IR card lands at RAM 0o64012..0o64015; operand leading digit at 0o64014 byte 2 | FACT (CORE dump `core-pc.bin`, decoded log) |
| 5 | Same image, one-byte IR operand change → different printed digit (3 vs 2) | FACT (SIMH ACPU + C MTR) |
| 6 | One machine-word patch (HALF) → digit changes; byte-identical restore → digit returns | FACT (SIMH ACPU + SHAs) |
| 7 | Printed digits computed by BESM-6 FPU/asx, not Python | FACT (MTR ACC chain; builder stores no result digit) |
| 8 | 777010/777011 layouts follow `1X,NI8` | INFERENCE only (emitter absent from repo; docs/77 describes an absent workspace copy) |
| 9 | The contour reads only the **leading digit** of the 3-digit `arg1` (×100 scaled literal); it is not a general decimal-field decoder | FACT (disclosed limitation, §6) |
| 10 | `arg1` is read at a fixed card offset; no marker verification, no multi-record scan | FACT |

## 6. Honest scope: consuming IR is necessary, not sufficient

* **Proven here:** a genuine FRONT-produced `777005` LIT record, injected as a
  deck card, is read from the card buffer and its operand digit is computed
  on-machine through the SQRT+GOST path. The target deck invokes only our
  contour; FRONT ran only at BUILD time.
* **Minimal decode, disclosed:** the reader extracts byte 2 of word 0o64014,
  i.e. the leading digit of `arg1`. FRONT scales literals by 100, so for
  `X=d.0` with a single digit `d` this leading digit **is** the literal value
  (900→9, 400→4). Tens/ones digits, exponents, signs and multi-digit literals
  are not decoded. A general IR-field decoder (e.g. reconstruct 900/100 → 9.0
  from all three bytes) was costed at ≈63/58 words and does not fit the
  documented 58-word window without refactoring the GOST converter (docs/96 §7).
* **Not a general IR interpreter:** only the LIT record kind (`kind=1, op=0`)
  is consumed. `777001..777004` records are emitted by the BUILD step but are
  not parsed by this contour; no CODEGEN, no symbol table, no control flow.
* **Not FREXT READ/FORMAT:** 777010/777011 are absent from the current FRONT
  source (§1); formatted `READ(u,fmt)` remains blocked (docs/91/92/77).
* **Still required for "full compiler" (docs/63 §5):** FRONT coverage of the
  full Fortran grammar (BASE77 DO/FORMAT/PRINT are outside this contour),
  CODEGEN from IR, relocation into body RAM, multi-digit/negative/exponent
  float→GOST conversion, and elimination of fixed `21`/`.00` literal seeds.
* **Fixed seeds remain:** line prefix `21`, sign space, `.00` tail and Y field
  `3.00` are contour literals as in docs/89/90/95/96; only the X digit is
  computed. The mechanism constants (`BASE=0o30000`, `SR24=(64+24)<<41`,
  `MASK8=0o377`, `PD0=0xD0`, `EMASK`, `C105`, `M40`, `CWL16`, `HALF=0.5/0.4`)
  are disclosed setup values, never result digits.

## 7. Safety / reuse

No repo edits by this task (pre-existing concurrent changes noted but untouched:
` M tools/run_besm6_deck.py`, `?? tests/plan-f77/64-monitor-patch/`). No live disks, tmux session 0, SIMH
binary or C sources modified. All images/decks are copies; `/usr/local/share/besm6/2048`
was only read. Reused verbatim: repo tool `tools/build_zone2350_contour.py`
(checksum/zone writer, base SHA `a98e8109…` reproduced), docs/93/96 card-read
chain, docs/95 Newton SQRT, docs/89 float→GOST, docs/71 FRONT build step,
docs/96 SIMH harness (adapted only for paced sends and workspace-local printer).
New lines are limited to: two contour constants, the IR-card decks, the build
orchestration and this report.

## 8. Evidence index

```
scripts/build_ir.py               contour builder (35/58 words; two constants vs e2e)
scripts/{build_e2e,c_oracle,drive_manual,setup_workspace}.py
scripts/drive_case.py             original driver (race; superseded by drive_manual.py)
decks/deck_ir{9,4}.b6             A/B decks, one byte differs
frontbuild/{x9,x4}/               BUILD-step injected FRONT source, build/call decks, outputs
images/2048_{base,irA,irB,irRESTORE}
runs/localprn_ir*.txt             raw SIMH printer output (authoritative)
runs/console_ir*.txt              raw SIMH console captures
oracle/*/out.txt, core-pc.bin     raw C-dispak MTR/CORE (oracle only)
logs/MTR_*.txt                    clean MTR excerpts used in §2/§4
logs/card_buffer_ir9_at_entry.txt decoded card buffer at contour entry
```

DONE
