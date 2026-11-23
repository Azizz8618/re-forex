# C5 — FORMAT-like field width (`Fw.d`) from an IR record drives the contour GOST layout

> РЕЗУЛЬТАТ C5: **PASS** — ширина печати из IR. Нативного FRONT‑пути для
> FORMAT нет (`777011` отсутствует, FORMAT/PRINT идут в `777002`); используется
> build‑фикстура `TK=5, TO=w, TA=d` в том же формате `777005`, без выдумывания
> нового типа записи. SIMH на байтово том же образе: `w4d2 → -0034.50`,
> `w2d2 → -  34.50`, `w4d1 → -0034.5 `, `w3d2 → - 034.50`; правка слова N+2
> даёт тот же эффект, restore возвращает. 6/6 `КОНЕЦ ЗАДАЧИ`. Бюджет
> 54/58 слов N+3 + 8 слов N+2. Образ `2c543a7e…`, все 6 гейтов SIMH.

Date 23.11.2026. Workspace `/tmp/.private/azizz/opencode/c5-format/`
(bulky copies on `/dev/shm/c5-format`, symlinked; `/tmp` was 100% full, as in
docs/95/111). Copies only: no repo, live disk, tmux session 0, SIMH binary or
C `dispak` sources were edited. C `dispak` was **oracle only** (MTR/CORE,
docs/88); authoritative A/B/C results are full SIMH ACPU/printer captures with
a workspace-local `-n prn0`. Deck contains only `ДИС 41(2048)^`,
`*NAME FRX5XX`, `*TRANS:FRX5*,,412350` plus standard framing; no `*FOREX`,
`*FTN`, `*perso`.

---

## 1. IR encoding decision (FACT vs INFERENCE)

**Decision: a BUILD-TIME TEST FIXTURE `777005` record, not a native FRONT
FORMAT record.** Fields follow the proven `1X,6I8` contract:

```
  777005       6       5       w       d       0
                       ^       ^       ^
                       TK=5    TO=w    TA=d      (TB=0)
```

The two decimal digits are carried in the SAME card word as the C3 operator
token (RAM `0o64014`): byte 0 = last digit of `TO` (w), byte 2 = single digit
of `TA` (d). CORE at contour entry proves it (`logs/card_buffer_w4d2_at_entry.txt`):

```
064012  82 37 37 37 30 30    .77700
064013  35 87 36 87 35 87    5.6.5.
064014  34 87 32 87 30 a3    4.2.0.
        ^^     ^^
        w=4    d=2   (ASCII 0x34 / 0x32)
```

| statement | marker | citation |
|:--|:--|:--|
| `777005 <seq> <TK> <TO> <TA> <TB>` text is `1X,6I8` | FACT | `src/newcomp/FRONT.FTN:54`, `:346-349`, `:376` |
| FRONT emits `TK=1` LIT, `TK=2` VARIABLE, `TK=3/4` operators only | FACT | `FRONT.FTN:254-259`, `:262-276`, `:299-345` |
| FRONT rules 34 PRINT / 35 FORMAT stream raw source into `777002`, not a structured width record | FACT | `FRONT.FTN:22-23`, `:164`, `:173`, `:204` |
| `777010` (READ) and `777011` (FORMAT `K,R,W,D`) emitters are **absent from this repo** | FACT | `docs/99-frext-ir-input.md:83-89`; `docs/77-onmachine-format-limit.md:7`; `docs/106-final-limits.md:56`; repo-wide grep finds no emitter |
| An on-machine hand-written FORMAT/PRINT inside 58 words previously FAILED | FACT | `docs/77-onmachine-format-limit.md` (`ЗАПРЕЩ.КОМАНДА`, no numeric line) |
| `TK=5, TO=w, TA=d` is a **test-fixture encoding produced by the build step**; it is NOT a native FRONT FORMAT record and does not invent `777011` | FACT (this task) | `build/make_decks.py`; no `777011` in any deck or image |
| `777011` would follow `1X,NI8` like the other records | INFERENCE only | emitter absent (docs/99:203) |

A native FRONT route was checked first and rejected with the citations above:
FRONT's FORMAT/PRINT rules produce `777002` ASCII, and parsing that in 58
words was already proven to fail (docs/77). The fixture reuses the real
`777005` marker and its real `1X,6I8` layout, so the machine decoder is the
same hardware path as docs/99/111 (no new record type is claimed).

## 2. Machine implementation (reuse first)

Reused **verbatim**: repo `tools/build_zone2350_contour.py` checksum/zone
writer; docs/105 `final_sign.S` converter with sign block, `floor_acc`,
`drop_last_ati` and shared `floor_int` VJM at `0o30177` (docs/98 reclaims);
docs/98/105 seeded GOST text words `0o2006..0o2011`; docs/93/99 card read
`utc 60000` + short `xta 4014`; docs/109/110 N+2 free words via
`utc 20000` + indexed short ADR; docs/100 SIMH harness; resident `*64 2004`.

New code is only the front end in `build/c5_build.py` (27 halfwords):

```
30114L utc 60000        ; card page
30114R xta 4014         ; IR card word RAM 0o64014
30115L atx CARD         ; keep for second field
30115R asx SR40         ; byte 0 = w (TO digit)
30116L aax M8 ; 30116R arx NEG31 ; 30117L ati 6   ; M[6]=w
30117R xta CARD ; 30120L asx SR24                 ; byte 2 = d (TA digit)
30120R aax M8 ; 30121L arx NEG31 ; 30121R ati 7   ; M[7]=d
30122L utc 20000 ; 30122R xta 21635(6)            ; w -> N+2 mask offset 0..2
30123L aex 2006 ; 30123R atx 2006                 ; blank seeded leading zeros
30124L utc 20000 ; 30124R xta 21641(7)            ; d -> N+2 clear-mask offset 3..4
30125L aax 2007 ; 30125R atx 2007                 ; clear F2 byte when d=1
30126L utc 20000 ; 30126R xta 21643(7)            ; d -> N+2 space-add offset 5..6
30127L arx 2007 ; 30127R atx 2007                 ; put GOST space at F2
30130L utc 20000 ; 30130R xta 21646               ; pre-seeded operand (N+2[7])
30131L atx EST                                    ; -> verbatim docs/105 converter
```

Addressing fact (SIMH `besm6_cpu.c:1098-1102`): `UTC` arms a modifier that is
added to the next instruction's address **before** its own index register, so
`utc 20000` + `xta 0o1635(6)` with `M[6]=4` addresses `0o21641` = N+2 offset 2
(MTR confirms `xta 21635(6)` with `M[06]=00004`).

N+2 table (all 8 words inside the proven-free offsets `0..525`, docs/110;
`526..900` untouched):

| offsets | content | w/d values |
|:--|:--|:--|
| 0..2 | XOR masks for GOST word A chars 4,5 (two seeded leading zeros) | w=2 → `0o7417`, w=3 → `0o7400`, w=4 → `0` |
| 3..4 | AND clear masks for GOST word B char 4 (F2 digit) | d=1 → clears F2, d=2 → all ones |
| 5..6 | ADD words restoring GOST space (decimal 15 = octal 17) at char 4 | d=1 → `0o7400`, d=2 → `0` |
| 7 | operand float (345.0), same role as docs/98 `NUM` | input, not a result |

The GOST layout itself is unchanged: word A `21`, sep, sign, two seeded zeros;
word B low int digits, point, F1, F2, trailing space. Width is honoured by
blanking padding bytes; fractional count by blanking the F2 byte *after* the
converter deposits it. No host-computed digit is stored: MTR shows
`asn 30 AU=3`, `asn 40 AU=4`, `asn 60 AU=5`, `asn 70 AU=0` before
`atx 2007` and `*64 2004` (`logs/MTR_A_clean.txt`).

## 3. Decisive gates (authoritative: full SIMH ACPU/printer)

| gate | image SHA prefix | deck (only difference) | raw SIMH printer line | КОНЕЦ ЗАДАЧИ |
|:--|:--|:--|:--|:--:|
| A baseline | `2c543a7e…` | w4d2 | ` 21 -0034.50  3000.00` | yes |
| B width | `2c543a7e…` **byte-identical** | w2d2 (1 byte: `4`→`2`, pos 157) | ` 21 -  34.50  3000.00` | yes |
| C fraction | `2c543a7e…` **byte-identical** | w4d1 (1 byte: `2`→`1`, pos 165) | ` 21 -0034.5   3000.00` | yes |
| D width | `2c543a7e…` **byte-identical** | w3d2 (1 byte: `4`→`3`, pos 157) | ` 21 - 034.50  3000.00` | yes |
| PATCH | `b87cc87e…` (one N+2 machine word) | same as A | ` 21 -  34.50  3000.00` | yes |
| RESTORE | `2c543a7e…` (= A) | same as A | ` 21 -0034.50  3000.00` | yes |

Deck A vs B: `cmp -l` = exactly one byte (1-based 157, `0x34`→`0x32`).
Image A vs PATCH: N+2 word 2 `0 → 0o7417` plus its two recomputed zone
checksum copies, 6 byte diffs at 1-based 10419097/8, 10419129/30, 10419153/4.
Image A vs RESTORE: **byte-identical** (same SHA). Raw printers:
`runs/localprn_{A,B_w2d2,C_w4d1,D_w3d2,PATCH,RESTORE}.txt`. Every file ends
with ` КОНЕЦ ЗАДАЧИ        +000000000000⏨+00    0000206320000000`.

### Raw C-oracle MTR (oracle only, `logs/MTR_{A,B,C,D,PATCH,RESTORE}_clean.txt`)

```
MTR_A  30116L aax  2110(0) AU=0000000000064        ; w digit '4'
       30117L ati    6(0) AU=0000000000004        ; M[6]=4
       30121L arx  2126(0) AU=0000000000062        ; d digit '2'
       30121R ati    7(0) AU=0000000000002        ; M[7]=2
       30122R xta 21635(6) AU=... M[06]=00004     ; N+2 offset 2 (w=4 mask=0)
       30123R atx   2006(0) AU=40041703600000
       30125L aax   2007(0) AU=1763747717637477   ; d=2 clear mask = no-op
       30140R asn    30(0) AU=0000000000003       ; digit 3 COMPUTED ON MACHINE
       30147R asn    40(0) AU=0000000000004       ; digit 4
       30161R asn    60(0) AU=0000000000005       ; digit 5
       30175R *64   2004(0) AU=60201601200017
MTR_C  30121R ati    7(0) AU=0000000000001        ; d=1
       30125L aax   2007(0) AU=1763747717600077   ; clear F2 byte
       30127L arx   2007(0) AU=0000000007400      ; GOST space (octal 17) at F2
       30175R *64   2004(0) AU=60201601207417
```

## 4. Word budget and scope

* Zone N+3: **54/58 words** (108 halfwords including the shared `floor_int`
  subroutine at `0o30177`); 4 words spare. No N+4 word.
* Zone N+2: 8 words at offsets `0..7`; clean range `0..525` only.
* Low RAM: reused cells `NUM` (SR40), `PD0` (SR24), `CARD`; no new cell.
* **Honest subset:** `w ∈ {2,3,4}` integer digit positions and `d ∈ {1,2}`
  fractional digits, selected by one decimal digit each. This is a
  F-width *padding/layout selector* on the proven 2+2 GOST field, not a
  general Fortran `Fw.d` editor: no `w>4`, no `d>2`, no rounding, no
  justification other than blanking seeded zeros / F2, no exponent or
  signed literal, no `777011`, no full IR interpreter. Out-of-range digits
  are not validated (an honest limitation, not a silent fallback).
* The two leading zeros for `w=4` remain seeded from `codegen_wide` as in
  docs/90; all four printed digits `34.5`/`34.50` are produced by the
  on-machine converter. `w=2` prints only machine-derived digits.

## 5. PASS / FAIL

| # | criterion | verdict |
|:--|:--|:--|
| 1 | Minimal IR encoding decided with citations; no invented 777011; fixture explicitly labelled | **PASS** |
| 2 | w/d decoded on machine from one IR card word; GOST layout adjusted via N+2 masks; `*64` reused | **PASS** |
| 3 | Reuse docs/98/100/105 reclaims; N+3 54/58 words | **PASS** |
| 4 | SIMH A/B/C/D: byte-identical image, 1-byte deck change → different printed width/spacing | **PASS** |
| 5 | One machine-word patch changes width; byte-identical restore returns | **PASS** |
| 6 | All six gates reach `КОНЕЦ ЗАДАЧИ` | **PASS** |
| 7 | Digits machine-derived (MTR `asn`/`atx 2007` chain) | **PASS** |
| 8 | Native FRONT FORMAT/Fw.d route | **FAIL** (absent emitters, docs/77/99/106; not invented) |
| 9 | General Fw.d editor / arbitrary w,d / rounding | **FAIL** (out of scope; §4) |

## 6. SHA-256 (full list `logs/SHAs.txt`)

```
2c543a7e2325ebe03f88f44a7dd1d0d62c869524cb06bc6fe1294d2c6c280fa4  images/2048_C5_A = _RESTORE
b87cc87ea2dffa0376ce28510e29ac2707eef0bbffc6f9157da58839db5dbb78  images/2048_C5_PATCH
f94db59a12cbac3c34fcf45289246bdf31cacea46ae1ac23222284dd222a9cd9  decks/deck_w4d2.b6
2a7e0fdaea90b6d2119a0989c272aba2b1b755c58258f3a1b7d16b2d91c13e0c  decks/deck_w2d2.b6
039edc09bcec408964dba81f3883c8048b756e9a899958695d02fa88177d8a86  decks/deck_w4d1.b6
32fcddae7b8fdc5e461e1327b17ec8554be8e9f066772e774ce139a0237cacf7  decks/deck_w3d2.b6
5515ac637882a137703a26b8150651e5765b95fa6e533af02f5116c9f20668f2  runs/localprn_A.txt
68366963c0a6aa8ab8801b1b7e017684387f648aa4189b2ef25dfee9badb4fc8  runs/localprn_B_w2d2.txt
df41c8a1d5cb8320e527d1cc9bcb51791fe7a6393a04137428dc48e9a12845f3  runs/localprn_C_w4d1.txt
36c85796b95a1d7bbcf9e77868eb4dea44ea640eed40d86175d52b000e555459  runs/localprn_D_w3d2.txt
17401ea67944cee3ad66e97a9ea122566aa267998da3c32d942c9c86c6ae4bb7  runs/localprn_PATCH.txt
b435d86d04ee896fd0d3b639cba2a9eeaec1ad40d69a93e7cb7ff5a037a13aa3  runs/localprn_RESTORE.txt
2a46413d0ffa9e13edf4dbaf64241920226f157aeef8f3e3e4efe7657b666bf6  logs/MTR_A_clean.txt (= RESTORE)
4b050680a80d499789abc2e29de37be96dbef419ee981e79f45d273f29bdec8a  logs/MTR_B_clean.txt
5d743c077a73035c1369007773bce737d64de25fc4bd9501c8a446d8e575dda1  logs/MTR_C_clean.txt
0395ac004407c13cdcc86ccdf8c43c2dd7863fd7c308e7a5ddf25e64d1301fc2  logs/MTR_PATCH_clean.txt
79a49e7cfd04a86cb3518fefc37b29249ed82279e2b8e22cc05e30b12f623c8b  logs/card_buffer_w4d2_at_entry.txt
0f98af0a86b7ee1e942dc4464d122e5fd8e11f65f2a8bd998e074dc31c67a65b  build/c5_build.py
```

C-oracle windows: `BESM6_MTR_LO=030114`, `HI=030205`, `N=400`,
`BESM6_DD_DEBUG=1`, `BESM6_CORE_ON_PC=01770`, `CORE_SKIP=6`.

## 7. Evidence index

```
build/c5_build.py            width evaluator + image builder (54/58 words)
build/make_decks.py          fixture IR decks (1X,6I8, TK=5)
build/{drive_c3,oracle_clean,setup_c5}.py  harnesses (copies, paths adapted)
decks/deck_w{4,3,2}d{2,1}.b6 A/B/C/D decks
images/2048_C5_{A,PATCH,RESTORE}
runs/localprn_*.txt          authoritative SIMH printer/console captures
logs/MTR_*_clean.txt         C-oracle MTR excerpts (oracle only)
logs/card_buffer_w4d2_at_entry.txt  decoded card buffer at contour entry
logs/SHAs.txt                full SHA-256 inventory
```

DONE
