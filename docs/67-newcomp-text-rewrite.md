# re-forex, final loader step: TEXT rewrite of NEWCOMP* -- BLOCKED at install

> Предисловие главного агента: текст загрузчика действительно восстановлен и
> компилируется (§1–2) — возражение «почему не переписать текст» снято. Блокирует
> не текст, а установка: резидентные слова не берутся из доступных для записи
> зон диска 2048. Дополнительно я проверил патч **всех** копий слов на всех
> дисках (2048/2053/2099/2148/2348) на копиях: загрузчик в ОЗУ не изменился,
> а `*TRANS` дал `КОНТРОЛЬ КОМАНДЫ` — то есть этот путь тоже не рабочий.

**Date:** 22.11.2026. **Workspace:** `/tmp/.private/azizz/opencode/re-forex-newcomp-src/`.
**Scope honored:** COPIES only; `HOME`/`BESM6_PATH` redirected per case; bulky disks/cases in
`/dev/shm/re-forex-newcomp-src-*`; no repo edits, no git writes, no live disks, no tmux,
no processes, no dispak C patches, no secrets/env dumps.

**VERDICT: FAIL / BLOCKED.** A MADLEN-equivalent source of the resident NEWCOMP* loader was
authored, assembled and successfully compiled with `asm.pl`, and an object was produced with
`tostar.pl`/`linker.pl`. The two modified machine words were installed on copies of disk 2048
in **every** zone that contains them. But the resident RAM words at `0o3047` and `0o673` stayed
byte-for-byte identical to the original loader; `*TRANS` kept the original 3-zone / 58-clean-word
behavior. The literal text of this loader is **not reachable by a disk install** on this path:
its executable words are produced/held by the resident Monitor-80 image, not loaded from the
disk zones we can write. This is the exact failure the brief allowed to be reported.

---

## 1. Authored MADLEN source (complete)

File: `src/ournc%.asm` (copies: `src/ournc.asm`, `src/ournewcomp.asm`).  It is a line-by-line
MADLEN equivalent of `docs/62-newcomp-re.md` §5 (P1 entry, P2 catalog read, P3 scan, P4
decode/copy). Register modifiers in source syntax are **decimal** (e.g. `14,` = octal M16),
which was learned from `monitor80-re/permanent/givtran%.dis`.

```
 OURNC*:   ,NAME,DTRAN  / reconstructed NEWCOMP* text /
C=====================================================================
C OURNEWCOMP -- MADLEN equivalent of Monitor-80 NEWCOMP*, from
C docs/62-newcomp-re.md section 5.  Register modifiers below are DECIMAL
C (source syntax), i.e. 14 = octal M16, 15 = octal M17.
C MOD-1 P3 relaxed f0 satellite gate.
C MOD-2 P4 receiver M6 += 0o26040, body base 0o1760 -> 0o30000.
C=====================================================================
 P1:,LP,3000B
         ,ITA,13                .3000 save return (octal M15)
         ,STI,13
         ,ASN,64+10             .3001
         ,ASN,64-10
         ,ATI,11                .3002 M13 = 0o6000
  11,WTC,2000B
  12,ITS,11                .3003 M14 = M13
  10,UTC,1146B
         ,ITA,11                .3004
         ,ASN,64-20
         ,AOX,424B              .3005
  15,ATX,1
  15,*70,1                 .3006 *70 disk 30 zone 50
  14,UTC,3063B             .3007
  13,VJM,3033B
         ,UZA,3077B         .3010
  14,UTC,3064B
  13,VJM,3033B
         ,U1A,3070B         .3012
  14,UTC,3065B
  13,VJM,3056B
   9,UJ,                   .3014
         ,ASN,54B           .3020 P2
         ,AOX,77B
  15,ATX,1                .3021
  15,*70,1
  14,VTM,577B             .3022
  13,VJM,3033B
  12,MTJ,11               .3033 P3
         ,UTC,0
  11,XTA,                 .3034
  13,UZA,
  14,AEX,                 .3035
         ,UZA,3037B
  11,UTM,2                .3036
         ,UJ,3034B
  11,XTA,1                .3037
         ,UTC,3076B
         ,AAX,3076B        .3040
  15,ATX,1
  11,XTA,                 .3041
  10,ATX,0
  11,XTA,1                .3042
  10,ATX,1
  11,UTM,2                .3043
  10,UTM,2
  11,XTA,0                .3044
         ,UZA,3055B
  11,XTA,1                .3045
         ,AAX,3076B        .3046
C MOD-1: was  ,AEX,1(17) / ,UZA,3055B
         ,UJ,3055B
  10,MTJ,14               .3051
  14,UTM,-166B
  14,V1M,3041B
  15,XTA,1                .3055
  13,UJ,
 LIT:,LP,3063B
        ,LOG,0000 0000 0000 0000     .3063..0o3075 (literals)
        ... (13 words, 0o3076 = mask 0o7777, 0o3077 = 0o777777)
 P4:,LP,660B
  14,XTA,1                .660
         ,ASN,64+15
         ,ATI,3            .661
         ,ASN,64+15
  15,ATX,0                .662
         ,AAX,752B
         ,ASN,64-5         .663
  15,ATX,0
         ,ARX,35B          .664
   0,STX,153
         ,ASN,64-37        .665
         ,ARX,153B
   0,STX,153               .666
         ,ASN,64+5
         ,AAX,753B         .667
         ,ARX,146B
   0,ATX,145               .670
         ,*70,145
   5,XTA,3                .671
   0,ATX,151
   5,XTA,4                .672
   0,ATX,152
   6,ITS,5                .673 M6 = M5
C MOD-2: original second half of 0o673 was ,MOD
   6,UTM,26040B
   3,VZM,712B             .674
  13,VJM,736B
  15,ATX,0                .675
         ,ATI,9
         ,ASN,117B         .676
  10,UTM,0                .677
         ,AAX,750B
         ,UZA,701B
  13,VJM,736B             .700
         ,XTS,             .701
   9,VZM,706B             .702
  13,VJM,736B
   6,ATX,0                .703
   3,UTM,-1B
   9,UTM,-1B              .704
   6,UTM,1B
         ,UJ,702B         .705
         ,STX,             .706
  10,VZM,674B             .707
   6,ATX,0
   3,UTM,-1B              .710
  10,UTM,-1B
   6,UTM,1B               .711
         ,UJ,707B
         ,XTS,             .712
         ,END,
```

Only two behaviors were changed (both visible as `MOD-1`/`MOD-2` above):

| id | original | modified | intended effect |
|:--|:--|:--|:--|
| MOD-1 | `0o3047` first half `uza 3055` (f0-equality exit in satellite loop) | `uj 3055` (unconditional exit) | accept new f0 without breaking catalogue name lookup |
| MOD-2 | `0o673` second half `mod` (address-mode no-op) | `utm 26040(M6)` | receiver base `0o1760 + 0o26040 = 0o30000` (clean high RAM) |

The key descriptor fields (`f0=0o1760`, `f1=0o5710`, `f2=0o4027`, `f3[5:0]=0`) and the
catalogue name `OURMRK*` were deliberately kept, so the proven `*TRANS` path is not disturbed.

**Inference markers.** FACT: all opcodes/addresses except MOD-1/MOD-2 are transcribed from
`docs/62` §5 and confirmed word-for-word against a live CORE dump (`logs/live_ram.txt`).
INFERENCE: the exact numeric displacement `0o26040` for MOD-2 (chosen so `0o1760+0o26040 =
0o30000`); this is a design choice, not observed behavior. INFERENCE: replacing `mod` with
`utm` at `0o673` assumes the original `mod` halfword is a no-op for the copy loop.

---

## 2. Compile / build commands (all successful)

Toolchain copied from `/home/azizz/Yandex.Disk/monitor80-re/tools/` into `tools/`;
volume 80 = copy of disk 2048; `HOME`/`BESM6_PATH` redirected to workspace copies.

```
cd /tmp/.private/azizz/opencode/re-forex-newcomp-src/src
export HOME=../home BESM6_PATH=../disks WORKVOL=80
export PATH=../tools:/home/azizz/Yandex.Disk/dispak/build/dispak:$PATH
perl -CA ../tools/asm.pl 'ournc%.asm'          # -> ournc%.dis, 1195 bytes, 0 errors
perl ../tools/tostar.pl 'ournc%.asm'           # -> ournc%.obj, 2560 bytes
perl ../tools/linker.pl -zone 0004 -top ournc 'ournc%.obj'
```

`ournc%.dis` begins:

```
 OURNC*:,NAME,DTRAN  /01.06.84/
 P1:,LP,1536
 LIT:,LP,1587
 P4:,LP,432
 ,ITA,13
 ,STI,13
 ,ASN,64+10
 ...
```

This proves the rewritten TEXT compiles with the proven MADLEN toolchain (the same path that
reproduced `givtran%.dis` byte-identically in prior subagent work). `asm.pl` initially rejected
`ournewcomp.asm` (module name must be <= 8 chars and end in `%` so `*CALL DTRAN(mod*)` matches);
renaming to `ournc%.asm` fixed it.

---

## 3. Disk/RAM format research (FACT)

| item | fact |
|:--|:--|
| `reference/m80/zone422.bin` | 1024 six-byte big-endian words, logical zone `0o422` of disk 2048 |
| disk image layout | `zone_t` = 8 control words + 1024 data words = 8256 bytes; data words are 64-bit LE with 48-bit payload; `ZONE_OFFSET = 4` (`dispak/diski.h`); `besmtool dump --start=N` and `write --from-file` both address physical zone `N+4` |
| P1-P3 on disk | zone `0o422` word `0o777+k` corresponds to RAM `0o3000+k` |
| load-time transformation | long-format instruction address fields in `0o2001..0o2177` get `+0o762` (e.g. zone `0o1006` = `72402101 67102051` -> RAM `0o3007` = `72403063 67103033`); addresses outside that window, and all short-format/data words, are unchanged. Constant derived from 64 verified word pairs (`logs/live_ram.txt`, script inline in §5) |
| P4 on disk | disk 2048 zone `0o010` words `0o640..0o737` equal RAM `0o640..0o737` **identically** (no relocation). Nine other zones hold copies |
| DMS header | zone `0o422` word `0o740` = length `0o136`, word `0o741` = TEXT `FOREX3*`, words `0o742..0o751` = header/cmd (the resident 4.12 module) |
| catalog/body install | zones N=`0o2350` (catalog `OURMRK*`), N+1 (body), N+2 (overlay data), N+3..N+40 (zeros), deck `*TRANS:OURMRK*,,412350` (harness from `tests/plan-f77/80-high-ram-zone/`) |

Important correction to the task premise: disk-30 zone `0o0050` is **all zeros** (`zone50.bin`);
the `*70` at RAM `0o3006` clears the catalog buffer, it does not fetch scan/loader code.
All NEWCOMP* code is already resident/loaded from the system image.

---

## 4. MTR evidence of the unmodified loader (FACT)

Baseline run `cases/trace/out.txt`, `BESM6_MTR_LO=0660 BESM6_MTR_HI=0711 BESM6_MTR_N=4000`
(192,000 MTR records; `logs/trace_loader.out`):

```
MTR 00660L xta 1(16) ... M: 03=00000 05=01760 06=00000 11=00000 12=00000 16=64002
MTR 00661R asn 117(0) ... M: 03=03530                 M3  = 0o3530 (1880) counter
MTR 00673R utc 0(0)   ... M: 05=01760 06=01760        M5 = f0 = 0o1760, M6 := M5 (receiver)
MTR 00702L vzm 706(11) ... M: 03=03530 11=00070 12=00204  M11=0o70 zones, M12=0o204
MTR 00703L atx 0(6)    ... AU=5156606564434154        first body word stored to M6
MTR 00704R utm 1(6)    ... M6 0o1760 -> 0o1761
```

The loop at `0o703..0o705` executes ~5,940 times (calls to subroutine `0o736`), so the
baseline copies ~1,880 + ~132 words starting at RAM `0o1760`. Rejection/exit tests are
`vzm 674(12)` / `vzm 712(3)` (`docs/66` §4). The measured *clean* region remains 58 words at
`0o30114..0o30205` (`docs/66` §6, `docs/80`); the rest of `0o1760..` is reused by the resident
compiler. This is why a higher base was needed.

---

## 5. Installation attempts and A/B table

Scripts: `install_test.py`, `ab_run.py`, `ab_patchall.py`. Each case copies disks 2048/2053/2099,
writes the 4.12 catalog/body zones, then writes patched zone images with `besmtool write`.
The compiled MOD-1/MOD-2 machine words (computed from the assembler mnemonics and verified
against the live encodings) are:

```
MOD-1 (RAM 0o3047 first half):  uza 3055 = 02603055  ->  uj 3055 = 03003055
       full word: 0260207374120001 (disk, pre-relocation) -> 0300305574120001
MOD-2 (RAM 0o673 second half):  mod = 02200000 -> utm 26040(M6) = 32526040
       full word: 2444000602200000 -> 2444000632526040
```

`ab_patchall.py` scans **all 4000 disk zones** and rewrites every occurrence of each original
word. Occurrences found and patched:

```
MOD1 zone 0422 word 1046
MOD2 zones 0010,0053,0210,0230(word 0376),0440(word 0514),0604(word 1673),0635,1024,1076
```

| case | loader patches | body stub base | rc | `21 1.00 3.00` | `КОНЕЦ ЗАДАЧИ` | CORE RAM `0o3047` | CORE RAM `0o673` |
|:--|:--|:--|:--|:--|:--|:--|:--|
| `a_plain` | none | 0o1760 | 0 | yes | yes | `0260305574120001` | `2444000602200000` |
| `b_stub` | none | 0o30000 | 0 | yes | yes | unchanged | unchanged |
| `c_m1` | MOD-1 (one zone) | 0o1760 | 0 | yes | yes | unchanged | unchanged |
| `d_m2` | MOD-2 (two zones) | 0o1760 | 0 | yes | yes | unchanged | unchanged |
| `h_m1all` | MOD-1 (all zones) | 0o1760 | 0 | yes | yes | unchanged | unchanged |
| `l_m2all` | MOD-2 (all 9 zones) | 0o1760 | 0 | yes | yes | unchanged | unchanged |
| `m_both` | MOD-1 + MOD-2 (all) | 0o30000 | 0 | yes | yes | unchanged | unchanged |

CORE dumps were taken with `BESM6_CORE_ON_PC=03022` (right after the catalog `*70`), and the
words above are read directly from `cases/<name>/core-pc.bin`. Disk verification after the
writes shows the patched words **are present on disk** (e.g. physical zone `0o14` logical
`0o010` word `0o673` = `2444000632526040`), but the corresponding RAM words are still the
originals. Therefore the resident loader does not take these words from the writable disk
zones at boot: the text rewrite cannot be installed this way.

The requested A/B "zero a copied word -> output breaks / restore old loader words -> old
behavior returns / no install -> no marker" is **N/A** because no modified loader ever became
active; the only reproducible A/B is the descriptor-field one already in `docs/66` §8.

Two harness bugs were found and fixed during the work (both would have produced false results):
1. `besmtool write --from-file=<key>` needs the `.bin` suffix; without it the zone was zeroed and
   `*TRANS` reported `ОТСУТСТВУЕТ OURMRK*` (case `a_plain` first run).
2. `disk_zones[]` indices are the zone numbers accepted by `besmtool dump`/`write` (physical+4
   internally); subtracting 4 when writing targeted the wrong zone.

---

## 6. PASS/FAIL

| criterion | result |
|:--|:--|
| reconstructed MADLEN-equivalent source authored from `docs/62` §5 | **PASS** (§1) |
| compiled with `asm.pl`, object built with `tostar.pl`/`linker.pl` | **PASS** (§2) |
| correct disk-zone/transform install format identified | **PASS** (§3) |
| modified loader actually resident at RAM `0o3000`/`0o660` | **FAIL** (§5, CORE unchanged) |
| body loaded into a larger (>=200 words) clean RAM area at new base | **FAIL** (never attained) |
| marker preserved with new base | **N/A** (MOD-2 never active) |
| A/B of copied word / restored loader | **N/A** |

The text rewrite is real and compiles, but the final loader is LINK/resident-built and the
specific executable words cannot be replaced by writing disk 2048 zones; a prior attempt to
corrupt the adjacent DMS header (zone `0o422` word `0o751`) broke boot before `*TRANS`
(`docs/63` §4, run `e13_z422bad2`), which bounds the writable part of that zone. No dispak C
patch or old-`f0` catalog path was used or claimed as a solution.

BLOCKED: the rewritten loader words are resident/regenerated in Monitor-80 RAM (CORE at 03022 shows RAM 0o3047 and 0o673 unchanged after patching every disk-zone copy), so a text-level rewrite cannot be installed via disk 2048 zones; the >=200-word clean-region load cannot be demonstrated.
