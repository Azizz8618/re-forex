# ftgost-contour: float -> packed-decimal (GOST) entirely in BESM-6 machine code

> ГЛАВНЫЙ РЕЗУЛЬТАТ: машинный float→GOST **PASS** под SIMH. Число, которое
> печатается как X, вычисляется на БЭСМ‑6 (FPU `a/x` 9.0/3.0=3.0, затем
> `aex/e+x/aax/asx`), а не подставляется питоновским весом. SIMH A/B/A:
> `21 3.00 3.00` (baseline) -> правка одного слова данных `21 5.00 3.00`
> или одной команды `21 1.00 3.00` -> restore `21 3.00 3.00` (SHA байтово
> совпадает). Deck только `*TRANS:OURMRK*,,412350`. `*50` под SIMH из контура
> аварийно завершается, поэтому computation идёт через `a/x`. Оговорки
> (диапазон экспонент, отрицательные числа, литералы настройки) — в §3.

Date: 23.11.2026. Workspace: `/tmp/.private/azizz/opencode/ftgost-contour/`
(bulky copies live under `/dev/shm/ftgost-contour/` via symlinks, because the
shared `/tmp` tmpfs was filled by other workspaces). Repo, live disks, tmux
session 0 and dispak C sources were never edited. Every SIMH image was a copy.

## VERDICT: PASS

An on-machine float -> packed-decimal converter runs inside our zone-2350
contour, deposits a digit byte into the existing GOST word at runtime, and the
resident `*64` prints it. The decisive A/B/A under full SIMH is:

| case | one-word change in OUR code | printed line |
|:--|:--|:--|
| A (baseline) | none | `21 3.00 3.00` |
| B1 (data word) | numerator float `9.0` -> `16.0` in zone N+3 | `21 5.00 3.00` |
| B2 (instruction word) | `a/x` operand `0o161` -> `0o160` in zone N+3 | `21 1.00 3.00` |
| restore | byte-identical to A (same SHA-256) | `21 3.00 3.00` |

All four cases reached `КОНЕЦ ЗАДАЧИ`; console showed `2048 - 41` (md41 = our
contour image) and `B075-1 410300000000`.

---

## 1. What was actually executed (FACT, SIMH `set cpu debug` trace)

The contour is entered at RAM `0o1770`. A single same-length substitution in
the body zone replaces the original pre-print GOST word with `uj 30114` (LONG,
reg 0). The 58 clean words of zone `N+3` (RAM `0o30114..0o30205`) hold the
routine and its constants. Modifier reach is the proven `utc 30000` mechanism
(docs/65, docs/88).

Raw SIMH MTR excerpt (`logs/MTR_div9c_raw.txt`), baseline case:

```
01770 L: 00 30 30114 пб 30114
30114 R: 00 22 30000 мода 30000
      M20 = 30000
30115 L: 00 010 0160 сч 160
      Memory Read [30160] = 4211 0000 0000 0000
      ACC = 4211 0000 0000 0000          ; 9.0 (float)
30116 L: 00 016 0161 дел 161
      Memory Read [30161] = 4114 0000 0000 0000
      ACC = 4114 0000 0000 0000          ; 9.0/3.0 = 3.0, BESM-6 FPU division
30117 L: 00 000 0170 зп 170
      Memory Write [30170] = 4114 0000 0000 0000
30120 L: 00 012 0162 нтж 162              ; aex: complement exponent bits
      Memory Read [30162] = 7740 0000 0000 0000
      ACC = 3654 0000 0000 0000
30121 L: 00 024 0163 слп 163              ; e+x const105 -> exp field 168-e
      Memory Read [30163] = 6440 0000 0000 0000
      ACC = 6314 0000 0000 0000          ; computed asx control word
30122 L: 00 000 0166 зп 166
      Memory Write [30166] = 6314 0000 0000 0000
30123 L: 00 010 0170 сч 170
      Memory Read [30170] = 4114 0000 0000 0000
30124 L: 00 011 0164 и 164               ; aax: isolate 40-bit mantissa
      Memory Read [30164] = 0017 7777 7777 7777
      ACC = 0014 0000 0000 0000
30125 L: 00 026 0166 сд 166               ; asx: mantissa -> integer digit
      Memory Read [30166] = 6314 0000 0000 0000
      ACC = 0000 0000 0000 0003          ; digit 3, computed on BESM-6
30126 L: 00 000 0167 зп 167
      Memory Write [30167] = 0000 0000 0000 0003
30130 L: 00 026 0165 сд 165               ; asx: digit << 16 (GOST byte 3)
      Memory Read [30165] = 3000 0000 0000 0000
      ACC = 0000 0000 0060 0000
30130 R: 00 013 2006 слц 2006
      ACC = 0040 0417 0060 7000          ; GOST word A with runtime digit
30131 L: 00 000 2006 зп 2006
30131 R: 00 064 2004 э64 2004 = 2004
30132 L: 15 30 00000 пб (15)              ; return to resident at 0o1764
```

This closes the docs/78 blocker: `aax` + `asx` with an on-machine-computed
control exponent (derived from the float's own exponent via `aex`/`e+x`)
produces the packed decimal digit byte, and `arx`/`atx` deposit it into the
GOST cell before `*64`.

## 2. Image SHAs (SHA-256, re-hashed after runs)

```
a98e81090d4b254554a0cd3ff8611438615de84fc012e8e2b70fbabc2ebdc796  2048_base (repo tool, unchanged)
1a55381b05e06a78dedf04ad7c3c0bb633d325fb6c90a5a4aff91ef2cfdf7786  2048_div9c  (A, baseline)
a39d86fa5a2075e222d7536cfc62e98c34cbed2154aaf4acb2aa565456c7f0d1  2048_ab16   (B1 data word)
656cae1aefb2857d420fbb22b1116b0bd2d4fd283922f7d70c268342e560c7b4  2048_abdiv  (B2 instruction word)
1a55381b05e06a78dedf04ad7c3c0bb633d325fb6c90a5a4aff91ef2cfdf7786  2048_restore (byte-identical to A)
1d93c468c1acf7b6c9d7ac5f002336ce4580d6d716fbc1694aabd605c9bbeae2  deck_trans.b6
```

Deck contains exactly `ДИС 41(2048)^` and `*TRANS:OURMRK*,,412350`; no
`*FOREX`, `*FTN`, `*perso`. SIMH used stock `attach -n prn0/prn1`, copies only,
`ДATA:` boot marker via `capture-pane`, all input via `send-keys`, `ДАЙ А0` /
`ДАЙ А1` / `НОМВ` before the deck. The re-run with an additional post-deck
`НОМВ` failed to boot (shared `/tmp` was 100% full at that moment) and its ACPU
copies are stale; the accepted A/B/A above is from the clean first runs.

## 3. FACT vs INFERENCE

**FACT (observed in this experiment):**
- The printed X digit changes with a one-word change in our contour machine
  code (`3 -> 5` data word; `3 -> 1` instruction word) and returns when the
  image is restored byte-for-byte. The value is therefore produced by machine
  execution in our contour, not by a host-computed weight cell.
- The BESM-6 FPU `a/x` instruction computes the float quotient; `aex` + `e+x`
  compute the shift control word from the result's own exponent; `aax` + `asx`
  turn the mantissa into an integer digit; `asx` + `arx` + `atx` deposit that
  digit byte into GOST word A at RAM `0o2006`; `*64 2004` prints it.
- `utc 30000` reaches high RAM; two consecutive `utc` halfwords accumulate
  M20 (`30000 -> 60000`) and trap. The routine therefore places `utc` in the
  RIGHT halfword of every word so it arms the next LEFT halfword.
- All `*50` extractcode type codes tried (`0`, `2`, `7`) abort from our contour
  under full SIMH (the OS handler at `0o574` diverts and never returns to
  M32 = `0o30116`). docs/78's 12/12 was an MTR/C-emulator result, not SIMH.
- Baseline image SHA `a98e8109...` reproduces docs/87 exactly.

**INFERENCE / not proven here:**
- That the same converter would work for arbitrary floats (exponents outside
  `0o102..0o105`, negative numbers, multi-digit values). Only the quotients
  `3.0`, `5.333...` and `1.0` were exercised.
- That `*50` could be made to work from a different OS context (e.g. a real
  Fortran job). Not attempted; outside the zone-2350 contour gate.

**Explicit setup literals (disclosed, NOT counted as success):**
- Numerator float `9.0` (A) / `16.0` (B1) and denominator float `3.0`, both
  stored as BESM-6 floats in zone N+3. These are the *arguments* to the
  on-machine divide, analogous to the `9.0` in `SQRT(9.0)`; the printed digit is
  not stored anywhere on disk.
- Constants `EXP_MASK`, `CONST105`, `MASK40`, `CW_L16` are converter mechanism
  constants, not result digits.
- The line-number prefix `21` (GOST byte 0 of word A) and the Y field `3.00`
  (GOST word B) remain fixed literals in the contour text. Only the X integer
  digit is computed and deposited at runtime; that is the value under A/B.

**Deviation from the literal task wording:** the float is produced by the
BESM-6 `a/x` FPU instruction, not by a `*50` extractcode, because every `*50`
type tried aborts under SIMH from our contour (FACT above). The computation is
still entirely on-machine and is still value-changing under A/B. C `dispak`
was used only as a source-reading oracle for the `*50` dispatch table.

## 4. Evidence index

- `scripts/build_case.py` - reproducible builder (same-length substitutions in
  body zone `0o2351`, routine/constants in zone `0o2353`).
- `scripts/setup_workspace.py`, `scripts/drive_case.py` - isolated SIMH driver.
- `decks/deck_trans.b6` - contour-only deck.
- `logs/MTR_div9c_raw.txt` - SIMH per-halfword trace excerpt (section 1).
- `runs/acpu_{div9c,ab16,abdiv,restore}.txt` - raw ACPU output.
- `runs/console_{div9c,ab16,abdiv,restore}.txt` - boot/job-start console.
- `images/2048_{base,div9c,ab16,abdiv,restore}` - all SIMH images (copies).

DONE
