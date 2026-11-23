# plan item 2: full multi-digit FREXT/IR LIT operand on the BESM-6 in the zone-2350 contour

> ГЛАВНЫЙ РЕЗУЛЬТАТ: **PASS** — контур читает **все четыре цифры** LIT‑операнда
> подлинной записи `777005`, выданной FRONT build‑шагом, и печатает исходный
> Fortran‑литерал: `1234 -> 21 0012.34`, `5678 -> 21 0056.78` (байтово тот же
> образ, отличаются 4 байта деки). Машинный A/B: `T[1]` 10→20 даёт `0022.34`,
> restore возвращает `0012.34`. Все `КОНЕЦ ЗАДАЧИ`. Бюджет **56/58 слов**
> (111 полуслов), зона N+4 не используется. Масштаб `/10` здесь отсутствует —
> это шаг 3 плана. Знак и 777001..4/777010..11 остаются вне объёма.

Date: 23.11.2026. Workspace `/tmp/.private/azizz/opencode/ir-parser/`.
Repo, live disks, tmux session 0 and the C `dispak` sources were never edited.
Every attached disk, contour image and deck is a COPY. C `dispak` is the
**oracle only** (the only emulator with MTR/CORE hooks, docs/88); all
authoritative A/B/C results are full SIMH ACPU output. SIMH printer output was
redirected to a workspace-local file to avoid cross-session clobber of the
shared `ACPU/output.txt` (same disclosure as docs/94/99). Stock `attach -n prn`
semantics were kept; only the file path changed in the ini.

## VERDICT: PASS - four digits of `arg1` decoded on machine and fed into the proven ABS + 2+2 GOST chain

A genuine FRONT-emitted `777005` LIT record is injected as a deck card. Its
**full four-digit** scaled operand (`1234` for X=12.34, `5678` for X=56.78) is
read from the card buffer word at RAM `0o64014` and decoded on the BESM-6 by
four `asx`/`aax`/`arx NEG31` extractions, two 10*T[] table assemblies, two
integer-to-float normalizations and one on-machine `*100` recombination. The
resulting integer-valued float is divided by the existing `TEN` constant and
fed into the verbatim docs/98 ABS + four-floor/deposit GOST converter. The
printed 2+2 value is `0012.34` for `1234` and `0056.78` for `5678`, i.e. the
original Fortran literal, computed entirely on machine.

| gate | contour image | IR record card (only deck difference) | SIMH ACPU line (line 100) |
|:--|:--|:--|:--|
| A baseline | `2048_IR4_A` SHA `9a61c736...` | `777005 6 1 0 1234 0` | ` 21  0012.34  3000.00` |
| (a) operand change | `2048_IR4_A` **byte-identical** | `777005 6 1 0 5678 0` | ` 21  0056.78  3000.00` |
| (b) machine-word patch | `2048_IR4_PATCH` SHA `4efbbf69...` | same as A | ` 21  0022.34  3000.00` |
| (c) restore | `2048_IR4_RESTORE` SHA `9a61c736...` (= A) | same as A | ` 21  0012.34  3000.00` |

All four reached `КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000`.

* Deck A vs (a): `cmp -l` = exactly **four bytes**, 1-based positions 164-167,
  octal `61 62 63 67` ('1','2','3','4') -> `65 66 67 70` ('5','6','7','8').
  The deck contains only `*TRANS:OURMRK*,,412350` as translator; verified no
  `*FOREX`/`*FTN`/`*perso` in the target deck.
* Image A vs (b): `cmp -l` = 5 bytes in **3 machine words**: the low-RAM `T[1]`
  table word (body cell, octal `12` -> `24`, decimal 10 -> 20) plus the two
  recomputed zone-N+1 checksum copies. No host-computed result digit is stored
  anywhere. Image A vs (c): byte-identical (`cmp` empty, same SHA).
* The BUILD step (system FOREX, on copies) really emitted the operands:
  `frontbuild/x1234/call_canonical.out:74` = `   777005       6       1       0    1234       0`,
  `frontbuild/x5678/call_canonical.out:74` = same with `5678`; 0 ERR on both
  build and call logs.

---

## 1. STEP 1 - exact byte layout of multi-digit `arg1` fields (FACT)

`src/newcomp/FRONT.FTN`: `9005 FORMAT(1X,6I8)` (line 376), print at line 349,
`SC = VAL*100/FRAC` (line 254), `TA(NTK) = SC` (line 258). Therefore
`X=12.34` would be VAL=1234, FRAC=100, SC=1234. Verified by real BUILD above.

Emitted record text (FACT, `od -An -tx1 -c` of `call_canonical.out:74`):
49 characters plus newline. Columns (0-based): 0-2 three spaces (1X plus the
I8 pad), 3-7 `777005`, then three I8 fields, then **arg1 at columns 32-40**:
four pad spaces at 32-35 and the four digits at **36,37,38,39**
(`31 32 33 34` for 1234; `35 36 37 38` for 5678). The injected deck card drops
one leading space (48 characters plus newline), so the card's digits are at
columns 35-38.

C-oracle CORE dump at contour entry (`BESM6_CORE_ON_PC=01770`, `SKIP=6`),
`logs/card_buffer_ir1234_at_entry.txt` (COSY RLE: `0x80+n` = n spaces;
CORE word bytes are MSB-first, so byte k of the dump is extracted by a right
shift of `(5-k)*8` bits):

```
064012  82 37 37 37 30 30   <2sp> 7 7 7 0 0
064013  35 87 36 87 31 87   5 <7sp> 6 <7sp> 1 <7sp>
064014  30 84 31 32 33 34   0 <4sp> 1 2 3 4      <- arg1 digits, bytes 2,3,4,5
064015  87 30 a3 0a 0a 0a   <7sp> 0 <35sp> \n     <- arg2 starts at byte 1
```

So the four digits of `arg1` are bytes 2,3,4,5 of word `0o64014`, addressed in
machine code with `utc 60000` + short `xta 4014` (as in docs/93/99) and shifted
right by **24, 16, 8, 0** bits respectively. This is the direct extension of
docs/99, which decoded only byte 2 (shift 24) of the three-digit `900`/`400`
operand.

## 2. STEP 2 - machine code, word budget and A/B/C proof

Builder `scripts/ir4_build.py` (self-contained, imports only the read-only
`rz`/`wz`/`short`/`word`/`f32`/checksum helpers from the copied `build_e2e.py`).
The 4-digit reader is 32 halfwords:

```
utc 60000 ; xta 4014 ; atx CARD
asx SR24 ; aax M8 ; arx NEG31          ; d1 = '1' -> 1
ati 6 ; xta CARD ; asx SR16 ; aax M8 ; arx NEG31 ; arx T(6)  ; d1*10 + d2 = 12
e+x EMASK ; e+x C105 ; atx NUM         ; float 12
xta CARD ; asx SR8 ; aax M8 ; arx NEG31 ; ati 6
xta CARD ; aax M8 ; arx NEG31 ; arx T(6)          ; d3*10 + d4 = 34
e+x EMASK ; e+x C105 ; atx CARD        ; float 34 (card word no longer needed)
xta NUM ; a*x HUNDRED ; a+x CARD ; atx NUM        ; 12*100 + 34 = 1234
a/x TEN ; atx EST                      ; arg1/10 = 123.4, then ABS chain
```

`HUNDRED = f32(100.0)` reuses the `HALF` scratch cell, `SR8` reuses `PD0`,
`SR16`/`SR24` replace the old shift cells: **no new low-RAM cell** beyond the
30 proven-free cells of docs/98/100. `NEG31 = (-0x31) & MASK48` is the
one-instruction ASCII-to-digit trick of docs/98 (valid for digits 1..9; both
A/B operands satisfy that). The remaining chain (shared `floor_int` VJM
subroutine, four GOST deposits, resident `*64 2004`) is verbatim docs/98.
No sign block was added; only the ABS variant was needed.

Measured word budget (`scripts/ir4_build.py --measure`, 2 halfwords = 1 zone word,
zone N+3 = 58 words hard limit per docs/101):

| variant | halfwords | zone words | verdict |
|:--|--:|--:|:--|
| docs/98 ABS + 2-digit deck reader (reference) | 98 | 49 / 58 | prior work |
| **IR 4-digit reader + ABS + 2+2 GOST (built and SIMH-proven)** | **111** | **56 / 58** | **OK** |
| same, with docs/100 `drop_last_ati` reclaim | 109 | 55 / 58 | measured only |
| same, with docs/100 `floor_acc` reclaim | 110 | 55 / 58 | measured only |
| both reclaims | 108 | 54 / 58 | measured only |

No zone-N+4 word is used (docs/101: 58 words at `0o30114..0o30205` is the hard
hand-off limit). All additions are same-length reclaims or replacements inside
that window.

### Raw C-oracle MTR (oracle only, `logs/MTR_IR4_x1234_contour.txt`)

```
MTR 30114L utc    60000(0) AU=0000000001146
MTR 30114R xta    64014(0) AU=0000000001146
MTR 30115L atx    2125(0) AU=1410206114431464     ; card word = 0<4sp>1234
MTR 30116R arx    2126(0) AU=0000000000061        ; ASCII '1' (on machine)
MTR 30117R xta    2125(0) AU=0000000000001        ; M[6]=1
MTR 30121R arx    2127(6) AU=0000000000002        ; +T[1]=10 -> 12
MTR 30122L e+x    2112(0) AU=0000000000014        ; integer 12
MTR 30123L atx    2103(0) AU=4214000000000000     ; float 12
MTR 30125R arx    2126(0) AU=0000000000063        ; ASCII '3'
MTR 30127R arx    2127(6) AU=0000000000004        ; +T[3]=30 -> 34
MTR 30130L e+x    2112(0) AU=0000000000042        ; integer 34
MTR 30132R a+x    2125(0) AU=4551300000000000
MTR 30133L atx    2103(0) AU=4551510000000000     ; float 1234 (computed)
MTR 30133R a/x    2116(0) AU=4551510000000000     ; /TEN -> 123.4
MTR 30134L atx    2104(0) AU=4357331463146315     ; EST/ABS result
MTR 30137R vjm    30200(13) AU=4051676355442642   ; shared floor_int
MTR 30140R asn    30(0)   AU=0000000000001        ; GOST digit 1
MTR 30147R asn    40(0)   AU=0000000000002        ; GOST digit 2
MTR 30161R asn    60(0)   AU=0000000000003        ; GOST digit 3
MTR 30174R asn    70(0)   AU=0000000000004        ; GOST digit 4
MTR 30176L *64    2004(0) AU=20101600602017
PRN: 21  0012.34  3000.00
```

Deck `5678` changes the MTR ASCII words to `0o65,0o66,0o67,0o70` and the
deposited digits to `5,6,7,8` (`logs/MTR_IR4_x5678_contour.txt`).
The T1 patch gate changes `MTR 30121R arx T(6) AU=...2` and the first combined
integer from `0o14` (12) to `0o26` (22), giving `0022.34`
(`logs/MTR_IR4_PATCH_contour.txt`). No host digit is stored in the image.

### Raw SIMH ACPU (authoritative, `runs/localprn_*.txt`, line 100 / line 114)

```
A      : " 21  0012.34  3000.00" ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
B      : " 21  0056.78  3000.00" ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
PATCH  : " 21  0022.34  3000.00" ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
REST   : " 21  0012.34  3000.00" ... " КОНЕЦ ЗАДАЧИ  +000000000000⏨+00  0000206320000000"
```

Console captures (`runs/console_A.txt` etc.) show the required boot and job
markers: `ДATA:23.11.26`, sent `ДАЙ А0`, `ДАЙ А1`, `НОМВ`, then `B075-1
410300000000` and the post-job-start `НОМВ`. Deck-only input is
`*TRANS:OURMRK*,,412350` plus `*NAME`/`PROGRAM`/`END`/`*EXECUTE` framing.

## 3. STEP 3 - honest scope, limits and what is still missing

**Maximum honestly decoded width: 4 decimal digits of `arg1` in its fixed
I8 slot** (bytes 2..5 of RAM `0o64014`). This covers every FRONT LIT produced
by `SC = VAL*100/FRAC` up to `arg1 = 9999` (X up to 99.99). It is a full parse
of the operands actually tested (`1234`, `5678`). It is **not** a general IR
field decoder: there is no marker verification, no multi-record scan, no sign,
exponent or decimal-point handling, no field-width detection, and `arg1` values
with more than four digits (X >= 100, e.g. `12345` for 123.45) would be read
from a shifted column and are not decoded correctly by this fixed-offset
reader. The line prefix `21`, the sign space and the Y field `3.00` remain
contour seeds as in docs/89/90/95/96/99.

**What is needed for `777001..777004` (not done here):**
* `777001 <seq> <rule> <itype>` (1X,4I8): a rule/type dispatch. On machine this
  needs a second card-word reader (word `0o64012`/`0o64013`) plus a table of
  rule numbers and branch targets in low RAM, and a VJM dispatch. The current
  56/58 words leave only 2 words, so this requires replacing the GOST converter
  with a smaller one or a proven same-length reclaim; no extra zone is available
  (docs/101).
* `777002 <seq> <pos> <code>` (1X,4I8): a per-character table indexed by `pos`
  and a code-to-ASCII mapping; again a low-RAM table plus a scanner over several
  card words, with base-register arithmetic for the varying word offsets.
* `777003 <nlines> <nrewrites>` (1X,3I8): only needed as a loop bound for such
  a scanner; it would occupy one more decoded field.
* `777004 <seq> 21 0 <label>` (1X,5I8): a label allocator/symbol table, which
  needs writable low-RAM scratch across records and a relocation pass.
* All four require scanning multiple injected cards (not one fixed word), which
  means an address base different from the single `utc 60000` + `xta 4014`
  pair; two `utc`s cannot be consecutive (docs/98: M20 accumulates and traps).

**What is needed for `777010` / `777011` (emitters absent):**
Repository-wide search confirms `FRONT.FTN` emits only `777001..777005`; the
only in-repo description is docs/77, which refers to a *copy* of `FRONT.FTN` in
a now-absent workspace. `777011` (FORMAT descriptors K,R,W,D) and `777010`
(READ) would have to be authored into FRONT (and the FOREX runtime that emits
the READ record) at BUILD time, and only then could a card reader consume them.
Their exact `1X,NI8` field widths are INFERENCE, not FACT here. This task did
not edit the repo, so no such emitter was created. Formatted `READ(u,fmt)`
remains blocked (docs/91/92/77).

## 4. Harness, discipline and reuse

Deck: `decks/deck_ir{1234,5678}.b6`, copies of the docs/99 deck with exactly
the 4-byte `arg1` change. SIMH driver `scripts/drive_simh.py` (copied from the
proven docs/100 driver) uses an isolated `TMUX_TMPDIR`, detects `ДATA:` through
`capture-pane`, sends all input with `send-keys`, uses `ДАЙ А0`/`ДАЙ А1` and
`НОМВ` before the deck, a post-job-start `НОМВ`, and stock `attach -n prn0/prn1`.
`scripts/setup_simh.py` keeps the stock ini, only redirecting prn0 to a
workspace-local file and pointing md41/md45 at copies. C-oracle runs
(`scripts/oracle_ir.py`) are oracle-only MTR/CORE evidence.

Reused verbatim: repo tool `tools/build_zone2350_contour.py` (zone writer and
checksum, read-only; base SHA `a98e8109...` reproduced), docs/93/99 card-read
chain, docs/98 `ARX NEG31` and 10*T[] assembly, docs/90 `e+x` normalization,
docs/98 shared `floor_int` VJM subroutine and four-digit GOST converter with
`*64 2004`, docs/71 FRONT BUILD step, docs/100 SIMH harness. New lines are
limited to: three shift-constant substitutions, the `HUNDRED` recombination,
and the orchestration. No new emulator mechanism and no dispak C patch.

## 5. SHAs (SHA-256)

```
a98e81090d4b254554a0cd3ff8611438615de84fc012e8e2b70fbabc2ebdc796  images/2048_base (reproduces docs/87)
9a61c7366e803a0e47f52be447a23d5fec7d57853bb6b702e5198be6d900ab96  images/2048_IR4_A      (A and gate a, byte-identical)
4efbbf6989d065a407c4a6d9100d91b19567620f903d7078eaf183a865de76da  images/2048_IR4_PATCH  (gate b, T1 10->20)
9a61c7366e803a0e47f52be447a23d5fec7d57853bb6b702e5198be6d900ab96  images/2048_IR4_RESTORE (= A)
388e6da393727e33d73d6e12c1bb32355f1538b16abc864583281f09c6d28c02  decks/deck_ir1234.b6
3fb59748c487244f96758163a7151451a3425e5c01dd61a794bb3b71c32836e0  decks/deck_ir5678.b6
b637cefb5fd27611ed486b58f5750f13829801e55775946c4a4b715dc79d2339  frontbuild/x1234/call_canonical.out
e15ca08ba4afc6f496e68d49700e8f47de936b23de4e5038f7e961e15d63d7a6  frontbuild/x5678/call_canonical.out
b172ed08c6db4bd40197c7783344d39d2fa6487a52ea6439a6e21bde0d698a60  runs/localprn_A.txt
2f4c5f561a26de92a3aaa9b2db4115d3e62f4b0d0955d65d656e0df5ad03bb64  runs/localprn_B.txt
3b3af414e5ef4021812e3cca6576138510f080a6d736af24558aaf0dcb3d1e86  runs/localprn_PATCH.txt
e4f6be79b420a2b1e3f0611d0a58e6ab0c4e1e40940f1e867b7bdec770d18d2a  runs/localprn_REST.txt
ac89ce0ba3141c81952bde3fc073d008f08ed3ffdcdd42eaeb749d06d3535e61  logs/MTR_IR4_x1234_contour.txt
8bf1bf9f8e15a2a7146eec7739a475b5a31d546ff95ff534ff520b6ebf436d0c  logs/MTR_IR4_x5678_contour.txt
c13184505e62cb24ce88ef308e518f937f3a4bfa07bada8f31e1c64fc140e207  logs/MTR_IR4_PATCH_contour.txt
4f357aef8df7ea9afede97245ec0da73501eb815eed087b378f229a2a962e08e  oracle/dump1234/core-pc.bin
52d1dc8a3585fc8ad421c66a94f7f09c417dbd38b22fdf5925af0529f3559d80  oracle/MTR1234b/out.txt
e6e69f703a7bf14994f6632c6059325f861cff8cd3c7b099737e0923265a050a  oracle/MTR5678/out.txt
d78cdfad10d5bf8693657587c1b5f37efb279eab381bb9c5de4596da6c5788ef  oracle/MTRPATCH/out.txt
```

## 6. PASS / FAIL

| # | gate | verdict |
|:--|:--|:--|
| 1 | FRONT emits `arg1=1234` / `5678` for X=12.34 / 56.78 (real BUILD, 0 ERR) | **PASS** |
| 2 | CORE decode: four operand digits at RAM `0o64014` bytes 2..5 | **PASS** |
| 3 | On-machine decode of 4 digits (MTR ASCII -> digits -> float 1234/5678) | **PASS** |
| 4 | Full contour fits 58 words (built/ran at 56/58) | **PASS** |
| 5 | SIMH A: `1234` -> `0012.34`, КОНЕЦ ЗАДАЧИ | **PASS** |
| 6 | SIMH (a): same image, `5678` -> `0056.78`, КОНЕЦ ЗАДАЧИ | **PASS** |
| 7 | SIMH (b): one machine-word patch -> `0022.34`, КОНЕЦ ЗАДАЧИ | **PASS** |
| 8 | SIMH (c): byte-identical restore -> `0012.34`, КОНЕЦ ЗАДАЧИ | **PASS** |
| 9 | C-oracle MTR/ACPU agree with SIMH | **PASS** |
| 10 | `777001..777004` parsed by this contour | **FAIL** (out of scope; requirements in §3) |
| 11 | `777010/777011` emitters present / formatted READ | **FAIL** (absent from repo; requirements in §3) |
| 12 | `arg1` wider than 4 digits or signed/exponent literals | **FAIL** (not decoded; disclosed in §3) |

## 7. Evidence index

```
scripts/ir4_build.py              builder (measure + A/PATCH/RESTORE images)
scripts/build_e2e.py              copied read-only helpers (rz/wz/short/word/f32)
scripts/oracle_ir.py              C-dispak oracle wrapper (MTR/CORE only)
scripts/setup_simh.py             isolated ini, stock -n prn, workspace-local prn0
scripts/drive_simh.py             SIMH driver (ДATA:/send-keys/ДАЙ/НОМВ)
decks/deck_ir{1234,5678}.b6       A/B decks, four operand bytes differ
frontbuild/x{1234,5678}/          injected FRONT source, build/call decks and outputs
images/2048_{base,IR4_A,IR4_PATCH,IR4_RESTORE}
runs/localprn_{A,B,PATCH,REST}.txt  raw SIMH ACPU (authoritative)
runs/console_*.txt                raw SIMH console transcripts
runs/ini_*.ini                    per-case SIMH configs (copies)
oracle/{dump1234,MTR1234b,MTR5678,MTRPATCH}/  raw C MTR/CORE (oracle only)
logs/card_buffer_ir1234_at_entry.txt  decoded card buffer at contour entry
logs/MTR_IR4_*_contour.txt        clean MTR excerpts used in §2
```

DONE
