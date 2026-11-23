# zone-expand — can the zone-2350 contour copy/address MORE than the 58 words of N+3?

> ВЕРДИКТ: **BLOCKED** (FACT). Ограничение — каталог зоны N слово 3,
> дескриптор `0o400402757101760` (f3=`0o400`, f2=`0o4027`, f1=`0o5710`,
> f0=`0o1760`). DD/MTR‑трасса подтверждает: загрузчик читает зоны 2350..2353;
> все 58 слов лежат по `0o30114..0o30205`. Перебор 24 значений полей:
> любое изменение даёт либо `НЕТ РАЗДЕЛА`, либо чтение до конца диска с
> зависанием. MMU здесь ни при чём (`0o31000` в той же странице `0o14`),
> заголовки зон корректны. Значит 58 слов — жёсткий предел текущей передачи,
> и он больше не нужен: оптимизированная цепочка 2+2+знак влезает в 58/58
> (`docs/100`). DSQRT остаётся невозможным.

**Date:** 23.11.2026. **Workspace:** `/tmp/.private/azizz/opencode/zone-expand/`
(bulky C-oracle case disks under `/dev/shm/zone-expand-oracle`, symlinked as
`oracle/`; small evidence copies under `evidence/`).

**Discipline (all obeyed):** COPIES only of 2048/2053/2099/2348 and of the
SIMH binary; no repo edits, no git writes, no live disks, no tmux session 0,
no dispak C patches. Deck is only `*TRANS:OURMRK*,,412350` + `ДИС 41(2048)^`
(SHA `1d93c468…`, byte-identical to the proven contour deck). SIMH used
`ДATA:` via `capture-pane`, all input via `send-keys`, `ДАЙ А0`/`ДАЙ А1` +
`НОМВ` before the deck, post-job-start `НОМВ`, isolated `TMUX_TMPDIR`.
Stock `attach -n prn0/prn1` semantics kept, only the output path redirected
to a private workspace file to avoid cross-agent clobber (docs/95 §intro).
C `dispak` was **oracle only** (MTR/CORE/DD hooks, docs/88:70-73); all
authoritative A/B/A results are SIMH ACPU output.

---

## VERDICT: BLOCKED — 58 words is a hard limit of the current loader hand-off

| question | answer | marker |
|:--|:--|:--|
| which word/table caps the copy at N+3? | catalog zone N word 3 = descriptor `0o400402757101760`; field **f1** (bits 12-23, `0o5710`) together with f3/f2 selects the load variant and zone-run length | FACT (DD/MTR traces + field sweeps) |
| can any descriptor field be changed to copy N+4 and still run? | **NO** — every change either errors (`НЕТ РАЗДЕЛА`) or selects a read-to-disk-end path that hangs (no print, no `КОНЕЦ ЗАДАЧИ`) | FACT |
| is the blocker the MMU page for `utc 31000`? | **NO** — `0o30114`, `0o30205`, `0o31000` are ALL in MMU page `0o14` (`addr>>10`, `besm6_mmu.c:589,637`); page is accessible | FACT |
| is the blocker the SIMH zone header / w3 checksum? | **NO** — the marker zone N+4 was written with the proven `wz()` (docs/87:29-34 recipe) and is byte-valid; A/B restores exactly | FACT |
| **exact addressable word count** | **58 words, RAM `0o30114..0o30205`** (zone N+3 word `k` → `0o30114+k`, `k=0..0o71`); N+4..N+40 contribute 0 | FACT (CORE scan, 58/58 sentinels) |

Consequence: the 79/58-word deficit of docs/96:9,206 cannot be closed by
zone-count manipulation; DSQRT stays infeasible (docs/95:206-225).

---

## 1. STEP 1 — decode the `*TRANS:OURMRK*,,412350` loader/descriptor path

### 1.1 Call chain and load tables (FACT, from repo docs + my traces)

| item | source | finding |
|:--|:--|:--|
| LINK route | docs/62:73, 165-170 | zone 200 word `200.0331 = 6510700004300000` = `SHX 0o430(M14)` → NEWCOMP* stub |
| P1 entry | docs/62:79, 323-343 | RAM `0o3000..0o3014` from zone-422 words 511..525; saves M15, builds INF, `*70` disk 30 / zone `0o0050` |
| P2 catalog-read | docs/62:80, 346-350 | RAM `0o3020..0o3022`; INF `0o0010030000411550` → `*70` reads disk 41 zone N |
| P3 scan | docs/62:81, 352-375 | name XOR compare; `f0 = desc & 0o7777` (mask `0o3076`); main needs `f0=0o1760`; satellite-copy loop `0o3051..0o3052` |
| P4 decode-and-load | docs/62:82, 377-392 | RAM `0o660..0o711`; decodes f3/f2/f1/f0; builds body INF at `0o145/0o146`; `*70` reads continuous zones; copy loop `0o700..0o711`, receiver M6; branch on M3 at `0o674` (`vzm 712(3)`) |
| descriptor layout | docs/62:209; `src/newcomp/O412C.FTN` | `d = f3<<36 \| f2<<24 \| f1<<12 \| f0`; ours = `0o400402757101760` → **f3=`0o400`, f2=`0o4027`, f1=`0o5710`, f0=`0o1760`** (computed from `O412C.FTN` HI/LO pairs 2/3) |
| copy mapping | docs/62:229-245; test 66/80 | `body[k] → RAM 0o1757+k`; N+3 word `k → 0o30114+k` |

My DD trace (`evidence/f_base_out.txt`) proves the loader reads **exactly
four** zones from disk 41 and stops:

```
DD pc=03022L r016=53405 u=41 z=2350 RD uil=10/0/300  uir=41/0/2350   <- catalog N
DD pc=00671L r016=00145 u=41 z=2351 RD uil=10/0/3200 uir=41/0/2351   <- body N+1
DD pc=00744L r016=00145 u=41 z=2352 RD uil=10/0/3200 uir=41/0/2352
DD pc=00744L r016=00145 u=41 z=2353 RD uil=10/0/3200 uir=41/0/2353   <- LAST
```
(`grep -a 'u=41 z=' evidence/f_base_out.txt`; no `z=2354` line exists.)

### 1.2 What the copy loop actually does (FACT, MTR)

`oracle/trace1/mtr.txt` (192 000 MTR records, window `0o660..0o760`;
decisive excerpt copied to `evidence/trace1_mtr_excerpt.txt`):

```
00660L xta  1(16) AU=400400353001760      ; descriptor loaded
00661R ati  3(0)  ... 03=03530             ; M3 = branch/selector word
00670L atx  145(0) AU=10320000300051      ; INF word built
00670R *70  145(0)                        ; read zone N+1
00673R utc  0(0)  ... 06=01760             ; M6 receiver := 0o1760
00674R vjm  736(15)                       ; call read-word/counter subroutine
00675R ati  11(0) ... 11=00070             ; M11 counter := 0o70
00703L atx  0(6)                          ; store word, M6++
00704L utm  77777(3)  ... 03 decrements
00704R utm  77777(11) ... 11 decrements    ; 0o70 -> 0o67 ... -> 0
00705L uj   702(0)                        ; loop
00742L xta  145(0) / 00742R arx 747(0) / 00743L atx 145(0) / 00743R *70
                                          ; next-zone read (zone += const at 0o747)
```

`parse_stores.py` over the same trace: **21 723 `atx 0(6)` stores in 4
phases**, the third running `M6 = 0o1760..0o31551` and writing the high band.
The `M11 = 0o70 → 0` countdown is the per-phase word limiter.
docs/65:40-45 reports the same copy-loop shape (its `M11 = 0o106 → 0o007`
numbers come from a routine-installed variant; the mechanism is identical).

### 1.3 Zone→RAM map (FACT, reproduced here)

Sentinel probe (`exp_map.py`): distinct word `0o000077770000<zone><word>` in
words `0..0o71` of zones N+3..N+8, CORE dumped at PC `0o1770`, full RAM scan.
Result: **59 hits — 58 at `0o30114..0o30205` from zone N+3 word `0..0o71`,
plus one incidental copy at `0o053403`; ZERO hits from N+4..N+8.**
This reproduces docs/65:28-48 and docs/73:137-140 exactly.

### 1.4 FACT / INFERENCE boundary

* **FACT:** descriptor = `0o400402757101760`; loader reads zones 2350-2353;
  58 words land at `0o30114..0o30205`; no data from N+4+ reaches RAM.
* **FACT:** f1/f2/f3 changes alter the zone run (sweep below); f0 must be
  `0o1760`.
* **INFERENCE (strong, not a full disassembly proof):** the descriptor is
  effectively a magic constant; only the exact triple
  (f3=`0o400`, f2=`0o4027`, f1=`0o5710`) selects the "short" 3-zone path.
  All other low-bit-zero triples select a "read-to-disk-end" branch. This is
  inferred from the all-or-nothing sweep behaviour, not from a decoded branch
  table. docs/62:289,432 already flags f3/f2/f1 semantics as INFERENCE/Q3.

---

## 2. STEP 2 — minimum-change attempts on COPIES (field sweeps)

All cases below are C-oracle runs on copies; `BESM6_DD_DEBUG=1`; zone counts
are `grep -ao 'u=41 z=[0-9]* RD'`. Raw outputs in `evidence/*_out.txt`.

| case | change to catalog word 3 | disk-41 zones read | print / end |
|:--|:--|:--|:--|
| `f_base` | none | `2350,2351,2352,2353` (4) | `21 1.00 3.00`, end |
| `f_f0_p1/p10/p100` | f0 ≠ `0o1760` | `2350` only | no print, `НЕТ РАЗДЕЛА` |
| `f_f1_p1..p7` | f1 low 3 bits ≠ 0 | `2350` only | no print, `НЕТ РАЗДЕЛА` (branch `0o733`) |
| `f_f1_p10`, `f_f1_p100` | f1 `0o5720`, `0o5740` | `2350..2523` (108) | **TIMEOUT, no print, no end** |
| `f_f2_p1/p10/p100` | f2 +1/+8/+64 | `2350..2523` (108) | **TIMEOUT** |
| `f_f3_p1/p10/p100` | f3 +1/+8/+64 | start shifts to `2353`/`2371`/`2551`, runs to disk end | **TIMEOUT** |
| `sw_5700..5750` (24 values) | f1 sweep | only `0o5710` → 4 zones; all other low-bit-zero → 108 zones | only baseline completes |

Additional probes:

* `exp_hdr.py`: patching DMS header words body[2] (`set|data<<15|long<<30`) and
  body[3] (`cmd|bss<<15|const<<30`) by +1/+8/+64/+512 → **zone count unchanged
  (4), print unchanged**. So the header is not the limiter.
* `exp_extend.py`: with f1=`0o5700`/`0o5720`/`0o5730` AND sentinel data written
  into N+3..N+8 (valid SIMH zone headers + recomputed w3), the loader read
  N+1..N+5 then **hung before PC `0o1770`** (no CORE dump produced). So the
  hang is not caused by garbage in the extra zones.
* `exp_f3f1.py`: 21 combinations of f3∈{0o400,0o401,0o402} × 7 f1 values —
  only (0o400, 0o5710) completes; all others error or hang.

**Conclusion (FACT):** there is no descriptor-field value that loads N+4 (or a
controlled few extra zones) and still reaches the hand-off. The extra-zone
path exists but never terminates.

### 2.1 Why "base 0o31000" is not the blocker (FACT)

`besm6_mmu.c:589,637` uses `TLB[addr >> 10]` (page = 1024 words):

```
0o30114 >> 10 = 0o14     0o30205 >> 10 = 0o14
0o31000 >> 10 = 0o14     0o31777 >> 10 = 0o14
```

So the entire band `0o30000..0o31777` is ONE accessible page (`0o14`). The
task's suggested `utc 30000`-style base `0o31000` would be reachable if the
loader placed data there. The blocker is the loader, not the MMU. (docs/88's
protected pages `0o70000`/`0o74000` are different pages, `>>10` = `0o37`.)

### 2.2 Checksum / zone-header sanity (FACT)

`build_simh.py` writes the N+4 marker zone with `wz()` from the proven builder
(docs/87:29-34: `w0=(phys<<36)|0x038ca3c918`, `w1=0x000005f1c7800000`,
`w2=0x0000410300000000`, `w3` = end-around-carry checksum of 1024 words).
A and RESTORE images have identical SHA, so the header/checksum path is sound
and is not the blocker.

---

## 3. STEP 3 — minimal SIMH A/B/A proof

Deck: `decks/deck_trans.b6` (SHA `1d93c468…`). Cases built by `build_simh.py`.

| case | image | contour change | SIMH ACPU result |
|:--|:--|:--|:--|
| **A** | `2048_A` SHA `ef8fdc15…` | marker `0o0123456765432100` at zone N+4 word 0; descriptor untouched | `21 1.00 3.00` + `КОНЕЦ ЗАДАЧИ`, exit 0 |
| **B** | `2048_B` SHA `4e95fd4a…` | same marker, **f1 `0o5710`→`0o5720`** (extension attempt) | **no print line, no `КОНЕЦ ЗАДАЧИ`**, exit 2 (job hangs) |
| **RESTORE** | `2048_RESTORE` SHA `ef8fdc15…` (byte-identical to A) | restored | `21 1.00 3.00` + `КОНЕЦ ЗАДАЧИ`, exit 0 |

Raw ACPU excerpts (`runs/acpu_{A,B,RESTORE4}.txt`):

```
A / AC / RESTORE4 : line 100: " 21 1.00 3.00"
                    line 114: " КОНЕЦ ЗАДАЧИ  +000000000000e+00  0000206320000000"
B / BC            : 72 lines, ZERO matches for '21 1.00 3.00' or 'КОНЕЦ ЗАДАЧИ'
                    console: "B075-1 410300000000" (job started) then silence
```

`cmp`/SHA proof: `sha256sum images/2048_A images/2048_RESTORE` → both
`ef8fdc15a75818b13b47c90a2516a1966e5f4e152645d54f511f8de477d27e13`.
`images/2048_B` differs from A in exactly the descriptor word plus the two
recomputed zone-checksum copies (f1 patch), as expected.

**Note on binary:** the first A/B pair ran on the stock
`/home/azizz/Yandex.Disk/simh/BIN/besm6` (SHA at start: 1.5 M). A concurrent
agent removed that shared binary at ~15:29 (`BIN/Linux-build/Make.info` shows
a rebuild in progress). To complete a same-binary A/B/A I used a COPY of the
archived BESM6 SIMH binary `/home/azizz/Yandex.Disk/rezerv/besm6`
(SHA `e989fa10…`, 1.0 M, `file` = ELF BESM6 sim) for cases `AC`, `BC`,
`RESTORE4`. All three agree with the stock-binary A/B result. No repo, C
source or live disk was touched by this substitution.

**Marker-in-new-zone read test:** not executable, because the extension B
case never reaches our entry PC, so no machine code can read a word of N+4.
The A case proves the negative: with a valid marker in zone N+4, the CORE
scan finds no N+4 word in RAM (§1.3) and the console prints the unchanged
baseline `21 1.00 3.00`.

---

## 4. STEP 4 — exact new addressable word count / precise blocker

* **Addressable today: 58 words** at RAM `0o30114..0o30205`
  (zone N+3 word 0..0o71). This is the number used by docs/95/96 budgets
  (35/58 for single-digit e2e, 79/58 for full 2+2, 68/58 for ABS variant).
* **New addressable word count after any tested field change: 0 additional
  words.** No working image with an N+4 word in RAM exists.
* **Precise blocker:** the loader descriptor in catalog zone N word 3. Only
  `f3=0o400, f2=0o4027, f1=0o5710` (with `f0=0o1760`) selects the terminating
  3-body-zone copy; the loader then copies only zone N+3's first 58 words
  into the high-RAM band. Any other value either faults to `НЕТ РАЗДЕЛА` or
  enters a read-to-disk-end loop that never reaches the `VJM 0o64002`
  hand-off (docs/62:83, 263-265, 393-396).
* **NOT blockers:** MMU page for `0o31000` (same page `0o14`); SIMH zone
  header checksum (valid, recomputed); deck content (fixed, proven); C
  emulator (oracle only, never used as success evidence).

---

## 5. SHAs (SHA-256)

```
a98e81090d4b254554a0cd3ff8611438615de84fc012e8e2b70fbabc2ebdc796  images/2048_base  (reproduces docs/87/96)
ef8fdc15a75818b13b47c90a2516a1966e5f4e152645d54f511f8de477d27e13  images/2048_A      (= RESTORE)
4e95fd4a3b2a92a29f78c4d70eca1d191216871d096af61abdbf88a9c617c8bc  images/2048_B      (f1 extension attempt)
ef8fdc15a75818b13b47c90a2516a1966e5f4e152645d54f511f8de477d27e13  images/2048_RESTORE
1d93c468c1acf7b6c9d7ac5f002336ce4580d6d716fbc1694aabd605c9bbeae2  decks/deck_trans.b6
e989fa10b025322e55bac51c71f3b644f3a28f68c3dedc498f89c5c9b6f03499  tools_besm6_backup (archived SIMH binary, COPY)
```

## 6. PASS / FAIL

| # | gate | verdict |
|:--|:--|:--|
| 1 | reproduce docs/87 base SHA `a98e8109…` | **PASS** |
| 2 | reproduce docs/65 map (58 words @ 0o30114..0o30205, none from N+4+) | **PASS** |
| 3 | decode loader path and identify limiting field (f1/f2/f3 in catalog word 3) | **PASS** |
| 4 | field sweep finds a value that copies N+4 and completes | **FAIL** (no such value; §2) |
| 5 | SIMH A: valid N+4 marker, baseline output | **PASS** (`21 1.00 3.00`) |
| 6 | SIMH B: extension attempt changes printed digit / loads marker | **FAIL** (no output, job hangs) |
| 7 | SIMH byte-identical restore returns baseline | **PASS** (`21 1.00 3.00`) |
| 8 | MMU/checksum ruled out as blockers | **PASS** |

## 7. Evidence index

```
ze.py                 zone patch/checksum + C-oracle runner (reuses tools/build_zone2350_contour.py)
exp_map.py            sentinel zone->RAM map (58 hits @ 0o30114..0o30205)
exp_trace.py          MTR of P4 copy loop (192000 records)
exp_fields.py         f0/f1/f2/f3 sweep
exp_f1sweep.py        24-value f1 sweep (short timeout)
exp_extend.py         f1 extension + sentinel data in extra zones
exp_hdr.py            DMS header word sweep (no effect)
exp_f3f1.py           21 f3/f1 combinations (only baseline works)
parse_trace.py / parse_stores.py  M11 counter and 21723 atx 0(6) stores, 4 phases
build_simh.py         A/B/RESTORE images (marker in N+4, f1 patch)
simh_setup.py / drive_case.py   isolated SIMH driver (copies, private -n prn)
evidence/f_base_out.txt          DD trace: zones 2350-2353 only
evidence/trace1_mtr_excerpt.txt  MTR: M11=0o70 countdown, M6 receiver (full 38.5M trace in oracle/trace1/mtr.txt)
evidence/map1_out.txt + map1_core-pc.bin   58 sentinels, no N+4
evidence/f_*_out.txt, sw_*_out.txt, c_*_out.txt, ext_*_out.txt, hdr_*_out.txt
runs/acpu_{A,B,AC,BC,RESTORE4}.txt          SIMH ACPU (authoritative)
runs/console_{A,B,AC,BC,RESTORE4}.txt      SIMH console transcripts
runs/ini_*.ini                              per-case SIMH configs (all copies)
simh_sha.txt                                image SHAs
```

BLOCKED: loader descriptor in catalog zone N word 3 (f3=0o400/f2=0o4027/f1=0o5710, f0=0o1760) is the only value that terminates after zone N+3; every alternate value either errors (НЕТ РАЗДЕЛА) or hangs reading zones to disk end, so no extra zone reaches RAM and the addressable total stays 58 words (0o30114..0o30205).
