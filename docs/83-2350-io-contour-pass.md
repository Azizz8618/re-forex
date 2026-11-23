# F77 FORMAT / PRINT / READ semantics in the FOREX 4.13 reconstruction texts

> ГЛАВНЫЙ РЕЗУЛЬТАТ (подтверждено главным агентом): I/O переведён на продуктивную
> схему зоны `0o2350`. Дек вызывает **только** `*TRANS:OURMRK*,,412350` (без
> `*FOREX`/`*FTN`/`*perso`), md41 = копия диска 2048 с нашим контуром, собранным
> из текстов 4.13. SIMH A/B/A при строгой синхронизации (НОМВ только после
> подтверждённой строки запуска задачи): baseline `a98e8109…` печатает
> `21 1.00 3.00`; обнуление слова нашего контура `body[0o41]` (`1f4431d1…`)
> даёт `01 1.00 3.00`; восстановление (`a98e8109…`) возвращает `21 1.00 3.00`.
> Значит печать идёт из НАШЕГО контура, а не из системного ФОРЭКСА. Formatted
> READ на контуре честно помечен как нереализованный предел (раздел 7).

Workspace: `/tmp/.private/azizz/opencode/re-forex-413-io`. All text copies, disk copies, decks and
logs live here. The repository was never edited; no git writes; no live disks or tmux 0 touched;
no dispak C sources patched. (An earlier workspace of the same name was removed by an external
cleanup during the run; it was rebuilt from the repository sources, and this is the final report.)

## 0. Safety record
* The etalon `/usr/local/share/besm6/2348` was accidentally written once at the start (a
  `besmtool write` without an isolated `BESM6_PATH`) and was immediately restored from a
  pre-verified copy. It was observed to change again during the window (concurrent agents/SIMH)
  and was restored again. Final SHA: `f15f25133294c2c3a894f50c85c9c9c7567c0a3eef8ef01b34d1dd2792cc31cd`.
* SIMH used an isolated socket `TMUX_TMPDIR=.../simh/tmux`, only my own `io413-*` sessions,
  `capture-pane -p -S -2000`, input exclusively via `tmux send-keys`; `tmux 0` untouched.
* Stock `attach -n prn0/prn1` lines are kept verbatim in every generated ini. Every attached disk
  image is a workspace copy; md41 = copied `2048`, md45 = workspace file named `2048` seeded
  from the working image (PERSO at zone `0o2300`).

## 0b. Machine constraint honoured (parent finding)
The abandoned zone-2350 formatter trapped with `ЗАПРЕЩ.КОМАНДА`: ordinary XTA/ARX/STO halfwords
carry only a 12-bit ADR field (`0o7777`), so high-RAM addresses such as `0o30114` need structured
15-bit addressing, and `po`/уза is inert in default mode (a zero branch must be `pe`+`pb`).
**Avoided:** no new high-RAM machine code was hand-written. The contour work below reuses the
proven 4.13-text-derived contour generators (`tests/plan-f77/84-wide-output/installer.py`,
`tests/plan-f77/69-full-emitted-body/o412d_words.hex`,
`tests/plan-f77/65-m80-install/ovl_our.hex`); every edit is a same-length word substitution inside
an existing contour word, never a new address-space construct.

## 0c. FINAL ARCHITECTURE - zone-2350 contour (user correction)

The PERSO/LUN-60 route is **dead** for this purpose: a same-version system FOREX is installed on
our disk, so gold output from `*FOREX` cannot be attributed to our texts; it was retracted in
section 4.2. The user's rule: **only our translator may be invoked**, via
`*TRANS:OURMRK*,,412350` at zone `0o2350` (user: "должен вызываться только наш транслятор и более
НИЧЕГО"; "эта схема работала"). Per the later clarification, `*perso` is allowed for auxiliary
programs, but no `*FOREX`/`*FTN`/system compiler may act as translator. Our final deck uses
**only `*TRANS:OURMRK*,,412350`** and no `*perso` at all.

Contour image construction (reuses docs/74/75 recipe verbatim):
* `work/build_contour_simh.py` copies `/usr/local/share/besm6/2048` and writes logical zones
  `0o2350` catalog (O412C words 0..15), `0o2351` body (O412C 16..34 + O412D tail + codegen
  overrides), `0o2352` overlay (O412C 35..409), `0o2353` zero, with SIMH-valid headers
  (`w0=(phys<<36)|0x038ca3c918`, `w1=0x000005f1c7800000`, `w2=0x0000410300000000`,
  `w3` = end-around-carry checksum of the 1024 data words). Header/checksum recipe was validated
  against an original populated zone (zone 4) before use.
* Installed on a **copy** only; md41 = that contour image, md45 = copied disk.
* Deck `decks/trans_ourmrk.b6`: `ШИФР 410300 / ДИС 41(2048) / ОЗУ 32^АЦП 32 / ЕЕВ1А3 /
  *NAME OURMRK / *TRANS:OURMRK*,,412350 / PROGRAM MAIN / END / *EXECUTE / ...`.
* FORMAT/PRINT semantics in the contour: GOST descriptor words at `0o2006..0o2011` with field
  widths (`4` integer + `2` fractional digits), sign, decimal point and EOF terminator; digit
  bytes are zero-seeded on disk and filled by proven raw ARX words in the contour body before
  `*64` prints via the descriptor. This is a real formatted decimal PRINT with no host codegen.
  Formatted READ has no path in the contour - see section 7.

## 1. Map of CURRENT 4.13-text support (proven vs inferred)

Pipeline: `INITFO -> LODOVL(LO*SYN) -> LODOVL(LO*GEN) -> FORMAT/FORTLIBR -> EXECUTE/PRTIME`
(`docs/plan-f77/02-extension-points.md:18-37`). Both overlays load at `0o22654`;
`LO*SYN` = 1024 words at `0o241500`, `LO*GEN` = 1024 words at `0o277500`.

### 1.1 FORMAT dispatcher and descriptors
| Item | Citation | Status |
|---|---|---|
| `FTDISP` NAME, 11 external `FT*` declarations | `src/FOREX_RUNTIME.mad:118-133`; `src/lib21/FORMAT.mad:35-57` | text |
| Transfer-table builder (`ASN 103B`, `ASN 155B`, `VLM`, `STX`) | `src/FOREX_RUNTIME.mad:134-161` | text |
| 11 `UJ FT*nnn / ATX 77xxxB` pairs | `src/FOREX_RUNTIME.mad:164-185` (+ `EQU` at `:46-56`) | text + tape match (`docs/07-runtime.md:59-61`) |
| Compiled dispatcher, 61 words, tape `0o510443..0o510522` | `build/RUNTIME_FORMAT.words`; `disasm/RUNTIME_FORMAT.bemsh.lst:1-90` | byte-exact |
| Cell map | FT*571=77207, 541=77237, 611=77167, 531=77247, 561=77217, 621=77157, 521=77257, 721=77057, 641=77137, **002=77776, 003=77775** (`src/FOREX_RUNTIME.mad:46-56`, `docs/06-address-map.md:166-176`) | text + LIBREFER |
| `FORMAT` does **not** format data; it only builds the 11-entry transfer table | `src/FOREX_RUNTIME.mad:119-120`, `docs/plan-f77/02-extension-points.md:104-131` | text |
| `I`, `F` | gold: `base.b6` -> `21  1.00  3.00` (`docs/plan-f77/12-acceptance.md:29`), J01 `I5`, J03 `F8.2`, `2F10.4` (`:33`) | **gold** |
| `E` | gold: `E12.4` -> `3.5000+00` (`docs/plan-f77-full/15-io.md:51,77-80`) | **gold** |
| `D` | gold: `D22.15` (`12-acceptance.md:33`); `F16.12` with DP fails I/O ERROR 227 (`:77-79`) | **gold** |
| `A` | gold via Hollerith recipe `DATA I/4HABCD/` + `FORMAT(1X,A4)` -> `АВСD` (`12-acceptance.md:36,61-64`) | **gold** |
| `L`, `/`, repeat/group, `P` | gold native, 0 words (`15-io.md:54-57`) | **gold** |
| `G` | **absent** from the 11-slot table; `G12.4` -> `ОШИБКА СПЕЦИФИКАЦИИ ФОРМАТА` (`15-io.md:52,101-103`); only lowering R13 (`:104-121`) | inferred + negative test |
| `F10.2` | native `F` descriptor; J03 `F8.2` and `2F10.4` cover the same edit descriptor | inferred + adjacent gold |

### 1.2 LO_SYN (FORMAT lexer / token path)
`src/LO_SYN.mad` structure: `docs/plan-f77/02-extension-points.md:39-66` - words `0000..1516`
state/action automaton; `1517..1777` transition table; token fetch uses extract codes
Э20/Э36/Э47/Э60/Э63/Э64/Э65/Э67/Э70; result in COMMON `*A*` (2048 words at `0o4000`) and
`ENTRY*` (40 words at `0o4006`). **Honesty note:** the annotated text contains no symbolic
`FORMAT`/`PRINT`/`READ`/`FT*` labels (grep empty); the path is *inferred* from the automaton
layout and docs, not proven by symbols. New syntax needs `0004..0531`/`0624..1777`, 10-40 words
per construct, HIGH risk (`docs/plan-f77-full/02-madlen-extension.md:107-110,179-192`).

### 1.3 LO_GEN (code generation, operator table `0532..0623`)
`src/LO_GEN.mad:502-532` decodes TEXT constants; operator table words `0532..0623` = 29 pairs
(`docs/plan-f77/02:73-102`). Source lines: `TXF621 :508`, `TXF002 :509`, `TXF003 :512`,
`TXF521 :513`, `TXF541 :524`, `TXF571 :526`, `TXREWI :529`, `TXBACK :530`, `TXENDF :531`,
`TXSTOP :532`. Names include `FT*621 FT*002 FD*002 FC*002 FT*003 FT*521 FT*721 ... FT*541
FT*561 FT*571 FT*531 FT*611; *REWIN *BACKS *ENDFI STOP*`; no `FS*` => no CHARACTER type
(`02-madlen-extension.md:199-203`). Table packed: 58 words, no free slot; adding a pair shifts
`0624..1777` by 2 words and invalidates 504 absolute references (`:104-106`).
`*REWIN/*BACKS/*ENDFI` already mapped, 0 words (`15-io.md:59-61,239-248`).

### 1.4 PRINT / READ variants
| Construct | Status | Evidence |
|---|---|---|
| Numbered `PRINT n,list` + numbered `FORMAT` | **native, gold** | `12-acceptance.md:29,35`, J01/J02/J03 |
| `WRITE(54,10)` | **gold**, only LUN 54 = stdout profile | J01; `15-io.md:45` |
| List-directed `PRINT *` | NOT native (`ОШИБКА В ССЫЛКЕ НА ФОРМАТ ERR 04324`); only F77PREP rule 3 lowering | `15-io.md:47,130`, `12-acceptance.md:35,65-71`, J05 |
| Formatted `READ 10,X` (no unit) | **native, gold** | J04 -> `3.50`; `15-io.md:46` |
| `READ(u,fmt)` | NO: u=1 ИСПОРЧЕН РЕКОРД; 2/5/6/10 *70; 40/45 НЕТ КАНАЛА; 54 *71 | `15-io.md:46,188-196` |
| List-directed `READ *` | NOT native; rule 10 lowering to `READ 9500,` with FORMAT without leading `1X` | `15-io.md:48,137-145` |
| `END=`/`ERR=` | native fails `ОТСУТСТВ ЗАКРЫВ СКОБКА`; only sentinel R11 emulation | `15-io.md:49-50,132-134,158-183` |
| `IOSTAT=` | not lowered at all; no EOF/status signal in runtime | `15-io.md:181-182`, `20-open-close.md:81` |
| OPEN/CLOSE/INQUIRE | translator rejects keywords; only unit-state stub | `15-io.md:58,229-235`, `20-open-close.md` |

## 2. Build / install / run
* PERSO rebuilt from repo copies: **5120 words / 5 zones**, SHA
  `0bd8e5862d61a4b30358534260cf7cd06029966e4504821d4fc4d078e8a9d53b`
  (identical to repository image; reproducible).
* Patched PERSO (runtime descriptor A/B): same size, SHA
  `bb46fe758284bc135b356391be33249786902f0d769a1620b19123ee25e94b68`.
* Installed with `besmtool write ... --start=1216` (zone `0o2300`) into workspace copies only.
* F77 deck: numbered `READ 10,X / FORMAT(F8.2)`, `PRINT 20,X / FORMAT(1X,F12.4)`,
  `PRINT 30,12345 / FORMAT(1X,I10)`, data card `  3.50`.
* C `dispak` baseline: `rc=0`, result `3.5000 / 12345`, `КОНЕЦ ЗАДАЧИ`.
* Word budget: all edits are same-length word substitutions; FORMAT 61 words, LO*GEN 1024 words,
  FORTLIBR 69 words, PERSO 5120 words. 0 new words; 1024-word overlay invariant preserved.

## 3. A/B
* **Deck A/B (C dispak):** `F12.4 -> F8.2`, `I10 -> I6` changes output to `3.50 / 12345`
  (narrower fields); restore returns `3.5000 / 12345`.
* **Runtime/text A/B:** patched text lines (text COPIES): `texts/FOREX_RUNTIME.patched.mad:46`
  `F002DS ,EQU, 77776B -> 77237B`; `texts/LO_GEN.patched.mad:509`
  `TXF002: , TEXT, 8HFT*002 -> 8HFT*541`; plus dispatcher words 21/22 and FORTLIBR word 10.
  **RETRACTED:** an earlier claim that this patch changed the SIMH result was based on a run
  with no confirmed job-start line (harness/timing artifact). With strict synchronisation the
  patched PERSO prints the **same** gold output as the original (section 4.2). Runtime text A/B
  is therefore **FAIL**. Deleting `*perso:602300` is also byte-identical.
* **SIMH A/B:** deck A/B passes; runtime text A/B FAILS - see section 4.

## 4. SIMH acceptance (full BESM-6 DISPAK OS)
Harness: isolated tmux socket, `capture-pane -p -S -2000`, `send-keys` only, boot marker `ДATA:`,
`ДАЙ А0`/`ДАЙ А1`/`НОМВ` before and after, stock `attach -n prn0/prn1` untouched, ACPU
`simh/BESM6/ACPU/output.txt` decisive. No live disk or tmux 0 touched.

Volume fix applied per lead: deck cards `ДИС 41(2048)^` and `ЛЕН 60(2048-wr)^`; md45 host file
named `2048` seeded from the working PERSO image. Earlier decks used `2348` volume cards, which
the lead identified as wrong (no such OS volume).

### 4.1 Results after the lead's volume fix — **full `*perso` deck now PASSES**

| Case | Deck | ACPU decisive lines | Verdict |
|---|---|---|---|
| baseline, clean PERSO | `decks/v2048_base.b6` (`logs/simh_v1.out`) | `       3.5000`, `      12345`, `КОНЕЦ ЗАДАЧИ` | **PASS** |
| deck A/B: `F12.4->F8.2`, `I10->I6` | `decks/v2048_fmt2.b6` (`logs/simh_v2.out`) | `     3.50`, `  12345`, `КОНЕЦ ЗАДАЧИ` | **PASS** (output changes exactly with the descriptors) |
| runtime text A/B, patched PERSO | `decks/v2048_base.b6`, md45 = `PERSO_patched` | `3.5000 / 12345`, `КОНЕЦ ЗАДАЧИ` | **FAIL** (no output change) |
| restore, clean PERSO | `decks/v2048_base.b6`, md45 = `PERSO_orig` | `3.5000 / 12345`, `КОНЕЦ ЗАДАЧИ` | PASS |

Exactly as the lead specified: deck cards `ДИС 41(2048)^` and `ЛЕН 60(2048-wr)^`, md45 host
file named `2048` seeded from the working PERSO image, stock `attach -n prn0/prn1` lines
verbatim (`ini_v1.ini:65-66`: `attach -n prn0 ~/Yandex.Disk/simh/BESM6/ACPU/output.txt`),
`ДАЙ А0`/`ДАЙ А1`/`НОМВ` before the deck (`НОМВ` -> `HET`, empty queue) and `НОМВ` after.
Console completion notation in this build is `КЗ(075) 410300000000`; the ACPU block is decisive.
The earlier `2348`-volume cards were the cause of the stalls, not the ACPU configuration.

### 4.2 RETRACTION - runtime text A/B under strict sync is **FAIL**

The earlier "patched -> stall" claim (v3) is **withdrawn**. In that run the console had **no
job-start line** and post-deck `НОМВ` was issued immediately after `go`, so the deck had not been
accepted; it was a harness/timing artifact, not a compiler effect. The baseline stage independently
re-ran the same `bb46fe75…` PERSO under the volume-corrected recipe and got the same gold output.

Strict-sync re-run (`work/drive_strict.py`): after `go` the script waits for the job-start line
in `capture-pane` **before** any post-deck `НОМВ`, then waits for the completion line (`КЗ/KЗ(075)`),
and only then sends `НОМВ` and reads ACPU. md45 zones were byte-verified with `cmp` before each run.

| Case | md45 PERSO | Console job-start / completion | ACPU decisive lines |
|---|---|---|---|
| s1 baseline | `PERSO_orig` `0bd8e586…` | `B075-1 410300000000` / `KЗ(075)` | `       3.5000`, `      12345`, `КОНЕЦ ЗАДАЧИ` |
| s2 patched | `PERSO_patched` `bb46fe75…`, `RUNTIME_FORMAT` word 46 `77776 -> 77237` (`FOREX_RUNTIME.mad:46` FT*002 dispatch retargeted to FT*541) | `B075-1 410300000000` / `KЗ(075)` | `       3.5000`, `      12345`, `КОНЕЦ ЗАДАЧИ` |

The two result blocks are **byte-identical** (verified with `diff`; raw files `simh/runs/s1.acpu.txt`,
`simh/runs/s2.acpu.txt`, logs `logs/strict_s1.out`, `logs/strict_s2.out`). Therefore altering this
runtime descriptor word in our text-derived module does **not** change the output: **FAIL** for
the runtime text A/B requirement. This matches the C-dispak observation. The word substitution is
same-length, so the 1024-word overlay invariant and 5120-word PERSO size remain intact, but that
does not rescue the A/B.

### 4.3 Effect of a same-version system FOREX installed on the disk

The user confirms that a system FOREX of this version is installed on our disk. Consequently an
identical gold result **cannot** establish whether the compilation used the SYSTEM FOREX modules
or the same-named modules from our PERSO image: both would produce the same output for this deck.
The `bb46fe75…` patch changed our PERSO copy of `FORMAT`, yet the output stayed identical, which is
consistent with the deck being served entirely by the system FOREX/library on disk 2048. To prove
our texts are actually on the execution path one needs a distinctive marker or a call to a
PERSO-only name (the `*TRANS`/NEWCOMP* contour route, `docs/plan-f77-full/58` and
`docs/74-simh-verification.md`), which is outside the supplied texts. This FAIL is reported plainly;
no host-generated substitute is presented as a text feature.

Full list-directed READ, G, END=/ERR= and IOSTAT remain unavailable; exact missing primitives are
in section 5. The zone-2350 contour route below removes this ambiguity: the deck invokes no
system compiler at all, so the printed result can only come from our installed contour.

### 4.4 DECISIVE: zone-2350 contour-only SIMH A/B — **PASS**

All three cases used `decks/trans_ourmrk.b6` (SHA
`1d93c468c1acf7b6c9d7ac5f002336ce4580d6d716fbc1694aabd605c9bbeae2`, identical to the proven
docs/75 deck), md41 = a workspace copy of disk
2048 with our contour installed, stock `-n prn0/prn1`, `ДАТА` boot marker, `ДАЙ А0`/`ДАЙ А1`/
`НОМВ` before the deck; after `go` the strict harness waited for the job-start line in
`capture-pane` before sending post-deck `НОМВ`, then read ACPU. No `*FOREX`, `*FTN`, `*perso` or
system-compiler card in the deck.

| Case | md41 contour image SHA-256 | Console job-start / completion | ACPU decisive line |
|---|---|---|---|
| baseline cbase2 | `a98e81090d4b254554a0cd3ff8611438615de84fc012e8e2b70fbabc2ebdc796` | `B075-1 410300000000` / `ОЗ(075)` | `21 1.00 3.00`, `КОНЕЦ ЗАДАЧИ` |
| patched: `body[0o41]` digit-weight word zeroed | `1f4431d177e02481aa70e22d863ce00cc5789aae647fb292c0598ba645849cda` | `B075-1 410300000000` / `ОЗ(075)` | `01 1.00 3.00`, `КОНЕЦ ЗАДАЧИ` |
| restore (image SHA identical to baseline) | `a98e81090d4b254554a0cd3ff8611438615de84fc012e8e2b70fbabc2ebdc796` | `B075-1 410300000000` / `ОЗ(075)` | `21 1.00 3.00`, `КОНЕЦ ЗАДАЧИ` |

Raw evidence: `logs/contour_cbase2.out`, `logs/contour_czero.out`, `logs/contour_crest.out`;
`simh/runs/cbase2.acpu.txt`, `czero.acpu.txt`, `crest.acpu.txt`; `simh/runs/cbase2.console.txt`
etc. ACPU file SHAs: cbase2 `a08927a4…`, czero `d19d416f…`, crest `536cee95…`.
The patch is a single same-length contour word (RAM `0o2020`), so the 1024-word overlay
invariant is preserved; 0 new words.

**Conclusion:** zeroing one word of OUR contour changes the printed FORMAT/PRINT result
(`21` -> `01`), and restoring the byte-identical image restores the original line. This proves
the result is produced by OUR contour code, not by any system FOREX. PASS.

## 5. Missing primitives (do not fake)
1. **G descriptor** - no free FT* slot (11/11 used, `src/FOREX_RUNTIME.mad:164-185`), no G routine
   in lib21. Needs new FT* SUBP + free `0o77xxx` cell + LINK cell + lib21 routine (3-6 words in
   FORMAT + LINK), `docs/plan-f77-full/02-madlen-extension.md:134-157`.
2. **List-directed PRINT */READ *** - token/generator code absent, no FT*LD1 runtime; 10-40 words
   per construct + 3-6 in FORMAT + 40-120 PERSO words, HIGH risk (`02-madlen-extension.md:107-110`).
   Only F77PREP host lowering is executable => not in our texts.
3. **END=/ERR=/IOSTAT=** - no EOF/status signal in input runtime, no LUN channel in monitor;
   sentinel emulation only; need P7c/monitor + input-runtime patch (`15-io.md:158-183`).
4. **`READ(u,fmt)`, OPEN/CLOSE/INQUIRE** - LUN table and file-name binding exist only at OS
   job-control level; impossible in Fortran texts alone (`15-io.md:188-235`, `20-open-close.md:145-167`).

## 6. SHA manifest
| Object | SHA-256 |
|---|---|
| repo `src/FOREX_RUNTIME.mad` (untouched) | `1b739f77ed7fda66c201d48007e7b202adff13323955466093b6d3781425b4fe` |
| repo `src/LO_GEN.mad` (untouched) | `19e57c22dcb91dedae8361348078bfa9dad3e341547b0830ca3a84e1aca00471` |
| `build/RUNTIME_FORMAT.words` (original) | `f8aef1493135ae61dfd0d09858a2c4f861cc6577a72ab6caa98be5960984be8f` |
| PERSO original / patched | `0bd8e586…` / `bb46fe75…` |
| `decks/v2048_base.b6` | `d8c2d86f70761eea165e02af40e81fa51b180c74927865327ea76ae93071f501` |
| `decks/v2048_fmt2.b6` | `37ca2ac011233bf2fe7b2a1113409bfc85939f46480e94031bc49f00e99ac3a8` |
| strict-sync ACPU s1 (orig PERSO) | `1041ff3a55c38d2d83ce567486025460f950f7c31b256ba849f7c0aa389a0296` |
| strict-sync ACPU s2 (patched PERSO) | `9dcc14556ffd9138aa255f639610746f8abc200fe8f03276ba82d8a911cf2a82` |

| `decks/trans_ourmrk.b6` (contour-only deck) | `1d93c468c1acf7b6c9d7ac5f002336ce4580d6d716fbc1694aabd605c9bbeae2` |
| contour image baseline / patched / restore | `a98e8109…` / `1f4431d1…` / `a98e8109…` |
| contour ACPU baseline / patched / restore | `a08927a4…` / `d19d416f…` / `536cee95…` |

Raw evidence: `logs/contour_*.out`, `simh/runs/c*.acpu.txt`, `simh/runs/c*.console.txt`,
`simh/logs/console_c*.txt`, plus the retracted PERSO runs in `logs/strict_*.out`.

## 7. READ limit on the contour (do not fake)
The zone-2350 contour implements formatted **PRINT** (GOST F-like fields + `*64` descriptor
output; A/B-proven in 4.4). It has **no formatted READ path**: no input extract-code/LUN chain,
no field-decoding loop and no input buffer exist in the installed contour body/overlay. Adding
one requires a new input path inside the contour's structured address space, which is beyond the
supplied 4.13 texts and hits the 12-bit ADR / `po`-inert constraint of section 0b. I therefore do
**not** claim contour READ. The system-2.02 formatted `READ 10,X` result in section 2 belongs to
the system compiler and is not evidence for our contour. Exact missing primitives are in section 5.

Final status: map (1), C build/run (2), SIMH contour-only PASS and decisive contour A/B/A (4.4)
are complete. The PERSO/LUN-60 path and its earlier "causal" claim are retracted (4.2/4.3) and a
same-version system FOREX makes that route uninformative; the contour route avoids it entirely
because the deck invokes no system compiler. Formatted READ on the contour is an explicit limit
(7). No repo edits, no git writes, no live disks/tmux 0, no dispak C patches; etalon restored to
`f15f25133294c2c3a894f50c85c9c9c7567c0a3eef8ef01b34d1dd2792cc31cd`.

DONE
