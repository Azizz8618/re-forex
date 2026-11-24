# MANIFEST: integrated variant-B + DO + ABS product

Discipline: workspace `/tmp/.private/azizz/opencode/b-final-do/` only. Copies of
every builder, deck, image and harness. No repository edit, no live disk, no
tmux session 0, no C `dispak` patch. C `dispak` was used only as an advisory
oracle (MTR/CORE); all authoritative verdicts are isolated full-SIMH `prn0`
captures from `harness/drive_b.py`.

## Deliverables

| path | meaning |
|:--|:--|
| `images/2048_MODFINAL_B2` | THE ONE integrated image (candidate canonical variant-B product; all features) |
| `images/2048_FULL_PATCH` | one-machine-word PATCH gate of the same image (`--patch 1.0`) |
| `images/2048_FULL_RESTORE` | byte-identical restore of the candidate |
| `images/2048_base` | proven FRX5 base contour (unchanged input) |
| `images/2048_2048_FINAL_A6` | previous canonical image `b9bfba21…` (DO/ABS absent) |
| `decks/T*.b6` | 17 REAL fixed-form Fortran source decks (no `777005`, no fixtures) |
| `build/b_final_do_build.py` | reproducible merged builder (B5 + B4 + B6a + B6b + B6c + docs/129) |
| `build/run_suite_full.py` | full 16-case sequential SIMH suite driver |
| `harness/drive_b.py`, `harness/setup_b.py` | workspace copies of the proven b-harness |
| `harness/runs/verdict_FINAL2_*.json`, `localprn_FINAL2_*.txt` | authoritative verdicts / printer captures |
| `report.md` | PASS/FAIL table, raw excerpts, word budget, recommendation |

## SHAs (SHA-256)

```
5fd132876c9c6297dfeb2400d16771ac2b559328feee7ad1ad93303a8509c7d9  images/2048_MODFINAL_B2 (delivered; all features)
afb67ca5e96b59cac8ee17aeaacc9e2b3adbcec1ae64164c0ca851bf2a4e8ca5  images/2048_FULL_PATCH (built from B2)
5fd132876c9c6297dfeb2400d16771ac2b559328feee7ad1ad93303a8509c7d9  images/2048_FULL_RESTORE
e8bcf6b6e4727164b71e699a70f3e97c1d73b8c6388f5730fe952b522c02cd0f  images/2048_FULL_A2 (pre-MOD, all non-MOD gates passed)
2f5fcf873d43c2846ee1669669e26202f32fa25e6b71e109fd20ef4452142ff5  images/2048_base
b9bfba21b13d420f05ccbc2827d543a5a0bed23d42b2ae30aeb10595ca6612e4  images/2048_2048_FINAL_A6 (previous)
d058305796bcd0aaf108056f595ee2a222762abe31cf3bb59f1697c9473ca675  SIMH /home/azizz/Yandex.Disk/simh/BIN/besm6
```

Deck SHAs (SHA-256, first 16 shown; full values in `report.md`):

```
845d4f59f8af6aa3  T1_lit_A      8441a801149e46ce  T1_lit_B
1d034678dbcf0fed  T2_expr_A     4fdad173cd8b1ed2  T2_expr_B
9e18cd8c8433c177  T2_parens     945d7ba6b1afd4d3  T3_w4
b726c7fb156d68e6  T3_w2         562ac2edfb9bef38  T4_sqrt_A
ef8915c182a9f7dc  T4_sqrt_B     fe0e154f806a251f  T4_abs_A
15e427637ee19be2  T4_abs_B      9a125f35332f4222  T5_do_2
c2ade8f1b68d63f8  T5_do_3       e127b31ea6221374  T6_negative
```

`T5_do_2` vs `T5_do_3`: **1 deck byte** (1-based offset 154, octal `62` -> `63`).
PATCH vs candidate: **6 image bytes in 3 machine words** (one 6-byte `K_PATCH`
word plus the two recomputed zone-N+2 checksum copies). RESTORE is byte-identical.

## Reproduce

```
cd /tmp/.private/azizz/opencode/b-final-do
python3 build/b_final_do_build.py --build MODFINAL_B2
python3 build/b_final_do_build.py --build FINAL2_PATCH --patch 1.0
cp images/2048_FINAL2_PATCH images/2048_FULL_PATCH
cp images/2048_MODFINAL_B2 images/2048_FULL_RESTORE
python3 build/run_suite_full.py 2048_MODFINAL_B2
```

## What is reused (proven code, not rewritten)

* `parser_build.build_parser` - verbatim B4 shunting-yard evaluator with precedence,
  parentheses and the verbatim B3 dispatcher / print path (203 words).
* `c6_build.build_n3`, `c7_build.width_tables`, `final_sign` - docs/105 GOST converter (55 changed N+3 words).
* `b5_build` source-digit chain, sliding windows, GETCH/EMIT and the N+2 data map.
* B6a single-pass PRINT/FORMAT label and Fw.d resolution.
* B6b Newton SQRT (adapted: pool holds the true value, not 10x).
* B6c fixed-count DO source decoding and machine countdown (adapted to the shared scanner and N+1 body code space).
* docs/129 ABS mechanism: sign-aware `avx` negate, unary-minus `C_NEG`, and the
  structural gap guard lesson (reserved `LONG UJ` word at every region end).
* `build_e2e` zone I/O / checksums and `dispatch_build.tok()` B2 token encoder.

No IR card, no fixture token, no FRONT, no host-computed result digit.
