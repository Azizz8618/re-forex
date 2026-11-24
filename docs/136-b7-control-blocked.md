# B7 control-flow contour (GOTO / arithmetic IF): honest FAIL

> СТАТУС: **BLOCKED**. GOTO/IF machine‑кодом собраны (55/58 N+3, 543/649 N+2,
> keeper и 526..900 сохранены), но A/B/PATCH дают одинаковую печать. Hard‑coded
> target в machine‑коде работает — дефект локализован в two‑pass label fix‑up
> (LABTAB/PAY token index). SIMH не загружался из‑за port contention; как
> показано в docs/135, перевод tty на порты 6300+ снимает эту проблему.

**Verdict: FAIL.** A machine-side GOTO/arithmetic-IF contour was implemented on top of
BASE `2048_MODFINAL_B2` and builds byte-reproducibly, but it does **not** yet deliver a
decisive A/B: the label fix-up produces wrong branch targets, and the SIMH harness cannot
boot in this environment. The C `dispak` oracle was used as an advisory debugger only;
no SIMH A/B verdict was obtained. No host substitution, no 777005 IR card, no FRONT, no
system compiler was used. All files are workspace copies; no repository, live disk,
tmux session 0, SIMH binary or C `dispak` source was modified.

## 1. Verified inputs / provenance

```
BASE image  /tmp/.private/azizz/opencode/b-final-do/images/2048_MODFINAL_B2
  SHA-256 5fd132876c9c6297dfeb2400d16771ac2b559328feee7ad1ad93303a8509c7d9  (matches task)
rebuilt base from 2048_base with builder: byte-identical SHA (REPRO)
SIMH /home/azizz/Yandex.Disk/simh/BESM6/BIN/besm6
  SHA-256 d058305796bcd0aaf108056f595ee2a222762abe31cf3bb59f1697c9473ca675  (matches task)
```

Builder and harness are copies in `/tmp/.private/azizz/opencode/b7-control/build/`:
`b7_control_build.py` (new), `b7_parser.py` (copy of `parser_build.py` with two
same-size branch replacements), plus the copied proven builders and `drive_b.py`.

## 2. Word budget (measured by whole-image diff vs `2048_base`)

| resource | used | limit | verdict |
|:--|--:|--:|:--|
| N+3 converter + cells | 55 words | 58 | PASS |
| N+2 changed words | 543 | 649 | PASS |
| N+2 forbidden band 526..900 | 0 writes | 0 | PASS |
| N+1 body words changed | 443 | 998 | PASS |
| body keeper `body[0o26]` | unchanged (`0o1000040000000`) | preserve | PASS |
| B4 parser size | 203 words (unchanged) | - | PASS |
| LEX size | 576 halfwords / 829 body+N+2 slots | fit | PASS |

Build line (final A image):
`case=B7_A sha=71e5f2c2... N3=40/58w B4=203w LEX=576hw slots=829 N2last=1024 bodycode=344w bodyfirst=152 patch=False`

Images:
```
2048_B7_A     SHA-256 71e5f2c2713003ce472787991cfa70fe3a31e48a4f65dbf0700e66721191def1
2048_B7_PATCH SHA-256 582297c20617fffe9c1cb04f73b5a202cbbbdef8bf4e2e8e91a59da0da1c3b14
```
A vs PATCH differs in exactly 6 file bytes (one 6-byte machine word plus the two
recomputed zone checksum copies), i.e. the single body word `BW_THRESH` (f32(0) ->
f32(20.0)), which is the branch-decision threshold. A byte-identical restore image is
just `2048_B7_A` again (no separate copy was needed).

## 3. Deck used (verbatim)

`decks/deck_B7_A.b6` (positive condition):

```
ШИФР 410300 ЗС5^
ДИС 41(2048)^
ОЗУ 32^АЦП 32^
ЕЕВ1А3
*NAME FRX5XX
*TRANS:FRX5*,,412350
      PROGRAM MAIN
      IF (1.0) 2,2,1
    1 X=12.34
      GOTO 3
    2 X=56.78
    3 PRINT 100,X
  100 FORMAT(1X,F4.2)
      END
*EXECUTE
*END FILE
``````
ЕКОНЕЦ
```

Deck B is byte-identical except the condition literal: `IF (-1.0) 2,2,1`
(unary minus, 10 differing bytes). Both decks are real fixed-form Fortran source;
labels are single digits in column 5 (RLE byte `0x84`), FORMAT precedes END.

## 4. What was implemented (machine-side)

* LEX: sliding windows for `IF` (2 bytes) and `GOTO` (4 bytes), with body-resident
  window cells; the 14 N+2 working cells that collided with the longer token stream
  were relocated to body RAM 0o540..0o617 via a `C()` address-space override.
* LEX: two-digit-free **single-digit** label recognition, emitting a `LABEL` token
  (TK9, SUB=label, PAY=token index); `IF` emits TK10/SUB33 with labels packed
  8+8+8 in PAY, followed by the condition expression tokens and EOL; `GOTO` emits
  TK10/SUB32 with the label number.
* Machine **pre-scan/fixup** over the emitted token stream before the B4 hand-off:
  pass 1 builds `LABTAB[label] = token index` from LABEL tokens; pass 2 patches
  GOTO/IF label references.
* B4 (our copy) keeps 203 words: only two short branches were replaced by same-size
  long UJs into body-resident CONTROL and POSTEVAL processors. GOTO sets `C_SPC`;
  IF calls the verbatim shunting-yard EVAL, then compares `value - BW_THRESH` and
  sets `C_SPC` to the resolved first/second/third label.
* The measured body->RAM map is non-linear above body[0o602] (empirically:
  0o604->0o2621, 0o1235->0o3252, 0o1237->0o21066); the builder uses this measured
  map rather than the base builder's linear shortcut.
* Integer increment uses opcode 0o13 (`ARX`, "слц"), not float `A+X`; this was found
  by reading the SIMH opcode implementation.

## 5. Decisive A/B status — FAIL, with raw evidence

C `dispak` advisory oracle (90 s runs, authoritative SIMH capture unavailable):

```
deck A on 2048_B7_A     : rc=0   " 21  0000.00  3000.00"  + " КОНЕЦ ЗАДАЧИ"
deck B on 2048_B7_A     : rc=0   " 21  0000.00  3000.00"  + " КОНЕЦ ЗАДАЧИ"
deck A on 2048_B7_PATCH : rc=0   " 21  0000.00  3000.00"  + " КОНЕЦ ЗАДАЧИ"
```
Earlier intermediate builds gave `21 -0001.00` (IF condition value) or
`21 -0056.78` (always the second branch), proving the scanner/PRINT path works but
the branch-target resolution does not. A control experiment with the IF branch
target **hard-coded in machine code** to token index 6 printed the correct
`21 -0012.34` and reached `КОНЕЦ ЗАДАЧИ`, localising the remaining defect to the
two-pass fix-up / label-table resolution, not to the shunting-yard or printer.

MTR evidence: `CONTROL`, `CTL_IF`, `POSTEVAL` and `FIX1_LABEL`/`FIX2_IF` are all
reached; the IF result value at `N+2[33]` was observed as `f32(10.0)` for `IF (1.0)`;
the compare correctly detects positive vs negative after adding an `AEX 0` to force
logical mode for the exact-zero test. The resolved target cells are nevertheless
wrong, so both branches execute the same token range and print the unwritten symbol
word (0.00).

No SIMH verdict: `drive_b.py` was invoked three times with 240 s / 600 s boot budgets;
every run timed out waiting for the `ДATA:` boot marker. Manual inspection showed
SIMH stuck after `>>> MUX: clear, PRP = 01400` while 5+ other SIMH instances (fixed TCP
ports 4200+) consumed ~90% CPU each on the shared machine. The emulator SHA was
verified on every invocation, but no per-case prn0 capture with a result line was
produced. Therefore the task's decisive SIMH A/B/PATCH/RESTORE gate is **unmet**.

## 6. Exact supported subset of this build (implemented but NOT validated end-to-end)

* One statement per card, columns 7..72; single-digit labels in column 5.
* `IF (<real literal> [, optional unary -]) l1,l2,l3` with arithmetic IF semantics,
  condition evaluated by the verbatim B4 shunting-yard.
* `GOTO <single digit>`.
* `V=<real literal>` assignment (inherited), `PRINT 100,V` with
  `100 FORMAT(1X,F4.2)` (inherited), `END` (inherited).
* Two-digit labels, more than one IF per program, variable operands in IF/GOTO,
  computed GOTO, logical IF, other FORMAT widths are unsupported.

## 7. Blockers

1. **Label fix-up defect**: LABEL->token-index resolution and/or IF target packing
   yields wrong `C_SPC` values; both branches print the untouched symbol word.
2. **SIMH unavailable**: boot hangs in this shared environment (CPU contention and
   fixed-port conflicts), so no authoritative per-case printer capture exists. Only
   the C oracle (advisory) was available.
3. Disk pressure in `/tmp` required repeated cleanup of MTR traces; this did not
   affect the built images but limited further tracing.

## 8. Reproduction

```
cd /tmp/.private/azizz/opencode/b7-control
python3 build/b7_control_build.py --build B7_A
python3 build/b7_control_build.py --build B7_PATCH --patch
python3 build/oracle_run.py CHECK images/2048_B7_A decks/deck_B7_A.b6   # advisory only
python3 build/drive_b.py --case B7A --deck decks/deck_B7_A.b6 --image images/2048_B7_A
```

BLOCKED
