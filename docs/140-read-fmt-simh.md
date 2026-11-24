# D1: decisive formatted-READ feasibility for the autonomous F77 contour

> РЕЗУЛЬТАТ: **PASS** под авторитетным SIMH. `READ 100,X` и data‑карта
> читаются machine‑кодом из буфера `0o64000+`. Один образ `5916e0e4…`:
> `12.34 → 21 -0012.34`, `56.78 → -0056.78` (только data‑карта), PATCH →
> `-0013.57`, restore → `-0012.34`; data до `END`, control literal и базовый образ
> с READ‑dek → `0000.00`. Все `КОНЕЦ ЗАДАЧИ`. Причины прежних no‑result:
> port collision 6300+N, проверка только console, отсутствующий `C-g` и неполный
> handoff `ДАЙ A0`→`НОМВ`; исправлено в `drive_manual.py`.

## VERDICT

* **Task 1 (are DATA cards in RAM at contour entry?): PASS, FACT.** Data cards following the
  Fortran source are present in RAM `0o64000+`, with an exact, reproducible byte layout.
* **Task 2 (machine-code READ scanner): PASS as a mechanism.** A 41-word BESM-6 scanner in
  the contour body finds the DATA card, decodes its digits with the verbatim B1/B5 digit
  path, and feeds the value into the contour's variable cell before the untouched
  LEX/parser prints it through the proven GOST path. No host value, no `777005`, no
  compiler, no source-card literal substitution.
* **Task 3 (decisive A/B/PATCH/RESTORE): PASS under authoritative full SIMH** (and
  under the C-oracle). A byte-identical image prints `12.34` vs `56.78` when only the
  DATA card changes; a one-machine-word PATCH prints `13.57`; byte-identical RESTORE
  returns `12.34`. All runs reach `КОНЕЦ ЗАДАЧИ`. The earlier `D1V_*` no-result runs
  were a harness/operator problem (tty-port collision, console-only completion check,
  missing `C-g`, and an incomplete post-job `ЕСТЬ` handoff), diagnosed and fixed in
  `harness/drive_manual.py`.

## 1. Task 1: DATA cards in RAM - FACT

Method: C-dispak oracle (advisory only) run as
`BESM6_CORE_ON_PC=01770, BESM6_CORE_SKIP=6` with image `2048_B9_A` (SHA
`81d7790f...`) and a deck containing the real Fortran source
`READ 100,X / PRINT 200,X / 100 FORMAT(F8.2) / 200 FORMAT(1X,F8.2) / END`, with a
DATA card `   12.34` before or after `END`.

CORE (`oracle/CORE_post/core-pc.bin`, SHA `dc48e568...`) at contour entry:

```
064030  86 45 4e 44 ca 0a   <6sp>END<74sp>\n      <- END card
064031  83 31 32 2e 33 34   <3sp>12.34           <- DATA card (digits bytes 1..5)
064032  cb 0a 0a 0a 0a 0a   <75sp>\n\n\n\n\n     <- terminator
064033  2a 45 58 45 43 55   *EXECU
```

`0x83` = 3 RLE spaces; `31 32 2e 33 34` = ASCII `12.34`, dot at byte 3. For
`   56.78` the word is `83 35 36 2e 37 38`. With the DATA card BEFORE `END` the same
word appears at `0o64030` and `END` moves to `0o64032`. A byte-3 scan of all card
words in the CORE finds `0x2e` **only** in the DATA card word (the `F8.2` dots in
FORMAT cards sit at byte 2 or byte 5).

* FACT: raw deck text, including DATA cards, is in RAM `0o64000..` at contour entry.
* FACT (docs/93 §1.1, docs/94 §3): `utc 60000` + short `xta` reads that page in user
  mode (MMU page `0o150` permitted); our MTR confirms the read at `0o21203R`.
* INFERENCE only: the band is the monitor's AIO/card buffer filled by MONREAD*
  (`boot.asm:3`, `monread%.asm`); the storing instruction was not traced.

## 2. Task 2: implementation

Base image: byte-identical copy of `2048_B9_A` (SHA `81d7790f...`). Only N+1 body
words change: `body[0o11]` (RAM `0o1770`) now jumps to a scanner in the proven-free
band `body[0o1300..0o1600]` (docs/120), which ends with `LONG UJ 0o27740` into the
untouched LEX/parser. N+2, N+3, `body[0o26]` and forbidden band `526..900` unchanged.

Machine halfwords (41 words at RAM `0o21200..0o21250`, data 22 words at
`0o21300..0o21324`):

1. `utc 20000; xta 1300; ati 12` - load N+2 base into M[12] (one-shot UTC needed:
   data cells are above 12-bit ADR).
2. For k=0..31: `utc 60000; xta 4000(11)` reads card word `0o64000+k`; `asx`
   right 16, `aax 0xff`, `aex 0x2e`, `uza` detects the dot at byte 3. The bound test
   uses logical `aex 0o40` (using `arx` here leaves multiplicative RAU and changes
   the `uza` condition).
3. Four digits decoded with the **verbatim B1/B5 path**: `asx` byte extraction
   (right 32/24/8/0; zero-shift control is `64<<41`, NOT `0`), `aax 0x0f` (ASCII low
   nibble), `e+x EMASK`, `e+x C105` (integer->float), `F=F*10+digit` (`a*x`, `a+x`).
4. Two `a/x 10` divisions give `12.34`/`56.78`; one `a*x SCALE` applies the 10x
   factor that the contour's variable cells require (MTR-confirmed: `S_PRINT` loads
   `N+2[0o1637+32+VIDX]`, VIDX=1 -> RAM `0o21700`).
5. Store to `0o21700`; untouched contour compiles/prints through the proven GOST path.

Defects found and fixed via MTR: circular M[12] load, halfword-vs-word branch targets,
`ARX`/`UZA` RAU polarity, `ASX 0` semantics, variable-cell address, and 10x scaling.

## 3. Task 3: decisive gates

### C-oracle (advisory, full job stream, all `КОНЕЦ ЗАДАЧИ`)

| gate | image | deck | `prn` line |
|:--|:--|:--|:--|
| A | `2048_D1_A` (`5916e0e4...`) | `deck_READ_post.b6` (`12.34`) | ` 21 -0012.34  3000.00` |
| B | same byte-identical image | `deck_READ_post56.b6` (`56.78`) | ` 21 -0056.78  3000.00` |
| PATCH | `2048_D1_PATCH` (`374d4c53...`) | deck A | ` 21 -0013.57  3000.00` |
| RESTORE | `2048_D1_RESTORE` == A | deck A | ` 21 -0012.34  3000.00` |

A/B differ only in the DATA card byte field. PATCH changes one machine word (`SCALE`
f32(10)->f32(11), 3 differing image bytes including recomputed checksum); RESTORE is
byte-identical to A and returns `12.34`. Raw logs: `oracle/D1F_{A,B,P,R}/out.txt`.

### Authoritative full SIMH - PASS

Binary verified on every run: `d058305796bcd0aaf108056f595ee2a222762abe31cf3bb59f1697c9473ca675`.
Harness: `harness/drive_manual.py` (copies of `setup_b.py` ini logic), with every
`attach ttyN Line=N,PORT` shifted to `6300+N` (docs/135/137), no tty line commented,
and no artificial `go` at `>>> MUX: clear`. The sequence that launches the queued
job is: boot marker `ДATA:` -> `ДАЙ А0` / `ДАЙ А1` / `НОМВ` -> `C-g` -> `at vu0 <deck>`,
`d 6 1`, `d 5 10`, `set cpu req`, `go` -> after `B075-1`/`ОЗ(075)`, `ДАЙ А0` then
`НОМВ` -> poll **prn0** for the product. All captures in `harness/runs/`.

| gate | case | image (SHA prefix) | deck | prn0 `21` line | verdict |
|:--|:--|:--|:--|:--|:--|
| A | `D2_B` | `2048_D1_A` `5916e0e4...` | `deck_READ_post.b6` (`12.34`) | ` 21 -0012.34  3000.00` | PASS |
| B | `D2_C` | same byte-identical image | `deck_READ_post56.b6` (`56.78`) | ` 21 -0056.78  3000.00` | PASS |
| PATCH | `D2_D` | `2048_D1_PATCH` `374d4c53...` | deck A | ` 21 -0013.57  3000.00` | PASS |
| RESTORE | `D2_E` | `2048_D1_RESTORE` == A | deck A | ` 21 -0012.34  3000.00` | PASS |
| pre-END data card | `D2_F` | `2048_D1_A` | `deck_READ_pre.b6` (`12.34` before `END`) | ` 21 -0012.34  3000.00` | PASS |
| control literal | `D2_G` | `2048_B9_A` (unmodified base) | `deck_Xlit.b6` (`X=12.34`) | ` 21 -0012.34  3000.00` | PASS |
| no scanner | `D2_H` | `2048_B9_A` (unmodified base) | `deck_READ_post.b6` | ` 21  0000.00  3000.00` | PASS (non-regression) |

Every gate shows `КОНЕЦ ЗАДАЧИ` in prn0; verdict JSONs `verdict_D2_{B..H}.json`
all have `product_gate: PASS`. Causality: A vs B uses one byte-identical image and
changes only the DATA-card digits; PATCH changes one machine word (`SCALE`
f32(10)->f32(11)) plus recomputed checksums and changes the printed value;
RESTORE is byte-identical to A and returns `12.34`. The unmodified base with the
same READ deck prints `0.00`, proving the printed value is produced by our
machine-code card scanner, not by the compiler or a host substitution.

### Root cause of the earlier `D1V_*` no-result runs (all fixed)

1. The lead's `D1V_*` consoles show `Sockets: bind error 98` / `Can't open network
   port: 63xx` - another SIMH instance owned the fixed `6300+N` ports. A free
   moment was used for the decisive re-run (no `bind error` in `D2_*` consoles).
2. `tools/forex500-final/drive_b.py` only checks the **console** for completion
   (`COMPLETION.search(txt)`); printer output lives in prn0, so a completed job
   was reported `N/A`. `drive_manual.py` polls prn0 for `21` + `КОНЕЦ ЗАДАЧИ`.
3. A `C-g` break into `sim>` is mandatory before `at vu0`; without it the deck
   commands were swallowed by the OS console (garbled `HШИФ` echoes).
4. In this shared job queue a plain post-job `НОМВ` gets `HET`; the working
   handoff is `ДАЙ А0` followed by `НОМВ`, after an 8 s settle.

## 4. Word budget / invariants

| resource | D1_A | limit | verdict |
|:--|--:|--:|:--|
| N+3 converter | 55 | 58 | unchanged |
| N+2 changed words | 543 | 649 | unchanged vs B9_A |
| N+2 forbidden band 526..900 | 0 | 0 | PASS |
| body N+1 changed words | 545 (B9_A 482 + 63) | 998 | PASS |
| keeper `body[0o26]` | `0o1000040000000` | preserved | PASS |
| new scanner | 41 code + 22 data | 224 free words in band | PASS |

## 5. Supported subset (honest)

* Supported: one DATA card whose field matches `   dd.dd` (F8.2, two integer and
  two fractional digits, no sign/exponent), located within the first 32 raw card
  words; value delivered to the first Fortran variable (VIDX=1, normally `X`) in
  a deck with `READ <label>,X` and a following DATA card; all digit decoding and
  arithmetic on-machine; print through the existing `FORMAT(1X,Fw.d)` GOST path.
* Unit handling: no LUN is consulted. The deck is the job's own input stream
  (unit 5 / card reader equivalent); unit 10 or any OS-opened file is NOT supported.
* Not supported: arbitrary `Fw.d` widths/positions, signs, exponents, multiple DATA
  cards, EOF/ERR/IOSTAT, OPEN/CLOSE/INQUIRE, arrays, more than one READ variable,
  and true descriptor-driven `READ(u,fmt)` semantics. This is a raw-card-buffer
  numeric-field READ, the missing primitive of docs/91/92, not a full formatted READ.

## 6. Reproduce

```
cd /tmp/.private/azizz/opencode/d1-read
python3 build/read_build.py --build 2048_D1_A
python3 build/read_build.py --build 2048_D1_PATCH --scale 11
cp images/2048_D1_A images/2048_D1_RESTORE
python3 build/oracle_run.py A images/2048_D1_A decks/deck_READ_post.b6
python3 build/oracle_run.py B images/2048_D1_A decks/deck_READ_post56.b6
python3 build/oracle_run.py P images/2048_D1_PATCH decks/deck_READ_post.b6
python3 build/oracle_run.py R images/2048_D1_RESTORE decks/deck_READ_post.b6
python3 build/oracle_core.py CORE images/2048_B9_A decks/deck_READ_post.b6 01770
# authoritative SIMH (one case at a time; free tty 6300+N ports required):
python3 harness/drive_manual.py --case A --deck decks/deck_READ_post.b6 --image images/2048_D1_A --session a
python3 harness/drive_manual.py --case B --deck decks/deck_READ_post56.b6 --image images/2048_D1_A --session b
python3 harness/drive_manual.py --case P --deck decks/deck_READ_post.b6 --image images/2048_D1_PATCH --session p
python3 harness/drive_manual.py --case R --deck decks/deck_READ_post.b6 --image images/2048_D1_RESTORE --session r
```

## 7. Safety

Copies only: workspace under `/tmp/.private/azizz/opencode/d1-read/`, bulky images
under `/dev/shm/d1-read/`. No repo file, live disk, tmux session 0, SIMH binary or
C `dispak` source was modified. The temporary SIMH console experiments used only
workspace copies and isolated tmux sockets.

DONE
