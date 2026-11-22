# GO/NO-GO: can the `*TRANS` body copy window extend beyond `body[0..0o43]`?

> Предисловие главного агента: субагент измерил кусочно-сдвинутую карту копирования
> и закрыл go/no-go как GO. Я лично перепроверил ключевой факт на копиях:
> `body[0o46]=3<<40` и изменение `body[9]` на чтение `0o2041` дают печать
> `41 1.00 3.00` при `КОНЕЦ ЗАДАЧИ`, а дамп ядра содержит это слово по адресу
> `0o2041`. Важная оговорка §3.2 сохраняется: расширенная область пересекается
> с исполняемыми словами резидентного 4.12, поэтому это не «свободная память».

**Date:** 22.11.2026. **Work dir:** `/tmp/.private/azizz/opencode/re-forex-limit-window/`.

## VERDICT: **GO** — the copy does NOT stop at `body[0o43]`.

The phase-3 conclusion "`copy stops at body[0..0o43]`" was an **artifact of reading the wrong RAM
addresses**. Body words at offsets `0o45` and above ARE copied into RAM, but with a **piecewise
address map containing holes and shifted segment bases**. Data placed at `body[0o46]` is not only
copied: it was read by our own code and changed the printed result in a closed A/B test.

The "35-word window" is the *first contiguous low-RAM segment*, not a structural loader limit.

---

## 0. Scope and provenance (FACT)

* Only the designated work dir was used for scripts/reports/evidence. The bulky per-case disk copies
  live in `/dev/shm/re-forex-limit-window-cases`, reached through the `cases -> /dev/shm/...` symlink
  inside the work dir. Reason: shared `/tmp` tmpfs was at 100% (ENOSPC on the first case). No other
  session's files, no repo files, live disks, tmux, processes, git state or dispak C sources were
  touched. `HOME` and `BESM6_PATH` were redirected to per-case copies.
* Install recipe reused **verbatim** from `tests/plan-f77/70-computed-output/run.py` and
  `tests/plan-f77/72-bound-driven/installer.py`:
  * zone `N = 0o2350`: catalog = `O412C.FTN` words `0..15`;
  * zone `N+1`: body `0..18` = `O412C` words `16..34`, body `19..1023` = `O412D` tail (1005 words);
  * zone `N+2`: `O412C` words `35..409` placed at words `526..900`; zones `N+3..N+40` zero;
  * deck `*TRANS:OURMRK*,,412350`; code at body `9..12`, descriptor/GOST at `0o25..0o31`,
    operands at `0o41/0o42`, exactly as in test 70.
* Probe mechanism identical to phase 3: `BESM6_CORE_ON_PC=1770`, `BESM6_CORE_SKIP=6`,
  `BESM6_DD_DEBUG=1`, `BESM6_MTR_N=0`; RAM read from `core-pc.bin` at `0o1757 + body_index`.
  Sentinel word = `0o00007777000000<offset>` (high half `0o7777`, low half = offset), so a hit is
  unambiguous.

### 0.1 Baseline re-established (FACT)

`cases/baseline/out.txt`: `rc=0`, console line `21 1.00 3.00`, `КОНЕЦ ЗАДАЧИ` present. Core dump
valid; RAM `0o1770..0o1773` equals disk `body[9..12]` byte-for-byte. This is the unchanged test-70
baseline; every later case is a one-field or one-word variation of it.

---

## 1. Precise copy probe (FACT)

One sentinel per case, all other words at baseline. `arrived?` means the sentinel was found at the
*naive* address `0o1757+k`; `actual` is where the sentinel really was found by a full-RAM scan.

| body offset | naive RAM | word at naive address | real RAM (full scan) | arrived at naive? | marker |
|---:|---:|:--|:--|:--|:--|
| `0o40` | `0o2017` | sentinel | `0o2017` | **yes** | `21 1.00 3.00` |
| `0o41` | `0o2020` | sentinel | `0o2020` | **yes** | none (operand overwritten) |
| `0o42` | `0o2021` | sentinel | `0o2021` | **yes** | none (operand overwritten) |
| `0o43` | `0o2022` | sentinel | `0o2022` | **yes** | `21 1.00 3.00` |
| `0o44` | `0o2023` | NO DUMP | nowhere | **no** (TIMEOUT) | none |
| `0o45` | `0o2024` | `0` | `0o2216` (also `2217,2220,2221,2222`) | **no at naive, yes relocated** | `21 1.00 3.00` |
| `0o46` | `0o2025` | `0` | `0o2041` | **no at naive, yes relocated** | `21 1.00 3.00` |
| `0o50` | `0o2027` | `0` | `0o2043` | relocated | `21 1.00 3.00` |
| `0o60` | `0o2037` | `0` | `0o2053` | relocated | `21 1.00 3.00` |
| `0o70` | `0o2047` | resident code | `0o2063` | relocated | `21 1.00 3.00` |
| `0o100` | `0o2057` | resident code | `0o2073` | relocated | `21 1.00 3.00` |
| `0o200` | `0o2157` | resident code | `0o2173` | relocated | `21 1.00 3.00` |

This single table falsifies the phase-3 "hard boundary at `0o43`": offsets `0o45..0o200` are all
present in RAM, just shifted by `+0o14` words from the naive address. Phase 3 sampled the naive
address and saw zero/resident code.

### 1.1 The word at `body[0o44]` is load-bearing (FACT)

Baseline `body[0o44] = 0o4000000000500155`, i.e. descriptor fields
`f3=0o4000 f2=0 f1=0o0050 f0=0o1551` (an overlay descriptor for zone `0o1551`). It is **not copied**
to RAM (no hit anywhere in low RAM). Fourteen replacement values were tried
(`0, 1, 0o10, 0o40, 0o44, 0o45, 0o50, 0o100, 0o777, 0o7777, 0o0000777700000044, 0o1600043,
0o73461`, and baseline): every non-baseline value produced `TIMEOUT` or a run without the marker and
without a core dump. The loader/resident compiler consumes this word from the `*70` input buffer;
it must be preserved verbatim.

---

## 2. Complete body → RAM map (FACT)

Measured with one sentinel per case at 4-word to 32-word intervals and exact boundary narrowing.
All cases kept `body[0o44]`, `body[0o223]`, `body[0o603]` intact.

| body index range | RAM address | note |
|:--|:--|:--|
| `body[0]` | not copied | RAM `0o1757` reads `0`; service word `0o1600043` stays only in the `*70` buffer |
| `body[1] .. body[0o43]` | `0o1757 + k` | original "window"; unchanged from phase 3 |
| `body[0o44]` | **not copied** | overlay descriptor `f0=0o1551`; MUST stay intact |
| `body[0o45]` | `0o2216` (replicated at `0o2217,0o2220,0o2221,0o2222`) | special relocation |
| `body[0o46] .. body[0o222]` | `0o1773 + k` (shift `+0o14`) | **usable extended region** |
| `body[0o223]` | **not copied** | descriptor `0o0000000001700357`, `f0=0o0357`; MUST stay intact |
| `body[0o224] .. body[0o602]` | `0o1777 + k` (shift `+0o20`) | second extended segment |
| `body[0o603]` | **not copied** | descriptor `0o0000001561300432`, `f0=0o0432`; MUST stay intact |
| `body[0o604] ..` | `0o2015 + k` (shift `+0o36`) | third extended segment |

INFERENCE: the three special words are section/overlay descriptors; each one's consumption advances
the destination base for the following segment. The exact arithmetic of the advance (`+0o14`, then
`+0o4`, then `+0o16` on the base) is not decoded; it is a property of the O412D tail data, not of any
field we are free to tune.

---

## 3. Executability / usability proof (FACT)

### 3.1 Data in the extended region is read by our code

Our entry code at `0o1770` was changed from `ARX A1(0o2020)` to `ARX 0o2041`, i.e. the first addend
is now fetched from `body[0o46]`. Everything else (descriptor, GOST text, `*64` print) is baseline.
The printed leading digit is `0 + value(body[0o46]) + 1`:

| case | value written to `body[0o46]` | printed | reading |
|:--|:--|:--|:--|
| `data_control` | baseline (not an operand) | `21 1.00 3.00` | baseline `0+1+1` |
| `data_ext3` | `3 << 40` | **`41 1.00 3.00`** | `0+3+1` |
| `data_ext5` | `5 << 40` | **`61 1.00 3.00`** | `0+5+1` |
| `data_ext3_zero` | `0` | `11 1.00 3.00` | `0+0+1` |

All four ran to `КОНЕЦ ЗАДАЧИ` with `rc=0`. This closes causality on the *value* stored beyond
`0o43`: it arrives at RAM `0o2041` and is consumed by our instruction.

### 3.2 The region is also executed (FACT)

An MTR trace with `BESM6_MTR_LO=2041 HI=2042` shows PC `0o2041` reached and the baseline word at
`body[0o46]` decoded as `u1a 1776(0)`. So the extended segment overlaps resident-compiler code.

INFERENCE / CAVEAT: writing our data at `body[0o46+]` overwrites resident 4.12 words that are
themselves executed. The minimal minimal-path test above tolerated this, but a full compiler must
account for it: the clean, non-resident window remains `body[1..0o43]`. The extended region is
available, but it is *shared* with resident code rather than free scratch.

### 3.3 Negative control (FACT)

Redirecting the 4.12 stub's `пб 464` to `0o2041` (`body[5] = 0o7240176003002041`) and/or jumping
from `body[9]` with a guessed `uj 2041(15)` produced **no** change in the print. These paths are not
the hand-off used on this install; they are not part of the recipe and are reported only to avoid
implying an unproven execution route. (Q1 in docs/62 §6 remains open.)

---

## 4. Copy-loop trace evidence (FACT)

`trace_copyloop.txt`, window `BESM6_MTR_LO=0660 HI=0730 N=50000`, captured on the unmodified
baseline (251,111 output lines, 250,000 MTR records, marker still printed):

```
00660L xta 1(16)        ; AU = descriptor from 0o1153; M3 = 0o03530 (initial)
00670R *70 145(0)       ; read body zone -> *70 input buffer at M5 = 0o64000
00673L mtj 6(5) / 00673R utc 0(0)   ; M6 = receiver, starts 0o1760
00674L vzm 712(3) / 00674R vjm 736(15)  ; branch by M3; M11 = 0o70, M12 = 0o204
00701L xts 0(0) / 00702L vzm 706(11) / 00702R vjm 736(15)   ; fetch next source word
00703L atx 0(6)         ; STORE copied word to receiver M6
00703R utm 77777(3)     ; M3 -= 1
00704L utm 77777(11)    ; M11 -= 1
00704R utm 1(6)         ; M6 += 1
00705L uj 702(0)        ; loop
```

Machine-derived numbers:

* 21,723 `atx 0(6)` stores were executed in this trace window; `M6` runs from `0o1760` up to `0o14000`
  (multiple copy phases / reloaded counters).
* `M3` starts at `0o3530` and reaches `0`; `M11` starts at `0o70` and reaches `0` before being
  reloaded; both are decremented by `utm 77777` (add `-1`). Loop termination is counter exhaustion,
  **not** a sentinel in the body stream at `body[0o43]`.
* The subroutine at `0o736..0o741` (`wtc 153 / xta <M5> / xts 153 / arx 746 / atx 153 / uza 742 /
  stx 0 / uj 0(15)`) fetches the next word from the `*70` buffer addressed by `M5 = 0o64000`.

INFERENCE: the apparent 36-word boundary is a *destination layout* feature (three special descriptor
words plus per-segment base shifts), not the loop's stop condition. This is consistent with §2 and
with the successful relocation of `body[0o45+]`, and inconsistent with the phase-3 "hard stop" claim.

---

## 5. Field-variation matrix (FACT)

All cases include a sentinel at `body[0o45]` and keep `f0 = 0o1760`. `marker` = `21 1.00 3.00`;
`winGrew` below was originally checked at the **naive** RAM `0o2024`, which we now know is the wrong
address; no variation changed the segment map in any case, so the column is uniformly `False`
regardless of address choice.

| field varied | values tried | result |
|:--|:--|:--|
| catalog `f3` | `0`, `0o401`, `0o411`, `0o777` (baseline `0o400`) | `0` keeps marker; **all others TIMEOUT** |
| catalog `f2` | `0`, `0o4236`, `0o0236`, `0o7777` (baseline `0o4027`) | **all TIMEOUT** |
| catalog `f1` | `0`, `0o7303`, `0o3403`, `0o7777` (baseline `0o5710`) | `0` TIMEOUT; others `rc=0` but no marker / no core dump (our entry never reached) |
| `f0` | fixed `0o1760` per docs/62 §3.1 | constraint confirmed by prior M4 sweep; not re-swept here |
| body[0] service | `0`, `0o43`, `0o44`, `0o100`, `0o7777`, `0o1600043` | **only exact baseline `0o1600043` keeps marker** |
| w0 `head` | `0`, `1`, `0o1777` (baseline `0o1200`) | marker survives, no change |
| w0 `sym` | `0`, `2`, `0o7777` (baseline `0o7023`) | marker survives, no change |
| w0 `debug` | `0`, `0o7777` (baseline `0o4657`) | marker survives, no change |
| w1 `set` | `0`, `0o77777` (baseline `0o73377`) | marker survives, no change |
| w1 `data` | `0`, `0o77777` (baseline `0o100`) | marker survives, no change |
| w1 `long` | `0`, `0o77777` (baseline `0o377`) | marker survives, no change |
| w2 `cmd` | `0`, `0o11`, `0o1777`, `0o7777` (baseline `0o1760`) | marker survives, no change (confirms docs/62: `cmd` cannot substitute for `f0`) |
| w2 `bss` | `0o100`, `0o77777` (baseline `0`) | marker survives, no change |
| w2 `const` | `0`, `0o1000` (baseline `0o222`) | marker survives, no change |
| `cmd[0]` marker | `0`, `0o77777` (baseline `0o73461`) | marker survives, no change |
| `cmd[1]` stub | `0` (baseline `0o7240176003000464`) | marker survives, no change |

INFERENCE: none of the tunable fields controls the segment map. The map is a property of the O412D
tail descriptors at `body[0o44]/[0o223]/[0o603]`. Q3/Q4 in docs/62 §6 are therefore answered
negatively with respect to window growth: field tweaking cannot move the boundary; choosing the
right *body index* can.

---

## 6. Reproducible recipe (GO)

To place data or code for our compiler beyond the first segment:

1. Keep the install exactly as test 70 / 72 (zone `0o2350`, catalog descriptor `f0=0o1760`,
   `f3=0o400`, `f2=0o4027`, `f1=0o5710`, service word `body[0]=0o1600043`).
2. Keep the special words untouched: `body[0o44]=0o4000000000500155`,
   `body[0o223]=0o0000000001700357`, `body[0o603]=0o0000001561300432`.
3. Put the new data/code in `body[0o46] .. body[0o222]`. Its address in RAM is **`0o1773 + k`**.
   Example: `body[0o46]` -> `0o2041`, `body[0o50]` -> `0o2043`, `body[0o100]` -> `0o2073`.
4. Address all operands/branch targets from that base. A closed A/B for reading such an operand is
   `body[9] = XTA GOST(0o2006) / ARX 0o2041` plus a value at `body[0o46]`; printed digits
   `3 -> 41`, `5 -> 61`, `0 -> 11` were verified.
5. For a second segment use `body[0o224] .. body[0o602]` -> RAM `0o1777 + k`; after `0o603` use
   `0o2015 + k`.
6. Do **not** rely on `body[0o45]` at the naive address; its real home is `0o2216` (replicated).
7. Caveat: the extended region overlaps resident 4.12 words that are executed (MTR at `0o2041`).
   Verify any production use with the same A/B + `КОНЕЦ ЗАДАЧИ` + CORE-dump checks used here.

---

## 7. What was NOT proven (honest boundary)

* The exact field semantics of `f3/f2/f1` (Q3) and `пб 464` absolute-vs-relative (Q1). Our field
  sweep shows they gate loading but do not resize the window.
* Why each special descriptor advances the base by its specific amount; only the resulting map was
  measured, not the arithmetic that produces it.
* A *full* Fortran compiler occupying the extended region, with resident code still functioning.
  Only a data-read A/B and the minimal print path were exercised.
* The baseline tests 66-74 were not re-run wholesale, but test 70/72's install was reproduced and its
  marker, `КОНЕЦ ЗАДАЧИ`, CORE mapping and entry words were verified unchanged; every variation was
  incremental on that baseline.

**Next experiment if deeper certainty is wanted:** a breakpoint/MTR trace at PC `0o660..0o674` with
per-field variations of `f3/f2/f1` (Q3) would reveal how the segment base and the `M3` branch are
computed from descriptor bits; a trace at `0o736..0o741` with `M5` observation would show how the
three special descriptor words advance the destination base. Both are copy-only and are specified
in docs/62 §6 Q1/Q3.

---

## 8. Evidence index (all under the work dir)

| file / dir | content |
|:--|:--|
| `harness.py` | reusable installer/probe harness (test-70 recipe + CORE/MTR hooks) |
| `probe_copy_window.txt` | 12-offset copy-limit probe matrix |
| `probe_44.txt` | `body[0o44]` replacement experiment (14 values) |
| `map_sweep.txt`, `map_breaks.txt` | full piecewise body→RAM map and exact breakpoints |
| `exec_data.txt` | A/B proof that `body[0o46]` data is read by our code (`41/61/11`) |
| `exec_extended.txt`, `exec_jump.txt` | negative controls (stub redirect / guessed jump) |
| `trace_copyloop.txt` | 250,000-record MTR trace of P4 decode + copy loop |
| `field_variation_results.tsv` | 43-case one-field-at-a-time matrix |
| `cases/<name>/{out.txt,core-pc.bin,body.bin,patches.txt}` | per-case raw evidence (disks on `/dev/shm/...`) |

DONE: GO. The body copy window is not structurally capped at `body[0..0o43]`; words beyond it are
copied at a measured, piecewise-shifted address map, and a value at `body[0o46]` was read by our code
and changed the printed output in a closed A/B. Recipe and caveats are in §6.
