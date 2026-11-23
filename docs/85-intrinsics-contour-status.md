# F77 intrinsics in the FOREX 4.13 reconstruction texts (FOREX 5.00)

> Статус главного агента: контурный путь `0o2350` + `*TRANS` подтверждён
> SIMH A/B/A (`21 -> 01 -> 21`), но сами ABS/SQRT/MOD/DSQRT **не встроены** в
> контур, intrinsic‑специфичного A/B нет → FAIL. C‑результаты только oracle.
> Дальше: вспомогательные модули с уникальными именами через `*perso`
> (по образцу pascal-re) на базе проверенного каталога `build_forex_perso.py`.

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
| Same deck under full BESM-6 SIMH, after the `2048` volume-card fix | **COMPLETES**: `КЗ(075)`, ACPU `4.0000 3.0000 1.0000 / 4.00000000+000` + `КОНЕЦ ЗАДАЧИ` |
| SIMH control deck (`HELLO`, no PERSO) | PASS: `HELLO WORLD` + `КОНЕЦ ЗАДАЧИ` |
| SIMH A/B (4 -> 104 etc.) | **FAIL / not demonstrated**: every SIMH variant printed the good values, although the identical disk image under C `dispak` gives the A/B values (§5) |

The earlier SIMH hang was caused by using host volume `2348` in the deck cards.
After the lead's fix (`docs/80-deck-2048.md`) and seeding a host file named
`2048`, the deck completes under SIMH and prints the correct four values.
However, changing OUR intrinsic implementation does not change the SIMH output,
so the SIMH A/B gate is **not** met. C results are not substituted for it.

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

For the SIMH `2048`-label re-run, the same compiled modules were also merged
into the base PERSO 0o2300 image (so only one `*PERSO` card is needed) and
written into a legal SIMH tagged image:

```sh
python3 work/merge_intr_into_base.py --libzone /tmp/fulltext_zone2400.bin \
    --out work/FOREX_INTR_2300_good.bin      # SHA 1634521c...7fce3f489
python3 work/merge_intr_into_base.py --libzone /tmp/fulltext_ab_zone2400.bin \
    --out work/FOREX_INTR_2300_ab.bin        # SHA c5759918...55dcc842582
python3 work/write_simh_zone.py --image work/FOREX_INTR_2300_good.bin \
    --out work/simh_intr_good_2048           # SHA 2a53de5d...a888dba4cb
python3 work/write_simh_zone.py --image work/FOREX_INTR_2300_ab.bin \
    --out work/simh_intr_ab_2048             # SHA ac7c948c...a840dc51c
```

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

## 5. Full BESM-6 SIMH acceptance after the `2048` card fix

### 5.1 What was wrong and what was changed
The lead's correction (`docs/80-deck-2048.md`) is decisive: the OS-visible volume
label is `2048`; `2348` is only a host filename. With deck cards naming `2348`,
the PERSO path hung and no job completed. The SIMH deck was rewritten to

```
ДИС 41(2048)^
ЛЕН 60(2048)^          (variant: ДИС 45(2048)^ + *PERSO:452300)
*PERSO:602300
*EXECUTE
```

and the md45 host file is named `2048`, seeded from our working image. The
stock `attach -n prn0/prn1` lines were kept unchanged. Before and after the
deck the driver issues `ДАЙ А0`, `ДАЙ А1`, `НОМВ` (both ACPU acknowledged
`ECTЬ`, `НОМВ` reported `HET`), and reads the device that actually printed
(`disks/output.txt`, prn0). The boot marker is `ДATA:` via `capture-pane`
only; input via `send-keys`; no live disk, tmux 0 or C patch.

### 5.2 Good build: SIMH COMPLETES with correct values
Case `v2048_good` (image `work/fulltext/2348` seeded as host file `2048`,
PERSO 0o2300 + 0o2400), console:

```
 ДATA:23.11.26 BPEMЯ:07.01.00
 ДАЙ А0 / ECTЬ ; ДАЙ А1 / ECTЬ ; НОМВ / HET
 sim> at vu0 .../deck_simh_2048.b6 ; d 6 1 ; d 5 10 ; set cpu req ; go
 B075-1 410300000000
 KЗ(075) 410300000000 07.01 M=108
```

ACPU (`evidence/simh_v2048_good.acpu.txt`):

```
     4.0000    3.0000    1.0000
   4.00000000+000
 КОНЕЦ ЗАДАЧИ        +000000000000⏨+00    0000000000001041
```

So the earlier "hang" verdict is superseded: with the correct volume card the
full SIMH OS compiles our deck and prints the right intrinsic values.

### 5.3 SIMH A/B: FAIL
The A/B image was tried in four independent ways, all on copies:

| case | md45 image / PERSO placement | deck | result |
|:--|:--|:--|:--|
| `v2048_ab` | `work/fulltext_ab/2348` (A/B library at 0o2400) | `*perso:602300` + `*perso:602400,cont`, LUN 60 | `4 3 1 / 4.00000000+000` |
| `v45_ab` | same | `ДИС 45(2048)^`, `*perso:452300/452400,cont` | `4 3 1 / 4.00000000+000` |
| `base_ab` | A/B modules merged into 0o2300, dense image written to md45 | single `*perso:602300` | `4 3 1 / 4.00000000+000` |
| `tagged_ab` | same merge written with a valid SIMH tagged zone header at logical 0o2300 | `ДИС 45(2048)^`, single `*perso:452300` | `4 3 1 / 4.00000000+000` |

Every case reached `KЗ(075)` and `КОНЕЦ ЗАДАЧИ`; the ACPU result is identical
to the good build instead of the expected `104 203 301 / 404`. Link map entries
(`ABS E 01076`, `SQRТ E 01107`, `МОD 01125`, `DSQRТ 01153`) are identical
between the good and A/B SIMH runs. Control proof that the images themselves
are correct: the **same** `v45_ab/disks/2048` file under C `dispak` prints
`104.0000 203.0000 301.0000 / 4.04000000+002`
(`work/c_from_simh/run.out`). Therefore the SIMH OS build resolves these
intrinsic calls to its own implementations and does not route them through the
PERSO library we installed, regardless of LUN or PERSO placement; the C-side
A/B is causal but cannot be reproduced under SIMH.

### 5.4 Forced-resolution experiment with UNIQUE names (decisive)

To remove any ambiguity with the system `ABS/SQRT/MOD/DSQRT` entries, the four
modules were rebuilt with names absent from the system library:
`OURABS`, `OURSQR`, `OURMOD`, `OURDSQ` (all 6 characters). Patched text copies:
`work/src_our_good.FTN` / `work/src_our_ab.FTN`; catalog of the compiled
library: `OURDSQ OURMOD OURSQR OURABS FOREX* LO*SYN`. The deck was changed to
`EXTERNAL OURABS,OURSQR,OURMOD,OURDSQ` and `A=OURABS(X)`, `B=OURSQR(X)`,
`C=OURMOD(X,3.0)`, `E=OURDSQ(DX)` (`work/deck_our.b6`). Under C `dispak` with
the very same image, good prints `4 3 1 / 4.00000000+000` and A/B prints
`104 203 301 / 4.04000000+002`, so the compiled modules and the deck are
correct.

Under SIMH (cases `our_good`, `wr_good`, `wr45_good`, `simh_clean_good`,
`clean2_good`, `clean2300_good`) every run reached `КЗ(075)` and `КОНЕЦ ЗАДАЧИ`,
but the ACPU link map reported:

```
 *PERSO:602300
 *** ДЛЯ ПРАВИЛЬНОЙ РАБОТЫ СИСТЕМЫ ИСКЛЮЧИТЕ
 *** ИЗ ЛИЧНОЙ БИБЛИОТЕКИ СЛЕД. ПОДПРОГРАММЫ:
                    PRINT8
                    FICMEMOR
                    STAR*
 ИСПОРЧЕН КАТАЛОГ РЕRSОNАL LIВRАRУ
 ...
   ОТСУТСТВУЕТ  OURABS
   ОТСУТСТВУЕТ  OURSQR
   ОТСУТСТВУЕТ  OURMOD
   ОТСУТСТВУЕТ  OURDSQ
```

The `-wr` variant of the mount card (`ЛЕН 60(2048-wr)^`) and the LUN45 variant
(`ДИС 45(2048-wr)^`, `*PERSO:452300`) were both tried; retraction from the lead
notes that `-wr` is irrelevant because the deck only reads PERSO. A clean
catalog containing only the four `OUR*` modules (no `FOREX*`/`LO*SYN`
duplicates) was also built (`work/build_clean_lib.py`,
`work/clean_our_good.bin` / `clean_our_ab.bin`) and installed both at 0o2400
and at 0o2300, written with `besmtool` and with explicit SIMH zone headers
(`work/write_simh_zone.py`). The monitor still printed
`ИСПОРЧЕН КАТАЛОГ РЕRSОNАL LIВRАRУ` and all four unique names remained
`ОТСУТСТВУЕТ`. Hence the SIMH OS never loaded our personal library at all;
this is stronger than the earlier "system wins the name" hypothesis: with
unique names there is no system entry to win, and the job cannot link.

Causal A/B under SIMH is therefore impossible in this OS build: the good and
A/B images differ in their compiled bodies and C `dispak` demonstrates the
`4 -> 104` change from the same bytes, but SIMH provides no result lines to
compare. This is reported as FAIL; the C result is not substituted.

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

BLOCKED: SIMH unique-name experiment shows ИСПОРЧЕН КАТАЛОГ PERSONAL LIBRARY and ОТСУТСТВУЕТ OURABS/OURSQR/OURMOD/OURDSQ, so our PERSO library is never loaded and SIMH causal A/B is impossible; C-dispak A/B is PASS 4/4.

## 9. Rebase onto the zone-2350 contour (user architecture correction)

The user corrected the architecture: the PERSO/LUN60 route is dead under SIMH
and the same-version system FOREX makes gold uninformative. The MAIN translator
must be OUR contour at 0o2350, invoked by `*TRANS:OURMRK*,,412350`; auxiliary
`*perso` modules are permitted but no `*FOREX`/`*FTN` translator card.

### 9.1 Contour-only path: PASS under SIMH, with A/B/A
We reused the parallel stage's proven image builder verbatim on copies
(`work/build_contour_simh.py`, copied from
`/tmp/.private/azizz/opencode/re-forex-413-io/work/build_contour_simh.py`):
logical zones 0o2350 = catalog (O412C words 0..15), 0o2351 = body (O412C
16..34 + O412D tail + overrides), 0o2352 = overlay (O412C 35..409),
0o2353 = zero; SIMH header `w0=(phys<<36)|0x038ca3c918`,
`w1=0x000005f1c7800000`, `w2=0x0000410300000000`, `w3` end-around-carry
checksum, data written as 6-byte LE + 2 tag bytes at byte 64. Earlier
hand-written headers produced `НЕТ СОВП.КС … 02350` / `ДРУГАЯ ДОРОЖКА`;
the reused builder fixes both.

Target deck (`work/deck_trans.b6`) contains ONLY
`ДИС 41(2048)^`, `ОЗУ 32^АЦП 32^`, `*NAME OURMRK`,
`*TRANS:OURMRK*,,412350`, a dummy `PROGRAM MAIN / END`, `*EXECUTE`.
No system compiler card, no PERSO card. SIMH runs (stock `-n prn0/prn1`,
`ДАЙ А0`/`ДАЙ А1`/`НОМВ` before and after, `ДATA:` boot marker,
capture-pane only, copies only):

| case | image SHA-256 (first 16) | patched word | ACPU result |
|:--|:--|:--|:--|
| baseline | `a98e81090d4b2545` | none | `21 1.00 3.00` |
| A/B | `1f4431d177e02481` | body[0o41] = 0 | `01 1.00 3.00` |
| restore | `a98e81090d4b2545` | none | `21 1.00 3.00` |

All three runs were executed and reached `КОНЕЦ ЗАДАЧИ`; the restore run used the byte-identical baseline image (SHA `a98e81090d4b2545`) and reproduced `21 1.00 3.00`. This proves decisively that under the full
BESM-6 SIMH OS the printed value comes from OUR zone-2350 contour code, with a
causal A/B/A, and that no system FOREX participates.

### 9.2 Intrinsic extension: FAIL (not completed)
The four intrinsics were NOT integrated into the contour body in this session.
The contour's existing GOST digit builder emits the constants `1.00/3.00`;
replacing them with computed `ABS/SQRT/MOD/DSQRT` values requires BESM-6 raw
`*50` arithmetic plus float -> packed-GOST conversion inside the 1024-word
body/overlay. The earlier decisive finding
(`/tmp/.private/azizz/opencode/re-forex-intrinsics/report.md`) records that
this conversion needs about six constants/cells, only seven 12-bit-addressable
cells exist, and high-RAM constants are not reachable by the 15-bit ADR field.
No intrinsic-specific contour word was patched, so there is no honest
BLOCKED: zone-2350 *TRANS contour is PASS with SIMH A/B/A (21 -> 01 -> 21), but ABS/SQRT/MOD/DSQRT were not integrated into the contour, so the intrinsic A/B goal is not met.
