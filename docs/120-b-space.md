# B-SPACE: is the zone-2350 body N+1 area a usable code/data reservoir for variant B?

> РЕЗУЛЬТАТ b‑space: **PASS** — зона N+1 (body) содержит 999/1024 слов,
> переживающих побайтовый zero‑A/B; 25 слов load‑bearing. Пять крупных
> свободных диапазонов дают 909 слов (больше, чем 649 в N+2). Все body‑адреса
> ≤ `0o21636` < `0o7777` — direct 12‑битный ADR, без модификатора.
> Исполняемость доказана трамплинами и 8‑словными цепочками.
> Оговорка FACT: обнулить все 999 сразу FAIL; если сохранить одно из 12
> «keeper» слов (например `body[0o26]`), 998 слов перезаписываются сразу.
> Это снимает проблему бюджета для machine‑парсера Fortran.

**Verdict: YES, with one aggregate caveat.** 999 of the 1024 body words survive an
independent zero-A/B (25 load-bearing exceptions). The body RAM lives entirely
below the N+2 base and is reachable by 12-bit ADR. Trampoline and 8-word code-chain
experiments prove that free words can hold and execute real code. Caveat: zeroing
*all* 999 simultaneously FAILS — see §8; preserving any one of 12 specific words
(e.g. `body[0o26]`) while overwriting the other 998 PASSES.

**Discipline (FACT):** workspace `/tmp/.private/azizz/opencode/b-space/` only.
All runs are on copies. No repository file, live disk, tmux session 0, SIMH binary,
or C `dispak` source was modified. The C `dispak` binary was used **as an oracle
only** (`/home/azizz/Yandex.Disk/dispak/build/dispak/dispak`), with
`BESM6_DD_DEBUG=1`, `BESM6_CORE_ON_PC=01770`, `BESM6_CORE_SKIP=6`, and
`BESM6_MTR_LO/HI/N/SKIP` for traces. No SIMH gate was used as success evidence.

---

## 0. Artifacts and SHAs (FACT)

```
b3ede98828cd42ccbfe866a0c371f31a07e512d9f45a4b2cc0e11334014a525c  images/2048_base_C7_A   (= canonical C7 image A)
b6e4488aff18a3c6707a18c460036d79c4d29b696b42752cb0c1afb415d05a88  decks/deck_c7_A.b6      (= canonical C7 deck A)
dc60fcdc3032e5574abe819cc9fabbc80a263a20f7a46bbc84d311c075e141b0  cases/baseline/core-pc.bin
9b91f4f5841de9e2399d794b9b2ee5daae67a2ea3e8a5eb4815f955641fba7e7  cases/final_stats.txt
0cd2de6a6e2e06508177b16861d810e7d95eb37822d57e3dcf13029d90b7f6ed  cases/wordprobe.txt
4ec984c79ed513e0d6d2a394f5fcdb3a80cd0d524efe207793067ff633a8de99  cases/fine_sweep.txt
```
Script SHAs are in `cases/sha256.txt`. Image/deck SHAs match docs/116 §6 exactly.

## 1. Baseline (FACT)

`build/oracle.py baseline images/2048_base_C7_A decks/deck_c7_A.b6`:

```
CASE=baseline rc=0 bytes=60477 done=True
vals=['-0012.34', '-0056.78', '-0003.75', '-0000.40', '-0034.50', '-0040.00'] PASS=True
```

Canonical output defined for every A/B below = all six values **and**
`КОНЕЦ ЗАДАЧИ`. Each probe is a fresh copy of `2048_base_C7_A`; only body N+1
words in the probed index set are changed; `build_zone2350_contour.wz` semantics
(`build_e2e.wz`) recompute the zone checksum.

## 2. Method (FACT)

1. Coarse sweep: sixteen 64-word blocks covering body[0..0o1777].
2. Fine sweep: 8-word blocks inside every FAIL coarse block.
3. Word probe: single words inside every FAIL 8-word block (104 words).
4. Positive executability: trampolines through free words in all RAM segments;
   three 8-word contiguous LONG-UJ chains.
5. CORE verification: `build/core.py` reads `core-pc.bin` as 65536 words × 6 bytes
   **MSB-first** (docs/114 §1.1); `build/mapcore.py` checks each body word at its
   measured RAM address.
6. MTR: narrow PC windows so each run completes with canonical output.

PASS/FAIL per probed range is in `cases/coarse_sweep.txt`, `cases/fine_sweep.txt`,
`cases/wordprobe.txt`, `cases/interaction.txt`, `cases/narrow_interact.txt`.

## 3. Raw A/B results — coarse (FACT)

`PASS` = canonical six values + `КОНЕЦ ЗАДАЧИ`; `FAIL` = crash/timeout or missing/altered values.

| body range zeroed | rc | values | verdict |
|:--|--:|:--|:--|
| `[0..0o100)` | -9 | none | **FAIL** |
| `[0o100..0o200)` | 0 | none (job ends, no print) | **FAIL** |
| `[0o200..0o300)` | -9 | none | **FAIL** |
| `[0o300..0o400)` | 0 | all six | **PASS** |
| `[0o400..0o500)` | 0 | all six | **PASS** |
| `[0o500..0o600)` | 0 | all six | **PASS** |
| `[0o600..0o700)` | -9 | none | **FAIL** |
| `[0o700..0o1000)` | 0 | all six | **PASS** |
| `[0o1000..0o1100)` | 0 | all six | **PASS** |
| `[0o1100..0o1200)` | 0 | all six | **PASS** |
| `[0o1200..0o1300)` | -9 | none | **FAIL** |
| `[0o1300..0o1400)` | 0 | all six | **PASS** |
| `[0o1400..0o1500)` | 0 | all six | **PASS** |
| `[0o1500..0o1600)` | 0 | all six | **PASS** |
| `[0o1600..0o1700)` | -9 | none | **FAIL** |
| `[0o1700..0o1777)` | 0 | all six | **PASS** |

Fine and single-word results narrow every FAIL block to the 25 words in §5.
Examples of the decisive single-word lines (raw, octal indices):

```
w0|range=[0,1)|zeroed=1|rc=0|done=False|vals=|FAIL
w25|range=[25,26)|zeroed=1|rc=0|done=True|vals=|FAIL
w44|range=[44,45)|zeroed=1|rc=-9|done=False|vals=|FAIL
w131|range=[131,132)|zeroed=1|rc=0|done=True|vals=-0012.33,-0056.77,-0003.75,-0000.40,-0034.50,-0040.00|FAIL
w144|range=[144,145)|zeroed=1|rc=0|done=True|vals=0012.34,0056.78,0003.75,0000.40,0034.50,0040.00|FAIL
w223|range=[223,224)|zeroed=1|rc=-9|done=False|vals=|FAIL
w603|range=[603,604)|zeroed=1|rc=-9|done=False|vals=|FAIL
w1236|range=[1236,1237)|zeroed=1|rc=0|done=False|vals=|FAIL
w1616|range=[1616,1617)|zeroed=1|rc=-9|done=False|vals=|FAIL
w1627|range=[1627,1630)|zeroed=1|rc=-9|done=False|vals=|FAIL
```

`w44` reproduces the known "zeroing body 36 (decimal) = 0o44 causes TIMEOUT".
`w131`/`w135`/`w137` change the last digit; `w144`/`w145` drop the sign.
`w11` FAILs when zeroed, but C7 already proved it is *replaceable* by a valid
`long uj 0o22147` (MTR in §7) — so "load-bearing under zero" is not the same as
"unusable".

## 4. Body → RAM map, CORE evidence (FACT)

`build/mapcore.py baseline`:

```
S1 body[1..43]     -> RAM[1760..2022] match=34/35 firstbad=4
S2 body[46..222]   -> RAM[2041..2215] match=109/109 firstbad=None
S3 body[224..602]  -> RAM[2223..2601] match=239/239 firstbad=None
S4 body[604..1235] -> RAM[2621..3252] match=282/282 firstbad=None
S5 body[1237..1615]-> RAM[21066..21444] match=239/239 firstbad=None
S6 body[1617..1626]-> RAM[21452..21461] match=8/8 firstbad=None
S7 body[1630..1777]-> RAM[21467..21636] match=103/104 firstbad=1630
descriptors (not copied): 44 223 603 1236 1616 1627
max body RAM: 0o21636   N+2 base: 0o21637   ADR ceiling: 0o7777
```

This **extends docs/64 §2** (which documented descriptors at `0o44/0o223/0o603`
only) with three more section descriptors found here: `body[0o1236]`,
`body[0o1616]`, `body[0o1627]`. `body[0]` is not copied; `body[4]` is patched by
the loader; `body[0o1630]` is skipped by the loader. `body[0o45]` is replicated at
`0o2216,2217,2220,2221,2222` (docs/64). Raw CORE words:

```
body[0011]=0302214700000000 -> RAM ['0o1770']  (our long UJ entry)
body[0025]=0000200600002006 -> RAM ['0o2004']
body[0046]=7044000664440007 -> RAM ['0o2041']
body[1235]=0000000050154240 -> RAM ['0o3252']
body[1600]=4041600014300453 -> RAM ['0o21427']
body[1777]=6010002763076742 -> RAM ['0o21636']
```

FACT: the zeroed value appears verbatim at the expected RAM address, e.g. for a
PASS case `sw_0o300_0o400`, RAM `0o2277..0o2374` differs from baseline in 62
words and those words read `0000000000000000`. So the disk edit really reaches RAM.

## 5. Load-bearing words (FACT for zero-A/B; INFERENCE for role)

25 words fail when zeroed alone:

```
body[0000] dec=0    not copied                (service word 0o1600043, docs/64)
body[0010] dec=8    RAM 0o1767                (resident code)
body[0011] dec=9    RAM 0o1770                (our contour entry, replaceable by code)
body[0025] dec=21   RAM 0o2004                (resident code)
body[0044] dec=36   DESCRIPTOR (not copied)
body[0112..0117] dec=74..79 RAM 0o2105..0o2112   (our C2 data cells)
body[0120] dec=80   RAM 0o2113                (our data cell)
body[0121] dec=81   RAM 0o2114                (our data cell)
body[0123] dec=83   RAM 0o2116                (our data cell)
body[0131] dec=89   RAM 0o2124                (sign/rounding cell)
body[0133] dec=91   RAM 0o2126                (sign/rounding cell)
body[0135] dec=93   RAM 0o2130                (sign/rounding cell)
body[0137] dec=95   RAM 0o2132                (sign/rounding cell)
body[0144] dec=100  RAM 0o2137                (sign control; print loses '-')
body[0145] dec=101  RAM 0o2140                (sign control; print loses '-')
body[0223] dec=147  DESCRIPTOR (not copied)
body[0603] dec=387  DESCRIPTOR (not copied)
body[1236] dec=670  DESCRIPTOR (not copied)
body[1616] dec=910  DESCRIPTOR (not copied)
body[1627] dec=919  DESCRIPTOR (not copied)
```

INFERENCE: the six descriptor words and the service word must be preserved
verbatim; the 15 `body[0o112..0o145]` words are *our* C7 setup cells
(`c7_build.py` writes `vals()` there) and are relocatable rather than structurally
fixed; `body[0o10]`, `body[0o25]` are resident 4.12 words that are genuinely
executed (MTR in §7).

## 6. Exact safe ranges and total (FACT: single-word A/B; INFERENCE: simultaneous use)

Maximal contiguous FREE ranges, in octal body indices (inclusive):

| range | count | decimal | RAM range |
|:--|--:|:--|:--|
| `body[0001..0007]` | 7 | 1..7 | `0o1760..0o1766` |
| `body[0012..0024]` | 11 | 10..20 | `0o1771..0o2003` |
| `body[0026..0043]` | 14 | 22..35 | `0o2005..0o2022` |
| `body[0045..0111]` | 37 | 37..73 | `0o2216..0o2104` |
| `body[0122..0122]` | 1 | 82 | `0o2115` |
| `body[0124..0130]` | 5 | 84..88 | `0o2117..0o2123` |
| `body[0132..0132]` | 1 | 90 | `0o2125` |
| `body[0134..0134]` | 1 | 92 | `0o2127` |
| `body[0136..0136]` | 1 | 94 | `0o2131` |
| `body[0140..0143]` | 4 | 96..99 | `0o2133..0o2136` |
| `body[0146..0222]` | 45 | 102..146 | `0o2141..0o2215` |
| `body[0224..0602]` | 239 | 148..386 | `0o2223..0o2601` |
| `body[0604..1235]` | 282 | 388..669 | `0o2621..0o3252` |
| `body[1237..1615]` | 239 | 671..909 | `0o21066..0o21444` |
| `body[1617..1626]` | 8 | 911..918 | `0o21452..0o21461` |
| `body[1630..1777]` | 104 | 920..1023 | `0o21467..0o21636` |

**TOTAL SINGLE-WORD FREE = 999 / 1024.** The five largest contiguous ranges
(282, 239, 239, 104, 45 words) already total 909 words — more than the 649-word
N+2 budget, so a full source parser fits in body alone.

## 7. Executability proof (FACT)

`build/trampoline.py` replaces `body[0o11]` with `long uj RAM(free_word)` and puts
`long uj 0o22147` (the real N+2 code) in the free word:

```
tramp_c300|free_idx=300|RAM=2277|rc=0|done=True|vals=all six|PASS
tramp_c604|free_idx=604|RAM=2621|rc=0|done=True|vals=all six|PASS
tramp_c1600|free_idx=1600|RAM=21427|rc=0|done=True|vals=all six|PASS
tramp_c1640|free_idx=1640|RAM=21477|rc=0|done=True|vals=all six|PASS
tramp_c1770|free_idx=1770|RAM=21627|rc=0|done=True|vals=all six|PASS
```

`build/chain.py` builds an 8-word contiguous LONG-UJ chain through free words:

```
chain8_s1|chain=body[300..307] n=8|RAMs=['2277','2300','2301','2302','2303','2304','2305','2306']|PASS
chain8_s5|chain=body[1300..1307] n=8|RAMs=['21127','21130','21131','21132','21133','21134','21135','21136']|PASS
chain8_s7|chain=body[1700..1707] n=8|RAMs=['21537','21540','21541','21542','21543','21544','21545','21546']|PASS
```

MTR raw traces (C oracle, narrow windows, all cases rc=0, canonical output):

```
# mtr_entry_skip6: BESM6_MTR_LO=01770,HI=01770,N=20,SKIP=6
MTR 01770L uj     22147(0) AU=0000000001146 ... R16=01760 R17=53401
MTR 22147L xta    2105(0)  AU=0000000001146 ...
MTR 22147R ati    14(0)    AU=0000000020000 ...

# mtr_load2004: body[0o25] RAM 0o2004 is genuinely executed
MTR 02004L vtm    2034(1) ...
MTR 02004R xta    2251(0) ...
MTR 02005L aox    2252(0) ...

# mtr_free2277 (body[0o300], a FREE word) and mtr_free21427 (body[0o1600]):
grep -ac '^MTR ' out.txt  ->  0      (never PC, never operand)
# mtr_n2: BESM6_MTR_LO=022147,HI=022150,N=80
MTR 22147L xta 2105(0) / 22147R ati 14(0) / 22150L xta 2015(14) ...
```

FACT: a load-bearing body word is executed; free-word RAM addresses are not
touched as PC or operand in the canonical run; our code enters through
`body[0o11]` and the trampolines prove a free word can be an executable waypoint.
INFERENCE: a full contiguous free range can host arbitrary code, demonstrated for
8-word chains but not for a 282-word program.

## 8. AGGREGATE CAVEAT (FACT)

`build/zeroallfree.py` (zero all 999 free words, keep the 25 load-bearing):

```
zero_all_999_free|zeroed=999 kept=25|rc=-11|done=False|vals=-0012.34|FAIL
```

Deterministic across 3 repeats. Filling all 999 with other constants also FAILS
(`fill_26val` rc=-9 no values; `fill_ntr15` and `fill_ones` rc=0, no values).
Therefore the per-word/per-block PASS results must not be read as "all 999 can be
overwritten at once".

However, `build/interact.py` and `build/narrow_interact.py` show the failure is
avoidable with a single preserved word. Keeping `body[0o26]` at its baseline value
and zeroing the other 998 free words:

```
keep+body[0026] zero 998: PASS vals=['-0012.34', '-0056.78', '-0003.75', ...]
```

12 words individually suffice when kept: `0o26, 0o34, 0o46, 0o47, 0o50, 0o57,
0o61, 0o65, 0o66, 0o67, 0o72, 0o73`. Keeping other single free words does not.
INFERENCE: this is an aggregate/global effect (resident-code state or emulator
instruction-cache interaction across the heavily overlaid low-RAM region), not a
new load-bearing word; at least **998 words are simultaneously overwritable**.
The trampoline/chain results (real code, not zero fill) all PASS, so the caveat
may not apply to genuine parser code, but that was not proven for a full program.

## 9. Reachability by 12-bit ADR (FACT)

* Naive maximum: `0o1757 + 1023 = 0o3756 <= 0o7777`.
* Measured maximum: body[0o1777] -> RAM `0o21636 <= 0o7777`, and it ends exactly
  one word below the N+2 base `0o21637` (docs/116).
* Body RAM is **directly addressable by SHORT (12-bit) ADR** without a UTC base
  modifier; no HIGH-RAM trick is needed. A `long uj` can also reach any of them.
* All seven segments are below 0o7777, so variant B can use body words as code
  or data with ordinary short addressing.

## 10. FACT vs INFERENCE summary

FACT: baseline and all A/B SHAs; CORE dump and piecewise body→RAM map; 25 words
that fail one-word zero; 16 exact free ranges totalling 999; six descriptors;
trampoline and 8-word chain PASS; MTR lines; 12-bit reachability; all-999-zero FAIL
and the `body[0o26]`-kept 998-word PASS.

INFERENCE: roles assigned to the 25 words; that the 12-word aggregate effect is a
global interaction rather than hidden load-bearing semantics; that an arbitrary
contiguous 282-word range can host a full parser (only 8-word chains were
executed); that SIMH would reproduce the C-oracle A/B (no SIMH gate was run here).

## 11. Limits

* Only the C oracle was used (per task); SIMH A/B was not re-run.
* Zero is a conservative replacement: `body[0o11]` shows a word can be unusable
  under zero yet usable under valid code. Conversely, the all-zero aggregate FAIL
  shows zero is not always representative.
* The 25 load-bearing words include 15 of C7's own data cells; a real variant B
  would relocate those cells and could reclaim them, which would raise the usable
  count above 999 but was not tested.
* No repository/live-disk/tmux/C-source change was made.

## 12. Reproduce

```
cd /tmp/.private/azizz/opencode/b-space
python3 build/oracle.py baseline images/2048_base_C7_A decks/deck_c7_A.b6
python3 build/sweep.py 0:0o100 ...            # cases/coarse_sweep.txt
python3 build/wordprobe.py 0:0o30 ...         # cases/wordprobe.txt
python3 build/final_stats.py                  # cases/final_stats.txt
python3 build/trampoline.py t 0o300
python3 build/chain.py c 0o300 8
python3 build/zeroallfree.py
python3 build/narrow_interact.py 0o26:0o26
```

DONE
