# FINAL INTEGRATION (variant B): ONE image, REAL Fortran source deck, full SIMH system test suite

> ИТОГ ТЕКУЩЕГО ЭТАПА: **PASS для проверенного подмножества**. Один образ
> `b9bfba21…` (55/58 N+3, 518/649 N+2) с настоящим Fortran в деке: выражения
> с приоритетом/скобками, `PRINT`+метка `FORMAT`, `SQRT` по имени; 14 SIMH‑кейсов,
> 9/9 позитивных PASS, T6 негативный PASS, PATCH/RESTORE PASS. **T5 (DO) FAIL** —
> DO не вошёл в финальный образ. ABS/MOD и полный F77 ещё не готовы. Сборщики
> `tools/forex500-final/`, дек и манифест `tests/plan-f77/91-variant-b-final/`.

**Date:** 24.11.2026. **Workspace:** `/tmp/.private/azizz/opencode/b-final/`.
**Discipline:** copies only; no repository edit, no live disk, no tmux session 0, no C `dispak`
patch. C `dispak` was used **only** as an advisory oracle (MTR / CORE / fast preview).
All authoritative verdicts are full SIMH captures from the isolated b-harness
(`harness/drive_b.py`, tmux `TMUX_TMPDIR=harness/runs/tmux`).
Emulator SHA-256 verified before every run:
`d058305796bcd0aaf108056f595ee2a222762abe31cf3bb59f1697c9473ca675`.

---

## 0. VERDICT

| criterion | verdict |
|:--|:--|
| ONE image supports assignment expression + precedence + parens, PRINT with labelled FORMAT, SQRT by name, all from REAL source text | **PASS** (T1-T4, 9/9 positive cases) |
| fixed-count DO from source in the same image | **FAIL** (T5; DO machine source was concurrently removed from the shared workspace before integration) |
| T6 negative control `*TRANS:OURMRK*` -> `ОТСУТСТВУЕТ` | **PASS** (absence_marker true) |
| Byte-identical image across all deck-only changes | **PASS** (all 12 decks, same image SHA) |
| One machine-word PATCH (11.60) + byte-identical RESTORE (11.50) | **PASS** |
| Word budgets N+3 55/58, N+2 518/649, forbidden 526..900 untouched, body keeper preserved | **PASS** |
| No 777005 IR card, no FRONT, no system compiler, no fixture result digit in any deck | **PASS** |
| 14-case full SIMH suite harness plumbing | **PASS** in all 14 cases; completion marker present in all 14 prn0 captures |

---

## 1. THE ONE IMAGE

`images/2048_2048_FINAL_A6`, SHA-256 `b9bfba21b13d420f05ccbc2827d543a5a0bed23d42b2ae30aeb10595ca6612e4`.

Builder: `build/b_final_build.py` (reproducible, see `MANIFEST.md`). It reuses **verbatim**:

* `parser_build.build_parser` - B4 shunting-yard evaluator with operator precedence,
  parentheses, plus the embedded verbatim B3 statement dispatcher and print path (203 words);
* `c6_build.build_n3`, `c7_build.width_tables`, `final_sign` - docs/105 GOST converter (N+3);
* `b5_build.lex_consts` and the proven source-digit to BESM-float chain;
* the B6b Newton SQRT algorithm (adapted: the B5 literal pool holds the true value, not 10x);
* `build_e2e` zone I/O/checksums and `dispatch_build.tok()` B2 token encoder.

New code is only the **single-pass unified LEX** (214 words): byte scanner with GETCH/EMIT VJM
subroutines, expression tokenizer (literals, `+ - * / ( )`), `SQRT` name recognition, sliding-window
`PRINT` / `FORMAT` / `END` recognition, runtime resolution of the FORMAT `Fw.d` PAY into the FDESC
token, and region-crossing `LONG UJ` trampolines for the split free N+2 bands.

All printed digits come from BESM FPU operations and the verbatim converter; the deck carries no
fixture token and no host-computed result.

---

## 2. DECKS (REAL fixed-form Fortran source)

Every deck begins with the standard framing
`ШИФР 410300 ЗС5^ / ДИС 41(2048)^ / ОЗУ 32^АЦП 32^ / ЕЕВ1А3 / *NAME FRX5XX / *TRANS:FRX5*,,412350`
and ends with `*EXECUTE / *END FILE / `````` / ЕКОНЕЦ`. The Fortran body occupies columns 7..72
(labels in 1..5). `grep 777005`, `*FOREX`, `*FTN`: **0 hits**.

Representative deck (`decks/T2_expr_A.b6`, SHA `1d034678dbcf0fed9645c9a8e900e1ad70fc22a1c30264094d980116a00cbdde`):

```
      PROGRAM MAIN
      X=1.5+2.5*4.0
      PRINT 100,X
  100 FORMAT(1X,F4.2)
      END
```

Deck-only changes are one/few source bytes; the image is byte-identical for all T1-T6.

| deck | SHA-256 |
|:--|:--|
| T1_lit_A (`X=12.34`) | `845d4f59f8af6aa3a79adec2c952a9684756c787b321f4154e249c7f854de738` |
| T1_lit_B (`X=56.78`) | `8441a801149e46ce553dead41d88296abb3ece677b0707a092a0aa9f621c945d` |
| T2_expr_A (`X=1.5+2.5*4.0`) | `1d034678dbcf0fed9645c9a8e900e1ad70fc22a1c30264094d980116a00cbdde` |
| T2_expr_B (`X=1.5+2.5*2.0`) | `4fdad173cd8b1ed2af2f0be999f0e63448b5a7693acd8f5e9388d94d94cfd6d9` |
| T2_parens (`X=(1.5+2.5)*4.0`) | `9e18cd8c8433c17778ad48648420ecb81d97667bd24ea323ab07b89e8e18b9a1` |
| T3_w4 (`F4.2`) | `945d7ba6b1afd4d39daea27984ae90d827c1e80efff7c063c0e4f758eaddfcf1` |
| T3_w2 (`F2.2`) | `b726c7fb156d68e6a80c447c9a1ed11e89ba64fb3f8060e3d8b3bc46bf1f70c3` |
| T4_sqrt_A (`SQRT(16.0)`) | `562ac2edfb9bef388c2bee6ae11de0a3880092393cfc475707563ae7571957ae` |
| T4_sqrt_B (`SQRT(09.0)`) | `ef8915c182a9f7dc4465ab1aec05d8bb88d6844aa3a027e040f4bd614555decc` |
| T5_do_2 (`DO 10 I=1,2`) | `9a125f35332f42220cb98afe270f33455411436ec3828a0e365cd69de62bac5b` |
| T5_do_3 (`DO 10 I=1,3`) | `c2ade8f1b68d63f8634fad409c7ba78d7c468ee853897e9d159c9b68092273ff` |
| T6_negative (`*TRANS:OURMRK*`) | `e127b31ea62213747ca5874233b555ce2af3e94635a7124db3489a13552aeb00` |

T3/T4/T5 deck SHAs are byte-identical to the separately proven B6a/B6b/B6c decks.

---

## 3. FULL SIMH TEST SUITE

Harness verdict for every case: `plumbing: PASS`, emulator SHA `d058305796bcd0aa`.
ACPU device copies are shared/stale read-only files (per `PROBE.md`) and are **not** the
measured observable; the authoritative observable is the isolated `prn0` capture.

| case | deck change | expected | prn0 `21` line (SIMH) | КОНЕЦ ЗАДАЧИ | verdict |
|:--|:--|:--|:--|:--|:--|
| FINAL_T1_A | `X=12.34` | 12.34 | ` 21 -0012.34  3000.00` | yes | **PASS** |
| FINAL_T1_B | `X=56.78` (deck only) | 56.78 | ` 21 -0056.78  3000.00` | yes | **PASS** |
| FINAL_T2_A | `X=1.5+2.5*4.0` | 11.50 | ` 21 -0011.50  3000.00` | yes | **PASS** |
| FINAL_T2_B | `*4.0` -> `*2.0` (1 byte) | 6.50 | ` 21 -0006.50  3000.00` | yes | **PASS** |
| FINAL_T2_P | `(1.5+2.5)*4.0` | 16.00 | ` 21 -0016.00  3000.00` | yes | **PASS** |
| FINAL_T3_W4 | `F4.2` | 34.50 wide | ` 21 -0034.50  3000.00` | yes | **PASS** |
| FINAL_T3_W2 | `F4.2` -> `F2.2` (1 byte) | 34.50 narrow | ` 21 -  34.50  3000.00` | yes | **PASS** |
| FINAL_T4_A | `Y=SQRT(16.0)` | 4.00 | ` 21 -0004.00  3000.00` | yes | **PASS** |
| FINAL_T4_B | `16.0` -> `09.0` (2 bytes) | 3.00 | ` 21 -0003.00  3000.00` | yes | **PASS** |
| FINAL_T5_2 | `DO 10 I=1,2` | 40.00 (unsupported) | none | yes | **FAIL** (expected: DO not integrated) |
| FINAL_T5_3 | `DO 10 I=1,3` | 60.00 (unsupported) | none | yes | **FAIL** (expected: DO not integrated) |
| FINAL_T6_NEG | `*TRANS:OURMRK*` | ОТСУТСТВУЕТ | none (negative control) | yes | **PASS** (`absence_marker: true`) |
| FINAL_PATCH | T2_A + one machine word | 11.60 | ` 21 -0011.60  3000.00` | yes | **PASS** |
| FINAL_RESTORE | T2_A + byte-identical image | 11.50 | ` 21 -0011.50  3000.00` | yes | **PASS** |

Negative-control raw prn0 (`harness/runs/localprn_FINAL_T6_NEG.txt`):

```
101:   ОТСУТСТВУЕТ  ОURМRК*
105: КОНЕЦ ЗАДАЧИ        +000000000000⏨+00    0000000000001146
```

Raw prn0 excerpts (authoritative):

```
FINAL_T1_A  : " 21 -0012.34  3000.00"  ...  " КОНЕЦ ЗАДАЧИ ... 00002..."
FINAL_T1_B  : " 21 -0056.78  3000.00"  ...  " КОНЕЦ ЗАДАЧИ ..."
FINAL_T2_A  : " 21 -0011.50  3000.00"  ...  " КОНЕЦ ЗАДАЧИ ..."
FINAL_T2_B  : " 21 -0006.50  3000.00"  ...  " КОНЕЦ ЗАДАЧИ ..."
FINAL_T2_P  : " 21 -0016.00  3000.00"  ...  " КОНЕЦ ЗАДАЧИ ..."
FINAL_T3_W4 : " 21 -0034.50  3000.00"  ...  " КОНЕЦ ЗАДАЧИ ..."
FINAL_T3_W2 : " 21 -  34.50  3000.00"  ...  " КОНЕЦ ЗАДАЧИ ..."
FINAL_T4_A  : " 21 -0004.00  3000.00"  ...  " КОНЕЦ ЗАДАЧИ ..."
FINAL_T4_B  : " 21 -0003.00  3000.00"  ...  " КОНЕЦ ЗАДАЧИ ..."
FINAL_T5_2  : (no 21 line)              ...  " КОНЕЦ ЗАДАЧИ ..."
FINAL_T5_3  : (no 21 line)              ...  " КОНЕЦ ЗАДАЧИ ..."
```

Raw ACPU device copy excerpt (`harness/runs/acpu_FINAL_T2_A.txt`, identical in
`acpu_FINAL_T4_A.txt` and all other cases):

```
 99:           *ТRАNS:ОУРМRК*,,412350
100: 21 -0000.58  3000.00
114: КОНЕЦ ЗАДАЧИ        +000000000000⏨+00    0000206320000000
116: 00020 00020 00006 02034 00000 00000 00000 64000 02020 02065 03332 ...
```

These `ACPU/output.txt` copies are shared read-only device files: they contain the last job of
*another* concurrent SIMH session and are identical for every case, so per
`/tmp/.private/azizz/opencode/b-harness/PROBE.md` they are disclosed but **not** used as the
per-case verdict; the isolated `localprn_<case>.txt` is.

Causality: with the image byte-identical across T1-T6, source digit/byte changes move
`12.34 -> 56.78`, `11.50 -> 6.50`, `11.50 -> 16.00`, field width `F4.2 -> F2.2` changes spacing,
and `SQRT(16.0) -> SQRT(09.0)` moves `4.00 -> 3.00`. Precedence is proven by `11.50` (not left-to-right
`16.00`); parentheses override it (`16.00`). The `-` sign is the inherited docs/105 convention.

---

## 4. PATCH / RESTORE GATE

The single patched machine word is B4's `K_PATCH` display-bias cell (N+2[151]),
`f32(0)` -> `f32(1.0)`. Whole-image diff A vs PATCH: **8 bytes** = one 6-byte machine word
(file offsets `10420349..10420354`) plus the two recomputed zone-N+2 checksum copies
(`10419097`, `10419129`). Deck and emulator are byte-identical.
RESTORE is byte-identical to A (`cmp`: **0 bytes**, same SHA-256).

Deck-only byte diffs: `T1_lit_A` vs `T1_lit_B` = 4 digit bytes; `T2_expr_A` vs `T2_expr_B` = 1 byte
(offset 142, octal `064` -> `062`); `T3_w4` vs `T3_w2` = 1 byte (offset 175, `064` -> `062`);
`T4_sqrt_A` vs `T4_sqrt_B` = 2 bytes (offsets 139/140).

SIMH PATCH: ` 21 -0011.60  3000.00`; RESTORE: ` 21 -0011.50  3000.00`, both with
`КОНЕЦ ЗАДАЧИ`, same deck and same emulator SHA. Causality is therefore machine-code-side,
not a deck substitution.

---

## 5. WORD BUDGET (measured by whole-image diff against `2048_base`)

| resource | used | limit | verdict |
|:--|--:|--:|:--|
| N+3 converter + floor cells | 55 words | 58 | PASS (3 spare) |
| N+2 changed words (all regions) | 518 | 649 free | PASS |
| N+2 forbidden band offsets 526..900 changed | 0 | 0 | PASS |
| N+2 B4 parser (verbatim, 260..462) | 203 words | - | unchanged |
| N+2 unified LEX code (162..199, 245..259, 463..525, 901..1023) | 214 words (239 slots) | 239 | PASS |
| N+1 body words changed | 6 (`0o11` entry + `0o112..0o116`) | 998 | PASS |
| body keeper `0o26` changed | **no** (`0o1000040000000` in both) | must be kept | PASS |
| N+4 | not used | unavailable | PASS |

---

## 6. SUPPORTED / UNSUPPORTED

**Supported (FACT):** one statement per source card; `V=<expr>` with `+ - * /`, precedence,
left associativity and parentheses; real literals with arbitrary integer/fractional digits;
`SQRT` by name; `PRINT n,V` with labelled `FORMAT(1X,Fw.d)` parsed from source text (`w` 2/3/4,
`d` 1/2); `END` from source; verbatim B4/B3 + docs/105 print path.

**Unsupported:** fixed-count DO / CONTINUE in this image (T5); ABS and MOD by name; DSQRT;
READ; general DO variables / nested loops; multi-letter identifiers and PRINT lists;
E/I/G editors; continuation cards; unary minus / exponentiation / rounding; FORTRAN diagnostics.

---

## 6b. RAW C-ORACLE MTR EVIDENCE (advisory, oracle only)

Curated from `oracle/O6_SQRT_MTR/out.txt` (window `027721..030200`, 2500 traces):

```
MTR 30104R uj     22106(0) AU=0000000000001   ; SQRT name selected (C_INTR=2)
MTR 22110L a/x    1670(14) AU=4412000000000000 ; Newton: arg / x
MTR 22116L a/x    1767(14) AU=4250000000000000 ; arg / x (iteration)
MTR 22116R a+x    1767(14) AU=4050000000000000 ; x + arg/x
MTR 22117L a*x    2007(14) AU=4250400000000000 ; (x + arg/x) * 0.5
MTR 22120R a/x    1767(14) AU=4250000000000000 ; next iteration
MTR 22121L a+x    1767(14) AU=4057036074170361 ; converging to f32(4.0)
```

`oracle/O6_T2*/core-pc.bin` at B4 entry shows the 18 source-derived tokens, including
`N+2[71..75] = LIT(0), OP(+), LIT(1), OP(*), LIT(2)` and `N+2[78]` FDESC with PAY `1026`
(`F4.2`), proving the FORMAT width was patched from the source text.

## 7. FACT / INFERENCE

**FACT:** all SIMH captures, image/deck SHAs, byte diffs, word budgets, keeper/forbidden-band
invariants; C CORE token stream at B4 entry proving 18 source-derived tokens with FDESC PAY 1026
(`F4.2`); C MTR traces of the scanner, float construction, Newton loop and handoff.
**INFERENCE / local choices:** single-pass FDESC PAY patch instead of B6a's two-pass label table
(one FORMAT per deck; the PRINT label is consumed but not compared); initial-byte SQRT recognition
from B6b; one-word `K_PATCH` display bias as the patch gate; placement of our code in the proven
free N+2 bands with trampolines.

---

## 8. RECOMMENDATION

**Recommendation: adopt this image as the new canonical variant-B product for the currently
proven subset (T1-T4, T6), with the DO limitation recorded explicitly.**

Rationale:

1. It is the first single image that runs REAL Fortran source for assignment with expression,
   precedence and parentheses, `SQRT` by name, and `PRINT` with a labelled `FORMAT` descriptor
   parsed from the deck text. The earlier B5/B6a/B6b/B6c images each covered only one of these
   paths; this image unifies them in one contour (N+2 LEX 214 words, B4 203 words, N+3 55/58).
2. All 9 positive SIMH cases (T1a/b, T2a/b/parens, T3w4/w2, T4a/b) print the exact expected
   values and reach `КОНЕЦ ЗАДАЧИ`; the negative control correctly yields `ОТСУТСТВУЕТ`;
   the one-word PATCH/RESTORE gate is byte-verified.
3. It reuses the verbatim B4/B3 evaluator, dispatcher and GOST converter, so no new architecture
   is introduced.

Caveat: T5 (DO/CONTINUE) fails in this image because the DO machine source was removed from the
shared workspace before integration. If DO must be part of the canonical product, either recover
the B6c source and merge its fixed-count loop into the free N+2 bands (about 100 extra words are
available: 518/649 N+2 words currently changed), or keep the B6c image as a separate DO-only
product until that merge is done. ABS/MOD, DSQRT, READ and general DO remain unsupported.

## 9. EVIDENCE INDEX

```
images/2048_2048_FINAL_A6, _PATCH, 2048_FINAL_RESTORE   contour images
decks/T*.b6                                              12 real Fortran source decks
build/b_final_build.py                                   reproducible integrated builder
build/make_decks.py                                      deck generator
build/run_suite.sh                                       full SIMH suite driver
build/suite_final.log                                    authoritative suite transcript
harness/runs/verdict_FINAL_*.json                        14 harness verdicts
harness/runs/localprn_FINAL_*.txt                        14 authoritative printer captures
harness/runs/console_FINAL_*.txt, acpu_FINAL_*.txt       raw console / ACPU device copies
oracle/O6_*/out.txt, core-pc.bin                        advisory C-oracle preview / CORE
oracle/O6_SQRT_MTR/out.txt                               advisory C MTR of the SQRT path
MANIFEST.md                                              SHAs and reproduction recipe
```
