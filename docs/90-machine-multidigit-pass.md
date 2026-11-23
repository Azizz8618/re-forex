# ftgost-multi: multi-digit on-machine float -> GOST in the zone-2350 contour

> ГЛАВНЫЙ РЕЗУЛЬТАТ: многозначный machine float→GOST **PASS** под SIMH.
> FPU `123.4/10.0` печатается как `21 0012.34 3000.00`: все четыре цифры
> (2 целые + 2 дробные) извлечены на машине (`aex/e+x/aax/asx`) и вложены
> в GOST‑слово B. A/B одним словом данных `123.4 -> 156.7` даёт `0015.67`;
> байтово тождественный restore возвращает `0012.34`. Знак НЕ реализован —
> конкретный упор в бюджет 58 слов (§5), не подменяется фикцией. Поле Y —
> фиксированный литерал настройки, в счёт не идёт.

Date: 23.11.2026. Workspace: `/tmp/.private/azizz/opencode/ftgost-multi/`
(bulky copies under `/dev/shm/ftgost-multi/` via symlinks, because `/tmp` tmpfs is
100% full). Repo, live disks, tmux session 0 and dispak C sources were never
edited. Every SIMH image was a COPY. The deck is the proven contour-only deck
(`1d93c468...`), containing `ДИС 41(2048)^` and `*TRANS:OURMRK*,,412350`; no
`*FOREX`, `*FTN`, `*perso`. `stock -n prn0/prn1` kept verbatim.

## VERDICT

**MULTI-DIGIT: PASS (decisive SIMH A/B/A).** A float produced by the BESM-6 FPU
(`123.4 / 10.0`) prints as `21  0012.34  3000.00`; four decimal digits (2
integer + 2 fractional) are extracted on-machine with `aex`/`e+x`/`aax`/`asx`
and deposited into the codegen_wide GOST word B at RAM `0o2007` before the
resident `*64 2004` prints. Patching ONE data word of OUR image changes the
printed value to `21  0015.67  3000.00`; restoring the byte-identical image
returns `21  0012.34  3000.00`.

**SIGN: NOT IMPLEMENTED (concrete budget blocker in §5).** The GOST sign byte is
the fixed seed `GOST_SPACE` (15). Negative values were not exercised.

### Decisive A/B/A

| case | one change in OUR image | SIMH ACPU line (verbatim) |
|:--|:--|:--|
| A (baseline) | none | ` 21  0012.34  3000.00` |
| B (data word) | NUM float `f32(123.4)` -> `f32(156.7)` | ` 21  0015.67  3000.00` |
| restore | byte-identical to A (same SHA-256) | ` 21  0012.34  3000.00` |

All three reached `КОНЕЦ ЗАДАЧИ`; console showed `2048 - 41` (md41 = our contour
image), `B075-1 410300000000`, `ОЗ(075) 410300000000`.

### Image SHAs (SHA-256, re-hashed after the runs)

```
a98e81090d4b254554a0cd3ff8611438615de84fc012e8e2b70fbabc2ebdc796  2048_base (repo tool, unchanged)
8b88fa123058e59a97e50d6281f39621cba8fe92f3a9b32bdbc8aba409e56051  2048_AB_A     (A, baseline)
8097b527757edb352b57af5a01e5e85ce8f1305eed0dc69315cff0fa9d7451a5  2048_AB_B     (B, NUM word changed)
8b88fa123058e59a97e50d6281f39621cba8fe92f3a9b32bdbc8aba409e56051  2048_AB_RESTORE (byte-identical to A)
1d93c468c1acf7b6c9d7ac5f002336ce4580d6d716fbc1694aabd605c9bbeae2  deck_trans.b6
```

`cmp -l A B` shows exactly one 6-byte data word in zone N+3 plus the two
recomputed zone-checksum copies (w3 in the primary and duplicate header);
`cmp -l A RESTORE` is empty.

---

## 1. What actually executed (FACT, raw SIMH `set cpu debug` MTR)

Entry is the proven same-length substitution at body `0o11` (RAM `0o1770`):
`LONG uj 30114`. Zone N+3 uses `M[7]=0o30000` as a base register, so every
high-RAM operand is one SHORT halfword (`Aex = addr + M[7]`). All code+data fit
in **45 code + 13 data = 58 words** (`0o30114..0o30205`). Modifier `utc` is NOT
used in the routine; the base register is installed by `utc 30000 ; xta BASE ;
ati 7`.

Raw excerpt from `logs/debug_AB_A.txt` (A case). Octal words are printed as
four 4-digit groups, i.e. 48-bit BESM words.

```
01770 L: 00 30 30114 пб 30114            ; entry
30114 L: 00 22 30000 мода 30000
30114 R: 00 010 0171 сч 171
      Memory Read [30171] = 0000 0000 0003 0000   ; M[7] base constant 0o30000
30115 L: 00 040 0007 уи 7                         ; M[7] = 0o30000
30115 R: 07 010 0172 сч 172(7)
      Memory Read [30172] = 4357 3314 6314 6315   ; 123.4 (float, setup literal)
      ACC = 4357 3314 6314 6315
30116 L: 07 016 0173 дел 173(7)                   ; FPU a/x on the machine
      Memory Read [30173] = 4212 0000 0000 0000   ; 10.0 (float)
      ACC = 4214 2560 5075 3412                   ; V = 12.34 (FPU quotient)
30117 R: 07 016 0173 дел 173(7)
      ACC = 4051 6763 5544 2642                   ; V/10 = 1.234...
30121 L: 07 012 0174 нтж 174(7)
      Memory Read [30174] = 7740 0000 0000 0000   ; EXP_MASK (0o177<<41)
30121 R: 07 024 0175 слп 175(7)
      Memory Read [30175] = 6440 0000 0000 0000   ; C105 (0o151<<41)
30122 L: 07 000 0205 зп 205(7)
      Memory Write [30205] = 6351 6763 5544 2642  ; on-machine CW, exp=0o147
30122 R: 07 011 0176 и 176(7)                     ; aax: isolate mantissa
30123 L: 07 026 0205 сд 205(7)                    ; asx with computed CW
      ACC = 0000 0000 0000 0001                   ; digit 1 (machine-computed)
30124 L: 00 036 0030 сда 30                       ; asn 0o30: digit << 40
30124 R: 00 013 2007 слц 2007                     ; GOST word B += digit byte
      Memory Read [02007] = 0000 0016 0000 0017
      ACC = 0020 0016 0000 0017
30125 L: 00 000 2007 зп 2007
      Memory Write [02007] = 0020 0016 0000 0017
...
30147 L: 07 011 0176 и 176(7)
      ACC = 0015 4631 5231 4600
30150 L: 07 026 0205 сд 205(7)
      ACC = 0000 0000 0000 0003                   ; tenths digit 3
30151 L: 00 036 0060 сда 60                       ; << 16
30151 R: 00 013 2007 слц 2007
      ACC = 0020 1016 0060 0017
30152 L: 00 000 2007 зп 2007
      Memory Write [02007] = 0020 1016 0060 0017
...
30165 R: 07 026 0205 сд 205(7)
      ACC = 0000 0000 0000 0004                   ; hundredths digit 4
30166 R: 00 036 0070 сда 70                       ; << 8
30167 L: 00 013 2007 слц 2007
      ACC = 0020 1016 0060 2017
30167 R: 00 000 2007 зп 2007
      Memory Write [02007] = 0020 1016 0060 2017
30170 L: 00 064 2004 э64 2004 = 2004              ; resident *64 prints
00564 L: 00 042 0016 счи 16                       ; into resident output path
```

The GOST word B written by machine code is `0020 1016 0060 2017`, i.e. bytes
`[1][2][.][3][4][sp]`. Word A carries the fixed prefix `21` and two seeded
zero bytes, hence the printed `21  0012.34  3000.00`.

Digit derivation (all in machine code): `tens=floor(V/10)`;
`units=floor(V)-10*tens` with `floor(V)=10*tens+units`;
`tenths=floor(V*10)-10*floor(V)`;
`hundredths=floor(V*100)-10*floor(V*10)`. A tiny `EPS = f32(2^-18)` is added
before the two fractional floors to undo BESM FPU truncation (`V*100` otherwise
lands at `1233.999...` and floors to 1233).

## 2. Reuse of proven code

Reused verbatim from the predecessor work (`docs/89`, ftgost-contour report):
(a) the repo tool `tools/build_zone2350_contour.py` and its zone writer/checksum;
(b) the base image SHA `a98e8109...`; (c) the contour-only deck and SIMH ini/deck
driver pattern (capture-pane `ДATA:`, `send-keys`, `ДАЙ А0/A1`, `НОМВ`, `at vu0`,
`d 6 1`, `d 5 10`, `set cpu req`, post-job-start `НОМВ`, copies only);
(d) the entry substitution `uj 30114` at RAM `0o1770`; (e) the codegen_wide GOST
layout in body `0o27..0o32`; (f) the `aex`/`e+x`/`aax`/`asx` floor primitive with
an on-machine-computed control word; (g) `arx`/`atx` deposit into GOST word and
resident `*64 2004`. New lines are limited to: the M[7] base-register addressing
(saves ~1 word per high-RAM operand vs the predecessor's UTC-in-right-halfword
pattern), the four-digit arithmetic chain, the `asn` immediate byte shifts, and
the rounding epsilon. The single-word A/B is a new data value, not a new
mechanism.

## 3. FACT vs INFERENCE

**FACT (observed here):**
- The FPU `a/x` instruction on the machine computes `123.4/10 = 12.34`;
  `aex`/`e+x`/`aax`/`asx` with a control word derived from the result's own
  exponent yields the four integer digits 1,2,3,4; `asn`/`arx`/`atx` deposit them
  into GOST word B; `*64` prints `0012.34`. The MTR above shows each digit as an
  ACC value immediately before its byte shift.
- One 6-byte data-word change in OUR image (123.4 -> 156.7) changes the printed
  value from `0012.34` to `0015.67`; a byte-identical restore returns `0012.34`.
  Therefore the printed multi-digit value is produced by machine execution in
  our contour, not by a host-computed weight cell.
- All three cases reached `КОНЕЦ ЗАДАЧИ` with the stock ACPU setup.
- `asn` (opcode 0o36) with address `0o30/0o40/0o60/0o70` performs immediate
  left shifts 40/32/16/8, eliminating four shift-constant cells.
- The M[7] base trick is valid: `SHORT op,adr,reg=7` addresses `0o30000+adr`;
  the MTR shows every high-RAM read at `0o30xxx` with `reg=7`.
- Baseline image SHA and deck SHA are byte-identical to the predecessor work.

**INFERENCE / not proven here:**
- Arbitrary exponents, arbitrary 2-digit fractions, negative values, and values
  >= 100 were not exercised. The epsilon bias is proven for the two cases run;
  it is not a general rounding proof.
- The sign byte is a fixed space; no negative float was run.

## 4. Explicit setup literals (disclosed, NOT counted as success)

- `NUM = f32(123.4)` in A/restore, `f32(156.7)` in B (the ONLY changed word),
  and `TEN = f32(10.0)`: arguments to the on-machine `a/x`. They are inputs,
  analogous to `9.0` in `SQRT(9.0)`; no result digit is stored on disk.
- Converter mechanism constants: `EMASK=0o177<<41`, `C105=0o151<<41`,
  `M40=0xFFFFFFFFFF`, `EPS=f32(2^-18)`, `BASE=0o30000`, `ASN` immediates.
- Fixed GOST bytes: line prefix `21` and sign `sp` (word A), point `.` (word B
  byte 2), Y text `3000.00` (words C/D), `EOF=0o231`. Only the four X digit bytes
  are computed and deposited at runtime; the two leading `0` digits in `0012.34`
  are seeded zeros from the codegen_wide layout, not machine-computed digits.

## 5. Concrete blocker: sign in the 58-word budget

The routine occupies all 58 words (45 code + 13 data), so there is no room for
sign handling. A machine negative-sign deposit needs roughly 4-6 more words:
isolate bit 40 of V (a mask cell), form 11 (minus) vs 15 (space) for GOST word A
byte 3 (`asn` shift left 16, `arx G_A`, `atx G_A`), plus a conditional branch if
computed arithmetically. Freeing that space would require refactoring the four
floor+deposit blocks into a `vjm` subroutine (plausible, not attempted here).
Per the task's instruction, this is reported rather than faked. **Maximum proven
width: 2 integer + 2 fractional digits computed on-machine, printed with two
additional seeded leading zeros (4 integer positions total), positive sign.**

## 6. Evidence index

- `scripts/build_own2.py` - reproducible builder (same-length substitutions;
  code+data in zone N+3).
- `scripts/setup_own.py`, `scripts/drive_own.py`, `scripts/drive_trace.py` -
  isolated SIMH driver (copies only, no tmux 0, no live disks).
- `decks/deck_trans.b6` - contour-only deck (SHA above).
- `images/2048_AB_{A,B,RESTORE}` and `images/2048_base` - all SIMH images (copies).
- `runs/acpu_{AB_A,AB_B,AB_RESTORE}.txt` - raw ACPU output (printed lines at
  line 99).
- `runs/debug_AB_A.txt` - raw SIMH MTR trace (359,728,284 bytes; SHA above);
  routine starts at the first `мода 30000` line.
- `runs/console_AB_A.txt` - boot/job-start console.
- `runs/drive_AB_{A,B,RESTORE}.log` - driver transcripts.
- ACPU SHA-256: A `c4af6c72...`, B `81676e3c...`, RESTORE `30f9a494...`.

DONE
