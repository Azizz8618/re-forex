# Phase 4 PREPARATION — design: integrate our Fortran front end / codegen / emitters into the proven `*TRANS` install path

> Предисловие главного агента. Документ — проектное задание фазы 4, созданное
> субагентом 22.11.2026. М0 (воспроизведение тестов 66/67/68) уже выполнено:
> все три теста дают VERDICT=PASS, так что риск R1 снят для конфигурации этих
> тестов; вычисляемый вывод (R2/M4) разрабатывается отдельным субагентом фазы 3.
> Первый независимый шаг после этого документа — M2 (подключение вывода O412D
> вместо живого root-хвоста тела 19..1023).

**Status:** design only. No repo edits, no git writes, no dispak C patches, no live disks/tmux/processes. All reads were of repository files and the two design documents listed in the task; all numerical claims below are traced to those files. Writes confined to `/tmp/.private/azizz/opencode/re-forex-phase4-design/`.

**Date:** 22.11.2026. **Owner:** phase-4 preparation subagent. **Concurrency:** phase 3 ("runtime computed output") runs in a separate session; this report deliberately does not solve that problem and marks every dependency on it explicitly in §5 and §6.

---

## 0. Ground truth and the one correction that matters

Before the design, the conflicting evidence must be stated honestly, because it decides the milestone order.

| claim | source | status |
|:--|:--|:--|
| `*TRANS` copies zone `N+1` to RAM with `body[k] → 0o1757+k`; `body[9] → 0o1770`, `body[0o25] → 0o2004`, `body[0o27] → 0o2006` | `docs/62-newcomp-re.md` §3.3, test 66 | **FACT** |
| Test 66: our rebuilt `SETTRAN*` words at those offsets print the static GOST marker; zeroing `body[9]`, descriptor or GOST removes it | `tests/plan-f77/66-newcomp-ourcode/README.md`, `run.py` | **FACT (PASS)** |
| Test 67: zone `N+2` words 526..900 emitted by `O412C.FTN` replace the live `2148:0o1552`; zeroing 526 or 900 gives TIMEOUT | `tests/plan-f77/67-our-n2/README.md`, `run.py` | **FACT (PASS)** |
| Test 68: a multi-word sequence (`*64`, `UJ`, second `*64`) executes in order | `tests/plan-f77/68-two-stage/README.md` | **FACT (PASS)** |
| B1: all 1024 words of zone `N+1` can be emitted by our Fortran (`O412C` 0..18, `O412D` 19..1023), A/B on body word 36 → TIMEOUT | `logs/f77_30_59_b1_full_emit.txt` | **FACT** |
| B2 (21.11): "our body words are **never** executed; `*TRANS` only prints the banner read from disk" | `logs/f77_30_59_b2_no_exec.txt` | **SUPERSEDED for the test-66 configuration** |
| The preface of `docs/62-newcomp-re.md` (22.11) explicitly corrects B2: the B2 statement is true only for the banner; test 66 proved `body[9]` executes at `0o1770` | `docs/62-newcomp-re.md` lines 7-11 | **FACT (latest word)** |
| D1: our FRONT/CODEGEN compiles BASE77 and emits an image that prints `21 1.00 3.00` through **our** `*64`; bound 6/5 → `21`/`15`; but the prototype needed a (forbidden) C patch to reach RAM | `logs/f77_30_59_d1_our_compiler_prototype.txt` | **FACT (prototype), BLOCKED on install path** |
| E1: clean binary monitor patch that loads our words into RAM | `logs/f77_30_59_e1_binary_patch.txt` | **BLOCKED** (redirect word found, word-loading not achieved) |

**Consequence for phase 4.** The target is not "invent a new execution mechanism". It is: take the *proven disk-only install recipe of tests 66/67/68*, replace its hand-built static marker with words produced by `FRONT.FTN → CODEGEN → EMIT48/GOSTEN`, and prove the A/B criteria. Whether the *computed* value can be produced by BESM-6 arithmetic at run time, or must be folded by our codegen into GOST bytes at emission time, is **phase 3's result**; phase 4 must be designed to accept either (§5).

---

## 1. Data-flow diagram — proven components vs missing links

```
  Fortran source deck (BASE77, physical cards, 72 cols)
    e.g. docs/plan-f77-full/logs/f77_30_base77_deck_forex.txt
         PROGRAM / N=0 / DO 10 I=1,6 / N=N+I / X=1.0 / Y=X+2.0
         PRINT 100,N,X,Y / FORMAT(1X,I4,2F10.2) / STOP / END
        |
        | host injects: PARAMETER(NC,NLV,LL=132,LW=72); INTEGER RAW(LW,NC)
        |               INTEGER C(LL,NLV); INTEGER SEQ(NLV); DATA RAW /ASCII/
        v
  [1] FRONT.FTN  (src/newcomp/FRONT.FTN, 131 lines)  .......... PROVEN PARTIAL
        N1.1 logical lines / continuation / SEQ
        N1.3 label allocator (777004 kind 21, 90000..99999)
        N1.4 IR records 777001 / 777002 / 777003 / 777004 via PRINT+I8
        GAP: only pattern recognised today is `PRINT *` (PATPRN=80,82,73,78,84,32,42).
             BASE77 has NUMBERED PRINT, counted DO, FORMAT, assignments, STOP.
             -> rule table must be extended (design in §3.1). No new record TYPE needed.
        |
        v IR (all numeric, 1X,4I8/5I8)
        777001 <seq> <rule> <itype>
        777002 <seq> <pos> <code>      (ASCII stream of the logical line)
        777004 <seq> <kind> <pos> <code>
        777003 <nlines> <nrewrites>
        |
        v
  [2] CODEGEN  (src/newcomp/CODEGEN.deck N3E/N3D/N3P + EMIT48 contract)
       ....................................................... PROVEN PARTIAL
        N3E: expressions N=0, X=1.0, Y=X+2.0        (5 words)
        N3D: counted DO I=1,6, back-jump            (5 words)
        N3P: PRINT/FORMAT + FT* calls               (8 words, 3 are FORMAT DATA)
        GAP: addresses 0100..0115 are placeholders (N,I,X,Y,ZERO,ONE,SIX,F1,F2,
             /100,FT*571,FT*002,FT*003); no symtab; FT* calls are resident routines
             and cannot be relied on in the *TRANS body (57 §3 risks, LINK report).
             Phase 4 substitutes *64+descriptor for the FT* chain (§3.3), and
             relocates all addresses onto body RAM 0o1757+k (§3.4).
        |
        v  (IR/KOP/ADR pairs, IR*2^21+KOP*2^15+ADR per 24-bit halfword)
  [3] EMIT.FTN: EMIT48 + GOSTEN + OCT8  ....................... PROVEN (0 ERR, 2.02)
        EMIT48 -> HI(NW)=IR1*2097152+K1*32768+A1; LO(NW)=...
        GOSTEN -> ASCII(12) -> GOST-10859 bytes -> 2 words, 6 bytes/word
        GAP: /EMBUF/ must be sized HI(1100),LO(1100) for >=1005 words;
             overflow at NW=1101 corrupts NW (B1 §2). Nothing else.
        |
        +---------------------------+---------------------------+
        |                           |                           |
        v                           v                           v
  [4a] O412C.FTN                [4b] O412D.FTN              [4c] computed-result
       16 catalog words             1005 tail words              words from [2]+[3]
       + 19 body 0..18              body 19..1023               (N digits / X,Y GOST)
       + 375 N+2 words 526..900     (1005/1005 = live root)    <-- PHASE 3 interface
       .... PROVEN (410 words)      .... PROVEN (1005 words)    .... DESIGN / P3
        |
        v complete word set: 16 + 19 + 1005 + 375 = 1415 words
        | (1415 words require COMMON /EMBUF/ HI(1500),LO(1500): B1 §2)
        v
  [5] Install harness (pattern of tests 66/67/68; run-our-trans.sh uses the older
      30-word O412B variant)  ................................. PROVEN for static words
       copy 2048/2053/2099/2148, redirect HOME and BESM6_PATH
       besmtool write 2148 --start=01744 (catalog, 16 words)
       besmtool write 2148 --start=01745 (body, 1024 words)
       besmtool write 2148 --start=01746 (N+2, 375 words at offsets 526..900)
       zones N+3..N+40 := 1024 zero words each
       deck: DIS 41(2148)^ / *TRANS:OURMRK*,,411744 / PROGRAM... / *execute
        |
        v
  [6] NEWCOMP* (resident, zone 422 fragment + disk-30 overlay) .... PROVEN RE
       P1 ENTRY 0o3000..0o3014   save M15; M13=0o6000, M14, M12=0o1146; *70 d30/z50
       P2 0o3020..0o3022         read catalog zone N (disk 41); M16 = TEXT name
       P3 0o3033..0o3055         XOR name compare; f0 = desc & 0o7777; require f0=0o1760
       P4 0o660..0o711           decode f-fields; *70 continuous N+1,N+2,...;
                                 copy body[k] -> RAM 0o1757+k (M6 receiver)
       P5 RAM 0o455               runtime-built vjm 64002(15) -> resident FOREX 4.12
        |
        v
  [7] Execution / output .................................. PROVEN for static marker
       our *64 at 0o1770 -> descriptor at 0o2004 -> GOST at 0o2006 -> E64 -> console
       " 21 1.00 3.00" then "КОНЕЦ ЗАДАЧИ"
        |
        +-- GAP (phase 4 target): the printed digits must be OUR computed result,
            and must change when OUR front-end/codegen words change (A/B).
        +-- GAP (phase 3 owner): run-time arithmetic vs emission-time folding.
```

**One-line summary of what is missing:** everything up to (and including) the *static* print is proven; the missing link is a *computed* GOST result produced by our FRONT+CODEGEN and placed in the exact body slots that the proven `*64`/descriptor path consumes, plus wiring `O412D` into the 66/67 harness so no live-root word remains.

---

## 2. Exact word budget and layout

### 2.1 The three zones and one descriptor

All numbers are 1-based unless marked "offset" (offset = index inside the 1024-word zone).

| zone | disk 2148 logical zone | word offsets | word count | source (proven) |
|:--|:--|:--|--:|:--|
| catalog `N` | `0o1744` | 0..15 | **16** | `O412C.FTN` output 1..16 (same values as `O412B` K0..K15) |
| body `N+1` | `0o1745` | 0..18 | **19** | `O412C.FTN` output 17..35 |
| body `N+1` tail | `0o1745` | 19..1023 | **1005** | `O412D.FTN` output 1..1005 |
| overlay table `N+2` | `0o1746` | 526..900 | **375** | `O412C.FTN` output 36..410 |
| `N+2` outside 526..900 | `0o1746` | all others | 649 | zeros |
| `N+3 .. N+40` | `0o1747..0o1814` | 0..1023 | 38*1024 | zeros |
| **total emitted by our Fortran** | | | **1415** | 16+19+1005+375 |

### 2.2 Catalog word identities (must not change)

From `O412B.FTN` / `O412C.FTN`, 1-based output index → 48-bit word (octal):

| idx | role | value / decode |
|--:|:--|:--|
| 1 | TEXT `MONITOR*` | `0o5557565164576212` (sentinelHI=11991977, LO=13827210) |
| 2 | sentinel descriptor | `0o0000000000000370` (f0 = 0o370) |
| 3 | TEXT `OURMRK*` | `0o5765625562531200` (HI=12541101, LO=13283968) |
| 4 | **main descriptor** | `0o400402757101760` → `f0 = 0o1760` — **required** by P3 (`aax 3076` + `aex 0o1760`) |
| 5..8 | LO*SYN / LO*GEN TEXT+desc pairs | live satellite pairs, copied by P3 |
| 9..16 | terminator + ISO OVERLA + build comment | zeros / `417050000000000` / 4 comment words / zero |

`f0 = 0o1760` is the only hard constraint on the catalog: the M4 sweep (`62` §3.1) showed every other value gives `НЕТ РАЗДЕЛА` or `СВОБОД`.

### 2.3 Body prefix and copy mapping

| body offset | RAM (= `0o1757 + offset`) | role | provenance |
|--:|:--|:--|:--|
| 0 | `0o1757` | service word `0o1600043` | O412C |
| 1 | `0o1760` | DMS `w0` = TEXT `FOREX3*` / `head|sym|debug` | O412C |
| 2 | `0o1761` | DMS `w1` = `set|data<<15|long<<30` | O412C |
| 3 | `0o1762` | DMS `w2` = `cmd|bss<<15|const<<30`, `cmd=0o1760` | O412C |
| 4 | `0o1763` | marker `0o73461` | O412C |
| 5 | `0o1764` | loader stub `уиа '1760'(М16) / пб 464` — **DATA, not our code** | O412C |
| 6..8 | `0o1765..0o1767` | live header words | O412C |
| **9** | **`0o1770`** | **our first executable word (`*64`, or first arithmetic word)** | **OURS — phase 4 slot** |
| 10 | `0o1771` | `uj 0(15)` return / second word of our sequence | OURS |
| 11..18 | `0o1772..0o2000` | descriptor words, GOST text, or arithmetic/data | OURS / A5 layout |
| 0o25 = 21 | `0o2004` | test-66 descriptor word 0 (`addr0=addr1=0o2006`) | OURS |
| 0o27 = 23 | `0o2006` | test-66 GOST text start | OURS |
| 19..1023 | `0o1776..0o2156` | **B1 tail** | `O412D.FTN` (1005 words) |

**Critical: the phase-2 harness still takes body words 19..1023 from the live root.** Concretely, `tests/plan-f77/t412/run-our-trans.sh` line 68 builds `body.bin` as `words[16:] + lw[14:1024]`, i.e. 14 words from `O412B` plus `live_root[14:1024]`; `tests/plan-f77/66-newcomp-ourcode/run.py` line 80-82 similarly fills every zero body slot from `live1551[i]` for `i in 22..1023`. Test 67 only replaces zone `N+2`. `O412D.FTN` (1005 words, 4 UNITs EMT00..EMT03, `4089` lines) has already demonstrated byte-exact equivalence to the live tail (`1005/1005`, B1 §1), so **phase 4's wiring change is to make the harness use O412D output instead of `live1551`/`live_root`** — no new emitter is needed.

### 2.4 Critical words (A/B sentinels)

Body words whose zeroing breaks the run, from B1 §5 (O412D 1-based index = body offset − 18):

| body offset | O412D 1-based idx | emitted word (octal) | zeroing effect |
|--:|--:|:--|:--|
| **36** | 18 | `0o4000000000500155` | **TIMEOUT** |
| 147 | 129 | `0o0000000001700357` | TIMEOUT |
| 387 | 369 | `0o0000001561300432` | no banner |
| 670 | 652 | `0o0000000000500357` | no banner |
| 910 | 892 | `0o0000000000600010` | TIMEOUT |
| 919 | 901 | `0o4000000002601165` | TIMEOUT |

Zone `N+2` sentinels (from test 67): offset 526 = `0o0000000402400101`, offset 900 = `0o0000000134300265`; zeroing either → TIMEOUT. Word 36 must be present in **our** body; the design therefore keeps the entire O412D tail verbatim and only edits the designated code/data slots 9..18 and 0o25..0o31.

### 2.5 Constraints that must be respected by any new Fortran unit

1. **`COMMON /EMBUF/` sizing.** Layout is `HI(1..n), LO(1..n), NW`. Writing word `n+1` overwrites `NW` itself. Proven: `n=1100` handles 1005 words; for the combined 1415-word stream use `n=1500` or chunk into several UNITs (B1 §2, §3). O412C uses 1100, O412D uses 1100 in 4 chunks — keep that pattern.
2. **40-bit mantissa.** FOREX 2.02 INTEGER mantissa is 40 bits. The proven `EMIT48` formula stays within it: max halfword = `7*2^21 + 63*2^15 + 32767 = 2^24−1` (`EMIT.FTN` lines 17-22). Do not form a full 48-bit value in one INTEGER; always keep HI and LO separate 24-bit INTEGERs. GOST bytes are 8-bit values packed 6 per word (HI = bytes 0..2, LO = bytes 3..5) via step-by-step Horner, as in `GOSTEN`.
3. **FOREX 2.02 subset.** No `CHARACTER`, no `PRINT *`, no `SAVE`, no `IMPLICIT`, no `nH` literals; names ≤6 characters; fixed form ≤72 columns; `NLV ≤ 31` per logical UNIT; all output numeric (`PRINT n, ...`, `I8`/`I12`/`O16`). TEXT/GOST data are injected as decimal ASCII codes (`DATA IA /.../`).
4. **Descriptor contract** (`59-a5prep` §1.2, `extra.c`): word 0 = `iiii ........ xxxxxxxxxxxx / jjjj ........ yyyyyyyyyyyy` (addr0/addr1 = x+R[i], y+R[j]); word 1 = `ffff bbbbbbbb dddddddddddd / esss wwwwwwww rrrrrrrrrrrr` (`f=0` GOST text, `b=1` one leading column, `e=0o10` final/flush, `d=w=r=0`). GOST terminator byte is `0o231`.
5. **Do not patch the link cells or the monitor.** 59-LINK and 62 §1.1 prove the `*TRANS` route is `SHX 0o430(M14)`; patching LINK or zone 422 breaks boot. C3 (C patch) is explicitly not the target path.

---

## 3. Minimal first target: BASE77 compiled by our own front end, printing its own computed `21 1.00 3.00`

### 3.1 Exact IR records to emit for BASE77

Use the existing four record types only; extend the **rule numbers** in `777001`, not the record schema. `RAW` (physical-card ASCII) is host-injected; `FRONT.FTN` builds logical lines and streams their ASCII into `777002`.

Source (canonical deck, `f77_30_base77_deck_forex.txt`) and the IR to produce (seq = first physical card number; positions 1-based on the glued 132-char logical line):

```
777001  1 30 0      PROGRAM BASE77                         rule 30 = PROGRAM
777001  2 31 1      N=0                                    rule 31 = assignment, itype 1 INTEGER
777002  2 1 78       'N'                                   (ASCII codes of whole logical line,
777002  2 2 61       '='                                    one record per position)
777002  2 3 48       '0'
777001  3 32 1      DO 10 I=1,6                            rule 32 = counted DO, itype 1
777002  3 1 68 ...   'DO 10 I=1,6'                          ASCII stream (positions 1..11)
777004  3 21 0 90000  reserved label for loop               kind 21 = label request (existing)
777001  4 33 0        10 CONTINUE                          rule 33 = labelled CONTINUE
777001  5 31 1      X=1.0                                  rule 31, itype 2 REAL
777002  5 1 88 ...   'X=1.0'
777001  6 31 2      Y=X+2.0                                rule 31, itype 2 REAL
777002  6 1 89 ...   'Y=X+2.0'
777001  7 34 0      PRINT 100,N,X,Y                        rule 34 = numbered PRINT
777002  7 1 80 ...   'PRINT 100,N,X,Y'                     ASCII stream, parsed for the var list
777001  8 35 0      FORMAT(1X,I4,2F10.2)                   rule 35 = FORMAT
777002  8 1 70 ...   'FORMAT(1X,I4,2F10.2)'                ASCII stream, parsed for the spec
777004  8 21 0 90001  reserved label for FORMAT            optional, as in F77PREP
777001  9 36 0      STOP                                   rule 36
777001 10 37 0      END                                    rule 37
777003 10  8                                               summary: 10 logical lines, 8 rewrites
```

Rules 30..37 are **new pattern entries** in the FRONT.FTN `PAT*` table (same technique as `PATPRN /80,82,73,78,84,32,42/`); no `CHARACTER`, no `PRINT *`. The existing `777001/2/3/4` writer loops (`FRONT.FTN` lines 101-129, formats 9001..9004) are reused unchanged — this is the "reuse proven code" requirement: only the classification table and the `IRULE` assignment grow.

**Codegen's minimum extraction from this IR:** DO bound `B = 6` (from the `777002` stream of seq 3), variable slots `N,I,X,Y`, and FORMAT spec text `1X,I4,2F10.2`. With `B=6` the integer result is `N = B(B+1)/2 = 21`; X=1.0, Y=3.0. (If phase 3 delivers run-time arithmetic, these become values in data cells instead — see §5.)

### 3.2 Codegen words — the proven 18-word BASE77 sequence

`src/newcomp/CODEGEN.deck` (N3E/N3D/N3P), decoded in `logs/f77_30_n3_codegen_report.txt` §5. These 18 words are the **exact** output of our Fortran codegen (compiled by SYSTEM FOREX 2.02, `NW=18`, 0 errors):

| # | word (octal) | decode | role |
|--:|:--|:--|:--|
| 1 | `0010010400000100` | `сч 104 / зп 100` | N = 0 |
| 2 | `0010010000040101` | `сч 100 / сл 101` | N + I |
| 3 | `0000010000100110` | `зп 100 / сч 110` | store N; load F1 |
| 4 | `0000010200040111` | `зп 102 / сл 111` | X; +F2 |
| 5 | `0000010300000000` | `зп 103 / зп 0` | Y; pad |
| 6 | `0010010500000101` | `сч 105 / зп 101` | I = 1 |
| 7 | `0010010000040101` | `сч 100 / сл 101` | loop body |
| 8 | `0000010000100101` | `зп 100 / сч 101` | store N; load I |
| 9 | `0004010500000101` | `сл 105 / зп 101` | I = I + 1 |
| 10 | `0005010702700020` | `вч 107 / пе 20` | I−6; back-jump |
| 11 | `7010011203100113` | `сч(М14) 112 / пв 113` | FORMAT address; CALL FT*571 |
| 12 | `0010010003100114` | `сч 100 / пв 114` | N → FT*002 |
| 13 | `0010010203100114` | `сч 102 / пв 114` | X → FT*002 |
| 14 | `0010010303100114` | `сч 103 / пв 114` | Y → FT*002 |
| 15 | `0310011500000000` | `пв 115 / зп 0` | CALL FT*003; pad |
| 16 | `1203053013044464` | DATA | `(1X,I4` |
| 17 | `1303110614230056` | DATA | `,2F10.` |
| 18 | `1442444010020040` | DATA | `2)` |

Placeholder cells (`n3_codegen_report` §5): `0100=N, 0101=I, 0102=X, 0103=Y, 0104=0, 0105=1, 0106=2, 0107=6, 0110=F1(1.0), 0111=F2(2.0), 0112=/100, 0113=FT*571, 0114=FT*002, 0115=FT*003`.

**For the integrated body, two substitutions are required (design, not yet implemented):**

- **S1 — remove the resident FT* chain.** Words 11..15 cannot be used as-is: `FT*571/002/003` are external SUBP of the resident compiler, and 59-LINK proved LINK cells are not patched in the `*TRANS` path. Replace them with the proven `*64` idiom from tests 66/68/A5: a two-word `*64 ADR` + `uj 0(15)` sequence, followed by a 2-word descriptor and the GOST text. The D1 prototype already demonstrated this substitution in a generated 400-word image (§3.4).
- **S2 — relocate addresses.** `0100..0115` → body RAM `0o1757+k` for the chosen slots. In the D1 layout, N=`0o2257`, I=`0o2260`, descriptor=`0o2266`, GOST=`0o2300`; in the A5/test-66 layout, `*64` at `0o1770`, descriptor at `0o2004`, GOST at `0o2006`. Choose **one** canonical layout and compute every ADR from `0o1757 + body_offset` (the same identity the loader uses). This is the symtab/N3.6 step; the numbers must be derived, not hardcoded.

### 3.3 GOST descriptors needed

Canonical descriptor pair (test-66 layout, `addr0 = addr1 = 0o2006`):

```
descriptor word 0  = 0o0000200600002006   (i=j=0, x=y=0o2006)
descriptor word 1  = 0o0001000040000000   (f=0 GOST, b=1, e=0o10 final/flush, d=w=r=0)
```

`*64` command (word at body 9 / RAM `0o1770`): `0o0064177202200000` was the A3 value pointing at `0o1772`; for the test-66 descriptor at `0o2004` use the same encoding with ADR=`0o2004`, i.e. `0o0064200402200000`. Return word: `0o6700000002200000` (`uj 0(15)`).

GOST bytes for `21 1.00 3.00` (12 bytes + `0o231` terminator), packed 6 per 48-bit word by `GOSTEN` (`EMIT.FTN` GT table, authoritative `monitor80-re/tools/encoding.cpp:614-679`):

| byte # | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|:--|
| char | `2` | `1` | ` ` | `1` | `.` | `0` | `0` | ` ` | `3` | `.` | `0` | `0` | EOF |
| GOST code (octal) | 2 | 1 | 15 | 1 | 14 | 0 | 0 | 15 | 3 | 14 | 0 | 0 | 231 |

Packed words (A5prep §2 / B2 §5.1, verified on console):

```
word A = 0o0040041700207000   bytes [2,1,15,1,14,0]   -> "21 1."
word B = 0o0000740303400000   bytes [0,15,3,14,0,0]   -> " 3.00" (leading space is byte 7)
word C = 0o4620741703607417   bytes [231,15,15,15,15,15] -> EOF + padding spaces
```

**Computed variant:** only bytes 1..2 vary with `N`. With `N=21` → `[2,1]`; with `N=15` (bound 5) → `[1,5]`. The D1 prototype emitted exactly these two variants (`logs/f77_30_59_d1_our_compiler_prototype.txt` §3, E64 trace confirms `gost -002-001-...` vs `gost -001-005-...`). This is the concrete phase-3 handoff point: phase 3 decides whether those bytes are produced by BESM-6 arithmetic or by our codegen; phase 4 places whichever words it supplies into word A.

### 3.4 Body placement for the first target (one canonical layout)

```
body[0..8]   unchanged O412C prefix (B0..B8, includes critical word 3/4/5/36? no: 36 is in the tail)
body[9]      *64  ADR=descriptor_body  (first executable word, RAM 0o1770)
body[10]     uj 0(15)                   (RAM 0o1771)
body[11]     descriptor word 0
body[12]     descriptor word 1
body[13]     GOST word A  ("21 1.")  <- computed bytes here
body[14]     GOST word B  (" 3.00")
body[15]     GOST word C  (EOF + spaces)
body[16..18] data cells (N, I, constants) if S2 needs them
body[19..1023] O412D tail verbatim (word 36 must stay 0o4000000000500155)
```

If phase 3 requires the D1 400-word unrolled-loop image instead, the same body slots are used with `*64` at `0o2014`, descriptor at `0o2266`, GOST at `0o2300` (D1 §2.3); the install harness is unchanged. **Keep both layouts parameterised by a single base address** so the choice is a data change, not a code change.

### 3.5 Acceptance criteria (the A/B that must close)

Positive: deck with `*TRANS:OURMRK*,,411744` prints `21 1.00 3.00` and `КОНЕЦ ЗАДАЧИ` on stock dispak with all disks copied.

| # | mutation | expected | proves |
|--:|:--|:--|:--|
| A1 | zero our `*64` word (`body[9]`) | marker disappears | our emitted code word is on the execution path |
| A2 | zero our descriptor word (`body[0o25]`) | marker disappears | descriptor is ours, not resident `53450/53464` |
| A3 | zero our GOST word A (`body[0o27]`) | marker disappears / changes | text is read from our emitted word |
| A4 | change the IR DO bound 6 → 5 in the front-end input | output becomes `15 1.00 3.00` | **our FRONT+CODEGEN computed the result** |
| A5 | zero `body[36]` (O412D idx 18) | TIMEOUT | O412D tail is installed and necessary |
| A6 | zero zone `N+2` offset 526 or 900 | TIMEOUT | emitted overlay table is necessary |
| A7 | keep `N+3..N+40` zero (already the harness default) | output unchanged | no live resident overlay zone is needed |
| A8 | delete/neutralise the live-root file at build time | output unchanged | no byte comes from `disk412_forex3_root.words` |
| A9 | skip install entirely | no marker (only `КОНЕЦ ЗАДАЧИ`) | negative control |

A1-A4 are the "our front-end/codegen words change → output changes" half; A7-A8 are the "resident overlay zones zeroed → output unchanged" half. A4 additionally closes the loop that test 66/67/68 leave open (they only prove a *static* marker).

---

## 4. Risks

| id | risk | evidence | mitigation / gating |
|:--|:--|:--|:--|
| R1 | **Execution-path ambiguity.** Test 66/68 say our body word executes at `0o1770`; B2 says body words are never loaded and the banner is read from disk. Both cannot be literally true for every configuration. | `62` preface vs `b2_no_exec` §2-4 | First milestone M0 must reproduce A1/A2/A3 on the **target** configuration and record an MTR/core trace. If our arithmetic words turn out not to execute, fall back to D1's emission-time folding (phase 3 interface) — the printed result is still *our* computed result, but not BESM-6-computed. This is the single largest design risk. |
| R2 | Simulator arithmetic mantissa. `сч 1; сл 1; зп N` yielded `N=0` (left-half 17-bit mantissa, right half unused) in D1 §2.2. | `d1` §2.2 | Do not rely on BESM-6 run-time arithmetic for the first target unless phase 3 explicitly proves a workaround. Compute `B(B+1)/2` in our Fortran codegen and emit GOST bytes. |
| R3 | FT* external SUBP unavailable in `*TRANS`. Words 11..15 of CODEGEN call resident routines; LINK cells not patched. | `n3_codegen` §7, 59-LINK | Substitute `*64`+descriptor (S1) before integration; gate on E64 trace showing our descriptor address, not `53450/53464`. |
| R4 | `/EMBUF/` overflow. 1415 words with `HI(1100)` corrupts `NW` and truncates output. | B1 §2 | Keep O412C at 1100 and O412D chunked at 1100; if a single combined emitter is used, size 1500. Verify emitted count = 410 + 1005 = 1415. |
| R5 | Word 36 / other critical words accidentally overwritten by inserting our code into body 19..1023. | B1 §5 | Only write slots 9..18 and 0o25..0o31; treat 19..1023 as read-only except the designated data cells below 0o31. Re-run the six-word sentinel scan after each change. |
| R6 | FOREX 2.02 subset violations (CHARACTER, `PRINT *`, SAVE, IMPLICIT, >72 cols, >31 logical lines, names >6). | 57 §4, EMIT.FTN header | All new units are copy-only extensions of `FRONT.FTN`/`EMIT.FTN`; compile each with the `run-our-trans.sh` pattern and require `0 ERR`. |
| R7 | Install harness still reads live root for body 19..1023. | test 66 `run.py:80-82`, `run-our-trans.sh:68` | Explicit milestone M2 replaces those reads with O412D output and an A8 negative control. Until M2 passes, "autonomy" claims are false. |
| R8 | Renumbering body offsets breaks every absolute ADR. | `body[k] → 0o1757+k` | Derive all ADRs from one `BASE = 0o1757` constant in the codegen; never hand-edit octal addresses. |
| R9 | C-patch / monitor-patch temptation. C3 and E1 are proven research paths but forbidden/not target. | 60, 59-E1 | Design stays strictly disk-only + stock dispak; no `BESM6_*` env injection, no `cu.c`/`defs.h` edits. |

---

## 5. Ordered milestones, each with go/no-go

Legend: **[P3]** = depends on the concurrent phase-3 result; **[ind]** = independent of phase 3 and can start now.

| # | milestone (design step) | go/no-go criterion | dep |
|:--|:--|:--|:--|
| **M0** | Baseline reproduction: run tests 66, 67, 68 unchanged on copies; capture MTR/core evidence for `0o1770` and confirm the exact A1/A2/A3 A/B on the target config. | All three VERDICT=PASS; trace recorded. If our words are **not** in RAM, invoke R1 fallback and re-scope M4 to emission-time folding. | ind |
| **M1** | Extend `FRONT.FTN` rule table to the BASE77 rules 30..37 (§3.1); keep `777001..4` writer unchanged; inject RAW from the canonical deck. | SYSTEM FOREX 2.02 compiles with 0 ERR; IR matches §3.1 exactly (diff against expected numeric records). | ind |
| **M2** | Wire `O412D.FTN` output into the 66/67 harness: body 19..1023 from O412D, body 0..18 + catalog + N+2 from O412C, `N+3..N+40` zero. A5/A6/A7/A8 pass. | Console banner + `КОНЕЦ ЗАДАЧИ`; zeroing body 36 → TIMEOUT; live-root file absent → unchanged output. **This is the "no live-root words" gate.** | ind |
| **M3** | Wire the 18-word CODEGEN sequence into EMIT48/GOSTEN with relocated addresses (S2) and the `*64`+descriptor substitution (S1); emit a static `21 1.00 3.00` image first. | Emitted words decode to the §3.2 sequence with body-based ADRs; A1/A2/A3 close; E64 trace shows **our** descriptor address. | ind |
| **M4** | Computed result: feed the §3.1 IR bound into codegen so the GOST bytes become `21` for bound 6 and `15` for bound 5. | **A4 passes** (`15 1.00 3.00`); A1-A3 still pass. If phase 3 supplies run-time arithmetic instead, substitute its word stream at the same slots and re-run A4. | **[P3]** |
| **M5** | Full integration + catalogue A/B table: run the complete 1415-word emission (O412C 410 + O412D 1005 + computed words), stock dispak, copies only. | All A1..A9 PASS; SHA of live 2148/2048 unchanged; `git status` clean. | **[P3]** for the computed half; ind for the rest |
| **M6** | Regression/handoff: document SHA of fixtures, record the exact word table, update plan docs (no repo edits in this design task; main agent owns them). | Reviewer can reproduce from report + existing tests alone. | ind |

**Go/no-go discipline:** stop at whichever milestone fails. M0 failure → R1 re-scope (do not proceed to M3/M4 as if execution were proven). M2 failure → no autonomy claim. M4 failure with P3 incomplete → report "static marker only", not "computed output". M5 failure → no commit, no claim.

---

## 6. Explicit phase-3 interface contract (what phase 4 needs and will not duplicate)

Phase 4 **does not** design or implement the runtime computed-output mechanism. It consumes one of two possible results:

| phase-3 outcome | what phase 4 does with it |
|:--|:--|
| **P3-A: run-time arithmetic works** (BESM-6 computes N=21 in data cells) | Phase 4 places phase 3's arithmetic word stream at body slots 9..k, keeps the descriptor/GOST words as a *formatter target*, and re-runs A4. No change to catalog/O412C/O412D. |
| **P3-B: emission-time folding required** (D1-style: our codegen computes `B(B+1)/2` and emits GOST bytes) | Phase 4 places the phase-3-supplied GOST words at body words 0o27.. (or D1's `0o2300..`), keeps `*64`+descriptor, re-runs A4. This is already proven feasible by D1 §3. |
| **P3-C: neither** | Phase 4 delivers M0-M3 only (static marker, fully autonomous body) and reports "computed output BLOCKED, owned by phase 3". |

Interfaces phase 4 fixes regardless of the outcome:
1. **Single base constant** `BASE = 0o1757`; every body address = `BASE + body_offset`.
2. **Reserved slots** for code/data: body 9..18 and 0o25..0o31; everything else in 19..1023 stays verbatim O412D.
3. **The descriptor pair and `*64` idiom** are unchanged (§3.3); phase 3 may only change the GOST payload word(s) and/or add arithmetic words before them.
4. **A4 is the shared gate**: bound 6 → `21`, bound 5 → `15`. Both phases measure the same console string.

---

## 7. Bottom line

- The install path is proven end-to-end for a **static** marker: catalog `f0=0o1760`, body copy to `0o1757+k`, N+2 table, zeroed outer zones, `*TRANS:OURMRK*,,411744`.
- Our emitters can already produce **every one of the 1415 words** (`O412C` 410 + `O412D` 1005) with byte-exact A/B, but the current 66/67 harness still takes body 19..1023 from the live root — that is phase 4's first concrete wiring change (M2).
- Our FRONT+CODEGEN can already produce the **shape** of BASE77's machine code (18 words) and a prototype image that prints a computed result, but the FT* calls must be replaced by the proven `*64` idiom and all addresses must be relocated onto the body base.
- The one unclosed question — whether our body arithmetic words truly execute in the disk-only `*TRANS` path — is the R1 gate at M0 and is **not** answered by this design; phase 3 owns the computed-output half. Phase 4 is ready to proceed with M0–M3 independently of phase 3.

**End of design document.**
