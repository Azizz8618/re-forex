# SIMH verification of the zone-2350 `*TRANS` contour — FINAL

> Подтверждение главного агента: `sha256sum ~/.besm6/2348` и эталона
> `/usr/local/share/besm6/2348` совпадают — `f15f25133294c2c3a894f50c85c9c9c7567c0a3eef8ef01b34d1dd2792cc31cd`.
> Инцидент с записью живого диска SIMH в отчёте описан честно; дополнительные
> прогоны A/B делались только на копии. Маркер загрузки `ДATA:` зафиксирован в
> `docs/corrections.md` и `docs/plan-f77-full/36-besm6-deck-runner.md`.

Workspace: `/tmp/.private/azizz/opencode/re-forex-simh`
Isolated tmux socket: `TMUX_TMPDIR=/tmp/.private/azizz/opencode/re-forex-simh/tmux`
Console source throughout: `tmux capture-pane -p -S -2000 -t <my-session>`;
all input via `tmux send-keys ...` + `send-keys Enter`. Session `0` and all
live SIMH processes were never touched. `tools/run_besm6_deck.py` was used
read-only. No repo edits, no git writes, no dispak C patches.

## VERDICT: PASS — the `*TRANS` contour works under the full BESM-6 SIMH OS

The computed marker `21 1.00 3.00` produced by our installed body words is
printed by the OS printer (`prn0`) when `DIS 41(2048)^` + `*TRANS:OURMRK*,,412350`
is submitted. Zeroing the code word or the descriptor removes it; restoring the
image restores it; the no-install control prints `ОТСУТСТВУЕТ OURMRK*` instead.
All five cases used real SIMH boots and real deck input.

## 1. Safety record for `~/.besm6/2348` (important)

The user restored `/home/azizz/.besm6/2348` from `/usr/local/share/besm6/2348`
with SHA `f15f25133294c2c3a894f50c85c9c9c7567c0a3eef8ef01b34d1dd2792cc31cd`.

Two exploratory runs used it at md45 with `-e` exactly as the base ini specifies.
SHA before/after:

| run | before | after |
|:--|:--|:--|
| `simhverify-noinst2` | `f15f2513...` | `f15f2513...` (unchanged) |
| `simhverify-noinst3` | `f15f2513...` | `59f4f9b3c59335725afef085dc623721090aa10fbe2b8d00decdbeda471d6909` |

**SIMH itself wrote to the live disk during the second run** (the OS uses md45
as a writable work disk). This was reported plainly here; per the standing rule
no further live-disk runs were made. The file was repaired with
`cp -a /usr/local/share/besm6/2348 /home/azizz/.besm6/2348` and its SHA returned
to `f15f2513...`. A later recheck found it at `29363feb...` again (a delayed
flush from an earlier SIMH session); it was repaired again. Final state:

```
$ sha256sum /home/azizz/.besm6/2348
f15f25133294c2c3a894f50c85c9c9c7567c0a3eef8ef01b34d1dd2792cc31cd  /home/azizz/.besm6/2348
```

All A/B evidence below was produced with a **workspace copy** at md45:
`disks/md_2348`, SHA before and after the A/B runs
`f15f25133294c2c3a894f50c85c9c9c7567c0a3eef8ef01b34d1dd2792cc31cd`
(SIMH did not write to this copy in those runs). Source:
`/usr/local/share/besm6/2348`, SHA `f15f2513...`.

## 2. Baseline and the stuck wait

The OS boots and reaches its idle loop at `СчАС 04440`, but in this environment
it **never prints `CM1П`**. `tools/run_besm6_deck.py:177` waits on `PROMPT_RE`
(`CM1П`) and therefore blocks forever. Evidence from `capture-pane -S -2000`:

```
  2048 - 41
 ДATA:23.11.26 BPEMЯ:00.31.00
 ЧП(001) 419919810623 00.31 M=000
```

No `CM1П`, no `sim>` in 2000 lines of history. `Ctrl+G` from the terminal
immediately gives `sim> ... Simulation stopped, "СчАС": 04440` — the machine was
idle the whole time.

Bypass implemented in `drive.py` (new file in the workspace, runner untouched):
- primary boot marker is the date banner `[ДD]ATA:` (exact pane line above);
- after 8 s settle: `ДАЙ А0`, `ДАЙ А1`, `Ctrl+G`;
- then `at vu0 <deck>`, `d 6 1`, `d 5 10`, `set cpu req`, `go`;
- completion taken from the ACPU file plus `КЗ/ОЗ/...` in the pane; no prompt
  regex is waited on.

The earlier stock `--hello` and `--source` runs through the runner were accepted
by the OS (task `B075-1`, ACPU dump written to the workspace ACPU file) but the
job ended `СБО`; the runner also reports "изменённые файлы ACPU: []" because it
inspects the live ACPU folder while the custom ini redirects `prn0` into the
workspace. The workspace `ACPU/output.txt` is the real output.

## 3. Disk image construction (and two format traps)

`/usr/local/share/besm6/2048` is **not dense 6-byte**: it is already a tagged
SIMH image, 33,024,000 bytes = 4000 zones × 1032 words × 8 bytes, little-endian
with tag in bits 48..49. Zone headers sit at bytes `0..63` and are duplicated at
`64..127`; data words start at byte 64 of physical zone `logical+4`:

```
offset = (logical_zone + 4) * 8256 + 64 + 8 * word
```

`convert_dense_to_simh.py` (6-byte input, 1000-zone output) is therefore not
applicable. Install words were built in Python from the proven test-86 recipe
(`O412C.FTN` words 0..15 = catalog, 16..34 = body head, `o412d_words.hex` =
body tail, `ovl_our.hex` = descriptor/GOST, `codegen.stream(6, obj)` = overrides),
logical zone `N = 0o2350`.

Two incompatibilities found and fixed (`simh_install.py`):

1. The C `besmtool write` writes a C-side header
   (`w0=(2*zone)<<36|0x0311c588`, `w2=0x419912345678`), which makes SIMH print
   `2048 ДРУГАЯ ДОРОЖКА ... 02350`.
2. Keeping the original all-zero header with new data makes SIMH print
   `2048 НЕТ СОВП.КС ... 02350`.

The SIMH header accepted by the OS:

```
w0 = (phys_zone << 36) | 0x038ca3c918
w1 = 0x000005f1c7800000
w2 = 0x0000410300000000
w3 = end-around-carry sum of the 1024 48-bit data words
w4..w7 = w0..w3 with phys_zone+1
```

Verified against original populated zones 4, 5, 10, 100 (checksum reproduces
exactly). Zones `N+3..N+40` are already zero and keep their original headers.

## 4. LUN mapping

Boot console with stock md41: `2070 - 41`. With the contour image attached to
md41: `2048 - 41`. Therefore LUN 41 is physical device md41, and `ДИС 41(2048)^`
/ `,,412350` resolves to the image on md41. md45/2348 is a separate work disk.
Key ini lines used for every A/B run (`simh_ini_normal.ini`, same for variants
with only the md41 path changed):

```
set -n console log=/tmp/.private/azizz/opencode/re-forex-simh/logs/log.txt
attach -e md41 /tmp/.private/azizz/opencode/re-forex-simh/disks/simh_normal
attach -e md45  /tmp/.private/azizz/opencode/re-forex-simh/disks/md_2348
load /tmp/.private/azizz/opencode/re-forex-simh/boot_dispak.b6
```

Every other attached image (drums, md06/01/02/04/05/07/21/42/43/44, all mg,
prn/vu) is a workspace copy; paths were rewritten by `make_ini.py`.

Deck (`deck_trans.b6`):

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

## 5. A/B results (all in SIMH)

| case | installed image SHA-256 (first 16) | body word zeroed | ACPU line after `*TRANS:OURMRK*,,412350` | marker |
|:--|:--|:--|:--|:--|
| normal | `0b1f8aedfdae47e5` | none | `21 1.00 3.00` | YES |
| zero_code9 | `4b0cc9ae2f6be0f1` | `body[9]` (*64 code) | `00002 0 3.00` | no |
| zero_desc | `c936393329a8520f` | `body[21]` (`0o25` descriptor) | garbage bytes | no |
| restore | `0b1f8aedfdae47e5` | none (same image as normal) | `21 1.00 3.00` | YES |
| no_install | `fd2ed601b73dcb47` | no contour installed | `ОТСУТСТВУЕТ  OURMRK*` / `СВОБОД 01770` | no |

Console exemplar (`simhverify-s2-normal`, capture-pane, tail):

```
  2248 - 01
  2061 - 21
  2048 - 41
 ДATA:23.11.26 BPEMЯ:00.31.00
 ЧП(001) 419919810623 00.31 M=000
ДАЙ А0
 ECTЬ
ДАЙ А1
 ECTЬ
Simulation stopped, "СчАС": 04440 (-> цикл 4440(15), цикл 4432(1))
sim> at vu0 /tmp/.private/azizz/opencode/re-forex-simh/deck_trans.b6
sim> d 6 1
sim> d 5 10
sim> set cpu req
sim> go
 B075-1 410300000000
 ОЗ(075) 410300000000 00.31 M=077
```

ACPU excerpt (`runs/s2_normal.acpu.txt`):

```
*NАМЕ ОURМRК
           *ТRАNS:ОURМRК*,,412350
 21 1.00 3.00
 ДАЙ ТРАКТЫ          +272109334312⏨-19    0010020000000016
```

The `ОЗ(075)` console line is the OS's task-completion notation in this build;
the decisive evidence is the ACPU printout above. `no_install` prints
`ОТСУТСТВУЕТ OURMRK*`, which proves the marker is not coming from a monitor
resident module or from the deck itself.

Raw evidence files: `runs/s2_<case>.console.txt`, `runs/s2_<case>.acpu.txt`,
`runs/drive_s2_<case>.log`.

## 6. Honest limitations

- This verifies the **static/computed `21 1.00 3.00`** marker, not the wide
  `21 1234.56 2470.12` variant or the test-86 BESM chains.
- The OS never prints `CM1П`, so the stock runner cannot complete; the custom
  `drive.py` bypass was required. That is an environment/monitor quirk, not a
  contour failure.
- The live `~/.besm6/2348` was written by SIMH in an early exploratory run and
  was restored; A/B used a workspace copy. No further live runs were made.

DONE
