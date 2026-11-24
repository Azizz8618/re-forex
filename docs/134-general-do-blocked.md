# Generalized `DO` from real Fortran source: BLOCKED

> СТАТУС: **BLOCKED** (честно). Обобщённый `DO` (init/limit/step, обновление
> переменной, `S=S+I`) запрограммирован в workspace‑копии сборщика, но ни один
> образ не прошёл: расширение LEX в дополнительные области body ломало контур
> даже для не‑DO decks (`КОНТРОЛЬ КОМАНДЫ`/hang в C‑oracle); workspace‑harness
> не загружался. Word budget соблюдён (55/58 N+3, 543/649 N+2, 301/998 N+1).
> Отдельный факт: `limit 5` и `6` при step 2 дают одинаковый `S=9`, для A/B
> нужен limit 7 или step 1. Рабочее исправление не найдено, PASS не заявлен.

Workspace: `/tmp/.private/azizz/opencode/b8-gendo/`. Copies only; no repository edit,
no live disk, no tmux session 0, no C `dispak` patch, no system compiler, no `777005`
IR card. C `dispak` was used only as an advisory oracle; a full-SIMH verdict was
required but could not be obtained (blocker B). Emulator SHA verified in the
harness: `d058305796bcd0aaf108056f595ee2a222762abe31cf3bb59f1697c9473ca675`.

## 0. Outcome

**BLOCKED.** The source-level generalized `DO` parser and the float loop-variable
update were implemented in a workspace copy of `b_final_do_build.py`, and several
images were built (final attempt `2048_GENDO_A7`,
SHA `f7f53fddf71430bc496530bbe0dd335fd9dbfde1e08bfab8b3a12732eaea870f`). None of
the attempted images is a measured success:

* the advisory C oracle either hangs (`rc -9`) or ends in `КОНТРОЛЬ КОМАНДЫ`
  / `ЗАТЕРТО СПО`, and this happens even for a **non-DO** deck (`T1_lit_A`), so the
  contour itself is broken by the code-layout extension (blocker A);
* the authoritative SIMH harness cannot boot **any** image in this environment,
  including the unchanged base image `2048_MODFINAL_B2` (blocker B).

Therefore the decisive A/B, one-word PATCH/RESTORE and `КОНЕЦ ЗАДАЧИ` gates for
generalized `DO` were **not** demonstrated. No claim of a working generalized
`DO` image is made.

## 1. Blocker A (exact): extending the proven LEX code layout breaks the contour

Base builder `b_final_do_build.py` fills its five code regions exactly and places
one `LONG UJ` guard at each region end. Generalized `DO` needed ~60 extra words,
so I appended two free N+1 body regions (`body[0o552..0o602]` and
`body[0o604..0o700]`, both listed as free in docs/120) and let the assembler spill
into them. Controlled bisection on workspace copies identified the failure:

| builder variant (all workspace copies) | LEX words | C oracle `T1_lit_A` |
|:--|--:|:--|
| original `b_final_do_build.py` (base B2) | 377 | `21 -0012.34`, no error |
| original + only extra code regions | 377 | `21 -0012.34`, no error |
| original + regions + one extra dispatch mode | 379 | `21 -0012.34`, no error |
| + `M_DONUM` 'I' detection | 381 | `21 -0012.34`, no error |
| + init-digit capture in mode 8 | 398 | `21 -0012.34`, no error |
| + dead-code spill into the new regions | 407 | `21 -0012.34`, no error |
| + mode 9/20 limit/step parse (one new `Z(0o24,...)` pair) | 432 | **hang / `КОНТРОЛЬ КОМАНДЫ` at PC 0** |
| same, but with the new `Z` pair removed | 428 | `21 -0012.34`, no error |
| unified single-`Z` limit/step parse | 429 | **hang** |
| Z-free FPU-add digit builder (`A7`) | 435 | **hang** |

A `T1_lit_A` deck has no `DO` statement at all, so the failure is not in the new
semantics but in the contour's code layout/guard behaviour once the extra digits
code is emitted at those slot positions. Specific observed failures:

* `oracle/A4_T1/out.txt`: `ЗАТЕРТО СПО`, code word at PC `0o22361`;
* `oracle/A5_T1/out.txt`: `КОНТРОЛЬ КОМАНДЫ`, PC `0` (`atx 0`);
* `oracle/A7_T1_lit_A/out.txt`: timeout, no `21` line, no completion.

I tried the docs/129 structural remedy (a `LONG UJ` in every unwritten slot of a
code region, so no fall-through can reach a zero word). It did not remove the
failure. I also tried reusing the proven `M_NUM` digit chain with one exponent
word pair instead of two; that variant (`T_LIMONLY`) passed `T1_lit_A` but did not
implement step parsing. The root cause was not isolated within this task's scope.

## 2. Blocker B (exact): SIMH harness cannot boot in this session

`harness/drive_b.py` (workspace copy, isolated tmux socket under
`harness/runs/tmux`, never session 0) fails before any deck is fed:

```
Traceback (most recent call last):
  File ".../drive_b.py", line 138, in main
    raise TimeoutError("no ДATA: boot marker in capture-pane")
TimeoutError: no ДATA: boot marker in capture-pane
```

This is **not image-specific**: the unchanged base image `2048_MODFINAL_B2`
also fails identically (`runs/base_run.log`, `runs/base2_run.log`,
`runs/okbase.log`). The console pane stops at
`>>> MUX: clear, PRP = 01400` / `Booting the OS now...`; `ДATA:` never appears.
I also made a workspace-local SIMH tree (`simh/OSZAGR`, `simh/BIN/besm6`,
`simh/ACPU`) and pointed the harness copies at it; the result was the same.
An intermediate cause was `/tmp` filling to 100% with oracle traces; after
cleanup 1.4 G was free, but the boot failure persisted. No emulator, OS image,
tmux session 0 or shared device was modified by this task.

## 3. Semantic finding about the requested A/B

With correct Fortran `DO` semantics and a body that only uses `I`:

```
DO 10 I=1,5,2   -> I = 1,3,5  -> S = 9
DO 10 I=1,6,2   -> I = 1,3,5  -> S = 9   (7 > 6, so no extra iteration)
```

the two decks suggested in the task **must print the same accumulated value**.
A step of 2 from 1 never lands on 6. A genuinely decisive limit A/B with this
body is `limit 5 -> 9` versus `limit 7 -> 16`; the one-word patch gate can be
`step 2 -> 1` (`limit 5 -> 15`). If a strict `5` vs `6` A/B with differing output
is required, the body must also depend on the limit (e.g. `S=S+I+K`), or the
termination would have to be non-Fortran (`I >= limit`), which I did not do.

## 4. What was implemented in source (FACT about the workspace builder)

Workspace file: `build/b_final_do_build.py` (copy of the base builder). Changes:

1. **Label / init parse (mode 8).** `DOPHASE` phases 0..4 now separate the two
   label digits from the digit after `I=`. The init digit is converted to a BESM
   float and stored in `D_INIT`. This fixes an earlier off-by-one where the
   second label digit `0` was taken as the init value (observed in C MTR:
   `MTR 30075L atx ...`, `C_CH = 0o60`).
2. **Limit / step parse (mode 9 plus a unified handler).** The first comma in
   `DO 10 I=init,limit,step` follows **init** (verified in C oracle traces), so
   mode 9 now reads the first digit after that comma as the **limit**. A phase
   flag switches the same digit path to the **step** after the second comma;
   end-of-card without a step defaults to `f32(1.0)`. `D_BOUND` holds the limit,
   `D_NLIMIT = f32(-limit)` is built with `avx` sign flip (docs/129).
3. **Loop-variable update and crossing test** in `DO_ITER`: `I = init`; each
   iteration adds `I*10` (or the literal addend) to `N+2[33]` in the SAME 10x
   convention, then `I += step` (FPU `a+x`) and `diff = I + (-limit)`. `diff == 0`
   (I equals limit) and negative diff continue; positive diff (I > limit) exits.
   The sign test reuses the proven `ASX L_SHRTAB; AAX 1; UZA` sequence.
4. **Body selector.** `M_DONUM` distinguishes a digit body (`S=S+<literal>`,
   unchanged base behaviour) from `S=S+I` (`D_IBODY = 1`).
5. Pre-scan of the `DO` label (`D_DOLAB`) and the existing keyword/FORMAT windows
   were preserved; no new opcode and no host-computed digit was introduced.

None of these source-level changes has a passing machine-code verdict (blocker A).

## 5. Word budget of the final attempted build (`2048_GENDO_A7`)

Whole-image diff against `images/2048_base`, measured with `build_e2e.rz`:

| resource | used | limit | verdict |
|:--|--:|--:|:--|
| N+3 converter + cells | 55 | 58 | within budget |
| N+2 changed words | 543 | 649 | within budget |
| N+2 forbidden band 526..900 changed | 0 | 0 | PASS |
| N+1 body words changed | 301 | 998 | within budget |
| `body[0o26]` keeper | `0o1000040000000` in both | must be kept | PASS |
| N+4 | unused | unavailable | PASS |

Build line: `N3=40/58w B4=203w LEX=435w slots=486 N2last=1024 bodycode=254w`.
Budgets are met; the failure is structural/control-flow, not capacity.

## 6. Supported subset of the *attempt* and what remains

**Attempted:** one statement per card in columns 7..72; `DO <2-digit label>
I=<1-digit init>,<1-digit limit>[,<1-digit step>]`; terminal `<label> CONTINUE`;
body `S=S+I` or `S=S+<literal>`; positive step only; single-digit fields;
default step 1; verbatim B3 dispatcher + docs/105 GOST converter; PATCH/RESTORE
via the proven docs/128 `K_PATCH` word (not exercised).

**Not achieved / remains:** any passing SIMH execution of generalized `DO`;
nested loops; multi-digit init/limit/step; negative step; array/multi-variable
DO; general expression bodies; body-target dispatch; Fortran diagnostics; ABS/MOD
regression verification on the new image.

## 7. Decks (verbatim)

`decks/G_DO_A.b6` (SHA `eb962846ae808cebad7766ece6a7b8a829023f73cc91c4eaaca2a05bc751ac17`):

```
ШИФР 410300 ЗС5^
ДИС 41(2048)^
ОЗУ 32^АЦП 32^
ЕЕВ1А3
*NAME FRX5XX
*TRANS:FRX5*,,412350
      PROGRAM MAIN
      S=0.0
      DO 10 I=1,5,2
      S=S+I
   10 CONTINUE
      PRINT 100,S
  100 FORMAT(1X,F4.2)
      END
*EXECUTE
*END FILE
``````
ЕКОНЕЦ
```

`decks/G_DO_B.b6` (SHA `c3079bf8ed829569eb5f08e9158995d610b46455ae7731bedce5124ceda5b700`)
is byte-identical except one byte at 1-based offset 154: `5` -> `6`
(`cmp -l` output `154  65  66`). Also prepared: `G_DO_C.b6` (`limit 7`),
`G_DO_NOS.b6` (no step), `G_DO_LIT.b6` (literal body), all with the same framing.

`grep 777005` on every deck: 0 hits. No `*FOREX`, `*FTN` or IR card.

## 8. Evidence index

```
build/b_final_do_build.py        generalized-DO source changes (workspace copy)
build/t_orig.py ... t_noz.py     bisection builders for blocker A
images/2048_GENDO_A7             final attempted image
decks/G_DO_{A,B,C,NOS,LIT}.b6    real Fortran source decks
oracle/A*_*/out.txt              advisory C-oracle traces/hangs (not verdicts)
runs/{base_run,base2_run,okbase,isobase_run}.log   SIMH boot failures
harness/runs/verdict_*.json      none produced (harness never reached the deck)
```

BLOCKED
