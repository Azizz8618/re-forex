# FOREX 5.00 canonical contour product

> УСТАРЕЛО как продукт: текущий канонический образ — `docs/105`
> (`f483f6ca…4120b`, 57/58 слов, полный IR‑LIT + знак, без `/10`). Этот документ
> сохраняется как предыдущий канонический вариант (`f620c72a…`, 58/58, `/10`).

> Применено в репозитории главным агентом: сборщики лежат в `tools/forex500/`,
> колоды и манифест — в `tests/plan-f77/87-canonical/`, этот документ —
> `docs/103-canonical-product.md`. Ниже пути `build/`, `images/` и `decks/`
> относились к рабочему каталогу субагента; в репозитории используйте
> `tools/forex500/` и `tests/plan-f77/87-canonical/`. Манифест
> `sha256.manifest` проверен `sha256sum -c` 28/28 в исходном workspace.
> Главный агент повторил сборку из файлов репозитория: base `a98e8109…`,
> canonical `f620c72a…`, B `21325b50…`, restore `f620c72a…` — совпало.

One image, one deck, one build command. This is the consolidation of the proven
docs/100 chain (the largest honest subset); nothing is re-derived here.

## Artifacts

- `images/2048_forex500_canonical` - 58/58-word (116 halfword) contour with
  2+2 GOST digits and an on-machine sign. SHA-256 `f620c72a...541be`.
- `decks/deck_canonical.b6` - only `ДИС 41(2048)^` plus
  `*TRANS:OURMRK*,,412350` and standard Fortran framing (X=12). SHA-256
  `6520677f...38d0a`.

Printed result (KONECHЗАДАЧИ reached): ` 21 -0000.34  3000.00` for X=12 and
` 21 -0000.58  3000.00` for the X=34 deck. Scaling is `/10`.

## Rebuild from the repo tool alone

The repo tool `tools/build_zone2350_contour.py` is the only builder; everything
else is a verbatim copy of the proven scripts. The canonical workspace vendors
the tool and fixtures under `fixtures/repo/`, so no subagent workspace is needed.

```
cd /tmp/.private/azizz/opencode/canonical
python3 build/build_canonical.py
```

Equivalent manual sequence (base first, then the sign-augmented builder):

```
cp <repo>/tools/build_zone2350_contour.py build/
python3 build/build_zone2350_contour.py base --out images          # SHA a98e8109...
python3 -c 'import sys; sys.path.insert(0,"build"); import final_sign as S; \
  S.build("forex500_canonical", sign="plain", drop_last_ati=True, floor_acc=True)'
```

Required read-only inputs (vendored copies in `fixtures/repo/`):

```
src/newcomp/O412C.FTN
src/newcomp/CODEGEN.deck, src/newcomp/EMIT.FTN      (import-time only)
tests/plan-f77/84-wide-output/installer.py, codegen.py
tests/plan-f77/69-full-emitted-body/o412d_words.hex
tests/plan-f77/65-m80-install/ovl_our.hex
/usr/local/share/besm6/2048                          (system base, read-only)
```

`build_canonical.py` asserts the expected SHAs for the base, canonical, B and
restore images, so a drift in any fixture fails the build.

## Exact remaining limits

- `/10` scaling stays: `sqrt(X)/10`; no numeric accuracy claim beyond ACPU text.
- Sign comes from the float's bit 40 via the SIGNBIT patch, not from a card minus.
  Only deck digits 1..4 are proven (`NEG31` is invalid for zero).
- DSQRT impossible: no double FPU, software DP > 100 instructions.
- Descriptive `READ(u,fmt)` impossible; only the literal card-buffer read at
  `0o64012` works.
- No full compilation in the contour (no FRONT/CODEGEN/EMIT records).
- IR parsing: leading LIT digit only (x100); `777001..777004` not parsed,
  emitters `777010/777011` absent.
- Zone `N+4` impossible (docs/101); 58 words is a hard limit. Do not exceed it.
- FRONT-IR input (docs/99) is a SEPARATE variant, not merged: the 58 words are
  exhausted and the FRONT path would need `N+4`.

Full evidence: `report.md`; hashes: `sha256.manifest`.
