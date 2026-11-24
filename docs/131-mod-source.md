# B6c: `MOD(X,Y)` from REAL Fortran source under full SIMH

> РЕЗУЛЬТАТ: **PASS**. `MOD(X,Y)` по имени из Fortran‑текста: `MOD(7,3)→1.00`,
> `MOD(8,3)→2.00`, `MOD(7,4)→3.00` (второй аргумент live); patch → `2.00`,
> restore → `1.00`; ABS/SQRT без регрессии. Образ `2af489b4…`, N+3 55/58,
> N+2 522/649, 526..900 = 0, keeper сохранён. Исправления к docs/129:
> разбор двух аргументов, opcode `0o05` вместо reverse‑subtract `0o06`,
> перенос ITAB/intrinsics в свободные слоты 255..287.

**VERDICT: PASS.** The autonomous contour recognises the name `MOD` in real
fixed-form Fortran source text, parses TWO comma-separated REAL arguments,
executes the proven bitwise-AINT MOD machine routine on the BESM-6 FPU, and
prints the result through the verbatim GOST path.

Full SIMH (authoritative, isolated b-harness, emulator SHA
`d058305796bcd0aaf108056f595ee2a222762abe31cf3bb59f1697c9473ca675` verified
on every run):

| gate | image | deck | prn0 `21` line | КОНЕЦ ЗАДАЧИ | verdict |
|:--|:--|:--|:--|:--|:--|
| A | `2048_MOD_A` | `Y=MOD(7.0,3.0)` | ` 21 -0001.00  3000.00` | yes | **PASS** |
| B | `2048_MOD_A` (byte-identical) | `Y=MOD(8.0,3.0)` | ` 21 -0002.00  3000.00` | yes | **PASS** |
| C (second arg live) | `2048_MOD_A` (byte-identical) | `Y=MOD(7.0,4.0)` | ` 21 -0003.00  3000.00` | yes | **PASS** |
| PATCH | `2048_MOD_PATCH` | A | ` 21 -0002.00  3000.00` | yes | **PASS** |
| RESTORE | `2048_MOD_RESTORE` (= A, same SHA) | A | ` 21 -0001.00  3000.00` | yes | **PASS** |
| ABS (no regression) | `2048_MOD_A` | `Y=ABS(-16.0)` | ` 21 -0016.00  3000.00` | yes | **PASS** |
| SQRT (no regression) | `2048_MOD_A` | `Y=SQRT(16.00)` | ` 21 -0004.00  3000.00` | yes | **PASS** |

C `dispak` was used **only** as an advisory MTR/CORE oracle; no host-computed
result digit appears anywhere in any image or deck.

Discipline: workspace `/tmp/.private/azizz/opencode/b6c-mod/` (symlink to
`/dev/shm/b6c-mod/` because tmpfs `/tmp` was 100% full), copies only. No
repository edit, no live disk, no tmux session 0, no C `dispak` patch, no edit
to the `b-final`, `b6b-abs-fix` or `b6b-intr` workspaces.

---

## 1. THE DECK (verbatim, `decks/deck_MOD_A.b6`)

```
ШИФР 410300 ЗС5^
ДИС 41(2048)^
ОЗУ 32^АЦП 32^
ЕЕВ1А3
*NAME FRX5XX
*TRANS:FRX5*,,412350
      PROGRAM MAIN
      Y=MOD(7.0,3.0)
      PRINT 100,Y
  100 FORMAT(1X,F4.2)
      END
*EXECUTE
*END FILE
``````
ЕКОНЕЦ
```

Deck B is byte-identical except offset 138 (1-based): `7` -> `8`
(`      Y=MOD(8.0,3.0)`). Deck C is byte-identical to A except offset 142:
`3` -> `4` (`      Y=MOD(7.0,4.0)`). No `777005` IR card, no `*FOREX`, no
`*FTN`, no fixture.

---

## 2. WHAT WAS IMPLEMENTED

Base image: `2048_ABS_FINAL` (docs/129), reproduced byte-identically from
`build/b6b_absfix_full.py` before modification. Builder:
`build/b6c_mod_full.py` (SHA `40dc26252007913af7f16c155785b003c8c55245a32b3dec334e4b0a630b3e68`).

1. **Source recognition.** The proven 4-byte sliding-window name compare of
   docs/129 (`C_NAMEW` vs `L_TXT_SQRT/ABS/MOD`) is reused verbatim. `MOD`
   matches `TXT_MOD = 0x004d4f44` and sets `C_INTR = 3`; `PE_NAME_LOCK` also
   resets the new argument counter.
2. **Two-argument parse.** After the first literal is converted it is saved in
   `C_MODA` and the argument counter is bumped; scanning resumes at the comma.
   The second literal is saved in `C_MODB`. Only then does the `ITAB` dispatch
   run, with the FIRST argument restored as the routine's ACC input. ABS/SQRT
   take the unchanged single-argument path.
3. **Number-layout fix.** The inherited pad loop counted fractional digits and
   broke one-digit integer parts (`7.0` was parsed 100x). It now uses
   `C_NDIG`, and a one-digit integer part gets a leading ASCII `0` inserted
   (`C_NUM |= 0x300000`), yielding the expected `07.00` layout.
4. **MOD opcode fix.** The ABS base had `FSUB = 0o06` (reverse subtract
   `x-a`); the C4/C7-proven MOD routine uses `0o05` (`a-x`). Corrected; MTR now
   shows `a-x` and `f32(10)` as the remainder of `f32(70)`, `f32(30)`.
5. **Slot-gap guard reuse.** The docs/129 explicit `uj GAP_CROSS` before the
   499/901 hole and the padding to halfword 400 are retained. The two-word
   ABS post-resolve branch/lock fix is retained as belt-and-braces.
6. **ITAB relocation.** The two-argument parser grew the LEX past slot 986,
   where docs/129 placed ITAB; that would overwrite the LEX tail (observed as
   a spurious ABS dispatch and `ДЕЛЕНИЕ НА НУЛЬ`). ITAB and the three intrinsic
   routines now live in the otherwise unused N+2 low-band window 255..299;
   the whole proven tail band 901..1023 is LEX code. No forbidden-band write.

**Reused verbatim:** `parser_build` B3 dispatcher/print path (105 words),
`c6_build` N+3 GOST converter (55 changed words), `c7_build` width tables,
`final_sign` low-RAM cells, `build_e2e` zone I/O/checksums,
`dispatch_build.tok()`, the docs/129 gap guard, name compare, number-to-float
chain, ITAB trampoline technique and ABS/SQRT routines, and the b-harness.

---

## 3. RAW EVIDENCE

### 3.1 Authoritative full-SIMH printer captures

From `harness/runs/localprn_<case>.txt` (all seven runs, exactly one
completion marker each; full raw lines also in `evidence/raw_prn0_lines.txt`):

```
--- MOD_SIM_A ---
PRN21:  21 -0001.00  3000.00
DONE :  КОНЕЦ ЗАДАЧИ        +000000000000⏨+00    0000206320000000
--- MOD_SIM_B ---
PRN21:  21 -0002.00  3000.00
DONE :  КОНЕЦ ЗАДАЧИ        +000000000000⏨+00    0000206320000000
--- MOD_SIM_C ---
PRN21:  21 -0003.00  3000.00
DONE :  КОНЕЦ ЗАДАЧИ        +000000000000⏨+00    0000206320000000
--- MOD_SIM_PATCH ---
PRN21:  21 -0002.00  3000.00
--- MOD_SIM_RESTORE ---
PRN21:  21 -0001.00  3000.00
--- MOD_SIM_ABS ---
PRN21:  21 -0016.00  3000.00
--- MOD_SIM_SQRT2 ---
PRN21:  21 -0004.00  3000.00
```

Harness verdict for every gate: `plumbing: PASS`, `emulator_sha:
d058305796bcd0aa`. The shared `SIMH/ACPU/output.txt` copies are empty/0 bytes
(per the harness `PROBE.md`, those device files are shared and stale); the
private `-n prn0` capture is the authoritative observable. One SQRT run
(`MOD_SIM_SQRT`) had a harness flake with no job-start line; the identical
re-run `MOD_SIM_SQRT2` produced the printed line and completion above.

### 3.2 C `dispak` MTR (advisory, `evidence/mtr_mod_dispatch.txt`)

Source name match, `C_INTR`, first/second argument split and ITAB dispatch
(ACC values octal):

```
MTR 27755L xta    1707(14) AU=0000000000000
MTR 27755R atx    2643(14) AU=0000000000003   ; TXT_MOD match -> C_INTR = 3
MTR 30001R uza    30005(0) AU=0000000000000   ; C_MODARG = 0 -> first argument
MTR 30005R atx    2056(14) AU=4350600000000000 ; C_MODA = f32(70)
MTR 30006R atx    2000(0) AU=0000000000001   ; C_MODARG = 1
...
MTR 30002R atx    2057(14) AU=4257000000000000 ; C_MODB = f32(30)
MTR 22240L uj     22264(0) AU=4350600000000000 ; ITAB2 -> I_MOD, ACC = first arg
```

### 3.3 C `dispak` MTR, MOD routine (`evidence/mtr_mod_routine.txt`)

```
MTR 22264L atx    2056(14) AU=4350600000000000 ; A = 70
MTR 22266R a/x    2057(14) AU=4350600000000000 ; Q = 70/30
MTR 22267L atx    2060(14) AU=4111252525252525 ; Q = 2.3333
MTR 22273L atx    1732(14) AU=4110000000000000 ; AINT(Q) = 2
MTR 22274R atx    2637(14) AU=4317000000000000 ; B*AINT = 60
MTR 22275R a-x    2637(14) AU=4350600000000000 ; 70 - 60 (opcode 0o05)
MTR 22276L uj     30015(0) AU=4212000000000000 ; remainder f32(10) -> print path
```

C-oracle printer: ` 21 -0001.00  3000.00`, `КОНЕЦ ЗАДАЧИ`.

### 3.4 Causality

* **A/B/C:** image SHA identical (`2af489b4...`); one deck byte changes the
  dividend 7->8 (value 1.00->2.00) or the divisor 3->4 (value 1.00->3.00).
  Both source arguments are therefore live.
* **PATCH:** deck A frozen; one N+2 machine word at offset 98
  (`RAM 0o22001`, `L_PATCHDELTA`) is changed from `f32(0)` to `f32(10)`, so the
  on-machine dividend becomes 80 and `80 mod 30 = 20` -> `2.00`.
  `cmp -l` shows exactly 6 differing bytes: the one word plus the two zone
  checksum copies.
* **RESTORE:** image byte-identical to A (same SHA, `cmp` = 0), value returns
  to `1.00`.

---

## 4. WORD BUDGET (measured vs `2048_base`, `build/budget.py`)

| resource | used | limit | verdict |
|:--|--:|--:|:--|
| N+3 converter + cells | **55** changed words | 58 | PASS |
| N+2 changed words | **522** | 649 | PASS |
| N+2 forbidden band 526..900 | **0** writes | 0 | PASS |
| N+1 body changed words | **6** (offsets 9, 74..78) | 998 | PASS |
| keeper `body[0o26]` | `0o1000040000000` unchanged | preserved | PASS |

Builder line: `N3=40/58w LEX=600hw (300w) B3disp=105w N2used=1001/649`.
LEX 600 halfwords = 300 words, all in slots 300..499 and 901..1000;
ITAB 255..257, intrinsics 258..287 (30 words); no overlap, no forbidden-band
write. N+3 changed-word count is 55 (converter 40 clean words plus 15 cells),
consistent with docs/129.

---

## 5. SHAs (SHA-256)

```
2af489b41dd4c90891d010c3f1f5e44b30b30cea3118ca1d754f36db7393fdc0  2048_MOD_A (A = B = C = RESTORE = ABS = SQRT)
0d8e0b7dfdecd3636db8a2e4f1c3fee7a1724e00d65d9860a202ea0532a5453c  2048_MOD_PATCH (one-machine-word patch)
2af489b41dd4c90891d010c3f1f5e44b30b30cea3118ca1d754f36db7393fdc0  2048_MOD_RESTORE
631c90a10caa98648adda5e7848ee2216c0570a1e9f4ca9d11c081daed9a8bd2  deck_MOD_A.b6
8398d688ed1460417e78201bd9c1718806a88dc4e2be4fc51064c659ba171176  deck_MOD_B.b6
29bc9a2f66d4dd8e89e426d4395a61a2e5f3d7b8c3242eedd96224bdfc2354bd  deck_MOD_C.b6
40dc26252007913af7f16c155785b003c8c55245a32b3dec334e4b0a630b3e68  build/b6c_mod_full.py
d86df73f60ee6c5bf4bd516b7125ecf80df8affeb4fe03a94e340f16976073a1  build/make_decks.py
1bc70acda6ddf66aef847e5d1f400b982ccdfab29228f1339a6acbb8c2adaaba  harness/drive_b.py
d058305796bcd0aaf108056f595ee2a222762abe31cf3bb59f1697c9473ca675  SIMH besm6 (verified)
```

---

## 6. EXACT SUPPORTED SUBSET

* One statement per card, columns 7..72; `PROGRAM MAIN` skipped.
* `V=<real literal>`; `V=SQRT(<real>)`, `V=ABS(<real>)` by name (inherited).
* `V=MOD(<real>, <real>)` by name, two comma-separated REAL literals, each
  with 1 or 2 integer digits and 1 or 2 fractional digits; results via the
  verbatim assignment/PRINT path. MOD arguments are positive literals in this
  gate; negative MOD arguments are not exercised.
* `PRINT n,V` with referenced labelled `n FORMAT(1X,Fw.d)`; `w` 2/3/4, `d` 1/2
  projected, `1X` discarded (inherited from B6a/docs/123).
* `END` from source; no IR cards, no FRONT, no fixture digit.

---

## 7. DEFERRED / OUT OF SCOPE

1. General expression operands inside `MOD` (variables, nested intrinsics,
   arithmetic expressions). Only literal arguments are parsed in this subset.
2. Negative or zero MOD divisor/dividend from source, and Fortran `AINT`/`AMOD`
   semantics for non-integer results beyond the proven bitwise AINT path.
3. DSQRT / double precision (single 48-bit FPU; docs/95 §6).
4. General DO/CONTINUE statement loop, multi-variable PRINT lists, E/I/G
   editors, continuation cards, unary minus on MOD arguments.
5. Full `Fw.d` widths; only `w in {2,3,4}, d in {1,2}` are proven
   (docs/113/123 projection).
6. ITAB relocation consumes low-band N+2 offsets 255..287, previously unused;
   this is inside the 649-word budget but must be kept disjoint from any future
   low-band expansion.

---

## 8. REPRODUCE

```
cd /tmp/.private/azizz/opencode/b6c-mod
python3 build/b6c_mod_full.py --build MOD_A
python3 build/b6c_mod_full.py --build MOD_PATCH --patch-off 98 --patch-delta 150220776144896
cp images/2048_MOD_A images/2048_MOD_RESTORE
python3 build/make_decks.py
python3 build/budget.py 2048_MOD_A
python3 harness/drive_b.py --case MOD_SIM_A --deck decks/deck_MOD_A.b6 --image images/2048_MOD_A
# ... repeat for B / C / PATCH / RESTORE, one case at a time
```

---

## 9. PASS / FAIL SUMMARY

| # | criterion | verdict |
|:--|:--|:--|
| 1 | `MOD` name recognised in real Fortran source | PASS |
| 2 | Two comma-separated arguments parsed from source | PASS (A/B/C) |
| 3 | Machine MOD routine computes the value on BESM FPU | PASS (MTR) |
| 4 | Result printed via proven GOST path, no host digit | PASS |
| 5 | Byte-identical image, deck-only A/B (1.00 vs 2.00) | PASS |
| 6 | One-machine-word PATCH changes value (1.00 -> 2.00) | PASS |
| 7 | Byte-identical RESTORE returns 1.00 | PASS |
| 8 | All full-SIMH runs reach КОНЕЦ ЗАДАЧИ | PASS |
| 9 | ABS / SQRT no regression | PASS |
| 10 | Word budgets and forbidden band / keeper preserved | PASS |
| 11 | General expression arguments, negative MOD operands | deferred |

DONE
