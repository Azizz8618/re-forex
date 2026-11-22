# SIMH proof of WIDE output (test 84) and CHAINED BESM inserts (test 86)

> Главный агент проверил сырые ACPU-файлы и SHA образов: 15 кейсов на месте,
> `wide_baseline`/`neg`/`max` = `1234.56 / -1234.56 / 9999.99`, `comb_inserts`
> печатает две строки, `comb_operand` меняет вторую на `4470.12`, `comb_zero_acc`
> и `comb_zero_ins4` — на `3470.12`, `no_install` даёт `ОТСУТСТВУЕТ OURMRK*`.
>
> **Внимание про живой диск:** SHA `~/.besm6/2348` в момент проверки отличался
> от эталонного (`d45a2ac1…` против `f15f2513…`). Субагент не подключал живой
> файл ни в одном из 15 ini; причина изменения не установлена (ранее уже фиксировались
> отложенные записи SIMH). Восстановление живого файла не выполнялось без
> отдельного решения пользователя — все доказательства получены на копиях.

Workspace: `/tmp/.private/azizz/opencode/re-forex-simh-wide`
Isolated tmux socket: `TMUX_TMPDIR=/tmp/.private/azizz/opencode/re-forex-simh-wide/tmux`
Console source throughout: `tmux capture-pane -p -S -2000 -t <my-session>`;
all input via `tmux send-keys` + `send-keys Enter`. Only my own `wisim-*` sessions
were created/killed. Live tmux session `0` was never touched (still present at
handoff). No edits to `tools/run_besm6_deck.py`, no repo or git writes, no dispak
C patches, no live SIMH processes or disks. All 15 machine cases are real SIMH
boots of the full BESM-6 DISPAK OS with a real deck submitted on `vu0`.

## VERDICT

| feature | verdict | decisive proof |
|:--|:--|:--|
| WIDE output, 4 integer + 2 fractional digits (test 84) | **PASS under SIMH** | `21 1234.56 2470.12`, negatives, `9999.99` ceiling, weight/code zeroing and restore, all from ACPU of a real SIMH job |
| CHAINED BESM inserts with `V = BESM(...)` in one contour (test 86) | **PASS under SIMH** | two ACPU lines per job: `21 1234.56 2470.12` then `21 1234.56 5470.12`; operand change, 777007/zeroed-store and zeroed-entry mutations all move/remove only the second line |

All 15 cases printed `КОНЕЦ ЗАДАЧИ` and all boot consoles showed `2048 - 41`
(md41 = the contour image), confirming the contour was read from the attached
copy. No C `dispak` results were substituted anywhere in this report.

## 1. Safety record

### 1.1 Live `~/.besm6/2348` - SHA before/after (recorded, not attached)

```
BEFORE  b1a45f9548da4bd789c24d9691dee3b4619e4b74784c87c0eb7e3677e491408f  /home/azizz/.besm6/2348
AFTER   d45a2ac17edd9ca947450110e30ed9531116b8db601bf58ea03ffb3cd3e053d1  /home/azizz/.besm6/2348
```

I must report this plainly: the live file's SHA **changed during the task window**
(mtime `2026-11-23 00:56:12 +0300`), although none of my 15 generated ini files
contains any `.besm6` reference:

```
$ grep -l '\.besm6' ini_wi_*.ini | wc -l
0
$ for f in ini_wi_*.ini; do grep '^attach -e md45' "$f"; done | sort | uniq -c
     15 attach -e md45  /tmp/.private/azizz/opencode/re-forex-simh-wide/disks/md_2348
```

Every md45 in every run was a **workspace copy** of `/usr/local/share/besm6/2348`.
Its SHA was unchanged across all 15 boots:

```
BEFORE  f15f25133294c2c3a894f50c85c9c9c7567c0a3eef8ef01b34d1dd2792cc31cd  disks/md_2348
AFTER   f15f25133294c2c3a894f50c85c9c9c7567c0a3eef8ef01b34d1dd2792cc31cd  disks/md_2348
```

No SIMH process is alive at handoff and no process holds either file. The
previous SIMH task's report already documented repeated delayed writes to this
same live file by earlier sessions; the cause of this change is not established
in this task, and it did not come from any attached image used for the evidence
below. I did not write to, restore, or otherwise touch the live file.

### 1.2 Other safety facts

- md41 was only ever attached to `disks/wi_*` images built in this workspace.
- Every other attached image (drums, md06/01/02/04/05/07/21/42/43/44, all mg,
  prn/vu) is a workspace copy; `base.ini` was rewritten from the reused
  `/tmp/.private/azizz/opencode/re-forex-simh` paths to the new workspace (33
  path replacements) before any boot.
- All my tmux sessions were killed by `drive_wide.py`; the isolated socket has
  no server at handoff. Session `0` (created 20 Nov) was left as found.

## 2. Image construction and exact placement

`build_wide.py` imports the proven generators read-only:
`tests/plan-f77/84-wide-output/codegen_wide.py` and
`tests/plan-f77/86-combined-contour/codegen_combined.py`. Fixtures:
`src/newcomp/O412C.FTN`, `tests/plan-f77/69-full-emitted-body/o412d_words.hex`,
`tests/plan-f77/65-m80-install/ovl_our.hex`.

Each image is a COPY of `/usr/local/share/besm6/2048` (33,024,000-byte tagged
SIMH image, 8-byte LE words with tag in bits 48..49). Four logical zones were
written with the SIMH-valid header proven in the earlier task:

```
phys      = logical + 4
data word i at byte (phys * 8256) + 64 + 8*i
header w0=(phys<<36)|0x038ca3c918, w1=0x000005f1c7800000, w2=0x0000410300000000,
w3 = end-around-carry sum of the 1024 data words,
w4..w7 = same with phys+1
```

Zones `N=0o2350` (catalog = O412C words 0..15), `N+1` (body head = O412C
16..34 + O412D tail 1005 words, then the codegen overrides), `N+2` (overlay =
O412C 35..409 at word 526), `N+3` (combined BESM chain; all-zero for wide-only
and no-install cases). `write_zone` + `verify_zone` from the reused
`simh_install.py` were applied verbatim; data, checksum and w0 were read back
and asserted for every written zone of every image.

Key body words (octal, **indices printed in decimal**; RAM = `0o1757+body`):

| body idx | octal idx | RAM | wide baseline | combined | role |
|:--|:--|:--|:--|:--|:--|
| 9..14 | 11..16 | 1770..1775 | GOST A/B/C/D build chain (identical in both) | identical | digit build |
| 15 | 17 | 1776 | `0064200402200000` | `0064200402200000` | `*64 2004`, FIRST print |
| 16 | 20 | 1777 | `6700000002200000` (RET) | `0303011400000000` (UJ 0o30114) | combined entry; `0` in `comb_zero_entry` |
| 17 | 21 | 2000 | - | `6700000002200000` | fall-through guard |
| 21/22 | 25/26 | 2004/2005 | descriptor pair | descriptor pair | `*64` descriptor |
| 23..26 | 27..32 | 2006..2011 | zero-seeded GOST A/B/C/D + EOF | identical | printed text |
| 27..29 | 33..35 | 2012..2014 | - | Y cell(0), `1<<32`, `2<<32` | BESM weights |
| 32..35 | 40..43 | 2017..2022 | wD/wA/wB/wC digit weights | identical | runtime ARX addends |

Combined high-RAM chain in zone `N+3` (word `k` -> RAM `0o30114+k`):

| k | word (octal) | decode / role |
|:--|:--|:--|
| 0 | `0010201000132013` | `xta 2010 / arx 2013` - C + +1 thousands |
| 1 | `0000201000102014` | `atx 2010 / xta 2014` - store C, build +2 in AU |
| 2 | `0000201200002012` | `atx 2012 / atx 2012` - **777007 (`Y = BESM`)**, AU -> Y cell |
| 3 | `0010201000132012` | `xta 2010 / arx 2012` - reload C, add Y cell |
| 4 | `0000201000002010` | `atx 2010 / atx 2010` - store final C |
| 5 | `0064200402200000` | `*64 2004` - SECOND print |
| 6 | `6700000002200000` | `uj 0(15)` - return |

`comb_operand` replaces word 1 right half `33804` -> `33803` (`xta 2014` ->
`xta 2013`), so the Y cell receives `+1` thousands instead of `+2`.

The FRONT `777006`/`777007` records used to drive `codegen_combined.emit` were
taken verbatim from test 86's report (same numbers as its real `call.out`):

```
777006 11 1 33800 46091
777006 12 1 1032 33804
777007 12 2
777006 13 1 33800 46090
777006 14 1 1032 1032
```

### Deck (identical for all 15 cases, SHA-256 `1d93c468c1acf7b6c9d7ac5f002336ce4580d6d716fbc1694aabd605c9bbeae2`)

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

The Fortran source is intentionally a dummy: `*TRANS:OURMRK*,,412350` pulls the
installed contour body and high-RAM chain from zone 2350 of md41; this is exactly
how the earlier SIMH `*TRANS` proof worked.

### Key ini lines (`ini_wi_<case>.ini`, only the md41 path varies)

```
attach -e md41 /tmp/.private/azizz/opencode/re-forex-simh-wide/disks/wi_<case>
attach -e md45  /tmp/.private/azizz/opencode/re-forex-simh-wide/disks/md_2348
load /tmp/.private/azizz/opencode/re-forex-simh-wide/boot_dispak.b6
```

Boot sequence in `drive_wide.py`: wait for `[ДD]ATA:` via capture-pane, settle 8 s,
`ДАЙ А0` / `ДАЙ А1`, `Ctrl+G`, `at vu0 <deck>`, `d 6 1`, `d 5 10`,
`set cpu req`, `go`; completion from ACPU file + `КЗ/ОЗ/КОНЕЦ ЗАДАЧИ` in the pane.
No `CM1П`/`sim>` regex is ever waited on. Console exemplar (`comb_inserts`):

```
  2248 - 01
  2061 - 21
  2048 - 41
 ДATA:23.11.26 BPEMЯ:01.02.00
 CM1П:00.00.ЭBM-3  ДATA:23.11.26 BPEMЯ:01.02.00  000.00
ДАЙ А0
 ECTЬ
ДАЙ А1
 ECTЬ
Simulation stopped, "СчАС": 04440 (-> цикл 4440(15), цикл 4432(1))
sim> at vu0 /tmp/.private/azizz/opencode/re-forex-simh-wide/deck_trans.b6
sim> d 6 1
sim> d 5 10
sim> set cpu req
sim> go
 B075-1 410300000000
 ОЗ(075) 410300000000 01.02 M=076
```

## 3. ACPU excerpts (all from real SIMH runs, raw double spaces preserved)

```
wide_baseline      :  21  1234.56  2470.12
wide_neg           :  21 -1234.56 -1232.56
wide_max           :  21  9999.99  9998.99
wide_zero_wB       :  21  1200.00  2470.12
wide_zero_wD       :  21  1234.56  2470.00
wide_zero_code     :  21  1200.00  2470.12
wide_restore       :  21  1234.56  2470.12

comb_nowide_ret    :  21  1234.56  2470.12
comb_inserts       :  21  1234.56  2470.12
                      21  1234.56  5470.12
comb_operand       :  21  1234.56  2470.12
                      21  1234.56  4470.12
comb_zero_acc      :  21  1234.56  2470.12
                      21  1234.56  3470.12
comb_zero_ins4     :  21  1234.56  2470.12
                      21  1234.56  3470.12
comb_zero_entry    :  21  1234.56  2470.12
comb_negative      :  21 -1234.56 -1232.56
                      21 -1234.56 -4232.56
no_install         :  ОТСУТСТВУЕТ  OURMRK*
                       СВОБОД   01770
```

Verbatim ACPU context for the two headline cases:

```
*NАМЕ ОURМRК
           *ТRАNS:ОURМRК*,,412350
 21  1234.56  2470.12
 21  1234.56  5470.12
 КОНЕЦ ЗАДАЧИ        +000000000000⏨+00    0000000000001146
```

## 4. A/B table (all with `КОНЕЦ ЗАДАЧИ`, all with `2048 - 41`)

| case | mutation | image SHA-256 (first 16) | ACPU print(s) | expected | result |
|:--|:--|:--|:--|:--|:--|
| wide_baseline | none | `79e8dff32d6cff08` | `21 1234.56 2470.12` | same | PASS |
| wide_neg | X/Y negative | `db0f7ecef1345a89` | `21 -1234.56 -1232.56` | same | PASS |
| wide_max | 9999.99 ceiling | `7919f6996d2043d6` | `21 9999.99 9998.99` | same | PASS |
| wide_zero_wB | `wB` (body 0o42) = 0 | `e52f1096092a9bce` | `21 1200.00 2470.12` | same | PASS |
| wide_zero_wD | `wD` (body 0o40) = 0 | `f6639bd2741a6eb7` | `21 1234.56 2470.00` | same | PASS |
| wide_zero_code | code body[11] = 0 | `57235569507fc5ae` | `21 1200.00 2470.12` | B never stored | PASS |
| wide_restore | restored image (SHA = baseline) | `79e8dff32d6cff08` | `21 1234.56 2470.12` | same as baseline | PASS |
| comb_nowide_ret | no BESM cards -> wide RET | `79e8dff32d6cff08` | `21 1234.56 2470.12` (one line) | same | PASS |
| comb_inserts | 4 BESM cards incl. `Y = BESM` | `7b7fcbcd33d60cc1` | `21 1234.56 2470.12` ; `21 1234.56 5470.12` | same | PASS |
| comb_operand | operand `33804` -> `33803` | `cd08e7bf08f3b1cd` | `21 1234.56 2470.12` ; `21 1234.56 4470.12` | same | PASS |
| comb_zero_acc | 777007 word (zone3[2]) = 0 | `f790bbbdf7b0cd9f` | `21 1234.56 2470.12` ; `21 1234.56 3470.12` | same | PASS |
| comb_zero_ins4 | final store (zone3[4]) = 0 | `1e7d952c821bfaa4` | `21 1234.56 2470.12` ; `21 1234.56 3470.12` | same | PASS |
| comb_zero_entry | entry jump body[16] = 0 | `0ec34c5c45206208` | `21 1234.56 2470.12` (one line) | guard returns | PASS |
| comb_negative | negative wide + 4 BESM cards | `bd5a2e285619ba1c` | `21 -1234.56 -1232.56` ; `21 -1234.56 -4232.56` | same | PASS |
| no_install | pristine 2048, no contour | `fd2ed601b73dcb47` | `ОТСУТСТВУЕТ OURMRK*` | same | PASS |

### Causal conclusions

1. **Wide output.** Baseline, negative-sign and `9999.99` ceiling all print as
   predicted by `codegen_wide.expected_text`. Zeroing digit-weight word `wB`
   changes only X's high integer/fraction digits (`1234.56` -> `1200.00`);
   zeroing `wD` removes only Y's fraction (`2470.12` -> `2470.00`); zeroing the
   code word that stores GOST B gives the same `1200.00`. Restoring the exact
   baseline image (identical SHA) restores `1234.56 2470.12`.
2. **BESM chains.** `comb_inserts` prints the unmodified wide value and then the
   modified `5470.12`, proving the second print comes from the chained inserts
   in high RAM. Changing one operand (`xta 2014` -> `xta 2013`) moves only the
   second line to `4470.12`; zeroing the `777007` accumulator-store word or the
   final GOST-C store word moves it to `3470.12`; zeroing the entry jump removes
   the second line entirely while the guard returns cleanly (`КОНЕЦ ЗАДАЧИ`).
   This is the `V = BESM(...)` accumulator-store path, exercised under SIMH.
3. **Control.** With no installed contour the same deck prints
   `ОТСУТСТВУЕТ OURMRK*`, so neither the marker nor the wide/BESM output can
   come from a monitor-resident module or from the deck itself.

## 5. Image SHA-256 manifest (all verified after the runs)

| case | full SHA-256 |
|:--|:--|
| wide_baseline | `79e8dff32d6cff08c8cb91c9b3adb51312591b8856fccaf8f83e16f2de100ef5` |
| wide_neg | `db0f7ecef1345a895ac8d2ff34df8eb4e821d256e5412170f4af7b523f5e3a0d` |
| wide_max | `7919f6996d2043d6e0e2a731c853340aa719d6c02cb3040e5f3d8be7be58ba1c` |
| wide_zero_wB | `e52f1096092a9bce116d1dada0f2ae72c38d4bc6556a9c815a7bdf06e209efd6` |
| wide_zero_wD | `f6639bd2741a6eb7c9a1d55bd412e85e9304e9e6bd18a5db916f8b26dc29a10e` |
| wide_zero_code | `57235569507fc5ae8f0e8edcd58cf122da9d78a1bc9eb8cb613906782d57124f` |
| wide_restore | `79e8dff32d6cff08c8cb91c9b3adb51312591b8856fccaf8f83e16f2de100ef5` |
| comb_nowide_ret | `79e8dff32d6cff08c8cb91c9b3adb51312591b8856fccaf8f83e16f2de100ef5` |
| comb_inserts | `7b7fcbcd33d60cc19ba1697e7eec334d5bb3cc7b3bd51b400acb10945f1c8f94` |
| comb_operand | `cd08e7bf08f3b1cdc94a4058c4b8b0cd197e96df94c901f340685bc7f6042319` |
| comb_zero_acc | `f790bbbdf7b0cd9fd26463d440109be43b3d90d3c466b7028dd25d074767f425` |
| comb_zero_ins4 | `1e7d952c821bfaa4d12a51b83a2165a0ff7d108d76a10d9fa8a1ff3950b7b346` |
| comb_zero_entry | `0ec34c5c45206208a7a66a5d4852172a3fba6482ae4fd7de0fe73ce2e03400ef` |
| comb_negative | `bd5a2e285619ba1c546f778f097d4335996b36e0ce23128f4cdcb6a9d0d7f0f7` |
| no_install | `fd2ed601b73dcb47693c8c1953f7b31e2ac48b5131c948c258bf753b5bd0f500` |

All 15 SHAs re-hashed from the images after every run: `BAD: []` (see
`wide_manifest.json` for the full 64-hex values). Raw evidence:
`runs/wi_<case>.acpu.txt`, `runs/wi_<case>.console.txt`,
`runs/drive_wi_<case>.log`; placement detail in `wide_placement.json`.

## 6. Honest limitations

- The magnitude limit is `|v| <= 9999.99` (same as test 84); `10000.0` would
  need an extra GOST word. Not retested here beyond the ceiling case.
- The deck's Fortran source is a dummy; what is proved is that the installed
  contour (the real test-84/test-86 emitted words) executes under the full SIMH
  OS. The FRONT compilation that produced those words is the already-verified
  test 84/86 C-side work, not repeated here.
- `~.besm6/2348` changed during the window as recorded in section 1.1; I did not
  attach it, and all evidence uses the unchanged workspace copy. No SIMH process
  is alive at handoff.
- `CM1П` is at best printed once, early and unreliably in this environment, so
  the stock runner's prompt wait cannot be trusted; the custom `drive.py`
  bypass was required. That is an environment/monitor quirk, not a contour
  failure.

DONE
