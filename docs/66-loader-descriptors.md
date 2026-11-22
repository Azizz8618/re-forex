# re-forex / decisive: NEWCOMP* 4.12 descriptor-field decode and attempt at a >58-word load

> Предисловие главного агента: я лично повторил 3-случайный A/B из §8 — база
> (`f2=0o4027`) печатает маркер и читает 3 зоны, обнуление `f2` уходит в 31 зону
> и таймаут без `КОНЕЦ ЗАДАЧИ`, восстановление возвращает маркер. Это закрывает
> вопрос «почему нельзя просто увеличить дескриптор»: поля — ключ загрузчика,
> а не длина. Отрицательный результат здесь не стоит на месте: он позволяет
> выбрать честную границу (58 чистых слов) и искать память другим путём.

**Date:** 22.11.2026. **Write scope:** only `/tmp/.private/azizz/opencode/re-forex-desc/`.
No repo edits, no git writes, no live disks/tmux/processes, no dispak C patches.
`HOME`/`BESM6_PATH` redirected to per-case copies; bulky case disks in
`/dev/shm/re-forex-desc-cases`. Harness copied verbatim from
`tests/plan-f77/80-high-ram-zone/harness.py` (only `REPO_ROOT` override supplied).

## VERDICT: FAIL for ">58 usable words"; loader contract is closed

A **consistent multi-field descriptor set that copies more than 58 clean words does not exist
for this install path.** The fields are not independent length/zone knobs: `f1=0o5710` and the
exact pair `f2=0o4027`, `f3[5:0]=0` form a *key*. Every deviation either (a) suppresses the body
load entirely (clean exit, no marker) or (b) drives the loader into a non-terminating overlay
loop at `0o707..0o711` that reads 95..2251 zones and never reaches our entry. The three
load-bearing body descriptors are equally rigid: any change to any of them, alone or jointly
with a catalog change, also hangs the loader.

**This is not a fallback to the 58-word path.** The 58-word result is reported only as the
measured baseline that could not be improved; the goal is explicitly scored FAIL below.

---

## 1. Method (FACT)

For each case the install is exactly tests 66/70/78/80 (zone `N=0o2350`, catalog = `O412C` words
0..15, body `N+1`, z2 `N+2`, zones `N+3..N+40` zero unless patched), deck
`*TRANS:OURMRK*,,412350`, marker `21 1.00 3.00`.
Probes:

* `BESM6_DD_DEBUG=1` prints `DD pc=NNNNNx r016=... u=.. z=.... uil=a/b/c uir=d/e/f`.
  At pc `0o671` this is the `*70` that reads the body; `uil` and `uir` are the **assembled INF
  word at RAM `0o145`** unpacked into (opcode/reg/addr) of its two halfwords. This is the direct
  observation of the descriptor-to-INF map requested by docs/62 §6 Q3.
* `BESM6_MTR_LO=0660 BESM6_MTR_HI=0711 BESM6_MTR_N=40..80` traces the decode and copy loop with
  all 16 index registers, so `M3`, `M6`, `M11`, `M12` and the branch at `0o674` are visible.
* `BESM6_CORE_ON_PC=1770 BESM6_CORE_SKIP=6` dumps full RAM at our entry (or `=674` for an
  in-loader dump). Sentinels `0o000077770000<k>` uniquely identify zone words.
* Timeout per case 20..60 s (trace on) and 240 s (trace-free) for hang cases.

Baseline reproduced exactly: `rc=0`, `21 1.00 3.00`, `КОНЕЦ ЗАДАЧИ`, CORE valid.

---

## 2. Field-to-effect map (FACT)

Descriptor `d = f3<<36 | f2<<24 | f1<<12 | f0`. Catalog descriptor is zone `N` word **3**;
the scanned value is copied to the descriptor buffer at `core[0o1153]` (verified in CORE dump:
`01153 0400402757101760`).

| field | baseline | observed role | effect of changing |
|:--|:--|:--|:--|
| **f0** | `0o1760` | main-section ID / load base | any other value (`0o1551`, `0o2351`, …) -> rc=0, clean `КОНЕЦ ЗАДАЧИ`, **no body read, no marker** (`sat_results.tsv`) |
| **f1** | `0o5710** | load-enable / entry key | `0`, `0o3403`, `0o7303` -> **no body read**; `0o5710` is the only tested value that loads anything (`pairs_results.tsv`, `sat_results.tsv`) |
| **f2** | `0o4027` | exact key, NOT a count | 17 values swept (`0`, `0o4000`..`0o4300`) -> **only `0o4027`** gives the terminating 3-zone load; all others read 95..110 zones and hang (`fine_results.tsv`) |
| **f3 bits 5..0** | `0` | branch mode selector | `!=0` (`0o401`, `0o402`, `0o404`, `0o410`, `0o420`) -> satellite/overlay mode, 87..2251 zones, hang; high bits are don't-care (`0`, `0o400`, `0o1000`, `0o2000`, `0o4000`, `0o7400` all behave identically) (`f3sweep`, `sweep2_results.tsv`) |

Satellite catalog entries (LO*SYN `0o0401423673031551`, LO*GEN `0o0411023634031551`) are copied
into the descriptor buffer but **never loaded**: promoting their `f0` to `0o1760` or to `0o2351`
does not change the zone set (`satpromote.py`, 5/5 cases still 3 zones `2351..2353`).

### 2.1 Assembled INF word at `0o145` (Q3 answered)

| read | pc | `uil` (op/reg/addr) | `uir` (op/reg/addr) | disk/zone |
|:--|:--|:--|:--|:--|
| catalog | `0o3022` | `10/0/300` | `41/0/2350` | 41 / N |
| body first | `0o671` | `10/0/3200` | `41/0/2351` | 41 / N+1 |
| body next | `0o744` | `10/0/3200` | `41/0/2352`, `2353` | 41 / N+2, N+3 |

The page field `0o3200` (vs `0o300` for the catalog) and the zone `N+1` are assembled by the
`0o660..0o670` shift/mask chain; the `DD` traces show it is **identical for every working
descriptor**, i.e. the fields gate the *mode* and the *counter values*, not the INF layout
directly. M3 is loaded at `0o661L` (`ati 3(0)`) to `0o03530` for the key combination.

---

## 3. Exact descriptor words used

| role | word (octal) | f3 | f2 | f1 | f0 | source |
|:--|:--|--:|--:|--:|--:|:--|
| catalog main (baseline) | `0400402757101760` | `0400` | `4027` | `5710` | `1760` | `O412C.FTN` CAT 03 / disk `2350.0003` |
| f2 zeroed (A/B B) | `0400000057101760` | `0400` | `0000` | `5710` | `1760` | this report |
| f2 alternate (hang) | `0400423657101760` | `0400` | `4236` | `5710` | `1760` | this report |
| f3 satellite (hang) | `0401402757101760` | `0401` | `4027` | `5710` | `1760` | this report |
| LO*SYN (satellite) | `0401423673031551` | `0401` | `4236` | `7303` | `1551` | catalog `2350.0005` |
| LO*GEN (satellite) | `0411023634031551` | `0411` | `0236` | `3403` | `1551` | catalog `2350.0007` |
| body[0o44] (kept) | `4000000000500155` | `4000` | `0000` | `0050` | `0155` | zone `N+1` word 36 |
| body[0o223] (kept) | `0000000001700357` | `0000` | `0000` | `0170` | `0357` | zone `N+1` word 147 |
| body[0o603] (kept) | `0000001561300432` | `0000` | `1561` | `3004` | `0432` | zone `N+1` word 387 |

Note: docs/64 §2 quotes `f0=0o1551` for `body[0o44]`; the **installed** word is
`...500155`, i.e. low field `0o0155`. This was verified from `body.bin`; it does not change the
conclusion (all replacement attempts failed).

---

## 4. Rejecting instruction (FACT)

Both the successful and the failed loads use the same copy loop. The exit is via two `vzm`
tests; with non-key descriptor fields the counters are far too large to satisfy them:

```
00703L atx    0(6)      ; store copied word to M6
00703R utm 77777(3)     ; M3 -= 1
00704L utm 77777(11)    ; M11 -= 1
00704R utm    1(6)      ; M6 += 1
00705L uj   702(0)
00707L vzm  674(12)     ; EXIT test 1: branch to 00674 when M12 == 0
00710L utm 77777(3)     ; M3 -= 1
00710R utm 77777(12)    ; M12 -= 1
00711L utm    1(6)      ; M6 += 1
00711R uj   707(0)      ; unconditional loop
00674L vzm  712(3)      ; EXIT test 2: branch to 00712 when M3 == 0
00674R vjm  736(15)
```

Baseline exit (MTR, last records):
`MTR 00711R ... M3=00000 M6=14000 M11=00000 M12=00000`,
`MTR 00707L vzm 674(12)`, `MTR 00674L vzm 712(3)`, then `00712L xta 0(0)` (next phase).

Failed case `f2=0` at the 240 s cutoff:
`M3=27215 M6=53334 M11=00000 M12=76503`; the loop keeps decrementing M3/M12 and M6 keeps
climbing, while the `*70` loop reads zones `2351..2407` (31 zones, 36,648 `atx 0(6)` stores).
Failed case `f2=0o4236`: `M3=16110 M6=22441 M12=00001`, zones `2351..2526` (110 zones,
12,930 stores). Neither reaches `КОНЕЦ ЗАДАЧИ` in 240 s with tracing on or off, and neither
ever executes our entry at `0o1770` (no CORE dump at `CORE_ON_PC=1770`).
**Decisive run:** `f2=0o4236` with `core=True`, no MTR, `timeout=850 s` ->
`rc=TIMEOUT end=False print=None core=False zones=110 range=2351..2526 elapsed=850.2 s`
(`decisive.log`). The load never completes even after 14 minutes.

This is the exact rejecting mechanism: **`vzm 674(12)` / `vzm 712(3)` never see both counters
zero**, so control never leaves `0o707..0o711` for the hand-off at `0o712..`.

---

## 5. Failed combinations (exhaustive within scope)

| experiment (script / result file) | combinations | outcome |
|:--|:--|:--|
| `sweep2.py` → `sweep2_results.tsv` | 7 single-field catalog cases | only baseline/`f3=0` work; all others hang or suppress load |
| `pairs.py` → `pairs_results.tsv` | 27 f3×f2×f1 triples | exactly 1/27 (`400,4027,5710`) gives marker; 10 hang with 31..117 zones; 16 suppress load |
| `fine.py` → `fine_results.tsv` | 17 f2 values | exactly 1/17 (`0o4027`) works; 16 hang with 95..110 zones |
| `f3sweep.py` | 9 f3 values | low6=0 works (4/4), low6!=0 hangs (5/5, up to 2251 zones) |
| `sat.py` → `sat_results.tsv` | 8 catalog field sets incl. real satellites | only main key works |
| `satpromote.py` | 5 satellite-promotion variants | no change (3 zones always) |
| `joint.py` → `joint_results.tsv` | 12 catalog f2/f3 **+ body[0o44]/[0o223]/[0o603]** joint variants | 0/12 improve; all hang |
| `coreprobe.py` | CORE at `0o674` for baseline vs `f2=0o4236` | identical before divergence; failed case never reaches entry |
| `bodylim.py` → `bodylim_results.txt` | 7 body[0o603] variants with 1024 sentinels in N+3 | only baseline loads (58 sentinels); all 6 changes hang |
| docs/64 §1.1 (prior) | 14 body[0o44] replacements | only baseline works |

---

## 6. RAM map achieved (FACT)

Baseline, full-RAM sentinel scan of `cases/cases/bl_base/core-pc.bin`
(1024 distinct sentinels written to zone `N+3`):

* `zone N+3 (0o2353) word k -> RAM 0o30114 + k`, `k=0..0o71`, **58 contiguous words**,
  all 58 present, no holes (identical to docs/65).
* 3 further sentinel-like words at `0o53403`, `0o100226`, `0o100520` (monitor/task areas, not usable).
* Zones `N+4..N+40` contribute **no image at our entry** under any tested descriptor set.
* Failed descriptor sets: **no CORE dump at all** because our entry at `0o1770` is never reached.

Thus the measured usable region stays at 58 words; no larger contiguous clean region was created.

---

## 7. CORE / MTR evidence index

| file | content |
|:--|:--|
| `probe_400_4027_5710.out` | baseline DD (524 `*70` lines) + MTR decode/copy/exit |
| `logs/f3_0401.out`, `f3_0401_nomtr` case | 125+ zone reads, non-terminating `0o707..0o711` loop |
| `diag_f2base` / `diag_f2zero` / `diag_f2alt` cases (out.txt in `/dev/shm/re-forex-desc-cases/cases/`) | MTR loop tails with M3/M6/M11/M12 |
| `core_baseline_674`, `core_fail_674` cases | CORE dumps at `0o674` for working vs failing load |
| `bl_base` case | CORE at entry with 1024 zone-N+3 sentinels -> 58 at `030114..030205` |
| `decisive.log` | 850 s decisive run: `TIMEOUT`, no entry, 110 zones read |
| `sweep2_results.tsv`, `pairs_results.tsv`, `fine_results.tsv`, `sat_results.tsv`, `joint_results.tsv`, `bodylim_results.txt`, `ab_results.txt` | all numeric result tables |
| `fieldprobe.py`, `sweep2.py`, `pairs.py`, `fine.py`, `sat.py`, `joint.py`, `bodylim.py`, `ab.py`, `coreprobe.py`, `harness.py` | reproducible scripts |

---

## 8. 3-case A/B (change a field, zero a field, restore) — FACT

All cases use the same install; only catalog descriptor word 3 changes.

| case | descriptor | rc | `КОНЕЦ ЗАДАЧИ` | print | body zones |
|:--|:--|:--|:--|:--|:--|
| A baseline | `0400402757101760` | 0 | yes | `21 1.00 3.00` | 3 (`2351..2353`) |
| B f2 zeroed | `0400000057101760` | TIMEOUT | **no** | none | 31 (`2351..2407`) |
| C restored | `0400402757101760` | 0 | yes | `21 1.00 3.00` | 3 (`2351..2353`) |

Causality is closed: zeroing `f2` changes a 3-zone terminating load into a 31-zone hang;
restoring the exact word restores the marker. The "failed" case does **not** end with
`КОНЕЦ ЗАДАЧИ`, which is the observable rejection at the console.

---

## 9. PASS/FAIL

| criterion | result |
|:--|:--|
| field-to-effect map derived (length vs zone vs base vs entry) | PASS (§2, with the result that f2/f1 are keys, not lengths) |
| consistent multi-field set with >200 clean words | **FAIL** |
| more than 58 usable words (any amount) | **FAIL** |
| exact rejecting instruction and failed combinations shown | PASS (§3, §4, §5) |
| marker preserved in any improved set | N/A (no improved set exists) |

**Final answer: the goal "more than 58 usable words" is FAIL.** The loader contract is a
closed key: `f0=0o1760`, `f1=0o5710`, `f2=0o4027`, `f3[5:0]=0`, plus the three verbatim body
descriptors. Any in-scope field combination either suppresses the load or hands control to a
non-terminating overlay loop at `0o707..0o711`; the rejecting tests are `vzm 674(12)` and
`vzm 712(3)` (§4). No larger copy can be constructed from these descriptors.

BLOCKED: no descriptor set produces more than 58 clean words; all tested combinations (over 100) either suppress the load or hang in the loader loop at 0o707..0o711 (rejecting vzm 674(12)/vzm 712(3)), proven by CORE/MTR/A-B in §§4-8.
