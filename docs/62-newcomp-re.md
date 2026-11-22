# RE report: M80 `NEWCOMP*` (`*TRANS`) — procedures, index registers, loader contract

> Предисловие главного агента. Документ получен субагентом 22.11.2026 по запросу
> «подробно прокомментировать процедуры NEWCOMP* и установить значения индексных
> регистров по образцу re-siprod». Отчёт полностью сохранён, включая ссылки на
> временный workspace. Одна формулировка §3.5 взята из более раннего отчёта B2 и
> **устарела**: «*TRANS никогда не исполняет слова нашего тела». Это верно только
> для баннера, который загрузчик читает с диска. Тест 66
> (`tests/plan-f77/66-newcomp-ourcode/`) доказал, что слово `body[9]` исполняется
> по адресу `0o1770`, а `body[0o25]`/`body[0o27]` — по `0o2004`/`0o2006`.
> Читать §3.5 нужно с этой поправкой; остальные FACT/INFERENCE-метки не изменены.

**Date:** 22.11.2026. **Working directory:** `/tmp/.private/azizz/opencode/re-forex-newcomp-re/`.
**Scope honored:** all repositories and live disks READ-ONLY; every disassembler run was on a copy
(`zone422_orig.bin`) inside this workspace; no git writes, no dispak C patches, no live disks, no tmux,
no processes, no secrets/env dumps. `dtran -F dms zone422_orig.bin` crashed with SIGBUS (the whole zone
is not a valid DMS object); `disbesm6` worked and is the source of all machine-code lines below.

**Methodology:** the `re-siprod` style of `notes/registers.md` + `madlen/BEGPG.madlen`
(register EQU block, header with roles, per-instruction inline comments, procedure boundaries after
unconditional jumps) is emulated in §5. Names of registers are written as `Mnn` (octal register numbers,
as in `re-siprod/notes/registers.md` §2 and §4). Addresses are octal with `0o` prefix unless stated.

---

## 0. Provenance: what the "compiled binary" actually is

An honest correction to the task premise, established by correlating the raw zone with the live RAM dump
(all items below are **FACT**):

1. There is **no source text** of `NEWCOMP*` (accepted premise, not re-proved).
2. `reference/m80/zone422.bin` (1024 words, file offsets of disk 2048, logical zone `0o422`) contains a
   **compiled object fragment**: its words `511..` decode as executable code at RAM `0o3000..`, followed
   by literal pools / tables. Verified directly:

   ```
   zone word 511 = 0o02200d00300f  -> disbesm6 -a3000:  счи М15 / счм 15
   zone word 512 = 0o0042001500030017 ->            сда 64+10 / сда 64-10
   zone word 513 = 0o0036011200360066 ->            уи М13 / слиа '2000'(М13)
   ```
   This is word-for-word the first three lines of the live-RAM entry at `0o3000..0o3002`
   (`logs/f77_30_m80_newcomp_live_disasm.txt` §3.1). So the zone file **is** the on-disk image of the
   loader's entry point, and the "first 7 words match RAM `0o3000..0o3006`" note in
   `docs/plan-f77-full/61-ttable-newcomp-findings.md` §2 is confirmed, with the precise alignment
   `zone word (511+k) -> RAM 0o3000+k`.
3. The **remaining procedures** (`0o3033..0o3055` catalog scan, `0o640..0o711` body loader) are **not**
   present as contiguous code in this zone: at zone addresses `0o3033..` the file contains data words
   (e.g. `0o3033 = 6044001302200000`, not `mtj 13(14)/utc 0`). They are brought in at run time by the
   `*70` read of disk 30 / zone `0o0050` executed at RAM `0o3006`. They are documented in
   `docs/plan-f77-full/logs/f77_30_m80_newcomp_live_disasm.txt` (RAM dump + 90 000-instruction trace).
   **Both sources are therefore required** and both are used below; §5 labels each line with its source.
4. The **final hand-off** is not code inside this fragment. The word at RAM `0o455` is *assembled at run
   time* by the monitor cycle `0o64415..0o64427` and equals `6710000202200000` = `vjm 64002(15)`
   (`59-autonomous-body-plan.md` §5a C1, `60-patched-trans-recipe.md` §2.1). That is the transfer into
   the resident FOREX 4.12 body.

Consequence for the report: "NEWCOMP* compiled binary" = zone-422 entry fragment + RAM-resident scan
and loader procedures + the runtime-built VJM word. All are covered.

---

## 1. Procedure map — from `*TRANS:name,,41/N` to `VJM 0o64002`

### 1.1 Call chain around NEWCOMP* (FACT, from `monitor80-re/permanent/` and findings §10)

| step | source | what happens |
|---|---|---|
| 1 | `star%.masm:116-118` | `XTA TRCAT*` (translator catalog) -> `M13,VJM,SETTRAN*`. **M13 is the VJM linkage/return register** (see §2). |
| 2 | `givtran%.asm` | `SETTRAN*`: `XTA MONCARD*` (the `*TRANS` card) -> `AEX для*тип*трн` -> `UZA в*STACOMP` -> `M14,XTA,1; UJ STACOMP*`. |
| 3 | `stacomp%.asm` | `STACOMP*` stores the name in `TRNAME*`, searches `TRCAT*` via `dncomp`, loads `STLOAD*`, reads the catalog with `*70`/E70. |
| 4 | `ltable%.asm:37-38` | `ISO 6H*TRANS / TEXT 8HNEWCOMP*` — this is the **STABLE (disassembler) mapping**, not the runtime resolver (findings §7, §11). |
| 5 | physical resolver | The name is resolved against the **catalog in zone N on disk 41 (2148)**: pairs `TEXT-name / descriptor`. Proved by A/B: patching `FOREX3* -> OURCOM*` in `2148:0o1550.0002` makes `*TRANS:OURCOM*` load 4.12 (findings §9). |
| 6 | LINK route | Zone 200 of disk 2048, word `200.0331` = `6510700004300000` = **`SHX 0o430(M14)`** — the LINK address word that routes `*TRANS` into NEWCOMP*'s jump-table stub at `M14 + 0o430` (findings §7-8). Patching only this word breaks resolution, so it is inseparable from the stub. |

### 1.2 Procedures inside NEWCOMP* (the executable fragment)

| id | range (RAM) | source | role |
|---|---|---|---|
| **P1 ENTRY** | `0o3000..0o3014` | zone-422 words `511..525`, verified against live dump | Save return register; unpack the `*TRANS:name,,41/N` parameter; set up catalog buffer (`M13`/`M14`) and descriptor buffer (`M12`); assemble INF word in task-catalog element `1(М17)`; `*70` read disk 30 / zone `0o0050` (loads the rest of NEWCOMP*); error branches; exit via `M11`. |
| **P2 CATALOG-READ** | `0o3020..0o3022` | live RAM dump | Build INF `0o10030000411550` (disk 41, zone `0o1550` / generic `N`); `*70` reads the catalog zone; set `M16` to the searched TEXT name; goto scan. |
| **P3 SCAN-DESCRIPTOR** | `0o3033..0o3055` | live RAM dump + trace | Walk `name/descriptor` pairs in the catalog buffer; XOR-compare the name; extract `f0` with mask `0o7777`; copy matched and satellite pairs into `M12` buffer; compare `f0` with `0o1760`; return via `M15`. |
| **P4 DECODE-AND-LOAD** | `0o660..0o711` | live RAM dump + trace | Decode `f3/f2/f1/f0` with shifts and masks; build body-read INF `0o10320000411551` (zone `N+1`); `*70` reads continuous zones `N+1, N+2, ...`; copy loop with receiver `M6`; branch on `M3`. |
| **P5 HAND-OFF** | word at RAM `0o455` | runtime cycle `0o64415..0o64427` | `vjm 64002(15)` transfers to the resident 4.12 compiler body. |

### 1.3 Control flow (compact)

```
*TRANS:name,,41/N
   |
   v  (LINK SHX 0o430(M14) -> NEWCOMP* stub)
0o3000 P1: счи М15; счм 15            save return
0o3001     сда 64+10 / сда 64-10      unpack parameter bits
0o3002     уи М13; слиа '2000'(М13)   M13 = 0o6000  catalog buffer
0o3003     уии М14(М13); уиа '1146'(М12)  M14 = M13; M12 = descriptor buffer
0o3005     или '424'; зп 1(М17)       INF word -> 0o53405
0o3006     Э70 1(М17)                 *70: disk 30 / zone 0o0050 (fetch rest of NEWCOMP*)
0o3007..0o3014  error branches, exit via пб (М11)
0o3020 P2: asn 54; aox 77             INF = 41/N
0o3021     atx 1(17); Э70 1(17)       *70: read catalog zone N
0o3022     vtm 577(16); vjm 3033(15)  M16 = target name; goto P3
0o3033 P3: mtj 13(14); utc 0          M13 = M14 = catalog start
0o3034     xta 0(13); uza 0(15)       name; 0 = end -> return
0o3035     aex 0(16); uza 3037        name XOR target; 0 = match
0o3036     utm 2(13); uj 3034         next pair
0o3037     xta 1(13); utc 3076        descriptor; MODREG = mask 0o7777
0o3040     aax 3076; atx 1(17)        f0 = descriptor & 0o7777
0o3041-42  copy name+descriptor into M12 buffer
0o3043     utm 2(13); utm 2(12)       advance both pointers
0o3044-50  check f0 of following pairs; loop back via 0o3051-52
0o3055     xta 1(17); uj 0(15)        return (f0 in accumulator)
0o660  P4: сч 1(М16); сда 64+15       decode f-fields
0o671     сч 3(М5) ...                f0 = 0o1760
0o674     пио A00656+28(М3)           branch by M3
0o700-711 copy loop (M6 = receiver, zones N+1, N+2, ...)
   |
   v
RAM 0o455: 6710000202200000 = vjm 64002(15)
   |
   v
resident FOREX 4.12 at 0o64002
```

### 1.4 Data areas

| area | address | role | evidence |
|---|---|---|---|
| catalog buffer | `0o6000` (from `M13 = 0o6000`, `слиа '2000'(М13)`) | one zone read from disk 41/N; pairs of words | live disasm 0o3002, trace `DD pc=03022L u=41 z=1550` |
| descriptor buffer | `0o1146` (`M12`), grows by 2 | matched name/descriptor pairs copied here | 0o3003, 0o3041-43 |
| search string | pointed to by `M16` (`'2101'`, symbolic `D03064-1`; then `0o577` = target name) | TEXT name from the card | 0o3007, 0o3022 |
| task-catalog element | `1(М17)` = `0o53405` (`0o53402..`) | INF word for `*70` | 0o3005, 0o3021; re-siprod `notes/registers.md` §3.4 identifies `0o4000+` addresses as Monitor-80 task catalog |
| masks | `0o3076 = 0o7777`, `0o750 = 0o777777?` (18-bit), `0o752 = 0o37`, `0o753 = 0o777`, `0o751 = 0o777777` | descriptor field extraction | live log §3.3 constants |
| body load base | `0o1760` = `f0` = `cmd` | M16 base of loaded body | M4 §3.1, object-format spec §1.3 |
| final VJM word | RAM `0o455` | `vjm 64002(15)`, built by cycle `0o64415..0o64427` | 59-C1, 60 §2.1 |

---

## 2. Index register table — values and roles, with evidence

Legend: **F** = FACT from disassembly/dump/trace; **I** = INFERENCE from behavior experiments.
"Not observed" means the register does not appear in the NEWCOMP* code examined; the re-siprod
convention for that register is given only as context, not claimed as used here.

| reg | when set | what it holds | setting / using instructions (address) | status |
|---|---|---|---|---|
| **M1** | not observed in NEWCOMP* | (in re-siprod: `MОДА` index / module base) | none in this code | F (absence) |
| **M2** | not observed | (re-siprod: scratch) | none | F |
| **M3** | `0o661` | high part of decoded descriptor (f3/f2/f1 bits), selects load branch | `уи М3` / `сда 64+15` (`0o661`); `пио A00656+28(М3)` (`0o674`) | F (mechanism), I (which bit means what) |
| **M4** | secondary code island `0o1400..0o1406` of the zone | counter/index into a name field | `сч 1(М4)` + `сда 64+15`/`сда 64+41` (`0o1402`, `0o1406`) | F (code), I (role) |
| **M5** | `0o671..0o673` | base of descriptor buffer (`0o1153` = copy of `f0`); source for body-copy setup | `сч 3(М5)` (`0o671`), `сч 4(М5)` (`0o672`), `уии М6(М5)` (`0o673`) | F |
| **M6** | `0o673` | **receiver pointer for body copy**, grows through `0o700..0o711` | `уии М6(М5)` (`0o673`); loop `0o700-711` | F |
| **M7** | not observed | (re-siprod: task frame pointer; NEWCOMP* uses `M17` for the task-catalog element instead) | none | F |
| **M8** | not observed | — | none | F |
| **M9** | not observed | — | none | F |
| **M10** | caller's block in secondary island | caller's parameter block pointer: reads fields `'261'(М10)`, `'263'(М10)` | `сч '261'(М10)` (`0o1401`), `и '263'(М10)` (`0o1403`), `сч '272'(М10)` (`0o1407`) | F |
| **M11** | — | **second return channel** | `пб (М11)` at `0o3014` (exit on error path) | F |
| **M12** | `0o3003` | **descriptor-buffer pointer**, initially `0o1146`, advanced by 2 per pair | `уиа '1146'(М12)` (`0o3003`); `atx 0(12)/1(12)` (`0o3041-42`); `utm 2(12)` (`0o3043`) | F |
| **M13** | `0o3002`, `0o3033`, `0o3036`, `0o3043` | **catalog scan pointer**, initially `0o6000`, +2 per name/descriptor pair. **Separate monitor convention: VJM linkage/return register** (`M13,VJM,SETTRAN*` in `star%.masm`; callee ends `13,UJ`; `INITFO: ITA 13; ATX RET`), confirmed in `docs/plan-f77/02-extension-points.md` §28/§275 and `include/FOREX_CORE.registers.md` | `уи М13` + `слиа '2000'(М13)` (`0o3002`); `mtj 13(14)` (`0o3033`); `utm 2(13)` (`0o3036`, `0o3043`) | F (both roles, from different sources) |
| **M14** | `0o3003` | copy of `M13` = **catalog base** for the scan. Also the index register in the LINK word `SHX 0o430(M14)` that enters NEWCOMP*'s jump-table stub | `уии М14(М13)` (`0o3003`); LINK word `200.0331 = 6510700004300000` (findings §7) | F |
| **M15** | `0o3000` (saved), used `0o3007..0o3055` | **return-address register for internal VJM (`пв`) calls**; saved on entry, restored for `uj 0(15)` | `счи М15 / счм 15` (`0o3000`); `пв '2051'(М15)` (`0o3007`, `0o3010`, `0o3012`); `vjm 3033(15)` (`0o3022`); `uza 0(15)` (`0o3034`); `uj 0(15)` (`0o3055`) | F |
| **M16** | `0o3007`, `0o3022`; in loaded body `0o1760` | **modified-address / search-string pointer**; holds the TEXT name to find. In the 4.12 body it is set to `f0 = 0o1760` (the load base) by the stub `уиа '1760'(М16)` | `уиа '2101'(М16)` (`0o3007`); `vtm 577(16)` (`0o3022`); `aex 0(16)` (`0o3035`); body stub `уиа '1760'(М16)` (`1551.0005`) | F |
| **M17** | implicit task context | task-catalog base; `1(М17) = 0o53405` holds the packed INF word | `зп 1(М17)` (`0o3005`); `atx 1(17)` (`0o3021`) | F |

### 2.1 The M14 / M16 special case (explicitly requested)

* **FACT:** the LINK entry for NEWCOMP* in zone 200, word `200.0331`, is `6510700004300000`, decoded in
  findings §7 as **`SHX 0o430(M14)`**. This is an address word, not ordinary code; it routes `*TRANS`
  through a jump-table stub at offset `0o430` relative to `M14`. Replacing just this word with the
  STACOMP* address word (`6610700010200000`) produced a silent `КОНЕЦ ЗАДАЧИ`, and patching the
  LINK *name* `200.0330` produced `ОТСУТСТВУЕТ NEWCOMP*` — i.e. the stub structure is required
  (findings §7-8).
* **FACT:** in the loaded 4.12 body, `f0 = 0o1760` (low 12 bits of descriptor `0o400402757101760`),
  and `cmd[1] = 0o7240176003000464` decodes to `уиа '1760'(М16) / пб '464'`
  (`412_object_format_spec` §1.3). Therefore **M16 = 0o1760** exactly when the real compiler is loaded.
  A register dump at the failure point shows `... 01760 ...` in the M16 slot (`W_hybrid/out.txt:30`).
* **FACT:** the DMS header field `cmd = 0o1760` (`body word 3 = 0o0002220000001760`) is numerically
  equal to `f0`, but is a different field (command-section length). The sweep in M4 §3.1 showed that
  `f0`, not `cmd`, must be exactly `0o1760`: changing `cmd` of our little module to `0o1760` while
  leaving `f0 = 0o11` still gave `НЕТ РАЗДЕЛА`.
* **INFERENCE:** `0o1760` serves simultaneously as main-section ID, load base of the body, and (by
  construction of the 4.12 linker) the command-section length. The experiment that would separate these
  roles is given in §6.

### 2.2 M13 return convention — precise statement (FACT)

There are two distinct M13 conventions in play and they must not be confused:

1. **Monitor MADLEN convention:** `M13,VJM,<subr>` = call subroutine with return address in M13;
   the callee returns with `13,UJ` (or `M13,UJ`). Seen in `monitor%.asm:109`,
   `stload%.asm:65/72/75/107`, `stacomp%.asm:33/36/39/52/106/117`, `ioxxfmr%.asm` (many),
   and on the `*TRANS` path in `star%.masm:118` (`M13,VJM,SETTRAN*`).
   `INITFO` saves it: `ITA 13; ATX RET(0o4023)`; `PRINT8` uses `STI RETLR` then `13,VJM,WRTLBR+1`.
2. **NEWCOMP* internal convention:** its own calls use **M15** (`пв ...(М15)`) and the procedure
   returns via `uj 0(15)` at `0o3055`, with an alternate error exit `пб (М11)` at `0o3014`.
   M13 here is a data pointer (catalog scan), not a return register.

---

## 3. Loader contract

### 3.1 Catalog at zone N (FACT)

* Zone N on disk 41 is read by one `*70` at RAM `0o3021`; packed INF = `0o0010030000411550`
  (opcode/count `0o001003` + packed disk/zone `41 / N`).
* Structure (from live catalog `2148:0o1550`, confirmed by A/B patching):
  * word 0 = TEXT `MONITOR*`, word 1 = short descriptor `0o370` (sentinel);
  * then 2-word pairs `TEXT-name / descriptor`, e.g. `FOREX3*` = `0o4657624570231200` with
    descriptor `0o400402757101760`;
  * terminated by a zero word (`0o3034: xta 0(13); uza 0(15)`).
* Descriptor layout: `d = f3<<36 | f2<<24 | f1<<12 | f0`, four 12-bit fields.
* Name comparison is bitwise XOR of the 8×6-bit TEXT words (`0o3035: aex 0(16)`), not string compare.
* `f0` extraction is `MODREG = 0o3076 (=0o7777)` followed by `aax 3076` at `0o3040`
  (trace table in live log §3.2: FOREX3* -> `0o1760`, LO*SYN -> `0o1551`, LO*GEN -> `0o1551`).
  `f0` is then XOR-compared with `0o1760` at `0o3046`; a mismatch runs the satellite-copy loop
  `0o3051..0o3052`.
* For the **main section, exactly `f0 = 0o1760` is required** (M4 §3.1: 0o1761/1757/1762/1770/
  1551/140/24/11/20/100/4027 -> `НЕТ РАЗДЕЛА OURMRK* 01770`; `f0=0` -> `СВОБОД 01770`).

### 3.2 Body at zone N+1 (FACT)

* `word0` = service word (live 4.12: `0o1600043`; our tests: 0).
* `word1..3` = DMS header:
  `w0 = head|sym<<12|debug<<36` (= `0o4657624570231200`, simultaneously TEXT `FOREX3*`),
  `w1 = set|data<<15|long<<30`, `w2 = cmd|bss<<15|const<<30`
  (`cmd=0o1760`, `const=0o222`, `bss=0`).
* `cmd[0]` (`word4`) = marker `0o73461`, common to FOREX3*, LO*SYN and LO*GEN.
* `cmd[1]` (`word5`) = `0o7240176003000464` = `уиа '1760'(М16) / пб '464'` — the 4.12 entry stub
  which sets the base register. Whether `пб 464` is absolute or relative to M16 is still open (§6).

### 3.3 Copy mapping (FACT, reconciled)

The copy loop `0o700..0o711` uses `M6` as receiver. The proven mapping from
`tests/plan-f77/66-newcomp-ourcode/README.md` is:

```
RAM address = 0o1757 + k        where k = 1-based word index in zone N+1
body[1]  -> RAM 0o1760  (= f0 = M16 base; DMS header starts here)
body[9]  -> RAM 0o1770  (our *64 2004 word; decimal 9 = octal 11: 0o1757+0o11 = 0o1770)
body[0o25] -> RAM 0o2004 (descriptor)
body[0o27] -> RAM 0o2006 (GOST '21 1.00 3.00')
```

This is consistent with `59-autonomous-body-plan.md` §A2 ("тело зоны N+1 копируется в ОЗУ с `0o1760`,
цикл `0o701-0o711`, M6 — приёмник"): the first body word (the service word, k=0) lands at `0o1757`,
the DMS header (k=1) at `0o1760`. All address fields in our test body were left **unchanged** precisely
because of this mapping, and the marker appeared at `0o1770` / `0o2004` / `0o2006` as predicted.

The loader reads a **continuous run of zones** `N+1, N+2, ...` (M4 §3.3: trace `DD pc=00671L z=1745`,
`DD pc=00744L z=1746`, ..., ~30 zones; live 4.12 has ~124 body zones). It is not a single-zone load.

### 3.4 Words required in N+2 (FACT + INFERENCE)

* **FACT (A1, plan 59):** the live zones actually executed are `N+2..N+7`, `N+9..N+28` plus nearly all
  of `N+1`; `N+8`, `N+29..N+40` are not needed.
* **FACT (A4, plan 59):** the essential range in `N+2` is **words 526..900 (375 words)**, which are
  *data* (masks/addresses/counters of the overlay loader), not code. Zeroing word 526 or 900 gives TIMEOUT.
* **FACT (test 66):** a working minimal installation used live words of `2148:0o1552` in `N+2` and
  zeros in `N+3..N+40`; our static GOST marker printed and `КОНЕЦ ЗАДАЧИ` followed.
* **INFERENCE:** N+2 is the overlay-loader table area for the resident compiler; NEWCOMP* itself does
  not interpret its contents, it simply copies them.

### 3.5 Where control goes (FACT + INFERENCE)

* **FACT:** the word at RAM `0o455` is `6710000202200000` = `vjm 64002(15)`, assembled at run time by
  the cycle `0o64415..0o64427` (59-C1). Patching it to `6711577002200000` = `vjm 1770(15)` redirects
  execution to RAM `0o1770` (the address identity `0o15770 + 0o64000 = 0o77770`, masked to `0o1770`).
* **FACT (B2, plan 59):** with only disk patches, `*TRANS` **never executes words of our body**;
  it reads the banner from the disk body and hands control to the resident compiler via
  `VJM 0o64002`. The compiled body is copied with a transformation, but control stays resident
  (CORE DIFF shows no GOST bytes from our body in executable RAM).
* **INFERENCE:** `VJM 0o64002` lands inside the resident 4.12 entry/loader table, not at the user's
  first Fortran statement. The exact landing instruction was never captured in the 90 000-instruction
  trace window (open question Q2).

---

## 4. FACT / INFERENCE markers — consolidated

| # | statement | marker | basis |
|---|---|---|---|
| 1 | zone-422 words 511..525 are the entry code at RAM 0o3000..0o3014 | **FACT** | direct disbesm6 decode + live-dump identity |
| 2 | scan (0o3033..0o3055) and loader (0o660..0o711) code arrive via `*70` disk 30 / 0o0050 | **FACT** | trace `DD pc=03006L ... u=30 z=0050`, live dump |
| 3 | descriptor fields f3/f2/f1/f0, f0 mask 0o7777, f0 XOR 0o1760 | **FACT** | trace, sweep |
| 4 | body[k] -> RAM 0o1757+k; body[9] -> 0o1770 | **FACT** | test 66 + A2 |
| 5 | `f0 = 0o1760` required for main; other f0 -> НЕТ РАЗДЕЛА | **FACT** | M4 full f0 sweep |
| 6 | `SHX 0o430(M14)` is the LINK route into NEWCOMP* | **FACT** | zone 200 word 200.0331 + A/B patch |
| 7 | M13 is the VJM linkage register in monitor MADLEN | **FACT** | `M13,VJM,...` in many *.asm; INITFO/PRINT8 |
| 8 | final transfer is `vjm 64002(15)` at RAM 0o455 | **FACT** | C1 patch + disassembly of built word |
| 9 | `cmd = 0o1760` and `f0 = 0o1760` are "main-section ID = load base" | **INFERENCE** | numerical identity + behavior; roles not separated by an experiment |
| 10 | f3/f2/f1 encode length/address/entry of the body | **INFERENCE** | shifts and masks observed, semantics not proven |
| 11 | N+2 words 526..900 are overlay-loader data tables | **INFERENCE** | zeroing changes behavior; content not decoded |
| 12 | M4/M10 roles in the secondary code island 0o1400..0o1410 | **INFERENCE** | code shape only |
| 13 | `пб 464` in the stub is absolute vs M16-relative | **UNRESOLVED** | see Q1 |

---

## 5. Commented MADLEN-style listing (annotated disassembly)

Style follows `re-siprod/madlen/BEGPG.madlen`: `C` header comments, `Mnn:,EQU,nnB` register block,
procedure boundaries, inline `.` comments. Two sources are interleaved and marked:
`[ZONE]` = disbesm6 of `zone422.bin` word 511+ (exact bytes, FACT);
`[LIVE]` = RAM dump + trace from `f77_30_m80_newcomp_live_disasm.txt` (FACT).

```
C =====================================================================
C NEWCOMP* -- MONITOR-80 *TRANS TRANSLATOR LOADER
C Нет исходника. Листинг собран из двух материалов:
C   [ZONE] reference/m80/zone422.bin, word 511.. -> RAM 0o3000..
C   [LIVE] RAM dump 0o3000..0o3077 / 0o640..0o711 + трасса
C Вход:  *TRANS:name,,41/N  (LINK: SHX 0o430(M14) -> stub)
C Выход: RAM 0o455 = vjm 64002(15) -> резидентный FOREX 4.12
C =====================================================================
 M1:,EQU,1B    (не используется)      M9:,EQU,11B   (не используется)
 M2:,EQU,2B    (не используется)      M10:,EQU,12B  блок вызывающего (островок 1400)
 M3:,EQU,3B    старшие поля дескр.    M11:,EQU,13B  второй канал возврата
 M4:,EQU,4B    счётчик (1400)         M12:,EQU,14B  буфер дескрипторов
 M5:,EQU,5B    база буфера дескр.     M13:,EQU,15B  указатель каталога / VJM-link
 M6:,EQU,6B    приёмник тела          M14:,EQU,16B  база каталога (копия M13)
 M7:,EQU,7B    (кадр, не здесь)       M15:,EQU,17B  адрес возврата пв
 M8:,EQU,10B   (не используется)      M16:,EQU,20B  мод.адрес / имя / база 1760
                                      M17:,EQU,21B  каталог задачи
C ---------------------------------------------------------------------
C P1 ENTRY -- сохранить возврат, распаковать параметр, [*70] докачать код
 3000 00 042 0015  счи М15            .сохранить M15 (возврат)          [ZONE]
      00 003 0017  счм 15             .СМ := M15, в магазин
 3001 00 036 0112  сда 64+10          .выделить биты параметра          [ZONE]
      00 036 0066  сда 64-10
 3002 00 040 0013  уи М13             .M13 := 0o6000 (буфер каталога)    [ZONE]
      13 25 02000  слиа '2000'(М13)   .M13 += 0o2000 -> 0o6000
 3003 13 044 0014  уии М14(М13)       .M14 := M13 (база каталога)        [ZONE]
      12 24 01146  уиа '1146'(М12)    .M12 := 0o1146 (буфер дескрипторов)
 3004 00 042 0013  счи М13            .СМ := M13; сда 64-20             [ZONE]
 3005 00 015 0424  или '424'          .собрать INF-слово                [ZONE]
      17 000 0001  зп 1(М17)          .каталог задачи 1(М17)=0o53405
 3006 17 070 0001  Э70 1(М17)         .*70: диск 30 / зона 0o0050       [ZONE]
 3007 16 24 02101  уиа '2101'(М16)    .M16 := строка поиска (D03064-1)  [ZONE]
      15 31 02051  пв '2051'(М15)     .вызов A03033
 3010 00 26 02077  по '2077'          .ошибка чтения                    [ZONE]
      16 24 02102  уиа '2102'(М16)
 3011 15 31 02051  пв '2051'(М15)
 3012 00 27 02032  пе '2032'          .ошибка чтения                    [ZONE]
      16 24 02106  уиа '2106'(М16)
 3013 15 31 02074  пв '2051'(М15)     .                                  [ZONE]
 3014 11 30 00000  пб (М11)           .выход через M11                   [ZONE]
C 3015..3077: литералы/таблицы (0o3076 = маска 0o7777, 0o3077 = 0o777777)
C ---------------------------------------------------------------------
C P2 CATALOG-READ -- читаем зону N каталога трансляторов            [LIVE]
 3020             asn 54 / aox 77     .INF = 0o0010030000411550
 3021             atx 1(17) / Э70 1(17) .*70: диск 41 / зона N (0o1550)
 3022             vtm 577(16)         .M16 := TARGET NAME (TEXT)
                / vjm 3033(15)        .переход в P3
C ---------------------------------------------------------------------
C P3 SCAN-DESCRIPTOR -- поиск имени и разбор f0                      [LIVE]
 3033             mtj 13(14) / utc 0  .M13 := M14 := начало каталога
 3034             xta 0(13)           .СМ := очередное имя
                / uza 0(15)           .нуль = конец каталога -> возврат
 3035             aex 0(16)           .СМ := имя XOR искомое
                / uza 3037            .0 = совпадение
 3036             utm 2(13) / uj 3034 .M13 += 2; следующая пара
 3037             xta 1(13)           .СМ := дескриптор
                / utc 3076            .М16 := маска 0o7777
 3040             aax 3076            .СМ &= 0o7777 -> f0
                / atx 1(17)           .f0 -> 0o53405
 3041             xta 0(13) / atx 0(12) .имя -> буфер M12
 3042             xta 1(13) / atx 1(12) .дескриптор -> буфер M12+1
 3043             utm 2(13) / utm 2(12) .M13 += 2; M12 += 2
 3044             xta 0(13) / uza 3055 .следующее имя; 0 -> выход
 3045             xta 1(13)           .его дескриптор
 3046             aax 3076            .выделить f0
                / aex 1(17) / uza 3055 .f0 XOR f0(эталон); равно -> выход
 3047             aex 1(17) / aex 1(13)
 3050             aex 1(13) / uza 3055
 3051             mtj 16(12)          .M16 := M12 - 0o1166
                / utm 76612(16)
 3052             v1m 3041(16)        .вернуться к копированию
 3055             xta 1(17) / uj 0(15).возврат; СМ = f0
C ---------------------------------------------------------------------
C P4 DECODE-AND-LOAD -- поля дескриптора -> INF -> чтение и копирование тела
 660             сч 1(М16) / сда 64+15 .дескриптор из 0o1153
 661             уи М3 / сда 64+15    .M3 := старшая часть -> ветвь 674
 662             зп (М17) / и 0752    .маска 0o37
 663             сда 64-5 / зп (М17)
 664             слц 35 / зпм 153
 665             сда 64-37 / слц 153
 666             зпм 153 / сда 64+5
 667             и 0753 / слц 146     .маска 0o777
 670             зп 145 / Э70 145     .*70: читать зону N+1 (0o1551)
 671             сч 3(М5) / зп 151    .f0 = 0o1760
 672             сч 4(М5) / зп 152
 673             уии М6(М5) / мода    .M6 := приёмник
 674             пио A00656+28(М3)    .ветвь по M3
 676             уи М11 / сда 64+15 / уим М12 / и 0750 ...
 700-711          цикл копирования    .M6 растёт; зоны N+1,N+2,...
C ---------------------------------------------------------------------
C P5 HAND-OFF -- слово собирается в RAM 0o455 циклом 0o64415..64427
 0455             6710000202200000   .vjm 64002(15) -> резидентный 4.12
                                      .патч C1: 6711577002200000 = vjm 1770(15)
C =====================================================================
C КОНЕЦ
```

### 5.1 Secondary code island in the zone (FACT, role INFERENCE)

The original `reference/m80/NEWCOMP_zone422.dis` also decodes one small island at `0o1400..0o1410`
(which the `[ZONE]` listing above does not include because it belongs to a different part of the file):

```
  1400 START пино '41053'(М16) / уиа 3(М5)
  1401 сч '261'(М10) / зп '4507'
  1402 сч 1(М4) / сда 64+15
  1403 и '263'(М10) / нтж '4427'
  1404 пе '41053' / пв '41155'(М15)
  1405 зп (М6) / сч 1(М4)
  1406 сда 64+41 / и '261'(М10)
  1407 пе '41003' / сч '272'(М10)
  1410 пб '41004'
```

It uses `M4` as a counter, `M5` as a base, `M6` as a destination, `M10` as the caller's block,
`M15` for a call and `M16` as modified address. It reads fields `0o261`/`0o263`/`0o272` of `M10`,
which matches the re-siprod convention "`M10` = block passed by caller" (`notes/registers.md` §2.1).
Its exact relationship to the `*TRANS` path is not established; it may be a name-parsing helper
loaded with the disk-30 fragment. This is the only evidence for M4/M10 roles in this program.

---

## 6. Open questions and the experiments that would settle them

| id | open question | status | settling experiment (all on **copies**) |
|---|---|---|---|
| **Q1** | Is `пб 464` in `cmd[1]` absolute `0o464`, or `M16(0o1760)+0o464 = 0o2244`? | UNRESOLVED (`object_format_spec` §8.1) | Live trace with `BESM6_MTR_LO=0o464` and `BESM6_MTR_HI=0o2300` around the hand-off; compare PC at the first instruction after the stub. A/B: patch `0o464` in the body to a distinctive `*64` print descriptor and see whether it fires. |
| **Q2** | Exact landing instruction of `VJM 0o64002` (never inside the 90 000-instruction window) | FACT of absence (`live_disasm` §6.1) | Re-run with `BESM6_MTR_LO=0o736`, `BESM6_MTR_SKIP` large, or trace 200K+ instructions after the copy loop; record the PC sequence `0o711 -> 0o455 -> 0o64002 -> ...`. |
| **Q3** | Semantics of `f3/f2/f1` (length / load address / entry?) | INFERENCE only | In a copy of zone `0o1550`, vary one 12-bit field at a time and observe the assembled INF word at `0o145` in the `*70` trace (`DD pc=00671L ...`). Map each field to the resulting disk/zone/count bits. |
| **Q4** | Why `f0 = cmd = 0o1760` (coincidence or one field reused?) | INFERENCE | Build a body whose `cmd` is `0o300` but whose descriptor keeps `f0=0o1760` and M16 stub stays `0o1760`; if it loads and runs, the two roles are independent. (M4 already showed `cmd` alone cannot substitute for `f0`.) |
| **Q5** | Are the scan/loader procedures really fetched from disk 30 / zone `0o0050` by the `*70` at `0o3006`? | FACT of the `*70` call, not of the *content* | `besmtool dump 2048 --start=0o0050 --length=1` (on a copy), then `disbesm6` and look for `mtj 13(14)/utc 0` and `aax 3076` at the offsets that the trace shows being executed; compare word-for-word with the live RAM region `0o3033..`. |
| **Q6** | Full meaning of the marker `0o73461` at `cmd[0]` | UNRESOLVED | A/B: replace it with zero / other values in a 4.12-format copy body and observe whether the banner still appears; trace the first read of `cmd[0]` to see which instruction consumes it. |
| **Q7** | Minimum required words in N+2 for a *fully autonomous* body | INFERENCE (526..900 needed for resident banner) | Iteratively zero ranges of `N+2` in copies while running our own emitter; the smallest set for which our marker still prints is the answer. Plan 59 A3/A4 already narrowed it to words 526..900. |
| **Q8** | Relation of the `0o1400..0o1410` island to the `*TRANS` path | INFERENCE | Set a trace breakpoint at RAM `0o1400` during `*TRANS`; if it is never hit, it belongs to another routine sharing the zone. |

---

## 7. Bottom line (one paragraph)

`NEWCOMP*` is **not** a DMS module with a source file: it is a resident Monitor-80 procedure whose
on-disk fragment sits in zone `0o422` (bytes at file word 511 onward decode exactly to RAM `0o3000..`).
Its entry saves `M15`, derives the catalog buffer `M13 = 0o6000` / `M14` and descriptor buffer
`M12 = 0o1146`, reads a loader fragment from disk 30, packs an INF word into task-catalog element
`1(М17) = 0o53405` and issues `*70` for disk 41 / zone `N`. The scan compares TEXT names by XOR,
extracts `f0 = descriptor & 0o7777`, requires `f0 = 0o1760` for the main section, then the body loader
decodes the remaining fields, reads the continuous zone run `N+1, N+2, ...` and copies it to RAM with
`body[k] -> 0o1757+k` (M6 receiver), so `body[9] -> 0o1770` and the descriptor/GOST land at
`0o2004`/`0o2006`. Control finally passes through the runtime-built word at RAM `0o455`,
`vjm 64002(15)`, into the resident 4.12 compiler. M13's role here is a catalog pointer; the
monitor-wide `M13,VJM` linkage convention is a different use of the same register. Every numeric
claim above is tagged FACT or INFERENCE, and §6 lists the discriminating copy-only experiment for
each unresolved point.
