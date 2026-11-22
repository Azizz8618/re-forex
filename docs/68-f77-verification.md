# re-forex F77 track (F0+F1) — complete verification pyramid, single auditable report

- Repo: `/home/azizz/Yandex.Disk/re-forex`, HEAD `999cde42f36efe76ae29c90205fd5d7d5ffd80ab`, branch `main`.
- All six gates run sequentially on 2026-11-22 (UTC), with `HOME=/tmp/.private/azizz/opencode/re-forex-f77-verify/home`, `TMPDIR=TMPROOT=/dev/shm/re-forex-f77-verify/shm` (tmpfs, 7.6 G free; system `/tmp` is 97% full and was avoided).
- Read-only on the repo: no repo file was restored, staged, or edited by this verification. All captures, MD5 snapshots and raw stdout/stderr live under `/tmp/.private/azizz/opencode/re-forex-f77-verify/out/`.
- Pre-existing user changes were left untouched: `M tools/run_besm6_deck.py` and `?? tests/plan-f77/64-monitor-patch/`. Nothing was staged (index empty).

## 1. Gate table (all six, rc=0)

| # | Script | Date (UTC start→end) | rc | OK / PENDING / SKIP / FAIL | Key output lines | Manifest SHA |
|---|---|---|---|---|---|---|
| 1 | `tests/verify-dumps.sh` | 18:50:12Z → 18:50:12Z | 0 | 2 overlays OK / 0 / 0 / 0 | `LO_SYN offset=0o241500 size=6144 sha256=83a7e962…459366`; `LO_GEN offset=0o277500 size=6144 sha256=4f4d8e4c…2cbfd`; both `побайтовая сверка с build/LO_*.words: OK`; `OK: оверлеи LO*SYN и LO*GEN выгружены и сверены` | n/a |
| 2 | `tests/run-f77-prep.sh` | 18:50:21Z → 18:51:07Z | 0 | 21/21 cases, each PASS1+PASS2 OK / 0 / 0 / 0 | `ZF bridge: РЕАЛЬНЫЙ PERSO АРФЫ (G1), image=…/FOREX_ARFA_2320.zone`; 21 × `[caseN] PASS1 OK` + 21 × `[caseN] PASS2 OK`; `OK: все случаи пройдены на РЕАЛЬНОМ PERSO-мосте АРФЫ G1 (rc=0)`. Cases executed: 1, 2, 8–26 (IDs 3–7 do not exist as prep cases) | n/a |
| 3 | `tests/run-f77-full.sh` | 18:51:29Z → 18:51:46Z | 0 | L0 55 OK / L1 55 OK / L2 8 OK / L3 2 OK + 2 SKIP / L4 9 OK / GATE 20 OK, 0 FAIL; PENDING 0 everywhere | `F77LIBR: 13 процедур собраны в PERSO 0o2310 (для *perso:602310,cont)`; final table `L0 55/0/0, L1 55/0/0, L2 8/0/0, L3 2/0/2, L4 9/0/0, GATE 20/0(FAIL)/0`; `Итог GATE: 20/20 OK, FAIL=0`; `OK: gate 20/20; L0 55 OK / 0 PENDING, L1 55 OK / 0 PENDING` | file `logs/f77_full.sha256` SHA256 `0e059c4a0f45266df611ab1ea3b934de21f81191f63a92b9db3b6ffabb3d05d2` (364 lines); content without timestamp header SHA256 `514de5a8b72356e809303289f3dbcd2516caf1e63223236a0500f5fd88d8fda9`; header `# F77 full verification manifest — 2026-11-22T18:51:45Z` (timestamp-dependent, use the headerless digest for reproducibility) |
| 4 | `tests/run-glissade-forex.sh` | 18:52:00Z → 18:52:01Z | 0 | 14/14 lines OK / 0 / 0 / 0 | `PERSO catalog (9 modules): FOREX* LO*SYN LO*GEN FORMAT FORTLIBR XDATAPR OCTTDE* XGIVPG XTAKPG`; `catalog terminator: (0, FULWORD) OK`; `OK: 14 строк результата совпадают с эталоном (после нормализации даты)` | n/a |
| 5 | `tests/run-f77-suite.sh` | 18:52:11Z → 18:52:13Z | 0 | suite 8/8 OK; cross `*FTN` 3/3 OK; 0 FAIL | `OK base / blockif / charhollerith / dataparam / do2d / dpcomplex / intrinsics_ext / listio` (8 lines); `Итог: 8/8 случаев OK; кросс-сверка *FTN: 3/3`; `OK: F77 suite пройден полностью` | n/a |
| 6 | `python3 tests/check-f77-matrix-200.py` (the §12.4 matrix reproduction; sixth gate, see note) | 18:52:26Z → 18:52:26Z | 0 | 200 OK / 0 NO / 0 PARTIAL / 0 UNKNOWN | `строк: 200 (ожидается 200); уникальных ID: 200`; `счётчик: OK=200 NO=0 PARTIAL=0 UNKNOWN=0`; `OK: 200/200, каждая строка OK имеет исполнимое доказательство`. Bonus `--strict-proof` run also rc=0 with identical output | n/a |

Note on "six scripts": the context names five shell scripts explicitly. `python3 tests/check-f77-matrix-200.py` was added as the sixth because §12.4 of the matrix lists it as the canonical reproduction of the 200/200 claim. `run-f77-suite.sh` itself contains both accepted gates (8/8 suite and 3/3 cross), so no separate cross script exists. Both facts were verified by reading the scripts.

**Confirmed:** 8/8 suite still holds; 3/3 cross `*FTN` still holds; gate 20/20 still holds.

**SKIPs (2, all in L3, no FAIL):**
- `SKIP R03 DHRYSTONE: внешний эталон (F77_FULL_EXTERNAL=1 для прогона)` — external etalon `/home/azizz/Yandex.Disk/besm6-new/besm6.net/examples/dhrystone-forex.dub`, profile `18+4`, reason `external: внешний эталон 4.13/Дубна`.
- `SKIP R04 WHETSTONE: внешний эталон (F77_FULL_EXTERNAL=1 для прогона)` — external etalon `…/whetstone-longbottom-forex.dub`, profile `8/8 MWIPS`, same reason.
- L2 has **0** SKIP in this run (`Итог L2: 8 OK / 0 PENDING / 0 SKIP (нет эталона)` for both `*FTN` and `*FORTRAN`). The context's "L3 2 + 2 SKIP" is confirmed; there are no L2 skips.

`logs/f77_full_summary.txt` after the run: `L0|55|0|0`, `L1|55|0|0`, `L2|8|0|0`, `L3|2|0|2`, `L4|9|0|0`, `GATE|20|0|0`, `RC=0`.

## 2. Repo files changed by the runs (lead must restore; DO NOT stage)

111 tracked files were modified by these runs (110 under `logs/`, 1 under `tests/`). Nothing was restored. Exact list is saved at `/tmp/.private/azizz/opencode/re-forex-f77-verify/changed-by-runs.txt`.

Grouped:
- `logs/f77_full_run.txt`, `logs/f77_full.sha256` — from gate 3 (timestamped).
- `logs/f77_prep_v2_test.txt` plus, for each executed case (1, 2, 8–26): `logs/f77_prep_v2_case<N>.txt`, `logs/f77_prep_v2_pass1_case<N>.txt`, `logs/f77_prep_v2_pass2_case<N>.txt`, `logs/f77_prep_v2_pass1_case<N>.err.txt`, `logs/f77_prep_v2_pass2_case<N>.err.txt` — from gate 2 (106 files total: 1 + 21×5 = 106; see list).
- `logs/f77_suite.txt` — from gate 5. (`logs/f77_cross_ftn.txt` was rewritten with byte-identical content, MD5 unchanged, no restore needed.)
- `logs/glissade_run_full.txt` — written by gate 4 and also by gate 3's internal L3 glissade deck.
- `tests/forex-glissade/output.new.txt` — **tracked, outside `logs/`**; written by gate 4 (`OUT` in the script). This is the easy-to-miss one.

Files the scripts rewrite but whose content is byte-identical to HEAD (MD5 unchanged; restore optional): `logs/f77_full_matrix.txt`, `logs/f77_full_gold.txt`, `logs/f77_full_cross_ftn.txt`, `logs/f77_full_cross_fortran.txt`, `logs/f77_full_real.txt`, `logs/f77_full_negative.txt`, `logs/f77_full_gate.txt`, `logs/f77_full_summary.txt`, `logs/f77_cross_ftn.txt`, and the prep `f77_prep_v2_lowered_*.f77` / `f77_prep_v2_result_*.txt` / `f77_27_real_adapted_*.f77` artifacts. Verify-dumps and the matrix checker wrote nothing into the repo.

## 3. Exact proposed replacement text for `docs/plan-f77-full/00-master-plan.md` (do not apply — lead edits)

### 3.1 Header, lines 3–5 — replace with:
```
**Цель:** зафиксировать достигнутый критерий полной поддержки X3.9-1978 /
FORTRAN 77 (200/200 = 100 % элементов имеют исполнимое доказательство по §0.2
матрицы) и сохранить проверяемость и эффективность.
```
(Drop the old "перейти от верифицированного подмножества (76/200 …)" framing; it is already achieved.)

### 3.2 §1 table, lines 15–23 — replace the block with:
```
| Метрика | Значение |
|---|---:|
| Элементов стандарта X3.9-1978 | 200 |
| OK (исполнимо подтверждено, §0.2 матрицы) | 200 (100 %) |
| PARTIAL | 0 |
| NO | 0 |
| UNKNOWN | 0 |
| Реальные F77-программы | Глиссада 14/14 в gate; Dhrystone/Whetstone — SKIP в штатном прогоне (external 4.13/Дубна, `F77_FULL_EXTERNAL=1`) |
| Тестовая приёмка E5 | 8/8 gold, 3/3 cross `*FTN` |
| Пирамида P8 (факт) | L0 55 OK, L1 55 OK, L2 8 OK, L3 2 OK + 2 SKIP, L4 9 OK, GATE 20/20 OK |
```

### 3.3 §1 "Ключевые P0-риски", lines 25–27 — replace with:
```
**Бывшие P0-риски закрыты исполнимыми доказательствами:** 6-символьная коллизия
(A5), `CHARACTER` (B6/D3/I1–I4/H7/F2/F8), `SAVE` (F11). Оговорка: OK здесь означает
«есть исполнимое доказательство» по §0.2 матрицы, а не нативную поддержку ядром
2.02; для J2/J4/J23/J24 доказательство получено через F77PREP + реальный
PERSO-мост АРФЫ G1 (Э63/Э70), нативный путь — `NEEDS-RUNTIME-REBUILD`
(`01-f77-standard-matrix.md` §12.5).
```

### 3.4 §3, lines 48–63 (heading + P0–P9 table + total) — replace the whole block with:
```
## 3. Этапы и трудоёмкость (фактический статус на 22.11.2026)

| Этап | Содержание | Статус | Дни (план) | Вход → выход | Фактический критерий / доказательство |
|---|---|---|---:|---|---|
| **P0** | Инвентаризация и контракты: матрица 200 элементов, golden SHA, 20/20 gate | **ЗАКРЫТ** | 3 | `01-f77-standard-matrix.md` → `tests/plan-f77-full/manifest.sha256` | §12.1: 200/200 OK, 0 NO/PARTIAL/UNKNOWN; gate 20/20 rc=0; манифест `logs/f77_full.sha256` |
| **P1** | Диагностика 6-символьных коллизий (A5) | **ЗАКРЫТ** | 2 | правка `F77PREP` rule 20 | A5 OK в матрице; >6 знаков диагностируются, не сливаются молча |
| **P2** | `F77PREP` инфраструктура: SEQ 73–80, continuation, динамические метки `777004`, список переменных (M1–M4) | **ЗАКРЫТ** | 5 | `03-fortran-path.md` §1 → новый `F77PREP.FTN` | `run-f77-prep.sh` 21/21 case (IDs 1, 2, 8–26), PASS1+PASS2 OK, rc=0 |
| **P3** | Decl-правила 1/2/9/10/11/15/16: IMPLICIT, SAVE, PRINT *, READ *, END=/ERR=, ASSIGN/computed GO TO, EQUIVALENCE | **ЗАКРЫТ** | 6 | rules 9–16 | F 19/19 OK; gate `implicit_ok` / `endread_ok` / `save_ok` OK |
| **P4** | CHARACTER любой длины (rules 7/8/12/13/14), `F77LIBR`: STRCAT/SUBSTR/ISTRCM | **ЗАКРЫТ** | 5 | `W=ceil(n/6)`, 6-байтовые слова | I 7/7 OK; E5 `charhollerith` OK |
| **P5** | Интринзики: 12 нативных + ~11 inline (rule 19) + 6 новых в F77LIBR | **ЗАКРЫТ** (профильно) | 4 | 80 элементов K → 80/80 OK | K 80/80 OK; K05 численно (49), K06 отрицательным контролем (17); `intrinsics_ext` OK |
| **P6** | I/O через lowering: list-directed READ, END=/ERR= sentinel, DP `D22.15` | **ЗАКРЫТ** (профильно) | 4 | J4/J5/J6/J7 | J 28/28 OK через F77PREP + реальный PERSO-мост АРФЫ G1 (Э63/Э70); оговорка §12.5: IOSTAT 0/−1, ≤8 слов на Э70, `ACCESS='DIRECT'`/`RECL` не проверены |
| **P7** | МАДЛЕН-spine: дескрипторы E/G/L, unformatted I/O, REWIND/BACKSPACE/ENDFILE, настоящий CHARACTER, IOSTAT | **СНЯТ С КРИТИЧЕСКОГО ПУТИ**; нативный путь — `NEEDS-RUNTIME-REBUILD` | 7–10 | `02-madlen-extension.md` таблица → patch в SYN/GEN/FORMAT | цель 200/200 достигнута Fortran-путём; нативный путь требует правки `monitor80-re` (`01-f77-standard-matrix.md` §12.5), 20–40 чел.-дн. минимум |
| **P8** | Полная верификация: gate 20/20 + L0–L4 + E5 | **ЗАКРЫТ** с оговорками | 5 | `04-verification.md` → отчёт | L0 55 OK, L1 55 OK, L2 8 OK, L3 2 OK + 2 SKIP, L4 9 OK, GATE 20/20; E5 8/8 + cross 3/3. Плановые 32/32 и real 4/4 не совпадают с фактом — см. §4 |
| **P9** | Публикация: README, checklist, DWG DRAKON-схемы, bundle, GitHub+SourceCraft | **ОСТАЁТСЯ ОТКРЫТЫМ** | 2 | репозиторий | Обновить `README.md`, `checklist/STATUS.md`, DRAKON-схемы, отправить оба remote на один HEAD; гейтами не подтверждено |

**Остаток работы:** P9 (публикация) и, опционально, нативный P7 (`NEEDS-RUNTIME-REBUILD`, 20–40 чел.-дн. минимум). Историческая оценка 43–46 чел.-дн. относится к исходному плану, а не к оставшемуся объёму.
```
(Закрыты: P0–P6, P8. Снят с критического пути: P7. Остаётся открытым: P9.)

### 3.5 §4 references, lines 69 and 72 — replace those two lines with:
```
- **Матрица/приоритеты/счётчики:** `01-f77-standard-matrix.md` §12.1/§12.2/§12.5 (200/200 OK; P0–P6 закрыты; P7 снят с критического пути; P9 открыт).
- **Тестовая пирамида (факт P8):** `04-verification.md`, `logs/f77_full_summary.txt` (L0 55, L1 55, L2 8, L3 2 + 2 SKIP, L4 9, Gate 20/20); E5 `logs/f77_suite.txt` 8/8 + `logs/f77_cross_ftn.txt` 3/3. Плановые L0/L1 32 и L3 4 в `04-verification.md` устарели.
```

### 3.6 §5 criteria, lines 78–84 (code block) — replace the block with:
```
F77_FULL = (OK = 200/200 по §0.2 матрицы) and
           (L0 55/55) and (L1 55/55) and (L2 8/8) and
           (L3 2/2 OK + 2 SKIP: Dhrystone/Whetstone, внешний эталон 4.13/Дубна,
            F77_FULL_EXTERNAL=1) and
           (L4 9/9) and (E5 8/8, cross *FTN 3/3) and (gate 20/20) and
           (0 FAIL in check-label-semantics / check-text-decoded /
            check-extract-codes / check-drakon / check-source-words)
```
Caveat for the lead: the last `0 FAIL in check-*` clause was **not re-run** in this pass (out of the six-script scope) and remains unverified here; keep it in the criteria but do not claim it as freshly verified.

### 3.7 §7, line 110 — optional consistency tweak:
```
2. Каждый закрытый этап P0–P8: отдельный коммит, 20/20 gate до и после, логи в `logs/f77_full_*.txt`; P9 — публикация после обновления статуса.
```

## 4. Contradictions between the 200/200 claim and actual gate output / between plan and matrix

Reported plainly:

1. **Primary (the one being reconciled).** Master plan `00-master-plan.md:3-5,15-23,25-27` still states 76 OK / 20 PARTIAL / 4 NO / 100 UNKNOWN (38 % confirmed, 48 % with partial). Matrix `01-f77-standard-matrix.md:397-410` §12.1 states 200 / 0 / 0 / 0, and `check-f77-matrix-200.py` confirms it on the current HEAD. This is a stale-document contradiction; §3.1–3.3 above fix it.

2. **Pyramid counts in the plan are stale, not a gate failure.** `00-master-plan.md:60` (P8 "32 unit, 32 gold, … real 4/4"), `:72` ("L0 32, L1 32, L2 8, L3 4, L4 9"), and `:80` ("gold 32/32 … real 4/4") disagree with the produced output: **L0 55, L1 55, L3 2 OK + 2 SKIP**. The "real 4/4" criterion is therefore **not demonstrated by the default gate run** (Dhrystone and Whetstone are SKIP; they rely on prior external evidence at `01-f77-standard-matrix.md:22` and `12-intrinsics-coverage.md`/docs). §3.4–3.6 above fix the numbers.

3. **"26/26" prep label is a mislabel, not a discrepancy in results.** The context says `run-f77-prep.sh` 26/26, but the script contains exactly 21 `run_case` invocations (`tests/run-f77-prep.sh:381-401`, IDs case1, case2, case8–case26; case3–7 do not exist). The matrix itself documents `Прогон 21/21 case rc=0` at `01-f77-standard-matrix.md:497`. The correct statement is **21/21 cases, each PASS1+PASS2 OK**; the "26" is the highest case ID, not the case count.

4. **"200/200 OK" is a documentation-status claim, not 200 freshly executed independent proofs.** `tests/check-f77-matrix-200.py` parses the matrix and checks that every OK row has a non-empty evidence column; it does not re-execute each referenced artifact. The six executed gates independently cover a subset (55 L0 unit probes, 55 L1 gold pairs, 8 cross, 9 negative, 21 prep cases, 14/14 glissade, 8/8 + 3/3 E5). No gate produced a line asserting "200/200". So the 200/200 is consistent with, but not derived from, the gate output. Moreover the matrix itself downgrades the semantic strength at `01-f77-standard-matrix.md:416-424` and `:479-503`: confirmation is **"профильное"** (IOSTAT 0/−1, ≤8 words on Э70, `ACCESS='DIRECT'`/`RECL` unverified) and the native path is **`NEEDS-RUNTIME-REBUILD`**. Publishing "full X3.9 support" without this caveat would be an overclaim relative to the evidence.

5. **Internal inconsistency in the matrix about F13 (`IMPLICIT NONE`).** `01-f77-standard-matrix.md:412-414` says F13 is "пограничная (NO)" and instructs "вычесть 1 из NO и из общего числа (199 элементов, NO=3)", but the §12.1 table at `:404,:410` has F=19/19 OK and NO=0, and `:473-475` explicitly says F13 is counted as OK via rule 1 (`tests/f77/prep-case1.f77`). The note at `:412-414` is stale and contradicts the 200/200 claim. Suggested lead fix: replace it with a sentence that F13 is counted as OK via lowering while remaining in a separate F77PREP extension registry, preserving 200/200. (Doc edit not applied.)

6. **Display quirk (not a defect).** In gate 3 stdout, the GATE row prints the FAIL count in the SKIP column (`GATE 20 0(FAIL) 0 …`), while `logs/f77_full_summary.txt` correctly records `GATE|20|0|0` and the gate log says `Итог GATE: 20/20 OK, FAIL=0`. Final rc=0.

## 5. Audit trail

- Raw captures: `/tmp/.private/azizz/opencode/re-forex-f77-verify/out/<gate>.stdout`, `.stderr`, `.rc` (rc file: `name<TAB>start<TAB>end<TAB>rc`).
- Log MD5 snapshots per gate: `out/<gate>.logs-before.md5`, `out/<gate>.logs-after.md5`; whole-run baseline `logs-md5-before.txt` (497 files) vs `logs-md5-after.txt`.
- Changed-repo-file list: `changed-by-runs.txt` (111 paths).
- Runner: `run_gate.sh` (sets `HOME`, `TMPDIR`, `TMPROOT`; captures rc and snapshots).

DONE
