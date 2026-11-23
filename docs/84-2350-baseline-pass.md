# FOREX 5.00 from the 4.13 texts: baseline inventory, rebuild proof, A/B, extension points

Workspace: `/tmp/.private/azizz/opencode/re-forex-413-baseline` (all writes).
Disk copies: `/dev/shm/re-forex-413-baseline/`.
Repository, `/usr/local/share/besm6/*`, `~/.besm6/2348`, tmux 0: read-only / untouched.
No git writes, no dispak C patches, no host-side Python codegen in the target path.
Date: 2026-11-23.

> ГЛАВНЫЙ РЕЗУЛЬТАТ (продукт, подтверждено главным агентом): baseline **PASS**
> на контуре зоны `0o2350`, собранном из текстов 4.13 (`O412C.FTN`,
> `o412d_words.hex`, `ovl_our.hex`, `installer.py`). Дек вызывает **только**
> `*TRANS:OURMRK*,,412350`. SIMH A/B/A: baseline `a98e8109…` ->
> `21 1.00 3.00`; обнуление `body[0o41]` (`1f4431d1…`) -> `01 1.00 3.00`;
> restore -> исходное; no-install -> `ОТСУТСТВУЕТ OURMRK*`. Печать идёт из
> нашего контура, системный ФОРЭКС в пути отсутствует. PERSO‑путь откатан.


## 0. Verdict up front

| Question | Answer |
|---|---|
| Do the authoritative 4.13 texts exist and are they byte-verified? | **YES** (§1, §1.2) |
| Can the PERSO image be rebuilt from texts on copies and installed byte-identically? | **YES** (§3), SHA `0bd8e586…53b` |
| Does C `dispak` produce gold-like output with `*perso:602300` + `*forex`? | **YES**, 14/14 result lines (§4) |
| Does full BESM-6 SIMH produce that output with `*perso:602300` and our rebuilt image installed? | **YES** with the volume-corrected recipe (§5.3): gold 14 lines + `КОНЕЦ ЗАДАЧИ`, ACPU 34,011 B. The earlier `СБОЙ АЦПУ0` was our ini (prn attached after boot); the later `НЕЗАК.МЛ` was the wrong `2348` volume card. |
| Does A/B prove the *rebuilt* compiler (not the system binary) produced the output? | **NO** (§6.3): under that same recipe, patching `RUNTIME_FORMAT` word 46 (byte-identical to the parallel stage's `bb46fe75…`), `F003DS`, or a root code word leaves the output byte-identical; the no-PERSO control also prints the same gold. Verdict stays **FAIL**. |
| Can F77 extensions be located in the texts? | **YES**, concrete anchors in §7 |
| **PRODUCT: zone-0o2350 contour built from the 4.13 texts, `*TRANS:OURMRK*,,412350` only** | **PASS** (§9): SIMH ACPU `21 1.00 3.00`; zeroing one contour word gives `01 1.00 3.00`; restore returns `21 1.00 3.00`; no-install prints `ОТСУТСТВУЕТ OURMRK*`. |

The PERSO/LUN-60 route is **dead for the product** (a same-version system FOREX makes its
gold output uninformative; the runtime-text A/B there was retracted). The user's final
architecture is the contour at zone `0o2350`, invoked by `*TRANS:OURMRK*,,412350` with no
system-compiler card. That path is now proven PASS under full SIMH (§9). Earlier sections
remain as the inventory and as the audit trail of why PERSO was rejected.

## 1. Authoritative text inventory

All files below are read-only in the repo. Hashes are of the files as read on 2026-11-23.

| File | Lines | SHA256 (first 16) | Role | Version evidence | Compile status under system tools |
|---|---:|---|---|---|---|
| `reference/libra211.forex.inc` | 81 | `d18f35494a2b5007` | ROOT, authoritative 4.13 source (Dubna `libra211.l21:15448-15528`; `INITFOR*`, `LOREX`, `RMON`, `STOP/`) | 4.13, 11.09.85 | Assemblable MADLEN; used indirectly through derived relocatable text (§3) |
| `src/reloc/FOREX_ROOT.reloc.mad` | 78 | `efe04c36def76f72` | ROOT, relocatable reworking of the above (LC→BSS, renamed externals, `FXLODR`) | derived from 4.13 root | **compiled** by Monitor-80 `*assembler` in `tools/build_forex_perso.py` |
| `include/FOREX_ROOT.mad` | 300 | `a72fef40c17cdecf` | ROOT, annotated MADLEN text (absolute tape addresses, `; Sx:nnnn` provenance); includes `GIV/PG` at :198-254 | 4.13 root + 2.02 load map | annotated disassembly, **not** directly assemblable |
| `src/FOREX_CORE.mad` | 648 | `70d849e02d7e6d7e` | ROOT, annotated resident core (`0o510300..0o510437`, 96 words) | 4.13 root + monsys.9 | annotated disassembly, **not** directly assemblable |
| `src/LO_SYN.mad` | 3847 | `66e2acb80f9a5775` | OVERLAY `LO*SYN`, annotated MADLEN, 1024 words | monsys.9 `0o241500` | annotated disassembly; compiled body taken from byte-exact dump |
| `src/LO_GEN.mad` | 3566 | `19e57c22dcb91ded` | OVERLAY `LO*GEN`, annotated MADLEN, 1024 words | monsys.9 `0o277500` | annotated disassembly; compiled body taken from byte-exact dump |
| `src/FOREX_RUNTIME.mad` | 569 | `1b739f77ed7fda66` | RUNTIME annotated text (FORMAT, FORTLIBR, DATAPR*, OCTTDE) | Dubna 4.13 sources | annotated; bodies partly tape dumps, partly assembled from authoritative slices |
| `reference/libra211.format.inc` | 202 | `7252ab92624984ed` | RUNTIME verbatim source `libra211.l21:15529-15712` (FORMAT + FORTLIBR) | 4.13 | assemblable Dubna MADLEN |
| `docs/08-forex3.md` | 204 | `a08c944b79b68128` | report: FOREX3* branch / 4.12 banner analysis | 4.12 | n/a |
| `docs/06-core-modules.md` | 225 | `73959e77b90dcab5` | report: root/core boundaries, 412 banner | 4.13/412 | n/a |
| `docs/07-runtime.md` | 142 | `8c36086691a3353e` | report: runtime recovery boundaries | 4.13 | n/a |

External authoritative inputs (not copied into the repo):
`/usr/local/share/besm6/2348` (SHA `f15f25133294c2c3…` on this machine),
`/home/azizz/besm6.github.io/sources/dubna/besml21/libra211.l21` (`b98b7e8f…`),
`…/besmmons/system1.txt`, `monsys.9` (`e26a2036…1118b`).

### 1.1 4.12 versus 4.13: do not silently mix

- Overlay bodies come from `monsys.9` words `0o241500` (`LO*SYN`) and `0o277500` (`LO*GEN`).
- The tape's service area at word `0o201762` reads, verbatim (read 2026-11-23):
  `OVERLAY OT  27/04/87     FOREX 412`.
- `docs/PLAN.md:19`, `docs/06-core-modules.md:68`, `README.md:48` classify this as a
  **monitor service message, not overlay code and not an in-module version stamp**.
- Therefore the overlays **cannot be asserted to be 4.13**. They are byte-exact compiled
  bodies from a tape whose service banner says FOREX 412. The 4.13 semantic base rests on
  the root source `libra211.forex.inc` and the gold `reference/expect_forex.txt`, not on
  that banner. **This build is a hybrid**: 4.13 root text + monsys.9 overlay binaries
  (412-labelled carrier) + Dubna runtime sources. System 2.02 remains the host tool; its
  banner `ВЕРСИЯ 2.02 ОТ 15.07.80` is external to our image (`docs/16` §6).
- `docs/08-forex3.md:143-163` documents a separate `FOREX 4.12 ОТ 25.06.85` reached via
  `*TRANS:FOREX3*,,411550` on disk 2148. It is a different branch and is **not** used here.

### 1.2 Byte-verification evidence (run 2026-11-23, rc=0)

```
$ python3 tests/check-source-words.py
OK LO*SYN: все 1024 слова совпадают с дампом
OK LO*GEN: все 1024 слова совпадают с дампом

$ ./tests/verify-dumps.sh
LO_SYN offset=0o241500  size=6144   sha256=83a7e962a9db89e62b856b7461ce2aba91239957931a03e1520fb4d228459366
       побайтовая сверка с build/LO_SYN.words: OK
LO_GEN offset=0o277500  size=6144   sha256=4f4d8e4cc8fff1ec9742fe8be0a0c5f797716ab1bd085a1625d37569d222cbfd
       побайтовая сверка с build/LO_GEN.words: OK
OK: оверлеи LO*SYN и LO*GEN выгружены и сверены
```

## 2. What "compiled by the system compiler" means for these texts

The authoritative compiler sources are MADLEN autocode; the system FOREX 2.02 is a
**Fortran** compiler. The system tool that assembles our texts is Monitor-80
`*assembler` through `dispak`. There is no host-side Python codegen in the target path:
`tools/build_forex_perso.py` only wraps and places compiled/assembled BESM-6 words.

Modules actually **assembled from texts** by `*assembler` in the default build:
`FOREX*` (from `src/reloc/FOREX_ROOT.reloc.mad`, derived from the 4.13 root),
`XDATAPR` (Dubna `system1.txt` slice), `XGIVPG`/`XTAKPG` (`libra211.l21:16780-16836`).
Modules taken as **byte-exact compiled dumps**: `LO*SYN`, `LO*GEN`, `FORMAT`,
`FORTLIBR`, `OCTTDE*`.

The annotated overlay texts are **not assemblable as-is**: they carry absolute-address
columns and `; (POLN: …)` annotations (e.g. `src/LO_SYN.mad:60-77`). A cleanup/symbolic
rewrite would be required before `*assembler` could compile them; that work does not yet
exist (`src/reloc/README.md:3-11`).

## 3. Minimal reproducible build chain (all on copies)

```
BASE=/tmp/.private/azizz/opencode/re-forex-413-baseline
SHM=/dev/shm/re-forex-413-baseline
cp <repo>/tools/build_forex_perso.py              $BASE/repo-copy/tools/
cp <repo>/src/reloc/*.mad                         $BASE/repo-copy/src/reloc/
cp <repo>/build/*.words                           $BASE/repo-copy/build/
cp <repo>/tests/forex-glissade/*                  $BASE/repo-copy/tests/forex-glissade/
cp /usr/local/share/besm6/2348                    $SHM/2348-etalon
cd $BASE/repo-copy && python3 tools/build_forex_perso.py
python3 $BASE/run_case.py --image $BASE/repo-copy/build/FOREX_PERSO_2300.bin --tag baseline
```

Actual assembler log:

```
  assembled FOREX*  : body=379 load=347 takepg_entry=0o462
  assembled XDATAPR : body=63  load=47  takepg_entry=0o0
  OCTTDEC etalon : body=32 load=27 (monsys.9 0o37100) catalog=OCTTDE*
  assembled XGIVPG  : body=47  load=35  takepg_entry=0o24
image sha256 : 0bd8e5862d61a4b30358534260cf7cd06029966e4504821d4fc4d078e8a9d53b
words 5120 (5 zones), bytes 30720
catalog: FOREX* LO*SYN LO*GEN FORMAT FORTLIBR XDATAPR OCTTDE* XGIVPG XTAKPG
```

The rebuilt image is **byte-identical** to the repo's checked-in
`build/FOREX_PERSO_2300.bin` (same SHA, `cmp` clean). The `aab191de…` SHA in `docs/15:86`
is stale relative to the current etalon (`f15f2513…`).

Install (`run_case.py`): fresh copy from etalon, `besmtool zero 2348 --start=1216
--length=5`, `besmtool write … --from-file=<image> --start=1216`, readback
`cmp` against the image = OK; etalon unchanged. Working disk SHA after install:
`7558091f7dbc427ab23a87f817eecee31720dd3d814f7a407fe070d364cfe998`.

Deck (C): `шифр 419999 зс5^`, `лен 60(2348)^`, `*call yesmemory`, `*perso:602300`,
`*full list`, `*forex`, `glkern.b6` body, `*execute`.

## 4. C-dispak result

```
image      : 0bd8e5862d61a4b30358534260cf7cd06029966e4504821d4fc4d078e8a9d53b
install    : zones 0o2300..0o2304 identical to image: OK
dispak rc  : 0  raw=27511B  stderr=29B ("KCNT: on_pc=00000 env=(none)")
RESULT     : MATCH gold (14 result lines, date-normalized)
```

ACPU-equivalent raw output (`cases/baseline/output.raw`, SHA
`32f12e4af908ccbf83ca509d788dcbb54846361ae491b8693776a3cd233147d9`); result block:

```
  1  0.00      1.9000      0.6250      7.5290
  2  0.30      2.7502      3.5760     35.0000
  3  0.50      1.0621      1.7243     53.2897
  4  1.00      1.0199      1.4679     18.5361
  5  1.50      2.0285      2.3918     35.0978
      0.0  288.1500    1.225000
   5000.0  255.6500    0.736114
  10000.0  223.1500    0.412704
  15000.0  216.6500    0.193663
  1    0.55071441
  2   -0.38747490
  3   -0.50065876
  4   -1.30818495
  5   -1.50960208
```

Banner in the output: `F О R Е Х ИПМ АН СССР ВЕРСИЯ 2.02 ОТ …` and `ВРЕМЯ СЧЕТА: …`;
both are external to our image (`docs/16` §6). Load map (`*system load list` case):
`FOREX* 01770`, `LO*SYN 22654`, `LO*GEN 22654` - the **system** root address 01770,
not a load address from our catalog record (f0=0o462).

## 5. Full BESM-6 SIMH result: corrected ini, no-PERSO deck passes, PERSO deck still fails

Method reused from `docs/74-simh-verification.md`, `docs/75`, `docs/plan-f77-full/36`
and the parallel workspace tools (`make_simh_ini.py`, `drive_simh.py`, `simh_ops.py`):
isolated tmux socket `TMUX_TMPDIR=$BASE/simh/tmux`; console **only** via
`tmux capture-pane -p -S -N`; input **only** via `send-keys`; `ДATA:` as boot marker
(never `CM1П`; live session 0 was never touched); system 2048 image at md41, **copy** of
2348 at md45 (never `~/.besm6/2348`); tty DKS ports moved to 4302+ because other agents
own 4199+.

### 5.1 Root cause of the earlier `СБОЙ АЦПУ0` / empty ACPU: our custom ini

The earlier generated ini **commented out** the stock prn lines and **appended** new
`attach -n prn0/prn1` AFTER `load boot_dispak.b6` / `run 2000`:

```
 65: ; attach -n prn0 /.../BESM6/ACPU/output.txt     <- stock line commented
 66: ; attach -n prn1 /.../BESM6/ACPU/output1.txt
187: load .../boot_dispak.b6
188: run 2000
192: attach -n prn0 /.../runs/case.acpu.txt          <- attached AFTER boot
193: attach -n prn1 /.../runs/case.acpu1.txt
```

The OS initialises its device configuration during `run 2000`, so it booted with **no
printers**, producing `СБОЙ AЦПУ0` and empty ACPU files. The user's edit to
`tools/run_besm6_deck.py` deliberately keeps the stock prn lines for exactly this reason.

**Fix applied** (`simh/make_simh_ini.py`): keep `attach -n prn0/prn1` **in place** before
boot, changing only the path to a writable workspace file:

```
 65: attach -n prn0 /dev/shm/re-forex-413-baseline/simh/runs/case.acpu.txt
 66: attach -n prn1 /dev/shm/re-forex-413-baseline/simh/runs/case.acpu1.txt
187: load .../boot_dispak.b6
188: run 2000
(no appended prn lines)
```

After the fix the operator directives behave exactly like the live machine:
`ДАЙ А0 → ЕСТЬ`, `ДАЙ А1 → ЕСТЬ`, `НОМВ → HET` (empty, healthy queue). With the broken
ini the same sequence produced `CБОЙ AЦПУ1` and `НОМВ → CБОЙ: A1`, then after the deck
`CБОЙ: A0 A1` with queue lines `419919 04 001/001 A0+`, `410300 06 002/001 A1+`.
No `СБО` without parameters was used; explicit `ПОВ А0`/`ПОВ А1` recovered the state but
could not make the printers produce the listing.

### 5.2 Fixed-ini results

| case | deck | ACPU prn0 | КОНЕЦ ЗАДАЧИ | 14 result lines |
|---|---|---|---|---|
| `fix_disonly` | no `2348` mount, no `*perso` | full listing | yes | **MATCH gold** |
| `fixedhello2` | HELLO control, `*ftn` | `НЕLLО WОRLD` at line 194 | yes | n/a (control) |
| `fix_pnomount` | `*perso:452300`, no mount card | 1220 B | yes (abort) | no |
| `fix_lun45`, `fix_lun40b`, `fix_etalon` | `*perso` via various LUNs | 1669 B (footer only) | no | no |

Decisive ACPU excerpt (`simh/runs/fix_disonly.acpu.txt`):

```
581:  1  0.00      1.9000      0.6250      7.5290
586:      0.0  288.1500    1.225000
590:  1    0.55071441
596: КОНЕЦ ЗАДАЧИ        +000000000000⏨+00    0000000000001114
```

HELLO control (`simh/runs/fixedhello2.acpu.txt`): `194: НЕLLО WОRLD`,
`196: КОНЕЦ ЗАДАЧИ`. This proves the ACPU path and the deck runner now work under SIMH.

When the deck used volume `2348` (the earlier mistake), the OS failed at device
configuration. Exact error (`simh/runs/fix_pnomount.acpu.txt:102`):

```
 *РЕRSО:452300
 ОБРАЩ.К НЕЗАК.МЛ    +272109409626⏨-19    0010020000452300
```

i.e. "reference to unconnected magnetic-tape device 45". LUN 40/46 and an explicit
`дис NN(2348)` mount also abort before the deck is echoed.

### 5.3 Volume-corrected recipe from the parallel stage (docs/79 §4), replicated

Exact recipe reproduced on my copies: deck cards `ДИС 41(2048)^` +
`ЛЕН 60(2048-wr)^`, monitor card `*PERSO:602300`, stock `-n prn` lines in place before
boot, **md45 host file named `2048` seeded from a FULL disk image whose zone `0o2300`
holds our rebuilt PERSO image** (my earlier attempt used the bare 30,720-byte PERSO file
instead of the 33,024,000-byte disk, which is why patches had no effect). Operator
`ДАЙ А0`/`ДАЙ А1`/`НОМВ` before and after; `НОМВ → HET`.

The rebuilt image is SHA `0bd8e5862d61a4b30358534260cf7cd06029966e4504821d4fc4d078e8a9d53b`.

```
[vfull_clean] done_flag=True, prn0=34011B, КОНЕЦ ЗАДАЧИ at ACPU line 602
587:  1  0.00      1.9000      0.6250      7.5290
592:      0.0  288.1500    1.225000
596:  1    0.55071441
602: КОНЕЦ ЗАДАЧИ
```

So the full `*perso` glissade deck **does** complete under SIMH with our rebuilt image
installed. This removes the earlier harness/volume objections; it does not, by itself,
attribute the output to our compiler (see §6.3).

## 6. A/B

### 6.1 C-dispak A/B (does not discriminate)

| case | patched word | raw output SHA (first 12) | 14 result lines |
|---|---|---|---|
| `baseline` | none | `32f12e4af908` | MATCH |
| `ab_rootcode` | image 2357, FOREX* cmd word | `32f12e4af908` | MATCH |
| `ab_syncode` | image 2437, LO*SYN first code word | `32f12e4af908` | MATCH |
| `ab_gencode` | image 3493, LO*GEN first code word | `32f12e4af908` | MATCH |
| `ab_name_syn` | catalog name word 4 (LO*SYN) | different (`ИСПОРЧЕН КАТАЛОГ РЕRSОNАL LIВRАRУ` printed) | MATCH |
| `ab_cat_fx` | catalog record word 3 (FOREX* TV) | different (symbol table shifted) | MATCH |
| `no-perso` | `*perso` card removed, etalon untouched | different only in echoed card + blank line | MATCH |

All raw outputs of the code-word A/B are **byte-identical** (SHA above). The strongest
control is `no-perso`: with and without `*perso:602300`, the full normalized output is
identical except the echoed `*РЕRSО:602300` line. Corrupting the catalog is detected
(`ИСПОРЧЕН КАТАЛОГ…`) and changes the linked symbol table, so the library *is* read, but
**none of the rebuilt compiler words affect the Fortran result**. `docs/16` §6 point 3
already records that the root loaded at 01770 is the system one.

Conclusion: **zero/alter-one-word → output-breaks → restore → works is NOT achieved**.
The gold-like output in §4 was produced by the pre-existing system FOREX 2.02, not by the
rebuilt-from-texts compiler. A "PASS" here would be a false claim.

### 6.2 SIMH A/B (after the ini fix)

| SIMH case | image on md45 | deck | ACPU result |
|---|---|---|---|
| `fix_disonly` | rebuilt image present, but no `*perso` card | no `2348` mount, no `*perso` | **gold 14 lines**, `КОНЕЦ ЗАДАЧИ` |
| `fix_pnomount` | rebuilt image (catalog word 3 intact) | `*perso:452300`, no mount | `ОБРАЩ.К НЕЗАК.МЛ`, abort |
| `fix_ab` | rebuilt image with **catalog word 3 zeroed** (verified `word3=0o0`) | same `*perso:452300` | identical `ОБРАЩ.К НЕЗАК.МЛ`, abort |
| `fix_lun45`, `fix_lun40b` | rebuilt image | `*perso` via other LUN / explicit mount | 1669 B footer only, abort |

Zeroing a word in our rebuilt image does **not** change the SIMH outcome: the device
configuration fault (`LUN 45 is an ML`, or an invalid data mount) occurs before the
PERSO catalog or any module body is read. Restoring the word restores the same abort.
The only deck that produces the gold in SIMH is the **no-PERSO control** - exactly the
condition the directive says must *not* produce the same gold if the rebuilt compiler
were responsible. It does, so the discrimination fails in SIMH too.

**Consequence at that stage:** the ini fix only established that the harness/operator
path is healthy. §5.3 then removed the remaining volume obstacle.

### 6.3 A/B with the volume-corrected recipe (execution-path patches)

All cases below use the **same** deck (`decks/v2048_glissade.b6`, cipher 410300,
`ДИС 41(2048)^`, `ЛЕН 60(2048-wr)^`, `*PERSO:602300`), the same full-disk md45 setup,
and `НОМВ → HET` before/after. Each patched image was written into zone `0o2300` of a
fresh 2348 copy with `besmtool write --start=1216`, then copied to the host file `2048`.

| case | same-length patch in our PERSO image | image SHA256 | ACPU result |
|---|---|---|---|
| `vfull_clean` | none | `0bd8e586…53b` | gold 14 lines, `КОНЕЦ ЗАДАЧИ` (line 602) |
| `vfull_patched` | `RUNTIME_FORMAT` word 46 (`F002DS`) `0o40077776 → 0o40077237` (image word 4593) | `bb46fe75…94b68` | **identical** gold 14 lines, `КОНЕЦ ЗАДАЧИ` (line 602) |
| `vfull_f003` (bare-file trial) | `F003DS` `0o40077775 → 0o40077237` (image word 4594) | `17bded7b…966b5` | identical gold 14 lines |
| `vfull_root` | FOREX* first code word (image 2357) `0o042001500004005 → 0` | `adfe1227…59986` | identical gold 14 lines |
| `vf_noperso` | `*PERSO` card removed, clean image | `0bd8e586…53b` | identical gold 14 lines |
| `vf_stand` | clean image + `*STAND` | `0bd8e586…53b` | identical gold 14 lines |
| restore (`vfull_clean` again) | none | `0bd8e586…53b` | gold 14 lines |

The patched word-46 image SHA `bb46fe758284bc135b356391be33249786902f0d769a1620b19123ee25e94b68`
is **exactly** the SHA reported for `PERSO_patched` in `docs/79-413-io-map.md:94`, so the
byte-level patch matches the parallel stage's. With the same deck family and the same
image bytes, however, my replication shows **no output change** for word 46, for
`F003DS`, for a zeroed root code word, or for removal of the `*PERSO` card. The parallel
stage's `simh/runs/v3.console.txt` shows no job-start line (`B075-1` absent) and `НОМВ`
sent immediately after `go`; my driver sends `НОМВ` only after completion, and the job is
accepted and prints the full gold block. I report this as an unresolved discrepancy,
not as a successful A/B.

**Verdict stays FAIL.** The discriminator the task requires - zero/alter a rebuilt
module word, see the gold output change, restore, see it return - was not obtained in
my workspace under the exact volume-corrected recipe. The no-PERSO control still prints
the same gold, so the available evidence continues to attribute the compiled result to
the system FOREX 2.02, not to the rebuilt-from-texts compiler.

## 7. F77 extension-point map (anchors in the 4.13 texts)

| F77 feature | Where to extend | Exact 4.13 anchor | Scope |
|---|---|---|---|
| Intrinsics (`SQRT`, `EXP`, `ABS`, `FLOAT`, `IFIX`, `AMOD`, …) | The root declares five expression/dispatch subprograms whose bodies were **never found**; they are the natural intrinsic/constant/operator hooks. Add bodies as a **new module** and a catalog entry; do not fake them inside the root. | `reference/libra211.forex.inc:13-17` (`FOREX:`, `CONST:`, `COMEQ:`, `OPRTR:`, `ПP:` SUBP); missing bodies confirmed `docs/06-core-modules.md`, `docs/07-runtime.md:34-39` | **new module** + root SUBP/catalog update in `reference/libra211.forex.inc` / `src/reloc/FOREX_ROOT.reloc.mad:9-14` |
| `FUNCTION` / `SUBROUTINE` / `CALL` | Entry table `ENTRY*` and 2048-word buffer `*A*` are the compiler's symbol pool; page linkage is `GIV/PG`/`TAK/PG`. Extend entry-table layout and linkage conventions, then the syntax/generator automata in the overlays. | `reference/libra211.forex.inc:2` (`ENTRY* ,LC,50B`), `:18` (`*A* ,LC,4000B`), `:10-11` (`TAK/PG`, `GIV/PG` SUBP); `include/FOREX_ROOT.mad:198-254` (GIV/PG body); `src/LO_SYN.mad:17-33` (COMMON declarations); `src/LO_GEN.mad` external refs `X_CONST/X_COMEQ/X_OPRTR` (`include/LO_GEN.labels.md:23-25`) | entry table in **root**; call semantics in **overlays** (needs a symbolic rewrite first, `src/reloc/README.md:9-11`) |
| `FORMAT` descriptors | FORMAT is an 11-entry dispatcher `FT*nnn`. A new descriptor = one new `SUBP` + one new `UJ` in the dispatch chain; the existing table is the pattern. | `reference/libra211.format.inc:19-30` (FORMAT NAME + 11 `SUBP`), `:55-75` (`UJ FT*…` chain), `:79` (`,END,`); `src/FOREX_RUNTIME.mad:121,123-133` (FTDISP), `:46-56` (`77xxxB` transfer cells) | **runtime module** (append entries to FORMAT catalog) |
| `PRINT` / `WRITE` / formatted output | `FORTLIBR` exports `PRINT8` and `WRITLIBR`; `PRINT8` is invoked via `VJM` at `:15615` and `*74` at `:15616`. Add a new print routine alongside `PRINT8`, not by patching the byte-exact tape body. | `reference/libra211.format.inc:80-82` (`FORTLIBR NAME`, `BUFFER`, `WRITLIBR`, `PRINT8`), `:103` (`VJM PRINT8`), `:201-202` (`,END,`); `src/FOREX_RUNTIME.mad:191-194`, `reference/README.md` 4.13 gold `expect_forex.txt:44` (`PRINT8 03324`) | **runtime module** |
| `READ` / formatted input | No `READ` descriptor exists in the 11 `FT*` entries; it requires a new descriptor plus a library reader. This is the largest gap. | `reference/libra211.format.inc:19-30,55-75` (complete FT* set); `src/FOREX_RUNTIME.mad:118-190` (whole FORMAT section) | **new runtime module** + FORMAT entry |
| Overlay/extension loading | `LOREX` loads `LO*SYN` then `LO*GEN` via `LOADANGO`; a third overlay or a modular extension hooks here. | `reference/libra211.forex.inc:38-42` (`LOREX:`, `XTS LO*SYN`, `CALL LOADANGO`, `XTS LO*GEN`, `CALL LOADANGO`), `:78-79` (TEXT names) | **root** dispatch + new overlay module |
| Program-level version/identity | Version markers live in the image tail and source headers, not in compiler code; a rebuilt identity needs a distinct catalog name/zone so it can be selected instead of the system compiler. | `tools/build_forex_perso.py:89-92,169-172,418-419`; `docs/16` §6; PERSO `0o2400` is free per `docs/14-perso-write.md` | **new module/catalog entry** |

What can be added in place: the root SUBP declarations, the `ENTRY*`/`*A*` layout, the
overlay TEXT names, and the FT* dispatch chain (all in the authoritative texts above).
What needs a new module: all five missing root bodies (`FOREX`, `CONST`, `COMEQ`,
`OPRTR`, `ПP`), any new FT* descriptor/reader, and a compiler identity that the monitor
can actually select. The current `*perso:602300` + `*forex` path does **not** select our
compiler (§6), so F77 work must first establish a selection mechanism (e.g. a distinct
compiler module in PERSO `0o2400` invoked through its own card) and re-run the §5/§6 gates.

## 8. Files and artifacts produced (all outside the repo)

- `report.md` (this file)
- `run_case.py`, `simh_case.py` (isolated install/run drivers)
- `simh/{make_simh_ini.py,drive_simh.py,simh_ops.py,ini_*.ini,decks/,runs/,logs/,disks/,images/}`
  (SIMH tree lives in `/dev/shm/re-forex-413-baseline/simh`, symlinked from the workspace;
  `make_simh_ini.py` contains the fixed in-place prn attach)
- `repo-copy/` (copies of build tool, reloc sources, word dumps, glissade fixtures)
- `cases/<tag>/{image.bin,job.b6,output.raw,output.norm,result.txt}`
- `simh-runs*.log`, `simh-run-fix_*.log`, `case-*.log`, `build-stdout.txt`

**PERSO route verdict: FAIL** (same-length patches do not discriminate; no-PERSO control
prints the same gold). This route is **not the product**. See §9 for the contour product.

## 9. PRODUCT: zone-0o2350 contour from the 4.13 texts - PASS

### 9.1 Build (SYSTEM FOREX is only the build compiler; the deck invokes only our contour)

The contour is assembled from the 4.13-text-derived Fortran fixtures, with no host codegen
in the product: `src/newcomp/O412C.FTN` (catalog words 0..15, head 16..34, overlay 35..409),
`tests/plan-f77/69-full-emitted-body/o412d_words.hex` (1005 body words emitted by O412D),
`tests/plan-f77/65-m80-install/ovl_our.hex` (1024-word rebuilt object), and the proven
`tests/plan-f77/84-wide-output/installer.py` generators. The builder reused verbatim from
the parallel stage is `simh/build_contour_simh.py` (copy of
`re-forex-413-io/work/build_contour_simh.py`); it writes logical zones

```
N = 0o2350   catalog  = O412C words 0..15
N+1 = 0o2351 body     = O412C 16..34 + O412D tail + codegen overrides
N+2 = 0o2352 overlay  = O412C 35..409 at word 526
N+3 = 0o2353 zero
header w0=(phys<<36)|0x038ca3c918, w1=0x000005f1c7800000,
w2=0x0000410300000000, w3 = end-around-carry sum of 1024 data words
```

into a **copy** of `/usr/local/share/besm6/2048` attached at md41. Note: the `zero` index
must be octal (`0o41`), not decimal 41; decimal 41 builds a different image with no effect.

Deck (SHA `1d93c468c1acf7b6c9d7ac5f002336ce4580d6d716fbc1694aabd605c9bbeae2`, identical to
docs/75's proven deck) contains only the contour translator call - no `*FOREX`, no
`*FTN`, no `*perso`, no runtime cards:

```
ШИФР 410300 ЗС5^
ДИС 41(2048)^
ОЗУ 32^АЦП 32^
ЕЕВ1А3
*NAME OURMRK
*TRANS:OURMRK*,,412350
      PROGRAM MAIN
      END
*EXECUTE
*END FILE
``````
ЕКОНЕЦ
```

md45 = workspace copy named `2048` (SHA `d4996cfd15e17132c64bd3f1e23dbea925f5dc9f26f27d6ee446fb876be660e4`),
stock `-n prn0/prn1` in place before boot, isolated tmux, `ДATA:` boot marker,
`ДАЙ А0`/`ДАЙ А1`/`НОМВ` before the deck; post-deck `НОМВ` only **after** the confirmed
job-start line `B075-1 410300000000` (docs/83 §4.4 strict sync).

### 9.2 SIMH A/B/A + no-install (all real boots on copies)

| Case | md41 image SHA-256 | ACPU decisive line | Verdict |
|---|---|---|---|
| baseline | `a98e81090d4b254554a0cd3ff8611438615de84fc012e8e2b70fbabc2ebdc796` | `21 1.00 3.00`, `КОНЕЦ ЗАДАЧИ` | PASS |
| patched: `body[0o41]` word zeroed (RAM `0o2020`) | `1f4431d177e02481aa70e22d863ce00cc5789aae647fb292c0598ba645849cda` | `01 1.00 3.00`, `КОНЕЦ ЗАДАЧИ` | output changed |
| restore (byte-identical to baseline) | `a98e81090d4b254554a0cd3ff8611438615de84fc012e8e2b70fbabc2ebdc796` | `21 1.00 3.00`, `КОНЕЦ ЗАДАЧИ` | PASS |
| no-install (stock 2048, SHA `fd2ed601b73dcb47693c…`) | stock | `ОТСУТСТВУЕТ OURMRK*` | control |

Raw ACPU excerpts (`simh/runs/sc_*.acpu.txt`):

```
base     : 21 1.00 3.00          КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000
zero41o  : 01 1.00 3.00          КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000
restore  : 21 1.00 3.00          КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000
noinst   : ОТСУТСТВУЕТ OURMRK*   КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000000000001146
```

Every case confirmed the console job start `B075-1 410300000000`. The ACPU files were
read from whichever of prn0/prn1 actually received the print (both recorded).

**Conclusion: PASS.** Zeroing a single word of OUR contour changes the printed result
`21` → `01`; restoring the byte-identical image restores `21 1.00 3.00`; without our
contour the OS prints `ОТСУТСТВУЕТ OURMRK*`. The deck invokes no system compiler, so the
marker is produced by the contour built from the 4.13 texts, not by the system FOREX.
This is the decisive proof the PERSO route could not provide.

### 9.3 Honest limits

- This proves the contour (built from the text fixtures) executes and produces the
  formatted output; it does not prove a full F77 front end (READ formats, G, END=/ERR=/IOSTAT
  are still absent, docs/83 §5-7).
- The marker is a 4-integer + 2-fraction digit PRINT via the contour's GOST descriptor
  words at `0o2006..0o2011`; it is a real formatted decimal print, not host codegen.
- No repo edits, no git writes, no live disk or tmux 0, no dispak C patches; all images
  and ACPU files live in this workspace / `/dev/shm`.
