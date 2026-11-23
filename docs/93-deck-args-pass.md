# deck-args: zone-2350 contour reads its numeric ARGUMENT from the DECK's Fortran source

> ГЛАВНЫЙ РЕЗУЛЬТАТ: **PASS** с оговоркой объёма. Один и тот же байтово
> тождественный образ контура печатает разные числа, если в deck’е поменять
> только литерал: `X=1.0` -> `21 1.00 3.00`, `X=2.0` -> `21 2.00 3.00`.
> Контур читает сырой текст карты из ОЗУ `0o64000..` через `utc 60000` +
> `xta 4012` (страница `0o150` доступна в user mode), затем машинный
> FPU→GOST печатает цифру. Это **доказывает передачу аргумента из деки** и
> машинную конвертацию, но НЕ полную компиляцию: FREXT/IR‑записей в деке
> нет, исполняется hand‑built 23‑словная процедура (§1.2). Важно для READ:
> путь ввода через сырой буфер карты работает, в отличие от привилегированного
> `э52` (`docs/91/92`).

Date: 23.11.2026. Workspace: `/tmp/.private/azizz/opencode/deck-args/`
(bulky copies and all logs under `data/`; the shared `/dev/shm` tmpfs filled up
mid-session, so the data were moved into this workspace. Repo, live disks,
tmux session 0 and dispak C sources were never edited. Every SIMH/C-dispak
image was a copy. SIMH used stock `attach -n prn0/prn1`, `ДATA:` marker via
`capture-pane`, all input via `send-keys`, `ДАЙ А0`/`ДАЙ А1`/`НОМВ` before the
deck, post-job-start `НОМВ`, and isolated tmux sockets.)

## VERDICT: PASS (decisive A/B) — with an explicit scope limit

One byte-identical contour image printed **two different numbers** under full
SIMH because only the DECK literal changed:

| case | deck Fortran line | contour image SHA-256 | ACPU line |
|:--|:--|:--|:--|
| A | `      X=1.0` | `4b8365ee…` | `21 1.00 3.00` |
| B | `      X=2.0` | `4b8365ee…` (same) | `21 2.00 3.00` |

Both reached `КОНЕЦ ЗАДАЧИ`. Deck contains only
`*TRANS:OURMRK*,,412350`; no `*FOREX`, `*FTN`, `*perso`.

**Scope limit (do not overclaim):** this proves *deck-to-contour argument
transfer* and on-machine FPU→GOST conversion of a deck-supplied digit. It does
**not** by itself prove "our translator compiles the source program": no
FREXT/IR records (777010/777011) exist in this deck-only run (§1.2), and the
contour still executes a hand-built 23-word routine, not a front-end/codegen
product. The claim requires the additional phase-4 milestones of
`docs/63-full-compiler-design.md` §5.

---

## 1. Where the deck's source text lands at contour entry

### 1.1 Raw card text: RAM `0o64000..`, FACT

C-dispak oracle (only the C emulator has `BESM6_CORE_ON_PC`, `docs/88`
lines 70-79) was run with `BESM6_CORE_ON_PC=01770`, `BESM6_CORE_SKIP=6`,
i.e. the contour entry at RAM `0o1770`. Raw CORE:
`data/oracle/v3_x1/core-pc.bin` (SHA-256
`c625849bc22bb5e2ce43cb6336c89c39bc881dc65bbe25b691c07da07de589cb`);
decoded dump `data/logs/card_buffer_at_entry_x1.txt`. The complete deck card
stream is present in RAM, 6 bytes per 48-bit word, UPP/COSY encoding
(`docs/20-besm6-text-encodings.md:32,83,96`):

```
064000 1244710123242601  2a 4e 41 4d 45 81  *NAME.
064001 2365252223251113  4f 55 52 4d 52 4b  OURMRK
064002 6160501202405012  c7 0a 0a 0a 0a 0a  ......
064003 1245212220247123  2a 54 52 41 4e 53  *TRANS
064004 1644752524446522  3a 4f 55 52 4d 52  :OURMR
064005 2262505413032061  4b 2a 2c 2c 34 31  K*,,41
064006 1443146514136412  32 33 35 30 bd 0a  2350..
064007 4145012223643522  86 50 52 4f 47 52  .PROGR
064010 2024660123240511  41 4d 81 4d 41 49  AM.MAI
064011 2354041202405012  4e c1 0a 0a 0a 0a  N.....
064012 4145407514227060  86 58 3d 31 2e 30  .X=1.0    <-- ASCII digit 0x31, byte 3
064013 1343030602405012  c8 0a 0a 0a 0a 0a  .0.....
064014 4144251621145012  86 45 4e 44 ca 0a  .END..
```

Corroborating sources:
- `monitor80-re/utility/boot.asm:3` — `AIO:,EQU,64000B`: `0o64000` is the
  monitor's AIO/exchange-page base.
- `monitor80-re/permanent/monread%.asm:33-57` — `M15,*70,1` reads a card,
  `разбор:` decodes it into `MONCARD*` via `COZУTISO` (`:73`). The raw card
  image written by this path lands in the `AIO` band observed in CORE.
- `docs/62-newcomp-re.md:229-240` — the copy loop puts OUR body at
  `0o1757+k`, so `body[9]` is `0o1770` (our entry). `*TRANS` does not itself
  pass a source pointer; the source is already in the card buffer when the
  body runs.

**Can our contour read it? FACT, yes.** A 12-bit address field cannot reach
`0o64012` (`reference/412/lindis.py:55,63`; `docs/77-onmachine-format-limit.md:16-18`).
We use the proven modifier mechanism: `utc 60000` sets `M20`, then a short
`xta 4012` forms the effective address `0o60000+0o4012=0o64012`. Raw C MTR
(`data/logs/MTR_v3_AB_excerpt.txt`):

```
MTR 30114R utc    60000(0)  AU=0200600002006
MTR 30115L xta    64012(0)  AU=0200600002006
MTR 30115R utc    30000(0)  AU=4145407514227060   <-- card word, digit 0x31
```

MMU: protection is page-granular (`besm6_mmu.c:305-310`, `besm6_cpu.c:1049-1092`);
page `0o64000>>10 = 0o150` is readable in this context (FACT: both SIMH and C
oracle executed the read without `Число в чужом листе`). Other pages can trap
(`docs/88-ft002-15bit-blocked.md:70-79`, `utc 70000` attempt), so the result is
per-page, not a blanket claim. **INFERENCE:** the exact store instruction that
filled `0o64000` was not traced; the identification of the buffer with the
`AIO` band rests on `boot.asm:3` plus the CORE bytes.

### 1.2 FREXT / IR records: not present, FACT

`777010` (`READ X/1.0/`) and `777011` (FORMAT descriptors) are **outputs of our
FRONT.FTN stage**, documented in `docs/77-onmachine-format-limit.md:7,25`;
the IR schema `777001/2/3/4` is produced by `FRONT.FTN` in
`docs/63-full-compiler-design.md:43-62`. The deck used here never invokes
FRONT, and a scan of the entry CORE found no such numeric IR records; only raw
card text at `0o64000`. Therefore `*TRANS` does **not** expose FREXT/IR
records to the contour in this configuration. This is not a defect of the
contour: the stage that would produce them was never run.

---

## 2. The contour routine (same machine code in A and B)

Builder: `scripts/build_deckargs3.py`; it only rewrites zone `0o2351`
(`body[9]`, GOST digit byte zeroed) and the 58-word high-RAM window
`0o2353 → 0o30114..0o30205` (`docs/65-high-ram-zone.md:28-48`). Routine,
addresses derived from `0o30000+short` with `M20` armed by the preceding
`utc`:

| halfword | action |
|:--|:--|
| `30114R` | `utc 60000` arm card-page modifier |
| `30115L` | `xta 4012` → ACC = card word `0o4145407514227060` |
| `30116L` | `asx` right 16 → digit byte in low byte |
| `30117L` | `aax 0o377` → ASCII `0o61`/`0o62` |
| `30120L` | `arx +0xd0` → `0x101`/`0x102` (positive operand; a negative two's-complement operand double-carries in `arx`) |
| `30121L` | `aax 0o377` → integer `1`/`2` |
| `30122L`,`30123L` | `asx` left 41, `arx FBASE` → BESM-6 float `1.0`/`2.0` |
| `30124L..30142L` | proven `docs/89` chain: `a/x 1.0`, `aex`, `e+x 105`, `aax MASK40`, `asx` → packed digit, `arx/atx GOST 0o2006`, `*64 2004`, `uj 0(15)` |

No host-computed weight, no C patch, no monitor/LINK patch. All constants are
inside the documented 58-word window; addresses beyond its 58-word limit are
not copied into RAM (measured by sentinel probe, `data/oracle/sentinel` during
this session, 58/58 words k=0..0o71 arrive).

---

## 3. Raw evidence

### 3.1 C-dispak MTR excerpt (oracle only, `data/logs/MTR_v3_AB_excerpt.txt`)

```
===== deck X=1.0 =====
MTR 30114R utc    60000(0) AU=0200600002006
MTR 30115L xta    64012(0) AU=0200600002006
MTR 30115R utc    30000(0) AU=4145407514227060
MTR 30117R utc    30000(0) AU=0000000000061     ; ASCII '1'
MTR 30121R utc    30000(0) AU=0000000000001     ; integer 1
MTR 30123R utc    30000(0) AU=4050000000000000  ; float 1.0
MTR 30135R utc    30000(0) AU=0000000000001     ; GOST digit 1
PRINT: ' 21 1.00 3.00'
===== deck X=2.0 =====
MTR 30117R utc    30000(0) AU=0000000000062     ; ASCII '2'
MTR 30121R utc    30000(0) AU=0000000000002
MTR 30123R utc    30000(0) AU=4110000000000000  ; float 2.0
PRINT: ' 21 2.00 3.00'
```

Full oracle stdout: `data/oracle/v3_x1/out.txt`, `data/oracle/v3_x2/out.txt`.

### 3.2 SIMH ACPU (authoritative), stock `-n prn`

`data/runs/acpu_v3s1.txt` (A) and `data/runs/acpu_v3s2.txt` (B), raw lines:

```
*NАМЕ ОURМRК
           *ТRАNS:ОURМRК*,,412350
 21 1.00 3.00          <- deck X=1.0
...
 КОНЕЦ ЗАДАЧИ        +000000000000⏨+00    0000206320000000
```

```
*NАМЕ ОURМRК
           *ТRАNS:ОURМRК*,,412350
 21 2.00 3.00          <- deck X=2.0
...
 КОНЕЦ ЗАДАЧИ        +000000000000⏨+00    0000206320000000
```

Console showed `2048 - 41` and `B075-1 410300000000` in both cases.

### 3.3 SHAs (SHA-256)

```
4b8365eec3c318b7ff3deba782ad0d297971567fb6382b8c25e6280c730b079d  images/2048_deckargs3       (A and B, byte-identical)
c07a2b359bd1b0c1f359128818f5bdb7da436a59f6f28c60bb723bc493529dd0  decks/deck_x1.b6            (X=1.0)
11b4c8bed5c2b2da27652e8da3f52bd354d484ab66a9210451fb9512e4b7fee3  decks/deck_x2.b6            (X=2.0)
c625849bc22bb5e2ce43cb6336c89c39bc881dc65bbe25b691c07da07de589cb  data/oracle/v3_x1/core-pc.bin
9ca3338594b94018ec3d79919c6aabe04fba52894929c17ab24015054f1338a0  data/runs/acpu_v3s1.txt
67c0c501e4afcfdc74067a8b5feaff0b0f6bf7ab82ffe5b14503dd2657fa04a6  data/runs/acpu_v3s2.txt
```

---

## 4. FACT / INFERENCE summary

| statement | marker |
|:--|:--|
| Deck card text is in RAM at `0o64000..` at contour entry, including `X=1.0` at `0o64012` byte 3 | FACT (CORE + MTR) |
| `utc 60000` + short `4012` reads it; no MMU trap in page `0o150` | FACT (SIMH + C MTR) |
| Same contour image SHA prints `21 1.00` / `21 2.00` for the two decks | FACT (SIMH ACPU) |
| FREXT/IR records are absent in the deck-only run | FACT (CORE scan + docs/63, docs/77) |
| The `AIO` band at `0o64000` is filled by `MONREAD*`/card path | INFERENCE (`boot.asm:3`, `monread%.asm:33-57`, CORE bytes; store not traced) |
| Reading one literal means the translator "compiles the source program" | **FALSE / not established**; needs the FRONT/CODEGEN/EMIT milestones |

## 5. Minimum change if IR records are required

No monitor/loader change is needed to read deck **literals** (proved above).
If the goal is to hand our contour **FREXT/IR records** (777001..4, 777010/11),
the minimum change on copies would be to extend the `*TRANS` hand-off so that
the IR produced by FRONT is placed in a known, modifier-addressable area
before `vjm 64002`: e.g. have the loader copy a short IR table into the free
cells of the 58-word `N+3` window (`docs/65-high-ram-zone.md:28-48`) or into
reserved body slots `0o41..0o43` (`docs/70-computed-output/README.md:11-20`),
using the same `M6` receiver loop already documented in
`docs/62-newcomp-re.md:229-240`. This is a **design proposal (INFERENCE)**;
it was not implemented, because the task forbids monitor/loader edits.

## 6. Evidence index

```
scripts/build_deckargs3.py          builder (same-length substitutions only)
scripts/c_oracle.py                 C-dispak CORE/MTR oracle wrapper
scripts/drive_case.py               SIMH driver (copies, isolated tmux, stock -n prn)
decks/deck_x1.b6 / deck_x2.b6       A/B decks, only X literal differs
images/2048_deckargs3               byte-identical contour image for both cases
oracle/v3_x1|v3_x2/out.txt          raw C-dispak MTR/ACPU logs
oracle/v3_x1/core-pc.bin            raw CORE at contour entry
logs/MTR_v3_AB_excerpt.txt          MTR excerpt used in §3.1
logs/card_buffer_at_entry_x1.txt    decoded card buffer from CORE
runs/acpu_v3s1.txt / v3s2.txt       raw SIMH ACPU output
runs/console_v3s1.txt / v3s2.txt    raw SIMH console capture
runs/ini_v3s1.ini / ini_v3s2.ini    per-case SIMH configs (all attached images are copies)
```

DONE
