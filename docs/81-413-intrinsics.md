# F77 intrinsics in the FOREX 4.13 reconstruction texts (FOREX 5.00)

> Предисловие главного агента: C‑часть действительно собрана из наших текстов и
> даёт A/B 4/4, но SIMH‑гейт не пройден. Возможная причина hang’а — старые карты
> с `2348`; все три субагента перезапущены с картами `2048`/`2048-wr` и исправленным
> `attach -n prn0/prn1`. Пока SIMH A/B не получен, результат считается FAIL по
> главной цели («только наш компилятор»). Ни один host‑результат в счёт не идёт.

Date: 23.11.2026. All authored files, disk copies and evidence live only under
`/tmp/.private/azizz/opencode/re-forex-413-intrinsics/` (texts) and
`/var/tmp/re-forex-413-intrinsics-simh/` (SIMH images). No repository file was
edited, no git write, no live disk/tmux-0 use, no dispak C patch. All disks
attached to SIMH were workspace copies; the live `~/.besm6/2348` and
`/usr/local/share/besm6/2048` were unchanged at handoff (§8).

## 0. Verdict

| stage | result |
|:--|:--|
| Extension points located in the 4.13 texts | PASS (§1, §6) |
| Intrinsic library text patched on a COPY and compiled by SYSTEM FOREX from OUR PERSO 0o2300 | PASS (§3) |
| Installed into working 2348 copies at PERSO 0o2300 + 0o2400 | PASS (§3) |
| Real Fortran deck with `ABS/SQRT/MOD/DSQRT`, C `dispak`: correct values + A/B | **PASS 4/4** (§4) |
| Same deck under full BESM-6 SIMH | **FAIL** (§5): no `КОНЕЦ ЗАДАЧИ`, ACPU contains only the system footer |
| SIMH control deck (`HELLO`, no PERSO) | PASS: `HELLO WORLD` + `КОНЕЦ ЗАДАЧИ` (proves the harness, ACPU and system compiler path are healthy) |
| SIMH A/B for the four intrinsics | **NOT OBTAINABLE**: every deck containing `*PERSO:602300` hangs in this SIMH OS build (§5) |

Therefore the C-side implementation is complete and causal, but the mandatory
SIMH acceptance gate is **not** met. This is reported as FAIL, not papered over
with the C result.

## 1. Exact extension points in the 4.13 texts

### 1.1 Function-name recognition (lexer / token path, `LO*SYN`)
- `src/LO_SYN.mad:20-38` - module `LO*SYN` and the external names it exchanges
  with the resident root (`FOREX`, `CONST`, `COMEQ`, `OPRTR`, `ПP`, `LOADAN`).
- `src/LO_SYN.mad:789` - word 0007, resident extractcode `*63` (`Э63`, argument
  `0274`), one of the lexical/syntax entry points used by the automaton.
- `src/LO_SYN.mad:3312-3846` - syntax-automaton transition/action table,
  relative words `1517..1777` (abs `0o243217..0o243477`). This is the only
  recognition table inside the overlay.
- `docs/plan-f77/02-extension-points.md:151-161` - a new lexeme needs the
  resident `Э20` token extractor plus this table; the table is data inside a
  1024-word dump, so an edit breaks the byte-exact check.
- Scan of all 1024 words of both overlays (`evidence/overlay_text_scan.txt`)
  finds **no** TEXT word containing `ABS`, `SQRT`, `MOD`, `SIN`, `COS`, `EXP`,
  `ATAN` or `DSQRT`. Intrinsic names are not recognised by these tables;
  function-style names go through the resident compiler as ordinary externals.

### 1.2 Call generation (`LO*GEN` operator table / FT* chain)
- `src/LO_GEN.mad:19-40` - module `LO*GEN` and its external root procedures.
- `src/LO_GEN.mad:773,800,815,848,971,986,1001,1100,1181,1205,1238,1250,1265,
  1283,1748,1766,1769,...` - the `VJM,JT18CK` / `JT0W2U` / `JT0WMA` chain:
  the generator is linear, every block calls a resident helper, no internal
  labels.
- `src/LO_GEN.mad:504-532` and `src/LO_GEN.mad:1584-1699` - the operator-name
  table at relative `0532..0623`: 29 pairs `descriptor
  (0o0000000000020005) + TEXT name` (`POWER`, `A/RHOCHI`, `A/NOT`, `A/AND`,
  `FT*/FD*/FC*`, `*REWIN`, `*BACKS`, `*ENDFI`, `STOP*`).
- `docs/plan-f77/02-extension-points.md:77-96,148-161,199-215,327` - this is a
  table of *internal* names, not Fortran keywords and not the intrinsic path;
  adding a pair costs 2 words from a fully packed table.

### 1.3 Runtime implementations (LIBREFER / FORTLIBR / PERSO)
- `src/FOREX_RUNTIME.mad:121-189` - `FORMAT`/`FTDISP`, 11 transfer pairs
  `UJ FT*nnn / ATX 77xxxB` (`FT*571..FT*003`).
- `src/FOREX_RUNTIME.mad:194-325` - `FORTLIBR`/`FTLIO`, `PRINT8`, `WRTLBR`,
  the `PU 0o2000` buffer and ISO/GOST assembly.
- `src/FOREX_RUNTIME.mad:330-427` - `DATAPR*`; `src/FOREX_RUNTIME.mad:433-519`
  - `OCTTDEC`, number to 6 ISO digits.
- `docs/plan-f77/02-extension-points.md:203-217,303-330` and
  `docs/plan-f77-full/12-intrinsics-coverage.md:12-36` - a function-style name
  is an external reference resolved by the linker through a library catalog;
  no overlay edit is needed.
- `reference/expect_library21.txt` contains no `ABS/SQRT/MOD/DSQRT` entry;
  the system permanent-library link cells are `ABS E 07422`, `SQRT E 07433`
  (`logs/f77_intrinsics_coverage.txt:47`). `MOD` is lowered inline.
- `src/f77libr/F77LIB.FTN` - the F77LIBR Fortran text; its patched COPY is
  `work/F77LIB_intr.FTN` (§3).

## 2. Minimal first set and provenance

| intrinsic | mechanism available in 4.13 texts | what we did | etalon proof | C status |
|:--|:--|:--|:--|:--|
| `ABS` | existing system external `ABS E 07422` **and** inline lowering; can be a small Fortran routine in F77LIBR | `FUNCTION ABS(X)`, pure BESM arithmetic, compiled by SYSTEM FOREX; deck uses `EXTERNAL ABS` to force the external call | `logs/plan_f77_probes.txt`, matrix K19; deck result 4.0000 for -4.0 | **PASS** (A/B 4 -> 104) |
| `SQRT` | existing system external `SQRT E 07433`; small Fortran routine (`X**0.5`) | same, `EXTERNAL SQRT` | matrix K78; deck 3.0000 for 9.0 | **PASS** (A/B 3 -> 203) |
| `MOD` | inline lowering in the 4.13 compiler; small Fortran routine `X-Y*AINT(X/Y)` (uses proven `AINT`) | same, `EXTERNAL MOD`; AINT is documented in `docs/plan-f77-full/10-implementation-libr.md:99` | matrix K23; deck 1.0000 for (7,3) | **PASS** (A/B 1 -> 301) |
| `DSQRT` | external call (`ПВ DSQRT ('15')` in compiled listing), no system entry in LIBREFER; small DP Fortran routine `X**0.5D0` | same; decisive **without** `EXTERNAL` too | K79, `docs/plan-f77-full/16-k-closure.md:48,56`; deck 4.00000000+000 for 16D0 | **PASS** (A/B 4 -> 404) |
| `SIN`, `COS`, `EXP`, `ATAN2` | system externals (`SIN E 07441`, `EXP E 07417`, `ATAN E 07436`) or tiny Fortran wrappers | attempted with truncated Taylor / `ATAN(X/Y)` wrappers (§4.3) | matrix K54,K58,K69,K66 | SIN/COS/ATAN2 PASS, EXP PARTIAL |
| `LOG` | system native (`LOG` has no external reference) | wrapper via `ALOG`, `ALOG10` and a direct series all printed `0.0000` in our A/B deck | matrix K71 | **FAIL** under this mechanism |

No new hand-written machine code was needed: SYSTEM FOREX emits all BESM-6
instructions from the patched Fortran text. Without the `EXTERNAL` statement
the compiler keeps its native inline lowering for `ABS/SQRT/MOD`, and changing
our library has no effect (measured: v1 and A/B both printed `4 3 1`); with
`EXTERNAL` all four calls are routed to OUR compiled bodies. `DSQRT` is already
an external call and is decisive in both cases.

## 3. Patched text copies, rebuild and install

Files (all on copies):
- `work/F77LIB_intr.FTN` - verbatim copy of `src/f77libr/F77LIB.FTN` (116
  lines) + 21 appended lines. Exact patched lines:
  - `:118` `C---- FOREX 5.00 F77 INTRINSIC EXTENSION (COPIED TEXT, 4 entries) ----`
  - `:120-124` `FUNCTION ABS(X)` / `ABS=X` / `IF (X .LT. 0.0) ABS=-X` / `RETURN` / `END`
  - `:125-128` `FUNCTION SQRT(X)` / `SQRT=X**0.5` / `RETURN` / `END`
  - `:129-132` `FUNCTION MOD(X,Y)` / `MOD=X-Y*AINT(X/Y)` / `RETURN` / `END`
  - `:133-137` `DOUBLE PRECISION FUNCTION DSQRT(X)` / `DOUBLE PRECISION X` /
    `DSQRT=X**0.5D0` / `RETURN` / `END`
- `work/F77LIB_intr_ab.FTN` - A/B variant; the four result assignments are
  `ABS=ABS+100.0` (`:126`), `SQRT=X**0.5+200.0` (`:130`),
  `MOD=X-Y*AINT(X/Y)+300.0` (`:134`), `DSQRT=X**0.5D0+400.0D0` (`:138`).
- The overlays/root/runtime texts were used verbatim (no patch): their dumps
  `build/LO_SYN.words` (`83a7e962...8459366`) and `build/LO_GEN.words`
  (`4f4d8e4c...222cbfd`) are unchanged, so the 1024-word invariant holds.

Rebuild (SYSTEM FOREX compiles the patched Fortran text; 0o2300 is OUR base
image built from the 4.13 texts by `tools/build_forex_perso.py`):

```sh
cd /tmp/.private/azizz/opencode/re-forex-413-intrinsics
python3 work/try_catalog.py --out work/fulltext --src work/F77LIB_intr.FTN --zones 8
python3 work/try_catalog.py --out work/fulltext_ab --src work/F77LIB_intr_ab.FTN --zones 8
```

`try_catalog.py` uses the proven deck of `tests/run-f77-runtime.sh:64-78`:
`лен 60(2348-wr)^`, `*call yesmemory`, `*perso:602300`, `*forex`, the patched
source, `*to perso:602400`, `*end file`; the SYSTEM FOREX object modules are
assembled into a fresh COPY of disk 2348. The compile logged (good / A/B):

```
ДЛИНА ПОДПРОГРАММЫ АВS 00017 / 00021
ДЛИНА ПОДПРОГРАММЫ SQRТ 00016 / 00017
ДЛИНА ПОДПРОГРАММЫ МОD 00032 / 00034
ДЛИНА ПОДПРОГРАММЫ DSQRТ 00022 / 00025
ДЛИНА LIВRАRУ 004 ЗОН
```

Catalog at 0o2400 (both variants):
`DSQRT MOD SQRT ABS DINT2 DMOD2 ISTRCM SUBSTR STRCAT STRCMP IDIV ISGN0 IMAX0 FMTLNK MYMAX MYABS FOREX* LO*SYN`.

SHAs:
```
10f94eb7...5571eb  work/F77LIB_intr.FTN
a8b251a7...58e760  work/F77LIB_intr_ab.FTN
0bd8e586...87f7877a83  build/FOREX_PERSO_2300.bin (unchanged input)
d49cfe10...374e90b  work/fulltext/2348        (good disk)
60eddb14...840a551f  work/fulltext_ab/2348     (A/B disk)
3b599862...631fb9  work/fulltext/libzone.bin  (0o2400 good)
416544a7...c176f3  work/fulltext_ab/libzone.bin (0o2400 A/B)
9b30f41d...1a478   work/intr_deck3.b6          (C deck)
efd94817...8104957  work/deck_simh.b6          (SIMH deck)
```
Full 64-hex values are in `evidence/final_shas.txt` and
`evidence/artifact_shas.txt`.

## 4. C `dispak` acceptance (built with the system compiler, executed by `dispak`)

Deck `work/intr_deck3.b6` (excerpt): `*perso:602300`, `*perso:602400,cont`,
`*forex`, `EXTERNAL ABS,SQRT,MOD,DSQRT`, `A=ABS(-4.0)`, `B=SQRT(9.0)`,
`C=MOD(7.0,3.0)`, `E=DSQRT(16.0D0)`, `PRINT 1000` (`3F10.4`), `PRINT 1001`
(`D16.8`). Command:

```sh
cd work/fulltext && cp ../intr_deck3.b6 job.b6 && echo job.b6 > options.txt
BESM6_PATH="$PWD:/usr/local/share/besm6" \
  /home/azizz/Yandex.Disk/dispak/build/dispak/dispak job.b6 > run.out
```

| case | ACPU result block | verdict |
|:--|:--|:--|
| good | `4.0000    3.0000    1.0000` / `4.00000000+000` | correct for all four |
| A/B | `104.0000  203.0000  301.0000` / `4.04000000+002` | all four changed |
| restore = good SHA | same as good | PASS |

The compiled listing (`work/fulltext/runfull.out`) shows the real BESM-6 call
chain: `ПВ DSQRT ('15')`, then `ПВ FТ*571`, `FТ*002`, `FD*002`, `FТ*003` for
`PRINT` - i.e. the runtime output path is the system FORMAT/FORTLIBR machinery,
not host code.

### 4.3 Additional intrinsics (attempted)
Deck `work/deck_more.b6` with `EXTERNAL SIN,COS,EXP,LOG,ATAN2`, library
`work/more3`: `0.4794 0.8776 1.6458 0.0000 0.4636`. `SIN(0.5)` and `COS(0.5)`
match the etalons; `ATAN2(1,2)` gives the proven `0.4636`; `EXP(0.5)` is a
truncated-series approximation (PARTIAL); `LOG(2.0)` prints `0.0000` with all
three attempted bodies (`ALOG`, `ALOG10`, direct series) and is FAIL. None of
these five was re-run under SIMH.

## 5. Full BESM-6 SIMH acceptance: FAIL

Driver: `work/drive_simh.py` (isolated `TMUX_TMPDIR`, capture-pane only,
`send-keys`, `ДATA:` boot marker, no `CM1П`/`sim>` boot wait). Ini generator:
`work/make_simh_ini.py`. Fixed ini lines actually used (stock `-n` form kept,
per the operator fix):

```
attach -e md41 /var/tmp/re-forex-413-intrinsics-simh/finalgood/disks/sys2048_on_md41   # COPY of /usr/local/share/besm6/2048
attach -e md45  /var/tmp/re-forex-413-intrinsics-simh/finalgood/disks/work2348_on_md45  # COPY of work/fulltext/2348
attach -n prn0 /var/tmp/re-forex-413-intrinsics-simh/finalgood/disks/output.txt
attach -n prn1 /var/tmp/re-forex-413-intrinsics-simh/finalgood/disks/output1.txt
load /var/tmp/re-forex-413-intrinsics-simh/finalgood/boot_dispak.b6
```

Boot/deck sequence (from `evidence/simh_finalgood.log`):
`ДATA:23.11.26 BPEMЯ:06.51.00` seen; `ДАЙ А0` -> `ECTЬ`, `ДАЙ А1` -> `ECTЬ`,
`НОМВ` -> `HET` (empty output queue); `Ctrl+G`, `at vu0 <deck>`, `d 6 1`,
`d 5 10`, `set cpu req`, `go`; console then shows only
`B075-1 410300000000  2348`, then `НОМВ` -> `HET`, and **no** `КОНЕЦ ЗАДАЧИ`,
`КЗ(...)` or `СБОЙ` line. prn0 = 1669 bytes containing only the system footer
(`... ИТМ И ВТ ... *АЦПУ-0 ... 555...`), no result block.

Control: the same harness with `work/hello.b6` (no `*perso`) printed
`HELLO WORLD` and `КОНЕЦ ЗАДАЧИ` (`evidence/simh_hello.log`). Decreasing
diagnostics: `work/simple_perso.b6` (`*perso:602300` only) and
`work/simple_perso_noyes.b6` (no `*call yesmemory`) both hang the same way.
So the blocker is the `*PERSO:602300` path in this SIMH OS build, not our
intrinsic library, the ACPU devices or the deck reader. The same failure was
observed independently in `/tmp/.private/azizz/opencode/re-forex-413-baseline/report.md`
§5. Consequently SIMH A/B for `ABS/SQRT/MOD/DSQRT` could not be produced; the
C A/B in §4 is the only causal evidence, and it is **not** substituted for SIMH.

## 6. Word-budget evidence (why no overlay edit was needed or possible)

- `LO*GEN:0532..0623` = `0o623-0o532+1` = `0o72` = 58 words = exactly 29
  descriptor+TEXT pairs, no free slot (`docs/plan-f77/02-extension-points.md:160-161`).
  Adding even one internal operator requires repacking all 29 pairs and every
  displacement that refers to them.
- `LO_SYN:1517..1777` = `0o261` = 177 words, fully populated inside the
  1024-word dump; `tests/check-source-words.py` requires all 1024 words of
  each overlay to match its dump byte-for-byte.
- Our solution adds **zero** words to either overlay. All four intrinsics are
  ordinary function-style names resolved at link time; the implementation is
  a separate Fortran text compiled by SYSTEM FOREX into a separate PERSO
  library at 0o2400, installed next to the unchanged 0o2300 compiler library.

## 7. Avoiding the abandoned hand-built contour path

The abandoned zone-2350 work (`/tmp/.private/azizz/opencode/re-forex-intrinsics/report.md`)
proved the raw extractcodes but showed float -> packed GOST is blocked in a
58-word hand-built contour: about six constants/cells are needed, only seven
12-bit-addressable cells exist, high-RAM constants are unreachable by the
15-bit ADR field, `FT*571/002/003` are unavailable under `*TRANS`, and `*50 15`
is unimplemented in `dispak`. We did **not** repeat that path. Instead the
float result is produced by SYSTEM FOREX from ordinary Fortran (`X**0.5`,
`X**0.5D0`, `X-Y*AINT(X/Y)`) and float -> GOST conversion is delegated to the
existing, proven runtime text `src/FOREX_RUNTIME.mad:121-189` (`FORMAT` and its
11 `FT*` transfer cells) and `:433-519` (`OCTTDEC`). The compiled listing
(`work/fulltext/runfull.out`) shows exactly the reuse: `ПВ FТ*571`, `FТ*002`,
`FD*002`, `FТ*003` for both `F10.4` and `D16.8` output. No hand-written
digit-weight cell, high-RAM constant or `*50 15` is involved.

## 8. Safety record

- Early in the experiment a relative `BESM6_PATH` entry in `try_catalog.py`
  caused `besmtool write`/`dispak` to resolve `2348` to the system etalon
  `/usr/local/share/besm6/2348` and write there. This was detected by SHA/mtime
  checks, the harness was changed to use absolute paths with an etalon guard,
  and the file was restored from the pre-task snapshot (SHA `5f0b415c...`).
  During the later task window that file was independently set to
  `f15f25133294c2c3a894f50c85c9c9c7567c0a3eef8ef01b34d1dd2792cc31cd` by another
  actor; the final SHA is that documented value. `~/.besm6/2348` and
  `/usr/local/share/besm6/2048` stayed byte-identical to the pre-SIMH record.
- All SIMH md41/md45 images were workspace copies; no live disk, tmux session
  0 or dispak source was touched. All SIMH/tmux processes started by this task
  were stopped at handoff; obsolete scratch disk copies were removed.

BLOCKED: SIMH acceptance of the PERSO-based intrinsic deck fails in this OS build (no КОНЕЦ ЗАДАЧИ, ACPU only system footer), so SIMH A/B for ABS/SQRT/MOD/DSQRT could not be obtained; C-dispak build and A/B are PASS 4/4.
