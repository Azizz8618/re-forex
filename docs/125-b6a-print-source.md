# B6a IMPLEMENTATION: real Fortran source `PRINT`/labeled `FORMAT` drives the proven B3 print path

> РЕЗУЛЬТАТ B6a: **PASS**. Двухпроходный machine‑код читает Fortran‑карты:
> pre‑scan находит `100 FORMAT(1X,F4.2)`, проход выдачи распознаёт `PRINT 100,X`,
> разрешает метку и отдаёт токены B3‑диспетчеру и неизменному GOST.
> SIMH: `F4.2 → 21 -0034.50`, `F2.2 → 21 -  34.50` при том же образе,
> PATCH machine‑слова → `-  34.50`, restore → `-0034.50`. Все `КОНЕЦ ЗАДАЧИ`.
> Бюджет 40/58 N+3, 409/649 N+2, 6 слов N+1 с keeper, 526..900 не тронуты.
> В деке — настоящий Fortran, без IR и фикстур.

**VERDICT: PASS.** A BESM-6 machine-code, two-pass source-text path reads the actual
Fortran card image, pre-scans `n FORMAT(1X,Fw.d)`, resolves the label written in
`PRINT n,X`, emits the B2 one-word token stream, and feeds the **verbatim** B3
dispatcher at `0o22065` + verbatim docs/105 GOST converter in N+3.  The decisive
SIMH A/B/PATCH/RESTORE gates all print the required `21` line and reach
`КОНЕЦ ЗАДАЧИ`.  Every value printed is machine-derived from the source digits;
no `777005` IR card, no expression/print fixture, no host-computed result digit.

Discipline: workspace `/tmp/.private/azizz/opencode/b6a-print/` only; copies of
every image/deck/emulator; no repository edit, no live disk, no tmux session 0,
no C `dispak` patch.  C `dispak` was **oracle only** (MTR / CORE).  Authoritative
verdicts are full SIMH printer/ACPU captures from `drive_b.py`
(emulator SHA-256 prefix `9ef71b26`, verified on every run).

---

## 1. VERDICT

| gate | image SHA-256 (first 16) | deck | decisive printer line | КОНЕЦ ЗАДАЧИ | verdict |
|:--|:--|:--|:--|:--|:--|
| A | `c09fcca634415add` | A `F4.2` | ` 21 -0034.50  3000.00` | yes | **PASS** |
| B | `c09fcca634415add` (byte-identical to A) | B `F2.2` | ` 21 -  34.50  3000.00` | yes | **PASS** |
| PATCH | `0e3edf2a80ca6b37` | A | ` 21 -  34.50  3000.00` | yes | **PASS** |
| RESTORE | `c09fcca634415add` (= A) | A | ` 21 -0034.50  3000.00` | yes | **PASS** |

Harness `plumbing: PASS` and `product_gate: PASS` for all four captures
(`evidence/verdict_*.json`).  (`completion_marker:false` in those JSONs only
means the console-pane regex did not match; `product_gate` independently
verifies `КОНЕЦ ЗАДАЧИ` in the printer capture, and the line is present in all
four `localprn_*.txt` files.)  A vs B: image byte-identical, **one** deck byte
changes (`4` -> `2` in `F4.2` -> `F2.2`); the printed field spacing changes.
PATCH vs A: deck byte-identical, **one machine word of OUR code** changes
(N+2[52] `L_FPAY_PATCH`, `0` -> one's-complement `-512`), and the value prints
with the w=2 mask.  RESTORE: image byte-identical to A, output returns to A.
This is the required A/B/PATCH/RESTORE causality, not a host substitution.

---

## 2. The deck is real Fortran source (verbatim, `decks/deck_A.b6`)

```
ШИФР 410300 ЗС5^
ДИС 41(2048)^
ОЗУ 32^АЦП 32^
ЕЕВ1А3
*NAME FRX5XX
*TRANS:FRX5*,,412350
      PROGRAM MAIN
      X=34.50
      PRINT 100,X
  100 FORMAT(1X,F4.2)
      END
*EXECUTE
*END FILE
``````
ЕКОНЕЦ
```

(These 15 lines are the exact UTF-8 text of `decks/deck_A.b6`; deck B is the
same text with `F4.2` replaced by `F2.2`.)

The four leading bytes on each of the first/last two lines are the standard
`*NAME` framing control bytes inherited from the proven b-harness deck template;
the Fortran body is physical columns 7..72 with the label `100` in columns 1..5.
`grep 777005` on the deck: **0 hits**.  No `*FOREX`, `*FTN`, `*perso`, or IR card.

Deck B is byte-identical except at 1-based byte 175: octal `64` (`4`) -> `62`
(`2`), i.e. `F4.2` -> `F2.2`.  `deck_C_label_mismatch.b6` changes `PRINT 100,X`
to `PRINT 200,X` and is used only as a label-resolution probe (§6).

SHA-256:

```
945d7ba6b1afd4d39daea27984ae90d827c1e80efff7c063c0e4f758eaddfcf1  decks/deck_A.b6
b726c7fb156d68e6a80c447c9a1ed11e89ba64fb3f8060e3d8b3bc46bf1f70c3  decks/deck_B.b6
b3683340f44e686ab5c59131a58ae7c96f8646c860f680ea44fbdde7867efbd7  decks/deck_C_label_mismatch.b6
```

---

## 3. What the machine code does

`build/b6a_build.py` (new) reuses **verbatim**: `build_e2e.py` zone reader/writer
and encoders, `c6_build.py` N+3 converter + low-RAM cell layout, `c7_build.py`
width tables, `final_sign.py` LO cells, and `dispatch_build.py` B3 dispatcher +
`tok()` encoder.  No B3 word was changed.

1. **Pass L (label/FORMAT pre-scan).**  A byte stream over the RLE card buffer
   (`M[10]=0o60000`, `M[11]` byte index, `C_CURW`) starts at `0o64012` and walks
   to the `0xff` end marker.  Leading label digits of each card are packed into
   `C_LABPACK`; the keyword is detected by exact 3/5/6-byte sliding-window
   compares against `END`/`PRINT`/`FORMAT` ASCII constants (masked to 3/5 bytes,
   so the window really slides).  On `FORMAT(` the packed label is stored into
   `C_LAB`; the `F`, `w` digit, `.`, `d` digit after `1X,` are decoded with the
   proven `PD0`/`M8` byte trick, `PAY = w<<8|d` is stored in `C_PAY`, and
   `C_FOUND=1`.  `1X` is recognized and discarded (design §1.6).
2. **Pass E (emit + execute).**  The buffer is rewound; the lexer emits the
   B2 one-word stream: `PROGRAM`, name, `REAL`, `X`, `EOL` scaffolding; then
   from source `X=34.50` it installs the 6-bit name word at N+2[1] and builds
   the literal float by the docs/104 chain into pool word N+2[100] =
   `f32(345.0)` = 10 x 34.50; then from source `PRINT 100,X` it emits
   `KW(34)`, an FDESC whose PAY is fetched from `C_PAY` **only after comparing
   the PRINT label `C_PLABPACK` with the FORMAT label `C_LAB`**, `ID(X)`, `EOL`;
   `100 FORMAT(...)` is a no-op; `END` emits `KW(37)`.
3. **Handoff** `LONG UJ 0o22065` to the verbatim B3 dispatcher.  B3 reads EST
   from N+2[33], seeds GOST words `0o2006/0o2007`, applies the docs/113 w/d
   masks (w=4: none; w=2: `0o7417`-equivalent leading-zero blanking), and calls
   the verbatim converter via VJM.  No digit is produced by the host.

The one-word PATCH cell `L_FPAY_PATCH` (N+2[52]) is added to the resolved PAY
before the FDESC token is composed; default `0`, patched to one's-complement
`-512` (octal `7777777777776777`), which turns the A-deck `F4.2` (PAY 1026) into
`F2.2` (PAY 514).

---

## 4. Authoritative SIMH evidence

Printer `prn0` line 100 and completion line (raw files in `evidence/`):

```
A       : " 21 -0034.50  3000.00"   ...  " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
B       : " 21 -  34.50  3000.00"   ...  " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
PATCH   : " 21 -  34.50  3000.00"   ...  " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
RESTORE : " 21 -0034.50  3000.00"   ...  " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
```

Full captures: `evidence/{localprn,console,acpu,verdict}_*.txt|json`.  A/B were
driven by `/tmp/.private/azizz/opencode/b-harness/drive_b.py`; PATCH/RESTORE by
a byte-for-byte copy of that same driver in `harness/drive_b.py` (an isolated
image cache was needed because the shared harness cache had drifted after A/B;
the driver logic, ini builder, emulator SHA and tmux discipline are unchanged).

Whole-image byte diffs (`cmp -l`):

* deck A vs B: **1 byte**, offset 175, `64` -> `62` octal (the FORMAT digit).
* image A vs PATCH: **8 bytes** = one 6-byte machine word at file offset
  `10419553..10419558` (N+2[52]) plus the two recomputed zone-N+2 checksum
  copies at `10419098` and `10419130` (`0o106` -> `0o105`).
* image A vs RESTORE: **0 bytes** (same SHA-256).
* image A vs B: **0 bytes** (same SHA-256).

---

## 5. Machine state at the B3 handoff (C oracle CORE, advisory)

C `dispak` CORE dumped at PC `0o22065` (B3 dispatcher entry), decoded with
`dump_core_n2.py`:

```
                     deck A (F4.2)          deck B (F2.2)          PATCH (deck A)
N+2[1]  name word   7000000000000000       7000000000000000       7000000000000000   ('X')
N+2[33] value       4452620000000000       4452620000000000       4452620000000000   (f32 345.0 = 10x34.50)
N+2[100] literal    4452620000000000       4452620000000000       4452620000000000
N+2[73] KW PRINT    1242000000000000       1242000000000000       1242000000000000
N+2[74] FDESC       1501000000002002       1501000000001002       1501000000001002
                    (PAY=1026, F4.2)       (PAY=514, F2.2)         (PAY=514, via one-word patch)
N+2[75] ID X        0200000000000001       0200000000000001       0200000000000001
N+2[76] EOL         1300000000000000       1300000000000000       1300000000000000
N+2[77] END         1245000000000000       1245000000000000       1245000000000000
```

Label table at the same instant (deck A): `C_LAB` (N+2[63]) =
`00 00 00 31 30 30` = ASCII `100`; PRINT's collected label
`C_PLABPACK` (N+2[507]) = `00 00 00 31 30 30` = `100`; `C_PAY` (N+2[500]) =
`00 00 00 00 04 02` = `0x402` = `4<<8|2`.  **The FDESC token is therefore
resolved from the FORMAT label, not from inline PRINT digits.**

Label-mismatch probe (advisory, `decks/deck_C_label_mismatch.b6`, `PRINT 200,X`
against `100 FORMAT`): the core at B3 entry shows `KW(34)` at N+2[73] followed
immediately by `END` at N+2[74] and zeros after it, i.e. no FDESC/ID and no
`21` line would be produced.  This demonstrates the comparison is real.

---

## 6. Raw ACPU and MTR

Raw ACPU captures are in `evidence/acpu_*.txt` (e.g. the job-accounting header
`СБО,ВВЕДИ ПО ИНС ...`, `ДАТА РЕШ. ВЕРСИЯ 117А ...`, `*АЦПУ-0 ЭВМ-3`).

Raw C-oracle MTR: `evidence/mtr_final_a_raw.txt` (10 191 lines, window
`BESM6_MTR_LO=022340,HI=023000,N=3000`).  Curated decisive lines in
`evidence/mtr_final_a_curated.txt` (AU is the 48-bit accumulator in octal):

```
MTR 22401R aex    1704(14) AU=2144752223240524   ; C_WIN6 == "FORMAT" -> label pre-scan hit
MTR 22450L atx    2623(14) AU=0000000002002      ; C_PAY = w<<8|d = 4<<8|2 (F4.2)
MTR 22457R atx    1736(14) AU=0000014230060      ; C_LAB = "100" (ASCII 31 30 30)
MTR 22533L aex    1703(14) AU=5012222247124      ; C_WIN5 == "PRINT" -> source PRINT hit
MTR 27752L uj     22065(0) AU=0000000000016      ; handoff to verbatim B3 dispatcher
```

`1704`/`1703` are the FORMAT/PRINT comparison cells, `2623` is `C_PAY`,
`1736` is `C_LAB`.  The value `5012222247124` octal is exactly the five ASCII
bytes `P R I N T`; `2144752223240524` is `F O R M A T`.

---

## 7. Word budget (measured from the build, not projected)

| resource | used | limit | verdict |
|:--|--:|--:|:--|
| N+3 hot path (verbatim converter + floor_int) | **40 words** | 58 | PASS (18 spare) |
| N+2 dispatcher (verbatim B3, offsets 150..254) | **105 words** | 649 | PASS |
| N+2 source lexer code (offsets 300..525 + 901..926) | **226 words** (452 halfwords) | 649 | PASS |
| N+2 changed words vs base image (all regions) | **409 words** | 649 free | PASS |
| N+2 forbidden band offsets 526..900 changed | **0** | 0 | PASS |
| N+1 body words changed | **6** (`body[0o11]`, `body[0o112..0o116]` converter cells) | 998 | PASS |
| N+1 keeper `body[0o26]` changed | **no** | must be kept | PASS |

The 409 changed N+2 words break down as: offsets 0..63 = 51, 96..149 = 25
(B3 work/constants), 150..254 = 105 (B3 code), 300..525 = 202, 901..926 = 26.
Tokens (64..77) and the literal pool (100..103) are written at runtime by OUR
code, not seeded in the image.  All code/data live below offset 526 or in the
proven 901..1023 tail band; no N+4, no new opcode, no MMU trick beyond the
proven `UTC 20000`/M[7]=0o20000 usage.

---

## 8. Supported subset and deferrals

**Implemented (FACT):** one statement per card in columns 7..72; `X=<real>`
assignment with arbitrarily many digits and one decimal point (digits decoded
by the docs/104 chain); `PRINT n,V` with single-letter variable `X` (VIDX 1);
labeled `n FORMAT(1X,Fw.d)` with `w in {2,3,4}`, `d in {1,2}`; label resolution
by packed-digit equality; `FORMAT` as an execution no-op; `END` from source;
EOF (`0xff`) scan termination; the verbatim B3 dispatch, docs/113 width masks
and docs/105 converter.  No `PROGRAM`/`REAL` parsing: those two statements are
emitted as constants (as in proven B1/B5), and `PROGRAM MAIN` in the deck is
only skipped by the scanner.

**Deferred / not claimed (FACT about this build):**
* `w > 4` or `d > 2` projection (design §1.6 `F8.2 -> F4.2`) is not wired: the w/d
  digits are used directly, only the proven mask set is supported.
* Multi-letter identifiers, multi-variable PRINT lists, other editors
  (E/I/G), rounding, continuation cards, arbitrary decks, DO/CONTINUE,
  intrinsics by name (B6b/B6c scope).
* Print label mismatch is a machine-visible no-go (no `21` line), not a Fortran
  diagnostic message.
* The `1X` editor is consumed and discarded by design (docs/123 §1.6).

---

## 9. FACT / INFERENCE

**FACT (measured or cited):** all four SIMH printer lines, completion markers,
image/deck SHAs and byte diffs; N+3=40, N+2 dispatcher=105, lexer=226, changed
N+2=409, 0 writes to 526..900, keeper preserved; C CORE at `0o22065` showing
the resolved FDESC PAY 1026 (A) / 514 (B, PATCH) and labels `100`/`100`;
C MTR showing the `FORMAT`/`PRINT` window matches, `C_PAY` and `C_LAB` stores
and the `uj 22065` handoff; card-buffer RLE layout at `0o64000+`; verbatim B3
dispatcher/converter behavior; label-mismatch no-go in C CORE.

**INFERENCE / design choices in this build:** the exact N+2 cell placement and
the two VJM subroutines (GETCH/EMIT) with link register 5; representation of
labels as packed ASCII bytes compared for equality rather than numeric
integers; the single label-table entry (one FORMAT in the supported deck); the
`L_FPAY_PATCH` addition as the one-word PATCH mechanism; starting the byte
stream at `0o64012`, which assumes the proven `PROGRAM MAIN` first-card layout.
These are engineering choices, not new architectural claims.

**Not claimed:** any repository/live-disk/C patch, a Fortran compiler, full
`Fw.d` semantics, or any SIMH result for decks other than A/B/PATCH/RESTORE
(the mismatch probe is C oracle advisory only).

---

## 10. SHAs (SHA-256)

```
c09fcca634415addbc6141ce3785cba2a020903936063b86ae6ce4828e308852  images/2048_A
c09fcca634415addbc6141ce3785cba2a020903936063b86ae6ce4828e308852  images/2048_B  (identical)
0e3edf2a80ca6b37410653c805575100edd25d5ee2b1936ab9ad484f232ad7e5  images/2048_PATCH
c09fcca634415addbc6141ce3785cba2a020903936063b86ae6ce4828e308852  images/2048_RESTORE  (identical to A)
2f5fcf873d43c2846ee1669669e26202f32fa25e6b71e109fd20ef4452142ff5  images/2048_base (FRX5 base, unchanged)
945d7ba6b1afd4d39daea27984ae90d827c1e80efff7c063c0e4f758eaddfcf1  decks/deck_A.b6
b726c7fb156d68e6a80c447c9a1ed11e89ba64fb3f8060e3d8b3bc46bf1f70c3  decks/deck_B.b6
```

## 11. Evidence index

```
build/b6a_build.py               new: two-pass source PRINT/FORMAT lexer + build
build/make_decks.py              real-Fortran deck generator (A/B/C)
build/dispatch_build.py          verbatim B3 dispatcher (reused unchanged)
build/c6_build.py, c7_build.py, final_sign.py, build_e2e.py   verbatim helpers
images/2048_{A,B,PATCH,RESTORE}  contour images (A=B=RESTORE byte-identical)
decks/deck_{A,B,C_label_mismatch}.b6
oracle/CORE_DISP4/core-pc.bin    C CORE at 0o22065, deck A
oracle/CORE_B/core-pc.bin        C CORE at 0o22065, deck B
oracle/CORE_PATCH/core-pc.bin    C CORE at 0o22065, PATCH
oracle/CORE_MISMATCH/core-pc.bin C CORE for PRINT 200 / FORMAT 100 (no-go)
evidence/mtr_final_a_raw.txt     raw C MTR (10 191 lines)
evidence/mtr_final_a_curated.txt decisive MTR lines (§6)
evidence/{localprn,console,acpu,verdict}_*.txt|json   authoritative SIMH captures
harness/{drive_b.py,setup_b.py}  isolated copy of the b-harness for PATCH/RESTORE
```

DONE
