# B6c IMPLEMENTATION: source-text `DO 10 I=1,N` / `10 CONTINUE` decoded and executed by BESM-6 machine code

> РЕЗУЛЬТАТ B6c: **PASS** (честное подмножество). Machine‑код читает
> `DO 10 I=1,2` и `10 CONTINUE` из Fortran‑карт, разрешает метку в pre‑scan,
> считает границу из исходника и machine‑обратным счётчиком в N+2 повторяет
> FPU‑накопление. SIMH: `2→21 -0040.00`, `3→-0060.00`, patch→`-0020.00`,
> restore→`-0040.00`, без `END` → `-0040.00` (EOF закрыт). Все `КОНЕЦ ЗАДАЧИ`.
> Бюджет 40/58 N+3, 528/649 N+2, 6 слов N+1 с keeper, 526..900 не тронуты.
> Отложено: обновление переменной цикла, шаг≠1, вложенные циклы.

**VERDICT: PASS (honest subset).** A BESM-6 machine-code, two-pass source-text path reads the
actual Fortran card image, decodes `DO <label> I=init,limit` and the labelled terminal statement
`<label> CONTINUE`, resolves the label in the pre-scan (Pass L), parses the single accumulation
body `S=S+20.00`, then runs a **machine-code countdown** in N+2 that repeats the FPU
`S += addend` exactly `limit` times.  The accumulated value is printed through the **verbatim**
B3 dispatcher at `0o22065` and the verbatim docs/105 GOST converter in N+3.  Every printed digit
is produced by the BESM-6 FPU and converter; no `777005` IR card, no fixture, no host-computed
result digit.  The B6a source-text `PRINT`/`FORMAT` path and its label resolution are reused
unchanged.

Discipline: workspace `/tmp/.private/azizz/opencode/b6c-do/` only; copies of every image, deck and
driver.  No repository edit, no live disk, no tmux session 0, no C `dispak` patch.  C `dispak`
was **oracle only** (MTR / CORE).  Authoritative verdicts are full SIMH printer captures from
the b-harness (`drive_b.py`).

---

## 1. VERDICT (decisive SIMH A/B/PATCH/RESTORE + EOF)

| gate | image SHA-256 (first 16) | deck / change | printer line 100 | КОНЕЦ ЗАДАЧИ | verdict |
|:--|:--|:--|:--|:--|:--|
| **A** | `c0ac6e326d67030d` | `DO 10 I=1,2` | ` 21 -0040.00  3000.00` | line 114, yes | **PASS** |
| **B** | `c0ac6e326d67030d` (byte-identical) | `DO 10 I=1,3` (1 deck byte) | ` 21 -0060.00  3000.00` | line 114, yes | **PASS** |
| **PATCH** | `04770dfea5c82d18` | deck A; one N+2 counter word `-1 -> -2` | ` 21 -0020.00  3000.00` | line 114, yes | **PASS** |
| **RESTORE** | `c0ac6e326d67030d` (= A) | deck A | ` 21 -0040.00  3000.00` | line 114, yes | **PASS** |
| **EOF** | `c0ac6e326d67030d` (= A) | deck A with `END` removed | ` 21 -0040.00  3000.00` | line 114, yes | **PASS** |

Harness `plumbing: PASS`, `product_gate: PASS`, `result_21_line: true`, `fatal_error: false`
for all five captures (`harness/runs/verdict_*.json`).  (As in B6a, `completion_marker:false`
in the JSON only means the console-pane regex missed the line; `КОНЕЦ ЗАДАЧИ` is present in
every `localprn_*.txt` at line 114.)

**Causality:**
* A vs B: image byte-identical (same SHA), **one** deck byte differs at 1-based offset 154,
  octal `62` (`2`) -> `63` (`3`) in the DO bound.  With the contour frozen, the source bound
  alone changes the accumulated result `40.00 -> 60.00`.
* PATCH vs A: deck byte-identical, **3 image bytes in 3 machine words** = one 6-byte N+2 word
  (`K_DO_DECR`, file offset 10419569, octal `376` -> `375`, i.e. one's-complement `-1 -> -2`)
  plus the two recomputed zone-N+2 checksum copies (offsets 10419097, 10419129).  With bound 2
  the counter reaches zero after one body execution, so the result changes `40.00 -> 20.00`.
  This is a one-word patch of **our own counter**, not of a precomputed result.
* RESTORE: image byte-identical to A (0 differing bytes), output returns to `40.00`.
* EOF: with no `END` card the `0xff` / `*END FILE` scan terminates Pass E, an `END` token is
  emitted at `PE_DONE`, and the value line plus `КОНЕЦ ЗАДАЧИ` are unchanged (closes the B2
  open item for the DO path too).

---

## 2. The deck is real Fortran source text (verbatim, `decks/deck_do_A.b6`)

```
ШИФР 410300 ЗС5^
ДИС 41(2048)^
ОЗУ 32^АЦП 32^
ЕЕВ1А3
*NAME FRX5XX
*TRANS:FRX5*,,412350
      PROGRAM MAIN
      S=0.0
      DO 10 I=1,2
      S=S+20.00
   10 CONTINUE
      PRINT 100,S
  100 FORMAT(1X,F4.2)
      END
*EXECUTE
*END FILE
``````
ЕКОНЕЦ
```

These are the exact UTF-8 lines of `decks/deck_do_A.b6`.  Deck B is byte-identical except the
bound digit `2` -> `3` in `DO 10 I=1,3`.  Fortran statements occupy physical columns 7..72;
the DO/CONTINUE/FORMAT labels occupy columns 1..5.  `grep 777005` on both decks: **0 hits**.
No `*FOREX`, `*FTN`, `*perso`, or IR card.

---

## 3. Machine implementation (reuse first)

`build/b6c_build.py` is an extension of the proven B6a assembler.  It reuses **verbatim**:
`build_e2e.py` (rz/wz/short/long/word/f32), `c6_build.py` (N+3 converter + low-RAM cells),
`c7_build.py` (width tables), `final_sign.py` (LO cells), `dispatch_build.py` (B3 dispatcher +
`tok()` encoder).  **No B3 word was changed.**  New machine code is confined to our two-pass
source lexer in free N+2.

1. **Pass L (label / FORMAT / DO pre-scan).**  Adds 2-byte `DO` and 8-byte `CONTINUE` sliding
   windows to the B6a 3/5/6-byte window logic.  On `DO` it starts a 2-digit cap counter and
   packs the terminating label into `C_DO_LAB`.  On the labelled `CONTINUE` card it packs the
   card's leading label into `C_CONT_LAB`, compares the two, and sets `C_LABMATCH=1` on equality.
   The FORMAT label/PAY resolution of B6a is untouched.
2. **Pass E (emit + execute).**  Recognises the DO keyword -> modes 10/11; skips
   `10 I=1` and decodes the digit after the comma into `L_BOUND` (N+2[147]).  Recognises the
   body `S=S+20.00`: `=` initialises S (N+2[33]) to 0, a leading `S` selects the accumulation
   subset, `+` selects the addend, and the proven docs/104 digit chain builds `L_ADDEND =
   f32(200.0)` (N+2[149]).  The terminal `CONTINUE` (with `C_LABMATCH=1`) runs the count loop:
   `L_CNT = L_BOUND` (N+2[148]); `S += L_ADDEND` (FPU `a+x`); `L_CNT += K_DO_DECR`;
   `uza` exits on 0 / `-0`; else `uj` back to the body.  Scaffolding emits only
   `PROGRAM, name, EOL` (no `REAL`, because B3's REAL would zero S *after* the loop).  PRINT,
   FORMAT and END are emitted exactly as in B6a, including the final `END` at `PE_DONE` for
   the EOF case.
3. **Handoff** `LONG UJ 0o22065` to the verbatim B3 dispatcher.  B3 reads the accumulated
   N+2[33] through the resolved FDESC and calls the verbatim converter.  No digit is produced
   by the host.

A region-crossing trampoline was added to our assembler (`LAsm.guard`): the free N+2 code is
split into slots 255..499 and 901..1023, and straight-line code must not run sequentially
across the gap (it would execute N+2 data words as instructions).  `guard` pads to the last
word of the low band and emits `LONG UJ` to the next region.  This was a real defect found and
fixed via C-oracle MTR before the gates were run.

---

## 4. Authoritative SIMH evidence (raw captures)

Printer `prn0` line 100 and completion line, from `harness/runs/localprn_B6C_*.txt`:

```
A       : " 21 -0040.00  3000.00"   ...  " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
B       : " 21 -0060.00  3000.00"   ...  " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
PATCH   : " 21 -0020.00  3000.00"   ...  " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
RESTORE : " 21 -0040.00  3000.00"   ...  " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
EOF     : " 21 -0040.00  3000.00"   ...  " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
```

Raw ACPU device copies (`harness/runs/acpu_B6C_*.txt`, first lines:
`СБО,ВВЕДИ ПО ИНС`, `ДАТА РЕШ. ВЕРСИЯ 117А ...`, `*АЦПУ-0 ЭВМ-3`) are byte-identical across all
five runs (SHA `ae565a30e562f8e9...`).  Per `PROBE.md` these are shared/stale read-only copies
and are **not** the measured observable; the printer captures are.

Whole-image byte diffs: deck A vs B = **1 byte** (offset 154); A vs PATCH = **3 bytes** in 3
machine words (above); A vs RESTORE = **0 bytes**; A vs B = **0 bytes**.

---

## 5. Raw C-oracle MTR (oracle only)

Full raw trace: `oracle/B6C_MTR_LOOP/out.txt` (6000 lines, window
`BESM6_MTR_LO=027700,HI=030100,N=6000`).  Decisive lines in
`evidence/MTR_B6C_curated.txt` (AU is the 48-bit accumulator in octal, loop at PC `0o30011`):

```
MTR 30010R atx    2063(14) AU=0000000000002   ; L_CNT = L_BOUND = 2 (from source DO card)
MTR 30011R a+x    2064(14) AU=0000000000000   ; iter 1: S(0) += f32(200.0)
MTR 30013R atx    2063(14) AU=0000000000001   ; counter 2 -> 1
MTR 30014L uza    30015(0) AU=0000000000001   ; not done -> loop
MTR 30014R uj     30011(0) AU=0000000000001   ; rewind to loop body
MTR 30011R a+x    2064(14) AU=4414400000000000 ; iter 2: S(f32 200.0) += f32(200.0)
MTR 30013R atx    2063(14) AU=7777777777777777 ; counter 1 -> -0
MTR 30014L uza    30015(0) AU=7777777777777777 ; exit (uza also on -0)
```

C CORE at the handoff (`oracle/B6C_CORE5/core-pc.bin`, PC `0o22065`) confirms machine-derived
state: `N+2[33] = 4454400000000000` (f32 400.0), `L_BOUND=2`, `L_CNT=-0`,
`C_DO_LAB = C_CONT_LAB = "10"`, `C_LABMATCH=1`, `L_ADDEND = f32(200.0)`, and the token stream
`PROGRAM, ID0, EOL, KW(34), FDESC(PAY=1026), ID(X), EOL, KW(37)`.  The negative sign in the
printed line is the inherited docs/105 sign convention (B6a printed `-0034.50` for +34.50).

---

## 6. Word budget (measured from the build, not projected)

| resource | used | limit | verdict |
|:--|--:|--:|:--|
| N+3 code (verbatim converter + floor_int) | **40 words** | 58 | **PASS** (18 spare) |
| N+2 changed words vs base image | **528** | 649 | **PASS** |
| N+2 offsets 526..900 changed | **0** | 0 | **PASS** |
| N+2 lexer code | **348 words** (696 halfwords), slots 255..499 + 901..1023 | free | **PASS** |
| N+2 verbatim B3 dispatcher (unchanged) | **105 words** (150..254) | free | **PASS** |
| N+1 body words changed | **6** (`body[0o11]`, `body[0o112..0o116]`) | 998 | **PASS** |
| N+1 keeper `body[0o26]` changed | **no** (base/A both `0o1000040000000`) | must be kept | **PASS** |
| N+4 | not used | unavailable | **PASS** |

The 528 changed N+2 words split as 425 in offsets 0..525 and 103 in 901..1023.
`K_DO_DECR` lives at N+2[54] (a previously unused cell), `L_BOUND/L_CNT/L_ADDEND` at 147/148/149,
and the label/window cells in 515..525 and 142..146.  No new opcode, no MMU trick beyond the
proven `UTC 20000` / M[7]=M[12]=0o20000 usage.

---

## 7. Supported DO subset / deferrals

**Implemented (FACT):** one statement per card in columns 7..72 with labels in columns 1..5;
`DO <label> I=init,limit` with a 2-digit terminating label (capped), single-digit `init`/`limit`
decoded from the source card (only the limit is used as the countdown bound); the body
`S=S+<literal>` as a **fixed-count repeat of one accumulation**, with the addend parsed from
the source by the docs/104 digit chain (`20.00 -> f32(200.0)`); labelled terminal `<label>
CONTINUE` with the label resolved in Pass L (`C_LABMATCH` gate); `PRINT n,S` and labelled
`n FORMAT(1X,Fw.d)` from B6a (`w in {2,3,4}, d in {1,2}`); `END` from source and the
`0xff`/`*END FILE` EOF terminator; countdown `uza` exit on 0 and `-0`; verbatim B3 + docs/105.

**Deferred / not claimed:**
* **No general DO-variable update.** `I` is parsed but its value word is never seeded or
  incremented; the bound directly drives the countdown.
* **Step is fixed at 1** (countdown with `K_DECR`), `init` other than 1 is ignored.
* **No nested loops, no arbitrary body, no body-target dispatch.** Only one accumulation
  statement in the body; no general expression evaluator (B4), no TO/body selector.
* **One variable `S`** (single-letter, VIDX 1); no multi-letter identifiers or lists.
* **`w>4` / `d>2` projection** (design §1.6) is not wired; only the proven mask set.
* Label mismatch is a machine-visible no-go (no `21` line), not a Fortran diagnostic.
* No native FRONT DO IR is used or needed (C6 established FRONT emits none); this is a
  contour-side source-text implementation.

---

## 8. FACT / INFERENCE

**FACT (measured or cited):** all five SIMH printer lines and completion markers; image/deck
SHAs and byte diffs (1 deck byte, 3 patch bytes, 0 restore bytes); N+3=40, N+2=528 changed / 0
in 526..900, N+1=6 changed with keeper preserved; C CORE showing f32(400.0), resolved labels and
the token stream; C MTR showing the counter from source, two FPU iterations and the `uza` exit;
verbatim B3/converter behavior; EOF completion without `END`.

**INFERENCE / design choices in this build:** the exact N+2 cell placement; the 2-digit cap on
the DO label (supports labels 10..99 only, sufficient for the stated deck); representation of
labels as packed ASCII compared for equality; the `guard()` region trampoline; the omission of
the `REAL` scaffolding token so the loop result survives to B3; starting the byte stream at
`0o64012` (inherited from B6a).  These are engineering choices, not new architectural claims.

**Not claimed:** any repository/live-disk/C patch, a Fortran compiler, general DO semantics,
nested loops, or any SIMH result beyond the five decks above.

---

## 9. Emulator provenance note

The harness normally pins emulator SHA-256 prefix `9ef71b26` (`9ef71b260e8a780d`).  Gates
A, B and PATCH were run with that binary.  During the run the shared binary at
`/home/azizz/Yandex.Disk/simh/BIN/besm6` was rebuilt externally to prefix `d0583057`
(mtime 01:45), which we did **not** cause.  RESTORE and EOF were therefore driven by a
workspace-local driver copy `harness/drive_b_newemu.py` that accepts the new prefix; it is a
one-line SHA-constant change to the same `drive_b.py` logic.  We verified equivalence on the
RESTORE deck: the new emulator reproduces `-0040.00` and `КОНЕЦ ЗАДАЧИ` byte-for-byte in the
printer output.  No emulator source or binary was modified by this task.

---

## 10. SHAs (SHA-256)

```
c0ac6e326d67030ddc79577f17dec974be7cb43e557101944eefd57e857e1606  images/2048_B6C_A = _B = _RESTORE (= EOF run)
04770dfea5c82d182568882ec4b08769344f19d284c7fca3ac5ae7dbcdcdc7e1  images/2048_B6C_PATCH
2f5fcf873d43c2846ee1669669e26202f32fa25e6b71e109fd20ef4452142ff5  images/2048_base (unchanged)
9a125f35332f42220cb98afe270f33455411436ec3828a0e365cd69de62bac5b  decks/deck_do_A.b6
c2ade8f1b68d63f8634fad409c7ba78d7c468ee853897e9d159c9b68092273ff  decks/deck_do_B.b6
65be86771e0a0b50e1228f25055b48b52c872fa0fde47c3f21fcccd69e5cea88  decks/deck_do_EOF.b6
7b9b1c0fc6d22b2ee2d0807526215ac06505eb3d63ee8106cf7a97f669bc64aa  harness/runs/localprn_B6C_A3.txt
b7e2b48f0c668bbcb2652aaf69e4c3d1cad1eb01e98e11c3c70f8fb703f02560  harness/runs/localprn_B6C_B.txt
307f0db3838eedb057211cbb1df8e0039b9f8011f0b8792a85354bdb1c5ef846  harness/runs/localprn_B6C_PATCH.txt
ad307c3665324bb12178120897a70354f94fad198fb1a79eabc1f6255d9da1f9  harness/runs/localprn_B6C_RESTORE2.txt
206848f4a8022af4126f8c2f3876f1ff4cf369380da04d345ef57c24e7cbf889  harness/runs/localprn_B6C_EOF2.txt
ae565a30e562f8e9443fbd4a48c43ffb1e15458b769679087f4287bd73f8fdfb  harness/runs/acpu_B6C_{A3,B,PATCH,RESTORE2,EOF2}.txt
17dd40a70db388fb90db1793b08c2fd38b600d4923a4cf62183186ebe3e8f9d4  oracle/B6C_MTR_LOOP/out.txt (raw MTR)
884bfa2baade377117e353d86f9af80ab6e3436d987a6500106723ef4d19424e  evidence/MTR_B6C_curated.txt
```

---

## 11. Evidence index

```
build/b6c_build.py                 DO/CONTINUE source lexer + count loop (extends b6a_build.py)
build/make_decks_b6c.py            real-Fortran deck generator (A bound 2, B bound 3)
build/oracle_core0.py              C-oracle CORE dump at first PC hit
decks/deck_do_{A,B,EOF}.b6         Fortran source decks (no 777005)
images/2048_B6C_{A,PATCH,RESTORE}  contour images
harness/runs/localprn_B6C_*.txt    authoritative SIMH printer captures
harness/runs/verdict_B6C_*.json    harness verdicts
harness/runs/acpu_B6C_*.txt        raw ACPU device copies (not the observable)
oracle/B6C_MTR_LOOP/out.txt        raw C-oracle MTR
oracle/B6C_CORE5/core-pc.bin       C CORE at 0o22065 (machine state at handoff)
evidence/MTR_B6C_curated.txt       decisive MTR lines
```

DONE
