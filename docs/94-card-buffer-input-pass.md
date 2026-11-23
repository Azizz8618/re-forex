# read-ctx: on-machine card-input primitive for the zone-2350 contour

> ГЛАВНЫЙ РЕЗУЛЬТАТ: **PASS** с оговоркой. При байтово тождественном образе
> контура (`f23376b2…`) дек `X=1.0` даёт `21 1.00 3.00`, `X=2.0` — `21 2.00
> 3.00`, restore возвращает исходное. Более сильный A/B: `X=12` -> `2112.00`,
> `X=34` -> `2134.00` ( image `b0d25b04…`) — две цифры декодируются на машине
> из байтов 3–4 слова карты по `0o64012` (`utc 60000` + `xta 4012`).
> Патч только бита привилегии для `э52` на копии **не помог** (`ЗАПРЕЩ.ЭКСТРАКОД`),
> значит этого мало — требуется больший контекст супервизора.
> Оговорка: это буквальный/числовой ввод из сырого буфера карты, НЕ
> дескрипторный formatted READ (`READ(u,fmt)` по-прежнему заблокирован).

Date: 23.11.2026. Workspace: `/tmp/.private/azizz/opencode/read-ctx/`
(bulky copies under `bulk/`, moved there from `/dev/shm` when that tmpfs filled
from other workspaces). Repo, live disks, tmux session 0, SIMH binary and
dispak C sources were never edited. Every attached image was a COPY. C
`dispak` was used only as an MTR/CORE oracle; no C run result is claimed as
authoritative. Authoritative A/B is full SIMH.

## VERDICT: PASS (with an explicit scope limit)

One byte-identical contour image prints different numbers when only the DECK
literal changes:

| case | deck line | image SHA-256 (identical) | authoritative SIMH ACPU line |
|:--|:--|:--|:--|
| A | `      X=1.0` | `f23376b2…` | ` 21 1.00 3.00` |
| B | `      X=2.0` | `f23376b2…` | ` 21 2.00 3.00` |
| restore | `      X=1.0` | `f23376b2…` (byte-identical) | ` 21 1.00 3.00` |

All three reached `КОНЕЦ ЗАДАЧИ`. A second, stronger A/B parses a TWO-character
numeric field from the same card word:

| case | deck line | image SHA-256 (identical) | SIMH ACPU line |
|:--|:--|:--|:--|
| C | `      X=12` | `b0d25b04…` | ` 2112.00 3.00` |
| D | `      X=34` | `b0d25b04…` | ` 2134.00 3.00` |

Both reached `КОНЕЦ ЗАДАЧИ`. The differing digits (`12` vs `34`) come from two
distinct ASCII bytes of the deck card word, decoded on the BESM-6.

Positive control (same harness, `xta` instead of an extractcode): `01 1.00 3.00`,
`КОНЕЦ ЗАДАЧИ` (image `2048_posctl`, SHA `3195a4f9…`).

**SCOPE LIMIT - do not overclaim.** This proves **on-machine capture and decode
of literal/numeric-field text from the monitor's raw card buffer in RAM
`0o64000..`**, plus the existing FPU->GOST print path. It is **NOT**
descriptor-driven formatted READ: there is no LUN, no format descriptor, no
`*52`/`*60`/INPUT* chain, and no `E`-terminated input array. Call it
*literal / numeric-field input from the card buffer*, the primitive that was
missing in docs/91. A true `READ(u,fmt)` remains blocked (docs/91/92).

---

## 1. What was tried, and the result of each attempt

| # | attempt | verdict | evidence |
|:--|:--|:--|:--|
| 0 | user-mode input extractcodes (`э52`, `э60`, `э70`) from the contour, as in docs/91 | **FAIL** | `ЗАПРЕЩ.ЭКСТРАКОД`, `МАССИВ НЕ СУЩ-Т.`, `ПЕРЕПОЛНЕНА ТАБЛИЦА ОПИСАНИЙ` (docs/91; reproduced again this session, `acpu_*.txt`) |
| 1 | minimal copied-disk/OS-state change: set the task privilege bit `M[0o72512] \|= 0o100000` from our contour code at runtime (SIH console deposit also tested), plus a 2-word COS descriptor pointing at RAM `0o30170` | **FAIL** | still `ЗАПРЕЩ.ЭКСТРАКОД` after the patch: ACPU line `0000000000100000`. Minimum patch is therefore **not sufficient** (or the runtime write did not reach the word the handler tests; see FACT/INFERENCE). |
| 2 | raw card-buffer literal input, single digit, `X=1.0`/`X=2.0` (proven technique of docs/93, independently rebuilt here) | **PASS (A/B/A)** | table above; MTR §3 |
| 3 | raw card-buffer numeric field, two characters, `X=12`/`X=34`, decoded on-machine to two GOST digit bytes | **PASS (A/B)** | table above; MTR §3 |

Attempt 1 detail (FACT): the SIMH console deposit at the contour breakpoint was
verified byte-for-byte:

```
> ex 474
474:  6700 0000 0007 2451
> ex 72512
72512: 7774 2546 4000 0000
> d 72512 7774254640100000
> ex 72512
72512: 7774 2546 4010 0000     ; 0o100000 bit set
```

The contour-internal variant (`build_priv52.py`, runtime `UTC 72512` +
`сч`/`или`/`зп`) produced the same ACPU refusal. No SIMH binary or product
image was patched; this was a runtime state change in an isolated SIMH session
on copied images.

---

## 2. Decisive method (FACT)

Deck contains only the standard job cards and the contour translator; no
`*FOREX`, `*FTN`, `*perso`:

```
ШИФР 410300 ЗС5^
ДИС 41(2048)^
ОЗУ 32^АЦП 32^
ЕЕВ1А3
*NAME OURMRK
*TRANS:OURMRK*,,412350
      PROGRAM MAIN
      X=1.0              <-- only line changed for A/B
      END
*EXECUTE
*END FILE
``````
ЕКОНЕЦ
```

The contour entry substitution is the proven `body[0o11] (RAM 0o1770 L) =
LONG uj 30114`; routine/constants live in the 58 clean words `0o30114..0o30205`
of zone N+3. Input sequence for variant `single` (verbatim docs/93 routine):

1. `30114R utc 60000` arms M20 for next left halfword.
2. `30115L xta 4012` reads `0o60000+0o4012 = 0o64012`, the raw card word.
3. `30116L asx` right 16, `30117L aax 0o377` isolate the ASCII digit byte
   (`0o61`/`0o62`).
4. `30120L arx +0xd0`, `30121L aax 0o377` convert ASCII to GOST digit
   (`1`/`2`) without host substitution.
5. `30122L asx`/`30123L arx` form a BESM-6 float `1.0`/`2.0` on the machine.
6. Proven docs/89 chain (`a/x`, `aex`, `e+x`, `aax`, `asx`, `arx`, `atx`)
   deposits the digit into GOST word A at RAM `0o2006`; resident `*64 2004`
   prints it; `UJ 0(15)` returns.

Variant `twochar` instead isolates byte 3 (tens) and byte 4 (ones) of the same
card word with `asx` right 16 / right 8, converts each ASCII digit to a GOST
digit with the same `+0xd0`/mask trick, shifts them left 24 / left 16, adds the
baseline GOST word and prints. Both digits are produced by machine execution.

SIMH rules respected: isolated `TMUX_TMPDIR`, console only via
`capture-pane -p -S -2000`, all input via `send-keys`, `ДATA:` boot marker,
`ДАЙ А0` / `ДАЙ А1` / `НОМВ` before the deck, post-job-start `НОМВ`, MTR traces.
One deviation, disclosed: because other concurrent SIMH sessions from other
workspaces share the stock `ACPU/output{,1}.txt`, the printer files in **our
copies of the ini** were redirected to workspace-local files
(`prn0_<case>.txt`, `prn1_<case>.txt`). Stock `-n prn` devices are otherwise
unchanged. This was required for a clean A/B.

---

## 3. Raw MTR evidence (C `dispak` oracle, read-only)

Single-digit variant, same image, two decks. Digit path, per halfword:

```
===== deck X=1.0 =====
MTR 30115L xta    64012(0) AU=0200600002006 ... 20=60000
MTR 30117R utc    30000(0) AU=0000000000061   ; ASCII '1' from card byte 3
MTR 30121R utc    30000(0) AU=0000000000001   ; integer 1
MTR 30123R utc    30000(0) AU=4050000000000000 ; BESM float 1.0
MTR 30135R utc    30000(0) AU=0000000000001   ; GOST digit 1
===== deck X=2.0 =====
MTR 30115L xta    64012(0) AU=0200600002006 ... 20=60000
MTR 30117R utc    30000(0) AU=0000000000062   ; ASCII '2'
MTR 30121R utc    30000(0) AU=0000000000002
MTR 30123R utc    30000(0) AU=4110000000000000 ; BESM float 2.0
MTR 30135R utc    30000(0) AU=0000000000002
```

Two-character variant (deck `X=12` vs `X=34`):

```
===== X=12 =====
MTR 30117R utc 30000 AU=...061   ; tens ASCII '1'
MTR 30121R utc 30000 AU=...001   ; GOST tens 1
MTR 30126R utc 30000 AU=...062   ; ones ASCII '2'
MTR 30130R utc 30000 AU=...002   ; GOST ones 2
===== X=34 =====
MTR 30117R utc 30000 AU=...063   ; '3'
MTR 30121R utc 30000 AU=...003
MTR 30126R utc 30000 AU=...064   ; '4'
MTR 30130R utc 30000 AU=...004
```

Raw CORE at contour entry (`core-pc.bin`, 6 bytes/word) confirms the source
bytes in RAM `0o64012`:

```
064012 4145407514231311  86 58 3d 31 32 c9   .X=12.     (deck X=12)
064012 4145407514227060  86 58 3d 31 2e 30   .X=1.0     (deck X=1.0)
```

Full traces: `oracle/oracle/{sx1,sx2,tx12,tx34}/out.txt`,
`oracle/oracle/{x12,sx1}/core-pc.bin`.

---

## 4. SHAs (SHA-256)

```
a98e81090d4b254554a0cd3ff8611438615de84fc012e8e2b70fbabc2ebdc796  bulk/images/2048_base       (repo tool baseline)
3195a4f927aaf5702e3b93ffd0f3ac8e3c6236102136f8910b41a28c1e6fed3b  bulk/images/2048_posctl     (positive control)
f23376b20a0f5529b40cb1fadfacde5e1473609fea874a815bada4fb6b81d921  bulk/images/2048_readA      (A, B and restore, byte-identical)
b0d25b04c12f8d0b75c5e4024a0e6bf20c407b1ada6abfd661a9b94960314781  bulk/images/2048_read12b    (C and D, byte-identical)
d9e3011027174a75610a9e720cb8bc6f6af5586896d17243586554faa8e5cf43  bulk/images/2048_priv52     (attempt 1)
c07a2b359bd1b0c1f359128818f5bdb7da436a59f6f28c60bb723bc493529dd0  decks/deck_x1.b6            (X=1.0)
11b4c8bed5c2b2da27652e8da3f52bd354d484ab66a9210451fb9512e4b7fee3  decks/deck_x2.b6            (X=2.0)
67c80729b1f9a75d067ad35abef79841afa81f54fdb940f6dd0ff7fb222b6b96  decks/deck_x12.b6           (X=12)
042bfe9eca7df76f4120af826af6eaa96f34417eb6b039504254f839e3a52899  decks/deck_x34.b6           (X=34)
7717b3255054e009a579c2eeb882e1853745cb7267adde6c4a8f8c65663a4edc  runs/acpu_readA.txt
dd4484b10422e68061e4e72e9cb308f2260ed401245f159f3e8094247410b6ef  runs/acpu_readB.txt
0abad748058b4d254826ddf1a6da8e2d5214c83499f322157842fdc38fff3de0  runs/acpu_readRESTORE.txt
920e44d93cd4540c17298067f24bfff87491874acc8e138476200b7da0984faa  runs/acpu_read12b.txt
24f12593bb19571c8adfa9fe1b69f19882b02458888383218d72b4ffd0bfb16b  runs/acpu_read34b.txt
13f1604a26fc816189b955d8f8d32591646ded746d4b1ce7caac2f3d53513ca6  runs/acpu_priv52.txt
```

---

## 5. FACT vs INFERENCE

| # | statement | marker |
|:--|:--|:--|
| 1 | Deck text is present as raw 6-byte words at RAM `0o64000..` at contour entry; page `0o150` is readable in user mode | FACT (CORE + MTR; no protection trap) |
| 2 | `utc 60000` + short `xta 4012` reads `0o64012`; ASCII digit at byte 3 (`X=1.0`) / bytes 3-4 (`X=12`) | FACT (CORE + MTR) |
| 3 | Same contour image SHA prints `1.00` / `2.00` and `12` / `34` for the four decks; restore returns to `1.00` | FACT (SIMH ACPU, local prn) |
| 4 | Every digit is computed on-machine (ASCII -> GOST -> FPU or direct GOST deposit); no host-computed value is stored in the image | FACT (MTR ACC chain, builder source) |
| 5 | `э52` refusal is an OS task-permission decision at `05162 R` (`M[0o72451+0o41] & 0o100000 == 0` -> `по 5164`), correlated by parallel research docs/92 | FACT (MTR decoded there; ACPU here) |
| 6 | Setting the privilege bit alone does not make `э52` succeed | FACT (attempt 1 ACPU) |
| 7 | Why setting the bit did not help (runtime write not reaching the tested supervisor cell, or a second missing LUN/descriptor condition) | INFERENCE - SIMH breakpoint traces at `0o30114` captured a different context, so the post-write handler path was not cleanly traced |
| 8 | The `0o64000` band is the monitor's AIO/card buffer filled by MONREAD* | INFERENCE (boot.asm AIO base, monread%.asm, CORE bytes; the storing instruction was not traced) |
| 9 | This is a formatted, descriptor-driven READ | **FALSE - not established.** No LUN/format descriptor/INPUT* is involved; the routine reads literal text at fixed offsets. |
| 10 | A general READ with arbitrary field positions, sign, exponents or EOF semantics would need more code than the 58-word window allows | INFERENCE (docs/90 already fills all 58 words for 4-digit conversion) |

---

## 6. Safety record

* No repo edits: `git status --short` unchanged from entry (` M tools/run_besm6_deck.py`,
  `?? tests/plan-f77/64-monitor-patch/`). No live disks, tmux session 0,
  SIMH binary or dispak C sources were modified.
* All attached disks are copies under this workspace; the source of truth
  `/usr/local/share/besm6/2048` was only read.
* The one OS-state patch (attempt 1) was a SIMH console RAM deposit in an
  isolated session on copies, reverted by ending the session; it is reported
  as a diagnostic, never as product. The successful input path (attempts 2/3)
  needs **no** monitor, loader, disk or emulator patch at all.
* `/dev/shm` copies from this workspace were moved into `bulk/` when that
  shared tmpfs filled from other agents' workspaces.

## 7. Evidence index

* `scripts/build_read.py` - reproducible builders (`single`, `twochar`); copies only.
* `scripts/build_priv52.py`, `scripts/build_ctx.py` - attempt-1 builders.
* `scripts/setup_read.py`, `scripts/drive_read.py`, `scripts/drive_patch.py` - isolated SIMH harness.
* `scripts/c_oracle.py` - read-only C MTR/CORE oracle wrapper.
* `decks/deck_x{1,2,12,34}.b6` - A/B/A and two-character A/B decks.
* `bulk/runs/acpu_{posctl,readA,readB,readRESTORE,read12b,read34b,priv52}.txt` - raw SIMH printer output.
* `bulk/runs/drive_*.log`, `bulk/runs/console_*.txt`, `bulk/runs/ini_*.ini` - driver transcripts/configs.
* `oracle/oracle/{sx1,sx2,tx12,tx34}/out.txt` - raw C MTR excerpts.
* `oracle/oracle/{x12,sx1}/core-pc.bin` - raw CORE at contour entry.

DONE
