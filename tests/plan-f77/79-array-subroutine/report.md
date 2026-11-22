# re-forex, limit-lifting step 4 (revised direction): monitor-side call path + ARRAY + SUBROUTINE

**Date:** 22.11.2026. **Work dir:** `/tmp/.private/azizz/opencode/re-forex-limit-array/`.
**Write scope:** only this work dir; bulky disk copies under `/dev/shm/re-forex-limit-array-cases`
(reached through `run78/cases -> /dev/shm/...` symlink). `HOME`/`BESM6_PATH` redirected per case.
No repo edits, no git writes, no live disks/tmux/processes, no dispak C patches.

---

## 0. Direction change (per user directive)

The original step-4 brief asked for safe slots inside the shared NEWCOMP* body. The user
overrode that: use the Monitor-80 sources to make the monitor call our compiler, and stop
safe-slot hunting. All work below follows the override. The earlier safe-slot map is kept
only as background (§1) and is **not** used as the implementation path.

---

## 1. Background: safe-slot map (FACT, from the earlier part of this session)

Measured with test-78's harness + MTR window bands (LO/HI octal, re-arming means a 0-hit band
proves no PC in the band is ever executed):

| probe | result |
|:--|:--|
| RAM `0o2064` | EXECUTED (MTR `uta` at 0o2064) |
| RAM `0o2065 .. 0o2260` | **NEVER executed** (wide bands `0o2065..0o2215`, `0o2223..0o2257` and `0o2065..0o2257` all had 0 MTR records; single-address probes 0o2065/0o2070/0o2074/0o2100/0o2214/0o2215/0o2257/0o2260 all 0) |
| RAM `0o2261` | EXECUTED (MTR `vzm` at 0o2261) |
| RAM `0o2041` | EXECUTED (MTR `u1a 17..`, matches docs/64 §3.2) |

Overwrite A/B of body[0o100..0o120] with sentinels: marker `21 1.00 3.00`, `КОНЕЦ ЗАДАЧИ`,
valid CORE dump all preserved, sentinels arrived at RAM `0o1773+k`. So the region is not
load-bearing. **This path was abandoned per the user's directive.**

---

## 2. Monitor-side rebuild (FACT)

Toolchain copied into `m80build/` (volumes 80 = copy of disk 2048, plus 2048/2053/2099/2148/2348).
One local tool fix: `degak.py` was patched for Python 3 (leading-zero octal tokens in `eval`);
this is a copy in the work dir, not a repo edit.

Exact commands (all with `PATH=m80build:dispak/build/{besmtool,dispak}:$PATH`,
`BESM6_PATH=m80build`, `WORKVOL=80`):

```
WORKVOL=80 BESM6_PATH=m80build perl -CA asm.pl 'givtran%.asm'
# -> givtran%.dis = 486 bytes, byte-identical to monitor80-re/permanent/givtran%.dis
WORKVOL=80 BESM6_PATH=m80build perl -CA asm.pl 'sub%.asm'
# -> sub%.dis: 15,VJM,*0002B / 13,UJ, / *0002B:,ARX,*0003B / 15,UJ, / *0003B:,LOG,3
WORKVOL=80 BESM6_PATH=m80build perl -CA asm.pl 'ourc%.asm'
# -> ourc%.dis (OURC* module): XTA AIDX / ARX / ATX / 15,VJM,OURSUB / UJ,1 /
#    OURSUB:,*64,SDESC / 15,UJ,  (0 errors)
perl overlay.pl 80 'sub*' 'sub%.asm'
# -> catalog: SUB* 60 0001 00 00014 01770 ; object written to volume-80 zone 04
```

`ourc%.asm` (full source in `m80build/ourc%.asm`) is our compiler as a monitor text: an array
element `AIDX` at the measured base, a `VJM` call to an internal subroutine `OURSUB*` that owns
the `*64` print descriptor and returns with `15,UJ,`.

---

## 3. Working *TRANS install path (FACT)

Reused verbatim from tests 66/78 (zone `N=0o2350`, catalog = O412C words 0..15, body at N+1,
overlay words at N+2, zones N+3..N+40 zero; deck `*TRANS:OURMRK*,,412350`). The rebuilt
GIVTRAN/SETTRAN text (test 65's `givtran_our.asm` lineage) is the monitor side of the call;
our body words are installed via the NEWCOMP* 4.12 catalog.

**Honest boundary (FACT + INFERENCE):** the recomputed modules compile and build cleanly, but
the resident GIVTRAN*/TTABLE*/STACOMP* are formed at load time from the zone-0200 LINK table,
not loaded from the disk library (repo `docs/plan-f77-full/61-ttable-newcomp-findings.md` §19-22).
Writing an `overlay.pl` object into OCATALOG zones therefore does **not** change `*TRANS`
dispatch. The route that actually works is the 4.12 catalog at zone N, whose main-section
load base is fixed at `f0=0o1760`. I did **not** obtain a different/high load base from the
monitor text rebuild. Verdict for "clean RAM in a separate high zone": **NOT ACHIEVED**;
the working path is the monitor-side call with our code in the catalog body.

---

## 4. ARRAY + SUBROUTINE implementation and A/B (FACT)

Word placement (RAM addresses from the measured map, `BASE=0o1757`, body[k] -> RAM BASE+k):

| item | body index | RAM | word / role |
|:--|:--|:--|:--|
| entry / array load | 9 | 0o1770 | `XTA 2006 / ARX A(index)`; ADR = `0o2020 + index-1` (base+index) |
| N-unit add / store | 10 | 0o1771 | `ARX / STO 2006` |
| subroutine call | 0o11 | 0o1772 | `VJM 0o2000` (computed from SUB base) |
| after-return return | 0o13 | 0o1774 | `uj 0(15)` |
| **internal subroutine** | 0o21 | 0o2000 | `*64 2004` = the print word lives in the routine |
| subroutine return | 0o22 | 0o2001 | `uj 0(15)` |
| array A(1) | 0o41 | 0o2020 | value cell |
| array A(2) | 0o42 | 0o2021 | value cell |
| array A(3) | 0o43 | 0o2022 | value cell |

The `VJM` operand is generated as `vjm(SUB)`, `SUB = BASE + 0o21 = 0o2000`; the array operand
as `ARX (BASE + 0o41 + index-1)`. No hardcoded print result: the leading digit is produced at
run time from the addressed array cell and the routine.

### A/B table (all cases: rc=0, `КОНЕЦ ЗАДАЧИ` present)

| case | index | A(k) value | subroutine | console line | verdict |
|:--|:--|:--|:--|:--|:--|
| `fin2_idx2` | 2 | 3 | live | `61 1.00 3.00` | array loaded |
| `fin2_idx3` | 3 | 5 | live | `51 1.00 3.00` | **index 2->3 changes printed digit** |
| `fin2_zeroA` | 2 | 0 | live | `01 1.00 3.00` | **zeroing A(2) changes printed digit** |
| `fin2_zerosub` | 2 | 3 | **first word zeroed** | (no print line) | **output breaks** |

Console evidence (grep of `run78/cases/fin2_*/out.txt`): `61 1.00 3.00` at line 205,
`КОНЕЦ ЗАДАЧИ` at line 1118; `51`/`01` likewise; `fin2_zerosub` has no `1.00` line but still
`КОНЕЦ ЗАДАЧИ`. CORE dumps exist for all four cases (`core-pc.bin`, `core-uic.bin`, 384 KB).

Instruction words were generated with the proven test-72 `emit48` opcodes (XTA=0x008000,
ARX=0x00b000, STO=0), `VJM` with the resident `пб`-style opcode (b0=0o14), and `uj 0(15)`
return = `0o6700000002200000`.

---

## 5. Verdicts

| item | verdict | evidence |
|:--|:--|:--|
| (i) Monitor-side call path: rebuild with `asm.pl`/`overlay.pl` on copies | **PASS** | `givtran%.dis` 486 B byte-identical; `sub%.dis`, `ourc%.dis` compile with 0 errors; `overlay.pl` catalog produced |
| (i) Monitor-side call path: `*TRANS` routes to OUR code | **PASS** | tests 66/78 recipe; our VJM subroutine and array change the printed output |
| (i) Clean RAM in a separate high zone via monitor text | **NOT ACHIEVED** | resident GIVTRAN/TTABLE/STACOMP are LINK-built; OCATALOG installs do not affect `*TRANS`; main-section base fixed at 0o1760 |
| (ii) ARRAY | **PASS** | A(2)=3->`61`, A(3)=5->`51`, A(2)=0->`01`; address = base+index |
| (ii) internal SUBROUTINE | **PASS** | VJM call to OURSUB at 0o2000; zeroing its first word removes the print line |

---

## 6. Evidence index

| file | content |
|:--|:--|
| `m80build/ourc%.asm`, `m80build/ourc%.dis` | monitor MADLEN text of our array+subroutine compiler, assembled cleanly |
| `m80build/givtran%.dis`, `m80build/sub%.dis` | rebuild outputs |
| `execmap_bands.txt`, `execmap_hits.txt`, `safe_boundaries.txt`, `safe_overwrite_fixed.txt` | background safe-slot map (abandoned path) |
| `array_sub.py`, `array_sub2.py`, `final_proof.py`, `final_proof2.py` | implementation scripts (final: `final_proof2.py`) |
| `fin2_*_out.txt`, `run78/cases/fin2_*/out.txt` | console evidence + CORE dumps |
| `final_proof2_results.txt`, `core_verify.txt` | A/B table and word-placement dump |
