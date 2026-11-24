# B9: multi-digit F77 labels + minimal CALL/SUBROUTINE name binding

> РЕЗУЛЬТАТ: **PASS** под SIMH — `CALL SUB` печатает `21 -0056.78`, `CALL OTHER`
> при байтово том же образе `834a5a08…` печатает `21 -0078.90`; PATCH → `-0061.70`,
> restore → `-56.78`, все `КОНЕЦ ЗАДАЧИ`. Имя SUBROUTINE разбирается из Fortran‑текста
> в 6‑битное TEXT‑слово и сравнивается machine‑кодом; CALL передаёт управление.
> Исправлены: region‑guard против one‑shot `utc`, `AEX` вместо `AOX` для сравнения,
> анализ границы `SUBROUTINE <name>`, FIXUP PAY. Бюджет 55/58 N+3, 540/649 N+2,
> body 639/998, keeper и 526..900 сохранены.

## 0. Verdict

**Both tasks PASS on authoritative full SIMH.**

* **Task 1 (multi-digit labels):** byte-identical image prints `21 -0012.34` for `GOTO 100`
  and `21 -0056.78` for `GOTO 200`; PATCH flips an IF gate, RESTORE returns. Verified in the
  earlier round and re-verified here (C10_G100 / C10_G200).
* **Task 2 (CALL/SUBROUTINE name binding):** implemented entirely in BESM-6 machine code.
  Byte-identical image prints `21 -0056.78` for `CALL SUB` and `21 -0078.90` for `CALL OTHER`;
  one-machine-word PATCH (`L_TEN` f32(10) -> f32(11)) gives `21 -0061.70`; byte-identical
  RESTORE returns `-56.78`. All reach `КОНЕЦ ЗАДАЧИ`. Non-regression GOTO 100/200, T1 and T5
  all PASS. No host/compiler faking: the name is parsed from Fortran source into a 6-bit TEXT
  word, compared on-machine, and the CALL transfers control to the named subroutine body.

Discipline: workspace `/tmp/.private/azizz/opencode/b9-labels/` only; copies of every builder,
deck, image and harness. No repository file, live disk, tmux session 0, SIMH binary or C
`dispak` source was modified. C `dispak` was used only as an advisory oracle (MTR/CORE); every
product verdict is an isolated full-SIMH `prn0` capture via `harness/drive_b.py` with every
`attach ttyN Line=N,PORT` shifted to `6300+N` (docs/135/137). SIMH binary verified on every run:
`d058305796bcd0aaf108056f595ee2a222762abe31cf3bb59f1697c9473ca675`.

## 1. Artifacts (SHA-256)

```
834a5a08f2934887b6b83a0e4b0782bceef628769d0b1497d7da7710edc1fc11  images/2048_B9C_A  (A=B=RESTORE)
735d46a764790de7f91e66728072d621a083b2390366a4b89e5fac56b83f83bc  images/2048_B9C_PATCH
81d7790f7541ebcfee248c5fc5264b74c6b82c942b57d79f5b3e07046cd8eb7acbcc  images/2048_B9_A (Task 1)
72800718de9355a81766e8214121aab06d388cf5acd492dfae58e7137e2b9c67      images/2048_B9_PATCH
488cab0cdc6ff4649a56e89f2159afeafd2b01a3156b6186deac099f86ba5055  decks/deck_B9C_A.b6 (CALL SUB)
dd3305a683de09bcc6c88bac4348e4aa86b56152d0dc7d280a9e578f72201c77  decks/deck_B9C_B.b6 (CALL OTHER)
4abc1d38696c0f955dad7c58a0090cb2bbf4bb5f8ac6ded70018566dff1cf7da  decks/deck_B9_A.b6 (GOTO 100)
b565498fb6d362c67584d93d34028a2a4799b6f2789f4c61fa9ebd33ef591006  decks/deck_B9_B.b6 (GOTO 200)
```

Builders: `build/b9_labels_build.py` (Task 1), `build/b9_call_build.py` (Task 1 + CALL).
Marker sweep: `build/marker_sweep2.py`. All verdicts/captures: `harness/runs/`.

## 2. Step 1: docs/120-style marker sweep of the suspect cells

`build/marker_sweep2.py` wrote 26 distinct marker words into **every** suspect cell on the
known-passing Task-1 image: body indices `0o536,0o537,0o654..0o667,0o670..0o677,0o716` and
N+2 offsets `153,154,155`, then ran a full C-oracle job (`deck_B9_A.b6`) with a CORE dump at
B4 `DONE` (post LEX/FIXUP). **Every one of the 26 markers reported `KEEP`** with its exact
expected value; the job still printed `21 -0012.34` and `КОНЕЦ ЗАДАЧИ`.

Conclusion: the body gap `0o670..0o677` and N+2 `153..155` survive LEX/B4 execution, so no
relocation was needed. This also matches the invariant table in §6 (forbidden band untouched,
keeper preserved). The earlier "garbage cells" observation was a UTC-corrupted control flow,
not a cell collision. (One constant, `BW_NEG20`, was initially placed at body `0o775`, which
*is* inside code region `0o740..0o1234` and got overwritten; it was moved to the proven-free
N+2 offset 33 and the sweep confirmed stability.)

## 3. Machine-level defects found and fixed (Task 2)

1. **Region-end guard vs. UTC modifier.** The added code grew LEX from 605 to ~742 halfwords,
   pushing `PATCHTOK` across the region-6 boundary. Its last halfword was `utc 20000`, so the
   one-shot modifier was inherited by the region-end LONG UJ guard and corrupted its target
   (`0o21066 -> 0o41066`), causing the CPU to run through zero words and `КОНТРОЛЬ КОМАНДЫ`.
   Fixed by 8 halfwords of padding at LEX entry, which keeps every UTC one instruction clear
   of a guard; docs/129 region-end guards, keeper and forbidden band are unchanged.
2. **`AEX` is XOR, not subtract.** The 6-bit TEXT code must be `ASCII - 0x20` (docs/109/114).
   Using `AEX 0x20` produced `ASCII ^ 0x20` (wrong codes). Fixed by adding a two's-complement
   `-0x20` cell (`BW_NEG20`, N+2 offset 33) with the proven integer-add opcode `ARX`.
3. **`AOX` is OR, not XOR.** The name compare used `AOX`, which never matches nonzero names.
   Fixed to `AEX` (XOR) with `UZA` on equality; C-oracle MTR then showed `BW_NSUB > 0` and a
   bound name word (`0o646643`) equal to the CALL name word.
4. **Keyword/name boundary.** `SUBR` matching consumes the first four characters of
   `SUBROUTINE`, so the name parser had to skip the rest of the keyword to the separating space
   (phase flag) before accumulating the name. Likewise `CALL` name accumulation starts after
   the space. Both names now pack identically.
5. **CALL name -> token PAY.** The parsed CALL name is written into the CALL token PAY by
   `PATCHTOK` at `CN_DONE`. FIXUP then resolves it once at `FIX_DONE` via `FIND_SUB` and patches
   the CALL token with the subroutine's entry token index (`BW_CALLIDX`).
6. **B4 linkage.** `CONTROL` handles SUB35 (CALL: save C_SPC in `BW_RETADDR`, jump to resolved
   PAY), SUB36 (`SUBROUTINE` header: no-op) and SUB40 (`RETURN`: C_SPC = `BW_RETADDR`).
   Single-level, single-CALL, up to 2 subroutines (name table 2 pairs).

Causality proof (C oracle): at B4 entry the CALL token (index 3 in the A/B deck) carries
`PAY = 0o13` = the SUBROUTINE entry; the name table holds `SUBNAM0 = 0o646643` and
`SUBENT0 = 0o17`; calling SUB reaches `X=56.78`, RETURN returns to `PRINT`.

## 4. Task 2: decisive SIMH gates (all `plumbing=PASS`, all `КОНЕЦ ЗАДАЧИ`)

| Gate | image | deck | prn0 `21` line | Verdict |
|:--|:--|:--|:--|:--|
| A | `2048_B9C_A` | `deck_B9C_A.b6` (`CALL SUB`) | ` 21 -0056.78  3000.00` | PASS |
| B | `2048_B9C_A` (byte-identical) | `deck_B9C_B.b6` (`CALL OTHER`) | ` 21 -0078.90  3000.00` | PASS |
| PATCH | `2048_B9C_PATCH` | `deck_B9C_A.b6` | ` 21 -0061.70  3000.00` | PASS |
| RESTORE | `2048_B9C_A` (byte-identical to A) | `deck_B9C_A.b6` | ` 21 -0056.78  3000.00` | PASS |
| GOTO 100 | `2048_B9_A` | `deck_B9_A.b6` | ` 21 -0012.34  3000.00` | PASS |
| GOTO 200 | `2048_B9_A` | `deck_B9_B.b6` | ` 21 -0056.78  3000.00` | PASS |
| T1 | `2048_B9_A` | `T1_lit_A.b6` | ` 21 -0012.34  3000.00` | PASS |
| T5 | `2048_B9_A` | `T5_do_2.b6` | ` 21 -0040.00  3000.00` | PASS |

Case IDs `C10_*` in `harness/runs/` (`verdict_C10_*.json`, `localprn_C10_*.txt`), plus the
earlier `C9_*` run on the pre-cleanup build. **Causality:** A vs B uses one byte-identical
image; only the CALL name in the deck differs, so the bound entry (and the printed value)
differs. PATCH changes exactly one machine word in N+2 (`L_TEN`, f32(10) -> f32(11)) plus the two
recomputed zone checksums; the name binding is unchanged, but on-machine digit construction
yields a different literal, so `56.78 -> 61.70`. RESTORE is byte-identical to A and returns
`56.78`. `cmp -l 2048_B9C_A 2048_B9C_PATCH` differs in 3 words (9 bytes).

## 5. Word budget / invariants (final `2048_B9C_A` vs `2048_base`)

| resource | used | limit | verdict |
|:--|--:|--:|:--|
| N+3 converter | 55 | 58 | PASS |
| N+2 changed words | 540 | 649 | PASS |
| N+2 forbidden band 526..900 | 0 | 0 | PASS |
| body N+1 changed words | 639 | 998 | PASS |
| keeper `body[0o26]` | `0o1000040000000` | preserved | PASS |
| LEX code | 742 hw | 829 slots | PASS |

## 6. Supported subset / unsupported (honest)

**Supported and SIMH-proved:** literals and `+ - * /` with parentheses; `PRINT <label>,X` with
`Fw.d`; SQRT/ABS/MOD; DO; 1..3 digit labels in GOTO/IF/FORMAT; arithmetic IF; **one CALL with
name binding to one of up to two SUBROUTINE blocks, with RETURN**; `END`.

**Still unsupported:** nested/recursive CALL, argument lists, COMMON blocks, more than two
subroutines or more than one CALL per program, computed GOTO, logical IF, arrays, COMPLEX,
double precision, DSQRT, READ/file I/O, 5-digit labels.

## 7. Reproduce

```
cd /tmp/.private/azizz/opencode/b9-labels
python3 build/b9_labels_build.py --build B9_A
python3 build/b9_call_build.py --build B9C_A
python3 - <<'PY'
import sys,shutil; sys.path.insert(0,'build')
from build_e2e import rz,wz,N,MASK,f32
import b5_build as B
shutil.copy2('images/2048_B9C_A','images/2048_B9C_PATCH')
z=rz('images/2048_B9C_PATCH',N+2); z[B.L_TEN]=f32(11.0)&MASK; wz('images/2048_B9C_PATCH',N+2,z)
PY
python3 harness/drive_b.py --case X --deck decks/deck_B9C_A.b6 --image images/2048_B9C_A --session bh-X
python3 harness/drive_b.py --case Y --deck decks/deck_B9C_B.b6 --image images/2048_B9C_A --session bh-Y
python3 harness/drive_b.py --case P --deck decks/deck_B9C_A.b6 --image images/2048_B9C_PATCH --session bh-P
```

DONE
