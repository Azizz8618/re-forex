# Master-план: полный FORTRAN 77 в FOREX 5.00

**Цель:** перейти от верифицированного подмножества (76/200 = 38 % подтверждено,
96/200 = 48 % с учётом частичного) к **полной поддержке X3.9-1978** /
FORTRAN 77, сохранив проверяемость и эффективность.

**База:** `docs/plan-f77-full/01-f77-standard-matrix.md` (200 элементов A–K),
`02-madlen-extension.md`, `03-fortran-path.md`, `04-verification.md`.
Версия изделия: **FOREX 5.00 / 19.11.2026 (re-forex)**.

---

## 1. Стартовое состояние

| Метрика | Значение |
|---|---:|
| Элементов стандарта X3.9-1978 | 200 |
| OK (исполнимо подтверждено) | 76 (38 %) |
| PARTIAL | 20 |
| NO | 4: `SAVE` (F11), `IMPLICIT NONE` (F13, вне F77), `READ(u,fmt)` (J4), `END=` (J7) |
| UNKNOWN | 100 (в основном 66 интринзиков) |
| Реальные F77-программы | Глиссада 14/14, Dhrystone 18+4, Whetstone (risk low) |
| Тестовая приёмка E5 | 8/8 gold, 3/3 cross `*FTN` |

**Ключевые P0-риски:** 6-символьная коллизия имён (A5 — молчаливая компиляция в
неверную программу), `CHARACTER` (B6/D3/I1–I4/H7/F2/F8 — нативно в базе 4.13;
2.02 требует Hollerith-понижения), `SAVE` (F11 — молчаливое изменение семантики при удалении).

---

## 2. Стратегия (гибрид)

1. **Fortran-путь (основной, ~80 % элементов)** — `F77PREP` rules 1–19 +
   `F77LIBR` (7 → 13+ процедур). Даёт проверяемость на исходном уровне, нулевую
   стоимость при execution для lowered-форм.
2. **МАДЛЕН-spine (минимальный, ~20 %)** — правки `LO*SYN` (лексемы/автомат
   1517..1777), `LO*GEN` (таблица 29 операторов 0532..0623, inline-генерация),
   `FORMAT` (таблица передач 0o77xxx). Только там, где lowering невозможен:
   новые FORMAT-дескрипторы, unformatted I/O, настоящий CHARACTER в GENERATOR,
   REWIND/BACKSPACE/ENDFILE, vero IOSTAT/EOF.
3. **Инкапсуляция версий:** 4.13 — семантическая база и oracle (CHARACTER,
   Dhrystone/Whetstone/kermit); 2.02 — исторический эталон системного баннера
   и единственный исполняемый здесь bootstrap-компилятор; `*FTN`/`*FORTRAN` —
   cross-эталоны; `FOREX 5.00 / 19.11.2026` — версия изделия во всех артефактах.

---

## 3. Этапы и трудоёмкость

| Этап | Содержание | Дни | Вход → выход | Критерий готовности |
|---|---|---:|---|---|
| **P0** | Инвентаризация и контракты: матрица 200 элементов, golden SHA, 20/20 gate | 3 | `01-f77-standard-matrix.md` → `tests/plan-f77-full/manifest.sha256` | счётчики 76/20/4/100 воспроизводимы; 20/20 rc=0 |
| **P1** | Диагностика 6-символьных коллизий (A5) | 2 | правка `F77PREP` rule 20 |]> `AAAAAAX` → явная ошибка, не молчаливое слияние |
| **P2** | `F77PREP` инфраструктура: SEQ 73–80, continuation, динамические метки `777004`, список переменных (M1–M4) | 5 | `03-fortran-path.md` §1 → новый `F77PREP.FTN` | 20→132 знака, >20 строк, метки без коллизий |
| **P3** | Decl-правила 1/2/9/10/11/15/16: IMPLICIT, SAVE, PRINT *, READ *, END=/ERR=, ASSIGN/computed GO TO, EQUIVALENCE | 6 | rules 9–16 | все NO/P1 declarations Lukily через lowering |
| **P4** | CHARACTER любой длины (rules 7/8/12/13/14), `F77LIBR`: STRCAT/SUBSTR/ISTRCM | 5 | `W=ceil(n/6)`, 6-байтовые слова | n=1..30, подстроки, `//`, сравнения, печать A/5A6 |
| **P5** | Интринзики: 12 нативных + ~11 inline (rule 19) + 6 новых в F77LIBR | 4 | 80 элементов K → ≥90 % OK | 66 UNKNOWN закрыты обёртками/алиасами |
| **P6** | I/O через lowering: list-directed READ, END=/ERR= sentinel, DP `D22.15` | 4 | J4/J5/J6/J7 | gold-пары 32/32 |
| **P7** | МАДЛЕН-spine: дескрипторы E/G/L, unformatted I/O, REWIND/BACKSPACE/ENDFILE, настоящий CHARACTER, IOSTAT | 7–10 | `02-madlen-extension.md` таблица → patch в SYN/GEN/FORMAT | инвариант 1024 слов, opcode-сверка, L0–L5 |
| **P8** | Полная верификация: 32 unit, 32 gold, 8 cross, 4 real, 9 negative, gate 20/20 | 5 | `04-verification.md` → отчёт | **200/200 OK/PARTIAL→OK, 0 FAIL** |
| **P9** | Публикация: README, checklist, DWG DRAKON-схемы, bundle, GitHub+SourceCraft | 2 | репозиторий | оба remote на одном HEAD |

**Итого: 43–46 чел.-дн.** (Fortran-путь ~27, МАДЛЕН ~7–10, верификация ~7, инфраструктура ~5).

---

## 4. Детальные спецификации

- **Матрица/приоритеты/счётчики:** `01-f77-standard-matrix.md` §12 (P0–P3, вне F77).
- **МАДЛЕН-правки и workflow с симтаблицей:** `02-madlen-extension.md` (12 групп, 10–150 слов, инвариант 1024 слова, L0–L5).
- **Fortran-rules 9–19, F77LIBR, границы:** `03-fortran-path.md` (~25 из 30 конструкций без ассемблера).
- **Тестовая пирамида:** `04-verification.md` (L0 32, L1 32, L2 8, L3 4, L4 9, Gate 20/20).

---

## 5. Критерии «полный F77»

```
F77_FULL = (OK+P0/P1→OK = 200/200) and
           (gold 32/32) and (cross 8/8) and
           (real 4/4) and (negative 9/9) and (gate 20/20) and
           (0 FAIL in check-label-semantics / check-text-decoded /
            check-extract-codes / check-drakon / check-source-words)
```

**Исключения (явно зафиксированный exclude-лист):**
- `IMPLICIT NONE`, `DO WHILE/END DO`, `RECORD`, `ARM` — вне X3.9-1978; считаются отдельным реестром расширений F77PREP.
- Рекурсия — вне F77.
- Числовая семантика 40-бит mantissa vs IEEE и `D`-дескриптор — отдельные контрольные векторы, не断言 «полной точности».
- Байтовая идентичность симтаблицы при обратной сборке — недостижима (`docs/05-roundtrip.md`), заменена opcode-сверкой + homeomorphic mapping.

---

## 6. Управление рисками

| Риск | Митигация |
|---|---|
| Симтаблица при сборке оверлеев | JSON-manifest, opcode-поле `[ИР:3][КОП:6][АДР:15]`, golden SHA, 1024-словный инвариант |
| Конфликт имён с системной библиотекой | имена ≤6, не системные (урок `OCTTDE*`) |
| ГОСТ/ISO/TEXT/УПП decoding | `tools/besm6_text_scan.py` (12 кодировок) + `dtran -D` (только Pascal backend) |
| SAVE меняет семантику | `SAVE → COMMON+DATA`, НЕ удаление |
| CHARACTER 2.02/4.13 | 4.13 — база и oracle; 2.02 — исторический эталон баннера и bootstrap |
| IO cross-эталоны | `*FTN` и `*FORTRAN` с допуском 1e-5, а не только internal gold |

---

## 7. Порядок работы

1. Прочитать `00-master-plan.md`, затем `01` (матрица) и свой раздел (`02`/`03`/`04`).
2. Каждый этап P0–P9: отдельный коммит, 20/20 gate до и после, логи в `logs/f77_full_*.txt`.
3. Статус этапа — только по факту (gold/cross/регрессия), не по «почти готово».
4. По завершении P9 — обновить `README.md`, `checklist/STATUS.md`, DRAKON-схемы и отправить в GitHub/SourceCraft.
