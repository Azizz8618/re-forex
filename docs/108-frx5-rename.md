# FRX5* renamed-translator SIMH acceptance - FINAL

> РЕЗУЛЬТАТ главного агента: **PASS** по переименованию `OURMRK*` → `FRX5*`.
> Каталог зоны `N` слово 2 заменено на `FRX5*` (WORD `0o4662702512000000`),
> образ `2f5fcf87…` побайтово воспроизводится скриптом
> `tools/forex500-ir4sign/rename_catalog.py` из канонического `f483f6ca…`.
> Все 5 гейтов SIMH PASS: `21 -0012.34`, `21 -0056.78`, SIGNBIT → `21 0012.34`,
> restore → минус, негатив `OURMRK*` → `ОТСУТСТВУЕТ OURMRK*`.
> Важно: `*NAME` в деке должен быть **6 символов** (`FRX5XX`); 4‑символьное
> `FRX5` сдвигает fixed‑offset чтение IR‑карты и даёт `ПЕРЕПОЛНЕНИЕ АУ`.
> Колоды: `tests/plan-f77/89-frx5/`. Текущий SIMH‑бинарь `9ef71b26…` —
> значения SHA в docs/102 и docs/107 (`b555acc0…`) устарели.

Date: 23.11.2026. Workspace `/tmp/.private/azizz/opencode/frx5-simh/`.
Copies only: no repo edits, no live disks, no tmux session 0, no C `dispak`
patches. C `dispak` was **oracle only** and was not needed for any result below;
all authoritative output is full SIMH ACPU/printer capture. Every attached image
is a workspace-local copy.

## VERDICT: PASS - all five gates, with the 6-character-name deck fix

| gate | image (SHA prefix) | deck | expected | raw prn result | verdict |
|:--|:--|:--|:--|:--|:--|
| A | `2f5fcf87…` | `deck_frx5xx_1234.b6` | `21 -0012.34` | `21 -0012.34  3000.00` | **PASS** |
| b | `2f5fcf87…` (byte-identical copy) | `deck_frx5xx_5678.b6` | `21 -0056.78` | `21 -0056.78  3000.00` | **PASS** |
| c | `cfbfb6d7…` (one SIGNBIT word patched) | `deck_frx5xx_1234.b6` | `21  0012.34` | `21  0012.34  3000.00` | **PASS** |
| d | `2f5fcf87…` (fresh byte-identical restore) | `deck_frx5xx_1234.b6` | `21 -0012.34` | `21 -0012.34  3000.00` | **PASS** |
| neg | `2f5fcf87…` | `deck_frx5xx_ourmrk.b6` | `ОТСУТСТВУЕТ OURMRK*` | `ОТСУТСТВУЕТ  OURМRК*` | **PASS** |

All five reached `КОНЕЦ ЗАДАЧИ`. Gate A and gate d produced the identical result
on byte-identical images; gate c changed only the sign while all four digits
stayed `0012.34`; gate b changed only the IR operand. The negative control still
fails translator lookup after the rename, as required.

### The earlier FAIL was a deck-name-length issue, NOT a product defect

With the originally supplied deck (`*NAME FRX5`, 4 characters), gates A-d all
printed `ПЕРЕПОЛНЕНИЕ АУ +160905981253⏨-09 2013035300360035` and no result line.
That was traced to the deck, not the image or the emulator: shortening only
`*NAME` to four characters on the **canonical** image reproduced the identical
overflow, while five- or six-character names worked; the renamed image with
`*NAME FRX5XX` works. Now that the deck cards use a 6-character name (same length
as the canonical `*NAME OURMRK`), every gate passes. The catalog rename and the
contour body were never at fault.

---

## 1. Boot-marker timeout: Harness root cause (FACT, unchanged)

The lead's `TimeoutError: no ДATA: boot marker in capture-pane` came from
`Can't open file /tmp/.private/azizz/opencode/ir4-sign/runs/ini_FRX5.ini` in the
preserved failed capture: the driver's hardcoded workspace differed from where
the ini was placed, so SIMH sat at `sim>` and never booted. Fix: self-contained
workspace with all images/decks/inis, per-case prn capture, isolated tmux socket
(`runs/tmux`, via `TMUX_TMPDIR`). Detected `ДATA:` via `capture-pane` only; all
input via `send-keys` only; `ДАЙ А0`, `ДАЙ А1`, `НОМВ` before the deck; post-deck
`НОМВ` only after the confirmed `B075-1` / `ОЗ(075)` job-start lines.

## 2. Emulator binary (FACT)

`/home/azizz/Yandex.Disk/simh/BIN/besm6`,
SHA-256 `9ef71b260e8a780d12fa63c152c5979dd8dc50e8959a57849bd73fb5252a8254`,
mtime 23.11.2026 18:05:23. **Docs 102 and 107 quote `b555acc0e22f270617a1b560`;
those references are stale** because the binary was rebuilt again afterwards.
The BESM6 C sources match git HEAD (only data/config files are dirty). No docs
were modified here; the lead will update them. The current binary was
functionally validated by the canonical-image control run, so the SHA drift does
not affect the verdict.

## 3. Final decks (canonical framing preserved)

Both final decks were generated from the canonical deck `deck_ir1234.b6`
(SHA `388e6da3…`) with only the two header cards changed, plus the IR digit field
for the 5678 variant. Line-by-line diff versus canonical:

```
1234: ~5 *NAME OURMRK → *NAME FRX5XX
      ~6 *TRANS:OURMRK*,,412350 → *TRANS:FRX5*,,412350
5678: same two lines plus ~8  777005 ... 1234 ... → ... 5678 ...
```

Every other card (`ШИФР`, `ДИС`, `ОЗУ/АЦП`, `ЕЕВ1А3`, `PROGRAM MAIN`, `END`,
`*EXECUTE`, `*END FILE`, the backtick line and `ЕКОНЕЦ`) is byte-for-byte
identical to canonical. Paths and SHAs:

```
/tmp/.private/azizz/opencode/frx5-simh/decks/deck_frx5xx_1234.b6
  SHA-256 37ad17d69475017172bb1d838c0e974d2a62498100cf05e3481568ca2ce57c2b
/tmp/.private/azizz/opencode/frx5-simh/decks/deck_frx5xx_5678.b6
  SHA-256 6ea6259fb0620e28574486a2025c8545e6af5a3a68fedc4a20d00ab1e8443315
/tmp/.private/azizz/opencode/frx5-simh/decks/deck_frx5xx_ourmrk.b6   (negative control)
  SHA-256 80d9be50c389bf304478e992ba311d4263441a96458c1f687a389925a3f5fd73
```

## 4. Raw ACPU / printer excerpts (authoritative: `runs/localprn_<case>.txt`)

Stock `attach -n prn0` semantics with a per-case workspace-local path; the
driver's `runs/acpu_<case>.txt` copies of the shared `ACPU/output.txt` contain
stale lines from older jobs and are not evidence.

Gate A (`runs/localprn_FIX_A.txt`, lines 98-114):

```
*NАМЕ FRХ5ХХ
           *ТRАNS:FRХ5*,,412350
 21 -0012.34  3000.00

 ДАЙ ТРАКТЫ          +272109334312⏨-19    0010020000000016
  АП   Э     РК    И1    И2    И3    И4    И5    И6    И7    И10   И11   И12   И13   И14   И15   И16   И17   КРА  ЗПСЧ
02063 02063 00006 02034 00000 00000 00000 64000 02020 02065 03332 03015 01160 02020 00000 06134 00040 53422 00000 53400
...
 КОНЕЦ ЗАДАЧИ        +000000000000⏨+00    0000206320000000
```

Gate b (`runs/localprn_FIX_B.txt`, line 100 / 114):

```
*NАМЕ FRХ5ХХ
           *ТRАNS:FRХ5*,,412350
 21 -0056.78  3000.00
 ...
 КОНЕЦ ЗАДАЧИ        +000000000000⏨+00    0000206320000000
```

Gate c, one-word SIGNBIT patch (`runs/localprn_FIX_PATCH.txt`, lines 98-105):

```
*NАМЕ FRХ5ХХ
           *ТRАNS:FRХ5*,,412350
 21  0012.34  3000.00

 ДАЙ ТРАКТЫ          +272109334312⏨-19    0010020000000016
```

Gate d, byte-identical restore (`runs/localprn_FIX_RESTORE.txt`, lines 100/114):

```
 21 -0012.34  3000.00
 ...
 КОНЕЦ ЗАДАЧИ        +000000000000⏨+00    0000206320000000
```

Negative control (`runs/localprn_FIX_NEG.txt`, lines 99-105):

```
*NАМЕ FRХ5ХХ
           *ТRАNS:ОURМRК*,,412350

   ОТСУТСТВУЕТ  ОURМRК*
          СВОБОД   01770

 КОНЕЦ ЗАДАЧИ        +000000000000⏨+00    0000000000001146
```

Console markers were present in every positive run, e.g. FIX_A
(`runs/console_FIX_A.txt`): `ДATA:23.11.26 BPEMЯ:18.32.00`, `ДАЙ А0`, `ДАЙ А1`,
`НОМВ`, `sim> at vu0 .../deck_frx5xx_1234.b6`, `go`, `B075-1 410300000000`,
`ОЗ(075) 410300000000 18.32 M=059`, post-job-start `НОМВ`. The negative run
correctly has no `ОЗ(075)` (translator lookup failed).

## 5. SHAs (SHA-256)

```
9ef71b260e8a780d12fa63c152c5979dd8dc50e8959a57849bd73fb5252a8254  BIN/besm6 (current rebuilt; docs' b555acc0... is stale)
2f5fcf873d43c2846ee1669669e26202f32fa25e6b71e109fd20ef4452142ff5  images/2048_FRX5_FIX_A / _FIX_B / _FIX_RESTORE / _FIX_NEG
                                                                    and the supplied images/2048_FRX5_TEST (all byte-identical; unchanged post-run)
cfbfb6d7b3efe04479b3991742c327acc9eaeb962c6a847112c3e6804e653abf  images/2048_FRX5_FIX_PATCH (SIGNBIT word 1->0 at file offset 10411686 plus two zone-N checksum copies 0o33->0o32 at 10410846/10410878)
f483f6ca1e60c58415d816111757ec9a35da04b545d79cf3c7656c0f1484120b  images/2048_IR4SIGN_A (canonical image, read-only reference)
37ad17d69475017172bb1d838c0e974d2a62498100cf05e3481568ca2ce57c2b  decks/deck_frx5xx_1234.b6
6ea6259fb0620e28574486a2025c8545e6af5a3a68fedc4a20d00ab1e8443315  decks/deck_frx5xx_5678.b6
80d9be50c389bf304478e992ba311d4263441a96458c1f687a389925a3f5fd73  decks/deck_frx5xx_ourmrk.b6
388e6da393727e33d73d6e12c1bb32355f1538b16abc864583281f09c6d28c02  canonical deck deck_ir1234.b6 (base for the two final decks)
```

FACT: decoded catalog word 2 of every FRX5 image is `0o4662702512000000` =
six-bit text `FRX5*   `, versus `0o5765625562531200` = `OURMRK* ` in canonical A.
The old name occurs nowhere else; only that word and the two zone-N checksum
copies differ from canonical A (18 bytes), both checksums verify. A and d ran on
byte-identical images. C `dispak` was not used for acceptance.

## 6. FACT / INFERENCE

FACT: all four positive gates printed the exact expected line and reached
`КОНЕЦ ЗАДАЧИ` with continuation word `0000206320000000`; the negative control
printed `ОТСУТСТВУЕТ OURMRK*` and reached `КОНЕЦ ЗАДАЧИ`; the SIGNBIT patch
changed only the sign, IR 5678 changed only the digits, and restore reproduced A.
FACT: the earlier FAIL was caused by the 4-character deck name, reproduced on the
canonical image and eliminated by a 6-character name on the renamed image.
INFERENCE (not MTR-traced): the 4-character `*NAME` shifts the DISPAK card buffer
so the fixed-offset reader at RAM `0o64014` bytes 2..5 misses the `1234` digits.

## 7. Should the FRX5 catalog rename replace the canonical repo image?

**Recommendation: NO - keep the canonical image `f483f6ca…` as the product
image.** Reasons, all evidence-based:

* The rename is functionally neutral: the FRX5 image
  `2f5fcf873d43c2846ee1669669e26202f32fa25e6b71e109fd20ef4452142ff5` is
  byte-identical to canonical A
  `f483f6ca1e60c58415d816111757ec9a35da04b545d79cf3c7656c0f1484120b` except for
  catalog name word 2 and its two checksum copies. Acceptance output is identical
  with the fixed deck, so there is no functional gain.
* A clean `FRX5*` deck is impossible with the current contour: the 4-character
  `*NAME FRX5` fails, so the passing deck has to use the mismatched alias
  `*NAME FRX5XX` with `*TRANS:FRX5*`. Adopting it as canonical would bake a
  deck-name/translator-name mismatch into the product and all its docs/tests.
* Replacing would require coordinated updates to the canonical deck SHA
  (`388e6da3…` -> `37ad17d6…` / `6ea6259f…`), docs 102/107 and existing tests,
  with no behavioral benefit.

If a rename is nevertheless required by product decision, use a 5- or
6-character translator name (for example `FRX5TR*`) so that `*NAME FRX5TR` and
`*TRANS:FRX5TR*` are both valid and consistent; the exact artifacts for the
current `FRX5*` variant, should it be adopted as-is, are image
`2f5fcf873d43c2846ee1669669e26202f32fa25e6b71e109fd20ef4452142ff5` with decks
`37ad17d69475017172bb1d838c0e974d2a62498100cf05e3481568ca2ce57c2b` (IR 1234)
and `6ea6259fb0620e28574486a2025c8545e6af5a3a68fedc4a20d00ab1e8443315`
(IR 5678).

## 8. PASS / FAIL table

| # | criterion | verdict |
|:--|:--|:--|
| 0 | Diagnose boot-marker timeout as Harness issue | PASS |
| A | FRX5 image + IR 1234 -> `21 -0012.34` | **PASS** |
| b | same image + IR 5678 -> `21 -0056.78` | **PASS** |
| c | one-word SIGNBIT patch -> `21  0012.34` | **PASS** |
| d | byte-identical restore -> `21 -0012.34` | **PASS** |
| - | all reach `КОНЕЦ ЗАДАЧИ` | PASS |
| 3 | negative control `ОТСУТСТВУЕТ OURMRK*` | **PASS** |
| - | current binary SHA confirmed; stale docs noted, docs untouched | PASS |
| - | final decks at the requested paths with canonical framing | PASS |

DONE
