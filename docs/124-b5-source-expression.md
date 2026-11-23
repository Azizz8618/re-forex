# B5 INTEGRATION: REAL Fortran source expression, lexed and computed entirely by our machine code

> РЕШАЮЩИЙ РЕЗУЛЬТАТ ВАРИАНТА Б: **PASS**. В целевом деке лежит настоящий
> Fortran‑текст `X=1.5+2.5*4.0` (без `777005`, без `*FOREX`), наш лексер
> machine‑кодом читает его, токены идут в B4 shunting‑yard и B3/GOST.
> SIMH: `4.0 → 21 -0011.50`, `2.0 → -0006.50` при том же образе (1 байт
> в деке), PATCH → `-0011.60`, restore → `-0011.50`, скобки → `-0016.00`.
> Все `КОНЕЦ ЗАДАЧИ`. Бюджет 40/58 N+3, 472/649 N+2, запретная зона
> 526..900 не тронута. Отложено: метки, несколько операторов, PRINT/FORMAT,
> intrinsic по имени, DO (B6/B6a).

**Date:** 24.11.2026. **Workspace:** `/tmp/.private/azizz/opencode/b5-source-expr/`.
**Discipline:** copies only; no repository edit, no live disk, no tmux session 0, no C `dispak`
patch. C `dispak` was **oracle only** (MTR/CORE hooks). All authoritative A/B/PATCH/RESTORE/PARENS
verdicts are full SIMH printer captures from the b-harness. Emulator
`/home/azizz/Yandex.Disk/simh/BIN/besm6`, SHA-256 prefix `9ef71b26` (verified on every run).

---

## 0. VERDICT

| gate | verdict |
|:--|:--|
| Machine-code lexer reads REAL fixed-form Fortran card text (columns 7..72) | **PASS** |
| Multi-digit real literals, identifiers, `= + - * / ( )` tokenized in source order | **PASS** |
| Token stream + machine-derived literal floats handed to verbatim B4 shunting-yard | **PASS** |
| Verbatim B3 print path / docs/105 converter produces the computed value | **PASS** |
| A: `X=1.5+2.5*4.0` -> `21 -0011.50` | **PASS** |
| B: `X=1.5+2.5*2.0` -> `21 -0006.50` (image byte-identical to A) | **PASS** |
| PATCH: one machine word of OUR code -> `21 -0011.60` | **PASS** |
| RESTORE: byte-identical image -> `21 -0011.50` | **PASS** |
| PARENS: `X=(1.5+2.5)*4.0` -> `21 -0016.00` | **PASS** |
| Word budgets N+3 <= 58, N+2 <= 649 free words, forbidden 526..900 untouched | **PASS** |
| Full F77 statement coverage (labels, multi-statement, PRINT/FORMAT, intrinsics, DO) | **FAIL** (deferred, §8) |

---

## 1. RAW DECK (printed verbatim, no IR cards, no fixtures)

Deck A (`decks/deck_exprA.b6`, SHA-256 `bcdd3e9d68b15946575b6548618da97b3b5d0ed7c32af5a38577dcec39006e38`):

```
ШИФР 410300 ЗС5^
ДИС 41(2048)^
ОЗУ 32^АЦП 32^
ЕЕВ1А3
*NAME FRX5XX
*TRANS:FRX5*,,412350
      PROGRAM MAIN
      X=1.5+2.5*4.0
      END
*EXECUTE
*END FILE
``````
```

Deck B differs in **one card byte**: `X=1.5+2.5*4.0` -> `X=1.5+2.5*2.0`
(1-based deck offset 142, octal `064` -> `062`, i.e. ASCII `4` -> `2`).
Deck PARENS: `X=(1.5+2.5)*4.0`.
There is no `777005`, no `*FOREX`/`*FTN`, no host-computed result anywhere in the deck or image.

The RLE card buffer at RAM `0o64012..0o64014` for deck A decodes (C CORE dump) as:

```
064012  86 58 3d 31 2e 35  <6sp>X=1.5
064013  2b 32 2e 35 2a 34  +2.5*4
064014  2e 30 c0 0a 0a 0a  .0<64sp>\n\n\n
```

---

## 2. WHAT WAS BUILT (reuse, not rewrite)

One new machine-code routine `LEX` (183 words, assembled by `build/b5_build.py`) reads the card
buffer byte by byte and emits the B2 one-word token stream into `N+2[64..]` plus machine-derived
literal floats into `N+2[100..]`. It then executes `LONG UJ 0o22243` into the **verbatim** B4
shunting-yard parser (`parser_build.build_parser`, 203 words, copied unchanged), which stores
`10*result` into the symbol value word; the **verbatim** B3 `PRINT` handler calls the **verbatim**
docs/105 GOST converter in N+3 (40/58 words). No parallel print/converter/dispatch mechanism was
written.

`LEX` is a single state machine (modes 0 scan-for-`=`, 1 expression, 2 number) with one shared
byte-fetch routine, reusing B1's proven RLE byte-shift table (`UTC 20000` + `ASX` indexed by the
byte register) and B1's first-card-word load. Digits are accumulated by on-machine FPU
`F = F*10 + float(d)`; `float(d)` uses the proven docs/104 `e+x EMASK / e+x C105` normalization;
fractional digits are divided out on machine with `a/x f32(10)`. Token words are built with
bitwise XOR of disjoint fields (floating `a+x` cannot construct an integer bit pattern with zero
mantissa). Stack/loop counters use a +100 bias so one's-complement `-0` never defeats `UZA`.

Token stream emitted from the Fortran text (decoded from C CORE at the B4 entry `0o22243`):

| N+2 idx | TK | SUB | PAY | source |
|--:|--:|--:|--:|:--|
| 64 | 10 | 30 | 0 | `PROGRAM` (seeded keyword scaffold) |
| 65 | 2 | 0 | 1 | program name (seeded) |
| 66 | 10 | 31 | 0 | `REAL` (seeded keyword scaffold) |
| 67 | 2 | 0 | 1 | `X` declared (seeded) |
| 68 | 11 | 0 | 0 | EOL |
| 69 | 2 | 0 | 1 | `X` (source letter before `=`) |
| 70 | 8 | 0 | 0 | `=` (source byte) |
| 71 | 1 | 0 | 0 | `1.5` (source digits -> pool 0) |
| 72 | 3 | 1 | 0 | `+` |
| 73 | 1 | 0 | 1 | `2.5` (source digits -> pool 1) |
| 74 | 3 | 3 | 0 | `*` |
| 75 | 1 | 0 | 2 | `4.0` (source digits -> pool 2; B: `2.0`) |
| 76 | 11 | 0 | 0 | EOL |
| 77 | 10 | 34 | 0 | `PRINT` (seeded) |
| 78 | 13 | 1 | 1026 | `F4.2` (seeded) |
| 79 | 2 | 0 | 1 | `X` |
| 80 | 11 | 0 | 0 | EOL |
| 81 | 10 | 37 | 0 | `END` (seeded) |

The three literal floats in the pool are built by machine from the deck digit bytes; the print
digits come from the BESM FPU and the verbatim converter, never from the host.

---

## 3. DECISIVE SIMH A/B/PATCH/RESTORE/PARENS (authoritative, prn0)

| gate | image SHA-256 (full) | deck | prn0 line 100 | line 114 | verdict |
|:--|:--|:--|:--|:--|:--|
| A | `6c661248fbee8157ee9ff6862f1ed64c9c2ca30c06ac1894ba8de3a749c44986` | `X=1.5+2.5*4.0` | ` 21 -0011.50  3000.00` | `КОНЕЦ ЗАДАЧИ` | PASS |
| B | `6c661248fbee8157ee9ff6862f1ed64c9c2ca30c06ac1894ba8de3a749c44986` (byte-identical) | `X=1.5+2.5*2.0` | ` 21 -0006.50  3000.00` | `КОНЕЦ ЗАДАЧИ` | PASS |
| PATCH | `16b0f71b4e1c77e1c412ac55c296dae0043d930fd77c8fca3a49cfedf3ca094e` | same as A | ` 21 -0011.60  3000.00` | `КОНЕЦ ЗАДАЧИ` | PASS |
| RESTORE | `6c661248fbee8157ee9ff6862f1ed64c9c2ca30c06ac1894ba8de3a749c44986` (= A) | same as A | ` 21 -0011.50  3000.00` | `КОНЕЦ ЗАДАЧИ` | PASS |
| PARENS | `6c661248fbee8157ee9ff6862f1ed64c9c2ca30c06ac1894ba8de3a749c44986` | `X=(1.5+2.5)*4.0` | ` 21 -0016.00  3000.00` | `КОНЕЦ ЗАДАЧИ` | PASS |

Byte diffs (`cmp -l`):
* `deck_A` vs `deck_B`: **1 byte** at 1-based 142, octal `064`->`062` (the Fortran digit).
* image A vs PATCH: **one N+2 machine word**, offset 151 (`K_PATCH` of the verbatim B4 parser),
  `f32(0)` -> `f32(1.0)`, plus the two recomputed zone checksum copies. Every other N+2 word is
  identical; the deck and emulator are byte-identical.
* image A vs RESTORE: **empty** (same SHA, byte-identical restore).

Causality: with the image frozen, changing one Fortran digit byte changes the printed value
`11.50 -> 6.50`; with the deck frozen, changing one machine word of OUR code changes
`11.50 -> 11.60`; restoring the exact image restores `11.50`. All digits are machine-derived.

The `-` sign is the verbatim converter's proven sign-byte convention for a positive EST
(docs/105, docs/119); interpreted values are `11.50`, `6.50`, `11.60`, `11.50`, `16.00`.
A (`11.50`, not left-to-right `16.00`) proves `*`-over-`+` precedence; PARENS (`16.00`)
proves that parentheses override it; B proves a single deck digit changes the computed value.

---

## 4. RAW ACPU / MTR EVIDENCE

Authoritative prn0 captures (per-case driver logs in `logs/drive_B5X_*.log`):

```
B5X_A      : " 21 -0011.50  3000.00"  ...  " КОНЕЦ ЗАДАЧИ ... 0002253520000000"
B5X_B      : " 21 -0006.50  3000.00"  ...  " КОНЕЦ ЗАДАЧИ ..."
B5X_PATCH  : " 21 -0011.60  3000.00"  ...  " КОНЕЦ ЗАДАЧИ ..."
B5X_RESTORE: " 21 -0011.50  3000.00"  ...  " КОНЕЦ ЗАДАЧИ ..."
B5X_PARENS : " 21 -0016.00  3000.00"  ...  " КОНЕЦ ЗАДАЧИ ..."
```

C `dispak` oracle reproduces every printed value (oracle only, all `rc 0`):
`oracle/B5A10/out.txt` `-0011.50`, `oracle/B5B/out.txt` `-0006.50`,
`oracle/B5P/out.txt` `-0011.60`, `oracle/B5R/out.txt` `-0011.50`,
`oracle/B5PAR/out.txt` `-0016.00`.

Curated C MTR of OUR lexer at `0o27721` (`evidence/mtr_b5_lexer_curated.txt`, window
`027721..030200`) shows: base-register setup, `utc 20000`/`asx 21641(13)` indexed card-byte
fetch, `aax 2000` digit nibble extraction, `e+x`/`a*x`/`a+x` float build, `a/x` fractional
division, `atx 22003(6)` literal-pool store and `atx 21737(6)` B2 token store.
C CORE at B4 entry `0o22243` shows the token stream of §2 and the machine-derived pool floats.

---

## 5. WORD BUDGET (exact, measured from the build and whole-image diff)

| resource | used | limit | verdict |
|:--|--:|--:|:--|
| N+3 hot path (verbatim converter + floor_int) | **40 words** | 58 | PASS (18 free) |
| N+2 LEX data cells | 62 words (offsets 2..63 minus 33, plus 96,97) | - | PASS |
| N+2 LEX code | **183 words** (tail 901..1023 + low 162..199, 245..259, 463..469) | - | PASS |
| N+2 verbatim B4 parser code | 203 words (offsets 260..462) | - | PASS |
| N+2 whole footprint (changed words vs base) | **472 words** | 649 free | PASS |
| N+2 forbidden band offsets 526..900 | **0 words changed** | 0 | PASS |
| body N+1 words touched | **6 words** (`0o11` entry + `0o112..0o116` converter cells) | 998 (keeper `0o26` untouched) | PASS |
| zone N+4 | not used | unavailable | PASS |

No overrun, no new opcode, no MMU trick beyond the proven `UTC 20000` / M20 mechanism.
The tail band 901..1023 is used exactly as mapped by docs/110 (RAM `0o27721..0o30113`).

---

## 6. SUPPORTED F77 SOURCE SUBSET (FACT)

* One fixed-form statement card in columns 7..72, RLE card buffer at `0o64012..`.
* One assignment `V=<expr>` where `V` is a single-letter real variable; `V` and `=` are read from
  the source bytes (the name word at `N+2[1]` is built from the source ASCII).
* Real literals with a decimal point and arbitrary digit counts (integer and fractional part are
  accumulated on the machine and divided by 10 per fractional digit). In the decisive decks these
  are `1.5`, `2.5`, `4.0`, `2.0`.
* Binary operators `+ - * /` with `* /` above `+ -`, left associativity, and parentheses; all
  emitted as B2 tokens in source order and evaluated by the verbatim B4 shunting-yard.
* Keyword scaffolding tokens `PROGRAM`, `REAL`, `PRINT`, `F4.2`, `END` and the statement EOLs are
  seeded constants: statement labels and keywords are explicitly **skipped**, as permitted.

---

## 7. SHAs (SHA-256)

```
6c661248fbee8157ee9ff6862f1ed64c9c2ca30c06ac1894ba8de3a749c44986  2048_B5_A = 2048_B5_B = 2048_B5_RESTORE
16b0f71b4e1c77e1c412ac55c296dae0043d930fd77c8fca3a49cfedf3ca094e  2048_B5_PATCH  (N+2[151] one word)
2f5fcf873d43c2846ee1669669e26202f32fa25e6b71e109fd20ef4452142ff5  2048_base (unchanged)
bcdd3e9d68b15946575b6548618da97b3b5d0ed7c32af5a38577dcec39006e38  deck_exprA.b6
9c43bb508730dc7b0930e7504cd5c607f12c44f321cf083b8abc8ab5e9664716  deck_exprB.b6
6908cc8e932b8621c102cdb6df9548b31a4c8567bd836da04933e4f66ff9a95b  deck_parens.b6
```

---

## 8. DEFERRED (not achieved in B5)

1. **Multi-statement programs**: only one assignment plus seeded `PRINT`/`END` scaffolding;
   no EOF-driven statement loop from source.
2. **`PRINT`/`FORMAT` parsed from text**: `PRINT` and the `F4.2` descriptor are seeded constants.
3. **Intrinsics by name** (`ABS`, `SQRT`, `MOD`): TK=5 exists in B2 but is not wired.
4. **`DO`/`CONTINUE`, labels, multi-letter identifiers, statement labels**: not lexed.
5. **Unary minus, exponentiation, division-by-zero checks, full `Fw.d`, E/I/G editors**: unsupported.
6. **Negative computed results**: sign block inherited but not validated for a computed negative.

---

## 9. FACT / INFERENCE

**FACT:** the deck is real Fortran text; the A/B image is byte-identical; one deck digit byte
changes the printed value; one N+2 word of our code changes it; RESTORE is byte-identical; all jobs
print a `21` line and reach `КОНЕЦ ЗАДАЧИ`; token stream and literal floats were dumped from C CORE
at the B4 entry; N+3=40/58, N+2 forbidden band untouched, body keeper untouched.

**INFERENCE / limits:** the keyword scaffolding is intentional (explicitly allowed by the task);
the two-digit float scaling divides by 10 per fractional digit and assumes no exponent notation;
the tail-band code placement is a local allocation choice consistent with docs/110; the `-` sign
interpretation is inherited from docs/119.

---

## 10. EVIDENCE INDEX

```
build/b5_build.py                 integrated builder (LEX + verbatim parser + verbatim converter)
build/drive_b5.py                 workspace-local copy of the b-harness driver
build/collect_evidence.py         evidence aggregator -> evidence/gates_b5.json
decks/deck_{exprA,exprB,parens}.b6  real Fortran source cards
images/2048_B5_{A,B,PATCH,RESTORE}
evidence/mtr_b5_lexer_curated.txt  raw C MTR of OUR lexer
evidence/n2_at_b4_entry.txt        N+2 tokens + machine-derived pool floats at B4 entry
build/runs/{localprn,console,acpu,verdict}_B5X_*.txt|json
oracle/{B5A10,B5B,B5P,B5R,B5PAR}/out.txt   C-oracle printed values
```

SHA-256 of supporting captures:
```
8e9fa9b9585844991429ad1edcd8be1e2c1552e170edeb1121c1dd2520df6da3  oracle/B5A10/out.txt
baf7b438eb7fa94c4c6a92f7ff14d2db49470e3ed6aa391589a5909720c53b85  oracle/B5B/out.txt
20a5f0f559f2c74ea685881078efcbc44bef475e203ce8c8cc0769e9f94013ab  oracle/B5P/out.txt
8e9fa9b9585844991429ad1edcd8be1e2c1552e170edeb1121c1dd2520df6da3  oracle/B5R/out.txt
452b29d090e3d6a9f24235615477acd0982073a9881a357c93c36cbc125e44a5  oracle/B5PAR/out.txt
46dd9b5debc58dbaa24921fb293916a51dd23e4810fd688b7c5de78bb14160d1  evidence/mtr_b5_lexer_curated.txt
```

Structured verdict and all invariants: `evidence/gates_b5.json`: `all_product_PASS`,
`all_values_match`, `all_komets`, `image_A_eq_B`, `image_A_eq_RESTORE`, `image_PATCH_diff_A`
are all **true**.

DONE
