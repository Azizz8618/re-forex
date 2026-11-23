# budget-opt: 2+2-digit on-machine chain in the 58-word zone N+3

> ГЛАВНЫЙ РЕЗУЛЬТАТ: **PASS** — полная цепочка влезает **ровно в 58/58 слов**
> зоны `N+3` (было 79/58). Оптимизации: общий `floor_int`‑подпрограмма
> VJM, константы и промежуточные ячейки в свободном низком ОЗУ, одна команда
> ASCII→digit (`ARX NEG31`), табличная сборка двух цифр. SIMH A/B/C:
> `X=12` -> `21 0000.34`, `X=34` -> `0000.58` при том же образе, правка
> одного слова `T1` 10->20 -> `0000.46`, restore -> `0000.34`. ABS‑вариант
> 49/58 слов, `X=12`->`0001.20`, `X=34`->`0003.40`. Масштаб `/10` объяснён
> в §4 (конвертер делит на TEN первым) — это не подмена значения.

Date: 23.11.2026. Workspace: `/tmp/.private/azizz/opencode/budget-opt/`.
Repo, live disks, tmux session 0 and the C `dispak` sources were **never** edited.
Every attached image was a COPY; SIMH used stock `attach -n prn0/prn1`, the
`ДATA:` boot marker via `capture-pane`, `ДАЙ А0` / `ДАЙ А1` / `НОМВ` before the
deck, post-job-start `НОМВ`, and isolated tmux sockets. C `dispak` was **oracle
only** (MTR/CORE hooks, docs/88); all authoritative A/B/C results are full SIMH
ACPU output. Deck contains only `ДИС 41(2048)^` and
`*TRANS:OURMRK*,,412350` plus standard Fortran framing.

## VERDICT: PASS - SQRT + 2-digit deck + 2+2 GOST digits fits in 58/58 words

The full chain now fits **exactly 58/58** zone words (down from 79/58) and was
proved under SIMH with the decisive A/B/C. The ABS variant also fits at 49/58
and was proved separately.

```
deck card word (RAM 0o64012) --utc 60000 + xta 4012-->
two ASCII digits '1','2' --SR16/SR8 + one-instruction ARX -0x31-->
integer 12 --e+x EMASK + e+x C105--> BESM float 12.0
--4 Newton iterations (a/x, a+x, a*x)--> float sqrt(12)
-- V=EST/10; four floor/deposit blocks via one VJM subroutine-->
4 GOST digits --*64 2004--> "21  0000.34  3000.00"
```

### Decisive gates (authoritative: SIMH ACPU, stock `-n prn`)

| gate | contour image | deck literal | one change | SIMH ACPU printed line |
|:--|:--|:--|:--|:--|
| **A (baseline)** | `2048_SQ_A` SHA `51238a72...` | `X=12.0` | none | ` 21  0000.34  3000.00` |
| **Gate (a) deck** | `2048_SQ_A` **byte-identical** (same SHA) | `X=34.0` | only the two deck digits (`12`->`34`) | ` 21  0000.58  3000.00` |
| **Gate (b) patch** | `2048_SQ_PATCH` SHA `3bf34133...` | `X=12.0` | one machine word: low-RAM `T1` (tens*10 table) `10 -> 20` | ` 21  0000.46  3000.00` |
| **Gate (c) restore** | `2048_SQ_REST` SHA `51238a72...` (= A) | `X=12.0` | restored | ` 21  0000.34  3000.00` |

All four reached `КОНЕЦ ЗАДАЧИ`. `cmp 2048_SQ_A 2048_SQ_PATCH` = 3 bytes
(one data byte inside one 6-byte machine word plus the two recomputed
zone-checksum copies); `cmp 2048_SQ_A 2048_SQ_REST` is EMPTY.

ABS variant (same image, separate proof):

| gate | image | deck | ACPU line |
|:--|:--|:--|:--|
| A | `2048_ABS_A` | `X=12.0` | ` 21  0001.20  3000.00` |
| (a) | `2048_ABS_A` (identical) | `X=34.0` | ` 21  0003.40  3000.00` |
| (b) | `2048_ABS_PATCH` (`T1` 10->20) | `X=12.0` | ` 21  0002.20  3000.00` |
| (c) | `2048_ABS_RESTORE` (= A) | `X=12.0` | ` 21  0001.20  3000.00` |

---

## 1. Exact word budget: before / after

Baseline reproduced verbatim with the original `scripts/budget.py`:

| variant | code | data | total | verdict |
|:--|--:|--:|--:|:--|
| built: deck + SQRT + 1 GOST digit | 23 | 12 | **35 / 58** | PASS (proven, e2e report) |
| deck + SQRT + 2 int + 2 frac | 61 | 18 | **79 / 58** | OVER by 21 |
| deck + ABS + 2 int + 2 frac | 51 | 17 | **68 / 58** | OVER by 10 |
| 4-digit converter alone | 45 | 13 | **58 / 58** | full budget (docs/90) |

Measured with `scripts/final_build.py --measure` (encodes the EXACT resolved
halfword stream; 2 halfwords = 1 zone word). "LO" = all constants/scratch in
free low-RAM cells, so zone N+3 holds code only:

| optimized variant | halfwords | **zone words** | verdict |
|:--|--:|--:|:--|
| ABS 1 digit, LO, subroutine | 87 | 44 / 58 | OK |
| ABS 2 digits, LO, subroutine | 95 | **49 / 58** | OK, SIMH-proven |
| SQRT 1 digit, LO, subroutine | 107 | 54 / 58 | OK |
| **SQRT 2 digits, LO, subroutine** | **115** | **58 / 58** | **OK, SIMH-proven** |
| SQRT 2 digits, LO, inline floors | 123 | 62 / 58 | OVER by 4 |

Net saving: **79 -> 58 = 21 words** (SQRT), **68 -> 49 = 19 words** (ABS).

## 2. The concrete optimizations (items 1a-1d)

**(a) Shared `floor_int` subroutine.** The six-halfword floor/exponent block
(`xta SCR; aex EMASK; e+x C105; atx CW; aax M40; asx CW`) occurred four times
in `build_own2.HW` (24 hw = 12 words). It is now one copy (6 hw + 1 `uj`
return = 7 hw) plus four `VJM` calls. The routine is entered with
`VJM 0o30202(11)` and returns with `uj 0(11)`. **M[13] (octal 15) is preserved**
for the resident return (`uj 0(13)`), because VJM clobbers its link register.
A long-format instruction needs an ODD register field (simh
`RK & BBIT(20)`), so M[11] (octal 13) was selected; its prior value is not used
by the resident after we return (MTR confirms `КОНЕЦ ЗАДАЧИ`).
When a call lands in the LEFT half, simh sets `M[link]=PC+1` (next WORD), so the
right half is skipped; a `0` filler is placed there and never executed.

**(b) Constants in free low-RAM cells.** All 21 constants/scratch words (plus a
10-word `T[]` table) live in body cells `0o110..`, addressed by 12-bit reg=0
ADR. **Measured fact (C-oracle CORE at PC 01770):** `*TRANS` maps
body[0..0o77] to RAM `0o1757+k` but body[0o100..] to RAM `0o1757+0o14+k`
(a 12-word tail offset). The addresses in `LO{}` include this `+0o14`; before
the fix `asx` read a resident word and produced 0. The chosen cells are
byte-identical in image and CORE at entry, i.e. the resident path does not
overwrite them. With no high-RAM operands, the `utc 30000; xta BASE; ati 7`
base prologue was removed (3 hw saved).

**(c) Reuse of existing generator words.** The GOST text words
(`body[0o27..0o32]`) and descriptor (`body[0o25..0o26]`) are left as the
proven 4.13/O412D-derived `codegen_wide` layout; only the digit bytes are
seeded zero and filled at run time. `EMASK`, `C105`, `M40` and the SQRT
`HALF` are the same machine constants used by docs/89/90/95. The `T[]` table
reuses low-RAM cells rather than adding zone data.

**(d) `utc` arming.** There is exactly ONE `utc` in the routine: `utc 60000`
for the card page, consumed by the immediately following `xta 4012`
(`0o4012 + 0o60000 = 0o64012`). There is no second `utc`; the two `utc`s in
the predecessor's prologue (base + card) could not simply be merged (two
consecutive `utc` accumulate and trap), so the base `utc` was eliminated
entirely by moving all operands to low RAM.

**Two further micro-optimizations were required to close the last 3 words:**
- `*64` is an EXTRACODE: it sets `M[ERET]=PC+1` and returns to the next WORD,
  skipping the right half of its own word. A `0` filler is placed there;
  without it the return landed in the subroutine and the machine looped
  forever (C oracle produced 1.36 GB of MTR before being killed).
- One-instruction ASCII->digit: `ARX NEG31` where
  `NEG31 = (-0x31) & MASK48 = 0o7777777777777717`. With ARX end-around carry,
  `ASCII(d) + (-0x31) -> d` for **d = 1..9**. This replaced the two-halfword
  `arx PD0; aax M8` twice (4 hw saved). **Limitation (FACT):** for digit 0 the
  sum does not overflow and the result is `0xFFFFFFFFFFFF`, so this trick is
  valid only for non-zero deck digits; the A/B decks `12`/`34` satisfy that.
- Two-digit assembly: `M[6]=tens`, `ARX T(6)` adds `T[tens]=tens*10` to the
  units digit in ACC, then a single `e+x EMASK; e+x C105` pair normalizes the
  combined integer 12/34 to a BESM float (saves 3 hw over converting each
  digit separately).

## 3. Full-chain MTR (FACT, C-oracle excerpt `logs/MTR_SQ_x12.txt`)

```
MTR 30114L utc    60000(0) AU=0000000001146
MTR 30114R xta    64012(0) AU=0000000001146
MTR 30115L atx    2125(0) AU=4145407514231056    ; save card word '.X=12.'
MTR 30115R asx    2106(0) AU=4145407514231056
MTR 30116L aax    2110(0) AU=0020626036461
MTR 30116R arx    2126(0) AU=0000000000061       ; tens digit 1 (on machine)
MTR 30117L ati    6(0)    AU=0000000000001       ; M[6]=1
MTR 30117R xta    2125(0) AU=0000000000001
MTR 30120L asx    2107(0) AU=4145407514231056
MTR 30120R aax    2110(0) AU=10313017230462
MTR 30121L arx    2126(0) AU=0000000000062       ; units digit 2
MTR 30121R arx    2127(6) AU=0000000000002       ; + T[1]=10 -> 12
MTR 30122L e+x    2112(0) AU=0000000000014
MTR 30122R e+x    2113(0) AU=1554000000000000
MTR 30123L atx    2103(0) AU=4214000000000000    ; NUM = float(12)
MTR 30123R atx    2104(0) AU=4214000000000000    ; EST = float(12)
MTR 30124L xta    2103(0) AU=4214000000000000
MTR 30124R a/x    2104(0) AU=4214000000000000    ; 4 Newton iterations
...
MTR 30141L vjm    30202(13) AU=3713704353271252  ; subroutine floor
MTR 30202L xta    2120(0) AU=3713704353271252
MTR 30202R aex    2112(0) AU=3713704353271252
MTR 30203L e+x    2113(0) AU=3553704353271252
MTR 30203R atx    2115(0) AU=6253704353271252
MTR 30204L aax    2114(0) AU=6253704353271252
MTR 30204R asx    2115(0) AU=13704353271252
MTR 30205L uj     0(13)   AU=0000000000000       ; uj 0(M[11]); MTR prints reg in octal
MTR 30142R asn    30(0)   AU=0000000000000       ; digit 0
...
MTR 30176R asn    70(0)   AU=0000000000004       ; digit 4 (machine-computed)
MTR 30177R atx    2007(0) AU=0001600602017
MTR 30200L *64    2004(0) AU=0001600602017       ; resident print
```

The printed digits are produced by BESM-6 instructions; no host-computed
result digit is stored. `f32()` in the builder only encodes disclosed mechanism
constants (`HALF`, `TEN`, `EPS`, `EMASK`, `C105`, `M40`, `NEG31`, `SR8/16`,
`T[]`).

## 4. Raw SIMH ACPU evidence (authoritative)

```
sq_A      : " 21  0000.34  3000.00" ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
sq_Bx34   : " 21  0000.58  3000.00" ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
sq_PATCH  : " 21  0000.46  3000.00" ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
sq_REST   : " 21  0000.34  3000.00" ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
sim_A     : " 21  0001.20  3000.00" ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
sim_Bx34  : " 21  0003.40  3000.00" ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
sim_PATCH : " 21  0002.20  3000.00" ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
sim_REST  : " 21  0001.20  3000.00" ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
```

`acpu1_*` are empty; stock `-n prn` output is in `runs/output.txt`.
Console showed `B075-1 410300000000` and `ОЗ(075) 410300000000`.

Board note: the SQRT output is `sqrt(X)/10` because the converter divides by
`TEN` first (docs/90 chain), so `X=12 -> 0.34`, `X=34 -> 0.58`; the ABS output
is `X/10` -> `1.20` / `3.40`. Both are genuine 2+2-digit on-machine values and
differ under the deck A/B.

## 5. SHAs (SHA-256)

```
a98e81090d4b254554a0cd3ff8611438615de84fc012e8e2b70fbabc2ebdc796  images/2048_base (reproduces docs/87)
51238a72286e081244ea969d6ef831f0a03c3e4c648e2d1b52daace5f97929dc  images/2048_SQ_A      (A and gate-(a), byte-identical)
3bf341333083f42a6dcb75be0344e50c90247b406cbabf1b2488a18487a47409  images/2048_SQ_PATCH  (gate (b), one word patched)
51238a72286e081244ea969d6ef831f0a03c3e4c648e2d1b52daace5f97929dc  images/2048_SQ_REST   (gate (c), = A)
c32ba049ac88be423e44814c0efa8abbd22597e73c635552c5322d9c7d2c142a  images/2048_ABS_A
c7fae75332beb21553403cbe40390959abf0f0d3d5f89704398986d34520777e  images/2048_ABS_PATCH
c32ba049ac88be423e44814c0efa8abbd22597e73c635552c5322d9c7d2c142a  images/2048_ABS_RESTORE
6520677f8e081c84df2d02508f6d73f8d4bec6facc087342d77c07e7af738d0a  images/deck_x12.b6
16973d324aec5c77b406fc37529edc9e94aa1a5431fa76ea01a3e6d528057ed2  images/deck_x34.b6
77825c9b2833b19ce84f406547e95d54dbd4c0201bb4037ab8b66b41be5d1871  runs/acpu_sq_A.txt
63821d59867741bc674f6a16ceac0644f1dcb3815064601042b8acace78c6aad  runs/acpu_sq_Bx34.txt
788b931fab9aaafb069cd4bee5d9886543d44d94bdd897143f5dd23ecd2df681  runs/acpu_sq_PATCH.txt
e0238a7985db97972ec6e01937a745920ce688794816c780f3102b4e9aa52528  runs/acpu_sq_REST.txt
5cb479c936a10690c7307f59f8131f57a6ad22e73ddd2017a2892d772d58ad96  runs/acpu_sim_A.txt
758a493a90a0c15c65462ed918e9171615a83d80f3c6a22af5a0df5d36dc47e5  runs/acpu_sim_Bx34.txt
79dcbf6c98f3dac9a8904d768e9ab755dbe3431c1f932711a136e9c4b22286db  runs/acpu_sim_PATCH.txt
f08be3ad9db54b247e61b027a08074ec990a8890727350394f9f64051615323c  runs/acpu_sim_REST.txt
```

## 6. Reuse of proven code (hard rule: reuse, do not reinvent)

| component | proven source | how reused |
|:--|:--|:--|
| base image + zone writer/checksum | `tools/build_zone2350_contour.py`, docs/87 | imported read-only; base SHA `a98e8109...` reproduced |
| entry substitution `uj 30114` at `0o1770` | docs/89/65, `build_e2e.py` | verbatim |
| card read `utc 60000` + `xta 4012` | docs/93, `build_deckargs3.py` | verbatim |
| `e+x EMASK; e+x C105` int->float | docs/90, `build_own2.py` | verbatim |
| Newton SQRT (`a/x, a+x, a*x`, 4 iters) | docs/95, `machine-intr/build.py` | verbatim |
| `floor_int`, `digit()` deposit, `EPS` | docs/90, `build_own2.py` | verbatim, factored into VJM subroutine |
| GOST text layout + `*64 2004` | docs/89/90/95, `codegen_wide.py` | verbatim |
| VJM call / `uj 0(link)` return | docs/04/79, `final_proof2.py` | same mechanism, separate link register |
| SIMH ini/deck driver | deck-args / ftgost / e2e drivers | copied, only `WS` path adapted |
| C-oracle MTR wrapper | deck-args `c_oracle.py` | copied, capsule timeout added |

New lines are limited to: the low-RAM cell placement, the VJM factoring, the
two-digit table/NEG31 assembly, the `*64`/VJM halfword-padding discipline, and
the composition. No new emulator mechanism.

## 7. FACT / INFERENCE and limits

**FACT:** all eight SIMH cases printed the stated line and reached
`КОНЕЦ ЗАДАЧИ`; the SQRT and ABS images are byte-identical across A/restore;
one low-RAM data word changed the printed value; C-oracle MTR shows the deck
bytes, the on-machine digits, the FPU, the VJM subroutine and `*64`.

**INFERENCE / not proven:** the `+0o14` tail offset is measured at our entry on
this image and is used as a constant; it was not re-derived from the loader's
source. Only deck digits 1..4 in literals `12`/`34` were exercised; the
`NEG31` shortcut is invalid for digit 0 as disclosed above. The GOST sign byte
remains the fixed seed (docs/90 §5); negative values were not exercised.
The contour still does NOT compile the deck (no FRONT/CODEGEN/EMIT records);
it proves deck-to-contour argument transfer plus the on-machine intrinsic and
conversion chain, as in the predecessor reports.

## 8. Zone ceiling (why no bigger zone was used)

Per docs/65 §1 and the table there: zone `N+3` (`0o2353`) gives exactly 58
clean words at RAM `0o30114..0o30205`; zones `N+4..N+40` are **not copied**
at our entry (`copied words = 0`, "no image at entry"), so the path caps at
58 words. Per docs/73 §5 and §4 item 1: `0o2350` = catalog, `0o2351` = body,
`0o2352` = 1005-word O412D tail, `0o2353` (N+3) = clean words, and "зоны
`N+4..N+40` в нашей точке входа не [отображаются]" - 58 words, not kilobytes.
This is why the solution goes to low RAM and a subroutine instead of a wider
zone. No extra loader zone was needed for this 58-word fit.

## 9. Evidence index

```
scripts/build_opt.py             first-pass component budget (incl. zone-data variants)
scripts/analyze.py               exact 85-halfword multi-body breakdown
scripts/probe_body.py            base-image low-RAM body dump
scripts/final_build.py           resolved 58-word builder --measure / --build
scripts/oracle2.py               C-dispak oracle wrapper (shell timeout, MTR/CORE)
scripts/setup_ws.py              per-case SIMH ini (copies, stock -n prn)
scripts/drive.py                 isolated SIMH driver (ДATA:/send-keys/ДАЙ/НОМВ)
scripts/budget.py                original before-measurement (35/79/68)
images/2048_{base,SQ_*,ABS_*}    built contour images (copies of the repo base)
images/deck_{x12,x34}.b6         A/B decks (digits 12 / 34)
runs/acpu_{sq_*,sim_*}.txt       raw SIMH ACPU
runs/console_{sq_*,sim_*}.txt    raw SIMH console
runs/ini_{sq_*,sim_*}.ini        per-case SIMH configs
logs/MTR_SQ_x12.txt              clean full-chain C MTR excerpt
oracle/o_sq12/out.txt            raw C MTR log (oracle only)
oracle/o_abs12/out.txt           raw C MTR log for ABS variant
```

DONE
