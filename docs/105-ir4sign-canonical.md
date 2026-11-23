# ir4-sign: FULL 4-digit IR LIT reader + machine GOST SIGN - recommended NEW canonical candidate

> НОВЫЙ КАНОНИЧЕСКИЙ ПРОДУКТ (принято главным агентом): образ
> `f483f6ca…4120b` (57/58 слов, 114 полуслов) объединяет полный 4‑цифровой
> IR‑LIT и машинный знак. SIMH A/B/C: `21 -0012.34` → правка SIGNBIT →
> `21  0012.34` → restore → минус; IR `5678` → `21 -0056.78`. Печать идёт
> без масштаба `/10`. Воспроизведение из файлов репозитория проверено:
> `tools/build_zone2350_contour.py base`, затем `tools/forex500-ir4sign/
> ir4_sign_build.py --build IR4SIGN_CANON --sign --floor-acc --drop-last-ati`
> даёт `f483f6ca…4120b`. Сборщики: `tools/forex500-ir4sign/`; колоды и
> `sha256.manifest`: `tests/plan-f77/88-ir4sign/`. `docs/103` остаётся
> историческим предыдущим каноническим вариантом (с масштабом `/10`).

Date: 23.11.2026. Workspace `/tmp/.private/azizz/opencode/ir4-sign/`.
Repo, live disks, tmux session 0 and the C `dispak` sources were **never** edited.
Every attached disk, contour image and deck is a COPY. C `dispak` was **oracle
only** (the only emulator with MTR hooks, docs/88); all authoritative A/B/C
results are full SIMH ACPU output. SIMH printer output was redirected to a
workspace-local file to avoid cross-session clobber of the shared
`ACPU/output.txt` (same disclosure as docs/94/99/104); stock `attach -n prn0/prn1`
semantics were kept, only the path changed in the ini. Target deck contains only
`*TRANS:OURMRK*,,412350` plus standard Fortran framing (no `*FOREX`/`*FTN`/
`*perso` in the target deck).

## VERDICT: PASS - 57/58 words; recommended NEW canonical candidate over docs/103

The two proven pieces were combined into ONE contour with verbatim reuse:

* docs/104 + `ir-parser/report.md`: FRONT-emitted `777005` LIT with the **full
  four-digit** `arg1` (`1234`/`5678`) decoded on the BESM-6 by `asx`/`aax`/`arx
  NEG31` + 10*T[] table assembly + `*100` recombination, fed into the ABS+2+2
  GOST converter, printing the literal value with **NO /10 scaling**.
* docs/100 + `sign-opt/report.md`: on-machine sign block `avx/aax/asx/aex/atx`
  taking the sign from the float's bit 40, flipping GOST word A byte 3
  (space `15` <-> minus `11`).

Reclaims applied exactly as measured: `floor_acc` (dead `xta SCR` in
`floor_int`) + `drop_last_ati` (dead `ati 5` on the last digit, `asn` uses
`M[reg=0]`). Sign constants `SIGNBIT=1<<40` and `SHR22=(64+22)<<41` live in the
**free T[8]/T[9] low-RAM cells** (body `0o134/0o135`, RAM `0o2137/0o2140`),
inside the proven-free `body[0o110..0o135]` range of docs/98 and never indexed
by our decks (only tens digits 1..4 are exercised). No host-computed digit and no
minus byte is stored in the image.

| variant (measured, 2 halfwords = 1 zone word) | halfwords | zone words | verdict |
|:--|--:|--:|:--|
| docs/104 IR 4-digit reader + ABS + 2+2 GOST (no sign) | 111 | 56 / 58 | proven baseline |
| + `drop_last_ati` only | 109 | 55 / 58 | measured |
| + `floor_acc` only | 110 | 55 / 58 | measured |
| + both reclaims, NO sign | 108 | 54 / 58 | measured |
| + sign, no reclaims | 117 | 59 / 58 | over |
| + sign, one reclaim | 115-116 | 58 / 58 | fits, no headroom |
| **+ sign + both reclaims (FINAL, built and SIMH-proven)** | **114** | **57 / 58** | **OK - 1 word headroom** |

No zone-N+4 word is used (docs/101: 58 words at `0o30114..0o30205` is the hard
hand-off limit). Shared `floor_int` subroutine entry: RAM `0o30202`.

---

## 1. Decisive A/B/C gates (authoritative: full SIMH ACPU, stock `-n prn`)

| gate | contour image | IR record card (only deck difference) | printed line (line 100) |
|:--|:--|:--|:--|
| A baseline | `2048_IR4SIGN_A` SHA `f483f6ca...` | `777005 6 1 0 1234 0` | ` 21 -0012.34  3000.00` |
| (a) operand change | `2048_IR4SIGN_A` **byte-identical** | `777005 6 1 0 5678 0` | ` 21 -0056.78  3000.00` |
| (b) SIGNBIT patch | `2048_IR4SIGN_B` (`1<<40 -> 0`) | same as A | ` 21  0012.34  3000.00` |
| (c) restore | `2048_IR4SIGN_RESTORE` SHA `f483f6ca...` (= A) | same as A | ` 21 -0012.34  3000.00` |

All four reached
`КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000` (line 114 of the prn
capture). Console showed the required boot/job markers: `ДATA:23.11.26`,
`ДАЙ А0`, `ДАЙ А1`, `НОМВ`, `B075-1 410300000000`, post-job-start `НОМВ`.

* Deck A vs (a): `cmp -l` = exactly **four bytes**, 1-based positions 164-167,
  octal `61 62 63 67` ('1','2','3','4') -> `65 66 67 70` ('5','6','7','8').
  The changed value is the literal digit string in the `777005` `arg1` I8 slot.
* Image A vs (b): `cmp -l` = **3 bytes** in one machine data word plus two
  checksum copies: file offsets `10411686` (SIGNBIT T8 low-RAM data word,
  `1 -> 0`), and `10410846` / `10410878` (recomputed zone-N checksum copies,
  octal `33 -> 32`). The four digits are unchanged by the sign patch: gate (b)
  prints `0012.34` with the minus simply removed.
* Image A vs (c): `cmp` empty, same SHA - byte-identical restore.

### Raw SIMH ACPU (authoritative, `runs/localprn_*.txt`, line 100 / line 114)

```
A        : " 21 -0012.34  3000.00" ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
(a) 5678 : " 21 -0056.78  3000.00" ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
(b) PATCH: " 21  0012.34  3000.00" ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
(c) REST : " 21 -0012.34  3000.00" ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
```

`runs/acpu_*.txt` are copies of the shared SIMH `ACPU/output.txt` and contain
stale lines from other jobs; the dedicated prn0 capture `runs/localprn_*.txt` is
the authoritative printer output (same disclosure as docs/104).

---

## 2. Raw C-oracle MTR (oracle only, `BESM6_MTR_LO=030114`, `HI=030220`, `N=1400`)

C `dispak` printed the same lines as SIMH (A ` 21 -0012.34  3000.00`,
PATCH ` 21  0012.34  3000.00`). MTR prints AU **before** each instruction.

Gate A, four-digit read + recombination + `/10` into EST (verbatim docs/104):

```
MTR 30114L utc    60000(0) AU=0000000001146
MTR 30114R xta    64014(0) AU=0000000001146      ; card word RAM 0o64014
MTR 30115R asx    2106(0) AU=1410206114431464    ; SR24 -> digit '1'
MTR 30116R arx    2126(0) AU=0000000000061        ; ASCII '1' (on machine)
MTR 30121R arx    2127(6) AU=0000000000002        ; +T[1]=10 -> 12
MTR 30122L e+x    2112(0) AU=0000000000014        ; integer 12
MTR 30123L atx    2103(0) AU=4214000000000000    ; float 12
MTR 30133L atx    2103(0) AU=4551510000000000    ; float 1234 (computed, *100)
MTR 30133R a/x    2116(0) AU=4551510000000000    ; /TEN -> 123.4
MTR 30134L atx    2104(0) AU=4357331463146315    ; EST
```

Gate A, sign block inserted after `atx V` (ACC holds V, positive float):

```
MTR 30135R atx    2117(0) AU=4214256050753412    ; V (positive float)
MTR 30136L avx    2137(0) AU=4214256050753412    ; -V (bit40 set by SIGNBIT)
MTR 30136R aax    2137(0) AU=4223521727024366    ; sign bit isolated
MTR 30137L asx    2140(0) AU=20000000000000      ; 1<<18 (shift right 22)
MTR 30137R aex    2006(0) AU=0000001000000       ; XOR into GOST_A
MTR 30140L atx    2006(0) AU=40041702600000      ; GOST A byte3 = 11 (MINUS)
MTR 30140R xta    2117(0) AU=40041702600000      ; reload V for digit path
```

Gate A, shared `floor_int` (reclaim `floor_acc`: subroutine starts with `aex`,
no `xta SCR`) and last digit (reclaim `drop_last_ati`: no `ati 5`):

```
MTR 30202L aex    2112(0) AU=4150000001777400    ; floor_int entry (no xta SCR)
MTR 30202R e+x    2113(0) AU=3610000001777400
MTR 30200L atx    2007(0) AU=20101600602017      ; last digit deposit, no ati 5
MTR 30200R *64    2004(0) AU=20101600602017      ; resident print -> -0012.34
```

Gate B (SIGNBIT T8 = 0):

```
MTR 30136L avx    2137(0) AU=4214256050753412    ; no negate (bit40 = 0)
MTR 30136R aax    2137(0) AU=4214256050753412    ; ACC = 0 after mask
MTR 30137L asx    2140(0) AU=0000000000000
MTR 30137R aex    2006(0) AU=0000000000000       ; no XOR
MTR 30140L atx    2006(0) AU=40041703600000      ; GOST A byte3 = 15 (SPACE)
```

The sign is produced purely on machine from the float's bit 40; the digits are
unchanged by the SIGNBIT patch (gate B), and the sign persists when only the
deck digits change (gate a). The two mechanisms are independent and both
on-machine.

---

## 3. Negative operand from the IR record: NOT POSSIBLE in `777005` arg1 (FACT)

FRONT.FTN cannot emit a negative `arg1` in a `777005` LIT record, so no such
operand could be tried. Source evidence (`src/newcomp/FRONT.FTN`):

* The LIT numeric scanner (lines 234-261) accepts only ASCII digits `48..57`
  and the decimal point `46`. It computes `SC = VAL*100/FRAC` (line 254) and
  stores it as `TA(NTK) = SC` (line 258), i.e. `arg1`. `VAL` and `FRAC` are
  built only from digits, so `arg1` is always a non-negative integer.
* A minus sign (CH=45) is intercepted at line 225-226 and routed to the
  **operator** handler at 524, never to the numeric literal scanner at 510.
  Line 302 sets `OP=2` (subtraction); line 306-307 treats a leading minus as a
  separate **unary minus operator** (pushed as `ST=6`). It is emitted as another
  `777005` token with `kind=2/4`, not as a negative `arg1`.
* The field is printed with `9005 FORMAT(1X,6I8)` (line 376). Even a hand-made
  negative I8 field would place the minus inside the field and shift the four
  digits one column right, breaking the fixed-offset reader (digits are read at
  bytes 2..5 of RAM `0o64014`); the `ARX NEG31` digit trick is in any case only
  valid for digits 1..9.

Therefore `X=-12.34` arrives as `777005 <lit 1234>` plus a separate operator
record, and there is no negative `arg1` to feed to this contour. The sign in
this product is deliberately demonstrated with the machine SIGNBIT patch (gate
b), exactly as in docs/100/103. This was a source-level determination; the repo
FRONT was not modified and no BUILD harness for a negative literal exists in
the preserved workspace.

---

## 4. Why this is a better canonical candidate than docs/103

| axis | docs/103 canonical | this candidate (ir4-sign) |
|:--|:--|:--|
| input | deck literal at `0o64012` (X=12) | real FRONT-emitted `777005` IR record, full 4-digit `arg1` |
| printed value | ` 21 -0000.34` for X=12 (`/10` scaling, `sqrt(X)/10`) | ` 21 -0012.34` for arg1=1234 (**literal value, no /10 scaling**) |
| digits | 2+2 | 2+2 (four digits, `1234`->`0012.34`, `5678`->`0056.78`) |
| machine sign | yes (SIGNBIT patch) | yes (SIGNBIT patch, same block) |
| word budget | 58/58 (no headroom) | **57/58 (1 word headroom)** |
| FRONT-IR merged with sign | no - "SEPARATE variant, needs N+4" (docs/103 limits) | **yes, merged in one contour** |
| zone N+4 | blocked | not used |

This candidate supersedes docs/103 on the task's stated criteria: correct
literal value, no `/10` scaling, machine sign, and it fits within 58 words. It
does not replace the SQRT intrinsic of docs/103 (that chain is absent here); it
is a different, more faithful IR-literal product. Its canonical artifacts are:

```
image: images/2048_IR4SIGN_A
SHA-256 f483f6ca1e60c58415d816111757ec9a35da04b545d79cf3c7656c0f1484120b
deck:  decks/deck_ir1234.b6   (translator line only: *TRANS:OURMRK*,,412350)
SHA-256 388e6da393727e33d73d6e12c1bb32355f1538b16abc864583281f09c6d28c02
```

---

## 5. Reuse of proven code (hard rule: reuse, do not reinvent)

| component | proven source | how reused |
|:--|:--|:--|
| base image + zone writer/checksum | `tools/build_zone2350_contour.py`, docs/87 | imported read-only; base SHA `a98e8109...` reproduced |
| entry substitution `uj 30114` at `0o1770` | docs/89/65 | verbatim |
| 4-digit IR card read `utc 60000` + `xta 4014` + `NEG31`/T[]/`*100` | docs/104, `ir4_build.Stream.ir_read4()` | verbatim |
| ABS + 2+2 GOST converter + `*64 2004` | docs/98/104 | verbatim, with two measured reclaims |
| `floor_acc` / `drop_last_ati` reclaims | docs/100, `final_sign.py` | verbatim |
| sign block `avx/aax/asx/aex/atx`, T[8]/T[9] constants | docs/97/100, `final_sign.sign_block()` | verbatim mechanism |
| SIMH ini/deck driver | docs/100/104 drivers | copied, only WS path adapted |
| C-oracle MTR wrapper | docs/98/104 `oracle_ir.py` | copied, only WS path adapted |

New lines are limited to orchestration in `scripts/ir4_sign_build.py` (insert
the sign block after `atx V` in the converter, set T[8]/T[9], wire the two
reclaims). No new emulator mechanism, no new low-RAM cell, no C patch.

## 6. FACT / INFERENCE and limits

**FACT:** all four SIMH cases printed the stated line and reached `КОНЕЦ ЗАДАЧИ`;
A and RESTORE are byte-identical; one low-RAM data word changed the printed sign
while leaving all four digits unchanged; the byte-identical A image with a
different deck changed the digits while leaving the sign unchanged; C-oracle
MTR shows the sign block, the shortened `floor_int` and the last digit.

**Limits / not covered (FACT from source, unless noted):**
* Only `arg1` of `777005` is parsed (four decimal digits at RAM `0o64014`
  bytes 2..5). No marker verification, no multi-record scan, no field-width
  detection, no sign/exponent/decimal-point parsing. `arg1 > 9999` (X >= 100)
  is not decoded correctly.
* `777001`, `777002`, `777003`, `777004` are **not** parsed by this contour;
  doing so needs a card-word scanner, per-character tables and low-RAM dispatch
  (requirements in `ir-parser/report.md` §3).
* `777010` / `777011` emitters are **absent** from the repo (`FRONT.FTN` emits
  only `777001..777005`; docs/77 refers to a now-absent copy). Their field
  widths are INFERENCE; formatted READ remains out of scope.
* Negative `arg1` cannot be emitted by FRONT (see §3). `NEG31` is invalid for
  digit 0; only digits 1..4 were exercised.
* The line prefix `21`, the sign space and the Y field `3.00` remain contour
  seeds as in docs/89/90/95/96/99/104. The contour still does not compile the
  deck (no FRONT/CODEGEN/EMIT records inside it).
* Zone `N+3` gives 58 clean words (`0o30114..0o30205`); zones `N+4..N+40` are
  not copied at our entry (docs/65/73). Final usage 57/58.

## 7. SHAs (SHA-256)

```
a98e81090d4b254554a0cd3ff8611438615de84fc012e8e2b70fbabc2ebdc796  images/2048_base (reproduces docs/87)
f483f6ca1e60c58415d816111757ec9a35da04b545d79cf3c7656c0f1484120b  images/2048_IR4SIGN_A      (A, gate a, RESTORE; byte-identical)
2a12ddf32bf1f0c627b6e530dc863dad61554d7cec5034f9ffd5281945a7d34a  images/2048_IR4SIGN_B      (gate b, SIGNBIT T8 1<<40 -> 0)
f483f6ca1e60c58415d816111757ec9a35da04b545d79cf3c7656c0f1484120b  images/2048_IR4SIGN_RESTORE (= A)
388e6da393727e33d73d6e12c1bb32355f1538b16abc864583281f09c6d28c02  decks/deck_ir1234.b6
3fb59748c487244f96758163a7151451a3425e5c01dd61a794bb3b71c32836e0  decks/deck_ir5678.b6
e13653ec222aff53a196496f4b2fdd2a5c692cfa30c2a0e24a1e6e5f974f530e  runs/localprn_A.txt
7064e2f07b183cd9b40023bd8a1073acc1ba959e6e9d97525844641ccd94bd3b  runs/localprn_DECK5678.txt
b06f2e55a2a90a8fb032ac58e008e2057a7f3ba0fc8cd7be642f08571c8c2478  runs/localprn_PATCH.txt
a947b1d149a8a1398e88077c8be291fd0701338365a749157230526809864d2a  runs/localprn_RESTORE.txt
df0e75406e15e72379744e69e04afbf77ccb860893a841ba761da8412b0c7e64  oracle/A_SIGN/out.txt (C MTR, oracle only)
9b8c47ae8053a88aafedd1615b5dc843c41775e14f352cecf8ccea9c15ee5988  oracle/PATCH_SIGN/out.txt
b1f73497f4840179afda0de82bcd770e9e2971b2718ccbcb663db7647b43cf85  scripts/ir4_sign_build.py
```

## 8. PASS / FAIL

| # | gate | verdict |
|:--|:--|:--|
| 1 | combine 4-digit IR reader + machine sign with measured reclaims | **PASS** |
| 2 | exact word count <= 58 (built/ran at 57/58, 114 halfwords) | **PASS** |
| 3 | SIMH A: `1234` -> ` 21 -0012.34`, КОНЕЦ ЗАДАЧИ | **PASS** |
| 4 | SIMH (a): byte-identical image, `5678` -> ` 21 -0056.78`, КОНЕЦ ЗАДАЧИ | **PASS** |
| 5 | SIMH (b): SIGNBIT one-word patch -> ` 21  0012.34` (minus removed), КОНЕЦ ЗАДАЧИ | **PASS** |
| 6 | SIMH (c): byte-identical restore -> ` 21 -0012.34`, КОНЕЦ ЗАДАЧИ | **PASS** |
| 7 | correct literal value, NO /10 scaling, machine sign | **PASS** |
| 8 | C-oracle MTR shows sign block, short floor_int, last digit; agrees with SIMH | **PASS** |
| 9 | negative operand from IR record | **N/A** (FRONT cannot emit negative `arg1`; §3) |
| 10 | `777001..777004` parsed by this contour | **FAIL** (out of scope; §6) |
| 11 | `777010/777011` emitters / formatted READ | **FAIL** (absent from repo; §6) |
| 12 | `arg1` wider than 4 digits or exponent/sign fields | **FAIL** (not decoded; §6) |

Recommendation: **adopt this as the new canonical product** in place of docs/103
on the task's stated criteria (literal fidelity, no /10 scaling, machine sign,
fits 58 words with headroom), while retaining docs/103 for the separate SQRT
intrinsic variant.

## 9. Evidence index

```
scripts/ir4_sign_build.py          combined builder (measure + A/B/REST images)
scripts/{ir4_build,final_sign,build_e2e}.py  proven verbatim sources (read-only imports)
scripts/setup_ir4sign.py           isolated ini, stock -n prn0, workspace-local prn
scripts/drive_ir4sign.py           SIMH driver (ДATA:/send-keys/ДАЙ/НОМВ)
scripts/oracle_ir4sign.py          C-dispak oracle wrapper (MTR only)
decks/deck_ir{1234,5678}.b6        A/B decks, four operand bytes differ
images/2048_{base,IR4SIGN_A,IR4SIGN_B,IR4SIGN_RESTORE}
runs/localprn_{A,DECK5678,PATCH,RESTORE}.txt  raw SIMH ACPU (authoritative)
runs/console_*.txt, runs/ini_*.ini
oracle/{A_SIGN,PATCH_SIGN}/out.txt  raw C MTR (oracle only)
logs/MTR_IR4SIGN_*.txt             clean MTR excerpts used in §2
frontbuild/                        FRONT-emitted 777005 records (from docs/104, copies)
```

DONE
