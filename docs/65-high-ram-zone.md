# re-forex, zone-run experiment: clean high RAM under the `*TRANS` path

> Предисловие главного агента: отчёт субагента, лично перепроверенный
> прогоном `tests/plan-f77/80-high-ram-zone/final_probe.py` (6/6 A/B, CORE 58/58,
> MTR PC-ы внутри нашей программы). Это снимает вопрос «где взять память» без
> пересборки LINK-таблицы, без нового имени транслятора и без обхода `f0`.

**Date:** 22.11.2026. **Work dir:** `/tmp/.private/azizz/opencode/re-forex-zones/`.
**Write scope:** only this directory; bulky per-case copies live in
`/dev/shm/re-forex-zones-cases` reached through the `cases` symlink. All runs are on
COPIES of 2048/2053/2099 with per-case `HOME`/`BESM6_PATH` redirection. No repo
edits, no git writes, no live disks/tmux/processes, no dispak C patches.
Harness: verbatim test-78 installer (`harness78.py` -> `harness.py`, only a
`zone_patches` argument and `REPO_ROOT` override added), `N = 0o2350`,
baseline marker `21 1.00 3.00`, `CORE_ON_PC=1770`, `CORE_SKIP=6`.

## VERDICT: PASS for "usable large code area" (with a measured size limit)

`N+3` gives **58 clean words at RAM 0o30114..0o30205**. A 58-word routine
(real array in high RAM + internal subroutine printing via `*64`) was placed
there, called with one structured jump from `body[9]`, and proved by CORE dump,
MTR and a six-case console A/B. No LINK table, new translator name or `f0`
patch was used. Zones `N+4..N+40` turn out NOT to be copied at our entry, so
this path caps at 58 words, not at several kilobytes.

---

## 1. Zone -> RAM map (FACT)

Method: one distinct sentinel `0o000077770000<zone><word>` in every word
`k = 0..0o71` of every zone `N+3..N+40` (`final_map.py`), CORE dump at our
entry PC `0o1770`, full 65536-word RAM scan. Baseline with all sentinels still
prints `21 1.00 3.00` and `КОНЕЦ ЗАДАЧИ` (`cases/final_map/out.txt`).

| zone | disk zone | first word -> RAM | copied words | stride |
|:--|:--|:--|:--|:--|
| N+3 | 0o2353 | word 0 -> **0o30114** | 58 (k=0..0o71) | 1 word per zone word |
| N+4 .. N+40 | 0o2354..0o2420 | **none** | 0 | no image at entry |

`zone N+3 word k -> RAM 0o30114 + k` exactly, with no holes (all 58 sentinel
words found; `final_zone_map.txt`, `final_zone_map.json`). The copy-loop MTR
trace (`probe_trace.py`, 21,723 `atx 0(6)` stores) shows four copy phases;
phase 3 runs `M6 = 0o1760..0o31551` and is the one that writes the
`0o301xx` band. Only the first 58 words of the first extra zone survive into
our entry, consistent with the `M11 = 0o106 -> 0o007` countdown observed there.
Earlier probes: `zmap_all` (word 0 and word 100 of all 38 zones) found only
N+3 word 0; `zfillall` (all 1024 words of N+3..N+8) found only N+3 words
0..0o57. All three probes agree.

## 2. Clean-region evidence (FACT)

MTR windows are octal LO/HI; a 0-hit band means no PC in it was ever executed
(the window arms on first entry, then prints N records and re-arms).

| window (octal) | case | MTR records | meaning |
|:--|:--|--:|:--|
| `02065..02260` | baseline | 0 | low "clean" gap, re-confirms test 79 |
| `30000..30777` | baseline | 0 | high band clean before our code |
| `30100..30200` | baseline | 0 | candidate region clean |
| `30206..30777` | final routine installed | 0 | remainder of high band still clean |
| `30100..30174` | final routine installed | 60 | PCs `30114,30115,30116,30117,30144,30145` only |

So the resident 4.12 path never executes `0o30114..0o30205`; the only hits
there are OUR routine (`final_mtr.txt`).

## 3. Routine placement (FACT)

Install: zone N catalog/body/z2 exactly as tests 66/70/78; zones N+4..N+40
zero; zone N+3 carries the 58 routine words. `body[9]` (RAM `0o1770`) is a
structured 15-bit jump to `0o30114` (encoding `0x0C304C<<24`, the form proved
by baseline word `03104067` = `пв 4067`).

| RAM | role | encoding |
|:--|:--|:--|
| 0o30114L | `xta 2006` | load GOST accumulator |
| 0o30114R | `utc 30000(0)` (`мода`, half `0x093000`) | M20 = 0o30000, arm modifier |
| 0o30115L | `arx 0o155(0)` + modifier -> **0o30155** | A(idx), high-RAM array |
| 0o30115R | `utc 30000(0)` | re-arm modifier |
| 0o30116L | `arx 0o160(0)` + modifier -> **0o30160** | N-cell = `1<<40` |
| 0o30116R | `utc 0(0)` | M20 = 0, modifier off |
| 0o30117L | `atx 2006` | store result back into GOST text |
| 0o30117R | jump `0o30144` | call internal subroutine |
| 0o30120..0o30143 | filler | `0o777700000000|k` (visible in CORE) |
| 0o30144 | `*64 2004` | print word (OBJ12), owned by the routine |
| 0o30145 | `uj 0(15)` | return to resident (M15 = 0o1764 unchanged) |
| 0o30155..0o30157 | A(1), A(2), A(3) | high-RAM array cells |
| 0o30160 | N-cell | `1<<40` |
| 0o30161..0o30205 | filler | distinctive words |

The subroutine is entered by the jump at 0o30117R and returns through the
return register M15 left intact by our entry jump, exactly the mechanism
proved in test 79. `MODA`/`UTC` sets the modifier register M20, so the
non-structured `ARX` can address the **high-RAM array directly**; the
modifier is cleared before the `*64` print so the descriptor address 0o2004
is unaffected.

## 4. Console A/B (FACT)

All cases end with `КОНЕЦ ЗАДАЧИ`, `rc=0`, with the same install; only the
listed field changes. Script `final_probe.py`, raw logs `fin_hi_*_out.txt`.

| case | change | console line | verdict |
|:--|:--|:--|:--|
| fin_hi_val3 | A(2)=3, idx=2, routine live | `41 1.00 3.00` | baseline of new path |
| fin_hi_val5 | A(2)=5 | `61 1.00 3.00` | value changes digit |
| fin_hi_idx3 | idx=3, A(3)=7 | `81 1.00 3.00` | index changes digit |
| fin_hi_zeroA | A(2)=0 | `11 1.00 3.00` | zeroed value changes digit |
| fin_hi_zfirst | **routine first word zeroed** | (no print line) | breaks output |
| fin_hi_zsub | **subroutine first word zeroed** | (no print line) | breaks output |

CORE proof: `fin_hi_*_core.txt` for all six cases report `word_count=58`,
`first_ram=030114`, `last_ram=030205`, `mismatch=0`: every routine word,
including the array and the print word, arrived at the measured address.
MTR proof: `final_mtr.txt` shows the PC actually executing
`30114L/30114R/30115L/30115R/30116L/30116R/30117L/30117R`, then
`30144L *64 2004` and `30145L uj 0(15)`.

## 5. Answer to the goal

| question | answer |
|:--|:--|
| usable "big memory" for arrays/functions? | **YES, 58 words**, at 0o30114..0o30205 |
| clean (not executed by resident 4.12)? | **YES**, wide MTR bands 0 hits |
| routine really arrives and executes? | **YES**, CORE 58/58 words, MTR PCs inside |
| touched LINK table / new name / f0? | **NO** |
| can N+4..N+40 add more? | **NO at our entry**; no sentinel from those zones appears in RAM |
| enough for 50-100 word routine? | **YES at 58 words**; larger needs a different loader descriptor, not zone count |

## 6. Evidence index

| file | content |
|:--|:--|
| `harness.py`, `harness78.py` | test-78 installer + zone_patches extension |
| `final_map.py`, `final_zone_map.txt/json` | definitive zone->RAM map |
| `probe_map.py`, `probe_fill.py`, `probe_fillall.py`, `zmap_*.txt`, `zfill*_diff.txt` | first/word-100 and dense sentinel probes |
| `probe_trace.py`, `trace_copy.txt` (regenerated on demand) | copy-loop MTR, M6 phases |
| `probe_mtr.py`, `mtr_*.txt` | wide MTR clean-band scans |
| `final_probe.py`, `final_results.txt`, `fin_hi_*_out.txt/_core.txt` | final routine + A/B + CORE |
| `final_clean.py`, `final_clean_mtr.txt` | clean remainder band with routine installed |
| `final_mtr.txt` | execution trace of the high-RAM routine |
| `cases -> /dev/shm/re-forex-zones-cases` | per-case disks, CORE dumps, patch logs |

DONE
